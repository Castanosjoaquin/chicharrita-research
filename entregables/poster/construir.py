#!/usr/bin/env python3
"""Arma poster.html (A0 vertical, 841 x 1189 mm) con las figuras en SVG.

Todas las cifras salen de los entregables versionados; cada panel dice de cuál.
Las figuras se dibujan acá con coordenadas en milímetros (1 unidad = 1 mm), así
que el tamaño de letra de una figura se piensa en puntos con pt().
"""
import math
import re
from pathlib import Path

AQUI = Path(__file__).parent

INK = "#14241f"
VERDE_OSC = "#0f2a26"
VERDE = "#2f6b57"
SALVIA = "#9db8a6"
SALVIA_CL = "#dfe8dc"
PAPEL = "#f7f5ef"
OXIDO = "#b5502a"
OCRE = "#c58a1a"
AZUL = "#2a6f8f"
VIOLETA = "#6a4f9c"
GRIS = "#6a756f"
LINEA = "#c9c4b6"


ESCALA_TEXTO = 1.15   # los textos de figura (<= 20 pt) se agrandan un poco: el A0 se lee de lejos


def pt(p):
    return round(p * 0.3528, 3)


def T(x, y, s, size=16, w=500, anchor="start", fill=INK, mono=False, italic=False, halo=False):
    fam = "'IBM Plex Mono',Menlo,monospace" if mono else "Montserrat,'Helvetica Neue',Arial,sans-serif"
    st = "italic" if italic else "normal"
    hc = halo if isinstance(halo, str) else PAPEL
    h = f' stroke="{hc}" stroke-width="2.2" stroke-linejoin="round" paint-order="stroke"' if halo else ""
    if size <= 20:
        size = size * ESCALA_TEXTO
    return (f'<text x="{x}" y="{y}" font-size="{pt(size)}" font-weight="{w}" text-anchor="{anchor}" '
            f'fill="{fill}" font-family="{fam}" font-style="{st}"{h}>{s}</text>')


def sp(nombre):
    """Nombre de especie en cursiva dentro de un texto SVG."""
    return f'<tspan font-style="italic">{nombre}</tspan>'


def fig(w, h, body, defs=""):
    return (f'<svg class="fig" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}mm" height="{h}mm"><defs>{defs}</defs>{body}</svg>')


def rayado(cid, x, y, w, h, color, borde, paso=3.2, grosor=0.9):
    """Rectángulo rayado a 45°, dibujado con líneas recortadas: vectorial puro, sin patrones ni transparencias."""
    n = int((w + h) / paso) + 1
    ls = "".join(f'<line x1="{x + k * paso - h:.2f}" y1="{y + h:.2f}" x2="{x + k * paso:.2f}" y2="{y:.2f}"/>' for k in range(n))
    return (f'<clipPath id="{cid}"><rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}"/></clipPath>'
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{PAPEL}"/>'
            f'<g clip-path="url(#{cid})" stroke="{color}" stroke-width="{grosor}">{ls}</g>'
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="none" stroke="{borde}" stroke-width=".6"/>')


# ---------------------------------------------------------------- figura 1
def fig1():
    W, H = 253, 92
    b = []

    def virus(cx, cy, r=11):
        pts = " ".join(f"{cx + r * math.cos(math.radians(60 * i + 30)):.2f},{cy + r * math.sin(math.radians(60 * i + 30)):.2f}" for i in range(6))
        pts2 = " ".join(f"{cx + r * .5 * math.cos(math.radians(60 * i + 30)):.2f},{cy + r * .5 * math.sin(math.radians(60 * i + 30)):.2f}" for i in range(6))
        sp = "".join(f'<line x1="{cx + r * .5 * math.cos(math.radians(60 * i + 30)):.2f}" y1="{cy + r * .5 * math.sin(math.radians(60 * i + 30)):.2f}" '
                     f'x2="{cx + r * math.cos(math.radians(60 * i + 30)):.2f}" y2="{cy + r * math.sin(math.radians(60 * i + 30)):.2f}" stroke="{OCRE}" stroke-width="1"/>' for i in range(6))
        return (f'<polygon points="{pts}" fill="{PAPEL}" stroke="{OCRE}" stroke-width="1.6" stroke-linejoin="round"/>'
                f'<polygon points="{pts2}" fill="#ebdab9" stroke="{OCRE}" stroke-width="1"/>{sp}')

    def espiroplasma(cx, cy):
        d = f"M{cx - 13},{cy} " + " ".join(f"q3.25,{-6 if i % 2 == 0 else 6} 6.5,0" for i in range(4))
        return (f'<path d="{d}" fill="none" stroke="{GRIS}" stroke-width="3.2" stroke-linecap="round"/>'
                f'<path d="{d}" fill="none" stroke="{PAPEL}" stroke-width="1" stroke-linecap="round"/>')

    def vector(cx, cy):
        return (f'<g transform="translate({cx},{cy})">'
                f'<path d="M-19,3 C-17,-6 4,-10 15,-2 L19,0.5 L15,3.2 C5,8 -11,9 -19,3 Z" fill="{VERDE_OSC}"/>'
                f'<path d="M-15,1.5 C-8,-6 6,-7 13,-1.5" fill="none" stroke="{SALVIA}" stroke-width="1"/>'
                f'<path d="M-12,2.8 C-4,-4 7,-5 13,-0.6" fill="none" stroke="{SALVIA}" stroke-width=".8"/>'
                f'<circle cx="17" cy="-0.4" r="2.4" fill="{VERDE_OSC}"/>'
                f'<path d="M19,-2 q4,-4 8,-5 M19,-1 q5,-3 9,-2" fill="none" stroke="{VERDE_OSC}" stroke-width=".7"/>'
                f'<path d="M-6,6 l-4,7 M0,7 l0,8 M7,6 l4,7" stroke="{VERDE_OSC}" stroke-width="1" stroke-linecap="round"/></g>')

    def maiz(cx, cy):
        return (f'<g transform="translate({cx},{cy})">'
                f'<path d="M0,22 L0,-20" stroke="{VERDE}" stroke-width="1.8" stroke-linecap="round"/>'
                f'<path d="M0,10 C-12,9 -19,0 -24,-12 C-13,-6 -5,-2 0,3 Z" fill="{SALVIA}" stroke="{VERDE}" stroke-width=".8"/>'
                f'<path d="M0,16 C13,15 20,7 25,-4 C14,0 5,4 0,9 Z" fill="{SALVIA}" stroke="{VERDE}" stroke-width=".8"/>'
                f'<path d="M0,-2 C-9,-4 -13,-12 -16,-22 C-8,-17 -3,-12 0,-7 Z" fill="{SALVIA_CL}" stroke="{VERDE}" stroke-width=".8"/>'
                f'<ellipse cx="6.5" cy="-8" rx="3.3" ry="8" transform="rotate(14 6.5 -8)" fill="{OCRE}"/>'
                f'<path d="M6.5,-16 l1.5,-6 M5,-15.5 l-0.5,-6 M8,-15 l3,-5" stroke="{OCRE}" stroke-width=".8"/></g>')

    def flecha(x1, y1, x2, y2, c=INK):
        a = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - 3.4 * math.cos(a - .5), y2 - 3.4 * math.sin(a - .5))
        p2 = (x2 - 3.4 * math.cos(a + .5), y2 - 3.4 * math.sin(a + .5))
        return (f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{c}" stroke-width="1.1" fill="none"/>'
                f'<path d="M{p1[0]:.2f},{p1[1]:.2f} L{x2},{y2} L{p2[0]:.2f},{p2[1]:.2f}" fill="none" stroke="{c}" stroke-width="1.1" stroke-linejoin="round"/>')

    b.append(virus(18, 20))
    b.append(f'<circle cx="18" cy="20" r="15.5" fill="none" stroke="{VERDE}" stroke-width="1.1" stroke-dasharray="2.4 1.8"/>')
    b.append(espiroplasma(18, 66))
    b.append(f'<path d="M3,59 L33,73 M3,73 L33,59" stroke="{OXIDO}" stroke-width="1.5" stroke-linecap="round"/>')
    b.append(T(40, 18.5, "Virus", 19, 700))
    b.append(T(40, 25.5, "MRFV", 15, 500, mono=True, fill=GRIS))
    b.append(T(40, 63.5, "Bacterias", 19, 700))
    b.append(T(40, 70.4, "espiroplasma,", 15, 500, italic=True, fill=GRIS))
    b.append(T(40, 76.8, "fitoplasma", 15, 500, italic=True, fill=GRIS))
    b.append(flecha(86, 28, 105, 40))
    b.append(flecha(86, 62, 105, 50))
    b.append(vector(134, 45))
    b.append(f'<circle cx="134" cy="45" r="26" fill="none" stroke="{VERDE}" stroke-width="1.1" stroke-dasharray="2.4 1.8"/>')
    b.append(T(134, 82.2, "Chicharrita", 19, 700, "middle"))
    b.append(T(134, 89, "Dalbulus maidis", 15, 500, "middle", italic=True, fill=GRIS))
    b.append(flecha(164, 45, 202, 45))
    b.append(T(183, 40.4, "transmite", 15, 500, "middle", italic=True, fill=GRIS))
    b.append(maiz(228, 45))
    b.append(T(228, 82.2, "Maíz", 19, 700, "middle"))
    # leyenda
    b.append(f'<circle cx="152" cy="7" r="2.6" fill="none" stroke="{VERDE}" stroke-width="1.1" stroke-dasharray="1.4 1"/>')
    b.append(T(157.5, 9.2, "blanco posible", 16, 600, fill=VERDE))
    b.append(f'<path d="M149.5,12.4 l5,5 M154.5,12.4 l-5,5" stroke="{OXIDO}" stroke-width="1.3" stroke-linecap="round"/>')
    b.append(T(157.5, 17.6, "sin maquinaria de ARNi", 16, 600, fill=OXIDO))
    return fig(W, H, "".join(b))


