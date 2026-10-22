# Proyecto: Investigathon Y-Hat — Track chicharrita del maíz / RNAi

## Qué es esto
Repositorio de investigación de un equipo de 4 estudiantes de Ingeniería en IA
(UdeSA) para el Investigathon de Y-Hat (UBA). El track es el diseño y la
priorización de soluciones basadas en ARN exógeno (mecanismo de RNAi) contra el
vector *Dalbulus maidis* (chicharrita del maíz) y los patógenos que transmite.
El equipo NO aporta laboratorio: aporta bioinformática, datos, desarrollo
computacional e innovación abierta.

## Reglas permanentes

### Evidencia
- Toda afirmación técnica lleva fuente. Sin fuente, no entra al reporte.
- Etiquetá cada afirmación relevante con uno de estos marcadores:
  - `[E]` establecido: consenso en literatura revisada por pares. Un resultado
    computacional propio nunca es `[E]`, aunque la herramienta sea estándar.
  - `[R]` reportado: una o pocas fuentes, preprint, nota técnica, patente, web de empresa.
  - `[M]` medido por nosotros: conteo, tasa, frecuencia o concordancia calculados por el
    equipo, reproducibles desde el repo (script, entrada y salida con ruta). Si la entrada
    es un dato no publicado que no se versiona (p. ej. secuencias de EPILAB), se declara
    «con insumos locales». `[M]` rotula el número, no su lectura: la interpretación va en
    `[H]`. Un resultado in silico es una hipótesis sobre eficacia, no una prueba (Guía del
    checkpoint 2).
  - `[H]` hipótesis nuestra: idea del equipo, todavía sin respaldo; incluye toda lectura
    o recomendación que se derive de un `[M]`.
  - `[?]` incierto / contradicción entre fuentes.
- Prohibido citar una fuente que no abriste. Nada de DOIs, títulos o números
  reconstruidos de memoria. Si no pudiste abrir la fuente, anotala en
  `00_meta/PREGUNTAS_ABIERTAS.md` como pendiente.
- Los números (porcentajes de eficacia, rendimientos, dosis, pérdidas de
  cosecha) van siempre con la fuente y el contexto experimental (laboratorio,
  invernáculo, campo; especie; n).

### Alcance ético y de seguridad
- El trabajo es control fitosanitario agrícola con información pública y
  publicada.
- Fuera de alcance, sin excepción: cualquier cosa que aumente la virulencia,
  la transmisibilidad o el rango de hospedadores de un patógeno; protocolos de
  síntesis o producción de agentes biológicos peligrosos; diseño dirigido a
  dañar especies no objetivo.
- Si una herramienta o búsqueda devuelve un rechazo, registralo en
  `00_meta/PREGUNTAS_ABIERTAS.md` y seguí con otra línea. No reformules para
  esquivar el rechazo.
- Toda propuesta de diseño incluye su contracara de riesgo: off-targets en
  maíz, en organismos no objetivo (polinizadores, enemigos naturales, fauna
  del suelo, humanos), persistencia ambiental y resistencia.

### Memoria del proyecto (se actualiza siempre, no al final)
- `00_meta/GLOSARIO.md` — término, definición en una línea, por qué nos importa.
- `00_meta/DECISIONS.md` — una entrada por decisión: fecha, decisión, alternativas
  consideradas, criterio, consecuencia. Formato ADR liviano.
- `00_meta/CAMINOS_PROBADOS.md` — qué se intentó, qué se descartó y por qué.
  Un descarte bien documentado vale tanto como un hallazgo.
- `00_meta/PREGUNTAS_ABIERTAS.md` — lo que no sabemos, lo que hay que preguntarle
  al investigador, lo que depende de datos que todavía no tenemos.
- `00_meta/FUENTES.md` — bibliografía consolidada.

### Formato
- Los reportes son prosa técnica en Markdown, no listas de bullets sueltos.
- Nombres científicos en itálica y completos la primera vez.
- Español. Términos técnicos en inglés entre paréntesis la primera vez que
  aparecen.

## Corpus oficial del Investigathon (ola 2)

El material que nos dieron vive en la carpeta YHAT-biotech: papers, un .docx con
links a bases de datos, herramientas de diseño y verificación de off-targets,
genomas y transcriptomas, y las secuencias provistas por EPILAB.

### Manejo del material
- Los archivos originales no se modifican, no se renombran y no se mueven.
  Todo trabajo se hace sobre copias dentro de `work/`.
- Todo lo que se derive del corpus (tablas, extractos, índices) se guarda en
  `research/ola2/` y apunta al archivo original por su ruta relativa exacta.
- Si un archivo no se puede abrir o está corrupto, se anota en el manifiesto con
  el motivo. No se adivina su contenido por el nombre.

### Confidencialidad de las secuencias
- Las secuencias de EPILAB y cualquier dato no publicado del corpus no se suben
  a servicios web de terceros: ni al BLAST web del NCBI, ni a servidores de
  plegado online, ni a ninguna herramienta que procese del lado del servidor.
  Todo análisis de esas secuencias se corre con herramientas locales.
- Si una herramienta del corpus solo funciona como servicio web, se documenta la
  limitación y se busca el equivalente local; no se sube el dato igual.
- Buscar en la web información *sobre* las herramientas, los genes o los
  organismos está bien. Lo que no se hace es pegar las secuencias en un
  buscador o en un formulario.

### Uso de los papers
- Se parafrasea. No se copian párrafos ni secciones completas a nuestros
  documentos. Citas textuales solo cuando la formulación exacta importa, breves
  y entrecomilladas, con referencia.
- Cada paper leído entra en `research/ola2/W1_papers/papers.json`, aunque se
  haya descartado por irrelevante: saber qué se descartó y por qué es parte del
  resultado.
