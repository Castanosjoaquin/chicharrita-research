# W3 — Las bases de datos del corpus: qué contienen, cómo se consultan y qué nos falta

Investigación de la ola 2 sobre la sección 3 del manifiesto
(`research/ola2/MANIFEST.md`): los enlaces a bases de datos del documento
`YHat-Biotech/Links de interes.docx`. Corrida del 17 de octubre de 2026. Todas
las consultas que se citan acá se ejecutaron: el registro completo, con código
HTTP, tamaño de respuesta y marca de tiempo de las 409 peticiones, está en
`consultas/registro_consultas.csv`, y los ejemplos trabajados, en los ocho
archivos numerados de `consultas/`.

---

## 1. El insumo, verificado de nuevo

El `.docx` se descomprimió y se leyó su `word/document.xml` y su
`word/_rels/document.xml.rels` sobre una copia en `work/W3/`, sin tocar el
original. Tiene siete párrafos, tres rótulos en negrita y cuatro hipervínculos
cuyo destino real (`Target` en el archivo de relaciones) coincide exactamente con
el texto visible, de modo que no hay ningún enlace enmascarado. No trae
credenciales, ni instrucciones, ni fecha, ni autor en los metadatos. [E]

Los dos enlaces que le tocan a W3 son
`https://www.ncbi.nlm.nih.gov/` bajo el rótulo «Database general de genes» y
`https://www.ncbi.nlm.nih.gov/datasets/genome/` bajo «Genomas y transcriptomas
disponibles». Los dos responden HTTP 200 hoy (`consultas/08_enlaces_versiones_licencia.md`). [E]

**El titular de este reporte es que esos dos enlaces no son dos bases de datos.**
El primero es la puerta de un portal que hoy expone 38 bases Entrez distintas, con
esquemas, identificadores y políticas de actualización propios; el segundo es una
interfaz de descarga sobre un subconjunto de ese mismo acervo. Tratarlos como «la
base de genes» y «la base de genomas» es lo que después hace que un equipo busque
los genes de la chicharrita donde no están. Y no están: lo mostramos en la
sección 4. [E]

Una advertencia de lectura sobre el segundo enlace: la página
`datasets/genome/` devuelve 26.954 bytes de HTML que, quitadas las etiquetas,
dejan 892 caracteres de texto, todos de encabezado y pie institucional. No hay
una sola línea de datos de genomas en la respuesta del servidor: la página es una
aplicación que arma la tabla en el navegador llamando a su propia API. Para
nosotros eso es una buena noticia, porque esa API es pública y documentada, pero
significa que cualquier intento de raspar la página es tiempo perdido. [E]

---

## 2. El portal no es una base: son 38 bases Entrez

`einfo` sin argumentos devuelve la lista de bases y, con `db=<nombre>`, el
conteo de registros y la fecha de última actualización de cada una
(`consultas/01_eutilities_einfo.md`). El resultado del 17 de octubre de 2026,
en las bases que nos interesan: [E]

| base | registros | última actualización |
| --- | ---: | --- |
| `gene` | 100.909.498 | 2026/10/17 |
| `nuccore` | 743.915.950 | 2026/10/16 |
| `protein` | 1.657.446.902 | 2026/10/17 |
| `ipg` | 1.236.696.225 | 2026/10/17 |
| `assembly` | 3.959.472 | 2026/10/16 |
| `biosample` | 60.414.006 | 2026/10/17 |
| `bioproject` | 1.104.628 | 2026/10/14 |
| `sra` | 47.243.078 | 2026/10/17 |
| `taxonomy` | 3.156.786 | 2026/10/13 |
| `gds` (GEO DataSets) | 9.121.639 | 2026/10/16 |
| `geoprofiles` | 128.414.055 | **2024/02/20** |
| `pubmed` | 41.300.169 | 2026/10/17 |
| `cdd` | 67.160 | 2025/07/02 |
| `annotinfo` | 2.751 | 2026/10/16 |

La frecuencia de actualización no hace falta estimarla: la declara la propia
base, y salvo `geoprofiles`, `cdd` y la base `genome` (2025/07/08), todas las que
usamos se actualizaron en los últimos cuatro días. Que `geoprofiles` figure
congelada desde febrero de 2024 es un dato a tener en cuenta antes de apoyar
cualquier análisis de expresión en ella. [E] No encontramos un anuncio oficial que
explique ese congelamiento, así que la causa queda como `[?]`.

---

## 3. Las bases que importan, una por una

### 3.1 Gene — el rótulo del organizador, y la trampa

