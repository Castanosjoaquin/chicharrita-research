# W4 — Qué material genómico tenemos, en qué estado, y qué análisis habilita

Ola 2 del Investigathón Y-Hat. Reporte de los genomas y transcriptomas.
Fecha de todas las consultas y corridas: **17 de octubre de 2026**.
Marcadores: `[E]` establecido, `[R]` reportado, `[H]` hipótesis nuestra, `[?]` incierto.

---

## 0. El titular, en la primera página

**El corpus oficial no trae ni un solo archivo genómico.** Ni FASTA, ni GFF, ni GTF, ni
FASTQ, ni índices. Lo verificamos contra el inventario del corpus:
`research/ola2/MANIFEST.md`, sección 5, lo declara explícitamente y el único recurso que
figura es un enlace a NCBI Datasets dentro de `YHat-Biotech/Links de interes.docx`
(`https://www.ncbi.nlm.nih.gov/datasets/genome/`) `[E]`. En consecuencia este inventario
no es de archivos recibidos: es de **material que bajamos nosotros del NCBI**, con todas
las métricas recalculadas localmente sobre lo que efectivamente se descargó.

**El segundo titular, que es el que condiciona el proyecto:** *Dalbulus maidis* (la
chicharrita del maíz) **tiene tres ensamblados genómicos públicos y ninguno de los tres
tiene anotación de genes** `[E]`. La consulta a NCBI Datasets v2alpha del 17 de octubre de
2026 devuelve tres ensamblados para el taxón y ninguno con bloque `annotation_info`
(`scripts/01_consulta_ncbi_datasets.py`). No hay registros TSA (*Transcriptome Shotgun
Assembly*) de la especie: la búsqueda `"Dalbulus maidis"[Organism] AND TSA[Division]` en la
base `nucleotide` devuelve **0** `[E]`. La base Gene del NCBI tiene **37 registros** para
*D. maidis*, contra **24.179** de *Macrosteles quadrilineatus*, un cicadélido de la misma
subfamilia que sí está anotado `[E]`. Esto confirma, con datos de hoy, lo que la ola 1 ya
había anotado en `research/R2_attention_diseno_arn/datos_disponibles.md`.

La consecuencia operativa es precisa y conviene no suavizarla: **el insumo más básico de
cualquier método de diseño o priorización de ARN de doble cadena (ARNdc) contra el vector
—la lista de transcriptos del blanco— no existe y hay que construirlo**. Lo que sí
mostramos en la sección 6.1 es que la ausencia de anotación **no bloquea** localizar genes
concretos en el genoma del vector: con un proteoma de cicadélido anotado y `miniprot`,
64 de 64 proteínas consultadas (maquinaria de RNAi y familias de los genes blanco)
alinearon con cobertura 1,00 sobre el ensamblado de nivel cromosoma, en minutos.

Y un tercer titular, chico pero con consecuencias de alcance: el ensamblado de nivel
cromosoma del vector, publicado por el Wellcome Sanger Institute el 26 de octubre de 2025,
es **excelente**. Nuestra estimación de completitud da **97,7 %** de ortólogos de insecto
recuperados (94,51 % completos más 3,22 % duplicados, sobre 1.367 ortólogos de
`insecta_odb10`). El borrador argentino del CIAP-INTA, en cambio, da **68,8 %**. La ola 1
tenía los dos ensamblados en la misma línea de la tabla, como si fueran alternativas
equivalentes: no lo son.

---

## 1. Cómo se produjo cada número

Todo corrió local, sobre copias en `work/W4/`. Ninguna secuencia se subió a ningún
servicio web: las únicas llamadas salientes son consultas de **metadatos** y descargas
desde el NCBI. Los scripts están en `research/ola2/W4_genomas/scripts/` y son ejecutables.

| Paso | Script | Qué hace |
| --- | --- | --- |
| Metadatos de ensamblados | `01_consulta_ncbi_datasets.py` | Consulta NCBI Datasets v2alpha para 15 taxones, por nombre y —desde la corrección del fitoplasma— también por taxid y guarda nivel, fecha, BioProject, estadísticas declaradas y estado de anotación |
| Descarga | `02_descarga_ncbi.py` | Baja por accesión el FASTA genómico, los transcriptos, los CDS, las proteínas y el GFF3, vía la API de Datasets |
| Consultas de SRA, TSA y taxonomía | `03_eutils_consultas.py` | E-utilities: conteos por base y metadatos corrida por corrida |
| Métricas | `04_metricas.py` | En una pasada: número de secuencias, largo total, mínimo, máximo, mediana, N50/L50, N90/L90, GC sobre bases no ambiguas, conteo de N y de bases IUPAC ambiguas; para GFF3, conteo por tipo de *feature*, biotipos de gen, transcriptos por gen |
| Barrido completo | `05_inventario_metricas.py` | Recorre `work/W4/downloads/` y produce `metricas_todas.jsonl` (43 archivos medidos) |
| Completitud | `06_completitud_miniprot.py` | Alinea las 13.663 variantes ancestrales de `insecta_odb10` (1.367 ortólogos) contra un ensamblado con `miniprot` y clasifica por cobertura |
| Ortólogos dirigidos | `07_busqueda_ortologos.py` | Selecciona proteínas de un proteoma anotado por nombre y las alinea contra un genoma sin anotar |
| Factibilidad de tamizaje | `08_tamizaje_factibilidad.py` | Deriva los 21-meros de una secuencia **pública** y cuenta coincidencias exactas 21/21 en las dos hebras contra transcriptomas locales |

