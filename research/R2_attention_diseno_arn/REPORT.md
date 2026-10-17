# R2 — Attention y diseño de ARN: evaluación de la idea del equipo

Evaluación de una idea propuesta por un integrante del equipo: tratar las porciones de
ARN como tokens de un modelo de lenguaje grande (large language model, LLM) y usar el
mecanismo de atención (attention) para encontrar qué secuencia mejora la respuesta, con la
termodinámica de BLAST como función de pérdida (loss).

---

## Veredicto

**La idea descansa sobre un error factual y reinventa algo publicado al menos cuatro
veces, pero el problema que intuye es el problema correcto, y hay una reformulación de ese
problema que es viable y que apunta exactamente a la pregunta que el organizador declara
abierta.** El error factual es que BLAST no calcula termodinámica: es una heurística de
alineamiento local de secuencias cuyo puntaje son log-odds de sustitución, y la fuente
primaria de NCBI no menciona la energía libre de hibridación en ningún momento `[E]`. La
termodinámica —la asimetría de extremos, la energía de autoplegamiento, la accesibilidad
del sitio blanco— la calcula ViennaRNA, un paquete completamente distinto, con un modelo
físico de parámetros medidos por experimentos de melting óptico `[E]`. Son dos
herramientas que responden dos preguntas que no se tocan: BLAST dice "¿a qué otra cosa se
parece esta secuencia?", que es la pregunta de la especificidad y del off-target;
ViennaRNA dice "¿qué tan favorable es energéticamente que este dúplex se forme y que este
sitio esté accesible?", que es parte de la pregunta de la eficacia. La "loss termodinámica
de BLAST" no existe. Y la termodinámica, aun bien calculada, no es una loss: es una
*feature de entrada*. La loss sólo puede ser el fenotipo medido —mortalidad, hazard ratio,
reducción de transcripto—, porque es lo único que constituye supervisión.

**El segundo problema es que la arquitectura propuesta ya está publicada y nombrada.**
OligoFormer (*Bioinformatics* 2024) combina embeddings del modelo de lenguaje de ARN
RNA-FM, un encoder transformer con atención multi-cabeza y parámetros termodinámicos, para
predecir eficacia de knockdown `[E]`. AttSiOff declara textualmente entre sus aportes
haber aplicado RNA-FM "en lugar de one-hot" y empleado self-attention en predicción de
inhibición de siRNA "por primera vez" `[R]`. BERT-siRNA hereda pesos de DNA-BERT, hace
fine-tuning sobre datos de siRNA, y reporta que su atención se concentra en el extremo 5'
de la guía `[E]`. DeepSipred combina one-hot, embeddings de RNA-FM y energía libre de
Gibbs `[E]`. La idea del equipo es, feature por feature, la familia OligoFormer/AttSiOff.
Reimplementarla no es innovación. Peor: la revisión más reciente del campo concluye que
esos embeddings son "sufficient but not necessary", que las ablaciones que los justifican
"rest largely on single-model ablations", y que al aplicar particiones que controlan la
fuga de datos el rendimiento absoluto cae y las diferencias entre métodos se angostan
`[E]`. Y hay un problema de dominio que es fatal para la transferencia directa: todos esos
modelos se entrenaron con siRNA sintéticos de 19 a 21 nt transfectados en líneas celulares
humanas, y Cedden et al. demostraron experimentalmente que al menos un parámetro —el
contenido de GC en las posiciones 9 a 14 del antisentido— **se invierte de signo** entre
humano e insecto, y que la accesibilidad del ARNm, pilar de la literatura humana, **no es
predictor significativo** de eficacia insecticida `[E]`.

**Lo que sí se sostiene, y lo que recomendamos construir, es otra cosa: no un generador de
secuencias nuevas sino una función de puntuación y ordenamiento sobre candidatos dados,
multiobjetivo, auditable término por término, y con la incertidumbre propagada hasta el
ranking.** Esto no es una concesión: es el encuadre que el propio organizador declara como
su pregunta abierta —"candidatos preliminares diseñados por el equipo del EPILAB" y
"¿cuáles merecen validación y por qué?" `[R]`— y es lo único de esta familia de ideas que
cuatro personas pueden ejecutar y *validar* sin un solo experimento húmedo, porque existe
un benchmark retrospectivo real: los 29 ARNdc de Cedden et al. en *Tribolium castaneum*
con hazard ratio medido y datos crudos bajo licencia CC BY `[E]`. Un generador de
secuencias, en cambio, produce salidas que nadie puede verificar sin laboratorio, y por
eso lo descartamos explícitamente. Hay un condicionante de datos que hay que decir en la
primera página: **ningún ensamblado público de *Dalbulus maidis* tiene anotación de
genes** —los tres existen, ninguno trae transcriptos, y no hay registro TSA para la
especie `[E]`—, de modo que el conjunto de transcriptos del blanco, insumo mínimo de
cualquier método de este tipo, hay que construirlo desde las 20 corridas públicas de
RNA-seq. Es trabajo acotado, no un bloqueo, pero es el camino crítico y la primera tarea.
El veredicto, entonces: **la idea como fue formulada se descarta; la reformulación como
priorización auditable es viable, y la especificación está en `PROPUESTA.md`.**

---

## 1. El malentendido de base: BLAST no calcula termodinámica

La idea original dice que "para ver si un ARN sirve, se usa el algoritmo de BLAST, donde
se separa en porciones y se calcula la termodinámica". Hay dos operaciones distintas
fusionadas en esa frase, y separarlas redefine por completo qué puede ser la loss.

### Qué hace BLAST, con qué entrada y qué salida

BLAST (Basic Local Alignment Search Tool) es una heurística de búsqueda de similitud de
secuencias. Su entrada es una secuencia consulta y una base de datos de secuencias; su
salida son alineamientos locales con un puntaje y una significancia estadística. El
algoritmo original se describe a sí mismo como una aproximación directa a alineamientos
que optimizan una medida de similitud local, el puntaje de par de segmentos maximal
(maximal segment pair, MSP) `[E]`. El esquema es de semilla y extensión (seed-and-extend):
se buscan aciertos de palabras (word hits) de longitud fija y se extienden; la versión de
1997 introduce justamente "un nuevo criterio para disparar la extensión de los aciertos de
palabra" `[E]`.

El puntaje es lo que importa acá. La documentación primaria de NCBI sobre la estadística de
BLAST establece que cualquier matriz de sustitución con esperanza negativa puede escribirse
como puntajes log-odds construidos a partir de frecuencias objetivo, frecuencias de fondo y
una constante de escala lambda `[E]`. El bit score es el puntaje crudo normalizado con K y
lambda. El E-value, por la ecuación de Karlin-Altschul, es —en la definición textual de
NCBI— "un parámetro que describe el número de aciertos que uno puede esperar ver por azar"
en una base de datos de un tamaño dado, y decrece exponencialmente a medida que crece el
puntaje `[E]`. **En ninguna parte de ese modelo aparece la energía libre de hibridación.**
Es un modelo estadístico de similitud bajo un nulo de residuos independientes, no un modelo
físico. Para alineamientos con huecos la teoría ni siquiera es analítica: lambda y K se
estiman empíricamente de comparaciones de secuencias aleatorias `[E]`.

