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
| [`M4_evidencia_y_potencia/`](M4_evidencia_y_potencia/REPORT.md) | Que evidencia distinguiria los dos modos del port y cuanta hace falta. Con los 29 siRNA de Cedden la comparacion **no podia salir distinta** (un solo discordante, p exacto 1,00); replicando ese diseno harian falta **2.784** (y 232 es el piso optimista, que supone que todos los discordantes se parecen al unico observado). El inventario de fuentes de etiquetas dice que ese numero es inalcanzable con datos abiertos, y el ensayo prospectivo que si discrimina pide **32 siRNA por brazo**. | completa: los tres criterios de terminado cumplidos, mas el preregistro del analisis de M3 |
| [`M7_robustez_bicc/`](M7_robustez_bicc/REPORT.md) | Si la ventaja de `BicC_Dm` 922-1221 aguanta los parametros y la referencia. Sobre **4.368 configuraciones** le gana a la region del laboratorio (264-563) en el 99,1 % contando dentro del gen y en el 99,6 % contando la molecula recortada, pero a 2121-2420 solo en el **36,4 %** en contexto —15,7 % en modo corregido— y en el **75,6 %** recortada: el marco de conteo decide tanto como los umbrales. La cifra que se publica es **26** y no 36. Y `GCWP01` no cubre un solo nucleotido de 922-1221, asi que el «32 contra 22» de D25 compara una region contradicha con una no mirada. El tercer eje se midio como **sensibilidad y no como adopcion**: la eleccion de criterio de riesgo no cambia quien gana (36,4 % a 35,3 % en contexto), pero bajo la regla mecanicista el riesgo de las tres regiones es **cero**. | **parcial por diseno:** los tres ejes medidos; la regla de alertas la decide M6 (#10) |

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
- **Para comparar dos criterios, lo que cuenta es la discordancia y no el n.** Con k casos en los
  que los dos criterios difieren, la prueba de aleatorizacion por intercambio no puede dar un p
  menor que 2/2^k, asi que con menos de **6** discordantes ningun dato alcanza alfa 0,05 `[M]`. En
  los 29 siRNA de Cedden hay **uno**, de modo que la validacion de C9 no tenia forma de salir
  distinta. Antes de pedir mas etiquetas, contar discordantes
  (`research/ola4/M4_evidencia_y_potencia/`).
- **`GCF_002217175.1` no es el transcriptoma de *D. maidis*.** El plan y el issue #5 lo nombran
  asi; el archivo dice *Folsomia candida*. En `work/offtarget_db/` hay genoma de *D. maidis* y
  ningun transcriptoma suyo.
