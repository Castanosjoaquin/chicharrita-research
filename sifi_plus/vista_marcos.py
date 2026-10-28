"""Vista B: los tres marcos de conteo de una region.

Tres cifras para la misma region, que contestan tres preguntas distintas y por eso no se
promedian ni se eligen. La vista las muestra **las tres a la vez**, con la del marco 3
destacada —es la molecula que existiria— y las otras dos al lado, nunca en vez de.

La vista no decide cual tiene razon, igual que la interfaz no decide entre el modo fiel y el
corregido: muestra las tres con su etiqueta y dice que pregunta contesta cada una.

Las cifras salen de `tres_marcos.tsv` y **la configuracion de `tres_marcos.json`**, que es el
unico de los dos que la declara. Si esta el TSV y falta el JSON, las cifras se muestran con
«procedencia no declarada»: sin el JSON no hay archivo que diga con que modo y que motor se
contaron, y un conteo de eficientes sin eso no significa nada.
"""

from __future__ import annotations

from lectura import (MOTORES, NO_APLICA, NO_DECLARADA, entero, leer_json, leer_tsv,
                     procedencia, rel)
from lectura import RAIZ

O3 = RAIZ / "research" / "ola6" / "O3_quimera_bicc_vatpase_b" / "resultados"
TSV = O3 / "tres_marcos.tsv"
JSON = O3 / "tres_marcos.json"
COMANDO = "python research/ola6/O3_quimera_bicc_vatpase_b/scripts/ (ver el REPORT de O3)"

# Que contesta cada marco. El texto es de la vista y por eso va aca, al lado del codigo que lo
# muestra, y no escondido en una plantilla del navegador.
MARCOS = (
    {"n": 1, "columna": "marco1_contexto_todos",
     "titulo": "Marco 1 — en el contexto del gen, todos los arranques",
     "pregunta": "cuantas ventanas eficientes hay en este tramo cuando el plegado se calcula "
                 "sobre el gen entero y se cuentan todos los arranques del tramo",
     "arranques": "arranques_marco1"},
    {"n": 2, "columna": "marco2_contexto_comparables",
     "titulo": "Marco 2 — en el contexto del gen, solo los arranques comparables",
     "pregunta": "lo mismo, pero contando solo los arranques que tambien caben en la molecula "
                 "recortada, que es lo que hace comparables los dos marcos",
     "arranques": "arranques_comparables"},
    {"n": 3, "columna": "marco3_molecula",
     "titulo": "Marco 3 — la molecula que existiria",
     "pregunta": "cuantas ventanas eficientes tiene el ARNdc que se sintetizaria, con el "
                 "plegado calculado sobre ese fragmento y no sobre el gen entero",
     "arranques": "arranques_comparables"},
)

# Las otras columnas del TSV, que son diferencias entre los marcos y no un cuarto conteo.
DERIVADAS = ("limite_fisico", "contexto_neto", "pierden", "ganan")


def _config(meta) -> dict:
    """La procedencia, leida del bloque `configuracion` de `tres_marcos.json`.

    El panel va en **«no aplica»**: un conteo de ventanas eficientes no consulta ninguna
    referencia. Es el estado 2 del preregistro y no el 1: no es que no se haya mirado, es que
    esta cifra no tiene panel.
    """
    if not isinstance(meta, dict):
        return procedencia(TSV, panel=NO_APLICA,
                           nota="falta %s, que es el unico archivo que declara con que modo y "
                                "que motor se contaron estas cifras" % rel(JSON))
    c = meta.get("configuracion") or {}
    backend = (c.get("backend") or "").strip()
    crit = c.get("criterio") or {}
    detalle = ""
    if crit:
        detalle = ("tabla %s, %s °C, siRNA %s nt, umbral de extremos %s, umbral de "
                   "accesibilidad %s, ventana %s" % (
                       c.get("tabla_nn", "?"), c.get("temp_c", "?"),
                       crit.get("sirna_size", "?"), crit.get("end_stability_threshold", "?"),
                       crit.get("accessibility_threshold", "?"),
                       crit.get("accessibility_window", "?")))
    return procedencia(
        TSV,
        modo=(c.get("modo") or NO_DECLARADA).strip() or NO_DECLARADA,
        motor=MOTORES.get(backend, NO_DECLARADA if not backend else backend),
        panel=NO_APLICA,
        nota="la configuracion la declara %s; el panel no aplica porque un conteo de "
             "eficientes no consulta ninguna referencia. %s" % (rel(JSON), detalle))


def ver() -> dict:
    """Las siete regiones del archivo, cada una con sus tres marcos."""
    filas, problema = leer_tsv(TSV, COMANDO)
    if problema:
        return dict(problema, vista="marcos")

    meta, falta_json = leer_json(JSON, COMANDO)
    proc = _config(meta)

    regiones = []
    for f in filas:
        cifras = []
        for m in MARCOS:
            cifras.append({
                "marco": m["n"], "titulo": m["titulo"], "pregunta": m["pregunta"],
                "valor": entero(f.get(m["columna"])),
                "arranques": entero(f.get(m["arranques"])),
                "columna": m["columna"],
                "destacado": m["n"] == 3,
            })
        regiones.append({
            "gen": f.get("gen", ""), "inicio": entero(f.get("inicio")),
            "fin": entero(f.get("fin")), "largo": entero(f.get("largo")),
            "nota": f.get("nota", ""),
            "cifras": cifras,
            "derivadas": {c: entero(f.get(c)) for c in DERIVADAS},
            # La cifra de cabecera es la del marco 3 y queda nombrada como tal, para que el
            # dia que alguien lea el JSON de esta vista no tenga que adivinar cual eligio.
            "cabecera": {"marco": 3, "valor": entero(f.get("marco3_molecula"))},
        })

    return {
        "estado": "listo", "vista": "marcos", "regiones": regiones,
        "procedencia": proc,
        "configuracion_declarada": falta_json is None,
        "falta_configuracion": falta_json,
        "archivo": rel(TSV), "archivo_configuracion": rel(JSON),
        "texto": "Las tres cifras contestan tres preguntas distintas y no se promedian. La "
                 "destacada es la del marco 3, que es la molecula que existiria; las otras dos "
                 "van al lado para que se vea cuanto de la cifra del marco 1 viene del "
                 "contexto del gen entero.",
    }
