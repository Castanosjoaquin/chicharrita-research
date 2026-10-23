# Notas para el meta — M2

## Para `PREGUNTAS_ABIERTAS.md`

- **El par de motores sigue sin correr, y es un insumo, no una pregunta.** Falta el
  `RNAplfold.exe` del instalador de si-Fi2015, o los TSV por ventana con backend `exe` de
  los cuatro genes. Con cualquiera de los dos se cierra el par 3 y además se pueden correr
  los dos controles numéricos del issue en el motor en que fueron medidos. La máquina que
  corrió M1 lo tiene. **Es el único faltante de esta línea.**
- **La atribución de `RNA_NN4` a Zuber et al. 2022** sigue `[?]`: sale del comentario de
  `freeEnergy.py:306` y el artículo no se abrió. Ya estaba anotado; lo que cambió es que
  ahora la tabla está transcrita en el port, así que la pregunta pasa de ser sobre un
  parámetro ajeno a ser sobre uno que usamos.
- **La ventana de `BicC_Dm` que cruza por `end_stability` en el par de recorte.** El ΔG no
  depende del contexto salvo en las dos primeras ventanas del recorte, donde el motor usa
  `_ends_plain` porque no existe el siRNA de dos posiciones antes. La explicación es
  nuestra y no está verificada contra el fuente `[H]`.

## Para `CAMINOS_PROBADOS.md`

Nada que descartar. Lo que sí conviene registrar es que **compilar ViennaRNA 2.1.5 desde
fuente se consideró y se descartó** como vía para el par 3: el criterio de terminado pide
reproducir números medidos con el binario del instalador, y otra compilación probaría otra
cosa.

## Correcciones que esta línea confirma

- Los «27 cambios de veredicto por borde» del criterio de terminado del issue son del
  conjunto `recomendadas`. Con las regiones vigentes son **23**, medido de forma
  independiente acá. Coincide con la corrección que ya había detectado la sesión que
  trabajó el issue.
- Los «19, 7, 50 y 8» son del backend `exe`. Con ViennaRNA 2.7.2 el mismo par da
  **19, 9, 52 y 6**, y el total pasa de 84 a 86 ventanas. No es discrepancia, es otro motor.

## Para el entregable, si hace falta

Dos cifras presentables, las dos medidas con herramienta y no a mano:

1. **La diferencia entre `sifi21INTA` y el original es la tabla de energía.** Con `RNA_NN4`
   el port da 138, 40, 218 y 35, que es exactamente lo que el entregable ya declara para
   `sifi21INTA`. Ese eje queda cerrado.
2. **Entre los dos modos no cambia ningún término, cambia cómo se combinan.** Las 86
   ventanas que difieren caen todas en la rama del atajo y todas en la misma dirección.

## Para quien retome

El comparador está listo para la salida por ventana de Diego, que es la tercera tarea del
issue: es la misma herramienta con `--etiquetas nuestro,suyo`. Lo que falta es el archivo,
que es el pedido 1 del lunes.
