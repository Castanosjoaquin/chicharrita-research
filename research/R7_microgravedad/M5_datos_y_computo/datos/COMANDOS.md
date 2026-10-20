# COMANDOS.md — registro de consultas y descargas (M5, R7)

Fecha de corte de la pista: 2026-10-19 (todas las consultas se hicieron ese día; la hora local va en cada entrada del registro cronológico de la Parte B). Las respuestas crudas pequeñas están en `datos/`; las grandes (volcados del índice) están comprimidas en `datos/osdr_search/`.

**Presupuesto de descarga (tope de la tarea: 1 GB).** Descargado en total, estimado: ~200 MB, casi todo metadatos y listados de OSDR (74,7 MB de listados de archivos de los 642 OSD + 52,8 MB y 29,5 MB de metadatos ISA de 155 OSD + ~7 MB del volcado del índice + ~25 MB de respuestas de consultas por término + 4,3 MB de GEO). **No se descargó ningún archivo de datos de OSDR** (lecturas, conteos, microarrays): su descarga redirige a un host de almacenamiento fuera de la lista permitida (ver B-bloqueos). Las únicas descargas de datos de expresión son de GEO (GSE78839, 2,8 MB; GPL2025, 1,5 MB).

## Parte A — OSDR: lógica y consultas reproducibles

**A0. Rutas de la API de OSDR, y desvío respecto del prompt.**
La búsqueda `https://osdr.nasa.gov/osdr/data/search?term=<t>&from=<i>&size=<n>` funciona; acepta además `type=` (verificado: `cgene`, `alsda`, `nih_geo_gse`, `ebi_pride`, `mg_rast`; `esa` y `jaxa` devuelven HTTP 400). El accesión OSD está en el campo `_source.Accession`, **no** en `_id` (un primer filtro por `_id` dio cero OSD y era erróneo). Las rutas de metadatos y archivos con prefijo (`/osdr/data/osd/meta/OSD-375`, `/osdr/data/osd/files/OSD-375`) devuelven `hits: 0`; **funcionan con el número solo**: `/osdr/data/osd/meta/375` y `/osdr/data/osd/files/375?size=2000` (probado con 375, 622, 588, 751 y 118 (el aviso del prompt sobre OSD-118 coincide: con el prefijo `OSD-` la respuesta viene vacía; con el número solo, el listado de metadatos de OSD-118 se obtuvo sin error)). La ruta `/geode-py/ws/studies/OSD-375` devuelve 403.

**A1. Composición del índice (2026-10-19, `size=1`, sin término).** Sin `type`: 138.413 registros. Por `type`: cgene 572, alsda 84 (13 registros llevan ambos), nih_geo_gse 122.472, ebi_pride 12.569, mg_rast 2.729. Comprobación: 572 + 84 − 13 = 643 = 138.413 − 122.472 − 12.569 − 2.729. Los 643 registros con Accession `OSD-*` son 642 accesiones únicas (OSD-729 está duplicado en cgene); todo lo demás es registro federado de GEO, PRIDE o MG-RAST y **no cuenta**. Rango de accesiones: OSD-1 a OSD-1015.

**A2. Volcado completo del universo OSD.** `GET .../search?term=&from=0,100,200,...&size=100&type=cgene` (572 registros) y `type=alsda` (84). Guardado en `datos/osdr_search/volcado_type_cgene.json.gz` y `volcado_type_alsda.json.gz`; lista de accesiones en `accesiones_OSD_indice.json`. Sobre este volcado se aplican los filtros locales (organismo, texto) que respaldan los ceros.

**A3. Batería de consultas por término** (cada una: sin `type`, `size=1`, para el total mixto; luego con `type=cgene` y `type=alsda` paginadas; el filtro de OSD es `Accession` que empieza con `OSD-`). Resultados completos, con la lista de OSD de cada consulta, en `datos/osdr_search/consultas_osdr.json`. Los hits del buscador son difusos (coincidencias de subcadenas y de texto libre) y **no son un conteo curado**: por ejemplo «rice» devuelve 6 OSD que son estudios bacterianos, y «double-stranded RNA» devuelve 46 por menciones de ADNc de doble cadena en protocolos.

