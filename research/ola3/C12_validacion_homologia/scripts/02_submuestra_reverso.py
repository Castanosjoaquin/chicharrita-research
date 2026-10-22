"""C12 validacion A, submuestra. Comando (raiz del repo, env w5bio): python research/ola3/C12_validacion_homologia/scripts/02_submuestra_reverso.py
Desvio declarado: el forward MQ->HV (script 01) se interrumpio por lento; se usa el parcial (sin la ultima consulta, posiblemente cortada),
submuestra aleatoria (semilla 0) de 4.000 consultas con hit, y el reverso se corre solo para sus mejores hits HV. No se corrio MQ-NL.
"""
import random, subprocess, collections
O='work/C12'
rows=[r for r in (l.rstrip('\n').split('\t') for l in open(f'{O}/MQ_vs_HV.tsv')) if len(r)==9]
order=[]; best={}
for r in rows:
    if not order or order[-1]!=r[0]: order.append(r[0])
    if r[0] not in best or float(r[7])>float(best[r[0]][7]): best[r[0]]=r
order=order[:-1]  # la ultima puede estar cortada
random.seed(0); samp=random.sample(order,4000)
subj=sorted({best[q][1] for q in samp})
HV='work/W4/downloads/GCF_021130785.1/ncbi_dataset/data/GCF_021130785.1/protein.faa'
want=set(subj); out=open(f'{O}/hv_sub.faa','w'); keep=False
for l in open(HV):
    if l.startswith('>'): keep=l[1:].split()[0] in want
    if keep: out.write(l)
out.close()
open(f'{O}/muestra_mq.txt','w').write('\n'.join(samp))
print(len(order),len(samp),len(subj))
