# Decisiones

Una entrada por decisión, en formato ADR liviano: fecha, decisión, alternativas
consideradas, criterio, consecuencia. Las decisiones de contenido que tomen las
investigaciones se registran acá cuando afectan al proyecto entero; las que son
internas a una investigación quedan en su propio reporte.

---

## D1 — Competir en tres ejes y no en el de biología experimental
**Fecha:** 2026-10-16
**Quién:** el equipo, antes de esta sesión. Se registra acá porque condiciona todo lo demás.
**Decisión:** presentar en los ejes de bioinformática y datos, desarrollo
computacional e innovación abierta, y no en el de biología y evidencia
experimental.
**Alternativas consideradas:** intentar una propuesta con componente
experimental, apoyada en colaboración externa con algún laboratorio.
**Criterio:** cuatro estudiantes de tercer año de Ingeniería en IA, sin
laboratorio húmedo y sin formación formal en biología, no tienen forma de
producir evidencia experimental propia en el plazo del evento. La ventaja
comparativa está en lo computacional.
**Consecuencia:** toda propuesta nuestra tiene que ser demostrable sin un solo
experimento húmedo. Eso convierte la validación retrospectiva contra resultados
ya publicados en el único camino de validación disponible, y vuelve la
disponibilidad de datos públicos el riesgo número uno del proyecto.

---

## D2 — Tratar las notas de la charla como hipótesis numeradas, no como hechos
**Fecha:** 2026-10-16
**Decisión:** lo que el equipo anotó de la charla del investigador invitado se
trata como tres supuestos a verificar, S1 (identidad de los patógenos y qué
síntoma causa cada uno), S2 (qué calcula BLAST y qué calcula la termodinámica) y
S3 (la diferencia entre dsRNA exógeno y ARN no codificante). Cada uno se
confirma o se corrige con fuentes abiertas, y la resolución va explícita en
`SINTESIS.md`.
**Alternativas consideradas:** partir de las notas como base de trabajo y
corregir sobre la marcha.
**Criterio:** son notas de segunda mano de una charla oral. Un error en S2
contaminaría directamente dos de los enfoques candidatos del equipo, porque la
distinción entre alineamiento y termodinámica es la que define qué es la
"función de pérdida" de la que habla la idea del integrante.
**Consecuencia:** R1 y R2 verifican la misma distinción desde ángulos distintos,
lo que es redundancia deliberada y no duplicación de trabajo. Si las dos llegan
a conclusiones distintas, el término queda `[?]` en el glosario.

---

## D3 — Cinco investigaciones en paralelo, con los prompts del repositorio sin modificar
**Fecha:** 2026-10-16
**Decisión:** lanzar exactamente cinco líneas de investigación, una por archivo
de `prompts/`, pasando el texto de cada prompt completo y sin resumir. El
orquestador no ejecuta ninguna de las cinco: integra.
**Alternativas consideradas:** partir las investigaciones más grandes (R1, R4)
en subtareas más chicas para acortar el tiempo de cada una; o ejecutar
secuencialmente para poder encadenar los hallazgos.
**Criterio:** los cinco prompts están escritos con condición de terminación
propia y con verificación propia. Partirlos obligaría a reconciliar fragmentos
sin dueño, y secuenciarlos multiplicaría por cinco el tiempo total sin mejorar
cada reporte, porque las cinco preguntas son en buena medida independientes.
**Consecuencia:** hay solapamiento previsible entre R2 y R4 en los modelos
fundacionales de secuencias, y entre R1 y R3 en el estado del arte de
tratamientos. El solapamiento se resuelve en la integración, no se evita: dos
lecturas independientes de la misma bibliografía son una forma barata de
detectar error.

---

## D4 — El glosario se arma en dos pasadas
**Fecha:** 2026-10-16
**Decisión:** escribir primero el núcleo conceptual de `GLOSARIO.md` desde
consenso de libro de texto, marcado como pendiente de fuente, y fusionar después
los glosarios parciales de las cinco investigaciones agregando la cita.
**Alternativas consideradas:** esperar los glosarios parciales y escribir el
glosario una sola vez.
**Criterio:** el glosario es la pieza que el equipo necesita para poder leer los
reportes. Tenerlo a medias desde el principio es más útil que tenerlo completo al
final, y el costo de la segunda pasada es bajo.
**Consecuencia:** hay entradas que durante un rato dicen "pendiente de fuente".
La regla de `CLAUDE.md` de que toda afirmación lleva fuente se cumple en el
estado final del archivo, no en cada momento intermedio. Lo que no se admite en
ningún momento es una cita reconstruida de memoria.

---

## D5 — Un commit por investigación integrada, más uno final
**Fecha:** 2026-10-16
**Decisión:** las investigaciones no commitean. El orquestador hace un commit por
cada reporte que vuelve y queda integrado, y un commit final con la síntesis y
la portada.
**Alternativas consideradas:** que cada investigación commitee su propia carpeta.
**Criterio:** cinco procesos escribiendo sobre el mismo índice de git al mismo
tiempo se pisan. Y la unidad de trabajo revisable no es "el archivo que escribió
un agente" sino "la investigación integrada al resto de la memoria del
proyecto".
**Consecuencia:** el historial de git se lee como la secuencia de integración, y
cada commit deja el repositorio en un estado coherente entre `research/` y
`00_meta/`.

---

## D6 — El material pesado de referencia queda fuera del control de versiones
**Fecha:** 2026-10-16
**Decisión:** mantener en `.gitignore` los PDF de material de referencia, entre
ellos el de la sesión técnica del Investigathon (unos 45 MB).
**Criterio:** son insumos de lectura, no entregables, y no corresponde empujar
decenas de megabytes a un repositorio de texto.
**Consecuencia:** quien clone el repositorio no recibe ese material. Todo dato
que venga de ahí y se use en un reporte tiene que quedar citado en el reporte,
no solo referenciado al archivo local.

---

## D7 — El aporte del equipo es la priorización auditable, no el diseño ni la entrega
**Fecha:** 2026-10-17
**Quién:** el orquestador, al integrar las cinco investigaciones.
**Decisión:** el eje central de la propuesta es una función de decisión sobre
candidatos *dados* —orden, criterio escrito, evidencia citada e incertidumbre
propagada—, y no el diseño de secuencias nuevas, ni la formulación, ni la vía de
entrega.
**Alternativas consideradas:** atacar la barrera de entrega, que es la que el
organizador declara central; construir una plataforma de diseño de ARN con
chequeo de off-targets; entrenar un modelo de eficacia.
**Criterio:** tres resultados independientes apuntan al mismo lugar. R3 muestra
que el diseño con chequeo de off-targets ya existe y se llama Apolo Rocket, que
la encapsulación está publicada desde 2017 con al menos seis químicas, y que la
co-entrega contra la dsRNasa del insecto la propuso un grupo argentino en 2023:
proponer cualquiera de las tres como novedad sería proponerle a alguien del
EPILAB lo que ya hace. R3 muestra además que el cuello de botella de la entrega
es experimental y de capital, no computacional. Y el propio organizador declara
abierta exactamente la pregunta de priorización: tiene candidatos preliminares y
pregunta cuáles merecen validación y por qué. R2 y R4, que trabajaron por
separado y desde preguntas distintas, llegaron de forma independiente a la misma
propuesta —R2 la llama PRIOR-dsRNA y R4 la llama L1—, lo que es la mejor señal
disponible de que el encuadre es el correcto.
**Consecuencia:** el entregable se juzga por la calidad de la decisión que
produce, no por la novedad del método ni por la interfaz. La línea de base a
superar o a alimentar es dsRIP, que ya hace la mayor parte del cálculo, y
reconocerlo en voz alta es parte de la propuesta. Si el método no le gana a
dsRIP en la validación retrospectiva, el entregable sigue siendo válido y así
está declarado de antemano.

---

## D8 — No se entrena ningún modelo, y eso es una decisión declarada, no una carencia
**Fecha:** 2026-10-17
**Decisión:** no entrenar ni ajustar ningún modelo. El cálculo es una función de
puntuación explícita con coeficientes publicados, más tamizaje por alineamiento,
más cuantificación de incertidumbre. Los datos de fenotipo existentes se reservan
íntegros para validar.
**Alternativas consideradas:** ajuste fino de un modelo fundacional de ácidos
nucleicos (la línea L4 de R4); un cabezal liviano sobre representaciones
congeladas; entrenar sobre los datos humanos de siRNA y transferir.
**Criterio:** el conjunto de entrenamiento honesto que existe en este subcampo
son 31 siRNA probados en un coleóptero, de los cuales 29 entraron al modelo
publicado. No hay nada en Hemiptera. Cuatro evaluaciones independientes —Tang y
Koo en *Genome Biology*, BEND, BEACON y el relevamiento revisado por pares de 21
modelos de ARN— coinciden en que los modelos fundacionales no dan ventaja
consistente fuera de su dominio, y en la tarea medida más parecida a nuestro
tamizaje de off-target rinden la mitad que una red convolucional entrenada desde
cero. Entrenar sobre datos humanos y transferir es lo que la evidencia
desaconseja de forma más directa: el contenido GC en las posiciones 9 a 14 del
antisentido invierte su signo entre humano e insecto.
**Consecuencia:** el cálculo es determinista y reproducible bit a bit, lo que
satisface la palabra «reproducible» de la pregunta del track sin esfuerzo
adicional. Y el único conjunto de validación que existe sigue siendo conjunto de
validación: usarlo para ajustar lo habría quemado. La contracara es que no hay
nada que presentar como «nuestro modelo», y conviene decirlo antes de que lo
pregunten.

---

## D9 — Lo heredado de corridas anteriores se mantiene con su nivel de verificación declarado
**Fecha:** 2026-10-17
**Decisión:** las afirmaciones que vienen de una corrida previa de la misma
investigación se conservan tal como quedaron registradas, con su nivel de
verificación explícito, en lugar de reabrir todas las fuentes.
**Alternativas consideradas:** reabrir y reverificar cada fuente en cada corrida.
**Criterio:** reabrir tiene costo y no agrega información cuando la cita textual
quedó registrada en las notas; lo que sí agrega información es **declarar** qué
se verificó cuándo. El riesgo que importa no es que una fuente vieja esté mal
copiada: es que alguien lea el reporte creyendo que todo se verificó hoy.
**Consecuencia:** hay tres declaraciones vigentes que viajan con los números y
que hay que repetir al presentarlos. R4: 29 de las 52 entradas de `modelos.json`
tienen su especificación tomada de la tabla de un relevamiento revisado por pares
que sí se abrió, y no de su artículo primario; está declarado entrada por entrada
en el campo `nivel_verificacion`, y por eso esa investigación no marca su propia
lista de verificación como aprobada. R5: unas diez fuentes de la sección de
innovación abierta dependen de dominios institucionales que no estaban
disponibles en la última corrida —`argentina.gob.ar`, `embrapa.br`,
`repositorio.inta.gob.ar` y la API de GBIF—, conservan la verificación de la
corrida anterior con sus citas textuales en `notes/evidencia_verificada.md`, y no
se volvieron a comprobar. R1: una parte de las fuentes está marcada `[RES]`,
leída sólo en el resumen, y su hallazgo central sobre la ausencia de maquinaria
de RNAi en mollicutes proviene de una consulta de anotación, no de una búsqueda
por perfil.

---

## D10 — El corpus oficial no entra al control de versiones
**Fecha:** 2026-10-17
**Decisión:** `YHat-Biotech/` y `work/` quedan en `.gitignore`. El corpus se cita
por ruta y se describe en `research/ola2/MANIFEST.md`; sus archivos no se
commitean.
**Alternativas consideradas:** versionar el corpus completo para que el
repositorio sea autocontenido.
**Criterio:** el repositorio tiene remoto en GitHub, y la planilla
`Sequences_EPILAB.xlsx` contiene secuencias **no publicadas** de un tercero. Un
commit es un paso a un empujón de distancia de publicarlas. Los PDF, además, son
material con derechos de autor, y ya existía la decisión D6 para el material
pesado de referencia.
**Consecuencia:** quien clone el repositorio no recibe el corpus. Todo lo que se
use de él tiene que quedar citado con su archivo y su contenido descrito en el
manifiesto, no sólo referenciado. Y ninguna de las cinco investigaciones de la
ola 2 subió secuencias de EPILAB a un servicio de terceros: donde hacía falta un
ejemplo, se usó una secuencia pública de referencia, y la limitación quedó
declarada.

---

## D11 — El aporte se reorienta: desagregar lo que la herramienta oficial suma
**Fecha:** 2026-10-17
**Decisión:** el eje del aporte deja de formularse como «decidir mejor que un
modelo» y pasa a formularse como **desagregar y calificar el número que la
herramienta oficial ya produce**, más el término de conservación entre aislados,
que resultó tener un caso real y medido.
**Alternativas consideradas:** sostener el encuadre de la ola 1 sin cambios;
o pivotear hacia construir una herramienta de diseño propia.
**Criterio:** tres resultados de la ola 2, todos verificados. Primero, la
herramienta oficial **no estima eficacia de ninguna forma**: cuenta coincidencias
exactas de k-meros con Bowtie y las suma, de modo que la vara a superar es mucho
más baja de lo que suponía la ola 1. Segundo, ese conteo **no es interpretable
como riesgo** sin desagregarlo: está dominado por la condición de 16 pb (70 de 70
aciertos en maíz y 67 de 67 en abeja) y mezcla ventanas riesgosas con parálogos
alcanzados. Tercero, el candidato de cápside del EPILAB es 100 % idéntico sólo al
aislado de Costa Rica y pierde la mayor parte de sus siRNA conservados frente a
los aislados brasileños, lo que es precisamente lo que nuestro término de
conservación existía para detectar.
**Consecuencia:** la cartera de enfoques no cambia de orden, pero sí de
argumento, y hay un entregable nuevo y barato que antes no existía: una lectura
desagregada del tamizaje oficial, candidato por candidato. Queda registrado en
`SINTESIS_V2.md`.

---

## D12 — Las contradicciones entre investigaciones se adjudican con evidencia, no por autoridad
**Fecha:** 2026-10-17
**Decisión:** cuando dos investigaciones de la misma ola se contradicen, el
orquestador verifica el punto por su cuenta y deja escrito cómo lo resolvió, en
lugar de promediar, elegir la más reciente o dar por buena la que suene más
segura.
**Alternativas consideradas:** confiar en la investigación más específica del
tema; o reportar las dos sin resolver.
**Criterio:** en esta ola pasó dos veces y las dos se resolvieron mirando la
fuente. En el fitoplasma, W4 afirmó que el taxón 202462 no tenía ensamblados; tres
consultas directas a NCBI Datasets mostraron que sí —`total_count: 2`, genoma
completo de 576.118 pb— y que el error venía de consultar por nombre común en
lugar de por taxid. **La ola 1 tenía razón y la investigación nueva estaba mal**,
que es exactamente el caso que la regla «el corpus no gana por ser oficial» tiene
que cubrir. En MSMV, W4 dio el cuarto agente por resuelto y W3 mostró que la sigla
mapea a dos taxones de familias distintas: se adjudicó a favor de W3 por ser
estrictamente más completo.
**Consecuencia:** las dos correcciones se devolvieron a la investigación que las
produjo, que las aplicó y volvió a medir. Y queda una advertencia de método en el
repositorio: **un cero devuelto por una consulta por nombre común no es una
ausencia**; hay que resolver el taxid primero.

---

## D13 — El port de si-Fi21 tiene dos modos, y el fiel conserva los defectos a propósito
**Fecha:** 2026-10-19
**Decisión:** `tools/sifi21_port/` expone un modo `fiel`, que reproduce si-Fi21 tal
como es —incluida la rama que permite declarar eficiente un siRNA que falla los
filtros termodinámicos—, y un modo `corregido` con los arreglos justificados. El
modo por defecto del CLI es el corregido; el fiel hay que pedirlo.
**Alternativas consideradas:** (a) portar y arreglar, sin conservar el
comportamiento viejo; (b) portar sin arreglar nada y dejar la crítica por escrito;
(c) dos implementaciones separadas.
**Criterio:** arreglar sin conservar hace imposible la tarea que el investigador
pidió primero, que es auditar los números que ya existen. Si el modo fiel no
existe, no se puede responder «¿de dónde salen los 114?», porque cualquier
discrepancia se confunde con nuestros propios arreglos. Al revés, portar sin
arreglar nos deja usando para diseñar una regla que sabemos mal. Dos
implementaciones separadas duplican el código y se desincronizan; un parámetro de
modo sobre el mismo código no, y además permite **medir** cuánto cambia cada
arreglo, que es la parte interesante.
**Consecuencia:** la diferencia entre los dos modos es un dato, no una molestia.
Medida sobre el corpus, contando ventana por ventana, la rama del original agrega
**19 de 133** «eficientes» en `MP_MRFV_full`, 7 de 32 en `CP_MRFV_full`, 50 de 212
en `BicC_Dm_full` y 8 de 42 en `ATPaseD_Dm_full`: entre el **14 % y el 24 %** de lo
que si-Fi reporta como eficiente lo es solo porque la regla terminal se saltea la
física, y ninguna ventana va en sentido contrario.
*(Una versión anterior de esta entrada decía «11 de 133, entre el 8 y el 9 %». Era
una resta de totales —eficientes menos termodinámicos— y el total termodinámico
incluye ventanas de la rama 4, que los dos modos rechazan igual. Restar totales no
cuenta ventanas.)*
Ese número es un entregable, y no habría existido con ninguna de las
alternativas. Queda en `tools/sifi21_port/CAMBIOS.md` C1.
**Nota de alcance:** el modo fiel es fiel al fuente de GitHub, que no es idéntico
al binario de 2017 de SourceForge. `[?]`

**La decisión quedó validada el mismo día.** Se corrió el **programa original** —el
binario, con su interfaz y sus valores por defecto— sobre los cuatro genes, y el
modo fiel reproduce sus cuatro conteos exacto: **42, 32, 133 y 212**. `[E]` Eso es
precisamente lo que la alternativa (a) —portar y arreglar sin conservar el
comportamiento viejo— habría hecho imposible: sin modo fiel no hay contra qué
comparar, y la diferencia de la regla terminal seguiría siendo una lectura del
código en vez de una medición. Detalle en
`research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md` §0; salidas crudas del
programa en `analisis/sifi21_original_*.csv`.

---

## D14 — El gráfico por gen tiene un solo eje, y la curva se indexa por el centro de la región
**Fecha:** 2026-10-19
**Decisión:** las tres capas del gráfico de cada gen —la curva de densidad, las
bandas de región y las tiras de marcas por ventana— comparten un único eje
horizontal en coordenadas del gen. La curva se indexa por el **centro** de la región
candidata, no por su inicio, y se dibuja sólo en el tramo donde cabe una región
completa.
**Alternativas consideradas:** (a) indexar la curva por el inicio de la región, que
es la variable que el código ya barría; (b) dos ejes, uno para la curva y otro para
las tiras; (c) extender la curva a todo el gen contando regiones truncadas en los
bordes.
**Criterio:** la primera versión hizo (a) y (b) a la vez sin darse cuenta: la curva
iba de 1 a *n−L+1* y las tiras de 1 a *n*, así que **las capas estaban desalineadas
y las bandas no coincidían con las marcas**. Con 300 nt de región en un gen de 491
—el caso de `ATPaseD_Dm`— el desfasaje era de más de dos tercios del ancho. Indexar
por el centro arregla el eje sin cambiar un solo número: el máximo de la curva
corresponde a la misma región que devuelve `best_region`, sólo reindexada. La
opción (c) se descartó porque un conteo sobre una región truncada no es comparable
con los demás y produciría una caída artificial en los bordes.
**Consecuencia:** el gráfico es legible de una pasada y la curva arranca y termina
donde deja de haber opciones, lo que comunica gratis algo que importa: en
`ATPaseD_Dm` hay apenas 172 regiones posibles y en `BicC_Dm` hay 2.201. Además salió
a la luz un bug latente en `best_region`, que consideraba regiones pasadas del final
del gen; con los cuatro genes del corpus el máximo caía dentro del dominio válido,
así que acotarlo no movió ningún número publicado.
**Nota:** las decisiones de color están en `CAMINOS_PROBADOS.md`, porque se tomaron
descartando alternativas con el validador de paleta.