| grupo | término | hits (índice mixto) | cgene | alsda | OSD-n tras filtro | hora |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| plantas | Zea mays | 505 | 0 | 0 | 0 | 18:55:27 |
| plantas | maize | 535 | 0 | 0 | 0 | 18:55:29 |
| plantas | corn | 147 | 0 | 1 | 1 | 18:55:32 |
| plantas | Oryza sativa | 947 | 0 | 0 | 0 | 18:55:34 |
| plantas | rice | 1164 | 6 | 0 | 6 | 18:55:36 |
| plantas | Triticum aestivum | 232 | 1 | 0 | 1 | 18:55:39 |
| plantas | wheat | 355 | 1 | 0 | 1 | 18:55:42 |
| plantas | Hordeum vulgare | 141 | 0 | 0 | 0 | 18:55:45 |
| plantas | barley | 185 | 0 | 0 | 0 | 18:55:47 |
| plantas | Sorghum bicolor | 39 | 0 | 0 | 0 | 18:55:49 |
| plantas | Brachypodium distachyon | 32 | 1 | 0 | 1 | 18:55:52 |
| plantas | Poaceae | 7 | 1 | 0 | 1 | 18:55:54 |
| plantas | cereal | 84 | 1 | 0 | 1 | 18:55:57 |
| plantas | Lolium | 4 | 1 | 0 | 1 | 18:55:59 |
| plantas | plant defense | 349 | 5 | 0 | 5 | 18:56:02 |
| plantas | plant immunity | 120 | 0 | 0 | 0 | 18:56:05 |
| plantas | jasmonic acid | 99 | 0 | 0 | 0 | 18:56:07 |
| plantas | salicylic acid | 138 | 1 | 0 | 1 | 18:56:09 |
| plantas | plant pathogen | 395 | 11 | 0 | 11 | 18:56:12 |
| plantas | Arabidopsis thaliana | 4571 | 63 | 3 | 63 | 18:56:15 |
| insectos | Hemiptera | 13 | 0 | 0 | 0 | 18:56:19 |
| insectos | leafhopper | 6 | 0 | 0 | 0 | 18:56:23 |
| insectos | Dalbulus maidis | 0 | 0 | 0 | 0 | 18:56:25 |
| insectos | planthopper | 9 | 0 | 0 | 0 | 18:56:28 |
| insectos | aphid | 54 | 0 | 0 | 0 | 18:56:30 |
| insectos | Acyrthosiphon pisum | 24 | 0 | 0 | 0 | 18:56:32 |
| insectos | Bemisia tabaci | 13 | 0 | 0 | 0 | 18:56:35 |
| insectos | whitefly | 16 | 0 | 0 | 0 | 18:56:37 |
| insectos | insect | 302 | 3 | 0 | 3 | 18:56:41 |
| insectos | Drosophila melanogaster | 3837 | 16 | 3 | 19 | 18:56:43 |
| insectos | Apis mellifera | 119 | 0 | 0 | 0 | 18:56:47 |
| insectos | Tribolium castaneum | 26 | 0 | 0 | 0 | 18:56:49 |
| insectos | Aedes aegypti | 76 | 0 | 0 | 0 | 18:56:52 |
| insectos | mosquito | 150 | 2 | 0 | 2 | 18:56:54 |
| insectos | Leptopilina | 6 | 3 | 0 | 3 | 18:56:57 |
| insectos | Manduca sexta | 14 | 0 | 0 | 0 | 18:57:00 |
| insectos | cicada | 0 | 0 | 0 | 0 | 18:57:02 |
| insectos | Nilaparvata lugens | 4 | 0 | 0 | 0 | 18:57:04 |
| insectos | Homalodisca | 0 | 0 | 0 | 0 | 18:57:07 |
| insectos | bug | 13 | 0 | 0 | 0 | 18:57:09 |
| microbios | Spiroplasma | 2 | 0 | 0 | 0 | 18:57:12 |
| microbios | Mycoplasma | 60 | 3 | 0 | 3 | 18:57:16 |
| microbios | Phytoplasma | 12 | 0 | 0 | 0 | 18:57:18 |
| microbios | Mollicutes | 0 | 0 | 0 | 0 | 18:57:21 |
| microbios | Acholeplasma | 2 | 0 | 0 | 0 | 18:57:23 |
| microbios | Pseudomonas syringae | 111 | 0 | 0 | 0 | 18:57:25 |
| microbios | Xanthomonas | 75 | 0 | 0 | 0 | 18:57:28 |
| microbios | Erwinia | 19 | 0 | 0 | 0 | 18:57:31 |
| microbios | Ralstonia | 41 | 1 | 0 | 1 | 18:57:33 |
| microbios | Agrobacterium | 65 | 2 | 0 | 2 | 18:57:36 |
| microbios | Fusarium | 179 | 7 | 0 | 7 | 18:57:38 |
| microbios | phytopathogen | 22 | 1 | 0 | 1 | 18:57:41 |
| microbios | Burkholderia | 100 | 4 | 0 | 3 | 18:57:44 |
| microbios | Serratia | 30 | 2 | 0 | 2 | 18:57:47 |
| microbios | Bacillus thuringiensis | 30 | 2 | 0 | 2 | 18:57:50 |
| microbios | Beauveria | 28 | 2 | 0 | 2 | 18:57:54 |
| microbios | entomopathogenic | 24 | 0 | 0 | 0 | 18:57:56 |
| microbios | endosymbiont | 33 | 0 | 0 | 0 | 18:57:59 |
| microbios | Wolbachia | 28 | 0 | 0 | 0 | 18:58:01 |
| microbios | Buchnera | 6 | 0 | 0 | 0 | 18:58:03 |
| arn_pequeno | small RNA | 4209 | 113 | 2 | 113 | 18:58:06 |
| arn_pequeno | miRNA | 5426 | 82 | 1 | 82 | 18:58:17 |
| arn_pequeno | microRNA | 3739 | 33 | 1 | 33 | 18:58:21 |
| arn_pequeno | siRNA | 1599 | 1 | 0 | 1 | 18:58:25 |
| arn_pequeno | piRNA | 316 | 0 | 0 | 0 | 18:58:28 |
| arn_pequeno | Argonaute | 377 | 0 | 0 | 0 | 18:58:30 |
| arn_pequeno | Dicer | 386 | 1 | 0 | 1 | 18:58:33 |
| arn_pequeno | RNA interference | 651 | 1 | 0 | 1 | 18:58:35 |
| arn_pequeno | RNAi | 1413 | 3 | 0 | 3 | 18:58:38 |
| arn_pequeno | gene silencing | 2287 | 0 | 0 | 0 | 18:58:41 |
| arn_pequeno | RNA silencing | 1219 | 0 | 0 | 0 | 18:58:43 |
| arn_pequeno | non-coding RNA | 9335 | 24 | 0 | 24 | 18:58:45 |
| arn_pequeno | dsRNA | 197 | 0 | 0 | 0 | 18:58:49 |
| arn_pequeno | double-stranded RNA | 313 | 46 | 0 | 46 | 18:58:51 |
| arn_pequeno | miRNA-seq | 787 | 60 | 1 | 60 | 18:58:56 |
| arn_pequeno | small RNA sequencing | 3145 | 77 | 0 | 77 | 18:59:00 |
| arn_pequeno | lncRNA | 1093 | 3 | 0 | 3 | 18:59:04 |
| arn_pequeno | circRNA | 168 | 0 | 0 | 0 | 18:59:06 |
| arn_pequeno | RNA-dependent RNA polymerase | 376 | 2 | 0 | 2 | 18:59:09 |
| plataforma | microgravity | 383 | 270 | 35 | 299 | 18:59:11 |
| plataforma | clinostat | 23 | 20 | 1 | 21 | 18:59:22 |
| plataforma | random positioning machine | 16 | 13 | 0 | 13 | 18:59:26 |
| plataforma | rotating wall vessel | 26 | 13 | 0 | 12 | 18:59:29 |
| plataforma | simulated microgravity | 114 | 74 | 6 | 79 | 18:59:32 |
| plataforma | parabolic flight | 10 | 9 | 0 | 9 | 18:59:37 |
| plataforma | hypergravity | 30 | 20 | 0 | 20 | 18:59:40 |
| plataforma | centrifuge | 68 | 42 | 6 | 45 | 18:59:45 |
| plataforma | International Space Station | 350 | 297 | 30 | 319 | 18:59:49 |
| plataforma | Tiangong | 1 | 0 | 0 | 0 | 19:00:01 |
| plataforma | space shuttle | 51 | 39 | 6 | 44 | 19:00:04 |
| plataforma | sounding rocket | 4 | 2 | 0 | 2 | 19:00:08 |
| plataforma | spaceflight | 486 | 392 | 52 | 434 | 19:00:10 |
| plataforma | ground control | 493 | 388 | 59 | 433 | 19:00:26 |

