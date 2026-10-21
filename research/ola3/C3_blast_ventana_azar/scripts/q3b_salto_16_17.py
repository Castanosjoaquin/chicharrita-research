#!/usr/bin/env python3
"""Q3b - por que el salto de la tabla de ventanas esta en 17 y no es gradual.

La tabla de `pipeline/REPORT.md` §4.1 no cuenta k-meros sueltos: cuenta ventanas de
21 nt que sobreviven a un filtro de «ningun bloque contiguo de >= k nt aparece en la
referencia». Este script reconstruye exactamente esa cantidad a partir de los conteos
exactos por k-mero que dejo `q3_azar_vs_real.py`: una ventana de 21 nt tiene un bloque
de >= k nt en la referencia si y solo si alguno de sus 21-k+1 k-meros aparece.

Compara esa curva con la prediccion de Poisson lambda = (21-k+1) * 2N/4^k, que es el
modelo de azar uniforme con la multiplicidad de sub-ventanas incluida. Si las dos
curvas tienen la misma forma, el «salto» no es un umbral biologico: es el punto donde
lambda cruza el orden de 1.

Uso:
    python q3b_salto_16_17.py --salida <dir>
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

KS = list(range(16, 23))
REFS = ["A_mellifera_transcriptoma", "Z_mays_transcriptoma", "D_maidis_genoma"]
VENT = 21


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True)
    a = ap.parse_args()
    sal = Path(a.salida)
    meta = json.loads((sal / "q3_meta_ventanas.json").read_text())
    filas, extra = [], []
    for ref in REFS:
        z = np.load(sal / ("q3_observado_%s.npz" % ref))
        neff = {k: int(v) for k, v in zip(KS, z["neff"])}
        for conjunto in ("real", "barajado"):
            # indice por (gen, pos) para cada k
            idx = {}
            for k in KS:
                m = meta[str(k)]
                idx[k] = {(g, int(p)): i for i, (g, c, p) in enumerate(m) if c == conjunto}
            # ventanas de 21 nt del conjunto
            v21 = sorted(idx[VENT])
            for k in KS:
                obs = z["obs_k%d" % k]
                con_bloque = 0
                for (g, p) in v21:
                    hit = False
                    for off in range(VENT - k + 1):
                        j = idx[k].get((g, p + off))
                        if j is not None and obs[j] > 0:
                            hit = True
                            break
                    con_bloque += hit
                N = neff[k]
                lam = (VENT - k + 1) * 2.0 * N / 4.0 ** k
                filas.append({
                    "referencia": ref, "conjunto": conjunto, "k": k,
                    "ventanas_21nt": len(v21),
                    "con_bloque_ge_k": con_bloque,
                    "frac_con_bloque": con_bloque / len(v21),
                    "sobrevive_pct": 100.0 * (1 - con_bloque / len(v21)),
                    "lambda_uniforme": lam,
                    "frac_poisson_uniforme": 1 - np.exp(-lam),
                    "sobrevive_poisson_pct": 100.0 * np.exp(-lam),
                })
            # sobredispersion: aciertos concentrados en pocas ventanas
            for k in KS:
                obs = z["obs_k%d" % k]
                sel = np.array(sorted(idx[k].values()))
                o = obs[sel]
                N = neff[k]
                lam = 2.0 * N / 4.0 ** k
                extra.append({
                    "referencia": ref, "conjunto": conjunto, "k": k,
                    "kmeros": len(o), "aciertos_totales": int(o.sum()),
                    "kmeros_con_acierto": int((o > 0).sum()),
                    "frac_con_acierto": float((o > 0).mean()),
                    "frac_poisson_esperada": float(1 - np.exp(-lam)),
                    "aciertos_por_kmero_positivo": float(o[o > 0].mean()) if (o > 0).any() else 0.0,
                    "varianza_sobre_media": float(o.var() / o.mean()) if o.mean() > 0 else None,
                    "max_aciertos_en_un_kmero": int(o.max()),
                })
    with open(sal / "q3b_salto_16_17.tsv", "w") as fh:
        cols = list(filas[0].keys())
        fh.write("\t".join(cols) + "\n")
        for f in filas:
            fh.write("\t".join(str(f[c]) for c in cols) + "\n")
    with open(sal / "q3b_sobredispersion.tsv", "w") as fh:
        cols = list(extra[0].keys())
        fh.write("\t".join(cols) + "\n")
        for f in extra:
            fh.write("\t".join(str(f[c]) for c in cols) + "\n")
    for f in filas:
        print("%-26s %-9s k=%2d  con_bloque=%.4f  poisson=%.4f  sobrevive=%.1f%% (poisson %.1f%%)"
              % (f["referencia"], f["conjunto"], f["k"], f["frac_con_bloque"],
                 f["frac_poisson_uniforme"], f["sobrevive_pct"], f["sobrevive_poisson_pct"]))
    print("escrito en", sal)


if __name__ == "__main__":
    main()
