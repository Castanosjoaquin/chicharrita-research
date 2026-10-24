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

from sifi_core import COLUMNAS_FEATURES, DEFAULTS, SifiEngine, best_region, to_tsv

CASILLAS = ["strand_check", "end_check", "accessibility_check", "terminal_check"]


def cadena_criterio(c):
    """El criterio en una cadena corta, para el nombre del archivo.

    Mismo orden de campos que la cadena con la que el investigador declaro su configuracion,
    `siFi21_8_1.0_0.1_1111` (ADR D45): ventana de accesibilidad, umbral de extremos, umbral
    de accesibilidad y las cuatro casillas, mas el tamano de la ventana adelante.
    """
    return "s%d_u%d_e%g_a%g_%s" % (
        c["sirna_size"], c["accessibility_window"], c["end_stability_threshold"],
        c["accessibility_threshold"],
        "".join("1" if c[k] else "0" for k in CASILLAS))


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

    # Los parametros que el panel del original expone y que hasta ahora solo llegaban por
    # kwargs de SifiEngine. Los defaults son los del original y no se mueven: los nombres de
    # los TSV ya publicados dependen de ellos.
    g = ap.add_argument_group(
        "criterio",
        "Los mismos que el panel de si-Fi21 (`Resources/sifi2015.ui`). Los valores por "
        "defecto son los suyos.")
    g.add_argument("--sirna-size", type=int, default=DEFAULTS["sirna_size"],
                   dest="sirna_size", help="largo de la ventana, en nt (default 21)")
    g.add_argument("--ventana-acc", type=int, default=DEFAULTS["accessibility_window"],
                   dest="accessibility_window",
                   help="u: largo del tramo cuya probabilidad de desapareamiento se mira, "
                        "al final de la ventana (default 8)")
    g.add_argument("--umbral-extremos", type=float,
                   default=DEFAULTS["end_stability_threshold"],
                   dest="end_stability_threshold",
                   help="kcal/mol de diferencia de estabilidad de extremos (default 1.0)")
    g.add_argument("--umbral-acc", type=float, default=DEFAULTS["accessibility_threshold"],
                   dest="accessibility_threshold",
                   help="probabilidad minima de desapareamiento (default 0.1)")
    g.add_argument("--sin-hebra", action="store_false", dest="strand_check",
                   help="apaga la seleccion de hebra (la casilla del original)")
    g.add_argument("--sin-extremos", action="store_false", dest="end_check",
                   help="apaga la estabilidad de extremos")
    g.add_argument("--sin-acc", action="store_false", dest="accessibility_check",
                   help="apaga la accesibilidad del sitio blanco")
    g.add_argument("--sin-terminal", action="store_false", dest="terminal_check",
                   help="apaga la regla del nucleotido terminal 5'")
    a = ap.parse_args(argv)

    criterio = {k: getattr(a, k) for k in DEFAULTS}
    if criterio["accessibility_window"] > criterio["sirna_size"]:
        ap.error("--ventana-acc (%d) no puede ser mayor que --sirna-size (%d)"
                 % (criterio["accessibility_window"], criterio["sirna_size"]))

    # Sufijo solo cuando no es la tabla del original, para no cambiar los nombres de los
    # TSV que ya estan publicados.
    sufijo_nn = "" if a.tabla_nn == "NN3" else "_" + a.tabla_nn.lower()
    # Y otro cuando el criterio deja de ser el del original, para que una corrida con otro
    # tamano de ventana o con una casilla apagada no pise el TSV de la corrida por defecto.
    if criterio != DEFAULTS:
        sufijo_nn += "_" + cadena_criterio(criterio)
    salida = Path(a.salida) if a.salida else None
    if salida:
        salida.mkdir(parents=True, exist_ok=True)

    todo = []
    for ruta in a.fasta:
        for nombre, seq in leer_fastas(ruta):
            eng = SifiEngine(mode=a.modo, temp_c=a.temp, tabla_nn=a.tabla_nn, **criterio)
            ventanas, resumen = eng.run(seq, backend=a.backend)
            reg = best_region(ventanas, a.region)
            resumen["nombre"] = nombre
            resumen["mejor_region_%dnt" % a.region] = reg
            # El criterio queda en la salida: un conteo sin los umbrales con los que se
            # calculo no se puede reproducir ni comparar con otro.
            resumen["criterio"] = dict(criterio)
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
