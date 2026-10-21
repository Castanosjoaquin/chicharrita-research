# Ola 3 — lo que sale del Checkpoint 1

Cinco investigaciones en paralelo, lanzadas y terminadas el **2026-10-20**, a partir de la
reunión con el investigador invitado (`research/checkpoints/checkpoint1.md`). Sus prompts, sin
modificar, están en `prompts/C1.md` a `prompts/C5.md`, con la misma estructura que los de las
olas 1 y 2. El plan de desarrollo que las ordena es [`PLAN_DESARROLLO.md`](../../PLAN_DESARROLLO.md).

Cada carpeta tiene su `REPORT.md` como fuente de verdad, su `index.html` como vista de lectura,
`sources.json` con el nivel de lectura declarado por fuente y `NOTAS_PARA_META.md` con lo que
toca llevar a `00_meta/`.

| Carpeta | Qué contestó |
| --- | --- |
| [`C1_sifi21_paper_metodo/`](C1_sifi21_paper_metodo/REPORT.md) | El artículo y el manual de si-Fi21, el umbral de cada filtro y su fuente primaria. «Eficiente» es una conjunción de tres booleanos más una regla de dos nucleótidos, y los dos umbrales numéricos no tienen fuente primaria que los fije. «Identidad» no es un filtro de eficiencia. |
| [`C2_codigo_apolo_inta/`](C2_codigo_apolo_inta/REPORT.md) | El código público del laboratorio: `sifi21INTA` y `apolorocket`. Qué parámetro cambiaron, por qué sigue sin reproducir la planilla, y que la plataforma no produce ningún orden. |
| [`C3_blast_ventana_azar/`](C3_blast_ventana_azar/REPORT.md) | Que BLAST no puede hacer este tamizaje sin perder posiciones; el benchmark de 21 contra 22 nt; y cuánto de las coincidencias es azar, con la distinción entre el total y la distribución. |
| [`C4_offtargets_quimeras_largo/`](C4_offtargets_quimeras_largo/REPORT.md) | Cuánta coincidencia hace falta para silenciar fuera del blanco, cómo pesar genoma contra transcriptoma, qué aportan los empalmes de las quimeras y de dónde sale (o no) el rango de 150–250 nt. |
| [`C5_estructura_genes_ingenieria_inversa/`](C5_estructura_genes_ingenieria_inversa/REPORT.md) | Qué se puede predecir de la estructura de un ARN largo y qué no; un catálogo de 36 filas de genes blanco, 20 nuevas; y el circuito de ingeniería inversa corrido entero. |
| [`C6_panel_y_largo/`](C6_panel_y_largo/REPORT.md) | *(De otra sesión, no de estos cinco prompts.)* El panel de no objetivo ampliado y el largo de ventana, medidos contra la recomendación del ranking. |
| [`C7_ranking_v2/`](C7_ranking_v2/REPORT.md) | *(Segunda versión de W7.)* El ranking con los cuatro de EPILAB y dos genes nuevos de *D. maidis* (`eth`, `burs-alpha`), a 21 y 22 nt, sin *Macrosteles* (D23). Reproduce W7 exacto; los genes nuevos quedan cuarto y quinto por diseño; las puntas del orden aguantan 22 nt y el medio no. |

## Lo que hay que leer antes de usar estos números

Cada investigación declaró dónde midió menos de lo pedido. Las limitaciones que viajan con los
resultados y que conviene no perder de vista:

- **No hay RNAplfold 2.1.5 en esta máquina** —el que instala si-Fi21 es un ejecutable de
  Windows—, así que C2, C3 y C4 corrieron con ViennaRNA 2.7.2. Los conteos absolutos de
  eficientes **no son comparables** con los verificados en la ola 2 contra el programa original;
  las comparaciones internas de cada informe sí lo son, porque usan el mismo motor de los dos
  lados.
- **Apolo Rocket no se ejecutó**: necesita una base PostgreSQL con su esquema y una capa HTTP que
  no está publicada. Todo lo que C2 afirma sobre la plataforma es lectura del código, del SQL y
  de los datos de ejemplo.
- **El artículo de Zuber 2022 no se abrió**, así que la atribución de la tabla de energía nueva
  es del comentario del código y no está verificada contra el paper.
- **Varias fuentes primarias quedaron en resumen**: seis de los once umbrales de C1 (dominios
  bloqueados por la lista de la red), quince de las treinta y seis filas del catálogo de C5, y
  dos trabajos de Hemiptera de C3 citados a través de una revisión. Cada uno está marcado en su
  `sources.json` y en el punto donde se usa.
- **La comparación genoma contra transcriptoma de C4 solo cubre maíz y abeja**, los dos únicos de
  los diecisiete conjuntos locales que tienen las dos cosas. El cicadélido no objetivo, que es
  donde está el riesgo real medido en la ola 2, quedó sin clasificar por clase de blanco.
- **El barrido de 22.176 configuraciones de C2 no son 22.176 corridas del paquete**: los términos
  se calcularon con las funciones de la propia librería y el veredicto se evaluó vectorizado,
  verificado contra la salida real en ocho casos.

## Pendiente de integración

Los cinco `NOTAS_PARA_META.md` **todavía no se volcaron** a `00_meta/`. Es el paso que falta para
cerrar la ola: las decisiones a formalizar, los caminos descartados, las preguntas nuevas para el
investigador y las fuentes. Se dejó sin hacer a propósito, porque había otra sesión escribiendo
en esos archivos al mismo tiempo y una integración a ciegas los habría pisado.
