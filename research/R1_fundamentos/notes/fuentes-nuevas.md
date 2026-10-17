# Notas crudas R1 — segunda tanda (fuentes nuevas de esta corrida)

Misma convención que `fuentes-crudas.md`: `[FT]` = leí texto completo;
`[FT-parcial]` = leí resumen, introducción y las secciones que importaban, no el
artículo entero; `[RES]` = leí solamente el resumen. Todo lo de acá se abrió
efectivamente. Los identificadores siguen la numeración del archivo anterior
(que llega hasta S40).

---

## Mecanismo de RNAi: base estructural

**S41 [FT] Wilson RC, Doudna JA (2013). Molecular mechanisms of RNA interference.
*Annu Rev Biophys* 42:217-239. PMC5895182. Manuscrito de autor en PMC.**
- Resumen: los pre-miRNA se procesan primero en el núcleo por Drosha y se
  exportan al citoplasma, donde el corte por Dicer genera miRNA maduros y siRNA.
  "Estos productos de doble cadena se ensamblan con proteínas Argonauta de modo
  que una hebra es preferentemente seleccionada y usada para guiar el
  silenciamiento secuencia-específico de ARNm blanco complementarios por corte
  endonucleolítico o represión traduccional."
- **Dicer como regla molecular**: el dominio PAZ (nombrado por PIWI, Argonaute y
  Zwille) reconoce el extremo de dsRNA característico de los intermediarios de
  RNAi — **saliente de 2 nt en el extremo 3′ y fosfato en el 5′**. "Los dominios
  PAZ y RNasa III actúan juntos como una regla molecular" que fija el largo del
  producto. En la estructura de Dicer de *Giardia intestinalis* el dominio PAZ
  está a **65 Å del centro catalítico**; la distancia entre PAZ y los sitios de
  corte de RNasa III está determinada por la orientación estructural de los
  dominios, y se reordena en otras versiones de Dicer para dar productos de
  largos distintos. Dicer de *Giardia* carece de dominio helicasa; Dcr1 de
  *Kluyveromyces polysporus* carece de PAZ y conserva una sola RNasa III, y aun
  así especifica el tamaño del producto.
- **Carga en RISC**: una vez presentada la hélice de dsRNA a Argonauta, el
  **extremo 3′ lo une el dominio PAZ y el fosfato 5′ el dominio MID**, generando
  el RISC. Las dos hebras son la **guía** y la **pasajera**, y su selección "es un
  determinante clave del silenciamiento que sigue". El complejo transitorio con
  la pasajera aún sin cortar o disociar es el **pre-RISC**.
- **Reconocimiento del blanco**: el RISC hace vigilancia celular y une ARN de
  cadena simple con complementariedad a la guía. Los **nucleótidos 2–6 de la guía
  son la secuencia semilla (seed)** e inician la unión al blanco. La porción
  semilla está típicamente bien ordenada; no se observa densidad electrónica más
  allá de la posición 10 salvo el nucleótido terminal unido a PAZ.
- **Arquitectura de Argonauta**: bilobular; un lóbulo con los dominios N y PAZ,
  el otro con MID y PIWI. La estructura de la Argonauta de *Pyrococcus furiosus*
  mostró que **el dominio PIWI adopta un plegamiento tipo RNasa H**, lo que lo
  implica como dominio catalítico y sitio de la actividad "slicer". El motivo de
  tríada catalítica **DDX** (X = Asp o His) está presente en las Argonautas
  catalíticamente activas y ausente en las que carecen de actividad slicer.
  De las cuatro Argonautas humanas, **sólo Ago2 tiene actividad slicer**.
- Para que ocurra el corte, el extremo 3′ de la guía debe liberarse del dominio
  PAZ: con un blanco de 12 nt el 3′ sigue unido, con uno de 15 nt se libera para
  acomodar la extensión más allá de una vuelta completa (11 nt) de hélice A.
  Mutaciones del dominio PAZ tienen poco efecto en los ensayos de corte, en
  contraste con la pérdida de corte al mutar residuos del dominio MID que
  reconocen el extremo 5′.
