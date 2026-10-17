# Rúbrica de priorización de candidatos de ARN exógeno

Versión 1.1, 2026-10-17. Lista para aplicar sin agregarle criterios.

Cambios de la v1.0 a la v1.1, todos hechos al ampliar las fuentes para
`REPORT.md` y todos explicados en el lugar donde ocurren: se incorporó el
criterio de off-target de la guía de la EFSA de 2025 a la compuerta G2 y al
criterio C2; se cerró el pendiente regulatorio de C7 con esa guía y con dos
precedentes de registro más; y se corrigió la fila conservadora del ejemplo
trabajado de la sección 7, que tenía dos totales mal calculados y cuyo arreglo
cambia el orden de los dos últimos candidatos.

## 0. Para qué existe y en qué modo se aplica

El organizador del Investigathón (EPILAB · IFIBYNE, UBA-CONICET) declara dos
cosas que fijan el propósito de este documento. La primera es su pregunta
abierta, textual: "¿cuáles merecen validación y por qué?", sobre candidatos
preliminares que su equipo ya tiene diseñados. La segunda es su criterio de
evaluación, textual: "Un equipo no debería ganar por construir la interfaz más
vistosa, sino por producir la mejor decisión científica posible con el tiempo y
los datos disponibles" (ambas citas de `docs/sesion-tecnica-EPILAB-notas.md`,
transcripción del material del organizador).

Esta rúbrica es la respuesta directa a esa pregunta. Se aplica en dos modos:

- **Modo A, el que importa: un conjunto de candidatos dados.** Entra una lista
  de candidatos de ARN de doble cadena (dsRNA, *double-stranded RNA*) —los del
  EPILAB o los nuestros— y sale un orden, con la justificación por criterio, la
  evidencia que sostiene cada puntaje, la incertidumbre de cada uno y la
  identificación de qué medición cambiaría el orden. El orden no es el
  entregable completo: el entregable es el orden **más** la ficha de decisión de
  cada candidato.
- **Modo B, secundario: un enfoque o una propuesta de línea de trabajo.** Los
  mismos criterios se aplican a una estrategia en lugar de a una secuencia,
  con las anclas de C1b y C2 interpretadas sobre la clase de diseño en lugar de
  sobre una secuencia concreta.

Lo que la rúbrica **no** hace: no predice eficacia en campo, no reemplaza un
bioensayo y no produce un número que se pueda defender sin la ficha que lo
acompaña. Un puntaje sin su ficha no es un resultado.

## 1. Qué es un candidato: la ficha de entrada

Para que un candidato sea puntuable hace falta esto, y nada más que esto. Si
falta un campo, se registra como faltante y se puntúa de forma conservadora
(sección 5.3), no se inventa.

| Campo | Qué es | Ejemplo |
| --- | --- | --- |
| `id` | identificador estable del candidato | `K2` |
| `organismo_blanco` | vector, patógeno o planta | *Dalbulus maidis* |
| `gen_blanco` | nombre y accesión o identificador del transcripto | *BicC* |
| `secuencia_dsrna` | la secuencia del disparador, en FASTA, con su largo | 250 pb |
| `region` | ORF o UTR, con coordenadas sobre el transcripto | ORF, 310–560 |
| `via_entrega_propuesta` | oral en dieta, pulverización foliar, absorción por raíz, inyección, planta transgénica, nanovehículo | pulverización foliar |
| `evidencia_declarada` | qué dice quien propone el candidato que ya se sabe | — |
| `fecha_y_version` | para poder rehacer el puntaje | 2026-10-17, v1 |

## 2. Compuertas: lo que se rechaza antes de puntuar

Las compuertas (*gates*) no se puntúan. Un candidato que no pasa una compuerta
no entra al orden; vuelve a rediseño o se descarta, y eso se escribe.

- **G0 — Alcance ético.** Se rechaza cualquier candidato cuyo diseño busque
  aumentar la virulencia, la transmisibilidad o el rango de hospedadores de un
  patógeno, o que esté dirigido a dañar especies no objetivo. Es la regla
  permanente de `CLAUDE.md` y no admite excepción ni compensación por puntaje.
- **G1 — Blanco verificable.** Tiene que existir la secuencia del disparador y
  la del transcripto blanco con una accesión pública o depositable. Sin
  secuencia no hay nada que tamizar, y un candidato sin secuencia no es un
  candidato: es una idea, y va al Modo B.
