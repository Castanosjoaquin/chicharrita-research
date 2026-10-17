# Notas de trabajo R5 — evidencia verificada, con cómo se verificó

Fecha de verificación: 2026-10-16. Todo lo de acá se abrió con `WebFetch` o se
consultó por API en esta corrida. Lo que no se pudo abrir está marcado
`NO VERIFICADO` y replicado en `00_meta/PREGUNTAS_ABIERTAS.md`.

## A. Qué datos existen hoy para los seis organismos del sistema

Consultas hechas contra las E-utilities del NCBI y la API `datasets v2alpha`,
que devuelven texto plano y por lo tanto son auditables (la URL exacta queda en
`sources.json`).

### A.1 *Dalbulus maidis* (vector) — hay más de lo que el equipo suponía

Tres ensamblados en GenBank (`esearch db=assembly`, Count = 3):

| Accesión | Nombre | Quién | Nivel | Tamaño | N50 contig | Tecnología | Liberado |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GCA_975739785.1 | ihDalMaid1.1 | Wellcome Sanger Institute | cromosoma (10 cromosomas, 140 scaffolds, 499 contigs) | 972.206.121 pb | 5.293.657 (L50 58); N50 scaffold 93.705.284 | PacBio + Arima2 (Hi-C) | 2025-10-26 |
| GCA_975739835.1 | ihDalMaid1.1 haplotipo alternativo | Wellcome Sanger Institute | scaffold | 488.450.451 pb | — | PacBio + Hi-C | 2025-10-26 |
| GCA_054756405.1 | CIAP v1 | IPAVE, CIAP-INTA | contig (22.333 contigs) | 585.210.080 pb | 50.514 (L50 3.255) | ONT MinION, ensamblado con Flye v2.9.1, 20x, 34,5 % GC | 2026-01-26 |

