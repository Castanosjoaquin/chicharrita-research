# Checkpoint 1 — reunión con el investigador invitado

**Fuente:** `Checkpoint1.mp4` (raíz del repo, 25 min 20 s).
**Transcripción:** local, faster-whisper `large-v3`, español, VAD activado. El
audio no se subió a ningún servicio.
**Marcadores:** todo lo de este documento es `[R]` salvo aclaración — es lo que
dijo una persona en una reunión, no literatura revisada. Lo que el investigador
presenta como mecanismo consolidado va como `[E]`, y lo que queda sin resolver
está en la sección de pendientes.

---

## Resumen

El investigador — biólogo de formación, con años de trabajo en bioinformática
aplicada — nos encuentra arrancando de cero en biología y lo asume como punto
de partida: dedica el primer tercio de la reunión a verificar que entendimos el
mecanismo y corrige dos cosas que teníamos mal. La más importante es que las
bacterias quedan fuera: el ARNi no opera sobre ellas, así que la rama del
complejo patogénico que pensábamos atacar por esa vía se cae. La segunda es de
encuadre: la chicharrita no es el problema en sí, es el vector.

De ahí sale una bifurcación que él valida como las dos estrategias legítimas:
pegarle al insecto, o pegarle al patógeno dentro de la planta. Recomienda la
primera por ser más directa, y nosotros agregamos un argumento que él acepta —
el período de latencia de unos 20 días entre que la chicharrita se infecta y
puede transmitir abre una ventana para matarla antes.

El núcleo técnico de la reunión es cómo se decide que un diseño de ARN es
bueno. El criterio que usa su equipo viene de **si-Fi21**: se corre una ventana
de 21 nucleótidos a lo largo de todo el gen y para cada posición se evalúa si
pasa un umbral que combina energía libre, identidad y estructura secundaria. El
resultado es un perfil con picos y valles, y el diseño consiste en elegir la
región de entre 150 y 250 nucleótidos con mayor densidad de ventanas
eficientes. El límite de ese enfoque lo marca él mismo y es lo que más nos
sirve: **no hay datos empíricos suficientes** sobre cómo se plieguan los ARN
largos ni sobre qué los hace eficientes, así que no hay nada que entrenar.
Quien resuelva eso, dice, se gana un Nobel como el de AlphaFold.

Sobre qué espera de nosotros fue explícito y acotó expectativas dos veces.
Construir una plataforma propia no es realista — él lleva cinco meses
arreglando la que tienen. Lo que sí quiere es un **benchmarking** de si-Fi21,
dsRNA-Engineer y BLAST sobre los cuatro genes que ya nos dieron, y un
**ranking** de candidatos. Y marcó el criterio de evaluación con claridad:
*"no porque tenga que ser cierto eso que decís, porque al final hay que
evaluarlo, sino el pensamiento que nos llevó a ustedes para decidir ese
ranking"*. Se evalúa el razonamiento, no el acierto. Agregó dos extensiones
opcionales: incorporar genes nuevos que encontremos en la literatura, y
documentar qué mejoras le haríamos a las herramientas aunque no las
implementemos.

Un dato que reordena lo que pensábamos del material: los cuatro diseños del
Excel **son suyos, de hace unos dos años, y nunca se testearon** — bajó la
incidencia de la plaga y se quedaron sin material experimental. Los llamó
"medio viejos" y no recordaba con certeza por qué eligió esas regiones. El
ejercicio deja de ser reproducir un resultado validado y pasa a ser auditar una
decisión vieja de la que ni el autor está seguro.

Por último, validó el camino que ya habíamos tomado con el genoma no anotado de
*Dalbulus maidis*: mapear contra especies anotadas para recuperar genes
candidatos. Lo describió como ingeniería inversa y nos dio el circuito
completo, con la advertencia de chequear identidad en cada paso.

---

## Transcripción por temas

### Presentación y punto de partida

Arranca preguntando de dónde somos y en qué año estamos. Le contamos que
Ingeniería en Inteligencia Artificial en la Universidad de San Andrés, y que
todo esto es un ámbito nuevo para nosotros: el fin de semana se nos fue primero
en entender los conceptos. Pregunta qué nos llevamos de la charla del viernes y
qué entendimos mal. Le respondemos que al principio entendimos poco y nada.

### El problema: la chicharrita es el vector

Nuestro resumen inicial fue que hay un insecto que contagia un virus a la
planta. Nos corrige el encuadre: `[E]` la chicharrita en sí no es el problema,
el problema es que es el **vector** que transporta virus y bacterias hasta la
planta.

