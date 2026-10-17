# Plan de ingesta

Qué bajar, en qué orden, cuánto pesa de verdad y cómo versionarlo. Los tamaños
de esta página no son estimaciones: salen del campo `available_files` de la API
de Datasets, de la cabecera `Content-Length` del FTP del NCBI y de la columna
`size_MB` del `runinfo` de SRA, todos medidos el 17 de octubre de 2026
(`consultas/03_datasets_api_genomas.md`, `consultas/05_tsa_y_ftp.md`,
`consultas/06_edirect_cli.md`). Nada de esto se descargó todavía, salvo los
10.394 bytes del ejemplo de MRFV: el encargo era el plan, no la ingesta.

## Nivel 1 — El núcleo de diseño y tamizaje

Con esto se puede diseñar y tamizar sin tocar un solo genoma grande. Total:
**117,8 MB**.

| qué | accesión | tamaño | para qué |
| --- | --- | ---: | --- |
| Transcriptoma del vector, el más grande | `GITV00000000` | 31,44 MB | blanco y tamizaje dentro del vector |
| Transcriptoma del vector, segundo | `GHCC00000000` | 10,74 MB | control de cobertura |
| Transcriptoma del vector, tercero | `GCWP00000000` | 7,20 MB | control de cobertura |
| Transcriptoma de maíz | `GCF_902167145.1` rna | 37,78 MB | off-target en el cultivo |
| Transcriptoma de *Macrosteles* | `GCF_028750875.1` rna | 21,38 MB | ortología y control de especificidad |
| Proteoma de *Macrosteles* | `GCF_028750875.1` prot | 7,70 MB | transferencia de blancos por ortología |
| Genoma, GFF3, proteínas y CDS del espiroplasma | `GCF_001274875.1` | 1,12 MB | contexto del patógeno |
| Genoma, GFF3, proteínas y CDS del fitoplasma | `GCF_001712875.1` | 0,44 MB | contexto del patógeno |
| Genoma y anotación de MRFV | `GCF_000862485.2` | 0,01 MB | blanco viral |
| Los dos candidatos a MSMV | `GCF_004788335.1`, `GCF_002867025.1` | 0,03 MB | hasta que se resuelva cuál es |

Orden de descarga: primero los patógenos y los virus, que pesan menos de 2 MB y
permiten probar la cadena entera; después los tres transcriptomas del vector;
después maíz y *Macrosteles*. El criterio es que cada paso deje algo usable
aunque el siguiente falle.

## Nivel 2 — Los genomas, sólo si hacen falta

Total: **1,06 GB**. No entran en el camino crítico. El genoma del
vector sirve para dos cosas que hoy no estamos haciendo: anotar de novo y mirar
variabilidad del sitio blanco.

| qué | accesión | tamaño |
| --- | --- | ---: |
| Genoma cromosómico del vector (Sanger) | `GCA_975739785.1` | 268,63 MB |
| Genoma CIAP-INTA del vector | `GCA_054756405.1` | 171,58 MB |
| Genoma de maíz B73 | `GCF_902167145.1` | 619,98 MB |
| GFF3 de maíz | `GCF_902167145.1` | 15,40 MB |
| Proteoma de maíz | `GCF_902167145.1` | 12,19 MB |

## Nivel 3 — Las lecturas crudas, con los ojos abiertos

`PRJNA631706`, los 16 RNA-Seq del vector expuesto a MRFV: **42.305 MB**, es
decir unos 41,3 GB, y 6,381 × 10¹⁰ bases. La cifra sale de sumar la columna
`size_MB` del `runinfo`, no de una regla general. Bajarlo entero y cuantificarlo
contra el TSA con Salmon es una tarde de cómputo en una notebook; mapearlo contra
el genoma de 972 Mb, no. Decidir esto es una decisión de proyecto, no de ingesta,
y conviene tomarla después de saber si EPILAB ya tiene datos de expresión propios.

## Versionado

El principio: los datos no entran al repositorio, el manifiesto sí.

1. Estructura fija, una carpeta por fuente y accesión, con la fecha de descarga
   en el nombre: `data/raw/ncbi/<accesion>/<AAAA-MM-DD>/`. La fecha no es
   decorativa: RefSeq reanota, y el genoma del espiroplasma cambió de anotación
   el 2025-12-13 y el del fitoplasma el 2026-06-07.
2. Checksums del propio NCBI, no nuestros: el ZIP de Datasets trae `md5sum.txt`
   adentro y cada directorio del FTP trae `md5checksums.txt`. Se verifican al
   bajar y se vuelven a verificar antes de cualquier corrida que se vaya a
   reportar.
3. Un `manifiesto.csv` versionado en git con una fila por archivo: accesión,
   ruta, bytes, md5, URL exacta, fecha y hora UTC de descarga, versión de la
   anotación cuando aplique y versión de la API que respondió (hoy, 18.39.0).
4. `data/` entero en `.gitignore`, como ya están `YHat-Biotech/` y `work/`.
5. Para rehacer una corrida vieja: el manifiesto tiene la URL y el md5; si el
   NCBI ya cambió el archivo, el md5 no coincide y eso es justamente lo que uno
   quiere enterarse.

## Scripts que hacen falta

Cinco, chicos, en este orden:

1. `01_inventario.py` — consulta la API de Datasets y las E-utilities y escribe
   un JSON con lo que existe hoy para la lista de taxones del proyecto. Es el
   que ya corrimos en esta investigación; queda por empaquetarlo.
2. `02_descarga.sh` — baja lo del nivel 1 con `datasets download genome
   accession ...` para los ensamblados y `curl` contra el FTP para los TSA.
   Idempotente: si el md5 coincide, no vuelve a bajar.
3. `03_verificar.py` — compara contra `md5sum.txt` y `md5checksums.txt` y
   escribe el `manifiesto.csv`.
4. `04_indices.sh` — construye los índices que consume el tamizaje:
   `bowtie-build` sobre cada transcriptoma y `makeblastdb` sobre los proteomas.
   Es lo que convierte los 117,8 MB de FASTA en una base de off-target usable.
5. `05_actualizar.py` — vuelve a correr el inventario y reporta las diferencias
   contra el manifiesto: ensamblados nuevos, anotaciones nuevas, accesiones
   retiradas. Una corrida por semana durante el evento alcanza.

Una nota sobre la clave de API: la guía de E-utilities permite diez peticiones
por segundo con clave y tres sin ella, y nuestras 409 peticiones sin clave
recibieron dos respuestas 429. Para `01_inventario.py` y `05_actualizar.py`,
que hacen cientos de consultas, conviene pedirla.