- Burbujas (bulges) insertadas en la región semilla **de la guía** impiden el
  corte; en la misma región **del blanco** el corte sí procede.
- Una guía mantenida en conformación helicoidal puede aumentar la afinidad por el
  blanco **hasta ~300 veces**, al reducir el costo entrópico de ordenar la guía
  (calorimetría de titulación isotérmica sobre la proteína de *T. thermophilus*).
- El RISC también puede inducir **represión traduccional no endonucleolítica**,
  antes o después de la iniciación, seguida eventualmente de desadenilación y
  degradación.

**S50 [FT-parcial] Zotti MJ, Wegner J, Farias BF, Smagghe G (2026). Molecular
Ruler Variation in Insect Dicer-2 Suggests a Structural Basis for
Species-Dependent siRNA Length and Antiviral Defense Diversity. *Viruses*
18:285. PMC13030778. OA.**
- Dicer-2 pertenece a la familia RNasa III; estructura modular con dominio
  helicasa, dominio PAZ para reconocer el extremo del dsRNA, dos dominios
  catalíticos RNasa III que forman un centro de corte dimérico, y un dominio de
  unión a dsRNA. Mide una distancia definida desde el extremo unido hasta el
  sitio catalítico.
- **Los largos de siRNA son específicos de orden**: dípteros (*Drosophila
  melanogaster*) y coleópteros (*Tribolium castaneum*) producen principalmente
  **21 nt**; himenópteros (*Bombus terrestris*) y ortópteros (*Locusta
  migratoria*) están enriquecidos en **22 nt**; lepidópteros (*Spodoptera
  exigua*, *Trichoplusia ni*) predominantemente **20 nt**. Los patrones son
  consistentes entre virus distintos y disparadores sintéticos, lo que sugiere
  que el largo lo dicta la maquinaria del hospedador y no el virus.
- Los autores declaran la implicancia aplicada: ajustar la producción de siRNA al
  orden del insecto blanco podría mejorar eficacia y especificidad.
- **El trabajo no reporta el perfil de largo de siRNA de ningún hemíptero.**

---

## La pregunta central: ¿hay RNAi en mollicutes?

**S42 [RES] Kaya E, Doxzen KW, Knoll KR, Wilson RC, Strutt SC, Kranzusch PJ,
Doudna JA (2016). A bacterial Argonaute with noncanonical guide RNA specificity.
*PNAS* 113(15):4057-4062. PMC4839417.**
- Del apartado de significancia: "Las proteínas Argonauta son efectores clave del
  RNA interference **eucariota** y, en procariotas, funcionan en la defensa del
  genoma del hospedador." La Argonauta de *Marinitoga piezophila* asociada a
  CRISPR usa guías de ARN **5′-hidroxiladas** en lugar de las 5′-fosforiladas que
  usan todas las demás Argonautas conocidas.
- Las Argonautas tipo MpAgo identificadas por alineamiento están **todas
  codificadas dentro de loci CRISPR-cas**.
- Nota de honestidad: por esta vía sólo pude abrir el resumen y el apartado de
  significancia, no el cuerpo del artículo. La afirmación fuerte de que bacterias
  y arqueas "carecen de vías de RNAi" aparece en el cuerpo según el buscador,
  pero **no la cito porque no abrí esa parte**. Lo que sí queda citable es la
  separación explícita entre RNAi eucariota y función procariota de defensa del
  genoma.

**D01 [consulta propia, reproducible] UniProtKB / InterPro, 17 de octubre de 2026.**
Pregunta: ¿existen en los mollicutes los dominios proteicos que definen la
maquinaria de RNAi? Consulta vía la API REST de UniProt, contando resultados por
taxón y por dominio InterPro:

```
https://rest.uniprot.org/uniprotkb/search?query=(taxonomy_id:TAXID) AND (xref:interpro-IPRXXXXXX)
```

Dominios: **IPR003165 = PIWI** (dominio catalítico de Argonauta),
**IPR003100 = PAZ** (reconocimiento del extremo del dúplex),
**IPR005034 = dominio de dimerización de Dicer**,
**IPR000999 = dominio RNasa III** (control positivo: es ubicuo en bacterias).

