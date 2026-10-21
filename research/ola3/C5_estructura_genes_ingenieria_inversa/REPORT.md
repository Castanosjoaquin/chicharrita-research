# C5 — Estructura del ARN largo, genes blanco en hemípteros e ingeniería inversa

Investigación C5 de la **ola 3** del Investigathón Y-Hat, derivada del Checkpoint 1.
Fecha de todas las consultas y corridas: **20 de octubre de 2026**. Todo corrió local; ninguna
secuencia del corpus de EPILAB se usó ni se subió a ningún servicio. Marcadores según `CLAUDE.md`:
`[E]` establecido, `[R]` reportado, `[H]` hipótesis nuestra, `[?]` incierto.

Documentos de esta carpeta: [`estructura_arn_largo.md`](estructura_arn_largo.md) (Q1),
[`catalogo_genes_blanco.md`](catalogo_genes_blanco.md) y
[`catalogo_genes_blanco.json`](catalogo_genes_blanco.json) (Q2),
[`ingenieria_inversa.md`](ingenieria_inversa.md) (Q3), más `scripts/`, `resultados/`,
[`sources.json`](sources.json) y [`NOTAS_PARA_META.md`](NOTAS_PARA_META.md).

---

## Las tres respuestas

### Q1. ¿Se puede predecir hoy la estructura de un ARN largo, y eso importa para la eficiencia?

**La afirmación del investigador se sostiene, con una precisión que habilita trabajo y un hallazgo
que reordena el problema.**

La precisión: lo que no se puede predecir de un ARN de 800 nucleótidos es la estructura **global**.
El plegado **local** —probabilidades de apareamiento y accesibilidad dentro de un radio de unos 150
nt— sí se predice, y con exactitud publicada: exactitud mediana de pares de bases de **0,65** para
plegado local con alcance 150 contra **0,55** del plegado global, sobre 2.158 elementos curados de
90 familias de Rfam, y una tasa de fracaso del **11 %** contra **22 %** (Lange et al. 2012, *NAR*
40:5215) `[E]`. La ventaja del local **crece** en ARNm completos. Como el 85 % de los apareamientos
reales cae dentro de 100 nt, el régimen útil está cubierto y el resto no. En 3D no hay nada que
discutir: ninguna estructura natural no vista superó TM-score 0,8 en CASP16 y el mejor método
declara degradación por encima de ~500 nt (`research/R4_frontier_ml_rna/REPORT.md` §2.2) `[E]`.

El hallazgo: **sí hay evidencia publicada en insectos sobre estructura y eficacia, y separa dos
cosas que el equipo venía tratando juntas.** En el único experimento controlado del campo —31
siRNA individuales en un esqueleto común, inyectados a 1 µg/µL en larvas L5 de *Tribolium
castaneum*, n = 20 por grupo, más 8 genes con tres o cuatro ARNdc cada uno a 1 ng/µL con n = 25—
la **ausencia de estructura secundaria dentro del siRNA de 21 nt resultó predictora significativa
de eficacia insecticida**, y la **accesibilidad del sitio blanco en el ARNm no resultó
significativa**: P > 0,05 en el modelo de Cox del primer ensayo y **P = 0,41** en la regresión del
segundo, donde además se habían diseñado ARNdc expresamente sobre la región de máxima
accesibilidad (Cedden et al. 2025, *BMC Biology* 23:114) `[E]`. La estructura que importa se
calcula sobre 21 nt, que es el régimen fácil; la que requeriría plegar 800 nt es la que no
apareció.

Y el vacío, que es resultado: **no encontramos ningún estudio que mida si el plegado de la molécula
de ARNdc larga cambia la eficacia**, en insectos ni fuera de ellos. Sobre datos experimentales, el
conjunto más grande del campo —Ribonanza, dos millones de secuencias con mapeo químico— tiene
**170.000 secuencias con señal-ruido mayor que 1**, llega a **457 nt** de largo máximo y reporta
que las secuencias largas dan *peor* señal `[R]`. El cuello de botella no es sólo el precio: el
instrumento mide peor cuanto más larga es la molécula.

