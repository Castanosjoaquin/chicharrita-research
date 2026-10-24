"""Genera estado.html: que esta hecho, que falta y que decisiones estan abiertas.

Por que es un script y no HTML escrito a mano: el estado del entregable ya se
declara en tres lugares de PLAN_DESARROLLO.md (la tabla de los cinco pedidos, la
cobertura de §1 bis y el cuerpo de T1 a T6). Una cuarta copia a mano se
desincroniza sola. Esta pagina NO es fuente de verdad: enlaza a la que lo es, y
verifica contra el disco que cada entregable que nombra existe de verdad.

Uso (desde la raiz del repositorio):
    python tools/generar_estado.py
"""
import html
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CSS = re.search(r"<style>(.*?)</style>",
                (RAIZ / "index.html").read_text(encoding="utf-8"), re.S).group(1)


def existe(rel):
    return (RAIZ / rel).exists()


# ---------------------------------------------------------------- contenido
# (titulo, descripcion, [rutas que respaldan la afirmacion])
HECHO = [
    ("Pedido 1 · Entender si-Fi21",
     "El port verificado contra el original, el método del artículo con la fuente de cada umbral, "
     "y la nota de método que explica que «eficiente» es un booleano por ventana de 21 nt y no un puntaje.",
     ["entregables/que-significa-eficiente.md", "research/ola3/C1_sifi21_paper_metodo", "tools/sifi21_port"]),
    ("Pedido 2 · Benchmarking de las tres herramientas",
     "si-Fi21, dsRNA-Engineer y BLAST sobre los cuatro genes, en un eje común y con el panel de "
     "referencias verificado como idéntico entre las tres.",
     ["research/ola2/W7_ranking/benchmark_tres_herramientas.md"]),
    ("Pedido 3 · Ranking con criterio explícito",
     "El orden, las cinco decisiones declaradas, la ficha por candidato y el barrido de 2.000 juegos "
     "de pesos. La segunda versión suma el panel ampliado, dos genes nuevos y los dos largos de ventana.",
     ["research/ola2/W7_ranking/REPORT.md", "research/ola3/C7_ranking_v2/REPORT.md"]),
    ("Pedido 4 · Evaluación de las regiones elegidas",
     "La región dentro de cada gen contra la distribucion de su propio gen, y la conservación entre aislados.",
     ["research/ola3/C8_conservacion"]),
    ("Pedido 5 · Crítica de las herramientas",
     "Cada crítica va con su medición o su línea de código. Lo más fuerte: la accesibilidad del sitio "
     "blanco es una de las tres condiciones de si-Fi21 y es la que no mostró valor predictivo sobre la "
     "eficacia medida.",
     ["entregables/critica-herramientas.md"]),
    ("C9 · Tarea 1 · Sensibilidad del umbral, sin etiquetas",
     "Barrido de los dos umbrales sin fuente primaria sobre 546 puntos por modo (4.368 filas). "
     "El candidato superior aguanta; la región exacta de 200 nt no. Mide fragilidad de la "
     "recomendación, no calidad del umbral.",
     ["research/ola3/C9_sensibilidad_umbral/REPORT.md",
      "research/ola3/C9_sensibilidad_umbral/resultados/grilla_umbral.tsv"]),
    ("C9 · Tarea 1 bis · El mismo barrido, sobre la región que proponemos",
     "El barrido anterior elegía en cada punto la ventana libre de 200 nt, que no es la regla con "
     "la que se eligieron las regiones del entregable. Repetido sobre la región propuesta y con el "
     "veto aplicado, a 21 y 22 nt y sobre los seis candidatos: el candidato superior sale más "
     "robusto, y el empate del tercer puesto se deshace y aparece en otros pares.",
     ["research/ola3/C9_sensibilidad_umbral/REPORT.md",
      "research/ola3/C9_sensibilidad_umbral/resultados/grilla_region_propuesta.tsv"]),
    ("C9 · Tarea 2 · Corregida la lectura del barrido de pesos",
     "La diagonal de B.3 mide la escala, no la robustez del orden. La afirmación vieja queda dicha y "
     "tachada, con la nueva y su fuente al lado, en W7 y en el ranking v2.",
     ["research/ola2/W7_ranking/REPORT.md", "research/ola3/C7_ranking_v2/REPORT.md"]),
    ("Las cuatro decisiones del checkpoint, formalizadas",
     "D33 a D36: las bacterias salen del alcance del diseño por ARNi, el objetivo es el insecto como "
     "vector, la ventana se fija en 21 y 22 nt por evidencia biológica y el ejercicio sobre los cuatro "
     "candidatos es una auditoría y no la reproducción de un resultado validado.",
     ["00_meta/DECISIONS.md"]),
    ("Validación retrospectiva corrida: no concluyente",
     "Pre-registro con tres enmiendas fechadas y la validación corrida el 2026-10-21. Primario: los 31 "
     "siRNA de <i>Tc-gawky</i>, n = 29, ρ = +0,142 con IC95 [−0,247, +0,492]; confirmatorio sobre los 28 "
     "ARNdc, ρ = +0,236. La curva precisión-recall sólo supera la base de 82,8 % en el umbral más bajo del barrido (0,02: precisión 0,875, con IC95 [0,529, 0,978] que contiene la base), y en el umbral por defecto de 0,1 queda por debajo (0,800). "
     "<b>Un nulo no refuta el puntaje</b>, y eso estaba declarado antes de mirar los datos.",
     ["research/ola3/C9_sensibilidad_umbral/RESULTADOS_validacion_retrospectiva.md",
      "research/ola3/C9_sensibilidad_umbral/PREREGISTRO_validacion_retrospectiva.md"]),
    ("C12 · ¿Cuánto vale la homología como regla?",
     "La concordancia de anotación entre cicadélidos sube de 76 % a 86 % con la identidad y no llega a 100 %. La función de la poliproteína del MRFV se transfiere a 11 de 11 marafivirus y la de la proteína de movimiento a 2 de 11; las ventanas de 21 nt compartidas con parientes son menos del 1 %. Sirve para inferir función, no para diseñar sobre otra especie (D37).",
     ["research/ola3/C12_validacion_homologia/REPORT_A.md", "research/ola3/C12_validacion_homologia/REPORT_B.md", "research/ola3/C12_validacion_homologia/PREREGISTRO.md"]),
    ("Fase 2 · ¿Cuántos genes blanco llegan a un ortólogo utilizable en <i>D. maidis</i>?",
     "Veredicto (b): viable sólo para 2 genes nominales. Ortología recíproca por secuencia resuelta en 11 de 14 familias (Swiss-Prot de artrópodos contra el proteoma de <i>M. quadrilineatus</i>). Sólo ATP synthase beta y actina superan el criterio de nucleótido (≥ 300 nt con ≥ 90 %) contra los TSA de <i>D. maidis</i>, y la actina es multigénica. Criterio fijado antes de buscar.",
     ["research/ola3/C11_diseno_nuevo/REPORT.md", "research/ola3/C11_diseno_nuevo/criterio.md", "research/ola3/C11_diseno_nuevo/sources.json"]),
    ("C10 · ¿Hay datos de ARN pequeños virales para nuestro blanco?",
     "No, y es un vacío documentado: cero registros en SRA y GEO para el <i>Maize rayado fino virus</i> y "
     "para <i>Dalbulus maidis</i> con estrategia de ARN pequeño. Los dos sustitutos abiertos que sí existen "
     "muestran que los puntos calientes no siguen la estructura del ARN y dependen del hospedador, lo que "
     "desaconseja copiarlos como selector de región blanco.",
     ["research/ola3/C10_vsirna_virus/REPORT.md", "research/ola3/C10_vsirna_virus/sources.json"]),
    ("C9 · Tarea 3 · Pre-registro de la validación retrospectiva",
     "Escrito antes de mirar los datos: que conjunto, que estadistico, qué contaría como éxito y como "
     "fracaso, y la decisión de reportar el intervalo y no el valor p. La validación no se corrió.",
     ["research/ola3/C9_sensibilidad_umbral/PREREGISTRO_validacion_retrospectiva.md"]),
    ("Checkpoint 2 · Página de siete casillas",
     "La página que se lee en diez minutos, con las siete casillas de la guía y las cifras verificadas contra sus archivos. El protagonista (D42) es el veto y el movimiento de región: las dos regiones que EPILAB eligió para los genes del insecto contienen ventanas de 21 nt idénticas a <i>H. vitripennis</i>, y moviendo la región dentro del mismo gen <code>BicC_Dm</code> pasa de 20 a 36 ventanas que pasan el filtro y de 22 a 0 coincidencias (región 922-1221, vigente por D25), con lo que queda primero de la lista del insecto en las diez combinaciones de agregación a 21 nt. Se presenta en dos listas por mecanismo (D38).",
     ["entregables/checkpoint2-una-pagina.md", "docs/plan_checkpoint2/salidas/F4_checklist_guia.md"]),
    ("Checkpoint 2 · Entrega y mecanismo (Fase 2)",
     "Qué dicen las fuentes abiertas sobre la entrega oral y el mecanismo de RNAi en insectos, con el estado de apertura de cada fuente. Las que no se pudieron abrir se declaran y no se citan.",
     ["docs/plan_checkpoint2/salidas/F2_entrega_y_mecanismo.md"]),
    ("Checkpoint 2 · Hipótesis, alternativas y validación (Fase 3)",
     "Diseño conceptual: pregunta, hipótesis con la condición que la refutaría, cinco alternativas, controles y una tabla de interpretación con el criterio de descarte escrito de antemano. No es una recomendación experimental.",
     ["docs/plan_checkpoint2/salidas/F3_hipotesis_alternativas_validacion.md"]),
    ("Checkpoint 2 · Decisiones de ranking y de etiquetas (Fase 1)",
     "D38 (dos listas por mecanismo), D39 (marcador [M] para lo medido por nosotros) y D40 (matar y esterilizar como dos ejes). Incluye la corrección de la lectura del par eth–burs-α.",
     ["docs/plan_checkpoint2/salidas/F1_decision_ranking.md", "00_meta/DECISIONS.md"]),
    ("Robustez de la región <code>BicC_Dm</code> 922-1221 en los tres ejes (M7)",
     "Sobre <strong>4.368 configuraciones</strong> —umbrales, modos, tablas de apilamiento y los dos motores de plegado— "
     "922-1221 le gana a la región que eligió el laboratorio (264-563) en el 99,1 % contando dentro del gen y en el "
     "99,6 % contando la molécula recortada, pero a 2121-2420 sólo en el 36,4 % en contexto y en el 75,6 % recortada: "
     "el marco de conteo decide tanto como los umbrales. Al cambiar de referencia queda primera en las tres fuentes que "
     "permiten compararla, y <code>GCWP01</code> no cubre un solo nucleótido de la región. El criterio de riesgo no "
     "cambia quién gana, y bajo la regla mecanicista el riesgo de las tres regiones es cero.",
     ["research/ola4/M7_robustez_bicc/REPORT.md", "research/ola4/M7_robustez_bicc/resultados/tabla_unica.md"]),
    ("Las 28 secuencias de Cedden: se dejan publicadas y declaradas (D41)",
     "La tabla unida a su razón de riesgo ya estaba en el remoto desde el 2026-10-21. Son datos públicos CC BY y no secuencias de EPILAB. "
     "Se decidió dejarla publicada con la advertencia de que la unión no tiene clave publicada.",
     ["research/ola3/C9_sensibilidad_umbral/datos/LEEME.md", "00_meta/DECISIONS.md"]),
]