- **G2 — Especificidad mínima.** Si alguno de los siRNA derivables del
  disparador tiene **19 nucleótidos o más perfectamente complementarios** con un
  transcripto de *Zea mays*, de *Apis mellifera* o humano, el candidato vuelve a
  rediseño. El umbral no es nuestro: Cedden (2026), *Insect Molecular Biology*
  35(4):364-375, dice textual que "the presence of at least 19 complementary
  nucleotides to an off-target transcript is sufficient to flag the siRNA" `[E]`.
  Importa marcar que una coincidencia de secuencia **no** prueba efecto
  biológico: Romeis y Widmer (2020) citan un colémbolo con seis coincidencias de
  21 nt que no se vio afectado en ensayos de alimentación `[E]`. Por eso G2 manda
  a rediseño y no a descarte, y por eso C3 se puntúa aparte.

  **Agregado del 2026-10-17: el criterio del regulador, que es más exigente que
  el nuestro.** La guía de la EFSA para plantas modificadas por RNAi, aprobada el
  7 de marzo de 2025 (*EFSA Journal* 23:e9321), pide reportar todo transcripto
  off-target que cumpla **todas** estas reglas para cada ARN pequeño de 21 nt
  derivable: no más de cuatro apareamientos erróneos (*mismatches*) sin hueco
  (*gap*), o tres más un hueco; un par G:U cuenta como medio mismatch; un solo
  hueco, de un solo nucleótido, en el blanco o en el ARN pequeño; ningún
  mismatch ni hueco en las posiciones 10 u 11; no más de dos mismatches (o uno
  más un hueco) en los primeros 12 nucleótidos del extremo 5′; y que el cociente
  entre la energía libre mínima del dúplex y la del complemento perfecto sea
  mayor que 0,75 `[E]`. Es un criterio regulatorio publicado, no una heurística:
  admite hasta cuatro mismatches donde el umbral de 19 nt exige complementariedad
  perfecta, de modo que **marca más candidatos, no menos**. La rúbrica mantiene
  el umbral de 19 nt como compuerta —es el que las herramientas de insectos
  implementan y el que corre con Bowtie 1— y adopta el conjunto de reglas de la
  EFSA como tamizaje extendido que se reporta en la ficha de C2 y C3, con la
  salvedad de que Bowtie con 0 a 2 mismatches **no** evalúa huecos, pares G:U,
  restricciones de posición ni el cociente de energía libre: para eso la propia
  EFSA publica un script en su repositorio, que corre en el entorno que uno
  elija y no depende de ninguna base de la agencia `[E]`. Dos límites de alcance
  que hay que decir al citarla: la guía es para plantas modificadas
  genéticamente, no para dsRNA pulverizado, y **declara explícitamente que no
  cubre la evaluación de riesgo ambiental** `[E]`, que es justo la mitad de C3.
- **G3 — Trazabilidad del puntaje.** La ficha tiene que poder regenerarse desde
  la ficha de entrada con un comando, sobre datos versionados. Un puntaje que no
  se puede volver a producir no entra al orden. Esta compuerta es la que vuelve
  operativa la palabra "reproducible" de la pregunta del track: no es un
  criterio que se pondera, es una condición de admisión.

## 3. Los ocho criterios

Cada criterio se puntúa de 0 a 4 con las anclas textuales que están abajo. Cada
puntaje lleva obligatoriamente tres cosas: la **evidencia** que lo sostiene (con
fuente), el **marcador** `[E]` / `[R]` / `[H]` / `[?]` de esa evidencia, y la
marca **(P)** si el dato todavía no existe pero lo podemos producir nosotros
dentro del plazo del evento.

### C1 — Probabilidad de acción biológica · peso 20

Se parte en dos subcriterios y el puntaje del criterio es el promedio, con pasos
de 0,5 permitidos.

**C1a — Evidencia de que silenciar ese gen produce el efecto buscado.**

| Puntaje | Ancla |
| --- | --- |
| 4 | Silenciamiento de ese gen, en *D. maidis*, por una vía de entrega aplicable, con fenotipo cuantificado y control adecuado, publicado y revisado por pares |
| 3 | Silenciamiento de ese gen en *D. maidis* con fenotipo cuantificado, pero por inyección o en condiciones no agronómicas |
| 2 | Silenciamiento del ortólogo en otro hemíptero con fenotipo cuantificado, con ortología establecida en *D. maidis* |
| 1 | Gen esencial por tamizaje en un insecto modelo (p. ej. la lista curada de *Tribolium castaneum* que usa dsRIP), con ortólogo identificable, sin datos en hemípteros |
| 0 | Esencialidad solo postulada, o el fenotipo esperado no se relaciona con alimentación, supervivencia ni transmisión |

**Evidencia requerida y de dónde sale:** búsqueda en Europe PMC por el nombre
del gen y la especie; ortología con OrthoFinder sobre los proteomas disponibles;
anotación funcional del transcripto por BLASTX contra UniProtKB y asignación KO
en KEGG. Todo corre en una notebook.

**Lo que ya está establecido para esta especie, y sirve de calibración:** *BicC*
puntúa 4 o cerca —Dalaisón-Fuentes et al. (2022), *Pest Management Science*
78(7):3108-3116, probaron inyección **y alimentación** en hembras adultas, con
reducción del transcripto de hasta 170 veces, caída de la oviposición y
desarrollo alterado de los ovocitos `[R]`, una sola fuente. *eth* y *burs-α*
puntúan 3 —Andrada et al. (2026), *Frontiers in Insect Science* 6:1811933,
obtuvieron ~90 % y ~95 % de knockdown y supervivencia del 10 %, con n = 40 por
tratamiento, pero **solo por microinyección** de 0,25 µL a 500 ng/µL `[R]`.

**C1b — Calidad de la secuencia del disparador.**

