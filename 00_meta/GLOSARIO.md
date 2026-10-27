# Glosario

Término, definición en una línea, por qué nos importa. Marcadores de evidencia
según `CLAUDE.md`: `[E]` establecido, `[R]` reportado, `[M]` medido por nosotros
(reproducible desde el repo), `[H]` hipótesis nuestra, `[?]` incierto o en conflicto
entre fuentes. Las entradas de esta primera pasada, que son consenso de libro de texto,
conservan `[E]`; `[M]` no aplica a definiciones.

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

---

## Segunda pasada — fusión de los glosarios parciales

Hecha el 2026-10-17, al integrar las cinco investigaciones. Cumple lo que
`DECISIONS.md` D4 dejó comprometido: el núcleo conceptual de arriba se escribió antes de
tener fuentes, y acá se le suman los términos que las investigaciones efectivamente usaron,
cada uno con el documento del repositorio donde está empleado y citado.

La referencia biológica completa y citada es `research/R1_fundamentos/glosario_parcial.md`,
77 entradas en orden temático. Lo que sigue son los términos que ese glosario aporta y que
el núcleo de arriba no tenía, más los términos de método que introdujeron R2, R4 y R5.

### Clases de ARN

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **microARN (miRNA)** | ARN endógeno corto, de 20 a 24 nt, que regula negativamente otros genes, muchas veces con apareamiento imperfecto. | Es la vía que la sobresaturación de dsRNA puede alterar, causando letalidad inespecífica. |
| **vsiRNA** | siRNA derivado de un virus, generado por la planta a partir del ARN viral. | Su presencia indica que la defensa se activó, pero no prueba que la planta esté protegida. |
| **syn-tasiRNA / atasiRNA** | Dúplex de 21 nt diseñados y expresados desde precursores *TAS* ingenierizados, con registro de corte definido. | Es el extremo de "precisión" del espacio de diseño que plantea el organizador: dúplex predefinidos en vez de pool heterogéneo. |

### El mecanismo

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **Dicer-2** | La Dicer de insectos especializada en dsRNA largo exógeno y viral. | Su variación entre órdenes explica por qué el largo del siRNA cambia de 20 a 22 nt según el insecto. |
| **Dominio PAZ** | Dominio que reconoce el extremo característico del dúplex (saliente de 2 nt en 3′), presente en Dicer y en Argonaute. | Junto con RNasa III forma la "regla molecular" que mide el largo del producto. |
| **Dominio PIWI** | Dominio catalítico de Argonaute, con plegamiento tipo RNasa H y tríada DDX cuando corta. | Su ausencia en un genoma es evidencia directa de que no hay Argonaute: es el dominio que contamos en los mollicutes. |
| **Dominio MID** | Dominio de Argonaute que une el fosfato 5′ de la hebra guía. | Mutarlo abole el corte, a diferencia de mutar PAZ: el extremo 5′ manda. |
| **RNasa III** | Familia de endonucleasas que cortan ARN de doble cadena; ubicua en bacterias. | Que un mollicute la tenga **no** significa que tenga Dicer: es la tijera genérica, no la regla. |
| **Hebra guía / hebra pasajera** | De las dos hebras del dúplex, la que se conserva en el RISC y la que se degrada. | Si se carga la equivocada, el complejo busca la secuencia equivocada: es el núcleo del problema de diseño. |
| ***Slicer*** | La actividad de corte endonucleolítico del dominio PIWI. | No todas las Argonautas la tienen; de las cuatro humanas, sólo Ago2. |
| **Knockdown** | Reducción parcial de la expresión de un gen, medida típicamente por RT-qPCR. | Es la métrica de eficacia que reportan los papers (por ejemplo ~95 % para *burs-α* en *D. maidis*). |
| **SID-1 / SID-2** | Proteínas del sistema de diseminación sistémica del silenciamiento en nematodos. | Los insectos carecen de homólogos: la señal no se disemina sola. |

### Las plataformas de aplicación

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **Portador / nanoportador** | Material que encapsula el dsRNA para protegerlo y liberarlo gradualmente (quitosano, liposomas, nanoarcillas LDH). | Las nanoarcillas LDH ("BioClay") protegen del lavado y la degradación por al menos 30 días. |
| **Pirimidina 2′-F** | Nucleótido modificado químicamente en la posición 2′ del azúcar, más resistente a nucleasas. | Con 32–55 % de incorporación aumentó la mortalidad 12–35 % en varios hemípteros. |
| **dsRNasa** | Nucleasa que degrada específicamente ARN de doble cadena. | *D. maidis* tiene tres, una muy expresada en intestino medio y glándulas salivales: es el cuello de botella declarado de la entrega oral. |

### El sistema patógeno

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **Floema** | Tejido vascular que transporta la savia elaborada. | Es donde se alimenta el vector y donde viven los cuatro patógenos. |
| **Fitófago de floema** | Insecto que se alimenta perforando el floema con su estilete. | Explica por qué el dsRNA pulverizado en superficie le llega mal: depende de captación vascular. |
| **Transmisión persistente circulativa** | El patógeno circula por el insecto pero **no** se multiplica en él. | Una fuente atribuye este modo al MSMV y otra lo da por desconocido: queda como incertidumbre. |
| **Período latente** | Tiempo entre la adquisición y el momento en que el insecto puede transmitir. | En *S. kunkelii* es de 18 a 22 días: es la ventana donde una intervención sobre el insecto todavía sirve. |
| **Transmisión transovárica** | Paso del patógeno de la madre a la descendencia por el huevo. | No ocurre en este sistema: cada individuo debe adquirir por su cuenta. |
| **Mollicute** | Bacteria sin pared celular, de genoma pequeño y bajo contenido GC. | *S. kunkelii* y el fitoplasma lo son, y es la razón central de que no respondan a RNAi. |
| **Marafivirus** | Género de virus de ARN de cadena simple de sentido positivo; acá, MRFV. | Es uno de los dos virus del complejo, y se multiplica dentro del insecto. |
| **Mastrevirus / Geminiviridae** | Género y familia de virus de ADN de cadena simple transmitidos por chicharritas; acá, MSMV (*Mastrevirus striatis*). | Es el único patógeno del complejo contra el cual la planta puede usar la vía RdDM. |
| **+ssRNA / ssDNA** | ARN de cadena simple de sentido positivo / ADN de cadena simple. | Son los tipos de genoma de MRFV y MSMV: determinan qué vía de defensa vegetal aplica. |
| **Maíz guacho** | Plantas voluntarias de maíz que sobreviven entre campañas y sirven de "puente verde" al vector. | Eliminarlo es una de las pocas medidas culturales con lógica epidemiológica clara. |
| ***Safrinha*** | Segunda zafra brasileña de maíz, sembrada después de la soja. | Es el contexto de la mayoría de los datos de incidencia brasileños. |
| **Brocosomas** | Partículas proteicas que las chicharritas secretan y esparcen sobre su cutícula. | Son una barrera física que limita la eficacia de los hongos entomopatógenos. |
| **Antixenosis** | Resistencia por no preferencia: el insecto evita la planta. | Reduce el tiempo de contacto y con él la eficiencia de transmisión. |
| **Antibiosis** | Resistencia que afecta la biología del insecto que sí se alimenta. | Es el otro componente separable de la resistencia del híbrido. |
| **Incidencia / severidad** | Proporción de plantas con síntomas / intensidad del cuadro en las plantas afectadas. | A campo, el índice de severidad explicó el 72 % de la variabilidad del rendimiento; la acumulación del patógeno no lo explicó. |
| **Estadio V2 / R4** | Etapas fenológicas del maíz: dos hojas desarrolladas / grano pastoso. | El tratamiento de semilla fue efectivo sólo hasta V2; la incidencia se evaluó en R4. |
| **DAS-ELISA** | Inmunoensayo de doble sándwich para detectar un antígeno. | Es la técnica con la que se confirmó *S. kunkelii* en el ensayo argentino. |
| **CL50** | Concentración letal 50: la dosis que mata a la mitad de los individuos. | Es la unidad en la que se mide la resistencia a insecticidas. |
| **Razón de resistencia (RR)** | Cociente entre la CL50 de una cepa resistente y la de una susceptible. | 3.170 veces para bifentrina: la magnitud del problema que justifica buscar otro modo de acción. |