Esto tiene una consecuencia práctica inmediata: **BLAST sí es la herramienta correcta, pero
para la otra mitad del problema.** La pregunta "¿esta porción de ARNdc se parece
peligrosamente a un transcripto del maíz, de la abeja o de un enemigo natural?" es
exactamente una pregunta de similitud de secuencias. Y de hecho las dos herramientas de
diseño de ARNdc que son estado del arte no usan BLAST para eso sino Bowtie, que es un
mapeador de lecturas cortas: si-Fi21 lo eligió explícitamente por "exactitud, velocidad y
eficiencia de memoria" `[E]`, y dsRIP usa Bowtie1 v1.3 instruido para reportar todas las
coincidencias sin importar la direccionalidad `[E]`. La razón es que el objeto a buscar no
es un alineamiento local difuso sino una coincidencia casi exacta de una ventana de 19 a 21
nt, con 0, 1 o 2 desapareamientos; para eso un mapeador de lecturas cortas es la
herramienta natural y BLAST es sobrecalificado y más lento.

### Qué hace ViennaRNA, con qué entrada y qué salida

La termodinámica la calcula el paquete ViennaRNA, sobre el modelo de energía con los
parámetros Turner 2004 `[E]`. Los programas relevantes y lo que hace cada uno:

- **RNAfold** toma una secuencia y calcula la energía libre mínima (minimum free energy,
  MFE) y retrocede una estructura secundaria óptima. Con la opción `-p` aplica el algoritmo
  de McCaskill para obtener la función de partición, la matriz de probabilidades de
  apareamiento de bases y la estructura centroide `[E]`. Es la herramienta del término de
  autoplegamiento: cuánta estructura interna tiene la hebra guía, que compite con su
  hibridación al blanco.
- **RNAplfold** calcula la probabilidad de apareamiento de bases promediada sobre todas las
  ventanas que contienen el par putativo, y con la opción `-a` las accesibilidades locales,
  es decir las probabilidades de que intervalos de secuencia estén de hebra simple en
  equilibrio termodinámico `[E]`. Es la herramienta de la accesibilidad del sitio blanco, y
  es la que implementa si-Fi21 con parámetros u=8, L=40, W=80 `[E]`.
- **RNAup** descompone explícitamente la energía de interacción. Su manual da la relación
  `dG = dGint + dGu_l`, donde `dGu_l` es la energía de apertura de la región blanco y
  `dGint` la energía de interacción propiamente dicha `[E]`. Primero calcula las energías
  locales de apertura de ambas moléculas y después busca el mejor sitio de interacción
  `[E]`. Es la herramienta conceptualmente más completa para la hibridación guía-blanco,
  porque separa el costo de abrir el sitio del beneficio de aparearse.
- **RNAduplex** hace lo mismo pero ignorando las estructuras intramoleculares y todos los
  bucles multirrama `[E]`: es la versión rápida y menos exacta.

### Cuál de las dos señales sirve realmente para seleccionar un ARNdc

Acá hay un hallazgo que contradice la intuición que viene de la literatura humana y que es
el dato más importante de toda esta sección. Cedden et al. probaron experimentalmente en
*Tribolium castaneum* 31 siRNA de 21 nt, cada uno insertado individualmente en un esqueleto
no dirigido de mGFP, apuntando a distintas regiones del mismo gen esencial (*Tc-gawky*), y
ajustaron la supervivencia de 29 de ellos contra nueve features de secuencia en un modelo
de Cox (C-statistic de Harrell = 0,76; IC 95% 0,73 a 0,79) `[E]`. Cuatro features
resultaron significativamente asociadas a la eficacia insecticida:

1. la **asimetría termodinámica**, que favorece que el antisentido sea elegido como hebra
   guía por el complejo RISC;
2. la **energía de autoplegamiento del antisentido** (ausencia de estructura secundaria
   fuerte);
3. el **%GC de las posiciones 9 a 14** del antisentido;
4. la presencia de **adenina en la posición 10** del antisentido.

Y cinco no resultaron significativas (P > 0,05), entre ellas dos que la literatura humana
considera centrales: **la accesibilidad del ARNm** y la energía de unión del antisentido al
blanco `[E]`. Más todavía: el %GC, que en la literatura terapéutica humana se prefiere
*bajo*, en insecto se asoció a eficacia cuando es *alto* en esa ventana de posiciones
`[E]`. Al pasar a ARNdc largo, un modelo de regresión múltiple confirmó que el score de
siRNA agregado fue el predictor positivo más significativo de eficacia (aumento de 1,462 en
hazard ratio por unidad de score, P = 0,003) mientras que **la accesibilidad del ARNm
siguió sin ser significativa (P = 0,41)** `[E]`.

El mecanismo detrás de esto quedó documentado: los ARNdc de alto score produjeron en
promedio 20,1% más siRNA antisentido ligado a RISC `[E]`. Es decir, la asimetría
termodinámica funciona porque sesga la selección de hebra guía, que es un paso
mecanísticamente conservado.

**Conclusión de la sección 1, y redefinición de la loss.** La señal termodinámica útil para
seleccionar un ARNdc en un insecto es la **asimetría de extremos del dúplex y el
autoplegamiento de la guía**, calculadas con ViennaRNA y con tablas de estabilidad de
dúplex de ARN; **no** la accesibilidad del blanco, que la evidencia en insectos no sostiene;
y **nada** de lo que calcula BLAST, que pertenece al eje de especificidad. Y la
termodinámica no puede ser la loss: es una feature. La loss, si hubiera entrenamiento, es
el fenotipo medido. En nuestra propuesta no hay entrenamiento de un modelo nuevo
precisamente porque no hay datos de fenotipo suficientes en el orden correcto de insectos;
lo que hay es una función de puntuación calibrada con coeficientes publicados y validada
retrospectivamente.

---

## 2. Estado del arte: qué reinventa la idea

### 2.1 Modelos de lenguaje de ácidos nucleicos

