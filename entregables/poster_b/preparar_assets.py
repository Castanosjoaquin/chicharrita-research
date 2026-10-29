#!/usr/bin/env python3
"""Compone el encabezado y el pie como imágenes planas a 150 dpi (sin canal alfa).

Parte de las piezas del template del Investigathon (track biotecnología): fondo verde, logo Ŷ e hélice.
Así el PDF final no lleva ninguna imagen con transparencia ni por encima de 150 dpi.
"""
from pathlib import Path
from PIL import Image

A = Path(__file__).parent / "assets"
DPI = 150
mm = lambda v: round(v / 25.4 * DPI)

bg = Image.open(A / "header_bg.jpg").convert("RGB")
logo = Image.open(A / "logo_Y.png").convert("RGBA")
helix = Image.open(A / "icon_helix.png").convert("RGBA")

# encabezado: 841 x 168 mm
W, H = mm(841), mm(168)
h = bg.resize((W, H), Image.LANCZOS)
lh = mm(107)
lw = round(logo.width * lh / logo.height)
l = logo.resize((lw, lh), Image.LANCZOS)
h.paste(l, (mm(24), mm(31)), l)
hw = mm(58)
hh = round(helix.height * hw / helix.width)
x = helix.resize((hw, hh), Image.LANCZOS)
h.paste(x, (W - mm(26) - hw, mm(38)), x)
h.save(A / "header.jpg", quality=92, dpi=(DPI, DPI))

# pie: 841 x 92 mm
f = bg.resize((mm(841), mm(82)), Image.LANCZOS)
f.save(A / "footer.jpg", quality=92, dpi=(DPI, DPI))
print("header.jpg", h.size, "footer.jpg", f.size)
