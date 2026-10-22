# Conservación entre poblaciones y aislados, y qué parte de la molécula probada cubren nuestras regiones

Fecha: 2026-10-21. Complementa [`research/ola3/C7_ranking_v2/REPORT.md`](../C7_ranking_v2/REPORT.md). Reproducible con `tools/sifi21_port/conservacion.py`; los números salen de `resultados/conservacion.json`. Marcadores de `CLAUDE.md`.


## El resultado, en un párrafo

**Una recomendación de C7 cambia, una aguanta, y para dos candidatos virales el dato no alcanza.** En `BicC_Dm`, la región que C7 recomienda (2121-2420) tiene 35 eficientes y solo 22 son idénticas en los tres transcriptomas públicos de *D. maidis*; la región 922-1221 tiene 36 eficientes, 32 idénticas en los tres, 36 de 36 idénticas en el transcriptoma argentino y las 36 presentes en el genoma de Córdoba son exactas. Es la misma región que C6 había encontrado como salida al veto de *Macrosteles*, y ahora aparece por un motivo que no depende de ese pariente. Cambiarla no mueve el ranking de diseño (`BicC_Dm` sigue segundo, 95 % de los sorteos). En `ATPaseD_Dm`, la región de C7 (72-371) aguanta: sus 21 eficientes son idénticas en los tres transcriptomas y en Córdoba. En el virus, `CP_MRFV` es frágil —de las 17 eficientes de la región de EPILAB solo 7 están en el 75 % o más de los registros que las cubren— y `MP_MRFV`, el primero del ranking, no se puede evaluar: solo 4 de 71 registros de GenBank la cubren y dos de ellos son la referencia. Por último, los cebadores publicados ubican el ARNdc de `eth` (544 pb) sobre la secuencia codificante 1–446 y el de `burs-alpha` (578 pb) sobre 79–468 más 188 nt de 3′UTR `[H]`: la región propuesta para `eth` queda entera dentro de lo probado, y la de `burs-alpha` solo en un 70 %.

> **Lo que se deduce, en cinco líneas.** (1) La recomendación de región para `BicC_Dm` pasa de 2121-2420 a 922-1221: más conservada en todas las fuentes y sin costo en el ranking. (2) La de `ATPaseD_Dm` (72-371) se mantiene. (3) `CP_MRFV` tiene pocas ventanas eficientes que sobrevivan a la variación entre aislados, y de `MP_MRFV` no sabemos nada porque no hay registros. (4) Nuestra región de `burs-alpha` cubre solo el 70 % de lo probado y hay una alternativa dentro de lo probado que cuesta dos ventanas eficientes. (5) Todo esto es conservación entre fuentes públicas y no entre poblaciones de campo del noroeste argentino, que no tenemos.


## 1. Qué parte de la molécula probada cubren nuestras regiones

La Tabla 1 de Andrada *et al.* 2026 (PMC13279319) da los cebadores del ARNdc y de la qPCR de `eth` y `burs-alpha`, pero no sus posiciones: el texto remite a la Figura S1, que no se leyó, y no dice si los amplicones incluyen UTR. Lo que sigue **es una inferencia nuestra** `[H]`: se buscó cada cebador en las dos hebras de la secuencia pública (GenBank PZ371507.1 y PZ371508.1, que son la secuencia codificante) y se dedujo la orientación de dónde aparece. Los rótulos "forward" y "reverse" de la tabla no coinciden con la orientación real: el "forward" del ARNdc de `eth` es antisentido sobre la secuencia. Un cebador con la secuencia del sentido se extiende hacia 3′; uno con la del antisentido, hacia 5′. Con un cebador ubicado y el largo declarado del amplicón se obtiene el otro extremo, que cae fuera de la secuencia pública y por lo tanto es UTR.

| Gen | ARNdc declarado | Cebadores | Amplicón (coordenadas de la secuencia pública) | Parte dentro de la secuencia pública | Fuera (UTR) | qPCR |
|---|---|---|---|---|---|---|
| `eth_Dm` | 544 pb | un cebador en 427–446 (hebra antisentido); el otro cebador no está en la secuencia pública | -97 a 446 | 1–446 de 615 | 98 nt | 428–523 |
| `bursA_Dm` | 578 pb | un cebador en 79–98 (hebra sentido); el otro cebador no está en la secuencia pública | 79 a 656 | 79–468 de 468 | 188 nt | 5′ de la secuencia pública |

