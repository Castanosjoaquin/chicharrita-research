#!/usr/bin/env bash
# Chequea integridad de los .gz bajados. Una descarga truncada hace fallar el escaneo.
cd "$HOME/yhat/data" || exit 1
malos=0
for f in *.fna.gz; do
  if gzip -t "$f" 2>/dev/null; then
    echo "ok  $f  $(stat -c %s "$f") bytes"
  else
    echo "CORRUPTO  $f  $(stat -c %s "$f") bytes"
    malos=$((malos+1))
  fi
done
echo "corruptos: $malos"
