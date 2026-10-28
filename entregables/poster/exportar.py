#!/usr/bin/env python3
"""Genera el PDF de impresión: A0 vertical, una página, fuentes en curvas.

1. Chromium imprime poster.html a un PDF A0 (las fuentes quedan incrustadas).
2. pdftocairo (poppler) pasa ese PDF a SVG: cada glifo se vuelve un trazado, así que no queda ninguna fuente.
3. Chromium imprime ese SVG a un PDF A0 final, sin fuentes.

Uso: python exportar.py <directorio_de_trabajo> <pdf_final>
"""
import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).parent.resolve()
trabajo = Path(sys.argv[1]).resolve()
final = Path(sys.argv[2]).resolve()
trabajo.mkdir(parents=True, exist_ok=True)
crudo = trabajo / "poster_crudo.pdf"
svg = trabajo / "poster_curvas.svg"
PX_MM = 96 / 25.4

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": round(841 * PX_MM), "height": round(1189 * PX_MM)})
    pg.goto((AQUI / "poster.html").as_uri())
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(800)
    pg.pdf(path=str(crudo), width="841mm", height="1189mm", print_background=True, prefer_css_page_size=True)
    subprocess.run(["pdftocairo", "-svg", str(crudo), str(svg)], check=True)
    pg2 = b.new_page()
    pg2.goto(svg.as_uri())
    pg2.wait_for_timeout(1500)
    pg2.pdf(path=str(final), width="841mm", height="1189mm", print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}, page_ranges="1")
    b.close()

# Chromium redondea la página a píxeles (841,4 x 1189,2 mm): se recorta al A0 exacto, 841 x 1189 mm.
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
r = PdfReader(str(final))
w = PdfWriter()
pag = r.pages[0]
alto = float(pag.mediabox.height)
A0_W, A0_H = 841 / 25.4 * 72, 1189 / 25.4 * 72
caja = RectangleObject([0, alto - A0_H, A0_W, alto])
pag.mediabox = caja
pag.cropbox = caja
pag.trimbox = caja
pag.bleedbox = caja
w.add_page(pag)
w.add_metadata({"/Title": "Decidir mejor sin laboratorio — póster Investigathon Y-Hat"})
with open(final, "wb") as fh:
    w.write(fh)
print("listo:", final)
