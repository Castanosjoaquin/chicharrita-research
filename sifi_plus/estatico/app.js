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

// ------------------------------------------------- las vistas de lectura (V1)
//
// Estas cinco vistas LEEN resultados que otras lineas ya calcularon y versionaron. Ninguna
// calcula un criterio: no hay un solo veredicto de eficiencia, un tamizado ni un puntaje
// decidido en este archivo, y por eso ninguna puede mover un numero del motor.
//
// Las tres reglas que el dibujo tiene que respetar, y que son el contrato de datos:
//   * ningun numero aparece solo: cada uno lleva modo, motor, panel y archivo de origen;
//   * un archivo que falta produce «no corrido», NUNCA un cero;
//   * «sin medir», «no aplica», «declarado faltante» y «cero medido» son cuatro estados
//     distintos y se dibujan distinto. La interfaz ya lo hace en sus tiras; esto lo hereda.

/** La etiqueta de procedencia. Va arriba de los numeros que describe, no al pie. */
function sello(p) {
  if (!p) return '';
  const campo = (k, v) => {
    const falta = String(v).startsWith('procedencia no declarada');
    return `<span class="${falta ? 'no' : ''}"><b>${k}:</b> ${esc(
      Array.isArray(v) ? v.join(', ') : v)}</span>`;
  };
  return `<div class="sello ${p.declarada ? '' : 'sello-falta'}">
    ${campo('modo', p.modo)} ${campo('motor', p.motor)} ${campo('panel', p.panel)}
    <span><b>archivo:</b> <code>${esc(p.archivo)}</code></span>
    ${p.nota ? `<p class="nota">${esc(p.nota)}</p>` : ''}</div>`;
}

/** El bloque «no corrido». Sin una sola cifra al lado: un cero aca seria una afirmacion. */
function noCorrido(d) {
  return `<div class="aviso ojo"><p><b>No corrido.</b> Falta
    <code>${esc(d.archivo)}</code> (${esc(d.motivo || 'no esta en disco')}).</p>
    ${d.comando ? `<p class="nota">Se genera con: <code>${esc(d.comando)}</code></p>` : ''}
    <p class="nota">Esto no es un cero. Un cero significaria que se miro y no hay nada; acá
      no se miró.</p></div>`;
}

/** Una contradiccion entre dos archivos se anota con las dos cifras y las dos rutas. */
function contradicciones(lista) {
  if (!lista || !lista.length) return '';
  return `<div class="aviso mal"><p><b>Dos archivos de la misma corrida no coinciden.</b>
    No se corrige ninguno de los dos: van las dos cifras con sus dos rutas.</p>
    <ul class="nota">${lista.map((c) => `<li>${esc(c.quimera || c.clave || '')} —
      ${esc(c.que)}: ${c.en_el_detalle ?? c.por_ventana} contra
      ${c.en_el_resumen ?? c.por_region}</li>`).join('')}</ul></div>`;
}

// --- Vista A: mover la region ---

async function cargarInventarioRegiones() {
  const d = await pedir('/api/vista/regiones');
  if (d.estado !== 'listo') { $('#salida-regionv').innerHTML = noCorrido(d); return; }
  const op = d.regiones.map((r) =>
    `<option value="${esc(r.clave)}">${esc(r.gen)} ${esc(r.region)}</option>`).join('');
  $('#par-a').innerHTML = op;
  $('#par-b').innerHTML = op;
  // El par de BicC es el caso que motiva la vista, asi que arranca ahi; cualquier otro par
  // del directorio se elige en los desplegables.
  if (d.regiones.some((r) => r.clave === 'BicC_Dm_264-563')) $('#par-a').value = 'BicC_Dm_264-563';
  if (d.regiones.some((r) => r.clave === 'BicC_Dm_922-1221')) $('#par-b').value = 'BicC_Dm_922-1221';
  verRegiones();
}

