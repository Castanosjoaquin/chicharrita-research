# F4 — Preregistro: qué par de candidatos es elegible, declarado antes de enumerar ninguno

**Fecha y hora de escritura:** 2026-10-27, 19:05 (−03). **Issue:** #39.
**Máquina:** la de Santino, Windows 11 Pro for Workstations 10.0.26300 (`D71` pide que el
nombre de la máquina viaje en la misma oración que la afirmación de entorno; es la entrada 68).
**Qué se preregistra:** la **regla de elegibilidad** de un par de candidatos para armar una
quimera por mecanismo, de dónde sale —y de dónde **no** sale—, qué dice la salida sobre el
respaldo de cada mecanismo, y las tres anclas que tienen que pasar antes de leer un número
nuevo. Se escribe y se commitea **antes de enumerar un solo par**.

## 1. Por qué este preregistro existe, y por qué es sobre la elegibilidad y no sobre el orden

`O4` ya preregistró lo que había que preregistrar sobre el **orden**: el objetivo es obligatorio,
no tiene default y viaja en cada fila. Esta línea no toca nada de eso y no agrega ningún
objetivo. Lo que esta línea agrega es el paso de **antes**: quiénes son los dos candidatos.

Hasta ahora eso se elegía a mano. Las combinaciones de `O3` se eligieron por `D67` y por qué
secuencia había disponible, y el enumerador de `O4` recibe el eje de fenotipo de cada gen como
dos cadenas escritas en la línea de comandos —`--eje BicC_Dm=reproduccion:C5/DM-01`—. Eso fue
correcto mientras el eje no existía en forma legible por máquina, y su propio preregistro lo
declara así: «el eje de fenotipo es entrada declarada, no inferencia». Desde `F3` existe
`research/ola6/F3_recomendador_genes/resultados/eje_fenotipo.tsv`, con la asignación de
mecanismo de las 36 filas del catálogo de `C5`, la frase textual de la fuente al lado y un
script que **falla** si alguna frase no está en el catálogo.

El riesgo que este preregistro existe para cerrar es concreto y tiene precedente en el
repositorio. Si la lista de quién entra se escribe a mano —aunque sea una lista correcta hoy—
queda muerta: cuando el catálogo cambie, la lista sigue publicando la asignación vieja sin
romperse. Es la misma forma del agujero que `D48` dejó abierto y que `D69` cerró: **una tabla
que no frena nada deja lo no leído operativamente igual que lo aceptado.** Acá la versión
específica del agujero es peor que un pendiente, porque dos de las 36 filas tienen el signo
invertido: silenciarlas **aumenta** la colonización del vector por el patógeno (`CI-08` y
`CI-13`, entrada 66). Una lista escrita a mano que se olvide de sacarlas no produce un número
flojo, produce una quimera peor que no hacer nada.

Entonces la regla de elegibilidad **se deriva de las columnas de la propia tabla** y ningún
identificador de candidato se escribe en el código que decide. Eso es verificable y se verifica:
§6 lo pone como prueba estructural.

## 2. La regla de elegibilidad, y el triple candado

Un candidato es **elegible** si y sólo si las tres condiciones valen sobre su fila de
`eje_fenotipo.tsv`:

1. `etiqueta_de_ausencia` está **vacía**;
2. `entra_al_orden_por_fenotipo` vale `si`;
3. `mecanismos` no está vacío y cada uno de sus mecanismos es uno de los cuatro de `F3`.

Las tres dicen lo mismo por tres caminos, y eso es a propósito: la corrida **aborta** si una
fila no las tiene coherentes entre sí. Una fila con etiqueta y mecanismo a la vez, o sin ninguno
de los dos, no es un caso a resolver con una preferencia: es una tabla que cambió de semántica,
y lo que corresponde es parar.

Lo mismo con el vocabulario. Los cinco valores de etiqueta de `F3` —`sin_fenotipo_publicado`,
`sin_fenotipo_atribuible_al_blanco`, `fenotipo_invertido`, `potenciador_de_entrega`,
`fenotipo_fuera_de_los_cuatro`— y los cuatro mecanismos —`reproduccion`, `movilidad`,
`letalidad`, `transmision`— quedan declarados acá. Si la tabla trae una etiqueta o un mecanismo
que no está en esa lista, **la corrida aborta y lo nombra**. No se excluye en silencio ni se
admite en silencio: una etiqueta nueva puede significar cualquiera de las dos cosas y el
programa no tiene con qué decidirlo.

