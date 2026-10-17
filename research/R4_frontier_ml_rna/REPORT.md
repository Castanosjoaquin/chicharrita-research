# R4 — Frontera de aprendizaje automático aplicado a biotecnología de ARN

Relevamiento de estado del arte en la intersección entre aprendizaje automático
(*machine learning*) y biotecnología de ARN, hecho para decidir en qué subcampo
conviene que se pare un equipo de cuatro personas de Ingeniería en IA que tiene
que proponer un método de diseño y priorización de ARN exógeno contra
*Dalbulus maidis* y los patógenos del complejo de achaparramiento del maíz.

**Fechas del relevamiento:** 16 y 17 de octubre de 2026.
**Catálogo estructurado:** `modelos.json`.
**Propuestas priorizadas:** `lineas_de_ataque.md`.
**Fuentes:** `sources.json`, con la URL efectivamente abierta de cada una y una
sección aparte con las que no se pudieron abrir y por qué.
**Material crudo sin redactar:** `notes/02_material_crudo.md` y
`notes/03_material_crudo_ampliacion.md`.

Marcadores de evidencia, según `CLAUDE.md`: `[E]` establecido, consenso en
literatura revisada por pares; `[R]` reportado por una o pocas fuentes, preprint
o nota técnica; `[H]` hipótesis nuestra; `[?]` incierto o fuentes en conflicto.
Además, y porque el prompt de esta investigación lo exige explícitamente, cada
resultado relevante se califica como **validado experimentalmente**, **sólo
computacional** o **demostración sin evaluación seria**. Las dos escalas son
independientes: un resultado puede ser `[E]` y a la vez sólo computacional.

---

## Veredicto, antes de las seis secciones

El campo se ve, desde afuera, como una escalera de modelos cada vez más grandes.
Visto desde adentro, con los benchmarks independientes en la mano, se ve
distinto: **hay una brecha sistemática entre lo que los artículos de modelos
nuevos reportan y lo que miden las evaluaciones hechas por terceros**, y esa
brecha se ensancha justamente en el régimen que nuestro problema habita —baja
homología, especie sin datos, tarea de tipo fuera de blanco, conjuntos de
entrenamiento de decenas de puntos.

Tres resultados, cada uno de un grupo que no construyó los modelos que evalúa,
sostienen el veredicto:

1. En seis tareas de genómica funcional, las representaciones de cuatro modelos
   fundacionales de ADN **no ofrecen ventaja apreciable sobre una codificación
   one-hot**, y una CNN bien ajustada entrenada desde cero iguala o supera a los
   preentrenados `[E]`, sólo computacional (Tang, Somia, Yu y Koo, *Genome
   Biology* 26:203, 2025).
2. En trece tareas de ARN, una LSTM entrenada sólo en la tarea supera al resto de
   las líneas base ingenuas en **9 de 13** tareas, y en la tarea de predicción de
   efecto fuera de blanco **todos** los modelos fundacionales de ARN quedan por
   debajo de una CNN simple `[E]`, sólo computacional (BEACON, NeurIPS 2024).
3. En estructura secundaria con baja homología, ningún modelo de lenguaje de ARN
   mejora significativamente sobre one-hot, y el método termodinámico clásico los
   supera a todos `[E]`, sólo computacional (Zablocki et al., *Briefings in
   Bioinformatics* 26(2) bbaf137, 2025).

Eso no dice que los modelos fundacionales no sirvan. Dice **dónde** sirven: donde
hay homología con el preentrenamiento, donde la tarea es clasificación de
familias o anotación, y donde después hay ajuste fino con datos etiquetados
suficientes. Nuestro problema no cumple ninguna de las tres condiciones.

La recomendación que sale de acá, desarrollada en `lineas_de_ataque.md`, es
pararse en el subcampo que el relevamiento muestra **abierto y barato**: la
cuantificación de incertidumbre y la auditabilidad de la decisión de priorización,
sobre una base híbrida de termodinámica más características validadas en insecto.
No en el subcampo que se ve más impresionante.

---

## 1. Modelos fundacionales de secuencias biológicas

### 1.1 Cómo está organizado el campo

Conviene empezar por la taxonomía, porque el término "modelo fundacional" tapa
tres objetos con propiedades muy distintas. El relevamiento revisado por pares de
Wang, Zhang, Chen y Zhan (*Briefings in Bioinformatics* 27(2) bbag098, 2026)
propone una clasificación por datos de preentrenamiento que resultó la más útil
para decidir `[E]`:

- **Clase I**, modelos de ARN enriquecidos en ARN no codificante (*non-coding
  RNA*, ncRNA): RNA-FM, RNABERT, Uni-RNA, AIDO.RNA, RiNALMo, ERNIE-RNA, RNAErnie,
  RNA-km, RNA-MSM, ProtRNA, BiRNA-BERT, LAMAR, DGRNA, GenerRNA, RFamLlama.
- **Clase II**, modelos de propósito específico entrenados sobre ARN mensajero o
  sus regiones: SpliceBERT, UTR-LM, 3UTRBERT, MP-RNA y PlantRNA-FM.
- **Clase III**, modelos unificados que procesan ADN, ARN y proteína juntos:
  LucaOne y, en el límite, la familia Evo.

A eso hay que sumarle la familia de ADN propiamente dicha —Nucleotide
Transformer, DNABERT y sus sucesores, HyenaDNA, GPN, GENA-LM, GROVER— que es la
que tiene los benchmarks independientes más duros.

Dato de arquitectura que ordena el panorama: **17 de los 21 modelos de ARN
catalogados por Wang et al. son BERT con modelado de lenguaje enmascarado**
(*masked language modeling*, MLM) `[E]`. La diversidad aparente del campo es
sobre todo diversidad de datos de preentrenamiento y de tokenización, no de
arquitectura. Las excepciones —DGRNA con Mamba2, GenerRNA con GPT y codificación
por pares de bytes, RFamLlama con arquitectura Llama, RNA-MSM con
MSA-Transformer— son minoría, y una de ellas, RNA-MSM, es precisamente la que
mejor rinde en estructura.

El catálogo completo, con arquitectura, escala, datos, objetivo, tokenización,
tareas evaluadas, disponibilidad de pesos, licencia, artículo y fecha de cada
modelo, está en `modelos.json`. Acá se discute sólo lo que cambia una decisión.

### 1.2 El lado del ADN

**Nucleotide Transformer** (Dalla-Torre et al., *Nature Methods* 22(2):287–297,
2025) es la referencia obligada `[E]`. Familia BERT con enmascarado al 15 %,
tokenización en **6-meros no solapados** con vocabulario de 4104 tokens, y cuatro
variantes de primera generación —genoma humano de referencia 500M, 1000 Genomas
500M, 1000 Genomas 2,5B y multiespecie 2,5B— más cuatro de segunda generación de
50M a 500M, de las cuales la de 250M da el mejor coeficiente de correlación de
Matthews promedio (0,769). Los datos: GRCh38 con unos 3,2 Gnt, los 3202 genomas
humanos del proyecto 1000 Genomas con 20,5 Tnt, y 850 especies con 174 Gnt.
Trescientos mil millones de tokens en la versión 1 y hasta un billón en la 2, con
128 GPU A100 durante 28 días. Contexto de 6 kb en la versión 1 y 12 kb en la 2.
Se evaluó en 18 tareas: 10 de marcas de histonas, 3 de promotores, 2 de
*enhancers* y 3 de empalme, con validación cruzada de 10 pliegues.

Lo que importa de ese artículo no es el ranking sino las **limitaciones que los
propios autores declaran**: los modelos supervisados con arquitectura optimizada
siguen siendo superiores en algunos escenarios, el alcance de la atención es
limitado, y la región 3'UTR queda mal separada en el espacio de *embeddings*
`[E]`. Y advierten de posible fuga de datos (*data leakage*) en Enformer, uno de
los competidores con los que se comparan. Es un artículo honesto; la lectura
promocional del campo es la que se saltea esos párrafos.

**DNABERT-2** (Zhou et al., arXiv 2306.15006, ICLR 2024) es relevante por una
decisión de diseño: reemplaza los k-meros por **codificación por pares de bytes**
(*byte-pair encoding*, BPE), con el argumento de reducir el desbalance de tokens
raros, y logra el estado del arte comparado con unas 21 veces menos parámetros y
unas 92 veces menos tiempo de GPU de preentrenamiento `[R]`, sólo computacional.
Su benchmark propio, GUE, tiene 36 conjuntos sobre 9 tareas multiespecie con
longitudes de 70 a 10.000 nt.

**Evo 2** (Brixi et al., bioRxiv 10.1101/2025.02.18.638918, con versión en
*Nature*) es el extremo de escala: 7B y 40B de parámetros, arquitectura
StripedHyena 2, contexto de un millón de tokens a resolución de nucleótido,
corpus OpenGenome2 de 8,8 billones de tokens, pesos bajo Apache 2.0 `[R]`. Es el
único modelo del catálogo cuya licencia permite uso comercial sin restricción.
Sus limitaciones declaradas son instructivas: rinde mal en proteínas virales
humanas, atribuido en parte a la exclusión deliberada de virus de eucariotas del
corpus; las secuencias eucariotas que genera tienen menor densidad de ARN de
transferencia y de rasgos génicos que el genoma nativo de levadura; y las
secuencias generadas pueden ser "semánticamente válidas" sin similitud
significativa con ninguna natural `[R]`.

Un detalle operativo que vale más que cualquier métrica: **Evo quedó fuera de la
comparación de Wang et al. porque su implementación oficial no provee código para
extraer *embeddings* ni mapas de atención** `[E]`. Un modelo que no se puede
sondear no se puede auditar, y para nuestro criterio de decisión eso lo descalifica
antes de mirar su rendimiento.

### 1.3 El lado del ARN

De los modelos de clase I, los que importan para nuestro problema son cuatro.