/** El eje compartido con una tira por organismo x criterio, y una marca por tramo. */
function dibujarPanelRegion(p, eje) {
  if (p.estado !== 'listo') return noCorrido(p);
  const W = 860, ML = 128, MR = 14, H_TIRA = 13, GAP = 6;
  const n = Math.max(1, eje.hasta - eje.desde);
  const x = (pos) => ML + (pos - eje.desde) * (W - ML - MR) / n;
  const alto = 26 + p.marcas.length * (H_TIRA + GAP) + 24;

  const regionIni = p.inicio, regionFin = p.fin;
  const tiras = p.marcas.map((m, i) => {
    const y = 26 + i * (H_TIRA + GAP);
    const clase = m.criterio === 'perfecto_21' ? 'tick-off' : 'tick-mm1';
    const marcas = m.tramos.map(([a, b]) =>
      `<rect class="${clase}" x="${x(a).toFixed(1)}" y="${y}"
         width="${Math.max(2, x(b) - x(a) + 2).toFixed(1)}" height="${H_TIRA}">
         <title>${esc(m.organismo_corto)} · ${esc(m.criterio)} · ${a}–${b}</title></rect>`).join('');
    return `<rect class="lane" x="${ML}" y="${y}" width="${W - ML - MR}" height="${H_TIRA}"/>
      ${marcas}
      <text class="lane-lab" x="${ML - 6}" y="${y + H_TIRA - 3}" text-anchor="end">${
        esc(m.organismo_corto)} · ${m.criterio === 'perfecto_21' ? '21/21' : '≥19'}</text>`;
  }).join('');

  const sinAlertas = !p.marcas.length
    ? `<text class="lane-lab" x="${ML}" y="40">se tamizó y no hay ninguna ventana con alerta
        en esta región — cero medido, no «sin medir»</text>` : '';

  return `<figure>
    <figcaption><b>${esc(p.gen)} ${esc(p.region)}</b> — ${esc(p.que_es || '')}
      ${p.vigente === 'sí' ? '<span class="si">· vigente</span>' : '<span class="no">· no vigente</span>'}
      <br>${p.n_filas} fila(s) de alerta · ${p.posiciones_distintas} posición(es) con alerta
      · <code>${esc(p.archivo_region)}</code></figcaption>
    <svg class="plot" viewBox="0 0 ${W} ${alto}" role="img">
      <rect class="band" x="${x(regionIni).toFixed(1)}" y="14"
        width="${(x(regionFin) - x(regionIni)).toFixed(1)}" height="${alto - 38}"/>
      <text class="band-lab" x="${((x(regionIni) + x(regionFin)) / 2).toFixed(1)}" y="11">${
        regionIni}–${regionFin}</text>
      ${tiras}${sinAlertas}
      <line class="axis" x1="${ML}" y1="${alto - 20}" x2="${W - MR}" y2="${alto - 20}"/>
      <text class="tick" x="${ML}" y="${alto - 7}">${eje.desde}</text>
      <text class="tick" x="${W - MR}" y="${alto - 7}" text-anchor="end">${eje.hasta}</text>
    </svg>
  </figure>
  <div class="tabla-marco"><table>
    <thead><tr><th>Organismo</th><th>Gen impactado</th><th class="n">21/21</th>
      <th class="n">≥19 nt</th><th class="n">21/21 eficientes</th><th>Evidencia</th>
      <th>Firma</th></tr></thead>
    <tbody>${p.filas.map((f) => `<tr>
      <td title="${esc(f.organismo_rol || '')}">${esc(f.organismo_corto)}</td>
      <td>${esc(f.gen_simbolo || '—')}<br><span class="nota">${esc(f.gen_locus || '')}</span></td>
      <td class="n">${f.ventanas_perfecto_21 ?? '<span class="no">sin medir</span>'}</td>
      <td class="n">${f.ventanas_perfecto_ge19 ?? '<span class="no">sin medir</span>'}</td>
      <td class="n">${f.ventanas_21_eficientes.valor ?? '—'}
        <span class="no" title="${esc(f.ventanas_21_eficientes.procedencia)}">⚠</span></td>
      <td><span class="nota">${esc(f.evidencia_clave || '')}</span></td>
      <td>${esc(f.decision_usuario || '')}</td>
    </tr>`).join('')}</tbody></table></div>`;
}

async function verRegiones() {
  const a = $('#par-a').value, b = $('#par-b').value;
  if (!a || !b) return;
  aviso('#aviso-regionv', '');
  const d = await pedir(`/api/vista/region?a=${encodeURIComponent(a)}&b=${encodeURIComponent(b)}`);
  if (d.estado !== 'listo') { $('#salida-regionv').innerHTML = noCorrido(d); return; }
  if (d.aviso) aviso('#aviso-regionv', esc(d.aviso), 'ojo');
  $('#salida-regionv').innerHTML = sello(d.procedencia)
    + contradicciones(d.paneles.flatMap((p) => p.contradicciones || []))
    + `<p class="nota">El eje va de ${d.eje ? d.eje.desde : '—'} a ${d.eje ? d.eje.hasta : '—'}:
        ${esc(d.eje ? d.eje.que_es : '')}.</p>`
    + d.paneles.map((p) => dibujarPanelRegion(p, d.eje || { desde: 1, hasta: 2 })).join('')
    + `<p class="nota"><b>${esc(d.organismos_nota)}</b> En estas dos regiones:
        ${d.organismos_con_alerta.map(esc).join(', ') || '—'}.</p>`;
}

// --- Vista B: los tres marcos ---

async function verMarcos() {
  const d = await pedir('/api/vista/marcos');
  if (d.estado !== 'listo') { $('#salida-marcos').innerHTML = noCorrido(d); return; }
  const tarjeta = (r) => `<figure>
    <figcaption><b>${esc(r.gen)} ${r.inicio}–${r.fin}</b> · ${r.largo} nt ·
      ${esc(r.nota || '')}</figcaption>
    <ul class="kpis">${r.cifras.map((c) => `<li ${c.destacado ? 'class="kpi-dest"' : ''}>
      <span class="n">${c.valor ?? '<span class="no">sin medir</span>'}</span>
      <span class="k">marco ${c.marco}${c.destacado ? ' — la molécula que existiría' : ''}</span>
      <span class="nota">${esc(c.pregunta)}</span></li>`).join('')}</ul>
    <p class="nota">Diferencias que el archivo trae, no calculadas acá: límite físico
      ${r.derivadas.limite_fisico ?? '—'}, contexto neto ${r.derivadas.contexto_neto ?? '—'},
      pierden ${r.derivadas.pierden ?? '—'}, ganan ${r.derivadas.ganan ?? '—'}.</p>
  </figure>`;
  $('#salida-marcos').innerHTML = sello(d.procedencia)
    + (d.configuracion_declarada ? '' : `<div class="aviso ojo"><p><b>Procedencia no
        declarada.</b> Falta <code>${esc(d.archivo_configuracion)}</code>, que es el único
        archivo que dice con qué modo y qué motor se contaron estas cifras.</p></div>`)
    + `<p class="nota">${esc(d.texto)}</p>` + d.regiones.map(tarjeta).join('');
}

