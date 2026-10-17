# Investigathon Y-Hat (UBA) — Track chicharrita / RNAi
## Prompt orquestador para Claude Code + sub-prompts de investigación

> **Cómo usar este archivo**
> 1. Creá el repo vacío (`mkdir chicharrita-research && cd chicharrita-research && git init`).
> 2. Copiá la **PARTE 0** a `CLAUDE.md` en la raíz.
> 3. Pegá la **PARTE 1** como primer mensaje de la sesión principal de Claude Code. Ese prompt ya contiene las instrucciones para lanzar las 5 investigaciones en paralelo.
> 4. La **PARTE 2** son los 5 sub-prompts completos. El orquestador los usa; también podés pegar cualquiera suelto en una sesión/worktree independiente.
> 5. La **PARTE 3** es configuración recomendada (modelo, effort, permisos).

---

# PARTE 0 — `CLAUDE.md` del repositorio

```markdown
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
  - `[E]` establecido: consenso en literatura revisada por pares.
  - `[R]` reportado: una o pocas fuentes, preprint, nota técnica, patente, web de empresa.
  - `[H]` hipótesis nuestra: idea del equipo, todavía sin respaldo.
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
```

---

# PARTE 1 — Prompt orquestador (pegar en la sesión principal)

```text
Sos el orquestador de la investigación previa de nuestro equipo para el
Investigathon de Y-Hat (UBA). Te doy la tarea completa de una sola vez: armá el
repositorio de conocimiento, lanzá las cinco investigaciones en paralelo y
consolidá los resultados. No me pidas aprobación para empezar.

<contexto>
Equipo: 4 estudiantes de tercer año de Ingeniería en IA (UdeSA). Cero laboratorio
húmedo, cero formación formal en biología. Ventaja comparativa: bioinformática y
datos, desarrollo computacional, innovación abierta. La estrategia del equipo es
NO competir en el eje "biología y evidencia experimental" sino en esos tres ejes.

Pregunta del track, textual:
"¿Cómo diseñar y priorizar una solución basada en la aplicación de ARN exógeno
que utilice el mecanismo de RNAi para silenciar genes del vector y/o de los
patógenos asociados, de manera biológicamente informada y reproducible, con
mayor probabilidad de acción y menor riesgo para el maíz, los organismos no
objetivo y el ecosistema?"

Lo que contó el investigador invitado (notas del equipo, segunda mano, VERIFICAR
todo):
- Una startup argentina, posiblemente "Apolo Biotech", trabaja el problema con
  una selección de ARN de doble cadena —aparentemente no codificantes y también
  exógenos— que atacan al insecto y al virus vía silenciamiento génico.
- Un segundo enfoque que probaron: mejorar la planta, seleccionando marcadores
  genéticos donde el ARN activa las defensas del maíz.
- Se mencionaron cuatro patógenos. Los dos que más pesan económicamente serían
  un fitoplasma (afectaría la cantidad de granos por mazorca) y
  *Spiroplasma kunkelii* (afectaría el crecimiento/altura del tallo).
- Las herramientas que usan para encontrar genes candidatos corren BLAST,
  separando por sectores y mirando termodinámica.

<supuestos_a_verificar>
Lo siguiente es conocimiento de partida SIN VERIFICAR. Tratalo como hipótesis a
confirmar o refutar con fuentes, nunca como hecho establecido. Si algo resulta
falso, corregilo explícitamente en el reporte y en el glosario.

S1. El vector sería *Dalbulus maidis*, y el cuadro se conoce como "complejo de
    achaparramiento del maíz" (corn stunt). Los patógenos asociados serían
    *Spiroplasma kunkelii*, un fitoplasma del grupo *Candidatus* Phytoplasma
    asteris (maize bushy stunt) y el virus del rayado fino del maíz (MRFV),
    posiblemente con un cuarto agente. Confirmar nombres, cuál causa qué
    síntoma y el daño económico atribuible a cada uno por separado.
S2. Hay una confusión probable en las notas del equipo: BLAST es un algoritmo de
    alineamiento local de secuencias (seed-and-extend, E-value, bit score); no
    calcula termodinámica. En los pipelines de diseño de dsRNA conviven dos
    cosas distintas: (a) alineamiento tipo BLAST/Bowtie contra transcriptomas,
    que se usa sobre todo para el tamizaje de off-targets y para elegir regiones
    conservadas en el objetivo, y (b) termodinámica de hibridación y estructura
    secundaria (ΔG, accesibilidad del sitio blanco, asimetría termodinámica de
    los extremos para la selección de la hebra guía), que se calcula con
    herramientas tipo ViennaRNA/RNAfold/RNAup. Verificá esto y dejá la
    distinción escrita con precisión en el glosario: es la base de dos de
    nuestros enfoques.
S3. "ARN de doble cadena no codificante" probablemente mezcla dos conceptos
    distintos (dsRNA aplicado exógenamente para disparar RNAi, y ARN largo no
    codificante como clase funcional). Desambiguar.
</supuestos_a_verificar>
</contexto>

<objetivo>
Dejar al equipo, antes de que nos entreguen las herramientas, bases de datos y
bibliografía oficiales del Investigathon, con:
1. Entendimiento real del dominio, no superficial.
2. Un mapa del estado del arte y de lo que ya hace la industria.
3. Tres o cuatro enfoques candidatos nuestros, evaluados y priorizados, con sus
   riesgos y lo que haría falta para ejecutarlos.
4. Una memoria del proyecto que sobreviva a esta sesión: glosario, decisiones,
   caminos probados y preguntas abiertas.
</objetivo>

<plan_de_ejecucion>
Paso 1. Creá la estructura del repositorio:

chicharrita-research/
├── CLAUDE.md                     (ya existe; leelo antes de nada)
├── README.md                     (qué es el proyecto, cómo navegarlo)
├── index.html                    (portada que linkea los 5 reportes; va al final)
├── SINTESIS.md                   (va al final)
├── 00_meta/
│   ├── GLOSARIO.md
│   ├── DECISIONS.md
│   ├── CAMINOS_PROBADOS.md
│   ├── PREGUNTAS_ABIERTAS.md
│   └── FUENTES.md
└── research/
    ├── R1_fundamentos/
    ├── R2_attention_diseno_arn/
    ├── R3_apolo_biotech/
    ├── R4_frontier_ml_rna/
    └── R5_metodologias_ejes/

Cada carpeta de research/ termina conteniendo: REPORT.md, index.html,
sources.json, y notes/ con lo que haga falta.

Paso 2. Lanzá CINCO subagentes en paralelo, uno por investigación, usando los
prompts de la sección <sub_prompts>. Pasá a cada uno su prompt completo y
textual: cada sub-prompt es autosuficiente y el subagente no ve esta
conversación. Exactamente cinco: no agregues subagentes extra para tareas que
podés hacer vos directamente, y no partas una investigación en varias.
Cada subagente puede, si lo necesita, delegar como mucho una búsqueda acotada.

Paso 3. Mientras corren, preparás el esqueleto de 00_meta/ con las entradas
iniciales del glosario que ya podés escribir, y el README.

Paso 4. A medida que vuelven los subagentes, integrás:
- Fusionás los glosarios parciales en 00_meta/GLOSARIO.md sin duplicados y
  resolviendo definiciones en conflicto (si dos agentes definen distinto el
  mismo término, lo marcás `[?]` y lo anotás en PREGUNTAS_ABIERTAS.md).
- Consolidás todas las fuentes en 00_meta/FUENTES.md.
- Anotás en DECISIONS.md las decisiones de alcance que tomaste vos.

Paso 5. Escribís SINTESIS.md, que es el entregable que lee el equipo. Contiene:
(a) qué sabemos ahora que no sabíamos, en prosa, media carilla;
(b) los supuestos S1–S3 resueltos: cuáles se confirmaron, cuáles no y qué
    corrige la evidencia;
(c) la cartera de enfoques candidatos, priorizados con una matriz explícita de
    impacto esperado × factibilidad para 4 personas sin laboratorio ×
    diferenciación frente a lo que ya hace la industria × riesgo;
(d) una propuesta de reparto: qué toma cada uno de los 4 integrantes, en
    paralelo, y cuál es el entregable de cada rama al cierre del Investigathon;
(e) las preguntas concretas para hacerle al investigador y los datos que hay que
    pedir el día que nos den acceso a las herramientas.

Paso 6. Construís index.html en la raíz: portada que linkea los cinco reportes
con un párrafo de resumen de cada uno y la matriz de priorización.
</plan_de_ejecucion>

<formato_de_los_html>
Cada index.html es un único archivo autocontenido, sin build, que abre con
doble clic y se lee bien en celular. HTML y CSS a mano; JavaScript solo si
agrega algo real (filtros, tabs, una tabla ordenable). Nada de dependencias
externas salvo, si hace falta un gráfico, una librería por CDN.

No uses: fondo crema u off-white, palabras en itálica como acento en los
títulos, numeración de secciones tipo "01 / 02 / 03", etiquetas en monoespaciada
sobre los encabezados, botones tipo píldora, gradientes violetas sobre blanco,
tarjetas con sombra difusa en grilla de tres. Elegí una tipografía con carácter,
una paleta propia y comprometete con ella; definí los colores como variables CSS
y soportá modo oscuro con prefers-color-scheme.

El HTML es la vista de lectura; REPORT.md es la fuente de verdad y lleva el
contenido completo. El HTML puede resumir, pero no puede afirmar nada que no
esté en el REPORT.md con su fuente.
</formato_de_los_html>

<reglas_de_evidencia>
Rigen las de CLAUDE.md, y además:
- Buscá en inglés y en español. Para este cultivo y esta plaga, la literatura
  argentina y brasileña (INTA, CONICET, EMBRAPA, congresos de Maizar) es
  primaria, no secundaria.
- Priorizá: papers revisados por pares > preprints (bioRxiv) > patentes y
  documentos regulatorios > notas técnicas institucionales > prensa
  especializada > comunicación corporativa. Marcá el nivel de cada una.
- Cuando dos fuentes se contradicen, reportá las dos y marcá `[?]`. No promedies
  ni elijas la más cómoda.
- sources.json: lista de objetos con id, titulo, autores, anio, venue, url, tipo,
  nivel_evidencia, acceso (abierto|paywall|no_accesible), y para qué afirmación
  del reporte se usó.
</reglas_de_evidencia>

<definicion_de_hecho>
La tarea está terminada cuando, y solo cuando:
1. Las cinco carpetas de research/ tienen REPORT.md, index.html y sources.json,
   y ningún REPORT.md tiene secciones vacías o marcadores de relleno.
2. 00_meta/ tiene los cinco archivos poblados, con el glosario cubriendo como
   mínimo: ADN, ARN, ARNm, dsRNA, siRNA, miRNA, ARN no codificante, RNAi, RISC,
   Argonaute, Dicer, ARN exógeno, SIGS, HIGS, silenciamiento transcripcional vs
   post-transcripcional, off-target, BLAST, E-value, ΔG de hibridación,
   accesibilidad del sitio blanco, asimetría termodinámica, vector, fitoplasma,
   espiroplasma, transmisión persistente propagativa.
3. Los supuestos S1, S2 y S3 están resueltos explícitamente en SINTESIS.md.
4. SINTESIS.md tiene la cartera priorizada con la matriz y el reparto para 4
   personas.
5. index.html de la raíz abre y linkea los cinco reportes.
6. git log muestra un commit por investigación integrada más uno final.
</definicion_de_hecho>

<como_terminar_los_turnos>
Esto corre sin que yo esté mirando. Un mensaje sin llamada a herramienta corta
el turno y la tarea se frena ahí. No quiero que termines un turno de estas
cuatro maneras, con trabajo todavía pendiente: (1) un resumen largo de lo hecho
que cierra anunciando el próximo paso y no lo arranca; (2) un ofrecimiento a
seguir salvo que yo prefiera otra cosa; (3) una lista de decisiones para mí
cuando, por tu propia descripción, ninguna bloquea el resto del trabajo; (4)
cortar porque el turno viene largo o porque cerraste un hito. Las notas de
estado son bienvenidas: mandalas en el mismo mensaje que tu siguiente llamada a
herramienta y seguí con todo lo que no dependa de mi respuesta. Si un subagente
sigue corriendo, la tarea no está terminada: esperá su salida e integrala.
Las únicas paradas que quiero son las que nada puede avanzar sin mí.
Mantené la lista de tareas actualizada y chequeada contra la
<definicion_de_hecho> antes de cerrar.
</como_terminar_los_turnos>

<sub_prompts>
[Pegar acá los cinco bloques R1 a R5 de la PARTE 2 de este archivo]
</sub_prompts>
```

