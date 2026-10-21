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
