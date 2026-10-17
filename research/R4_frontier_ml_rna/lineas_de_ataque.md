# Líneas de ataque — R4

Cuatro propuestas, ordenadas. El orden no es neutro y el criterio está escrito
abajo. Cada línea declara explícitamente si los datos que necesita existen hoy.

> **Veredicto de la ola 2 — 2026-10-17.** Con el corpus oficial y con los datos
> efectivamente descargados y medidos, **el orden no cambia: L1 > L2 > L3 >> L4**,
> y ahora la factibilidad está evaluada contra datos que existen de verdad. El
> cruce línea por línea está en `research/ola2/W4_genomas/viabilidad_lineas.md`;
> las correcciones, en `research/ola2/CORRECCIONES.md`.
>
> - **L1 y L2: viables con lo que hay.** El insumo que faltaba —los candidatos
>   del EPILAB— llegó, y el transcriptoma que esta línea daba por inexistente
>   resultó ser tres transcriptomas descargables.
> - **L3: viable con dos faltantes declarados.** No hay etiquetas de esencialidad
>   génica para hemípteros, y el panel de no objetivo del agroecosistema argentino
>   sigue sin existir: lo que se corrió usa especies modelo como sustitutas.
> - **L4: inviable, y el corpus lo confirma por una vía nueva.** No sólo faltan
>   los datos de entrenamiento; la herramienta que el organizador entrega bajo el
>   rótulo de diseño y verificación **no estima eficacia de ninguna forma**:
>   cuenta coincidencias exactas de k-meros con Bowtie y las suma.
>
> Eso corre el eje del aporte y conviene decirlo así ante el jurado: **no se trata
> de modelar mejor que el estado del arte, sino de decidir mejor con lo que ya se
> calcula.** La vara es más baja de lo que suponía este documento, y el hueco de
> eficacia es ahora un hueco verificado del material oficial.

Marcadores: `[E]` establecido, `[R]` reportado, `[H]` hipótesis nuestra,
`[?]` incierto. Las fuentes están en `sources.json`; todas fueron abiertas.

---

## Criterio de priorización (explícito, y no es el nuestro)

La última diapositiva del material oficial de la sesión técnica del Investigathón
dice, textual: *"Un equipo no debería ganar por construir la interfaz más
vistosa, sino por producir la mejor decisión científica posible con el tiempo y
los datos disponibles"* (transcripto en `docs/sesion-tecnica-EPILAB-notas.md`).
Y la pregunta abierta que el organizador declara, sobre candidatos preliminares
que el laboratorio del EPILAB ya tiene diseñados, es: *"¿cuáles candidatos
merecen validación y por qué?"*.

De ahí se derivan cuatro preguntas que ordenan las líneas, en este orden de peso:

1. **¿Cuánta decisión defendible produce?** Una línea que contesta la pregunta
   declarada vale más que una que exhibe un modelo grande. Una línea que usa un
   modelo impresionante y no mejora ninguna decisión queda abajo, sin importar su
   mérito técnico.
2. **¿Los datos que necesita existen hoy, y son abiertos?** Si no existen, baja.
3. **¿Es auditable?** Criterio escrito, incertidumbre explícita, código y fuentes
   abiertas. Sin eso no es una decisión: es una opinión con tabla.
4. **¿Cabe en el plazo, con cuatro personas y sin laboratorio?**

Un quinto criterio, propio del proyecto y no negociable: toda propuesta trae su
contracara de riesgo (off-target en maíz y en organismos no objetivo,
persistencia, resistencia). Eso no ordena las líneas: las condiciona a todas.

**Resultado del ordenamiento:** L1 > L2 > L3 >> L4. L1 y L2 son una sola decisión
en dos tiempos (L1 produce el ranking, L2 lo mide); si hubiera que elegir una
sola, es L1, pero L1 sin L2 es una opinión. L3 es independiente y es la línea que
cubre la obligación de riesgo. L4 va última y está documentada como descarte
razonado, que es lo que `00_meta/CAMINOS_PROBADOS.md` pide.

---

# L1 — Tamizaje multiobjetivo auditable con incertidumbre explícita sobre los candidatos del EPILAB

**Prioridad: 1 de 4.** Es la única línea que ataca de frente la pregunta abierta
declarada por el organizador.

### Qué modelo o técnica usa

Deliberadamente, **ninguno de los modelos fundacionales del catálogo**. La
decisión está respaldada por tres resultados abiertos: en baja homología ningún
modelo de lenguaje de ARN mejora significativamente sobre una codificación
one-hot en estructura secundaria `[E]` (Zablocki et al. 2025, F1 < 0,40 para
todos los modelos en PDB-RNA contra 0,67 del método termodinámico); el
relevamiento de aprendizaje automático para siRNA concluye textualmente que los
embeddings de modelos fundacionales son *suficientes pero no necesarios* para el
estado del arte, porque DeepSilencer iguala o supera a OligoFormer en Mixset
(0,858 contra 0,845) sin ninguno `[E]`; y lo que sí rinde son los **modelos
híbridos que integran características termodinámicas con representaciones
aprendidas** `[E]`.

