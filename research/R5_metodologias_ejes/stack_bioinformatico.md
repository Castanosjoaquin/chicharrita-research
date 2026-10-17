# Stack bioinformático para el track de ARN exógeno contra la chicharrita

Tabla de bases de datos y herramientas con para qué sirve cada una, URL, formato
de entrada y salida, y si corre local. "Local" significa una notebook de
estudiante, que acá se toma como 16 GB de RAM, 8 hilos y disco SSD con 100 GB
libres.

> **Correcciones de la ola 2 — 2026-10-17.** Medido contra las bases reales, con
> 409 consultas ejecutadas (`research/ola2/W3_bases_datos/`) y 17 conjuntos
> descargados y medidos (`research/ola2/W4_genomas/`):
>
> - **Hay tres transcriptomas TSA del vector, no uno.** A `GITV00000000` se le
>   suman `GHCC00000000` (55.286 secuencias) y `GCWP00000000` (25.662). Y el
>   conteo de `GITV00000000` es 56.117 según el registro del NCBI, contra las
>   56.116 que esta tabla tomó del artículo `[?]`.
> - **La base Gene no sirve para la especie blanco:** tiene 37 registros de
>   *Dalbulus maidis* y **los 37 son mitocondriales**. Cero genes nucleares. El
>   camino practicable es la ortología desde *Macrosteles quadrilineatus*
>   (`GCF_028750875.1`, 24.178 genes anotados), que esta tabla no registraba.
> - **Genoma anotado no implica genes indexados:** *'Ca.* Phytoplasma zeae' tiene
>   0 registros en Gene pese a sus 581 genes. La anotación sale del GFF3 o de la
>   base protein.
> - **El recurso web Assembly fue retirado** en favor de NCBI Datasets, aunque la
>   base Entrez `assembly` sigue consultable y los comandos de esta tabla no se
>   rompen.
> - **Falta un recurso que esta tabla no tenía y es directamente relevante:**
>   `PRJNA631706`, 16 corridas de RNA-seq del vector expuesto al MRFV contra
>   naive, a 4 h y 7 días.
>
> Ver `research/ola2/CORRECCIONES.md`, entradas H2, H3 y H5.

**Estado de verificación.** Cada URL de esta tabla se abrió en esta corrida
(2026-10-16) salvo donde dice `NO VERIFICADA`, y en ese caso se explica por qué.
Las URL de API se verificaron por uso directo: la consulta corrió y devolvió
datos. Lo que no se pudo abrir también está anotado en
`00_meta/PREGUNTAS_ABIERTAS.md`.

## 1. Bases de datos de secuencia y anotación

