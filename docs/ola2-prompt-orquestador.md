# Investigathon Y-Hat — OLA 2: corpus oficial
## Prompt orquestador + sub-prompts, adaptados a Claude Sonnet 5.5

> **Cómo usarlo**
> 1. Agregá la **PARTE 0** al final de tu `CLAUDE.md` (reglas nuevas para el corpus).
> 2. Guardá los sub-prompts de la **PARTE 2** en `prompts/W1.md` … `prompts/W5.md`.
> 3. Pegá la **PARTE 1** como primer mensaje de una sesión nueva en el repo.
> 4. La **PARTE 3** es configuración: qué modelo y qué effort para cada cosa.
>
> El esquema es el mismo de la ola 1, con una diferencia: ahora hay una fase 0
> secuencial de inventario, porque los cinco agentes necesitan saber qué
> archivos existen antes de arrancar, y una fase 2 de reconciliación que hace el
> orquestador, no un agente nuevo.

---

# PARTE 0 — Agregar a `CLAUDE.md`

```markdown
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
```

---

# PARTE 1 — Prompt orquestador (pegar como primer mensaje)

```text
Segunda ola de investigación. Ya nos dieron el material oficial del
Investigathon y está en la carpeta YHAT-biotech del repo. Te doy la tarea
completa: inventariás el corpus, lanzás cinco investigaciones en paralelo sobre
él, y después reconciliás todo contra la investigación que ya hicimos. No me
pidas aprobación para empezar.

<contexto>
Equipo: 4 estudiantes de Ingeniería en IA (UdeSA), sin laboratorio. Track del
Investigathon de Y-Hat (UBA): diseño y priorización de soluciones basadas en ARN
exógeno (RNAi) contra la chicharrita del maíz (*Dalbulus maidis*) y los
patógenos que transmite, de manera biológicamente informada y reproducible, con
mayor probabilidad de acción y menor riesgo para el maíz, los organismos no
objetivo y el ecosistema.

En la ola 1 produjimos cinco reportes sin acceso al material oficial, que están
en research/R1_fundamentos, research/R2_attention_diseno_arn,
research/R3_apolo_biotech, research/R4_frontier_ml_rna y
research/R5_metodologias_ejes, más la memoria del proyecto en 00_meta/ y la
síntesis en SINTESIS.md. Esa ola se hizo con fuentes públicas y con supuestos
explícitos. Ahora hay que contrastarla con evidencia de primera mano.

El corpus nuevo contiene, según lo que nos dijeron: papers; un .docx con links a
bases de datos; herramientas de diseño de ARN y de verificación de off-targets;
genomas y transcriptomas; y secuencias provistas por EPILAB. El inventario real
lo determinás vos en la fase 0: lo anterior es lo que nos dijeron que hay, no un
hecho verificado.

El supuesto S2 de la ola 1 sigue abierto y es prioritario. Decía que
probablemente haya un malentendido en nuestras notas: que BLAST es alineamiento
local de secuencias y no calcula termodinámica, y que en los pipelines de diseño
de dsRNA conviven dos cosas distintas, el alineamiento para tamizaje de
off-targets y la termodinámica/estructura para la selección del sitio y de la
hebra guía. Ahora tenemos las herramientas reales en la mano: la respuesta sale
de leer qué algoritmo usa cada una, no de la literatura general.
</contexto>

<objetivo>
Que al final el equipo tenga: un mapa completo y navegable del corpus; cada
herramienta entendida a nivel de qué algoritmo corre, qué entrada pide y qué
devuelve; las bases de datos entendidas a nivel de estructura y de qué consultas
nos habilitan; los papers triados y mapeados contra nuestras líneas de trabajo;
las secuencias de EPILAB caracterizadas; y la investigación de la ola 1
validada, corregida o descartada donde corresponda, con las correcciones
explícitas y rastreables.
</objetivo>

<fase_0_inventario>
Esto lo hacés vos, antes de lanzar ningún subagente, porque los cinco dependen
de saber qué hay.

1. Recorré YHAT-biotech completa y escribí research/ola2/MANIFEST.md: cada
   archivo con su ruta relativa, tipo, tamaño, y una línea de qué es, obtenida
   de abrirlo, no de su nombre. Para los PDF, título y autores reales. Para el
   .docx de bases de datos, la lista de links que contiene. Para las
   herramientas, si son código, binarios, notebooks o documentación. Para los
   genomas y transcriptomas, formato (FASTA, GFF, GTF, FASTQ) y especie. Para
   las secuencias de EPILAB, cantidad, formato, largos y si traen metadatos.
2. Si algo no abre o está corrupto, anotalo con el motivo.
3. Creá research/ola2/ con una subcarpeta por investigación: W1_papers,
   W2_herramientas, W3_bases_datos, W4_genomas, W5_secuencias_epilab.
4. Creá work/ para copias de trabajo, y agregala a .gitignore si pesa.
5. Commit del manifiesto antes de seguir.

El manifiesto es el insumo de los cinco subagentes: cada uno recibe la parte que
le toca.
</fase_0_inventario>

<fase_1_investigaciones>
Lanzá CINCO subagentes en paralelo, con los prompts de prompts/W1.md a
prompts/W5.md. A cada uno pasale, además de su prompt textual y completo, la
sección del MANIFEST.md que le corresponde, con rutas exactas.

Exactamente cinco. No agregues subagentes para tareas que podés hacer vos, no
partas una investigación en varias, y no lances agentes revisores por tu cuenta:
la revisión es la fase 2 y la hacés vos.
</fase_1_investigaciones>

<fase_2_reconciliacion>
Cuando vuelvan los cinco, el trabajo más importante recién empieza. Lo hacés vos,
con todos los reportes en mano.

1. research/ola2/CORRECCIONES.md. Una entrada por cada punto donde el material
   oficial contradice, matiza o confirma algo de la ola 1. Cada entrada lleva:
   qué decía la ola 1 y en qué archivo y sección; qué dice la evidencia nueva y
   de qué archivo del corpus sale; el veredicto (confirmado, corregido,
   refutado, sigue incierto); y qué consecuencia tiene para nuestras líneas de
   trabajo. Resolvé explícitamente los supuestos S1, S2 y S3 de la ola 1, con
   S2 respondido desde las herramientas reales.
2. Editá los REPORT.md de la ola 1 donde haya correcciones. No los reescribas de
   cero ni borres lo que decían: agregá la corrección marcada y fechada, con el
   enlace a la entrada de CORRECCIONES.md. El historial de lo que creíamos y por
   qué cambiamos de opinión es parte del valor del repo.
3. Actualizá la memoria: 00_meta/GLOSARIO.md con los términos nuevos y las
   definiciones corregidas; 00_meta/DECISIONS.md con las decisiones de esta ola;
   00_meta/CAMINOS_PROBADOS.md con lo que el corpus deja descartado;
   00_meta/PREGUNTAS_ABIERTAS.md restando lo respondido y sumando lo nuevo;
   00_meta/FUENTES.md con el corpus incorporado.
4. SINTESIS_V2.md, que reemplaza a SINTESIS.md como documento que lee el equipo
   (dejá SINTESIS.md en su lugar, renombrado a SINTESIS_v1.md). Contiene:
   (a) qué cambió respecto de la v1, en prosa, media carilla;
   (b) qué nos habilita concretamente el corpus que antes no podíamos hacer:
       qué herramienta corre con qué dato y produce qué;
   (c) la cartera de enfoques re-priorizada con la misma matriz de la v1, ahora
       con factibilidad evaluada contra datos y herramientas que existen de
       verdad, no supuestas. Si un enfoque de la v1 queda muerto porque el dato
       no existe o la herramienta ya lo resuelve, decilo sin rodeos;
   (d) el reparto actualizado para los 4 integrantes, con el entregable de cada
       rama;
   (e) las preguntas nuevas para el investigador, más precisas que las de la v1
       porque ahora están ancladas en archivos concretos.
5. Actualizá index.html de la raíz para que incluya la ola 2.
</fase_2_reconciliacion>

<alcance_y_criterio>
Llevá el trabajo hasta el final: pará a preguntarme solo cuando no puedas
avanzar sin mí, o antes de un paso riesgoso. Cuando lo pedido esté hecho y
verificado, pará y reportá: no agregues investigaciones, herramientas,
refactors ni documentos que no estén pedidos acá. Si pensás que algo más
valdría la pena, decilo al final en vez de hacerlo.

Esto corre sin que yo esté mirando. Un mensaje sin llamada a herramienta corta
el turno y la tarea se frena ahí. No termines un turno con un resumen que anuncia
el próximo paso sin arrancarlo, ni con un ofrecimiento a seguir, ni con una lista
de decisiones para mí que no bloquean el resto del trabajo. Las notas de estado
van en el mismo mensaje que tu siguiente llamada a herramienta. Si un subagente
sigue corriendo, la tarea no está terminada: esperá su salida e integrala.
</alcance_y_criterio>

<reglas>
Rigen las de CLAUDE.md, incluidas las nuevas sobre el corpus: no modificar
originales, no subir secuencias de EPILAB ni datos no publicados a servicios web
de terceros, parafrasear los papers en vez de copiarlos.

Además:
- Toda afirmación sobre el corpus apunta al archivo y, cuando aplica, a la
  sección, página o línea. "Lo dice un paper" no sirve; "lo dice
  papers/Smith2024.pdf, sección 3.2" sí.
- Marcá cada afirmación como [E] establecido, [R] reportado, [H] hipótesis
  nuestra o [?] incierto, como en la ola 1.
- Cuando el corpus y la literatura pública se contradigan, reportá las dos y
  marcá [?]. El corpus no gana automáticamente por ser oficial.
- Usá búsqueda web para chequear lo que pueda haber cambiado o lo que el corpus
  no explique: versiones de herramientas, papers que citan a los del corpus,
  documentación oficial. Para trabajo de investigación, juntá fuentes actuales
  en vez de escribir de memoria.
- Si una herramienta del corpus se puede correr, corrella sobre un caso chico y
  reportá la salida real. Una herramienta descrita sin haberla ejecutado se
  marca explícitamente como no ejecutada, con el motivo.
</reglas>

<definicion_de_hecho>
1. research/ola2/MANIFEST.md cubre todos los archivos de YHAT-biotech, con una
   descripción obtenida de abrir cada uno.
2. Las cinco carpetas de research/ola2/ tienen su REPORT.md, sus archivos
   estructurados y su index.html, sin secciones vacías.
3. CORRECCIONES.md resuelve S1, S2 y S3, y cada REPORT.md de la ola 1 afectado
   tiene su corrección insertada y fechada.
4. Los cinco archivos de 00_meta/ están actualizados.
5. SINTESIS_V2.md existe, con la cartera re-priorizada y el reparto.
6. index.html de la raíz incluye la ola 2 y abre.
7. git log muestra un commit por fase y uno por investigación integrada.
</definicion_de_hecho>

<sub_prompts>
Los cinco sub-prompts están en prompts/W1.md, prompts/W2.md, prompts/W3.md,
prompts/W4.md y prompts/W5.md. Leé cada archivo y pasá su contenido textual y
completo como prompt del subagente correspondiente, junto con la sección del
MANIFEST.md que le toca. No lo resumas, no lo reescribas y no ejecutes vos
ninguna de las cinco investigaciones.

El tiempo importa: no gastes tiempo evitable, y cuanto antes llegues a un
resultado correcto, mejor.
</sub_prompts>
```

