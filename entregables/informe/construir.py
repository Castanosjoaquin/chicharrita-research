"""Convierte INFORME.md en informe.pdf (A4): portada, resumen, indice con paginas, cuerpo y anexos.

El markdown es la fuente de verdad; el PDF es la entrega. Las figuras salen de `figuras.py`.
El PDF se imprime con chrome-headless-shell, que viene con las descargas de playwright. El indice
se calcula en dos pasadas: la primera imprime con marcas invisibles en cada titulo y leyenda para
saber en que pagina cae cada uno; la segunda imprime el indice ya con sus numeros.

Uso (desde la raiz del repositorio):
    python entregables/informe/figuras.py
    python entregables/informe/construir.py            # deja informe.pdf
    python entregables/informe/construir.py --html     # deja ademas informe.html (revision)
"""
import base64
import html
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import mistune
import pypdf

AQUI = Path(__file__).resolve().parent
FUENTE = AQUI / "INFORME.md"
PDF_SALIDA = AQUI / "informe.pdf"

TITULO = "Decidir mejor sin laboratorio"
SUBTITULO = "Auditoría computacional de diseños de ARN de doble cadena contra la chicharrita del maíz, <i>Dalbulus maidis</i>"
AUTORES = "Lorenzo Door · Luca Fassio · Santino Cardelli · Joaquín Castaños"
FECHA = "28 de octubre de 2026"

