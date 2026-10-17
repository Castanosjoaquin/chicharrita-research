# W2 — Las herramientas del corpus, por dentro

Análisis de ingeniería de las dos herramientas que el corpus oficial del
Investigathón entrega bajo el rótulo «Herramientas de diseño y verificación de
off targets»: **dsRNAEngineer** y **NCBI BLAST**. No son archivos: son dos
enlaces dentro de `YHat-Biotech/Links de interes.docx`, que abrimos y
verificamos (cuatro hipervínculos en `word/_rels/document.xml.rels`, los dos
primeros a NCBI y bases de datos —insumo de W3—, los dos últimos a estas
herramientas). El corpus no trae código, binarios, documentación local ni
credenciales.

Marcadores, según `CLAUDE.md`: `[E]` establecido, `[R]` reportado por una o
pocas fuentes, `[H]` hipótesis nuestra, `[?]` incierto o fuentes en conflicto.
Todo lo que afirmamos del algoritmo sale del preprint de los autores, del código
cliente del servicio vivo, de la salida real de una corrida o del texto de ayuda
del binario; cuando sale de otro lado, lo decimos.

**Fecha del relevamiento:** 17 de octubre de 2026. **Herramientas ejecutadas:**
BLAST+ 2.17.0 local (Bioconda), ViennaRNA 2.7.2 local (complementaria, no es del
corpus) y **dsRNAEngineer, ejecutado de verdad** sobre una secuencia pública de
referencia del NCBI —proyecto `6fab2304bf273f5e`— sin subir una sola base de las
secuencias de EPILAB.

---

## Respuesta a la pregunta prioritaria (S2)

**El supuesto S2 queda cerrado, y con una precisión mayor que la que la ola 1
había conjeturado: ninguna de las dos herramientas del corpus calcula
termodinámica, y en la que sí diseña ARNdc el alineamiento ni siquiera es
alineamiento local con E-value, es coincidencia exacta de k-meros con presupuesto
de desapareamientos corrida con Bowtie.** La frase de las notas del equipo
—«BLAST separa en porciones y calcula la termodinámica»— mezcla tres cosas, no
dos, y la tercera es la que la ola 1 no podía ver sin el corpus.

**Primero, la evidencia de que no hay termodinámica en dsRNAEngineer.** El
preprint completo de la herramienta (`work/W2/dsRNAEngineer_preprint.pdf`, 22
páginas, descargado de bioRxiv por su DOI 10.1101/2024.07.22.604585) no contiene
*ninguna* ocurrencia de «thermodynamic», «free energy», «Gibbs», «Vienna»,
«fold», «melting», «Tm», «accessibility», «GC content» ni «asymmetry»: el conteo
es cero para cada término, hecho sobre el texto extraído completo
(`work/W2/dsRNAEngineer_preprint.txt`). Tampoco aparece «machine learning». Lo
que sí aparece cinco veces es «Dicer» y tres veces «mismatch» y «BLAST». El
catálogo de parámetros que el servicio expone hoy (`GET
/v1/api/info/option-list`, guardado en
`ejemplos/salidas/E8_dsrnaengineer_option-list.json`) tiene exactamente dos
campos numéricos por condición: `length` y `mismatch`. No hay energía, no hay
temperatura, no hay estructura secundaria. `[E]`

**Segundo, qué hace entonces para el tamizaje.** La sección de métodos del
preprint (página 10, líneas 154-160 de la numeración del propio documento)
describe el «Default Match Model» como *matching* secuencial del tamaño mayor de
ARN pequeño —«the size of dsRNA sliced by Dicer-2 is predefined in a
species-specific manner»— más dos tamaños adicionales: 16 pb con apareamiento
perfecto y 26 pb «almost perfect match with 0~2 mismatches». El servicio vivo lo
confirma y agrega el dato que el preprint no da: el texto de ayuda de la opción
«Custom Options», servido por su propia API, dice que lo que el usuario define
son «the length and mismatch parameters of **bowtie**»
(`ejemplos/salidas/E8_dsrnaengineer_option-list.json`, campo
`data.upload_option[0].desc[0]`). **Y la corrida real lo demuestra a nivel de
archivo:** el paquete de resultados que el propio servicio entrega
(`project/download-file`) contiene nueve archivos intermedios con nombre
`<especie>.<k>.bwt` —`dalbulus_maidis.16.bwt`, `dalbulus_maidis.21.bwt`,
`dalbulus_maidis.26.bwt`, `zea_mays_l.16/21/26.bwt`,
`apis_mellifera.16/22/26.bwt`— que son salidas de Bowtie, un archivo por especie
y por tamaño de ventana, con el formato tabular de Bowtie 1 reordenado
(`ejemplos/salidas/E8_dsrnaengineer_resultado/`). Es la prueba directa de que el
motor del tamizaje es un mapeador de lecturas cortas, no BLAST. `[E]`

**Tercero, dónde sí entra BLAST dentro de dsRNAEngineer.** En dos lugares, y
ninguno es el tamizaje de off-targets. Uno: en el módulo *screen-target*, para
buscar genes conservados entre especies de plaga, con «transcriptome level
pairwise BLAST» citando a Altschul 1990 (preprint página 8, líneas 127-129), con
cortes de identidad de secuencia y de largo del acierto que el usuario fija y una
recomendación de identidad ≥ 80 % tomada de la literatura (líneas 134-137). Dos:
en la construcción de la base, para anotar los ensamblados de novo contra la base
NR del NCBI (página 6, líneas 101-103). Además, el servicio vivo tiene una página
«Blast» independiente del flujo de diseño, que manda a `POST /v1/api/tools/blast`
con cuatro parámetros —`sequence`, `subject`, `evalue`, `num_align`— donde el
E-value se elige de una lista cerrada de cinco valores (1e-5 a 1e-1) y el número
de alineamientos viene en 20 por defecto
(`work/W2/chunks/Blast-1ffc05ce.js`). Es decir: **dentro de la misma
herramienta, BLAST sirve para elegir región conservada y para anotar; Bowtie
sirve para contar aciertos dentro y fuera del blanco.** La ola 1 acertó en
separar alineamiento de termodinámica, pero atribuyó el tamizaje de off-targets a
BLAST; en la herramienta real esa tarea es de Bowtie y BLAST hace la otra mitad
—la elección de región conservada— que la ola 1 también había anticipado. `[E]`

