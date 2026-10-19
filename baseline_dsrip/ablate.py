import csv
import numpy as np
from scipy import stats
S = r"C:\Users\Luca\AppData\Local\Temp\claude\C--Proyectos-yHat\9bf9b77a-cd77-4b98-b86b-847bff6ee6a8\scratchpad"
ours = list(csv.DictReader(open(r"C:\Proyectos\yHat\pipeline\salida\sirna_vatpaseA.csv")))
th = {r["antisense_5_3_DNA"]: r for r in csv.DictReader(open(S + r"\dsrip_vatpaseA.csv"))}
T = [th[o["guia"]] for o in ours]
n = len(ours)
f = lambda rows, k: np.array([float(r[k]) for r in rows])
def norm(v):
    lo, hi = v.min(), v.max(); return np.full_like(v, .5) if hi == lo else (v - lo) / (hi - lo)
dr = f(T, "total_score")
asim, g914, acc, dgc, a10 = f(ours,"asimetria"), f(ours,"gc_9_14"), f(ours,"accesibilidad"), f(ours,"desea_gc"), f(ours,"a_en_10")
alive = np.array([o["descarte"] == "" for o in ours])
N = lambda v: norm(v[alive])
def score(w, asv=asim, sf=None, wsf=0):
    d = {"asim": np.zeros(n), "g914": np.zeros(n), "acc": np.zeros(n)}
    d["asim"][alive] = N(asv); d["g914"][alive] = N(g914); d["acc"][alive] = N(acc)
    s = w["asim"]*d["asim"] + w["g914"]*d["g914"] + w["acc"]*d["acc"] + w["gc"]*dgc + w["a10"]*a10
    if sf is not None:
        sfn = np.zeros(n); sfn[alive] = N(sf); s = s + wsf*sfn
    return s
W = {"asim": .35, "g914": .2, "acc": .2, "gc": .15, "a10": .1}
rho = lambda s, m=alive: stats.spearmanr(s[m], dr[m])[0]
print("V0 original                                  ", round(rho(score(W)),3))
W1 = dict(W, acc=0.0); print("V1 acc peso 0                                ", round(rho(score(W1)),3))
asd = f(T, "asymScore")
print("V2 V1 + asimetria de dsRIP                   ", round(rho(score(W1, asv=asd)),3))
sfe = -f(T, "self_fold_energy")*-1  # energia (negativa); mas negativo = peor plegado
sf = f(T, "self_fold_energy")  # mayor (menos negativo) = menos plegado = mejor
print("V3 V2 + autoplegamiento (peso 0.21)           ", round(rho(score(W1, asv=asd, sf=sf, wsf=0.21)),3))
W4 = {"asim": .0, "g914": .0, "acc": 0, "gc": 0, "a10": 0}
print("solo asimetria nuestra                        ", round(rho(score(W4, ) + N_ if False else norm_ if False else np.where(alive, asim, asim.min())),3))
print("solo asimetria dsRIP                          ", round(rho(asd),3))
print("solo autoplegamiento                          ", round(rho(sf),3))
print("asim nuestra vs asim dsRIP                    ", round(stats.spearmanr(asim, asd)[0],3))
print("autoplegamiento vs dsRIP total                ", round(stats.spearmanr(sf, dr)[0],3))
# componentes de dsRIP: aporte a la varianza
asn = f(T,"asymScore_normalized"); sfn = f(T,"self_fold_energy_normalized")
print("dsRIP: corr total vs asym_norm", round(stats.spearmanr(dr, asn)[0],3), " vs selffold_norm", round(stats.spearmanr(dr, sfn)[0],3), " vs A10", round(stats.spearmanr(dr, a10)[0],3))
print("edge_asyym valores:", {k:int((f(T,'edge_asyym')==k).sum()) for k in (0,1,2)})
# regiones
def best(vals, w=281):
    cs = np.concatenate([[0], np.cumsum(vals)]); m = (cs[w:] - cs[:-w]) / w; i = int(m.argmax()); return i + 1, i + w, m[i], m
oursuma = f(ours, "score"); ourgeom = f(ours, "score_geom")
rd = best(dr); ro = best(oursuma); rg = best(ourgeom)
ov = lambda a, b: max(0, min(a[1], b[1]) - max(a[0], b[0]) + 1)
print("region dsRIP  :", rd[:2], round(rd[2],2))
print("region nuestra suma:", ro[:2], "solape con dsRIP", ov(rd, ro), "de 281 siRNAs")
print("region nuestra geom:", rg[:2], "solape con dsRIP", ov(rd, rg))
# evaluacion cruzada, en percentil: cuanto vale la region del otro bajo mi metrica
def pct(mm, i): return float((mm < mm[i-1]).mean())
print("score dsRIP medio en region dsRIP", round(rd[2],2), "| en region nuestra", round(rd[3][ro[0]-1],2), "| media del gen", round(dr.mean(),2), "| min ventana", round(rd[3].min(),2))
print("score nuestro medio en region nuestra", round(ro[2],4), "| en region dsRIP", round(ro[3][rd[0]-1],4), "| media del gen", round(oursuma.mean(),4), "| min", round(ro[3].min(),4))
print("sd de medias de ventana dsRIP", round(rd[3].std(),2), "| rango", round(rd[3].min(),1), round(rd[3].max(),1))