### Herramientas y conceptos de cómputo

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **Bowtie** | Alineador de lecturas cortas con índice Burrows-Wheeler y backtracking consciente de la calidad. | Es el motor que usan si-Fi y dsRIP para buscar off-targets; tampoco calcula energía. |
| **Mismatch** | Posición donde el siRNA y el transcrito no aparean. | Los minimizadores de off-target cuentan coincidencias permitiendo 1 o 2 mismatches. |
| **Ortólogo** | Gen de otra especie derivado del mismo gen ancestral. | Es como se transfieren blancos efectivos de una plaga modelo a la plaga objetivo. |
| **Transcriptoma** | Conjunto de todos los transcritos de un organismo o tejido. | Es el insumo mínimo para cualquier análisis de off-target; el de *D. maidis* tiene 56.116 transcriptos. |
| **si-Fi21 / si-Fi** | Diseñador de disparadores largos y predictor de off-targets. | Hace la enumeración de x-meros que el equipo creía que hacía BLAST, y usa Bowtie + RNAplfold. |
| **dsRIP** | Plataforma de diseño de dsRNA para manejo de plagas. | Es la herramienta con el tratamiento cuantitativo más explícito de eficacia y de riesgo no objetivo. |
| **pssRNAit / P-SAMS** | Diseñadores de ARN pequeños **para plantas**. | Importante: no sirven para diseñar contra un insecto; sus bases y reglas son vegetales. |

### Términos biológicos de apoyo que aparecen en el reporte

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **Estilete** | Pieza bucal alargada con la que el hemíptero perfora el tejido y succiona savia. | Es la vía física por la cual el insecto adquiere e inocula los patógenos. |
| **Ninfa / estadio ninfal** | Cada una de las etapas juveniles por las que pasa el insecto antes de ser adulto; *D. maidis* tiene cinco. | Las ninfas ya transmiten, y el tercer estadio fue el más sensible al RNAi en un psílido emparentado. |
| **Ecdisis / muda** | Proceso de desprenderse del exoesqueleto viejo para crecer. | Es el proceso que fallan los insectos con *burs-α* o *eth* silenciados, y por eso mueren. |
| **Hemolinfa** | El "sangre" de los insectos: fluido circulatorio del hemocele. | Es por donde circula el patógeno entre el intestino y las glándulas salivales. |
| **Glándulas salivales** | Órganos que producen la saliva que el insecto inyecta al alimentarse. | Colonizarlas es el último paso antes de que el insecto pueda transmitir. |
| **Ovogénesis** | Formación de los oocitos en el ovario. | Es el proceso que afecta el silenciamiento de *Bicaudal C*, el primer blanco validado en *D. maidis*. |
| **Virulífero** | Insecto que porta el patógeno y puede transmitirlo. | Es la condición que se cuenta en los ensayos de transmisión. |
| **Epifitia** | Brote epidémico de una enfermedad en una población vegetal. | Es la palabra que corresponde al episodio argentino de 2023/24. |
| **Efector** | Proteína que un patógeno secreta en el hospedador para manipular su fisiología. | Es la vía por la cual los mollicutes alteran la planta y el vector, y un blanco alternativo al RNAi. |
| **Supresor viral del silenciamiento (RSS)** | Proteína codificada por un virus que bloquea la maquinaria de RNAi del hospedador. | Explica que la defensa antiviral vegetal exista y aun así el virus se establezca. |
| **Apoplasto** | El espacio extracelular de la planta, fuera de la membrana celular. | Las RNasas apoplásticas degradan el ARNdc pulverizado antes de que entre a la célula. |
| **Estoma** | Poro regulable de la epidermis foliar que controla el intercambio gaseoso. | Es la vía principal implicada en la captación foliar de ARNdc. |
| **RT-qPCR** | PCR cuantitativa sobre ADN copiado desde ARN; mide cuánto transcrito hay. | Es la técnica con la que se mide el *knockdown* en todos los trabajos citados. |
| ***In vitro* / *in vivo* / *ex vivo*** | En tubo / en el organismo vivo / en tejido extraído del organismo. | Distingue, por ejemplo, el corte de ARN por Argonautas procariotas (demostrado *in vitro*, rol *in vivo* desconocido). |
| **x-mero** | Subcadena de largo *x* extraída de una secuencia; para nosotros, cada ventana de 21 nt del disparador. | Es la unidad que enumeran los diseñadores de ARNdc por ventana deslizante. |