Más adelante aclara que una chicharrita puede portar ninguno, uno, dos, tres o
los cuatro agentes del complejo a la vez.

### El mecanismo de ARNi

Le planteamos que la idea es silenciar genes por interferencia. Confirma y
define la cadena completa: `[E]` silenciar un gen significa que no produzca su
proteína; si esa proteína es esencial para vivir, el organismo muere.

Nosotros habíamos entendido que al entrar el ARN al organismo "lo parte en 21
pedacitos". Lo precisa: `[E]` existen mecanismos **endógenos** en insectos,
hongos, plantas y virus que agarran ARN de doble cadena y lo cortan en
fragmentos de 21 nucleótidos. Esos fragmentos los toma otra proteína, que los
lleva hasta el gen del organismo y corta donde encuentra **homología** de
secuencia (A, C, G, T).

El punto que corrige de raíz nuestro planteo: `[E]` **las bacterias no tienen
este mecanismo.** Cuando preguntamos si convenía apuntar a los genes esenciales
del insecto o de las bacterias, la respuesta fue *"de las bacterias
olvídense, porque son otros mecanismos"*.

### Las dos estrategias posibles

Le planteamos la bifurcación: atacar a la chicharrita, o atacar dentro de la
planta para que el virus no se pueda reproducir. Responde que son **dos buenas
estrategias**, y recomienda la del insecto porque es más directa —
*"si vos le pegás a la chicharrita y tratás de matar a la chicharrita, es más
fácil directamente"*.

Agregamos el argumento del período de latencia: `[R]` hay un ciclo de unos 20
días entre que la chicharrita se infecta y el momento en que puede transmitir a
la planta, y en esa ventana se la puede matar antes de que contagie. Lo
confirma: *"es en ese tiempo"*.

### Alcance: diseño sí, formulación y ensayo no

Preguntamos cómo se diseña efectivamente una molécula y con qué programas.
Separa la cadena en etapas y nos ubica en la primera: el **diseño** es nuestro
terreno; encapsularlo, aplicarlo a la planta, lograr que entre y armar el
diseño experimental para probarlo es trabajo de laboratorio.

### Nuestra propuesta de enfoque y su reacción

Le explicamos que, como de biología sabemos poco, la idea es trabajar sobre los
cuatro diseños que ya tienen: rankearlos para ver cuáles tienen más potencial y
que el laboratorio no tenga que probarlos todos. Responde *"perfecto"* y
pregunta si ya los habían probado — lo que abre el tema siguiente.

### Los cuatro diseños del Excel: origen y estado

Dato importante y no evidente en el material: `[R]` los cuatro diseños los hizo
**él mismo**, entre los primeros que diseñó cuando entró al laboratorio, hace
alrededor de dos años. Nunca se testearon: *"después bajó la incidencia y no
pudimos testearlos"*. Los describe como *"medio viejos"* y encuadra el
ejercicio como preparación: *"estemos preparados para la próxima"*.

Sobre el criterio con el que eligió la región 1–200 de cada gen, más adelante
admite que no lo recuerda: *"probate dos, tres más a ver si, en teoría, debería
haber elegido los que más tienen eficientes, pero tal vez no (…) tal vez porque
tenía [off-targets], no me acuerdo, la verdad, fue hace dos años"*.

### Las herramientas: si-Fi21 y dsRNA-Engineer

Nos dirige a **si-Fi21** — lo dicta letra por letra y aclara que hay un paper
asociado que explica el método. `[R]` Es la base que usa su equipo, y sobre esa
base están construyendo ellos mismos una capa de estructura de proyectos,
visualización, descarga de archivos y contexto propio del laboratorio.

`[R]` si-Fi21 usa **energía libre** como método principal para determinar si una
molécula es eficiente, más algunas métricas de estructura secundaria.

Sobre la carpeta que nos compartieron, mencionamos que hay un programa
—**dsRNA-Engineer**— que *"no anda bien"*. Él confirma la limitación y agrega
contexto: `[R]` el programa que usan *"corre en Windows nada más"* y es viejo.
Se define como biólogo de formación que trabaja en informática desde hace mucho
y no lee código, y cuenta que ahora, con asistentes de código, lo está
arreglando y mejorando.

### Cómo se calcula la eficiencia: la ventana de 21 nucleótidos

Esta es la explicación central de la reunión. `[E]`/`[R]` El procedimiento:

