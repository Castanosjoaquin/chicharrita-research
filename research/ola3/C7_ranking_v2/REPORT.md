# El ranking v2: los cuatro candidatos de EPILAB y dos genes nuevos, a 21 y a 22 nt

Fecha: 2026-10-21. Complementa [`research/ola2/W7_ranking/REPORT.md`](../../ola2/W7_ranking/REPORT.md), que sigue siendo el ranking de partida, y toma lo que midieron [C5](../C5_estructura_genes_ingenieria_inversa/REPORT.md) (los genes nuevos) y [C6](../C6_panel_y_largo/REPORT.md) (el largo de ventana). Reproducible con `tools/sifi21_port/ranking_v2.py`; todos los números salen de `resultados/ranking_v2.json`. Marcadores de `CLAUDE.md`.


## El resultado, en un párrafo

**La v2 reproduce a W7 y no le desarma ninguna conclusión; agrega dos candidatos que entran sin vetos en el medio de la tabla, y muestra qué parte del orden aguanta un cambio de 21 a 22 nt.** Antes de medir nada nuevo el motor reprodujo exacto los cuatro conteos de eficientes, las cuatro fichas y el barrido de 2.000 sorteos de W7. Con el panel de W7 más humano —y sin *Macrosteles quadrilineatus*, decisión D23—, `MP_MRFV` sigue primero y `CP_MRFV` segundo entre los virales; `BicC_Dm` y `ATPaseD_Dm`, tal como los eligió EPILAB, siguen vetados y sin orden entre sí; y la recomendación de mover la región dentro de los dos genes del insecto sigue en pie (`BicC_Dm` pasa de 2123-2422 a 2121-2420 por dos nucleótidos que cambia humano, `ATPaseD_Dm` sigue en 72-371). Los dos genes nuevos, `eth` y `burs-alpha`, no desplazan a nadie: cuando los seis se comparan cada uno en su mejor región, el orden es `MP_MRFV` > `BicC_Dm` > `CP_MRFV` > `eth_Dm` > `bursA_Dm` > `ATPaseD_Dm` (95,7 % de los sorteos) y a 22 nt es `MP_MRFV` > `BicC_Dm` > `eth_Dm` > `CP_MRFV` > `bursA_Dm` > `ATPaseD_Dm` (90,0 %). Lo que los distingue no está en los dos ejes del ranking sino en lo que el ranking no mide: tienen el fenotipo letal publicado en la propia especie (10 % de supervivencia al día 4 contra más del 95 % del control, por microinyección), y `burs-alpha` es el único candidato sin una sola coincidencia perfecta de 19 nt o más contra ninguna referencia en el gen entero. **A 22 nt las puntas del orden aguantan y el medio no** (con la escala absoluta, la que W7 recomienda leer en este nivel): `MP_MRFV` primero, `BicC_Dm` segundo y `ATPaseD_Dm` último a los dos largos, pero `CP_MRFV`, `eth` y `burs-alpha` se reordenan, y las regiones propuestas de `MP_MRFV`, `CP_MRFV`, `eth` y `burs-alpha` se mudan, mientras que las de `BicC_Dm` y `ATPaseD_Dm` se mueven uno o dos nucleótidos.

> **Lo que se deduce, en cinco líneas.** (1) El ranking de W7 aguanta: se reprodujo exacto y agregar humano no mueve ninguna conclusión. (2) Tal como los eligió EPILAB, `BicC_Dm` y `ATPaseD_Dm` quedan vetados y últimos; moviendo la región, `BicC_Dm` sube a segundo y `ATPaseD_Dm` sigue último en el orden por tasas. (3) Los genes nuevos no ganan por diseño; su valor está en la evidencia publicada y, en `burs-alpha`, en una especificidad limpia. (4) El largo de ventana mueve el medio de la tabla y las regiones de cuatro candidatos, pero no las de `BicC_Dm` ni `ATPaseD_Dm`. (5) Quedan abiertas cosas que no podemos cerrar nosotros: una ventana de `eth`, las posiciones del amplicón publicado, la conservación entre poblaciones y el largo de siRNA en hemípteros.

> **Qué es medición y qué es decisión nuestra.** Son medición: los conteos de ventanas eficientes, las coincidencias por referencia, los nulos y las frecuencias del barrido. Son decisión nuestra y están declaradas: que *Macrosteles* no entre al panel (D23); el peso 1,00 de humano; elegir la región de los dos genes nuevos por la misma cascada con la que W7 recomienda regiones; y leer el ranking de diseño y la evidencia publicada como dos ejes separados, sin sumarlos (D24). Las cinco decisiones de agregación de W7 (D16 a D20) no se tocan.


## 1. Qué cambió respecto de W7

`[E]` Antes de contar nada se verificó el entorno contra W7. El motor reproduce los cuatro conteos de eficientes (123, 30, 171 y 29), las cuatro fichas campo por campo —ventanas, eficientes, eficacia, limpieza, exposición, limpias y eficientes, ventanas con off-target, ventanas con 21/21, veto— y las frecuencias del barrido de 2.000 sorteos con la misma semilla. Si alguno hubiera fallado, el script aborta; no abortó. Esa verificación se hizo **sin** la columna de humano, para que fuera la de W7. El primer intento de ancla falló y vale registrarlo: no se había incluido el genoma de *D. maidis*, que para los genes virales cuenta como off-target (D20), y el desfase de una ventana lo delató.

