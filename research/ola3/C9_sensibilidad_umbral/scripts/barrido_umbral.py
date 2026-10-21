"""C9 - sensibilidad de la recomendacion al umbral de si-Fi21. Sin etiquetas.

Pregunta: cuanto cambia la region recomendada por gen y el orden de candidatos
al mover los dos umbrales sin fuente primaria (brecha de extremos, accesibilidad).
NO mide si el valor por defecto es correcto.

Motor: ViennaRNA (backend vienna, temperatura 22 C). Los conteos absolutos no son
comparables con RNAplfold 2.1.5 (no disponible); las comparaciones internas si.

Uso (desde la raiz del repo, entorno w5bio):
    conda run -n w5bio python research/ola3/C9_sensibilidad_umbral/scripts/barrido_umbral.py
"""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / "tools" / "sifi21_port"))
from sifi_core import primitives, apply_rules  # noqa: E402

GENES = ["ATPaseD_Dm", "BicC_Dm", "CP_MRFV", "MP_MRFV"]
FASTA = ROOT / "work" / "W5" / "fasta"
OUT = HERE.parents[1] / "resultados"
SIZE = 21
REGION = 200
U = 8
TEMP = 22.0
MODES = ["fiel", "corregido"]
END_GRID = [round(0.1 * i, 2) for i in range(21)]        # 0,0 .. 2,0 kcal/mol
ACC_GRID = [round(0.05 + 0.01 * i, 2) for i in range(26)]  # 0,05 .. 0,30
DEF_END, DEF_ACC = 1.0, 0.1


def leer_fasta(p):
    return "".join(l.strip() for l in Path(p).read_text().splitlines()
                   if not l.startswith(">"))


def best_region(eff):
    """Misma regla que sifi_core.best_region: region de 200 posiciones con mas eficientes,
    primer maximo gana; solo regiones completas."""
    n = len(eff)
    if n == 0 or eff.sum() == 0:
        return None
    last_start = max(1, n - REGION + 1)
    cs = np.concatenate([[0], np.cumsum(eff)])
    starts = np.arange(1, last_start + 1)
    counts = cs[np.minimum(starts - 1 + REGION, n)] - cs[starts - 1]
    k = int(np.argmax(counts))
    return int(starts[k]), int(starts[k]) + REGION - 1, int(counts[k])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    prims, seqs = {}, {}
    for g in GENES:
        seq = leer_fasta(FASTA / f"{g}_full.fasta")
        seqs[g] = len(seq)
        prims[g] = primitives(seq, temp_c=TEMP, backend="vienna", sirna_size=SIZE)
        print(f"{g}: {len(seq)} nt, {len(prims[g])} ventanas", flush=True)

    rows = []
    for mode in MODES:
        for e in END_GRID:
            for a in ACC_GRID:
                per_gene = {}
                for g in GENES:
                    flags = np.array([apply_rules([p], mode=mode, u=U, end_thr=e,
                                                  access_thr=a, sirna_size=SIZE)
                                      for p in prims[g]], dtype=float)
                    n_eff = int(flags.sum())
                    reg = best_region(flags)
                    per_gene[g] = (n_eff, reg)
                    rows.append({
                        "modo": mode, "end_thr": e, "access_thr": a, "gen": g,
                        "n_ventanas": len(prims[g]), "n_eficientes": n_eff,
                        "region_inicio": reg[0] if reg else "", "region_fin": reg[1] if reg else "",
                        "region_eficientes": reg[2] if reg else 0,
                        "eficacia_region": round(reg[2] / REGION, 4) if reg else 0.0,
                        "es_defecto": int(mode and e == DEF_END and a == DEF_ACC),
                    })
                print(mode, e, a, flush=True) if (e == DEF_END and a == DEF_ACC) else None

    cols = list(rows[0].keys())
    with open(OUT / "grilla_umbral.tsv", "w", encoding="utf-8") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join(str(r[c]) for c in cols) + "\n")
    print("grilla escrita:", len(rows), "filas", flush=True)


if __name__ == "__main__":
    main()