### Método, decisión e incertidumbre (R2, R4 y R5)

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **Frente de Pareto** | Subconjunto de candidatos que ningún otro supera simultáneamente en todos los criterios. | Es la parte del ordenamiento que **no** depende de los pesos que elijamos, y por eso es la parte no discutible de una priorización. `[E]` — uso en `R2/PROPUESTA.md` §3 y `R2/REPORT.md` §3.3. |
| **Predicción conformal (*conformal prediction*)** | Envoltorio sobre cualquier predictor que devuelve un conjunto o intervalo con cobertura garantizada sin suponer una distribución. | Es la forma concreta de entregar «este candidato es mejor, y con esta confianza» en lugar de un número pelado; el relevamiento del campo señala la ausencia de cuantificación de incertidumbre como la brecha de máxima prioridad. `[E]` — `R4/REPORT.md` y `R4/lineas_de_ataque.md` L1. |
| **Estabilidad del ordenamiento** | Fracción de remuestreos (pesos del simplex y bootstrap de coeficientes) en que un candidato precede a otro; por encima de 0,90 lo llamamos orden robusto y por debajo, empate. | Convierte un ranking en una afirmación falsable y es lo que permite decir «estos dos están empatados dentro de la incertidumbre». `[H]` del equipo — `R2/PROPUESTA.md` §3. |
| **Modelo de riesgos proporcionales de Cox / *hazard ratio*** | Modelo de supervivencia que estima cuánto multiplica un factor la tasa instantánea de muerte; el hazard ratio es ese multiplicador. | Es la forma en que está medida la eficacia de un ARNdc en el único conjunto de datos de insecto con diseño controlado, y por lo tanto la unidad en la que podemos validar. `[E]` — `R1/REPORT.md` §6, `R2/REPORT.md` §2.2. |
| **Estadístico C de Harrell** | Medida de concordancia de un modelo de supervivencia, análoga al AUC: probabilidad de ordenar bien un par al azar. | Es el 0,76 (IC 95 % 0,73–0,79) que define cuánta confianza merece el puntaje de eficacia que vamos a reusar. `[E]` — `R1/REPORT.md` §6. |
| **Fuga de datos (*data leakage*)** | Contaminación entre entrenamiento y prueba que infla artificialmente el resultado de un benchmark. | El relevamiento del campo de siRNA la señala como causa sistemática de resultados inflados; por eso nuestras particiones son por gen y por especie, nunca aleatorias. `[E]` — `R4/REPORT.md`, `R2/REPORT.md` §5. |
| **Partición dejando un gen afuera (*leave-one-gene-out*)** | Validación cruzada en la que todas las ventanas de un mismo gen blanco quedan juntas en el pliegue de prueba. | Con n = 29 es la única partición honesta disponible para validar el puntaje sin fuga. `[E]` — `R2/REPORT.md` §5. |
| **Modelo fundacional de secuencias** | Red preentrenada sobre grandes volúmenes de ADN o ARN sin etiquetas, que se reusa como extractor de representaciones. | Es la familia que el equipo tenía como primera intuición; cuatro evaluaciones independientes muestran que fuera de su dominio no aventaja a una codificación simple. `[E]` — `R4/REPORT.md` §1 y `R4/modelos.json`. |
| **Representación aprendida (*embedding*)** | Vector de números con el que un modelo representa cada nucleótido o secuencia. | El relevamiento del subcampo los califica de «suficientes pero no necesarios» para el estado del arte en predicción de eficacia. `[E]` — `R4/REPORT.md` §3. |
| **Atención (*attention*)** | Mecanismo que pondera qué partes de la entrada mira un modelo al producir cada salida. | Es el núcleo de la idea original del equipo; la literatura sostiene que sus pesos **no** habilitan una lectura causal, y para nuestro caso el perfil posicional explícito del puntaje cumple la misma función y es fiel por construcción. `[E]`/`[?]` — `R2/REPORT.md` §3.5. |
| **Explicación fiel frente a plausible (*faithful* / *plausible*)** | Fiel es la que refleja el proceso real de decisión del modelo; plausible es la que convence a una persona. | Distinción que evita el error más caro que podríamos cometer ante un jurado académico: presentar un mapa de atención como evidencia. `[E]` — `R2/REPORT.md` §3.5. |
| **Compuerta (*gate*) de la rúbrica** | Condición de admisión que no se puntúa ni se compensa: G0 alcance ético, G1 blanco verificable, G2 especificidad mínima, G3 trazabilidad. | Es lo que impide que un buen puntaje tape un problema inadmisible, y G3 es la que vuelve operativa la palabra «reproducible» del track. `[H]` del equipo — `R5/RUBRICA.md` §2. |
| **Marca (P) de la rúbrica** | Señal de que un dato todavía no existe pero lo podemos producir nosotros dentro del plazo. | Permite reportar dos órdenes, conservador y optimista, y leer en la distancia entre ambos qué medición hay que hacer antes de decidir. `[H]` del equipo — `R5/RUBRICA.md` §5.3. |
| **Criterio de off-target de la EFSA (2025)** | Conjunto de reglas regulatorias para marcar transcriptos fuera de blanco de cada ARN pequeño de 21 nt: hasta cuatro apareamientos erróneos sin hueco (o tres más un hueco), G:U como medio error, nada en las posiciones 10 u 11, no más de dos errores en los primeros 12 nt del extremo 5′, y cociente de energía libre mayor que 0,75. | Es más exigente que el umbral de 19 nt complementarios que usan las herramientas de insectos, y marca más candidatos, no menos; su alcance declarado son plantas modificadas genéticamente y **no** cubre riesgo ambiental. `[E]` — `R5/RUBRICA.md` G2. |
| ***Candidatus* Phytoplasma zeae** | Nombre formal, dado en 2026, del fitoplasma del achaparramiento arbustivo del maíz, transmitido exclusivamente por *Dalbulus maidis* y *D. elimatus*. | Cierra una pregunta abierta del proyecto: el genoma del fitoplasma del complejo existe, completo y anotado, y no es ninguno de los de *Ca.* P. asteris. `[E]` — `R5/REPORT.md` y `R5/RUBRICA.md` §7.1. |
| **TSA (*Transcriptome Shotgun Assembly*)** | División del NCBI donde se depositan transcriptomas ensamblados, con su propio prefijo de accesión. | El transcriptoma de *D. maidis* que usamos como insumo central vive ahí (`GITV00000000`), y su ausencia o presencia decide si hay análisis de off-target intraespecífico. `[E]` — `R5/PLAN_EQUIPO.md` P1. |
| **Paquete de datos congelado (*data package*)** | Conjunto de insumos descargados, con manifiesto de hashes, licencia por insumo y procedencia. | Es el entregable de la rama de datos y la condición para que el puntaje se pueda regenerar: sin él, G3 no se cumple. `[H]` del equipo — `R5/PLAN_EQUIPO.md` P1 y `R5/REPORT.md` §2. |

### Conflictos de definición

Ninguno. Las cinco investigaciones coincidieron en los términos que comparten, incluida
la distinción entre alineamiento y termodinámica que R1 y R2 verificaron por separado
—la redundancia deliberada de `DECISIONS.md` D3—, y llegaron a la misma conclusión.

---

## Tercera pasada — términos de la ola 2 (corpus oficial)

Agregada el 2026-10-17, al integrar las cinco investigaciones de la ola 2. Son los términos
que aparecen en el corpus oficial y en el trabajo sobre él, más una definición que la
ola 1 tenía mal y queda corregida.

La referencia completa de los términos biológicos de los papers del corpus es
`research/ola2/W1_papers/glosario_parcial.md`, 48 entradas con el paper del que sale cada
una.