**Cuarto, qué calcula y qué no calcula BLAST, verificado en el binario.** El
texto de ayuda de `blastn` 2.17.0, guardado íntegro en
`ejemplos/salidas/blastn_help_2.17.0.txt`, lista en las líneas 95-182 los 48
especificadores del formato tabular: `pident`, `length`, `mismatch`, `gapopen`,
`evalue`, `bitscore`, `score`, `nident`, `btop`, coordenadas, taxonomía y
cobertura. **No hay un solo campo de energía libre, temperatura de fusión ni
accesibilidad.** Los parámetros por defecto, en las líneas 53-74 y 221-223:
`-task megablast`, `-evalue 10` (1000 para `blastn-short`), penalidad y premio de
nucleótido configurables, y filtro de baja complejidad `dust '20 64 1'` (`no`
para `blastn-short`). El puntaje de BLAST es estadístico —bit score y E-value de
Karlin-Altschul— y la única «física» que hay en el programa es la matriz de
premio/penalidad de nucleótidos, que es un modelo de sustitución, no de
hibridación. `[E]`

**Quinto, la única termodinámica que existe en el sitio del enlace del corpus, y
de dónde sale probablemente la confusión.** `https://blast.ncbi.nlm.nih.gov/`
aloja, además de los BLAST, un conjunto de herramientas especializadas, entre
ellas **Primer-BLAST**. Su página oficial
(`https://www.ncbi.nlm.nih.gov/tools/primer-blast/`, abierta el 17 de octubre de
2026) declara que combina Primer3 con BLAST y que «The default Table of
thermodynamic parameters is "SantaLucia 1998" and the default Salt correction
formula is "SantaLucia 1998"». Ahí sí hay termodinámica de hibridación: cálculo
de Tm de cebadores de PCR con el modelo de vecino más cercano y corrección por
sal. **Es la única de todo el sitio, y es para cebadores, no para ARNdc.** Nuestra
hipótesis `[H]` es que la frase «BLAST separa en porciones y calcula la
termodinámica» nace de haber visto Primer-BLAST: separa la plantilla en porciones
—los cebadores candidatos—, les calcula Tm y después los pasa por BLAST para ver
si son específicos. Es un pipeline que existe, se llama así, y cuelga del mismo
enlace que nos dio el organizador; sólo que resuelve otro problema.

**Sexto, para fijar el contraste con números reales.** Instalamos ViennaRNA
2.7.2 (no es del corpus; está acá sólo para mostrar qué cantidad produce la otra
familia de herramientas) y lo corrimos sobre la misma secuencia pública con la
que corrimos BLAST+: `RNAfold` devuelve para el ARNm de *eth* de *Dalbulus
maidis* (PZ371507.1, 615 nt) una energía libre mínima de **-186,90 kcal/mol**,
una energía libre del ensamble de **-198,17** y un centroide de **-159,50**, y
`RNAduplex` devuelve **-26,00 kcal/mol** para el dúplex de 21 nt entre una guía
antisentido y su sitio blanco (`ejemplos/salidas/E6_vienna_completo.txt`).
Verificamos además, corriendo el mismo cálculo con los dos juegos de parámetros
que trae la distribución, que **el juego por defecto es Turner 2004**: con
`-P rna_turner2004.par` da idéntico -186,90 y con `-P rna_turner1999.par` da
-202,90 (`ejemplos/salidas/E7_param_set.txt`), a 37 °C por defecto. Eso es una
cantidad física con unidades. Lo que BLAST devuelve para la misma secuencia es un
E-value de 1,66e-04 y un bit score de 32,2. **Son dos preguntas distintas, y el
corpus sólo trae herramientas para una de ellas.** `[E]`

La consecuencia de diseño, dicha sin vueltas: **en el corpus que nos dieron no
hay ninguna herramienta que estime eficacia.** Ni termodinámica, ni reglas de
secuencia, ni modelo entrenado. Las dos herramientas oficiales responden
«¿a qué más se parece esto?»; ninguna responde «¿esto va a silenciar?». Ese hueco
es el que define nuestro espacio de aporte y se desarrolla en la última sección.

---

## 1. dsRNAEngineer

### 1.1 Qué es, quién la hizo, versión, licencia, paper

dsRNAEngineer es un servicio web de diseño de ARNdc para control de plagas,
desarrollado por Yang Chen, Yufei Shi, Ziguo Wang, Xin An, Siyu Wei, Christos
Andronis, John Vontas, Jin-jun Wang y Jinzhi Niu, de la Southwest University de
Chongqing con participación del IMBB-FORTH y la Universidad Agrícola de Atenas
(preprint, página 1, líneas 5-14). El trabajo está financiado por el programa
nacional chino 2023YFC2607000 y por el proyecto europeo RATION (líneas 271-274).
`[R]`

El artículo que abrimos y usamos como fuente primaria es el **preprint de bioRxiv
de julio de 2024**, DOI 10.1101/2024.07.22.604585, descargado por Unpaywall en
`work/W2/dsRNAEngineer_preprint.pdf`. Existe una versión revisada por pares en
*Trends in Biotechnology* (2025) que **no abrimos**: aparece en la búsqueda web
como `S0167-7799(25)00002-2` en cell.com y como `S0167779925000022` en
ScienceDirect, ambas con muro de pago. No citamos nada de esa versión, y queda
anotado como pendiente: si la versión final cambió parámetros o agregó
validación, no lo sabemos. `[?]`

**Versión del servicio:** el preprint declara 942 transcriptomas al 5 de julio de
2024 (página 6, líneas 96-100). El servicio que corrimos hoy tiene **1.103
especies** en su lista completa, **808 seleccionables como on-target** y **1.104
como off-target** (`GET /v1/api/info/all-species-list` y
`/v1/api/info/species-list`). No hay número de versión ni changelog: lo único que
fecha el despliegue es el encabezado `Last-Modified: Sun, 01 Feb 2026 04:25:58
GMT` de su `index.html`. `[R]`

**Licencia: no declarada.** El preprint dice «It is free and open to all users
without login requirement» (líneas 266-267) y no menciona licencia, repositorio
de código ni disponibilidad del código fuente; las palabras «license», «code» y
«github» tienen cero ocurrencias en todo el documento. No hay código público:
sólo hay servicio. `[E]`

