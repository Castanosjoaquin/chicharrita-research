#!/usr/bin/env bash
# C5 / Q2 — Ventanas de 21 nt eficientes (criterio si-Fi21) para los genes candidatos
# NUEVOS de la literatura, sobre secuencia PUBLICA unicamente.
#   - eth y burs-alpha de Dalbulus maidis: GenBank PZ371507.1 / PZ371508.1 (copia local en work/W2/)
#   - Rpn6 de Scaphoideus titanus y Euscelidius variegatus: TSA GJQL01135962.1 / GFTU01006765.1
#   - ortologos del cicadelido anotado Macrosteles quadrilineatus: RefSeq local de W4
# Corre el port de si-Fi21 SIN modificarlo (tools/sifi21_port/run_sifi.py), modo fiel,
# backend vienna (ViennaRNA 2.7.2; el backend exe del original solo existe en Windows).
set -euo pipefail
cd "$(dirname "$0")/../../../.."
S=work/C5/seqs; O=work/C5/sifi21
mkdir -p "$S" "$O"
MQ=work/W4/downloads/GCF_028750875.1/ncbi_dataset/data/GCF_028750875.1/rna.fna

# 1. Armar el FASTA de candidatos (una secuencia por gen)
python3 - <<'PY'
from pathlib import Path
def leer(p):
    nom, buf, out = None, [], {}
    for l in Path(p).read_text().splitlines():
        if l.startswith(">"):
            if nom: out[nom] = "".join(buf)
            nom, buf = l[1:].split()[0], []
        else: buf.append(l.strip())
    if nom: out[nom] = "".join(buf)
    return out
mq = leer("work/W4/downloads/GCF_028750875.1/ncbi_dataset/data/GCF_028750875.1/rna.fna")
dm = leer("work/W2/dmaidis_public_mrnas.fa")
st = leer("work/C5/seqs/GJQL01135962.fa"); ev = leer("work/C5/seqs/GFTU01006765.fa")
sel = [
 ("eth_Dmaidis_PZ371507",        dm["PZ371507.1"]),
 ("bursA_Dmaidis_PZ371508",      dm["PZ371508.1"]),
 ("Rpn6_Stitanus_GJQL01135962",  st["GJQL01135962.1"]),
 ("Rpn6_Evariegatus_GFTU01006765", ev["GFTU01006765.1"]),
 ("Rpn6_Mquadrilineatus_XM_054426723", mq["XM_054426723.1"]),   # ortologo por HOMOLOGIA (paso 03/04)
 ("PSMD11_Mquadrilineatus_XM_054432574", mq["XM_054432574.1"]), # el que devuelve la busqueda POR NOMBRE
 ("ATPsynBeta_Mquadrilineatus_XM_054410120", mq["XM_054410120.1"]),
 ("Ruvbl1_Mquadrilineatus_XM_054402769", mq["XM_054402769.1"]),
 ("XPO1_Mquadrilineatus_XM_054404977", mq["XM_054404977.1"]),
 ("TnC_Mquadrilineatus_XM_054409464", mq["XM_054409464.1"]),
]
with open("work/C5/seqs/candidatos_c5.fa","w") as fh:
    for n,s in sel:
        fh.write(f">{n}\n")
        for i in range(0,len(s),70): fh.write(s[i:i+70]+"\n")
        print(f"{n}\t{len(s)} nt")
PY

# 2. Perfil de eficiencia
python3 tools/sifi21_port/run_sifi.py "$S/candidatos_c5.fa" --modo fiel --backend vienna \
        --region 200 --salida "$O/fiel" | tee "$O/resumen_fiel.txt"