### Del corpus de papers

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **Lipofectamina** | Reactivo catiónico de transfección usado como coadyuvante para favorecer la internalización de ácidos nucleicos; en P6 al 13 % final | Es el coadyuvante concreto que no alcanzó para vencer la barrera cuticular del cicadélido |
| **Dieta artificial en sobre de parafilm** | Sacarosa al 15 % con colorante, encerrada entre dos capas de parafilm sobre un vial, de la que el insecto chupa a través de la membrana (P1) | Es el bioensayo estándar para tamizar muchos ARNdc en un hemíptero adulto; no sirve para ninfas porque la dieta ya las mata |
| **Hidróxido doble laminar (LDH, *layered double hydroxide*)** | Arcilla inorgánica laminar de carga positiva, fórmula general con M²⁺ y M³⁺, que adsorbe ácidos nucleicos; en P4, nanoláminas de 45 nm de diámetro Z | Es el portador de BioClay; su degradación por ácido carbónico atmosférico es lo que libera el ARNdc de a poco |
| **Pulverización a alta presión / inundación de estomas abaxiales** | Técnicas para forzar la entrada de ARN a través de la cutícula y la pared celular (P7, citando a Bennett et al. 2020) | Cuando un paper reporta "captación foliar", hay que mirar cómo forzó la entrada antes de generalizar a una pulverización de campo |
| **Vaina foliar abierta** | El cartucho de hojas jóvenes todavía enrollado de una plántula de maíz, con paredes flexibles y cutícula delgada; el sitio de aplicación de P7 | Es una variable de diseño que no teníamos: dónde se aplica cambia si entra o no |
| **Electropenetrografía (EPG)** | Registro eléctrico del recorrido del estilete de un insecto chupador, que permite distinguir si está sondeando floema, xilema o parénquima (P6) | Es la evidencia de que los fitófagos de floema **también** beben de xilema, que es el único mecanismo por el que la entrega mediada por planta puede funcionar |
| **Melaza / *honeydew*** | Excreción azucarada del insecto chupador; en P6 se tiñó de azul al alimentarse sobre hoja tratada | Es la prueba barata de que el insecto efectivamente ingirió lo que la planta absorbió |
| **Bursicón (Burs-α / Burs-β)** | Neurohormona heterodimérica que endurece y melaniza la cutícula nueva y expande las alas tras la muda; Burs-α tiene 11 cisteínas conservadas (P3) | Es uno de los dos blancos con mejor fenotipo publicado en *D. maidis*: 10 % de supervivencia a día 4 |
| **Hormona desencadenante de la ecdisis (ETH)** | Neuropéptido producido por las células INKA de las glándulas epitraqueales que dispara la secuencia conductual de la ecdisis (P3) | El otro blanco de P3; su silenciamiento deja al insecto atrapado dentro de la exuvia vieja |
| **Células INKA / glándulas epitraqueales** | El grupo de células que secreta ETH (P3) | Ubica anatómicamente al blanco: no es intestino ni glándula salival |
| **Exuvia** | La cutícula vieja que el insecto desecha al mudar (P3) | El fenotipo de ds-*eth* se define como no poder desprenderse de ella |
| **Legumaína** | Cisteín-proteasa de tipo asparaginil endopeptidasa, expresada en intestino (P6); en *E. variegatus* se expresa 2.500 veces más en intestino que en glándulas salivales | Blanco de "primer órgano que toca el ARNdc ingerido": la lógica de elegir un gen por **dónde** se expresa y no sólo por qué hace |
| **Naterina (*natterin*)** | Proteína de intestino de insecto, originalmente descrita en veneno de pez, asociada a la interacción con patógenos (P6) | Ídem; y en la ola 1 figuraba como fuente `S30` sin enlace, con el rótulo "natterin-like y legumaína de intestino de insecto" |
| **ATP sintasa beta** | Subunidad catalítica de la ATP sintasa mitocondrial, de expresión sistémica, implicada en la transmisión del fitoplasma (P6) | Es el blanco que une "matar al vector" con "desarmar la transmisión", y el que P6 silenció en las dos especies por vía de planta |
| **Cathepsin D** | Proteinasa aspártica lisosomal del intestino medio posterior de hemípteros, implicada en la metamorfosis (P1) | Uno de los tres blancos de entrega oral en *D. citri* |
| **Inhibidor de apoptosis (IAP)** | Proteína que bloquea la maquinaria apoptótica y participa en señalización, ubiquitinación y división celular (P1) | Fue el blanco **más letal** de los tres en *D. citri*: 64 % de mortalidad a 1000 ng/µL |
| **Fitoeno desaturasa (PDS)** | Enzima de la biosíntesis de carotenoides cuyo silenciamiento produce fotoblanqueo visible de la hoja (P2) | Es el gen reportero estándar de VIGS en plantas: no es un blanco de control, es un semáforo |
| **ZmlspH / lemon white1 (lw1)** | Gen de maíz necesario para el desarrollo del cloroplasto; silenciado da un fenotipo albino amarillo (P2) | El segundo reportero que P2 usa para mostrar que su vector sirve para más de un gen |
| **AGO18a** | Argonauta específica de monocotiledóneas, inducible por virus, que secuestra microARN del hospedador para liberar a AGO1 (P7) | En P7 es el gen de la vía de RNAi que más responde a la infección: 16 veces de inducción |
| **MOP1 (*mediator of paramutation 1*)** | Homólogo de RDR2 en maíz, necesario para la paramutación y el silenciamiento transcripcional (P7) | Conecta la vía de RNAi del maíz con el RdDM, que es el cuarto escalón de la escalera de precisión del organizador |
| **Inoculación por punción vascular (VPI)** | Inocular un virus pinchando el tejido vascular del embrión de la semilla con agujas finas y una herramienta de grabado (P2) | El MRFV **no** se transmite por frote de savia; sin VPI o sin el insecto no hay experimento |
| ***Marafibox*** | Promotor conservado de 16 nucleótidos de los marafivirus que dirige la síntesis del ARN subgenómico; equivalente al *tymobox* de los tymovirus (P2) | Es el elemento que controla la expresión de CP2, una de las dos cápsides |
| **CP1 y CP2 carboxi-coterminales** | Las dos proteínas de cápside del MRFV, que comparten el extremo carboxilo; CP1 se escinde de la poliproteína y CP2 se expresa desde el ARN subgenómico, en razón 1:3 en la partícula (P2) | Importa para interpretar el candidato `CP_MRFV` del EPILAB: "la cápside" del MRFV son dos productos distintos |
| **Unión HEL/POL** | La unión predicha de corte entre helicasa y polimerasa de la poliproteína del MRFV, nucleótidos 3709/3710 (P2) | Es el **único** sitio del genoma del MRFV que tolera una inserción; los otros tres probados son letales |
| **Peptidasa 2A del virus de la fiebre aftosa (FMDV 2A)** | Secuencia corta de 51 nt que provoca la separación cotraduccional de dos proteínas, usada para insertar una secuencia dentro de una poliproteína sin romper su procesamiento (P2) | Es el truco de ingeniería que hace viable la inserción: no duplica el sitio de corte nativo, lo sustituye |
| **Período de acceso a adquisición (AAP)** | El tiempo que el insecto pasa alimentándose sobre la fuente infectada para adquirir el patógeno; en P2, tres semanas para el MRFV (P2) | Es el parámetro que define cualquier bioensayo de transmisión, y el que hay que pedir si se propone uno |
| ***Escherichia coli* HT115 (DE3)** | Cepa deficiente en RNasa III y con T7 ARN polimerasa inducible, que por eso acumula ARNdc en lugar de degradarlo (P4, P5) | Es **la** cepa de producción barata de ARNdc, y la que usan tanto P5 como P4 |
| **IPTG** | Análogo de lactosa que induce el promotor T7 en esa cepa (P5) | El disparador de la producción; `R1/REPORT.md` ya registraba que la lactosa a 6 g/L puede sustituirlo y multiplicar el rendimiento |
| **ARN en horquilla (hpRNA) y vector de repetición invertida** | Construcción donde el fragmento se clona en sentido y en antisentido separados por un intrón o espaciador, de modo que el transcrito se pliega sobre sí mismo formando ARNdc (P4, P5) | Es la forma concreta de producir ARNdc en una bacteria o en una planta; en P5 el tallo mide 147 y 140 pb y el lazo 199 pb |
| **Lisado crudo sonicado** | Extracto bacteriano roto por ultrasonido y centrifugado, aplicado sin purificar (P5) | Es la versión más barata posible del producto, y la que P5 demuestra que funciona |
| **Cy3 y ALEXA FLUOR 488** | Fluoróforos conjugados al ARN para seguirlo por microscopía (P4 y P7 respectivamente) | Es cómo se "ve" el ARN dentro del tejido; y en P4 los propios autores advierten que ver el fluoróforo no prueba que el ARNdc esté intacto |
| **Cuantificación absoluta por qPCR con sonda** | Asignar una concentración real a cada Ct contra una curva de calibración hecha con un fragmento sintético de referencia (P7) | Es la diferencia entre "bajó" y "bajó de X a Y": P7 reporta carga viral en attomol/µL, no en veces de cambio |
| **GeNorm y valor M** | Método para evaluar la estabilidad de un gen de referencia en RT-qPCR; en P1, M de 0,05 y 0,07 para actina | Es el control de calidad que decide si un porcentaje de knockdown significa algo |
| **Método de Pfaffl** | Cuantificación relativa de qPCR que corrige por la eficiencia real de cada par de cebadores, a diferencia del 2^-ΔΔCt que la asume en 2 (P7) | Dos papers del corpus usan métodos distintos: sus porcentajes no son estrictamente comparables entre sí |
| **Criterio de exclusión por rango intercuartílico (IQR)** | Descartar del análisis los individuos cuyo valor supera 1,5 o 3 veces el rango intercuartílico; en P6, los tratados con expresión por encima de la media y la mediana del control | Es la decisión metodológica que convierte el silenciamiento reportado en el del subconjunto que sí recibió el ARNdc, y hay que leerla antes de usar el número |
| **Auchenorrhyncha** | Suborden de Hemiptera que agrupa a casi la mitad de las especies del orden, en su mayoría fitófagas y muchas vectoras (P3) | Es el grupo al que pertenecen *D. maidis* y *D. kuscheli*, y la unidad taxonómica dentro de la cual P3 argumenta conservación funcional |
| **Cicadomorpha / Fulgoromorpha** | Las dos infraórdenes de Auchenorrhyncha: la primera incluye a los cicadélidos como *D. maidis*, la segunda a los delfácidos como *D. kuscheli* (P3) | P3 encontró que el número de motivos de ETH en el precursor sigue esa división: tres en *D. maidis*, dos en *D. kuscheli* |
| **Hemimetábolo** | Insecto con metamorfosis incompleta, sin estadio de pupa, que pasa por estadios ninfales parecidos al adulto (P3) | Distingue a nuestra plaga de los modelos clásicos de RNAi (*Tribolium*, *Drosophila*), que son holometábolos |
| **Adulto teneral** | Adulto recién emergido, con la cutícula todavía blanda y poco pigmentada (P1) | Es el estadio que P1 usa para los bioensayos de dieta, y conviene saberlo para comparar dosis entre trabajos |
| **Motivo FFLKAXXSXPRI** | La secuencia conservada del precursor de ETH, que se escinde en sitios básicos GRR para liberar el péptido maduro (P3) | Es la firma que permite identificar el gen por homología sin tener el genoma anotado |
| **tBLASTn** | Búsqueda de una consulta de proteína contra una base de nucleótidos traducida en los seis marcos | Es la herramienta con la que P3 identificó sus blancos; y es, junto con BLASTn, **todo** el cómputo de diseño del corpus |
| **SCMV (*Sugarcane mosaic virus*)** | Potyvirus que causa el mosaico enanizante del maíz, transmitido por pulgones (P5) | Es el virus del precedente de maíz del corpus; **no** es transmitido por *D. maidis* ni pertenece al complejo del achaparramiento |
| **MDMV (*Maize dwarf mosaic virus*)** | Otro potyvirus de maíz, con hasta 70 % de pérdidas reportadas en maíz dulce (P7) | Ídem. Atención: el SCMV se llamó históricamente MDMV-B, y P5 rotula su propia tabla 2 como "MDMV disease ratings" aunque el trabajo sea sobre SCMV |
| **Necrosis letal del maíz (MLN)** | Enfermedad que aparece cuando un potyvirus y un machlomovirus co-infectan la misma planta (P7) | Es el precedente de que una co-infección viral puede ser cualitativamente peor que la suma, algo a tener en cuenta en un complejo de cuatro agentes |
| **PMMoV y CMV** | *Pepper mild mottle virus* y *Cucumber mosaic virus*, los dos virus modelo de P4 | Ninguno infecta maíz: los números de BioClay vienen de tabaco, Xanthi, caupí y *Arabidopsis* |

