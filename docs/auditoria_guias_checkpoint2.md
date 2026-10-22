# Auditoría del entregable contra las dos guías del investigador

**Fecha:** 2026-10-22. **Material leído:** `Guia_Checkpoint2_Estudiantes.pdf` (v1.0, 21 oct), `Fichas_Optativas_Estudiantes_v3.pdf` (18 oct), `entregables/para-el-investigador.md`, `entregables/correo-investigador.md`, `research/checkpoints/checkpoint1.md`, `PLAN_DESARROLLO.md`, el tablero y la búsqueda de términos en el repo.
**Alcance:** lectura y cotejo; no se recalculó ningún número del entregable. Los huecos se detectaron buscando términos en el repo, no releyendo los ~30 informes: un tema marcado «ausente» puede estar en un informe que la búsqueda no tocó.

## 1. Veredicto en tres líneas

1. **Alineados en el fondo, desalineados en el formato.** La guía pide «una página o unas pocas diapositivas» con siete elementos; nuestro entregable es un documento de diez minutos organizado alrededor de *lo que él pidió en el checkpoint 1*, no alrededor de esos siete elementos.
2. **Cubrimos con holgura** evidencia, avance propio, incertidumbre y dudas abiertas (elementos 3, 4, 7). **Cubrimos a medias** pregunta, hipótesis y alternativas (1, 2, 5). **No cubrimos** el elemento 6, la validación propuesta (qué medir, con qué controles, qué resultado cambiaría la interpretación), y es el hueco más grande.
3. **Hay una tensión de coherencia que él va a ver:** nuestro candidato número uno es viral (`MP_MRFV`), pero las fichas piden, para un blanco viral, explicar en qué células del maíz ocurre el RNAi antiviral y cómo llegaría el ARN hasta ahí, y el repo no lo discute. En el checkpoint 1 él mismo recomendó la estrategia del insecto. *(Corrección posterior: el ADR D34 ya había decidido separar los rankings por estrategia y dejar los genes virales como material de EPILAB a auditar; lo que falta es que el entregable lo aplique, porque hoy muestra una lista única.)*

## 2. Cotejo con la guía del checkpoint 2

| # | Elemento de la guía | Estado | Qué hay | Qué falta |
| --- | --- | --- | --- | --- |
| 1 | La pregunta (relevancia para el sistema chicharrita–achaparramiento) | **Parcial** | El entregable cuenta *qué hicimos*, no *qué pregunta resolvemos*. | Una oración de pregunta que conecte vector, virus y aplicación. |
| 2 | La hipótesis (mecanismo + resultado predicho) | **Parcial** | Argumento de la latencia (~20 días) y la tensión central marcada `[H]`. | Hipótesis explícita y falsable, con la predicción. |
| 3 | La evidencia (artículos, datos, procedencia e identificadores) | **Cubierto** | Cada número tiene informe detrás; marcadores `[E]/[R]/[H]`; accesiones de transcriptomas (GHCC01, GITV01). | Versión y accesión de las secuencias dentro del documento corto (las fichas piden «organismo, gen, función, secuencia y versión»). |
| 4 | Un avance propio | **Cubierto, con exceso** | Auditoría de si-Fi21, benchmark, ranking, regiones, sensibilidad, validación retrospectiva. | Elegir *uno* como protagonista; el resto va de anexo. |
| 5 | Las alternativas | **Parcial** | Alternativas *dentro* del método (pesos, umbrales, 21 vs 22 nt). | Alternativa de *estrategia*: insecto vs. planta; matar vs. esterilizar; otra explicación para el «no valor predictivo» de la accesibilidad. |
| 6 | La validación (medidas, controles, qué cambiaría la interpretación) | **No cubierto** | Validación *retrospectiva* sobre *Tribolium* (no concluyente). | Diseño de ensayo propuesto sobre *D. maidis*. Ver §4. |
| 7 | Las dudas abiertas | **Cubierto** | Siete preguntas ordenadas por impacto. | Añadir qué *recurso* faltaría (transcriptoma, ensayo de largos, acceso a insectos), no sólo preguntas de método. |

**Regla de trabajo de la guía** («una coincidencia, una puntuación o un resultado in silico es una hipótesis, no una prueba»): **se cumple en el espíritu** (el entregable declara que no predice eficacia y que el nulo no refuta). **Riesgo de redacción:** la etiqueta `[E]` (establecido por literatura revisada, según `CLAUDE.md`) aparece al lado de resultados computacionales propios en las partes A y B. Quien lea rápido puede entender «establecido» como «probado». Conviene usar `[H]` para ranking y regiones, o cambiar el nombre de la etiqueta de las mediciones («medido»).

