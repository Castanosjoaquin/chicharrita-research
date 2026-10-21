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
    ("C9 · Tarea 2 · Corregida la lectura del barrido de pesos",
     "La diagonal de B.3 mide la escala, no la robustez del orden. La afirmación vieja queda dicha y "
     "tachada, con la nueva y su fuente al lado, en W7 y en el ranking v2.",
     ["research/ola2/W7_ranking/REPORT.md", "research/ola3/C7_ranking_v2/REPORT.md"]),
    ("Las cuatro decisiones del checkpoint, formalizadas",
     "D33 a D36: las bacterias salen del alcance del diseño por ARNi, el objetivo es el insecto como "
     "vector, la ventana se fija en 21 y 22 nt por evidencia biológica y el ejercicio sobre los cuatro "
     "candidatos es una auditoría y no la reproducción de un resultado validado.",
     ["00_meta/DECISIONS.md"]),
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
]

FALTA = [
    ("Confirmar apellido y dominio del correo del investigador", "decision", True,
     "El borrador del correo está escrito y <strong>sin enviar</strong>: la transcripción automática del "
     "checkpoint escribió el apellido de varias formas y no se adivina. Es lo único que bloquea el envío "
     "(<a href=\"entregables/correo-investigador.md\">ver borrador</a>)."),
    ("Decidir el análisis primario de la validación", "decision", True,
     "Correlación agrupada sobre los 28 ARNdc, o dentro de cada gen. Los propios autores muestran que el "
     "gen blanco domina la razón de riesgo (efecto del gen P = 0,047, R<sup>2</sup> ajustado 0,40), así que una "
     "correlación agrupada alta podria venir del gen y no del puntaje. <strong>Bloquea la validación</strong>, y "
     "decidirlo despues de ver los datos rompe el pre-registro."),
    ("Autorizar la publicación de las 28 secuencias de Cedden", "decision", False,
     "Son datos públicos de un artículo CC BY, no secuencias de EPILAB. Están unidas a su razón de riesgo "
     "en <code>research/ola3/C9_sensibilidad_umbral/datos/</code>, <strong>sin subir al remoto</strong> a la espera de esa decision."),
    ("Correr la validación retrospectiva", "trabajo", False,
     "Media hora de cómputo una vez cerrado el punto anterior. Con la fiabilidad medida del desenlace la "
     "potencia es 0,42, de modo que lo mas probable es un intervalo que incluya el cero; el pre-registro ya "
     "declara que eso <strong>no refuta el puntaje</strong>."),
    ("Confirmar el criterio de commits", "decision", False,
     "El prompt de C9 pide un commit por tarea y la regla general de la ola 3 dice no commitear (D5). Se "
     "siguió la instrucción específica del prompt; si se prefiere la regla general, se reescribe."),
]

LIMITES = [
    ("No hay etiquetas de eficacia para el vector",
     "Ningún dato experimental de silenciamiento en <i>Dalbulus maidis</i> respalda el umbral. Por eso el "
     "barrido mide fragilidad de la recomendación y no si el umbral es correcto: lo segundo necesita "
     "etiquetas que no existen."),
    ("Los conteos absolutos no son comparables con la ola 2",
     "No hay RNAplfold 2.1.5 en la máquina (el que instala si-Fi21 es un ejecutable de Windows), así que "
     "todo corre con ViennaRNA 2.7.2. Las comparaciones internas de cada informe sí valen, porque usan el "
     "mismo motor de los dos lados. Cada numero declara su backend y su modo."),
    ("La validación está sub-potenciada por un factor 2,4 en n",
     "Dos ARNdc contra el mismo gen correlacionan 0,245, de modo que una correlación verdadera de 0,7 se "
     "observa como 0,35 y la potencia con n = 28 es 0,42; para 80 % harían falta n = 67. Comparar dos "
     "proxies entre si es inviable: 0,11 con atenuacion."),
    ("La unión de secuencias y desenlace no tiene clave publicada",
     "Los dos archivos adicionales de Cedden no comparten identificador. La unión es por orden dentro de "
     "cada gen y pasó 20 de 20 chequeos de consistencia con las etiquetas de predicción, pero si el orden "
     "de las dos hojas no fuera el mismo, el error no se detectaria con esos chequeos."),
]


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

<h2>El resultado de C9 en una línea</h2>
<p class="lead">El <strong>candidato</strong> superior es robusto al umbral y la <strong>región exacta</strong>
no lo es. <code>MP_MRFV</code> queda primero en el 99,1 % de la grilla en modo fiel y el 98,2 % en
modo corregido, pero su región de 200 nt coincide con la de defecto en apenas el 11,7 % y el 25,8 %
de los puntos, y hay puntos con solapamiento cero. El par <code>ATPaseD_Dm</code> contra
<code>CP_MRFV</code> es un empate práctico: se invierte en casi la mitad de la grilla. Lo defendible
es entregar una <strong>región candidata, no un sitio</strong>.
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
