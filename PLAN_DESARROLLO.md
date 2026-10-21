# Plan de desarrollo — después del Checkpoint 1

**Fuente principal:** `research/checkpoints/checkpoint1.md`, la reunión de 25 minutos con el
investigador invitado. Todo lo que sale de ahí es `[R]` —es lo que dijo una persona en una
reunión, con dos tramos de audio perdido—, salvo lo que él presenta como mecanismo consolidado,
que va como `[E]`. Lo que este plan agrega como criterio propio va marcado `[H]`.

**Estado.** Escrito el 2026-10-20 a partir del checkpoint; actualizado el 2026-10-21 con lo que
devolvieron las cinco investigaciones de la ola 3 y con el ranking que se produjo en paralelo.

**Qué es este documento.** El orden de trabajo que sale del checkpoint: qué pidió el
investigador, qué de eso ya está hecho en el repositorio, qué falta, y en qué secuencia
conviene hacerlo. No reemplaza a `SINTESIS_V2.md`, que sigue siendo el panorama del proyecto;
lo que hace es convertir la reunión en tareas con entrada, salida y criterio de terminado.

---

## 0. Lo que el checkpoint cambia

Cuatro cosas, y ninguna es menor.

**Las bacterias salen del alcance.** `[E]` El mecanismo de ARN de interferencia no existe en
bacterias: *«de las bacterias olvídense, porque son otros mecanismos»*. La rama del complejo
patogénico que pensábamos atacar por esa vía se cae. Esto coincide con lo que R1 §4 y R6 ya
habían medido por homología en los dos mollicutes, así que no es una corrección sino una
confirmación por otra vía.

**El objetivo es el insecto, no el patógeno dentro de la planta.** `[R]` Las dos estrategias son
legítimas y él recomienda la del vector por directa. A eso se suma el argumento de la latencia
—unos 20 días entre que la chicharrita se infecta y puede transmitir— que él confirmó: hay una
ventana para matarla antes de que contagie.

**La ventana se fija en 21 y 22 nucleótidos.** `[E]` El fundamento es biológico: es el tamaño en
que la maquinaria corta y el tamaño del fragmento que después se aparea. Por debajo de eso la
molécula no funciona. Su regla de método, que adoptamos: *«tenés que tener la evidencia
biológica atrás de por qué elegís 21»*.

**El ejercicio es auditar, no reproducir.** `[R]` Los cuatro diseños de la planilla los hizo él
mismo hace unos dos años, nunca se testearon porque bajó la incidencia de la plaga, y no
recuerda con certeza por qué eligió esas regiones. No hay un resultado validado que replicar:
hay una decisión vieja de la que ni el autor está seguro. Eso convierte nuestro trabajo en una
auditoría, que es exactamente lo que un equipo sin laboratorio puede hacer bien.

Y el criterio con el que nos va a evaluar, textual: *«no porque tenga que ser cierto eso que
decís, porque al final hay que evaluarlo, sino el pensamiento que nos llevó a ustedes para
decidir ese ranking»*. **Se evalúa el razonamiento, no el acierto.** La consecuencia de método
es que cada número que entreguemos tiene que venir con el porqué de haberlo elegido, y que un
«no se puede saber con los datos que hay» bien fundamentado suma en vez de restar.

---

## 1. Los cinco pedidos, y qué hay de cada uno

Él los enumeró en orden. Esta es la foto honesta de dónde estamos.