**RNA-FM** (Chen et al., arXiv 2204.00300) es el más usado como proveedor de
*embeddings*: 12 capas, 640 de dimensión oculta, 99M de parámetros, 23,7M de
secuencias de ncRNA de RNAcentral100; la variante mRNA-FM tiene 12 capas, 1280 de
dimensión, 239M de parámetros y 45M de secuencias codificantes. Repositorio MIT,
pesos en Hugging Face. Hay un punto sin resolver: **el repositorio oficial afirma
que el modelo se presentó originalmente en *Nature Methods*, pero el enlace apunta
al artículo de RhoFold, no al de RNA-FM**, así que queda `[?]` si RNA-FM tiene
versión revisada por pares propia o sigue siendo preprint.

**RiNALMo** (Penić et al., *Nature Communications* 16:5671, 2025) es la mejor
opción si se quisiera usar un modelo de ARN: tres tamaños (33M, 148M, 651M), 36M
de secuencias de RNAcentral, nt, Rfam y Ensembl, **código Apache 2.0 y parámetros
del modelo bajo CC BY 4.0**, verificado en el repositorio oficial `[E]`. Es la
única licencia de pesos del catálogo que es a la vez abierta, permisiva y
explícita.

**ERNIE-RNA** (Yin et al., bioRxiv 10.1101/2024.03.17.585376, con versión en
*Nature Communications*) introduce un sesgo de atención informado por
apareamiento de bases, con 86M de parámetros sobre 20,4M de secuencias. Su
resultado más citado es que, **en cero disparos y leyendo directamente el mapa de
atención**, alcanza F1 de 0,55 en estructura secundaria sobre bpRNA-1m, superando
a RNAfold y RNAstructure ajustados sobre ese mismo conjunto de entrenamiento
`[R]`, sólo computacional. Ajustado, mejora a UFold en 14,4 % de F1 binario hasta
0,748 con menos de un quinto de los parámetros. El artículo es CC BY-NC-ND 4.0,
es decir **no comercial y sin derivados**.

**AIDO.RNA** (Zou et al., bioRxiv 10.1101/2024.11.28.625345) es el más grande
específico de ARN: 1,6B de parámetros, 32 capas, 32 cabezas, RoPE, SwiGLU,
tokenización de un nucleótido con vocabulario de 16 tokens, 41,5M de secuencias
de RNAcentral v24.0 (unos 30 Gnt, longitud media 728 nt), seis épocas de MLM al
15 %. Reporta estado del arte en 24 de 26 conjuntos de su propio benchmark
`[R]`, sólo computacional. Una decisión de los autores vale la pena registrarla
porque contradice el instinto de escala: **eligieron RNAcentral sobre MARS porque
cerca del 85 % de MARS es escopeta de genoma completo**, y concluyeron que la
calidad importó más que la cantidad `[R]`.

Y hay un quinto que el relevamiento previo no tenía y que es el más relevante
para el lado del maíz: **PlantRNA-FM** (Yu, Deng, Zhang et al., *Nature Machine
Intelligence* 6:1616–1625, 2024). Treinta y cinco millones de parámetros —el más
chico de todos los que acá se discuten—, 12 capas, 24 cabezas, dimensión 480,
preentrenado sobre transcriptomas de **1124 especies de plantas** de la
iniciativa OneKP, integrando secuencia, **estructura predicha con RNAfold** y
anotación de CDS y UTR. En anotación de región génica alcanza F1 de **0,974
contra 0,639** del mejor modelo previo, comparado contra DNABERT-2, RNABERT,
Nucleotide Transformer, ESM2 y cdsBERT `[R]`. Y, cosa rara en este campo, los
motivos de ARN asociados a traducción que el modelo identificó fueron
**validados experimentalmente** por los autores `[R]`. El artículo es CC BY 4.0;
la licencia de los pesos no está declarada en el artículo `[?]`.

### 1.4 La crítica independiente, que es lo que el prompt pide buscar

Acá está el contenido que distingue este relevamiento de un resumen de
divulgación. Cuatro evaluaciones hechas por terceros, con cuatro diseños
distintos, llegan a conclusiones compatibles entre sí y bastante más frías que
los artículos originales.

**Tang, Somia, Yu y Koo** (*Genome Biology* 26:203, 2025) hicieron lo que nadie
había hecho: **congelar los pesos**. En vez de ajustar finamente cada modelo a
cada tarea —que es lo que hacen todos los benchmarks previos—, sondearon las
representaciones tal como salen del preentrenamiento, en seis tareas de genómica
funcional específicas de tipo celular: actividad regulatoria por lentiMPRA,
unión de factores de transcripción por ChIP-seq, efecto de variantes en cero
disparos, unión de proteínas de unión a ARN por eCLIP-seq, potencial de
elongación de la ARN polimerasa II por INSERT-seq, e interpretación por mapas de
atribución. Cuatro modelos: Nucleotide Transformer, DNABERT-2, HyenaDNA y un GPN
propio. Líneas base: one-hot con CNN, MPRAnn, un ResNet muy ajustado y Sei, un
modelo fundacional **supervisado** preentrenado sobre 21.907 perfiles de
cromatina.

El resultado, textual: las representaciones de los modelos de lenguaje genómico
"provided little to no advantage over standard one-hot encoded sequences"
`[E]`, sólo computacional. Dos corolarios que importan más que el titular:

- **El token CLS, que es la forma habitual de resumir una secuencia en un vector,
  codifica información "only marginally more informative than bag-of-dinucleotide
  statistics"** `[E]`. Cualquier tubería que use el CLS como representación
  compacta está, en la práctica, usando frecuencias de dinucleótidos con pasos
  extra.
- Los rasgos cis-regulatorios específicos de tipo celular **se aprenden durante el
  ajuste fino, no durante el preentrenamiento**, y el valor del preentrenamiento
  puede estar sobre todo en inicializar el modelo con estadística de secuencia de
  bajo nivel `[E]`.

Y un resultado de escala que contradice la narrativa dominante: GPN, que es
convolucional, y HyenaDNA, que es un modelo de espacio de estados liviano,
superaron consistentemente a los modelos fundacionales más grandes. Los autores
concluyen que "simply scaling model size may only incrementally improve
performance in regulatory genomics" y que lo que pesa son los sesgos inductivos
de la arquitectura `[E]`. Los autores declaran además una autocrítica: usaron
particiones aleatorias, que pueden favorecer a las CNN sobre secuencia cruda al
permitirles aprender patrones homólogos compartidos entre particiones.

**BEND** (Marin et al., ICLR 2024) ataca desde el otro lado: compara catorce
modelos preentrenados de seis fuentes no contra one-hot sino contra **métodos
expertos del dominio**, en siete tareas sobre el genoma humano. El resultado es
mixto y vale leerlo con los números: en búsqueda de genes, AUGUSTUS llega a 0,80
y el mejor modelo de lenguaje (NT-MS) a 0,68, con la CNN de dos capas en 0,00
—no aprende—; en anotación de *enhancers* **todos** fracasan, con Enformer en
0,07 y los modelos entre 0,02 y 0,06; en accesibilidad de cromatina BASSET llega
a 0,85 y DNABERT lo iguala; en metilación CpG BASSET 0,93 y NT-MS 0,92; en efecto
de variantes sobre enfermedad NT-MS (0,77) **supera** a DeepSEA (0,56) `[E]`,
sólo computacional. Conclusión de los autores: los modelos "do not offer
consistent improvements over all included tasks and can fall short of surpassing
specialized existing prediction methods".

De BEND sale además la limitación que más directamente nos toca, declarada por
los propios autores: BEND es **sólo humano**, y "an important question that
remains unanswered is whether DNA LMs can aid with generalization across
different organisms" `[E]`. La transferencia entre organismos —que es exactamente
lo que necesitaríamos para usar un modelo humano o de planta en un hemíptero— no
está medida por nadie en este benchmark, y los autores la dejan como trabajo
futuro.

**BEACON** (NeurIPS 2024) hace lo mismo del lado del ARN, con trece tareas
agrupadas en estructura, función e ingeniería. Dos resultados:

- Las líneas base ingenuas son fuertes: "ResNet, which has only been trained on
  downstream tasks, can outperform most if not all language models on some
  tasks", y la LSTM supera a las demás líneas base ingenuas en **9 de 13** tareas
  `[E]`.
- Los modelos de lenguaje de ARN superan al estado del arte previo específico de
  tarea en **8 de 13** tareas, y quedan claramente cortos en mapa de contactos,
  mapa de distancias, degradación de vacunas y CRISPR dentro y fuera de blanco
  `[E]`.

El número de BEACON que más pesa para nuestro problema está en la tarea CRI-Off,
predicción de efecto **fuera de blanco** de CRISPR, medida en correlación de
Spearman: el estado del arte específico llega a 12,6, una CNN ingenua a 11,40, la
LSTM a 8,60, y **todos los modelos de lenguaje de ARN quedan entre 2,49 y 5,00**
—RNA-FM 2,49, RNA-MSM 3,85, UTRBERT-3mer 4,48 `[E]`, sólo computacional. No es
la misma tarea que nuestro tamizaje de efectos fuera de blanco, pero es la más
parecida que está medida: predecir, desde secuencia, la consecuencia de un
apareamiento imperfecto. Y en esa tarea los modelos fundacionales rinden **la
mitad o menos que una CNN entrenada desde cero**.

**Wang et al.** (bbag098, 2026) completan el cuadro con 21 modelos de ARN
evaluados estrictamente en cero disparos, en tres tareas ligadas cada una a una
parte distinta del modelo: estructura desde los pesos de atención, clasificación
desde los *embeddings*, aptitud mutacional desde los *logits*. Tres hallazgos:

1. **RNA-MSM, que usa alineamientos múltiples y fue entrenado con menos de 4000
   familias de Rfam, tiene el mejor F1 mediano de su clase, superando a AIDO.RNA
   de 1,6B en 9,0 %** `[E]`. Información evolutiva por encima de escala.
2. **Hay un compromiso real entre representaciones**: los modelos buenos en
   estructura son peores en clasificación o en aptitud, y viceversa. "Different
   biological signals are not automatically aligned in current RNA LMs" `[E]`.