La ventana es de 21 nucleótidos porque ese es el tamaño en que la maquinaria
celular corta físicamente. Entonces se corre esa ventana a lo largo de toda la
secuencia y para cada posición se calcula la eficiencia: si pasa un umbral que
combina energía libre, identidad y estructura secundaria, esa ventana cuenta
como eficiente; si no, no.

El resultado es un **perfil con picos y valles** a lo largo del gen — él lo
llama un plot *"con subiditas y bajaditas"*. Conceptualmente: en un gen de 1000
nucleótidos hay que elegir la región que concentre la mayor cantidad de
ventanas eficientes.

`[R]` El tamaño de región que usan es de entre **150 y 250 nucleótidos**, y el
criterio es empírico, no teórico: *"eso lo sabemos porque empíricamente
hablamos con largos y no funciona"* — con fragmentos largos no funciona, con
más cortos sí. Y usan **distintos genes**, no uno solo.

### Cómo leer el plot y elegir la región

Nos muestra un plot y lo recorre. Arriba están las secuencias; para cada
ventana de 21 se marca si es eficiente o no. En el ejemplo, las primeras 13
posiciones están en cero, y a partir de la 13 el perfil se levanta.

Nos plantea el ejercicio sobre un gen de 800: si hay que elegir 200
nucleótidos, cuál región se elige. Mirando el dibujo la respuesta es obvia —
*"vas a agarrar la primera, porque es la mayor cantidad"*. Pero inmediatamente
introduce la tensión real del problema: esa región con muchas ventanas
eficientes puede resultar que **también le pegue al humano y al maíz**. En ese
caso hay que ir a buscar otra región, tal vez una con menos densidad pero
limpia de off-targets: *"mira este no tiene ninguno, bueno, tal vez me conviene
quedarme con esto"*.

Preguntamos si eso se mide con un promedio. Responde que no hace falta
calcularlo: el programa mismo cuenta cuántas ventanas eficientes hay de tal
posición a tal otra.

### El flujo de trabajo concreto que nos propone

Operativamente, con la tabla que ya tenemos: `[R]` el Excel trae para cada gen
cuántas ventanas eficientes tiene el gen entero (114, 130) y cuál es la región
seleccionada (1 al 200), pero **no trae el número de eficientes de esa región
recortada**. Eso es lo que nos pide calcular, y sugiere dos caminos:

1. Recortar la región, subirla como archivo nuevo a la herramienta y dejar que
   calcule la eficiencia sólo para ese fragmento.
2. Correr el gen entero, verificar si efectivamente da esos 114, mirar el plot
   y comparar con lo que muestra la tabla —
   *"tratá de llegar al mismo resultado"*.

También sugiere escribir código propio que vaya cortando de a 200 a lo largo
del gen, y agregar al Excel una columna con el número obtenido para cada
región.

### Quimeras: combinar regiones de genes distintos

`[R]` Una vez elegida la mejor región de un gen, se puede repetir el
procedimiento con otro gen y **pegar los dos fragmentos** en una sola molécula.
Lo llama *quimera*: se extraen los 200 nucleótidos de mayor densidad de un gen,
los 200 del otro, y se obtiene una secuencia de 400 que se vuelve a evaluar.

El punto fino que marca: la eficiencia total *"en general siempre era la suma
entre uno y otro, salvo en la unión"*. La unión es secuencia nueva — las
ventanas de 21 que caen a caballo del empalme no existían en ninguno de los dos
genes originales, así que hay que recalcular, y ahí el número puede subir o
bajar. Y después hay que correr off-targets sobre la quimera completa, no sobre
los fragmentos por separado.

### Off-targets, BLAST y mismatches

Mencionamos BLAST, que nos habían recomendado. Lo confirma y define: `[E]`
BLAST busca identidad entre una secuencia y otra en distintas ventanas, y es
uno de los parámetros que se usan para evaluar eficiencia además de off-targets.

El punto clave que agrega: `[E]` no hay que buscar sólo ventanas de 21
**exactamente iguales**. Dentro de esos 21 nucleótidos pueden haber
**mismatches** — posiciones donde el gen del otro organismo tiene una base
distinta — y BLAST detecta esos casos. Menciona que BLAST tiene parámetros
propios para decidir cuán parecidas son dos secuencias.

