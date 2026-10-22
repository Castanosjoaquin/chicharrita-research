# Fase 4 — Armar la página de siete casillas (y, opcional, tres diapositivas)

| | |
| --- | --- |
| **Día sugerido** | sábado 24 oct |
| **Depende de** | Fases 1, 2 y 3 |
| **Necesita cómputo** | no |
| **Decide el usuario** | el protagonista, si no se confirma el sugerido |
| **Produce** | `entregables/checkpoint2-una-pagina.md` y `.html`; opcional: `entregables/checkpoint2-diapositivas.md` |

**Para empezar:** abrí una sesión nueva sobre el repo y pedile: «Leé `docs/plan_checkpoint2/FASE_4_pagina_de_siete_casillas.md` completo y ejecutá esa fase». Todo el contexto está en este archivo.

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

**Qué se pide.** La guía del checkpoint 2 dice que «una página o unas pocas diapositivas bastan» para orientar la conversación y que se valora «una decisión razonada y una incertidumbre real». No es una presentación terminada. El entregable actual (`para-el-investigador.md`) dura diez minutos y está organizado por lo que él pidió en el checkpoint 1, no por los siete elementos.

**Los siete elementos, con la fuente de cada casilla.**
1. La pregunta → Fase 3.
2. La hipótesis → Fase 3.
3. La evidencia → Fase 2 y el entregable actual; **incluir procedencia e identificadores** (organismo, gen, versión, accesiones, ya presentes en `research/ola2/W5_secuencias_epilab/REPORT.md` y en C11), porque la ficha pide «organismo, gen, función, secuencia y versión».
4. Un avance propio → un solo protagonista; el resto va de anexo.
5. Las alternativas → Fase 3.
6. La validación → Fase 3.
7. Las dudas abiertas → las preguntas del correo enviado (el borrador tiene siete; confirmar con el texto enviado) más, si la Fase 3 las generó, qué recurso falta (transcriptoma, un ensayo con largos comparados en la especie).

**Protagonista sugerido** (el usuario puede cambiarlo): con los datos abiertos no se puede distinguir un criterio bueno de uno inútil (validación retrospectiva: ρ = +0,142, IC95 [−0,247, +0,492], n = 29), y la región exacta de 200 nt es frágil aunque el candidato superior sea robusto. Es una incertidumbre real, está medida y se alinea con la regla de la guía (lo in silico es hipótesis). Alternativa: la separación de rankings por mecanismo de la Fase 1.

**Reglas de redacción para esta página.**
- Entre 450 y 700 palabras. Sin tablas largas; una tabla corta de siete filas se acepta.
- Ninguna afirmación in silico se escribe como hecho: se dice «ventana que pasa el filtro», «hipótesis de riesgo», «no demuestra silenciamiento».
- Cada número lleva su ruta de archivo en una nota al pie o en la lista «dónde está cada cosa»; la guía exige que las evidencias sean recuperables.
- Categoría declarada: Bioinformática accesible; el esbozo de validación se presenta como complemento, no como segundo producto.

## Entradas

- `docs/plan_checkpoint2/salidas/F1_decision_ranking.md`, `F2_entrega_y_mecanismo.md` y `F3_hipotesis_alternativas_validacion.md`. **Si falta alguna**: usar `docs/auditoria_guias_checkpoint2.md` §4, escribir sólo las casillas que se puedan sostener con material del repo y dejar la casilla faltante con «pendiente: Fase N» en vez de rellenarla.
- `entregables/para-el-investigador.md`, `entregables/correo-investigador.md` (qué se envió)
- `research/ola3/C9_sensibilidad_umbral/REPORT.md` y `RESULTADOS_validacion_retrospectiva.md`; `entregables/validacion_retrospectiva.png`
- `research/ola2/W5_secuencias_epilab/REPORT.md` y `secuencias.json` (identificadores y versiones)
- Guía del checkpoint 2 (raíz del repo)
- `tools/md_a_html.py`

## Tareas

1. Confirmar con el usuario el protagonista (sugerido arriba).
2. Escribir la página: un título y las siete casillas numeradas, una a tres líneas cada una, más una línea final con «dónde está cada cosa».
3. Verificar cada número contra el archivo de origen y copiarlo; no escribir de memoria.
4. Pasar el checklist de la guía: ¿las siete casillas están?, ¿hay una decisión razonada?, ¿hay una incertidumbre real?, ¿lo in silico se presenta como hipótesis?, ¿las evidencias se pueden recuperar?
5. Opcional: tres diapositivas en Markdown (1: pregunta + hipótesis + alternativas; 2: avance protagonista con la figura de la validación retrospectiva; 3: validación propuesta + dudas).
6. Generar el `.html`: `python tools/md_a_html.py entregables/checkpoint2-una-pagina.md entregables/checkpoint2-una-pagina.html` desde la raíz.
7. Pedirle al usuario que lea la página en voz alta en menos de cinco minutos y marcar lo que se atraganta.

## Salidas

- `entregables/checkpoint2-una-pagina.md` y `.html`
- Opcional: `entregables/checkpoint2-diapositivas.md`
- `docs/plan_checkpoint2/salidas/F4_checklist_guia.md`: la tabla de siete casillas con ✓ o ✗ y la ruta de la fuente de cada una

## Criterio de terminado

- [ ] Las siete casillas están completas o marcadas «pendiente» con la fase que falta.
- [ ] Cabe en una página (450–700 palabras).
- [ ] Cada número está verificado contra su archivo.
- [ ] No hay `[E]` sobre resultados propios.
- [ ] El `.html` se generó y se abre.
- [ ] El usuario la leyó en voz alta y se entiende.

## Qué no hacer

- No copiar en la página el contenido de las partes A y B del entregable: ahí va un enlace.
- No agregar resultados nuevos ni correr análisis: esta fase no calcula.
- No ocultar una casilla débil: «no lo sabemos todavía y necesitamos X» es una respuesta válida según la guía.
- No tocar `para-el-investigador.md` (Fase 5).

## Cierre de la sesión

- Si en la lectura en voz alta aparece una pregunta sin respuesta, agregarla a `PREGUNTAS_ABIERTAS.md`.
- Dejar escrito, al final de la salida, un apartado «Qué quedó sin hacer y por qué».

## Qué pasa a la fase siguiente

La Fase 5 enlaza esta página desde `para-el-investigador.md`, `index.html` y `estado.html`. La Fase 6 usa la página como base del ensayo de preguntas.
