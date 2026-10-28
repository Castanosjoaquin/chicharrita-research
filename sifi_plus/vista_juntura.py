"""Vista C: la juntura de la quimera, con el bloque heredado separado del fabricado.

Un bloque **heredado** entra entero en el aporte de un solo gen; uno **fabricado** toma al menos
un nucleotido de cada lado y por lo tanto **no existe en ninguno de los dos genes**. Esa
distincion es la que decide la alerta —un acierto contra una referencia en un bloque fabricado
es riesgo que el empalme invento— y es la que el dibujo tiene que hacer obvia. Por eso van en
dos colores y no en dos columnas de una tabla.

La vista **lee** `cruza_la_union` de cada ficha; no lo deduce de `nt_de_izquierda` y
`nt_de_derecha`. Que las tres cosas sean consistentes se verifica contra el conteo que el
resumen publica, y si no lo fueran la vista lo dice en vez de elegir una.

**Lo que esta vista no puede dibujar.** El archivo de detalle trae las fichas de los bloques
**con acierto**, no la de cada bloque que la juntura enumera: son 19 de los 240 que el REPORT de
O3 publica. Los otros 221 se dibujan como **no medidos** —ni heredados ni sin acierto—, porque
ninguna de sus propiedades esta en un archivo versionado y deducir su geometria seria calcular.
Es el estado 1 del preregistro, y es la respuesta correcta de esta linea: falta un archivo con
una ficha por bloque enumerado.
"""

from __future__ import annotations

from lectura import (MOTORES, NO_DECLARADA, entero, leer_json, leer_tsv, procedencia, rel)
from lectura import RAIZ

O3 = RAIZ / "research" / "ola6" / "O3_quimera_bicc_vatpase_b" / "resultados"
RESUMEN = O3 / "juntura_resumen_o3_corregido_vienna.tsv"
DETALLE = O3 / "juntura_detalle_o3_corregido_vienna.json"
CAMBIADAS = O3 / "quimeras_ventanas_cambiadas_o3_corregido_vienna.tsv"
COMANDO = "python research/ola6/O3_quimera_bicc_vatpase_b/scripts/ (ver el REPORT de O3)"

# El total de bloques que la juntura enumera **no se calcula aca**: se cita de donde esta
# publicado. La vista compara ese total con lo que el archivo trae y muestra la diferencia como
# no medida.
BLOQUES_PUBLICADOS = 240
FUENTE_PUBLICADOS = "research/ola6/O3_quimera_bicc_vatpase_b/REPORT.md:218"

COLS_RESUMEN = ("ventanas_de_juntura", "juntura_eficientes",
                "juntura_con_blanco_continuo_21nt", "juntura_eficientes_con_blanco_continuo",
                "bloques_con_acierto", "bloques_fabricados_por_el_empalme")


def _procedencia(det) -> dict:
    """Modo, motor y panel, leidos del JSON de detalle, que los declara los tres."""
    if not isinstance(det, dict):
        return procedencia(RESUMEN, nota="falta %s, que es donde se declaran el modo, el motor "
                                         "y el panel de esta corrida" % rel(DETALLE))
    backend = (det.get("backend") or "").strip()
    return procedencia(
        DETALLE,
        modo=(det.get("modo") or NO_DECLARADA).strip() or NO_DECLARADA,
        motor=MOTORES.get(backend, NO_DECLARADA if not backend else backend),
        panel=det.get("panel") or NO_DECLARADA,
        nota="bloque minimo %s nt. %s" % (det.get("min_bloque", "?"), det.get("limite", "")))


def _bloques(det: dict) -> dict:
    """Las fichas de bloque agrupadas por quimera, con su geometria para el dibujo.

    `pos_en_la_quimera` es el arranque de la **ventana**; el bloque arranca `bloque_offset`
    nucleotidos mas adelante y mide `bloque_largo`. Eso es lo que se dibuja, y sale tal cual del
    archivo.
    """
    por_quimera: dict[str, list] = {}
    for b in det.get("bloques_con_acierto") or []:
        pos = entero(b.get("pos_en_la_quimera"))
        off = entero(b.get("bloque_offset"), 0)
        largo = entero(b.get("bloque_largo"))
        aciertos = b.get("aciertos") or {}
        por_quimera.setdefault(b.get("quimera", ""), []).append({
            "j": entero(b.get("j")),
            "pos_ventana": pos,
            "inicio": None if pos is None or off is None else pos + off,
            "largo": largo,
            "offset": off,
            "nt_de_izquierda": entero(b.get("nt_de_izquierda")),
            "nt_de_derecha": entero(b.get("nt_de_derecha")),
            # Se LEE del archivo. No se recalcula desde los dos conteos de arriba.
            "fabricado": bool(b.get("cruza_la_union")),
            "ventana_eficiente": bool(b.get("ventana_eficiente")),
            "on_target_del_vector": bool(b.get("on_target_del_vector")),
            "blanco_continuo_en": b.get("blanco_continuo_en") or [],
            "organismos": sorted(aciertos.keys()),
            "aciertos": {k: list(v) for k, v in aciertos.items()},
        })
    for lista in por_quimera.values():
        lista.sort(key=lambda d: (d["j"] or 0, d["offset"] or 0))
    return por_quimera