**Revisión del mismo día, a partir de una lectura del equipo.** La primera versión
dibujaba la curva **sólo** donde cabe una región completa, y eso se leía como un
hueco: en `BicC_Dm` la banda de la región más densa llega hasta 2422 y la curva se
cortaba en 2350, así que parecía faltar dato dentro de la banda. El diagnóstico es
que el eje tenía **dos significados a la vez** —las bandas y las tiras marcan la
extensión en nucleótidos, la curva indexaba por el centro de la región— y eso no se
resuelve con una aclaración al pie.
**Corrección:** la curva pasa a estar definida en todas las posiciones del gen. En
los dos extremos la región se recorta contra el borde, el valor baja de verdad
—porque ahí hay menos ventanas alcanzables, no porque falte el dato— y esos tramos
van punteados para no darlos por comparables.
**Lo que esto habilita, y que conviene conservar:** leída en el centro de cualquier
banda, la curva da **exactamente** el conteo de esa región en la tabla. Es una
propiedad verificable, y está verificada en las ocho combinaciones de gen y región.
Un gráfico que contradiga su propia tabla es peor que no tener gráfico.

---

## D15 — La contradicción del 7,2 % se adjudica midiendo, y lo que las separa es el nulo
**Fecha:** 2026-10-20
**Decisión:** las dos mediciones que parecían contradecirse —`pipeline/REPORT.md` §6,
que dice que afinar la región no discrimina, y `sifi21_reproduccion.md` §3, que dice
que las cuatro regiones de EPILAB están 19-46 % por debajo del óptimo— **no se
contradicen**, y la diferencia se explica entera por el modelo nulo y por el sesgo
del máximo. El ranking **no** apoya ninguna recomendación de mover una región en la
ganancia de densidad; la apoya en la exposición a no objetivo.
**Alternativas consideradas:** (a) declarar que no son comparables porque miden
cantidades distintas y seguir, que es una explicación y no una adjudicación;
(b) elegir una de las dos por autoridad del documento más reciente; (c) hacer la
medición que faltaba, que es construir el nulo del lado de si-Fi21.
**Criterio:** se hizo (c), con tres resultados. **Primero**, el nulo del 7,2 % sí es
reproducible: está en `baseline_dsrip/region_nulo_multigen.py`, no en
`region_scoring.py` como decía el registro, y con las rutas corregidas da la misma
ganancia mediana de 7,2 % y los mismos 0 de 20 genes. Tiene una asimetría de método
—paso 5 para el observado y 20 para el nulo— y corregirla no cambia el veredicto.
**Segundo**, el percentil reemplaza al porcentaje: la región de `MP_MRFV` está en el
percentil 91 de su propio gen y las otras tres alrededor de la mediana, lo que es
una afirmación falsable donde «21 % por debajo del óptimo» no lo era, porque el
óptimo es un máximo sobre cientos de regiones superpuestas y está sesgado hacia
arriba. Medido: barajando la etiqueta de eficiente, el máximo queda 17-46 % por
encima de la media sólo por maximizar. **Tercero**, con el mismo estadístico sobre
los cuatro genes, el nulo que baraja etiquetas da 3 de 4 significativos y el nulo de
bloques de 30 —el del 7,2 %— da 0 de 4. Las dos mediciones contestan preguntas
distintas: si las eficientes están agrupadas (sí) y si el mejor grupo es mejor que
otro grupo (no).
**Consecuencia:** el ranking recomienda mover región en `BicC_Dm` y `ATPaseD_Dm`
**por el veto de off-target y no por densidad**, y lo dice así. La correlación entre
el puntaje biofísico del pipeline y la densidad de si-Fi21 es +0,63 y +0,49 en los
dos genes donde la comparación tiene poder, así que una es sustituta imperfecta de
la otra. Detalle en `research/ola2/W7_ranking/REPORT.md` §1.
**Nota de método que conviene conservar:** el número de regiones independientes es
el largo del gen dividido el largo de la región —entre 1,6 y 8,3 acá—, no las
cientos de regiones deslizantes que se promedian. Por eso no se reporta ningún valor
p sobre esas correlaciones.

---

## D16 — Los dos ejes se combinan con media geométrica, y el veto queda como compuerta aparte
**Fecha:** 2026-10-20
**Decisión:** el puntaje es la media geométrica ponderada de eficacia y limpieza, y
el veto duro por coincidencia perfecta de 21 nt se conserva como compuerta previa,
no como un término del puntaje. Se reportan además la suma ponderada y la cascada.
**Alternativas consideradas:** (a) suma ponderada, que dice que una región muy
eficiente puede comprar su propio riesgo; (b) sólo la cascada de
`pipeline/region_scoring.py` —`buenos_limpios` más veto—, que trata los ejes como
filtro y no como puntaje; (c) la media geométrica sola, sin veto.
**Criterio:** la media geométrica tiene antecedente medido en `pipeline/REPORT.md`
§5, donde por suma ponderada entraba tercero un candidato con accesibilidad 0,0388
compensada por una asimetría de 6,4 y por media geométrica no entraba; una región
expuesta compensada por eficaz es el mismo error con otro nombre. El veto no se
disuelve en el puntaje porque no es una ponderación: es la afirmación de que cierto
hecho descalifica, y expresarlo como peso permitiría comprarlo.
**Consecuencia:** **la decisión no cambia el ranking.** Con suma ponderada `MP_MRFV`
sigue primero (91 % contra 99 % de los sorteos) y `CP_MRFV` segundo; lo único que se
mueve es el tercer puesto, que ya era inestable. Que la forma de combinación no
decida es, con estos cuatro candidatos, un resultado.
**Lo que se pierde, declarado:** la media geométrica trata los dos ejes como
igualmente confiables, y no lo son: «eficiente» es una predicción nuestra con umbral
discutible y «coincidencia perfecta de 21 nt» es un hecho de secuencia.

---

## D17 — Se mantiene la posición conservadora del código: una ventana riesgosa cuenta aunque no sea eficiente
**Fecha:** 2026-10-20
**Decisión:** se **mantiene** y no se overridea la posición que
`pipeline/region_scoring.py` ya había tomado en código: una ventana con coincidencia
en un no objetivo cuenta como riesgo sea eficiente o no.
**Alternativas consideradas:** (a) la regla mecanicista, que sólo cuenta como riesgo
las ventanas que además son eficientes, con el argumento de que una ventana que no
carga bien en el complejo no silencia nada, y con dato propio a favor —en `MP_MRFV`,
de 22 ventanas con off-target del gen entero sólo 2 son eficientes—.
**Criterio:** no es un argumento mecanicista sino de dónde poner la incertidumbre.
«Eficiente» es una predicción de si-Fi21 con un umbral que no reproduce los conteos
declarados por el propio laboratorio —ninguna de 15.120 configuraciones lo hace— y
del que entre el 14 % y el 24 % entra por una rama que se saltea la termodinámica.
La exposición, en cambio, se mide por coincidencia exacta de secuencia y no depende
de ningún umbral nuestro. Apostar la seguridad al componente más débil de la cadena
es la apuesta equivocada.
**Consecuencia:** se reporta el ranking bajo las dos reglas y **el orden de los dos
primeros no cambia**. Lo que cambia es la estabilidad del tercer puesto: bajo la
regla mecanicista con escala absoluta se vuelve determinista y bajo la conservadora
se reparte 75-25. La decisión no cambia quién gana, cambia cuánta confianza se puede
tener en el orden de los que pierden.
**Lo que se pierde:** se descartan regiones que probablemente sean seguras, y se
penaliza de más a las regiones largas, que por tener más ventanas tienen más chance
de que alguna pegue.

---

## D18 — Los pesos por referencia se justifican por consecuencia, y el panel es el límite real
**Fecha:** 2026-10-20
**Decisión:** pesos base maíz 1,00, *Harmonia axyridis* 0,80, *Apis mellifera* 0,80,
*Homalodisca vitripennis* 0,60, *Folsomia candida* 0,40, barridos sobre todo el
símplex. El riesgo de una ventana es su **peor** acierto entre referencias, no la
suma.
**Alternativas consideradas:** (a) pesos iguales, que es una posición y no una
ausencia de posición; (b) sumar los aciertos entre referencias en vez de tomar el
máximo; (c) ponderar por número de parálogos alcanzados.
**Criterio:** por consecuencia. Un acierto en maíz es daño al objetivo mismo de la
intervención; uno en *H. axyridis* es contraproducente en sentido fuerte porque
ayuda a la plaga; uno en *A. mellifera* tiene costo regulatorio antes que ecológico;
*H. vitripennis* es riesgo ecológico y además esperable por conservación
filogenética; *F. candida* es el modelo estándar de ecotoxicología. Se toma el
máximo y no la suma porque una ventana es peligrosa por su peor coincidencia: si ya
pega perfecto en maíz hay que sacarla, y sumar haría que seis aciertos leves pesaran
como uno grave.
**Consecuencia:** el orden de los dos primeros aguanta todo el símplex. Donde los
pesos muerden es en el tercer puesto, porque `BicC_Dm` concentra su exposición en
*H. vitripennis*: subirle el peso a esa referencia lo hunde y bajárselo lo levanta.
Ésa es la razón honesta de que el tercer puesto sea inestable, y depende de una
pregunta que no nos corresponde contestar.
**Dos cosas que hay que escribir aunque no cambien el número:** el criterio de
genoma contra transcriptoma que el investigador entregó **ya está resuelto por
construcción**, porque las cinco referencias no objetivo son transcriptomas y la
única genómica es la del vector, que entra como on-target; no hay nada que
descontar. Y el límite del panel: la ausencia de riesgo en cicadélidos nativos y
parasitoides **no está medida**, porque no hay transcriptomas. Un peso sobre una
referencia que no existe es cero por omisión, no por evidencia.

---

## D19 — Los tres criterios de riesgo se ordenan, no se cuantifican
**Fecha:** 2026-10-20
**Decisión:** `perfecto_21` > `perfecto_ge19` > `mm1_21`, con pesos base 1,00, 0,60
y 0,30 barridos **conservando ese orden**. El veto usa sólo `perfecto_21`.
**Alternativas consideradas:** (a) tratarlos como equivalentes; (b) fijar pesos de
la literatura, que no los da para esta combinación; (c) ponderar también por la
posición del desajuste dentro de la ventana.
**Criterio:** lo único que la evidencia sostiene es el orden —un bloque perfecto más
largo no puede ser menos riesgoso que uno más corto—, así que el barrido deja libres
las magnitudes y fija el orden. (c) no se hizo: no tenemos evidencia para distinguir
un desajuste en la región semilla de uno en el extremo 3', y se declara `[?]` en vez
de inventar un peso.
**Consecuencia:** los pesos de criterio no mueven el orden de los dos primeros. El
veto es insensible a esta decisión porque usa un solo criterio; y eso es deliberado:
si el veto se disparara con bloque de 19, `MP_MRFV` y `ATPaseD_Dm` también quedarían
vetados y la compuerta dejaría de discriminar. **Que el veto use 21/21 y no 19 es lo
que lo hace informativo.**
**Nota que corrige un matiz propio:** la frase de `sifi21_reproduccion.md` §4 «cero
coincidencias en *Apis mellifera* para los cuatro genes» es cierta para los
criterios de bloque perfecto pero **no para el de un desajuste**: `BicC_Dm` tiene 7
ventanas con un desajuste contra *Apis*. La conclusión de fondo no cambia; la frase
hay que decirla con el criterio al lado.

---

## D20 — Dos rankings, uno por estrategia, con el criterio de comparación declarado
**Fecha:** 2026-10-20
**Decisión:** se presentan dos rankings separados —genes virales y genes del
insecto— más un criterio declarado de comparación entre estrategias. No se fuerza un
orden único.
**Alternativas consideradas:** (a) un solo ranking de los cuatro, que exige una
equivalencia entre los dos tipos de candidato; (b) dos rankings sin criterio de
comparación, que deja la decisión sin cerrar.
**Criterio:** los off-targets no significan lo mismo en los dos casos, y la
asimetría es de signo y no de magnitud: para los genes del insecto el genoma de
*D. maidis* se excluye por ser on-target, y para los virales entra como off-target
—9 ventanas de `MP_MRFV`, 2 eficientes— pero pegarle al vector mientras se apunta al
virus no es obviamente un defecto. Un solo ranking obligaría a asignarle un signo a
ese acierto y no tenemos con qué.
**El criterio de comparación, que es posición nuestra y no medición:** preferimos la
vía del insecto, por la recomendación del investigador —es más directa— y por el
argumento propio de la ventana de latencia de unos 20 días, que él aceptó; a lo que
se agrega que una intervención sobre el vector corta la transmisión de los cuatro
agentes del complejo y una sobre `MRFV` corta uno.
**Consecuencia, y es el punto más atacable del entregable:** por los números ganan
los dos candidatos virales; por la estrategia preferimos la del insecto. No son
contradictorios porque el ranking mide calidad de diseño dentro de un gen dado y no
valor del blanco, pero **si se forzara un orden único los dos virales quedarían
arriba, y eso sería un artefacto de que el ranking no mide valor del blanco**. Queda
dicho en el reporte en lugar visible.
**Verificado:** con el genoma del vector neutralizado para los virales en vez de
contado como off-target (`--dmaidis-viral neutro`), `MP_MRFV` sigue primero y
`CP_MRFV` segundo. La decisión refuerza el orden en vez de darlo vuelta.

---

## D21 — Se subieron las dos secuencias virales a dsRNA-Engineer, con la compuerta cumplida en los dos pasos
**Fecha:** 2026-10-20
**Decisión:** se subieron `MP_MRFV` y `CP_MRFV` al servicio web dsRNA-Engineer.
`BicC_Dm` y `ATPaseD_Dm` **no se subieron**.
**Alternativas consideradas:** (a) no subir nada y dejar el benchmark con dos
herramientas sobre los cuatro genes y la tercera sobre la secuencia pública que ya
se había corrido; (b) subir las cuatro, que está prohibido sin excepción.
**Criterio:** la compuerta tiene dos pasos y los dos se cumplieron **en esta
corrida**. Paso 1: reverificación byte a byte contra `NC_002786.2` recalculada acá,
no heredada de otro documento nuestro — `MP_MRFV` es la subcadena exacta 332-1594 y
`CP_MRFV` la 5674-6201, las dos en hebra +, de modo que son material ya publicado en
el NCBI y subirlas no revela nada. `BicC_Dm` y `ATPaseD_Dm` no son subcadenas de
nada publicado. Paso 2: confirmación explícita de la persona, pedida antes de subir
nada y mostrando qué secuencia iba y a dónde; la autorización fue para las dos
virales únicamente. Sin cualquiera de los dos pasos la decisión habría sido (a).
**Consecuencia:** el benchmark de las tres herramientas existe sobre los dos genes
virales y queda con dos herramientas sobre los dos del insecto. Ese hueco **es** un
resultado y va a la presentación: la herramienta que el organizador señala como la
de diseño y verificación de off-targets es la que no se puede usar con el material
que el organizador entregó. Proyectos `ff5138f6b1e5a91c` y `c816ff87893b36a4`,
registrados en `research/ola2/W7_ranking/dsrnaengineer_corrida.json`.

## D22 — El panel de no objetivo se amplía con el pariente más cercano y con humano, y el largo de ventana pasa a ser un parámetro declarado
**Fecha:** 2026-10-20
**Decisión:** el veto por coincidencia perfecta de 21 nt se evalúa también contra
*Macrosteles quadrilineatus* (`GCF_028750875.1`, transcriptoma) y *Homo sapiens*
(`GCF_000001405.40`, transcriptoma), y toda recomendación de región declara a qué largo de
ventana se calculó, reportando 21 y 22 nt cuando difieren.
**Alternativas consideradas:** (a) dejar el panel de seis de W7 y anotar la ausencia como
límite; (b) bajar el catálogo completo de 26 especies de `pipeline/no_objetivo_catalogo.py`;
(c) seguir sólo con 21 nt, que es lo que hacen si-Fi21 y todo el repositorio.
**Criterio:** (a) no alcanza porque la especie que falta no es una más: `pipeline/REPORT.md`
§4.2 ya había medido que *M. quadrilineatus* descarta 70 veces más que el maíz y que 613 de
sus 700 descartes no los ve ninguna otra especie, y es el cicadélido con genoma anotado más
cercano a *Dalbulus*. Humano lo nombró el investigador y lo pide `CLAUDE.md`. (b) es lo
correcto a futuro pero son 26 descargas y el objetivo acá era falsar una recomendación
concreta, para lo que alcanza con que agregar referencias sólo pueda agregar vetos. (c) deja
fijo un parámetro que `R1_fundamentos` §2.1 muestra que es específico de orden y que para
hemípteros no está publicado.
**Consecuencia:** la recomendación de W7 §2.2 de mover la región en los dos genes del insecto
**no sobrevive**. En `BicC_Dm` la región propuesta (2123-2422) tiene 19 ventanas con 21/21
contra *Macrosteles* y la de EPILAB tiene 10; la alternativa 922-1221 conserva 36 de las 37
ventanas eficientes y escapa al veto. En `ATPaseD_Dm` ninguna región de 300 nt escapa, y la
salida es acortar a 200 nt (94 de 272 regiones limpias, la mejor 88-287 con 17 eficientes),
lo que además devuelve el diseño al rango de 150-250 nt que declaró el investigador. Los dos
genes virales no se tocan: cero coincidencias perfectas contra las dos referencias nuevas.
Sobre el largo: el conteo total de eficientes se mueve menos de un punto porcentual entre 21
y 22 nt, pero el conjunto cambia casi entero (Jaccard 0,20 a 0,39), y en `MP_MRFV` la mejor
región se muda de 72-271 a 820-1019. Detalle en `research/ola3/C6_panel_y_largo/REPORT.md`.

## D23 — *Macrosteles quadrilineatus* queda fuera del panel del ranking v2
**Fecha:** 2026-10-21
**Decisión:** el ranking v2 se calcula con el panel de W7 más humano y **sin** *Macrosteles
quadrilineatus*. Modifica la parte de D22 que lo incorporaba al veto; el resto de D22 (humano y el
largo de ventana como parámetro declarado) sigue vigente.
**Alternativas consideradas:** (a) mantener *Macrosteles* como en D22, donde reordena la
recomendación de `BicC_Dm`; (b) incluirlo solo como sensibilidad.
**Criterio:** decisión del equipo, con el argumento de que la especie no está en Argentina y por
lo tanto no es un organismo expuesto. ~~**Ese argumento no está verificado**: una búsqueda inicial
no encontró registros sudamericanos, pero no es un catálogo de distribución, así que es `[R]` y
queda pendiente.~~ **Verificado el 2026-10-21 contra GBIF** (`taxonKey` 2039662): de 3.592
ocurrencias, 2.929 son de Canadá y 549 de Estados Unidos, y hay cero en Argentina y cero en las
siete consultas sudamericanas (AR, BR, CL, UY, PY, BO, PE); los únicos registros neotropicales son
cuatro ocurrencias sueltas en México, Panamá, Jamaica y Puerto Rico. El género llega a Argentina
con una sola ocurrencia. `[E]` La premisa fáctica se sostiene. Queda la salvedad de método: GBIF
mide esfuerzo de muestreo y Sudamérica está submuestreada para Cicadellidae, así que lo que
sostiene la conclusión es la proporción y la concentración norteamericana, no el cero aislado `[H]`. Contra (a): *Macrosteles* se había incorporado como sustituto filogenético del
resto de los Deltocephalinae, no por exposición directa, y ese uso no se descarta con su
ausencia en Argentina; se acepta igual porque el equipo prefiere acotar el panel a organismos
con exposición plausible.
**Consecuencia:** las recomendaciones de región de W7 vuelven a valer contra el panel de seis
más humano (`BicC_Dm` 2121-2420, `ATPaseD_Dm` 72-371). Las mediciones de C5 y C6 contra
*Macrosteles* no se borran: el informe v2 las cita como límite (21 ventanas con 21/21 en el gen
entero de `eth`; 19 en la región recomendada de `BicC_Dm`). Reabrir si el investigador dice que
los cicadélidos hermanos cuentan como no objetivo.

