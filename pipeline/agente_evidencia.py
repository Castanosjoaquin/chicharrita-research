"""Agente de evidencia de esencialidad con citas verificables.

Problema: el ranking de genes hoy se apoya en un cribado (iBeetle) cerrado, de otro orden de
insectos, y el pipeline clasico no tiene NINGUN criterio de esencialidad trazable. Este modulo arma
uno donde cada afirmacion lleva su cita textual y su fuente, y donde la cita se comprueba por
codigo, no por confianza.

Cuatro piezas, y solo la 2 usa un LLM:

  1. recolectar   busca documentos (titulo + resumen) en Europe PMC. Determinista: un documento
                  entra solo si menciona el simbolo del gen como palabra completa.
  2. extraer      un LLM llena una FICHA estructurada: afirmaciones sobre el efecto de perder el
                  gen, cada una con doc_id y una cita que debe ser literal.
  3. verificar    DETERMINISTA. La cita tiene que existir en el documento citado. Niveles:
                  exacta / normalizada (unicode, comillas, mayusculas) / difusa (casi igual, no
                  alcanza) / ausente / doc_inexistente. Solo exacta y normalizada pasan.
                  Ademas chequea coherencia lexica entre el efecto declarado y la cita.
  4. agregar      DETERMINISTA. Reglas fijas de puntaje sobre las afirmaciones que pasaron.
                  El LLM no ve ni decide el puntaje.

La metrica que importa es la TASA DE CITAS NO VERIFICABLES: cuanto de lo que extrae el LLM no se
puede respaldar. Se reporta aunque sea mala.

Limite conocido: el verificador prueba que la cita EXISTE, no que SOSTIENE la afirmacion. Una
frase real puesta en un contexto equivocado pasa el chequeo literal. Se mitiga con la coherencia
lexica y con una auditoria manual de una muestra (ver los hallazgos f15).

Uso:
    python3 agente_evidencia.py --genes 15 --backend claude --model haiku
    python3 agente_evidencia.py --autotest          # mutaciones sobre fichas ya extraidas
    python3 agente_evidencia.py --genes 15 --backend manual    # usa fichas escritas a mano
"""

from __future__ import annotations

import argparse
import csv
import difflib
import html
import json
import math
import random
import re
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

SALIDA = Path(__file__).parent / "salida"
EVIDENCIA = SALIDA / "evidencia"
EUROPEPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

# Genes con literatura fuerte, para contrastar contra los primeros de la tabla.
CONTROLES = ["Act5C", "Rpt6", "Vha55", "RpS2", "Polr2B"]

# ---------------------------------------------------------------- 1. recolectar


def simbolo_valido(simbolo: str) -> bool:
    """Un simbolo ambiguo (muy corto, lista de copias, genes l(1)...) genera falsos documentos."""
    return len(simbolo) >= 4 and ";" not in simbolo and "(" not in simbolo and " " not in simbolo