---

# PARTE 2 — Los cinco sub-prompts

Cada uno es autosuficiente: asume que el subagente no vio nada más. Si los corrés en sesiones o worktrees separados, pegá antes el bloque `<contexto>` y `<supuestos_a_verificar>` de la PARTE 1.

---

## R1 — Fundamentos del dominio

```text
<rol>
Investigás y escribís el documento de fundamentos que va a usar un equipo de 4
ingenieros en IA, sin formación en biología, para trabajar sobre control de la
chicharrita del maíz mediante ARN exógeno. El lector es técnicamente fuerte pero
biológicamente nuevo: podés asumir álgebra lineal, probabilidad, estructuras de
datos y optimización; no podés asumir nada de biología molecular.
</rol>

<objetivo>
Que después de leer el documento, cualquiera del equipo pueda sostener una
conversación técnica con el investigador del track sin perderse, y pueda
evaluar si una idea computacional nuestra tiene sentido biológico o no.
</objetivo>

<alcance>
Cubrí, en este orden, construyendo cada concepto sobre el anterior:

1. Base molecular. ADN, ARN, transcripción, traducción, qué es un gen y qué es
   un transcrito. ARNm frente a ARN no codificante; dentro de los no
   codificantes, miRNA, siRNA, lncRNA y qué los distingue funcionalmente.
   Qué es ARN de doble cadena y por qué una célula lo trata distinto al simple.

2. El mecanismo de RNAi, con precisión. Dicer, el cargado en RISC, Argonaute,
   selección de la hebra guía, corte del transcrito objetivo, silenciamiento
   post-transcripcional frente a transcripcional. Amplificación por RdRP y
   silenciamiento sistémico: dónde existe y dónde no (plantas, nematodos,
   insectos: esto no es uniforme y es decisivo para nuestro problema).
   Qué significa "ARN exógeno" y por qué aplicar dsRNA desde afuera puede
   disparar la maquinaria endógena.

3. El sistema patógeno. El vector *Dalbulus maidis*: biología, ciclo, cómo se
   alimenta, cómo adquiere y transmite, qué significa transmisión persistente
   propagativa y por qué cambia las opciones de intervención. Los patógenos del
   complejo de achaparramiento: identificá cuáles son con certeza, qué tipo de
   organismo es cada uno (mollicute sin pared celular, virus, etc.), dónde vive
   dentro de la planta y dentro del insecto, qué síntoma causa cada uno y qué
   pérdida de rendimiento se le atribuye. Verificá específicamente: cuál afecta
   granos por mazorca y cuál afecta crecimiento del tallo, o si esa asignación
   es incorrecta.

4. Por qué estos patógenos son blancos difíciles. Un mollicute sin pared y un
   virus no responden igual a RNAi que un insecto. ¿Hay evidencia de RNAi
   funcional en bacterias/mollicutes? Si no la hay, ¿qué implica eso para la
   estrategia "silenciar al patógeno" frente a "silenciar al vector" frente a
   "preparar la defensa de la planta"? Esta es la pregunta más importante de
   todo el documento: respondela con evidencia, no con plausibilidad.

5. Tratamientos existentes, con y sin ARN. Insecticidas y manejo del vector;
   resistencia y tolerancia genética del maíz; manejo cultural (fecha de
   siembra, maíz guacho, refugios); control biológico. Y del lado del ARN:
   SIGS (spray-induced gene silencing), HIGS (host-induced), VIGS, dsRNA
   formulado, nanopartículas y portadores, plantas transgénicas que expresan
   dsRNA. Para cada uno: nivel de madurez, evidencia de eficacia a campo, costo
   relativo, estado regulatorio.

6. Diseño de dsRNA como problema de ingeniería. Qué define un buen candidato:
   elección del gen blanco, región del transcrito, largo, conservación entre
   poblaciones del objetivo, accesibilidad estructural del sitio, asimetría
   termodinámica para que se cargue la hebra correcta, ausencia de coincidencias
   en organismos no objetivo. Qué herramientas se usan realmente (nombrá
   software concreto: BLAST, Bowtie, ViennaRNA/RNAfold/RNAup, si-Fi21, pssRNAit,
   dsRNAEngineer u otras que encuentres) y qué calcula cada una.

<correccion_a_verificar>
Las notas del equipo dicen que "BLAST separa en porciones y calcula la
termodinámica". Probablemente sea un malentendido: BLAST es alineamiento local
de secuencias (seed-and-extend, E-value, bit score), y la termodinámica (ΔG,
estructura secundaria, accesibilidad) se calcula con otras herramientas.
Verificalo y dejá la distinción explicada con precisión y con fuentes: dos de
los enfoques del equipo dependen de entender bien esta separación.
</correccion_a_verificar>

<fuera_de_alcance>
No produzcas información que sirva para aumentar la virulencia, la
transmisibilidad o el rango de hospedadores de ningún patógeno, ni protocolos de
síntesis o producción de agentes biológicos. El documento es de control
fitosanitario, con literatura publicada.
</fuera_de_alcance>

<fuentes>
Papers revisados por pares primero; reviews recientes de RNAi en protección de
cultivos para el marco general, y trabajos específicos de *Dalbulus maidis* y
del complejo de achaparramiento para el sistema particular. La literatura
argentina y brasileña (INTA, CONICET, EMBRAPA) es primaria acá, no secundaria.
Buscá en inglés y en español. No cites nada que no hayas abierto.
Etiquetá cada afirmación como [E] establecido, [R] reportado, [H] hipótesis o
[?] incierto.
</fuentes>

<salida>
En research/R1_fundamentos/:

1. REPORT.md — prosa técnica, no listas de bullets. Apuntá a un documento que se
   lea de corrido en 30-40 minutos y se pueda consultar después. Secciones según
   los seis puntos del alcance. Cada número y cada afirmación no trivial con su
   cita. Cerrá con "Lo que esto implica para nuestro proyecto": media carilla
   que traduzca la biología a restricciones de diseño para gente de IA.

2. glosario_parcial.md — todos los términos que usaste, con definición de una
   línea y por qué nos importa.

3. sources.json — id, titulo, autores, anio, venue, url, tipo, nivel_evidencia,
   acceso, y para qué afirmación se usó.

4. index.html — versión navegable del reporte, un archivo autocontenido, legible
   en celular, con índice lateral o superior y una figura o diagrama hecho en
   SVG o CSS del mecanismo de RNAi y otra del ciclo vector-patógeno-planta.
   No uses: fondo crema, acentos en itálica en los títulos, numeración "01/02/03",
   etiquetas en monoespaciada, botones píldora, gradientes violetas sobre blanco.

5. preguntas_abiertas.md — lo que no pudiste resolver y lo que habría que
   preguntarle al investigador.
</salida>

<verificacion>
Antes de cerrar, revisá el REPORT.md contra esta lista:
- ¿Cada número tiene fuente y contexto experimental?
- ¿Está respondida con evidencia la pregunta de si el RNAi funciona sobre
  mollicutes y virus, o solo sobre el insecto y la planta?
- ¿Alguien sin biología entiende cada párrafo sin googlear un término que no
  está en el glosario?
- ¿Quedó corregido o confirmado el punto de BLAST y termodinámica?
</verificacion>

<condicion_de_terminacion>
Los cinco archivos existen, completos, sin secciones vacías ni placeholders, y
la lista de verificación pasa entera. Si una pregunta del alcance no se pudo
responder con fuentes, eso se dice explícitamente en el reporte y se anota en
preguntas_abiertas.md: un vacío documentado es un resultado válido; un vacío
tapado con texto plausible, no.
</condicion_de_terminacion>
```

