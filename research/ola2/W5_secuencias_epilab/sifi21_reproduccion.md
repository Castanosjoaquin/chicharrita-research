# si-Fi21 contra la planilla de EPILAB: conteos, regiones y off-targets

Fecha: 2026-10-19. Herramientas: `tools/sifi21_port/` (port propio de si-Fi21 a
Python 3 sin interfaz; ver su `CAMBIOS.md`) y `tools/sifi21_port/offtarget_21nt.py`
(tamizaje exacto de 21 nt). Fuente de las secuencias: `Sequences_EPILAB.xlsx`,
hoja `Hoja1`, las cuatro filas de datos. Todo local; nada salió de la máquina.

Tres resultados:

1. **Ninguna configuración de si-Fi21 reproduce los cuatro conteos declarados.**
2. **Las cuatro regiones elegidas por EPILAB están por debajo del óptimo** por
   densidad de siRNA eficientes, entre un 25 % y un 46 %.
3. **Los off-targets no explican esas elecciones.** En `BicC_Dm` la contradicen
   de frente: la región elegida es a la vez menos eficiente y once veces más
   expuesta que la mejor alternativa.

---

## Corrección a la versión anterior de este informe

La primera versión se escribió sin la planilla, reconstruyendo dos secuencias desde
`NC_002786.2`, y tomó de `secuencias.json` que la región elegida de `CP_MRFV` era
la 1-200. **Es la 201-400.** El hallazgo sobre esa región estaba mal dimensionado:
decía 8-9 eficientes contra 21, y con la región correcta son 17 contra 21.

Lo que sí se validó al llegar la planilla: las dos secuencias virales que se habían
reconstruido desde el NCBI son **idénticas byte a byte** a las de EPILAB, así que la
medición anterior sobre ellas era correcta.

## Los datos

| Gen | Función | Largo | Región elegida | Declarado |
|---|---|---|---|---|
| `MP_MRFV` | proteína de movimiento | 1.263 | 1-200 | 114 |
| `CP_MRFV` | proteína de cápside | 528 | 201-400 | 35 |
| `BicC_Dm` | Bicaudal C | 2.520 | 264-563 | 199 |
| `ATPaseD_Dm` | subunidad D de V-ATPasa | 491 | 151-450 | 33 |

Las columnas 7 y 8 de la planilla dicen «200-400» para `CP_MRFV`, que son 201
posiciones para una secuencia de 200 nt. Se resolvió localizando la subcadena
exacta: es **201-400**. Las otras tres coinciden exacto con lo declarado.

La **columna 9 de la planilla se llama «Nro de eficientes por región?»**, con signo
de pregunta, y **está vacía en las cuatro filas**. Es la que el investigador pidió
llenar en el checkpoint. Está más abajo.

## 0. El port está verificado contra el programa original `[E]`

Todo lo que sigue depende de que nuestro port calcule lo mismo que si-Fi21. Eso ya
no es un supuesto: se corrió el programa original, con su interfaz gráfica, sobre
**los cuatro genes**, y **los cuatro conteos coinciden exacto**.

| Gen | Hits de si-Fi | siRNA eficientes de si-Fi | Port, modo fiel + RNAplfold 2.1.5 |
|---|---|---|---|
| `ATPaseD_Dm` | 471 | **42** | **42** |
| `CP_MRFV` | 508 | **32** | **32** |
| `MP_MRFV` | 1.243 | **133** | **133** |
| `BicC_Dm` | 2.504 | **212** | **212** |

Salidas crudas del programa en `analisis/sifi21_original_*.csv`.

**El caso de `BicC_Dm` merece una nota, porque es donde se ve el mecanismo que
podría inflar un conteo.** si-Fi reporta 2.504 hits y el gen tiene 2.500 ventanas.
La diferencia no es un error: `general_helpers.py:113` cuenta **un registro por hit
de Bowtie, no un siRNA único**. El gen tiene dos pares de 21-meros repetidos dentro
de sí mismo —posiciones 2411/2488 y 2412/2489—, así que esas cuatro consultas
matchean en dos lugares cada una y aportan cuatro registros de más. Los cuatro son
**no eficientes**, de modo que el conteo de eficientes no se infla y la coincidencia
con nuestro port no es casual. `[E]`

Esto le da peso a una de las hipótesis sobre por qué los conteos de EPILAB no se
reproducen: **con una base de datos distinta el mismo criterio da otro número.**
Acá la base contenía sólo los cuatro genes; contra un transcriptoma completo, con
parálogos e isoformas, muchas ventanas tendrían varios hits y el conteo subiría sin
que cambie un solo parámetro. `[H]`