Dos lecturas. El ARNdc de `eth` cubre el 72 % de la secuencia codificante (1–446 de 615) más 98 nt río arriba; el de `burs-alpha` cubre 79–468 más 188 nt de 3′UTR, es decir que le falta el primer sexto de la secuencia codificante. Y en `burs-alpha` el amplicón de la qPCR (90 pb) cae río arriba del ARNdc, mientras que en `eth` se solapa con apenas 19 nt: las dos mediciones se hicieron en gran parte fuera de la región silenciada, que es la práctica correcta para no detectar el ARNdc inyectado `[H]`.

| Ventana | Gen | Tramo probado | Región propuesta en C7 | Dentro de lo probado | Eficientes | Mejor región dentro de lo probado | Eficientes | Limpias y eficientes |
|---|---|---|---|---|---|---|---|---|
| 21 nt | `eth_Dm` | 1–446 | 114-313 (ocupa 114–333) | 100 % | 19 | 114-313 | 19 | 18 |
| 21 nt | `bursA_Dm` | 79–468 | 13-212 (ocupa 13–232) | 70 % | 16 | 79-278 | 14 | 13 |
| 22 nt | `eth_Dm` | 1–446 | 193-392 (ocupa 193–413) | 100 % | 26 | 193-392 | 26 | 26 |
| 22 nt | `bursA_Dm` | 79–468 | 44-243 (ocupa 44–264) | 84 % | 18 | 105-304 | 16 | 16 |

`[E]` **`eth`: la región propuesta en C7 (114-313) está entera dentro de lo probado**, a 21 y a 22 nt. **`burs-alpha`: no.** La propuesta a 21 nt (13-212) ocupa 13–232, y solo 79–232 (70 %) está dentro; a 22 nt, el 84 %. La mejor región enteramente dentro de lo probado es 79-278 a 21 nt (14 eficientes y 13 limpias y eficientes, contra 16 de la propuesta) y 105-304 a 22 nt (16 contra 18). Cuesta dos ventanas eficientes y deja el argumento limpio: cada nucleótido de la región propuesta pertenece a una molécula que se probó.

Un límite que conviene decir: las ventanas se calculan sobre la secuencia codificante, así que los 98 nt de 5′UTR de `eth` y los 188 nt de 3′UTR de `burs-alpha` que sí estaban en la molécula probada no se pueden evaluar con lo que tenemos. Y lo que se probó fue la molécula completa, no una región de 200 nt: que esa región silencie como la molécula entera sigue sin estar demostrado `[H]`.


## 2. De dónde sale la conservación, y qué tan buena es cada fuente

No tenemos poblaciones de campo. Lo que existe en bases públicas son tres transcriptomas de *D. maidis* y tres ensamblados genómicos, de orígenes distintos. La procedencia de cada uno se leyó en su registro de GenBank y en el informe de ensamblado de NCBI.

| Fuente | Qué es | Origen declarado | Tecnología | Papel en este análisis |
|---|---|---|---|---|
| `GCA_975739785.1` (hap1) | genoma cromosómico | Reino Unido, muestra de 2024-11-11 (BioProject PRJEB97791) | PacBio y Arima2 | línea de base: separa las ventanas que caen en un empalme |
| `GCA_975739835.1` (hap2) | haplotipo alternativo, 488 Mb en 8.928 contigs | el mismo individuo | PacBio y Arima2 | descripción; **está incompleto en estos loci** y no entra al criterio |
| `GCA_054756405.1` (CIAP v1) | genoma a nivel de contig, 585 Mb, N50 de 50,5 kb | **Argentina: Córdoba**, muestra de 2024-05-27 (INTA) | Oxford Nanopore MinION, Flye | descripción; con tasa de error del orden de la variación que se busca, no entra al criterio |
| `GCWP01` (TSA) | transcriptoma | Illinois Natural History Survey (Johnson *et al.*, sin publicar) | 454, Newbler | criterio; cubre solo fragmentos de `BicC_Dm` |
| `GITV01` (TSA) | transcriptoma | Ohio State University (Xu y Stewart; BioProject PRJNA631706) | Illumina HiSeq, CLC | criterio |
| `GHCC01` (TSA) | transcriptoma de huevos, cuerpo entero | **Argentina**, colecta de 2015-03-01; depositado desde el CeBio, Pergamino (BioProject PRJNA505619) | Illumina HiSeq, Trinity | criterio, y la fuente argentina de mejor calidad |