Ejemplo de invocación, tal cual se corrió:

```
python3 scripts/02_descarga_ncbi.py work/W4/downloads GCA_975739785.1 GENOME_FASTA
python3 scripts/04_metricas.py fasta work/W4/downloads/GCA_975739785.1/ncbi_dataset/data/\
GCA_975739785.1/GCA_975739785.1_ihDalMaid1.1_genomic.fna --etiqueta GCA_975739785.1
python3 scripts/06_completitud_miniprot.py <genoma.fna> work/W4/busco/insecta_odb10 \
work/W4/completitud/GCA_975739785.1 9
```

El volumen total: **17 conjuntos de datos descargados del NCBI, 43 archivos medidos,
7,0 GB en `work/W4/downloads/`**, más el linaje `insecta_odb10` (90 MB). Nada de eso entra
al repositorio: `work/` está fuera del control de versiones.

Versiones: `miniprot` 0.18-r281 (Bioconda, entorno `bioinfo`), linaje BUSCO
`insecta_odb10` del 2024-01-08 (1.367 ortólogos), Python 3.11 para los scripts propios.
Las descargas usan NCBI Datasets v2alpha y E-utilities, sin clave de API.

**Una advertencia sobre la completitud.** `06_completitud_miniprot.py` **no es BUSCO ni
compleasm**: el paquete `compleasm` de Bioconda no resuelve en este equipo (conflicto
irreconciliable entre `dendropy <4.6` que pide `compleasm` y `dendropy >=5.0.8` que pide
`sepp`, registrado abajo en la sección 8). Implementamos el mismo esquema —alinear las
variantes ancestrales del linaje con `miniprot` y clasificar por cobertura— con umbrales
**nuestros y declarados**: completo ≥ 0,70 de la proteína de referencia, fragmentado entre
0,30 y 0,70, ausente por debajo, duplicado si hay dos o más loci sin solapamiento por
encima de 0,70. BUSCO usa cortes por ortólogo derivados de `lengths_cutoff`, así que los
números son comparables en orden de magnitud y no idénticos. La calibración disponible es
buena: sobre el borrador del CIAP-INTA nuestro proxy da **68,76 %** de completos más
duplicados y el preprint del mismo ensamblado reporta **68,6 %** de completitud con BUSCO
en modo genoma **contra el mismo linaje `insecta_odb10`, de 1.367 ortólogos** `[R]`
(Debat, Humberto Julio y Fernández, Franco, IPAVE-CIAP-INTA y UFYMA-CONICET, Córdoba,
*First Draft Genome of the Corn Leafhopper Dalbulus maidis: A Transparent, Open, and
Updateable Resource in the Context of Agricultural Emergence*, bioRxiv
10.1101/2024.06.25.600652, versión depositada el 30 de junio de 2024 según la marca de
agua del propio PDF, abierta el 17 de octubre de 2026). La coincidencia es
de 0,16 puntos porcentuales sobre un ensamblado distinto del que calibramos, lo que
respalda usar el proxy para comparar ensamblados entre sí `[H]`.

---

## 2. El vector: *Dalbulus maidis*

Tres ensamblados, ninguno anotado. Las métricas son nuestras, calculadas sobre el FASTA
descargado; las de NCBI se muestran al lado porque **no coinciden**, y la diferencia tiene
una explicación exacta.

| | GCA_975739785.1 | GCA_975739835.1 | GCA_054756405.1 |
| --- | --- | --- | --- |
| Nombre | ihDalMaid1.1 | ihDalMaid1.1 haplotipo alternativo | CIAP v1 |
| Nivel | cromosoma | scaffold | contig |
| Enviado por | Wellcome Sanger Institute | Wellcome Sanger Institute | Instituto de Patología Vegetal, CIAP-INTA |
| BioProject | PRJEB97791 | PRJEB97790 | PRJNA1120083 |
| Fecha | 2025-10-26 | 2025-10-26 | 2026-01-26 |
| Secuencias en el FASTA | 141 | 7.864 | 22.334 |
| Largo total medido | 972.225.736 bp | 488.450.451 bp | 585.230.275 bp |
| Largo declarado por NCBI | 972.206.121 bp | 488.450.451 bp | 585.210.080 bp |
| N50 (nuestro, sobre el FASTA) | 93.705.284 bp | 492.899 bp | 50.514 bp |
| L50 | 5 | 184 | 3.255 |
| Secuencia más larga | 122.877.750 bp | 5.754.311 bp | 813.345 bp |
| GC | 35,035 % | 34,682 % | 34,749 % |
| N (huecos) | 38.900 (0,004 %) | 106.400 (0,022 %) | 0 |
| Completitud (proxy, `insecta_odb10`) | **94,51 % completo + 3,22 % dup.** | 32,33 % + 3,15 % | 65,47 % + 3,29 % |
| Fragmentados / ausentes | 0,29 % / 1,98 % | 8,63 % / 55,89 % | 16,46 % / 14,78 % |
| Anotación de genes | **no** | **no** | **no** |

