"""Barrido de configuraciones de si-Fi21 contra los conteos declarados por EPILAB.

Pregunta que contesta: existe UNA configuracion de si-Fi que reproduzca a la vez
todos los conteos de "numero de siRNA eficientes" declarados en la planilla del
corpus? Un acierto aislado en un gen no prueba nada; el criterio es simultaneo.

Uso:
    python barrido.py <fasta>=<conteo_declarado> [<fasta>=<conteo> ...]

Ejemplo:
    python barrido.py work/sifi_check/MP_MRFV_full.fasta=114 \
                      work/sifi_check/CP_MRFV_full.fasta=35
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np

# Para que el modulo se encuentre tambien con python -I (modo aislado, que no
# agrega el directorio del script al path).
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sifi_core import primitives

TEMPS = (22.0, 25.0, 37.0)
BACKENDS = ("exe", "vienna")
U_VALUES = tuple(range(1, 22))
END_THRS = (0.0, 0.5, 1.0, 1.5, 2.0)
ACCESS_THRS = (0.01, 0.05, 0.1, 0.15, 0.2, 0.3)
MODES = ("fiel", "corregido")
SIZE = 21


def leer_fasta(p) -> str:
    return "".join(l.strip() for l in Path(p).read_text().splitlines()
                   if not l.startswith(">"))


def vectorizar(prims):
    """Pasa los primitivos a arrays de numpy para barrer rapido."""
    ddg = np.array([p["dg_as"] - p["dg_s"] for p in prims], dtype=float)
    lunp = np.array([[np.nan if v != v else v for v in p["lunp"]] for p in prims],
                    dtype=float)
    nt19 = np.array([p["sirna"][SIZE - 3] in ("A", "T") for p in prims])
    nt2_at = np.array([p["sirna"][1] in ("A", "T") for p in prims])
    nt2_gc = np.array([p["sirna"][1] in ("G", "C") for p in prims])
    return ddg, lunp, nt19, nt2_at, nt2_gc


def contar(arrays, modo, u, end_thr, access_thr, terminal):
    ddg, lunp, nt19, nt2_at, nt2_gc = arrays
    strand_sel = ddg >= 0.0
    end_stab = ddg >= end_thr
    col = lunp[:, u]
    access_ok = np.where(np.isnan(col), False, col >= access_thr)
    thermo = strand_sel & end_stab & access_ok

    if not terminal:
        return int(thermo.sum())
    if modo == "fiel":
        # La rama del original: con nt19 A/T y nt2 no A/T, el veredicto
        # termodinamico se saltea y manda solo la accesibilidad.
        eff = np.where(nt19,
                       np.where(nt2_at, thermo, access_ok),
                       np.where(nt2_gc, thermo, False))
        return int(eff.sum())
    return int((thermo & (nt19 | nt2_gc)).sum())


def main(argv):
    if not argv:
        print(__doc__)
        return 1

    casos = []
    for arg in argv:
        ruta, _, decl = arg.partition("=")
        casos.append((Path(ruta).stem, leer_fasta(ruta), int(decl)))

    print("Genes: " + ", ".join("%s (declarado %d)" % (n, d) for n, _, d in casos))
    print("Configuraciones por gen: %d\n" % (
        len(TEMPS) * len(BACKENDS) * len(U_VALUES) * len(END_THRS) *
        len(ACCESS_THRS) * len(MODES) * 2))

    # arrays[(nombre, temp, backend)]
    arrays = {}
    for nombre, seq, _ in casos:
        for temp in TEMPS:
            for be in BACKENDS:
                arrays[(nombre, temp, be)] = vectorizar(
                    primitives(seq, temp_c=temp, backend=be, sirna_size=SIZE))
        print("primitivos calculados: %s" % nombre)
    print()

    exactas = []
    mejores = []
    grid = itertools.product(TEMPS, BACKENDS, MODES, U_VALUES, END_THRS,
                             ACCESS_THRS, (True, False))
    for temp, be, modo, u, end_thr, access_thr, terminal in grid:
        conteos = [contar(arrays[(n, temp, be)], modo, u, end_thr, access_thr, terminal)
                   for n, _, _ in casos]
        decls = [d for _, _, d in casos]
        err = sum(abs(c - d) for c, d in zip(conteos, decls))
        cfg = dict(temp=temp, backend=be, modo=modo, u=u, end_thr=end_thr,
                   access_thr=access_thr, terminal=terminal)
        if err == 0:
            exactas.append((cfg, conteos))
        mejores.append((err, cfg, conteos))

    mejores.sort(key=lambda t: t[0])
    nombres = [n for n, _, _ in casos]
    decls = [d for _, _, d in casos]

    if exactas:
        print("=== CONFIGURACIONES QUE REPRODUCEN TODOS LOS CONTEOS ===")
        for cfg, conteos in exactas:
            print("  %s -> %s" % (cfg, conteos))
    else:
        print("=== NINGUNA configuracion reproduce todos los conteos a la vez ===")

    print("\n=== 15 configuraciones mas cercanas (error = suma de |dif|) ===")
    print("err  " + "  ".join("%-14s" % n for n in nombres) +
          "   temp backend modo       u  endThr accThr term")
    print("     " + "  ".join("%-14s" % ("decl=%d" % d) for d in decls))
    vistos = set()
    for err, cfg, conteos in mejores:
        clave = tuple(conteos)
        if clave in vistos:
            continue
        vistos.add(clave)
        print("%-4d " % err + "  ".join("%-14d" % c for c in conteos) +
              "   %-4.0f %-7s %-10s %-2d %-6.1f %-6.2f %s"
              % (cfg["temp"], cfg["backend"], cfg["modo"], cfg["u"],
                 cfg["end_thr"], cfg["access_thr"], cfg["terminal"]))
        if len(vistos) >= 15:
            break
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
