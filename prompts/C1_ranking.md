# C1 — Ranking de candidatos y lo que falta del checkpoint 1

<rol>
Cerrás el pedido central del investigador invitado del Investigathon: el ranking
de los cuatro candidatos de EPILAB, con el criterio de combinación escrito y
defendido. Trabajás para un equipo de cuatro ingenieros en IA que no aporta
laboratorio y cuya ventaja comparativa es exactamente ésta: la priorización
auditable. El investigador dijo textual que va a evaluar *"el pensamiento que nos
llevó a ustedes para decidir ese ranking"* y no si el ranking acierta, así que la
justificación es el entregable y el número es su consecuencia.
</rol>

<objetivo>
Un ranking de candidatos con cada regla de combinación justificada por escrito,
sostenido por insumos que ya están calculados y versionados, y sin una sola
afirmación que contradiga otra medición nuestra sin adjudicarla. Alrededor del
ranking, cerrar los tres pedidos del checkpoint que todavía no están y que el
ranking necesita o que el investigador pidió explícitamente.
</objetivo>

<insumos>
Leé esto antes de escribir una línea de código. Cada uno aporta algo distinto y
el plan asume que los leíste:

- `research/checkpoints/checkpoint1.md` — la reunión completa. Las secciones que
  mandan acá son «Cómo se calcula la eficiencia», «Off-targets, BLAST y
  mismatches», «Genoma vs. transcriptoma como criterio de ranking» y «Qué espera
  como entregable».
- `research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md` — el insumo
  principal. §0 (el port verificado contra el original: 42, 32, 133, 212), §2
  (eficientes por región, aislada contra en contexto), §3 (las cuatro regiones
  están 19-46 % por debajo del óptimo) y §4 (el cruce con off-targets, incluida
  la refutación en `BicC_Dm`).
- `pipeline/REPORT.md` §5, §6 y §10 — nuestro propio método de agregación, el
  resultado negativo que contradice a §3 de arriba, y la ficha de decisión por
  candidato que figura como pendiente.
- `pipeline/region_scoring.py` — el encabezado del módulo. **Ya tomamos posición
  en código** sobre una de las decisiones que hay que defender: el veto duro por
  región y `buenos_limpios` como criterio de orden por defecto.
- `pipeline/resultados.json` — las entradas `region-no-discrimina`,
  `sensibilidad-pesos`, `media-geometrica` y `candidatos-epilab-mapeados`.
- `tools/sifi21_port/` — `cruce.py` ya cruza eficiencia con off-targets por gen y
  región; `offtarget_21nt.py` produce el TSV por ventana. El README dice qué
  calcula cada cosa.
- `research/ola2/W2_herramientas/REPORT.md` §1.2, §2.4 y §4 — qué es
  dsRNA-Engineer, por qué no corre local, y las dos mediciones que ya tenemos
  sobre su conteo de off-targets.
- `00_meta/DECISIONS.md`, `00_meta/PREGUNTAS_ABIERTAS.md` y
  `00_meta/CAMINOS_PROBADOS.md` — el estado de la memoria del proyecto. Se
  actualizan durante el trabajo, no al final.

Los datos por ventana ya están en `work/sifi_check/`: los TSV de eficiencia por
gen y `offtarget_full/offtarget_por_sirna.tsv` con una fila por posición y una
columna por referencia y criterio (`perfecto_21`, `perfecto_ge19`, `mm1_21`).
Nada de esto hay que recalcular salvo que una tarea lo pida.
</insumos>

<reglas_heredadas>
Rigen las de `CLAUDE.md` sin excepción. Las tres que pegan fuerte acá:

1. **Marcadores de evidencia** en toda afirmación relevante: `[E]` establecido,
   `[R]` reportado, `[H]` hipótesis nuestra, `[?]` incierto o en contradicción.
   Un número sin contexto experimental no entra.
