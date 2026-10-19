"""Baja proteomas de UniProt y los mapea al genoma de D. maidis con miniprot.

Hipotesis que prueba: usar una especie mas cercana a la chicharrita deberia recuperar
mas loci y con mejor identidad que usar Drosophila, que es una mosca.

Homalodisca vitripennis es Cicadellidae, la MISMA FAMILIA que Dalbulus maidis.
Nilaparvata lugens es Hemiptera pero otra familia (Delphacidae).
Drosophila melanogaster es otro orden entero (Diptera). Es la linea de base.

Uso (desde Windows):
    MSYS_NO_PATHCONV=1 wsl -d Ubuntu-24.04 -- python3 /mnt/c/Proyectos/yHat/pipeline/hemip_mapear.py
"""

from __future__ import annotations

import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

DATOS = Path.home() / "yhat" / "data"
MINIPROT = Path.home() / "yhat" / "tools" / "miniprot" / "miniprot"
INDICE = DATOS / "genome.mpi"
HILOS = "20"

ESPECIES = {
    "homalodisca": dict(taxid=197043, nombre="Homalodisca vitripennis", rango="misma familia (Cicadellidae)"),
    "nilaparvata": dict(taxid=108931, nombre="Nilaparvata lugens", rango="mismo orden, otra familia"),
}


def correr(cmd: list[str], salida: Path | None = None) -> float:
    inicio = time.time()
    if salida is None:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    else:
        with salida.open("wb") as fh:
            subprocess.run(cmd, stdout=fh, stderr=subprocess.DEVNULL, check=True)
    return time.time() - inicio


def bajar(clave: str, taxid: int) -> Path:
    destino = DATOS / f"{clave}.faa"
    if destino.exists() and destino.stat().st_size > 1000:
        return destino
    consulta = urllib.parse.urlencode({"query": f"(organism_id:{taxid})", "format": "fasta"})
    url = f"https://rest.uniprot.org/uniprotkb/stream?{consulta}"
    correr(["curl", "-sS", "-o", str(destino), url])
    return destino


def contar_fasta(ruta: Path) -> int:
    return sum(1 for linea in ruta.open(encoding="utf-8", errors="ignore") if linea.startswith(">"))


def main() -> None:
    if not INDICE.exists():
        sys.exit(f"falta el indice: {INDICE}")

    for clave, info in ESPECIES.items():
        faa = bajar(clave, info["taxid"])
        n = contar_fasta(faa)
        if n == 0:
            print(f"{clave:14s} SIN SECUENCIAS en UniProt")
            continue
        gff = DATOS / f"{clave}.gff"
        seg = correr([str(MINIPROT), "-t", HILOS, "--gff", str(INDICE), str(faa)], salida=gff)
        print(f"{clave:14s} {info['rango']:32s} proteinas={n:>6}  mapeo={seg:>6.1f}s  -> {gff.name}")


if __name__ == "__main__":
    main()
