# El ranking de los cuatro candidatos de EPILAB, y el criterio con el que se armó

Fecha: 2026-10-20. Reproducible con `tools/sifi21_port/ranking.py`; los números que
cita este documento están en `ranking.json`, `nulo_region.json` y `azar_por_k.json`,
en esta misma carpeta. La cuenta de azar por tamaño de ventana está en
[`azar_por_k.md`](azar_por_k.md) y el cotejo de las tres herramientas en
[`benchmark_tres_herramientas.md`](benchmark_tres_herramientas.md).

---

## El resultado, en un párrafo

El orden es **`MP_MRFV` > `CP_MRFV` > {`BicC_Dm`, `ATPaseD_Dm`}**, y lo que aguanta
el barrido de pesos es la primera mitad: `MP_MRFV` sale primero en entre el 76 % y
el 100 % de los 2.000 juegos de pesos según la combinación de reglas, `CP_MRFV`
sale segundo en entre el 76 % y el 100 %, y **los dos genes del insecto no se
distinguen entre sí**: su orden relativo se da vuelta con los pesos y cada uno
ocupa el tercer puesto en alrededor de la mitad de los sorteos. Decir «`BicC_Dm` es
tercero» sería reportar una elección de pesos, no una medición. Lo que sí separa a
los dos del insecto de los dos virales no es el puntaje sino una compuerta: **las
regiones elegidas de `BicC_Dm` y `ATPaseD_Dm` contienen ventanas con coincidencia
perfecta de 21 nt en el transcriptoma de *Homalodisca vitripennis***, un cicadélido
no objetivo, y las dos virales no contienen ninguna. Y dentro de cada gen del
insecto hay regiones alternativas que escapan a esa compuerta y además son más
eficientes: `BicC_Dm` 2123-2422 (37 ventanas eficientes contra 20, y cero
coincidencias de 21 nt contra 22) y `ATPaseD_Dm` 72-371 (21 contra 18, cero contra
3). **La recomendación operativa no es cambiar de gen: es mover la región dentro
del gen, en los dos genes del insecto.**

Y esa recomendación no es cosmética: **si se acepta, el orden cambia**. Con las
regiones recomendadas el ranking pasa a ser `MP_MRFV` > `BicC_Dm` > `CP_MRFV` >
`ATPaseD_Dm` en entre el 89,7 % y el 100 % de los sorteos, porque `BicC_Dm` mejora
mucho en los dos ejes a la vez y salta de pelear el último puesto a quedar segundo
(§2.3).

> **Qué de todo esto es medición y qué es nuestra decisión.** Son medición: los
> conteos de ventanas eficientes, los de ventanas con coincidencia en cada
> referencia, los percentiles, los nulos y la cuenta de azar. Son decisión nuestra,
> discutible y declarada: que el riesgo de una ventana sea su **peor** acierto y no
> la suma; que los ejes se combinen con **media geométrica** y no con suma; que una
> coincidencia perfecta de 21 nt sea un **veto** y no una penalización; los **pesos
> por referencia**; y que los dos genes virales y los dos del insecto se presenten
> en **rankings separados**. Cada una de esas cinco está argumentada abajo con lo
> que se gana, lo que se pierde, y cómo cambia el orden si la decisión fuera la
> contraria.

---

## 1. La adjudicación del 7,2 %: no es una contradicción, es una diferencia de nulo

Teníamos dos mediciones propias apuntando en direcciones opuestas.
`pipeline/REPORT.md` §6 dice que elegir la mejor región de 300 pb dentro de un gen
mejora alrededor del 7,2 % sobre el promedio del gen y que **no es significativo en
0 de 20 genes** contra un modelo nulo, de donde concluye que lo que discrimina es
qué gen se ataca y no qué región. `sifi21_reproduccion.md` §3 dice que las cuatro
regiones de EPILAB están entre un 19 % y un 46 % por debajo del óptimo por densidad
de ventanas eficientes, lo que presupone que la región sí discrimina. Si el ranking
recomendara mover `BicC_Dm` sin resolver esto, el flanco quedaría abierto.

### 1.1 El nulo del 7,2 % sí es reproducible, y lo que mide es más angosto de lo que parece

El registro apuntaba a `region_scoring.py`, donde la palabra «nulo» no aparece. Está
en otro lado: **`baseline_dsrip/region_nulo_multigen.py`**. Tiene las rutas de
entrada escritas a mano contra una máquina que ya no existe (`C:\Proyectos\yHat\…`),
así que no corre tal cual, pero el método está completo y con las rutas corregidas
reproduce el número publicado: ganancia mediana **7,2 %** sobre 20 genes y **0 de
20** con p < 0,05. `[E]`

Reproducirlo deja ver tres cosas sobre qué es ese nulo, y la tercera es la que
adjudica:

Primero, el estadístico no es el conteo de ventanas eficientes sino **la media del
puntaje biofísico** de la región, promediada sobre unas 280 ventanas. Un promedio
sobre 280 valores tiene un rango dinámico chico por construcción, y una ganancia del
7,2 % sobre un promedio así no es comparable con una ganancia sobre un conteo por
umbral. No son la misma cantidad. `[E]`

Segundo, el observado se barre con paso 5 y el nulo con paso 20, o sea que el máximo
observado se busca en una rejilla cuatro veces más fina que el máximo nulo. Esa
asimetría favorece al observado. Corregida —paso 5 de los dos lados— el veredicto no
cambia: sigue siendo **0 de 20**, y la mediana del z baja de 0,60 a 0,43. El
resultado negativo es robusto a su propio defecto de método. `[E]`

Tercero, y es lo que importa: el nulo es una **permutación de bloques contiguos de
30 ventanas**. Permutar bloques de 30 reordena los grupos pero **conserva intacta la
estructura local dentro de cada bloque**. Si las ventanas eficientes se agrupan en
rachas de menos de 30 —que es justamente lo que un perfil «con subiditas y
bajaditas» significa—, este nulo reproduce esas rachas y por lo tanto **no tiene
poder para detectarlas**. El 7,2 % no significativo es, entonces, una afirmación
sobre el nulo tanto como sobre la biología. `[H]`

### 1.2 La medición que faltaba: el percentil de la región elegida en su propio gen

El lado de si-Fi21 no tenía nulo de ninguna clase. Construirlo es barato porque el
perfil por ventana ya existe: para cada gen se calcula el conteo de eficientes sobre
**todas** las regiones deslizantes del largo que usó EPILAB y se ubica en esa
distribución la región elegida.