### Q2. ¿Qué genes blanco tienen evidencia en hemípteros y en *Dalbulus maidis*?

**Treinta y seis filas, de las cuales veinte las agrega esta investigación y dieciséis vienen del
catálogo que ya tenía el pipeline.** El detalle está en
[`catalogo_genes_blanco.md`](catalogo_genes_blanco.md); lo que cambia el panorama es esto.

Hay un blanco **letal y esterilizante probado en dos géneros de cicadélidos de nuestra subfamilia**,
publicado en 2025: la subunidad reguladora del proteasoma 26S que los autores llaman `Rpn6`, por
microinyección de 80 ng por insecto, con transcripto reducido entre 5,8 y 14,9 veces, supervivencia
significativamente menor (P = 0,028 contra el control de dsGFP en *Scaphoideus titanus*, P < 0,001
en *Euscelidius variegatus*) y progenie de **0,03 ninfas por día de oviposición contra 1,5** de los
no tratados `[E]`. Con una advertencia que medimos nosotros: por secuencia, el transcrito usado
pertenece a la familia **PSMD6** y no a PSMD11/`Rpn6` `[?]` —el detalle, en
[`ingenieria_inversa.md`](ingenieria_inversa.md) §3—.

Los dos genes con evidencia funcional en la **propia especie objetivo** que el catálogo del pipeline
no tenía son `eth` y `burs-alpha`: knockdown de ~90 % y ~95 %, supervivencia del 10 % al día 4
contra más del 95 % del control, n = 40 por tratamiento, 125 ng por insecto `[E]`. Tienen ARNm
público de *D. maidis* y por eso son los únicos candidatos nuevos a los que se les pudo calcular la
ventana sobre la secuencia correcta: 44 y 33 siRNA eficientes, con mejores regiones de 200 nt en
194-393 (24 eficientes) y 45-244 (20 eficientes).

Hay dos **contraejemplos** que valen tanto como los blancos: silenciar `uk1_LRR` en *E. variegatus*
aumentó la colonización del vector por el fitoplasma, y silenciar `NcHig` en *Nephotettix
cincticeps* aumentó la infección por un rabdovirus `[R]`. Son genes a excluir explícitamente, y
ningún tamizaje de esencialidad o de off-targets los marcaría.

Y hay un resultado negativo sobre el propio ejercicio: **ningún gen nuevo se destaca por densidad
de ventanas eficientes** —todos caen entre 5,7 % y 12,8 %, el mismo rango que los cuatro candidatos
de EPILAB—, lo que es coherente con lo que el pipeline ya había medido: lo que discrimina es qué
gen se ataca y el filtro de especificidad `[H]`.

### Q3. ¿El circuito de ingeniería inversa coincide con la práctica estándar y con nuestro pipeline?

**Sí, y el paso que el investigador marcó como crítico es exactamente donde se rompe.** Lo corrimos
entero sobre un gen nuevo y medimos los tres puntos de falla.

El umbral de **99 % de identidad** como señal de conservación no es alcanzable entre géneros de
cicadélidos: medimos 83,6 % de identidad de nucleótidos entre el `Rpn6` de *S. titanus* y su
ortólogo en *Macrosteles quadrilineatus*, 77,3 % contra *Homalodisca vitripennis*, y sobre los
12.540 loci recuperados la identidad proteica mediana es **0,866**, con sólo **244 loci (1,9 %)** por
encima de 0,99 `[H]`. Hay además una ambigüedad en la pregunta misma, medida sobre un solo par de
genes y las dos escalas: el ortólogo del cicadélido anotado alinea contra el locus recuperado en el
vector con **85,7 % de identidad de nucleótidos ponderada sobre 1.232 nt** (seis bloques exónicos,
83,7-88,7 %) y con **0,978 de identidad proteica**, de modo que un umbral de 99 % significa cosas
opuestas según qué identidad se esté mirando. Buscar el gen **por nombre**
en el transcriptoma de la especie cercana devolvió un gen distinto del que devolvió la homología
—que además cae en **otro cromosoma** del vector, `OZ319708.1` contra `OZ319707.1`—, con **162
contra 98** ventanas eficientes: un 65 % de diferencia en el número que el laboratorio usa para
decidir `[H]`. Y la secuencia
recuperada en la especie cercana **no sirve para diseñar**: entre el 0,7 % y el 11,1 % de sus
ventanas de 21 nt existen idénticas en el genoma de *D. maidis*, contra el 89-91 % de los genes que
sí son del vector `[H]`.

