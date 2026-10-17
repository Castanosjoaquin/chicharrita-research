# Glosario

Término, definición en una línea, por qué nos importa. Marcadores de evidencia
según `CLAUDE.md`: `[E]` establecido, `[R]` reportado, `[H]` hipótesis nuestra,
`[?]` incierto o en conflicto entre fuentes.

Este archivo se arma en dos pasadas. La primera es el núcleo conceptual que
cualquier libro de texto de biología molecular comparte, escrito por el
orquestador antes de que volvieran las investigaciones: va marcado `[E]` cuando
es consenso de libro de texto y lleva `— pendiente de fuente` cuando todavía no
tiene cita abierta en `FUENTES.md`. La segunda pasada fusiona los glosarios
parciales de R1 a R5, agrega la cita y resuelve los conflictos de definición.
Donde dos investigaciones definan distinto el mismo término, la entrada queda
marcada `[?]` y el conflicto se anota en `PREGUNTAS_ABIERTAS.md`.

## Ácidos nucleicos y expresión génica

### ADN (ácido desoxirribonucleico) `[E]`
Polímero de doble cadena de cuatro nucleótidos (A, C, G, T) que almacena la
información genética de la célula y se copia a ARN para expresarse.
**Por qué nos importa:** es el nivel donde viven los genes del insecto, del maíz
y de los patógenos; los genomas que vamos a descargar de las bases públicas son
secuencias de ADN, y todo nuestro trabajo de selección de blancos empieza ahí.

### ARN (ácido ribonucleico) `[E]`
Polímero de nucleótidos (A, C, G, U) habitualmente de una sola cadena, que
cumple funciones de mensajero, estructurales y regulatorias; a diferencia del
ADN se plega sobre sí mismo formando estructura secundaria.
**Por qué nos importa:** es la molécula que se aplica como tratamiento y también
la que se quiere destruir dentro del organismo objetivo. Que se plegue es lo que
hace relevante la accesibilidad del sitio blanco.

### Transcripción `[E]`
Síntesis de una molécula de ARN usando una hebra de ADN como molde.
**Por qué nos importa:** define el conjunto de transcritos existentes en un
tejido, que es el espacio real de blancos y también el espacio donde hay que
buscar coincidencias indeseadas.

### Traducción `[E]`
Síntesis de una proteína a partir de la secuencia de un ARN mensajero, en el
ribosoma.
**Por qué nos importa:** el efecto final de silenciar un gen es que su proteína
deja de producirse; el fenotipo que se observa es consecuencia de eso.

### Gen `[E]`
Región del genoma que se transcribe a un ARN funcional, codificante o no.
**Por qué nos importa:** la unidad sobre la que se decide "qué silenciar". La
elección del gen blanco es la primera y más consecuente decisión de diseño.

### Transcrito `[E]`
La molécula concreta de ARN producida a partir de un gen, con sus variantes de
procesamiento.
**Por qué nos importa:** el dsRNA no se aparea contra el gen abstracto sino
contra un transcrito concreto, con sus regiones y su estructura; una región
presente en una variante puede faltar en otra.

### ARNm (ARN mensajero) `[E]`
ARN que codifica una proteína y sirve de molde para la traducción.
**Por qué nos importa:** es el blanco típico del silenciamiento
post-transcripcional: lo que el complejo efector corta.

### ARN no codificante (ncRNA, *non-coding RNA*) `[E]`
Clase funcional de ARN que no se traduce a proteína y cuya función es la propia
molécula: incluye ARN ribosomales y de transferencia, miRNA, siRNA y lncRNA.
**Por qué nos importa:** aparece en las notas del equipo como si fuera lo mismo
que el dsRNA aplicado desde afuera, y no lo es. Ver el supuesto S3 en
`SINTESIS.md`: "no codificante" es una categoría funcional, mientras que
"exógeno" y "doble cadena" describen origen y forma.

### lncRNA (ARN largo no codificante, *long non-coding RNA*) `[E]`
ARN no codificante de más de unos doscientos nucleótidos, con funciones
regulatorias variadas, en general endógeno del organismo que lo transcribe.
**Por qué nos importa:** es la clase que probablemente se confundió con el
dsRNA exógeno en las notas de la charla. Son conceptos de ejes distintos: un
lncRNA puede ser sustrato o regulador de la maquinaria, pero no es lo que se
pulveriza sobre un cultivo.