| Taxón (taxid) | PIWI | PAZ | Dicer-dim. | RNasa III | proteínas en UniProtKB |
| --- | --- | --- | --- | --- | --- |
| Mollicutes (31969) | **0** | **0** | **0** | 154 | 126.874 |
| *Spiroplasma* (2132) | **0** | **0** | **0** | 30 | 36.551 |
| *Spiroplasma kunkelii* (47834) | **0** | — | — | 1 | 1.755 |
| *Candidatus* Phytoplasma (33926) | **0** | **0** | **0** | 43 | 24.307 |
| *Zea mays* (4577) | 79 | 66 | 15 | 43 | — |
| Hemiptera (7524) | 284 | 351 | 98 | 143 | — |
| Bacteria (2) | 757 | 8 | 14 | 21.593 | — |

Lectura: el cero no es un cero por falta de datos — hay 126.874 proteínas de
mollicutes anotadas, 1.755 de *S. kunkelii* sola, y el control de RNasa III da
positivo en todos los taxones. Las bacterias **como dominio** sí tienen 757
proteínas con dominio PIWI (las Argonautas procariotas), pero prácticamente
ninguna con PAZ (8) ni con el dominio de dimerización de Dicer (14): no hay un
Dicer bacteriano. Y dentro de Mollicutes el conteo de PIWI es cero.
Esta consulta es nuestra, no de un paper: es verificable en un minuto y es la
evidencia más directa que pudimos construir sobre la ausencia de maquinaria de
RNAi en los dos mollicutes del complejo.

**S44 [FT] Balog A, Hevér L, Csorba AB (2026). Innovative Pest Management
Strategies in Phytoplasma Insect Vectors Control. *Plants* 15:1664.
PMC13259061. OA.**
- Revisión del espacio completo de estrategias contra fitoplasmas. **Todas las
  estrategias que revisa son dirigidas al vector o a la planta: ninguna propone
  silenciar genes del fitoplasma.** El RNAi aparece siempre como "RNAi dirigido a
  la fisiología del vector" o "enfoques de silenciamiento basados en miRNA" sobre
  vías endocrinas del vector.
- Cita textual relevante: "Aunque los fitoplasmas no son directamente
  atacables debido a su estilo de vida restringido al floema, los tratamientos
  basados en nanopartículas pueden reducir indirectamente la enfermedad al
  afectar la supervivencia o el comportamiento alimenticio del vector."
- Los fitoplasmas "han perdido muchas partes de su genoma, y sus funciones son
  más similares a las de los virus"; clase Mollicutes; colonizan floema.
- Transmisión persistente propagativa: atraviesan el epitelio del intestino
  medio, entran al hemocele, colonizan tejidos secundarios y en particular las
  glándulas salivales. **Sólo una fracción limitada de los insectos infectados se
  vuelven vectores competentes.**
- Límites del control convencional: los insecticidas reducen la abundancia del
  vector dentro del cultivo pero **no previenen los eventos de infección inicial
  causados por insectos infectivos que llegan de afuera**, porque la transmisión
  puede ocurrir rápidamente apenas empieza la alimentación.
- Nombra como blancos moleculares prometedores las vías de hormona juvenil (JH) y
  los miRNA responsivos a fitoplasma del vector.

---

## Virus como blanco: el dsRNA actúa dentro de la planta

**S43 [FT] Choi SK, Baek E, Ju HJ, Tenllado F, Yoon JY (2026). Control Strategies
of Plant Viruses Using Spray-Induced Gene Silencing. *Plant Pathol J*
42(1):1-17. PMC12884052. OA (CC BY-NC).**
- Marco: no hay agentes antivirales tipo pesticida disponibles para control
  efectivo de virus vegetales; el dsRNA por RNAi da una estrategia
  secuencia-específica y no transgénica.
