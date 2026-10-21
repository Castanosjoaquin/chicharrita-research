# Q3 — Apolo Rocket por dentro

Todo lo que sigue sale de `bioinformaticaInta/apolorocket`, commit
`da4aa10114635b3929aa3613ce3f2db42e601cb2` (2024-05-15, cabeza de `main`, verificado con
`git ls-remote`), de su `Documentacion_Endpoints.pdf` de 30 páginas —texto extraído con `pypdf`
local, en `work/C2/runs/endpoints_pdf_reflow.txt`— y de los dos volcados de base de ejemplo que
trae el propio repositorio. El árbol está en `work/C2/apolorocket/`, fuera del control de
versiones. No se corrió: hace falta PostgreSQL con el esquema cargado y el árbol de referencias
en disco. `[E]`

## Qué es, en una línea

Es **el backend de funciones** de la aplicación: diecinueve funciones de Python que reciben la
ruta de un archivo JSON y devuelven una tupla con rutas de archivos de salida —JSON, HTML de
figura— escritos en el `outputDir` que pide la entrada (`mainFunctions.py:13-470`). No hay capa
HTTP, ni autenticación, ni servidor web en este repositorio: lo que el PDF llama «endpoints»
son funciones, y quien las exponga queda fuera de lo publicado. `[E]`

## Qué entra y qué sale

La unidad de trabajo es el **proyecto** (`project`), con género y especie del organismo de
interés y un nombre de usuario. Dentro de un proyecto se corren **comparaciones**: una secuencia
consulta contra una o varias **referencias**, cada una un FASTA indexado con `bowtie-build`
(`externalSoftware.py:18-27`) y, opcionalmente, un GFF3 convertido a un JSON de anotación
(`annotationFunctions.py:15-23`). Las referencias no viven en la base: viven en un árbol de
directorios en disco, `<REFERENCEDIR>/<género>/<especie>/<genome|transcriptome>/<versión>/`
(`externalSoftware.py:13-16`), y la base guarda sólo la fila que las identifica. `[E]`

La secuencia consulta entra **como texto dentro del JSON** (`querySequence`), no como archivo:
`getMaintargetsPlot` la recibe junto con género, especie y nombre, y la guarda en la tabla
`query` (`mainFunctions.py:224-277`). El volcado de ejemplo tiene doce consultas, de 781 a
1.698 nt, de *Arabidopsis thaliana*, *Botrytis cinerea*, *Drosophila melanogaster* y *Oryza
sativa*. No hay ninguna de *Dalbulus maidis*, ni de maíz, ni de un virus. `[E]`

## El pipeline, en tres pasos y en este orden

**Paso 1, blancos principales (`getMaintargetsPlot`, `mainFunctions.py:224-277`).** Parte la
consulta en ventanas del tamaño pedido (`inputOutputFunctions.py:31-49`), corre Bowtie contra
cada referencia de la lista —un proceso por referencia, en serie
(`mainFunctions.py:239-247`)—, agrupa los alineamientos en bloques por solapamiento y escribe
una figura HTML con una línea de tiempo de Plotly por región blanco, más un JSON para paginar la
tabla. Guarda en la base la consulta, la región, la comparación y todos los bloques.

**Paso 2, eficiencia (`getEfficiencyPlot`, `mainFunctions.py:304-355`).** Primero mira si ya hay
eficiencia calculada para esa consulta y ese método; si no, escribe un FASTA temporal, corre
RNAplfold, calcula la eficiencia de cada ventana y guarda **la curva** en la base. Acá es donde
el usuario declara, con `maintargetNumbers`, cuáles de las regiones del paso 1 son el blanco
deseado; el resto queda marcado como off-target en la tabla
`maintarget_comparison_reference_region` (`databaseFunctions.py:320-345`).

**Paso 3, off-targets (`getOfftargetsPlot`, `mainFunctions.py:383-433`).** Toma una **región**
de la consulta —`queryRegionStart` y `queryRegionEnd`, en coordenadas interbase, provistas por
el usuario— y vuelve a correr Bowtie contra la lista de referencias, ahora sólo con ese
fragmento, devolviendo una figura HTML por referencia.

## Los diecinueve endpoints

Los nombres son los de la página 3 del PDF; entre paréntesis, la línea de `mainFunctions.py`
donde está la función y lo que hace que no sea evidente.

