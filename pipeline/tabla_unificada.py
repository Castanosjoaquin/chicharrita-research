"""Tabla unificada: locus en D. maidis -> mejor hit por especie -> fenotipo de RNAi.

Junta tres mapeos de miniprot contra el mismo genoma (ihDalMaid1.1) con los
fenotipos del cribado de iBeetle en Tribolium castaneum.

IMPORTANTE SOBRE LAS PALABRAS
-----------------------------
Un hit de miniprot NO es un ortologo. En toda la salida las columnas se llaman
`mejor_hit_*` a proposito. Para llamarlo ortologo haria falta mejor hit
reciproco o sintenia, y no se corrio.

El unico lugar donde aparece la palabra ortologia es en las tablas de iBeetle
(OrthoFinder y eggNOG6), que si son predicciones de ortologia, pero entre
Tribolium y Drosophila, no con D. maidis.

ENTRADAS
--------
  pipeline/salida/tcas_vs_dmaidis.csv    Tribolium castaneum (OGS3)   -> locus
  pipeline/salida/dmel_vs_dmaidis.csv    Drosophila melanogaster      -> locus
  pipeline/salida/nlug_vs_dmaidis.csv    Nilaparvata lugens           -> locus
  <ibeetle>/dmel_fbgn.tsv                UniProt entry name -> FBgn
  <ibeetle>/OrthoFinder_orthology.tsv    Tcas <-> Dmel
  <ibeetle>/Eggnog6_orthology.tsv        Tcas <-> Dmel
  <ibeetle>/iB_TC.csv                    fragmento de dsRNA -> gen TC
  <ibeetle>/iBeetle_lethality.csv        letalidad por fragmento
  <ibeetle>/iBeetle_grouped_phenotypes.ndjson   anotaciones por gen TC

Uso:
    python3 tabla_unificada.py <dir_ibeetle> <dir_salida>
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Distancia filogenetica de cada especie de referencia a Dalbulus maidis.
# D. maidis es Hemiptera / Cicadellidae. [inferencia] a partir de taxonomia NCBI.
# Se guarda en la tabla porque el mapeo mejora con la cercania (medido: Drosophila
# recupera 72,1 % de sus proteinas con identidad mediana 0,545; Nilaparvata, que es
# del mismo orden, 77,6 % con 0,634) y porque la transferencia del FENOTIPO entre
# ordenes es justamente el supuesto sin verificar de todo el proyecto.
# ---------------------------------------------------------------------------
ESPECIES = {
    "nlug": {
        "nombre": "Nilaparvata lugens",
        "orden": "Hemiptera",
        "rango_comun": "mismo orden",
        "distancia": 1,
        "tiene_fenotipos": False,
    },
    "tcas": {
        "nombre": "Tribolium castaneum",
        "orden": "Coleoptera",
        "rango_comun": "misma clase, otro orden",
        "distancia": 2,
        "tiene_fenotipos": True,
    },
    "dmel": {
        "nombre": "Drosophila melanogaster",
        "orden": "Diptera",
        "rango_comun": "misma clase, otro orden",
        "distancia": 2,
        "tiene_fenotipos": False,
    },
}

# ---------------------------------------------------------------------------
# Clasificacion de las descripciones de fenotipo de iBeetle.
#
# Reglas ordenadas: gana la primera que matchea. Estan escritas para poder
# auditarse, no para ser elegantes. El script reporta cuantas anotaciones caen
# en "otro" para que se vea cuanto no cubren.
#
# [inferencia] - clasificacion armada leyendo las descripciones, por un equipo
# sin formacion biologica. Va a revision con un profesional.
#
# La categoria "normal" existe porque NO toda anotacion de iBeetle es un defecto:
# "larva number hatched many (ca. 70-100 %)" aparece 8.179 veces y es un resultado
# sano. Contarla como fenotipo infla todo.
# ---------------------------------------------------------------------------
REGLAS = [
    ("normal", [
        "without detectable defects",
        "no detectable defects",
        "hatched many (ca. 70-100",
        "number hatched many",
        "not affected",
        "unaffected",
    ]),
    ("letal", [
        "lethality",
        "lethal",
        "died as",
        "not fulfilled",
        "not hatched",
        "dead",
    ]),
    ("esteril", [
        "egg production",
        "egg-lay",
        "egg lay",
        "ovary",
        "ovariole",
        "vitellarium",
        "tropharium",
        "mature egg",
        "fertility",
        "number hatched none",
        "number few",
        "sterile",
        "germarium",
    ]),
    ("letal_embrionario", [
        "affected eggs/embryos/larvae",
        "embryo/egg",
        "without visible larval cuticle",
        "not developed/not fertilized",
        "cuticle remnants",
        "no cuticle",
    ]),
    ("morfologico", [
        "muscul", "cuticle", "segment", "wing", "elytra", "leg", "antenna",
        "head", "thorax", "abdomen", "gland", "urogomphi", "eye", "shape",
        "size", "pattern", "number decreased", "number increased",
        "transformed", "blistered", "fused", "irregular", "delayed",
        "molt", "pigmentation", "colour", "color", "bristle", "appendage",
    ]),
]

# Porcentaje de letalidad del cribado a partir del cual se cuenta como fenotipo letal
# aunque no haya ninguna anotacion en el ndjson. [inferencia] 50 % es la mitad de los
# animales inyectados; los autores no publican un umbral, asi que queda a revision.
UMBRAL_LETALIDAD = 50.0

# Las categorias que cuentan como "este gen hizo algo malo al silenciarlo".
DEFECTOS = ("letal", "letal_embrionario", "esteril", "morfologico", "otro")


def clasificar(descripcion: str) -> str:
    texto = descripcion.lower()
    for etiqueta, claves in REGLAS:
        for clave in claves:
            if clave in texto:
                return etiqueta
    return "otro"


# ---------------------------------------------------------------------------
# Lectura de los mapeos de miniprot
# ---------------------------------------------------------------------------

def leer_mapeo(ruta: Path, clave_especie: str) -> dict[str, dict]:
    """Mejor hit por proteina (mayor score), con cuantos hits tuvo en total."""
    por_prot: dict[str, list[dict]] = defaultdict(list)
    with ruta.open(encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            fila["score"] = int(fila["score"])
            fila["inicio"] = int(fila["inicio"])
            fila["fin"] = int(fila["fin"])
            fila["identidad"] = float(fila["identidad"])
            fila["positivos"] = float(fila["positivos"])
            fila["frameshift"] = int(fila["frameshift"])
            fila["stop_interno"] = int(fila["stop_interno"])
            fila["exones"] = int(fila["exones"])
            por_prot[fila["proteina"]].append(fila)

    mejores = {}
    for prot, hits in por_prot.items():
        mejor = max(hits, key=lambda h: h["score"])
        mejor = dict(mejor)
        mejor["n_hits"] = len(hits)
        mejor["especie"] = clave_especie
        mejores[prot] = mejor
    return mejores


# ---------------------------------------------------------------------------
# Agrupamiento de loci: dos hits son el mismo locus si se solapan lo suficiente
# ---------------------------------------------------------------------------

SOLAPE_MINIMO = 0.5  # fraccion del intervalo mas corto


def agrupar_loci(hits: list[dict]) -> list[list[dict]]:
    """Agrupa hits que se solapan en el mismo cromosoma y hebra.

    Enlace simple sobre intervalos ordenados: un hit entra al grupo abierto si
    solapa al menos SOLAPE_MINIMO del mas corto de los dos. El riesgo conocido
    del enlace simple es encadenar genes en tandem; por eso la salida reporta
    cuantos hits distintos se fusionaron en cada locus, para que se vea.
    """
    por_contexto: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for h in hits:
        por_contexto[(h["cromosoma"], h["hebra"])].append(h)

    grupos: list[list[dict]] = []
    for clave in sorted(por_contexto):
        lista = sorted(por_contexto[clave], key=lambda h: (h["inicio"], h["fin"]))
        actual: list[dict] = []
        fin_actual = -1
        for h in lista:
            if not actual:
                actual = [h]
                fin_actual = h["fin"]
                continue
            solape = min(fin_actual, h["fin"]) - h["inicio"] + 1
            corto = min(fin_actual - actual[0]["inicio"] + 1, h["fin"] - h["inicio"] + 1)
            if solape > 0 and corto > 0 and solape / corto >= SOLAPE_MINIMO:
                actual.append(h)
                fin_actual = max(fin_actual, h["fin"])
            else:
                grupos.append(actual)
                actual = [h]
                fin_actual = h["fin"]
        if actual:
            grupos.append(actual)
    return grupos


# ---------------------------------------------------------------------------
# Fenotipos de iBeetle, agregados por gen TC
# ---------------------------------------------------------------------------

def cargar_fenotipos(base: Path) -> tuple[dict[str, dict], Counter]:
    resumen: dict[str, dict] = {}
    categorias_totales: Counter[str] = Counter()

    with (base / "iBeetle_grouped_phenotypes.ndjson").open(encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            obj = json.loads(linea)
            gen = obj.get("gene", "")
            if not gen:
                continue
            cuentas: Counter[str] = Counter()
            pen_max: dict[str, float] = {}
            estructuras: set[str] = set()
            for fen in obj.get("phenotypes", []):
                cat = clasificar(fen.get("description", ""))
                cuentas[cat] += 1
                categorias_totales[cat] += 1
                pen = fen.get("penetrance")
                if isinstance(pen, (int, float)):
                    pen_max[cat] = max(pen_max.get(cat, 0.0), float(pen))
                for est in fen.get("structures", []) or []:
                    nombre = est.get("termName")
                    if nombre:
                        estructuras.add(nombre)
            n_defectos = sum(cuentas[c] for c in DEFECTOS)
            resumen[gen] = {
                "n_anotaciones": sum(cuentas.values()),
                "n_defectos": n_defectos,
                "cuentas": cuentas,
                "penetrancia_max": pen_max,
                "estructuras": sorted(estructuras),
            }
    return resumen, categorias_totales


def cargar_letalidad(base: Path) -> dict[str, float]:
    """Maxima letalidad reportada por gen TC, en porcentaje. -1 y vacio = no medido."""
    ib_a_tc: dict[str, str] = {}
    with (base / "iB_TC.csv").open(encoding="utf-8-sig") as f:
        for fila in csv.reader(f):
            if not fila or fila[0].startswith("#"):
                continue
            if len(fila) >= 2:
                ib_a_tc[fila[0].strip()] = fila[1].strip()

    por_gen: dict[str, float] = {}
    with (base / "iBeetle_lethality.csv").open(encoding="utf-8-sig") as f:
        for fila in csv.DictReader(f, delimiter=";"):
            gen = ib_a_tc.get(fila["iB"].strip())
            if not gen:
                continue
            for col in ("dali11", "dali22", "dapi11"):
                v = (fila.get(col) or "").strip()
                if not v:
                    continue
                try:
                    num = float(v)
                except ValueError:
                    continue
                if num < 0:
                    continue
                por_gen[gen] = max(por_gen.get(gen, 0.0), num)
    return por_gen


def cargar_ortologia(base: Path) -> dict[str, set[str]]:
    """FBgn de Drosophila -> genes TC de Tribolium, uniendo OrthoFinder y eggNOG6."""
    fbgn_a_tc: dict[str, set[str]] = defaultdict(set)
    for nombre in ("OrthoFinder_orthology.tsv", "Eggnog6_orthology.tsv"):
        ruta = base / nombre
        if not ruta.exists():
            continue
        with ruta.open(encoding="utf-8") as f:
            for fila in csv.DictReader(f, delimiter="\t"):
                tcas = [x.strip() for x in (fila.get("Tcas") or "").split(",") if x.strip()]
                dmel = [x.strip() for x in (fila.get("Dmel") or "").split(",") if x.strip()]
                for fb in dmel:
                    fbgn_a_tc[fb].update(tcas)
    return fbgn_a_tc


def cargar_crosswalk_dmel(base: Path) -> dict[str, tuple[str, str]]:
    """Nombre de entrada de UniProt -> (FBgn, nombre de gen)."""
    salida: dict[str, tuple[str, str]] = {}
    ruta = base / "dmel_fbgn.tsv"
    if not ruta.exists():
        return salida
    with ruta.open(encoding="utf-8") as f:
        for fila in csv.DictReader(f, delimiter="\t"):
            entrada = (fila.get("Entry Name") or "").strip()
            fb = (fila.get("FlyBase") or "").strip().rstrip(";")
            gen = (fila.get("Gene Names (primary)") or "").strip()
            if entrada:
                salida[entrada] = (fb.split(";")[0] if fb else "", gen)
    return salida


# ---------------------------------------------------------------------------

def categoria_dominante(cuentas: Counter) -> str:
    """Una etiqueta por gen, con prioridad biologica, no por frecuencia.

    [inferencia] El orden es letal > letal_embrionario > esteril > morfologico
    porque para un insecticida por RNAi matar o esterilizar vale mas que deformar.
    """
    for cat in ("letal", "letal_embrionario", "esteril", "morfologico", "otro"):
        if cuentas.get(cat, 0) > 0:
            return cat
    return "sin_fenotipo"


def main() -> int:
    base = Path(sys.argv[1])
    salida_dir = Path(sys.argv[2])
    salida_dir.mkdir(parents=True, exist_ok=True)

    mapeos = {
        "tcas": leer_mapeo(salida_dir / "tcas_vs_dmaidis.csv", "tcas"),
        "dmel": leer_mapeo(salida_dir / "dmel_vs_dmaidis.csv", "dmel"),
        "nlug": leer_mapeo(salida_dir / "nlug_vs_dmaidis.csv", "nlug"),
    }
    for clave, m in mapeos.items():
        print(f"{clave}: {len(m)} proteinas con locus")

    fenotipos, cat_totales = cargar_fenotipos(base)
    letalidad = cargar_letalidad(base)
    fbgn_a_tc = cargar_ortologia(base)
    crosswalk = cargar_crosswalk_dmel(base)
    genes_cribados = set()
    with (base / "iB_TC.csv").open(encoding="utf-8-sig") as f:
        for fila in csv.reader(f):
            if fila and not fila[0].startswith("#") and len(fila) >= 2:
                genes_cribados.add(fila[1].strip())

    print(f"genes TC con anotaciones de fenotipo: {len(fenotipos)}")
    print(f"genes TC con letalidad medida       : {len(letalidad)}")
    print(f"genes TC cribados (tuvieron dsRNA)  : {len(genes_cribados)}")
    print(f"FBgn con al menos un TC asociado    : {len(fbgn_a_tc)}")
    print(f"crosswalk UniProt->FBgn             : {len(crosswalk)}")
    print()
    print("anotaciones de fenotipo por categoria (todas las de iBeetle):")
    total_anot = sum(cat_totales.values())
    for cat, n in cat_totales.most_common():
        print(f"  {cat:<20}{n:>8}  ({n/total_anot*100:.1f} %)")
    print()

    todos_hits = [h for m in mapeos.values() for h in m.values()]
    grupos = agrupar_loci(todos_hits)
    print(f"hits totales: {len(todos_hits)}  ->  loci agrupados: {len(grupos)}")

    filas = []
    for i, grupo in enumerate(sorted(grupos, key=lambda g: (g[0]["cromosoma"], g[0]["inicio"])), 1):
        por_especie: dict[str, dict] = {}
        for h in grupo:
            prev = por_especie.get(h["especie"])
            if prev is None or h["score"] > prev["score"]:
                por_especie[h["especie"]] = h

        tc_directo = por_especie["tcas"]["proteina"] if "tcas" in por_especie else ""
        fb, gen_dmel = ("", "")
        if "dmel" in por_especie:
            fb, gen_dmel = crosswalk.get(por_especie["dmel"]["proteina"], ("", ""))
        tc_via_dmel = sorted(fbgn_a_tc.get(fb, set())) if fb else []

        # Que gen TC usamos para buscar fenotipo, y por que camino llegamos.
        if tc_directo and tc_directo in fenotipos:
            tc_fenotipo, ruta = tc_directo, "hit_directo_tribolium"
        elif tc_directo:
            tc_fenotipo, ruta = tc_directo, "hit_directo_tribolium"
        elif tc_via_dmel:
            con_fen = [t for t in tc_via_dmel if t in fenotipos]
            tc_fenotipo = con_fen[0] if con_fen else tc_via_dmel[0]
            ruta = "ortologia_drosophila_tribolium"
        else:
            tc_fenotipo, ruta = "", "sin_ruta"

        # Los dos caminos coinciden? Es la mejor evidencia disponible sin reciproco.
        if tc_directo and tc_via_dmel:
            concordancia = "coinciden" if tc_directo in tc_via_dmel else "discrepan"
        elif tc_directo or tc_via_dmel:
            concordancia = "una_sola_via"
        else:
            concordancia = "ninguna"

        # La tabla de letalidad es una fuente INDEPENDIENTE del ndjson, no un
        # resumen de el. Verificado: TC010367 (el que cae donde Vha26 de
        # Drosophila) es 100 % letal en los tres tiempos y no tiene ni una
        # anotacion en el ndjson. [inferencia] Si el animal muere temprano no
        # queda nada que puntuar morfologicamente. Mirar solo el ndjson pierde
        # justamente los genes que mas matan, que son los que nos interesan.
        let_tabla = letalidad.get(tc_fenotipo)
        fen = fenotipos.get(tc_fenotipo)
        if fen is None:
            cuentas: Counter[str] = Counter()
            estructuras: list[str] = []
            pen = {}
            if let_tabla is not None and let_tabla >= UMBRAL_LETALIDAD:
                cat = "letal"
                fuente_fen = "solo_tabla_letalidad"
            elif tc_fenotipo in genes_cribados:
                cat = "sin_fenotipo"
                fuente_fen = "cribado_sin_defecto"
            else:
                cat = "sin_dato"
                fuente_fen = "ninguna"
        else:
            cuentas = fen["cuentas"]
            cat = categoria_dominante(cuentas)
            estructuras = fen["estructuras"]
            pen = fen["penetrancia_max"]
            if cat == "sin_fenotipo" and let_tabla is not None and let_tabla >= UMBRAL_LETALIDAD:
                cat = "letal"
                fuente_fen = "solo_tabla_letalidad"
            elif let_tabla is not None:
                fuente_fen = "ndjson_y_tabla"
            else:
                fuente_fen = "solo_ndjson"

        # ---------------------------------------------------------------
        # Nivel de evidencia [inferencia]. No es un score biologico, es
        # cuanta confianza merece la fila como candidata a mirar primero.
        # Combina tres cosas independientes:
        #   1. que las dos vias a Tribolium (hit directo y ortologia via
        #      Drosophila) caigan en el mismo gen;
        #   2. que el alineamiento al genoma sea bueno;
        #   3. que el fenotipo sea fuerte segun el propio cribado (letalidad
        #      alta o penetrancia alta), porque los autores de iBeetle avisan
        #      que por debajo del 50 % de penetrancia la reproducibilidad cae.
        # ---------------------------------------------------------------
        let_pct = letalidad.get(tc_fenotipo)
        pen_letal = pen.get("letal") or pen.get("letal_embrionario") or 0.0
        fenotipo_fuerte = (let_pct is not None and let_pct >= 80.0) or pen_letal >= 0.8
        ident_tcas = por_especie["tcas"]["identidad"] if "tcas" in por_especie else 0.0
        tiene_defecto = cat in DEFECTOS

        if not tiene_defecto:
            nivel = "evidencia_negativa" if cat == "sin_fenotipo" else "sin_dato"
        elif concordancia == "coinciden" and fenotipo_fuerte and ident_tcas >= 0.6:
            nivel = "alto"
        elif concordancia == "coinciden" or (fenotipo_fuerte and ident_tcas >= 0.6):
            nivel = "medio"
        else:
            nivel = "bajo"

        mejor_global = max(grupo, key=lambda h: h["score"])
        fila = {
            "locus": f"L{i:05d}",
            "cromosoma": mejor_global["cromosoma"],
            "inicio": min(h["inicio"] for h in grupo),
            "fin": max(h["fin"] for h in grupo),
            "hebra": mejor_global["hebra"],
            "n_hits_fusionados": len(grupo),
            "especies_que_caen_aca": "|".join(sorted(por_especie)),
            # --- fenotipo
            "fenotipo_categoria": cat,
            "nivel_evidencia": nivel,
            "fenotipo_fuente": fuente_fen,
            "fenotipo_ruta": ruta,
            "fenotipo_especie_origen": "Tribolium castaneum" if cat not in ("sin_dato",) and tc_fenotipo else "",
            "fenotipo_distancia": ESPECIES["tcas"]["distancia"] if tc_fenotipo else "",
            "fenotipo_rango_comun": ESPECIES["tcas"]["rango_comun"] if tc_fenotipo else "",
            "n_letal": cuentas.get("letal", 0),
            "n_letal_embrionario": cuentas.get("letal_embrionario", 0),
            "n_esteril": cuentas.get("esteril", 0),
            "n_morfologico": cuentas.get("morfologico", 0),
            "n_normal": cuentas.get("normal", 0),
            "n_otro": cuentas.get("otro", 0),
            "penetrancia_max_letal": pen.get("letal", ""),
            "letalidad_pct_max": letalidad.get(tc_fenotipo, ""),
            "estructuras_afectadas": "|".join(estructuras[:8]),
            # --- de donde sale el locus
            "mejor_hit_tribolium": tc_directo,
            "tribolium_via_ortologia_dmel": "|".join(tc_via_dmel[:5]),
            "concordancia_tribolium": concordancia,
            "mejor_hit_drosophila": por_especie["dmel"]["proteina"] if "dmel" in por_especie else "",
            "gen_drosophila": gen_dmel,
            "fbgn": fb,
            "mejor_hit_nilaparvata": por_especie["nlug"]["proteina"] if "nlug" in por_especie else "",
        }
        for clave in ("tcas", "dmel", "nlug"):
            h = por_especie.get(clave)
            fila[f"{clave}_identidad"] = h["identidad"] if h else ""
            fila[f"{clave}_positivos"] = h["positivos"] if h else ""
            fila[f"{clave}_exones"] = h["exones"] if h else ""
            fila[f"{clave}_frameshift"] = h["frameshift"] if h else ""
            fila[f"{clave}_stop_interno"] = h["stop_interno"] if h else ""
            fila[f"{clave}_n_hits_de_esa_proteina"] = h["n_hits"] if h else ""
        filas.append(fila)

    altos = [f for f in filas if f["nivel_evidencia"] == "alto"]
    altos.sort(key=lambda f: (-(float(f["letalidad_pct_max"]) if f["letalidad_pct_max"] != "" else 0),
                              -(float(f["tcas_identidad"]) if f["tcas_identidad"] != "" else 0)))
    corto = salida_dir / "candidatos_alto.csv"
    columnas_corto = ["locus", "cromosoma", "inicio", "fin", "hebra", "fenotipo_categoria",
                      "letalidad_pct_max", "penetrancia_max_letal", "fenotipo_fuente",
                      "mejor_hit_tribolium", "gen_drosophila", "mejor_hit_nilaparvata",
                      "tcas_identidad", "dmel_identidad", "nlug_identidad",
                      "tcas_exones", "tcas_frameshift", "tcas_stop_interno",
                      "tcas_n_hits_de_esa_proteina", "estructuras_afectadas"]

    destino = salida_dir / "tabla_unificada.csv"
    with destino.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"escrito: {destino}  ({len(filas)} loci)")
    with corto.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=columnas_corto, extrasaction="ignore")
        escritor.writeheader()
        escritor.writerows(altos)
    print(f"escrito: {corto}  ({len(altos)} loci de nivel alto)")

    # -------------------------------------------------------------------
    # Reporte
    # -------------------------------------------------------------------
    print()
    print("=== loci por categoria dominante (excluyente, prioridad letal > esteril > morfologico) ===")
    cats = Counter(f["fenotipo_categoria"] for f in filas)
    for cat, n in cats.most_common():
        print(f"  {cat:<22}{n:>7}  ({n/len(filas)*100:.1f} %)")

    con_fenotipo = sum(n for c, n in cats.items() if c in DEFECTOS)
    print()
    print(f"loci con ALGUN fenotipo de defecto : {con_fenotipo} ({con_fenotipo/len(filas)*100:.1f} %)")
    print(f"loci con evidencia negativa        : {cats.get('sin_fenotipo', 0)} (cribados, sin defecto)")
    print(f"loci sin dato de cribado           : {cats.get('sin_dato', 0)}")

    print()
    print("=== loci por tipo de fenotipo (NO excluyente: un locus puede estar en varias) ===")
    print("    la de arriba subestima todo lo que no sea letal, porque la prioridad lo tapa")
    for etiqueta, col in (("letal", "n_letal"), ("letal_embrionario", "n_letal_embrionario"),
                          ("esteril", "n_esteril"), ("morfologico", "n_morfologico"),
                          ("otro", "n_otro"), ("anotacion normal", "n_normal")):
        n = sum(1 for f in filas if f[col] > 0)
        print(f"  {etiqueta:<22}{n:>7}  ({n/len(filas)*100:.1f} %)")

    print()
    print("=== nivel de evidencia ===")
    print("    alto  = las dos vias coinciden + fenotipo fuerte (letalidad >=80 % o")
    print("            penetrancia >=0,8) + identidad del alineamiento >=0,60")
    for nivel, n in Counter(f["nivel_evidencia"] for f in filas).most_common():
        print(f"  {nivel:<22}{n:>7}  ({n/len(filas)*100:.1f} %)")

    print()
    print("=== de que archivo salio el fenotipo ===")
    for fu, n in Counter(f["fenotipo_fuente"] for f in filas).most_common():
        print(f"  {fu:<24}{n:>7}")

    print()
    print("=== como se llego al fenotipo ===")
    for ruta, n in Counter(f["fenotipo_ruta"] for f in filas).most_common():
        print(f"  {ruta:<34}{n:>7}")

    print()
    print("=== concordancia entre las dos vias a Tribolium ===")
    for c, n in Counter(f["concordancia_tribolium"] for f in filas).most_common():
        print(f"  {c:<22}{n:>7}")

    print()
    print("=== cuantas especies caen en cada locus ===")
    for combo, n in Counter(f["especies_que_caen_aca"] for f in filas).most_common():
        print(f"  {combo:<22}{n:>7}")

    print()
    print("=== loci letales de nivel alto ===")
    letales = [f for f in filas if f["fenotipo_categoria"] == "letal"
               and f["nivel_evidencia"] == "alto"]
    letales.sort(key=lambda f: -float(f["tcas_identidad"]))
    print(f"({len(letales)} loci)")
    print(f"{'locus':<9}{'ubicacion':<30}{'TC':<11}{'gen Dmel':<12}{'ident':>7}{'let%':>7}  estructuras")
    for f in letales[:25]:
        ubic = f"{f['cromosoma']}:{f['inicio']}-{f['fin']}"
        print(f"{f['locus']:<9}{ubic:<30}{f['mejor_hit_tribolium']:<11}"
              f"{(f['gen_drosophila'] or '-'):<12}{float(f['tcas_identidad']):>7.3f}"
              f"{(f['letalidad_pct_max'] or '-'):>7}  {f['estructuras_afectadas'][:40]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
