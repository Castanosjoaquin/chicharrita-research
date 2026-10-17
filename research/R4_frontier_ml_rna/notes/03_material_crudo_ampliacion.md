# R4 — material crudo verificado, segunda tanda (2026-10-17)

Ampliación del relevamiento para poder escribir `REPORT.md`. El criterio de la
ampliación fue el que pide el prompt: **crítica independiente por cada familia de
métodos** y **separación entre resultado validado experimentalmente y resultado
sólo computacional**. Volcado sin redactar, igual que `02_material_crudo.md`.
Todas las fuentes de acá abajo se abrieron en texto completo en esta sesión.

---

## 1. Tang Z, Somia N, Yu Y, Koo PK. "Evaluating the representational power of pre-trained DNA language models for regulatory genomics". Genome Biology 26:203 (2025), DOI 10.1186/s13059-025-03674-8. PDF abierto (CC BY-NC-ND 4.0).

Crítica independiente a los modelos fundacionales de ADN. Es la más dura que se
encontró y viene de un grupo que no construyó ninguno de los modelos evaluados.

- Diseño: **probing sin ajuste fino (fine-tuning)**. Se congelan los pesos y se
  mide si la representación, por sí sola, sirve. Cuatro modelos: Nucleotide
  Transformer, DNABERT-2, HyenaDNA y un GPN propio preentrenado sobre el genoma
  humano de referencia. Seis tareas de genómica funcional específicas de tipo
  celular, a nivel de ADN y de ARN.
- Tareas: 1) actividad regulatoria por lentiMPRA (entrada de 230 nt, salida
  escalar); 2) sitios de unión de factores de transcripción por ChIP-seq (200 nt,
  10 conjuntos, métrica AUROC, 5 inicializaciones); 3) efecto de variantes en
  cero disparos (zero-shot) con datos de MPRA; 4) unión de proteínas de unión a
  ARN (RBP) con eCLIP-seq (1000 nt, 120 RBP en K562); 5) potencial de elongación
  de la ARN polimerasa II por INSERT-seq (173 nt); 6) interpretación por mapas de
  atribución.
- Líneas base: one-hot con CNN; MPRAnn; un ResidualBind-like (ResNet) muy
  ajustado; y Sei, un "modelo fundacional supervisado" preentrenado sobre 21.907
  perfiles de cromatina en más de 1300 líneas celulares y tejidos.
- Resultado literal: "gLM representations provided little to no advantage over
  standard one-hot encoded sequences when used by downstream models to predict
  regulatory activity".
- Resultado sobre el token CLS: las CNN entrenadas sobre el embedding completo
  superaron consistentemente a los modelos que usan el token CLS, en todas las
  tareas, y el CLS "appeared to encode information only marginally more
  informative than bag-of-dinucleotide statistics".
- Conclusión de mecanismo: "cell type–specific cis-regulatory features are
  largely learned during fine-tuning, and that the value of pre-training may lie
  mostly in initializing models with low-level sequence statistics".
- Resultado de escala: GPN (convolucional) dio representaciones algo más
  informativas que los BERT más pesados; HyenaDNA (modelo de espacio de estados
  liviano) rindió comparable a GPN y superó consistentemente a los modelos
  fundacionales más grandes. Ambos operan a nivel de nucleótido. Los autores
  concluyen que "simply scaling model size may only incrementally improve
  performance in regulatory genomics" y que lo que importa son los sesgos
  inductivos de la arquitectura.
- Matiz sobre tokenización: señalan que Evo 2 se construye sobre HyenaDNA pero usa
  codificación por pares de bytes, lo que sugiere que la tokenización sola no
  explica la diferencia.
- Autocrítica declarada: usaron particiones aleatorias de entrenamiento y prueba,
  lo que "may favor CNNs operating directly on raw sequences by enabling them to
  more readily learn from homologous patterns shared across splits". Lo declaran
  y sostienen que no cambia la conclusión principal.
- Explicación propuesta de por qué el no codificante es más difícil que la
  proteína: las proteínas tienen gramáticas de bajo nivel (estructura secundaria)
  y de alto nivel (dominios) conservadas entre especies; el genoma no codificante
  tiene motivos cortos, dispersos, con reglas que varían por locus y tipo
  celular, y poca conservación profunda.