- `PRJEB97791` / `SAMEA117578701` es el BioProject/BioSample del ensamblado
  cromosómico; el estudio de lecturas asociado es `PRJEB96547` ("*Dalbulus
  maidis*, genomic and transcriptomic data", ERP179252), con una corrida HiFi de
  PacBio Revio (ERR15499462, 69.624.384.652 bases) y una de Hi-C en NovaSeq X
  (ERR15500418).
- `PRJNA1120083` / `SAMN41674197` es el del INTA; el subagente verificó además
  que hoy contiene un segundo aislado (`SAMN51875076`, "Arg-2025"), el WGS
  master `JBQVWA000000000` y, como proyecto multiespecie, el genoma del
  endosimbionte *Wolbachia* (`GCA_060295765.1` / `JCCBIV000000000`).
- **Ninguno de los dos ensamblados tiene anotación de genes en el NCBI.** La
  API `dataset_report` no devuelve bloque `annotation_info` para ninguno, y
  `annotation_summary` sobre GCA_975739785.1 devuelve HTTP 404. Esto es la
  restricción metodológica central de la rama de bioinformática: hay genoma,
  no hay modelos de genes.
- Preprint del borrador del INTA: Debat & Fernández, bioRxiv
  10.1101/2024.06.25.600652, posteado 2024-06-30. Reporta `Dalbulus_CIAPv0.1`:
  584.127.104 pb, N50 50.453, 22.107 contigs, **BUSCO 68,6 % completo**
  (modo genoma, `insecta_odb10`, 1.367 BUSCOs), MinION R9.4.1 + SQK-LSK109,
  basecalling con Dorado 0.7.1, Flye v2.9.1 pulido con Medaka. Dice textual que
  "The assembly will be updated continuously whenever additional data is
  available" y comparte el ensamblado por el repositorio institucional
  (`hdl.handle.net/20.500.12123/18043`). No declara accesión WGS ni anotación de
  genes. Licencia del preprint: CC BY-NC-ND 4.0.
- SRA: 37 registros para `Dalbulus maidis[Organism]`, de los cuales **23 son
  RNA-Seq**. Estudios identificados por `esummary`: `PRJNA579843` (Xu et al.
  2021), `PRJNA631706` (Ohio State, respuesta a MRFV a temperatura alta y
  baja), `PRJNA1282137` (Iowa State, viroma, NovaSeq X), `PRJNA505618` (CeBio),
  `PRJNA318849` (John Innes Centre), `PRJNA562189` (Oklahoma State,
  Deltocephalinae), `PRJNA272239` (1KITE).

### A.2 Transcriptoma de referencia utilizable sin laboratorio

Xu J, Willman M, Todd J, Kim K-H, Redinbaugh MG, Stewart LR (2021),
*Microbiology Spectrum* 9:e00612-21, doi 10.1128/Spectrum.00612-21. Abierto.

- 1.727.369.026 lecturas apareadas de ~100 nt, 32 muestras, cada una un pool de
  25 adultos enteros, Illumina HiSeq 2000.
- Recorte y ensamblado *de novo* en CLC Genomics Workbench v11, contigs
  fusionados en Sequencher 5.4.6. **56.116 transcriptos no redundantes ≥200 nt.**
- Anotación por BLASTX/BLASTN contra nr/nt y una base propia de insectos +
  RefSeq; expresión diferencial con DESeq2.
- BUSCO v4.1.1: 1.126/1.367 completos (**82,4 %**), 39 fragmentados (2,9 %).
- Disponibilidad, textual: "Sequence data are stored in the NCBI short sequence
  read (SRA) archive as BioProject PRJNA579843" y "The assembled 56,116
  transcripts were deposited at DDBJ/EMBL/GenBank (accession GITV00000000)".
- Es obra del gobierno de EE. UU., sin copyright en EE. UU. (verificado por el
  subagente en la página de PMC).

Consecuencia práctica: el transcriptoma anotado (82,4 % de completitud BUSCO) es
mejor insumo inmediato para elegir blancos que el genoma cromosómico sin
anotar.

### A.3 Patógenos

- ***Spiroplasma kunkelii*** CR2-3x: `GCA_001274875.1` / `GCF_001274875.1`
  (`ASM127487v1`), enviado por el Beltsville Agricultural Research Center,
  **genoma completo**, 1.514.561 pb, 4 replicones, PacBio, liberado 2015-08-26,
  `PRJNA270865`. Anotación liberada 2015-11-05: **1.760 genes totales, 1.685
  codificantes de proteína, 36 no codificantes, 39 pseudogenes**. Es el único
  patógeno del complejo con genoma completo y anotado.
  `[?]` Las accesiones por replicón (CP010899 para el cromosoma y CP012423/4/5
  para los plásmidos) y la cita Davis et al. 2015 *Genome Announc.*
  3:e01216-15 aparecieron en un resumen de búsqueda; la página de PMC devolvió
  una pantalla de verificación de navegador. **NO VERIFICADO por lectura
  directa**: usar la accesión de ensamblado, que sí se verificó por API.
- ***Candidatus* Phytoplasma asteris**: 4 ensamblados (`esearch db=assembly`,
  Count = 4). `GCF_038505995.1` (778.308 pb, genoma completo, Universität
  Hohenheim, 2024-04-28); `GCF_038396745.1` (662.369 pb, completo, Hohenheim,
  2024-04-21); `GCF_047530585.1` (cepa SPGN, 634.631 pb, contig, University of
  Agricultural Sciences, 2025-02-09); `GCA_030686925.1` (aislado QS2022,
  834.303 pb, completo, Academia Sinica, 2023, excluido de RefSeq por derivar de
  metagenoma). **Ninguno es un aislado de maize bushy stunt de la región**: son
  fitoplasmas del mismo grupo 16SrI, no la cepa del complejo del maíz.
- **MRFV**: existe como taxón (TaxId 59749) y hay 3 registros de nucleótidos
  titulados "complete genome".
- **MSMV**: el nombre que resuelve en la taxonomía del NCBI es **maize striate
  mosaic virus** (TaxId 2025388); 19 registros de nucleótidos para ese
  organismo. El nombre "maize stripe mosaic virus" no devolvió taxón propio en
  la misma consulta. `[?]` Confirmar con el organizador a cuál de los dos se
  refiere la diapositiva.
- **Maíz**: Ensembl Plants sirve el FTP `ensemblgenomes/pub/plants/current/` con
  `fasta/`, `gff3/`, `gtf/`, `compara/`, `variation/`, `mysql/`,
  `species_EnsemblPlants.txt` y `uniprot_report_EnsemblPlants.txt` (verificado
  por listado de directorio). Las páginas HTML de `plants.ensembl.org` y de
  `maizegdb.org` no se pudieron leer (JavaScript y HTTP 403 respectivamente).

## B. RNAi en *D. maidis*: la evidencia publicada que el organizador menciona

El organizador declara "RNAi experimental en *D. maidis*" como evidencia
publicada. Está confirmado y son al menos tres trabajos del mismo grupo
(Catalano y colaboradores), con 21 resultados en Europe PMC para
`"Dalbulus maidis" AND (RNAi OR "RNA interference")`:

1. **Dalaisón-Fuentes LI, Pascual A, Gazza E, Welchen E, Rivera-Pomar R,
   Catalano MI (2022)**, *Pest Management Science* 78(7):3108-3116,
   doi 10.1002/ps.6937, PMID 35442515. Suscripción. Caracterizan los genes
   centrales de la maquinaria de RNAi y prueban la respuesta **por inyección y
   por alimentación** en hembras adultas; el blanco es *Bicaudal C* (*BicC*),
   involucrado en la ovogénesis. Reportan reducción del transcripto **de hasta
   170 veces**, caída de la oviposición y desarrollo alterado de los ovocitos.
   Se presentan como el primer RNAi eficiente en la especie.
2. **Dalaisón-Fuentes LI, Pascual A, Crespo M, Andrada NL, Welchen E,
   Catalano MI (2023)**, *Pesticide Biochemistry and Physiology* 196:105618,
   doi 10.1016/j.pestbp.2023.105618, PMID 37945254. Suscripción. Identifican
   **tres dsRNasas**, con *Dmai-dsRNase-2* la más expresada en intestino medio y
   glándulas salivales; un ensayo *ex vivo* muestra degradación rápida del dsRNA
   por homogenatos de tejido; **silenciar *Dmai-dsRNase-2* mejora la respuesta
   al dsRNA del gen de interés**. Proponen co-entregar dsRNA anti-dsRNasa junto
   al del blanco.
3. **Andrada NL, Crespo M, Baricalla AA, Dalaisón-Fuentes LI, Sterkel M,
   Catalano MI (2026)**, *Frontiers in Insect Science* 6:1811933,
   doi 10.3389/finsc.2026.1811933, PMC13279319. Abierto. Blancos *burs-α*
   (bursicona-α) y *eth* (hormona desencadenante de la ecdisis), por
   **microinyección** en ninfas de quinto estadio recién mudadas, 0,25 µL de
   dsRNA a 500 ng/µL (≈125 ng por ninfa), n = 40 por tratamiento, control
   ds-*βlac*. Knockdown por RT-qPCR al día 4: **~95 % para *burs-α* y ~90 % para
   *eth***. Supervivencia: ds-*burs-α* cae a **10 %**, con 77,5 % de alas sin
   expandir o deformes y 12,5 % con restos de exuvia; ds-*eth* impide completar
   la ecdisis y solo ~10 % completa la muda (`[?]` el texto dice 10 % y la
   figura ~15 %). Controles por encima del 95 % de supervivencia.
   Accesiones depositadas: PZ371507 (*eth* de *D. maidis*), PZ371508 (*burs-α*
   de *D. maidis*), PZ371509 y PZ371510 (los de *Delphacodes kuscheli*).
   **Metodología computacional, que es el precedente directo de nuestra rama:**
   transcriptoma propio del laboratorio, **Galaxy Europe**, tBLASTn y BLASTn
   para la especificidad del dsRNA y de los primers con umbrales explícitos
   (E-value < 1×10⁻⁴, identidad > 35 %, bit score > 40 %), ExPASy Translate,
   Primer3plus, Jalview v2.11.5.1 con MAFFT (L-INS-i), BEAST X v10.5.0, Tracer
   v1.7.2, TreeAnnotator, iTOL v6, GraphPad Prism v8.0.2.

Lectura para la rúbrica: el cuello de botella declarado por el organizador —"las
RNasas limitan la entrega oral"— tiene respaldo primario en (2), y el único
blanco con eficacia demostrada **por vía oral** en la especie es *BicC* en (1).
Todo lo de (3) es por inyección, que no es una vía de aplicación agronómica.

## C. Barrera de entrega en Hemiptera: contexto general

- Nitnavare RB, Bhattacharya J, Singh S, Kour A, Hawkesford MJ, Arora N (2021),
  *Frontiers in Plant Science* 12:673576, doi 10.3389/fpls.2021.673576. Abierto.
  Textual: los coleópteros "exhibiting maximum response", los hemípteros son
  "relatively inefficient" y los lepidópteros "show minimum response to RNAi".
  Para hemípteros: respuesta solo moderada "due to the degradation of dsRNA in
  the midgut as well as reduced penetration capability", lo que "requires a high
  dosage of dsRNA to compensate for the degradation". Los dsRNA concluyentes de
  la literatura van de **185 a 675 pb**. Afirma que "even a single base pair
  mismatch would prevent binding to off-targets" `[?]` (contradice el umbral de
  19 nt complementarios que usan las herramientas de tamizaje; ver D).
  Nanopartículas: "Nanoparticles are known to be able to protect the dsRNA from
  nucleases", con citotoxicidad por encima de ciertas concentraciones.
