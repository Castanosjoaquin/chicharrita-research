#!/usr/bin/env python3
"""Renderiza poster.html con Chromium: vista previa PNG, chequeo de desborde y PDF A0 crudo.

Uso: python render.py <salida_dir> [escala_png]
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).parent
out = Path(sys.argv[1])
esc = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3
out.mkdir(parents=True, exist_ok=True)
PX_MM = 96 / 25.4

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": round(841 * PX_MM), "height": round(1189 * PX_MM)}, device_scale_factor=esc)
    pg.goto((AQUI / "poster.html").as_uri())
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(800)
    info = pg.evaluate("""() => {
      const mm = v => v / (96 / 25.4);
      const main = document.querySelector('main').getBoundingClientRect();
      const pie = document.querySelector('.pie').getBoundingClientRect();
      const out = {main_bottom_mm: mm(main.bottom), pie_top_mm: mm(pie.top), paneles: []};
      document.querySelectorAll('.pan, .hilo').forEach(e => {
        const r = e.getBoundingClientRect();
        out.paneles.push([e.querySelector('h2') ? e.querySelector('h2').innerText.slice(0, 28) : 'hilo', Math.round(mm(r.top)), Math.round(mm(r.bottom)), Math.round(mm(r.left)), Math.round(mm(r.right))]);
      });
      const fonts = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + f.weight + f.style);
      out.fonts = fonts;
      return out;
    }""")
    print("main termina en", round(info["main_bottom_mm"], 1), "mm; el pie empieza en", round(info["pie_top_mm"], 1), "mm")
    for n in info["paneles"]:
        print("  ", n)
    print("fuentes cargadas:", len(info["fonts"]))
    pg.screenshot(path=str(out / "preview.png"), full_page=False)
    pg.pdf(path=str(out / "poster_crudo.pdf"), width="841mm", height="1189mm", print_background=True, prefer_css_page_size=True)
    b.close()