| Puntaje | Ancla |
| --- | --- |
| 4 | Largo entre 185 y 675 pb, apunta al ORF, y el score de features de siRNA está en el cuartil superior de la distribución de ventanas posibles del mismo transcripto |
| 3 | Cumple largo y ORF, score en el segundo cuartil |
| 2 | Cumple largo y ORF, score sin calcular todavía **(P)**, o score en el tercer cuartil |
| 1 | Apunta a UTR, o largo fuera del rango documentado |
| 0 | El disparador cae sobre una familia de ARN no codificante conservada (detectada en Rfam), o sobre una región repetida |

**Evidencia requerida:** las cuatro features que resultaron significativas en
Cedden et al. (2025), *BMC Biology* 23(1):114 —asimetría termodinámica, energía
de autoplegado de la hebra antisentido, contenido GC en las posiciones 9 a 14 de
la antisentido, y adenina en la posición 10—, calculadas sobre todos los siRNA
derivables del disparador `[E]` para *T. castaneum*, `[?]` en cuanto a su
transferencia a hemípteros, que es una limitación que los propios autores
señalan. El GC **alto** en 9–14 se asocia a mayor eficacia, al revés de lo que
indican los datos humanos, y la accesibilidad del mRNA **no** resultó
significativa (P = 0,41), lo que vale consignar porque contradice la práctica
heredada de si-Fi. Apuntar al ORF superó a apuntar a las UTR con una razón de
riesgo de 9,91 (P = 0,011). El rango de 185 a 675 pb viene de Nitnavare et al.
(2021), *Frontiers in Plant Science* 12:673576 `[R]`. Se calcula con ViennaRNA
(`RNAfold`, `RNAplfold`) y un script propio; el tamizaje de Rfam con búsqueda
por secuencia. Todo local.

### C2 — Especificidad en el objetivo y ausencia de off-target en el maíz · peso 15

| Puntaje | Ancla |
| --- | --- |
| 4 | Cero siRNA con ≥19 nt complementarios en el transcriptoma de *Z. mays*, y en *D. maidis* los hits se concentran en el gen blanco y su familia |
| 3 | Cero hits en maíz con 0 mismatches; algún hit con 1 mismatch en genes no esenciales del maíz |
| 2 | Tamizaje no corrido todavía **(P)**, con los insumos disponibles |
| 1 | Hits en maíz en genes no esenciales, o dispersión del disparador sobre varios genes no relacionados de *D. maidis* |
| 0 | Hits con 0 mismatches en genes esenciales del maíz — además dispara G2 |

**Evidencia requerida:** Bowtie 1 de los siRNA derivables contra (a) el
transcriptoma de *Z. mays* de Ensembl Plants, descargable del FTP verificado, y
(b) los 56.116 transcriptos de *D. maidis* del TSA `GITV00000000` (Xu et al.
2021, *Microbiology Spectrum* 9:e00612-21, 82,4 % de completitud BUSCO) `[E]`.
Permitir 0, 1 y 2 mismatches y reportar los tres. Es exactamente el método que
usan dsRIP y si-Fi internamente, y corre en minutos en una notebook. **Este es
el criterio más barato de medir y, como muestra la sección 7, el que más mueve
el orden: se mide primero.** La ficha declara con qué criterio se puntuó: el
umbral de 19 nt complementarios de Cedden (2026) o el conjunto de reglas de la
EFSA (2025) descrito en G2. No son intercambiables y la diferencia no es
cosmética: el criterio de la EFSA tolera mismatches y huecos, así que devuelve
un superconjunto de los hits del umbral de 19 nt. Un 4 en C2 obtenido con el
umbral de 19 nt y un 4 obtenido con las reglas de la EFSA no son el mismo
resultado, y el candidato que pasa el segundo es el que tiene argumento
regulatorio. Además, la EFSA indica que la discusión del riesgo se base en
**cuántos ARN pequeños distintos coinciden con el mismo transcripto**, porque la
probabilidad de represión correlaciona con ese número, y que los transcriptos
con múltiples coincidencias sean el foco del análisis `[E]`: eso es un conteo
que nuestro tamizaje ya produce y que conviene reportar explícitamente en vez de
colapsarlo en un sí o un no.

### C3 — Riesgo para organismos no objetivo y ambiente · peso 15

| Puntaje | Ancla |
| --- | --- |
| 4 | Cero hits de ≥19 nt en los nueve taxones representativos del agroecosistema de maíz y en polinizadores, con el tamizaje documentado y los taxones sin transcriptoma declarados como vacío de datos |
| 3 | Cero hits en polinizadores y en enemigos naturales; algún hit en un taxón de relevancia menor o con 2 mismatches |
| 2 | Tamizaje no corrido todavía **(P)**, o corrido contra una selección parcial de taxones |
| 1 | Hits en un enemigo natural o polinizador, sin evidencia de efecto fenotípico |
| 0 | Hits con 0 mismatches en genes esenciales de *A. mellifera*, o el candidato apunta a un gen conservado en el filo — además dispara G2 |

