#!/usr/bin/env bash
# Mapea el proteoma de Tribolium castaneum (OGS3) al genoma de D. maidis.
set -u
cd "$HOME/yhat/data"
/usr/bin/time -v "$HOME/yhat/tools/miniprot/miniprot" -t 16 --gff genome.mpi tcas_ogs3.faa > tcas.gff 2> tcas.err
echo "gff: $(wc -l < tcas.gff) lineas"
tail -20 tcas.err
