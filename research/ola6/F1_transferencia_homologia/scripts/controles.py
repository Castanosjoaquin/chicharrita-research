#!/usr/bin/env python3
"""F1 — controles del preregistro: positivo (V-ATPase B), cordura (BicC) y senuelo.

Uso (raiz del repo, env f1_homologia, despues de transferir_anotacion.py):
    python controles.py
Lee resultados/transferencia_{MQ,HV}.tsv y work/F1/corrida/{orfs.faa,db_*.dmnd}; escribe
resultados/controles.json. El senuelo son 1.000 ORF al azar (semilla 0) con los residuos
barajados: cualquier hit con e <= 1e-10 es un falso positivo del umbral.
"""
import csv
import gzip
import json
import random
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import transferir_anotacion as T

R = Path("research/ola6/F1_transferencia_homologia/resultados")
W = Path("work/F1/corrida")
DIAMOND = str(Path(sys.executable).parent / "diamond")


def filas(et):
    return list(csv.DictReader(gzip.open(R / f"transferencia_{et}.tsv.gz", "rt"), delimiter="\t"))


def positivo(rows):
    r = [x for x in rows if x["contig"] == "GITV01003502.1" and x["orf_aa"] == "517"][0]
    estricta = r["categoria"].startswith(("e_", "f_"))
    amp = r["categoria_ampliada"].startswith(("e_", "f_"))
    return dict(
        orf=f"GITV01003502.1 {r['orf_hebra']} {r['orf_ini']}-{r['orf_fin']}",
        mejor_hit_estricta=r["ref_producto"], pident_estricta=float(r["pident"]),
        categoria_estricta=r["categoria"],
        categoria_ampliada=r["categoria_ampliada"],
        ampliada_ref=r["ampliada_ref_producto"], ampliada_pident=r["ampliada_pident"],
        pasa_estricta=estricta and float(r["pident"]) >= 99 and "subunit B" in r["ref_producto"],
        pasa_ampliada=amp and r["ampliada_pident"] != "" and float(r["ampliada_pident"]) >= 99
        and "subunit B" in r["ampliada_ref_producto"])


def cordura_bicc(rows):
    out = []
    for r in rows:
        if r["contig"] == "GITV01000968.1" and r["categoria_ampliada"].startswith(("e_", "f_")):
            out.append(dict(orf_aa=r["orf_aa"], producto=r["ampliada_ref_producto"],
                            pident=r["ampliada_pident"], categoria_estricta=r["categoria"]))
    return dict(orfs_con_reciproco_ampliada=out,
                algun_bicaudal=any("bicaudal" in o["producto"].lower() for o in out))


def senuelo():
    rng = random.Random(0)
    orfs = list(T.leer_fasta(W / "orfs.faa"))
    muestra = rng.sample(orfs, 1000)
    with open(W / "senuelo.faa", "w") as fo:
        for i, (cab, seq) in enumerate(muestra):
            l = list(seq)
            rng.shuffle(l)
            fo.write(f">senuelo{i}\n{''.join(l)}\n")
    res = {}
    for et in ("MQ", "HV"):
        out = W / f"senuelo_{et}.tsv"
        T.diamond_blastp(DIAMOND, W / "senuelo.faa", W / f"db_{et}", out)
        con_hit = {l.split("\t")[0] for l in open(out)}
        res[et] = dict(consultas=1000, con_hit=len(con_hit), tasa=len(con_hit) / 1000)
    return res


if __name__ == "__main__":
    mq = filas("MQ")
    res = dict(positivo_MQ=positivo(mq), cordura_bicc_MQ=cordura_bicc(mq), senuelo=senuelo())
    (R / "controles.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    print(json.dumps(res, indent=1, ensure_ascii=False))
