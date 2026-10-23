# M4 — Que evidencia distinguiria los dos modelos, y cuanta hace falta

**Ola 4, linea M4.** El investigador escribio que no asumiria todavia que la correccion de la
regla terminal mejora la prediccion de eficiencia, y propuso «conservar ambos modelos y pensar
que evidencia experimental permitiria compararlos» `[R]`
(`docs/plan_checkpoint2/salidas/F6_respuesta_y_cambios.md`). Esta linea contesta la segunda
mitad del pedido con numeros: **cuanta evidencia hace falta, de que tipo, y por que la que
tenemos no alcanza.**

**Las cuatro respuestas, en una linea cada una.**

1. Con el diseno de Cedden 2025 replicado tal cual hacen falta **232 siRNA** con eficacia medida
   para distinguir los dos modos con potencia 0,80 y alfa 0,05, ocho veces los 29 que existen
   `[M]`. Y hay un resultado mas fuerte que ese: con los 29 actuales la prueba **no puede
   rechazar nunca**, cualquiera sea el dato, porque los dos modos discrepan en **un solo**
   siRNA `[M]`.
2. Las fuentes de etiquetas publicas estan inventariadas abajo con su identificador y su
   licencia. Ninguna resuelve el problema: la unica del reino y la unidad correctos es la que ya
   usamos, y las grandes cambian de reino, de maquinaria y de via de entrega.
3. El ensayo que si discrimina no mide siRNA al azar: **elige** los discordantes. Pide **32
   siRNA por brazo** si la conclusion buscada es «silencian igual», con margen de 15 puntos
   porcentuales y desviacion de 20 `[M]`, y el repertorio de discordantes que ya tenemos contado
   alcanza para armarlo.
4. El analisis de la tercera via de M3 queda preregistrado en
   [`PREREGISTRO_tercera_via.md`](PREREGISTRO_tercera_via.md), escrito antes de que exista una
   sola etiqueta nueva.

**Decision del usuario, tomada el 2026-10-23.** El diseno de la seccion 3 **entra al entregable
del checkpoint 2 como la casilla de validacion**, declarando que el ensayo lo proponemos y no lo
corremos. Queda como D53.

---

## 1. Por que la comparacion no se puede hacer con lo que hay: no es falta de n, es falta de discordancia

La validacion retrospectiva preregistrada de C9 dejo las dos estimaciones sobre los 29 siRNA de
*Tribolium castaneum* de Cedden *et al.* 2025: rho = +0,142 con IC95 [−0,247, +0,492] para el modo
fiel y rho = +0,024 [−0,356, +0,397] para el corregido `[M]`
(`research/ola3/C9_sensibilidad_umbral/resultados/validacion_resumen.json`). La lectura obvia es
que los intervalos se solapan y que con n = 29 no hay potencia. La lectura obvia es correcta pero
se queda corta, y lo que falta es el punto de esta linea.

Las dos correlaciones **no son independientes**: se evaluan sobre los mismos siRNA, y por C1 de
`tools/sifi21_port/CAMBIOS.md` el modo corregido es un subconjunto estricto del fiel, de modo que
cada siRNA aporta a las dos. Cuando se mira de a pares en vez de por totales aparece el hecho que
gobierna todo lo demas: de los 29 siRNA, el modo fiel marca 5 como eficientes y el corregido 4,
y la clasificacion **difiere en uno solo**, `si778` `[M]`. Toda la diferencia entre rho = 0,142 y
rho = 0,024 —los 0,118 de brecha— sale de ese unico siRNA.

