"""Perfil de eficiencia (si-Fi21 corregido, ViennaRNA) de los seis genes a 21 y a 22 nt.

Escribe work/sifi_v2/salida_k21 y salida_k22 con un TSV por gen. Correr desde la raiz del
repositorio, con ViennaRNA instalado.
"""
import sys
from pathlib import Path
sys.path.insert(0,'tools/sifi21_port')
from sifi_core import SifiEngine, to_tsv
fa=Path('work/sifi_v2/fasta')
for k in (21,22):
    out=Path(f'work/sifi_v2/salida_k{k}'); out.mkdir(exist_ok=True)
    for f in sorted(fa.glob('*_full.fasta')):
        g=f.name.replace('_full.fasta','')
        seq=''.join(l.strip() for l in f.read_text().splitlines() if not l.startswith('>'))
        w,r=SifiEngine(mode='corregido',sirna_size=k).run(seq,backend='vienna')
        to_tsv(w,out/f'{g}_full_corregido_vienna.tsv')
        print(k,g,len(w),sum(x.is_efficient for x in w),flush=True)