La tubería, en cinco módulos:

1. **Descomposición.** Cada dsRNA candidato se parte en todos los siRNA de 21 nt
   derivables, que es la unidad que efectivamente carga en RISC.
2. **Puntaje de eficacia por siRNA.** Reimplementación de las **cuatro
   características que dsRIP validó experimentalmente en insecto** `[R]`:
   asimetría termodinámica, energía de autoplegado de la cadena antisentido,
   porcentaje de GC en los nucleótidos 9–14 de la antisentido, y adenina en la
   posición 10. El modelo de referencia es una regresión de riesgos
   proporcionales de Cox con estadístico C de Harrell 0,76 (IC 95 % 0,73–0,79).
   La asimetría de extremos (ΔΔG5′) está descrita en el relevamiento de siRNA
   como la característica de diseño más importante de toda esa literatura `[R]`:
   las dos fuentes, independientes y de campos distintos, convergen en ella, y eso
   es lo más cerca de evidencia robusta que hay en este subcampo.
3. **Accesibilidad del sitio blanco, con peso bajo y declarado.** RNAplfold de
   ViennaRNA con ventana deslizante, en el régimen que usa DSIR (W = 80, L = 40,
   u = 16) `[R]`. Entra como eje con peso bajo y análisis de sensibilidad, no como
   criterio de descarte, porque la evidencia está en conflicto: el relevamiento de
   siRNA la llama determinante mayor e independiente `[E]`, pero **en dsRIP, el
   único modelo entrenado con bioensayos de insecto, la accesibilidad del ARNm no
   resultó un predictor significativo** `[R]`, y hay un estudio retrospectivo
   sobre siRecords que tampoco encontró relación `[?]`.
4. **Tamizaje de off-target por semilla.** Bowtie contra transcriptomas de maíz,
   *Dalbulus maidis* y organismos no objetivo, con dos criterios en paralelo: la
   regla del subcampo de plagas (coincidencia perfecta o hasta 2 desapareamientos;
   para siRNA de 21 nt, al menos 19 nucleótidos complementarios) `[E]` y la
   mecánica de semilla establecida en la literatura de siRNA (posiciones 2–5
   esenciales para la actividad fuera de blanco, 6–8 contribuyen a las dos cosas,
   8–14 correlacionan negativamente, 6-mero 2–7 como característica más
   ampliamente predictiva) `[E]`. Las dos reglas no coinciden, y mostrar dónde
   difieren ya es un aporte.
5. **Calibración e incertidumbre.** Acá está el diferencial real. El relevamiento
   de siRNA afirma textualmente que **ningún método formal de cuantificación de
   incertidumbre se ha aplicado a la predicción de eficacia de siRNA**, y lo llama
   *posiblemente la brecha de máxima prioridad del campo*, proponiendo predicción
   conformal (*conformal prediction*), que da garantías de cobertura libres de
   distribución y se puede envolver sobre cualquier predictor existente `[E]`.
   La entrega no es un ranking puntual: es un **intervalo de cobertura declarada
   por candidato**, más una ficha de trazabilidad que dice qué características lo
   subieron, qué lo bajó, y qué no se pudo evaluar.

> **Actualización del 17 de octubre de 2026 (ampliación del relevamiento).** La
> decisión de no usar un modelo fundacional queda *más* respaldada, con dos
> resultados nuevos que no estaban cuando se escribió esta línea. Primero, en el
> benchmark en cero disparos revisado por pares de 21 modelos de ARN, los dos
> que mejor capturan estructura pese a tener poco ARN no codificante en sus
> datos —MP-RNA y PlantRNA-FM— lo logran porque **incorporan predicciones de
> ViennaRNA en el preentrenamiento** `[E]`: dentro de los modelos fundacionales
> que funcionan, la termodinámica ya está adentro, así que usarla directamente
> no es una renuncia sino el mismo ingrediente sin la capa intermedia. Segundo,
> en la tarea más parecida a "predecir el efecto de una secuencia que nadie
> midió" —aptitud mutacional en cero disparos— el rendimiento absoluto de todos
> los modelos es pobre: **MCC medio por debajo de 0,20, AUC por debajo de 0,64**
> `[E]`. Fuente: Wang et al., *Briefings in Bioinformatics* 27(2) bbag098 (2026).
>
> **Módulo opcional nuevo, módulo 6: anotación del diseño estructural de la
> molécula.** El relevamiento ampliado encontró un eje de diseño que ninguna
> herramienta computacional del catálogo cubre y que **sí tiene validación
> húmeda reciente**: la arquitectura física del dsRNA. En *Varroa destructor*,
> dsRNA de extremos en lazo con apareamientos G-U oscilantes (ledG:U) o con una
> protuberancia asimétrica cada 22 nt (led[Δ22]) dieron el **doble de
> estabilidad**, silenciamiento de 36 a 86 % y aumento de mortalidad de 32 a
> 56 % respecto del dsRNA convencional, en laboratorio, con n = 5 réplicas
> biológicas `[R]` (Muita et al., *Frontiers in Insect Science*, agosto de
> 2026). Lo decisivo para nosotros: en led[Δ22] **la secuencia de la hebra
> antisentido no cambia**, de modo que la estabilidad mejora sin alterar el
> perfil de efectos fuera de blanco. Son dos decisiones ortogonales, y la ficha
> por candidato puede declarar explícitamente cuál arquitectura se asume, en
> lugar de dejarlo implícito. Entra como **anotación declarada, no como término
> del puntaje**, porque no tenemos forma de predecir ese efecto desde secuencia
> ni de validarlo.

