"""
Cálculos derivados de M1 (R7). Entradas transcritas a mano desde las fuentes abiertas indicadas (id de sources.json);
nada se descargó ni se imputó. Salida impresa: ver calculos_salida.txt. Python 3, numpy y scipy.
"""
import math, numpy as np
from scipy import stats

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return round(100 * (c - h) / d, 1), round(100 * (c + h) / d, 1)

print("== A. JAXA PCG#1-5 (M1-02, Tablas 1 y 2 del XML de Europe PMC)")
for name, (k, n) in {
    "proteínas con prueba de aceptación buena 61/215": (61, 215),
    "muestras lanzadas 144/215 (44+41+59)": (144, 215),
    "buen resultado sobre proteínas 40/215 (tabla: 19 %)": (40, 215),
    "buen resultado sobre muestras lanzadas 40/144": (40, 144),
    "buen resultado 22/44 (aceptación buena, optimizada)": (22, 44),
    "buen resultado 15/41 (purificación adicional)": (15, 41),
    "buen resultado 3/59 (sin purificación adicional)": (3, 59),
    "D/beta < 1 mm: 7/10": (7, 10), "D/beta 1-3: 9/13": (9, 13), "D/beta 3-10: 7/14": (7, 14), "D/beta > 10: 11/27": (11, 27),
    "D/beta < 3 agrupado 16/23": (16, 23), "D/beta >= 3 agrupado 18/41": (18, 41)}.items():
    print(f"  {name}: {100*k/n:.1f} %  IC95 Wilson {wilson(k, n)}")
print("  Fisher D/beta<3 (16/23) vs >=3 (18/41), dos colas:", stats.fisher_exact([[16, 7], [18, 23]])[1].round(3))
print("  suma de 'buen resultado' por rama:", 22 + 15 + 3, "; lanzadas:", 44 + 41 + 59)

print("\n== B. H-PGDS (M1-16, Tabla 2): pares con resolución de conjunto de datos en ambos brazos")
pares = {"S1/G1": (1.10, 1.80), "S4/G4": (1.90, 2.00), "S5/G5": (1.30, 1.50), "S6/G6": (1.50, 1.75),
         "S8/G8": (1.30, 2.50), "S14/G14": (1.68, 1.70), "S23/G23": (1.50, 1.50)}
d = np.array([g - s for s, g in pares.values()])
print("  Delta (tierra - espacio) en A:", dict(zip(pares, d.round(2))))
print("  n =", len(d), " mediana =", round(float(np.median(d)), 2), " media =", round(float(d.mean()), 2))
print("  Wilcoxon una cola (cero descartado):", stats.wilcoxon(d, alternative="greater").pvalue.round(4), "(n efectivo 6; solo orientativo)")
print("  condiciones lanzadas 25; pares válidos 12 (texto del artículo); 12/25 =", round(100 * 12 / 25), "%")

print("\n== C. PfGST (M1-04, Tablas 1 y 2; rango de resolución y mosaicidad por conjunto de datos, n = 3 por celda)")
res = {"0 %": ([3.42, 3.14, 3.19], [2.12, 3.24, 2.30]), "0,2 %": ([2.63, 3.14, 3.10], [3.00, 2.82, 2.76]),
       "1 %": ([3.53, 3.59, 2.73], [3.27, 3.62, 3.09]), "5 %": ([3.48, 3.08, 3.23], [2.74, 3.17, 2.41])}
mos = {"0 %": ([0.14, 0.34, 0.27], [0.12, 0.11, 0.12]), "0,2 %": ([0.12, 0.12, 0.07], [0.34, 0.15, 0.23]),
       "1 %": ([0.37, 0.44, 0.51], [0.77, 0.61, 0.25]), "5 %": ([0.48, 0.52, 0.73], [0.25, 0.65, 0.15])}
G, M, gm, mm = [], [], [], []
for c in res:
    g, m = res[c]; G += g; M += m
    g2, m2 = mos[c]; gm += g2; mm += m2
    print(f"  tetrámero {c}: resolución tierra {np.mean(g):.2f} vs MG {np.mean(m):.2f} (delta {np.mean(g)-np.mean(m):+.2f} A); "
          f"mosaicidad tierra {np.mean(g2):.3f} vs MG {np.mean(m2):.3f}")
print(f"  agrupado 12 vs 12: resolución {np.mean(G):.2f} vs {np.mean(M):.2f} (delta {np.mean(G)-np.mean(M):+.2f} A), Mann-Whitney p = {stats.mannwhitneyu(G, M).pvalue:.3f}")
print(f"  agrupado 12 vs 12: mosaicidad {np.mean(gm):.3f} vs {np.mean(mm):.3f}, Mann-Whitney p = {stats.mannwhitneyu(gm, mm).pvalue:.3f}")

print("\n== D. CrystalCards (M1-19, resumen): tarjetas con cristales")
print("  16/25 vs 12/25; Fisher dos colas p =", stats.fisher_exact([[16, 9], [12, 13]])[1].round(3))

print("\n== E. Diferencias de resolución de los pares restantes (Å, tierra - espacio; positivo = espacio mejor)")
otros = {"L-PGDS PEG 8000 (M1-17)": 1.30 - 1.06, "Heterodúplex condición 1 (M1-12)": 1.5 - 1.6, "Heterodúplex condición 2 (M1-12)": 1.6 - 1.4,
         "HEWL bioensamblador, mejores conjuntos (M1-13)": 0.80 - 1.09, "Lipasa SAL-penfluridol (M1-14)": 2.23 - 2.57,
         "Lipasa T1, cifras citadas (M1-18)": 1.3 - 1.1, "Neutrones TS 0,2 mm3, integrado a (M1-06)": 4.0 - 3.2}
for k, v in otros.items(): print(f"  {k}: {v:+.2f}")

print("\n== F. Órdenes de magnitud físicos (supuestos explícitos; cálculo propio [H], no es una fuente)")
kB, T0, NA, g0 = 1.380649e-23, 293.0, 6.02214076e23, 9.80665
for nombre, M_ in [("lisozima, 14,3 kDa (supuesto)", 14300), ("proteína de 50 kDa (supuesto)", 50000)]:
    m = M_ / 1000 / NA
    print(f"  {nombre}: m g h / kT con h = 10 nm -> {m*g0*10e-9/(kB*T0):.1e}")
r_, drho, eta = 50e-6, 100.0, 1e-3
v = 2 * drho * g0 * r_**2 / (9 * eta)
print(f"  Stokes, r = 50 um, delta rho = 100 kg/m3, eta = 1 mPa s: v = {v*1e6:.0f} um/s")
D = 1.1e-10
print(f"  longitud difusiva sqrt(2 D t), D = 1,1e-10 m2/s (orden típico supuesto): 1 h -> {math.sqrt(2*D*3600)*1e3:.2f} mm; 24 h -> {math.sqrt(2*D*86400)*1e3:.2f} mm")
