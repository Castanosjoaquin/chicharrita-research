# Metodologías de los tres ejes y plan de equipo

**Investigación R5.** Cierre 17 de octubre de 2026. Responde cómo se trabaja de
verdad en cada uno de los tres ejes en los que el equipo decidió competir
—bioinformática y datos, desarrollo computacional, innovación abierta—, cómo se
evalúa una solución de ARN exógeno contra la chicharrita del maíz (*Dalbulus
maidis*) y qué hace cada una de las cuatro personas del equipo.

Este archivo es la fuente de verdad en prosa. Los otros cinco son la parte
operable: `RUBRICA.md` es la rúbrica de priorización lista para aplicar,
`PLAN_EQUIPO.md` el reparto con su cronograma y su plan B,
`stack_bioinformatico.md` la tabla de bases de datos y herramientas con URL,
formatos y si corren en una notebook, `sources.json` el registro estructurado de
fuentes con el alcance de verificación de cada una, e `index.html` la vista de
lectura. No hay nada afirmado acá que no esté en `sources.json` con su fuente.

**Cómo leer los marcadores.** `[E]` establecido en literatura revisada o en
norma vigente; `[R]` reportado por una o pocas fuentes, preprint, nota técnica o
material institucional; `[H]` hipótesis nuestra; `[?]` incierto o contradictorio
entre fuentes.

**Estado de verificación, dicho de entrada.** Esta investigación se hizo en dos
corridas. La primera verificó 43 fuentes, entre ellas los sitios
institucionales argentinos y brasileños (INTA, CONICET, Secretaría de
Agricultura, Embrapa) y las API de GBIF e iNaturalist, y dejó las citas
textuales en `notes/evidencia_verificada.md`. La segunda, que escribió este
reporte, abrió 11 fuentes nuevas de literatura por texto completo y verificó dos
recursos más por uso directo de su API —NCBI Datasets y la API REST de Europe
PMC—, de modo que el total citado es de 56 fuentes abiertas sobre 57
registradas: la única que figura como no verificada no se cita. En esta segunda
corrida los dominios institucionales
(`argentina.gob.ar`, `embrapa.br`, `repositorio.inta.gob.ar`, `api.gbif.org`) no
estaban accesibles desde el entorno de trabajo, así que **todo lo que este
reporte afirma sobre esas fuentes se apoya en la verificación de la primera
corrida y no se volvió a comprobar hoy**. Está marcado donde corresponde. Lo que
no se pudo abrir en ninguna de las dos corridas está en la sección 6.

---

## 1. Eje bioinformática y datos

La pregunta de este eje no es qué base de datos existe —eso es la tabla de
`stack_bioinformatico.md`— sino en qué orden se consultan, qué pipeline se
arma con lo que devuelven y dónde el proyecto se choca con un hueco. La
respuesta corta, y es la decisión metodológica más importante de toda la
investigación: **en este sistema la consulta no empieza por el genoma, porque el
genoma no sirve para elegir blancos todavía.**

### 1.1 El orden de consulta, y por qué ese orden

El primer paso no es descargar: es contar. Antes de bajar un solo archivo se
pregunta qué existe, con las E-utilities y la API `datasets v2alpha` del NCBI,
que devuelven texto plano y por lo tanto dejan registro auditable de la consulta
`[E]`. Ese paso, que parece burocrático, fue el que produjo el hallazgo que
reorganiza todo lo demás: *D. maidis* tiene tres ensamblados de genoma en
GenBank —el cromosómico del Wellcome Sanger Institute `GCA_975739785.1`, con
972.206.121 pb en diez cromosomas, su haplotipo alternativo `GCA_975739835.1`, y
el CIAP v1 del INTA `GCA_054756405.1`— y **ninguno de los tres tiene anotación
de genes en el NCBI** `[E]`: la API no devuelve bloque `annotation_info` para
ninguno y `annotation_summary` sobre el cromosómico devuelve HTTP 404.

Hay genoma y no hay modelos de genes. Eso descarta el camino que cualquiera
elegiría por defecto —partir del genoma anotado, elegir genes esenciales,
diseñar sobre sus transcriptos— y obliga al segundo paso: el transcriptoma
ensamblado. Xu et al. (2021), *Microbiology Spectrum* 9:e00612-21, depositaron
**56.116 transcriptos no redundantes** de la especie bajo la accesión
`GITV00000000`, con 82,4 % de completitud BUSCO (1.126 de 1.367 BUSCOs
completos, v4.1.1) `[E]`. Ese archivo, de decenas de megabytes, es el insumo
central del proyecto: es sobre él que se eligen regiones blanco y contra él que
se tamiza la especificidad dentro del propio vector.

El tercer paso es el cultivo a proteger, porque la pregunta del track nombra al
maíz como primer sujeto a no dañar: el transcriptoma y el proteoma de *Zea mays*
se bajan del FTP de Ensembl Plants, que es la URL que efectivamente entrega
archivos `[E]`, y no de la página web, que no renderiza sin JavaScript.

El cuarto paso son los patógenos, y acá esta corrida corrige un supuesto del
equipo. La primera corrida había concluido que *Spiroplasma kunkelii* era el
único patógeno del complejo con genoma completo y anotado —`GCA_001274875.1`,
1.514.561 pb, 1.685 genes codificantes `[E]`— y que ninguno de los cuatro
ensamblados de '*Candidatus* Phytoplasma asteris' correspondía a un aislado de
maíz. Lo segundo es cierto y lo primero es falso: **el fitoplasma del
achaparramiento arbustivo del maíz (maize bushy stunt) tiene genoma completo en
una sola secuencia desde agosto de 2016**. Es `GCA_001712875.1` /
`GCF_001712875.1`, cepa M3, 576.118 pb, 28,5 % de GC, una sola secuencia
circular, enviado por la Academia Sinica, secuenciado en Illumina MiSeq y
ensamblado con Velvet 1.2.10; la anotación original declara 544 genes, 485 de
ellos codificantes, y la reanotación de RefSeq del 7 de junio de 2026 declara
581 genes y 524 codificantes `[E]`. La muestra de origen, `SAMN04623572`, se
colectó el 29 de mayo de 2013 en Piracicaba, São Paulo, Brasil, y su hospedador
declarado es *Dalbulus maidis* `[E]`. Todo esto se verificó por consulta directa
a la API de NCBI Datasets en esta corrida.