### Qué datos necesita, y si existen

| Dato | ¿Existe? | Dónde |
| --- | --- | --- |
| Características y coeficientes del modelo de eficacia de insecto | **Sí** `[R]` | dsRIP: preprint abierto; datos en figshare 10.6084/m9.figshare.27490890.v1 y .27495843.v1; lecturas en SRA PRJNA1157760 |
| Cálculo de accesibilidad y energía de plegado | **Sí** `[E]` | ViennaRNA (RNAplfold, RNAfold), local, segundos por transcripto |
| Transcriptomas de plagas y no plagas | **Sí, con cobertura desigual** `[R]` | dsRNAEngineer aloja 942 transcriptomas de NCBI (439 RefSeq) al 2024-07-05; dsRIP infiere ortología sobre 83 organismos |
| Transcripto / genoma de *D. maidis* | **Sí, parcialmente** `[E]` | hay transcriptoma publicado y los transcriptos de *eth* y *burs-α* están en GenBank (PZ371507–PZ371510) |
| Genoma y transcriptoma de maíz | **Sí** `[E]` | Ensembl Plants / NCBI |
| **Los candidatos preliminares del EPILAB** | **NO los tenemos** | Hay que pedirlos. Es la única dependencia externa de esta línea, y es bloqueante para la versión final (no para construir la tubería) |

### Qué se podría demostrar en el plazo del Investigathón

Un ranking de los candidatos del EPILAB con intervalo de incertidumbre por
candidato, una ficha de una página por candidato con su criterio desagregado, y
el código que lo reproduce. Si los candidatos no llegan a tiempo, la misma
tubería se demuestra sobre los cuatro dsRNA publicados en *D. maidis* y
*D. kuscheli* más un conjunto de candidatos propios generados sobre genes
esenciales conservados: el entregable sigue siendo la **decisión y su
trazabilidad**, no la lista.

### Riesgo principal

**El modelo de eficacia viene de un coleóptero y *D. maidis* es un hemíptero.**
dsRIP se entrenó y validó en *Tribolium castaneum*, *Psylliodes chrysocephala* y
*Leptinotarsa decemlineata*, y el relevamiento de 2026 le anota como limitación
explícita que falta probarlo fuera de coleópteros `[E]`. Mitigación: usar el
puntaje como **ordenador relativo dentro del conjunto de candidatos**, nunca como
predicción absoluta de eficacia; declarar la transferencia como no validada en
cada ficha; y medirla en L2.

Riesgo secundario: el propio dsRIP advierte que su puntaje promedia todos los
siRNA por igual, lo que diluye los efectos posicionales `[R]`. Nuestra versión
puede reportar la distribución de puntajes por dsRNA y no solo la media, que es
una mejora chica, honesta y defendible.

### Esfuerzo estimado

Bajo. Dos personas, entre tres y cinco días. No hay entrenamiento: hay
reimplementación de features documentadas, llamadas a ViennaRNA y a Bowtie, y un
envoltorio de predicción conformal. El costo real está en el curado de
transcriptomas y en escribir bien las fichas.

---

# L2 — Validación retrospectiva del puntaje contra el RNAi publicado en hemípteros

**Prioridad: 2 de 4.** Es lo que convierte L1 de propuesta en medición. No es una
alternativa a L1: es su condición de credibilidad.

### Qué modelo o técnica usa

Ninguno nuevo. Es un **protocolo de evaluación**, y el protocolo es el aporte.

