"""
Prueba de humo del "control de anclaje" (pista EVA). NO es un prototipo del pipeline:
solo comprueba que las tres verificaciones baratas del diseno son realizables con APIs
publicas desde este entorno: (1) existencia de DOI/PMID/arXiv, (2) cotejo de titulo,
(3) cita literal contra texto abierto. No envia ninguna secuencia ni dato del repo.
Uso: python verify_refs_smoketest.py   (imprime una tabla y sale con 0 si todo coincide con lo esperado)
"""
import re, sys, time, unicodedata, json
import requests
from lxml import html as LH
UA = {"User-Agent": "grounding-smoketest/0.1"}   # sin correo: en uso real, enviar el contacto que pida cada servicio

def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def crossref(doi):
    r = requests.get(f"https://api.crossref.org/works/{doi}", headers=UA, timeout=30)
    if r.status_code != 200: return None
    m = r.json()["message"]
    return {"title": (m.get("title") or [""])[0], "year": (m.get("issued", {}).get("date-parts") or [[None]])[0][0]}

def pubmed(pmid):
    r = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
                     params={"db": "pubmed", "id": pmid, "retmode": "json"}, headers=UA, timeout=30)
    res = r.json().get("result", {})
    rec = res.get(str(pmid))
    if not rec or "error" in rec: return None
    return {"title": rec.get("title", ""), "year": (rec.get("pubdate") or "")[:4]}

def arxiv(aid):
    r = requests.get(f"https://arxiv.org/abs/{aid}", headers=UA, timeout=30)
    if r.status_code != 200: return None
    t = LH.fromstring(r.text).xpath('//meta[@name="citation_title"]/@content')
    return {"title": t[0] if t else "", "year": None}

def title_match(claimed, found):
    a, b = set(norm(claimed).split()), set(norm(found).split())
    return len(a & b) / max(1, len(a | b))          # Jaccard de palabras

def quote_in_text(quote, text):
    return norm(quote) in norm(text)

cases = [
 # (tipo, id, titulo declarado, esperado_existe)
 ("doi",   "10.1038/s41592-025-02748-6", "GeneAgent: self-verification language agent for gene-set analysis using domain databases", True),
 ("doi",   "10.1038/s41592-025-99999-9", "GeneAgent: self-verification language agent for gene-set analysis using domain databases", False),
 ("pmid",  "38898292", "Detecting hallucinations in large language models using semantic entropy", True),
 ("pmid",  "38898292", "A study of nothing in particular about maize leafhoppers", True),   # existe pero el titulo declarado NO coincide
 ("pmid",  "99999999", "Titulo inventado", False),
 ("arxiv", "2503.00096", "BixBench: a Comprehensive Benchmark for LLM-based Agents in Computational Biology", True),
 ("arxiv", "2503.99999", "Titulo inventado", False),
]
fn = {"doi": crossref, "pmid": pubmed, "arxiv": arxiv}
ok_all = True
print(f"{'tipo':6} {'id':30} {'existe':7} {'esperado':9} {'jaccard_titulo':14}")
for kind, ident, claimed, expected in cases:
    try:
        found = fn[kind](ident)
    except Exception as e:
        found = None; print("  error de red:", str(e)[:80])
    exists = found is not None
    jac = title_match(claimed, found["title"]) if found else 0.0
    print(f"{kind:6} {ident:30} {str(exists):7} {str(expected):9} {jac:14.2f}")
    ok_all &= (exists == expected)
    time.sleep(0.4)

# (3) cita literal contra el texto abierto (HTML de arXiv de BixBench, version vigente)
r = requests.get("https://arxiv.org/html/2503.00096", headers=UA, timeout=60)
text = LH.fromstring(r.text).text_content()
real_q = "the agent's submitted answer is compared directly to the ground truth answer by a separate LLM call"
fake_q = "the agent's submitted answer is compared directly to the ground truth answer by three human experts"
paraph = "the final answer of the agent is judged against the reference by another language model call"
for name, q, exp in [("literal real", real_q, True), ("literal alterada", fake_q, False), ("parafrasis (no es cita literal)", paraph, False)]:
    got = quote_in_text(q, text)
    print(f"cita[{name}] encontrada={got} esperado={exp}")
    ok_all &= (got == exp)
print("TODO COINCIDE CON LO ESPERADO" if ok_all else "HAY DIFERENCIAS")
sys.exit(0 if ok_all else 1)