**Evidencia requerida:** tamizaje contra transcriptomas de especies no objetivo.
Dos fuentes de la lista de especies, ambas verificadas y ambas defendibles ante
un jurado. Primera: los grupos que dsRIP ofrece —paquete recomendado,
polinizadores, enemigos naturales, microorganismos, mamíferos, plantas y
organismos modelo. Segunda, y es la que recomendamos citar porque es regional:
los **nueve taxones** que Ahmad et al. (2016), *Transgenic Research* 25:1-17,
encontraron presentes en al menos dos regiones y cuatro sitios sobre 14 sitios
de campo en Estados Unidos, Argentina y Brasil —áfido, tijereta depredadora,
crisopa, vaquita, chicharrita, chinche pirata, avispa parasitoide, escarabajo de
la savia y araña— con datos que declaran "readily transportable for use in risk
assessment between these geographic regions" `[R]`. Hay que decir al citarlo que
los autores son de Monsanto y el trabajo fue financiado por Monsanto. Los
criterios de selección de especies de prueba se toman de Romeis y Widmer (2020),
*Frontiers in Plant Science* 11:679: sensibilidad —"species closely related to
the target organism are more likely to be susceptible"—, relevancia
—"representative of valued taxa or functional groups that are most likely to be
exposed"— y disponibilidad práctica del material biológico `[E]`.

**Advertencia que va escrita en la ficha:** para la mayoría de esos nueve
taxones no hay transcriptoma público de buena calidad. Un 4 en este criterio es,
en la práctica, "no encontramos riesgo donde pudimos mirar", y la ficha tiene
que declarar dónde no se pudo mirar. Esa declaración es parte del puntaje.

### C4 — Viabilidad de la vía de entrega · peso 20

Este criterio tiene el peso más alto empatado con C1 porque el organizador
declara que la barrera del problema es la entrega y no el diseño: "las RNasas
limitan la entrega oral del ARN".

| Puntaje | Ancla |
| --- | --- |
| 4 | Vía agronómicamente aplicable (pulverización o absorción por la planta) con eficacia demostrada en *D. maidis* o en un cicadélido cercano, publicada |
| 3 | Vía aplicable, con una estrategia explícita y respaldada para contrarrestar las dsRNasas (co-entrega de dsRNA anti-dsRNasa, nanovehículo, formulación protegida), sin eficacia demostrada todavía en esta especie |
| 2 | Eficacia demostrada por alimentación en dieta artificial, sin paso a planta ni formulación |
| 1 | Solo por inyección, o requiere planta transgénica, lo que mueve el proyecto a un plazo y un marco regulatorio distintos |
| 0 | No hay vía de entrega identificada para el compartimento donde está el blanco |

**Evidencia requerida:** Dalaisón-Fuentes et al. (2023), *Pesticide Biochemistry
and Physiology* 196:105618, identifican **tres dsRNasas** en *D. maidis*, con
*Dmai-dsRNase-2* la más expresada en intestino medio y glándulas salivales,
muestran degradación rápida del dsRNA por homogenatos de tejido en un ensayo
*ex vivo*, y demuestran que **silenciar *Dmai-dsRNase-2* mejora la respuesta** al
dsRNA del gen de interés; proponen la co-entrega `[R]`. El contexto de orden es
`[E]`: Nitnavare et al. (2021) reportan que los coleópteros muestran
"maximum response", los hemípteros son "relatively inefficient" por degradación
en el intestino medio y menor capacidad de penetración, lo que "requires a high
dosage of dsRNA to compensate for the degradation". Zielińska (2026), *Journal of
Plant Protection Research* 66(3):303-317, revisa las alternativas de entrega
—HIGS, SIGS, nanovehículos, formulaciones biodegradables, expresión
transplastómica— para hemípteros `[E]`.

**Nota de aplicación para los candidatos del EPILAB:** el esquema oficial del
organizador es pulverización sobre la planta. Un candidato cuya única evidencia
sea por inyección puntúa 1 acá por definición, por bueno que sea su diseño. Esa
es la asimetría que esta rúbrica existe para hacer visible.

### C5 — Factibilidad técnica y de costo · peso 10

| Puntaje | Ancla |
| --- | --- |
| 4 | Todo lo que falta para avanzar lo podemos hacer nosotros con datos públicos y una notebook |
| 3 | Requiere síntesis de dsRNA y un bioensayo de alimentación estándar, que un laboratorio asociado puede correr en semanas |
| 2 | Requiere un bioensayo con planta o cría de insectos, y por lo tanto un convenio |
| 1 | Requiere capacidad de formulación o nanoencapsulado, o transformación de planta |
| 0 | Requiere infraestructura que no existe en el país o una escala fuera de alcance |

**Evidencia requerida:** la vía institucional concreta, no una estimación. INTA
publica sus instrumentos de vinculación tecnológica —convenios con empresas,
licencia de tecnologías, **asistencia técnica a terceros**, Empresas de Base
Tecnológica con INCUINTA como plataforma de biotecnología, Nodos de Innovación—
y una vía de entrada para terceros por "Banco de ideas", con base pública de
convenios en `sigec.inta.gov.ar` `[R]`. Para síntesis de ARN existe capacidad
local: CONICET informa que Apolo Biotech, Empresa de Base Tecnológica fundada
por Federico Ariel (IFIBYNE, CONICET-UBA), inauguró en Santa Fe la primera planta
de producción de ARN de América Latina `[R]`; la misma nota **no** vincula a esa
empresa con la chicharrita ni menciona RNAi, y eso hay que decirlo al usarlo.

