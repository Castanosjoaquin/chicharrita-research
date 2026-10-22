"""Genera index.html de C9 desde REPORT.md, con el CSS de C7_ranking_v2/index.html.

El markdown es la fuente de verdad; el HTML es la vista de lectura.
Uso (desde la raiz del repositorio):
    python research/ola3/C9_sensibilidad_umbral/scripts/generar_index.py
"""
import html
import re
from pathlib import Path

import sys
AQUI = Path(__file__).resolve().parents[1]
PARES = [("REPORT.md", "index.html"),
         ("RESULTADOS_validacion_retrospectiva.md", "resultados_validacion.html")]
SRC, DST = PARES[int(sys.argv[1]) if len(sys.argv) > 1 else 0]
C7 = AQUI.parent / "C7_ranking_v2" / "index.html"
css = re.search(r"<style>(.*?)</style>", C7.read_text(encoding="utf-8"), re.S).group(1)


def inline(t):
    out = []
    for p in re.split(r"(`[^`]*`)", t):
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append("<code>%s</code>" % html.escape(p[1:-1]))
            continue
        p = html.escape(p, quote=False)
        # las imagenes primero: si no, ![alt](src) queda como !<a href>
        p = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)",
                   r'<img src="\2" alt="\1" style="max-width:100%;height:auto">', p)
        p = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', p)
        p = re.sub(r"~~(.+?)~~", r"<del>\1</del>", p)
        p = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", p)
        p = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", p)
        out.append(p)
    return "".join(out)


def celdas(l):
    return [c.strip() for c in l.strip().strip("|").split("|")]


bloques, tabla, parrafo = [], [], []


def vaciar_p():
    global parrafo
    if parrafo:
        bloques.append("<p>%s</p>" % inline(" ".join(parrafo)))
        parrafo = []


def vaciar_t():
    global tabla
    if tabla:
        cab, filas = tabla[0], tabla[2:]
        bloques.append("<div class=\"tw\"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (
            "".join("<th>%s</th>" % inline(c) for c in celdas(cab)),
            "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in celdas(r)) for r in filas)))
        tabla = []


titulo = ""
for l in (AQUI / SRC).read_text(encoding="utf-8").split("\n"):
    if l.startswith("|"):
        vaciar_p(); tabla.append(l); continue
    vaciar_t()
    if l.startswith("# "):
        vaciar_p(); titulo = l[2:].strip()
    elif l.startswith("## "):
        vaciar_p(); bloques.append("<h2>%s</h2>" % inline(l[3:].strip()))
    elif l.strip() == "":
        vaciar_p()
    else:
        parrafo.append(l.strip())
vaciar_p(); vaciar_t()

out = ("<!doctype html>\n<html lang=\"es\"><head><meta charset=\"utf-8\">\n"
       "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n<title>%s</title>\n"
       "<style>%s</style></head><body><main>\n<h1>%s</h1>\n"
       "<p class=\"lead\">2026-10-21. Detalle y reproducción en <a href=\"%s\">%s</a>.</p>\n%s\n</main></body></html>\n"
       % (html.escape(titulo), css, html.escape(titulo), SRC, SRC, "\n".join(bloques)))
(AQUI / DST).write_text(out, encoding="utf-8")
print("escrito", AQUI / DST, len(out), "bytes")
