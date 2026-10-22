"""Convierte un .md del repo a un .html autocontenido, con el CSS de C7.

El markdown es la fuente de verdad; el HTML es solo la vista de lectura. Soporta
titulos, parrafos, tablas, imagenes, enlaces, negrita, cursiva, tachado, codigo en
linea y lineas horizontales. No es un conversor general: cubre lo que usan los
documentos de este repositorio.

Uso (desde la raiz del repositorio):
    python tools/md_a_html.py entregables/para-el-investigador.md \
        entregables/para-el-investigador.html
"""
import html
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CSS_FUENTE = RAIZ / "research" / "ola3" / "C7_ranking_v2" / "index.html"
CSS = re.search(r"<style>(.*?)</style>", CSS_FUENTE.read_text(encoding="utf-8"), re.S).group(1)


def inline(t):
    out = []
    for p in re.split(r"(`[^`]*`)", t):
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append("<code>%s</code>" % html.escape(p[1:-1]))
            continue
        p = html.escape(p, quote=False)
        # las imagenes antes que los enlaces: si no, queda como !<a href>
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


def convertir(md):
    bloques, tabla, parr = [], [], []
    titulo = ""

    def vaciar_p():
        nonlocal parr
        if parr:
            bloques.append("<p>%s</p>" % inline(" ".join(parr)))
            parr = []

    def vaciar_t():
        nonlocal tabla
        if tabla:
            cab, filas = tabla[0], tabla[2:]
            bloques.append(
                '<div class="tw"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                % ("".join("<th>%s</th>" % inline(c) for c in celdas(cab)),
                   "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in celdas(r))
                           for r in filas)))
            tabla = []

    for l in md.split("\n"):
        if l.startswith("|"):
            vaciar_p(); tabla.append(l); continue
        vaciar_t()
        if l.startswith("# "):
            vaciar_p(); titulo = l[2:].strip()
        elif l.startswith("## "):
            vaciar_p(); bloques.append("<h2>%s</h2>" % inline(l[3:].strip()))
        elif l.startswith("### "):
            vaciar_p(); bloques.append("<h3>%s</h3>" % inline(l[4:].strip()))
        elif l.strip() == "---":
            vaciar_p(); bloques.append("<hr>")
        elif l.strip() == "":
            vaciar_p()
        else:
            parr.append(l.strip())
    vaciar_p(); vaciar_t()
    return titulo, "\n".join(bloques)


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    titulo, cuerpo = convertir(src.read_text(encoding="utf-8"))
    doc = ("<!doctype html>\n<html lang=\"es\"><head><meta charset=\"utf-8\">\n"
           "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
           "<title>%s</title>\n<style>%s</style></head><body><main>\n<h1>%s</h1>\n"
           "<p class=\"lead\">Vista de lectura de <a href=\"%s\">%s</a>, que es la fuente de verdad.</p>\n"
           "%s\n</main></body></html>\n"
           % (html.escape(titulo), CSS, html.escape(titulo), src.name, src.name, cuerpo))
    dst.write_text(doc, encoding="utf-8")
    print("escrito %s (%d bytes)" % (dst, len(doc)))


if __name__ == "__main__":
    main()
