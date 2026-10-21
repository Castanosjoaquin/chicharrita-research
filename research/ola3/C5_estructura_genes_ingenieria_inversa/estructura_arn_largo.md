# Estructura de un ARN largo: qué se puede predecir, qué no, y si eso cambia la eficiencia

Investigación C5 de la ola 3. Fecha de las consultas y corridas: **20 de octubre de 2026**.
Marcadores según `CLAUDE.md`. Este documento contesta Q1 y no repite lo que
`research/R4_frontier_ml_rna/REPORT.md` §2 ya estableció sobre aprendizaje profundo aplicado a
estructura de ARN; lo que agrega es el eje que esa investigación no cubrió: **el largo de la
molécula**, los datos experimentales disponibles, y la única evidencia publicada en insectos.

---

## La respuesta, antes de todo

La afirmación del investigador —que para un ARN de 800 nucleótidos no se puede predecir cómo se
pliega ni en 2D ni en 3D en condiciones reales, que faltan datos empíricos y que los experimentos
que los darían son caros— **se sostiene, con dos precisiones que cambian qué se puede hacer hoy**.

La primera precisión es que «no se puede predecir la estructura secundaria» es demasiado gruesa.
Lo que no se puede predecir es la **estructura global** de un ARN largo: el plegado completo con
apareamientos de largo alcance. Lo que sí se puede, con exactitud medida y publicada, es la
**estructura local** —probabilidades de apareamiento y accesibilidad dentro de una ventana de
unos 150 nucleótidos—, y es justamente lo que calcula la herramienta que usa el laboratorio.
si-Fi21 no predice el plegado del ARNdc: corre `RNAplfold` con ventana de 80 y alcance máximo de
40 nucleótidos para estimar si los últimos 8 nt de cada ventana de 21 están desapareados
(`tools/sifi21_port/README.md`). Eso está dentro del régimen donde el plegado local es el método
más exacto disponible y no dentro del régimen imposible `[E]`.

La segunda precisión es la que más importa para el equipo, y es un hallazgo: **sí hay evidencia
publicada en insectos sobre estructura y eficacia, y dice dos cosas opuestas según de qué
estructura se hable**. La ausencia de estructura secundaria *dentro del siRNA de 21 nt* resultó
predictora significativa de eficacia insecticida en bioensayo; la **accesibilidad del sitio blanco
en el ARNm no resultó significativa**, ni en el ensayo de siRNA individual ni en el de ARNdc largo
(Cedden et al. 2025, *BMC Biology* 23:114) `[E]`. Y sobre lo que el investigador describió —cómo
se pliega la molécula de ARNdc de 800 nt y si ese plegado cambia la eficacia— **no encontramos
ningún estudio, en insectos ni fuera de ellos**, que lo mida. Eso es un vacío documentado, no un
resultado negativo: lo buscamos y no está.

---

## 1. Qué se puede y qué no se puede predecir de un ARN largo

| Qué | Método | Qué tan bien, medido | Aplica a 800 nt | Fuente |
|---|---|---|---|---|
| Plegado **global** de mínima energía libre | `RNAfold` sin restricción de alcance | Exactitud mediana de pares de bases **0,55** sobre 2.158 elementos curados de 90 familias de Rfam; **22 %** de los casos sin predecir (exactitud ≤ 0,2) | sí, pero es la peor opción | Lange et al. 2012 `[E]` |
| Plegado **local** con alcance acotado | `Rfold`, `RNAplfold`, `LocalFold` con L = 150, W = 200 | Exactitud mediana **0,65 / 0,60 / 0,62**; fallan en el **11-15 %** de los casos; la ventaja sobre el global **crece** en ARNm completos (diferencia 0,13 contra 0,07) | sí, es el régimen correcto | Lange et al. 2012 `[E]` |
| **Accesibilidad** de un tramo corto (función de partición) | `RNAplfold -u` | No evaluada como exactitud absoluta acá; es la cantidad que si-Fi21 usa con W=80, L=40, u=21 | sí | Lange et al. 2012; `tools/sifi21_port` `[E]` |
| Apareamientos de **largo alcance** (> 150 nt de separación) | cualquiera | El global sólo mejora al local en familias con alcances reales de 338 y 551 nt; en 151 estructuras de ncRNA, el 85 % de los pares tiene alcance ≤ 100 nt | **no** | Lange et al. 2012 `[E]` |
| Estructura secundaria con aprendizaje profundo | MXfold2, UFold, modelos de lenguaje | F1 cae de 0,72 a 0,50 al validar dejando una familia afuera; bajo baja homología ninguno mejora a one-hot | no cambia el panorama | R4 §2.1, fuentes abiertas allí `[E]` |
| Estructura **terciaria** | CASP16, RhoFold+, AlphaFold3 | Ninguna estructura natural no vista superó TM-score 0,8; RhoFold+ declara peor rendimiento por encima de unos 500 nt | **no** | R4 §2.2, fuentes abiertas allí `[E]` |
| Estructura **en condiciones reales** (en célula, con proteínas, cotranscripcional) | — | No hay método predictivo evaluado para esto | **no** | vacío documentado `[?]` |