---

## R2 — Attention y modelos de secuencia para diseño de ARN

```text
<rol>
Evaluás y formalizás una idea del equipo, y la convertís en una propuesta
técnica ejecutable o en un descarte bien argumentado. El equipo es de
ingeniería en IA: podés usar todo el vocabulario de deep learning sin explicarlo,
y tenés que explicar la biología que toques.
</rol>

<idea_del_equipo_a_evaluar>
Textual, tal como la escribió uno de los integrantes, con sus dudas incluidas:

"Se me ocurrió un enfoque basado en la estructura de los LLMs y el mecanismo de
attention. Por lo que entendí, para ver si un ARN (o un gen, esta parte no la
terminé de entender) sirve, se usa el algoritmo de BLAST, donde se separa en
porciones y se calcula la termodinámica. Puede ser interesante, si pensamos a
estas porciones de ARN como tokens o parte del vocabulario del LLM, ver la
atención o relación entre las distintas secuencias. Esto se podría usar pensando
al output como el objetivo, dado cuál sería la secuencia que mejore la
respuesta. Como no sé mucho del tema, puede ser que no resulte. Además le falta
pulir cuál sería la loss, cómo se predeciría y qué se quiere predecir con ella.
Para la loss pensé en el factor de termodinámica que usa BLAST."

Tu trabajo no es validar esta idea ni demolerla: es ver qué parte se sostiene,
qué parte descansa en un malentendido, y qué queda cuando se la reformula con
rigor.
</idea_del_equipo_a_evaluar>

<objetivo>
Entregar una de dos cosas, la que la evidencia soporte:
(a) una especificación técnica de un método implementable por 4 personas en el
    plazo de un Investigathon, con datos que existan y sean accesibles; o
(b) un descarte argumentado, que explique exactamente dónde se rompe la idea, y
    qué se rescata de ella en una formulación distinta.
Un descarte bien fundamentado es un entregable tan válido como una propuesta.
</objetivo>

<alcance>
1. Desarmá el malentendido de base. BLAST es alineamiento local de secuencias
   (seed-and-extend, E-value, bit score); no calcula termodinámica. La
   termodinámica de hibridación y estructura secundaria (ΔG, accesibilidad del
   sitio blanco, asimetría de extremos) la calculan herramientas tipo
   ViennaRNA/RNAfold/RNAup. Documentá qué hace cada una, con qué entrada y qué
   salida, y cuál de las dos es realmente la señal útil para seleccionar un
   dsRNA. Esto redefine la "loss" que proponía la idea original.

2. Estado del arte de lo que la idea reinventa. Investigá y reportá:
   - Modelos de lenguaje de ácidos nucleicos: Nucleotide Transformer, DNABERT,
     RNA-FM, RiNALMo, Evo y los que encuentres. Qué tokenización usan (bases,
     k-mers, BPE), con qué objetivo se preentrenaron, qué tareas downstream
     resuelven bien y con qué datos.
   - Predicción de eficacia de siRNA/dsRNA con aprendizaje automático: qué
     modelos existen, con qué datasets se entrenaron (tamaño, especie,
     condiciones), qué métricas reportan y qué tan transferibles son entre
     especies. Prestá atención específica a si existe algo para insectos, y no
     solo para líneas celulares humanas.
   - Predicción de off-target basada en aprendizaje, más allá del alineamiento.
   - Si ya existe un método publicado que hace lo que propone la idea del
     equipo, decilo de entrada y claramente. Reinventar algo publicado no es
     innovación; partir de ahí y mejorarlo, sí.

3. Reformulación rigurosa. Planteá el problema como lo que realmente es:
   optimización multiobjetivo sobre el espacio de secuencias candidatas, con un
   scoring que combine al menos eficacia de knockdown predicha, penalidad por
   off-target en maíz y en no-objetivo, restricciones termodinámicas y de
   accesibilidad, y conservación entre poblaciones del blanco. Para cada
   término: cómo se calcula, qué datos necesita y qué tan confiable es.
   Después evaluá, para cada opción, factibilidad real:
   - Scoring con modelo preentrenado congelado (embeddings + cabezal liviano).
   - Fine-tuning de un modelo de secuencia sobre datos de eficacia de RNAi.
   - Búsqueda sobre el espacio de secuencias (algoritmo genético, búsqueda
     guiada por gradiente, muestreo) usando el score como objetivo.
   - Usar los pesos de atención como herramienta de interpretabilidad para
     identificar regiones del transcrito, que es probablemente lo más cercano a
     la intuición original. Advertencia que tenés que investigar y reportar:
     interpretar pesos de atención como relación causal es discutido en la
     literatura. Reportá esa discusión con fuentes, no de memoria.

4. Datos. La pregunta que mata o salva el proyecto. ¿Qué datos existen,
   públicos y descargables, para entrenar o validar algo de esto? Genoma y
   transcriptoma de *Dalbulus maidis* y de especies emparentadas, genomas de los
   patógenos, datasets de eficacia de RNAi en insectos, bases de off-target.
   Dejá URLs concretas, tamaños aproximados, formatos y licencias. Si el dato
   necesario no existe públicamente, eso es el hallazgo central del reporte y
   hay que decirlo en la primera página.

5. Plan de validación sin laboratorio. Cómo demostraríamos que el método sirve,
   sin poder hacer un solo experimento húmedo: validación retrospectiva contra
   resultados publicados, held-out por especie, comparación contra el baseline
   de las herramientas de diseño que ya existen, ablaciones. Definí la métrica
   de éxito antes de proponer el método.

<fuera_de_alcance>
No produzcas secuencias ni diseños que apunten a aumentar virulencia,
transmisibilidad o rango de hospedadores, ni nada que apunte deliberadamente a
organismos no objetivo. El trabajo es metodológico y de control fitosanitario.
</fuera_de_alcance>

<salida>
En research/R2_attention_diseno_arn/:
1. REPORT.md con las cinco secciones, en prosa. Primera página: veredicto en
   tres párrafos, antes de cualquier desarrollo.
2. PROPUESTA.md: si el veredicto es viable, la especificación — datos, modelo,
   objetivo de entrenamiento, baselines, métricas, plan de validación,
   estimación de esfuerzo en días-persona, riesgos ordenados por probabilidad de
   hundir el proyecto. Si el veredicto es no viable, el argumento del descarte y
   qué se rescata.
3. datos_disponibles.md: tabla de datasets con URL, tamaño, formato, licencia,
   para qué sirve, y qué falta.
4. sources.json
5. index.html autocontenido con el veredicto arriba, un diagrama del pipeline
   propuesto y la tabla de datos. Mismas restricciones visuales que el resto del
   proyecto: nada de fondo crema, acentos en itálica en títulos, numeración
   "01/02/03", etiquetas monoespaciadas, botones píldora ni gradientes violetas.
</salida>

<verificacion>
- ¿El veredicto está en la primera página y es inequívoco?
- ¿Cada afirmación sobre un modelo publicado tiene cita de la fuente abierta?
- ¿Cada dataset listado tiene URL verificada, o está marcado como no verificado?
- ¿La propuesta es ejecutable por 4 personas en el plazo, o es un plan de tesis
  disfrazado? Si es lo segundo, decilo y recortá.
</verificacion>

<condicion_de_terminacion>
Los cinco archivos existen y completos, y el veredicto está tomado: viable con
especificación, o descartado con argumento. "Habría que investigar más" no es un
veredicto.
</condicion_de_terminacion>
```