| Gen | Largo | Regiones posibles | Elegida | **Percentil** | Mínimo | p25 | Mediana | p75 | Máximo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `MP_MRFV` | 200 | 1.044 | 30 | **90,9** | 8 | 13 | 19 | 26 | 38 |
| `CP_MRFV` | 200 | 309 | 17 | **48,5** | 5 | 9 | 18 | 19 | 21 |
| `BicC_Dm` | 300 | 2.201 | 20 | **44,1** | 3 | 14 | 21 | 26 | 37 |
| `ATPaseD_Dm` | 300 | 172 | 18 | **45,3** | 17 | 17 | 19 | 23 | 24 |

`[E]` **Esto reencuadra el hallazgo de §3 de `sifi21_reproduccion.md`.** Decir que
`MP_MRFV` 1-200 está «un 21 % por debajo del óptimo» es cierto y es engañoso: esa
región está en el **percentil 91** de su propio gen, o sea que es mejor que nueve de
cada diez regiones de 200 nt que se podrían haber elegido. Las otras tres están
alrededor de la mediana, es decir que **no se distinguen de haber elegido al azar
dentro del gen**, que es una afirmación mucho más precisa —y más falsable— que un
porcentaje contra un óptimo.

Los cuartiles agregan algo que el mínimo y el máximo solos esconden, y es cuánto
margen hay en cada gen. **`ATPaseD_Dm` es el caso extremo: todo su gen va de 17 a 24
ventanas eficientes**, con el cuartil 25 pegado al mínimo. Ahí la elección de región
casi no mueve la aguja se elija como se elija, de modo que discutir cuál es la mejor
región de ese gen por densidad es discutir sobre un rango de 7 ventanas. En
`BicC_Dm`, en cambio, el rango va de 3 a 37 y el margen es real. `[E]`

El porcentaje contra el óptimo no es falsable porque el óptimo está sesgado hacia
arriba por construcción: es un máximo sobre cientos de regiones superpuestas. Cuánto,
se mide. Barajando la etiqueta de «eficiente» entre todas las ventanas del gen
—conservando cuántas hay y destruyendo dónde están— el máximo sigue quedando muy por
encima de la media, sólo por el efecto de maximizar:

| Gen | Ganancia del máximo observada | Ganancia del máximo bajo azar puro | Resto |
|---|---:|---:|---:|
| `MP_MRFV` | 89,1 % | 42,6 % | 46,5 % |
| `CP_MRFV` | 41,8 % | 36,5 % | 5,3 % |
| `BicC_Dm` | 80,5 % | 46,3 % | 34,2 % |
| `ATPaseD_Dm` | 21,9 % | 17,0 % | 4,9 % |

`[E]` **Entre la mitad y casi toda la «brecha contra el óptimo» es artefacto de
maximizar sobre regiones superpuestas**, no señal. En `CP_MRFV` y `ATPaseD_Dm` casi
todo lo es.

### 1.3 Los dos nulos sobre el mismo dato, que es lo que cierra la cuestión

Sobre los cuatro genes, con el mismo estadístico —el máximo del conteo de eficientes
por región— y 2.000 repeticiones, se corren los dos nulos: el de barajar la etiqueta
entre ventanas, que destruye toda la estructura local, y el de permutar bloques de
30, que es exactamente el del 7,2 %.

| Gen | Máximo observado | Nulo de etiquetas | z | p | Nulo de bloques de 30 | z | p |
|---|---:|---:|---:|---:|---:|---:|---:|
| `MP_MRFV` | 38 | 28,2 | 4,33 | **0,0020** | 35,3 | 0,66 | 0,2695 |
| `CP_MRFV` | 21 | 16,0 | 3,04 | **0,0070** | 19,0 | 0,76 | 0,2950 |
| `BicC_Dm` | 37 | 30,0 | 2,92 | **0,0110** | 37,6 | −0,15 | 0,5640 |
| `ATPaseD_Dm` | 24 | 21,6 | 1,35 | 0,1450 | 23,9 | 0,04 | 0,5910 |

`[E]` **Con el nulo de etiquetas, el efecto de región resiste en 3 de 4 genes. Con
el nulo de bloques de 30, en 0 de 4 — exactamente el mismo veredicto que el 7,2 %,
ahora sobre nuestros genes y con nuestro estadístico.**

Ésa es la adjudicación, y no es que una de las dos mediciones esté mal: **las dos
están bien y contestan preguntas distintas.** El nulo de etiquetas contesta «¿las
ventanas eficientes están agrupadas?», y la respuesta es sí. El nulo de bloques
contesta «dado que están agrupadas en rachas de ese tamaño, ¿el mejor grupo es mejor
que otro grupo?», y la respuesta es no. Para la decisión que tenemos entre manos
—elegir una región dentro de un gen— la pregunta relevante es la primera, porque lo
que se sintetiza es una región y lo que se cuenta es cuántos efectores produce; pero
la segunda explica por qué la ventaja esperable de afinar la región es modesta.

### 1.4 Los dos puntajes sobre los mismos genes

`pipeline/resultados.json` registra que `BicC_Dm` y `ATPaseD_Dm` caen en loci del
mapeo, así que sobre las mismas regiones se puede calcular el puntaje biofísico del
pipeline y la densidad de eficientes de si-Fi21 y correlacionarlos.

| Gen | Regiones comparadas | Regiones independientes | Spearman | Pearson |
|---|---:|---:|---:|---:|
| `MP_MRFV` | 1.044 | 6,2 | **0,491** | 0,475 |
| `CP_MRFV` | 309 | 2,5 | −0,554 | −0,604 |
| `BicC_Dm` | 2.201 | 8,3 | **0,632** | 0,665 |
| `ATPaseD_Dm` | 172 | 1,6 | 0,638 | 0,634 |

La columna que hay que mirar primero es la tercera. Las regiones deslizantes se
superponen casi del todo, así que el número de observaciones independientes es el
largo del gen dividido el largo de la región, no las cientos que se promedian. Con
1,6 y 2,5 regiones independientes, los valores de `ATPaseD_Dm` y `CP_MRFV` **no son
interpretables** y no se usan; por eso tampoco se reporta ningún valor p, que sobre
estos pares no significaría nada. `[E]`