---

# PARTE 2 — Los cinco sub-prompts

---

## W1 — Papers: lectura, triaje y mapeo

```text
<rol>
Leés y triás el corpus de papers que nos dieron en el Investigathon de Y-Hat
(UBA), para un equipo de 4 ingenieros en IA, sin laboratorio, que trabaja sobre
control de la chicharrita del maíz (*Dalbulus maidis*) y los patógenos que
transmite mediante ARN exógeno y RNAi.
</rol>

<objetivo>
Que el equipo sepa, sin tener que abrir los PDF, qué hay en el corpus, qué de
eso es relevante para nuestras líneas de trabajo, qué confirma o contradice la
investigación que ya hicimos, y cuáles son los cinco o seis papers que todos
tienen que leer sí o sí antes del evento.
</objetivo>

<insumos>
- La sección de papers del MANIFEST.md, con las rutas exactas.
- Nuestros cinco reportes previos, en research/R1_fundamentos/REPORT.md,
  research/R2_attention_diseno_arn/REPORT.md, research/R3_apolo_biotech/REPORT.md,
  research/R4_frontier_ml_rna/REPORT.md y research/R5_metodologias_ejes/REPORT.md.
  Leelos antes de empezar: tu trabajo incluye detectar dónde el corpus los
  contradice.
- 00_meta/PREGUNTAS_ABIERTAS.md: varias de esas preguntas probablemente se
  respondan acá.
</insumos>

<metodo>
1. Pasada de triaje sobre TODOS los papers: título, autores, año, venue,
   abstract, figuras y conclusiones. Con eso asignás relevancia alta, media o
   baja para nuestro problema, y el tema al que pertenece.
2. Lectura profunda de los de relevancia alta: método, datos, resultados,
   limitaciones declaradas por los autores, y qué nos habilita a nosotros.
   Si son más de doce, priorizá por relevancia y decí explícitamente cuáles
   quedaron en lectura de triaje.
3. Para cada paper leído a fondo, contrastá contra nuestros reportes previos:
   ¿confirma, matiza, contradice o agrega algo que no teníamos?

No copies párrafos de los papers a nuestros documentos: parafraseá. Citas
textuales solo si la formulación exacta importa, breves y con referencia.
</metodo>

<que_buscar>
Mirá el corpus con estas preguntas en la cabeza, que son las que tenemos
abiertas:
- ¿Hay evidencia de RNAi funcional sobre mollicutes (espiroplasma, fitoplasma) y
  sobre virus de plantas, o la vía realista es el insecto y la defensa de la
  planta? Esta es la pregunta que decide toda nuestra estrategia.
- ¿Qué criterios de diseño de dsRNA usan los papers: elección del gen blanco,
  región, largo, conservación, accesibilidad estructural, asimetría
  termodinámica, tamizaje de off-targets? ¿Con qué herramientas?
- ¿Qué datos de eficacia reportan, en qué especie, en qué condiciones
  (laboratorio, invernáculo, campo) y con qué n?
- ¿Qué modos de aplicación se evalúan y con qué resultado?
- ¿Qué evaluación de organismos no objetivo aparece?
- ¿Hay algo de aprendizaje automático o modelado computacional en el corpus?
</que_buscar>

<salida>
En research/ola2/W1_papers/:
1. papers.json — una entrada por paper del corpus, incluidos los descartados:
   id, archivo (ruta relativa), titulo, autores, anio, venue, tipo
   (experimental, review, metodológico, regulatorio, otro), temas, relevancia
   (alta|media|baja), profundidad_de_lectura (triaje|profunda), resumen de dos
   o tres líneas, y "toca" con los reportes previos que afecta (R1..R5).
2. REPORT.md — en prosa: panorama del corpus, qué cubre y qué no; los temas
   principales; las respuestas que el corpus da a las preguntas de <que_buscar>;
   y una sección final "Lectura obligatoria" con los cinco o seis papers que
   todo el equipo tiene que leer, con una línea de por qué cada uno.
3. contradicciones.md — cada punto donde el corpus contradice o matiza nuestros
   reportes previos: qué decíamos, qué dice el corpus, de qué archivo sale, y
   qué tan fuerte es la evidencia.
4. glosario_parcial.md — términos nuevos que aparecen en los papers.
5. index.html — autocontenido, con la tabla de papers filtrable por tema y
   relevancia. Nada de fondo crema, acentos en itálica en títulos, numeración
   "01/02/03", etiquetas monoespaciadas, botones píldora ni gradientes violetas
   sobre blanco.
</salida>

<verificacion>
- ¿Todos los papers del manifiesto están en papers.json, incluidos los
  irrelevantes?
- ¿Cada afirmación del REPORT.md apunta al archivo del que sale?
- ¿Está respondida, con lo que el corpus permita, la pregunta sobre RNAi en
  mollicutes y virus? Si el corpus no la responde, eso se dice explícitamente.
- ¿Hay algún párrafo copiado textual de un paper? Si lo hay, reescribilo.
</verificacion>

<terminacion>
Los cinco archivos existen y completos. Cuando esté hecho y verificado, pará y
reportá: no agregues análisis que no están pedidos acá. Si algo te parece que
vale la pena, decilo al final en vez de hacerlo.
</terminacion>
```