| Recurso | Para qué sirve en este proyecto | URL | Entrada | Salida | ¿Local? |
| --- | --- | --- | --- | --- | --- |
| NCBI E-utilities | Buscar y contar qué existe antes de bajar nada: `esearch`, `esummary`, `efetch` sobre `assembly`, `sra`, `nuccore`, `taxonomy`. Es la forma auditable de responder "¿hay datos?" | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/` (VERIFICADA por uso) | términos de consulta en la URL | XML o JSON | sí, es un HTTP GET |
| NCBI Datasets v2 | Ficha de un ensamblado: nivel, N50, tecnología, BioProject y, sobre todo, **si tiene anotación** | `https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/{ACC}/dataset_report` (VERIFICADA por uso) | accesión GCA/GCF | JSON | sí |
| NCBI Assembly / GenBank | Los tres ensamblados de *D. maidis* (`GCA_975739785.1` cromosómico del Sanger, `GCA_975739835.1` haplotipo alternativo, `GCA_054756405.1` CIAP v1 del INTA), el de *Spiroplasma kunkelii* (`GCA_001274875.1`, completo y anotado), los cuatro de *Candidatus* Phytoplasma asteris y —**corrección del 2026-10-17, el dato se nos había escapado por el cambio de nomenclatura**— el del fitoplasma del achaparramiento arbustivo del maíz, hoy '*Candidatus* Phytoplasma zeae' (TaxId 202462): `GCA_001712875.1` / `GCF_001712875.1`, cepa M3, **genoma completo en una sola secuencia**, 576.118 pb, 28,5 % de GC, Illumina MiSeq con Velvet 1.2.10, `PRJNA317711`, aislado de un *D. maidis* colectado el 29/05/2013 en Piracicaba (São Paulo, Brasil); 544 genes y 485 codificantes en la anotación de 2016, 581 y 524 en la reanotación de RefSeq del 07/06/2026. Los tres genomas nuevos de Pellegrinetti et al. 2026 (`PRJNA1294367`) **no devuelven ensamblados en `db=assembly`** al 2026-10-17: buscarlos por BioSample | `https://www.ncbi.nlm.nih.gov/datasets/genome/` (la página HTML **NO VERIFICADA**: no renderiza sin JavaScript; se usó la API de arriba) | accesión | FASTA genómico, GFF3 cuando hay anotación | descarga sí; el genoma de 972 Mb ocupa ~1 GB sin comprimir |
| NCBI SRA | Las lecturas crudas: 37 corridas de *D. maidis*, 23 de ellas RNA-Seq | `https://www.ncbi.nlm.nih.gov/sra` (verificada por E-utilities, no por HTML) | accesión SRR/ERR | FASTQ vía `fasterq-dump` | la descarga sí; una corrida de RNA-Seq de 20 M de lecturas son ~5 GB |
| TSA (Transcriptome Shotgun Assembly) | **El atajo del proyecto**: el transcriptoma ensamblado de *D. maidis*, 56.116 transcriptos, accesión `GITV00000000` | se descarga por NCBI nuccore / `efetch` con la accesión (VERIFICADA la accesión en el paper de Xu et al. 2021) | accesión | FASTA de transcriptos | sí, son decenas de MB |
| Repositorio institucional del INTA | El ensamblado `Dalbulus_CIAPv0.1` en `.fasta` más las métricas, declarado "versión actualizable". **Licencia CC BY-NC-SA**, o sea no comercial | `https://repositorio.inta.gob.ar/xmlui/handle/20.500.12123/18043` (VERIFICADA) | — | FASTA, DOCX | sí |
| Ensembl Plants (FTP) | Genoma, modelos de genes y ortologías de *Zea mays*, para el tamizaje de off-target en el cultivo | `https://ftp.ebi.ac.uk/ensemblgenomes/pub/plants/current/` (VERIFICADA: listado con `fasta/`, `gff3/`, `gtf/`, `compara/`, `variation/`) | — | FASTA, GFF3, GTF | descarga sí; el transcriptoma de maíz indexado para Bowtie entra en una notebook |
| Ensembl Plants (web) | BLAST, BioMart, genómica comparada | `https://plants.ensembl.org/` (**NO VERIFICADA**: redirige a `www.ensembl.org` y la página no entrega texto sin JavaScript) | — | — | — |
| MaizeGDB | Pan-genoma, atlas de expresión y modelos de genes de maíz, complementario a Ensembl Plants | `https://www.maizegdb.org/` (**NO VERIFICADA**: HTTP 403 a nuestro cliente) | — | — | — |
| UniProtKB | Secuencias de proteína revisadas (Swiss-Prot) y no revisadas (TrEMBL) para anotar funcionalmente los blancos candidatos | `https://www.uniprot.org/` (la página **NO VERIFICADA**: devuelve un mensaje de respaldo sin JavaScript). Referencia verificada: UniProt Consortium (2025), *Nucleic Acids Research* 53(D1):D609-D617, doi 10.1093/nar/gkae1010 | FASTA, accesiones | FASTA, TSV, JSON | la API REST sí |
| KEGG | Vías metabólicas y ortología KO, para argumentar por qué un gen blanco es esencial; el genoma de *S. kunkelii* está como `T04056` | `https://www.genome.jp/kegg/` (VERIFICADA). Bases: PATHWAY, KO, GENES, MODULE, BRITE | secuencias (BlastKOALA, GhostKOALA), identificadores (KEGG Mapper) | asignaciones KO, mapas | servicios web; el FTP tiene suscripción (`[?]` los términos exactos no se verificaron) |
| Rfam | Familias de ARN no codificante con modelos de covarianza; sirve para no diseñar contra un ARN estructural conservado y para desambiguar "ARN no codificante" del supuesto S3 | `https://rfam.org/` (VERIFICADA: release 15.1 de enero de 2026, 4.227 familias, búsqueda por secuencia con entrada FASTA) | FASTA | familias, alineamientos semilla, modelos CM | la búsqueda web sí; `cmscan` local también |
| VectorBase / VEuPathDB | Recurso de vectores: BLAST, genomas, popgen | `https://vectorbase.org/` (**NO VERIFICADA**: la app es JavaScript y `www.vectorbase.org/organisms` devolvió HTTP 421). Un paper de actualización de 2022 no lista Cicadellidae entre sus taxones, así que **no asumir que sirve *Dalbulus*** | — | — | — |
| GBIF | Ocurrencias georreferenciadas de *D. maidis*: 610 registros globales, de los cuales **17 en Argentina** | `https://api.gbif.org/v1/occurrence/search?scientificName=Dalbulus%20maidis` (VERIFICADA por uso) | parámetros de consulta | JSON, Darwin Core | sí |
| iNaturalist | Observaciones de ciencia ciudadana: 151 globales | `https://api.inaturalist.org/v1/observations?taxon_name=Dalbulus%20maidis` (VERIFICADA por uso) | parámetros | JSON | sí |

