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
| [`M1_conteo_y_referencia/`](M1_conteo_y_referencia/REPORT.md) | La regla de conteo del si-Fi21 original —un registro por acierto de Bowtie en la hebra `+`, agrupado por referencia— implementada, verificada y **aplicada a once bases**. El conteo por acierto explica `BicC_Dm` con un error de uno (200 contra 199) y no explica los otros tres genes. Descarta la orientacion con medicion y agrega una pregunta discriminante para el lunes. | **parcial, los cuatro criterios de terminado cumplidos.** Ningun gen pendiente de correr; lo que falta es un dato del laboratorio |
| [`M8_que_compara_el_conteo/`](M8_que_compara_el_conteo/REPORT.md) | Hasta donde compara el numero de siRNAs eficientes: los cuatro limites, todos ya medidos en el repositorio, y las siete variables biologicas que faltan. Normalizando por largo, `BicC_Dm` pasa de primero por conteo a tercero por densidad. | completa: sin computo nuevo, solo aritmetica sobre conteos ya publicados |

## Lo que hay que leer antes de usar estos numeros

- **Las herramientas estaban dentro de si-Fi2015.** La primera sesion de M1 declaro Bowtie y
  RNAplfold como ausentes y escribio los comandos para otra maquina; el instalador de si-Fi2015
  trae los dos en `%LOCALAPPDATA%\siFi2015\`, y son los binarios con los que corrio el programa
  original. Sigue siendo cierto que `work/` no esta en git y que puede no estar en la maquina
  (`research/ola3/C2_codigo_apolo_inta/corridas/README.md`), pero una linea que necesite el motor
  de eficiencia o un alineador no depende por eso de otra maquina.
- **El conteo por ventana y el conteo por acierto son unidades distintas.** Es el hallazgo que
  reordeno el plan (seccion 3 de `PLAN_OLA4.md`) y vale para leer cualquier numero de la planilla
  de EPILAB contra cualquier numero nuestro. En el resumen de la ola 3 el mismo problema aparece
  un nivel mas abajo y **ya esta resuelto**: `hits_bowtie` cuenta alineamientos y
  `hits_blanco_principal` cuenta ventanas `[M]`.
- **La base de una corrida puede borrar un gen entero de la tabla.** `ATPaseD_Dm` esta anotado en
  la hebra reversa del cromosoma, asi que contra el genoma de *Dalbulus maidis* cuarenta de sus
  cuarenta y dos ventanas eficientes pegan solo en `-`, y como el original evalua la eficiencia
  unicamente para aciertos en `+`, la fila da **0** `[M]`. Es una trampa de la herramienta, no de
  nuestros datos, y afecta a cualquier corrida con base genomica.
- **`GCF_002217175.1` no es el transcriptoma de *D. maidis*.** El plan y el issue #5 lo nombran
  asi; el archivo dice *Folsomia candida*. En `work/offtarget_db/` hay genoma de *D. maidis* y
  ningun transcriptoma suyo.