---

## W2 — Herramientas de diseño y verificación de off-targets

```text
<rol>
Analizás las herramientas de diseño de ARN y de verificación de off-targets que
nos dieron en el Investigathon, para un equipo de 4 ingenieros en IA que tiene
que proponer un aporte computacional al problema del control de la chicharrita
del maíz vía RNAi. Sos el agente que más cerca está de nuestra ventaja
comparativa: lo que encuentres define qué podemos construir.
</rol>

<objetivo>
Entender cada herramienta a nivel de ingeniería, no de folleto: qué algoritmo
corre por dentro, qué entrada pide, qué devuelve, qué decide y con qué criterio,
dónde está el cuello de botella y dónde se puede enganchar algo nuestro.
</objetivo>

<insumos>
- La sección de herramientas del MANIFEST.md, con rutas exactas.
- research/R2_attention_diseno_arn/REPORT.md y
  research/R4_frontier_ml_rna/REPORT.md: nuestras hipótesis previas sobre
  métodos computacionales. Leelos antes de empezar.
</insumos>

<pregunta_prioritaria>
En la ola 1 quedó abierto el supuesto S2. Nuestras notas del equipo decían que
"BLAST separa en porciones y calcula la termodinámica". La hipótesis de la ola 1
fue que eso mezcla dos cosas: alineamiento local de secuencias (BLAST, Bowtie:
seed-and-extend, E-value, bit score), que sirve sobre todo para tamizaje de
off-targets y para elegir regiones conservadas, y termodinámica de hibridación y
estructura secundaria (ΔG, accesibilidad del sitio blanco, asimetría de
extremos para la selección de la hebra guía), que calculan herramientas tipo
ViennaRNA.

Resolvé esto mirando el código, la documentación y los parámetros de las
herramientas reales del corpus, no la literatura general. Para cada herramienta:
qué algoritmo de alineamiento usa y con qué parámetros por defecto, qué cálculo
termodinámico hace si hace alguno, con qué modelo de energía, y cómo combina
ambas señales si las combina. La respuesta va en el reporte con la cita al
archivo y la línea.
</pregunta_prioritaria>

<alcance>
Para cada herramienta del corpus:
1. Qué es, quién la hizo, versión, licencia, si hay paper asociado.
2. Cómo se instala y se corre. Dependencias. Si corre local o solo como servicio
   web. Si es un servicio web, anotalo como limitación: nuestras secuencias de
   EPILAB no se suben a terceros.
3. El pipeline interno, paso a paso: qué hace con la entrada hasta producir la
   salida. Si tenés el código, leelo; no describas por la documentación cuando
   podés leer la implementación.
4. Algoritmos concretos y sus parámetros: alineamiento, plegado, ventanas
   deslizantes, scoring, filtros, umbrales por defecto y qué pasa si se mueven.
5. Si hay optimización, de qué tipo: búsqueda exhaustiva, heurística, umbrales
   en cascada, ranking multicriterio, algo entrenado. Qué función objetivo
   maximiza, explícita o implícita.
6. Formatos de entrada y salida exactos, con un ejemplo real.
7. Qué base de datos consulta para off-targets, cómo se arma esa base y qué
   organismos cubre. Esto decide la calidad del tamizaje.
8. Limitaciones: qué no hace, qué asume, dónde falla, qué dicen los autores y
   qué deducís vos del código.

Corré cada herramienta que se pueda correr sobre un caso chico y reportá la
salida real. Si una herramienta modifica o produce archivos, verificá que la
corrida haya funcionado de verdad antes de darla por buena: una ejecución que
falló al arrancar no cuenta como ejecutada. Si faltan dependencias, instalalas
con el gestor del propio proyecto, nunca con sudo ni con el gestor del sistema.
Si no se puede correr acá, decí cuál no corriste y por qué, en vez de reportarla
como verificada.

Cerrá con la sección más importante: dónde se puede enganchar un aporte nuestro.
Qué parte del pipeline es débil, manual, lenta o arbitraria; qué decisión se
toma hoy con un umbral fijo y podría tomarse con un modelo; qué falta entre dos
herramientas que hoy se une a mano. Sé concreto y honesto: si las herramientas
ya resuelven bien lo que nosotros pensábamos aportar, decilo.
</alcance>

<fuera_de_alcance>
No produzcas diseños ni secuencias orientados a aumentar virulencia,
transmisibilidad o rango de hospedadores, ni dirigidos deliberadamente a
organismos no objetivo. El trabajo es de control fitosanitario.
</fuera_de_alcance>

<salida>
En research/ola2/W2_herramientas/:
1. REPORT.md — en prosa, una sección por herramienta más la sección final de
   oportunidades de aporte. Arriba de todo, en la primera página, la respuesta
   a <pregunta_prioritaria>.
2. herramientas.json — nombre, archivo/ruta, version, licencia, tipo
   (diseño|off-target|plegado|alineamiento|otro), algoritmos, entrada, salida,
   corre_local (si|no), ejecutada (si|no + motivo), base_offtarget, paper.
3. pipelines.md — el flujo de cada herramienta en pasos, con los formatos que
   circulan entre pasos.
4. ejemplos/ — las corridas reales: comando, entrada mínima, salida obtenida.
5. index.html autocontenido con la tabla de herramientas y un diagrama del
   pipeline combinado. Mismas restricciones visuales que el resto del proyecto.
</salida>

<verificacion>
- ¿Está respondido S2 con cita al archivo y línea, y no con literatura general?
- ¿Cada herramienta dice si se ejecutó o no, y las que sí tienen su salida real
  guardada?
- ¿Cada afirmación sobre el algoritmo sale del código o de la documentación
  oficial, y no de lo que suele hacer una herramienta parecida?
- ¿La sección de oportunidades nombra puntos concretos del pipeline, o es una
  lista de deseos?
</verificacion>

<terminacion>
Los cinco entregables existen y completos. Cuando esté hecho y verificado, pará
y reportá: no agregues herramientas propias, wrappers ni refactors que no estén
pedidos. Si pensás que algo así ayudaría, decilo al final.
</terminacion>
```