| Conclusión de W7 | En la v2 | ¿Cambió? |
|---|---|---|
| `MP_MRFV` primero y `CP_MRFV` segundo entre los cuatro | `MP_MRFV` primero 98 %, `CP_MRFV` segundo 98 % (antes 99 % y 99 %) | No |
| `BicC_Dm` y `ATPaseD_Dm` no se ordenan entre sí | Tercero `BicC_Dm` 79 % / `ATPaseD_Dm` 21 % (antes 75 % / 25 %) | No (sigue siendo la elección de pesos) |
| Mover la región en `BicC_Dm` a 2123-2422 | A 2121-2420 (35 ventanas eficientes), por la columna de humano | Dos nucleótidos |
| Mover la región en `ATPaseD_Dm` a 72-371 | 72-371, igual | No |
| Con las regiones movidas: `MP_MRFV` > `BicC_Dm` > `CP_MRFV` > `ATPaseD_Dm` | Mismo orden entre los cuatro: `BicC_Dm` segundo 98 % | No |
| Los dos genes del insecto, vetados por *H. vitripennis* | Siguen vetados y últimos a 21 y a 22 nt | No |
| Seis referencias, cuatro candidatos, 21 nt | Seis referencias más humano, seis candidatos, 21 y 22 nt | **Sí: es lo que agrega la v2** |

`[E]` **Humano no cambia ninguna conclusión.** Da cero coincidencias perfectas de 21 nt en los seis genes, como ya había medido C6. Baja la limpieza de las regiones de EPILAB en menos de un centésimo (`MP_MRFV` de 0,9802 a 0,9757; `BicC_Dm` de 0,9334 a 0,9304; `ATPaseD_Dm` de 0,9804 a 0,9724) porque agrega algunos aciertos de un desajuste y de 19 nt, que son del orden de lo que el azar da contra un transcriptoma de 718,6 Mb: para un 19-mero cualquiera la probabilidad de aparecer en alguna de las dos hebras es de unos 2·718,6·10⁶/4¹⁹ ≈ 0,5 %, o sea entre 2 y 13 aciertos esperados por gen contra los 0 a 12 observados (cuenta gruesa, sin corregir composición). La excepción posible es `ATPaseD_Dm` (7 observados contra 2,4 esperados), compatible con que la subunidad D de la V-ATPasa esté conservada. `[H]`


## 2. El panel, y lo que queda afuera

Seis referencias no objetivo más el genoma del vector. Cinco son transcriptomas de RefSeq que W7 ya usaba —maíz, *Harmonia axyridis*, *Apis mellifera*, *Homalodisca vitripennis* y *Folsomia candida*— y se volvieron a bajar para esta corrida (116 MB, accesiones en la sección 9); la sexta es humano (GRCh38.p14), con peso base 1,00 porque, nuestra lectura `[H]`, un acierto ahí frenaría un registro antes que cualquier otro. El genoma de *D. maidis* (GCA_975739785.1) es on-target para los genes del insecto y se excluye del cómputo; para los virales cuenta como off-target, igual que en W7. El barrido mueve los pesos sobre todo el símplex, de modo que el orden que sobrevive no depende de ese peso base.

**Lo que no entra.** *Macrosteles quadrilineatus* queda fuera de esta versión por decisión del equipo (D23), con el argumento de que la especie no está en Argentina, que todavía no verificamos contra un catálogo de distribución `[?]`. La medición existe y no se borra: C6 midió exposición alta en `BicC_Dm` y C5 midió 21 ventanas con coincidencia perfecta en el gen entero de `eth`. Esta versión simplemente no la usa, y por eso toda recomendación de región de este informe dice contra qué panel se evaluó. Tampoco entran los parasitoides de huevos ni los cicadélidos nativos, que no tienen transcriptoma anotado: un peso sobre una referencia que no existe es cero por omisión, no por evidencia. `[?]`


## 3. Los dos candidatos nuevos

`eth` (*ecdysis triggering hormone*) y `burs-alpha` (*bursicon* α) son los dos genes del trabajo de Andrada *et al.* 2026 sobre la muda de *D. maidis* que no estaban en la planilla de EPILAB. C5 los puso primeros en su lista corta porque son los únicos candidatos nuevos con ARNm público de la propia especie (GenBank PZ371507.1 y PZ371508.1; 615 y 468 nt), de modo que la ventana se calcula sobre la secuencia que se sintetizaría y no sobre el ortólogo de otro cicadélido. Los otros candidatos de C5 **no entran**: se diseñaron sobre ortólogos de *Macrosteles*, *Scaphoideus* o *Euscelidius* y la propia medición de C5 muestra que entre el 0,7 % y el 11,1 % de sus 21-meros existen en el genoma del vector, así que no son material para diseñar sobre *D. maidis* hasta recuperar su secuencia.

