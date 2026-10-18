"""Soporte mínimo de AQA: descarga de texto de arXiv con pypdf y test de Fisher sin apareamiento
sobre las ablaciones de Bioinfoysis (arXiv 2609.03871, tabla 3). Sin dependencias fuera de requests, pypdf, lxml, scipy."""
import io, requests
from pypdf import PdfReader
from scipy.stats import fisher_exact

def arxiv_text(aid):
    r = requests.get(f"https://arxiv.org/pdf/{aid}", headers={"User-Agent": "research-notes-fetch/0.1"}, timeout=90)
    r.raise_for_status()
    rd = PdfReader(io.BytesIO(r.content))
    return "\n".join(f"[[p{i+1}]]\n" + (p.extract_text() or "") for i, p in enumerate(rd.pages))

if __name__ == "__main__":
    full = 162  # correctas de 205 con la configuración completa (GPT-5.4), tabla 3
    for label, ok in [("plan fijo", 148), ("sin memoria", 116), ("sin habilidades de bioinformática", 123), ("sin habilidades", 87)]:
        p = fisher_exact([[full, 205 - full], [ok, 205 - ok]])[1]
        print(f"{label}: diferencia {(full - ok) / 205 * 100:.2f} puntos, Fisher sin apareamiento p = {p:.4f}")