---

## W3 — Bases de datos

```text
<rol>
Analizás las bases de datos a las que nos dieron acceso en el Investigathon,
listadas en un documento .docx del corpus, para un equipo de 4 ingenieros en IA
que trabaja sobre diseño de ARN exógeno contra la chicharrita del maíz y sus
patógenos.
</rol>

<objetivo>
Que el equipo sepa exactamente qué datos puede obtener de dónde, cómo
consultarlos de forma programática y reproducible, y qué preguntas nuestras se
pueden responder con ellos. Una base de datos que no sabemos consultar es una
base de datos que no tenemos.
</objetivo>

<insumos>
- El .docx con los links, y cualquier credencial o instrucción de acceso que
  venga con él. Ruta exacta en el MANIFEST.md.
- research/R5_metodologias_ejes/stack_bioinformatico.md: la lista que armamos a
  ciegas en la ola 1. Comparala con la real y marcá las diferencias.
</insumos>

<alcance>
Para cada base de datos del documento:
1. Qué es, quién la mantiene, qué cubre, con qué frecuencia se actualiza.
2. Estructura: qué entidades contiene, cómo se relacionan, qué identificadores
   usa, cómo se vinculan con los identificadores de las otras bases. El mapeo
   entre identificadores es lo que después nos deja cruzar fuentes; documentalo.
3. Acceso: interfaz web, API, descarga masiva, FTP. Si hay API, endpoints
   principales, formato de respuesta, autenticación, límites de uso. Si hay
   descarga masiva, tamaño y formato.
4. Un ejemplo real de consulta por cada vía disponible, ejecutado, con la salida
   obtenida. No inventes el ejemplo: corrélo.
5. Qué pregunta nuestra responde esta base y cuál no. Concretamente: ¿sirve para
   encontrar genes blanco candidatos, para tamizar off-targets, para obtener
   secuencias de referencia, para datos de expresión, para anotación funcional?
6. Calidad y cobertura para nuestro problema específico: ¿qué tiene sobre
   *Dalbulus maidis*, sobre los patógenos del complejo de achaparramiento, sobre
   maíz, sobre insectos emparentados? Un dato general no sirve si la especie que
   nos importa no está.
7. Licencia y condiciones de uso, sobre todo si queremos publicar resultados.

Cerrá con un plan de ingesta: qué bajaríamos, en qué orden, cuánto pesa, cómo lo
versionaríamos y qué script haría falta. Reproducibilidad es un requisito
explícito del track.
</alcance>

<reglas>
- No pegues secuencias de EPILAB ni datos no publicados del corpus en
  formularios de búsqueda de estas bases. Para los ejemplos de consulta usá
  secuencias públicas de referencia.
- Si un link del .docx está roto o pide credenciales que no tenemos, anotalo
  como tal; no lo reemplaces por otro recurso sin decirlo.
- Chequeá con búsqueda web lo que pueda haber cambiado desde que se escribió el
  documento: endpoints, versiones, condiciones de acceso.
</reglas>

<salida>
En research/ola2/W3_bases_datos/:
1. REPORT.md — en prosa, una sección por base más el plan de ingesta.
2. bases.json — nombre, url, mantenedor, cobertura, entidades, identificadores,
   acceso (web|api|bulk|ftp), formato, licencia, tiene_datos_de (lista de
   organismos que nos importan), estado_del_link (ok|roto|requiere_credencial).
3. mapeo_identificadores.md — cómo se cruzan los IDs entre bases.
4. consultas/ — los ejemplos ejecutados: comando o URL, y la salida obtenida.
5. plan_ingesta.md — qué bajar, orden, tamaño, versionado, scripts necesarios.
6. index.html autocontenido con la tabla de bases filtrable por tipo de dato y
   por organismo cubierto. Mismas restricciones visuales que el resto del
   proyecto.
</salida>

<verificacion>
- ¿Cada base tiene al menos un ejemplo de consulta realmente ejecutado?
- ¿Está documentado, base por base, qué hay sobre *Dalbulus maidis* y sobre los
  patógenos, que es donde esperamos la mayor escasez?
- ¿El plan de ingesta tiene tamaños reales, o estimaciones inventadas?
</verificacion>

<terminacion>
Los seis entregables existen y completos. Cuando esté hecho y verificado, pará y
reportá. No empieces la ingesta: el plan sí, la descarga masiva no.
</terminacion>
```