- Dato colateral útil: el preentrenamiento sobre regiones focalizadas (CDS, UTR,
  promotores) o sobre organismos de genoma compacto sí da mejores resultados, y
  los modelos a nivel de codón preservan señales sinónimas como el sesgo de uso
  de codones.

## 2. Marin FI, Teufel F, Horlacher M, Madsen D, Pultz D, Winther O, Boomsma W. "BEND: Benchmarking DNA Language Models on Biologically Meaningful Tasks". ICLR 2024 (arXiv 2311.12570). PDF abierto.

Segundo benchmark independiente de modelos de ADN, con criterio distinto al de
Tang y Koo: compara contra **métodos expertos**, no sólo contra one-hot.

- Siete tareas sobre el genoma humano. Catorce modelos preentrenados de seis
  fuentes distintas, más líneas base supervisadas.
- Tabla 3 (resultados; mejor método experto entre paréntesis):
  - Búsqueda de genes (gene finding): experto AUGUSTUS **0,80**; mejor LM NT-MS
    **0,68**; NT-V2 0,64; DNABERT 0,20; HyenaDNA large 0,35; CNN de dos capas
    **0,00** (no aprende); ResNet supervisada 0,46.
  - Anotación de enhancers: experto Enformer 0,07; todos los LM entre 0,02 y
    0,06. **Todos fracasan.**
  - Accesibilidad de cromatina: experto BASSET 0,85; mejor LM DNABERT 0,85;
    CNN one-hot 0,75.
  - Modificación de histonas: BASSET 0,74; mejor LM DNABERT 0,79; CNN 0,76.
  - Metilación CpG: BASSET 0,93; mejor LM NT-MS 0,92; CNN 0,84.
  - Efecto de variantes (expresión): DeepSEA 0,70; mejor LM DNABERT 0,60.
  - Efecto de variantes (enfermedad): DeepSEA 0,56; mejor LM NT-MS 0,77.
- Conclusión literal: los LM de ADN "do not offer consistent improvements over
  all included tasks and can fall short of surpassing specialized existing
  prediction methods"; "For modeling functional genomics data, DNA LMs only show
  limited utility".
- Hallazgo que importa para nosotros: NT-MS es un buen valor por defecto pero en
  algunas tareas es inferior al mucho más chico DNABERT, y los dos aprendieron
  **rasgos genómicos distintos** pese a compartir el objetivo de enmascarado. Los
  autores atribuyen la diferencia a los datos de preentrenamiento y la
  tokenización.
- **Limitación declarada, directamente aplicable a nuestro caso:** BEND es sólo
  humano, y "an important question that remains unanswered is whether DNA LMs can
  aid with generalization across different organisms". Proponen como trabajo
  futuro entrenar en un organismo y evaluar en otro. Es exactamente la
  transferencia que nuestro problema necesitaría y que nadie midió.

## 3. Ren Y, Chen Z, Qiao L, Jing H, Cai Y, Xu S, Ye P, Ma X, Sun S, Yan H, Yuan D, Ouyang W, Yao X [autoría según el PDF abierto]. "BEACON: Benchmark for Comprehensive RNA Tasks and Language Models". NeurIPS 2024 (arXiv 2406.10391). PDF abierto.

Benchmark independiente del lado ARN. Trece tareas: estructura (SSP, CMP, DMP,
SSI), función (SPL, APA, NcRNA, Modif, MRL), ingeniería (VDP, PRS, CRI-On,
CRI-Off).

- Modelos evaluados: RNA-FM, RNABERT, RNA-MSM, SpliceBERT (tres variantes),
  UTR-LM (dos), UTRBERT (cuatro tamaños de k-mero), más su propia línea base
  BEACON-B, más líneas base ingenuas CNN / ResNet / LSTM, más el estado del arte
  publicado de cada tarea.
- Resultado 1, literal: "ResNet, which has only been trained on downstream tasks,
  can outperform most if not all language models on some tasks. LSTM outperforms
  the other Naive supervised Models on 9 out of 13 tasks".
- Resultado 2: los modelos de lenguaje de ARN superan al estado del arte previo
  específico de tarea en **8 de 13** tareas, y quedan claramente cortos en mapa
  de contactos, mapa de distancias, degradación de vacunas y CRISPR dentro y
  fuera de blanco.
