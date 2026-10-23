"""Corre el criterio de eficiencia de si-Fi21 sobre uno o varios FASTA, sin interfaz.

Uso:
    python run_sifi.py <fasta> [...] [--modo fiel|corregido] [--backend exe|vienna]
                       [--temp 22] [--region 200] [--salida DIR]

Por cada secuencia imprime el resumen y, si se pasa --salida, escribe un TSV con
una fila por ventana de 21 nt y todos los terminos del veredicto.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sifi_core import COLUMNAS_FEATURES, SifiEngine, best_region, to_tsv


def leer_fastas(ruta):
    """Devuelve [(nombre, secuencia)] de un FASTA simple o multiple."""
    nombre, buf, out = None, [], []
    for linea in Path(ruta).read_text().splitlines():
        if linea.startswith(">"):
            if nombre is not None:
                out.append((nombre, "".join(buf)))
            nombre, buf = linea[1:].strip().split()[0], []
        else:
            buf.append(linea.strip())
    if nombre is not None:
        out.append((nombre, "".join(buf)))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fasta", nargs="+")
    ap.add_argument("--modo", choices=("fiel", "corregido"), default="corregido")
    ap.add_argument("--backend", choices=("exe", "vienna"), default="vienna")
    ap.add_argument("--temp", type=float, default=22.0)
    ap.add_argument("--region", type=int, default=200,
                    help="largo de region a buscar por densidad de eficientes")
    ap.add_argument("--salida", default=None, help="directorio para los TSV")
    ap.add_argument("--tabla-nn", choices=("NN1", "NN2", "NN3", "NN4"), default="NN3",
                    dest="tabla_nn",
                    help="tabla de apilamiento: NN3 es la del original (default), NN4 la "
                         "que usa sifi21INTA (issue #6)")
    ap.add_argument("--features", action="store_true",
                    help="emite la tabla de terminos sin ningun booleano de veredicto, "
                         "para analizar como contribuyen a la eficiencia (issue #7)")
    ap.add_argument("--con-seq", action="store_true", dest="con_seq",
                    help="incluye la columna seq. NO versionar esa salida: la columna "
                         "reconstruye el gen entero (ver tools/verificacion/sin_secuencias.py)")
    a = ap.parse_args(argv)

    # Sufijo solo cuando no es la tabla del original, para no cambiar los nombres de los
    # TSV que ya estan publicados.
    sufijo_nn = "" if a.tabla_nn == "NN3" else "_" + a.tabla_nn.lower()
    salida = Path(a.salida) if a.salida else None
    if salida:
        salida.mkdir(parents=True, exist_ok=True)

    todo = []
    for ruta in a.fasta:
        for nombre, seq in leer_fastas(ruta):
            eng = SifiEngine(mode=a.modo, temp_c=a.temp, tabla_nn=a.tabla_nn)
            ventanas, resumen = eng.run(seq, backend=a.backend)
            reg = best_region(ventanas, a.region)
            resumen["nombre"] = nombre
            resumen["mejor_region_%dnt" % a.region] = reg
            todo.append(resumen)

            print("== %s ==" % nombre)
            print("   largo %d, ventanas %d" % (resumen["largo"], resumen["ventanas"]))
            print("   eficientes: %d  (%.1f%%)" % (
                resumen["eficientes"], 100.0 * resumen["eficientes"] / resumen["ventanas"]))
            print("   desglose: hebra %d, extremos %d, accesibilidad %d, termodinamico %d"
                  % (resumen["seleccion_hebra"], resumen["estabilidad_extremos"],
                     resumen["accesibilidad"], resumen["solo_termodinamico"]))
            if reg:
                print("   mejor region de %d nt: %d-%d con %d eficientes"
                      % (a.region, reg["inicio"], reg["fin"], reg["eficientes"]))
            if resumen["tablas_mismatch_usadas"]:
                print("   AVISO tablas de mismatch de ADN consultadas: %s"
                      % resumen["tablas_mismatch_usadas"])
            print()

            if salida:
                to_tsv(ventanas,
                       salida / ("%s_%s_%s%s.tsv" % (nombre, a.modo, a.backend, sufijo_nn)),
                       con_seq=a.con_seq)
                if a.features:
                    # La etiqueta va al final y aparte: la tabla de terminos es lo que
                    # se analiza, `is_efficient` es contra que se la analiza.
                    to_tsv(ventanas,
                           salida / ("%s_%s_%s%s_features.tsv" % (nombre, a.modo, a.backend, sufijo_nn)),
                           columnas=COLUMNAS_FEATURES + ["is_efficient"])

    if salida:
        (salida / "resumen.json").write_text(
            json.dumps(todo, indent=2, ensure_ascii=False), encoding="utf-8")
        print("escrito en %s" % salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
