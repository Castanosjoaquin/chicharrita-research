# Plan del checkpoint 2 — seis fases, una sesión por fase

**Qué es.** El plan para llegar al checkpoint del **26 de octubre** alineados con la *Guía del checkpoint 2* y las *Fichas optativas* del investigador, a partir de la auditoría `docs/auditoria_guias_checkpoint2.md`. Hoy es 22 de octubre; quedan cuatro días. El correo ya se envió, así que dejó de ser un pendiente (el borrador del repo tiene siete preguntas; el texto realmente enviado no se verificó).

**Cómo usarlo.** Cada fase tiene su propio archivo con todo el contexto adentro (quiénes somos, qué se hizo, qué piden las guías, los resultados medidos, las reglas del repo, las entradas, las tareas, las salidas y el criterio de terminado). Abrí una sesión nueva, pedile que lea el archivo de la fase y la ejecute. No hace falta pasarle nada más.

**Corrección respecto de la auditoría inicial.** Al armar el plan se verificó que el ADR D34 ya había decidido separar los rankings por estrategia, así que la Fase 1 es en realidad *aplicar D34 al entregable* (o revisarlo), no abrir una discusión nueva; y que el «0 de 20 genes» del nulo de región tiene una aclaración en W7 §1.1 que hay que leer antes de citarlo. Ambas cosas ya están reflejadas en las fases.

## Las fases

| # | Fase | Resuelve | Día sugerido | Depende de | Cómputo | Decide el usuario |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [Decisión del ranking y de las etiquetas](FASE_1_decision_ranking_y_etiquetas.md) | Tensión entre el candidato viral y la estrategia del insecto; uso de `[E]` | jue 22 | — | poco | sí |
| 2 | [Entrega y mecanismo](FASE_2_entrega_y_mecanismo.md) | Ruta B de las fichas (casi sin cubrir) | jue 22 / vie 23 | — | no | no |
| 3 | [Hipótesis, alternativas y validación](FASE_3_hipotesis_alternativas_validacion.md) | Elementos 2, 5 y 6; Ruta C | vie 23 | 1 y 2 | no | matar o esterilizar |
| 4 | [Página de siete casillas](FASE_4_pagina_de_siete_casillas.md) | Formato de la guía | sáb 24 | 1, 2 y 3 | no | protagonista |
| 5 | [Reorden y estado del repo](FASE_5_reorden_y_estado_del_repo.md) | Coherencia entre documentos y estado | dom 25 | 1 a 4 | no | CSV de Cedden |
| 6 | [Ensayo y respuesta del investigador](FASE_6_ensayo_y_respuesta.md) | Preparar la reunión y absorber la respuesta | lun 26 y cuando llegue | 4 y 5 | según la respuesta | qué cambios aplicar |

Las fases 1 y 2 son independientes y pueden hacerse en dos sesiones simultáneas, por dos personas distintas. La 3 espera a las dos. Si una fase no alcanza a terminarse, la siguiente tiene una regla de «qué hacer si falta la salida anterior» y no se bloquea.

## Qué cubre cada fase de la guía

| Elemento de la guía del checkpoint 2 | Fase |
| --- | --- |
| 1. La pregunta | 3 y 4 |
| 2. La hipótesis | 3 y 4 |
| 3. La evidencia (procedencia e identificadores) | 2 y 4 |
| 4. Un avance propio | 4 (protagonista) y 1 |
| 5. Las alternativas | 3 y 4 |
| 6. La validación | 3 y 4 |
| 7. Las dudas abiertas | 4 y 6 |

## Mínimo viable si el tiempo no alcanza

1. Fase 1 (decisión, sin recomputar).
2. Fase 3 (sin la parte de Fase 2: marcando `[?]` lo que dependa de entrega).
3. Fase 4.

Con esas tres, las siete casillas existen y la tensión central queda dicha. Las fases 2 y 5 mejoran la calidad y la coherencia; la 6 es el ensayo.

## Pendientes del usuario que este plan no puede cerrar

- La fecha en que se envió el correo, para dejar el estado escrito (Fase 5).
- El texto del correo realmente enviado (cuántas preguntas tenía), para cotejarlo con el borrador (siete) y con `PLAN_DESARROLLO.md` §8 (dice cinco, desactualizado).
- Publicar o no el CSV con las 28 secuencias de Cedden *et al.* (datos públicos CC BY), que sigue sin versionar.
- El peso de un hemíptero no objetivo frente al maíz, que le corresponde al investigador.

## Dónde van las salidas

Todo lo que las fases producen como borrador o decisión va a `docs/plan_checkpoint2/salidas/`. Lo que se entrega al investigador va a `entregables/` (con su `.md` como fuente y su `.html` como vista de lectura). Las decisiones, los descartes y los pendientes van a `00_meta/` como ya se hace.