- Zielińska A (2026), *Journal of Plant Protection Research* 66(3):303-317,
  doi 10.24425/jppr.2026.2975, CC BY 4.0. Nombra como desafíos la degradación en
  el tracto digestivo, la captación celular ineficiente y la difusión sistémica
  limitada; evalúa HIGS, SIGS, nanovehículos, formulaciones biodegradables y
  expresión transplastómica. No menciona *Dalbulus* en el cuerpo; sí cita
  trabajos en *Euscelidius variegatus* y *Scaphoideus titanus* en las
  referencias (línea pendiente, ver `PREGUNTAS_ABIERTAS.md`).

## D. Herramientas de diseño y su evidencia

- **si-Fi / si-Fi21** — Lück S, Kreszies T, Strickert M, Schweizer P, Kuhlmann M,
  Douchkov D (2019), *Frontiers in Plant Science* 10:1023,
  doi 10.3389/fpls.2019.01023. Parte la secuencia disparadora en todos los
  x-meros posibles, con x = largo de siRNA elegido, y los alinea con **Bowtie**
  ("chosen because of its accuracy, speed, and memory efficiency"). Selección de
  hebra guía por reglas de nucleótido terminal y termodinámica: U o A en el
  extremo 5′, mayor MFE en el 5′ que la hebra opuesta, ΔMFE de los primeros tres
  nucleótidos > 1 kcal/mol; textual, "the strand with the lower stability (high
  MFE) at its 5'-end is selected as a guide strand". La accesibilidad del sitio
  blanco se calcula con **RNAplfold de ViennaRNA 2.0** (umbral por defecto 0,1,
  u = 8). Dos modos: alta sensibilidad (solo reglas de hebra, para off-target) y
  alta eficiencia (suma accesibilidad, para diseño). Bases propias en FASTA,
  uso offline. **Solo Windows 7+, GUI en Python 2.7, Qt4/PyQt4.** Licencia
  CC BY-SA 4.0. `[?]` SourceForge declara CC BY-NC 2.0: verificar antes de
  reusar código.
