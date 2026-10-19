"""Resume un GFF de miniprot: un renglon por locus, con las metricas que importan.

Uso:
    python3 resumir_miniprot.py <archivo.gff> [--csv salida.csv]

Lo que reporta por alineamiento:
  proteina, cromosoma, inicio, fin, largo del locus, hebra, exones,
  identidad, positivos, cobertura de la proteina, frameshifts, stops internos, rank.

El "rank" es clave: rank 0 es el mejor alineamiento de esa proteina. Un rank 1 o mas
con score parecido es senal de parálogo o de duplicacion, no de ortologo limpio.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path


def atributos(campo: str) -> dict[str, str]:
    salida = {}
    for par in campo.rstrip(";").split(";"):
        if "=" in par:
            clave, _, valor = par.partition("=")
            salida[clave] = valor
    return salida


def parsear(ruta: Path) -> list[dict]:
    loci: list[dict] = []
    exones: dict[str, int] = defaultdict(int)

    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if linea.startswith("#") or linea.startswith("##PAF") or not linea.strip():
            continue
        campos = linea.split("\t")
        if len(campos) < 9:
            continue
        if campos[2] == "CDS":
            exones[atributos(campos[8]).get("Parent", "")] += 1
        elif campos[2] == "mRNA":
            attr = atributos(campos[8])
            objetivo = attr.get("Target", "")
            m = re.match(r"(\S+)\s+(\d+)\s+(\d+)", objetivo)
            prot, ini_p, fin_p = (m.group(1), int(m.group(2)), int(m.group(3))) if m else (objetivo, 0, 0)
            loci.append({
                "id": attr.get("ID", ""),
                "proteina": prot.split("|")[-1] if "|" in prot else prot,
                "cromosoma": campos[0],
                "inicio": int(campos[3]),
                "fin": int(campos[4]),
                "largo_locus": int(campos[4]) - int(campos[3]) + 1,
                "hebra": campos[6],
                "score": int(campos[5]) if campos[5] not in (".", "") else 0,
                "identidad": float(attr.get("Identity", 0)),
                "positivos": float(attr.get("Positive", 0)),
                "frameshift": int(attr.get("Frameshift", 0)),
                "stop_interno": int(attr.get("StopCodon", 0)),
                "rank": int(attr.get("Rank", -1)),
                "prot_desde": ini_p,
                "prot_hasta": fin_p,
            })

    for loc in loci:
        loc["exones"] = exones.get(loc["id"], 0)
    return loci


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ruta = Path(sys.argv[1])
    loci = parsear(ruta)

    por_prot = defaultdict(list)
    for loc in loci:
        por_prot[loc["proteina"]].append(loc)

    limpios = 0
    print(f"{'proteina':<16}{'ubicacion':<34}{'kb':>7}{'ex':>5}{'ident':>8}{'posit':>8}{'fs':>4}{'st':>4}{'hits':>6}")
    print("-" * 92)
    for prot, hits in sorted(por_prot.items()):
        mejor = max(hits, key=lambda h: h["score"])
        ubic = f"{mejor['cromosoma']}:{mejor['inicio']}-{mejor['fin']}({mejor['hebra']})"
        kb = mejor["largo_locus"] / 1000
        if mejor["frameshift"] == 0 and mejor["stop_interno"] == 0:
            limpios += 1
        print(f"{prot:<16}{ubic:<34}{kb:>7.1f}{mejor['exones']:>5}"
              f"{mejor['identidad']:>8.3f}{mejor['positivos']:>8.3f}"
              f"{mejor['frameshift']:>4}{mejor['stop_interno']:>4}{len(hits):>6}")

    print("-" * 92)
    print(f"proteinas con al menos un locus : {len(por_prot)}")
    print(f"alineamientos totales           : {len(loci)}")
    print(f"loci sin frameshift ni stop     : {limpios} ({limpios/max(len(por_prot),1)*100:.1f} %)")

    if "--csv" in sys.argv:
        destino = Path(sys.argv[sys.argv.index("--csv") + 1])
        with destino.open("w", newline="", encoding="utf-8") as fh:
            escritor = csv.DictWriter(fh, fieldnames=list(loci[0].keys()))
            escritor.writeheader()
            escritor.writerows(loci)
        print(f"csv escrito en {destino}")


if __name__ == "__main__":
    main()