### 1.2 Cómo se corre, y la limitación que define todo lo demás

Corre **sólo como servicio web**. El front-end es Vue.js y el back-end Python con
Sanic (preprint, líneas 92-93), con la API en `https://dsrna-engineer.cn/v1/api`.
No hay binario, no hay contenedor, no hay forma de correrlo en nuestra máquina.
`[E]`

Eso tiene una consecuencia innegociable para este proyecto: **las secuencias de
EPILAB no se pueden analizar con esta herramienta.** Son material no publicado y
el procesamiento es del lado del servidor, en infraestructura de terceros, sin
política de retención de datos declarada y sin siquiera una cuenta que acote
quién ve qué. Dicho de otro modo: la herramienta que el organizador señala como
«de diseño y verificación de off targets» es exactamente la herramienta que no
podemos usar con el material que el mismo organizador nos dio. Esto no es un
tecnicismo; es el principal condicionante operativo de toda la ola 2 y hay que
decirlo en la presentación. `[H]` sobre la política de datos —no encontramos
ninguna—, `[E]` sobre el hecho de que el procesamiento es remoto.

Para igual poder reportar su comportamiento real, la corrimos con una **secuencia
pública de referencia del NCBI**: el ARNm de la hormona desencadenante de la muda
(*ecdysis triggering hormone*, `eth`) de *Dalbulus maidis*, accesión
**PZ371507.1**, 615 nt, que es material publicado y no coincide con ninguno de los
cuatro candidatos de la planilla de EPILAB.

Dos límites operativos más, leídos del código cliente: **un máximo de 10 especies
por análisis** para usuarios no administradores (`work/W2/chunks/Design-2e7b5b61.js`,
constante `ee=10`) y **archivos FASTA de hasta 1 MB** para secuencias propias
(misma fuente, regla `u[0].size<1024e3`). Diez especies por corrida es poco para
un panel de no objetivo serio; obliga a partir el análisis en varias corridas y a
juntar los resultados a mano. `[E]`

### 1.3 El pipeline interno, paso a paso

El preprint describe dos flujos (página 7, líneas 109-115). El primero arranca de
especies de plaga elegidas por el usuario, corre *screen-target* y sigue con
on-/off-target y multi-target; el segundo arranca del gen blanco que trae el
usuario y salta directo al análisis on-/off-target. Nosotros corrimos el segundo.

Paso a paso, con lo que verificamos de la corrida real:

El usuario entrega la secuencia blanco en FASTA. La interfaz recomienda, en un
*tooltip* que sólo se ve en el código,
«remove the 5' cap structure (Cap), the untranslated region (UTR), and the
poly(A) tail» (`work/W2/chunks/Design-2e7b5b61.js`); es la única recomendación
biológica de diseño que la herramienta da, y coincide con lo que la literatura de
insectos reporta sobre apuntar al marco de lectura y no a los UTR. `[R]`

El servicio **parte la secuencia en ventanas deslizantes** de los tamaños del
modelo de coincidencia. Lo verificamos en la salida real: el nombre de consulta
en los archivos Bowtie es `PZ371507_1_sliding` y cada línea trae las coordenadas
de inicio y fin de la ventana. Para cada especie seleccionada corre el
alineamiento de esas ventanas contra el transcriptoma de esa especie, con el
tamaño mayor y los dos adicionales, y **cuenta** los aciertos.

El conteo que reporta es una **suma sin ponderar de los aciertos de las tres
condiciones**. Lo comprobamos aritméticamente contra los archivos crudos de la
corrida: para *D. maidis* el servicio informó «237 on-targets» y los archivos
tienen 190 líneas en `dalbulus_maidis.21.bwt` más 47 en
`dalbulus_maidis.16.bwt` más 0 en `dalbulus_maidis.26.bwt`, y 190 + 47 = 237.
Para *Zea mays* informó «70 off-targets» y hay 70 líneas en `zea_mays_l.16.bwt`,
0 en el de 21 y 0 en el de 26. Para *Apis mellifera* informó «67 off-targets» y
hay 67 en `apis_mellifera.16.bwt`, 0 en el de 22 y 0 en el de 26. `[E]`

Después, sobre el perfil posicional de esos conteos, hace una **ventana
deslizante exhaustiva** por tamaño de fragmento de ARNdc —de 50-100 pb hasta
650-700 pb en incrementos de 50— y recomienda los diez mejores fragmentos por
intervalo de tamaño (preprint, página 11, líneas 171-175, y figura suplementaria
2, líneas 364-367: la ventana arranca en 50 pb, barre todo el gen, pasa a 51 pb,
y así hasta 100; cada ventana produce una secuencia óptima y todas se reordenan
para quedarse con las diez primeras). Nuestra corrida devolvió exactamente diez
fragmentos, de largos 51, 61, 71, 81 y 91 pb, dos por largo
(`ejemplos/salidas/E8_match_result.json`).

Finalmente, el módulo *multi-target* concatena fragmentos de distintos genes y
**optimiza el orden de concatenación recalculando los mismos conteos** (preprint,
página 13, líneas 195-199).

### 1.4 Parámetros, umbrales y qué pasa si se mueven

Los valores por defecto, leídos del almacén de estado del cliente
(`work/W2/chunks/Design-2e7b5b61.js`, `selectedOption:888, custom_length1:21,
custom_length2:0, custom_mismatch2:0, custom_length3:0, custom_mismatch3:0`) y
del catálogo de la API:

| Modelo | Condición mayor | Condiciones adicionales |
| --- | --- | --- |
| Model I (`match_id` 1) | 21 pb, apareamiento perfecto | 16 pb perfecto · 26 pb con ≤ 2 desapareamientos |
| Model II (`match_id` 2) | 22 pb, apareamiento perfecto | iguales |
| Model III (`match_id` 3) | 20 pb, apareamiento perfecto | iguales |
| Custom (`match_id` 999) | 20, 21 o 22 pb perfecto | dos condiciones libres, 14-27 pb, 0-2 desapareamientos |