El dato se nos había escapado por una razón de nomenclatura que vale la pena
entender, porque va a volver a pasar: el organismo figuraba en la literatura
como "maize bushy stunt phytoplasma", un nombre informal que no es un taxón, y
recién en 2026 recibió nombre formal. Pellegrinetti et al. (2026),
*International Journal of Systematic and Evolutionary Microbiology* 76(10),
doi 10.1099/ijsem.0.007301, proponen '*Candidatus* Phytoplasma zeae' sobre la
base de distinción ecológica, especificidad de vector, comparación de genomas
completos y consenso de la comunidad de investigación; la identidad del gen 16S
rRNA con '*Ca.* P. asteris' supera el 99 %, pero la identidad nucleotídica
promedio (*average nucleotide identity*, ANI) entre '*Ca.* P. zeae' y todos los
genomas disponibles de cepas emparentadas con '*Ca.* P. asteris' cae entre 92,6
y 98,4 % `[E]`. La taxonomía del NCBI ya usa ese nombre para el genoma M3
(TaxId 202462). Para el equipo esto significa que la búsqueda por el nombre
viejo no encuentra lo que existe, y que el pedido al investigador sobre "cuál de
los genomas de fitoplasma corresponde al complejo del maíz" ya tiene respuesta
pública.

El quinto paso son los organismos no objetivo, que es el insumo de la mitad
"riesgo" de la pregunta del track y el que no existe curado en ninguna parte
para el agroecosistema del maíz argentino: hay que armarlo, y cómo se arma está
en la sección 4 y en el criterio C3 de `RUBRICA.md`. El sexto es la anotación
funcional —BLASTX contra UniProtKB, asignación de ortología KO en KEGG, y
tamizaje contra Rfam, que en su release 15.1 de enero de 2026 tiene 4.227
familias de ARN no codificante con modelos de covarianza `[E]`— para no diseñar
un disparador contra un ARN estructural conservado. El séptimo, opcional pero
barato, es la distribución del vector: GBIF devuelve 610 registros globales de
*D. maidis*, de los cuales 17 en Argentina, e iNaturalist 151 observaciones
`[E]`, ambos verificados por uso de la API en la primera corrida. Ese número
—17 registros abiertos en el país del brote— es en sí mismo un resultado, y
reaparece en la sección 3.

### 1.2 Los dos precedentes publicados en este mismo patosistema

La regla de esta investigación es que ninguna metodología se propone sin mostrar
quién la usa. Para este eje hay dos trabajos publicados que hacen exactamente lo
que el equipo va a hacer, sobre el mismo insecto, y conviene copiarles el método
antes que inventar uno.

El primero es el del grupo de María Inés Catalano. Andrada et al. (2026),
*Frontiers in Insect Science* 6:1811933, para silenciar *eth* y *burs-α* en
*D. maidis* trabajaron sobre un transcriptoma propio del laboratorio, corrieron
el análisis en **Galaxy Europe**, y verificaron la especificidad del dsRNA y de
los cebadores con tBLASTn y BLASTn con umbrales explícitos —E-value menor a
1×10⁻⁴, identidad mayor al 35 %, bit score mayor al 40 %—, más ExPASy Translate,
Primer3plus, Jalview v2.11.5.1 con MAFFT en modo L-INS-i, BEAST X v10.5.0,
Tracer v1.7.2, TreeAnnotator, iTOL v6 y GraphPad Prism v8.0.2 `[R]`. Dos cosas
se aprenden de ahí. Una, que el tamizaje de especificidad con BLAST y umbrales
declarados es el estándar de facto aceptable en una publicación de esta
comunidad, y que no hace falta una plataforma propietaria para publicarlo. Otra,
que cuando el cómputo no entra en la máquina de uno, la salida de la gente que
publica en esta especie es Galaxy, no un cluster privado.

El segundo es el de Pellegrinetti et al. (2026), ya citado, y es el ejemplo
completo de un pipeline de genómica hecho con software libre y datos públicos:
recortado de lecturas con fastp v0.23.4, remoción de lecturas del hospedador
—incluido el propio *D. maidis*— con KrakenTools v1.2, ensamblado con dos
ensambladores metagenómicos en paralelo (MEGAHIT v1.1.4 y MetaSPAdes v4.1.0)
para comparar desempeño, identificación de los contigs del fitoplasma por BLAST
nucleotídico contra el genoma M3 ya existente, andamiaje con RagTag v2.1.0,
pulido con Pilon v1.23.0, control de calidad con CheckM y CheckM2 —completitud
entre 97,14 y 98,57 % y contaminación 0 % por el primero— anotación con Bakta
v1.11.3 y análisis pangenómico con el flujo de Anvi'o v8 `[E]`. Es la
demostración práctica de la afirmación de la sección 1.4: casi todo este camino
es software que corre en una notebook sobre genomas bacterianos de menos de un
megabase.

### 1.3 El pipeline de diseño y tamizaje, paso por paso

Lo que sigue es el camino concreto, con la herramienta de cada paso y el formato
que circula. No es una propuesta nuestra: es la reconstrucción de lo que hacen
las dos herramientas de referencia del campo, si-Fi y dsRIP, cuyos papers
describen su funcionamiento interno.

1. **Del transcripto a los ORF.** Se corre TransDecoder sobre los 56.116
   transcriptos del TSA. El paso existe porque la evidencia dice que apuntar al
   marco abierto de lectura (*open reading frame*, ORF) supera a apuntar a las
   regiones no traducidas: en el modelo de riesgos proporcionales de Cedden et
   al. (2025), *BMC Biology* 23(1):114, apuntar al ORF aportó una razón de
   riesgo de 9,91 con P = 0,011 `[E]` en *Tribolium castaneum*. Entra FASTA de
   transcriptos, sale FASTA de CDS y péptidos más un GFF3.
2. **Del disparador a la población de siRNA.** Ventana deslizante de 21
   nucleótidos sobre el disparador, con 19 a 23 como parámetro. Es literalmente
   lo que hace si-Fi: parte la secuencia en todos los x-meros posibles, con x el
   largo de siRNA elegido (Lück et al. 2019, *Frontiers in Plant Science*
   10:1023) `[E]`. La interfaz de dsRIP ofrece el mismo rango de 19 a 23 nt y
   sugiere 21 para la mayoría de las plagas `[E]`.
3. **Las features de eficacia, calculadas con termodinámica real.** Las cuatro
   que resultaron significativas en Cedden et al. (2025) con P < 0,05 son
   asimetría termodinámica, energía de autoplegado de la hebra antisentido,
   contenido GC en las posiciones 9 a 14 de la antisentido y adenina en la
   posición 10 `[E]`. Se calculan con ViennaRNA 2.7.2, que tiene binarios para
   macOS Intel y ARM y bindings de Python `[E]`. Dos advertencias que hay que
   llevar escritas: el GC **alto** en 9–14 se asocia a **mayor** eficacia, al
   revés de lo que indican los datos humanos, y la accesibilidad del ARNm
   —pilar de la literatura humana y de si-Fi— **no** resultó significativa
   (P = 0,41) `[E]`. Por eso la rúbrica la calcula y la reporta con peso cero.
