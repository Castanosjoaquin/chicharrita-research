#!/usr/bin/env bash
# O2 paso 1 — las cuatro proteinas de referencia contra el genoma de D. maidis.
# Corre en WSL (Ubuntu 24.04), con miniprot local y el indice ya construido.
# Uso: bash 01_forward_genoma.sh <dir_del_bloque_O2>
# Entradas: $HOME/yhat/data/genome.mpi (indice de ihDalMaid1.1), consultas/consultas_vatpase.faa
# Salidas:  resultados/forward_genoma.gff, forward_genoma.aln, forward_genoma_trans.faa
set -euo pipefail
O2="${1:?falta el directorio del bloque O2}"
MP="$HOME/yhat/tools/miniprot/miniprot"
IDX="$HOME/yhat/data/genome.mpi"
Q="$O2/consultas/consultas_vatpase.faa"
R="$O2/resultados"
mkdir -p "$R"

"$MP" --version > "$R/version_miniprot.txt"

# --outn 5 y --outs 0.5: se piden los secundarios a proposito, para poder ver si
# el mejor acierto de la subunidad B compite con un paralogo del mismo complejo.
"$MP" -t 8 --gff --outn=5 --outs=0.5 "$IDX" "$Q" > "$R/forward_genoma.gff" 2> "$R/forward_genoma.err"
"$MP" -t 8 --aln --outn=5 --outs=0.5 "$IDX" "$Q" > "$R/forward_genoma.aln" 2>> "$R/forward_genoma.err"
"$MP" -t 8 --trans --outn=5 --outs=0.5 "$IDX" "$Q" > "$R/forward_genoma_trans.faa" 2>> "$R/forward_genoma.err"

echo "gff: $(grep -c mRNA "$R/forward_genoma.gff" || true) mRNA"
tail -3 "$R/forward_genoma.err"