**A4. Filtros locales sobre los 642 OSD** (sobre `Study Title`, `Study Description`, `Study Protocol Description`, `organism`, `Characteristics`, `Material Type`, `Study Factor Name`, `Study Publication Title`, etc.; expresiones regulares insensibles a mayúsculas salvo la de maíz):

| filtro | OSD que coinciden | lectura |
| --- | ---: | --- |
| `\bZea\b|\bmaize\b|\bcorn\b` | 1 (OSD-855) | falso positivo: «Iowa corn soil» como sustrato de un ensayo de regolito lunar con lechuga y rábano. **Cero estudios de maíz.** |
| Oryza, rice, Triticum, wheat, Hordeum, barley, Sorghum, Brachypodium, Lolium, Poaceae, cereal | 4 (OSD-375, 581, 622, 794) | 375 = *Brachypodium distachyon* (ISS), 622 = trigo (ISS), 581 = raigrás (ground, regolito); 794 es un falso positivo (microbiota de trajes espaciales). |
| Hemiptera, leafhopper, planthopper, aphid, Acyrthosiphon, Bemisia, whitefl, cicada, Dalbulus, Nilaparvata, Homalodisca, stink bug, Halyomorpha, Rhodnius, Cimex, bed bug, Triatom | 1 (OSD-144) | falso positivo: «aphidicolin» (inhibidor del ciclo celular en cultivo de *Arabidopsis*). **Cero hemípteros.** |
| Spiroplasm, Mycoplasm, Phytoplasm, Mollicut, Acholeplasm, Ureaplasm | 3 (OSD-344, 812, 999) | falsos positivos: prueba de contaminación por micoplasma en cultivos de células humanas. **Cero mollicutes.** |
| phytopathogen, plant pathogen, Fusarium, Pseudomonas syringae, Xanthomonas, Erwinia, Ralstonia, Agrobacterium, Pectobacterium, Magnaporthe, Botrytis, Phytophthora | 11 | ver inventario (OSD-132, 177, 264, 306, 358, 372, 400, 434, 497, 594, 658). |
| small RNA, miRNA, microRNA, siRNA, piRNA, Argonaute, Dicer, RNA interference, RNAi, RNA silencing, gene silencing, dsRNA, sRNA | 106 | texto en cualquier campo; 47 con el término en título o tipo de ensayo (revisión manual en el inventario). |

**A5. Categorías de archivo en todo el universo (listados de los 642 OSD).** Script `datos/fetch_files_summary.py` (4 hilos): `GET https://osdr.nasa.gov/osdr/data/osd/files/<n>?size=2000` para los 642 accesiones; 0 errores; 74,7 MB; resumen en `datos/osdr_search/files_summary_todos.json`. Resultado: las categorías de archivo `miRNA-Seq`/`miRNA`/`small RNA` aparecen en **21 OSD, todos *Mus musculus* (18) o *Homo sapiens* (3)**; ninguno de planta, insecto ni microbio.

**A6. Metadatos de los 155 OSD del inventario.** `datos/fetch_meta_extract.py` (`GET /osdr/data/osd/meta/<n>`, 155 estudios, 0 errores, 52,8 MB; extrae conteos de la tabla de muestras de `additionalInformation`) y `datos/fetch_meta_isa.py` (los 111 estudios cuyo registro no trae `additionalInformation`: se leyó `studies[0].materials.samples`, `factors`, `assays`; 29,5 MB). Salidas: `datos/osdr_search/meta_extract_inventario.json` y `meta_extract_isa.json`.

**A7. Listados de archivos de los candidatos de reanálisis.** `GET /osdr/data/osd/files/{375,622,427,678,120,37,346}?size=2000`; nombres y tamaños de las tablas de conteos, normalizadas y de expresión diferencial en `datos/osdr_meta/tablas_procesadas_candidatas.json` y `files_cereales_375_622.json`.

