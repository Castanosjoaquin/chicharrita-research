# Ola 4 — lo que sale de la respuesta del mentor

Nueve lineas, `M1` a `M9`, para implementar lo que el investigador contesto el **2026-10-22** a
las siete preguntas de `entregables/correo-investigador.md`. La carta esta transcripta y mapeada
en `docs/plan_checkpoint2/salidas/F6_respuesta_y_cambios.md`; el plan que ordena las lineas, con
sus tareas y su criterio de terminado, es
[`docs/plan_ola4/PLAN_OLA4.md`](../../docs/plan_ola4/PLAN_OLA4.md). El estado de cada linea se
sigue por los issues del repositorio (`#5` a `#13`, con el indice en `#14`).

Cada carpeta tiene su `REPORT.md` como fuente de verdad, su `index.html` como vista de lectura y
`NOTAS_PARA_META.md` con lo que toca llevar a `00_meta/`.

| Carpeta | Que contesto | Estado |
| --- | --- | --- |
| [`M1_conteo_y_referencia/`](M1_conteo_y_referencia/REPORT.md) | La regla de conteo del si-Fi21 original —un registro por acierto de Bowtie en la hebra `+`, agrupado por referencia— implementada y verificada. Acota la hipotesis del desajuste con numeros ya medidos y mueve el pedido del lunes de «contra que base corrieron» a «contra que registro». | parcial: la matriz de bases no corrio por falta de insumos en la maquina, y se declara como pendiente con los comandos exactos |

## Lo que hay que leer antes de usar estos numeros

- **La maquina que ejecuto M1 no tiene el corpus ni las herramientas.** Sin `work/`, sin Bowtie,
  sin BLAST+, sin ViennaRNA y sin si-Fi21 instalado. Las corridas de la ola 3 se hicieron en otra
  maquina (`research/ola3/C2_codigo_apolo_inta/corridas/README.md`: Darwin arm64, conda `c2sifi`).
  Cualquier linea de la ola 4 que necesite correr el motor de eficiencia o un alineador depende de
  esa otra maquina, y conviene planificarlo antes de empezarla.
- **El conteo por ventana y el conteo por acierto son unidades distintas.** Es el hallazgo que
  reordeno el plan (seccion 3 de `PLAN_OLA4.md`) y vale para leer cualquier numero de la planilla
  de EPILAB contra cualquier numero nuestro.
