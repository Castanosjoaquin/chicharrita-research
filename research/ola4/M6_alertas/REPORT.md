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

---

## Addendum (2026-10-26) — las diecisiete firmadas, y dónde vive la firma

Esta línea entregó la tabla **en «pendiente» a propósito**: construir el mecanismo y decidir
con él son dos cosas distintas, y M6 hizo la primera. La segunda la cierra `D68`, después de que
la reunión del checkpoint 2 diera el argumento que faltaba para las tres filas de
*Homalodisca vitripennis*.

### El problema de persistencia, que había que resolver primero

`scripts/tabla_alertas.py` reconstruye `alertas.tsv` entero en cada corrida y escribía
`decision_usuario = "pendiente"` **fijo**. Una firma escrita a mano sobre esa tabla **se perdía la
próxima vez que alguien corría el script**, sin aviso y sin diff que lo explicara, porque el
archivo volvía a su estado de fábrica `[M]`. O sea que el mecanismo que D48 monta para que no
saber cueste algo se desarmaba solo.

La firma vive ahora en [`decisiones.tsv`](../decisiones.tsv), que es **entrada** del generador y
no salida suya, y por eso está fuera de `resultados/`, que se reescribe entera. El volcado está en
`tools/sifi21_port/alertas.py` (`leer_decisiones`, `aplicar_decisiones`) y tiene las dos formas de
fallar cerradas:

| Qué pasa | Qué hace | Por qué |
| --- | --- | --- |
| una firma no corresponde a ninguna fila | `FirmaHuerfana` | la tabla cambió debajo de la firma: la región se retiró, el organismo salió del panel o el gen impactado es otro |
| los conteos de la fila cambiaron desde que se firmó | `FirmaVencida` | una fila que pasa de 0 a 5 coincidencias perfectas **no es la fila que alguien aceptó**, y heredar el «aceptada» sería el default invertido otra vez |

`[M]` **La clave de una firma es región × organismo × gen impactado, y el cuarto campo no es
decorativo:** en `ATPaseD_Dm` 72-371 hay **dos** filas de *Homo sapiens* —`LOC107984331` y
`PDE1C`— y lo mismo en 137-436. Con la clave de región × organismo que parecía natural, firmar una
habría firmado la otra sin que nadie la leyera. Está cubierto por una prueba.

### El resultado

`[M]` **Catorce aceptadas y tres bloqueantes**, cero pendientes. Las tres bloqueantes son las
únicas con coincidencia perfecta de 21 nt, las tres contra el ortólogo del gen que se silencia en
*H. vitripennis*, y las tres sobre regiones que el proyecto no recomienda.

`[M]` Con las diecisiete firmadas, `exigir_decidida()` pasa sobre **las seis regiones vigentes en
los dos umbrales de D28**. Eso mueve la pregunta abierta que esta línea dejó en su addendum
anterior: con el umbral literal nada se movía, pero con el laxo **cuatro de las seis vigentes
quedaban frenadas por no tener firma**, y ahora pasan por tenerla. Qué umbral adopta la compuerta
sigue sin decidirse; lo que ya no pasa es que frene por omisión.

`estado_regiones.tsv` gana dos columnas, `estado_firmado_21` y `estado_firmado_ge19`. La vieja
`estado_D48` se deja como estaba: es lo que el motor puede decir solo y por diseño **nunca** dice
«aceptada» (ver el docstring de `ejes_separados.estado_region`).

### Verificación

- `tabla_alertas.py` corrido dos veces seguidas: las cinco anclas pasan (A1 162/162, A2 51/51,
  A3 3/3, A4 68/68, A5 30/30), las diecisiete quedan firmadas y **`alertas.tsv` sale idéntico byte
  a byte** `[M]`. Es la prueba de que regenerar ya no borra la firma.
