"""Consulta la API de AlphaFold DB para cada accesión UniProt de los dos taxones (lista tomada de datos/uniprot_taxon_*.txt, UniProt REST).
Guarda la respuesta cruda por accesión en datos/afdb_bulk_{taxid}.jsonl y escribe un resumen en datos/log_consultas.jsonl."""
import requests, json, io, datetime, time, sys, os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, 'datos')
S = requests.Session(); S.headers['User-Agent']='python-requests (academic structure coverage survey)'
def q(acc):
    for i in range(3):
        try:
            r = S.get(f'https://alphafold.ebi.ac.uk/api/prediction/{acc}', timeout=60)
            if r.status_code in (200,404):
                return acc, r.status_code, (r.json() if r.status_code==200 else None)
        except Exception as e:
            time.sleep(1.5)
    return acc, -1, None
for tid, nm in [(202462,'CaPzeae'),(47834,'Skunkelii')]:
    df = pd.read_csv(os.path.join(D, f'uniprot_taxon_{tid}_{nm}.txt'), sep='\t')
    accs = df['Entry'].tolist()
    t0=time.time()
    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(q, accs))
    with open(os.path.join(D, f'afdb_bulk_{tid}.jsonl'),'w') as f:
        for acc, st, body in res:
            f.write(json.dumps({'accession':acc,'http_status':st,'body':body}, ensure_ascii=False)+'\n')
    n200 = sum(1 for _,s,_ in res if s==200); n404=sum(1 for _,s,_ in res if s==404); nerr=sum(1 for _,s,_ in res if s==-1)
    rec = dict(ts=datetime.datetime.utcnow().isoformat()+'Z', method='GET', url='https://alphafold.ebi.ac.uk/api/prediction/{UniProt accession}', params=f'{len(accs)} accesiones del taxid {tid}', status=f'200:{n200} 404:{n404} error:{nerr}', file=f'afdb_bulk_{tid}.jsonl', name=f'afdb_bulk_{tid}', note=f'consulta masiva; {time.time()-t0:.0f} s')
    open(os.path.join(D,'log_consultas.jsonl'),'a').write(json.dumps(rec, ensure_ascii=False)+'\n')
    print(tid, len(accs), n200, n404, nerr, flush=True)
