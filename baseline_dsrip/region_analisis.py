"""Comparacion de agregaciones a nivel region y contra dsRIP, sobre V-ATPase A.

Usa pipeline/region_scoring.py. Rutas absolutas de la maquina de Luca; ajustar.
"""
import csv
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, r"C:\Proyectos\yHat\pipeline")
import region_scoring as rs  # noqa: E402

BASE = r"C:\Proyectos\yHat"
LARGO = 301  # 281 ventanas, igual que la region fija de dsRIP
AGGS = ["media", "mediana", "frac_buenos", "p10", "buenos_limpios"]

ours = list(csv.DictReader(open(BASE + r"\pipeline\salida\sirna_vatpaseA.csv")))
th = {r["antisense_5_3_DNA"]: r for r in csv.DictReader(open(BASE + r"\investigathon\dsrip_baseline\dsrip_vatpaseA.csv"))}
dsr = [float(th[o["guia"]]["total_score"]) for o in ours]
n = len(ours)


def regiones(filas, p=75, campo="score"):
    return rs.regiones_de_un_gen(filas, LARGO, 1, p, campo)


def mejor(reg, agg):
    return max(reg, key=lambda r: float(r[agg]))


def rango(r):
    return (r["inicio"], r["fin"])


reg = regiones(ours)
starts = [r["inicio"] for r in reg]

print("== A. acuerdo entre agregaciones (Spearman entre las", len(reg), "regiones deslizantes) ==")
for i, a in enumerate(AGGS):
    for b in AGGS[i + 1:]:
        print(f"  {a:>14} vs {b:<14} {stats.spearmanr([r[a] for r in reg], [r[b] for r in reg])[0]:.3f}")

print("\n== B. mejor region por agregacion (largo", LARGO, ") ==")
mej = {a: mejor(reg, a) for a in AGGS}
for a, r in mej.items():
    print(f"  {a:>14}: {r['inicio']}-{r['fin']}  vivos {r['frac_vivos']:.2f} media {r['media']:.3f} buenos {r['frac_buenos']:.2f} p10 {r['p10']:.3f}")

# dsRIP a nivel region: media del total_score (lo que hace find_best_siRNA_region)
d_filas = [{"pos": o["pos"], "score": dsr[i], "descarte": ""} for i, o in enumerate(ours)]
d_reg = rs.regiones_de_un_gen(d_filas, LARGO, 1, 75, "score")
d_mejor = mejor(d_reg, "media")
print(f"\n  dsRIP (media del total_score): {d_mejor['inicio']}-{d_mejor['fin']}")
d_bueno = mejor(d_reg, "frac_buenos")
print(f"  dsRIP (frac_buenos P75)      : {d_bueno['inicio']}-{d_bueno['fin']}")

print("\n== C. acuerdo con dsRIP a nivel region ==")
print("  solape en pb de la mejor region de cada agregacion con la mejor de dsRIP (media):")
for a, r in mej.items():
    s = rs.solape(rango(r), rango(d_mejor))
    print(f"    {a:>14}: {s} de {LARGO} pb ({s / LARGO * 100:.0f} %)")
print("  Spearman a lo largo de las regiones: metrica nuestra vs media del total_score de dsRIP")
d_media = [r["media"] for r in d_reg]
for a in AGGS:
    print(f"    {a:>14}: {stats.spearmanr([r[a] for r in reg], d_media)[0]:.3f}")
print("  mismo agregador a ambos lados (frac_buenos P75 vs frac_buenos P75):",
      round(stats.spearmanr([r['frac_buenos'] for r in reg], [r['frac_buenos'] for r in d_reg])[0], 3))
print("  mismo agregador a ambos lados (mediana vs mediana):",
      round(stats.spearmanr([r['mediana'] for r in reg], [r['mediana'] for r in d_reg])[0], 3))

print("\n== D. robustez de la region elegida a los pesos del score (150 juegos Dirichlet) ==")
comp = {k: np.array([float(o[k]) for o in ours]) for k in ("asimetria", "gc_9_14", "accesibilidad", "desea_gc", "a_en_10")}
vivo = np.array([o["descarte"] == "" for o in ours])


def nrm(v):
    lo, hi = v[vivo].min(), v[vivo].max()
    out = (v - lo) / (hi - lo) if hi > lo else np.full_like(v, .5)
    return np.where(vivo, out, 0.0)


N = {k: (nrm(comp[k]) if k in ("asimetria", "gc_9_14", "accesibilidad") else comp[k]) for k in comp}
rnd = np.random.default_rng(0)
elegidas = {a: [] for a in AGGS}
for _ in range(150):
    w = rnd.dirichlet(np.ones(5))
    s = w[0] * N["asimetria"] + w[1] * N["gc_9_14"] + w[2] * N["accesibilidad"] + w[3] * N["desea_gc"] + w[4] * N["a_en_10"]
    s = np.where(vivo, s, 0.0)
    filas = [{"pos": o["pos"], "score": float(s[i]), "descarte": o["descarte"]} for i, o in enumerate(ours)]
    rr = rs.regiones_de_un_gen(filas, LARGO, 10, 75, "score")  # paso 10 para acelerar
    for a in AGGS:
        elegidas[a].append(mejor(rr, a)["inicio"])
for a in AGGS:
    v = np.array(elegidas[a])
    base = mej[a]["inicio"]
    moda = int(stats.mode(np.round(v / 50) * 50, keepdims=False).mode)
    cerca = np.mean(np.abs(v - moda) <= 75)
    print(f"  {a:>14}: inicio mediano {int(np.median(v))}, rango intercuartil {int(np.percentile(v,25))}-{int(np.percentile(v,75))}, "
          f"{cerca * 100:.0f} % de los juegos cae a +-75 pb de la moda ({moda})")

print("\n== E. la mejor region se distingue del azar? (permutacion por bloques de 30 ventanas, 300 reps) ==")
base_s = np.array([float(o["score"]) for o in ours])
bloques = [base_s[i:i + 30] for i in range(0, n, 30)]
obs = {a: float(mej[a][a]) for a in ("media", "frac_buenos")}
nulo = {a: [] for a in obs}
for _ in range(300):
    idx = rnd.permutation(len(bloques))
    s = np.concatenate([bloques[i] for i in idx])
    filas = [{"pos": o["pos"], "score": float(s[i]), "descarte": ""} for i, o in enumerate(ours)]
    rr = rs.regiones_de_un_gen(filas, LARGO, 10, 75, "score")
    for a in obs:
        nulo[a].append(max(float(r[a]) for r in rr))
for a in obs:
    z = (obs[a] - np.mean(nulo[a])) / np.std(nulo[a])
    p = np.mean(np.array(nulo[a]) >= obs[a])
    print(f"  {a:>12}: observado {obs[a]:.3f}, maximo bajo azar {np.mean(nulo[a]):.3f} +- {np.std(nulo[a]):.3f}, z = {z:.2f}, p = {p:.3f}")
print("  media del gen:", round(base_s.mean(), 3), "| mejor region:", round(obs['media'], 3), f"(+{(obs['media'] / base_s.mean() - 1) * 100:.1f} %)")