### dsRNA (ARN de doble cadena, *double-stranded RNA*) `[E]`
Dos hebras complementarias de ARN apareadas; en la mayoría de los eucariotas es
una señal que la célula reconoce como anómala y procesa.
**Por qué nos importa:** es la molécula que se aplica en los tratamientos de
ARN exógeno. Que la célula lo trate distinto del ARN de cadena simple es
precisamente lo que hace posible disparar el silenciamiento desde afuera.

### siRNA (ARN pequeño de interferencia, *small interfering RNA*) `[E]`
Dúplex corto, del orden de 21 a 24 nucleótidos, producido al procesar un dsRNA
largo, que guía el silenciamiento de un transcrito complementario.
**Por qué nos importa:** es la unidad efectora real. Un dsRNA largo aplicado
como tratamiento se convierte en una población de siRNA, y la eficacia depende
de qué siRNA salen de ese procesamiento y cuál de sus dos hebras se carga.

### miRNA (micro ARN) `[E]`
ARN pequeño endógeno, codificado por el propio genoma, que regula la expresión
de genes propios con complementariedad parcial.
**Por qué nos importa:** usa la misma maquinaria que el siRNA pero es endógeno y
tolera apareamiento imperfecto. Esa tolerancia es la razón de fondo por la que
el tamizaje de efectos indeseados no puede limitarse a coincidencias exactas.

## El mecanismo

### RNAi (interferencia por ARN, *RNA interference*) `[E]`
Mecanismo conservado por el cual un ARN de doble cadena provoca la degradación o
la represión específica de los transcritos con secuencia complementaria.
**Por qué nos importa:** es el mecanismo que la pregunta del track nos pide
aprovechar. Todo el proyecto es una apuesta a que se lo puede dirigir con
precisión de secuencia.

### Dicer `[E]`
Ribonucleasa que corta el dsRNA largo en dúplex cortos de tamaño característico.
**Por qué nos importa:** determina qué fragmentos de nuestro dsRNA diseñado
existen efectivamente dentro del organismo; el diseño de la secuencia larga
condiciona, pero no elige, la población de siRNA resultante.

### RISC (complejo silenciador inducido por ARN, *RNA-induced silencing complex*) `[E]`
Complejo ribonucleoproteico que incorpora una hebra del dúplex corto y la usa
como guía para encontrar y silenciar el transcrito complementario.
**Por qué nos importa:** es el paso donde la secuencia se convierte en función.
Los criterios termodinámicos de diseño existen para sesgar qué hebra entra acá.

### Argonaute `[E]`
Proteína central del RISC que sostiene la hebra guía y, en varias de sus
versiones, corta el transcrito objetivo.
**Por qué nos importa:** sus preferencias de carga —por ejemplo por el
nucleótido inicial de la guía— son reglas de diseño concretas y verificables.

### Selección de la hebra guía `[E]`
Elección, entre las dos hebras del dúplex corto, de la que queda cargada como
guía; la otra se descarta.
**Por qué nos importa:** si se carga la hebra equivocada, el tratamiento apunta
a un complementario que no es el blanco: se pierde eficacia y se gana riesgo de
efecto indeseado.

### Asimetría termodinámica `[E]`
Diferencia de estabilidad de apareamiento entre los dos extremos del dúplex
corto, que sesga cuál de las dos hebras se carga como guía.
**Por qué nos importa:** es uno de los pocos criterios de diseño calculables
desde la secuencia sola, sin datos experimentales. Es un término natural de
cualquier función de puntuación que armemos.

### Silenciamiento post-transcripcional (PTGS) `[E]`
Silenciamiento que actúa sobre el transcrito ya producido, cortándolo o
bloqueando su traducción; el gen sigue transcribiéndose.
**Por qué nos importa:** es el modo de acción que se espera de un tratamiento de
dsRNA aplicado desde afuera, y es reversible: el efecto dura mientras dure la
molécula.

### Silenciamiento transcripcional (TGS) `[E]`
Silenciamiento que actúa sobre el ADN y su cromatina, por metilación dirigida
por ARN, impidiendo que el gen se transcriba.
**Por qué nos importa:** tiene otra persistencia y otras implicancias
regulatorias y de herencia que el post-transcripcional. Conviene no mezclarlos
cuando se discute cuánto dura el efecto de un tratamiento.

