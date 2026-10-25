# Plan de la ola 4 — nueve líneas para implementar la respuesta del mentor

**Qué es.** El plan para ejecutar lo que Diego nos contestó el 22 de octubre de 2026 por
correo, en respuesta a las siete preguntas de `entregables/correo-investigador.md`. La carta
está transcripta y mapeada, punto por punto, en
`docs/plan_checkpoint2/salidas/F6_respuesta_y_cambios.md`, que es la salida de la Fase 6 Parte 2
del plan del checkpoint 2. Este archivo es lo que sigue: las líneas de trabajo, con sus tareas,
sus entradas y su criterio de terminado.

**Cuándo.** Hoy es jueves 22 de octubre. La reunión es el **lunes 26** («nos vemos el lunes»).
Quedan tres días y medio, y cuatro personas. El plan está ordenado por lo que llega al lunes y
lo que no: la sección «Mínimo viable antes del lunes» dice qué pasa si el tiempo no alcanza.

**Dónde van las salidas.** Las líneas son `M1` a `M9` y escriben en
`research/ola4/M<n>_<tema>/`, con la estructura que ya usan las olas 2 y 3 (`REPORT.md`,
`scripts/`, `resultados/`, `NOTAS_PARA_META.md`). Las decisiones van a `00_meta/DECISIONS.md`
como ADR; los descartes, a `CAMINOS_PROBADOS.md`; los pendientes, a `PREGUNTAS_ABIERTAS.md`.

**Nomenclatura de marcadores.** Se aplica `CLAUDE.md`. Dentro de este plan se agrega una
convención: una afirmación sobre lo que hace un fuente público, citada por archivo y línea
contra un commit declarado, va como `[R]` —es una fuente primaria que abrimos, no consenso de
literatura revisada—. Un número que salga de correr algo nuestro va como `[M]`. Lo que Diego
afirma en la carta va como `[R]`, y su carta es la fuente.

---

## 1. Lo que la carta cierra

Tres cosas quedan cerradas, y las tres eran preguntas nuestras de hace tres días.

**La configuración está declarada.** Los conteos de la planilla salen de la corrida identificada
como `siFi21_8_1.0_0.1_1111`, con el umbral de estabilidad de extremos en **1,0** y no en 1,75
`[R]`. Ese nombre se decodifica contra el fuente original: `main.py:344-362`
(`set_design_settings`) fija, en modo diseño, ventana de accesibilidad `xmer` = 8, umbral de
extremos = 1, corte de accesibilidad = 0,1 y las cuatro casillas de verificación en verdadero
—`checkBox_end`, `checkBox_access`, `checkBox_strand`, `checkBox_terminal`— `[R]`. El `1111` es
legible sin ambigüedad justamente porque las cuatro están activas: no hace falta saber en qué
orden las serializa el nombre. Conclusión: **es el modo diseño con los valores por defecto**.

**Nuestra hipótesis del 1,75 se cae como explicación.** No como medición: el barrido de 22.176
configuraciones sigue diciendo que el punto `RNA_NN3`, 22 °C, u = 8, extremos 1,75,
accesibilidad 0,1, regla terminal activa da 117, 35, 199 y 32 contra los 114, 35, 199 y 33
declarados, con dos valores exactos y un error total de 4 `[M]`
(`research/ola3/C2_codigo_apolo_inta/corridas/05_barrido_22176_configs.json`). Lo que se cae es
la lectura causal: el laboratorio no movió ese umbral, así que la cercanía es coincidencia de un
barrido grande, y no evidencia de haber encontrado su configuración. Queda registrado como
descarte en `CAMINOS_PROBADOS.md` y como ADR D45.

**La columna es «eficientes», no «eficientes sin off-targets».** Los números de la planilla son
los predichos como eficientes en el análisis de diseño; la evaluación de off-targets la hacen
por separado `[R]`. Eso cierra la segunda mitad de nuestra pregunta 1 y descarta la hipótesis de
que 114, 35, 199 y 33 fueran la segunda columna de `sifi21INTA` (`getResultSummary`,
`SifiPipeline.py:430-448`), que es la que depende de la base y del blanco principal elegido a
mano.

## 2. Lo que la carta no contesta, y conviene no fingir que sí

De las siete preguntas del correo, Diego contestó una (la 1, en sus dos mitades) y reencuadró el
resto como método. Siguen sin respuesta, y son para el lunes: por qué la región de `MP_MRFV` es
1–200 (pregunta 2), qué transcriptoma de *Dalbulus maidis* usan y si lo comparten (3), qué pesos
le daría a cada criterio y cuánto pesa un hemíptero no objetivo frente al maíz (4), si les
interesa matar o esterilizar (5), de dónde sale el rango de 150 a 250 nt (6) y las dos de BLAST
(7). La pregunta 4 la movió a terreno de método —separar exposición de conservación— pero no dio
números, y la 5 la dejó abierta.

Además nos preguntó dos cosas, que la línea M0 contesta hoy: de dónde sacamos `sifi21INTA`, con
enlace y versión exacta, y conocer nuestro port.

## 3. El hallazgo que reordena el plan

Diego escribió: «convendría verificar que las implementaciones utilicen exactamente las mismas
secuencias, orientación, **referencias** y criterios de contabilización». Siguiendo esa pista
hasta el fuente apareció algo que no habíamos mirado.