## 3. Cotejo con las fichas optativas

| Tema de las fichas | Estado | Comentario |
| --- | --- | --- |
| «On-target no demuestra silenciamiento; off-target es hipótesis de riesgo» | **Cubierto** | Es nuestra postura central. |
| Mecanismo: Dicer-2, carga en AGO2, selección de hebra por asimetría 5′; «no basta contar ventanas de 21 nt» | **Cubierto** | `que-significa-eficiente.md` desglosa regla del nucleótido terminal y selección de hebra con su fuente y grado de evidencia. Es el punto donde más coincidimos con él. |
| «¿Por qué terminar en esa posición y no en otra?» (longitud de región) | **Cubierto en parte** | Pregunta 6 (150–250 nt sin fuente) y el informe C6. Falta decir en una frase que la ventana de 200 nt es frágil (11,7 % y 25,8 % de coincidencia con la de defecto), lo que responde su pregunta con un dato. |
| Seguridad: organismos no objetivo y cómo evaluar el riesgo | **Cubierto** | Panel con maíz, abeja, humano y cicadélidos; hallazgo clave: el riesgo está en cicadélidos emparentados (`tablero/riesgo.html`). |
| Cómo leer dsRNAEngineer (ejes, escalas, totales ≠ siRNA eficaces) | **Cubierto** | Es el núcleo de `critica-herramientas.md`. |
| Ruta A, eficacia mecanística (¿qué célula recibe el ARN?) | **Parcial** | Mecanismo sí; célula receptora en el insecto no se discute en los entregables. |
| **Ruta B, formulación y entrega** (dónde se aplica, barreras, dsRNasas, estabilidad ≠ captación ≠ actividad, comparadores) | **Débil** | Una sola línea en el entregable («la entrega oral es mucho más débil que la inyección»). La bibliografía de entrega (Rossi 2024, Mitter 2017, Dalaisón-Fuentes 2023) está en el repo (`W1_papers`) pero no aparece en los entregables; Hoang 2022 sólo figura en `sources.json`, **no hay evidencia de que se haya leído**. |
| **Ruta C, diseño experimental y riesgo** (endpoint primario/secundario, grupo control, dosis, muestreo, qué descartaría la propuesta) | **No cubierto** | Es el elemento 6 de la guía. |
| Regla de oro: «detectamos ARN» ≠ «entró a la célula» ≠ «hay siRNA funcional» ≠ «hay efecto» | **Cubierto implícitamente** | Convendría citarla con esas palabras como marco de la ficha. |
| «Knockdown sin fenotipo / fenotipo sin knockdown» | **No cubierto** | Búsqueda sin resultados en el repo. Es la lectura del ensayo que más le interesa. |
| Elegir sistema: D. maidis vs MRFV vs otros | **Incoherencia con D34** | Ver §1, punto 3. |

**Encaje con los tipos de entrega de las fichas:** somos «Bioinformática accesible» (comparación documentada de secuencias, especies y ventanas + discusión de parámetros). Esa es la categoría que declarar. Quedar a medias entre dos categorías diluye el mensaje; lo que sí puede sumarse es un esbozo de «Biología» (target + barreras + plan de ensayo) como cierre, no como segundo producto.

## 4. Lo que falta, en orden de prioridad

1. **Un esbozo de validación (elemento 6 / Ruta C). Es el hueco principal y se puede cerrar sin cómputo nuevo**, con lo que ya está medido. Estructura mínima:
   - Candidato a ensayar: el que sobreviva a la alternativa de «objetivo insecto» (ver punto 2).
   - Endpoint primario: transcripto del gen blanco (RT-qPCR) con gen de referencia validado en *D. maidis*. Secundario: supervivencia o fecundidad, según la respuesta a la pregunta 5 del correo (matar o esterilizar).
   - Controles: ARNdc control no relacionado (p. ej. GFP), vehículo solo, y una región alternativa del mismo gen (la 922–1221 frente a la elegida) para probar que la *región* importa y no sólo el gen.
   - Qué cambiaría la interpretación: knockdown sin fenotipo; fenotipo sin knockdown; efecto del control inespecífico; nulo si el ARN no es estable en el compartimento de ingesta.
   - Medida de exposición: integridad del ARN en el alimento antes y después.
   - *Esto es una propuesta de diseño, no una recomendación de dosis ni formulación (las fichas lo piden explícitamente así).*
