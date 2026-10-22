# Fase 3 — Escribir hipótesis, alternativas y el esbozo de validación (elementos 2, 5 y 6)

| | |
| --- | --- |
| **Día sugerido** | viernes 23 oct |
| **Depende de** | Fase 1 (qué candidato y qué estructura) y Fase 2 (entrega); si no están, ver «Entradas» |
| **Necesita cómputo** | no |
| **Decide el usuario** | una cosa: matar o esterilizar como objetivo, si la respuesta del investigador aún no llegó |
| **Produce** | `docs/plan_checkpoint2/salidas/F3_hipotesis_alternativas_validacion.md` |

**Para empezar:** abrí una sesión nueva sobre el repo y pedile: «Leé `docs/plan_checkpoint2/FASE_3_hipotesis_alternativas_validacion.md` completo y ejecutá esa fase». Todo el contexto está en este archivo.

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

**El hueco principal.** El elemento 6 de la guía (qué medirían, con qué controles, qué resultado cambiaría la interpretación) y la Ruta C de las fichas (endpoint primario y secundario, grupo control que demuestre especificidad, verificación de dosis/exposición, variación biológica y tiempo de muestreo, qué resultado obligaría a descartar la propuesta) no tienen respuesta en el entregable. Lo único que tenemos es una validación **retrospectiva** en *Tribolium*, que es otra cosa. Las fichas también piden pensar «knockdown sin fenotipo» y «fenotipo sin knockdown», y no aparece en ningún lado del repo.

**Lo que el repo ya aporta a un diseño de ensayo.**
- **Antes de usar el nulo de región, leer W7 §1.1.** El «0 de 20 genes, ganancia mediana 7,2 %» (`baseline_dsrip/region_nulo_multigen.py`) mide la media de un puntaje biofísico y no el conteo de ventanas eficientes, y W7 lo concilia con la auditoría de regiones: no repetirlo como «la región no discrimina» sin esa aclaración. Lo que sí está medido es que la región exacta de 200 nt es frágil frente al umbral (11,7 % y 25,8 % de coincidencia con la de defecto). Un ensayo con dos regiones del **mismo** gen, la elegida por EPILAB y la recomendada (922–1221 para `BicC_Dm`), probaría de frente si «la región importa». Es coherente con la pregunta de las fichas: «¿por qué terminar en esa posición y no en otra?»
- Techo de reproducibilidad: dos ARN distintos contra el mismo gen, dentro de la misma fase, correlacionan 0,245 en datos publicados (`tablero/limites.html`; verificar la fuente antes de citarlo). Esto obliga a replicados biológicos y a no leer una diferencia chica como señal.
- Latencia de unos 20 días entre que la chicharrita adquiere el virus y puede transmitirlo: abre una ventana para actuar antes (argumento aceptado por el investigador en el checkpoint 1). El ensayo debe tener el tiempo de muestreo en cuenta.
- Candidatos con evidencia funcional en *D. maidis*: `eth` y `burs-alpha` (knockdown de 90 a 95 % en Andrada *et al.* 2026, con efecto sobre la muda). Una ATP sintasa β silenciada entre 5 y 46 veces en *Scaphoideus titanus* no afectó la supervivencia hasta los 14 días: un ejemplo medido de «knockdown sin fenotipo».
- Si el objetivo es matar o esterilizar cambia el endpoint; la pregunta 5 del correo enviado se lo preguntó al investigador. Si hay respuesta, usarla; si no, redactar las dos variantes.

**Estructura exigida del documento.**
1. **Pregunta** en una oración que conecte vector, virus y aplicación.
2. **Hipótesis** falsable: mecanismo + resultado predicho + condición bajo la cual fallaría (entrega, dsRNasas, maquinaria RNAi, redundancia del gen).
3. **Alternativas** (al menos tres): insecto contra virus en planta; matar contra esterilizar; otra explicación de que la accesibilidad no prediga (por ejemplo, que el ARN largo se procese distinto de un siRNA aislado, o que el desenlace sea demasiado ruidoso, que es lo que mide el techo de 0,245).
4. **Esbozo de validación**: endpoint primario (transcripto, RT-qPCR) y secundario (supervivencia o fecundidad); controles (ARN control no relacionado, vehículo solo, región alternativa del mismo gen, ARN blanco libre contra formulado si la Fase 2 lo respalda); medida de exposición e integridad; tiempos de muestreo; replicados; **tabla de interpretación**: «knockdown sin fenotipo», «fenotipo sin knockdown», «efecto del control», «sin efecto y ARN degradado» → qué concluiríamos y qué haríamos después; **criterio de descarte** escrito de antemano, al estilo del pre-registro de C9.
5. **Contracara de riesgo**: no objetivo (cicadélidos emparentados, polinizadores, maíz, humano), persistencia, resistencia (`tablero/riesgo.html`).

