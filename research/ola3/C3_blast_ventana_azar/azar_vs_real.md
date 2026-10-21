# Q3 — Cuántas coincidencias da el azar y cuántas hay de verdad

El investigador argumentó que la biología no es aleatoria y que las coincidencias que predice
la probabilidad pura no aparecen en un genoma real: *«no vas a encontrar lo que te dice la
estadística que deberías encontrar por azar»*. Lo medimos para k de 16 a 22 contra tres
referencias de naturaleza distinta. **La respuesta es más interesante que un sí o un no: la
intuición falla en el total y acierta en la distribución.**

## 1. Qué se midió y cómo

Para cada k de 16 a 22 se toman **todas** las ventanas de largo k de los cuatro genes de EPILAB
(4.802 nt en total: MP_MRFV 1.263, CP_MRFV 528, BicC_Dm 2.520, ATPaseD_Dm 491) y, en paralelo,
las de un **control barajado** que conserva exactamente el conteo de dinucleótidos de cada gen
(barajado euleriano del grafo de dinucleótidos, semilla determinista). El control es la pieza
clave: tiene la misma composición que el gen real pero **ninguna homología**, así que separa lo
que es azar de lo que es parentesco.

Tres cantidades por ventana y por referencia:

- **(i) esperado uniforme**: `2·N / 4^k`, con N el número de posiciones de arranque válidas
  (sólo A, C, G, T) y el factor 2 por las dos hebras.
- **(ii) esperado con Markov** de orden 3, 4 y 5 ajustado **a la propia referencia** en la misma
  pasada, que absorbe el sesgo de composición: `N·(P(w) + P(rc w))`.
- **(iii) observado**: búsqueda **exacta**, no heurística. Se recorre la referencia por bloques
  y se cuenta cada aparición de la ventana y de su complemento reverso.

**El observado no sale de BLAST a propósito.** Q1 muestra que BLAST pierde casos por posición
del desajuste; acá hace falta un conteo completo. El escáner está en
[`scripts/kmers.py`](scripts/kmers.py): codifica la secuencia a enteros de 2 bits, filtra las
posiciones candidatas con una tabla booleana de 4^12 entradas (16 MB) construida con los
prefijos de 12 nt de las consultas, y verifica a largo completo sólo las candidatas. Es exacto
—todo k-mero de consulta con k ≥ 12 tiene su prefijo en la tabla— y entra en memoria: **sólo se
sostiene un bloque de 8 Mb por vez**, de modo que el genoma de 972 Mb se recorre con un pico de
uso de unos cientos de MB y no con el genoma entero indexado. Prueba de humo con ocurrencias
contadas a mano al pie del módulo.

```bash
python research/ola3/C3_blast_ventana_azar/scripts/q3_azar_vs_real.py \
       --salida research/ola3/C3_blast_ventana_azar/resultados
python research/ola3/C3_blast_ventana_azar/scripts/q3b_salto_16_17.py \
       --salida research/ola3/C3_blast_ventana_azar/resultados
```

Las tres referencias, con el tiempo de la pasada completa:

| Referencia | Naturaleza | Registros | Bases | GC | Pasada |
| --- | --- | ---: | ---: | ---: | ---: |
| *Dalbulus maidis* `GCA_975739785.1` | genoma de ADN, sin anotar, el propio vector | 141 | 972.225.736 | 0,350 | 61 s |
| *Zea mays* `GCF_902167145.1` | transcriptoma RefSeq, planta hospedadora | 76.549 | 162.712.215 | 0,495 | 21 s |
| *Apis mellifera* `GCF_003254395.2` | transcriptoma RefSeq, insecto no objetivo | 27.887 | 98.645.700 | 0,401 | 9 s |

## 2. Resultado principal: el control sin homología

Totales sobre las ~4.740 ventanas del conjunto barajado. `E_u` es el uniforme, `E_m5` el Markov
de orden 5 ajustado a la referencia.