// --- Vista C: la juntura ---

async function verJuntura() {
  const d = await pedir('/api/vista/juntura');
  if (d.estado !== 'listo') { $('#salida-juntura').innerHTML = noCorrido(d); return; }

  const dibujo = (o) => {
    const W = 860, ML = 14, MR = 14, Y = 34, ALTO = 30;
    const total = (o.resumen.ventanas_de_juntura || 20) + 40;
    const centro = ML + (W - ML - MR) / 2;
    const esc_x = (nt) => centro + nt * (W - ML - MR) / (2 * total / 2) / 2;
    const bloques = o.bloques.map((b) => {
      const ini = (b.offset || 0) + ((b.j || 1) - 1) - 10;
      const x1 = esc_x(ini), x2 = esc_x(ini + 1.0);
      return `<rect class="${b.fabricado ? 'bl-fab' : 'bl-her'}" x="${x1.toFixed(1)}"
        y="${Y + (b.fabricado ? 0 : ALTO + 6)}" width="${Math.max(6, x2 - x1).toFixed(1)}"
        height="${ALTO}"><title>j=${b.j} · ${b.largo} nt · ${b.nt_de_izquierda} nt de
        ${esc(o.izquierda)} + ${b.nt_de_derecha} nt de ${esc(o.derecha)} ·
        ${b.fabricado ? 'FABRICADO por el empalme' : 'heredado'} ·
        aciertos: ${esc(b.organismos.join(', ') || 'ninguno')}</title></rect>`;
    }).join('');
    return `<svg class="plot" viewBox="0 0 ${W} ${Y + 2 * ALTO + 34}" role="img">
      <line class="cross" x1="${centro}" y1="${Y - 8}" x2="${centro}" y2="${Y + 2 * ALTO + 12}"/>
      <text class="band-lab" x="${centro}" y="${Y - 12}">la unión</text>
      <text class="lane-lab" x="${ML}" y="${Y + ALTO - 10}">fabricados</text>
      <text class="lane-lab" x="${ML}" y="${Y + 2 * ALTO - 4}">heredados</text>
      ${bloques}
      <text class="tick" x="${ML}" y="${Y + 2 * ALTO + 28}">← ${esc(o.izquierda)}</text>
      <text class="tick" x="${W - MR}" y="${Y + 2 * ALTO + 28}" text-anchor="end">${
        esc(o.derecha)} →</text>
    </svg>`;
  };

  const orden = (o) => `<figure>
    <figcaption><b>${esc(o.quimera)}</b> — ${esc(o.izquierda)} + ${esc(o.derecha)},
      corte en ${o.corte_nt ?? '—'} nt</figcaption>
    ${dibujo(o)}
    <ul class="kpis">
      <li><span class="n">${o.heredados}</span><span class="k">bloques heredados con acierto</span></li>
      <li class="${o.fabricados ? 'kpi-mal' : ''}"><span class="n">${o.fabricados}</span>
        <span class="k">bloques fabricados por el empalme</span></li>
      <li><span class="n">${o.resumen.juntura_eficientes ?? '<span class="no">sin medir</span>'}</span>
        <span class="k">ventanas eficientes de juntura</span></li>
      <li><span class="n">${o.resumen.juntura_con_blanco_continuo_21nt ?? '—'}</span>
        <span class="k">con blanco continuo de 21 nt</span></li>
    </ul>
    <p class="nota">Referencias contra las que el empalme fabrica riesgo:
      <b>${o.referencias_fabricadas.map(esc).join(', ') || 'ninguna'}</b>.</p>
    ${o.cambiadas.length ? `<div class="tabla-marco"><table>
      <thead><tr><th class="n">Posición</th><th>Lado</th><th>Antes</th><th>Ahora</th>
        <th class="n">nt hasta la unión</th></tr></thead>
      <tbody>${o.cambiadas.map((c) => `<tr><td class="n">${c.pos_quimera}</td>
        <td>${esc(c.lado)}</td><td>${esc(c.antes)}</td><td>${esc(c.ahora)}</td>
        <td class="n">${c.nt_hasta_la_union}</td></tr>`).join('')}</tbody></table></div>
      <p class="nota">Ventanas heredadas que cambiaron de veredicto, con su distancia a la
        unión.</p>` : '<p class="nota">Ninguna ventana heredada cambió de veredicto.</p>'}
  </figure>`;

  const c = d.cobertura_de_bloques;
  $('#salida-juntura').innerHTML = sello(d.procedencia) + contradicciones(d.contradicciones)
    + `<div class="aviso ojo"><p><b>El dibujo muestra ${c.en_el_archivo} bloques de los
        ${c.publicados} que la juntura enumera.</b> ${esc(c.nota)}</p>
      <p class="nota">Los ${c.no_medidos ?? '—'} restantes se dibujan como <b>no medidos</b>:
        ni heredados ni sin acierto. Deducir su geometría sería calcular, y esta vista lee.</p>
      <p class="nota">${esc(c.contradiccion_publicada)}</p></div>`
    + d.ordenes.map(orden).join('');
}

