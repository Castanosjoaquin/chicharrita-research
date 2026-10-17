# Síntesis

Investigación previa del equipo para el Investigathón de Y-Hat (UBA), track
*La chicharrita del maíz: un desafío de diseño y validación con ARN*
(EPILAB · IFIBYNE, UBA-CONICET). Cerrada el 17 de octubre de 2026, **antes** de
recibir las herramientas, las bases de datos y la bibliografía oficiales del
evento.

Cinco investigaciones independientes, 46.423 palabras de reportes citados y 211
fuentes distintas efectivamente abiertas. Este documento es lo que hay que leer
si se lee una sola cosa: qué sabemos ahora que no sabíamos, qué de lo que
creíamos era falso, qué vamos a construir y qué le vamos a preguntar al
investigador. Todo lo que se afirma acá está sostenido en el reporte de la
investigación que lo produjo, y el puntero está al lado.

---

## 1. La respuesta corta

**Vamos a construir una función de decisión sobre candidatos de ARN de doble
cadena dados: un orden, con el criterio escrito, la evidencia citada y la
incertidumbre propagada hasta el ranking, que diga cuáles merecen validación y
por qué, y que declare cuáles están empatados dentro de la incertidumbre.**

No vamos a diseñar secuencias nuevas, no vamos a entrenar ningún modelo y no
vamos a atacar la barrera de entrega. Las tres cosas están decididas y
registradas (`00_meta/DECISIONS.md`, D7 y D8), y las tres se decidieron por la
misma razón: son las únicas opciones que podemos **validar** sin un laboratorio.

El encuadre no es nuestro: es el del organizador, que declara tener candidatos
preliminares diseñados por su equipo y pregunta, textual, cuáles merecen
validación y por qué; y que declara que un equipo no debería ganar por construir
la interfaz más vistosa sino por producir la mejor decisión científica posible
con el tiempo y los datos disponibles.

Dos investigaciones que trabajaron por separado y desde preguntas distintas
—R2, que evaluaba una idea del equipo, y R4, que relevaba la frontera de
aprendizaje automático— llegaron de forma independiente a la misma propuesta.
R2 la llama PRIOR-dsRNA y R4 la llama L1. Es la señal más fuerte que tenemos de
que el encuadre es correcto.

---

## 2. Los tres supuestos que traíamos de la charla

Las notas de la charla del investigador invitado se trataron como hipótesis
numeradas, no como hechos (`DECISIONS.md`, D2). Así quedaron.

### S1 — Los patógenos y qué síntoma causa cada uno: **corregido**

Son cuatro agentes y el material oficial los nombra: dos virus (MRFV y MSMV),
un fitoplasma y *Spiroplasma kunkelii*. El fitoplasma tiene nombre formal desde
2026, '*Candidatus* Phytoplasma zeae', y tiene genoma completo y anotado desde
2016 —576.118 pb en una sola secuencia, aislado de un *Dalbulus maidis*
colectado en Piracicaba en 2013—, dato que el proyecto había dado por
inexistente porque lo buscaba por su nombre informal.

Lo que **no** se sostiene es la asignación de síntomas. Con fitoplasma y
espiroplasma inoculados por separado y juntos en cinco cultivares, en macetas
hasta cosecha: la reducción de producción de grano fue significativamente
distinta (P < 0,01) y **mayor con el espiroplasma**, mientras que la reducción
de altura **no** fue significativamente diferente entre fitoplasma, espiroplasma
o ambos; la inoculación simultánea no dio sinergismo. La idea de que uno afecta
los granos y el otro el tallo hay que abandonarla.
→ `research/R1_fundamentos/REPORT.md` §3.

### S2 — «BLAST separa en porciones y calcula la termodinámica»: **falso**

BLAST es alineamiento local: semilla y extensión, matrices de sustitución,
puntajes log-odds y un E-value que es estadística de similitud bajo un modelo
nulo. En ninguna parte de ese modelo aparece la energía libre de hibridación. La
termodinámica la calcula ViennaRNA —RNAfold para el autoplegamiento, RNAplfold
para la accesibilidad, RNAup para la energía de apertura—, que es un paquete
distinto con un modelo físico. Bowtie, que es lo que las herramientas del campo
usan para el tamizaje, tampoco calcula energía.

