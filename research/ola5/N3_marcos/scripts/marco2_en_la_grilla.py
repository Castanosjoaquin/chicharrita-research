"""N3 - El marco intermedio cruzado con las 4.368 configuraciones.

El hueco que N3 dejo declarado. M7 cruzo la grilla de parametros con dos marcos de conteo
--la region dentro del gen y la molecula recortada-- y midio que la ventaja de `BicC_Dm`
922-1221 sobre la region de C7 se sostiene en el 36,4 % de las configuraciones en el primero y
en el 75,6 % en el segundo. El marco intermedio --los 21-meros que existen en la molecula, con
la accesibilidad evaluada en el gen, que es el que propone la carta del 2026-10-25-- quedo
medido solo en el punto por defecto. Si el laboratorio adopta ese marco como criterio, la
pregunta es si la comparacion aguanta ahi, y es lo que este script contesta.

No recalcula nada que M7 ya tenga: importa `primitivos` y `eficientes` de
`M7/scripts/grilla_parametros.py`, que son las mismas rutinas verificadas contra `apply_rules`
del port, y agrega una sola cuenta --el recorte del vector de veredictos al rango de arranques
comparables-- que es gratis porque sale del mismo vector que el marco 1.

Las anclas que tiene que reproducir, y aborta si no: los nueve conteos del punto por defecto de
las tres regiones en los tres marcos, y las cuatro fracciones publicadas por M7 para los marcos
1 y 3.

El eje del motor necesita `SIFI_RNAPLFOLD`; sin esa variable se declara **no corrido** y la
grilla queda en 2.184 configuraciones en vez de 4.368, como hace M7.

Uso (desde la raiz del repositorio):

    SIFI_RNAPLFOLD='/ruta/a/RNAplfold.exe' \\
        python research/ola5/N3_marcos/scripts/marco2_en_la_grilla.py
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
SALIDA = AQUI.parents[1] / "resultados"
sys.path.insert(0, str(RAIZ / "research" / "ola4" / "M7_robustez_bicc" / "scripts"))

from grilla_parametros import (ACC_GRID, BACKENDS, DEF_ACC, DEF_END, END_GRID,  # noqa: E402
                               HAY_EXE, K, MODOS, REGIONES, TABLAS, eficientes,
                               primitivos)

GEN = "BicC_Dm"
FASTA = RAIZ / "work" / "sifi_check" / f"{GEN}_full.fasta"
FOCO, RIVALES = "922-1221", ["2121-2420", "264-563"]

#: Punto por defecto, modo `corregido`, ViennaRNA, NN3: los tres marcos de las tres regiones.
ANCLA_PUNTO = {"922-1221": (36, 29, 26), "2121-2420": (35, 27, 22), "264-563": (20, 15, 17)}

#: Fracciones publicadas por M7 §2 para los marcos 1 y 3, en conjunto sobre las 4.368.
ANCLA_FRACCION = {("2121-2420", "contexto_todos"): 0.364,
                  ("2121-2420", "molecula"): 0.756,
                  ("264-563", "contexto_todos"): 0.991,
                  ("264-563", "molecula"): 0.996}

MARCOS = ["contexto_todos", "contexto_comparables", "molecula"]


def leer_fasta(ruta: Path) -> str:
    return "".join(l.strip() for l in ruta.read_text().splitlines()
                   if not l.startswith(">")).upper().replace("U", "T")


def main() -> int:
    if not FASTA.exists():
        raise SystemExit("falta %s; `work/` no esta en git" % FASTA)
    if not HAY_EXE:
        print("AVISO: sin SIFI_RNAPLFOLD el eje del motor queda no corrido; la grilla sale "
              "en %d configuraciones." % (len(END_GRID) * len(ACC_GRID) * len(MODOS)
                                          * len(TABLAS)))

    seq = leer_fasta(FASTA)
    moleculas = {n: seq[i - 1:f] for n, (i, f) in REGIONES.items()}

    # Los primitivos se calculan una vez por (backend, tabla): son lo caro.
    P_gen, P_mol = {}, {}
    for backend, tabla in itertools.product(BACKENDS, TABLAS):
        P_gen[(backend, tabla)] = primitivos(seq, backend, tabla)
        for n, mol in moleculas.items():
            P_mol[(n, backend, tabla)] = primitivos(mol, backend, tabla)
        print("primitivos listos: %s / %s" % (backend, tabla))

    filas = []
    for backend, tabla, modo, end_thr, acc_thr in itertools.product(
            BACKENDS, TABLAS, MODOS, END_GRID, ACC_GRID):
        ef_gen = eficientes(P_gen[(backend, tabla)], modo, end_thr, acc_thr)
        cuenta = {}
        for n, (ini, fin) in REGIONES.items():
            ult = fin - (K - 1)
            # `ef_gen` esta indexado desde 0 y las posiciones son 1-based.
            cuenta[(n, "contexto_todos")] = int(ef_gen[ini - 1:fin].sum())
            cuenta[(n, "contexto_comparables")] = int(ef_gen[ini - 1:ult].sum())
            ef_mol = eficientes(P_mol[(n, backend, tabla)], modo, end_thr, acc_thr)
            cuenta[(n, "molecula")] = int(ef_mol.sum())
        filas.append({"backend": backend, "tabla": tabla, "modo": modo,
                      "end_thr": end_thr, "acc_thr": acc_thr, "cuenta": cuenta})

    # Ancla 1: el punto por defecto, modo corregido, vienna, NN3.
    punto = next(f for f in filas
                 if f["backend"] == "vienna" and f["tabla"] == "NN3"
                 and f["modo"] == "corregido"
                 and f["end_thr"] == DEF_END and f["acc_thr"] == DEF_ACC)
    for n, esp in ANCLA_PUNTO.items():
        obt = tuple(punto["cuenta"][(n, m)] for m in MARCOS)
        if obt != esp:
            raise SystemExit("ancla del punto por defecto rota en %s: %s, publicado %s"
                             % (n, obt, esp))

    # Fracciones por marco y por rival.
    fracciones = {}
    for marco, rival in itertools.product(MARCOS, RIVALES):
        gana = sum(1 for f in filas
                   if f["cuenta"][(FOCO, marco)] > f["cuenta"][(rival, marco)])
        fracciones["%s/%s" % (marco, rival)] = {
            "configuraciones": len(filas), "gana": gana,
            "fraccion": round(gana / len(filas), 4),
            "empates": sum(1 for f in filas
                           if f["cuenta"][(FOCO, marco)] == f["cuenta"][(rival, marco)]),
            "margen_mediano": float(np.median([f["cuenta"][(FOCO, marco)]
                                               - f["cuenta"][(rival, marco)]
                                               for f in filas])),
        }

    # Ancla 2: las cuatro fracciones publicadas por M7, al 0,5 %.
    if len(filas) == 4368:
        for (rival, marco), esp in ANCLA_FRACCION.items():
            obt = fracciones["%s/%s" % (marco, rival)]["fraccion"]
            if abs(obt - esp) > 0.005:
                raise SystemExit("fraccion publicada por M7 no reproducida en %s/%s: "
                                 "%.4f, publicado %.3f" % (marco, rival, obt, esp))

    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "marco2_en_la_grilla.json").write_text(
        json.dumps({"configuraciones": len(filas),
                    "ejes": {"end_thr": len(END_GRID), "acc_thr": len(ACC_GRID),
                             "modos": MODOS, "tablas": TABLAS, "backends": BACKENDS},
                    "ancla_punto_por_defecto": {k: list(v)
                                                for k, v in ANCLA_PUNTO.items()},
                    "fracciones": fracciones}, indent=2, ensure_ascii=False),
        encoding="utf-8")

    print("\n%d configuraciones, %d marcos" % (len(filas), len(MARCOS)))
    print("%-24s %-12s %8s %8s %9s" % ("marco", "rival", "gana", "empates", "margen"))
    for k, v in fracciones.items():
        marco, rival = k.split("/")
        print("%-24s %-12s %7.1f%% %8d %9.1f"
              % (marco, rival, 100 * v["fraccion"], v["empates"], v["margen_mediano"]))
    print("\nresultados en %s" % (SALIDA / "marco2_en_la_grilla.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
