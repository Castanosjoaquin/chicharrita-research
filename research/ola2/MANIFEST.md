# MANIFEST — corpus oficial del Investigathón (ola 2)

Inventario de `YHat-Biotech/`, hecho el 17 de octubre de 2026 **abriendo cada
archivo**, no leyendo su nombre. Es el insumo de las cinco investigaciones de la
ola 2: cada una recibe la sección que le toca.

**Resumen:** 10 archivos, 61 MB. Siete papers en PDF, un documento de Word con
cuatro enlaces, una planilla de Excel con las secuencias candidatas de EPILAB, y
el PDF de la sesión técnica oficial.

> **Lo que el corpus NO contiene, y nos habían anunciado.** No hay herramientas
> como archivos: ni código, ni binarios, ni notebooks, ni documentación local.
> No hay genomas ni transcriptomas: ningún FASTA, GFF, GTF ni FASTQ. Lo que hay
> en su lugar son **cuatro enlaces** dentro del `.docx`, dos a bases de datos del
> NCBI y dos a herramientas que son servicios web. Esto no es un archivo faltante
> ni un error de copia: es la forma real del corpus, y cambia el alcance de W2 y
> de W4, que trabajan sobre recursos remotos en vez de sobre archivos locales.
> Tampoco hay credenciales, README ni instrucciones de acceso.

**Control de versiones.** El repositorio tiene remoto en GitHub. La planilla de
EPILAB contiene secuencias no publicadas y los PDF son material con derechos de
autor, así que `YHat-Biotech/` y `work/` quedan fuera del control de versiones.
El corpus se cita por ruta; no se copia su contenido a los reportes más allá de
lo mínimo para ilustrar un punto.

---

## 1. Papers → W1

Siete artículos, todos en PDF y todos abiertos y legibles. Título y autores
tomados del propio documento.

| # | Archivo | Págs | Qué es |
| --- | --- | --- | --- |
| P1 | `YHat-Biotech/Papers/Dcitri.pdf` | 15 | Galdeano, Breton, Spotti Lopes, Falk y Machado. *Oral delivery of double-stranded RNAs induces mortality in nymphs and adults of the Asian citrus psyllid, Diaphorina citri*. Artículo experimental, 2017. Entrega **oral** de ARNdc en un **hemíptero** fitófago de floema, con mortalidad medida en ninfas y adultos. |
| P2 | `YHat-Biotech/Papers/PLD3-4-e00224.pdf` | 15 | Mlotshwa, Xu, Willie, Khatri, Marty y Stewart. *Engineering Maize rayado fino virus for virus-induced gene silencing*. Plant Direct, 2020, doi 10.1002/pld3.224. Construcción de **MRFV** como vector de silenciamiento inducido por virus en maíz. |
| P3 | `YHat-Biotech/Papers/finsc-6-1811933.pdf` | 10 | Andrada, Crespo, Baricalla, Dalaisón-Fuentes, Sterkel y Catalano. *ETH and Burs-α are necessary for the normal molting in Dalbulus maidis and Delphacodes kuscheli*. Front. Insect Sci. 6:1811933, 2026, doi 10.3389/finsc.2026.1811933. RNAi por microinyección en **la especie blanco**. |
| P4 | `YHat-Biotech/Papers/nplants2016207 (1).pdf` | 10 | Mitter, Worrall, Robinson, Li, Jain, Taochy, Fletcher, Carroll, Lu y Xu. *Clay nanosheets for topical delivery of RNAi for sustained protection against plant viruses*. Nature Plants, 2017, doi 10.1038/nplants.2016.207. El trabajo original de **BioClay**. |
| P5 | `YHat-Biotech/Papers/s00299-010-0911-z.pdf` | 8 | Gan, Zhang, Jiang, Jiang, Zhu y Cheng. *Bacterially expressed dsRNA protects maize against SCMV infection*. Plant Cell Reports, 2010. ARNdc producido en bacteria, aplicado a **maíz** contra un virus. |
| P6 | `YHat-Biotech/Papers/s10340-023-01670-0.pdf` | 13 | Rossi, Ottati, Bucci, Fusco, Abbà, Bosco, Marzachì y Galetto. *Lab-scale method for plant-mediated delivery of dsRNAs to phloem-feeding leafhoppers*. Journal of Pest Science 97:455-467, 2024, doi 10.1007/s10340-023-01670-0. Entrega de ARNdc **mediada por planta** a **cicadélidos** de floema. |
| P7 | `YHat-Biotech/Papers/s12298-024-01500-2.pdf` | 12 | Balassa, Balassa, Almási, Visnovitz y Rudnóy. *Detection of exogenous siRNA inside sweet corn bundle sheath cells and the RNAi dynamics in the early stage of Maize dwarf mosaic virus infection*. Physiol. Mol. Biol. Plants 30(8):1265-1276, 2024. siRNA exógeno **dentro de células de maíz**, con su dinámica temprana. |