**Dos aclaraciones que cambian cómo leer los números.** Primero, los conteos de C5 (44 y 33 eficientes) son del modo fiel de si-Fi21; los de acá son del modo corregido (37 y 25), y la diferencia es exactamente la rama de la regla terminal que W5 midió entre el 14 y el 24 % de lo que el original llama eficiente: no son comparables y no se mezclan. Segundo, **la molécula que tiene evidencia es del orden del transcrito entero**: los ARNdc publicados miden 544 y 578 pb frente a los 615 y 468 nt de la secuencia codificante pública que tenemos (en `burs-alpha` el amplicón es más largo que ella, así que incluye regiones no codificantes), y nosotros proponemos 200 nt. Esa región es una extrapolación `[H]`: el piso de longitud está sostenido (unos 60 pb, C4) pero que 200 nt de `eth` o de `burs-alpha` silencien como la molécula completa no está probado.

| Gen (secuencia pública completa) | Ventanas | Eficientes | maíz | *H. axyridis* | *A. mellifera* | *H. vitripennis* | *F. candida* | humano |
|---|---|---|---|---|---|---|---|---|
| `eth_Dm` | 595 | 37 | 0 / 0 / 1 | · | 0 / 0 / 4 | 1 / 5 / 5 | · | 0 / 6 / 6 |
| `bursA_Dm` | 448 | 25 | 0 / 0 / 1 | · | · | 0 / 0 / 3 | 0 / 0 / 1 | · |
| `BicC_Dm` | 2500 | 171 | 0 / 6 / 5 | 3 / 7 / 3 | 0 / 0 / 7 | 40 / 56 / 56 | 0 / 4 / 6 | 0 / 12 / 27 |
| `ATPaseD_Dm` | 471 | 29 | 0 / 3 / 2 | · | 0 / 0 / 1 | 3 / 7 / 24 | 0 / 0 / 1 | 0 / 7 / 6 |
| `MP_MRFV` | 1243 | 123 | 0 / 3 / 18 | · | 0 / 0 / 7 | 0 / 3 / 3 | 0 / 7 / 4 | 0 / 3 / 23 |
| `CP_MRFV` | 508 | 30 | 0 / 0 / 6 | · | 0 / 0 / 2 | 0 / 0 / 2 | 0 / 0 / 2 | 0 / 2 / 2 |

*Cada celda es 21/21 perfectos / ventanas con un bloque perfecto de ≥19 nt / ventanas con un desajuste, sobre la secuencia pública completa y a 21 nt; · = ninguna. Es el riesgo de la molécula que se acerca a la que se probó, no el de la región de 200 nt.*

`[E]` **`burs-alpha` es el candidato más limpio de los seis sobre la secuencia completa:** cero coincidencias perfectas de 21 nt y cero bloques de 19 nt o más contra las seis referencias; solo cinco ventanas con un desajuste. Su región propuesta (13-212, 16 eficientes) tiene cero ventanas con riesgo bajo cualquiera de los tres criterios. **`eth` tiene una sola ventana con coincidencia perfecta de 21 nt** contra *H. vitripennis*, en la posición 347 y no eficiente, y cinco ventanas con un bloque de 19 nt o más (una de ellas es la misma de 21/21); la región propuesta (114-313, 19 eficientes) la evita, pero evitarla cuesta: la región más densa de `eth` (194-393) tiene 22 eficientes y contiene esa ventana. Si una sola ventana debe vetar la molécula completa es una decisión de umbral que no podemos tomar con estos datos y va a la lista de preguntas para el investigador. `[?]`

`[E]` Sobre si elegir región discrimina en estos genes cortos, el resultado repite el de W7: con el nulo de etiquetas `eth` sí (p = 0,018) y `burs-alpha` no (p = 0,145); con el de bloques de 30, ninguno (p = 0,364 y 0,459). En un gen de 468 nt, una región de 200 nt cubre casi la mitad, y no hay mucho que elegir.

| Gen | Regiones de 200 nt | Rango de eficientes | Mediana | Máximo observado | Nulo de etiquetas (media) | p | Nulo de bloques de 30 (media) | p |
|---|---|---|---|---|---|---|---|---|
| `eth_Dm` | 396 | 4–22 | 12 | 22 | 17,2 | 0,0180 | 20,7 | 0,3640 |
| `bursA_Dm` | 249 | 3–17 | 11 | 17 | 14,8 | 0,1450 | 16,3 | 0,4590 |


## 4. El ranking

Dos lecturas, y la segunda es la que hay que usar para comparar. **Nivel 1:** los cuatro de EPILAB con la región que eligió el laboratorio y los dos nuevos con la que proponemos nosotros. Mezcla regiones elegidas por procedimientos distintos —las de EPILAB sin ver los off-targets, las nuestras con la cascada—, así que favorece a los nuevos. **Nivel 3:** los seis, cada uno en la mejor región que la cascada encuentra para su gen. Es la comparación pareja y es la que reportamos como resultado.

Nivel 1, 21 nt (escala absoluta, media geométrica, regla conservadora; 2.000 sorteos):

