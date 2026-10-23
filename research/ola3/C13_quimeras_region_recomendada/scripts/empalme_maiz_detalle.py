"""Que bloque exacto del empalme cae en maiz, y en que transcriptos.

`offtarget_21nt.py` contesta si una ventana tiene un bloque perfecto de 19 nt o mas en
una referencia, no cual bloque ni donde. Para el hallazgo que importa de C13 --que el
empalme de `MP_MRFV` + `ATPaseD_Dm` crea aciertos en el transcriptoma de *Zea mays*
que no existen en ninguna de las dos regiones por separado-- hace falta el detalle:
cual de los tres bloques de 19 nt de cada ventana coincide, cuantos nucleotidos aporta
cada gen a ese bloque, y en que transcriptos cae.

Esto no reemplaza el tamizaje: lo audita en un caso. Scanea una sola referencia (el
transcriptoma de maiz) buscando los bloques de 19 y 20 nt y el 21-mero completo de las
ventanas de empalme indicadas, y reporta el identificador de cada transcripto que
coincide, en las dos hebras.

Nada sale de la maquina.

Uso:
    python research/ola3/C13_quimeras_region_recomendada/scripts/empalme_maiz_detalle.py
"""

from __future__ import annotations

import argparse
import gzip
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
BLOQUE = Path(__file__).resolve().parents[1]
DB_MAIZ = RAIZ / "work/offtarget_db/GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna.fna.gz"
COMP = str.maketrans("ACGT", "TGCA")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import quimeras_v2 as QV  # noqa: E402

# Las ventanas que el tamizaje marco con acierto en maiz, por quimera y posicion j
# dentro del tramo de 40 nt que cruza la union.
CASOS = [("MP_MRFV", "ATPaseD_Dm", [15, 16, 17]),
         ("BicC_Dm", "ATPaseD_Dm", [16])]


def rc(s: str) -> str:
    return s.translate(COMP)[::-1]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-block", type=int, default=19, dest="min_block")
    a = ap.parse_args(argv)

    regiones = QV.recortar("recomendadas")
    buscar = {}      # patron -> lista de etiquetas
    fichas = []
    for izq, der, js in CASOS:
        tramo = regiones[izq][-20:] + regiones[der][:20]
        for j in js:
            vent = tramo[j - 1:j + 20]
            n_izq = 21 - j          # nucleotidos que aporta el gen de la izquierda
            for largo in range(a.min_block, 22):
                for off in range(0, 21 - largo + 1):
                    bloque = vent[off:off + largo]
                    # de ese bloque, cuantos nt vienen de cada gen
                    desde_izq = max(0, min(largo, n_izq - off))
                    etiqueta = {"quimera": "Q_%s__%s" % (izq, der), "j": j,
                                "ventana": vent, "bloque": bloque, "largo": largo,
                                "offset": off, "nt_de_izquierda": desde_izq,
                                "nt_de_derecha": largo - desde_izq,
                                "es_nuevo": 0 < desde_izq < largo}
                    fichas.append(etiqueta)
                    buscar.setdefault(bloque, []).append(len(fichas) - 1)
                    buscar.setdefault(rc(bloque), []).append(len(fichas) - 1)

    print("%d bloques distintos a buscar en %s" % (len(buscar), DB_MAIZ.name))
    aciertos = {}
    nombre, buf = None, []
    with gzip.open(DB_MAIZ, "rt") as fh:
        for linea in fh:
            if linea.startswith(">"):
                if nombre is not None:
                    seq = "".join(buf)
                    for pat, idxs in buscar.items():
                        if pat in seq:
                            for i in idxs:
                                aciertos.setdefault(i, set()).add(nombre)
                nombre, buf = linea[1:].strip().split()[0], []
            else:
                buf.append(linea.strip().upper())
    if nombre is not None:
        seq = "".join(buf)
        for pat, idxs in buscar.items():
            if pat in seq:
                for i in idxs:
                    aciertos.setdefault(i, set()).add(nombre)

    salida = []
    for i, f in enumerate(fichas):
        if i not in aciertos:
            continue
        f = dict(f)
        f["transcriptos"] = sorted(aciertos[i])
        salida.append(f)
        print("\n%s  j=%d" % (f["quimera"], f["j"]))
        print("  ventana   %s" % f["ventana"])
        print("  bloque    %s (%d nt, offset %d)" % (f["bloque"], f["largo"], f["offset"]))
        print("  aporta    %d nt de %s + %d nt de %s  ->  %s" % (
            f["nt_de_izquierda"], f["quimera"].split("__")[0][2:],
            f["nt_de_derecha"], f["quimera"].split("__")[1],
            "secuencia que no existe en ningun gen" if f["es_nuevo"]
            else "bloque heredado de un solo gen"))
        print("  en maiz   %s" % ", ".join(f["transcriptos"]))
    if not salida:
        print("\nningun bloque coincide; el tamizaje y esta auditoria no concuerdan")
    (BLOQUE / "resultados" / "empalme_maiz_detalle.json").write_text(
        json.dumps(salida, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nescrito en %s" % (BLOQUE / "resultados" / "empalme_maiz_detalle.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