# ---------------------------------------------------------------- figura 2 (rho, compacta)
def fig2():
    """Los dos intervalos de rho contra el 0 y el 0,35, sin eje numerado: las dos
    referencias con nombre alcanzan para leerlos y el panel 02 no tiene mas de 36 mm."""
    W, H = 253, 36
    a, c = -0.6, 0.8
    x0, x1 = 6, 247

    def X(v):
        return x0 + (v - a) / (c - a) * (x1 - x0)
    b = []
    b.append(f'<line x1="{X(0)}" y1="8" x2="{X(0)}" y2="27" stroke="{INK}" stroke-width=".9" stroke-dasharray="2 1.6"/>')
    b.append(T(X(0), 4.2, "0 · sin relación", 15, 500, "middle", fill=GRIS))
    b.append(f'<line x1="{X(0.35)}" y1="8" x2="{X(0.35)}" y2="27" stroke="{VERDE}" stroke-width=".9" stroke-dasharray="2 1.6"/>')
    b.append(T(X(0.35) + 2, 4.2, "0,35 · criterio bueno", 15, 600, "start", fill=VERDE))

    def fila(y, lo, mid, hi, color, rot):
        s = (f'<line x1="{X(lo)}" y1="{y}" x2="{X(hi)}" y2="{y}" stroke="{color}" stroke-width="1.8"/>'
             f'<line x1="{X(lo)}" y1="{y - 2.6}" x2="{X(lo)}" y2="{y + 2.6}" stroke="{color}" stroke-width="1.8"/>'
             f'<line x1="{X(hi)}" y1="{y - 2.6}" x2="{X(hi)}" y2="{y + 2.6}" stroke="{color}" stroke-width="1.8"/>'
             f'<rect x="{X(mid) - 2.6}" y="{y - 2.6}" width="5.2" height="5.2" fill="{color}"/>')
        return s + T(0, y + 2.2, rot, 18, 700, "start", fill=color, mono=True)
    b.append(fila(13, -0.247, 0.142, 0.492, VERDE_OSC, "ρ = +0,142"))
    b.append(fila(23, -0.161, 0.236, 0.568, GRIS, "ρ = +0,236"))
    b.append(T(0, 33, f"{sp('Tribolium castaneum')}, laboratorio · 31 siRNA (n = 29) y 28 ARNdc (n = 28)", 15, 500, fill=GRIS, italic=True))
    return fig(W, H, "".join(b))