| # | Lo que pidió | Qué hay ya | Qué falta |
| --- | --- | --- | --- |
| 1 | **Leer y entender si-Fi21**: qué implica que algo sea eficiente, cómo lo calculan, qué significa la energía libre ahí | El port a Python 3 verificado contra el programa original: `tools/sifi21_port/`, los tres filtros implementados y `CAMBIOS.md` con lo que se cambió y por qué | El paper y la fuente primaria de cada umbral; qué validó el artículo y qué no; de dónde sale el criterio de 150–250 nt |
| 2 | **Benchmarking** de si-Fi21, dsRNA-Engineer y BLAST sobre los cuatro genes | **Hecho** en `research/ola2/W7_ranking/benchmark_tres_herramientas.md`: las tres en un eje común, con el panel de referencias verificado como idéntico y la atribución del conteo por condición | Nada del pedido. Queda el hueco declarado: los dos genes del insecto no tienen corrida de dsRNA-Engineer y no la van a tener |
| 3 | **Un ranking** de candidatos con el criterio explicitado | **Hecho** el 2026-10-20 en `research/ola2/W7_ranking/`: el orden, las cinco decisiones declaradas, la ficha por candidato y el barrido de 2.000 juegos de pesos | Rehacerlo con lo que la ola 3 midió después, que toca su recomendación central (ver §3) |
| 4 | **Evaluación de las regiones ya elegidas** | **Hecho** en `W7_ranking/REPORT.md` §2.2 y §2.3: la región dentro de cada gen, con la región alternativa recomendada en los dos genes del insecto y el efecto sobre el orden | Revisar la recomendación contra el panel ampliado, que la da vuelta en `BicC_Dm` (§3) |
| 5 | **Crítica de las herramientas**, aunque no la implementemos | **Casi todo el material ya existe y está medido**: la regla terminal que saltea la física, las tablas de ADN dentro de un cálculo de ARN, los tres defectos operativos de si-Fi21, el conteo de dsRNA-Engineer dominado por la condición de 16 pb, lo que BLAST no puede hacer, y qué herramienta conviene para qué (`benchmark_tres_herramientas.md` §5) | Juntarlo en un documento único escrito para que lo lea él, con las mejoras propuestas |

Y las dos extensiones opcionales que ofreció: **sumar genes nuevos** encontrados en la
literatura, y **comparar 21 contra 22 nt**.

---

## 1 bis. Dónde está parado el entregable, al 2026-10-21

De los cinco pedidos, **tres están cerrados, uno está casi y uno falta**. Lo cerrado no lo hizo
esta línea de trabajo: salió de la rama del ranking (`research/ola2/W7_ranking/`, commits de
Santino del 2026-10-20) y de la ola 3 (`research/ola3/`). Conviene leerlo junto porque las dos
mitades se tocan.

| Pedido | Estado | Dónde está | Qué falta |
| --- | --- | --- | --- |
| 1 · Entender si-Fi21 | **Cubierto como contenido, falta el documento** | `tools/sifi21_port/` + `research/ola3/C1_sifi21_paper_metodo/` | La nota corta y legible, para él (T1) |
| 2 · Benchmarking de las tres | **Cerrado** | `W7_ranking/benchmark_tres_herramientas.md` | Nada del pedido |
| 3 · Ranking con criterio | **Cerrado** | `W7_ranking/REPORT.md` §2 a §4 | Rehacerlo con el panel ampliado (T3) |
| 4 · Evaluación de las regiones | **Cerrado, con una revisión pendiente** | `W7_ranking/REPORT.md` §2.2 y §2.3 | La recomendación de `BicC_Dm` no sobrevive al panel ampliado |
| 5 · Crítica de las herramientas | **Material completo, sin documento** | Disperso en seis archivos | Juntarlo y escribirlo para él (T5) |
| Opcional · 21 contra 22 | **Cerrado** | `research/ola3/C3_blast_ventana_azar/ventana_21_vs_22.md` y `C6_panel_y_largo/` | Nada |
| Opcional · Genes nuevos | **Cerrado como catálogo** | `research/ola3/C5_.../catalogo_genes_blanco.md` | Meter los dos mejores al ranking (T6) |

**Lo que esto quiere decir en una línea:** el entregable ya existe y lo que queda no es
producirlo sino **reescribir dos piezas con lo que se midió después, y redactar dos documentos
con material que ya está**. No hay ninguna medición grande pendiente.

Y una pregunta que el checkpoint dejó abierta y que ahora tiene respuesta medida: **la cuenta del
azar que él pidió para 18, 19 y 20 nucleótidos está hecha dos veces, por dos caminos, y las dos
coinciden aunque a primera vista parezca que no.** La rama del ranking contó cuántas *ventanas*
tienen al menos un acierto y encontró que por debajo de 18 nt aparecen **menos** de las que
predice el azar; la ola 3 contó el *total* de coincidencias y encontró que coincide con el azar
una vez corregido por composición. No se contradicen: hay tantas coincidencias como predice la
estadística, pero amontonadas sobre menos ventanas, porque caen en familias repetidas. Él tenía
razón en lo que se ve al tamizar, y la razón no es la que parecía.

---

## 2. Fase 0 — la investigación de la ola 3, terminada

