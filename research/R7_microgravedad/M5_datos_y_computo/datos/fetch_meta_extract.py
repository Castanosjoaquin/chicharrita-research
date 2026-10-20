
import requests, json, sys, time, re
from concurrent.futures import ThreadPoolExecutor
OUT=sys.argv[1]
accs=json.load(open(OUT+'/datos/osdr_search/accesiones_inventario.json'))
def strip(h): return re.sub('<[^>]+>','',h or '')
def fetch(a):
    n=a.split('-')[1]; err=''
    for attempt in range(3):
        try:
            r=requests.get(f'https://osdr.nasa.gov/osdr/data/osd/meta/{n}',timeout=180)
            nb=len(r.content); j=r.json()
            st=j.get('study',{}).get(a)
            if not st: return a,{'error':'sin_estudio','hits':j.get('hits'),'bytes':nb}
            ai=st.get('additionalInformation',{})
            samples=ai.get('samples',{}) or {}
            ns={k:len(v.get('table',[])) for k,v in samples.items() if isinstance(v,dict)}
            assays=list((ai.get('assays') or {}).keys())
            adesc=ai.get('description',{}).get('assays',[]) if isinstance(ai.get('description'),dict) else []
            facs=[strip(f.get('factor')) for f in (ai.get('description',{}).get('factors',[]) if isinstance(ai.get('description'),dict) else [])]
            orgs=ai.get('organisms')
            orgn=list(orgs.keys()) if isinstance(orgs,dict) else orgs
            # n muestras por ensayo
            an={}
            for k,v in (ai.get('assays') or {}).items():
                if isinstance(v,dict): an[k]=len(v.get('table',[]))
            return a,{'n_samples_por_tabla':ns,'assays_keys':assays,'assays_desc':adesc,'factores':facs,'organismos':orgn,'n_filas_por_ensayo':an,'bytes':nb}
        except Exception as e:
            err=str(e)[:150]; time.sleep(3)
    return a,{'error':err}
res={}
with ThreadPoolExecutor(4) as ex:
    for a,d in ex.map(fetch,accs): res[a]=d
json.dump(res,open(OUT+'/datos/osdr_search/meta_extract_inventario.json','w'),indent=0)
print('done',len(res),sum(d.get('bytes',0) for d in res.values())/1e6,'MB')