2. **Las secuencias de EPILAB no se suben a servicios de terceros.** En la tarea
   T4 esto es una compuerta, no una recomendación: ver el procedimiento exacto
   ahí. Un dato subido no se puede desubir.
3. **Prosa técnica en español**, no listas de bullets sueltos. Nombres
   científicos en itálica y completos la primera vez.
</reglas_heredadas>

<orden_de_trabajo>

## T1 — Adjudicar la contradicción del 7,2 % (primero, porque condiciona T2)

Tenemos dos mediciones propias que apuntan en direcciones opuestas.
`pipeline/REPORT.md` §6 dice que elegir la mejor región de 300 pb dentro de un gen
mejora alrededor del 7,2 % sobre el promedio de ese gen y que **no es
significativo contra un modelo nulo en 0 de 20 genes**, y concluye que lo que
discrimina es qué gen se ataca, no qué región. `sifi21_reproduccion.md` §3 dice
que las cuatro regiones de EPILAB están entre 19 % y 46 % por debajo del óptimo
por densidad de ventanas eficientes. Si el ranking recomienda mover `BicC_Dm` a
2123-2422 sin resolver esto, el investigador tiene el flanco abierto en la primera
pregunta.

No son la misma cantidad: una mide nuestro puntaje biofísico agregado por región,
la otra cuenta ventanas eficientes de si-Fi21. Pero eso es una explicación, no una
adjudicación. Lo que hay que hacer es la medición que falta:

1. Localizar cómo se construyó el modelo nulo del 7,2 % (el registro apunta a
   `region_scoring.py`; la palabra «nulo» no aparece en el archivo, así que puede
   estar en otro script o no ser reproducible). Si no se puede reproducir,
   decilo con esas palabras y seguí con el punto 2, que no depende de él.
2. Construir el nulo del lado de si-Fi21, que es barato porque el perfil por
   ventana ya existe: para cada uno de los cuatro genes, calcular la distribución
   completa del conteo de eficientes sobre **todas** las regiones deslizantes del
   mismo largo que usó EPILAB, y ubicar en esa distribución tanto la región
   elegida como la mejor. El resultado es un percentil, no un porcentaje: decir
   que la región elegida está en el percentil 18 de su propio gen es una
   afirmación falsable, y decir que está «21 % por debajo del óptimo» no lo es,
   porque el óptimo de un máximo sobre cientos de ventanas superpuestas está
   sesgado hacia arriba por construcción.
3. Medir los dos puntajes sobre los mismos genes. `pipeline/resultados.json`
   registra que `BicC_Dm` y `ATPaseD_Dm` caen en loci del mapeo, así que en esos
   dos se puede calcular el puntaje biofísico del pipeline y la densidad de
   eficientes de si-Fi21 sobre las mismas regiones, y correlacionarlos. Si
   correlacionan, las dos mediciones no se contradicen y una es proxy de la otra.
   Si no correlacionan, la contradicción es real y hay que elegir cuál manda en el
   ranking, con el motivo.

**Entregable:** una sección de adjudicación, más una entrada en
`00_meta/DECISIONS.md` con el veredicto y su consecuencia sobre T2. Los dos
desenlaces son publicables: si el efecto de región resiste el nulo, el ranking
recomienda regiones alternativas; si no resiste, el ranking las reporta como
indistinguibles y recomienda a nivel de gen, que es un resultado más interesante
que el otro porque contradice lo que el propio investigador dio por supuesto.

## T2 — El ranking

El núcleo. Una función que combine los dos ejes ya medidos por ventana
—eficiencia y exposición a no objetivo— en un orden de candidatos, con cada regla
de combinación justificada. Las cinco decisiones a defender están en
`<decisiones_a_defender>`, que es la parte sustantiva de este prompt.

Requisitos de método, no negociables porque son lo que hace al ranking defendible:

- **Reusar el método de agregación que ya tenemos en vez de inventar uno.**
  `pipeline/REPORT.md` §5 resolvió esta misma pregunta: media geométrica ponderada
  en lugar de suma ponderada, para que un criterio cercano a cero no se compense
  con otro muy bueno, y después un barrido de pesos sobre el simplex. Si te
  desviás de ese método, justificá por qué; si lo seguís, citá el antecedente.
- **El barrido de pesos es obligatorio y el resultado reportado es el conjunto de
  sobrevivientes, no el orden puntual.** Con cuatro candidatos el barrido es
  trivial de correr y la pregunta que contesta es la que importa: ¿el orden
  depende de pesos que nadie justificó, o hay candidatos que aguantan todo el
  simplex? Reportá la frecuencia de cada candidato en cada posición sobre el
  barrido, no un único vector de pesos. En el antecedente del pipeline, 119 de
  124 candidatos llegaron al top-10 por una elección de pesos arbitraria: ese es
  exactamente el error que hay que no cometer en el entregable principal.
- **Dos niveles de ranking.** Primero los cuatro candidatos de EPILAB tal como
  están, que es lo que él pidió. Después, condicionado al veredicto de T1, las
  regiones alternativas dentro de cada gen, que es donde el ranking deja de ser un
  ejercicio y pasa a ser una recomendación.
- **El código va en `tools/sifi21_port/ranking.py`**, junto a `cruce.py`, porque
  consume los mismos TSV. Mismo estilo que el resto del directorio: sin interfaz,
  reproducible por línea de comandos, con las entradas por parámetro. Pruebas en
  `test_sifi.py` o en un `test_ranking.py` al lado.

**Entregable:** `research/ola2/W7_ranking/REPORT.md` con el ranking, las cinco
decisiones justificadas una por una, el barrido de pesos y sus sobrevivientes, y
la ficha por candidato. Más `ranking.json` con los números que cita el reporte.

## T3 — La cuenta de azar para 18, 19 y 20 nt

El investigador la pidió explícitamente —hacer la probabilidad teórica y
compararla con lo que devuelve el programa— porque es el soporte de su argumento
de que la biología no es random. Tenemos el lado observado y no tenemos el
esperado ni la comparación.

`offtarget_21nt.py` fija el tamaño en `SIZE = 21` (línea 37). Hace falta
parametrizarlo o escribir un script hermano; si lo parametrizás, verificá antes
que con 21 sigue dando los mismos conteos que hoy, porque ese número está citado
en tres documentos.

Comparar observado contra esperado bajo tres nulos, que es lo que convierte la
cuenta en un argumento en vez de una aritmética:

1. **Uniforme**, 1/4^k por posición: el número que el investigador llamó «lo que
   te dice la estadística».
2. **Ajustado por composición** de cada referencia, que ya baja bastante el
   esperado y es el nulo honesto mínimo.
3. **Empírico por barajado** de la referencia preservando composición de
   mononucleótidos y, si el costo lo permite, de dinucleótidos. Este es el que
   muestra el efecto que él describió, porque conserva la composición y destruye
   la estructura.

Reportar una tabla de esperado contra observado por k (18, 19, 20, 21) y por
referencia, sobre los cuatro genes, con la conclusión escrita: cuánto de la
diferencia entre lo que predice el azar y lo que aparece se explica por
composición y cuánto queda sin explicar. El salto en 17 nt que el equipo le contó
en la reunión no está documentado con números en el repositorio: si lo
reconstruís, queda documentado; si no, anotalo como tal en
`PREGUNTAS_ABIERTAS.md` en lugar de citarlo.

**Entregable:** una sección del REPORT de T2 o un documento propio en
`research/ola2/W7_ranking/`, más el script.

## T4 — Completar el benchmarking de las tres herramientas

Su punto 2 pedía si-Fi21, dsRNA-Engineer y BLAST sobre los cuatro genes. si-Fi21
corrió sobre los cuatro y el tamizaje exacto de 21 nt también; **dsRNA-Engineer
corrió solamente sobre `PZ371507.1`**, una secuencia pública, y no existe el
documento que compare las tres sobre un eje común.