**La columna «Efficient siRNA hits» del original no cuenta ventanas: cuenta aciertos de Bowtie.**
En `general_helpers.py:107-123`, `get_table_data` arma la tabla con
`Counter(player['hit_name'] for player in query if player['is_efficient'])`: un registro por
**acierto**, agrupado por el nombre de la referencia contra la que pegó `[R]`. Y en
`sifi_pipeline.py:195-221` hay dos caminos para construir el registro: si hay acierto de Bowtie,
`hit_name` es el nombre de la referencia; si no hay acierto, `hit_name = False` y `strand = None`,
y como todo el bloque de eficiencia está dentro de `if strand == '+'`, esa ventana **nunca se
evalúa** `[R]`.

De ahí salen tres consecuencias que ninguno de nuestros barridos podía capturar, porque no son
parámetros:

1. Una ventana eficiente que **no pega** en la referencia elegida no entra al conteo.
2. Una ventana que pega sólo en la hebra menos no entra tampoco, porque la eficiencia se calcula
   únicamente para aciertos en `+`.
3. Una ventana que pega **dos veces** en la misma referencia cuenta dos veces. Que eso pasa está
   medido: en `BicC_Dm`, Bowtie reporta 2.504 aciertos para 2.500 ventanas `[M]`
   (`research/ola3/C2_codigo_apolo_inta/diff_sifi21INTA_vs_original.md`, fila 3).

Esto explica la forma del desajuste, que ningún umbral explicaba. Contra las mismas secuencias,
el original con sus valores por defecto da 133, 32, 212 y 42 ventanas eficientes y la planilla
declara 114, 35, 199 y 33: **baja en tres genes y sube en uno** `[M]`. Un umbral más estricto
sólo puede bajar; un conteo por acierto contra una referencia distinta puede mover en los dos
sentidos. La hipótesis es que la planilla cuenta aciertos contra la base que el laboratorio usó
—probablemente su transcriptoma de *D. maidis* para los dos genes del insecto y alguna
referencia de MRFV para los dos virales—, y que las ventanas que no pegan en esa base se
perdieron del conteo mientras que las que pegan más de una vez se contaron de más `[H]`.

Es importante ser claro sobre el estatus: la decodificación del nombre y la lectura del fuente
son `[R]`; que eso **sea** la causa del desajuste es `[H]` hasta que M1 lo mida. Lo que sí está
cerrado es que las dos implementaciones **no cuentan lo mismo** —`sifi21INTA` cuenta una fila por
ventana (`SifiPipeline.py:430-448`)— y por lo tanto comparar 133 contra 114 fue, desde el
principio, comparar dos unidades distintas.

Conviene registrar también lo que ya está verificado del lado de las secuencias, porque es la
primera de las cuatro cosas que Diego pide verificar y está hecha: los cuatro largos de la
planilla son 1.263, 528, 2.520 y 491 nt, lo que da 1.243, 508, 2.500 y 471 ventanas de 21 nt, y
el volcado del propio programa original declara 471 aciertos totales para `ATPaseD_Dm_full`
(`research/ola2/W5_secuencias_epilab/analisis/sifi21_original_ATPaseD.csv`) `[M]`. Mismas
secuencias, mismo largo, misma orientación de entrada. El alfabeto es ACGT en mayúsculas en los
cuatro, así que la trampa de las minúsculas —que da 0 eficientes sin un solo aviso— no está
actuando `[M]`.

## 4. Las nueve líneas

| # | Línea | Qué resuelve de la carta | Día | Depende de | Cómputo | Decide el usuario |
| --- | --- | --- | --- | --- | --- | --- |
| M0 | Cierres, ADR y respuesta a sus dos preguntas | — (higiene) | jue 22 | — | no | qué se envía |
| M1 | Reconciliación de conteos por referencia y unidad de conteo | §2 | jue 22 / vie 23 | M0 | sí, medio | no |
| M2 | Comparador ventana por ventana | §2 | vie 23 | M1 | sí, poco | no |
| M3 | Tercera vía: términos continuos sin corte | §1 | sáb 24 | — | sí, poco | no |
| M4 | Qué evidencia distinguiría los dos modelos, y cuánta hace falta | §1 | sáb 24 | — | sí, poco | sí |
| M5 | Separar exposición ecológica de señal de conservación | §3 | sáb 24 | — | sí, medio | **sí** |
| M6 | Del veto binario a la alerta justificada | §4 | sáb 24 | M5 | sí, medio | **sí** |
| M7 | Robustez de `BicC_Dm` 922–1221 en tres ejes | §5 | dom 25 | M5, M6 | sí, alto | no |
| M8 | Qué permite y qué no permite comparar el número de eficientes | §6 | dom 25 | — | no | no |
| M9 | Auditoría de secuencia antes de compartir el repo o el port | §2 (nos pidió el port) | jue 22 | — | sí, poco | **sí** |

M9 está el jueves y no al final a propósito: Diego pidió conocer el port, y no se comparte nada
hasta que la auditoría pase.

---

## M0 — Cierres, ADR y respuesta a sus dos preguntas

**Problema.** La carta cierra tres cosas y abre varias. Si no se registran hoy, el lunes
discutimos sobre un estado que ya no es el nuestro.

**Tareas.**
1. Escribir `docs/plan_checkpoint2/salidas/F6_respuesta_y_cambios.md` con la carta transcripta y
   la tabla de qué cambia. *(hecho)*
