#!/usr/bin/env python3
"""
PRB — Potencia de un chequeo a ciegas con n genes (n = 5..10 y referencias mayores).

Pregunta: si calculamos un proxy computacional para n genes con desenlace medido
retrospectivamente (p. ej. genes de D. maidis con RNAi publicado) y correlacionamos
proxy vs desenlace, ¿qué tan bien distinguimos una correlación verdadera rho = 0,3 / 0,5 / 0,7
de rho = 0 (proxy inútil)?

Supuestos (todos explícitos, ninguno verificado con datos de D. maidis):
 S1. Los n pares (proxy, desenlace) son independientes e idénticamente distribuidos con
     distribución normal bivariada de correlación verdadera rho (caso favorable: sin ruido de
     laboratorio entre estudios, sin dosis/vía/estadio heterogéneos).
 S2. Estadístico: correlación de Spearman (rango), que es lo que corresponde a un 'ranking'.
 S3. Fisher z con varianza de Fieller para Spearman: Var(z) = 1,06/(n-3). Para Pearson: 1/(n-3).
 S4. Para n pequeño (<=10) la aproximación de Fisher es mala; por eso la potencia se calcula
     también por simulación, con valor crítico exacto aproximado por 200.000 permutaciones nulas.
 S5. Atenuación por error de medición del desenlace: rho_obs = rho_verdadera * sqrt(fiabilidad).
     La fiabilidad de un desenlace de bioensayo entre laboratorios es desconocida: se muestran
     0,5 y 0,8 como escenarios ilustrativos, no como estimaciones.
Se usa solo numpy y scipy.
"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(20261018)

def fisher_ci(r, n, alpha=0.05, spearman=True, k_controlled=0):
    """IC de Fisher para una correlación observada r con n pares; k_controlled variables parciales."""
    z = np.arctanh(r)
    var = (1.06 if spearman else 1.0) / (n - k_controlled - 3)
    se = np.sqrt(var)
    zc = stats.norm.ppf(1 - alpha / 2)
    return np.tanh(z - zc * se), np.tanh(z + zc * se)

def power_fisher(rho, n, alpha=0.05, spearman=True, two_sided=True):
    var = (1.06 if spearman else 1.0) / (n - 3)
    se = np.sqrt(var)
    zc = stats.norm.ppf(1 - alpha / (2 if two_sided else 1))
    mu = np.arctanh(rho) / se
    return stats.norm.cdf(mu - zc) + (stats.norm.cdf(-mu - zc) if two_sided else 0)

def n_for_power(rho, power=0.8, alpha=0.05, spearman=True):
    for n in range(4, 2000):
        if power_fisher(rho, n, alpha, spearman) >= power:
            return n
    return None

def spearman_crit_perm(n, alpha=0.05, nperm=200_000):
    """Valor crítico bilateral de |rho_s|: el menor c tal que P0(|rho_s| >= c) <= alpha.
    Distribución nula EXACTA por enumeración de las n! permutaciones para n <= 10;
    por 200.000 permutaciones aleatorias para n mayor. (Una versión previa de este script usaba el
    cuantil 95 % de |rho|, que con valores discretos es anticonservador: se corrigió.)"""
    import itertools
    x = np.arange(n)
    if n <= 10:
        perms = np.fromiter(itertools.chain.from_iterable(itertools.permutations(range(n))), dtype=np.int8,
                            count=int(np.prod(np.arange(1, n + 1))) * n).reshape(-1, n)
        d2 = ((perms.astype(np.int32) - x) ** 2).sum(axis=1)
        rs = 1 - 6 * d2 / (n * (n**2 - 1))
    else:
        rs = np.empty(nperm)
        for i in range(nperm):
            y = rng.permutation(n)
            rs[i] = 1 - 6 * np.sum((x - y) ** 2) / (n * (n**2 - 1))
    a = np.abs(rs)
    vals = np.unique(np.round(a, 12))
    crit = np.inf
    for c in vals:  # ascendente
        if np.mean(a >= c - 1e-12) <= alpha:
            crit = c
            break
    return crit, rs

def power_sim(rho, n, crit, reps=20_000, reliab=1.0):
    rho_eff = rho * np.sqrt(reliab)
    cov = np.array([[1, rho_eff], [rho_eff, 1]])
    L = np.linalg.cholesky(cov)
    hit = 0
    rs_all = np.empty(reps)
    for i in range(reps):
        z = rng.standard_normal((n, 2)) @ L.T
        r = stats.spearmanr(z[:, 0], z[:, 1])[0]
        rs_all[i] = r
        if abs(r) >= crit - 1e-12:
            hit += 1
    return hit / reps, rs_all


def enrichment_section(P):
    """Prueba de enriquecimiento con clase ÚNICA (solo genes con RNAi publicado exitoso; no hay negativos publicados).
    H0: el proxy no ordena; cada gen cae por encima de la mediana del fondo con prob 0,5.
    H1: el proxy tiene AUC = a; con normales de igual varianza, P(positivo > mediana del fondo) = Phi(d'), d' = sqrt(2)*Phi^-1(a).
    Prueba exacta binomial unilateral alfa=0,05 sobre k de n genes por encima de la mediana del fondo."""
    P("")
    P("== 7. Prueba de enriquecimiento con clase única (sin negativos): potencia según n y AUC verdadera del proxy ==")
    P("n   | k mínimo (P0<=0,05) | P0 exacta | potencia con AUC=0,6 | 0,7 | 0,8 | 0,9")
    for n in [5, 6, 7, 8, 10, 15]:
        kmin = next(k for k in range(n + 1) if stats.binom.sf(k - 1, n, 0.5) <= 0.05)
        p0 = stats.binom.sf(kmin - 1, n, 0.5)
        cells = []
        for a in [0.6, 0.7, 0.8, 0.9]:
            dprime = np.sqrt(2) * stats.norm.ppf(a)
            pi = stats.norm.cdf(dprime)
            cells.append(f"{stats.binom.sf(kmin - 1, n, pi):.2f}")
        P(f"{n:<3} | {kmin:<19} | {p0:.3f}     | " + " | ".join(cells))
    P("(Advertencia de circularidad: los genes de D. maidis con RNAi publicado (BicC, V-ATPasa B/D, burs-a, eth) fueron elegidos por los autores a partir")
    P(" de conocimiento previo de esencialidad en otros insectos; un proxy basado en ortología de genes esenciales los 'predeciría' por construcción.)")

def main():
    out = []
    P = out.append
    ns = [5, 6, 7, 8, 9, 10, 15, 20, 28]
    rhos = [0.3, 0.5, 0.7]
    P("== 1. IC de Fisher (95 %) para una r de Spearman observada igual a rho (caso típico) ==")
    P("n   | " + " | ".join(f"rho={r}: IC95 (¿excluye 0?)" for r in rhos))
    for n in ns:
        cells = []
        for r in rhos:
            lo, hi = fisher_ci(r, n)
            cells.append(f"[{lo:+.2f}, {hi:+.2f}] ({'sí' if lo > 0 else 'no'})")
        P(f"{n:<3} | " + " | ".join(cells))
    P("")
    P("== 2. Potencia para rechazar rho=0 (bilateral, alfa=0,05): Fisher-Fieller vs simulación con valor crítico por permutación ==")
    P("n   | crit|rho_s| (perm) | " + " | ".join(f"rho={r}: Fisher / sim" for r in rhos))
    crits = {}
    for n in [5, 6, 7, 8, 9, 10, 15, 20, 28]:
        crit, _ = spearman_crit_perm(n)
        crits[n] = crit
        cells = []
        for r in rhos:
            pf = power_fisher(r, n)
            ps, _ = power_sim(r, n, crit)
            cells.append(f"{pf:.2f} / {ps:.2f}")
        P(f"{n:<3} | {crit:.3f}               | " + " | ".join(cells))
    P("(valor crítico = menor |rho_s| con P nula exacta <= 0,05 bilateral; para n=5 ningún |rho_s|<1 alcanza ese nivel y n=5 con rho_s=1 tiene P=2/120=0,017)")
    P("")
    P("== 3. n necesario para 80 % de potencia (Fisher-Fieller, bilateral, alfa=0,05) ==")
    for r in rhos:
        P(f"rho={r}: n = {n_for_power(r)}  (Pearson, sin Fieller: n = {n_for_power(r, spearman=False)})")
    P("")
    P("== 4. Atenuación por error de medición del desenlace (potencia simulada, n=10, valor crítico de n=10) ==")
    for rel in [1.0, 0.8, 0.5]:
        cells = []
        for r in rhos:
            ps, _ = power_sim(r, 10, crits[10], reliab=rel)
            cells.append(f"rho={r}: {ps:.2f} (rho_obs esperado {r*np.sqrt(rel):.2f})")
        P(f"fiabilidad={rel}: " + " | ".join(cells))
    P("")
    P("== 5. Discriminar entre dos proxies con n genes (diferencia entre correlaciones dependientes, aproximación independiente, SE de la diferencia de z) ==")
    for n in [5, 8, 10, 15, 20, 28]:
        se = np.sqrt(2 * 1.06 / (n - 3))
        # potencia para distinguir rho=0,7 de rho=0,3 (bilateral 0,05)
        d = abs(np.arctanh(0.7) - np.arctanh(0.3))
        pw = stats.norm.cdf(d / se - stats.norm.ppf(0.975)) + stats.norm.cdf(-d / se - stats.norm.ppf(0.975))
        P(f"n={n}: potencia para distinguir rho=0,7 de rho=0,3 = {pw:.2f}")
    P("")
    P("== 6. Aplicación a datos reales ya abiertos (Cedden et al. 2025, Tabla S1; 28 dsRNA, 8 genes, T. castaneum) ==")
    # valores calculados en el análisis de PRB (ver notas): Spearman score~HR = 0,43 (n=28); intra-gen Pearson 0,415 (n=28, 7 gl absorbidos)
    for label, r, n, k, sp in [("Spearman score siRNA vs HR, n=28", 0.4296, 28, 0, True),
                               ("Correlación intra-gen (Pearson, gen controlado)", 0.4152, 28, 7, False),
                               ("Spearman Tribolium vs Diabrotica (Knorr 2018, 50 genes preseleccionados)", 0.4282, 50, 0, True)]:
        lo, hi = fisher_ci(r, n, spearman=sp, k_controlled=k)
        P(f"{label}: r={r:.3f}  IC95 Fisher [{lo:+.2f}, {hi:+.2f}]")
    enrichment_section(P)
    txt = "\n".join(out)
    print(txt)
    return txt

if __name__ == "__main__":
    txt = main()
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "prb_potencia_salida.txt"), "w") as f:
        f.write(txt + "\n")