Son **dos ejes ortogonales**: BLAST y Bowtie responden «¿a qué otra cosa se
parece esta secuencia?», que es la pregunta de la especificidad; ViennaRNA
responde «¿qué tan favorable es que este dúplex se forme?», que es parte de la
pregunta de la eficacia. La operación de «dividir en porciones» existe, pero la
hace el diseñador con una ventana deslizante, no BLAST.

R1 y R2 verificaron esto por separado, con fuentes primarias distintas, y
llegaron a lo mismo. Era redundancia deliberada y sirvió: dos de los enfoques
que el equipo tenía en mente dependían de entender bien esta separación.
→ `research/R1_fundamentos/REPORT.md` §6 y `research/R2_attention_diseno_arn/REPORT.md` §1.

### S3 — ARN exógeno frente a ARN no codificante: **eran dos cosas distintas, y las dos aparecen**

«ARN exógeno» es una vía de administración: ARN aplicado desde afuera que dispara
la maquinaria endógena del receptor. «ARN no codificante» es una clase de
molécula. La confusión tenía una raíz real: APOLO, el nombre de la empresa, es el
de un ARN largo no codificante de *Arabidopsis* descrito por el grupo de su
fundador, y la empresa nació alrededor de esa línea. En su propia revisión
declaran dos mecanismos distintos —silenciar al patógeno con ARNdc contra genes
esenciales, y modular la planta para activar sus defensas—, y juegan en SIGS
(aplicación por pulverización, no transgénico) y no en HIGS (planta transgénica).
→ `research/R3_apolo_biotech/REPORT.md` §2.

---

## 3. El hallazgo que define la estrategia

La pregunta más importante de todo el trabajo era sobre qué actores del sistema
funciona realmente el RNAi. La respuesta ordena todo lo demás.

**Sobre los mollicutes, no.** Consulta propia a UniProtKB/InterPro, documentada y
reproducible: cero proteínas con dominio PIWI, cero con PAZ y cero con
dimerización de Dicer en Mollicutes (126.874 proteínas anotadas), en
*Spiroplasma* (36.551), en *S. kunkelii* (1.755) y en '*Candidatus* Phytoplasma'
(24.307), con control positivo de RNasa III en todos los taxones y juego completo
de dominios en *Zea mays* y en Hemiptera. No existe mecanismo conocido por el
cual un ARNdc exógeno silencie un gen del espiroplasma o del fitoplasma.
**Limitación declarada:** es una consulta de anotación, no una búsqueda por
perfil contra los genomas, de modo que no descarta genes no anotados.

**Sobre los virus, sí, pero el silenciamiento ocurre en la planta,** no en el
virus: es la célula vegetal la que corta el ARN viral con su propia maquinaria.
Hay 25 combinaciones virus-cultivo tratadas con ARNdc exógeno tabuladas en la
literatura, una de ellas en maíz. Para MRFV y MSMV en particular **no existe
ningún trabajo publicado**.

**Sobre el vector, sí, y está demostrado en la especie exacta:** knockdown de
~95 % de *burs-α* y ~90 % de *eth* por microinyección (125 ng por insecto,
n = 40 por tratamiento, control de ds-β-lactamasa), con supervivencia a día 4
cayendo a ~10 % y ~15 % contra ~100 % del control; y reducción de hasta 170 veces
del transcripto de *Bicaudal C* con caída de la oviposición.

**Consecuencia directa:** el circuito oficial de la diapositiva, que termina en
«inhibición del crecimiento del patógeno», no puede leerse como silenciamiento
directo de un mollicute. O es una simplificación, o se refiere a los dos virus, o
implica una vía indirecta. Es la primera pregunta para el investigador, y quedan
tres rutas plausibles: silenciar al vector, silenciar a los virus vía la planta,
o preparar la defensa de la planta.
→ `research/R1_fundamentos/REPORT.md` §4.