En los dos genes donde la comparación tiene algo de poder —`BicC_Dm` con 8,3 y
`MP_MRFV` con 6,2— las dos mediciones **correlacionan positivamente y de forma
moderada**, ρ = 0,63 y 0,49. `[H]` Es decir: no se contradicen, una es sustituta
imperfecta de la otra, y la discrepancia aparente entre §6 del pipeline y §3 de
`sifi21_reproduccion.md` se explica entera por el nulo y por el sesgo del máximo, sin
necesidad de que ninguna de las dos mediciones esté equivocada.

**Consecuencia sobre el ranking, que es lo que esta tarea tenía que entregar:** el
ranking **no** apoya la recomendación de mover una región en la ganancia de densidad,
porque esa ganancia no sobrevive al nulo conservador y la mitad es artefacto. La
apoya en el eje de exposición a no objetivo, donde la diferencia no es un máximo
sobre regiones superpuestas sino la presencia o ausencia de un hecho discreto: una
coincidencia perfecta de 21 nt. Queda registrado como **D15** en
`00_meta/DECISIONS.md`.

---

## 2. Cómo se construye el orden

Dos ejes por candidato, los dos como tasas sobre las ventanas de la región, que es
lo que los hace comparables entre regiones de 200 y de 300 nt:

- **Eficacia**, la fracción de ventanas de la región que si-Fi21 marca como
  eficientes, en modo corregido con ViennaRNA 2.7.2 y contadas «en contexto» (la
  región dentro del gen entero, no recortada y plegada sola; la diferencia entre las
  dos llega al 47 % y está medida en `sifi21_reproduccion.md` §2).
- **Limpieza**, la fracción de ventanas limpias, descontando cada ventana sucia en
  proporción a la gravedad de su peor acierto contra el panel de no objetivo.

### 2.0 Con qué se calcula cada eje, y qué le cambiamos a si-Fi21

El eje de eficacia sale de **si-Fi21**, que es la referencia declarada del
laboratorio. El problema práctico es que es una aplicación Qt4 en Python 2.7, corre
sólo en Windows, abre diálogos modales en medio del cálculo y no es automatizable, de
modo que no sirve como dependencia de un pipeline. Lo portamos a Python 3 sin
interfaz, con **dos modos a propósito**, y lo que sigue es lo que cambia respecto del
original, con el efecto medido. El detalle está en `tools/sifi21_port/CAMBIOS.md` y en
`sifi21_reproduccion.md`; acá va lo que hace falta para leer los números de este
documento.

| Qué | Por qué | Efecto medido |
|---|---|---|
| **Modo fiel**, que reproduce si-Fi21 tal cual, defectos incluidos | Sin él no hay contra qué comparar: los conteos de la planilla se hicieron con el original, y auditarlos exige poder correrlo | Reproduce **los cuatro conteos exacto** —42, 32, 133 y 212— y la curva del «RNAi design plot» tramo por tramo `[E]` |
| **Modo corregido**, que arregla la regla de los nucleótidos terminales | Esa regla **no es un filtro, es una ramificación**: una de sus cuatro ramas devuelve «eficiente» mirando sólo la accesibilidad, sin el veredicto termodinámico | Entre el **14 % y el 24 %** de lo que el original cuenta como eficiente entra por ahí: 19 de 133, 7 de 32, 50 de 212 y 8 de 42. Las 84 diferencias caen **todas** en esa rama y ninguna va en sentido contrario `[E]` |
| **Conteo «en contexto»**, no sobre la región recortada y plegada sola | La accesibilidad depende del plegado local; un fragmento recortado pierde el contexto que apareaba o liberaba su extremo | La diferencia llega al **47 %** en `MP_MRFV`: 16 eficientes aislada contra 30 en contexto. Si se comparan regiones, hay que fijar el procedimiento `[E]` |
| **Tamizaje de off-targets propio**, por coincidencia exacta con Aho-Corasick en vez de BLAST | Para bloques perfectos la coincidencia exacta es la respuesta correcta y no una heurística | Coincide con BLAST+ local en las **20 celdas** de los criterios de bloque perfecto; en el de un desajuste **no**, y el exacto encuentra hasta **tres veces más** `[E]` |
| **Tamaño de ventana parametrizable** (`--size`) | Hacía falta para la cuenta de azar por *k* de §5 y el código lo tenía fijo en 21 | Con el valor por defecto la salida es **idéntica byte a byte** a la de antes de parametrizar, verificado en esta corrida `[E]` |

Con eso, elegir región es un barrido: para cada gen se calcula el conteo de ventanas
eficientes de **todas** las regiones deslizantes del largo que usó EPILAB, se
descartan las que contienen alguna ventana idéntica en 21 nt a una referencia no
objetivo, y se ordena lo que queda. **Por eso la región más densa no siempre es la que
proponemos**, y el único caso donde difieren es `ATPaseD_Dm`.

Con los pesos base, y contando todas las ventanas (regla conservadora de D2):

| Candidato | Región | Ventanas | Eficientes | Eficacia | Exposición | Limpieza | Eficientes y limpias | ¿Vetada? |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `MP_MRFV` | 1-200 | 200 | 30 | 0,1500 | 0,0198 | 0,9802 | 29 | no |
| `CP_MRFV` | 201-400 | 200 | 17 | 0,0850 | 0,0069 | 0,9931 | 17 | no |
| `BicC_Dm` | 264-563 | 300 | 20 | 0,0667 | 0,0666 | 0,9334 | 17 | **sí** |
| `ATPaseD_Dm` | 151-450 | 300 | 18 | 0,0600 | 0,0196 | 0,9804 | 14 | **sí** |

### 2.1 El barrido de pesos, que es el resultado y no el orden puntual

Se sortean 2.000 juegos de pesos: el reparto entre los dos ejes uniforme en [0,1]
—que es Dirichlet(1,1) sobre el símplex de dos—, los pesos de las seis referencias
Dirichlet uniforme sobre su símplex, y los tres criterios de riesgo Dirichlet
uniforme **ordenado de mayor a menor**. Lo último es en sí una decisión: deja libres
las magnitudes pero impone lo único que la evidencia sostiene, que un bloque
perfecto más largo no puede ser menos riesgoso que uno más corto.

Frecuencia de cada candidato en cada posición, sobre las combinaciones de forma de
combinación, regla de D2 y escala de normalización:

| Combinación | `MP_MRFV` | `CP_MRFV` | `BicC_Dm` | `ATPaseD_Dm` |
|---|---|---|---|---|
| geométrica / conservadora / absoluta | **99**/1/0/0 | 1/**99**/0/0 | 0/0/75/25 | 0/0/25/75 |
| geométrica / conservadora / min-max | **76**/14/6/5 | 24/**76**/0/0 | 0/8/42/50 | 0/2/52/45 |
| geométrica / mecanicista / absoluta | **100**/0/0/0 | 0/**100**/0/0 | 0/0/100/0 | 0/0/0/100 |
| geométrica / mecanicista / min-max | **79**/11/6/4 | 21/**79**/0/0 | 0/10/90/0 | 0/0/4/96 |
| suma / conservadora / absoluta | **91**/7/2/0 | 9/**91**/0/0 | 0/0/25/75 | 0/2/72/25 |
| suma / conservadora / min-max | **76**/13/9/3 | 21/**78**/1/0 | 0/0/12/88 | 3/8/79/9 |
| cascada (veto + eficientes limpias) | **100**/0/0/0 | 0/**100**/0/0 | vetada | vetada |

`[E]` Lo que sobrevive a todo el barrido:

1. **`MP_MRFV` primero**, entre el 76 % y el 100 % de los sorteos según la
   combinación, y nunca por debajo del 76 %.
2. **`CP_MRFV` segundo**, entre el 76 % y el 100 %.
3. **`BicC_Dm` y `ATPaseD_Dm` no se ordenan entre sí.** En la combinación geométrica
   con min-max se reparten el tercer puesto 42 a 52; con suma y escala absoluta se
   da vuelta y `ATPaseD_Dm` queda tercero el 72 % de las veces. Su orden relativo
   **es la elección de pesos**, no una propiedad de los candidatos.

Esto es exactamente lo que el antecedente de `pipeline/REPORT.md` §5 advertía: ahí,
119 de 124 candidatos llegaron al top-10 por una elección de pesos que nadie había
justificado. Acá, con cuatro candidatos, lo defendible son los dos primeros puestos
y el empate de los dos últimos.

> **Una nota de método que impide leer de más un número de arriba.** En los rankings
> por estrategia, que tienen dos candidatos cada uno, la escala min-max da 50 % / 50 %
> exacto. **No es un empate medido: es la escala.** Con dos candidatos, min-max
> manda uno a 0 y el otro a 1 en cada eje, de modo que si se ordenan al revés en los
> dos ejes el resultado es una moneda, cualquiera sea la magnitud de la diferencia.
> Está fijado como prueba en `test_ranking.py` para que nadie lo cite como hallazgo.
> Para los rankings de dos candidatos vale la escala absoluta, y los números están
> en D5.

#### 2.1 bis · Corrección de lectura (2026-10-21): la diagonal de B.3 mide la escala, no la robustez del orden

El cálculo de arriba no cambia. Lo que se corrige es cómo se leyó el gráfico B.3 del `index.html`,
cuyo pie decía ~~«la diagonal se arma sola: cada candidato ocupa una posición distinta en el 99 % o
más de los sorteos»~~, que sin la escala al lado se lee como robustez del orden. **Lectura
corregida:** la diagonal sale de que los pesos de cruce de los tres pares en conflicto se corren
al borde del rango (w* ≈ 0,02), y **no de que un candidato domine a otro**: en los dos paneles
hay 3 pares en conflicto de 6. Con las regiones de EPILAB hay un cruce adentro del rango, `BicC_Dm`
contra `ATPaseD_Dm` en w* = 0,32, que es el bloque 75/25 de A.3. `[E]` Fuente: auditoría propia
sobre `ranking.json`, registrada en `00_meta/PREGUNTAS_ABIERTAS.md` (pendientes internos); **los
números de esta subsección no se volvieron a medir en la sesión que la escribió**.

| Orden modal | Escala absoluta | Escala min-max |
|---|---|---|
| Regiones propuestas, geométrica / conservadora | `MP > BicC > CP > ATPaseD` en el 98,7 % | cae al 33,7 %, con 14 órdenes distintos; `MP_MRFV` pasa de primero a tercero |
| Tres de las cuatro variantes absolutas | coincide exactamente con el orden por eficacia sola | — |
| `suma / conservadora / absoluta`, regiones de EPILAB | `MP > CP > ATPaseD > BicC` en el 65,9 % | — |

**Cota de palanca de la limpieza.** Entre candidatos la eficacia varía un factor 2,38–2,50 y la
limpieza 1,015–1,064. El piso duro de la limpieza, con cualquier sorteo de pesos, es 1 menos la
fracción de ventanas de la región con algún off-target, que da 0,8533 en el peor caso
(`BicC_Dm`, regiones de EPILAB). Por eso el sorteo de pesos **sólo puede dar vuelta un par que ya
esté casi empatado en eficacia**; en los demás pares es inerte por construcción. `[E]` La figura
que lo muestra es `barrido_escala.png`. La sensibilidad de la región recomendada a los umbrales
de si-Fi21 es otra cuestión y está en `research/ola3/C9_sensibilidad_umbral/REPORT.md`.

### 2.2 Nivel 2: la región dentro de cada gen

Acá el ranking deja de ser un ejercicio y pasa a ser una recomendación. Para cada
gen se barren todas las regiones deslizantes del mismo largo y se comparan con la
elegida.

| Gen | Región elegida | Percentil | ¿Vetada? | Mejor alternativa sin veto | Eficientes | Con off-target | Con 21/21 |
|---|---|---:|---|---|---:|---:|---:|
| `MP_MRFV` | 1-200 | 90 | no | 72-271 | 38 (contra 30) | 9 | 0 |
| `CP_MRFV` | 201-400 | 44-49 | no | 99-298 | 21 (contra 17) | 5 | 0 |
| `BicC_Dm` | 264-563 | 16-38 | **sí** | **2123-2422** | **37 (contra 20)** | 6 | **0 (contra 22)** |
| `ATPaseD_Dm` | 151-450 | 9-40 | **sí** | **72-371** | **21 (contra 18)** | 12 | **0 (contra 3)** |

La columna «con off-target» cuenta ventanas bajo **cualquiera** de los tres
criterios, incluido el de un desajuste; con el criterio de §4 de
`sifi21_reproduccion.md`, que es sólo bloque perfecto de ≥19 nt, los números son
menores (en `BicC_Dm` 2123-2422, 3 en vez de 6). Los dos rangos de percentil
corresponden a ordenar por puntaje geométrico y por la cascada con veto.