## 2. Herramientas específicas de diseño de dsRNA y tamizaje de off-target

| Herramienta | Qué hace exactamente | URL | Entrada | Salida | ¿Local? |
| --- | --- | --- | --- | --- | --- |
| **dsRIP** (Cedden et al. 2025, *BMC Biology*, CC BY) | Lo más cercano a un estándar actual para insectos: puntúa cada siRNA posible con las cuatro features que resultaron significativas en *Tribolium castaneum* (asimetría termodinámica, autoplegado de la antisentido, GC en posiciones 9–14, adenina en posición 10), elige por ventana deslizante la región de 300 pb del ORF con mejor score medio, y calcula un score de seguridad contando off-targets con los de genes esenciales ponderados 20:1. El módulo de blancos filtra por ortología contra una lista curada de un tamizaje genómico de *T. castaneum*; el de off-target corre Bowtie1 contra transcriptomas del NCBI o subidos por el usuario, con 1 o 2 mismatches | `https://dsrip.uni-goettingen.de/efficiency` (VERIFICADA) | secuencia pegada o FASTA de genes blanco; FASTA de transcriptoma no objetivo opcional | región de dsRNA recomendada, scores de eficacia y seguridad, primers | **no**: es web. Las features sí son reimplementables localmente, y es lo que recomendamos hacer |
| **si-Fi / si-Fi21** (Lück et al. 2019, *Front. Plant Sci.*, CC BY-SA 4.0) | Parte la secuencia disparadora en todos los x-meros (x = largo de siRNA), los alinea con **Bowtie**, elige la hebra guía por reglas de nucleótido terminal y termodinámica (U o A en el 5′, mayor MFE en el 5′, ΔMFE de los tres primeros nucleótidos > 1 kcal/mol) y calcula accesibilidad del sitio blanco con **RNAplfold** de ViennaRNA | `https://sourceforge.net/p/sifi21/` (VERIFICADA la existencia del proyecto). Paper: doi 10.3389/fpls.2019.01023 | FASTA, bases propias en FASTA | tabla de siRNA con eficiencia y off-targets, gráficos | **solo Windows 7+**, GUI Python 2.7 / Qt4. Es el principal problema práctico: en macOS o Linux no corre sin máquina virtual. `[?]` La licencia en SourceForge figura CC BY-NC 2.0 y en el paper CC BY-SA 4.0 |
| dsRNA Analyzer (IMBB-FORTH) | Diseño de dsRNA con foco en seguridad para organismos no objetivo, tamizando candidatos contra bases de no objetivo | `https://dsrna-analyzer.org/` (VERIFICADA la ficha de la herramienta; la página no declara publicación ni formatos) | — | — | no: web |
| dsRNA Specificity App (IMBB-FORTH) | Verifica la especificidad del dsRNA dentro del organismo blanco (que pegue al gen buscado y no a otros del mismo genoma) | `https://bioinformatics.imbb.forth.gr/dsrna-specificity/` (VERIFICADA la ficha) | — | — | no: web |
| **ViennaRNA 2.7.2** | La termodinámica de verdad, que es lo que el supuesto S2 confundía con BLAST: `RNAfold` (MFE y estructura), `RNAplfold` (probabilidades locales de pareo, o sea accesibilidad del sitio blanco), `RNAcofold`, `RNAeval`, `RNAsubopt` | `https://www.tbi.univie.ac.at/RNA/` (VERIFICADA). Cita: Lorenz et al. 2011, doi 10.1186/1748-7188-6-26 | FASTA, secuencia cruda | notación de paréntesis (dot-bracket), ΔG en kcal/mol, perfiles de accesibilidad, PostScript | **sí, holgado**: binarios para macOS Intel y ARM, Linux, Windows, y bindings de Python en PyPI |
| **Bowtie 1** | El alineador que usan tanto si-Fi como dsRIP para el tamizaje de off-target de siRNA de 19–23 nt. Bowtie 1 es el correcto acá: Bowtie 2 está pensado para lecturas largas y no garantiza encontrar todos los alineamientos cortos exactos | `https://bowtie-bio.sourceforge.net/index.shtml` (NO VERIFICADA en esta corrida; la usan si-Fi y dsRIP según sus publicaciones, que sí se verificaron) | FASTA/FASTQ de siRNA; índice de transcriptoma | SAM o listado de hits con mismatches | **sí**: indexar 56.116 transcriptos es cuestión de minutos |
| **BLAST+** (`blastn`, `tblastn`) | Búsqueda de ortólogos y de regiones conservadas; es el precedente metodológico concreto del grupo que publicó RNAi en *D. maidis*, con umbrales explícitos: E-value < 1×10⁻⁴, identidad > 35 %, bit score > 40 % (Andrada et al. 2026) | `https://blast.ncbi.nlm.nih.gov/Blast.cgi` (NO VERIFICADA en esta corrida) | FASTA | tabular (`-outfmt 6`), XML, JSON | **sí**, contra bases propias. Contra `nr` completo, no: usar el servicio web o DIAMOND |
| **OrthoFinder** (GPL-3.0) | Transferir blancos por ortología: si un gen es letal en *Tribolium* o en otro hemíptero, encontrar su ortólogo en *D. maidis*. Es el método que dsRIP usa internamente | `https://github.com/davidemms/OrthoFinder` (VERIFICADA; el desarrollo se movió a `github.com/OrthoFinder/OrthoFinder`) | un FASTA de proteínas por especie | `N0.tsv` y grupos de ortología jerárquicos, ortólogos por par de especies, árboles de genes y de especies | **sí** para un puñado de especies: 80 proteomas de vertebrados corrieron en ~20 h en un escritorio de 4 núcleos y 8 GB con `--core`/`--assign` |

