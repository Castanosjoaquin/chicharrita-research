#!/usr/bin/env bash
# O2 paso 5 — la via que pedia el issue: las proteinas de referencia contra los TRES
# transcriptomas publicos de D. maidis (TSA GCWP01, GHCC01, GITV01), a nivel proteina.
# Los tres archivos se bajan del FTP del GenBank; no se sube ninguna secuencia a nada.
#   https://ftp.ncbi.nlm.nih.gov/genbank/tsa/G/tsa.{GCWP,GHCC,GITV}.1.fsa_nt.gz
# Uso: bash 05_tsa_publicos.sh <dir_O2> [dir_con_los_tsa]
set -euo pipefail
O2="${1:?falta el directorio del bloque O2}"
TSA="${2:-$HOME/yhat/o2_tsa}"
MP="$HOME/yhat/tools/miniprot/miniprot"
R="$O2/resultados"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT

# la consulta incluye la proteina predicha en el propio D. maidis: si el transcriptoma
# tuviera el transcripto, con esa consulta tiene que salir casi perfecto.
cat "$O2/consultas/consultas_vatpase.faa" "$R/VATPaseB_Dm_prot.faa" > "$T/q.faa"

for p in GCWP GHCC GITV; do
  zcat "$TSA/tsa.$p.1.fsa_nt.gz" > "$T/ref.fna"
  "$MP" -t 8 --gff --outn=5 --outs=0.5 "$T/ref.fna" "$T/q.faa" \
      > "$R/tsa_$p.gff" 2> "$R/tsa_$p.err"
  awk -F'\t' -v p="$p" '$3=="mRNA"{print p"\t"$1"\t"$4"\t"$5"\t"$7"\t"$6"\t"$9}' "$R/tsa_$p.gff"
  echo "$p: $(awk -F'\t' '$3=="mRNA"' "$R/tsa_$p.gff" | wc -l) aciertos de 6 consultas"
done