La fuente central de las dos primeras filas es Lange, Maticzka, Möhl, Gagnon, Brown y Backofen,
*Global or local? Predicting secondary structure and accessibility in mRNAs*, *Nucleic Acids
Research* 40(12):5215-5226, 2012 (doi `10.1093/nar/gks181`), abierta por C5 el 20 de octubre de
2026. Curaron 2.500 elementos *cis*-regulatorios estructurados de 95 familias de Rfam —más de
85.000 pares de bases— y evaluaron contra ellos los métodos global y locales, más datos
experimentales de sondeo enzimático transcriptómico (PARS) para la accesibilidad. La conclusión
que cierra la discusión, en sus palabras, es que la menor exactitud en predecir apareamientos de
largo alcance hace que el plegado local sea mejor que el global para determinar la estructura
secundaria **en ARN largos** `[E]`. El mejor alcance máximo fue 150 nt, con la ventana al menos
50 nt mayor, y documentan un efecto de borde que degrada la predicción en los extremos hasta
cuatro veces el alcance máximo —600 nt para L = 150—, lo que es una advertencia directa para
quien recorte una región de 200 nt de un gen y la pliegue sola.

Dicho de otro modo: **para un ARN de 800 nt, el 85 % de los apareamientos que importan cae dentro
de un radio de 100 nt, y ése se predice con una exactitud mediana de ~0,6; el resto no se predice
y es el que define «cómo se pliega la molécula»**.

---

## 2. Los datos experimentales que existen, y por qué no alcanzan

El argumento del investigador —«se necesita dato»— es el correcto, y el dato tiene una forma
precisa. El conjunto experimental más grande del campo es **Ribonanza**: mediciones de mapeo
químico (SHAPE con 2A3 y DMS) sobre **dos millones** de secuencias de ARN diversas, reunidas por
Eterna y otras iniciativas de participación masiva, usadas para un desafío de Kaggle y destiladas
en el modelo RibonanzaNet (He, Huang, Townley y colaboradores, con Rhiju Das como autor de cierre; bioRxiv
`10.1101/2024.02.24.581671`, versión abierta por C5) `[R]`.

Tres números de ese trabajo explican el problema mejor que cualquier argumento.

**De dos millones de secuencias medidas, 170.000 alcanzaron relación señal-ruido mayor que 1 en
las dos químicas a la vez**, y 140.000 se usaron para entrenar. El dato crudo abunda; el dato
utilizable es el 8,5 % de él `[R]`.

**El largo máximo del conjunto está en el orden de los 450 nt, no de los 800.** Las secuencias de
evaluación prospectiva se eligieron a propósito con largos de **207 a 457 nt** para forzar
generalización por longitud, contra una biblioteca de entrenamiento de 177 nt `[R]`. No hay un
conjunto de mapeo químico de moléculas del tamaño de un ARNdc de diseño.

**Y la calidad del dato empeora con el largo.** Los propios autores reportan que los experimentos
que buscan secuencias más largas —un conjunto con inserto de 240 nt contra los de 50 a 130 nt—
dan fracciones menores de secuencias con señal-ruido por encima de 1, y encuentran una diferencia
estadísticamente significativa (P = 0,003) en el F1 de estructura secundaria entre secuencias
cortas, de menos de 75 nt, y largas, de 75 nt o más `[R]`.