De ahi sale el resultado mas limpio de esta linea, y no necesita simulacion. La prueba correcta
para dos correlaciones dependientes con el mismo desenlace es una **aleatorizacion por
intercambio**: la hipotesis nula es que la etiqueta «fiel» o «corregido» pegada a cada
clasificacion es arbitraria respecto de la eficacia, y la aleatorizacion consiste en intercambiar,
siRNA por siRNA, los dos valores del predictor. Solo las filas discordantes cambian al
intercambiar. Con **k** discordantes el conjunto de aleatorizacion tiene 2^k elementos y el p mas
chico que admite es 2/2^k —la asignacion observada y su espejo— asi que **con k < 6 ningun dato
puede dar p ≤ 0,05**, por mucho que crezca el n total `[M]`. Con k = 1, que es el caso real, el p
exacto por enumeracion completa es **1,00** `[M]`.

Esto cambia la respuesta que conviene dar. La objecion no es «su validacion tiene poca muestra»,
sino **«su validacion no tenia forma de salir distinta»**: con un solo siRNA discordante, el
resultado era 1,00 antes de mirar los datos. Y no es una peculiaridad del conjunto de Cedden: es
lo que pasa siempre que dos criterios discrepan en una fraccion chica de los casos y la muestra es
chica. La tasa de discordancia medida entre los dos modos sobre los 29 siRNA es **3,45 %** `[M]`,
del mismo orden que el 14-24 % de C1 pero sobre un conjunto distinto —alla se contaban ventanas de
cuatro genes del corpus, aca siRNA elegidos por otros autores—, asi que las dos cifras no se
comparan directamente.

## 2. Cuantas etiquetas harian falta: 232, por remuestreo

El numero que pidio el investigador sale de remuestrear el propio conjunto de Cedden. El
procedimiento, implementado en [`scripts/potencia_dos_modelos.py`](scripts/potencia_dos_modelos.py)
y verificado con 25 pruebas en
[`scripts/test_potencia_dos_modelos.py`](scripts/test_potencia_dos_modelos.py), es: tomar las 29
filas como poblacion madre, sortear n filas con reposicion, correr sobre cada muestra la prueba de
aleatorizacion por intercambio con 999 permutaciones, y contar en que fraccion de 2000 muestras el
p queda en 0,05 o menos. Asi la tasa de discordancia, la proporcion de negativos y la restriccion
de rango del desenlace son las del dato real y no las de un supuesto.

| n de siRNA | Potencia | IC95 de la potencia |
|---|---|---|
| 29 (lo que existe) | 0,001 | [0,000, 0,004] |
| 58 | 0,017 | [0,012, 0,023] |
| 116 | 0,209 | [0,192, 0,227] |
| 174 | 0,570 | [0,548, 0,592] |
| 203 | 0,710 | [0,689, 0,729] |
| 217 | 0,770 | [0,751, 0,787] |
| 224 | 0,800 | [0,781, 0,817] |
| **232** | **0,824** | [0,806, 0,840] |

`[M]` (semilla 20261023, `resultados/potencia.json`). El n minimo que alcanza 0,80 es **232**, y la
busqueda lo localiza por duplicacion y biseccion, de modo que el 224 de la fila anterior ya esta en
el borde: cualquier numero entre 224 y 232 es defendible y **el redondeo honesto es «del orden de
230, no de 30»**.

Los dos numeros de la tabla que conviene llevar a la reunion no son el 232 sino los dos extremos.
Con los 29 que existen la potencia es **0,001**, o sea que el ejercicio de C9 tenia una chance en
mil de distinguir los modos aunque uno fuera bueno y el otro inutil. Y el 174 no es una fila
cualquiera: es exactamente el n al que la tasa de discordancia del 3,45 % produce, en promedio, los
**6 discordantes** que la cota combinatoria de la seccion 1 exige para que la prueba pueda rechazar
`[M]`. Las dos cuentas —una exacta y de una linea, otra por remuestreo— coinciden en el mismo orden
de magnitud, que es la clase de acuerdo que da confianza en el numero.