Lo que la regla **excluye por construcción**, que es lo que el issue #39 pide que no pueda
aparecer: los dos de signo invertido (`fenotipo_invertido`), los dos de mortalidad que su propia
fuente desatribuye del blanco (`sin_fenotipo_atribuible_al_blanco`, entrada 71) y el potenciador
de entrega sin fenotipo propio (`potenciador_de_entrega`). Quedan afuera **por su etiqueta y no
por su nombre**, junto con los cinco sin fenotipo publicado y el que cae fuera de los cuatro
mecanismos: once filas en total, que son las once de `fuera_del_orden.tsv`. La exclusión no les
pone puntaje negativo —`F3` ya decidió que un puntaje sugeriría que compiten— y tampoco los
esconde: la salida los lista con su etiqueta, porque saber qué se descartó y por qué es parte
del resultado.

## 3. Qué es un par, y qué no se decide acá

Un **par elegible** para el pedido «un mecanismo `X` con un mecanismo `Y`» es una asignación de
rol a dos candidatos **distintos**: el candidato `a` entra cubriendo `X`, el candidato `b` entra
cubriendo `Y`, con `X ≠ Y` y `a ≠ b`. Las decisiones de forma, declaradas ahora porque tomarlas
después de ver los pares sería elegir el resultado:

- **`X ≠ Y` es obligatorio.** Es `D67` —fenotipos que no se solapan— y es la misma condición que
  `O4` ya exige con `len({ejes}) < 2`. Pedir dos veces el mismo mecanismo aborta.
- **`a ≠ b`.** Un candidato no se empareja consigo mismo, incluso cuando tiene los dos
  mecanismos pedidos. Una quimera son dos fragmentos de **dos genes**.
- **El par no está ordenado; el orden de los genes es de `O4` y no de acá.** Que el fragmento
  izquierdo sea uno o el otro está medido que cambia el resultado —en `C13` las mismas dos
  regiones dan +3 y −3 ventanas según el orden, y en `O3` sólo uno de los dos órdenes fabrica
  riesgo— y por eso es un grado de libertad de la grilla de `O4`, que lo enumera. Acá sería
  duplicar cada fila sin agregar información.
- **Lo que sí se enumera dos veces es la asignación de roles,** cuando los dos candidatos tienen
  los dos mecanismos: `{CI-01 como letalidad, CI-02 como reproducción}` y
  `{CI-01 como reproducción, CI-02 como letalidad}` son dos filas, porque el eje declarado de
  cada gen es distinto en cada una y es lo que `O4` escribe en sus columnas. Para que el número
  de filas no se lea como número de combinaciones biológicas, la salida reporta **las dos
  cuentas**: asignaciones y pares de genes distintos.