Lectura de catálogo: `getAllProjectsInformation` (23), `getAllReferencesInformation` (33),
`getAllQueriesInformation` (43), `getProjectInformation` (53), `getReferenceInformation` (65),
`getQueryInformation` (77), `getQueryProjects` (104), `getReferenceProjects` (118) y
`getProjectComparisons` (89, lista las comparaciones de blancos y de off-targets de un
proyecto). Todas son un `SELECT` volcado a un JSON con nombre aleatorio de veinte letras
(`inputOutputFunctions.py:12-13`), con 0,5 s de tiempo declarado en el PDF.

Alta de datos: `createNewProject` (132) y `createNewReference` (156, corre `bowtie-build` y
parsea el GFF3; el PDF declara 74 minutos y 5 GB de RAM para el genoma humano con un hilo) y
`addNewAnnotationToReference` (198).

Cálculo: `getMaintargetsPlot` (224), `getEfficiencyPlot` (304) y `getOfftargetsPlot` (383), más
sus tres variantes `...FromDB` (279, 356, 434) que vuelven a dibujar desde lo guardado sin
recalcular, y `getTargetsTable` (453), que pagina la tabla de blancos.

## Qué guarda en la base

Quince tablas en PostgreSQL (`apoloRocket.sql`), sin un solo índice declarado aparte de las
claves primarias y las restricciones de unicidad. El eje son tres entidades —`project`, `query`,
`reference`— y dos tipos de comparación, cada una con su cadena de tablas puente hasta el
alineamiento: `maintarget_comparison` → `..._reference` → `..._reference_region`, e igual para
`offtarget_comparison`. Las coordenadas se guardan dos veces, una del lado de la consulta
(`query_region`, `query_region_block`) y otra del lado de la referencia (`reference_region`,
`reference_region_block`), y la tabla `alignment` une un bloque de cada lado con su hebra, sus
desapareamientos y su número de bloque (`apoloRocket.sql:65-80`). `[E]`

La tabla que más dice es `efficiency` (`apoloRocket.sql:81-91`): tres columnas útiles —`query_id`,
`method` y `efficiency_data INT[]`—. **La eficiencia no se guarda por siRNA: se guarda la curva
del gráfico.** Un arreglo de enteros de largo igual al de la secuencia más uno, donde cada
posición dice cuántos siRNA eficientes la cubren. En el volcado con resultados hay dos filas, las
dos con `method = 'sifi21'`, de 1.699 y 1.635 enteros. `[E]` De ahí **no se puede recuperar qué
ventana era eficiente**, sólo la silueta; y el número de eficientes se recupera únicamente porque
la curva es una suma de rectángulos de ancho fijo: 3.280/20 = 164 y 3.380/20 = 169 dan exacto. `[E]`

La anotación de cada región se guarda como **texto** (`reference_region.annotation TEXT`) y se
recupera con `eval()` sobre ese texto (`databaseFunctions.py:202`). Es el `repr` de un
diccionario de Python guardado como cadena y reinterpretado como código al leerlo.

## Cómo puntúa y cómo ordena

**No puntúa y no ordena.** No hay score, ni peso, ni función de agregación, ni umbral de corte
en ninguna parte del repositorio. Lo que existe es:

- el veredicto binario de si-Fi21 por ventana, que no se persiste;
- la curva de cobertura de eficientes, que sí;
- y una tabla de blancos ordenada por `target_number`, que es el **orden de inserción** en el
  diccionario de bloques (`figuresFunctions.py:42-50`), no un ranking. La paginación corta ese
  mismo orden (`databaseFunctions.py:113-146`).

La tabla que ve el usuario (`figuresFunctions.py:172-190`) trae, por región blanco: número,
referencia, nombre de la secuencia, región, largo, anotación, cuántos bloques y, por bloque,
posiciones en consulta y en blanco, desapareamientos y hebra. Ningún campo es un puntaje. `[E]`

## El criterio de off-target, exacto

`externalSoftware.py:43-54` corre, por referencia:

```
bowtie -a -l <tamaño del siRNA> -n <desapareamientos> -y -x <índice> -f <fasta de siRNA> <salida>
```

Cuatro consecuencias, todas leídas del código y del PDF: `[E]`