3. En aptitud mutacional en cero disparos —la tarea más parecida a "predecir el
   efecto de una secuencia que nadie midió"— el rendimiento absoluto es pobre
   para todos: **MCC medio por debajo de 0,20, AUC por debajo de 0,64 y
   correlación de Spearman por debajo de 0,27** `[E]`, sólo computacional.

Y un cuarto hallazgo que no es crítica sino pista constructiva: MP-RNA y
PlantRNA-FM rinden bien pese a tener poco ncRNA en sus datos, y los autores lo
atribuyen explícitamente a que **incorporan estructura secundaria calculada con
ViennaRNA durante el preentrenamiento y la inferencia** `[E]`. Dicho de otro
modo: dentro de los modelos fundacionales de ARN, los que mejor funcionan son los
que le meten termodinámica clásica adentro.

**NABench** (Li et al., arXiv 2511.02888) agrega escala a la misma conclusión:
162 ensayos de alto rendimiento, unos 2,6 millones de secuencias mutadas de
familias de ADN y ARN, 29 modelos fundacionales evaluados en cero disparos, pocos
disparos, transferencia y supervisado, con el hallazgo de que el rendimiento
varía por tarea y por tipo de ácido nucleico, con modos de falla distintos según
la decisión de modelado `[R]`, sólo computacional. Su motivación declarada es la
misma que sostiene todo este apartado: los conjuntos previos eran heterogéneos y
con preprocesamiento inconsistente, lo que impedía comparaciones justas.

### 1.5 Licencias, que deciden más que las métricas

Para un equipo que podría querer que su trabajo sirva después, la licencia no es
un detalle administrativo. Verificado directamente en las tarjetas de modelo y
repositorios oficiales:

- **Nucleotide Transformer v2 250M multiespecie: CC BY-NC-SA 4.0, es decir NO
  comercial** `[E]`. Es la licencia más restrictiva del catálogo y afecta al
  modelo más citado.
- **RiNALMo: código Apache 2.0, parámetros CC BY 4.0** `[E]`. Pesos en Zenodo.
- **Evo 2 7B: Apache 2.0** `[E]`.
- **RNA-FM: repositorio MIT** `[E]`.
- **gRNAde: código MIT** `[E]`.
- **AIDO.RNA: licencia no declarada en el texto del artículo** `[?]`.
- **PlantRNA-FM: artículo CC BY 4.0, licencia de pesos no declarada** `[?]`.

### 1.6 Qué se transfiere desde los modelos de proteína

El prompt pide mencionarlos sólo en la medida en que su metodología sea
transferible, y hay un dato que sí lo es. En la comparación de Wang et al., ESM2
evaluado en contactos de proteína da F1 medio de 0,672, 0,663, 0,675, 0,677,
0,623 y 0,636 para 8M, 35M, 150M, 650M, 3B y 15B de parámetros respectivamente
`[E]`. Es decir: **prácticamente independiente del tamaño, y con los dos modelos
más grandes por debajo de los medianos.** En ARN el efecto de escala existe pero
es moderado —RiNALMo de 651M mejora 28,3 % en mediana sobre la versión de 148M, y
AIDO.RNA de 1,6B mejora 32,2 % sobre la de 648M—, aunque con un matiz que ya
apareció: AIDO.RNA de 1,6B mejora en estructura y **empeora** en clasificación
respecto de la versión de 650M `[E]`.

La metodología transferible, entonces, no es "hacer el modelo más grande". Es la
otra: **ProtRNA se construyó por transferencia desde un modelo de proteína**, y
el patrón de usar un modelo preentrenado como extractor de características que
alimenta una cabeza supervisada chica —el patrón de OligoFormer— viene
directamente de ahí.

---

## 2. Predicción de estructura de ARN con aprendizaje profundo

Esta sección importa de manera directa y no abstracta: **la accesibilidad del
sitio blanco es uno de los determinantes clásicos de la eficacia del dsRNA**, y
la accesibilidad se calcula a partir de una predicción de estructura. Si la
predicción es mala, el término es ruido con apariencia de física.

### 2.1 Estructura secundaria: qué reemplaza el aprendizaje profundo y qué no

El resultado fundacional de la crítica es de **Szikszai, Wise, Datta, Ward y
Mathews** (*Bioinformatics* 38(16):3892–3899, 2022), con un título que es la
conclusión: los modelos profundos de estructura secundaria de ARN
(probablemente) no generalizan entre familias. Sobre ArchiveII, 3865 ARN en 9
agrupamientos tras quitar 109 secuencias de más de 512 nt, el F1 medio cae de
**0,72 con validación cruzada intra-familia a 0,50 con validación cruzada
dejando una familia afuera** —una caída del 36 %—, mientras que RNAstructure, el
método termodinámico, se queda en 0,60 de manera estable `[E]`, sólo
computacional. Reentrenados bajo el protocolo honesto, MXfold2 llega a 0,51 y
UFold a 0,44, con UFold alcanzando 0,80 en telomerasa pero hundiéndose en ARNt y
en SRP. De ocho modelos analizados, **sólo dos se pudieron reentrenar**, lo que
es en sí un dato sobre el estado de la reproducibilidad del subcampo.

Las recomendaciones de ese trabajo son las que después adoptamos como protocolo:
validación cruzada por familia, reportar por familia, particionar por clan de
Rfam además de por familia, no solapar familias en la búsqueda de
hiperparámetros, y construir conjuntos más grandes.

El benchmark independiente más completo del lado de los modelos de lenguaje es el
de **Zablocki et al.** (*Briefings in Bioinformatics* 26(2) bbaf137, 2025), que
evalúa seis modelos de ARN en estructura secundaria. Los números, por conjunto:

- **ArchiveII**: ERNIE-RNA 0,95, RiNALMo 0,95, RNA-FM 0,91, RNAErnie 0,76,
  RNA-MSM 0,74, RNABERT 0,62, one-hot 0,57, y sincFold —un modelo supervisado
  específico— 0,97.
- **bpRNA TS0**: ERNIE 0,68, RiNALMo 0,64, RNA-FM 0,52, LinearPartition-V 0,53,
  one-hot 0,35.
- **PDB-RNA, baja homología, 62 secuencias**: **todos los modelos de lenguaje por
  debajo de 0,40, one-hot entre los tres mejores, y LinearPartition-V en 0,67**.
- **bpRNA-new**: el método clásico 0,67, y sólo ERNIE lo iguala; RiNALMo cae
  a 0,44.
- **Validación dejando una familia afuera sobre ArchiveII**: RiNALMo y ERNIE
  ganan en ARNt (0,86 y 0,84 contra 0,70) y en 5S (0,82 y 0,84 contra 0,73) y en
  tmRNA (0,73 contra 0,42); el clásico gana en 23S (0,74) y 16S (0,58); y en
  telomerasa **todos los modelos de lenguaje quedan por debajo de 0,15 contra
  0,45 del clásico**.
- Pares no canónicos: F1 mediano por debajo de 0,2 para todos.

La conclusión literal de los autores es la frase que debería gobernar cualquier
decisión de diseño en este campo: **bajo baja homología, ningún modelo de
lenguaje de ARN mejora significativamente sobre one-hot** `[E]`, sólo
computacional.

A eso se suma la crítica metodológica del grupo de ViennaRNA, **Flamm et al.**
(*Frontiers in Bioinformatics* 2:835422, 2022), que ataca la raíz del problema:
el sesgo de los datos. En bpRNA, el 55 % de las secuencias son ARN ribosomales
del Comparative RNA Website y el 43 % viene de Rfam, y en la versión de Rfam
usada, ARNr y ARNt juntos son más del 90 % de las secuencias. **El conjunto de
referencia del subcampo está dominado por cuatro familias** `[E]`. Su propuesta
metodológica —entrenar primero sobre datos sintéticos generados desde un modelo
biofísico simplificado, donde todos los sesgos son controlables— produjo el
hallazgo más incómodo de toda esta sección: **el número de pares de bases que
predicen las redes escala de forma cuadrática con la longitud de la secuencia,
cuando una estructura secundaria sólo puede acomodar un número lineal de pares**
`[E]`, sólo computacional. El modelo no aprendió una restricción elemental del
objeto que predice.

### 2.2 Estructura terciaria: la evaluación ciega

Para estructura 3D existe una evaluación ciega oficial, que es el tipo de
evidencia más fuerte disponible: **CASP16** (Kretsch, Hummer, He et al., bioRxiv
10.1101/2025.05.06.652459; versión en *Proteins* 94:192–217, 2026). Cuarenta y
dos blancos de ácidos nucleicos aportados por 22 grupos experimentales, evaluados
sobre 65 grupos predictores de 46 laboratorios: 36 monómeros (35 de ARN y 1 de
ADN), 11 multímeros de ARN, 18 híbridos con proteína y 5 con ligando.

Los resultados `[E]`, validados experimentalmente en el sentido de que las
estructuras de referencia son experimentales y los predictores no las vieron:

- El ranking lo encabezan Vfold, KiharaLab, GuangzhouRNA-human, GeneSilico,
  CSSB_experimental y Yang-Server, y **"all top-performing groups were human
  expert predictors"**.
- AlphaFold3 en modo servidor fue superado por 8 grupos en la evaluación global y
  por 12 en monómeros de ácido nucleico; quedó 8° en blancos con alineamiento
  múltiple profundo y 19° con alineamiento superficial, y rindió mal en blancos
  con plantilla porque **AF3 no hace búsqueda de plantillas para ácidos
  nucleicos**.
- De 36 monómeros, 21 alcanzaron un plegamiento aceptable (TM-score por encima de
  0,45), pero **sólo 2 de esos lo lograron sin plantilla disponible**.
- **Ninguna estructura natural de ARN no vista superó TM-score de 0,8.** El mejor
  modelo del blanco R1283 llegó a 0,376 y el de R1252 a 0,284.
- F1 de pares no canónicos por debajo de 0,5 en promedio. Fallan pseudonudos,
  pares Watson-Crick aislados, motivos A-minor, y la estequiometría y simetría de
  los multímeros.
