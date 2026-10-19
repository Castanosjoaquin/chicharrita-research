#!/usr/bin/env bash
# Baja los datos publicos de iBeetle-Base (cribado de RNAi en Tribolium castaneum)
# y el proteoma OGS3. Todo va a un directorio propio, separado de los scripts.
#
# Uso:  bash pipeline/bajar_ibeetle.sh
set -u

DEST="$HOME/yhat/data/ibeetle"
mkdir -p "$DEST"

BASE="https://ibeetle-base.uni-goettingen.de/download"

bajar() {
  url="$1"
  nombre="$2"
  echo "--- $nombre"
  curl -sS -L --retry 3 --fail -o "$DEST/$nombre" "$url"
  echo "    $(stat -c %s "$DEST/$nombre" 2>/dev/null || echo 0) bytes"
}

bajar "$BASE/phenotypes/iBeetle_lethality.csv"            iBeetle_lethality.csv
bajar "$BASE/phenotypes/iBeetle_grouped_phenotypes.ndjson" iBeetle_grouped_phenotypes.ndjson
bajar "$BASE/phenotypes/iB_TC.csv"                         iB_TC.csv
bajar "$BASE/phenotypes/iB_sequence.csv"                   iB_sequence.csv
bajar "$BASE/orthology/1.OrthoFinder_orthology.tsv"        OrthoFinder_orthology.tsv
bajar "$BASE/orthology/2.Eggnog6_orthology.tsv"            Eggnog6_orthology.tsv
bajar "$BASE/species/Tcas/OGS3_proteins.fasta.gz"          OGS3_proteins.fasta.gz

echo "=== listado ==="
ls -la "$DEST"
