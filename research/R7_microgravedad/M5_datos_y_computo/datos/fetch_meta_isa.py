
import requests, json, sys, time, re
from concurrent.futures import ThreadPoolExecutor
OUT=sys.argv[1]
accs=json.load(open(OUT+'/datos/osdr_search/accesiones_meta_isa.json'))
def fetch(a):
    n=a.split('-')[1]; err=''
    for attempt in range(3):
        try:
            r=requests.get(f'https://osdr.nasa.gov/osdr/data/osd/meta/{n}',timeout=180)
            nb=len(r.content); j=r.json()
            st=j.get('study',{}).get(a)
            if not st: return a,{'error':'sin_estudio','bytes':nb}
            ss=st.get('studies') or []
            if not ss: return a,{'error':'sin_studies','claves':list(st.keys()),'bytes':nb}
            s0=ss[0]
            mats=s0.get('materials') or {}
            ns=len(mats.get('samples',[])) if isinstance(mats,dict) else None
            nsrc=len(mats.get('sources',[])) if isinstance(mats,dict) else None
            facs=[f.get('factorName') for f in s0.get('factors',[])]
            assays=[]
            for x in s0.get('assays',[]):
                assays.append({'medida':(x.get('measurementType') or {}).get('annotationValue'),'tecnologia':(x.get('technologyType') or {}).get('annotationValue'),'plataforma':x.get('technologyPlatform'),'n_dataFiles':len(x.get('dataFiles',[])) if 'dataFiles' in x else None})
            return a,{'n_samples':ns,'n_sources':nsrc,'factores':facs,'assays':assays,'bytes':nb}
        except Exception as e:
            err=str(e)[:150]; time.sleep(3)
    return a,{'error':err}
res={}
with ThreadPoolExecutor(4) as ex:
    for a,d in ex.map(fetch,accs): res[a]=d
json.dump(res,open(OUT+'/datos/osdr_search/meta_extract_isa.json','w'),indent=0)
print('done',len(res),sum(d.get('bytes',0) for d in res.values())/1e6,'MB')
