# F3 eje 4 — conservación entre los tres TSA: resultado (regla original y enmienda 1)

**Fecha: 2026-10-27.** Criterio: `../PREREGISTRO_EJE4.md` (commit anterior a esta corrida). Script:
`../scripts/05_eje_conservacion.py`. Salidas: `eje4_conservacion.tsv`, `eje4_meta.json`. Crudo en
`work/F3_eje4/` (no versionado). Máquina de Joaquín, entorno `w5bio` (BLAST+ 2.17.0, Biopython 1.88).
Marcadores `[M]`: con insumos locales (secuencias de EPILAB para `DM-01` y `DM-03`).

## Resultado

| fila | gen | ventanas | evaluables en los 3 | idénticas en los 3 | cobertura | fracción | estado |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `DM-01` | BicC | 2.500 | 404 | 244 | 0,162 | — | cobertura insuficiente |
| `DM-02` | V-ATPase B | 1.483 | 693 | 672 | 0,467 | — | cobertura insuficiente |
| `DM-03` | V-ATPase D | 471 | 471 | 450 | 1,000 | **0,9554** | puntuado |
| `DM-05` | eth | 595 | 0 | 0 | 0 | — | ausente en GCWP01 |
| `DM-06` | burs-alpha | 448 | 0 | 0 | 0 | — | ausente en GCWP01 |

`[M]` Solo **una** de las cinco filas recibe puntaje. Ninguna se rescató moviendo el umbral.

## Lo que la regla del preregistro produjo, y hay que decidir

1. **`GCWP01` (454, Illinois) es el que deja afuera a cuatro de cinco.** `eth` y `burs-alpha` están
   en `GHCC01` y `GITV01` (595/595 y 420/384 para `eth`; 419/419 y 419/281 para `burs-alpha`) y
   **no están en `GCWP01`**. La regla «ausente en alguno → sin puntaje» los descarta por el
   ensamblado más viejo, no por variación `[M]`. `[H]` Es la regla escrita; cambiarla a «dos de tres»
   sería una enmienda con fecha, decidida antes de ver qué fila sube, no después.
2. **`DM-02` queda a 0,033 del umbral de cobertura (0,467 contra 0,50).** El umbral se fijó antes de
   ver coberturas y no se movió. Sus ventanas evaluables son 672/693 idénticas (0,970) `[M]`, pero
   eso no se puntúa.
3. **El eje no rompe el empate de tres de la cohorte A, lo deshace de otro modo.** Con solo `DM-03`
   en la cohorte nueva A+4, se queda sola, y sin otro candidato de sus mismos ejes no hay puesto que
   ordenar. El empate declarado de la A queda en `DM-02` y `DM-05`. `orden_genes.tsv` **no se
   regeneró**: hacerlo cambia cifras publicadas de la línea y pide que el equipo confirme antes.

## Control contra `C8` (preregistro §3.1)

| gen | `C8` conservadas | este eje | lectura |
| --- | ---: | ---: | --- |
| `ATPaseD_Dm` | 450 de 471 | 450 de 471 | coincide |
| `BicC_Dm`, en Argentina (`GHCC01`) | 2.417 de 2.500 | 2.417 de 2.500 | coincide |
| `eth_Dm` | **0 de 595, «sin transcriptoma suficiente»** | 595 y 420 con dato en `GHCC01` y `GITV01` | **difiere** |
| `bursA_Dm` | **0 de 448, «sin transcriptoma suficiente»** | 419 y 419 con dato en `GHCC01` y `GITV01` | **difiere** |

`[M]` `C8` declaró `eth` y `bursA` sin ningún transcriptoma que los cubra. Con `blastn` contra los
ensamblados completos aparecen en dos de los tres. `[?]` No se averiguó por qué: `C8` partía de los
contigs que `W5` ya había ubicado, y es la explicación más simple, pero no está probada. Por el
umbral de 5 puntos del preregistro es un hallazgo del control y no se promedia.


---

## Enmienda 1 (`../PREREGISTRO_EJE4_ENMIENDA1.md`, commit `629086b`): las dos reglas lado a lado

**La enmienda es posterior al resultado de arriba**, y se escribió sabiendo qué filas dejaba afuera
la regla original. Por eso las dos columnas se publican: la original (tres TSA, intersección) y la
enmendada (al menos dos TSA con dato). Sólo la enmendada entra al puntaje; la original queda en
`eje4_conservacion.tsv` como lectura estricta.