**Sobre 384 o 684: no es ninguna de las dos.** Ya estaba adjudicado en
`00_meta/PREGUNTAS_ABIERTAS.md` y corregido en la transcripción del checkpoint antes de que esta
investigación corriera; C5 lo verificó de forma independiente con `grep` sobre el árbol versionado y
`git grep` sobre todos los commits (`resultados/384_684_busqueda.txt`) y **agrega una quinta cifra,
con la referencia que el propio circuito recomienda**: con el proteoma anotado de un cicadélido,
**32.269 de 34.269 proteínas encuentran locus (94,2 %) y colapsan en 12.540 loci distintos**. La
tabla de qué cuenta cada número está en [`ingenieria_inversa.md`](ingenieria_inversa.md) §5. La
razón de fondo por la que la cifra se pudo decir mal es que «genes recuperados» nombra siete
cantidades distintas que van de 62 a 32.269.

---

## Qué se corrió, y con qué

Cinco scripts, todos en `scripts/`, todos reproducibles desde la raíz del repositorio. Nada se
subió a ningún servicio: las únicas llamadas salientes fueron a NCBI E-utilities y UniProt, por
secuencias y metadatos **públicos**, y a los servidores de los editores para los textos completos.

| Script | Qué hace | Costo medido |
|---|---|---|
| `01_recuperar_genes_miniprot.sh` | `miniprot` del proteoma de *M. quadrilineatus* (34.269 proteínas) contra `ihDalMaid1.1` (972 Mb) | 568 s con 9 hilos, 3,71 GB de RSS máximo |
| `02_ventanas_sifi21.sh` | criterio de eficiencia de si-Fi21, modo `fiel`, sobre 10 secuencias públicas | 3,6 s |
| `03_transferencia_y_no_objetivo.sh` | 21-meros exactos de cada candidato contra 5 referencias locales (genoma del vector, 2 cicadélidos, maíz, abeja) | 105 s |
| `04_circuito_ingenieria_inversa.sh` | el circuito del investigador de punta a punta sobre `Rpn6` | < 2 min (incluye dos `makeblastdb`) |
| `05_contar_genes_recuperados.py` | define y cuenta «genes recuperados» de tres maneras | instantáneo |
| `06_catalogo.py` | genera el catálogo en JSON y en Markdown desde una sola estructura | instantáneo |
| `07_referencias_uniprot.py` | baja las proteínas revisadas de UniProt con las que se resuelve a qué familia pertenece un gen publicado | instantáneo |
| `08_identidad_locus_dmaidis.sh` | identidad de nucleótidos del ortólogo contra el locus recuperado en el vector, para comparar las dos escalas de identidad sobre el mismo par de genes | < 10 s |

Las herramientas de terceros se usaron **sin modificarlas**: el port de si-Fi21 del repositorio
(`tools/sifi21_port/run_sifi.py` y `offtarget_21nt.py`), `pipeline/resumir_miniprot.py`,
`pipeline/buscar_rnai_hemipteros.py`, `miniprot` 0.18-r281, BLAST+ y ViennaRNA 2.7.2.

---

## Lo que esto cambia para el equipo