> **La mejor región por densidad no siempre es la que recomendamos, y conviene no
> confundirlas.** En tres de los cuatro genes coinciden. En `ATPaseD_Dm` no: la región
> más densa de 300 nt es **136-435, con 24 ventanas eficientes, y está vetada**
> —contiene las tres ventanas con coincidencia perfecta de 21 nt—, así que la
> recomendación es **72-371, con 21**. Donde la tabla del percentil de §1.2 dice que
> el máximo de ese gen es 24, ese 24 es un máximo que nosotros mismos descartamos.

### 2.3 Si el laboratorio acepta mover las regiones, el orden cambia

El ranking de §2.1 es el que pidió el investigador: los cuatro candidatos **tal como
están**. Pero si la recomendación se acepta, los candidatos dejan de ser esos, y la
pregunta de si el orden aguanta es distinta. No es obvia, porque mover una región
cambia los dos ejes a la vez y no por igual en todos los genes.

| Candidato | Región elegida | Eficacia | Limpieza | → | Región recomendada | Eficacia | Limpieza |
|---|---|---:|---:|---|---|---:|---:|
| `MP_MRFV` | 1-200 | 0,1500 | 0,9802 | → | 72-271 | 0,1900 | 0,9826 |
| `CP_MRFV` | 201-400 | 0,0850 | 0,9931 | → | 99-298 | 0,1050 | 0,9925 |
| `BicC_Dm` | 264-563 | 0,0667 | **0,9334** | → | 2123-2422 | **0,1233** | **0,9922** |
| `ATPaseD_Dm` | 151-450 | 0,0600 | 0,9804 | → | 72-371 | 0,0700 | 0,9924 |

`[E]` **El orden pasa a ser `MP_MRFV` > `BicC_Dm` > `CP_MRFV` > `ATPaseD_Dm`**, en
entre el 89,7 % y el 100 % de los sorteos con la escala absoluta y en el 100 % con la
cascada. **`BicC_Dm` salta de pelear el último puesto a quedar segundo.**

El mecanismo está en la tabla y es el único que hace falta: su eficacia casi se
duplica —0,0667 a 0,1233, con lo que pasa a `CP_MRFV`— y a la vez su limpieza sube de
0,9334 a 0,9922, porque la región nueva deja afuera las 22 ventanas que coincidían
perfecto con *Homalodisca vitripennis*. Es el único de los cuatro que mejora mucho en
los dos ejes al mismo tiempo, y por eso es el único que cambia de puesto.

**Esto es lo que vuelve a la recomendación algo más que una observación.** Si el
laboratorio se queda con sus regiones, `BicC_Dm` es un candidato mediocre y vetado.
Si acepta moverla 1.859 nucleótidos dentro del mismo gen, es el segundo mejor de los
cuatro. **El gen no cambió; cambió qué parte del gen se usa.**

Dos advertencias sobre este nivel 3. La primera: bajo la escala min-max el orden se
vuelve inestable —ningún orden supera el 36 % de los sorteos—, y el motivo es que al
mejorar los cuatro quedan mucho más juntos en los dos ejes, de modo que una
normalización que estira el rango observado a [0,1] convierte diferencias chicas en
distancias grandes. Es un argumento a favor de leer este nivel con la escala
absoluta. La segunda: `ATPaseD_Dm` sigue último incluso mejorado, lo que es coherente
con que todo su gen vaya de 17 a 24 ventanas eficientes.

`[E]` **Las dos recomendaciones que importan están en los genes del insecto, y no
se apoyan en la densidad sino en el veto.** La región elegida de `BicC_Dm` contiene
22 ventanas con coincidencia perfecta de 21 nt en *Homalodisca vitripennis*; la
alternativa 2123-2422 contiene cero y además tiene casi el doble de eficientes. En
`ATPaseD_Dm` el patrón se repite más chico: 3 ventanas con coincidencia perfecta
contra cero, y 21 eficientes contra 18.

Mirar dónde caen esas coincidencias explica el caso de `BicC_Dm` de una vez. En todo
el gen hay coincidencias perfectas de 21 nt con *H. vitripennis* en tres tramos
—posiciones 212-229, 446-463 y 512-515— y **la región que EPILAB eligió, 264-563,
se superpone con dos de los tres**. En `ATPaseD_Dm` las tres coincidencias están
juntas en 392-394, dentro de la región elegida 151-450 y fuera de la alternativa
72-371. `[E]`

Cuántas regiones escapan al veto, que es lo que dice si la restricción deja material:
**1.384 de 2.201 en `BicC_Dm` y 92 de 172 en `ATPaseD_Dm`.** `[E]` El argumento de
que un filtro duro deja al proyecto sin material no se sostiene acá, igual que no se
sostuvo en `pipeline/REPORT.md` §4.3 sobre otro conjunto.

En los dos genes virales no hay nada que vetar: ninguna ventana de ninguna región
tiene coincidencia perfecta de 21 nt con el panel. La región de `MP_MRFV` ya está en
el percentil 90 y mejorarla es marginal; la de `CP_MRFV` está en la mediana y
moverla a 99-298 agrega 4 ventanas eficientes sin costo de exposición.

---

## 3. Las cinco decisiones, una por una

Cada una dice qué se gana, qué se pierde, qué evidencia la sostiene y cómo cambia el
ranking si estuviera equivocada. Las cinco están en `00_meta/DECISIONS.md` como D16
a D20.

### D1 · Cuánto pesa la densidad de eficientes contra la exposición a no objetivo

Hay tres formas posibles y no dicen lo mismo sobre el problema. La **suma ponderada**
dice que una región muy eficiente puede comprar su propio riesgo. La **media
geométrica** dice que no: un eje cerca de cero no se compensa con el otro. Y existe
una tercera, que es la que **ya tomamos en código**: `pipeline/region_scoring.py` usa
`buenos_limpios` —la intersección, cuántas ventanas son a la vez buenas y limpias—
más un veto duro, o sea trata los ejes como un filtro en cascada y no como un
puntaje combinado.

**Elegimos la media geométrica para el puntaje y conservamos la cascada como
compuerta previa**, y las reportamos a las dos. El motivo de la media geométrica es
el antecedente: `pipeline/REPORT.md` §5 resolvió esta misma pregunta sobre 1.825
ventanas y encontró que con suma ponderada entraba tercero un candidato con
accesibilidad 0,0388 compensada por una asimetría de 6,4, y con media geométrica no
entraba. Un candidato con exposición alta compensada por eficacia alta es el mismo
error con otro nombre. El motivo de conservar la cascada es que el veto no es un
peso: es una afirmación de que cierto hecho descalifica, y eso no se expresa como
ponderación.

