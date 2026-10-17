# W1 — Triaje y lectura del corpus de papers del Investigathón

**Qué es esto.** El inventario y la lectura de los siete artículos que el
organizador entregó en `YHat-Biotech/Papers/`, hecho abriendo y leyendo cada PDF
completo, no su resumen. Está escrito para que los cuatro integrantes del equipo
sepan qué hay en el corpus sin abrir un solo PDF, qué de eso cambia lo que ya
habíamos escrito en la ola 1, y cuáles son los papers que hay que leer sí o sí
antes del evento.

**Alcance y profundidad.** Los siete se leyeron a fondo: métodos, tablas,
resultados, discusión y limitaciones declaradas por los autores. **Ninguno quedó
en lectura de triaje y ninguno se descartó por irrelevante.** El corpus es chico
y está curado por el organizador, así que casi todo toca algo nuestro; la
diferenciación útil no es "relevante / no relevante" sino *para qué* sirve cada
uno, y eso está en la sección 2 y en `papers.json`.

**Convención de evidencia**, la misma de `CLAUDE.md`: `[E]` establecido, `[R]`
reportado por una o pocas fuentes, `[H]` hipótesis nuestra, `[?]` incierto o con
contradicción. Toda afirmación sobre el corpus apunta al archivo y a la sección
o tabla de la que sale. Donde el corpus y nuestra ola 1 se contradicen, las dos
versiones están en `contradicciones.md` y ninguna gana por ser oficial.

---

## 1. Panorama: qué cubre el corpus y qué no

Los siete papers se reparten en tres bloques que, leídos juntos, dibujan una
cadena bastante precisa: **ARN exógeno → planta → insecto**, con un eslabón
flojo en el medio y uno ausente al final.

El primer bloque es **el insecto**. `Papers/finsc-6-1811933.pdf` (P3) es RNAi
funcional en la especie blanco, *Dalbulus maidis*, por microinyección;
`Papers/Dcitri.pdf` (P1) es entrega **oral** en otro hemíptero fitófago de
floema, *Diaphorina citri*, vector de una bacteria limitada al floema; y
`Papers/s10340-023-01670-0.pdf` (P6) es entrega **mediada por planta** a dos
cicadélidos vectores de fitoplasma. Los tres juntos cubren las tres vías de
entrega que importan y, lo que es más valioso, cubren la que falla.

El segundo bloque es **la planta**. `Papers/s12298-024-01500-2.pdf` (P7) muestra
siRNA exógeno dentro de células de maíz; `Papers/s00299-010-0911-z.pdf` (P5)
aplica ARNdc producido en bacteria a maíz contra un virus; y
`Papers/nplants2016207 (1).pdf` (P4) es el trabajo original de BioClay, que fija
el techo de persistencia que cualquier formulación tiene que superar.

El tercer bloque es **el patógeno**, y es el más engañoso.
`Papers/PLD3-4-e00224.pdf` (P2) es el único paper del corpus sobre uno de los
cuatro agentes del complejo, el *Maize rayado fino virus* (MRFV), y hay que
decir con todas las letras lo que hace y lo que no: **convierte al MRFV en una
herramienta para silenciar genes del maíz, no en un blanco de silenciamiento**
`[E]` (`PLD3-4-e00224.pdf`, Abstract y sección 3). Quien lo cite como evidencia
de que se puede silenciar al MRFV lo estará citando al revés.

**Lo que el corpus no contiene, y conviene tener claro antes de empezar.** No
hay ni un solo trabajo sobre aprendizaje automático, modelado computacional o
predicción de eficacia: el corpus es íntegramente experimental y metodológico, y
el único cálculo bioinformático que aparece en todo él es un tBLASTn para buscar
ortólogos y un BLASTn para verificar especificidad, los dos en P3
(`finsc-6-1811933.pdf`, "In silico identification" y "RNAi experiments"). No hay
nada sobre espiroplasma ni fitoplasma como blanco. No hay nada sobre el MSMV. No
hay evaluación de organismos no objetivo en ninguno de los siete. Y no está el
trabajo de dsRNasas en *D. maidis* (PubMed 37945254) que la ola 1 dejó anotado
como pendiente, aunque P3 lo cita como su referencia 44 y resume su conclusión
`[R]`.

---

## 2. Para qué sirve cada paper

No todos sirven para lo mismo y mezclarlos es el error más fácil de cometer.

**P6 — `s10340-023-01670-0.pdf` es el paper que más mueve nuestra estrategia.**
Es el único del corpus que entrega ARNdc a un cicadélido vector de fitoplasma a
través de la planta, que es exactamente nuestro problema con otro insecto. Es
también el que la ola 1 había declarado como "no se pudo abrir" en
`00_meta/PREGUNTAS_ABIERTAS.md`.