2. ADR D45 a D49 en `00_meta/DECISIONS.md`. *(hecho; D47, D48 y D49 esperan confirmación del
   usuario antes de que se toque un entregable)*
3. Descarte del 1,75 como explicación en `CAMINOS_PROBADOS.md`. *(hecho)*
4. Sección nueva en `PREGUNTAS_ABIERTAS.md`: tres cerradas, seis que siguen abiertas, las nuevas
   que abre la carta. *(hecho)*
5. Borrador de respuesta en `entregables/respuesta-al-mentor.md`, con las dos preguntas suyas
   contestadas y las seis nuestras repreguntadas para el lunes. **No se envía sin que el usuario
   lo confirme.**

**Las dos respuestas que él pidió, para que no haya que reconstruirlas:**

- `sifi21INTA` es `github.com/bioinformaticaInta/sifi21INTA`, commit
  `92df44494373551d86eb1aee1b72d82858c581b2`, cabeza de `main` al 2024-03-27, verificado con
  `git ls-remote`. El original con el que se comparó es `github.com/snowformatics/siFi21-`,
  commit `d6296b73c08a2176e9d0257e0a175278cff8c231`, cabeza de `master` al 2025-03-18. La
  comparación archivo por archivo está en
  `research/ola3/C2_codigo_apolo_inta/diff_sifi21INTA_vs_original.md`, con dieciocho diferencias
  y la medición de cuáles mueven un número.
- Nuestro port es `tools/sifi21_port/`: Python 3, sin interfaz, dos modos (`fiel` reproduce la
  rama terminal del original, `corregido` la aplica como filtro adicional), dos backends de
  accesibilidad (`exe`, el RNAplfold 2.1.5 que instala si-Fi21, y `vienna`, las ligaduras de
  ViennaRNA 2.7.2). Está verificado contra el original en los cuatro genes: 42, 32, 133 y 212
  para `ATPaseD_Dm`, `CP_MRFV`, `MP_MRFV` y `BicC_Dm`, los mismos cuatro números, y la curva del
  «RNAi design plot» reproducida tramo por tramo `[M]`
  (`research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md` §0). Los cambios respecto del
  original están uno por uno en `tools/sifi21_port/CAMBIOS.md`.

**Criterio de terminado.** Los cuatro archivos de `00_meta/` y de `salidas/` están escritos; el
borrador de respuesta existe y quedó aprobado para envío antes del lunes, pendiente de revisión del equipo (D50).

---

## M1 — Reconciliación de conteos: la referencia y la unidad de conteo

**Problema.** Con la configuración ya declarada, el desajuste entre 133/32/212/42 y
114/35/199/33 no puede atribuirse a un parámetro. La hipótesis es la unidad de conteo y la
referencia (§3). Hay que medirla, y hay que hacerlo de modo que el resultado sea interpretable
incluso si la hipótesis falla.

**Lo que ya hay.** El port con salida por ventana (`run_sifi.py --salida`, un TSV por gen con
`pos`, `ddg`, `accessibility` y los cuatro booleanos). Las seis bases de
`work/offtarget_db/` —genoma de *D. maidis* `GCA_975739785.1`, transcriptomas de *Folsomia
candida* `GCF_002217175.1`, de *Homalodisca vitripennis* `GCF_021130785.1`, de *Apis mellifera*
`GCF_003254395.2`, de *Harmonia axyridis* `GCF_914767665.1` y de maíz `GCF_902167145.1`—. Los 71
registros públicos de MRFV ya descargados y analizados en W5. Bowtie y BLAST+ locales.