Tres precauciones de método. **Primera:** el criterio de "conservada" usa solo los transcriptomas, que no tienen intrones ni la tasa de error del ONT. **Segunda:** el haplotipo 2 del Reino Unido es un ensamblado alternativo incompleto —no contiene los loci de `ATPaseD_Dm`, `eth` ni `burs-alpha` (0, 1 y 0 ventanas exactas)— y usarlo como fuente habría contado como variación lo que es un hueco; un primer intento lo hizo y dio números absurdos. **Tercera:** el genoma de Córdoba es solo ONT a 20x, de modo que una ventana con un desajuste puede ser variación o error de lectura; por eso se reporta en tres categorías (exacta, un desajuste, ausente) y no se usa para excluir. Además, un alineamiento local puede esconder una inserción: se marcó como "con diferencia" toda ventana que cruza un salto entre bloques alineados, que es lo que detectó la inserción de 36 nt del transcriptoma argentino en `BicC_Dm`.


## 3. Insecto: lo que dicen los transcriptomas y el genoma de Córdoba

`[E]` `BicC_Dm` es idéntico al 99,88 % al transcriptoma argentino sobre 2.520 nt (tres cambios de base y una inserción de 36 nt en ese transcriptoma, en la posición 1409) y al 99,72 % al de Ohio (siete cambios de base). `ATPaseD_Dm` es idéntica al 100 % al contig de Illinois y al 99,80 % a los de Ohio y Argentina, **con un único cambio de base en las mismas ventanas (242–282) de los dos y ausente en el de Illinois**. Eso es consistente con lo que W5 ya había anotado (§2.5): la secuencia de `ATPaseD_Dm` es un fragmento exacto de un contig público y lleva el alelo del de Illinois `[H]`. Anotamos acá que la frase de D21 "no son subcadenas de nada publicado" no vale para `ATPaseD_Dm`; la decisión no cambia —las dos siguen tratándose como confidenciales y no se subieron— pero la frase hay que corregirla.

| Gen | Fuente | Ventanas con datos | Idénticas | Con diferencia | Tramos de ventanas con diferencia (cada tramo de 41 es un solo cambio de base) |
|---|---|---|---|---|---|
| `BicC_Dm` | GCWP01 (Illinois, 454) | 569 | 419 | 150 | 2089–2128; 2240–2280; 2288–2349; 2336–2376; 2402–2467 |
| `BicC_Dm` | GITV01 (Ohio State, Illumina) | 2500 | 2353 | 147 | 626–666; 1121–1161; 1149–1189; 1316–1356; 2123–2163; 2288–2349 |
| `BicC_Dm` | GHCC01 (Argentina, Illumina) | 2500 | 2417 | 83 | 239–279; 1316–1356; 1390–1429; 2240–2280 |
| `ATPaseD_Dm` | GCWP01 (Illinois, 454) | 471 | 471 | 0 | ninguno |
| `ATPaseD_Dm` | GITV01 (Ohio State, Illumina) | 471 | 450 | 21 | 242–282 |
| `ATPaseD_Dm` | GHCC01 (Argentina, Illumina) | 471 | 450 | 21 | 242–282 |

| Gen | Genoma | Ventanas exactas | Con un desajuste | Ausentes | Sobre cuántas |
|---|---|---|---|---|---|
| `BicC_Dm` | UK hap1 (línea de base) | 2170 | 101 | 229 | — |
| `BicC_Dm` | UK hap2 | 2157 | 13 | 0 | 2170 presentes en hap1 |
| `BicC_Dm` | Cordoba CIAP | 2041 | 37 | 92 | 2170 presentes en hap1 |
| `ATPaseD_Dm` | UK hap1 (línea de base) | 376 | 52 | 43 | — |
| `ATPaseD_Dm` | UK hap2 | 0 | 3 | 373 | 376 presentes en hap1 |
| `ATPaseD_Dm` | Cordoba CIAP | 372 | 2 | 2 | 376 presentes en hap1 |
| `eth_Dm` | UK hap1 (línea de base) | 539 | 10 | 46 | — |
| `eth_Dm` | UK hap2 | 1 | 11 | 527 | 539 presentes en hap1 |
| `eth_Dm` | Cordoba CIAP | 495 | 25 | 19 | 539 presentes en hap1 |
| `bursA_Dm` | UK hap1 (línea de base) | 398 | 10 | 40 | — |
| `bursA_Dm` | UK hap2 | 0 | 1 | 397 | 398 presentes en hap1 |
| `bursA_Dm` | Cordoba CIAP | 225 | 118 | 55 | 398 presentes en hap1 |

