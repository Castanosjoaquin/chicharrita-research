
import requests, re, os, io, json, time
from pypdf import PdfReader
import xml.etree.ElementTree as ET
CACHE='cache'; os.makedirs(CACHE,exist_ok=True)
META_FILE=os.path.join(CACHE,'meta.json')
META=json.load(open(META_FILE,encoding='utf-8')) if os.path.exists(META_FILE) else {}
def _save(): json.dump(META,open(META_FILE,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
def arxiv_meta(aid):
    r=requests.get('https://arxiv.org/abs/'+aid,timeout=60)
    r.raise_for_status()
    h=r.text
    def metas(k): return [x for x in re.findall(r'<meta name="%s" content="([^"]*)"'%k,h)]
    import html as H
    t=H.unescape(metas('citation_title')[0]) if metas('citation_title') else '?'
    au='; '.join(H.unescape(a) for a in metas('citation_author'))
    d=(metas('citation_date') or ['?'])[0]
    ol=(metas('citation_online_date') or ['?'])[0]
    m=re.search(r'\[Submitted on ([^\]]*)\]',h)
    ab=re.search(r'<blockquote class="abstract[^>]*>(.*?)</blockquote>',h,re.S)
    abst=H.unescape(re.sub(r'<[^>]+>','',ab.group(1))).strip() if ab else ''
    return dict(titulo=' '.join(t.split()),autores=au,publicado=d,actualizado=ol,submitted=m.group(1) if m else '',url='https://arxiv.org/abs/'+aid,abstract=' '.join(abst.split()))
def get_pdf(url,name,meta=None):
    r=requests.get(url,timeout=120)
    r.raise_for_status()
    rd=PdfReader(io.BytesIO(r.content))
    txt='\n'.join((p.extract_text() or '')+f'\n[[page {i+1}]]' for i,p in enumerate(rd.pages))
    open(os.path.join(CACHE,name+'.txt'),'w',encoding='utf-8',errors='replace').write(txt)
    META[name]=dict(meta or {},url_abierta=url,npag=len(rd.pages),nchar=len(txt),fecha_apertura='2026-10-18')
    _save()
    return len(rd.pages),len(txt)
def get_html(url,name,meta=None):
    r=requests.get(url,timeout=120); r.raise_for_status()
    from lxml import html as LH
    doc=LH.fromstring(r.content)
    for bad in doc.xpath('//script|//style|//nav|//header|//footer'): bad.getparent().remove(bad)
    txt=doc.text_content()
    txt=re.sub(r'\n\s*\n+','\n',txt)
    open(os.path.join(CACHE,name+'.txt'),'w',encoding='utf-8',errors='replace').write(txt)
    META[name]=dict(meta or {},url_abierta=url,nchar=len(txt),fecha_apertura='2026-10-18')
    _save(); return len(txt)
def arx(aid,name=None,mode='pdf'):
    name=name or aid
    m=arxiv_meta(aid)
    if mode=='pdf': n=get_pdf('https://arxiv.org/pdf/'+aid,name,m)
    else: n=get_html('https://arxiv.org/html/'+aid,name,m)
    print(name,m['titulo'],'|',m['autores'][:80],'|',m['publicado'],m['actualizado'],'|',n)
def T(name): return open(os.path.join(CACHE,name+'.txt'),encoding='utf-8').read()
def grep(name,pat,w=300,maxn=8,flags=re.I):
    t=T(name); n=0
    for m in re.finditer(pat,t,flags):
        s=max(0,m.start()-w); e=min(len(t),m.end()+w)
        print(f'--- [{name}] @{m.start()}:',t[s:e].replace('\n',' '))
        n+=1
        if n>=maxn: break
    if n==0: print('(sin coincidencias)',pat)
def show(name,start=0,n=3000): print(T(name)[start:start+n])