4. **El tamizaje de off-target.** Bowtie 1 de todos los siRNA derivables contra
   el transcriptoma de maíz, contra el del propio vector y contra los
   transcriptomas de no objetivo, permitiendo 0, 1 y 2 mismatches y reportando
   los tres. Bowtie 1 y no Bowtie 2: el primero está pensado para lecturas
   cortas y es el que usan tanto si-Fi —que lo eligió, en palabras de sus
   autores, por exactitud, velocidad y eficiencia de memoria— como el módulo de
   off-target de dsRIP `[E]`. El criterio de corte tiene dos versiones y hay que
   reportar con cuál se puntuó, porque no coinciden: el umbral de **19
   nucleótidos complementarios** de la revisión de Cedden (2026), *Insect
   Molecular Biology* 35(4):364-375 `[E]`, y el conjunto de reglas de la guía de
   la EFSA de 2025, que tolera hasta cuatro mismatches y un hueco bajo
   condiciones de posición y de energía libre y por lo tanto marca más
   candidatos `[E]`. El detalle está en la compuerta G2 de `RUBRICA.md`.
5. **El cruce con familias de ARN no codificante.** Búsqueda contra Rfam, para
   descartar disparadores que caigan sobre una familia conservada.
6. **La ortología, cuando hace falta transferir un blanco.** OrthoFinder sobre
   los proteomas disponibles, que es el método que dsRIP usa internamente para
   filtrar genes cuyos ortólogos están en la lista curada de letalidad de
   *T. castaneum* `[E]`. Entra un FASTA de proteínas por especie y sale
   `N0.tsv` con los grupos de ortología jerárquicos.

El formato que circula entre pasos es deliberadamente aburrido —FASTA, GFF3,
BED, SAM, dot-bracket, TSV, JSON— y esa es una virtud: cada paso se puede
reemplazar sin tocar los demás, que es la condición para que cuatro personas
trabajen en paralelo.

### 1.4 Qué corre en una notebook y qué no

Corre en una notebook de 16 GB, con holgura: todo el diseño y el tamizaje
descritos arriba, BLAST contra bases propias, OrthoFinder sobre menos de diez
proteomas, BUSCO sobre un transcriptoma, cuantificación con Salmon y todas las
consultas a las API. El motivo es de escala: el objeto de cómputo son
transcriptos de kilobases y genomas bacterianos de menos de un megabase, no el
genoma de casi un gigabase del insecto.

No corre: el ensamblado *de novo* del transcriptoma con Trinity sobre los
1.727.369.026 lecturas de Xu et al., porque la regla práctica de
aproximadamente 1 GB de RAM por millón de lecturas `[R]` lo pone fuera de
alcance; la anotación estructural completa del genoma cromosómico de 972 Mb; y
el mapeo de las 23 corridas de RNA-Seq contra ese genoma dentro del plazo del
evento. Los tres tienen la misma salida, que es no hacerlos: el transcriptoma ya
está publicado y alcanza para lo que el proyecto necesita.

Cuando haga falta un paso pesado, la vía es Galaxy, y no es una recomendación
genérica sino el precedente del grupo que publicó RNAi en esta especie. La
actualización de 2024 del proyecto (*Nucleic Acids Research* 52(W1):W83)
documenta que los servicios públicos de Estados Unidos, Australia y Europa
acumulan más de 500.000 usuarios registrados y que durante 2023 más de 11.000
usuarios individuales corrieron, en promedio, más de 1.000.000 de trabajos por
mes, con más de 9.000 herramientas disponibles y estadísticas operativas
públicas `[E]`. Es infraestructura gratuita, con trazabilidad, y el mismo
trabajo documenta que cada trabajo muestra una estimación de sus emisiones de
CO₂ `[E]`, dato que sirve para una pregunta previsible del jurado sobre el costo
ambiental del cómputo.

### 1.5 Cuál es el entregable defendible de esta rama

Dos artefactos, y conviene decir por qué cada uno es defendible y no sólo
trabajoso.

El primero es un **paquete de datos congelado y versionado** (*data package*):
los insumos de arriba, con su manifiesto de hashes, la licencia declarada de
cada uno y su procedencia. Es defendible porque hoy no existe: cualquiera que
quiera repetir un análisis sobre este sistema tiene que volver a averiguar que
los genomas no están anotados, que el transcriptoma útil está en el TSA y no en
Assembly, y que el fitoplasma cambió de nombre en 2026. Ese trabajo es el que
hace que todo lo demás sea reproducible, y es exactamente lo que los principios
FAIR llaman procedencia y licencia de uso (Wilkinson et al. 2016, *Scientific
Data* 3:160018, principios R1.1 y R1.2) `[E]`.

El segundo es el **informe de especificidad por candidato**: para cada
disparador, los conteos de hits contra maíz, contra el propio vector y contra
cada taxón no objetivo, con los dos criterios de corte, los tres niveles de
mismatch, y la lista explícita de los taxones **donde no se pudo mirar porque no
hay transcriptoma público**. Es el entregable más valioso de la rama por una
razón que la rúbrica demuestra numéricamente en su sección 7: es la medición más
barata que más cambia el orden de los candidatos. Cuesta horas de cómputo en una
notebook, con datos públicos, sin laboratorio y sin permiso de nadie.

---

## 2. Eje desarrollo computacional

### 2.1 Qué construye, de hecho, la gente que hace esto

Antes de elegir qué construir conviene mirar qué construyeron los tres grupos
que publicaron herramientas de diseño de dsRNA, porque las tres eligieron
arquitecturas distintas y las tres pagaron un costo por su elección.

**si-Fi / si-Fi21** (Lück et al. 2019) es una aplicación de escritorio con
interfaz gráfica: parte el disparador en x-meros, los alinea con Bowtie,
selecciona la hebra guía con reglas de nucleótido terminal y termodinámica y
calcula accesibilidad con RNAplfold. Corre **solo en Windows 7 o superior**, con
interfaz en Python 2.7 y Qt4 `[E]`. El costo de esa elección es directo y nos
afecta: en las máquinas del equipo no corre sin una máquina virtual, de modo que
cualquier pipeline que dependa de si-Fi no es reproducible para nosotros. La
salida no es descartar sus reglas, que están descritas en el paper, sino
reimplementarlas con ViennaRNA y Bowtie.

**dsRIP** (Cedden et al. 2025) es una aplicación web alojada por la Universidad
de Göttingen, con tres módulos —blancos, eficacia, off-target— y un deslizador
eficacia/seguridad al 50/50 por defecto `[E]`. El costo de ser web es que la
salida hay que exportarla y versionarla a mano, o el puntaje no se puede
regenerar; y que el día que el servicio esté caído, el pipeline se detiene.