*Para los dos genomas que no son la línea de base, los conteos son sobre las ventanas que sí están en hap1, para no confundir un empalme con una diferencia. Un genoma no tiene la secuencia continua de un transcrito: las ventanas que cruzan un intrón faltan en todos, y por eso hap1 no llega al total.*


### `BicC_Dm`: la región recomendada cambia

| Región | Posiciones | Eficientes | Idénticas en los tres transcriptomas | Idénticas en el argentino | En Córdoba: exactas / un desajuste / ausentes | Con 21/21 en el panel | ¿Vetada? | Limpias y eficientes |
|---|---|---|---|---|---|---|---|---|
| elegida por EPILAB | 264-563 | 20 | 20 (100 %) | 20 | 13 / 0 / 0 | 22 | sí | 17 |
| recomendada en C7 | 2121-2420 | 35 | 22 (63 %) | 35 | 14 / 4 / 9 | 0 | no | 34 |
| mejor por conservación | 922-1221 | 36 | 32 (89 %) | 36 | 36 / 0 / 0 | 0 | no | 32 |

`[E]` Las ventanas eficientes de la región que recomendó C7 (2121-2420) se pierden en las otras fuentes porque caen sobre los cambios de base de los transcriptomas (ventanas 2123–2163 y 2288–2349 en el de Ohio, 2240–2280 en el argentino y varios más en los fragmentos de Illinois), donde la tecnología (454) produce errores de homopolímero que no se pueden separar de variación real `[H]`. En el transcriptoma argentino las 35 eficientes son idénticas; la pérdida está en Ohio y en Illinois. Y en el genoma de Córdoba, 9 de las 27 eficientes presentes en hap1 no aparecen, con la salvedad del ONT. La región 922-1221 no tiene ese problema: 32 de 36 idénticas en los tres transcriptomas, todas en el argentino y las 36 presentes exactas en Córdoba.

`[E]` **El costo es chico.** La región 922-1221 tiene 36 eficientes contra 35, 32 limpias y eficientes contra 34 y 22 ventanas con alguna señal de off-target contra 10; ninguna de las dos tiene coincidencias perfectas de 21 nt con el panel. Con la región cambiada, el orden de diseño no se mueve (tabla de abajo). La región de EPILAB (264-563) es la más conservada de las tres —sus 20 eficientes son idénticas en todo— y sigue vetada por *H. vitripennis*, así que la conservación no la rescata.

| Escenario | Orden más frecuente (media geométrica, escala absoluta) | Frecuencia | `BicC_Dm` |
|---|---|---|---|
| regiones de C7 | `MP_MRFV` > `BicC_Dm` > `CP_MRFV` > `eth_Dm` > `bursA_Dm` > `ATPaseD_Dm` | 95,7 % | 97 % segundo |
| con `BicC_Dm` en 922-1221 | `MP_MRFV` > `BicC_Dm` > `CP_MRFV` > `eth_Dm` > `bursA_Dm` > `ATPaseD_Dm` | 94,2 % | 95 % segundo |


### `ATPaseD_Dm`: la recomendación aguanta

| Región | Posiciones | Eficientes | Idénticas en los tres transcriptomas | Idénticas en el argentino | En Córdoba: exactas / un desajuste / ausentes | Con 21/21 en el panel | ¿Vetada? | Limpias y eficientes |
|---|---|---|---|---|---|---|---|---|
| elegida por EPILAB | 151-450 | 18 | 18 (100 %) | 18 | 18 / 0 / 0 | 3 | sí | 14 |
| recomendada en C7 | 72-371 | 21 | 21 (100 %) | 21 | 20 / 0 / 0 | 0 | no | 17 |
| mejor por conservación (vetada) | 137-436 | 24 | 24 (100 %) | 24 | 23 / 0 / 0 | 3 | sí | 19 |

`[E]` Las 21 eficientes de 72-371 son idénticas en los tres transcriptomas y las 20 presentes en hap1 están exactas en Córdoba: el cambio de base de las ventanas 242–282 no toca ninguna eficiente de esa región. La región más densa del gen (137-436) tiene 24 eficientes pero está vetada por *H. vitripennis*, así que la conservación no la recomienda.