### Herramientas, datos y método de la ola 2

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **dsRNA-Engineer** | Servicio web de diseño de ARNdc y tamizaje de off-targets, una de las dos herramientas que entregó el organizador. | Es la herramienta oficial del track: tamiza con Bowtie sobre coincidencia exacta de ventanas de 16, 20-22 y 26 nt, no calcula termodinámica y no estima eficacia. `[E]` — `ola2/W2_herramientas/REPORT.md`. |
| **Primer-BLAST y la tabla SantaLucia 1998** | Herramienta del sitio de BLAST que combina Primer3 con BLAST y calcula la temperatura de fusión (Tm) de cebadores de PCR. | Es la única termodinámica alcanzable desde el enlace oficial, y la explicación más probable de la frase «BLAST calcula la termodinámica» que traía el equipo. `[H]` — `ola2/W2_herramientas/REPORT.md`. |
| **Ventana de k nucleótidos (k-mero)** | Cada subcadena contigua de largo k que se puede derivar de una secuencia deslizando una posición por vez. | Es la unidad real del tamizaje: la herramienta oficial cuenta coincidencias exactas de k-meros y las suma, y el conteo cambia por completo según k. `[E]` — `ola2/W2_herramientas/REPORT.md`. |
| **TSA (*Transcriptome Shotgun Assembly*)** | División del NCBI donde se depositan transcriptomas ensamblados, con prefijo de accesión propio. | Ahí viven los tres transcriptomas del vector que la ola 1 daba por inexistentes: `GITV00000000`, `GHCC00000000` y `GCWP00000000`. `[E]` — `ola2/W3_bases_datos/REPORT.md`. |
| **Identical Protein Groups (IPG)** | Base del NCBI que agrupa proteínas de secuencia idéntica depositadas con accesiones distintas. | Es el puente correcto entre los mapeos de KEGG, que apuntan a accesiones GenBank, y las accesiones WP_ de RefSeq. `[E]` — `ola2/W3_bases_datos/mapeo_identificadores.md`. |
| **EDirect** | Conjunto de utilidades de línea de comandos del NCBI para consultar Entrez de forma encadenable y reproducible. | Es la vía programática que sí funcionó para medir cobertura por organismo cuando el cliente `datasets` falló en el entorno. `[E]` — `ola2/W3_bases_datos/consultas/`. |
| **Completitud estilo BUSCO con miniprot** | Proxy de completitud de un ensamblado: se alinean los ortólogos de un linaje y se cuenta cuántos aparecen con cobertura suficiente. | Es lo que permitió mostrar que los tres ensamblados del vector no son equivalentes (97,7 %, 68,8 % y 35,5 %). No es BUSCO oficial: es un proxy calibrado contra el valor publicado. `[R]` — `ola2/W4_genomas/REPORT.md`. |
| **btop (*blast traceback operations*)** | Cadena compacta que devuelve BLAST describiendo coincidencias y desajustes a lo largo de un alineamiento. | Permitió contar siRNA conservados entre aislados de MRFV sin recorrer los alineamientos a mano, y sirvió de método de verificación cruzada. `[E]` — `ola2/W5_secuencias_epilab/analisis/`. |
| **dustmasker** | Herramienta de BLAST+ que marca regiones de baja complejidad en una secuencia de nucleótidos. | Se usó para descartar que las regiones elegidas por EPILAB cayeran sobre secuencia repetitiva: sólo un intervalo de 7 nt en los cuatro candidatos. `[E]` — `ola2/W5_secuencias_epilab/`. |
| **Aislado (*isolate*) y conservación entre aislados** | Cada muestra de un patógeno recolectada en un lugar y momento concretos; la conservación entre aislados es cuánta secuencia comparten. | Es el concepto que decide si un candidato sirve acá: la región de cápside elegida es 100 % idéntica al aislado de Costa Rica y cae a 91,5-93,5 % contra los brasileños. `[E]` — `ola2/W5_secuencias_epilab/REPORT.md`. |
| **Modelo de tamaño de siRNA (Model I, II, III)** | Clasificación con la que dsRNA-Engineer asigna a cada especie un largo de siRNA de 21, 22 o 24 pb para derivar las ventanas. | Determina el tamizaje de cada especie y **no tiene fuente publicada**: a *D. maidis* le asigna 21 pb y a otro hemíptero, *Peregrinus maidis*, 22 pb, sin seguir la filogenia. `[?]` — `ola2/W2_herramientas/REPORT.md`. |
| **Sondeo de xilema** | Fase del recorrido del estilete en que un insecto chupador de floema perfora y prueba el xilema, documentable por electropenetrografía. | Es la vía de entrega que el corpus habilita: el ARN exógeno llega al apoplasto y al xilema, y no hay evidencia de que entre al floema, que es donde se alimenta el vector. `[R]` — `ola2/W1_papers/REPORT.md`. |
| **V-ATPasa (ATPasa vacuolar de protones)** | Bomba de protones de membrana formada por un sector soluble V1 y uno de membrana V0; es un complejo distinto de la ATP sintasa mitocondrial (F-ATPasa). | **Corrige una definición de la ola 1:** el blanco del candidato `ATPaseD_Dm` del EPILAB es la subunidad D de la V-ATPasa, no de la «ATP sintasa vacuolar» como decía `R1/REPORT.md` §4.6. `[E]` — `ola2/CORRECCIONES.md`, entrada E7. |

### Definiciones corregidas

- **V-ATPasa:** ver la entrada de arriba. `R1/REPORT.md` §4.6 la llamaba «ATP sintasa
  vacuolar», que es otro complejo. El término unificado en todo el repositorio es
  «subunidad D de la ATPasa vacuolar de protones (V-ATPasa)».

