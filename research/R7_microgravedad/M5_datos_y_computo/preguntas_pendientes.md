# preguntas_pendientes.md — M5 (datos abiertos y cómputo), R7

Corte: 2026-10-19. Tres partes: fuentes que no se pudieron abrir, dominios que fallaron o rechazos y avisos de seguridad, y preguntas que cambiarían una decisión.

## 1. Dominios que fallaron (todos por la lista permitida, no por error del servidor)

Un intento por URL; no se pidió acceso (la tarea lo prohíbe: la aprobación no llegaría) y no se buscaron espejos. Todas las URL están en `datos/COMANDOS.md`.

1. `genelab-repo-prod.s3.amazonaws.com` (almacenamiento de objetos de GeneLab al que redirige la descarga `.../geode-py/ws/studies/OSD-<n>/download?source=datamanager&file=...`): HTTP 403 del proxy. **Consecuencia: no se pudo descargar ningún archivo de datos de OSDR**; la factibilidad de las opciones 2 y 4 se midió con listados de archivos, no con contenido. Esta es la limitación que más afecta a este reporte.
2. `genelab-data.ndc.nasa.gov` (API de GeneLab): bloqueado. `visualization.osdr.nasa.gov`: bloqueado.
3. `ddbj.nig.ac.jp`: bloqueado. Por eso no se pudo localizar ni abrir el archivo de expresión del BioProject PRJDB11348 (maíz en la ISS), que es el único dato de expresión de maíz en microgravedad real que se encontró.
4. `researchsquare.com`, `academic.oup.com`, `nature.com`, `reference-global.com`, `frontiersin.org` y `link.springer.com`: solo se vieron como fragmentos del buscador; no se intentó abrirlos desde código (nature.com redirige a un login según el prompt; los demás no estaban en la lista de dominios verificados).
5. Errores transitorios (no son bloqueos): un error SSL y un 502 del proxy contra Europe PMC durante la obtención de metadatos; se reintentó y se resolvió.

## 2. Fuentes que no se abrieron o se abrieron a menor profundidad

Texto completo no disponible (solo resumen): Herranz et al. 2013 (M5-10), Nickerson et al. 2024 (M5-16) y los tres artículos del experimento «Auxin Transport» en maíz (M5-20 a M5-22). Fragmento del buscador (no sostienen cifras): M5-34 a M5-38, M5-41 a M5-44. De las 44 fuentes de `sources.json`, 3 se leyeron completas (son registros de base de datos), 19 en forma parcial, 13 solo en resumen y 9 como fragmento; ninguna bibliográfica se leyó linealmente de principio a fin.

## 3. Rechazos de herramientas y contenido sospechoso

No hubo rechazos por filtros de seguridad ni de contenido. No se encontró ninguna instrucción embebida dirigida a sistemas de IA en las páginas, resúmenes ni respuestas de API leídas.

## 4. Hallazgos de método que conviene registrar

La API de OSDR devuelve el accesión en `Accession` y no en `_id`; las rutas `/osdr/data/osd/meta/OSD-<n>` y `/osdr/data/osd/files/OSD-<n>` devuelven vacío y solo funcionan con el número. El índice de OSDR no expone taxid, así que los ceros se apoyan en el campo `organism` y en búsqueda de texto, no en una consulta por taxid (cf. D12). Los metadatos «Study Public Release Date» pueden venir en 0 (época Unix): afectó a OSD-38 y a cuatro más.

## 5. Preguntas cuya respuesta cambiaría una decisión

**Para el orquestador (decisión de acceso, no bibliográfica).** ¿Se autoriza el acceso a `genelab-repo-prod.s3.amazonaws.com` y a `ddbj.nig.ac.jp` si se decide ejecutar la opción 2 o la opción 3 de `opciones.md`? Sin ellos, ambas quedan en «medida solo por listados». Si no se piensa ejecutarlas, no hace falta pedirlos.

**Para el investigador del EPILAB (1).** ¿Les interesa saber si la maquinaria de silenciamiento de la propia planta (AGO, DCL, RDR) cambia de expresión en condiciones de estrés, o solo importa la maquinaria del insecto? Si la respuesta es «solo la del insecto», la opción 2 de `opciones.md` se descarta entera y la conclusión de este reporte es que los datos de vuelo no aportan nada al track.

**Para el investigador del EPILAB (2).** ¿Existe alguna vía (agencia, colaboración con el grupo japonés del experimento «Auxin Transport») para obtener el maíz de PRJDB11348 en forma de tabla procesada? Si no existe y DDBJ no es accesible, el maíz queda sin dato de vuelo utilizable y el único cereal reanalizable es el arroz de GSE78839.

**Para el investigador del EPILAB (3).** ¿Los parasitoides del insecto de interés tienen alguna secuencia pública que ustedes conozcan? Los dos únicos transcriptomas de parasitoides del OSDR (*Leptopilina* spp.) lo son de *Drosophila*, no de *Dalbulus*; si el EPILAB tiene otra fuente, no hace falta mirar el OSDR para L3.
