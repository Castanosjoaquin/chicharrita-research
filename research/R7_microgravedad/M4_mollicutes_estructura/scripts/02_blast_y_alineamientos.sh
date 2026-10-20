#!/usr/bin/env bash
# Cómputo local de M4 (entorno conda w5bio: blast 2.17.0+, biopython 1.88). Se corrió desde datos/.
# Las secuencias son proteínas públicas de UniProt y los dos genomas públicos de RefSeq; nada de YHat-Biotech/ ni work/.
set -e
cd datos
# 1) base de homólogos con estructura experimental: 143 de Mycoplasmatota con PDB + 12.412 bacterianas revisadas con PDB + 3 añadidas desde RCSB
makeblastdb -in db_pdb_homologos.faa -dbtype prot -out db_pdb_homologos -parse_seqids
makeblastdb -in uniprot_fasta_prot_Skunkelii_47834.fasta -dbtype prot -out db_Sk_uniprot
makeblastdb -in uniprot_fasta_prot_CaPzeae_202462.fasta -dbtype prot -out db_Pz_uniprot
FMT='6 qseqid sseqid pident length qlen slen qcovs evalue bitscore'
# 2) determinantes de S. citri -> proteoma de S. kunkelii (ortología)
blastp -query q_scitri_determinantes.faa -db db_Sk_uniprot -evalue 1e-5 -seg no -outfmt "$FMT" -max_target_seqs 6 > blast_scitri_vs_Sk.tsv
blastp -query q_scitri_fru.faa -db db_Sk_uniprot -evalue 1e-5 -seg no -outfmt "$FMT" -max_target_seqs 3 -max_hsps 1 > blast_scitri_fru_vs_Sk.tsv
# 3) proteínas de fitoplasmas con PDB -> proteoma de Ca. P. zeae
blastp -query q_fitoplasma_estructurados.faa -db db_Pz_uniprot -evalue 1e-2 -seg no -outfmt "$FMT" -max_target_seqs 6 > blast_fitoplasma_vs_Pz.tsv
# 4) blancos -> mejor homólogo con estructura
blastp -query q_blancos_para_homologo_pdb.faa -db db_pdb_homologos -evalue 1e-3 -seg no -outfmt '6 qseqid sseqid pident length qlen slen qcovs evalue bitscore stitle' -max_target_seqs 400 -max_hsps 1 > blast_blancos_vs_pdbhomologos_raw.tsv
# 5) blancos sin acierto: búsqueda sensible (E hasta 10)
blastp -query q_sin_homologo.faa -db db_pdb_homologos -evalue 10 -seg no -outfmt '6 qseqid sacc pident length qcovs evalue bitscore stitle' -max_hsps 1 -max_target_seqs 3 > blast_sensible_sin_homologo.tsv
# 6) 16S: alineamiento global (Biopython PairwiseAligner: match 1, mismatch -1, apertura -2, extensión -0,5) contra el 16S de 8P6P
python - <<'EOF'
from Bio import SeqIO, Align
recs = {r.id:str(r.seq).upper().replace('U','T') for r in SeqIO.parse('rrna16S_consultas_y_referencia.fna','fasta')}
ref = recs['Mpneumoniae_8P6P_16S']
al = Align.PairwiseAligner(); al.mode='global'; al.match_score=1; al.mismatch_score=-1; al.open_gap_score=-2; al.extend_gap_score=-0.5
for k in ['CaPzeae_op1','CaPzeae_op2','Skunkelii']:
    q=recs[k]; a=al.align(q,ref)[0]; m=cols=0
    for (qs,qe),(rs,re_) in zip(*a.aligned):
        for i in range(qe-qs): cols+=1; m+= q[qs+i]==ref[rs+i]
    print(k, round(100*m/cols,1), cols)
EOF