## D24 — El ranking v2 suma dos genes de *D. maidis*, y evidencia y diseño quedan en ejes separados
**Fecha:** 2026-10-21
**Decisión:** (1) `eth` y `burs-alpha` (GenBank PZ371507.1 y PZ371508.1) entran al ranking, con la
región de 200 nt que elige la misma cascada con la que W7 recomienda regiones; (2) humano entra al
panel con peso base 1,00; (3) todo se corre a 21 y a 22 nt; (4) la comparación entre candidatos
es el nivel 3 (cada uno en su mejor región), no el nivel 1 (regiones de EPILAB tal como están);
(5) la evidencia publicada de cada gen se presenta como un segundo eje descriptivo, **sin puntaje**.
**Alternativas consideradas:** sumar la evidencia al puntaje; incluir los ortólogos de C5
(`Rpn6`, `Ruvbl1`, `XPO1`, ATP sintasa β); comparar solo en el nivel 1.
**Criterio:** sumar evidencia exigiría una equivalencia entre un fenotipo de microinyección y uno
de ingesta que no tenemos. Los ortólogos no entran porque C5 midió que solo entre el 0,7 % y el
11,1 % de sus 21-meros existen en el genoma del vector. El nivel 1 mezcla regiones elegidas por
procedimientos distintos y favorece a los nuevos.
**Consecuencia:** los genes nuevos quedan cuartos y quintos por diseño cuando todos están en su
mejor región; su aporte es la evidencia y, en `burs-alpha`, el perfil de especificidad (cero
bloques de 19 nt o más en el gen entero). Las puntas del orden (`MP_MRFV` primero, `BicC_Dm`
segundo, `ATPaseD_Dm` último) aguantan 22 nt bajo la escala absoluta; el medio no. Detalle en
`research/ola3/C7_ranking_v2/REPORT.md`.

## D25 — La región recomendada de `BicC_Dm` pasa de 2121-2420 a 922-1221, por conservación
**Fecha:** 2026-10-21
**Decisión:** para `BicC_Dm` se recomienda la región 922-1221 (300 nt, a 21 nt) y no 2121-2420, que era la
de C7. Para `ATPaseD_Dm` se mantiene 72-371.
**Alternativas consideradas:** (a) mantener 2121-2420, que tiene un eficiente menos —cifra retirada como argumento por D65, porque ese margen se empata con el contador del laboratorio y se invierte con el motor del original— y 12 ventanas menos con
señal de off-target; (b) elegir por conservación sin mirar el veto; (c) usar el genoma de Córdoba (ONT) como
criterio.
**Criterio:** de las 35 eficientes de 2121-2420 solo 22 son idénticas en los tres transcriptomas públicos y
9 de las 27 presentes en el genoma de referencia faltan en el de Córdoba; 922-1221 tiene 36 eficientes, 32
idénticas en los tres, 36 de 36 en el transcriptoma argentino y 36 de 36 exactas en Córdoba, y no tiene
coincidencias perfectas de 21 nt con el panel. (b) se descartó porque la región más conservada de
`ATPaseD_Dm` (137-436) está vetada. (c) se descartó porque un ensamblado ONT a 20x tiene una tasa de error
del orden de la variación que se busca: el genoma de Córdoba se reporta pero no entra al criterio.
**Consecuencia:** cambiar la región no mueve el ranking de diseño (`BicC_Dm` sigue segundo, 94,8 % de los
sorteos). 922-1221 es la misma región que C6 había encontrado como salida al veto de *Macrosteles*, y ahora
aparece por un motivo independiente de ese pariente. La conservación es entre fuentes públicas (tres
transcriptomas y un genoma de Córdoba), no entre poblaciones de campo. Detalle en
`research/ola3/C8_conservacion/REPORT.md`.


---

## D26 — El criterio de eficiencia se reporta con sus términos continuos, no sólo con el booleano
**Fecha:** 2026-10-21
**Quién:** el orquestador, al integrar la ola 3 (candidata de C1, con el respaldo de C5).
**Decisión:** todo entregable que use si-Fi21 publica, por ventana, la brecha de ΔG entre extremos,
la probabilidad de apertura del sitio blanco y los dos nucleótidos de la regla terminal, y deja el
booleano de si-Fi como columna de compatibilidad con lo que usa el laboratorio. Además, cada
término estructural declara su régimen de validez: plegado local con alcance de hasta ~150 nt
—exactitud mediana publicada ~0,6— sí; plegado global de un ARN largo o estructura terciaria, no.
**Alternativas consideradas:** reportar sólo el booleano, que es lo que hace la herramienta; o
reemplazar el criterio por uno propio.
**Criterio:** de los seis valores que componen el veredicto, **dos no tienen ninguna fuente
primaria** (la brecha de 1,00 kcal/mol y los 22 °C) y dos la tienen para el principio pero no para
el número (asimetría y accesibilidad). Un booleano construido sobre cortes sin fuente esconde
exactamente la información que permitiría discutirlos. Publicar los términos continuos cuesta una
columna y deja el corte a la vista.
**Consecuencia:** quien no esté de acuerdo con un umbral puede recalcular sin volver a correr
nada, que es la definición operativa de auditable. Y queda escrito que el booleano de si-Fi se
conserva por compatibilidad, no por acuerdo.

---

## D27 — El tamizaje de off-targets por ventana no se hace con BLAST, y ahora hay número
**Fecha:** 2026-10-21
**Quién:** el orquestador, al integrar la ola 3 (candidata de C3).
**Decisión:** el tamizaje de ventanas de 21 nt se hace con coincidencia exacta y presupuesto de
desajustes (`offtarget_21nt.py`) o con Bowtie, nunca con BLAST. Si por algún motivo hay que usar
BLAST igual, la configuración es `blastn-short` con **`-word_size 10`**, más
`-ungapped -dust no -soft_masking false` y postfiltro obligatorio por `length` y `mismatch`.
**Alternativas consideradas:** `blastn-short` con sus valores por defecto (palabra 7), que da lo
mismo y cuesta unas veinte veces más; o seguir usando `blastn` por su mayor sensibilidad nominal.
**Criterio:** medido sobre 3.150 consultas con desajustes plantados en cada una de las 21
posiciones, **ninguna de trece configuraciones recupera el 21-mero en todas las posiciones**: el
techo es 0,762 con `-task blastn` y 0,619 con cualquier `blastn-short`, y `megablast` por defecto
da **cero**. La causa no es sólo el tamaño de palabra —10 es el máximo que no pierde la posición
11, por ⌊(21−1)/2⌋— sino el modelo de puntaje, que recorta un desajuste cercano al extremo en vez
de cruzarlo. Confirma por medición la decisión que ya estaba vigente por lectura.
**Consecuencia:** si algún entregable usa BLAST para esto, declara el sesgo por posición. Y queda
registrado que el criterio de un desajuste medido con BLAST subestima por un factor de hasta 3,2.

---

## D28 — El umbral de coincidencia se declara en dos niveles, y «genoma» no es una clase de blanco
**Fecha:** 2026-10-21
**Quién:** el orquestador, al integrar la ola 3 (candidatas de C4 y C3).
**Decisión:** se reporta siempre el conteo con **21/21 perfecto** y el conteo con **bloque perfecto
de ≥ 19 nt**, diciendo cuál es cuál; no se reportan coincidencias de 16 a 18 nt como off-targets.
Y los aciertos se clasifican por clase de blanco —exón codificante, unión exón-exón del ARNm
maduro, ARN no codificante anotado, intrón, intergénico sin anotación— en vez de por «genoma
contra transcriptoma».
**Alternativas consideradas:** elegir un solo umbral «del campo», que es lo que se venía haciendo
sin fuente; y aplicar el criterio del investigador tal cual, preguntando sólo si el acierto está
en el transcriptoma.
**Criterio:** el umbral de 21 nt tiene bioensayo detrás en insectos y el de 19 es convención del
campo con fundamento mecánico declarado pero sin experimento, así que mezclarlos en un número
borra la diferencia de evidencia. Sobre el corte inferior, la medición es contundente: a 19 nt el
azar explica el total de coincidencias y son 25 sobre 4.730 ventanas en un genoma de 972 Mb,
mientras que a 16 nt son 1.979 y están a la par del azar con la misma composición. Sobre las
clases, se midió que la asimetría entre genoma y transcriptoma **va en los dos sentidos**: el
genoma pierde las ventanas de unión de exones, que fueron las únicas que tocaron secuencia
expresada de maíz.
**Consecuencia:** el criterio que entregó el investigador se implementa, pero corregido: no alcanza
con preguntar si está en el transcriptoma, hay que preguntar en qué parte cae. Y pasar de 19 a 21
nt borra todo el riesgo en maíz de nuestras 920 ventanas salvo un acierto, que cae en región
intergénica.

---

## D29 — El rango de 150 a 250 nt es convención declarada; lo único respaldado es el piso
**Fecha:** 2026-10-21
**Quién:** el orquestador, al integrar la ola 3 (candidatas de C4 y C1).
**Decisión:** el rango que usa el laboratorio se adopta como convención declarada y no como
restricción respaldada. Si una región candidata queda mejor con 300 nt, el largo no es argumento
para descartarla. La restricción que sí se respeta es el **piso de ~60 pb**.
**Alternativas consideradas:** adoptar 150-250 como restricción dura, que es lo que veníamos
haciendo implícitamente.
**Criterio:** se verificó una por una la ausencia en las tres fuentes posibles. **En el artículo no
hay ninguna recomendación de largo** —al contrario, sus construcciones del «reloj molecular» son
de 500 pb y las ventanas de accesibilidad de 100 pb rellenadas hasta 500—; **en el manual el
criterio de región es cualitativo**, sin largo mínimo ni máximo; y **si-Fi21 directamente no busca
regiones**: dibuja el perfil y la elección la hace una persona. En la literatura abierta, el piso
de ~60 pb está medido como serie de largos, y hay evidencia en contra de un techo bajo **en la
propia especie blanco**: silenciamiento publicado con ARNdc de 544 y 578 pb en *Dalbulus maidis*.
Una revisión de 2025 dice que no hay consenso sobre el largo óptimo.
**Consecuencia:** la búsqueda de la región de 200 nt más densa es un agregado del port y hay que
presentarla así. Y queda como pregunta de alto rendimiento para el investigador: si hay un ensayo
propio con largos comparados en su especie, ese dato vale más que toda nuestra tabla de literatura.

---

## D30 — La identidad de un gen se resuelve por secuencia antes que por nombre
**Fecha:** 2026-10-21
**Quién:** el orquestador, al integrar la ola 3 (candidata de C5).
**Decisión:** antes de buscar un gen publicado en el proteoma o el transcriptoma de una especie
anotada, se traduce y se compara contra proteínas revisadas de UniProt (`blastx`) para fijar a qué
familia pertenece. Dos minutos por gen nuevo del ranking.
**Alternativas consideradas:** confiar en el nombre de la anotación automática, que es lo que hace
el paso 4 del circuito de ingeniería inversa y lo que W4 §6.1 ya había declarado como límite.
**Criterio:** hay un caso medido. El gen que un trabajo de 2025 llama `Rpn6` en *Scaphoideus
titanus*: el **nombre** lleva a la subunidad 11 del proteasoma y la **secuencia** a la subunidad 6
(45,2 % de identidad con la familia PSMD6 humana contra 20,4 % con PSMD11), y el conteo de
ventanas eficientes cambia de 162 a 98 —un 65 %— según cuál se tome.
**Consecuencia:** cualquier candidato nuevo que entre al ranking lleva su familia verificada por
secuencia. Y la discrepancia de nomenclatura de ese trabajo queda como pregunta para el
investigador, porque es la única de esa investigación que no se puede contestar con bibliografía.

---

## D31 — Las quimeras se recalculan enteras, y la región no se entrega como un argmax
**Fecha:** 2026-10-21
**Quién:** el orquestador, al integrar la ola 3 (candidatas de C4 y C3).
**Decisión:** una quimera se evalúa completa y **en los dos órdenes**, nunca sumando los conteos de
las partes. Y la recomendación de región no se entrega como «la mejor», sino como el conjunto de
regiones que están en el top-5 con ventana de 21 y de 22 nt, declarando el solapamiento en
nucleótidos cubiertos como medida de estabilidad.
**Alternativas consideradas:** el atajo de sumar las partes, que es lo que sugiere la intuición; y
entregar el máximo puntual, que es lo que veníamos haciendo.
**Criterio:** medido, el orden de pegado cambia el total de eficientes entre +3 y +19 sobre la suma
de partes, y el cambio de veredicto de ventanas heredadas llega hasta **54 nt** de la unión, así
que el atajo puede errar por hasta 10 ventanas en una molécula de 500 nt. Sobre el argmax: al
pasar la ventana de 21 a 22 nt, en los dos genes largos **la región ganadora se muda de lugar del
gen** —en `BicC_Dm` la ganadora a 21 nt queda 166.ª a 22—, mientras que el solapamiento del top-5
se mantiene entre 0,74 y 0,83.
**Consecuencia:** hay un sesgo de borde que antes no estaba contabilizado: las ventanas de los
primeros y últimos ~60 nt de una región recortada no valen lo que valían dentro del gen entero.
Si el laboratorio elige región mirando el perfil del gen completo, ese sesgo está presente.

---

## D32 — El port no se parece al código del INTA, y la licencia del original queda sin resolver
**Fecha:** 2026-10-21
**Quién:** el orquestador, al integrar la ola 3 (candidata de C2).
**Decisión:** no se reutiliza ni se copia estructura del código de `bioinformaticaInta` en la parte
versionada del repositorio. El clon quedó en `work/C2/`, fuera de git. El linaje de
`tools/sifi21_port/` sigue siendo el fuente de `snowformatics`, documentado desde antes.
**Alternativas consideradas:** tomar de ahí los arreglos que ya tienen resueltos, que habría sido
más rápido.
**Criterio:** los dos repositorios del INTA son **GPL-3.0**, y el original declara licencias con
cláusula no comercial. Mantener el linaje limpio es lo que deja abierta la opción de publicar.
**Consecuencia:** la contradicción de licencia del original ahora tiene **tres declaraciones
distintas y ninguna resuelta** `[?]`: el artículo (página 9) dice CC BY-SA 4.0, el README del
repositorio oficial dice CC BY-NC-SA 2.0 Generic y la última página del manual dice CC BY-NC-SA.
Las dos últimas tienen cláusula NonCommercial, incompatible con la primera, y una licencia no
comercial con *share alike* tampoco es compatible con relicenciar un derivado bajo GPL-3.0. No es
asesoría legal: queda anotado por si alguna vez se publica algo. La afirmación previa del
repositorio —«SourceForge dice CC BY-NC 2.0»— no se pudo verificar, porque el dominio está
bloqueado, y además no coincide con lo que dice el README, que sí se verificó.


---

## D33 — Las bacterias salen del alcance del diseño por ARNi
**Fecha:** 2026-10-21
**Quién:** el equipo, al formalizar el Checkpoint 1 (sección 7 de `PLAN_DESARROLLO.md`).
**Decisión:** ningún diseño del proyecto apunta a los mollicutes del complejo patogénico
(*Candidatus* Phytoplasma asteris y *Spiroplasma kunkelii*). El alcance del diseño por ARNi queda
limitado al insecto vector y a los dos genes virales.
**Alternativas consideradas:** (a) mantener una rama exploratoria contra los mollicutes por si
apareciera un mecanismo alternativo; (b) reencuadrarla como control indirecto vía el vector, que es
lo que efectivamente quedó.
**Criterio:** el mecanismo de interferencia por ARN no existe en bacterias —*«de las bacterias
olvídense, porque son otros mecanismos»*, dicho por el investigador en el checkpoint `[E]`—, y eso
coincide con lo que R1 §4 y R6 ya habían medido por homología en los dos mollicutes: no se
recuperan los componentes de la maquinaria. Son dos vías independientes que dan lo mismo, así que
no es una corrección sino una confirmación. (a) se descartó porque no hay hipótesis de mecanismo
que explorar, y una rama sin mecanismo consume tiempo sin producir evidencia.
**Consecuencia:** la rama del complejo patogénico que el proyecto había considerado atacar por esa
vía se cae entera. Lo que queda de los patógenos en el entregable es el argumento de transmisión:
se los controla matando al vector antes de que transmita, no silenciándolos. El trabajo de R6 no se
descarta: pasa a ser el registro de por qué esa vía está cerrada, que es un descarte documentado y
vale como resultado.

---

## D34 — El objetivo del diseño es el insecto como vector, no el patógeno dentro de la planta
**Fecha:** 2026-10-21
**Quién:** el equipo, al formalizar el Checkpoint 1.
**Decisión:** el blanco del diseño es *Dalbulus maidis*. La estrategia de silenciar al patógeno
dentro de la planta queda registrada como legítima pero no es la que el proyecto desarrolla.
**Alternativas consideradas:** (a) atacar al patógeno dentro de la planta; (b) sostener las dos
estrategias en paralelo y rankearlas juntas.
**Criterio:** el investigador presentó las dos como legítimas y recomendó la del vector por directa
`[R]`. A eso se suma el argumento de la **ventana de latencia**: pasan unos 20 días entre que la
chicharrita se infecta y puede transmitir, que él confirmó, así que hay una ventana real para
matarla antes de que contagie. (b) se descartó porque comparar candidatos de las dos estrategias en
un mismo orden exigiría una equivalencia entre desenlaces que no tenemos —mortalidad del vector
contra carga del patógeno en planta—; donde las dos conviven, conviven como rankings separados con
el criterio de comparación declarado (D20).
**Consecuencia:** los dos genes virales siguen en el ranking porque son material de EPILAB que hay
que auditar, no porque el proyecto recomiende esa vía. La ventana de latencia pasa a ser un
argumento del entregable y no un dato de contexto: es lo que justifica que matar al vector sirva
aunque ya esté infectado.

---

## D35 — La ventana se fija en 21 y 22 nucleótidos por evidencia biológica, no por convención de la herramienta
**Fecha:** 2026-10-21
**Quién:** el equipo, al formalizar el Checkpoint 1.
**Decisión:** todo cálculo del proyecto usa ventanas de 21 y 22 nt, y el fundamento que se declara
es biológico y no heredado de si-Fi21.
**Alternativas consideradas:** (a) usar 21 nt solo, por ser el defecto de la herramienta; (b) barrer
largos menores (18, 19, 20 nt) como parámetro libre.
**Criterio:** 21-22 nt es el tamaño en que la maquinaria corta y el tamaño del fragmento que después
se aparea; por debajo de eso la molécula no funciona `[E]`. La regla de método que el investigador
dio y que el proyecto adopta es *«tenés que tener la evidencia biológica atrás de por qué elegís
21»*. (b) se midió igual, y el resultado sostiene la decisión en vez de contradecirla: por debajo de
18 nt las coincidencias son indistinguibles del azar una vez corregido por composición
(`research/ola3/C3_blast_ventana_azar/`), así que un largo menor no agrega señal, agrega ruido.
**Consecuencia:** 21 y 22 nt dejan de ser un parámetro y pasan a ser una decisión fundada que se
puede defender sin apelar a la herramienta. El costo es que todo resultado se reporta dos veces, a
21 y a 22, porque el conjunto de ventanas eficientes cambia casi entero entre los dos largos aunque
el conteo casi no cambie (C3, C7): las puntas del orden aguantan y el medio no. Y queda declarado
que la regla de nucleótidos terminales del port a 22 nt es una generalización nuestra y no una
regla publicada.

---

## D36 — El ejercicio sobre los cuatro candidatos es una auditoría, no la reproducción de un resultado validado
**Fecha:** 2026-10-21
**Quién:** el equipo, al formalizar el Checkpoint 1.
**Decisión:** el trabajo sobre los cuatro diseños de la planilla de EPILAB se encuadra y se escribe
como auditoría de una decisión vieja, no como intento de replicar un resultado.
**Alternativas consideradas:** (a) tratar la planilla como verdad de terreno y medir cuánto nos
acercamos a ella; (b) tratarla como un dato más entre varios candidatos.
**Criterio:** los cuatro diseños los hizo el propio investigador hace unos dos años, **nunca se
testearon** porque bajó la incidencia de la plaga, y no recuerda con certeza por qué eligió esas
regiones `[R]`. No hay resultado validado que replicar: hay una decisión vieja de la que ni el autor
está seguro. (a) se descartó porque tomar como referencia un número que nadie validó convierte
cualquier desvío nuestro en error cuando podría ser corrección. Y el criterio con el que se nos va a
evaluar es explícito: *«no porque tenga que ser cierto eso que decís, porque al final hay que
evaluarlo, sino el pensamiento que nos llevó a ustedes para decidir ese ranking»*.
**Consecuencia:** cambia qué significa que nos vaya bien. Un «la elección es mejorable, y acá está
por qué» vale tanto como un «la elección se justifica», y un «no se puede saber con los datos que
hay» bien fundamentado suma en vez de restar. La consecuencia de método es que cada número del
entregable viaja con el porqué de haberlo elegido. Es también lo que vuelve defendible que el equipo
no tenga laboratorio: auditar una decisión de diseño es exactamente lo que se puede hacer bien sin
uno.