**Qué se pierde.** La media geométrica es más dura de lo que el dato aguanta: trata
los dos ejes como igualmente confiables cuando «eficiente» es una predicción nuestra
con un umbral discutible y «coincidencia perfecta de 21 nt» es un hecho de secuencia.
Si hubiera que elegir un eje para creerle más, es el segundo, y la media geométrica
no lo refleja.

**Cómo cambia el ranking si la decisión fuera la contraria.** Poco y en un solo
lugar: con suma ponderada, `MP_MRFV` sigue primero (91 % contra 99 %) y `CP_MRFV`
segundo, y lo único que se mueve es el tercer puesto entre los dos del insecto, que
ya era inestable. **La decisión D1 no cambia el ranking**, y eso también es un
resultado: con estos cuatro candidatos la forma de la combinación no es lo que
decide. `[E]`

### D2 · Si una ventana riesgosa pero no eficiente cuenta igual que una riesgosa y activa

Acá ya habíamos tomado posición **en código y en la posición contraria** a la que la
mecánica sugiere: el veto de `region_scoring.py` descarta la región entera si alguna
ventana tiene coincidencia perfecta de 21 nt con un no objetivo, **sea eficiente o
no**, con el motivo escrito de que Dicer procesa el ARN de doble cadena entero y esa
ventana va a estar en el pool.

La posición mecanicista dice lo contrario: una ventana que no carga bien en el
complejo no silencia nada, así que una ventana riesgosa y no eficiente no es un
riesgo. Tenemos dato propio a favor: en `MP_MRFV`, de las 22 ventanas con off-target
del gen entero sólo 2 son eficientes.

**Mantenemos la posición conservadora del código y no la overrideamos.** El motivo
no es mecanicista sino de dónde ponemos la incertidumbre: «eficiente» es una
predicción de si-Fi21 con un umbral que ni siquiera reproduce los conteos declarados
por el propio laboratorio —`sifi21_reproduccion.md` §1, ninguna de 15.120
configuraciones los reproduce—, y entre el 14 % y el 24 % de lo que el original
marca como eficiente lo es sólo porque una regla terminal se saltea la física
(§0). Apostar la seguridad a esa predicción es apostar al componente más débil de la
cadena. La exposición a no objetivo se mide con coincidencia exacta de secuencia y
no depende de ningún umbral nuestro.

**Qué se pierde.** Se descartan regiones que probablemente sean seguras, y se
sobreestima el riesgo de cualquier región larga, porque cuantas más ventanas tiene
más chances hay de que alguna pegue.

**Cómo cambia el ranking.** Se reportan las dos reglas en la tabla del barrido y
**el orden de los dos primeros no cambia**: `MP_MRFV` primero y `CP_MRFV` segundo
bajo las dos. Lo que cambia es la estabilidad del tercer puesto, que bajo la regla
mecanicista con escala absoluta se vuelve determinista (`BicC_Dm` tercero el 100 %)
y bajo la conservadora se reparte 75-25. O sea: **la decisión D2 no cambia quién
gana; cambia cuánta confianza se puede tener en el orden de los que pierden.** `[E]`

### D3 · Si un off-target en maíz pesa lo mismo que uno en *Homalodisca vitripennis*

No, y los pesos se justifican por consecuencia, no por simetría. Los pesos base son
nuestros y el barrido los mueve sobre todo el símplex, así que lo que sobrevive no
depende de ellos.

| Referencia | Rol | Peso base | Por qué ese lugar |
|---|---|---:|---|
| *Zea mays* | el cultivo que se protege | 1,00 | un acierto acá es daño al objetivo mismo de la intervención |
| *Harmonia axyridis* | enemigo natural del blanco | 0,80 | un acierto es contraproducente en sentido fuerte: ayuda a la plaga |
| *Apis mellifera* | polinizador | 0,80 | el costo es regulatorio antes que ecológico, y puede bloquear el registro |
| *Homalodisca vitripennis* | cicadélido no objetivo | 0,60 | riesgo ecológico, y esperable por conservación filogenética |
| *Folsomia candida* | fauna del suelo | 0,40 | especie modelo estándar de ecotoxicología |

**El criterio de genoma contra transcriptoma ya está resuelto por construcción, y
conviene decirlo para que no parezca que lo ignoramos.** El investigador entregó
explícitamente el criterio de que un off-target que cae en el genoma pero no en el
transcriptoma pesa menos, porque no se expresa. En nuestro panel **las cinco
referencias no objetivo son transcriptomas** —todas terminan en `_rna`— y la única
genómica es la de *Dalbulus maidis*, que para los genes del insecto entra como
on-target. No hay nada que descontar: todo lo que medimos como riesgo ya cae sobre
secuencia expresada. `[E]`

**El límite del panel, que es más importante que los pesos.** Los ceros de *Apis
mellifera* son reales para los criterios de bloque perfecto, pero **la ausencia de
riesgo en cicadélidos nativos y en parasitoides no está medida**, porque no hay
transcriptomas: `pipeline/REPORT.md` §4.5 registra que las familias de parasitoides
de huevos de *D. maidis* —Mymaridae, Dryinidae, Halictophagidae— tienen cero
ensamblados anotados en RefSeq, y que el parasitismo de huevos en el noroeste
argentino promedia 16,4 % con picos de 56,7 %. **Un peso sobre una referencia que no
existe es cero por omisión, no por evidencia**, y seis referencias no son el
ambiente. `[?]`

**Cómo cambia el ranking.** Los pesos por referencia están barridos sobre todo el
símplex y el orden de los dos primeros aguanta, así que ningún reparto de pesos
razonable lo da vuelta. Donde sí muerden es en el tercer puesto: `BicC_Dm` concentra
su exposición en *H. vitripennis*, de modo que subirle el peso a esa referencia lo
hunde y bajárselo lo levanta por encima de `ATPaseD_Dm`. **Esa es la razón de que el
tercer puesto sea inestable, y es una razón honesta: depende de cuánto nos importe
un cicadélido no objetivo, que es una pregunta que no nos corresponde contestar a
nosotros.** `[H]`

### D4 · Si un bloque perfecto de 19 nt pesa lo mismo que un desajuste único

Los tres criterios se miden por separado —`perfecto_21`, `perfecto_ge19`, `mm1_21`—
y entran con pesos base 1,00, 0,60 y 0,30, barridos conservando ese orden. El orden
es lo único que sostenemos; las magnitudes, no.