## 3. Cadena de procesamiento de datos crudos

| Herramienta | Paso | URL | Entrada | Salida | ¿Local? |
| --- | --- | --- | --- | --- | --- |
| SRA Toolkit (`prefetch`, `fasterq-dump`) | Bajar lecturas del SRA | `https://github.com/ncbi/sra-tools` (NO VERIFICADA en esta corrida) | accesión SRR/ERR | FASTQ | sí |
| FastQC / MultiQC | Control de calidad de lecturas y reporte agregado | `https://www.bioinformatics.babraham.ac.uk/projects/fastqc/`, `https://multiqc.info/` (NO VERIFICADAS en esta corrida) | FASTQ | HTML, ZIP | sí |
| fastp o Trimmomatic | Recorte de adaptadores y filtrado por calidad | `https://github.com/OpenGene/fastp` (NO VERIFICADA en esta corrida) | FASTQ | FASTQ, HTML, JSON | sí |
| HISAT2 | Mapeo de RNA-Seq contra el genoma de 972 Mb. Se elige sobre STAR por memoria: el índice de STAR para un genoma de ese tamaño no entra cómodo en 16 GB | `https://daehwankimlab.github.io/hisat2/` (NO VERIFICADA en esta corrida) | FASTQ + FASTA genómico | SAM, luego BAM | sí, con paciencia |
| samtools | Conversión, ordenamiento e índices | `http://www.htslib.org/` (NO VERIFICADA en esta corrida) | SAM | BAM, CRAM, BAI | sí |
| StringTie | Ensamblado de transcriptos guiado por el genoma, que es la vía realista para obtener modelos de genes dado que **ningún ensamblado de *D. maidis* tiene anotación en el NCBI** | `https://ccb.jhu.edu/software/stringtie/` (NO VERIFICADA en esta corrida) | BAM | GTF | sí |
| Salmon o kallisto | Cuantificación sin alineamiento contra los 56.116 transcriptos del TSA; es el camino más corto para tener expresión por tejido o condición | `https://combine-lab.github.io/salmon/` (NO VERIFICADA en esta corrida) | FASTQ + FASTA de transcriptos | TSV de abundancias | sí, y es rápido |
| Trinity | Ensamblado *de novo* de transcriptoma. **Se descarta por costo**: la regla práctica es ~1 GB de RAM por millón de lecturas y ~0,5–1 h por millón, y el conjunto de Xu et al. son 1.727 millones de lecturas | `https://github.com/trinityrnaseq/trinityrnaseq` (NO VERIFICADA en esta corrida; la regla es `[R]`, de materiales de taller de UCLA y Cornell que citan Haas et al. 2013) | FASTQ | FASTA de transcriptos | **no**: necesita cluster o nube, y no vale la pena cuando el TSA ya está publicado |
| TransDecoder | Encontrar los ORF en transcriptos, necesario porque dsRIP y la evidencia de Cedden et al. muestran que apuntar al ORF supera a apuntar a las UTR | `https://github.com/TransDecoder/TransDecoder` (NO VERIFICADA en esta corrida) | FASTA de transcriptos | FASTA de péptidos y CDS, GFF3 | sí |
| BUSCO 6.1.0 | Medir completitud de un ensamblado o transcriptoma antes de confiar en él. Referencia de comparación ya verificada: 68,6 % para el borrador del INTA y 82,4 % para el transcriptoma de Xu et al. | `https://busco.ezlab.org/` (VERIFICADA; datasets `odb12.2`, conda y Docker; cita Tegenfeldt et al. 2025, doi 10.1093/nar/gkae987) | FASTA de genoma, transcriptos o proteínas | resumen `short_summary.txt`, tablas | sí |
| Galaxy Europe | Plantea la salida al problema del cluster: entorno web gratuito con BLAST y la mayoría de estos pasos. **Es el que usó el grupo de Catalano en Andrada et al. 2026**, así que es un precedente metodológico del propio problema, no una recomendación genérica. Escala verificada el 2026-10-17 en el paper de actualización del proyecto: los servicios públicos de EE. UU., Australia y Europa acumulan más de 500.000 usuarios registrados y en 2023 más de 11.000 usuarios individuales corrieron en promedio más de 1.000.000 de trabajos por mes, con más de 9.000 herramientas; cada trabajo muestra una estimación de sus emisiones de CO₂ | `https://usegalaxy.eu/` (la URL del servicio sigue NO VERIFICADA por acceso directo). Cita verificada por texto completo: The Galaxy Community (2024), *Nucleic Acids Research* 52(W1):W83, doi 10.1093/nar/gkae410 | FASTA, FASTQ | lo que corresponda al paso | no: es remoto, y por eso resuelve lo que la notebook no puede |