| Modelo | Tamaño | Datos de preentrenamiento | Tokenización | Objetivo | Licencia |
| --- | --- | --- | --- | --- | --- |
| **RNA-FM** | ~99M, encoder BERT de 12 capas | 23,7M secuencias de ARN no codificante de RNAcentral | Por nucleótido | Predicción de tokens enmascarados | MIT (código) `[R]` |
| **RiNALMo** | 650M | ~36M secuencias de ARN no codificante | Por nucleótido | Enmascarado | — `[R]` |
| **Nucleotide Transformer v2** | 500M | 850 genomas de NCBI, 174 Gnt (~29 Gtokens), **excluye plantas y virus** | 6-meros cuando es posible, nucleótido individual si no; vocabulario de 4.105 | MLM tipo BERT al 15% | **CC-BY-NC-SA-4.0: no comercial** `[R]` |
| **DNABERT** | — | Genoma humano | k-meros solapados | MLM | — `[R]` |
| **DNABERT-2** | — | Multiespecie | **BPE**, vocabulario de 4.096 | MLM | — `[R]` |
| **Evo 1 / Evo 2** | 7B / 40B | Procariotas, fagos, multidominio | Por nucleótido | Autorregresivo | `[?]` sólo fuentes secundarias |

RNA-FM produce embeddings de 640 dimensiones por nucleótido y es, con diferencia, el modelo
más usado como fuente de features en predictores de siRNA: OligoFormer, AttSiOff y
DeepSipred los tres lo usan `[E]`. Vale la pena registrar dos limitaciones de dominio que
la revisión de *NAR Genomics and Bioinformatics* señala y que son directamente relevantes
para nosotros: los tokenizadores de estos modelos carecen de símbolos para nucleótidos
modificados, de modo que un siRNA químicamente modificado se colapsa o queda fuera de
vocabulario `[E]`; y la brecha entre el preentrenamiento sobre ARN no codificante natural y
los oligonucleótidos sintéticos modificados "no está sistemáticamente cuantificada" `[E]`.
Nucleotide Transformer tiene además un problema de licencia que hay que mirar si el
proyecto deriva en algo comercial, y excluye plantas de su corpus, lo que lo vuelve mal
candidato para la mitad "off-target en maíz" del problema `[R]`.

### 2.2 Predicción de eficacia de siRNA y dsRNA con aprendizaje automático

**En humano, el campo está maduro y saturado.** La cronología va de reglas de secuencia
(Reynolds, Ui-Tei, Amarzguioui) a features termodinámicas y composicionales, a ML clásico
(BIOPREDsi, LASSO, i-Score, SVM con kernels de strings), a aprendizaje profundo (CNN
multikernel, GNN como siRNADiscovery, modelo 3D equivariante ENsiRNA), a transformers con
embeddings de modelos fundacionales `[E]`. El benchmark de referencia es Hüsken: 2.431
siRNA contra 34 ARNm en células H1299, con PCC de 0,66 para el modelo original `[R]`. El
agregado que usa el campo son nueve estudios, 3.714 siRNA y 75 ARNm, todos en líneas
celulares humanas: H1299, HeLa, HaCaT, HEK293T, HEK293, T24 `[E]`.

**En insectos, el campo está esencialmente vacío, y lo poco que hay es Coleoptera.** Hay
dos líneas:

- **dsRNAPredictor / dsRNAPredictor-II.** Embeddings dna2vec de 3-meros, CNN, BiLSTM y una
  capa de self-attention. Datos de iBeetle-Base: de 16.094 registros se retuvieron 12.027
  ARNdc "eficientes" como positivos, con negativos construidos como fragmentos de ARNm
  reordenados `[R]`. Métricas: exactitud 0,76 y AUC 0,83 en validación cruzada de cinco
  pliegues, y prácticamente las mismas en el "test independiente" `[R]`. El problema es
  grave y hay que decirlo: **ese "test independiente" es una porción retenida del mismo
  dataset**, no un benchmark externo; y para *Aedes aegypti*, la única especie fuera del
  dominio de entrenamiento, **no reportan ni exactitud ni AUC**: el claim de transferencia
  se apoya en acuerdo cualitativo, con desacuerdos reconocidos por los propios autores
  `[R]`. La etiqueta además es binaria y grosera —letalidad de al menos 20% o cambio
  fenotípico— con dosis y vía no controladas entre genes: no es una medida de eficacia
  comparable entre registros `[R]`.
- **dsRIP (Cedden et al. 2025).** No es un modelo de aprendizaje profundo sino un modelo de
  Cox con cuatro features, calibrado sobre experimentos propios, y es —por lejos— el trabajo
  más sólido del área. Validado prospectivamente: un ARNdc diseñado por dsRIP superó
  significativamente a la secuencia comercial de Ledprona a dosis baja (P = 0,022, hazard
  ratio 2,1) en *Leptinotarsa decemlineata*, y mejoró los diseños previos en *Psylliodes
  chrysocephala* con hazard ratios de 1,8 a 2,5 `[E]`.

**Transferibilidad entre especies: la evidencia es explícitamente mixta y hay que reportarla
así.** A favor: el perfil de siRNA ligado a RISC fue muy similar entre *T. castaneum*
(inyección) y *P. chrysocephala* (ingestión) para la misma secuencia de ARNdc, lo que
sugiere que el procesamiento y la selección de hebra guía son conservados al menos entre
esos dos coleópteros `[E]`. En contra: los propios autores advierten que Dicer-2 y
Argonaute-2 varían en secuencia entre órdenes, que Lepidoptera es el orden con mayor
divergencia filogenética en esas enzimas, que algunos lepidópteros generan siRNA de 20 nt y
no de 21, y que **"será importante validar las predicciones de dsRIP para otros órdenes y
ajustar los parámetros si hace falta"** `[E]`. *Dalbulus maidis* es Hemiptera: no es ninguno
de los dos casos medidos. Ésta es la incertidumbre dominante de todo el proyecto y no se
puede resolver sin laboratorio.

**Para insectos específicamente, y no sólo líneas celulares humanas, la respuesta es: existe
dsRIP y existe dsRNAPredictor, ambos en Coleoptera, y no existe nada en Hemiptera.** `[E]`

### 2.3 Predicción de off-target más allá del alineamiento

El mecanismo está establecido: la actividad off-target de tipo miARN la dirige la
complementariedad de la región semilla (seed), posiciones 2 a 8 de la hebra guía, contra
sitios en los 3' UTR `[E]`. Una disección más fina reporta que las posiciones 2 a 5 dirigen
la actividad off-target, las 6 a 8 contribuyen a ambas actividades, y las 8 a 14
correlacionan *negativamente* con off-target `[E]`.

Lo que existe por encima del alineamiento puro:

- **SeedMatchR**, un paquete de Bioconductor que no predice sino que *testea*: evalúa si los
  transcriptos con coincidencia de semilla están enriquecidos entre los genes regulados a la
  baja en datos de RNA-seq, sobre más de 50 conjuntos `[E]`.
- **siSPOTR**, que calcula un puntaje de potencial off-target de semilla (POTS) a escala de
  transcriptoma, para humano y ratón `[E]`.
- **Features estructurales aprendidas**: Richter y Admasu usaron más de 30.000 puntos de
  datos siRNA/gen y compararon nueve estrategias de features; las mejores fueron huellas
  digitales de conectividad extendida (ECFP) calculadas sobre alineamientos estructurales
  siRNA/AGO2 minimizados en energía `[R]`.
