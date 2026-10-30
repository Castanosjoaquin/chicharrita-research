"""V2 - barrido de robustez de `Rpn6` (P1, P2, P3 del PREREGISTRO_ROBUSTEZ.md).

Importa el motor de M7 SIN tocarlo. `BicC_Dm` 922-1221 NO se recalcula: se lee de
`research/ola4/M7_robustez_bicc/resultados/grilla_parametros.tsv` (filas vienna), y antes de leer
ningun numero de `Rpn6` se reproducen 12 de sus filas con el motor local. Si una falla, aborta.
Lo que se escribe son conteos, nunca secuencia.
"""
from __future__ import annotations
import csv, itertools, json, sys
from pathlib import Path
import numpy as np

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
SAL = AQUI.parents[1] / "resultados_002972"
sys.path.insert(0, str(RAIZ / "research/ola4/M7_robustez_bicc/scripts"))
sys.path.insert(0, str(RAIZ / "tools/sifi21_port"))
import grilla_parametros as G  # noqa: E402  el motor de M7, sin tocarlo

CDS_ID = "GITV01002972_1_cds"
INI, FIN = 345, 644
BICC_INI, BICC_FIN = 922, 1221
M7_TSV = RAIZ / "research/ola4/M7_robustez_bicc/resultados/grilla_parametros.tsv"
OFF_TSV = RAIZ / "work/V2/offtarget/offtarget_por_sirna.tsv"
BANDA, LARGO = 59, 300
SUF = {"contexto": "ctx", "recorte": "rec"}


def leer_cds() -> str:
    seq, cur = {}, None
    for l in (RAIZ / "work/V2/rpn6_cds.fna").read_text().splitlines():
        if l.startswith(">"):
            cur = l[1:].strip(); seq[cur] = []
        else:
            seq[cur].append(l.strip())
    return "".join(seq[CDS_ID]).upper()


def veto_por_ventana(n: int) -> np.ndarray:
    v = np.zeros(n, bool)
    with OFF_TSV.open(newline="") as f:
        rd = csv.DictReader(f, delimiter="\t")
        c21 = [c for c in rd.fieldnames if c.endswith("|perfecto_21")]
        for r in rd:
            if r["consulta"] == CDS_ID and any(int(r[c] or 0) > 0 for c in c21):
                v[int(r["pos"]) - 1] = True
    return v


