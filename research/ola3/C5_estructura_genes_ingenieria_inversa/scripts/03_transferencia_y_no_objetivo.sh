#!/usr/bin/env bash
# C5 / Q2 — Dos preguntas sobre los candidatos nuevos, con herramientas locales:
#  (a) TRANSFERENCIA: de las ventanas de 21 nt de un ortologo de otra especie,
#      cuantas existen identicas en el genoma de Dalbulus maidis (ihDalMaid1.1).
#  (b) NO OBJETIVO: cuantas aparecen en cicadelidos no objetivo (Macrosteles
#      quadrilineatus, Homalodisca vitripennis), en maiz y en abeja.
# Usa tools/sifi21_port/offtarget_21nt.py sin modificarlo. Todo local.
set -euo pipefail
cd "$(dirname "$0")/../../../.."
D=work/W4/downloads; O=work/C5/offtarget; R=work/C5/refs
mkdir -p "$O" "$R"
# enlaces con nombre de especie: el resumen del port identifica la referencia por
# nombre de archivo y los cinco originales se llaman rna.fna
ln -sf "$PWD/$D/GCF_028750875.1/ncbi_dataset/data/GCF_028750875.1/rna.fna" "$R/Macrosteles_quadrilineatus_rna.fna"
ln -sf "$PWD/$D/GCF_021130785.1/ncbi_dataset/data/GCF_021130785.1/rna.fna" "$R/Homalodisca_vitripennis_rna.fna"
ln -sf "$PWD/$D/GCF_902167145.1/ncbi_dataset/data/GCF_902167145.1/rna.fna" "$R/Zea_mays_rna.fna"
ln -sf "$PWD/$D/GCF_003254395.2/ncbi_dataset/data/GCF_003254395.2/rna.fna" "$R/Apis_mellifera_rna.fna"
python3 tools/sifi21_port/offtarget_21nt.py \
  --consulta work/C5/seqs/candidatos_c5.fa \
  --db "$D/GCA_975739785.1/ncbi_dataset/data/GCA_975739785.1/GCA_975739785.1_ihDalMaid1.1_genomic.fna" \
       "$R/Macrosteles_quadrilineatus_rna.fna" \
       "$R/Homalodisca_vitripennis_rna.fna" \
       "$R/Zea_mays_rna.fna" \
       "$R/Apis_mellifera_rna.fna" \
  --salida "$O"