### `eth` y `burs-alpha`: sin transcriptoma, solo una descripción

~~No ubicamos contigs de estos dos genes en los transcriptomas~~ **Superado por C11 (2026-10-21):** la búsqueda local encuentra secuencia de ambos en el TSA de Pergamino (GHCC01), verificada letra por letra en el tramo alineado; los hits de Ohio (GITV01) no están verificados. Ver `research/ola3/C11_conservacion_eth_bursa/REPORT.md`. Lo que sigue, tal como se escribió: La búsqueda contra el TSA de NCBI (con las secuencias públicas PZ371507 y PZ371508, no con las de EPILAB) quedó en cola más de media hora sin resultado y se canceló. Su conservación solo se puede describir con el genoma de Córdoba, que es la fuente menos confiable. No se afirma conservación ni variación: se reporta lo que aparece. Es un pendiente concreto: un transcriptoma de *D. maidis* que contenga `eth` y `burs-alpha` permitiría hacer con ellos lo que acá se hizo con `BicC_Dm` y `ATPaseD_Dm`. `[?]`

| Gen | Región propuesta | Eficientes | Presentes en hap1 | Exactas en Córdoba | Con un desajuste | Ausentes |
|---|---|---|---|---|---|---|
| `eth_Dm` | 114-313 | 19 | 19 | 17 | 0 | 2 |
| `bursA_Dm` | 13-212 | 16 | 16 | 12 | 4 | 0 |

`[?]` En `eth` 17 de 19 eficientes están exactas y 2 ausentes; en `burs-alpha`, 12 exactas y 4 con un desajuste. Con un ensamblado ONT eso es compatible con error y con variación a la vez, y no permite decidir.


## 4. Virus: `MP_MRFV` no se puede evaluar y `CP_MRFV` es frágil

Se alineó cada gen contra los 71 registros de MRFV de GenBank (los mismos de W5, rebajados de NCBI) y se midió, ventana por ventana, en cuántos de los registros que la cubren es idéntica. Ningún registro es argentino: de los 71, 45 son de Brasil, 4 de EE. UU., 2 de Ecuador, 1 de Costa Rica y 19 no declaran país `[E]`.

| Gen | Registros de GenBank que lo cubren (de 71) | Por país | Mediana de registros por ventana |
|---|---|---|---|
| `MP_MRFV` | 4 | Brazil 1, USA 1, sin dato 2 | 3 |
| `CP_MRFV` | 65 | Brazil 42, Costa Rica 1, Ecuador 2, USA 1, sin dato 19 | 65 |

`[E]` **`MP_MRFV`: cuatro registros alinean y dos son la referencia** (NC_002786.2 y AF265566.2). Los otros dos son un registro de EE. UU. completo (KM523134.1, 93,75 % de identidad sobre el gen) y un fragmento brasileño de 40 nt. No hay ventana con diez registros que la cubran. Es el candidato que el ranking de diseño pone primero, y su robustez frente a la variación entre aislados **no se puede medir con lo que hay publicado**; contra el único aislado independiente disponible, W5 midió que solo 54 de las 180 ventanas de la región son idénticas. `[?]`

`[E]` **`CP_MRFV`: 65 registros cubren cada ventana, y pocas ventanas son idénticas en la gran mayoría: 118 de 505 llegan al 75 % y 11 al 90 %.**

| Registros considerados | Ventanas evaluables (≥10 registros) | Idénticas en ≥90 % | ≥75 % | ≥50 % |
|---|---|---|---|---|
| todos los registros | 505 | 11 | 118 | 164 |
| solo los 42 brasileños | 505 | 90 | 123 | 164 |

| Región de `CP_MRFV` | Posiciones | Eficientes | Idénticas en ≥75 % de los registros | Fracción |
|---|---|---|---|---|
| elegida por EPILAB | 201-400 | 17 | 7 | 41 % |
| recomendada en C7 | 99-298 | 21 | 4 | 19 % |
| mejor por conservación | 196-395 | 21 | 7 | 33 % |

