# F3 — notas para los archivos de memoria, separadas por destino

Estado al 2026-10-27, con el `PREREGISTRO.md` escrito y **antes** de rankear. Lo que sigue
está ya aplicado en los archivos de `00_meta/` en el mismo commit; esta página es el registro
de qué fue a dónde y por qué.

## A `DECISIONS.md`

**`D84` — los pesos del recomendador, como PROPUESTA.** Aplicado. Cuatro ejes con peso
—fenotipo 0,40, esencialidad 0,25, off-target 0,25, conservación 0,10— más el eje de
expresión en tejido expuesto con peso 0,00 y declarado faltante; agregación por **cohortes**
según qué ejes tiene calculados cada candidato, sin comparar entre cohortes y sin rellenar
ningún hueco. Lleva «PROPUESTA» en el título a propósito: el issue es `decide-usuario` y
mientras diga eso no se rankea nada.

## A `PREGUNTAS_ABIERTAS.md`

**Entrada 54 — `D67` no cubre un cuarto mecanismo que el catálogo sí tiene.** Aplicada.
Cuatro filas describen *menos transmisión con el insecto vivo*, que no entra en reproducción,
movilidad ni letalidad. Amplía un ADR ajeno, así que se propone y se pregunta.

**Entrada 55 — los dos candidatos de signo invertido merecen una pregunta al investigador.**
Aplicada. `CI-08` y `CI-13` empeoran la colonización al silenciarlos. Quedan fuera del orden,
pero la pregunta interesante es la contraria a la nuestra.

**Entrada 56 — `work/sifi_v2/` y los tres TSA, pedidos al grupo.** Aplicada. Son los insumos
de los ejes 3 y 4. Con el pedido va la advertencia de `PENDIENTE.md` de `R11`: no se
regeneran acá con otra versión del motor.

**Entrada 57 — «esta máquina» sin nombrar la máquina, dos veces el mismo día.** Aplicada. Es
una observación de método, no un reproche: `D71` pide que cada verificación diga en qué
máquina se hizo, y dos artefactos de hoy no lo hacen.

## A `CAMINOS_PROBADOS.md`

**La suma ponderada sobre los 36 candidatos, descartada antes de implementarla.** Aplicada.
Es la forma obvia y la que un recomendador «normal» usaría; se descarta porque 28 de 36 filas
no tienen el eje de off-target y obligaría a imputar.

## Lo que NO va a ningún archivo de memoria todavía

El orden de los candidatos, porque no está calculado: los pesos no están confirmados. Y la
respuesta a «matar o esterilizar», que es lo que esta línea tiene que volver decidible: hoy
sigue siendo lo que era, una pregunta abierta, y lo será hasta que el eje de fenotipo esté
calculado y los pesos confirmados. Anotar antes cualquier insinuación de respuesta sería
exactamente lo que el preregistro existe para impedir.