**Nota para W1, y es importante.** Tres de estos siete resuelven pendientes que
la ola 1 dejó anotados en `00_meta/PREGUNTAS_ABIERTAS.md`: P6 es del grupo cuya
evidencia de RNAi en cicadélidos vectores de fitoplasmas no se había podido
abrir; P4 y P5 se habían citado a través de una revisión, sin el original. El
corpus no trae el trabajo de dsRNasas en *D. maidis* (PubMed 37945254), que
sigue pendiente.

Ningún paper del corpus es de aprendizaje automático ni de modelado
computacional: el corpus es experimental y metodológico.

## 2. Sesión técnica oficial → W1 (contexto)

| Archivo | Págs | Qué es |
| --- | --- | --- |
| `YHat-Biotech/Sesion_tecnica_Investigathon_60min_v2.pptx.pdf` | 17 | Presentación del organizador, *La chicharrita del maíz: un desafío de diseño y validación con ARN*, EPILAB · IFIBYNE (UBA-CONICET). Autor del archivo según sus metadatos: **Johan Rodríguez**. |

**Es idéntico al que ya teníamos** (mismo MD5, `7baa0f16901188f2df9c9c36f864296a`,
que el archivo de la raíz del repositorio) y ya está transcrito en
`docs/sesion-tecnica-EPILAB-notas.md`. No hace falta volver a extraerlo: usar la
transcripción, y recurrir al PDF sólo para verificar una diapositiva puntual.

## 3. Enlaces a bases de datos → W3

| Archivo | Qué es |
| --- | --- |
| `YHat-Biotech/Links de interes.docx` | Documento de Word de 7.245 bytes, siete párrafos. Contiene **cuatro enlaces**, bajo tres rótulos. No trae credenciales, instrucciones de acceso ni texto explicativo más allá de los rótulos. |

Contenido completo, transcrito:

| Rótulo en el documento | Enlace |
| --- | --- |
| Database general de genes | `https://www.ncbi.nlm.nih.gov/` |
| Genomas y transcriptomas disponibles | `https://www.ncbi.nlm.nih.gov/datasets/genome/` |
| Herramientas de diseño y verificación de off targets | `https://www.dsrna-engineer.cn/` |
| Herramientas de diseño y verificación de off targets | `https://blast.ncbi.nlm.nih.gov/Blast.cgi` |

Los dos primeros son el insumo de W3; los dos últimos, el de W2. Que el
organizador agrupe dsRNA-Engineer y BLAST bajo el mismo rótulo —«diseño y
verificación de off targets»— es, en sí mismo, un dato para el supuesto S2 y hay
que analizarlo, no darlo por obvio.

## 4. Herramientas → W2

**No hay archivos de herramientas en el corpus.** Lo que hay son los dos enlaces
de la sección anterior:

| Herramienta | URL | Qué habrá que determinar |
| --- | --- | --- |
| dsRNA-Engineer | `https://www.dsrna-engineer.cn/` | Si corre sólo como servicio web o tiene código disponible; qué algoritmo de diseño y de tamizaje usa; qué transcriptomas tiene precargados. |
| NCBI BLAST | `https://blast.ncbi.nlm.nih.gov/Blast.cgi` | Qué calcula exactamente y qué no; si conviene y se puede correr la versión local (BLAST+). |

Dos consecuencias operativas, que W2 tiene que respetar y declarar:

1. **Las secuencias de EPILAB no se suben a ninguno de los dos.** Si hace falta
   un ejemplo de corrida, se usa una secuencia pública de referencia, y la
   limitación se documenta.
2. Lo que se pueda correr **local** se corre local: BLAST+ se instala desde
   Bioconda. Lo que sólo exista como servicio web se marca como no ejecutado,
   con el motivo.

## 5. Genomas y transcriptomas → W4

