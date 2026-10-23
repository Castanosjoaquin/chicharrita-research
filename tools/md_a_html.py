"""Convierte un .md del repo a un .html autocontenido, con el CSS de C7.

El markdown es la fuente de verdad; el HTML es solo la vista de lectura. Soporta
titulos, parrafos, tablas, imagenes, enlaces, negrita, cursiva, tachado, codigo en
linea, bloques de codigo con cercas (```), listas con viñeta y numeradas, citas (`>`)
y lineas horizontales. No es un conversor general: cubre lo que usan los documentos de este
repositorio.

Las cercas y las listas se agregaron en la ola 4: antes el contenido de un bloque de
codigo se unia en un solo parrafo y los comandos de varias lineas quedaban ilegibles
en la vista de lectura.

Las citas se agregaron en la linea M8: antes un `> ` quedaba como un `&gt;` literal
al principio de cada linea.

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


VINETA = re.compile(r"^[-*] +(.*)$")
NUMERADA = re.compile(r"^\d+\. +(.*)$")
# Regla horizontal: tres o mas del mismo caracter, con o sin espacios. Hay que
# mirarla **antes** que la viñeta, porque `* * *` y `- - -` son reglas y no items.
REGLA = re.compile(r"^([-*_])( *\1){2,} *$")
# Cita: el `>` tiene que abrir la linea. Los informes escriben ordenes como
# `BicC_Dm > CP_MRFV` en medio de un parrafo, y eso no es una cita.
CITA = re.compile("^>( .*)?$")
CERCA = "```"


def sangria(l):
    return len(l) - len(l.lstrip())


def marca(l):
    """('ul'|'ol', texto del item) si la linea abre un item; None si no."""
    s = l.strip()
    if REGLA.match(s):
        return None
    m = VINETA.match(s)
    if m:
        return "ul", m.group(1).strip()
    m = NUMERADA.match(s)
    if m:
        return "ol", m.group(1).strip()
    return None


def bloque_lista(lineas):
    """Convierte un bloque de lista, con anidado y cercas adentro de los items.

    Las lineas vienen sin blancos. Un item arranca con un marcador a la sangria
    minima del bloque; todo lo que sigue hasta el proximo marcador de ese nivel es
    contenido del item: lineas de continuacion, una cerca de codigo o una sublista,
    que se resuelve recursivamente. Limitacion declarada: una continuacion de texto
    que venga **despues** de una sublista se renderiza antes que ella.
    """
    base = min(sangria(l) for l in lineas)
    tipo = marca(lineas[0])[0]
    items = []
    for l in lineas:
        mk = marca(l)
        if mk and sangria(l) <= base:
            items.append({"texto": [mk[1]], "resto": []})
        elif items:
            items[-1]["resto"].append(l)
    return "<%s>%s</%s>" % (
        tipo, "".join("<li>%s</li>" % contenido_item(i) for i in items), tipo)


def contenido_item(item):
    texto, extra, resto, i = list(item["texto"]), [], item["resto"], 0
    while i < len(resto):
        if resto[i].strip().startswith(CERCA):
            j, cuerpo = i + 1, []
            while j < len(resto) and not resto[j].strip().startswith(CERCA):
                cuerpo.append(resto[j]); j += 1
            extra.append("<pre>%s</pre>" % html.escape(desangrar(cuerpo)))
            i = j + 1
        elif marca(resto[i]):
            j = i
            while j < len(resto) and not resto[j].strip().startswith(CERCA):
                j += 1
            extra.append(bloque_lista(resto[i:j]))
            i = j
        else:
            texto.append(resto[i].strip()); i += 1
    return inline(" ".join(texto)) + "".join(extra)


def desangrar(lineas):
    """Saca la sangria comun, para que una cerca indentada no quede corrida."""
    while lineas and not lineas[-1].strip():
        lineas = lineas[:-1]
    utiles = [l for l in lineas if l.strip()]
    corte = min((sangria(l) for l in utiles), default=0)
    return "\n".join(l[corte:] if l.strip() else "" for l in lineas)


def convertir(md):
    bloques, tabla, parr, lbuf, cita = [], [], [], [], []
    cerca, cerca_abierta = [], False
    blanco_pendiente = False
    titulo = ""

    def vaciar_p():
        nonlocal parr
        if parr:
            bloques.append("<p>%s</p>" % inline(" ".join(parr)))
            parr = []

    def vaciar_l():
        nonlocal lbuf
        if lbuf:
            bloques.append(bloque_lista(lbuf))
            lbuf = []

    def vaciar_c():
        nonlocal cita
        if cita:
            bloques.append("<blockquote><p>%s</p></blockquote>" % inline(" ".join(cita)))
            cita = []

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

    BLOQUE = ("# ", "## ", "### ", "|", CERCA, ">")
    for l in md.split("\n"):
        if cerca_abierta:
            if l.strip().startswith(CERCA):
                bloques.append("<pre>%s</pre>" % html.escape(desangrar(cerca)))
                cerca, cerca_abierta = [], False
            else:
                cerca.append(l)
            continue
        # Un blanco con la lista abierta no la cierra todavia: si lo que sigue viene
        # indentado o es otro marcador, la lista continua, que es lo que markdown
        # hace con una lista de items separados por blancos.
        if lbuf and not l.strip():
            blanco_pendiente = True
            continue
        # Con una lista abierta, todo lo indentado y todo marcador es contenido de
        # la lista: tambien una cerca, que si no cerraria el item y reiniciaria la
        # numeracion. Una linea sin sangria que no abre otro bloque es una
        # continuacion perezosa, que es lo que markdown hace con ella.
        if lbuf and l.strip():
            mk = marca(l)
            # Cambiar de viñeta a numerada al mismo nivel son dos listas, no una.
            if mk and sangria(l) <= min(sangria(x) for x in lbuf) \
                    and mk[0] != marca(lbuf[0])[0]:
                vaciar_l(); blanco_pendiente = False
                vaciar_p(); lbuf.append(l); continue
            if mk or sangria(l) > 0:
                blanco_pendiente = False
                lbuf.append(l); continue
            # Sin blanco de por medio es una continuacion perezosa del item; con un
            # blanco, markdown abre un parrafo nuevo y la lista se cierra.
            if not blanco_pendiente and not (
                    l.startswith(BLOQUE) or REGLA.match(l.strip())):
                lbuf.append(l); continue
        blanco_pendiente = False
        cit = CITA.match(l)
        if cit:
            vaciar_p(); vaciar_l(); vaciar_t()
            cita.append((cit.group(1) or "").strip())
            continue
        vaciar_c()
        if l.strip().startswith(CERCA):
            vaciar_p(); vaciar_l(); vaciar_t()
            cerca_abierta = True
            continue
        if l.startswith("|"):
            vaciar_p(); vaciar_l(); tabla.append(l); continue
        vaciar_t()
        if l.startswith("# "):
            vaciar_p(); vaciar_l(); titulo = l[2:].strip()
        elif l.startswith("## "):
            vaciar_p(); vaciar_l(); bloques.append("<h2>%s</h2>" % inline(l[3:].strip()))
        elif l.startswith("### "):
            vaciar_p(); vaciar_l(); bloques.append("<h3>%s</h3>" % inline(l[4:].strip()))
        elif REGLA.match(l.strip()):
            vaciar_p(); vaciar_l(); bloques.append("<hr>")
        elif marca(l):
            vaciar_p(); lbuf.append(l)
        elif l.strip() == "":
            vaciar_p(); vaciar_l()
        else:
            vaciar_l(); parr.append(l.strip())
    if cerca_abierta:
        bloques.append("<pre>%s</pre>" % html.escape(desangrar(cerca)))
    vaciar_p(); vaciar_l(); vaciar_c(); vaciar_t()
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
