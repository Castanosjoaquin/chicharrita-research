# Notas de la linea M8 (ola 4)

Esta linea no midio nada nuevo con el motor: junto lo que ya estaba medido en otras cuatro lineas
y lo ordeno como respuesta a la ultima pregunta de la carta. Por eso lo que toca llevar a
`00_meta/` es poco y es casi todo pendientes.

---

## Que se llevo a `00_meta/`

- **`PREGUNTAS_ABIERTAS.md`**: una entrada fechada con las siete variables biologicas y lo que
  falta de cada una. Van juntas y no separadas porque son pedidos que se le pueden hacer al
  investigador en la misma conversacion del lunes.
- **`DECISIONS.md`**: nada. M8 no decide; describe los limites de un numero que ya se usa y
  reafirma dos decisiones que ya estaban tomadas (D24, los dos ejes separados; D38, las dos listas
  sin comparar entre si).
- **`CAMINOS_PROBADOS.md`**: nada nuevo. El unico descarte de la linea fue no volver a correr
  nada, y esa es la premisa del plan para M8, no un intento fallido.

## Donde corrio, y por que eso no limita el resultado esta vez

Windows 11, **Python 3.10.11, solo biblioteca estandar**, igual que M1. A diferencia de M1, aca
eso no limita nada: la unica cuenta de la linea es una division y un ordenamiento sobre conteos
que ya estan en el repositorio. No hizo falta ViennaRNA, ni Bowtie, ni `work/`, ni las secuencias
de EPILAB.

## Que se verifico antes de escribir

`python scripts/test_densidad.py` -> **7 de 7**. Las pruebas no verifican el informe entero:
verifican las tres afirmaciones de la seccion 1, que son las unicas que la linea calcula.

1. Que la cantidad de ventanas sale del largo de la secuencia, con el caso de `BicC_Dm` aparte
   porque es donde el denominador se puede equivocar: son 2.500 ventanas y no los 2.504 hits que
   informa el programa original.
2. Que la densidad es eficientes por 100 ventanas, con dos valores calculados a mano.
3. Que en las cuatro configuraciones medidas el primero por conteo crudo y el primero por
   densidad son genes distintos, que es la afirmacion que sostiene el limite 1.

Los numeros de las secciones 2, 3 y 4 **no se recalcularon**: son citas a corridas de W5, C2, C3,
C13 y la matriz de M1, cada una con su archivo. Esta linea los transcribe y los ordena; si alguno
de esos informes cambia, este tambien hay que tocarlo, y ya paso una vez: la seccion 2 se
reescribio el mismo dia, cuando la matriz de M1 corrio y convirtio en medicion la hipotesis que
el borrador citaba como pendiente (D52).

## Confidencialidad

Ningun archivo de esta linea contiene secuencia. `densidad.py` guarda largos (1263, 528, 2520,
491) y conteos, que son metadatos ya publicados en el entregable, no nucleotidos. No se abrio
ninguna secuencia de EPILAB y no salio nada de la maquina.

## Que sirve de lo que salio

El parrafo de la seccion 7 esta escrito para copiarse a la casilla de validacion del entregable
tal como esta. La tabla de la seccion 1 sirve sola como respuesta a la pregunta del investigador:
es la que muestra que el conteo crudo y la densidad no ordenan igual en ninguna de las cuatro
configuraciones medidas, incluida la suya.