- **pssRNAit** para siRNA de plantas, y **si-Fi** que combina mapeo con Bowtie y
  accesibilidad con ViennaRNA `[E]`.

Un dato importante sobre la madurez real del área: de todo ese conjunto, **sólo SeedMatchR y
el trabajo de Richter y Admasu están entrenados o derivados de datos experimentales de
off-target**; los demás se validan contra esos datos pero no se entrenan con ellos `[E]`. Y
en insectos para control de plagas el estado del arte es más simple todavía: dsRIP busca
coincidencias de los siRNA prospectivos contra transcriptomas de organismos no objetivo con
Bowtie1, permitiendo 1 o 2 desapareamientos según elija el usuario, y calcula un puntaje de
seguridad que pondera los aciertos en ortólogos de genes esenciales 20 a 1 frente a los
aciertos comunes `[E]`. Esa ponderación por identidad del gen, y no por conteo plano de
off-targets, es la contribución conceptual de dsRIP en este eje, y los autores la presentan
como mejora sobre "el enfoque usado por los métodos actuales de predicción de off-target
para control de plagas basado en RNAi" `[E]`.

### 2.4 ¿Ya existe un método publicado que hace lo que propone la idea del equipo?

**Sí, y hay que decirlo de entrada: cuatro.** No es una coincidencia parcial; es la misma
arquitectura con los mismos componentes.

| Método | Qué hace | Coincidencia con la idea del equipo |
| --- | --- | --- |
| **OligoFormer** (*Bioinformatics* 2024) | Embeddings congelados de RNA-FM (19x640 para siRNA, 57x640 para la ventana de ARNm) + encoder con transformer multi-cabeza + parámetros termodinámicos, concatenados en un MLP | Completa. Es literalmente "porciones de ARN como tokens, atención, y termodinámica". AUC 0,86 y PCC 0,71 intra-dataset en Hüsken; AUC 0,82 y PCC 0,59 inter-dataset `[E]` |
| **AttSiOff** (preprint 2023) | Predictor de inhibición basado en self-attention sobre embeddings de RNA-FM, más buscador de ARNm y filtro de off-target por conteo de semillas | Completa, y los autores reclaman explícitamente la novedad de usar self-attention en esta tarea "por primera vez" `[R]` |
| **BERT-siRNA** | Hereda pesos de DNA-BERT y hace fine-tuning sobre datos de siRNA; su atención se concentra en el extremo 5' de la guía | Completa, y es además la versión "fine-tuning de un modelo de secuencia" que la idea plantea como alternativa `[E]` |
| **DeepSipred** | One-hot + embeddings de RNA-FM + energía libre de Gibbs | Completa `[E]` |

Hay un matiz que sí es un hueco real: **todos son para siRNA corto en células humanas, y
ninguno para ARNdc largo en insectos.** La revisión de *NAR GAB*, que cubre el campo
completo hasta 2026, **no menciona insectos en ninguna parte** `[E]`. Ese es el único
espacio donde la idea tendría algo que agregar, y es exactamente el espacio que dsRIP ya
ocupó en 2025 con un método mucho más simple y con validación prospectiva real. Partir de
dsRIP y mejorarlo es innovación; reimplementar OligoFormer con datos que no existen, no.

---

## 3. Reformulación rigurosa

### 3.1 El problema real, planteado como lo que es

Dado un conjunto *C* de candidatos de ARNdc (en el caso del Investigathón, los candidatos
preliminares del EPILAB), cada candidato *c* definido por una secuencia de 200 a 500 pb y
un transcripto blanco en un organismo del sistema, el problema no es generativo: es de
**ordenamiento multiobjetivo bajo incertidumbre**. Hay que producir un ranking de *C* y, por
cada posición del ranking, la razón auditable de por qué está ahí y cuán estable es esa
posición.

La descomposición natural es en dos niveles, porque así funciona la biología: el ARNdc largo
se procesa por Dicer-2 en un pool de siRNA de ~21 nt, y son esos siRNA los que actúan. De
modo que todo término se calcula por ventana de 21 nt y se agrega al nivel del candidato.
Esto no es una elección estética: es la arquitectura que Cedden et al. validaron
experimentalmente, y la razón por la cual su ventana deslizante de 300 pb que maximiza el
score medio de siRNA funcionó `[E]`.

### 3.2 Los términos, uno por uno

Para cada ventana *w* de 21 nt derivable de *c*:

**E(w) — eficacia de knockdown predicha.**
*Cómo se calcula:* combinación lineal de las cuatro features significativas de Cedden et
al. con sus coeficientes del modelo de Cox: asimetría termodinámica (diferencia de energía
de apareamiento entre los primeros cuatro nucleótidos del antisentido y los últimos cuatro
del sentido, excluyendo los dos nucleótidos de overhang 3', con valores de tablas de
estabilidad de dúplex de ARN medidas por melting óptico), energía de autoplegamiento del
antisentido (ViennaRNA), %GC de las posiciones 9 a 14 del antisentido, y presencia de
adenina en la posición 10.
*Qué datos necesita:* sólo la secuencia. ViennaRNA es software libre.
*Confiabilidad:* **moderada y con un sesgo taxonómico conocido.** C-statistic 0,76 sobre
n=29, calibrado en Coleoptera, con validación prospectiva en dos coleópteros más `[E]`. Para
Hemiptera, no validado. Es el término mejor fundado del conjunto y a la vez el portador de
la incertidumbre dominante.

**A(w) — accesibilidad del sitio blanco. Término que proponemos EXCLUIR, con fundamento.**
*Por qué:* es el término que la literatura humana considera central y que la idea original
probablemente tenía en mente al hablar de termodinámica. La evidencia en insectos lo
contradice dos veces en el mismo trabajo: no significativo en el ensayo de siRNA individual
(P > 0,05) ni en el de ARNdc largo (P = 0,41) `[E]`. Incluirlo con peso alto es importar un
supuesto de células humanas que el único experimento controlado en insectos refuta.
*Qué hacemos:* se calcula con RNAplfold y **se reporta** para trazabilidad y para la
ablación, pero entra al score con peso cero por defecto. Esta decisión es uno de los puntos
donde el método se diferencia de un si-Fi21 aplicado a ciegas, que sí lo usa con peso `[E]`.

**O_maiz(w) — penalidad por off-target en maíz.**
*Cómo se calcula:* mapeo con Bowtie de *w* y su complemento contra los transcriptos de *Zea
mays* B73 (RefSeq `GCF_902167145.1`, anotación `GCF_902167145.1-RS_2025_02`), con 0, 1 y 2
desapareamientos reportados por separado; y por separado también el conteo de coincidencias
de la semilla (posiciones 2 a 8).
*Qué datos necesita:* el genoma y la anotación del maíz, que existen y son de dominio
público.
*Confiabilidad:* **el cálculo es determinista y confiable; su interpretación no.** Dos
reservas honestas: B73 no es el germoplasma comercial argentino y la variación de secuencia
entre ambos no está cuantificada; y la relevancia funcional de un acierto depende de la
maquinaria de RNAi de la planta, que es otra pregunta.

