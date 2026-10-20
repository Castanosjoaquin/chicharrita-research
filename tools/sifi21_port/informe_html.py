"""Genera un informe HTML autocontenido por gen, con el grafico que pidio el investigador.

El grafico que describio en el checkpoint es el perfil de eficiencia a lo largo del
gen: «un plot con subiditas y bajaditas», donde se ve en que tramo se concentran los
siRNA eficientes. Acá se dibuja en tres capas sobre un mismo eje de posicion:

  curva     cuantos siRNA eficientes tendria una region que EMPIEZA en esa posicion.
            Es literalmente la variable de decision: elegir region es elegir un punto
            de esta curva.
  bandas    la region que eligio EPILAB y la de maxima densidad, para compararlas.
  tiras     una marca por ventana: eficiente, con off-target perfecto, con un desajuste.

Decisiones de color, validadas con el validador del skill de dataviz contra las
superficies reales de estas paginas (#f4f5f6 y #1b1e22), todos los pares:
  - La eficiencia es una sola serie -> un hue. Azul: #2a78d6 claro / #3987e5 oscuro.
  - El riesgo es ORDINAL, no categorico (perfecto > un desajuste), asi que es un
    solo hue en dos pasos: rojo #d03b3b, y el mismo rojo atenuado para el desajuste.
    Dos hues distintos para los dos niveles no pasa el piso de vision normal: rojo
    contra naranja da dE 10,8 y amarillo contra naranja 13,6, ambos bajo 15.

Uso:
    python informe_html.py --dir work/sifi_check --salida research/ola2/W5_secuencias_epilab/genes
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sifi_core import SifiEngine, best_region

SIZE = 21
ONTARGET = "GCA_975739785.1_ihDalMaid1.1_genomic"

GENES = [
    {"id": "MP_MRFV", "nombre": "MP_MRFV", "funcion": "proteína de movimiento",
     "organismo": "Maize rayado fino virus", "region": (1, 200), "declarado": 114,
     "ontarget": None},
    {"id": "CP_MRFV", "nombre": "CP_MRFV", "funcion": "proteína de cápside",
     "organismo": "Maize rayado fino virus", "region": (201, 400), "declarado": 35,
     "ontarget": None},
    {"id": "BicC_Dm", "nombre": "BicC_Dm", "funcion": "Bicaudal C",
     "organismo": "Dalbulus maidis", "region": (264, 563), "declarado": 199,
     "ontarget": ONTARGET},
    {"id": "ATPaseD_Dm", "nombre": "ATPaseD_Dm", "funcion": "subunidad D de la V-ATPasa",
     "organismo": "Dalbulus maidis", "region": (151, 450), "declarado": 33,
     "ontarget": ONTARGET},
]

NOMBRE_BASE = {
    "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna": "maíz (el cultivo)",
    "GCF_021130785.1_UT_GWSS_2.1_rna": "Homalodisca vitripennis (chicharrita no objetivo)",
    "GCF_003254395.2_Amel_HAv3.1_rna": "Apis mellifera (polinizador)",
    "GCF_914767665.1_icHarAxyr1.1_rna": "Harmonia axyridis (enemigo natural)",
    "GCF_002217175.1_ASM221717v1_rna": "Folsomia candida (fauna del suelo)",
    ONTARGET: "Dalbulus maidis (genoma)",
}


def leer_fasta(p):
    return "".join(l.strip() for l in Path(p).read_text().splitlines()
                   if not l.startswith(">"))


def leer_off(ruta_tsv, consulta, criterio, ontarget):
    """{pos: {base: n}} para un criterio, excluyendo la base on-target."""
    out = {}
    if not Path(ruta_tsv).exists():
        return None
    with open(ruta_tsv, encoding="utf-8") as fh:
        r = csv.DictReader(fh, delimiter="\t")
        cols = [c for c in r.fieldnames or []
                if c.endswith("|" + criterio)
                and (ontarget is None or not c.startswith(ontarget))]
        for fila in r:
            if fila["consulta"] != consulta:
                continue
            d = {c.split("|")[0]: int(fila[c]) for c in cols if int(fila[c] or 0)}
            out[int(fila["pos"])] = d
    return out


# ---------------------------------------------------------------- SVG

W, H = 960, 366
ML, MR, MT = 58, 16, 34
PLOT_H = 168
RUG_Y = MT + PLOT_H + 26
LANE_H = 11
LANE_GAP = 7
PW = W - ML - MR


def eje_x_ticks(n, maxn=8):
    paso = max(1, n // maxn)
    mag = 10 ** (len(str(paso)) - 1)
    paso = max(mag, (paso // mag) * mag)
    return list(range(0, n + 1, paso)) or [0, n]


def svg(gen, dens, dom_max, efic_pos, off_pos, mm1_pos, region, mejor, n_vent, largo_reg):
    # UN SOLO eje horizontal, en coordenadas del gen (1..n_vent), para que la curva,
    # las bandas y las tiras queden alineadas. La curva se indexa por el CENTRO de la
    # region, no por su inicio: asi cubre el tramo del gen donde cabe una region
    # completa y el pico marca el centro de la mejor region, que es la misma region
    # que devuelve best_region (solo reindexada).
    def sx(p):
        return ML + (p - 1) * PW / max(1, n_vent - 1)

    dmax = max(max(dens), 1) if dens else 1

    def sy(v):
        return MT + PLOT_H - (v / dmax) * PLOT_H

    o = []
    o.append('<svg viewBox="0 0 %d %d" width="100%%" role="img" '
             'aria-label="Perfil de siRNA eficientes a lo largo de %s" '
             'class="plot" preserveAspectRatio="xMidYMid meet">'
             % (W, H, html.escape(gen["nombre"])))

    # bandas de region (detras de todo). Si las dos etiquetas caen cerca se
    # escalonan en vertical, porque en genes cortos las regiones casi coinciden.
    bandas = [(region, "band-epilab", "EPILAB"),
              ((mejor["inicio"], mejor["fin"]), "band-best", "más densa")]
    centros = [(sx(max(1, a)) + sx(min(n_vent, b))) / 2 for (a, b), _, _ in bandas]
    escalonar = abs(centros[0] - centros[1]) < 76
    for i, ((a, b), cls, etq) in enumerate(bandas):
        x1, x2 = sx(max(1, a)), sx(min(n_vent, b))
        o.append('<rect class="%s" x="%.1f" y="%d" width="%.1f" height="%d"/>'
                 % (cls, x1, MT, max(2.0, x2 - x1), PLOT_H))
        dy = (0 if not escalonar else (-12 if i == 0 else 0))
        cx = min(max(centros[i], ML + 30), W - MR - 30)
        o.append('<text class="band-lab %s-lab" x="%.1f" y="%d">%s</text>'
                 % (cls, cx, MT - 6 + dy, etq))

    # grilla y eje y
    for i in range(5):
        v = dmax * i / 4
        y = sy(v)
        o.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>'
                 % (ML, y, W - MR, y))
        o.append('<text class="tick" x="%d" y="%.1f" text-anchor="end">%d</text>'
                 % (ML - 8, y + 4, round(v)))

    # Area + linea de densidad. `dens` esta indexada por POSICION del gen: dens[x-1]
    # es cuantos siRNA eficientes caen en la region de largo `largo_reg` centrada en
    # x. Cerca de los extremos la region se recorta contra el borde del gen, asi que
    # el valor baja de verdad —hay menos ventanas alcanzables ahi— y ese tramo se
    # dibuja punteado para no darlo por comparable con el resto.
    media = (largo_reg - 1) // 2
    cmin, cmax = 1 + media, n_vent - largo_reg + 1 + media
    xs = [sx(x) for x in range(1, n_vent + 1)]
    pts = ["%.1f,%.1f" % (x, sy(v)) for x, v in zip(xs, dens)]
    if pts:
        o.append('<polygon class="area" points="%.1f,%.1f %s %.1f,%.1f"/>'
                 % (xs[0], MT + PLOT_H, " ".join(pts), xs[-1], MT + PLOT_H))
        i0, i1 = max(0, cmin - 1), min(len(pts), cmax)
        if i0 > 0:
            o.append('<polyline class="line line-borde" points="%s"/>'
                     % " ".join(pts[:i0 + 1]))
        o.append('<polyline class="line" points="%s"/>' % " ".join(pts[i0:i1]))
        if i1 < len(pts):
            o.append('<polyline class="line line-borde" points="%s"/>'
                     % " ".join(pts[i1 - 1:]))

    # tiras
    lanes = [("Ventana eficiente", efic_pos, "tick-efic"),
             ("Off-target: bloque perfecto ≥19 nt", off_pos, "tick-off"),
             ("Off-target: 21 nt con 1 desajuste", mm1_pos, "tick-mm1")]
    for li, (etq, posiciones, cls) in enumerate(lanes):
        y = RUG_Y + li * (LANE_H + LANE_GAP)
        o.append('<rect class="lane" x="%d" y="%.1f" width="%d" height="%d"/>'
                 % (ML, y, PW, LANE_H))
        if posiciones is None:
            o.append('<text class="tick" x="%d" y="%.1f">sin medir</text>'
                     % (ML + 6, y + LANE_H - 2))
            continue
        for p in posiciones:
            if p <= n_vent:
                o.append('<rect class="%s" x="%.1f" y="%.1f" width="1.6" height="%d"/>'
                         % (cls, ML + (p - 1) * PW / max(1, n_vent - 1), y, LANE_H))

    # eje x
    ybase = MT + PLOT_H
    o.append('<line class="axis" x1="%d" y1="%d" x2="%d" y2="%d"/>'
             % (ML, ybase, W - MR, ybase))
    for t in eje_x_ticks(n_vent):
        if t == 0:
            t = 1
        x = sx(min(t, n_vent))
        o.append('<text class="tick" x="%.1f" y="%d" text-anchor="middle">%d</text>'
                 % (x, H - 8, t))

    # capa de interaccion
    o.append('<line class="cross" x1="0" y1="%d" x2="0" y2="%d" style="display:none"/>'
             % (MT, RUG_Y + 3 * (LANE_H + LANE_GAP)))
    o.append('<rect class="hit" x="%d" y="%d" width="%d" height="%d"/>'
             % (ML, MT, PW, RUG_Y + 3 * (LANE_H + LANE_GAP) - MT))
    o.append("</svg>")
    return "\n".join(o)


def leyenda():
    return (
        '<ul class="legend">'
        '<li><span class="sw sw-efic"></span>siRNA eficiente</li>'
        '<li><span class="sw sw-off"></span>Off-target: bloque perfecto ≥19 nt</li>'
        '<li><span class="sw sw-mm1"></span>Off-target: 21 nt con 1 desajuste</li>'
        '</ul>')


# ---------------------------------------------------------------- HTML

CSS = """
:root{
  --bg:#ffffff; --surface:#f4f5f6; --surface-2:#eceef0;
  --text:#16191c; --text-dim:#565d64; --line:#d4d8dc;
  --accent:#1d5c4a; --accent-soft:#e3efea;
  --warn:#8a4b1c; --warn-soft:#f6ece3;
  --stop:#8a2b2b; --stop-soft:#f7e8e8;
  --efic:#2a78d6; --risk:#d03b3b;
  --grid:#e1e0d9; --axis:#c3c2b7; --muted:#898781;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#121417; --surface:#1b1e22; --surface-2:#23272c;
    --text:#e8eaec; --text-dim:#a0a7ae; --line:#343a40;
    --accent:#6fc4a7; --accent-soft:#1c2b26;
    --warn:#d79a68; --warn-soft:#2a221b;
    --stop:#dd8b8b; --stop-soft:#2b1d1d;
    --efic:#3987e5; --risk:#d03b3b;
    --grid:#2c2c2a; --axis:#383835; --muted:#898781;
  }
}
:root[data-theme="dark"]{
  --bg:#121417; --surface:#1b1e22; --surface-2:#23272c;
  --text:#e8eaec; --text-dim:#a0a7ae; --line:#343a40;
  --accent:#6fc4a7; --accent-soft:#1c2b26;
  --warn:#d79a68; --warn-soft:#2a221b;
  --stop:#dd8b8b; --stop-soft:#2b1d1d;
  --efic:#3987e5; --risk:#d03b3b;
  --grid:#2c2c2a; --axis:#383835; --muted:#898781;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0; background:var(--bg); color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  font-size:16px; line-height:1.6}
.wrap{max-width:960px; margin:0 auto; padding:0 16px}
header{border-bottom:1px solid var(--line); padding:44px 0 32px; margin-bottom:36px}
.eyebrow{font-size:.8rem; letter-spacing:.08em; text-transform:uppercase;
  color:var(--text-dim); margin:0 0 10px}
h1{font-size:1.95rem; line-height:1.22; font-weight:650; margin:0 0 12px; letter-spacing:-.015em}
h1 em{font-style:italic}
.sub{color:var(--text-dim); margin:0; max-width:62ch}
h2{font-size:1.3rem; font-weight:650; margin:44px 0 14px; letter-spacing:-.01em;
  padding-top:18px; border-top:1px solid var(--line)}
h3{font-size:1.02rem; font-weight:650; margin:26px 0 8px}
p{margin:0 0 14px; max-width:68ch}
.lead{font-size:1.06rem}
strong{font-weight:650}
a{color:var(--accent)}
.verdict{background:var(--surface); border:1px solid var(--line);
  border-left:4px solid var(--accent); padding:22px 24px; margin:0 0 28px}
.verdict h2{margin:0 0 12px; border-top:none; padding-top:0; font-size:1.15rem}
.verdict p:last-child{margin-bottom:0}
.kpis{display:flex; flex-wrap:wrap; gap:10px; margin:0 0 22px; padding:0; list-style:none}
.kpis li{flex:1 1 150px; background:var(--surface); border:1px solid var(--line); padding:12px 14px}
.kpis .n{display:block; font-size:1.6rem; font-weight:650; line-height:1.1; letter-spacing:-.02em}
.kpis .k{display:block; font-size:.78rem; color:var(--text-dim); margin-top:4px}
figure{margin:0 0 10px; background:var(--surface); border:1px solid var(--line); padding:14px}
figcaption{font-size:.85rem; color:var(--text-dim); margin-top:10px; max-width:none}
.plot{display:block; width:100%; height:auto; overflow:visible; touch-action:pan-y}
.legend{display:flex; flex-wrap:wrap; gap:14px; list-style:none; padding:0;
  margin:0 0 10px; font-size:.84rem; color:var(--text-dim)}
.legend li{display:flex; align-items:center; gap:6px}
.sw{width:11px; height:11px; border-radius:2px; display:inline-block; flex:none}
.sw-efic{background:var(--efic)}
.sw-off{background:var(--risk)}
.sw-mm1{background:var(--risk); opacity:.45}
.area{fill:var(--efic); opacity:.16}
.line{fill:none; stroke:var(--efic); stroke-width:2; stroke-linejoin:round}
.line-borde{stroke-dasharray:4 3; opacity:.6}
.grid{stroke:var(--grid); stroke-width:1}
.axis{stroke:var(--axis); stroke-width:1}
.tick{fill:var(--muted); font-size:11px; font-variant-numeric:tabular-nums}
.lane{fill:var(--surface-2)}
.tick-efic{fill:var(--efic)}
.tick-off{fill:var(--risk)}
.tick-mm1{fill:var(--risk); opacity:.45}
.band-epilab{fill:var(--muted); opacity:.14; stroke:var(--muted); stroke-width:1; stroke-opacity:.5}
.band-best{fill:var(--efic); opacity:.10; stroke:var(--efic); stroke-width:1; stroke-opacity:.6}
.band-lab{font-size:11px; font-weight:650; text-anchor:middle}
.band-epilab-lab{fill:var(--text-dim)}
.band-best-lab{fill:var(--efic)}
.cross{stroke:var(--text-dim); stroke-width:1; stroke-dasharray:3 3}
.hit{fill:transparent}
.tip{position:absolute; pointer-events:none; opacity:0; transition:opacity .08s;
  background:var(--bg); border:1px solid var(--line); padding:8px 10px;
  font-size:.82rem; line-height:1.45; box-shadow:0 2px 10px rgba(0,0,0,.14);
  max-width:260px; z-index:5}
.tip b{font-variant-numeric:tabular-nums}
.tipwrap{position:relative}
table{border-collapse:collapse; width:100%; font-size:.9rem; margin:0 0 16px}
th,td{text-align:left; padding:8px 10px; border-bottom:1px solid var(--line);
  vertical-align:top}
th{font-weight:650; font-size:.82rem; color:var(--text-dim)}
td.n,th.n{text-align:right; font-variant-numeric:tabular-nums}
.tag{display:inline-block; font-size:.72rem; padding:1px 7px; border-radius:9px;
  border:1px solid currentColor; margin-left:6px; vertical-align:1px}
.tag-e{color:var(--accent)} .tag-r{color:var(--warn)} .tag-h{color:var(--text-dim)}
.tag-q{color:var(--stop)}
footer{border-top:1px solid var(--line); margin-top:48px; padding:22px 0 56px;
  color:var(--text-dim); font-size:.86rem}
@media (max-width:640px){ h1{font-size:1.55rem} .kpis li{flex:1 1 100%} }
"""

JS = """
(function(){
  document.querySelectorAll('[data-plot]').forEach(function(fig){
    var d = JSON.parse(fig.querySelector('script[type="application/json"]').textContent);
    var svg = fig.querySelector('svg');
    var hit = svg.querySelector('.hit');
    var cross = svg.querySelector('.cross');
    var tip = fig.querySelector('.tip');
    if(!svg || !hit || !tip) return;
    var ML=d.ml, PW=d.pw, nVent=d.nVent, cmin=d.cmin, cmax=d.cmax;
    var efic=new Set(d.efic), off=new Set(d.off), mm1=d.mm1?new Set(d.mm1):null;

    function mover(ev){
      var r = svg.getBoundingClientRect();
      var cx = (ev.touches?ev.touches[0].clientX:ev.clientX) - r.left;
      var vx = cx * d.vbw / r.width;
      var f = (vx - ML) / PW;
      if(f<0) f=0; if(f>1) f=1;
      var pos = Math.round(1 + f*(nVent-1));
      var x = ML + (pos-1)*PW/Math.max(1,nVent-1);
      cross.setAttribute('x1',x); cross.setAttribute('x2',x);
      cross.style.display='';
      var partes = ['<b>posición '+pos+'</b>'];
      var i = pos-1;
      if(i>=0 && i<d.dens.length){
        var nota = (pos<cmin || pos>cmax)
          ? ' <span style="opacity:.75">(región recortada contra el borde del gen)</span>'
          : '';
        partes.push('región centrada acá: <b>'+d.dens[i]+'</b> eficientes'+nota);
      }
      var est=[];
      if(pos<=nVent){
        est.push(efic.has(pos)?'eficiente':'no eficiente');
        if(off.has(pos)) est.push('off-target perfecto');
        if(mm1 && mm1.has(pos)) est.push('off-target con 1 desajuste');
        if(!off.has(pos) && (!mm1||!mm1.has(pos))) est.push('sin off-target');
      }
      if(est.length) partes.push('esta ventana: '+est.join(' · '));
      tip.innerHTML = partes.join('<br>');
      tip.style.opacity=1;
      var tw = tip.offsetWidth, fw = fig.clientWidth;
      var left = cx - tw/2; if(left<4) left=4; if(left+tw>fw-4) left=fw-tw-4;
      tip.style.left = left+'px';
      tip.style.top  = '6px';
    }
    function salir(){ tip.style.opacity=0; cross.style.display='none'; }
    hit.addEventListener('mousemove', mover);
    hit.addEventListener('mouseleave', salir);
    svg.addEventListener('touchstart', mover, {passive:true});
    svg.addEventListener('touchmove', mover, {passive:true});
    svg.addEventListener('touchend', salir);
  });
})();
"""


def tabla_bases(off_full, mm1_full, efic_set, n_vent):
    """Tabla de off-targets por base, con cuantas ventanas y cuantas eficientes."""
    agg = {}
    for fuente, pos_dict in (("perf", off_full), ("mm1", mm1_full)):
        if pos_dict is None:
            continue
        for p, bases in pos_dict.items():
            for b in bases:
                a = agg.setdefault(b, {"perf": 0, "perf_ef": 0, "mm1": 0, "mm1_ef": 0})
                a[fuente] += 1
                if p in efic_set:
                    a[fuente + "_ef"] += 1
    if not agg:
        return ('<p>Ninguna ventana de este gen coincide con ninguna de las cinco '
                'referencias no objetivo, con ninguno de los dos criterios. '
                '<span class="tag tag-e">[E]</span></p>')
    filas = []
    for b, a in sorted(agg.items(), key=lambda kv: -(kv[1]["perf"] + kv[1]["mm1"])):
        filas.append(
            "<tr><td>%s</td><td class='n'>%d</td><td class='n'>%d</td>"
            "<td class='n'>%s</td><td class='n'>%s</td></tr>" % (
                html.escape(NOMBRE_BASE.get(b, b)), a["perf"], a["perf_ef"],
                a["mm1"] if mm1_full is not None else "—",
                a["mm1_ef"] if mm1_full is not None else "—"))
    return ("<table><thead><tr><th>Referencia no objetivo</th>"
            "<th class='n'>Ventanas con bloque perfecto ≥19 nt</th>"
            "<th class='n'>de esas, eficientes</th>"
            "<th class='n'>Ventanas con 1 desajuste</th>"
            "<th class='n'>de esas, eficientes</th></tr></thead><tbody>"
            + "".join(filas) + "</tbody></table>")


def pagina(gen, datos):
    g = gen
    d = datos
    reg = "%d-%d" % g["region"]
    mejor_reg = "%d-%d" % (d["mejor"]["inicio"], d["mejor"]["fin"])
    brecha = (d["mejor"]["eficientes"] - d["efic_region"])
    pct = (100.0 * brecha / d["mejor"]["eficientes"]) if d["mejor"]["eficientes"] else 0

    _L = g["region"][1] - g["region"][0] + 1
    _media = (_L - 1) // 2
    json_blob = json.dumps({
        "ml": ML, "pw": PW, "vbw": W, "nVent": d["n_vent"],
        "cmin": 1 + _media, "cmax": d["n_vent"] - _L + 1 + _media,
        "dens": d["dens"], "efic": sorted(d["efic_set"]),
        "off": sorted(d["off_pos"]),
        "mm1": sorted(d["mm1_pos"]) if d["mm1_pos"] is not None else None,
    }, separators=(",", ":"))

    cmp_off = ""
    if d["mm1_pos"] is not None:
        cmp_off = (
            "<p>Con el criterio de un desajuste sumado, la región de EPILAB pasa de "
            "<b>%d</b> a <b>%d</b> ventanas con algún off-target, y la región %s pasa "
            "de <b>%d</b> a <b>%d</b>. %s</p>" % (
                d["off_region"], d["riesgo_region_tot"], mejor_reg,
                d["off_mejor"], d["riesgo_mejor_tot"],
                "La comparación no se da vuelta."
                if d["riesgo_mejor_tot"] <= d["riesgo_region_tot"]
                else "<strong>La comparación cambia de signo: con el criterio más "
                     "amplio, la región elegida resulta la menos expuesta.</strong>"))

    return """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(nombre)s — perfil de eficiencia y off-targets</title>
<style>%(css)s</style>
</head>
<body>
<div class="wrap">
<header>
  <p class="eyebrow">Investigathon Y-Hat · track chicharrita / ARNi · gen %(idx)d de 4</p>
  <h1>%(nombre)s<span style="color:var(--text-dim); font-weight:400"> · %(funcion)s</span></h1>
  <p class="sub">%(organismo_it)s · %(largo)s nt · región elegida por EPILAB: %(reg)s ·
  conteo declarado en la planilla: %(declarado)d siRNA eficientes</p>
</header>

<div class="verdict">
  <h2>Qué dice este gen</h2>
  %(veredicto)s
</div>

<ul class="kpis">
  <li><span class="n">%(efic_total)d</span><span class="k">siRNA eficientes en el gen entero, de %(n_vent)d ventanas</span></li>
  <li><span class="n">%(efic_region)d</span><span class="k">en la región que eligió EPILAB (%(reg)s)</span></li>
  <li><span class="n">%(efic_mejor)d</span><span class="k">en la región más densa (%(mejor_reg)s)</span></li>
  <li><span class="n">%(declarado)d</span><span class="k">declarado en la planilla para el gen entero</span></li>
</ul>

<h2>El perfil a lo largo del gen</h2>
<p>La curva contesta una sola pregunta, en cada punto: <strong>si eligiera una región
de %(largo_reg)d nt centrada acá, cuántos siRNA eficientes tendría</strong>. Elegir
región es elegir un punto de esta curva, y por eso el máximo de la curva es la mejor
región posible por densidad. Leída en el centro de cualquiera de las dos bandas, la
curva da exactamente el número de esa región en la tabla de más abajo.</p>
<p>Cerca de los dos extremos del gen la región ya no entra completa y queda recortada
contra el borde: ahí hay menos ventanas alcanzables y el valor baja de verdad, no por
falta de dato. Esos dos tramos van <strong>punteados</strong>, porque no son
comparables con el resto. Abajo de la curva, una marca por ventana de 21 nt: si es
eficiente y si le pega a algo que no queremos tocar.</p>

<figure data-plot class="tipwrap">
  %(leyenda)s
  %(svg)s
  <div class="tip"></div>
  <script type="application/json">%(json)s</script>
  <figcaption>Eje horizontal: posición dentro del gen, 1 a %(n_vent)d (las ventanas de
  21 nt que entran en %(largo)s nt). La banda gris es la región que eligió EPILAB; la
  banda azul, la de máxima densidad. El tramo punteado de la curva, en los dos
  extremos, es donde la región de %(largo_reg)d nt ya no entra completa. Hay
  %(dom_max)d regiones completas posibles en este gen. Pasá el mouse por el gráfico
  para leer cualquier posición.</figcaption>
</figure>

<h2>La región elegida contra la más densa</h2>
%(tabla_reg)s
<p>%(parrafo_region)s</p>

<h2>Off-targets a 21 nt</h2>
<p>Cada ventana de 21 nt se buscó por coincidencia exacta contra seis referencias
públicas, en las dos hebras. El criterio principal es un <strong>bloque contiguo
perfecto de 19 nt o más</strong>, que es el umbral publicado que ya usa nuestra
rúbrica. El segundo criterio, más amplio, son los 21 nt con exactamente un
desajuste: un siRNA así todavía puede cortar, más débilmente.%(nota_on)s</p>
%(tabla_bases)s
%(cmp_off)s

<h2>Qué queda sin resolver</h2>
%(pendientes)s

<footer>
  <p>Generado por <code>tools/sifi21_port/informe_html.py</code> desde
  <code>Sequences_EPILAB.xlsx</code>. Motor de eficiencia: port propio de si-Fi21
  (Lück et al. 2019), modo %(modo)s. Tamizaje: coincidencia exacta con Aho-Corasick.
  Todo corrió local; ninguna secuencia salió de la máquina.</p>
  <p>Marcadores: <span class="tag tag-e">[E]</span> establecido ·
  <span class="tag tag-r">[R]</span> reportado ·
  <span class="tag tag-h">[H]</span> hipótesis nuestra ·
  <span class="tag tag-q">[?]</span> incierto.</p>
</footer>
</div>
<script>%(js)s</script>
</body>
</html>
""" % {
        "css": CSS, "js": JS, "json": json_blob,
        "nombre": html.escape(g["nombre"]), "funcion": html.escape(g["funcion"]),
        "organismo_it": "<em>%s</em>" % html.escape(g["organismo"]),
        "largo": d["largo"], "reg": reg, "declarado": g["declarado"],
        "idx": d["idx"], "n_vent": d["n_vent"], "dom_max": d["dom_max"],
        "largo_reg": g["region"][1] - g["region"][0] + 1,
        "efic_total": d["efic_total"], "efic_region": d["efic_region"],
        "efic_mejor": d["mejor"]["eficientes"], "mejor_reg": mejor_reg,
        "veredicto": d["veredicto"], "parrafo_region": d["parrafo_region"],
        "pendientes": d["pendientes"], "nota_on": d["nota_on"],
        "leyenda": leyenda(), "svg": d["svg"],
        "tabla_reg": d["tabla_reg"], "tabla_bases": d["tabla_bases"],
        "cmp_off": cmp_off, "modo": d["modo"],
        "brecha": brecha, "pct": pct,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="work/sifi_check")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--modo", choices=("fiel", "corregido"), default="corregido")
    ap.add_argument("--backend", choices=("exe", "vienna"), default="vienna")
    a = ap.parse_args(argv)

    d_in = Path(a.dir)
    out = Path(a.salida)
    out.mkdir(parents=True, exist_ok=True)
    resumen_global = []

    for idx, g in enumerate(GENES, 1):
        seq = leer_fasta(d_in / ("%s_full.fasta" % g["id"]))
        vent, res = SifiEngine(mode=a.modo).run(seq, backend=a.backend)
        n_vent = len(vent)
        efic_set = {w.pos for w in vent if w.is_efficient}

        off = leer_off(d_in / "offtarget_full" / "offtarget_por_sirna.tsv",
                       "%s_full" % g["id"], "perfecto_ge19", g["ontarget"]) or {}
        mm1_raw = leer_off(d_in / ("offtarget_mm1_%s" % g["id"]) / "offtarget_por_sirna.tsv",
                           "%s_full" % g["id"], "mm1_21", g["ontarget"])
        off_pos = {p for p, b in off.items() if b}
        mm1_pos = ({p for p, b in mm1_raw.items() if b} - off_pos
                   if mm1_raw is not None else None)

        L = g["region"][1] - g["region"][0] + 1
        dom_max = max(1, n_vent - L + 1)
        # Densidad local por posicion del gen: cuantos siRNA eficientes caen en la
        # region de largo L centrada en x, recortada contra los bordes del gen.
        # Con suma de prefijos para que sea lineal y no cuadratica.
        pre = [0] * (n_vent + 1)
        for i in range(1, n_vent + 1):
            pre[i] = pre[i - 1] + (1 if i in efic_set else 0)
        media = (L - 1) // 2
        dens = []
        for x in range(1, n_vent + 1):
            ini = max(1, x - media)
            fin = min(n_vent, x - media + L - 1)
            dens.append(pre[fin] - pre[ini - 1])
        mejor = best_region(vent, L)
        a0, b0 = g["region"]
        m0, m1 = mejor["inicio"], mejor["fin"]

        def en(r, s):
            return sum(1 for p in s if r[0] <= p <= r[1])

        efic_region = en((a0, b0), efic_set)
        off_region = en((a0, b0), off_pos)
        off_mejor = en((m0, m1), off_pos)
        riesgo_region_tot = off_region + (en((a0, b0), mm1_pos) if mm1_pos else 0)
        riesgo_mejor_tot = off_mejor + (en((m0, m1), mm1_pos) if mm1_pos else 0)

        tabla_reg = (
            "<table><thead><tr><th>Región</th><th class='n'>Largo</th>"
            "<th class='n'>siRNA eficientes</th>"
            "<th class='n'>Ventanas con off-target perfecto</th>"
            "<th class='n'>Con 1 desajuste</th></tr></thead><tbody>"
            "<tr><td>Elegida por EPILAB (%d-%d)</td><td class='n'>%d</td>"
            "<td class='n'>%d</td><td class='n'>%d</td><td class='n'>%s</td></tr>"
            "<tr><td>Más densa en eficientes (%d-%d)</td><td class='n'>%d</td>"
            "<td class='n'>%d</td><td class='n'>%d</td><td class='n'>%s</td></tr>"
            "<tr><td>Gen entero</td><td class='n'>%d</td><td class='n'>%d</td>"
            "<td class='n'>%d</td><td class='n'>%s</td></tr>"
            "</tbody></table>" % (
                a0, b0, L, efic_region, off_region,
                en((a0, b0), mm1_pos) if mm1_pos else "—",
                m0, m1, L, mejor["eficientes"], off_mejor,
                en((m0, m1), mm1_pos) if mm1_pos else "—",
                d_largo := len(seq), len(efic_set), len(off_pos),
                len(mm1_pos) if mm1_pos else "—"))

        datos = {
            "idx": idx, "largo": len(seq), "n_vent": n_vent, "dom_max": dom_max,
            "dens": dens, "efic_set": efic_set, "off_pos": off_pos, "mm1_pos": mm1_pos,
            "efic_total": len(efic_set), "efic_region": efic_region,
            "off_region": off_region, "off_mejor": off_mejor,
            "riesgo_region_tot": riesgo_region_tot,
            "riesgo_mejor_tot": riesgo_mejor_tot,
            "mejor": mejor, "modo": a.modo,
            "svg": svg(g, dens, dom_max, sorted(efic_set), sorted(off_pos),
                       sorted(mm1_pos) if mm1_pos is not None else None,
                       g["region"], mejor, n_vent, L),
            "tabla_reg": tabla_reg,
            "tabla_bases": tabla_bases(off, mm1_raw, efic_set, n_vent),
            "nota_on": ("" if g["ontarget"] is None else
                        " Para este gen, que es de <em>Dalbulus maidis</em>, los hits "
                        "contra su propio genoma son <strong>on-target</strong> y se "
                        "excluyen del cómputo."),
            "veredicto": NARRATIVA[g["id"]]["veredicto"],
            "parrafo_region": NARRATIVA[g["id"]]["region"],
            "pendientes": NARRATIVA[g["id"]]["pendientes"],
        }
        (out / ("%s.html" % g["id"])).write_text(pagina(g, datos), encoding="utf-8")
        resumen_global.append({
            "gen": g["id"], "declarado": g["declarado"], "calculado": len(efic_set),
            "region": "%d-%d" % (a0, b0), "efic_region": efic_region,
            "off_region": off_region, "mejor": "%d-%d" % (m0, m1),
            "efic_mejor": mejor["eficientes"], "off_mejor": off_mejor,
            "riesgo_region_total": riesgo_region_tot,
            "riesgo_mejor_total": riesgo_mejor_tot,
        })
        print("%-12s escrito  efic %d/%d  region %d  mejor %d" % (
            g["id"], len(efic_set), n_vent, efic_region, mejor["eficientes"]))

    (out / "resumen.json").write_text(
        json.dumps(resumen_global, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "index.html").write_text(indice(resumen_global, a.modo), encoding="utf-8")
    print("\nresumen en %s" % (out / "resumen.json"))
    print("indice en  %s" % (out / "index.html"))
    return 0


def indice(res, modo):
    filas = []
    for r, g in zip(res, GENES):
        brecha = r["efic_mejor"] - r["efic_region"]
        pct = (100.0 * brecha / r["efic_mejor"]) if r["efic_mejor"] else 0
        filas.append(
            "<tr><td><a href='%s.html'><strong>%s</strong></a><br>"
            "<span style='color:var(--text-dim);font-size:.85rem'>%s</span></td>"
            "<td class='n'>%d</td><td class='n'>%d</td>"
            "<td>%s<br><span style='color:var(--text-dim);font-size:.85rem'>"
            "%d efic · %d off</span></td>"
            "<td>%s<br><span style='color:var(--text-dim);font-size:.85rem'>"
            "%d efic · %d off</span></td>"
            "<td class='n'>−%.0f %%</td></tr>" % (
                r["gen"], html.escape(g["nombre"]), html.escape(g["funcion"]),
                r["declarado"], r["calculado"],
                r["region"], r["efic_region"], r["off_region"],
                r["mejor"], r["efic_mejor"], r["off_mejor"], pct))
    return """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Los cuatro genes de EPILAB: perfil de eficiencia y off-targets</title>
<style>%(css)s</style>
</head>
<body>
<div class="wrap">
<header>
  <p class="eyebrow">Investigathon Y-Hat · track chicharrita / ARNi</p>
  <h1>Los cuatro genes de EPILAB</h1>
  <p class="sub">Perfil de siRNA eficientes a lo largo de cada gen, la región que
  eligió EPILAB contra la más densa, y el tamizaje de off-targets a 21 nt contra seis
  referencias. Una página por gen.</p>
</header>

<div class="verdict">
  <h2>Los tres resultados</h2>
  <p><strong>Uno.</strong> Ninguna de 15.120 configuraciones de si-Fi21 reproduce los
  cuatro conteos declarados en la planilla. El orden de magnitud es correcto; el
  número exacto no sale. <span class="tag tag-e">[E]</span></p>
  <p><strong>Dos.</strong> Las cuatro regiones elegidas están por debajo del óptimo
  por densidad de siRNA eficientes, entre un 19 %% y un 46 %%.
  <span class="tag tag-e">[E]</span></p>
  <p><strong>Tres.</strong> Los off-targets no explican esas elecciones. En
  <code>BicC_Dm</code> la contradicen: la región elegida es a la vez menos eficiente y
  once veces más expuesta que la alternativa, que gana en los dos ejes a la vez.
  <span class="tag tag-e">[E]</span></p>
</div>

<h2>Resumen</h2>
<table>
<thead><tr><th>Gen</th><th class='n'>Declarado</th><th class='n'>Calculado</th>
<th>Región de EPILAB</th><th>Región más densa</th><th class='n'>Brecha</th></tr></thead>
<tbody>%(filas)s</tbody>
</table>
<p>«Declarado» es la columna 5 de la planilla, para el gen entero. «Calculado» es
nuestro port en modo %(modo)s. «off» cuenta ventanas con bloque perfecto de 19 nt o
más en alguna referencia no objetivo.</p>

<h2>La columna que faltaba</h2>
<p>La columna 9 de la planilla se llama <em>«Nro de eficientes por región?»</em>, con
signo de pregunta, y está vacía en las cuatro filas. Es la que el investigador pidió
llenar. Con su procedimiento —recortar la región y correrla sola— los valores son
<strong>16, 14, 17 y 16</strong>. Contando las mismas ventanas dentro de la corrida
del gen entero son 30, 17, 20 y 18: una diferencia de hasta el 47 %%, porque un
fragmento recortado pierde el contexto de plegado de sus extremos. Los dos números
son defendibles y no son comparables entre sí.
<span class="tag tag-e">[E]</span></p>

<footer>
  <p>Generado por <code>tools/sifi21_port/informe_html.py</code>. Detalle completo en
  <code>research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md</code>. Todo corrió
  local; ninguna secuencia salió de la máquina.</p>
</footer>
</div>
</body>
</html>
""" % {"css": CSS, "filas": "".join(filas), "modo": modo}


# Narrativa por gen: se escribe a mano porque es interpretacion, no calculo.
NARRATIVA = {
    "MP_MRFV": {
        "veredicto": """
<p>Es el gen con más siRNA eficientes de los cuatro en términos absolutos, y el
único donde el conteo declarado y uno de nuestros modos coinciden exacto — lo que
resultó ser casualidad, porque esa misma configuración falla en los otros tres.
<span class="tag tag-e">[E]</span></p>
<p>La región elegida, la 1-200, es el arranque del gen. No es la más densa: hay un
tramo a partir de la posición 72 que tiene ocho siRNA eficientes más. La exposición
a off-targets es idéntica en las dos, así que la seguridad no explica la
elección.</p>""",
        "region": """La región 1-200 tiene 30 siRNA eficientes y la 72-271 tiene 38, un
21 % más, con la misma cantidad de ventanas comprometidas. Las dos regiones se
solapan en buena parte, así que el cambio es barato: correr el inicio 71 posiciones
hacia adelante. <span class="tag tag-h">[H]</span> Que el gen arranque justo en el
codón de inicio sugiere que la región pudo elegirse por conveniencia de construcción
más que por el perfil, pero eso no lo medimos.""",
        "pendientes": """
<p>El gen tiene 22 ventanas con off-target perfecto, pero <strong>solo 2 de ellas son
eficientes</strong>, así que el riesgo real es bajo: una ventana que no se carga en
el complejo silenciador no corta nada, ni en el blanco ni fuera de él. Esa
distinción —ventana riesgosa contra ventana riesgosa <em>y</em> activa— es la que
conviene llevar al diseño. <span class="tag tag-h">[H]</span></p>
<p>Con el criterio de un desajuste aparece el número más alto del gen:
<strong>18 ventanas con coincidencia en maíz</strong>, contra 3 con bloque perfecto.
<span class="tag tag-e">[E]</span> El cultivo es el no objetivo que más importa, así
que ese salto merece revisarse ventana por ventana antes de construir nada.</p>
<p>Las 9 coincidencias contra el genoma de <em>Dalbulus maidis</em> son off-target
acá, porque el blanco es el virus y no el insecto. Están contadas como tales.</p>""",
    },
    "CP_MRFV": {
        "veredicto": """
<p>Es el gen más limpio de los cuatro y por lejos: <strong>cero coincidencias con el
criterio de bloque perfecto</strong> contra las cinco referencias no objetivo, en todo
el gen. <span class="tag tag-e">[E]</span></p>
<p>Con el criterio más amplio —21 nt con un desajuste— sí aparecen coincidencias, 14
ventanas en total, de las cuales 6 en maíz. No es cero, y conviene decirlo: el gen es
el más limpio del conjunto, no un gen sin riesgo.
<span class="tag tag-e">[E]</span></p>
<p>Aun así la conclusión sobre la elección de región se sostiene: con el criterio
principal no hay nada que esquivar en ningún tramo, así que acá la región
<strong>no pudo haberse elegido por off-targets</strong>. Y tampoco es la más
densa.</p>""",
        "region": """La región 201-400 tiene 17 siRNA eficientes contra 21 de la
99-298. La brecha es la más chica de los cuatro genes, un 19 %, y sin off-targets de
por medio la decisión es puramente de densidad. <span class="tag tag-q">[?]</span>
Las coordenadas de la planilla dicen «200-400», que son 201 posiciones para una
secuencia de 200 nt; se resolvió localizando la subcadena exacta, que es la
201-400.""",
        "pendientes": """
<p>Este es el gen donde la conservación entre aislados sí podría explicar la
elección, y no lo medimos acá. W5 ya había encontrado que la región de cápside
elegida es 100 % idéntica solo al aislado de Costa Rica, y que contra los 45
registros brasileños la identidad baja al 91,5-93,5 %, con una mediana de 44 de 180
siRNA con apareamiento perfecto. <span class="tag tag-r">[R]</span> Cruzar eso con
este perfil es el próximo paso obvio: una región más densa que funcione solo en un
aislado no sirve.</p>""",
    },
    "BicC_Dm": {
        "veredicto": """
<p>Es el caso más fuerte de los cuatro, y el único donde la hipótesis de los
off-targets queda <strong>refutada en vez de simplemente descartada</strong>.
<span class="tag tag-e">[E]</span></p>
<p>La región que eligió EPILAB tiene 20 siRNA eficientes y 33 ventanas con
off-target. La región 2123-2422, del otro extremo del gen, tiene 37 eficientes y 3
ventanas comprometidas: <strong>casi el doble de potencia con un onceavo de la
exposición</strong>. Domina en los dos ejes a la vez, así que no hay compromiso entre
eficacia y seguridad que justifique la elección original.</p>""",
        "region": """La brecha es la más grande de los cuatro: 46 % menos siRNA
eficientes que el óptimo. Y a diferencia de los otros genes, acá las dos regiones
están muy lejos entre sí —una al principio, la otra casi al final de un gen de 2.520
nt—, así que no es un ajuste de coordenadas sino otra región. La concentración de
off-targets en la zona elegida tiene explicación biológica: Bicaudal C está
conservado entre cicadélidos, y ese tramo cae en una porción conservada.
<span class="tag tag-h">[H]</span>""",
        "pendientes": """
<p>Acá está el riesgo no objetivo más serio de todo el conjunto.
<strong>40 ventanas del gen tienen coincidencia perfecta de 21 sobre 21 con
<em>Homalodisca vitripennis</em></strong>, una chicharrita que no es nuestro blanco,
y 3 la tienen con <em>Harmonia axyridis</em>, una vaquita predadora, o sea un enemigo
natural del propio objetivo. <span class="tag tag-e">[E]</span> Esto no es una
sorpresa —es lo esperable para un gen de desarrollo conservado— pero sí es una
restricción de diseño que hay que declarar.</p>
<p>Sobre los polinizadores hay que ser preciso, porque es fácil pasarse de
optimista. Con el criterio de bloque perfecto, <em>Apis mellifera</em> da
<strong>cero</strong> en los cuatro genes. Con el criterio de un desajuste no da
cero: este gen tiene 7 ventanas. <span class="tag tag-e">[E]</span> Son coincidencias
más débiles, pero existen, y la frase defendible es «sin homología perfecta en abeja»,
no «sin riesgo en abeja».</p>
<p><span class="tag tag-q">[?]</span> El panel sigue siendo de especies modelo. La
ausencia de riesgo en cicadélidos nativos y en parasitoides <strong>no está
medida</strong>, porque no hay transcriptomas públicos. Seis referencias no son el
ambiente, y para un gen tan conservado esa laguna pesa más que para los otros
tres.</p>""",
    },
    "ATPaseD_Dm": {
        "veredicto": """
<p>Es el gen más corto de los cuatro, 491 nt, y el que menos margen deja: la región
elegida de 300 nt ocupa más de la mitad del gen, así que casi no hay alternativas
independientes para comparar.</p>
<p>La mejor región encontrada, la 136-435, está apenas 15 posiciones corrida de la
elegida y comparte casi todo el tramo. La ganancia es real pero chica, y la
exposición a off-targets es idéntica.</p>""",
        "region": """La región 151-450 tiene 18 siRNA eficientes contra 24 de la
136-435. Las dos se solapan en 285 de sus 300 posiciones, así que la diferencia la
hacen los extremos: correr el inicio 15 posiciones hacia atrás suma 6 siRNA
eficientes sin agregar ventanas comprometidas. Es la corrección más barata de los
cuatro genes. <span class="tag tag-h">[H]</span>""",
        "pendientes": """
<p>Es el único gen de los cuatro donde hay ventanas que son <strong>a la vez
eficientes y con off-target</strong> en una referencia no objetivo: 2 contra
<em>Homalodisca vitripennis</em>. En los otros genes las ventanas riesgosas resultaron
ser casi todas ineficientes. <span class="tag tag-e">[E]</span></p>
<p>La V-ATPasa es el blanco con más respaldo experimental del conjunto: W5 ya
registró un preprint que probó ARNi oral contra las subunidades B y D en
<em>D. maidis</em> con mortalidad significativa. <span class="tag tag-r">[R]</span>
Eso lo vuelve el candidato más defendible pese al margen chico, y vale decirlo junto
con el perfil.</p>""",
    },
}

if __name__ == "__main__":
    sys.exit(main())
