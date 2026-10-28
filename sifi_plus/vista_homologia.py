"""Vista G: la transferencia de nombre de gen por homologia reciproca (F1), leida de disco.

El transcriptoma del vector viene sin anotar. `F1` corrio DIAMOND contra dos proteomas de
referencia y dejo, por ORF, si se le puede poner nombre de gen y con cuanta confianza. Esta vista
muestra ese resultado. **No corre DIAMOND ni transfiere nada.**

Tres cosas que esta vista hace distinto de las anteriores, y las tres son del dato y no de
capricho:

**1. No lleva modo ni motor: `no aplica`.** Una transferencia por homologia no pasa por el
criterio de eficiencia de si-Fi ni por RNAplfold. El campo que ocupa el lugar del panel son las
**dos referencias con su SHA-256**, que es como este archivo declara contra que se corrio. Es el
primer caso donde el contrato de procedencia pide un campo distinto, y se resuelve declarandolo.

**2. La cifra de cabecera es la variante PREREGISTRADA.** Hay dos: `estricta_preregistrada` y
`ampliada_H_post_hoc`. La segunda se definio **despues de ver los datos** y rinde mas del doble de
ORFs reciprocos. Las dos se muestran y la etiqueta dice cual es cual; de cabecera va la
preregistrada. Poner la ampliada porque es mas grande seria elegir el numero despues de verlo.

**3. El control positivo no pasa la variante estricta, y eso va junto a la cifra.** El ORF de la
subunidad B de la V-ATPasa —que se sabe que esta— cae en `d_empate` en la estricta y solo pasa en
la ampliada. Es el dato que mas califica la lectura de toda la vista. El senuelo, en cambio, sale
limpio. Los dos se muestran arriba, no en una nota al pie.

Y las 131.683 filas del detalle **no se vuelcan al navegador**: se paginan y se filtran por
categoria.
"""

from __future__ import annotations

import csv
import gzip
import threading

from lectura import NO_APLICA, NO_DECLARADA, entero, falta, leer_json, procedencia, rel
from lectura import RAIZ

F1 = RAIZ / "research" / "ola6" / "F1_transferencia_homologia" / "resultados"
RESUMEN_LECTURA = F1 / "resumen_lectura.json"
RESUMEN = F1 / "resumen.json"
CONTROLES = F1 / "controles.json"
COMANDO = "python research/ola6/F1_transferencia_homologia/scripts/ (ver el REPORT de F1)"

# Las dos referencias, con el nombre con el que el archivo las llama.
REFERENCIAS = {
    "MQ": "Macrosteles quadrilineatus (UCM_ALF_1.0)",
    "HV": "Homalodisca vitripennis (UT_GWSS_2.1)",
}

# Las dos variantes, y cual es cual. El rotulo no es decorativo: es la diferencia entre un
# numero preregistrado y uno elegido despues de ver los datos.
VARIANTES = {
    "estricta_preregistrada": {
        "titulo": "Estricta (preregistrada)",
        "rotulo": "preregistrada",
        "que_es": "el criterio como quedo escrito antes de mirar los datos",
    },
    "ampliada_H_post_hoc": {
        "titulo": "Ampliada (post hoc)",
        "rotulo": "post hoc",
        "que_es": "una ampliacion definida DESPUES de ver los datos, que admite empates; rinde "
                  "mas ORFs y por eso mismo no puede ser la cifra de cabecera",
    },
}
VARIANTE_DE_CABECERA = "estricta_preregistrada"

# El embudo, en orden. Las seis categorias son excluyentes y su suma es el total de ORFs mas los
# contigs sin ORF, asi que el embudo se lee de arriba hacia abajo.
CATEGORIAS = (
    ("a_sin_orf", "el contig no tiene ningun ORF de largo suficiente"),
    ("b_sin_hit", "el ORF no tiene ningun hit en la referencia"),
    ("c_hit_no_reciproco", "tiene hit, pero la busqueda inversa no vuelve al mismo ORF"),
    ("d_empate", "la busqueda inversa vuelve empatada entre varios"),
    ("e_reciproco_sin_nombre", "hay reciprocidad, pero la referencia no tiene nombre informativo"),
    ("f_reciproco_con_nombre", "hay reciprocidad y nombre: a este ORF se le puede poner nombre"),
)

COLS_DETALLE = ("contig", "orf_aa", "orf_hebra", "orf_ini", "orf_fin", "categoria",
                "categoria_ampliada", "ref_id", "ref_producto", "nombre_normalizado",
                "pident", "cob_orf", "rotulo_cobertura", "banda_identidad", "evalue")