Se adopta la metodología de las dos críticas abiertas más duras del campo:
la validación cruzada **por familia** de Szikszai et al., que mostró que el F1
cae de 0,72 a 0,50 cuando se deja una familia afuera y que la validación cruzada
aleatoria es insuficiente como benchmark `[E]`; y los protocolos **partición por
siRNA** y **partición por ARNm** del relevamiento de siRNA, que existen porque
*la fuga de datos entre entrenamiento y prueba ha inflado sistemáticamente los
resultados de benchmark de todo el campo* `[E]`. Traducidos a nuestro problema:
**partición por gen y por especie, nunca aleatoria.**

Procedimiento:

1. Curar a mano un conjunto de dsRNA publicados con efecto medido en hemípteros,
   registrando para cada uno: especie, gen, longitud del amplicón, vía de entrega,
   concentración, n, lectura (knockdown por RT-qPCR, mortalidad, fenotipo) y la
   secuencia exacta cuando está disponible.
2. Calcular el puntaje de L1 sobre cada uno, a ciegas del resultado.
3. Medir concordancia de orden (ρ de Spearman, AUC si se binariza) con partición
   por gen y por especie, y reportar el **intervalo de confianza junto con el n**.
4. Reportar el resultado aunque sea negativo.

### Qué datos necesita, y si existen

**Existen, pero son decenas, no miles.** Lo verificado hasta acá:

- **Cuatro dsRNA, dos genes, dos especies, con números completos** `[E]`:
  Andrada et al. 2026 en *Frontiers in Insect Science*, silenciando *eth* y
  *burs-α* en *D. maidis* y *Delphacodes kuscheli*. Amplicones T7 de 578 pb
  (*burs-α* de *D. maidis*), 544 pb (*eth* de *D. maidis*), 326 pb y 394 pb;
  microinyección de 0,25 µL a 500 ng/µL en ninfas de quinto estadio; knockdown de
  ~95 % y ~90 % al día 4; supervivencia cayendo a 10 % con *burs-α*; 77,5 % con
  alas deformes; n = 40 por tratamiento; control de β-lactamasa con supervivencia
  > 95 %. Las secuencias con las regiones blanco marcadas están en material
  suplementario y los transcriptos en GenBank (PZ371507–PZ371510). **Esto solo ya
  permite una prueba de concordancia de cuatro puntos.**
- **Más trabajos en *D. maidis*, por verificar** `[R]`: hay literatura sobre
  silenciamiento de *bicaudal-C* por inyección y por ingesta, y sobre knockdown de
  dsRNasas para mejorar el RNAi oral. Este último **no pudo abrirse** (rechazo de
  herramienta registrado, ver `00_meta/PREGUNTAS_ABIERTAS.md`) y es prioridad
  abrirlo por otra vía.
- **Otros hemípteros** `[R]`: hay trabajos en *Peregrinus maidis* (silenciamiento
  de *Ruvbl1* afectando la reproducción) y en otros vectores; cada uno hay que
  abrirlo y verificarlo antes de entrar al conjunto.
- **Lo que NO existe:** un conjunto público, curado y con secuencias, de eficacia
  de dsRNA en hemípteros. Construirlo, aunque sea chico, es en sí mismo un
  entregable reutilizable.

### Qué se podría demostrar en el plazo del Investigathón

Un conjunto curado publicable (tabla con fuente, n y contexto experimental por
entrada) y una medición de concordancia con su n y su intervalo. Dos resultados
posibles, los dos útiles: que el puntaje ordena mejor que el azar, lo que respalda
L1; o que **con este n no se puede distinguir del azar**, lo que es un hallazgo
honesto y es exactamente el tipo de afirmación que una priorización defendible
necesita declarar.

### Riesgo principal

**Potencia estadística y sesgo de publicación.** Con decenas de puntos, el
intervalo de confianza va a ser ancho. Y casi todos los dsRNA publicados
funcionan: los que no funcionaron rara vez se publican, así que el conjunto está
truncado por arriba del efecto. Mitigación: no convertir el resultado en un
número de rendimiento, sino en un enunciado de capacidad discriminativa con su
incertidumbre; y aprovechar los controles negativos que los propios trabajos
reportan (β-lactamasa, mGFP) como ancla del extremo bajo.

Riesgo secundario: la heterogeneidad de condiciones. Inyección contra ingesta,
longitudes de 326 a 578 pb, lecturas distintas. Es el mismo problema que el
relevamiento de siRNA documenta para los nueve conjuntos de OligoFormer, que
difieren en línea celular, transfección, método de lectura y escala temporal, y
que requirieron normalización específica por conjunto `[E]`. La mitigación es la
misma: estratificar por vía de entrega y no mezclar.

### Esfuerzo estimado

Medio. Una a dos personas, cuatro a seis días, casi todo lectura y curado manual
de papers. Es la línea con menos código y más disciplina.

