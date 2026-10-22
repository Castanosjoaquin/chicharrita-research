# Fase 2 — Entrega y mecanismo: media página con lo que las fuentes dicen (Rutas A y B)

| | |
| --- | --- |
| **Día sugerido** | jueves 22 o viernes 23 oct |
| **Depende de** | nada (puede correr en paralelo con la Fase 1) |
| **Necesita cómputo** | no; es lectura y redacción |
| **Decide el usuario** | no, salvo permisos de red si una fuente no abre |
| **Produce** | `docs/plan_checkpoint2/salidas/F2_entrega_y_mecanismo.md` (máximo una página) y actualización de `FUENTES.md` y `papers.json` |

**Para empezar:** abrí una sesión nueva sobre el repo y pedile: «Leé `docs/plan_checkpoint2/FASE_2_entrega_y_mecanismo.md` completo y ejecutá esa fase». Todo el contexto está en este archivo.

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

**El hueco.** Las fichas dedican su Ruta B y el anexo a la entrega: dónde se aplica el ARN, a qué compartimento debe llegar, qué falla primero (depósito, estabilidad, entrada en hoja, transporte vascular, ingestión, dsRNasas, entrada celular, maquinaria RNAi), cómo separar estabilidad química, captación y actividad biológica, y qué comparar (ARN libre, vehículo solo, ARN control). Nuestro entregable dice una sola línea: «la entrega oral es mucho más débil que la inyección en los datos que revisamos», y que no encontramos evidencia de que el ARN exógeno entre al floema.

**Dos rutas que las fichas piden discutir con el mentor.** Ruta insecto: ¿cómo llega el dsRNA a las células de *D. maidis* si se alimenta de savia?, ¿qué cambia si las dsRNasas lo degradan? Ruta virus: ¿puede un ARN aplicado a maíz llegar a los tejidos donde se replica MRFV, antes o después de la infección?

**Lecturas de las fichas y su estado en el repo (verificar al empezar; no asumir).**
- Rossi *et al.* 2024, entrega de dsRNA mediante hojas a chicharritas, doi:10.1007/s10340-023-01670-0: **el PDF está en el repo** (`YHat-Biotech/Papers/s10340-023-01670-0.pdf`; ya hay notas en `research/ola2/W1_papers/REPORT.md`).
- Mitter *et al.* 2017, arcillas LDH (BioClay), doi:10.1038/nplants.2016.207: **PDF en el repo** (`YHat-Biotech/Papers/nplants2016207 (1).pdf`).
- Andrada *et al.* 2026 (ETH y Burs-α en *D. maidis*), `YHat-Biotech/Papers/finsc-6-1811933.pdf`: PDF en el repo; sirve para los métodos de RNAi en la especie.
- Dalaisón-Fuentes *et al.* 2022 (doi:10.1002/ps.6937) y 2023 (doi:10.1016/j.pestbp.2023.105618): están en `00_meta/FUENTES.md`, pero la entrada de 2022 dice que se **citó a través de otra fuente**, y no hay PDF en el repo. Hay que abrirlos o declararlos no abiertos.
- Hoang *et al.* 2022, captación foliar de dsRNA, doi:10.3390/ijms23126639: **sólo aparece en archivos `sources.json`; no hay evidencia de que se haya leído.**
- Chen *et al.* 2025 (dsRNAEngineer, doi:10.1016/j.tibtech.2025.01.002): hay un preprint en `work/W2/dsRNAEngineer_preprint.pdf`, ya usado en la crítica de herramientas; la versión publicada no.
- Review de RNAi en insectos (2024), PMCID PMC10968014: procesamiento por Dicer, guía/pasajera y AGO2. Sin evidencia de apertura.

## Entradas