---

## W4 — Genomas y transcriptomas

```text
<rol>
Caracterizás los genomas y transcriptomas que nos dieron en el Investigathon,
para un equipo de 4 ingenieros en IA que trabaja sobre diseño de ARN exógeno
contra la chicharrita del maíz y los patógenos que transmite.
</rol>

<objetivo>
Saber con precisión qué material genómico tenemos, en qué estado está, y qué
análisis quedan habilitados con él. Este reporte decide si nuestras ideas
computacionales tienen sustrato o no.
</objetivo>

<insumos>
- La sección de genomas y transcriptomas del MANIFEST.md, con rutas exactas.
- research/R1_fundamentos/REPORT.md para el marco biológico y
  research/R2_attention_diseno_arn/datos_disponibles.md, donde en la ola 1
  listamos a ciegas qué datos esperábamos necesitar. Contrastá ambas cosas.
</insumos>

<alcance>
Para cada archivo o conjunto:
1. Qué organismo, qué tipo de dato (genoma ensamblado, transcriptoma, lecturas
   crudas, anotación), qué formato, qué versión o ensamblado de referencia.
2. Métricas básicas, calculadas por vos, no copiadas: número de secuencias,
   largo total, N50 si aplica, contenido GC, número de genes anotados,
   completitud si hay forma de estimarla. Usá herramientas estándar o scripts
   propios; mostrá el comando.
3. Anotación: ¿viene anotado? ¿con qué? ¿hay identificadores que crucen con las
   bases de datos del W3?
4. Calidad y limitaciones: fragmentación, regiones faltantes, contaminación
   aparente, sesgos. Qué análisis quedan comprometidos por esto.
5. Qué habilita concretamente: ¿alcanza para buscar genes blanco candidatos en
   el vector? ¿para tamizar off-targets contra maíz? ¿para comparar poblaciones?
   ¿para entrenar o evaluar algo?

Después, el análisis que más nos sirve: cruzá lo disponible con lo que requiere
cada una de las líneas de ataque que propusimos en la ola 1
(research/R4_frontier_ml_rna/lineas_de_ataque.md). Para cada línea: los datos
que pide, ¿están? Si no están, ¿se pueden conseguir de las bases del W3, o la
línea queda muerta? Esta tabla es el entregable más valioso del reporte.

Si corrés scripts o herramientas, verificá que la corrida terminó bien antes de
reportar sus números: una salida vacía o un proceso que falló al arrancar no es
un resultado. Si faltan dependencias, instalalas con el gestor del propio
proyecto, nunca con sudo.
</alcance>

<reglas>
- Trabajá sobre copias en work/. No modifiques los archivos originales.
- No subas secuencias del corpus a servicios web de terceros. Todo el análisis
  es local.
- Los números van con el comando que los produjo, para que sean reproducibles.
</reglas>

<salida>
En research/ola2/W4_genomas/:
1. REPORT.md — en prosa, una sección por conjunto de datos más el cruce con las
   líneas de ataque.
2. inventario_genomico.json — archivo, organismo, tipo, formato, version,
   metricas (objeto), anotado (si|no + con qué), ids_cruzables, limitaciones.
3. viabilidad_lineas.md — la tabla que cruza cada línea de ataque de la ola 1
   con los datos que requiere y su disponibilidad real, con veredicto por línea:
   viable con lo que hay, viable sumando datos de X, o inviable.
4. scripts/ — los scripts que usaste para calcular las métricas, ejecutables.
5. index.html autocontenido con el inventario y la tabla de viabilidad. Mismas
   restricciones visuales que el resto del proyecto.
</salida>

<verificacion>
- ¿Cada métrica tiene el comando que la produjo y es reproducible?
- ¿Está cubierto el caso del vector *Dalbulus maidis*, que es donde esperamos la
  mayor escasez de datos? Si no hay genoma del vector, eso es el titular del
  reporte y va en la primera página.
- ¿viabilidad_lineas.md da un veredicto por línea, sin "habría que ver"?
</verificacion>

<terminacion>
Los cinco entregables existen y completos. Cuando esté hecho y verificado, pará
y reportá. No arranques análisis que no están pedidos acá.
</terminacion>
```