| Candidato | Región | La eligió | Ventanas | Eficientes | Eficacia | Limpieza | Limpias y eficientes | Con 21/21 | ¿Vetada? |
|---|---|---|---|---|---|---|---|---|---|
| `MP_MRFV` | 1-200 | EPILAB | 200 | 30 | 0,1500 | 0,9757 | 29 | 0 | no |
| `CP_MRFV` | 201-400 | EPILAB | 200 | 17 | 0,0850 | 0,9931 | 17 | 0 | no |
| `BicC_Dm` | 264-563 | EPILAB | 300 | 20 | 0,0667 | 0,9304 | 17 | 22 | **sí** |
| `ATPaseD_Dm` | 151-450 | EPILAB | 300 | 18 | 0,0600 | 0,9724 | 14 | 3 | **sí** |
| `eth_Dm` | 114-313 | nuestra (cascada) | 200 | 19 | 0,0950 | 0,9856 | 18 | 0 | no |
| `bursA_Dm` | 13-212 | nuestra (cascada) | 200 | 16 | 0,0800 | 1,0000 | 16 | 0 | no |

| Candidato | Puesto 1 | Puesto 2 | Puesto 3 | Puesto 4 | Puesto 5 | Puesto 6 |
|---|---|---|---|---|---|---|
| `MP_MRFV` | 98 % | 0 % | 1 % | 1 % | 0 % | 0 % |
| `CP_MRFV` | 0 % | 2 % | 95 % | 2 % | 0 % | · |
| `BicC_Dm` | · | · | · | · | 79 % | 21 % |
| `ATPaseD_Dm` | · | · | 0 % | 0 % | 21 % | 79 % |
| `eth_Dm` | 0 % | 96 % | 2 % | 2 % | · | · |
| `bursA_Dm` | 2 % | 1 % | 2 % | 95 % | · | · |

Orden más frecuente `MP_MRFV` > `eth_Dm` > `CP_MRFV` > `bursA_Dm` > `BicC_Dm` > `ATPaseD_Dm` en el 78,5 %. Con otras combinaciones:

| Combinación | Frecuencia del orden | Orden más frecuente |
|---|---|---|
| geométrica · conservadora · absoluta | 78,5 % | `MP_MRFV` > `eth_Dm` > `CP_MRFV` > `bursA_Dm` > `BicC_Dm` > `ATPaseD_Dm` |
| geométrica · conservadora · min-max | 41,0 % | `MP_MRFV` > `eth_Dm` > `CP_MRFV` > `bursA_Dm` > `BicC_Dm` > `ATPaseD_Dm` |
| suma · conservadora · absoluta | 38,8 % | `MP_MRFV` > `eth_Dm` > `CP_MRFV` > `bursA_Dm` > `ATPaseD_Dm` > `BicC_Dm` |
| cascada (veto + eficientes limpias) | 100,0 % | `MP_MRFV` > `eth_Dm` > `CP_MRFV` > `bursA_Dm` > `BicC_Dm` > `ATPaseD_Dm` |

Nivel 3, 21 nt, todos en su mejor región:

| Candidato | Región | La eligió | Ventanas | Eficientes | Eficacia | Limpieza | Limpias y eficientes | Con 21/21 | ¿Vetada? |
|---|---|---|---|---|---|---|---|---|---|
| `MP_MRFV` | 72-271 | nuestra (cascada) | 200 | 38 | 0,1900 | 0,9796 | 37 | 0 | no |
| `CP_MRFV` | 99-298 | nuestra (cascada) | 200 | 21 | 0,1050 | 0,9910 | 20 | 0 | no |
| `BicC_Dm` | 2121-2420 | nuestra (cascada) | 300 | 35 | 0,1167 | 0,9852 | 34 | 0 | no |
| `ATPaseD_Dm` | 72-371 | nuestra (cascada) | 300 | 21 | 0,0700 | 0,9774 | 17 | 0 | no |
| `eth_Dm` | 114-313 | nuestra (cascada) | 200 | 19 | 0,0950 | 0,9856 | 18 | 0 | no |
| `bursA_Dm` | 13-212 | nuestra (cascada) | 200 | 16 | 0,0800 | 1,0000 | 16 | 0 | no |

| Candidato | Puesto 1 | Puesto 2 | Puesto 3 | Puesto 4 | Puesto 5 | Puesto 6 |
|---|---|---|---|---|---|---|
| `MP_MRFV` | 99 % | 0 % | 0 % | 0 % | 0 % | 0 % |
| `CP_MRFV` | 1 % | 2 % | 96 % | 0 % | 0 % | 0 % |
| `BicC_Dm` | · | 97 % | 2 % | 1 % | 0 % | · |
| `ATPaseD_Dm` | · | · | 0 % | 0 % | 0 % | 100 % |
| `eth_Dm` | · | 0 % | 0 % | 97 % | 3 % | · |
| `bursA_Dm` | 1 % | 0 % | 1 % | 2 % | 96 % | · |

