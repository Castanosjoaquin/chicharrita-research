# Notas para el meta — M9

## Para `DECISIONS.md`

Hace falta un ADR para **qué se hace con las 25 ventanas de
`q2_aciertos_localizados.tsv`** (REPORT §3.1). Es la misma clase de decisión que D41 y
conviene resolverla con el mismo criterio, pero no es la misma decisión: D41 era sobre
datos públicos con licencia CC BY, y esto son ventanas de las regiones que entregó
EPILAB. Las tres alternativas y la recomendación están en §6.1. **No se tomó acá porque
es del usuario.**

## Para `PREGUNTAS_ABIERTAS.md`

- **Procedencia de `baseline_dsrip/dsrip_vatpaseA.csv`.** Reconstruye 1.845 nt, el CDS
  completo de V-ATPase A de *D. maidis*. No es ninguna de las cuatro regiones de EPILAB,
  verificado. Pero el README dice que el CDS se reconstruyó desde
  `pipeline/salida/sirna_vatpaseA.csv`, que no se versiona, y no se comprobó contra qué
  genoma. Es una pregunta para Luca y es barata de contestar `[?]`.
- **Cuántas posiciones difieren entre las regiones virales de EPILAB y `NC_002786.2`.**
  La cobertura da 90,5 % y 96,5 %, compatible con un aislado distinto, pero no se midió.
- **La licencia de D32** sigue abierta y bloquea la tarea 4. Es el pedido 6 del lunes.

## Para `CAMINOS_PROBADOS.md`

Nada que descartar. La hipótesis con la que empezó la línea —que el repositorio podía
tener secuencias de EPILAB sin detectar— resultó cierta en un caso y acotada.

## Para el entregable, si hace falta

El dato de §3.2 es presentable y conviene tenerlo a mano el lunes: **las dos regiones
virales que entregó EPILAB son subcadenas del genoma público de MRFV** (`NC_002786.2`),
así que su confidencialidad es nominal. Las dos del insecto no están en esa situación.
Eso cambia qué se puede discutir en público sobre los dos candidatos virales, y no
cambia nada sobre los dos del insecto.

## Para quien siga la ola 4

- El gancho **no está activo** hasta que alguien corra
  `git config core.hooksPath tools/verificacion/hooks` en su clon. El sandbox no puede
  escribir `.git/config`.
- **M3 (#7) tiene un supuesto que está medido y es falso.** El issue dice de las columnas
  `nt19`, `nt2` y `rama_terminal`: «son dos letras y un entero: no reconstruyen
  secuencia, así que no chocan con la regla de confidencialidad». Como las ventanas se
  solapan de a 1 nt, **cada una de esas columnas concatenada es una subcadena literal del
  gen**: sobre un gen sintético de 500 nt y 480 ventanas, la columna `nt19` da 480 nt que
  aparecen en el gen con desplazamiento 18, y `nt2` otros 480 con desplazamiento 1; entre
  las dos reconstruyen 497 de 500 nt, el 99,4 % `[M]`
  (`scripts/prueba_columnas_terminales.py`). No hay ninguna racha de 21 nt en el archivo:
  la fuga está en la columna, no en la celda. Si M3 publica esas columnas para los cuatro
  genes, publica los cuatro genes. **Dos salidas posibles:** emitir la tabla de
  `--features` sin esas dos columnas, o emitirla sólo para ventanas no consecutivas (un
  muestreo), que rompe la cadena. Conviene decidirlo antes de implementar, no después.
- M3 también quita la columna `seq`, que es lo que esta línea recomienda.
