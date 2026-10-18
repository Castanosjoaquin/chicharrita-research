"""ANA — regla cuantitativa de proxy imperfecto (script de apoyo, sin datos del proyecto).
Modelos: (1) normal bivariado proxy/verdad con correlacion rho (regresion a la media);
(2) binormal para clasificacion binaria con prevalencia b y AUC dado (enriquecimiento);
(3) KL de best-of-n (Gao et al. 2022): KL = ln n - (n-1)/n; (4) potencia/IC de un rho estimado con n pequeno.
Semilla fija. Todo lo que imprime es calculo propio [H], no dato de fuente."""
import numpy as np
from scipy.stats import norm, rankdata
from scipy.optimize import brentq
rng = np.random.default_rng(20261018)

def sim_pool(N, rho, reps=20000):
    """Devuelve, por replica: z verdadero del top-1 por proxy, percentil verdadero del top-1,
    P(top-1 verdadero in top-k proxy) para k=1,3,5,10 y z verdadero del mejor-de-k por ensayo."""
    x = rng.standard_normal((reps, N))                    # verdad (z)
    e = rng.standard_normal((reps, N))
    p = rho * x + np.sqrt(1 - rho**2) * e                 # proxy
    order = np.argsort(-p, axis=1)                        # indices por proxy desc
    top1 = order[:, 0]
    zt = np.take_along_axis(x, top1[:, None], 1)[:, 0]
    pct = (x < zt[:, None]).sum(1) / (N - 1)              # percentil verdadero del top-1 proxy
    best_true = np.argmax(x, axis=1)
    rank_of_best = np.argmax(order == best_true[:, None], axis=1) + 1   # rango proxy del mejor verdadero
    out = {"E_z_top1": zt.mean(), "E_pct_top1": pct.mean()}
    for k in (1, 3, 5, 10):
        if k <= N:
            out[f"P_best_in_top{k}"] = (rank_of_best <= k).mean()
            zk = np.take_along_axis(x, order[:, :k], 1).max(1)  # mejor verdadero entre los k ensayados
            out[f"E_z_bestofk_assayed{k}"] = zk.mean()
    return out

def hit_at_least_one_true_topq(N, rho, k, q, reps=40000):
    """P(al menos 1 de los k mejores por proxy esta entre los q mejores verdaderos)."""
    x = rng.standard_normal((reps, N)); e = rng.standard_normal((reps, N))
    p = rho * x + np.sqrt(1 - rho**2) * e
    kp = np.argsort(-p, 1)[:, :k]; kt = np.argsort(-x, 1)[:, :q]
    hit = np.array([len(set(a) & set(b)) > 0 for a, b in zip(kp, kt)])
    return hit.mean()

def binormal_precision(b, auc, f):
    """Precision al testear la fraccion f superior del pool, binormal de varianzas iguales."""
    d = np.sqrt(2) * norm.ppf(auc)
    g = lambda t: b * norm.sf(t - d) + (1 - b) * norm.sf(t) - f
    t = brentq(g, -10, 15)
    tp = b * norm.sf(t - d)
    return tp / f, tp / b       # precision, recall

def kl_bon(n): return np.log(n) - (n - 1) / n

def power_corr(n, rho, alpha=0.05):
    z = np.arctanh(rho) * np.sqrt(n - 3)
    return norm.sf(norm.isf(alpha / 2) - z) + norm.cdf(-norm.isf(alpha / 2) - z)

def n_for_power(rho, power=0.8, alpha=0.05):
    return int(np.ceil(((norm.isf(alpha / 2) + norm.isf(1 - power)) / np.arctanh(rho)) ** 2 + 3))

def ci_rho(r, n, conf=0.95):
    z = np.arctanh(r); se = 1 / np.sqrt(n - 3); h = norm.isf((1 - conf) / 2)
    return np.tanh(z - h * se), np.tanh(z + h * se)