- Los tres PDF del repo citados arriba, desde `YHat-Biotech/Papers/` (leer copias en `work/`; el original no se toca)
- `research/ola2/W1_papers/REPORT.md` y `contradicciones.md` (notas previas sobre Rossi y Mitter)
- `00_meta/FUENTES.md` y `research/ola2/W1_papers/papers.json`
- `research/R1_fundamentos/REPORT.md` y `glosario_parcial.md` (dsRNasas, floema, mecanismo)
- `entregables/que-significa-eficiente.md` (la parte de Dicer-2, AGO2 y asimetría de hebra, que ya está cubierta)
- Fichas, pp. 1–3, en la raíz del repo

## Tareas

1. Abrir cada lectura y registrar en `papers.json` su estado: abierta completa, abierta sólo resumen, no abierta. Las no abiertas no se citan.
2. Para las que están en el repo (Rossi 2024, Mitter 2017, Andrada 2026): extraer, parafraseando y con el contexto experimental (especie, vía de entrega, ensayo, n), qué se midió y qué no. Distinguir en cada caso las cuatro cosas de la «regla de oro»: ARN presente, ARN en la célula correcta, siRNA funcional, efecto biológico.
3. Para Dalaisón-Fuentes 2022 y 2023, Hoang 2022 y PMC10968014: intentar abrirlas por los medios del repo (PMC y NCBI suelen estar disponibles). Si una está bloqueada, pedir acceso con la herramienta de permisos de red y esperar la respuesta del usuario; **no usar espejos ni copias de terceros**. Si no se puede abrir, registrarla en `PREGUNTAS_ABIERTAS.md` y seguir sin ella.
4. Responder en media página, sólo con lo abierto: (a) ¿qué célula recibe el ARN en el insecto y por qué ruta?, (b) ¿qué falla primero según lo medido?, (c) ¿qué cambia si hay dsRNasas?, (d) qué comparadores usan los estudios, (e) qué se sabe y qué no sobre el blanco viral en maíz. Lo que ninguna fuente abierta responda va marcado `[?]` y se convierte en pregunta abierta.
5. Dejar listo un párrafo de «qué implica esto para nuestra propuesta» (una idea por frase, marcado `[H]`) para que la Fase 3 lo use al escribir el riesgo de entrega.
6. Actualizar `00_meta/FUENTES.md` y `papers.json` con lo abierto.

## Salidas

- `docs/plan_checkpoint2/salidas/F2_entrega_y_mecanismo.md` (≤ 1 página, con tabla «fuente, contexto, qué se midió, qué no»)
- `FUENTES.md` y `papers.json` actualizados con el estado de apertura de cada lectura
- Entradas nuevas en `PREGUNTAS_ABIERTAS.md` por cada fuente que no se pudo abrir y cada pregunta sin respuesta

## Criterio de terminado

- [ ] Cada afirmación del documento tiene fuente abierta, con su rótulo `[E]`, `[R]`, `[H]` o `[?]`.
- [ ] Ninguna cita proviene de una lectura no abierta.
- [ ] Quedó explícito qué se sabe del blanco viral en maíz y qué no.
- [ ] No hay dosis, concentraciones ni formulaciones recomendadas.
- [ ] El documento cabe en una página.

## Qué no hacer

- No reconstruir de memoria el contenido de Hoang, Dalaisón ni del review: si no se abrió, no se cita.
- No usar sitios espejo ni servicios de terceros para sortear un bloqueo.
- No subir ninguna secuencia de EPILAB a ningún servicio.
- No convertir esto en revisión bibliográfica larga: son cinco preguntas.

## Cierre de la sesión

- Si una fuente cambia algo que ya afirmamos en un entregable, anotarlo en `00_meta/CAMINOS_PROBADOS.md` o `PREGUNTAS_ABIERTAS.md`; la corrección del entregable se hace en la Fase 5.
- Dejar escrito, al final de la salida, un apartado «Qué quedó sin hacer y por qué».

## Qué pasa a la fase siguiente

La Fase 3 usa la tabla de fuentes y el párrafo «qué implica». La Fase 4 usa las dos frases de entrega que entren en la casilla de evidencia y en la de dudas.