CSS = """
@page { size: A4; margin: 20mm 20mm 21mm 20mm;
  @top-left { content: 'Decidir mejor sin laboratorio'; font: 8pt 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #8a8984; }
  @top-right { content: 'Informe final de investigación'; font: 8pt 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #8a8984; }
  @bottom-center { content: counter(page); font: 9pt 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #6b6a66; }
}
@page :first { margin: 0; @top-left { content: none; } @top-right { content: none; } @bottom-center { content: none; } }
:root { --ink:#1a1a19; --ink2:#52514e; --line:#d9d7cf; --acc:#1f6b4f; --soft:#f4f3ee; }
* { box-sizing: border-box; }
html { font-size: 9.7pt; }
body { margin: 0; color: var(--ink); background: #fff; font-family: Charter, 'Iowan Old Style', Georgia, 'Times New Roman', serif;
  line-height: 1.48; hyphens: auto; -webkit-hyphens: auto; text-align: justify; }
h1,h2,h3,table,figcaption,.refs,.tag,.toc,.cap-tabla { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; text-align: left; hyphens: manual; }
/* portada */
.portada { position: relative; width: 210mm; height: 297mm; overflow: hidden; background: #0b2219; color: #fff; page-break-after: always; break-after: page;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; text-align: left; hyphens: manual; }
.portada svg.arte { position: absolute; inset: 0; width: 210mm; height: 297mm; }
.portada .sup { position: absolute; left: 22mm; right: 22mm; top: 22mm; }
.portada .kicker { font-size: 8.6pt; letter-spacing: .16em; text-transform: uppercase; color: #9fd8bd; }
.portada h1 { font-size: 37pt; line-height: 1.04; margin: 17mm 0 5mm; font-weight: 700; letter-spacing: -.012em; color: #fff; border: 0; padding: 0; max-width: 150mm; }
.portada .repo { font-size: 8.8pt; color: #d6e9df; margin-top: 2.5mm; letter-spacing: .02em; }
.portada .sub { font-size: 13.5pt; line-height: 1.32; color: #cfe6da; max-width: 140mm; }
.portada .inf { position: absolute; left: 22mm; right: 22mm; bottom: 15mm; }
.portada .tipo { font-size: 8.6pt; letter-spacing: .16em; text-transform: uppercase; color: #9fd8bd; margin-bottom: 3mm; }
.portada .autores { font-size: 12pt; font-weight: 600; margin-bottom: 2mm; }
.portada .afil { font-size: 9.2pt; line-height: 1.55; color: #cfe6da; }
/* titulos */
h2 { font-size: 16.5pt; margin: 9mm 0 3.5mm; break-after: avoid; color: var(--ink); letter-spacing: -.005em; }
h2.sinnum { }
h3 { font-size: 11pt; margin: 5mm 0 1.8mm; break-after: avoid; color: var(--acc); }
p { margin: 0 0 2.9mm; orphans: 3; widows: 3; }
ol, ul { margin: 0 0 3.2mm; padding-left: 7mm; }
li { margin-bottom: 1.2mm; }
hr { display: none; }
code { font-family: Menlo, 'SF Mono', Consolas, monospace; font-size: .84em; background: var(--soft); padding: .05em .3em; border-radius: 3px; }
.tag { display: inline-block; font-size: .72em; font-weight: 600; letter-spacing: .02em; padding: 0 .35em; border-radius: 3px; vertical-align: .08em; margin: 0 .08em; white-space: nowrap; }
.tag.E { background: #dfeadf; color: #24592b; } .tag.R { background: #e6eaf6; color: #28458f; }
.tag.M { background: #dbeafc; color: #124b94; } .tag.H { background: #fbe9d3; color: #8a4a05; } .tag.q { background: #eee; color: #444; }
.m { position: absolute; font-size: 2px; line-height: 1; color: #fff; white-space: nowrap; }
/* figuras y tablas */
figure { margin: 4mm 0; break-inside: avoid; text-align: center; }
figure img { max-width: 100%; height: auto; }
figure.f4 img { max-width: 74%; } figure.f6 img, figure.f8 img { max-width: 88%; }
figcaption { font-size: 8.8pt; color: var(--ink2); text-align: left; margin-top: 2mm; line-height: 1.4; }
figcaption b { color: var(--ink); }
.cap-tabla { font-size: 8.8pt; color: var(--ink2); margin: 4mm 0 1.2mm; break-after: avoid; }
.cap-tabla b { color: var(--ink); }
table { border-collapse: collapse; width: 100%; font-size: 8.8pt; margin: 0 0 5mm; }
tr { break-inside: avoid; }
th, td { border-bottom: 1px solid #efeee9; padding: 1.7mm 2.4mm; vertical-align: top; text-align: left; }
th { background: var(--soft); border-bottom: 0; font-weight: 600; }
pre { background: var(--soft); padding: 3mm; font-size: 8.4pt; border-radius: 3px; break-inside: avoid; text-align: left; white-space: pre-wrap; }
pre code { background: none; padding: 0; }
.refs p { font-size: 9.2pt; text-align: left; padding-left: 6mm; text-indent: -6mm; margin-bottom: 2mm; hyphens: manual; }
/* indice */
.pagina { break-before: page; }
.toc h3.lista { font-size: 10pt; color: var(--ink); margin: 3mm 0 1mm; }
.toc .fila { display: flex; align-items: baseline; font-size: 8.2pt; line-height: 1.28; }
.toc .fila .t { flex: 0 1 auto; }
.toc .fila .p { flex: 0 0 auto; margin-left: auto; padding-left: 2mm; font-variant-numeric: tabular-nums; }
.toc .fila .d { flex: 1 1 auto; }
.toc .n1 { font-weight: 600; margin-top: 1.1mm; }
.toc .n2 { padding-left: 6mm; color: var(--ink2); }
"""

MARCAS = {"E": "E", "R": "R", "M": "M", "H": "H", "?": "q"}


def texto_plano(t):
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(t).strip()


