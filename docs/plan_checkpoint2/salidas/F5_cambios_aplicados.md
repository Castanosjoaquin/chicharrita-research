# Fase 5 — Reorden del entregable y estado del repo: cambios aplicados

Fecha: 2026-10-22. No hay commit ni push. Todos los cambios están sin commitear, listos para revisar con `git diff`.

## Entregable `entregables/para-el-investigador.md` (y `.html`)

1. **Portada según la guía.** Se agregó «Cómo se lee según la guía» con el enlace a la página de siete casillas (`.html` y `.md`). La parte A queda debajo de esa portada.
2. **Etiquetas según D39.** Las 11 líneas con `[E]` se reclasificaron. El conteo es de la versión anterior del archivo, en el commit `35786c7`: `git show 35786c7:entregables/para-el-investigador.md | grep -c '\[E\]'` da 11 líneas (17 a 21, 29, 31, 33, 37, 41 y 47): lo medido en el repo pasa a `[M]` y las lecturas a `[H]`. El documento queda con cero `[E]`. Lo que es consenso de literatura no aparece en este entregable.
3. **Texto tachado.** Se quitó el tachado de la pregunta 3 y quedó una sola versión vigente. La historia está en `CAMINOS_PROBADOS.md`.
4. **Conciliación del nulo de 7,2 %.** Nueva nota antes de B.2: el nulo mide la media de un puntaje biofísico y permuta bloques de 30 ventanas (W7 §1.1), así que no contradice mover la región de `BicC_Dm`, que se apoya en el veto por *H. vitripennis* y en conservación.
5. **«Eficiente» → «ventana que pasa el filtro».** Cambiado donde describe ventanas (A.4 y D.2). Se conserva el término donde cita la planilla (D.1) y donde define el booleano (A.1).
6. **Estructura de dos listas por mecanismo.** «En cinco líneas» y la fila A.3 describen las dos listas (D38). Se corrigió la frase de que `eth` y `burs-α` «no se distinguen»: ahora dice que `eth` precede en escala absoluta y que el par no tiene orden firme en min-max.
7. **Referencias a fases 1 a 4 en «Dónde está cada cosa».**

## `entregables/que-significa-eficiente.md` (y `.html`)

- Nota de lectura al inicio: «eficiente» es un booleano por ventana, no una medición de eficacia.

## `entregables/correo-investigador.md`

- Estado cambiado a «enviado», con la fecha y el texto por confirmar. Se quitó el bloqueo por apellido y dominio.
- Nota: la pregunta 5 del borrador dice que los candidatos nuevos están «sesgados a esterilidad». El borrador no se editó porque el texto enviado no está verificado.

## `PLAN_DESARROLLO.md`

- §8: el correo figura como enviado, con la fecha por confirmar.
- §5, ítem 5: resuelto.
- §9 nueva «Checkpoint 2», con enlace a `docs/plan_checkpoint2/`.
- Las tablas de los cinco pedidos, la cobertura de §1 bis y T1 a T6 no cambiaron de estado: ningún pedido cambió de estado en esta fase.

## `index.html`

- Enlace a la página de siete casillas y al plan del checkpoint 2, debajo de la síntesis.

## `tools/generar_estado.py` y `estado.html` (regenerado con el script)

- HECHO: cuatro tarjetas nuevas (página de siete casillas, entrega y mecanismo, hipótesis y validación, decisiones y etiquetas).
- FALTA: el ítem del correo pasó a «Fecha y texto del correo enviado». Se agregó «Escala para ordenar pares dentro de un grupo». Los ítems de la publicación del CSV de Cedden y del criterio de commits siguen.
- Verificación: 0 archivos nombrados que faltan en disco; 0 menciones de «sin enviar».

## Las 28 secuencias de Cedden (decisión del usuario)

- El CSV unido **ya estaba en `origin/main`** desde el 2026-10-21 (commit `6b8a800`). El plan y el generador de estado decían «sin subir al remoto», y era falso: se corrigió en el generador.
- El usuario eligió dejarlo publicado y declararlo. No se tocó el remoto ni el historial.
- Se agregó D41 en `00_meta/DECISIONS.md` y una nota de estado de publicación en `research/ola3/C9_sensibilidad_umbral/datos/LEEME.md`.
- En `tools/generar_estado.py` el ítem pasó de FALTA a una tarjeta HECHO.
- Los archivos adicionales originales (`MOESM1` y `MOESM2`) no están en disco.

## `00_meta/`

- `PREGUNTAS_ABIERTAS.md`: sección «Resuelto en la Fase 5» (grafía del correo).
- `CAMINOS_PROBADOS.md`: historia de la corrección de la pregunta 3 y de la lectura del par `eth`–`burs-α`.
- `DECISIONS.md`: se agregó D41 (CSV de Cedden). La enmienda de D38 es de la sesión anterior.

## Qué quedó sin hacer y por qué

1. **Fecha y texto del correo enviado.** Lo pide `PLAN_DESARROLLO.md` §8 y el generador. Sin esos datos no se puede cerrar el ítem.
2. **Número de preguntas del correo.** El borrador tiene siete; `PLAN_DESARROLLO.md` decía cinco. Hay que cotejarlo con el texto enviado.
3. **Lectura de «eficiente» en otros documentos.** `entregables/critica-herramientas.md` tiene 7 apariciones del término que no se cambiaron en esta fase.
4. **Frases del orden de W7 en `PLAN_DESARROLLO.md` (T3, línea 201).** Dicen que `BicC_Dm` y `ATPaseD_Dm` no se ordenan entre sí. Es cierto con las regiones de la planilla (W7); con las regiones recomendadas, `BicC_Dm` va primero en escala absoluta. Hay que aclararlo en T3.
5. **Discrepancia de región de `BicC_Dm`.** `ranking_v2.json` (C7 v2) recomienda 2121–2420; `C8` y el entregable dicen 922–1221 por conservación. El entregable no cambia los números; hay que decidir cuál es la recomendación vigente y dejarla igual en todos los documentos.
6. **Diff por cambio mostrado antes de cada siguiente.** Los cambios se aplicaron en una pasada y se documentan aquí. Revisar con `git diff` antes del commit.
7. **Commit y push.** No se hicieron, como pidió el usuario.
8. **Enlace desde `correo-investigador.md` a esta lista.** No aplica: el borrador no tiene `.html`.

## Qué pasa a la fase siguiente

La Fase 6 asume el repo al día y la página existente. Esta lista (`F5_cambios_aplicados.md`) es el insumo que pide la fase, y el punto 5 de «sin hacer» (región vigente de `BicC_Dm`) afecta al ensayo de preguntas de la reunión.