El modelo se asigna **por especie**, no lo elige el usuario salvo en modo
personalizado. *Dalbulus maidis* tiene asignado el **Model I** (21 pb) y *Zea
mays* también; *Apis mellifera* tiene el **Model II** (22 pb)
(`ejemplos/salidas/E8_dsrnaengineer_especies_clave.csv`). Acá hay un hueco que
conviene marcar fuerte: **el preprint dice que el tamaño es específico de especie
porque depende de Dicer-2, pero no cita ninguna fuente para la asignación de cada
especie, y el servicio tampoco la expone.** Y la asignación no sigue la
filogenia: dentro de Hemiptera, *D. maidis* (Cicadellidae) está en Model I y
*Peregrinus maidis* (Delphacidae) en Model II. De dónde sale ese 21 para nuestra
especie blanco es, hoy, desconocido. `[?]`

**Qué pasa si se mueven.** El resultado más importante de nuestra corrida es
cuánto depende el conteo del tamaño de ventana: de los 70 off-targets en maíz,
**los 70 vienen de la condición de 16 pb** y ninguno de la de 21; lo mismo en
abeja, 67 de 67 desde la condición de 16 pb. Es decir, **el número que la
herramienta muestra como riesgo de off-target está dominado por una condición
que no corresponde al tamaño de siRNA que la propia herramienta considera
mecanísticamente relevante.** Bajar la condición adicional de 16 a 14 pb —el
mínimo que el modo personalizado permite— sólo puede aumentar ese número; subirla
a 19 o 20 lo acercaría al conteo de la condición mayor, que en nuestro caso fue
cero. No hay en la documentación ninguna justificación empírica del 16, más allá
de la cita general a que ARN pequeños de 16 a 26 pb pueden disparar algún nivel
de silenciamiento (preprint, líneas 69-70, con cinco referencias). `[E]` el
hallazgo numérico, `[?]` la justificación del umbral.

### 1.5 Qué tipo de optimización es y qué función objetivo maximiza

Es **búsqueda exhaustiva con ranking multicriterio implícito**. No hay nada
entrenado, no hay heurística de búsqueda, no hay gradiente: la ventana
deslizante recorre todas las posiciones para cada tamaño de fragmento, y el
único criterio de ordenamiento son los conteos de aciertos dentro y fuera del
blanco. El preprint declara que el usuario elige la prioridad —«priority to pest
control: on-target, or priority to biosafety: off-target»— al seleccionar los
fragmentos candidatos (líneas 170-172). `[R]`

**La función objetivo explícita no está expuesta.** La tabla de resultados que
devuelve la API trae por fragmento sólo `section_length`, `position`,
`match_times`, `target_gene` y `off_target_gene` con sus conteos, y **ningún
campo de puntaje** (`ejemplos/salidas/E8_match_result.json`). Buscamos el control
de prioridad en el código cliente desplegado y no lo encontramos. Así que el peso
relativo entre on-target y off-target con el que se ordenan esos diez fragmentos
es, desde afuera, una caja negra. `[?]`

Un detalle que ilustra el punto: en nuestra corrida, el fragmento que la
herramienta puso primero está en la posición 95 y tiene **1 on-target**, mientras
que el de la posición 223 tiene **31 on-targets** y quedó tercero. Si el criterio
fuera maximizar on-target, el orden sería otro. Si fuera minimizar off-target,
los dos tienen 1. Con la información que la API devuelve no se puede reconstruir
el orden. `[?]`

### 1.6 Formatos de entrada y salida, con el ejemplo real

**Entrada.** Texto FASTA pegado en el formulario, o archivo `.fa/.fasta/.fna` de
hasta 1 MB. El cuerpo real del pedido que mandamos a `POST /v1/api/project/design`
—reconstruido leyendo el cliente— es un JSON con `uid` (un entero decimal de
época en milisegundos más un dígito aleatorio, generado en el navegador),
`name`, `sequence`, `conserved_list`, `off_target_list`, `email` y `parent_id`.
Cada elemento de las dos listas de especies lleva `species_id`, `species`,
`upload_file`, `match_id`, `match_name`, `match_length`, `match_mismatch`,
`match_desc` y `option`. El pedido completo, tal como se envió, está en
`ejemplos/salidas/E8_dsrnaengineer_request.json`. Dato operativo verificado por
error: con un `uid` en formato UUID el servidor responde **500**; con el formato
numérico que genera su propio cliente, responde `code 0` y devuelve el
`project_id`. `[E]`

**Salida.** Tres capas. La API de detalle devuelve el resumen con los conteos por
especie («Dalbulus maidis (Model I, 237 on-targets)», «Zea mays (Model I, 70
off-targets)», «Apis mellifera (Model II, 67 off-targets)»); la API de
`match-result` devuelve la tabla de diez fragmentos candidatos; y
`project/download-file` entrega un `.tar.gz` —5.323 bytes en nuestro caso— con el
FASTA de entrada y los nueve archivos `.bwt` crudos. El formato de esos archivos,
descrito por observación nuestra porque no está documentado: nueve columnas
separadas por tabulación —nombre de la consulta, inicio y fin de la ventana en la
consulta (1-based, inclusive), hebra, identificador del transcripto blanco,
desplazamiento en el blanco, secuencia alineada, cadena de calidades ficticias
`IIII...` y un entero final—. Verificamos las **374 líneas** de los cuatro
archivos no vacíos: las 374 son coincidencias exactas de la ventana
correspondiente (0 desapareamientos), con las coordenadas interpretadas como
1-based inclusivas.

**Y la novena columna, que quedaba pendiente, es el campo 7 de Bowtie 1 —«otras
instancias»— y no el de desapareamientos.** Lo determinamos de tres maneras
convergentes, registradas en `ejemplos/salidas/E9_bowtie_formato_columnas.txt`.
Primero, el manual de Bowtie 1 describe una salida por defecto de ocho campos en
la que el séptimo es el número de otras instancias en las que la misma secuencia
alineó contra los mismos caracteres de la referencia —y advierte explícitamente
que *no* es el número de otros lugares donde la lectura alinea— mientras que el
octavo es la lista de descriptores de desapareamiento. Segundo, lo reprodujimos:
instalamos Bowtie 1.3.1 y corrimos las mismas ventanas de 16 nt contra nuestra
base de demostración; con `-v 0` el séptimo campo es un entero y el octavo queda
vacío, y con `-v 2` el octavo aparece con cadenas del tipo `2:G>C,4:T>C`,
mientras el séptimo sigue siendo un entero independiente. **El desapareamiento
en Bowtie nunca se reporta como un entero suelto: se reporta como descriptor de
posición y base.** Tercero, los archivos del servicio tienen exactamente nueve
columnas en las 374 líneas, nunca diez, de modo que no hay campo de descriptores;
y su columna final llega a 9 en `zea_mays_l.16.bwt`, a 7 en
`apis_mellifera.16.bwt` y a 3 en `dalbulus_maidis.16.bwt`, valores imposibles
para un conteo de desapareamientos bajo una condición que la propia herramienta
define como apareamiento perfecto. Las nueve columnas del servicio son, entonces,
el campo 1 de Bowtie partido en tres —nombre, inicio y fin de la ventana— seguido
de los campos 2 a 7. `[E]`