FALTA = [
    ("Fecha y texto del correo enviado", "decision", True,
     "El correo se envió, como confirmó el usuario, pero el repo no registra la fecha ni el texto enviado. "
     "El borrador tiene siete preguntas y <code>PLAN_DESARROLLO.md</code> §8 decía cinco."),
    ("Qué cifra de ventanas eficientes se publica, y con qué argumento", "decision", True,
     "Esta página y los entregables dicen que <code>BicC_Dm</code> 922-1221 «pasa de 20 a 36 ventanas que pasan el "
     "filtro». Son los conteos <em>en contexto</em>; M7 midió que la cifra de la molécula que se sintetizaría es "
     "<strong>26 contra 17</strong>, y que el «32 idénticas en los tres transcriptomas contra 22» de D25 mezcla "
     "conservación con cobertura, porque <code>GCWP01</code> no cubre 922-1221. Las dos cifras y su fuente están en "
     "<code>research/ola4/M7_robustez_bicc/NOTAS_PARA_META.md</code>. No se corrigió por cuenta propia: cambia una "
     "recomendación publicada."),
    ("Confirmar el criterio de commits", "decision", False,
     "El prompt de C9 pide un commit por tarea y la regla general de la ola 3 dice no commitear (D5). Se "
     "siguió la instrucción específica del prompt; si se prefiere la regla general, se reescribe."),
    ("Escala para ordenar pares dentro de un grupo", "decision", False,
     "<code>eth</code> y <code>burs-α</code>: el orden cambia entre escala absoluta y min-max. La regla de D38 "
     "exige que el orden se sostenga en las dos. Pregunta de método para el equipo."),
]