| Referencia | k | Observado | E_u | E_m3 | E_m5 | obs/E_u | obs/E_m5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| *D. maidis* genoma | 16 | 1.979 | 2.146,7 | 1.577,5 | 1.602,8 | 0,92 | 1,235 |
| | 17 | 473 | 536,2 | 388,6 | 395,1 | 0,88 | 1,197 |
| | 18 | 99 | 133,9 | 95,8 | 97,4 | 0,74 | **1,016** |
| | 19 | 25 | 33,5 | 23,8 | 24,2 | 0,75 | **1,035** |
| | 20 | 6 | 8,4 | 5,9 | 6,0 | 0,72 | **1,000** |
| | 21 | 4 | 2,1 | 1,5 | 1,5 | 1,92 | 2,68 |
| | 22 | 2 | 0,5 | 0,4 | 0,4 | 3,84 | 5,37 |
| *Z. mays* transcriptoma | 16 | 616 | 356,8 | 513,1 | 525,7 | 1,73 | 1,17 |
| | 17 | 157 | 89,1 | 131,4 | 135,0 | 1,76 | 1,16 |
| | 18 | 52 | 22,2 | 33,6 | 34,6 | 2,34 | 1,50 |
| | 19 | 14 | 5,6 | 8,6 | 8,9 | 2,52 | 1,58 |
| | 20 | 6 | 1,4 | 2,2 | 2,3 | 4,33 | 2,64 |
| | 21 | 0 | 0,35 | 0,56 | 0,58 | 0,00 | 0,00 |
| | 22 | 0 | 0,09 | 0,14 | 0,15 | 0,00 | 0,00 |
| *A. mellifera* transcriptoma | 16 | 202 | 216,9 | 194,2 | 198,4 | 0,93 | **1,02** |
| | 17 | 42 | 54,2 | 48,5 | 49,6 | 0,78 | 0,85 |
| | 18 | 9 | 13,5 | 12,1 | 12,4 | 0,67 | 0,73 |
| | 19 | 6 | 3,4 | 3,0 | 3,1 | 1,78 | 1,94 |
| | 20 | 3 | 0,8 | 0,8 | 0,8 | 3,56 | 3,87 |
| | 21 | 2 | 0,21 | 0,19 | 0,19 | 9,50 | 10,36 |
| | 22 | 1 | 0,05 | 0,05 | 0,05 | 19,01 | 20,85 |

Tabla completa, con las dos hebras, los tres órdenes de Markov y el conjunto real, en
[`resultados/q3_tabla.tsv`](resultados/q3_tabla.tsv).

**Qué dice.** Para secuencias con la composición de nuestros genes pero sin homología, el
número total de coincidencias exactas en un genoma real es **el que predice el modelo de azar**,
dentro de un factor de 1,3 en el genoma de *D. maidis* para k de 16 a 20 una vez que el modelo
de Markov absorbe la composición (razones 1,235, 1,197, 1,016, 1,035 y 1,000). En maíz el modelo
uniforme se queda corto por un factor de 1,7 a 4,3 —el transcriptoma tiene GC 0,495 y nuestras
ventanas no— y el Markov corrige la mayor parte, bajando a 1,2-2,6. `[E]`

**La cuenta de probabilidad pura no está rota.** Lo que está mal es usarla sin corregir la
composición, y aun así el error es de un factor pequeño, no de órdenes de magnitud.

**Los valores de k ≥ 21 no se pueden leer.** Las razones de 9, 19 o 5 de las últimas filas
salen de contar 1, 2 o 4 coincidencias contra un esperado de 0,05 a 2: con esos números un
Poisson da cualquier cosa. **Son ruido, no señal, y no los usamos para ninguna conclusión.**
`[E]`

## 3. Donde la intuición del investigador sí acierta: la distribución

El total coincide, pero **no está repartido como el azar lo repartiría**. Conjunto barajado:

| Referencia | k | Coincidencias | k-meros con ≥1 | Fracción con ≥1 | Fracción que predice Poisson | Por k-mero positivo | Varianza/media | Máximo en un k-mero |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| *D. maidis* genoma | 16 | 1.979 | 755 | **0,159** | 0,364 | 2,62 | **66,1** | **325** |
| | 17 | 473 | 240 | 0,051 | 0,107 | 1,97 | 18,1 | 81 |
| | 18 | 99 | 72 | 0,015 | 0,028 | 1,38 | 4,7 | 19 |
| *Z. mays* | 16 | 616 | 234 | 0,049 | 0,072 | 2,63 | 5,6 | 23 |
| | 17 | 157 | 62 | 0,013 | 0,019 | 2,53 | 3,9 | 8 |
| *A. mellifera* | 16 | 202 | 65 | 0,014 | 0,045 | 3,11 | 8,0 | 27 |

En el genoma de *D. maidis* y con k = 16, el azar uniforme predice que el **36,4 %** de las
ventanas tendría al menos una coincidencia; lo observado es **15,9 %**, menos de la mitad.
Y sin embargo el total de coincidencias es el esperado. La explicación está en las dos últimas
columnas: la varianza del conteo es **66 veces la media** —un Poisson tiene varianza igual a la
media— y un solo 16-mero del control barajado aparece **325 veces** en el genoma. Las
coincidencias no se reparten: se amontonan sobre unos pocos k-meros, que son los que caen en
familias repetidas.

> **La frase correcta, con la medición atrás.** No es que haya *menos* coincidencias por azar
> de las que dice la estadística: hay las mismas. Lo que hay es **menos ventanas tocadas y más
> coincidencias por ventana tocada**, porque el genoma es repetitivo. Para un tamizaje eso
> importa de los dos lados: se descartan menos candidatos de lo que uno temía, pero los que se
> descartan se descartan con mucha más fuerza. `[E]` la medición, `[H]` la lectura.

El efecto es mucho más fuerte en el genoma (varianza/media 66) que en los transcriptomas
(5,6 en maíz, 8,0 en abeja), que es lo esperable: un transcriptoma RefSeq está desprovisto de
la mayor parte del ADN repetitivo y su redundancia viene de familias génicas e isoformas, no de
transposones. `[H]`

## 4. El conjunto real: eso ya no es azar, es homología

| Referencia | k=16 | k=17 | k=18 | k=19 | k=20 | k=21 | k=22 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| *D. maidis* genoma, obs | 4.285 | 3.003 | 2.692 | 2.617 | 2.580 | 2.550 | 2.524 |
| *D. maidis* genoma, obs/E_u | 2,0 | 5,6 | 20,1 | 78,2 | 308,7 | **1.221,5** | **4.840,3** |
| *Z. mays*, obs/E_u | 2,5 | 2,2 | 1,5 | 1,1 | 0,0 | 0,0 | 0,0 |
| *A. mellifera*, obs/E_u | 1,5 | 1,7 | 2,7 | 0,0 | 0,0 | 0,0 | 0,0 |

La columna del genoma de *D. maidis* **no mide off-target, mide on-target**: dos de los cuatro
genes (BicC_Dm y ATPaseD_Dm) son genes de la propia chicharrita, y sus ventanas se encuentran a
sí mismas. Por eso el observado se aplana en ~2.550 a partir de k = 18 y la razón contra el
esperado explota: el denominador cae ×4 por nucleótido y el numerador no se mueve. **Es la
firma cuantitativa de la homología, y es exactamente lo que no hay que confundir con azar.**
`[E]`

Contra las referencias no objetivo la historia es la contraria: a partir de k = 19 en maíz y
k = 19 en abeja, **cero coincidencias exactas** de las ~4.730 ventanas reales. El riesgo medido
de off-target exacto de nuestros cuatro candidatos sobre maíz y abeja a 21 nt es cero, que es
consistente con lo que el pipeline ya había reportado por otra vía.

## 5. Por qué el salto de nuestra tabla está en 17 y no es gradual

`pipeline/REPORT.md` §4.1 reporta, sobre 10.950 ventanas de 438 genes, un porcentaje de
supervivencia que va de 99,8 % a 21 nt a 91,1 % a 17 nt y se desploma a 72,3 % a 16 nt contra
maíz y abeja, y de 90,7 % a 36,2 % a 7,4 % contra el catálogo de 25 especies. La caída parece
un umbral. **No lo es, y se puede mostrar con una medición en vez de una anécdota.**

