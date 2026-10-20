"""Genera research/ola3/C6_panel_y_largo/index.html desde resultados/panel_y_k.json.

Sin dependencias externas. Uso: python3 informe_html.py
"""
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RES = AQUI.parent / "resultados"
d = json.loads((RES / "panel_y_k.json").read_text())

NOMBRE = {"MP_MRFV": "proteína de movimiento · virus", "CP_MRFV": "cápside · virus",
          "BicC_Dm": "Bicaudal C · chicharrita", "ATPaseD_Dm": "V-ATPasa subunidad D · chicharrita"}
# Barrido por largo de region, de resultados/ (seccion 3.1 del REPORT)
ESCAPE = {
    "BicC_Dm": [(300, 497, 2201, "922-1221", 36, "2123-2422", 37),
                (250, 741, 2251, "973-1222", 29, "973-1222", 29),
                (200, 991, 2301, "1022-1221", 25, "1022-1221", 25)],
    "ATPaseD_Dm": [(300, 0, 172, None, 0, "136-435", 24),
                   (250, 44, 222, "38-287", 17, "122-371", 21),
                   (200, 94, 272, "88-287", 17, "272-471", 19),
                   (150, 161, 322, "136-285", 15, "136-285", 15)],
}


def barra(n, total):
    """Barra neutra: comunica la proporcion, no un juicio. El unico caso que se destaca
    es el cero, que si es cualitativo (no queda ninguna region)."""
    pct = 0 if not total else n / total * 100
    cls = "cero" if n == 0 else "neutro"
    return f'<span class="bar"><i class="{cls}" style="width:{max(pct,1.5):.1f}%"></i></span>'


filas_panel = ""
for g, v in d["panel_ampliado"].items():
    for et, r in v["regiones"].items():
        m, h = r["veto_nuevo"]["macrosteles_rna"], r["veto_nuevo"]["humano_rna"]
        vet = r["vetada_por_panel_nuevo"]
        etq = "EPILAB" if et == "epilab" else "W7 propone"
        filas_panel += (
            f'<tr class="{"veto" if vet else ""}"><td><code>{g}</code></td>'
            f'<td>{r["region"][0]}–{r["region"][1]}</td><td class="muted">{etq}</td>'
            f'<td>{r["eficientes"]}</td><td class="{"hot" if m else ""}">{m}</td><td>{h}</td>'
            f'<td>{"vetada" if vet else "limpia"}</td></tr>')

filas_k = ""
for g, v in d["k21_vs_k22"].items():
    a, b = v["k21"], v["k22"]
    j = v["solapamiento"]["jaccard"]
    mismo = a["mejor_region"][0] and abs(a["mejor_region"][0] - b["mejor_region"][0]) <= 2
    filas_k += (
        f'<tr><td><code>{g}</code></td><td>{a["eficientes"]} <span class="muted">({a["tasa"]:.1%})</span></td>'
        f'<td>{b["eficientes"]} <span class="muted">({b["tasa"]:.1%})</span></td>'
        f'<td>{a["epilab"]} → {b["epilab"]}</td>'
        f'<td>{a["mejor_region"][0]}–{a["mejor_region"][1]} <span class="muted">({a["mejor_eficientes"]})</span></td>'
        f'<td class="{"" if mismo else "hot"}">{b["mejor_region"][0]}–{b["mejor_region"][1]} '
        f'<span class="muted">({b["mejor_eficientes"]})</span></td>'
        f'<td>{barra(j*100,100)} {j:.2f}</td></tr>')

bloques_escape = ""
for g, rows in ESCAPE.items():
    tr = ""
    for (L, ok, tot, mejor, n, libre, nl) in rows:
        tr += (f'<tr><td>{L} nt</td><td>{barra(ok,tot)} {ok} / {tot}</td>'
               f'<td class="{"hot" if not mejor else ""}">{mejor or "ninguna"}</td><td>{n or "—"}</td>'
               f'<td class="muted">{libre} ({nl})</td></tr>')
    bloques_escape += f"""<div class="sub-card"><h4><code>{g}</code></h4>
<table><thead><tr><th>Largo</th><th>Regiones que escapan al veto</th><th>Mejor limpia</th><th>Efic.</th><th>Mejor sin restricción</th></tr></thead>
<tbody>{tr}</tbody></table></div>"""