Mantenida por el NCBI (NLM/NIH). Un registro de `gene` es un locus con su
identificador numérico estable (GeneID), su símbolo, su descripción, el taxón, y
punteros al genoma, a los transcriptos y a las proteínas. Se puebla, para la
mayoría de los organismos, a partir de la anotación de RefSeq. **Esa última frase
es la clave de todo: si un genoma no tiene anotación de RefSeq, su organismo no
tiene genes en esta base, por más que su genoma esté depositado.** [E]

Acceso: web, E-utilities (`esearch`, `esummary`, `efetch`, `elink`) y volcado
masivo por FTP en `gene/DATA/`. Formato de respuesta JSON o XML.

Ejemplo ejecutado (`consultas/02_cobertura_por_organismo.md`): los 37 registros
de *Dalbulus maidis* en `gene`, recuperados con `esearch` y descritos con
`esummary` uno por uno. Los 37 tienen `chromosome = MT` y están sobre
`NC_070066.1`: son los 13 genes codificantes del mitogenoma, los 2 ARN
ribosomales y los 22 ARN de transferencia. **Cero genes nucleares.** [E]

Responde: «¿cuál es el GeneID de este locus y qué transcriptos y proteínas le
corresponden?», para organismos con anotación RefSeq. No responde nada sobre el
vector más allá de su mitocondria, y no responde absolutamente nada sobre
'*Candidatus* Phytoplasma zeae', que tiene cero registros aquí pese a tener un
genoma completo y anotado (sección 4.2). [E]

### 3.2 Nucleotide (`nuccore`) — GenBank, RefSeq, TSA y WGS en una sola base

`nuccore` es el núcleo de secuencias nucleotídicas y mezcla cuatro orígenes que
conviene no confundir: los depósitos de autor en GenBank (accesiones de dos
letras y cinco dígitos o similares, `[Properties] srcdb_genbank`), los registros
curados de RefSeq (`NC_`, `NM_`, `NZ_`, `XM_`; `srcdb_refseq`), los proyectos de
genoma completo WGS y los transcriptomas ensamblados TSA, cuyos registros
maestros se filtran con `tsa_master[Properties]`. [E]

Ejemplo ejecutado (`consultas/05_tsa_y_ftp.md`): la consulta
`txid74065[Organism:exp] AND tsa_master[Properties]` devuelve **tres** registros
maestros de TSA para el vector, no uno. [E]

| accesión | secuencias | pares de bases | más larga | más corta | archivo `.fsa_nt.gz` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `GITV00000000` (2021) | 56.117 | 94.702.486 | 205.383 nt | 200 nt | 31,44 MB |
| `GHCC00000000` (2020) | 55.286 | 38.748.947 | 8.162 nt | 201 nt | 10,74 MB |
| `GCWP00000000` (2018) | 25.662 | 28.305.469 | 9.283 nt | 203 nt | 7,20 MB |

Los conteos y los tamaños no son nuestros: los primeros cinco salen de los
archivos `stats.tsa.*` del propio GenBank y el último, de la cabecera
`Content-Length` de cada archivo en el FTP. [E]

Responde: «dame la secuencia de referencia de X», «qué transcriptos hay
ensamblados para esta especie», «qué base de datos local puedo construir para
tamizar off-targets». Es, para nuestro problema, la base más importante de las
38. No responde qué hace cada transcripto: la anotación funcional no vive acá.

### 3.3 Protein e Identical Protein Groups

`protein` guarda secuencias proteicas de las tres fuentes (traducciones de
GenBank, entradas RefSeq `WP_`/`NP_`/`XP_`, y PDB). `ipg` agrupa las proteínas
idénticas de distintas fuentes bajo un identificador de grupo, y es el puente
práctico entre el mundo GenBank y el mundo RefSeq. [E]

Ejemplo ejecutado (`consultas/07_mapeo_ids_ejecutado.md`): `efetch -db protein
-id AOF54549 -rettype ipg` devuelve dos filas, la de INSDC y la de RefSeq, que
unen `AOF54549.1` sobre `CP015149.1` del ensamblado `GCA_001712875.1` con
`WP_069027986.1` sobre `NZ_CP015149.1` del ensamblado `GCF_001712875.1`, mismas
coordenadas 1-1524, misma hebra. Es la proteína iniciadora de la replicación
cromosómica del fitoplasma. [E]

### 3.4 Assembly y NCBI Datasets — el segundo enlace del documento

El recurso web heredado *Assembly* fue retirado por el NCBI; su reemplazo
declarado es NCBI Datasets, y el NCBI avisó que el acceso programático por
E-utilities y EDirect a la base `assembly` seguía funcionando. [R] Nuestra
corrida lo confirma por los dos lados: la base Entrez `assembly` responde y
declara 3.959.472 registros actualizados al 2026/10/16, y la API de Datasets
responde en `v2alpha` y en `v2` con la misma versión de servicio, 18.39.0. [E]

