#!/usr/bin/env bash
# O2 paso 3 — la vuelta: la proteina predicha de D. maidis contra los transcriptomas
# anotados de dos cicadelidos parientes. La ortologia se da por buena solo si el mejor
# acierto de la vuelta es el ARNm de la misma subunidad del que salio la ida.
# Uso: bash 03_reciproco.sh <dir_O2>
set -euo pipefail
O2="${1:?falta el directorio del bloque O2}"
MP="$HOME/yhat/tools/miniprot/miniprot"
D="$HOME/yhat/data"
R="$O2/resultados"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT

cat "$R"/VATPaseB_Dm_prot.faa "$R"/VATPaseA_Dm_prot.faa "$R"/VATPaseD_Dm_prot.faa > "$T/vuelta.faa"

for par in cercano_Macrosteles_quadrilineatus:cicadelido_cercano_rna \
           pariente_Homalodisca_vitripennis:cicadelido_pariente_rna; do
  etiqueta="${par%%:*}"; archivo="${par##*:}"
  zcat "$D/$archivo.fna.gz" > "$T/ref.fna"
  "$MP" -t 8 --gff --outn=5 --outs=0.3 "$T/ref.fna" "$T/vuelta.faa" \
      > "$R/reciproco_$etiqueta.gff" 2> "$R/reciproco_$etiqueta.err"
  # defline completa de cada transcripto con acierto, para poder leer el nombre del gen
  grep -oE "^[A-Za-z0-9_.]+" <(awk -F'\t' '$3=="mRNA"{print $1}' "$R/reciproco_$etiqueta.gff") \
      | sort -u > "$T/ids.txt"
  grep -F -f "$T/ids.txt" <(grep "^>" "$T/ref.fna") > "$R/reciproco_${etiqueta}_deflines.txt" || true
  echo "$etiqueta: $(awk -F'\t' '$3=="mRNA"' "$R/reciproco_$etiqueta.gff" | wc -l) aciertos"
done
