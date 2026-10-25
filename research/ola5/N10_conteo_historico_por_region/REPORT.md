# N10 — La función histórica aplicada a regiones: el 36 contra 35 es un empate

**Ola 5, línea N10.** Fecha: 2026-10-25. No sale de la carta: sale de la pregunta que abre el
hallazgo de [`N1`](../N1_regla_de_conteo/REPORT.md) y que no estaba en el plan. Reproducible con
`scripts/conteo_region.py`. Marcadores de `CLAUDE.md`.

## El resultado, en un párrafo

`N1` midió el sesgo de la función histórica sobre **genes completos**. Pero las cifras con las que
se elige una región candidata son conteos de **región**, y si la planilla los construyó con el
mismo contador, entonces nuestro número y el suyo no son el mismo **y el orden entre candidatas
podría no ser el mismo tampoco**. Medido: **lo es en dos de los tres marcos y no en el tercero**.
En el marco de contexto, la ventaja de `BicC_Dm` 922-1221 sobre la región de C7 —36 contra 35, una
ventana— **se convierte en un empate, 33 a 33** `[M]`. En el marco de los comparables queda 26
contra 25 y en la molécula 23 contra 21: el orden se mantiene, con el margen reducido. Contra la
región del laboratorio la ventaja no se mueve en ningún marco.

> **Lo que se deduce** `[H]`. El margen de una ventana del punto por defecto nunca fue una
> diferencia, y ahora hay una segunda razón independiente para decirlo: no sobrevive a la grilla de
> parámetros (`M7`: 36,4 % de 4.368 configuraciones) **y no sobrevive al contador con el que la
> planilla está escrita**. La afirmación que sostenemos sigue siendo «no 264-563», que aguanta las
> dos cosas.

## 1. Las dos lecturas posibles, y que dan lo mismo

No sabemos sobre qué secuencia se construye la curva cuando el laboratorio informa una región, así
que el script no elige: reporta las dos lecturas en paralelo. Es la misma decisión de diseño que
tomó `M1` con las tres agregaciones de la tabla del original.

- **`historico_region`**: la región es el universo. Una ventana eficiente en `p` no se cuenta si la
  de `p − 20` también es eficiente **y cae dentro de la región**.
- **`historico_gen`**: la curva se construye sobre el gen completo y se leen los incrementos que
  caen dentro de la región. Una ventana del borde izquierdo puede quedar tapada por una vecina que
  está **afuera** de la región.

`[M]` **Las dos lecturas coinciden en las seis regiones y en los dos marcos de contexto.** Ninguna
ventana queda tapada por un vecino de afuera de su región, así que no hace falta saber cuál de las
dos usó el laboratorio. Eso cierra una ambigüedad que podría haber quedado abierta.

## 2. Los conteos

`[M]` Punto por defecto, modo `corregido`, ViennaRNA 2.7.2, tabla `RNA_NN3`. «Directo» es lo que
publicamos hoy; «histórico» es el conteo por incrementos con ancho 20. Fuente:
`resultados/conteo_region.tsv`.

| Región | Marco | Directo | Histórico | Tapadas | Sesgo |
|---|---|---:|---:|---:|---:|
| `MP_MRFV` 72-271 | contexto, todos | 38 | 31 | 7 | 18,4 % |
| | comparables | 31 | 25 | 6 | 19,4 % |
| | molécula | 27 | **21** | 6 | 22,2 % |
| `CP_MRFV` 99-298 | contexto, todos | 21 | 19 | 2 | 9,5 % |
| | comparables | 20 | 18 | 2 | 10,0 % |
| | molécula | 23 | **21** | 2 | 8,7 % |
| `BicC_Dm` 922-1221 | contexto, todos | 36 | 33 | 3 | 8,3 % |
| | comparables | 29 | 26 | 3 | 10,3 % |
| | molécula | 26 | **23** | 3 | 11,5 % |
| `ATPaseD_Dm` 72-371 | contexto, todos | 21 | 21 | 0 | **0 %** |
| | comparables | 17 | 17 | 0 | **0 %** |
| | molécula | 20 | **20** | 0 | **0 %** |
| `BicC_Dm` 2121-2420 | contexto, todos | 35 | 33 | 2 | 5,7 % |
| | comparables | 27 | 25 | 2 | 7,4 % |
| | molécula | 22 | **21** | 1 | 4,5 % |
| `BicC_Dm` 264-563 | contexto, todos | 20 | 19 | 1 | 5,0 % |
| | comparables | 15 | 15 | 0 | **0 %** |
| | molécula | 17 | **17** | 0 | **0 %** |

`[M]` **El sesgo por región va de 0 % a 22,2 %**, y el extremo inferior es exacto: la región
vigente de `ATPaseD_Dm` no pierde una sola ventana en ninguno de los tres marcos, y la de
`BicC_Dm` 264-563 no pierde ninguna en dos de los tres. `[H]` Refuerza lo de `N1` y lo empeora: si
el sesgo de un gen ya era desparejo, el de una región puede ser cero o más de un quinto, así que
**comparar una cifra histórica de una región contra una cifra histórica de otra es comparar dos
números que perdieron fracciones incomparables**.

## 3. El orden entre las tres regiones de `BicC_Dm`

`[M]` Fuente: `resultados/conteo_region.json`, clave `ordenes`.

| Marco | Lectura | 922-1221 | 2121-2420 | 264-563 | ¿Gana 922? |
|---|---|---:|---:|---:|---|
| contexto, todos | directo | 36 | 35 | 20 | sí, por 1 |
| contexto, todos | **histórico** | **33** | **33** | 19 | **empate** |
| comparables | directo | 29 | 27 | 15 | sí, por 2 |
| comparables | histórico | 26 | 25 | 15 | sí, por 1 |
| molécula | directo | 26 | 22 | 17 | sí, por 4 |
| molécula | histórico | 23 | 21 | 17 | sí, por 2 |

`[M]` El empate aparece **sólo** en el marco de contexto, que es justamente el marco en el que `M7`
ya había medido que la ventaja no sobrevive a la grilla. En los otros dos el orden se mantiene y el
margen se reduce a la mitad. Contra 264-563 la ventaja es intacta en los tres marcos y en las dos
lecturas.

`[H]` La lectura para la reunión no es que la región se caiga: es que **el argumento de conteo
contra 2121-2420 no existe**, y lo decimos nosotros con tres mediciones independientes que apuntan
al mismo lado —la grilla de parámetros, el marco de conteo y ahora el contador—. Lo que sostiene a
922-1221 frente a C7 es el perfil de off-target y la conservación por fuente, no el número de
ventanas.

## 4. Lo que esto no dice

`[?]` No sabemos si la planilla usó este contador para las cifras de región o sólo para los cuatro
genes completos. Es la pregunta 2 de las nuevas de `PREGUNTAS_ABIERTAS.md` y la contesta él. Si fue
sólo para los genes, esta línea mide una propiedad del contador y no un defecto de la planilla.

`[?]` Tampoco sabemos si, cuando el laboratorio informa una región, pliega el fragmento o lee un
tramo de la curva del gen. Las dos lecturas dan lo mismo en estos seis casos, así que la pregunta
no bloquea nada acá, pero puede no dar lo mismo en otra región.

## Archivos

| Archivo | Qué es |
|---|---|
| `scripts/conteo_region.py` | los tres conteos por región y por marco, con las anclas de `N3` y el chequeo de orden |
| `resultados/conteo_region.tsv` | la tabla de la sección 2 |
| `resultados/conteo_region.json` | lo mismo, más el orden de las tres regiones en cada lectura |
