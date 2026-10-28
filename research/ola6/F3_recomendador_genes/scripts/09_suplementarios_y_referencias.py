#!/usr/bin/env python3
"""Suplementarios de DE-03 y CI-07, y la referencia completa de cada paper usado (issue #43).

1. Referencias: para cada paper del que se saco algo en la recuperacion, pide a Europe PMC la cita
   (autores, anio, revista, volumen, paginas, DOI, PMID, PMCID). Nada de memoria: si Europe PMC
   no lo devuelve, la celda queda vacia y se dice.
2. DE-03: lee las secuencias del S1 File (DOCX) de Pmtra-2, comprueba que contienen los tres
   cebadores que el propio paper publica en su S1 Table (en la orientacion que sea) y mide el ORF.
   Las secuencias van a work/F3_recuperacion/ (no versionado); aqui solo conteos y sha256.
3. CI-07: deja constancia de que su suplementario es una tabla proteomica, sin secuencias.

Uso: python research/ola6/F3_recomendador_genes/scripts/09_suplementarios_y_referencias.py
"""
import csv, hashlib, json, re, sys, urllib.parse, urllib.request, zipfile
from pathlib import Path
from Bio.Seq import Seq

RAIZ = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1] / "resultados"
W = RAIZ / "work/F3_recuperacion"
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&resultType=core&query="

# fila(s) -> identificador con el que se pide la cita. Salen de `fuente` en el catalogo de C5.
PAPERS = [
    ("DE-01", "DOI:10.1371/journal.pone.0070243"),   # Yao et al. 2013
    ("DE-03", "EXT_ID:38635824 AND SRC:MED"),        # PMID del catalogo
    ("CI-07", "EXT_ID:36750707 AND SRC:MED"),        # PMID del catalogo
    ("CI-13", "EXT_ID:32362876 AND SRC:MED"),        # PMID del catalogo
    ("HE-04", "DOI:10.1371/journal.pone.0171847"),   # Galdeano et al. 2017
    ("DE-06", "DOI:10.3389/finsc.2026.1811933"),     # Andrada et al. 2026
]
COMP = str.maketrans("ACGT", "TGCA")
rc = lambda s: s.translate(COMP)[::-1]


def cita(q):
    d = json.load(urllib.request.urlopen(EPMC + urllib.parse.quote(q), timeout=60))
    r = d["resultList"]["result"]
    if not r:
        return None
    r = r[0]
    return {"autores": r.get("authorString", ""), "anio": r.get("pubYear", ""), "titulo": r.get("title", ""),
            "revista": r.get("journalInfo", {}).get("journal", {}).get("title", r.get("journalTitle", "")),
            "volumen": r.get("journalInfo", {}).get("volume", ""), "numero": r.get("journalInfo", {}).get("issue", ""),
            "paginas": r.get("pageInfo", ""), "doi": r.get("doi", ""), "pmid": r.get("pmid", ""), "pmcid": r.get("pmcid", "")}


def main():
    refs = []
    for fila, q in PAPERS:
        c = cita(q)
        if c is None:
            refs.append({"fila": fila, "consulta": q, "autores": "", "anio": "", "titulo": "", "revista": "", "volumen": "",
                         "numero": "", "paginas": "", "doi": "", "pmid": "", "pmcid": "", "nota": "Europe PMC no lo devolvio"})
        else:
            c.update({"fila": fila, "consulta": q, "nota": ""}); refs.append(c)
    campos = ["fila", "autores", "anio", "titulo", "revista", "volumen", "numero", "paginas", "doi", "pmid", "pmcid", "consulta", "nota"]
    with open(OUT / "referencias_recuperacion.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, delimiter="\t", lineterminator="\n"); w.writeheader(); w.writerows(refs)
    for r in refs:
        print(r["fila"], "|", r["autores"][:50], r["anio"], "|", r["revista"], r["volumen"], r["paginas"], "|", r["doi"], r["pmid"], r["pmcid"], r["nota"])

    # ---- DE-03: S1 File ----
    z = zipfile.ZipFile(W / "suplementarios/PMC11025951/pone.0295335.s002.docx").read("word/document.xml").decode()
    t = re.sub(r"<[^>]+>", "", re.sub(r"</w:p>", "\n", z))
    seqs, cur = {}, None
    for l in t.splitlines():
        l = l.replace("&gt;", ">").strip()
        if l.startswith(">"):
            cur = l[1:]; seqs[cur] = ""
        elif cur and l:
            seqs[cur] += re.sub(r"[^ACGTacgt]", "", l).upper()
    # Los cebadores se LEEN del S1 Table del paper (no se escriben aqui: son rachas de 21 nt y el repo
    # no versiona rachas asi). Primera ronda de PCR de Pmtra-2 = primer par F/R de la tabla; qPCR = el
    # primer F/R despues del encabezado qRT-PCR.
    tz = zipfile.ZipFile(W / "suplementarios/PMC11025951/pone.0295335.s001.docx").read("word/document.xml").decode()
    tt = re.sub(r"<[^>]+>", " ", re.sub(r"</w:p>", "\n", tz)); tt = re.sub(r"\s+", " ", tt)
    antes, despues = tt.split("qRT", 1)   # el guion de "qRT-PCR" no es ASCII en el DOCX
    pcr1 = re.findall(r"\b[FR]: ([ACGT]{15,})", antes)
    pq = re.findall(r"\bF: ([ACGT]{15,})", despues)
    prim = {"PCR1_F": pcr1[0], "PCR1_R": pcr1[1], "qPCR_F": pq[0]}
    (W / "DE-03_S1File.fasta").write_text("".join(f">{k}\n{s}\n" for k, s in seqs.items()))
    filas = []
    for k, s in seqs.items():
        hall = {}
        for n, p in prim.items():
            for q, lab in ((p, "directa"), (rc(p), "inversa")):
                if q in s:
                    hall[n] = lab
        best = max(len(p) for st in (s, rc(s)) for f in range(3)
                   for p in str(Seq(st[f:len(st) - ((len(st) - f) % 3)]).translate()).split("*"))
        filas.append({"fila": "DE-03", "secuencia": k, "largo_nt": len(s), "sha256": hashlib.sha256(s.encode()).hexdigest(),
                      "cebadores_del_paper_hallados": "; ".join(f"{n} ({o})" for n, o in hall.items()) or "ninguno",
                      "orf_mas_largo_aa": best, "origen": "S1 File (pone.0295335.s002.docx); cebadores de S1 Table (pone.0295335.s001.docx)",
                      "accesion_ncbi": "ninguna: el paper no la cita"})
    with open(OUT / "recuperacion_suplementarios.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]), delimiter="\t", lineterminator="\n"); w.writeheader(); w.writerows(filas)
    for f in filas:
        print(f["secuencia"], f["largo_nt"], f["cebadores_del_paper_hallados"], "ORF aa", f["orf_mas_largo_aa"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
