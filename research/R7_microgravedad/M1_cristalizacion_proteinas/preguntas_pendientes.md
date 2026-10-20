# Preguntas pendientes — R7 · M1 (cristalización de proteínas en microgravedad)

Corte: 2026-10-19. Registro de lo que no se pudo abrir, de los dominios que fallaron, de los rechazos y de las preguntas para el investigador del EPILAB. Las fuentes se citan por su id de `sources.json`.

## 1. Dominios que fallaron (no se buscaron espejos ni rutas alternativas)

`www.mdpi.com` (ProxyError, 403 del proxy de la lista de permitidos): impide abrir en texto completo *Crystals* 14(1):12 (M1-26, metaanálisis de 507 experimentos) y *Crystals* 14(7):652 (M1-27, base BμCDB). Ambas son de acceso abierto en origen; de ellas solo se obtuvieron el resumen (con `fetch_article_fulltext`) y fragmentos devueltos por un buscador. Quien tenga acceso o conceda el dominio podría extraer la tabla por métrica y, sobre todo, las reglas exactas con que cada estudio se clasificó como «mejorado». No se pidió acceso porque el encargo lo prohíbe y dejaría la tarea en espera.

`hwi.buffalo.edu` (ProxyError, 403): copia de autor de Snell y Helliwell 2021 (M1-29). Esa revisión es de pago en Taylor & Francis (`fetch_article_fulltext`: sin versión abierta, sin PMCID, `doi_resolve` 403). Solo se vio el resumen y fragmentos.

`doi.org` vía `fetch_article_fulltext` respondió 403 para los cuatro artículos de la sección 2; sin texto completo: 10.1080/0889311X.2021.1900833 (Snell y Helliwell), 10.3390/cryst14070652, 10.3390/cryst14010012 y 10.1021/acs.cgd.2c01056 (Wright 2022; ni siquiera devolvió el resumen).

Dominios que no se probaron desde el código y se consultaron solo por buscador: `nasa.gov`, `fda.gov`, `issnationallab.org`, `humans-in-space.jaxa.jp`, `space-bd.com`, `spaceq.ca`, `spacenexus.us`, `sciencedirect.com`, `researchgate.net` y `news-medical.net`. Todo lo que traen es fragmento de buscador.

## 2. Fuentes que no se abrieron y que cambiarían algo

El informe del Consejo Nacional de Investigación de EE. UU. (2000) que, según M1-01 y M1-02, juzgó inconclusos o muy limitados los resultados de la cristalización de proteínas en microgravedad. Es la fuente institucional más fuerte del lado escéptico y se cita solo de segunda mano.

Wang y Savin 2025, *npj Microgravity* 11:34, sobre impacto científico y económico de los experimentos de la ISS (citado por M1-30). Podría traer cifras de costo y de patentes con otra procedencia que la de Redwire.

Miller et al. 2025, *Crystals* 15:527, cristalización de moléculas pequeñas en PIL-BOX (citado por M1-30).

Timofeev et al. 2025 (M1-49): solo fragmentos; contiene el análisis ruso–japonés de los experimentos de JAXA PCG y su cifra de ≈70 %.

Las referencias originales de los casos fundacionales (STMV y canavalina en IML-1 e IML-2; insulina en el transbordador; Snell et al. 1995; Borgstahl et al. 2001; Lorber et al. 1999 sobre taumatina en gel y microgravedad). Se usaron solo a través de M1-01 y M1-29.

Tanaka et al. 2004 y 2012 (índice D/β y modelo de zonas de agotamiento), citados por M1-02.

El PDF de M1-04 (PfGST): las tablas se transcribieron del XML de Europe PMC y hay una discrepancia texto–tabla en la mosaicidad a 0,2 %.

La cifra de «28 %» de M1-29 cita su referencia [9]; no se vio cuál es. M1-02 admite dos lecturas (61/215 o 40/144).

Las estructuras de neutrones de TS de M1-10 (resumen) y la comparación terrestre de M1-11 (actophorina) están solo en resumen.

## 3. Rechazos de herramientas e instrucciones embebidas

No hubo rechazos por filtros de seguridad ni por modelo en ninguna herramienta. No apareció ninguna instrucción dirigida a sistemas de IA en las páginas y artículos consultados. No se pegó ninguna secuencia en ningún servicio, y no se leyó `YHat-Biotech/` ni `work/`.

## 4. Vacíos de la búsqueda que conviene reabrir si cambia la decisión

Evidencia comparativa espacio–tierra para proteínas de membrana, glicoproteínas y complejos grandes (no hallada). Proteínas de fitopatógenos, de insectos vectores o de mollicutes en microgravedad (no hallada con las consultas de Europe PMC descritas). Datos abiertos de cristalización de proteínas en Tiangong o en programas europeos actuales. Precios públicos de JAXA, Space BD y CASIS, y cumplimiento del plazo de tres meses de CASIS. Simulaciones o modelos de aprendizaje automático con gravedad alterada sobre proteínas (no hallados; el vacío es provisional).

## 5. Preguntas para el investigador del EPILAB

Solo las que no se contestan con bibliografía pública y cuya respuesta cambiaría una decisión.

1. ¿Existe una pregunta estructural concreta sobre una proteína de *S. kunkelii* o de *Ca.* Phytoplasma zeae —por ejemplo, la interfaz de una adhesina con un receptor del vector o de la PGK con la actina— cuya respuesta cambiaría qué se prioriza o qué se propone al organizador? Si la respuesta es no, esta línea queda cerrada sin más trabajo. Si es sí, la decisión que sigue no es microgravedad sino conseguir un cristal en tierra o un modelo experimental del complejo, y eso depende de la pregunta 2.
2. ¿Hay algún laboratorio de cristalografía o de producción de proteínas con el que el EPILAB colabore y que haya expresado proteínas de mollicutes? Sin ese socio, las condiciones 2, 4 y 6 de la regla de decisión no se cumplen y no tiene sentido evaluar el costo de un vuelo.