- Mecanismo declarado: las proteínas Dicer-like procesan el dsRNA endógeno o
  **introducido exógenamente** en dúplex de siRNA de **21–24 nt**; se asocian a
  proteínas de unión a ARN como DRB4, que interactúan con RDR1 y RDR6; la
  amplificación por las RdRP de la planta genera siRNA secundarios que se cargan
  en AGO; la pasajera se degrada y la guía dirige el RISC, que une el transcripto
  complementario y lo corta. En RNAi antiviral **DCL4 produce predominantemente
  siRNA de 21 nt, DCL2 de 22 nt y DCL3 de 23–24 nt**; AGO1 une principalmente
  21 nt, AGO2 mayormente 21 y 22 nt, AGO5 puede acomodar 21, 22 y 24 nt.
- **Tabla 1 del artículo**: 25 combinaciones virus–cultivo con dsRNA aplicado
  externamente. Incluye **maíz**: *sugarcane mosaic virus* (SCMV), gen blanco CP,
  "inhibición de la replicación de SCMV e inducción de resistencia que resultó en
  menor acumulación de SCMV en maíz" (Gan et al., 2020). Incluye virus de ADN:
  *tomato yellow leaf curl virus* (TYLCV), blanco RdRp, descrito como "vacunación
  basada en dsRNA contra un virus de ADN monopartito" (Melita et al., 2021), y
  varios begomovirus con blancos AV1/AV2/AC1/AC4. Blancos más comunes: RdRp, el
  supresor viral de silenciamiento (VSR) y la cápside (CP).
- **Estabilidad**: la exposición a UV durante aproximadamente una hora degrada el
  dsRNA y abole su actividad biológica (San Miguel y Scott, 2016). El monitoreo a
  campo mostró que **lluvias de más de 20 mm en 24 h remueven una proporción
  significativa** de los depósitos foliares de dsRNA (Bachman et al., 2020).
- **Duración**: "la protección antiviral del dsRNA pulverizado típicamente dura
  sólo unos pocos días, requiriendo reaplicaciones frecuentes, lo que es un
  enfoque impracticable para cultivos extensivos de ciclo largo."
- **Entrada**: la vía principal implicada en la captación foliar de dsRNA es la
  **entrada estomática**; alta densidad de tricomas aumenta la hidrofobicidad y
  reduce la absorción; las RNasas apoplásticas degradan el dsRNA expuesto.
- **BioClay** (nanoarcillas de hidróxido doble laminar, LDH): protege al dsRNA de
  la degradación y del lavado **por al menos 30 días**.
- **Costo**: con la plataforma libre de células de GreenLight el costo puede ser
  **menor a 1 USD por gramo de dsRNA**; la síntesis *in vitro* clásica cuesta
  varios cientos de dólares por gramo.
- **Limitación específica para chupadores**: "mientras los insectos masticadores
  pueden ingerir eficientemente el dsRNA aplicado en superficie, las plagas
  chupadoras de savia dependen fuertemente de la captación vascular, que a menudo
  es ineficiente."
- Doble función del dsRNA exógeno: pulverizar papa con dsRNA específico de PVY
  disparó RNAi y además indujo marcadores de inmunidad disparada por patrones
  (PTI: WRKY29, EDS5, PR-1b); el tratamiento suprimió selectivamente PVY, y la
  infección por el no relacionado PVX **no cambió** pese a la activación de PTI.
  Conclusión de los autores: el RNAi dirigido por homología es el determinante
  próximo de la protección, y la PTI sola no alcanza.
- Dato que conviene no olvidar: "las plantas susceptibles infectadas generan
  siRNA derivados del virus en abundancia y aun así permiten replicación,
  movimiento y desarrollo de síntomas", es decir **la generación de siRNA no es
  prueba de resistencia**.
- Regulación: en EE. UU. los productos de dsRNA se clasifican como pesticidas
  bioquímicos bajo FIFRA/FFDCA (EPA); en Australia se regulan como productos
  químicos agrícolas y la OGTR considera a SIGS como no-OGM bajo ciertas
  condiciones; en Corea del Sur no hay todavía lineamientos regulatorios
  formales.

---

## Tratamientos existentes: evidencia argentina y brasileña nueva

**S45 [FT] Oleszczuk JD, Catalano MI, Dalaisón L, Di Rienzo JA, Giménez Pecci MP,
Carpane P (2020). Characterization of components of resistance to Corn Stunt
disease. *PLoS ONE* 15(10):e0234454. PMC7571704. OA (CC BY).**
- Objetivo: separar los componentes de la resistencia al achaparramiento en
  **cuatro híbridos** comerciales argentinos — DK670 y DK72-10 de la región
  templada, DK79-10 y DKB390 de la tropical.