Acceso: API REST en `https://api.ncbi.nlm.nih.gov/datasets/v2alpha/`, sin
autenticación para lo que usamos; cliente de línea de comandos `datasets` y
`dataformat`; y el FTP `genomes/all/GC{A,F}/...`, cuya ruta exacta la devuelve
`esummary` en el campo `FtpPath_GenBank`. Los tres endpoints que resolvieron todo
nuestro trabajo son `genome/taxon/{TAXID}/dataset_report`,
`genome/accession/{ACC}/dataset_report` y
`genome/accession/{ACC}/download_summary`; el cuarto, `/download`, baja un ZIP
(`consultas/03_datasets_api_genomas.md` y `consultas/04_descarga_real_mrfv.md`). [E]

Ejemplo ejecutado: la descarga completa del genoma y la anotación de *Maize
rayado fino virus* (`GCF_000862485.2`), 10.394 bytes de ZIP que contienen el
FASTA genómico de `NC_002786.2`, el GFF3 con sus dos CDS, el FASTA de proteínas y
el de CDS. Se eligió una secuencia pública de referencia justamente para no tocar
material del corpus. [E]

Lo que **no** corrió: el cliente `datasets` 18.39.0 se instaló desde Bioconda y
responde `--version`, pero toda llamada de red falla con
`tls: failed to verify certificate: x509: OSStatus -26276` contra el proxy del
entorno, también forzando `SSL_CERT_FILE`. `curl` contra el mismo endpoint
devuelve 200, así que es una limitación del cliente Go en nuestro sandbox, no del
servicio ni del dominio; en las notebooks del equipo va a funcionar. Las mismas
consultas se resolvieron por REST (`consultas/06_edirect_cli.md`). [E]

### 3.5 BioProject y BioSample

`bioproject` describe el proyecto —quién, para qué, qué tipo de datos— y
`biosample` la muestra física. Son el tejido conectivo: de un BioProject se llega
por `elink` a sus BioSamples, a sus corridas de SRA y a sus ensamblados. Para
nosotros valen sobre todo como índice de qué experimentos existen sobre el
vector; la lista completa de los 17 proyectos de *D. maidis* está en la
sección 4.1. [E]

### 3.6 SRA

Lecturas crudas. Se consulta por E-utilities y, lo más útil, `efetch -format
runinfo` devuelve un CSV con una fila por corrida y 40 columnas, entre ellas
`spots`, `bases`, `size_MB`, `LibraryStrategy`, `Platform` y `SampleName`. Esa
columna de tamaño es lo que permite planificar una ingesta con números reales en
lugar de estimaciones (`consultas/06_edirect_cli.md`, ejemplos E3 y E4). [E]

### 3.7 GEO

`gds` indexa series y muestras de expresión; `geoprofiles`, perfiles por gen.
Para nuestro problema la respuesta es corta y vale como vacío documentado:
*Dalbulus maidis* tiene **cero** registros en `gds`, y también los tienen en cero
*Spiroplasma kunkelii*, el fitoplasma y los tres virus. Los datos de expresión
del vector existen, pero están en SRA sin pasar por GEO. [E]

### 3.8 Taxonomy

Un taxón por registro, con su TaxID, su rango y su linaje completo. Es la llave
con la que se consulta todo lo demás: `txid<N>[Organism:exp]` expande a los
descendientes, que es lo que hace comparables las cifras de la sección 4. Los
TaxID que usamos, resueltos por `esearch` sobre `[Scientific Name]`: *Dalbulus
maidis* 74065, *Zea mays* 4577, *Spiroplasma kunkelii* 47834, '*Candidatus*
Phytoplasma zeae' 202462, *Maize rayado fino virus* 59749, Cicadellidae 30102. [E]

### 3.9 Las que usamos poco, y por qué

`pubmed` es el insumo de W1 y no lo tocamos acá salvo por `elink`, que lleva de
un gen a los artículos que lo describen. `cdd` (dominios conservados) es el
camino para anotar funcionalmente una proteína sin ortólogo evidente, y su última
actualización es de julio de 2025. `annotinfo` describe las corridas de anotación
del NCBI y resultó un verificador independiente del vacío del vector: *D. maidis*
tiene 0 registros, *Macrosteles quadrilineatus* tiene 1 y *Zea mays*, 6. `genome`
está en desuso y su conteo no se mueve desde julio de 2025. [E]

---

## 4. Cobertura para nuestro problema, que es donde se decide todo

