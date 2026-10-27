#!/usr/bin/env python3
"""F1 — distribuciones por banda y contraste entre las dos referencias (preregistro, punto 7).
Uso (raiz del repo): python resumir.py ; escribe resultados/resumen_lectura.json"""
import collections
import csv
import gzip
import json
from pathlib import Path

R = Path("research/ola6/F1_transferencia_homologia/resultados")


def leer(et):
    return list(csv.DictReader(gzip.open(R / f"transferencia_{et}.tsv.gz", "rt"), delimiter="\t"))


def recip(r, amp):
    return r["categoria_ampliada" if amp else "categoria"].startswith(("e_", "f_"))


def vista(rows, amp):
    pre = "ampliada_" if amp else ""
    sel = [r for r in rows if recip(r, amp)]
    inf = [r for r in sel if (r["categoria_ampliada"] if amp else r["categoria"]).startswith("f_")]
    por_banda = collections.Counter(r[pre + "banda_identidad"] for r in inf)
    cob = collections.Counter()
    for r in inf:
        q, s = float(r[pre + "cob_orf"]), float(r[pre + "cob_ref"])
        cob["cobertura_alta" if min(q, s) >= 70 else "parcial" if min(q, s) >= 30 else "fragmento"] += 1
    return dict(orfs_reciprocos=len(sel), con_nombre_informativo=len(inf),
                sin_nombre_informativo=len(sel) - len(inf),
                por_banda_de_identidad=dict(por_banda), por_cobertura=dict(cob),
                orfs_con_nombre_en_banda_ge90_y_cobertura_alta=sum(
                    1 for r in inf if r[pre + "banda_identidad"] == ">=90"
                    and min(float(r[pre + "cob_orf"]), float(r[pre + "cob_ref"])) >= 70))


def contraste(mq, hv, amp):
    pre = "ampliada_" if amp else ""
    h = {r["contig"] + "|" + r["orf_ini"] + "|" + r["orf_fin"]: r for r in hv if recip(r, amp)}
    n = coinciden = 0
    for r in mq:
        if not recip(r, amp):
            continue
        o = h.get(r["contig"] + "|" + r["orf_ini"] + "|" + r["orf_fin"])
        a, b = r[pre + "nombre_normalizado"], (o or {}).get(pre + "nombre_normalizado", "")
        if o is not None and a and b:
            n += 1
            coinciden += a == b
    return dict(orfs_con_nombre_informativo_en_las_dos=n, coinciden=coinciden,
                pct=round(100 * coinciden / n, 1) if n else None)


mq, hv = leer("MQ"), leer("HV")
out = {}
for amp, nom in ((False, "estricta_preregistrada"), (True, "ampliada_H_post_hoc")):
    out[nom] = dict(MQ=vista(mq, amp), HV=vista(hv, amp), contraste_MQ_vs_HV=contraste(mq, hv, amp))
(R / "resumen_lectura.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