| fila | gen | TSA con el gen | regla original | regla enmendada (cobertura) | enmendada: conservadas / evaluables |
| --- | --- | ---: | ---: | ---: | --- |
| `DM-01` | BicC | 3 | sin puntaje | **0,8876** (1,00) | 2.219 / 2.500 |
| `DM-02` | V-ATPase B | 3 | sin puntaje | **0,9575** (1,00) | 1.420 / 1.483 |
| `DM-03` | V-ATPase D | 3 | 0,9554 | **0,9554** (1,00) | 450 / 471 |
| `DM-05` | eth | 2 | sin puntaje | **0,9143** (0,71) | 384 / 420 |
| `DM-06` | burs-alpha | 2 | sin puntaje | **0,6706** (0,94) | 281 / 419 |

`[M]` Con insumos locales para `DM-01` y `DM-03`. `DM-03` no cambia entre reglas: es la única fila
donde las dos se pueden comparar de igual a igual.

**Lo que la enmienda cuesta**, visible en la columna `enm1_tsa_con_el_gen`: `DM-05` y `DM-06`
puntúan sobre **dos** fuentes, no tres, y una fracción de 0,91 sobre dos transcriptomas es evidencia
más débil que sobre tres. `DM-06` es además la fila menos conservada, 0,67: 138 de sus 419 ventanas
evaluables varían, todas en `GITV01` (419 con dato, 281 idénticas; en `GHCC01` son 419 de 419) `[M]`.

### Qué le hace al orden

`orden_genes.tsv` se regeneró (`scripts/03_orden.py`). Las 25 filas del orden son las mismas y las
11 excluidas no cambian, así que `F4` sigue pasando sus tres anclas. Cambia lo que el preregistro
anticipó:

| cohorte | candidatos | primer puesto |
| --- | ---: | --- |
| **A+4** (ejes 1, 2 y 4), pesos 0,533 / 0,333 / 0,133 | 5, todos `DM` | empate declarado `DM-02` (0,9943), `DM-03` (0,9941), `DM-05` (0,9886) |
| A (ejes 1 y 2) | 12 | empate declarado `CI-01`, `CI-02`, `CI-03`, `DE-01` (0,7908) |
| B (solo eje 1) | 8 | `DE-02` |

1. **El eje 4 no rompe el empate de tres.** El preregistro calculó que hacía falta una diferencia
   de más de 0,375 en la fracción de conservación entre dos de los tres; la mayor entre ellos es
   0,9575 − 0,9143 = 0,043 `[M]`. El empate sigue declarado, con los mismos tres.
2. **`DM-01` (BicC) sale del empate de la cohorte A**, pero no por mérito: en A+4 queda en 0,7617,
   quinto, solo, sin empate. Entre cohortes no se compara.
3. **La cohorte A, sin los cinco `DM`, quedó con otro primer puesto.** No es un cambio de orden
   dentro de A: los que la lideraban pasaron a otra cohorte. No se lee como que `CI-01…` sea mejor
   que `DM-02`; las dos cohortes no se comparan.
4. **Sensibilidad de A+4:** el primer puesto sólo cambia con un peso de fenotipo igual a 1,0 (se
   suman `DM-01` y `DM-06`), no en el rango intermedio `[M]` (`resultados/meta.json`).
5. **`segundo_orden`** se regeneró con cuatro cohortes. «¿Cambia el orden según el objetivo?»
   sigue en **sí**, en las dos lecturas posibles de «cohorte A»: la nueva A+4 (`DM-02, DM-03,
   DM-05` para matar contra `DM-01` para esterilizar) y la A que quedó (`CI-01, CI-02, DE-01`
   contra `CI-01, CI-02, CI-03, DE-01`) `[M]`. Si hubieran discrepado, el script lo declara
   «depende de la cohorte» y no elige.

### Lo que no se hizo
- Las 31 filas que no son `DM-01/02/03/05/06` no reciben el eje 4: su ortólogo en *D. maidis* no
  se recuperó (preregistro §2). `DM-04` tampoco: no hay secuencia en esta máquina.
- El hallazgo del control con `C8` para `eth` y `burs-alpha` sigue sin explicación probada.
- El eje 4 es conservación entre **fuentes públicas** (Illinois, Ohio State, Argentina), no entre
  poblaciones de campo del noroeste argentino.

### Nulo del eje 4 (agregado el 2026-10-28)

El eje se publicó primero sin su nulo, que el preregistro daba por vigente. Se calculó después, con la
definición corregida por la enmienda 1 de `PREREGISTRO_EJE3.md`: **ninguna de las 250 permutaciones
supera 0,0050 de ventanas con presencia exacta en un TSA** (`eje4_nulo.tsv`). Los puntajes de arriba
son homología y no azar. Detalle y límites en `eje3_REPORT.md`.