> **Actualización del 17 de octubre de 2026.** La pregunta obvia sobre esta
> línea es si la extracción desde literatura se puede automatizar, y ahora hay
> una respuesta medida. PaperQA2 alcanza en el benchmark LitQA2 una **precisión
> de 85,2 % ± 1,1 %** contra **73,8 % ± 9,6 %** de anotadores con doctorado,
> pero una **exactitud de 66,0 % ± 1,2 %** contra **67,7 % ± 11,9 %** de los
> humanos: la diferencia es significativa en precisión (p = 0,0036) y **no lo es
> en exactitud** (p = 0,66), y la precisión superior se consigue
> **absteniéndose en el 21,9 % de los casos** `[R]` (Skarlinski et al., arXiv
> 2409.13740, abierto el 17 de octubre; resuelve un pendiente registrado).
> Además, su sistema de resúmenes deja **13,5 % de afirmaciones citadas y no
> sostenidas**, una de cada siete.
>
> Consecuencia para esta línea, y es un refuerzo, no un cambio de plan: un
> sistema así sirve como **triador** para encontrar y preseleccionar los
> trabajos candidatos, y **no sustituye el curado manual**, porque una tasa de
> una afirmación no sostenida cada siete es incompatible con la regla número uno
> de este repositorio. El curado sigue siendo humano y sigue siendo el costo
> principal de L2.

---

# L3 — Mapa de riesgo fuera de blanco ponderado por consecuencia, no por conteo

**Prioridad: 3 de 4.** Independiente de L1 y L2. Cubre la obligación de contracara
de riesgo del proyecto y ataca un hueco que el propio relevamiento del subcampo
declara abierto.

### Qué modelo o técnica usa

Un índice de riesgo por organismo no objetivo que **pondere por consecuencia y no
solo cuente coincidencias**. El hueco está declarado con precisión: el
relevamiento de Cedden 2026 le anota a dsRNAmax, dsRNAEngineer y dsOMG, a las
tres, la misma limitación —*no considera la función del gen fuera de blanco*— y a
dsCheck también `[E]`. La única que pondera es dsRIP, que suma impactos totales
más impactos en genes esenciales con un peso 20:1 por defecto, normalizado a
0–100 % `[R]`; pero ese 20 es un número por defecto sin justificación publicada, y
ahí hay espacio para un aporte metodológico barato.

Componentes del índice, cada uno con peso explícito:

1. **Carga de coincidencias**: número de siRNA derivables del dsRNA con
   coincidencia de semilla o con ≥ 19 de 21 nucleótidos complementarios en el
   transcriptoma del organismo no objetivo.
2. **Esencialidad del gen impactado**, por ortología. La fuente de esencialidad a
   escala es iBeetle-Base, el tamizaje genómico de RNAi de *T. castaneum*, que
   reporta que los procesos conservados (proteasoma, expresión génica) son blancos
   más efectivos que los genes del sistema nervioso `[E]`. Es exactamente el
   mecanismo que dsRIP usa, y hereda su sesgo: **es una sola especie de
   coleóptero**.
3. **Exposición ecológica**, como factor declarado y editable: polinizadores
   (*Apis mellifera*), enemigos naturales, fauna del suelo, maíz y humano. No es
   un número que se pueda derivar de secuencia; es un juicio que el índice debe
   exponer en lugar de esconder.
4. **Análisis de sensibilidad** sobre los tres pesos, incluido el 20:1 de dsRIP,
   para mostrar cuánto cambia el orden de los candidatos según el peso elegido. Si
   el orden es robusto a los pesos, la decisión es fuerte; si no, eso hay que
   decirlo.

### Qué datos necesita, y si existen

| Dato | ¿Existe? |
| --- | --- |
| Transcriptomas de maíz y de *D. maidis* | **Sí** `[E]` |
| Transcriptoma de *Apis mellifera* | **Sí** `[E]`, es una de las especies no objetivo que dsRIP usa como ejemplo |
| Transcriptomas de enemigos naturales y fauna del suelo regionales | **Parcialmente, cobertura desigual** `[R]`. dsRNAEngineer aloja 942 transcriptomas, algunos ensamblados de novo con Trinity en lugar de genomas de referencia |
| Etiquetas de esencialidad génica | **Sí para *T. castaneum*** (iBeetle-Base) `[E]`. **No existe equivalente para hemípteros** |
| Un benchmark para validar el índice | **NO EXISTE.** El relevamiento de siRNA lo dice textual: ninguna de las herramientas de off-target constituye un benchmark estandarizado por la comunidad comparable a Huesken, y los recursos experimentales están dispersos en lugar de estandarizados `[E]` |

### Qué se podría demostrar en el plazo del Investigathón