**La diferencia de largo con NCBI es la mitocondria** `[E]`. En el ensamblado de Sanger el
FASTA incluye `OZ319714.1`, de **19.615 bp**, rotulado `organelle: mitochondrion`, y
972.225.736 − 972.206.121 = 19.615. En el del CIAP-INTA incluye `CM139083.1`, de **20.195
bp**, y la diferencia es exactamente esa. El dato no es trivial para nosotros: el genoma
mitocondrial del vector está disponible en los dos ensamblados y los genes mitocondriales
son blancos de RNAi usados en otros insectos, de modo que entra al espacio de diseño sin
trabajo adicional `[H]`.

Sobre el **L50 de 5** del ensamblado de Sanger: cinco secuencias cubren la mitad del
genoma y diez cubren el 90 %, lo que es consistente con un cariotipo de pocas y grandes
unidades cromosómicas. Para nuestro problema significa que una región blanco se puede
ubicar en coordenadas estables, que los genes caben enteros en un scaffold, y que un
tamizaje de off-target intraespecífico contra el genoma completo es directo.

El **haplotipo alternativo no es un segundo genoma**: con 55,89 % de ortólogos ausentes,
es la fracción divergente del individuo diploide. Sirve para preguntar si una región
blanco elegida cae en una zona heterocigota —una pregunta real, porque un ARNdc diseñado
sobre un alelo puede perder apareamientos en el otro—, y no sirve como referencia `[H]`.

El **borrador del CIAP-INTA** tiene un N50 de 50.514 bp y 22.334 contigs. Un gen de
insecto de tamaño mediano no entra en un contig típico de ese ensamblado, de modo que la
anotación por transferencia de ortología sobre él va a producir modelos partidos. Su valor
es otro: es el único ensamblado de **material argentino** y permite comparar secuencia
entre el aislamiento de Sanger y el local, que es lo más cerca que estamos hoy de evaluar
variación poblacional en una región blanco `[H]`. El propio preprint lo declara un
*living genome* sujeto a actualizaciones `[R]`, y de hecho la versión depositada en NCBI
(585.210.080 bp, 22.333 contigs) no es idéntica a la del preprint, que describe
`Dalbulus_CIAPv0.1`, ensamblada con Flye a partir de 1.398.710 lecturas de nanoporo
(6.151.663.624 bases), con 584.127.104 bases en 22.107 contigs y N50 de 50.453 bp `[R]`: son iteraciones distintas del mismo proyecto, y conviene citar la accesión
y no el preprint cuando se reporten métricas.

**Lo que hay para construir el transcriptoma que falta.** La base SRA tiene **37 corridas**
para *D. maidis* `[E]` (`scripts/03_eutils_consultas.py`): **23 de RNA-seq**, con
**110,1 Gbases** en total, repartidas en seis BioProjects (PRJNA631706 con 16 corridas,
PRJNA318849, PRJNA1282137, PRJNA562189, PRJNA505618 y PRJNA272239, esta última de 454); y
**10 de WGS**, con 129,8 Gbases, incluidas las lecturas PacBio y Hi-C del proyecto de
Sanger (PRJEB96547). El transcriptoma de referencia del vector es, por lo tanto, un
ensamblado *de novo* o guiado por genoma a partir de datos públicos: trabajo acotado y no
un bloqueo, pero **es el camino crítico** y nadie lo tiene hecho en forma descargable.