- **El dato más relevante para nosotros**, tabla 3, tarea CRI-Off (predicción de
  efecto fuera de blanco de CRISPR, métrica correlación de Spearman en %):
  estado del arte DeepCRISPR **12,6**; CNN ingenua **11,40**; LSTM 8,60; y todos
  los modelos de lenguaje de ARN entre **2,49 y 5,00** (RNA-FM 2,49; RNA-MSM
  3,85; UTRBERT-3mer 4,48; BEACON-B 4,42). Es decir: **en la tarea de tipo fuera
  de blanco, los modelos fundacionales de ARN rinden la mitad o menos que una CNN
  entrenada desde cero.**
- Otros números de la tabla 3 que sirven de contexto: estructura secundaria (F1%)
  estado del arte UFold 65,4; RNA-FM 68,50; SpliceBERT-MS1024 68,26; LSTM 58,61;
  CNN 49,95. Clasificación de ncRNA (ACC%): RNA-FM 96,81 contra GCN 85,73 y LSTM
  88,78. Carga ribosomal media MRL (R²%): LSTM 83,94, RNA-FM 79,47, Optimus 78.
- Limitaciones declaradas por los autores: 13 tareas no cubren toda la biología
  del ARN; falta explorar sistemáticamente el efecto de los datos de
  preentrenamiento y los hiperparámetros; evalúan sólo exactitud predictiva, sin
  interpretabilidad, eficiencia ni robustez.

## 4. Wang H, Zhang Y, Chen J, Zhan J et al. "Zero-shot benchmarking of RNA language models in structural, functional, and evolutionary learning". Briefings in Bioinformatics 27(2):bbag098 (2026), DOI 10.1093/bib/bbag098, PMC12963973. Texto completo abierto por PMC.

**Corrección importante al catálogo previo.** Este artículo es, casi con certeza,
la versión revisada por pares y ampliada del preprint que `02_material_crudo.md`
registró como "Wang et al., A Comparative Review of RNA Language Models, arXiv
2505.09087": mismo primer autor (Wang He), misma institución (Shenzhen Bay
Laboratory), misma metodología de estructura secundaria por mapas de atención y
de clasificación por razón de solapamiento, y **el mismo resultado numérico**
(RNA-MSM supera a AIDO.RNA 1,6B en 9,0 % de F1 mediano). El artículo no declara
explícitamente ser la misma obra, así que la equivalencia se marca `[?]`.
Amplía de ~14 a **21 modelos de ARN** y agrega una tercera tarea.

- Tres tareas estrictamente en cero disparos, cada una ligada a una parte
  distinta del modelo: estructura secundaria desde **pesos de atención**;
  clasificación desde **embeddings**; aptitud mutacional desde **logits**.
- Protocolo de estructura: se elige una única combinación de capa y cabeza, y un
  único umbral, maximizando F1 en el conjunto de validación VL1, y se aplica sin
  cambios a los conjuntos de prueba. Simetrización de la matriz de atención y
  corrección por producto promedio (APC).
- Conjunto TS-Hard: identidad de secuencia por debajo de 80 %, TM-score por
  debajo de 0,45 entre validación y prueba, y eliminación de solapamiento de
  familias de Rfam con Infernal. Quedan **15 estructuras del PDB**. Es el régimen
  de baja homología, el que importa.
- Resultado de estructura: RNA-MSM, que usa alineamientos múltiples y fue
  entrenado con menos de 4000 familias, tiene el F1 y el MCC medianos más altos
  de la clase I, superando a AIDO.RNA 1,6B en 9,0 % y 6,6 %. Los autores lo leen
  como que la información evolutiva pesa más que la escala.
- Resultado de aptitud mutacional, el más duro: los mejores (MP-RNA, AIDO.RNA,
  RNA-FM, SpliceBERT, DGRNA) alcanzan MCC mediano de **0,14–0,18**, AUC mediano
  de aproximadamente **0,60** y correlación de Spearman mediana por encima de
  0,20; MP-RNA es el mejor por mediana (0,215) y SpliceBERT por media (0,268).
  Literal: "absolute performance remained limited across all models (mean MCC
  < 0.20, AUC < 0.64, SR < 0.27), indicating that zero-shot RNA fitness
  prediction remains a challenging task".