LIMITES = [
    ("No hay etiquetas de eficacia para el vector",
     "Ningún dato experimental de silenciamiento en <i>Dalbulus maidis</i> respalda el umbral. Por eso el "
     "barrido mide fragilidad de la recomendación y no si el umbral es correcto: lo segundo necesita "
     "etiquetas que no existen."),
    ("Los conteos absolutos de los dos motores no son comparables entre sí",
     "<s>No hay RNAplfold 2.1.5 en la máquina (el que instala si-Fi21 es un ejecutable de Windows), así que "
     "todo corre con ViennaRNA 2.7.2.</s> <strong>Corregido el 2026-10-24:</strong> M2 compiló RNAplfold 2.1.5 "
     "desde el fuente oficial y reproduce los cuatro conteos publicados del binario del instalador, así que los "
     "dos motores corren en esta máquina y M7 los usó como eje. Sigue valiendo lo esencial: los conteos de un "
     "motor no se comparan con los del otro, y el motor mueve el resultado —en <code>BicC_Dm</code> da vuelta la "
     "comparación entre 922-1221 y 2121-2420 en el punto por defecto—. Cada número declara su motor, su tabla de "
     "apilamiento y su modo."),
    ("La validación está sub-potenciada por un factor 2,4 en n",
     "Dos ARNdc contra el mismo gen correlacionan 0,245, de modo que una correlación verdadera de 0,7 se "
     "observa como 0,35 y la potencia con n = 28 es 0,42; para 80 % harían falta n = 67. Comparar dos "
     "proxies entre si es inviable: 0,11 con atenuacion."),
    ("La unión de secuencias y desenlace no tiene clave publicada",
     "Los dos archivos adicionales de Cedden no comparten identificador. La unión es por orden dentro de "
     "cada gen y pasó 20 de 20 chequeos de consistencia con las etiquetas de predicción, pero si el orden "
     "de las dos hojas no fuera el mismo, el error no se detectaria con esos chequeos."),
]


