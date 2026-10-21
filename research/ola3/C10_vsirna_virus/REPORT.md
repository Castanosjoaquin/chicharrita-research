# C10 — ¿Existen datos de ARN pequeños derivados de virus para nuestro blanco?

**La pregunta.** Si el hospedador fabrica ARN pequeños cortando el ARN del virus, ese mapa es una **observación** de qué ventanas se procesan de verdad y se cargan en RISC, no una predicción nuestra. Serviría como verificación externa del criterio de accesibilidad de si-Fi21, que es el único de sus tres filtros que no mostró valor predictivo sobre la eficacia medida. Esta nota contesta si esos datos existen y qué dicen.

**Qué se buscó y cómo.** Europe PMC (siete consultas) y NCBI por E-utilities (ocho consultas, bases `sra` y `gds`), el 2026-10-21. Los conteos crudos están en `datos/`. No se subió ninguna secuencia a ningún servicio: las consultas son por nombre de organismo y de virus.

## La respuesta corta

**Para el *Maize rayado fino virus* (MRFV) y para *Dalbulus maidis* no existen datos de ARN pequeños.** `[E]` En SRA, MRFV como organismo devuelve **0** registros, y MRFV cruzado con estrategias de ARN pequeño (`miRNA-Seq`, `ncRNA-Seq`) también **0**. Los 16 aciertos de MRFV por texto libre son los transcriptomas de *D. maidis* que ya conocíamos, que lo nombran en los metadatos. *D. maidis* tiene 37 registros —genoma, ADN y transcriptoma— y **0** con estrategia de ARN pequeño. En GEO, cero para ambos. En Europe PMC ningún trabajo perfila ARN pequeños derivados del MRFV.

Es un **vacío documentado**, no una búsqueda fallida: el método es rutinario —hay 1.706 corridas de `miRNA-Seq` en *Zea mays*— y simplemente nadie lo aplicó a este patosistema. Para nuestro blanco, la versión directa de la idea **no se puede correr hoy**.

## Lo que sí existe, y por qué conviene leerlo antes de insistir

Dos trabajos abiertos perfilan ARN pequeños virales en hospedadores comparables, y los dos contestan de antemano la pregunta que motivaba el ejercicio.

**Primero: los puntos calientes no se correlacionan con la estructura del ARN.** En *Mal de Río Cuarto virus* (MRCV), que causa pérdidas importantes en maíz en la Argentina, los autores probaron exactamente esa hipótesis sobre trigo y su vector delfácido *Delphacodes kuscheli*, con RNAfold del paquete ViennaRNA —la misma familia de herramienta que calcula la accesibilidad en si-Fi21— y **no detectaron una correlación clara entre los puntos calientes y la estructura secundaria**. `[E]` Es una tercera línea independiente contra el criterio de accesibilidad, que se suma a las dos que el repositorio ya tenía medidas.

**Segundo, y más importante para el diseño: los puntos calientes dependen del hospedador, no sólo de la secuencia viral.** En MRCV no hay puntos calientes comunes a los dos hospedadores. `[E]` En *Rice dwarf virus* la misma comparación da lo mismo: el segmento más cortado es S1 en el cicadélido *Nephotettix cincticeps*, S11 en cultivo celular del vector y S9 en arroz, y los puntos calientes se agrupan en las **regiones terminales** de los segmentos. `[E]` Hay además unas 50 veces más ARN pequeños virales en arroz que en el cicadélido, lo que los autores atribuyen en parte a que los cicadélidos carecen de genes RDR. `[E]`

La consecuencia es directa sobre tu idea: **dónde corta el hospedador no es una propiedad transferible de la secuencia del virus.** Si eligiéramos regiones blanco copiando los puntos calientes naturales, la respuesta cambiaría según de qué hospedador se secuenciaron, y no habría forma de decidir cuál es el correcto para nuestro caso.

**Un dato colateral que toca D35.** En el cicadélido de *Rice dwarf virus* domina la clase de 21 nt; en arroz dominan 21 y 22 nt; en el delfácido de MRCV el pico está en 22 nt, seguido de 21 y 23. `[E]` La ventana de 21 y 22 nt que el equipo fijó por evidencia biológica queda respaldada también por estos conteos, con la salvedad de que son otros insectos y otros virus.

## Qué se puede hacer con esto, y qué no

No se puede verificar el criterio de accesibilidad sobre nuestro blanco: faltan los datos y no hay forma de producirlos sin laboratorio. `[H]`

Sí se puede, como **ablación declarada sobre datos ajenos**: los ARN pequeños de *Rice dwarf virus* están depositados en SRA bajo el proyecto **PRJNA541035**, con hospedador cicadélido, que es lo más cercano taxonómicamente a *D. maidis* que apareció. Correr nuestro filtro sobre ese genoma viral y contrastar las ventanas que marca contra las que el cicadélido corta de verdad sería la primera prueba externa del criterio. El resultado esperable, a juzgar por los dos trabajos de arriba, es que no coincidan; eso sería un hallazgo sobre el criterio, no sobre nuestros candidatos. `[H]`

Lo que **no** sería válido es pasar genomas de virus emparentados por nuestro propio filtro, quedarse con las regiones que el filtro prefiere y presentarlas como mejores. Sin un desenlace medido, eso es el mismo puntaje sin validar aplicado a más secuencias. `[H]`

## Límites de esta nota

Se consultaron Europe PMC y NCBI, no Scopus ni Web of Science, y OpenAlex quedó afuera porque el conector pide una clave que no está configurada. Una ausencia en SRA y GEO no prueba que el dato no exista en un suplemento sin depositar. Las dos fuentes centrales se leyeron a texto completo; el resto de los títulos se usó sólo para delimitar el panorama y figura en `sources.json` con ese alcance. No se descargó PRJNA541035 ni se corrió ninguna comparación: esta nota contesta si los datos existen, nada más.