La tabla siguiente es una consulta por celda: `esearch` con
`txid<TAXID>[Organism:exp]` y `rettype=count`, sobre ocho bases, para
veinticuatro organismos que nos importan por alguna razón: el vector, el
cultivo, los cuatro candidatos a patógeno, parientes del vector con y sin
genoma anotado, los hemípteros donde el RNAi ya está demostrado, y una selección
de no objetivo de referencia. Está entera, con el comando, en
`consultas/02_cobertura_por_organismo.md` y en `consultas/cobertura_entrez.csv`. [E]

| organismo | taxid | gene | nuccore | protein | assembly | sra | biosample | bioproject | gds |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dalbulus maidis | 74065 | 37 | 92 | 87 | 3 | 37 | 45 | 17 | 0 |
| Dalbulus (género) | 74053 | 37 | 124 | 98 | 5 | 40 | 52 | 21 | 0 |
| Cicadellidae (familia) | 30102 | 56.026 | 347.492 | 333.699 | 59 | 2.930 | 3.930 | 636 | 25 |
| Zea mays | 4577 | 72.398 | 4.890.322 | 377.650 | 204 | 186.342 | 167.801 | 6.499 | 24.701 |
| Spiroplasma kunkelii | 47834 | 20 | 507 | 3.647 | 1 | 1 | 6 | 3 | 0 |
| Ca. Phytoplasma zeae | 202462 | 0 | 78 | 1.066 | 1 | 6 | 6 | 4 | 0 |
| Mollicutes (clase) | 31969 | 51.249 | 98.477 | 885.140 | 3.104 | 1.548 | 8.365 | 935 | 47 |
| Maize rayado fino virus | 59749 | 3 | 71 | 67 | 2 | 0 | 0 | 0 | 0 |
| Maize striate mosaic virus | 2025388 | 9 | 19 | 73 | 2 | 0 | 0 | 0 | 0 |
| Maize stripe virus | 3052767 | 9 | 77 | 131 | 1 | 0 | 0 | 0 | 0 |
| Diaphorina citri | 121845 | 31.912 | 252.391 | 95.854 | 10 | 808 | 1.248 | 86 | 14 |
| Nephotettix cincticeps | 94400 | 37 | 535 | 441 | 1 | 40 | 33 | 17 | 25 |
| Macrosteles quadrilineatus | 74068 | 24.179 | 38.771 | 35.221 | 3 | 34 | 41 | 15 | 0 |
| Graminella nigrifrons | 30127 | 0 | 37.565 | 25 | 0 | 56 | 56 | 8 | 0 |
| Euscelidius variegatus | 13064 | 0 | 142 | 132 | 1 | 19 | 61 | 5 | 0 |
| Nilaparvata lugens | 108931 | 29.502 | 338.438 | 35.943 | 4 | 2.187 | 2.261 | 200 | 36 |
| Tribolium castaneum | 7070 | 19.371 | 129.093 | 42.666 | 7 | 2.636 | 2.579 | 149 | 793 |
| Apis mellifera | 7460 | 21.375 | 398.812 | 62.955 | 17 | 26.520 | 35.878 | 728 | 3.272 |
| Bombus terrestris | 30195 | 15.804 | 303.519 | 28.096 | 5 | 4.860 | 5.665 | 101 | 224 |
| Chrysoperla carnea | 189513 | 15.868 | 20.224 | 17.827 | 5 | 23 | 20 | 13 | 0 |
| Coccinella septempunctata | 41139 | 16.934 | 26.554 | 24.091 | 3 | 293 | 297 | 30 | 5 |
| Daphnia magna | 35525 | 33.021 | 601.688 | 622.453 | 14 | 6.791 | 6.856 | 184 | 3.037 |
| Eisenia fetida | 6396 | 37 | 5.544 | 764 | 2 | 582 | 704 | 68 | 586 |
| Homo sapiens | 9606 | 360.659 | 29.885.237 | 2.183.220 | 3.220 | 7.271.118 | 16.837.648 | 153.982 | 4.753.639 |

### 4.1 El vector: genoma sí, genes no

*Dalbulus maidis* tiene tres ensamblados y ninguno anotado. El informe de
Datasets lo dice campo por campo: `GCA_975739785.1` (nivel cromosoma,
972.206.121 pb en 499 secuencias, N50 de contig 5.293.657, Wellcome Sanger
Institute), `GCA_975739835.1` (haplotipo alternativo, 488.450.451 pb en 8.928
secuencias) y `GCA_054756405.1` (CIAP v1, 585.210.080 pb en 22.333 contigs, N50
50.514, Instituto de Patología Vegetal CIAP-INTA). En los tres, el campo
`annotation_info` viene vacío. La base `annotinfo` lo confirma desde otro lado
con 0 registros, y la base `gene`, con sus 37 entradas mitocondriales. **Al 17 de
octubre de 2026 no existe un conjunto de genes nucleares anotados de la
chicharrita en el NCBI.** [E]