# ---------------------------------------------------------------- figura 3 (el contador historico)
def fig3():
    """Arriba, por que el contador pierde una ventana: dos arranques eficientes separados por
    veinte posiciones dejan la curva de cobertura plana y el segundo no se registra. Abajo, los
    cuatro conteos. Numeros de research/ola5/N1_regla_de_conteo/resultados/conteo_por_curva.tsv."""
    W, H = 253, 97
    b = []

    # --- el mecanismo: las cajas y sus etiquetas primero, la curva despues, sin solaparse
    b.append(T(0, 4, "ventanas eficientes, de 21 nt", 14, 600, fill=GRIS))
    for xa, xb, col, et in ((14, 74, OCRE, "arranca en p"), (74, 134, OCRE, "arranca en p + 20"),
                            (170, 230, VERDE, "aislada")):
        b.append(f'<rect x="{xa}" y="8" width="{xb - xa}" height="5.5" fill="{PAPEL}" stroke="{col}" stroke-width="1.1"/>')
        b.append(T(xa + 2, 19, et, 13, 500, fill=GRIS))
    b.append(T(0, 25, "curva de cobertura", 14, 600, fill=GRIS))
    b.append(f'<path d="M0 41 H14 V32 H134 V41 H170 V32 H230 V41 H253" fill="none" stroke="{OCRE}" stroke-width="1.3"/>')
    b.append(f'<line x1="74" y1="31" x2="74" y2="42" stroke="{INK}" stroke-width=".8" stroke-dasharray="2 1.6"/>')
    for x, et, col in ((14, "+1 · se cuenta", VERDE_OSC), (74, "0 · no se cuenta", OXIDO),
                       (170, "+1 · se cuenta", VERDE_OSC)):
        b.append(T(x + 2, 47, et, 14, 700 if col == OXIDO else 500, fill=col))

    # --- los cuatro conteos
    cols = (("las nuestras", 96), ("su contador", 140), ("la planilla", 182), ("tapadas", 236))
    b.append(f'<line x1="0" y1="56" x2="253" y2="56" stroke="{VERDE_OSC}" stroke-width=".7"/>')
    for et, x in cols:
        b.append(T(x, 54, et, 13, 600, "end", fill=GRIS))
    filas = (("MP_MRFV", 138, 114, "17,4 %"), ("CP_MRFV", 40, 35, "12,5 %"),
             ("BicC_Dm", 218, 199, "8,7 %"), ("ATPaseD_Dm", 35, 33, "5,7 %"))
    y = 64
    for g, ef, ct, oc in filas:
        b.append(T(0, y, g, 19, 500, mono=True))
        b.append(T(96, y, str(ef), 19, 500, "end", fill=INK, mono=True))
        b.append(T(108, y, "→", 17, 500, "middle", fill=GRIS))
        b.append(T(140, y, str(ct), 19, 800, "end", fill=VERDE_OSC, mono=True))
        b.append(T(150, y, "=", 17, 500, "middle", fill=VERDE))
        b.append(T(182, y, str(ct), 19, 800, "end", fill=VERDE_OSC, mono=True))
        b.append(T(236, y, oc, 19, 700, "end", fill=OXIDO, mono=True))
        y += 8
    b.append(T(0, 95, "el ancho de cobertura es 20: con 19 o con 21 fallan tres de los cuatro", 15, 500, fill=GRIS, italic=True))
    return fig(W, H, "".join(b))


# ---------------------------------------------------------------- figura 4
def fig4():
    W, H = 253, 134
    xl, xr = 72, 162
    ys = [30, 64, 98, 132]
    izq = [("BicC_Dm", "212", 0, "i"), ("MP_MRFV", "133", 1, "v"), ("ATPaseD_Dm", "42", 2, "i"), ("CP_MRFV", "32", 3, "v")]
    der = {"MP_MRFV": ("10,70", 0), "ATPaseD_Dm": ("8,92", 1), "BicC_Dm": ("8,48", 2), "CP_MRFV": ("6,30", 3)}
    col = {"i": VERDE, "v": OCRE}
    claro = {"i": "#6b9485", "v": "#d4aa5a"}   # los mismos colores al 70 % sobre el papel, sin transparencia
    b = []
    b.append(T(xl + 4, 5, "por conteo", 18, 700, "end"))
    b.append(T(xl + 4, 12, "ventanas eficientes", 16, 500, "end", fill=GRIS, italic=True))
    b.append(T(xr - 4, 5, "por densidad", 18, 700, "start"))
    b.append(T(xr - 4, 12, "cada 100 ventanas", 16, 500, "start", fill=GRIS, italic=True))
    for g, n, r, k in izq:
        d, rr = der[g]
        yl, yr = ys[r], ys[rr]
        dest = g == "BicC_Dm"
        b.append(f'<line x1="{xl}" y1="{yl}" x2="{xr}" y2="{yr}" stroke="{col[k] if dest else claro[k]}" stroke-width="{3.4 if dest else 1.4}"/>')
        b.append(f'<circle cx="{xl}" cy="{yl}" r="{2.8 if dest else 2}" fill="{col[k]}"/>')
        b.append(f'<circle cx="{xr}" cy="{yr}" r="{2.8 if dest else 2}" fill="{col[k]}"/>')
        wt = 700 if dest else 500
        b.append(T(xl - 5, yl + 2.6, g, 18, wt, "end", fill=col[k], mono=True))
        b.append(T(xr + 5, yr + 2.6, d, 18, 700 if dest else 600, "start", fill=INK, mono=True))
        b.append(T(xr + 31, yr + 2.6, g, 18, wt, "start", fill=col[k], mono=True))
    for g, n, r, k in izq:
        b.append(T(0, ys[r] + 2.6, n, 18, 700, "start", fill=INK, mono=True))
    return fig(W, H, "".join(b))