La afirmación de que los 374 aciertos no tienen desapareamientos, de todos modos,
no descansaba en esa columna: descansa en haber comparado cada secuencia
reportada contra la ventana correspondiente de la consulta, y las 374 son
idénticas. La resolución de la columna confirma esa lectura en vez de
corregirla, y **los conteos de off-target de la sección 1.3 no cambian**.

### 1.7 Qué base de datos consulta, cómo se arma y a quién cubre

Esto es lo que decide la calidad del tamizaje, y es a la vez lo mejor y lo más
frágil de la herramienta.

**Cómo se arma.** De las especies listadas hoy, 443 traen un identificador RefSeq
`GCF_` en el nombre, **577 traen una accesión de corrida del SRA** (`SRR`/`ERR`),
49 son secuencias individuales del NCBI (virus, con `NC_`/`MZ`/`MK`) y 34 no
traen identificador (`ejemplos/salidas/E8_dsrnaengineer_fuente_de_los_transcriptomas.csv`).
Las que vienen del SRA son ensamblados de novo hechos por los autores: control de
calidad con fastp, ensamblado con Trinity y anotación por BLAST contra NR
(preprint, líneas 101-103). Es decir, **más de la mitad del panel no es un
transcriptoma de referencia sino un ensamblado propio a partir de una única
corrida pública.** `[E]`

**A quién cubre.** El árbol de categorías del servicio
(`ejemplos/salidas/E8_dsrnaengineer_categorias_especies.csv`) tiene dos raíces.
En on-target: Blattaria 105, Coleoptera 84, Diptera 122, **Hemiptera 127**,
Hymenoptera 27, Lepidoptera 126, Orthoptera 25, Thysanoptera 9, ácaros 20,
nematodos 13, hongos fitopatógenos 54, malezas 46 y virus 49. En off-target:
ecosistemas acuáticos 36, aves 16, **polinizadores 27**, gusano de seda 1,
artrópodos no blanco 97, lombrices 1, **plantas de cultivo 94**, mamíferos 12,
hongos de biocontrol 4 y animales de granja 8. Para nuestro problema, la cobertura
es buena donde más importa y mala donde más duele:

Está *Dalbulus maidis*, con `species_id` 1312, y **es seleccionable como
on-target** —es el hallazgo que más cambia el plan de la ola 1—. Está *Zea mays*
con el mismo ensamblado RefSeq `GCF_902167145.1` que R2 había identificado, y
*Apis mellifera* con `GCF_003254395.2`, también el mismo. Están los dos
cicadélidos no objetivo con anotación RefSeq que R2 propuso como panel mínimo,
*Homalodisca vitripennis* y *Macrosteles quadrilineatus*, y además *Peregrinus
maidis*, *Nephotettix cincticeps* y *Diaphorina citri*. `[E]`

**Lo que no está:** el virus **MRFV no figura entre los 49 virus del listado**
—sí están *Maize dwarf mosaic virus*, *Maize chlorotic mottle virus* y *Maize
rough dwarf virus*—, y no hay ninguna entrada de *Spiroplasma* ni de
*Phytoplasma*. Dos de los cuatro candidatos de EPILAB apuntan a MRFV: para esos,
el análisis on-target en esta herramienta requeriría subir el genoma del virus
como archivo propio, lo que el modo personalizado permite pero que vuelve a
chocar con la restricción de no subir material. La ausencia de mollicutes es
coherente con lo que la ola 1 predijo y W5 confirmó: no hay candidatos contra
fitoplasma ni espiroplasma porque no hay maquinaria de RNAi en esos organismos.
`[E]`

**Y el problema de fondo del transcriptoma de *D. maidis*, cuantificado.** Su
entrada en el servicio es `Dalbulus maidis (Maize leafhopper) SRR15166998`: un
ensamblado de novo de una sola corrida pública. En nuestra corrida, los 190
aciertos perfectos de 21 nt del ARNm público de *eth* cayeron **todos en un único
contig**, `TRINITY_DN64958_c0_g1_i1`, cubriendo un tramo contiguo de las
posiciones **215 a 424** del ARNm de 615 nt. Fuera de ese tramo de 210 nt, la
herramienta informa **cero on-targets** para un transcripto que sabemos que
existe en la especie y que fue publicado. Un equipo que diseñara contra el tercio
5' de ese gen leería «sin aciertos en el blanco» y concluiría lo contrario de lo
que corresponde. **El conteo de on-target de dsRNAEngineer para *D. maidis* es,
en realidad, una medida de cobertura del ensamblado, no de identidad del
blanco.** `[E]`

### 1.8 Limitaciones

Las que declaran los autores son pocas y suaves: el preprint sólo menciona que
los transcriptomas se actualizan con pedidos de usuarios y que se irán agregando
más (líneas 104-107), y cierra afirmando que la herramienta «can be confidently
used» y «provides a reliable reference for assessing the safety of RNAi-based
pest control» (líneas 242-244). No hay sección de limitaciones. Su validación son
dos casos: *screen-target* recuperando β-actina en el puesto 123 de 447 genes con
corte de identidad ≥ 97 % y largo ≥ 300 pb entre cuatro ácaros (líneas 220-223),
y *off-target* sobre dos productos registrados, MON87411 y Ledprona, contra 84
especies no objetivo, con conteos de 2 a 134 y de 0 a 222 off-targets
respectivamente (líneas 232-241). **Ninguna de las dos es una validación de que
los off-targets predichos ocurran: son demostraciones de que el programa
corre y devuelve números plausibles.** `[E]`