**O_nt(w) — penalidad por off-target en organismos no objetivo.**
*Cómo se calcula:* igual, contra un panel curado. Mínimo: *Apis mellifera*
(`GCF_003254395.2`, anotación Release 104) como polinizador de referencia, y los cicadélidos
con anotación RefSeq disponible —*Homalodisca vitripennis* `GCF_021130785.1` y *Macrosteles
quadrilineatus* `GCF_028750875.1`— como no objetivo cercano, que es el caso difícil.
Ponderando los aciertos en ortólogos de genes esenciales por encima de los demás, siguiendo
la lógica de dsRIP `[E]`.
*Confiabilidad:* el cálculo es confiable; la **cobertura del panel no**. Falta curar
enemigos naturales y fauna del suelo relevantes en maíz argentino, y eso es trabajo de
curaduría que hay que hacer y declarar como incompleto.

**O_self(w) — off-target dentro de *D. maidis*.**
*Cómo se calcula:* igual, contra el transcriptoma de referencia de *D. maidis*.
*Qué datos necesita:* **el transcriptoma que no existe.** Éste es el término que depende de
la tarea del camino crítico.
*Confiabilidad:* condicionada por la calidad del ensamblado propio. Baja mientras no esté
hecho.

A nivel del candidato *c*:

**K(c) — calidad del gen blanco.**
*Cómo se calcula:* ¿es ortólogo de un gen blanco efectivo del cribado genómico de *T.
castaneum*? ¿tiene parálogos que puedan compensar funcionalmente el knockdown? Es la lógica
del Target Gene Finder de dsRIP `[E]`.
*Confiabilidad:* es el predictor que Cedden et al. identificaron como **dominante**: "un
predictor principal sigue siendo la selección del gen blanco", con diferencias enormes de
hazard ratio entre genes (15,83 de caída comparando *Tc-eIF3a* contra *Tc-gawky*, P = 0,005)
`[E]`. Para los candidatos del EPILAB, cuyos blancos ya están elegidos, este término es
sobre todo informativo: explica por qué dos candidatos pueden diferir mucho sin que el
diseño de secuencia tenga nada que ver.
*Nota:* los blancos con RNAi publicado y efectivo en *D. maidis* —*BicC*, las dsRNasas,
*burs-alfa* y *eth*— son evidencia directa de calidad de blanco en la especie, y hay que
usarlos como tales `[E]`.

**R(c) — región del transcripto: ORF frente a UTR.**
*Cómo se calcula:* binario, a partir de la anotación.
*Confiabilidad:* buena y con dirección clara. Apuntar al ORF se asoció a mayor eficacia
insecticida (aumento de 9,91 en hazard ratio, P = 0,011), y además incluir los UTR en la
búsqueda permitía encontrar fragmentos con score de siRNA más alto **que no se traducían en
mayor letalidad** `[E]`. Es un buen recordatorio de que maximizar el score no es maximizar
el efecto.

**C(c) — conservación de la región blanco entre poblaciones.**
*Cómo se calcula:* fracción de las ventanas de 21 nt libres de variantes entre los
individuos disponibles.
*Qué datos necesita:* **datos poblacionales que no existen.** Lo que hay son seis corridas
de WGS en MiSeq (PRJNA852223, de profundidad y origen geográfico no verificados), una de
captura dirigida con diseño filogenético, y la comparación entre los dos ensamblados
independientes (Sanger y CIAP-INTA).
*Confiabilidad:* **la más baja del conjunto.** `[H]` Es calculable sobre un puñado de
individuos; **no es interpretable como conservación poblacional** y hay que decirlo así en
la salida, no esconderlo detrás de un número.

**D(c) — riesgo de entrega: la barrera de las dsRNasas.**
Este término merece un tratamiento distinto y es donde el encuadre del organizador cambia la
propuesta. El organizador declara que las RNasas limitan la entrega oral, y la fuente
primaria existe: en *D. maidis* se identificaron y caracterizaron tres dsRNasas, con
*Dmai-dsRNase-2* fuertemente expresada en intestino medio y glándulas salivales; un ensayo
de degradación ex vivo mostró actividad nucleasa significativa y alta inestabilidad del
ARNdc frente a homogenatos de tejido; y silenciar *Dmai-dsRNase-2* mejoró la respuesta al
ARNdc del gen de interés `[E]`.
*Cómo se calcula:* **no se calcula como score continuo, y pretender lo contrario sería
deshonesto.** La degradación por dsRNasas es en primera aproximación independiente de la
secuencia: no hay una secuencia que escape a una nucleasa de ARN de doble hebra. Lo que es
*sequence-addressable* es la estrategia de co-administración que proponen los autores. Así
que D(c) es una **anotación categórica por candidato**: ¿el candidato forma parte de un
diseño de co-entrega con ARNdc contra *Dmai-dsRNase-2*? ¿la vía de entrega prevista es oral
o inyección? Entra al reporte como condición declarada, no al score como número.
*Por qué importa igual:* porque dos candidatos con idéntica eficacia predicha tienen
pronóstico distinto si uno va por vía oral sin co-entrega y el otro con. Omitir el término
haría que el ranking prometa algo que la biología de la entrega no sostiene.

### 3.3 La agregación: por qué NO una suma ponderada presentada como verdad

La tentación es colapsar todo en S(c) = suma de w_i por término_i y ordenar. Es lo que hace
dsRIP con su deslizador de prioridad entre eficacia y seguridad `[E]`, y es razonable como
herramienta de diseño. Pero para responder "¿cuáles merecen validación y por qué?" es
insuficiente, porque los pesos son una elección nuestra y el ranking que producen hereda esa
arbitrariedad sin declararla.

Lo que proponemos es un ordenamiento con tres capas, y esto es el corazón de la
contribución metodológica:

1. **El vector de términos sin colapsar**, por candidato. Siempre visible. Un candidato que
   gana por eficacia y pierde por off-target en maíz no es lo mismo que uno mediocre en
   todo, y un escalar los vuelve indistinguibles.
2. **El frente de Pareto.** Qué candidatos no están dominados por ningún otro en todos los
   términos simultáneamente. Esto es independiente de los pesos y por lo tanto no
   discutible: es la parte del ranking que no depende de nuestras preferencias.
3. **La estabilidad del ordenamiento bajo perturbación.** Para cada par de candidatos
   (a, b), la fracción de vectores de peso muestreados del simplex, y de remuestreos
   bootstrap de los coeficientes de Cox, en los que a se ordena antes que b. Un par con 0,97
   de estabilidad es una afirmación; uno con 0,55 es un empate y hay que decir que es un
   empate.