> **Nota de transcripción:** el parámetro que nombró se transcribió como "HCP".
>
> **Corregido el 2026-10-20.** La nota anterior decía que no corresponde a ningún
> parámetro conocido de BLAST, y eso estaba mal: **«HCP» es casi con seguridad
> HSP**, *high-scoring segment pair*, que es un término central de BLAST. En
> `blastn` 2.17.0 hay dos parámetros que lo usan, verificados en el texto de ayuda
> del binario: **`-qcov_hsp_perc`** («percent query coverage per HSP») y
> **`-max_hsps`**. Cuál de los dos nombró sigue siendo `[?]` y se le pregunta, pero
> ya no en abstracto. Detalle que importa: `-qcov_hsp_perc` es justamente el
> parámetro que evita la trampa de `-perc_identity` que W2 §2.4 cuantificó —que no
> filtra sobre la consulta completa sino sobre el alineamiento encontrado—, así que
> si era ése, estaba usando el correcto.

### Nuestro experimento con ventanas más cortas

Contamos que al evaluar off-targets no buscamos sólo coincidencias de 21, sino
también de menos: 20, 19, 18. Pregunta qué observamos. Le describimos el
resultado: hasta 18 el comportamiento era aproximadamente lineal y no
descartaba demasiado, pero en **17 subía marcadamente** la cantidad de
off-targets detectados y por lo tanto de ventanas descartadas.

Pregunta por qué nos parece que pasa eso. Nuestra respuesta — que éramos
demasiado estrictos — la acepta, y de ahí sale la explicación más interesante
de la reunión.

### Por qué 21 y no menos: el argumento estadístico

`[E]` La razón de los 21 nucleótidos es biológica: es el tamaño en que la
proteína corta y el tamaño del fragmento que después se empareja con el gen
blanco. También funciona 22, y sugiere hacer un benchmark de 21 contra 22. Por
debajo de eso el argumento se cae: *"si pones 18, no hay molécula funcional que
funcione"* — con excepciones que considera irrelevantes. La conclusión que nos
deja: *"tenés que tener la evidencia biológica atrás de por qué elegís 21"*.

Sobre por qué aparecen más coincidencias al acortar la ventana, el razonamiento
es estadístico: cuanto más corta la secuencia, más chance de encontrarla por
azar en millones de secuencias. Pero agrega el giro que importa — `[E]` **la
biología no es random**. Si se hace la cuenta de probabilidad de encontrar 18
nucleótidos idénticos en un genoma humano de 3 mil millones de bases, el número
que da es enorme; en la práctica no se encuentran tantos. *"A pesar de que
parezca que es A, G, T, G, que es todo random, no es random. No vas a encontrar
lo que te dice la estadística que deberías encontrar por azar."* Nos propone
hacer las cuentas para 18, 19 y 20 y compararlas con lo que devuelve el
programa.

Cierra el tema: quedarse con 21 y 22.

### Genoma vs. transcriptoma como criterio de ranking

`[E]` Explica el dogma central — ADN, ARN, proteína — y de ahí deriva la
distinción: el **genoma** es todo el material genético; el **transcriptoma** son
los genes que efectivamente se expresan. Lo que queremos atacar son los genes
que se expresan, los que pueden producir proteína: si se corta el ARN
mensajero, no hay proteína.

De esa distinción sale un criterio de ranking que nos entrega explícitamente:
`[R]` un off-target que cae en el genoma **pero no en el transcriptoma** —
en una región que no se expresa — es menos grave que uno que cae sobre un gen
activo. *"Ese off-target vos podés marcarlo como, bueno, es off-target, pero no
tanto."* Y lo enmarca como parámetro para construir el ranking.

Menciona **NCBI** como el lugar para explorar recursos genómicos y
transcriptómicos.

### Qué espera como entregable

Acotó expectativas dos veces, sin que se lo pidiéramos.

Primero planteó la idea ambiciosa: dado que la herramienta actual tiene
problemas reales — no permite cargar 20 genomas o transcriptomas a la vez, el
visualizador es malo, *"es como una línea así, que no se entiende bien"* —
sugiere pensar si se podría armar una API que, con los cuatro ejemplos, devuelva
el plot y corra los off-targets. Pero inmediatamente lo relativiza él mismo:
*"eso es un montón"*, y nosotros agregamos que en una semana es imposible.
Confirma: lleva **cinco meses** arreglando la que tienen.

Lo que sí pide, en orden:

1. **Leer y entender si-Fi21 primero.** Qué implica que algo sea eficiente, cómo
   lo calculan, qué significa la energía libre en ese contexto.
2. **Un benchmarking** de si-Fi21, dsRNA-Engineer y BLAST sobre los cuatro genes
   que ya nos dio.
3. **Un ranking** de candidatos, con el criterio explicitado: qué le damos más
   importancia, por ejemplo a los off-targets.
