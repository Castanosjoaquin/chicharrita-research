# Datos disponibles para un método de priorización de ARNdc contra *Dalbulus maidis*

Estado de verificación: cada fila dice cómo se comprobó. Las accesiones de NCBI se
consultaron por la API de NCBI Datasets v2alpha o por E-utilities el 16 de octubre de
2026; los tamaños son los que devuelve la API. Las filas marcadas **NO VERIFICADO** no
se abrieron y no deben usarse sin comprobarlas.

> **Correcciones de la ola 2 — 2026-10-17.** Este archivo listaba los datos que
> esperábamos necesitar, con lo que se podía verificar sin el material oficial.
> Contrastado contra lo que efectivamente se descargó y se midió
> (`research/ola2/W4_genomas/` y `research/ola2/W3_bases_datos/`):
>
> - Hay **tres** transcriptomas TSA del vector —`GITV00000000`, `GHCC00000000` y
>   `GCWP00000000`—, de modo que el «no existe transcriptoma público» de este
>   archivo es falso y el ensamblado propio deja de ser el camino crítico.
> - Hay **37 corridas SRA** (23 de RNA-seq, 110,1 Gbases; 10 de WGS, 129,8
>   Gbases), no 20.
> - Los tres ensamblados del vector **no son equivalentes**: 97,7 % de
>   completitud el de Sanger, 68,8 % el del CIAP-INTA y 35,5 % el haplotipo
>   alternativo, que no es utilizable como referencia. Ninguno está anotado.
> - El fitoplasma del complejo **sí tiene genoma completo y anotado**
>   (`GCF_001712875.1`, 576.118 pb, 565 genes), descargado y medido.
> - Existe el genoma de *Dalbulus elimatus* (`GCA_976225285.1`), el congénere más
>   cercano, que este archivo no registraba.
> - El cuarto agente, MSMV, **mapea a dos taxones de familias virales distintas**
>   y sigue sin definirse `[?]`.
>
> Detalle en `research/ola2/CORRECCIONES.md`, parte III.

## El hallazgo que condiciona todo lo demás

**Ningún ensamblado genómico público de *Dalbulus maidis* tiene anotación de genes.** Los
tres existen y son descargables; ninguno trae un conjunto de transcriptos. No hay registro
TSA (Transcriptome Shotgun Assembly) de la especie: la búsqueda
`Dalbulus maidis[Organism] AND TSA[Division]` en la base `nucleotide` devuelve 0 `[E]`.
Esto significa que el insumo más básico de cualquier método de diseño o priorización de
ARNdc —la lista de transcriptos del blanco, para calcular eficacia por ventana y para
buscar off-targets en el propio insecto— **hay que construirlo**. Existen 20 corridas
públicas de RNA-seq con las que se puede hacer; es trabajo acotado, no un bloqueo, pero es
el camino crítico del proyecto y la primera tarea que hay que empezar.

## Genoma y transcriptoma del vector

| Recurso | URL | Tamaño | Formato | Licencia | Para qué sirve | Qué falta |
| --- | --- | --- | --- | --- | --- | --- |
| *D. maidis* ihDalMaid1.1, nivel cromosoma, haploide | `https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_975739785.1/` | 972.206.121 bp, 499 contigs, N50 de scaffold 93,7 Mb | FASTA (vía NCBI Datasets o FTP) | Dominio público (INSDC) | Referencia genómica de calidad para mapear off-targets intraespecíficos y para llamar variantes | **Sin anotación.** Wellcome Sanger Institute, BioProject PRJEB97791, liberado 2025-10-26 |
| *D. maidis* ihDalMaid1.1, haplotipo alternativo | `https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_975739835.1/` | 488.450.451 bp, 8.928 contigs | FASTA | Dominio público (INSDC) | Heterocigosis; segundo haplotipo | Sin anotación. BioProject PRJEB97790 |
| *D. maidis* CIAP v1, nivel contig | `https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_054756405.1/` | 585.210.080 bp, 22.333 contigs, N50 50.514 bp | FASTA | Dominio público (INSDC) | Borrador argentino (IPV, CIAP-INTA), BioProject PRJNA1120083 | Sin anotación; muy fragmentado frente al de Sanger |
| RNA-seq de *D. maidis*, 20 corridas Illumina en 5 BioProjects: PRJNA631706 (17), PRJNA318849 (3), PRJNA562189, PRJNA505618 (huevos), PRJNA1282137, PRJNA272239 (454) | `https://www.ncbi.nlm.nih.gov/sra/?term=Dalbulus+maidis%5BOrganism%5D` | No consultado por corrida | SRA / FASTQ | Dominio público (INSDC) | **El insumo clave**: ensamblar *de novo* o guiado por el genoma un transcriptoma de referencia | Hay que ensamblarlo y anotarlo. Metadatos de tejido y condición no se revisaron corrida por corrida |
| Transcriptoma ensamblado de Xu et al. 2021, 56.116 transcriptos, con respuesta a MRFV | `https://pubmed.ncbi.nlm.nih.gov/34817206/` | 1.727.369.026 lecturas de 100 nt pareadas | — | Artículo con muro de pago; datos crudos presumiblemente en SRA | Sería el atajo al transcriptoma anotado | **NO VERIFICADO que el ensamblado esté depositado.** No aparece como TSA. Puede estar sólo como suplemento. Hay que pedirlo o rehacerlo |

