"""Eje 3 de F3 (issue #43): ¿hay secuencias de GenBank enlazadas a los papers fuente de las filas sin ventanas?

Para cada PMID citado por el catálogo de C5 en una fila sin `ventanas_21nt`, pregunta a E-utilities (elink,
pubmed -> nuccore y pubmed -> protein, vía curl: el Python del sistema no trae certificados) cuántos registros el depositante enlazó al paper. Solo tráfico público: no
sube ninguna secuencia. Salida: resultados/eje3_enlaces_genbank_por_paper.tsv
"""
import json, subprocess, time
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
PMIDS = {  # fila(s) del catálogo -> PMID, tal como los cita catalogo_genes_blanco.json
    "DM-01": 35442515, "DM-04": 37945254, "CI-04,CI-05": 30417535, "CI-06": 33253714,
    "CI-07": 36750707, "CI-07,CI-08": 41401619, "CI-09": 39616656, "CI-11": 31328822,
    "CI-12": 26728387, "CI-13": 32362876, "DE-03": 38635824, "DE-04": 36912710,
}

def get(url):
    for _ in range(3):
        try:
            return json.loads(subprocess.run(["curl", "-fsS", "-m", "25", url], capture_output=True, check=True, text=True).stdout)
        except Exception:
            time.sleep(1.5)
    return None

filas = ["filas\tpmid\tnuccore_enlazados\tprotein_enlazados\tconsulta_ok"]
for k, p in PMIDS.items():
    n, ok = [], True
    for db in ("nuccore", "protein"):
        j = get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db={db}&id={p}&retmode=json")
        ok &= j is not None
        n.append(sum(len(l["links"]) for ls in (j or {"linksets": []})["linksets"] for l in ls.get("linksetdbs", [])))
        time.sleep(0.4)
    filas.append(f"{k}\t{p}\t{n[0]}\t{n[1]}\t{ok}")
(AQUI / "resultados" / "eje3_enlaces_genbank_por_paper.tsv").write_text("\n".join(filas) + "\n", encoding="utf-8")
print("\n".join(filas))