**P3 — `finsc-6-1811933.pdf` es el único dato cuantitativo en la especie
blanco** y, de paso, el único paper del corpus que describe un criterio de
diseño de ARNdc, aunque sea mínimo.

**P1 — `Dcitri.pdf` es el mejor análogo de entrega oral que existe**: hemíptero
de floema, vector de un procariota limitado al floema, dos vías orales
probadas. Y trae el resultado más incómodo del corpus, que está en la sección
4.3 de este reporte.

**P7 y P5 — `s12298-024-01500-2.pdf` y `s00299-010-0911-z.pdf` son la mitad
vegetal de la cadena**: qué entra al maíz, hasta dónde llega, cuánto dura.

**P4 — `nplants2016207 (1).pdf` es la vara de la formulación.** Su relevancia la
clasificamos como media y conviene explicar por qué: no hay maíz, no hay
insecto, no hay vector. Lo que aporta es el número que cualquier propuesta de
formulación nuestra tiene que batir, más una corrección y una advertencia que
están en `contradicciones.md`.

**P2 — `PLD3-4-e00224.pdf` es la arquitectura del MRFV**, y eso importa porque
dos de los cuatro candidatos del EPILAB apuntan al MRFV (ver sección 7).

---

## 3. La pregunta que decide todo: ¿RNAi sobre mollicutes y virus?

Esta es la pregunta que la ola 1 puso como bisagra de `R1/REPORT.md` sección 4 y
la que el prompt nos pide responder explícitamente. La respuesta, con lo que el
corpus permite, es ésta.

### 3.1 Sobre mollicutes el corpus no dice nada, y ese silencio es informativo

