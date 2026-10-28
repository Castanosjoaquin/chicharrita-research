# F3 eje 3 — off-target contra el panel de seis: resultado (cinco filas `DM`)

**Fecha: 2026-10-28.** Issue [#43](../../../../../issues/43), tramo del eje de off-target de
[#37](../../../../../issues/37). Criterio: [`PREREGISTRO_EJE3.md`](../PREREGISTRO_EJE3.md) y su
enmienda 1, commiteados (`a303c51`, `402e0a5`) antes de calcular. Script:
[`07_eje_offtarget.py`](../scripts/07_eje_offtarget.py). Salidas: `eje3_offtarget.tsv`,
`eje3_nulo.tsv`, `eje4_nulo.tsv`, `eje3_meta.json`. Máquina de Joaquín, entorno `w5bio`
(ViennaRNA 2.7.2 en el tamizado publicado; `pyahocorasick`). Insumos locales: secuencias de
EPILAB para `DM-01` y `DM-03` `[M]`.

**Cobertura: 5 de 36 filas.** Las otras 31 siguen con el eje faltante, y no por falta de `work/`:
no tienen secuencia de *D. maidis* admisible (entradas 97 y 99).

## Resultado

Fracción limpia = ventanas de 21 nt sin ningún bloque ≥19 nt idéntico en ninguna de las seis
referencias, sobre todas las ventanas, sin filtrar por eficiencia predicha. El nulo son 50
permutaciones que conservan la composición, tamizadas con el mismo motor y panel.

| fila | gen | ventanas | limpias | **fracción limpia** | nulo (mediana, rango) | frente al nulo |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `DM-01` | BicC | 2.500 | 2.415 | **0,9660** | 0,9948 (0,9832–1,0000) | fuera del rango del nulo |
| `DM-02` | V-ATPase B | 1.483 | 1.309 | **0,8827** | 0,9943 (0,9872–0,9980) | fuera del rango del nulo |
| `DM-03` | V-ATPase D | 471 | 454 | **0,9639** | 0,9936 (0,9660–1,0000) | fuera del rango del nulo |
| `DM-05` | eth | 595 | 584 | **0,9815** | 0,9950 (0,9748–1,0000) | dentro del rango del nulo |
| `DM-06` | burs-alpha | 448 | 448 | **1,0000** | 0,9933 (0,9777–1,0000) | dentro del rango del nulo |

`[M]` **El nulo no da 1,0000.** Una secuencia sin homología trae, en mediana, 0,5–0,7 % de ventanas
con un bloque ≥19 nt coincidente (0,9933–0,9950 limpias), y en el peor caso 3,4 % (`DM-03`, mínimo
0,9660). Con 471 ventanas, una sola permutación afortunada fija ese mínimo. `[?]` No se investigó por
qué el azar alcanza ese nivel; la hipótesis es secuencias de baja complejidad o repetitivas en los
transcriptomas de referencia, sin probar.

### Cómo se lee, con la regla escrita antes

La regla del preregistro era que si la fracción real y el rango del nulo se superponen, **el eje no
distingue ese gen del azar y se dice**.

1. **`DM-02`, `V-ATPase B`: claramente por encima del azar** (0,8827 contra un nulo de 0,9872–0,9980).
   Es homología real: el gen está conservado, y aparece contra *H. vitripennis* (5,5 %), humano
   (4,0 %) y maíz (1,5 %) `[M]`. Es la única fila con una señal de riesgo inequívoca.
2. **`DM-01` (`BicC`) queda fuera del rango del nulo** (0,9660 contra 0,9832–1,0000), con exceso
   sobre todo contra *H. vitripennis* (2,2 %).
3. **`DM-03` queda fuera del rango por 0,0021** (0,9639 contra un mínimo de 0,9660), con 471 ventanas.
   Es un caso marginal, y no conviene leerlo como señal firme.
4. **`DM-05` y `DM-06` están dentro del rango del nulo.** Su número de aciertos no se distingue del de
   una secuencia sin homología. Esa es la lectura **favorable**: no hay exceso de coincidencias sobre
   el azar. Pero también implica que **la diferencia entre 0,9815 (`eth`) y 1,0000 (`burs-alpha`) es
   menor que la dispersión del propio nulo** y no ordena nada.

### Qué referencia aporta cada coincidencia (publicado, no puntúa)

| fila | maíz | *H. axyridis* | *A. mellifera* | *H. vitripennis* | *F. candida* | humano | con `perfecto_21` | con `mm1_21` | limpia sin humano |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `DM-01` | 0,0024 | 0,0028 | 0,0000 | 0,0224 | 0,0016 | 0,0048 | 0,0172 | 0,0404 | 0,9708 |
| `DM-02` | 0,0148 | 0,0054 | 0,0000 | 0,0553 | 0,0020 | 0,0398 | 0,0479 | 0,2637 | 0,9225 |
| `DM-03` | 0,0064 | 0,0000 | 0,0000 | 0,0149 | 0,0000 | 0,0149 | 0,0064 | 0,0701 | 0,9788 |
| `DM-05` | 0,0000 | 0,0000 | 0,0000 | 0,0084 | 0,0000 | 0,0101 | 0,0017 | 0,0269 | 0,9916 |
| `DM-06` | 0,0000 | 0,0000 | 0,0000 | 0,0000 | 0,0000 | 0,0000 | 0,0000 | 0,0112 | 1,0000 |

`[H]` La mayor parte del exceso viene de *H. vitripennis*, que es un cicadélido emparentado con el
vector: coincidencias contra un ortólogo cercano son esperables y su lectura es de riesgo para
parientes, no de fuga contra especies lejanas. La columna «sin humano» muestra cuánto del exceso es
humano: en `V-ATPase B`, 0,8827 contra 0,9225.

## Qué le hace al orden

Los cinco pasan a la cohorte **A+3+4**, y por primera vez los pesos de `D87` no se renormalizan
(suman 1,00 porque sólo falta el eje 5, que pesa 0,00).

| cohorte A+3+4 (pesos de `D87` sin renormalizar: 0,40 / 0,25 / 0,25 / 0,10) | puntaje | antes (A+4) |
| --- | ---: | ---: |
| `DM-05` eth — si, con DM-03, DM-02 | 0,9868 | 0,9886 |
| `DM-03` V-ATPase D — si, con DM-05, DM-02 | 0,9865 | 0,9941 |
| `DM-02` V-ATPase B — si, con DM-05, DM-03 | 0,9664 | 0,9943 |
| `DM-06` burs-alpha — no | 0,8821 | 0,8427 |
| `DM-01` BicC — no | 0,8128 | 0,7617 |

1. **El empate de tres del primer puesto sigue declarado**, con los mismos tres. Lo había previsto
   el preregistro (§4): romperlo pedía más de 0,20 de diferencia en la fracción limpia entre dos de
   ellos, y la mayor es 0,9815 − 0,8827 = 0,0988 `[M]`.
2. **`DM-02` sale del primer lugar dentro del empate** (de 0,9943 a 0,9664), pero sigue **dentro**: la
   diferencia con el primero es 0,0204, menor que 0,05. El orden *dentro* de un empate declarado no
   se lee.
3. **`DM-06` y `DM-01` suben de puntaje** (0,8427 → 0,8821 y 0,7617 → 0,8128) porque su off-target es
   bueno. No cambian de puesto: entre cohortes no se compara.
4. **La sensibilidad al peso de fenotipo** no cambia el primer puesto en ningún valor intermedio; sólo
   a 1,0 se suman los cinco `[M]` (`meta.json`).
5. `segundo_orden` se regeneró con la cohorte nueva y **sigue en sí**: el orden cambia según el
   objetivo, en las dos lecturas de «cohorte A» (A+3+4 y la A que quedó) `[M]`.
6. Las 25 filas del orden son las mismas y las anclas de `F4` pasan (`00_anclas.py`, las tres).

## Nulo del eje 4 (pendiente heredado, cerrado)

`PREREGISTRO_EJE4.md` §5 declaró vigente la regla del nulo y el eje 4 se publicó sin él. Con la
definición corregida por la enmienda 1, **ninguna permutación supera 0,0050 de ventanas con presencia
exacta en un TSA** (máximo por gen: `DM-01` 0,0008, `DM-02` 0,0020, `DM-03` 0,0, `DM-05` 0,0050,
`DM-06` 0,0) `[M]`. Las ventanas idénticas de las secuencias reales son, en el peor caso, 0,6706 de las
evaluables (`DM-06`). **No son la misma unidad** —el nulo es presencia sobre todas las ventanas y lo
real es idénticas sobre evaluables—, así que no se restan; lo que se lee es la distancia de dos
órdenes de magnitud: la conservación medida es homología y no coincidencia por azar.

## Lo que no se hizo ni se concluye

- Las 31 filas restantes siguen sin el eje 3. El hallazgo de la entrada 97 sigue vigente: recuperar
  esas secuencias es trabajo de lectura.
- Es el perfil de la **molécula entera**, no de la región elegida (`M6` y el ranking ya lo resuelven).
  No afirma que una coincidencia de 19 nt silencie nada.
- Las seis referencias pesan igual: el peso de exposición de cada organismo es la decisión de `D47`.
- El nulo es un **piso**: las permutaciones no conservan uso de codones ni repeticiones, así que
  subestima el azar de un transcripto real.
- Ejecución: el nulo en un solo archivo (125.000 ventanas) no terminó en 55 min y se corrió en 51 lotes
  de unas 6.000 ventanas, 6 a la vez (35 min). Es forma de ejecutar, no de método; ver
  `CAMINOS_PROBADOS.md`.
