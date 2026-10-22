"""Fase 2, pasos 3-4: ortologia reciproca por secuencia y medicion a nivel de nucleotido.
Comando (raiz del repo, env w5bio para BLAST; el analisis en python con pandas):
  1) curl "https://rest.uniprot.org/uniprotkb/stream?query=reviewed:true+AND+taxonomy_id:6656&format=fasta" -o work/C11_diseno_nuevo/swissprot_arthropoda_rev.faa   (14.079 entradas, 2026-10-22)
  2) makeblastdb -dbtype prot sobre proteoma GCF_028750875.1 (M. quadrilineatus, 34.269) y sobre el FASTA de UniProt
  3) blastp -evalue 1e-10 -max_target_seqs 5 en ambos sentidos (sp_vs_mq.tsv, mq_vs_sp.tsv); BLAST+ 2.17.0
  4) bash research/ola3/C11_diseno_nuevo/scripts/03_nucleotido_dmaidis.sh   (tblastn al ARNm de M. quadrilineatus)
  5) blastn -task blastn -evalue 1e-10 xm.fna vs tsa_db (GCWP01+GHCC01+GITV01) -> xm_vs_tsa.tsv
Este archivo documenta la logica de los pasos de analisis (RBH, filtro estricto, ventanas de 21 nt). Todo local.
Criterio fijado antes de buscar: criterio.md (2026-10-22). Umbrales: ev<=1e-20, qcov>=70, HSP>=300 nt con >=90 %.
"""
# RBH: mejor hit por bitscore en cada sentido; par si coinciden. Normalizar ids: 'ref|XP_..|' -> 'XP_..'.
# Ventanas de 21 nt: k-mers exactos del ARNm de M. quadrilineatus presentes en los contigs TSA con hit (ambas cadenas).
# Familias por NOMBRE DE PROTEINA en Swiss-Prot (no por GN: GN de Drosophila difiere, p. ej. Rpn6 es PSD11 y PSMD6 es Rpn7).