**dsRNAEngineer** (preprint en bioRxiv 2024.07.22.604585) es la tercera variante
y la más instructiva para nosotros, porque publica su arquitectura: front-end en
Vue.js, back-end en el framework asincrónico Sanic de Python, visualización de
red con la API Canvas, y **942 transcriptomas** descargados del NCBI que incluyen
plagas de insectos, ácaros, nematodos y hongos más especies de evaluación de
seguridad `[R]`. Su funcionalidad distintiva es *screen-target*: buscar una
región conservada que sirva de blanco común a varias especies de plaga, con
análisis de ventana deslizante de fragmentos de 50 a 100 pb `[R]`. Lo que este
trabajo prueba, y es el punto que importa para la decisión de arquitectura, es
que **el valor de la herramienta está del lado de los datos precargados, no de
la interfaz**: lo que hace útil a dsRNAEngineer son los 942 transcriptomas que
alguien se tomó el trabajo de bajar y ordenar.

Hay dos advertencias de uso. La primera es que del preprint se abrió el texto
completo; la versión revisada por pares existe en *Trends in Biotechnology*
según el índice de búsqueda, pero **no se abrió** y no se cita como tal. La
segunda es que la revisión de Cedden (2026) evalúa esta familia de herramientas
y marca que las predicciones de off-target "need to be experimentally tested" y
que falta validación fuera de coleópteros `[E]`: ninguna de las tres herramienta
está validada en un hemíptero.

### 2.2 Las cuatro opciones de artefacto, evaluadas

Las horas son horas-persona de estudiante de tercer año con cursada en paralelo,
con el presupuesto declarado en `PLAN_EQUIPO.md` de 8 horas por persona por
semana.

| Opción | Arquitectura mínima | Stack | Horas | Qué demuestra | Riesgo principal |
| --- | --- | --- | --- | --- | --- |
| **A. Herramienta de scoring y priorización** | CLI que lee fichas JSON de candidatos e informes de tamizaje, aplica pesos y topes, emite orden, fichas de decisión y análisis de sensibilidad | Python, `pydantic` para validar esquema, `pandas`, salida Markdown/HTML, tests con `pytest` | 26 | Que el equipo convirtió una pregunta abierta —"¿cuáles merecen validación?"— en una función de decisión auditable | Que el jurado lo lea como "una planilla con pasos": se responde con los topes, la sensibilidad y los tests |
| **B. Pipeline reproducible de tamizaje** | Flujo declarativo que baja insumos, construye índices, deriva siRNA, corre Bowtie y ViennaRNA y emite tablas por candidato | Snakemake, entornos por regla desde Bioconda, DVC para los datos | 28 | Que la evidencia del puntaje se regenera con un comando, que es la palabra "reproducible" de la pregunta del track | Tiempo de descarga e indexado; se mitiga con el paquete offline congelado |
| **C. Dashboard de exploración** | Front-end que muestra candidatos, scores y perfiles posicionales | Streamlit o HTML estático con JSON embebido | 12–30 según ambición | Comunicación, nada más | **Es el riesgo declarado por el organizador**: "un equipo no debería ganar por construir la interfaz más vistosa" `[R]`. Horas que no compran decisión |
| **D. API pública** | Servicio que recibe una secuencia y devuelve scores | FastAPI más un contenedor y hosting | 20 + mantenimiento | Que la herramienta es consumible por terceros | Nadie la va a consumir en el plazo del evento, y requiere hosting que hay que sostener |

### 2.3 La recomendación, y por qué

**A + B fusionados, con C reducido a una vista de lectura estática y D
descartada.** El argumento no es de gusto: el material del organizador dice
textualmente que un equipo "no debería ganar por construir la interfaz más
vistosa, sino por producir la mejor decisión científica posible con el tiempo y
los datos disponibles" `[R]`. Un dashboard compite por horas con el motor de
decisión y no agrega evidencia. La vista de lectura sí se construye —un HTML
estático con el JSON de resultados embebido, sin servidor— porque cuesta pocas
horas y hace legible el resultado en un teléfono.

Hay además un argumento de hueco. Lo que ya existe y funciona es la plataforma
de diseño con chequeo de off-targets: dsRIP, dsRNAEngineer, si-Fi, y en el país
Apolo Rocket. Lo que nadie publicó es el **criterio de agregación** que convierte
esos reportes en un orden defendible, con pesos declarados antes de puntuar,
topes que impiden compensar una barrera de entrega inexistente con un diseño de
secuencia brillante, y un análisis de sensibilidad que diga cuál es la medición
más barata que cambiaría la decisión. Ese es el artefacto que el equipo puede
construir y que nadie tiene.

### 2.4 Reproducibilidad, tratada como requisito y no como virtud

La pregunta del track pide una solución reproducible con esa palabra, así que
conviene usar un marco publicado y no una lista improvisada. Sandve et al.
(2013), *PLoS Computational Biology* 9(10):e1003285, dan diez reglas que se
mapean una a una sobre decisiones concretas de este proyecto `[E]`:

| Regla | Qué exige | Cómo se cumple acá |
| --- | --- | --- |
| 1. Registrar cómo se produjo cada resultado | trazar de dato crudo a resultado | Snakemake registra la cadena completa |
| 2. Evitar pasos manuales | nada de editar archivos a mano | las fichas de candidatos son JSON validado contra esquema |
| 3. Archivar las versiones exactas de los programas externos | | `environment.yml` con versiones fijas desde Bioconda |
| 4. Versionar todo script propio | | git, con el commit citado en cada ficha |
| 5. Guardar resultados intermedios en formatos estándar | | los FASTA, SAM y TSV de la sección 1.3 |
| 6. Anotar las semillas de lo aleatorio | | hoy no hay aleatoriedad en el pipeline; la semilla se fija igual y se declara |
| 7. Guardar los datos crudos detrás de cada figura | | el TSV que alimenta cada gráfico se entrega junto al gráfico |
| 8. Generar salida jerárquica | del resumen al detalle | el total, después el puntaje por criterio, después los conteos de hits |
| 9. Conectar cada afirmación con el resultado que la sostiene | | los marcadores `[E]`/`[R]`/`[H]`/`[?]` y la cita por criterio |
| 10. Dar acceso público a scripts, corridas y resultados | | repositorio público con DOI por Zenodo |

Las herramientas con las que se cumple están verificadas. **Snakemake** declara
el software requerido y lo despliega desde Conda-Forge y Bioconda, y genera
reportes portables que combinan resultados con parámetros, código y software
(Mölder et al. 2021, *F1000Research* 10:33) `[E]`. **Bioconda** es la fuente de
versiones fijas (Grüning et al. 2018, *Nature Methods* 15(7):475-476) `[E]`.
**DVC** versiona los datos por hash fuera de git, dejando en el repositorio un
archivo `.dvc` de metadatos `[E]`. El **DOI** sale del flujo documentado de
GitHub con Zenodo, que archiva y emite un DOI nuevo en cada publicación de
versión `[E]`. Y la capa de arriba es FAIR: identificador persistente (F1),
licencia de uso clara y accesible (R1.1), procedencia detallada (R1.2) y
estándares de la comunidad (R1.3) `[E]`.