Un mapa de riesgo por candidato y por organismo, con los pesos a la vista, y la
curva de sensibilidad que muestra qué decisiones sobreviven al cambio de pesos.
Es el entregable que hace auditable la parte del problema que más se suele
maquillar.

### Riesgo principal

**El índice mide riesgo potencial, no efecto.** El relevamiento de Cedden 2026
cita un estudio en *Leptinotarsa* donde **los cambios transcriptómicos no
coincidieron con la complementariedad in silico** `[E]`, y dsRIP declara que su
propio módulo de off-target es computacional únicamente, sin validación
experimental `[R]`. Cualquier afirmación de seguridad derivada de este mapa sería
una sobreinterpretación. Mitigación: nombrarlo explícitamente *mapa de riesgo
potencial*, y que cada celda del mapa cargue la frase de que no está validada
experimentalmente.

Riesgo secundario: el sesgo de especie de la esencialidad. Heredar iBeetle para
razonar sobre un hemíptero o sobre una abeja es una extrapolación grande, y hay
que marcarla en cada uso.

### Esfuerzo estimado

Medio-alto. Dos personas, cinco a siete días. El costo no está en el algoritmo
—es conteo sobre alineamientos— sino en el curado de los transcriptomas no
objetivo y en el mapeo de ortología, que es donde se van las horas.

> **Actualización del 17 de octubre de 2026.** Aparece evidencia directa contra
> la alternativa de resolver el tamizaje fuera de blanco con un modelo
> fundacional en lugar de con alineamiento. En BEACON, el benchmark
> independiente de trece tareas de ARN, la tarea de predicción de efecto **fuera
> de blanco** de CRISPR da correlación de Spearman de **12,6** para el método
> específico, **11,40** para una CNN entrenada desde cero, y entre **2,49 y
> 5,00** para *todos* los modelos de lenguaje de ARN evaluados, incluido RNA-FM,
> que queda último `[E]` (Ren et al., NeurIPS 2024). No es nuestra tarea exacta,
> pero es la más parecida que está medida: predecir desde secuencia la
> consecuencia de un apareamiento imperfecto. Refuerza mantener el índice sobre
> alineamiento y conteo ponderado, que además es auditable.

---

# L4 — Ajuste fino de un modelo fundacional de ARN para eficacia de dsRNA en insectos

**Prioridad: 4 de 4, y el orden es el aporte.** Esta es la línea que más
impresiona y la que menos decisión produce. Queda documentada como **descarte
razonado**, con la condición explícita que la reactivaría.

### Qué modelo o técnica usaría

Embeddings de RiNALMo (650 M, pesos CC BY 4.0, licencia verificada) o de AIDO.RNA
(1,6 B) más una cabeza supervisada de regresión o clasificación, en el patrón de
OligoFormer (embeddings de RNA-FM + características termodinámicas + transformer),
que es el que el campo de siRNA ya recorrió.

### Qué datos necesita, y si existen

**No existen en escala ni calidad suficientes.** Esto es lo que la descarta, y
está documentado en fuentes abiertas:

- La única fuente de etiquetas de eficacia de dsRNA a escala es **iBeetle-Base**,
  y el relevamiento de 2026 le anota como limitación que es **solo *Tribolium
  castaneum*** `[E]`. Una sola especie de coleóptero no entrena un modelo que
  decida sobre un hemíptero.
- El único intento publicado de usar esos datos, **dsRNAPredictor**, construyó los
  negativos **barajando fragmentos de ARNm de la misma base** `[R]`. Un
  clasificador puede resolver "secuencia real contra secuencia barajada" sin
  aprender nada sobre eficacia de silenciamiento. Y falla donde se lo puede medir
  fuera de su especie: en quitina sintasa de *Aedes aegypti*, su mejor fragmento
  (dsCHSA_1550) no coincide con el mejor experimental (dsCHSA_1928) `[R]`.
- El modelo de eficacia validado en insecto —dsRIP— se entrenó con **31 siRNA**
  `[R]`. Treinta y uno. Ese es el tamaño real del conjunto de entrenamiento
  honesto que existe en este subcampo.
- La literatura de siRNA humano sí tiene miles de puntos (Huesken: 2.431 siRNA
  contra 34 ARNm), pero su propio relevamiento **no evalúa generalización entre
  especies y no menciona RNAi de insecto** `[E]`, y las herramientas que
  intentaron esa transferencia (si-Fi, E-RNAi, DEQOR) figuran en el relevamiento
  de plagas justamente con *basado en datos humanos* como limitación `[E]`.

### Por qué queda última, en términos del criterio

Falla los cuatro filtros a la vez. **Decisión:** si el modelo no se puede validar,
su salida no mejora ninguna decisión sobre cuáles candidatos merecen validación.
**Datos:** no existen. **Auditabilidad:** un modelo profundo ajustado sobre
etiquetas de una sola especie, con negativos dudosos y sin cuantificación de
incertidumbre, es el opuesto de auditable. **Plazo:** consume el presupuesto de
tiempo de L1, L2 y L3 juntas.

