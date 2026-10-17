#!/usr/bin/env python3
"""W4 - consultas a E-utilities del NCBI (conteos y metadatos, sin subir secuencias).

Uso: python3 03_eutils_consultas.py <salida.json>
"""
import json, sys, time, requests, xml.etree.ElementTree as ET

E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

CONSULTAS = {
    "sra_dmaidis_total":        ("sra", '"Dalbulus maidis"[Organism]'),
    "sra_dmaidis_rnaseq":       ("sra", '"Dalbulus maidis"[Organism] AND "rna seq"[Strategy]'),
    "sra_dmaidis_wgs":          ("sra", '"Dalbulus maidis"[Organism] AND "wgs"[Strategy]'),
    "tsa_dmaidis":              ("nucleotide", '"Dalbulus maidis"[Organism] AND TSA[Division]'),
    "nuc_dmaidis_total":        ("nucleotide", '"Dalbulus maidis"[Organism]'),
    "nuc_dmaidis_mrna":         ("nucleotide", '"Dalbulus maidis"[Organism] AND biomol_mrna[PROP]'),
    "prot_dmaidis":             ("protein",    '"Dalbulus maidis"[Organism]'),
    "sra_skunkelii":            ("sra", '"Spiroplasma kunkelii"[Organism]'),
    "tsa_cicadellidae":         ("nucleotide", 'Cicadellidae[Organism] AND TSA[Division]'),
}

def pedir(endpoint, params, intentos=6):
    """GET con reintentos y espera creciente: E-utilities limita a 3 pedidos por segundo."""
    for i in range(intentos):
        r = requests.get(f"{E}/{endpoint}", params=params, timeout=300)
        if r.status_code == 429:
            time.sleep(2 * (i + 1))
            continue
        r.raise_for_status()
        return r
    r.raise_for_status()

def esearch(db, term, retmax=0):
    r = pedir("esearch.fcgi", {"db": db, "term": term, "retmax": retmax, "retmode": "json"})
    d = r.json()["esearchresult"]
    return int(d["count"]), d.get("idlist", [])

def runinfo(term):
    """Metadatos por corrida de SRA (csv) para un termino de busqueda."""
    ids = esearch("sra", term, retmax=500)[1]
    if not ids:
        return []
    r = pedir("efetch.fcgi", {"db": "sra", "id": ",".join(ids), "rettype": "runinfo", "retmode": "text"})
    lineas = [l for l in r.text.splitlines() if l.strip()]
    if not lineas:
        return []
    cab = lineas[0].split(",")
    filas = []
    for l in lineas[1:]:
        c = l.split(",")
        if len(c) == len(cab):
            filas.append(dict(zip(cab, c)))
    return filas

def accesiones(accs):
    """Verifica que existan accesiones de nucleotido y devuelve titulo y largo."""
    r = pedir("esummary.fcgi", {"db": "nucleotide", "id": ",".join(accs), "retmode": "json"})
    d = r.json()["result"]
    return {d[u]["caption"]: {"titulo": d[u]["title"], "largo": d[u]["slen"],
                              "organismo": d[u].get("organism"), "fecha": d[u].get("updatedate")}
            for u in d.get("uids", [])}

def main(dest):
    res = {"conteos": {}}
    for k, (db, term) in CONSULTAS.items():
        n, _ = esearch(db, term)
        res["conteos"][k] = {"db": db, "term": term, "count": n}
        print(f"{k:26s} {n}")
        time.sleep(1.2)
    res["sra_dmaidis_runinfo"] = runinfo('"Dalbulus maidis"[Organism]')
    print("corridas SRA detalladas:", len(res["sra_dmaidis_runinfo"]))
    res["accesiones_andrada2026"] = accesiones(["PZ371507", "PZ371508", "PZ371509", "PZ371510"])
    print("accesiones eth/burs:", list(res["accesiones_andrada2026"]))
    with open(dest, "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "eutils.json")
