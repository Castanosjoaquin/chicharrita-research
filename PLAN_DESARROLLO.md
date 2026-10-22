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
| 1 | **Leer y entender si-Fi21**: qué implica que algo sea eficiente, cómo lo calculan, qué significa la energía libre ahí | **Hecho.** El port verificado contra el original, `research/ola3/C1_sifi21_paper_metodo/` con el artículo y la fuente de cada umbral, y la nota escrita en `entregables/que-significa-eficiente.md` | Nada |
| 2 | **Benchmarking** de si-Fi21, dsRNA-Engineer y BLAST sobre los cuatro genes | **Hecho** en `research/ola2/W7_ranking/benchmark_tres_herramientas.md`: las tres en un eje común, con el panel de referencias verificado como idéntico y la atribución del conteo por condición | Nada del pedido. Queda el hueco declarado: los dos genes del insecto no tienen corrida de dsRNA-Engineer y no la van a tener |
| 3 | **Un ranking** de candidatos con el criterio explicitado | **Hecho** el 2026-10-20 en `research/ola2/W7_ranking/`: el orden, las cinco decisiones declaradas, la ficha por candidato y el barrido de 2.000 juegos de pesos | ~~Rehacerlo con lo que la ola 3 midió después~~ (hecho el 2026-10-21 en `research/ola3/C7_ranking_v2/`). Nada del pedido; el 2026-10-21 se corrigió la lectura de B.3 (W7 §2.1 bis) y se midió la sensibilidad a los umbrales (`research/ola3/C9_sensibilidad_umbral/`) |
| 4 | **Evaluación de las regiones ya elegidas** | **Hecho** en `W7_ranking/REPORT.md` §2.2 y §2.3: la región dentro de cada gen, con la región alternativa recomendada en los dos genes del insecto y el efecto sobre el orden | ~~Revisar la recomendación contra el panel ampliado, que la da vuelta en `BicC_Dm` (§3)~~ **Hecho el 2026-10-21**: C8 movió la región de `BicC_Dm` de 2121-2420 a 922-1221 por conservación (D25) y `ATPaseD_Dm` mantiene la suya. Nada del pedido. Esta fila quedó desactualizada frente a §1 bis y al cuerpo de T4, que ya lo declaraban cerrado; corregido al detectar la contradicción |
| 5 | **Crítica de las herramientas**, aunque no la implementemos | **Hecho.** Todo el material medido, reunido y escrito en `entregables/critica-herramientas.md`: si-Fi21, dsRNA-Engineer, BLAST y el código del laboratorio, cada crítica con su medición o su línea de código, más las mejoras que propondríamos | Nada |

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
| 1 · Entender si-Fi21 | **Cerrado** | `tools/sifi21_port/` + `research/ola3/C1_sifi21_paper_metodo/` + `entregables/que-significa-eficiente.md` | Nada |
| 2 · Benchmarking de las tres | **Cerrado** | `W7_ranking/benchmark_tres_herramientas.md` | Nada del pedido |
| 3 · Ranking con criterio | **Cerrado, con segunda versión** | `W7_ranking/REPORT.md` §2 a §4 y `research/ola3/C7_ranking_v2/` | Nada del pedido; la v2 reproduce W7 exacto, suma humano, `eth` y `burs-alpha`, y reporta 21 y 22 nt. Fortalecido el 2026-10-21: lectura de B.3 corregida (W7 §2.1 bis, C7 §4) y sensibilidad a los umbrales en `research/ola3/C9_sensibilidad_umbral/` |
| 4 · Evaluación de las regiones | **Cerrado y revisado** | `W7_ranking/REPORT.md` §2.2 y §2.3, y `research/ola3/C8_conservacion/` | Nada del pedido; `BicC_Dm` pasa a 922-1221 por conservación (D25) y `ATPaseD_Dm` mantiene 72-371 |
| 5 · Crítica de las herramientas | **Cerrado** | `entregables/critica-herramientas.md` | Nada |
| Opcional · 21 contra 22 | **Cerrado** | `research/ola3/C3_blast_ventana_azar/ventana_21_vs_22.md` y `C6_panel_y_largo/` | Nada |
| Opcional · Genes nuevos | **Cerrado: catálogo y entrada al ranking** | `research/ola3/C5_.../catalogo_genes_blanco.md` y `C7_ranking_v2/` | Un transcriptoma que contenga `eth` y `burs-alpha`, para medir su conservación |