La corrida usó los valores por defecto de la interfaz —tamaño 21, 0 desajustes,
umbral de extremos 1,00, accesibilidad 0,10, ventana 8, y las cuatro casillas
tildadas, incluida la regla del nucleótido terminal 5'— y una base de Bowtie
construida con el `bowtie-build` del propio instalador sobre los cuatro genes.

Verificación adicional, independiente del número: la curva roja del «RNAi design
plot» de si-Fi —que no es eficiente sí/no por ventana, sino cuántos siRNA eficientes
se superponen a cada posición del ARNm— se reprodujo con nuestro port y **coincide
tramo por tramo**: ocho tramos separados, en las mismas posiciones, con las mismas
alturas (máximo 9 en 150-156, luego 8 en 287-297), y la línea azul plana en 21.

**Qué habilita esto.** Si el modo fiel es fiel, entonces la diferencia que mide el
modo corregido es real y no un artefacto nuestro: en este gen son 8 siRNA que si-Fi
declara eficientes salteándose los filtros termodinámicos, 42 contra 34.

### El defecto que sí cambia los números: la regla terminal no filtra, ramifica

Es el hallazgo que justifica que el port tenga un modo corregido, y la verificación
de arriba es lo que lo convierte en una medición y no en una lectura del código.

si-Fi compone primero un veredicto termodinámico —selección de hebra, estabilidad de
extremos y accesibilidad, en conjunción— y después aplica una regla sobre los
nucleótidos 19 y 2. Esa segunda regla **no es un filtro: es una ramificación**, y una
de sus cuatro ramas devuelve «eficiente» sin mirar el veredicto termodinámico.
Concretamente, cuando el nucleótido 19 es A o T y el 2 es G o C, las líneas 535-541
de `sifi_pipeline.py` deciden mirando **sólo la accesibilidad**: un siRNA que falló
la selección de hebra y la estabilidad de extremos puede quedar clasificado como
eficiente por esa vía.

Medido ventana por ventana, con el mismo RNAplfold en los dos modos: `[E]`

| Gen | Fiel (= si-Fi) | Corregido | Entran por el bypass | En sentido contrario |
|---|---|---|---|---|
| `MP_MRFV` | 133 | 114 | **19** (14 %) | 0 |
| `CP_MRFV` | 32 | 25 | **7** (22 %) | 0 |
| `BicC_Dm` | 212 | 162 | **50** (24 %) | 0 |
| `ATPaseD_Dm` | 42 | 34 | **8** (19 %) | 0 |

Entre el **14 % y el 24 %** de lo que si-Fi reporta como eficiente lo es sólo porque
la regla terminal se saltea la física. No es un caso de borde.

**Por qué el efecto tiene ese tamaño.** La rama del bypass cubre entre el 24 % y el
29 % de las ventanas de cada gen. Ahí el original exige una sola condición en lugar
de tres, así que deja pasar de más alrededor del 6 % de esa franja. Es poco sobre el
gen entero, pero el conjunto de eficientes ronda el 10 % de las ventanas: un efecto
chico en absoluto se vuelve de dos dígitos en relativo, porque lo que se cuenta es
un subconjunto chico.

**Qué dice esta medición sobre el modo corregido**, que es su propio test: las 84
diferencias caen **todas** en esa rama, ninguna en las otras tres, y **ninguna
ventana va en sentido contrario**. Si la regla corregida hubiera cambiado algo más
que el bypass, aparecerían diferencias en las demás ramas. Y las restas cierran
exactas en los cuatro genes (133−19=114, 32−7=25, 212−50=162, 42−8=34), lo que no
pasaría si hubiera ventanas moviéndose en las dos direcciones. El modo corregido es
un subconjunto estricto del fiel.

> **Corrección de una versión anterior.** Este hallazgo se reportó primero como «11
> de 133, entre el 8 y el 9 %». Ese número salía de restar dos totales —133
> eficientes menos 122 que pasan la termodinámica— y el total termodinámico incluye
> ventanas de la rama 4, que los dos modos rechazan igual. **Restar totales no
> cuenta ventanas.** Fue un error de descripción y no de cálculo: los conteos de los
> dos modos nunca cambiaron, así que la verificación contra el programa original, la
> comparación con los conteos declarados, la elección de regiones y el cruce con
> off-targets quedan intactos. Lo único que cambia es el tamaño del defecto, y
> cambia en contra del original.