// --- Vista E: los dos ejes ---

async function verEjes() {
  const d = await pedir('/api/vista/ejes');
  if (d.estado !== 'listo') { $('#salida-ejes').innerHTML = noCorrido(d); return; }
  const pct = (v) => (v === null || v === undefined ? '—' : (v * 100).toFixed(2) + ' %');
  const bloque = (regla) => `<h3>Regla ${esc(regla)}</h3>
    <div class="tabla-marco"><table>
      <thead><tr><th>Objeto</th><th>Clase</th><th class="n">nt</th><th class="n">ventanas</th>
        <th class="n">eficientes</th><th class="n">eficacia</th><th class="n">limpieza</th>
        <th class="n">con off-target</th><th class="n">21/21</th><th>vetada</th></tr></thead>
      <tbody>${d.objetos.filter((o) => o.regla === regla).map((o) => `<tr>
        <td><b>${esc(o.objeto)}</b></td><td>${esc(o.clase)}</td>
        <td class="n">${num(o.largo_nt || 0)}</td><td class="n">${num(o.n_ventanas || 0)}</td>
        <td class="n">${o.eficientes ?? '<span class="no">sin medir</span>'}</td>
        <td class="n">${pct(o.eficacia)}</td>
        <td class="n">${pct(o.limpieza.valor)} <span class="no"
          title="${esc(o.limpieza.procedencia)}">⚠</span></td>
        <td class="n">${o.con_off_target.valor ?? '—'} <span class="no"
          title="${esc(o.con_off_target.procedencia)}">⚠</span></td>
        <td class="n">${o.con_21_perfecto.valor ?? esc(String(o.con_21_perfecto.valor))}</td>
        <td>${esc(o.vetada)}</td></tr>`).join('')}</tbody></table></div>`;
  $('#salida-ejes').innerHTML = sello(d.procedencia)
    + `<div class="aviso ojo"><p>Las columnas
        <b>${d.columnas_sin_panel.map(esc).join(', ')}</b> dependen del panel de referencias, y
        ningún archivo de esta corrida lo declara: van marcadas con ⚠ y
        «procedencia no declarada».</p></div>`
    + `<p class="nota">${esc(d.texto)}</p>` + d.reglas.map(bloque).join('');
}

// --- Vista F: el enumerador de quimeras (V2) ---
//
// El orden de la tabla es el del archivo y la columna «#» lo dice: es el puesto en el archivo,
// no la posicion en lo que quedo despues de filtrar. Por eso al filtrar los numeros salen
// salteados —11, 13, 19— y eso es correcto: el filtro recorta, no reordena.

const Q = { objetivos: null, datos: null };

async function cargarObjetivos() {
  const d = await pedir('/api/vista/quimeras/objetivos');
  $('#q-objetivo').innerHTML = d.objetivos.map((o) =>
    `<option value="${esc(o.objetivo)}" ${o.en_disco ? '' : 'disabled'}>${esc(o.titulo)}${
      o.en_disco ? '' : ' — no está'}</option>`).join('');
  Q.objetivos = d.objetivos;
  await verQuimeras(true);
}

