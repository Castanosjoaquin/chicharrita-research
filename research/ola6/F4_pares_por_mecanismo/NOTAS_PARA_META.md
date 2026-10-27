# F4 — notas para los archivos de memoria, separadas por destino

Estado al cierre de la línea, 2026-10-27. Todo lo que sigue está **ya aplicado** en los
archivos de `00_meta/`; esta página es el registro de qué fue a dónde y por qué, más lo que
es propio del bloque.

## A `DECISIONS.md`

**`D91` — el eje de fenotipo de una quimera se resuelve desde la tabla de `F3`, y la exclusión
es por etiqueta y no por identificador.** Aplicada. Las cuatro alternativas quedaron escritas
con su motivo, y la que importa descartar es la primera: escribir en el enumerador la lista de
elegibles y de excluidos. No se descartó por estilo sino porque no es verificable —no hay forma
de probar que una lista escrita a mano siga coincidiendo con la fuente— y porque el modo de
falla de este caso en particular no es un número flojo: dos de las 36 filas tienen el signo
invertido.

## A `PREGUNTAS_ABIERTAS.md`

Entradas **88 a 92**. La numeración arranca en 88 porque es el siguiente libre después del
máximo existente; el archivo tiene un **hueco entre la 75 y la 86** que esta línea no tocó y
que quedó anotado como nota de numeración en el propio archivo, para que el próximo que lo lea
no crea que se perdieron once entradas.

- **88** — el cuarto mecanismo no tiene **ni un** candidato en *Dalbulus maidis*, y eso le pone
  precio a la pregunta de la entrada 70: la elección es entre una pata que descansa en una fila
  de nuestra especie y una que descansa en cuatro de otras.
- **89** — la entrada 65 nombra cuatro filas de transmisión y la tabla publicada tiene otras
  cuatro; comparten dos y las dos listas tienen cuatro elementos, lo que vuelve la discrepancia
  fácil de no ver. No se editó la 65 porque es entrada de otra línea.
- **90** — «fenotipos que no se solapan» tiene dos lecturas y **las 15 de 15** combinaciones de
  letalidad con movilidad fallan la segunda. `F4` informa el solape y **no** cambió el criterio.
- **91** — cuatro filas del catálogo son más de un gen; hasta que no se diga cuál, los pares que
  las usan no son insumo del enumerador. Es falta de trabajo, no falta de fuente.
- **92** — **se corrigieron cuatro citas que apuntaban al ADR equivocado.** Las entradas 65, 66,
  74 y 75 citaban el criterio del recomendador de `F3` como `D84`, que es el ADR de `F1`; el de
  `F3` es `D87`. Apareció al querer citar la categoría `transmision` desde el `sources.json` de
  esta línea: la cita se verificó antes de escribirla y no cerró. La causa es el merge que
  renumeró el ADR de `F3` de `D84` a `D87` —las entradas se renumeraron y las referencias dentro
  del cuerpo quedaron viejas—, y el `D84` del encabezado del cierre de `F1` es correcto y se
  dejó. Esto **sí** se editó, a diferencia de la 65: una cita a un ADR es verificable y estaba
  inequívocamente mal (`D84` no tiene pesos ni cohortes ni umbral de empate), mientras que qué
  cuatro filas son de transmisión es una lectura de quien escribió la entrada.

## A `GLOSARIO.md`

Tres filas nuevas, las tres verificadas contra el archivo antes de escribirlas: **«par elegible
por mecanismo»**, **«candidato de signo invertido»** y **«fila que agrupa varios genes»**.
Ninguno de los tres términos estaba.

## A `CAMINOS_PROBADOS.md`

Nada. Esta línea no descartó ningún camino después de medirlo: las cuatro alternativas de `D91`
se descartaron **antes**, con el argumento escrito en el ADR, y ninguna llegó a implementarse.

---

## Lo que la prueba encontró y el código no tenía

Vale anotarlo porque es el único defecto real que apareció en esta línea, y lo encontró una
prueba escrita para otra cosa. La §6 de `test_pares.py` iba a verificar que una contraevidencia
que no se verifica contra la tabla aborta, y le pasó un TSV con otro esquema: el lector de
`contraevidencia.tsv` se rompió con `KeyError` en la primera columna que no existía, en vez de
abortar diciendo que el esquema cambió. Un `KeyError` y un `SystemExit` se parecen desde afuera
—los dos paran la corrida— y ahí la diferencia no es cosmética: el preregistro §2 pide que una
entrada que cambió de semántica **se nombre**, porque el que la lee tiene que saber si la tabla
cambió o si el archivo está mal. Se agregó el chequeo de esquema explícito, igual al que ya
tenía la tabla de `F3`, y la prueba quedó partida en los tres casos que corresponden: frase que
no está textual, fila que no existe y esquema cambiado.