Orden más frecuente `MP_MRFV` > `BicC_Dm` > `CP_MRFV` > `eth_Dm` > `bursA_Dm` > `ATPaseD_Dm` en el 95,7 %. Con otras combinaciones:

| Combinación | Frecuencia del orden | Orden más frecuente |
|---|---|---|
| geométrica · conservadora · absoluta | 95,7 % | `MP_MRFV` > `BicC_Dm` > `CP_MRFV` > `eth_Dm` > `bursA_Dm` > `ATPaseD_Dm` |
| geométrica · conservadora · min-max | 22,8 % | `MP_MRFV` > `BicC_Dm` > `CP_MRFV` > `eth_Dm` > `bursA_Dm` > `ATPaseD_Dm` |
| suma · conservadora · absoluta | 73,5 % | `MP_MRFV` > `BicC_Dm` > `CP_MRFV` > `eth_Dm` > `bursA_Dm` > `ATPaseD_Dm` |
| cascada (veto + eficientes limpias) | 100,0 % | `MP_MRFV` > `BicC_Dm` > `CP_MRFV` > `eth_Dm` > `ATPaseD_Dm` > `bursA_Dm` |

`[E]` **Lo que dice el nivel 3.** `MP_MRFV` primero (99 % de los sorteos con la escala absoluta), `BicC_Dm` segundo (97 %) y `ATPaseD_Dm` último (100 %). Entre medio, `CP_MRFV`, `eth` y `burs-alpha` quedan separados por dos ventanas limpias y eficientes de 200 entre cada par (20, 18 y 16) y por centésimas de limpieza. La cascada, que cuenta limpias y eficientes, los ordena `CP_MRFV`, `eth`, `ATPaseD_Dm`, `burs-alpha`, y le pone `ATPaseD_Dm` por delante de `burs-alpha` por una sola ventana (17 contra 16). La cascada cuenta ventanas y no tasas, así que favorece a las regiones de 300 nt sobre las de 200: es la razón de que ponga a `ATPaseD_Dm` por delante de `burs-alpha`. **Una diferencia de una o dos ventanas sobre 200 está por debajo de la resolución del umbral de si-Fi21**, que ni siquiera reproduce los conteos que declara el laboratorio. Por eso el medio no se lee como orden.

`[E]` **Corrección de lectura (2026-10-21), equivalente a la de W7 §2.1 bis.** ~~Los porcentajes de arriba (99 %, 97 %, 100 %) se leían como robustez del orden.~~ Con la escala absoluta la limpieza casi no tiene palanca (factor 1,015–1,064 entre candidatos contra 2,38–2,50 de la eficacia; piso duro de 0,8533 en el peor caso), de modo que el sorteo de pesos sólo puede dar vuelta un par ya casi empatado en eficacia, y esos porcentajes **miden la escala**, no que un candidato domine a otro: hay 3 pares en conflicto de 6 y sus cruces caen en w* ≈ 0,02, al borde del rango. Bajo la escala min-max las frecuencias de las tablas de esta sección se aflojan. Fuente: auditoría propia registrada en `00_meta/PREGUNTAS_ABIERTAS.md`; no se volvió a medir aquí. Detalle en [`research/ola2/W7_ranking/REPORT.md`](../../ola2/W7_ranking/REPORT.md) §2.1 bis.

`[H]` **Los genes nuevos no mejoran el ranking de diseño y eso es un resultado.** C5 ya lo había anticipado ("ningún gen nuevo se destaca por densidad de eficientes") y acá se confirma con el procedimiento completo: su eficacia (0,0950 y 0,0800) cae en el rango de las regiones de EPILAB, elegidas o movidas (0,0600 a 0,1900), y son genes cortos con poco margen de región. Lo que aportan es otra cosa: un fenotipo publicado en la especie objetivo y, en el caso de `burs-alpha`, el perfil de especificidad más limpio. Ninguna de las dos cosas la mide el ranking.


### Por estrategia, como en W7 (D20)

Los off-targets no significan lo mismo para un gen viral que para uno del insecto, y W7 presenta un ranking por estrategia. Virus, con las regiones de EPILAB: `MP_MRFV` > `CP_MRFV` (98,4 % a 21 nt y 96,9 % a 22). Insecto, con las regiones movidas: `BicC_Dm` > `eth_Dm` > `bursA_Dm` > `ATPaseD_Dm` (96,3 % a 21 nt y 91,9 % a 22). Con las regiones de EPILAB tal como están, el orden de los insectos es `eth` > `burs-alpha` > `BicC_Dm` / `ATPaseD_Dm`, pero ahí compiten regiones vetadas contra regiones ya elegidas por la cascada, y el resultado se explica por el veto, no por el gen.

`[E]` En la estrategia insecto, que es la que el investigador prefirió, `BicC_Dm` pasa a primero **solo si se acepta mover su región**: tal como la eligió EPILAB (264-563) está vetada por 22 ventanas con 21/21 contra *H. vitripennis*. Ese es el mismo mecanismo de W7 y no cambió.


## 5. Veintiuno contra veintidós