- `test_alertas.py` pasa, con nueve verificaciones nuevas en §8. La §6 queda **salteada y
  declarada** en esta máquina: el ancla de identidad necesita `pyahocorasick`, que no está. El
  import se movió detrás de un `try` para que la falta de esa dependencia no impida correr las
  pruebas que no la usan, que son todas las demás.

### Lo que esta firma no dice

No dice que ninguna región sea segura. Dice que fueron leídas, por quién y con qué argumento. El
límite viaja en cada justificación: se midió **coincidencia exacta** de 21 nt, no apareamiento
parcial ni efecto de tipo miARN `[?]`.

## Addendum (2026-10-27) — la compuerta pasa a llamarse desde el port, y el umbral queda elegido

§5 bis dejó dos cosas abiertas y las dos se cierran acá. Era D69, y es la línea `R2` del plan de
cierre.

**La compuerta se llama desde donde se produce una recomendación.** Hasta hoy la única llamada a
`exigir_decidida()` fuera de la prueba estaba en `scripts/compuerta.py`, que es el inventario de
esta línea y no produce ninguna recomendación `[M]`. Ahora la llama
`ranking.region_recomendada()`, en `tools/sifi21_port/ranking.py`: el único punto del port donde
el primer puesto de `alternativas()` se convierte en una región recomendada. Antes esa conversión
estaba escrita **tres veces, idéntica** —el nivel 3 de `ranking.cmd_ranking` y las dos rutas de
`ranking_v2`— y ninguna consultaba esta tabla. Una región con una fila en «pendiente» ya no sale
de ahí.

**El umbral elegido es `perfecto_21`, y la elección costó lo que §5 bis decía que costaba.** La
medición de §5 bis se rehizo con el estado de firma como segunda variable, con
`scripts/umbral_compuerta.py`, y su salida queda en `resultados/umbral_compuerta.json`:

| Estado de la tabla | `perfecto_21` (D48 literal) | `perfecto_ge19` (laxo de D28) |
| --- | --- | --- |
| con las diecisiete firmas | pasan **12 de 12**, tres bloqueantes, ninguna vigente | pasan **12 de 12**, las mismas tres |
| con las diecisiete en «pendiente» | pasan **9 de 12**, ninguna vigente frenada | pasan **3 de 12**, y frena **cuatro de las seis vigentes** |

`[M]` El renglón de abajo reproduce exacto la tabla de §5 bis, que es de antes de las firmas, así
que las dos lecturas que circulaban por separado —«9 de 12 contra 3 de 12» y «cuatro de las seis
vigentes»— son dos columnas de la misma medición y no dos mediciones distintas.

`[H]` Se adopta el literal porque es el único de los dos sobre el que hay decisión escrita: D48
habla textualmente de la coincidencia perfecta de 21 nt, y D28 fijó el piso de 19 declarando que
a ese largo la convención del campo no tiene experimento detrás. Y se adopta **ahora** porque con
las firmas puestas los dos umbrales dan el mismo resultado operativo, o sea que elegir uno no
mueve ninguna región ni ninguna cifra publicada. El otro umbral queda a un parámetro de
distancia, no a una edición de código.

**Lo que la compuerta sigue sin poder hacer cumplir.** No distingue «se tamizó y no hay alertas»
de «no se tamizó»: una región que no tiene ninguna fila en `alertas.tsv` pasa como «sin alertas en
este umbral». Lo que queda protegido son las **doce** regiones de esta tabla y no una propuesta
nueva —el caso concreto es el ranking a 22 nt, cuyas seis recomendadas no están en el
inventario— `[M]`. Cerrarlo pide exigir presencia en el inventario, y eso haría fallar una corrida
cuyo resultado está publicado, así que quedó anotado en `00_meta/PREGUNTAS_ABIERTAS.md` y no se
hizo por cuenta propia.

### Verificación

