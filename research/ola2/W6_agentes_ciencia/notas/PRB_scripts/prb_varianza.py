#!/usr/bin/env python3
"""
PRB — Partición de varianza gen vs secuencia con datos abiertos (CC BY 4.0), solo numpy/pandas/scipy.

Fuente 1: Cedden et al. 2025, BMC Biology 23:114, material suplementario Additional file 3, Tabla S1
          (28 dsRNA largos contra 8 genes esenciales de Tribolium castaneum; hazard ratio (HR) frente a dsmGFP,
          n = 25 larvas por dsRNA según el texto principal; inyección). Archivo: cedden2025_tablaS1.csv
Fuente 2: Knorr et al. 2018, Sci Rep 8:2061, Tabla 1 (50 genes preseleccionados: mortalidad en T. castaneum
          por inyección de 250 ng/µL a 14 d y mortalidad en Diabrotica virgifera virgifera por dieta). Archivo: knorr2018_tabla1.csv

Advertencias: (i) los 8 genes de Cedden fueron elegidos entre los mejores blancos del cribado genómico: el rango de
varianza entre genes está RESTRINGIDO; no representa la varianza entre genes esenciales y no esenciales.
(ii) n = 28 con 8 genes: R2 ajustado es la cifra a mirar. (iii) Es un cálculo propio sobre datos publicados, no un
resultado de los autores. (iv) El modelo completo reproduce el R múltiple 0,79 (gl residuales = 17) que reportan los autores.
"""
import numpy as np, pandas as pd, scipy.stats as st, os
here = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(here, "cedden2025_tablaS1.csv"))
y = df.hr.values; n = len(y)
G = pd.get_dummies(df.gene, drop_first=True).values.astype(float)
s = df.sirna.values[:, None]; a = df.access.values[:, None]; reg = (df.region == "ORF").values.astype(float)[:, None]

def ols_r2(X, y):
    X = np.column_stack([np.ones(len(y)), X]); b, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ b; return 1 - (res ** 2).sum() / ((y - y.mean()) ** 2).sum(), X.shape[1] - 1
def adj(r2, k): return 1 - (1 - r2) * (n - 1) / (n - k - 1)

lines = []
P = lines.append
P("== Cedden 2025, Tabla S1: n=%d dsRNA, %d genes ==" % (n, df.gene.nunique()))
r2f, kf = ols_r2(np.hstack([s, a, reg, G]), y)
P(f"Modelo completo (score siRNA + accesibilidad + región + gen): R2={r2f:.3f}, R múltiple={np.sqrt(r2f):.3f}, gl residuales={n-kf-1}  (autores: R=0,79, gl=17)")
for name, X in [("solo gen", G), ("solo score siRNA", s), ("gen + score", np.hstack([G, s])), ("score + accesibilidad + región (sin gen)", np.hstack([s, a, reg]))]:
    r2, k = ols_r2(X, y); P(f"{name:42s} R2={r2:.3f}  R2 ajustado={adj(r2,k):.3f}")
sst = ((y - y.mean()) ** 2).sum()
r2full, kfull = ols_r2(np.hstack([s, a, reg, G]), y)
P("Contribución única (caída de R2 al quitar el término del modelo completo):")
for name, X in [("gen", np.hstack([s, a, reg])), ("score siRNA", np.hstack([a, reg, G])), ("región ORF/UTR", np.hstack([s, a, G])), ("accesibilidad", np.hstack([s, reg, G]))]:
    r2, k = ols_r2(X, y); P(f"  quitar {name:15s}: caída de R2 = {r2full - r2:.3f}")
P("Spearman score siRNA vs HR (todas): rho=%.3f, P=%.3f" % st.spearmanr(df.sirna, df.hr))
o = df[df.region == "ORF"]
P("Spearman score siRNA vs HR (solo ORF, n=%d): rho=%.3f, P=%.3f" % ((len(o),) + tuple(st.spearmanr(o.sirna, o.hr))))
dc = df.copy(); dc["s_c"] = dc.sirna - dc.groupby("gene").sirna.transform("mean"); dc["y_c"] = dc.hr - dc.groupby("gene").hr.transform("mean")
P("Intra-gen (centrado por gen): Pearson=%.3f (P=%.3f), Spearman=%.3f (P=%.3f)" % (st.pearsonr(dc.s_c, dc.y_c) + st.spearmanr(dc.s_c, dc.y_c)))
P("HR medio por gen: " + "; ".join(f"{g}={v:.1f}" for g, v in df.groupby('gene').hr.mean().items()))
P("Rango de HR dentro de gen (máx/mín): " + "; ".join(f"{g}={v:.1f}x" for g, v in (df.groupby('gene').hr.max() / df.groupby('gene').hr.min()).items()))

kn = pd.read_csv(os.path.join(here, "knorr2018_tabla1.csv"))
P("")
P("== Knorr 2018, Tabla 1: %d genes preseleccionados por letalidad en T. castaneum ==" % len(kn))
P("Genes con mortalidad significativa en Diabrotica (asterisco): %d de %d" % (kn.sig.sum(), len(kn)))
P("Spearman mortalidad Tribolium (250 ng/uL, 14 d) vs mortalidad Diabrotica (dieta): rho=%.3f, P=%.4f" % st.spearmanr(kn.tc_m, kn.dvv_m))
P("Mortalidad en Tribolium: min=%.1f, mediana=%.1f, genes en 100%%=%d (techo: rango restringido)" % (kn.tc_m.min(), kn.tc_m.median(), (kn.tc_m >= 100).sum()))
txt = "\n".join(lines); print(txt)
open(os.path.join(here, "prb_varianza_salida.txt"), "w").write(txt + "\n")