Mismo motor, mismo modo corregido, misma versión de ViennaRNA; lo único que cambia es el tamaño de ventana, con la regla terminal conservada en su posición relativa (la decisión de C6). Para hemípteros no hay perfil de longitud de siRNA publicado, así que **no hay forma de saber hoy cuál de los dos largos es el correcto** y reportamos los dos.

| Candidato | Eficientes a 21 | a 22 | En ambos | Jaccard | Región propuesta a 21 | a 22 | ¿Aguanta? |
|---|---|---|---|---|---|---|---|
| `MP_MRFV` | 123 | 123 | 66 | 0,37 | 72-271 | 162-361 | **se muda** |
| `CP_MRFV` | 30 | 29 | 10 | 0,20 | 99-298 | 77-276 | **se muda** |
| `BicC_Dm` | 171 | 174 | 83 | 0,32 | 2121-2420 | 2119-2418 | estable |
| `ATPaseD_Dm` | 29 | 32 | 17 | 0,39 | 72-371 | 71-370 | estable |
| `eth_Dm` | 37 | 42 | 27 | 0,52 | 114-313 | 193-392 | **se muda** |
| `bursA_Dm` | 25 | 29 | 10 | 0,23 | 13-212 | 44-243 | **se muda** |

`[E]` **Las puntas aguantan y el medio no**, bajo la escala absoluta. A 22 nt `MP_MRFV` sigue primero (98 %), `BicC_Dm` segundo (92 %) y `ATPaseD_Dm` último. `CP_MRFV`, `eth` y `burs-alpha` se permutan: a 22 nt `eth` pasa de cuarto a tercero y `CP_MRFV` de tercero a cuarto. Las regiones de `BicC_Dm` y `ATPaseD_Dm` se mueven uno o dos nucleótidos, de modo que **esas dos recomendaciones son robustas al largo**; las de `MP_MRFV`, `CP_MRFV`, `eth` y `burs-alpha` se mudan decenas de posiciones. El conjunto de ventanas eficientes cambia mucho aunque el conteo no: Jaccard de 0,20 a 0,52, con `eth` en el extremo alto (0,52) y `CP_MRFV` en el bajo (0,20).

Nivel 3 a 22 nt:

| Candidato | Región | La eligió | Ventanas | Eficientes | Eficacia | Limpieza | Limpias y eficientes | Con 21/21 | ¿Vetada? |
|---|---|---|---|---|---|---|---|---|---|
| `MP_MRFV` | 162-361 | nuestra (cascada) | 200 | 30 | 0,1500 | 0,9937 | 30 | 0 | no |
| `CP_MRFV` | 77-276 | nuestra (cascada) | 200 | 22 | 0,1100 | 0,9970 | 22 | 0 | no |
| `BicC_Dm` | 2119-2418 | nuestra (cascada) | 300 | 40 | 0,1333 | 0,9834 | 39 | 0 | no |
| `ATPaseD_Dm` | 71-370 | nuestra (cascada) | 300 | 25 | 0,0833 | 0,9766 | 21 | 0 | no |
| `eth_Dm` | 193-392 | nuestra (cascada) | 200 | 26 | 0,1300 | 0,9850 | 26 | 0 | no |
| `bursA_Dm` | 44-243 | nuestra (cascada) | 200 | 18 | 0,0900 | 1,0000 | 18 | 0 | no |

| Candidato | Puesto 1 | Puesto 2 | Puesto 3 | Puesto 4 | Puesto 5 | Puesto 6 |
|---|---|---|---|---|---|---|
| `MP_MRFV` | 98 % | 1 % | 1 % | 1 % | 0 % | 0 % |
| `CP_MRFV` | 1 % | 1 % | 3 % | 94 % | 0 % | · |
| `BicC_Dm` | 1 % | 92 % | 5 % | 1 % | 1 % | 0 % |
| `ATPaseD_Dm` | · | · | · | 0 % | 1 % | 99 % |
| `eth_Dm` | 0 % | 5 % | 90 % | 2 % | 2 % | 1 % |
| `bursA_Dm` | 0 % | 1 % | 1 % | 2 % | 97 % | · |

| Combinación | Frecuencia del orden | Orden más frecuente |
|---|---|---|
| geométrica · conservadora · absoluta | 90,0 % | `MP_MRFV` > `BicC_Dm` > `eth_Dm` > `CP_MRFV` > `bursA_Dm` > `ATPaseD_Dm` |
| geométrica · conservadora · min-max | 12,0 % | `MP_MRFV` > `BicC_Dm` > `CP_MRFV` > `bursA_Dm` > `eth_Dm` > `ATPaseD_Dm` |
| suma · conservadora · absoluta | 61,8 % | `MP_MRFV` > `BicC_Dm` > `eth_Dm` > `CP_MRFV` > `bursA_Dm` > `ATPaseD_Dm` |
| cascada (veto + eficientes limpias) | 100,0 % | `BicC_Dm` > `MP_MRFV` > `eth_Dm` > `CP_MRFV` > `ATPaseD_Dm` > `bursA_Dm` |

