# Notas de la línea V2 (`Rpn6`), para integrar a `00_meta/`

Esta línea **no** tocó `00_meta/`: el árbol estaba compartido con otras dos sesiones (la demo de
lectura y la línea de quimeras y homología), y la regla del repo es agregar por ruta y no editar
archivos de los que otro puede estar escribiendo. Lo que sigue son **candidatas**, para
consolidar cuando se integre la ola 7. La última ADR al momento de escribir esto es `D102`.

## Decisiones candidatas

**(a) Un candidato recuperado por homología se compara con los del laboratorio sólo dentro de la
misma cohorte de ejes.** `F3` ya tenía las cohortes; esta línea muestra por qué importan: `Rpn6`
pasa de «primero de su cohorte» a «equivalente a `BicC`» cuando se le miden los mismos ejes sobre
la secuencia propia. Un puntaje construido sobre menos ejes no se pone en la misma columna.

**(b) Una ventaja en un eje del ranking no se reporta sin su nulo.** Es la consecuencia directa
del resultado: una diferencia de limpieza de 0,0026 parecía una ventaja y cayó en el percentil
51,6 del azar. Propuesta: toda comparación de limpieza entre regiones lleva el percentil del nulo
al lado, o se declara «no evaluada».

**(c) La limpieza de una región se calcula siempre con `ranking.ejes()`, nunca con una definición
propia.** Lo aprendí equivocándome (ver `REPORT.md` §0): la fracción de ventanas sin bloque de
≥ 19 nt **no** es la limpieza del proyecto, que pondera por referencia y por criterio e incluye
`mm1_21`. Las dos cifras difieren lo suficiente para dar vuelta una conclusión.

**(d) El marco de conteo decide el veredicto de una comparación, no sólo su magnitud.** `D63` ya
declaraba los tres marcos. Acá, el mismo par de regiones se compara al revés según el marco: en
recorte `Rpn6` gana o empata en el 70,5 %, en contexto en el 40,1 %. Propuesta: toda comparación
entre regiones de genes distintos declara el marco **en la misma frase** que el número.

## Entradas candidatas para `PREGUNTAS_ABIERTAS.md`

1. **Los aciertos secundarios de `Rpn6` no están resueltos:** `GITV01001189.1` (98,6 % sobre
   277 aa) y `GITV01003958.1` (96,0 % sobre 225). No se sabe si son fragmentos del mismo
   transcripto, isoformas o parálogos. Si fueran parálogos, habría riesgo de off-target **dentro
   de la propia especie**, que el panel de seis no ve.
2. **El contig viene de un TSA y no tiene estructura exónica.** Correr `miniprot` contra el genoma
   `ihDalMaid1.1` diría si 325-624 cae en un exón único o la parte un intrón.
3. **Las dos posiciones divergentes (21 y 261 de la región) son sinónimas y aparecen idénticas en
   Argentina e Illinois.** Es compatible con variación real entre poblaciones, pero con dos
   fuentes no se puede separar de un error de secuenciación; Illinois es 454.
4. **`RNAplfold 2.1.5` sigue sin binario en esta máquina.** El eje del motor de `M7` no se pudo
   barrer para `Rpn6`; son cuatro ejes de cinco.
5. **La región 325-624 no está en el inventario de alertas de `M6`.** La compuerta de `D72` la
   rechaza como recomendación, y así debe seguir hasta que se tamice y se firmen sus filas.

## Para `CAMINOS_PROBADOS.md`

**Comparar contra una cifra publicada sin recalcularla con la misma función.** La primera versión
de esta línea comparó una limpieza propia contra la de `ranking.ejes()` y concluyó una ventaja que
no existía. El patrón que funcionó fue el de `O3`: importar `ranking.py` por `sys.path` y pasar
las dos regiones por la **misma** llamada. Vale como regla general y no sólo para este eje.

## Para el glosario

- **nulo de regiones**: el conjunto de limpiezas de todas las regiones de 300 nt de N permutaciones
  del gen que conservan composición. Sirve para decir si la limpieza de una región real se
  distingue del azar. Es un **piso**: no conserva uso de codones ni repeticiones.