## Genomas de los cuatro patógenos del sistema

| Recurso | URL | Tamaño | Formato | Licencia | Para qué sirve | Qué falta |
| --- | --- | --- | --- | --- | --- | --- |
| *Spiroplasma kunkelii* CR2-3x, genoma completo | `https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_001274875.1/` | 1.514.561 bp | FASTA + GFF (RefSeq, anotado) | Dominio público | Único patógeno del sistema con genoma completo **y anotado** | Que el RNAi funcione sobre un molicute sin pared es justo lo que R1 tiene que resolver |
| *Candidatus* Phytoplasma asteris, 3 genomas completos | `https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_038505995.1/` (778.308 bp), `GCF_038396745.1` (662.369 bp), `GCA_030686925.1` (834.303 bp) | 0,66–0,83 Mb | FASTA + anotación | Dominio público | El fitoplasma del achaparramiento pertenece al grupo 16SrI (asteris) | **No se verificó** que alguno de estos aislamientos sea el del achaparramiento del maíz (*maize bushy stunt*). El taxón "maize bushy stunt phytoplasma" tiene taxid 202462; no se consultaron sus ensamblados |
| Maize rayado fino virus (MRFV), genoma de referencia | `https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000862485.2/` | 6.366 bp | FASTA + anotación RefSeq | Dominio público | Virus de ARN+ de transmisión propagativa; blanco directo posible | Diversidad de aislamientos no relevada |
| MSMV (el cuarto agente de la diapositiva del organizador) | — | — | — | — | — | **NO VERIFICADO.** La búsqueda taxonómica por "Maize striate mosaic virus / Maize stripe virus" devolvió los taxid 3052767 y 2025388, sin confirmar cuál corresponde a MSMV ni qué ensamblados tiene. Pendiente para R1 |

## Genomas para el cálculo de off-target

| Recurso | URL | Tamaño | Formato | Licencia | Para qué sirve | Qué falta |
| --- | --- | --- | --- | --- | --- | --- |
| *Zea mays* B73, Zm-B73-REFERENCE-NAM-5.0 | `https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_902167145.1/` | 2.182.075.994 bp | FASTA + GFF, anotación RefSeq `GCF_902167145.1-RS_2025_02` | Dominio público | **Penalidad por off-target en el cultivo que se quiere proteger.** Único genoma de referencia de maíz en NCBI | Los híbridos comerciales argentinos no son B73; la variación de secuencia entre B73 y el germoplasma local no está cuantificada |
| *Apis mellifera* Amel_HAv3.1 | `https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_003254395.2/` | 225.234.541 bp | FASTA + GFF, anotación Release 104 | Dominio público | Polinizador: el organismo no objetivo de referencia obligado en cualquier evaluación de riesgo de ARNdc | Falta el panel de enemigos naturales y de fauna del suelo relevantes en maíz argentino |
| Genomas de Cicadellidae emparentados, 55 ensamblados en total | `https://www.ncbi.nlm.nih.gov/datasets/taxonomy/33349/` | *Homalodisca vitripennis* 2,30 Gb (**anotado**, `GCF_021130785.1`); *Macrosteles quadrilineatus* 1,32 Gb (**anotado**, `GCF_028750875.1`); *Nephotettix cincticeps* 746 Mb; *Matsumurasca onukii* 599 Mb; *Empoasca fabae* 909 Mb | FASTA, algunos con GFF | Dominio público | Dos cicadélidos **con anotación RefSeq**: sirven para transferir anotación por ortología a *D. maidis* y como no objetivo cercano | Ninguno es *Dalbulus*; la distancia filogenética a *D. maidis* no se midió |
| *Nilaparvata lugens*, `GCF_014356525.2` | `https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_014356525.2/` | 1.085.539.448 bp, anotado (Release 101) | FASTA + GFF | Dominio público | Hemíptero con RNAi muy estudiado; referencia para transferir conocimiento dentro del orden | Delphacidae, no Cicadellidae |

