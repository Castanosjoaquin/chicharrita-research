/* si-Fi+ — la interfaz.
 *
 * El grafico son DOS paneles que comparten el eje de posicion, no uno con dos escalas:
 *
 *   Panel de arriba (paridad).  La curva del «RNAi design plot» del si-Fi21 original:
 *       cuantos siRNA eficientes se superponen a cada posicion del ARNm, con la linea de
 *       referencia de todos los siRNA (plana en el tamano de la ventana). Es la curva que el
 *       investigador reconoce, y la que se reprodujo tramo por tramo contra su programa.
 *   Panel de abajo (decision).  Cuantos eficientes tendria una region de largo L centrada en
 *       cada posicion. No existe en el original: es la variable de decision, porque elegir
 *       region es elegir un punto de esta curva (D14). Debajo, las tres tiras de marcas.
 *
 * Por que dos paneles y no dos curvas en uno: son dos medidas con escalas distintas —la de
 * arriba topea en el tamano de la ventana, la de abajo en decenas—. Meterlas en un eje seria
 * un grafico de doble escala, que es exactamente lo que no se hace.
 *
 * Este archivo no calcula ningun veredicto: dibuja lo que manda `perfil.py`.
 */
'use strict';

// ---------------------------------------------------------------- utilidades

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const esc = (s) => String(s).replace(/[&<>"]/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const num = (n) => Number(n).toLocaleString('es-AR');

async function pedir(ruta, cuerpo, metodo) {
  const op = { method: metodo || (cuerpo ? 'POST' : 'GET') };
  if (cuerpo) {
    op.headers = { 'Content-Type': 'application/json' };
    op.body = JSON.stringify(cuerpo);
  }
  const r = await fetch(ruta, op);
  const d = await r.json().catch(() => ({ error: 'respuesta ilegible del servidor' }));
  if (!r.ok) throw new Error(d.error || ('HTTP ' + r.status));
  return d;
}

function aviso(donde, texto, clase) {
  $(donde).innerHTML = texto
    ? `<div class="aviso ${clase || ''}">${texto}</div>` : '';
}

/** Tramos de posiciones consecutivas, para dibujar una marca por tramo y no por posicion.
 *  `BicC_Dm` tiene 2.500 ventanas: una marca por ventana son 2.500 nodos por tira. */
function tramos(posiciones) {
  const out = [];
  let ini = null, prev = null;
  for (const p of posiciones) {
    if (ini === null) { ini = prev = p; continue; }
    if (p === prev + 1) { prev = p; continue; }
    out.push([ini, prev]); ini = prev = p;
  }
  if (ini !== null) out.push([ini, prev]);
  return out;
}

// ---------------------------------------------------------------- estado

const S = {
  arranque: null,
  gen: null,        // { contrato, columnas, tabla }
  col: {},          // nombre de columna -> indice
  off: null,        // resultado del tamizaje
  seleccion: null,  // [a, b] en coordenadas del gen
  orden: { col: 0, asc: true },
};

// ---------------------------------------------------------------- geometria del svg

const G = {
  W: 980, ML: 54, MR: 16,
  MT_A: 26, H_A: 104,
  MT_B: 172, H_B: 124,
  LANE_H: 11, LANE_GAP: 7,
};
G.PW = G.W - G.ML - G.MR;
G.baseA = G.MT_A + G.H_A;
G.baseB = G.MT_B + G.H_B;
G.RUG = G.baseB + 24;
G.H = G.RUG + 3 * (G.LANE_H + G.LANE_GAP) + 20;

const sx = (p, n) => G.ML + (p - 1) * G.PW / Math.max(1, n - 1);
const px = (x, n) => Math.round(1 + (x - G.ML) * Math.max(1, n - 1) / G.PW);

function ticksX(n) {
  let paso = Math.max(1, Math.floor(n / 8));
  const mag = Math.pow(10, String(paso).length - 1);
  paso = Math.max(mag, Math.floor(paso / mag) * mag);
  const out = [];
  for (let t = 0; t <= n; t += paso) out.push(t || 1);
  return out;
}

function ejeY(o, base, alto, max, etiqueta) {
  for (let i = 0; i <= 4; i++) {
    const v = max * i / 4;
    const y = base - (v / Math.max(max, 1)) * alto;
    o.push(`<line class="grid" x1="${G.ML}" y1="${y.toFixed(1)}" x2="${G.W - G.MR}" y2="${y.toFixed(1)}"/>`);
    o.push(`<text class="tick" x="${G.ML - 7}" y="${(y + 3.5).toFixed(1)}" text-anchor="end">${Math.round(v)}</text>`);
  }
  o.push(`<line class="axis" x1="${G.ML}" y1="${base}" x2="${G.W - G.MR}" y2="${base}"/>`);
  o.push(`<text class="eje-lab" x="${G.ML}" y="${base - alto - 9}">${esc(etiqueta)}</text>`);
}

function curva(o, serie, base, alto, max, n, clase, desde, hasta) {
  const pts = [];
  for (let i = 0; i < serie.length; i++) {
    const x = sx(i + 1, n);
    const y = base - (serie[i] / Math.max(max, 1)) * alto;
    pts.push(`${x.toFixed(1)},${y.toFixed(1)}`);
  }
  if (!pts.length) return;
  if (clase.includes('area')) {
    o.push(`<polygon class="area" points="${sx(1, n).toFixed(1)},${base} ${pts.join(' ')} ${sx(serie.length, n).toFixed(1)},${base}"/>`);
  }
  // El tramo donde la region no entra completa va punteado: ahi el valor baja porque hay
  // menos ventanas alcanzables, no porque la secuencia sea peor.
  if (desde !== undefined) {
    const i0 = Math.max(0, desde - 1), i1 = Math.min(pts.length, hasta);
    if (i0 > 0) o.push(`<polyline class="line line-borde" points="${pts.slice(0, i0 + 1).join(' ')}"/>`);
    o.push(`<polyline class="line" points="${pts.slice(i0, i1).join(' ')}"/>`);
    if (i1 < pts.length) o.push(`<polyline class="line line-borde" points="${pts.slice(i1 - 1).join(' ')}"/>`);
  } else {
    o.push(`<polyline class="line" points="${pts.join(' ')}"/>`);
  }
}

function dibujar(d) {
  // El dominio del eje x es la POSICION EN EL GEN (1..largo), igual que el original
  // («mRNA sequence position», `xlim=[0, len(query)]`). No las ventanas: hay `largo` posiciones
  // y solo `largo - size + 1` ventanas, asi que mezclar las dos escalas corre la curva de
  // solapamiento 20 posiciones hacia la derecha. La curva de densidad esta indexada por el
  // arranque de la ventana, que tambien es una posicion del gen, y por eso termina antes: en
  // las ultimas 20 posiciones no empieza ninguna ventana.
  const n = d.largo, o = [];
  o.push(`<svg viewBox="0 0 ${G.W} ${G.H}" width="100%" class="plot" id="svg-perfil"
    role="img" preserveAspectRatio="xMidYMid meet"
    aria-label="Perfil de siRNA a lo largo de ${esc(d.nombre)}: curva de solapamiento y curva de densidad por region">`);

  // --- bandas (detras de todo), en los dos paneles
  const bandas = (d.bandas || []).concat([{
    ini: d.mejor.inicio, fin: d.mejor.fin, etq: 'más densa', clase: 'band-best',
  }]);
  const centros = bandas.map((b) => (sx(Math.max(1, b.ini), n) + sx(Math.min(n, b.fin), n)) / 2);
  const escalonar = centros.length > 1 && Math.abs(centros[0] - centros[1]) < 80;
  bandas.forEach((b, i) => {
    const x1 = sx(Math.max(1, b.ini), n), x2 = sx(Math.min(n, b.fin), n);
    const w = Math.max(2, x2 - x1);
    const cls = b.clase || 'band';
    o.push(`<rect class="${cls}" x="${x1.toFixed(1)}" y="${G.MT_A}" width="${w.toFixed(1)}" height="${G.H_A}"/>`);
    o.push(`<rect class="${cls}" x="${x1.toFixed(1)}" y="${G.MT_B}" width="${w.toFixed(1)}" height="${G.H_B}"/>`);
    const cx = Math.min(Math.max(centros[i], G.ML + 34), G.W - G.MR - 34);
    const dy = escalonar && i === 0 ? -11 : 0;
    o.push(`<text class="band-lab ${cls}-lab" x="${cx.toFixed(1)}" y="${G.MT_B - 5 + dy}">${esc(b.etq || '')}</text>`);
  });

  // --- seleccion: los dos rectangulos existen siempre, con ancho cero. Durante el arrastre
  // se les mueve x y width y nada mas. Redibujar el SVG entero en cada mousemove rehacia dos
  // polilineas de miles de puntos por pixel de mouse, y —peor— reemplazaba el elemento, con
  // lo que el manejador en curso quedaba sobre un nodo desprendido: ahi getBoundingClientRect
  // devuelve cero, la division da Infinity y el rango saltaba al final del gen.
  o.push(`<rect class="sel" id="sel-a" x="0" y="${G.MT_A}" width="0" height="${G.H_A}"/>`);
  o.push(`<rect class="sel" id="sel-b" x="0" y="${G.MT_B}" width="0" height="${G.H_B}"/>`);

  // --- PANEL A: la curva del original
  const maxA = Math.max(d.size, 1);
  ejeY(o, G.baseA, G.H_A, maxA, 'siRNA que cubren la posición');
  // Linea de referencia: todos los siRNA. Es una constante (el tamano de la ventana), no una
  // serie, asi que va gris, punteada y con etiqueta directa en vez de color propio.
  curva(o, d.todos, G.baseA, G.H_A, maxA, n, 'ref-solo');
  o[o.length - 1] = o[o.length - 1].replace('class="line"', 'class="ref"');
  o.push(`<text class="ref-lab" x="${G.W - G.MR - 2}" y="${(G.baseA - G.H_A + 10).toFixed(1)}" text-anchor="end">todos los siRNA (${d.size})</text>`);
  curva(o, d.solapamiento, G.baseA, G.H_A, maxA, n, 'line');

  // --- PANEL B: la curva de densidad
  const maxB = Math.max(d.dens_max, 1);
  ejeY(o, G.baseB, G.H_B, maxB, `siRNA eficientes en una región de ${d.largo_region} nt centrada acá`);
  curva(o, d.densidad, G.baseB, G.H_B, maxB, n, 'line area', d.centro_min, d.centro_max);

  // --- tiras
  // Cada tira lleva su nombre corto a la izquierda. Numerarlas 1-2-3 obliga a ir y volver a
  // la leyenda para saber cual es cual, que es trabajo que la figura tiene que ahorrar.
  const lanes = [
    ['eficiente', 'Ventana eficiente', d.eficientes, 'tick-efic'],
    ['off ≥' + Math.min(19, d.size), 'Off-target: bloque perfecto ≥' + Math.min(19, d.size) + ' nt',
      d.off_perfecto, 'tick-off'],
    ['1 desaj.', 'Off-target: ' + d.size + ' nt con 1 desajuste', d.off_mm1, 'tick-mm1'],
  ];
  lanes.forEach(([corto, etq, pos, cls], li) => {
    const y = G.RUG + li * (G.LANE_H + G.LANE_GAP);
    o.push(`<rect class="lane" x="${G.ML}" y="${y}" width="${G.PW}" height="${G.LANE_H}"/>`);
    o.push(`<text class="lane-lab" x="${G.ML - 6}" y="${y + G.LANE_H - 2}" text-anchor="end">${esc(corto)}</text>`);
    if (pos === null || pos === undefined) {
      o.push(`<text class="tick" x="${G.ML + 6}" y="${y + G.LANE_H - 2}">sin medir — ${esc(etq)}</text>`);
      return;
    }
    if (!pos.length) {
      o.push(`<text class="tick" x="${G.ML + 6}" y="${y + G.LANE_H - 2}">medido, ninguna — ${esc(etq)}</text>`);
      return;
    }
    for (const [a, b] of tramos(pos)) {
      const x1 = sx(a, n), x2 = sx(Math.min(b + 1, n), n);
      o.push(`<rect class="${cls}" x="${x1.toFixed(1)}" y="${y}" width="${Math.max(1.4, x2 - x1).toFixed(1)}" height="${G.LANE_H}"/>`);
    }
  });

  // --- eje x compartido
  for (const t of ticksX(n)) {
    o.push(`<text class="tick" x="${sx(Math.min(t, n), n).toFixed(1)}" y="${G.H - 6}" text-anchor="middle">${t}</text>`);
  }

  // --- capa de interaccion
  o.push(`<line class="cross" id="cruz" x1="0" y1="${G.MT_A}" x2="0" y2="${G.RUG + 3 * (G.LANE_H + G.LANE_GAP)}" style="display:none"/>`);
  o.push(`<rect class="hit" id="hit" x="${G.ML}" y="${G.MT_A}" width="${G.PW}" height="${G.RUG + 3 * (G.LANE_H + G.LANE_GAP) - G.MT_A}"/>`);
  o.push('</svg>');
  return o.join('\n');
}

function leyenda(d) {
  const l = ['<ul class="legend">',
    '<li><span class="sw sw-efic"></span>siRNA eficiente</li>',
    '<li><span class="sw sw-todos"></span>todos los siRNA (referencia)</li>'];
  if (d.off_perfecto) l.push('<li><span class="sw sw-off"></span>off-target: bloque perfecto</li>');
  if (d.off_mm1) l.push('<li><span class="sw sw-mm1"></span>off-target: 1 desajuste</li>');
  l.push('</ul>');
  return l.join('');
}

// ---------------------------------------------------------------- vista de diseño

function params() {
  const p = {};
  for (const k of ['sirna_size', 'accessibility_window']) p[k] = parseInt($('#' + k).value, 10);
  for (const k of ['end_stability_threshold', 'accessibility_threshold']) p[k] = parseFloat($('#' + k).value);
  for (const k of ['strand_check', 'end_check', 'accessibility_check', 'terminal_check']) p[k] = $('#' + k).checked;
  return p;
}

function cadenaConfig() {
  const p = params();
  const bits = ['strand_check', 'end_check', 'accessibility_check', 'terminal_check']
    .map((k) => (p[k] ? '1' : '0')).join('');
  const g = (v) => (String(v).includes('.') ? String(v) : v + '.0');
  return `siFi21_${p.accessibility_window}_${g(p.end_stability_threshold)}_${g(p.accessibility_threshold)}_${bits}`;
}

function notaModo() {
  const fiel = $('#modo').value === 'fiel';
  $('#nota-modo').innerHTML = fiel
    ? 'Reproduce la rama del original tal cual, incluido el atajo: cuando el nucleótido 19 '
      + 'es A/T y el 2 es G/C, decide <b>sólo</b> la accesibilidad y se saltea la '
      + 'termodinámica. Es el modo para auditar cualquier número producido con si-Fi.'
    : 'Aplica la preferencia terminal como filtro adicional sobre el veredicto '
      + 'termodinámico, que nunca se saltea. Es un subconjunto estricto del modo fiel.';
}

async function correrDiseno(e) {
  if (e) e.preventDefault();
  const secuencia = $('#secuencia').value.trim();
  if (!secuencia) { aviso('#aviso-diseno', 'Falta la secuencia.', 'mal'); return; }

  $('#btn-correr').disabled = true;
  $('#btn-correr').textContent = 'Corriendo…';
  aviso('#aviso-diseno', '');
  try {
    const d = await pedir('/api/diseno', {
      secuencia,
      modo: $('#modo').value,
      backend: $('#backend').value,
      temp_c: parseFloat($('#temp_c').value),
      tabla_nn: $('#tabla_nn').value,
      largo_region: parseInt($('#largo_region').value, 10),
      params: params(),
      con_seq: false,
      off_perfecto: S.off && S.off.consulta ? S.off.off_perfecto : null,
      off_mm1: S.off && S.off.consulta ? S.off.off_mm1 : null,
    });
    S.gen = d.genes[0];
    S.col = {};
    S.gen.columnas.forEach((c, i) => { S.col[c] = i; });
    S.seleccion = null;
    if (d.genes.length > 1) {
      aviso('#aviso-diseno', `El FASTA traía ${d.genes.length} secuencias; se muestra la `
        + `primera (<b>${esc(S.gen.contrato.nombre)}</b>).`, 'ojo');
    }
    pintarDiseno();
  } catch (err) {
    aviso('#aviso-diseno', esc(err.message), 'mal');
  } finally {
    $('#btn-correr').disabled = false;
    $('#btn-correr').textContent = 'Correr';
  }
}

function pintarDiseno() {
  const { contrato: c, tabla } = S.gen;
  const r = c.resumen;
  $('#vacio-diseno').hidden = true;

  const pct = (100 * r.eficientes / Math.max(1, r.ventanas)).toFixed(1);
  $('#salida-diseno').innerHTML = `
    <h2>${esc(c.nombre)} <span class="etq">${esc(c.etiqueta)}</span></h2>
    <ul class="kpis">
      <li><span class="n">${num(r.largo)}</span><span class="k">nt de secuencia</span></li>
      <li><span class="n">${num(r.ventanas)}</span><span class="k">ventanas de ${c.size} nt</span></li>
      <li><span class="n">${num(r.eficientes)}</span><span class="k">eficientes (${pct} %)</span></li>
      <li><span class="n">${num(c.mejor.eficientes)}</span><span class="k">en la región más densa</span></li>
      <li><span class="n">${c.mejor.inicio}–${c.mejor.fin}</span><span class="k">región de ${c.largo_region} nt más densa</span></li>
    </ul>
    <div id="aviso-sel"></div>
    <figure>
      ${leyenda(c)}
      <div class="lectura" id="lectura">Pasá el puntero por el gráfico para leer una posición.
        Arrastrá para marcar un rango.</div>
      ${dibujar(c)}
      <figcaption>
        <b>Arriba</b>, la curva del «RNAi design plot» del si-Fi21 original: cuántos siRNA
        eficientes se superponen a cada posición. <b>Abajo</b>, la variable de decisión:
        cuántos eficientes tendría una región de ${c.largo_region} nt centrada ahí. Son dos
        escalas distintas, por eso van en dos paneles y no en un eje.
      </figcaption>
    </figure>
    <h3>Desglose del criterio</h3>
    <ul class="kpis">
      <li><span class="n">${num(r.seleccion_hebra)}</span><span class="k">pasan selección de hebra</span></li>
      <li><span class="n">${num(r.estabilidad_extremos)}</span><span class="k">pasan estabilidad de extremos</span></li>
      <li><span class="n">${num(r.accesibilidad)}</span><span class="k">pasan accesibilidad</span></li>
      <li><span class="n">${num(r.solo_termodinamico)}</span><span class="k">pasan las tres (termodinámico)</span></li>
    </ul>
    <h3>Las ${num(tabla.length)} ventanas, una por fila</h3>
    <p class="nota">Esta tabla el original no la muestra nunca: de si-Fi sólo se puede sacar el
      total por gen, y únicamente por <code>Save as → Table (CSV)</code>. Clic en un
      encabezado para ordenar.</p>
    <div class="botones" id="exportes">
      <button class="boton-2" data-exp="tsv">TSV por ventana</button>
      <button class="boton-2" data-exp="features">TSV de términos</button>
      <button class="boton-2" data-exp="csv">CSV resumen (formato del original)</button>
      <button class="boton-2" data-exp="fasta">FASTA de los siRNA eficientes</button>
      <button class="boton-2" id="exp-html">Informe HTML</button>
    </div>
    <div id="aviso-exp"></div>
    <div class="tabla-marco"><table id="tabla-vent"></table></div>`;

  pintarTabla();
  conectarGrafico();
  $$('#exportes [data-exp]').forEach((b) => {
    b.onclick = () => exportar(b.dataset.exp);
  });
  $('#exp-html').onclick = informeHTML;
}

const ENCABEZADOS = {
  pos: 'pos', seq: 'secuencia', dg_sense5: 'ΔG 5′ sentido',
  dg_antisense5: 'ΔG 5′ antisentido', ddg: 'ΔΔG', accessibility: 'accesibilidad',
  nt19_at: 'nt19 A/T', nt2_gc: 'nt2 G/C', rama_terminal: 'rama',
  strand_selection: 'hebra', end_stability: 'extremos',
  target_site_accessibility: 'acces.', thermo_efficient: 'termodinámico',
  is_efficient: 'EFICIENTE', homopolimero: 'homopol.', baja_complejidad: 'baja compl.',
};

function pintarTabla() {
  const { columnas, tabla } = S.gen;
  const { col, asc } = S.orden;
  const filas = tabla.slice().sort((a, b) => {
    const x = a[col], y = b[col];
    const v = (typeof x === 'boolean') ? (x === y ? 0 : (x ? 1 : -1))
      : (typeof x === 'number' ? x - y : String(x).localeCompare(String(y)));
    return asc ? v : -v;
  });
  const cel = (v) => (typeof v === 'boolean'
    ? `<td class="${v ? 'si' : 'no'}">${v ? 'sí' : '—'}</td>`
    : `<td class="n">${typeof v === 'number' && !Number.isInteger(v) ? v.toFixed(4) : esc(v)}</td>`);

  $('#tabla-vent').innerHTML =
    '<thead><tr>' + columnas.map((c, i) =>
      `<th class="n" data-col="${i}">${esc(ENCABEZADOS[c] || c)}${i === col ? (asc ? ' ↑' : ' ↓') : ''}</th>`).join('')
    + '</tr></thead><tbody>'
    + filas.map((f) => `<tr class="${f[S.col.is_efficient] ? 'es-efic' : ''}">`
      + f.map(cel).join('') + '</tr>').join('')
    + '</tbody>';

  $$('#tabla-vent th').forEach((th) => {
    th.onclick = () => {
      const i = parseInt(th.dataset.col, 10);
      S.orden = { col: i, asc: i === S.orden.col ? !S.orden.asc : true };
      pintarTabla();
    };
  });
}

// ---------------------------------------------------------------- hover y seleccion

function conectarGrafico() {
  const svg = $('#svg-perfil'), hit = $('#hit'), cruz = $('#cruz');
  if (!svg) return;
  const c = S.gen.contrato, n = c.largo;   // mismo dominio que `dibujar`
  let arrastre = null;

  const posDe = (ev) => {
    const caja = svg.getBoundingClientRect();
    const x = (ev.clientX - caja.left) * G.W / caja.width;
    return Math.min(n, Math.max(1, px(x, n)));
  };

  const leer = (p) => {
    const i = p - 1;
    const fila = S.gen.tabla.find((f) => f[S.col.pos] === p);
    const partes = [`posición <b>${p}</b>`];
    const k = c.solapamiento[i];
    if (k !== undefined) {
      partes.push(k === 1
        ? `la cubre <b>1</b> siRNA eficiente de ${c.todos[i]}`
        : `la cubren <b>${k}</b> siRNA eficientes de ${c.todos[i]}`);
    }
    if (c.densidad[i] !== undefined) {
      const fuera = p < c.centro_min || p > c.centro_max;
      partes.push(`región de ${c.largo_region} nt centrada acá: <b>${c.densidad[i]}</b> eficientes`
        + (fuera ? ' <i>(recortada contra el borde)</i>' : ''));
    }
    if (fila) {
      const t = [];
      if (fila[S.col.strand_selection]) t.push('hebra');
      if (fila[S.col.end_stability]) t.push('extremos');
      if (fila[S.col.target_site_accessibility]) t.push('accesibilidad');
      partes.push(`la ventana que empieza acá: ${fila[S.col.is_efficient] ? '<b>eficiente</b>' : 'no eficiente'}`
        + (t.length ? ` — pasa ${t.join(', ')}` : ' — no pasa ningún término')
        + `, ΔΔG ${Number(fila[S.col.ddg]).toFixed(2)}, acc. ${Number(fila[S.col.accessibility]).toFixed(3)}, rama ${fila[S.col.rama_terminal]}`);
    }
    $('#lectura').innerHTML = partes.join(' · ');
  };

  hit.addEventListener('mousemove', (ev) => {
    const p = posDe(ev);
    const x = sx(p, n);
    cruz.setAttribute('x1', x); cruz.setAttribute('x2', x);
    cruz.style.display = '';
    if (arrastre !== null) { S.seleccion = [arrastre, p]; pintarBanda(); }
    else leer(p);
  });
  hit.addEventListener('mouseleave', () => { cruz.style.display = 'none'; });
  hit.addEventListener('mousedown', (ev) => {
    arrastre = posDe(ev);
    S.seleccion = [arrastre, arrastre];
    ev.preventDefault();
    // El mouseup se escucha en la ventana porque el puntero puede soltarse fuera del
    // grafico, y con `once` para no acumular un manejador por arrastre.
    window.addEventListener('mouseup', () => {
      const sel = S.seleccion;
      arrastre = null;
      if (!sel || Math.abs(sel[1] - sel[0]) < 2) limpiarSeleccion();
      else mostrarSeleccion();
    }, { once: true });
  });

  pintarBanda();
}

/** Mueve los dos rectangulos de seleccion. No redibuja nada mas. */
function pintarBanda() {
  const a = $('#sel-a'), b = $('#sel-b');
  if (!a || !b) return;
  if (!S.seleccion) {
    a.setAttribute('width', 0); b.setAttribute('width', 0);
    return;
  }
  const n = S.gen.contrato.largo;
  const x1 = sx(Math.max(1, Math.min(...S.seleccion)), n);
  const x2 = sx(Math.min(n, Math.max(...S.seleccion)), n);
  const w = Math.max(1, x2 - x1);
  for (const r of [a, b]) { r.setAttribute('x', x1.toFixed(1)); r.setAttribute('width', w.toFixed(1)); }
}

function limpiarSeleccion() {
  S.seleccion = null;
  pintarBanda();
  aviso('#aviso-sel', '');
}

function mostrarSeleccion() {
  if (!S.seleccion) { aviso('#aviso-sel', ''); return; }
  const c = S.gen.contrato;
  const a = Math.min(...S.seleccion), b = Math.max(...S.seleccion);
  const dentro = (xs) => (xs ? xs.filter((p) => p >= a && p <= b).length : null);
  const ef = dentro(c.eficientes);
  const off = dentro(c.off_perfecto), mm = dentro(c.off_mm1);
  aviso('#aviso-sel',
    `<b>Rango ${a}–${b}</b> (${num(b - a + 1)} nt): <b>${ef}</b> siRNA eficientes · `
    + `off-target con bloque perfecto: ${off === null ? '<i>sin medir</i>' : off} · `
    + `con 1 desajuste: ${mm === null ? '<i>sin medir</i>' : mm}`
    + `<div class="botones">`
    + `<input type="text" id="nombre-rango" placeholder="nombre del rango" style="width:200px">`
    + `<button class="boton-2" id="btn-guardar-rango">Guardar este rango</button>`
    + `<button class="boton-2" id="btn-fasta-rango">FASTA de este rango</button>`
    + `<button class="boton-2" id="btn-limpiar-sel">Limpiar</button></div>`, 'bien');

  $('#btn-guardar-rango').onclick = () => guardarRango(a, b, ef, off, mm);
  $('#btn-fasta-rango').onclick = () => exportar('fasta', [a, b]);
  $('#btn-limpiar-sel').onclick = limpiarSeleccion;
}

async function guardarRango(a, b, ef, off, mm) {
  const c = S.gen.contrato, r = c.resumen;
  try {
    await pedir('/api/rangos', {
      nombre: $('#nombre-rango').value.trim() || `${c.nombre} ${a}-${b}`,
      gen: c.nombre, inicio: a, fin: b,
      eficientes: ef, off_perfecto: off, off_mm1: mm,
      densidad: c.densidad[Math.floor((a + b) / 2) - 1],
      modo: r.modo, motor: r.backend, config: r.config, etiqueta: c.etiqueta,
      temp_c: r.temp_c, tabla_nn: r.tabla_nn,
    });
    aviso('#aviso-sel', `Guardado. Está en la pestaña <b>Rangos guardados</b>.`, 'bien');
    cargarRangos();
  } catch (err) {
    aviso('#aviso-sel', esc(err.message), 'mal');
  }
}

// ---------------------------------------------------------------- exportar

async function exportar(que, rango) {
  try {
    const d = await pedir('/api/exportar', {
      gen: S.gen.contrato.nombre, que, rango: rango || null,
      con_seq: que === 'tsv' ? confirm(
        'Incluir la columna con la secuencia de cada ventana?\n\n'
        + 'Como las ventanas se solapan de a 1 nt, esa columna reconstruye el gen entero. '
        + 'El archivo sale con un aviso y no hay que versionarlo ni subirlo a ningún '
        + 'servicio web.') : false,
    });
    aviso('#aviso-exp', `Escrito: <code>${esc(d.ruta)}</code> (${num(d.bytes)} bytes)`, 'bien');
  } catch (err) {
    aviso('#aviso-exp', esc(err.message), 'mal');
  }
}

/** El informe HTML lo serializa el navegador desde el SVG que ya esta en pantalla, asi que el
 *  archivo es exactamente lo que el usuario vio. El original, en cambio, exporta un PNG y le
 *  corrompe el nombre (`filename += filename + '.csv'`). */
function informeHTML() {
  const c = S.gen.contrato, r = c.resumen;
  const css = Array.from(document.styleSheets)
    .flatMap((h) => { try { return Array.from(h.cssRules).map((x) => x.cssText); } catch { return []; } })
    .join('\n');
  const svg = $('#svg-perfil').outerHTML.replace(/<(line class="cross"|rect class="hit")[^>]*>/g, '');
  const doc = `<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>si-Fi+ — ${esc(c.nombre)}</title><style>${css}</style></head>
<body><div class="wrap"><header><div class="titulo"><h1>${esc(c.nombre)}</h1></div>
<p class="sub">${esc(c.etiqueta)} · configuración <code>${esc(r.config)}</code> ·
generado por si-Fi+ el ${new Date().toLocaleString('es-AR')}</p></header><main>
<ul class="kpis">
<li><span class="n">${num(r.largo)}</span><span class="k">nt</span></li>
<li><span class="n">${num(r.ventanas)}</span><span class="k">ventanas de ${c.size} nt</span></li>
<li><span class="n">${num(r.eficientes)}</span><span class="k">eficientes</span></li>
<li><span class="n">${num(c.mejor.eficientes)}</span><span class="k">en ${c.mejor.inicio}–${c.mejor.fin}</span></li>
</ul>
<figure>${leyenda(c)}${svg}<figcaption>Arriba, la curva del «RNAi design plot» del si-Fi21
original. Abajo, los siRNA eficientes que tendría una región de ${c.largo_region} nt centrada
en cada posición.</figcaption></figure>
<p class="nota">Este informe no incluye secuencias: son coordenadas y conteos.</p>
</main></div></body></html>`;
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([doc], { type: 'text/html' }));
  a.download = `sifi_plus_${c.nombre}.html`;
  a.click();
  URL.revokeObjectURL(a.href);
}

// ---------------------------------------------------------------- off-target

function pintarBases() {
  $('#bases').innerHTML = S.arranque.bases.map((b) => `
    <div class="casilla">
      <input type="checkbox" class="base" value="${esc(b.id)}" ${b.en_panel ? 'checked' : ''}
             data-ontarget="${/genomic/.test(b.id) ? '1' : ''}">
      <label style="margin:0"><i>${esc(b.nombre)}</i>
        <span>${esc(b.papel || b.id)} · ${b.mb} MB</span></label>
    </div>`).join('') || '<p class="nota">No hay bases en <code>work/</code>.</p>';
}

async function correrOff(e) {
  if (e) e.preventDefault();
  const secuencia = $('#secuencia').value.trim();
  if (!secuencia) {
    aviso('#aviso-off', 'Falta la secuencia: pegala en la pestaña <b>Diseño</b>.', 'mal'); return;
  }
  const marcadas = $$('.base:checked');
  const ont = marcadas.find((i) => i.dataset.ontarget);
  $('#btn-off').disabled = true;
  aviso('#aviso-off', '');
  try {
    const { id } = await pedir('/api/offtarget', {
      secuencia,
      bases: marcadas.map((i) => i.value),
      size: parseInt($('#off_size').value, 10),
      min_block: parseInt($('#off_block').value, 10),
      mm1: $('#off_mm1').checked,
      ontarget: ont ? ont.value : null,
    });
    seguirOff(id);
  } catch (err) {
    aviso('#aviso-off', esc(err.message), 'mal');
    $('#btn-off').disabled = false;
  }
}

async function seguirOff(id) {
  $('#vacio-off').hidden = true;
  const t = await pedir('/api/offtarget/' + id);
  const pct = Math.round(100 * t.hecho / Math.max(1, t.total));
  if (t.estado === 'error') {
    aviso('#aviso-off', esc(t.error), 'mal');
    $('#btn-off').disabled = false;
    return;
  }
  if (t.estado !== 'listo') {
    $('#salida-off').innerHTML = `
      <div class="aviso"><b>${esc(t.estado)}</b>
        ${t.base_actual ? ' — ' + esc(t.base_actual) : ''}
        ${t.mensaje ? '<br>' + esc(t.mensaje) : ''}
        <div class="barra"><div style="width:${pct}%"></div></div>
        <span class="nota">${t.hecho} de ${t.total} bases · ${t.segundos} s</span></div>`;
    setTimeout(() => seguirOff(id), 600);
    return;
  }
  S.off = t.resultado;
  $('#btn-off').disabled = false;
  pintarOff(t);
}

/** Una cifra y, abajo, cuánto de esa cifra es cola de poli-A o repetición simple. */
function celdaConBaja(total, baja, destacar) {
  if (total === null || total === undefined) return '<td class="n"><span class="no">sin medir</span></td>';
  const neto = total - (baja || 0);
  return `<td class="n ${destacar && neto > 0 ? 'si' : ''}">${num(total)}`
    + (baja ? `<br><span class="nota">−${num(baja)} baja compl. → <b>${num(neto)}</b></span>` : '')
    + '</td>';
}

function pintarOff(t) {
  const r = S.off;
  const fil = r.bases.map((b) => `
    <tr>
      <td><i>${esc(b.nombre)}</i>${b.es_ontarget ? ' <span class="etq">(blanco)</span>' : ''}
        <br><span class="nota">${esc(b.papel || b.base)}</span></td>
      ${celdaConBaja(b.perfecto_21, b.perfecto_21_baja, !b.es_ontarget)}
      ${celdaConBaja(b.perfecto_ge19, b.perfecto_ge19_baja, false)}
      ${celdaConBaja(b.mm1_21, b.mm1_21_baja, false)}
      <td class="n">${num(b.referencias_distintas)}</td>
    </tr>`).join('');

  const hayBaja = r.ventanas_baja > 0;
  $('#salida-off').innerHTML = `
    <h2>${esc(r.consulta)} contra ${r.bases.length} referencias
      <span class="etq">${r.ventanas} ventanas de ${r.size} nt · ${t.segundos} s</span></h2>
    <p class="nota">Una corrida, todas las bases. El original elige una sola en un desplegable
      y su gráfico topea en cinco objetivos.</p>
    ${hayBaja ? `<div class="aviso ojo"><b>${num(r.ventanas_baja)} de las ${num(r.ventanas)}
      ventanas son de baja complejidad</b> y se descuentan aparte en cada celda. Una cola de
      poli-A pega en cualquier transcriptoma: no es homología, y sumarla al riesgo sin
      decirlo es lo que hace el original. Criterio: ${esc(r.criterio_baja)}.</div>` : ''}
    <div class="tabla-marco"><table>
      <thead><tr><th>Referencia</th><th class="n">${r.size}/${r.size} perfecto</th>
      <th class="n">bloque ≥${r.min_block} nt</th><th class="n">1 desajuste</th>
      <th class="n">registros distintos</th></tr></thead>
      <tbody>${fil}</tbody></table></div>
    <div class="botones">
      <button class="boton-2" id="btn-llevar">Llevar estas marcas al gráfico de diseño</button>
    </div>
    <p class="nota">Un acierto en el genoma del propio vector es el blanco, no un riesgo: esa
      base se excluye de las tiras del gráfico, igual que hace <code>cruce.py</code>.</p>`;

  $('#btn-llevar').onclick = () => {
    verVista('diseno');
    correrDiseno();
  };
}

// ---------------------------------------------------------------- rangos

async function cargarRangos() {
  const { rangos } = await pedir('/api/rangos');
  if (!rangos.length) {
    $('#salida-rangos').innerHTML = '<div class="vacio">Todavía no guardaste ninguno. '
      + 'Corré un análisis, arrastrá sobre el gráfico y apretá <b>Guardar este rango</b>.</div>';
    return;
  }
  $('#salida-rangos').innerHTML = `
    <div class="tabla-marco"><table>
      <thead><tr><th>Nombre</th><th>Gen</th><th class="n">Rango</th><th class="n">nt</th>
      <th class="n">eficientes</th><th class="n">off perf.</th><th class="n">1 desaj.</th>
      <th>Configuración</th><th>Guardado</th><th></th></tr></thead>
      <tbody>${rangos.map((x) => `<tr>
        <td><b>${esc(x.nombre || '')}</b></td>
        <td>${esc(x.gen || '')}</td>
        <td class="n">${x.inicio}–${x.fin}</td>
        <td class="n">${num(x.largo || 0)}</td>
        <td class="n">${x.eficientes ?? '—'}</td>
        <td class="n">${x.off_perfecto ?? '<span class="no">sin medir</span>'}</td>
        <td class="n">${x.off_mm1 ?? '<span class="no">sin medir</span>'}</td>
        <td><span class="nota">${esc(x.etiqueta || '')}<br><code>${esc(x.config || '')}</code></span></td>
        <td><span class="nota">${esc(x.creado || '')}</span></td>
        <td><button class="boton-2" data-borrar="${esc(x.id)}">borrar</button></td>
      </tr>`).join('')}</tbody></table></div>
    <p class="nota">Un conteo sin su modo y su motor no significa nada: los mismos cuatro
      genes dan cuatro números distintos según cuál de los dos RNAplfold corrió. Por eso cada
      rango guarda su configuración.</p>`;

  $$('[data-borrar]').forEach((b) => {
    b.onclick = async () => {
      await pedir('/api/rangos/' + b.dataset.borrar, null, 'DELETE');
      cargarRangos();
    };
  });
}

// ---------------------------------------------------------------- arranque

function verVista(cual) {
  for (const v of ['diseno', 'off', 'rangos']) {
    $('#vista-' + v).hidden = (v !== cual);
    $('#tab-' + v).setAttribute('aria-selected', String(v === cual));
  }
  if (cual === 'rangos') cargarRangos();
  if (cual === 'off') {
    const pares = $('#secuencia').value.trim();
    $('#off-consulta').innerHTML = pares
      ? 'Usa la secuencia de la pestaña <b>Diseño</b>.'
      : 'Primero pegá una secuencia en la pestaña <b>Diseño</b>.';
  }
}

async function iniciar() {
  S.arranque = await pedir('/api/arranque');

  $('#motores').innerHTML = S.arranque.motores.map((m) =>
    `<li class="${m.disponible ? '' : 'falta'}" ${m.disponible ? '' : `title="${esc(m.motivo)}"`}>
      ${m.disponible ? '✓' : '✗'} ${esc(m.nombre)}</li>`).join('')
    + `<li>${S.arranque.bases.length} bases de off-target en disco</li>`;

  $('#backend').innerHTML = S.arranque.motores.map((m) =>
    `<option value="${m.id}" ${m.disponible ? '' : 'disabled'}>${esc(m.nombre)}${m.disponible ? '' : ' — no está'}</option>`).join('');
  const vienna = S.arranque.motores.find((m) => m.id === 'vienna');
  $('#backend').value = (vienna && vienna.disponible) ? 'vienna'
    : (S.arranque.motores.find((m) => m.disponible) || { id: '' }).id;

  $('#ejemplos').innerHTML = '<option value="">— ejemplo —</option>'
    + S.arranque.ejemplos.map((e, i) => `<option value="${i}">${esc(e.nombre)}</option>`).join('');
  $('#ruta-salidas').textContent = S.arranque.salidas;
  pintarBases();
  notaModo();

  // navegacion
  $$('nav button').forEach((b) => { b.onclick = () => verVista(b.dataset.vista); });

  // formularios
  $('#form-diseno').onsubmit = correrDiseno;
  $('#form-off').onsubmit = correrOff;
  $('#modo').onchange = notaModo;

  $('#btn-archivo').onclick = () => $('#archivo').click();
  $('#archivo').onchange = async (ev) => {
    const f = ev.target.files[0];
    if (f) $('#secuencia').value = await f.text();
  };
  $('#ejemplos').onchange = (ev) => {
    const e = S.arranque.ejemplos[parseInt(ev.target.value, 10)];
    if (e) $('#secuencia').value = e.texto;
  };

  // presets del original
  $$('[data-preset]').forEach((b) => {
    b.onclick = () => {
      const p = S.arranque.presets[b.dataset.preset];
      for (const [k, v] of Object.entries(p)) {
        const el = $('#' + k);
        if (!el) continue;
        if (el.type === 'checkbox') el.checked = v; else el.value = v;
      }
      $('#config').value = cadenaConfig();
    };
  });

  // la cadena de configuracion, de ida y de vuelta
  const sincronizar = () => { $('#config').value = cadenaConfig(); };
  ['sirna_size', 'accessibility_window', 'end_stability_threshold',
    'accessibility_threshold', 'strand_check', 'end_check', 'accessibility_check',
    'terminal_check'].forEach((k) => { $('#' + k).onchange = sincronizar; });

  $('#config').onkeydown = async (ev) => {
    if (ev.key !== 'Enter') return;
    ev.preventDefault();
    try {
      const p = await pedir('/api/config', { config: $('#config').value });
      for (const [k, v] of Object.entries(p)) {
        const el = $('#' + k);
        if (!el) continue;
        if (el.type === 'checkbox') el.checked = v; else el.value = v;
      }
      aviso('#aviso-diseno', 'Configuración aplicada.', 'bien');
    } catch (err) {
      aviso('#aviso-diseno', esc(err.message), 'mal');
    }
  };

  $('#btn-panel').onclick = () => $$('.base').forEach((i) => {
    i.checked = S.arranque.bases.find((b) => b.id === i.value).en_panel;
  });
  $('#btn-ninguna').onclick = () => $$('.base').forEach((i) => { i.checked = false; });
}

iniciar().catch((e) => {
  document.body.insertAdjacentHTML('afterbegin',
    `<div class="wrap"><div class="aviso mal">No pude arrancar: ${esc(e.message)}</div></div>`);
});