---

## R3 — Apolo Biotech y el panorama industrial

```text
<rol>
Hacés inteligencia competitiva y técnica sobre una empresa y su sector, para un
equipo que va a presentar una propuesta en un Investigathon donde el investigador
invitado viene de esa empresa. El objetivo no es halagar ni criticar: es que el
equipo sepa exactamente qué ya está hecho, para no proponerlo como novedad, y
dónde quedan huecos reales.
</rol>

<sujeto>
Apolo Biotech, startup de biotecnología aplicada al agro, presumiblemente
argentina. LinkedIn de referencia que nos pasaron:
https://www.linkedin.com/company/apolo-biotech/
Si el nombre no coincide o hay más de una empresa similar, identificá cuál es la
correcta por su trabajo en ARN aplicado a cultivos y decilo explícitamente.
Pista sin verificar: podría estar vinculada a investigación del CONICET sobre
ARN no codificante. Verificar, no asumir.
</sujeto>

<alcance>
1. Qué es la empresa. Fundación, fundadores y su background académico, vínculos
   institucionales (CONICET, universidades, INTA), financiamiento, tamaño,
   mercados donde opera, estado regulatorio de sus productos.

2. Qué hacen técnicamente, con el mayor detalle que permita la información
   pública. Qué tipo de moléculas de ARN usan, contra qué objetivos, en qué
   cultivos y contra qué plagas o patógenos. Cómo producen el ARN a escala
   (fermentación bacteriana, síntesis in vitro, otro) y qué dice eso sobre el
   costo por hectárea.

3. Formas de aplicación, con prioridad. Esta sección es la más importante para
   nosotros, porque el modo de aplicación es uno de los ejes donde nuestro
   equipo podría aportar. Pulverización foliar, tratamiento de semilla,
   aplicación al suelo, inyección, riego, portadores y nanopartículas,
   formulaciones que protegen el ARN de la degradación por UV y nucleasas.
   Para cada modo: evidencia de eficacia, persistencia del efecto, número de
   aplicaciones por campaña, limitaciones conocidas. Incluí también lo que haga
   el resto de la industria, no solo esta empresa: Greenlight Biosciences,
   Bayer, Syngenta, Renaissance BioScience, GreenVenus y quien encuentres.

4. Metodología de validación. Cómo pasan de un candidato a un tratamiento
   probado: selección del gen blanco, tamizaje in vitro, bioensayos, ensayos de
   invernáculo, ensayos a campo, diseño experimental y métricas, evaluación de
   organismos no objetivo, trámite regulatorio. Reconstruí el embudo con la
   mayor fidelidad posible y marcá qué partes son explícitas en fuentes y cuáles
   inferiste. Este embudo es lo que nuestra propuesta computacional tiene que
   poder alimentar: si no sabemos qué consume la empresa como entrada, cualquier
   herramienta que propongamos cae al vacío.

5. Trabajo específico sobre la chicharrita y el complejo de achaparramiento.
   ¿Hay algo publicado, anunciado, patentado o en ensayo? Buscá patentes
   (Google Patents, INPI, WIPO), registros de ensayos, presentaciones a
   congresos, notas de prensa agropecuaria argentina.

6. Huecos. Cerrá con lo que la industria no está resolviendo: qué parte del
   problema queda sin cubrir, dónde el cuello de botella es computacional o de
   datos y no biológico, y qué podría aportar un equipo de ingeniería en IA sin
   laboratorio. Sé concreto y honesto: si el cuello de botella es puramente
   experimental y de capital, decilo.

<reglas>
- Distinguí siempre entre lo que la empresa afirma de sí misma y lo que está
  validado por terceros o por literatura revisada. Marcá cada afirmación como
  [E], [R] o [?]. El material de marketing es evidencia de intención, no de
  eficacia.
- Fuentes posibles: sitio de la empresa, LinkedIn, patentes, papers de sus
  fundadores, prensa agropecuaria (Clarín Rural, La Nación Campo, Infocampo,
  Bichos de Campo), bases regulatorias (SENASA, CONABIA), registros de
  financiamiento.
- No infieras cifras de negocio que no estén publicadas. Si no hay dato, el dato
  es que no hay dato.
- Nada de información personal más allá de la trayectoria profesional pública de
  fundadores y referentes técnicos.
</reglas>

<salida>
En research/R3_apolo_biotech/:
1. REPORT.md con las seis secciones, en prosa.
2. embudo_validacion.md: el proceso de validación reconstruido paso a paso, con
   entradas y salidas de cada etapa, marcando qué está documentado y qué es
   inferencia nuestra.
3. panorama_industria.md: tabla comparativa de empresas con tecnología, cultivos,
   plagas objetivo, modo de aplicación y estado regulatorio.
4. sources.json
5. index.html autocontenido, con una línea de tiempo de la empresa y el diagrama
   del embudo de validación. Mismas restricciones visuales que el resto del
   proyecto.
</salida>

<verificacion>
- ¿Quedó confirmada la identidad de la empresa, o marcada la ambigüedad?
- ¿Cada afirmación sobre su tecnología distingue fuente propia de fuente externa?
- ¿La sección de huecos es específica y honesta, o es una lista de deseos?
</verificacion>

<condicion_de_terminacion>
Los cinco archivos existen y completos. Si la información pública es escasa,
eso se reporta como hallazgo con lo que sí se encontró, y las preguntas que
quedan van a preguntas_abiertas.md para hacérselas al investigador en persona.
</condicion_de_terminacion>
```

