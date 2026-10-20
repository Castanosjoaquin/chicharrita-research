#!/usr/bin/env bash
# C5 / Q3 — Cuantos genes recupera el circuito de ingenieria inversa sobre el genoma
# NO ANOTADO de Dalbulus maidis, partiendo del proteoma anotado de un cicadelido.
#
# Insumos locales (bajados del NCBI en W4; nada sale de la maquina):
#   - genoma   : work/W4/downloads/GCA_975739785.1/.../GCA_975739785.1_ihDalMaid1.1_genomic.fna
#   - proteoma : work/W4/downloads/GCF_028750875.1/.../protein.faa  (Macrosteles quadrilineatus)
# Salidas: work/C5/miniprot/  (crudas, pesadas)  + resultados/  (conteos)
set -euo pipefail
cd "$(dirname "$0")/../../../.."          # raiz del repo
G=work/W4/downloads/GCA_975739785.1/ncbi_dataset/data/GCA_975739785.1/GCA_975739785.1_ihDalMaid1.1_genomic.fna
P=work/W4/downloads/GCF_028750875.1/ncbi_dataset/data/GCF_028750875.1/protein.faa
O=work/C5/miniprot
mkdir -p "$O"
echo "miniprot $(miniprot --version)"
[ -f "$O/dmaidis.mpi" ] || /usr/bin/time -l miniprot -t 9 -d "$O/dmaidis.mpi" "$G" 2> "$O/index.time"
/usr/bin/time -l miniprot -t 9 --gff "$O/dmaidis.mpi" "$P" > "$O/macrosteles_vs_dmaidis.gff" 2> "$O/align.time"
wc -l "$O/macrosteles_vs_dmaidis.gff"