## Parte B — Registro cronológico (generado durante la corrida)

**B-bloqueos (resumen).** (1) Descarga de archivos de OSDR: HTTP 403 del proxy para `genelab-repo-prod.s3.amazonaws.com` (destino de la redirección de `/geode-py/ws/studies/OSD-<n>/download?...`). (2) `genelab-data.ndc.nasa.gov` y `visualization.osdr.nasa.gov`: bloqueados. (3) `ddbj.nig.ac.jp`: bloqueado. En los tres casos hubo un intento por URL y **no se pidió acceso**, por la regla de la tarea; no se buscaron espejos. Ver `preguntas_pendientes.md`.

### Europe PMC búsqueda — 2026-10-19 19:03:46
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=("random positioning machine" OR clinostat OR "rotating wall vessel") AND (review OR critical OR artifacts OR "fluid shear") AND (microgravity)`, pageSize=10, resultType=lite
Resultado: hitCount=948, devueltos=10.

### Europe PMC búsqueda — 2026-10-19 19:03:47
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=TITLE:"ground-based facilities" AND (microgravity OR "altered gravity") AND simulation`, pageSize=10, resultType=lite
Resultado: hitCount=1, devueltos=1.

### Europe PMC búsqueda — 2026-10-19 19:03:48
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=TITLE:("random positioning machine") AND TITLE:(critical review OR mammalian)`, pageSize=10, resultType=lite
Resultado: hitCount=0, devueltos=0.

### Europe PMC búsqueda — 2026-10-19 19:03:49
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=(clinostat OR RPM) AND "plant" AND ("spaceflight" OR "ISS") AND comparison AND analog`, pageSize=10, resultType=lite
Resultado: hitCount=140, devueltos=10.

### Europe PMC búsqueda — 2026-10-19 19:04:00
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=TITLE:"random positioning machines" AND TITLE:"mammalian cell culture"`, pageSize=12, resultType=lite
Resultado: hitCount=1, devueltos=1.

### Europe PMC búsqueda — 2026-10-19 19:04:01
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=TITLE:"simulation of microgravity" AND (ESA OR "ground-based facility")`, pageSize=12, resultType=lite
Resultado: hitCount=2, devueltos=2.

### Europe PMC búsqueda — 2026-10-19 19:04:03
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=(TITLE:"random positioning machine" OR TITLE:clinostat) AND (TITLE:"fluid" OR TITLE:"dynamics" OR TITLE:"shear" OR TITLE:"acceleration")`, pageSize=12, resultType=lite
Resultado: hitCount=2, devueltos=2.

### Europe PMC búsqueda — 2026-10-19 19:04:04
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=TITLE:"random positioning machine" AND TITLE:(technology OR developments OR "simulated microgravity" )`, pageSize=12, resultType=lite
Resultado: hitCount=8, devueltos=8.

### Europe PMC búsqueda — 2026-10-19 19:04:05
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=("magnetic levitation" OR "diamagnetic levitation") AND (microgravity) AND (biological OR cells OR plants OR Drosophila) AND (artifact OR limitation OR review OR "magnetic field")`, pageSize=12, resultType=lite
Resultado: hitCount=193, devueltos=12.

### Europe PMC búsqueda — 2026-10-19 19:04:06
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=("large diameter centrifuge" OR "hypergravity" ) AND (plants OR Arabidopsis OR transcriptome) AND (ESA OR "ground-based")`, pageSize=12, resultType=lite
Resultado: hitCount=182, devueltos=12.

### Europe PMC búsqueda — 2026-10-19 19:04:07
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=("rotating wall vessel" OR "low shear modeled microgravity" OR "RCCS") AND (bacteria OR microbial) AND (shear OR "fluid dynamics" OR "limitations" OR "not equivalent")`, pageSize=12, resultType=lite
Resultado: hitCount=714, devueltos=12.

### Europe PMC búsqueda — 2026-10-19 19:04:09
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=(clinostat OR "random positioning machine") AND (Arabidopsis OR plant) AND (transcriptome OR "gene expression") AND (spaceflight) AND (differ OR discrepan OR "not mimic" OR similar)`, pageSize=12, resultType=lite
Resultado: hitCount=102, devueltos=12.

### Europe PMC texto completo — 2026-10-19 19:04:27
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3549630/fullTextXML` → HTTP 500, 150 bytes (no disponible).

### Europe PMC texto completo — 2026-10-19 19:04:28
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4310317/fullTextXML` → HTTP 200, 77351 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:04:30
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5460110/fullTextXML` → HTTP 200, 68928 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:04:32
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6908503/fullTextXML` → HTTP 200, 119732 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:04:34
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12216757/fullTextXML` → HTTP 200, 93975 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:04:36
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13271463/fullTextXML` → HTTP 200, 135646 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:04:39
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13287604/fullTextXML` → HTTP 200, 182877 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:04:41
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12177493/fullTextXML` → HTTP 200, 329746 bytes (OK).

### Europe PMC resumen — 2026-10-19 19:05:17
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:23252378 AND SRC:MED&resultType=core` → abstract de Herranz 2013 (solo resumen; texto completo no OA).

### Europe PMC búsqueda — 2026-10-19 19:05:18
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=TITLE:"random positioning machines" AND TITLE:"mammalian cell culture"`, pageSize=12, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=1, devueltos=1.

