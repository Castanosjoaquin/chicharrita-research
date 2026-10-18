# Funciones mínimas usadas por la pista AQB para abrir fuentes (requests + lxml + pypdf); sin credenciales ni envío de datos del repo.
import io, re, requests
from lxml import etree, html as lhtml
UA={'User-Agent':'python-requests'}
def arxiv_meta(aid):
    r=requests.get('http://export.arxiv.org/api/query',params={'id_list':aid},timeout=60)
    t=etree.fromstring(r.content); ns={'a':'http://www.w3.org/2005/Atom'}; e=t.find('a:entry',ns)
    return dict(title=' '.join(e.find('a:title',ns).text.split()),authors=[a.find('a:name',ns).text for a in e.findall('a:author',ns)],
                published=e.find('a:published',ns).text[:10],updated=e.find('a:updated',ns).text[:10],abstract=' '.join(e.find('a:summary',ns).text.split()))
def html_text(content):
    doc=lhtml.fromstring(content)
    for bad in doc.xpath('//script|//style|//nav|//header|//footer'): bad.getparent().remove(bad)
    txt=doc.text_content(); txt=re.sub(r'[ \t]+',' ',txt); return re.sub(r'\n\s*\n+','\n\n',txt)
def get_arxiv(aid):
    r=requests.get(f'https://arxiv.org/html/{aid}',headers=UA,timeout=90)
    if r.status_code==200 and len(r.content)>20000: return html_text(r.content)
    from pypdf import PdfReader
    r=requests.get(f'https://arxiv.org/pdf/{aid}',headers=UA,timeout=120); r.raise_for_status()
    return '\n'.join((p.extract_text() or '') for p in PdfReader(io.BytesIO(r.content)).pages)
def grep(txt,pat,w=300,maxn=8):
    n=0
    for m in re.finditer(pat,txt,flags=re.I):
        print('...',txt[max(0,m.start()-w):m.end()+w].replace('\n',' '),'...\n'); n+=1
        if n>=maxn: break