- La conclusión literal: **"no notable increase in nucleic acid modeling accuracy
  between previous blind challenges and CASP16"**, y la integración de
  aprendizaje profundo "has yet to result in a significant increase in prediction
  accuracy".

El mejor método de la familia profunda es **RhoFold+** (Shen et al., arXiv
2207.01586 v2, con versión en *Nature Methods*), que combina RNA-FM con un módulo
Rhoformer y uno de estructura con atención de punto invariante y diez ciclos de
reciclado, con alineamientos limitados a 256 secuencias. Sobre RNA-Puzzles, 24
blancos de cadena única: RMSD medio de 4,02 Å contra 6,32 Å de FARFAR2, y
TM-score medio de 0,57 contra 0,41 y 0,44 `[R]`. Sobre un conjunto nuevo de 76
estructuras sólo-ARN del PDB: RMSD medio de 7,74 Å, unos 2,2 Å mejor que
AlphaFold3 y 10,5 Å mejor que FARFAR2. Y 0,14 segundos por predicción en una
A100, sin contar la búsqueda de alineamientos. Sus limitaciones declaradas son
precisas: uniones con múltiples conformaciones, peor rendimiento por encima de
unos 500 nt, pseudonudos y multihélices, nulo manejo de iones y ligandos, y
dependencia del alineamiento múltiple, **lo que lo limita en ARN huérfanos o
diseñados** `[R]`.

Esa última limitación tiene una confirmación práctica, independiente y dura: el
equipo de gRNAde **descartó su filtro de autoconsistencia 3D basado en RhoFold
porque no recuperaba la geometría nativa del esqueleto** `[R]`. Un grupo que
quiso usar la herramienta para filtrar diseños la tuvo que sacar del pipeline.

### 2.3 Dónde todavía gana la termodinámica clásica

La respuesta, con los datos de arriba, es bastante nítida y se puede enunciar en
tres condiciones `[E]`:

1. **Cuando la secuencia no se parece a nada del entrenamiento.** En PDB-RNA con
   baja homología, LinearPartition supera a todos los modelos de lenguaje; en
   familias no vistas, el clásico gana en 23S, 16S y telomerasa.
2. **Cuando hace falta una cantidad física, no una clasificación.** La
   accesibilidad por conjunto de función de partición, las energías libres de
   apareamiento y autoplegado, y la asimetría de extremos son cantidades que el
   modelo termodinámico produce con un significado definido, y que ningún modelo
   de lenguaje produce.
3. **Cuando hace falta que el resultado sea auditable y reproducible en una
   notebook.** ViennaRNA corre en segundos por transcripto, sin GPU y sin
   descargar pesos de varios gigabytes.

Y hay un cuarto punto, más sutil, que surge de juntar dos hallazgos: dentro de
los modelos de ARN, los que mejor rinden en estructura en cero disparos son
**MP-RNA y PlantRNA-FM, que incorporan predicciones de ViennaRNA en el
preentrenamiento** `[E]`. No es que la termodinámica compita con el aprendizaje
profundo; es que el aprendizaje profundo que funciona en ARN tiende a llevar
termodinámica adentro.

Lo que el aprendizaje profundo sí **complementa**, y bien: clasificación de
familias de ncRNA (RNA-FM llega a 96,81 % de exactitud en BEACON contra 85,73 %
del método específico previo), sitios de empalme, sitios de modificación, y la
generación de hipótesis estructurales rápidas sobre secuencias con homólogos
conocidos `[E]`.

### 2.4 El conflicto sobre la accesibilidad, que no está resuelto

Este punto merece su propio apartado porque es donde nuestro proyecto toma una
decisión que se aparta de la literatura dominante, y conviene que el argumento
quede escrito.

**A favor de la accesibilidad como determinante:** el relevamiento revisado por
pares de aprendizaje automático para siRNA (Khodagholi y Yousefi, *NAR Genomics
and Bioinformatics* 8(3) lqag099, 2026) la describe como determinante mayor e
independiente, recomienda el conjunto por función de partición por encima de la
estructura única de mínima energía libre, y documenta el régimen de ventana
deslizante que usa DSIR (W = 80, L = 40, u = 16) `[E]`. En esa misma literatura,
la asimetría de extremos está descrita como "the most important design feature in
the entire siRNA prediction literature".

**En contra, y con el único experimento controlado en insectos:** en dsRIP
(Cedden et al., *BMC Biology*, 2025), el modelo de eficacia entrenado con
bioensayos de insecto, **la accesibilidad del ARNm no resultó un predictor
significativo** `[R]`. El propio repositorio del proyecto registra que en el
ensayo de dsRNA largo el valor fue P = 0,41. Y hay un estudio retrospectivo sobre
siRecords que tampoco encontró relación, que no pudimos abrir y queda `[?]`.

La resolución que adopta este proyecto, ya registrada en
`00_meta/CAMINOS_PROBADOS.md`, es tratar la accesibilidad como **variable
calculada y reportada, con peso cero por defecto, y medir la ablación**. Esta
sección agrega un argumento más para esa decisión: aun si la accesibilidad fuera
determinante, su estimación depende de una predicción de estructura que, en el
régimen de baja homología y de transcriptos largos de una especie sin datos, es
el régimen donde todos los métodos rinden peor.

---
## 3. Aprendizaje automático aplicado a RNAi y diseño de dsRNA

### 3.1 Son dos literaturas, y casi no se hablan

El hallazgo estructural de esta sección es que "aprendizaje automático para
RNAi" nombra dos campos separados, con comunidades, conjuntos de datos, métricas
y organismos distintos, y con muy poco tráfico entre ellos `[E]`:

- **La literatura de siRNA terapéutico humano.** Miles de puntos de datos,
  líneas celulares, lectura de inhibición normalizada, métricas de clasificación
  y regresión, transformers y redes de grafos. Su relevamiento de referencia es
  Khodagholi y Yousefi (2026).
- **La literatura de dsRNA para control de plagas.** Decenas de puntos de datos,
  bioensayos de mortalidad, insectos enteros, reglas empíricas y conteo de
  desapareamientos. Su relevamiento de referencia es Cedden (*Insect Molecular
  Biology* 35(4):364–375, 2026).

La separación no es casual, y una sola observación la explica: **el relevamiento
de siRNA no evalúa generalización entre especies y no menciona RNAi de insecto;
el relevamiento de plagas no menciona aprendizaje automático ni aprendizaje
profundo en absoluto** —la predicción de eficacia allí es por reglas `[E]`. Dos
campos maduros, publicados el mismo año, que se ignoran mutuamente. El puente
entre ellos es, hoy, territorio vacante; y también es la razón por la que no hay
ninguna garantía de que lo que funciona de un lado funcione del otro.

### 3.2 El lado humano: qué se logró y con qué trampa

**OligoFormer** (Bai, Zhong, Wang y Lu, *Bioinformatics* 40(10) btae577, 2024)
es el representante canónico, y lo abrimos en su versión preprint completa. Tres
módulos: cálculo termodinámico, módulo RNA-FM y un codificador transformer
propio. Los datos son nueve conjuntos, **todos humanos y todos de línea
celular**: Huesken con 2431 siRNA contra 34 ARNm en H1299, Takayuki con 702
contra 1 en HeLa, y siete más —Amarzguioui, Haborth, Hsieh, Khvorova, Reynolds,
Vickers, Ui-Tei— agrupados en "Mixset". La eficacia se normaliza a inhibición de
0 a 100 % y el umbral que separa positivos de negativos es el 70 % del máximo.

Los números, de la fuente primaria `[R]`, sólo computacional:

| Validación | AUC | F1 |
| --- | --- | --- |
| Intra-conjunto, Huesken, 5 pliegues | 0,8619 | 0,7584 |
| Intra-conjunto, Mixset | 0,8444 | 0,7636 |
| Intra-conjunto, Takayuki | 0,8628 | 0,577 |
| **Inter-conjunto**, entrenado en Huesken, evaluado en Mixset | **0,8153** | 0,7689 |

Y las líneas base en la misma validación inter-conjunto: DSIR 0,7483, i-Score
0,7462, s-BioPredsi 0,7374, OligoWalk 0,708, siRNAPred 0,5782.

Lo que hay que leer en esa tabla no es que OligoFormer gane. Es que **el mejor
modelo del subcampo cae de 0,8444 a 0,8153 cuando cambia de conjunto de datos
dentro de la misma especie, el mismo tipo de ensayo y la misma clase de lectura**.
Si eso pasa entre dos conjuntos de líneas celulares humanas, la pregunta de
cuánto cae entre un coleóptero y un hemíptero no es retórica.

La ablación del mismo trabajo dice algo útil para el diseño: quitar cualquier
módulo empeora, el codificador transformer es el que más aporta, y **tanto el
módulo RNA-FM como los parámetros termodinámicos mejoran el rendimiento y
aceleran la convergencia** `[R]`. Y su limitación declarada, textual: "the
limited representation and quantity of existing datasets severely limit the
effectiveness of siRNA design models and further generalization".

Un detalle que conviene no pasar por alto: el módulo de efectos fuera de blanco
de OligoFormer usa **puntajes PITA y TargetScan**, que son herramientas de
predicción de blancos de microARN, no modelos entrenados sobre datos medidos de
efecto fuera de blanco de siRNA `[R]`. Es una heurística prestada de otro
problema, presentada dentro de un pipeline de aprendizaje profundo.

El relevamiento de Khodagholi y Yousefi pone el resto del subcampo en contexto, y
tiene dos frases que valen más que las métricas que compila.

La primera es una acusación general y está en el texto: **"data leakage between
training and test sets has systematically inflated benchmark results across the
field"** `[E]`. La propuesta correctiva son los protocolos de **partición por
siRNA** y **partición por ARNm**, 70:15:15 con 10 semillas, y el efecto medido de
aplicarlos es doble: cae el rendimiento absoluto y **se achican las diferencias
entre métodos**, degradándose menos los métodos con sesgo inductivo más fuerte.
Es el mismo mecanismo que Szikszai documentó para estructura secundaria, en otro
subcampo y con otros autores.