Una aclaración honesta sobre nf-core y Nextflow: es la alternativa obvia a
Snakemake y no se pudo abrir ni el paper ni la documentación en ninguna de las
dos corridas, así que **no se recomienda ni se cita**, y queda en la sección 6.
La recomendación se sostiene con lo que sí se verificó.

---

## 3. Eje innovación abierta

Este eje es el que más fácilmente se llena de palabras, así que conviene fijar
una regla de admisión: acá sólo entra un antecedente si existe, si se puede
mirar y si se puede evaluar contra un criterio. "Ciencia abierta" como valor no
entra; un repositorio con licencia declarada, sí.

### 3.1 Qué significa concretamente en este problema

Cinco cosas, todas verificables y todas con un entregable asociado: publicar
datos con estándar y licencia; publicar el código con entorno y DOI; aportar al
monitoreo colaborativo del vector en vez de consumirlo; publicar lo que no
funcionó; y declarar las licencias de entrada que condicionan lo que se puede
hacer después con el resultado. Las cinco se juntan en el **paquete de apertura**
de la sección 3.8, que es el entregable de esta rama.

### 3.2 Monitoreo colaborativo del vector: tres antecedentes y lo que enseña cada uno

El primero es argentino, es el más cercano al problema y es el que deja el hueco
más claro. La **Red Nacional de Monitoreo de *Dalbulus maidis*** publicó su
séptimo informe, correspondiente al período del 22 de octubre al 8 de noviembre
de 2024, con capturas de adultos por localidad y por quincena obtenidas con
trampas cromáticas adhesivas en **426 localidades de Argentina** —74 en el NOA,
77 en el NEA, 35 en el Litoral, 77 en el Centro Norte y 163 en el Centro Sur—
más 17 localidades de Uruguay, operada por una coalición que el propio documento
declara: AAPPCE, Aapresid, CASAFE, CONICET, CREA, EEAOC, INTA, MAIZAR y SENASA,
con el porcentaje de infección por *Corn Stunt Spiroplasma* determinado por el
Centro de Bioinvestigaciones UNNOBA-CICBA (CONICET) `[R]`, verificado en la
primera corrida. El hueco es el formato: **el dato se publica en PDF, sin API,
sin CSV y sin licencia declarada**, y el propio informe advierte que los valores
están sujetos a modificación hasta auditar las trampas. Es un esfuerzo nacional
coordinado y multiinstitucional cuyo producto no es reutilizable por una
máquina. Dicho de otro modo: existe el dato y no existe el dataset.

El segundo es brasileño y muestra la misma asimetría desde otro ángulo.
**Monitora Oeste**, descrito en el Comunicado Técnico 48 de Embrapa Territorial
de septiembre de 2025, es una web y una aplicación de monitoreo fitosanitario en
el Oeste de Bahía, con trampas de feromona para *Anthonomus grandis*, datos en
tiempo real y alertas; el documento declara que el acceso a la herramienta es
gratuito y que es fruto de una asociación entre Embrapa Territorial y la
Associação Baiana de Produtores de Algodão `[R]`, verificado en la primera
corrida. Los datos de trampa los cargan los técnicos de la asociación: el acceso
a la visualización es abierto y **el dato crudo queda del lado privado**. Es el
modelo de colaboración público-privada funcionando, con la apertura detenida en
la capa de presentación.

El tercero no es de agro pero es el que resuelve lo que a los dos anteriores les
falta, y por eso vale citarlo. **Mosquito Alert** es un sistema de ciencia
ciudadana para vigilancia de mosquitos vectores operativo desde 2014; su
conjunto de datos de 2014 a 2020 se publicó como artículo de datos
(*Gigabyte*, 2022, doi 10.46471/gigabyte.54, CC BY) y, sobre todo, **como
conjunto de datos en GBIF** `[E]`. El diseño tiene cuatro piezas que son
directamente trasladables a un monitoreo de chicharrita: los registros van
ligados a fotografías enviadas por los participantes y **validadas por
entomólogos**, lo que resuelve la calidad del dato sin cerrar la participación;
hay un módulo para enviar muestras físicas a laboratorios de referencia cuando
hace falta identificación especializada; la aplicación recoge información
anónima sobre la distribución geográfica de los participantes **para corregir el
sesgo de esfuerzo de muestreo**, que es el defecto clásico de la ciencia
ciudadana; y las imágenes validadas por expertos ya se usaron para entrenar un
modelo de aprendizaje profundo que preselecciona casos `[E]`. Ese último punto
es exactamente el tipo de aporte que un equipo de IA puede hacer a una red de
monitoreo: no reemplazar al validador, sino preseleccionarle el trabajo.

Como cuarto punto de apoyo, para que no quede duda de que el diseño distribuido
escala en agricultura: van Etten et al. (2019), *PNAS* 116(10):4194-4199,
generaron un conjunto de datos de **12.409 parcelas experimentales manejadas por
agricultores** en Nicaragua (poroto común), Etiopía (trigo candeal) e India
(trigo pan) con el enfoque *tricot* —comparación triádica de tecnologías—, en el
que cada participante recibe tres variedades asignadas al azar de un conjunto
mayor y ordena su desempeño, y las observaciones se compilan y analizan
centralmente `[E]`. La lección metodológica es la del diseño de la tarea: se
escala porque lo que se le pide a cada participante es mínimo y comparativo, no
una medición absoluta.

De los cuatro sale una propuesta concreta y evaluable para el equipo, marcada
`[H]` porque es nuestra: publicar como conjunto de datos en formato Darwin Core,
con licencia CC BY y DOI por Zenodo, la consolidación de lo que hoy está
disperso —los 610 registros de GBIF, las 151 observaciones de iNaturalist y, si
se consigue permiso, la serie de la Red Nacional transcrita de los PDF—, con el
esquema declarado y el procedimiento de transcripción versionado. Para
dimensionar la brecha que eso cerraría: hoy GBIF tiene **17 registros de
*D. maidis* en Argentina** `[E]`, en el país del brote y con una red nacional de
426 localidades funcionando.

### 3.3 Datos y código abiertos, y las licencias que ya nos condicionan

La parte menos glamorosa de este eje es la que más decisiones cambia. Tres
licencias verificadas afectan directamente lo que el equipo puede entregar.