- Hallazgo de compromiso (trade-off): los modelos buenos en estructura (RNA-km,
  MP-RNA) son peores en clasificación o en aptitud, y viceversa. "different
  biological signals are not automatically aligned in current RNA LMs".
- Hallazgo que respalda el enfoque híbrido: MP-RNA y PlantRNA-FM rinden bien pese
  a tener poco ncRNA en sus datos, y los autores lo atribuyen explícitamente a
  "the explicit incorporation of RNA secondary structure information, derived
  from **ViennaRNA-based predictions**, during pretraining and inference".
- LucaOne (unificado) rinde por debajo de la mayoría de los modelos específicos
  de ARN: "modality-agnostic pretraining may dilute RNA-specific structural
  inductive biases".
- Dato de arquitectura: 17 de los 21 modelos son BERT con enmascarado.
- Tabla 1 (especificaciones verificadas en fuente revisada por pares; completa
  entradas que antes estaban sólo en el preprint y agrega modelos nuevos):
  - RNA-FM 2022, 100M, RNAcentral ~23M seq, base, BERT, 12 capas, 20 cabezas,
    640 dim, 1024 nt.
  - RNABERT 2022, 0,5M, humano de RNAcentral ~762K seq, BERT, 6, 12, 120, 440.
  - Uni-RNA 2023, L8 21M / L12 71M / L16 168M, RNAcentral + nt + GWH ~1000M seq.
  - AIDO.RNA 2024, 648M y 1,6B, RNAcentral ~41,5M seq, BERT, 33/32, 20/32,
    1280/2048, 1024.
  - **DGRNA 2024, 108M, MARS ~1,2B, arquitectura Mamba2, 12 capas, 768 dim, 2048 nt.**
  - **GenerRNA 2024, 304M, RNAcentral ~16,09M seq, tokenización BPE, GPT, 24
    capas, 16 cabezas, 1280 dim, 1024 nt. Es generativo.**
  - **RFamLlama 2024, base 31M y large 89M, Rfam 14.10 ~676K, arquitectura Llama.**
  - RNAErnie 2024, 86M, RNAcentral ~23M, BERT, 12, 12, 768, 512.
  - RNA-km 2024, 152M, RNAcentral ~23M, BERT, 12, 16, 1024, 512.
  - RNA-MSM 2024, 96M, MSA de ~4000 familias de Rfam, MSA-Transformer, 10, 12,
    768, 1024.
  - BiRNA-BERT 2025, 116M, RNAcentral + RefSeq ~36,5M, base o BPE.
  - ERNIE-RNA 2025, 86M, RNAcentral ~20,4M, BERT, 12, 12, 768, 1024.
  - **LAMAR 2025, 86M, RNAcentral + RefSeq + NCBI Genome ~15M seq, 2048 y 4096 nt.**
  - ProtRNA 2025, 651M, RNAcentral no redundante ~6M, BERT, 33, 20, 1280, 512.
  - RiNALMo 2025, micro 33M / mega 148M / giga 651M, ~36M seq, 12/30/33 capas.
  - **3UTRBERT 2023, 86M, 3'UTR humanos de GENCODE ~20K seq, tokenización k-mero.**
  - MP-RNA 2024, 186M, OneKP ~54,2 Gb, entrada secuencia + estructura secundaria.
  - **PlantRNA-FM 2024, 34M, OneKP ~54,2 Gb, entrada secuencia + estructura
    secundaria, BERT, 12 capas, 20 cabezas, 480 dim, 1026 nt.**
  - SpliceBERT 2024, 20M, 72 genomas de vertebrados de UCSC ~2M seq.
  - UTR_LM 2024, 1M, 5'UTR de Ensembl ~2,3M seq, entrada secuencia + SS + MFE.
  - LucaOne 2025, 1,6B, RefSeq ~136M secuencias de ARN, BERT, 20, 40, 2560, 1280.
- Advertencia de cobertura de los propios autores: modelos muy recientes o
  preprints sin checkpoint público estable pueden no estar incluidos.

## 5. Yu H, Deng H, Zhang J et al. (Ding Y, Li K, Zhang H, correspondencia). "An interpretable RNA foundation model for exploring functional RNA motifs in plants" (PlantRNA-FM). Nature Machine Intelligence 6:1616–1625 (diciembre 2024), DOI 10.1038/s42256-024-00946-z. PDF abierto, artículo CC BY 4.0.