---

## 4. Lo que ya está hecho, y no hay que proponer como novedad

Esto es inteligencia competitiva, y evita el peor error posible: proponerle a
alguien del EPILAB la herramienta que usa todos los días.

| Lo que podríamos haber propuesto | Quién ya lo hizo |
| --- | --- |
| Una plataforma bioinformática de diseño de ARN con chequeo de off-targets | **Apolo Rocket**: corre en la nube, consume secuenciación masiva, evalúa más de 140 organismos a la vez y emite reportes automáticos |
| Encapsular el ARN para protegerlo de nucleasas y radiación UV | Publicado desde 2017, con al menos seis químicas distintas |
| Co-entregar ARNdc contra la dsRNasa del insecto | Publicado en 2023 por el grupo de Catalano, en esta especie |
| Pulverización foliar con efecto sistémico | Es el modo de aplicación de la industria y el estándar del campo |
| Nanoportadores para entrega controlada | Objetivo declarado y financiado de una cátedra 2025-2029 del fundador de APOLO |

Dos datos de contexto que conviene tener en la cabeza al hablar con ellos. El
laboratorio organizador y la empresa **comparten director, personal, espacio
físico y publicaciones**: quien venga del EPILAB conoce ese pipeline desde
adentro. Y en todo lo que pudimos abrir **no hay nada de APOLO sobre la
chicharrita**: su pipeline declarado son hongos y virus en cultivos intensivos, y
los extensivos estaban previstos para 2027, lo cual es coherente con que el costo
por gramo de ARN es lo que decide si el maíz cierra.
→ `research/R3_apolo_biotech/REPORT.md` §§1, 5 y 6.

---

## 5. Dónde cabe nuestro aporte

El hueco no es la falta de herramientas de diseño: hay de sobra. Es la **ausencia
de una función de decisión escrita**. Nadie publicó el criterio de agregación que
convierte los reportes de una plataforma en un orden defendible, y la propia
revisión del campo señala que no se han aplicado métodos formales de
cuantificación de incertidumbre a la predicción de eficacia, y lo llama la brecha
de máxima prioridad.

La línea de base es **dsRIP**, que ya hace la mayor parte del cálculo: puntaje de
eficacia con coeficientes calibrados en insecto, tamizaje de off-target con
Bowtie ponderando genes esenciales, y una ventana deslizante. Está publicado,
validado prospectivamente y en línea. Decirlo en voz alta es parte de la
propuesta: reconocer el baseline es más fuerte que ocultarlo.

Lo que agregamos, y es todo lo que agregamos:

1. **Incertidumbre propagada hasta el ordenamiento**, no un número puntual.
2. **Cada par de candidatos declarado como orden robusto o como empate**, que es
   la forma exacta que toma la pregunta del organizador.
3. **El frente de Pareto además del escalar**, que es la parte del orden que no
   depende de los pesos que elijamos.
4. **Instanciación en Hemiptera y en el agroecosistema del maíz argentino**, con
   el panel de organismos no objetivo que hoy no existe curado en ninguna parte.
5. **Exclusión fundamentada del término de accesibilidad**, convertida en una
   ablación medida y reportable.
6. **Anotación explícita de la barrera de entrega** por candidato, que ninguna
   herramienta existente registra.

---

## 6. La cartera de enfoques, priorizada

El criterio de orden es el del organizador, no el nuestro: cuánta decisión
defendible produce cada línea; si los datos que necesita existen hoy y son
abiertos; si es auditable; y si cabe en el plazo con cuatro personas y sin
laboratorio.