La métrica de éxito del entregable no es un número de correlación: es que para el conjunto
del EPILAB se pueda decir, de cada par de candidatos, si su orden es robusto o si es un
empate dentro de la incertidumbre. Ésa es la forma de "la mejor decisión científica posible
con el tiempo y los datos disponibles" que el organizador declara como criterio de
evaluación `[R]`.

Esto además llena un hueco que la revisión del campo señala explícitamente: **"no se han
aplicado métodos formales de cuantificación de incertidumbre a la predicción de eficacia de
siRNA"**, y la llama "the most critical gap" `[E]`. Y nadie optimiza conjuntamente eficacia
y seguridad off-target de forma declarada `[E]`.

En la escalera de precisión del organizador, esto se para firmemente en el **primer y
segundo escalón: ARNdc largo canónico y ARNdc ingenierizado**. No tocamos miARN artificial,
syn-tasiRNA, dúplex maduro listo para AGO ni siRNA de 24 nt con RdDM, porque el único
conjunto de coeficientes de eficacia calibrado en insectos que existe fue medido sobre siRNA
de 21 nt procesados de ARNdc largo, y extrapolarlo a una plataforma de precisión con otra
vía de carga sería inventar.

### 3.4 Factibilidad de las cuatro opciones que plantea la idea

**Opción A — scoring con modelo preentrenado congelado (embeddings + cabezal liviano).**
*Factible técnicamente, inútil en la práctica, y por eso lo descartamos como vía principal.*
El cabezal liviano necesita datos de entrenamiento con fenotipo medido en el dominio
correcto. Lo que hay en Hemiptera son seis construcciones publicadas. Se podría entrenar
sobre los 29 ARNdc de Cedden et al., pero con n=29 y features de 640 dimensiones por
nucleótido el cabezal memoriza; y la revisión del campo ya advierte que los embeddings son
"sufficient but not necessary" y que las ablaciones que los justifican son frágiles `[E]`.
Lo conservamos como **un brazo de ablación opcional, sólo si sobra tiempo**, nunca como la
vía principal.

**Opción B — fine-tuning de un modelo de secuencia sobre datos de eficacia de RNAi.**
*No factible y hay que decirlo sin matizar.* Requiere un dataset de eficacia que no existe
para Hemiptera. El candidato más grande, iBeetle-Base, tiene etiquetas binarias y groseras
con dosis y vía no controladas, y es Coleoptera. Hacer fine-tuning sobre los datasets
humanos y aplicarlo a *D. maidis* es precisamente lo que la evidencia desaconseja: el signo
del %GC se invierte entre humano e insecto `[E]`. Esto es un plan de tesis, no un
entregable de Investigathón.

**Opción C — búsqueda sobre el espacio de secuencias (algoritmo genético, búsqueda guiada
por gradiente, muestreo).**
*Técnicamente trivial, epistemológicamente vacío, y además fuera del encuadre del desafío.*
Una ventana deslizante sobre un transcripto ya es la búsqueda exhaustiva del espacio
relevante: dsRIP la hace nucleótido por nucleótido y encuentra el óptimo del score `[E]`. No
hay nada que un algoritmo genético agregue, porque el espacio de candidatos legítimos está
restringido a subcadenas del transcripto blanco: no se puede inventar secuencia que no esté
en el blanco, por definición del mecanismo. Y si se relajara esa restricción, se obtendrían
secuencias que optimizan nuestro propio score sin ninguna manera de verificarlas sin
laboratorio: el modo de falla clásico de optimizar contra un proxy. Descartado.

**Opción D — pesos de atención como herramienta de interpretabilidad.**
*Es lo más cercano a la intuición original, es legítimo en una versión acotada, y arrastra
una advertencia que hay que reportar con fuentes.* Lo desarrollo abajo porque es donde el
riesgo de decir algo falso es más alto.

### 3.5 La advertencia sobre interpretar atención como relación causal

La literatura sobre esto es extensa, está en disputa, y conviene reportar su estructura
real y no una caricatura en ninguna de las dos direcciones.

**Lo que mostró el trabajo que abrió el debate.** Jain y Wallace (NAACL 2019) reportan que
permutar aleatoriamente los pesos de atención "often induces only minimal changes in
output", y que se pueden construir distribuciones adversarias que maximizan la divergencia
de Jensen-Shannon respecto de la original y aun así "yield equivalent predictions". Su
conclusión sobre si la atención provee explicaciones significativas es: "We find that they
largely do not", y advierten contra usar pesos de atención para resaltar tokens de entrada
`[E]`. Serrano y Smith (ACL 2019), por una vía distinta —borrar pesos, renormalizar y
recorrer sólo la capa de clasificación—, concluyen que "attention does not necessarily
correspond to importance" y que ordenar por atención descendente "is not optimal": los
rankings por gradiente y por gradiente por atención dan vuelta la decisión quitando *menos*
ítems `[E]`.

**Lo que hay que saber para no citarlos mal, y es importante.** El resultado de Jain y
Wallace **no es arquitectónicamente universal**, y ellos mismos declaran la excepción: "The
exception to this is when one uses a very simple (averaging) encoder model", donde la
atención sí correlaciona bien con las medidas de importancia `[E]`. Serrano y Smith
encuentran el mismo patrón: los encoders recurrentes dispersan la señal entre muchos
tokens, mientras que los modelos sin encoder se dan vuelta más rápido `[E]`. La variable
que manda es el **grado de contextualización**. Y un punto que se cita mal con frecuencia:
**Jain y Wallace no testearon self-attention multi-cabeza ni Transformers** —su foco es un
encoder BiLSTM con atención aditiva—, de modo que extrapolar su conclusión a un transformer
no está respaldado por su paper `[E]`.

**La réplica.** Wiegreffe y Pinter (EMNLP 2019) objetan que manipular pesos post-hoc no
produce un modelo realmente entrenado con esa atención, y proponen cuatro tests: baseline de
pesos uniformes, calibración de varianza por semilla, un framework diagnóstico con pesos
congelados en un MLP no contextual, y un adversario entrenado end-to-end. Su resultado clave
es que las distribuciones adversarias halladas **rinden mal en el MLP diagnóstico**: la
atención entrenada captura algo real y difícil de explotar adversarialmente. Su conclusión
es definicional —la respuesta "depends on the definition of explainability one is looking
for"— y su formulación más citada es que la atención provee "an explanation; not the
explanation" `[E]`. Distinguen explicación **plausible** (convincente para una persona) de
**fiel** (faithful, que refleje el proceso real de decisión), y aceptan ofrecer sólo la
primera `[R]`.