---

## D37 — El mapeo por homología se cierra como mapa de límites, no como ruta de genes nuevos
**Fecha:** 2026-10-22
**Quién:** el equipo, tras la Fase 2 y C12.
**Decisión:** no se sigue desarrollando el mapeo por homología como fuente de genes blanco nuevos para *D. maidis*. Se conserva como (a) criterio para inferir qué hace un gen, con su tasa de acierto medida, y (b) mapa documentado de qué no se puede diseñar con datos públicos. El diseño sigue haciéndose sobre secuencias propias del vector.
**Alternativas consideradas:** (a) seguir con el paso que falta (diseño sobre el contig de *D. maidis*, tras la búsqueda inversa); (b) ampliar a más especies o más familias; (c) cerrar.
**Criterio:** la inferencia de función por homología funciona (concordancia de anotación entre cicadélidos 76–86 % según la identidad, C12 A; poliproteína del MRFV transferida a 11 de 11 marafivirus, C12 B). El diseño a partir de otra especie no: 2 de 11 familias pasan el criterio de nucleótido (Fase 2) y las ventanas de 21 nt compartidas con parientes virales son ≤ 0,66 % (C12 B). Esto coincide con C5 (0,7–11,1 %), así que la Fase 2 confirma y extiende, no descubre. Lo que falta no se resuelve con más cómputo sino con más secuencia de *D. maidis* y más aislados del MRFV. `[R]`
**Consecuencia:** quedan declarados como no hechos la búsqueda inversa desde *D. maidis*, el uso del genoma en el paso de nucleótido y el chequeo de ventanas contra *Apis mellifera*. Se retoman sólo si aparece anotación del genoma o un investigador los pide.

---

## D38 — El entregable presenta dos listas, una por mecanismo: se aplica D34 y no se reordena en una lista única
**Fecha:** 2026-10-22
**Quién:** el equipo, con la decisión del usuario sobre la opción A propuesta en la Fase 1 del plan del checkpoint 2.
**Decisión:** el ranking del entregable se presenta en dos listas. La lista del insecto (*Dalbulus maidis* como blanco) contiene `BicC_Dm`, `eth_Dm`, `bursA_Dm` y `ATPaseD_Dm`. La lista del virus dentro de la planta contiene `MP_MRFV` y `CP_MRFV`. Cada lista lleva su evidencia y su incertidumbre, y una frase de por qué no se comparan entre sí. Dentro de cada lista, un orden se reporta sólo si se sostiene en las escalas absoluta y min-max y a los dos largos (21 y 22 nt); lo que no se sostiene se dice «no se distinguen».
**Alternativas consideradas:** (a) una lista única con una columna cualitativa de «se entiende cómo llegaría el ARN» (opción B de la Fase 1), que exige un juicio nuestro sin medición; (b) dejar la lista única con una advertencia (opción C), que mantiene la tensión sin resolver y contradice D34.
**Criterio:** D34 ya había decidido que el blanco es el insecto y que, donde las dos estrategias conviven, lo hacen como rankings separados con el criterio declarado (D20). Una lista única con `MP_MRFV` primero es el artefacto que D20 describe. El orden dentro del grupo del insecto no es robusto: `eth_Dm` precede a `bursA_Dm` en escala absoluta a los dos largos, pero el par es inestable en min-max y no se toma como orden firme, y `bursA_Dm` frente a `ATPaseD_Dm` depende de si el método cuenta ventanas (cascada) o tasas. Ver `docs/plan_checkpoint2/salidas/F1_decision_ranking.md` §2.
**Consecuencia:** la Fase 5 reescribe `entregables/para-el-investigador.md` en dos listas. `MP_MRFV` deja de figurar como primero de un ranking general. El último puesto de `ATPaseD_Dm` se reporta con la salvedad del método. La comparación entre las dos listas se hace por criterio declarado, no por número.

**Enmienda (2026-10-22):** se corrige la lectura del par `eth_Dm`–`bursA_Dm`. El texto original decía que no se distinguían; ese enunciado era consecuencia de exigir que el orden se sostenga en las dos escalas, no un resultado de los datos. Con escala absoluta `eth_Dm` precede a `bursA_Dm` en 76,1 a 100 % de los sorteos (21 nt) y en 84,3 a 100 % (22 nt). Con min-max el par es inestable. La regla de esta decisión no cambia; el orden se reporta como no firme, con la escala absoluta a favor de `eth_Dm`. Fuente: `research/ola3/C7_ranking_v2/resultados/por_estrategia.json`.

---

## D39 — Se introduce el marcador [M] para resultados medidos por nosotros; [E] queda reservado a consenso en literatura revisada
**Fecha:** 2026-10-22
**Quién:** el equipo, con la decisión del usuario sobre la opción (i) propuesta en la Fase 1.
**Decisión:** `CLAUDE.md` incorpora `[M]` («medido por nosotros»): conteo, tasa, frecuencia o concordancia calculados por el equipo, reproducibles desde el repo, con script, entrada y salida con ruta. Si la entrada es un dato no publicado que no se versiona, se declara «con insumos locales». `[M]` rotula el número, y su lectura va en `[H]`. Un resultado computacional propio nunca es `[E]`. `00_meta/GLOSARIO.md` recibe la nueva definición. En las frases del entregable, «ventana eficiente» se reemplaza por «ventana que pasa el filtro de si-Fi21».
**Alternativas consideradas:** (ii) rotular todo lo propio como `[H]`, sin categoría nueva. Se descartó porque un conteo exacto quedaría con la misma etiqueta que una idea sin respaldo.
**Criterio:** la guía del checkpoint 2 dice que una coincidencia de secuencia, una puntuación o un resultado in silico es una hipótesis para validar, no una prueba directa de eficacia (`Guia_Checkpoint2_Estudiantes.pdf`, texto de la regla de trabajo). `CLAUDE.md` define `[E]` como consenso en literatura revisada por pares, así que usarlo junto a resultados propios contradice su propia definición.
**Consecuencia:** `CLAUDE.md` y `00_meta/GLOSARIO.md` cambian (sin commit). La regla de reemplazo para `entregables/para-el-investigador.md` (11 líneas con `[E]`) está definida en la salida de la Fase 1 y se aplica en la Fase 5. Hasta entonces, el entregable usa `[E]` donde debería usar `[M]`, y eso figura como pendiente.


---

## D40 — El diseño presenta matar y esterilizar como dos ejes separados, sin ordenarlos entre sí
**Fecha:** 2026-10-22
**Quién:** el equipo, por decisión del usuario en la Fase 3 del plan del checkpoint 2.
**Decisión:** el objetivo fenotípico se presenta como dos ejes con su evidencia, sin elegir uno. Eje letal: `eth` y `burs-α` (letalidad y falla de muda en *D. maidis* según Andrada *et al.* 2026, P3). Eje reproductivo: `BicC` (reducción de oviposición según el resumen de Dalaisón-Fuentes *et al.* 2022, P11). `ATPaseD` se registra como letal por ingesta, con control GFP (Jones *et al.* 2021, P8).
**Alternativas consideradas:** (a) matar como eje principal (la letalidad está publicada para dos genes); (b) esterilizar como eje principal (BicC es el único con una medición de reproducción); (c) dos ejes separados, elegido.
**Criterio:** ninguna fuente abierta mide letalidad y reproducción en el mismo gen de *D. maidis*. Para `BicC` el resumen no reporta letalidad, y para `eth` y `burs-α` no hay medición de descendencia (Andrada lo deja como trabajo futuro). Ordenar «matar» contra «esterilizar» exigiría una equivalencia que no tenemos, como en D20.
**Consecuencia:** el orden del ranking (D38) no cambia por este eje. La Fase 3 y la Fase 4 presentan el objetivo como límite declarado. Queda pendiente, para el investigador, cuál de los dos desenlaces le importa para la población en campo.

---

## D41 — Las 28 secuencias de Cedden se dejan publicadas, con la advertencia de la unión
**Fecha:** 2026-10-22
**Quién:** el equipo, por decisión del usuario en la Fase 5 del plan del checkpoint 2.
**Decisión:** la tabla `research/ola3/C9_sensibilidad_umbral/datos/cedden2025_28dsrna_con_secuencia.csv` se deja publicada tal como está. Son datos de un artículo con licencia CC BY (Cedden *et al.* 2025, PMC12039203), de *Tribolium castaneum*, y no tienen relación con las secuencias de EPILAB. No se toca el historial ni el remoto.
**Hecho que motivó la decisión:** el plan y el generador de estado decían que el CSV estaba «sin subir al remoto». No era así: ya está en `origin/main` desde el commit `6b8a800` (2026-10-21).
**Alternativas consideradas:** (a) dejarlo publicado y declararlo, elegida; (b) quitarlo del árbol con un commit nuevo, que lo deja en el historial y deja sin dato de entrada a la validación retrospectiva; (c) reescribir el historial, que es destructivo e irreversible para quien ya clonó el repositorio.
**Criterio:** los datos son públicos y con licencia abierta, y retirar algo ya publicado no lo borra de las copias existentes. La salvaguarda real es la advertencia de que la unión no tiene clave: los dos archivos adicionales de Cedden no comparten identificador, la unión es por orden dentro de cada gen y pasó 20 de 20 chequeos de consistencia, pero esos chequeos no prueban que el orden sea el mismo.
**Consecuencia:** el LEEME de `datos/` declara el estado de publicación; el estado deja de listarlo como pendiente. Los archivos adicionales originales (`MOESM1` y `MOESM2`) no están en disco, así que cualquier verificación de la unión contra el original requiere bajarlos de Europe PMC.

---

## D42 — La casilla del avance propio se abre con el veto y el movimiento de región, no con la separación de listas
**Fecha:** 2026-10-22
**Quién:** el equipo, por decisión del usuario al revisar el entregable del checkpoint 2.
**Decisión:** en `entregables/checkpoint2-una-pagina.md`, la casilla 4 («un avance propio») se reordena para abrir con la cadena port verificado → auditoría → veto de las dos regiones del insecto → movimiento de región, y cierra con la presentación en dos listas por mecanismo. La separación por mecanismo (D38) pasa de ser el protagonista a ser el marco en el que se presenta el resultado.
**Alternativas consideradas:** (a) dejar la casilla como estaba, con D38 adelante y el detalle de pares; (b) abrir con el port y la crítica de si-Fi21 como protagonista, dejando el ranking de apoyo; (c) la elegida.
**Criterio:** la casilla abría con la decisión de separar las listas y seguía con comparaciones de pares, que es lo más abstracto y lo más frágil de lo medido —el par `eth`/`burs-α` es inestable en min-max y no se reporta como orden firme—. El hallazgo concreto sobre el diseño real del laboratorio no figuraba: que las dos regiones que EPILAB eligió para los genes del insecto contienen ventanas de 21 nt idénticas a *Homalodisca vitripennis* y quedan vetadas, y que moviendo la región dentro del mismo gen `BicC_Dm` pasa de 20 a 36 ventanas que pasan el filtro y de 22 a 0 coincidencias, con lo que queda primero de la lista del insecto en las diez combinaciones de agregación a 21 nt. (b) se descartó porque el port es el medio que habilita la auditoría, no el resultado: presentado solo, no dice nada sobre los diseños de EPILAB. **Y la mitad del hallazgo que importa no depende del filtro de si-Fi21:** el veto es una coincidencia exacta de secuencia, de modo que sobrevive a que el valor predictivo del filtro sea el que es (casilla 6, validación no concluyente).
**Consecuencia:** la casilla 4 pasa de un párrafo a tres: el hallazgo, las dos salvedades (las coordenadas son una región candidata y no un sitio, porque en el barrido de umbrales el solapamiento con la región de defecto llega a cero; y el conteo de ventanas depende del filtro mientras que el veto no) y la presentación en dos listas. Las veinte cifras citadas se verificaron contra `research/ola3/C7_ranking_v2/resultados/ranking_v2.json` y `por_estrategia.json`. El pie de «dónde está cada cosa» suma el port y el REPORT de C9. D38 y D16 no cambian: esta decisión es de orden de presentación, no de método.

**Nota de aplicación (2026-10-22):** al escribir la casilla se citó primero 2121-2420, que es la región de C7, y se corrigió a **922-1221**, que es la vigente desde D25 por conservación (**corregido el 2026-10-25:** el «36 ventanas contra 35» ya no es argumento, por D65, y el «32 de 36 idénticas contra 22» tampoco, por D64; lo que sostiene la preferencia es el perfil de off-target y la conservación por fuente, con las 36 exactas en el genoma de Córdoba y en el del Reino Unido; fuentes `research/ola3/C8_conservacion/REPORT.md`, `research/ola4/M7_robustez_bicc/REPORT.md` §4 y `research/ola5/N10_conteo_historico_por_region/REPORT.md`). Con eso queda cerrado el punto 5 de «qué quedó sin hacer» de `docs/plan_checkpoint2/salidas/F5_cambios_aplicados.md`, que pedía decidir cuál es la recomendación vigente y dejarla igual en todos los documentos: no hacía falta una decisión nueva, porque D25 ya la había tomado y lo que faltaba era aplicarla. `entregables/para-el-investigador.md` ya decía 922-1221. Las cifras del barrido de pesos (diez de diez combinaciones) se midieron con 2121-2420; cambiar la región no mueve el orden, que se conserva en el 94,2 % de los sorteos (C8).

---

## D43 — Las quimeras no entran al ranking: se comparan contra sus propias partes y a igual largo
**Fecha:** 2026-10-22
**Quién:** el equipo, a partir de la pregunta del usuario sobre combinar de a dos las mejores regiones de los cuatro genes.
**Decisión:** las 12 quimeras ordenadas se miden y se reportan (línea C13), pero **no se agregan a las dos listas del entregable**. Lo que se reporta es cada quimera contra sus dos regiones recortadas, medidas con el mismo panel y en la misma tabla, y cualquier comparación entre quimeras y regiones sueltas se hace a igual largo total.
**Alternativas consideradas:** (a) agregarlas como candidatos más a la lista que corresponda; (b) armar una tercera lista de quimeras; (c) la elegida, medirlas y mantenerlas fuera de las listas.
**Criterio:** medido en C13, con las regiones vigentes y el motor de W7 sin modificar. En los dos ejes que son tasas, la quimera es el promedio ponderado de sus mitades más un empalme que aporta casi nada (4 ventanas eficientes de 240), así que **no puede superar a su mejor parte**: el máximo de eficacia de las doce es 0,1368 contra 0,1500 de `MP_MRFV` sola, y una queda por debajo de sus dos partes. En el eje que es conteo (`buenos_limpios`) gana cualquiera, pero eso mide el largo —de 180 a 380 ventanas— y no el diseño. Agregarlas a la lista no cambiaría el orden de los candidatos: le agregaría filas cuyo lugar lo decide el largo.
**Consecuencia:** el entregable no cambia. La razón para hacer una quimera deja de ser «sumar eficiencia» —medido que no ocurre— y pasa a ser cubrir dos blancos con una sola molécula, que es un beneficio que el ranking no mide y que en los dos antecedentes hemípteros publicados aparece como silenciamiento más temprano, no como más mortalidad. D31 sigue en pie y recibe una corrección: la banda de contexto no es de 59 nt sino **asimétrica, 72 nt corriente abajo y 59 corriente arriba**, porque el criterio mide la accesibilidad de un tramo de 8 nt al final de la ventana y no de los 21. Detalle en `research/ola3/C13_quimeras_region_recomendada/REPORT.md`.

---

## D44 — En una quimera que mezcla un gen viral con uno del insecto, el genoma del vector se trata por ventana
**Fecha:** 2026-10-22
**Quién:** el equipo, línea C13.
**Decisión:** para una quimera mixta, los aciertos contra el genoma de *Dalbulus maidis* **cuentan** como off-target en las ventanas heredadas de la mitad viral y **no cuentan** en las de la mitad del insecto, donde son on-target. Las 20 ventanas del empalme no pertenecen a ningún gen y **se cuentan**, que es la lectura conservadora. Los tres tratos (`viral`, `insecto` y `mixto`) se reportan juntos, porque la elección mueve el resultado.
**Alternativas consideradas:** (a) tratar toda la molécula como viral; (b) tratarla toda como del insecto; (c) la elegida, por ventana; (d) no evaluar las mixtas.
**Criterio:** D5 y D20 fijan el trato del genoma del vector según la estrategia del gen, y D34 y D38 separan el ranking en dos listas por ese mismo motivo. Una molécula que mezcla las dos estrategias no cae en ninguna regla, y las dos opciones uniformes son indefendibles en direcciones opuestas: con (a) la limpieza se desploma a ~0,66 y las ocho mixtas quedan vetadas por aciertos que son on-target; con (b) se borran aciertos de la mitad viral, que sí son off-target. La atribución por ventana es posible porque cada ventana tiene procedencia conocida, y el motor no hace falta tocarlo: lo que se construye distinto es la matriz de riesgo que se le pasa.
**Consecuencia:** con el trato `mixto`, **2 de las 8 quimeras mixtas quedan vetadas y el veto viene enteramente del empalme** (`BicC_Dm` + `MP_MRFV` por una ventana con 21/21 contra el genoma del vector, `CP_MRFV` + `ATPaseD_Dm` por dos), aunque ninguna de las cuatro regiones sueltas está vetada. Ese veto depende de la decisión sobre el empalme y se declara como parámetro, no como dato: con el trato `insecto` las dos quedarían sin veto.

---

## D45 — El umbral de 1,75 se retira como explicación del desajuste de conteos, y queda sólo como medición
**Fecha:** 2026-10-22
**Quién:** el orquestador, al integrar la respuesta del investigador del 2026-10-22.
**Decisión:** se retira de todo documento la afirmación de que subir el umbral de estabilidad de extremos a 1,75 explica la diferencia entre nuestros conteos y los de la planilla de EPILAB. El número se conserva como lo que es: la celda más cercana de un barrido. La explicación del desajuste pasa a buscarse en la **unidad de conteo y la referencia** (línea M1 de `docs/plan_ola4/PLAN_OLA4.md`).
**Alternativas consideradas:** (a) conservar la hipótesis del 1,75 como «compatible» porque la medición sigue siendo válida; (b) borrar el barrido entero del entregable; (c) la elegida, conservar la medición y retirar la lectura causal.
**Criterio:** el investigador declaró la configuración de sus corridas, `siFi21_8_1.0_0.1_1111`, y el umbral en **1,0** `[R]`. El nombre se decodifica contra `main.py:344-362` del fuente original, donde el modo diseño fija `xmer` = 8, extremos = 1, accesibilidad = 0,1 y las cuatro casillas en verdadero `[R]`: es el modo diseño con sus valores por defecto. Con 22.176 celdas barridas, que una de ellas acierte dos de cuatro números no es evidencia de haber encontrado la configuración ajena; es lo que se espera de un barrido grande. Mantener la lectura causal sería sostener una explicación que el autor del dato desmintió.
**Consecuencia:** hay que corregir la sección de la planilla de `entregables/critica-herramientas.md`, y conviene hacerlo con el resultado de M1 en mano para no reemplazar una explicación equivocada por un agujero. El barrido sigue publicado; lo que cambia es qué se afirma con él. Es, además, un caso de libro del riesgo de ajustar a cuatro números con muchos grados de libertad, y como tal entra en `CAMINOS_PROBADOS.md`.

---