**Ningún paper del corpus propone, intenta o discute silenciar un gen de un
fitoplasma o de un espiroplasma** `[E]`. No es que lo intenten y falle: es que
no aparece la idea. P6 trabaja con los dos vectores europeos de la flavescencia
dorada y, teniendo el fitoplasma en el sistema, dirige los tres ARNdc a **genes
del insecto** —ATP sintasa beta, legumaína y naterina—
(`s10340-023-01670-0.pdf`, "Synthesis of dsRNAs"). P1 trabaja con el vector del
huanglongbing y dirige los tres ARNdc a **genes del psílido** —cathepsin D,
chitin synthase e inhibitor of apoptosis— (`Dcitri.pdf`, "Identification, primer
design and amplification of target genes"), aunque el patógeno, *Candidatus*
Liberibacter, sea también una bacteria limitada al floema.

Esto es importante y hay que decirlo con precisión: **el corpus no demuestra que
no se pueda; confirma que nadie de los que trabajan en este problema lo
intenta**, y lo hace en dos sistemas independientes con dos procariotas
distintos. Es exactamente lo que la verificación propia de la ola 1 sobre
126.874 proteínas de mollicutes predecía, y es la segunda confirmación
independiente del mismo punto. Para el circuito de cuatro pasos de la
diapositiva del organizador, que termina en "inhibición del crecimiento del
patógeno", el corpus no aporta ninguna lectura directa: la pregunta 1 de
`00_meta/PREGUNTAS_ABIERTAS.md` sigue abierta y **sigue siendo la primera que
hay que hacerle al investigador** `[?]`.

Lo que el corpus sí aporta es la alternativa, y la aporta con un gen concreto.
P6 eligió la ATP sintasa beta precisamente por estar "involucrada en la
transmisión del fitoplasma" `[E]` (`s10340-023-01670-0.pdf`, "Synthesis of
dsRNAs"), y la silenció significativamente en las dos especies por vía de planta
(figura 6 y tabla S5). Es decir: el corpus respalda la **vía 2** que la ola 1
había ordenado en segundo lugar —silenciar genes del vector que el patógeno
necesita— y le pone una vía de entrega encima.

### 3.2 Sobre virus el corpus dice bastante, y nada sobre los nuestros

Hay dos papers de ARN exógeno contra un virus de maíz, y los dos funcionan.
P5 protegió maíz contra el *Sugarcane mosaic virus* con lisado bacteriano crudo
`[E]` (`s00299-010-0911-z.pdf`, tablas 2 y 3) y P7 redujo la carga de *Maize
dwarf mosaic virus* en maíz dulce con un siRNA de 21 nt `[E]`
(`s12298-024-01500-2.pdf`, figura 6). P4 hizo lo propio con CMV y PMMoV en
tabaco y caupí `[E]` (`nplants2016207 (1).pdf`, figuras 4 y 5).

**Pero ninguno de esos virus es del complejo del achaparramiento.** El SCMV y el
MDMV son potyvirus de maíz transmitidos por pulgones; el CMV y el PMMoV no
infectan maíz. El hueco que la ola 1 documentó —cero trabajos de ARNdc, SIGS o
HIGS contra MRFV y contra MSMV— **el corpus no lo llena** `[?]`. Lo que sí hace
es demostrar que el maíz es un hospedador competente para esta tecnología, que
es un prerrequisito distinto y necesario.

### 3.3 Dónde para realmente el ARN exógeno dentro de la planta

Éste es el hallazgo transversal más importante del corpus y no está enunciado
como tal en ningún paper individual: hay que leer tres en paralelo para verlo.

- P6: el ARNdc aplicado al peciolo o a la hoja cortada "permanece restringido al
  xilema y al apoplasto", y los cicadélidos lo adquieren **no porque llegue al
  floema sino porque los fitófagos de floema también sondean xilema**, según
  datos de electropenetrografía `[E]` (`s10340-023-01670-0.pdf`, Introducción y
  Discusión). Entre las referencias que sostienen ese punto está Carpane et al.
  2011, que es electropenetrografía **de la chicharrita del maíz** `[R]`.
- P7: la señal de ALEXA488 apareció dentro de células parenquimáticas de la
  vaina del haz, y "no se halló señal fluorescente dentro de la tráquea ni del
  floema" `[E]` (`s12298-024-01500-2.pdf`, "Detection of fluorophore-labelled
  siRNA").
- P4: la captación del fluoróforo se observó "en el xilema" y en el mesófilo
  esponjoso `[R]` (`nplants2016207 (1).pdf`, sección de captación y
  Supplementary Fig. 3).

Tres sistemas distintos, tres técnicas distintas, la misma conclusión: **el ARN
exógeno entra al apoplasto y al xilema y no hay evidencia de que entre al
floema** `[E]`. Para nosotros esto reordena la cuestión de la entrega. *D.
maidis* es un fitófago de floema, y la hipótesis de trabajo que el corpus
habilita no es "que el ARNdc viaje por el floema hasta el estilete" sino "que el
insecto lo tome durante sus episodios de sondeo de xilema" `[H]`. Es una
hipótesis con respaldo en P6 y con un dato de electropenetrografía propio de la
especie, y es contrastable sin laboratorio revisando la literatura de EPG de *D.
maidis*. Es, además, un argumento que ningún material de la ola 1 contenía.

---

## 4. Criterios de diseño, eficacia y modos de aplicación

### 4.1 Qué criterios de diseño usan los papers: muchos menos de los que esperábamos

El hallazgo acá es negativo y es rotundo. **Ningún paper del corpus usa
asimetría termodinámica, accesibilidad estructural, selección de hebra guía ni
tamizaje contra organismos no objetivo.** El tratamiento más completo es el de
P3, y consiste en: identificar el ortólogo con tBLASTn en Galaxy Europe con
umbrales de E-value < 1×10⁻⁴ e identidad > 35 %, y después verificar la región
elegida con BLASTn **contra el transcriptoma de la propia especie**, declarando
un único acierto significativo y ninguna similitud con transcriptos no blanco
`[E]` (`finsc-6-1811933.pdf`, "In silico identification of eth and burs-a" y
"RNAi experiments", con Supplementary Table 1).

Es decir: el estado de la práctica en el grupo argentino que publica RNAi en
nuestra especie es **especificidad intraespecífica verificada con BLASTn, y nada
más**. No hay panel de no objetivo, no hay conteo de coincidencias de semilla,
no hay ventana de 21-meros, no hay termodinámica. Esto no es una crítica: es la
medida exacta del hueco que la propuesta de la ola 2 puede llenar, y confirma
desde una fuente nueva el diagnóstico de `R3/REPORT.md` sección 6.2(a) —que lo
que falta no son herramientas de diseño sino una función de decisión escrita.

Un detalle a registrar, porque es el tipo de cosa que conviene no repetir: P3
declara entre sus umbrales un "bit score > 40 %" (`finsc-6-1811933.pdf`, "In
silico identification"). El bit score no es un porcentaje, así que el criterio,
tal como está escrito, no es interpretable `[?]`.

Sobre **largo del disparador**, el corpus aporta cuatro puntos y uno de ellos
incomoda a la recomendación general:

| Paper | Disparador | Largo | Resultado |
| --- | --- | --- | --- |
| P3 | ARNdc inyectado, *D. maidis* | **578 pb** (*burs-a*) y **544 pb** (*eth*) | ~95 % y ~90 % de knockdown |
| P6 | ARNdc por hoja cortada, cicadélidos | no declarado en el texto principal | silenciamiento sin mortalidad |
| P5 | horquilla en bacteria, maíz | **147 pb** y **140 pb** de tallo | inhibición del SCMV |
| P2 | inserto en vector viral, maíz | **120 nt** y **231 nt** | el de **120 nt silenció mejor** |
| P7 | siRNA sintético, maíz | **21 nt** | cebado de la vía y menor carga viral |

Lo que sale de ahí es que la banda de 200 a 500 pb que la ola 1 recogió de la
literatura `[E]` describe bien la práctica en insectos, pero **no en planta**:
en planta funcionan horquillas de ~140 pb (P5), insertos de 120 nt (P2) y hasta
un solo siRNA de 21 nt (P7), y P2 reporta explícitamente que subir de 120 a 231
nt "no dio ganancias fenotípicas de silenciamiento" `[E]`
(`PLD3-4-e00224.pdf`, sección 4). Si nuestro método trata el largo como una
variable con un óptimo único, está asumiendo algo que el corpus desmiente: el
óptimo depende del organismo que procesa.

Sobre **región del gen**, hay un dato limpio y poco citado: en P5, el ARNdc
derivado de la región corriente arriba de la cápside del SCMV (CP1) fue más
efectivo que el de la región corriente abajo (CP2) del **mismo gen** `[E]`
(`s00299-010-0911-z.pdf`, Resultados y Discusión). Es evidencia directa de que
la región importa dentro de un mismo blanco, que es el supuesto sobre el que se
apoya toda la idea de puntuar ventanas a lo largo de un transcripto.

### 4.2 Qué datos de eficacia reportan, y con qué n

Reunidos en un solo lugar, porque es lo que hay que poder citar sin equivocarse:

| Paper | Especie | Condición | Gen | Entrega y dosis | Efecto | n |
| --- | --- | --- | --- | --- | --- | --- |
| P3 | *D. maidis* | laboratorio | *burs-a* | microinyección, 125 ng/insecto | ~95 % knockdown; **10 % de supervivencia a día 4** | 40 por tratamiento; **3 réplicas biológicas de 3 ninfas** para la qPCR |
| P3 | *D. maidis* | laboratorio | *eth* | ídem | ~90 % knockdown; **10 % de supervivencia a día 5** | ídem |
| P3 | *D. kuscheli* | laboratorio | *burs-a* / *eth* | ídem | ~95 % / 80-85 % knockdown; 17,5 % / 20 % de supervivencia | ídem |
| P1 | *D. citri* adulto | laboratorio | inhibitor of apoptosis | dieta artificial, 1000 ng/µL, 120 h | **64 % de mortalidad** | 30 por réplica, 3 réplicas |
| P1 | *D. citri* adulto | laboratorio | cathepsin D / chitin synthase | ídem | 52 % / 49 % de mortalidad | ídem |
| P1 | *D. citri* ninfa | laboratorio | los tres | foliolo cortado, 500 ng/µL, 11 días | reducción de supervivencia; knockdown 61 %, 59 % y 76 % | 5 réplicas |
| P6 | *E. variegatus* | laboratorio | legumaína / naterina | hoja cortada, 7 µg/tubo | reducción significativa a **17 y 24 dpf, no a 13** | 18 y 21 insectos, con 17 % y 33 % excluidos |
| P6 | *E. variegatus* / *S. titanus* | laboratorio | ATP sintasa beta | ídem | reducción significativa a 14 dpf | 8 y 25, con 25 % y 28 % excluidos |
| P5 | *Zea mays* | invernáculo | cápside del SCMV | lisado crudo pulverizado | 16/20 y 14/20 plantas resistentes | 20 por tratamiento |
| P7 | maíz dulce | cámara | cápside del MDMV | 300 ng en vaina foliar | pico de cápside **retrasado una semana** | 3 réplicas biológicas × 3 técnicas |
| P4 | *N. tabacum* | invernáculo | CMV 2b | BioClay, desafío a 20 días | **24 % de plantas infectadas** contra 71 % con ARNdc desnudo y 75 % con sólo LDH | 70 / 70 / 62 plantas |

Dos advertencias sobre esta tabla, y las dos cambian cómo se lee. La primera:
**los n de las mediciones moleculares son muy chicos**. El ~95 % de knockdown en
*D. maidis* descansa sobre tres réplicas biológicas de tres ninfas cada una
(`finsc-6-1811933.pdf`, "RT-qPCR analyses"), y los de P7 sobre tres réplicas
biológicas. Son suficientes para el propósito de los autores —demostrar que el
gen es esencial— y **no son suficientes como punto de calibración cuantitativo**
para un modelo nuestro. La prueba de rango V3 que `R2/PROPUESTA.md` propone
sigue siendo legítima, pero el dato contra el que se compara es más blando de lo
que su porcentaje sugiere.

La segunda: **P6 excluye del análisis estadístico a los insectos cuya expresión
quedó por encima de la media y la mediana del grupo control**, entre 17 % y 33 %
de cada grupo, atribuyéndolo a captación nula o insuficiente
(`s10340-023-01670-0.pdf`, "Statistical analysis" y tablas S4-S5). Los autores
lo declaran con transparencia y lo justifican con el dato de que el 28 % de los
intestinos no se tiñó con la solución marcadora. Pero la consecuencia operativa
hay que decirla: el silenciamiento reportado es el **del subconjunto que
efectivamente recibió el ARNdc**, no el de la población tratada. Para una
decisión de campo, que es poblacional, la magnitud relevante es la otra `[?]`.

### 4.3 El resultado más incómodo del corpus: mortalidad sin knockdown proporcional

P1 es el único paper del corpus que hace una curva de dosis con tres
concentraciones y mide las dos cosas a la vez, y el resultado es doble y
desagradable.

Primero: **el control de ARNdc-GFP a 500 y 1000 ng/µL causó mortalidad
significativamente mayor que el control de sacarosa** `[E]` (`Dcitri.pdf`,
Resultados, figuras 1B y 1C). Es decir, a esas dosis una parte de la mortalidad
no es específica de secuencia. Los autores lo atribuyen a efectos fuera de
blanco o a saturación de la vía de RNAi.

Segundo, y peor: **"no hubo correlación entre las dosis altas de ARNdc y las
reducciones en los niveles de expresión del ARNm"** `[E]` (`Dcitri.pdf`,
Discusión), mientras que la mortalidad sí escaló con la dosis. Para cathepsin D
y chitin synthase, el knockdown incluso *empeoró* al subir la dosis.

Esto confirma y endurece el punto 8 de las implicancias de `R1/REPORT.md`. La
versión de la ola 1 era "menos patógeno no es menos pérdida". La versión que el
corpus habilita es más fuerte: **en entrega oral a un hemíptero, la mortalidad y
el knockdown son dos variables que pueden moverse en direcciones distintas, y
una fracción de la mortalidad a dosis alta no es atribuible al silenciamiento**.
Cualquier función de puntuación nuestra que use mortalidad como proxy de
knockdown, o al revés, está asumiendo una relación que el único experimento del
corpus que la mide no encuentra `[E]`.

El corolario práctico para el diseño experimental es inmediato y es el tipo de
recomendación que un equipo sin laboratorio sí puede hacer: **el control
correcto no es "sin ARNdc" sino "ARNdc no relacionado a la misma concentración",
y hay que correrlo a cada dosis**. P1, P3 y P6 los tres lo hacen —con GFP los
dos primeros, con b-lactamasa el tercero— y es la única razón por la que el
efecto se puede ver.

Hay una pieza que apunta en el mismo sentido desde el lado de la planta. En P6,
el silenciamiento de los tres genes **no tuvo ningún efecto sobre la
supervivencia** de ninguna de las dos especies en la ventana del experimento
`[E]` (`s10340-023-01670-0.pdf`, Discusión), y los autores lo explican por el
recambio lento de la ATP sintasa. Knockdown confirmado, cero mortalidad. Junto
con P1 —mortalidad sin knockdown proporcional— el corpus deja las dos
disociaciones posibles documentadas, cada una en un sistema distinto.

### 4.4 Modos de aplicación: cuál funcionó y cuál no

El corpus prueba seis modos y el mapa que deja es más claro que el de cualquier
revisión:

- **Microinyección**: funciona en *D. maidis* y *D. kuscheli* con ~90-95 % de
  knockdown (P3) y es el patrón de oro de P6, con ~100 % de eficiencia de
  entrega frente al ~70 % de la alimentación `[E]`. No es aplicable a campo y
  los dos papers lo dicen.
- **Dieta artificial** (sacarosa al 15 % en sobre de parafilm): funciona en
  adultos de *D. citri*, con mortalidad dosis-dependiente y ARNdc estable en la
  solución a los 5 días `[E]` (P1). Los propios autores advierten que es
  ineficiente para ninfas porque la dieta artificial ya mata.
- **Hoja u hojuela cortada sumergida en ARNdc**: funciona en ninfas de *D.
  citri* (P1) y es la vía elegida por P6 tras comparar con planta entera, porque
  **sube la eficiencia de entrega de 40 % a cerca de 80 %** al concentrar el
  ARNdc en menos tejido `[E]` (`s10340-023-01670-0.pdf`, Discusión).
- **Absorción por peciolo en planta entera**: entrega, pero diluido. En el
  ensayo piloto de P6 el dsGFP se detectó en 2 de 5 insectos y con señal débil
  `[R]`.
- **Inmersión de ninfas en ARNdc con lipofectamina al 13 %**: **no funcionó.**
  La expresión de ATP sintasa beta en el grupo tratado fue 0,561 ± 0,036 (n=48)
  contra 0,414 ± 0,025 (n=21) del control de dsGFP, es decir **más alta que el
  control** `[E]` (`s10340-023-01670-0.pdf`, tabla 1). Los autores no pudieron
  determinar si falló la entrega o si el ARNdc se degradó, y abandonaron la vía.
  Es un resultado negativo publicado y vale como tal: la misma técnica había
  funcionado en *D. citri* y en *Aedes aegypti* según las referencias que ellos
  mismos citan, de modo que **la transferencia de un método de entrega entre
  especies de hemípteros no está garantizada** `[E]`.
- **Pulverización foliar de lisado bacteriano crudo**: funciona en maíz contra
  un virus, de manera **preventiva** (P5).

Para el maíz específicamente, P7 agrega una variable de diseño que no
habíamos considerado: **el sitio de aplicación**. Aplicaron en la vaina foliar
abierta de una planta de diez días, justamente porque ahí las paredes celulares
son flexibles y la cutícula delgada `[R]` (`s12298-024-01500-2.pdf`,
Introducción). El mismo paper enumera las barreras de la captación foliar
—cutícula, pared celular y nucleasas— y dice que el ARNdc no las atraviesa solo,
sino con herida, pulverización a alta presión o inundación de estomas abaxiales
`[E]`. Dicho de otro modo: cuando un paper reporta captación foliar, hay que
mirar **cómo** forzó la entrada antes de generalizar.

### 4.5 Evaluación de organismos no objetivo: cero

**Ninguno de los siete papers evalúa un organismo no objetivo.** Ni un
polinizador, ni un enemigo natural, ni fauna del suelo, ni un análisis *in
silico* de homología contra otra especie. El único control de especificidad que
aparece en todo el corpus es intraespecífico: el BLASTn de P3 contra el
transcriptoma de *D. maidis* y de *D. kuscheli*, y los controles de secuencia no
relacionada (GFP, b-lactamasa, PMMoVIR54 usado como control no específico frente
a CMV en P4).

Esto confirma, desde el material oficial, el diagnóstico de `R5/RUBRICA.md`
sobre el criterio C3 y el de `R3/REPORT.md` sección 6.2(d): **el riesgo no
objetivo es un hueco de la práctica publicada, no sólo de nuestra información**.
Es, probablemente, el argumento más fuerte que tenemos para justificar que un
equipo de bioinformática aporte algo que el laboratorio no está produciendo.

---

## 5. Aprendizaje automático y modelado computacional en el corpus

**No hay.** El manifiesto lo anticipaba y la lectura lo confirma: cero modelos,
cero predictores, cero aprendizaje automático, cero código. El cómputo total del
corpus es BLAST para homología (P2, P3), Primer3Plus y Primer-BLAST para
cebadores (P1, P3, P7), MAFFT y BEAST para alineamiento y filogenia (P3),
ImageJ y LAS X para imagen (P6, P7), GraphPad Prism, SigmaPlot y R para
estadística, y el alineador SCRAM para siRNA-seq en P4, cuyo código está
publicado en GitHub `[R]` (`nplants2016207 (1).pdf`, Data availability).

La lectura estratégica es la que `R2/REPORT.md` ya había adelantado por otra
vía: en este problema **no hay competencia metodológica del lado del modelado**.
El hueco es real. Y el corpus agrega un matiz que conviene tener presente al
presentar: el laboratorio que publica en nuestra especie no usa herramientas de
diseño de ARNdc, usa BLASTn. Una propuesta que proponga saltar de ahí a un
modelo de lenguaje de ARN se va a leer como dos escalones de más; una que
proponga el primer escalón bien hecho y auditable, no.

---

## 6. Lo que el corpus cierra de `00_meta/PREGUNTAS_ABIERTAS.md`

- **Cerrada: evidencia primaria de RNAi en cicadélidos vectores de fitoplasmas.**
  Era el pendiente de R5 que quedó tras un rechazo de herramienta registrado y
  no reformulado. P6 lo responde: RNAi funciona en *Euscelidius variegatus* y
  *Scaphoideus titanus*, por inyección y por planta.
- **Cerrada: el original de BioClay.** La ola 1 lo citaba a través de una
  revisión y `R3/panorama_industria.md` marcaba "paper no abierto". Está abierto
  y verificado; ver `contradicciones.md`, punto 1.
- **Cerrada: el original de ARNdc bacteriano en maíz.** Ídem; ver
  `contradicciones.md`, punto 2.
- **Cerrada: el RNAi experimental en *D. maidis* de Frontiers in Insect
  Science.** R4 lo tenía como "falta verificar en texto completo". Verificado:
  los números de `R1/REPORT.md` S15 son correctos salvo una atribución entre
  especies; ver `contradicciones.md`, punto 4.
- **Sigue abierta: el trabajo de dsRNasas (PubMed 37945254).** No está en el
  corpus. P3 lo cita como referencia 44 y resume su conclusión —que silenciar
  dsRNasas mejora la respuesta de RNAi tras entrega oral en *D. maidis*
  (`finsc-6-1811933.pdf`, Discusión)—, de modo que ahora tenemos la afirmación
  en segunda mano desde **el mismo grupo autor**, no desde el índice de PubMed.
  Sube de `[R]` débil a `[R]` sólido, y sigue siendo la petición número uno al
  investigador.
- **Sigue abierta: pérdidas económicas en Brasil.** P3 cita el trabajo que no
  pudimos abrir —Oliveira, Pereira, Mouro y Canale, *Crop Protection* 202:107549
  (2026), sobre pérdidas de cosecha e impacto económico del complejo en Brasil—
  como su referencia 31 (`finsc-6-1811933.pdf`, Introducción). Confirma que
  existe y qué mide; no lo abrimos, así que no aporta cifra.
- **Sigue abierta y sin tocar: la magnitud de la epifitia argentina 2023/24, el
  modo de transmisión del MSMV, y la identidad taxonómica del MSMV.** El corpus
  no las menciona.

---

## 7. Un dato del corpus que afecta directamente a los candidatos del EPILAB

Esto excede el encargo estricto de W1 y lo dejamos anotado porque W5 lo necesita
y porque sale de un paper que sólo nosotros leímos.

Según el manifiesto, dos de los cuatro candidatos del EPILAB son genes del MRFV:
`MP_MRFV`, rotulado *Movement Protein*, de 1.263 nt, y `CP_MRFV`, rotulado
*Capsid Protein*, de 528 nt. P2 describe la organización genómica del MRFV con
detalle: genoma monopartito de **6.337 nt**, una poliproteína precursora que se
procesa en metiltransferasa, proteasa tipo papaína, helicasa y polimerasa, más
**dos proteínas de cápside carboxi-coterminales, CP1 y CP2**, donde CP1 se
escinde de la poliproteína y CP2 se expresa desde un ARN subgenómico dirigido
por la *marafibox*; y un ORF pequeño de 5' que codifica una proteína P43 de
función desconocida `[E]` (`PLD3-4-e00224.pdf`, Introducción y figura 1).

**En esa descripción no figura ninguna proteína de movimiento.** El esquema
genómico de la figura 1 no nombra un gen de movimiento, y el único ORF accesorio
que el paper identifica es el P43, que además declara **no requerido para el
movimiento sistémico ni para la transmisión por cicadélidos** `[R]`
(`PLD3-4-e00224.pdf`, Introducción). De modo que queda una pregunta concreta y
de alto valor para el investigador: **¿a qué región del genoma del MRFV
corresponde el candidato `MP_MRFV` de 1.263 nt, si el genoma anotado del MRFV no
declara una proteína de movimiento?** `[?]` Puede ser una anotación por homología
con los tymovirus, que sí tienen una proteína de movimiento; puede ser una de
las regiones de la replicasa; o puede ser un rótulo heredado. No lo resolvemos
acá, y no conviene darlo por obvio.

El mismo paper deja dos datos duros que W5 va a querer. Uno: **la unión
helicasa/polimerasa es el único sitio del genoma del MRFV que tolera una
inserción**; el 3'UTR, la unión POL/CP1 y el inicio de la poliproteína son
letales `[E]`. Dos: la eficiencia de transmisión del MRFV silvestre por *D.
maidis* en condiciones controladas fue de **19/49 plantas (39 %)**, con 196
insectos sobre 49 plantas durante cuatro días tras un período de acceso de
adquisición de tres semanas `[E]` (`PLD3-4-e00224.pdf`, tabla 3 y sección 2.4).
Es el primer número de transmisión del MRFV por nuestra especie que tenemos de
fuente primaria.

---

## 8. Lo que viene después del corpus, y no abrimos

Buscamos trabajos que citen al más decisivo del corpus (P6) para saber si la vía
de entrega mediada por planta avanzó desde 2024. Existen y los dejamos
anotados **como pistas, no como fuentes: no los abrimos y no se pueden citar**
hasta que alguien los lea.

- Canuto, Marzachì, Bosco y Galetto, abril de 2026, sobre entrega no
  transformativa mediada por planta de ARNdc dirigidos a *Scaphoideus titanus*.
  Es la continuación directa de P6 y es el primer PDF que yo pediría después del
  de dsRNasas.
- Parise, Galetto, Palmano y Marzachì, octubre de 2025, una revisión de métodos
  de RNAi para estorbar la transmisión de fitoplasmas por vectores de floema.
- Canuto, Taliano, Marzachì y otros, *Journal of Pest Science*,
  doi 10.1007/s10340-025-01961-8, sobre silenciamiento de una subunidad
  reguladora del proteasoma 26S con mortalidad y esterilidad femenina en
  cicadélidos vectores.
- Un trabajo de 2026 indexado en PubMed con identificador 42374844 sobre
  herramientas de RNAi en la chicharrita de la remolacha por microinyección y
  por **pulverización tópica con nanopartículas de policatión en estrella**, con
  más del 90 % de knockdown por inyección a los 5 días según el resumen
  indexado.

El último es el que más nos interesa, porque cruza las dos cosas que el corpus
deja separadas: un cicadélido y un portador catiónico pulverizado.

---

## Lectura obligatoria

Seis papers, en este orden. El resto se puede consultar.

1. **`Papers/s10340-023-01670-0.pdf` (P6) — Rossi et al. 2024, entrega mediada
   por planta a cicadélidos.** Es el paper más cercano a nuestro problema que
   existe: dos cicadélidos vectores de fitoplasma, ARNdc entregado a través de
   la planta, con la vía que falló documentada y con la clave mecanística de por
   qué funciona —el xilema, no el floema—. Si alguien del equipo lee uno solo,
   es éste.

2. **`Papers/finsc-6-1811933.pdf` (P3) — Andrada et al. 2026, ETH y Burs-α en
   *D. maidis*.** Es la especie blanco, es el grupo argentino con el que
   probablemente se hable, y es el único lugar donde se puede ver qué criterio
   de diseño usan realmente. Leer en particular la sección de métodos: ahí está
   el tamaño de muestra verdadero detrás del 95 %.

3. **`Papers/Dcitri.pdf` (P1) — Galdeano et al. 2017, entrega oral en
   *Diaphorina citri*.** Por la curva de dosis y por los dos resultados
   incómodos: el control de GFP también mata a dosis alta, y el knockdown no
   escala con la dosis aunque la mortalidad sí. Es el paper que impide que
   prometamos de más.

4. **`Papers/s12298-024-01500-2.pdf` (P7) — Balassa et al. 2024, siRNA exógeno
   dentro de células de maíz.** Porque es la prueba física de que ARN exógeno
   entra a células de maíz, y porque dice exactamente dónde entra y dónde no.
   Más el concepto de cebado: la planta se prepara antes de la infección y el
   pico viral se corre una semana.

5. **`Papers/s00299-010-0911-z.pdf` (P5) — Gan et al. 2010, ARNdc bacteriano en
   maíz contra SCMV.** Es el precedente de maíz más directo, es la ruta de
   producción más barata que existe, y trae los dos límites que definen la
   economía del producto: la protección es preventiva y se pierde más allá de
   unos cinco días, y una lluvia la anula. Leerlo con el ojo puesto en la tabla
   2, por la razón que está en `contradicciones.md`, punto 2.

6. **`Papers/nplants2016207 (1).pdf` (P4) — Mitter et al. 2017, BioClay.** Para
   saber qué hay que superar y qué no está demostrado. Protege de nucleasas y
   del lavado, sí, con experimento; del UV, no lo midió nadie en ese paper. Y
   porque contiene la observación más desconcertante del corpus: protección
   antiviral sostenida **sin** siRNA detectables derivados del ARNdc aplicado.

**Queda fuera de la lectura obligatoria `Papers/PLD3-4-e00224.pdf` (P2)**, no
por poco relevante sino porque su utilidad es puntual: lo tiene que leer quien
trabaje sobre los candidatos de MRFV del EPILAB y quien necesite la arquitectura
del genoma viral. Para el resto del equipo alcanza con saber que **no** demuestra
silenciamiento del MRFV.

---

## Archivos de este paquete

- `REPORT.md` — este documento.
- `papers.json` — una entrada por paper, con relevancia, temas, resumen y qué
  reporte de la ola 1 toca.
- `contradicciones.md` — los seis puntos donde el corpus corrige o matiza lo que
  habíamos escrito, con la fuerza de la evidencia de cada uno.
- `glosario_parcial.md` — los términos nuevos que trae el corpus.
- `index.html` — la tabla de papers, filtrable por tema y por relevancia.