### Términos que agrega el port de si-Fi21 (2026-10-19)

Origen: `tools/sifi21_port/` y `research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md`.

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **Selección de hebra guía (*strand selection*)** | Regla que decide cuál de las dos hebras del dúplex de 21 nt se carga en Argonauta y cuál se descarta: gana la que tiene el extremo 5' termodinámicamente menos estable. | Es el primero de los tres filtros de si-Fi21 y el que más peso tiene en el veredicto. Si la hebra que se carga es la pasajera, el siRNA no silencia el blanco aunque la secuencia sea correcta. `[E]` — `tools/sifi21_port/CAMBIOS.md`. |
| **Estabilidad de extremos (*end stability*)** | Diferencia de energía libre entre los dos extremos 5' del dúplex; si supera 1 kcal/mol, el siRNA pasa el filtro. | Implica matemáticamente la condición de selección de hebra, así que con los dos filtros activados el primero no aporta nada. Vale saberlo al leer el desglose de un perfil. `[E]` — `tools/sifi21_port/README.md`. |
| **Regla terminal de si-Fi21** | Condición sobre los nucleótidos 19 y 2 del siRNA que el programa aplica después de los filtros termodinámicos. | **No es un filtro: es una ramificación**, y una de sus ramas declara eficiente un siRNA que falló la termodinámica. Medido ventana por ventana: 19 de 133 «eficientes» en `MP_MRFV`, 50 de 212 en `BicC_Dm`; entre el 14 % y el 24 % segun el gen, y ninguna ventana va en sentido contrario. Es la razón por la que nuestro port tiene un modo corregido. `[E]` — `CAMBIOS.md` C1. |
| **Modo fiel y modo corregido** | Los dos modos de nuestro port: uno reproduce si-Fi21 tal como es, defectos incluidos; el otro aplica los arreglos justificados. | El fiel hace falta para auditar números ya producidos con si-Fi; el corregido, para diseñar. La diferencia entre los dos es un dato medible, no una molestia. `[E]` — `DECISIONS.md` D13. |
| **Perfil de eficiencia y densidad de eficientes** | Cuántos siRNA eficientes contiene cada región candidata de largo fijo, a lo largo del gen; es la «curva de subiditas y bajaditas» que describió el investigador. | Es la variable de decisión: elegir región es elegir un punto de esa curva. **Cuidado con la brecha contra el máximo**: el máximo de cientos de regiones superpuestas está sesgado hacia arriba y entre la mitad y casi toda esa brecha es artefacto; la cantidad falsable es el percentil. `[E]` — `genes/index.html` y `W7_ranking/REPORT.md` §1.2. |
| **Bloque contiguo perfecto de ≥19 nt** | Criterio de riesgo de off-target: dentro del siRNA de 21 nt hay 19 o más nucleótidos seguidos idénticos a un transcrito no objetivo. | Es el umbral publicado que usa nuestra rúbrica y el criterio principal del tamizaje. No implica buscar siRNA más cortos: la molécula sigue midiendo 21, lo que se relaja es cuánto tiene que coincidir. `[E]` — Cedden 2026, ver `FUENTES.md`. |
| **Desajuste único (*one mismatch*)** | Criterio más amplio: los 21 nt alineados con un no objetivo pero con exactamente una letra distinta. | Un siRNA así todavía puede cortar, más débilmente, así que es riesgo real. Agregarlo no da vuelta ninguna de nuestras comparaciones de región, pero sí sube los conteos: en `BicC_Dm` de 33 a 44 ventanas comprometidas. `[E]` — `sifi21_reproduccion.md` §4. |
| **Aho-Corasick** | Autómata que busca miles de patrones en un texto en una sola pasada, independientemente de cuántos patrones sean. | Es lo que permite tamizar off-targets por coincidencia **exacta** en vez de con la heurística de semillas de BLAST, sin instalar BLAST y sobre 379 MB de referencias. Reprodujo los conteos de bloque perfecto de W5 en las 20 celdas. `[E]` — `tools/sifi21_port/offtarget_21nt.py`. |
| **Ventana riesgosa contra ventana riesgosa y activa** | Distinción entre un siRNA que coincide con un no objetivo y uno que además pasa los filtros de eficiencia. | Es la que conviene llevar al diseño: una ventana que no se carga en el complejo silenciador no corta nada, ni en el blanco ni fuera de él. En `MP_MRFV` hay 22 ventanas con off-target y sólo 2 son eficientes. `[H]` — `genes/MP_MRFV.html`. |

## Términos del ranking de candidatos (2026-10-20)

Origen: `tools/sifi21_port/ranking.py` y `research/ola2/W7_ranking/`.

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **Percentil de la región elegida** | En qué lugar queda la región que eligió EPILAB dentro de la distribución del conteo de eficientes sobre **todas** las regiones del mismo largo de ese gen. | Reemplaza a «está 21 % por debajo del óptimo», que no es falsable porque el óptimo es un máximo sobre cientos de regiones superpuestas y está sesgado hacia arriba por construcción. El percentil sí lo es: `MP_MRFV` está en el 91 y las otras tres en la mediana. `[E]` — `REPORT.md` §1.2. |
| **Nulo de etiquetas contra nulo de bloques** | Dos formas de barajar: repartir al azar la etiqueta «eficiente» entre todas las ventanas, o permutar bloques contiguos de 30 ventanas conservando lo que pasa adentro de cada uno. | **Es lo que separaba nuestras dos mediciones contradictorias.** El primero destruye la estructura local y da 3 de 4 genes significativos; el segundo la preserva y da 0 de 4, igual que el resultado del 7,2 %. Elegir nulo es elegir qué pregunta se contesta. `[E]` — D15. |
| **Sesgo del máximo sobre regiones superpuestas** | Tomar el máximo de cientos de regiones que se pisan entre sí produce un valor muy por encima de la media aunque no haya ninguna señal. | Medido acá: barajando las etiquetas al azar, el máximo queda entre un 17 % y un 46 % por encima de la media. Entre la mitad y casi toda la «brecha contra el óptimo» de `sifi21_reproduccion.md` §3 es este artefacto. `[E]` |
| **Regiones independientes** | El largo del gen dividido el largo de la región: cuántas regiones verdaderamente distintas hay, frente a las cientos de posiciones deslizantes. | Es el *n* efectivo. Acá vale entre 1,6 y 8,3, así que una correlación calculada sobre 2.201 regiones deslizantes **no** tiene 2.201 observaciones y no admite un valor p. Es la razón por la que dos de nuestras cuatro correlaciones no se interpretan. `[E]` |
| **Eficacia y limpieza** | Los dos ejes del ranking, los dos como fracciones sobre las ventanas de la región: cuántas son eficientes, y cuántas quedan limpias descontando cada sucia por la gravedad de su peor acierto. | Al ser tasas y no conteos, son comparables entre regiones de 200 y de 300 nt, que es lo que hace comparables a los cuatro candidatos de EPILAB entre sí. `[H]` — D16. |
| **El peor acierto contra la suma de aciertos** | Que el riesgo de una ventana sea su coincidencia más grave y no la suma de todas sus coincidencias. | Si una ventana ya pega perfecto en maíz hay que sacarla, y que además pegue en fauna del suelo no la hace cualitativamente peor. Sumar haría que seis aciertos leves pesaran como uno grave. Es una decisión de contenido, no de implementación. `[H]` — D18. |
| **Veto duro contra penalización** | Tratar la coincidencia perfecta de 21 nt con un no objetivo como un descarte de la región entera, en vez de como un término que baja el puntaje. | Un veto no se puede comprar con eficiencia y una penalización sí. Acá decide: deja afuera las regiones elegidas de `BicC_Dm` y `ATPaseD_Dm` y a ninguna de las dos virales. `[H]` — D16, D17. |
| **Barrido del símplex** | Sortear miles de juegos de pesos sobre el espacio de todos los repartos posibles y reportar la frecuencia de cada candidato en cada posición, en vez de un orden bajo pesos elegidos a dedo. | Es lo que convierte un ranking en una afirmación defendible: contesta si el orden depende de pesos que nadie justificó. Acá sobreviven los dos primeros puestos y no el tercero. `[E]` — antecedente en `pipeline/REPORT.md` §5. |
| **Escala absoluta contra min-max** | Normalizar los ejes contra su propio significado, o contra el mejor y el peor candidato del conjunto. | **Con dos candidatos, min-max es degenerado**: manda uno a 0 y el otro a 1 en cada eje, de modo que un 50/50 no es un empate medido sino la escala. Está fijado como prueba para que nadie lo cite como hallazgo. `[E]` — `test_ranking.py`. |
| **Cruce entre observado y esperado por azar** | El tamaño de ventana en el que lo que se encuentra deja de ser menos de lo que predice el azar y pasa a ser más. | Está entre **17 y 18 nt**, medido sobre los cuatro genes y cinco referencias. Por debajo, lo que aparece es ruido; por arriba, homología. Es el argumento estadístico que acompaña a la evidencia biológica del 21. `[E]` — `azar_por_k.md`. |
| **Nulo por barajado de la referencia** | Mezclar las bases de un genoma conservando su composición exacta y volver a buscar, para separar lo que explica la composición de lo que explica la estructura. | A 20 y 21 nt una referencia barajada produce **cero** coincidencias donde la real produce 54 y 46: a ese tamaño el azar no explica nada. Y a 15 nt coincide con la cuenta analítica por composición, lo que valida las dos. `[E]` |