**Lo que esto quiere decir en una línea:** **los cinco pedidos están entregados y los dos
opcionales también.** Las dos reescrituras que este plan listaba —el ranking con el panel ampliado
y la región de `BicC_Dm`— se hicieron el 2026-10-21 (C7 y C8); los dos documentos que faltaban
—T1 y T5— se escribieron el mismo día y están en `entregables/`; y el fortalecimiento que
recomendaba §3 ter se hizo en C9. No hay ninguna medición grande pendiente. Lo que queda es de
cierre y está en §8.

El ranking v2 (`research/ola3/C7_ranking_v2/`, 2026-10-21) cerró las dos reescrituras que este
plan listaba. Hizo lo que corresponde antes de agregar nada: **reprodujo a W7 exacto** —los cuatro
conteos de eficientes, las cuatro fichas campo por campo y el barrido— y recién después sumó
humano al panel, los dos genes nuevos y el cálculo a 21 y a 22 nt. Ninguna conclusión de W7 se
cayó. Los dos genes nuevos entran sin vetos pero quedan cuartos y quintos cuando se compara a
todos en su mejor región, y eso es por diseño: su aporte es la evidencia publicada, que se
presenta como un eje descriptivo aparte y sin puntaje, porque sumarla al puntaje exigiría una
equivalencia entre un fenotipo de microinyección y uno de ingesta que no tenemos (D24).

**La región de `BicC_Dm` se movió dos veces, y la segunda vez por conservación y no por el panel.**
C7 recomendaba 2121-2420; C8 la pasa a **922-1221** porque de sus 36 ventanas eficientes 32 son
idénticas en los tres transcriptomas públicos de *Dalbulus maidis* y las 36 son exactas en el
transcriptoma argentino y en el genoma de Córdoba, contra 22 de 35 en 2121-2420, y el cambio no
mueve el orden del ranking (D25, `research/ola3/C8_conservacion/`). `[E]` Lo que importa para la
discusión que este plan dejaba abierta: 922-1221 es la misma región que C6 había encontrado como
salida al veto de *Macrosteles quadrilineatus*, **pero ahora llega por un motivo que no depende de
ese pariente**, así que la recomendación ya no cuelga de D23. Esa decisión igual quedó con su
premisa verificada el 2026-10-21 contra GBIF: de 3.592 ocurrencias, 2.929 son de Canadá y 549 de
Estados Unidos, y hay cero en Argentina y cero en las siete consultas sudamericanas. `[E]` Y el
segundo flanco que el propio D23 declara sigue abierto para el panel —*Macrosteles* se había
incorporado como **sustituto filogenético** del resto de los Deltocephalinae, no por exposición
directa—, pero ya no puede tumbar esta región: si el investigador dice que los cicadélidos hermanos
cuentan como no objetivo, lo que hay que revisar es el panel del ranking, no la región de
`BicC_Dm`.

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

### T1 · La nota de método: qué significa «eficiente» — hecha

**Estado:** escrita el 2026-10-21 en [`entregables/que-significa-eficiente.md`](entregables/que-significa-eficiente.md).
Explica la ventana de 21 y los tres filtros sin pedir que se abra código, dice qué es la energía
libre acá y qué no es, y trae la tabla con el umbral de cada filtro y su fuente. El saldo de esa
tabla, que es lo que hay que poder decir en voz alta: **dos umbrales tienen fuente experimental
abierta, dos tienen fuente para el principio pero no para el número, y dos no tienen ninguna** —el
margen de 1,00 kcal/mol y los 22 °C—. Incluye además las tres cosas que el artículo no dice y se
verificaron una por una: que «identidad» no es un filtro de eficiencia, que lo validado son doce
construcciones en cebada con fenotipo y no caída de transcrito (Pearson −0,61, n = 12), y que el
rango de 150-250 nt no está ni en el artículo, ni en el manual, ni en el código.

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

**Lo que motivó la segunda versión.** Dos mediciones posteriores tocaron su recomendación
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