## Una línea de `.gitattributes`, por un diff que no es un cambio

Las salidas de este bloque se escriben con LF, y esta máquina tiene `core.autocrlf=true`, que
es el default de Git para Windows. Con eso, un clon nuevo recibe los TSV con CRLF y
regenerarlos produce un diff de **archivo entero** sin que cambie un solo dato, lo que vuelve
inútil la única verificación barata que hay sobre una salida versionada: generar y comparar
contra lo commiteado. Se agregó una línea acotada al directorio `resultados/` de este bloque,
con el motivo escrito arriba, en el mismo archivo donde ya estaba la regla equivalente para los
ganchos de verificación. **No se tocó el resto del repositorio:** los otros bloques tienen el
mismo patrón de escritura y la misma trampa, pero forzar LF sobre sus salidas las
renormalizaría en el próximo checkout, y eso es un cambio de archivos de otras líneas.

## La frontera entre los dos bloques, que es la decisión de diseño que importa

El selector trabaja sobre **identificadores del catálogo** y el enumerador de `O4` sobre
**secuencias**. Juntarlos en un paso era tentador —el issue habla de «el enumerador» en
singular— y habría sido un error: de los 25 candidatos elegibles sólo **dos** tienen el gen
entero en esta máquina, así que la falta de una secuencia se habría leído como falta de
elegibilidad, que es exactamente la clase de confusión que `F3` evitó al separar «fuera del
orden» de «eje no calculable».

Por eso la salida de esta línea dice cuántos pares son **elegibles** y no cuántos son
**corribles**: lo segundo lo dice el enumerador cuando se le pasan las rutas, y depende de qué
tenga la máquina.

## Qué código se tocó, y qué se dejó sin tocar

**Nada de `tools/sifi21_port/` cambió** y nada de `F3` cambió. De `O4` se tocó un solo archivo,
`scripts/enumerar_quimeras.py`, y sólo por agregado: tres parámetros nuevos, una función que
resuelve los ejes desde la tabla, la exclusión mutua con `--eje` y una clave de JSON que
aparece sólo cuando se usa la vía nueva. **Ninguna columna se agregó ni se sacó**, que es lo
que el `test_enumerador.py` de `O4` afirma a propósito, y sus cuatro anclas se volvieron a
correr después de la edición: las cuatro pasan.

Las tres salidas commiteadas de `O4` **no se regeneraron**. La corrida de verificación del §4
del `REPORT.md` escribió en un directorio temporal, y el `--resultados <temporal>` de su comando
no es decorativo: sin él habría dejado una salida nueva dentro del bloque de otra línea.

## Un detalle de la numeración de entradas que conviene saber

Las dos entradas de `R4` arrancan en **86** y la anterior es la **75**, así que hay un hueco de
diez números que no corresponde a entradas perdidas. Esta línea no lo rellenó: usar 76 a 79
habría sido razonable y también habría sido una apuesta a que ninguna otra sesión los tomó. La
regla barata es la que se siguió: **el siguiente libre después del máximo**, y una nota en el
archivo diciendo por qué hay un agujero.

## Confidencialidad

- Esta línea **no lee ni una secuencia**. Su entrada es un TSV de identificadores, mecanismos y
  frases de la fuente, todo versionado, más su propio `contraevidencia.tsv`. No llama al motor
  de plegado, no toca `work/` y no manda nada a ningún servicio.
- Ninguna salida de este bloque escribe bases, y el bloque no necesita `.gitignore` propio
  porque no produce ningún archivo de nucleótido.
- La corrida de verificación del §4 sí usó secuencias y referencias, todas leídas de disco, con
  el plegado en el módulo `RNA` local y el tamizado con un autómata en memoria. Su salida fue a
  un temporal fuera del árbol.
- `tools/verificacion/sin_secuencias.py` queda en **6 hallazgos no exceptuados**, que es la
  línea base; los archivos que los producen son de `W2` y `C4`, ninguno de acá.