El trabajo que ya lo hizo —Xu, Chen, Yang y colaboradores, transcriptoma de *D. maidis*
con respuesta a MRFV, 56.116 transcriptos, citado por la ola 1 y por R1— tiene su
BioProject registrado (**PRJNA579843**, "Dalbulus maidis Transcriptome with/without MRFV
exposed at 25C") pero **cero corridas asociadas a ese accesión** en SRA; las corridas
equivalentes están bajo PRJNA631706 `[?]`. El ensamblado en sí **no está depositado como
TSA**, lo que confirma la sospecha que la ola 1 había dejado marcada como no verificada.

**Identificadores cruzables con el W3.** Los tres ensamblados sólo exponen accesiones INSDC
de secuencia (`OZ319704.1`…, `CM139083.1`) y su BioProject. No hay `GeneID`, no hay
`locus_tag`, no hay accesiones RefSeq. Lo único que cruza hoy con la base Gene del NCBI son
los 37 registros sueltos de la especie, entre los que están las cuatro accesiones de
ARNm del trabajo de microinyección del corpus: verificamos por E-utilities que
**PZ371507** (*eth* de *D. maidis*, 615 nt), **PZ371508** (*burs-α* de *D. maidis*, 468
nt), **PZ371509** (*eth* de *Delphacodes kuscheli*, 645 nt) y **PZ371510** (*burs-α* de
*D. kuscheli*, 480 nt) existen y están actualizadas al 13 de junio de 2026 `[E]`.

**Una especie hermana que la ola 1 no registró.** La consulta por el género devuelve cinco
ensamblados, e incluye `GCA_976225285.1`, *Dalbulus elimatus*, **nivel cromosoma**,
1.015.357.212 bp, GC 35 %, Wellcome Sanger Institute, BioProject PRJEB97895, liberado el
mismo 26 de octubre de 2025 y también **sin anotación** `[E]`. Es el
congénere más cercano con genoma disponible y es el control de especificidad más obvio
para un diseño que quiera no tocar a otros *Dalbulus* `[H]`. No lo descargamos (ver
sección 8).

---

## 3. El cultivo: *Zea mays*

`GCF_902167145.1`, Zm-B73-REFERENCE-NAM-5.0, MaizeGDB, BioProject PRJEB32225, con
anotación **NCBI RefSeq `GCF_902167145.1-RS_2025_02`** del 14 de febrero de 2025 `[E]`.
Nuestras métricas: **687 secuencias**, **2.182.786.008 bp**, N50 de 226.353.449 bp, GC
46,769 %, 0,1745 % de N. La diferencia con el largo declarado por NCBI (2.182.075.994 bp)
es, otra vez, exactamente la suma de los dos organelos: mitocondria `NC_007982.1` de
569.630 bp más cloroplasto `NC_001666.2` de 140.384 bp, que suman 710.014 bp.

La anotación, contada por nosotros sobre el GFF3: **44.680 *features* de tipo `gene`**
más 5.222 de tipo `pseudogene` (NCBI declara 49.888 genes totales, 34.313 codificantes;
nuestro conteo por biotipo da 34.327 `protein_coding`, 5.348 `lncRNA`, 2.439 `rRNA`), con
57.345 ARNm, 346.676 CDS, 509.115 exones y 1,717 transcriptos por gen. El origen de la
evidencia está mezclado y conviene tenerlo presente al interpretar un off-target: 691.724
*features* provienen del predictor **Gnomon** y 269.791 de **BestRefSeq**.

Para el tamizaje de off-target en el cultivo bajamos además el conjunto de transcriptos:
**76.549 secuencias, 162.712.215 bp, N50 de 2.660 nt, GC 49,522 %**. Es el archivo contra
el que hay que correr el filtro, no el genoma: lo que importa es si un siRNA derivado del
ARNdc encuentra complementariedad en un ARNm de maíz.

La limitación es la de siempre y no la resuelve ningún archivo: **B73 no es el germoplasma
comercial argentino**, y la variación entre B73 y los híbridos locales no está
cuantificada `[?]`. Un off-target ausente en B73 puede estar presente en un híbrido
sembrado en Córdoba, y al revés.

---

## 4. Los cuatro agentes del complejo de achaparramiento

R1 estableció cuáles son los cuatro (`research/R1_fundamentos/REPORT.md`, sección 3.2).
Bajamos un genoma por agente, con esta salvedad grande en el segundo.

**1. *Spiroplasma kunkelii*, `GCF_001274875.1`** (aislamiento CR2-3x). Genoma completo:
**4 secuencias** —el cromosoma circular de **1.463.926 bp** más tres plásmidos—,
**1.514.561 bp** en total, GC **24,983 %**. El largo del cromosoma coincide al dígito con
el que R1 reporta de la literatura `[E]`. La anotación es RefSeq y es **más nueva de lo
que la ola 1 registró**: `GCF_001274875.1-RS_2025_12_13`, con 1.814 genes, 137
pseudogenes, 1.912 CDS y 1.775 proteínas codificantes en nuestro conteo del GFF3. Los
identificadores cruzan con el W3 por `locus_tag` (`SKUN_RS#####`) y por proteínas `WP_`.

**2. El fitoplasma del achaparramiento: existe, está completo y está anotado. Lo tuvimos
mal en la primera versión de este reporte y la corrección importa.** Nuestra primera
consulta pidió el taxón por el nombre común, *maize bushy stunt phytoplasma*, y la API
devolvió cero ensamblados; de ahí concluimos —mal— que el agente del achaparramiento rojo
no tenía genoma. El nombre común no es el nombre científico: el **taxid 202462** se llama
hoy **'*Candidatus* Phytoplasma zeae'**, con rango de especie, y *maize bushy stunt
phytoplasma* figura como su nombre común `[E]` (consulta a
`/taxonomy/taxon/202462` del 17 de octubre de 2026). Consultado **por taxid**, el taxón
devuelve **dos ensamblados**: `GCA_001712875.1` y su par RefSeq `GCF_001712875.1`, los dos
del ensamblado ASM171287v1, liberado el **25 de agosto de 2016** `[E]`. La investigación
R5, de la **ola 1**, ya lo había registrado así —es la corrección que esa investigación
aporta— y la citamos como tal (`research/R5_metodologias_ejes/sources.json`, entrada
`pellegrinetti-2026-phytoplasma-zeae` y el dataset report de ASM171287v1).

Bajamos el ensamblado RefSeq y lo medimos con nuestros propios scripts, igual que el
resto: **una sola secuencia, `NZ_CP015149.1`, cepa M3, cromosoma completo de 576.118 bp,
GC 28,462 %, sin un solo N** `[E]`. Su anotación es RefSeq
`GCF_001712875.1-RS_2026_06_07`, del 7 de junio de 2026, y nuestro conteo sobre el GFF3 da
**565 *features* `gene`** más 16 `pseudogene`, 540 CDS, 524 genes codificantes, 32 ARNt y
6 ARNr, con un gen mediano de 615 bp; el FASTA de CDS trae 540 secuencias (452.829 bp, GC
29,884 %) y el de proteínas 522 entradas, con mediana de 220 aminoácidos. Los
identificadores cruzan con el W3 por `locus_tag` y por proteínas `WP_`.

La consecuencia es doble y conviene decirla sin rodeos. Primero: **los tres patógenos
procariotas y virales del complejo que importan acá tienen genoma completo y anotado**, de
modo que el sistema está mejor cubierto de lo que decía nuestra versión anterior y mejor
de lo que la ola 1 suponía. Segundo: entre los **genomas celulares** del complejo, el del
fitoplasma es el más chico —576 kb contra 1,5 Mb del espiroplasma—, lo que lo vuelve
barato de usar como referencia de descarte de off-targets. Los virus del complejo son dos
órdenes de magnitud más chicos todavía: el MRFV son 6.366 nt.

Mantenemos descargados los dos genomas de *'Candidatus* Phytoplasma asteris'
—`GCF_038505995.1` (778.308 bp, GC 27,835 %, 781 genes, 740 codificantes) y
`GCF_038396745.1` (662.369 bp, GC 26,772 %, 591 genes, 550 codificantes)— pero cambia su
papel: **ya no son subrogantes del agente del achaparramiento sino contexto del grupo
16SrI**. Que dos aislamientos de esa especie difieran en 116 kb y en 150 genes sigue
siendo una advertencia útil sobre cuánto se puede extrapolar dentro del grupo `[E]`.

Lo que no cambia es la pregunta de fondo, que R1 ya cerró: no hay maquinaria de RNAi en
mollicutes, de modo que tener el genoma del fitoplasma sirve para contexto y para descartar
off-targets, **no** lo convierte en blanco de silenciamiento `[E]`.

**3. Maize rayado fino virus, `GCF_000862485.2`.** Una secuencia de **6.366 nt**, GC
**61,734 %**, con **2 genes y 2 CDS** anotados (`GeneID:921087` y el siguiente,
`locus_tag` `IM012_gp#`, proteínas `NP_`), que suman 7.350 nt de CDS porque se solapan.
Es el genoma de uno de los dos blancos virales de la planilla de EPILAB y es diminuto: el
espacio de diseño completo cabe en una pantalla.

**4. Maize striate mosaic virus: resuelto.** La ola 1 lo dejó como **NO VERIFICADO**,
sin saber qué taxón ni qué ensamblados le correspondían. La consulta por *Mastrevirus
striatis* devuelve **cuatro ensamblados**, dos de ellos RefSeq, cada uno de **2.746 nt**
`[E]`, que es exactamente el largo que R1 había tomado de la literatura. Bajamos
`GCF_004788335.1`: una secuencia de 2.746 nt, GC **51,384 %**, **4 genes** y **5 CDS**
—cinco porque la replicasa de los mastrevirus se expresa por empalme—, con `GeneID`,
`locus_tag` `QKD23_gp#` y proteínas `YP_`. Que haya dos entradas RefSeq distintas
(`GCF_004788335.1` y `GCF_004130985.1`) del mismo largo es un detalle a mirar antes de
elegir referencia `[?]`: no verificamos cuál corresponde al aislamiento sudamericano.

Y una distinción que importa para el diseño: MSMV es un **virus de ADN** (*Geminiviridae*)
`[E]` `R1 §3.2`. Silenciarlo por RNAi no es silenciar su genoma sino sus transcriptos, y
el blanco efectivo es otro; agrupar los cuatro agentes como si fueran el mismo tipo de
problema molecular sería un error de diseño.

---

## 5. Organismos no objetivo y cicadélidos anotados

Para la contracara de riesgo bajamos un panel de cuatro no objetivo y tres hemípteros
anotados. De los no objetivo bajamos **los transcriptos**, que es lo que consume un
tamizaje de off-target.

| Organismo | Accesión | Rol | Transcriptos | Largo total | GC |
| --- | --- | --- | --- | --- | --- |
| *Apis mellifera* | GCF_003254395.2 | polinizador de referencia | 27.887 | 98.645.700 bp | 40,078 % |
| *Coccinella septempunctata* | GCF_907165205.1 | enemigo natural | 25.480 | 60.783.413 bp | 40,09 % |
| *Chrysoperla carnea* | GCF_905475395.1 | enemigo natural | 19.671 | 42.058.792 bp | 34,659 % |
| *Folsomia candida* | GCF_002217175.1 | fauna del suelo | 42.425 | 108.211.853 bp | 41,634 % |
| *Macrosteles quadrilineatus* | GCF_028750875.1 | cicadélido anotado | 36.629 | 102.705.550 bp | 41,754 % |
| *Homalodisca vitripennis* | GCF_021130785.1 | cicadélido anotado | 33.294 | 91.125.523 bp | 40,513 % |
| *Nilaparvata lugens* | GCF_014356525.2 | hemíptero de referencia en RNAi | 36.412 | 105.612.311 bp | 39,931 % |

De *Apis mellifera* bajamos además el genoma (177 secuencias, **225.250.884 bp** —la
diferencia con el largo declarado es la mitocondria `NC_001566.1` de 16.343 bp—, N50
13.619.445, GC 32,526 %, 0,583 % de N) y su GFF3: **12.356 genes**, 23.471 ARNm, 226.465
CDS, 2,305 transcriptos por gen, anotación *Release 104* de 2018, la más vieja del panel
`[E]`. De los tres hemípteros anotados bajamos también las proteínas: 34.269 de
*M. quadrilineatus* (mediana 450 aa), 31.163 de *H. vitripennis*, 32.453 de
*N. lugens*.

El panel tiene un sesgo que hay que declarar y que ningún archivo corrige: son las
especies **modelo** de cada rol, no las especies del agroecosistema del maíz argentino
`[?]`. *Folsomia candida* es el colémbolo de los ensayos de ecotoxicología; *Coccinella
septempunctata* y *Chrysoperla carnea* son subrogantes de los enemigos naturales locales;
y el maíz es anemófilo, de modo que la exposición real de *Apis mellifera* es por polen y
deriva, no por visita floral. El panel sirve para que el índice de riesgo exista y se
pueda correr; no sirve para afirmar seguridad local.

---

## 6. Qué habilita concretamente este material: dos pruebas que corrimos

### 6.1 Se pueden ubicar genes blanco en el genoma del vector, aunque no esté anotado

Seleccionamos del proteoma RefSeq de *Macrosteles quadrilineatus* (34.269 proteínas) las
que llevan en el nombre la maquinaria de RNAi o las familias de los genes blanco que
importan, y las alineamos con `miniprot` contra el ensamblado de nivel cromosoma del
vector.

**Resultado: 64 de 64 proteínas alinearon, y la mejor alineación de cada una tiene
cobertura 1,00** (`work/W4/ortologos/dmaidis_vs_macrosteles.json`). Entre ellas:

- **Dicer** (`endoribonuclease Dicer`, 3 isoformas) en `OZ319710.1:6.916.199-6.976.983`.
- **Argonauta-2**: 18 isoformas de consulta que resuelven en dos loci distintos, el
  primero en `OZ319711.1:10.478.739-10.512.924`.
- **Exportina-5** en `OZ319706.1:37.480.785-37.527.489`.
- **Bicaudal C** en `OZ319706.1:38.450.054-38.486.911` —la familia del gen `BicC_Dm` de la
  planilla de EPILAB— y **bicaudal D** en otros dos loci.
- **Bursicona** en `OZ319710.1:76.446.012-76.454.926` y **partner of bursicon** en
  `OZ319710.1:54.701.471-54.703.323` —el gen validado por microinyección en el corpus—.
- **Dieciséis subunidades distintas de la ATPasa de protones tipo V**, la familia del
  `ATPaseD_Dm` de EPILAB, cada una en su locus.

Una segunda corrida con los transportadores de captación: **8 de 8** proteínas de la
familia `SID1 transmembrane family member` alinearon con cobertura ≥ 0,98, en tres loci
(`work/W4/ortologos/dmaidis_sid1.json`). Es el aparato de captación sistémica de ARNdc, y
que esté presente en el genoma del vector es relevante para la vía oral `[H]`.

Dos límites de esta prueba, que no son menores. Primero, **la selección fue por nombre en
el proteoma de referencia**, de modo que lo que el cicadélido anotado no tiene anotado, no
se busca: no hay ninguna proteína llamada *ecdysis triggering hormone* en los proteomas de
*M. quadrilineatus*, *H. vitripennis* ni *N. lugens* `[E]`, y sin embargo *eth* es uno de
los dos genes validados experimentalmente en *D. maidis*. Para ese gen el camino es la
accesión de GenBank (PZ371507), no la transferencia de ortología. Segundo, **una
alineación de proteína no es un modelo de transcripto**: da el locus y la estructura
exónica aproximada, no los extremos UTR ni las isoformas, que es lo que haría falta para
elegir una ventana de ARNdc con precisión de nucleótido.

### 6.2 El tamizaje de off-target se puede correr hoy, local, y en segundos

Para medir si el tamizaje es factible con lo que tenemos, tomamos una secuencia
**pública** —los dos CDS del genoma de referencia del MRFV, nunca una secuencia de la
planilla de EPILAB—, derivamos sus **6.067 21-meros únicos** y contamos coincidencias
exactas de 21/21 en las dos hebras contra los seis transcriptomas descargados.

| Transcriptoma | Bases escaneadas | 21-meros con coincidencia exacta | Coincidencias | Segundos |
| --- | --- | --- | --- | --- |
| *Zea mays* | 162.712.215 | **0** | 0 | 9,6 |
| *Apis mellifera* | 98.645.700 | **0** | 0 | 4,5 |
| *Coccinella septempunctata* | 60.783.413 | 3 | 3 | 2,6 |
| *Chrysoperla carnea* | 42.058.792 | 0 | 0 | 1,8 |
| *Folsomia candida* | 108.211.853 | 0 | 0 | 4,7 |
| *Macrosteles quadrilineatus* | 102.705.550 | 1 | 2 | 4,4 |

**575,1 Mb escaneados en 27,6 segundos** con un script propio de 60 líneas y sin índice.
La conclusión operativa: el módulo de tamizaje por semilla de L1 y el conteo de carga de
coincidencias de L3 **son baratos**; el costo del proyecto no está ahí, está en conseguir
los transcriptomas correctos.

Un detalle que vale la pena mirar porque es justamente el argumento de L3. Los tres
21-meros que coinciden en *C. septempunctata* son solapados —`CCTGCCCCAGCTCCAGCTTCA`,
`CTGCCCCAGCTCCAGCTTCAG`, `TGCCCCAGCTCCAGCTTCAGA`—, es decir, **una sola ventana de 23 nt
de identidad exacta** entre un virus de maíz y el transcriptoma de una vaquita, y en
*M. quadrilineatus* hay un 21-mero con dos ocurrencias. Con el criterio binario de
"coincidencia perfecta = riesgo", un diseño sobre esta secuencia pública quedaría marcado
en dos de los seis organismos; el conteo crudo no dice nada sobre la consecuencia, que es
exactamente el hueco que L3 propone llenar ponderando por función del gen impactado `[H]`.

### 6.3 Qué **no** habilita

- **No habilita un transcriptoma del vector listo para usar.** Hay que ensamblarlo desde
  las 23 corridas de RNA-seq. Sin él, el off-target *dentro* del propio vector —el que
  distingue un blanco limpio de uno que pega en veinte genes del insecto— se puede
  aproximar contra el genoma, pero no contra un conjunto de transcriptos.
- **No habilita comparar poblaciones.** Hay dos individuos de origen distinto (Sanger y
  CIAP-INTA) y seis corridas de WGS de PRJNA852223 de 0,37 Gbases en total, que es muy
  poco. Un término de conservación poblacional calculado sobre esto no es poblacional
  `[?]`.
- **No habilita entrenar nada.** No hay ni una etiqueta de eficacia en el material
  genómico. Lo que decide L4 no está acá y no va a estar.
- **No habilita afirmar seguridad para los no objetivo locales.** El panel es de especies
  modelo.

---

## 7. Contraste con la ola 1

`research/R2_attention_diseno_arn/datos_disponibles.md` fue escrito a ciegas el 16 de
octubre. Lo revisamos entero contra lo que bajamos.

**Lo que se confirma, y conviene decirlo porque fue la apuesta central:** los tres
ensamblados del vector existen y **ninguno está anotado**; no hay TSA de la especie; el
transcriptoma de Xu et al. no está depositado de forma descargable; *S. kunkelii* es el
único agente del complejo con genoma completo y anotado desde el principio; el maíz B73 es
la única referencia RefSeq del cultivo; *Apis mellifera* y los dos cicadélidos anotados
están donde la ola 1 dijo.

**Lo que cambió o se corrige:**

| Punto | Ola 1 (16-10-2026) | W4 (17-10-2026, medido) |
| --- | --- | --- |
| Corridas públicas de *D. maidis* en SRA | "20 corridas de RNA-seq en 5 BioProjects" | **37 corridas en total**: 23 de RNA-seq (110,1 Gbases, 6 BioProjects) y 10 de WGS (129,8 Gbases) `[E]` |
| GCA_975739785.1 | "499 contigs" | 499 contigs **y 140 scaffolds**; el FASTA trae 141 secuencias porque incluye la mitocondria `[E]` |
| GCA_975739835.1 | "8.928 contigs" | 8.928 contigs **en 7.864 scaffolds**; y es un haplotipo parcial: 55,89 % de ortólogos ausentes `[E]` |
| Calidad relativa de los ensamblados del vector | las tres filas en pie de igualdad | **97,7 % contra 68,8 % de completitud**: el de Sanger es la referencia y el del CIAP-INTA es complemento `[R]` |
| MSMV | "NO VERIFICADO", taxón sin confirmar | *Mastrevirus striatis*, **4 ensamblados**, 2 RefSeq de 2.746 nt, uno descargado y medido `[E]` |
| Fitoplasma del achaparramiento | "no se verificó que alguno de estos aislamientos sea el del achaparramiento" | El taxid 202462 es **'*Candidatus* Phytoplasma zeae'** y tiene **dos ensamblados** del mismo genoma completo (ASM171287v1, 2016); bajamos y medimos `GCF_001712875.1`: 576.118 bp, GC 28,462 %, 565 genes `[E]` |
| Anotación de *S. kunkelii* | "FASTA + GFF (RefSeq, anotado)" | anotación **renovada el 13-12-2025**, 1.951 genes declarados, 1.814 `gene` + 137 `pseudogene` en nuestro conteo `[E]` |
| Cicadellidae | "55 ensamblados" | **58** `[E]` |
| *Dalbulus elimatus* | no mencionado | `GCA_976225285.1`, **nivel cromosoma**, 1.015.357.212 bp, sin anotación: el control de especificidad congenérico `[E]` |

**Dónde la ola 1 fue más precisa que nosotros:** su tabla incluía licencias por recurso y
el detalle del material suplementario de los papers de eficacia, que W4 no reproduce.

No encontramos ninguna contradicción entre el corpus oficial y la literatura pública en
materia genómica: el corpus, en esta sección, **no afirma nada** sobre genomas: sólo
remite al NCBI.

---

## 8. Limitaciones y lo que no se ejecutó

- **No se corrió BUSCO ni compleasm oficiales.** `compleasm` de Bioconda no resuelve en
  este equipo: pide `dendropy <4.6` y arrastra `sepp`, que pide `dendropy >=5.0.8`; el
  paquete tampoco está en PyPI. Se implementó el proxy con `miniprot`, con umbrales
  declarados, y se calibró contra el 68,6 % publicado del ensamblado del CIAP-INTA.
- **No se descargó el genoma de *Dalbulus elimatus***, ni los 190 ensamblados restantes de
  maíz, ni los 55 ensamblados de Cicadellidae que no entraron al panel, ni los otros cinco
  de *'Ca.* Phytoplasma asteris'. Están inventariados por metadatos en
  `work/W4/ncbi_datasets_metadatos.json`, sin métricas propias.
- **No se ensambló el transcriptoma de *D. maidis***. Está fuera del alcance de W4: es la
  tarea que W4 identifica como camino crítico, no la que ejecuta.
- **No se bajaron lecturas crudas de SRA** (los 240 Gbases del conjunto): sólo metadatos
  por corrida.
- **No se evaluó contaminación** en los ensamblados del vector (simbiontes como
  *'Candidatus* Sulcia muelleri' y *'Ca.* Nasuia', que en cicadélidos suelen aparecer en
  los ensamblados). Haría falta un tamizaje taxonómico de contigs, que no corrimos; el
  número de secuencias cortas del borrador del CIAP-INTA lo hace especialmente relevante
  `[H]`.
- **Las secuencias de EPILAB no se usaron en ninguna corrida de W4**, por la regla de
  confidencialidad: el ejemplo de tamizaje usa los CDS públicos del MRFV.
- **Error de nomenclatura corregido, y vale como advertencia de método.** La primera
  versión de este reporte afirmó que el agente del achaparramiento rojo no tenía genoma,
  porque la consulta usó el nombre común (*maize bushy stunt phytoplasma*) en lugar del
  taxid. El taxón existe como '*Candidatus* Phytoplasma zeae' (taxid 202462) y tiene
  genoma completo desde 2016. Conclusión operativa para todo el equipo: **las consultas
  al NCBI por nombre común pueden devolver cero sin que eso signifique ausencia**; hay
  que resolver el taxid primero. `scripts/01_consulta_ncbi_datasets.py` consulta ahora
  también por taxid.
- Los conteos de genes propios y los declarados por NCBI difieren un poco (en maíz, 44.680
  `gene` + 5.222 `pseudogene` = 49.902 contra 49.888 declarados): son convenciones de
  conteo distintas sobre el mismo GFF3, no un error de descarga.

---

## 9. Cruce con las líneas de ataque de la ola 1

El detalle está en `viabilidad_lineas.md`, con una tabla de datos requeridos por línea y
un veredicto por línea. El resumen:

- **L1 — tamizaje multiobjetivo con incertidumbre: viable con lo que hay.** Los dos
  insumos que dependían de datos genómicos —transcriptoma de maíz para el off-target en el
  cultivo y acceso al genoma del vector— están descargados y medidos. El término de
  off-target *dentro* del vector corre contra el genoma mientras no haya transcriptoma.
- **L2 — validación retrospectiva: viable con lo que hay.** No depende de genomas; su
  insumo es literatura curada a mano, y las cuatro accesiones de ARNm del trabajo del
  corpus están verificadas.
- **L3 — mapa de riesgo ponderado: viable sumando dos cosas que no son genómicas.** El
  panel de transcriptomas no objetivo está bajado y el tamizaje corre en segundos; faltan
  las etiquetas de esencialidad (iBeetle-Base) y la ortología que las transfiera.
- **L4 — ajuste fino de un modelo fundacional: inviable, y el material genómico no la
  mueve.** El problema de L4 nunca fueron los genomas sino las etiquetas de eficacia en
  hemípteros, y en el NCBI no hay ninguna.

---

## 10. Preguntas para el investigador

1. ¿El EPILAB tiene un transcriptoma de *D. maidis* ensamblado y anotado que no esté
   público? Es el único insumo que nos falta y cambiaría el plan de trabajo.
2. ¿Sobre qué referencia se eligieron las regiones de la planilla —`BicC_Dm` 264-563 y
   `ATPaseD_Dm` 151-450—? Si fue un transcriptoma propio, las coordenadas no son
   reproducibles con datos públicos.
3. El único genoma de '*Candidatus* Phytoplasma zeae' es la cepa M3 de 2016. ¿Hay
   aislamientos argentinos secuenciados, publicados o no? Con una sola cepa no se puede
   distinguir variación geográfica en ninguna región candidata.
4. ¿Hay interés en que el equipo ensamble y publique el transcriptoma de referencia del
   vector desde las 23 corridas públicas? Es un entregable reutilizable y nadie lo tiene.
