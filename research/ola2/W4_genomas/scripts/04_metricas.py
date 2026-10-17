#!/usr/bin/env python3
"""W4 - metricas basicas de FASTA y de GFF3, calculadas localmente.

Uso:  python3 04_metricas.py fasta <archivo.fna> [--etiqueta NOMBRE]
      python3 04_metricas.py prot  <archivo.faa> [--etiqueta NOMBRE]
      python3 04_metricas.py gff   <archivo.gff>  [--etiqueta NOMBRE]
Imprime un objeto JSON por linea. Lee gzip o texto plano, en una sola pasada.

FASTA: numero de secuencias, largo total, minimo/maximo/mediana, N50, L50, N90,
       GC sobre bases no ambiguas, conteo de N, conteo de bases ambiguas IUPAC.
GFF3:  conteo por tipo de feature, genes por biotipo, transcriptos por gen,
       largo mediano de gen y de CDS, y numero de secuencias (regiones) distintas.
"""
import gzip, json, sys, statistics as st
from collections import Counter, defaultdict


def abrir(ruta):
    return gzip.open(ruta, "rt") if ruta.endswith(".gz") else open(ruta, "rt")


def metricas_fasta(ruta, alfabeto="nt"):
    largos, gc, at, n_amb, n_n, nseq = [], 0, 0, 0, 0, 0
    largo_actual = 0
    comp = Counter()
    with abrir(ruta) as fh:
        for linea in fh:
            if linea.startswith(">"):
                if nseq:
                    largos.append(largo_actual)
                nseq += 1
                largo_actual = 0
            else:
                s = linea.strip().upper()
                largo_actual += len(s)
                comp.update(s)
    if nseq:
        largos.append(largo_actual)
    gc = comp["G"] + comp["C"]
    at = comp["A"] + comp["T"] + comp["U"]
    n_n = comp["N"]
    n_amb = sum(v for k, v in comp.items() if k not in "ACGTUN")
    total = sum(largos)
    orden = sorted(largos, reverse=True)
    def nx(frac):
        objetivo, acum = total * frac, 0
        for i, L in enumerate(orden, 1):
            acum += L
            if acum >= objetivo:
                return L, i
        return 0, 0
    n50, l50 = nx(0.50)
    n90, l90 = nx(0.90)
    if alfabeto == "aa":
        return {
            "archivo": ruta,
            "alfabeto": "aminoacidos",
            "n_secuencias": nseq,
            "largo_total_aa": total,
            "largo_min_aa": min(largos) if largos else 0,
            "largo_max_aa": max(largos) if largos else 0,
            "largo_mediano_aa": int(st.median(largos)) if largos else 0,
        }
    return {
        "archivo": ruta,
        "alfabeto": "nucleotidos",
        "n_secuencias": nseq,
        "largo_total_bp": total,
        "largo_min_bp": min(largos) if largos else 0,
        "largo_max_bp": max(largos) if largos else 0,
        "largo_mediano_bp": int(st.median(largos)) if largos else 0,
        "N50_bp": n50, "L50": l50, "N90_bp": n90, "L90": l90,
        "GC_pct": round(100 * gc / (gc + at), 3) if (gc + at) else None,
        "n_N": n_n,
        "pct_N": round(100 * n_n / total, 4) if total else None,
        "n_ambiguas_iupac": n_amb,
    }


def metricas_gff(ruta):
    tipos = Counter()
    biotipos = Counter()
    regiones = set()
    largos_gen, largos_cds = [], []
    tx_por_gen = defaultdict(int)
    fuentes = Counter()
    with abrir(ruta) as fh:
        for linea in fh:
            if linea.startswith("#"):
                continue
            c = linea.rstrip("\n").split("\t")
            if len(c) < 9:
                continue
            regiones.add(c[0])
            tipos[c[2]] += 1
            fuentes[c[1]] += 1
            atr = c[8]
            if c[2] == "gene" or c[2] == "pseudogene":
                largos_gen.append(int(c[4]) - int(c[3]) + 1)
                for campo in atr.split(";"):
                    if campo.startswith("gene_biotype="):
                        biotipos[campo.split("=", 1)[1]] += 1
            if c[2] == "CDS":
                largos_cds.append(int(c[4]) - int(c[3]) + 1)
            if c[2] in ("mRNA", "transcript", "ncRNA", "rRNA", "tRNA", "lnc_RNA"):
                padre = [x.split("=", 1)[1] for x in atr.split(";") if x.startswith("Parent=")]
                if padre:
                    tx_por_gen[padre[0]] += 1
    return {
        "archivo": ruta,
        "n_regiones": len(regiones),
        "fuentes": dict(fuentes.most_common(5)),
        "features_por_tipo": dict(tipos.most_common(25)),
        "genes_por_biotipo": dict(biotipos.most_common(20)),
        "n_genes": tipos.get("gene", 0),
        "n_mRNA": tipos.get("mRNA", 0),
        "n_CDS": tipos.get("CDS", 0),
        "n_exon": tipos.get("exon", 0),
        "largo_mediano_gen_bp": int(st.median(largos_gen)) if largos_gen else None,
        "transcriptos_por_gen_medio": round(sum(tx_por_gen.values()) / len(tx_por_gen), 3) if tx_por_gen else None,
    }


if __name__ == "__main__":
    modo, ruta = sys.argv[1], sys.argv[2]
    etiqueta = sys.argv[sys.argv.index("--etiqueta") + 1] if "--etiqueta" in sys.argv else None
    if modo == "fasta":
        res = metricas_fasta(ruta)
    elif modo == "prot":
        res = metricas_fasta(ruta, alfabeto="aa")
    else:
        res = metricas_gff(ruta)
    if etiqueta:
        res = {"etiqueta": etiqueta, **res}
    print(json.dumps(res, ensure_ascii=False))