**Fortalecimiento del 2026-10-21 (C9).** Se corrigió la lectura de B.3: la diagonal sale de que
los cruces de los pares en conflicto caen al borde del rango de pesos y de que la limpieza casi no
tiene palanca con la escala absoluta, no de que el orden sea robusto (W7 §2.1 bis y C7 §4, con la
afirmación vieja tachada). Y se midió, sin etiquetas y con el backend `vienna`, cuánto depende la
recomendación de los dos umbrales sin fuente primaria: el candidato superior (`MP_MRFV`) se
mantiene en el 98–99 % de la grilla, pero la región exacta de 200 nt no, y el par
`ATPaseD_Dm`/`CP_MRFV` es un empate práctico **si se lo mide con la ventana libre de 200**.
Mide fragilidad, no calidad del umbral. **T1 bis, misma fecha:** el barrido se repitió sobre
la región que de verdad proponemos y con el veto de off-target aplicado, a 21 y 22 nt y sobre
los seis candidatos del ranking v2. Reeligiendo la región con la regla del ranking, `MP_MRFV`
queda primero en el **100 %** de la grilla a 21 nt y el par `ATPaseD_Dm`/`CP_MRFV` **deja de
estar empatado** (se invierte en el 3,3 %, no en el 48,9 %), porque la ventana libre de
`ATPaseD_Dm` cae sobre una región vetada. Lo frágil pasa a ser congelar las coordenadas: con
las regiones fijas y el umbral moviéndose, `MP_MRFV` queda primero en apenas el 62 %. Los
empates que quedan son otros pares: `CP_MRFV`/`burs-alpha` y `eth`/`burs-alpha`.
Ver `research/ola3/C9_sensibilidad_umbral/REPORT.md`.

### T4 · La auditoría de las regiones 1–200 — hecha y revisada

**Estado:** hecha en `W7_ranking/REPORT.md` §2.2 y §2.3, y **revisada el 2026-10-21 en
`research/ola3/C7_ranking_v2/`**. Para los dos genes del insecto hay región alternativa
recomendada, mejor en los dos ejes a la vez, y el informe dice explícitamente qué pasa si el
laboratorio acepta moverlas: el orden cambia y `BicC_Dm` salta de pelear el último puesto a
quedar segundo. Las regiones vigentes, después de C8, son **`BicC_Dm` 922-1221** —por
conservación (D25), en lugar de la 2121-2420 de C7, que a su vez corría dos nucleótidos respecto de
la 2123-2422 de W7 por la columna de humano— y **`ATPaseD_Dm` 72-371**, igual que en W7.

**La revisión, hecha el 2026-10-21.** Al agregar al panel el cicadélido más cercano a la
chicharrita con genoma anotado, la región que W7 recomendaba para `BicC_Dm` tenía 19 ventanas con
coincidencia perfecta de 21 nt contra las 10 de la que eligió EPILAB (C6). El equipo decidió dejar
a *Macrosteles* fuera del ranking (D23), con el argumento de que no está en Argentina: esa premisa
**quedó verificada el 2026-10-21 contra GBIF** —de 3.592 ocurrencias, 2.929 son de Canadá y 549 de
Estados Unidos, con cero en Argentina y cero en las siete consultas sudamericanas `[E]`—, aunque el
flanco que D23 declara sigue abierto, porque la especie entró como sustituto filogenético del resto
de los Deltocephalinae y no por exposición directa. Con esa decisión las recomendaciones de W7
vuelven a valer (C7), y la conservación entre fuentes públicas (C8) cambia solo una: **`BicC_Dm`
pasa de 2121-2420 a 922-1221** (36 eficientes, 32 idénticas en los tres transcriptomas, todas en el
argentino; D25), sin costo en el orden de diseño, y por un criterio que ya no depende de
*Macrosteles*; `ATPaseD_Dm` mantiene 72-371. Es conservación entre fuentes públicas y no entre
poblaciones de campo.

**Nota de método que ya pagamos:** el número de eficientes de una región depende de si se calcula
sobre la región recortada o sobre el gen entero, y la diferencia llega al 47 %. Hay que declarar
cuál se usó antes de comparar.

### T5 · La crítica de las herramientas — hecha

**Estado:** escrita el 2026-10-21 en [`entregables/critica-herramientas.md`](entregables/critica-herramientas.md),
con la regla de que cada crítica va con la medición o la línea de código que la respalda. Cubre
si-Fi21, dsRNA-Engineer, BLAST y el código del laboratorio, y cierra con las mejoras que
propondríamos sin implementarlas, como él pidió.