Las que deducimos del código y de la corrida, que son las que importan: el
conteo suma sin ponderar condiciones de plausibilidad mecánica muy distinta y en
la práctica queda dominado por la de 16 pb; el conteo mezcla número de ventanas
riesgosas con número de parálogos alcanzados —en maíz, 70 aciertos sobre sólo 28
posiciones distintas de la consulta repartidas en 60 transcriptos; en abeja, 67
sobre 22 posiciones y 39 transcriptos—; la calidad del on-target depende de un
ensamblado de novo cuya cobertura no se informa; el tamaño de siRNA por especie
no tiene fuente; el criterio de ordenamiento final no se expone; el tope de diez
especies por corrida obliga a fragmentar el panel; y no hay forma de correr nada
de esto sobre material no publicado. `[E]` los hechos, `[H]` la lectura de que
en conjunto vuelven el número de off-target poco informativo como medida de
riesgo.

---

## 2. NCBI BLAST, web y local

### 2.1 Qué es y qué calcula exactamente

El segundo enlace del corpus apunta a `https://blast.ncbi.nlm.nih.gov/Blast.cgi`,
la portada del servicio de BLAST del NCBI. BLAST no es una herramienta de diseño
de ARNdc: es una heurística de búsqueda de similitud de secuencias que devuelve
alineamientos locales con un puntaje y una significancia estadística. Para el
problema que nos ocupa sirve para dos cosas —ver a qué más se parece una
secuencia, y encontrar regiones conservadas entre organismos— y no sirve para
ninguna otra.

Lo verificado en el binario, que es lo que pide el prompt en vez de describir por
la documentación: `blastn` 2.17.0 expone 48 especificadores de salida tabular y
ninguno es termodinámico (`ejemplos/salidas/blastn_help_2.17.0.txt`, líneas
95-182); los valores por defecto relevantes son `-task megablast`, `-evalue 10`
—1000 para `blastn-short`— y `-dust '20 64 1'`, `no` para `blastn-short` (líneas
53-74 y 221-223). El propio texto de ayuda define `word_size` como «length of
best perfect match» (línea 66-67), que es la semilla del esquema de semilla y
extensión. `[E]`

### 2.2 El servicio web, sus valores por defecto y por qué no nos sirve

Del formulario vivo de `blastn` del 17 de octubre de 2026
(`work/W2/blastn_web.html`, atributos `defVal`/`selected` del HTML) salen los
valores por defecto del servicio: programa **Megablast** marcado por defecto,
**word size 28**, **match/mismatch 1,-2**, **Expect 0.05** —no 10, como en la
línea de comandos— y **100 secuencias alineadas** como máximo. Y hay una casilla
marcada por defecto, «Short queries: Automatically adjust parameters for short
input sequences», cuya ayuda dice que ajusta automáticamente el tamaño de palabra
y otros parámetros. `[E]`

Esa casilla es justamente el problema de usar el BLAST web para tamizaje de
ventanas de 21 nt: **el servidor cambia los parámetros por su cuenta y no informa
cuáles usó**, de modo que el resultado no es reproducible desde el registro de lo
que uno pidió. Sumado a que las secuencias de EPILAB no se suben a servicios de
terceros, la conclusión es simple: **el BLAST web queda para consultas
exploratorias sobre material público, y todo el tamizaje serio va con BLAST+
local.** `[H]`

### 2.3 BLAST+ local: instalación y corridas reales

Instalamos BLAST+ **2.17.0+** (build del 22 de agosto de 2026) desde Bioconda en
un entorno conda propio del proyecto, junto con ViennaRNA 2.7.2; sin `sudo` y sin
tocar el gestor del sistema. El script reproducible de todas las corridas es
`ejemplos/corrida_blast_local.sh` y las salidas están en `ejemplos/salidas/`.

Las entradas son públicas: el ARNm de *eth* de *D. maidis* (PZ371507.1, 615 nt) y
el de bursicón α (PZ371508.1, 468 nt) —los dos únicos registros que devuelve
`Dalbulus maidis[Organism] AND biomol_mrna[PROP]` en el NCBI, y que por nombre de gen
y voucher parecen ser los del paper P3 del corpus, que no abrimos en esta ola `[?]`—,
el genoma de referencia de MRFV (NC_002786.2, 6.366 nt), y una base de
demostración de 81 secuencias y 138.269 bases hecha con 40 ARNm RefSeq de *Zea
mays*, 40 de *Apis mellifera* y el genoma de MRFV. **La base es de demostración y
no sirve para tamizar nada en serio:** el maíz tiene 57.091 ARNm RefSeq, de los
que bajamos 40. Está puesta para mostrar el comportamiento de los parámetros, no
para medir riesgo.

El tamizaje del lado del blanco funciona como se espera: las 595 ventanas de 21
nt del ARNm de *eth* contra una base que contiene ese mismo ARNm dan **595
aciertos perfectos, todos de 21/21 y todos contra PZ371507.1**, cero contra
bursicón α (`ejemplos/salidas/E5_21mers_ontarget.tsv`). Del lado del no blanco,
contra la base de demostración, las 595 ventanas de 21 nt dan **cero aciertos**
con la condición mayor, y la de 16 nt da **un acierto**: la ventana 550-565 de
*eth* coincide perfecto, en hebra menos, con el ARNm `NM_001346803.1` de *Zea
mays* («uncharacterized LOC103654892»), con E-value 1,66e-04 y bit score 32,2
(`ejemplos/salidas/E3_16mers_perfect.tsv`). Es el mismo fenómeno que dominó la
corrida del servicio: el riesgo que se reporta viene de la condición de 16 nt.

### 2.4 El error que hay que no cometer, cuantificado

Hay una trampa en usar BLAST para este tipo de tamizaje que conviene dejar
escrita con números, porque es la razón de ingeniería por la que el campo usa
Bowtie.

**`-perc_identity` no es un filtro de identidad sobre la consulta completa: es
sobre el alineamiento que BLAST encontró.** Corrimos las 590 ventanas de 26 nt
pidiendo `-perc_identity 92` —que es lo que daría 24 de 26 identidades, es decir
el «26 pb con ≤ 2 desapareamientos» de dsRNAEngineer— y BLAST devolvió **827
filas**. De esas 827, **cero** son alineamientos de 26 nt con ≤ 2
desapareamientos: los largos de alineamiento son 11 nt (617 filas), 12 (104), 13
(38), 14 (43), 15 (14) y 16 (11). Lo mismo con las ventanas de 21 nt y
`-word_size 11 -perc_identity 100`: 578 filas, todas de entre 11 y 16 nt de
alineamiento. Con `-word_size 21` la misma consulta da **0 filas**, y con el
`megablast` por defecto —tamaño de palabra 28, mayor que la consulta— también
**0** (`ejemplos/salidas/E4_sensibilidad_umbrales.tsv`). `[E]`