## 4. Formatos que circulan

| Formato | Qué lleva | Dónde aparece en este pipeline |
| --- | --- | --- |
| FASTQ | lecturas con calidad por base | salida del SRA, entrada de QC y mapeo |
| FASTA | secuencias sin calidad | genomas, transcriptos, proteínas, bases de off-target, entrada de ViennaRNA y Bowtie |
| SAM / BAM / CRAM | alineamientos | salida de HISAT2 y Bowtie, entrada de StringTie |
| GFF3 / GTF | coordenadas de genes y transcriptos | anotación; lo que **falta** para *D. maidis* y hay que producir |
| BED | intervalos simples | regiones de dsRNA candidatas sobre el transcripto |
| VCF | variantes | solo si se analiza variabilidad poblacional del sitio blanco, que es un criterio de durabilidad |
| dot-bracket (Vienna) | estructura secundaria y ΔG | salida de RNAfold y RNAplfold |
| Stockholm | alineamiento con estructura consenso | alineamientos semilla de Rfam |
| TSV / CSV | tablas | scores, abundancias, la ficha de decisión de cada candidato |
| JSON | registros estructurados | respuestas de las API del NCBI, GBIF e iNaturalist; la ficha de decisión versionable |

## 5. Qué corre en una notebook y qué no

Corre en una notebook de 16 GB, con holgura: todo el diseño de dsRNA
(ViennaRNA, Bowtie 1 sobre transcriptomas, reimplementación de las features de
dsRIP), BLAST contra bases propias, OrthoFinder sobre menos de diez proteomas,
BUSCO sobre un transcriptoma, cuantificación con Salmon, y todas las consultas a
las API. Esto es importante: **el núcleo del aporte del equipo cabe en una
notebook**, porque el objeto de cómputo son transcriptos de kilobases, no un
genoma de casi un gigabase.

No corre en una notebook: el ensamblado *de novo* de transcriptoma con Trinity
sobre los 1.727 millones de lecturas de Xu et al.; la anotación estructural
completa del genoma cromosómico de 972 Mb con un pipeline tipo BRAKER; el mapeo
de las 23 corridas de RNA-Seq contra ese genoma dentro del plazo del evento. Los
tres tienen la misma salida: no hacerlos. El transcriptoma ensamblado ya está
publicado con accesión `GITV00000000`, y para lo que el proyecto necesita —
elegir regiones blanco y tamizar especificidad — un transcriptoma con 82,4 % de
completitud BUSCO alcanza. Si en algún momento hace falta un paso pesado, la vía
es Galaxy Europe, que es gratis y es lo que usó el grupo que publicó RNAi en
esta especie.


