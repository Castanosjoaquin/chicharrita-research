#!/usr/bin/env bash
# C12 validacion A. Comando (raiz del repo, env w5bio): bash research/ola3/C12_validacion_homologia/scripts/01_blast_pares.sh
# BLAST+ 2.17.0, local. Fecha 2026-10-22. Proteomas RefSeq de work/W4/downloads.
set -e
O=work/C12; mkdir -p $O
P=ncbi_dataset/data
MQ=work/W4/downloads/GCF_028750875.1/$P/GCF_028750875.1/protein.faa
HV=work/W4/downloads/GCF_021130785.1/$P/GCF_021130785.1/protein.faa
NL=work/W4/downloads/GCF_014356525.2/$P/GCF_014356525.2/protein.faa
for n in MQ HV NL; do f=${!n}; [ -f $O/$n.psq ] || makeblastdb -in $f -dbtype prot -out $O/$n >/dev/null; done
F="6 qseqid sseqid pident length qlen slen evalue bitscore qcovs"
run(){ blastp -query ${!1} -db $O/$2 -evalue 1e-10 -max_target_seqs 5 -num_threads 10 -outfmt "$F" -out $O/$1_vs_$2.tsv; }
run MQ HV; run HV MQ; run MQ NL; run NL MQ
echo done