Las cuatro que más pesan: **la accesibilidad del sitio blanco no muestra valor predictivo sobre la
eficacia medida** (OR 1,00 [0,89–1,12] en 300 casos humanos; HR 0,9994 con P = 0,853 en
*Tribolium*), y es una de las tres patas del criterio; **el 100 % del riesgo que informa
dsRNA-Engineer viene de su condición de 16 pb**, que a su vez es indistinguible del azar (860
ventanas observadas contra 909 esperadas por un nulo que conserva la composición, razón 0,95, y
0,98 contra un nulo barajado; la señal recién aparece de 18 nt en adelante); **BLAST no puede hacer este tamizaje**, con un
techo medido de 0,762 de sensibilidad y cero con los valores por defecto de `megablast`; y en el
código del laboratorio, **una secuencia en minúsculas produce cero eficientes en silencio**, medido
138 contra 0 sobre el mismo gen.

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

## 3 ter. Recomendación: qué hacer ahora, y en qué orden

Escrito el 2026-10-21, después de auditar el barrido y de calcular la potencia real de la
validación retrospectiva. El encuadre que ordena todo: **de los cinco pedidos no queda ninguno**,
así que lo que se agregue de acá en más compite con el tiempo de revisión, no con llenar un hueco.

**Actualización del 2026-10-21, al cierre:** las opciones 1, 2 y 3 están hechas, y de la 4 está
escrito el pre-registro ~~pero la validación no se corrió~~ **y la validación se corrió el 2026-10-21**
(`research/ola3/C9_sensibilidad_umbral/RESULTADOS_validacion_retrospectiva.md`): el veredicto con el
criterio pre-registrado es **no concluyente** (ρ = +0,142, IC95 [−0,247, +0,492], n = 29). La tabla queda tal como se escribió,
con el veredicto de cada fila anotado, porque el razonamiento que descartó las opciones 6 y 7 es
parte del entregable: es la respuesta fundada a «¿por qué no entrenaron un modelo?».

| Opción | Qué daría | Pros | Contras | Veredicto |
| --- | --- | --- | --- | --- |
| **1. Escribir T1 y T5** (nota de «eficiente» y crítica de herramientas) | Los dos únicos pedidos del investigador sin entregable | Material íntegramente medido y disperso en seis archivos; es redacción, no investigación. Cierra el pedido que él puso primero | Ninguno. Es trabajo pendiente, no una apuesta | **Hecho el 2026-10-21** — `entregables/que-significa-eficiente.md` y `entregables/critica-herramientas.md` |
| **2. Sensibilidad del umbral sin etiquetas** | Si mover el corte de accesibilidad de 0,1 o la brecha de 1,00 kcal/mol cambia el orden de candidatos | No necesita etiquetas ni laboratorio. La maquinaria existe (`barrido.py`, `ranking.py`). Contesta de frente «¿cómo saben que 0,1 es el valor?» con una medición | No dice si el umbral es bueno, sólo si la recomendación es frágil. Hay que no confundir las dos cosas al presentarlo | **Hacer segundo** — *hecho el 2026-10-21 en C9* |
| **3. Corregir cómo se presenta B.3** | Que la diagonal se lea como lo que es | Una tabla y un párrafo. Evita que nos pregunten lo que ya sabemos que no se sostiene | Obliga a mostrar que el orden modal cae del 98,7 % al 33,7 % en la otra escala | **Hacer tercero** — *hecho el 2026-10-21 (W7 §2.1 bis y C7 §4)* |
| **4. Validación retrospectiva pre-registrada** | Una cota sobre cuánto discrimina el puntaje | Es la única comprobación empírica posible sin laboratorio. Los 28 ARNdc de Cedden son CC BY y están en el repo. «Con este n no se distingue» es un resultado | **Sub-potenciada por un factor 2,4 en n**: con la fiabilidad medida del desenlace, una correlación verdadera de 0,7 se observa como 0,35 y la potencia con n = 28 es 0,42. Harían falta n = 67 | ~~**Hacer cuarto, con tiempo acotado y el pre-registro escrito antes**~~ — ***hecho el 2026-10-21***: pre-registro con tres enmiendas fechadas y validación corrida. Veredicto **no concluyente** (ρ = +0,142, IC95 [−0,247, +0,492], n = 29) |
| **5. Curva precisión-recall barriendo el umbral** | El umbral elegido con su precisión y su cobertura | Es el método correcto, y la fila de Reynolds (88,9 % de precisión con 1,1 % de cobertura) muestra la forma que tendría | Necesita las mismas etiquetas de la opción 4, así que hereda su falta de potencia. Con n = 28 los intervalos tapan la curva | **Sólo como salida de la opción 4, no como línea propia** |
| **6. Modelo de ML existente entrenado en humano** | Una estimación de eficacia por ventana | Existen, son buenos en su dominio (Pearson 0,55-0,58 entre conjuntos humanos, AUC 0,81-0,87) y correrlos es barato | Al cambiar de ensayo caen a AUC ≈ 0,50, que es azar; y entre humano e insecto el GC de las posiciones 9-14 invierte su signo. Sin verdad de terreno en hemípteros no hay forma de saber si acertó | **No como predictor. Sólo como ablación declarada sobre los datos CC BY de *Tribolium*** |
| **7. Aprendizaje no supervisado para predecir eficacia** | — | — | No resuelve la falta de etiquetas: la mueve al cabezal. Un método no supervisado encuentra estructura, no puede saber que esa estructura es silenciamiento | **Descartar como predictor.** Sí vale lo label-free que ya hacemos: el eje de especificidad, que es un hecho de alineamiento y no una predicción |
| **8. Encadenar fuentes independientes de confiabilidad** | Una lista corta con alta precisión | Es el uso correcto del techo bajo del dato: filtrar conservador en vez de ordenar fino | Sólo paga si las fuentes son de naturaleza distinta —termodinámica, alineamiento, conservación entre aislados—. Sumar proxies correlacionados infla la confianza sin agregar información | **Adoptar como criterio de presentación del ranking**, no como línea de trabajo aparte |

