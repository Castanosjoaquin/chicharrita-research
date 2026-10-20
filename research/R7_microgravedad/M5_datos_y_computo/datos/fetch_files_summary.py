
import requests, json, sys, time, re
from concurrent.futures import ThreadPoolExecutor
OUT=sys.argv[1]
accs=json.load(open(OUT+'/datos/osdr_search/accesiones_OSD_indice.json'))
def fetch(a):
    n=a.split('-')[1]
    for attempt in range(3):
        try:
            r=requests.get(f'https://osdr.nasa.gov/osdr/data/osd/files/{n}',params={'size':2000},timeout=120)
            nb=len(r.content)
            j=r.json()
            st=j.get('studies',{}).get(a)
            if not st: return a,{'error':'sin_estudio','hits':j.get('hits'),'bytes':nb}
            files=st['study_files']
            cats={}; 
            tot=0; names_flag=[]
            for f in files:
                c=(f.get('category') or '')+'|'+(f.get('subcategory') or '')
                d=cats.setdefault(c,{'n':0,'bytes':0}); d['n']+=1; d['bytes']+=f.get('file_size') or 0
                tot+=f.get('file_size') or 0
                if re.search(r'mirna|small[-_ ]?rna|srna|smallrna|sirna|pirna',f.get('file_name',''),re.I): names_flag.append(f['file_name'])
            return a,{'file_count':st.get('file_count'),'n_listados':len(files),'total_bytes':tot,'categorias':cats,'archivos_smallrna':names_flag[:20],'bytes':nb,'restricted':sum(1 for f in files if f.get('restricted'))}
        except Exception as e:
            err=str(e)[:150]; time.sleep(2)
    return a,{'error':err}
res={}
with ThreadPoolExecutor(4) as ex:
    for a,d in ex.map(fetch,accs):
        res[a]=d
json.dump(res,open(OUT+'/datos/osdr_search/files_summary_todos.json','w'),indent=0)
print('done',len(res),sum(d.get('bytes',0) for d in res.values()))
