#!/usr/bin/env bash
# W2 — corridas reales de BLAST+ 2.17.0 (Bioconda, env conda "w2tools"), 17-oct-2026.
# Entradas: sólo secuencias públicas de referencia del NCBI. NINGUNA secuencia de EPILAB.
#   consulta  : PZ371507.1  Dalbulus maidis ecdysis triggering hormone (eth) mRNA, 615 nt
#   base demo : 40 mRNA RefSeq de Zea mays + 40 mRNA RefSeq de Apis mellifera + genoma MRFV NC_002786.2
set -euo pipefail
cd "$(dirname "$0")"
IN=entradas; OUT=salidas; mkdir -p $OUT

# --- E1: construcción de la base de datos -----------------------------------
makeblastdb -in $IN/db_demo_zmays40_amel40_mrfv.fa -dbtype nucl \
  -title "demo_offtarget_W2" -out $OUT/db_demo -parse_seqids > $OUT/E1_makeblastdb.log 2>&1
blastdbcmd -db $OUT/db_demo -info >> $OUT/E1_makeblastdb.log 2>&1

# --- E2: blastn por defecto (task megablast) del mRNA completo --------------
blastn -query $IN/eth_PZ371507.1.fa -db $OUT/db_demo -outfmt 0 -num_threads 2 \
  > $OUT/E2_blastn_megablast_pairwise.txt 2>&1
blastn -query $IN/eth_PZ371507.1.fa -db $OUT/db_demo \
  -outfmt "7 qaccver saccver pident length mismatch gapopen qstart qend sstart send evalue bitscore" \
  -num_threads 2 > $OUT/E2_blastn_megablast.tsv 2>&1

# --- E3: tamizaje por ventanas de 21 nt, condición mayor de dsRNAEngineer ----
# Modelo I = 21 nt con apareamiento perfecto. Equivalente en BLAST+:
blastn -task blastn-short -query $IN/eth_21mers.fa -db $OUT/db_demo \
  -word_size 21 -perc_identity 100 -ungapped -dust no -evalue 1000 -max_target_seqs 5000 \
  -outfmt "6 qaccver saccver pident length mismatch gapopen sstrand evalue bitscore" \
  -num_threads 2 > $OUT/E3_21mers_perfect.tsv 2>&1
# Condición adicional 1 = 16 nt perfecto
blastn -task blastn-short -query $IN/eth_16mers.fa -db $OUT/db_demo \
  -word_size 16 -perc_identity 100 -ungapped -dust no -evalue 1000 -max_target_seqs 5000 \
  -outfmt "6 qaccver saccver pident length mismatch gapopen sstrand evalue bitscore" \
  -num_threads 2 > $OUT/E3_16mers_perfect.tsv 2>&1
# Condición adicional 2 = 26 nt con 0-2 desapareamientos (>=24/26 identidades)
blastn -task blastn-short -query $IN/eth_26mers.fa -db $OUT/db_demo \
  -word_size 11 -perc_identity 92 -ungapped -dust no -evalue 1000 -max_target_seqs 5000 \
  -outfmt "6 qaccver saccver pident length mismatch gapopen sstrand evalue bitscore" \
  -num_threads 2 > $OUT/E3_26mers_2mm.tsv 2>&1

# --- E4: sensibilidad a los umbrales (mismo set de 21-meros) ----------------
for PI in 100 95 90; do
  for WS in 21 11 7; do
    N=$(blastn -task blastn-short -query $IN/eth_21mers.fa -db $OUT/db_demo \
        -word_size $WS -perc_identity $PI -ungapped -dust no -evalue 1000 -max_target_seqs 5000 \
        -outfmt 6 -num_threads 2 2>/dev/null | wc -l | tr -d ' ')
    echo -e "perc_identity=$PI\tword_size=$WS\thits=$N"
  done
done > $OUT/E4_sensibilidad_umbrales.tsv
# por defecto (megablast, word_size 28) sobre los mismos 21-meros:
echo -e "task=megablast(default)\tword_size=28(default)\thits=$(blastn -query $IN/eth_21mers.fa -db $OUT/db_demo -outfmt 6 -num_threads 2 2>/dev/null | wc -l | tr -d ' ')" >> $OUT/E4_sensibilidad_umbrales.tsv
echo -e "task=blastn(default ws=11, evalue=10)\tword_size=11\thits=$(blastn -task blastn -query $IN/eth_21mers.fa -db $OUT/db_demo -outfmt 6 -num_threads 2 2>/dev/null | wc -l | tr -d ' ')" >> $OUT/E4_sensibilidad_umbrales.tsv
echo "OK"

# --- E5: lado "on-target": mismas ventanas contra el propio transcriptoma ----
makeblastdb -in $IN/dmaidis_public_mrnas.fa -dbtype nucl -title "dmaidis_publico" \
  -out $OUT/db_dmaidis -parse_seqids >> $OUT/E1_makeblastdb.log 2>&1
blastn -task blastn-short -query $IN/eth_21mers.fa -db $OUT/db_dmaidis \
  -word_size 21 -perc_identity 100 -ungapped -dust no -evalue 1000 -max_target_seqs 5000 \
  -outfmt "6 qaccver saccver pident length mismatch gapopen sstrand" -num_threads 2 \
  > $OUT/E5_21mers_ontarget.tsv 2>&1
echo "E5 OK"