Dicho de otro modo: con BLAST hay que **postfiltrar por `length` y `mismatch`**, o
fijar `-word_size` igual al largo de la ventana y `-ungapped`, para que el
resultado signifique lo que uno cree que significa. Un conteo de líneas de
salida de BLAST interpretado como «cantidad de off-targets» sobreestima el riesgo
por un factor de cientos. Esto no es un defecto de BLAST: es que su pregunta es
otra. Bowtie, que alinea la lectura entera con un presupuesto de desapareamientos
fijo, responde la pregunta correcta sin postfiltro, y por eso lo eligen
dsRNAEngineer, si-Fi21 y dsRIP. `[H]` la conclusión, `[E]` los conteos.

---

## 3. Lo que corrimos y lo que no

| Herramienta | ¿Corre local? | ¿Ejecutada? | Qué se corrió |
| --- | --- | --- | --- |
| BLAST+ 2.17.0 (blastn, makeblastdb, blastdbcmd) | sí | **sí** | 7 corridas: base de datos, megablast del ARNm completo, tamizaje de 16/21/26-meros, barrido de umbrales, tamizaje on-target |
| dsRNAEngineer (servicio web) | no | **sí, con secuencia pública** | proyecto `6fab2304bf273f5e`: 1 gen, 1 especie on-target, 2 off-target; resultados y archivos Bowtie crudos descargados |
| NCBI BLAST web (`Blast.cgi`) | no | **no** | no se envió ninguna consulta al servidor; sólo se leyeron el formulario y la documentación oficial. Motivo: todo lo que necesitábamos medir se mide mejor con BLAST+ local, y no corresponde mandar material propio |
| Primer-BLAST | no | **no** | fuera del problema: calcula Tm de cebadores de PCR. Sólo se leyó su documentación oficial para responder S2 |
| ViennaRNA 2.7.2 (RNAfold, RNAduplex) | sí | **sí** | complementaria, no es del corpus: para mostrar qué cantidad produce la familia termodinámica |

---

## 4. Dónde se puede enganchar un aporte nuestro

Esta es la sección que importa y la escribimos con la corrida real en la mano, no
con deseos. Los enganches están ordenados por relación entre valor y costo, y los
dos primeros son consecuencia directa de números que medimos hoy.

**1. El conteo de off-target está dominado por la condición menos plausible, y
rebalancearlo es barato.** En nuestra corrida, 70 de 70 off-targets en maíz y 67
de 67 en abeja vienen de la condición de 16 pb; cero de la condición de 21 o 22
pb que la propia herramienta considera el tamaño de corte de Dicer-2. Hoy el
número que se le muestra al usuario es una suma sin pesos. Un índice que separe
—y pondere— aciertos por condición, y que además pondere por consecuencia del gen
alcanzado como hace dsRIP con su razón 20:1 para ortólogos de genes esenciales —dato tomado de nuestros propios reportes R2 y R4, que sí abrieron ese trabajo; en esta ola no lo volvimos a abrir—,
se calcula sobre exactamente los mismos archivos `.bwt` que el servicio ya
entrega. **Esto es reponderar una salida existente, no construir un pipeline
nuevo, y cambia la conclusión de seguridad de un candidato.** `[H]`

**2. El conteo mezcla «cuántas ventanas son riesgosas» con «a cuántos parálogos
llegan», y separarlo es trivial y cambia la decisión.** Los 70 aciertos en maíz
son 28 posiciones distintas de la consulta repartidas en 60 transcriptos. No es
lo mismo un ARNdc con 28 ventanas malas que uno con 2 ventanas que pegan en 35
parálogos cada una: el primero no tiene región segura, el segundo sí, y basta con
recortar. Un perfil posicional de riesgo —riesgo por ventana en vez de total por
especie— sale del mismo archivo y es lo que permite decir *dónde* recortar.
`[H]`

**3. Falta por completo el eslabón de eficacia, y ése es el hueco grande.**
Ninguna de las dos herramientas del corpus estima si un fragmento va a silenciar:
dsRNAEngineer no calcula termodinámica ni tiene modelo entrenado, y BLAST menos.
El único conjunto de coeficientes calibrado con bioensayos de insecto es el de
dsRIP, con sus cuatro variables de secuencia (según R2 y R4 de la ola 1, que abrieron
ese trabajo; acá no lo reabrimos). Hoy, pasar de «fragmento con menos
off-targets» a «fragmento que además tiene chance de funcionar» se hace a mano o
no se hace. **Unir las dos señales en una sola salida ordenada, con el vector de
términos sin colapsar, es la junta que falta entre dos herramientas existentes**,
y es exactamente la propuesta que R2 ya había especificado; la novedad de esta ola
es que ahora sabemos que el lado de la especificidad no hay que construirlo, hay
que leerlo bien. `[H]`

**4. Hay un bloqueo de confidencialidad que sólo se resuelve con una
reimplementación local del criterio, y eso nos toca a nosotros.** Las secuencias
de EPILAB no pueden ir a dsRNAEngineer. Pero su criterio de coincidencia está
completamente especificado —tamaño mayor por especie, 16 pb perfecto, 26 pb con
hasta 2 desapareamientos, Bowtie— y es reproducible con `bowtie` o con `blastn`
más el postfiltro que la sección 2.4 muestra que hace falta. **No es innovación:
es una condición necesaria para poder analizar el material del corpus.** Conviene
presentarlo como lo que es, un puente, y no como un aporte metodológico. `[H]`

**5. El umbral de 16 pb y el tamaño de siRNA por especie son números sin
respaldo, y una prueba de sensibilidad es un resultado publicable en el contexto
del Investigathón.** No encontramos fuente para que *D. maidis* esté asignado al
Model I de 21 pb mientras *Peregrinus maidis*, también Hemiptera, está en el
Model II de 22 pb. Nuestra tabla `E4_sensibilidad_umbrales.tsv` es la versión
mínima del experimento: muestra que el número de aciertos cambia en órdenes de
magnitud con el tamaño de palabra. La versión seria es rehacer el ranking de un
conjunto de candidatos variando *k* y reportar cuántos pares de candidatos
cambian de orden. Es barato, es auditable y ataca la pregunta que el organizador
declara abierta —cuáles merecen validación y por qué—. `[H]`