**La compuerta de confidencialidad, que es la parte delicada de toda esta tarea.**
dsRNA-Engineer corre solo como servicio web, con procesamiento del lado del
servidor y sin política de retención declarada. `MP_MRFV` y `CP_MRFV` son
—según `sifi21_reproduccion.md`— idénticas byte a byte a `NC_002786.2`, o sea
material publicado, y por lo tanto subirlas no revela nada que no esté ya en el
NCBI. `BicC_Dm` y `ATPaseD_Dm` no lo son y **no se suben por ningún motivo**.
Procedimiento obligatorio, en este orden:

1. Reverificar la identidad byte a byte de las dos secuencias virales contra
   `NC_002786.2` en esta corrida, con el comando y su salida en el reporte. No
   alcanza con que lo diga otro documento nuestro.
2. **Pedirle confirmación explícita a la persona antes de subir cualquier cosa**,
   mostrándole qué secuencia se va a subir y a dónde. Es una acción externa e
   irreversible y no está cubierta por una autorización general.
3. Si la verificación falla o no hay confirmación, el benchmark se hace con dos
   herramientas sobre los cuatro genes y con la tercera sobre la secuencia
   pública que ya corrimos, y el hueco se documenta. El hueco **es** un resultado:
   la herramienta que el organizador señala como la de diseño y verificación de
   off-targets es exactamente la que no se puede usar con el material que dio el
   organizador, y eso va a la presentación.

El eje comparable es el de off-targets, porque si-Fi21 mide eficiencia, BLAST mide
especificidad y dsRNA-Engineer dice medir las dos. Compará qué ventanas marca cada
una sobre el mismo gen con el panel de referencias más parecido que se pueda armar
—dsRNA-Engineer admite diez especies por corrida y nuestro panel tiene seis— y
retomá las dos mediciones que ya existen: que su conteo está dominado por la
condición de 16 pb (70 de 70 aciertos en maíz, cero de la condición de 21-22 pb
que la propia herramienta llama tamaño de corte de Dicer-2) y que `blastn-short`
con `word_size 11` subestima el criterio de un desajuste por hasta un factor de
tres. Lo que falta es ponerlas sobre los mismos genes y en un solo lugar, con la
conclusión de cuál herramienta usaríamos para qué.

**Entregable:** `research/ola2/W7_ranking/benchmark_tres_herramientas.md`, con una
tabla por gen y por herramienta y la conclusión operativa.

## T5 — Cerrar el pendiente de `pipeline/REPORT.md` §10

Ahí figura la ficha de decisión por candidato para los cuatro candidatos del
laboratorio como pendiente de dos respuestas del investigador: el umbral de
identidad del filtro de especificidad y los pesos de los criterios. **El barrido
de pesos de T2 hace innecesario esperar los pesos**, y el umbral de identidad se
puede tratar igual: barrerlo y reportar sobre qué rango el orden no cambia. Dejar
una decisión esperando una respuesta que podemos convertir en un eje de
sensibilidad es la salida fácil, y acá la salida fácil es además peor, porque lo
que él dijo que va a evaluar es el razonamiento.

Actualizar §10 con lo que quedó resuelto y con lo que sigue abierto de verdad.

## T6 — Tres pendientes chicos, antes de escribirle

Están en `PREGUNTAS_ABIERTAS.md` y conviene cerrarlos en esta corrida:

- **384 o 684 genes recuperados del mapeo.** Se resuelve contra nuestros propios
  resultados, no hace falta preguntárselo. Resolvelo y corregí donde esté mal.
- **El parámetro de BLAST que transcribió como «HCP».** Candidatos razonables son
  E-value, bit score y percent identity. Si la documentación oficial no permite
  decidir, queda `[?]` y se le pregunta; no se adivina.
