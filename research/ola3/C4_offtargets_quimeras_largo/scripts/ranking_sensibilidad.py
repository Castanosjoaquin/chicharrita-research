"""Cuánto del orden de las cuatro regiones lo deciden los pesos que elegimos.

Alcance 3 de C4. No es un motor de ranking nuevo: es la prueba de sensibilidad del
criterio propuesto en `criterio_ranking_propuesto.md`, sobre los cuatro candidatos
de EPILAB y con los conteos medidos en esta investigación y en W5.

Modelo (todo `[H]`, salvo los conteos, que son medidos):

    puntaje = w_ef * densidad_de_eficientes
              - w_exp * aciertos_en_transcriptoma_de_cultivo
              - w_gen * aciertos_solo_en_genoma_de_cultivo
              - w_nti * aciertos_en_transcriptoma_de_insecto_no_objetivo

con los cuatro pesos en el símplex (suman 1) y las variables normalizadas por cada
100 ventanas de 21 nt de la región. Se barre el símplex con Dirichlet uniforme y se
cuenta cuántos órdenes distintos aparecen, cuáles son forzados por dominancia
(ningún peso no negativo los puede invertir) y cuáles dependen de la elección.

Uso:
    python research/ola3/C4_offtargets_quimeras_largo/scripts/ranking_sensibilidad.py
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

RESULTADOS = Path(__file__).resolve().parents[1] / "resultados"

# --- datos medidos --------------------------------------------------------
# ventanas de 21 nt y eficientes: port de si-Fi21, modo fiel, backend vienna,
#   sobre la región recortada (work/C4/sifi/fiel_vienna, resumen.json)
# aciertos: tools/sifi21_port/offtarget_21nt.py, criterio de bloque perfecto >=19 nt
#   maíz genoma y transcriptoma -> esta investigación (work/C4/offtarget/gen_vs_tx)
#   Homalodisca vitripennis (transcriptoma) -> W5, reproducido acá
REGIONES = {
    "MP_MRFV":    {"ventanas": 180, "eficientes": 20, "exp_cultivo": 3,
                   "solo_genoma_cultivo": 3, "nt_insecto": 0},
    "CP_MRFV":    {"ventanas": 180, "eficientes": 16, "exp_cultivo": 0,
                   "solo_genoma_cultivo": 0, "nt_insecto": 0},
    "BicC_Dm":    {"ventanas": 280, "eficientes": 22, "exp_cultivo": 3,
                   "solo_genoma_cultivo": 8, "nt_insecto": 30},
    "ATPaseD_Dm": {"ventanas": 280, "eficientes": 19, "exp_cultivo": 0,
                   "solo_genoma_cultivo": 0, "nt_insecto": 7},
}
N_SORTEOS = 20000
SEMILLA = 20261020


def vectores():
    nombres = list(REGIONES)
    V = []
    for n in nombres:
        d = REGIONES[n]
        k = 100.0 / d["ventanas"]
        V.append([d["eficientes"] * k, -d["exp_cultivo"] * k,
                  -d["solo_genoma_cultivo"] * k, -d["nt_insecto"] * k])
    return nombres, np.array(V)


def main():
    nombres, V = vectores()
    print("variables por 100 ventanas (eficientes, -exp, -solo_genoma, -nt_insecto):")
    for n, v in zip(nombres, V):
        print("   %-12s %s" % (n, np.round(v, 2)))

    # dominancia: a domina a b si es >= en las cuatro variables y > en alguna
    dominancias = []
    for a, b in itertools.permutations(range(len(nombres)), 2):
        if np.all(V[a] >= V[b]) and np.any(V[a] > V[b]):
            dominancias.append((nombres[a], nombres[b]))
    print("\npares forzados por dominancia (ningún peso no negativo los invierte):")
    for a, b in dominancias:
        print("   %s  >  %s" % (a, b))

    rng = np.random.default_rng(SEMILLA)
    W = rng.dirichlet(np.ones(4), size=N_SORTEOS)
    puntajes = W @ V.T                                   # (N, 4)
    ordenes = Counter()
    primeros = Counter()
    for fila in puntajes:
        idx = np.argsort(-fila)
        ordenes[tuple(nombres[i] for i in idx)] += 1
        primeros[nombres[idx[0]]] += 1

    print("\nquién queda primero, sobre %d juegos de pesos:" % N_SORTEOS)
    for n, c in primeros.most_common():
        print("   %-12s %6.2f %%" % (n, 100.0 * c / N_SORTEOS))
    print("\nórdenes completos distintos: %d" % len(ordenes))
    for o, c in ordenes.most_common(6):
        print("   %6.2f %%  %s" % (100.0 * c / N_SORTEOS, " > ".join(o)))

    # pares cuyo orden relativo nunca cambia en el barrido
    estables, inestables = [], []
    for a, b in itertools.combinations(range(len(nombres)), 2):
        gana_a = int(np.sum(puntajes[:, a] > puntajes[:, b]))
        if gana_a in (0, N_SORTEOS):
            estables.append((nombres[a], nombres[b], gana_a == N_SORTEOS))
        else:
            inestables.append((nombres[a], nombres[b], gana_a / N_SORTEOS))
    print("\npares estables en todo el barrido:")
    for a, b, a_gana in estables:
        print("   %s %s %s" % (a, ">" if a_gana else "<", b))
    print("pares que dependen de los pesos:")
    for a, b, f in inestables:
        print("   %s vs %s : %s primero en el %.1f %% del espacio" % (a, b, a, 100 * f))

    (RESULTADOS / "q5_sensibilidad_pesos.json").write_text(json.dumps({
        "n_sorteos": N_SORTEOS, "semilla": SEMILLA,
        "datos": REGIONES,
        "dominancias": dominancias,
        "primeros_pct": {k: 100.0 * v / N_SORTEOS for k, v in primeros.items()},
        "ordenes_distintos": len(ordenes),
        "ordenes_pct": {" > ".join(k): 100.0 * v / N_SORTEOS
                        for k, v in ordenes.most_common()},
        "pares_estables": [[a, b, bool(x)] for a, b, x in estables],
        "pares_dependientes": [[a, b, f] for a, b, f in inestables],
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nescrito en %s" % (RESULTADOS / "q5_sensibilidad_pesos.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