**Lo que este 232 es y lo que no.** Es el n necesario para distinguir los dos modos **replicando el
diseno de Cedden**: siRNA elegidos por los autores sin referencia a nuestra discordancia, con
mortalidad de larvas como desenlace y su misma restriccion de rango. No es el n de un ensayo
disenado para la pregunta, que es la seccion 3 y pide mucho menos. Y como todo remuestreo, hereda el
limite de su poblacion madre: hay **un solo** siRNA discordante en las 29 filas, asi que cada vez
que el sorteo lo elige reproduce su mismo desenlace. Eso invalida usar este mismo procedimiento
para estimar la potencia de un diseno que enriquezca discordantes —no habria variabilidad entre
ellos— y es la razon metodologica por la que la seccion 3 cambia de estadistico en vez de subir el
n. `[M]`

## 3. Las fuentes de etiquetas que existen, con lo que cada una cuesta

La tabla es el inventario pedido. Cada fila se abrio: la columna de identificador apunta a lo que
se leyo, y lo que no se pudo abrir esta marcado `[?]` y anotado en
`00_meta/PREGUNTAS_ABIERTAS.md` en vez de citarse.

| Fuente | Identificador | Licencia | Unidad y n | Lo que cuesta |
|---|---|---|---|---|
| Cedden *et al.* 2025 | DOI 10.1186/s12915-025-02219-6, PMC12039203 | CC BY 4.0 | 31 siRNA de 21 nt contra *Tc-gawky* (29 usables) y 3-4 ARNdc por gen en 8 genes de *Tribolium castaneum*; desenlace de supervivencia con razon de riesgo de log-rank | Es la que ya usamos. Coleoptero, no hemiptero; **un solo** siRNA discordante entre modos; restriccion de rango (24 de 29 positivos); y la prueba no es independiente de lo ya publicado, porque los autores analizaron sus propios descriptores sobre estos mismos siRNA `[R]` |
| Huesken *et al.* 2005 | DOI 10.1038/nbt1118 | no verificada `[?]` | 2431 siRNA sobre 34 ARNm humanos y de roedor, ensayo con reportero fluorescente | n de cuatro cifras, pero cambia de reino, de maquinaria y de via de entrega: celulas en cultivo con transfeccion, no insecto alimentado o inyectado. **No conseguimos un punto de descarga abierto**: los dos trabajos que la usan la citan al original sin enlace `[?]` |
| Reynolds, Vickers, Harborth y la compilacion de Shabalina, tal como las reporta Vert *et al.* 2006 | DOI 10.1186/1471-2105-7-520, PMC1698581 | CC BY 2.0 el articulo; los datos, no verificada `[?]` | 240, 76, 44 y 653 siRNA, todos humanos | Mismo salto de reino, y ademas son conjuntos de prueba chicos de un solo gen o dos en dos de los casos. El articulo que los compila no adjunta los datos `[?]` |
| siRecords, tal como lo reporta Thang *et al.* 2015 | DOI 10.1186/s12859-015-0495-2, PMC4379720 | CC BY 2.0 el articulo; la base, no verificada `[?]` | 2470 siRNA de eficacia «muy alta» y 2514 de eficacia «baja», humanos | Las etiquetas son **clases, no valores**: no hay eficacia continua, asi que sirve para una comparacion de clasificadores y no para una correlacion de rangos. No pudimos abrir la base original `[?]` |
| iBeetle-Base | DOI 10.1093/nar/gku1054, PMC4383896 | **CC BY-NC 4.0** | 5180 ARNdc distintos sobre 16.505 genes de *Tribolium castaneum*, con fenotipo anotado **por fragmento** y penetrancia | Es la unica fuente grande del reino correcto, y es la mas prometedora de la tabla. Pero el reactivo es un fragmento de ~479 pb, no un siRNA de 21 nt; el desenlace son terminos de ontologia y penetrancia en tramos, no una eficacia continua; la licencia excluye uso comercial; y **el articulo no dice si hay dos fragmentos independientes por gen**, que es justamente lo que haria falta para tener discordancia dentro de un mismo blanco `[?]` |
| Hemipteros | Jain *et al.* 2020, DOI 10.3390/insects11090557, PMC7564473 | CC BY 4.0 | 33 especies en 14 familias con silenciamiento publicado | **No hay dataset de eficacia por reactivo.** La revision resume por gen blanco y fenotipo, tipicamente con un ARNdc por gen, y no menciona ninguna base de eficiencia por siRNA o por ARNdc. Es la confirmacion de lo que suponiamos: para hemipteros no hay etiquetas, ni pocas ni muchas `[R]` |
| GenomeRNAi | genomernai.org | no verificada `[?]` | — | **No se pudo abrir** desde esta maquina (error de TLS). No se cita nada de su contenido `[?]` |