### Europe PMC búsqueda — 2026-10-19 19:05:19
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=TITLE:"simulation of microgravity" AND (ESA OR "ground-based facility")`, pageSize=12, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=2, devueltos=2.

### Europe PMC búsqueda — 2026-10-19 19:05:20
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=(TITLE:"random positioning machine" OR TITLE:clinostat) AND (TITLE:"fluid" OR TITLE:"dynamics" OR TITLE:"shear" OR TITLE:"acceleration")`, pageSize=12, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=2, devueltos=2.

### Europe PMC búsqueda — 2026-10-19 19:05:21
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=TITLE:"random positioning machine" AND TITLE:(technology OR developments OR "simulated microgravity" )`, pageSize=12, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=8, devueltos=8.

### Europe PMC búsqueda — 2026-10-19 19:05:22
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=("magnetic levitation" OR "diamagnetic levitation") AND (microgravity) AND (biological OR cells OR plants OR Drosophila) AND (artifact OR limitation OR review OR "magnetic field")`, pageSize=12, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=193, devueltos=12.

### Europe PMC búsqueda — 2026-10-19 19:05:23
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=("large diameter centrifuge" OR "hypergravity" ) AND (plants OR Arabidopsis OR transcriptome) AND (ESA OR "ground-based")`, pageSize=12, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=182, devueltos=12.

### Europe PMC búsqueda — 2026-10-19 19:05:24
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=("rotating wall vessel" OR "low shear modeled microgravity" OR "RCCS") AND (bacteria OR microbial) AND (shear OR "fluid dynamics" OR "limitations" OR "not equivalent")`, pageSize=12, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=714, devueltos=12.

### Europe PMC búsqueda — 2026-10-19 19:05:26
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=(clinostat OR "random positioning machine") AND (Arabidopsis OR plant) AND (transcriptome OR "gene expression") AND (spaceflight) AND (differ OR discrepan OR "not mimic" OR similar)`, pageSize=12, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=102, devueltos=12.

### Europe PMC búsqueda — 2026-10-19 19:05:34
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=("molecular dynamics") AND (microgravity OR "altered gravity" OR "hypergravity" OR "weightlessness") AND (protein OR RNA OR "nucleic acid") AND (simulation)`, pageSize=12, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=112, devueltos=12.

### Europe PMC búsqueda — 2026-10-19 19:05:35
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query="protein crystal growth" AND microgravity AND ("molecular dynamics" OR "computational model" OR "numerical simulation" OR "convection" OR "depletion zone")`, pageSize=12, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=54, devueltos=12.

### Europe PMC búsqueda — 2026-10-19 19:05:36
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=("machine learning" OR "deep learning") AND ("protein crystallization" OR "crystallizability" OR "crystallization propensity")`, pageSize=12, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=410, devueltos=12.

### Europe PMC búsqueda — 2026-10-19 19:05:37
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=("machine learning" OR "deep learning" OR "artificial intelligence") AND microgravity AND ("protein crystal" OR "crystallization")`, pageSize=12, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=50, devueltos=12.

### Europe PMC texto completo — 2026-10-19 19:06:18
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5515504/fullTextXML` → HTTP 200, 172113 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:06:20
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3795566/fullTextXML` → HTTP 200, 53821 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:06:22
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11743144/fullTextXML` → HTTP 200, 335253 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:06:24
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8854672/fullTextXML` → HTTP 200, 125648 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:06:26
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12167385/fullTextXML` → HTTP 200, 120755 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:06:28
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10027818/fullTextXML` → HTTP 200, 166645 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:06:30
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6158273/fullTextXML` → HTTP 200, 125066 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:06:32
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6151610/fullTextXML` → HTTP 200, 92217 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:06:34
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10485020/fullTextXML` → HTTP 200, 179698 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:06:36
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13141840/fullTextXML` → HTTP 200, 263738 bytes (OK).

### arXiv PDF — 2026-10-19 19:07:18
`GET https://arxiv.org/pdf/2606.28856` → HTTP 200, 2348476 bytes.

### api.biorxiv.org — 2026-10-19 19:07:43
`GET https://api.biorxiv.org/details/biorxiv/10.1101/2024.06.04.597470` → HTTP 200, 4475 bytes.

### api.biorxiv.org — 2026-10-19 19:07:44
`GET https://api.biorxiv.org/details/biorxiv/10.1101/2024.01.24.577100` → HTTP 200, 4450 bytes.

### Europe PMC búsqueda — 2026-10-19 19:08:04
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=("Zea mays" OR maize) AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR hypergravity OR "simulated gravity")`, pageSize=15, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=367, devueltos=15.

### Europe PMC búsqueda — 2026-10-19 19:08:05
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=(aphid OR planthopper OR leafhopper OR Hemiptera OR whitefly OR "stink bug") AND (microgravity OR spaceflight OR clinostat OR hypergravity OR "random positioning")`, pageSize=15, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=31, devueltos=15.

### Europe PMC búsqueda — 2026-10-19 19:08:06
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=(Spiroplasma OR Mycoplasma OR Phytoplasma OR Mollicutes OR Acholeplasma) AND (microgravity OR spaceflight OR "simulated microgravity") AND NOT (contamination)`, pageSize=15, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=75, devueltos=15.

### Europe PMC búsqueda — 2026-10-19 19:08:08
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=("RNA interference" OR RNAi OR dsRNA OR siRNA) AND (microgravity OR spaceflight) AND (plant OR insect OR Arabidopsis OR Drosophila)`, pageSize=15, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=243, devueltos=15.