- **La grafía del apellido y el dominio del correo.** No se infiere. Queda en la
  lista para preguntarle.

## T7 — Extensión opcional, solo si T1 a T5 están cerrados

Sumar genes nuevos de la literatura al ranking, que es la extensión que él
ofreció. No empieza antes de que exista la vara: sin criterio de orden, un gen
nuevo no se puede comparar con nada. Si llegás acá, cada gen nuevo entra con el
paper abierto y citado, nunca de memoria, y con el mismo tratamiento de los otros
cuatro.

</orden_de_trabajo>

<decisiones_a_defender>
Son cinco, no cuatro. Cada una es una tensión real con material nuestro de los dos
lados, y lo que se evalúa es el argumento, así que ninguna se resuelve eligiendo
un número: se resuelve diciendo qué se gana y qué se pierde con cada opción, qué
evidencia sostiene la elección, y cómo cambia el ranking si uno se equivoca.

**D1. Cuánto pesa la densidad de eficientes contra la exposición a no objetivo.**
La respuesta defendible no es un peso: es el barrido del simplex de T2 y el
conjunto de candidatos que lo sobrevive. Pero hay que decir además qué forma tiene
la combinación, porque media geométrica y suma ponderada no son la misma
afirmación sobre el problema. La suma dice que una región muy eficiente puede
comprar su propio riesgo; la media geométrica dice que no. Y existe una tercera
posición, que es la que ya tomamos en código: `region_scoring.py` usa
`buenos_limpios` —la intersección, cuántas ventanas son a la vez buenas y
limpias— más un veto duro, o sea trata los ejes como un filtro en cascada y no
como un puntaje combinado. Elegí entre las tres con argumento.

**D2. Si una ventana riesgosa pero no eficiente cuenta igual que una riesgosa y
activa.** Esto lo medimos por separado y es un argumento propio: en `MP_MRFV`, de
las 22 ventanas con off-target del gen entero solo 2 son eficientes. Pero cuidado,
porque **ya tomamos la posición contraria en código**: el veto de
`region_scoring.py` descarta la región entera si alguna ventana tiene coincidencia
perfecta de 21 nt con un no objetivo, sea eficiente o no, con el motivo escrito de
que Dicer procesa el dsRNA entero y esa ventana va a estar en el pool. Las dos
posiciones son razonables y son incompatibles: la mecanicista dice que una ventana
que no carga bien en el complejo no silencia nada, y la conservadora dice que
«eficiente» es una predicción nuestra con un umbral discutible y que apostar la
seguridad a esa predicción es apostar al componente más débil de la cadena.
Resolvelo explícitamente y declará que estás overrideando el código previo si lo
hacés, con una entrada en `DECISIONS.md`. Reportá el ranking bajo las dos reglas:
si no cambia, la decisión no importa y eso también es un resultado.

**D3. Si un off-target en maíz pesa lo mismo que uno en *Homalodisca
vitripennis*.** Hacen falta pesos por referencia y cada uno con su motivo por
consecuencia, no por simetría: el maíz es el cultivo que estamos protegiendo, de
modo que un acierto ahí es un daño al objetivo mismo de la intervención;
*H. vitripennis* es un cicadélido no objetivo y el riesgo ahí es ecológico y
además esperable por conservación filogenética; *Apis mellifera* es polinizador y
el costo de un acierto es regulatorio antes que ecológico; *Harmonia axyridis* es
enemigo natural del propio blanco, así que un acierto ahí es contraproducente en
el sentido fuerte; *Folsomia candida* es fauna del suelo y especie modelo
estándar de ecotoxicología. El cuadro de riesgo ya está medido por referencia, así
que esto es ponderación y redacción.