def main() -> int:
    SAL.mkdir(parents=True, exist_ok=True)
    cds = leer_cds()
    bicc = G.leer_fasta(G.FASTA["BicC_Dm"])
    nR = len(cds) - G.K + 1
    print("Rpn6 CDS %d nt (%d ventanas); BicC_Dm %d nt" % (len(cds), nR, len(bicc)), flush=True)

    # ---- primitivos ------------------------------------------------------------------
    prim_gen4 = {("vienna", "NN3"): {g: G.primitivos(G.leer_fasta(G.FASTA[g]), "vienna", "NN3")
                                     for g in G.GENES}}
    PR_gen, PR_rec = {}, {}
    for tabla in G.TABLAS:
        PR_gen[tabla] = G.primitivos(cds, "vienna", tabla)
        PR_rec[tabla] = G.primitivos(cds[INI - 1:FIN], "vienna", tabla)
    PB_gen = prim_gen4[("vienna", "NN3")]["BicC_Dm"]
    PB_gen_t = {"NN3": PB_gen, "NN4": G.primitivos(bicc, "vienna", "NN4")}
    PB_rec = {t: G.primitivos(bicc[BICC_INI - 1:BICC_FIN], "vienna", t) for t in G.TABLAS}
    print("primitivos listos", flush=True)

    # ---- ANCLAS (§2): abortan ---------------------------------------------------------
    anc = G.anclas(prim_gen4)
    G.verificar_vectorizacion(PR_gen["NN3"], "Rpn6 gen")
    G.verificar_vectorizacion(PR_rec["NN3"], "Rpn6 region recortada")
    m7 = {}
    for r in csv.DictReader(M7_TSV.open(newline=""), delimiter="\t"):
        if r["backend"] == "vienna":
            m7[(r["tabla_nn"], r["modo"], round(float(r["end_thr"]), 2),
                round(float(r["access_thr"]), 2), r["marco"])] = int(r["922-1221"])
    esquinas = [(0.0, 0.05), (0.0, 0.30), (2.0, 0.05), (2.0, 0.30), (1.0, 0.10)]
    ver = []
    for tabla, modo in itertools.product(G.TABLAS, G.MODOS):
        for e, a in esquinas:
            ctx = int(G.eficientes(PB_gen_t[tabla], modo, e, a)[BICC_INI - 1:BICC_FIN].sum())
            rec = int(G.eficientes(PB_rec[tabla], modo, e, a).sum())
            ok = (ctx == m7[(tabla, modo, e, a, "contexto")]
                  and rec == m7[(tabla, modo, e, a, "recorte")])
            ver.append({"tabla": tabla, "modo": modo, "end": e, "acc": a,
                        "mio_ctx": ctx, "m7_ctx": m7[(tabla, modo, e, a, "contexto")],
                        "mio_rec": rec, "m7_rec": m7[(tabla, modo, e, a, "recorte")], "ok": ok})
    n_ok = sum(v["ok"] for v in ver)
    print("anclas de BicC contra M7: %d de %d filas coinciden" % (n_ok, len(ver)), flush=True)
    if n_ok != len(ver):
        print(json.dumps([v for v in ver if not v["ok"]], indent=1))
        raise SystemExit("ANCLA FALLIDA: mi motor no reproduce la grilla de M7 para BicC")

    # ---- regiones admisibles de Rpn6 y rival por densidad -----------------------------
    veto = veto_por_ventana(nR)
    cds_nt = len(cds)
    ini_min, ini_max = BANDA + 1, cds_nt - BANDA - LARGO + 1
    cv = np.concatenate([[0], np.cumsum(veto)])
    adm = np.array([s for s in range(ini_min, ini_max + 1)
                    if cv[s - 1 + (LARGO - G.K + 1)] - cv[s - 1] == 0])  # 280 ventanas internas
    print("regiones admisibles: %d de %d posibles (inicio %d..%d)"
          % (len(adm), ini_max - ini_min + 1, ini_min, ini_max), flush=True)
    ef0 = G.eficientes(PR_gen["NN3"], "corregido", G.DEF_END, G.DEF_ACC)
    c0 = np.concatenate([[0], np.cumsum(ef0)])
    todas = np.arange(1, nR - LARGO + 2)
    cnt0 = np.array([c0[s - 1 + LARGO] - c0[s - 1] for s in todas])
    rival = int(todas[int(np.argmax(cnt0))])
    print("rival por densidad sin veto: %d-%d con %d eficientes (contexto, defecto)"
          % (rival, rival + LARGO - 1, cnt0.max()), flush=True)
    PR_riv = {t: G.primitivos(cds[rival - 1:rival + LARGO - 1], "vienna", t) for t in G.TABLAS}

    # ---- la grilla ----------------------------------------------------------------------
    filas, estab = [], []
    for tabla, modo, e, a in itertools.product(G.TABLAS, G.MODOS, G.END_GRID, G.ACC_GRID):
        eg = G.eficientes(PR_gen[tabla], modo, e, a)
        cg = np.concatenate([[0], np.cumsum(eg)])
        cuenta = lambda s: int(cg[s - 1 + LARGO] - cg[s - 1])  # 300 arranques (marco contexto)
        R_ctx = cuenta(INI)
        R_rec = int(G.eficientes(PR_rec[tabla], modo, e, a).sum())
        riv_ctx = cuenta(rival)
        riv_rec = int(G.eficientes(PR_riv[tabla], modo, e, a).sum())
        B_ctx, B_rec = m7[(tabla, modo, e, a, "contexto")], m7[(tabla, modo, e, a, "recorte")]
        filas.append({"tabla_nn": tabla, "modo": modo, "end_thr": e, "access_thr": a,
                      "es_defecto": int(e == G.DEF_END and a == G.DEF_ACC),
                      "Rpn6_ctx": R_ctx, "BicC_ctx": B_ctx, "Rpn6_rec": R_rec, "BicC_rec": B_rec,
                      "rival_ctx": riv_ctx, "rival_rec": riv_rec})
        cnt = np.array([cuenta(int(s)) for s in adm])
        mx = int(cnt.max())
        arg = adm[cnt == mx]
        estab.append({"tabla_nn": tabla, "modo": modo, "end_thr": e, "access_thr": a,
                      "max": mx, "n_empatadas": int(len(arg)),
                      "Rpn6_en_el_maximo": int(R_ctx == mx and INI in adm),
                      "Rpn6_conteo": R_ctx, "primera_del_maximo": int(arg[0])})

    with (SAL / "robustez_grilla.tsv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]), delimiter="\t"); w.writeheader(); w.writerows(filas)
    with (SAL / "robustez_estabilidad_region.tsv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(estab[0]), delimiter="\t"); w.writeheader(); w.writerows(estab)

    def frac(par, a, b, filtro=lambda r: True):
        s = [r for r in filas if filtro(r)]
        d = np.array([r[a] - r[b] for r in s])
        return {"n": len(s), "gana": int((d > 0).sum()), "empata": int((d == 0).sum()),
                "pierde": int((d < 0).sum()),
                "gana_pct": round(100 * (d > 0).mean(), 1), "empata_pct": round(100 * (d == 0).mean(), 1),
                "pierde_pct": round(100 * (d < 0).mean(), 1),
                "dif_mediana": float(np.median(d)), "dif_min": int(d.min()), "dif_max": int(d.max())}
    cortes = {"en conjunto": lambda r: True,
              "modo = fiel": lambda r: r["modo"] == "fiel", "modo = corregido": lambda r: r["modo"] == "corregido",
              "tabla = NN3": lambda r: r["tabla_nn"] == "NN3", "tabla = NN4": lambda r: r["tabla_nn"] == "NN4",
              "punto por defecto": lambda r: r["es_defecto"] == 1}
    res = {"anclas": {"M7_gen_entero_y_regiones": anc, "BicC_vs_grilla_M7": {"filas": len(ver), "coinciden": n_ok}},
           "region_rpn6": [INI, FIN], "region_bicc": [BICC_INI, BICC_FIN],
           "regiones_admisibles": {"n": int(len(adm)), "de": ini_max - ini_min + 1},
           "rival_densidad": {"region": [rival, rival + LARGO - 1], "conteo_defecto_ctx": int(cnt0.max())},
           "configuraciones": len(filas), "motor": "vienna (RNAplfold 2.1.5: NO CORRIDO, binario no disponible)",
           "P1": {m: {c: frac("P1", f"Rpn6_{SUF[m]}", f"BicC_{SUF[m]}", fl) for c, fl in cortes.items()}
                  for m in ("contexto", "recorte")},
           "P3": {m: frac("P3", f"Rpn6_{SUF[m]}", f"rival_{SUF[m]}") for m in ("contexto", "recorte")}}
    en = [e for e in estab]
    res["P2"] = {"configuraciones": len(en),
                 "Rpn6_en_el_maximo": int(sum(e["Rpn6_en_el_maximo"] for e in en)),
                 "pct": round(100 * np.mean([e["Rpn6_en_el_maximo"] for e in en]), 1)}
    from collections import Counter
    fuera = Counter(e["primera_del_maximo"] for e in en if not e["Rpn6_en_el_maximo"])
    res["P2"]["reemplazos_mas_frecuentes"] = [{"inicio": int(k), "veces": v} for k, v in fuera.most_common(6)]
    res["P2"]["conteo_Rpn6_vs_maximo_mediana_brecha"] = float(np.median([e["max"] - e["Rpn6_conteo"] for e in en]))
    (SAL / "robustez_resumen.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))

    for m in ("recorte", "contexto"):
        c = res["P1"][m]["en conjunto"]
        print("P1 %-8s n=%d  Rpn6 gana %.1f%% / empata %.1f%% / pierde %.1f%%  dif mediana %+.0f (rango %+d a %+d)"
              % (m, c["n"], c["gana_pct"], c["empata_pct"], c["pierde_pct"], c["dif_mediana"], c["dif_min"], c["dif_max"]))
    print("P2 325-624 en el maximo de las admisibles: %d de %d (%.1f%%)"
          % (res["P2"]["Rpn6_en_el_maximo"], len(en), res["P2"]["pct"]))
    for m in ("contexto", "recorte"):
        c = res["P3"][m]
        print("P3 %-8s vs %d-%d: Rpn6 gana %.1f%% / empata %.1f%% / pierde %.1f%%"
              % (m, rival, rival + LARGO - 1, c["gana_pct"], c["empata_pct"], c["pierde_pct"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