### Europe PMC búsqueda — 2026-10-19 19:08:09
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=("small RNA" OR miRNA OR microRNA OR Argonaute OR "RNA silencing" OR "RNA-directed DNA methylation") AND (Arabidopsis OR plant OR rice OR wheat OR maize) AND (microgravity OR spaceflight)`, pageSize=15, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=202, devueltos=15.

### OSDR listados de archivos — 2026-10-19 19:08:32
Script `datos/fetch_files_summary.py` (4 hilos): `GET https://osdr.nasa.gov/osdr/data/osd/files/<n>?size=2000` para los 642 accesiones OSD-<n> del índice (n numérico, sin prefijo OSD-). Resultado: 642 respuestas, 0 con error o sin estudio; 74.7 MB descargados en total (cuentan para el tope de 1 GB). Resumen en `datos/osdr_search/files_summary_todos.json`.

### OSDR files — 2026-10-19 19:09:32
`GET https://osdr.nasa.gov/osdr/data/osd/files/375?size=2000` → HTTP 200, 39140 bytes.

### OSDR files — 2026-10-19 19:09:33
`GET https://osdr.nasa.gov/osdr/data/osd/files/622?size=2000` → HTTP 200, 4015 bytes.

### Descarga de archivo de datos — 2026-10-19 19:10:06 — BLOQUEADA
`GET https://osdr.nasa.gov/geode-py/ws/studies/OSD-622/download?source=datamanager&file=GLDS-594_microarray_Summary+PESTO+wheat+array+anno.xls` redirige a un host de almacenamiento de objetos de AWS (`genelab-repo-prod.s3.amazonaws.com`, ruta `/genelab-data/GLDS-594/microarray/...`, con URL prefirmada que no se registra aquí). El proxy responde 403: host fuera de la lista permitida. Conforme a la regla de la tarea (no pedir dominios nuevos) no se solicitó acceso; no se buscaron espejos. Consecuencia: ningún archivo de datos de OSDR se pudo descargar; la factibilidad de las opciones se mide solo con listados de archivos (nombres, categorías, tamaños) y metadatos.

