"""Motor de ranking: carga candidatos, re-pondera y explica cada posicion.

El scoring NO se reescribe aca. Los pesos, el rango ideal de GC, la deseabilidad de GC,
la normalizacion min-max y las dos formas de agregar (suma ponderada y media geometrica)
se importan de `pipeline/sirna_enumerar.py`, que es donde viven. Este modulo agrega tres
cosas que el pipeline no da:

  1. **Descomposicion.** Cuanto aporto cada criterio al score de un candidato, para poder
     dibujar la cascada. Dos lecturas: el aporte absoluto (suma al score) y el aporte
     contra la mediana del conjunto (suma a la diferencia con el candidato tipico). La
     segunda es la que contesta "por que este quedo ACA y no mas abajo".
  2. **Re-ponderacion en vivo.** Mismo conjunto, pesos distintos, ranking nuevo, y cuanto
     se movio cada candidato.
  3. **Carga de un CSV ajeno.** Mapeo de columnas, para que entre una tabla con otro
     formato sin tocar el codigo.

Sobre ViennaRNA: `sirna_enumerar` lo importa arriba porque lo necesita para CALCULAR las
features (asimetria, dg_duplex, accesibilidad). Aca las features ya vienen calculadas en el
CSV y lo unico que se hace es aritmetica sobre ellas, asi que si ViennaRNA no esta instalado
se mete un sustituto que falla ruidosamente si alguien lo llama. De ese modo no se puede
calcular una feature a ciegas: o esta el ViennaRNA de verdad, o no se calcula nada.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import statistics
import sys
import types
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

if "RNA" not in sys.modules:
    try:
        import RNA  # noqa: F401
    except ModuleNotFoundError:
        _falso = types.ModuleType("RNA")

        def _no_disponible(*_a, **_k):
            raise RuntimeError(
                "ViennaRNA no esta instalado: este motor solo re-pondera features ya "
                "calculadas por el pipeline. Para calcular features nuevas hay que correr "
                "pipeline/sirna_enumerar.py en el entorno que tiene ViennaRNA."
            )

        _falso.duplexfold = _no_disponible
        _falso.pfl_fold_up = _no_disponible
        sys.modules["RNA"] = _falso

sys.path.insert(0, str(RAIZ / "pipeline"))

from sirna_enumerar import (GC_IDEAL, PESOS, VENTANA, deseabilidad_gc,  # noqa: E402
                            normalizar)
from sirna_offtarget import K, K_ALERTA, clave_de  # noqa: E402

try:
    from objetivo_candidatos import (CONFIANZA_MINIMA, OBJETIVOS,  # noqa: E402
                                     calidad_alineamiento)
    from objetivo_candidatos import puntuar as puntuar_objetivo
except ImportError:  # el pipeline todavia no tiene el modulo de objetivos
    OBJETIVOS, CONFIANZA_MINIMA = {}, 0.0
    puntuar_objetivo = calidad_alineamiento = None

SALIDA_PIPELINE = RAIZ / "pipeline" / "salida"
DATOS_PIPELINE = Path(__file__).resolve().parent / "datos"

# Un criterio del score. `columna` es de donde sale el valor crudo; `escala` dice como se
# lleva a 0-1 antes de multiplicar por el peso:
#   minmax    normalizacion min-max sobre el conjunto cargado (lo que hace el pipeline)
#   desea_gc  curva de deseabilidad con el rango ideal de GC
#   binario   el valor ya es 0 o 1
# `sentido` es solo para el texto de la UI. `evidencia` es el nivel de respaldo que tiene
# el criterio y se muestra en la cascada, para que nadie confunda una convencion de
# diseno con un resultado medido.
CRITERIOS = [
    {"clave": "asimetria", "columna": "asimetria", "escala": "minmax",
     "etiqueta": "Asimetria del duplex", "unidad": "kcal/mol", "sentido": "mas es mejor",
     "evidencia": "paper",
     "nota": "dG del extremo 5-prima de la guia menos el del pasajero. Positivo = la "
             "guia se carga mejor en el complejo. Es la regla de diseno con mas respaldo "
             "publicado y la que mejor transfiere entre especies."},
    {"clave": "gc_9_14", "columna": "gc_9_14", "escala": "minmax",
     "etiqueta": "GC en posiciones 9-14", "unidad": "fraccion", "sentido": "mas es mejor",
     "evidencia": "sin-verificar",
     "nota": "GC alto en la region central de la guia. En insectos apuntaria al revez "
             "que en los datos humanos. Falta confirmarlo contra dsRIP."},
    {"clave": "accesibilidad", "columna": "accesibilidad", "escala": "minmax",
     "etiqueta": "Accesibilidad del sitio", "unidad": "probabilidad",
     "sentido": "mas es mejor", "evidencia": "sin-verificar",
     "nota": "Probabilidad de que el sitio blanco este desapareado, con RNAplfold. El "
             "cribado dsRIP en insectos no la encontro significativa."},
    {"clave": "gc", "columna": "gc", "escala": "desea_gc",
     "etiqueta": "GC global en rango", "unidad": "fraccion", "sentido": "rango ideal",
     "evidencia": "convencion",
     "nota": f"Vale 1 entre {GC_IDEAL[0]:.0%} y {GC_IDEAL[1]:.0%} de GC y cae "
             f"linealmente afuera. Es una convencion de diseno, no una medicion."},
    {"clave": "a_en_10", "columna": "a_en_10", "escala": "binario",
     "etiqueta": "A en posicion 10 de la guia", "unidad": "0 o 1", "sentido": "1 es mejor",
     "evidencia": "sin-verificar",
     "nota": "Nucleotido en el sitio de corte. Misma fuente sin verificar que GC 9-14."},
]
POR_CLAVE = {c["clave"]: c for c in CRITERIOS}

# Columnas que se arrastran como contexto del gen, sin entrar al score.
CONTEXTO = ["locus", "gen_drosophila", "tribolium", "letalidad", "identidad",
            "dg_duplex", "corrida_max", "descarte", "off_target_max", "riesgo",
            # Desglose por especie que trae el propio pipeline, en formato
            # "especie:nt;especie:nt". Con esto la app puede mostrar el riesgo por especie
            # sin depender de que se haya corrido app/preparar_riesgo.py.
            "off_target_detalle", "off_target_n_especies", "off_target_peor_especie"]

UMBRALES_DEFECTO = {
    # Filtro duro del pipeline: corridas de mas de 4 nucleotidos iguales se descartan.
    "corrida_max": 4,
    # Umbral de off-target. La evidencia pone el riesgo confirmado en 21 nt contiguos y
    # reporta actividad desde 15. Arranca en 21 para no descartar nada de entrada: quien
    # lo baje esta tomando una decision, y el informe la registra.
    "off_target": K,
}


def _num(v, defecto=0.0) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return defecto


def hash_datos(texto: str) -> str:
    """SHA-256 de los bytes exactos del CSV de entrada. Va en el informe."""
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def columnas_de(texto: str) -> list[str]:
    """Encabezado del CSV, para poder ofrecer el mapeo de columnas en la UI."""
    return next(csv.reader(io.StringIO(texto)), [])


def leer_csv(texto: str, mapeo: dict | None = None) -> list[dict]:
    """Lee un CSV de candidatos. `mapeo` traduce clave_nuestra -> columna_del_archivo.

    Las columnas que no esten quedan en None, no en 0: un criterio ausente se tiene que
    poder distinguir de un criterio que vale cero.
    """
    filas = list(csv.DictReader(io.StringIO(texto)))
    if not filas:
        return []
    traducir = {v: k for k, v in (mapeo or {}).items() if v}
    salida = []
    for i, f in enumerate(filas):
        g = {traducir.get(k, k): v for k, v in f.items()}
        fila = {"id": i, "pos": int(_num(g.get("pos"), i + 1)),
                "sitio": (g.get("sitio") or "").upper(),
                "guia": (g.get("guia") or "").upper()}
        for c in CRITERIOS:
            crudo = g.get(c["columna"])
            fila[c["clave"]] = None if crudo in (None, "") else _num(crudo)
        for k in CONTEXTO:
            fila[k] = g.get(k) or ""
        fila["corrida_max"] = int(_num(fila.get("corrida_max"), 0))
        # La clave la define el pipeline (`sirna_offtarget.clave_de`): locus + posicion,
        # porque la posicion sola es relativa al CDS de cada gen y se pisa entre genes.
        fila["clave_unica"] = clave_de(fila)
        salida.append(fila)
    return salida


def criterios_presentes(filas: list[dict]) -> list[str]:
    """Criterios que tienen valor en al menos un candidato."""
    return [c["clave"] for c in CRITERIOS
            if any(f.get(c["clave"]) is not None for f in filas)]


def detalle_del_csv(fila: dict) -> list[dict]:
    """Desglose por especie que trae el CSV del pipeline: "especie:nt;especie:nt".

    No dice el transcripto donde cayo (para eso hace falta app/preparar_riesgo.py), pero si
    contra que especies pego y cuanto, que es lo que permite mostrar algo util sin volver a
    escanear los transcriptomas.
    """
    crudo = (fila.get("off_target_detalle") or "").strip()
    if not crudo:
        return []
    items = []
    for trozo in crudo.split(";"):
        if ":" not in trozo:
            continue
        nombre, _, valor = trozo.rpartition(":")
        items.append({"organismo": nombre.strip(), "especie": nombre.strip(),
                      "grupo": "", "ensamblado": "", "tramo_max": int(_num(valor, 0)),
                      "transcripto": "", "sitio": (fila.get("sitio") or "").upper(),
                      "fuente": "csv"})
    items.sort(key=lambda d: -d["tramo_max"])
    return items


SIN_DATO = ("sin medir", "desactualizado", "agregado")


def _peor_off_target(fila: dict, riesgo: dict | None) -> dict:
    """El peor tramo identico del candidato, y contra quien.

    Se prueban tres fuentes, de la mas informativa a la menos, y **ninguna ausencia de dato
    se traduce en "limpio"**: si no se midio, se dice que no se midio.

      1. La tabla de `app/preparar_riesgo.py`: tramo por especie y el transcripto exacto.
      2. El desglose `off_target_detalle` del CSV del pipeline: tramo por especie, sin
         transcripto.
      3. La columna agregada `off_target_max`: el maximo sobre todos los no objetivo
         juntos, sin decir contra quien.
    """
    vacio = {"tramo_max": 0, "organismo": "", "especie": "", "transcripto": "",
             "ensamblado": ""}
    limpio = dict(vacio, organismo="ninguno", especie="")

    # 1. Tabla propia.
    if riesgo and fila["clave_unica"] in riesgo:
        items = riesgo[fila["clave_unica"]]
        # Segunda capa de defensa: la clave ya incluye la secuencia, asi que un desajuste
        # entre corridas no deberia ni matchear. Si igual llega un dato de otra secuencia
        # (tabla vieja, de antes de que la clave la incluyera), no se usa.
        if items and fila["sitio"] and items[0]["sitio"] \
                and items[0]["sitio"] != fila["sitio"]:
            return dict(vacio, organismo="desactualizado", especie="desactualizado")
        if not items:
            # Medida contra todo el catalogo, sin ninguna coincidencia.
            return limpio
        peor = max(items, key=lambda d: d["tramo_max"])
        return peor if peor["tramo_max"] else limpio

    # 2. Desglose por especie del CSV.
    del_csv = detalle_del_csv(fila)
    if del_csv:
        return max(del_csv, key=lambda d: d["tramo_max"])

    # 3. Columna agregada del CSV. Que la columna de desglose exista y venga vacia es un
    # dato: quiere decir medido y sin coincidencias, no sin medir.
    if fila.get("off_target_max") not in (None, ""):
        maximo = int(_num(fila.get("off_target_max"), 0))
        if maximo == 0:
            return limpio
        quien = fila.get("off_target_peor_especie") or ""
        return dict(vacio, tramo_max=maximo, organismo=quien or "agregado",
                    especie=quien or "no desglosado")

    return dict(vacio, organismo="sin medir", especie="sin medir")


def aplicar_filtros(filas: list[dict], umbrales: dict, riesgo: dict | None = None) -> None:
    """Marca `fuera` y `motivo_fuera` en cada fila. No borra nada: el descarte se ve."""
    tope_corrida = int(_num(umbrales.get("corrida_max"), UMBRALES_DEFECTO["corrida_max"]))
    tope_off = int(_num(umbrales.get("off_target"), UMBRALES_DEFECTO["off_target"]))
    for f in filas:
        motivos = []
        if f.get("corrida_max", 0) > tope_corrida:
            motivos.append(f"corrida de {f['corrida_max']} nt iguales (tope {tope_corrida})")
        peor = _peor_off_target(f, riesgo)
        f["off_target_peor"] = peor["tramo_max"]
        f["off_target_donde"] = peor
        # El detalle por organismo sigue la misma regla que el peor caso: si el dato no
        # corresponde a esta ventana, no se muestra como si correspondiera.
        f["off_target_detalle"] = ([] if peor["organismo"] in ("sin medir", "desactualizado")
                                   else (riesgo or {}).get(f["clave_unica"], []))
        if peor["tramo_max"] >= tope_off:
            motivos.append(f"tramo identico de {peor['tramo_max']} nt en "
                           f"{peor['especie'] or 'un organismo no objetivo'} "
                           f"(tope {tope_off} nt)")
        f["fuera"] = bool(motivos)
        f["motivo_fuera"] = " - ".join(motivos)


def valores_normalizados(filas: list[dict], claves: list[str]) -> None:
    """Lleva cada criterio a 0-1 segun su escala, sobre los candidatos que quedaron dentro.

    La normalizacion min-max depende del CONJUNTO: cambiar el archivo de entrada, o mover
    un umbral que saca candidatos, cambia los valores normalizados y por lo tanto el
    score. Es la misma convencion del pipeline, y por eso el informe guarda el hash del
    archivo de entrada junto con los umbrales usados.
    """
    dentro = [f for f in filas if not f["fuera"]]
    normas: dict[str, list[float]] = {}
    for k in claves:
        esc = POR_CLAVE[k]["escala"]
        crudos = [_num(f.get(k)) for f in dentro]
        if not crudos:
            normas[k] = []
        elif esc == "minmax":
            normas[k] = normalizar(crudos)
        elif esc == "desea_gc":
            normas[k] = [deseabilidad_gc(v) for v in crudos]
        else:
            normas[k] = [float(v) for v in crudos]
    for j, f in enumerate(dentro):
        f["norm"] = {k: normas[k][j] for k in claves}
    for f in filas:
        if f["fuera"]:
            f["norm"] = {k: None for k in claves}


def rankear(filas: list[dict], pesos: dict, agregacion: str = "suma") -> list[dict]:
    """Puntua y ordena. Devuelve los que quedaron dentro, de mejor a peor.

    `pesos` se normaliza para que sume 1: mover un slider no tiene que cambiar la escala
    del score, solo el reparto entre criterios.
    """
    claves = [k for k in pesos if k in POR_CLAVE and _num(pesos[k]) > 0]
    total = sum(_num(pesos[k]) for k in claves)
    if not claves or total <= 0:
        return []
    w = {k: _num(pesos[k]) / total for k in claves}
    valores_normalizados(filas, claves)
    dentro = [f for f in filas if not f["fuera"]]
    if not dentro:
        return []

    medianas = {k: statistics.median([f["norm"][k] for f in dentro]) for k in claves}
    base = sum(w[k] * medianas[k] for k in claves)
    for f in dentro:
        aportes = {k: w[k] * f["norm"][k] for k in claves}
        f["score_suma"] = sum(aportes.values())
        producto = 1.0
        for k in claves:
            producto *= max(f["norm"][k], 1e-6) ** w[k]
        f["score_geom"] = producto
        f["score"] = f["score_geom"] if agregacion == "geometrica" else f["score_suma"]
        f["aportes"] = aportes
        f["aportes_vs_mediana"] = {k: w[k] * (f["norm"][k] - medianas[k]) for k in claves}
        f["base_mediana"] = base
        f["pesos_usados"] = w
    orden = sorted(dentro, key=lambda f: (-f["score"], f["clave_unica"]))
    for i, f in enumerate(orden):
        f["puesto"] = i + 1
    return orden


def cascada(fila: dict, modo: str = "vs_mediana") -> dict:
    """Los datos del grafico de cascada de un candidato.

    `vs_mediana` arranca en el score del candidato tipico del conjunto y cada barra es
    cuanto lo separa de el ese criterio. Contesta "por que quedo aca".
    `absoluto` arranca en cero y las barras suman el score. Contesta "de que esta hecho".
    """
    clave = "aportes_vs_mediana" if modo == "vs_mediana" else "aportes"
    aportes = fila.get(clave, {})
    inicio = fila.get("base_mediana", 0.0) if modo == "vs_mediana" else 0.0
    barras = []
    acum = inicio
    for k, v in sorted(aportes.items(), key=lambda kv: -abs(kv[1])):
        c = POR_CLAVE[k]
        barras.append({
            "clave": k, "etiqueta": c["etiqueta"], "evidencia": c["evidencia"],
            "nota": c["nota"], "unidad": c["unidad"], "sentido": c["sentido"],
            "peso": fila["pesos_usados"][k], "valor_crudo": fila.get(k),
            "valor_norm": fila["norm"][k], "aporte": v,
            "desde": acum, "hasta": acum + v,
        })
        acum += v
    nota = ""
    if abs(fila["score"] - fila["score_suma"]) > 1e-9:
        nota = ("La cascada descompone la suma ponderada. El ranking mostrado usa media "
                "geometrica, que no es una suma: las barras explican de donde sale la "
                "diferencia entre criterios, pero no suman al numero del ranking.")
    return {"modo": modo, "inicio": inicio, "total": acum, "barras": barras,
            "score": fila["score"], "score_suma": fila["score_suma"],
            "score_geom": fila["score_geom"], "nota": nota}


def cargar_riesgo_por_organismo() -> dict:
    """clave_unica -> un renglon por organismo no objetivo. Lo escribe preparar_riesgo.py."""
    ruta = DATOS_PIPELINE / "riesgo_por_organismo.csv"
    if not ruta.exists():
        return {}
    salida: dict[str, list[dict]] = {}
    with ruta.open(encoding="utf-8") as fh:
        for f in csv.DictReader(fh):
            # `_medida` es el centinela que deja constancia de que la ventana se midio
            # contra todo el catalogo aunque no haya pegado en ninguna especie. Es lo que
            # permite distinguir "limpia" de "nunca medida". No es una especie, asi que no
            # entra en el detalle que se muestra.
            if f["organismo"] == "_medida":
                salida.setdefault(clave_de(f), [])
                continue
            salida.setdefault(clave_de(f), []).append({
                "organismo": f["organismo"], "especie": f["especie"],
                "grupo": f.get("grupo") or "",
                "ensamblado": f["ensamblado"], "tramo_max": int(_num(f["tramo_max"], 0)),
                "transcripto": f["transcripto"],
                # La secuencia con la que se midio. Segunda capa de defensa: la clave ya
                # incluye el sitio, asi que un desajuste no deberia ni llegar aca.
                "sitio": (f.get("sitio") or "").upper(),
            })
    for items in salida.values():
        items.sort(key=lambda d: -d["tramo_max"])
    return salida


def procedencia_riesgo() -> dict:
    """De que archivo salio la tabla de riesgo y cuando. Lo escribe preparar_riesgo.py."""
    ruta = DATOS_PIPELINE / "riesgo_por_organismo.json"
    if not ruta.exists():
        return {}
    try:
        return json.loads(ruta.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}


def riesgo_verificable(riesgo: dict) -> bool:
    """Si la tabla de riesgo trae la secuencia con que se midio cada ventana.

    Una tabla vieja, sin columna `sitio`, no se puede confrontar contra los candidatos
    cargados: si el pipeline regenero las ventanas, la clave puede ser la misma y la
    secuencia otra, y no hay forma de detectarlo. En ese caso no se puede afirmar que el
    dato corresponda, y la app lo avisa en vez de confiar en silencio.
    """
    for items in riesgo.values():
        if items:
            return bool(items[0].get("sitio"))
    # Todas las ventanas limpias: no hay con que comprobarlo, pero tampoco hay ningun
    # dato que pueda estar mal atribuido.
    return True


def curva_umbral(filas: list[dict], riesgo: dict | None) -> list[dict]:
    """Cuantos candidatos sobreviven a cada umbral de off-target posible.

    Es la curva que el pipeline imprime por consola. Mostrarla es el punto: el umbral es
    una palanca enorme y elegir el numero le toca al biologo, no a nosotros.
    """
    peores = [_peor_off_target(f, riesgo)["tramo_max"] for f in filas]
    n = len(peores) or 1
    salida = []
    for u in range(K_ALERTA, K + 1):
        caen = sum(1 for v in peores if v >= u)
        salida.append({"umbral": u, "caen": caen, "sobreviven": n - caen,
                       "pct": round((n - caen) / n * 100, 1)})
    return salida


def estabilidad(filas: list[dict], n: int = 10, muestras: int = 1000,
                agregacion: str = "suma", semilla: int = 0) -> dict:
    """Frecuencia con que cada candidato entra al top-N barriendo todo el espacio de pesos.

    Es el analisis de sensibilidad de `sirna_enumerar.sensibilidad` aplicado al conjunto
    cargado. Contesta cuales candidatos son robustos a como pesemos los criterios y
    cuales estan arriba solo por los pesos que elegimos nosotros.
    """
    import random

    claves = criterios_presentes(filas)
    valores_normalizados(filas, claves)
    dentro = [f for f in filas if not f["fuera"]]
    if not dentro or not claves:
        return {"muestras": 0, "n": n, "top": [], "distintos": 0, "robustos": 0}

    base = [{"clave_unica": f["clave_unica"], "norm": f["norm"]} for f in dentro]
    conteo: dict[str, int] = {}
    rnd = random.Random(semilla)
    for _ in range(muestras):
        crudo = [rnd.gammavariate(1.0, 1.0) for _ in claves]
        total = sum(crudo) or 1.0
        w = {k: v / total for k, v in zip(claves, crudo)}
        if agregacion == "geometrica":
            def puntaje(d):
                p = 1.0
                for k in claves:
                    p *= max(d["norm"][k], 1e-6) ** w[k]
                return p
        else:
            def puntaje(d):
                return sum(w[k] * d["norm"][k] for k in claves)
        for d in sorted(base, key=lambda d: -puntaje(d))[:n]:
            conteo[d["clave_unica"]] = conteo.get(d["clave_unica"], 0) + 1

    etiqueta = {f["clave_unica"]: f for f in dentro}
    top = [{"clave_unica": c, "locus": etiqueta[c]["locus"], "pos": etiqueta[c]["pos"],
            "gen": etiqueta[c]["gen_drosophila"] or etiqueta[c]["tribolium"],
            "frecuencia": round(v / muestras * 100, 1)}
           for c, v in sorted(conteo.items(), key=lambda kv: -kv[1])]
    return {"muestras": muestras, "n": n, "top": top[:20], "distintos": len(conteo),
            "robustos": sum(1 for v in conteo.values() if v / muestras > 0.5)}


# ---------------------------------------------------------------------------
# Seleccion de gen. Va antes que todo lo de arriba en el orden de la decision:
# la sesion F2 midio que elegir la mejor region dentro de un gen gana ~7 % sobre
# el promedio del gen y en 0 de 20 genes es significativo. Lo que discrimina es
# QUE GEN se ataca y el filtro de off-target, no el score de la ventana.
# ---------------------------------------------------------------------------

# Blancos ya publicados para esta especie, con quien los eligio y para que. Son el
# control de la pantalla de objetivos: cada grupo eligio su gen para un objetivo
# distinto, asi que un ranking honesto los tiene que ordenar distinto segun el objetivo.
PUBLICADOS = {
    "Vha55": {"descripcion": "V-ATPase B", "grupo": "Texas A&M", "objetivo_del_grupo": "letal",
              "detalle": "Elegido para matar; reportan caida de supervivencia en ninfas."},
    "Vha36-1": {"descripcion": "V-ATPase D", "grupo": "Texas A&M", "objetivo_del_grupo": "letal",
                "detalle": "Mismo trabajo, misma estrategia."},
    "BicC": {"descripcion": "Bicaudal C", "grupo": "Catalano y colegas",
             "objetivo_del_grupo": "esteril",
             "detalle": "Elegido a proposito por dar un fenotipo visible NO letal: "
                        "esterilidad, para bajar el crecimiento poblacional sin matar."},
}

_tabla_loci: list[dict] | None = None


def cargar_loci() -> list[dict]:
    """La tabla unificada de loci con fenotipo. Se lee una sola vez."""
    global _tabla_loci
    if _tabla_loci is None:
        ruta = SALIDA_PIPELINE / "tabla_unificada.csv"
        if not ruta.exists():
            _tabla_loci = []
        else:
            with ruta.open(encoding="utf-8") as fh:
                _tabla_loci = list(csv.DictReader(fh))
    return _tabla_loci


def objetivos_disponibles() -> list[dict]:
    """Los objetivos de control que el pipeline sabe puntuar, con su explicacion."""
    textos = {
        "letal": "Matar al insecto. Efecto rapido y presion de seleccion alta.",
        "esteril": "Cortar la reproduccion. Mas lento pero sostenido; es lo que eligio el "
                   "unico grupo argentino que publico sobre la especie.",
        "morfologico": "Incapacitar (alas, movilidad). Baja la capacidad de transmitir sin "
                       "matar.",
        "cualquiera": "Cualquier fenotipo distinto de normal.",
    }
    return [{"clave": k, "detalle": textos.get(k, "")} for k in OBJETIVOS]


def rankear_genes(objetivo: str, tope: int = 60) -> dict:
    """Rankea los loci para un objetivo de control, usando el scoring del pipeline.

    No reimplementa nada: llama a `objetivo_candidatos.puntuar`. Lo que agrega es decir
    donde cae cada blanco ya publicado, que es el control de que el ranking responde al
    objetivo y no a un supuesto escondido.
    """
    if not puntuar_objetivo or objetivo not in OBJETIVOS:
        return {"objetivo": objetivo, "disponible": False, "genes": [], "publicados": [],
                "n_total": 0, "n_con_evidencia": 0}
    filas = cargar_loci()
    puntuados = []
    for f in filas:
        s = puntuar_objetivo(f, objetivo)
        if s > 0:
            puntuados.append((s, f))
    puntuados.sort(key=lambda par: -par[0])

    def publicar(i: int, s: float, f: dict) -> dict:
        gen = f.get("gen_drosophila") or ""
        return {
            "puesto": i, "locus": f["locus"], "gen": gen or f.get("mejor_hit_tribolium") or "",
            "score": round(s, 4), "categoria": f.get("fenotipo_categoria") or "",
            "nivel_evidencia": f.get("nivel_evidencia") or "",
            "distancia": f.get("fenotipo_distancia") or "",
            "letalidad": f.get("letalidad_pct_max") or "",
            "tribolium": f.get("mejor_hit_tribolium") or "",
            "n_letal": f.get("n_letal") or "0", "n_esteril": f.get("n_esteril") or "0",
            "n_morfologico": f.get("n_morfologico") or "0",
            "n_normal": f.get("n_normal") or "0",
            "confianza": round(calidad_alineamiento(f), 3) if calidad_alineamiento else None,
            "publicado": PUBLICADOS.get(gen),
        }

    genes = [publicar(i, s, f) for i, (s, f) in enumerate(puntuados[:tope], start=1)]

    # Donde cae cada blanco publicado en ESTE objetivo. Si no entro, se dice que no entro.
    publicados = []
    for gen, meta in PUBLICADOS.items():
        hallado = next(((i, s, f) for i, (s, f) in enumerate(puntuados, start=1)
                        if f.get("gen_drosophila") == gen), None)
        if hallado:
            i, s, f = hallado
            publicados.append({**publicar(i, s, f), "gen": gen, "meta": meta,
                               "de": len(puntuados),
                               "percentil": round(i / len(puntuados) * 100, 1)})
        else:
            publicados.append({"gen": gen, "meta": meta, "puesto": None,
                               "de": len(puntuados), "percentil": None})
    return {"objetivo": objetivo, "disponible": True, "genes": genes,
            "publicados": publicados, "n_total": len(filas),
            "n_con_evidencia": len(puntuados), "confianza_minima": CONFIANZA_MINIMA}


def publicados_por_objetivo() -> dict:
    """Donde cae cada blanco publicado en CADA objetivo.

    Es la demostracion de la pantalla: el mismo sistema, cambiando solo el objetivo de
    control, reordena completo. Cada grupo eligio su gen para un objetivo distinto y el
    ranking lo refleja.
    """
    salida: dict[str, list[dict]] = {}
    for obj in OBJETIVOS:
        salida[obj] = rankear_genes(obj, tope=0)["publicados"]
    return salida