4. **Una evaluación de las regiones ya seleccionadas**: si nos parece que están
   bien elegidas, o si dentro de esos genes encontramos una mejor.
5. **Crítica de las herramientas**, aunque no la implementemos:
   *"probamos el programa, este es una porquería por tal cosa (…) ¿qué mejoras
   le haría? No hace falta hacerlo."*

Y el criterio de evaluación, textual: *"no porque tenga que ser cierto eso que
decís, porque al final hay que evaluarlo, sino el pensamiento que nos llevó a
ustedes para decidir ese ranking"*.

Como extensión opcional, invita a sumar genes nuevos más allá de los cuatro.
Reconoce que la búsqueda de candidatos es *"el estado del arte del problema"* y
lo más difícil para quien no es biólogo, pero valora el ejercicio: encontrar un
paper que muestre que un gen es importante para el insecto, calcular cuántas
ventanas eficientes tiene en total, elegir región y sumarlo al ranking para
comparar.

Su resumen de hacia dónde deberíamos ir: el ranking, entender bien qué significa
esa eficiencia —*"computacionalmente, porque sigue siendo computacional"*— y qué
otras cosas se podrían medir para mejorar esa predicción.

### Por qué no hay un modelo predictivo: el límite del campo

El pasaje más valioso para nuestro perfil. `[E]`/`[R]` No se puede entrenar un
modelo que prediga eficiencia porque **no hay datos empíricos suficientes**:

- Falta evidencia sobre cuáles diseños son realmente eficientes. *"Todavía no
  hay dato empírico de cuáles son eficientes, no le podemos tirar a un modelo
  para que me prediga."*
- Falta evidencia sobre el rol de la **estructura secundaria** del ARN, y él la
  identifica como *"una falencia que tienen los programas de búsqueda de
  eficientes"* — sobre todo para ARN largos.
- Para un ARN de 800 nucleótidos no se puede predecir cómo se pliega en 2D ni en
  3D en condiciones reales. Los experimentos que generarían esos datos existen
  pero son muy caros.

Su proyección: cuando haya evidencia suficiente, la estructura secundaria se
incorporaría como parámetro a los predictores de eficiencia. Y la dimensión del
problema, en sus palabras: *"el que haga bien eso se gana el Nobel igual que el
AlphaFold"*. Lo dijo medio en broma para que los otros equipos de datos se
peleen por el tema, pero remató: *"pero se necesita dato"*.

### El genoma no anotado de Dalbulus maidis

Le contamos lo que ya habíamos hecho: el genoma de la chicharrita está en el
material pero **no está anotado** —no dice qué gen es cada cosa— así que lo
mapeamos contra genomas que sí lo están. Encontramos del orden de **384 o 684
genes** potencialmente útiles, y dentro de ese conjunto estaban los que nos
habían pasado.

> **Nota de transcripción:** la cifra quedó ambigua en el audio, se dijeron las
> dos. `[?]` A verificar contra nuestros propios resultados.
>
> **Resuelto el 2026-10-20: no es ninguna de las dos.** `[E]` Ni 384 ni 684
> corresponde a una cantidad que hayamos producido. Las cifras reales del mapeo son
> **2.814 proteínas con locus** de 3.904 alineadas (72,1 %), **7.416 loci** en la
> tabla unificada, **494 candidatos de alta confianza** y **438 genes** en el
> tamizaje de especificidad. La más parecida a «384» es **438**, que es una
> transposición de dígitos plausible en un audio; «684» no se parece a ninguna.
> Lo que se le dijo en la reunión estaba mal, y lo que hay que usar de acá en más
> son los números de `pipeline/REPORT.md` §2 y §4.

Lo entiende y lo valida, con una advertencia: hay que **chequear identidad** en
cada paso, porque los genes de especies distintas no son iguales. Aclara además
que los genes que faltan están sin anotar en ese genoma, no en NCBI.

Y nos da el circuito completo, que describe como **ingeniería inversa**: `[R]`

1. Partir de un gen anotado del que haya papers asociados y que se pueda bajar.
2. Correr BLAST de ese gen en NCBI y ver qué organismos parecidos aparecen.
3. Mirar la identidad. Si hay alguno con 99%, ese gen está conservado entre las
   dos especies.
4. Si esa especie tiene transcriptoma disponible, buscar ahí los genes
   interesantes.
5. Hacer BLAST de esos genes contra el genoma no anotado de la chicharrita para
   ver si se encuentran.