La segunda es un hueco declarado: **"no formal uncertainty quantification methods
have been applied to siRNA efficacy prediction"**, que el relevamiento llama
posiblemente la brecha de máxima prioridad del campo, proponiendo predicción
conformal (*conformal prediction*), métodos bayesianos y escalado de temperatura
`[E]`. Y un segundo hueco: **"active learning has no dedicated siRNA
publications despite clear applicability"**.

Y una tercera conclusión, central para nuestra decisión: **"embeddings are
evidently sufficient but not necessary for state-of-the-art performance"**, con
el caso concreto de DeepSilencer alcanzando 0,858 en Mixset sólo con secuencia y
fisicoquímica, por encima del 0,845 de OligoFormer, que usa RNA-FM `[E]`. Los
modelos más fuertes del subcampo son los **híbridos de termodinámica con
representación aprendida**, no los que apilan modelo fundacional.

El resto de las métricas compiladas, para tener la escala: siRNADiscovery 0,874
de AUC en partición por siRNA con correlación de Pearson de 0,770; GNN4siRNA
0,821 y 0,679; ENsiRNA con una mejora de Pearson de alrededor del 13 %; una
regresión de soporte vectorial clásica con características de la hebra
antisentido en R = 0,719 y R² = 0,516 sobre Huesken; AttSiOff ubicando cinco
siRNA aprobados por la FDA en el 1–12 % superior de su ranking `[E]`.

### 3.3 El lado de plagas: lo único entrenado con bioensayos de insecto

**dsRIP** (Cedden et al., *BMC Biology*, 2025) es la pieza central de todo este
relevamiento para nuestro problema, y conviene ser exacto sobre qué es y qué no
es `[R]`, validado experimentalmente en parte:

- Cuatro módulos: buscador de blancos, optimizador de eficacia, minimizador de
  efectos fuera de blanco y diseñador de cebadores.
- El modelo de eficacia a nivel de siRNA es una **regresión de riesgos
  proporcionales de Cox sobre 9 características de secuencia**, entrenada con
  **31 siRNA de 21 nt** contra *Tc-gawky* de *Tribolium castaneum*, insertados en
  un esqueleto de mGFP de 232 pb, con n = 20 larvas L5 por grupo. Estadístico C
  de Harrell **0,76 (IC 95 % 0,73–0,79)**.
- Las características significativas son cuatro: **asimetría termodinámica,
  energía de autoplegado de la hebra antisentido, porcentaje de GC en los
  nucleótidos 9–14 de la antisentido, y adenina en la posición 10**.
- El modelo a nivel de dsRNA es una regresión múltiple sobre 8 genes con 3 a 4
  dsRNA cada uno, n = 25 larvas, R múltiple 0,79 con 17 grados de libertad, razón
  de riesgo 1,462 por unidad de puntaje, P = 0,003.
- Validación experimental en *T. castaneum* (8 genes), *Psylliodes chrysocephala*
  y *Leptinotarsa decemlineata*. **Todos coleópteros.**
- El módulo de efectos fuera de blanco usa Bowtie1 v1.3 y un puntaje de seguridad
  que suma impactos totales más impactos en genes esenciales con peso 20:1,
  normalizado de 0 a 100 %, con ortología por OrthoFinder sobre 83 organismos. Ese
  módulo **no está validado experimentalmente**, lo declaran los autores.
- Limitaciones declaradas: la accesibilidad del ARNm no fue predictor
  significativo, las muestras son chicas, y el puntaje promedia los efectos
  posicionales de todos los siRNA derivables.
- Datos en figshare (10.6084/m9.figshare.27490890.v1 y .27495843.v1) y lecturas
  en SRA PRJNA1157760; plataforma en dsrip.uni-goettingen.de.

Treinta y un siRNA. Ese es el tamaño del conjunto de entrenamiento honesto que
existe hoy en el subcampo de insectos, y es el número que hay que tener presente
cada vez que alguien proponga ajustar finamente un modelo de mil millones de
parámetros sobre eficacia de dsRNA.

**dsRNAEngineer** (Chen, Shi, Wang et al., bioRxiv 10.1101/2024.07.22.604585) es
la herramienta con mayor cobertura taxonómica: aloja 942 transcriptomas de NCBI,
439 de ellos RefSeq, al 5 de julio de 2024, y soporta diseño multiblanco y
multiespecie `[R]`, sólo computacional. **dsRNAmax** hace diseño multiespecie
local por k-meros `[R]`. Y la generación anterior de herramientas —si-Fi, E-RNAi,
dsCheck, dsOMG, DEQOR— figura en las tablas de los dos relevamientos con sus
limitaciones anotadas, incluyendo que **varias están discontinuadas desde 2022** y
que las que hacen predicción de eficacia la basan en **datos humanos** `[E]`.

**dsRNAPredictor** (Cheng, Xu y Jia, *Briefings in Functional Genomics*
23(6):858–865, 2024) es el único intento publicado de aprendizaje profundo sobre
eficacia de dsRNA en insectos, y es el caso de estudio de cómo no hacerlo `[R]`.
Dos problemas, cada uno suficiente:

1. **Construyó los negativos barajando fragmentos de ARNm de la misma base de
   datos.** Un clasificador puede resolver la tarea "secuencia real contra
   secuencia barajada" sin aprender absolutamente nada sobre eficacia de
   silenciamiento: le alcanza con detectar la estadística de composición de una
   secuencia biológica real.
2. **Falla donde se lo puede medir fuera de su especie de entrenamiento:** en
   quitina sintasa de *Aedes aegypti*, su mejor fragmento predicho (dsCHSA_1550)
   no coincide con el mejor fragmento experimental (dsCHSA_1928).

La fuente de etiquetas a escala del subcampo es **iBeetle-Base**, el tamizaje
genómico de RNAi de *T. castaneum*, con la limitación que el relevamiento de 2026
le anota explícitamente: **es una sola especie de coleóptero** `[E]`. De ahí sale
también el dato útil de que los procesos conservados —proteasoma, expresión
génica— son blancos más efectivos que los genes del sistema nervioso.

### 3.4 Efectos fuera de blanco: dos reglas distintas y ningún benchmark

Las dos literaturas también difieren acá, y la diferencia es operativa `[E]`:

- **Subcampo de plagas:** el criterio es conteo de desapareamientos. Coincidencia
  perfecta o hasta 2 desapareamientos; para siRNA de 21 nt, al menos 19
  nucleótidos complementarios. Se implementa con BLAST o Bowtie contra
  transcriptomas no blanco. Simple, auditable y grueso.
- **Subcampo de siRNA humano:** el criterio es la mecánica de la región semilla.
  Posiciones 2–5 esenciales para la actividad fuera de blanco, 6–8 contribuyen a
  las dos cosas, 8–14 correlacionan negativamente; el 6-mero de las posiciones
  2–7 es la característica más ampliamente predictiva, y los 7-meros y 8-meros
  dan firmas individuales más fuertes.

Las dos reglas no coinciden, y mostrar dónde difieren sobre un conjunto concreto
de candidatos ya es un aporte metodológico barato.

Las herramientas existentes del lado humano son SeedMatchR (función de
distribución acumulada empírica de enriquecimiento de semilla sobre más de 50
conjuntos de RNA-seq, con paquete en Bioconductor), Richter y Admasu (huellas
ECFP más alineamiento estructural siRNA/AGO2, sobre más de 30.000 puntos
siRNA/gen, con nueve estrategias de características de las cuales ECFP resultó la
mejor), siSPOTR, si-Fi, pssRNAit y el módulo propio de AttSiOff `[E]`.

Y sobre todas ellas pesa una frase del relevamiento: **"none of these constitutes
a community-standardized off-target benchmark"** `[E]`. No existe para efectos
fuera de blanco el equivalente a Huesken. Los recursos experimentales están
dispersos en lugar de estandarizados.

A lo que hay que sumar dos resultados que acotan cuánto se puede confiar en
cualquier predicción de este tipo:

- El relevamiento de Cedden 2026 cita un estudio en *Leptinotarsa* donde **los
  cambios transcriptómicos medidos no coincidieron con la complementariedad
  predicha in silico** `[E]`.
- En BEACON, en la tarea análoga de predicción de efecto fuera de blanco de
  CRISPR, **todos los modelos fundacionales de ARN rinden por debajo de una CNN
  simple**, con correlaciones de Spearman de 2,49 a 5,00 contra 11,40 `[E]`.

Conclusión operativa: un mapa de efectos fuera de blanco calculado desde
secuencia es un **mapa de riesgo potencial**, no una medición de efecto, y
cualquier afirmación de seguridad derivada de él sería una sobreinterpretación
`[H]`.

### 3.5 Generalización fuera del dominio de entrenamiento

El prompt pide, para cada herramienta, qué tan bien generaliza fuera de su
dominio. La respuesta honesta, para todas, es **que casi nadie lo midió**, y que
donde se midió el resultado fue malo:

| Herramienta | Dominio de entrenamiento | ¿Se midió fuera de dominio? | Resultado |
| --- | --- | --- | --- |
| OligoFormer | 9 conjuntos humanos de línea celular | Sí, entre conjuntos de la misma especie | AUC cae de 0,8444 a 0,8153 `[R]` |
| Familia de siRNA humano en general | Humano | **No entre especies.** El relevamiento no lo evalúa | Sin dato `[E]` |
| dsRIP | 31 siRNA de *T. castaneum* | Sí, a otros dos coleópteros | Validado en coleópteros; el relevamiento de 2026 anota que **falta probarlo fuera de coleópteros** `[E]` |
| dsRNAPredictor | iBeetle, *T. castaneum* | Sí, a *Aedes aegypti* | **Falló**: el mejor fragmento predicho no es el mejor experimental `[R]` |
| si-Fi, E-RNAi, DEQOR | Datos humanos | No | Figuran en el relevamiento de plagas con "basado en datos humanos" como limitación `[E]` |
| Modelos fundacionales de ADN/ARN | Humano o pan-especie | **No entre organismos.** BEND lo declara como pregunta abierta | Sin dato `[E]` |