class Render(mistune.HTMLRenderer):
    def __init__(self, marcar):
        super().__init__(escape=False)
        self.marcar = marcar
        self.titulos = []   # (id, nivel, texto)
        self.figuras = []   # (id, texto)
        self.tablas = []    # (id, texto)

    def _marca(self, ident):
        return f'<span class="m">§§{ident}§§</span>' if self.marcar else ""

    def codespan(self, text):
        t = html.unescape(text)
        m = re.fullmatch(r"\[([ERMH?])\]", t)
        if m:
            return f'<span class="tag {MARCAS[m.group(1)]}">[{m.group(1)}]</span>'
        return f"<code>{text}</code>"

    def heading(self, text, level, **attrs):
        ident = f"h{len(self.titulos)}"
        plano = texto_plano(text)
        self.titulos.append((ident, level, plano))
        clase = "" if re.match(r"\d", plano) else ' class="sinnum"'
        return f'<h{level} id="{ident}"{clase}>{self._marca(ident)}{text}</h{level}>\n'

    def paragraph(self, text):
        m = re.fullmatch(r'\s*<img src="([^"]+)" alt="([^"]*)"[^>]*/?>\s*', text)
        if m:
            ruta = AQUI / m.group(1)
            datos = base64.b64encode(ruta.read_bytes()).decode()
            cap = re.sub(r"^(Figura \d+\.)", r"<b>\1</b>", m.group(2))
            n = re.search(r"fig(\d)_", m.group(1)).group(1)
            ident = f"f{n}"
            self.figuras.append((ident, texto_plano(m.group(2))))
            return (f'<figure class="f{n}" id="{ident}"><img src="data:image/png;base64,{datos}" alt=""/>'
                    f'<figcaption>{self._marca(ident)}{cap}</figcaption></figure>\n')
        m = re.match(r"\s*<strong>(Tabla (\d+)\.)</strong>(.*)", text, re.S)
        if m:
            ident = f"t{m.group(2)}"
            self.tablas.append((ident, texto_plano(text)))
            return f'<p class="cap-tabla" id="{ident}">{self._marca(ident)}<b>{m.group(1)}</b>{m.group(3)}</p>\n'
        return f"<p>{text}</p>\n"

    def image(self, text, url, title=None):
        return f'<img src="{url}" alt="{text}"/>'


def helice(x0, x1, cy, amp, onda, fase=0.0, paso=0.6):
    """Puntos de las dos hebras de la doble helice y de los peldaños (pares de bases)."""
    a, b, peldanos = [], [], []
    n = int((x1 - x0) / paso)
    for i in range(n + 1):
        x = x0 + i * paso
        s = math.sin(2 * math.pi * (x - x0) / onda + fase)
        a.append((x, cy + amp * s, s))
        b.append((x, cy - amp * s, -s))
    k = 0
    x = x0 + onda / 24
    while x < x1:
        s = math.sin(2 * math.pi * (x - x0) / onda + fase)
        peldanos.append((x, cy + amp * s, cy - amp * s, s))
        x += onda / 12
        k += 1
    return a, b, peldanos


