#!/usr/bin/env python3
"""Reanalisis de los datos suplementarios de dsRIP (Cedden et al., BMC Biol 2025, PMC12039203).
Fuente de datos: archivo suplementario MOESM2 (hojas 'Fig 1 log-rank' y 'Fig. 2 regression'), bajado
de Europe PMC (endpoint supplementaryFiles). Solo dependencias: requests, lxml, numpy, pandas, scipy.
Salida: tablas CSV en la misma carpeta + resumen por stdout. Semilla fija.
Alcance: N chico (29 siRNA, 28 dsRNA, 8 genes). Todo es EN MUESTRA salvo donde se indica LOO/LOGO.
No se sube nada del proyecto a ningun servicio: solo se descarga el suplemento publico.
"""
import io, re, zipfile, sys, os
import numpy as np, pandas as pd, requests
from lxml import etree
from scipy import stats

OUT = os.path.dirname(os.path.abspath(__file__))
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
rng = np.random.default_rng(20261018)

def read_xlsx(zf_bytes):
    z = zipfile.ZipFile(io.BytesIO(zf_bytes))
    ss = [''.join(si.xpath('.//m:t/text()', namespaces=NS)) for si in
          etree.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', NS)]
    wb = etree.fromstring(z.read('xl/workbook.xml'))
    rels = {r.get('Id'): r.get('Target') for r in etree.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
    sheets = {}
    for sh in wb.find('m:sheets', NS):
        tgt = rels[sh.get('{%s}id' % NS['r'])].lstrip('/')
        tgt = tgt if tgt.startswith('xl/') else 'xl/' + tgt
        rows = []
        for row in etree.fromstring(z.read(tgt)).iter('{%s}row' % NS['m']):
            d = {}
            for c in row.findall('m:c', NS):
                col = re.match(r'[A-Z]+', c.get('r')).group(); v = c.find('m:v', NS)
                d[col] = ss[int(v.text)] if (c.get('t') == 's' and v is not None) else (v.text if v is not None else None)
            rows.append(d)
        sheets[sh.get('name')] = rows
    return sheets

def load():
    r = requests.get('https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12039203/supplementaryFiles', timeout=180)
    r.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(r.content))
    name = [n for n in z.namelist() if n.endswith('MOESM2_ESM.xlsx')][0]
    return read_xlsx(z.read(name))

def to_num(x):
    try: return float(x)
    except Exception: return np.nan

def sirna_table(S):
    rows = S['Fig 1 log-rank']; hdr = {k: v.strip() for k, v in rows[0].items() if v}
    df = pd.DataFrame([{hdr[c]: r.get(c) for c in hdr} for r in rows[1:] if r.get('A')])
    df = df.rename(columns={'hazard ratio vs mGFP': 'HR', 'binding energy_percentile': 'bind_pct',
                            'asymScore_percentile': 'asym_pct', 'self_fold_energy_percentile': 'selffold_pct',
                            'accessibility_percentile': 'access_pct', 'Code': 'siRNA'})
    for c in ['HR', 'anti_GC', 'anti_9_14_GC', 'bind_pct', 'anti_10th_A', 'asym_pct', 'selffold_pct', 'access_pct']:
        df[c] = df[c].map(to_num)
    df = df[['siRNA', 'HR', 'anti_GC', 'anti_9_14_GC', 'bind_pct', 'anti_10th_A', 'ORF_info', 'asym_pct',
             'selffold_pct', 'access_pct']]
    return df

def dsrna_table(S):
    rows = S['Fig. 2 regression']; out = []
    for r in rows:
        g = r.get('A')
        if g and g.strip().startswith('Tc-') and r.get('E') in ('ORF', 'UTR'):
            out.append(dict(gene=g.strip(), siRNA_score=to_num(r['B']), access_score=to_num(r['C']),
                            region=r['D'] if 'D' in r and r['D'] in ('ORF','UTR') else r['E'], HR=to_num(r.get('F') if r.get('E') in ('ORF','UTR') and False else None)))
    return out

def dsrna_table2(S):
    # layout: A gene, B siRNA score, C accessibility, D region, E hazard ratio (columns tras filtrar None)
    rows = S['Fig. 2 regression']; out = []
    for r in rows:
        vals = [r.get(c) for c in sorted(r, key=lambda x: (len(x), x)) if r.get(c) not in (None, 'None')]
        if len(vals) == 5 and str(vals[0]).strip().startswith('Tc-') and vals[3] in ('ORF', 'UTR'):
            out.append(dict(gene=vals[0].strip(), siRNA_score=to_num(vals[1]), access_score=to_num(vals[2]),
                            region=vals[3], HR=to_num(vals[4])))
    return pd.DataFrame(out)

def boot_ci(fn, n, B=5000, idx_groups=None):
    vals = []
    for _ in range(B):
        i = rng.integers(0, n, n)
        try: vals.append(fn(i))
        except Exception: pass
    vals = np.array([v for v in vals if np.isfinite(v)])
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))