Hay además un dato de signo, registrado por la línea R2 de este mismo proyecto a
partir de la comparación entre las dos literaturas, que es el argumento más
fuerte contra la transferencia ingenua: **el contenido de GC en las posiciones 9
a 14 de la hebra antisentido invierte su signo entre humano e insecto**, y la
accesibilidad del ARNm, pilar de la literatura humana, no resulta predictor
significativo en el único ensayo controlado en insectos `[E]`. No es que la
transferencia se degrade: en al menos un parámetro, apunta al revés.

### 3.6 El eje de diseño que ningún modelo computacional cubre

Todo lo anterior trata el diseño como **elección de un tramo de secuencia dentro
de un transcripto**. Hay un segundo eje, independiente, que la literatura
experimental está explorando activamente y que no aparece en ningún modelo de
este catálogo: **la arquitectura física de la molécula de dsRNA**.

El trabajo más reciente que lo documenta es de Muita, Damayo, Remnant et al.
(CSIRO y Universidad de Sídney, *Frontiers in Insect Science*, 17 de agosto de
2026), sobre *Varroa destructor* `[R]`, **validado experimentalmente**. Dos
diseños sobre dsRNA de extremos en lazo (*loop-ended*, ledRNA): **ledG:U**, donde
todas las citosinas de la hebra sentido se sustituyen por timinas para generar
apareamientos G-U oscilantes (*wobble*) en todo el tallo; y **led[Δ22]**, con una
deleción cada 22 nt en la hebra sentido que genera una protuberancia (*bulge*)
asimétrica en la antisentido **sin alterar la secuencia de la antisentido**.

Resultados, en dos genes blanco (*Pero*, una proteína de unión a quitina, y
*CHH*, una hormona hiperglucémica), con ledGFP como control negativo, n = 5
réplicas biológicas salvo dos condiciones con 2 y 4:

- El **doble de estabilidad** en solución de sacarosa y dentro de abejas adultas
  respecto del dsRNA convencional.
- Silenciamiento del blanco con reducción de **36 a 86 %** y aumento de
  mortalidad de ácaros de **32 a 56 %**, descritos por los autores como
  "variables pero mejorados" respecto del dsRNA convencional.
- Secuenciación de ARN pequeños: procesamiento efectivo, cobertura completa de
  siRNA sobre la región blanco, pico de tamaño en **22–24 nt** y sesgo hacia la
  hebra antisentido.
- Alcance declarado: **sólo laboratorio**; hace falta más optimización de la
  combinación gen–diseño; y los autores reconocen que faltó probar genes control
  con el diseño ledRNA para descartar que el propio diseño estructural tenga
  efectos no dirigidos sobre la mortalidad.

Por qué esto importa para un equipo computacional: la hebra antisentido —que es
la que determina especificidad y por lo tanto el perfil de efectos fuera de
blanco— **no cambia** en el diseño led[Δ22]. Es decir, la estabilidad se mejora
sin tocar el eje sobre el que trabaja cualquier modelo de secuencia. Son dos
decisiones ortogonales, y una propuesta de diseño que sólo optimiza la secuencia
está ignorando la mitad del espacio de diseño que la literatura experimental ya
demostró que rinde `[H]`.

---

## 4. Modelos de lenguaje grandes como herramienta de trabajo

Esta sección pide separar lo evaluado de lo demostrado, y el campo hace esa
separación especialmente difícil porque los artículos más visibles son los que
tienen la evaluación más débil. El orden de abajo va de más evaluado a menos.

### 4.1 Lo que está medido con rigor: los benchmarks de agentes

**BixBench** (Mitchener, Laurent, Andonian et al., arXiv 2503.00096) es la
evaluación más dura y la más relevante para nosotros, porque mide exactamente lo
que un equipo de cuatro personas podría querer delegar: **análisis de datos
biológicos reales**. Más de 50 escenarios tomados de análisis reales, con unas
300 preguntas abiertas. El resultado `[E]`, sólo computacional en el sentido de
que la referencia son análisis ya hechos: los modelos de frontera alcanzan
**alrededor del 17 % de exactitud en respuesta abierta**, y en formato de opción
múltiple rinden **no mejor que el azar**. La conclusión de los autores es que los
agentes actuales no son confiables para análisis bioinformático riguroso.

Ese número —17 %— es la cota superior realista para cualquier propuesta que
plantee "un agente hace el análisis". No invalida usar asistencia de modelos de
lenguaje; invalida presentarla como resultado autónomo.

**Biomni** (Huang, Zhang, Wang et al., bioRxiv 10.1101/2025.05.30.656746) es el
agente biomédico de propósito general más completo publicado: un entorno con 150
herramientas, 105 paquetes y 59 bases de datos, un agente sobre CodeAct con
recuperador, y ejecución de Python, R y Bash. Sus números `[R]`:

- LAB-Bench DbQA: 74,4 % contra 74,7 % de humanos y 40,8 % de una línea base
  ReAct con código.
- LAB-Bench SeqQA: 81,9 % contra 78,8 % de humanos.
- Subconjunto de biología del benchmark HLE, 52 preguntas: **17,3 %**, contra
  6,0 % del modelo base, 12,8 % de un agente de código y 12,2 % de un agente de
  literatura.
- Ocho tareas nuevas: mejora relativa del 402,3 % sobre el modelo base.

Hay que leer esos números con tres advertencias que están en el propio artículo:
**LAB-Bench se evaluó sobre un subconjunto del 12,5 % por costo de API**; la
validación húmeda del trabajo es **un solo experimento** (clonado de un sgRNA
contra *B2M* en lentiCRISPR v2 Blast, con dos colonias verificadas por Sanger); y
las demostraciones grandes —458 archivos de dispositivos vestibles con 30
participantes, y un multioma esquelético de unos 336.000 núcleos en 10 pasos y
unas 5 horas— son **enteramente computacionales**, con los genes resultantes
(*AUTS2*, *ZFHX3*, *PBX1*) explícitamente presentados como hipótesis. Los autores
declaran que el sistema no es de nivel experto en todas las categorías, que
flaquea en juicio clínico matizado, razonamiento experimental novedoso y síntesis
profunda, y que necesitó depuración por desajustes de nombres de variables.
Registramos además dos inconsistencias internas del texto: el resumen dice
"decenas de miles de publicaciones" donde los resultados dicen 2500 preprints de
bioRxiv, y los resultados hablan de 10 tareas de clonado donde los métodos dicen
20 `[?]`.

### 4.2 Extracción de información desde literatura

Este es el uso con mejor relación entre evidencia y utilidad para nuestro equipo,
y además es la tarea que el propio equipo eligió primero. **PaperQA2**
(Skarlinski, Cox, Laurent et al., arXiv 2409.13740) resuelve un pendiente que
este relevamiento tenía registrado sin abrir, y la lectura cuidadosa cambia el
titular.

El artículo se llama "los agentes de lenguaje alcanzan síntesis superhumana del
conocimiento científico". Los números dicen algo más preciso `[R]`:

| Sistema | Precisión en LitQA2 | Exactitud en LitQA2 |
| --- | --- | --- |
| PaperQA2 (n = 3 corridas) | **85,2 % ± 1,1 %** | 66,0 % ± 1,2 % |
| Anotadores humanos con doctorado (n = 9) | 73,8 % ± 9,6 % | 67,7 % ± 11,9 % |

La precisión es la fracción de aciertos **entre las preguntas que el sistema
contestó**; la exactitud es sobre el total. La diferencia es significativa en
precisión (t(8,6) = 3,49; p = 0,0036) y **no es significativa en exactitud**
(t(8,5) = −0,42; p = 0,66). El sistema logra la precisión superior
**absteniéndose en el 21,9 % de los casos** y usando 14,5 artículos por pregunta
en promedio. Los humanos trabajaron con acceso completo a internet y a las
suscripciones de su institución, una semana de plazo e incentivo económico.

Traducido a nuestra situación: **un sistema así no lee más literatura por
nosotros, lee con menos errores cuando decide contestar.** Es un triador
(*triage*), no un sustituto del curado. Para construir el conjunto retrospectivo
de la línea L2 eso es exactamente lo que sirve —y exactamente lo que no alcanza.

Los otros dos resultados del mismo trabajo refuerzan la lectura. WikiCrow,
generando artículos tipo enciclopedia sobre genes humanos, bajó las afirmaciones
"citadas y no sostenidas" de 24,9 % a **13,5 %** y las no citadas de 13,6 % a
3,5 %, con precisión de 86,1 % contra 71,2 %, todo juzgado a ciegas por expertos
sobre 375 afirmaciones `[R]`. Mejor que Wikipedia, sí; pero **13,5 % de
afirmaciones citadas y no sostenidas es una de cada siete**, y para un proyecto
cuya regla número uno es no citar lo que no se abrió, esa tasa es inaceptable sin
verificación humana. ContraCrow detectó 2,34 ± 1,99 contradicciones por artículo
sobre 93 artículos de biología, de las cuales **el 70 % fueron validadas por
expertos** `[R]`: el 30 % restante, no.

### 4.3 Agentes de laboratorio y generación de hipótesis

**Coscientist** (Boiko, MacKnight, Kline y Gomes, *Nature* 624(7992):570–578,
2023) es el trabajo fundacional, con planificador más herramientas de búsqueda
web, Python en Docker aislado, documentación por búsqueda vectorial y ejecución
física sobre un robot Opentrons OT-2 y la nube de Emerald Cloud Lab. Lo que
efectivamente se hizo en el mundo físico: manejo de líquidos, espectroscopía
UV-Vis con colorantes, **una** reacción de Suzuki y **una** de Sonogashira con
verificación por GC-MS, y HPLC con un estándar de cafeína `[R]`, validado
experimentalmente en un sentido acotado.