## D46 — Los conteos de la planilla son «eficientes» del análisis de diseño, no «eficientes sin off-targets»
**Fecha:** 2026-10-22
**Quién:** el orquestador, al integrar la respuesta del investigador del 2026-10-22.
**Decisión:** se fija que los 114, 35, 199 y 33 de la planilla de EPILAB corresponden a siRNA predichos como eficientes en el análisis de diseño, y **no** a la columna que queda después de descartar off-targets. Toda comparación nuestra contra esos cuatro números se hace contra nuestra cifra de eficientes, nunca contra `buenos_limpios` ni contra ninguna cifra post-tamizaje.
**Alternativas consideradas:** (a) seguir reportando las dos lecturas en paralelo por si la respuesta era ambigua; (b) la elegida.
**Criterio:** el investigador lo dice sin ambigüedad —«no son conteos de eficientes después de eliminar todos los posibles off-targets; esa evaluación la realizamos por separado»— `[R]`. Eso descarta la hipótesis de que la planilla fuera la segunda columna de `sifi21INTA` (`getResultSummary`, `SifiPipeline.py:430-448`), que es la única que depende de la base y del blanco principal elegido a mano, y por lo tanto la única que habría sido irreproducible por construcción.
**Consecuencia:** el objetivo de reproducir sus cuatro números deja de depender de saber contra qué base tamizaron **para la columna**, y pasa a depender de contra qué base corrieron **el diseño**, que no es lo mismo y sigue sin saberse. Es el pedido 1 del lunes.

---

## D47 — La exposición ecológica y la señal de conservación son dos ejes, y no se combinan en el motor
**Fecha:** 2026-10-22
**Quién:** el orquestador, sobre la recomendación explícita del investigador del 2026-10-22.
**Decisión:** el vector de pesos del panel no objetivo se parte en dos vectores con nombres distintos y sin ninguna operación que los mezcle: `w_exposicion`, la probabilidad de contacto real con la formulación en la Argentina, y `s_conservacion`, la informatividad filogenética sobre cuán conservada está una región entre organismos emparentados. Cada región reporta **dos números**, y el código no los pondera: la ponderación es una decisión declarada del equipo o del laboratorio, fuera del motor. *Homalodisca vitripennis* queda con exposición cercana a cero y conservación alta.
**Alternativas consideradas:** (a) dejar el peso único de D18 y bajar el de *H. vitripennis*, que confunde las dos funciones en un solo número más chico; (b) sacar a *H. vitripennis* del panel, que es lo que el investigador pide explícitamente no hacer; (c) la elegida.
**Criterio:** el investigador: «mantendría esa información, pero separaría el riesgo de exposición ecológica de la señal de conservación de secuencia. No necesariamente deberían tener el mismo peso en la decisión final» `[R]`. Y es correcto por estructura: las dos funciones tienen signo opuesto. Que una región esté conservada en un cicadélido emparentado es **información útil** sobre que la región es funcional y poco variable; que un organismo esté expuesto es **riesgo**. El peso 0,60 de D18 estaba haciendo las dos cosas a la vez, y por eso no podía estar bien para ninguna.
**Consecuencia:** hay que medirla antes de aplicarla, porque **nos quita una conclusión**. El desempate del tercer puesto entre `ATPaseD_Dm` y `CP_MRFV` se apoya en el veto de `ATPaseD_Dm` por tres coincidencias perfectas con *H. vitripennis* en 392-394; si ese organismo deja de pesar como exposición, el veto se debilita y el empate vuelve, que era un empate invertido en el 47,4 % y el 48,9 % de la grilla `[M]` (`research/ola3/C9_sensibilidad_umbral/REPORT.md`, T1 bis). La implementación es la línea M5 y **no se aplica a ningún entregable sin confirmación del usuario**. Riesgo declarado: *H. vitripennis* es plaga cuarentenaria, así que darle exposición cero es correcto hoy y es una apuesta sobre que siga ausente `[H]`.

---

## D48 — La coincidencia perfecta de 21 nt es una alerta que obliga a justificar, no un veto automático
**Fecha:** 2026-10-22
**Quién:** el orquestador, sobre la corrección explícita del investigador del 2026-10-22.
**Decisión:** se reemplaza la compuerta booleana del veto ecológico por una tabla de alertas. Cada coincidencia perfecta de 21 nt con una referencia del panel genera una fila con cuatro campos obligatorios —organismo, posibilidad de exposición, gen involucrado y evidencia biológica disponible— y la región no se descarta por tenerla: se acepta o se descarta con una justificación escrita que cita la fila. Una fila sin los cuatro campos es un error de validación. Se mantiene la posición conservadora de D17, que el investigador confirma, y los dos umbrales de D28.
**Alternativas consideradas:** (a) conservar el veto automático, que es lo que estaba; (b) pasar a la regla mecanicista y contar como riesgo sólo las ventanas además eficientes, que es lo que D17 ya había descartado y lo que el investigador también descarta; (c) la elegida.
**Criterio:** el investigador confirma el criterio y corrige la consecuencia. Confirma: evalúa la identidad de los off-targets «independientemente de que esas ventanas sean clasificadas como siRNAs eficientes», porque «una predicción negativa de eficiencia no garantiza que un siRNA carezca de actividad biológica» `[R]`, que es palabra por palabra el argumento de D17. Corrige: «no trataría todas las coincidencias de 21 nt como equivalentes ni las convertiría automáticamente en un veto ecológico universal. Sí las conservaría como alertas fuertes que deben ser consideradas y justificadas» `[R]`. El cambio no es de severidad sino de carga de la prueba: antes el motor decidía solo, ahora obliga a argumentar.
**Consecuencia:** regiones hoy vetadas vuelven a estar sobre la mesa con su justificación, empezando por la región más conservada de `ATPaseD_Dm`, 137-436, que D25 había descartado por veto. La implementación es la línea M6 y, como D47, **no se aplica sin confirmación del usuario**. Lo que se pierde es la comodidad de una compuerta automática: de acá en adelante cada alerta exige un párrafo, y un párrafo puede estar mal escrito de un modo en que un booleano no puede.

---

## D49 — Se conservan los dos modos del port y se agrega una tercera vía, de términos continuos sin corte
**Fecha:** 2026-10-22
**Quién:** el orquestador, sobre la sugerencia del investigador del 2026-10-22.
**Decisión:** los modos `fiel` y `corregido` se conservan los dos, en paralelo y sin declarar superior a ninguno, hasta que haya evidencia que los distinga. Se agrega una tercera salida, `--features`, que emite por ventana los términos sin ningún corte binario: ΔG de los dos extremos, su brecha, la probabilidad de apertura del sitio blanco, los dos nucleótidos de la regla terminal y la rama que les corresponde. Esa tabla no es un modelo y se declara como tal: es el insumo para evaluar cómo contribuye cada término cuando existan etiquetas.
**Alternativas consideradas:** (a) declarar el modo `corregido` como el correcto, que es lo que el tono de `CAMBIOS.md` C1 insinuaba; (b) volver al `fiel` por fidelidad al original; (c) la elegida.
**Criterio:** el investigador acepta la crítica y frena la conclusión: «me parece razonable cuestionar esa excepción», pero «tampoco asumiría todavía que esa modificación mejora la predicción de eficiencia. Sería interesante conservar ambos modelos» `[R]`. Y tiene el dato a favor: la validación retrospectiva preregistrada contra *Tribolium castaneum* da ρ = +0,142 [-0,247, +0,492] en modo fiel y +0,024 [-0,356, +0,397] en corregido, n = 29 `[M]`, o sea que con los datos abiertos que existen **los dos modelos no se distinguen**. Afirmar que el corregido predice mejor sería exactamente el error que D45 acaba de corregir en otro terreno. La tercera vía es suya y completa el ADR D26, que ya obligaba a publicar los términos continuos y estaba implementado a medias: faltaban justamente los nucleótidos terminales.
**Consecuencia:** el port gana dos columnas y una bandera (línea M3), y el proyecto gana una pregunta contestable: cuántas etiquetas hacen falta para distinguir los dos modelos, y cuál es el ensayo mínimo que lo haría. Eso es la línea M4, y tiene una ventaja de diseño que no es menor: los dos modos difieren en un conjunto identificable y ya contado —19, 7, 50 y 8 ventanas en los cuatro genes— y **ninguna ventana va en sentido contrario** `[M]`, así que el ensayo que discrimina mide discordantes contra concordantes y no siRNA al azar.

---

## D50 — El borrador de respuesta se envía antes del lunes, y lo revisa el equipo antes de mandarlo
**Fecha:** 2026-10-22
**Quién:** el usuario, al cerrar la única casilla abierta de la línea M0.
**Decisión:** el borrador de `entregables/respuesta-al-mentor.md` **se envía antes de la reunión del lunes 26**. El equipo lo evalúa cuando esté listo y lo manda: el envío es una acción del equipo hacia afuera y no la ejecuta el agente. Fallback declarado por el usuario: si no se llega a revisarlo a tiempo, no se manda nada, los tres contenidos se dicen en persona el lunes y el usuario avisa.
**Alternativas consideradas:** (a) no mandar nada y llevar todo a la reunión; (b) mandar sólo el pedido del archivo, que es la opción que el propio borrador proponía como mínimo; (c) la elegida, mandar el borrador completo con revisión previa.
**Criterio:** de las tres cosas que hace el borrador, la única con costo de demora es el pedido de la salida por ventana de la corrida `siFi21_8_1.0_0.1_1111`, porque necesita que el investigador busque un archivo antes del lunes; es el pedido 1 de la lista y lo que cierra M1 y M2 de una vez. Las dos respuestas que él pidió y el párrafo del hallazgo no pierden nada por decirse en persona, pero tampoco cuestan por escrito, y llegan antes. La revisión del equipo antes de mandar es la condición que el usuario puso y es la que corresponde: el texto afirma cosas sobre su código y sobre nuestro port, y una afirmación mal calibrada en un mensaje no se puede retirar.
**Consecuencia:** el estado del borrador pasa de «BORRADOR, SIN ENVIAR» a «aprobado para envío, pendiente de revisión del equipo», y la casilla abierta de M0 queda cerrada. Esta decisión **no toca D47, D48 ni D49**: lo que esos tres esperan no es el envío sino la confirmación para aplicar los cambios a un entregable, que son las líneas M5 y M6, y sigue abierta. Cuando el mensaje se mande, hay que registrar fecha y texto enviado en `00_meta/PREGUNTAS_ABIERTAS.md`, donde ya está abierto el mismo pendiente del correo anterior.

---

## D51 — La regla de conteo del original se implementa como script propio, sin Bowtie obligatorio y sin elegir fila
**Fecha:** 2026-10-22
**Quién:** el orquestador, al implementar la línea M1 de la ola 4.
**Decisión:** el conteo por acierto del si-Fi21 original se implementa en un script del repositorio (`research/ola4/M1_conteo_y_referencia/scripts/conteo_por_acierto.py`) con tres propiedades decididas acá: **(1) sólo biblioteca estándar**, sin ViennaRNA, sin Biopython y sin `pyahocorasick`; **(2) la enumeración de aciertos no depende de Bowtie** —entra una salida de Bowtie en formato nativo o SAM, o se enumeran localmente las coincidencias exactas, que es lo mismo que reporta `bowtie -a -v 0`—; y **(3) el script no elige qué fila de la tabla leyó el laboratorio**: reporta tres agregaciones en paralelo (`suma_filas`, `fila_max`, `fila_homonima`) con su distancia L1 al vector declarado, y ninguna se declara la verdadera.
**Alternativas consideradas:** (a) reimplementar la regla dentro de `sifi21INTA` o del original, que es donde vive el código leído; (b) exigir Bowtie y el corpus para poder correr cualquier parte de la línea; (c) elegir una agregación —la fila mayor, que es el orden en que el original presenta la lista— y reportar un solo número por celda; (d) la elegida.
**Criterio:** las tres propiedades salen del mismo hecho práctico: la máquina que ejecutó M1 no tiene `work/`, ni Bowtie, ni ViennaRNA, ni si-Fi21 instalado, y la que corrió la ola 3 es otra (`research/ola3/C2_codigo_apolo_inta/corridas/README.md`). Con esas tres restricciones la regla se puede escribir y **verificar** en cualquier máquina del equipo, y lo único que hay que pedir prestado es el TSV por ventana. Sobre (c): con una base de 71 registros la tabla del original tiene hasta 71 filas y no sabemos cuál leyeron, así que fijar una agregación es elegir un supuesto no declarado justo en la variable que la línea vino a medir. Las tres en paralelo hacen que el resultado sea interpretable incluso si la hipótesis falla, que es lo que el plan pedía explícitamente.
**Consecuencia:** la regla queda verificada con 44 pruebas sobre insumos sintéticos, y los tres casos que la definen —la ventana eficiente que no pega, la que pega sólo en la hebra menos y la que pega dos veces— quedan cubiertos `[M]`. Quince de esas pruebas salieron de revisar el script y cubren formas de fallar en silencio, que son las que importan cuando el número sale impreso: posición repetida en el TSV, ventana sin secuencia, código IUPAC ambiguo, N en la ventana o en la referencia —comparar `N == N` inventaba aciertos que Bowtie no reporta—, nombre de lectura con dos grupos de dígitos y dos referencias que nombran al mismo gen. Las seis abortan o devuelven `None` en lugar de un número plausible y equivocado. Dos consecuencias que no estaban previstas. Primera: **el criterio de terminado del plan era falso como estaba escrito**. Pedía que, contra el gen mismo, el conteo por ventana y el conteo por acierto coincidan, y eso sólo vale si no hay 21-meros repetidos; en `BicC_Dm` hay cuatro aciertos de más sobre 2.500 ventanas `[M]`. El invariante correcto, que el script verifica con `--exigir-identidad`, es que ninguna ventana eficiente quede sin acierto en la hebra `+`. Segunda: **la matriz de bases sigue sin correr**, y se declara como pendiente con los comandos exactos, no como resultado nulo. Lo que sí se pudo cerrar sin insumos nuevos está en la sección 5 del REPORT y mueve el pedido del lunes de «contra qué base corrieron» a «contra qué registro», con número de acceso.

---

## D52 — La matriz de bases explica un gen de cuatro, y eso se reporta como parcial y no como hallazgo
**Fecha:** 2026-10-23
**Quién:** el orquestador, al correr la mitad que faltaba de la línea M1 de la ola 4.
**Decisión:** la matriz de bases de M1 se corre completa —once bases, treinta y ocho celdas, el control de orientación incluido— y el resultado se reporta como **parcial**: la regla del conteo por acierto contra el transcriptoma público de *Dalbulus maidis* explica `BicC_Dm` con un error de uno (200 contra 199 declarados) y **no explica** `MP_MRFV`, `CP_MRFV` ni `ATPaseD_Dm` `[M]`. No se declara explicación cerrada, no se declara nulo, y **no se presenta como resultado la combinación mejor por gen**, que daría una distancia L1 de 25 contra los 44 de la celda de verificación pero mezcla dos motores distintos entre genes y por lo tanto no corresponde a ninguna corrida.
**Alternativas consideradas:** (a) titular que el conteo por acierto explica el desajuste, apoyándose en la celda de `BicC_Dm`, que es la que cualquiera miraría primero; (b) titular que la hipótesis se cae, apoyándose en que tres de cuatro genes no cierran; (c) reportar la combinación mejor por gen como la configuración encontrada; (d) la elegida, que dice cuál gen cierra, cuáles no, y por qué cada uno.
**Criterio:** los cuatro genes se comportan distinto y promediarlos en un veredicto pierde justo lo que se midió. `BicC_Dm` pierde doce ventanas eficientes contra el contig público y la fila cae de 212 a 200. `ATPaseD_Dm` no pierde ninguna contra ese mismo transcriptoma —la fila da 42, no 33— y contra el genoma cae a **0**, porque el gen está anotado en la hebra reversa y la regla del original sólo evalúa la hebra `+`: cuarenta de sus cuarenta y dos ventanas eficientes pegan sólo en `-` `[M]`. `MP_MRFV` es casi una función escalón: contra los sesenta y cinco registros públicos de MRFV las filas posibles son 133, 133 y 30, y ninguna es 114 `[M]`. Y `CP_MRFV` es estructuralmente inalcanzable por esta vía: su declarado, 35, está **por encima** de nuestras 32 ventanas eficientes, y la regla sólo puede superar el conteo por ventana si alguna ventana eficiente pega dos veces en la misma referencia, lo que no ocurre en ninguna de las sesenta y cinco `[M]`.
**Consecuencia:** tres cosas quedan cerradas y una se abre. Cerradas: el criterio de terminado 1 se cumple —contra el gen mismo (a) y (b) dan 133, 32, 212 y 42 con el invariante `--exigir-identidad` en verde `[M]`—; la orientación se descarta con medición y no con argumento, L1 190 contra 44; y la unidad de los dos campos de `04_resumen_base_datos.json`, que estaba como `[?]` esperando un driver sin versionar, se resuelve corriendo Bowtie una vez: 2.504 alineamientos contra 2.500 nombres de lectura distintos, así que `hits_bowtie` cuenta alineamientos y `hits_blanco_principal` cuenta ventanas `[M]`. Se abre el eje del motor de accesibilidad, que el plan condicionaba a que la referencia no cerrara: el cruce de los dos ejes —que nunca se había hecho, porque la ola 3 barrió el motor con una sola base y M1 barrió la base con un solo motor— muestra que la versión del motor mueve los conteos en **direcciones distintas según el gen**, así que los puntos intermedios 2.4.x y 2.6.x tienen ahora una pregunta concreta que contestar. Y el pedido del lunes gana una tercera pieza con una predicción verificable: si para los genes del insecto corrieron contra el genoma y no contra un transcriptoma, el conteo de `ATPaseD_Dm` que sale de la herramienta es 0 y el 33 declarado no puede venir de ahí.

---

## D53 — El ensayo discriminante entra al entregable como la casilla de validacion, y el analisis de la tercera via queda preregistrado sin ejecutar
**Fecha:** 2026-10-23
**Quién:** Luca, consultado al cerrar la línea M4 de la ola 4; el orquestador implementa.
**Decisión:** el diseño de ensayo prospectivo de la sección 4 de `research/ola4/M4_evidencia_y_potencia/REPORT.md` —siRNA discordantes entre modos contra concordantes eficientes, con un brazo de concordantes rechazados como control de validez interna y un control negativo no dirigido, sobre un gen, con el silenciamiento del transcrito como variable de respuesta y **32 siRNA por brazo**— **entra al entregable del checkpoint 2 como su casilla de validación**, declarando que el equipo lo propone y no lo corre. En paralelo, el plan de análisis de la tercera vía de M3 queda **preregistrado y sin ejecutar** en `research/ola4/M4_evidencia_y_potencia/PREREGISTRO_tercera_via.md`, con condición de disparo explícita: no se ajusta nada con menos de 100 etiquetas y 3 genes blanco.
**Alternativas consideradas:** (a) dejar el diseño como anexo interno y llenar la casilla de validación con la validación retrospectiva de C9, que es no concluyente; (b) no proponer validación experimental; (c) ajustar ya el modelo continuo sobre las 29 etiquetas de Cedden para tener «la tercera vía» mostrable el lunes; (d) la elegida.
**Criterio:** sobre (a), presentar como validación un resultado que su propio pre-registro declara no concluyente sería usarlo para lo contrario de lo que mide. Sobre (c), con 29 etiquetas y seis términos el ajuste describe el ruido de un solo trabajo, y encima M4 midió que ese conjunto **no puede** distinguir ni dos criterios que difieren en una rama: el modelo saldría y no significaría nada. Sobre (d): el ensayo es el único diseño que discrimina los dos modelos, su tamaño de muestra está calculado por remuestreo y por la cuenta de equivalencia, y su repertorio de siRNA discordantes ya está contado (84 ventanas, 50 en `BicC_Dm`, C1 de `CAMBIOS.md`), así que es la casilla más fuerte que el entregable puede tener sin laboratorio propio.
**Consecuencia:** el entregable gana una casilla de validación con números y resultado falsador, y queda obligado a declarar en el mismo lugar que no lo corremos nosotros. El pre-registro de la tercera vía cierra el pedido del investigador sobre los términos continuos sin fabricar un modelo: la tabla existe (M3), el plan de análisis existe y está congelado, y falta el dato. Dos hechos nuevos quedan disponibles para la reunión: con los 29 siRNA de Cedden la comparación entre modos **no podía salir distinta** —un solo siRNA discordante, p exacto 1,00 por enumeración completa `[M]`—, y replicando ese diseño harían falta **2.784** siRNA con eficacia medida para distinguirlos con potencia 0,80 `[M]`. El 232 que una primera corrida dio como respuesta es sólo un piso: sale de remuestrear copias del único discordante observado, lo que deja a esa clase con varianza cero y sobreestima la potencia doce veces.

---

