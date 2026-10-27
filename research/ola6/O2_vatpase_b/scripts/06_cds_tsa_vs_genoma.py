#!/usr/bin/env python3
"""O2 paso 6 — el CDS del transcriptoma argentino contra el CDS del genoma.

El contig `GHCC01013224.1` del TSA de Pergamino cubre la proteina entera. Este paso
le saca el CDS con las coordenadas que dio miniprot, verifica que traduce a la misma
proteina, y lo compara nucleotido por nucleotido con el CDS que salio del genoma.
Dos ensamblados independientes de la misma especie: si coinciden, el insumo de `O3`
no depende de cual se use; si no, la diferencia es el dato.

Uso: python3 06_cds_tsa_vs_genoma.py <dir_O2> <tsa.GHCC.1.fsa_nt.gz> <contig>
"""
from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path

CODONES = {}
_B = "TCAG"
_AA = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
for i, b1 in enumerate(_B):
    for j, b2 in enumerate(_B):
        for k, b3 in enumerate(_B):
            CODONES[b1 + b2 + b3] = _AA[i * 16 + j * 4 + k]
COMP = str.maketrans("ACGTacgtNn", "TGCAtgcaNn")


def traducir(nt: str) -> str:
    nt = nt.upper()
    return "".join(CODONES.get(nt[i:i + 3], "X") for i in range(0, len(nt) - 2, 3))


def leer_fasta_un_registro(p: Path, ident: str) -> str:
    trozos, dentro = [], False
    abrir = gzip.open if p.suffix == ".gz" else open
    with abrir(p, "rt") as fh:
        for linea in fh:
            if linea.startswith(">"):
                if dentro:
                    break
                dentro = linea[1:].split()[0] == ident
                continue
            if dentro:
                trozos.append(linea.strip())
    if not trozos:
        sys.exit(f"{ident} no esta en {p}")
    return "".join(trozos)


def exones(gff: Path, contig: str, consulta: str):
    filas, hebra = [], None
    for linea in gff.read_text().splitlines():
        if linea.startswith("#"):
            continue
        c = linea.split("\t")
        if len(c) < 9 or c[2] != "CDS" or c[0] != contig:
            continue
        if f"Target={consulta} " not in c[8]:
            continue
        hebra = c[6]
        filas.append((int(c[3]), int(c[4])))
    if not filas:
        sys.exit(f"sin exones CDS de {consulta} en {contig}")
    filas.sort(reverse=(hebra == "-"))
    return hebra, filas


def main() -> None:
    o2, tsa, contig = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    res = o2 / "resultados"
    prot_gen = "".join(l.strip() for l in
                       (res / "VATPaseB_Dm_prot.faa").read_text().splitlines()[1:] if l.strip())
    consulta = (res / "VATPaseB_Dm_prot.faa").read_text().splitlines()[0][1:].split()[0]

    hebra, filas = exones(res / "tsa_GHCC.gff", contig, consulta)
    seq = leer_fasta_un_registro(tsa, contig)
    piezas = []
    for ini, fin in filas:
        tramo = seq[ini - 1:fin]
        if hebra == "-":
            tramo = tramo.translate(COMP)[::-1]
        piezas.append(tramo)
    cds_tsa = "".join(piezas)
    prot_tsa = traducir(cds_tsa).rstrip("*")
    if "*" in prot_tsa:
        sys.exit("ABORTA: codon de parada interno en el CDS del TSA")

    cds_gen = "".join(l.strip() for l in
                      (res / "VATPaseB_Dm_cds.fna").read_text().splitlines()[1:] if l.strip())

    salida = {
        "contig_tsa": contig,
        "tramo_tsa": f"{min(f[0] for f in filas)}-{max(f[1] for f in filas)}({hebra})",
        "largo_cds_tsa_nt": len(cds_tsa),
        "largo_cds_genoma_nt": len(cds_gen),
        "proteina_tsa_aa": len(prot_tsa),
        "proteina_igual_a_la_del_genoma": prot_tsa == prot_gen,
    }
    if len(cds_tsa) == len(cds_gen):
        dif = [i for i, (a, b) in enumerate(zip(cds_tsa.upper(), cds_gen.upper())) if a != b]
        salida["nt_distintos"] = len(dif)
        salida["identidad_nt_pct"] = round(100 * (len(cds_gen) - len(dif)) / len(cds_gen), 2)
        salida["posiciones_distintas_1based"] = [i + 1 for i in dif[:40]]
    else:
        salida["nt_distintos"] = None
        salida["nota"] = "largos distintos: la comparacion sin huecos no corresponde"

    (res / "cds_tsa_vs_genoma.json").write_text(
        json.dumps(salida, indent=2, ensure_ascii=True) + "\n", newline="\n")
    sal = res / "VATPaseB_Dm_cds_desde_TSA_GHCC.fna"
    with sal.open("w", newline="\n") as fh:
        fh.write(f">VATPaseB_Dm_{contig}_{salida['tramo_tsa']} CDS del TSA de Pergamino | "
                 f"{len(cds_tsa)} nt | {len(prot_tsa)} aa\n")
        for i in range(0, len(cds_tsa), 70):
            fh.write(cds_tsa[i:i + 70] + "\n")
    print(json.dumps(salida, indent=2))


if __name__ == "__main__":
    main()