- Diseño: ensayos de **antixenosis** (no preferencia) y **antibiosis** frente al
  vector, y resistencia al patógeno bajo **inoculación artificial** con alta
  presión de insectos infectivos en condiciones de no elección, para que la
  posible antixenosis no confundiera el resultado. Oviposición: 50
  repeticiones, cada una con una jaula por híbrido y seis hembras. Otro ensayo:
  30 repeticiones con cinco insectos por jaula.
- Resultados: **DK72-10 mostró antixenosis y antibiosis** al vector; **DK79-10
  mostró resistencia a *S. kunkelii* como un retraso en la aparición de
  síntomas**; **DKB390 mostró antixenosis al vector y resistencia al patógeno**.
- Hallazgo clave para nosotros: **hubo asociación entre severidad de síntomas y
  reducción de rendimiento, pero no entre acumulación del patógeno y severidad,
  ni entre acumulación y rendimiento.** Es decir, el título del patógeno no
  predice el daño.
- Los síntomas aparecen **de tres a cinco semanas después de la inoculación**.
- Por la transmisión persistente-propagativa, los insectos que adquieren el
  patógeno **permanecen inoculativos durante toda su vida**.

**S47 [FT-parcial] Araujo L, Druetta M, Torrico K, Giménez Pecci MP, Barontini J
(2025). Response of maize hybrids to corn stunt disease caused by *Spiroplasma
kunkelii* in the Argentine Northwest (NOA) – 2023-2024 growing season.
*AgriScientia* 42(1). DOI 10.31047/1668.298x.v42.n1.46410. OA.**
- Enuncia los cuatro agentes del complejo: *S. kunkelii*, MRFV, MBSP y MSMV,
  transmitidos por *D. maidis*.
- **Campaña 2023–2024 en Argentina: brote que afectó toda la región agrícola, con
  una reducción estimada del 20 % de la producción nacional de maíz.** La cifra
  es cita secundaria del artículo: (Bolsa de Comercio de Rosario, 2024).
- Diseño: **14 híbridos comerciales en cinco localidades del NOA** (Bañado de
  Ovanta en Catamarca, Rumi Punco, Metán, entre otras); cultivo antecesor soja en
  todos los casos. Entre quince y veinte hojas con síntomas compatibles por lote
  analizadas por **DAS-ELISA** con reactivos producidos por IPAVE–CIAP–INTA para
  confirmar *S. kunkelii*. Incidencia estimada sobre treinta plantas consecutivas
  por repetición en estadio **R4**.
- Resultados: **incidencia de 8 % a 100 %** según híbrido y sitio. Desempeño sobre
  el promedio en SYN505VIP3, DK7210PRO4, DK7220PRO4, P2297PWUE y PAN5175PWU;
  bajo el promedio en BRV8380PWE, DK7272VT3P, BRV8421PWUE, ZEFIRPWU y
  NEXT22.6PWUE.
- **Regresión lineal mixta con efecto aleatorio de localidad: el índice de
  severidad explica el 72 % de la variabilidad del desempeño, y cada unidad
  adicional de severidad se asocia a una reducción promedio de 15,96 kg/ha.**
- Nota: en la introducción de este trabajo **el modo de transmisión del MSMV se
  declara desconocido**, lo que contradice a S46; queda como `[?]`.

**S46 [FT-parcial] Redoan ACM, Marques VM, Pereira PS, de Oliveira IR,
Silva-Araújo DD, Cota LV, Fadini MAM, Oliveira CM, Rafael DD, Mendes S (2025).
What Is the Relationship Between Efficacy of Seed Treatment with Insecticides
Against *Dalbulus maidis* ... in the Corn Stunt Control? *Insects* 16:713.
PMC12295506. OA (CC BY).**
- Enuncia los cuatro patógenos del complejo (CSDC) y afirma: *D. maidis*
  transmite de manera persistente y propagativa, **"excepto MSMV, que se
  transmite de manera persistente circulativa"**. Contradice a S47, que lo da por
  desconocido → `[?]`.
