#!/usr/bin/env python3
"""O2 paso 7 — junta las salidas de miniprot en una tabla con identidad y cobertura.

Una fila por (consulta, base de busqueda, acierto). `cobertura_pct` es el tramo de la
consulta que el alineamiento cubre, que es lo que distingue un gen completo de un
fragmento: en `GCWP01` la subunidad B sale partida en dos contigs y ninguno la cubre.

Uso: python3 07_tabla.py <dir_O2>
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

BASES = [
    ("genoma_ihDalMaid1.1", "forward_genoma.gff"),
    ("TSA_GCWP01", "tsa_GCWP.gff"),
    ("TSA_GHCC01", "tsa_GHCC.gff"),
    ("TSA_GITV01", "tsa_GITV.gff"),
    ("ARNm_Macrosteles_quadrilineatus", "reciproco_cercano_Macrosteles_quadrilineatus.gff"),
    ("ARNm_Homalodisca_vitripennis", "reciproco_pariente_Homalodisca_vitripennis.gff"),
]
LARGOS = {}


def largos_consultas(o2: Path) -> dict[str, int]:
    out, nombre = {}, None
    for ruta in [o2 / "consultas" / "consultas_vatpase.faa",
                 o2 / "resultados" / "VATPaseB_Dm_prot.faa",
                 o2 / "resultados" / "VATPaseA_Dm_prot.faa",
                 o2 / "resultados" / "VATPaseD_Dm_prot.faa"]:
        for linea in ruta.read_text().splitlines():
            if linea.startswith(">"):
                nombre = linea[1:].split()[0]
                out[nombre] = 0
            elif nombre:
                out[nombre] += len(linea.strip())
    return out


def main() -> None:
    o2 = Path(sys.argv[1])
    res = o2 / "resultados"
    largos = largos_consultas(o2)
    filas = []
    for base, archivo in BASES:
        ruta = res / archivo
        if not ruta.exists():
            continue
        for linea in ruta.read_text().splitlines():
            if linea.startswith("#"):
                continue
            c = linea.split("\t")
            if len(c) < 9 or c[2] != "mRNA":
                continue
            a = c[8]
            consulta, ini_q, fin_q = re.search(r"Target=(\S+) (\d+) (\d+)", a).groups()
            largo = largos.get(consulta)
            cobertura = round(100 * (int(fin_q) - int(ini_q) + 1) / largo, 1) if largo else ""
            filas.append({
                "base": base,
                "consulta": consulta,
                "largo_consulta_aa": largo or "",
                "referencia": c[0],
                "desde": c[3], "hasta": c[4], "hebra": c[6],
                "puntaje": c[5],
                "rango": re.search(r"Rank=(\d+)", a).group(1),
                "identidad": re.search(r"Identity=([\d.]+)", a).group(1),
                "positivos": re.search(r"Positive=([\d.]+)", a).group(1),
                "tramo_consulta": f"{ini_q}-{fin_q}",
                "cobertura_pct": cobertura,
                "corrimiento_marco": "si" if "Frameshift=" in a else "no",
            })
    destino = res / "ortologia_vatpase_b.tsv"
    with destino.open("w", newline="\n", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]), delimiter="\t")
        w.writeheader()
        w.writerows(filas)
    print(f"{len(filas)} filas -> {destino.name}")


if __name__ == "__main__":
    main()