### RdRP (ARN polimerasa dependiente de ARN) `[E]`
Enzima que sintetiza ARN usando ARN como molde y que, en los organismos que la
tienen, amplifica la señal de silenciamiento.
**Por qué nos importa:** su presencia o ausencia explica por qué el
silenciamiento se propaga y se sostiene en plantas y nematodos y es mucho más
irregular en insectos. R1 verifica el detalle por grupo.

### Silenciamiento sistémico `[E]`
Propagación de la señal de silenciamiento desde las células donde se inició
hacia tejidos distantes.
**Por qué nos importa:** decide si alcanza con que el ARN entre por un tejido o
hace falta exponer directamente el tejido donde está el gen blanco. Cambia por
completo el modo de aplicación.

### ARN exógeno `[E]`
ARN aportado desde afuera del organismo —pulverizado, ingerido, inyectado, por
riego o por tratamiento de semilla— en contraste con el que el propio organismo
transcribe.
**Por qué nos importa:** es el término exacto de la pregunta del track. Define
el problema como "entregar una molécula que funcione" y no como "modificar un
genoma", con todo lo que eso implica en costo, reversibilidad y regulación.

### SIGS (silenciamiento génico inducido por pulverización, *spray-induced gene silencing*) `[E]`
Aplicación tópica de dsRNA o siRNA sobre la planta para que lo absorba la planta
o lo ingiera la plaga, sin modificar ningún genoma.
**Por qué nos importa:** es la familia de tratamientos que corresponde a "ARN
exógeno" en el campo, y la que tiene el camino regulatorio más corto por no ser
transgénica.

### HIGS (silenciamiento génico inducido por el hospedador, *host-induced gene silencing*) `[E]`
La planta se modifica genéticamente para producir ella misma el dsRNA que
silencia un gen de la plaga o del patógeno que la ataca.
**Por qué nos importa:** es el enfoque alternativo, con mejor persistencia y
peor camino regulatorio. Sirve de comparación obligada para argumentar por qué
el exógeno es la apuesta razonable.

### VIGS (silenciamiento génico inducido por virus, *virus-induced gene silencing*) `[E]`
Uso de un vector viral para que exprese dentro de la planta el fragmento que
dispara el silenciamiento; es sobre todo una herramienta de investigación.
**Por qué nos importa:** aparece en la literatura de diseño y conviene no
confundirlo con un producto aplicable a campo.

### Efecto indeseado / off-target `[E]`
Silenciamiento de un transcrito que no era el blanco, por complementariedad
total o parcial de la guía con otra secuencia.
**Por qué nos importa:** es la mitad "riesgo" de la pregunta del track. El
tamizaje de off-target en maíz, en polinizadores, en enemigos naturales y en
fauna del suelo es una tarea computacional pura: nuestra ventaja comparativa
está justamente acá.

## Herramientas y cantidades calculables

### BLAST (*Basic Local Alignment Search Tool*) `[E]`
Algoritmo y familia de programas de alineamiento local de secuencias por
semilla y extensión (*seed-and-extend*), que busca una consulta contra una base
de datos y devuelve los parecidos con su significancia estadística.
**Por qué nos importa:** es la herramienta del tamizaje de off-target y de la
búsqueda de regiones conservadas. Y es el centro del supuesto S2: las notas del
equipo le atribuyen un cálculo de termodinámica que no hace. Ver `DECISIONS.md`
y la resolución de S2 en `SINTESIS.md`.

### E-value (valor esperado) `[E]`
Número de coincidencias de ese puntaje o mejor que cabría esperar por azar en
una base de datos de ese tamaño; cuanto más chico, menos atribuible al azar.
**Por qué nos importa:** es el umbral con el que se decide si una coincidencia
indeseada cuenta como riesgo. Depende del tamaño de la base, lo que lo vuelve
una decisión de diseño y no un número objetivo.

### Bit score (puntaje en bits) `[E]`
Puntaje de similitud de un alineamiento, normalizado e independiente del tamaño
de la base de datos.
**Por qué nos importa:** es la cantidad comparable entre búsquedas distintas
cuando el E-value no lo es.

### ΔG de hibridación (energía libre) `[E]`
Cambio de energía libre asociado al apareamiento de dos cadenas de ARN o al
plegado de una sobre sí misma; más negativo indica apareamiento más estable.
**Por qué nos importa:** es la cantidad termodinámica real del problema, la que
BLAST no calcula. La computan herramientas de la familia ViennaRNA, y es un
término candidato de nuestra función de puntuación.