**Sobre la pregunta causal, que es la que importa para nuestro uso.** La afirmación
publicada más directa es de Grimsley, Mayfield y Bursten (LREC 2020): "attention weights
alone cannot be used as causal explanation for model behavior", porque el vínculo entre la
capa de atención y la salida no puede aislarse de los otros componentes del modelo; afirman
directamente "the impossibility of causal explanations from attention layers over text
data" `[R]`. El survey de Bibal et al. (ACL 2022) lo ratifica y agrega que asumir causalidad
al evaluar el poder explicativo de la atención "is doomed to fail by design" `[E]`.

**Dos complicaciones que el survey señala y que conviene no omitir.** Primero, la fidelidad
de la atención se suele evaluar usando gradientes o LIME **como patrón oro**, pero esas
técnicas "can lead to unexpected (and potentially misleading) results": no hay un patrón oro
confiable sobre el que apoyarse, y "the question of how to evaluate faithfulness is still
open" `[?]`. Segundo, la intuición de que hacer la atención más dispersa mejora la
interpretabilidad no está bien respaldada: inducir esparsidad "may in fact reduce the
faithfulness of attention" `[?]`.

**Qué se prefiere a los pesos crudos.** La dirección de la literatura es consistente aunque
el orden exacto no esté resuelto. Abnar y Zuidema (ACL 2020) parten de que la información de
distintos tokens se mezcla entre capas —razón por la cual los pesos crudos son poco
confiables en un transformer multicapa— y reportan que attention rollout y attention flow
"yield higher correlations with importance scores of input tokens" que la atención cruda
`[R]`. Bastings y Filippova (BlackboxNLP 2020) van más lejos: si el objetivo es saber qué
tokens de entrada importan y la audiencia es quien desarrolla el modelo, "input saliency
methods are better suited", y no hay "compelling reasons to use attention" `[R]`. Y un test
de violación de fidelidad (ICML 2022) muestra que features con atención alta pueden
*suprimir* la predicción, problema que afecta a la mayoría de los métodos "especially the
raw attention" `[R]`.

**Y qué pasa específicamente en modelos genómicos, que es nuestro dominio.** DNABERT
presenta su atención como medida de importancia y reporta que 1.595 de 1.999 motivos
descubiertos se alinearon a motivos validados en JASPAR; pero los propios autores declaran
que "the model is not guaranteed to place high attention on entire region" del motivo y
reportan atención alta espuria al inicio de la secuencia "likely due to model bias" `[R]`.
Clauwaert et al. (*Briefings in Bioinformatics* 2021) reportan cabezas de atención
"specialized towards identifying transcription factors" en *Escherichia coli*, y a la vez
citan la literatura de NLP para advertir que "attention scores do not necessarily offer
transparency into the neural network", aclaran que la especialización "cannot be ascertained
for other prediction tasks or model architectures", y su mejor PR AUC en el test curado es
0,141 `[R]`. Lo decisivo es esto: **ninguno de los dos valida la atención como explicación
fiel de la decisión del modelo; ambos validan coincidencia con bases de datos de motivos
conocidos**, que es una afirmación mucho más débil. Un preprint de 2026 refuerza la cautela:
distintos métodos de interpretabilidad discrepan entre sí sobre las mismas predicciones y
pueden "fail to localize known regulatory motifs" `[R]`; otro propone reemplazar la atención
cruda por propagación de relevancia (AttnLRP) en DNABERT-2 `[R]`.

**Conclusión operativa para nosotros.** El uso legítimo de la atención en este proyecto es
estrecho y hay que enunciarlo con precisión: **como mapa de comunicación de dónde está la
señal a lo largo del transcripto, nunca como evidencia de que el modelo usa esa región
causalmente, y menos aún como evidencia de causalidad biológica.** En rigor, para nuestro
método ni siquiera se necesita: el perfil posicional del score de siRNA a lo largo del
transcripto —que es una función explícita y auditable de cuatro features con coeficientes
publicados— cumple la misma función comunicativa y **sí** es fiel por construcción, porque
es el cálculo mismo y no una lectura de las entrañas de una red. Ésa es la ironía productiva
del caso: la intuición del integrante sobre "ver la relación entre las distintas secuencias
a lo largo del transcripto" es correcta y valiosa, y se satisface mejor sin attention que
con attention.

---

## 4. Datos: la pregunta que mata o salva el proyecto

El detalle completo, con URL, tamaño, formato, licencia y qué falta, está en
`datos_disponibles.md`. Acá va lo que decide el proyecto.

**El hallazgo central es una ausencia: no existe anotación génica pública de *Dalbulus
maidis*.** Hay tres ensamblados, y son buenos: ihDalMaid1.1 del Wellcome Sanger Institute a
nivel cromosoma, 972 Mb en 499 contigs con N50 de scaffold de 93,7 Mb, liberado el 26 de
octubre de 2025; su haplotipo alternativo; y el borrador CIAP v1 del Instituto de Patología
Vegetal del CIAP-INTA, 585 Mb en 22.333 contigs, liberado el 26 de enero de 2026. **Ninguno
de los tres tiene anotación** `[E]`. Y no hay registro TSA para la especie: la búsqueda
`Dalbulus maidis[Organism] AND TSA[Division]` devuelve cero `[E]`. El transcriptoma de Xu et
al. 2021, con 56.116 transcriptos, está publicado pero **no se encontró depositado** `[?]`;
puede estar sólo como material suplementario de un artículo con muro de pago.

Esto significa que el insumo más básico del método —la lista de transcriptos del blanco,
para calcular el score por ventana y para buscar off-targets intraespecíficos— hay que
construirlo. Los materiales existen: 20 corridas públicas de RNA-seq en Illumina,
principalmente PRJNA631706 con 17 corridas, más PRJNA318849, PRJNA562189, PRJNA505618 de
huevos y PRJNA1282137 `[E]`. Y hay un atajo de calidad disponible: dos cicadélidos con
anotación RefSeq, *Homalodisca vitripennis* y *Macrosteles quadrilineatus*, sirven para
transferir anotación por ortología `[E]`. Es trabajo acotado y es el camino crítico.

**Sobre datos de eficacia, la respuesta es que existen pero en el orden equivocado de
insectos y con n de dos dígitos.** Lo utilizable:

- Los datos de bioensayo de Cedden et al.: ~29 siRNA individuales con curvas de
  supervivencia y ~29 ARNdc con hazard ratio medido, en Additional file 2 y Additional file 3
  Tabla S1, bajo **CC BY 4.0** `[E]`. Es el único benchmark cuantitativo de eficacia de
  ARNdc en insectos con diseño controlado y datos abiertos. Es Coleoptera.
- Las seis construcciones de ARNdc publicadas en *D. maidis*: *BicC* con reducción de
  transcripto de hasta 170 veces y reducción de oviposiciones; tres dsRNasas; *burs-alfa* y
  *eth* con alta mortalidad y defectos de muda `[E]`. Es la especie correcta y es todo lo que
  hay. **No alcanza para entrenar nada**; alcanza para una prueba de rango.