| Línea | Qué decisión produce | ¿Datos? | Riesgo principal | Esfuerzo |
| --- | --- | --- | --- | --- |
| **L1 · Priorización auditable con incertidumbre** (PRIOR-dsRNA) | Cuáles candidatos merecen validación, con intervalo y traza | Sí, salvo los candidatos del EPILAB | La transferencia de coleóptero a hemíptero no está validada | Bajo: 2 personas, 3-5 días |
| **L2 · Validación retrospectiva** contra el RNAi publicado | Si el puntaje discrimina, y cuánto | Sí, pero son decenas de puntos | n chico y sesgo de publicación: casi todo lo publicado funcionó | Medio: 1-2 personas, 4-6 días |
| **L3 · Mapa de riesgo fuera de blanco ponderado por consecuencia** | Qué candidato es inaceptable y por qué | Parciales: la esencialidad génica sólo existe para *Tribolium* | Mide riesgo potencial, no efecto medido | Medio-alto: 2 personas, 5-7 días |
| **L4 · Ajuste fino de un modelo fundacional** | Ninguna que se pueda defender hoy | **No** | Reproducir el error de los negativos barajados | Alto y mal invertido |

**L1 y L2 son una sola decisión en dos tiempos:** L1 produce el ranking y L2 lo
mide. L1 sin L2 es una opinión. L3 es independiente y cubre la obligación de
contracara de riesgo del proyecto.

**L4 queda documentada como descarte razonado, y el orden es el aporte.** Es la
línea que más impresiona y la que menos decisión produce. El conjunto de
entrenamiento honesto que existe en este subcampo son 31 siRNA probados en un
coleóptero; no hay nada en Hemiptera. Y cuatro evaluaciones independientes
coinciden en que los modelos fundacionales de ácidos nucleicos no dan ventaja
consistente fuera de su dominio: en la tarea medida más parecida a nuestro
tamizaje de off-target, todos los modelos de lenguaje de ARN rinden entre 2,49 y
5,00 de correlación contra 11,40 de una red convolucional entrenada desde cero.
La condición explícita que reactivaría L4 está escrita.

Hay un hallazgo que reencuadra el argumento y conviene decirlo así ante un
jurado: **los modelos fundacionales de ARN que mejor capturan estructura lo
logran porque incorporan predicciones de ViennaRNA en su preentrenamiento.** Usar
termodinámica directamente no es renunciar al modelo grande: es usar el
ingrediente que al modelo grande le da el resultado.
→ `research/R4_frontier_ml_rna/lineas_de_ataque.md` y
`research/R2_attention_diseno_arn/PROPUESTA.md`.

### Qué se rescata de la idea original del equipo

La intuición de tratar las porciones de ARN como tokens y mirar la atención
entre ellas se descarta como fue formulada —la termodinámica no puede ser la
loss, es una variable de entrada; la loss sólo puede ser el fenotipo medido; y la
arquitectura ya está publicada al menos cuatro veces—. Pero la **forma** del
problema que identificó es correcta: señal posicional a lo largo del transcripto,
donde distintas porciones valen distinto. Eso es exactamente el estado del arte,
y se satisface con un perfil posicional explícito del puntaje, que cumple la
misma función comunicativa que un mapa de atención y es **fiel por construcción**,
porque es el cálculo mismo y no una lectura de las entrañas de una red.

---

## 7. La rúbrica: la respuesta directa a la palabra «priorizar»

Es un entregable en sí mismo y está lista para aplicar. Ocho criterios con pesos
declarados **antes** de ver ningún candidato, cuatro compuertas que no se
compensan con puntaje, y dos totales por candidato —conservador y optimista—
cuya distancia dice qué medición hay que hacer antes de decidir.

| Criterio | Peso | Criterio | Peso |
| --- | --- | --- | --- |
| C1 Probabilidad de acción biológica | 20 | C5 Factibilidad técnica y de costo | 10 |
| C2 Especificidad y off-target en maíz | 15 | C6 Reproducibilidad | 10 |
| C3 Riesgo no objetivo y ambiente | 15 | C7 Viabilidad regulatoria | 5 |
| C4 Viabilidad de la vía de entrega | 20 | C8 Tiempo hasta demostración | 5 |

El ejemplo trabajado sobre cinco candidatos propios —construidos sobre blancos
con evidencia publicada, no son los del EPILAB— produce el orden conservador
**K2 (53,8) > K1 (52,5) > K5 (42,5) > K4 (40,0) = K3 (40,0, topado)**, y tres
resultados que valen más que el orden:

- **El candidato con el mejor fenotipo publicado es el que peor prioriza.** K3
  recibe 0 en vía de entrega porque toda su evidencia es por microinyección, y la
  inyección no es una vía agronómica; el tope lo deja en 40 pese a tener el mejor
  puntaje de acción biológica. La rúbrica lo explica en lugar de esconderlo.
- **Los dos primeros están empatados dentro de la incertidumbre,** y con el
  esquema de pesos alternativo —el que lee literalmente la declaración del
  organizador de que la barrera es la entrega— el orden entre ellos se invierte.
- **La medición de menor costo que más cambia el orden es el tamizaje de
  especificidad:** Bowtie contra el transcriptoma de maíz y los 56.116
  transcriptos del vector. Es una tarde de cómputo en una notebook, con datos
  públicos, sin laboratorio y sin permiso. Es lo primero que hay que correr.

La decisión científica que produce la rúbrica, entonces, no es «elijan K2». Es:
*los dos de cabeza están empatados, el desempate cuesta una tarde de cómputo, y
el candidato que incluye una respuesta a la barrera de las dsRNasas gana en
cuanto se pondera esa barrera como el propio organizador la pondera.* Eso es
aplicable mañana a los candidatos del EPILAB sin tocar un criterio.
→ `research/R5_metodologias_ejes/RUBRICA.md`.

---

## 8. El reparto para cuatro personas

Presupuesto declarado: 8 horas por persona por semana, 96 horas-persona en tres
semanas. Una sola dependencia dura, y se paga el primer día: **cuatro horas los
cuatro juntos para escribir los contratos de datos** —el esquema de la ficha de
candidato, el esquema de la salida y cinco candidatos de juguete—. Con eso cada
rama avanza contra datos falsos mientras llegan los reales, y ninguna queda
esperando a otra.

| Rama | Entregable propio | Horas |
| --- | --- | --- |
| **P1 · Datos y genómica** | Paquete de datos congelado, con manifiesto de hashes, licencia por insumo y procedencia, más los marcos de lectura del vector | 20 |
| **P2 · Diseño y tamizaje** | Informe de especificidad por candidato, con los dos criterios de off-target reportados por separado | 28 |
| **P3 · Herramienta y reproducibilidad** | El artefacto de decisión: motor de puntaje, fichas, análisis de sensibilidad, entorno fijado y tests | 26 |
| **P4 · Evidencia, riesgo y apertura** | Dossier de evidencia con la rúbrica poblada y citada, panel de no objetivo, estado regulatorio y paquete de apertura | 22 |

El punto no obvio del cronograma es que **el día del evento no se construye
nada**: se reemplazan nuestros candidatos por los del EPILAB y se vuelve a
correr. Lo que se construye antes es la capacidad de producir una decisión. El
hito a proteger es la primera corrida punta a punta sobre candidatos propios:
desde ahí el equipo tiene un entregable completo aunque no pase nada más.

El plan B está escrito para el escenario de fracaso más probable —que no existan
los datos para entrenar nada— y la respuesta incómoda es que **ya es verdad hoy y
el plan está construido para que no importe**: no entrenamos nada, y por eso el
cálculo es determinista y reproducible bit a bit.
→ `research/R5_metodologias_ejes/PLAN_EQUIPO.md`.

---

## 9. Lo que no vamos a poder validar, y hay que decirlo en la primera página

- **La transferencia de coleóptero a hemíptero.** Es la incertidumbre dominante
  del proyecto. Los coeficientes de eficacia que vamos a reusar se calibraron en
  *Tribolium castaneum* y se validaron prospectivamente en otros dos coleópteros;
  *Dalbulus maidis* es Hemiptera, y los propios autores dejan la validación fuera
  de coleópteros como pendiente. Ningún experimento computacional la resuelve.
- **La conservación poblacional del sitio blanco.** Los datos públicos no
  alcanzan: el término es calculable sobre un puñado de individuos y no es
  interpretable como conservación poblacional.
- **La relevancia funcional de los off-targets predichos.** Una coincidencia de
  secuencia no prueba un efecto, y hay al menos un caso publicado donde los
  cambios transcriptómicos no coincidieron con la complementariedad in silico.