Cinco investigaciones en paralelo, con la misma estructura de prompts de las olas anteriores,
en `prompts/C1.md` a `prompts/C5.md`. Se lanzaron el 2026-10-20 y terminaron el mismo día; sus
entregables están en `research/ola3/`. Lo que devolvieron está resumido en §3 bis.

| | Qué responde | Alimenta a |
| --- | --- | --- |
| **C1** | El paper de si-Fi21, el umbral de cada filtro y su fuente primaria, qué validó el artículo, de dónde sale 150–250 nt | Pedido 1 |
| **C2** | El código público del grupo que mantiene la reescritura de si-Fi21 y la plataforma: qué parámetros cambiaron y si reproducen los conteos de la planilla | Pedidos 1, 2 y 5 |
| **C3** | El parámetro de BLAST que nombró, el benchmark de 21 contra 22, y cuántas coincidencias da el azar contra cuántas hay de verdad | Pedido 2 y opcional 2 |
| **C4** | Cuánta coincidencia hace falta para silenciar fuera del blanco, cómo pesar genoma contra transcriptoma, qué pasa en las quimeras, de dónde sale el largo de la región | Pedidos 3 y 4 |
| **C5** | Estructura de ARN largos y por qué no hay modelo que entrenar; catálogo de genes blanco con evidencia; el circuito de ingeniería inversa | Opcional 1 |

**Hallazgo que disparó C2.** Buscando el GitHub que él mencionó aparecieron dos repositorios
públicos del grupo de bioinformática de INTA: `sifi21INTA`, una reescritura de si-Fi21 en
Python 3 con módulos propios, y `apolorocket`, descrito como el backend de endpoints para
predecir siRNA. Los dos con licencia GPL-3.0. `[R]` Que sean el código al que se refirió el
investigador es una inferencia nuestra `[H]`, apoyada en el nombre y en que el código deriva de
si-Fi21; confirmarlo es parte de C2. Si lo es, responde de una la pregunta que teníamos abierta
desde hace días: por qué su planilla declara 114, 35, 199 y 33 cuando si-Fi21 sin modificar da
133, 32, 212 y 42.

---

## 3. Fase 1 — las tareas del entregable

Cada tarea dice qué consume, qué produce y cuándo está terminada. Las que dependen de la fase 0
lo dicen.

### T1 · La nota de método: qué significa «eficiente»

**Entrada:** `research/ola3/C1_sifi21_paper_metodo/` —que ya tiene el artículo, el manual, la tabla
de umbrales con su fuente y lo que el artículo validó—, más `tools/sifi21_port/` y
`sifi21_reproduccion.md`. **El contenido está completo: lo que falta es escribirlo para él.**
**Salida:** una nota corta, legible por alguien que no programa, que explique la ventana de 21,
los tres filtros, qué es la energía libre acá y qué NO es —no es eficacia medida, es una regla
de diseño—, y una tabla con el umbral de cada filtro, su fuente y si esa fuente es evidencia
empírica o convención.
**Terminada cuando:** cada fila de la tabla tiene fuente abierta o dice «convención».
**Por qué primero:** él lo puso primero, y sin esto el ranking no se puede defender.

### T2 · El benchmarking de las tres herramientas — hecho

**Estado:** hecho el 2026-10-20 en `research/ola2/W7_ranking/benchmark_tres_herramientas.md`.
Lo que cerró, y por qué es más fuerte de lo que este plan pedía:

- **El panel de referencias es el mismo.** Las cinco referencias no objetivo que usa
  dsRNA-Engineer son exactamente los mismos ensamblados que los nuestros, así que las
  diferencias de resultado son atribuibles al método y no al dato. Esa verificación es la que
  vuelve interpretable todo lo demás.
- **La atribución del conteo, replicada.** Para los dos genes virales, dsRNA-Engineer informa 215
  y 87 off-targets en maíz donde nuestro tamizaje exacto no encuentra ninguna coincidencia de
  21 nt: **el 100 % de ese riesgo viene de la condición de 16 pb y el 0 % de la de 21–22 pb**.
  W2 ya lo había medido sobre un gen; ahora son tres.
- **Dónde BLAST subestima.** El criterio de un desajuste medido con BLAST+ queda por debajo del
  exacto por un factor de hasta 3,2, y la causa está identificada: `blastn-short` con palabra 11
  no puede sembrar un 21-mero cuyo desajuste cae en la posición 11.