Esa tabla no cuenta k-meros: cuenta **ventanas de 21 nt que tienen algún bloque contiguo de ≥ k
nt en la referencia**. Una ventana de 21 contiene 21−k+1 sub-ventanas de largo k, así que el
número esperado de aciertos por ventana bajo azar uniforme es
`λ(k) = (21−k+1) · 2N / 4^k`, y la fracción con al menos un acierto es `1 − e^(−λ)`.
Reconstruimos esa misma cantidad a partir de los conteos exactos
([`scripts/q3b_salto_16_17.py`](scripts/q3b_salto_16_17.py)) y la comparamos con el modelo:

| k | λ uniforme (genoma *D. maidis*) | Sobrevive, Poisson | Sobrevive, medido (control barajado) | Sobrevive, medido (ventanas reales) |
| ---: | ---: | ---: | ---: | ---: |
| 16 | 2,72 | 6,6 % | **54,5 %** | 25,9 % |
| 17 | 0,57 | 56,8 % | **82,8 %** | 36,8 % |
| 18 | 0,11 | 89,3 % | **95,6 %** | 41,8 % |
| 19 | 0,021 | 97,9 % | **98,9 %** | 43,9 % |
| 20 | 0,0035 | 99,6 % | **99,8 %** | 45,2 % |
| 21 | 0,00044 | 100,0 % | **99,9 %** | 46,1 % |

La misma tabla para maíz y abeja está en
[`resultados/q3b_salto_16_17.tsv`](resultados/q3b_salto_16_17.tsv). Dos lecturas:

**Primera: el salto es la saturación de una exponencial, no un umbral.** λ crece un factor ~4
por cada nucleótido que se saca, pero la fracción de ventanas tocadas es `1 − e^(−λ)`, que es
casi igual a λ mientras λ es chico y se satura cuando λ pasa de 1. Entre 21 y 18 nt λ va de
0,0004 a 0,11 y la supervivencia se mueve de 99,9 % a 95,6 %: la curva parece plana. Entre 17 y
16 λ va de 0,57 a 2,72 y la supervivencia cae de 82,8 % a 54,5 %. **El «salto» está donde λ
cruza el orden de 1, y para una referencia de entre 10^8 y 10^9 bases eso cae exactamente entre
16 y 17.** Con el tamaño del catálogo de 25 especies del pipeline —752 MB— la cuenta da
λ(16) = 2,10, λ(17) = 0,44 y λ(18) = 0,088, es decir supervivencias de 12,2 %, 64,6 % y 91,6 %,
que es la forma de su tabla medida (7,4 %, 36,2 %, 66,7 %). `[E]` la cuenta; `[H]` la
correspondencia con su tabla, porque el conjunto de candidatos y de referencias no es el mismo
que el nuestro.

**Segunda: la parte plana de la cola no es azar, es homología.** La columna de ventanas reales
contra el genoma del propio vector se estanca en ~45 % y no sube más aunque k llegue a 21.
Ese piso es on-target. En la tabla del pipeline el piso equivalente es el ~9 % que no sobrevive
a 21 nt contra el catálogo de 25 especies, y ése es el número que de verdad informa sobre
riesgo. Todo lo que se gana bajando el umbral de 21 a 16 **no es riesgo detectado, es azar
detectado**: en el control barajado, que por construcción no tiene ninguna homología, bajar de
21 a 16 nt descarta el 54,5 % de las ventanas. `[E]`

## 6. Una advertencia operativa que salió de paso

El escáner cuenta también en cuántos registros distintos aparece cada ventana. El máximo
observado fue de **70 transcriptos distintos** para una ventana de 16 nt de nuestros genes en
el transcriptoma de maíz, y ninguna ventana superó los 500 registros en ninguna de las tres
referencias. Eso quiere decir que, **con estas tres referencias**, el `-max_target_seqs 500`
que BLAST trae por defecto no trunca. Contra un catálogo de 25 transcriptomas concatenados, o
con umbrales por debajo de 16 nt, el margen desaparece: conviene subirlo igual. `[E]` la
medición; `[H]` la recomendación.
