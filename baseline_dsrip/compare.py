import csv, sys
import numpy as np
from scipy import stats
S = r"C:\Users\Luca\AppData\Local\Temp\claude\C--Proyectos-yHat\9bf9b77a-cd77-4b98-b86b-847bff6ee6a8\scratchpad"
ours = list(csv.DictReader(open(r"C:\Proyectos\yHat\pipeline\salida\sirna_vatpaseA.csv")))
theirs = list(csv.DictReader(open(S + r"\dsrip_vatpaseA.csv")))
by_guia = {r["antisense_5_3_DNA"]: r for r in theirs}
rows = []
for o in ours:
    t = by_guia.get(o["guia"])
    if t is None: continue
    rows.append((o, t))
print("emparejadas", len(rows), "de", len(ours))
def col(f, key): return np.array([float(f(r)[key]) for r in rows])
O = lambda r: r[0]; T = lambda r: r[1]
pairs = [("score ponderado (nuestro) vs dsRIP total_score", col(O,"score"), col(T,"total_score")),
         ("score_geom (nuestro) vs dsRIP total_score", col(O,"score_geom"), col(T,"total_score")),
         ("asimetria vs asymScore", col(O,"asimetria"), col(T,"asymScore")),
         ("gc_9_14 vs anti_9_14_GC", col(O,"gc_9_14"), col(T,"anti_9_14_GC")),
         ("a_en_10 vs anti_10th_A", col(O,"a_en_10"), col(T,"anti_10th_A")),
         ("gc vs anti_GC", col(O,"gc"), col(T,"anti_GC")),
         ("accesibilidad (u=8) vs accesibilidad dsRIP (u=16 prom)", col(O,"accesibilidad"), col(T,"accessibility"))]
for n,a,b in pairs:
    r,p = stats.spearmanr(a,b); print(f"  Spearman {n}: {r:.3f}")
# solo ventanas vivas (sin descarte nuestro)
viv = [i for i,(o,t) in enumerate(rows) if not o["descarte"]]
print("vivas nuestras", len(viv))
a = np.array([float(rows[i][0]["score"]) for i in viv]); b = np.array([float(rows[i][1]["total_score"]) for i in viv])
print("  Spearman score vs dsRIP (solo vivas):", round(stats.spearmanr(a,b)[0],3))
a2 = np.array([float(rows[i][0]["score_geom"]) for i in viv])
print("  Spearman score_geom vs dsRIP (solo vivas):", round(stats.spearmanr(a2,b)[0],3))
# top-N
def topn(keyf, n, idx=None):
    idx = range(len(rows)) if idx is None else idx
    return set(sorted(idx, key=lambda i: -keyf(rows[i]))[:n])
for n in (10, 25, 50, 90):
    to = topn(lambda r: float(r[0]["score"]), n); td = topn(lambda r: float(r[1]["total_score"]), n)
    tg = topn(lambda r: float(r[0]["score_geom"]), n)
    print(f"top-{n}: nuestro(suma) vs dsRIP comparten {len(to&td)}; nuestro(geom) vs dsRIP {len(tg&td)}; esperado al azar {n*n/len(rows):.1f}")
# ventana 300 pb
def best_window(vals, w=280):  # 300 pb de sitio => 280 siRNAs de 21 nt
    v = np.array(vals); cs = np.concatenate([[0], np.cumsum(v)])
    m = (cs[w:] - cs[:-w]) / w
    return int(m.argmax()) + 1, float(m.max())
for lab, vals in (("nuestro suma", [float(r[0]["score"]) for r in rows]), ("nuestro geom", [float(r[0]["score_geom"]) for r in rows]), ("dsRIP", [float(r[1]["total_score"]) for r in rows])):
    p, m = best_window(vals); print(f"mejor region de 300 pb ({lab}): inicio {p}-{p+299}, media {m:.3f}")
print("top-10 dsRIP:")
for i in sorted(range(len(rows)), key=lambda i: -float(rows[i][1]["total_score"]))[:10]:
    o,t = rows[i]; print("  pos", o["pos"], "dsRIP", t["total_score"], "asym", t["asymScore"], "A10", t["anti_10th_A"], "gc914", t["anti_9_14_GC"], "| nuestro score", o["score"], "descarte", o["descarte"], "rank nuestro", 1+sum(1 for r in rows if float(r[0]["score"])>float(o["score"])))
print("top-10 nuestro:")
for i in sorted(range(len(rows)), key=lambda i: -float(rows[i][0]["score"]))[:10]:
    o,t = rows[i]; print("  pos", o["pos"], "nuestro", o["score"], "asim", o["asimetria"], "A10", o["a_en_10"], "gc914", o["gc_9_14"], "| dsRIP", t["total_score"], "rank dsRIP", 1+sum(1 for r in rows if float(r[1]["total_score"])>float(t["total_score"])))
# estructura de empates dsRIP
vals = [float(r[1]["total_score"]) for r in rows]
print("dsRIP valores distintos:", len(set(vals)), "min", min(vals), "max", max(vals))