# ---------------------------------------------------------------- figura 5 (mapa del gen)
def fig5():
    W, H = 525, 104
    x0 = 12
    esc = 0.196

    def X(n):
        return x0 + n * esc
    yg = 76
    b = []
    b.append(f'<rect x="{X(0)}" y="{yg - 1.6}" width="{2500 * esc}" height="3.2" fill="{SALVIA_CL}" stroke="{SALVIA}" stroke-width=".5"/>')
    for n in range(0, 2501, 500):
        b.append(f'<line x1="{X(n)}" y1="{yg + 10}" x2="{X(n)}" y2="{yg + 13}" stroke="{INK}" stroke-width=".7"/>')
        b.append(T(X(n), yg + 20, f"{n:,}".replace(",", "."), 15, 500, "middle", fill=GRIS, mono=True))
    b.append(T(X(2500) + 13, yg + 20, "nt", 15, 500, "start", fill=GRIS, mono=True))
    regs = [(264, 563, f"{OXIDO}", PAPEL, None), (922, 1221, VERDE, PAPEL, None), (2121, 2420, SALVIA_CL, INK, GRIS)]
    for a, c, fillc, txtc, st in regs:
        b.append(f'<rect x="{X(a)}" y="{yg - 9}" width="{(c - a + 1) * esc:.2f}" height="18" fill="{fillc}" stroke="{st or fillc}" stroke-width="1" '
                 f'{"stroke-dasharray=\"2.4 1.6\"" if st else ""}/>')
        b.append(T(X(a) + (c - a + 1) * esc / 2, yg + 2.4, f"{a}–{c}", 16, 700, "middle", fill=txtc, mono=True))

    def tarjeta(cx, grande, gcol, l1, l2, l3):
        s = T(cx, 15.5, grande, 46, 800, "middle", fill=gcol)
        s += T(cx, 25, l1, 17, 700, "middle", fill=INK)
        s += T(cx, 31.4, l2, 16, 500, "middle", fill=GRIS)
        s += T(cx, 37.8, l3, 16, 500, "middle", fill=GRIS)
        return s
    c1, c2, c3 = X(264) + 29.4, X(922) + 29.4, X(2121) + 29.4
    b.append(tarjeta(c1, "22", OXIDO, "coincidencias perfectas", f"de 21 nt con {sp('H. vitripennis')}", "33 alertas de bloque ≥ 19 nt"))
    b.append(tarjeta(c2, "0", VERDE, "coincidencias perfectas", "26 ventanas eficientes · 3 alertas", "de bloque ≥ 19 nt, firmadas"))
    b.append(tarjeta(c3, "0", GRIS, "coincidencias perfectas", "6 alertas de bloque ≥ 19 nt;", f"la elige la cascada si {sp('H. v.')} ≠ 0"))
    # unión de las dos regiones del mismo gen
    b.append(f'<line x1="{c1}" y1="{yg - 11}" x2="{c1}" y2="46"  stroke="{OXIDO}" stroke-width=".8" stroke-dasharray="1.6 1.4"/>')
    b.append(f'<line x1="{c2}" y1="{yg - 11}" x2="{c2}" y2="46"  stroke="{VERDE}" stroke-width=".8" stroke-dasharray="1.6 1.4"/>')
    b.append(f'<line x1="{c3}" y1="{yg - 11}" x2="{c3}" y2="46"  stroke="{GRIS}" stroke-width=".8" stroke-dasharray="1.6 1.4"/>')
    xa, xb = X(564) + 4, X(922) - 4
    b.append(f'<path d="M{xa},{yg - 12} C{xa + 30},{yg - 30} {xb - 30},{yg - 30} {xb},{yg - 12}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    b.append(f'<path d="M{xb - 3.6},{yg - 17.4} L{xb},{yg - 12} L{xb + 1.2},{yg - 18}" fill="none" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>')
    b.append(T((xa + xb) / 2, yg - 31.6, "mismo gen, otra región", 15, 600, "middle", italic=True))
    b.append(T(X(0), yg + 28, "BicC_Dm · 2.500 nt · bloques de 300 nt · alerta: tramo de 19 nt o más idéntico a un gen de otro organismo", 15, 500, "start", fill=GRIS, italic=True))
    return fig(W, H, "".join(b))


# ---------------------------------------------------------------- figura 6 (firmeza)
def fig6():
    W, H = 166, 64
    x0, x1 = 3, 163

    def X(p):
        return x0 + p / 100 * (x1 - x0)
    b = []
    b.append(f'<line x1="{X(50)}" y1="2" x2="{X(50)}" y2="50" stroke="{GRIS}" stroke-width=".7" stroke-dasharray="2 1.6"/>')
    b.append(T(X(50), 57, "50 %", 15, 500, "middle", fill=GRIS, mono=True))
    filas = [("99,1 %", 99.1, VERDE, "contra 264–563 (la planilla)"),
             ("75,6 %", 75.6, SALVIA, "contra 2121–2420, molécula"),
             ("36,4 %", 36.4, OCRE, "contra 2121–2420, contexto")]
    y = 2
    for lab, v, c, txt in filas:
        b.append(T(x0, y + 4.4, txt, 15, 500, "start", halo="#ecf1e8"))
        b.append(f'<rect x="{x0}" y="{y + 6.2}" width="{X(v) - x0:.1f}" height="5.4" fill="{c}"/>')
        b.append(T(X(v) - 2, y + 10.8, lab, 15, 800, "end", fill=PAPEL if c != SALVIA else VERDE_OSC, mono=True))
        y += 16
    b.append(T(x0, 63, "% de 4.368 configuraciones en que gana 922–1221", 13, 500, "start", fill=GRIS, italic=True))
    return fig(W, H, "".join(b))


# ---------------------------------------------------------------- figura 7 (tension V-ATPasa)
def fig7():
    W, H = 166, 64
    b = []
    b.append(T(0, 4.4, "supervivencia a 4 días, por dieta", 15, 600))
    esc = 1.6
    for i, (lab, v, c) in enumerate([("ARNdc de V-ATPasa D", 18, VERDE), ("control GFP", 37, GRIS)]):
        y = 8 + i * 8.4
        b.append(f'<rect x="0" y="{y}" width="{v * esc:.1f}" height="5.4" fill="{c}"/>')
        b.append(T(v * esc + 2.5, y + 4.8, f"~{v} %", 16, 800, fill=c, mono=True))
        b.append(T(v * esc + 25, y + 4.6, lab, 14, 500, fill=GRIS, italic=True))
    b.append(T(0, 36, "bloques perfectos ≥ 19 nt contra humano", 15, 600))
    esc2 = 9.6
    for i, (lab, v, c) in enumerate([("observados en 72–371", 7, OXIDO), ("esperados por azar", 2.4, GRIS)]):
        y = 40 + i * 8.4
        b.append(f'<rect x="0" y="{y}" width="{v * esc2:.1f}" height="5.4" fill="{c}"/>')
        b.append(T(v * esc2 + 2.5, y + 4.8, f"{str(v).replace('.', ',')}", 16, 800, fill=c, mono=True))
        b.append(T(v * esc2 + 19, y + 4.6, lab, 14, 500, fill=GRIS, italic=True))
    return fig(W, H, "".join(b))


# ---------------------------------------------------------------- figura 9 (quimera)
def fig9():
    W, H = 322, 103
    b = []
    esc = 0.49
    xa, xj = 12, 12 + 300 * esc
    yc = 17
    b.append(f'<rect x="{xj - 66 * esc:.1f}" y="{yc - 8}" width="{132 * esc:.1f}" height="22" fill="{SALVIA_CL}"/>')
    b.append(f'<rect x="{xa}" y="{yc - 4}" width="{300 * esc:.1f}" height="14" fill="{VERDE}"/>')
    b.append(f'<rect x="{xj}" y="{yc - 4}" width="{300 * esc:.1f}" height="14" fill="{AZUL}"/>')
    b.append(f'<line x1="{xj}" y1="{yc - 9}" x2="{xj}" y2="{yc + 15}" stroke="{INK}" stroke-width="1.1"/>')
    b.append(T(xa + 3, yc + 5.8, "fragmento A · 300 nt", 16, 700, fill=PAPEL, mono=True))
    b.append(T(xj + 3, yc + 5.8, "fragmento B", 16, 700, fill=PAPEL, mono=True))
    b.append(T(xj, yc - 11.4, "unión", 15, 700, "middle"))
    b.append(T(xj, yc + 20.5, "sombreado: hasta 66 nt de la unión cambió un veredicto", 14, 500, "middle", fill=GRIS, italic=True))

    y1 = 45
    b.append(T(0, y1, "ventanas de juntura, en doce combinaciones de cuatro regiones", 17, 700))
    esc2 = 0.85
    filas = [("240", 240, GRIS, "ventanas que cruzan una unión"), ("4", 4, OCRE, "eficientes"), ("0", 0, OXIDO, "eficientes y con blanco continuo")]
    yy = y1 + 5.5
    for n, v, c, txt in filas:
        wv = v * esc2
        if v == 240:
            b.append(f'<rect x="0" y="{yy}" width="{wv:.1f}" height="6.4" fill="{c}"/>')
            b.append(T(3, yy + 4.8, txt, 14, 600, "start", fill=PAPEL))
            b.append(T(wv + 3, yy + 5, n, 17, 800, fill=c, mono=True))
        elif v:
            b.append(f'<rect x="0" y="{yy}" width="{max(wv, 1.4):.1f}" height="6.4" fill="{c}"/>')
            b.append(T(wv + 3, yy + 5, n, 17, 800, fill=c, mono=True))
            b.append(T(wv + 11, yy + 5, txt, 14, 500, fill=GRIS, italic=True))
        else:
            b.append(f'<line x1="0.6" y1="{yy}" x2="0.6" y2="{yy + 6.4}" stroke="{c}" stroke-width="1.6"/>')
            b.append(T(4, yy + 5, n, 17, 800, fill=c, mono=True))
            b.append(T(12, yy + 5, txt, 14, 500, fill=GRIS, italic=True))
        yy += 9
    y2 = yy + 5
    b.append(T(0, y2, "ventanas heredadas que cambiaron de veredicto", 17, 700))
    cx, esc3 = 140, 3.4
    b.append(f'<rect x="{cx - 31 * esc3:.1f}" y="{y2 + 4.5}" width="{31 * esc3:.1f}" height="6.4" fill="{OXIDO}"/>')
    b.append(f'<rect x="{cx}" y="{y2 + 4.5}" width="{30 * esc3:.1f}" height="6.4" fill="{VERDE}"/>')
    b.append(f'<line x1="{cx}" y1="{y2 + 2}" x2="{cx}" y2="{y2 + 13.4}" stroke="{INK}" stroke-width=".9"/>')
    b.append(T(cx - 31 * esc3 + 3, y2 + 9.6, "31", 16, 800, fill=PAPEL, mono=True))
    b.append(T(cx + 30 * esc3 - 3, y2 + 9.6, "30", 16, 800, "end", fill=PAPEL, mono=True))
    b.append(T(cx - 2, y2 + 18.5, "pierden eficiencia", 14, 500, "end", fill=OXIDO, italic=True))
    b.append(T(cx + 2, y2 + 18.5, "la ganan", 14, 500, "start", fill=VERDE, italic=True))
    b.append(T(320, y2 + 10, "= 61", 20, 800, "end", mono=True))
    return fig(W, H, "".join(b))


# ---------------------------------------------------------------- figura 11 (benchmark de las tres herramientas)
def fig11():
    """Adaptada de la version B a una columna de 253 mm: los dos contrastes apilados en vez de
    lado a lado, y un gen por herramienta en lugar de dos en el bloque de dsRNA-Engineer.
    Cifras de research/ola2/W7_ranking/benchmark_tres_herramientas.md."""
    W, H = 253, 113
    b = []

    # ---- dsRNA-Engineer contra el tamizaje exacto, off-target en maiz
    b.append(T(0, 4.6, "dsRNA-Engineer informa · el tamizaje exacto encuentra", 15, 600, fill=GRIS))
    x0, esc = 58, 0.474
    b.append(T(0, 17.4, "MP_MRFV", 19, 700, mono=True))
    y = 11
    for v, tag, col in ((215, "informa", OCRE), (97, "k = 16 nt", GRIS), (3, "k ≥ 19 nt", VERDE)):
        w = v * esc
        b.append(f'<rect x="{x0}" y="{y}" width="{max(w, 1.4):.1f}" height="6.6" fill="{col}"/>')
        b.append(T(x0 + w + 4, y + 6.2, str(v), 19, 700, fill=col, mono=True))
        b.append(T(x0 + w + 4 + (15 if v >= 100 else 11 if v >= 10 else 7), y + 6.2, tag, 15, 500, fill=GRIS))
        y += 10
    b.append(T(0, 44, "en CP_MRFV pasa lo mismo: 87, 48 y 0", 15, 500, fill=GRIS, italic=True))

    # ---- BLAST a un desajuste contra el conteo exacto
    b.append(f'<line x1="0" y1="50" x2="253" y2="50" stroke="{LINEA}" stroke-width=".7"/>')
    b.append(T(0, 58, "BLAST a 1 desajuste · contra el conteo exacto", 15, 600, fill=GRIS))
    esc2 = 5.4
    for g, y0, blast, exacto, razon in (("BicC_Dm", 64, 5, 16, "3,2"), ("ATPaseD_Dm", 86, 9, 17, "1,9")):
        b.append(T(0, y0 + 6.2, g, 19, 700, mono=True))
        for k, (v, tag, col) in enumerate(((blast, "BLAST+", AZUL), (exacto, "exacto", VERDE))):
            yy = y0 + k * 10
            b.append(f'<rect x="{x0}" y="{yy}" width="{v * esc2:.1f}" height="6.6" fill="{col}"/>')
            b.append(T(x0 + v * esc2 + 4, yy + 6.2, str(v), 19, 700, fill=col, mono=True))
            b.append(T(x0 + v * esc2 + 4 + (11 if v >= 10 else 7), yy + 6.2, tag, 15, 500, fill=GRIS))
        b.append(T(196, y0 + 11.5, f"subestima × {razon}", 15, 700, fill=OXIDO))
    b.append(T(0, 110, "bloque perfecto: las dos coinciden en las 20 celdas", 15, 500, fill=GRIS, italic=True))
    return fig(W, H, "".join(b))


# ---------------------------------------------------------------- figura 10 (tiempo)
def fig10():
    W, H = 186, 62
    x0 = 3
    esc = 7.6

    def X(d):
        return x0 + d * esc
    b = []
    b.append(f'<rect x="{X(0)}" y="5" width="{20 * esc}" height="11" fill="{OCRE}"/>')
    b.append(T(X(0) + 3, 12.6, "latencia del patógeno · ~20 días", 17, 700, fill=PAPEL))
    b.append(f'<rect x="{X(0)}" y="20" width="{5 * esc}" height="11" fill="{AZUL}"/>')
    b.append(T(X(0) + 3, 27.6, "4–5 d", 17, 700, fill=PAPEL))
    b.append(rayado("r10", X(5), 20, 15 * esc, 11, GRIS, GRIS))
    b.append(T(X(5) + 3, 27.6, "sin datos", 17, 600, halo=True))
    b.append(T(X(0), 40, "ensayos abiertos: medidos a los 4 o 5 días", 15, 500, fill=GRIS, italic=True))
    b.append(f'<line x1="{X(0)}" y1="46" x2="{X(20)}" y2="46" stroke="{INK}" stroke-width=".7"/>')
    for d in (0, 5, 10, 15, 20):
        b.append(f'<line x1="{X(d)}" y1="46" x2="{X(d)}" y2="48.4" stroke="{INK}" stroke-width=".7"/>')
        b.append(T(X(d), 55.6, str(d), 16, 500, "middle", fill=GRIS, mono=True))
    b.append(T(X(20) + 4, 55.6, "días", 16, 500, "start", fill=GRIS, italic=True))
    return fig(W, H, "".join(b))


def chip(letra):
    cls = {"E": "mE", "R": "mR", "M": "mM", "H": "mH", "?": "mQ"}[letra]
    return ""


M, R, H, Q, E = chip("M"), chip("R"), chip("H"), chip("?"), chip("E")

CSS = f"""
@font-face{{font-family:Montserrat;font-weight:400;src:url(assets/fonts/montserrat-latin-400-normal.woff2)}}
@font-face{{font-family:Montserrat;font-weight:500;src:url(assets/fonts/montserrat-latin-500-normal.woff2)}}
@font-face{{font-family:Montserrat;font-weight:600;src:url(assets/fonts/montserrat-latin-600-normal.woff2)}}
@font-face{{font-family:Montserrat;font-weight:700;src:url(assets/fonts/montserrat-latin-700-normal.woff2)}}
@font-face{{font-family:Montserrat;font-weight:800;src:url(assets/fonts/montserrat-latin-800-normal.woff2)}}
@font-face{{font-family:Montserrat;font-weight:400;font-style:italic;src:url(assets/fonts/montserrat-latin-400-italic.woff2)}}
@font-face{{font-family:Montserrat;font-weight:600;font-style:italic;src:url(assets/fonts/montserrat-latin-600-italic.woff2)}}
@font-face{{font-family:Montserrat;font-weight:700;font-style:italic;src:url(assets/fonts/montserrat-latin-700-italic.woff2)}}
@font-face{{font-family:'IBM Plex Mono';font-weight:400;src:url(assets/fonts/ibm-plex-mono-latin-400-normal.woff2)}}
@font-face{{font-family:'IBM Plex Mono';font-weight:500;src:url(assets/fonts/ibm-plex-mono-latin-500-normal.woff2)}}
@font-face{{font-family:'IBM Plex Mono';font-weight:600;src:url(assets/fonts/ibm-plex-mono-latin-600-normal.woff2)}}
@page{{size:841mm 1189mm;margin:0}}
:root{{--ink:{INK};--vd:{VERDE_OSC};--v:{VERDE};--salvia:{SALVIA};--papel:{PAPEL};--oxido:{OXIDO};--ocre:{OCRE};--azul:{AZUL};--vio:{VIOLETA};--gris:{GRIS};--linea:{LINEA}}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
body{{width:841mm;height:1189mm;overflow:hidden;background:var(--papel);color:var(--ink);
  font-family:Montserrat,'Helvetica Neue',Arial,sans-serif;font-size:26.5pt;line-height:1.36;position:relative;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}}
em{{font-style:italic}}
.top{{height:168mm;position:relative;color:#fff;background:#0b1d1c url(assets/header.jpg) center/100% 100% no-repeat}}
.top .logo{{position:absolute;left:24mm;top:31mm;height:107mm}}
.top .helix{{position:absolute;right:26mm;top:38mm;width:58mm}}
.top .tt{{position:absolute;left:112mm;right:112mm;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;text-align:center}}
.top h1{{margin:0;font-weight:800;font-size:92pt;line-height:1.02;letter-spacing:-.01em}}
.top .sub{{margin:5mm 0 0;font-weight:600;font-size:36pt;line-height:1.18}}
.top .aut{{margin:7mm 0 0;font-weight:500;font-size:27pt}}
.top .id{{margin:1.5mm 0 0;font-weight:400;font-size:22pt;color:#d6e2da}}
main{{height:939mm;padding:11mm 22mm 10mm;display:grid;grid-template-columns:repeat(12,1fr);grid-template-rows:auto auto auto auto;align-content:space-between;column-gap:18mm;row-gap:9mm}}
.hilo{{grid-column:1/13;display:grid;grid-template-columns:34mm 1fr;column-gap:8mm;align-items:baseline;border-bottom:.7mm solid var(--vd);padding-bottom:6mm}}
.hilo .k{{font-family:'IBM Plex Mono',Menlo,monospace;font-weight:600;font-size:19pt;letter-spacing:.12em;color:var(--v);text-transform:uppercase}}
.hilo p{{margin:0;font-weight:600;font-size:44pt;line-height:1.2;color:var(--vd);letter-spacing:-.005em}}
.hilo p b{{font-weight:800;text-decoration:underline;text-decoration-color:#e6cf97;text-decoration-thickness:3.4mm;text-underline-offset:-1.6mm;text-decoration-skip-ink:none}}
.pan{{grid-column:span 4;border-top:1.5mm solid var(--vd);padding-top:4.4mm;min-width:0;display:flex;flex-direction:column}}
.pan.s5{{grid-column:span 5}}
.pan.s3{{grid-column:span 3}}
.pan.s2{{grid-column:span 8;background:#ecf1e8;padding:3.4mm 7mm 4mm;border-top-width:2.6mm}}
.pan .n{{font-family:'IBM Plex Mono',Menlo,monospace;font-weight:600;font-size:19pt;letter-spacing:.1em;color:var(--v);margin:0}}
.pan h2{{margin:1.5mm 0 5mm;font-weight:800;font-size:36pt;line-height:1.1;color:var(--vd);letter-spacing:-.008em}}
.pan p{{margin:0 0 4.4mm}}
.pan p.tight{{margin-bottom:3.2mm}}
.fig{{display:block;max-width:100%;height:auto;margin:0 0 4.6mm}}
.chica{{font-size:22pt}}
.chica h2{{font-size:30pt}}
.chica ul.l li{{margin-bottom:2.6mm}}
.src{{font-size:15.5pt;line-height:1.3;color:var(--gris);margin:2mm 0 0;font-style:italic}}
.src code{{font-family:'IBM Plex Mono',Menlo,monospace;font-style:normal;font-size:.9em}}
.kw{{font-family:'IBM Plex Mono',Menlo,monospace;font-weight:500;font-size:.88em}}
.dos{{display:grid;grid-template-columns:1fr 1fr;margin:0 0 3mm;border:.5mm solid var(--vd)}}
.dos div{{padding:3.2mm 5mm 3.6mm}}
.dos div+div{{border-left:.5mm dashed var(--gris)}}
.dos b{{display:block;font-size:17pt;letter-spacing:.09em;text-transform:uppercase;font-family:'IBM Plex Mono',Menlo,monospace;font-weight:600;margin-bottom:.8mm}}
.dos span{{display:block;font-family:'IBM Plex Mono',Menlo,monospace;font-size:21pt;line-height:1.4}}
.dos .i b{{color:var(--v)}}.dos .v b{{color:var(--ocre)}}
.nocomp{{margin:0 0 5mm!important;text-align:center;font-size:18pt;font-weight:700;color:var(--oxido);letter-spacing:.05em;text-transform:uppercase}}
.sub3{{display:grid;grid-template-columns:1fr 1fr 1fr;column-gap:12mm;margin-top:2mm}}
.sub3 h3{{margin:0 0 3.4mm;font-size:20pt;font-weight:800;color:var(--vd);text-transform:uppercase;letter-spacing:.06em;border-bottom:.5mm solid var(--linea);padding-bottom:1.6mm}}
.sub3 p{{font-size:22.5pt;line-height:1.38;margin:0 0 3.6mm}}
.call{{border-left:2.2mm solid var(--ocre);background:#f0e7d1;padding:3.4mm 5mm 3.6mm;margin:0 0 4mm}}
.call p{{margin:0!important;font-weight:600}}
table.t{{width:100%;border-collapse:collapse;font-size:22pt;line-height:1.3;margin:0 0 5mm}}
table.t th{{font-weight:600;font-size:15pt;letter-spacing:.07em;text-transform:uppercase;text-align:left;color:var(--gris);padding:0 2mm 1.4mm 0;border-bottom:.6mm solid var(--vd);font-family:'IBM Plex Mono',Menlo,monospace}}
table.t td{{padding:1.8mm 2mm 1.8mm 0;border-bottom:.3mm solid var(--linea);vertical-align:top}}
table.t td.g{{font-weight:700;font-family:'IBM Plex Mono',Menlo,monospace;font-size:.92em}}
table.t .a{{color:var(--oxido);font-family:'IBM Plex Mono',Menlo,monospace;font-weight:600}}
table.t .b{{color:var(--v);font-family:'IBM Plex Mono',Menlo,monospace;font-weight:600}}
ul.l{{margin:0 0 3mm;padding:0;list-style:none}}
ul.l li{{padding-left:6.8mm;position:relative;margin:0 0 3mm}}
ul.l li:before{{content:"";position:absolute;left:0;top:3.4mm;width:2.8mm;height:2.8mm;background:var(--oxido)}}
.rule{{font-weight:800;font-size:27pt;line-height:1.2;color:var(--vd);border-top:.5mm solid var(--vd);border-bottom:.5mm solid var(--vd);padding:3mm 0;margin:0 0 4mm}}
.pie{{position:absolute;left:0;right:0;bottom:0;height:82mm;color:#fff;background:#0b1d1c url(assets/footer.jpg) center/100% 100% no-repeat}}
.pie .in{{position:absolute;left:0;right:0;top:0;height:68mm;padding:7mm 22mm 0;display:grid;display:flex;justify-content:space-between;align-items:flex-start}}
.pie .cont p{{margin:0;font-size:20pt;font-weight:500;line-height:1.5}}
.pie .cont .mail{{font-family:'IBM Plex Mono',Menlo,monospace;font-size:.94em;color:#d6e2da}}
.pie h4{{margin:0 0 2.6mm;font-family:'IBM Plex Mono',Menlo,monospace;font-weight:600;font-size:16pt;letter-spacing:.12em;text-transform:uppercase;color:#a9c7b2}}
.qr{{display:grid;grid-template-columns:50mm auto;column-gap:7mm;align-items:start}}
.qr h4{{grid-column:1/3}}
.qr .tile{{background:var(--papel);padding:3mm;width:50mm;height:50mm}}
.qr .tile img{{width:100%;height:100%;display:block}}
.qr p{{margin:0;font-size:15pt;line-height:1.28}}
.qr .mono{{font-family:'IBM Plex Mono',Menlo,monospace;font-size:13.5pt;word-break:break-all;margin-bottom:2mm}}
.refs{{position:absolute;left:22mm;right:22mm;bottom:4.5mm;font-size:14pt;line-height:1.28;color:#c3d1c9;border-top:.3mm solid #4d6860;padding-top:2mm}}
"""


def construir():
    f1, f2, f3, f4, f5, f6, f7, f9, f10, f11 = fig1(), fig2(), fig3(), fig4(), fig5(), fig6(), fig7(), fig9(), fig10(), fig11()
    html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>Decidir mejor sin laboratorio — póster Investigathon Y-Hat (track biotecnología)</title>
<style>{CSS}</style></head><body>

<header class="top">
  <div class="tt">
    <h1>Decidir mejor sin laboratorio</h1>
    <p class="sub">Auditoría computacional de diseños de ARN de doble cadena<br>contra la chicharrita del maíz, <em>Dalbulus maidis</em></p>
    <p class="aut">Lorenzo Door · Luca Fassio · Santino Cardelli · Joaquín Castaños</p>
    <p class="id">Ingeniería en Inteligencia Artificial, Universidad de San Andrés · ID: B01</p>
  </div>
</header>

<main>

<div class="hilo"><span class="k">El hilo</span>
<p>Sin laboratorio no podemos probar que un ARN silencia. Podemos <b>decidir mejor</b>, mostrando&nbsp;cada decisión.</p></div>

<section class="pan">
  <p class="n">01 · LA PREGUNTA</p>
  <h2>Un vector y dos blancos posibles</h2>
  {f1}
  <p>Un ARN de doble cadena (ARNdc) genera fragmentos de 21 nt (siRNA) que guían a la célula a destruir el mensajero de un gen con esa secuencia. Puede apuntar al <strong>insecto</strong>, que transmite el complejo de achaparramiento, o al <strong>virus</strong>; las bacterias no tienen maquinaria de ARNi.</p>
</section>

<section class="pan">
  <p class="n">02 · EL MOTOR PROPIO</p>
  <h2>Reimplementamos el criterio del laboratorio y reproduce al original</h2>
  <p>si-Fi21, en que se basa el pipeline de EPILAB, recorre un gen con una ventana de 21 nt y la aprueba si su hebra guía se carga bien y el sitio del mensajero no está plegado. Nuestro port en Python reproduce sus cuatro conteos clavados: <strong>133, 32, 212 y 42</strong>.</p>
  {f2}
  <p><strong>«Eficiente» no es «silencia».</strong> ρ mide si las ventanas aprobadas son las que más silencian; con los únicos datos abiertos no se puede decidir. Decidimos sobre el riesgo, que es secuencia exacta, no una predicción.</p>
</section>

<section class="pan">
  <p class="n">03 · EL CONTEO</p>
  <h2>La planilla tapa ventanas, y no las mismas en cada gen</h2>
  {f3}
  <p>Aplicado a nuestras ventanas eficientes, su contador devuelve las cuatro cifras de la planilla, exactas: no cuenta ventanas, cuenta las subidas de una curva de cobertura de 20 posiciones. Por eso ninguna cifra de la planilla es comparable con otra.</p>
</section>

<section class="pan">
  <p class="n">04 · DOS LISTAS</p>
  <h2>Dos listas, no un ranking único</h2>
  <div class="dos"><div class="i"><b>Insecto</b><span>BicC_Dm</span><span>eth_Dm</span><span>bursA_Dm</span><span>ATPaseD_Dm</span></div>
  <div class="v"><b>Virus</b><span>MP_MRFV</span><span>CP_MRFV</span></div></div>
  <p class="nocomp">no se comparan entre sí</p>
  <p class="tight">Contar ventanas eficientes mide el diseño <em>dentro</em> de un gen, no el valor del blanco. <em>BicC_Dm</em> (2.500 nt) es primero por conteo, con 212 ventanas, pero <strong>tercero por densidad</strong>: 8,48 cada 100, detrás de <em>MP_MRFV</em> (10,70; 1.243 nt). Un gen largo junta más ventanas sin ser mejor blanco.</p>
  <p class="tight">Con 2.000 juegos de pesos, <em>MP_MRFV</em> va antes que <em>CP_MRFV</em> en ≥ <strong>78,5 %</strong> y <em>BicC_Dm</em> es primero en el insecto en 76 a 100 %; el par <em>eth_Dm</em>–<em>bursA_Dm</em> no es firme.</p>
  {f4}
</section>

<section class="pan s2">
  <p class="n">05 · LA RECOMENDACIÓN</p>
  <h2><em>BicC_Dm</em> 922–1221: no cambiar de gen, mover la región dentro del gen</h2>
  <p>Las regiones que eligió EPILAB para el insecto contienen ventanas de 21 nt idénticas a las de <em>Homalodisca vitripennis</em>, un cicadélido no objetivo: <strong>22</strong> en <em>BicC_Dm</em> 264–563 y <strong>3</strong> en <em>ATPaseD_Dm</em> 151–450. Las que proponemos (ARNdc de 300 nt) tienen <strong>cero</strong>, mientras esa exposición no sea cero. Además se conserva: 36 de 36 ventanas idénticas en el transcriptoma argentino y en el genoma del Reino Unido.</p>
  {f5}
  <div class="sub3">
    <div><h3>Cuánta firmeza tiene</h3>{f6}
      <p class="tight">Firme: «<strong>no</strong> 264–563». Débil: «922 antes que 2121», que depende de cómo se cuente.</p></div>
    <div><h3>Qué hace y qué no</h3>
      <div class="call"><p>Reduce la población <u>entre generaciones</u>; no corta la transmisión de la temporada en curso.</p></div>
      <p>El fenotipo publicado del gen es de oviposición y ovario. Un adulto que ya adquirió el patógeno lo sigue transmitiendo.</p></div>
    <div><h3>La tensión de la V-ATPasa</h3>{f7}
      <p class="tight">La V-ATPasa D es el único candidato con efecto medido por dieta, pero su región tiene más tramos idénticos a humano que el azar: <strong>mejor evidencia y peor riesgo en el mismo gen</strong>.</p></div>
  </div>
  <p class="tight"><strong>La exposición de <em>H. vitripennis</em> es nuestra y está abierta.</strong> Es el peso que le damos a no afectarla, y no inventamos un número: con exposición exactamente 0 se mudan 3 de las 6 regiones elegidas, y de 0,05 a 1,00 no se muda ninguna. 922–1221 no cambia en todo el rango.</p>
</section>


<section class="pan">
  <p class="n">06 · EL BENCHMARK</p>
  <h2>Las tres herramientas no miden lo mismo</h2>
  {f11}
  <p class="tight">si-Fi21 es la única que estima eficiencia. <strong>dsRNA-Engineer</strong> informa 215 off-targets en maíz donde el tamizaje exacto encuentra 3: todo su número sale de la condición de 16 nt. <strong>Eficiencia: si-Fi21. Off-target: tamizaje exacto local. BLAST: exploración.</strong></p>
  <p class="src">Los genes del insecto no se subieron al servicio: material no publicado, así que ese benchmark se hizo con dos herramientas.</p>
</section>

<section class="pan s5">
  <p class="n">07 · QUIMERAS</p>
  <h2>El riesgo se hereda; la eficacia, no</h2>
  <p class="tight">Una molécula puede combinar fenotipos que no se solapan; la juntura crea 20 ventanas nuevas.</p>
  {f9}
  <div class="rule">Revisar sólo la juntura no alcanza: hay que recalcular.</div>
  <p class="tight">Las 4 de juntura eficientes no tienen blanco continuo, pero <strong>61 heredadas cambian de veredicto</strong> porque el plegado cruza la unión.</p>
</section>

<section class="pan s3 chica">
  <p class="n">08 · LÍMITES</p>
  <h2>Lo que no sabemos</h2>
  {f10}
  <ul class="l">
    <li>Si transmite antes de que el ARN haga efecto, matarlo no corta la transmisión.</li>
    <li>No hay silenciamiento medido en este insecto.</li>
    <li>13 de 32 alertas de off-target sin firmar.</li>
  </ul>
  <p class="tight"><strong>La refutarían</strong> un bioensayo de más de 20 días y 32 siRNA por brazo. Los proponemos; no los corremos.</p>
</section>

</main>

<footer class="pie"><div class="in">
  <div class="cont">
    <h4>Contacto</h4>
    <p>Lorenzo Door · <span class="mail">lolodoor3@gmail.com</span><br>
    Luca Fassio · <span class="mail">lucavfassio@gmail.com</span><br>
    Santino Cardelli · <span class="mail">sancardelli@gmail.com</span><br>
    Joaquín Castaños · <span class="mail">castanosjoaquin@gmail.com</span></p>
  </div>
  <div class="qr">
    <h4>Repositorio</h4>
    <div class="tile"><img src="assets/qr_repo.svg" alt="QR del repositorio"></div>
    <div><p class="mono">github.com/<br>Castanosjoaquin/<br>chicharrita-research</p></div>
  </div>
  <div class="qr">
    <h4>Informe</h4>
    <div class="tile"><img src="assets/qr_informe.svg" alt="QR del informe"></div>
    <div><p class="mono">[enlace<br>pendiente]</p></div>
  </div>
</div>
<div class="refs">Lück <em>et al.</em> 2019, <em>Front. Plant Sci.</em> 10:1023 · Cedden <em>et al.</em> 2025, <em>BMC Biol.</em> 23:114 · Dalaisón-Fuentes <em>et al.</em> 2022, <em>Pest Manag. Sci.</em> 78(7):3108 · Jones, Bernal y Medina 2021, bioRxiv 2021.09.29.462424 · Jones y Medina 2020, <em>Plants</em> 9(6):747.</div>
</footer>

</body></html>"""
    cab, cuerpo = html.split("</style>", 1)   # sólo el cuerpo: en el CSS el espacio antes del punto es un selector
    cuerpo = re.sub(r" +([.,;:])", r"\1", cuerpo)   # sin etiquetas quedan espacios antes de la puntuación
    cuerpo = re.sub(r"(?<=[a-záéíóúñ)]) +(?=</p>|</li>)", "", cuerpo)
    html = cab + "</style>" + cuerpo
    (AQUI / "poster.html").write_text(html, encoding="utf-8")
    print("poster.html escrito,", len(html) // 1024, "KB")


if __name__ == "__main__":
    construir()