def arte_portada():
    """Ilustracion de la portada: una doble helice de ARN con una ventana de 21 nt, hojas de maiz y la chicharrita."""
    cx, cy = 105, 165
    a, b, peldanos = helice(12, 198, cy, 15, 46, fase=0.4)

    def tramos(pts, frente):
        # dibuja la hebra en tramos para dar profundidad: de frente, mas gruesa y clara
        out = []
        for i in range(len(pts) - 1):
            x1, y1, s1 = pts[i]
            x2, y2, s2 = pts[i + 1]
            esta_al_frente = (s1 + s2) / 2 > 0
            if esta_al_frente == frente:
                out.append((x1, y1, x2, y2))
        return out

    partes = []
    # hebra posterior (tenue) y peldaños
    for (x1, y1, x2, y2) in tramos(a, False) + tramos(b, False):
        partes.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#2f8f6b" stroke-width="1.1" stroke-linecap="round" opacity=".55"/>')
    for (x, ya, yb, s) in peldanos:
        partes.append(f'<line x1="{x:.2f}" y1="{ya:.2f}" x2="{x:.2f}" y2="{yb:.2f}" stroke="#bfe3d1" stroke-width=".7" opacity="{0.25 + 0.4 * abs(s):.2f}"/>')
        partes.append(f'<circle cx="{x:.2f}" cy="{ya:.2f}" r=".9" fill="#f6b38f" opacity=".85"/><circle cx="{x:.2f}" cy="{yb:.2f}" r=".9" fill="#9fd8bd" opacity=".85"/>')
    # hebras frontales
    for (x1, y1, x2, y2) in tramos(a, True):
        partes.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#ee7a4a" stroke-width="2.1" stroke-linecap="round"/>')
    for (x1, y1, x2, y2) in tramos(b, True):
        partes.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#7fd6b0" stroke-width="2.1" stroke-linecap="round"/>')
    helice_svg = "\n".join(partes)

    return f"""
<svg class="arte" viewBox="0 0 210 297" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
  <defs>
    <linearGradient id="fondo" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0b2219"/><stop offset=".55" stop-color="#103a2d"/><stop offset="1" stop-color="#0b2219"/>
    </linearGradient>
    <radialGradient id="brillo" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="#2fa37a" stop-opacity=".42"/><stop offset="1" stop-color="#2fa37a" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="210" height="297" fill="url(#fondo)"/>
  <circle cx="{cx}" cy="{cy}" r="96" fill="url(#brillo)"/>
  <g transform="rotate(-9 {cx} {cy})">
    {helice_svg}
    <rect x="{cx - 21}" y="{cy - 24}" width="42" height="48" rx="5" fill="#ffffff" fill-opacity=".06" stroke="#f3c969" stroke-width=".7" stroke-dasharray="2.2 1.6"/>
  </g>
  <!-- hojas de maiz -->
  <path d="M-6 258 C18 222 56 204 110 198 C74 214 50 232 34 258 Z" fill="#17583e"/>
  <path d="M-6 258 C22 226 58 208 104 201" stroke="#3aa174" stroke-width=".5" fill="none" opacity=".7"/>
  <path d="M40 258 C72 227 114 210 176 211 C134 221 104 238 88 258 Z" fill="#1e7552"/>
  <path d="M44 258 C76 230 116 214 170 213" stroke="#59bf90" stroke-width=".5" fill="none" opacity=".7"/>
  <path d="M112 258 C138 238 170 228 214 228 C182 238 166 248 156 258 Z" fill="#2d9568"/>
  <!-- la chicharrita, sobre la hoja -->
  <g transform="translate(150 207) rotate(-9) scale(1.25)">
    <line x1="-4" y1="2" x2="-7.5" y2="6.6" stroke="#e9e3c8" stroke-width=".55" stroke-linecap="round"/>
    <line x1="0" y1="2.2" x2="-1.6" y2="7" stroke="#e9e3c8" stroke-width=".55" stroke-linecap="round"/>
    <line x1="4" y1="2" x2="4.8" y2="6.6" stroke="#e9e3c8" stroke-width=".55" stroke-linecap="round"/>
    <path d="M-10 0.2 C-7 -3.4 4 -3.6 9.4 -1.2 L12.6 0.4 C10 2.6 -4 3.2 -10 0.2 Z" fill="#e9e3c8"/>
    <path d="M-9 -0.6 C-3 -6.6 7 -5.8 11 -1.4 C5 -2.4 -3 -1.8 -9 -0.6 Z" fill="#bfe3d1" fill-opacity=".85"/>
    <circle cx="12.4" cy="0" r="1.9" fill="#e9e3c8"/><circle cx="13" cy="-.5" r=".35" fill="#0b2219"/>
    <line x1="14" y1="-1.2" x2="16.6" y2="-3.4" stroke="#e9e3c8" stroke-width=".3"/>
  </g>
  <!-- franja inferior -->
  <rect y="256" width="210" height="41" fill="#0b2219" fill-opacity=".94"/>
</svg>"""


def portada():
    return (f'<section class="portada">{arte_portada()}'
            f'<div class="sup"><div class="kicker">Biotecnología · ARN de interferencia · Achaparramiento del maíz</div>'
            f'<div class="repo">Repositorio · github.com/Castanosjoaquin/chicharrita-research</div>'
            f'<h1>{TITULO}</h1><div class="sub">{SUBTITULO}</div></div>'
            f'<div class="inf"><div class="tipo">Informe final de investigación</div>'
            f'<div class="autores">{AUTORES}</div>'
            f'<div class="afil">Ingeniería en Inteligencia Artificial, Universidad de San Andrés<br>{FECHA}</div></div>'
            f'</section>')


def titulo_corto(texto):
    m = re.match(r"((?:Figura|Tabla) \d+\.\s*.+?\.)(\s|$)", texto)
    return m.group(1) if m else texto[:110]


def indice(titulos, figuras, tablas, paginas):
    def fila(ident, texto, clase):
        p = paginas.get(ident, "00")
        return (f'<div class="fila {clase}"><span class="t">{html.escape(texto)}</span><span class="d"></span>'
                f'<span class="p">{p}</span></div>')

    partes = ['<section class="toc pagina"><h2 class="sinnum">Índice</h2>']
    for ident, nivel, texto in titulos:
        partes.append(fila(ident, texto, "n1" if nivel == 2 else "n2"))
    partes.append('<h3 class="lista">Índice de figuras</h3>')
    for ident, texto in figuras:
        partes.append(fila(ident, titulo_corto(texto), "n2"))
    partes.append('<h3 class="lista">Índice de tablas</h3>')
    for ident, texto in tablas:
        partes.append(fila(ident, titulo_corto(texto), "n2"))
    partes.append("</section>")
    return "\n".join(partes)