- **Cualquier cosa sobre la eficacia real de la entrega.** Es un problema de
  banco y de parcela.

Cualquier cosa que entreguemos es una **hipótesis priorizada**, no un
tratamiento. Decirlo así, frente a alguien que conoce el pipeline desde adentro,
es más fuerte que insinuar lo contrario.

---

## 10. Las ocho preguntas para el investigador

La lista completa, con las quince, está en `00_meta/PREGUNTAS_ABIERTAS.md`. Si el
tiempo es corto, estas ocho:

1. ¿Qué significa «inhibición del crecimiento del patógeno» en el circuito de
   cuatro pasos, si no hay maquinaria de RNAi en los mollicutes?
2. Los candidatos preliminares: cuántos son, en qué formato, contra qué organismo
   y con qué vía de entrega prevista.
3. ¿Contra qué variable se validan: knockdown, mortalidad o transmisión?
4. El trabajo que nombra a '*Ca.* P. zeae' dice que la enfermedad no se reportó
   en la Argentina. ¿Es un error, o está distinguiendo el achaparramiento
   arbustivo del fitoplasma del achaparramiento del espiroplasma?
5. ¿Qué criterio de off-target usan: 19 nucleótidos complementarios, o el
   conjunto de reglas de la EFSA de 2025?
6. ¿Tienen datos propios de eficacia en la especie, y sobre todo **negativos**?
7. ¿En qué escalón de su escalera de precisión están los candidatos?
8. ¿Contemplan la co-entrega contra *Dmai-dsRNase-2*, y sus candidatos son de
   extremos romos o estructurados?

---

## 11. El estado de la evidencia, con sus límites declarados

211 fuentes distintas abiertas, consolidadas en `00_meta/FUENTES.md` con su nivel
de evidencia y su acceso; ocho de ellas fueron abiertas por más de una
investigación de forma independiente. Tres límites viajan con los números y hay
que repetirlos al presentarlos (`DECISIONS.md`, D9):

- **R4:** 29 de las 52 entradas del catálogo de modelos tienen su especificación
  tomada de la tabla de un relevamiento revisado por pares, no de su artículo
  primario. Está declarado entrada por entrada, y por eso esa investigación no
  marca su propia lista de verificación como aprobada.
- **R5:** unas diez fuentes de la sección de innovación abierta dependen de
  dominios institucionales que no estuvieron disponibles en la última corrida;
  conservan la verificación anterior, con citas textuales en sus notas, y no se
  volvieron a comprobar.
- **R1:** parte de las fuentes está leída sólo en el resumen, y el hallazgo sobre
  la ausencia de maquinaria de RNAi en mollicutes proviene de una consulta de
  anotación, no de una búsqueda por perfil.

Cuatro rechazos de herramienta quedaron registrados y **ninguno se reformuló**,
según la regla del repositorio. El más costoso es el del trabajo sobre dsRNasas
en *D. maidis*, que sigue sin abrirse y es el primer PDF para pedir.

---

## 12. Qué leer, y en qué orden

1. Este documento.
2. `research/R1_fundamentos/REPORT.md` — la biología, desde cero y para gente de
   IA. Es el más largo y el que más rinde.
3. `research/R2_attention_diseno_arn/PROPUESTA.md` — la especificación de lo que
   vamos a construir.
4. `research/R5_metodologias_ejes/RUBRICA.md` y `PLAN_EQUIPO.md` — cómo se
   decide y quién hace qué.
5. `research/R3_apolo_biotech/REPORT.md` — con quién estamos hablando.
6. `research/R4_frontier_ml_rna/lineas_de_ataque.md` — las alternativas y por qué
   quedaron en ese orden.
7. `00_meta/` — glosario, decisiones, caminos probados, preguntas abiertas y
   fuentes. Es lo que sobrevive a cualquier sesión de trabajo.

Cada carpeta tiene además su `index.html`, que es la misma información en versión
navegable y se lee en el celular. La portada es `index.html`, en la raíz.
