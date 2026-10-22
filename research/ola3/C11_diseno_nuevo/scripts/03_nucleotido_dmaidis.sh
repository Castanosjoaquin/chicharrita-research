#!/usr/bin/env bash
# Paso 3-4 Fase 2. Comando (desde la raiz del repo, env w5bio): bash research/ola3/C11_diseno_nuevo/scripts/03_nucleotido_dmaidis.sh
# Entrada: ortologos reciprocos M. quadrilineatus (GCF_028750875.1) en work/C11_diseno_nuevo/ortologos_mq.faa
# Local, sin subir secuencias. Motor: BLAST+ 2.17.0 (tblastn, blastn). Fecha: 2026-10-22
set -e
W=work/C11_diseno_nuevo; B=$W/blast
[ -f $B/mq_rna_db.nsq ] || makeblastdb -in work/C5/refs/Macrosteles_quadrilineatus_rna.fna -dbtype nucl -parse_seqids -out $B/mq_rna_db >/dev/null
[ -f $B/tsa_db.nsq ] || { cat work/W5/ref/TSA_GCWP01.fasta work/W5/ref/TSA_GHCC01.fasta work/W5/ref/TSA_GITV01.fasta > $B/tsa_all.fasta; makeblastdb -in $B/tsa_all.fasta -dbtype nucl -out $B/tsa_db >/dev/null; }
# 1) proteina ortologa -> ARNm de M. quadrilineatus (mejor hit tblastn)
tblastn -query $W/ortologos_mq.faa -db $B/mq_rna_db -evalue 1e-30 -max_target_seqs 1 -outfmt "6 qseqid sseqid pident length sstart send" -out $B/orto_to_xm.tsv
# 2) extraer el ARNm y alinear a nivel de nucleotido contra el TSA de D. maidis
cut -f2 $B/orto_to_xm.tsv | sort -u > $B/xm.ids
blastdbcmd -db $B/mq_rna_db -entry_batch $B/xm.ids -out $B/xm.fna 2>/dev/null || true