Bajo la escala min-max y bajo la cascada las puntas se aflojan: la cascada pone a `BicC_Dm` primero a 22 nt (39 limpias y eficientes contra 30 de `MP_MRFV`) por la misma razón de longitud de región. Es una sensibilidad a la regla de combinación que ya tenía W7 (D16) y no una propiedad nueva de los candidatos.

`[H]` Una regla de método sale de acá: **toda región concreta lleva el largo al que se la eligió**, y las que dependen del largo se reportan con las dos. Cuando dos regiones empatan en limpias y eficientes, la cascada se queda con la primera por posición, que es un desempate arbitrario: a 22 nt `MP_MRFV` tiene dos regiones con 30 limpias y eficientes (162-361 y 820-1019) y la cascada elige la primera sin que haya un motivo.


## 6. El segundo eje: qué evidencia hay de que el gen sirve

El ranking mide calidad de diseño dentro de un gen que alguien ya eligió, no el valor del gen (W7 §5). Para no esconder eso, la evidencia publicada se presenta aparte y **sin puntaje**: sumarla al ranking exigiría una equivalencia entre un fenotipo de microinyección y uno de ingesta que no tenemos. C5 marcó estas filas como `[E]`; acá van como `[R]` porque cada gen descansa en un solo estudio, según la definición de `CLAUDE.md`.

| Gen | Qué se midió en *D. maidis* | Cómo se entregó | Fuente | Marcador |
|---|---|---|---|---|
| `eth_Dm` | Knockdown del transcrito ~90 %; supervivencia 10 % al día 4 frente a >95 % del control (β-lactamasa); defectos de muda. ARNdc de **544 pb**; n = 40 por tratamiento para supervivencia y 3 réplicas biológicas de 3 ninfas para el knockdown | Microinyección en ninfas de quinto estadio recién mudadas, 125 ng por insecto | Andrada *et al.* 2026, *Front Insect Sci* 6:1811933 (vía W1/P3, ola 2) | `[R]` |
| `bursA_Dm` | Knockdown ~95 %; supervivencia 10 % al día 4 frente a >95 % del control. ARNdc de **578 pb**; mismo n | Ídem | Ídem | `[R]` |
| `BicC_Dm` | Oviposición casi nula; transcrito baja >170 veces al día 7. Fenotipo de **esterilidad**, no de letalidad | Microinyección e ingesta (dosis: ver fuente) | Dalaisón-Fuentes *et al.* 2022, *Pest Manag Sci* (PMID 35442515), fila `DM-01` de C5 | `[R]` |
| `ATPaseD_Dm` | Supervivencia 18 % al día 4; efecto en alas no significativo. El catálogo no registra el control de esta fila | Ingesta | Jones, Bernal y Medina 2021 (leído en la ola 2), fila `DM-03` de C5 | `[R]` |
| `MP_MRFV`, `CP_MRFV` | Ninguna medición propia del ARNi sobre estos genes; el mecanismo antiviral es en planta, no en el insecto | — | Checkpoint 1 (investigador) y W1 | `[?]` |

Dos cosas que la tabla obliga a decir. Primero, la entrega es distinta: `eth` y `burs-alpha` se probaron por microinyección, que esquiva la barrera que el laboratorio declara como principal (las dsRNasas del intestino y las glándulas salivales, Dalaisón-Fuentes *et al.* 2023); la evidencia de silenciamiento por ingesta es la de `ATPaseD_Dm`. Segundo, el knockdown de los dos genes nuevos descansa en tres réplicas biológicas de tres ninfas cada una: demuestra que el gen es esencial, no mide una eficacia comparable. La regla de oro de la ficha del investigador aplica sin retoques: detectar ARN no es que haya entrado a la célula correcta, ni que se haya generado siRNA funcional, ni que haya efecto biológico.


## 7. Lo que proponemos, y lo que no se puede decir

`[H]` Para el entregable, la lectura que mejor aguanta es de dos ejes. **Diseño:** `MP_MRFV` primero entre todos y `CP_MRFV` segundo entre los virales; entre los del insecto, `BicC_Dm` en la región 2121-2420 (35 eficientes, limpia a 21 y a 22 nt) por delante de los dos nuevos, y `ATPaseD_Dm` último incluso mejorado. **Evidencia y especificidad:** `burs-alpha` es el candidato de menor riesgo de los seis y `eth` tiene, como `burs-alpha`, un fenotipo letal documentado por microinyección, con un único punto a decidir (la ventana de 21 nt contra *H. vitripennis*). Si el laboratorio quiere un candidato nuevo para probar en paralelo con `BicC_Dm`, la v2 sostiene `burs-alpha`, con la advertencia de que su región de 200 nt es una extrapolación de la molécula de 578 pb que sí se probó.

**Lo que este informe no dice.** No dice que `eth` o `burs-alpha` sean mejores que `BicC_Dm`: por diseño no lo son y por evidencia no se pueden comparar. No dice cuál largo de siRNA es el correcto en hemípteros. No mide eficacia: "eficiente" sigue siendo "pasa el umbral de si-Fi21". Y no dice que las regiones propuestas estén conservadas en las poblaciones de *D. maidis* del noroeste argentino: ese cruce sigue sin hacerse y heredan el pendiente de W7.


