# Fase 1 — Decidir cómo se presenta el ranking y cómo se etiqueta la evidencia

| | |
| --- | --- |
| **Día sugerido** | jueves 22 oct |
| **Depende de** | nada (puede correr en paralelo con la Fase 2) |
| **Necesita cómputo** | poco: sólo si se elige la opción A y hay que reordenar con el código existente |
| **Decide el usuario** | sí: dos decisiones, con recomendación del agente |
| **Produce** | ADR D38 y D39; `docs/plan_checkpoint2/salidas/F1_decision_ranking.md` |

**Para empezar:** abrí una sesión nueva sobre el repo y pedile: «Leé `docs/plan_checkpoint2/FASE_1_decision_ranking_y_etiquetas.md` completo y ejecutá esa fase». Todo el contexto está en este archivo.

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

**El problema.** El ranking actual mezcla en una sola lista candidatos cuya acción ocurre en lugares distintos: `MP_MRFV` y `CP_MRFV` actúan sobre un virus dentro del maíz (RNAi antiviral de la planta); `BicC_Dm`, `ATPaseD_Dm`, `eth` y `burs-alpha` actúan sobre el insecto. Las fichas del investigador piden, para un blanco viral, explicar en qué células del maíz ocurre ese RNAi y cómo llegaría el ARN. Eso no está discutido, y el candidato primero es además el menos evaluable (conservación: 4 de 71 registros). Es lo primero que él va a preguntar.

**Antecedente que cambia el planteo (verificado en `00_meta/DECISIONS.md`).** El ADR **D34** ya decidió que el objetivo es el insecto y descartó rankear juntas las dos estrategias, porque exigiría una equivalencia entre desenlaces que no tenemos (mortalidad del vector contra carga viral en planta). Dice que los genes virales siguen en el ranking «porque son material de EPILAB que hay que auditar, no porque el proyecto recomiende esa vía». Es decir, la opción A de abajo no es una idea nueva: es **cumplir D34**, que el entregable no aplicó. La decisión del usuario es entonces confirmar D34 o revisarlo, y esta fase debe leer D34 y D20 antes de proponer nada.

**Qué ya sabemos que condiciona la decisión.**
- Agregar un peso numérico de «plausibilidad de entrega» sería otro parámetro sin fuente: es exactamente la crítica que hacemos a los umbrales de si-Fi21. Por eso la recomendación de la auditoría es una separación cualitativa, no un nuevo término del puntaje.
- Con sólo dos candidatos virales, ordenarlos entre sí es casi trivial; el grupo del insecto tiene cuatro. Antes de afirmar un orden dentro de un grupo hay que comprobar si depende de la escala (z-score contra min-max), porque ese fue el error que ya corregimos en B.2.
- Los dos del insecto originales no se distinguían entre sí; con `eth` y `burs-alpha` el catálogo de C5 los sesga a esterilidad, y el orden cambia según se busque matar o esterilizar (`tablero/orden.html`).

**Decisión 1: estructura del ranking (confirmar D34 o revisarlo).**
- **A (recomendada; cumple D34).** Dos listas, una por mecanismo (insecto, virus en planta), cada una con su evidencia y su incertidumbre, y una frase explícita de por qué no se comparan entre sí. Contra: se pierde el «ganador» único; a favor: no mezcla mecanismos y es coherente con lo que el investigador recomendó.
- **B.** Lista única más una columna cualitativa «¿se entiende cómo llegaría el ARN y dónde actúa?». Contra: la columna es un juicio nuestro, sin medición.
- **C.** Dejar todo como está y agregar una advertencia. Contra: deja la tensión sin resolver.

**Decisión 2: etiquetas de evidencia.** `[E]` significa «consenso en literatura revisada» (`CLAUDE.md`), pero se usa al lado de resultados computacionales propios. Opciones: (i) **recomendada:** no usar `[E]` para resultados propios; las mediciones se rotulan `[M]` («medido por nosotros, reproducible desde el repo») y las interpretaciones `[H]`. Eso toca `CLAUDE.md` y `GLOSARIO.md`, por lo que requiere el visto bueno del usuario; (ii) rotular todo lo propio como `[H]`, sin crear marcador nuevo. Además, en la página y en la diapositiva decir «ventana que pasa el filtro de si-Fi21» en vez de «ventana eficiente».

