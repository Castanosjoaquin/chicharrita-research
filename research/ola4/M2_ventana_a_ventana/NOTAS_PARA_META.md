# Notas para el meta — M2

## Para `PREGUNTAS_ABIERTAS.md`

- **El par de motores quedó resuelto compilando ViennaRNA 2.1.5**, y conviene que el equipo
  sepa que ya no hace falta Windows para correr el backend `exe`: el port lee la ruta del
  binario de la variable `SIFI_RNAPLFOLD`, y la receta de compilación está en el encabezado
  de `scripts/correr_pares.py`. El binario no se versiona, pero se rehace en minutos.
- **La atribución de `RNA_NN4` a Zuber et al. 2022** sigue `[?]`: sale del comentario de
  `freeEnergy.py:306` y el artículo no se abrió. Ya estaba anotado; lo que cambió es que
  ahora la tabla está transcrita en el port, así que la pregunta pasa de ser sobre un
  parámetro ajeno a ser sobre uno que usamos.
- **La ventana de `BicC_Dm` que cruza por `end_stability` en el par de recorte.** El ΔG no
  depende del contexto salvo en las dos primeras ventanas del recorte, donde el motor usa
  `_ends_plain` porque no existe el siRNA de dos posiciones antes. La explicación es
  nuestra y no está verificada contra el fuente `[H]`.

## Para `CAMINOS_PROBADOS.md`

Nada que descartar, y una corrección a registrar: esta línea **primero declaró el par 3
como no corrible** con el argumento de que una compilación propia de 2.1.5 no serviría como
control, porque el criterio pide reproducir números medidos con el binario del instalador.
El argumento era malo y la vía sí funcionaba: el binario del instalador **es** ViennaRNA
2.1.5, y la compilación del tag oficial reproduce los seis números publicados —los cuatro
conteos en los dos modos y el control de 19, 7, 50 y 8—. Lo que hacía falta no era
descartar la vía sino poner el ancla que la valida.

## Correcciones que esta línea confirma

- Los «27 cambios de veredicto por borde» del criterio de terminado del issue son del
  conjunto `recomendadas`. Con las regiones vigentes son **23**, medido de forma
  independiente acá. Coincide con la corrección que ya había detectado la sesión que
  trabajó el issue.
- Los «19, 7, 50 y 8» son del backend `exe`, y **se reproducen exactos** con el 2.1.5
  compilado. Con ViennaRNA 2.7.2 el mismo par da 19, 9, 52 y 6, y el total pasa de 84 a 86
  ventanas. No era discrepancia: era otro motor.

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

Y un dato que sirve más allá de M2: **el backend `exe` ya se puede correr en esta máquina**,
así que cualquier cifra de la ola 2 o 3 medida con RNAplfold 2.1.5 es reproducible acá sin
depender de Windows. Eso destraba, por ejemplo, el eje de motor que M1 dejó planteado para
los puntos intermedios 2.4.x y 2.6.x.
