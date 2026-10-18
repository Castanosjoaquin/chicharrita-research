#!/usr/bin/env python3
"""R6 - busqueda por perfiles HMM de dominios de RNAi (PIWI, PAZ, Dicer_dimer) con control RNasa III.
Entradas: dos proteomas RefSeq (NCBI Datasets) + 3 controles positivos de UniProt.
Umbral: GA (gathering) propio de cada perfil Pfam.  Sin semillas: HMMER es determinista.
Uso: python3 scripts/01_hmm_rnai_dominios.py
"""
import pyhmmer, glob, os, csv, sys
from pyhmmer.easel import SequenceFile, Alphabet
from pyhmmer.plan7 import HMMFile
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
alpha = Alphabet.amino()
def txt(x):
    return x.decode() if isinstance(x, (bytes, bytearray)) else x

targets = {
 "Ca_P_zeae_M3_GCF_001712875.1": f"{base}/datos/GCF_001712875.1/ncbi_dataset/data/GCF_001712875.1/protein.faa",
 "S_kunkelii_CR2-3x_GCF_001274875.1": f"{base}/datos/GCF_001274875.1/ncbi_dataset/data/GCF_001274875.1/protein.faa",
 "S_kunkelii_pSKU146_NC_006400.1": f"{base}/datos/pSKU146_NC_006400.1_cds_aa.faa",
 "controles_positivos": f"{base}/datos/controles_positivos.faa",
}
hmms = []
for p in sorted(glob.glob(f"{base}/datos/pfam/*.hmm")):
    with HMMFile(p) as hf: hmms.extend(list(hf))
rows = []
summ = []
for tname, path in targets.items():
    with SequenceFile(path, digital=True, alphabet=alpha) as sf: seqs = sf.read_block()
    for hmm in hmms:
        n = 0
        for hits in pyhmmer.hmmsearch(hmm, seqs, bit_cutoffs="gathering", cpus=4):
            for h in hits:
                if h.included:
                    n += 1
                    rows.append([tname, txt(hmm.accession), txt(hmm.name), txt(h.name), f"{h.score:.1f}", f"{h.evalue:.2e}"])
        summ.append([tname, len(seqs), txt(hmm.accession), txt(hmm.name), n])
with open(f"{base}/datos/hmm_hits.tsv", "w", newline="") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(["objetivo","pfam","perfil","proteina","bitscore","evalue"]); w.writerows(rows)
with open(f"{base}/datos/hmm_resumen.tsv", "w", newline="") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(["objetivo","n_secuencias","pfam","perfil","n_hits_GA"]); w.writerows(summ)
print("pyhmmer", pyhmmer.__version__)
for s in summ: print(*s, sep="\t")