### Accesibilidad del sitio blanco `[E]`
Probabilidad de que la región del transcrito objetivo esté desapareada y
disponible para que la guía se aparee con ella, en lugar de estar plegada dentro
de una estructura.
**Por qué nos importa:** un sitio perfectamente complementario pero inaccesible
no se silencia. Es calculable desde la secuencia, sin datos experimentales: otro
término barato y defendible de la función de puntuación.

### ViennaRNA / RNAfold / RNAup `[E]`
Paquete y programas de predicción de estructura secundaria y de energías de
apareamiento y de accesibilidad de ARN, basados en modelos termodinámicos de
vecino más cercano.
**Por qué nos importa:** es la mitad termodinámica del pipeline, la que en las
notas del equipo quedó fundida con BLAST. Corre en una notebook y es
reproducible, lo que lo vuelve cimiento razonable de un artefacto nuestro.

### Conservación entre poblaciones `[E]`
Grado en que la región elegida del transcrito blanco es idéntica entre
individuos y poblaciones geográficas del organismo objetivo.
**Por qué nos importa:** una región variable hace que el tratamiento funcione en
un lote y no en el de al lado, y acelera la aparición de resistencia.

## El sistema biológico del track

### Vector (en epidemiología vegetal) `[E]`
Organismo, en general un insecto, que adquiere un patógeno de una planta
infectada y lo transmite a una planta sana.
**Por qué nos importa:** define la estructura del problema. Hay tres puntos
posibles de intervención —insecto, patógeno y defensa de la planta— y no son
igual de atacables por RNAi: es la pregunta central de R1.

### *Dalbulus maidis* `[E]`
Chicharrita del maíz, insecto hemíptero de la familia Cicadellidae que se
alimenta del floema del maíz y transmite los patógenos del complejo de
achaparramiento.
**Por qué nos importa:** es el vector y, por ser un insecto, es el único de los
tres actores con maquinaria de RNAi propia de la que se sabe que responde a
dsRNA ingerido. La magnitud de esa respuesta en esta especie es lo que R1
verifica.

### Fitoplasma `[E]`
Bacteria sin pared celular, del grupo de los mollicutes, que no se cultiva en
medios convencionales, vive en el floema de la planta y se transmite por
insectos.
**Por qué nos importa:** es uno de los patógenos del complejo. Ser una bacteria
y no un eucariota es la razón por la que no se le puede suponer maquinaria de
RNAi: la verificación de esto decide qué estrategias quedan en pie.

### Espiroplasma / *Spiroplasma kunkelii* `[E]`
Mollicute helicoidal, también sin pared celular, habitante del floema y
transmitido por insectos; *S. kunkelii* es el agente del achaparramiento del
maíz (*corn stunt*).
**Por qué nos importa:** el segundo patógeno de peso del complejo. Mismo
problema que el fitoplasma para una estrategia de silenciamiento directo, y
misma consecuencia estratégica.

### MRFV (virus del rayado fino del maíz, *Maize rayado fino virus*) `[E]`
Virus de ARN transmitido por *Dalbulus maidis*, tercer agente habitualmente
asociado al complejo.
**Por qué nos importa:** al ser un virus de ARN, su genoma es en principio
sustrato de la maquinaria de RNAi de la planta, lo que lo pone en una categoría
distinta de los dos mollicutes. R1 verifica qué evidencia hay de que eso sea
aprovechable.

### Complejo de achaparramiento del maíz (*corn stunt complex*) `[R]`
Cuadro de enfermedad del maíz atribuido a la acción conjunta de varios
patógenos transmitidos por *Dalbulus maidis*.
**Por qué nos importa:** es el objeto de la pregunta del track. Cuántos agentes
son con certeza, y qué síntoma y qué pérdida de rendimiento corresponde a cada
uno, es el supuesto S1 y lo verifica R1: las notas del equipo le atribuyen
granos por mazorca a uno y altura de tallo al otro, y esa asignación hay que
confirmarla o corregirla.

### Transmisión persistente propagativa `[E]`
Modo de transmisión en el que el patógeno adquirido atraviesa el intestino del
insecto, se multiplica dentro de él, llega a las glándulas salivales y queda
transmisible por el resto de la vida del vector, tras un período de latencia.
**Por qué nos importa:** es la propiedad que vuelve insuficiente matar al
insecto tarde: una vez infectivo, lo es hasta que muere. Y, del lado
constructivo, abre una ventana de intervención distinta: interferir con la
adquisición o con el pasaje interno dentro del vector en lugar de atacar al
patógeno en la planta.