### C6 — Reproducibilidad · peso 10

G3 ya exige que el puntaje se pueda regenerar. Este criterio puntúa cuánto del
**candidato**, no de nuestro cálculo, es reproducible por un tercero.

| Puntaje | Ancla |
| --- | --- |
| 4 | Secuencia con accesión pública, insumos con licencia que permite reuso, entorno declarado con versiones fijas, semillas fijadas, y el puntaje se regenera con un comando |
| 3 | Lo mismo, pero algún insumo tiene licencia restrictiva (p. ej. no comercial) o requiere registro |
| 2 | La secuencia es reproducible pero algún paso depende de una herramienta web sin versión declarada o sin salida exportable |
| 1 | Depende de un dato no publicado o de una herramienta que no corre en nuestra plataforma |
| 0 | No se puede reconstruir de dónde salió el candidato |

**Evidencia requerida y las trampas concretas de este proyecto.** Tres están
verificadas y hay que puntuarlas, no lamentarlas. Primera: el ensamblado del
INTA está bajo **CC BY-NC-SA**, o sea no comercial, lo que baja a 3 cualquier
candidato derivado de él si después se pretende licenciar `[R]`; el preprint del
borrador está bajo CC BY-NC-ND 4.0 `[R]`. Segunda: **si-Fi corre solo en Windows
7 o superior**, con interfaz en Python 2.7 y Qt4 (Lück et al. 2019) `[E]`, así
que un pipeline que dependa de él no es reproducible en las máquinas del equipo;
la salida es reimplementar sus reglas con ViennaRNA y Bowtie, que es lo que el
propio paper describe. Tercera: **dsRIP es una herramienta web** y su salida hay
que exportarla y versionarla, o el puntaje no se puede rehacer. Las anclas de 4
se sostienen con Snakemake —que declara el software requerido y lo despliega
desde Conda-Forge y Bioconda, y genera reportes portables que combinan
resultados, parámetros, código y software (Mölder et al. 2021, *F1000Research*
10:33) `[E]`; con Bioconda (Grüning et al. 2018, *Nature Methods*
15(7):475-476, doi 10.1038/s41592-018-0046-7) para fijar versiones —de esta
última verificamos el registro bibliográfico en Europe PMC, no el texto
completo—; con
DVC para versionar los datos por hash fuera de git; y con el flujo de
GitHub-Zenodo para que la versión del cálculo tenga DOI.

### C7 — Viabilidad regulatoria · peso 5

| Puntaje | Ancla |
| --- | --- |
| 4 | La clase de producto tiene precedente de registro para aplicación foliar sobre un cultivo alimenticio |
| 3 | Precedente en otra jurisdicción, con datos que podrían ser transportables |
| 2 | Clase de producto sin precedente pero sin obstáculo identificado |
| 1 | Requiere marco de organismo genéticamente modificado (planta transgénica) |
| 0 | Obstáculo regulatorio identificado y sin vía de resolución |

**Evidencia requerida:** el precedente existe y es citable. La EPA registró el
22 de diciembre de 2023 el ingrediente activo **ledprona**, un dsRNA
pulverizable contra el escarabajo de la papa de Colorado que silencia el gen de
la proteína **PSMB5**, por un plazo de **tres años**, describiéndolo como "the
first sprayable dsRNA pesticide in the world allowed to be used commercially and
sprayed on plants", sin riesgo de preocupación para la salud humana ni el
ambiente y habiendo consultado expertos internacionales a través de la OCDE;
expediente `EPA-HQ-OPP-2021-0271` `[R]`, fuente institucional primaria. Para
transportabilidad de datos de artrópodos no objetivo entre regiones, Ahmad et
al. (2016) con sus 14 sitios en Estados Unidos, Argentina y Brasil `[R]`.

**Actualización del 2026-10-17.** La guía de la EFSA, que en la v1.0 figuraba
como pendiente, se abrió y está citada en G2: *Risk assessment considerations for
RNAi-based genetically modified plants*, aprobada el 7 de marzo de 2025,
doi 10.2903/j.efsa.2025.9321 `[E]`. Dos consecuencias para este criterio.
Primera, el precedente de registro ya no es uno solo: una perspectiva en *Pest
Management Science* (2026, doi 10.1002/ps.70806, acceso abierto) consigna que
ledprona quedó registrada como bioplaguicida con el número EPA 94614-2, que un
producto de dsRNA contra el ácaro *Varroa* —vadescana— también llegó a
comercialización, y que se presentó un expediente en Estados Unidos, la Unión
Europea y **Brasil** para un ingrediente activo de dsRNA contra *Erysiphe
necator* `[R]`. Un expediente presentado en Brasil mueve el ancla de 3 a algo
más cercano a 4 para la clase de producto en la región, y conviene decirlo en la
ficha. Segunda, el mismo trabajo ubica el marco de HIGS como organismo
genéticamente modificado evaluado por la CTNBio en Brasil `[R]`, lo que respalda
el ancla de 1 para candidatos que requieran planta transgénica. Sigue pendiente,
y es pregunta para el investigador, el marco argentino (SENASA, CONABIA) `[?]`.