anclas = " · ".join(f"{g} {v['obtenido']}" for g, v in d["anclas_21nt"].items())

html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Panel ampliado y largo de ventana</title>
<style>
:root{{--bg:#fff;--fg:#1c1f23;--mut:#5b6470;--line:#dfe3e8;--card:#f5f7f9;--azul:#2a6fdb;
--rojo:#c23b3b;--verde:#1f7a4d;--amar:#a85d00;--hot:#c23b3b1a}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#14171a;--fg:#e6e8eb;
--mut:#9aa4af;--line:#2b3138;--card:#1b1f24;--azul:#6aa3ff;--rojo:#ff8a8a;--verde:#5fd09a;
--amar:#f0a74a;--hot:#ff8a8a1f}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,sans-serif}}
main{{max-width:820px;margin:0 auto;padding:28px 16px 60px}}
.k{{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}}
h1{{font-size:26px;margin:6px 0 4px;line-height:1.2}}h2{{font-size:19px;margin:34px 0 10px}}
h3{{font-size:16px;margin:22px 0 6px}}h4{{font-size:14px;margin:0 0 6px}}
.lead{{color:var(--mut);margin:0 0 18px}}
.box{{background:var(--card);border-left:3px solid var(--rojo);padding:12px 16px;border-radius:6px;margin:16px 0}}
.box.ok{{border-left-color:var(--verde)}}.box p{{margin:6px 0}}
table{{width:100%;border-collapse:collapse;font-size:14px;margin:4px 0}}
th,td{{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left}}
th{{color:var(--mut);font-weight:600;font-size:13px}}
tr.veto td{{background:var(--hot)}}.hot{{color:var(--rojo);font-weight:600}}
.muted{{color:var(--mut)}}code{{font-size:.92em}}
.tw{{overflow-x:auto}}
.sub-card{{border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:12px 0}}
.bar{{display:inline-block;width:56px;height:8px;background:var(--line);border-radius:4px;
vertical-align:middle;overflow:hidden;margin-right:4px}}
.bar i{{display:block;height:100%}}.bar i.neutro{{background:var(--azul)}}.bar i.cero{{background:var(--rojo)}}
ul{{padding-left:20px}}li{{margin:5px 0}}.fine{{font-size:13px;color:var(--mut)}}
</style></head><body><main>
<div class="k">Investigathon Y-Hat · track chicharrita / ARNi · complemento de W7</div>
<h1>El panel ampliado y el largo de la ventana</h1>
<p class="lead">2026-10-20. Dos huecos del ranking de <a href="../../ola2/W7_ranking/index.html">W7</a>, medidos.
No lo reemplaza: los nulos, los percentiles y el barrido de pesos siguen siendo los de ahí.
Detalle en <a href="REPORT.md">REPORT.md</a>.</p>

<div class="box"><p><b>El resultado.</b> La recomendación de W7 de mover la región en los dos genes del
insecto <b>no sobrevive</b> a agregar al panel el cicadélido con genoma anotado más cercano a la
chicharrita, <i>Macrosteles quadrilineatus</i>. En <code>BicC_Dm</code> la región que W7 propone tiene
<b>19 ventanas idénticas en 21 nt</b> contra las 10 de la que eligió EPILAB: en ese eje, empeora.</p>
<p><b>Hay salida, y está medida.</b> En <code>BicC_Dm</code>, la región <b>922–1221</b> conserva 36 de las
37 ventanas eficientes y escapa al veto. En <code>ATPaseD_Dm</code> ninguna región de 300 nt escapa, así que
la salida es <b>acortar a 200 nt</b> — que además devuelve el diseño al rango de 150–250 que declaró el investigador.</p></div>

<h2>1. El veto con las dos referencias nuevas</h2>
<p class="fine">Coincidencia perfecta de 21 nt, el mismo criterio con el que W7 define su veto. Agregar
referencias sólo puede agregar vetos, nunca sacarlos, así que correr las nuevas por separado alcanza para falsar
una región «limpia».</p>
<div class="tw"><table><thead><tr><th>Gen</th><th>Región</th><th>Origen</th><th>Efic.</th>
<th><i>M. quadrilineatus</i></th><th>Humano</th><th></th></tr></thead><tbody>{filas_panel}</tbody></table></div>

<div class="box ok"><p><b>Humano da cero en los cuatro genes</b> bajo el criterio de bloque perfecto. Es el dato
tranquilizador y conviene decirlo con su alcance: es ausencia de homología en un transcriptoma de referencia,
no un ensayo de toxicidad. Los dos genes virales quedan intactos con las dos referencias nuevas.</p></div>

<h3>Cuánto material queda, y qué proponer en su lugar</h3>
{bloques_escape}

<h2>2. Veintiuno contra veintidós nucleótidos</h2>
<p class="fine">Lo pidió el investigador en el checkpoint. <code>R1_fundamentos</code> §2.1 establece que el largo
del siRNA lo fija la Dicer del organismo y que <b>para hemípteros no hay perfil publicado</b>, así que correr sólo
a 21 nt fija un parámetro que nadie midió en la especie.</p>
<div class="tw"><table><thead><tr><th>Gen</th><th>Efic. 21 nt</th><th>Efic. 22 nt</th>
<th>En región EPILAB</th><th>Mejor región 21</th><th>Mejor región 22</th><th>Jaccard</th></tr></thead>
<tbody>{filas_k}</tbody></table></div>

<div class="box"><p><b>El agregado es estable y el detalle no.</b> Las tasas se mueven menos de un punto
porcentual, pero entre el <b>41 % y el 67 %</b> de las ventanas eficientes a 21 nt no lo son a 22, y casi
lo mismo en la otra dirección.
En <code>MP_MRFV</code> —el mejor candidato del ranking— la mejor región de 200 nt se muda de 72–271 a
<b>820–1019</b>, al otro extremo del gen. En los dos genes del insecto se corre una sola posición, así que
ahí la elección sí es robusta.</p></div>

<h2>Qué queda abierto</h2>
<ul>
<li><b>Si <i>M. quadrilineatus</i> cuenta como no objetivo es una pregunta para el laboratorio</b>, no nuestra:
es a su vez plaga y vector de fitoplasmas. Lo que esto muestra es que la recomendación de W7 <i>depende</i> de esa
respuesta, no que esté mal.</li>
<li><b>Faltan 18 especies del catálogo propio</b> (<code>pipeline/no_objetivo_catalogo.py</code> tiene 26, el panel
cubre 8). Por el patrón, las siguientes son <i>Nilaparvata lugens</i> y <i>Acyrthosiphon pisum</i>.</li>
<li>Las regiones propuestas acá <b>no están verificadas contra la conservación dentro de <i>D. maidis</i></b>,
igual que las de W7.</li>
<li>El <b>puntaje de limpieza completo no se recalculó</b>: se corrieron sólo las dos referencias nuevas.</li>
</ul>

<p class="fine">Anclas verificadas antes de medir: {anclas} ventanas eficientes, los cuatro conteos de W7 exactos
(modo corregido, ViennaRNA 2.7.2). <code>panel_y_k.py</code> aborta si no coinciden.
Reproducir: ver §6 de <a href="REPORT.md">REPORT.md</a>.</p>
</main></body></html>
"""
(AQUI.parent / "index.html").write_text(html, encoding="utf-8")
print("escrito", AQUI.parent / "index.html", len(html), "bytes")
