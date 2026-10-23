# M7 — lo que va a `00_meta/`, separado por destino

Fecha: 2026-10-23. Fuente de todo lo de acá: [`REPORT.md`](REPORT.md) y `resultados/`.


## Para `DECISIONS.md`

**Entrada nueva, a redactar con el investigador: la cifra que se publica es la de la molécula recortada.**
Decisión: todo entregable que informe «ventanas eficientes» de una región candidata publica el conteo de la **molécula de 300 nt plegada sola** y, al lado, el de la región dentro del gen, diciendo cuál es cuál. Para `BicC_Dm` 922-1221 son **26** y 36 `[M]`. Criterio: lo que se sintetiza es la molécula, y las diez ventanas de diferencia se reparten en siete que caen en los veinte últimos arranques del tramo —que en el gen siguen teniendo 21 nt por delante y en la molécula no— más tres que cambian de veredicto al plegarse sin contexto. Consecuencia: las tres regiones candidatas de `BicC_Dm` cambian de conteo al recortarse y **en direcciones distintas** (922-1221 pierde 3, 2121-2420 pierde 5, 264-563 gana 2), así que un ranking construido sobre conteos en contexto no es el mismo que sobre moléculas recortadas. M7 no tocó el ranking.

**Enmienda a D25 (la región de `BicC_Dm` pasa a 922-1221, por conservación).**
La decisión se sostiene, pero su criterio principal está mal leído y hay que reescribirlo. D25 dice «32 de 36 idénticas en los tres transcriptomas contra 22 de 35». Medido por fuente separada `[M]`: en el transcriptoma argentino las dos regiones conservan el 100 % de sus eficientes (36/36 y 35/35); en el de Ohio, 2121-2420 conserva 33 de 35 y 922-1221 conserva 32 de 36, o sea que ahí la región de C7 está **mejor**; y en el de Illinois (`GCWP01`) 922-1221 **no tiene una sola ventana con datos**, porque esa fuente cubre 609 de los 2.520 nt del gen y ninguno de ellos cae en 922-1221. El «32 contra 22» surge de contar la ausencia de datos como ausencia de contradicción. Lo que sigue sosteniendo D25 es el genoma del Reino Unido (36 de 36 idénticas contra 27 idénticas y 8 que cruzan un empalme, `[M]` de esta línea) y el ensamblado de Córdoba (C8, no remedido acá).

**Nota para cualquier decisión futura que use conteos de si-Fi21.**
Los conteos de RNAplfold 2.1.5 y los de ViennaRNA 2.7.2 no son comparables, y el motor **da vuelta** la comparación entre 922-1221 y 2121-2420 en el punto por defecto del modo corregido: 36 contra 35 con ViennaRNA 2.7.2 y 30 contra 32 con RNAplfold 2.1.5 `[M]`. Toda cifra publicada tiene que declarar motor y tabla de apilamiento.


## Para `PREGUNTAS_ABIERTAS.md`