if __name__ == "__main__":
    print("== (1) Normal bivariado: top-1 por proxy en un pool de N candidatos ==")
    for N in (29, 100, 595):
        print(f"-- N={N}; E[max de N normales estandar] ~ {np.mean(rng.standard_normal((20000,N)).max(1)):.3f}")
        for rho in (0.3, 0.4, 0.5, 0.7, 0.8):
            o = sim_pool(N, rho)
            print(f" rho={rho}: " + ", ".join(f"{k}={v:.3f}" for k, v in o.items()))
    print("\n== Verificacion contra Haeussler 2016 (zebrafish: 104 guias/11 loci, top-2 por locus; observado: 9/11 loci con una de las 2 mejores) ==")
    for rho in (0.3, 0.4, 0.5):
        pr = hit_at_least_one_true_topq(N=9, rho=rho, k=2, q=2)
        pr10 = hit_at_least_one_true_topq(N=10, rho=rho, k=2, q=2)
        print(f" rho={rho}: P(>=1 de top2-proxy in top2-verdad), N=9: {pr:.3f}; N=10: {pr10:.3f}; esperado en 11 loci ~ {11*pr:.1f}-{11*pr10:.1f}; observado 9")
    print(" fraccion de ensayos: 2/9.45 =", round(2/9.45, 3), "-> 104->22 inyecciones = factor", round(104/22, 2))

    print("\n== (2) Binormal: factor de reduccion de ensayos por acierto = precision/b ==")
    for b in (0.003, 0.03, 0.12):
        for auc in (0.6, 0.7, 0.8, 0.9):
            for f in (0.01, 0.1):
                if f > b:  # el top-f debe poder contener positivos
                    p, r = binormal_precision(b, auc, f)
                    print(f" b={b}, AUC={auc}, top-f={f}: precision={p:.3f} (EF={p/b:.1f}x), recall={r:.3f}")
    print("\n== Verificaciones numericas de fuente (calculo propio sobre numeros citados) ==")
    # Lyu 2019 D4: 453000 activos modelados (IC95% 188000-1035000) en 138e6; hit rate top 22-26%
    b0 = 453000 / 138e6; blo = 188000 / 138e6; bhi = 1035000 / 138e6
    print(f" Lyu D4: b = {b0:.5f} ({blo:.5f}-{bhi:.5f}); EF con p=0.24: {0.24/b0:.0f}x ({0.24/bhi:.0f}-{0.24/blo:.0f}x); ensayos por acierto: {1/0.24:.1f} vs {1/b0:.0f}")
    # Hie 2023 enriquecimiento de tasa base a tasa con LM
    for nm, b1, p1 in (("beta-lactamasa", 0.07, 0.40), ("HA", 0.07, 0.31), ("PafA", 0.03, 0.20)):
        print(f" Hie 2023 {nm}: {b1:.2f}->{p1:.2f} EF={p1/b1:.1f}x; ensayos por acierto {1/b1:.1f}->{1/p1:.1f}")
    # Overath: 12% binders agregado; top-10 recupera >=1 binder en 15/15 targets
    print(f" Overath: azar con b=0.12 y 10 ensayos: P(>=1)={1-0.88**10:.3f}; esperado en 15 targets {15*(1-0.88**10):.1f}; observado 15 (b por target no abierta -> aproximacion)")
    # Adaptyv: hit rate 2.5% (5/201) R1 -> 13% R2; 0.01% previo
    print(f" Adaptyv: 0.0001->0.025 = {0.025/0.0001:.0f}x; R1->R2 {0.13/0.025:.1f}x")
    # CCLMoff base: GUIDE-seq 414 positivos de 1,599,541 sitios
    print(f" CCLMoff GUIDE-seq: b={414/1599541:.6f}; AUPRC 0.52 => lift ~{0.52/(414/1599541):.0f}x (AUPRC no es precision@k)")
    print("\n== (3) KL de best-of-n (Gao et al.): KL = ln n - (n-1)/n; d = sqrt(KL) ==")
    for n in (5, 29, 100, 595, 1000, 60000):
        print(f" n={n}: KL={kl_bon(n):.2f} nats, d={np.sqrt(kl_bon(n)):.2f}")
    print("\n== (4) Potencia e IC con n pequeno ==")
    for n in (22, 29, 31, 52, 100):
        print(f" n={n}: potencia p/detectar rho=0.4: {power_corr(n,0.4):.2f}; rho=0.5: {power_corr(n,0.5):.2f}; rho=0.75: {power_corr(n,0.75):.2f}")
    for rho in (0.3, 0.4, 0.5, 0.7):
        print(f" n para 80% potencia con rho={rho}: {n_for_power(rho)}")
    for r, n in ((0.5, 29), (0.5, 31), (0.4, 29), (0.7, 29), (0.5, 100)):
        lo, hi = ci_rho(r, n); print(f" IC95% (Fisher) de r={r} con n={n}: [{lo:.2f}, {hi:.2f}]")

if __name__ == "__main__":
    print("\n== (5) Pool enumerado de N=595 ventanas: P(>=1 de los k mejores por proxy cae en el q% superior verdadero) ==")
    N = 595
    for rho in (0.3, 0.4, 0.5, 0.7):
        for q in (0.01, 0.05, 0.10):
            qn = max(1, int(round(q * N)))
            vals = {k: hit_at_least_one_true_topq(N, rho, k, qn, reps=6000) for k in (1, 3, 5, 10)}
            azar = {k: 1 - np.prod([(N - qn - i) / (N - i) for i in range(k)]) for k in (1, 3, 5, 10)}
            print(f" rho={rho}, q={q:.0%} ({qn} ventanas): " + ", ".join(f"k={k}: {vals[k]:.2f} (azar {azar[k]:.2f})" for k in vals))
    print("\n== Mapeo ingenuo C de Harrell -> rho bajo normal bivariada sin censura (solo orientativo; tau = 2C-1; rho = sin(pi*tau/2)) ==")
    for C in (0.60, 0.65, 0.70, 0.73, 0.76, 0.79):
        tau = 2 * C - 1; print(f" C={C}: tau={tau:.2f}, rho~{np.sin(np.pi*tau/2):.2f}")
    print("\n== (6) Haeussler: filtro CFD>=0.023 sobre 26,034 candidatos con 143 validados (supuesto: los 143 estan dentro de los 26,034) ==")
    b = 143 / 26034; tpr, fpr = 0.98, 0.43
    tp = tpr * 143; fp = fpr * (26034 - 143)
    print(f" b={b:.4f}; retenidos={tp+fp:.0f} de 26034 ({(tp+fp)/26034:.2%}); precision={tp/(tp+fp):.4f}; EF={tp/(tp+fp)/b:.2f}; reduccion de sitios a revisar={26034/(tp+fp):.2f}x con recall {tpr:.0%}")