2. **Resolver la tensión `MP_MRFV` primero (aplicando D34).** Dos opciones honestas: (a) presentar *dos rankings separados* —blancos del insecto y blancos virales— porque comparar un blanco cuya acción ocurre en el vector con otro que ocurre en la planta mezcla mecanismos distintos; o (b) mantener el ranking único y agregar una columna de «plausibilidad de entrega/mecanismo» que baje al viral. En cualquiera de los dos casos, decirlo antes de que él lo pregunte. Recordar que para `MP_MRFV` sólo 4 de 71 registros cubren la región: el candidato más alto es el menos evaluable.
3. **Hipótesis explícita y alternativa.** Una frase para cada una; ejemplo de forma: «si el gen X se silencia en el vector antes del fin del período de latencia, se espera menor transmisión; esto fallaría si la entrega oral no alcanza el tejido o si las dsRNasas degradan el ARN». Alternativa: apuntar al virus en la planta, con su barrera propia.
4. **Un tema de entrega en media página** con las tres lecturas que ya están en el repo (Rossi, Mitter, Dalaisón-Fuentes 2023) y sólo lo que éstas afirman. No agregar lo que no se leyó.
5. **Corregir inconsistencias internas de lectura:**
   - La pregunta 3 del entregable trae un texto tachado con la corrección pegada. Para un tercero se lee confuso: dejar sólo la versión vigente y mover la historia a una nota.
   - El nulo de región («0 de 20 genes», `tablero/limites.html`) y la recomendación de mover la región (922–1221) pueden leerse como contradicción. **Corrección:** W7 §1.1 ya las concilia: el nulo mide la media de un puntaje biofísico, no el conteo de ventanas eficientes. Hay que enlazar esa conclusión, no reinterpretarla (mi descripción inicial, «una es eficiencia y otra seguridad», era incompleta).
   - El título de `que-significa-eficiente` usa «eficiente»; en la diapositiva conviene «ventana que pasa el filtro de si-Fi21», para no chocar con la regla de oro de las fichas.

## 5. Cómo ordenar lo que ya existe

La guía dice que basta una página. Propuesta de tres capas, de más corta a más larga:

1. **Una página (la que se muestra el 26):** los siete elementos como siete casillas, una a tres líneas cada una, con la decisión razonada y la incertidumbre real en primer plano. Nada de tablas largas.
2. **El documento actual (`para-el-investigador`)**, reenfocado: pasar la «Parte A, lo que pidieron» a anexo y abrir con los siete elementos. Mantener la parte de lo que no sabemos y las preguntas.
3. **El repositorio** (`index.html`, `estado.html`, informes) como respaldo recuperable, que es lo que la guía llama «las evidencias deben poder recuperarse».

**Resultado protagonista sugerido:** el hallazgo con más alcance y mejor medido es que *con los datos abiertos no se puede distinguir un criterio bueno de uno inútil* (validación retrospectiva), más la fragilidad de la región de 200 nt. Eso es una «incertidumbre real» como la que la guía dice valorar, y está respaldada por números. Los números del ranking exacto van de apoyo.

## 6. Cómo seguir hasta el 26 de octubre

| Orden | Tarea | Necesita cómputo | Quién decide |
| --- | --- | --- | --- |
| 1 | Decidir ranking único vs. dos rankings (§4.2) | No | Equipo |
| 2 | Escribir hipótesis, alternativa y esbozo de validación (§4.1, §4.3) | No | Equipo, revisar contra pregunta 5 |
| 3 | Escribir la página de siete casillas | No | Equipo |
| 4 | Media página de entrega con Rossi, Mitter, Dalaisón-Fuentes | No (lectura) | Equipo |
| 5 | Generar el `.html` de lectura de los entregables (falta por la convención del repo) | No | Equipo |
| 6 | Confirmar apellido y dominio del correo y enviarlo | No | **Usuario** (bloqueo actual) |
| 7 | Decidir si se publica el CSV con las 28 secuencias de Cedden (CC BY) | No | **Usuario** |

El borrador del correo (siete preguntas; no se verificó cuántas tenía el enviado) ya no se puede modificar: esto sólo sirve para una segunda tanda o la reunión. Una sugerencia: agregar una pregunta sobre *qué ensayo les parece más informativo y viable* (elemento 7 de la guía: recursos), y ordenar las preguntas de manera que la 5 (matar o esterilizar) pase a la primera mitad, porque define el endpoint del esbozo de validación.