---

## R4 — Frontera de ML y modelos de lenguaje en biotecnología de ARN

```text
<rol>
Hacés el relevamiento de estado del arte en la intersección entre aprendizaje
automático y biotecnología de ARN, para un equipo de ingeniería en IA que tiene
que proponer un método en un Investigathon sobre control de plagas vía RNAi.
Este es el eje donde el equipo tiene su mayor ventaja comparativa, así que el
relevamiento tiene que ser profundo y actual, no un resumen de divulgación.
</rol>

<objetivo>
Un mapa de la frontera que permita decidir, con fundamento, en qué subcampo
conviene pararse, y que sirva de respaldo a la metodología que el equipo proponga.
</objetivo>

<alcance>
1. Modelos fundacionales de secuencias biológicas. Para cada uno que incluyas:
   arquitectura, datos y escala de preentrenamiento, objetivo de entrenamiento,
   tokenización, tareas donde se evaluó, disponibilidad de pesos y licencia.
   Cubrí al menos la familia de modelos de ADN/ARN (Nucleotide Transformer,
   DNABERT y sucesores, RNA-FM, RiNALMo, Evo y lo que haya salido después) y
   mencioná los de proteínas solo en la medida en que su metodología sea
   transferible.

2. Predicción de estructura de ARN con aprendizaje profundo. Qué reemplaza, qué
   complementa y dónde todavía gana la termodinámica clásica. Esto importa
   directamente: la accesibilidad del sitio blanco es uno de los determinantes de
   la eficacia del dsRNA.

3. Aprendizaje automático aplicado específicamente a RNAi y diseño de dsRNA.
   Modelos de predicción de eficacia, modelos de off-target, herramientas de
   diseño asistido. Para cada uno: datos de entrenamiento, especies cubiertas,
   métricas reportadas, si el código y los datos son públicos, y qué tan bien
   generaliza fuera de su dominio de entrenamiento.

4. Modelos de lenguaje grandes como herramienta de trabajo en biotecnología:
   agentes de laboratorio, diseño asistido de experimentos, extracción de
   información desde literatura, generación de hipótesis, pipelines
   bioinformáticos manejados por LLM. Qué está publicado y evaluado, y qué es
   demostración sin evaluación seria.

5. Diseño generativo e inverso de secuencias funcionales. Qué funciona hoy, con
   qué garantías, qué requiere validación húmeda obligatoria.

6. Síntesis orientada a decisión. Terminá con tres o cuatro líneas de ataque
   posibles para nuestro problema, cada una con: qué modelo o técnica usa, qué
   datos necesita, si esos datos existen, qué se podría demostrar en el plazo del
   Investigathon, y cuál es el riesgo principal. Ordenalas por relación entre
   valor esperado y costo para un equipo de 4 personas sin laboratorio.

<reglas>
- Priorizá los últimos 24 meses, pero marcá los trabajos fundacionales
  anteriores que haga falta para entender el campo.
- Para cada método, buscá activamente su crítica: benchmarks independientes,
  réplicas fallidas, limitaciones reportadas. Un relevamiento que solo recoge
  los claims de los autores no sirve para tomar decisiones.
- Distinguí siempre: resultado validado experimentalmente, resultado solo
  computacional, demostración sin evaluación. Marcá [E], [R], [?].
- bioRxiv y arXiv valen, marcados como preprints.
- No cites nada que no hayas abierto.
</reglas>

<fuera_de_alcance>
Nada que apunte a aumentar virulencia, transmisibilidad o rango de hospedadores
de un patógeno, ni protocolos de producción de agentes biológicos. El
relevamiento es de métodos computacionales aplicados a protección de cultivos.
</fuera_de_alcance>

<salida>
En research/R4_frontier_ml_rna/:
1. REPORT.md con las seis secciones, en prosa.
2. modelos.json: catálogo estructurado con nombre, tipo, arquitectura, escala,
   datos, tareas, pesos disponibles (sí/no + URL), licencia, paper, fecha.
3. lineas_de_ataque.md: las tres o cuatro propuestas de la sección 6, cada una
   en una página, con datos requeridos, entregable demostrable, riesgo y
   estimación de esfuerzo.
4. sources.json
5. index.html autocontenido con el catálogo de modelos como tabla filtrable y
   una línea de tiempo del campo. Mismas restricciones visuales que el resto del
   proyecto.
</salida>

<verificacion>
- ¿Cada modelo del catálogo tiene paper abierto y verificado?
- ¿Cada línea de ataque dice explícitamente si los datos que necesita existen?
- ¿Hay al menos una crítica o limitación reportada por cada familia de métodos?
</verificacion>

<condicion_de_terminacion>
Los cinco archivos existen y completos, y lineas_de_ataque.md está priorizado
con criterio explícito, no como lista neutra.
</condicion_de_terminacion>
```