El **ensamblado del genoma de *D. maidis* del INTA**, publicado en el repositorio
institucional como ítem de tipo conjunto de datos —"Genoma de *Dalbulus maidis*,
la chicharrita del maíz, versión actualizable v0.1", IPAVE-CIAP-INTA, 4 de junio
de 2024, descargable en FASTA con dos documentos de métricas— está bajo **CC
BY-NC-SA**, es decir, no comercial `[R]`, verificado en la primera corrida, con
una ambigüedad de versión que quedó anotada (`[?]`: el pie del sitio dice 2.5
Unported y los metadatos del ítem enlazan 4.0). La cláusula no comercial es un
límite real: cualquier resultado derivado de ese insumo arrastra la restricción
si después se pretende licenciar a una empresa. El preprint del borrador está
bajo CC BY-NC-ND 4.0 `[R]`. Y entre los insumos de modelado, los pesos de
Nucleotide Transformer son CC BY-NC-SA 4.0, también no comercial `[R]` (dato de
R4). La consecuencia operativa es la que está en el criterio C6 de la rúbrica:
un candidato derivado de un insumo con cláusula no comercial no puede puntuar 4,
y eso se declara en vez de descubrirse después.

Del lado de lo que sí habilita: **REDAPE**, el repositorio de datos de
investigación de Embrapa, declara acceso público y gratuito y no fija una
licencia única —cada conjunto declara sus condiciones—, y no se encontró en él
ningún conjunto de datos de plagas de maíz `[R]`, verificado en la primera
corrida. Ese vacío es, otra vez, una oportunidad documentada más que una queja.

### 3.4 Estándares e interoperabilidad

Un dato abierto sin estándar es un archivo que hay que interpretar a mano.
**Darwin Core** es el estándar de la comunidad de biodiversidad para publicar e
integrar registros de ocurrencia; su paper de referencia (Wieczorek et al. 2012,
*PLoS ONE* 7(1):e29715) describe las categorías de términos, la diferencia entre
el Darwin Core simple y el relacional, las extensiones a nuevas comunidades
—metagenómica y recursos genéticos entre ellas— y el proceso comunitario de
mantenimiento del estándar, y consigna que ya en ese momento GBIF indexaba del
orden de 300 millones de registros en formato Darwin Core publicados por más de
340 organizaciones de 43 países `[E]`. El sitio del estándar, mantenido por el
Darwin Core Maintenance Group bajo TDWG, tiene su contenido bajo CC BY 4.0
`[R]`, verificado en la primera corrida. Para la parte vegetal existe
**MIAPPE**, con especificación y lista de verificación públicas `[R]`, y para
secuencias el marco es **INSDC**, la colaboración de DDBJ, ENA y NCBI `[R]`,
ambos verificados en la primera corrida.

La decisión concreta del equipo, `[H]`: los dos artefactos de salida llevan
esquema declarado y versionado —`esquema_candidato.json` y `esquema_score.json`
de `PLAN_EQUIPO.md`— y el conjunto de ocurrencias, si se publica, va en Darwin
Core. No se inventa un formato propio para nada que ya tenga estándar.

### 3.5 Publicar lo que no funcionó

Es la pieza del eje que casi nadie entrega y la que este proyecto ya tiene a
medio construir, porque `00_meta/CAMINOS_PROBADOS.md` es exactamente eso: el
registro de lo que se intentó, lo que se descartó y qué lo reabriría. Hay
precedente editorial para el argumento: *Life Science Alliance* declara
explícitamente que acepta trabajos que describan resultados negativos, y su
editorial de 2026 sostiene que el sesgo sistémico contra los resultados
negativos deja persistir en el registro científico callejones sin salida,
reactivos defectuosos e hipótesis erróneas, consumiendo recursos más tiempo del
que deberían `[E]`. Para nuestro caso la aplicación es directa y barata: el
descarte documentado de una línea —por ejemplo, que la accesibilidad del sitio
blanco no resultó predictor significativo de eficacia insecticida y por lo tanto
entra con peso cero— vale tanto como un hallazgo y se publica junto con el
resto. Un revisor puede discutirlo; eso es la idea.

### 3.6 Colaboración público-privada: qué instrumentos existen de verdad

**INTA** publica sus instrumentos de vinculación tecnológica: convenios con
empresas, licencia de tecnologías, asistencia técnica a terceros, Empresas de
Base Tecnológica con INCUINTA como plataforma de biotecnología y los
Facilitadores de Flujo de Proyectos junto a INIS BIOTECH SA autorizados por la
ANPCyT, Nodos de Innovación, clusters y parques, y gestión de propiedad
intelectual, con base pública de convenios en `sigec.inta.gov.ar` y una vía de
entrada para terceros llamada "Banco de ideas" `[R]`, verificado en la primera
corrida. Para un equipo sin laboratorio, "asistencia técnica a terceros" y
"Banco de ideas" son las dos puertas con nombre propio, y esa concreción es lo
que convierte el criterio C5 de la rúbrica en algo puntuable en lugar de una
estimación.

Del lado del CONICET, una nota institucional del 5 de noviembre de 2024 sobre
articulación público-privada en biotecnología agrícola informa que Apolo Biotech
es una Empresa de Base Tecnológica fundada por Federico Ariel (IFIBYNE,
CONICET-UBA) que desarrolla tecnologías basadas en ARN para control de plagas,
con la primera planta de producción de ARN de América Latina en Santa Fe y 30
empleados `[R]`, verificado en la primera corrida. Dos salvedades que hay que
decir al usarlo: **la nota no vincula a esa empresa con la chicharrita ni
menciona RNAi**, y el organizador del Investigathón es el EPILAB · IFIBYNE, el
mismo instituto de origen del fundador, de modo que la relación entre ambos es
una pregunta abierta y no un hecho.

En septiembre de 2024 hubo además un **taller para la construcción de la
gobernanza de la información de la chicharrita**, convocado por la Secretaría de
Agricultura con el IICA, cuyo informe existe en el sitio oficial pero cuyo
cuerpo no resultó extraíble por la codificación de sus fuentes tipográficas; lo
que se pudo verificar es la portada y, por prensa especializada, la lista de
participantes —INTA, SENASA, INASE, la Comisión Federal Fitosanitaria, Maizar,
ASA, FADIA, CREA, APRONOR, Aapresid, CASAFE, CIAFA, AAPPCE, SRA, Coninagro y
CRA— y que el objetivo era fortalecer el intercambio de datos para la campaña
2024/25, sin compromisos concretos, sin mención de dato abierto ni de plataforma
compartida `[R]` / `[?]`, verificado parcialmente en la primera corrida. Es,
tal como está documentado, la mejor evidencia disponible de que la gobernanza de
estos datos está declarada como problema y no resuelta como infraestructura.