Confirmamos que algo parecido fue lo que hicimos, y preguntamos si los genes
encontrados se pueden meter en las herramientas de diseño. La respuesta es que
sí, y que agregarlos al ranking *"está buena"*.

### Contacto y material de guía

Dictó su dirección de correo, deletreándola. `[R]` La parte local es
`apolo.d.zaballo` — "Apolo" con una sola L, "D" de Diego, y el apellido
dictado letra por letra. El dominio no quedó registrado en el audio.

> **Nota:** la grafía del apellido es `[?]`. El deletreo en el audio fue
> "Z-A-B-A-L-L-O" con una corrección en el medio y la transcripción automática
> lo escribió de varias formas. A confirmar antes de escribirle.

Sobre el material: además del Excel que ya habíamos visto, subió un **documento
de guía** con preguntas. Fue explícito en que no hay que completarlo —
*"no, no, no tienen que completarlo ni nada, es como una guía"*— y que la
intención es que las preguntas nos disparen ideas. Nos dirigió a la parte
asociada a nuestra ficha. Ofreció seguir la conversación por correo.

### Cierre

El tramo final es charla informal: pregunta qué se está haciendo en San Andrés,
cuántos años tiene la carrera (cinco) y cuántas camadas salieron. Comentamos
que ahora abren Biotecnología —desde mediados del año pasado— y que este año
abriría Ingeniería Industrial. Hay un intercambio sobre qué docente está
detrás de cada carrera que quedó sin resolver y que no tiene relevancia técnica.
Cierre con agradecimientos.

---

## Calidad de la transcripción

Whisper confundió términos técnicos de forma sistemática y predecible. Las
correcciones aplicadas en este documento:

| En el audio | Lo correcto |
|---|---|
| "Sci-Fi", "S-I-F-I" | **si-Fi21** |
| "engineer", "Ingenier" | **dsRNA-Engineer** |
| "ARNI" | **ARNi** (interferencia de ARN) |
| "soft target" | **off-target** |
| "Plot Key" | el **plot** de eficiencia |
| "una araña" (04:15) | "un ARN" |
| "se puede hacer en Canadá" (03:22) | probablemente "en el laboratorio"; `[?]` |
| "mi informática" (10:13) | "bioinformática" |
| "el ecoso" (16:33) | probablemente "el ARN mensajero"; `[?]` |
| "HCP" | parámetro de BLAST sin identificar; `[?]` |
| "hostales" (23:19) | "off-targets" |
| "ambiente activo" (03:10) | `[?]` sin resolver |

Dos tramos tienen pérdida real de contenido por diafonía (varias personas
hablando a la vez), donde el modelo rellenó con "Sí" repetido: **05:25–06:18**
—unos 50 segundos, justo cuando preguntaba en qué año estábamos y si leíamos
código— y **21:00–21:22**, en medio del tema del genoma no anotado. También hay
tramos cortos con el mismo problema en 08:08–08:15 y 12:50–13:00. Si algo de
esos minutos importa, hay que volver al video.

---

## Pendientes que salen de esta reunión

Para registrar en `00_meta/PREGUNTAS_ABIERTAS.md`:

1. Confirmar la grafía del apellido y el dominio del correo antes de escribirle.
   **Sigue abierto** al 2026-10-20: no se infiere, y el dominio no quedó en el
   audio. Es lo único que bloquea el envío.
2. ~~Identificar qué parámetro de BLAST es el que nombró como "HCP".~~ **Resuelto a
   medias el 2026-10-20:** es HSP, y los candidatos son `-qcov_hsp_perc` y
   `-max_hsps`. Ver la nota de la sección de off-targets.
3. ~~Resolver si los genes recuperados del mapeo son 384 o 684.~~ **Resuelto el
   2026-10-20: ninguno de los dos.** Ver la nota de la sección del genoma no
   anotado.
4. Qué umbral exacto usa si-Fi21 para marcar una ventana como eficiente, y cómo
   combina energía libre, identidad y estructura secundaria en esa decisión.
5. Con qué criterio eligió las regiones 1–200 de los cuatro diseños. Dijo que no
   lo recuerda, así que probablemente no haya respuesta y haya que tratarlo como
   decisión a auditar, no a reproducir.

Para `00_meta/DECISIONS.md`, quedan al menos tres decisiones a formalizar: las
bacterias salen del alcance del diseño por ARNi; el objetivo es el insecto como
vector y no el patógeno dentro de la planta; y la ventana se fija en 21–22
nucleótidos con la evidencia biológica como fundamento.