- **La compuerta de confidencialidad quedó documentada como procedimiento**, no como principio:
  se verificó byte a byte que los dos genes virales son subcadenas exactas de un registro público
  del NCBI, se pidió autorización explícita antes de subir, y los dos genes del insecto no se
  subieron.

**El hueco, que es un resultado y va a la presentación:** la herramienta que el organizador
señala como la de diseño y verificación de off-targets es exactamente la que no se puede usar con
el material que el mismo organizador entregó. Y un dato operativo que lo refuerza: los fragmentos
que recomienda miden entre 51 y 91 pb, y el laboratorio sintetiza regiones de 150 a 300.

### T3 · El ranking de los cuatro candidatos — hecho, con segunda versión

**Estado:** existe desde el 2026-10-20 en `research/ola2/W7_ranking/`. El orden es
`MP_MRFV` > `CP_MRFV` > {`BicC_Dm`, `ATPaseD_Dm`}, y lo que aguanta el barrido de pesos es la
primera mitad: los dos genes del insecto no se distinguen entre sí, su orden relativo se da
vuelta según los pesos, y decir «`BicC_Dm` es tercero» sería reportar una elección de pesos y no
una medición. Lo que separa a los virales de los del insecto no es el puntaje sino una
compuerta: las regiones elegidas de los dos genes del insecto contienen ventanas con
coincidencia perfecta de 21 nt en el transcriptoma de un cicadélido no objetivo, y las virales
no contienen ninguna. Están además las cuatro fichas y las cinco decisiones de agregación, cada
una con su alternativa y su consecuencia.

**Lo que queda por hacer, y no es cosmético.** Dos mediciones posteriores tocan su recomendación
central de mover la región dentro de los dos genes del insecto:

- Al agregar al panel el cicadélido más cercano a la chicharrita con genoma anotado, la región
  que el ranking propone para `BicC_Dm` tiene **19 ventanas con coincidencia perfecta de 21 nt**
  contra las 10 de la región que eligió EPILAB: en ese eje la recomendación empeora las cosas.
  Hay salida medida —otra región del mismo gen que escapa al veto perdiendo una sola ventana
  eficiente— pero la recomendación tal como está escrita no sobrevive (`research/ola3/C6_panel_y_largo/`).
- El benchmark de 21 contra 22 nt muestra que el conteo de eficientes casi no cambia, pero **el
  conjunto de ventanas eficientes cambia casi entero**, y en los dos genes largos la región
  elegida se muda al pasar de 21 a 22 (`research/ola3/C3_blast_ventana_azar/`).

**Estado (2026-10-21): la segunda versión está hecha** en `research/ola3/C7_ranking_v2/`. Con la decisión del equipo de
no usar *Macrosteles* (D23), la v2 reproduce W7 exacto, suma humano, `eth` y `burs-alpha`, y reporta el orden a 21 y a 22 nt:
las puntas aguantan y el medio no. La tarea original era:

**Tarea:** una segunda versión del ranking que incorpore el panel ampliado y declare la
estabilidad del orden frente al largo de ventana. **Terminada cuando:** cada recomendación de
mover una región dice contra qué panel se evaluó, y el documento dice cuáles de sus conclusiones
cambiaron respecto de la primera versión.

### T4 · La auditoría de las regiones 1–200 — hecha, y con una revisión pendiente

**Estado:** hecha en `W7_ranking/REPORT.md` §2.2 y §2.3. Para los dos genes del insecto hay
región alternativa recomendada —`BicC_Dm` 2123-2422 y `ATPaseD_Dm` 72-371—, mejores en los dos
ejes a la vez, y el informe dice explícitamente qué pasa si el laboratorio acepta moverlas: el
orden cambia y `BicC_Dm` salta de pelear el último puesto a quedar segundo.

**Lo que queda, y no es un detalle:** al agregar al panel el cicadélido más cercano a la
chicharrita con genoma anotado, la región recomendada para `BicC_Dm` tiene 19 ventanas con
coincidencia perfecta de 21 nt contra las 10 de la que eligió EPILAB, así que en ese eje la
recomendación empeora las cosas. Hay salida medida —otra región del mismo gen que escapa al veto
perdiendo una sola ventana eficiente—, pero **la recomendación tal como está escrita no
sobrevive al panel ampliado** y hay que reescribirla.