- **dsRIP** — Cedden D, Güney G, Rostás M, Bucher G (2025), *BMC Biology*
  23(1):114, doi 10.1186/s12915-025-02219-6, PMC12039203, CC BY. Probaron 31
  siRNA de 21 nt contra *Tc-gawky* en *Tribolium castaneum* (29 entraron al
  modelo de Cox, 20 larvas por grupo; bioensayos de dsRNA con 25 larvas).
  **Cuatro de nueve features resultaron significativas (P < 0,05): asimetría
  termodinámica, energía de autoplegado de la antisentido, contenido GC en las
  posiciones 9–14 de la antisentido y adenina en la posición 10.** El GC **alto**
  en 9–14 se asocia a mayor eficacia, al revés de lo que indican los datos
  humanos. La accesibilidad del mRNA **no** fue significativa (P = 0,41).
  C de Harrell del modelo = 0,76 (IC 95 % 0,73–0,79). El score de siRNA fue el
  predictor más fuerte de la eficacia del dsRNA (razón de riesgo +1,462 por
  unidad, P = 0,003) y apuntar al ORF superó a apuntar a las UTR (+9,91,
  P = 0,011). dsRIP puntúa cada siRNA posible con esas features, usa una ventana
  deslizante para elegir la región de 300 pb del ORF con mejor score medio, y
  calcula un score de seguridad que cuenta off-targets con los de genes
  esenciales ponderados 20:1. El módulo de blancos filtra genes cuyos ortólogos
  están en una lista curada de un tamizaje genómico de *T. castaneum* (Buer et
  al. 2024), con ortología inferida por **OrthoFinder** sobre ~80 especies y
  anotaciones de iBeetle-Base. El módulo de off-target corre **Bowtie1** contra
  transcriptomas de especies no objetivo que el usuario elige del NCBI o sube,
  con 1 o 2 mismatches permitidos.
  Interfaz web verificada: largos de siRNA 19–23 nt (sugiere 20 para algunos
  lepidópteros y 21 para la mayoría de las plagas, p. ej. coleópteros), grupos
  de especies no objetivo (paquete recomendado, polinizadores, enemigos
  naturales, microorganismos, mamíferos, plantas, organismos modelo), opción de
  priorizar off-targets en genes esenciales, y un deslizador eficacia/seguridad
  al 50/50 por defecto.