Esto no es un detalle administrativo: es la restricción que ordena todo el
trabajo del equipo. Sin anotación no hay lista de genes blanco, no hay
identificador estable por gen, y el tamizaje de especificidad dentro del propio
vector no se puede hacer contra un catálogo de genes. Lo que sí hay es
transcriptoma ensamblado, y por triplicado: los 56.117 transcriptos de
`GITV00000000` son el objeto de cómputo realista, y los otros dos conjuntos
sirven de control de cobertura. [E]

Hay además un recurso que la ola 1 no había identificado y que es el mejor dato
nuevo de esta investigación en materia de expresión: el BioProject
**PRJNA631706**, «Transcriptional response of *Dalbulus maidis* to maize rayado
fino virus», con 16 corridas de RNA-Seq en Illumina HiSeq 2000, 6,381 × 10¹⁰
bases y 42.305 MB de descarga declarada por el propio SRA. Los nombres de muestra
describen un diseño de dos factores con cuatro réplicas: insectos expuestos a
MRFV contra insectos naíf, a 4 horas y a 7 días, a 30 °C
(`consultas/06_edirect_cli.md`, ejemplos E3 y E4). [E] Es decir: hay material
público para preguntar qué genes del vector responden a la infección por el
virus, que es una pregunta directamente útil para priorizar blancos. [H] Que ese
diseño sirva para elegir blancos de RNAi es una hipótesis nuestra, no un
resultado publicado que hayamos leído.

Los 17 BioProjects del vector, tal como los devuelve `esummary`:

| accesión | tipo | registro | título |
| --- | --- | --- | --- |
| PRJEB97791 | Genome sequencing | 2025/10/27 | Dalbulus maidis genome assembly, ihDalMaid1 |
| PRJEB97790 | Genome sequencing | 2025/10/27 | ihDalMaid1, haplotipo alternativo |
| PRJEB96548 | — | 2025/10/27 | Dalbulus maidis |
| PRJEB96547 | Other | 2025/10/27 | Dalbulus maidis, genomic and transcriptomic data |
| PRJNA1282137 | Raw sequence reads | 2025/06/25 | Virome Characterization of the Corn Leafhopper |
| PRJNA1120083 | Genome sequencing | 2024/06/04 | Dalbulus maidis isolate:CIAP and endosymbiont |
| PRJNA927516 | RefSeq Genome | 2023/01/25 | Dalbulus maidis RefSeq Genome |
| PRJNA852223 | Genome sequencing | 2022/06/23 | Genome sequencing and assembly |
| PRJNA780295 | Raw sequence reads | 2021/11/14 | Anchored hybrid enrichment sequencing of Cicadellidae |
| PRJNA631706 | Transcriptome/expr. | 2020/05/11 | Transcriptional response to maize rayado fino virus |
| PRJNA609979 | Raw sequence reads | 2020/03/03 | Maize leafhopper Iso-Seq reads and transcriptome |
| PRJNA579843 | Transcriptome/expr. | 2019/10/27 | Transcriptome with/without MRFV exposed at 25C |
| PRJNA562189 | Transcriptome/expr. | 2019/08/26 | Deltocephalinae leafhoppers |
| PRJNA505619 | Transcriptome/expr. | 2018/11/15 | Dalbulus maidis Transcriptome or Gene expression |
| PRJNA505618 | Raw sequence reads | 2018/11/15 | Dalbulus maidis Raw sequence reads |
| PRJNA318849 | Transcriptome/expr. | 2016/04/19 | Dalbulus maidis Transcriptome or Gene expression |
| PRJNA272239 | Transcriptome/expr. | 2015/01/09 | The 1KITE project: evolution of insects |

Llama la atención `PRJNA927516`, registrado como «RefSeq Genome» en enero de
2023, cuando ningún ensamblado del vector tiene anotación de RefSeq hoy. Puede
ser un proyecto reservado para una anotación futura. Lo anotamos como `[?]` y es
una de las preguntas de la sección 10. [?]

### 4.2 Los patógenos: dos genomas completos y un agujero de anotación

*Spiroplasma kunkelii* y '*Candidatus* Phytoplasma zeae' tienen cada uno su
genoma completo en las dos versiones, GenBank y RefSeq, y las dos versiones de
RefSeq fueron reanotadas hace poco: [E]

