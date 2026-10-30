"""V2 - N1 y N2 del PREREGISTRO_ROBUSTEZ.md: el nulo de 50 permutaciones."""
from __future__ import annotations
import csv, json, sys
from pathlib import Path
import numpy as np

AQUI = Path(__file__).resolve(); RAIZ = AQUI.parents[4]; SAL = AQUI.parents[1] / "resultados_002972"
sys.path.insert(0, str(RAIZ / "research/ola4/M7_robustez_bicc/scripts"))
sys.path.insert(0, str(RAIZ / "tools/sifi21_port"))
import grilla_parametros as G   # noqa: E402
import ranking as R             # noqa: E402
import ranking_v2 as V          # noqa: E402
V.con_panel(sin_humano=False)
wr, wc = R.pesos_base()
excluir = R.excluidas_de({"gen": "X", "estrategia": "insecto", "region": (1, 300), "largo": 300}, "off")
LARGO, BANDA = 300, 59


def riesgo(tsv: Path, cons: str, n: int) -> dict:
    rk = {}
    with tsv.open(newline="") as f:
        rd = csv.DictReader(f, delimiter="\t"); cols = [c for c in rd.fieldnames if "|" in c]
        for c in cols:
            ref, crit = c.split("|", 1); ref = ref[:-4] if ref.endswith(".fna") else ref
            rk.setdefault(ref, {})[crit] = np.zeros(n, bool)
        for r in rd:
            if r["consulta"] != cons: continue
            p = int(r["pos"])
            for c in cols:
                if int(r[c] or 0) > 0:
                    ref, crit = c.split("|", 1); ref = ref[:-4] if ref.endswith(".fna") else ref
                    rk[ref][crit][p - 1] = True
    return rk


def frac_limpia_F3(rk: dict, n: int) -> float:
    """Definicion del eje 3 de F3: ventanas sin ningun bloque >=19 nt en ninguna referencia."""
    sucia = np.zeros(n, bool)
    for d in rk.values():
        sucia |= d["perfecto_21"] | d["perfecto_ge19"]
    return float((~sucia).sum()) / n


perm = {}
for l in (RAIZ / "work/V2b/nulo/perm.fasta").read_text().splitlines():
    if l.startswith(">"): cur = l[1:].strip(); perm[cur] = []
    else: perm[cur].append(l.strip())
perm = {k: "".join(v) for k, v in perm.items()}
NT = RAIZ / "work/V2b/nulo/offtarget/offtarget_por_sirna.tsv"
n = len(next(iter(perm.values()))) - 20

# ---- N1: nivel gen ----------------------------------------------------------------
obs_rk = riesgo(RAIZ / "work/V2/offtarget/offtarget_por_sirna.tsv", "GITV01002972_1_cds", 1174)
obs_gen = frac_limpia_F3(obs_rk, 1174)
nulo_gen = np.array([frac_limpia_F3(riesgo(NT, k, n), n) for k in perm])
N1 = {"observado": round(obs_gen, 4), "nulo_mediana": round(float(np.median(nulo_gen)), 4),
      "nulo_min": round(float(nulo_gen.min()), 4), "nulo_max": round(float(nulo_gen.max()), 4),
      "dentro_del_rango": bool(nulo_gen.min() <= obs_gen <= nulo_gen.max()),
      "percentil_del_observado": round(float((nulo_gen < obs_gen).mean() * 100), 1), "n_permutaciones": len(perm)}
print("N1 gen: observado %.4f  nulo %.4f (%.4f-%.4f)  -> %s"
      % (obs_gen, np.median(nulo_gen), nulo_gen.min(), nulo_gen.max(),
         "DENTRO del rango del nulo" if N1["dentro_del_rango"] else "FUERA del rango del nulo"), flush=True)

# ---- N2: nivel region -------------------------------------------------------------
def limpiezas_de(seq: str, rk: dict, nn: int) -> tuple[np.ndarray, float]:
    efi = G.eficientes(G.primitivos(seq, "vienna", "NN3"), "corregido", G.DEF_END, G.DEF_ACC)
    vals, con_veto = [], 0
    ini_max = len(seq) - BANDA - LARGO + 1
    for s in range(BANDA + 1, ini_max + 1):
        sl = slice(s - 1, s - 1 + 280)
        g = {"gen": "x", "n": 280, "eficiente": efi[sl].copy(), "presente": np.ones(280, bool),
             "riesgo": {ref: {c: d[c][sl].copy() for c in R.CRITERIOS} for ref, d in rk.items()}}
        e = R.ejes(g, 1, 280, wr, wc, excluir, False)
        vals.append(e["limpieza"]); con_veto += int(e["vetada"])
    return np.array(vals), con_veto / max(1, len(vals))

obs_vals, obs_veto = limpiezas_de("".join(l.strip() for l in
    (RAIZ / "work/V2/rpn6_cds.fna").read_text().split(">GITV01002972_1_cds", 1)[1].split(">")[0].splitlines()[1:]).upper(),
    obs_rk, 1225)
OBS_REG = 0.9901
todas, vetos = [], []
for k, s in perm.items():
    v, pv = limpiezas_de(s, riesgo(NT, k, n), n)
    todas.append(v); vetos.append(pv)
todas = np.concatenate(todas)
N2 = {"observado_325_624": OBS_REG,
      "nulo_n_regiones": int(todas.size), "nulo_mediana": round(float(np.median(todas)), 4),
      "nulo_p5": round(float(np.percentile(todas, 5)), 4), "nulo_p25": round(float(np.percentile(todas, 25)), 4),
      "nulo_p75": round(float(np.percentile(todas, 75)), 4), "nulo_min": round(float(todas.min()), 4),
      "nulo_max": round(float(todas.max()), 4),
      "percentil_del_observado": round(float((todas < OBS_REG).mean() * 100), 1),
      "tasa_base_de_veto_en_el_nulo": round(float(np.mean(vetos)), 4),
      "tasa_de_veto_en_el_gen_real": round(float(obs_veto), 4),
      "mejor_region_del_gen_real": round(float(obs_vals.max()), 4)}
print("N2 region: observado %.4f  nulo mediana %.4f  p5 %.4f  p25-p75 %.4f-%.4f  percentil %.1f"
      % (OBS_REG, np.median(todas), np.percentile(todas, 5), np.percentile(todas, 25),
         np.percentile(todas, 75), N2["percentil_del_observado"]), flush=True)
print("   veto en el nulo: %.2f%% de las regiones; en el gen real: %.2f%%"
      % (100 * np.mean(vetos), 100 * obs_veto), flush=True)
(SAL / "nulo_resumen.json").write_text(json.dumps({"N1": N1, "N2": N2, "semilla": 20261029},
                                                 ensure_ascii=False, indent=1))
