#!/usr/bin/env bash
# C5 / Q3 — El circuito del investigador, corrido de punta a punta sobre un gen
# nuevo (Rpn6 de Scaphoideus titanus, TSA GJQL01135962.1) con herramientas locales.
#  Paso 2-3: BLAST contra transcriptomas anotados de cicadelidos -> identidad real
#  Paso 4  : el ortologo en la especie cercana anotada (Macrosteles quadrilineatus)
#  Paso 5  : recuperar el locus en el genoma NO anotado de Dalbulus maidis
#            (miniprot con la proteina del ortologo; tblastn seria el equivalente
#            con solo BLAST, pero no modela intrones)
set -euo pipefail
cd "$(dirname "$0")/../../../.."
D=work/W4/downloads; O=work/C5/circuito; mkdir -p "$O" work/C5/db
MQ=$D/GCF_028750875.1/ncbi_dataset/data/GCF_028750875.1
HV=$D/GCF_021130785.1/ncbi_dataset/data/GCF_021130785.1

for pair in "mq:$MQ/rna.fna" "hv:$HV/rna.fna"; do
  k=${pair%%:*}; f=${pair#*:}
  [ -f work/C5/db/$k.nin ] || [ -f work/C5/db/$k.nal ] || makeblastdb -in "$f" -dbtype nucl -out work/C5/db/$k > "$O/makeblastdb_$k.log"
done

echo "=== paso 2-3: blastn de Rpn6 de S. titanus contra cicadelidos anotados ==="
for k in mq hv; do
  blastn -task dc-megablast -query work/C5/seqs/GJQL01135962.fa -db work/C5/db/$k \
    -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" \
    -max_target_seqs 5 -evalue 1e-5 > "$O/rpn6_vs_$k.tsv"
  echo "--- $k (dc-megablast, top 5)"; head -5 "$O/rpn6_vs_$k.tsv"
done

echo "=== identidad proteica del ortologo (blastp reciproco no; solo para contexto) ==="
grep -A999999 "XP_054288549" /dev/null 2>/dev/null || true

echo "=== paso 5: locus en el genoma no anotado, con miniprot ==="
python3 - <<'PY'
from pathlib import Path
nom,buf,out=None,[],{}
for l in Path("work/W4/downloads/GCF_028750875.1/ncbi_dataset/data/GCF_028750875.1/protein.faa").read_text().splitlines():
    if l.startswith(">"):
        if nom: out[nom]="".join(buf)
        nom,buf=l[1:],[]
    else: buf.append(l.strip())
if nom: out[nom]="".join(buf)
sel=[(k,v) for k,v in out.items() if "non-ATPase regulatory subunit 11" in k]
with open("work/C5/circuito/rpn6_mq_prot.faa","w") as fh:
    for k,v in sel:
        fh.write(">"+k.split()[0]+"\n"+v+"\n"); print(k[:90], len(v),"aa")
PY
miniprot -t 4 --gff work/C5/miniprot/dmaidis.mpi "$O/rpn6_mq_prot.faa" > "$O/rpn6_en_dmaidis.gff" 2> "$O/rpn6_miniprot.log"
grep -E "^##PAF" "$O/rpn6_en_dmaidis.gff" | awk '{print $2,$3,$6,$7,$8,$9,$10,$11,$12,$13}'