## Términos de la ola 3 (2026-10-21)

| Término | Definición | Por qué nos importa |
| --- | --- | --- |
| **`RNA_NN4`** | Tabla de parámetros de vecinos más cercanos (*nearest neighbours*) que `sifi21INTA` y Apolo Rocket usan por defecto en vez de la de Chen *et al.* 2012; el comentario del código la atribuye a Zuber *et al.* 2022. | Es el **único cambio químico** entre si-Fi21 y la versión del INTA, y mueve los conteos sólo −4, +1, −5 y 0 sobre los cuatro genes. La atribución es del comentario: el artículo no se abrió. `[R]` |
| **Blanco principal (*main target*)** | La región o secuencia que el usuario declara como objetivo deseado; todo acierto fuera de ella cuenta como off-target. | Es una **decisión humana sin registro** —`input()` por consola en una librería, una lista de números en el JSON en la otra— de la que depende por completo la columna de eficientes sin off-targets, que es la única que mira especificidad. `[E]` |
| **Bypass de la regla terminal** | La rama del criterio de si-Fi que devuelve «eficiente» mirando sólo la accesibilidad, sin el veredicto termodinámico. | Está **viva en las tres implementaciones públicas** que leímos, y explica entre el 14 % y el 24 % de lo que el programa reporta como eficiente. `[E]` |
| **Plegado local (*local folding*)** | Predicción de estructura secundaria restringiendo el alcance máximo de los apareamientos a L nucleótidos, en ventanas de tamaño W. | Es el **único régimen con exactitud medida** para ARN largos —mediana ~0,65 contra ~0,55 del global— y es lo que corre si-Fi21 (W = 80, L = 40). Fija dónde podemos hablar de estructura y dónde no. `[E]` |
| **Tramo perfecto (*perfect stretch*)** | Bloque contiguo de nucleótidos idénticos entre dos secuencias. | El riesgo de ARNi se rige por tramos perfectos y no por identidad promedio. Es la unidad en la que están los umbrales con bioensayo: 21 nt contiguos embebidos en un ARNdc de ≥ 60 nt. `[E]` |
| **TSA (*Transcriptome Shotgun Assembly*)** | Base del NCBI donde se depositan transcriptomas ensamblados. | Los genes publicados de cicadélidos vectores **viven ahí y no en RefSeq**, así que una búsqueda que sólo mire RefSeq los pierde. `[E]` |
| **Razón de riesgo (*hazard ratio*)** | Medida de efecto en análisis de supervivencia: cuántas veces más probable es el evento en un grupo que en el control. | Es la variable respuesta del **único experimento de eficacia en insectos** que usamos, y por eso aparece en toda la discusión de proxies. `[E]` |
| **HSP (*high-scoring segment pair*)** | La unidad de resultado de BLAST: un tramo alineado con puntaje alto, no un parámetro configurable. | Es nuestra lectura de lo que el investigador transcribió como «HCP». Importa porque los parámetros que sí llevan HSP en el nombre —`-max_hsps`, `-qcov_hsp_perc`— **no son los que deciden** sobre una ventana de 21 nt: el que decide es `-word_size`. `[H]` la identificación, `[E]` lo demás. |
| **Quimera (*chimeric dsRNA*)** | Un solo ARNdc armado concatenando fragmentos de genes distintos, que se vuelve a evaluar como una sola molécula. | Es la técnica que propuso el investigador en el Checkpoint 1. En la literatura aparece además como *multi-target*, *fusion dsRNA* y «recombinación artificial de fragmentos»; **no existe ninguna técnica de ARNi llamada «mecha»**. Medimos que, con regiones ya optimizadas, no suma eficiencia y sí puede fabricar off-targets (D43). `[R]` el nombre, `[M]` lo medido. |
| **Empalme (de una quimera)** | El punto donde se pegan los dos fragmentos, y las 20 ventanas de 21 nt que quedan a caballo de él. | Es la única secuencia **nueva** de una quimera: no existe en ninguno de los dos genes, así que ahí hay que recalcular eficiencia y off-targets. Es donde apareció el acierto en maíz y los 21/21 contra el genoma del vector. `[M]` |
| **Banda de contexto** | El tramo a cada lado de un borde o de un empalme donde el veredicto de una ventana puede cambiar sin que cambie su secuencia. | Es **asimétrica**: 72 nt corriente abajo y 59 corriente arriba, porque si-Fi21 mide la accesibilidad de un tramo de 8 nt al final de la ventana, con plegado local de 80. Verificado en 204 ventanas cambiadas de cuatro tablas, sin una sola violación. Corrige el techo único de 59 nt que había estimado C4. `[M]` el número, `[H]` la derivación. |

## Términos que agrega la interfaz del port (2026-10-23)