### C8 — Tiempo hasta demostración · peso 5

| Puntaje | Ancla |
| --- | --- |
| 4 | Se puede demostrar algo verificable dentro del plazo del evento, con datos públicos |
| 3 | Semanas: síntesis más un bioensayo de alimentación |
| 2 | Meses: bioensayo con planta |
| 1 | Más de un año: campo o planta transgénica |
| 0 | Sin camino de demostración definido |

**Evidencia requerida:** el plan de la rama correspondiente en `PLAN_EQUIPO.md`,
con las horas-persona asignadas. Un 4 acá no premia ser ambicioso: premia que
exista una afirmación falsable que el equipo pueda cerrar con lo que tiene.

## 4. Pesos y su justificación

| Criterio | Peso | Por qué ese peso |
| --- | --- | --- |
| C1 Probabilidad de acción biológica | 20 | Es el núcleo de la pregunta del track ("mayor probabilidad de acción") |
| C2 Especificidad y off-target en maíz | 15 | La pregunta del track nombra al maíz como primer sujeto a no dañar |
| C3 Riesgo no objetivo y ambiente | 15 | La pregunta del track nombra organismos no objetivo y ecosistema |
| C4 Viabilidad de la vía de entrega | 20 | El organizador declara que la barrera del problema son las RNasas, no el diseño |
| C5 Factibilidad técnica y de costo | 10 | Decide si el candidato es accionable para este equipo, sin laboratorio |
| C6 Reproducibilidad | 10 | La pregunta del track pide soluciones reproducibles, con esa palabra |
| C7 Viabilidad regulatoria | 5 | Importa, pero es poco discriminante entre candidatos de la misma clase |
| C8 Tiempo hasta demostración | 5 | Igual: discrimina poco dentro de una misma clase de entrega |

Los pesos son una decisión del equipo, no un hecho, y están marcados `[H]`. La
regla de uso es que **se declaran antes de puntuar** y que cualquier cambio
posterior se reporta junto con su efecto sobre el orden (sección 5.4). Esto es lo
que distingue una priorización de una racionalización.

## 5. Cómo se combina

### 5.1 Fórmula

Con `s_i` el puntaje de 0 a 4 del criterio `i` y `w_i` su peso:

```
Total = ( Σ w_i · s_i ) / 4        →  escala 0 a 100
```

La división por 4 solo reescala: con todos los criterios en 4 el total es 100.

### 5.2 Topes, para que ningún criterio se compense con otro

Un promedio ponderado puro deja que un diseño de secuencia brillante tape la
ausencia de vía de entrega. Eso es exactamente el error que esta rúbrica tiene
que evitar, así que:

- **Cualquier criterio en 0 topea el total en 40** y el candidato se reporta como
  *no priorizable sin rediseño*, con el criterio culpable nombrado.
- **Dos o más criterios en 1 entre C1, C2, C3 y C4 topean el total en 60.**
- El tope se reporta siempre junto al total sin topar, para que se vea qué lo
  causó.

### 5.3 Incertidumbre: dos puntajes, no uno

Cada criterio se puntúa y se le adosa su marcador de evidencia. Los criterios
marcados **(P)** —dato producible por nosotros pero todavía no producido— se
resuelven de dos maneras y se reportan las dos:

- **Puntaje conservador:** los (P) se puntúan en 1.
- **Puntaje optimista:** los (P) se puntúan en 4.

El orden oficial se construye con el **conservador**, porque es el que no
promete. La distancia entre los dos órdenes es información de primera: dice qué
medición hay que hacer antes de decidir.

### 5.4 Análisis de sensibilidad, obligatorio

Se reportan tres cosas, siempre:

1. El orden con los pesos declarados.
2. El orden con un esquema alternativo justificado. El que recomendamos usar
   como alternativo es **C4 a 30 y C1 a 10**, que es la lectura más literal de la
   declaración del organizador sobre que la barrera es la entrega.
3. **Cuál es la medición de menor costo que más cambia el orden.** Esta es la
   salida más valiosa de la rúbrica y es la que convierte un ranking en una
   decisión científica.

## 6. Ficha de decisión: el entregable por candidato

Una por candidato, de una carilla, generada por la herramienta y no a mano.