---

## 6. Ampliación del 2026-10-17

Esta sección se agregó al escribir `REPORT.md`, cuando la ampliación de fuentes
dejó tres cosas que la tabla de la primera corrida no tenía. Se escribe acá, y no
reemplazando las tablas de arriba, para que quede visible qué se supo después.

### 6.1 Herramientas y recursos nuevos

| Recurso | Para qué sirve en este proyecto | URL / cita | Entrada | Salida | ¿Local? |
| --- | --- | --- | --- | --- | --- |
| **dsRNAEngineer** | Tercera herramienta publicada de diseño de dsRNA, y la única que declara su arquitectura: front-end en Vue.js, back-end en Sanic, visualización con Canvas API. Trae **942 transcriptomas** del NCBI precargados (plagas de insectos, ácaros, nematodos, hongos y especies de evaluación de seguridad) y agrega la función *screen-target*, que busca una región conservada que sirva de blanco común a varias plagas, con ventana deslizante de 50 a 100 pb. Su lección para nosotros es de arquitectura: el valor está en los transcriptomas precargados, no en la interfaz | `https://dsrna-engineer.cn/` (NO VERIFICADA: no se abrió el servicio). Preprint verificado por texto completo: bioRxiv 2024.07.22.604585. `[?]` La versión revisada por pares figura en el índice de búsqueda (*Trends in Biotechnology*) pero no se abrió | secuencia del gen blanco | regiones recomendadas, análisis on/off/multi/screen-target | no: es web |
| **Script de off-target de la EFSA** | Implementa el conjunto de reglas de la guía de 2025 para reportar transcriptos off-target de cada ARN pequeño de 21 nt: hasta cuatro mismatches sin hueco o tres más un hueco, G:U como medio mismatch, un solo hueco de un nucleótido, nada en las posiciones 10 u 11, no más de dos mismatches en los primeros 12 nt del 5′, y cociente de energía libre del dúplex sobre el del complemento perfecto mayor que 0,75. **Bowtie con 0 a 2 mismatches no evalúa nada de eso salvo los mismatches**, así que los dos tamizajes no son intercambiables | Declarado en EFSA (2025), *EFSA Journal* 23:e9321, doi 10.2903/j.efsa.2025.9321, con repositorio propio de la agencia (URL citada en la guía; no se abrió el repositorio) | secuencia consulta, transcriptomas | transcriptos off-target que cumplen las reglas | sí: la guía dice que corre en el entorno que elija el usuario y no depende de ninguna base de la agencia |

### 6.2 La cadena de genómica bacteriana, con un precedente en este patosistema

Pellegrinetti et al. (2026) reconstruyeron genomas de fitoplasma a partir de
tejido de insecto y de planta con una cadena enteramente de software libre, y es
el molde a copiar si alguna vez hace falta ensamblar un patógeno del complejo:
**fastp** v0.23.4 para recorte, **KrakenTools** v1.2 para remover lecturas del
hospedador (incluidas las del propio *D. maidis*), **MEGAHIT** v1.1.4 y
**MetaSPAdes** v4.1.0 corridos en paralelo para comparar desempeño, **BLASTn**
contra el genoma M3 ya publicado para identificar los contigs del fitoplasma,
**RagTag** v2.1.0 para andamiaje, **Pilon** v1.23.0 para pulido, **CheckM** y
**CheckM2** para completitud y contaminación, **Bakta** v1.11.3 para anotación y
el flujo pangenómico de **Anvi'o** v8 para la comparación. Todo eso corre en una
notebook cuando el objeto es un genoma de menos de un megabase; lo que no corre
en una notebook sigue siendo el genoma de 972 Mb del insecto.

### 6.3 Qué quedó corregido de la primera corrida

Dos cosas. La fila de Galaxy Europe tenía la cita sin verificar y ahora está
verificada por texto completo, con la escala del servicio. Y la fila de NCBI
Assembly afirmaba implícitamente que el único patógeno del complejo con genoma
completo y anotado era *Spiroplasma kunkelii*: no lo es, y el error venía de
buscar por el nombre informal "maize bushy stunt phytoplasma" en lugar del taxón,
que recién recibió nombre formal en 2026.