Dos datos propios entran acá y los dos empujan en contra de usar el número de BLAST.
Primero: **el criterio de un desajuste medido por coincidencia exacta encuentra más
que el de BLAST, hasta un factor de tres** —16 contra 5 en `BicC_Dm`, 17 contra 9 en
`ATPaseD_Dm`— porque `blastn-short` con `word_size 11` no puede sembrar un 21-mero
cuyo único desajuste cae en la posición 11, que deja dos bloques de 10. Ponderar con
el número de BLAST sería ponderar una subestimación. `[E]`

Segundo: **la posición del desajuste dentro de la ventana no es indiferente**, y la
pregunta de si un desajuste en la región semilla pesa como uno en el extremo 3' no
la podemos contestar con lo que tenemos. No inventamos un peso: queda `[?]` y va a
la lista para el investigador. El criterio `mm1_21` que usamos **no distingue
posición**, y eso es una limitación declarada, no una elección.

Un hallazgo nuevo de esta corrida que corrige un matiz de `sifi21_reproduccion.md`
§4: la frase «cero coincidencias en *Apis mellifera* para los cuatro genes» es
cierta para los criterios de bloque perfecto, **pero no para el de un desajuste**:
`BicC_Dm` tiene 7 ventanas con un desajuste contra *Apis*. La conclusión de fondo no
cambia —ninguna de esas 7 es un bloque perfecto— pero la frase hay que decirla con
el criterio al lado. `[E]`

**Cómo cambia el ranking.** Los pesos de los tres criterios están en el barrido, y
el orden de los dos primeros no se mueve. El veto, en cambio, usa **sólo**
`perfecto_21` y no los pesos, así que es insensible a D4 por construcción: si en vez
de 21/21 el veto se disparara con bloque de 19, `MP_MRFV` (6 ventanas) y
`ATPaseD_Dm` (7) también quedarían vetados y la compuerta dejaría de discriminar.
**Que el veto use 21/21 y no 19 es, entonces, lo que lo hace informativo**, y es una
decisión que conviene que el investigador mire. `[H]`

### D5 · Si un gen del insecto y un gen del virus compiten en el mismo ranking

Ésta es anterior a las otras cuatro. `MP_MRFV` y `CP_MRFV` son genes del *Maize
rayado fino virus* y `BicC_Dm` y `ATPaseD_Dm` son genes de *Dalbulus maidis*: son
las dos estrategias que el investigador separó en la reunión, y recomendó la del
insecto por ser más directa.

**Presentamos dos rankings, uno por estrategia, más un criterio declarado de
comparación entre ellas.** El motivo es que los off-targets no significan lo mismo
en los dos casos, y la asimetría es de signo, no de magnitud: para los genes del
insecto el genoma de *D. maidis* se excluye porque es on-target, y para los virales
entra como off-target —9 ventanas de `MP_MRFV`, 2 de ellas eficientes— pero
**pegarle al vector mientras se apunta al virus no es obviamente un defecto**. Un
solo ranking obligaría a asignarle un signo a ese acierto, y no tenemos con qué.

Los dos rankings, con la escala absoluta que es la que vale con dos candidatos:

- **Estrategia virus:** `MP_MRFV` > `CP_MRFV` en entre el 90,7 % y el 100 % de los
  sorteos, según la forma de combinación. El orden es firme.
- **Estrategia insecto:** **no hay orden.** `BicC_Dm` gana en el 75 % con media
  geométrica y regla conservadora y en el 100 % con la regla mecanicista, pero
  `ATPaseD_Dm` gana en el 75 % con suma ponderada y regla conservadora. **El orden
  se da vuelta según la forma de combinación, que es una decisión nuestra**, así que
  reportar un ganador sería reportar la decisión D1. Y además las dos regiones
  elegidas están vetadas, de modo que lo que se recomienda acá no es un gen sino las
  regiones alternativas 2123-2422 y 72-371.

**El criterio declarado para comparar entre estrategias**, que es lo que falta para
poder poner los cuatro en una línea y que no es una medición sino una posición
nuestra: preferimos la vía del insecto, por dos argumentos que no salen de estos
números. Uno es del investigador —es más directa, «si vos le pegás a la chicharrita
y tratás de matar a la chicharrita, es más fácil»—. El otro es nuestro y él lo
aceptó: el período de latencia de unos 20 días entre que la chicharrita se infecta y
puede transmitir abre una ventana para matarla antes de que contagie, y una
intervención sobre el vector corta la transmisión de los cuatro agentes del complejo
a la vez, mientras que una sobre `MRFV` corta uno solo. `[R]`

**Y acá está la tensión que hay que decir en voz alta, porque es el punto más
atacable de todo el entregable:** por los números, los dos candidatos virales ganan;
por la estrategia, preferimos la vía del insecto. **No son contradictorios porque no
miden lo mismo** —el ranking mide calidad del diseño dentro de un gen dado, no valor
del blanco— pero juntarlos en un solo orden exigiría una equivalencia entre
«ventanas eficientes por nucleótido» y «cuántos patógenos del complejo corta», y esa
equivalencia no la tenemos. Si hubiera que forzar un solo orden, los dos virales
quedarían arriba, y **eso sería un artefacto de que el ranking no mide valor del
blanco.**

**Cómo cambia el ranking si la decisión fuera la contraria.** Si se presentara un
único ranking con el genoma de *D. maidis* neutralizado para los virales en vez de
contado como off-target, `MP_MRFV` sigue primero y `CP_MRFV` segundo: su exposición
baja todavía más, así que la decisión refuerza el orden en vez de darlo vuelta.
Probado con `--dmaidis-viral neutro`. `[E]`

---

## 4. La ficha por candidato

### `MP_MRFV` — proteína de movimiento del *Maize rayado fino virus*

Gen de 1.263 nt, 1.243 ventanas, 123 eficientes (9,9 %). Región elegida 1-200, con
30 ventanas eficientes en contexto y 16 aisladas. **Es el mejor candidato de los
cuatro y el único cuya región elegida está bien elegida**: percentil 91 de su propio
gen. Exposición baja: 6 ventanas con bloque perfecto de ≥19 nt en la región, 3 en
maíz y 3 en el genoma del vector, ninguna con coincidencia perfecta de 21 nt y
ninguna de las 6 es eficiente. Sin veto. La alternativa 72-271 agrega 8 eficientes y
3 ventanas expuestas; la mejora es real pero chica y no sobrevive al nulo
conservador, así que **se reporta y no se recomienda mover**. Riesgo declarado: es un
gen viral, de modo que la estrategia es la que el investigador consideró menos
directa, y el panel no mide aislados de MRFV distintos del de referencia.