RANKING = "research/ola3/C7_ranking_v2/resultados/ranking_v2.json"
ORDEN_GENES = ["MP_MRFV", "BicC_Dm", "CP_MRFV", "eth_Dm", "bursA_Dm", "ATPaseD_Dm"]
NUEVOS = {"eth_Dm", "bursA_Dm"}   # los dos que agrego C5; no tienen region de planilla
SIN_PLANILLA = "gen nuevo: no estaba en la planilla"


def tabla_regiones():
    """Las seis regiones, leidas del JSON del ranking v2 en vez de copiadas a mano."""
    if not existe(RANKING):
        return ('<p class="lead" style="color:var(--stop)">No se encontró %s en disco.</p>'
                % html.escape(RANKING))
    d = json.loads((RAIZ / RANKING).read_text(encoding="utf-8"))
    filas = []
    for g in ORDEN_GENES:
        planilla = d["k"]["21"]["regiones"][g]
        prop21 = d["k"]["21"]["regiones_recomendadas"][g]
        prop22 = d["k"]["22"]["regiones_recomendadas"][g]
        nueva = g not in NUEVOS
        filas.append(
            "<tr><td><code>%s</code></td><td>%s</td><td><strong>%s</strong></td>"
            "<td>%s</td><td>%s</td></tr>"
            % (html.escape(g),
               html.escape(planilla) if nueva else "—",
               html.escape(prop21), html.escape(prop22),
               "" if nueva else SIN_PLANILLA))
    return ('<div class="tw"><table>\n<thead><tr><th>Gen</th><th>Región de la planilla</th>'
            "<th>La que proponemos, 21 nt</th><th>22 nt</th><th></th></tr></thead>\n"
            "<tbody>\n%s\n</tbody></table></div>" % "\n".join(filas))