De las 17 eficientes de la región de EPILAB, 7 están en el 75 % o más de los registros; en la que recomendó C7, 4 de 21. La mejor región por conservación (196-395) llega a 7 eficientes conservadas de 21. Es el reverso de lo que mostró el ranking: `CP_MRFV` es el candidato más limpio, pero casi todas sus ventanas eficientes dejan de ser idénticas en los aislados brasileños, que son los de mayor peso en la muestra. Una región limpia que funciona en un solo aislado no sirve, y acá la cifra es 7. Pesa menos de lo que parece porque un ARNdc largo se procesa en un conjunto de siRNA y no todos necesitan ser idénticos, pero no tenemos con qué cuantificarlo. `[H]`


## 5. Qué cambia en el ranking de C7

`[H]` Tres cosas. **Primera:** para `BicC_Dm`, la región recomendada pasa a 922-1221 sin costo en el orden de diseño. **Segunda:** el primer puesto de `MP_MRFV` descansa en un candidato cuya variación entre aislados es desconocida, y el tercero de `CP_MRFV` en uno con muy pocas ventanas conservadas; las dos cosas deben ir junto al orden de diseño y no debajo. **Tercera:** el argumento de que los candidatos del insecto tienen más respaldo que los virales gana un componente que no tenía: sus regiones recomendadas son idénticas en fuentes argentinas y las virales no se pueden evaluar o no lo aguantan. Esto es una lectura de datos públicos y no una medición sobre poblaciones de campo.


## 6. Límites

La conservación entre fuentes públicas no es conservación entre poblaciones de campo: son tres transcriptomas de laboratorio o de colonia y un genoma de una muestra de Córdoba, y ninguno fue diseñado para medir variación. Con tres fuentes una ventana "idéntica en todas" no descarta variación en una cuarta. Los fragmentos de Illinois (454) mezclan variación y error de secuenciación. El criterio de MRFV (idéntica en al menos el 75 % de los registros que cubren la ventana, con al menos diez) es una decisión nuestra; la tabla da los umbrales de 50, 75 y 90 % para que se vea cuánto cambia. Los registros brasileños pesan 42 de 65, de modo que la muestra describe a Brasil más que a cualquier otro lugar. El análisis se hizo a 21 nt y no se repitió a 22. Por último, quedan sin evaluar los 98 nt de 5′UTR de `eth` y los 188 de 3′UTR de `burs-alpha`, y las posiciones exactas de los amplicones dependen de la Figura S1 del artículo, que no se leyó. `[?]`


## 7. Cómo reproducirlo

Fuentes, todas públicas y bajadas a disco (solo entró tráfico): los dos genomas `GCA_975739835.1_ihDalMaid1.1_alternate_haplotype` (135,0 MB) y `GCA_054756405.1_CIAP_v1` (179,9 MB) del FTP de NCBI bajo `genomes/all/GCA/`; los nueve contigs TSA de `tsa/` (`GITV01000968.1`, `GITV01001458.1`, `GHCC01002326.1`, `GHCC01051703.1`, `GCWP01003534.1`, `GCWP01003535.1`, `GCWP01004692.1`, `GCWP01004693.1`, `GCWP01010867.1`), que son los que W5 ya había ubicado; y los 71 registros de MRFV, por E-utilities (`Maize rayado fino virus[Organism]`).

```bash
# off-targets de los cuatro genes del insecto contra los dos genomas nuevos
python tools/sifi21_port/offtarget_21nt.py --size 21 --mm1 --consulta work/sifi_v2/fasta/{BicC_Dm,ATPaseD_Dm,eth_Dm,bursA_Dm}_full.fasta \
    --db <genomas>/GCA_975739835.1*.fna.gz --salida work/sifi_v2/cons_hap2
python tools/sifi21_port/offtarget_21nt.py --size 21 --mm1 --consulta work/sifi_v2/fasta/{BicC_Dm,ATPaseD_Dm,eth_Dm,bursA_Dm}_full.fasta \
    --db <genomas>/GCA_054756405.1*.fna.gz --salida work/sifi_v2/cons_ciap

# la conservación, los amplicones y el efecto sobre el ranking
python tools/sifi21_port/conservacion.py --datos <dir con tsa/ mrfv/ gen/> \
    --json research/ola3/C8_conservacion/resultados/conservacion.json

# este informe y su página
python research/ola3/C8_conservacion/scripts/generar_informes.py
```

Necesita `ViennaRNA`, `biopython`, `pyahocorasick` y `numpy`, y los resultados de C7 en `work/sifi_v2/`.