### Tres defectos operativos de si-Fi21 encontrados al hacerlo

Ninguno afecta a nuestros números, pero cualquiera que intente correr el programa se
los va a cruzar, así que quedan documentados. `[E]`

1. **No encuentra su propio RNAplfold.** `sifi_pipeline.run_rnaplfold` hace
   `os.chdir()` al directorio de la herramienta y después llama
   `subprocess.Popen(["RNAplfold", ...], cwd=<temporal>)`. En Windows, pasar `cwd`
   hace que la búsqueda del ejecutable se haga desde ahí y no desde el directorio del
   padre, así que falla con `FileNotFoundError` salvo que el directorio esté en el
   PATH. `run_bowtie` no tiene el problema porque no pasa `cwd`: es la única
   diferencia entre las dos funciones. **El síntoma es que el botón Start no hace
   nada**, porque el error cae en un `else` que nunca asigna `lunp_data` y el
   `return lunp_data` siguiente tira `UnboundLocalError`, que el slot de Qt se traga.
   *Solución:* lanzar el programa con `%LOCALAPPDATA%\siFi2015\RNAplfold` y
   `...\Bowtie` en el PATH.
   `[H]` Es probable que sea a lo que el investigador se refirió en el checkpoint
   cuando dijo que el programa «no anda bien». Quien tenga ViennaRNA instalado aparte
   nunca ve el bug.
2. **La tabla de resultados no se muestra nunca.** `imageviewer.ImageViewer` recibe
   `table_data` y sólo la usa en `export_table`: la ventana de resultados muestra la
   imagen y nada más. El número de eficientes, que es el resultado principal, sólo se
   obtiene por el menú **Save as → Table (CSV)**.
3. **La exportación corrompe el nombre del archivo.** `export_table`, `export_image`
   y `export_gbk` hacen `filename += filename + '.csv'` cuando falta la extensión, o
   sea concatenan la ruta consigo misma. Hay que escribir la extensión a mano.

## 1. El conteo declarado no es reproducible con si-Fi21

Se barrieron 15.120 configuraciones por gen, exigiendo que una sola configuración
reprodujera **los cuatro** conteos: temperatura (22, 25, 37 °C), motor de plegado
(RNAplfold 2.1.5 del instalador de si-Fi contra ViennaRNA 2.7.2), modo (fiel y
corregido), ventana de accesibilidad u (1 a 21), umbral de estabilidad de extremos
(0 a 2 kcal/mol), umbral de accesibilidad (0,01 a 0,3) y regla terminal sí/no.

**Ninguna lo logra.** El mejor error acumulado es 8 sobre ~381 siRNA declarados, y
lo alcanzan dos configuraciones a 25 °C con umbral de extremos 2,0 —no el 1,0 por
defecto— que aciertan `BicC_Dm` exacto y fallan los otros tres.

Con los valores por defecto del programa:

| Gen | Declarado | Fiel + 2.1.5 | Fiel + 2.7.2 | Corregido + 2.1.5 | Corregido + 2.7.2 |
|---|---|---|---|---|---|
| `MP_MRFV` | 114 | 133 | 142 | 114 | 123 |
| `CP_MRFV` | 35 | 32 | 39 | 25 | 30 |
| `BicC_Dm` | 199 | 212 | 223 | 162 | 171 |
| `ATPaseD_Dm` | 33 | 42 | 35 | 34 | 29 |

El orden de magnitud es correcto —entre 5,9 % y 11,4 % de ventanas eficientes,
contra 6,7 % a 9,2 % declarados—, pero el número exacto no sale. `[E]`

Una advertencia de método que vale registrar: en la primera pasada, con solo dos
genes, el modo corregido con RNAplfold 2.1.5 dio **exactamente 114** en `MP_MRFV` y
pareció la respuesta. Esa misma configuración da 25 en `CP_MRFV` contra 35. Con
15.120 configuraciones y conteos de dos o tres cifras, los aciertos aislados son
esperables. Agregar los otros dos genes subió el error de esa configuración a 25.

`[H]` Las explicaciones que sobreviven: que el laboratorio corriera una versión
modificada —el investigador dijo en el checkpoint que cambió parámetros químicos—;
que el conteo sume un registro por hit de Bowtie y no un siRNA único
(`general_helpers.py:113`), lo que lo haría dependiente de la base de datos usada;
o que el número venga de la plataforma propia que están construyendo encima.

## 2. La columna 9: eficientes por región