## D54 — La tabla de términos publica las categorías de la regla terminal, no los nucleótidos, y la tabla por ventana no se versiona
**Fecha:** 2026-10-23
**Quién:** el equipo, línea M3 de la ola 4 (issue #7), a partir de una medición de la línea M9.
**Decisión:** el TSV por ventana del port suma tres columnas para la regla terminal —`nt19_at`, `nt2_gc` y `rama_terminal` (1 a 4)— y **no** las letras `nt19` y `nt2` que el issue pedía. Además, la columna `seq` deja de emitirse por defecto y queda detrás de `--con-seq`. La tabla de `--features` por ventana **no se versiona**: se versiona el resumen agregado por gen y por rama, más el comando para regenerarla.
**Hecho que motivó la decisión:** el issue #7 afirmaba que `nt19`, `nt2` y `rama_terminal` «son dos letras y un entero: no reconstruyen secuencia, así que no chocan con la regla de confidencialidad», y pedía que M9 lo verificara. M9 lo verificó y es falso: como las ventanas se solapan de a 1 nt, la columna con la letra de una posición fija, concatenada en orden, es una subcadena literal del gen. Sobre un gen sintético de 500 nt y 480 ventanas, `nt19` y `nt2` juntas reconstruyen 497 de 500 nt, el 99,4 %, y **sin producir ninguna racha de 21 nt** que un escáner por rachas pueda ver `[M]`.
**Alternativas consideradas:** (a) emitir las letras como pedía el issue y confiar en que el repositorio es privado; (b) emitir la tabla sólo sobre ventanas no consecutivas, que rompe la cadena pero tira la mitad de las filas y cambia la unidad de análisis; (c) no emitir nada de la regla terminal, que deja a M4 sin la variable que Diego quiere ver como independiente; (d) la elegida, emitir las categorías que la regla efectivamente usa.
**Criterio:** la regla terminal no mira la letra, mira si `nt19` es A/T y si `nt2` es G/C (`sifi_core.py:_terminal_rule`, que reproduce `sifi_pipeline.py:525-550`). Las categorías conservan por lo tanto **todo** el poder predictivo de la regla y bajan de dos bits por posición a uno, con lo que no permiten escribir la secuencia. Aun así un bit por posición sobre ventanas consecutivas sigue siendo un perfil del gen, y de ahí que la tabla por ventana no se versione: es la misma política que ya rige para `seq`.
**Consecuencia:** la tabla corre en los cuatro genes y en los dos modos, y con las ramas numeradas se puede medir cuánto pesa el atajo que Diego confirmó: entre el 54,3 % y el 64,1 % de las ventanas que el original llama eficientes salen de la rama 2, la que saltea el veredicto termodinámico `[M]`. El control que lo cierra es que toda la diferencia entre los dos modos está en esa rama —cae 19, 9, 52 y 6, exactamente la caída de los totales—, mientras que las ramas 1 y 3 no se mueven ni una ventana y la 4 da cero eficientes en los dos modos `[M]`. Un consumidor dependía de la columna `seq` y quedó arreglado en la misma pasada: `research/ola4/M1_conteo_y_referencia/scripts/correr_matriz.py` ahora pasa `--con-seq`, y su salida vive bajo `work/`, que no se versiona; sin eso `conteo_por_acierto.py` se habría quedado sin consultas en silencio, porque lee la columna con `fila.get("seq") or ""`. Ningún veredicto se movió: las 4.722 ventanas de los cuatro genes en los dos modos reproducen el ancla de C9 con cero discrepancias `[M]`. **No se ajusta ningún modelo acá**: con 29 etiquetas y un ρ de +0,142 con IC95 [−0,247, +0,492] no se ajustan seis variables, y el plan de análisis se preregistra en M4.

---

## D55 — La interfaz del port es una herramienta para el investigador, no el artefacto con el que competimos
**Fecha:** 2026-10-23
**Quién:** el equipo, al abrir la línea de la interfaz del port (`sifi_plus/`).
**Decisión:** se construye una interfaz para el port de si-Fi21 y se la trata explícitamente como **entregable para el investigador que ya usa si-Fi y nos pidió conocer el port**, no como el artefacto de la competencia. El artefacto con el que competimos sigue siendo la ficha de decisión por candidato.
**Hecho que motivó la decisión:** `CAMINOS_PROBADOS.md:203` ya descartó «construir un tablero de exploración como artefacto principal», porque el organizador dijo que un equipo no debería ganar por tener la interfaz más vistosa. Sin esta distinción escrita, la línea nueva parece una reapertura de un camino descartado.
**Alternativas consideradas:** (a) no construirla y entregar sólo el CLI, como se prometió; (b) construirla y presentarla como el entregable principal; (c) la elegida, construirla y acotar por escrito para qué es.
**Criterio:** sobre (a), el port se le prometió a alguien que hoy usa un programa que se abre con doble clic; entregarle una herramienta que exige escribir comandos y leer TSV convierte una mejora real en una que no va a usar, y el argumento de paridad se pierde. Sobre (b), el descarte del tablero sigue en pie y el criterio del organizador no cambió. Lo que hace defendible a (c) es que el valor de esta herramienta no es el CSS: es que reproduce los cuatro conteos del programa original y expone los dos modos con sus números, que es auditoría, no presentación.
**Consecuencia:** el `LEEME.md` de la carpeta abre diciendo qué es y qué no es, y la demo del lunes se presenta como «tu herramienta, sin sus defectos operativos», no como un producto. La carpeta vive en la raíz del repositorio y no en `tools/`, porque es un entregable y no una utilidad interna, y la unidad que se comparte es `sifi_plus/` más `tools/sifi21_port/`. El nombre público y la licencia quedan en suspenso hasta que se resuelva D32: el artículo de si-Fi declara CC BY-SA 4.0 y SourceForge declara CC BY-NC 2.0 `[?]`, y un trabajo derivado no puede adjudicar eso por su cuenta.

---

## D56 — El servidor es de biblioteca estándar, está atado a 127.0.0.1, y nada de lo que escribe cae dentro de la carpeta
**Fecha:** 2026-10-23
**Quién:** el equipo, línea de la interfaz del port.
**Decisión:** la interfaz es un `ThreadingHTTPServer` de la biblioteca estándar atado a `127.0.0.1`, sin ninguna dependencia nueva: `tools/sifi21_port/requirements.txt` se queda en sus cuatro líneas. Todo lo que el programa escribe —tablas, FASTA de siRNA, rangos guardados, temporales del tamizaje— va a `work/sifi_plus/`, que está fuera del control de versiones.
**Alternativas consideradas:** (a) Streamlit o Dash, que dan una interfaz utilizable en mucho menos código; (b) FastAPI con uvicorn; (c) una ventana de escritorio en Tkinter o Qt, que se parece más al original; (d) la elegida.
**Criterio:** sobre (a) y (b), agregar un servidor web de terceros a una herramienta que procesa secuencias no publicadas mete una pila que no auditamos entre el dato y el disco, y obliga al investigador a resolver una instalación más. Sobre (c), los gráficos interactivos y las tablas ordenables cuestan mucho más código en Qt, y empaquetar un `.exe` de Windows es una tarea aparte que no entra antes del lunes. Lo decisivo de (d) es la regla de confidencialidad de `CLAUDE.md`: atado a `127.0.0.1` el socket **no escucha en ninguna interfaz de red**, así que «ninguna secuencia sale de la máquina» deja de ser una promesa en un documento y pasa a ser una propiedad de la estructura. Que las salidas caigan fuera de la carpeta tiene el mismo carácter: la entrega no depende de revisar archivo por archivo, porque la carpeta nunca tuvo adentro nada derivado de las secuencias.
**Consecuencia:** la carpeta se puede compartir sin auditarla cada vez. Medido sobre `sifi_plus/` completo con la pasada específica de `sin_secuencias.py` contra la planilla del EPILAB: **cero archivos con secuencias de EPILAB** `[M]`. El dato de ejemplo que viaja con la carpeta es `NM_001111367.2`, el ARNm de la ferredoxina-6 de *Zea mays*, elegido en reemplazo del genoma del MRFV porque `NC_002786.2` cubre el 90,5 % de `MP_MRFV` y el 96,5 % de `CP_MRFV` (M9 §3.2): es público y no es una fuga, pero no corresponde mandárselo de vuelta al investigador adentro de nuestra herramienta. Las dos salidas que sí llevan secuencia —el FASTA de siRNA y el TSV con `--con-seq`— se escriben con un aviso adentro del archivo.

---

## D57 — El CLI expone los ocho parámetros del panel del original, sin mover ningún valor por defecto
**Fecha:** 2026-10-23
**Quién:** el equipo, línea de la interfaz del port.
**Decisión:** `run_sifi.py` suma como banderas los ocho parámetros que el panel de si-Fi21 expone y que hasta ahora sólo llegaban por argumentos de palabra clave de `SifiEngine`: `--sirna-size`, `--ventana-acc`, `--umbral-extremos`, `--umbral-acc` y las cuatro casillas como `--sin-hebra`, `--sin-extremos`, `--sin-acc` y `--sin-terminal`. Ningún valor por defecto cambia.
**Alternativas consideradas:** (a) dejarlos accesibles sólo desde Python, como estaban; (b) exponerlos y aprovechar para revisar algún default; (c) la elegida.
**Criterio:** sobre (a), el panel del original los expone, así que un port que no los acepta no es un superconjunto de la herramienta que dice reemplazar, y cualquier barrido tiene que escribir Python. Sobre (b), los nombres de los TSV ya publicados y las ocho anclas de conteo dependen de esos valores: moverlos y exponerlos en la misma pasada haría imposible atribuir una diferencia.
**Consecuencia:** una corrida con el criterio cambiado ya no puede pisar el TSV de la corrida por defecto, porque el nombre del archivo gana un sufijo con el criterio, con el mismo orden de campos que la cadena `siFi21_8_1.0_0.1_1111` con la que el investigador declaró la suya (D45). El `resumen.json` ahora incluye el criterio completo: un conteo sin los umbrales con los que se calculó no se puede reproducir ni comparar. Verificado que los valores por defecto no se movieron: `MP_MRFV` en modo fiel con RNAplfold 2.1.5 sigue dando 133, y las cinco suites del repositorio siguen pasando `[M]`.

---

## D58 — Un contrato de datos y dos dibujantes, y el eje de posición es el del gen
**Fecha:** 2026-10-23
**Quién:** el equipo, línea de la interfaz del port.
**Decisión:** `sifi_plus/perfil.py` calcula los datos del gráfico una sola vez y los emite como JSON; el dibujo interactivo (`estatico/app.js`) y el informe estático (`tools/sifi21_port/informe_html.py`, que no se toca) son dos consumidores del mismo contrato. El gráfico son **dos paneles que comparten el eje de posición**, no uno con dos escalas.
**Alternativas consideradas:** (a) un solo panel con las tres curvas y dos ejes verticales; (b) reescribir `informe_html.py` para que dibuje desde el navegador y tener un solo dibujante; (c) que la interfaz dibuje y el informe estático se genere llamando a `informe_html.svg()`; (d) la elegida.
**Criterio:** sobre (a), las curvas no comparten escala —el solapamiento no puede pasar del tamaño de la ventana y la densidad por región llega a decenas— y un gráfico de doble escala vertical es el error de visualización más común; dos paneles con un eje horizontal compartido dicen lo mismo sin mentir sobre la comparabilidad. Sobre (b), `informe_html.py` está verificado tramo por tramo contra la pantalla del programa original y tocarlo antes del lunes pone en riesgo lo único que sostiene el argumento. Sobre (c), su `svg()` tiene las etiquetas de banda del informe de W5 («EPILAB», «más densa») cableadas, que en una herramienta general son incorrectas. Lo que resuelve (d) es que la fuente única no es el código de dibujo sino el **modelo de datos**: hay dos renderizadores y un solo contrato, y un test compara los dos algoritmos de densidad array por array.
**Consecuencia:** el dominio del eje horizontal es la posición en el gen (1..largo), igual que el original («mRNA sequence position»), y no el número de ventana. La distinción no es cosmética: hay `largo` posiciones y sólo `largo − size + 1` ventanas, y mezclar las dos escalas corría la curva de solapamiento 20 posiciones hacia la derecha, que fue un error real detectado al mirar la página `[M]`. Mirarla también encontró un segundo error que ningún test numérico podía ver: el arrastre para marcar un rango redibujaba el SVG entero en cada movimiento del mouse, lo que reemplazaba el elemento y dejaba el manejador en curso sobre un nodo desprendido —ahí `getBoundingClientRect` devuelve cero y el rango saltaba al final del gen—. Esto reabre y cierra en parte el pendiente de `CAMINOS_PROBADOS.md:542`: los gráficos del repositorio «no se miraron» y ahora uno sí, en Chrome.

---

## D59 — Las ventanas de baja complejidad se marcan y se descuentan aparte, no se descartan
**Fecha:** 2026-10-23
**Quién:** el equipo, línea de la interfaz del port, a partir de una medición hecha probando la vista de off-target.
**Decisión:** el tamizaje de off-targets marca las ventanas de baja complejidad y reporta **cada conteo en dos cifras**: el total y cuánto de ese total es baja complejidad. No se descartan.
**Hecho que motivó la decisión:** corriendo el genoma público del *Maize rayado fino virus* (`NC_002786.2`) contra tres transcriptomas no objetivo aparecieron 9, 11 y 13 ventanas con coincidencia perfecta de 21/21 nt en *Harmonia axyridis*, *Apis mellifera* y *Zea mays* respectivamente. Nueve coincidencias exactas de un 21-mero son unas trece órdenes de magnitud más de lo que da el azar. Mirándolas una por una: las de las tres bases son **la cola de poli-A del genoma viral**, posiciones 6338-6346. Descontadas, las tres cifras caen a **cero**; en el criterio de bloque perfecto de ≥19 nt queda señal real: 8, 7 y 19 `[M]`.
**Alternativas consideradas:** (a) no marcarlas, que es lo que hace el original; (b) filtrarlas y no contarlas; (c) la elegida, marcarlas y descontarlas a la vista.
**Criterio:** sobre (a), un conteo de off-targets que mete la cola de poli-A en la misma bolsa que una homología real no sirve para decidir nada, y el nuestro lo hacía igual que `bowtie -a -v N -y`, que es ciego a la complejidad igual que a la posición del desajuste. Sobre (b), descartar en silencio es el otro error: quien lee no puede saber qué se sacó ni con qué criterio, y un veto que se aplica sin mostrarse no se puede discutir. Sobre (c): la cifra que decide la lee una persona, así que las dos cifras van juntas y el criterio va escrito al lado.
**Consecuencia:** el criterio es nuestro `[H]` y está declarado en `sifi_plus/complejidad.py` —racha de un mismo nucleótido de 10 nt o más, o dos nucleótidos distintos o menos en la ventana—, deliberadamente grosero y transparente en vez de un puntaje con umbral ajustado. Marca 18 de las 6.346 ventanas del MRFV y ninguna de las 1.116 del ARNm de maíz del ejemplo `[M]`. Queda pendiente contrastarlo contra la corrida de `dustmasker` que el repositorio ya tiene en `research/ola2/W5_secuencias_epilab/analisis/dustmasker_full.txt`, que es el paso para reemplazar un criterio propio por el estándar; hasta entonces la marca va con `[H]` y no con `[E]`. Esto no cambia ningún número ya publicado, pero sí obliga a releer: el tamizaje que está en `research/` se corrió sin la marca, y corresponde volver a leer esas tablas con este descuento antes de sostener cualquier afirmación sobre coincidencia perfecta en no objetivo.

## D60 — La procedencia de un dato se verifica contra el propio pipeline antes de preguntarle a nadie
**Fecha:** 2026-10-24
**Quién:** el equipo, línea M9 (auditoría de secuencias, issue #13).
**Decisión:** `baseline_dsrip/dsrip_vatpaseA.csv` entra a la lista blanca de `tools/verificacion/sin_secuencias.py` con su locus y su ensamblado escritos en el motivo, y la excepción se sostiene en una verificación reproducible y no en la palabra de quien corrió la línea.
**Hecho que motivó la decisión:** la primera corrida de la auditoría dejó ese archivo sin exceptuar a propósito: reconstruye 1.845 nt —el CDS completo de V-ATPase A— y el LEEME sólo decía que venía de `pipeline/salida/sirna_vatpaseA.csv`, que no se versiona. La pasada contra la planilla de EPILAB daba cero, pero un cero no es una procedencia. La respuesta estaba en las salidas del propio pipeline: de las 1.825 ventanas, las 25 que sobreviven al tamizaje aparecen en `sirna_finales.csv` y `sirna_cercanos.csv` con columna `locus`, y las 25 caen en `L06020`, que `candidatos_alto.csv` ubica en `OZ319711.1:47265953-47286132` (+), 11 exones, ortólogo de *Drosophila* `Vha68-2` `[M]`. `OZ319711.1` es uno de los diez cromosomas de `GCA_975739785.1` (ihDalMaid1.1, Wellcome Sanger), público. El CDS reconstruido es un marco limpio: ATG inicial, 614 codones más `TAA`, cero stops internos `[M]`.
**Alternativas consideradas:** (a) preguntarle a quien corrió la línea y exceptuar con su respuesta; (b) mandar el CDS a un BLAST web, que lo resolvía en un minuto; (c) la elegida, reconstruir la procedencia con lo que ya está en disco.
**Criterio:** sobre (a), una excepción que se apoya en un recuerdo no es auditable y bloquea el criterio de terminado hasta que alguien conteste. Sobre (b), está prohibido por la regla de confidencialidad del `CLAUDE.md`, y el caso lo muestra bien: la procedencia dudosa es justamente la razón por la que no se puede subir —si se supiera que es público no haría falta el BLAST, y si no lo es, subirlo es la fuga—. Sobre (c), el pipeline ya había guardado el vínculo entre ventana y locus; sólo había que leerlo.
**Consecuencia:** la verificación queda en `research/ola4/M9_auditoria_secuencias/scripts/procedencia_vatpasea.py`, corre **con insumos locales** —`pipeline/salida/` está en `.gitignore`— y aborta declarando la corrida pendiente si el insumo falta, en vez de devolver un cero tranquilizador. Con esta excepción, el árbol y el historial dan la misma cifra, 28 hallazgos no exceptuados en dos archivos, que son los que esperan la decisión del §6.1 de M9. El método es generalizable: antes de preguntar de dónde salió un dato derivado, buscar la columna que lo ata a su locus en las salidas que lo produjeron.

## D61 — Las 28 ventanas de EPILAB que ya están en el árbol se dejan como están
**Fecha:** 2026-10-25
**Quién:** el usuario, al cerrar la última casilla técnica de M9 (issue #13).
**Decisión:** `research/ola3/C4_offtargets_quimeras_largo/resultados/q2_aciertos_localizados.tsv` y `research/ola3/C13_quimeras_region_recomendada/resultados/empalme_maiz_detalle.json` **no se tocan**. Entran a la lista blanca de `tools/verificacion/sin_secuencias.py` con la decisión y su motivo por escrito, de modo que la verificación deja de reportarlas y pasa a dar cero hallazgos no exceptuados.
**Hecho que motivó la decisión:** la auditoría de M9 encontró 28 ventanas de 21 nt de regiones de EPILAB repartidas en esos dos archivos, ya commiteadas y pusheadas `[M]`. Son ventanas sueltas —las que pegan en maíz— y no una serie consecutiva, así que **no reconstruyen la región**: cubren 46 de 200 nt de `MP_MRFV` (23,0 %) y 48 de 300 de `BicC_Dm` (16,0 %), con tramos contiguos máximos de 23 y 25 nt `[M]`. El repositorio es privado (verificado). Las dos regiones virales son además subcadenas del genoma público `NC_002786.2`, así que su confidencialidad es nominal; `BicC_Dm` no está en esa situación, y es la mitad del hallazgo.
**Alternativas consideradas:** (a) la elegida, dejarlo y declararlo; (b) quitar la columna con un commit nuevo, que lo deja en el historial igual; (c) reescribir el historial.
**Criterio:** la regla del `CLAUDE.md` es específica y dice que las secuencias de EPILAB **no se suben a servicios web de terceros que las procesen** —BLAST web, servidores de plegado, dsRNA-Engineer—; no dice que no puedan estar en el árbol, y de hecho el proyecto entero trabaja con ellas localmente. Con el repositorio privado y fragmentos que no reconstruyen nada, el riesgo es residual y no justifica el costo de (b), que además no borra nada porque el dato queda en el historial. Sobre (c), es destructivo para quien ya clonó y retirar algo ya publicado no lo borra de las copias existentes: es el mismo criterio de D41.
**Consecuencia:** el árbol y el historial dan **cero hallazgos no exceptuados**, así que el criterio de terminado del issue #13 queda satisfecho por la primera de sus dos vías. Lo que queda vivo es el escenario de compartir: si en vez del paquete autocontenido con `tools/sifi21_port/` se le diera a alguien acceso al repositorio entero, estos fragmentos van adentro, y esta decisión hay que releerla. Nótese que exceptuar estos archivos **no los exime de la pasada 3**: desde el cambio de hoy la lista blanca no tapa los hallazgos contra la planilla de EPILAB, así que si alguna vez entrara una secuencia que sí reconstruye, la verificación la seguiría marcando.

## D62 — La discrepancia de los cuatro conteos es de la función de conteo, no de la termodinámica
**Fecha:** 2026-10-25
**Quién:** el investigador lo resolvió del lado del laboratorio y lo comunicó en su carta del 25-10; el equipo lo verificó con insumos propios en la línea N1.
**Decisión:** la explicación vigente de la brecha entre nuestros conteos y los de la planilla es **la función histórica de conteo**, y la hipótesis del conteo por aciertos de Bowtie se retira como causa de esos cuatro números sin retirarse como hallazgo sobre la herramienta original.
**Hecho que motivó la decisión:** la carta informa que la curva de eficiencia se construye asignando 20 posiciones de cobertura a cada ventana de 21 nt y que el contador identifica siRNAs nuevos por los incrementos positivos de esa curva, de modo que una ventana eficiente que empieza donde otra termina no se registra `[R]`. Implementada esa regla sobre las ventanas eficientes de nuestro port con la configuración que reconstruye las curvas —modo `fiel`, ViennaRNA 2.7.2, tabla `RNA_NN4`, que da 138, 40, 218 y 35—, el conteo por incrementos con ancho 20 da **114, 35, 199 y 33**: los cuatro valores de la planilla, exactos. Con ancho 19 y con ancho 21 no se reproducen los cuatro `[M]` (`research/ola5/N1_regla_de_conteo/`).
**Alternativas consideradas:** (a) el umbral de estabilidad de extremos en 1,75; (b) la tabla de vecinos más cercanos; (c) la referencia de Bowtie contra la que se contó; (d) la elegida, la unidad y la función de conteo.
**Criterio:** (a) y (b) quedan descartadas por la propia reproducción: los cuatro valores salen sin mover un solo parámetro termodinámico, así que la coincidencia de 1,75 con algunos valores era circunstancial, como dice la carta. (c) quedó medida en M1 sobre once bases y treinta y ocho celdas y ninguna celda reproducía los cuatro; el «200 contra 199» de `BicC_Dm` era coincidencia, y el mecanismo verdadero da 199 clavado. (d) es la única que reproduce los cuatro a la vez con un solo parámetro entero.
**Consecuencia:** tres cosas. Primero, el pedido 1 de la reunión —la clasificación por ventana de su corrida— **se cae**: lo pedíamos para explicar los conteos. Segundo, aparece un quinto límite para `M8`: la función esconde entre el **5,7 %** y el **17,4 %** de las ventanas eficientes según el gen, y como el sesgo depende de cuán agrupadas están las ventanas y no del largo ni de la calidad del diseño, **dos cifras de la planilla no son comparables entre sí** `[H]`. Tercero, queda abierto con qué tabla de apilamiento corre el método histórico: que las curvas reconstruyan exactamente los valores de `sifi21INTA` por defecto es compatible con la tabla de Zuber, y si se confirma, la línea base para comparar contra la planilla deja de ser 133/32/212/42 `[?]`.

## D63 — Cada conteo se publica con su marco declarado, y hay tres marcos con nombre
**Fecha:** 2026-10-25
**Quién:** el equipo, línea N3, a partir de la distinción que propuso el investigador en su carta del 25-10.
**Decisión:** todo conteo de ventanas eficientes de una región viaja con su **marco**, igual que viaja con su configuración, y los marcos son tres y se nombran: **contexto, todos los arranques** (los `L` que caen en la región, plegados en el gen); **contexto, los comparables** (los `L − 20` que existen en la molécula, plegados en el gen); y **molécula recortada** (los `L − 20`, plegada sola). La cifra que se publica para una región candidata es la del tercer marco.
**Hecho que motivó la decisión:** la carta separa dos preguntas que el modelo heredado de si-Fi21 no separa, porque RNAplfold trabaja sobre la secuencia que se le pasa: qué siRNAs puede producir el ARNdc aplicado —y ahí manda la molécula final— y cuán accesible es el sitio de unión en el ARN endógeno, donde lo representativo es el transcrito en contexto `[R]`. Medidos los tres marcos en las seis regiones vigentes y rivales, el recorte **no baja los conteos: los mueve en direcciones distintas**, baja en tres regiones y sube en tres `[M]` (`research/ola5/N3_marcos/`). Para `BicC_Dm` 922-1221 los tres marcos dan 36, 29 y 26, y la diferencia se parte en siete ventanas de límite físico y tres de contexto de plegado; del modelo de eficiencia no sale ninguna.
**Alternativas consideradas:** (a) publicar un solo número y no nombrar el marco, que es lo que hacíamos; (b) publicar el marco intermedio, que es el que el investigador propone explorar; (c) la elegida, publicar el de la molécula y declarar los tres.
**Criterio:** sobre (a), con conteos que se mueven en direcciones distintas según el marco, un número sin marco no se puede comparar con ningún otro, y las seis filas de N3 son la prueba. Sobre (b), el marco intermedio contesta la pregunta de accesibilidad en el blanco y es el que hay que usar para esa pregunta, pero la cifra de una región candidata es la de la molécula que se sintetizaría, que es la que existe. Sobre (c), los tres números valen y lo que no vale es mezclarlos.
**Consecuencia:** la cifra de `BicC_Dm` 922-1221 sigue siendo **26** y queda respaldada por la carta. Y queda escrito que un ranking armado en contexto no es el ranking de las moléculas: cambiar el ranking no es de N3.

**Nota de aplicación (2026-10-25, el mismo día):** el marco intermedio se cruzó con los dos ejes que faltaban y las dos corridas refuerzan la decisión por caminos distintos. Con la grilla (`N3` §6): 41,1 % de las 4.368 configuraciones contra la región de C7, con 640 empates y margen mediano **cero**, y 99,9 % contra la del laboratorio, que es la fracción más alta de los tres marcos `[M]`. Con el eje de referencia (`N3` §7, una de las cuatro fuentes): las mismas tres bases que mueven el conteo de 2121-2420 en tres ventanas al plegar la molécula sola lo mueven en **ocho** al plegar el gen completo `[M]`. `[H]` O sea que el marco no sólo cambia el número: cambia **cuánta sensibilidad tiene el número a cada otra cosa que se mueva** —los umbrales, el motor, la fuente de la secuencia—. Por eso «cada conteo viaja con su marco» no es una convención de prolijidad: sin el marco, una afirmación de robustez no se puede evaluar.

## D64 — La razón escrita de D25 se reemplaza por la cobertura declarada por fuente
**Fecha:** 2026-10-25
**Quién:** el equipo, al preparar la ficha de N5 para la reunión.
**Decisión:** el criterio con el que D25 movió la región recomendada de `BicC_Dm` —«32 de 36 idénticas en los tres transcriptomas públicos contra 22 de 35»— **se retira como argumento** y se reemplaza por la tabla de cobertura e identidad por fuente separada. La decisión de recomendar 922-1221 **no se revierte**.
**Hecho que motivó la decisión:** medido por fuente (`M7` §4), `GCWP01` (Illinois) no cubre un solo nucleótido de 922-1221: alinea con el gen en dos tramos, 2044-2467 y 249-433, y cubre 609 de 2.520 posiciones `[M]`. Las 36 ventanas eficientes de 922-1221 quedan **sin datos** en esa fuente, y la única región que esa fuente cubre entera es 2121-2420, donde contradice 13 de 35. El «32 contra 22» sale de contar la ausencia de datos como ausencia de contradicción. Por fuente separada: en el transcriptoma argentino las dos regiones conservan el 100 % de sus eficientes; en el de Ohio, 2121-2420 conserva 33 de 35 y 922-1221 conserva 32 de 36, o sea que ahí la región de C7 está **mejor**.
**Alternativas consideradas:** (a) dejar el argumento como está; (b) revertir D25 y volver a 2121-2420; (c) la elegida, conservar la decisión y reescribir su razón.
**Criterio:** sobre (a), es una afirmación que no se sostiene y la íbamos a tener que defender en la reunión. Sobre (b), la decisión se sostiene por otras dos fuentes que sí cubren la región —el genoma del Reino Unido, con 36 de 36 idénticas contra 27 idénticas y 8 que cruzan un empalme, y el ensamblado de Córdoba según `C8`— más el perfil de off-target, donde 922-1221 tiene cero coincidencias perfectas de 21 nt. Sobre (c), lo que estaba mal era el argumento y no el resultado, y corresponde decirlo nosotros antes de que lo pregunte.
**Consecuencia:** todo documento que cite el «32 contra 22» hay que corregirlo, y la tabla de cobertura por fuente pasa a ser la forma de presentar la conservación: una fuente que no cubre una región se declara **sin datos** y no como cero. Es la misma distinción que M1 hizo con las celdas no corridas de su matriz.

## D65 — El conteo de eficientes deja de ser argumento entre `BicC_Dm` 922-1221 y 2121-2420
**Fecha:** 2026-10-25
**Quién:** el equipo, línea N10, al cerrar el hueco que N1 había abierto y el plan de la ola 5 no había cubierto.
**Decisión:** la comparación entre las dos regiones de `BicC_Dm` **no se sostiene con el número de ventanas eficientes**, en ningún marco y con ninguna lectura. Lo que la sostiene es el perfil de off-target y la conservación por fuente. Donde los documentos citan «36 ventanas contra 35» como criterio, se reemplaza por esa base.
**Hecho que motivó la decisión:** tres mediciones independientes, hechas en tres líneas distintas, apuntan al mismo lado. `M7` §2: sobre 4.368 configuraciones 922-1221 le gana a 2121-2420 en el 36,4 % contando dentro del gen y en el 15,7 % en el modo del ranking, y con el motor del si-Fi original la única ventana del punto por defecto **se invierte** `[M]`. `N3` §6: en el marco intermedio la fracción es 41,1 %, con 640 empates y **margen mediano exactamente cero** `[M]`. `N10`: con la función histórica de conteo del laboratorio, en el marco de contexto el 36 contra 35 **es un empate, 33 a 33** `[M]`. Contra `264-563`, en cambio, la ventaja aguanta las tres cosas: entre el 99,1 % y el 99,9 % en los tres marcos, con margen mediano de 10 a 12 ventanas.
**Alternativas consideradas:** (a) seguir citando el 36 contra 35, que es cierto en el punto por defecto; (b) revertir a 2121-2420, que gana en el motor del original; (c) la elegida, conservar 922-1221 y retirarle el argumento de conteo.
**Criterio:** sobre (a), un margen de una ventana que se invierte al cambiar de motor, se empata al cambiar de contador y se vuelve cero mediano al cambiar de marco no es una diferencia; citarlo es ofrecerle al interlocutor el contraejemplo. Sobre (b), tampoco hay base para revertir: la ventaja de 2121-2420 aparece sólo con un motor y desaparece con los otros, y esa región tiene 6 alertas de bloque de ≥ 19 nt contra las 3 de 922-1221 y 13 de sus 35 ventanas contradichas por el transcriptoma de Illinois. Sobre (c), es lo que la evidencia permite afirmar: una preferencia por riesgo y conservación, no por conteo.
**Consecuencia:** hay que corregir dos lugares donde el conteo figura como criterio: la nota de aplicación del 2026-10-22 de D18 (`DECISIONS.md`, que cita «36 ventanas contra 35») y la alternativa (a) de D25 («2121-2420, que tiene un eficiente menos»). `M7` y sus notas ya lo declaraban con el matiz correcto y no cambian. Y queda una regla general `[H]`: **un margen que se mueve menos que la sensibilidad del instrumento no se publica como argumento**, se publica como empate con sus incertidumbres al lado. Para la comparación contra `264-563` nada de esto aplica: ahí el margen es de diez a doce ventanas y aguanta los tres ejes.

## D66 — La exposición de un no objetivo se declara como decisión abierta, no se le pide un número al investigador
**Fecha:** 2026-10-26
**Quién:** el equipo, a partir de lo que el investigador contestó en el checkpoint 2.
**Decisión:** el peso de exposición de *Homalodisca vitripennis* **deja de tratarse como un dato pendiente del laboratorio** y pasa a ser una decisión del equipo, declarada, con su consecuencia medida al lado y sin valor único. Todo documento que hoy dice «falta que el investigador fije este número» se reescribe para decir qué pasa con cada valor.
**Hecho que motivó la decisión:** se le preguntó derecho, dos veces, qué exposición asignarle a un cicadélido norteamericano en un lote argentino, y contestó las dos cosas a la vez: que el organismo *«no está en Argentina, o sea que puede no importar»* y que *«puede venir eventualmente y tal vez si la querés matar»* `[R]`. Y dio el criterio de qué hacer con esa ambigüedad, que no es resolverla: *«igual si vos querés ser específico para esta, mostrar que esas posibles decisiones están presentes es como el extra que me parece»* `[R]`. En la misma reunión aclaró además que ese organismo **no estaba en su panel** —*«el bicho ese yo no lo tenía»*—, así que no hay una práctica del laboratorio que copiar.
**Alternativas consideradas:** (a) insistir por correo hasta obtener un número; (b) fijar nosotros un valor y defenderlo; (c) la elegida, declarar la decisión abierta y publicar el resultado en los dos extremos.
**Criterio:** sobre (a), ya se preguntó en el correo del 22 y en la reunión del 26, y la segunda respuesta fue explícitamente ambivalente: insistir es pedirle que invente una ponderación que él mismo no usa. Sobre (b), un valor nuestro sin fundamento ecológico sería un parámetro libre disfrazado de medición, y el veto es binario —en la cascada `CP_MRFV` va antes que `ATPaseD_Dm` en el 100 % de los sorteos con cualquier exposición y en el 0 % con exposición exactamente cero, sin transición `[M]`—, así que el número elegido no sería un matiz sino el resultado. Sobre (c), es lo que él pidió y es lo que la medición ya soporta: `research/ola4/M5_dos_ejes/` tiene los dos extremos corridos.
**Consecuencia:** la pregunta sale de `PREGUNTAS_ABIERTAS.md` como pedido al investigador. El entregable tiene que mostrar, en el mismo lugar, que con exposición cero **tres de las seis regiones recomendadas se mudan** y que una de ellas vuelve a ser `ATPaseD_Dm` 137-436, la región más conservada del gen, descartada por D25 justamente por estar vetada `[M]`. Y queda una regla `[H]`: cuando un parámetro no tiene fuente y tiene palanca, lo que se publica no es el valor sino el mapa de lo que cambia con él.

## D67 — Las quimeras se arman por combinación de fenotipos, y la juntura se cuenta aparte
**Fecha:** 2026-10-26
**Quién:** el investigador lo propuso en el checkpoint 2; el equipo lo adopta como criterio de diseño.
**Decisión:** una quimera deja de evaluarse sólo por densidad de ventanas eficientes y pasa a armarse por **combinación de fenotipos que no se solapan** —reproducción, movilidad, letalidad—, y su conteo de eficientes se publica **separando las ventanas de juntura**, que no se cuentan como capacidad de silenciamiento.
**Hecho que motivó la decisión:** describió cómo lo plantean ellos —*«tratar de armar quimeras, justamente atacando genes que tengan distintas características»*— y dio los tres ejes con un ejemplo cada uno: la reproducción del insecto, *«algún gen que esté involucrado en las alas, si no tiene alas, por más que ande ahí, no importa»*, y *«otro que sea súper esencial y que si no lo tiene se muere»* `[R]`. Sobre la juntura marcó el error de método: al pegar dos fragmentos el programa sigue calculando eficiencia sobre el empalme, pero *«biológicamente, una molécula que se genera acá, ¿a quién le va a pegar? A este, a este, a ninguno. No va a encontrar»*, y lo resumió en *«me puede decir que es el mejor eficiente del mundo, pero si no va a encontrar su target en la planta o en el insecto, no va a ser»* `[R]`.
**Alternativas consideradas:** (a) seguir armando quimeras por densidad, que es como se armaron las doce de C13; (b) descartar las quimeras por no tener evidencia de que funcionen en la especie; (c) la elegida, rearmarlas por fenotipo y contar la juntura aparte.
**Criterio:** sobre (a), es lo que veníamos haciendo y el propio conteo lo desmiente: una quimera **no agrega ventanas, canjea** los veinte arranques de cola de cada fragmento por veinte de juntura `[M]`, así que optimizar densidad sobre una quimera optimiza en parte sobre ventanas que no existen en ningún transcrito. Sobre (b), el argumento de él es biológico y no de eficiencia —cubrir varios mecanismos con una molécula— y ataca de frente la tensión que `entregables/recomendacion-defendida.md` ya declaraba: `BicC_Dm` tiene el mejor perfil de riesgo con un fenotipo que no bloquea transmisión, y la V-ATPasa tiene mortalidad medida por ingesta con peor perfil de off-target. Sobre (c), la mitad del trabajo ya está hecha y medida.
**Consecuencia:** la parte de la juntura **no requiere cómputo nuevo**: `research/ola5/N4_quimeras/` ya midió que de las 240 ventanas de juntura de las doce quimeras **4 son eficientes y ninguna de esas 4 tiene blanco continuo de 21 nt**, y que las 8 que sí tienen blanco son todas de los extremos de la unión y ninguna es eficiente `[M]`. Lo que falta es presentarlo —hoy vive en un REPORT y él lo señaló como el diferencial posible— y armar las combinaciones por fenotipo. Y acá apareció, al revisar el catálogo contra su pedido, que **los tres ejes ya tienen candidato en *Dalbulus maidis*** y ninguno hay que salir a buscarlo: `BicC` (`DM-01`) para reproducción, **`V-ATPase B` (`DM-02`) para alas** —alas deformes, más supervivencia del 16 % al día 4 contra 37 % del control— y `V-ATPase D` (`DM-03`, nuestro `ATPaseD_Dm`) para letalidad, con efecto en alas **no** significativo; los tres con la fuente leída completa `[M]`. Que dos subunidades del mismo complejo se separen justo por el eje que él nombró es lo que vuelve armable la combinación. El único insumo que falta es **la secuencia de `V-ATPase B`**, que no está en el panel de trabajo y puede salir del transcriptoma que ofreció mandar `[?]`.

## D68 — Las diecisiete alertas quedan firmadas, y la firma vive fuera de la tabla
**Fecha:** 2026-10-26
**Quién:** el equipo. D48 dice que la justificación la escribe el usuario y no el motor; esta decisión la escribe, no la delega.
**Decisión:** las diecisiete filas de `research/ola4/M6_alertas/resultados/alertas.tsv` quedan **decididas**: **catorce aceptadas y tres bloqueantes**. Las tres bloqueantes son las únicas con coincidencia perfecta de 21 nt, las tres contra *Homalodisca vitripennis* y las tres sobre regiones que el proyecto **no** recomienda: `BicC_Dm` 264-563, `ATPaseD_Dm` 151-450 y `ATPaseD_Dm` 137-436. Y la firma deja de vivir en la tabla: se escribe en `research/ola4/M6_alertas/decisiones.tsv`, que es **entrada** del generador y no salida suya.
**Hecho que motivó la decisión:** D48 invirtió el default. El veto descartaba por omisión; la tabla que lo reemplazó no descarta nada, así que **una alerta no leída quedaba operativamente igual que una aceptada**, y las diecisiete filas llevaban desde el 25 de octubre en «pendiente». La reunión del 26 destrabó lo que faltaba: el investigador aclaró que *Homalodisca vitripennis* no estaba en su panel —*«el bicho ese yo no lo tenía»*—, que no está en la Argentina y por eso *«puede no importar»*, pero también que *«puede venir eventualmente y tal vez si la querés matar»*, y dijo qué espera que hagamos con eso: *«si vos querés ser específico para esta, mostrar que esas posibles decisiones están presentes es como el extra que me parece»* `[R]`.
**Alternativas consideradas:** (a) dejar las diecisiete en «pendiente» hasta tener el número de exposición; (b) aceptar las diecisiete con un párrafo común; (c) convertir la firma en veto automático; (d) la elegida.
**Criterio:** sobre (a), D66 ya cerró que ese número no va a existir, así que esperarlo era esperar indefinidamente mientras la tabla seguía sin frenar nada. Sobre (b), el validador lo permitiría si cada párrafo nombra su locus, pero vacía de sentido el mecanismo: cada fila tiene su propio argumento y las tres de 21/21 no se parecen a las otras catorce. Sobre (c), D48 decidió lo contrario y él lo confirmó en su carta del 22: la carga de la prueba cambia de lugar, no se automatiza. Sobre (d): las catorce aceptadas tienen **cero** coincidencias perfectas de 21 nt —que es lo que D48 obliga a justificar textualmente— y sus bloques de ≥ 19 nt se informan porque lo manda D28, que al fijar ese piso declaró que a 19 nt la convención del campo no tiene experimento detrás `[M]`. Las tres bloqueantes impactan el **ortólogo del gen que se silencia** en un cicadélido no objetivo, y las tres caen en regiones que ya no recomendamos, así que bloquearlas no retira ninguna opción en uso y deja el motivo escrito.
**La tercera bloqueante lleva su condición escrita, y es la que importa:** `ATPaseD_Dm` 137-436 es la región que D25 descartó **precisamente por estar vetada**, y `M5` midió que con exposición cero vuelve a la mesa como la más conservada del gen, con 24 ventanas eficientes contra las 18 de la región de la planilla `[M]`. Firmarla aceptada adoptaría exposición cero por la ventana, que es justo lo que D66 decidió no hacer; firmarla bloqueante a secas cerraría una opción medida. Queda bloqueante **con la condición en la propia justificación**: si el equipo declara exposición cero para ese cicadélido, esa fila se vuelve a firmar, porque entonces los bloques compartidos se leen como señal de conservación entre cicadélidos y no como riesgo ecológico.
**Consecuencia:** con las diecisiete firmadas, `alertas.exigir_decidida()` pasa sobre **las seis regiones vigentes en los dos umbrales de D28** `[M]`, y eso cambia el estado de la pregunta abierta que dejó `M6`: con el umbral literal nada se movía, pero con el umbral laxo **cuatro de las seis vigentes quedaban frenadas** por no tener firma, y ahora pasan por tenerla. La pregunta de qué umbral adopta la compuerta sigue abierta —esta decisión no la cierra—, pero deja de bloquear por omisión. Y la fila de `PDE1C` sobre la región vigente `ATPaseD_Dm` 72-371 queda marcada en su propia justificación como la que hay que releer si alguna vez se adopta el umbral laxo: es la única fila humana con dos bloques de ≥ 19 nt en ventanas predichas eficientes.
**Lo que esta decisión no hace:** no dice que ninguna región sea segura. Dice que fueron leídas, por quién y con qué argumento. El límite viaja con las diecisiete y está en cada justificación: se midió **coincidencia exacta** de 21 nt, no apareamiento parcial ni efecto de tipo miARN `[?]`.

---

## D69 — La compuerta de alertas se llama desde el único punto donde una región se vuelve recomendación, y adopta el umbral literal de D48
**Fecha:** 2026-10-27
**Quién:** el orquestador, al ejecutar `R2` del plan de cierre (§3) sobre las firmas que dejó D68.
**Decisión:** `alertas.exigir_decidida()` pasa a llamarse desde **`ranking.region_recomendada()`** (`tools/sifi21_port/ranking.py`), que queda como el único lugar del port donde el primer puesto de `alternativas()` se convierte en una región recomendada. Las tres rutas que antes hacían esa conversión por su cuenta —el nivel 3 de `ranking.cmd_ranking` y las dos de `ranking_v2`, `completar_regiones` y `recomendadas`— pasan por ella, y una región con una fila de alerta en «pendiente» **no sale de ahí**: levanta `AlertaSinDecidir` y no devuelve región. El umbral con el que la compuerta exige decisión es **`perfecto_21`**, que es D48 literal; queda escrito como el nombre `ranking.UMBRAL_COMPUERTA`, se mueve con `--umbral-compuerta` en los dos ejecutables y con el parámetro `umbral` de la función, y **no se escribe en el cuerpo de ninguna llamada**. Si la tabla de alertas no está en disco, la recomendación falla cerrada: una tabla ausente no es «cero alertas».
**Hecho que motivó la decisión:** la compuerta estaba implementada y con prueba desde `M6`, y nadie la llamaba. Verificado abriendo el árbol: fuera de `test_alertas.py`, la única llamada estaba en `research/ola4/M6_alertas/scripts/compuerta.py:53`, un script de inventario de la ola 4 que no produce ninguna recomendación `[M]`. Y la conversión de «primer puesto del orden» en «región que recomendamos» estaba escrita **tres veces, idéntica** —`(int(x) for x in alt["mejores"][0]["region"].split("-"))`— y ninguna de las tres consultaba la tabla. O sea que el port podía recomendar una región cuya alerta nadie había leído, que es el default invertido que D48 dejó abierto y que `exigir_decidida()` existe para cerrar.
**Alternativas consideradas:** (a) ponerla en `pipeline/region_scoring.py`, que es el candidato obvio porque ya tiene un veto por región; (b) ponerla donde se genera el entregable; (c) ponerla dentro de `alternativas()`; (d) dejarla donde está, en el script de la ola 4, y declarar la tarea hecha; (e) la elegida.
**Criterio:** sobre (a), `region_scoring.py` es del linaje del `pipeline` —trabaja sobre las ventanas de los loci de *Dalbulus maidis* que enumera `sirna_enumerar.py`, con clave `locus|pos`— y **ninguna región publicada salió de ahí**: las seis vigentes son regiones de los seis genes con nombre. Poner la compuerta ahí sería ponerla donde no pasa ninguna recomendación. Sobre (b), **ese código no existe, y decirlo es parte del resultado**: los documentos de `entregables/` son Markdown escrito a mano y convertido con `tools/md_a_html.py`, así que no hay punto de generación que interceptar; el último eslabón entre el cómputo y lo publicado es una persona copiando un número, y eso ninguna compuerta lo cubre. Sobre (c), `alternativas()` tiene dos usos y sólo uno es recomendar: el nivel 2 publica las tres mejores como exploración dentro del gen, y frenar eso frenaría el diagnóstico junto con la recomendación. Sobre (d), eso ya estaba y es justamente lo que el pendiente decía que no alcanza: una compuerta que sólo llama un script de inventario no impide nada. Sobre (e), es el punto por el que pasa toda recomendación del port, y se verificó contra la salida publicada —`research/ola3/C7_ranking_v2/resultados/ranking_v2.json`, `k=21`, clave `regiones_recomendadas`— que **cinco de las seis regiones vigentes son literalmente lo que devuelve esa ruta** (`MP_MRFV` 72-271, `CP_MRFV` 99-298, `ATPaseD_Dm` 72-371, `eth_Dm` 114-313, `bursA_Dm` 13-212) y que la sexta es la misma ruta corregida después por D25 (`BicC_Dm`, de 2121-2420 a 922-1221) `[M]`.
**El umbral, con su consecuencia medida.** La elección del umbral no se podía dejar implícita, porque llamar a la compuerta con un default es adoptarlo. Se midió con `research/ola4/M6_alertas/scripts/umbral_compuerta.py`, sobre las doce regiones de `resultados/estado_regiones.tsv` y las diecisiete filas de `resultados/alertas.tsv`, en los dos umbrales de D28 y en los dos estados de firma; la salida queda en `resultados/umbral_compuerta.json`:

| Estado de la tabla | `perfecto_21` (D48 literal) | `perfecto_ge19` (umbral laxo de D28) |
| --- | --- | --- |
| con las diecisiete firmas de D68 | pasan **12 de 12**, tres de ellas bloqueantes y ninguna vigente | pasan **12 de 12**, las mismas tres bloqueantes |
| con las diecisiete en «pendiente» | pasan **9 de 12**: frena tres, **ninguna vigente** | pasan **3 de 12**: frena nueve, y **cuatro de las seis vigentes** |

`[M]` Los dos pares de cifras que circulaban por separado son las dos lecturas de ese mismo renglón de abajo y no se contradicen: «9 de 12 contra 3 de 12» cuenta regiones que pasan sobre el total de doce, y «cuatro de las seis vigentes» cuenta, de las nueve que el umbral laxo frenaba, las que el proyecto recomienda. Reproducen la tabla de `research/ola4/M6_alertas/REPORT.md` (líneas 257-260), que se midió antes de las firmas y que hasta ahora era la única fuente de esos dos números.

`[H]` **Por qué se adopta el literal, y por qué ahora.** Con las firmas puestas los dos umbrales dan el mismo resultado operativo —las doce pasan en los dos—, así que elegir uno hoy no mueve ninguna región ni ninguna cifra publicada, y es la única ventana en que la elección es barata. Entre los dos se adopta el que tiene detrás la decisión escrita: D48 dice textualmente «cada coincidencia perfecta de 21 nt ... genera una fila», y D28 fijó el piso de 19 nt declarando que a ese largo la convención del campo **no tiene experimento detrás**. Exigir decisión en un umbral sobre el que ninguna decisión del proyecto se pronunció sería inventar una obligación; dejarlo configurable, en cambio, deja medible el otro escenario sin adoptarlo.
**Consecuencia:** el criterio de `R2` queda cumplido en el port y no en un script suelto: `test_alertas.py` §9 prueba que la recomendación falla con la fila en «pendiente», que pasa firmada, que los dos umbrales de D28 no dan lo mismo sobre la misma fila, y que una tabla ausente falla cerrada. La última verificación de la sección es estructural y hace falta: comprueba que ninguna de las tres rutas del port rearma la región a mano, porque la forma de desactivar la compuerta sin tocarla es volver a escribir al lado la expresión que ella reemplazó. **Ninguna cifra publicada se mueve:** las seis regiones que el port recomienda hoy pasan la compuerta en los dos umbrales `[M]`.
**Lo que esta decisión no hace, y es el límite que hay que leer al lado:** `exigir_decidida()` no puede distinguir «se tamizó y no hay alertas» de «no se tamizó». Una región que no está en el inventario de las doce de `M6` no tiene filas y pasa la compuerta como «sin alertas en este umbral», así que lo que queda protegido son las doce regiones evaluadas y no una propuesta nueva —el caso concreto es el ranking a 22 nt, cuyas seis regiones recomendadas no están en el inventario—. Cerrarlo pide exigir que la región esté en el inventario, y eso cambiaría el resultado de una corrida publicada, así que queda anotado en `00_meta/PREGUNTAS_ABIERTAS.md` y no se hace acá. Y sigue en pie el límite de arriba: entre el cómputo y el documento publicado hay una persona, y la compuerta no la cubre.

## D70 — La compuerta va a exigir presencia en el inventario, y el tamizado va primero
**Fecha:** 2026-10-27
**Quién:** Luca, sobre la pregunta abierta 9 que dejó `D69`. La decisión es suya; esta entrada la registra y fija el orden de ejecución.
**Decisión:** `exigir_decidida()` **va a exigir que la región esté presente en el inventario de alertas**, de modo que «no se tamizó» deje de pasar como «se tamizó y no hay alertas». Y se decide el orden: **primero se tamizan las seis regiones recomendadas a 22 nt, después se aprieta la compuerta.** Apretarla antes rompería la única ruta que hoy produce esas seis.
**Hecho que motivó la decisión:** `D69` puso la compuerta en `ranking.region_recomendada()` pero dejó un agujero medido. El inventario de `M6` tiene **doce** regiones (`research/ola4/M6_alertas/resultados/estado_regiones.tsv`), y las seis que el ranking recomienda a **k=22** —`MP_MRFV` 162-361, `CP_MRFV` 77-276, `BicC_Dm` 2119-2418, `ATPaseD_Dm` 71-370, `eth_Dm` 193-392, `bursA_Dm` 44-243, leídas de `research/ola3/C7_ranking_v2/resultados/ranking_v2.json` clave `k.22.regiones_recomendadas`— **no son ninguna de las doce**, y tienen **cero** filas en `resultados/alertas.tsv` `[M]`. O sea que hoy atraviesan la compuerta sin que nadie las haya tamizado, que es exactamente el modo de fallar que `D48` quiso cerrar. No son un ejercicio hipotético: su `jaccard_21_22` está publicado.
**Alternativas consideradas:** (a) exigir inventario y re-tamizar las seis de 22 nt antes, la elegida; (b) exigir inventario sólo a 21 nt y declarar la corrida de 22 como exploratoria; (c) dejarlo como pregunta abierta en el entregable, sin tocar el código.
**Criterio:** sobre (c), es lo que `D69` ya hizo y deja el agujero abierto en el código, no sólo en la prosa. Sobre (b), es más barato pero convierte el largo de la ventana en el criterio de cuánta verificación se exige, y no hay nada en `D28` ni en `D48` que sostenga eso: el riesgo de off-target de una ventana no sabe de qué corrida salió. Sobre (a), es la única que deja al código incapaz de recomendar una región no tamizada, que es la propiedad que se quería.
**Consecuencia — y acá está el límite:** el paso 1 **no se puede correr en esta máquina y queda PENDIENTE**, no nulo. Verificado el 2026-10-27: `%LOCALAPPDATA%\siFi2015\` no existe, `bowtie`/`bowtie-build`/`RNAplfold` no están en el PATH, no hay `RNA` ni `Bio` en el Python del sistema, y `work/` no existe, de modo que `tabla_alertas.py` no tiene su `work/m6_alertas/identidad_por_ventana.tsv` `[M]`. Los comandos exactos para cuando los insumos estén, desde la raíz y en `cmd.exe`:

```
python research\ola4\M6_alertas\scripts\identidad.py
python research\ola4\M6_alertas\scripts\tabla_alertas.py
python research\ola4\M6_alertas\scripts\compuerta.py
python research\ola4\M6_alertas\scripts\umbral_compuerta.py
```

Hasta que el paso 1 corra, la compuerta **queda como la dejó `D69`** y el agujero sigue declarado en `PREGUNTAS_ABIERTAS.md`. `[H]` La regla general que queda: una compuerta que no puede distinguir «verificado y limpio» de «sin verificar» no es una compuerta, es un registro — y la diferencia sólo se cierra exigiendo la presencia del dato, no su ausencia de alertas.

---

## D71 — La secuencia de `V-ATPase B` se recupera por homologia local, y el insumo deja de estar bloqueado
**Fecha:** 2026-10-27
**Quien:** el equipo, linea `O2` del plan de la ola 6, ejecutando la segunda via que el issue #22 abrio contra la clasificacion de `PLAN_CIERRE` §8.
**Decision:** `V-ATPase B` (`DM-02`) **deja de ser un insumo bloqueado**. El CDS vigente del gen para el proyecto es el que `research/ola6/O2_vatpase_b/scripts/02_extraer_cds.py` regenera en `resultados/VATPaseB_Dm_cds.fna` —no se versiona, porque `sin_secuencias.py` rechaza toda racha de 21 nt y el bloque versiona el generador y no el dato— y mide 1.503 nt, 500 aminoacidos, diez exones, locus `OZ319705.1`:38.943.269-38.957.327 del cromosoma 2 del ensamblado `ihDalMaid1.1`—, recuperado por alineamiento proteina-genoma con ortologia reciproca verificada. `O3` puede arrancar sin esperar el zip del investigador.
**Hecho que motivo la decision:** la ida con cinco proteinas de referencia da el mismo locus para las tres consultas de la subunidad B, de tres familias distintas, y loci distintos para las subunidades A y D, sin ningun competidor al 0,5 del mejor puntaje `[M]`. La vuelta —la proteina predicha en *D. maidis* contra los transcriptomas RefSeq completos de dos cicadelidos parientes— cae en `XM_054432770.1` de *Macrosteles quadrilineatus*, que es el ARNm que codifica la proteina con la que se habia hecho la ida y **el mismo que `C11` habia identificado** para esa familia, con identidad 1,0000 y sin rango 2; en *Homalodisca vitripennis* cae en `XM_046812795.1`, tambien subunidad B, con 0,9940 `[M]`. Y la via que el issue pedia tambien se corrio: los **tres** transcriptomas publicos contienen el gen, dos de ellos entero —`GHCC01013224.1` de Pergamino y `GITV01003502.1` de Ohio, los dos al 100 % de identidad sobre las 500 posiciones— y `GCWP01` partido en dos contigs que dejan sin cubrir las posiciones 145-264 `[M]`. Los dos CDS independientes, el del genoma y el del transcriptoma argentino, difieren en **3 nucleotidos de 1.503** y codifican la misma proteina letra por letra `[M]`.
**Alternativas consideradas:** (a) esperar el zip del investigador, que es lo que `PLAN_CIERRE` §8 suponia; (b) tomar el mejor acierto del genoma y seguir, sin la vuelta; (c) declarar la corrida pendiente porque en la maquina del issue no hay `tblastn` ni existe `work/C11/`; (d) la elegida, correr la homologia local con el otro alineador y exigir el reciproco.
**Criterio:** sobre (a), el gen estaba en disco desde antes y esperarlo era esperar un insumo que ya teniamos; el zip sigue valiendo, pero como verificacion y no como condicion. Sobre (b), `C5` midio que elegir el gen por el camino corto devolvio un gen distinto con 65 % de diferencia en el conteo de ventanas eficientes `[M]`, y aca el riesgo era concreto porque hay por lo menos tres subunidades del mismo complejo con proteina disponible. Sobre (c), «no pude buscar» no es «no esta»: faltaba BLAST+ y faltaba `work/`, pero `miniprot` —el otro alineador que el propio issue admitia, y el que ya usa `pipeline/`— estaba compilado, el ensamblado estaba indexado, y los tres TSA se bajan de su fuente publica en un comando. Sobre (d): tiene tres anclas que no se eligieron despues de ver el resultado. `Vha55` de *Drosophila* contra el mismo ensamblado da **0,9776** contra el **0,978** que `pipeline/resultados.json` ya tenia versionado; la subunidad D cae en el cromosoma 8, que es donde el proyecto ya habia puesto `ATPaseD_Dm`/`Vha36-1`; y la proteina predicha **no depende de con que se la busco** —la consulta de *Peregrinus maidis*, que difiere en 17 de 500 residuos de la de *Macrosteles*, da exactamente la misma proteina de 500 aa—, que es lo que descarta que el alineador este arrastrando residuos del query `[M]`.
**Consecuencia:** `O3` tiene su insumo y arranca. Hay que corregir dos clasificaciones: `PLAN_CIERRE` §8 trata este gen como «espera el transcriptoma» y la entrada 1 de la seccion de la ola 5 de `PREGUNTAS_ABIERTAS.md` como «puede salir del transcriptoma que va a mandar»; las dos quedan contestadas. La entrada 6 de la seccion de la ola 6 —«esta maquina no puede correr nada que necesite alineador»— vale para la maquina que se verifico y **no** para la de Luca, donde hay `miniprot` 0.18-r281 en WSL con el ensamblado indexado: antes de declarar una corrida imposible por entorno hay que decir en cual. Y queda una regla `[H]`: **la banda de concordancia se publica junto con el nombre del gen**, porque son dos cosas distintas y la segunda no se deduce de la primera: la proteina de *D. maidis* y la de *Macrosteles* son identicas en 500 de 500 posiciones mientras sus CDS comparten el 90,35 % de los nucleotidos y solo **136 de 1.483 ventanas de 21 nt** (9,17 %) `[M]`, asi que una ventana disenada sobre el pariente no se traslada y hay que disenar sobre esta secuencia.
**Lo que esta decision no hace:** no afirma nada sobre la eficacia del gen como blanco —el fenotipo de `DM-02` es de la fuente que el catalogo de `C5` registra leida completa, y es evidencia sobre la especie, no sobre esta secuencia `[R]`—, no cuenta las copias del gen en el genoma `[?]`, y no reemplaza una anotacion: los limites de exon son los que propuso el alineador, aunque el CDS del transcriptoma argentino, que si viene de ARN, da el mismo marco y la misma proteina `[M]`. La corrida con `tblastn` sobre las bases de `work/C11/` queda **sin hacer**, con su comando exacto escrito en `research/ola6/O2_vatpase_b/REPORT.md` §8 por si alguna vez se quiere el numero del otro algoritmo: los dos resuelven proteina contra nucleotido con intrones, pero sus identidades no son intercambiables `[?]`.
