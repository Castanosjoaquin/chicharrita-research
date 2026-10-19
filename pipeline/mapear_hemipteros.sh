#!/usr/bin/env bash
# Mapea los blancos de RNAi de hemipteros al genoma de D. maidis, mismo indice.
set -u
cd "$HOME/yhat/data"
"$HOME/yhat/tools/miniprot/miniprot" -t 16 --gff genome.mpi hemipteros_rnai.faa > hemipteros.gff 2> hemipteros.err
echo "gff: $(wc -l < hemipteros.gff) lineas"
tail -3 hemipteros.err