Origen: `sifi_plus/` y `DECISIONS.md` D55 a D59.

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **Curva de solapamiento** | Cuántos siRNA eficientes se superponen a cada posición del ARNm; es la curva roja del «RNAi design plot» del si-Fi21 original (`show_plot.py`, `np.bincount`). | Es la curva de **paridad**: la que el investigador reconoce de su pantalla, y la que se reprodujo tramo por tramo —ocho tramos, máximo 9 en 150-156 y 8 en 287-297 en `ATPaseD_Dm`—. No hay que confundirla con la densidad por región: su máximo posible es el tamaño de la ventana. `[M]` — `sifi_plus/test_api.py`. |
| **Línea de todos los siRNA** | Cuántos siRNA cualesquiera cubren cada posición: plana en el tamaño de la ventana salvo en los dos bordes del gen. | Es una constante, no una serie, así que se dibuja gris y punteada con etiqueta directa en vez de competir por un color. En el original es la línea azul. `[R]`. |
| **Baja complejidad de una ventana** | Ventana cuya racha de un mismo nucleótido mide 10 nt o más, o que tiene dos nucleótidos distintos o menos. Criterio nuestro, declarado en `sifi_plus/complejidad.py`. | Sin esta marca el conteo de off-targets mezcla poli-A con homología: las 9, 11 y 13 coincidencias perfectas de 21/21 nt del genoma del MRFV en *Harmonia axyridis*, *Apis mellifera* y *Zea mays* son **todas** la cola de poli-A, y descontándolas las tres caen a cero. El original no lo marca en ningún lado. `[M]` — D59. |
| **Cadena de configuración** | La forma en que el investigador declaró la suya, `siFi21_8_1.0_0.1_1111`: ventana de accesibilidad, umbral de extremos, umbral de accesibilidad y las cuatro casillas. | Es el modo de nombrar una corrida sin ambigüedad. La interfaz la muestra y la parsea, así que se puede pegar la suya y ver el panel acomodarse. El orden de los cuatro dígitos es el del panel y con `1111` el dato original no permite distinguirlo: esa parte es lectura nuestra. `[H]` — D45, D57. |
| **Rango candidato guardado** | Un tramo del gen con su nombre, sus coordenadas, sus conteos y **la configuración que los produjo**; nunca la secuencia. | Un conteo sin su modo y su motor no significa nada: los mismos cuatro genes dan cuatro números distintos según cuál de los dos RNAplfold corrió. Por eso la configuración viaja con el rango y no al lado. `[M]` — D56. |
| **Contrato del gráfico** | El JSON que `sifi_plus/perfil.py` emite y que consumen los dos dibujantes: el interactivo del navegador y el informe estático de `informe_html.py`. | La fuente única no es el código de dibujo sino el modelo de datos. Es lo que evita una cuarta copia de algo: el repositorio ya tiene la regla de eficiencia escrita tres veces. `[E]` — D58. |
| **Conteo por incrementos** | La regla con la que la plataforma del laboratorio cuenta siRNAs eficientes: la suma de los incrementos positivos de la curva de cobertura. Equivale a contar los arranques eficientes cuyo antecesor a veinte posiciones no es eficiente. | Es la explicación de la brecha entre la planilla y cualquier corrida del criterio: convierte 138, 40, 218 y 35 en 114, 35, 199 y 33, exactos. Esconde entre el 5,7 % y el 17,4 % de las ventanas según el gen, y el sesgo no es constante, así que dos cifras de la planilla no son comparables entre sí. `[M]` — D62, `research/ola5/N1_regla_de_conteo/`. |
| **Ancho de cobertura** | Cuántas posiciones de la curva ocupa una ventana eficiente. No es el tamaño del siRNA aunque se parezca: el gráfico del si-Fi21 original usa 21 y la curva histórica del laboratorio usa 20. | Es la clase de parámetro que se deriva sin pensarlo y después nadie puede auditar. Con 21 nuestra curva reproduce las tres marcas leídas de la pantalla del programa; con 20 las tres caen un nucleótido antes. `[M]` — `research/ola5/N2_ancho_de_cobertura/`. |
| **Marco de conteo** | Cuál de tres conjuntos de ventanas se cuenta para una región: los `L` arranques que caen dentro de ella en el gen, los `L − 20` que existen en la molécula pero plegados en el gen, o los `L − 20` de la molécula plegada sola. | Un conteo sin marco no se puede comparar con otro: medidos los tres en seis regiones, el recorte **baja** el conteo en tres y lo **sube** en tres. La cifra que se publica es la de la molécula, porque es la que existe. `[M]` — D63, `research/ola5/N3_marcos/`. |
| **Ventana de juntura** | Una de las veinte ventanas de 21 nt que quedan a caballo de la unión de dos fragmentos en una quimera. | No existe en ningún transcrito, porque la unión es secuencia que el ensamblado fabrica: una quimera **canjea** los veinte arranques de cola de cada fragmento por veinte de juntura. De las 240 de las doce quimeras, 4 son eficientes y ninguna de esas 4 tiene blanco continuo: es capacidad de silenciamiento gastada que el conteo cuenta como si valiera. `[M]` — `research/ola5/N4_quimeras/`. |
| **Región candidata** | Una región elegida con el criterio del ranking que todavía **no** pasó por el inventario de alertas de `M6`. | No es lo mismo que región recomendada. Desde `D72` la compuerta **rechaza** una región ausente del inventario con `alertas.RegionNoTamizada`, así que una región nueva no puede presentarse como recomendada hasta que se la tamice. Primer caso: `V-ATPase B` 517-816 en `O3` (`D74`). `[H]` |
| **Bloque fabricado por el empalme** | Un tramo perfecto de 19 nt o más que toma nucleótidos de los dos genes de una quimera, así que no existe en ninguno de los dos. | Es la distinción que decide si una juntura genera alerta: un bloque de 19 nt que entra entero en el aporte de un solo gen lo **hereda** la quimera y ya estaba medido; el que cruza la unión es secuencia nueva y hay que tamizarlo. En `O3`, el empalme de un orden fabrica tres bloques que coinciden en maíz y el del orden inverso fabrica cero, y eso es lo que decide el orden. `[M]` — `research/ola6/O3_quimera_bicc_vatpase_b/`. |
| **Isla admisible** | Tramo maximal de ventanas consecutivas sin veto de off-target, dentro del cual caben los arranques de un fragmento. | Las islas que el veto deja son **angostas**: la única de 300 nt de `V-ATPase B` mide 21 nt de ancho. Una grilla gruesa anclada en el origen no las ve —con paso 50 la retícula no toca ninguna de esas 21 posiciones—, así que la enumeración de `O4` se ancla a los extremos de cada isla y no sólo a la posición 1 (`D76`). `[M]` |
| **Objetivo declarado antes de rankear** | La cuenta bajo la cual una enumeración ordena sus candidatos, fijada **antes** de enumerar y repetida en cada fila de la salida, no sólo en el encabezado. | Con tres cuentas por candidato y dos órdenes, elegir cuál ordena después de ver los resultados elige el ganador sin falsear ningún número. Medido: el primer puesto cambia según el objetivo, y el de eficiencia pura asciende un candidato que fabrica un bloque de ≥ 19 nt (`D75`). `[M]` el hecho, `[H]` la regla. |
| **Aporte de un bloque fabricado** | Cuántos nucleótidos toma de cada uno de los dos genes el bloque que coincide con una referencia cruzando la unión; se reporta el del gen menos representado. | Un bloque de 19 nt con aporte 1 es el gen solo más un nucleótido, y **existe por azar en una de cada cuatro** referencias que contengan al gen padre, porque basta con que el nucleótido siguiente coincida; uno repartido 10/9 es otra cosa. Sin el aporte, la alerta de juntura mezcla las dos. `[M]` la frecuencia observada, `[H]` la lectura. |
| **Ortología recíproca (*reciprocal best hit*, RBH)** | Dos secuencias de especies distintas son ortólogas recíprocas si cada una es el mejor hit de la otra al alinear en las dos direcciones. | Es la regla de `F1` para transferir un nombre: elegir «el gen que se llama igual» ya está medido como roto (`C5`, 65 % de diferencia). Los empates en el primer puesto son su punto débil en un transcriptoma redundante (`D84`). `[M]` el método, `[H]` la lectura. |
| **ORF (*open reading frame*)** | Tramo de un marco de lectura entre dos codones de parada, aquí de ≥ 100 aminoácidos y sin exigir ATG. | `F1` traduce los seis marcos y alinea todos los ORF, no sólo el más largo: con uno solo por contig se perdía la V-ATPasa B, que está en la hebra opuesta de un gen más largo. |
| **Banda de concordancia** | Para una identidad de aminoácidos dada, la frecuencia con la que dos ortólogos recíprocos llevan el mismo nombre, medida en `C12` (76 % a 86 %, IC95 de Wilson). | Es lo que impide que «es una subunidad de la V-ATPasa» se lea como cierto: viaja al lado de cada anotación transferida. Es una cota de consistencia entre nombres de RefSeq, no de función. `[M]` |