async function verQuimeras(primera) {
  const p = new URLSearchParams({
    objetivo: $('#q-objetivo').value,
    cuantas: '50',
    izquierda: $('#q-izq').value || '',
    derecha: $('#q-der').value || '',
    l1: $('#q-l1').value || '',
    alerta: $('#q-alerta').checked ? '1' : '',
  });
  const d = await pedir('/api/vista/quimeras?' + p.toString());
  if (d.estado !== 'listo') { $('#salida-quimeras').innerHTML = noCorrido(d); return; }
  Q.datos = d;

  if (primera) {
    const op = (vals) => '<option value="">— todos —</option>'
      + vals.map((v) => `<option value="${esc(v)}">${esc(v)}</option>`).join('');
    $('#q-izq').innerHTML = op(d.izquierdas);
    $('#q-der').innerHTML = op(d.derechas);
    $('#q-l1').innerHTML = op(d.l1_posibles.map(String));
  }

  const g = d.grilla;
  const obj = (Q.objetivos || []).find((o) => o.objetivo === d.objetivo) || {};

  $('#salida-quimeras').innerHTML = sello(d.procedencia)
    // La advertencia del archivo, ARRIBA de la tabla. Califica todas las columnas de
    // eficiencia: una tabla ordenada por eficiencia invita a leer el primer puesto como una
    // recomendacion, y no lo es.
    + (d.advertencia ? `<div class="aviso mal"><p><b>Lo que el archivo advierte sobre estas
        cifras:</b> ${esc(d.advertencia)}</p>
      <p class="nota">Califica todas las columnas de eficiencia de esta tabla. El primer puesto
        de un objetivo <b>no es una recomendación</b>.</p></div>` : '')
    + `<p class="nota"><b>${esc(obj.titulo || d.titulo)}</b> — ${esc(d.pregunta)}.</p>
      <ul class="kpis">
        <li><span class="n">${num(g.combinaciones_antes_de_podar || 0)}</span>
          <span class="k">combinaciones que recorre la grilla</span></li>
        <li class="kpi-dest"><span class="n">${num(g.combinaciones_admisibles || 0)}</span>
          <span class="k">admisibles, que son las que están en el archivo</span></li>
        <li><span class="n">${num(d.plegados || 0)}</span><span class="k">plegados que costó</span></li>
        <li class="${d.con_alerta_de_juntura_nueva ? 'kpi-mal' : ''}">
          <span class="n">${num(d.con_alerta_de_juntura_nueva)}</span>
          <span class="k">con alerta que fabrica el empalme</span></li>
      </ul>
      <p class="nota">Grilla de paso ${g.paso}, fragmento izquierdo de ${g.l1_min} a ${g.l1_max} nt,
        largo total ${g.largo_total} nt. <b>El orden es el del archivo:</b> ${esc(d.orden)}</p>
      <p class="nota">Mostrando ${d.filas.length} de ${num(d.total_filtrado)}${
        d.total_filtrado !== d.total_en_el_archivo
          ? ` filtradas (de ${num(d.total_en_el_archivo)} en el archivo)` : ''}.</p>`
    + `<div class="tabla-marco"><table>
      <thead><tr><th class="n" title="puesto en el archivo, no en lo filtrado">#</th>
        <th>Quimera</th><th class="n">izq</th><th class="n">der</th><th class="n">nt</th>
        <th class="n">ef. sueltas</th><th class="n">ef. heredadas</th><th class="n">Δ vs suma</th>
        <th class="n">cambiaron</th><th class="n">ef. juntura</th><th class="n">fabricados ≥19</th>
        <th>refs fabricadas</th><th>alerta nueva</th><th>en el vector</th></tr></thead>
      <tbody>${d.filas.map((f) => `<tr class="${
        (f.alerta_juntura_nueva || '').trim() === 'si' ? 'fila-alerta' : ''}">
        <td class="n">${f.puesto_en_el_archivo}</td>
        <td><code>${esc(f.quimera)}</code><br><span class="nota">${esc(f.eje_izq)} + ${
          esc(f.eje_der)}</span></td>
        <td class="n">${f.a1}<span class="no">+${f.l1}</span></td>
        <td class="n">${f.a2}<span class="no">+${f.l2}</span></td>
        <td class="n">${num(f.largo_total_nt || 0)}</td>
        <td class="n">${f.ef_fragmento_izq_solo}+${f.ef_fragmento_der_solo}=${f.suma_de_las_partes}</td>
        <td class="n"><b>${f.ef_heredadas}</b></td>
        <td class="n">${f.delta_heredadas_menos_suma > 0 ? '+' : ''}${f.delta_heredadas_menos_suma}</td>
        <td class="n">${f.heredadas_que_cambiaron}</td>
        <td class="n">${f.ef_juntura}</td>
        <td class="n">${f.fabricados_ge19_refs}</td>
        <td>${f.fabricados_refs.map(esc).join(', ') || '<span class="no">ninguna</span>'}</td>
        <td>${(f.alerta_juntura_nueva || '').trim() === 'si'
          ? '<span class="estado-bloqueante">sí</span>' : '<span class="no">no</span>'}</td>
        <td>${esc(f.existe_en_el_genoma_del_vector)}</td>
      </tr>`).join('')}</tbody></table></div>
      <p class="nota">La columna <b>#</b> es el puesto en el archivo. Al filtrar los números
        salen salteados a propósito: el filtro recorta las filas y <b>no las renumera</b>, porque
        renumerar convertiría el filtro en un criterio.</p>
      <div class="aviso ojo"><p><b>Lo que esta vista no muestra.</b> ${esc(d.grilla_fina.nota)}</p>
        <p class="nota">El archivo es <code>${esc(d.grilla_fina.archivo)}</code>${
          d.grilla_fina.en_disco ? ' y está en disco' : ' y no está en disco'}.</p></div>`;
}

// --- Vista G: la transferencia por homologia (V2) ---

async function cargarHomologia() {
  const d = await pedir('/api/vista/homologia?ref=HV');
  if (d.estado !== 'listo') { $('#salida-homologia').innerHTML = noCorrido(d); return; }
  $('#h-ref').innerHTML = d.referencias_disponibles.map((r) =>
    `<option value="${esc(r.id)}">${esc(r.nombre)}</option>`).join('');
  $('#h-ref').value = d.ref;
  pintarHomologia(d);
}