**Lo más valioso que tenemos y todavía no usamos.** La accesibilidad del sitio blanco es una de
las tres condiciones de si-Fi21, y es la que **no mostró valor predictivo sobre la eficacia
medida**: OR 1,00 con intervalo [0,89–1,12] sobre 300 casos humanos de siRecords, y en *Tribolium
castaneum* HR 0,9994 con P = 0,853. `[E]` Eso es una crítica con evidencia al criterio en el que
el laboratorio basa su pipeline, y es exactamente lo que el investigador pidió en el punto 5. Va
en T5 y es lo más fuerte que tenemos para decir.

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
| **Método** | T1 y T5 | La nota de qué significa «eficiente» y la crítica de las herramientas | Hecho: los dos documentos están en `entregables/` |
| **Medición** | T2 y T4 | El benchmarking de las tres herramientas y la auditoría de las cuatro regiones | Hecho, y la recomendación de región ya se reescribió (C8, D25) |
| **Decisión** | T3 | El ranking, las cuatro fichas y el análisis de sensibilidad | Hecho, con la segunda versión (C7) |
| **Evidencia** | T6 y la fase 2 | Los genes nuevos con su evidencia, el margen de conservación y las preguntas para él | Catálogo hecho y los dos mejores candidatos ya están en el ranking (C7); queda la conservación de `eth` y `burs-alpha` y la de `MP_MRFV`, que no se puede evaluar con los registros públicos (C8) |

El hito a proteger ya se pasó: **la primera corrida punta a punta sobre los cuatro candidatos
reales, con su ficha, existe desde el 2026-10-20**. Desde acá el riesgo cambia de naturaleza —ya
no es llegar, es que lo que está escrito se contradiga con lo que se midió después—, y por eso
las dos reescrituras valen más que cualquier medición nueva.

---

## 7. Decisiones a formalizar — hecho

Las cuatro decisiones que el checkpoint dejó abiertas se escribieron en `00_meta/DECISIONS.md`
el 2026-10-21, con el mismo formato ADR que las demás:

| | Decisión | Dónde |
| --- | --- | --- |
| **D33** | Las bacterias salen del alcance del diseño por ARNi | `00_meta/DECISIONS.md` |
| **D34** | El objetivo es el insecto como vector, no el patógeno dentro de la planta | `00_meta/DECISIONS.md` |
| **D35** | La ventana se fija en 21 y 22 nt por evidencia biológica, no por convención | `00_meta/DECISIONS.md` |
| **D36** | El ejercicio sobre los cuatro candidatos es una auditoría, no una reproducción | `00_meta/DECISIONS.md` |

Son las cuatro más estructurales del proyecto, porque no deciden un parámetro sino el encuadre: a
qué se le apunta, con qué largo, y qué cuenta como que nos haya ido bien.

---

## 8. Lo que queda, al cierre del 2026-10-21

