# Fase 6 — Ensayar el checkpoint e incorporar la respuesta del investigador

| | |
| --- | --- |
| **Día sugerido** | lunes 26 oct (antes de la reunión) y de nuevo cuando llegue la respuesta |
| **Depende de** | Fases 4 y 5 para el ensayo; no depende de nada para la parte de la respuesta |
| **Necesita cómputo** | sólo si la respuesta lo exige (ver tabla) |
| **Decide el usuario** | qué cambios de la respuesta se aplican |
| **Produce** | `docs/plan_checkpoint2/salidas/F6_ensayo_preguntas.md` y, tras la respuesta, `F6_respuesta_y_cambios.md` |

**Para empezar:** abrí una sesión nueva sobre el repo y pedile: «Leé `docs/plan_checkpoint2/FASE_6_ensayo_y_respuesta.md` completo y ejecutá esa fase». Todo el contexto está en este archivo.

## Contexto común (el mismo en las seis fases)

**Quiénes somos.** Equipo de 4 estudiantes de Ingeniería en IA (UdeSA) en el Investigathon de Y-Hat (UBA), track de la chicharrita del maíz (*Dalbulus maidis*) y los patógenos que transmite, con ARN exógeno (RNAi). No tenemos laboratorio: aportamos bioinformática, datos y desarrollo computacional. El investigador que nos orienta es del EpiLab (IFIBYNE, UBA-CONICET). Repo: `chicharrita-research/` (dentro de `/Users/joaquin/Documents/investigaton/`).

**Qué pasó hasta acá.**
- En el checkpoint 1 (`research/checkpoints/checkpoint1.md`) el investigador pidió cinco cosas: entender si-Fi21, benchmark de si-Fi21 / dsRNA-Engineer / BLAST sobre sus cuatro genes, un ranking con criterio explícito, evaluar las regiones elegidas y una crítica de las herramientas. Los cinco están entregados, más los dos opcionales (ver `PLAN_DESARROLLO.md` §1 bis y `estado.html`).
- Dijo que el criterio de evaluación es **el razonamiento, no el acierto**, y que las bacterias quedan fuera (el RNAi no opera en ellas). Validó dos estrategias, insecto o patógeno en la planta, y recomendó la del insecto por directa. Sus cuatro diseños (planilla) tienen unos dos años y nunca se testearon (ADR D36: es una auditoría, no una reproducción).
- El entregable principal es `entregables/para-el-investigador.md` (con `.html`). Documentos de apoyo: `entregables/que-significa-eficiente.md` y `entregables/critica-herramientas.md`. **El correo al investigador ya se envió** (lo confirmó el usuario); ya no hay bloqueo por apellido o dominio. El borrador del repo, `entregables/correo-investigador.md`, tiene siete preguntas y `para-el-investigador.md` también las lista como siete, pero `PLAN_DESARROLLO.md` §8 todavía habla de cinco (texto desactualizado, a corregir en la Fase 5). **No se sabe cuántas ni cuáles tenía el correo realmente enviado:** pedirle al usuario el texto enviado antes de depender de la numeración.
- El 21 oct el investigador mandó dos documentos nuevos, que están en la raíz del repo: `Guia_Checkpoint2_Estudiantes.pdf` y `Fichas_Optativas_Estudiantes_v3.pdf`. Son la base de este plan. **Hay una auditoría del entregable contra ellos**: `docs/auditoria_guias_checkpoint2.md`.

**Qué piden las dos guías (resumen).**
- *Guía del checkpoint 2* (material orientativo para el **26 de octubre**): conversar siete elementos: (1) pregunta, (2) hipótesis con mecanismo y resultado predicho, (3) evidencia con procedencia e identificadores, (4) un avance propio, (5) alternativas, (6) validación (qué medirían, con qué controles, qué resultado cambiaría la interpretación), (7) dudas abiertas. «Una página o unas pocas diapositivas bastan»; valoran «una decisión razonada y una incertidumbre real». Regla: una coincidencia de secuencia, una puntuación o un resultado in silico es una hipótesis, no una prueba de eficacia. Las evidencias deben poder recuperarse.
- *Fichas optativas*: no es consigna evaluable. Tres tipos de entrega: Biología, Bioinformática accesible, Innovación experimental. Nuestro encaje es **Bioinformática accesible**. Piden distinguir «detectamos ARN» ≠ «entró a la célula correcta» ≠ «se generó siRNA funcional» ≠ «hubo efecto biológico». Tres rutas de preguntas: A eficacia mecanística, B formulación y entrega, C diseño experimental y riesgo. Piden razonar desde el organismo donde actúa el ARN (en el insecto es Dicer-2/AGO2; en la planta, rutas DCL/AGO distintas). No recomiendan dosis ni formulaciones, y nosotros tampoco.