**El término de accesibilidad tiene ahora una medición en contra y una a favor, y la en contra es
en insectos.** La decisión vigente —calcularla, reportarla, peso cero por defecto— queda
respaldada por el único experimento que la puso a prueba de frente en bioensayo. Lo que sí hay que
mantener, porque la misma fuente lo encontró significativo, es el término de **autoplegado de la
hebra guía**, que si-Fi21 ya calcula y que se computa sobre 21 nt.

**El catálogo de blancos deja de depender de un único orden de insectos.** La debilidad declarada
del pipeline es que el 100 % de los fenotipos viene de *Tribolium castaneum*, un coleóptero. Las
veinte filas nuevas incluyen seis estudios en Cicadellidae con fenotipo medido y cinco en
Delphacidae, lo que permite que un candidato se apoye en evidencia de la propia familia.

**Y hay una regla operativa nueva para el paso 4 del circuito:** resolver la identidad del gen por
secuencia antes de buscarlo por nombre. Cuesta un `blastx` contra UniProt y evita el error más caro
del circuito.

---

## El cierre sobre «el que resuelva la estructura se gana el Nobel»

Qué datos públicos existen hoy: mapeo químico de dos millones de secuencias en Ribonanza, de las
cuales 170.000 con señal-ruido utilizable y ninguna por encima de ~457 nt; los conjuntos curados de
estructura secundaria (Rfam, bpRNA, ArchiveII), dominados por cuatro familias; y una evaluación
ciega oficial en 3D (CASP16) que concluyó que no hubo aumento notable de exactitud respecto de los
desafíos anteriores `[E]`/`[R]`.

Qué faltaría: estructura medida de moléculas del tamaño que se aplica —200 a 800 nt—, en condiciones
que se parezcan a las reales, y con eficacia medida sobre las mismas moléculas. Hoy no existe
ninguna de las tres cosas juntas para un insecto.

Puede el equipo aportar algo sin laboratorio: **para resolver la estructura, no.** El cuello de
botella es instrumental y se degrada con el largo de la molécula, así que ningún método nuevo lo
sortea. Lo que sí puede aportar, y está al alcance de esta semana, es declarar el régimen de
validez de cada término estructural que use su puntaje, medir la ablación del término de
accesibilidad sobre su propio ranking —que es la pregunta que la literatura dejó sin adjudicar— y
usar los 8 genes con tres o cuatro diseños cada uno de dsRIP como conjunto de validación
retrospectiva. Es un aporte de método, no de biología, y es el que corresponde a un equipo de datos.

---

## Lo que no pudimos hacer

**Quince fuentes quedaron en resumen y no en texto completo** —contra siete abiertas enteras por
C5 y tres ya leídas en la ola 2—, y las filas del catálogo que dependen de ellas no llevan dosis ni
`n`. La más importante es Pest Manag Sci 2019 (PMID 30417535), el único
estudio de mortalidad por ARNi en *E. variegatus*, detrás de muro de pago; Unpaywall no devolvió
PDF y no se intentó ninguna vía alternativa.

**Las ventanas de los candidatos nuevos se calcularon sobre ortólogos de otra especie** en seis de
los ocho casos, porque no hay secuencia pública del gen en *D. maidis*. Están declaradas como
sustituto en cada fila, y la propia medición de transferencia muestra cuánto se pierde.

**No se corrió ortología recíproca ni se evaluó parálogos** para los candidatos nuevos: el ortólogo
se asignó por mejor hit de `blastn` más verificación de familia por `blastx` contra UniProt, que es
más de lo que hacía el circuito pero menos que una ortología formal.

**No se buscó evidencia sobre `Macrosteles quadrilineatus`** más allá de la consulta a PubMed, que
devolvió cero resultados de ARNi funcional para esa especie pese a ser el cicadélido mejor anotado.

**No se tocaron** `00_meta/` ni los informes de otras investigaciones; los aportes a la memoria del
proyecto están en [`NOTAS_PARA_META.md`](NOTAS_PARA_META.md).
