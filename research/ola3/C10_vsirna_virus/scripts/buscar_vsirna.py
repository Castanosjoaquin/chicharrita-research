"""Busca datos publicados de ARN pequeños derivados de virus para nuestro blanco.

Pregunta: existe un mapa empirico de que ventanas del genoma viral corta el
hospedador, que sirva como verificacion externa del criterio de accesibilidad?

No sube ninguna secuencia: consulta por nombre de organismo y de virus.

Uso (desde la raiz del repositorio):
    python research/ola3/C10_vsirna_virus/scripts/buscar_vsirna.py
"""
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

SALIDA = Path(__file__).resolve().parents[1] / "datos"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"

CONSULTAS_EPMC = {
    "MRFV_srna": '("Maize rayado fino virus") AND (siRNA OR "small RNA" OR sRNA)',
    "MRFV_any": '("Maize rayado fino virus")',
    "marafi_srna": '(marafivirus OR Marafivirus) AND ("small RNA" OR siRNA)',
    "tymo_srna": '(Tymoviridae OR tymovirus) AND ("small RNA" OR siRNA OR "small interfering")',
    "dalbulus_srna": '("Dalbulus maidis") AND ("small RNA" OR siRNA OR sRNA OR microRNA)',
    "leafhopper": '(leafhopper OR Cicadellidae) AND ("virus-derived small" OR "vsiRNA" OR "virus-derived siRNA")',
    "maize_vsirna": '(maize OR "Zea mays") AND ("virus-derived siRNA" OR vsiRNA)',
}

CONSULTAS_NCBI = {
    "SRA · MRFV organismo": ("sra", '"Maize rayado fino virus"[Organism]'),
    "SRA · MRFV texto libre": ("sra", '"Maize rayado fino virus"'),
    "SRA · MRFV + ARN pequeno": ("sra", '"Maize rayado fino virus" AND (miRNA-Seq[Strategy] OR ncRNA-Seq[Strategy])'),
    "SRA · Dalbulus maidis": ("sra", '"Dalbulus maidis"[Organism]'),
    "SRA · Dalbulus + ARN pequeno": ("sra", '"Dalbulus maidis"[Organism] AND (miRNA-Seq[Strategy] OR ncRNA-Seq[Strategy])'),
    "SRA · maiz + ARN pequeno": ("sra", '"Zea mays"[Organism] AND miRNA-Seq[Strategy]'),
    "GEO · MRFV": ("gds", '"Maize rayado fino virus"'),
    "GEO · Dalbulus maidis": ("gds", '"Dalbulus maidis"'),
}


def epmc(q, n=25):
    u = EPMC + urllib.parse.urlencode(
        {"query": q, "format": "json", "pageSize": n, "resultType": "core"})
    d = json.load(urllib.request.urlopen(u, timeout=60))
    return d["hitCount"], d["resultList"]["result"]


def esearch(db, term, n=20):
    u = EUTILS + "esearch.fcgi?" + urllib.parse.urlencode(
        {"db": db, "term": term, "retmax": n, "retmode": "json"})
    d = json.load(urllib.request.urlopen(u, timeout=60))["esearchresult"]
    return int(d["count"]), d.get("idlist", [])


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    lit = {}
    for k, q in CONSULTAS_EPMC.items():
        n, filas = epmc(q)
        lit[k] = {"hits": n, "rows": [
            {"title": r.get("title"), "year": r.get("pubYear"), "doi": r.get("doi"),
             "pmcid": r.get("pmcid"), "oa": r.get("isOpenAccess"),
             "journal": (r.get("journalInfo") or {}).get("journal", {}).get("title")}
            for r in filas]}
        print("%7d  %s" % (n, k))
        time.sleep(0.3)
    (SALIDA / "epmc_vsirna.json").write_text(json.dumps(lit, indent=1), encoding="utf-8")

    cuentas = {}
    for etiqueta, (db, term) in CONSULTAS_NCBI.items():
        n, _ = esearch(db, term)
        cuentas[etiqueta] = n
        print("%7d  %s" % (n, etiqueta))
        time.sleep(0.4)
    (SALIDA / "ncbi_srna_busqueda.json").write_text(json.dumps(cuentas, indent=1), encoding="utf-8")
    print("\nescrito en", SALIDA)


if __name__ == "__main__":
    main()