El único modelo fundacional de ARN de plantas del catálogo, y el único con
validación experimental propia de lo que el modelo encontró.

- 35 millones de parámetros, 12 capas, 24 cabezas de atención, dimensión 480.
  (La tabla de bbag098 lo reporta como 34M y 20 cabezas; discrepancia menor,
  queda `[?]`; acá vale el primario.)
- Preentrenado sobre transcriptomas de **1124 especies de plantas** (iniciativa
  OneKP), integrando secuencia **y estructura predicha con RNAfold**, más
  anotación de CDS y UTR. Objetivo: modelado de nucleótidos enmascarados (MNM).
- Anotación de región génica (5'UTR / CDS / 3'UTR): F1 **0,974** contra **0,639**
  del mejor modelo previo. Comparado contra DNABERT-2, RNABERT, Nucleotide
  Transformer, ESM2 y cdsBERT.
- Estructura secundaria en tres conjuntos de referencia (bpRNA TR0-TS0, ArchiveII
  y otro): supera al segundo mejor por 0,124, 0,171 y 0,136, y los autores lo
  atribuyen a haber integrado estructura en el preentrenamiento.
- **Validación experimental:** revelaron motivos de ARN asociados a traducción en
  plantas y los validaron experimentalmente. Datos de *A. thaliana* en SRA
  PRJNA762705 y de *O. sativa* en PRJNA1112739.
- Código y pesos en huggingface.co/yangheng/PlantRNA-FM. El artículo es CC BY 4.0;
  **la licencia de los pesos no está declarada en el artículo** `[?]`.

## 6. Bai Y, Zhong H, Wang T, Lu ZJ. "OligoFormer: an accurate and robust prediction method for siRNA design". Bioinformatics 40(10) btae577 (2024), DOI 10.1093/bioinformatics/btae577.

**Nota de verificación:** el PDF que entregó Unpaywall para ese DOI es la versión
**preprint de bioRxiv (2024.02.02.578533)**, no el PDF de la revista. Los números
de abajo salen del preprint abierto. El resumen de la versión de revista (que sí
se leyó en los metadatos de Crossref) difiere en dos detalles: dice "six
comparable methods" donde el preprint dice 5, y agrega 6,6 % de PRC y 5,1 % de
PCC. La discrepancia se marca `[?]` y no se usa ninguno de esos dos números.

- Tres módulos: cálculo termodinámico, módulo RNA-FM y Oligo encoder
  (transformer). Entrada: secuencias de siRNA y de ARNm.
- Datos, tabla 1 del preprint: nueve conjuntos, **todos humanos y de línea
  celular**. Huesken 2431 siRNA contra 34 ARNm en H1299; Takayuki 702 contra 1 en
  HeLa; Amarzguioui 46/4 en HaCaT; Haborth 44/1 en HeLa; Hsieh 108/22 en HEK293T;
  Khvorova 14/1 en HEK293; Reynolds 240/7 en HEK293; Vickers 76/2 en T24; Ui-Tei
  53/3 en HeLa. Los ocho últimos sin Huesken y sin Takayuki forman "Mixset".
- Normalización: la eficacia se lleva a inhibición de 0 a 100 % y **el 70 % del
  máximo de inhibición es el umbral** que separa positivos de negativos.
- Intra-conjunto, validación cruzada de 5 pliegues: Huesken AUC 0,8619 y F1
  0,7584; Mixset AUC 0,8444 y F1 0,7636; Takayuki AUC 0,8628 y F1 0,577.
- **Inter-conjunto** (entrena en Huesken, evalúa en Mixset), tabla 2:
  OligoFormer AUC **0,8153** / F1 0,7689; DSIR 0,7483 / 0,6945; i-Score 0,7462 /
  0,2197; s-BioPredsi 0,7374 / 0,5936; OligoWalk 0,708 / 0,6258; siRNAPred
  0,5782 / 0,5245. **El propio mejor modelo cae de 0,8444 a 0,8153 al cambiar de
  conjunto dentro de la misma especie y el mismo tipo de ensayo.**
