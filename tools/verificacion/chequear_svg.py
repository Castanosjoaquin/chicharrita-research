"""Chequeos numericos de los SVG embebidos en nuestras paginas HTML.

Existe porque la verificacion visual no siempre esta disponible: el rasterizado
local no funciona (faltan las DLL de cairo) y la extension del navegador responde
de forma intermitente. Esto no reemplaza mirar la pagina, pero atrapa la clase de
error que mirar por encima deja pasar: una marca ubicada donde no corresponde segun
su propia escala, un texto fuera del viewBox, una clase sin regla CSS.

Lo que chequea:
  - toda clase usada tiene regla CSS, y toda variable CSS usada esta definida;
  - nada se sale del viewBox, ni los rectangulos por su ancho o alto;
  - colisiones aproximadas entre textos y entre texto y marca, **heredando**
    font-size y text-anchor del <g> que los contiene, que es donde la version
    anterior de este chequeo se equivocaba y daba falsos positivos.

El ancho de texto es una estimacion (0,55 em por caracter), asi que una colision
reportada hay que mirarla, no corregirla a ciegas.

    python tools/verificacion/chequear_svg.py <archivo.html> [...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

EM = 0.55          # ancho medio por caracter, en fracciones del font-size
HOLGURA = 1.0      # px de solape que no se reporta


def _caja_texto(x, y, txt, fs, anchor):
    w = len(txt) * fs * EM
    x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
    return (x0, y - fs * 0.85, x0 + w, y + fs * 0.2)


def _solapan(a, b):
    return (min(a[2], b[2]) - max(a[0], b[0]) > HOLGURA
            and min(a[3], b[3]) - max(a[1], b[1]) > HOLGURA)


def _textos_con_herencia(svg: str):
    """(caja, texto) de cada <text>, heredando font-size y text-anchor del <g>.

    Es la parte que importa: en estas paginas los ejes se escriben como un solo
    <g font-size="11" text-anchor="end"> con varios <text> adentro que no repiten
    esos atributos. Leerlos sin la herencia infla el ancho y mueve el anclaje, y
    aparecen colisiones que no existen.
    """
    fs_pila, an_pila = [12.0], ["start"]
    out = []
    for m in re.finditer(r'<(/?)(g|text)([^>]*?)(/?)>([^<]*)', svg):
        cierra, tag, attrs, auto, cuerpo = m.groups()
        if tag == "g":
            if cierra:
                if len(fs_pila) > 1:
                    fs_pila.pop(); an_pila.pop()
            else:
                fs = re.search(r'font-size="([\d.]+)"', attrs)
                an = re.search(r'text-anchor="(\w+)"', attrs)
                fs_pila.append(float(fs.group(1)) if fs else fs_pila[-1])
                an_pila.append(an.group(1) if an else an_pila[-1])
            continue
        if cierra or "transform" in attrs:
            continue
        txt = cuerpo.strip()
        x = re.search(r'\bx="([-\d.]+)"', attrs)
        y = re.search(r'\by="([-\d.]+)"', attrs)
        if not (txt and x and y):
            continue
        fs = re.search(r'font-size="([\d.]+)"', attrs)
        an = re.search(r'text-anchor="(\w+)"', attrs)
        out.append((_caja_texto(float(x.group(1)), float(y.group(1)), txt,
                                float(fs.group(1)) if fs else fs_pila[-1],
                                an.group(1) if an else an_pila[-1]), txt))
    return out


def chequear(ruta: Path) -> list[str]:
    s = ruta.read_text(encoding="utf-8")
    fallas = []

    estilo = re.search(r"<style>(.*?)</style>", s, re.S)
    if estilo:
        css = estilo.group(1)
        definidas = set(re.findall(r"\.([a-z][a-z0-9_-]*)", css))
        usadas = set()
        for m in re.finditer(r'class="([^"]+)"', s):
            usadas |= set(m.group(1).split())
        if usadas - definidas:
            fallas.append("clases sin regla CSS: %s" % sorted(usadas - definidas))
        var_def = set(re.findall(r"(--[a-z0-9-]+)\s*:", css))
        var_uso = set(re.findall(r"var\((--[a-z0-9-]+)\)", s))
        if var_uso - var_def:
            fallas.append("variables CSS sin definir: %s" % sorted(var_uso - var_def))

    for i, (W, H, cuerpo) in enumerate(
            re.findall(r'<svg viewBox="0 0 (\d+) (\d+)"(.*?)</svg>', s, re.S)):
        W, H = int(W), int(H)
        for attr, lim in (("x", W), ("y", H)):
            for m in re.finditer(r'\b%s(?:1|2)?="(-?[\d.]+)"' % attr, cuerpo):
                v = float(m.group(1))
                if not -1 <= v <= lim + 1:
                    fallas.append("svg %d: %s=%s fuera del viewBox %dx%d" % (i, attr, v, W, H))
        for m in re.finditer(r'<rect[^>]*x="([\d.]+)"[^>]*width="([\d.]+)"', cuerpo):
            if float(m.group(1)) + float(m.group(2)) > W + 1:
                fallas.append("svg %d: un rect se pasa del ancho" % i)
        for m in re.finditer(r'<rect[^>]*y="([\d.]+)"[^>]*height="([\d.]+)"', cuerpo):
            if float(m.group(1)) + float(m.group(2)) > H + 1:
                fallas.append("svg %d: un rect se pasa del alto" % i)

        cajas = _textos_con_herencia(cuerpo)
        marcas = [(float(a) - float(r), float(b) - float(r),
                   float(a) + float(r), float(b) + float(r))
                  for a, b, r in re.findall(
                      r'<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"', cuerpo)]
        for a in range(len(cajas)):
            for b in range(a + 1, len(cajas)):
                if _solapan(cajas[a][0], cajas[b][0]):
                    fallas.append("svg %d: se pisan los textos %r y %r"
                                  % (i, cajas[a][1], cajas[b][1]))
            for mk in marcas:
                if _solapan(cajas[a][0], mk):
                    fallas.append("svg %d: el texto %r se pisa con una marca"
                                  % (i, cajas[a][1]))
    return fallas


def main(argv=None) -> int:
    rutas = [Path(p) for p in (argv or sys.argv[1:])]
    if not rutas:
        sys.exit(__doc__)
    total = 0
    for r in rutas:
        fallas = chequear(r)
        total += len(fallas)
        print("%s: %s" % (r, "sin fallas" if not fallas else "%d fallas" % len(fallas)))
        for f in fallas:
            print("   -", f)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