Las acotaciones son grandes y están en el artículo: **no se reportan rendimientos
para la Suzuki ni la Sonogashira**, sólo que el GC-MS indicó formación de
producto; las optimizaciones de Suzuki en flujo y Buchwald-Hartwig usaron
conjuntos de datos existentes **como tablas de consulta, sin experimentos
nuevos**; la biblioteca grande de compuestos fue computacional con RDKit; el
sistema no estaba completamente automatizado, con placas movidas a mano; hubo un
error de nombre de método en el agitador-calentador; el UV-Vis necesitó un
*prompt* guía; y los datos, el código y los *prompts* **no se liberaron completos
por razones de seguridad y doble uso**, con un repositorio público que los
autores aclaran que puede no reproducir los resultados `[R]`.

**Robin** (Ghareeb, Chang, Mitchener et al., arXiv 2505.13400) combina agentes de
búsqueda bibliográfica y de análisis de datos en un ciclo semiautónomo con
laboratorio humano en el circuito (*lab-in-the-loop*). Partiendo de degeneración
macular seca llegó a la fagocitosis del epitelio pigmentario de la retina y
propuso ripasudil, un inhibidor de ROCK de uso clínico; el RNA-seq que el propio
sistema propuso mostró sobreexpresión de *ABCA1* `[R]`, validado
experimentalmente. Los autores afirman que todas las hipótesis, planes
experimentales, análisis y figuras del texto principal fueron producidos por el
sistema. La página del preprint no declara limitaciones ni código.

**Co-Scientist** (Gottweis, Weng, Daryin et al., arXiv 2502.18864) es el caso más
fuerte publicado, y el que más cuidado requiere al leer. Es un sistema multiagente
con paradigma "generar, debatir, evolucionar": autodebate, selección por torneo y
refinamiento iterativo, con escalado de cómputo en tiempo de inferencia. Tres
validaciones húmedas `[R]`, validadas experimentalmente:

1. Reposicionamiento de fármacos para leucemia mieloide aguda, con citotoxicidad
   selectiva **in vitro** a concentraciones clínicamente relevantes.
2. Blancos epigenéticos nuevos para fibrosis hepática, con actividad antifibrótica
   y regeneración de hepatocitos en **organoides hepáticos humanos**, incluyendo
   un fármaco aprobado por la FDA.
3. En microbiología, la recapitulación independiente de un mecanismo de
   transferencia de elementos genéticos móviles entre bacterias que en ese
   momento estaba sin publicar.

Y las limitaciones declaradas por los propios autores, que son las que hay que
citar cuando alguien proponga un agente como método `[E]`:

- El conocimiento está limitado a **literatura de acceso abierto**, con omisión
  de arte previo tras muros de pago y, textual, **"a systemic lack of access to
  negative experimental results"**. Para un problema como el nuestro, donde el
  conjunto de dsRNA publicados está truncado por sesgo de publicación, ese sesgo
  se hereda directamente.
- La calidad depende de la calidad mixta y contradictoria de la literatura
  fuente, con "risk of propagating erroneous or irreproducible findings".
- Textual: **"the validation of Co-Scientist's hypotheses, while successful,
  remains preliminary"**.
- Autocrítica metodológica explícita: hacen falta "more objective and automated
  evaluation metrics that move beyond current ranking systems". Es decir, los
  propios autores reconocen que **el puntaje Elo del torneo interno, que es su
  métrica principal sobre 203 objetivos de investigación, es una autoevaluación
  del sistema y no alcanza**.
- Advertencia final: el uso impropio sin revisión por pares ni salvaguardas podría
  agravar la crisis de reproducibilidad por producción de artefactos de baja
  calidad.

### 4.4 Dónde está la línea entre evaluado y demostrado

Resumiendo la sección en la distinción que el prompt pide `[H]`, como lectura
nuestra de las fuentes de arriba:

- **Evaluado con rigor y con resultado modesto:** análisis bioinformático
  autónomo (BixBench, ~17 %), preguntas de conocimiento de laboratorio (LAB-Bench
  vía Biomni, paridad humana en dos subconjuntos, sobre el 12,5 % del
  benchmark), recuperación y síntesis de literatura (PaperQA2, superioridad en
  precisión y paridad en exactitud).
- **Validado experimentalmente pero en escala de demostración:** Coscientist (dos
  reacciones sin rendimientos reportados), Biomni (un clonado), Robin (una
  cascada con un fármaco reposicionado), Co-Scientist (tres casos, declarados
  preliminares por sus autores).
- **Demostración sin evaluación seria:** las métricas internas de calidad de
  hipótesis basadas en torneos del propio sistema, y toda afirmación de
  "autonomía" en trabajos donde las placas se mueven a mano o donde el código no
  se liberó completo.

La consecuencia práctica para nuestro equipo es estrecha y concreta: **usar
asistencia de modelos de lenguaje para triar literatura y para escribir código es
razonable y está respaldado; presentar un agente como el método de la propuesta
no lo está** `[H]`.

---
## 5. Diseño generativo e inverso de secuencias funcionales

### 5.1 Qué funciona hoy, con validación húmeda

El mejor caso publicado de diseño inverso de ARN es **gRNAde** (Joshi, Gianni,
Kwok, Mathis, Liò y Holliger, Cambridge y MRC LMB; bioRxiv
10.1101/2025.11.29.691298 v2, con versión previa en ICLR 2025). Es un modelo
geométrico de grafos: cada nucleótido es un nodo, con aristas de vecino de
esqueleto, de pares de bases y pseudonudos detectados con DSSR, y de vecindad
tridimensional; codificador y decodificador GVP-GNN equivariantes SE(3) de cuatro
capas cada uno, con decodificación autorregresiva al estilo ProteinMPNN. Admite
como entradas opcionales la estructura secundaria, el esqueleto 3D y una
restricción parcial de secuencia. Entrenado sobre 4211 estructuras de ARN de
hasta 500 nt del PDB con resolución de 4,0 Å o mejor, curadas por RNASolo, con
corte al 31 de octubre de 2023, descartando las coordenadas 3D en un 50 %
aleatorio de los ejemplos por época.

Los resultados `[R]`, y los de la segunda tanda **validados
experimentalmente**:

- **Eterna OpenKnot, ronda 3** (hasta 100 nt, 10 blancos naturales y 10
  sintéticos), que es una competencia ciega con lectura experimental: gRNAde
  acertó 100 % y 90 %; Rosetta 40 % y 70 %; RFdiffusion 80 % y 60 %. En la ronda
  4 (hasta 240 nt): gRNAde 67 % y 70 %, RFdiffusion 33 % y 50 %, y Rosetta no
  escaló.
- **Ribozima polimerasa 5TU**: una biblioteca de 1989 secuencias diseñadas; con
  15 a 19 mutaciones, **31,5 % de variantes activas contra 15,0 % del diseño
  racional filtrado y 3,0 % sin filtrar**; nueve variantes confirmadas en gel;
  una variante con 28 mutaciones activa sobre molde GAA; secuencias activas que
  difieren en casi un 20 % de la original.
- Dato que modera el entusiasmo: la recuperación mediana de secuencia nativa
  entre los diseños exitosos de la ronda 7 de OpenKnot fue de **32 % para gRNAde
  contra 72 % para expertos humanos**. El modelo acierta, pero por caminos
  distintos de los del experto.
- Código MIT, pesos y datos en Hugging Face, depósito en Zenodo. Es, junto con
  RiNALMo, lo mejor licenciado del catálogo.

Dos detalles del propio pipeline de gRNAde son, para nosotros, más informativos
que sus tasas de éxito `[R]`:

1. El tamizaje de aproximadamente **un millón de candidatas** se hizo con
   **RibonanzaNet**, no con un modelo fundacional de lenguaje ni con una
   predicción 3D.
2. **El filtro de autoconsistencia 3D basado en RhoFold se descartó porque no
   recuperaba la geometría nativa del esqueleto**, y el filtro de estructura
   secundaria no se aplicó a los blancos sintéticos porque la cabeza de
   estructura de RibonanzaNet se había ajustado sólo con secuencias naturales.

Es decir: el mejor trabajo de diseño generativo de ARN publicado **no pudo usar
la predicción de estructura profunda como filtro**, exactamente el techo que
CASP16 midió de manera independiente. Dos evidencias, una de evaluación ciega y
otra de práctica de laboratorio, apuntando al mismo límite.

### 5.2 Generación a escala de genoma

**Evo 2** demuestra la otra punta del espectro: generación de genomas
mitocondriales, de secuencias a escala de *Mycoplasma genitalium* y del
cromosoma III de levadura, además de epigenómica generativa con búsqueda en
tiempo de inferencia para controlar la accesibilidad de la cromatina `[R]`,
**sólo computacional**. Y sus propias limitaciones declaradas ponen el límite:
las secuencias eucariotas generadas tienen **menor densidad de ARN de
transferencia y de rasgos génicos que el genoma nativo**, y las secuencias
generadas **pueden ser semánticamente válidas sin similitud significativa con
ninguna natural** `[R]`. Es generación sin garantía de función.

Del lado del ARN específicamente, el catálogo registra **GenerRNA** (304M,
arquitectura GPT con codificación por pares de bytes sobre unos 16 millones de
secuencias de RNAcentral) como el modelo generativo autorregresivo de ARN, y
**AIDO.RNA** reporta mejorar a gRNAde en plegado inverso en cero disparos y con
adaptación por difusión, con alrededor de 3 % sobre 14 estructuras `[R]`, sólo
computacional.

### 5.3 Qué garantías hay, y cuál es la asimetría que decide

La respuesta corta: **ninguna garantía formal**. Ni cobertura, ni calibración, ni
cotas. Lo que hay son tasas de éxito empíricas medidas en dominios donde existe
un ensayo de alto rendimiento.

Y ahí está la asimetría que, para nuestro problema, decide la cuestión `[H]`. El
diseño generativo funciona cuando se puede **evaluar barato y en masa** lo
generado. La escala de lo que hizo falta para que el aprendizaje profundo moviera
la aguja en estructura de ARN la fija **Ribonanza** (He, Huang, Townley, Kretsch
et al., bioRxiv 10.1101/2024.02.24.581671): mediciones de mapeo químico sobre
**dos millones de secuencias de ARN**, reunidas por ciencia colaborativa vía
Eterna, con un desafío abierto en Kaggle para evaluación prospectiva y
destilación posterior en RibonanzaNet `[R]`.