Por último, el contexto internacional de esta discusión está bien sintetizado en
una perspectiva reciente: la transición del RNAi de la investigación a la
comercialización trae de la mano incertidumbre regulatoria, costos altos de
producción de dsRNA y datos comparativos de eficacia a campo escasos, y los
autores sostienen que desarrollar estas tecnologías dentro de marcos de
investigación pública o liberarlas sin patentes restrictivas reduciría el riesgo
de dependencias de explotación en la cadena de suministro (*Pest Management
Science*, 2026, doi 10.1002/ps.70806) `[R]`. En la misma perspectiva se consigna
que el costo de producción del dsRNA puede bajar de forma marcada: para
ledprona, un dsRNA de 490 pb producido con una plataforma propietaria libre de
células, se reportan costos proyectados por debajo de 1 dólar por unidad de
dsRNA en la etapa de síntesis `[R]`.

### 3.7 El antecedente más cercano: una especie nombrada por consenso de comunidad

Si hay que mostrarle a un jurado un caso de innovación abierta que funcionó en
este patosistema exacto, es el de la sección 1.1. La propuesta de '*Candidatus*
Phytoplasma zeae' está firmada por una coalición de grupos de Brasil, Colombia,
México, Estados Unidos y Canadá —entre ellos EPAGRI de Santa Catarina, la
Alianza Bioversity-CIAT, universidades estatales de Oklahoma, Iowa y Missouri, la
Universidad Veracruzana, la Universidad de los Andes y Agriculture and Agri-Food
Canada— que estudiaron el patógeno por más de una década, y los autores declaran
explícitamente que la designación se propone por consenso de esa comunidad bajo
la Regla c de las guías del IRPCM `[E]`. El trabajo depositó los genomas en
GenBank bajo el BioProject `PRJNA1294367` con las muestras `SAMN50092827`,
`SAMN50092828` y `SAMN50092829`, la secuencia 16S de la cepa de referencia como
`PZ340875`, y **depositó además los ejemplares de *D. maidis* como vouchers en
la Colección Nacional Canadiense de Insectos, Arácnidos y Nematodos**, con
números de voucher y curador nombrado `[E]`. Eso último es la diferencia entre
"compartimos datos" y "otro laboratorio puede ir a ver el bicho": es
reproducibilidad material, no declarativa.

Dos cosas para el equipo. La primera, operativa: hoy, consultada la API de NCBI,
el BioProject `PRJNA1294367` **no devuelve ensamblados registrados en la base
`assembly`** `[?]`, de modo que los tres genomas nuevos hay que buscarlos por
BioSample y no dar por sentado que están empaquetados como ensamblado; el que sí
está completo y anotado es el M3 de 2016. La segunda, de contenido, y es una
contradicción que conviene llevar anotada: el mismo trabajo afirma que
*D. maidis* se distribuye hasta Argentina "although the disease has not yet been
reported there" `[?]`, lo que no se concilia obviamente con la epifitia
argentina de 2023/2024 ni con que la Red Nacional reporte porcentaje de
infección por espiroplasma. Puede ser una distinción entre el fitoplasma y el
espiroplasma del complejo —son dos patógenos distintos y el achaparramiento
arbustivo no es el achaparramiento del espiroplasma— o puede ser un error. Es
una pregunta corta y de alto valor para el investigador invitado.

### 3.8 El paquete de apertura: el entregable de esta rama

Seis piezas, todas producibles sin laboratorio y evaluables por un tercero:
licencia de salida declarada para código (permisiva) y para datos (CC BY), con
la justificación escrita; declaración de licencias de entrada, incluida la
cláusula no comercial del ensamblado del INTA y la de los pesos de modelos;
repositorio público con `environment.yml`, commit fijado y DOI por Zenodo;
esquemas de entrada y salida versionados, y Darwin Core para ocurrencias;
registro de resultados negativos y de caminos descartados; y el aporte de datos
concreto —la consolidación de ocurrencias y, si el investigador lo autoriza, la
transcripción estructurada de la serie de la Red Nacional—. Lo que **no** incluye,
y conviene decirlo antes de que lo pregunten: no incluye publicar secuencias de
disparadores optimizados contra blancos de patógenos sin revisión del alcance
ético del repositorio, que es la regla permanente de `CLAUDE.md`.

---

## 4. Cómo se evalúa una solución de este tipo

La rúbrica completa, con las ocho anclas textuales por criterio, las compuertas,
la fórmula, los topes, el tratamiento de la incertidumbre y el ejemplo trabajado
sobre cinco candidatos, está en `RUBRICA.md`, que es un entregable en sí mismo.
Acá va sólo el argumento de por qué está construida así.

El propósito lo fija el organizador. Su pregunta abierta es, textual, "¿cuáles
merecen validación y por qué?" sobre candidatos preliminares que su equipo ya
tiene diseñados `[R]`. Eso es un problema de priorización con criterio
explicitable, y es la parte del desafío que un equipo sin laboratorio puede
resolver completa.

Las decisiones de diseño que no son obvias son cinco. **Primera: hay compuertas
antes de los puntajes.** El alcance ético, la existencia de la secuencia, un
umbral mínimo de especificidad y la trazabilidad del cálculo no se ponderan: se
cumplen o el candidato no entra al orden. Convertir la reproducibilidad en
condición de admisión y no en criterio ponderado es lo que impide que un
candidato irreproducible compense con buen diseño. **Segunda: hay topes.** Un
promedio ponderado puro deja que un diseño de secuencia excelente tape la
ausencia de vía de entrega, que es precisamente el error que esta rúbrica existe
para evitar; por eso cualquier criterio en cero topea el total en 40 y el
candidato se reporta como no priorizable sin rediseño. **Tercera: cada candidato
tiene dos puntajes y no uno**, uno conservador y uno optimista según cómo se
resuelvan los criterios marcados como producibles pero todavía no producidos; la
distancia entre ambos dice qué medición hay que hacer antes de decidir.
**Cuarta: los pesos se declaran antes de ver los candidatos** y cualquier cambio
posterior se reporta junto con su efecto sobre el orden. **Quinta: el análisis de
sensibilidad es obligatorio**, y su salida más valiosa no es el orden sino cuál
es la medición de menor costo que más lo cambia.

El ejemplo trabajado de la sección 7 de `RUBRICA.md` muestra que eso produce una
decisión y no un ranking. Con los pesos declarados, los dos candidatos de cabeza
quedan separados por 1,3 puntos sobre 100 y sus rangos de incertidumbre se
superponen casi por completo: el orden entre ellos **no está determinado** con la
evidencia de hoy. Con el esquema de pesos alternativo —el que lee literalmente
la declaración del organizador de que la barrera es la entrega— el orden de los
dos primeros se invierte, y se invierte tanto con los puntajes conservadores
como con los de la tabla. Y el candidato con el mejor fenotipo publicado en la
especie es el que peor prioriza, porque toda su evidencia es por microinyección,
que no es una vía de aplicación agronómica. Esa es la clase de resultado que la
rúbrica existe para hacer visible.