## 8. Límites, incluidos los que marcó la ficha del investigador

La ficha optativa del 19 al 26 de octubre (`Investigathon_EpiLab_Fichas_Optativas_v3_19oct.docx.md`, en la raíz del repositorio, sin versionar) es una guía y no una consigna; tomamos tres cosas de ella. **Una coincidencia off-target es una hipótesis de riesgo, no un daño demostrado**: por eso en este informe lo que W7 llama veto se lee como señal para revisar, aunque el cálculo no cambia. **Contar ventanas de 21 nt no dice qué hebra termina en AGO2**: si-Fi21 usa la diferencia de estabilidad de los extremos 5′ como filtro, pero la hebra que carga también depende de otros factores, y el ranking no la modela `[H]`. **Hay que poder justificar el largo de la región**: la nuestra es de 200 nt para los genes cortos y de 300 para los largos por herencia de EPILAB, y para los dos genes nuevos hay evidencia a 544 y 578 pb, no a 200.

Otros límites: el panel es de seis referencias y no incluye cicadélidos nativos ni parasitoides; el genoma de *D. maidis* usado (GCA_975739785.1) no tiene anotación, de modo que las coincidencias contra él se miden sobre secuencia genómica y no solo expresada; ViennaRNA 2.7.2 no es el RNAplfold 2.1.5 que usa el original (los conteos absolutos no son comparables con los de la planilla, las comparaciones internas sí); y las posiciones exactas del amplicón publicado de `eth` y `burs-alpha` sobre el transcrito no se leyeron en esta sesión, de modo que no se puede decir qué fracción de la molécula probada cubre nuestra región. `[?]`


## 9. Cómo reproducirlo

Referencias (solo entró tráfico; las secuencias de EPILAB no salieron de la máquina). Las cinco de RefSeq salen de `https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/…/<accesión>_rna.fna.gz`: maíz `GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0` (37,8 MB), *H. axyridis* `GCF_914767665.1_icHarAxyr1.1` (14,0 MB), *A. mellifera* `GCF_003254395.2_Amel_HAv3.1` (19,5 MB), *H. vitripennis* `GCF_021130785.1_UT_GWSS_2.1` (19,0 MB) y *F. candida* `GCF_002217175.1_ASM221717v1` (25,6 MB); humano `GCF_000001405.40_GRCh38.p14` (135,5 MB, la copia de C6); y el genoma `GCA_975739785.1_ihDalMaid1.1_genomic.fna.gz` (281,7 MB).

El orden en que se listan acá **no** es el orden normativo del panel, y hasta `D76` esa distinción no estaba escrita en ningún lado. El orden de las claves de los objetos `riesgo_por_referencia` y `por_referencia` de este JSON lo heredaba el del tamizador: la versión publicada en `38ad686` los tenía en orden de accesión ascendente, 21 de sus 36 objetos fuera del orden del panel, y la de `625f128` los tiene los 36 en el orden del panel `[M]`. `[H]` La lectura es que las referencias se le pasaron al tamizador en el orden en que el sistema de archivos las listaba, que no quedaba registrado, y por eso el archivo no era reproducible byte a byte. Desde `D76` el orden lo fija `ranking.por_referencia_ordenado()` y es el del panel —`maiz`, `H_axyridis`, `A_mellifera`, `H_vitripennis`, `F_candida`, `humano`— con el vector al final; la clave `panel` de cada bloque del JSON lo publica. Para revisar una regeneración por valor y no por texto: `python tools/verificacion/comparar_json.py <publicado.json> <regenerado.json>`.

```bash
# perfil de eficiencia de los seis genes a 21 y a 22 nt (modo corregido, ViennaRNA 2.7.2)
python research/ola3/C7_ranking_v2/scripts/perfil_k.py

# off-targets: panel de siete referencias, a 21 y a 22 nt (el genoma de D. maidis va aparte)
python tools/sifi21_port/offtarget_21nt.py --size 21 --mm1 --consulta work/sifi_v2/fasta/*_full.fasta \
    --db <refs>/*.fna.gz --salida work/sifi_v2/offtarget_k21
python tools/sifi21_port/offtarget_21nt.py --size 21 --mm1 --consulta work/sifi_v2/fasta/*_full.fasta \
    --db <refs_dm>/*.fna.gz --salida work/sifi_v2/offtarget_dm_k21
# lo mismo con --size 22 y los directorios *_k22

# el ranking v2, con las anclas de W7 adelante
python tools/sifi21_port/ranking_v2.py --trabajo work/sifi_v2 \
    --json research/ola3/C7_ranking_v2/resultados/ranking_v2.json

# este informe y su página
python research/ola3/C7_ranking_v2/scripts/generar_informes.py
```

Necesita `ViennaRNA`, `biopython`, `pyahocorasick` y `numpy`, y las secuencias de EPILAB en `work/sifi_v2/fasta/` (fuera del control de versiones). Las de `eth` y `burs-alpha` salen de `research/ola3/C5_estructura_genes_ingenieria_inversa/resultados/candidatos_c5.fa`.
