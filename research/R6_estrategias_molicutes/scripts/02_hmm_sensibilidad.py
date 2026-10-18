#!/usr/bin/env python3
"""R6 - pasada de sensibilidad: mejor acierto por perfil SIN umbral GA (E<=10), para ver cuan lejos del corte queda el cero."""
import pyhmmer, glob, os, csv
from pyhmmer.easel import SequenceFile, Alphabet
from pyhmmer.plan7 import HMMFile
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
alpha = Alphabet.amino()
txt = lambda x: x.decode() if isinstance(x,(bytes,bytearray)) else x
targets = {
 "Ca_P_zeae_M3": f"{base}/datos/GCF_001712875.1/ncbi_dataset/data/GCF_001712875.1/protein.faa",
 "S_kunkelii_CR2-3x": f"{base}/datos/GCF_001274875.1/ncbi_dataset/data/GCF_001274875.1/protein.faa",
 "S_kunkelii_pSKU146": f"{base}/datos/pSKU146_NC_006400.1_cds_aa.faa",
 "controles": f"{base}/datos/controles_positivos.faa",
}
hmms=[]
for p in sorted(glob.glob(f"{base}/datos/pfam/*.hmm")):
    with HMMFile(p) as hf: hmms.extend(list(hf))
out=[]
for t,path in targets.items():
    with SequenceFile(path,digital=True,alphabet=alpha) as sf: seqs=sf.read_block()
    for hmm in hmms:
        ga=hmm.cutoffs.gathering[0]
        best=None
        for hits in pyhmmer.hmmsearch(hmm,seqs,E=10.0,cpus=4):
            for h in hits:
                if best is None or h.score>best[1]: best=(txt(h.name),h.score,h.evalue)
        out.append([t,txt(hmm.accession),txt(hmm.name),f"{ga:.1f}",best[0] if best else "-",f"{best[1]:.1f}" if best else "-",f"{best[2]:.1e}" if best else "-"])
with open(f"{base}/datos/hmm_sensibilidad.tsv","w",newline="") as f:
    w=csv.writer(f,delimiter="\t"); w.writerow(["objetivo","pfam","perfil","corte_GA","mejor_proteina","bitscore","evalue"]); w.writerows(out)
for r in out: print(*r,sep="\t")
