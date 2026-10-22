# Fase 5 — Reordenar el entregable existente y poner al día el repositorio

| | |
| --- | --- |
| **Día sugerido** | domingo 25 oct |
| **Depende de** | Fases 1 a 4 (si falta alguna, ver «Entradas») |
| **Necesita cómputo** | no; sólo correr dos scripts del repo |
| **Decide el usuario** | la publicación del CSV de Cedden, si sigue pendiente |
| **Produce** | `para-el-investigador.md` y `.html` reordenados; plan, ADR y `estado.html` al día |

**Para empezar:** abrí una sesión nueva sobre el repo y pedile: «Leé `docs/plan_checkpoint2/FASE_5_reorden_y_estado_del_repo.md` completo y ejecutá esa fase». Todo el contexto está en este archivo.

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

**Para qué.** Que el repo no se contradiga con la página nueva y que quien lo abra encuentre primero lo que pide la guía. Es mantenimiento con reglas precisas: el repo ya tuvo contradicciones por actualizar sólo uno de varios lugares.

**Cambios al entregable, que salen de la auditoría.**
1. Abrir `entregables/para-el-investigador.md` con un enlace a la página de siete casillas y con una frase de «cómo leer esto según la guía»; mover la Parte A («lo que pidieron») a un anexo o dejarla debajo de la nueva portada. No borrar resultados.
2. Aplicar la regla de etiquetas decidida en la Fase 1 (D39): `[E]` sólo para lo que cumpla la definición del repo; las mediciones propias como `[M]` o `[H]` según se haya aprobado.
3. En el punto D.3, que hoy tiene texto tachado con la corrección pegada, dejar una sola versión vigente; la historia va a una nota breve o a `CAMINOS_PROBADOS.md`.
4. Agregar una frase que concilie dos cosas que se pueden leer como contradicción: el nulo del 7,2 % (0 de 20 genes, `tablero/limites.html`) y la recomendación de mover la región en `BicC_Dm` (922–1221) por seguridad frente a un cicadélido no objetivo y por conservación. **Leer antes W7 §1.1**, que ya las concilia (el nulo mide la media de un puntaje biofísico, no el conteo de ventanas eficientes), y reflejar esa conclusión sin reinterpretarla.
5. Sustituir «eficiente» por «ventana que pasa el filtro de si-Fi21» en el material de lectura rápida (en `que-significa-eficiente.md`, que explica la palabra, se deja el término pero se aclara que es un booleano).
6. Aplicar en la sección del ranking la estructura elegida en la Fase 1 (por defecto, dos listas por mecanismo, como ya decía D34).
7. Agregar una referencia a la media página de entrega (Fase 2) y al esbozo de validación (Fase 3) en «Dónde está cada cosa».

**Estado del repo que se debe actualizar (los tres lugares de `PLAN_DESARROLLO.md`).**
- Tabla de los cinco pedidos, tabla de cobertura de §1 bis y cuerpo de cada tarea T1–T6 (para lo que cambie de estado).
- §8 «Lo que queda» dice «cinco preguntas de §5»; el borrador tiene siete: reconciliar con el texto realmente enviado (pedírselo al usuario). **Marcar el correo como enviado** (pedirle al usuario la fecha; no inventarla) y quitar el bloqueo de apellido y dominio; actualizar `entregables/correo-investigador.md`, que dice «Estado: sin enviar».
- Agregar una sección nueva «Checkpoint 2» que enlace a este plan (`docs/plan_checkpoint2/`).
- `00_meta/PREGUNTAS_ABIERTAS.md`: sacar lo resuelto y sumar lo nuevo.
- `tools/generar_estado.py`: mover de FALTA a HECHO lo que corresponda, agregar las tarjetas nuevas (página de siete casillas, entrega, validación) y **volver a correrlo** para regenerar `estado.html`. Enlazar la página nueva desde `index.html`.
- Dos pendientes del usuario que podrían seguir abiertos: publicar o no el CSV con las 28 secuencias de Cedden (datos públicos CC BY, hoy sin versionar en `research/ola3/C9_sensibilidad_umbral/datos/`) y la grafía del apellido (ya sin efecto para el envío). Preguntar al usuario antes de decidir cualquiera de las dos.

## Entradas

- `docs/plan_checkpoint2/salidas/` (F1 a F4) y `entregables/checkpoint2-una-pagina.md`
- `entregables/para-el-investigador.md`, `que-significa-eficiente.md`, `critica-herramientas.md`, `correo-investigador.md`
- `PLAN_DESARROLLO.md` (§1, §1 bis, §3 y §8), `estado.html`, `index.html`
- `tools/generar_estado.py`, `tools/md_a_html.py`
- `00_meta/DECISIONS.md`, `CAMINOS_PROBADOS.md`, `PREGUNTAS_ABIERTAS.md`, `GLOSARIO.md`, `CLAUDE.md`
- `docs/auditoria_guias_checkpoint2.md` §4.5 y §5

## Tareas

1. Leer el estado actual de `git status` (el repo ya tiene commits por fase: seguir el estilo de los mensajes) y no pisar cambios sin commitear que no sean de esta sesión.
2. Aplicar los siete cambios al entregable, uno por uno, mostrando el diff al usuario antes del siguiente.
3. Regenerar los `.html` de los entregables que cambiaron con `tools/md_a_html.py`. Verificar que `correo-investigador.md` no necesite `.html` (es un borrador enviado; sólo se corrige su estado).
4. Actualizar `PLAN_DESARROLLO.md` en los tres lugares y agregar la sección del checkpoint 2.
5. Actualizar `generar_estado.py` y correrlo; abrir `estado.html` y comprobar que no declara pendiente nada hecho.
6. Revisar que los ADR D38 y D39 (y D40 si existe) estén escritos y que las referencias cruzadas funcionen (rutas que existen en disco).
7. Dejar al usuario la lista de archivos tocados, listos para commit.

## Salidas

- `entregables/para-el-investigador.md` y `.html` reordenados
- `PLAN_DESARROLLO.md`, `00_meta/*`, `estado.html` (regenerado), `index.html` al día
- `docs/plan_checkpoint2/salidas/F5_cambios_aplicados.md`: lista de archivos tocados, con una línea por cambio

## Criterio de terminado

- [ ] `para-el-investigador.md` abre con la estructura de la guía y no tiene texto tachado.
- [ ] Las etiquetas siguen la regla D39.
- [ ] Los tres lugares de `PLAN_DESARROLLO.md` dicen lo mismo.
- [ ] `correo-investigador.md` y `PLAN_DESARROLLO.md` §8 dicen que el correo se envió.
- [ ] `estado.html` se regeneró con el script y no se editó a mano.
- [ ] Todas las rutas citadas existen.

## Qué no hacer

- No editar `estado.html` a mano.
- No borrar resultados ni informes: se reordenan y se enlazan.
- No tocar los originales del corpus ni `research/ola*/` salvo para agregar un README si corresponde.
- No cambiar números ni conclusiones: esta fase no calcula.
- No hacer commit ni push sin que el usuario lo pida.

## Cierre de la sesión

- Un ADR más si se tomó una decisión nueva de estructura del repo (D40 o siguiente).
- Si se descubrió una contradicción más, anotarla en `CAMINOS_PROBADOS.md` con su corrección.
- Dejar escrito, al final de la salida, un apartado «Qué quedó sin hacer y por qué».

## Qué pasa a la fase siguiente

La Fase 6 asume que el repo está al día y que la página existe. Pasarle la lista `F5_cambios_aplicados.md`.
