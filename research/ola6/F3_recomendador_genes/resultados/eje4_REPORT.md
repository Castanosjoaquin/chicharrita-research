# F3 eje 4 — conservación entre los tres TSA: resultado

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