| organismo | ensamblado | pb | secuencias | anotación RefSeq | genes | codificantes | no codificantes | pseudogenes |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| *S. kunkelii* CR2-3x | `GCF_001274875.1` | 1.514.561 | 4 | RS_2025_12_13 | 1.951 | 1.775 | 39 | 137 |
| '*Ca.* P. zeae' M3 | `GCF_001712875.1` | 576.118 | 1 | RS_2026_06_07 | 581 | 524 | 41 | 16 |
| MRFV | `GCF_000862485.2` | 6.366 | 1 | NCBI RefSeq, 2020-10-13 | 2 | 2 | — | — |

Y acá aparece la segunda trampa del rótulo «database general de genes»: esos
genomas anotados **no están en la base `gene`**. *S. kunkelii* tiene 20 registros
de gen para 1.775 genes codificantes anotados, y '*Ca.* P. zeae' tiene **cero**
para 524. La anotación existe, pero vive en el GFF3 del ensamblado y en la base
`protein` —1.727 proteínas RefSeq para el espiroplasma, 522 para el
fitoplasma—, no en `gene`. [E] La pequeña diferencia entre los genes codificantes
declarados por la anotación y las proteínas RefSeq indexadas (1.775 contra 1.727;
524 contra 522) no la pudimos explicar y queda `[?]`; lo más probable es que
tenga que ver con la no redundancia de las accesiones `WP_`. [H]

Consecuencia operativa concreta: para obtener el proteoma de cualquiera de los
dos patógenos no se consulta `gene`, se baja el `protein.faa` o el `cds_from_genomic.fna`
del ensamblado con Datasets. Pesan 0,22 MB y 0,09 MB. [E]

Sobre el cuarto agente del complejo hay un problema de identidad que no podemos
resolver nosotros. El equipo viene llamándolo MSMV desde la ola 1. En el NCBI hay
dos taxones distintos que compiten por ese nombre: `maize striate mosaic virus`
(TaxID 2025388), que es un *Mastrevirus* de Geminiviridae con dos genomas
completos de 2.746 pb (`GCF_004788335.1`, `GCF_004130985.1`); y *Tenuivirus
zeae* (TaxID 3052767), el maize stripe virus, de Phenuiviridae, con
`GCF_002867025.1` de 9.238 pb. Son familias de virus distintas, con vectores
distintos. [E] Cuál de los dos es el del complejo de achaparramiento argentino es
una pregunta para el investigador, y hasta que se responda cualquier diseño
contra «MSMV» apunta a un blanco mal definido. [?]

Mención aparte para `PRJNA1294367`, los tres genomas de fitoplasma de
Pellegrinetti y colaboradores que la ola 1 no había podido encontrar como
ensamblados. Hoy, 17 de octubre de 2026, el proyecto existe —registrado el
2025/07/21, con 13 BioSamples—, pero sigue **sin ensamblados**: `elink` hacia
`assembly` devuelve vacío y su único registro de nucleótidos es `PZ340875.1`, una
secuencia parcial de ARNr 16S de 1.533 nt publicada el 2026/05/03. La
observación de la ola 1 se mantiene. [E]

### 4.3 El cultivo

*Zea mays* es el extremo opuesto del vector: 72.398 genes, 4.890.322 registros de
nucleótidos, 204 ensamblados y 24.701 conjuntos en GEO. La referencia
`GCF_902167145.1` (Zm-B73-REFERENCE-NAM-5.0) tiene 2.182.075.994 pb y una
anotación RefSeq de febrero de 2025 con 49.888 genes, 34.313 de ellos
codificantes. Para el tamizaje de off-target en la planta lo que hace falta no es
el genoma sino el transcriptoma: `rna.fna` pesa 36,03 MB según el servicio y
37,78 MB comprimido en el FTP. [E]

### 4.4 Parientes del vector y organismos no objetivo

El hallazgo con mayor valor práctico de esta sección: *Macrosteles
quadrilineatus*, el cicadélido vector de fitoplasmas de la misma familia que la
chicharrita, **sí tiene anotación RefSeq**: `GCF_028750875.1`, 1.317.891.973 pb,
24.178 genes y 21.979 codificantes, anotación de marzo de 2023; su `rna.fna` pesa
20,39 MB y su `protein.faa`, 7,70 MB. Y hay dos ensamblados cromosómicos más
recientes, `GCA_976628355.1` y `GCA_976823985.1`, con N50 de 20,9 y 21,3 Mb, aún
sin anotar. [E] Es el proteoma de referencia natural para transferir blancos por
ortología hacia un transcriptoma de *D. maidis* que no tiene nombres de gen. [H]