- Ablación: quitar cualquier módulo empeora; el Oligo encoder es el que más
  aporta; RNA-FM y los parámetros termodinámicos mejoran y aceleran la
  convergencia. Ventana deslizante de 19 nt sobre el ARNm completo.
- Fuera de blanco: el pipeline usa puntajes **PITA y TargetScan**, que son
  herramientas de predicción de blancos de miRNA, no un modelo entrenado en datos
  de efecto fuera de blanco de siRNA.
- Limitación declarada, literal: "The limited representation and quantity of
  existing datasets severely limit the effectiveness of siRNA design models and
  further generalization". Y: la modificación química, que es la estrategia
  principal para reducir el efecto fuera de blanco, no está incluida en la
  predicción.
- Código en github.com/lulab/OligoFormer; imagen Docker en hub.docker.com.

## 7. Muita BK, Damayo JE, Remnant EJ, Smith NA, Greaves IK, Ghodke AB, Kumaran N, Roberts JMK. "Novel dsRNA designs increase the stability and bioefficacy of RNAi-based pesticides for *Varroa destructor*". Frontiers in Insect Science, publicado 17-ago-2026, DOI 10.3389/finsc.2026.1868457. PDF abierto. CSIRO + Universidad de Sídney.

Esta entra porque es el **eje de diseño que ningún modelo computacional del
catálogo cubre**: la arquitectura física de la molécula de dsRNA, no la elección
del tramo de secuencia. Y porque es validación húmeda reciente.

- Dos diseños avanzados, ambos sobre dsRNA de extremos en lazo (loop-ended,
  ledRNA): **ledG:U**, donde todas las citosinas de la hebra sentido se
  sustituyen por timinas para generar apareamientos G-U oscilantes (wobble) en
  todo el tallo; y **led[Δ22]**, con una deleción cada 22 nt en la hebra sentido
  que genera una protuberancia (bulge) asimétrica en la antisentido **sin alterar
  la secuencia de la antisentido**.
- Dos genes blanco en *Varroa destructor*: *Pero* (proteína de unión a quitina
  tipo peritrofina-A) y *CHH* (hormona hiperglucémica de crustáceo). Control
  negativo: ledGFP.
- Resultados: el doble de estabilidad en solución de sacarosa y dentro de abejas
  adultas respecto del dsRNA convencional; silenciamiento del blanco con
  reducción de **~36–86 %**; aumento de mortalidad de ácaros de **~32–56 %**;
  todo "variable pero mejorado" respecto del dsRNA convencional.
- Secuenciación de ARN pequeños: procesamiento efectivo de los diseños avanzados,
  cobertura completa de siRNA sobre la región blanco, clases de tamaño con pico
  en **22–24 nt** y sesgo hacia la hebra antisentido.
- Condiciones: inmersión 16 h a 4 °C, recuperación 3 h a 30 °C y 75 % de humedad
  relativa, cuatro ácaros por pupa en cápsulas de celulosa, mortalidad a 48 h.
  n = 5 réplicas biológicas, salvo led[Δ22]-Pero con 2 y led[Δ22]-CHH con 4.
  Tukey HSD, p < 0,05.
- Alcance declarado por los autores: **sólo condiciones de laboratorio**; hace
  falta "further optimisation of gene-design combinations"; y reconocen que
  faltó probar genes control con el diseño ledRNA para descartar efectos no
  dirigidos **del propio diseño estructural** sobre la mortalidad.

## 8. Skarlinski MD, Cox S, Laurent JM, Braza JD, Hinks M, Hammerling MJ, Ponnapati M, Rodriques SG, White AD. "Language agents achieve superhuman synthesis of scientific knowledge" (PaperQA2 / LitQA2). arXiv 2409.13740. PDF abierto. Resuelve el pendiente registrado en `sources.json`.

Lectura crítica, porque el título dice más de lo que el resultado sostiene.

- LitQA2: preguntas de opción múltiple sobre literatura reciente, con opción
  explícita de "información insuficiente". Dos métricas separadas: **precisión**
  (fracción de aciertos entre las preguntas que el sistema sí contestó) y
  **exactitud** (fracción de aciertos sobre el total de preguntas).
- PaperQA2: precisión **85,2 % ± 1,1 %** y exactitud **66,0 % ± 1,2 %** (media ±
  DE, n = 3 corridas), eligiendo "información insuficiente" en **21,9 % ± 0,9 %**
  de las respuestas. Usa en promedio 14,5 ± 0,6 artículos por pregunta.
