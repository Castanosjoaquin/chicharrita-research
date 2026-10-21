# Qué validó experimentalmente el artículo de si-Fi21, cómo y con qué resultado

Todo lo de este documento sale del texto completo de Lück S, Kreszies T, Strickert M,
Schweizer P, Kuhlmann M y Douchkov D (2019), *Frontiers in Plant Science* 10:1023,
`10.3389/fpls.2019.01023`, abierto por esta investigación. Cada afirmación lleva su sección,
tabla o figura. `[E]` salvo donde se marque otra cosa.

## El sistema experimental

El organismo es cebada (*Hordeum vulgare* ssp. *vulgare*) y el patógeno es el oídio
*Blumeria graminis* f. sp. *hordei*. El blanco de silenciamiento es *HvMlo*
(HORVU4Hr1G082710), un factor de susceptibilidad cuya represión da resistencia amplia al
oídio; el artículo lo elige precisamente porque la resistencia sirve de lectura fenotípica
del silenciamiento (Introducción, página 2).

El método es silenciamiento génico inducido transitoriamente (TIGS, *transient-induced gene
silencing*): las construcciones se introducen por bombardeo de partículas en células de la
epidermis de segmentos de hoja separados, montados en agar; tres días después se inocula el
hongo, con un aislado suizo de campo (CH4.8) a 150-200 conidios por milímetro cuadrado; a las
48 horas se cuentan las células transformadas teñidas con GUS y, de ellas, cuántas contienen
haustorio —es decir, cuántas fueron penetradas con éxito— (Materiales y Métodos, página 3).

**La medida de eficacia no es el ARN mensajero.** La Discusión (página 8) dice que medir
directamente el descenso del transcrito del gen blanco no es técnicamente viable en este
sistema, porque la respuesta se limita a unas pocas células transformadas, y que por eso se
usa el efecto fenotípico como sustituto (*proxy*) del silenciamiento del transcrito. La
variable es el índice de susceptibilidad relativa (RSI), normalizado contra el promedio de
tres bombardeos paralelos de vector vacío por experimento y transformado a log2; valores más
bajos indican efecto más fuerte (página 5).

**El n.** Cada construcción se probó en un mínimo de cinco repeticiones biológicas
independientes (página 5, con el detalle en la Tabla Suplementaria S2). La comparación
estadística es ANOVA de una vía contra el vector vacío, con corrección de Dunnett para
comparaciones múltiples; en las Figuras 3 y 4 se marcan con estrella las construcciones con
p ajustado menor que 0,05.

## Las dos series de construcciones

**Serie 1, el «reloj molecular».** Sobre una secuencia de 500 pb de la región codificante de
*HvMlo* se generaron variantes sintéticas con un número creciente de nucleótidos aleatorizados,
nombradas de 0MY (sin cambios) a 50MY (completamente aleatoria), simulando 50 millones de años
de divergencia neutral bajo la regla del 2 % por millón de años (páginas 2 y 4, Tabla 1). Como
la sustitución es aleatoria, en uno de cada cuatro casos cae el mismo nucleótido, y por eso la
identidad observada es mayor que el porcentaje aleatorizado: 0MY tiene 100 % de identidad,
1MY 98,0 %, 2MY 96,0 %, 3MY 94,4 %, 4MY 92,2 %, 5MY 90,2 % y 10MY 89,4 % (Tabla 1). Se agregó
*HvMloH1*, un parálogo con alrededor del 85 % de identidad, como ejemplo de off-target real.

**Serie 2, las ventanas de 100 pb.** La misma región de 500 pb se dividió en cinco ventanas de
100 pb y cada una se insertó en su posición correspondiente dentro de la secuencia aleatoria
50MY, de modo que las cinco construcciones tienen el mismo largo total y aproximadamente el
mismo número de siRNA posibles, pero difieren en la accesibilidad local de la región real
(página 5, Figura 2B).

## Los resultados

**Identidad.** La eficacia del silenciamiento cae rápido cuando la similitud global baja del
92 % (construcción 4MY, Figura 3; Discusión, página 8). El artículo aclara dos cosas honestas:
que el efecto más fuerte lo dio 3MY, no 0MY, y que las diferencias entre 0MY y 3MY no son
estadísticamente significativas, porque el sistema involucra dos organismos vivos y tiene
varianza considerable. En paralelo, el número de siRNA predichos en modo de alta eficiencia baja
al bajar la identidad: la Tabla 2 lista 26 para 0MY, 15 para 1MY, 25 para 2MY, 13 para 3MY, 9 para
4MY y 0 desde 5MY.

**Una inconsistencia interna del artículo, que conviene conocer antes de citar números.** `[?]`
La Discusión (página 8) afirma que 0MY genera hasta 480 siRNA distintos, de los cuales **239** en
modo HS y 26 en modo HE, y que «desde la construcción 4MY en adelante el número de siRNA en modo
HE cae a cero». La Tabla 2 dice otra cosa en los dos puntos: para 0MY lista **26** tanto en HS
como en HE, y para 4MY lista **9** en HE, con el cero recién en 5MY. No se puede resolver cuál es
el correcto sin los datos suplementarios (Tabla Suplementaria S4), que están en un archivo aparte
que no se abrió. Al citar, conviene citar la fuente concreta —texto o tabla— y no mezclarlas.