def tarjeta(titulo, desc, rutas):
    faltantes = [r for r in rutas if not existe(r)]
    def etiqueta(r):
        q = Path(r)
        # REPORT.md hay uno por investigacion: sin la carpeta, dos enlaces quedan
        # indistinguibles ("REPORT.md · REPORT.md").
        return "%s/%s" % (q.parent.name, q.name) if q.name in ("REPORT.md", "index.html") else q.name
    enlaces = " · ".join(
        '<a href="%s">%s</a>' % (html.escape(r), html.escape(etiqueta(r)))
        for r in rutas if existe(r))
    aviso = ("" if not faltantes else
             '<p class="f" style="color:var(--stop)">No encontrado en disco: %s</p>'
             % html.escape(", ".join(faltantes)))
    return ('<div class="card"><p class="t">%s</p><p class="d">%s</p>'
            '<p class="f">%s</p>%s</div>' % (html.escape(titulo), desc, enlaces, aviso))


hechos = "\n".join(tarjeta(t, d, r) for t, d, r in HECHO)
sin_disco = sum(1 for _, _, rs in HECHO for r in rs if not existe(r))

filas = "\n".join(
    '<tr><td>%s%s</td><td>%s</td><td>%s</td></tr>'
    % ('<strong>' + html.escape(t) + '</strong>' if urg else html.escape(t),
       ' <span class="tag q">?</span>' if urg else '',
       'decisión del equipo' if k == 'decision' else 'trabajo',
       d)
    for t, k, urg, d in FALTA)

regiones = tabla_regiones()

limites = "\n".join('<h3>%s</h3><p>%s</p>' % (html.escape(t), d) for t, d in LIMITES)

# No se incrusta el último commit ni el estado de la rama. La página se genera antes de
# commitearse, así que el hash que mostraría es siempre el del commit anterior y la rama
# siempre figura como desincronizada: no puede estar al día consigo misma. Para eso está
# `git log`, que además no miente.

n_dec = sum(1 for _, k, _, _ in FALTA if k == "decision")
n_tra = len(FALTA) - n_dec


CUENTA = {2: "dos", 3: "tres", 4: "cuatro", 5: "cinco", 6: "seis", 7: "siete", 8: "ocho"}


def contar(n, singular, plural):
    """«tres decisiones», «un trabajo chico»: el número en letras hasta ocho.

    El singular llega con su artículo, porque el género lo decide el sustantivo
    y no el contador: «una decisión» pero «un trabajo».
    """
    return singular if n == 1 else "%s %s" % (CUENTA.get(n, str(n)), plural)


doc = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Estado del entregable — que esta hecho y que falta</title>
<style>{CSS}</style></head><body>
<div class="wrap">
<header>
  <p class="eyebrow">Investigathón Y-Hat · track chicharrita del maíz</p>
  <h1>Qué está hecho y qué falta</h1>
  <p class="sub">Foto del entregable al 2026-10-21. Generada con
  <code>tools/generar_estado.py</code>, que comprueba contra el disco que cada archivo nombrado
  existe. <strong>Esta página no es fuente de verdad</strong>: el estado se declara en
  <a href="PLAN_DESARROLLO.md">PLAN_DESARROLLO.md</a> (§1 bis y §3 ter) y cada afirmación vive en
  el informe que enlaza.</p>
  <p class="sub"><a href="index.html">← Volver a la portada</a></p>
</header>

<div class="verdict">
<p><strong>Los cinco pedidos del Checkpoint 1 están cerrados</strong>, más los dos opcionales, y las
tres tareas de fortalecimiento de C9 tienen entregable. No queda ninguna medición grande pendiente.
Lo que sigue son <strong>{contar(n_dec, "una decisión", "decisiones")} y
{contar(n_tra, "un trabajo chico", "trabajos chicos")}</strong>, no producir el
entregable.</p>
<p>Dos cosas bloquean al resto: el dato que falta para mandar el correo al investigador, y cuál es
el análisis primario de la validación retrospectiva, porque decidirlo después de ver los datos
anula el pre-registro.</p>
</div>

<h2>Lo que está hecho</h2>
<p class="lead">Cada tarjeta enlaza el archivo que la respalda. Verificación automática de esta
corrida: <strong>{"todos los archivos existen" if sin_disco == 0 else f"{sin_disco} archivo(s) nombrados no están en disco"}</strong>.</p>
<div class="toc">
{hechos}
</div>