- iBeetle-Base, con ~12.000 ARNdc etiquetados, pero binario, grosero y Coleoptera, y con
  licencia que no pudimos confirmar `[?]`.

**Sobre off-target, los datos existen y son buenos.** *Zea mays* B73 `GCF_902167145.1` con
anotación RefSeq, 2,18 Gb; *Apis mellifera* `GCF_003254395.2` con anotación Release 104; los
cuatro patógenos del sistema con genomas disponibles, de los cuales *Spiroplasma kunkelii*
`GCF_001274875.1` (1,51 Mb, completo y anotado) y MRFV `GCF_000862485.2` (6.366 pb) están
resueltos, el fitoplasma tiene tres genomas de *Ca.* Phytoplasma asteris sin que hayamos
confirmado que alguno sea el del achaparramiento, y **MSMV quedó sin identificar
taxonómicamente** `[?]`.

**Sobre conservación poblacional, los datos no existen.** Seis corridas de WGS en MiSeq de
profundidad y origen no verificados, y una de captura dirigida con diseño filogenético. El
término se puede calcular sobre un puñado de individuos; no se puede interpretar como
conservación poblacional `[H]`. Hay que decirlo en la salida del método.

---

## 5. Plan de validación sin laboratorio

**La métrica de éxito se define antes del método, y es doble.**

*Primaria, cuantitativa:* en el conjunto de 29 ARNdc de *T. castaneum* con hazard ratio
medido, la correlación de Spearman entre nuestro score y el hazard ratio observado debe
**igualar o superar** la del score de siRNA de dsRIP solo. El baseline no es cero: es un
método publicado con validación prospectiva, y superarlo no está garantizado. Si no lo
superamos, se reporta así.

*Secundaria, la que responde al desafío:* para el conjunto de candidatos del EPILAB,
producir un ranking en el que cada par de candidatos esté clasificado como **orden robusto**
o **empate dentro de la incertidumbre**, con cada término trazable a una fuente abierta y
citada. El entregable vale por eso, no por la correlación.

**Los experimentos, en orden.**

**V1 — Retrospectiva contra ARNdc largo en *Tribolium*.** Los 8 genes esenciales por 3 a 4
regiones de ARNdc con hazard ratio medido de Cedden et al. Spearman contra el observado.
Baselines: el score de siRNA de dsRIP solo, si-Fi21 en modo HE, y azar. Es el experimento
que decide si el método tiene algún valor predictivo. n aproximadamente 29.

**V2 — Retrospectiva contra siRNA individuales.** Los 29 siRNA insertados en esqueleto de
mGFP, que son el caso limpio porque aíslan el efecto de la secuencia del efecto del gen
blanco (todos apuntan a *Tc-gawky*). Es el único conjunto del campo que permite esa
separación.

**V3 — Prueba de rango en la especie blanco.** Para cada una de las seis construcciones
publicadas en *D. maidis*, calcular el score de todas las ventanas de 300 pb del mismo
transcripto y verificar en qué percentil cae la región efectivamente usada y que funcionó.
Si el método sirviera, las regiones publicadas deberían caer por encima de la mediana.
**Advertencia que debe acompañar siempre este resultado:** n=6, sin controles negativos
diseñados, y las secuencias exactas hay que extraerlas de las listas de primers de cada
paper. Es una señal, no un benchmark, y presentarla como benchmark sería deshonesto.

**V4 — Comparación contra los baselines que ya existen.** dsRIP (vía su web o
reimplementando desde los depósitos de figshare, cuya licencia hay que verificar) y si-Fi21
(CC BY-SA, con la fricción de ser software de escritorio sólo para Windows en Python 2.7
`[E]`). Que el baseline sea bueno es una buena noticia para el proyecto y una mala para la
expectativa de ganarle: hay que entrar con esa expectativa calibrada.

**V5 — Ablaciones, que son el aporte de conocimiento más probable.**
(a) Con y sin el término de accesibilidad: si el método **empeora** al incluirlo, eso replica
el hallazgo de Cedden et al. en un análisis independiente y es un resultado reportable.
(b) Coeficientes de insecto contra coeficientes de la literatura humana, incluido el signo
invertido del %GC: cuantifica el costo de importar supuestos de células humanas.
(c) Con y sin el término de off-target: mide cuánta eficacia predicha se sacrifica por
seguridad, que es la pregunta que el deslizador de dsRIP plantea sin responder.
(d) Si sobra tiempo, el brazo de embeddings congelados de RNA-FM, declarado como
exploratorio y con n=29 explícito.

**V6 — Controles negativos y de fuga.** Candidatos con secuencia barajada deben ordenarse
bajo. Y las particiones tienen que ser conscientes de la fuga de datos: siguiendo los
protocolos que la revisión del campo recomienda, **mRNA-split** (ningún transcripto blanco de
test apuntado por un caso de entrenamiento) y no partición aleatoria, porque la fuga "has
systematically inflated benchmark results" en este campo `[E]`. Con n=29 esto significa en
práctica validación cruzada dejando un gen afuera (leave-one-gene-out), que es la única
partición honesta disponible.

**Qué NO podemos validar, y hay que escribirlo en la primera página del entregable.** No
podemos validar la transferencia de Coleoptera a Hemiptera. Es la incertidumbre dominante,
los propios autores de dsRIP la señalan como pendiente para otros órdenes `[E]`, y ningún
experimento computacional la resuelve. Tampoco podemos validar el término de conservación
poblacional, ni la relevancia funcional de los off-targets predichos, ni nada relativo a la
entrega oral más allá de anotar la condición. Un entregable que no diga esto está vendiendo
algo que no tiene.

---

## Qué se rescata de la idea original

Vale la pena cerrar reconociendo lo que la idea acertó, porque es más de lo que parece.

El integrante identificó, sin conocer el campo, que el problema tiene la **forma** correcta
de un problema de secuencias con estructura posicional, donde distintas porciones del
transcripto tienen distinto valor y hay que encontrar cuál. Eso es exactamente lo que hace
la ventana deslizante sobre el score de siRNA, y es el estado del arte. Identificó que la
termodinámica es parte de la señal: también correcto, aunque con la herramienta equivocada y
en el lugar equivocado de la ecuación. Identificó que los embeddings de un modelo
preentrenado podrían servir como representación: correcto, publicado, y con beneficio
marginal cuestionado por la propia literatura. Y su intuición de "ver la relación entre las
distintas secuencias" para identificar regiones del transcrito es la mejor parte de la idea:
se satisface con un perfil posicional explícito del score, que es fiel por construcción, en
lugar de con pesos de atención, que la literatura dice que no sostienen una lectura causal.

Lo que hay que abandonar es la termodinámica como loss, BLAST como calculador de
termodinámica, el fine-tuning sobre datos que no existen, y la generación de secuencias
nuevas sin manera de verificarlas. Lo que hay que construir está en `PROPUESTA.md`.
