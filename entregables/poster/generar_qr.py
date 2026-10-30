#!/usr/bin/env python3
"""Regenera los dos QR del pie del poster, en SVG, a partir de las URL de abajo.

Los SVG salen sin borde (`border=0`) porque el margen blanco se lo da el `.tile`
del CSS, que son 3 mm de `padding` dentro de un cuadro de 50 mm: el QR impreso
mide 44 x 44 mm. El color es el verde oscuro del poster.

Las dos URL viven en un repositorio **privado**: los QR no resuelven hasta que
el duenio lo haga publico (D106). Verificar con `curl` antes de mandar a imprenta:

    curl -s -o /dev/null -w "%{http_code}\\n" <url>   # 200 = sirve, 404 = todavia no

Uso: python generar_qr.py
"""
from pathlib import Path

import segno

AQUI = Path(__file__).parent
TINTA = "#0f2622"  # var(--vd) del poster
LADO_MM = 44.0  # el .tile son 50 mm con 3 mm de padding

# `blob/main` y no `raw`: GitHub lo muestra en su visor en vez de bajarlo, y al
# apuntar a `main` el QR sigue al informe si el PDF cambia antes de la entrega.
URLS = {
    "qr_repo.svg": "https://github.com/Castanosjoaquin/chicharrita-research",
    "qr_informe.svg": (
        "https://github.com/Castanosjoaquin/chicharrita-research"
        "/blob/main/entregables/informe/informe.pdf"
    ),
}


def main() -> None:
    for nombre, url in URLS.items():
        # `error="m"` recupera hasta el 15 % del codigo: es lo que aguanta un
        # poster rozado o con un reflejo encima, sin inflar la cuadricula como "q".
        qr = segno.make(url, error="m")
        destino = AQUI / "assets" / nombre
        # `xmldecl=False` para que la salida sea byte a byte la de los SVG que ya
        # estaban en `assets/`: con la cabecera XML, `qr_repo.svg` cambiaba sin
        # que cambiara el codigo, y asi el diff muestra solo lo que de verdad cambio.
        qr.save(
            destino,
            kind="svg",
            border=0,
            dark=TINTA,
            svgclass="segno",
            lineclass="qrline",
            xmldecl=False,
        )
        modulos = qr.symbol_size(border=0)[0]
        print(
            f"{nombre}: version {qr.version}, {modulos}x{modulos} modulos, "
            f"{LADO_MM / modulos:.2f} mm por modulo impreso\n  {url}"
        )


if __name__ == "__main__":
    main()