# El detalle son dos archivos de 2,4 MB comprimidos y 131.683 filas: descomprimirlos en cada
# pedido es medio segundo largo por pedido y la pagina pide uno por filtro. Se cachea por ruta y
# fecha de modificacion, de modo que si el archivo se regenera el cache se invalida solo.
_CACHE: dict = {}
_LOCK = threading.Lock()


def _detalle(ref: str):
    """Las filas del detalle de una referencia, cacheadas por fecha de modificacion."""
    ruta = F1 / ("transferencia_%s.tsv.gz" % ref)
    if not ruta.is_file():
        return None, falta(ruta, COMANDO)
    clave = (str(ruta), ruta.stat().st_mtime_ns)
    with _LOCK:
        if clave in _CACHE:
            return _CACHE[clave], None
    with gzip.open(ruta, "rt", encoding="utf-8", newline="") as fh:
        filas = [f for f in csv.DictReader(fh, delimiter="\t") if (f.get("contig") or "").strip()]
    with _LOCK:
        _CACHE.clear()          # una referencia a la vez: no hace falta mas de un archivo
        _CACHE[clave] = filas
    return filas, None


def _embudo(filas: list, columna: str) -> list:
    cuenta: dict = {}
    for f in filas:
        cuenta[(f.get(columna) or "").strip()] = cuenta.get((f.get(columna) or "").strip(), 0) + 1
    return [{"categoria": c, "que_es": q, "n": cuenta.get(c, 0)} for c, q in CATEGORIAS]


def ver(ref: str = "HV") -> dict:
    """La cabecera: el embudo, las dos variantes y los controles. Sin el detalle."""
    if ref not in REFERENCIAS:
        raise ValueError("la referencia es %s; recibi %r"
                         % (" o ".join(REFERENCIAS), ref))

    lectura, falta_lectura = leer_json(RESUMEN_LECTURA, COMANDO)
    if falta_lectura:
        return dict(falta_lectura, vista="homologia")
    meta, falta_meta = leer_json(RESUMEN, COMANDO)
    controles, falta_controles = leer_json(CONTROLES, COMANDO)
    filas, falta_det = _detalle(ref)

    variantes = []
    for clave, d in VARIANTES.items():
        bloque = (lectura or {}).get(clave) or {}
        por_ref = bloque.get(ref) or {}
        variantes.append({
            "variante": clave, "titulo": d["titulo"], "rotulo": d["rotulo"],
            "que_es": d["que_es"],
            "es_la_de_cabecera": clave == VARIANTE_DE_CABECERA,
            "orfs_reciprocos": por_ref.get("orfs_reciprocos"),
            "con_nombre_informativo": por_ref.get("con_nombre_informativo"),
            "sin_nombre_informativo": por_ref.get("sin_nombre_informativo"),
            "por_banda_de_identidad": por_ref.get("por_banda_de_identidad") or {},
            "por_cobertura": por_ref.get("por_cobertura") or {},
            "en_banda_ge90_y_cobertura_alta":
                por_ref.get("orfs_con_nombre_en_banda_ge90_y_cobertura_alta"),
            "contraste_MQ_vs_HV": bloque.get("contraste_MQ_vs_HV") or {},
        })

    # Las dos referencias con su SHA-256, que es lo que ocupa el lugar del panel.
    refs = []
    for k, v in ((meta or {}).get("referencias") or {}).items():
        refs.append({"ref": k, "nombre": REFERENCIAS.get(k, k),
                     "proteoma": v.get("proteoma", ""),
                     "sha256": (v.get("proteoma_sha256") or "")[:16] + "…"
                               if v.get("proteoma_sha256") else NO_DECLARADA})

    pos = (controles or {}).get("positivo_MQ") or {}
    senuelo = (controles or {}).get("senuelo") or {}

    return {
        "estado": "listo", "vista": "homologia", "ref": ref,
        "referencia_nombre": REFERENCIAS[ref],
        "referencias_disponibles": [{"id": k, "nombre": v} for k, v in REFERENCIAS.items()],
        "variantes": variantes,
        "variante_de_cabecera": VARIANTE_DE_CABECERA,
        "nota_de_las_variantes":
            "las dos variantes se muestran y la cifra de cabecera es la PREREGISTRADA. La "
            "ampliada se definio despues de ver los datos y rinde mas ORFs: ponerla de cabecera "
            "porque es mas grande seria elegir el numero despues de verlo.",
        "embudo": _embudo(filas, "categoria") if filas is not None else None,
        "embudo_ampliada": _embudo(filas, "categoria_ampliada") if filas is not None else None,
        "total_filas_del_detalle": len(filas) if filas is not None else None,
        "contigs": (meta or {}).get("contigs"),
        "orfs": (meta or {}).get("orfs"),
        "parametros": (meta or {}).get("parametros") or {},
        "diamond": (meta or {}).get("diamond", NO_DECLARADA),
        # Los controles, arriba y no al pie.
        "controles": {
            "positivo": {
                "orf": pos.get("orf", ""),
                "esperado": pos.get("mejor_hit_estricta", ""),
                "pident": pos.get("pident_estricta"),
                "categoria_estricta": pos.get("categoria_estricta", ""),
                "categoria_ampliada": pos.get("categoria_ampliada", ""),
                "pasa_estricta": pos.get("pasa_estricta"),
                "pasa_ampliada": pos.get("pasa_ampliada"),
                "lectura": "el control positivo es un ORF que SE SABE que esta. Que no pase la "
                           "variante estricta —cae en empate— es el dato que mas califica la "
                           "lectura de esta vista, y por eso va junto a la cifra.",
            },
            "senuelo": {
                "por_referencia": senuelo,
                "lectura": "mil consultas que no tendrian que dar hit. Si dieran, el metodo "
                           "estaria encontrando homologia donde no hay.",
            },
            "cordura_bicaudal": (controles or {}).get("cordura_bicc_MQ") or {},
        },
        # Un resultado que su propio autor declaro no leible no se muestra como resultado.
        "descartado": {
            "archivo": rel(F1 / "v1_resumen_un_orf_por_contig.json"),
            "estado": "v1 DESCARTADA POR SU PROPIO CONTROL: no se lee (PREREGISTRO.md, "
                      "Enmienda 1). Esta vista no la lee ni la muestra.",
        },
        "procedencia": procedencia(
            RESUMEN_LECTURA, modo=NO_APLICA, motor=NO_APLICA,
            panel=[r["ref"] for r in refs] or NO_DECLARADA,
            nota="una transferencia por homologia no pasa por el criterio de eficiencia de "
                 "si-Fi ni por RNAplfold: la hace %s. El lugar del panel lo ocupan las dos "
                 "referencias con su SHA-256."
                 % (meta or {}).get("diamond", "DIAMOND (version no declarada)")),
        "referencias_con_huella": refs,
        "falta_configuracion": falta_meta,
        "falta_controles": falta_controles,
        "falta_detalle": falta_det,
        "archivo": rel(RESUMEN_LECTURA), "archivo_configuracion": rel(RESUMEN),
        "archivo_controles": rel(CONTROLES),
        "archivo_detalle": rel(F1 / ("transferencia_%s.tsv.gz" % ref)),
    }


