"""V2 - P4 (fuente de la secuencia) y P5 (criterio de riesgo) del PREREGISTRO_ROBUSTEZ.md."""
from __future__ import annotations
import csv, json, sys
from pathlib import Path
import numpy as np
from Bio import SeqIO
from Bio.Seq import Seq

AQUI = Path(__file__).resolve(); RAIZ = AQUI.parents[4]; SAL = AQUI.parents[1] / "resultados"
sys.path.insert(0, str(RAIZ / "research/ola4/M7_robustez_bicc/scripts"))
sys.path.insert(0, str(RAIZ / "tools/sifi21_port"))
import grilla_parametros as G   # noqa: E402
import ranking as R             # noqa: E402
import ranking_v2 as V          # noqa: E402

CDS_ID, INI, FIN = "GITV01002940_1_cds", 325, 624
cds = "".join(l.strip() for l in (RAIZ / "work/V2/rpn6_cds.fna").read_text().split(">" + CDS_ID, 1)[1]
              .split(">")[0].splitlines()[1:]).upper()
mol = cds[INI - 1:FIN]
out = {}

# ---------------- P4: la molecula tal como la escribe cada fuente -----------------------
fuentes = {"GHCC01050726.1 (Argentina)": ("work/W5/ref/TSA_GHCC01.fasta", "GHCC01050726.1"),
           "GCWP01019967.1 (Illinois)": ("work/W5/ref/TSA_GCWP01.fasta", "GCWP01019967.1")}
base = {m: G.eficientes(G.primitivos(mol, "vienna", "NN3"), m, G.DEF_END, G.DEF_ACC) for m in G.MODOS}
out["P4"] = {"molecula_Rpn6_GITV01": {m: int(v.sum()) for m, v in base.items()}}
for etiqueta, (ruta, cid) in fuentes.items():
    rec = next(r for r in SeqIO.parse(RAIZ / ruta, "fasta") if r.id == cid)
    t = str(rec.seq).upper(); res = None
    for hebra, s in (("+", t), ("-", str(Seq(t).reverse_complement()))):
        i, j = s.find(mol[:19]), s.find(mol[-19:])
        if i >= 0 and j >= 0 and j + 19 - i == 300:
            res = (hebra, s[i:j + 19]); break
    if res is None:
        out["P4"][etiqueta] = "NO CORRIDA: no se hallan los dos extremos a 300 nt"; continue
    hebra, m2 = res
    dif = [k + 1 for k in range(300) if m2[k] != mol[k]]
    fila = {"hebra": hebra, "posiciones_distintas_de_300": dif}
    for modo in G.MODOS:
        e2 = G.eficientes(G.primitivos(m2, "vienna", "NN3"), modo, G.DEF_END, G.DEF_ACC)
        e1 = base[modo]
        fila[modo] = {"eficientes": int(e2.sum()), "conservadas": int((e1 & e2).sum()),
                      "perdidas": int((e1 & ~e2).sum()), "ganadas": int((~e1 & e2).sum())}
    out["P4"][etiqueta] = fila

# ---------------- P5: criterios de riesgo con ranking.ejes oficial ----------------------
V.con_panel(sin_humano=False)
wr, wc = R.pesos_base()
excluir = R.excluidas_de({"gen": "X", "estrategia": "insecto", "region": (1, 300), "largo": 300}, "off")
n = len(cds) - 20; rk = {}
with (RAIZ / "work/V2/offtarget/offtarget_por_sirna.tsv").open(newline="") as f:
    rd = csv.DictReader(f, delimiter="\t"); cols = [c for c in rd.fieldnames if "|" in c]
    for c in cols:
        ref, crit = c.split("|", 1); ref = ref[:-4] if ref.endswith(".fna") else ref
        rk.setdefault(ref, {})[crit] = np.zeros(n, bool)
    for r in rd:
        if r["consulta"] != CDS_ID: continue
        p = int(r["pos"])
        for c in cols:
            if int(r[c] or 0) > 0:
                ref, crit = c.split("|", 1); ref = ref[:-4] if ref.endswith(".fna") else ref
                rk[ref][crit][p - 1] = True
m = 280; sl = slice(INI - 1, INI - 1 + m)
efi = base["corregido"]
def g_con(crits):
    return {"gen": "Rpn6", "n": m, "eficiente": efi.copy(), "presente": np.ones(m, bool),
            "riesgo": {ref: {c: (d[c][sl].copy() if c in crits else np.zeros(m, bool)) for c in R.CRITERIOS}
                       for ref, d in rk.items()}}
p5 = {"ventanas_con_acierto_por_criterio": {}, "limpieza": {}}
for c in R.CRITERIOS:
    hit = np.zeros(m, bool)
    for d in rk.values(): hit |= d[c][sl]
    p5["ventanas_con_acierto_por_criterio"][c] = int(hit.sum())
for etiqueta, crits in {"solo perfecto_21": ["perfecto_21"], "solo perfecto_ge19": ["perfecto_ge19"],
                        "perfecto_21 + ge19 (sin mm1)": ["perfecto_21", "perfecto_ge19"],
                        "los tres (oficial)": list(R.CRITERIOS)}.items():
    g = g_con(crits)
    cons = R.ejes(g, 1, m, wr, wc, excluir, False); mec = R.ejes(g, 1, m, wr, wc, excluir, True)
    hay = np.zeros(m, bool)
    for d in g["riesgo"].values():
        for c in crits: hay |= d[c]
    p5["limpieza"][etiqueta] = {"conservadora": round(cons["limpieza"], 4), "mecanicista": round(mec["limpieza"], 4),
                                "limpias_y_eficientes": int((efi & ~hay).sum()), "con_acierto": int(hay.sum())}
p5["BicC_922_1221_publicado_O3"] = {"conservadora": 0.9884, "mecanicista": 0.9974,
                                    "limpias_y_eficientes": 22, "con_acierto": 19}
out["P5"] = p5
(SAL / "fuentes_y_criterios.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(json.dumps(out, ensure_ascii=False, indent=1))