### `CP_MRFV` — proteína de cápside del *Maize rayado fino virus*

Gen de 528 nt, 508 ventanas, 30 eficientes (5,9 %). Región elegida 201-400 —la
planilla dice «200-400», que son 201 posiciones para una secuencia de 200 nt, y se
resolvió localizando la subcadena exacta— con 17 eficientes en contexto y 14
aisladas. **Cero off-targets en todo el gen contra las seis referencias**, bajo los
tres criterios: es el candidato más limpio y por lejos. Su problema es el otro eje:
eficacia 0,0850, la mitad que `MP_MRFV`. La región elegida está en la mediana de su
gen y 99-298 agrega 4 eficientes sin costo. **Riesgo declarado y no resuelto:** la
región elegida es 100 % idéntica sólo al aislado de Costa Rica y cae a 91,5-93,5 %
contra los 45 registros brasileños, según la conservación entre aislados que W5 ya
midió. Una región muy limpia que funcione en un solo aislado no sirve, y **ese
cruce sigue sin hacerse**; está en `PREGUNTAS_ABIERTAS.md`.

### `BicC_Dm` — Bicaudal C de *Dalbulus maidis*

Gen de 2.520 nt, 2.500 ventanas, 171 eficientes (6,8 %). Región elegida 264-563, con
20 eficientes en contexto. **Es el candidato con la región peor elegida de los
cuatro**: percentil 44 por densidad, percentil 16 una vez que entra el veto, y **22
de sus 300 ventanas tienen coincidencia perfecta de 21 nt con el transcriptoma de
*H. vitripennis***. La alternativa **2123-2422 domina en los dos ejes a la vez**: 37
eficientes contra 20 y cero coincidencias perfectas contra 22. En el gen entero hay
56 ventanas con bloque ≥19 nt contra *H. vitripennis*, de las cuales 40 con 21/21,
lo que es esperable porque Bicaudal C está conservado entre cicadélidos; y 3
ventanas con 21/21 perfecto en *Harmonia axyridis*, un enemigo natural. **Recomendación:
mover la región.** Riesgo declarado: el blanco es de esterilización, no de letalidad
—el cribado por fenotipo lo pone en el puesto 621 de 7.416 para el objetivo «estéril»
y en el último 11 % para «letal»—, así que su valor depende de cuál sea el objetivo
de control, que es un parámetro y no un dato.

### `ATPaseD_Dm` — subunidad D de la V-ATPasa de *Dalbulus maidis*

Gen de 491 nt, 471 ventanas, 29 eficientes (6,2 %). Región elegida 151-450, con 18
eficientes. Percentil 45 por densidad y **9 una vez que entra el veto**: sus 300
ventanas incluyen las 3 del gen que tienen coincidencia perfecta de 21 nt con
*H. vitripennis*, en las posiciones 392-394. La alternativa 72-371 las deja afuera y
además tiene 21 eficientes. **Recomendación: mover la región.** Es el candidato con
menos margen de maniobra: el gen es corto, hay sólo 172 regiones posibles de 300 nt
y 92 escapan al veto; a 200 nt hay más aire. Riesgo declarado: la V-ATPasa es
exactamente el caso donde apuntar a lo más esencial y conservado maximiza la
letalidad y el riesgo no objetivo por la misma razón —`pipeline/REPORT.md` §4.4
encontró tres ventanas idénticas en 21 nt a la bomba de protones vacuolar del maíz
en otros blancos de esta familia— y además el catálogo de hemípteros del que salió
tiene un sesgo declarado: 456 de 917 proteínas descargadas son V-ATPasa.

---

## 5. Lo que este ranking no mide

Conviene dejarlo escrito junto al resultado y no en una nota al pie.

No mide **valor del blanco**: ordena qué tan bien está diseñada una región dentro de
un gen que ya alguien eligió, no si ese gen es un buen gen al que apuntar. Los dos
ejes son calidad de diseño; la pregunta de si conviene Bicaudal C o la V-ATPasa se
contesta con fenotipo y objetivo de control, no con esto.

No mide **eficacia real**, porque no hay con qué: ninguno de los cuatro diseños se
testeó nunca, y el techo del dato publicado es bajo —dos ARN de doble cadena contra
el mismo gen correlacionan 0,245 en datos publicados—. «Eficiente» acá significa
«pasa el umbral de si-Fi21», ni más ni menos.

No mide **el ambiente**: seis referencias, cinco de ellas transcriptomas de especies
modelo, con los parasitoides de huevos de *D. maidis* sin ensamblado anotado
disponible.

No mide **la quimera**: si se pegan dos regiones de genes distintos, las ventanas que
caen a caballo del empalme son secuencia nueva y hay que recalcular eficiencia y
off-targets sobre la molécula completa. Nada de lo de acá se traslada a una quimera
sin rehacerlo.

---

## 6. Cómo reproducirlo

```bash
# perfil de eficiencia por ventana de los cuatro genes (modo corregido, ViennaRNA)
python tools/sifi21_port/run_sifi.py work/sifi_check/*_full.fasta \
    --modo corregido --backend vienna --salida work/sifi_check/salida

# T1: percentil de la region elegida, los dos nulos y la correlacion con el pipeline
python tools/sifi21_port/ranking.py nulo --perfil work/sifi_check/salida \
    --reps 2000 --correlacion --json research/ola2/W7_ranking/nulo_region.json

# T2: el ranking, el barrido de pesos y las regiones alternativas
python tools/sifi21_port/ranking.py ranking --perfil work/sifi_check/salida \
    --offtarget work/sifi_check/offtarget_full/offtarget_por_sirna.tsv \
    --mm1 "work/sifi_check/offtarget_mm1_{gen}/offtarget_por_sirna.tsv" \
    --muestras 2000 --json research/ola2/W7_ranking/ranking.json

# verificaciones, incluidas las anclas contra los numeros ya publicados
python tools/sifi21_port/test_ranking.py
```

El nulo del 7,2 % se reproduce con `baseline_dsrip/region_nulo_multigen.py`
corrigiéndole las tres rutas absolutas, que apuntan a una máquina que ya no existe.