Y la propia advertencia de escala de los autores de Ribonanza es el dato más
útil de todo este apartado: esas dos millones de secuencias son
**aproximadamente 400 millones de mediciones a nivel de nucleótido, con relación
señal-ruido aceptable en sólo 80 millones**, y ellos mismos escriben que esos
conjuntos **"are much smaller than the corpora of 10 billion to many trillions of
data"** que produjeron modelos transformadores en otros dominios `[R]`.

Contrastemos. El conjunto más grande de ARN funcional medido experimentalmente en
la historia del campo tiene dos millones de secuencias, y sus propios autores lo
consideran chico. El conjunto de entrenamiento de eficacia de dsRNA validado en
insecto tiene **31 siRNA**. La lectura experimental en RNAi de insecto es un
bioensayo de mortalidad con n de 20 a 40 individuos por tratamiento. No hay
ninguna forma de cerrar esa brecha con cómputo.

### 5.4 Qué requiere validación húmeda obligatoria

Enumerado explícitamente, porque es la contracara de riesgo que `CLAUDE.md` exige
y porque es lo que separa una propuesta honesta de una que vende `[H]`,
fundamentado en las fuentes de arriba:

- **Toda secuencia generada de novo.** Evo 2 declara que sus secuencias pueden
  ser válidas sin parecido con ninguna natural; gRNAde midió 31,5 % de éxito en
  el mejor caso, con biblioteca de 1989 secuencias y lectura de actividad
  ribozimática. Sin ese ensayo, una secuencia generada es una conjetura.
- **Toda afirmación de eficacia derivada de un puntaje.** El modelo de insecto
  disponible tiene estadístico C de 0,76 sobre 31 puntos; es un ordenador
  relativo, no una predicción absoluta.
- **Toda afirmación de seguridad derivada de un mapa de efectos fuera de blanco.**
  El módulo correspondiente de dsRIP no está validado experimentalmente, no existe
  un benchmark estandarizado, y hay al menos un caso publicado donde los cambios
  transcriptómicos medidos no coincidieron con la complementariedad in silico.
- **Toda transferencia entre órdenes de insectos.** Nadie la midió, y en al menos
  un parámetro el signo se invierte entre humano e insecto.

Para un equipo sin laboratorio, eso no es una lista de obstáculos: es la
especificación de qué puede afirmar y qué no. Un entregable que declare
exactamente esos cuatro límites es más defendible ante un jurado que uno que los
tape.

---

## 6. Síntesis orientada a decisión

### 6.1 El mapa, en seis conclusiones

1. **Los modelos fundacionales de secuencia rinden donde hay homología, y nuestro
   problema no la tiene.** Cuatro evaluaciones independientes con diseños
   distintos —Tang y Koo por sondeo sin ajuste fino, BEND contra métodos
   expertos, BEACON contra líneas base ingenuas, Wang et al. en cero disparos
   estricto— coinciden en que la ventaja sobre representaciones simples es
   pequeña, inconsistente o nula fuera del régimen de entrenamiento `[E]`.
2. **La termodinámica clásica no fue reemplazada en lo que nos importa.** En baja
   homología gana en estructura secundaria; en 3D, CASP16 concluye que no hubo
   aumento notable de exactitud respecto de evaluaciones ciegas anteriores; y los
   modelos de ARN que mejor rinden en estructura son los que incorporan ViennaRNA
   en el preentrenamiento `[E]`.
3. **El subcampo específico de RNAi está partido en dos literaturas que no se
   hablan**, con todos los datos a escala de un lado (humano, líneas celulares) y
   toda la relevancia biológica del otro (insecto, bioensayo), y ningún trabajo
   mide la transferencia entre ellos `[E]`.
4. **Hay dos huecos metodológicos declarados por la propia literatura y que son
   baratos de atacar:** la ausencia total de cuantificación formal de
   incertidumbre en predicción de eficacia de siRNA, llamada por su relevamiento
   "posiblemente la brecha de máxima prioridad del campo", y la ausencia de un
   benchmark comunitario de efectos fuera de blanco `[E]`.
5. **Los agentes de modelos de lenguaje son buenos triadores y malos
   analistas.** Alrededor del 17 % de exactitud en análisis bioinformático
   abierto; en literatura, superioridad en precisión pero paridad en exactitud
   contra doctorandos, lograda absteniéndose en uno de cada cinco casos `[E]`.
6. **El diseño generativo funciona donde hay un ensayo de alto rendimiento, y en
   RNAi de insecto no lo hay.** La vara la fija Ribonanza con dos millones de
   secuencias medidas que sus propios autores consideran pocas; nuestro
   equivalente son 31 siRNA `[R]`.

### 6.2 Dónde conviene pararse

De las seis conclusiones sale una recomendación que no es la que el instinto del
campo sugiere. **El lugar con mejor relación entre valor esperado y costo no es
el modelo más grande ni el más nuevo: es la capa de decisión que ninguno de los
dos subcampos construyó.**

Concretamente, tres cosas que el relevamiento muestra abiertas y que cuatro
personas sin laboratorio pueden hacer en el plazo de un Investigathón:
cuantificación de incertidumbre envuelta sobre un predictor existente,
evaluación con particiones sin fuga por gen y por especie, y un índice de riesgo
fuera de blanco ponderado por consecuencia con análisis de sensibilidad de sus
pesos. Las tres son metodológicas, las tres son auditables, y las tres atacan
huecos que la propia literatura declara.

### 6.3 Las líneas de ataque

Las cuatro propuestas, cada una con qué modelo o técnica usa, qué datos necesita
y si existen, qué se puede demostrar en el plazo, el riesgo principal y la
estimación de esfuerzo, están desarrolladas en **`lineas_de_ataque.md`**, una
página por línea, y allí está escrito el criterio de priorización, que no es
neutro. El resumen, en una tabla:

| Línea | Decisión que produce | ¿Datos? | Riesgo principal | Esfuerzo |
| --- | --- | --- | --- | --- |
| **L1** Tamizaje multiobjetivo auditable con incertidumbre explícita | Cuáles candidatos merecen validación, con intervalo de cobertura y traza por candidato | Sí, salvo los candidatos del EPILAB | Transferencia coleóptero → hemíptero no validada | Bajo, 2 personas, 3–5 días |
| **L2** Validación retrospectiva contra el RNAi publicado en hemípteros | Si el puntaje de L1 discrimina, y cuánto | Sí, pero son decenas de puntos | n chico y sesgo de publicación | Medio, 1–2 personas, 4–6 días |
| **L3** Mapa de riesgo fuera de blanco ponderado por consecuencia | Qué candidato es inaceptable y por qué | Parciales: esencialidad sólo de *Tribolium* | Mide riesgo potencial, no efecto | Medio-alto, 2 personas, 5–7 días |
| **L4** Ajuste fino de un modelo fundacional de ARN para eficacia | Ninguna que se pueda defender hoy | **No** | Reproducir el error de negativos barajados | Alto y mal invertido |

El orden es L1 > L2 > L3 >> L4, con L1 y L2 como una sola decisión en dos tiempos
y L4 documentada como **descarte razonado** con la condición explícita que la
reactivaría. La ampliación de este relevamiento agregó evidencia en las dos
direcciones: reforzó L1 —porque los modelos de ARN que funcionan llevan
termodinámica adentro, y porque la predicción de aptitud en cero disparos tiene
MCC medio por debajo de 0,20— y reforzó el descarte de L4, con tres benchmarks
independientes más. El registro de qué cambió y por qué está dentro del propio
`lineas_de_ataque.md`, en la sección de revisión del 17 de octubre.

### 6.4 Lo que este relevamiento no pudo resolver

Para que quede como vacío documentado y no como silencio `[?]`:

- **No se pudo abrir el trabajo sobre knockdown de dsRNasas en *Dalbulus maidis***
  (PubMed 37945254). El intento original devolvió un rechazo de política de
  herramienta, registrado en `00_meta/PREGUNTAS_ABIERTAS.md` y no reformulado. Es
  la pieza que conecta el cuello de botella de entrega con una decisión de diseño
  de secuencia, y sigue pendiente de abrirse por otra vía.
- **No se pudo abrir el estudio retrospectivo sobre siRecords** que, según lo cita
  el relevamiento de siRNA, no encontró relación entre accesibilidad y eficacia.
  La evidencia en contra de la accesibilidad queda apoyada en la cita de segunda
  mano más el resultado directo de dsRIP.
- **La equivalencia entre el preprint arXiv 2505.09087 y el artículo bbag098**
  es nuestra inferencia por autor, institución, metodología y coincidencia
  numérica; el artículo no la declara.
- **Nadie midió la transferencia entre organismos** de ningún modelo fundacional
  de ácidos nucleicos. BEND lo declara explícitamente como pregunta abierta. Es
  el dato que más nos cambiaría el plan y no existe.
- **No existe un benchmark comunitario de efectos fuera de blanco**, ni en siRNA
  humano ni en dsRNA de plagas.
- **La licencia de los pesos de AIDO.RNA y de PlantRNA-FM** no está declarada en
  sus artículos.

---

## Nota de método

Las fuentes de este reporte se abrieron en dos tandas, el 16 y el 17 de octubre
de 2026, y están listadas en `sources.json` con la URL efectivamente abierta de
cada una y con una sección aparte, `no_abiertas`, para las que no se pudieron
abrir, con el motivo y el impacto de cada ausencia. El material crudo sin
redactar, con los números tal como figuran en cada fuente, está en
`notes/02_material_crudo.md` y `notes/03_material_crudo_ampliacion.md`. El
catálogo estructurado de modelos está en `modelos.json`, donde cada entrada lleva
un campo `nivel_verificacion` que distingue el artículo primario abierto, la
especificación tomada de un relevamiento que sí se abrió, y el repositorio
oficial abierto.

Ninguna cita de este reporte proviene de memoria. Donde una afirmación descansa
en una fuente que no se abrió en texto completo, está marcada como tal.