- `python tools/sifi21_port/test_alertas.py` pasa, con la §9 nueva: la recomendación falla con la
  fila en «pendiente», pasa firmada, los dos umbrales de D28 no dan lo mismo sobre la misma fila,
  una tabla ausente falla cerrada, y **ninguna de las tres rutas del port rearma la región a
  mano** —esta última es estructural, y hace falta porque la forma de desactivar la compuerta sin
  tocarla es volver a escribir al lado la expresión que reemplazó—. Siguen salteadas y declaradas
  la §5 (falta `work/sifi_v2/`) y la §6 (falta `pyahocorasick`).
- `python research/ola4/M6_alertas/scripts/compuerta.py` sigue dando 12 de 12 en los dos umbrales,
  con las tres bloqueantes, sin cambios.
- `ranking.py` y `ranking_v2.py` **no se pudieron correr de punta a punta en esta máquina**: les
  falta `work/sifi_v2/`, que no se versiona. Quedan verificados por el `--help` de los dos y por
  la §9, que ejerce la compuerta con la tabla real y con tablas sintéticas.

## Addendum (2026-10-27) — las seis regiones de 22 nt entran al inventario, y la compuerta exige presencia

Este addendum cierra `R7` (issue #30) y ejecuta `D70` en el orden que esa decisión fijó: primero el
tamizado, después el apriete. El resultado se resume en una frase: las seis regiones que el ranking
recomienda a 22 nt **ya están tamizadas**, cinco de ellas pasan la compuerta y una no, porque tiene
una coincidencia perfecta de 21 nt que nadie había visto.

### Por qué el orden no era negociable, ahora con el número

`D69` dejó la compuerta llamada desde `ranking.region_recomendada()` pero con un agujero declarado:
`exigir_decidida()` no podía distinguir «se tamizó y no hay alertas» de «no se tamizó», porque desde
`alertas.tsv` los dos casos son las mismas cero filas. El costo de apretar la compuerta antes de
tamizar quedó medido: con el inventario de doce regiones que había hasta ayer y la compuerta ya
exigiendo presencia, la corrida a 22 nt no produce **ninguna** recomendación —las seis levantan
`RegionNoTamizada`— mientras que la de 21 nt sigue dando sus seis `[M]`. Tamizando primero, en
cambio, frena una sola. Esa es la diferencia entre cerrar un agujero y romper la única ruta que
produce esas regiones.

### Lo que se tamizó

Las seis coordenadas salen de `research/ola3/C7_ranking_v2/resultados/ranking_v2.json`, clave
`k.22.regiones_recomendadas`, y entraron a la lista `REGIONES` de `scripts/tabla_alertas.py`, que
pasa de doce a dieciocho entradas. Van al final de la lista a propósito: el orden de esa lista es el
orden de las filas de `alertas.tsv`, así que agregarlas no mueve ni una línea de las que ya estaban
—verificado, las primeras dieciocho líneas del archivo son idénticas byte a byte a las de antes del
cambio `[M]`—. La columna `vigente` dice «no» en las seis: las vigentes siguen siendo las seis de
21 nt, y entrar al inventario no es ser recomendada.

No hizo falta volver a tamizar nada: `scripts/identidad.py` escanea los **genes enteros** contra el
panel de seis referencias y el genoma del vector, no regiones, así que las posiciones de las seis
ventanas nuevas ya estaban en `work/m6_alertas/identidad_por_ventana.tsv`. Lo que cambia al agregar
una región es de dónde a dónde se recorta esa matriz. Se corrió igual, para verificar que el insumo
no estuviera viejo, y reprodujo el archivo anterior byte a byte con su ancla A3 intacta —187 celdas,
cero faltantes, cero sobrantes `[M]`—.

Las cinco anclas siguen enteras y ninguna se desactivó: A1 162 de 162, A2 51 de 51, A3 3 de 3, A4
**74** de 74 (eran 68: las seis regiones nuevas agregan seis comparaciones) y A5 **40** de 40 (eran
30) `[M]`.

### Lo que dio: cuatro regiones con alertas, dos limpias, y un acierto perfecto de 21 nt

La tabla pasa de 17 a 23 filas. Seis filas nuevas, sobre cuatro de las seis regiones:

| región de k=22 | organismo | gen impactado | 21/21 | ≥ 19 nt |
| --- | --- | --- | ---: | ---: |
| `MP_MRFV` 162-361 | *Folsomia candida* | `LOC110856645`, sin caracterizar | 0 | 3 |
| `CP_MRFV` 77-276 | — | — | 0 | 0 |
| `BicC_Dm` 2119-2418 | humano | `SLC24A4` | 0 | 3 |
| `BicC_Dm` 2119-2418 | maíz | `lox2`, lipoxigenasa | 0 | 3 |
| `ATPaseD_Dm` 71-370 | humano | `LOC107984331`, sin caracterizar | 0 | 4 |
| `ATPaseD_Dm` 71-370 | humano | `PDE1C`, fosfodiesterasa | 0 | 3 |
| `eth_Dm` 193-392 | *Homalodisca vitripennis* | `LOC124369889`, quitinasa 2 probable | **1** | 5 |
| `bursA_Dm` 44-243 | — | — | 0 | 0 |

`[M]` Las dos regiones sin fila —`CP_MRFV` 77-276 y `bursA_Dm` 44-243— **se tamizaron y no dieron
ningún acierto**, y conviene detenerse en ellas porque son la razón de ser de todo este addendum:
en `alertas.tsv` son indistinguibles de una región que nunca se miró. Lo único que las separa es
estar en el inventario.

**El hallazgo, dicho con todas las letras: `eth_Dm` 193-392 tiene una coincidencia perfecta de
21 nt contra *Homalodisca vitripennis*, en la posición 347 del gen, sobre los transcriptos
`XM_046828031.1` y `XM_046828033.1`** `[M]`. Es la cuarta región del inventario con un acierto de
21/21 perfecto, y la primera que aparece entre las que el ranking propone en alguna de sus dos
corridas. Tres cosas al lado, para no leerla ni más ni menos de lo que dice:

- el gen impactado es una **quitinasa probable**, no el ortólogo de `eth`, así que la fila se
  clasifica como `gen_no_relacionado`. La regla que lo decide es nuestra y mira texto de cabecera
  `[H]`, no homología por alineamiento;
- la ventana **no** está entre las predichas eficientes: 1 ventana con 21/21 perfecto y 0 de esas
  eficientes `[M]`. Por `D17` la predicción de eficiencia no entra al criterio, así que esto no la
  descarta ni la salva; es contexto;
- la región vigente del mismo gen, `eth_Dm` 114-313, tiene **cero** aciertos de 21/21 `[M]`. O sea
  que correr la ventana de 114-313 a 193-392 **introduce** un acierto perfecto que la región
  vigente no tiene. Eso es información sobre la corrida de 22 nt, no sobre el gen: `[H]` si alguna
  vez se quisiera adoptar la propuesta de 22 nt para `eth_Dm`, esta fila es exactamente la clase de
  cosa que `D48` quiere que alguien lea antes y no después.

Y un detalle que no es menor: el organismo de esa fila es *H. vitripennis*, cuyo peso de exposición
es la decisión abierta del usuario —0,00 por `D47` y 0,60 por `D18`—. La fila lleva los dos valores,
como todas, así que se puede leer con cualquiera de los dos sin recalcular la tabla.

### Si la corrida a 22 nt pasa o queda frenada, y por qué

**Queda frenada, y el motivo es una sola región.** Con el umbral literal de `D48` —`perfecto_21`,
que es el que `D69` adoptó— cinco de las seis pasan y `eth_Dm` 193-392 levanta `AlertaSinDecidir`.
Con el umbral laxo de `D28` frenan cuatro de las seis `[M]`:

| corrida | `perfecto_21` (D48 literal) | `perfecto_ge19` (umbral laxo de D28) |
| --- | --- | --- |
| k=21, las seis vigentes | pasan **6 de 6** | pasan **6 de 6** |
| k=22, las seis recomendadas | pasan **5 de 6**: frena `eth_Dm` 193-392 | pasan **2 de 6**: frenan `MP_MRFV` 162-361, `BicC_Dm` 2119-2418, `ATPaseD_Dm` 71-370 y `eth_Dm` 193-392 |

`[M]` Lo que frena el umbral literal lo frena también el laxo, que es lo esperable porque los dos
umbrales de `D28` están anidados por construcción.

Que quede frenada es el comportamiento buscado y no un obstáculo que haya que sortear. Las seis
filas nuevas salen en «pendiente» porque `aplicar_decisiones()` deja en pendiente toda fila sin
firma, y **las firmas no se autogeneran ni se escribieron acá**: firmar es una decisión del equipo
—`D48` la pide por escrito y citando la fila, `D68` la ejerció caso por caso— y una firma puesta
desde la línea que agregó las filas sería exactamente el default invertido que `D48` vino a
corregir. Lo que hace falta para destrabar la corrida de 22 nt es que alguien lea la fila de
`eth_Dm` 193-392 y la acepte o la bloquee con su argumento.

### La compuerta, después del tamizado

`exigir_decidida()` pasa a pedir el inventario de regiones tamizadas además de la tabla, y una
región ausente levanta `RegionNoTamizada`, hermana de `AlertaSinDecidir` bajo una base común
`CompuertaCerrada`. El inventario es `resultados/estado_regiones.tsv` —la otra salida del mismo
generador, y la única que puede decir «tamizada, cero aciertos»— y el port lo busca al lado de la
tabla, de modo que `--alertas` mueve las dos cosas juntas: una tabla sin su inventario al lado es
media entrada y falla cerrada, igual que una tabla ausente desde `D69`.

El parámetro es **obligatorio y por nombre**. Es la decisión de diseño que importa de este cambio:
una compuerta cuyo parámetro de presencia tuviera un valor por defecto se desactivaría olvidándolo,
en silencio, y olvidarlo tiene que ser un `TypeError` ruidoso. Lo que antes era un pase ahora es un
error de programa.

### Qué cifra publicada se movió, y qué no

**Ninguna se movió.** Los dos pares de números de `D69` se conservan como la restricción a las doce
regiones de entonces, y lo que cambia son los denominadores, porque el inventario creció `[M]`:

| estado de la tabla | umbral | antes (12 regiones) | ahora (18 regiones) |
| --- | --- | --- | --- |
| con las firmas de `D68` | `perfecto_21` | 12 de 12 | **17 de 18** (las mismas 12, más 5 nuevas) |
| con las firmas de `D68` | `perfecto_ge19` | 12 de 12 | **14 de 18** (las mismas 12, más 2 nuevas) |
| todas en «pendiente» | `perfecto_21` | 9 de 12 | **14 de 18** (las mismas 9, más 5 nuevas) |
| todas en «pendiente» | `perfecto_ge19` | 3 de 12 | **5 de 18** (las mismas 3, más 2 nuevas) |

Y la cifra que había que cuidar con nombre propio: **`jaccard_21_22` no se movió** `[M]`. El archivo
`research/ola3/C7_ranking_v2/resultados/ranking_v2.json` quedó intacto, verificado con `git diff`.
La razón por la que no podía moverse es estructural y conviene dejarla escrita: `ranking_v2.jaccard()`
cuenta ventanas eficientes del **gen entero** leyéndolas de los TSV de ViennaRNA en `work/`, sin
pasar por la tabla de alertas ni por `region_recomendada()`, así que la compuerta no lo toca.

**Lo que sí cambia, y hay que decirlo:** `ranking_v2.py` calcula `jaccard_21_22` recién después de
las dos pasadas de `correr_k()` y escribe el JSON al final, así que **una regeneración de ese
archivo con el estado de hoy quedaría frenada en la pasada de k=22** antes de llegar a escribirlo.
El valor publicado no se mueve porque nada lo sobreescribe, pero el generador no lo puede reproducir
mientras la fila de `eth_Dm` 193-392 siga sin firma. Es la consecuencia directa y prevista de `D70`,
y la salida es firmar esa fila, no aflojar la compuerta.

Eso es lo que **se deduce leyendo el código**, y hay que marcar el límite: en esta máquina la
regeneración no se pudo correr para verlo, porque falta `work/sifi_v2/salida_k22` —están los
perfiles de ViennaRNA de k=21 y no los de k=22— y la corrida se detendría en ese insumo faltante
**antes** de llegar a la compuerta `[M]`. Lo que sí está medido es el comportamiento de la compuerta
en sí: `region_recomendada()`, llamada con las seis coordenadas publicadas de k=22 y contra la tabla
real, frena `eth_Dm` 193-392 y deja pasar las otras cinco `[M]`. O sea que el número publicado está
verificado intacto, el freno de la compuerta está medido, y lo único inferido es el orden en que
fallaría una regeneración completa `[H]`.

### Verificación

- `python tools/sifi21_port/test_alertas.py` pasa: **94 comprobaciones** con el entorno conda y
  ninguna salteada `[M]`. La §7 gana el par que es el núcleo de esto —la misma consulta, con cero
  filas en los dos casos, pasa o frena según el inventario— más la región ausente, la exigencia de
  presencia en los dos umbrales, la jerarquía de excepciones, el `TypeError` por olvidar el
  inventario y el inventario ausente que falla cerrado. La §9 gana la versión de puerto a puerto:
  `region_recomendada()` con una región fuera del inventario levanta `RegionNoTamizada`, y la misma
  región con el inventario que sí la tiene devuelve `(193, 392)`. Las pruebas de persistencia de
  firmas de la §8 siguen pasando y ahora verifican además que las diecisiete firmas de `D68` se
  aplican cada una sobre su fila con seis filas nuevas en la tabla: si agregar regiones hubiera
  corrido una fila debajo de una firma, `aplicar_decisiones()` habría levantado `FirmaVencida` o
  `FirmaHuerfana` antes del `check`.
- **La §6 ya corre.** Era la salteada por falta de `pyahocorasick`; instalado el módulo en el
  entorno conda, el ancla de identidad corre y pasa `[M]`. Con `/usr/bin/python3` sigue salteada y
  declarada, porque ese intérprete no tiene el módulo: las pruebas pasan en los dos, con 94
  comprobaciones en uno y la §6 declarada en el otro.
- `scripts/tabla_alertas.py` corrido **dos veces seguidas** da `resultados/` idéntico byte a byte,
  y la cadena entera —`tabla_alertas.py`, `compuerta.py`, `umbral_compuerta.py`— también `[M]`. Es
  la prueba de que regenerar la tabla no borra ninguna firma, que es el modo de fallar que `D68`
  tuvo que cerrar moviendo las firmas a un archivo de entrada.
- Antes de producir una sola salida nueva se verificó que el intérprete del entorno conda
  —Python 3.11.17, el único que tiene `RNA`, `Bio` y ahora `ahocorasick`— **reproduce lo ya
  commiteado**: las tres corridas de `M6` con ese intérprete dejaron el árbol de git limpio, y
  `identidad.py` reprodujo su tabla de `work/` byte a byte `[M]`. Las salidas de este addendum no
  arrastran ninguna diferencia de intérprete.
- `ranking_v2.py` sigue **sin poder correrse de punta a punta en esta máquina**, y el motivo es más
  acotado de lo que decía el addendum anterior: `work/sifi_v2/` **sí** existe —de ahí salen la
  matriz por ventana y los perfiles que usan `identidad.py` y las anclas— pero falta
  `work/sifi_v2/salida_k22`, los perfiles de ViennaRNA de la corrida de 22 nt, que no se versionan
  `[M]`. La compuerta queda ejercida por la §9 contra la tabla real y contra tablas sintéticas, que
  es donde se mide el comportamiento que cambió.

### Addendum del addendum (2026-10-27, más tarde) — la fila de `eth_Dm` 193-392 queda firmada

El equipo firmó la fila que el addendum anterior dejó frenando la corrida de 22 nt. El veredicto es
**`bloqueante` con la condición como parte de la firma** —bloqueante mientras la exposición de
*Homalodisca vitripennis* siga siendo una decisión abierta—, que es la forma que `D68` ya había
usado para `ATPaseD_Dm` 137-436. El ADR es `D73`; `decisiones.tsv` pasa de diecisiete a dieciocho
entradas y las otras cinco filas de las regiones de 22 nt **siguen en «pendiente»**.

Por qué el precedente no alcanzaba para deducir el veredicto, que es lo que hizo falta decidir
explícitamente `[M]`:

| | las 14 aceptadas de `D68` | las 3 bloqueantes de `D68` | `eth_Dm` 193-392 |
| --- | --- | --- | --- |
| ventanas con 21/21 perfecto | 0 en todas | ≥ 1 en las tres | **1** |
| organismo | humano, maíz, *D. maidis* | *H. vitripennis* en las tres | ***H. vitripennis*** |
| gen impactado | no relacionado | **ortólogo del blanco** en las tres | **no relacionado** (quitinasa 2 probable) |
| en ventana predicha eficiente | — | 2 de 3 en dos de las filas | **no**, 0 de 1 |

Comparte con las bloqueantes el umbral y el organismo, y con las aceptadas el que el gen impactado
no sea el ortólogo. Ninguna regla derivada de las firmas anteriores la decide.

**El estado de la compuerta después de la firma** `[M]`:

| | `perfecto_21` (D48 literal) | `perfecto_ge19` (umbral laxo de D28) |
| --- | --- | --- |
| regiones que pasan | **18 de 18** | **15 de 18** |
| frenadas | 0 | 3, ninguna vigente: `MP_MRFV` 162-361, `BicC_Dm` 2119-2418, `ATPaseD_Dm` 71-370 |
| de las que pasan, bloqueantes | **4** (eran 3), ninguna vigente | 4, ninguna vigente |

La corrida de 22 nt ya no levanta `AlertaSinDecidir`: las seis regiones pasan la compuerta. Las
primeras veintitrés líneas de `alertas.tsv` quedaron idénticas byte a byte y lo único que cambió es
la línea de esa fila, con su decisión y su justificación `[M]`. `jaccard_21_22` sigue intacto. La
cadena entera vuelve a ser idempotente y `test_alertas.py` pasa.

#### Lo que la firma destapa, y que antes no se podía ver

Pasar la compuerta y poder usarse no son lo mismo, y hasta hoy esa distinción era teórica. Las tres
regiones que `D68` firmó bloqueantes **no las recomienda ninguna de las dos corridas** del ranking,
así que la regla de `D69` —«bloquear es decidir, y el que llama tiene que descartarla»— nunca se
ejerció sobre una recomendación real. Con esta firma sí: **`eth_Dm` 193-392 es la primera región
bloqueante que una corrida del ranking efectivamente recomienda**, y `ranking.region_recomendada()`
**la devuelve igual** —verificado, devuelve `(193, 392)`— porque descartar no es su trabajo `[M]`.

O sea que el modo de fallar se corrió un casillero: ya no es «se recomienda una región cuya alerta
nadie leyó» —eso lo cerraron `D48`, `D69` y `D72`— sino «se recomienda una región cuya alerta
alguien leyó **y bloqueó**». La compuerta hace exactamente lo que `D69` decidió que hiciera, y el
que tendría que descartar es quien consuma la recomendación. Queda anotado en
`00_meta/PREGUNTAS_ABIERTAS.md` y **no se cambió acá**: tocarlo sería revisar `D69` de paso, en una
corrida cuyo objeto era firmar una fila.
