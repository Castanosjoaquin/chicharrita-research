# F3 — Eje 3, off-target contra el panel de seis: el criterio, escrito antes de calcularlo

**Fecha de escritura: 2026-10-28.** Extiende `PREREGISTRO.md` §3 (eje 3) y §4.2. Issue
[#43](../../../../issues/43); origen, la casilla del eje de off-target de
[#37](../../../../issues/37). Mismo procedimiento que `PREREGISTRO_EJE4.md`: se commitea
**antes** del primer cálculo y lo que cambie después entra como enmienda con fecha.

El `PREREGISTRO.md` declaró el eje 3 no calculable por dos motivos (§3 y
`resultados/correcciones_al_preregistro.md` §4): faltaba `work/sifi_v2/` y las ocho filas del
catálogo con conteos los traían contra otro panel. El barrido de `R12` midió que en la máquina
de Joaquín `work/sifi_v2/` está, y que **no alcanza para las 36 filas** —lo que falta ahí son 28
secuencias de transcripto de 15 especies, y es trabajo de lectura (entrada 97)—. **Este documento
cubre sólo lo que sí se puede calcular: cinco filas.** Las otras 31 siguen con el eje declarado
faltante.

## 0. Qué se miró antes de escribir, para que el orden quede claro

Se miró **qué archivos existen** y sus columnas, y **el resumen agregado por referencia**
(`offtarget_resumen.json`: cuántos siRNA con bloque ≥19 nt hay por gen y referencia). **No se
calculó ninguna fracción por gen**, pero esos agregados son la materia prima del puntaje, y se
vieron algunos: por ejemplo, que `V-ATPase B` tiene 22 siRNA con bloque ≥19 nt contra el maíz y
`ATPaseD` tiene 3. Por eso la definición de abajo **no se eligió mirando esos números**, sino
copiando las del proyecto —nivel de alerta en 19 nt (`D28`, `D90`) y el panel normativo de `D76`—,
y se declara que no es una elección a ciegas.

## 1. Qué candidatos reciben el eje, y de dónde sale cada tamizado

El eje se calcula sobre las **cinco filas `DM`** que ya reciben el eje 4, con el tamizado ya
existente en disco, sin regenerar ningún insumo (`R12`: regenerar con otra versión del motor
convierte un pendiente en una discrepancia).

| Fila | Gen | Consulta | Tamizado | Ventanas |
| --- | --- | --- | --- | ---: |
| `DM-01` | `BicC` | `BicC_Dm_full` | `work/sifi_v2/offtarget_k21/offtarget_por_sirna.tsv` | 2.500 |
| `DM-03` | `V-ATPase D` | `ATPaseD_Dm_full` | `work/sifi_v2/offtarget_k21/offtarget_por_sirna.tsv` | 471 |
| `DM-05` | `eth` | `eth_Dm_full` | `work/sifi_v2/offtarget_k21/offtarget_por_sirna.tsv` | 595 |
| `DM-06` | `burs-alpha` | `bursA_Dm_full` | `work/sifi_v2/offtarget_k21/offtarget_por_sirna.tsv` | 448 |
| `DM-02` | `V-ATPase B` | `VATPaseB_Dm_full` | `work/O3/offtarget/cds_completo/offtarget_por_sirna.tsv` | 1.483 |

`DM-02` sale de otro directorio y es **a propósito**: `D88` dejó escrito que cada medición
conserva su panel y su directorio. La condición para que sea comparable con las otras cuatro es
que **sean el mismo panel y los mismos parámetros**, y el script lo **verifica y aborta si no**:
las seis referencias del panel normativo de `D76` en las columnas de los dos archivos, `size` 21
y `min_block` 19 en los dos resúmenes JSON. `DM-04` no tiene secuencia en esta máquina y las 30
filas de otras especies no tienen su ortólogo de *D. maidis*: salen con el eje ausente, no con
cero (entrada 98).

## 2. La medida

**Panel.** Las seis referencias de `D76`: maíz (*Zea mays*), *H. axyridis*, *A. mellifera*,
*H. vitripennis*, *F. candida* y humano. El genoma de *D. maidis* **no** entra: es el propio
vector (`offtarget_dm_k21`), y una coincidencia contra uno mismo no es un off-target.

**Unidad.** Todas las ventanas de 21 nt de la secuencia, paso 1. **No se filtran por eficiencia
predicha**: `PREREGISTRO.md` §5 sostiene que este eje es el más sólido porque no depende del
criterio de eficiencia de si-Fi21, que no está validado en hemípteros (ρ = +0,142, IC95
[−0,247, +0,492], n = 29 `[M]`). Filtrar por `is_efficient` lo haría depender de él.

**Ventana limpia.** Una ventana es **limpia** si `perfecto_ge19` vale 0 en **las seis**
referencias, es decir, si ningún bloque contiguo de 19 nt o más coincide exacto con ninguna. 19
es el nivel de alerta vigente (`D28`, `D90`) y es la definición de `perfecto_ge19` que usa
`tabla_alertas.py`. Las seis pesan igual: el peso de exposición por organismo es la decisión que
`D47` dejó abierta y no se resuelve acá.

**El puntaje del eje**, para un candidato, es

> fracción limpia = (ventanas limpias) / (ventanas totales)

acotada a [0, 1], que es la escala que `PREREGISTRO.md` §4.2 pide para renormalizar. Mayor es
mejor. Todas las ventanas tienen dato en las seis referencias, así que **no hay umbral de
cobertura** ni hueco que declarar; lo verifica el script (el número de filas del tamizado debe ser
igual al de ventanas de la consulta).

**Y se publican, al lado del puntaje y en la misma fila, sin entrar a él:**
(a) por cada una de las seis referencias, la fracción de ventanas con `perfecto_ge19` > 0;
(b) la fracción de ventanas con `perfecto_21` > 0 en alguna referencia, que es el nivel más
estricto; (c) la fracción con `mm1_21` > 0, que **no** puntúa porque el nivel de alerta del
proyecto está en bloques perfectos y no en un desajuste; (d) la fracción limpia **sin humano**,
como lectura de sensibilidad, porque `D83` ya mostró que equivocarse de panel produce números
plausibles en la dirección optimista. Sin esas columnas el puntaje no se puede leer: una fracción
alta puede esconder una referencia con muchos aciertos.

**Lo que esta medida no es.** Es el perfil de la **molécula entera**, no la elección de región:
elegir la región dentro de un gen ya está resuelto por `M6` y por el ranking. Un gen con 90 %
de ventanas limpias puede tener su mejor región de 200 nt con 100 % o con 70 %, y esto no lo
distingue. Tampoco afirma que una coincidencia de 19 nt silencie nada: es un criterio de alerta,
no una medida de efecto.

## 3. El nulo (regla 6 de `PREREGISTRO.md` §7: un conteo sin su nulo no se publica)

Una fracción limpia de 0,95 no dice nada hasta saber cuánto daría una secuencia sin homología.
**Nulo:** para cada una de las cinco secuencias, **50 permutaciones que conservan la composición
de bases** (mismo largo, mismas proporciones de A, C, G y T), con semilla fija `20261028`,
tamizadas con **el mismo comando, el mismo panel y los mismos parámetros** que el real
(`--size 21 --mm1`, mismas referencias y mismo orden). Se publica, junto a cada fila real, la
mediana y el rango de la fracción limpia del nulo.

**Cómo se lee, escrito antes de ver el nulo.** El nulo **no entra al puntaje ni lo corrige**: sirve
para decir si lo que el eje cuenta como coincidencia es homología o azar. Si la fracción limpia
real y la del nulo se superponen, el eje no distingue ese gen del azar y se dice. Las
permutaciones **no conservan el uso de codones ni la estructura**, así que el nulo es un piso:
subestima el azar de una secuencia real con composición y repeticiones de un transcripto.

**Un pendiente heredado que se cierra en el mismo paso.** `PREREGISTRO_EJE4.md` §5 declaró
vigentes las seis reglas de `PREREGISTRO.md` §7, y la sexta pide el nulo; el eje 4 se publicó
**sin él**. Se calcula acá, con la misma regla de permutación y la misma semilla, para las cinco
secuencias contra los tres TSA (fracción de ventanas con presencia en todos los TSA donde hay
dato). Es un defecto de cumplimiento mío, no una enmienda a su método, y el resultado se publica
en `resultados/` junto al del eje 3 aunque el nulo salga trivial.

## 4. Qué le pasa al orden cuando entra el eje

Los cinco candidatos tienen ahora los ejes 1, 2, 3 y 4 y pasan a una cohorte nueva, «A+3+4: ejes 1,
2, 3 y 4». Es `PREREGISTRO.md` §4.2 sin excepción: entre cohortes no se compara. **Por primera vez
los pesos de `D87` no se renormalizan** —fenotipo 0,40, esencialidad 0,25, off-target 0,25,
conservación 0,10, suman 1,00—, porque sólo falta el eje 5, que pesa 0,00 por declaración.

**Consecuencia prevista, escrita antes de calcular.** Hoy el primer puesto de la cohorte A+4 es un
**empate declarado de tres** (`DM-02`, `DM-03`, `DM-05`) con puntajes 0,9943 / 0,9941 / 0,9886, que
vienen casi enteros de los ejes 1 y 2 (los tres valen 1,00 en los dos). Con el umbral de empate en
0,05 y el eje 3 pesando 0,25, **hace falta una diferencia de más de 0,20 en la fracción limpia**
entre dos de los tres —descontando lo que ya aporta el eje 4, que pesa 0,10— para que el empate se
rompa. Si la diferencia es menor, el empate sigue declarado. `orden_genes.tsv` y `segundo_orden` se
regeneran, y el `REPORT` del eje publica el `diff` contra la versión anterior fila por fila.

## 5. Reglas que siguen valiendo

De `PREREGISTRO.md` §7 valen las seis. En particular: **ninguna salida versionada lleva
nucleótidos de 21 nt o más** —el tamizado por siRNA trae la columna `sirna`, así que el script
**no copia ese archivo**: sólo publica conteos y fracciones; las permutaciones y sus salidas
quedan en `work/F3_eje3/`—; **ningún eje no calculado se ordena como si lo estuviera**; y este
eje no entra al diseño del ARNdc. **La versión del motor y el `sha256` de cada archivo de
tamizado quedan declarados** en el `meta.json` del eje, como en `R8`.

## 6. Cómo se verifica que este documento se respetó

- Este archivo tiene fecha de commit **anterior** al primer cálculo del eje, y el commit del
  cálculo lo cita.
- El script aborta si los dos directorios de tamizado no comparten panel y parámetros.
- Ningún candidato fuera de las cinco filas recibe puntaje; las otras 31 dicen «sin secuencia de
  *D. maidis* admisible» o «sin ortólogo recuperado», no cero.
- Cada fila trae las seis fracciones por referencia, la de `perfecto_21`, la de `mm1_21`, la fracción
  limpia sin humano, y el nulo.
- El umbral de empate es el de `PREREGISTRO.md` §4.3, sin ajustar después de ver los números.

---

## Enmienda 1 (2026-10-28, escrita antes de calcular el nulo del eje 4)

El §3 define el nulo del eje 4 como «fracción de ventanas con presencia en todos los TSA donde
hay dato». **Eso no se puede calcular para una permutación**: «con dato» sale de un alineamiento
`blastn` de la secuencia contra el TSA (`PREREGISTRO_EJE4.md` §3 paso 2), y una secuencia con la
composición conservada pero sin homología no alinea contra nada, así que no tendría ninguna ventana
«con dato». El error fue de redacción mía, no de método.

**Nulo del eje 4, corregido:** por cada una de las cinco secuencias y cada uno de los tres TSA,
la **fracción de ventanas de 21 nt de las 50 permutaciones con presencia exacta en ese TSA**
(las dos hebras, el mismo autómata de `05_eje_conservacion.py`), con mediana y rango. Se compara
con la fracción de ventanas **idénticas** de la secuencia real en ese mismo TSA, que es lo que
`eje4_conservacion.tsv` ya publica. Lo que contesta es la pregunta del nulo: cuánta presencia
exacta daría el azar, para saber qué parte de la conservación medida es homología. Lo demás del
§3 no cambia.