Dos lecturas de la tabla, las dos reportables.

**La primera es la respuesta directa al pedido.** Los 232 siRNA de la seccion 2 tienen que ser
siRNA con eficacia medida **en la unidad y el reino correctos**, y de esos hay 29 en el mundo
publico. Las fuentes grandes suman miles, pero ninguna sirve para la comparacion que el
investigador propone: las humanas cambian las tres cosas a la vez —reino, maquinaria y entrega— y
entran como `[?]`, utiles solo para preguntar si los terminos de si-Fi21 tienen **alguna** senal,
no para elegir entre dos variantes que difieren en una rama; y la grande del reino correcto cambia
la unidad del reactivo. **Con datos abiertos, el numero necesario es inalcanzable hoy.** Ese era el
riesgo declarado de esta linea y se cumplio, y es una respuesta: los dos modelos no son
distinguibles con la evidencia existente. `[M]` para el 232, `[H]` para la lectura.

**La segunda es una linea de trabajo que no habiamos visto.** iBeetle-Base es la unica fuente que
combina el reino correcto con n de cuatro cifras y resultado por reactivo, y la pregunta que
decide si sirve es chica y verificable: **si la base guarda dos fragmentos no solapados por gen**.
Si los guarda, hay pares de reactivos contra el mismo blanco con desenlaces independientes, que es
la estructura que la seccion 1 muestra como necesaria; y si no los guarda, se cierra la linea en una
tarde. Queda en `00_meta/PREGUNTAS_ABIERTAS.md` como pendiente con esa formulacion exacta. `[H]`

## 4. El ensayo prospectivo minimo que discrimina

Esta es la parte que contesta lo que el investigador pregunto de verdad, porque no depende de que
aparezcan etiquetas: se disena para generar las que hacen falta, y nada mas que esas.

**La idea, en una frase.** Los dos modelos difieren en un conjunto identificable y ya contado —19,
7, 50 y 8 ventanas en `MP_MRFV`, `CP_MRFV`, `BicC_Dm` y `ATPaseD_Dm` son eficientes en modo fiel y
no en corregido, y ninguna va en sentido contrario `[M]` (C1 de `CAMBIOS.md`)— asi que medir siRNA
al azar es tirar la mayor parte del esfuerzo a casos en los que los dos modelos dicen lo mismo. El
ensayo **elige** los discordantes. Es el mismo truco que la seccion 1 identifico como el cuello de
botella, aplicado al reves: en vez de esperar que la discordancia aparezca al 3,45 %, se la lleva al
100 % por diseno.

**Brazos.** Cuatro, sobre **un solo gen** para que el gen no confunda nada, y `BicC_Dm` es el
candidato porque es el que mas discordantes tiene (50 de las 84).

- **A, discordantes.** Eficientes en modo fiel y rechazados en corregido; todos de la rama de
  `sifi_pipeline.py:535-541`, que es por donde entran los 84.
- **B, concordantes eficientes.** Eficientes en los dos modos.
- **C, concordantes rechazados.** Rechazados por los dos. No es decorativo: es el **control de
  validez interna** del ensayo. Si el ensayo no separa B de C, no puede decir nada sobre A, y esa
  comparacion se mira **antes** que la de A, como condicion para interpretar el resultado.