El investigador describió el procedimiento: recortar la región, subirla como
archivo nuevo y calcular sobre ella. Eso da la columna «aislada». Se agrega la
columna «en contexto» —las mismas ventanas, pero tomadas de la corrida del gen
entero— porque **no dan lo mismo**, y la diferencia es grande:

| Gen | Región | Aislada | En contexto | Gen entero |
|---|---|---|---|---|
| `MP_MRFV` | 1-200 | 16 | 30 | 123 |
| `CP_MRFV` | 201-400 | 14 | 17 | 30 |
| `BicC_Dm` | 264-563 | 17 | 20 | 171 |
| `ATPaseD_Dm` | 151-450 | 16 | 18 | 29 |

Modo corregido con ViennaRNA 2.7.2. En modo fiel con RNAplfold 2.1.5 las aisladas
son 18, 12, 15 y 22.

`[E]` **El número depende de si la región se plega sola o dentro del gen**, y la
diferencia llega al 47 % en `MP_MRFV` (16 contra 30). La causa es el término de
accesibilidad: RNAplfold evalúa el plegado local, y un fragmento recortado pierde
el contexto que apareaba o liberaba su extremo. Dos efectos se suman: las primeras
20 posiciones del fragmento aislado no tienen contexto aguas arriba, y la corrida
aislada produce 180 o 280 ventanas mientras que el conteo en contexto abarca las
200 o 300 posiciones de inicio.

Consecuencia práctica: **si se va a comparar regiones, hay que fijar el
procedimiento**, porque las dos variantes no son comparables entre sí. Para llenar
la planilla con el procedimiento que describió el investigador, la columna correcta
es la aislada: **16, 14, 17 y 16**.

## 3. Las regiones elegidas no son las más densas

| Gen | Región elegida | Eficientes | Mejor región del mismo largo | Eficientes | Brecha |
|---|---|---|---|---|---|
| `MP_MRFV` | 1-200 | 30 | 72-271 | 38 | −21 % |
| `CP_MRFV` | 201-400 | 17 | 99-298 | 21 | −19 % |
| `BicC_Dm` | 264-563 | 20 | 2123-2422 | 37 | **−46 %** |
| `ATPaseD_Dm` | 151-450 | 18 | 136-435 | 24 | −25 % |

Conteo en contexto, modo corregido. En las cuatro hay una región mejor por
densidad. `[E]`

Esto responde lo que el investigador planteó él mismo: dijo que en teoría debería
haber elegido las regiones con más eficientes, que tal vez no lo hizo, y que quizá
fue por off-targets, pero que no lo recordaba —«fue hace dos años».

## 4. El cruce con off-targets a 21 nt

### Método

Tamizaje exacto, no heurístico: para cada ventana de 21 nt del gen entero se busca
coincidencia perfecta contra seis referencias públicas descargadas a disco, en las
dos hebras, con un autómata de Aho-Corasick en una sola pasada por base. Criterio
de riesgo: **bloque contiguo perfecto de 19 nt o más**, que es el umbral que usa la
revisión de Cedden 2026 ya registrada en `FUENTES.md`. Referencias: maíz
(`GCF_902167145.1`), *Homalodisca vitripennis* (`GCF_021130785.1`), *Apis mellifera*
(`GCF_003254395.2`), *Harmonia axyridis* (`GCF_914767665.1`), *Folsomia candida*
(`GCF_002217175.1`) y el genoma de *Dalbulus maidis* (`GCA_975739785.1`).

Para `BicC_Dm` y `ATPaseD_Dm` el genoma de *D. maidis* se excluye del cómputo: ahí
los hits son **on-target**, y de hecho lo confirman (2.170 de 2.500 ventanas de
`BicC_Dm` tienen coincidencia perfecta de 21/21 en su propio genoma).

**Validación del método** `[E]`: las columnas de bloque perfecto ≥19 nt y 21/21
reproducen **exactamente, en las 20 celdas**, los conteos que W5 obtuvo en octubre
con BLAST+ local sobre las regiones elegidas. Dos implementaciones independientes
—coincidencia exacta contra heurística de semillas— dan el mismo número.

**Discrepancia encontrada en el criterio de 1 desajuste** `[E]`: ahí no coinciden, y
el exacto encuentra más — 16 contra 5 en `BicC_Dm`, 17 contra 9 en `ATPaseD_Dm`.
La causa es identificable: `blastn-short` con `word_size 11` no puede sembrar un
21-mero cuyo único desajuste cae en la posición 11, porque deja dos bloques de 10.
**Los conteos de 1 desajuste de W5 son subestimaciones**, por hasta un factor de
tres. El criterio de bloque perfecto no está afectado.

