# M6 — Del veto binario a la alerta justificada

Línea M6 de la ola 4 (issue #10), que implementa **D48**. Diego confirma la posición
conservadora de **D17** —«evaluamos la identidad de secuencia de los posibles
off-targets independientemente de que esas ventanas sean clasificadas como siRNAs
eficientes», porque «una predicción negativa de eficiencia no garantiza que un siRNA
carezca de actividad biológica» `[R]`— y corrige la consecuencia: «no trataría todas
las coincidencias de 21 nt como equivalentes ni las convertiría automáticamente en un
veto ecológico universal. Sí las conservaría como alertas fuertes que deben ser
consideradas y justificadas» `[R]`.

El cambio no es de severidad sino de carga de la prueba. Lo que se entrega acá es la
tabla que hace exigible el argumento y el estado de las regiones bajo la regla nueva.
**Qué alertas se aceptan y cuáles siguen siendo bloqueantes no lo decide esta línea ni
el motor**: ninguna región se acepta ni se descarta en este informe, y las dos columnas
donde va esa decisión salen escritas con la palabra «pendiente».

## 1. Lo que hay que leer primero

Hay **17 alertas** sobre las doce regiones candidatas, y las cuatro vigentes de los
genes de EPILAB **no tienen ninguna de 21/21** `[M]`. Trece alertas de bloque ≥ 19 nt
entre esas cuatro —dieciséis si al genoma del vector se lo cuenta como no objetivo de
los genes virales, que es lo que hace el motor por D5— y nada más. La tabla de alertas
**no cambia el estado de lo que hoy recomendamos; cambia el de lo que hoy está
descartado** `[H]`.

Las únicas tres regiones con coincidencia perfecta de 21 nt son `BicC_Dm` 264-563,
`ATPaseD_Dm` 151-450 y `ATPaseD_Dm` 137-436, las tres contra *Homalodisca vitripennis*,
y en las tres el transcripto impactado es **el ortólogo del gen que se quiere silenciar**
`[M]`: `XM_046816879.1`, bicaudal C homolog 1-A (LOC124362408), y `XM_046807969.1`,
subunidad D de la V-ATPasa (LOC124356774). El acierto no es un off-target incidental en
un gen cualquiera: es el mismo gen en un pariente, que es exactamente el escenario en el
que un ARNdc silenciaría al no objetivo `[H]`.

Y hay un contraste que conviene llevar a la mesa junto con la decisión de M5. Bajo la
regla de veto de hoy, ciega al peso, esas tres regiones están vetadas. Bajo la regla
ponderada por exposición que midió M5 —con *H. vitripennis* en exposición cero— **las
tres dejan de estar vetadas sin que nadie escriba nada**: la alerta desaparece del
tablero `[M]`. Bajo D48 la alerta **no desaparece**, porque la tabla es ciega al peso: la
fila sigue ahí, con su exposición declarada en cero, y lo que cambia es que hay que
firmar un párrafo. Ésa es la salida intermedia que M5 dijo que no existía con la regla
de riesgo de hoy `[H]`.

## 2. La tabla de alertas y sus cuatro campos

`resultados/alertas.tsv` tiene una fila por coincidencia con los cuatro campos que
enumera Diego, explícitos y obligatorios, y el mismo contenido partido por región en
`resultados/alertas_por_region/`. Una fila sin los cuatro campos **no es una fila con
celdas vacías: es un error de validación**, `alertas.FilaIncompleta`, y
`alertas.escribir()` valida antes de abrir el archivo, de modo que una tabla incompleta
no llega al disco. La prueba está en `tools/sifi21_port/test_alertas.py` y rompe la fila
a propósito, columna por columna, en las diecisiete columnas que materializan los cuatro
campos, y también en las tres formas de estar incompleta sin estar vacía: clave fuera
del vocabulario cerrado, bioensayo fuera del vocabulario y prosa de una palabra.

**Campo 1, qué organismo.** Nombre corto, especie y rol en el panel, de `REFERENCIAS` e
`INFO_HUMANO`.

**Campo 2, su posibilidad de exposición.** No se reinventa: sale de `PANEL_EJES` de
`tools/sifi21_port/ejes_separados.py`, que es donde M5 dejó el peso y su motivo por
referencia (D47). La fila lleva **los dos valores** —`exposicion_w`, el de D47, y
`exposicion_w_alternativa`, el de D18— y una columna `exposicion_decision_abierta` que
vale «sí» sólo para *H. vitripennis*, porque ése es el pedido 4 del lunes y lo decide el
usuario. **La tabla sirve con ese valor en cero y distinto de cero sin recalcularse**:
la pertenencia de una fila a la tabla no depende del peso, sólo la lectura de su
gravedad.

**Campo 3, qué gen está involucrado.** Es el único desarrollo nuevo de la línea.
`offtarget_21nt.escanear()` ya calculaba el conjunto de accesiones impactadas y `main()`
escribía sólo `len(refs)`: la identidad se computaba y se tiraba. Ahora
`escanear_con_identidad()` la conserva y `iter_db_anotado()` trae la cabecera completa
del FASTA, de donde salen el nombre, el LOC y el tipo de molécula. **Todo de disco**: el
tamizaje es local y por coincidencia exacta, y ninguna secuencia de EPILAB sale de la
máquina. Se citan **20 transcriptos** distintos con su anotación textual `[M]`.

**Campo 4, qué evidencia biológica hay.** Lleva una clave de vocabulario cerrado —que el
script sí puede verificar— y la prosa, que no. De las 17 filas, **3 son
`ortologo_del_blanco`, 12 `gen_no_relacionado` y 2 `sin_anotacion_de_gen`** `[M]`. Las
dos últimas son las coincidencias de `MP_MRFV` contra el ensamblado genómico de
*Dalbulus maidis*, que no trae anotación de gen: ahí el campo dice que no se puede
nombrar un gen, y **no se inventa uno**. Y las 17 filas, sin excepción, llevan
`evidencia_bioensayo = sin_bioensayo_consultado`, porque esta línea no abrió ninguna
fuente experimental sobre esos organismos y esos genes. Eso queda en
`00_meta/PREGUNTAS_ABIERTAS.md`, no disimulado dentro del párrafo.

**La granularidad de la fila es región × organismo × gen**, y la decisión está medida.
Para los aciertos de 21/21 las dos granularidades dan casi lo mismo, como decía la sonda
del prompt: 28 filas por ventana × transcripto contra 3 agrupadas, porque todas caen en
un solo transcripto. Para el bloque de ≥ 19 nt **no**, y la diferencia es de isoformas
del mismo gen: las 3 ventanas de `BicC_Dm` 2121-2420 contra humano caen en **ocho
transcriptos de `SLC24A4`**, y las 3 contra maíz de 264-563 en **tres variantes de la
misma esterasa** (LOC100281777) `[M]`. Por ventana × transcripto la tabla tendría 143
filas en vez de 17 y pediría veinticuatro párrafos idénticos para un solo gen humano.
La tabla por ventana se conserva igual, sin columna de secuencia, en
`resultados/alertas_por_ventana.tsv`.

## 3. Los dos umbrales de D28, y la contradicción del umbral 17

Cada alerta informa los dos umbrales de D28 —`ventanas_perfecto_21` y
`ventanas_perfecto_ge19`— y la columna `umbrales_anidados` recuerda que el segundo
contiene al primero por construcción: toda ventana con 21/21 perfecto tiene también un
bloque perfecto de ≥ 19 nt. Por eso 264-563 informa 22 y 30 contra *H. vitripennis*, no
22 y 52.

`[M]` **La contradicción de `UMBRAL_OFF_ALERTA = 17` es real y es grande.** D28 fijó que
«no se reportan coincidencias de 16 a 18 nt como off-targets», y
`pipeline/region_scoring.py` sigue alertando desde 17. Medido sobre el único archivo del
repositorio que tiene la columna `off_target_max`, `baseline_dsrip/ventanas_multigen.csv`,
con 23.612 ventanas: con el umbral 17 quedan **2.338 ventanas en alerta**, con el umbral
19 quedan **436**, y la banda de 17 a 18 nt son **1.902 ventanas, el 81,4 % de las
alertas de hoy** `[M]`. El nivel de descarte, 21, marca 173. O sea que cuatro de cada
cinco alertas de ese módulo están por debajo del piso que D28 declaró, y en ese rango la
propia medición de D28 dice que el azar explica el total.

`[H]` **No se cambió la constante.** Bajarla a 19 mueve una cifra ya publicada de un
módulo que no es el de esta línea, y el alcance de M6 es medir y proponer. Queda
propuesto en `NOTAS_PARA_META.md` con las dos cifras y su fuente, para `DECISIONS.md`.
Vale aclarar que esa contradicción **no toca ningún número de este informe**: la tabla de
alertas se construye con `offtarget_21nt.py` y los dos criterios de D28, no con
`off_target_max`.

## 4. El estado de las doce regiones bajo la regla nueva

El issue habla de «las cuatro regiones vigentes», pero desde C7 v2 hay seis candidatos y
cada gen de EPILAB tiene región de planilla y región recomendada, así que se cubren las
**doce** de `resultados/estado_regiones.tsv`. La tabla trae, por región, las alertas en
los dos umbrales, el veredicto de la regla de hoy, el de la regla ponderada por
exposición de M5 y el estado bajo D48.

| gen | región | qué es | 21/21 | ≥ 19 nt | veto hoy | veto por exposición (M5) | estado D48 |
|---|---|---|---|---|---|---|---|
| `MP_MRFV` | 72-271 | recomendada C7 v2 | 0 | 6 | no | no | con alertas, pendiente |
| `CP_MRFV` | 99-298 | recomendada C7 v2 | 0 | 0 | no | no | **sin alertas** |
| `BicC_Dm` | 922-1221 | recomendada D25 | 0 | 3 | no | no | con alertas, pendiente |
| `ATPaseD_Dm` | 72-371 | recomendada C7 v2 / D25 | 0 | 7 | no | no | con alertas, pendiente |
| `eth_Dm` | 114-313 | propuesta C7 v2 | 0 | 3 | no | no | con alertas, pendiente |
| `bursA_Dm` | 13-212 | propuesta C7 v2 | 0 | 0 | no | no | **sin alertas** |
| `MP_MRFV` | 1-200 | planilla EPILAB | 0 | 6 | no | no | con alertas, pendiente |
| `CP_MRFV` | 201-400 | planilla EPILAB | 0 | 0 | no | no | **sin alertas** |
| `BicC_Dm` | 264-563 | planilla EPILAB | **22** | 33 | **sí** | no | con alertas, pendiente |
| `BicC_Dm` | 2121-2420 | C7 v2, desplazada por D25 | 0 | 6 | no | no | con alertas, pendiente |
| `ATPaseD_Dm` | 151-450 | planilla EPILAB | **3** | 11 | **sí** | no | con alertas, pendiente |
| `ATPaseD_Dm` | 137-436 | la más conservada, alt. b de D25 | **3** | 13 | **sí** | no | con alertas, pendiente |

`[M]` Las seis cifras de `BicC_Dm` que dejó M7 §5 se reproducen exactas: 0 / 0 / 22 con
21/21 y 3 / 6 / 33 con bloque de ≥ 19 nt. Y los conteos por región y por referencia
reproducen las 68 comparaciones que publica `ranking_v2.json` en los dos umbrales.

### Cuáles vuelven a estar sobre la mesa

`[H]` Las tres que el veto de hoy descarta —`BicC_Dm` 264-563, `ATPaseD_Dm` 151-450 y
`ATPaseD_Dm` 137-436— vuelven a estar sobre la mesa **con la obligación de justificarse**,
y no porque su alerta se haya debilitado. Empezando por la que nombra D48, `ATPaseD_Dm`
137-436, que D25 había descartado por veto siendo la región más conservada del gen: su
alerta son 3 ventanas con 21/21 y 7 con bloque de ≥ 19 nt contra el ortólogo de la
subunidad D de la V-ATPasa de *H. vitripennis*, más 6 ventanas de ≥ 19 nt contra dos
genes humanos sin relación con el blanco `[M]`.

`[M]` **Un dato que diferencia a `ATPaseD_Dm` de `BicC_Dm` y que conviene mirar antes de
firmar**: de las 3 ventanas con 21/21 contra el ortólogo de la V-ATPasa, **2 son además
predichas eficientes** en 151-450 y 137-436, lo que coincide con la ficha publicada. En
`BicC_Dm` 264-563, en cambio, las 22 son no eficientes, que es el resultado que M7 ya
había señalado. `[H]` La lectura: en `BicC_Dm` la regla mecanicista apagaría la alerta
entera y en `ATPaseD_Dm` no, así que la región que D48 nombra como primera candidata a
volver es justamente la que menos depende de descartar la predicción de eficiencia para
sostener su riesgo. Eso no la bloquea ni la habilita: es lo que el párrafo de
justificación tiene que mirar de frente. Y la predicción de eficiencia **no entra al
criterio** por D17; está en la tabla como contexto, no como compuerta.

`[H]` La decisión sobre esas tres regiones depende de un valor que no es nuestro: la
exposición de *H. vitripennis*. Con el valor de D47 —exposición cero, cicadélido no
reportado en la Argentina— la lectura natural es que una coincidencia con un organismo
que no está en el lote es señal de conservación y no riesgo ecológico, y que la alerta se
acepta con esa justificación escrita; con el valor de D18 —0,60— la misma fila es un
riesgo ecológico de primer orden sobre el ortólogo exacto del gen blanco. **Las dos
lecturas usan la misma fila sin recalcular nada**, que es para lo que la tabla trae las
dos columnas de peso. La apuesta declarada en D47 sigue en pie: *H. vitripennis* es plaga
cuarentenaria y darle exposición cero es correcto hoy y es una apuesta sobre que siga
ausente.

## 5. Qué se pierde al cambiar el booleano por un párrafo

D48 ya lo dice y no es retórica: se pierde la comodidad de una compuerta automática, y
un párrafo puede estar mal escrito de un modo en que un booleano no puede. Lo que esta
línea agrega es cuáles son esos modos, con la evidencia de nuestra propia tabla.

**Una tabla puede estar completa y vacía al mismo tiempo, y la validación la da por
buena.** Las 17 filas pasan la validación mecánica —los cuatro campos presentes, las
claves dentro del vocabulario cerrado, la prosa por encima del largo mínimo— y las 17
dicen `sin_bioensayo_consultado` `[M]`. Es decir: **el 100 % de la tabla es válida y el
0 % tiene respaldo experimental**. Un booleano no podía mentir sobre esto porque no
afirmaba nada; un campo llamado «evidencia biológica» sí parece afirmar algo. La
validación no puede atrapar esa diferencia y por eso la clave de bioensayo es una columna
aparte, obligatoria y de vocabulario cerrado, en vez de una frase dentro del párrafo.

**El default se invierte, y ése es el riesgo grande.** La compuerta descartaba por
omisión: una región con 21/21 quedaba afuera aunque nadie la mirara. La tabla no descarta
nada, así que **una alerta no leída queda operativamente igual que una alerta aceptada**.
El veto era conservador cuando nadie prestaba atención; la tabla es permisiva cuando nadie
presta atención. En esta entrega eso está apenas contenido por las columnas
`decision_usuario` y `justificacion_usuario`, que salen en «pendiente», pero **nada en el
código impide usar una región cuya fila sigue en «pendiente»**: hacerlo cumplir es una
decisión de proceso, no de software, y hoy no está tomada.

**Se pierde la comparabilidad.** Dos regiones con el mismo booleano eran iguales; dos
regiones con párrafos distintos no se pueden ordenar, y el motor ya no puede producir un
orden que las incluya. Eso está explícito en el código: pedirle la forma `cascada` bajo la
regla de alerta levanta `CompuertaRetirada`, porque la cascada **es** la compuerta —resta
1.000 a la región vetada— y fingir que se puede rankear sin ella sería esconder el
problema en un número.

**Se pierde la reproducibilidad del veredicto.** El booleano era una función de la
secuencia: el mismo dato daba el mismo resultado en cualquier máquina y en cualquier
fecha. El párrafo es una función de quién lo escribe. Dos personas pueden justificar la
misma fila en direcciones opuestas y las dos pasar la validación.

**Y lo que la validación mecánica no puede atrapar, enumerado para que nadie lo lea como
atrapado.** No puede verificar si la prosa es **cierta**; si es **pertinente** a la fila
que acompaña; si es **suficiente** para el riesgo que describe; si la justificación que
cita una fila efectivamente leyó esa fila. Tampoco verifica el campo 3 más allá de lo que
dice la cabecera: la anotación de RefSeq es una anotación, y en los transcriptos
`PREDICTED:` es una predicción computacional, no un gen caracterizado; que el ortólogo de
bicaudal C de *H. vitripennis* sea funcionalmente equivalente al blanco es una hipótesis
`[H]`, no un hecho medido por nosotros. Lo único que el script garantiza es que **los
cuatro campos están y tienen la forma declarada**. Que el argumento sea bueno no lo puede
verificar ningún script, y simular lo contrario sería el peor resultado posible de esta
línea.

## 5 bis. La compuerta que D48 deja abierta, y qué umbral la dispara

*Agregado el 2026-10-26, después del cierre del issue, sobre el punto que §5 dejó
declarado como lo que el software no puede hacer cumplir.*

De los cinco modos de fallar que enumera §5, hay uno que **sí** se puede atrapar en
código, y es el más peligroso: que el default se haya invertido. La compuerta descartaba
por omisión; la tabla no descarta nada, así que una alerta no leída queda operativamente
igual que una aceptada. `alertas.exigir_decidida()` se niega a tratar una región como
usable mientras alguna de sus filas siga en «pendiente», y `alertas.leer()` valida las
decisiones al abrir la tabla. No decide qué alertas se aceptan —eso sigue siendo del
usuario— ni se aplica a ningún entregable por su cuenta: se implementa sin adoptar, la
misma postura que `regla_veto="alerta"`.

Lo que la compuerta exige para dar por decidida una fila es lo que pide D48 y nada más:
una decisión del vocabulario cerrado (`pendiente`, `aceptada`, `bloqueante`) y, si no es
«pendiente», una justificación escrita que **cite la fila**, verificado como que nombre
el LOC o una de las accesiones de esa fila. Es un piso mecánico y grosero —se cumple
pegando una accesión— pero distingue una justificación escrita sobre esa fila de un
párrafo genérico copiado a todas, y rechaza la forma más barata de aceptar una alerta,
que es reescribir una palabra y dejar el texto de relleno. `bloqueante` también pasa la
compuerta: bloquear es decidir, y el estado lo dice.

`[M]` **Y acá aparece lo que no estaba escrito en ningún lado: de qué umbral obliga a
justificar depende casi todo.** D48 habla textualmente de «cada coincidencia perfecta de
21 nt»; la tabla informa además el bloque de ≥ 19 nt porque D28 lo manda, pero D48 no se
pronuncia sobre él. Corrida sobre las doce regiones:

| Umbral que obliga | Regiones que pasan | Frenadas | De ellas, vigentes |
|---|---|---|---|
| `perfecto_21` (D48 literal) | 9 de 12 | 3 | **0** |
| `perfecto_ge19` (umbral laxo de D28) | 3 de 12 | 9 | **4** |

`[H]` Con el umbral de D48 literal la compuerta confirma lo que dice §1: las tres
frenadas son `BicC_Dm` 264-563 y `ATPaseD_Dm` 151-450 y 137-436, exactamente las que el
veto ya descartaba, y **ninguna región vigente se mueve**. Con el umbral laxo, en cambio,
se frenan cuatro de las seis vigentes —`MP_MRFV` 72-271, `BicC_Dm` 922-1221, `ATPaseD_Dm`
72-371 y `eth_Dm` 114-313— que hoy recomendamos sin que nadie haya escrito un párrafo
sobre sus alertas de ≥ 19 nt. La diferencia entre «D48 no toca lo que recomendamos» y
«D48 congela cuatro de las seis recomendadas» es enteramente esa elección, y es una
decisión que no está tomada. Por eso el umbral es un parámetro de la función y no una
constante, y por eso van las dos cifras.

Se reproduce con `python research/ola4/M6_alertas/scripts/compuerta.py`; la salida está
en `resultados/compuerta.json` y las once verificaciones de la compuerta, en
`tools/sifi21_port/test_alertas.py` §7.

## 6. D59, las dos cifras

`[M]` Todo conteo de esta tabla va con su descuento de baja complejidad, y el descuento es
**cero en las 17 filas**. No se remidió: M5 ya corrió el criterio de
`sifi_plus/complejidad.py` sobre los seis genes y encontró **0 ventanas de baja
complejidad sobre las 5.765 ventanas de los seis genes** —1.243, 508, 2.500, 471, 595 y
448—, con homopolímero máximo de 7 nt contra un umbral de 10 y mínimo de 3 bases distintas
contra un umbral de 2
(`research/ola4/M5_dos_ejes/resultados/complejidad_seis_genes.json`). Si ninguna ventana
del gen es de baja complejidad, ninguna ventana de ninguna región suya puede serlo: el
descuento de cada fila se deriva de esa medición y la columna `complejidad_fuente` la
cita. El criterio de complejidad es nuestro `[H]` y sigue pendiente de contrastar contra
`dustmasker`.

## 7. Anclas y reproducibilidad

Las anclas corren **antes** de cualquier medición y abortan el script si fallan.

| Ancla | Qué verifica | Resultado |
|---|---|---|
| A1 | conteos del gen entero contra `ranking_v2.json`, seis genes | 162 de 162 `[M]` |
| A2 | barridos con los pesos de D18 sin partir | 51 de 51 `[M]` |
| A3 | las seis cifras de M7 §5 | 3 de 3 regiones, los dos umbrales `[M]` |
| A4 | conteos por región y referencia contra las fichas publicadas | 68 de 68 `[M]` |
| A5 | la tabla agrupada contra la matriz por ventana | 30 de 30 `[M]` |
| A6 | la identidad colapsada reproduce la matriz de `work/sifi_v2` | 187 celdas, 0 faltan, 0 sobran `[M]` |

A6 es la que sostiene el desarrollo nuevo: conservar la identidad del transcripto **no
cambió ningún conteo**, y `test_alertas.py` lo verifica además comparando
`escanear_con_identidad()` contra `escanear()` sobre la misma referencia.

Se reproduce desde la raíz del repositorio, con el entorno `w5bio`:

    python research/ola4/M6_alertas/scripts/identidad.py      # ~1 h, escribe work/
    python research/ola4/M6_alertas/scripts/tabla_alertas.py  # ~20 s
    python tools/sifi21_port/test_alertas.py

El primero tarda porque escanea las seis referencias del panel más el genoma del vector;
su salida vive en `work/m6_alertas/` y **no se versiona** (insumos locales). Los dos
umbrales de D28 alcanzan para la tabla de alertas, así que **no se corre `--mm1`**.

## 8. Lo que decide el usuario

Nada de esto lo cierra esta línea. Queda sobre la mesa, con la fila que lo hace
discutible: qué alertas se aceptan con justificación y cuáles siguen siendo bloqueantes;
qué valor de exposición toma *H. vitripennis*, que es el que decide si las tres filas de
21/21 se leen como señal de conservación o como riesgo ecológico; si `ATPaseD_Dm` 137-436
vuelve a ser candidata; y si el umbral de alerta de `region_scoring.py` se alinea con D28.
Las dos columnas de decisión de `alertas.tsv` están en «pendiente» y así se entregan.
