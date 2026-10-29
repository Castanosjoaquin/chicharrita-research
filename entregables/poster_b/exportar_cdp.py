"""Exporta poster.html a un PDF A0 de una pagina.

Usa CDP (Page.printToPDF con transferMode ReturnAsBase64) porque el Chromium de
este entorno corre con --single-process y el stream de IO.read falla.
Las tipografias quedan incrustadas (no pasadas a curvas: falta pdftocairo).
Uso: python exportar_cdp.py <poster.html> <salida.pdf>
"""
import base64, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

CHROME = str(Path(".pw-browsers/chromium_headless_shell-1194/chrome-mac/headless_shell").resolve())
html, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
PX_MM = 96 / 25.4
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--single-process", "--no-zygote"])
    pg = b.new_page(viewport={"width": round(841 * PX_MM), "height": round(1189 * PX_MM)})
    pg.goto(html.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(1200)
    cdp = pg.context.new_cdp_session(pg)
    r = cdp.send("Page.printToPDF", {"printBackground": True, "preferCSSPageSize": True,
                                     "paperWidth": 841 / 25.4, "paperHeight": 1189 / 25.4,
                                     "marginTop": 0, "marginBottom": 0, "marginLeft": 0, "marginRight": 0,
                                     "transferMode": "ReturnAsBase64", "pageRanges": "1"})
    out.write_bytes(base64.b64decode(r["data"]))
    b.close()

from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
rd = PdfReader(str(out)); w = PdfWriter(); pag = rd.pages[0]
alto = float(pag.mediabox.height)
A0_W, A0_H = 841 / 25.4 * 72, 1189 / 25.4 * 72
caja = RectangleObject([0, alto - A0_H, A0_W, alto])
pag.mediabox = pag.cropbox = pag.trimbox = pag.bleedbox = caja
w.add_page(pag)
w.add_metadata({"/Title": "Decidir mejor sin laboratorio - poster Investigathon Y-Hat - version B"})
with open(out, "wb") as fh:
    w.write(fh)
print("listo:", out, round(out.stat().st_size / 1e6, 2), "MB",
      "| pagina", round(float(PdfReader(str(out)).pages[0].mediabox.width) / 72 * 25.4, 1), "x",
      round(float(PdfReader(str(out)).pages[0].mediabox.height) / 72 * 25.4, 1), "mm")