## Datos de eficacia de RNAi: lo que se puede usar para entrenar o validar

Esta es la sección que decide si el método se puede validar. La respuesta corta: **sí, pero
con n de dos dígitos y en el orden equivocado de insectos.**

| Recurso | URL | Tamaño | Formato | Licencia | Para qué sirve | Qué falta |
| --- | --- | --- | --- | --- | --- | --- |
| Datos de bioensayo de Cedden et al. 2025 (dsRIP): 31 siRNA individuales en *Tribolium castaneum* con curvas de supervivencia, y 8 genes esenciales × 3–4 regiones de ARNdc con hazard ratios | `https://doi.org/10.1186/s12915-025-02219-6`, Additional file 2 (datos crudos) y Additional file 3 Tabla S1 (scores y hazard ratios) | ~29 siRNA con supervivencia + ~29 ARNdc con hazard ratio | Material suplementario del artículo | **CC BY 4.0** | **El único benchmark cuantitativo de eficacia de ARNdc en insectos con diseño controlado y datos abiertos.** Es el conjunto de validación retrospectiva principal | Coleoptera, no Hemiptera. n pequeño. El propio paper advierte que los parámetros pueden diferir en otros órdenes |
| Scripts de dsRIP y del análisis de sRNA-seq ligado a RISC | `https://doi.org/10.6084/m9.figshare.28156787` (plataforma) y `https://doi.org/10.6084/m9.figshare.27490890.v1` (análisis) | No consultado | Figshare | **NO VERIFICADO** (figshare suele ser CC BY, hay que comprobar cada depósito) | Reimplementar el baseline exactamente y no una aproximación | No se abrieron los depósitos |
| sRNA-seq ligado a RISC de Cedden et al. | `https://identifiers.org/ncbi/bioproject:PRJNA1157760` | No consultado | SRA / FASTQ | Dominio público (INSDC) | Qué siRNA se cargan realmente en RISC: es el mecanismo detrás del score de asimetría | No se consultó el BioProject |
| RNAi publicado en *D. maidis*: Dalaisón-Fuentes et al. 2022 (*Bicaudal C*, inyección e ingestión, reducción de transcripto de hasta 170 veces); Dalaisón-Fuentes et al. 2023 (tres dsRNasas, `Dmai-dsRNase-2`); Andrada et al. 2026 (*burs-α* y *eth*, alta mortalidad) | `https://pubmed.ncbi.nlm.nih.gov/35442515/`, `https://pubmed.ncbi.nlm.nih.gov/37945254/`, `https://pubmed.ncbi.nlm.nih.gov/42328018/` | **6 construcciones de ARNdc en total** | Abstracts abiertos; el de 2026 es acceso abierto (Front. Insect Sci., PMC13279319) | Varía: el de 2026 es CC BY | Única evidencia de eficacia de RNAi en la especie blanco. Permite una prueba de rango dentro del transcripto | n = 6 y sin controles negativos diseñados. **No alcanza para entrenar nada.** Las secuencias exactas de ARNdc hay que extraerlas de las listas de primers de cada paper |
| iBeetle-Base: fenotipos de RNAi en *T. castaneum* a escala genómica. 12.027 ARNdc "eficientes" según la curación de dsRNAPredictor | `https://ibeetle-base.uni-goettingen.de/` | >50% de los genes con fenotipo | Interfaz web + API REST | **NO VERIFICADO.** No se encontró declaración de licencia ni de descarga masiva | El dataset más grande de RNAi en insectos. Es la base de dsRNAPredictor | La etiqueta es binaria y grosera (letalidad ≥20% o cambio fenotípico), con dosis y vía no controladas entre genes. No es una medida de eficacia comparable |
| Datasets de siRNA en células humanas: Hüsken (2.431 siRNA, 34 mRNA, células H1299), Takayuki (702 siRNA, 1 mRNA, HeLa), y el agregado "Mixset"; en total 3.714 siRNA y 75 mRNA en nueve estudios | Compilados por OligoFormer: `https://github.com/lulab/OligoFormer` | 3.714 siRNA | Tablas en el repositorio | **NO VERIFICADO** (no se abrió el repositorio) | Preentrenamiento o calibración de un modelo de secuencia, si se decidiera ir por ahí | Humano, siRNA sintético de 19–21 nt transfectado en línea celular. Cedden et al. demostraron que al menos un parámetro (%GC en posiciones 9–14) **se invierte** entre humano e insecto |
| `siRNAEfficacyDB` y `RNATx-Bench` (>100.000 ARN validados, seis modalidades) | Mencionados en la revisión de NAR GAB `https://academic.oup.com/nargab/article/8/3/lqag099/8776214` | — | — | **NO VERIFICADO** | Benchmarks estandarizados emergentes | No se abrieron. Son de dominio terapéutico humano |