def ver() -> dict:
    """Los dos ordenes, con sus bloques y las ventanas heredadas que cambiaron de veredicto."""
    filas, problema = leer_tsv(RESUMEN, COMANDO)
    if problema:
        return dict(problema, vista="juntura")

    det, falta_det = leer_json(DETALLE, COMANDO)
    cambiadas, falta_cam = leer_tsv(CAMBIADAS, COMANDO)
    bloques = _bloques(det) if isinstance(det, dict) else {}
    coordenadas = (det.get("coordenadas") if isinstance(det, dict) else None) or {}

    ordenes, choques = [], []
    for f in filas:
        q = f.get("quimera", "")
        mios = bloques.get(q, [])
        fabricados = [b for b in mios if b["fabricado"]]
        declarado_fab = entero(f.get("bloques_fabricados_por_el_empalme"))
        declarado_con = entero(f.get("bloques_con_acierto"))

        # Las dos verificaciones que esta vista si hace, que no son criterio sino consistencia
        # entre dos archivos de la misma corrida. Si no cierran, se muestran las dos cifras.
        if det is not None and declarado_fab is not None and len(fabricados) != declarado_fab:
            choques.append({"quimera": q, "que": "bloques fabricados",
                            "en_el_detalle": len(fabricados), "en_el_resumen": declarado_fab,
                            "archivo_detalle": rel(DETALLE), "archivo_resumen": rel(RESUMEN)})
        if det is not None and declarado_con is not None and len(mios) != declarado_con:
            choques.append({"quimera": q, "que": "bloques con acierto",
                            "en_el_detalle": len(mios), "en_el_resumen": declarado_con,
                            "archivo_detalle": rel(DETALLE), "archivo_resumen": rel(RESUMEN)})

        izq, der = (q[2:].split("__") + ["", ""])[:2] if q.startswith("Q_") else ("", "")
        corte = None
        if izq in coordenadas:
            a, b = coordenadas[izq]
            corte = int(b) - int(a) + 1

        ordenes.append({
            "quimera": q, "izquierda": izq, "derecha": der,
            "corte_nt": corte,
            "resumen": {c: entero(f.get(c)) for c in COLS_RESUMEN},
            "juntura_eficientes_j": [x.strip() for x in
                                     (f.get("juntura_eficientes_j") or "").split(",")
                                     if x.strip()],
            "referencias_fabricadas": [x.strip() for x in
                                       (f.get("referencias_fabricadas") or "").split(",")
                                       if x.strip()],
            "bloques": mios,
            "heredados": sum(1 for b in mios if not b["fabricado"]),
            "fabricados": len(fabricados),
            "cambiadas": [{"pos_quimera": entero(c.get("pos_quimera")),
                           "lado": c.get("lado", ""),
                           "antes": c.get("antes", ""), "ahora": c.get("ahora", ""),
                           "nt_hasta_la_union": entero(c.get("nt_hasta_la_union"))}
                          for c in cambiadas if c.get("quimera") == q],
        })

    en_archivo = sum(len(v) for v in bloques.values())
    return {
        "estado": "listo", "vista": "juntura", "ordenes": ordenes,
        "procedencia": _procedencia(det),
        "coordenadas": coordenadas,
        "contradicciones": choques,
        "falta_detalle": falta_det, "falta_cambiadas": falta_cam,
        # Lo que el archivo trae contra lo que la juntura enumera. La resta de dos cifras
        # leidas, no una cifra calculada: las dos tienen su archivo al lado.
        "cobertura_de_bloques": {
            "en_el_archivo": en_archivo,
            "publicados": BLOQUES_PUBLICADOS,
            "fuente_publicados": FUENTE_PUBLICADOS,
            "no_medidos": None if det is None else BLOQUES_PUBLICADOS - en_archivo,
            "nota": "el archivo de detalle trae las fichas de los bloques CON acierto. Los "
                    "demas no estan: se dibujan como no medidos, que no es lo mismo que "
                    "heredados ni que sin acierto. Falta un archivo con una ficha por bloque "
                    "enumerado.",
            "contradiccion_publicada":
                "research/ola6/O3_quimera_bicc_vatpase_b/REPORT.md:371 describe este archivo "
                "como «los 240 bloques»; en disco tiene %d fichas bajo "
                "`bloques_con_acierto`. La linea 218 del mismo REPORT lo dice bien. Se anota, "
                "no se corrige." % en_archivo,
        },
        "archivo": rel(RESUMEN), "archivo_detalle": rel(DETALLE),
        "archivo_cambiadas": rel(CAMBIADAS),
    }