**Nota de método que ya pagamos:** el número de eficientes de una región depende de si se calcula
sobre la región recortada o sobre el gen entero, y la diferencia llega al 47 %. Hay que declarar
cuál se usó antes de comparar.

### T5 · La crítica de las herramientas

**Entrada:** seis archivos que ya tienen la crítica medida y dispersa: `tools/sifi21_port/CAMBIOS.md`,
`W2_herramientas/REPORT.md` §4, `sifi21_reproduccion.md`, `benchmark_tres_herramientas.md` §5,
`research/ola3/C2_codigo_apolo_inta/` y `research/ola3/C3_blast_ventana_azar/`. **No falta medir
nada: falta el documento.**
**Salida:** un documento por herramienta con lo que falla, cómo lo comprobamos y qué mejora
propondríamos. Él fue explícito en que no hace falta implementarla. Lo que ya tenemos y entra
acá: la rama de la regla terminal de si-Fi21 que declara eficiente un siRNA que falló los
filtros termodinámicos —entre el 14 % y el 24 % de lo que reporta como eficiente, medido ventana
por ventana sobre los cuatro genes—; las tablas de energía de ADN usadas dentro de un cálculo de
ARN; los tres defectos operativos que encontramos al correr el original; y que el conteo de
off-targets de la herramienta oficial, leído como riesgo, está dominado por la condición de
16 pb.
**Terminada cuando:** cada crítica tiene la medición o la línea de código que la respalda. Una
crítica sin evidencia no entra.

### T6 · Las extensiones opcionales

**21 contra 22 nt** (de C3) y **genes nuevos de la literatura** (de C5). Van al final porque son
opcionales, pero la de genes nuevos es la que él más valoró: dijo que la búsqueda de candidatos
es *«el estado del arte del problema»*. Si entra uno solo al ranking con su evidencia, ya suma.

---

## 3 bis. Lo que la ola 3 devolvió

Las cinco investigaciones terminaron el 2026-10-20 y están en `research/ola3/`. Siete resultados
cambian algo de lo que este plan daba por sentado. Cada uno lleva el aviso de con qué
profundidad se midió, porque varias piezas quedaron limitadas por el entorno.

**El GitHub del laboratorio se confirmó, y con él el parámetro que cambiaron.** `sifi21INTA` es
una reescritura de si-Fi21 en Python 3 y `apolorocket` es el backend que la usa: `Sirna.py` y
`freeEnergy.py` son el mismo archivo en los dos repositorios. El único parámetro de química que
tocaron es la tabla de vecinos más cercanos, que pasó de la de Chen 2012 a una que el comentario
del código atribuye a Zuber 2022 `[R]` —el artículo de Zuber no se abrió, así que la atribución
es del comentario y no está verificada—. Todo lo demás del criterio quedó igual, **incluida la
rama de la regla terminal que declara eficiente un siRNA que falló la termodinámica**, transcrita
literal. `[E]`

**Pero sigue sin reproducir la planilla.** `sifi21INTA` con sus valores por defecto da 138, 40,
218 y 35 contra los 114, 35, 199 y 33 declarados, y un barrido de 22.176 configuraciones no
encuentra ninguna que dé los cuatro. Lo que más se acerca es subir el umbral de estabilidad de
extremos de 1,0 a 1,75. Y una hipótesis que teníamos quedó descartada: en esta librería el
conteo es por ventana y no por acierto de Bowtie, así que **la base de datos no explica la
diferencia**. Con la salvedad de que no hay RNAplfold 2.1.5 en esta máquina, así que la
comparación contra la corrida del programa original está confundida por la versión de ViennaRNA.

**Apolo Rocket no ordena nada.** Leído entero: diecinueve funciones sobre PostgreSQL, Bowtie y
ViennaRNA, sin ningún puntaje ni ningún criterio de orden, y la eficiencia no se guarda por
siRNA sino como la curva del gráfico, de modo que no se puede auditar qué ventana fue eficiente.
Hay un parámetro `method` documentado como «'sifi21' or 'IA'» **sin ninguna implementación del
método IA**. `[E]` No se corrió la plataforma: requiere una base y una capa HTTP no publicadas,
así que esto es lectura de código, no medición.