**Resultados medidos que sostienen todo (verificá contra el archivo antes de citarlos).**
- Ranking: `MP_MRFV` > `CP_MRFV` > {`BicC_Dm`, `ATPaseD_Dm`}; los dos del insecto no se distinguen entre sí. Fuente: `research/ola2/W7_ranking/REPORT.md` y `research/ola3/C7_ranking_v2/`.
- El eje que ordena es la eficacia, porque la limpieza (off-target) casi no mueve el orden (factor 1,015–1,064 contra 2,38–2,50). Con otra escala (min-max) el orden modal cae de 98,7 % a 33,7 % y `MP_MRFV` pasa de primero a tercero.
- `MP_MRFV` no se puede evaluar por conservación: sólo 4 de 71 registros de GenBank cubren su región y dos son la referencia (`research/ola3/C8_conservacion/`).
- La región exacta de 200 nt es frágil: coincide con la de defecto en 11,7 % (modo fiel) y 25,8 % (corregido) de la grilla de umbrales; el candidato superior, en cambio, es robusto (99,1 % y 98,2 %) (`research/ola3/C9_sensibilidad_umbral/REPORT.md`). En `BicC_Dm` la región recomendada pasa a 922–1221.
- La condición de accesibilidad de si-Fi21 no mostró valor predictivo: OR 1,00 [0,89–1,12] sobre 300 siRNA humanos; en *Tribolium castaneum* (n = 29) HR 0,9994, P = 0,853.
- Validación retrospectiva pre-registrada, *Tribolium* (Cedden *et al.* 2025): ρ = +0,142, IC95 [−0,247, +0,492], n = 29, **no concluyente**; confirmatorio con 28 ARNdc: +0,236 [−0,161, +0,568]. Con los datos abiertos no se distingue un criterio bueno de uno inútil. Toda la validación es en un coleóptero; no hay validación en hemípteros.
- No existen datos de ARN pequeños virales ni para MRFV ni para *D. maidis* (`research/ola3/C10_vsirna_virus/`). El mapeo por homología se cerró como mapa de límites (ADR D37).
- Todo lo calculado por nosotros usa ViennaRNA 2.7.2 (no hay RNAplfold 2.1.5): los conteos absolutos no se comparan con los del programa original.

**Hallazgos de la auditoría (`docs/auditoria_guias_checkpoint2.md`) que esta fase continúa.**
1. El formato no es el que pide la guía: el entregable está organizado por «lo que pidieron», no por los siete elementos, y dura diez minutos de lectura.
2. Cubierto: evidencia, avance propio, dudas, mecanismo de hebra, seguridad. Parcial: pregunta, hipótesis, alternativas. **No cubierto: validación (Ruta C)** y casi nada de entrega (Ruta B).
3. **Tensión de coherencia:** el candidato número uno es viral, pero el investigador recomendó el insecto y las fichas piden explicar dónde y cómo actuaría el RNAi antiviral en maíz; eso no está discutido. **El ADR D34 ya había decidido** que el blanco es el insecto y que, donde las dos estrategias conviven, lo hacen como rankings separados con el criterio de comparación declarado (D20); los genes virales quedan en el ranking sólo como material de EPILAB a auditar. Lo que falta es que el entregable lo refleje: hoy presenta una lista única con `MP_MRFV` primero.
4. La etiqueta `[E]` figura junto a resultados in silico propios, y la guía dice que son hipótesis.

