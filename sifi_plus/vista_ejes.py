"""Vista E: los dos ejes por objeto, sin combinarlos en un puntaje.

Las dos regiones sueltas y las dos quimeras de O3, con sus dos ejes —eficacia y limpieza— bajo
las dos reglas de trato del vector. La vista los muestra **separados**: ponderar los dos ejes
para ordenar los cuatro objetos es un criterio, y el criterio no es de la demo. Si alguien
quiere un orden, el orden esta en el ranking del motor y tiene su propio preregistro.

Por eso esta vista tampoco ordena por una columna derivada ni calcula un «mejor». Ordena por el
objeto y por la regla, que es como el archivo ya viene.

**La procedencia queda a medias, y se dice.** El modo y el motor estan en el sidecar de la misma
corrida (`quimeras_meta_...json`); el **panel no esta declarado en ningun archivo de O3 fuera
del detalle de juntura**, y `limpieza` y `con_off_target` dependen del panel. Esas dos columnas
van con «procedencia no declarada».
"""

from __future__ import annotations

from lectura import MOTORES, NO_APLICA, NO_DECLARADA, entero, leer_json, leer_tsv, procedencia, rel
from lectura import RAIZ

O3 = RAIZ / "research" / "ola6" / "O3_quimera_bicc_vatpase_b" / "resultados"
TSV = O3 / "ejes_ranking_o3_corregido_vienna.tsv"
META = O3 / "quimeras_meta_o3_corregido_vienna.json"
COMANDO = "python research/ola6/O3_quimera_bicc_vatpase_b/scripts/ (ver el REPORT de O3)"

# Las dos columnas que dependen del panel, que es justo el campo que el archivo no declara.
COLS_DEPENDEN_DEL_PANEL = ("limpieza", "con_off_target", "con_21_perfecto")


def _decimal(v):
    s = str(v if v is not None else "").strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def ver() -> dict:
    filas, problema = leer_tsv(TSV, COMANDO)
    if problema:
        return dict(problema, vista="ejes")

    meta, falta_meta = leer_json(META, COMANDO)
    backend = ((meta or {}).get("backend") or "").strip() if isinstance(meta, dict) else ""
    modo = ((meta or {}).get("modo") or "").strip() if isinstance(meta, dict) else ""

    objetos = []
    for f in filas:
        objetos.append({
            "objeto": f.get("objeto", ""), "clase": f.get("clase", ""),
            "trato_dmaidis": f.get("trato_dmaidis", ""), "regla": f.get("regla", ""),
            "largo_nt": entero(f.get("largo_nt")), "n_ventanas": entero(f.get("n_ventanas")),
            # El eje de eficacia: no depende del panel, si del modo y del motor.
            "eficientes": entero(f.get("eficientes")),
            "eficacia": _decimal(f.get("eficacia")),
            # El eje de limpieza: depende del panel, que no esta declarado.
            "limpieza": {"valor": _decimal(f.get("limpieza")), "procedencia": NO_DECLARADA},
            "con_off_target": {"valor": entero(f.get("con_off_target")),
                               "procedencia": NO_DECLARADA},
            "con_21_perfecto": {"valor": entero(f.get("con_21_perfecto")),
                                "procedencia": NO_DECLARADA},
            "buenos_limpios": entero(f.get("buenos_limpios")),
            "vetada": f.get("vetada", ""),
        })

    reglas = sorted({o["regla"] for o in objetos if o["regla"]})
    return {
        "estado": "listo", "vista": "ejes", "objetos": objetos, "reglas": reglas,
        "procedencia": procedencia(
            TSV,
            modo=modo or NO_DECLARADA,
            motor=MOTORES.get(backend, NO_DECLARADA if not backend else backend),
            panel=NO_DECLARADA,
            nota="el modo y el motor los declara %s; el panel no lo declara ni este archivo ni "
                 "su sidecar, asi que %s van con «procedencia no declarada»"
                 % (rel(META), ", ".join(COLS_DEPENDEN_DEL_PANEL))),
        "columnas_sin_panel": list(COLS_DEPENDEN_DEL_PANEL),
        "falta_configuracion": falta_meta,
        "archivo": rel(TSV), "archivo_configuracion": rel(META),
        "texto": "Los dos ejes van separados y la vista no los combina en un puntaje: "
                 "ponderarlos es un criterio, y el criterio no es de la demo. La columna "
                 "`vetada` es la que el archivo trae; esta vista no la recalcula ni publica "
                 "ninguno de estos objetos como recomendacion.",
        "panel_no_aplica": NO_APLICA,
    }