- Resultados: en estadio **V2**, imidacloprid/tiodicarb fue el más efectivo, con
  **100 % de mortalidad de chicharritas sanas y 85,7 % de las infectivas**,
  previniendo la transmisión del espiroplasma. Tiametoxam y
  metomil + fipronil/tiametoxam dieron alta mortalidad total a las 72 h **sólo
  para las infectivas** (mortalidad de las sanas alrededor del 40 %), reduciendo
  el número de plantas con síntomas en **80 % y 90 %** respectivamente.
- **El tratamiento de semilla fue efectivo hasta el estadio V2**, y las
  chicharritas infectadas resultaron **más susceptibles a los insecticidas** que
  las sanas.
- La infestación con chicharritas portadoras de espiroplasma en estadios
  tempranos redujo fuertemente el rendimiento.

---

## Herramientas de diseño: lo que faltaba de la sección 6

**S48 [FT-parcial] Langmead B, Trapnell C, Pop M, Salzberg SL (2009). Ultrafast
and memory-efficient alignment of short DNA sequences to the human genome.
*Genome Biology* 10:R25. OA (CC BY 2.0).**
- Del resumen: "Bowtie es un programa de alineamiento ultrarrápido y eficiente en
  memoria para alinear lecturas cortas de secuencia de ADN contra genomas
  grandes." Indexación **Burrows-Wheeler**; más de 25 millones de lecturas por
  hora de CPU en el genoma humano con una huella de memoria de ~1,3 GB; extiende
  las técnicas previas con un **algoritmo de backtracking consciente de la
  calidad que permite mismatches**.
- No hay cálculo termodinámico: la salida son posiciones de alineamiento y
  mismatches.

**S49 [RES] Ahmed F, Senthil-Kumar M, Dai X, Ramu VS, Lee S, Mysore KS, Zhao PX
(2020). pssRNAit: A Web Server for Designing Effective and Specific Plant siRNAs
with Genome-Wide Off-Target Assessment. *Plant Physiology* 184(1):65-81.
DOI 10.1104/pp.20.00293.**
- **Es específico de plantas**: diseña un pool de siRNA para silenciar **genes
  vegetales**, con los siRNA diseñados pensados para construir un dsRNA largo y
  expresarlo por VIGS o por vectores de syn-tasiRNA.
- Integra el conjunto de transcriptos de plantas, "varias reglas que gobiernan el
  silenciamiento génico" y una serie de modelos computacionales del mecanismo
  biológico de la vía de RNAi.
- Validación: diseñaron y expresaron construcciones VIGS contra *phytoene
  desaturase* (PDS) y contra el gen ribosomal RPL10 (QM) en *Nicotiana
  benthamiana*; midieron blanco previsto y off-targets por RT-qPCR y evaluaron
  silenciamiento off-target genoma-completo por RNA-seq.
- Soporta **más de 160 especies vegetales**.
- Consecuencia práctica para nosotros: **no sirve para diseñar dsRNA contra un
  insecto**; su base de datos y sus reglas son de plantas.

**S51 [FT-parcial] Saha C, Saha S, Bhattacharyya NP (2025). LncRNAOmics: A
Comprehensive Review of Long Non-Coding RNAs in Plants. *Genes* 16:765.
PMC12294436. OA.**
- Definición citable: "el ARN largo no codificante (lncRNA) se define como
  moléculas de ARN funcionales con longitudes mayores a **200 nucleótidos** sin
  potencial de codificar proteínas".
- Los lncRNA se caracterizan por baja abundancia, menos exones que el ARNm,
  expresión tejido-específica y baja conservación de secuencia comparados con los
  genes codificantes de proteína.
- Los ncRNA regulatorios se dividen en ARN circulares, ncRNA cortos y ncRNA
  largos. Los cortos incluyen siRNA, microRNA y tRF; los siRNA se subclasifican
  en phasiRNA, tasiRNA y easiRNA. **Los microRNA son ARN endógenos cortos no
  codificantes de 20–24 nucleótidos** que generalmente regulan negativamente la
  expresión.
