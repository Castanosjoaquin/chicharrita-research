"""Deja una sola proteina por gen de Tribolium castaneum (la isoforma mas larga).

OGS3 trae 18.536 proteinas para 16.593 genes TC. Mapear todas las isoformas
multiplica loci que son el mismo gen. Nos quedamos con la mas larga por gen y
reescribimos el header a solo el identificador TC, que es el que engancha con
los fenotipos de iBeetle.

Uso:
    python3 preparar_proteoma_tcas.py entrada.fasta.gz salida.faa
"""

from __future__ import annotations

import gzip
import re
import sys
from pathlib import Path

RE_TC = re.compile(r"(TC\d+)")


def leer_fasta(ruta: Path):
    """Itera (header, secuencia) sobre un FASTA, con o sin gzip."""
    abrir = gzip.open if ruta.suffix == ".gz" else open
    header = None
    partes: list[str] = []
    with abrir(ruta, "rt") as f:
        for linea in f:
            linea = linea.rstrip("\n")
            if linea.startswith(">"):
                if header is not None:
                    yield header, "".join(partes)
                header = linea[1:]
                partes = []
            else:
                partes.append(linea)
    if header is not None:
        yield header, "".join(partes)


def main() -> int:
    entrada = Path(sys.argv[1])
    salida = Path(sys.argv[2])

    mejor: dict[str, tuple[int, str]] = {}
    total = 0
    sin_id = 0
    for header, seq in leer_fasta(entrada):
        total += 1
        m = RE_TC.search(header)
        if not m:
            sin_id += 1
            continue
        gen = m.group(1)
        # El '*' final de stop no cuenta como aminoacido util para miniprot.
        seq = seq.rstrip("*")
        if gen not in mejor or len(seq) > mejor[gen][0]:
            mejor[gen] = (len(seq), seq)

    with salida.open("w") as f:
        for gen in sorted(mejor):
            f.write(f">{gen}\n")
            seq = mejor[gen][1]
            for i in range(0, len(seq), 60):
                f.write(seq[i : i + 60] + "\n")

    print(f"proteinas leidas: {total}")
    print(f"sin identificador TC: {sin_id}")
    print(f"genes escritos: {len(mejor)}")
    print(f"salida: {salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
