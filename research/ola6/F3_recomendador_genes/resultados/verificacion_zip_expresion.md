# ¿Trae el zip de Diego el eje de expresión en el tejido expuesto?

**Fecha: 2026-10-27.** Verificación pedida por el equipo después de escribir el
`PREREGISTRO.md`, que declara ese eje como faltante. El issue #27 lo dejaba planteado con
estas palabras: «habría que ver si el zip lo trae».

**Respuesta: no, y no por un descuido del envío.** El eje 5 del preregistro queda declarado
faltante, sin cambios.

## Qué hay en el zip

Un solo archivo: `work/zip_diego/Dalbulus_maidis_transcriptome_GITV01.fas`, 100.291.817
bytes. Ninguna tabla de expresión, ningún archivo de conteos, ningún metadato de muestra
`[M]`.

Medido con un script propio, con el archivo pasado como argumento y sin ejecutar nada que
venga del directorio del zip:

| Medición | Valor |
| --- | ---: |
| secuencias | 56.117 |
| pares de bases | 94.702.486 |
| la más larga | 205.383 |
| la más corta | 200 |
| mediana de longitud | 1.091 |

Las cuatro primeras **reproducen exactamente** las estadísticas oficiales del TSA que `W3`
había bajado del FTP del NCBI en la ola 2 —
`NCBI_TSA_master|GITV|01|NT-Sequences|56117|Basepairs|94702486|NT-Largest|205383|NT-Smallest|200`,
en `research/ola2/W3_bases_datos/consultas/05_tsa_y_ftp.md` `[M]`. O sea que el zip es el
conjunto público `GITV01`, no un dato no publicado, y coincide con lo que la línea `F1` ya
había medido en el issue #25.

## Por qué no podía traerlo

Un TSA es un **ensamblado**: un conjunto de contigs, sin abundancia por muestra. La expresión
por tejido no es un dato que se omitió, es un dato que este tipo de archivo no contiene por
construcción. Las 56.117 cabeceras tienen todas la misma forma —
`>GITV01NNNNNN.1 TSA: Dalbulus maidis ContigNNNNN, transcribed RNA sequence`— y **ninguna**
trae cobertura, TPM, FPKM, nombre de librería, ni mención de tejido: cero de 56.117 contra
una búsqueda de `tissue|midgut|gut|salivar|gland|ovar|head|body|egg|nymph|adult|TPM|FPKM|RPKM|cov=|expr|count|sample|SRR` `[M]`.

## Lo que sí existe, y que no es este eje

El único proyecto de lecturas de *Dalbulus maidis* que el repositorio tiene fichado es
`PRJNA631706`, en `research/ola2/W3_bases_datos/consultas/06_edirect_cli.md` §E3: **16
corridas** de RNA-Seq, 42.305 MB y 6,381 × 10¹⁰ bases. Sus nombres de muestra contrastan
*naive* contra *expuesto a MRFV*, a 4 horas y a 7 días, a 30 °C — y **ninguno nombra un
tejido** `[M]`. Es insecto entero. Sirve para un eje distinto, que no tenemos y que sería
interesante por sí mismo —**respuesta de expresión a la exposición al virus**—, pero no
contesta la pregunta del eje 5, que es si el gen se expresa en el tejido que el ARNdc
ingerido alcanza `[H]`.

Construir ese otro eje costaría bajar 42 GB de lecturas y mapearlas, y en esta máquina no hay
mapeador instalado. Queda como posibilidad declarada, no como pendiente de esta línea.

## Consecuencia para el preregistro

Ninguna. El eje 5 sigue con peso 0,00 y declarado faltante en el mismo lugar donde se publica
el orden, tal como se escribió **antes** de abrir el zip. Que la verificación posterior
confirme la declaración es el resultado que un preregistro busca: la forma honesta del
entregable no dependió de lo que viniera en el archivo.