Dos cosas que hay que decir en esta decisión y que no están en la lista original:
el criterio de genoma contra transcriptoma que él entregó explícitamente —un
off-target que cae en el genoma pero no en el transcriptoma pesa menos— **ya está
resuelto por construcción en nuestro panel**, porque las cinco referencias no
objetivo son transcriptomas (`_rna`) y la única genómica es la de *Dalbulus
maidis*, que entra como on-target; no hay nada que descontar, pero si no lo
escribimos parece que ignoramos su criterio. Y el límite del panel: los ceros de
*Apis mellifera* son reales, pero la ausencia de riesgo en cicadélidos nativos y
parasitoides **no está medida** porque no hay transcriptomas, y seis referencias
no son el ambiente. Un peso sobre una referencia que no existe es cero por
omisión, no por evidencia.

**D4. Si un bloque perfecto de 19 nt pesa lo mismo que un desajuste único.** Los
tres criterios se miden por separado (`perfecto_21`, `perfecto_ge19`, `mm1_21`) y
hay literatura ya registrada en `FUENTES.md` sobre el umbral de 19 nt y sobre
tolerancia a desajustes, que es con lo que se ordena. Dos datos propios entran
acá: el criterio de un desajuste medido por coincidencia exacta encuentra **más**
que el de BLAST, hasta un factor de tres, porque `blastn-short` con `word_size 11`
no puede sembrar un 21-mero cuyo desajuste cae en la posición 11 —o sea que si se
pondera con el número de BLAST se está ponderando una subestimación—, y la
posición del desajuste dentro de la ventana no es indiferente, lo que abre la
pregunta de si un desajuste en la región semilla pesa como uno en el extremo 3'.
Si no tenemos evidencia para distinguirlos, decilo y tratalo como `[?]` en vez de
inventar un peso.

**D5. Si un gen del insecto y un gen del virus compiten en el mismo ranking.**
Ésta no estaba en la lista y es anterior a las otras cuatro. `MP_MRFV` y `CP_MRFV`
son genes del *Maize rayado fino virus* y `BicC_Dm` y `ATPaseD_Dm` son genes de
*Dalbulus maidis*: son las dos estrategias que él separó en la reunión, y
recomendó la del insecto por ser más directa. Si los cuatro entran en un solo
orden, hay que decir con qué equivalencia, porque ni los off-targets significan lo
mismo en los dos casos: para los genes del insecto el genoma de *D. maidis* se
excluye como on-target, y para los virales entra como off-target —9 ventanas de
`MP_MRFV`, 2 de ellas eficientes—, pero pegarle al vector mientras se apunta al
virus no es obviamente un defecto. Esa asimetría de signo hay que resolverla por
escrito. La recomendación por defecto es presentar dos rankings, uno por
estrategia, más un criterio declarado de comparación entre estrategias que
incorpore lo que ya sabemos: la recomendación del investigador por la vía del
insecto, y el argumento propio de la ventana de latencia de unos 20 días. Si
decidís un solo ranking, la equivalencia tiene que estar escrita y ser atacable.
</decisiones_a_defender>

<fuera_de_alcance>
- Nada que aumente virulencia, transmisibilidad o rango de hospedadores de un
  patógeno; ningún protocolo de síntesis o producción; ningún diseño dirigido a
  dañar especies no objetivo. El trabajo es control fitosanitario con información
  pública.
- **No** armes la crítica consolidada de herramientas con mejoras propuestas, y
  **no** corras el benchmark de 21 contra 22 nt. Las dos cosas están pedidas por
  el investigador y las dos están deliberadamente fuera de este plan: se hacen
  aparte. Si al pasar encontrás material para alguna, anotalo y seguí.
- No entrenes ningún modelo. La decisión está tomada y registrada en
  `DECISIONS.md` D8, y el motivo lo dio el propio investigador: no hay dato
  empírico de eficiencia con el que entrenar nada.
- No reescribas ni refactorices el port de si-Fi21 ni el pipeline. Están
  verificados y sus números están citados en varios documentos. Si necesitás
  parametrizar algo —el tamaño de ventana de `offtarget_21nt.py` en T3— verificá
  primero que el comportamiento anterior no cambió.