---

## R5 — Metodologías de los tres ejes y plan de ejecución

```text
<rol>
Diseñás el plan de trabajo del equipo para el Investigathon. El equipo son 4
estudiantes de Ingeniería en IA, sin laboratorio, que decidieron competir en los
ejes de bioinformática y datos, desarrollo computacional e innovación abierta,
en lugar del eje de biología y evidencia experimental.
</rol>

<objetivo>
Que el equipo llegue al día del evento con un método de trabajo definido por
eje, un reparto de roles, entregables concretos por rama y criterios de
evaluación claros. Nada de generalidades sobre "metodología ágil": esto tiene
que ser específico del problema del ARN exógeno contra la chicharrita.
</objetivo>

<alcance>
1. Eje bioinformática y datos. Cuál es la metodología real de un proyecto de
   este tipo: qué bases de datos se consultan y en qué orden (NCBI
   nucleotide/genome/SRA, VectorBase, Ensembl Plants, MaizeGDB, Rfam, UniProt,
   KEGG y las que encuentres), qué pipelines son estándar (descarga, control de
   calidad, ensamblado o mapeo, anotación, búsqueda de ortólogos, alineamiento,
   plegado), qué software concreto se usa en cada paso y qué formatos de archivo
   circulan. Qué se puede correr en una notebook y qué necesita cluster o nube.
   Qué entregable de esta rama sería defendible ante un jurado.

2. Eje desarrollo computacional. Qué tipo de artefacto conviene construir dado
   el plazo: una herramienta de scoring y priorización de candidatos, un
   pipeline reproducible, un dashboard de exploración, una API. Para cada
   opción: arquitectura mínima, stack, tiempo estimado, qué demuestra y qué
   riesgos tiene. Reproducibilidad como requisito explícito, porque la pregunta
   del track pide soluciones reproducibles: entornos, semillas, versionado de
   datos, contenedores, documentación.

3. Eje innovación abierta. Qué significa concretamente en este contexto: datos
   y código abiertos, licencias, ciencia ciudadana y recolección colaborativa de
   datos de campo, monitoreo participativo del vector, estándares e
   interoperabilidad, publicación de resultados negativos, modelos de
   colaboración público-privada entre INTA, universidades, startups y
   productores. Buscá antecedentes reales y evaluables en agro, no la teoría del
   concepto.

4. Cómo se evalúa una solución de este tipo. Construí, con fundamento en lo que
   pide la pregunta del track, una rúbrica de priorización: probabilidad de
   acción biológica, especificidad y riesgo de off-target, riesgo para no
   objetivo y ambiente, factibilidad técnica y de costo, reproducibilidad,
   viabilidad regulatoria, tiempo hasta demostración. Definí cómo se puntúa cada
   criterio, con qué evidencia, y cómo se combinan. Esta rúbrica es un entregable
   en sí mismo: es la respuesta directa a la palabra "priorizar" de la pregunta
   del track.

5. Plan para 4 personas. Reparto de roles, qué hace cada uno en paralelo, puntos
   de sincronización, dependencias entre ramas, plan de contingencia para el
   caso de que una rama se caiga. Qué se entrega y qué se presenta. Incluí un
   plan B explícito para el escenario más probable de fracaso: que no existan
   los datos necesarios para entrenar nada.

<reglas>
- Cada metodología que propongas tiene que estar respaldada por cómo lo hace
  gente real, con fuente: papers de metodología, documentación de herramientas,
  guías de consorcios, trabajos publicados que hayan seguido ese camino.
- Nada de recomendaciones genéricas de gestión de proyectos. Si una
  recomendación aplicaría igual a un proyecto de e-commerce, no va.
- Los tiempos estimados tienen que ser realistas para estudiantes de tercer año
  con cursada en paralelo.
</reglas>

<salida>
En research/R5_metodologias_ejes/:
1. REPORT.md con las cinco secciones, en prosa.
2. RUBRICA.md: la rúbrica de priorización completa, lista para aplicar, con
   criterios, escalas, evidencia requerida y método de combinación.
3. PLAN_EQUIPO.md: roles, ramas, cronograma, dependencias, entregables, plan B.
4. stack_bioinformatico.md: tabla de bases de datos y herramientas con para qué
   sirve cada una, URL, formato de entrada y salida, y si corre local o no.
5. sources.json
6. index.html autocontenido con la rúbrica como tabla interactiva y el plan de
   equipo como diagrama. Mismas restricciones visuales que el resto del proyecto.
</salida>

<verificacion>
- ¿Cada criterio de la rúbrica es puntuable con evidencia que podamos conseguir?
- ¿El plan de equipo asigna trabajo paralelo real, sin que tres personas esperen
  a la cuarta?
- ¿Existe el plan B escrito para el caso de que no haya datos?
</verificacion>

<condicion_de_terminacion>
Los seis archivos existen y completos, y la rúbrica es aplicable hoy a una
propuesta concreta sin tener que inventarle criterios.
</condicion_de_terminacion>
```