De los no objetivo que conviene tener en la base de tamizaje, todos tienen
genoma y anotación amplia: *Apis mellifera* (21.375 genes), *Bombus terrestris*
(15.804), *Coccinella septempunctata* (16.934), *Chrysoperla carnea* (15.868),
*Daphnia magna* (33.021). *Eisenia fetida*, la lombriz de referencia para fauna
del suelo, tiene 37 genes y 2 ensamblados: para ella el tamizaje tendría que
hacerse contra transcriptos, no contra un conjunto de genes. [E]

---

## 5. Qué pregunta nuestra responde cada base, y cuál no

| base | encontrar blancos | tamizar off-targets | secuencias de referencia | expresión | anotación funcional |
| --- | --- | --- | --- | --- | --- |
| `gene` | sólo para maíz y *Macrosteles*; inútil para el vector y los patógenos | no | no | no | parcial (descripción del locus) |
| `nuccore` | sí, vía TSA del vector | **sí: es la fuente de las bases locales** | sí | no | no |
| `protein` / `ipg` | sí, por ortología | sí, a nivel proteína | sí | no | parcial |
| Datasets / `assembly` | sí, cuando hay anotación | sí: FASTA de ARN y de CDS | sí | no | sí, vía GFF3 |
| `bioproject` / `biosample` | no | no | no | índice de qué existe | no |
| `sra` | no directamente | no | no | **sí, es la única fuente para el vector** | no |
| `gds` (GEO) | no | no | no | sí para maíz, nada para el vector | no |
| `taxonomy` | no | delimita el universo del tamizaje | no | no | no |
| `cdd` | no | no | no | no | sí |

---

## 6. Diferencias con la lista que la ola 1 armó a ciegas

La comparación es contra `research/R5_metodologias_ejes/stack_bioinformatico.md`.
El balance es bueno: la lista de la ola 1 acertó los recursos y los usos, y lo
que agrega esta ola es precisión, tres recursos que faltaban y dos correcciones.

Lo que se confirma tal cual: que los ensamblados del vector existen sin
anotación; que son 37 corridas en SRA de las cuales 23 son RNA-Seq —el número
coincide exactamente hoy—; que la página `datasets/genome/` no entrega datos sin
JavaScript; que el genoma del fitoplasma es `GCF_001712875.1`, de 576.118 pb en
una sola secuencia, con 581 genes y 524 codificantes en la reanotación del
2026-06-07; y que `PRJNA1294367` no devuelve ensamblados. [E]

Lo que se agrega:

1. **Hay tres transcriptomas TSA del vector, no uno.** La ola 1 registró
   `GITV00000000` como «el atajo del proyecto». Están además `GHCC00000000`
   (55.286 transcriptos) y `GCWP00000000` (25.662). [E]
2. **Existe *Macrosteles quadrilineatus* con anotación RefSeq completa.** La ola
   1 no lo menciona en ninguna de sus tablas, y es el donante de ortología más
   cercano que tenemos. [E]
3. **Existe PRJNA631706**, 16 corridas de RNA-Seq del vector expuesto a MRFV
   contra naíf. La ola 1 llegó a listar el proyecto hermano `PRJNA579843` sin
   notar que el de 2020 tiene las corridas. [E]
4. **'*Ca.* Phytoplasma zeae' está en KEGG** como organismo `mbp`, genoma T04456,
   con 485 genes mapeados a identificadores de proteína del NCBI. La ola 1 sólo
   había registrado el espiroplasma, `skn` / T04056. [E]

Lo que se corrige:

5. **El recurso web Assembly fue retirado** y su reemplazo es Datasets; la ola 1
   lo listaba como «NCBI Assembly / GenBank» sin señalarlo. La base Entrez
   `assembly` sigue viva y consultable, de modo que los comandos de la ola 1 no
   se rompen, pero la ruta recomendada hoy es otra. [R]
6. **El número de transcriptos de `GITV00000000`.** La ola 1 anotó 56.116,
   tomado del artículo de Xu y colaboradores; el registro maestro de `nuccore` y
   el archivo `stats.tsa.GITV` del NCBI declaran 56.117. Es una diferencia de un
   registro y no cambia nada práctico, pero el número que hay que citar cuando se
   describe el archivo que uno bajó es el del NCBI. [?]

Una precisión que no es contradicción: la ola 1 estimó que «el genoma de 972 Mb
ocupa ~1 GB sin comprimir», y es correcto; lo que se transfiere por la red son
268,6 MB, que es lo que declara el servicio para el FASTA genómico de
`GCA_975739785.1`. [E]

---

## 7. Licencia y condiciones de uso

