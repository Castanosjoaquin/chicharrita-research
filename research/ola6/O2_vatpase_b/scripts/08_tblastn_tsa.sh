#!/usr/bin/env bash
# O2 paso 8 — la via de `tblastn` que el issue #22 pedia y que se cerro con `miniprot`.
#
# Por que existe. #22 se cerro usando `miniprot` porque «no habia BLAST+ en ninguna de las
# dos maquinas». La entrada 54 de `PREGUNTAS_ABIERTAS.md` midio que eso era falso: hay
# BLAST+ 2.17.0 en la maquina de Joaquin, en los entornos de `micromamba` sin activar. Esta
# corrida **no corrige** ningun numero de §2 a §5: agrega el del otro algoritmo. Los dos
# resuelven proteina contra nucleotido con intrones y sus identidades **no son
# intercambiables** `[?]`: `miniprot` alinea con modelo de splicing sobre el genoma y
# `tblastn` alinea bloques sin intron sobre transcriptos ya ensamblados.
#
# Ambito: `tblastn` contra referencias de ARN encuentra **transcriptos, no genes**. Una
# ausencia aca es ausencia en el transcriptoma publicado, no en el genoma (nota de alcance
# de #32).
#
# Uso (desde la raiz del repo, entorno w5bio): bash research/ola6/O2_vatpase_b/scripts/08_tblastn_tsa.sh
# Entradas: work/C11/db_{GCWP01,GHCC01,GITV01}.* (las bases ya construidas por C11),
#           consultas/consultas_vatpase.faa (las cinco proteinas de referencia)
# Salidas:  resultados/tblastn_tsa.tsv, resultados/tblastn_tsa_version.txt
set -euo pipefail
O2="research/ola6/O2_vatpase_b"
R="$O2/resultados"
Q="$O2/consultas/consultas_vatpase.faa"
mkdir -p "$R"

tblastn -version > "$R/tblastn_tsa_version.txt"

# Las bases son las de `work/C11/`, que es lo que el issue pide: no se reconstruyen, para
# que la corrida consulte el mismo indice que ya esta publicado y no uno nuevo.
: > "$R/tblastn_tsa.tsv"
for p in GCWP01 GHCC01 GITV01; do
  tblastn -query "$Q" -db "work/C11/db_$p" \
          -evalue 1e-30 -max_target_seqs 5 \
          -outfmt "6 qseqid sseqid pident length qlen qstart qend sstart send evalue bitscore" \
    | awk -v tsa="$p" 'BEGIN{OFS="\t"}{print tsa, $0}' >> "$R/tblastn_tsa.tsv"
done

# La cabecera se agrega al final para que el bucle pueda concatenar sin cuidarla.
printf 'tsa\tqseqid\tsseqid\tpident\tlength\tqlen\tqstart\tqend\tsstart\tsend\tevalue\tbitscore\n' \
  | cat - "$R/tblastn_tsa.tsv" > "$R/.tmp" && mv "$R/.tmp" "$R/tblastn_tsa.tsv"

echo "filas: $(( $(wc -l < "$R/tblastn_tsa.tsv") - 1 ))"