Y hay una razón adicional, específica de este eje: el benchmark independiente
muestra que **en baja homología los embeddings de modelos de lenguaje de ARN no
superan a one-hot** `[E]`, y el relevamiento de siRNA concluye que esos embeddings
son *suficientes pero no necesarios* `[E]`. Es decir: incluso si los datos
existieran, el beneficio esperado del modelo fundacional sobre un híbrido
termodinámico simple no está demostrado.

### Qué la reactivaría (condición explícita)

Tres cosas, y hacen falta las tres:

1. Un conjunto de **al menos unos cientos de dsRNA en hemípteros** con lectura
   cuantitativa y **negativos reales** (dsRNA probados que no silenciaron), no
   barajados.
2. Un protocolo de partición sin fuga (por gen y por especie), porque sin eso
   cualquier número reportado estaría inflado por el mismo mecanismo que el
   relevamiento de siRNA documenta para todo el campo.
3. Cuantificación de incertidumbre encima, porque la salida tiene que ser
   accionable para decidir qué se valida.

### Esfuerzo estimado si se hiciera igual

Alto y mal invertido. Tres a cuatro personas, todo el plazo, con alta probabilidad
de reproducir el error metodológico de dsRNAPredictor y de no poder distinguir si
el modelo aprendió eficacia o aprendió a reconocer secuencias reales.

> **Actualización del 17 de octubre de 2026.** El descarte se sostenía en un
> benchmark independiente (Zablocki et al.) y en la conclusión del relevamiento
> de siRNA. Ahora hay **cuatro evaluaciones independientes**, con diseños
> distintos y grupos distintos, y todas apuntan al mismo lado `[E]`:
>
> 1. **Tang, Somia, Yu y Koo** (*Genome Biology* 26:203, 2025): sondeando
>    representaciones sin ajuste fino en seis tareas de genómica funcional, los
>    modelos de ADN "provided little to no advantage over standard one-hot
>    encoded sequences", y el token CLS codifica poco más que estadística de
>    dinucleótidos.
> 2. **BEND** (ICLR 2024): catorce modelos contra métodos expertos; sin mejoras
>    consistentes, y la generalización entre organismos —justo lo que
>    necesitaríamos— queda declarada como **pregunta abierta sin medir**.
> 3. **BEACON** (NeurIPS 2024): una LSTM entrenada sólo en la tarea supera a las
>    demás líneas base en 9 de 13 tareas, y en la tarea tipo fuera de blanco los
>    modelos fundacionales rinden la mitad que una CNN.
> 4. **Wang et al.** (bbag098, 2026): aptitud mutacional en cero disparos con
>    MCC medio por debajo de 0,20 para los 21 modelos evaluados.
>
> Ninguna de las cuatro cambia la prioridad de L4: la confirma. Y la condición
> explícita que la reactivaría sigue siendo la misma, porque ninguna de las
> cuatro resuelve el problema de fondo, que es la ausencia de etiquetas en
> hemípteros.

---

## Revisión del 17 de octubre de 2026 — qué cambió y por qué

Esta sección existe porque el archivo se escribió con un relevamiento que después
se amplió, y corresponde dejar dicho qué se movió. La ampliación agregó once
fuentes abiertas, orientadas a lo que el prompt de R4 exige y que la primera
tanda cubría de manera despareja: **crítica independiente de cada familia de
métodos** y **separación explícita entre resultado validado experimentalmente y
resultado sólo computacional**. El detalle crudo está en
`notes/03_material_crudo_ampliacion.md` y el desarrollo en `REPORT.md`.

**El orden de prioridad no cambió: sigue siendo L1 > L2 > L3 >> L4.** Ninguna
evidencia nueva movió una línea de lugar. Lo que cambió es la fuerza del
argumento en cuatro puntos, y se agregó un módulo:

1. **L1 se refuerza por una vía que no esperábamos.** No es sólo que los modelos
   fundacionales no aventajen a lo simple; es que **los modelos fundacionales de
   ARN que mejor funcionan en estructura llevan ViennaRNA adentro**. El
   argumento deja de ser "renunciamos al modelo grande" y pasa a ser "usamos
   directamente el ingrediente que al modelo grande le da el resultado".
2. **L1 incorpora un módulo 6 opcional de anotación del diseño estructural de la
   molécula**, a partir de la validación húmeda en *Varroa destructor* de los
   diseños ledG:U y led[Δ22]. Se agrega como anotación declarada y no como
   término del puntaje, por la razón de siempre: no podemos predecir ese efecto
   desde secuencia ni validarlo sin laboratorio.