- Anotadores humanos con doctorado en biología o en curso, con acceso completo a
  internet y a las suscripciones de su institución, alrededor de una semana de
  plazo e incentivo económico de 3 a 12 dólares por pregunta: precisión
  **73,8 % ± 9,6 %** y exactitud **67,7 % ± 11,9 %** (n = 9).
- **La diferencia es significativa en precisión (t(8,6) = 3,49; p = 0,0036) y NO
  es significativa en exactitud (t(8,5) = −0,42; p = 0,66).** Es decir: el
  sistema es "superhumano" en no equivocarse cuando contesta, y es equivalente al
  humano en cuánto contesta bien del total. Lo logra absteniéndose en uno de cada
  cinco casos.
- Control de sobreajuste: generaron 101 preguntas nuevas de LitQA2 después de
  hacer la mayoría de los cambios de ingeniería; la exactitud no difirió
  significativamente de la del conjunto original de 147.
- WikiCrow (resúmenes de genes codificantes humanos): 375 afirmaciones de 240
  artículos pareados, juzgadas a ciegas por expertos. Afirmaciones "citadas y no
  sostenidas" 13,5 % contra 24,9 % de Wikipedia (p = 0,0075); sin citar 3,5 %
  contra 13,6 % (p < 0,001); precisión 86,1 % contra 71,2 % (p = 0,0013). Nótese
  que **13,5 % de afirmaciones citadas y no sostenidas sigue siendo una de cada
  siete.**
- ContraCrow: 2,34 ± 1,99 contradicciones por artículo (n = 93 artículos de
  biología elegidos al azar), de las cuales el **70 % fueron validadas por
  expertos humanos**. El 30 % restante, no.

## 9. Gottweis J, Weng W-H, Daryin A et al. (Google Cloud AI Research, Google DeepMind, Google Research, Stanford, Imperial College). "Accelerating scientific discovery with Co-Scientist". arXiv 2502.18864. PDF abierto (157 páginas con material suplementario).

Es el caso más fuerte publicado de generación de hipótesis con validación
húmeda, y por eso conviene leer con precisión qué se validó.

- Sistema multiagente sobre modelos de la familia Gemini, con paradigma "generar,
  debatir, evolucionar": autodebate, selección por torneo y refinamiento
  iterativo, con escalado de cómputo en tiempo de inferencia.
- Métrica interna: puntaje Elo de las hipótesis en el torneo, medido a lo largo
  de 203 objetivos de investigación distintos hasta el 3 de febrero de 2025. **Es
  una autoevaluación del propio sistema.**
- Tres validaciones húmedas: 1) reposicionamiento de fármacos para leucemia
  mieloide aguda, con citotoxicidad selectiva **in vitro** a concentraciones
  clínicamente relevantes; 2) blancos epigenéticos nuevos para fibrosis hepática,
  con actividad antifibrótica y regeneración de hepatocitos en **organoides
  hepáticos humanos**, incluyendo un fármaco aprobado por la FDA; 3) en
  microbiología, el sistema **recapituló de forma independiente** un mecanismo de
  transferencia de elementos genéticos móviles entre bacterias que en ese momento
  estaba sin publicar.
- Limitaciones declaradas, textuales y relevantes: el conocimiento está limitado
  a literatura de acceso abierto, con omisión de arte previo tras muros de pago y
  **"a systemic lack of access to negative experimental results"**; la calidad de
  las hipótesis depende de la calidad mixta y contradictoria de la literatura
  fuente, con "risk of propagating erroneous or irreproducible findings"; hereda
  la factualidad imperfecta y las alucinaciones del modelo de base; y, textual,
  **"the validation of Co-Scientist's hypotheses, while successful, remains
  preliminary"**.
- Autocrítica metodológica explícita: hacen falta "more objective and automated
  evaluation metrics that move beyond current ranking systems", es decir, los
  propios autores reconocen que el Elo del torneo no alcanza como evaluación.
- Riesgo declarado: el uso impropio sin revisión por pares ni salvaguardas podría
  agravar la crisis de reproducibilidad por producción de artefactos científicos
  de baja calidad.