**6. El on-target de *D. maidis* mide cobertura de ensamblado, no identidad de
blanco, y eso sí que no se arregla desde afuera.** Los 190 aciertos de nuestra
corrida caen en un único contig que cubre 210 de los 615 nt del transcripto. Un
transcriptoma de referencia propio de la especie —la tarea del camino crítico que
R2 identificó y que W4 tiene entre manos— no es un lujo: es lo que hace que el
conteo on-target signifique algo. Es, además, el único de estos seis puntos que
requiere trabajo de datos pesado. `[E]` el hallazgo, `[H]` la prioridad.

**Y lo que no conviene construir, dicho con la misma franqueza.** El panel de
especies de dsRNAEngineer —1.103 especies, con maíz, abeja, lombriz, hongos de
biocontrol, 97 artrópodos no blanco y tres cicadélidos no objetivo— es mejor que
cualquier cosa que cuatro personas curen en una semana, y su mera existencia
contesta la pregunta de «contra qué comparar». La ventana deslizante exhaustiva
ya es óptima para el espacio de búsqueda: no hay nada que una metaheurística
agregue sobre enumerar todas las subcadenas de un transcripto. Y la optimización
del orden de concatenación en ARNdc multiblanco ya está hecha. Reimplementar
cualquiera de esas tres cosas sería trabajo perdido.

---

## 5. Contradicciones y correcciones respecto de la ola 1

Tres, y conviene anotarlas con precisión porque dos de ellas corrigen a nuestro
propio equipo.

**El supuesto S2 se confirma en su parte central y se corrige en el reparto de
tareas.** La ola 1 propuso que BLAST y Bowtie sirven «sobre todo para tamizaje de
off-targets y para elegir regiones conservadas». En la herramienta real del
corpus, esas dos funciones están repartidas entre dos programas distintos: BLAST
elige regiones conservadas —módulo *screen-target*, con corte de identidad ≥ 80 %—
y Bowtie hace el tamizaje de off-targets, con coincidencia exacta y presupuesto de
desapareamientos. La idea de fondo de la ola 1 era correcta; la atribución, no del
todo.

**La ola 1 dio por inexistente un transcriptoma de *D. maidis* que el corpus sí
alcanza.** R2 afirmó, con razón sobre los ensamblados genómicos, que no hay
anotación génica pública de la especie y que el conjunto de transcriptos hay que
construirlo. dsRNAEngineer tiene uno, armado por los autores desde la corrida
`SRR15166998` con Trinity y anotado contra NR. Eso no invalida la tarea de W4 por
dos razones que medimos: el ensamblado es parcial —cubre 210 de 615 nt de un
transcripto publicado— y **no es descargable**, sólo consultable a través del
servicio, que es justo donde no podemos mandar nuestras secuencias. La corrección
es de matiz pero importa: el recurso existe, es insuficiente y es inaccesible
localmente. `[E]`

**La ola 1 subestimó cuán simple es el estado del arte que nos dieron.** R2 y R4
dedicaron páginas a modelos fundacionales, atención y predicción de eficacia. La
herramienta que el organizador entrega como «de diseño y verificación de
off targets» no tiene nada de eso: cuenta coincidencias exactas de k-meros y las
suma. Eso baja la vara de lo que hay que superar y, sobre todo, cambia el eje: el
aporte no está en modelar mejor, está en **decidir mejor con lo que ya se
calcula**.

---

## 6. Vacíos documentados y preguntas para el investigador

No pudimos abrir la versión revisada por pares de dsRNAEngineer en *Trends in
Biotechnology* (muro de pago): si cambió parámetros, no lo sabemos `[?]`. No
encontramos fuente para la asignación del tamaño de siRNA por especie `[?]`. No
pudimos reconstruir el criterio de ordenamiento de los diez fragmentos que
recomienda la herramienta, porque la API no devuelve puntaje `[?]`. No
hay licencia declarada ni código público de dsRNAEngineer `[E]`. Y no evaluamos
el módulo *screen-target* con una corrida propia: habría requerido elegir
especies de plaga y gastar una corrida más del servicio, y la pregunta prioritaria
no lo necesitaba.

Para el investigador del EPILAB, tres preguntas que salen de este análisis y que
sólo él puede contestar. La primera: **¿con qué herramienta y con qué criterio se
llenó la columna «Nro de eficientes por gen» de la planilla?** dsRNAEngineer no
clasifica siRNA como eficientes: cuenta aciertos dentro y fuera del blanco. Si el
número saliera de ahí, para un transcripto bien representado debería acercarse al
total de ventanas, y no lo hace. Así que esa columna viene de otro lado, y saber
de dónde cambia cómo hay que leer los cuatro candidatos. La segunda: **¿el tamaño
de siRNA de 21 nt para *D. maidis* está medido o es el valor por defecto del
grupo?** Hay secuenciación de ARN pequeños publicada para otros cicadélidos, pero
para esta especie no la encontramos. La tercera: **¿con qué transcriptoma de
*D. maidis* trabaja el laboratorio?** Si tienen uno propio y más completo que el
ensamblado de una corrida que usa dsRNAEngineer, el conteo on-target de la
herramienta subestima sistemáticamente y conviene saberlo antes de usarla para
decidir.

---

## Nota de método

Todo lo que este reporte afirma sobre algoritmos sale de cuatro clases de fuente,
y cada afirmación dice de cuál: el preprint de los autores, citado por página y
por la línea impresa en el propio PDF; el código cliente del servicio desplegado,
citado por archivo descargado en `work/W2/chunks/`; la salida real de una corrida
nuestra, citada por archivo en `ejemplos/salidas/`; y el texto de ayuda del
binario instalado o la página oficial del NCBI, citados por archivo y línea.
Donde no hubo ninguna de las cuatro, dijimos que no sabemos. Los archivos
originales del corpus no se modificaron; la única copia que hicimos es la del
`.docx` de enlaces, en `work/W2/`, para verificar los hipervínculos. Ninguna
secuencia de EPILAB salió de esta máquina.