## Entradas

- `research/ola2/W7_ranking/REPORT.md` (§2.1 bis, §2.2, §2.3) y `benchmark_tres_herramientas.md`
- `research/ola3/C7_ranking_v2/` (REPORT, index.html y scripts; la v2 reproduce W7 exacto y suma humano, `eth` y `burs-alpha`, y reporta a 21 y 22 nt)
- `research/ola3/C8_conservacion/REPORT.md` y `research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.md`
- `tablero/orden.html` y `tablero/limites.html`
- `entregables/para-el-investigador.md`, partes A.3, B.2 y C
- `CLAUDE.md` (sección Evidencia) y `00_meta/GLOSARIO.md`
- `docs/auditoria_guias_checkpoint2.md` §1 y §4.2

## Tareas

1. Leer `00_meta/DECISIONS.md` D20 y D34, W7 §2 y el REPORT de C7 y armar una tabla de los candidatos con: nombre, organismo donde actúa el RNAi, evidencia de que el gen importa y la fuente de esa evidencia.
2. Presentarle al usuario las dos decisiones con `ask_user` (una pregunta por decisión), con la recomendación primero y el costo de cada opción.
3. Si se elige A: reordenar cada grupo **con el código y los datos existentes**, sin inventar un método nuevo. Comprobar si el orden dentro del grupo del insecto depende de la escala (z contra min-max) y si cambia entre matar y esterilizar; informar el resultado tal cual salga, incluida una eventual no distinción.
4. Si se elige B: redactar la columna cualitativa con una definición de una línea y la fuente de cada celda; marcar `[H]`.
5. Redactar `salidas/F1_decision_ranking.md`: la decisión, la tabla final de cada lista, una frase de «por qué no se comparan» y los números copiados del archivo fuente, con su ruta.
6. Si se aprueba `[M]`: proponer el diff de `CLAUDE.md` y `GLOSARIO.md` y aplicarlo sólo con confirmación explícita del usuario. Definir la regla de reemplazo para `para-el-investigador.md` (qué `[E]` pasan a `[M]` y cuáles a `[H]`); **no aplicarla todavía**: eso es la Fase 5.
7. Escribir los ADR D38 (aplicación de D34 al entregable, o su revisión si el usuario elige otra opción) y D39 (etiquetas y vocabulario) en `00_meta/DECISIONS.md`, con alternativas consideradas, criterio y consecuencia.

## Salidas

- `docs/plan_checkpoint2/salidas/F1_decision_ranking.md`
- ADR D38 y D39 en `00_meta/DECISIONS.md`
- Si hubo cómputo: la salida en `research/ola3/C7_ranking_v2/resultados/` con un README de una línea (qué se corrió y con qué script)

## Criterio de terminado

- [ ] La decisión de estructura está tomada por el usuario y escrita con sus alternativas.
- [ ] Cada número de la tabla final tiene ruta de archivo y se copió de ese archivo.
- [ ] Si algún orden dentro de un grupo no se sostiene, el documento dice «no se distinguen» en vez de forzar un primero.
- [ ] Quedó definida (no aplicada) la regla de etiquetas para la Fase 5.
- [ ] `CLAUDE.md` no se modificó sin confirmación.

## Qué no hacer

- No agregar un peso nuevo al puntaje.
- No reescribir `para-el-investigador.md` (es la Fase 5).
- No afirmar que el RNAi antiviral del maíz funciona de cierta manera sin una fuente abierta: eso se resuelve en la Fase 2; acá sólo se declara que falta.
- No descartar el candidato viral: se separa, no se elimina.

## Cierre de la sesión

- Anotar en `00_meta/PREGUNTAS_ABIERTAS.md` lo que quedó sin resolver (por ejemplo, el peso de un hemíptero no objetivo frente al maíz, que sigue siendo del investigador).
- Si algo se probó y se descartó, a `00_meta/CAMINOS_PROBADOS.md`.
- Dejar escrito, al final de la salida, un apartado «Qué quedó sin hacer y por qué».

## Qué pasa a la fase siguiente

La Fase 3 necesita la decisión de estructura (para saber qué candidato se propone ensayar) y la regla de etiquetas. La Fase 4 usa la tabla final. Entregar ambas en `F1_decision_ranking.md`.