## 10. He S, Huang R, Townley J, Kretsch RC, Karagianes TG et al. (consorcio Eterna/Kaggle; correspondencia Das R, Stanford). "Ribonanza: deep learning of RNA structure through dual crowdsourcing". bioRxiv 10.1101/2024.02.24.581671 (27-feb-2024), CC BY 4.0. PDF abierto.

Entra como **vara de medir de cuántos datos hace falta** para que el aprendizaje
profundo cambie un subcampo del ARN.

- Conjunto Ribonanza: mediciones de mapeo químico (chemical mapping) sobre **dos
  millones** de secuencias de ARN diversas, reunidas por Eterna y otras
  iniciativas de ciencia colaborativa.
- Escala real, declarada por los autores: aproximadamente **400 millones de
  mediciones a nivel de nucleótido** para esos dos millones de secuencias, con
  relación señal-ruido aceptable en **80 millones** de ellas. Y, textual, "these
  datasets are much smaller than the corpora of 10 billion to many trillions of
  data that have led to transform[ative]..." modelos en otros dominios.
- Proceso: desafío abierto en Kaggle con evaluación prospectiva de redes
  propuestas por terceros, y después destilación en un modelo único y
  autocontenido, RibonanzaNet.
- Resultado: tras superar en error absoluto medio a todas las soluciones del
  desafío, RibonanzaNet ajustado alcanza el estado del arte en tres tareas
  auxiliares: modelado de secuencias que se caen de los experimentos, degradación
  hidrolítica del ARN y estructura secundaria (evaluada en una partición temporal
  del PDB y en los blancos de ARN de CASP15).
- Motivación declarada del trabajo: hasta ese momento "there have been no blind
  tests that would allow rigorous evaluation of whether predictive models might
  be trained from chemical mapping data", y el campo venía con "scarcity of
  experimentally determined 3D coordinates", "lack of rigor in evaluation" y
  "poor generalization of deep learning models of RNA secondary structure".
- Limitación declarada: no pudieron evaluar prospectivamente estructura 3D por
  el costo y el tiempo de resolver estructuras nuevas; lo dejaron para CASP16.

## 11. Flamm C, Wielach J, Wolfinger MT, Badelt S, Lorenz R, Hofacker IL. "Caveats to Deep Learning Approaches to RNA Secondary Structure Prediction". Frontiers in Bioinformatics 2:835422 (2022), DOI 10.3389/fbinf.2022.835422. PDF abierto. Grupo de ViennaRNA.

Crítica metodológica al aprendizaje profundo en estructura secundaria, anterior a
Szikszai pero complementaria: el problema no es sólo la generalización entre
familias, es el **sesgo del conjunto de datos** y la ausencia de restricciones
físicas en el modelo.

- Diagnóstico del sesgo: en bpRNA, el **55 %** de las secuencias son ARN
  ribosomales del Comparative RNA Website y el **43 %** viene de Rfam; en la
  versión de Rfam usada por bpRNA, el ARNr y el ARNt juntos son **más del 90 %**
  de las secuencias. El conjunto está dominado por cuatro familias.
- Propuesta metodológica: estudiar capacidades y límites de los modelos
  entrenándolos primero sobre **datos sintéticos** generados desde un modelo
  biofísico simplificado, que se pueden producir en cantidad arbitraria y donde
  todos los sesgos son controlables.
- Modelos probados: red densa sobre ventanas, CNN unidimensional sobre ventanas y
  una BLSTM sin ventana.
- **Falla estructural encontrada:** el número de pares de bases predichos escala
  de forma **cuadrática** con la longitud de la secuencia, cuando una estructura
  secundaria sólo puede acomodar un número **lineal** de pares. Es decir, el
  modelo no aprendió una restricción elemental del objeto que predice.
- Control de memorización: sobre ARN plegados inversamente y sobre ARN barajados,
  la red preentrenada rinde igual (MCC 0,46 en ambos), y durante el entrenamiento
  el rendimiento sobre el conjunto inverso mejora rápido mientras que sobre el
  barajado casi no mejora.
- Conclusión de los autores: el rendimiento de las redes profundas depende
  fuertemente de la cantidad y la calidad de los datos, y los datos biológicos
  están fuertemente sesgados hacia unos pocos sistemas modelo bien estudiados.
