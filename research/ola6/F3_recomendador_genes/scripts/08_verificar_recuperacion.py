#!/usr/bin/env python3
"""Verifica en NCBI las accesiones que `recuperacion_6filas.tsv` leyo de los papers (issue #43).

El subagente que leyo los papers no tuvo red hacia NCBI (403 del proxy de su sandbox), asi que
dejo las accesiones sin verificar. Este script hace esa parte: pide el resumen y el FASTA de cada
accesion CITADA EN EL PAPER, comprueba organismo, producto y largo contra lo que el paper dice, y
guarda la secuencia en work/F3_recuperacion/ (no versionada).

No busca nada por nombre de gen ni de especie: solo resuelve accesiones que ya estan en el texto.

Uso: python research/ola6/F3_recomendador_genes/scripts/08_verificar_recuperacion.py
"""
import csv, hashlib, json, sys, time, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1] / "resultados"
W = RAIZ / "work/F3_recuperacion"
EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

# (fila, accesion citada en el paper, organismo esperado segun el paper, palabra de producto esperada,
#  largo que declara el paper o None). Todo sale de recuperacion_6filas.tsv y de los papers.
ESPERADO = [
    ("DE-01", "KC473163", "Peregrinus maidis", "V-ATPase B", 2495),
    ("DE-01", "KC473162", "Peregrinus maidis", "V-ATPase D", 985),
    ("CI-13", "MN815919", "Nephotettix cincticeps", "Hig", 1911),
    ("DE-06", "PZ371509", "Delphacodes kuscheli", "ecdysis triggering hormone", None),
    ("DE-06", "PZ371510", "Delphacodes kuscheli", "bursicon alpha", None),
]


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read().decode()


def main():
    W.mkdir(parents=True, exist_ok=True)
    ids = ",".join(a for _, a, *_ in ESPERADO)
    res = json.loads(get(EU + "esummary.fcgi?db=nuccore&retmode=json&id=" + ids))["result"]
    por_acc = {res[u]["caption"]: res[u] for u in res["uids"]}
    # la referencia de cada paper sale de referencias_recuperacion.tsv (script 09, Europe PMC), no de memoria
    with open(OUT / "referencias_recuperacion.tsv", encoding="utf-8") as fh:
        REF = {r["fila"]: r for r in csv.DictReader(fh, delimiter="\t")}
    filas = []
    for fila, acc, org, prod, largo_paper in ESPERADO:
        r = por_acc[acc]
        time.sleep(0.4)
        fa = get(EU + f"efetch.fcgi?db=nuccore&rettype=fasta&retmode=text&id={r['accessionversion']}")
        seq = "".join(l.strip() for l in fa.splitlines() if not l.startswith(">")).upper()
        (W / f"{fila}_{acc}.fasta").write_text(fa)
        assert len(seq) == r["slen"], (acc, len(seq), r["slen"])
        ok_org = org.lower() == r["organism"].lower()
        ok_prod = prod.lower() in r["title"].lower()
        filas.append({
            "id": fila, "accesion": r["accessionversion"], "organismo_ncbi": r["organism"],
            "organismo_coincide": "si" if ok_org else "NO", "producto_ncbi": r["title"],
            "producto_coincide": "si" if ok_prod else "NO", "moltype": r["moltype"],
            "largo_nt_ncbi": len(seq), "largo_nt_que_declara_el_paper": largo_paper if largo_paper else "",
            "diferencia_con_el_paper": (len(seq) - largo_paper) if largo_paper else "",
            "sha256_secuencia": hashlib.sha256(seq.encode()).hexdigest(),
            "paper": f"{REF[fila]['autores']} ({REF[fila]['anio']}) {REF[fila]['revista']} {REF[fila]['volumen']}:{REF[fila]['paginas']}",
            "paper_doi": REF[fila]["doi"], "paper_pmid": REF[fila]["pmid"], "paper_pmcid": REF[fila]["pmcid"],
        })
    with open(OUT / "recuperacion_6filas_verificacion.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]), delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(filas)
    for f in filas:
        print(f["id"], f["accesion"], f["organismo_ncbi"], f["organismo_coincide"], f["producto_coincide"],
              f["largo_nt_ncbi"], "paper:", f["largo_nt_que_declara_el_paper"], f["diferencia_con_el_paper"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
