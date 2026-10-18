#!/usr/bin/env python3
"""
PRB — Relación entre knockdown medido (qPCR) y fenotipo (mortalidad / hazard ratio) en hemípteros,
con las cifras TRANSCRIPTAS A MANO del texto de cada artículo abierto (ver fuentes en PRB_fuentes.json).
n minúsculo en todos los casos: los coeficientes son descriptivos, NO inferencia; se calculan solo para
mostrar si el orden del knockdown ordena el orden del fenotipo. Solo numpy y scipy.

Casos:
 A) Delottococcus aberiae (Hemiptera, Pseudococcidae), microinyección, 6 genes. PRB-35 (Gallego-Giraldo et al. 2026).
    knockdown = log2FC principal (efecto medio dias 3-6); fenotipo = hazard ratio de Cox frente a control sin dsRNA.
    Kr-h1: knockdown <5 % y no significativo, y sin embargo el peor fenotipo (HR 5,4; mortalidad total a día 18).
 B) D. aberiae, vía oral, 4 genes (mismo artículo): % de reducción de expresión a día 6 y HR.
 C) Bemisia tabaci (Hemiptera, Aleyrodidae), oral, 4 genes de intestino con cifras numéricas explícitas en el texto
    a día 6: % de reducción de expresión y % mortalidad (control buffer/dsGFP: 28 %). PRB-22 (Vyas et al. 2017).
 D) Diaphorina citri adultos, dieta, dosis 200/500/1000 ng/uL: expresión relativa (%) vs mortalidad a 120 h.
    PRB-16 (Galdeano et al. 2017). Catepsina D: expresión relativa 46/52/64 %; mortalidad 28/47/52 %.
"""
import numpy as np
from scipy import stats

def sp(x, y, label):
    r, p = stats.spearmanr(x, y)
    print(f"{label}: n={len(x)}, Spearman={r:+.2f} (P nominal={p:.2f}; descriptivo)")
    return r

print("A) Delottococcus aberiae, inyección: |log2FC| de knockdown vs HR")
genes = ["RPSL13", "ANT", "ATPsyn-b", "V-ATPase A", "Actin-a", "Kr-h1"]
log2fc = np.array([-3.98, -1.36, -1.61, -1.57, -0.549, -0.517])
hr = np.array([2.5, 2.3, 3.8, 2.2, 1.8, 5.4])
for g, l, h in zip(genes, log2fc, hr):
    print(f"   {g:11s} log2FC={l:+.2f}  HR={h}")
sp(-log2fc, hr, "   todos los genes")
m = np.array([g != "Kr-h1" for g in genes])
sp(-log2fc[m], hr[m], "   sin Kr-h1 (5 genes con knockdown significativo o claro)")

print("\nB) D. aberiae, vía oral (día 6): % de reducción vs HR")
genes_b = ["Actin-a", "V-ATPase A", "ATPsyn-b", "RPSL13"]
kd_b = np.array([53.88, 66.9, 34.63, 22.85]); hr_b = np.array([1.50, 1.9, 1.60, 1.2])
l2_b = np.array([-1.77, -1.53, -1.45, -0.568])
sp(kd_b, hr_b, "   4 genes orales, con el '% de reducción' entre paréntesis del texto")
sp(-l2_b, hr_b, "   4 genes orales, con el log2FC del texto")
print("   NOTA: en el texto del artículo el % entre paréntesis no coincide con el log2FC (p. ej. log2FC -1,45 equivale a ~63 % de reducción,")
print("   y el texto dice 34,63 %): la cifra de knockdown oral de este artículo es internamente inconsistente [?]; el coeficiente varía de +0,4 a +0,8 según la métrica.")

print("\nC) Bemisia tabaci, oral, día 6: % de reducción de expresión vs % mortalidad")
genes_c = ["AChRa", "AGLU1", "AQP1", "Hsp70"]
kd_c = np.array([50, 80, 70, 50]); mort_c = np.array([45, 92, 84, 35])
sp(kd_c, mort_c, "   4 genes (los otros 2 del estudio no tienen cifra individual en el texto)")

print("\nD) Diaphorina citri, catepsina D, dosis 200/500/1000 ng/uL")
dose = np.array([200, 500, 1000]); expr = np.array([46, 52, 64]); mort = np.array([28, 47, 52])
print("   expresión relativa sube con la dosis (menos knockdown), mortalidad también sube")
sp(dose, mort, "   dosis vs mortalidad")
sp(-expr, mort, "   knockdown (=-expresión relativa) vs mortalidad")
print("   (3 puntos. AMBIGÜEDAD: el texto dice que la expresión 'fue reducida a 46, 52 y 64 %'; se interpreta como nivel remanente.")
print("    El caso inequívoco es quitina sintasa: 'reducciones de ARNm de 76, 66 y 48 %' a 200/500/1000 ng/uL (menos knockdown con más dosis),")
print("    con mortalidad a 120 h de 41 % (500) y 49 % (1000) (la de 200 ng/uL no figura en el texto). Los autores dicen que no hubo correlación entre dosis y reducción de ARNm.)")