## Entradas

- `docs/plan_checkpoint2/salidas/F1_decision_ranking.md` y `salidas/F2_entrega_y_mecanismo.md`. **Si falta alguno**, usar `research/ola3/C7_ranking_v2/` y `research/ola2/W1_papers/REPORT.md`, declarar en el documento que la fase anterior no estaba y dejar los puntos que dependen de ella marcados `[?]`.
- `YHat-Biotech/Papers/finsc-6-1811933.pdf` (Andrada 2026): para los métodos de RNAi en *D. maidis*. Los controles y el gen de referencia que se nombren **tienen que salir de ahí o de otra fuente abierta**; si no están, `[?]`.
- `research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.md` (evidencia de silenciamiento por especie y fenotipo)
- `research/ola3/C9_sensibilidad_umbral/PREREGISTRO_validacion_retrospectiva.md` (modelo de cómo se escribe un criterio antes de mirar)
- `research/ola3/C8_conservacion/REPORT.md`, `tablero/riesgo.html`, `tablero/limites.html`
- Fichas, Ruta C y anexo; guía del checkpoint 2, elementos 2, 5 y 6
- `entregables/correo-investigador.md` (qué le preguntamos ya)

## Tareas

1. Verificar si el investigador ya contestó el correo. Si hay respuesta, pedirle al usuario el texto; si no, seguir con las variantes.
2. Redactar la pregunta (una oración).
3. Redactar la hipótesis con su condición de falla, `[H]`.
4. Redactar las alternativas (mínimo tres), cada una con la evidencia del repo que la hace razonable o débil.
5. Diseñar el esbozo de validación siguiendo la estructura, con cada control justificado por una fuente abierta o marcado `[?]`. Incluir la tabla de interpretación y el criterio de descarte.
6. Escribir la contracara de riesgo en un párrafo.
7. Revisar que no haya dosis, concentraciones, tiempos de aplicación ni formulaciones: las fichas dicen que no se recomiendan. Es un diseño conceptual.

## Salidas

- `docs/plan_checkpoint2/salidas/F3_hipotesis_alternativas_validacion.md`
- Pendientes nuevos en `PREGUNTAS_ABIERTAS.md` (por ejemplo, gen de referencia validado en *D. maidis*, si no se encontró en una fuente abierta)

## Criterio de terminado

- [ ] Están los cinco bloques: pregunta, hipótesis, alternativas (≥ 3), validación y riesgo.
- [ ] La hipótesis dice bajo qué resultado quedaría refutada.
- [ ] La tabla de interpretación incluye los cuatro casos de las fichas.
- [ ] Cada control tiene fuente o `[?]`.
- [ ] No hay dosis ni formulación.
- [ ] Todo lo propio está en `[H]` o `[M]` (según D39), no en `[E]`.

## Qué no hacer

- No inventar el gen de referencia, el ARN control ni los tiempos: salen de una fuente abierta o se marcan `[?]`.
- No calcular un tamaño de muestra sin una varianza de la fuente; mejor decir qué dato haría falta.
- No presentar el diseño como recomendación experimental: es una propuesta de diseño conceptual para discutir.
- No prometer que el ensayo validaría el filtro de si-Fi21; sólo puede acotar.

## Cierre de la sesión

- Anotar lo que se descartó (por ejemplo, un control que no tiene respaldo) en `CAMINOS_PROBADOS.md`.
- Si surge una decisión (por ejemplo, el candidato que se propone ensayar), un ADR D40.
- Dejar escrito, al final de la salida, un apartado «Qué quedó sin hacer y por qué».

## Qué pasa a la fase siguiente

La Fase 4 toma textualmente de acá las casillas 1, 2, 5 y 6. Dejar un resumen de cada bloque de máximo tres líneas al inicio del archivo.