- No toques el corpus original de `YHat-Biotech/`: no se modifica, no se renombra
  y no se mueve. Todo trabajo va sobre copias en `work/`.
</fuera_de_alcance>

<salida>
En `research/ola2/W7_ranking/`:

1. `REPORT.md` — prosa técnica. La adjudicación de T1, el ranking de T2 con las
   cinco decisiones defendidas una por una, el barrido de pesos con sus
   sobrevivientes, la ficha por candidato, y la cuenta de azar de T3 si no va
   aparte. Arriba de todo, en un párrafo, el resultado: el orden, y qué parte de
   ese orden aguanta el barrido.
2. `ranking.json` — un registro por candidato con los dos ejes, los pesos
   barridos, la frecuencia por posición y el veredicto. Es la fuente de los
   números que cita el reporte, igual que `pipeline/resultados.json`.
3. `benchmark_tres_herramientas.md` — T4, con la compuerta de confidencialidad
   documentada: qué se subió, qué no, y por qué.

En `tools/sifi21_port/`: `ranking.py` y sus pruebas. El tamaño de ventana
parametrizado en `offtarget_21nt.py` si T3 lo necesita, con la verificación de que
21 sigue dando lo mismo.

En `00_meta/`: las entradas de `DECISIONS.md` por cada una de las cinco decisiones
y por el veredicto de T1, en formato ADR liviano con fecha, alternativas y
consecuencia. Lo que se descartó en `CAMINOS_PROBADOS.md`, que un descarte bien
documentado vale tanto como un hallazgo. Lo que quedó abierto en
`PREGUNTAS_ABIERTAS.md`, incluida la lista final de preguntas para el
investigador. Términos nuevos en `GLOSARIO.md` y fuentes nuevas en `FUENTES.md`.

En `pipeline/REPORT.md`: §10 actualizada.
</salida>

<verificacion>
Antes de dar algo por terminado, contestá cada una de éstas por escrito:

- ¿La contradicción del 7,2 % quedó adjudicada con una medición, o con un
  argumento sobre por qué las dos mediciones no son comparables? Lo segundo no
  alcanza.
- ¿El ranking reporta el conjunto de candidatos que sobrevive al barrido de
  pesos, o un orden puntual bajo pesos elegidos a dedo? Si es lo segundo, no está
  hecho.
- ¿Las cinco decisiones están justificadas con lo que se gana y lo que se pierde,
  y cada una dice cómo cambia el ranking si la decisión fuera la contraria?
- ¿D2 reconoce que `region_scoring.py` ya tomó la posición opuesta, y la mantiene
  o la overridea explícitamente?
- ¿Cada número lleva marcador de evidencia y contexto, y cada fuente nueva se
  abrió de verdad?
- ¿Se subió algo a dsRNA-Engineer? Si sí: ¿se verificó la identidad byte a byte en
  esta corrida y hubo confirmación explícita de la persona? Si falta cualquiera de
  las dos, es un incidente y va reportado como tal.
- ¿El reporte dice en algún lugar visible qué parte del ranking es nuestra
  decisión y no una medición? El investigador va a evaluar el razonamiento: la
  honestidad sobre lo que es criterio y lo que es dato es parte de lo que se
  evalúa.
- ¿Alguna afirmación nueva contradice otra de `sifi21_reproduccion.md`,
  `pipeline/REPORT.md` o W2 sin adjudicarla?
</verificacion>

<terminacion>
Terminás cuando existen los tres entregables de `<salida>`, las entradas de
`00_meta/` están escritas y §10 del pipeline está actualizada. Pará ahí y
reportá: qué dio el ranking, qué parte aguanta el barrido, qué quedó abierto y
qué hace falta preguntarle al investigador. No agregues herramientas, wrappers,
refactors ni análisis que no estén pedidos; si pensás que algo así ayudaría,
decilo al final en una línea.
</terminacion>