```
CANDIDATO: <id> — <gen_blanco> en <organismo_blanco>
Vía de entrega propuesta: <...>
Compuertas: G0 pasa | G1 pasa | G2 pasa/rediseño (detalle) | G3 pasa

CRITERIO                      PUNTAJE  MARCADOR  (P)  EVIDENCIA (fuente)
C1  acción biológica            x.x      [ ]      [ ]  ...
  C1a evidencia del blanco      x        [ ]      [ ]  ...
  C1b calidad de secuencia      x        [ ]      [ ]  ...
C2  especificidad / maíz        x        [ ]      [ ]  ...
C3  no objetivo / ambiente      x        [ ]      [ ]  ...
C4  vía de entrega              x        [ ]      [ ]  ...
C5  factibilidad y costo        x        [ ]      [ ]  ...
C6  reproducibilidad            x        [ ]      [ ]  ...
C7  regulatorio                 x        [ ]      [ ]  ...
C8  tiempo a demostración       x        [ ]      [ ]  ...

TOTAL conservador: xx,x / 100    TOTAL optimista: xx,x / 100
Tope aplicado: <no | sí, por C_>   Total sin topar: xx,x
DÓNDE NO PUDIMOS MIRAR: <taxones sin transcriptoma, datos faltantes>
QUÉ MEDICIÓN CAMBIARÍA ESTE PUNTAJE: <la más barata primero>
VERSIÓN: rúbrica v1.0 | datos <hash> | código <commit> | fecha
```

## 7. Ejemplo trabajado

Cinco candidatos construidos por nosotros a partir de blancos con evidencia
publicada y verificada, para mostrar que la rúbrica corre hoy. **No son los
candidatos del EPILAB**, que no conocemos: son nuestros, y los puntajes son
`[H]`, aplicación nuestra de la rúbrica sobre evidencia `[E]` y `[R]` citada en
la sección 3.

| id | Candidato |
| --- | --- |
| K1 | dsRNA anti-*Dmai-dsRNase-2* co-entregado con dsRNA anti-*BicC*, pulverización foliar |
| K2 | dsRNA anti-*BicC* solo, entrega oral en dieta y luego foliar |
| K3 | dsRNA anti-*eth*, el blanco con mejor fenotipo publicado en la especie |
| K4 | dsRNA contra un gen esencial anotado de *Spiroplasma kunkelii* (genoma completo `GCA_001274875.1`, 1.685 genes codificantes), aplicado a la planta |
| K5 | dsRNA contra el genoma de MRFV, para bloquear la transmisión dentro del insecto |

### 7.1 Puntajes

| Criterio | peso | K1 | K2 | K3 | K4 | K5 |
| --- | --- | --- | --- | --- | --- | --- |
| C1 acción biológica | 20 | 2,5 | 3,0 | 3,5 | 1,0 | 1,5 |
| C2 especificidad / maíz | 15 | 2 (P) | 2 (P) | 2 (P) | 2 (P) | 2 (P) |
| C3 no objetivo / ambiente | 15 | 2 (P) | 2 (P) | 2 (P) | 3 | 3 |
| C4 vía de entrega | 20 | 3 | 2 | **0** | 1 | 1 |
| C5 factibilidad y costo | 10 | 2 | 3 | 3 | 2 | 2 |
| C6 reproducibilidad | 10 | 3 | 3 | 3 | 3 | 3 |
| C7 regulatorio | 5 | 2 | 2 | 1 | 1 | 1 |
| C8 tiempo a demostración | 5 | 2 | 3 | 3 | 1 | 1 |
| **Total (conservador aplicado a (P) = 1)** | | **52,5** | **53,8** | **40,0** (topado; 45,0 sin topar) | **40,0** | **42,5** |
| **Total con (P) = 2, como está arriba** | | 60,0 | 61,3 | 40,0 (topado; 52,5 sin topar) | 43,8 | 46,3 |
| **Total optimista ((P) = 4)** | | 75,0 | 76,3 | 40,0 (topado; 67,5 sin topar) | 51,3 | 53,8 |

**Corrección de la v1.0, hecha el 2026-10-17 al recalcular la tabla con la fórmula
de la sección 5.1.** La fila conservadora de la v1.0 traía dos valores mal: K4
decía 43,8 y K5 decía 46,3, que son los totales con (P) = 2 y no con (P) = 1. Los
valores correctos son 40,0 y 42,5. La corrección **cambia el orden oficial**: con
los puntajes conservadores K5 queda en 42,5 y K4 cae a 40,0, empatado con el
tope de K3. Se deja escrito el error porque es exactamente la clase de falla que
la compuerta G3 existe para atrapar: un puntaje que no se regenera desde la
ficha con un comando es un puntaje que nadie audita. El ejemplo de esta sección
se recalculó íntegro y los totales de arriba son los que devuelve la fórmula.

Razones de los puntajes que más deciden, en una línea cada uno:

- **K3 recibe 0 en C4** porque toda su evidencia es por microinyección (Andrada
  et al. 2026), y la inyección no es una vía de aplicación agronómica. Por eso se
  topea en 40 pese a tener el mejor C1 de los cinco: su total sin topar sería
  52,5. Es el resultado más instructivo del ejemplo, porque **el candidato con el
  mejor fenotipo publicado es el que peor prioriza**, y la rúbrica lo explica en
  lugar de esconderlo.
- **K1 recibe 3 en C4** por tener una estrategia explícita y respaldada contra
  las dsRNasas, y **K2 recibe 2** porque su eficacia oral demostrada fue en
  alimentación, sin paso a planta ni formulación.