async function verHomologia() {
  const d = await pedir('/api/vista/homologia?ref=' + encodeURIComponent($('#h-ref').value));
  if (d.estado !== 'listo') { $('#salida-homologia').innerHTML = noCorrido(d); return; }
  pintarHomologia(d);
}

function pintarHomologia(d) {
  const c = d.controles.positivo;
  const maxE = Math.max(...(d.embudo || [{ n: 1 }]).map((e) => e.n));

  // El embudo como barras: seis categorias excluyentes que se leen de arriba hacia abajo.
  const embudo = !d.embudo ? '' : `<div class="embudo">${d.embudo.map((e) => `
    <div class="embudo-fila ${e.categoria === 'f_reciproco_con_nombre' ? 'embudo-fin' : ''}">
      <span class="embudo-lab">${esc(e.categoria)}</span>
      <span class="embudo-barra"><i style="width:${(100 * e.n / maxE).toFixed(1)}%"></i></span>
      <span class="embudo-n">${num(e.n)}</span>
      <span class="nota">${esc(e.que_es)}</span>
    </div>`).join('')}</div>`;

  const variante = (v) => `<figure class="${v.es_la_de_cabecera ? 'var-pre' : 'var-post'}">
    <figcaption><b>${esc(v.titulo)}</b>
      <span class="${v.es_la_de_cabecera ? 'estado-aceptada' : 'estado-pendiente'}">${
        esc(v.rotulo)}</span><br><span class="nota">${esc(v.que_es)}</span></figcaption>
    <ul class="kpis">
      <li><span class="n">${num(v.orfs_reciprocos || 0)}</span><span class="k">ORF recíprocos</span></li>
      <li><span class="n">${num(v.con_nombre_informativo || 0)}</span>
        <span class="k">con nombre informativo</span></li>
      <li><span class="n">${num(v.en_banda_ge90_y_cobertura_alta || 0)}</span>
        <span class="k">con nombre, ≥90 % de identidad y cobertura alta</span></li>
    </ul>
    <p class="nota">Por banda de identidad: ${Object.entries(v.por_banda_de_identidad)
      .map(([k, n]) => `${esc(k)} <b>${num(n)}</b>`).join(' · ')}</p>
    <p class="nota">Por cobertura: ${Object.entries(v.por_cobertura)
      .map(([k, n]) => `${esc(k)} <b>${num(n)}</b>`).join(' · ')}</p>
    <p class="nota">Las dos referencias coinciden en el nombre de
      <b>${num(v.contraste_MQ_vs_HV.coinciden || 0)}</b> de
      ${num(v.contraste_MQ_vs_HV.orfs_con_nombre_informativo_en_las_dos || 0)} ORF
      (${esc(String(v.contraste_MQ_vs_HV.pct ?? '—'))} %).</p>
  </figure>`;

  $('#salida-homologia').innerHTML = sello(d.procedencia)
    // Los controles van ARRIBA, junto a la cifra. El positivo no pasa la variante estricta y eso
    // califica la lectura de toda la vista.
    + `<div class="aviso ${c.pasa_estricta === false ? 'mal' : 'bien'}">
        <p><b>Control positivo:</b> <code>${esc(c.orf)}</code> — ${esc(c.esperado)},
          ${esc(String(c.pident))} % de identidad.
          Pasa la estricta: <b>${c.pasa_estricta ? 'sí' : 'NO'}</b>
          (cae en <code>${esc(c.categoria_estricta)}</code>) ·
          pasa la ampliada: <b>${c.pasa_ampliada ? 'sí' : 'no'}</b>.</p>
        <p class="nota">${esc(c.lectura)}</p></div>
      <div class="aviso bien"><p><b>Señuelo:</b> ${Object.entries(d.controles.senuelo.por_referencia)
        .map(([k, v]) => `${esc(k)} ${v.con_hit}/${num(v.consultas)}`).join(' · ')} con hit.</p>
        <p class="nota">${esc(d.controles.senuelo.lectura)}</p></div>
      <p class="nota"><b>${esc(d.referencia_nombre)}</b> · ${num(d.contigs || 0)} contigs,
        ${num(d.orfs || 0)} ORF, ${num(d.total_filas_del_detalle || 0)} filas de detalle ·
        ${esc(d.diamond)} · ${Object.entries(d.parametros || {})
          .map(([k, v]) => `${esc(k)} ${esc(String(v))}`).join(', ')}</p>
      <h3>El embudo: de contig a nombre de gen</h3>${embudo}
      <h3>Las dos variantes</h3>
      <div class="aviso ojo"><p><b>${esc(d.nota_de_las_variantes)}</b></p></div>
      <div class="dos-col">${d.variantes.map(variante).join('')}</div>
      <h3>El detalle por ORF</h3>
      <div class="fila" style="max-width:860px">
        <div><label for="h-cat">Categoría</label><select id="h-cat">${
          d.embudo.map((e) => `<option value="${esc(e.categoria)}" ${
            e.categoria === 'f_reciproco_con_nombre' ? 'selected' : ''}>${esc(e.categoria)} — ${
            num(e.n)}</option>`).join('')}</select></div>
        <div><label for="h-busca">Buscar en el producto o el contig</label>
          <input type="text" id="h-busca" placeholder="p. ej. bicaudal"></div>
      </div>
      <div id="salida-h-detalle"></div>
      <p class="nota">Un resultado que su propio autor declaró no leíble no se muestra como
        resultado: <code>${esc(d.descartado.archivo)}</code> — ${esc(d.descartado.estado)}</p>`;

  $('#h-cat').onchange = verDetalleHomologia;
  $('#h-busca').oninput = () => {
    clearTimeout(window._tH);
    window._tH = setTimeout(verDetalleHomologia, 300);
  };
  verDetalleHomologia();
}