**«Identidad» no es un filtro de eficiencia.** El investigador la nombró como tercer término del
criterio; el artículo no tiene ningún filtro de identidad dentro de la regla. Entra por dos vías
distintas: el presupuesto de desajustes de BOWTIE, que por defecto es cero, y un experimento del
propio artículo donde la eficacia cae por debajo del 92 % de similitud. Y los dos umbrales
numéricos de la regla —1 kcal/mol y 0,1— **no tienen fuente primaria que los fije**: el artículo
los enuncia como valores de la herramienta. `[E]`

**BLAST no sirve para este tamizaje, y ahora está medido.** Sobre 3.150 consultas con desajustes
plantados en cada posición, ninguna configuración detecta los 21-meros con un desajuste en todas
las posiciones: el techo es 0,762 y el `megablast` por defecto da cero. La causa no es la semilla
sino que la extensión recorta un desajuste cercano al extremo en vez de cruzarlo. Para esto hace
falta coincidencia exacta con presupuesto de desajustes, que es lo que ya hacen Bowtie y el
tamizador del repositorio. Y «HCP» es casi con seguridad «HSP», que no es un parámetro sino la
unidad de resultado de BLAST `[H]`.

**El argumento del azar es más fino de lo que parecía.** El total de coincidencias en un genoma
real **es el que predice el modelo** una vez corregido por composición: razones
observado/esperado de 1,000 a 1,235 para k de 16 a 20. Donde el azar falla es en la
distribución: con k = 16 predice que el 36,4 % de las ventanas tendría alguna coincidencia y lo
observado es 15,9 %, porque las coincidencias no se reparten, se amontonan sobre los k-meros de
familias repetidas. **Hay las mismas coincidencias que predice la estadística, repartidas entre
menos ventanas.** Eso explica el salto de 16 a 17 de nuestra tabla.

**Los 150–250 nt no salen de la literatura, y hay evidencia en contra en nuestra propia
especie.** Un trabajo de 2026 silenció dos genes en *Dalbulus maidis* con ARNdc de 578 y 544 pb,
con reducción del transcrito y mortalidad alta. Lo que la evidencia sí sostiene es el piso, de
unos 60 pb. Una revisión de 2025 dice que no hay consenso sobre el largo óptimo. Lectura
nuestra `[H]`: el rango del laboratorio es una convención razonable y compatible con la
evidencia, no una conclusión de ella.

**Y aparecieron genes nuevos con evidencia mejor que la de los candidatos actuales.** Dos con
evidencia funcional en la propia especie objetivo, `eth` y `burs-alpha`, con knockdown del 90 al
95 % y supervivencia del 10 % al día 4 contra más del 95 % del control; tienen ARNm público de
*D. maidis*, así que se les pudo calcular la ventana sobre la secuencia correcta: 44 y 33 siRNA
eficientes. Y uno letal y esterilizante probado en dos géneros de cicadélidos de la misma
subfamilia, con una advertencia nuestra: por secuencia, el transcrito que usaron pertenece a otra
familia de proteínas que la que el trabajo nombra `[?]`. De 36 filas del catálogo, 15 se
leyeron solo por resumen y registran fenotipo pero no dosis ni n.

---

## 4. Fase 2 — nuestro valor agregado

Esto es lo que ponemos encima de lo pedido, y conviene que sea explícitamente lo segundo y no lo
primero: él acotó expectativas dos veces y dijo que construir una plataforma no es realista
—lleva cinco meses arreglando la que tienen—. Todo lo de esta sección está marcado `[H]` y
ninguna de estas piezas reemplaza a las de la fase 1.

**Desagregar el número en vez de sumar uno nuevo.** La herramienta oficial produce un conteo que
mezcla cosas distintas. Nuestro aporte más barato y más defendible es separarlo: cuántos
aciertos vienen de cada condición, cuáles caen en un gen expresado y cuáles no, cuáles están en
la región semilla. Es la decisión D11 del proyecto y el checkpoint la refuerza, porque él mismo
entregó el criterio de genoma contra transcriptoma como parámetro de ranking.

**El margen de conservación entre aislados.** La región de cápside elegida es 100 % idéntica al
aislado de Costa Rica y pierde la mayor parte de sus siRNA conservados frente a los brasileños,
y en GenBank no hay ninguna secuencia argentina de ese virus. Es un riesgo real, medido, que
ninguna herramienta del corpus evalúa.

**La cuantificación de la incertidumbre.** El barrido de pesos, la sensibilidad al umbral y la
declaración de qué no se puede saber. Es lo que convierte un ranking en un argumento, y es
exactamente lo que él dijo que iba a evaluar.