- **K4 y K5 reciben 1 en C1a** porque no hay evidencia de que un molicute sin
  pared ni un virus de ARN respondan a RNAi por esta vía; es la pregunta que
  queda para el investigador y está anotada en `PREGUNTAS_ABIERTAS.md`. Reciben
  3 en C3 porque un blanco procariota o viral tiene, a priori, menos
  coincidencias con artrópodos no objetivo.
- **Nota del 2026-10-17 sobre el fitoplasma, que corrige un supuesto nuestro.**
  La v1.0 daba por sentado que *Spiroplasma kunkelii* era el único patógeno del
  complejo con genoma completo y anotado. No lo es: el fitoplasma del
  achaparramiento arbustivo del maíz (*maize bushy stunt*) tiene genoma completo
  en una sola secuencia desde 2016 —`GCA_001712875.1` / `GCF_001712875.1`, cepa
  M3, 576.118 pb, 28,5 % de GC, 544 genes en la anotación original y 524 genes
  codificantes en la reanotación de RefSeq del 7 de junio de 2026, aislado de un
  ejemplar de *Dalbulus maidis* colectado el 29 de mayo de 2013 en Piracicaba,
  São Paulo, Brasil `[E]`, verificado por consulta directa a la API de NCBI
  Datasets—. Y el taxón tiene nombre propio desde 2026: '*Candidatus* Phytoplasma
  zeae' (Pellegrinetti et al., *International Journal of Systematic and
  Evolutionary Microbiology* 76(10), doi 10.1099/ijsem.0.007301) `[E]`, nombre
  que la taxonomía del NCBI ya usa para ese genoma (TaxId 202462). Consecuencia
  para la rúbrica: un candidato dirigido al fitoplasma deja de puntuar bajo en
  C5 por falta de insumo —el insumo existe, está anotado y pesa menos de un
  megabase— y lo que sigue decidiendo su puntaje es C1a, es decir si un molicute
  sin pared responde a RNAi, que sigue sin evidencia.

### 7.2 El orden y lo que hay que medir

Orden oficial, con el puntaje conservador: **K2 (53,8) > K1 (52,5) > K5 (42,5) >
K4 (40,0) = K3 (40,0, topado).**

El análisis de sensibilidad cambia la conclusión, y eso es el hallazgo:

- **Con el esquema alternativo (C4 a 30, C1 a 10)**, y con los puntajes de la
  tabla ((P) = 2), K1 pasa a 61,3 y K2 a 58,8: **el orden de los dos primeros se
  invierte.** La inversión no depende de cómo se resuelvan los (P): con el
  puntaje conservador y los pesos alternativos, K1 queda en 53,8 y K2 en 51,3, y
  el orden se invierte igual. Los dos candidatos de cabeza están separados por
  1,3 puntos sobre 100 con los pesos declarados, y el orden depende de cuánto
  peso se le dé a la barrera de entrega.
- **Los rangos conservador-optimista de K1 (52,5–75,0) y de K2 (53,8–76,3) se
  superponen casi por completo.** Con la evidencia de hoy, el orden entre los dos
  primeros **no está determinado**.
- **La medición de menor costo que más cambia el orden es C2 y C3**: el tamizaje
  de off-target con Bowtie 1 contra el transcriptoma de maíz de Ensembl Plants y
  los 56.116 transcriptos del TSA `GITV00000000`, más los taxones no objetivo.
  Son horas de cómputo en una notebook, con datos públicos, sin laboratorio y sin
  permiso. Es lo primero que hay que correr.

La decisión científica que la rúbrica produce, entonces, no es "elijan K2". Es:
**los dos candidatos de cabeza están empatados dentro de la incertidumbre, el
desempate es el tamizaje de especificidad, cuesta una tarde de cómputo, y el
candidato cuyo diseño incluye una respuesta a la barrera de las dsRNasas gana en
cuanto se pondera esa barrera como el propio organizador la pondera.** Eso es
aplicable mañana a los candidatos del EPILAB sin tocar un criterio.

## 8. Limitaciones, escritas

- Los pesos son nuestros `[H]`. La rúbrica incluye el análisis de sensibilidad
  precisamente porque los pesos son discutibles.
- Las features de eficacia de siRNA están validadas en *Tribolium castaneum*, un
  coleóptero, y su transferencia a un hemíptero es `[?]`. La propia revisión de
  Cedden (2026) marca que las predicciones de off-target "need to be
  experimentally tested" y que falta prueba fuera de coleópteros.
- C3 mide ausencia de coincidencia de secuencia, no ausencia de efecto. Romeis y
  Widmer (2020) muestran que no son lo mismo en ambas direcciones.
- La rúbrica no puntúa durabilidad frente a la evolución de resistencia en el
  vector, por falta de datos de variabilidad poblacional del sitio blanco. Queda
  como criterio candidato para la v2 y está anotado en
  `PREGUNTAS_ABIERTAS.md`.
- Un puntaje alto no autoriza nada. La compuerta G0 y el alcance ético de
  `CLAUDE.md` rigen por encima de cualquier total.