async function verDetalleHomologia() {
  const p = new URLSearchParams({
    ref: $('#h-ref').value, categoria: $('#h-cat').value,
    contiene: $('#h-busca').value || '', cuantas: '50',
  });
  const d = await pedir('/api/vista/homologia/detalle?' + p.toString());
  if (d.estado !== 'listo') { $('#salida-h-detalle').innerHTML = noCorrido(d); return; }
  if (!d.filas.length) {
    $('#salida-h-detalle').innerHTML = '<div class="vacio">Ninguna fila con ese filtro.</div>';
    return;
  }
  $('#salida-h-detalle').innerHTML = `
    <p class="nota">${esc(d.que_es)}. Mostrando ${d.filas.length} de ${num(d.total)}
      (${num(d.total_del_archivo)} filas en el archivo, que no se vuelcan enteras).</p>
    <div class="tabla-marco"><table>
      <thead><tr><th>Contig</th><th class="n">aa</th><th class="n">ORF</th>
        <th>Producto de la referencia</th><th>Nombre normalizado</th><th class="n">identidad</th>
        <th class="n">cobertura</th><th>banda</th></tr></thead>
      <tbody>${d.filas.map((f) => `<tr>
        <td><code>${esc(f.contig)}</code></td>
        <td class="n">${f.orf_aa ?? '—'}</td>
        <td class="n">${f.orf_ini ?? '—'}–${f.orf_fin ?? '—'} ${esc(f.orf_hebra)}</td>
        <td>${esc(f.ref_producto || '—')}</td>
        <td>${esc(f.nombre_normalizado || '—')}</td>
        <td class="n">${esc(f.pident || '—')}</td>
        <td class="n">${esc(f.cob_orf || '—')} <span class="nota">${esc(f.rotulo_cobertura || '')}</span></td>
        <td>${esc(f.banda_identidad || '—')}</td>
      </tr>`).join('')}</tbody></table></div>`;
}

// --- Vista D: la bandeja de firmas, la unica que escribe ---

function fichaDeFirma(f) {
  const campo = (titulo, cols) => `<dt>${esc(titulo)}</dt><dd>${
    Object.entries(cols).map(([k, v]) => `<span class="nota"><b>${esc(k)}:</b> ${
      esc(v || '—')}</span>`).join('<br>')}</dd>`;
  const d = f.destraba;
  return `<details class="ficha" data-clave="${esc(f.clave)}">
    <summary><b>${esc(f.gen)} ${esc(f.region)}</b> · ${esc(f.organismo_corto)} ·
      ${esc(f.campos.gen_involucrado.gen_locus || '')}
      <span class="etq">21/21: ${f.conteos.ventanas_perfecto_21 ?? 'sin medir'} ·
        ≥19: ${f.conteos.ventanas_perfecto_ge19 ?? 'sin medir'}</span>
      <span class="estado-${esc(f.decision_usuario)}">${esc(f.decision_usuario)}</span></summary>

    <p class="nota"><b>Qué destraba esta firma.</b> ${esc(d.region)} —
      ${esc(d.que_es || '')} (vigente: ${esc(d.vigente || '—')}).
      Estado D48: ${esc(d.estado_D48 || '—')}. Decide: ${esc(d.decide || '—')}.<br>
      <b>${esc(d.nota)}</b></p>

    <dl class="campos">
      ${campo('1 · Organismo', f.campos.organismo)}
      ${campo('2 · Exposición', f.campos.exposicion)}
      ${campo('3 · Gen involucrado', f.campos.gen_involucrado)}
      ${campo('4 · Evidencia biológica', f.campos.evidencia_biologica)}
    </dl>

    ${f.firma ? `<p class="nota">Firmada por <b>${esc(f.firma.firmado_por)}</b> el
      ${esc(f.firma.fecha)} — huella 21/21 ${esc(f.firma.huella_21)}, ≥19
      ${esc(f.firma.huella_ge19)}.</p>` : ''}
    ${f.justificacion_usuario ? `<p class="nota"><b>Justificación en el inventario:</b>
      ${esc(f.justificacion_usuario)}</p>` : ''}

    <form class="form-firma">
      <div class="fila">
        <div><label>Decisión</label><select class="f-decision">
          <option value="aceptada">aceptada</option>
          <option value="bloqueante">bloqueante</option></select></div>
        <div><label>Firmado por</label><input type="text" class="f-autor"
          placeholder="quién firma"></div>
      </div>
      <label>Justificación — un párrafo que cite la fila (el LOC o una accesión)</label>
      <textarea class="f-just" rows="4"
        placeholder="D48 pide un párrafo, no un clic. Mínimo 40 caracteres, y tiene que nombrar ${
          esc(f.campos.gen_involucrado.gen_locus || 'el LOC')} o una de las accesiones."></textarea>
      <button type="submit" class="boton">Escribir la firma</button>
      <p class="nota">Se escribe en el archivo de firmas, con fecha y autor. El inventario
        <b>no</b> se edita acá: se regenera desde el archivo de firmas.</p>
    </form>
  </details>`;
}