Lo que **no** se decide acá: cuál par conviene. No hay orden de calidad, no hay puntaje y no hay
primer puesto. Las filas salen en orden alfabético por identificador, y ese orden **no significa
nada** —se declara así para que sea reproducible, no para que se lea—. Elegir un candidato es
una decisión del equipo con su ADR, igual que en `O4`, `M5` y `M7`, y antes de eso hay un paso
que esta línea no puede saltear: el inventario de alertas de `M6`, donde la clave de juntura que
`D78` le dio a una quimera **todavía no está implementada** (entrada 41, issue #35 parte 3).

## 4. El respaldo de cada mecanismo viaja en la salida, y por qué

El issue #39 lo pide y conviene decir el motivo, porque es el hallazgo de `F3` que esta línea
hereda: **`movilidad` tiene un solo candidato en las 36 filas**, `DM-02`, y su apoyo es la frase
«alas deformes» sin magnitud ni estadístico; `DM-03` es la otra subunidad de la misma bomba, en
la misma especie y con la misma vía de entrega, y ahí el efecto sobre alas **se midió y no dio
significativo** (entrada 70). Si el enumerador ofrece combinaciones de tres mecanismos sin decir
eso, las de movilidad se leen como una opción entre varias cuando son una sola fila con su
réplica más cercana en contra.

Entonces cada fila lleva, por rol, **cuántos candidatos elegibles sostienen ese mecanismo** y un
`si`/`no` de si el rol descansa en uno solo; y la corrida imprime la tabla de respaldo de los
cuatro mecanismos antes de cualquier par. Y la contraevidencia va declarada: una tabla chica de
`mecanismo → (fila, frase)` que el script **verifica contra la columna
`evidencia_negativa_medida` de la propia tabla** y aborta si la frase no está textual, que es el
candado que `F3` usó para las frases de apoyo. Hoy tiene una sola entrada, la de `movilidad`.
Aparte de eso, la corrida **cuenta** cuántas filas elegibles traen algún «no hubo efecto»
medido, que es cómputo y no declaración.

Dos lecturas más que la salida reporta porque sin ellas el par se lee mejor de lo que es, y las
dos son medidas y no opiniones:

- **Si los mecanismos de los dos candidatos se solapan.** `D67` pide fenotipos que no se
  solapan y `O4` lo implementa sobre los dos ejes **declarados**. Esa es la lectura vigente y
  esta línea no la cambia. Pero un par puede tener ejes declarados distintos y conjuntos de
  mecanismos solapados —`DM-02` es `letalidad|movilidad`— y entonces la segunda pata del par
  agrega menos de lo que su rótulo promete. Se informa por par; no se descarta.
- **La especie de cada mitad.** Los candidatos vienen de nueve especies y el blanco es
  *Dalbulus maidis*. Un par con una mitad de *Nephotettix cincticeps* es una quimera sobre el
  ortólogo en nuestra especie, que hay que tener y anotar (es la línea `F1`), no sobre el gen
  medido. Se informa la especie de cada mitad y si las dos son la del blanco.
- **Si la fila agrupa varios genes.** El catálogo tiene filas que son más de un gen —`DE-01` es
  `V-ATPase B` **y** `V-ATPase D`, y `DE-04` agrupa tres transportadores ABC con desenlaces
  **distintos**, donde la letalidad es de dos y la reproducción del tercero—. Una quimera se
  arma con un gen, no con una fila, así que una fila agrupada no es directamente un insumo. Se
  detecta por la frase `fila que agrupa` de la columna `nota`, que es texto que el script de
  `F3` ya verificó, y se **cruza** contra la forma del campo `gen`; si los dos detectores no
  coinciden sobre una fila elegible, la corrida aborta.

## 5. El cuarto mecanismo queda detrás de una puerta, y la puerta se declara ahora

`F3` publica `transmision` como categoría declarada con **cuatro** candidatos, y `D67` no la
tiene: define tres. La entrada 65 dice que ampliar `D67` **no es de esa línea**, y tampoco es de
ésta. Pero medir no es adoptar, así que:

- Un pedido que incluya `transmision` **aborta** por defecto, nombrando que falta el ADR.
- Con `--ampliar-d67` corre, y entonces **cada fila** de la salida lleva
  `ampliacion_de_d67_sin_adr = si`, el JSON lo lleva en su encabezado y la corrida lo imprime.
  Es la misma forma que `O4` le dio a la advertencia de `eficiencia_heredada`: el objetivo que
  el issue pide no vender existe para poder medir cuánto se pierde al no usarlo, y viaja con su
  condición pegada.
- La tabla de respaldo de los **cuatro** mecanismos se imprime siempre, con o sin la puerta,
  porque contar filas de una tabla no amplía ninguna decisión.

## 6. Las tres anclas que tienen que pasar antes de leer cualquier número nuevo

1. **Contra el reparto publicado.** El respaldo de los cuatro mecanismos sobre las filas
   elegibles tiene que dar **letalidad 16, reproducción 13, transmisión 4 y movilidad 1**, con
   **25** filas elegibles y **11** excluidas de 36. Son las cifras de la entrada 70 y del
   `REPORT.md` de `F3` §6, medidas por otro script.
2. **Contra las dos salidas de `F3`.** El conjunto de identificadores elegibles tiene que ser
   **exactamente** el de las 25 filas de `orden_genes.tsv`, y el de excluidos **exactamente** el
   de las 11 de `fuera_del_orden.tsv`. Es el ancla que prueba que la regla de §2 no es una lista
   escrita a mano que coincide por casualidad: se llega al mismo conjunto por otro camino y
   desde otro archivo.
3. **Contra `D67` y `O3`, que es la que conecta con `O4`.** Pedido el par
   `reproduccion + movilidad` restringido a *Dalbulus maidis*, el **único** par elegible tiene
   que ser `DM-01` cubriendo reproducción con `DM-02` cubriendo movilidad —que es exactamente lo
   que `O4` recibe hoy escrito a mano como `--eje BicC_Dm=reproduccion:C5/DM-01 --eje
   VATPaseB_Dm=movilidad:C5/DM-02`—, y el enumerador resuelto por esta vía tiene que escribir en
   sus columnas `eje_izq`/`eje_der` los mismos valores que la corrida publicada. Si el camino
   nuevo no reproduce el viejo en el único caso donde el viejo existe, el camino nuevo está mal.

**Prueba estructural, que acompaña a las tres:** ningún identificador de candidato
—`^[A-Z]{2}-\d{2}$`— puede aparecer como literal en el código ejecutable del selector; se
verifica recorriendo el AST del módulo y excluyendo los docstrings. Es la forma de desactivar
esta regla sin tocarla: volver a escribir al lado la lista que reemplaza. La prueba es del mismo
tipo que la última de `test_alertas.py` §9, y existe por el mismo motivo.

**Si una de las tres anclas no pasa, esta línea para y lo dice, sin leer ningún número nuevo.**

## 7. Lo que se toca de `O4`, y lo que no

El enumerador de `O4` tiene tres salidas commiteadas y un `test_enumerador.py` que afirma la
**lista exacta** de columnas, a propósito: agregar una columna hace fallar la prueba. Así que la
conexión entra por donde no mueve nada:

- Se agregan dos parámetros nuevos, `--mecanismos X,Y` y `--candidato ID=NOMBRE`, que
  **resuelven el eje de cada gen desde la tabla** en vez de recibirlo escrito. Son
  mutuamente excluyentes con `--eje`: pasar los dos aborta.
- **No se agrega ni se saca ninguna columna**, y el valor que va en `eje_izq`/`eje_der` es el
  mismo que escribía la vía vieja (ancla 3). Las tres salidas publicadas no se regeneran y no se
  mueven.
- Si el par pedido no es elegible, el enumerador **no enumera**: aborta nombrando el motivo que
  la tabla da —la etiqueta que excluye al candidato, o que el mecanismo no está en su fila—.
- El JSON de `O4` gana una clave **sólo cuando se usa la vía nueva**, de modo que una corrida
  por la vía vieja sigue produciendo el mismo archivo.
- `cuentas_de`, el tamizado de juntura, la máscara y el motor **no se tocan**. Nada de
  `tools/sifi21_port/` cambia.

## 8. Lo que esta línea no hace

- **No recomienda ningún par.** Enumera y mide; no ordena por calidad y no tiene primer puesto.
- **No afirma eficacia.** Hereda la condición de toda la cadena: el criterio de eficiencia de
  si-Fi21 **no está validado** en hemípteros —ρ = +0,142, IC95 [−0,247, +0,492], n = 29 `[M]`—
  así que un par elegible es una hipótesis sobre eficacia y no una prueba.
- **No decide si `movilidad` sigue siendo una pata del esquema** ni si el tercer eje debería ser
  transmisión. Esa es la pregunta de la entrada 70 y es para el investigador. Esta línea la deja
  medible, no contestada.
- **No amplía `D67`** y no escribe el ADR que la ampliación pediría.
- **No elige la secuencia de nada.** Un par elegible no es un par corrible: el enumerador
  necesita el gen entero de cada mitad, y en esta máquina sólo dos de los 25 candidatos lo
  tienen (`BicC_Dm` y `V-ATPase B`, en `work/O3/fasta/`). La salida dice cuántos pares son
  elegibles; cuáles son corribles lo dice el enumerador cuando se le pasan las rutas.
- **No toca ninguna cifra publicada.** Si un número de esta línea contradijera uno publicado,
  eso va a `00_meta/PREGUNTAS_ABIERTAS.md` y lo decide el equipo.

## 9. Confidencialidad

Esta línea **no lee ni una secuencia**: su única entrada es un TSV de identificadores,
mecanismos y frases de la fuente, todo versionado. No escribe ninguna base, no llama al motor de
plegado, no toca `work/` y no manda nada a ningún servicio. El bloque no necesita `.gitignore`
propio y `tools/verificacion/sin_secuencias.py` tiene que seguir en **6 hallazgos no
exceptuados**, que es la línea base.