1. **Cambió el modo de conteo de desapareamientos respecto de si-Fi.** si-Fi21 y sifi21INTA usan
   `-v N`, que cuenta desapareamientos en todo el largo. Apolo Rocket usa `-n N` con `-l` igual
   al tamaño del siRNA, que es el modo «semilla» de Bowtie: los `N` desapareamientos se cuentan
   dentro de los primeros `-l` nucleótidos y pesa además la suma de calidades. Con `-l` igual al
   largo completo las dos cosas casi coinciden, pero `-n` admite **como máximo 3** y el PDF
   declara exactamente ese rango: «can be 0-3» (páginas 18 y 24).
2. **No hay ponderación por región semilla ni por posición.** Un desapareamiento en el
   nucleótido 2 pesa lo mismo que en el 20. Es el mismo defecto que arrastra si-Fi.
3. **No hay filtro de hebra ni de largo mínimo**: se reportan los alineamientos en las dos
   hebras (`bowtieToList` guarda la hebra, `externalSoftware.py:86-104`) y el largo mínimo es el
   tamaño del siRNA, porque la consulta son las ventanas enteras.
4. **Los bloques acumulan desapareamientos.** Al fusionar alineamientos contiguos en un bloque,
   el contador de desapareamientos del bloque se **suma** (`figuresFunctions.py:39`), así que el
   número que muestra la tabla no es «desapareamientos de este siRNA» sino la suma de los de
   todos los siRNA del bloque. En el volcado de ejemplo todos los alineamientos tienen cero
   desapareamientos, así que el efecto no se ve ahí. `[E]`

## Cómo elige regiones, y de qué largo

**No las elige: se las dan.** El largo del siRNA es un parámetro de entrada (`sirnaSize`, 21 en
todos los ejemplos del PDF) y la región de interés para off-targets viene en la entrada como par
de coordenadas. No hay ninguna función que busque la región más densa en eficientes, ni que
compare regiones entre sí. `[E]` La columna `offtarget_comparison.selected_region`
(`apoloRocket.sql:144-156`) sugiere que alguna vez se pensó marcar una región como elegida:
**ningún código del repositorio la escribe** —sólo la lee, en `databaseFunctions.py:61`— y en el
volcado de ejemplo las trece filas están en `false`. `[E]`

Tampoco hay validación de esas coordenadas: `databaseFunctions.py:248` rebana la secuencia con
`[inicio:fin]` sin comprobar nada, y el volcado trae la prueba de que eso pasa en producción —la
consulta `id` 10 es una región «800-100» con secuencia de **largo cero**, insertada igual en la
base junto a su `query_region` con inicio 800 y fin 100. `[E]`

## Qué usa de si-Fi, exactamente

`Sirna.py` y `freeEnergy.py` **son los mismos archivos que en sifi21INTA**: `freeEnergy.py` tiene
el mismo md5 (`cf13a78f945878fb4a9c02ab20f920d8`) y `Sirna.py` difiere sólo en anotaciones de
tipo y comentarios, sin un solo cambio de lógica (diff completo en
`work/C2/diffs/Sirna_inta_vs_apolo.diff`). Las constantes del cálculo también son las mismas, ahora
en `constants.py:5-10`: ventana 80, span 40, **22 °C**, extremo saliente 2, nucleótidos de
extremo 3. Y `calculateAllSirnasEfficiency` (`externalSoftware.py:166-173`) llama al mismo
`Sirna.calculateEfficiency` con los parámetros que llegan por JSON. `[E]`

Es decir: **el motor de eficiencia de Apolo Rocket es el criterio de si-Fi21, con la tabla de
energía de Zuber et al. 2022 como default y con la rama de la regla terminal que saltea la
termodinámica intacta** (`Sirna.py:66-96` en los dos repositorios). Lo que medimos para
sifi21INTA en Q1 y Q2 vale igual acá. `[E]`

## El campo `method` y el método «IA» que no está

`getEfficiencyPlot` y `getEfficiencyPlotFromDB` reciben un parámetro `method`, documentado en el
PDF (páginas 21 y 23) y en el código (`mainFunctions.py:315` y `:359`) como **«'sifi21' or
'IA'»**. El valor viaja a la base, se usa como clave de búsqueda y de inserción
(`databaseFunctions.py:228-236` y `:318`) y es parte de la restricción de unicidad de la tabla
`efficiency`. **Pero no hay ninguna implementación de un método «IA» en el repositorio**: no
existe una rama que mire ese valor, no hay modelo, ni pesos, ni inferencia; el cálculo que corre
es siempre el de si-Fi (`mainFunctions.py:319-328`). Las dos filas del volcado con resultados
dicen `sifi21`. `[E]`