- **Revisión de herramientas** — Cedden D (2026), *Insect Molecular Biology*
  35(4):364-375, doi 10.1111/imb.70040, PMC13340966, CC BY. Tabla verificada:
  dsRIP (blancos + diseño + off-target; limitación: "Off-target predictions need
  to be experimentally tested" y falta de prueba fuera de coleópteros);
  dsRNAmax y dsRNAEngineer (dsRNA quiméricos multi-especie y co-targeting, sin
  predicción de eficacia, sin considerar la función del gen off-target); dsOMG
  (solo off-target); si-Fi (validado solo en plantas, basado en datos humanos);
  iBeetle-Base (letalidad de un tamizaje genómico en *T. castaneum*, solo esa
  especie); E-RNAi (diseño de dsRNA no disponible desde al menos 2022); dsCheck
  (especies limitadas); DEQOR (no disponible públicamente desde al menos 2022).
  Para off-target, textual: **"the presence of at least 19 complementary
  nucleotides to an off-target transcript is sufficient to flag the siRNA"**.
  Nombra OrthoFinder y FastOMA para transferir blancos por ortología, y BLAST y
  Bowtie para el tamizaje. CleaveLand y PAREsnip son pipelines de miRNA de
  plantas adaptables a degradoma de insectos, aunque faltan herramientas
  específicas. Validación experimental que propone: secuenciación de ARN pequeño
  unido a RISC (muestra qué hebra se carga como guía; en *T. castaneum* ligó la
  relación antisentido/sentido con la letalidad) y degradómica tipo PARE (mapea
  los sitios de corte; en *Psylliodes chrysocephala* identificó un corte clave
  en una subunidad del proteasoma).
- **dsRNA Analyzer** (IMBB-FORTH), `https://dsrna-analyzer.org/`, y
  **dsRNA Specificity App**, `https://bioinformatics.imbb.forth.gr/dsrna-specificity/`.
  La página de herramientas verifica que existen y qué hacen (diseño con foco en
  seguridad para organismos no objetivo, y especificidad dentro del organismo
  blanco), pero **no declara publicación, formatos ni el tamaño de las bases**;
  el conteo de ">90 genomas y >70 transcriptomas" apareció solo en un resumen de
  búsqueda y queda `NO VERIFICADO`.

## E. Insumos para la rúbrica: riesgo, regulación, no objetivo

- **Romeis J, Widmer F (2020)**, *Frontiers in Plant Science* 11:679,
  doi 10.3389/fpls.2020.00679. Abierto. Marco para dsRNA aplicado tópicamente
  sobre artrópodos no objetivo: formulación del problema con metas de
  protección operativas y "pathways to harm"; tres rutas de exposición para
  enemigos naturales (indirecta por presa u hospedador —la más probable—,
  penetración del tegumento, e ingesta durante el aseo, que consideran
  despreciable); separa efectos específicos de secuencia de los no específicos
  (estimulación inmune a dosis altas); y menciona coincidencias de secuencia de
  **al menos 21 nt** como factor. Criterios para elegir especies de prueba,
  tomados de Romeis et al. 2013: sensibilidad ("species should be the most
  likely to be sensitive to the stressor under consideration", y "species
  closely related to the target organism are more likely to be susceptible"),
  relevancia ("representative of valued taxa or functional groups that are most
  likely to be exposed") y disponibilidad ("suitable life-stages of the test
  species must be obtainable in sufficient quantity and quality"). Advertencia
  clave: la homología de secuencia no establece sensibilidad —citan un colémbolo
  con seis coincidencias de 21 nt que no se vio afectado en ensayos de
  alimentación.
- **Ahmad A, Negri I, Oliveira W, Brown C, Asiimwe P, Sammons B, Horak M,
  Jiang C, Carson D (2016)**, *Transgenic Research* 25:1-17,
  doi 10.1007/s11248-015-9907-3, PMC4735227. Abierto. **Autores de Monsanto y
  financiado por Monsanto: hay que declararlo al citarlo.** 14 sitios de campo
  (4 en EE. UU. 2012, 4 en Argentina 2012-2013, 6 en Brasil 2013-2014) con maíz
  MON 87411 (dsRNA DvSnf7). Veinte taxones superaron el criterio de abundancia
  mínima; **nueve aparecieron en al menos dos regiones y cuatro sitios: áfido,
  tijereta depredadora, crisopa, vaquita, chicharrita, chinche pirata, avispa
  parasitoide, escarabajo de la savia y araña**. Sin diferencias significativas
  en 123 de 128 comparaciones de abundancia (96,1 %) y en 53 de 56 de daño
  (94,6 %). Textual: "the data are readily transportable for use in risk
  assessment between these geographic regions", "where the ecological assessment
  endpoints are similar" y con "proper justification". Nota de uso: la
  chicharrita figura entre los nueve taxones representativos, lo que hace a este
  trabajo directamente relevante para el argumento de línea de base regional.
- **EPA (22 de diciembre de 2023)**, registro del ingrediente activo
  **ledprona**, dsRNA pulverizable, contra el escarabajo de la papa de Colorado,
  silenciando el gen de la proteína **PSMB5**. Registro por **tres años**.
  Textual: "the first sprayable dsRNA pesticide in the world allowed to be used
  commercially and sprayed on plants". Declara "no risk of concern to human
  health and the environment" y ningún efecto sobre especies listadas bajo la
  Endangered Species Act; dice haber consultado expertos internacionales **a
  través de la OCDE** sobre riesgo de RNAi. Permiso de uso experimental de mayo
  de 2023 en 10 estados; comentario público en septiembre de 2023; expediente
  `EPA-HQ-OPP-2021-0271`. Lectura para la rúbrica: existe un camino regulatorio
  recorrido para un dsRNA pulverizado sobre un cultivo alimenticio, con un
  precedente de gen blanco del proteasoma.
  `[?]` La guía formal de EFSA para dsRNA no se pudo abrir; lo que hay son
  revisiones que la comentan. Pendiente.

## F. Reproducibilidad: herramientas con fuente

- **nf-core / Nextflow** — Ewels et al. (2020), *Nature Biotechnology*,
  doi 10.1038/s41587-020-0439-x (preprint bioRxiv 610741). Motivación
  verificada: muchos pipelines se construyen para una instalación local y eso
  hace difícil reproducir resultados; los pipelines de nf-core están escritos en
  Nextflow y heredan soporte nativo de Docker y Singularity, con conjuntos de
  datos mínimos de prueba.
- **Snakemake** — Mölder F et al. (2021), "Sustainable data analysis with
  Snakemake", *F1000Research* 10:33, citado por la documentación oficial como el
  paper "rolling" a citar. Define flujos en un lenguaje basado en Python;
  declara el software requerido y lo despliega automáticamente (Conda-Forge y
  Bioconda); genera reportes interactivos y portables que combinan resultados
  con parámetros, código y software.
- **Bioconda** — Grüning B, Dale R, Sjödin A et al. (2018), *Nature Methods*
  15(7):475-476, doi 10.1038/s41592-018-0046-7, PMC11070151.
- **BUSCO** v6.1.0, con datasets `odb12.2` basados en OrthoDB v12.2; acepta
  `-m genome|protein|transcriptome`; paquete de conda e imagen de Docker;
  cita Tegenfeldt F et al. (2025), *Nucleic Acids Research* 53(D1):D516-D522,
  doi 10.1093/nar/gkae987.
- **OrthoFinder** — Emms DM, Kelly S (2019), *Genome Biology* 20:238, y (2015),
  *Genome Biology* 16:157. GPL-3.0. Entrada: un FASTA de proteínas por especie.
  Salidas: `Phylogenetic_Hierarchical_Orthogroups/N0.tsv`, `Orthologues/`,
  árboles de genes, árbol de especies, duplicaciones, estadísticas. Instalación
  recomendada `conda install orthofinder -c bioconda`. Dato de hardware
  verificado y relevante para el alcance: 80 proteomas de vertebrados (~1,7
  millones de secuencias) tardaron **~20 horas en un escritorio de 2015 con 4
  núcleos y 8 GB de RAM** usando `--core`/`--assign`.
- **ViennaRNA** 2.7.2 (29 de diciembre de 2025): incluye RNAfold, RNAplfold,
  RNALfold, RNAalifold, RNAsubopt, RNAcofold, RNAmultifold, RNAeval, RNAplot;
  binarios para Linux, Windows y macOS (Intel y ARM) y bindings de Python en
  PyPI. Cita: Lorenz R et al. (2011), *Algorithms for Molecular Biology* 6:26,
  doi 10.1186/1748-7188-6-26. `[?]` La página no declara licencia.
- **Trinity** — la regla práctica de **~1 GB de RAM por millón de lecturas** y
  **~0,5 a 1 hora por millón de lecturas** aparece en materiales de taller de
  UCLA y de Cornell que citan Haas et al. (2013), *Nature Protocols*
  8:1494-1512. `[?]` No abrimos el paper de *Nature Protocols*: la regla queda
  como `[R]` de material docente. Es suficiente para la decisión de alcance:
  1.727 millones de lecturas implican un orden de magnitud de RAM inalcanzable
  en una notebook y también en una instancia gratuita.
- **DVC**: `dvc add` crea un archivo de metadatos `.dvc` con el hash y la ruta,
  que se commitea a git mientras el dato queda fuera; el dato va al caché
  `.dvc/cache` indexado por hash; `dvc remote add -d`, `dvc push`, `dvc pull`,
  `dvc checkout`, `dvc get`. Backends listados: Amazon S3, NFS, SSH, Google
  Drive, Azure Blob Storage, HDFS, y en la guía también Google Cloud Storage,
  Aliyun OSS, HTTP y WebDAV. `[?]` La página no declara licencia.
- **DOI para el repositorio**: la documentación de GitHub describe el flujo con
  Zenodo —repositorio público, licencia declarada, iniciar sesión en Zenodo con
  GitHub, activar el repositorio en
  `https://zenodo.org/account/settings/github/`, y Zenodo archiva y emite un DOI
  nuevo en cada *release*.

## G. Innovación abierta: antecedentes verificados por el subagente

Resumen de lo que trajo la búsqueda delegada (detalle completo y marcas de
verificación en `REPORT.md`, sección 3):

- **Red Nacional de Monitoreo de *Dalbulus maidis***, 7.º informe (22/10 al
  8/11/2024), `argentina.gob.ar/sites/default/files/2024/08/7mo_informe_red_nacional_de_monitoreo.pdf`,
  VERIFICADO. 426 localidades de Argentina (NOA 74, NEA 77, Litoral 35, Centro
  Norte 77, Centro Sur 163) más 17 de Uruguay; capturas de adultos por localidad
  y por quincena con trampas cromáticas adhesivas. Coalición operadora declarada
  en el documento: AAPPCE, Aapresid, CASAFE, CONICET, CREA, EEAOC, INTA, MAIZAR
  y SENASA; el porcentaje de infección por *Corn Stunt Spiroplasma* lo hace el
  Centro de Bioinvestigaciones UNNOBA-CICBA (CONICET). **Sin licencia declarada,
  sin API, sin CSV: PDF solamente**, y el informe advierte que los datos están
  sujetos a modificación hasta auditar las trampas.
- **Taller de gobernanza de la información de la chicharrita** (Secretaría de
  Agricultura + IICA, septiembre de 2024),
  `argentina.gob.ar/sites/default/files/informe_taller_gobernanza_chicharrita_sep2024.pdf`.
  VERIFICADO PARCIAL: existe en el sitio oficial y se leyó la portada (autora
  Lic. Carina Mazzola); el cuerpo usa fuentes con codificación CID y no es
  extraíble. El contenido se complementó con prensa (bichosdecampo, 16/9/2024,
  VERIFICADA como prensa): participaron INTA, SENASA, INASE, la Comisión Federal
  Fitosanitaria, Maizar, ASA, FADIA, CREA, APRONOR, Aapresid, CASAFE, CIAFA,
  AAPPCE, SRA, Coninagro y CRA; el objetivo era fortalecer el intercambio de
  datos para 2024/25; no hubo compromisos concretos ni se mencionó dato abierto
  ni plataforma compartida.
- **Repositorio institucional del INTA**,
  `repositorio.inta.gob.ar/xmlui/handle/20.500.12123/18043`, VERIFICADO. Ítem
  tipo "Conjunto de datos": "Genoma de *Dalbulus maidis*, la chicharrita del
  maíz, versión actualizable v0.1". Publicado por IPAVE-CIAP-INTA el 04/06/2024.
  Descargables: ensamblado en `.fasta` más dos `.docx` con métricas. Acceso
  abierto. **Licencia CC BY-NC-SA** (`[?]` el pie del sitio dice 2.5 Unported y
  los metadatos del ítem enlazan 4.0). La cláusula NC es un límite real si
  después se quiere licenciar a una empresa.
- **GBIF**, consultado por API:
  `api.gbif.org/v1/occurrence/search?scientificName=Dalbulus%20maidis` devuelve
  **610 registros globales**, repartidos BR 282, US 214, MX 24, CO 23, **AR 17**,
  DO 15, PR 14, CA 2, NI 2, BB 1. **iNaturalist**:
  `api.inaturalist.org/v1/observations?taxon_name=Dalbulus%20maidis` devuelve
  **151 observaciones** globales. (`argentinat.org` devolvió HTTP 403: la home
  queda NO VERIFICADA.)
- **Monitora Oeste** (Brasil), `embrapa.br/monitora-oeste`, descrito en el
  Comunicado Técnico 48 de Embrapa Territorial (septiembre de 2025, autores
  Bogiani, Custódio, Leivas, Takemura),
  `infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1178997/1/6367.pdf`,
  VERIFICADO. Web y app de monitoreo de plagas en el Oeste de Bahía con trampas
  de feromona para *Anthonomus grandis*, datos en tiempo real y alertas;
  "O acesso à ferramenta é gratuito"; "fruto de uma parceria entre a Embrapa
  Territorial e a Associação Baiana de Produtores de Algodão (Abapa)". Los datos
  de trampas los cargan los técnicos de Abapa: el dato crudo queda del lado
  privado.
- **REDAPE**, repositorio de datos de investigación de Embrapa,
  `gov.br/pt-br/servicos/acessar-o-repositorio-de-dados-de-pesquisa-da-embrapa-redape`,
  VERIFICADO. "O acesso é público e gratuito"; no fija licencia única: rigen los
  términos de uso y cada dataset declara sus condiciones. No se encontró ningún
  dataset de plagas de maíz.
- **INTA Vinculación Tecnológica**, `argentina.gob.ar/inta/relaciones/vt`,
  VERIFICADO. Instrumentos nombrados: convenios con empresas, licencia de
  tecnologías del INTA, asistencia técnica a terceros, Empresas de Base
  Tecnológica (con INCUINTA y los Facilitadores de Flujo de Proyectos junto a
  INIS BIOTECH SA, autorizados por ANPCyT), Nodos de Innovación, clusters y
  parques, y gestión de propiedad intelectual. Base pública de convenios en
  `sigec.inta.gov.ar`. Vía de entrada para terceros: "Banco de ideas".
- **CONICET, nota del 5/11/2024** sobre articulación público-privada en
  biotecnología agrícola, VERIFICADA: Apolo Biotech es una Empresa de Base
  Tecnológica fundada por Federico Ariel (IFIBYNE, CONICET-UBA) que desarrolla
  tecnologías basadas en ARN para control de plagas, con la primera planta de
  producción de ARN de América Latina en Santa Fe y 30 empleados. **La nota no
  vincula a Apolo Biotech con la chicharrita ni menciona RNAi.** El proyecto
  conjunto con IABIMO (INTA-CONICET) aparece en prensa NO VERIFICADA.
  Dato de contexto relevante: el organizador del Investigathón es EPILAB ·
  IFIBYNE, el mismo instituto de origen del fundador de Apolo Biotech.
- **Estándares**: Darwin Core, `dwc.tdwg.org`, mantenido por el Darwin Core
  Maintenance Group bajo TDWG, contenido del sitio bajo CC BY 4.0 (la página no
  muestra versión ni la lista de clases). MIAPPE, `miappe.org`, con
  especificación y checklist en `github.com/MIAPPE/MIAPPE`. INSDC,
  `insdc.org`, con DDBJ, ENA y NCBI como miembros. AGROVOC: se abrió pero no
  declara licencia, cantidad de conceptos ni endpoint SPARQL; no citar con
  cifras.
- **No verificados, no citar como existentes**: datos de la red publicados por
  SINAVIMO o SENASA; un dashboard "Alerta Chicharrita" de la Bolsa de Cereales;
  una "Mesa Nacional de Chicharrita" con resolución (lo que hay es un Comité de
  Crisis de la Secretaría de Bioeconomía); el contenido de AgroAPI de Embrapa
  (página JS; el modelo de token pago viene de prensa).