### Intento de ruta alternativa — 2026-10-19 19:10:06
`GET https://genelab-data.ndc.nasa.gov/genelab/data/glds/files/375` → error de conexión/proxy: HTTPSConnectionPool(host='genelab-data.ndc.nasa.gov', port=443): Max retries exceeded with url: /genelab/data/glds/files/375 (Caused by ProxyError('Unable to co. Un solo intento; no se pidió acceso (regla de la tarea).

### Intento de ruta alternativa — 2026-10-19 19:10:06
`GET https://visualization.osdr.nasa.gov/radlab/` → error de conexión/proxy: HTTPSConnectionPool(host='visualization.osdr.nasa.gov', port=443): Max retries exceeded with url: /radlab/ (Caused by ProxyError('Unable to connect to proxy', O. Un solo intento; no se pidió acceso (regla de la tarea).

### OSDR meta (inspección) — 2026-10-19 19:13:05
`GET https://osdr.nasa.gov/osdr/data/osd/meta/588` → HTTP 200, 734211 bytes (inspección de estructura cuando falta la tabla de muestras).

### Cálculo propio (Python, sin red) — 2026-10-19 19:13:39
Escala de la gravedad frente a la agitación térmica para macromoléculas y para un cristal. Salida completa en `datos/calculo_gravedad_escala_molecular.txt`. Es una estimación de orden de magnitud con parámetros supuestos y declarados [H]; no es una fuente.

### OSDR files — 2026-10-19 19:15:03
`GET https://osdr.nasa.gov/osdr/data/osd/files/427?size=2000` → HTTP 200, 280613 bytes.

### OSDR files — 2026-10-19 19:15:05
`GET https://osdr.nasa.gov/osdr/data/osd/files/678?size=2000` → HTTP 200, 334667 bytes.

### OSDR files — 2026-10-19 19:15:10
`GET https://osdr.nasa.gov/osdr/data/osd/files/120?size=2000` → HTTP 200, 440037 bytes.

### OSDR files — 2026-10-19 19:15:13
`GET https://osdr.nasa.gov/osdr/data/osd/files/37?size=2000` → HTTP 200, 492672 bytes.

### OSDR files — 2026-10-19 19:15:16
`GET https://osdr.nasa.gov/osdr/data/osd/files/346?size=2000` → HTTP 200, 336475 bytes.

### NCBI E-utilities esearch — 2026-10-19 19:16:15
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` db=gds, term=`"Zea mays"[Organism] AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station")` → HTTP 200; count=0; ids=[].

### NCBI E-utilities esearch — 2026-10-19 19:16:16
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` db=bioproject, term=`"Zea mays"[Organism] AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station")` → HTTP 200; count=1; ids=['730129'].

### NCBI E-utilities esearch — 2026-10-19 19:16:17
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` db=gds, term=`"Hemiptera"[Organism] AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station")` → HTTP 200; count=0; ids=[].

### NCBI E-utilities esearch — 2026-10-19 19:16:18
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` db=bioproject, term=`"Hemiptera"[Organism] AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station")` → HTTP 200; count=0; ids=[].

### NCBI E-utilities esearch — 2026-10-19 19:16:19
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` db=gds, term=`Dalbulus[Organism] AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station")` → HTTP 200; count=0; ids=[].

### NCBI E-utilities esearch — 2026-10-19 19:16:19
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` db=bioproject, term=`Dalbulus[Organism] AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station")` → HTTP 200; count=0; ids=[].

### NCBI E-utilities esearch — 2026-10-19 19:16:20
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` db=gds, term=`Spiroplasma[Organism] AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station")` → HTTP 200; count=0; ids=[].

### NCBI E-utilities esearch — 2026-10-19 19:16:21
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` db=bioproject, term=`Spiroplasma[Organism] AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station")` → HTTP 200; count=0; ids=[].

### NCBI E-utilities esearch — 2026-10-19 19:16:21
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` db=gds, term=`"Candidatus Phytoplasma"[Organism] AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station")` → HTTP 200; count=0; ids=[].

### NCBI E-utilities esearch — 2026-10-19 19:16:22
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` db=bioproject, term=`"Candidatus Phytoplasma"[Organism] AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station")` → HTTP 200; count=0; ids=[].

### NCBI E-utilities esearch — 2026-10-19 19:16:23
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` db=gds, term=`Mollicutes[Organism] AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station")` → HTTP 200; count=0; ids=[].

### NCBI E-utilities esearch — 2026-10-19 19:16:23
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` db=bioproject, term=`Mollicutes[Organism] AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station")` → HTTP 200; count=0; ids=[].

### NCBI E-utilities esearch — 2026-10-19 19:16:24
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` db=gds, term=`Poaceae[Organism] AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station")` → HTTP 200; count=17; ids=['200183508', '200149182', '200078839', '305558501', '305558500', '305558499', '305558498', '302078449', '302078448', '302078447', '302078446', '302078445', '302078444', '302078443', '302078442', '302078441', '302078440'].

### NCBI E-utilities esearch — 2026-10-19 19:16:25
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` db=bioproject, term=`Poaceae[Organism] AND (microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station")` → HTTP 200; count=7; ids=['1162653', '977874', '761100', '730129', '386075', '374931', '314119'].

### NCBI E-utilities esummary — 2026-10-19 19:16:33
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi` db=bioproject, id=1162653,977874,761100,730129,386075,374931,314119 → HTTP 200, 11866 bytes.

### NCBI E-utilities esummary — 2026-10-19 19:16:34
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi` db=gds, id=200183508,200149182,200078839,305558501,305558500,305558499,305558498,302078449,302078448,302078447,302078446,302078445,302078444,302078443,302078442,302078441,302078440 → HTTP 200, 16142 bytes.

### OSDR search (verificación de registros federados) — 2026-10-19 19:16:59
`GET https://osdr.nasa.gov/osdr/data/search?term=Zea+mays&from=0&size=100` (paginado) → total 505; todos federados (GEO/PRIDE), ninguno con Accession OSD-*. Se buscaron términos de gravedad en título/descripción de los 505 registros.

### NCBI E-utilities elink — 2026-10-19 19:17:17
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi` dbfrom=bioproject, db=gds, id=730129 → HTTP 200.

### NCBI E-utilities elink — 2026-10-19 19:17:18
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi` dbfrom=bioproject, db=sra, id=730129 → HTTP 200.

### NCBI E-utilities elink — 2026-10-19 19:17:19
`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi` dbfrom=bioproject, db=biosample, id=730129 → HTTP 200.

### Europe PMC búsqueda — 2026-10-19 19:17:28
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=(maize OR "Zea mays") AND (etiolated OR seedlings) AND (microgravity OR "International Space Station") AND (microarray OR transcript*)`, pageSize=10, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=84, devueltos=10.

### Europe PMC búsqueda — 2026-10-19 19:17:30
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=TITLE:(maize) AND (TITLE:microgravity OR TITLE:space OR TITLE:"International Space Station")`, pageSize=10, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=34, devueltos=10.

### Europe PMC búsqueda — 2026-10-19 19:17:31
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search` params: `query=(rice AND calli AND spaceflight AND microarray) OR (rice AND "root tip" AND "simulated microgravity" AND transcriptome)`, pageSize=10, resultType=lite, sort=P_PDATE_D desc
Resultado: hitCount=13, devueltos=10.

### Europe PMC resumen — 2026-10-19 19:17:42
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:36682823 AND SRC:MED&resultType=core` → resumen de PMID 36682823 (solo resumen).

### Europe PMC resumen — 2026-10-19 19:17:43
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:32635987 AND SRC:MED&resultType=core` → resumen de PMID 32635987 (solo resumen).

### Europe PMC resumen — 2026-10-19 19:17:44
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:30797426 AND SRC:MED&resultType=core` → resumen de PMID 30797426 (solo resumen).

### Europe PMC texto completo — 2026-10-19 19:17:46
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10288856/fullTextXML` → HTTP 200, 108025 bytes (OK).

### Europe PMC texto completo — 2026-10-19 19:17:48
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9287483/fullTextXML` → HTTP 200, 179963 bytes (OK).

### Intento DDBJ — 2026-10-19 19:18:00
`GET https://ddbj.nig.ac.jp/search/entry/bioproject/PRJDB11348.json` → error de proxy/conexión (HTTPSConnectionPool(host='ddbj.nig.ac.jp', port=443): Max retries exceeded with url: /search/entry/bioproject/). Un solo intento por URL; no se pidió acceso (regla de la tarea).

### Intento DDBJ — 2026-10-19 19:18:00
`GET https://ddbj.nig.ac.jp/public/ddbj_database/gea/experiment/` → error de proxy/conexión (HTTPSConnectionPool(host='ddbj.nig.ac.jp', port=443): Max retries exceeded with url: /public/ddbj_database/gea). Un solo intento por URL; no se pidió acceso (regla de la tarea).

### GEO ficha — 2026-10-19 19:18:12
`GET https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE78839&targ=self&form=text&view=brief` → HTTP 200, 1969 bytes.

### GEO ficha — 2026-10-19 19:18:12
`GET https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE183508&targ=self&form=text&view=brief` → HTTP 200, 2348 bytes.

### Descarga — 2026-10-19 19:18:24
`GET https://ftp.ncbi.nlm.nih.gov/geo/series/GSE78nnn/GSE78839/matrix/GSE78839_series_matrix.txt.gz` → HTTP 200, 2779934 bytes, guardado en `datos/descargas/GSE78839_series_matrix.txt.gz`. Acumulado de descargas de datos (no listados): 2.78 MB.

### HEAD — 2026-10-19 19:18:37
`HEAD https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL2nnn/GPL2025/annot/GPL2025.annot.gz` → HTTP 200, content-length=1512117.

### HEAD — 2026-10-19 19:18:37
`HEAD https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL2nnn/GPL2025/soft/GPL2025_family.soft.gz` → HTTP 200, content-length=1600069931.

### Descarga — 2026-10-19 19:18:45
`GET https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL2nnn/GPL2025/annot/GPL2025.annot.gz` → HTTP 200, 1512117 bytes, guardado en `datos/descargas/GPL2025.annot.gz`. Acumulado de descargas de datos (no listados): 4.30 MB.

### Cálculo propio sobre descargas de GEO — 2026-10-19 19:19:03
Sobre `GSE78839_series_matrix.txt.gz` (10 arrays, 57.381 sondas) y `GPL2025.annot.gz` (57.381 sondas, 23.850 con anotación): búsqueda por expresión regular de Argonaute/PIWI/PAZ, Dicer, RDR y otros en 'Gene title', 'Nucleotide Title', 'UniGene title' y GO. Resultado: 46 sondas candidatas únicas ({'Argonaute/PIWI/PAZ': 17, 'Dicer/DCL': 5, 'HEN1/SGS3/DRB/otros': 19, 'RDR (RNA-dep. RNA pol.)': 5}), 46 presentes en la matriz. Lista en `datos/gse78839_sondas_silenciamiento.tsv`. Solo se midió cobertura de sondas; no se calculó expresión diferencial. Falsos positivos posibles (por ejemplo 'phytolongin' en la categoría 'otros'): la lista no está curada.

### Europe PMC resumen — 2026-10-19 19:19:23
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:39158275 AND SRC:MED&resultType=core` → resumen de PMID 39158275 (solo resumen).

### Europe PMC metadatos — 2026-10-20 00:03:43
`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=PMCID:<id>` (20 PMCID) y `query=EXT_ID:<pmid> AND SRC:MED` (3 PMID), resultType=lite; se usó solo para título, autores, año, revista y DOI de registros ya abiertos. Hubo un error SSL transitorio y un 502 del proxy (no es bloqueo de lista permitida); se reintentó.


## Parte C — Búsquedas web (herramienta web_search; devuelven fragmentos, no documentos abiertos)

Todas el 2026-10-19. Lo que solo se vio como fragmento figura en `sources.json` con `nivel_lectura: fragmento_buscador`.

1. `machine learning meta-analysis NASA GeneLab spaceflight transcriptomes conserved response across experiments`
2. `foundation model spaceflight transcriptomics GeneLab OSDR pretrained model Geneformer scGPT space biology`
3. `molecular dynamics simulation effect of gravity on protein or RNA conformation microgravity hypergravity simulation study`
4. `deep learning protein crystallization propensity prediction benchmark 2025 sequence-based crystallizability`
5. `machine learning predict protein crystal quality microgravity International Space Station crystallization experiments data-driven` (la primera emisión se descartó por ir en paralelo con otras llamadas; se repitió sola)
6. `RNA foundation model OR protein language model applied to spaceflight microgravity data GeneLab OSDR 2025 2026`

## Parte D — Verificación cruzada de ceros de OSDR contra NCBI (GEO y BioProject)

Consultas `esearch` con nombre científico en `[Organism]` (no por nombre común, según la advertencia de D12) más términos de gravedad; fecha 2026-10-19; detalle por consulta en la Parte B. Resumen: *Zea mays*: gds 0, bioproject 1 (PRJDB11348); Hemiptera: 0 y 0; *Dalbulus*: 0 y 0; *Spiroplasma*: 0 y 0; *Candidatus* Phytoplasma: 0 y 0; Mollicutes: 0 y 0; Poaceae: gds 17 (3 series y sus muestras), bioproject 7. Términos de gravedad usados: `microgravity OR spaceflight OR "space flight" OR clinostat OR "random positioning" OR "simulated microgravity" OR hypergravity OR "International Space Station"`. Un cero de esta consulta significa «ningún registro de GEO/BioProject cuyo texto combine ese organismo con esos términos», no «ningún dato existe».

## Parte E — Notas sobre los archivos de `datos/`

`datos/textos/` guarda extractos de texto de artículos de acceso abierto (descargados con `GET .../europepmc/webservices/rest/<PMCID>/fullTextXML`, y el PDF de arXiv 2606.28856) que se usaron para leer y comprobar las afirmaciones del reporte; son material de lectura para auditoría, no para republicar. Un archivo, `PMC12177493.txt` (una revisión de 2025 sobre respuestas de plantas a gravedad alterada), se descargó pero **no se leyó ni se cita** en ningún reporte. `datos/descargas/` guarda las únicas descargas de datos de expresión: GSE78839 (matriz de serie, 2,78 MB), GPL2025 (anotación, 1,51 MB) y las fichas breves de GSE78839 y GSE183508. `datos/osdr_search/` guarda el volcado del índice, la batería de consultas y los resúmenes de listados y metadatos. Los guiones `fetch_files_summary.py`, `fetch_meta_extract.py` y `fetch_meta_isa.py` reproducen las tres extracciones de OSDR (se ejecutan con la ruta de esta carpeta como argumento).