Esto refina la afirmación del investigador: el cuello de botella no es sólo el precio. **Medir una
molécula larga no es medir muchas moléculas cortas a mayor costo; es un experimento cuya relación
señal-ruido se degrada con el largo.** Un presupuesto mayor no compra linealmente el dato que
falta.

Lo que no existe, y lo decimos como vacío: ningún conjunto público mide la estructura de un ARNdc
de diseño de 200 a 800 pb **dentro de un insecto**, ni en hemolinfa, ni en intestino, ni en
presencia de las nucleasas que el propio campo identificó como cuello de botella `[?]`.

---

## 3. La pregunta de fondo: ¿la estructura cambia la eficacia medida en insectos?

Hay un único experimento controlado que responde esto en insectos, y es el que está detrás de la
línea de base contra la que el repositorio ya se compara (`baseline_dsrip/`): Cedden et al.,
*Optimizing dsRNA sequences for RNAi in pest control and research with the dsRIP web platform*,
*BMC Biology* 23:114, 2025 (doi `10.1186/s12915-025-02219-6`),
abierto por C5. Tiene dos ensayos y conviene leerlos por separado porque miden cosas distintas.

**Ensayo 1, siRNA individuales.** Insertaron 31 siRNA de 21 nt, uno por vez, en un esqueleto no
dirigido de GFP modificado, generando ARNdc de 231 pb, y los inyectaron a 1 µg/µL en larvas L5 de
*Tribolium castaneum*, con n = 20 por grupo. La letalidad fue del 100 % a los 6 días en un extremo
y del 0 % a los 8 días en el otro: el mismo gen blanco, la misma dosis, 31 resultados distintos.
Ajustaron un modelo de riesgos proporcionales de Cox sobre 29 de ellos (C de Harrell = 0,76, con
intervalo de confianza del 95 % de 0,73 a 0,79) con nueve rasgos de secuencia. **Cuatro
resultaron significativos (P < 0,05): la asimetría termodinámica, el puntaje de energía de
autoplegado de la hebra antisentido —que es alto cuando la hebra *no* forma estructuras consigo
misma—, el contenido GC entre las posiciones 9 y 14 del antisentido, y la presencia de una
adenina en la posición 10.** No resultaron significativos (P > 0,05) la región blanco del ARNm
(marco de lectura contra región no traducida), **el puntaje de accesibilidad del ARNm**, el GC de
toda la hebra antisentido y la energía de unión del antisentido al blanco `[E]`.

**Ensayo 2, ARNdc largos.** Tomaron 8 genes esenciales de *T. castaneum* y diseñaron, para cada
uno, tres o cuatro ARNdc: la región de 300 pb de mayor puntaje medio de siRNA dentro del marco de
lectura, la de menor puntaje, la de mayor puntaje sin restringir al marco, y **la región de mayor
puntaje medio de accesibilidad del ARNm**. Inyectaron 1 ng/µL en larvas L5, con n = 25 por ARNdc.
En la regresión múltiple (R múltiple = 0,79, 17 grados de libertad), **el puntaje de eficacia de
siRNA fue el predictor significativo y positivo (aumento de 1,462 en la razón de riesgo por cada
unidad, P = 0,003), la accesibilidad del ARNm no lo fue (P = 0,41), y apuntar al marco de lectura
en lugar de a la región no traducida sí lo fue (aumento de 9,91, P = 0,011)** `[E]`.

La lectura conjunta es la que importa para el diseño:

**Sí, la estructura cambia la eficacia medida, pero la estructura que importa es la del propio
siRNA de 21 nucleótidos, no la del ARNm largo.** El autoplegado de una hebra de 21 nt se predice
sobre 21 nt: es el régimen más fácil que existe, no el de los 800. La accesibilidad del sitio
blanco —la que requiere plegar el ARNm largo— es la que no apareció como predictor, y es además
la única que fue puesta a prueba *de frente*, diseñando ARNdc expresamente sobre la región más
accesible y midiendo si mataban más. No mataron más.

Los propios autores ofrecen dos explicaciones alternativas y no las adjudican: que los ribosomas
deshagan la estructura del ARNm mientras se traduce —lo que explicaría de paso por qué el marco
de lectura funciona mejor que la región no traducida—, o que la predicción de estructura en
escarabajos sea sencillamente mala y la accesibilidad sea mejor predictor de lo que su medición
sugiere `[?]`. La segunda explicación es, en esencia, la del investigador.

