"""Prueba de azar por gen: la mejor region (por media) supera lo que sale al reordenar bloques de 30 ventanas?"""
import sys, pathlib
import numpy as np
sys.path.insert(0, r"C:\Proyectos\yHat\pipeline")
import region_scoring as rs
genes = rs.leer_ventanas(pathlib.Path(r"C:\Proyectos\yHat\investigathon\dsrip_baseline\multigen\ventanas_multigen.csv"))
rnd = np.random.default_rng(1)
pv, zs, gan = [], [], []
for locus, filas in genes.items():
    s = np.array([float(f["score"]) for f in filas]); n = len(s)
    reg = rs.regiones_de_un_gen(filas, 301, 5, 75, "score")
    obs = max(float(r["media"]) for r in reg)
    bl = [s[i:i + 30] for i in range(0, n, 30)]
    nulo = []
    for _ in range(100):
        t = np.concatenate([bl[i] for i in rnd.permutation(len(bl))])
        ff = [{"pos": f["pos"], "score": float(t[i]), "descarte": ""} for i, f in enumerate(filas)]
        nulo.append(max(float(r["media"]) for r in rs.regiones_de_un_gen(ff, 301, 20, 75, "score")))
    nulo = np.array(nulo); p = float((nulo >= obs).mean()); z = (obs - nulo.mean()) / nulo.std()
    pv.append(p); zs.append(z); gan.append(obs / s.mean() - 1)
    print(f"{locus}: ganancia {gan[-1]*100:.1f} %  z {z:.2f}  p {p:.2f}", flush=True)
print("genes con p<0.05:", sum(p < .05 for p in pv), "de", len(pv), "| z mediano", round(float(np.median(zs)), 2))
