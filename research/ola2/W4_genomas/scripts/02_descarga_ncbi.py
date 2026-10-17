#!/usr/bin/env python3
"""W4 - descarga de ensamblados desde NCBI Datasets v2alpha (API, no servicio web interactivo).

Uso:  python3 02_descarga_ncbi.py <directorio_destino> <accesion> <tipos,separados,por,coma>
Tipos validos: GENOME_FASTA, RNA_FASTA, CDS_FASTA, PROT_FASTA, GENOME_GFF, GENOME_GTF, SEQUENCE_REPORT
Descarga un .zip por accesion y lo descomprime en <destino>/<accesion>/.
"""
import os, sys, zipfile, requests

API = "https://api.ncbi.nlm.nih.gov/datasets/v2alpha"

def descargar(destino, acc, tipos):
    os.makedirs(destino, exist_ok=True)
    zpath = os.path.join(destino, f"{acc}.zip")
    if not os.path.exists(zpath):
        url = f"{API}/genome/accession/{acc}/download"
        params = [("include_annotation_type", t) for t in tipos] + [("filename", f"{acc}.zip")]
        with requests.get(url, params=params, stream=True, timeout=3600) as r:
            r.raise_for_status()
            with open(zpath + ".part", "wb") as fh:
                for chunk in r.iter_content(1 << 22):
                    fh.write(chunk)
        os.replace(zpath + ".part", zpath)
    with zipfile.ZipFile(zpath) as z:
        z.extractall(os.path.join(destino, acc))
    print(f"{acc}\tOK\t{os.path.getsize(zpath)} bytes zip")

if __name__ == "__main__":
    descargar(sys.argv[1], sys.argv[2], sys.argv[3].split(","))
