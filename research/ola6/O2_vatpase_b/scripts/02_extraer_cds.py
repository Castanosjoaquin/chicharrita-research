#!/usr/bin/env python3
"""O2 paso 2 — extrae el CDS del locus de V-ATPase B del genoma de D. maidis.

Lee los exones CDS del GFF de miniprot, saca el tramo del cromosoma, concatena en
orden de traduccion y **verifica** que la traduccion coincide letra por letra con la
proteina que miniprot predijo (lineas `##STA` de la salida `--trans`). Si no
coincide, aborta: un CDS que no reproduce la proteina predicha no sirve de insumo.

Uso: python3 02_extraer_cds.py <dir_O2> <genoma.fna.gz> <consulta|id_mRNA> <etiqueta>
"""
from __future__ import annotations

import gzip
import sys
from pathlib import Path

CODONES = {}
_B = "TCAG"
_AA = ("FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG")
for i, b1 in enumerate(_B):
    for j, b2 in enumerate(_B):
        for k, b3 in enumerate(_B):
            CODONES[b1 + b2 + b3] = _AA[i * 16 + j * 4 + k]

COMP = str.maketrans("ACGTacgtNn", "TGCAtgcaNn")


def traducir(nt: str) -> str:
    nt = nt.upper()
    return "".join(CODONES.get(nt[i:i + 3], "X") for i in range(0, len(nt) - 2, 3))


def exones(gff: Path, mrna: str):
    filas = []
    contig = hebra = None
    for linea in gff.read_text().splitlines():
        if linea.startswith("#"):
            continue
        c = linea.split("\t")
        if len(c) < 9 or c[2] != "CDS" or f"Parent={mrna};" not in c[8] + ";":
            continue
        contig, hebra = c[0], c[6]
        filas.append((int(c[3]), int(c[4])))
    if not filas:
        sys.exit(f"sin exones CDS para {mrna}")
    filas.sort(reverse=(hebra == "-"))
    return contig, hebra, filas


def leer_contig(fasta_gz: Path, contig: str) -> str:
    trozos, dentro = [], False
    with gzip.open(fasta_gz, "rt") as fh:
        for linea in fh:
            if linea.startswith(">"):
                if dentro:
                    break
                dentro = linea[1:].split()[0] == contig
                continue
            if dentro:
                trozos.append(linea.strip())
    if not trozos:
        sys.exit(f"contig {contig} no esta en {fasta_gz}")
    return "".join(trozos)


def proteina_predicha(trans: Path, consulta: str) -> str:
    anterior = ""
    for linea in trans.read_text().splitlines():
        if linea.startswith("##STA\t"):
            if anterior.split("\t")[0] == consulta:
                return linea.split("\t")[1].rstrip("*")
        else:
            anterior = linea
    sys.exit(f"sin linea ##STA para {consulta}")


def resolver(gff: Path, clave: str) -> str:
    """Acepta el ID de miniprot (MP000002) o la accesion de la consulta."""
    for linea in gff.read_text().splitlines():
        if "	mRNA	" not in linea:
            continue
        attr = linea.split("	")[8]
        ident = attr.split("ID=")[1].split(";")[0]
        blanco = attr.split("Target=")[1].split()[0]
        if clave in (ident, blanco) and ";Rank=1;" in attr:
            return ident
    sys.exit(f"no hay mRNA de rango 1 para {clave}")


def main() -> None:
    o2, genoma, clave, etiqueta = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
    res = o2 / "resultados"
    gff = res / "forward_genoma.gff"
    mrna = resolver(gff, clave)
    contig, hebra, filas = exones(gff, mrna)
    consulta = [l.split("Target=")[1].split()[0] for l in gff.read_text().splitlines()
                if f"ID={mrna};" in l][0]
    seq = leer_contig(genoma, contig)

    piezas = []
    for ini, fin in filas:
        tramo = seq[ini - 1:fin]
        if hebra == "-":
            tramo = tramo.translate(COMP)[::-1]
        piezas.append(tramo)
    cds = "".join(piezas)

    esperada = proteina_predicha(res / "forward_genoma_trans.faa", consulta)
    obtenida = traducir(cds).rstrip("*")
    if obtenida != esperada:
        n = sum(1 for a, b in zip(obtenida, esperada) if a != b)
        sys.exit(f"ABORTA: la traduccion no reproduce la proteina predicha "
                 f"({len(obtenida)} vs {len(esperada)} aa, {n} posiciones distintas)")
    if "*" in obtenida:
        sys.exit("ABORTA: hay codon de parada interno")

    ini_g, fin_g = min(f[0] for f in filas), max(f[1] for f in filas)
    nombre = f"{etiqueta}_{contig}_{ini_g}_{fin_g}"
    salida = res / f"{etiqueta}_cds.fna"
    with salida.open("w", newline="\n") as fh:
        fh.write(f">{nombre} CDS predicho por miniprot desde {consulta} | "
                 f"{contig}:{ini_g}-{fin_g}({hebra}) | "
                 f"{len(filas)} exones | {len(cds)} nt | {len(obtenida)} aa\n")
        for i in range(0, len(cds), 70):
            fh.write(cds[i:i + 70] + "\n")
    prot = res / f"{etiqueta}_prot.faa"
    with prot.open("w", newline="\n") as fh:
        fh.write(f">{nombre}_prot traduccion verificada del CDS\n")
        for i in range(0, len(obtenida), 70):
            fh.write(obtenida[i:i + 70] + "\n")
    print(f"OK {nombre}: {len(cds)} nt, {len(obtenida)} aa, {len(filas)} exones, hebra {hebra}")
    print(f"escrito: {salida.name}, {prot.name}")


if __name__ == "__main__":
    main()