**Lo que NO vamos a hacer, y por qué conviene decirlo en voz alta.** No entrenamos ningún modelo
de eficacia. Él lo explicó mejor que nosotros: no hay datos empíricos suficientes sobre qué
diseños son realmente eficientes ni sobre cómo se pliega un ARN largo, así que no hay nada que
entrenar, y *«el que haga bien eso se gana el Nobel igual que el AlphaFold»*. Coincide con la
decisión D8, que tomamos antes de la reunión por otras razones. Que el límite sea del campo y no
nuestro es un resultado del proyecto y va dicho en la primera página, no escondido al final.

---

## 5. Lo que depende de él

Ninguna de estas preguntas bloquea el trabajo; todas lo mejoran. Van en el correo, ordenadas por
cuánto cambian el resultado y por lo barato que le resulta contestarlas.

1. **¿Qué versión de si-Fi corrió y contra qué base de datos?** si-Fi21 sin modificar da 133, 32,
   212 y 42 sobre los cuatro genes, y su planilla dice 114, 35, 199 y 33. Tres por encima y uno
   por debajo, así que no es un desplazamiento constante. Si C2 confirma que el código público
   del grupo es el suyo, esta pregunta puede quedar contestada sin molestarlo.
2. **¿La región 1–200 se eligió por off-targets y no por densidad?** Él mismo lo sospechó y dijo
   no recordarlo. Medido: en uno de los genes la región elegida tiene menos de la mitad de
   ventanas eficientes que la mejor región del mismo largo.
3. **¿Qué pesos le daría a cada criterio del ranking, y qué umbral de identidad usa para
   descartar por off-target?** Son los dos parámetros libres del motor. Mientras no los tengamos,
   usamos un valor declarado y mostramos el barrido.
4. **¿Cuál de los transcriptomas del vector usan, y nos lo pasan?** De eso depende que las
   posiciones de la planilla sean reproducibles con datos públicos.
5. **Confirmación de la grafía del apellido y del dominio del correo** antes de escribirle. La
   transcripción automática lo escribió de varias formas.

---

## 6. El reparto para cuatro personas

Mismo presupuesto que venimos usando. Lo que cambia respecto del reparto de `SINTESIS_V2.md` es
que ahora hay un pedido explícito del investigador que ordena las prioridades.

| Rama | Dueño de | Entregable | Estado |
| --- | --- | --- | --- |
| **Método** | T1 y T5 | La nota de qué significa «eficiente» y la crítica de las herramientas | **Es lo que falta.** Dos documentos de redacción, con todo el material ya medido |
| **Medición** | T2 y T4 | El benchmarking de las tres herramientas y la auditoría de las cuatro regiones | Hecho. Queda reescribir la recomendación de región contra el panel ampliado |
| **Decisión** | T3 | El ranking, las cuatro fichas y el análisis de sensibilidad | Hecho. Queda la segunda versión con el panel ampliado |
| **Evidencia** | T6 y la fase 2 | Los genes nuevos con su evidencia, el margen de conservación y las preguntas para él | Catálogo hecho; falta meter los dos mejores candidatos al ranking |

El hito a proteger ya se pasó: **la primera corrida punta a punta sobre los cuatro candidatos
reales, con su ficha, existe desde el 2026-10-20**. Desde acá el riesgo cambia de naturaleza —ya
no es llegar, es que lo que está escrito se contradiga con lo que se midió después—, y por eso
las dos reescrituras valen más que cualquier medición nueva.

---

## 7. Decisiones a formalizar

Para `00_meta/DECISIONS.md`, cuando se integre la ola 3. Quedan anotadas acá para no perderlas:

- Las bacterias salen del alcance del diseño por ARNi. El fundamento es mecanístico y está
  confirmado por dos vías independientes.
- El objetivo del diseño es el insecto como vector, no el patógeno dentro de la planta, con el
  argumento de la ventana de latencia.
- La ventana se fija en 21 y 22 nucleótidos, con la evidencia biológica como fundamento y no por
  convención heredada de la herramienta.
- El ejercicio sobre los cuatro candidatos es una auditoría de una decisión vieja, no la
  reproducción de un resultado validado. Cambia qué significa que nos vaya bien: un
  «la elección es mejorable, y acá está por qué» es un resultado, igual que un
  «la elección se justifica».