**No hay ningún archivo genómico en el corpus.** Ni FASTA, ni GFF, ni GTF, ni
FASTQ, ni índices. El único recurso es el enlace a NCBI Datasets
(`https://www.ncbi.nlm.nih.gov/datasets/genome/`).

Esto es el titular del reporte de W4 y conviene decirlo en su primera página: el
material genómico no viene con el corpus, hay que traerlo del NCBI, y por lo
tanto el inventario de W4 es un inventario **de lo que se puede obtener**, con
sus métricas calculadas sobre lo que efectivamente se baje. Los organismos que
importan son *Dalbulus maidis*, *Zea mays*, los cuatro patógenos del complejo y
los no objetivo de referencia. En la ola 1 se registró que los ensamblados del
vector existen **sin anotación de genes**; verificarlo contra el estado actual
del NCBI es parte del trabajo.

## 6. Secuencias de EPILAB → W5

| Archivo | Qué es |
| --- | --- |
| `YHat-Biotech/Sequences_EPILAB.xlsx` | Planilla de Excel de 11.617 bytes, una hoja, ocho columnas y **cuatro filas de datos**. Trae metadatos ricos: organismo, gen, función, secuencia completa, número de siRNA eficientes por gen, secuencia elegida para RNAi y posición dentro del gen. Celdas combinadas en la columna de organismo (filas 2-3 y 4-5) y en el encabezado de posición. |

Estructura verificada, con los largos y el contenido GC calculados por nosotros
sobre las secuencias de la planilla:

| Organismo | Gen | Función | Secuencia completa | siRNA eficientes | Región elegida | Posición |
| --- | --- | --- | --- | --- | --- | --- |
| MRFV | `MP_MRFV` | Movement Protein | 1.263 nt, 63,1 % GC | 114 | 200 nt, 61,5 % GC | 1-200 |
| MRFV | `CP_MRFV` | Capsid Protein | 528 nt, 65,9 % GC | 35 | 200 nt, 65,0 % GC | 200-400 |
| *Dalbulus maidis* | `BicC_Dm` | Bicaudal Protein | 2.520 nt, 51,9 % GC | 199 | 300 nt, 49,3 % GC | 264-563 |
| *Dalbulus maidis* | `ATPaseD_Dm` | ATPase | 491 nt, 46,0 % GC | 33 | 300 nt, 47,0 % GC | 151-450 |

Cuatro cosas que W5 tiene que mirar de entrada, porque reordenan la ola 1:

1. **Estos son los «candidatos preliminares del EPILAB»** sobre los que gira toda
   nuestra propuesta, y que la ola 1 daba por no disponibles. Ya están acá, con
   su región elegida.
2. **No hay ningún candidato dirigido al fitoplasma ni al espiroplasma.** Los
   cuatro apuntan a un virus o al vector, que es exactamente lo que la ola 1
   predijo por la ausencia de maquinaria de RNAi en mollicutes. Es una
   confirmación fuerte y hay que tratarla como tal, no pasarla por alto.
3. **La columna «Nro de eficientes por gen»** implica que ya corrieron un
   tamizaje que clasifica siRNA como eficientes. Averiguar con qué criterio y con
   qué herramienta —presumiblemente dsRNA-Engineer— es la ingeniería inversa más
   valiosa de esta ola, y conecta directamente con W2.
4. **Las secuencias son material no publicado.** No se suben a ningún servicio
   web: ni BLAST del NCBI, ni dsRNA-Engineer, ni servidores de plegado. Todo
   análisis corre local sobre copias en `work/`.

---

## Archivos que no abrieron o están corruptos

Ninguno. Los diez archivos abrieron correctamente: los ocho PDF con `pypdf`, el
`.docx` y el `.xlsx` descomprimidos y parseados desde su XML. El único nombre
engañoso es `Papers/nplants2016207 (1).pdf`, que no declara su contenido en el
nombre pero es el artículo de Nature Plants sobre BioClay.

## Reparto para las cinco investigaciones

| Investigación | Secciones del manifiesto | Material |
| --- | --- | --- |
| W1 papers | 1 y 2 | 7 PDF + la transcripción de la sesión |
| W2 herramientas | 4 (y el rótulo de la 3) | 2 servicios web, sin archivos locales |
| W3 bases de datos | 3 | 2 enlaces al NCBI |
| W4 genomas | 5 | ningún archivo local; NCBI Datasets |
| W5 secuencias | 6 | 1 planilla, 4 candidatos, 8 secuencias |