### Resultado

| Gen | Región | Eficientes | Ventanas con off-target | Mejor región | Eficientes | Con off-target |
|---|---|---|---|---|---|---|
| `MP_MRFV` | 1-200 | 30 | 6 | 72-271 | 38 | 6 |
| `CP_MRFV` | 201-400 | 17 | **0** | 99-298 | 21 | **0** |
| `BicC_Dm` | 264-563 | 20 | **33** | 2123-2422 | 37 | **3** |
| `ATPaseD_Dm` | 151-450 | 18 | 7 | 136-435 | 24 | 7 |

`[E]` **La hipótesis de los off-targets no se sostiene en ningún gen, y en
`BicC_Dm` queda refutada.** Ahí la región elegida tiene 20 siRNA eficientes y 33
ventanas con off-target, mientras que la región 2123-2422 tiene 37 eficientes y
solo 3: **domina en los dos ejes a la vez**, casi el doble de eficientes con un
onceavo de la exposición. No hay compromiso que justifique la elección.

En `CP_MRFV` el gen entero tiene **cero** off-targets en las seis referencias, así
que no había nada que optimizar por ese lado. En `MP_MRFV` la exposición es idéntica
en las dos regiones (6 ventanas), y de las 22 ventanas con off-target del gen
entero solo 2 son eficientes. En `ATPaseD_Dm` también es idéntica (7 y 7).

### Dónde está el riesgo

Por base, ventanas afectadas en el gen entero y cuántas de esas son eficientes:

| Base no objetivo | `MP_MRFV` | `CP_MRFV` | `BicC_Dm` | `ATPaseD_Dm` |
|---|---|---|---|---|
| *H. vitripennis* (chicharrita no objetivo) | 3 / 0 | 0 | **56 / 1** | 7 / 2 |
| Maíz (el cultivo) | 3 / 0 | 0 | 6 / 0 | 3 / 0 |
| *H. axyridis* (enemigo natural) | 0 | 0 | 7 / 0 | 0 |
| *F. candida* (fauna del suelo) | 7 / 0 | 0 | 4 / 0 | 0 |
| *A. mellifera* (polinizador) | **0** | **0** | **0** | **0** |
| *D. maidis* (on-target de los genes del insecto) | 9 / 2 | 0 | 2.245 | — |

Tres lecturas. `[E]` **Cero coincidencias en *Apis mellifera*** para los cuatro
genes, que es la mejor noticia del cuadro. **El riesgo está concentrado en
*H. vitripennis***: 56 ventanas de `BicC_Dm`, de las cuales 40 con coincidencia
perfecta de 21/21, lo que es esperable porque Bicaudal C está conservado entre
cicadélidos. Y aparecen **3 ventanas de `BicC_Dm` con 21/21 perfecto en
*H. axyridis***, una vaquita predadora, o sea un enemigo natural del propio
objetivo.

`[?]` Advertencia de alcance, ya registrada en `PREGUNTAS_ABIERTAS.md`: el panel
sigue siendo de especies modelo. Los ceros de *Apis* son reales, pero la ausencia
de riesgo en cicadélidos nativos y parasitoides **no está medida**, porque no hay
transcriptomas. Y seis referencias no son el ambiente.

## Cómo reproducirlo

```bash
# 1. conteo y barrido de configuraciones
python tools/sifi21_port/barrido.py \
    work/sifi_check/MP_MRFV_full.fasta=114  work/sifi_check/CP_MRFV_full.fasta=35 \
    work/sifi_check/BicC_Dm_full.fasta=199  work/sifi_check/ATPaseD_Dm_full.fasta=33

# 2. tamizaje de off-targets de 21 nt (las referencias se bajan a work/offtarget_db/)
python tools/sifi21_port/offtarget_21nt.py \
    --consulta work/sifi_check/*_full.fasta \
    --db work/offtarget_db/*.fna.gz --salida work/sifi_check/offtarget_full

# 3. cruce
python tools/sifi21_port/cruce.py --gen BicC_Dm --region 264 563 \
    --ontarget GCA_975739785.1_ihDalMaid1.1_genomic \
    --dir work/sifi_check --offtarget work/sifi_check/offtarget_full
```

Las secuencias, las referencias y los TSV por ventana quedan en `work/`, fuera del
control de versiones. Se publica el generador, no el dato derivado del corpus.
