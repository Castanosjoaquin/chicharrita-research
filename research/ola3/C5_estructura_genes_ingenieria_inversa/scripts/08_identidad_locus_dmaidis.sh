#!/usr/bin/env bash
# C5 / Q3 — Identidad de NUCLEOTIDOS entre el ortologo del cicadelido anotado y el locus
# que el paso 5 recupero en el genoma no anotado de Dalbulus maidis. Sirve para comparar,
# sobre un mismo par de genes, la identidad proteica que devuelve miniprot con la
# identidad de nucleotidos que devuelve BLAST, que es la pregunta del "99 %".
# Requiere seqkit (entorno bioinfo) para recortar el locus y blastn (entorno w5bio) para
# alinear; en esta maquina no conviven, asi que cada bloque se saltea si falta la herramienta.
set -euo pipefail
cd "$(dirname "$0")/../../../.."
G=work/W4/downloads/GCA_975739785.1/ncbi_dataset/data/GCA_975739785.1/GCA_975739785.1_ihDalMaid1.1_genomic.fna
C=work/C5/circuito; O=research/ola3/C5_estructura_genes_ingenieria_inversa/resultados
mkdir -p "$C"

if command -v seqkit > /dev/null; then
  seqkit subseq --chr OZ319707.1 -r 3659542:3665386   "$G" > "$C/dmaidis_locus_OZ319707_3659542_3665386.fa"
  seqkit subseq --chr OZ319708.1 -r 67220266:67221513 "$G" > "$C/dmaidis_locus_OZ319708_67220266_67221513.fa"
else
  echo "seqkit no esta en este entorno: correr este bloque en el entorno que lo tiene (bioinfo)."
fi

python3 - <<'PY'
from pathlib import Path
nom, buf, out = None, [], {}
for l in Path("work/W4/downloads/GCF_028750875.1/ncbi_dataset/data/GCF_028750875.1/rna.fna").read_text().splitlines():
    if l.startswith(">"):
        if nom: out[nom] = "".join(buf)
        nom, buf = l[1:].split()[0], []
    else: buf.append(l.strip())
if nom: out[nom] = "".join(buf)
with open("work/C5/circuito/ortologos_mq.fa", "w") as fh:
    for a in ("XM_054426723.1", "XM_054432574.1"):   # por homologia / por nombre
        fh.write(f">{a}\n{out[a]}\n")
PY

if command -v blastn > /dev/null; then
  F="6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore"
  {
    echo "# Identidad de NUCLEOTIDOS del ortologo contra el locus recuperado en Dalbulus maidis"
    echo "# consulta: transcrito del cicadelido anotado; sujeto: la region del genoma ihDalMaid1.1 que miniprot devolvio"
    echo "# columnas: $F"
    echo "## XM_054426723.1 (Rpn6/PSMD6, elegido por homologia) vs OZ319707.1:3659542-3665386"
    blastn -task dc-megablast -query "$C/ortologos_mq.fa" \
      -subject "$C/dmaidis_locus_OZ319707_3659542_3665386.fa" -outfmt "$F" -evalue 1e-5
    echo "## XM_054432574.1 (PSMD11, elegido por nombre) vs OZ319708.1:67220266-67221513"
    blastn -task dc-megablast -query "$C/ortologos_mq.fa" \
      -subject "$C/dmaidis_locus_OZ319708_67220266_67221513.fa" -outfmt "$F" -evalue 1e-5
  } > "$O/ortologos_vs_locus_dmaidis.tsv"
  cat "$O/ortologos_vs_locus_dmaidis.tsv"
else
  echo "blastn no esta en este entorno: correr este bloque en el entorno que lo tiene (w5bio)."
fi