- **D, control negativo.** Secuencia no dirigida, del tipo del dsmGFP que usa Cedden.

**Variable de respuesta.** El silenciamiento del transcrito blanco, medido como reduccion
porcentual respecto del control negativo, no la mortalidad. Dos razones: el criterio de si-Fi21
predice carga de la hebra guia y accesibilidad del sitio, que es silenciamiento y no letalidad; y
la mortalidad agrega la variabilidad del fenotipo encima de la del reactivo, que es parte de por
que el desenlace de Cedden atenua tanto. La mortalidad puede ir como desenlace secundario.

**La unidad de analisis es el siRNA, no la replica.** La hipotesis es sobre clases de siRNA, asi
que el n que importa es cuantas **secuencias distintas** hay por brazo, con sus replicas
biologicas dentro de cada una. Confundir las dos cosas es la forma habitual de inflar la potencia
de un diseno asi, y conviene dejarlo escrito antes de que alguien proponga tres siRNA con diez
replicas.

**Tamano de muestra.** El estadistico ya no es una correlacion: es un contraste entre dos grupos
de siRNA, y la cuenta correspondiente es la t de dos muestras, exacta por t no central. La tabla da
el n **por brazo** segun la diferencia que se quiera detectar y la dispersion entre siRNA de una
misma clase, las dos en puntos porcentuales de silenciamiento `[M]`:

| Dispersion entre siRNA (pp) | Diferencia 20 pp | 30 pp | 40 pp |
|---|---|---|---|
| 15 | 11 | 6 | 4 |
| 20 | 17 | 9 | 6 |
| 25 | 26 | 12 | 8 |

Con alfa 0,025 por las dos comparaciones planificadas (A contra B, y B contra C) los numeros son
13, 7, 5 / 21, 10, 7 / 31, 15, 9 `[M]`. Como sensibilidad, con analisis por rangos
(Mann-Whitney) en vez de la t, la potencia en esos mismos n baja a 0,79, 0,80 y 0,83 para
dispersion 20, o sea que el analisis no parametrico **no obliga a cambiar el n** `[M]`.

**Pero el tamano que manda es el otro, y es la parte metodologica que no hay que pasar por alto.**
El resultado interesante del ensayo es el que dice «los discordantes silencian **como** los
concordantes», y eso es una afirmacion de **equivalencia**: no rechazar una diferencia no es
mostrar que no la hay, y con muestras chicas lo primero pasa casi siempre. La prueba que
corresponde es de equivalencia con margen declarado (dos pruebas unilaterales), y cuesta mas
muestra `[M]`:

| Dispersion entre siRNA (pp) | Margen 10 pp | 15 pp | 20 pp |
|---|---|---|---|
| 15 | 40 | 18 | 11 |
| 20 | 70 | **32** | 18 |
| 25 | 108 | 49 | 28 |

**El numero que se propone es 32 siRNA por brazo**, que corresponde a dispersion 20 pp y margen 15
pp: un margen de 15 puntos porcentuales de silenciamiento es la diferencia mas chica que todavia
cambiaria la decision de diseno, y 20 pp de dispersion entre siRNA de una misma clase es el
supuesto que hay que revisar primero con los datos del propio ensayo. Los dos valores son
supuestos nuestros, no mediciones: la dispersion entre siRNA no la tenemos medida en ningun
sistema comparable, y si en el ensayo resulta 25 pp el n necesario sube a 49. `[H]`

**El repertorio alcanza, y eso no era obvio.** 32 discordantes por brazo contra las 50 ventanas
discordantes de `BicC_Dm` deja margen para descartar por solapamiento, por contenido GC o por
off-targets, y si no alcanzara se completan con las 19 de `MP_MRFV`, al costo de agregar el gen
como variable `[M]`.