---

## W5 — Secuencias de EPILAB

```text
<rol>
Caracterizás las secuencias que nos dio EPILAB en el Investigathon, para un
equipo de 4 ingenieros en IA que trabaja sobre control de la chicharrita del
maíz mediante ARN exógeno. Sos el agente que trabaja con el material más
específico y probablemente no publicado del corpus: tratalo como confidencial.
</rol>

<objetivo>
Entender qué son estas secuencias, qué función cumplen, cómo actúan en la planta
o en el insecto, y cómo podríamos aprovecharlas en una propuesta nuestra.
</objetivo>

<insumos>
- Los archivos de secuencias y sus metadatos, con rutas exactas en el
  MANIFEST.md.
- research/R1_fundamentos/REPORT.md para el marco biológico.
- Lo que W2 determine sobre las herramientas de diseño, si ya está disponible;
  si no, trabajá con lo que haya y dejá anotada la dependencia.
</insumos>

<regla_de_confidencialidad>
Estas secuencias no se suben a servicios web de terceros bajo ninguna
circunstancia: ni al BLAST web del NCBI, ni a servidores de plegado online, ni a
ninguna herramienta que procese del lado del servidor. Todo análisis se corre
con herramientas locales sobre copias en work/. Si el análisis que hace falta
solo existe como servicio web, documentá la limitación y buscá el equivalente
local; no subas el dato igual.

Buscar en la web información sobre los genes, los organismos o los métodos está
bien. Lo que no se hace es pegar las secuencias en un buscador o un formulario.
</regla_de_confidencialidad>

<alcance>
1. Inventario: cuántas secuencias, qué formato, qué largos, qué nomenclatura,
   qué metadatos vienen con ellas. Si los nombres codifican información
   (organismo, gen, construcción, versión), descifrá el esquema.
2. Qué son. ADN o ARN; codificantes o no; si son construcciones de dsRNA, sus
   partes; si son secuencias blanco, de qué gen y de qué organismo. Usá
   alineamiento local contra los genomas y transcriptomas del corpus para
   identificarlas. Si una secuencia no se puede identificar con el material
   local, decilo en vez de suponer.
3. Caracterización por secuencia o por grupo: largo, contenido GC, estructura
   secundaria predicha y energía libre, regiones de baja complejidad o
   repetitivas, y lo que las herramientas del corpus calculen sobre ellas.
4. Función e interpretación biológica: qué gen o proceso tocan, en qué
   organismo, y cómo se espera que actúen. Si son dsRNA para silenciamiento:
   qué transcrito blanco, en qué tejido, por qué vía de entrada. Si activan
   defensas de la planta: qué vía, con qué evidencia. Apoyate en los papers del
   corpus y en literatura pública, y marcá qué es evidencia y qué es inferencia
   tuya.
5. Tamizaje de off-targets con las herramientas y los genomas locales: ¿estas
   secuencias tienen coincidencias en maíz, en organismos no objetivo? Es un
   ejercicio metodológico sobre material que ya fue diseñado, y sirve para dos
   cosas: validar que sabemos correr el pipeline, y ver qué criterios usaron
   quienes las diseñaron.
6. Cómo las aprovechamos. Esta es la sección que le importa al equipo: ¿sirven
   como conjunto de validación para un método nuestro, como ejemplos positivos
   para entrenar o calibrar un scoring, como punto de partida para optimizar,
   como caso de estudio para ingeniería inversa de los criterios de diseño?
   Para cada opción, qué haría falta y qué tan factible es.
</alcance>

<fuera_de_alcance>
No propongas modificaciones orientadas a aumentar virulencia, transmisibilidad o
rango de hospedadores, ni diseños dirigidos a organismos no objetivo. El trabajo
es caracterización y control fitosanitario.
</fuera_de_alcance>

<salida>
En research/ola2/W5_secuencias_epilab/:
1. REPORT.md — en prosa, con las seis secciones del alcance. La sección 6 va
   resumida también en la primera página.
2. secuencias.json — id, archivo, largo, tipo, gc, organismo_identificado,
   gen_identificado, metodo_de_identificacion, confianza (alta|media|baja),
   estructura (objeto con ΔG si se calculó), offtargets (resumen).
3. analisis/ — los comandos y las salidas reales de cada análisis que corriste.
4. aprovechamiento.md — las opciones de uso de la sección 6, cada una con qué
   requiere, qué demuestra y qué riesgo tiene.
5. index.html autocontenido con el inventario y las caracterizaciones. Mismas
   restricciones visuales que el resto del proyecto.

Las secuencias en sí no se copian a los reportes ni al HTML más allá de lo
mínimo necesario para ilustrar algo: los archivos originales ya están en el
repo.
</salida>

<verificacion>
- ¿Se respetó la regla de confidencialidad en todos los análisis? Dejá
  constancia de qué herramienta se corrió localmente.
- ¿Cada identificación tiene su método y su nivel de confianza, sin suposiciones
  presentadas como hechos?
- ¿La sección de aprovechamiento es concreta y factible para 4 personas en el
  plazo del evento?
</verificacion>

<terminacion>
Los cinco entregables existen y completos. Cuando esté hecho y verificado, pará
y reportá. No diseñes secuencias nuevas: no está pedido en esta ola.
</terminacion>
```