> **Corrección del 2026-10-23, al correr la línea.** Este inventario tenía dos errores que
> importan para la tarea 2. Primero: `GCF_002217175.1` **no es** un transcriptoma de *D. maidis*
> sino de *Folsomia candida*, el colémbolo del panel de no objetivo; queda corregido arriba. En
> `work/offtarget_db/` hay **genoma** de *D. maidis* y **ningún transcriptoma** suyo, así que
> donde la tarea 2 dice «cada uno de los tres transcriptomas públicos de *D. maidis*» hay que
> leer «el único, que es la ensambladura TSA `GITV01` y hay que bajarla». Segundo: de los 71
> registros de MRFV, los que W5 dejó inventariados con número de acceso son **65**. Y una
> aclaración de disponibilidad: Bowtie y RNAplfold 2.1.5 vienen con el instalador de si-Fi2015,
> en `%LOCALAPPDATA%\siFi2015\`, así que no hacen falta instalaciones aparte.

**Lo que falta.** Un script que **implemente la regla de conteo del original** —un registro por
acierto de Bowtie en la hebra `+`, agrupado por nombre de referencia— y la aplique a cada gen
contra un conjunto de bases candidatas, informando el conteo por fila de la tabla, no por
ventana.

**Tareas.**
1. `research/ola4/M1_conteo_y_referencia/scripts/conteo_por_acierto.py`: toma el TSV por ventana
   del port y una salida de Bowtie (`-a -v 0`, y también `-v 1` como sensibilidad), y devuelve
   (a) el conteo por ventana, (b) el conteo por acierto en `+`, (c) el conteo por acierto en
   cualquier hebra, (d) cuántas ventanas eficientes no pegan y (e) cuántas pegan más de una vez.
   La prueba de que está bien implementado: contra una base que es el gen mismo, (a) y (b) deben
   coincidir y dar los números verificados del original.
2. Correr la matriz de bases por gen: el gen mismo; los 71 registros de MRFV; cada uno de los
   tres transcriptomas públicos de *D. maidis*; el genoma de referencia; y las uniones
   plausibles. Para cada celda, el vector de cuatro conteos y su distancia a (114, 35, 199, 33).
3. Control de orientación: repetir con el complemento reverso de cada gen y registrar los cuatro
   conteos. Es barato y descarta un eje que Diego nombra explícitamente.
4. Control de versión del motor de accesibilidad: el eje ya está barrido en dos puntos (2.1.5 y
   2.7.2) y mueve los conteos entre 9 y 11 por gen, que es del orden de la brecha que falta
   explicar `[M]`. Agregar al menos dos puntos intermedios (2.4.x y 2.6.x) **sólo si M1 no cierra
   con la referencia**; si cierra, el eje se declara como no necesario y se deja escrito.
5. Escribir el REPORT con el resultado, incluido el nulo: si ninguna base reproduce los cuatro
   números, eso se informa como tal, y la conclusión pasa a ser que el desajuste necesita un dato
   que no tenemos —su salida por ventana— y no otra corrida nuestra.

**Lo que hay que pedirle el lunes, y es lo que más rinde de toda la lista.** La salida por
ventana de su corrida `siFi21_8_1.0_0.1_1111`: el CSV de `Save as → Table` si usaron el original,
o el JSON de `sirnaData` / el HTML de Plotly si usaron `sifi21INTA`. Con eso la comparación es
exacta y la pregunta se cierra en una tarde. Sin eso, lo mejor que podemos hacer es acotar la
explicación, no verificarla. Y la pregunta hermana, que ahora sabemos que importa: **contra qué
base de Bowtie corrieron el diseño**, y qué fila de la tabla de resultados tomaron.

**Salida.** `research/ola4/M1_conteo_y_referencia/REPORT.md`, con la matriz de celdas, el
conteo de ventanas que no pegan y de las que pegan doble, y el veredicto.

**Criterio de terminado.** (a) El script reproduce los cuatro números verificados cuando la base
es el gen mismo. (b) Hay una tabla con una fila por base y los cuatro conteos. (c) Está dicho si
alguna celda reproduce (114, 35, 199, 33) y, si ninguna lo hace, cuál es la más cercana y qué
dato falta. (d) El control de orientación está corrido e informado.

**Qué cierra.** La pregunta 1 del correo, que llevaba tres semanas abierta, deja de ser «qué
parámetro movieron» y pasa a ser «qué referencia usaron», que es contestable.

---

## M2 — Comparador ventana por ventana

**Problema.** Diego lo pide literalmente: «sería útil comparar cuáles son las ventanas
específicas que cambian de clasificación, en lugar de considerar únicamente el conteo final». Hoy
tenemos esa comparación hecha a mano para un par de casos (la rama terminal, en `CAMBIOS.md` C1,
y el recorte contra el contexto, en C13 §4) y no tenemos la herramienta.

**Tareas.**
1. `research/ola4/M2_ventana_a_ventana/scripts/comparar_ventanas.py`: toma dos TSV por ventana
   del port y devuelve la matriz de confusión (eficiente/no por lado), la lista de posiciones que
   cambian de clase y, para cada una, **qué término cruzó el corte**: la brecha de ΔG, la
   probabilidad de apertura, o la rama de la regla terminal. Que diga el término es lo que lo
   hace útil: un conteo que cambia no dice nada, una ventana que cambia porque su accesibilidad
   pasó de 0,1158 a 0,0890 sí.
2. Aplicarlo a los cuatro pares que importan: `fiel` contra `corregido`; `RNA_NN3` contra
   `RNA_NN4`; RNAplfold 2.1.5 contra ViennaRNA 2.7.2; y región recortada contra región en
   contexto. Los dos últimos reconstruyen con herramienta lo que hoy está medido a mano, así que
   sirven de control: tienen que dar los números ya publicados (19, 7, 50 y 8 ventanas por el
   atajo de la regla terminal; 27 cambios de veredicto por borde en las cuatro regiones).
3. Dejar el comparador listo para el día en que llegue su salida por ventana. Es la misma
   herramienta.

**Salida.** `research/ola4/M2_ventana_a_ventana/REPORT.md` y un TSV por par.

**Criterio de terminado.** Los dos controles reproducen los números ya publicados. Cada par
tiene su matriz de confusión y su lista de posiciones con el término que cruzó.

---

## M3 — Tercera vía: los términos continuos, sin corte

**Problema.** Diego propone «conservar los valores termodinámicos, las preferencias terminales y
la accesibilidad como variables independientes del proceso de clasificación, para evaluar
posteriormente cómo contribuyen a la eficiencia». El ADR D26 ya nos obliga a publicar los
términos continuos, y está implementado **a medias**: el TSV por ventana trae `dg_sense5`,
`dg_antisense5`, `ddg` y `accessibility`, pero **no trae los dos nucleótidos de la regla
terminal** ni la rama que se aplicó. Falta justamente la variable que Diego quiere ver como
independiente.

**Tareas.**
1. Agregar a `Window` (`tools/sifi21_port/sifi_core.py:57-70`) las columnas `nt19`, `nt2` y
   `rama_terminal` (1 a 4, la de `sifi_pipeline.py:525-555`). Son dos letras y un entero: no
   reconstruyen secuencia, así que no chocan con la regla de confidencialidad —a diferencia de la
   columna `seq`, que se quita (ver M9).
2. Agregar `--features` a `run_sifi.py`, que emite la tabla sin ningún booleano: una fila por
   ventana con los seis términos continuos o categóricos y nada más. Ese archivo es el insumo de
   M4 y es lo que se le puede mostrar a Diego como «el tercer modelo»: no es un modelo todavía,
   es la tabla sobre la que se podría ajustar uno.
3. Escribir, y esto es lo importante, **por qué no ajustamos nada ahora**: con 29 etiquetas no se
   ajusta un modelo de seis variables. El plan de análisis queda preregistrado en M4 y se ejecuta
   cuando haya etiquetas.

**Salida.** El port actualizado, con su prueba en `test_sifi.py`, y
`research/ola4/M3_features/REPORT.md` con la tabla de los cuatro genes.

**Criterio de terminado.** `--features` corre en los cuatro genes; las columnas nuevas no
permiten reconstruir la secuencia (lo verifica M9); está escrito que la tabla no es un modelo.

---

## M4 — Qué evidencia distinguiría los dos modelos, y cuánta hace falta

**Problema.** Diego: «tampoco asumiría todavía que esa modificación mejora la predicción de
eficiencia. Sería interesante conservar ambos modelos y pensar qué evidencia experimental
permitiría compararlos». Eso ya lo intentamos y el resultado fue nulo, lo cual es una respuesta
mejor que una opinión: la validación retrospectiva preregistrada contra *Tribolium castaneum*
(Cedden *et al.* 2025) da ρ = +0,142 con IC95 [−0,247, +0,492] para el modo fiel y ρ = +0,024
[−0,356, +0,397] para el corregido, n = 29 `[M]`
(`research/ola3/C9_sensibilidad_umbral/resultados/validacion_resumen.json`). Con los datos
abiertos que existen **no se distingue un criterio bueno de uno inútil**, y menos dos criterios
que difieren en una rama.

**Tareas.**
1. Calcular la **potencia**: cuántos siRNA con eficacia medida hacen falta para distinguir
   ρ = 0,14 de ρ = 0,02 en una comparación de dos correlaciones dependientes (los dos modelos se
   evalúan sobre las mismas ventanas), con α = 0,05 y potencia 0,8. Hacerlo por remuestreo sobre
   los datos de Cedden, que es más honesto que una fórmula asintótica con n = 29. El número que
   salga es la respuesta cuantitativa a su pregunta.
2. Inventariar las fuentes de etiquetas posibles, con lo que cada una cuesta en validez externa:
   Cedden 2025 (28 ARNdc y 29 siRNA, coleóptero, lo que ya usamos); los conjuntos públicos
   grandes de siRNA en células humanas, que dan n de tres dígitos pero cambian de reino, de
   maquinaria y de vía de entrega, y por lo tanto entran como `[?]` y sólo para medir si los
   términos tienen alguna señal; y lo que haya en hemípteros, que hasta donde buscamos es nada.
   Cada fuente va con su identificador y su licencia, y ninguna se cita sin abrirla.
3. Diseñar el **ensayo prospectivo mínimo que discrimina**, que es lo que Diego pregunta. La
   clave es que los dos modelos difieren en un conjunto identificable y ya contado: 19, 7, 50 y 8
   ventanas en `MP_MRFV`, `CP_MRFV`, `BicC_Dm` y `ATPaseD_Dm` son eficientes en modo fiel y no en
   corregido, y **ninguna va en el sentido contrario** `[M]` (`CAMBIOS.md` C1). Entonces el
   ensayo no necesita medir siRNA al azar: necesita medir siRNA **discordantes** contra siRNA
   **concordantes-eficientes** y contra un control negativo, sobre un gen, con el silenciamiento
   del transcrito como variable de respuesta. Si los discordantes silencian como los
   concordantes, la rama del original no infla nada y nuestro modo corregido está descartando
   diseños buenos; si no silencian, la rama infla y la corrección vale. Entregar el diseño con su
   tamaño de muestra (del punto 1), su ciego y su resultado que cambiaría la interpretación. **El
   ensayo lo propondríamos; no lo corremos nosotros: no tenemos laboratorio.**
4. Preregistrar el análisis de la tercera vía de M3: qué modelo, qué validación cruzada, qué
   medida de contribución, decidido antes de ver datos.

**Salida.** `research/ola4/M4_evidencia_y_potencia/REPORT.md`.

**Decide el usuario.** Si el diseño del punto 3 entra al entregable del checkpoint como la
casilla de validación. Es el candidato más fuerte que tenemos para esa casilla.

**Criterio de terminado.** Hay un número de tamaño de muestra con su método; hay una tabla de
fuentes de etiquetas con identificador y limitación; hay un diseño de ensayo discriminante con
su endpoint y su resultado falsador.

---

## M5 — Separar exposición ecológica de señal de conservación

**Problema.** Diego, sobre *Homalodisca vitripennis*: «mantendría esa información, pero
separaría el riesgo de exposición ecológica de la señal de conservación de secuencia. No
necesariamente deberían tener el mismo peso en la decisión final». Hoy las dos cosas están
colapsadas en un solo número: el ADR D18 le da a *H. vitripennis* un peso de riesgo de 0,60 en
la misma escala en la que el maíz vale 1,00 y *Folsomia candida* 0,40, y ese peso cumple las dos
funciones a la vez.

**Lo que hay que mirar antes de tocar nada.** Esto no es un refactor cosmético. El veto de
`ATPaseD_Dm` que sostiene el desempate del tercer puesto viene de tres coincidencias perfectas
con *H. vitripennis* en 392–394 `[M]`
(`research/ola3/C9_sensibilidad_umbral/REPORT.md`, T1 bis). Si *H. vitripennis* deja de pesar
como exposición —y no debería pesar, porque no está reportada en la Argentina—, **ese veto se
debilita y el empate entre `ATPaseD_Dm` y `CP_MRFV` vuelve a abrirse**: era un empate práctico,
invertido en el 47,4 % y el 48,9 % de la grilla, y lo que lo había resuelto era precisamente el
veto. Hay que decirlo en voz alta antes de implementarlo, porque es una consecuencia que nos
quita una conclusión.

**Tareas.**
1. Partir el vector de pesos de `pipeline/region_scoring.py` en dos, con nombres distintos y sin
   ninguna operación que los mezcle: `w_exposicion`, por probabilidad de contacto real con la
   formulación en la Argentina, y `s_conservacion`, por informatividad filogenética sobre cuán
   conservada está la región entre cicadélidos. *H. vitripennis* queda con exposición cercana a
   cero y conservación alta; el maíz, con exposición 1,00 y conservación nula (no es un
   cicadélido); los enemigos naturales y el polinizador, con exposición alta y conservación nula.
2. Reportar **dos números por región** y prohibir en el código que se combinen en uno. Que la
   decisión final los pondere es del usuario o de Diego, no del motor.
3. Rehacer el ranking v2 con los dos ejes y publicar qué cambia, incluido el reabrirse del tercer
   puesto. Si el orden de los dos primeros aguanta —y la expectativa es que sí, porque D17 ya
   había medido que el eje que ordena es la eficacia y no la limpieza—, decirlo con el número.
4. Dejar escrito el riesgo que la separación introduce: *H. vitripennis* es plaga cuarentenaria.
   Darle exposición cero hoy es correcto y es una apuesta sobre que siga ausente. Eso va como
   `[H]` y con su contracara, que es lo que `CLAUDE.md` pide de toda propuesta.

**Salida.** `research/ola4/M5_dos_ejes/REPORT.md`, el `pipeline/` modificado con su prueba, y el
ranking rehecho.

**Decide el usuario.** Los valores de `w_exposicion`. Y si el tercer puesto se reporta como
empate declarado —que es lo que la medición sostiene— o se sigue ordenando.

---

## M6 — Del veto binario a la alerta justificada

**Problema.** Diego confirma nuestra posición conservadora y nos corrige la consecuencia. Nos
confirma el ADR D17: «evaluamos la identidad de secuencia de los posibles off-targets
independientemente de que esas ventanas sean clasificadas como siRNAs eficientes», porque «una
predicción negativa de eficiencia no garantiza que un siRNA carezca de actividad biológica».
Pero nos corrige lo que hicimos con eso: «no trataría todas las coincidencias de 21 nt como
equivalentes ni las convertiría automáticamente en un veto ecológico universal. Sí las
conservaría como alertas fuertes que deben ser consideradas y justificadas».

**Tareas.**
1. Reemplazar la compuerta booleana por una tabla de alertas, `alertas.tsv`, con una fila por
   coincidencia y los cuatro campos que Diego enumera, explícitos y obligatorios: **qué
   organismo**, **su posibilidad de exposición**, **qué gen está involucrado** y **qué evidencia
   biológica hay**. Una fila sin esos cuatro campos es un error de validación, no una fila con
   celdas vacías.
2. La región no se descarta por tener alertas: se descarta, o se acepta, con una justificación
   escrita que cita la fila. El cambio no es de severidad, es de carga de la prueba: antes el
   motor decidía, ahora el motor obliga a argumentar.
3. Mantener los dos umbrales que ya están decididos en D28 —21/21 perfecto y bloque perfecto— y
   reportar los dos por alerta.
4. Reconstruir el estado de las cuatro regiones vigentes bajo la regla nueva, y decir cuáles
   vuelven a estar sobre la mesa. La región más conservada de `ATPaseD_Dm`, 137–436, estaba
   vetada y es la primera candidata a volver (D25, alternativa b).

**Salida.** `research/ola4/M6_alertas/REPORT.md` y `alertas.tsv` por región.

**Decide el usuario.** Qué alertas se aceptan con justificación y cuáles siguen siendo
bloqueantes. El motor ya no lo decide.

---

## M7 — Robustez de `BicC_Dm` 922–1221 en tres ejes

**Problema.** Diego: «antes de considerarla superior a la original, sería importante comprobar la
robustez de esa ventaja frente a los parámetros del modelo, la referencia utilizada y los
criterios de riesgo». Son tres ejes y hoy tenemos el primero, parcialmente.

**Tareas.**
1. **Parámetros.** La grilla de C9 —21 brechas de 0,0 a 2,0 por 26 accesibilidades de 0,05 a
   0,30, los dos modos— aplicada a la elección de región de `BicC_Dm`, comparando 922–1221 contra
   2121–2420 (la de C7) y contra **264–563, que es la que eligió el laboratorio**. Esa tercera
   comparación falta y es la que a él le interesa. Agregar `RNA_NN3` contra `RNA_NN4` como cuarto
   eje de la grilla.
2. **Referencia.** Recalcular eficiencia y coincidencias con cada uno de los tres transcriptomas
   públicos de *D. maidis* y con el genoma de referencia como fuente de coordenadas, y decir si
   922–1221 sigue ganando. El ensamblado ONT de Córdoba se reporta y no entra al criterio, por
   D25.
3. **Criterios de riesgo.** Los dos umbrales de D28 y las dos reglas de D17 —conservadora y
   mecanicista— cruzados, bajo la regla nueva de alertas de M6.
4. Reportar el conteo **de la molécula recortada**, no el del gen: en contexto 922–1221 tiene 36
   ventanas eficientes y recortada tiene 26, y es la recortada la que se sintetizaría `[M]`
   (C13 §4). La cifra que publicamos tiene que ser la de la molécula.
5. Una sola tabla de salida: en qué fracción de las configuraciones 922–1221 le gana a 2121–2420
   y a 264–563, por cada eje y en conjunto.

**Salida.** `research/ola4/M7_robustez_bicc/REPORT.md`.

**Criterio de terminado.** La fracción está calculada por eje y en conjunto; la comparación
contra 264–563 existe; la cifra publicada es la de la región recortada.

---

## M8 — Qué permite y qué no permite comparar el número de eficientes

**Problema.** Es su pregunta final, y es la más interesante: «¿hasta qué punto el número de
siRNAs eficientes predichos permite comparar estrategias dirigidas a genes diferentes? ¿Qué
otras variables biológicas incorporarían?». No necesita cómputo nuevo: necesita que escribamos
lo que ya medimos, ordenado como respuesta.

**Tareas.** Escribir el documento con cuatro límites medidos y una lista de variables.

Los cuatro límites, cada uno con su número ya existente:

1. **El conteo crudo no es comparable entre genes de largo distinto.** `BicC_Dm` tiene 2.520 nt y
   `CP_MRFV` 528: el primero tiene casi cinco veces más ventanas, así que un conteo mayor puede
   no significar nada. La unidad comparable es la densidad por 100 nt, o el conteo de la región
   de largo fijo que efectivamente se va a sintetizar.
2. **Depende de la referencia y de la unidad de conteo**, y eso es exactamente lo que M1 mide. Si
   la hipótesis de M1 se confirma, el mismo gen y la misma configuración dan conteos distintos
   según la base de Bowtie, lo que hace del número algo no comparable ni consigo mismo entre
   corridas.
3. **Depende de la versión del motor de accesibilidad**: entre RNAplfold 2.1.5 y ViennaRNA 2.7.2,
   con todo lo demás igual, los cuatro conteos se mueven de 133/32/212/42 a 142/39/223/35 `[M]`.
4. **El conteo en el contexto del gen no es el de la molécula recortada**: 38 baja a 27 en
   `MP_MRFV` y 36 baja a 26 en `BicC_Dm` `[M]` (C13 §4). Un cuarto del número.

Y lo que habría que incorporar, con lo que tenemos de cada cosa: evidencia de fenotipo tras
silenciamiento en la especie o en un pariente, que es lo único que conecta el diseño con el
efecto buscado y que es el eje que nuestro ranking ya separa de la eficacia de diseño;
esencialidad del gen; nivel de expresión en el tejido que el ARNdc ingerido efectivamente
alcanza; redundancia por parálogos, porque silenciar un miembro de una familia puede no hacer
nada; recambio de la proteína, que fija cuánto tarda el efecto; estadio de desarrollo en que se
expone el insecto; y, la que manda para nuestro objetivo, la **ventana de latencia del patógeno**
contra el tiempo hasta el efecto: si el insecto transmite antes de morir, matarlo no corta la
transmisión, y esa comparación es la que decide si esterilizar alcanza. Cada una va con qué
tenemos y qué nos falta, y lo que falta va a `PREGUNTAS_ABIERTAS.md`.

**Salida.** `research/ola4/M8_que_compara_el_conteo/REPORT.md`, y de ahí un párrafo a la casilla
de validación del entregable del checkpoint.

---

## M9 — Auditoría de secuencia antes de compartir el repo o el port

**Problema.** Diego pidió conocer el port. El port está en el repositorio, y el repositorio tuvo
ya un incidente: en C9 se commitearon TSV con una columna `seq` de 21-meros solapados de a 1 nt,
de los cuales **dos de los cuatro genes son de EPILAB** y la concatenación reconstruye el gen
entero. Se detectó revisando el diff antes de pushear y se reescribieron los tres commits
locales. La herramienta que lo evita existe pero es local a una línea de investigación:
`research/ola3/C9_sensibilidad_umbral/scripts/limpiar_ancla.py`.

**Tareas.**
1. Promover esa verificación a `tools/verificacion/sin_secuencias.py`, que recorra **todo el
   árbol versionado** buscando rachas de nucleótidos de 21 o más y las informe con archivo y
   línea, con una lista de excepciones declarada para lo que sí es público (los 28 ARNdc de
   Cedden, por D41).
2. Correrla sobre el árbol completo y sobre `git log -p` del historial, no sólo sobre el estado
   actual: un dato que estuvo en un commit sigue estando.
3. Dejarla como gancho de pre-commit.
4. Recién después, decidir cómo se comparte el port: repositorio privado con acceso, o un paquete
   con `tools/sifi21_port/` y nada más. **La recomendación es la segunda**, porque el port es
   autocontenido y no arrastra ni `work/` ni los resultados derivados de las secuencias de
   EPILAB. Y queda pendiente lo que el ADR D32 dejó sin resolver: la licencia del original está en
   conflicto entre el artículo (CC BY-SA 4.0) y SourceForge (CC BY-NC 2.0) `[?]`, de modo que
   redistribuir un derivado tiene una pregunta de licencia que conviene hacerle a él, que lo usa.

**Decide el usuario.** Cómo y por qué canal se comparte. Es una acción hacia afuera y no se hace
sin confirmación.

**Criterio de terminado.** La verificación corre sobre el árbol y sobre el historial y da cero
hallazgos no exceptuados, o los hallazgos están listados y resueltos.

---

## 5. Mínimo viable antes del lunes

Si el tiempo no alcanza —y con tres días y medio es probable que no alcance para las nueve—, el
orden de prioridad es este, y está elegido por cuánto mejora la conversación del lunes y no por
cuánto trabajo representa:

1. **M0**, que es higiene y ya está hecho. Sin esto llegamos al lunes afirmando cosas que su
   carta corrigió.
2. **M1 hasta el punto 2**, aunque sea con dos o tres bases y no con la matriz completa. Es la
   pregunta que él mismo dejó abierta y la que más nos cambia el estado. Y si no cierra, el
   resultado útil es saber exactamente qué pedirle.
3. **M8**, que no necesita cómputo y contesta su pregunta final. Llegar el lunes con una
   respuesta escrita a la pregunta que nos dejó para pensar vale más que una corrida más.
4. **M9 hasta el punto 2**, porque le prometemos el port y no se comparte antes de la
   verificación.
5. **Los seis pedidos del lunes**, que están en M0 y en el borrador de respuesta, y que son lo
   único que desbloquea M5, M7 y la mitad de lo que falta.

M5 y M6 **conviene no apurarlos antes de la reunión**, aunque sean los que más cambian el
resultado: los dos requieren decisiones del usuario, los dos tocan el ranking que ya está
entregado, y M5 además nos quita una conclusión (el desempate del tercer puesto). Hacerlos a las
apuradas el domingo es la forma de llegar el lunes con un ranking nuevo y a medio justificar. Es
mejor llegar con el análisis de qué cambiarían y la decisión tomada con él en la reunión.

## 6. Los seis pedidos del lunes, en orden de cuánto desbloquean

1. **La salida por ventana de su corrida** `siFi21_8_1.0_0.1_1111`, y contra qué base de Bowtie
   la corrieron. Cierra M1 y M2 de una vez.
2. **El transcriptoma de *D. maidis***. Desbloquea la conservación de `eth` y `burs-alpha`, que
   son los dos genes con evidencia funcional publicada que entraron al ranking y que ningún
   transcriptoma público que usamos contiene, y es también la referencia que M7 necesita.
3. **Matar o esterilizar.** Ordena el ranking de otra manera y es la decisión que la Fase 3 dejó
   marcada como suya.
4. **El peso de un hemíptero no objetivo frente al maíz**, ahora reformulado por su propia carta:
   no un peso, sino los dos pesos —exposición y conservación— de M5.
5. **Por qué la región de `MP_MRFV` es 1–200.** Sigue sin contestar y es lo que decide si la
   crítica de la región se sostiene o se reformula.
6. **La licencia del original** y de dónde sacar la versión que ellos usan, que es lo que M9
   necesita para poder compartir el port sin una pregunta abierta.

   > **Precisión del 25 de octubre, y acota el pedido.** si-Fi21 **no es una herramienta del
   > corpus**: lo que `YHat-Biotech/Links de interes.docx` entrega bajo «Herramientas de diseño
   > y verificación de off targets» son dsRNAEngineer y el BLAST del NCBI, y nada más (W2
   > REPORT, encabezado). A si-Fi21 llegamos nosotros, por Cedden 2026 y Lück *et al.* 2019, y
   > `tools/sifi21_port/` es un derivado nuestro de software de terceros que elegimos nosotros.
   > Consecuencia práctica: **mostrarle el port a Diego no depende de la licencia** —enseñarle
   > el código a un colega no es redistribuir, y ninguna de las tres declaraciones lo prohíbe—,
   > así que eso puede hacerse apenas se elija el canal. La licencia pesa recién cuando el port
   > se **publica**: el entregable del Investigathón, un repositorio público o cualquier cosa
   > que quede disponible para terceros. El pedido del lunes sigue en pie, pero como consulta a
   > quien usa la herramienta, no como permiso que necesitemos de él.

## 7. Riesgos de este plan

- **M1 puede no cerrar.** Si ninguna base reproduce los cuatro números, el plan no da una
  explicación sino una cota. Eso es un resultado y se informa como tal; lo que no se hace es
  seguir barriendo parámetros hasta que algún punto coincida, que es el error que ya cometimos con
  el 1,75.
- **M5 nos quita una conclusión.** Está dicho arriba y conviene no descubrirlo el domingo.
- **M4 puede concluir que el número de etiquetas necesario es inalcanzable** con datos públicos.
  Si es así, la respuesta a Diego es que los dos modelos no son distinguibles con la evidencia
  existente y que hace falta el ensayo prospectivo, lo cual es una respuesta y no un fracaso.
- **La tentación de este plan es el cómputo.** Siete de las nueve líneas piden correr algo, y la
  que más rinde —M8— no pide nada. El riesgo es llegar al lunes con tablas nuevas y sin la
  respuesta escrita a su pregunta final.