def elegir_genes(n: int) -> list[dict]:
    """Los primeros n genes de tabla_unificada.csv con simbolo de Drosophila utilizable."""
    elegidos: list[dict] = []
    if n <= 0:
        return elegidos
    with (SALIDA / "tabla_unificada.csv").open(encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            simbolo = (fila.get("gen_drosophila") or "").strip()
            if simbolo_valido(simbolo):
                elegidos.append({"locus": fila["locus"], "simbolo": simbolo,
                                 "tribolium": fila.get("mejor_hit_tribolium", ""),
                                 "fenotipo_tabla": fila.get("fenotipo_categoria", "")})
            if len(elegidos) == n:
                break
    return elegidos


def descargar(url: str, timeout: int = 40, reintentos: int = 4) -> bytes:
    """GET con reintentos: Europe PMC corta conexiones de vez en cuando y no debe tumbar toda la corrida."""
    for intento in range(reintentos):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return r.read()
        except Exception:
            if intento == reintentos - 1:
                raise
            time.sleep(2 * (intento + 1))
    return b""


def limpiar_html(texto: str) -> str:
    texto = html.unescape(texto or "")
    texto = re.sub(r"</?(?:i|b|em|strong|italic|bold|sup|sub|u)[^>]*>", "", texto)  # etiquetas en linea: sin hueco
    texto = re.sub(r"</?[a-zA-Z][^>]*>", " ", texto)
    return re.sub(r"\s+", " ", html.unescape(texto)).strip()


def menciona(simbolo: str, texto: str) -> bool:
    return re.search(rf"(?<![A-Za-z0-9]){re.escape(simbolo)}(?![A-Za-z0-9])", texto) is not None


def parrafos_con_simbolo(pmcid: str, simbolo: str, maximo: int = 3) -> str:
    """Parrafos del cuerpo (no referencias) de un articulo de acceso abierto que nombran al gen."""
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    try:
        raiz = ET.fromstring(descargar(url))
    except Exception:
        return ""
    cuerpo = raiz.find(".//body")
    if cuerpo is None:
        return ""
    elegidos = []
    for p in cuerpo.iter("p"):
        t = re.sub(r"\s+", " ", "".join(p.itertext())).strip()
        if len(t) >= 80 and menciona(simbolo, t):
            elegidos.append(t)
        if len(elegidos) == maximo:
            break
    return "\n".join(elegidos)


def recolectar(simbolo: str, maximo: int = 5, maximo_texto_completo: int = 4) -> list[dict]:
    consulta = (f'"{simbolo}" AND (RNAi OR "RNA interference" OR dsRNA OR knockdown OR "loss of function" '
                f'OR mutant OR lethal) AND (Tribolium OR Drosophila OR insect OR Hemiptera)')
    url = EUROPEPMC + "?" + urllib.parse.urlencode(
        {"query": consulta, "format": "json", "pageSize": 30, "resultType": "core"})
    datos = json.loads(descargar(url, 30))
    docs, completos = [], []
    for x in datos.get("resultList", {}).get("result", []):
        titulo = limpiar_html(x.get("title", ""))
        resumen = limpiar_html(x.get("abstractText", ""))
        texto = f"{titulo}. {resumen}" if resumen else titulo
        doc_id = f"PMID:{x['pmid']}" if x.get("pmid") else f"{x.get('source', 'EPMC')}:{x.get('id')}"
        base = {"titulo": titulo, "anio": x.get("pubYear", ""), "revista": x.get("journalTitle", ""),
                "doi": x.get("doi", "")}
        if len(resumen) >= 200 and menciona(simbolo, texto) and len(docs) < maximo:
            docs.append({"doc_id": doc_id, "tipo": "resumen", **base, "texto": texto})
        # texto completo (solo acceso abierto): los parrafos que nombran al gen, donde esta el fenotipo
        if x.get("pmcid") and x.get("isOpenAccess") == "Y" and len(completos) < maximo_texto_completo:
            pars = parrafos_con_simbolo(x["pmcid"], simbolo)
            if pars:
                completos.append({"doc_id": f"{x['pmcid']}:texto", "tipo": "texto_completo", **base,
                                  "texto": f"{titulo}. [parrafos que nombran a {simbolo}] {pars}"})
    return docs + completos


# ---------------------------------------------------------------- 2. extraer

PROMPT = """Eres un extractor de evidencia cientifica. Gen: {simbolo} (simbolo de Drosophila{trib}).
Te doy {n} documentos (titulo + resumen), cada uno con un ID.

TAREA: lista las afirmaciones que los documentos hacen sobre el EFECTO de perder o silenciar este
gen (RNAi, mutante, knockout, CRISPR) en algun organismo.

REGLAS ESTRICTAS:
1. Usa solo informacion que aparece en los documentos. Nada de conocimiento previo.
2. Para cada afirmacion, 'cita' debe ser una frase copiada LITERALMENTE del documento, caracter por
   caracter, de 300 caracteres como maximo. No parafrasees, no traduzcas, no resumas.
3. Si un documento no dice nada sobre el efecto de perder ESTE gen, no inventes nada: no lo cites.
4. 'doc_id' debe ser exactamente uno de los IDs dados.
5. Si ningun documento sirve, devuelve {{"afirmaciones": []}}.

Responde SOLO con JSON valido con este formato:
{{"afirmaciones": [{{"especie": "...", "orden": "Coleoptera|Diptera|Hemiptera|otro_insecto|no_insecto|desconocido",
 "metodo": "RNAi|mutante|knockout|CRISPR|otro", "efecto": "letal|esteril|morfologico|sin_efecto|otro",
 "texto": "la afirmacion en una linea", "doc_id": "...", "cita": "frase literal",
 "terminos_clave": ["..."]}}]}}

DOCUMENTOS:
{docs}
"""


def armar_prompt(gen: dict, docs: list[dict]) -> str:
    trib = f", ortologo en Tribolium {gen['tribolium']}" if gen.get("tribolium") else ""
    cuerpo = "\n\n".join(f"[{d['doc_id']}] {d['texto']}" for d in docs)
    return PROMPT.format(simbolo=gen["simbolo"], trib=trib, n=len(docs), docs=cuerpo)


def sacar_json(texto: str) -> dict:
    texto = texto.strip()
    texto = re.sub(r"^```(?:json)?\s*|\s*```$", "", texto)
    ini = texto.find("{")
    objeto, _ = json.JSONDecoder().raw_decode(texto[ini:])  # tolera texto sobrante despues del JSON
    return objeto


class ExtractorClaudeCLI:
    """LLM por la CLI de Claude Code en modo no interactivo. Sin herramientas, sin skills."""

    def __init__(self, modelo: str = "haiku"):
        self.modelo = modelo
        self.costo = 0.0
        self.errores = 0

    def extraer(self, gen: dict, docs: list[dict]) -> dict:
        if not docs:
            return {"afirmaciones": []}
        cmd = ["claude", "-p", "--tools", "", "--disable-slash-commands", "--no-session-persistence",
               "--system-prompt", "Eres una funcion de extraccion. Responde solo con JSON valido, sin texto extra.",
               "--output-format", "json", "--model", self.modelo]
        # cwd neutro y persistente: que no cargue el CLAUDE.md del proyecto (en Windows un directorio
        # temporal en uso no se puede borrar, por eso no se usa TemporaryDirectory)
        neutro = Path(tempfile.gettempdir()) / "agente_evidencia_cwd"
        neutro.mkdir(exist_ok=True)
        r = subprocess.run(cmd, input=armar_prompt(gen, docs), capture_output=True, text=True,
                           encoding="utf-8", timeout=240, cwd=neutro)
        try:
            sobre = json.loads(r.stdout)
            self.costo += float(sobre.get("total_cost_usd", 0))
            return sacar_json(sobre["result"])
        except (ValueError, KeyError) as e:  # respuesta no parseable: se cuenta, no rompe la corrida
            self.errores += 1
            return {"afirmaciones": [], "error_extraccion": f"{type(e).__name__}: {e}"}


class ExtractorManual:
    """Fichas escritas a mano en EVIDENCIA/manual_<simbolo>.json. Sirve de caso de ejemplo y de prueba."""

    def extraer(self, gen: dict, docs: list[dict]) -> dict:
        ruta = EVIDENCIA / f"manual_{gen['simbolo']}.json"
        return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {"afirmaciones": []}


# ---------------------------------------------------------------- 3. verificar

DASHES = dict.fromkeys(map(ord, "‐‑‒–—−­"), "-")
QUOTES = dict.fromkeys(map(ord, "‘’‚‛′"), "'")
QUOTES.update(dict.fromkeys(map(ord, "“”„‟″"), '"'))


def norm_espacios(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def norm_fuerte(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).translate(DASHES).translate(QUOTES)
    return norm_espacios(s).casefold()


def fragmentos(cita: str) -> list[str]:
    """Una cita con puntos suspensivos se verifica por tramos, en orden."""
    partes = [p.strip(" .") for p in re.split(r"\[\.\.\.\]|\.\.\.|…", cita)]
    return [p for p in partes if len(p) >= 12] or [cita.strip()]


def contiene_en_orden(doc: str, trozos: list[str]) -> bool:
    pos = 0
    for t in trozos:
        i = doc.find(t, pos)
        if i < 0:
            return False
        pos = i + len(t)
    return True


def similitud_maxima(cita: str, doc: str) -> float:
    """Mejor parecido entre la cita y alguna ventana del documento (para separar parafrasis de invento)."""
    cita_n, doc_n = norm_fuerte(cita), norm_fuerte(doc)
    if not cita_n or not doc_n:
        return 0.0
    oraciones = re.split(r"(?<=[.!?])\s+", doc_n)
    ventanas = oraciones + [" ".join(oraciones[i:i + 2]) for i in range(len(oraciones) - 1)]
    return max(difflib.SequenceMatcher(None, cita_n, v).ratio() for v in ventanas)


def verificar_cita(cita: str, doc_id: str, docs_por_id: dict[str, str]) -> tuple[str, float]:
    if doc_id not in docs_por_id:
        return "doc_inexistente", 0.0
    doc = docs_por_id[doc_id]
    trozos = fragmentos(cita or "")
    if not cita or not cita.strip():
        return "ausente", 0.0
    if contiene_en_orden(norm_espacios(doc), [norm_espacios(t) for t in trozos]):
        return "exacta", 1.0
    if contiene_en_orden(norm_fuerte(doc), [norm_fuerte(t) for t in trozos]):
        return "normalizada", 1.0
    sim = similitud_maxima(cita, doc)
    return ("difusa" if sim >= 0.85 else "ausente"), round(sim, 3)


PALABRAS_EFECTO = {
    "letal": ("lethal", "lethality", "mortality", "death", "dead", "die", "dies", "died", "kill", "surviv",
              "viab", "inviab", "essential", "arrest"),
    "esteril": ("steril", "fertil", "oogenesis", "oocyte", "egg", "ovar", "testis", "spermat", "germline",
                "reproduct", "oviposit", "fecund", "offspring", "hatch", "brood"),
    "morfologico": ("morpholog", "phenotyp", "defect", "malform", "wing", "eye", "cuticle", "development",
                    "abnormal", "size", "pattern"),
    "sin_efecto": ("no effect", "no phenotype", "not affect", "did not", "unaffected", "normal", "viable",
                   "without", "no obvious", "no significant", "failed to"),
}


def coherente(efecto: str, cita: str) -> bool:
    """Chequeo lexico barato: la cita contiene algun termino compatible con el efecto declarado.

    Solo ata a 'letal', 'esteril' y 'sin_efecto', que son las etiquetas que mueven el puntaje y donde un
    error es peligroso. 'morfologico' y 'otro' no tienen un vocabulario que discrimine (en la primera
    corrida rechazaba citas morfologicas validas como "cystic degeneration of the renal tubules").
    """
    palabras = PALABRAS_EFECTO.get(efecto) if efecto in ("letal", "esteril", "sin_efecto") else None
    if palabras is None:
        return True
    c = cita.casefold()
    return any(p in c for p in palabras)


def resolver_id(doc_id: str, por_id: dict[str, str]) -> str | None:
    """Un id mal formado que identifica a UN solo documento (p. ej. 'PMC123' por 'PMC123:texto')."""
    candidatos = [i for i in por_id if i.startswith(doc_id + ":")] if doc_id else []
    return candidatos[0] if len(candidatos) == 1 else None


def solo_como_driver(simbolo: str, cita: str) -> bool:
    """El simbolo aparece en la cita unicamente como promotor/driver (Act5C-GAL4), no como gen blanco."""
    apariciones = [m.end() for m in re.finditer(rf"(?<![A-Za-z0-9]){re.escape(simbolo)}(?![A-Za-z0-9])", cita)]
    if not apariciones:
        return False
    return all(re.match(r"\s*[-_ ]?(?:GAL4|Gal4|gal4|Gal80|promoter|driver|>)", cita[fin:]) for fin in apariciones)


def titulo_normalizado(doc: dict) -> str:
    return re.sub(r"[^a-z0-9]+", " ", doc.get("titulo", "").casefold()).strip()


def verificar_ficha(gen: dict, ficha: dict, docs: list[dict]) -> list[dict]:
    por_id = {d["doc_id"]: d["texto"] for d in docs}
    grupo = {d["doc_id"]: titulo_normalizado(d) or d["doc_id"] for d in docs}  # preprint y publicado = 1 fuente
    salida = []
    for a in ficha.get("afirmaciones", []):
        cita, doc_id = a.get("cita", ""), a.get("doc_id", "")
        nivel, sim = verificar_cita(cita, doc_id, por_id)
        estricta = nivel
        corregido = False
        if nivel == "doc_inexistente":
            real = resolver_id(doc_id, por_id)
            if real:
                n2, s2 = verificar_cita(cita, real, por_id)
                if n2 in ("exacta", "normalizada"):
                    nivel, sim, corregido, doc_id = n2, s2, True, real
        ok_literal = nivel in ("exacta", "normalizada")
        a = dict(a)
        driver = solo_como_driver(gen["simbolo"], cita)
        a.update({
            "doc_id": doc_id,
            "verificacion": nivel,
            "verificacion_estricta": estricta,
            "id_corregido": corregido,
            "similitud": sim,
            "coherente": coherente(a.get("efecto", "otro"), cita),
            "simbolo_en_cita": menciona(gen["simbolo"], cita) and not driver,
            "solo_driver": driver,
            "grupo_doc": grupo.get(doc_id, doc_id),
        })
        a["aceptada"] = bool(ok_literal and a["coherente"] and not driver)
        salida.append(a)
    return salida


# ---------------------------------------------------------------- 4. agregar

# Reglas fijas y a la vista. Se pueden discutir y correr analisis de sensibilidad sobre ellas.
PUNTOS_EFECTO = {"letal": 1.0, "esteril": 0.6, "morfologico": 0.2, "sin_efecto": -1.0, "otro": 0.0}
PESO_ORDEN = {"Hemiptera": 1.0, "Coleoptera": 0.6, "Diptera": 0.6, "otro_insecto": 0.5,
              "no_insecto": 0.2, "desconocido": 0.3}
PESO_ATRIBUCION = {True: 1.0, False: 0.5}  # 0,5 si la cita no nombra al gen: puede hablar de otro del mismo resumen
TOPE = 2.0


def agregar(aceptadas: list[dict]) -> dict:
    """Puntaje de esencialidad en [0, 1] con reglas deterministas. Sin LLM."""
    mejor_por_clave: dict[tuple, float] = {}
    for a in aceptadas:
        valor = (PUNTOS_EFECTO.get(a.get("efecto"), 0.0) * PESO_ORDEN.get(a.get("orden"), 0.3)
                 * PESO_ATRIBUCION[bool(a.get("simbolo_en_cita"))])
        clave = (a.get("grupo_doc", a["doc_id"]), a.get("efecto"))  # una fuente cuenta una vez por tipo de efecto
        if clave not in mejor_por_clave or abs(valor) > abs(mejor_por_clave[clave]):
            mejor_por_clave[clave] = valor
    positivos = sum(v for v in mejor_por_clave.values() if v > 0)
    negativos = -sum(v for v in mejor_por_clave.values() if v < 0)
    efectos = {a.get("efecto") for a in aceptadas}
    return {
        "score": round(max(0.0, min(TOPE, positivos - negativos)) / TOPE, 3),
        "n_docs_con_evidencia": len({a.get("grupo_doc", a["doc_id"]) for a in aceptadas}),
        "contradiccion": int("sin_efecto" in efectos and bool(efectos & {"letal", "esteril"})),
        "nivel": "ninguna" if not aceptadas else ("baja" if positivos < 1.0 else "media" if positivos < 2.0 else "alta"),
    }


# ---------------------------------------------------------------- metricas y autotest


def metricas(todas: list[dict]) -> dict:
    n = len(todas)
    cuenta = {k: sum(1 for a in todas if a["verificacion"] == k)
              for k in ("exacta", "normalizada", "difusa", "ausente", "doc_inexistente")}
    no_verif = n - cuenta["exacta"] - cuenta["normalizada"]
    estricta = sum(1 for a in todas if a.get("verificacion_estricta", a["verificacion"]) not in ("exacta", "normalizada"))
    return {
        "afirmaciones": n, **cuenta,
        "ids_corregidos": sum(1 for a in todas if a.get("id_corregido")),
        "tasa_no_verificable_estricta": round(estricta / n, 4) if n else None,  # sin corregir ids mal formados
        "tasa_no_verificable": round(no_verif / n, 4) if n else None,           # con ids corregidos (cita literal en doc unico)
        "solo_driver": sum(1 for a in todas if a.get("solo_driver")),
        "tasa_no_verificable_sin_difusas": round((cuenta["ausente"] + cuenta["doc_inexistente"]) / n, 4) if n else None,
        "incoherentes_entre_las_literales": sum(1 for a in todas
                                                if a["verificacion"] in ("exacta", "normalizada") and not a["coherente"]),
        "aceptadas": sum(1 for a in todas if a["aceptada"]),
    }


def mutar(cita: str, rnd: random.Random) -> dict[str, str]:
    """Falsificaciones plausibles de una cita real, para medir si el verificador las atrapa."""
    palabras = cita.split()
    out = {}
    if len(palabras) >= 6:
        p = palabras[:]
        i = rnd.randrange(1, len(p) - 1)
        p[i] = rnd.choice(["strongly", "never", "significantly", "mortality", "unrelated"])
        out["palabra_cambiada"] = " ".join(p)
        q = palabras[:]
        rnd.shuffle(q)
        out["palabras_barajadas"] = " ".join(q)
        out["recortada_y_extendida"] = " ".join(palabras[: len(palabras) // 2]) + " and caused complete lethality in all larvae"
    digitos = re.findall(r"\d+", cita)
    if digitos:
        out["numero_cambiado"] = cita.replace(digitos[0], str(int(digitos[0]) + 7), 1)
    return out


def autotest(fichas_dir: Path) -> dict:
    rnd = random.Random(0)
    total = atrapadas = 0
    por_tipo: dict[str, list[int]] = {}
    for ruta in sorted(fichas_dir.glob("ficha_*.json")):
        d = json.loads(ruta.read_text(encoding="utf-8"))
        por_id = {x["doc_id"]: x["texto"] for x in d["docs"]}
        otros = list(por_id)
        for a in d["verificadas"]:
            if a["verificacion"] not in ("exacta", "normalizada"):
                continue
            for tipo, cita_mala in mutar(a["cita"], rnd).items():
                nivel, _ = verificar_cita(cita_mala, a["doc_id"], por_id)
                ok = nivel not in ("exacta", "normalizada")
                por_tipo.setdefault(tipo, []).append(int(ok))
                total += 1
                atrapadas += ok
            # cita real pero atribuida a otro documento
            otros_ids = [i for i in otros if i != a["doc_id"] and a["cita"].casefold() not in por_id[i].casefold()]
            if otros_ids:
                nivel, _ = verificar_cita(a["cita"], rnd.choice(otros_ids), por_id)
                ok = nivel not in ("exacta", "normalizada")
                por_tipo.setdefault("documento_equivocado", []).append(int(ok))
                total += 1
                atrapadas += ok
    return {"mutaciones": total, "atrapadas": atrapadas,
            "deteccion": round(atrapadas / total, 4) if total else None,
            "por_tipo": {k: f"{sum(v)}/{len(v)}" for k, v in por_tipo.items()}}


# ---------------------------------------------------------------- orquestacion


def correr(args) -> None:
    EVIDENCIA.mkdir(parents=True, exist_ok=True)
    genes = elegir_genes(args.genes)
    genes += [{"locus": "control", "simbolo": s, "tribolium": "", "fenotipo_tabla": "control"} for s in CONTROLES[:args.controles]]
    genes += [{"locus": "pedido", "simbolo": s, "tribolium": "", "fenotipo_tabla": "pedido"} for s in args.simbolos]
    extractor = ExtractorClaudeCLI(args.model) if args.backend == "claude" else ExtractorManual()
    etiqueta = f"v2_{args.backend}_{args.model}" if args.backend == "claude" else "manual"
    directorio = EVIDENCIA / etiqueta
    directorio.mkdir(exist_ok=True)

    todas, resumen = [], []
    for g in genes:
        cache = EVIDENCIA / f"docs3_{g['simbolo']}.json"
        if cache.exists():
            docs = json.loads(cache.read_text(encoding="utf-8"))
        else:
            docs = recolectar(g["simbolo"])
            cache.write_text(json.dumps(docs, ensure_ascii=False, indent=1), encoding="utf-8")
        ficha = extractor.extraer(g, docs)
        verificadas = verificar_ficha(g, ficha, docs)
        aceptadas = [a for a in verificadas if a["aceptada"]]
        agg = agregar(aceptadas)
        (directorio / f"ficha_{g['simbolo']}.json").write_text(
            json.dumps({"gen": g, "docs": docs, "ficha": ficha, "verificadas": verificadas, "agregado": agg},
                       ensure_ascii=False, indent=1), encoding="utf-8")
        todas.extend(verificadas)
        resumen.append({"locus": g["locus"], "simbolo": g["simbolo"], "fenotipo_tabla": g["fenotipo_tabla"],
                        "n_docs": len(docs), "n_afirmaciones": len(verificadas), "n_aceptadas": len(aceptadas), **agg})
        print(f"{g['simbolo']:<10} docs {len(docs)}  afirmaciones {len(verificadas):>2}  aceptadas {len(aceptadas):>2}  "
              f"score {agg['score']:.2f}  nivel {agg['nivel']}", flush=True)

    with (directorio / "resumen.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(resumen[0].keys()))
        w.writeheader()
        w.writerows(resumen)
    m = metricas(todas)
    m["genes"] = len(genes)
    m["genes_con_alguna_evidencia_aceptada"] = sum(1 for r in resumen if r["n_aceptadas"] > 0)
    m["modelo"] = etiqueta
    if args.backend == "claude":
        m["costo_usd"] = round(extractor.costo, 4)
        m["respuestas_no_parseables"] = extractor.errores
    (directorio / "metricas.json").write_text(json.dumps(m, indent=1), encoding="utf-8")
    print("\n" + json.dumps(m, indent=1))


def reevaluar(origen: Path) -> None:
    """Recalcula verificacion y puntaje desde las fichas YA extraidas, sin volver a llamar al LLM.

    Sirve para cambiar una regla determinista (verificador, coherencia, agregacion) y ver el efecto exacto
    sobre las mismas extracciones. Escribe en <origen>_reeval.
    """
    destino = origen.parent / (origen.name + "_reeval")
    destino.mkdir(exist_ok=True)
    todas, resumen = [], []
    for ruta in sorted(origen.glob("ficha_*.json")):
        d = json.loads(ruta.read_text(encoding="utf-8"))
        verificadas = verificar_ficha(d["gen"], d["ficha"], d["docs"])
        aceptadas = [a for a in verificadas if a["aceptada"]]
        agg = agregar(aceptadas)
        d["verificadas"], d["agregado"] = verificadas, agg
        (destino / ruta.name).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        todas.extend(verificadas)
        g = d["gen"]
        resumen.append({"locus": g["locus"], "simbolo": g["simbolo"], "fenotipo_tabla": g["fenotipo_tabla"],
                        "n_docs": len(d["docs"]), "n_afirmaciones": len(verificadas),
                        "n_aceptadas": len(aceptadas), **agg})
    with (destino / "resumen.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(resumen[0].keys()))
        w.writeheader()
        w.writerows(resumen)
    m = metricas(todas)
    m["genes"] = len(resumen)
    m["genes_con_alguna_evidencia_aceptada"] = sum(1 for r in resumen if r["n_aceptadas"] > 0)
    m["origen"] = origen.name
    (destino / "metricas.json").write_text(json.dumps(m, indent=1), encoding="utf-8")
    print(json.dumps(m, indent=1))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--genes", type=int, default=10)
    ap.add_argument("--controles", type=int, default=len(CONTROLES))
    ap.add_argument("--simbolos", nargs="*", default=[], help="genes extra por simbolo de Drosophila (p. ej. BicC)")
    ap.add_argument("--backend", choices=("claude", "manual"), default="claude")
    ap.add_argument("--model", default="haiku")
    ap.add_argument("--autotest", metavar="DIR", nargs="?", const="", help="mutaciones sobre fichas de DIR")
    ap.add_argument("--reevaluar", metavar="DIR", help="recalcula verificacion y puntaje sobre fichas ya extraidas")
    args = ap.parse_args()
    if args.reevaluar:
        reevaluar(Path(args.reevaluar))
        return
    if args.autotest is not None:
        carpeta = Path(args.autotest) if args.autotest else EVIDENCIA / f"v2_claude_{args.model}"
        print(json.dumps(autotest(carpeta), indent=1))
        return
    correr(args)


if __name__ == "__main__":
    main()