---

# PARTE 3 — Configuración

**Modelos.** Sonnet 5.5 para los cinco subagentes, como pediste: es buena elección para trabajo acotado y bien especificado, que es exactamente lo que son W1–W5. Para el orquestador conviene dejar Opus 5.5, porque la fase 2 —reconciliar cinco reportes nuevos contra cinco viejos y re-priorizar la cartera— es el tipo de trabajo largo y conectado donde la propia guía de Anthropic recomienda un modelo Opus.

**Effort.** En Sonnet 5.5 los niveles están recalibrados y no equivalen a los de Sonnet 5. Para trabajo agéntico bien especificado la guía sugiere arrancar en `medium` y subir a `high` para lo más largo o difícil. Traducido a esta ola: `high` para W1 (leer y triar todo el corpus) y W5 (caracterización de secuencias, donde un error se propaga); `medium` para W2, W3 y W4. Si ves que alguno corta antes de terminar, el primer movimiento es subir el effort, no agregar instrucciones.

**Dos cosas que ya están en los prompts y conviene que sepas por qué.** En `low` y `medium`, Sonnet 5.5 tiende a parar a consultarte antes de terminar una tarea multiparte; por eso cada sub-prompt lleva la instrucción de llevar el trabajo hasta el final y parar solo ante un bloqueo real. Y en todos los niveles tiende a agregar archivos, tests y documentación que no pediste, así que cada sub-prompt cierra diciendo que al terminar pare y reporte, y que lo que le parezca buena idea lo diga en vez de hacerlo. Sin eso, volvés y tenés tres scripts de utilidad que nadie pidió.

**Verificación de corridas.** W2, W3 y W4 ejecutan herramientas. La guía de Sonnet 5.5 marca que en effort bajo a veces reporta algo como hecho sin correr una verificación real, así que los tres prompts incluyen la instrucción de correr un chequeo que ejercite el cambio, instalar dependencias con el gestor del propio proyecto y nunca con sudo, y declarar explícitamente lo que no se pudo ejecutar.

**Clasificador de biología.** Sonnet 5.5 corre clasificadores de seguridad, incluido uno de biología. Este trabajo es control fitosanitario con material provisto por un programa académico y no debería activarlo; por eso W2 y W5 llevan su sección de fuera de alcance explícita. Si aparece un rechazo, se registra y se sigue por otra vía, no se reformula para esquivarlo.

**Permisos.** Los subagentes necesitan lectura y escritura en el repo, ejecución de comandos (instalar dependencias, correr las herramientas), WebSearch y WebFetch. Si vas a dejarlo corriendo sin mirar, preaprobá eso para que no se frene.