---

# PARTE 3 — Configuración recomendada

**Modelo y effort.** Opus 5.5 para el orquestador y los subagentes. El default de Opus 5.5 es `medium`, y según la guía de Anthropic iguala o supera a Opus 5 en `high` en tareas de código y de trabajo de conocimiento, con menos pasos y menos tokens. Arrancá en `medium`; subí a `high` solo para R2 y R4, que son los dos que más razonamiento sostenido piden. Evitá `max`: cuesta mucho más y la ganancia medida es marginal.

**Qué sacar de tu `CLAUDE.md` y de tus prompts guardados.** Opus 5.5 piensa siempre y decide solo cuánto. Cualquier línea del tipo "pensá cuidadosamente paso a paso", "razoná antes de responder" o "pensá bien antes de actuar" ya no suma y demora el arranque de la respuesta. Tampoco le pidas que escriba su razonamiento interno en el texto de la respuesta: ese pedido puede terminar en un rechazo de categoría `reasoning_extraction`. Pedir un resumen de lo que hizo y por qué eligió cada cosa sí está permitido, y es lo que hace el `DECISIONS.md`.

**Paralelismo y tiempo.** Los cinco subagentes corren en paralelo. Si querés que el conjunto termine antes, la guía de Opus 5.5 sugiere darle señal de tiempo transcurrido contra un presupuesto; en Claude Code el equivalente práctico es agregar al prompt del orquestador una línea del tipo "el tiempo importa: no gastes tiempo evitable, y cuanto antes llegues a un resultado correcto, mejor".

**Clasificador de biología.** Opus 5.5 corre clasificadores de seguridad, entre ellos uno de biología. Este proyecto es protección de cultivos con literatura pública y no debería activarlo, y por eso los sub-prompts incluyen explícitamente la sección de fuera de alcance: encuadrar el trabajo correctamente desde el principio evita fricción. Si aun así aparece un rechazo, lo correcto es registrarlo y seguir por otra línea, no reformular para esquivarlo.

**Permisos.** Los subagentes necesitan WebSearch y WebFetch, lectura y escritura dentro del repo, y git. No necesitan nada más. Si vas a dejar la sesión corriendo sin mirar, conviene preaprobar esas herramientas para que no se frene esperando confirmación.

**Worktrees.** Si preferís aislamiento real en vez de subagentes dentro de una sesión, corré cada bloque R1–R5 en su propio `git worktree` y después mergeá a `main`; el orquestador hace entonces solo los pasos 1, 4, 5 y 6.