La página de GenBank, sección *GenBank Data Usage*, dice que el NCBI no impone
restricciones al uso ni a la redistribución de los datos, y advierte en la misma
frase que algunos depositantes pueden reclamar patente o derecho de autor sobre
lo que depositaron, que el NCBI no está en posición de evaluar esos reclamos y
que la responsabilidad de respetarlos es de quien usa el dato. Textual, lo que
importa: «NCBI places no restrictions on the use or distribution of the GenBank
data». [E] La página institucional de políticas agrega que la información creada
por o para el gobierno de los Estados Unidos es de dominio público y puede
copiarse y distribuirse libremente, con el pedido de citar a la NLM como fuente. [E]

Para publicar nuestros resultados eso alcanza, con tres cuidados. Primero, citar
las accesiones exactas y la fecha de descarga, porque RefSeq reanota: el genoma
del espiroplasma cambió de anotación en diciembre de 2025 y el del fitoplasma en
junio de 2026, y un resultado calculado sobre una versión no es reproducible sin
decir cuál. Segundo, el dominio público del dato no cubre el artículo que lo
describe. Tercero, hay recursos que vamos a usar y que **no** son del NCBI ni
tienen esta licencia: el ensamblado del INTA, que la ola 1 registró como CC
BY-NC-SA, y KEGG, cuyo uso académico por la web es gratuito pero cuyo volcado
masivo es pago. Eso se maneja caso por caso. [R]

Las condiciones de uso de las API, por último, son parte de la licencia en la
práctica: la guía oficial de E-utilities pide no superar tres peticiones por
segundo sin clave de API —diez con clave—, identificar la herramienta y un
correo de contacto, y correr los trabajos grandes fuera del horario pico de los
Estados Unidos. [R] Nuestras 409 peticiones corrieron sin clave, espaciadas entre
0,34 y 0,5 s, y el servidor devolvió 429 dos veces; con reintento y espera
creciente se resolvieron las dos. Para la ingesta del plan, conviene pedir la
clave. [E]

---

## 8. Lo que no está en el `.docx` y vamos a usar igual

Tres recursos ajenos al documento aparecen en este reporte porque resuelven algo
que el NCBI no resuelve, y los marcamos como lo que son: agregados nuestros.
UniProtKB, para anotación funcional curada y para su mapeo de identificadores
(ejecutado: `WP_053391442.1` → `A0A0K2JJJ7`, TrEMBL, proteoma UP000062963 de
*S. kunkelii* CR2-3x). KEGG, para vías metabólicas y esencialidad, con los dos
patógenos presentes como `skn` y `mbp`. Y Ensembl Plants para maíz, que la ola 1
ya había registrado. Ninguno reemplaza al NCBI: lo complementan por el lado de la
anotación funcional, que es exactamente lo que el portal del organizador no
cubre. [E]

---

## 9. Plan de ingesta

Está completo en `plan_ingesta.md`, con los tamaños medidos y el orden de
descarga. En una línea: 117,8 MB resuelven todo el trabajo de diseño y tamizaje —los tres
transcriptomas del vector, el transcriptoma de maíz, el transcriptoma y el
proteoma de *Macrosteles*, y los genomas con su anotación de los dos patógenos y
de los virus—, y recién después, si hace falta, se discuten los 268,6 MB del
genoma del vector y los 41,3 GB de PRJNA631706.

---

## 10. Vacíos y preguntas para el investigador

Lo que no pudimos resolver, en orden de importancia para el diseño:

1. **¿Cuál es el cuarto patógeno?** «MSMV» corresponde en el NCBI a dos virus de
   familias distintas. Sin eso, no hay blanco viral definido más allá de MRFV. [?]
2. **¿EPILAB trabaja sobre una anotación propia del vector?** Las secuencias de
   la planilla tienen nombres de gen (`BicC_Dm`, `ATPaseD_Dm`) que no pueden venir
   de la base `gene`, porque allí no hay genes nucleares de la especie. O vienen
   de una búsqueda por homología sobre el TSA, o de una anotación no publicada.
   La respuesta cambia qué podemos reproducir. [?]
3. **¿Qué significa `PRJNA927516`, «Dalbulus maidis RefSeq Genome», registrado en
   2023, si no hay anotación RefSeq del vector?** [?]
4. **¿Hay acceso a datos de expresión del vector por tejido?** Lo público es el
   diseño de PRJNA631706, que es por tratamiento y tiempo, no por tejido. Un
   criterio de priorización de blancos por expresión en intestino o glándula
   salival no se puede sostener hoy con datos públicos. [?]
5. Por qué `geoprofiles` figura sin actualizarse desde febrero de 2024. Es
   menor, pero conviene saberlo antes de apoyarse en esa base. [?]