**Correlación entre predicción y efecto.** Es el resultado cuantitativo central. Sobre las doce
construcciones de la Tabla 2, la correlación de Pearson con el efecto medio de silenciamiento es:

| Predictor | Pearson R con el efecto medio |
|---|---|
| si-Fi anterior, hits totales | −0,31 |
| si-Fi anterior, «eficientes» | −0,34 |
| si-Fi21, hits totales | −0,31 |
| si-Fi21, modo alta sensibilidad (HS) | −0,37 |
| **si-Fi21, modo alta eficiencia (HE, el de diseño)** | **−0,61** |

Esa tabla es toda la evidencia cuantitativa de que el criterio predice potencia. La unidad de
análisis es la **construcción** —500 pb, cientos de siRNA posibles— y no el siRNA individual:
**ningún siRNA individual fue medido** en el artículo.

**Ventanas de 100 pb.** Aunque las cinco generan casi el mismo número de siRNA totales (80 u 81),
su efecto sobre la susceptibilidad difiere mucho, y **sólo 401-500W tuvo efecto significativo**
(Figura 4). Dos de las cuatro ineficaces —101-200W y 201-300W— tenían números relativamente altos
de siRNA en modo HE (7 y 7), pero por debajo de los 10 de la ventana activa. Todas dieron números
comparables de siRNA en modo HS, de lo que el artículo concluye que ese criterio **no alcanza**
para predecir silenciamiento eficaz (página 8). Los autores interpretan el conjunto como un
fenómeno de umbral: hace falta cierta «presión de siRNA» sobre el blanco para que el efecto se
manifieste en la ventana corta de observación del TIGS.

**Off-targets.** La validación de especificidad no es un experimento propio sino un reanálisis de
datos ajenos: Xu y colaboradores (2006) habían medido los niveles de transcrito de *AtBTI1* y de
varios parálogos en *Arabidopsis thaliana* silvestre, mutante de inserción y transgénica de ARNi.
Corriendo si-Fi21 en modo HS sobre esas secuencias (Tabla 3), los cuatro genes con reducción de
transcrito confirmada tienen hits predichos —402, 14, 2 y 2 en modo HS— y el único gen sin
reducción (TC275407) tiene **cero** hits en las tres columnas. Son cinco secuencias y la
correspondencia es perfecta.

**Comparación con otras herramientas.** Se compararon siDirect, dsCheck y RNAi Designer contra
si-Fi21 sobre la misma secuencia de referencia (Tabla Suplementaria S1), pero el artículo aclara
que **no fue una comparación contra el resultado experimental**, porque ninguna de las
herramientas en línea admite una base de transcritos de cebada ni bases propias; la comparación
fue por número de siRNA recomendados. La conclusión que el artículo saca —que el mejor ajuste a
los datos experimentales lo da si-Fi21 en modo HE— se apoya entonces en su propia tabla de
correlaciones, no en un cotejo pareado entre herramientas.

## Qué queda validado y qué no

**Validado:** la herramienta completa, en modo diseño, como predictor del efecto relativo entre
construcciones largas, en un sistema planta-hongo, con n = 12 construcciones y una correlación de
−0,61 contra un fenotipo de resistencia. Y el modo off-target como detector de parálogos
efectivamente afectados, con n = 5 secuencias, en otro organismo y con datos de terceros.

**No validado:** ningún umbral por separado. El artículo no compara 1 kcal/mol contra otros
valores, ni 0,1 contra otros, ni u = 8 contra otros, ni mide el aporte marginal de la regla
terminal sobre las condiciones termodinámicas. No hay curva ROC, ni validación cruzada, ni
conjunto de prueba independiente para la regla de eficiencia; el único conjunto independiente del
artículo es el reanálisis de off-targets.

**Y no hay ningún insecto.** Toda la validación experimental es en cebada. Para el proyecto esto
es lo decisivo: aplicar el criterio a *Dalbulus maidis* es una extrapolación entre reinos, y la
única evidencia primaria de las reglas de secuencia que lo componen viene de células de mamífero
(Ui-Tei 2004, que además reporta que en *Drosophila* in vivo casi no se detecta preferencia de
secuencia).

`[H]` La forma defendible de usar esto ante el investigador no es «si-Fi está mal validado», que
sería injusto: para 2019, y para un laboratorio de patología vegetal, una correlación de −0,61 en
un bioensayo de dos organismos vivos con cinco réplicas es un resultado razonable. La forma
defendible es «si-Fi está validado para una pregunta distinta de la nuestra»: predecir qué
fragmento largo de un gen de planta conviene usar en una construcción de silenciamiento,
evaluado por fenotipo, en un sistema donde el ARN se produce dentro de la célula. Nuestro
problema —priorizar fragmentos para entrega exógena a un insecto— comparte la mecánica molecular
pero no el sistema de validación.
