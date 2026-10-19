"""Busca en PubMed papers de RNAi funcional en hemipteros, via E-utilities.

Por que la API y no el buscador web: pubmed.ncbi.nlm.nih.gov sirve un reCAPTCHA
a los navegadores automatizados. E-utilities es la via programatica oficial de
NCBI para esto y no tiene ese problema.

No intenta extraer el fenotipo automaticamente: devuelve titulo y resumen para
que la curacion la haga una persona (o un agente leyendo). La tabla curada vive
aparte, en `rnai_hemipteros.csv`, con una cita por fila.

Uso:
    python3 buscar_rnai_hemipteros.py [--sp "Nilaparvata lugens"] [--max 40]
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

ESPECIES = [
    "Nilaparvata lugens",
    "Bemisia tabaci",
    "Acyrthosiphon pisum",
    "Diaphorina citri",
    "Rhodnius prolixus",
    "Nephotettix cincticeps",
    "Halyomorpha halys",
    "Euschistus heros",
    "Laodelphax striatellus",
    "Sogatella furcifera",
    "Myzus persicae",
    "Dalbulus maidis",
]

# Terminos que apuntan a RNAi FUNCIONAL (hay un fenotipo medido), no a
# descripcion de la maquinaria.
CONSULTA = ('("{sp}"[Organism] OR "{sp}"[Title/Abstract]) AND '
            '(RNAi[Title/Abstract] OR "RNA interference"[Title/Abstract] OR '
            'dsRNA[Title/Abstract] OR siRNA[Title/Abstract]) AND '
            '(mortality[Title/Abstract] OR lethal[Title/Abstract] OR '
            'knockdown[Title/Abstract] OR silencing[Title/Abstract] OR '
            'fecundity[Title/Abstract] OR "gene function"[Title/Abstract])')


def pedir(url: str, intentos: int = 3):
    for i in range(intentos):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            if i == intentos - 1:
                print(f"    fallo: {str(e)[:70]}", file=sys.stderr)
                return ""
            time.sleep(2)
    return ""


def buscar(especie: str, maximo: int) -> list[str]:
    consulta = CONSULTA.format(sp=especie)
    url = (f"{E}esearch.fcgi?db=pubmed&retmode=json&retmax={maximo}"
           f"&sort=relevance&term={urllib.parse.quote(consulta)}")
    crudo = pedir(url)
    if not crudo:
        return []
    try:
        return json.loads(crudo)["esearchresult"]["idlist"]
    except (KeyError, json.JSONDecodeError):
        return []


def resumenes(pmids: list[str]) -> list[dict]:
    """Titulo, revista, anio y resumen de cada PMID, en una sola llamada."""
    if not pmids:
        return []
    url = f"{E}efetch.fcgi?db=pubmed&retmode=xml&id={','.join(pmids)}"
    xml = pedir(url)
    salida = []
    for bloque in xml.split("<PubmedArticle>")[1:]:
        def saca(etiqueta: str) -> str:
            m = re.search(rf"<{etiqueta}[^>]*>(.*?)</{etiqueta}>", bloque, re.S)
            if not m:
                return ""
            txt = re.sub(r"<[^>]+>", " ", m.group(1))
            return re.sub(r"\s+", " ", txt).strip()
        pmid = saca("PMID")
        salida.append({
            "pmid": pmid,
            "anio": saca("Year"),
            "revista": saca("ISOAbbreviation"),
            "titulo": saca("ArticleTitle"),
            "resumen": saca("AbstractText")[:1400],
        })
    return salida


def main() -> int:
    maximo = 25
    if "--max" in sys.argv:
        maximo = int(sys.argv[sys.argv.index("--max") + 1])
    especies = ESPECIES
    if "--sp" in sys.argv:
        especies = [sys.argv[sys.argv.index("--sp") + 1]]

    for especie in especies:
        pmids = buscar(especie, maximo)
        print(f"\n{'#' * 78}")
        print(f"# {especie}: {len(pmids)} resultados")
        print(f"{'#' * 78}")
        for art in resumenes(pmids):
            print(f"\n--- PMID {art['pmid']} · {art['revista']} {art['anio']}")
            print(f"    {art['titulo']}")
            if art["resumen"]:
                print(f"    {art['resumen']}")
        time.sleep(0.5)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
