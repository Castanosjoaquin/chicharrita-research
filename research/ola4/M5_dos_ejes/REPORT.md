# Exposición ecológica y señal de conservación: la separación, medida como sensibilidad al reparto

Fecha: 2026-10-24. Línea **M5** de la ola 4 (issue [#9](https://github.com/Castanosjoaquin/chicharrita-research/issues/9)), plan en [`docs/plan_ola4/PLAN_OLA4.md`](../../../docs/plan_ola4/PLAN_OLA4.md) §3. Implementa **D47**, que está escrito y **no se aplica a ningún entregable sin confirmación del usuario**.

Lo que sigue **no es un ranking nuevo con los pesos que nos parecieron**. Los valores de `w_exposicion` los decide el usuario —es el pedido 4 de la reunión del lunes, y son dos pesos, no uno—. Lo que esta línea entrega es la medición que esa decisión necesita: **en qué fracción del espacio de repartos posibles se sostiene cada afirmación que ya publicamos, y cuál se cae**. Es el mismo encuadre con el que M7 destrabó su tercer eje: medir la sensibilidad, no adoptar la regla.

Reproducible con los cinco scripts de [`scripts/`](scripts/) desde la raíz del repositorio; los números salen de [`resultados/`](resultados/). Marcadores de `CLAUDE.md`.


## El resultado, en un párrafo

**Separar los dos ejes casi no mueve el ranking por la vía del promedio ponderado, y lo da vuelta por la vía del veto.** De las siete afirmaciones publicadas que se pudieron medir, **seis se sostienen en todo el rango del reparto** —entre el 96,0 % y el 100 % de 2.000 sorteos en cada uno de los nueve puntos medidos— incluido el orden de los dos primeros, que es lo que D18 anticipaba `[M]`. La que **no** se sostiene es exactamente la que el issue anticipaba, y se cae de la forma más abrupta posible: en la cascada —la regla con la que se eligieron las regiones del entregable— `CP_MRFV` va antes que `ATPaseD_Dm` en el **100 %** de los sorteos mientras *Homalodisca vitripennis* conserve **cualquier** exposición, y en el **0 %** cuando su exposición es exactamente cero `[M]`. No hay transición: el veto es binario y el reparto sólo decide si esa referencia está adentro o afuera. Con exposición cero, además, **tres de las seis regiones recomendadas se mudan**, y una de ellas vuelve a ser `ATPaseD_Dm` **137-436**, la región más conservada del gen, que D25 había descartado *porque estaba vetada* `[M]`. La otra se muda a `BicC_Dm` **922-1221**, que es la que el equipo ya recomienda por otro camino. El control de D59 sobre los seis genes da **cero** ventanas de baja complejidad en 338 coincidencias contra el panel y en 71 contra los dos cicadélidos, así que ningún conteo de este informe lleva descuento `[M]`.


## 1. Dos correcciones al issue, antes de nada

**El vector de pesos no está donde el issue dice.** El issue #9 pide «partir el vector de pesos de `pipeline/region_scoring.py`». Ese archivo existe y **no tiene ningún vector de pesos**: trabaja con `UMBRAL_OFF_ALERTA` y `UMBRAL_OFF_DESCARTAR` sobre ventanas. Los pesos viven en [`tools/sifi21_port/ranking.py`](../../../tools/sifi21_port/ranking.py): `REFERENCIAS` (líneas 74-92), `DMAIDIS_INFO` (94-101), `CRITERIOS` y `PESO_CRITERIO` (108-109) y `pesos_base()` (526), y `ranking_v2.con_panel(sin_humano=False)` agrega el humano. La separación se implementó ahí `[M]`.

**El «47,4 % / 48,9 %» que el issue cita no es el estado actual.** Esa cifra es de la ventana libre de 200 nt, que no es la regla con la que se eligieron las regiones del entregable; C9 T1 bis (corrección del 2026-10-21) la rectifica a **3,3 %** con la región propuesta y el veto aplicado, a 21 nt y modo corregido. Ninguna de las dos se cita acá como estado: este informe lo vuelve a medir con los ejes separados, que es lo que no estaba hecho.


## 2. Qué se partió, y la prueba de que el motor no los junta

`w_exposicion` es probabilidad de contacto real con la formulación en la Argentina; `s_conservacion` es informatividad filogenética sobre cuán conservada está la región entre cicadélidos. La propuesta de valores es `[H]`, no una decisión, y **los de exposición distintos de *H. vitripennis* son los de D18 sin cambio**: D47 parte el vector, no rejustifica el resto, y el barrido los mueve igual sobre todo el símplex.

| Referencia | `w_exposicion` `[H]` | `s_conservacion` `[H]` | Por qué |
|---|---|---|---|
| *Zea mays* | 1,00 | 0,00 | el cultivo tratado; no es cicadélido |
| *Harmonia axyridis* | 0,80 | 0,00 | enemigo natural presente en el lote |
| *Apis mellifera* | 0,80 | 0,00 | polinizador que visita el cultivo |
| *Homalodisca vitripennis* | **0,00** | **1,00** | cicadélido no reportado en la Argentina |
| *Folsomia candida* | 0,40 | 0,00 | fauna del suelo, exposición indirecta |
| *Homo sapiens* | 1,00 | 0,00 | consecuencia máxima; no es cicadélido |
| *Dalbulus maidis* | 0,60 | 0,00 | el vector: on-target, no señal de conservación |

Vive en [`tools/sifi21_port/ejes_separados.py`](../../../tools/sifi21_port/ejes_separados.py), que **no toca `ranking.py`**: el orden se sigue calculando con el motor auditado de W7, al que se le pasa **sólo** el vector de exposición. Cada región devuelve un `DosEjes` cuyos dos campos son escalares con unidad y **sin ninguna operación en común**: sumar, restar, multiplicar, dividir o comparar un eje de exposición con uno de conservación levanta `TypeError`, y `float()` también.

La barrera sintáctica no es una imposibilidad lógica —nada impide escribir `a.valor_de("exposicion") + b.valor_de("conservacion")` a propósito— así que la verificación que vale es otra: **la invariancia**. [`tools/sifi21_port/test_ejes_separados.py`](../../../tools/sifi21_port/test_ejes_separados.py) corre el barrido con cuatro vectores de conservación distintos —el propuesto, todo cero, el propuesto por siete y todos en uno— y comprueba que las salidas son **idénticas carácter por carácter** `[M]`. Las 36 verificaciones pasan, incluida la que ancla el eje de exposición contra el motor de hoy: con `w_exposicion` igual a los pesos de D18 sin partir, las seis exposiciones reproducen `ranking_v2.json` en 6 de 6 `[M]`.


## 3. Los insumos, que había que reconstruir

`work/sifi_v2/` —lo que `ranking_v2.cargar()` espera— **no existía en esta máquina**. Se reconstruyó con [`scripts/reconstruir_insumos.py`](scripts/reconstruir_insumos.py) siguiendo la receta del encabezado de `research/ola3/C7_ranking_v2/REPORT.md`, con dos diferencias declaradas: **sólo k = 21** (k = 22 queda **no corrido**, no en cero) y el escaneo contra el genoma del vector corrido sólo con los dos genes virales, que son los únicos para los que esa referencia entra al cómputo (`excluidas_de` la saca de los cuatro genes del insecto). Las anclas verifican que esa economía no cambia ningún número.

**Las anclas corren antes de cualquier medición y abortan el proceso si fallan** ([`scripts/anclas.py`](scripts/anclas.py), salida en [`resultados/anclas.json`](resultados/anclas.json)):

| Ancla | Qué compara | Resultado |
|---|---|---|
| A1 | conteos del gen entero por referencia y criterio, seis genes, contra `ranking_v2.json` | **162 de 162** `[M]` |
| A2 | barridos de 2.000 sorteos con los pesos de D18 sin partir, diez combinaciones por cinco conjuntos, más las seis regiones recomendadas | **51 de 51** `[M]` |
| A3 | tamizaje contra *Macrosteles*, contra C6 y D23 | **6 de 6** `[M]` |

A1 extiende a los seis genes lo que M7 había verificado para los doce conteos de `BicC_Dm`. El abort no es decorativo: la primera corrida con 300 sorteos rompió A2 en 39 de 51 comparaciones, porque una frecuencia de 2.000 sorteos no se reproduce con 300. Las anclas quedaron fijadas en los 2.000 sorteos y la semilla 7 con los que se publicó el JSON.


## 4. Los dos números por región

Con la propuesta `[H]` de la §2 ([`resultados/dos_ejes_por_region.tsv`](resultados/dos_ejes_por_region.tsv)). La columna de exposición de D18 es la publicada, reproducida exacto por el módulo nuevo.

| Gen | Región | Exposición con D18 (un vector) | **Eje de exposición** (Hv = 0) | **Eje de conservación** | 21/21 con *H. vitripennis* |
|---|---|---|---|---|---|
| `MP_MRFV` | 1-200 | 0,0243 | 0,0240 | 0,0015 | 0 |
| `CP_MRFV` | 201-400 | 0,0069 | 0,0069 | 0,0000 | 0 |
| `BicC_Dm` | 264-563 | 0,0696 | **0,0124** | **0,0993** | 22 |
| `ATPaseD_Dm` | 151-450 | 0,0276 | **0,0090** | 0,0310 | 3 |
| `eth_Dm` | 114-313 | 0,0144 | 0,0117 | 0,0045 | 0 |
| `bursA_Dm` | 13-212 | 0,0000 | 0,0000 | 0,0000 | 0 |
| `ATPaseD_Dm` 137-436 (D25 alt. b) | 137-436 | — | 0,0130 | 0,0310 | 3 |

`[H]` La lectura: casi todo el «riesgo» que el motor le cobraba a `BicC_Dm` era *H. vitripennis*. Su exposición cae un 82 % (0,0696 → 0,0124) y la de `ATPaseD_Dm` un 67 % (0,0276 → 0,0090); las otras cuatro regiones no se mueven. Al mismo tiempo `BicC_Dm` 264-563 pasa a tener el eje de conservación **más alto** de las seis. Es el mismo hecho medido —22 ventanas idénticas a un transcripto de *H. vitripennis*— leído con el signo que le corresponde a cada eje, que es exactamente lo que pidió el investigador.

**El eje de conservación no tiene lectura para los genes virales.** `MP_MRFV` marca 0,0015 por una sola ventana con un desajuste contra *H. vitripennis*: eso no es conservación entre cicadélidos, es ruido. El número se reporta por completitud y no se lee.


## 5. La medición central: sensibilidad al reparto

El único parámetro que D47 deja abierto y que decide el usuario es cuánta exposición conserva *H. vitripennis*. Se barre como **ρ = `w_exposicion`(*H. vitripennis*) / `w_exposicion`(maíz)**, que es la forma en que D18 lo fijó (**0,60**) y la forma en que D47 lo propone (**0,00**). En cada uno de los nueve valores de ρ se sortean los pesos de las otras seis referencias con el mismo Dirichlet(1,…,1) del barrido de W7 y los tres pesos de criterio con el mismo Dirichlet ordenado: **2.000 sorteos por punto**, nueve puntos, diez combinaciones de forma, regla y escala, cinco conjuntos de candidatos. Script: [`scripts/sensibilidad_reparto.py`](scripts/sensibilidad_reparto.py); salidas en [`resultados/sensibilidad_reparto.tsv`](resultados/sensibilidad_reparto.tsv) (10.135 filas) y [`resultados/sensibilidad_reparto.json`](resultados/sensibilidad_reparto.json).

**Este barrido no es el publicado y no lo reemplaza.** El publicado sortea el peso de *H. vitripennis* junto con los demás sobre todo el símplex; acá se lo fija en cada punto para poder leer su efecto. El barrido publicado se reproduce exacto en el ancla A2.

### La tabla

Fracción de los 2.000 sorteos de cada punto en la que la afirmación **ya publicada** se sostiene, en escala absoluta y forma geométrica salvo donde se indica ([`resultados/tabla_afirmaciones.tsv`](resultados/tabla_afirmaciones.tsv); las diez combinaciones, en [`resultados/tabla_afirmaciones_todas_las_combinaciones.tsv`](resultados/tabla_afirmaciones_todas_las_combinaciones.tsv)).

| | Afirmación publicada | ρ = 0,00 | 0,05 | 0,10 | 0,20 | 0,30 | 0,45 | **0,60** (D18) | 0,80 | 1,00 |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | `MP_MRFV` antes que `CP_MRFV` | 98,6 | 98,6 | 98,6 | 98,6 | 98,6 | 98,6 | **98,6** | 98,6 | 98,6 |
| A2a | el orden de los dos primeros de los seis aguanta | 96,5 | 96,7 | 96,6 | 96,5 | 96,6 | 96,4 | **96,2** | 96,0 | 96,0 |
| A2b | ídem, lista del insecto | 97,4 | 97,3 | 97,3 | 97,2 | 97,2 | 97,0 | **96,7** | 96,6 | 96,5 |
| A3 | `BicC_Dm` primero, regiones recomendadas | 98,0 | 98,9 | 98,9 | 98,8 | 98,8 | 98,8 | **98,8** | 98,8 | 98,8 |
| A4 | `ATPaseD_Dm` último, regiones recomendadas | 99,9 | 99,9 | 99,9 | 99,9 | 100,0 | 100,0 | **100,0** | 100,0 | 100,0 |
| A5 | `eth` antes que `burs-α` | 97,4 | 97,4 | 97,4 | 97,2 | 97,2 | 97,0 | **96,7** | 96,6 | 96,5 |
| A6 | `BicC_Dm` tercero y `ATPaseD_Dm` cuarto (planilla) | 98,5 | 97,3 | 96,6 | 93,8 | 91,1 | 88,1 | **84,4** | 80,9 | 77,9 |
| **A7** | **`CP_MRFV` antes que `ATPaseD_Dm`, en la cascada** | **0,0** | **100,0** | 100,0 | 100,0 | 100,0 | 100,0 | **100,0** | 100,0 | 100,0 |
| A7b | ídem, en la forma geométrica | 99,9 | 99,9 | 99,9 | 100,0 | 100,0 | 100,0 | **100,0** | 100,0 | 100,0 |

### Las tres preguntas del issue, contestadas con el número

**¿El orden de los dos primeros aguanta, como dice D18?** Sí, y con un margen cómodo: entre **96,0 % y 97,4 %** en todo el rango, en las dos listas (A2a, A2b) `[M]`. D18 decía «aguanta todo el símplex» sin número; ahora lo tiene.

**¿Qué pasa con el tercer puesto cuando la exposición de *H. vitripennis* baja a cero?** Hay que contestar por separado según la forma de agregación, porque dicen cosas distintas:

- En la **cascada**, que es la regla con la que se eligieron las regiones del entregable, el par `ATPaseD_Dm` / `CP_MRFV` **se da vuelta entero**: 0 % contra 100 % de los sorteos, con el salto en ρ = 0 exacto `[M]`. El empate no «vuelve a abrirse»: se invierte. Y arrastra el orden completo de los seis: de `MP_MRFV > eth > CP_MRFV > burs-α > BicC_Dm > ATPaseD_Dm` a **`MP_MRFV > BicC_Dm > ATPaseD_Dm > eth > CP_MRFV > burs-α`**, en el 100 % de los sorteos de los dos lados. Los dos genes del insecto suben cuatro puestos.
- En las formas **ponderadas** (geométrica y suma), el mismo par no se mueve: `CP_MRFV` sigue adelante en el 99,9 % de los sorteos con ρ = 0 (A7b) `[M]`.
- Y el otro «tercer puesto», el de la lista del insecto —`BicC_Dm` tercero contra `ATPaseD_Dm` cuarto— **se refuerza** al bajar ρ: 84,4 % con el reparto de D18 y 98,5 % con exposición cero (A6) `[M]`. Es lo que la propia consecuencia de D18 anticipaba: «subirle el peso a esa referencia lo hunde y bajárselo lo levanta».

**¿Alguna región hoy vetada vuelve a estar sobre la mesa?** Sí ([`resultados/vetos_por_reparto.tsv`](resultados/vetos_por_reparto.tsv), [`resultados/regiones_recomendadas_por_reparto.tsv`](resultados/regiones_recomendadas_por_reparto.tsv)):

| | ρ > 0 (cualquiera) | ρ = 0 |
|---|---|---|
| `BicC_Dm` 264-563 (planilla) | vetada | **no vetada** |
| `ATPaseD_Dm` 151-450 (planilla) | vetada | **no vetada** |
| `ATPaseD_Dm` 137-436 (D25 alt. b) | vetada | **no vetada** |
| Regiones de `ATPaseD_Dm` sin veto | 92 de 172 | **172 de 172** |
| Regiones de `BicC_Dm` sin veto | 1.384 de 2.201 | **1.899 de 2.201** |
| Regiones de `eth_Dm` sin veto | 196 de 396 | **396 de 396** |
| Región recomendada de `BicC_Dm` | 2121-2420 | **922-1221** |
| Región recomendada de `ATPaseD_Dm` | 72-371 | **137-436** |
| Región recomendada de `eth_Dm` | 114-313 | **194-393** |

`[H]` Dos de esas mudanzas merecen atención opuesta. La de `BicC_Dm` es tranquilizadora: con el eje de exposición solo, la cascada elige por sí misma **922-1221**, que es la región que D25 ya recomienda por conservación entre fuentes públicas. Dos criterios independientes llegan al mismo lugar. La de `ATPaseD_Dm` es la que cambia una recomendación publicada: **137-436** es la región más conservada del gen y D25 la descartó explícitamente *porque estaba vetada*; sin el veto de *H. vitripennis* vuelve, y además tiene **24 ventanas eficientes contra las 18** de la región de la planilla y las mismas 3 coincidencias de 21/21 (que ahora cuentan como conservación) `[M]`.

### De dónde viene el cambio: del veto, no de la ponderación

La columna «veto ciego» de [`resultados/tabla_afirmaciones.tsv`](resultados/tabla_afirmaciones.tsv) repite el punto ρ = 0 manteniendo la regla de veto de hoy, en la que **cualquier** referencia del panel veta tenga el peso que tenga. Con esa regla, A7 vuelve a 100 % y el orden de los seis vuelve a ser el publicado `[M]`. Las formas ponderadas, en cambio, dan **exactamente lo mismo** con las dos reglas de veto, porque una referencia de peso cero ya aportaba cero al promedio.

`[H]` O sea que todo el efecto de la separación corre por un solo lugar: **qué mira la cascada**, que son dos cosas ciegas al peso —el veto de 21/21 y el conteo de «eficientes limpios»—. Y de ahí sale la consecuencia práctica más importante de esta línea: **la decisión del usuario no es cuánta exposición conserva *H. vitripennis*, sino si conserva alguna**. Entre 0,05 y 1,00 no hay ninguna diferencia en la cascada en la grilla medida; entre 0,00 y 0,05 está todo el cambio. Un reparto «chiquito pero no cero» —que es la salida intermedia que uno esperaría negociar— **no existe** con la regla de riesgo de hoy. Hacerla existir es justamente lo que D48 y la línea M6 proponen: cambiar el veto binario por una alerta con justificación.


## 6. El ranking rehecho con los dos ejes, con lo que se pierde

Con las regiones del ranking v2 y en forma geométrica, escala absoluta, el orden modal **no cambia** en todo el rango de ρ: `MP_MRFV > eth_Dm > CP_MRFV > burs-α > BicC_Dm > ATPaseD_Dm`, en el 95,3 % de los sorteos con ρ = 0 contra el 83,7 % con ρ = 0,60 `[M]`. La separación lo hace **más** firme, no menos.

Con la cascada, el orden modal cambia por completo en ρ = 0, como dice la §5. Y con las regiones recomendadas —reelegidas en cada ρ, porque son una salida y no una entrada— el orden de la cascada pasa de `MP_MRFV > BicC_Dm > CP_MRFV > eth > ATPaseD_Dm > burs-α` a `MP_MRFV > BicC_Dm > ATPaseD_Dm > eth > CP_MRFV > burs-α` `[M]`.

**Lo que se pierde, dicho con el mismo énfasis que lo que aguanta.** Tres afirmaciones publicadas dejan de estar sostenidas si el usuario adopta ρ = 0:

1. «Las dos regiones que EPILAB eligió para los genes del insecto **quedan vetadas**» (`entregables/checkpoint2-una-pagina.md`, punto 4). Con exposición cero no quedan vetadas: las 22 ventanas de `BicC_Dm` y las 3 de `ATPaseD_Dm` pasan a ser señal de conservación `[M]`.
2. «La región recomendada de `ATPaseD_Dm` (72-371) **se mantiene**» (`entregables/para-el-investigador.md`, fila 4, y D25). Con exposición cero el motor recomienda **137-436** `[M]`.
3. El desempate del par `ATPaseD_Dm` / `CP_MRFV` en la cascada, que se invierte `[M]`.

`[M]` Una cuarta, «`ATPaseD_Dm` último» (A4), conviene mirarla aunque **no dependa de ρ**: se sostiene entre el 99,9 % y el 100 % de los sorteos en escala absoluta y en los nueve puntos, pero en la cascada es falsa en el 100 % —con las regiones recomendadas el último es `burs-α` y `ATPaseD_Dm` queda tercero— y eso ya estaba así en el `ranking_v2.json` publicado. Es dependencia de la forma de agregación, no efecto de la separación, y se anota para que no se le atribuya a esta línea.

Las tres van a [`NOTAS_PARA_META.md`](NOTAS_PARA_META.md) con las dos cifras y su fuente. **Esta línea no tocó `entregables/` ni el ranking publicado**, que es lo que el alcance pide.

`[H]` Y una advertencia de lectura que vale para las tres: la comparación `ATPaseD_Dm` contra `CP_MRFV` cruza las dos listas que **D38 decidió no comparar** —el ranking mide la calidad del diseño dentro de un gen, no el valor del blanco—. El issue la pide porque es la que C9 midió, y está contestada, pero si D38 sigue en pie el par no debería decidir nada por sí solo.


## 7. El eje de conservación se apoya hoy en una sola referencia, y eso reabre D23

El panel tiene **un** cicadélido no objetivo, *H. vitripennis*, así que el eje de conservación de la §4 es en realidad «identidad con un transcriptoma de un cicadélido norteamericano». Hay un segundo cicadélido medido en el repositorio: *Macrosteles quadrilineatus*, que **D23 sacó del panel con un argumento de exposición** —«la especie no está en Argentina y por lo tanto no es un organismo expuesto»—, y la propia D23 anota que se lo había incorporado «como sustituto filogenético del resto de los Deltocephalinae, no por exposición directa, y ese uso no se descarta con su ausencia en Argentina».

`[H]` **Separar los ejes reabre esa decisión.** La ausencia en la Argentina lo saca del eje de exposición; no dice nada sobre el de conservación, que es para lo que había entrado. [`scripts/eje_conservacion_cicadelidos.py`](scripts/eje_conservacion_cicadelidos.py) lo mide **sin agregarlo al panel**: su `w_exposicion` es cero y la vista de exposición lo filtra, de modo que no mueve ningún número de orden de este informe ([`resultados/eje_conservacion_cicadelidos.tsv`](resultados/eje_conservacion_cicadelidos.tsv)).

| Gen | Región | Eje de conservación con 1 cicadélido | con 2 | 21/21 *H. vitripennis* | 21/21 *M. quadrilineatus* |
|---|---|---|---|---|---|
| `BicC_Dm` | 264-563 | 0,0993 | **0,2177** | 22 | 10 |
| `ATPaseD_Dm` | 151-450 | 0,0310 | **0,1070** | 3 | 12 |
| `ATPaseD_Dm` | 137-436 | 0,0310 | **0,1040** | 3 | 12 |
| `eth_Dm` | 114-313 | 0,0045 | **0,1050** | 0 | 9 |
| `bursA_Dm` | 13-212 | 0,0000 | **0,0345** | 0 | 0 |

`[M]` Con un solo cicadélido, `eth_Dm` y `burs-α` parecen no tener señal de conservación y `ATPaseD_Dm` tener poca; con dos, `eth_Dm` queda al nivel de `ATPaseD_Dm`. `[H]` La lectura es que **el eje de conservación, tal como está, mide poco y mal**: con n = 1 referencia no distingue «región poco conservada» de «región que ese transcriptoma no cubre». Las seis anclas del tamizaje reproducen los números de C6 y D23 (101 ventanas en el gen entero de `BicC_Dm`, 19 en 2123-2422, 10 en 264-563, las mismas 12 en las dos regiones de `ATPaseD_Dm`, 21 en el gen entero de `eth`), así que el dato es el mismo que ya estaba en el repositorio, leído con el otro signo `[M]`.


## 8. El control de D59, sobre los seis genes

D59 obliga a informar todo conteo de off-target en dos cifras —el total y cuánto es de baja complejidad— y a releer con ese descuento los tamizajes ya corridos. M7 lo había hecho en `BicC_Dm`; acá va en los seis ([`scripts/complejidad_seis_genes.py`](scripts/complejidad_seis_genes.py), [`resultados/complejidad_seis_genes.tsv`](resultados/complejidad_seis_genes.tsv)).

| Gen | Ventanas | De baja complejidad | Homopolímero más largo (umbral 10) | Bases distintas, mínimo (umbral 2) |
|---|---|---|---|---|
| `MP_MRFV` | 1.243 | **0** | 5 | 3 |
| `CP_MRFV` | 508 | **0** | 6 | 3 |
| `BicC_Dm` | 2.500 | **0** | 7 | 3 |
| `ATPaseD_Dm` | 471 | **0** | 4 | 3 |
| `eth_Dm` | 595 | **0** | 5 | 3 |
| `bursA_Dm` | 448 | **0** | 5 | 3 |

`[M]` De las **338** ventanas con coincidencia contra el panel, repartidas en 35 celdas de gen × referencia × criterio, **ninguna** es de baja complejidad; de las **71** con 21/21 contra los dos cicadélidos, **ninguna** tampoco. Ningún conteo de este informe lleva descuento, y en particular las 22 ventanas de `BicC_Dm` con *H. vitripennis* —el conteo del que depende toda la discusión— no son un artefacto de poli-A. `[H]` El criterio de complejidad es nuestro y sigue pendiente de contrastar contra `dustmasker`, así que la marca viaja como hipótesis.


## 9. El riesgo de la separación, escrito

`[H]` **Darle exposición cero a *Homalodisca vitripennis* es correcto hoy y es una apuesta sobre que siga ausente.** Es plaga cuarentenaria: si entrara a la Argentina, todas las ventanas que esta línea reclasificó como «señal de conservación» vuelven a ser exposición de un día para el otro, y el diseño que hoy se elige sin veto pasaría a estar vetado con el panel sin cambiar una sola secuencia. La contracara operativa es barata y conviene dejarla escrita: **el reparto se declara con fecha y se revisa si cambia el estatus cuarentenario**, y el informe guarda las dos cifras —con y sin exposición— para que esa revisión sea una lectura de tabla y no una corrida nueva. Las dos columnas están en [`resultados/tabla_afirmaciones.tsv`](resultados/tabla_afirmaciones.tsv).

`[H]` **Y hay un segundo riesgo, que es más probable que el primero y que el issue no menciona.** D18 puso a *H. vitripennis* en el panel con dos funciones, y la segunda era ser «sustituto medible de los nativos que no lo son». Los cicadélidos nativos argentinos **sí** están expuestos —comparten el cultivo con el vector— y no tienen genoma ni transcriptoma público con el que tamizar. Darle exposición cero al único cicadélido del panel no sólo reclasifica sus coincidencias: **deja el eje de exposición sin ningún representante de los cicadélidos no objetivo**, que son el grupo de riesgo más cercano al blanco por construcción del RNAi. La separación es correcta en su lógica y, aplicada tal cual, borra el único sustituto medible que teníamos. La salida no es volver al peso único: es declarar esa exposición en el eje donde corresponde —un cicadélido nativo con exposición alta— y admitir que hoy **no tenemos la referencia para medirla**. Eso es un pendiente de datos, no un peso, y va a `PREGUNTAS_ABIERTAS.md`.


## 10. Lo que esta línea no decide, y lo que no midió

No decide los valores de `w_exposicion` ni si el tercer puesto se reporta como empate declarado o se sigue ordenando: las dos cosas son del usuario, y el pedido 4 del lunes es exactamente el primero. No decide tampoco si el veto se vuelve alerta, que es D48 y la línea M6 (#10): esta línea mide que **todo el efecto de la separación pasa por ahí**, que es el insumo que a M6 le faltaba.

Límites `[M]`/`[H]`:

- **k = 22 no se corrió.** Todo lo medido es a 21 nt. El ranking v2 publica los dos largos y C9 T1 bis midió que el orden del par `ATPaseD_Dm`/`CP_MRFV` se comporta distinto a 22 nt. **No corrido, no cero.**
- **El barrido de ρ fija una sola coordenada.** Los otros seis pesos de exposición se sortean sobre todo el símplex, pero la relación entre ellos no se barre por separado: una pregunta como «¿cuánto cambia si el humano pesa más que el maíz?» no está contestada acá.
- **Las fracciones dependen de la grilla.** Cada una es sobre **2.000 sorteos** del punto correspondiente; los nueve valores de ρ son una elección nuestra y no una distribución de probabilidad sobre repartos.
- **El eje de conservación mide identidad de secuencia contra transcriptomas, no conservación filogenética.** Con una referencia subestima, y con dos sigue sin ser un alineamiento múltiple de cicadélidos. Es lo que hay medido, y está declarado.
- **La cascada es determinista.** Sus fracciones son 0 % o 100 % porque el veto y el conteo de eficientes limpios no dependen de los pesos sorteados. Que una columna diga 100 % no significa que sea más robusta: significa que el sorteo no la toca.
- Un resultado in silico es una hipótesis sobre eficacia, nunca una prueba.