async function verFirmas() {
  const d = await pedir('/api/vista/firmas');
  if (d.estado !== 'listo') { $('#salida-firmas').innerHTML = noCorrido(d); return; }

  const grupo = (estado) => {
    const filas = d.filas.filter((f) => f.decision_usuario === estado);
    if (!filas.length) return '';
    return `<h3>${esc(estado)} — ${filas.length}</h3>${filas.map(fichaDeFirma).join('')}`;
  };

  $('#salida-firmas').innerHTML = sello(d.procedencia)
    + `<ul class="kpis">
        <li><span class="n">${d.cuenta.pendiente || 0}</span><span class="k">pendientes</span></li>
        <li><span class="n">${d.cuenta.aceptada || 0}</span><span class="k">aceptadas</span></li>
        <li><span class="n">${d.cuenta.bloqueante || 0}</span><span class="k">bloqueantes</span></li>
        <li><span class="n">${d.total}</span><span class="k">filas en el inventario</span></li>
      </ul>
      <div class="aviso ojo"><p><b>${esc(d.nota_del_umbral)}</b></p>
        <p class="nota">Presentar las pendientes como regiones trabadas sería inventar una
          urgencia que la medición no respalda.</p></div>
      <p class="nota">${esc(d.regla)}</p>`
    + ['pendiente', 'bloqueante', 'aceptada'].map(grupo).join('');

  $$('#salida-firmas .form-firma').forEach((form) => {
    form.onsubmit = async (ev) => {
      ev.preventDefault();
      const ficha = form.closest('.ficha');
      try {
        const r = await pedir('/api/vista/firmar', {
          clave: ficha.dataset.clave,
          decision: $('.f-decision', form).value,
          justificacion: $('.f-just', form).value,
          firmado_por: $('.f-autor', form).value,
        });
        aviso('#aviso-firmas', `Firma escrita en <code>${esc(r.archivo)}</code>
          (${r.firmas} firmas). ${esc(r.siguiente_paso)}`, 'bien');
        verFirmas();
      } catch (err) {
        aviso('#aviso-firmas', `<b>La firma no se escribió.</b> ${esc(err.message)}`, 'mal');
      }
    };
  });
}

// ---------------------------------------------------------------- arranque

function verVista(cual) {
  for (const v of ['diseno', 'off', 'rangos', 'regionv', 'marcos', 'juntura', 'ejes',
    'quimeras', 'homologia', 'firmas']) {
    $('#vista-' + v).hidden = (v !== cual);
    $('#tab-' + v).setAttribute('aria-selected', String(v === cual));
  }
  if (cual === 'rangos') cargarRangos();
  // Las vistas de lectura se cargan al entrar y no al arrancar: leen archivos de `research/`
  // que pueden no estar, y un «no corrido» en una pestana que nadie abrio seria ruido.
  const carga = {
    regionv: cargarInventarioRegiones, marcos: verMarcos, juntura: verJuntura,
    ejes: verEjes, firmas: verFirmas,
    quimeras: () => (Q.objetivos ? verQuimeras(false) : cargarObjetivos()),
    homologia: cargarHomologia,
  }[cual];
  if (carga) {
    carga().catch((e) => {
      $('#salida-' + cual).innerHTML = `<div class="aviso mal">No pude leer la vista: ${
        esc(e.message)}</div>`;
    });
  }
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

  // Vista A: cambiar cualquiera de los dos desplegables redibuja el par.
  $('#par-a').onchange = () => verRegiones();
  $('#par-b').onchange = () => verRegiones();

  // Vista F: el objetivo y los tres filtros. Cambiar el objetivo cambia el ORDEN, que es el
  // criterio; los otros tres solo recortan.
  $('#q-objetivo').onchange = () => verQuimeras(false);
  ['#q-izq', '#q-der', '#q-l1'].forEach((s) => { $(s).onchange = () => verQuimeras(false); });
  $('#q-alerta').onchange = () => verQuimeras(false);

  // Vista G: la referencia.
  $('#h-ref').onchange = () => verHomologia();

  $('#btn-panel').onclick = () => $$('.base').forEach((i) => {
    i.checked = S.arranque.bases.find((b) => b.id === i.value).en_panel;
  });
  $('#btn-ninguna').onclick = () => $$('.base').forEach((i) => { i.checked = false; });
}

iniciar().catch((e) => {
  document.body.insertAdjacentHTML('afterbegin',
    `<div class="wrap"><div class="aviso mal">No pude arrancar: ${esc(e.message)}</div></div>`);
});