def pagina_html(cuerpo_md, marcar, paginas):
    r = Render(marcar)
    md = mistune.create_markdown(renderer=r, plugins=["table", "strikethrough"])
    cuerpo = md(cuerpo_md)
    cuerpo = cuerpo.replace('<h2 id="h0" class="sinnum">', '<h2 id="h0" class="sinnum">', 1)
    cuerpo = re.sub(r'(<h2 id="h\d+" class="sinnum">(?:<span class="m">[^<]*</span>)?Referencias</h2>)', r'\1<div class="refs">', cuerpo, count=1)
    cuerpo += "</div>"
    # el abstract va en la misma pagina que el resumen; el cuerpo arranca en pagina nueva despues del indice
    # separar: el resumen y el cuerpo, que arranca en pagina nueva despues del indice
    ident_intro = next(i for i, _, t in r.titulos if t.startswith("1. Introducción"))
    cuerpo = cuerpo.replace(f'<h2 id="{ident_intro}"', f'<h2 id="{ident_intro}" style="break-before: page"', 1)
    i = cuerpo.index(f'<h2 id="{ident_intro}"')
    front, resto = cuerpo[:i], cuerpo[i:]
    pag = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{TITULO}: informe final</title>'
           f"<style>{CSS}</style></head><body>{portada()}"
           f'<section class="pagina">{front}</section>'
           f"{indice(r.titulos, r.figuras, r.tablas, paginas)}{resto}</body></html>")
    return pag, r


def imprimir(pagina, salida):
    # playwright guarda sus descargas en Library/Caches en macOS y en AppData/Local en Windows
    shell = next((p for raiz in ("Library/Caches/ms-playwright", "AppData/Local/ms-playwright")
                  for p in Path.home().glob(f"{raiz}/chromium_headless_shell-*/*/chrome-headless-shell*")
                  if p.suffix in ("", ".exe")), None)
    if shell is None:
        sys.exit("falta chrome-headless-shell (viene con playwright)")
    with tempfile.TemporaryDirectory() as d:
        h = Path(d) / "informe.html"
        h.write_text(pagina, encoding="utf-8")
        subprocess.run([str(shell), "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={salida}", h.as_uri()], check=True, capture_output=True)


def paginas_de_marcas(pdf):
    paginas = {}
    for n, pg in enumerate(pypdf.PdfReader(str(pdf)).pages, 1):
        for ident in re.findall(r"§§([htf]\d+)§§", pg.extract_text() or ""):
            paginas.setdefault(ident, str(n))
    return paginas


def construir(con_html=False):
    cuerpo_md = FUENTE.read_text(encoding="utf-8")
    prov = Path(tempfile.mkdtemp()) / "pasada1.pdf"
    p1, r = pagina_html(cuerpo_md, True, {})
    imprimir(p1, prov)
    paginas = paginas_de_marcas(prov)
    # la tabla de contenidos no tiene marcas: verificar que todo titulo, figura y tabla se encontro
    esperados = [i for i, _, _ in r.titulos] + [i for i, _ in r.figuras] + [i for i, _ in r.tablas]
    faltan = [i for i in esperados if i not in paginas]
    if faltan:
        sys.exit(f"no se encontro la pagina de: {faltan}")
    p2, _ = pagina_html(cuerpo_md, False, paginas)
    imprimir(p2, PDF_SALIDA)
    n1 = len(pypdf.PdfReader(str(prov)).pages)
    n2 = len(pypdf.PdfReader(str(PDF_SALIDA)).pages)
    if n1 != n2:
        sys.exit(f"la segunda pasada cambio el numero de paginas ({n1} -> {n2}); los numeros del indice no valen")
    if con_html:
        (AQUI / "informe.html").write_text(p2, encoding="utf-8")
    print(f"pdf: {PDF_SALIDA} ({n2} paginas)")


if __name__ == "__main__":
    construir("--html" in sys.argv)