Dicho con cuidado: el esquema está preparado para guardar dos métodos de eficiencia por consulta
y uno de ellos se llama «IA», lo que indica que **estaba previsto** enchufar un modelo ahí. `[H]`
Eso, para un equipo de ingeniería en IA, es el punto de enganche más concreto de todo el
repositorio: el hueco está nombrado en el código.

## Contraste con lo que dice R3

`research/R3_apolo_biotech/REPORT.md` describe la plataforma con fuentes de prensa y de la
empresa. Lo que el código confirma, matiza o contradice:

| Afirmación de R3 | Veredicto contra el código | Fundamento |
|---|---|---|
| «Nadie publicó el criterio de agregación que convierte esos reportes en un orden defendible» (§6.2a) | **Confirmado, y más fuerte de lo que decía** | No es que no esté publicado: en el backend publicado **no existe** ningún puntaje ni orden. Lo único ordenable es el número de blanco, que es orden de inserción |
| «Evalúa más de 140 organismos a la vez» (§4, prensa, `[R]`) | **Compatible, no verificable, y con una advertencia de escala** | `referenceIDs` es una lista sin tope y el bucle corre Bowtie una vez por referencia, en serie (`mainFunctions.py:239-247`). El PDF declara 2 a 14 s para 1 a 3 referencias de *Arabidopsis* y 1,5 a 2,1 min para 1 o 2 de *Oryza*, y dice que siguen trabajando en la eficiencia de ese paso. Extrapolar a 140 referencias da decenas de minutos `[H]` |
| «Consume datos genómicos de NGS de bases públicas y propias» | **Compatible** | `createNewReference` acepta cualquier FASTA más GFF3 opcional y lo indexa; el volcado de ejemplo tiene cinco organismos modelo, genoma y transcriptoma de cada uno |
| «Corre en la nube» | **Ni confirmado ni contradicho** | El repositorio no dice nada de despliegue. Lo que sí trae es una base en `localhost:5432` y un árbol de referencias en un directorio local (`constants.py:11-16`) |
| «Emite reportes automáticos» | **Matizado** | Lo que emite son figuras HTML de Plotly y archivos JSON para tablas paginadas. No hay generación de informe, ni PDF, ni texto |
| «La construyeron con el IABIMO (INTA-CONICET) y la Fundación Sadosky» | **Compatible, con evidencia indirecta** | El repositorio es de la cuenta de bioinformática del INTA, y tanto la constante `REFERENCEDIR` como todos los `outputDir` de ejemplo del PDF cuelgan de un directorio llamado `sadosky` (`constants.py:11`; PDF, páginas 4 a 27). Es una pista de ruta, no una declaración `[H]` |
| R3 no menciona que el motor de eficiencia sea si-Fi | **Hallazgo nuevo** | Lo es, verbatim, incluido el bypass de la regla terminal |

## Lo que no se corrió, y por qué

No se levantó la base. Hacían falta tres cosas que el repositorio no trae: un PostgreSQL con el
esquema, el árbol de referencias indexadas en disco —el PDF ofrece bajarlo de un enlace de Google
Drive, que no se abrió porque no es un servicio de datos y porque no hacía falta para responder
Q3— y una capa HTTP que no está publicada. Lo que sí se hizo fue leer los dos volcados y usar sus
datos reales como evidencia, que es de donde salen los números de esta página. Las figuras HTML de ejemplo pesan entre 3,4 y 3,8 MB cada una y **no se leyeron enteras**: de
`example.efficiency.figure.html` se extrajo sólo el arreglo del trace «Efficient siRNAs» con una
expresión regular, y resultó **idéntico, valor por valor, al `INT[]` guardado en la base** para la
consulta 6 del volcado —1.635 enteros, máximo 14, suma 3.380—. La plataforma dibuja exactamente lo
que guarda. Detalle en `corridas/08_curva_eficiencia_html_vs_volcado.json`. `[E]`