**Ciego y asignacion.** Quien corre el bioensayo y quien mide el transcrito reciben los siRNA
codificados, sin la clase. La correspondencia entre codigo y brazo queda en manos de una persona
que no participa de la medicion y se abre **despues** de cerrar los datos. La posicion en placa se
sortea, porque el efecto de borde es el confusor clasico de este tipo de medicion. El analisis es
el preregistrado: la comparacion B contra C primero como condicion de interpretabilidad, despues
A contra B por equivalencia con el margen de 15 pp, y nada mas.

**El resultado que falsa cada cosa.** Las tres salidas estan fijadas de antemano, que es lo que
hace que el ensayo sea una prueba y no una ilustracion.

- **Si A es equivalente a B** (la prueba de equivalencia rechaza las dos unilaterales con margen
  de 15 pp): la rama terminal del original **no infla nada** y nuestro modo corregido esta
  descartando entre el 14 % y el 24 % de diseños buenos. Habria que revisar C1, y el modo por
  defecto del entregable deberia volver a ser el fiel.
- **Si A silencia menos que B**, con la diferencia por debajo de −15 pp: la rama infla, la
  correccion vale, y los 84 casos del corpus son falsos positivos del original.
- **Si ninguna de las dos**: no concluyente, y se reporta con el n que habria hecho falta segun la
  dispersion observada. Es el resultado que hay que estar dispuesto a publicar.

**Lo que el ensayo no resuelve.** Es *Dalbulus maidis* o el sistema que el laboratorio pueda
correr, pero sigue siendo **un gen**: generaliza a la rama, no a la especie. No mide nada sobre
off-targets ni sobre persistencia ambiental. Y no lo corremos nosotros: el equipo no tiene
laboratorio, asi que esto es una propuesta de diseno con su cuenta hecha, no un compromiso de
ejecucion.

## 5. Lo que se entrega

| Archivo | Que es |
|---|---|
| `scripts/potencia_dos_modelos.py` | La cuenta de potencia: remuestreo, prueba de aleatorizacion por intercambio, enumeracion exacta, y las cuentas de dos grupos y de equivalencia. Corre sin insumos nuevos |
| `scripts/test_potencia_dos_modelos.py` | 25 verificaciones. Las anclas: reproduce los rho de C9 (+0,142 y +0,024), reproduce el valor de libro de la t de dos muestras (17 por grupo), y la cota combinatoria coincide con la enumeracion exhaustiva para k de 1 a 8 |
| `resultados/potencia.json` | Todas las cifras de este reporte, con su semilla |
| `PREREGISTRO_tercera_via.md` | El plan de analisis de M3, escrito antes de que exista una etiqueta nueva |

**Que no se hizo, y por que.** No se ajusto ningun modelo: con 29 etiquetas y seis terminos no se
ajusta nada, y es la razon por la que M3 entrega una tabla y no un modelo. No se bajo ni se
reproceso ninguna de las fuentes de la seccion 3: la linea pedia inventariarlas con su costo, y
bajar la de Huesken no cambiaria el hecho de que es otro reino. No se toco el motor de eficiencia,
que en esta maquina no esta disponible.

## 6. Limites

El 232 depende de la poblacion madre: es el n para replicar el diseno de Cedden, y un conjunto con
otra tasa de discordancia o menos restriccion de rango daria otro numero. La cota de los 6
discordantes es exacta y no depende de nada, pero vale para esta prueba de aleatorizacion: otra
prueba tendria otra cota, y cualquier prueba que diera p ≤ 0,05 con un solo caso discordante
estaria suponiendo algo que el dato no tiene. Los dos supuestos del tamano de muestra del ensayo
—dispersion 20 pp, margen 15 pp— son nuestros y estan marcados `[H]`: el primero se revisa con el
propio ensayo, el segundo es una decision de diseño que conviene discutir con quien vaya a correrlo.
La licencia de iBeetle-Base es CC BY-NC, de modo que cualquier uso con fines comerciales queda
fuera. Y el ensayo mide silenciamiento en un gen: no dice nada sobre eficacia en campo, sobre
especies no objetivo ni sobre resistencia.