1. **La pregunta que dejó M2 y que M7 contesta a medias.** Santino preguntó si las dos primeras posiciones de un recorte —donde el original calcula los extremos sin nucleótidos colgantes— se excluyen de la comparación entre regiones o se reportan con la advertencia. Medido: de las dieciséis ventanas que cambian de veredicto al recortar las tres regiones, **una sola** cae ahí, y excluir esas dos posiciones de las 4.368 configuraciones mueve la fracción de victorias de 75,6 % a 74,2 % `[M]`. Propuesta: **reportar con la advertencia, sin excluir**, y dejar la columna «recorte sin bordes» en el TSV. Falta que el investigador lo confirme.
2. **El eje de criterios de riesgo sigue abierto** y no es de esta línea: depende de la decisión de M6 (#10) sobre qué alertas son bloqueantes. Qué haría falta, en `REPORT.md` §5.
3. **Falta el transcriptoma de *D. maidis* del laboratorio** (pedido 2 del lunes). Las tres fuentes públicas no son poblaciones de campo del noroeste argentino, y la única argentina es una colecta de 2015.
4. **Por qué el corte de accesibilidad decide la comparación.** En contexto, 922-1221 le gana a 2121-2420 en el 68,4 % de las celdas con accesibilidad de 0,05 a 0,10 y en el 0 % por encima de 0,25 `[M]`. La hipótesis es que 2121-2420 tiene más ventanas con accesibilidad intermedia-alta; no está medida la distribución del término, que es lo que lo contestaría (la tabla de `--features` de M3 ya tiene los insumos).
5. **Dentro de 922-1221 hay un empalme**, cerca de la posición 1118 del gen: veinte de sus 300 ventanas no existen como tramo contiguo del genoma del Reino Unido `[M]`. Ninguna es eficiente, así que no afecta al diseño, pero sí a cualquier búsqueda de off-targets con base genómica. Habría que revisar si las búsquedas publicadas de la ola 3 lo tuvieron en cuenta.


## Para `CAMINOS_PROBADOS.md`

- **Se probó alinear con blastn local en vez de `PairwiseAligner`, y conviene.** C8 alineó el gen contra una lista de contigs TSA escrita a mano; M7 lo hizo con blastn contra las bases de `work/W5/db/` sin lista previa, y reprodujo los conteos de C8 por fuente (GHCC01 2417 idénticas y 83 variantes; GITV01 2353 y 147; GCWP01 419 y 150 sobre 569 con datos) `[M]`. La ventaja no es la velocidad: es que la cobertura aparece sola, y así se vio que `GCWP01` no cubre 922-1221.
- **El eje que pedía el issue —`RNA_NN3` contra `RNA_NN4`— resultó el menos influyente de los cinco.** Mueve la fracción de victorias de 36,4 % a 36,3 % en contexto y de 76,8 % a 74,4 % en el recorte `[M]`. El eje que no estaba en el issue —el motor de plegado— mueve la del recorte de 88,8 % a 62,3 %. Si hay que declarar un eje en el entregable, es el motor.
- **Se descartó comparar los tres recortes con la grilla sin verificar antes el marco.** El primer impulso era medir sólo «la región dentro del gen», que es lo que venía publicando el proyecto; con ese marco la conclusión habría sido que 922-1221 le gana a 2121-2420 en el 36,4 % de la grilla, es decir que pierde. Con el marco de la molécula recortada, que es la que se sintetiza, gana en el 75,6 % `[M]`. El marco de conteo decidía el resultado y no estaba declarado en ningún lado.
- **RNAplfold 2.1.5 compilado desde el fuente oficial corre fuera de Windows** y reproduce los cuatro conteos publicados del binario del instalador. La receta es la de M2; esta línea la volvió a usar tal cual. Dependencias: `autoconf`, `automake`, `libtool`, `gengetopt`.


## Contradicción con lo publicado en `entregables/` — no corregida por esta línea

`entregables/checkpoint2-una-pagina.md` (línea 11) y `entregables/para-el-investigador.md` (fila 4) dicen que 922-1221 «pasa de 20 a 36 ventanas que pasan el filtro» y que tiene «36 ventanas que pasan el filtro, 32 idénticas en los tres transcriptomas públicos». Las dos cifras son del marco en contexto y del criterio que este informe corrige:

| Afirmación publicada | Fuente de la publicada | Lo que mide M7 |
|---|---|---|
| 922-1221 tiene 36 ventanas que pasan el filtro | C8 / D25, conteo en contexto, 300 arranques | 36 en contexto y **26 en la molécula recortada**, que es la que se sintetizaría `[M]` |
| 264-563 tiene 20 | ídem | 20 en contexto y 17 recortada `[M]` |
| 32 de las 36 son idénticas en los tres transcriptomas públicos | C8 / D25 | 36 de 36 en el argentino, 32 de 36 en el de Ohio y **0 de 36 con datos** en el de Illinois, que no cubre la región `[M]` |

Por el alcance de esta línea no se tocó ningún archivo de `entregables/` ni el ranking. La corrección la decide el investigador.