def topk_enrichment(score, target, k, B=20000):
    """Fraccion de los k mejores por 'score' que estan entre los k mejores por 'target'. IC por permutacion nula (azar)."""
    n = len(score); s_top = set(np.argsort(-score, kind='stable')[:k]); t_top = set(np.argsort(-target, kind='stable')[:k])
    obs = len(s_top & t_top)
    null = np.array([len(set(rng.permutation(n)[:k]) & t_top) for _ in range(B)])
    return obs, k, k * k / n, float((null >= obs).mean())

def auc(score, label):
    pos = score[label == 1]; neg = score[label == 0]
    return float((pos[:, None] > neg[None, :]).mean() + 0.5 * (pos[:, None] == neg[None, :]).mean())

def main():
    S = load()
    # ---------- Nivel siRNA ----------
    df = sirna_table(S); df.to_csv(os.path.join(OUT, 'dsrip_sirna_nivel.csv'), index=False)
    pal = df[df['asym_pct'].isna()]                     # los 2 palindromicos, excluidos del Cox por los autores
    d = df.dropna(subset=['asym_pct']).reset_index(drop=True)
    print('siRNA con features (usados por los autores en el Cox):', len(d), '| palindromicos excluidos:', len(pal))
    print('siRNA con HR=0 (sin efecto detectable, P no sig.):', int((d.HR == 0).sum()), 'de', len(d))
    res = []
    for f in ['asym_pct', 'selffold_pct', 'anti_9_14_GC', 'anti_10th_A', 'access_pct', 'bind_pct', 'anti_GC']:
        rho, p = stats.spearmanr(d[f], d.HR)
        lo, hi = boot_ci(lambda i: stats.spearmanr(d[f].values[i], d.HR.values[i])[0], len(d))
        res.append((f, rho, lo, hi, p))
    print('\nSpearman feature vs HR (n=29, en muestra), IC95% bootstrap')
    for f, rho, lo, hi, p in res: print(f'  {f:14s} rho={rho:+.2f} [{lo:+.2f},{hi:+.2f}] p={p:.3f}')
    # Score compuesto con coeficientes leidos de la Fig. 1c (HR por unidad): beta = ln(HR)
    beta = dict(anti_9_14_GC=np.log(1.0160), anti_10th_A=np.log(1.5659), asym_pct=np.log(1.0139), selffold_pct=np.log(1.0103))
    d['score'] = sum(b * d[f] for f, b in beta.items())
    rho, p = stats.spearmanr(d.score, d.HR)
    lo, hi = boot_ci(lambda i: stats.spearmanr(d.score.values[i], d.HR.values[i])[0], len(d))
    print(f'\nScore compuesto (4 features, coef. de Fig.1c) vs HR: rho={rho:+.2f} [{lo:+.2f},{hi:+.2f}] p={p:.4f} (EN MUESTRA: los coef. se ajustaron con estos mismos 29)')
    act = (d.HR > 0).astype(int).values
    a = auc(d.score.values, act)
    alo, ahi = boot_ci(lambda i: auc(d.score.values[i], act[i]), len(d))
    print(f'AUC score -> activo(HR>0) vs inactivo(HR=0): {a:.2f} [{alo:.2f},{ahi:.2f}] (n+={act.sum()}, n-={(1-act).sum()})')
    # Leave-one-out con regresion lineal sobre las 4 features (surrogado del Cox: no hay datos crudos de larva usados)
    X = np.column_stack([np.ones(len(d))] + [d[f].values for f in beta]); y = d.HR.values; pred = np.zeros(len(d))
    for i in range(len(d)):
        m = np.ones(len(d), bool); m[i] = False
        coef, *_ = np.linalg.lstsq(X[m], y[m], rcond=None); pred[i] = X[i] @ coef
    rho_loo, p_loo = stats.spearmanr(pred, y)
    lo, hi = boot_ci(lambda i: stats.spearmanr(pred[i], y[i])[0], len(d))
    print(f'LOO (OLS 4 features, sustituto del Cox): Spearman pred vs HR = {rho_loo:+.2f} [{lo:+.2f},{hi:+.2f}] p={p_loo:.4f}')
    # OLS a nivel siRNA (n=29) con las 4 features: p-valores con la unidad de analisis correcta (el siRNA, no la larva)
    Xo = np.column_stack([np.ones(len(d))] + [d[f].values for f in beta]); yo = d.HR.values
    coef, res, rk, sv = np.linalg.lstsq(Xo, yo, rcond=None)
    resid = yo - Xo @ coef; dof = len(yo) - Xo.shape[1]; s2 = resid @ resid / dof
    cov = s2 * np.linalg.inv(Xo.T @ Xo); se = np.sqrt(np.diag(cov)); tv = coef / se; pv = 2 * stats.t.sf(np.abs(tv), dof)
    r2 = 1 - (resid @ resid) / ((yo - yo.mean()) @ (yo - yo.mean())); r2a = 1 - (1 - r2) * (len(yo) - 1) / dof
    print('\nOLS HR ~ 4 features a nivel siRNA (n=29, gl=%d): R2=%.2f, R2 ajustado=%.2f' % (dof, r2, r2a))
    for nm, c_, t_, p_ in zip(['intercepto'] + list(beta), coef, tv, pv):
        print(f'  {nm:14s} coef={c_:+.3f} t={t_:+.2f} p={p_:.3f}')
    # Top-k
    print('\nEnriquecimiento top-k (score vs HR medido), n=29')
    for k in (5, 10):
        for nm, sc in [('score compuesto', d.score.values), ('LOO', pred), ('asimetria sola', d.asym_pct.values)]:
            obs, kk, exp, pv = topk_enrichment(sc, d.HR.values, k)
            print(f'  top-{k:2d} {nm:16s}: {obs}/{kk} en el top-{k} medido (azar esperado {exp:.1f}; p perm={pv:.3f})')
    # Filtro por reglas simples: falsos negativos entre los potentes
    pot = d.HR >= d.HR.quantile(2/3)                     # tercio superior de HR (>=10 siRNA)
    print(f'\nPotentes = tercio superior de HR (HR >= {d.HR.quantile(2/3):.1f}), n={int(pot.sum())}')
    d['pred_loo'] = pred
    inact = d.HR == 0
    for nm, mask in [('asimetria_pct>=50', d.asym_pct >= 50), ('asimetria_pct>=50 y selffold_pct>=50', (d.asym_pct >= 50) & (d.selffold_pct >= 50)),
                     ('score >= mediana (EN MUESTRA)', d.score >= d.score.median()),
                     ('prediccion LOO >= mediana (fuera de muestra)', d.pred_loo >= d.pred_loo.median())]:
        tp = int((mask & pot).sum()); fn = int((~mask & pot).sum())
        print(f'  filtro {nm:46s}: retiene {int(mask.sum())}/{len(d)}; recall potentes {tp}/{int(pot.sum())} (FN={fn}); precision {tp/max(mask.sum(),1):.2f}; inactivos(HR=0) retenidos {int((mask & inact).sum())}/{int(inact.sum())}')
    d.to_csv(os.path.join(OUT, 'dsrip_sirna_nivel_con_score.csv'), index=False)

    # ---------- Nivel dsRNA ----------
    g = dsrna_table2(S); g.to_csv(os.path.join(OUT, 'dsrip_dsrna_nivel.csv'), index=False)
    print('\ndsRNA: n=', len(g), 'genes:', g.gene.nunique(), '| ORF:', int((g.region == 'ORF').sum()), 'UTR:', int((g.region == 'UTR').sum()))
    rho, p = stats.spearmanr(g.siRNA_score, g.HR)
    lo, hi = boot_ci(lambda i: stats.spearmanr(g.siRNA_score.values[i], g.HR.values[i])[0], len(g))
    print(f'Spearman global siRNA_score vs HR: {rho:+.2f} [{lo:+.2f},{hi:+.2f}] p={p:.3f} (mezcla de genes y regiones)')
    rho_a, p_a = stats.spearmanr(g.access_score, g.HR)
    print(f'Spearman global accesibilidad vs HR: {rho_a:+.2f} p={p_a:.3f}')
    # intra-gen: centrar por gen
    g['HRc'] = g.HR - g.groupby('gene').HR.transform('mean'); g['sc'] = g.siRNA_score - g.groupby('gene').siRNA_score.transform('mean')
    g['ac'] = g.access_score - g.groupby('gene').access_score.transform('mean')
    r_in, p_in = stats.spearmanr(g.sc, g.HRc); r_ac, p_ac = stats.spearmanr(g.ac, g.HRc)
    print(f'Spearman INTRA-gen (centrado por gen) score vs HR: {r_in:+.2f} p={p_in:.3f}; accesibilidad vs HR: {r_ac:+.2f} p={p_ac:.3f}')
    # concordancia por pares dentro de gen
    conc = disc = ties = 0
    for gene, sub in g.groupby('gene'):
        v = sub[['siRNA_score', 'HR']].values
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                s = np.sign(v[i, 0] - v[j, 0]) * np.sign(v[i, 1] - v[j, 1])
                if s > 0: conc += 1
                elif s < 0: disc += 1
                else: ties += 1
    tot = conc + disc
    pc = conc / tot
    from scipy.stats import binomtest
    bt = binomtest(conc, tot, 0.5)
    ci = bt.proportion_ci(confidence_level=0.95, method='wilson')
    print(f'Pares intra-gen: concordantes {conc}, discordantes {disc} (empates {ties}); fraccion concordante {pc:.2f} IC95 Wilson [{ci.low:.2f},{ci.high:.2f}]; p binomial vs 0,5 = {bt.pvalue:.3f}')
    # mismo analisis solo con ORF (alto vs bajo diseñado por los autores)
    # el dsRNA con mayor score entre los de un gen: ¿es el de mayor HR?
    hit = 0; ng = 0; hits_orf = 0; ng_orf = 0
    for gene, sub in g.groupby('gene'):
        ng += 1; hit += int(sub.loc[sub.siRNA_score.idxmax(), 'HR'] == sub.HR.max())
        so = sub[sub.region == 'ORF']
        if len(so) >= 2:
            ng_orf += 1; hits_orf += int(so.loc[so.siRNA_score.idxmax(), 'HR'] == so.HR.max())
    print(f'Gen a gen: el dsRNA de mayor score fue el de mayor HR en {hit}/{ng} genes (todas las regiones) y en {hits_orf}/{ng_orf} (solo ORF)')
    # LOGO: pendiente intra-gen ajustada sin el gen k, prediccion del orden dentro del gen k
    concl = discl = 0
    for gene in g.gene.unique():
        tr = g[g.gene != gene]; te = g[g.gene == gene]
        slope = np.polyfit(tr.sc, tr.HRc, 1)[0]
        pr = slope * te.sc.values; v = te.HR.values
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                s = np.sign(pr[i] - pr[j]) * np.sign(v[i] - v[j])
                if s > 0: concl += 1
                elif s < 0: discl += 1
    print(f'LOGO (leave-one-gene-out) orden intra-gen: concordantes {concl}, discordantes {discl}; fraccion {concl/(concl+discl):.2f}  [NOTA: coincide con el analisis en muestra porque el signo de la pendiente es el mismo en todos los pliegues; no aporta informacion adicional]')
    # Rango del score vs variacion entre genes: cuanta varianza de HR explica el gen
    ss_tot = ((g.HR - g.HR.mean()) ** 2).sum(); ss_in = (g.HRc ** 2).sum()
    print(f'Varianza de HR dentro de gen / total = {ss_in/ss_tot:.2f} (el resto es entre genes)')
    # top tercio por score vs top tercio por HR (global, 28 -> 9)
    for k in (5, 9):
        obs, kk, exp, pv = topk_enrichment(g.siRNA_score.values, g.HR.values, k)
        print(f'  global top-{k}: {obs}/{kk} en el top-{k} medido (azar {exp:.1f}; p perm={pv:.3f})')
    # Solo ORF (21 dsRNA): orden intra-gen
    go = g[g.region == 'ORF'].copy()
    go['HRc'] = go.HR - go.groupby('gene').HR.transform('mean'); go['sc'] = go.siRNA_score - go.groupby('gene').siRNA_score.transform('mean')
    r_o, p_o = stats.spearmanr(go.sc, go.HRc)
    print(f'Solo ORF (n={len(go)}): Spearman INTRA-gen score vs HR = {r_o:+.2f} p={p_o:.3f}')
    print(f'Rango del score medio por dsRNA: {g.siRNA_score.min():.1f}-{g.siRNA_score.max():.1f} (n={len(g)}); rango de HR: {g.HR.min():.2f}-{g.HR.max():.2f}')
    print('Por region: HR medio ORF = %.1f ; UTR = %.1f ; score medio ORF = %.1f ; UTR = %.1f' % (g[g.region=='ORF'].HR.mean(), g[g.region=='UTR'].HR.mean(), g[g.region=='ORF'].siRNA_score.mean(), g[g.region=='UTR'].siRNA_score.mean()))
    # R2 ajustado del modelo publicado
    print('\nModelo publicado (hoja S2): R2=0,6247; R2 ajustado=0,4039; 28 filas / 11 parametros = 2,5 casos por parametro (copiado de la hoja)')

if __name__ == '__main__':
    main()