3. **L2 no cambia de plan, pero ahora responde a la objeción obvia** de por qué
   el curado es manual: porque la mejor herramienta publicada de extracción
   desde literatura es superior a los humanos en precisión y **equivalente en
   exactitud**, y deja una afirmación citada y no sostenida cada siete.
4. **L3 y L4 se refuerzan** con los resultados de BEACON y de los tres
   benchmarks independientes nuevos, detallados en sus respectivas secciones.

Lo que **no** cambió y conviene decirlo para que no parezca omisión: la
accesibilidad del sitio blanco sigue entrando con peso bajo y análisis de
sensibilidad, porque la evidencia nueva no resolvió el conflicto —lo agravó, al
mostrar que la predicción de estructura de la que depende es menos confiable
justamente en el régimen de baja homología que es el nuestro.

---

## Anexo — dos líneas consideradas y descartadas antes de llegar a la lista

**Diseño generativo / inverso de secuencias de dsRNA.** La técnica funciona y hay
validación húmeda: gRNAde igualó a expertos humanos en la competencia ciega Eterna
OpenKnot (100 % y 90 % de éxito en la ronda 3) y logró 31,5 % de variantes activas
de la ribozima polimerasa 5TU en el rango de 15–19 mutaciones, contra 15,0 % del
diseño racional filtrado `[R]`. Lo que la descarta para nosotros es la **asimetría
del ensayo**: gRNAde pudo validar porque existía una biblioteca de alto
rendimiento con lectura de actividad ribozimática sobre casi 2.000 secuencias. En
RNAi de insecto la lectura es bioensayo de mortalidad con decenas de individuos
por tratamiento (n = 20–25 en dsRIP, n = 40 en el trabajo de *D. maidis*). Sin
laboratorio y sin ensayo de alto rendimiento, generar secuencias produce
candidatos que nadie puede evaluar. Dato colateral que refuerza el descarte: el
propio equipo de gRNAde **descartó su filtro de autoconsistencia 3D basado en
RhoFold porque no recuperaba la geometría nativa del esqueleto** `[R]`, lo que
confirma desde la práctica el techo que CASP16 midió.

**Aprendizaje automático para formulación y entrega.** Es el cuello de botella
declarado por el organizador —las ribonucleasas limitan la entrega oral del ARN— y
por eso se buscó activamente. Lo que hay está en nanopartículas lipídicas para
terapéutica humana: el marco de comparación abierto más útil evalúa modelos de
eficiencia de transfección sobre **1.100 estructuras únicas de lípido ionizable
derivadas de un único conjunto en células HeLa**, y concluye que los modelos con
codificación explícita de subestructura molecular son la línea base a batir `[R]`.
Dos razones para descartarlo: la generalización fuera de ese único conjunto
derivado de HeLa **no está demostrada ni en la propia fuente** `[?]`, y el blanco
de la optimización es otro (resistencia a nucleasas intestinales y paso del
epitelio, no transfección de una línea celular), sin ningún conjunto público
agrícola con lectura de mortalidad. **Lo que sí se rescata, y entra como módulo
opcional de L1:** la vía de entrega se puede atacar desde la secuencia, con un
dsRNA quimérico que incluya un tramo contra las dsRNasas del propio insecto. Es el
tipo de diseño multiblanco que dsRNAEngineer y dsRNAmax ya soportan `[R]`, y
depende de abrir el trabajo sobre dsRNasas en *D. maidis*, que quedó pendiente por
un rechazo de herramienta registrado en `00_meta/PREGUNTAS_ABIERTAS.md`.

---

## Resumen para decidir en una pantalla

| Línea | Decisión que produce | ¿Datos? | Entregable | Riesgo principal | Esfuerzo |
| --- | --- | --- | --- | --- | --- |
| **L1** Tamizaje con incertidumbre | Cuáles candidatos merecen validación, con intervalo y traza | Sí, salvo los candidatos del EPILAB | Ranking con intervalos + ficha por candidato + código | Transferencia coleóptero → hemíptero no validada | Bajo (2 pers., 3–5 días) |
| **L2** Validación retrospectiva | Si el puntaje de L1 discrimina, y cuánto | Sí, pero son decenas | Conjunto curado + concordancia con n e intervalo | n chico y sesgo de publicación | Medio (1–2 pers., 4–6 días) |
| **L3** Riesgo off-target ponderado | Qué candidato es inaceptable y por qué | Parciales (esencialidad solo de *Tribolium*) | Mapa de riesgo + análisis de sensibilidad de pesos | Mide riesgo potencial, no efecto | Medio-alto (2 pers., 5–7 días) |
| **L4** Modelo fundacional ajustado | Ninguna que se pueda defender hoy | **No** | — (descarte razonado) | Reproducir el error de negativos barajados | Alto y mal invertido |