Los cinco pedidos y los dos opcionales están entregados. Esto es todo lo que el plan deja abierto,
y ninguna de las tres cosas es una medición que bloquee el entregable.

**El correo al investigador, con las cinco preguntas de §5.** Está escrito en
[`entregables/correo-investigador.md`](entregables/correo-investigador.md) y **no se envió**:
falta confirmar la grafía del apellido y el dominio antes de mandarlo, que es la quinta pregunta de
la lista y la única que bloquea a las otras cuatro.

**La conservación de `eth` y `burs-alpha`.** Es la única medición pendiente del plan, y el
2026-10-21 cambió de forma. ~~el transcriptoma que contiene los dos genes **no está depositado en
ninguna base pública**.~~ **Corrección (C11, mismo día):** la búsqueda local con `blastn` encuentra
secuencia de ambos genes en el TSA de Pergamino (GHCC01): `eth` en el contig `GHCC01027218.1` con los
615 nt de la consulta en cadena reversa, y `burs-alpha` en `GHCC01014529.1` con 439 de 468 nt en
cadena directa, las dos verificadas letra por letra. Los hits del TSA de Ohio (GITV01) no están
verificados. Ver `research/ola3/C11_conservacion_eth_bursa/REPORT.md`. Andrada *et al.* 2026 los identificaron sobre un ensamblado propio de la
UNNOBA (tesis de Palacio 2018); lo único público son las dos secuencias codificantes, PZ371507 y
PZ371508. Pero el paso que correspondía no se dio: C8 buscó con el BLAST web contra todo el TSA,
que se colgó, **cuando los tres transcriptomas que ya usa están descargados** y la búsqueda local
contra ellos es de minutos y sin compuerta de confidencialidad, porque las consultas son públicas.
El camino completo, en cuatro pasos por costo, está en `00_meta/PREGUNTAS_ABIERTAS.md`. La de
`MP_MRFV` no es una tarea pendiente sino un resultado: C8 determinó que **no se puede evaluar** con
los registros públicos disponibles.

**La validación retrospectiva.** El pre-registro está escrito
(`research/ola3/C9_sensibilidad_umbral/PREREGISTRO_validacion_retrospectiva.md`) con tres enmiendas
fechadas, y ~~la validación no se corrió~~ **se corrió el 2026-10-21**. El conjunto primario pasó a ser
los 31 siRNA de *Tc-gawky* (enmienda 2: empalme por clave real 31/31, unidad de 21 nt y un solo gen) y
los 28 ARNdc quedaron como confirmatorio. **Veredicto con el criterio fijado de antemano: no
concluyente** —ρ = +0,142 con IC95 [−0,247, +0,492] sobre n = 29, y el confirmatorio ρ = +0,236
[−0,161, +0,568]—, que es el resultado que el propio pre-registro declaró como más probable. La curva
precisión-recall sólo supera la base de 82,8 % en el umbral más bajo del barrido (0,02: precisión 0,875, con IC95 [0,529, 0,978] que contiene la base), y en el umbral por defecto de 0,1 queda por debajo (0,800). Lo que esto agrega es una medición donde
antes había un cálculo de potencia: **con los datos abiertos que existen no se puede distinguir un
criterio útil de uno inútil**. Salvedad de encuadre: los dos conjuntos ya estaban citados en
`entregables/critica-herramientas.md`, así que es un reanálisis de una línea ya contada y no una nueva.
Resultados en `RESULTADOS_validacion_retrospectiva.md`.

**Fase 2 (diseño nuevo), resultado del 2026-10-22.** Veredicto **(b): viable sólo para 2 genes nominales**. De 14 familias del catálogo de C5, 11 tienen ortólogo recíproco por secuencia en el proteoma de *M. quadrilineatus*. De esas 11, sólo ATP synthase beta y actina muscular superan el criterio de nucleótido (≥ 300 nt con ≥ 90 % de identidad contra los TSA de *D. maidis*), y la actina es multigénica. Criterio en `research/ola3/C11_diseno_nuevo/criterio.md`; resultado en `research/ola3/C11_diseno_nuevo/REPORT.md`. Pendiente: el `tblastn` inverso desde *D. maidis* para confirmar la ortología del contig.

Lo demás que figura en `00_meta/PREGUNTAS_ABIERTAS.md` bajo «pendientes internos» son huecos
declarados que viajan con los números, no tareas del entregable.
