# R3 — Rastro de fuentes y notas de trabajo

Registro de qué se abrió, qué devolvió y qué quedó sin abrir. Sirve para que
cualquiera del equipo pueda rehacer el camino sin repetir búsquedas fallidas.

## Fuentes abiertas con WebFetch (texto leído)

| Fuente | URL | Qué aportó |
| --- | --- | --- |
| Sitio de la empresa | apolobiotech.com.ar | Tecnología declarada, equipo completo, "hasta 65% de reducción de severidad", 9 ensayos 2023/24 en *Botrytis*, oficinas (incluye Pabellón IFIBYNE) |
| Cancillería argentina, ficha Next from Argentina | cancilleria.gob.ar/en/new-technologies/next-from-argentina-en/apolo-biotech | 28 personas, ronda seed, mercados de interés, sello de bioproducto, reconocimiento EBT del CONICET |
| Fertilizer Daily (23/06/2025) | fertilizerdaily.com/20250623-...md/ | 30 empleados, planta piloto 2024, plataforma bioinformática con Sadosky e INTA, ensayos en banano y maní por país, cuello de botella regulatorio |
| Agrofy News (15/04/2024) | news.agrofy.com.ar/noticia/209164/... | Planta piloto 120 m², capacidad "hasta 200 mil hectáreas", costo de producción "bajó hasta 80 veces en el último año", aplicación foliar, efecto sistémico, 24 patógenos en pipeline, trámite SENASA |
| La Nación (06/09/2023) | lanacion.com.ar/.../nid06092023 | Fundación 28/03/2022, 21 personas entonces, 23 proyectos, cultivos intensivos, extensivos recién en 2027, Brometan y SpeedAgro como *technology facilitators* |
| La Nación (10/04/2025) | lanacion.com.ar/.../nid10042025 | Apolo Rocket: nube, >140 organismos evaluados a la vez, reportes automáticos, IABIMO (INTA-CONICET), Fundación Sadosky |
| Fundación Sadosky, proyectos 2023 | solucionesinnovadoras.fundacionsadosky.org.ar/proyectos-seleccionados-en-2023/ | Título exacto del proyecto y las dos instituciones participantes |
| El Español (11/01/2025) | elespanol.com/invertia/.../915158847_0.html | "Es un líquido. Se aplica con un pulverizador sobre las hojas", estabilización a temperatura ambiente, sin producto comercial, planes Francia/España |
| UNL Noticias (24/05/2023) | unl.edu.ar/noticias/news/view/empresa_santafesina... | Vínculo con B Lab / PTLC / UNL Bio, laboratorio de Ariel desde 2016 en el IAL, 8 personas y +70 publicaciones |
| Bichos de Campo (18/09/2023) | bichosdecampo.com/?p=150088 | BID Lab: USD 130.000 no reembolsables + USD 450.000 de recuperación contingente; frutilla/*Botrytis* |
| Agrofy News (23/10/2025) | news.agrofy.com.ar/noticia/214536/... | Innovate for Impact Challenge, USD 50.000, ~400 propuestas de 65 países |
| PTLC, ficha de empresa | ptlc.org.ar/en/empresa/apolo-biotech-s-a-s-2/ | "we modulate genes in plants and pathogens using exogenous RNAs" |
| CONICET, nota chicharrita (24/09/2024) | conicet.gov.ar/especialistas-del-conicet-desarrollan-estrategias... | Grupo de Catalano (CIT NOBA / CEBIO-UNNOBA), las cuatro referencias con DOI, estrategia dsRNasa |
| IFIBYNE, Grupo Ariel | ifibyne.exactas.uba.ar/site/grupo-ariel | **Clave**: composición del laboratorio con dobles filiaciones UBA/APOLO, cátedra AXA, handle @arg_epilab |
| IFIBYNE, listado de grupos | ifibyne.exactas.uba.ar/grupos-investigacion/ | Confirma "Grupo Ariel — Laboratorio de Epigenética y ARNs no codificantes" como grupo del instituto |
| AXA Foundation, proyecto Ariel | axafoundation.org/en/science/funded-projects/... | Objetivos, tomate y trigo, "controlled delivery of RNAs using nanotechnology" |
| Vatanparast, Merkel & Amari 2024, *IJMS* 25(12):6530 | pmc.ncbi.nlm.nih.gov/articles/PMC11204322/ | Revisión revisada por pares: modos de aplicación, portadores, persistencias con número, marco regulatorio EPA/EFSA/APVMA, costos de registro |
| Attallah, Conti, Zuljan, Zavallo & Ariel 2025, *The Plant Cell* 37(5):koaf054 | academic.oup.com/plcell/article/37/5/koaf054/8079131 | **Clave**: revisión del propio equipo. SIGS vs HIGS, APOLO transcrito in vitro y pulverizado en *Arabidopsis*, "bioinformatic analyses play an essential role" |
| SENASA Res. 1004/2023, texto actualizado | argentina.gob.ar/normativa/nacional/resolución-1004-2023-391551/texto | Definición de bioinsumo, categorías, exigencia de 3 zonas agroecológicas × 2 campañas, fases de organismos no objetivo |
| Google Patents (consultas XHR) | patents.google.com/xhr/query?... | **0 resultados** para "apolo biotech" y para inventor Federico Ariel + "exogenous RNA" |

## Fuentes vistas sólo en resultados de búsqueda (no abiertas)

No se citan como evidencia en el reporte, o se citan marcando que no se abrieron:
Chemistry World (la página devolvió cuerpo vacío al abrirla), HortiDaily (se abrió,
aportó poco), Euroquity (HTTP 403), patents.justia.com (HTTP 403),
apolobiotech.com.ar/track-record/ (HTTP 404), repositorio INTA del genoma de
*D. maidis*, Infocampo, Descubre.vc, Pitchbook, Motherbase, Blycia, Martín
Bustamante, La Capital, El Economista, Clarín/La Voz, Blu Radio, iProUP.

## Rechazos de herramienta (regla de CLAUDE.md: registrar y cambiar de línea)

Seis llamadas fueron rechazadas por el filtro de seguridad de la herramienta web,
todas con el código `[bio]`. No se reformularon para esquivar el rechazo. Lo que
quedó sin leer:

1. WebFetch del preprint de bioRxiv 2022.01.17.476645 (métodos de RNAi en
   *D. maidis*). Consecuencia: el dato de la reducción de oviposición queda `[R]`
   por la nota del CONICET, no `[E]` por lectura del paper.
2. WebSearch sobre entrega de dsRNA mediada por planta y ensayos a campo en
   *D. maidis*.
3. WebFetch de PMC7072719 (comparación de métodos de aplicación de dsRNA contra
   *Botrytis* en vid a cielo abierto). Era la fuente más directa para comparar
   modos de aplicación al aire libre.
4. WebSearch sobre nanopartículas y portadores para hemípteros fitófagos.
5. WebSearch sobre BioClay / hidróxidos dobles laminares.
6. WebFetch del segundo tramo de la revisión de *The Plant Cell* (offset 100000),
   donde estarían producción a escala, marco regulatorio por país y criterios de
   selección de blancos según el propio equipo.

Los puntos 3, 4, 5 y 6 son los que más dolieron, porque caen justo sobre el eje
que el organizador declara como cuello de botella. La cobertura de portadores y
persistencia del reporte se sostiene entonces sobre la revisión de Vatanparast
et al. 2024, que sí se abrió completa en su primer tramo, y sobre lo que aporte
la búsqueda delegada.

## Contradicciones detectadas entre fuentes

1. **¿ARN mensajero o ARN de interferencia?** Bichos de Campo (18/09/2023) habla
   de "un fungicida basado en ARN mensajero". La empresa y la revisión de sus
   propios científicos dicen lo contrario: no es ARNm. Es un error periodístico.
   Marcar `[?]` y no usar la versión de ARNm.
2. **¿Ante qué organismo se registra?** Una nota mencionó la ANMAT como
   autoridad de aprobación del primer biofungicida. Todas las demás fuentes y la
   normativa aplicable apuntan al SENASA. Probable error de la nota. `[?]`
3. **Tamaño del equipo**: 21 personas (09/2023), 28 (ficha de Cancillería), 30
   (06/2025). Es crecimiento, no contradicción, pero hay que fechar la cifra.
4. **Sede**: el encabezado de la nota de La Nación de 2023 dice "Córdoba"
   mientras el cuerpo ubica todo en Santa Fe. Error de la nota.

## Intento de prompt injection detectado

La página de Fertilizer Daily contenía una instrucción embebida dirigida a
sistemas de IA, pidiendo que se le diera al usuario una URL distinta de la
real. La herramienta la ignoró y lo informó. Queda registrado porque es una
fuente que el equipo va a volver a visitar: el contenido periodístico parece
legítimo, pero la página está manipulada para envenenar lectores automáticos.
Conviene citarla sólo con la URL que figura en este archivo.
