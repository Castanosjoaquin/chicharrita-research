# F3 eje 3 — filas recuperadas de papers: resultado (proxy de la especie del paper)

**Fecha: 2026-10-28.** Issue [#43](../../../../../issues/43). Criterio:
[`PREREGISTRO_EJE3_FILAS_NUEVAS.md`](../PREREGISTRO_EJE3_FILAS_NUEVAS.md), commit `43c7fa0`, anterior a este
cálculo. Script: [`10_eje_offtarget_filas_nuevas.py`](../scripts/10_eje_offtarget_filas_nuevas.py). Salidas:
`eje3_filas_nuevas.tsv`, `eje3_filas_nuevas_por_secuencia.tsv`, `eje3_filas_nuevas_nulo.tsv`,
`eje3_filas_nuevas_meta.json`. Máquina de Joaquín, entorno `w5bio`. Las secuencias vienen de los papers citados
abajo y de NCBI (ver [`recuperacion_6filas_REPORT.md`](recuperacion_6filas_REPORT.md)).

> **Esto es un proxy.** Mide el off-target del gen **de la especie del paper**, no el del transcripto de
> *D. maidis*. El diseño de ARNdc se hace siempre sobre la secuencia propia del vector (`D37`). **Estos valores
> no son comparables con los de las cinco filas `DM`** (`eje3_REPORT.md`).

## Control del motor

Antes de tamizar, `eth_Dm` (ya tamizada en `work/sifi_v2/`) corrió en el mismo lote, y **sus 595 ventanas
reproducen las publicadas columna por columna** `[M]`; el script aborta si no. Es lo que permite leer estas
filas con el mismo criterio que las cinco `DM`.

## Resultado

Fracción limpia = ventanas de 21 nt, deduplicadas dentro de la fila, sin ningún bloque ≥19 nt idéntico en las seis
referencias del panel de `D76`. Nulo: 50 permutaciones por secuencia que conservan la composición, semilla
`20261029`, mismo motor y panel.

| fila | especie (paper) | secuencias | ventanas distintas | limpias | **fracción limpia** | nulo (mediana, rango) | frente al nulo | en el orden |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
| `DE-01` (R1) | *Peregrinus maidis* | 2 | 3.353 | 3.133 | **0,9344** | 0,9878 (0,9785–0,9949) | fuera del rango del nulo | en el orden (cohorte A) |
| `DE-03` (R2) | *Peregrinus maidis* | 2 | 1.254 | 1.242 | **0,9904** | 0,9944 (0,9860–1,0000) | dentro del rango del nulo | en el orden (cohorte B) |
| `CI-13` (R4) | *Nephotettix cincticeps* | 1 | 1.891 | 1.851 | **0,9788** | 0,9952 (0,9894–1,0000) | fuera del rango del nulo | fuera del orden: fenotipo_invertido |
| `DE-06` (R6) | *Delphacodes kuscheli* | 2 | 1.085 | 1.046 | **0,9641** | 0,9908 (0,9788–1,0000) | fuera del rango del nulo | fuera del orden: sin_fenotipo_publicado |

`[M]` Los datos de origen de cada fila son de los papers: `DE-01` son las accesiones `KC473163.1` y `KC473162.1`
citadas en R1; `DE-03`, las dos secuencias del S1 File de R2, **sin accesión**; `CI-13`, `MN815919.1` de R4; `DE-06`,
`PZ371509.1` y `PZ371510.1` de R6 `[R]`.

### Qué referencia aporta cada coincidencia (publicado, no puntúa)

| fila | maíz | *H. axyridis* | *A. mellifera* | *H. vitripennis* | *F. candida* | humano | con `perfecto_21` | con `mm1_21` | limpia sin humano |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `DE-01` | 0,0119 | 0,0218 | 0,0185 | 0,0176 | 0,0107 | 0,0191 | 0,0173 | 0,1420 | 0,9424 |
| `DE-03` | 0,0024 | 0,0000 | 0,0024 | 0,0000 | 0,0000 | 0,0048 | 0,0000 | 0,0183 | 0,9952 |
| `CI-13` | 0,0016 | 0,0000 | 0,0000 | 0,0111 | 0,0000 | 0,0085 | 0,0016 | 0,0386 | 0,9873 |
| `DE-06` | 0,0065 | 0,0092 | 0,0037 | 0,0092 | 0,0000 | 0,0083 | 0,0055 | 0,0498 | 0,9724 |

### Cómo se lee, con la regla del preregistro

1. **`DE-03` queda dentro del rango del nulo:** su número de coincidencias no se distingue del de una secuencia
   sin homología. Es la lectura favorable, y vale lo mismo que para `eth` y `burs-alpha` en `eje3_REPORT.md`.
2. **`DE-01`, `CI-13` y `DE-06` quedan fuera del rango, por debajo:** tienen más coincidencias que el azar.
   La más marcada es `DE-01` (0,9344 contra un mínimo del nulo de 0,9785); `CI-13` queda a 0,0106 del mínimo y
   `DE-06` a 0,0147. Por secuencia, `DE-01` pesa sobre todo en la subunidad B (0,9253) más que en la D (0,9562).
   `[H]` Que la V-ATPasa B de *P. maidis* tenga el peor perfil de estas cuatro coincide en dirección con la de
   *D. maidis* (`DM-02`, 0,8827), pero son secuencias de especies distintas y no se comparan como número.
3. **`DE-03` tiene el puntaje más alto de las cuatro, y es la fila sin accesión.** Su identidad descansa en R2 y
   en la coincidencia con los cebadores, no en una verificación en NCBI. Sus dos secuencias son isoformas y
   comparten tramo: por eso 2.134 ventanas en bruto (1.119 y 1.015) son 1.254 distintas.

## Qué le hace al orden

`CI-13` y `DE-06` **no están en el orden** (`fenotipo_invertido` y `sin_fenotipo_publicado`) y su eje 3 se publica
sólo acá. `DE-01` y `DE-03` sí están, y como no tienen eje 4 pasan a cohortes nuevas **donde quedan solas**:
`DE-01` en A+3 (puntaje 0,8307) y `DE-03` en B+3 (0,5840), con pesos renormalizados sobre los ejes presentes.

1. **Una cohorte de un solo candidato no ordena nada:** esos dos puntajes no se leen como puesto.
2. **La cohorte A pierde a `DE-01`.** Su empate de primer puesto pasa de `CI-01`, `CI-02`, `CI-03`, `DE-01` a
   `CI-01`, `CI-02`, `CI-03`, y la B pierde a `DE-03`. Se anotó antes de calcular (§4 del preregistro).
3. **Las cinco filas `DM` no cambian** (cohorte A+3+4, puntajes y empate de tres): verificado fila por fila.
4. **`segundo_orden` sigue en «sí»** en las dos lecturas de «cohorte A» (A+3+4: `DM-02, DM-03, DM-05` contra
   `DM-01`; A: `CI-01, CI-02` contra `CI-01, CI-02, CI-03`) `[M]`. Las anclas de `F4` pasan.

## Lo que no se hizo ni se concluye

- Siguen sin eje 3 las **21 filas sin secuencia** de las 25 que había que recuperar: `HE-04` y `CI-07` (sin
  accesión en su paper), 9 con PMID pero sin texto completo en PMC (incluye `DM-04`) y 10 sin paper identificado.
  El eje 3 cubre ahora 9 filas con puntaje: las 5 `DM` y 4 proxies.
- No se verificó `DE-03` en NCBI porque no tiene accesión (entrada 101 aparte para `DE-01`).
- Las seis referencias pesan igual (`D47`), y el eje es el perfil de la molécula entera, no de la región elegida.
- El nulo es un piso (no conserva uso de codones ni repeticiones).
- Ejecución: 80 lotes de unas 6.000 ventanas, 6 a la vez, 48 min.

## Referencias de los papers usados

**[R1]** Yao J, Rotenberg D, Afsharifar A, Barandoc-Alviar K, Whitfield AE (2013). Development of RNAi methods for Peregrinus maidis, the corn planthopper. *PloS one* 8(8):e70243. doi:10.1371/journal.pone.0070243; PMID 23950915; PMC3737204.

**[R2]** Wang YH, Rivera DE, Klobasa W, Lorenzen MD (2024). Evaluation of Peregrinus maidis transformer-2 as a target for CRISPR-based control. *PloS one* 19(4):e0295335. doi:10.1371/journal.pone.0295335; PMID 38635824; PMC11025951.

**[R4]** Wang H, Liu Y, Mo L, Huo C, Wang Z, Zhong P, Jia D, Zhang X, Chen Q, Chen H, Wei T (2020). A Neuron-Specific Antiviral Mechanism Modulates the Persistent Infection of Rice Rhabdoviruses in Leafhopper Vectors. *Frontiers in microbiology* 11:513. doi:10.3389/fmicb.2020.00513; PMID 32362876; PMC7180231.

**[R6]** Andrada NL, Crespo M, Baricalla AA, Dalaisón-Fuentes LI, Sterkel M, Catalano MI (2026). ETH and Burs-α are necessary for the normal molting in &lt;i&gt;Dalbulus maidis&lt;/i&gt; and &lt;i&gt;Delphacodes kuscheli&lt;/i&gt;. *Frontiers in insect science* 6:1811933. doi:10.3389/finsc.2026.1811933; PMID 42328018; PMC13279319.

El resto de las citas del paso de recuperación (`CI-07`, `HE-04`) está en `referencias_recuperacion.tsv`.