def detalle(ref: str = "HV", categoria: str = "f_reciproco_con_nombre", *,
            desde: int = 0, cuantas: int = 50, contiene: str = "") -> dict:
    """El detalle por ORF, paginado y filtrado. 131.683 filas no van al navegador enteras."""
    if ref not in REFERENCIAS:
        raise ValueError("la referencia es %s; recibi %r" % (" o ".join(REFERENCIAS), ref))
    validas = [c for c, _ in CATEGORIAS]
    if categoria and categoria not in validas:
        raise ValueError("la categoria es una de %s; recibi %r"
                         % (", ".join(validas), categoria))

    filas, problema = _detalle(ref)
    if problema:
        return dict(problema, vista="homologia_detalle", ref=ref)

    sel = [f for f in filas if (f.get("categoria") or "").strip() == categoria] \
        if categoria else list(filas)
    if contiene:
        t = contiene.lower()
        sel = [f for f in sel
               if t in (f.get("ref_producto") or "").lower()
               or t in (f.get("nombre_normalizado") or "").lower()
               or t in (f.get("contig") or "").lower()]

    desde = max(0, int(desde))
    cuantas = max(1, min(int(cuantas), 500))
    pagina = [{c: f.get(c, "") for c in COLS_DETALLE} for f in sel[desde:desde + cuantas]]
    for d in pagina:
        for c in ("orf_aa", "orf_ini", "orf_fin"):
            d[c] = entero(d.get(c))

    return {
        "estado": "listo", "vista": "homologia_detalle", "ref": ref,
        "categoria": categoria, "que_es": dict(CATEGORIAS).get(categoria, ""),
        "filas": pagina, "total": len(sel), "total_del_archivo": len(filas),
        "desde": desde, "cuantas": cuantas,
        "archivo": rel(F1 / ("transferencia_%s.tsv.gz" % ref)),
    }