Dos cosas cambiaron en la rúbrica durante esta corrida, y están explicadas
dentro del propio archivo. Se incorporó el criterio de off-target de la guía de
la EFSA de 2025 —aprobada el 7 de marzo de 2025, doi 10.2903/j.efsa.2025.9321—,
que exige reportar todo transcripto off-target que cumpla un conjunto de siete
condiciones sobre mismatches, huecos, posiciones y cociente de energía libre
para cada ARN pequeño de 21 nt derivable, y que es **más permisivo en
complementariedad y por lo tanto más exigente en resultado** que el umbral de 19
nucleótidos que usan las herramientas de insectos `[E]`; la EFSA publica además
el script para correrlo y recomienda que el análisis se base en cuántos ARN
pequeños distintos coinciden con el mismo transcripto `[E]`. Hay que decir al
citarla que su alcance son plantas modificadas genéticamente, no dsRNA
pulverizado, y que declara explícitamente no cubrir la evaluación de riesgo
ambiental `[E]`. Y se corrigió un error aritmético de la versión 1.0: dos
totales de la fila conservadora del ejemplo estaban calculados con el supuesto
equivocado, el arreglo cambia el orden de los dos últimos candidatos, y queda
escrito en el archivo porque es justamente la falla que la compuerta de
trazabilidad existe para atrapar.

---

## 5. Plan para cuatro personas

El plan completo —roles, ramas, grafo de dependencias, cronograma por semanas
relativas, qué se entrega y qué se presenta, plan B en cinco niveles y orden de
recorte si el plazo se acorta— está en `PLAN_EQUIPO.md`. Acá va la lógica.

El riesgo real de un equipo de cuatro con poco tiempo no es la falta de
capacidad: es que tres esperen a uno. Eso se resuelve con una decisión concreta
y verificable, no con una metodología: **el primer entregable del equipo, en las
primeras cuatro horas, son los dos esquemas de datos y sus casos de prueba.**
Con el esquema de la ficha de candidato, el de la ficha de puntaje y cinco
candidatos de juguete que los cumplan, cada rama puede avanzar contra datos
falsos mientras llegan los reales: la herramienta se construye y se testea sin
esperar el tamizaje, el tamizaje se desarrolla sin esperar la rúbrica poblada, y
la rúbrica se puebla a mano sin esperar la herramienta. Es la única dependencia
dura del plan y se paga el primer día.

El reparto queda entonces en cuatro ramas con entregable propio: datos y
genómica produce el paquete de datos congelado; diseño y tamizaje produce el
informe de especificidad por candidato, que es la evidencia más decisiva;
herramienta y reproducibilidad produce el artefacto de decisión con sus tests y
su entorno; y rúbrica aplicada, riesgo y apertura produce el dossier de
evidencia y el paquete de la sección 3.8. La única dependencia cruzada temprana
—que el tamizaje necesita la lista de taxones no objetivo— se entrega el día uno,
antes que cualquier otra cosa.

El hito que hay que proteger es el de la segunda sincronización: la primera
corrida punta a punta sobre los cinco candidatos propios. A partir de ahí el
equipo tiene un entregable completo aunque no pase nada más, y lo que ocurre el
día del evento es una **sustitución de entrada**, no una construcción: se
reemplazan nuestros candidatos por los del EPILAB y se vuelve a correr.

Sobre el plan B hay que decir algo incómodo y decirlo primero: el escenario de
fracaso más probable —que no existan los datos para entrenar nada— **ya es
verdad hoy**, y el plan está construido para que no importe. No hay un conjunto
de pares secuencia-eficacia en *D. maidis*; lo más cercano son 31 siRNA probados
en *T. castaneum*, de los cuales 29 entraron a un modelo de riesgos
proporcionales con una C de Harrell de 0,76 `[E]`, que es un coleóptero, con n
de dos dígitos y un modelo de supervivencia. La conclusión no es que falte un
dato: es que **el equipo no va a entrenar nada, y eso es una decisión**. Lo que
el track pide es una solución biológicamente informada y reproducible que
priorice, y priorizar con criterio explícito y evidencia citada no requiere
entrenamiento; la rúbrica y el tamizaje son cómputo determinista sobre
secuencias públicas, y por eso son reproducibles bit a bit.

---

## 6. Lo que quedó sin resolver

Cuatro cosas, para que no se busquen dos veces.

**Fuentes que no se pudieron abrir.** El paper del marco nf-core y Nextflow
(*Nature Biotechnology*, 2020) no tiene ubicación de acceso abierto accesible
desde este entorno y no se abrió en ninguna de las dos corridas: por la regla
del proyecto no se cita y la recomendación de reproducibilidad se sostiene con
Snakemake y Bioconda. La versión revisada por pares de dsRNAEngineer, en *Trends
in Biotechnology*, figura en el índice de búsqueda pero no se abrió: lo que se
cita es el preprint. Los PDF de los trabajos de 2022 y 2023 del grupo de
Catalano siguen siendo de suscripción y lo que se tiene de ellos son los
registros bibliográficos y los resúmenes.

**Dominios no accesibles en esta corrida.** `argentina.gob.ar`, `embrapa.br`,
`repositorio.inta.gob.ar` y `api.gbif.org` no estaban en la lista de dominios
permitidos del entorno de la segunda corrida. Todo lo que este reporte afirma
sobre la Red Nacional de Monitoreo, el taller de gobernanza, Monitora Oeste,
REDAPE, el repositorio del INTA, la vinculación tecnológica del INTA, la nota
del CONICET, GBIF e iNaturalist viene de la verificación de la primera corrida,
transcrita en `notes/evidencia_verificada.md`, y **no se volvió a comprobar
hoy**. Nada de eso se reconstruyó de memoria: o estaba verificado con cita
textual, o no entró.

**Un portal que no se abrió y por eso no se cita.** Los programas de innovación
abierta de Embrapa aparecen en resultados de búsqueda, pero sus páginas no se
abrieron en esta corrida y no se citan como antecedente. Lo que sí está
verificado del lado brasileño es Monitora Oeste y REDAPE.

**Contradicciones abiertas.** Que el trabajo de delineación de '*Ca.* P. zeae'
afirme que la enfermedad no fue reportada en Argentina `[?]`; que el BioProject
de sus tres genomas nuevos no devuelva ensamblados registrados `[?]`; y la
ambigüedad de versión de la licencia del ensamblado del INTA `[?]`. Las tres
están descritas donde corresponde y las tres son preguntas cortas para el
investigador invitado o para el día en que haya acceso.