**Lo que nadie midió.** No encontramos ningún trabajo que pregunte si el plegado de la molécula
de ARNdc larga —no del siRNA, no del ARNm blanco, sino del ARN de doble cadena que se aplica—
cambia la eficacia. La búsqueda que hicimos cubrió literatura abierta sobre estructura secundaria
de ARNdc y eficiencia de ARNi en insectos, accesibilidad del sitio blanco, y los conjuntos de
datos de mapeo químico; las fuentes abiertas están en `sources.json`. Es un hueco real y es,
además, un hueco con sentido biológico: un ARNdc perfectamente apareado no tiene mucha estructura
que predecir, y el procesamiento por Dicer no es aleatorio a lo largo de la molécula —el mismo
trabajo de dsRIP muestra un perfil de siRNA unidos a RISC reproducible entre experimentos
independientes— pero nadie relacionó ese perfil con una predicción de plegado `[H]`.

---

## 4. Por qué no hay modelo que entrenar, dicho con los números

El objetivo pedía una declaración clara. Es ésta, y tiene tres partes que se acumulan.

**No hay etiquetas de eficacia en hemípteros.** El único conjunto con bioensayos de insecto
sistemáticos es el de dsRIP, y es de *Tribolium castaneum*, un coleóptero: 31 siRNA en un gen más
8 genes con tres o cuatro ARNdc cada uno. Son del orden de 60 mediciones de eficacia, no de
60.000. El repositorio ya midió, además, que el techo de reproducibilidad del dato publicado es
bajo: dos ARNdc contra el mismo gen correlacionan 0,245 (`pipeline/REPORT.md` §6) `[H]`.

**No hay estructuras medidas del tamaño que importa.** Ribonanza llega a 457 nt con 140.000
secuencias utilizables, y la exactitud ya se degrada entre menos de 75 nt y 75 nt o más `[R]`.

**Y el rasgo estructural que sí predice ya está calculado por las herramientas existentes.** El
autoplegado del antisentido es un cálculo de ViennaRNA sobre 21 nt que si-Fi21 y dsRIP ya hacen.
No hace falta un modelo para eso; haría falta uno para la accesibilidad del ARNm largo, que es
exactamente la variable que el único experimento controlado en insectos encontró no significativa.

De ahí la consecuencia práctica, que coincide con la decisión que el repositorio ya tomó por otro
camino (`00_meta/CAMINOS_PROBADOS.md`, accesibilidad con peso cero por defecto): **la variable que
un modelo nuevo podría mejorar es la que la evidencia dice que no importa, y la que importa no
necesita modelo.** Para el ejercicio del Investigathón eso no es una mala noticia: es el argumento
que justifica no entrenar nada y dedicar el esfuerzo a la priorización auditable.

---

## 5. «El que resuelva la estructura se gana el Nobel»: qué puede y qué no puede aportar el equipo

El cierre honesto es que **el equipo no puede aportar nada al problema de predecir el plegado de
un ARN largo en condiciones reales, y no por falta de talento sino por falta de laboratorio**. El
cuello de botella del subcampo es dato experimental de moléculas largas con señal-ruido
aceptable, y eso se produce con química de sondeo y secuenciación, no con cómputo. Ribonanza
muestra el camino que sí escala —participación masiva en el diseño de las secuencias, medición
centralizada— y muestra también que incluso así el largo sigue siendo el límite.

Lo que el equipo sí puede hacer, y es defendible en una semana, es tres cosas que no requieren
ningún dato nuevo: **declarar el régimen de validez** de cada término estructural que use un
puntaje —local sí, global no, 21 nt sí, 800 nt no—; **medir la ablación** del término de
accesibilidad en su propio ranking, que es la pregunta abierta que la literatura dejó sin
adjudicar; y **usar el experimento de dsRIP como control retrospectivo**, porque sus 8 genes con
tres o cuatro diseños cada uno y su razón de riesgo medida son el conjunto de validación más
parecido a lo que el laboratorio querría predecir.

Si el investigador quiere una respuesta corta para la frase del Nobel: el problema no está
esperando un método, está esperando un instrumento. Y el instrumento mide peor cuanto más larga
es la molécula.