## Datos de conservación poblacional del blanco: el término más débil

El scoring que propone la sección 3 del reporte incluye un término de conservación de la
región blanco entre poblaciones de *D. maidis*, para que un ARNdc no falle por variación de
secuencia. **Los datos para calcularlo bien no existen públicamente.**

| Recurso | URL | Qué hay | Qué falta |
| --- | --- | --- | --- |
| PRJNA852223, seis corridas de WGS Illumina MiSeq de *D. maidis* | `https://www.ncbi.nlm.nih.gov/bioproject/PRJNA852223` | Seis muestras | Profundidad y origen geográfico **no verificados**. Seis muestras no son un estudio poblacional |
| PRJNA780295, captura dirigida con enriquecimiento híbrido anclado | `https://www.ncbi.nlm.nih.gov/bioproject/PRJNA780295` | Una corrida | Es un diseño filogenético, no de variación poblacional en los transcriptos de interés |
| Los tres ensamblados genómicos más las 20 corridas de RNA-seq | ver arriba | Permiten llamar variantes entre un puñado de individuos y entre el aislamiento de Sanger y el de CIAP-INTA | No es una muestra poblacional representativa de las poblaciones argentinas. El término de conservación queda como `[H]`: calculable sobre los individuos disponibles, no interpretable como conservación poblacional |

## Lo que hay que decir sobre lo que falta

Tres ausencias importan, en orden de gravedad.

**Primero, no existe ningún dataset de eficacia de RNAi en Hemiptera con el tamaño y el
control experimental necesarios para entrenar un modelo.** Lo que hay en insectos es
Coleoptera: los 29 ARNdc de Cedden et al. con hazard ratio medido, y los ~12.000 registros
binarios y poco controlados de iBeetle-Base. En la especie blanco hay seis construcciones
publicadas. Cualquier propuesta que diga "entrenamos un modelo de eficacia para *D.
maidis*" es, con los datos públicos de hoy, imposible de cumplir.

**Segundo, no existe un conjunto de transcriptos anotado de *D. maidis*.** Hay que
construirlo desde SRA. Es la primera tarea y la que bloquea al resto.

**Tercero, no existe una base de off-target para organismos no objetivo del agroecosistema
del maíz argentino.** dsRIP resolvió esto para 83 especies por ortología, pero la lista hay
que verificarla y casi con seguridad no incluye a los enemigos naturales ni a los
polinizadores relevantes en la región; la plataforma permite subir transcriptomas, así que
el trabajo es de curaduría, no de método.