<h2>Lo que falta</h2>
<p class="lead">Ordenado por lo que bloquea. Lo marcado con <span class="tag q">?</span> es lo que
hay que decidir antes de seguir.</p>
<div class="tw"><table>
<thead><tr><th>Qué</th><th>Tipo</th><th>Por qué</th></tr></thead>
<tbody>
{filas}
</tbody></table></div>

<h2>Los límites que viajan con todo lo anterior</h2>
<p class="lead">Ninguno invalida el entregable; todos cambian cómo se leen sus números, y están
declarados en cada informe.</p>
{limites}

<h2>Las regiones que proponemos</h2>
<p class="lead">Lo que cambia respecto de la planilla de EPILAB no es el conjunto de genes sino
<strong>qué tramo de cada uno se sintetiza</strong>. La tabla se arma leyendo
<code>ranking_v2.json</code>, no a mano. Los dos genes del insecto van a 300 nt, que es el largo
del amplicón de la planilla; los otros cuatro, a 200. <strong>Salvedad para
<code>BicC_Dm</code>:</strong> la tabla muestra lo que devolvió el ranking (2121-2420), pero la
recomendación vigente es <strong>922-1221</strong> desde D25, elegida por conservación entre
fuentes; cambiarla no mueve el orden (94,2 % de los sorteos lo conservan). La tabla no se edita a
mano, así que la salvedad va acá.</p>
{regiones}
<p class="lead" style="margin-top:14px">Las dos recomendaciones que importan, las del insecto, no
se apoyan en la densidad sino en el <strong>veto</strong>: la región de <code>BicC_Dm</code> que
eligió la planilla contiene 22 ventanas con coincidencia perfecta de 21 nt en
<i>Homalodisca vitripennis</i> y la que proponemos, cero
(<a href="research/ola2/W7_ranking/REPORT.md">W7 §2.2</a>). El orden que sale de ellas, con los dos
genes nuevos y los dos largos de ventana, está en
<a href="research/ola3/C7_ranking_v2/REPORT.md">C7 v2</a>.</p>

<h2>El resultado de C9 en una línea</h2>
<p class="lead">El <strong>candidato</strong> superior es robusto al umbral y las
<strong>coordenadas exactas</strong> no lo son. Reeligiendo la región con la regla del ranking
—largo propio del gen y veto aplicado— <code>MP_MRFV</code> queda primero en el
<strong>100 %</strong> de la grilla a 21 nt y en el 98,0–99,6 % a 22 nt. Lo que no aguanta es
congelar las coordenadas: con las regiones fijas y el umbral moviéndose queda primero en el 62 %.
Lo defendible es entregar una <strong>región candidata, no un sitio</strong>, y declarar con qué
umbral se corrió.</p>
<p class="lead">El par <code>ATPaseD_Dm</code> contra <code>CP_MRFV</code> <strong>no</strong> es
un empate práctico a 21 nt: se da vuelta en el 3,3 % de la grilla. El 48,9 % que decía la primera
versión de C9 salía de medir la ventana libre de 200 nt, que en <code>ATPaseD_Dm</code> cae sobre
una región <strong>vetada</strong>. Los empates que sí quedan son <code>CP_MRFV</code> contra
<code>burs-alpha</code> y <code>eth</code> contra <code>burs-alpha</code>: el orden de los tres
últimos puestos no se sostiene.
<a href="research/ola3/C9_sensibilidad_umbral/index.html">Leer C9</a>.</p>

<footer>
  <p>Marcadores de evidencia: <span class="tag e">E</span> establecido ·
  <span class="tag r">R</span> reportado · <span class="tag">H</span> hipótesis nuestra ·
  <span class="tag q">?</span> incierto o en conflicto entre fuentes.</p>
  <p>Las secuencias de EPILAB y cualquier dato no publicado del corpus no se suben a servicios web
  de terceros ni al repositorio público. Todo análisis de esas secuencias corre con herramientas
  locales.</p>
</footer>
</div>
</body></html>
"""

(RAIZ / "estado.html").write_text(doc, encoding="utf-8")
print("escrito estado.html (%d bytes); archivos nombrados que faltan en disco: %d"
      % (len(doc), sin_disco))