**Reglas permanentes del repo (`CLAUDE.md`).**
- Marcadores obligatorios: `[E]` establecido en literatura revisada, `[R]` reportado (una o pocas fuentes), `[H]` hipótesis nuestra, `[?]` incierto.
- **Prohibido citar una fuente que no abriste.** Si no pudiste abrirla, va a `00_meta/PREGUNTAS_ABIERTAS.md` como pendiente.
- Las secuencias de EPILAB no se suben a servicios web de terceros (ni BLAST web); análisis sólo local.
- Los originales del corpus no se tocan; se trabaja sobre copias en `work/`. Los papers se parafrasean.
- Todo número va con fuente y contexto (especie, n, tipo de ensayo). Prosa técnica en Markdown, en español, nombres científicos en itálica.
- Fuera de alcance: lo que aumente virulencia, transmisibilidad o rango de hospedadores, o apunte a dañar especies no objetivo. Toda propuesta lleva su contracara de riesgo.

**Convenciones de mantenimiento del repo.**
- Cada decisión nueva es un ADR en `00_meta/DECISIONS.md` (último: D37; la siguiente es D38) con fecha, decisión, alternativas, criterio y consecuencia. Lo descartado va a `00_meta/CAMINOS_PROBADOS.md`; lo pendiente, a `00_meta/PREGUNTAS_ABIERTAS.md`.
- Los entregables para el investigador viven en `entregables/`: el `.md` es la fuente de verdad y el `.html` autocontenido es la vista de lectura, generado con `python tools/md_a_html.py entrada.md salida.html` desde la raíz.
- `PLAN_DESARROLLO.md` declara el estado de cada pedido en **tres lugares** (tabla de los cinco pedidos, cobertura de §1 bis y cuerpo de cada tarea): al actualizar un estado hay que tocar los tres, o se contradice.
- `estado.html` se genera con `python tools/generar_estado.py`; la lista HECHO/FALTA está codificada en el script. No se edita a mano.

**Cómo trabajar esta fase.** Leé primero el archivo completo y los archivos de «Entradas». No hay fase que dependa de que se haya hecho otra sesión: si falta una salida de una fase anterior, la sección «Entradas» dice qué hacer. Al terminar, dejá la salida en la ruta indicada y declará en el archivo qué no se pudo hacer. Una afirmación que no pudiste verificar se marca `[?]` o `[H]`, no se redondea.

## Contexto específico de esta fase

**Dos partes independientes.**

**Parte 1: ensayo del checkpoint.** Anticipar las preguntas más difíciles que puede hacer el investigador y dejar la respuesta con la ruta de la evidencia. Lista inicial a completar (cada pregunta con su respuesta en tres líneas y el archivo de respaldo; si no hay respuesta, decirlo):
1. ¿Por qué `MP_MRFV` primero si el objetivo es el vector? (Fase 1; ADR D34: el objetivo es el insecto y los genes virales son material de EPILAB a auditar)
2. ¿Por qué no entrenaron un modelo? (`PLAN_DESARROLLO.md` §3 ter, opciones 6 y 7: los modelos entrenados en humano caen a AUC ≈ 0,50 al cambiar de ensayo; sin etiquetas en insecto)
3. ¿Cómo saben que el umbral de accesibilidad es 0,1? (no lo saben: convención; `entregables/que-significa-eficiente.md`, barrido C9)
4. ¿Qué dice la validación en *Tribolium* sobre *D. maidis*? (nada directo: coleóptero, no hemíptero)
5. ¿Cómo ensayarían primero? (Fase 3)
6. ¿Qué cambia si sólo esteriliza y no mata? (`tablero/orden.html`)
7. ¿Qué hay de los no objetivo? (`tablero/riesgo.html`: el riesgo está en cicadélidos emparentados)
8. ¿Por qué 21 nt? (`que-significa-eficiente.md` y ADR sobre 21/22)
9. ¿Por qué BLAST no encuentra off-targets? (C3: megablast con palabra 28 no puede sembrar 21 nt)
10. ¿Qué necesitan de nosotros para avanzar? (casilla 7 de la página)

**Parte 2: respuesta del investigador al correo ya enviado.** Cuando llegue, mapear cada respuesta a lo que cambia. Tabla de partida, armada con las siete preguntas del **borrador** `correo-investigador.md`; antes de usarla, cotejarla con el texto realmente enviado y ajustar filas y numeración:

| Pregunta del correo | Si contesta… | Qué se actualiza | ¿Cómputo? |
| --- | --- | --- | --- |
| 1. Modo de si-Fi21 y umbral de extremos | modo y valor | `tools/sifi21_port/`, `entregables/critica-herramientas.md` (sección de la planilla); ver si 1,75 reproduce 114, 35, 199 y 33 | sí, una corrida |
| 2. ¿Región 1–200 por off-targets o por densidad? | una razón | W7 §2.2; la crítica de la región | no |
| 3. Transcriptoma de *D. maidis* | cuál, y si lo comparte | `research/ola3/C11_conservacion_eth_bursa/` (medir conservación de `eth` y `burs-alpha`) | sí, búsqueda local |
| 4. Pesos y peso de un hemíptero no objetivo | números | `research/ola3/C7_ranking_v2/` (rehacer con sus pesos) | sí |
| 5. Matar o esterilizar | objetivo | orden por objetivo; endpoint de la Fase 3 | no |
| 6. Origen del rango 150–250 nt | fuente o ensayo | `que-significa-eficiente.md`, C6 | no |
| 7. BLAST: valores por defecto y «HCP» | cuál | `critica-herramientas.md`; C3 | no |

Cualquier respuesta que **contradiga** algo ya entregado se anota primero en `CAMINOS_PROBADOS.md` como corrección (qué se afirmaba, qué dijo él, qué evidencia hay de cada lado), y recién después se edita el entregable. El criterio de evaluación del investigador es el razonamiento, así que una corrección bien explicada suma.

## Entradas

- `entregables/checkpoint2-una-pagina.md` y `para-el-investigador.md`
- `entregables/correo-investigador.md` (qué se preguntó)
- El texto de la respuesta del investigador (pedirlo al usuario; no está en el repo)
- Los directorios de la tabla de la Parte 2, según lo que conteste
- `00_meta/CAMINOS_PROBADOS.md` y `DECISIONS.md`

## Tareas

1. Parte 1: armar el documento de preguntas anticipadas y completar cada respuesta con la ruta de evidencia verificada. Marcar las que no tengan respuesta.
2. Parte 1: proponer una agenda de cinco minutos para la conversación (qué decir primero; cuál es la decisión razonada; cuál la incertidumbre real; qué se le pide).
3. Parte 2 (cuando llegue la respuesta): pedirle el texto al usuario, pegarlo en `F6_respuesta_y_cambios.md` y completar la tabla de «qué cambia».
4. Parte 2: para cada respuesta que exija cómputo, reproducir primero el resultado anterior (para confirmar el entorno) y luego rehacerlo; informar lo que salga, incluidos los nulos.
5. Parte 2: aplicar sólo los cambios que el usuario confirme; escribir un ADR por cada decisión que cambie.

## Salidas

- `docs/plan_checkpoint2/salidas/F6_ensayo_preguntas.md`
- Tras la respuesta: `salidas/F6_respuesta_y_cambios.md` y los artefactos recalculados en el directorio correspondiente, con su README

## Criterio de terminado

- [ ] Las diez preguntas tienen respuesta con ruta o dicen «no sabemos».
- [ ] Hay una agenda de cinco minutos.
- [ ] Cada cambio por la respuesta del investigador está en una tabla y confirmado por el usuario.
- [ ] Lo recalculado se reprodujo antes de modificarse.
- [ ] Las contradicciones están documentadas en `CAMINOS_PROBADOS.md`.

## Qué no hacer

- No inventar la respuesta del investigador ni anticipar qué va a decir.
- No cambiar un entregable sin que el usuario confirme.
- No esconder una corrección: documentarla con la evidencia.
- No subir secuencias de EPILAB a servicios web si él comparte un transcriptoma: análisis local.

## Cierre de la sesión

- Cerrar en `PREGUNTAS_ABIERTAS.md` las preguntas contestadas y dejar las nuevas.
- Regenerar `estado.html` con `python tools/generar_estado.py` si cambió algo de HECHO o FALTA.
- Dejar escrito, al final de la salida, un apartado «Qué quedó sin hacer y por qué».

## Qué pasa a la fase siguiente

Fin del plan del checkpoint 2. Lo que surja de la reunión del 26 se planifica en un documento nuevo.
