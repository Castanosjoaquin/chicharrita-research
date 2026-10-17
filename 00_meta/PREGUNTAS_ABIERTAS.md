# Preguntas abiertas

Lo que no sabemos, lo que hay que preguntarle al investigador y lo que depende de
datos que todavía no tenemos. Tres secciones: preguntas para el investigador,
pedidos concretos de datos y herramientas para el día en que nos den acceso, y
pendientes internos nuestros, incluidas las fuentes que no pudimos abrir.

Las preguntas que vienen de una investigación llevan la marca de cuál.

---

## Para el investigador invitado

Se consolidan acá a medida que vuelven las cinco investigaciones, ordenadas por
cuánto cambia la respuesta nuestro plan de trabajo. El criterio para que una
pregunta entre: que no se pueda contestar con bibliografía pública, y que la
respuesta cambie una decisión nuestra. Una pregunta cuya respuesta no mueve nada
no se hace: el tiempo con el investigador es el recurso más escaso del evento.

Abiertas desde antes de las investigaciones:

1. Cuáles son exactamente los cuatro patógenos que mencionó, y si el cuarto
   agente del complejo está confirmado o es materia de discusión. *(origen: notas
   del equipo, supuesto S1)*
2. En su pipeline de selección de candidatos, qué consume como entrada y qué
   produce como salida cada etapa: concretamente, qué formato tiene lo que
   recibe de bioinformática y qué decisión toma con eso. *(sin esto, cualquier
   herramienta que propongamos no se enchufa a nada)*
3. Si el cuello de botella real de su proceso es computacional, experimental o
   regulatorio. Es la pregunta que decide si nuestra propuesta le sirve a alguien
   o es un ejercicio.

---

## Pedidos para el día en que nos den acceso a herramientas y datos

Se consolidan acá, con la justificación de para qué sirve cada uno. Un pedido sin
uso previsto no entra.

---

## Pendientes internos

### Fuentes que no se pudieron abrir
Toda fuente que una investigación necesitó y no pudo abrir —muro de pago, enlace
caído, documento no accesible— se anota acá con lo que se buscaba en ella, para
no volver a intentarlo a ciegas y para poder pedirla el día del evento.

### Rechazos de herramientas
Según `CLAUDE.md`, si una herramienta o una búsqueda devuelve un rechazo, se
registra acá y se sigue por otra línea, sin reformular para esquivarlo.

### Conflictos de definición en el glosario
Los términos donde dos investigaciones dieron definiciones incompatibles quedan
marcados `[?]` en `GLOSARIO.md` y anotados acá con las dos versiones y quién las
dio.

## Pendientes de R5 (metodologías y ejes) — 2026-10-16

- **Rechazo de herramienta registrado.** La búsqueda web `dsRNA leafhopper Euscelidius variegatus Scaphoideus titanus RNAi phytoplasma vector feeding delivery silencing efficacy` devolvió un rechazo de la API de búsqueda (clasificada como `[bio]`). Siguiendo la regla de CLAUDE.md no se reformuló. Queda pendiente: evidencia primaria de eficacia de RNAi oral en Cicadellidae vectores de fitoplasmas (*Euscelidius variegatus*, *Scaphoideus titanus*). Vía alternativa sugerida: la lista de referencias de Zielińska (2026) *J. Plant Prot. Res.* 66(3):303–317, que las cita, y pedirle los PDFs al investigador invitado.
- **VectorBase**: la lista de organismos no se pudo verificar directamente (la aplicación es JavaScript y la URL `www.vectorbase.org/organisms` devolvió HTTP 421). Un paper de actualización de VectorBase de 2022 no incluye Cicadellidae en su listado de taxones. Queda pendiente confirmar en el día del evento si VectorBase sirve algún Cicadellidae.
- **MaizeGDB**: `https://www.maizegdb.org/` devolvió HTTP 403 a nuestro cliente. La URL queda marcada como NO VERIFICADA en `research/R5_metodologias_ejes/stack_bioinformatico.md`.
- **Accesiones del borrador de genoma de *Dalbulus maidis*** (bioRxiv 10.1101/2024.06.25.600652): confirmar BioProject/BioSample/WGS en la sección de disponibilidad de datos del preprint.

## R4 — pendientes de verificación (2026-10-16)
- **Rechazo de herramienta registrado.** Al intentar abrir con WebFetch
  `https://pubmed.ncbi.nlm.nih.gov/37945254/` (Knockdown of double-stranded
  RNases enhances oral RNAi in the corn leafhopper, *Dalbulus maidis*), el
  submodelo de lectura devolvió un rechazo de política (`[bio]`). No se
  reformuló la consulta. Queda pendiente abrir ese trabajo por otra vía
  (ScienceDirect, PDF institucional o la biblioteca de la facultad) para fijar
  porcentajes de knockdown, concentraciones y mortalidad. Hasta entonces la
  afirmación "el knockdown de dsRNasas mejora el RNAi oral en *D. maidis*" queda
  como `[R]` apoyada solo en el índice de PubMed, no en el texto completo.
- Falta verificar en texto completo el RNAi experimental publicado en
  *D. maidis* (preprint bioRxiv 2022.01.17.476645 y el artículo de Frontiers in
  Insect Science 2026, 10.3389/finsc.2026.1811933). Es el dato retrospectivo que
  permitiría validar un modelo de eficacia sin laboratorio.
- RNA-FM: el repositorio oficial afirma que el modelo se publicó en Nature
  Methods, pero el enlace apunta al artículo de RhoFold. Queda `[?]` si RNA-FM
  tiene versión revisada por pares propia o sigue siendo preprint (arXiv
  2204.00300).
- Licencia de los pesos de Nucleotide Transformer y de RiNALMo: no aparece en el
  artículo; hay que leerla en las tarjetas de modelo de Hugging Face.
- **Segundo rechazo de herramienta registrado (R5).** `WebFetch` sobre el texto completo del preprint bioRxiv 10.1101/2022.01.17.476645 (métodos de RNAi en *Dalbulus maidis*) devolvió un rechazo clasificado `[bio]`. No se reformuló. Vía alternativa usada: la versión revisada por pares, Dalaisón-Fuentes et al. (2022) *Pest Management Science*, DOI 10.1002/ps.6937, y los metadatos de Europe PMC. Pendiente: conseguir el PDF de esa versión (es de suscripción) para extraer dosis, vía de entrega, porcentaje de knockdown y n.

## Desde R2 (attention y diseño de ARN), 2026-10-16

### Rechazo de herramienta registrado
Una búsqueda web con el texto `RNAi Dalbulus maidis leafhopper dsRNA knockdown Hemiptera
efficacy` fue rechazada por la herramienta con el detalle `[bio]`. Según la regla del
proyecto no se reformuló para esquivar el rechazo. La misma pregunta se respondió por otra
línea legítima y distinta —búsqueda bibliográfica en PubMed vía E-utilities— que devolvió
los cuatro registros de RNAi en *Dalbulus* y permitió traer los abstracts completos. La
información no se perdió.

### Para preguntarle al investigador del EPILAB
1. **Los candidatos preliminares.** ¿Cuántos son, en qué formato, y con qué metadatos?
   Mínimo necesario para poder priorizarlos: secuencia, transcripto blanco, organismo
   (vector o patógeno), y vía de entrega prevista. Sin esto no hay nada que ordenar.
2. **¿Contra qué organismo apunta cada candidato?** El esquema oficial termina en
   "inhibición del crecimiento del patógeno", y si un mollicute sin pared responde a RNAi es
   justo lo que R1 tiene que resolver. ¿Los candidatos apuntan al vector, al patógeno, o a
   preparar la defensa de la planta?
3. **¿En qué escalón de su propia escalera de precisión están los candidatos?** ARNdc largo
   canónico, ARNdc ingenierizado, plataforma de precisión, o siRNA de 24 nt con RdDM. Nuestro
   método sólo está calibrado para los dos primeros.
4. **¿Hay datos propios de eficacia, aunque sean preliminares o negativos?** Es el insumo
   que no existe públicamente y que cambiaría el alcance de lo que se puede validar.
5. **¿Contemplan la co-entrega de ARNdc contra *Dmai-dsRNase-2*** como estrategia frente a
   la barrera de las RNasas que ellos mismos declaran?
6. **El transcriptoma de Xu et al. 2021**, con 56.116 transcriptos, no aparece depositado en
   NCBI y no hay registro TSA para la especie. ¿Lo tienen, o saben dónde está? Nos ahorraría
   la tarea del camino crítico.

### Dependen de datos que no tenemos
7. **MSMV sin identificar.** La diapositiva del organizador nombra cuatro patógenos, y MSMV
   es el único que no pudimos resolver taxonómicamente. La búsqueda devolvió los taxid
   3052767 y 2025388 sin confirmar cuál corresponde. Pendiente para R1.
8. **Cuál de los tres genomas de *Candidatus* Phytoplasma asteris** corresponde al
   achaparramiento del maíz, si alguno. No se verificó.
9. **Conservación poblacional de *D. maidis*.** No existen datos poblacionales públicos
   suficientes: seis corridas de WGS en MiSeq de profundidad y origen no verificados. El
   término de conservación del scoring queda como `[H]`, calculable pero no interpretable
   como conservación poblacional.
10. **Panel de organismos no objetivo del maíz argentino.** No existe curado en ninguna
    parte: hay que armarlo (polinizadores, enemigos naturales, fauna del suelo).

### Licencias a verificar antes de reusar
11. **iBeetle-Base**: no se halló declaración de licencia ni formato de descarga masiva.
12. **Depósitos de figshare de dsRIP** (10.6084/m9.figshare.28156787 y 27490890.v1): licencia
    sin verificar. La web de dsRIP dice "All rights reserved" en el pie.
13. **Nucleotide Transformer** es CC-BY-NC-SA-4.0, **no comercial**. Relevante si el proyecto
    deriva en algo con fin comercial.

---

# Integración del 2026-10-17

Esta sección reordena el archivo después de integrar las cinco investigaciones:
qué quedó cerrado con fuente, qué sigue abierto, y la lista consolidada de
preguntas para el investigador, deduplicada y ordenada por cuánto cambia nuestro
plan.

## Cerradas con fuente

- **Supuesto S1, asignación de síntomas.** La idea de que un patógeno afecta los
  granos por mazorca y el otro el crecimiento del tallo **no se sostiene**. Con
  fitoplasma y *Spiroplasma kunkelii* inoculados por separado y juntos en cinco
  cultivares, en macetas hasta cosecha y con PCR a 30, 60 y 100 días: la
  reducción de producción de grano fue significativamente distinta (P < 0,01) y
  **mayor con el espiroplasma**, mientras que la reducción de altura **no** fue
  significativamente diferente entre fitoplasma, espiroplasma o ambos, y la
  inoculación simultánea no dio sinergismo. Fuente en `R1/sources.json` S13.
- **Supuesto S2, BLAST y termodinámica.** Falso que BLAST calcule termodinámica.
  Su artículo primario describe semilla y extensión, matrices de sustitución y
  E-value, y no menciona energía libre ni estructura secundaria. La termodinámica
  la calcula ViennaRNA; Bowtie tampoco calcula energía. La operación de «dividir
  en porciones» existe, pero la hace el diseñador. Verificado por separado y con
  el mismo resultado por R1 y por R2, que es la redundancia que D3 buscaba.
- **¿Hay RNAi funcional en mollicutes?** No, con la evidencia que pudimos
  producir: cero proteínas con dominio PIWI, cero con PAZ y cero con dimerización
  de Dicer en Mollicutes (126.874 proteínas anotadas), *Spiroplasma* (36.551),
  *S. kunkelii* (1.755) y '*Candidatus* Phytoplasma' (24.307), con control
  positivo de RNasa III en todos los taxones y juego completo de dominios en
  *Zea mays* y en Hemiptera. Consulta propia a UniProtKB/InterPro, documentada y
  reproducible en `R1/REPORT.md` como D01. **Limitación declarada:** es una
  consulta de anotación, no una búsqueda por perfil HMM ni un tblastn contra los
  genomas, de modo que no descarta genes no anotados o pseudogenizados. Queda
  como pendiente metodológico, abajo.
- **Cuál de los genomas de fitoplasma corresponde al complejo del maíz.**
  Ninguno de los de '*Ca.* Phytoplasma asteris': el agente es una especie
  distinta, '*Candidatus* Phytoplasma zeae', delineada en 2026, con genoma
  completo y anotado desde 2016 (`GCA_001712875.1` / `GCF_001712875.1`, cepa M3,
  576.118 pb, reanotado por RefSeq el 7 de junio de 2026). Cierra la pregunta 8
  de la sección de R2.
- **El transcriptoma de *D. maidis*.** Está depositado: 56.116 transcriptos en el
  TSA `GITV00000000`, con 82,4 % de completitud BUSCO. Cierra la pregunta 6 de la
  sección de R2 y elimina el «camino crítico» que R2 había declarado.
- **La guía formal de la EFSA.** Abierta y leída; su criterio de off-target está
  incorporado a la compuerta G2 y al criterio C2 de la rúbrica, con sus dos
  límites de alcance declarados: es para plantas modificadas genéticamente y no
  cubre riesgo ambiental.
- **OligoFormer y PaperQA2**, que figuraban como pendientes de R4, se abrieron y
  están en `R4/sources.json` con sus números primarios.
- **Licencias de pesos de modelos.** Verificadas las permisivas: RiNALMo
  (Apache 2.0 más CC BY 4.0), Evo 2 (Apache 2.0), RNA-FM y gRNAde (MIT). Y las
  que no lo son: Nucleotide Transformer es CC BY-NC-SA, no comercial, y ERNIE-RNA
  es CC BY-NC-ND.

## Siguen abiertas

### Fuentes que no se pudieron abrir
- **Knockdown de dsRNasas en *Dalbulus maidis*** (PubMed 37945254). El intento
  original devolvió un rechazo de política de herramienta, registrado y **no
  reformulado**, según la regla de `CLAUDE.md`. Sigue sin abrirse. Es la pieza
  que conecta el cuello de botella de entrega con una decisión de diseño de
  secuencia, así que es el primer PDF para pedirle al investigador.
- **Estudio retrospectivo sobre siRecords** (PMC4381284), la evidencia *en
  contra* de la accesibilidad del sitio blanco. El punto sigue marcado `[?]` y se
  apoya en una cita de segunda mano más el resultado directo de dsRIP.
- **Pérdidas económicas del complejo en Brasil** (*Crop Protection* 2026,
  doi 10.1016/j.cropro.2026.107549): sin versión abierta por ninguna de las
  cuatro vías probadas. Sería la fuente primaria más directa sobre magnitud.
- **nf-core / Nextflow** (doi 10.1038/s41587-020-0439-x): sin ubicación abierta
  accesible. No se cita, y por eso la recomendación de reproducibilidad se apoya
  sólo en Snakemake y Bioconda.
- **Versión revisada por pares de dsRNAEngineer** (*Trends in Biotechnology*): se
  cita el preprint de bioRxiv, marcado `[R]`.
- **Texto completo del preprint de RNAi oral en *D. maidis***: tenemos el resumen,
  no las dosis, los tiempos ni los tamaños de muestra.

### Dominios que no estuvieron disponibles en la última corrida
`argentina.gob.ar`, `embrapa.br`, `repositorio.inta.gob.ar` y la API de GBIF. Las
afirmaciones de la sección de innovación abierta de R5 que dependen de ellos
—Red Nacional de Monitoreo, taller de gobernanza, Monitora Oeste, REDAPE,
repositorio y vinculación tecnológica del INTA, nota del CONICET, GBIF e
iNaturalist— conservan la verificación de la corrida anterior, con sus citas
textuales en `research/R5_metodologias_ejes/notes/evidencia_verificada.md`. No se
reformuló ni se buscaron espejos. Reverificarlas es trabajo de una tarde si se
habilita el acceso.

### Contradicciones sin resolver, marcadas `[?]`
- **'*Ca.* Phytoplasma zeae' y la Argentina.** El trabajo que da nombre al taxón
  dice que *D. maidis* llega hasta la Argentina «aunque la enfermedad todavía no
  se reportó allí». No se concilia de forma obvia con la epifitia de 2023/24.
  Puede ser la distinción entre el achaparramiento arbustivo del fitoplasma y el
  achaparramiento del espiroplasma, o un error del trabajo. **Cambia cuál es el
  patógeno relevante en el país**, así que es la primera pregunta de la lista.
- **Magnitud de la epifitia argentina 2023/24.** Tres cifras incompatibles y
  ninguna rastreada hasta su fuente primaria: 20 % (cita secundaria de la Bolsa
  de Comercio de Rosario dentro de un paper revisado por pares), 77 % (cita
  secundaria en una revisión, no rastreada) y 11,5 Mt más 2.045 millones de USD
  (diapositiva del organizador, sin rótulo que diga qué mide cada una). No usar
  ninguna en la presentación sin resolver esto.
- **Modo de transmisión del MSMV:** una fuente de Embrapa lo da como persistente
  circulativa y una argentina del mismo período lo declara desconocido. Importa
  porque circulativa implica que el virus no se multiplica en el insecto.
- **MSMV sigue sin identificar taxonómicamente.** Es el único de los cuatro
  agentes que no pudimos resolver.
- **Discrepancias menores de catálogo:** PlantRNA-FM figura con 35 M de
  parámetros y 24 cabezas en su artículo primario y con 34 M y 20 cabezas en la
  tabla del relevamiento; el PDF que sirve Unpaywall para el DOI de revista de
  OligoFormer es en realidad el preprint; y la equivalencia entre el preprint
  arXiv 2505.09087 y el artículo de *Briefings in Bioinformatics* bbag098 es
  inferencia nuestra por coincidencia de autor, institución, metodología y
  resultado, no una declaración del artículo.

### Pendientes metodológicos nuestros
- **Verificación por perfiles de la ausencia de maquinaria de RNAi en
  mollicutes:** correr los modelos ocultos de Markov de los dominios de InterPro
  contra los proteomas completos, o tblastn contra los genomas, para descartar
  genes no anotados. El cero actual es sólido pero es de anotación.
- **Panel curado de organismos no objetivo del agroecosistema de maíz
  argentino:** no existe en ninguna parte. Hay que armarlo, y para la mayoría de
  los nueve taxones representativos no hay transcriptoma público de buena
  calidad; ese vacío es parte del puntaje del criterio C3 y hay que declararlo.
- **Conservación poblacional del sitio blanco:** los datos públicos no alcanzan.
  El término es calculable sobre un puñado de individuos y **no** es
  interpretable como conservación poblacional.
- **Licencias todavía sin confirmar:** AIDO.RNA, PlantRNA-FM, iBeetle-Base, los
  depósitos de figshare de dsRIP, y la del ensamblado del INTA, cuyo pie de sitio
  dice CC BY-NC-SA 2.5 y cuyos metadatos enlazan la 4.0.
- **Los tres genomas nuevos de '*Ca.* P. zeae'** (BioProject PRJNA1294367) no
  devuelven ensamblados registrados: hay que buscarlos por BioSample
  (SAMN50092827/28/29).
- **Falta anclar el cronograma:** la fecha del evento no está en el material que
  tenemos y el plan está escrito en semanas relativas.

## Lista consolidada para el investigador

Ordenada por cuánto cambia nuestro plan. Las ocho primeras son las que vale la
pena hacer si el tiempo con él es corto.

1. **¿Qué significa «inhibición del crecimiento del patógeno» en el circuito de
   cuatro pasos de la diapositiva?** Con la evidencia de que no hay maquinaria de
   RNAi en mollicutes, no puede ser silenciamiento directo del fitoplasma ni del
   espiroplasma. ¿Es una simplificación, se refiere a los dos virus, o implica
   una vía indirecta vía vector o vía defensa de la planta?
2. **Los candidatos preliminares del EPILAB: cuántos son, en qué formato, contra
   qué organismo y con qué vía de entrega prevista.** Es la única dependencia
   externa de toda la propuesta. Mínimo necesario por candidato: secuencia,
   transcripto blanco, organismo, región y vía.
3. **¿Contra qué variable se validan los candidatos: knockdown, mortalidad o
   transmisión?** Importa porque la acumulación del patógeno **no** predice el
   daño, y porque generar siRNA no prueba protección.
4. **¿El trabajo que nombra a '*Ca.* P. zeae' se equivoca al decir que la
   enfermedad no se reportó en la Argentina, o está distinguiendo el
   achaparramiento arbustivo del fitoplasma del achaparramiento del
   espiroplasma?** Cambia cuál es el blanco relevante en el país.
5. **¿Qué criterio de off-target usan: complementariedad perfecta de 19
   nucleótidos, o el conjunto de reglas de la EFSA con errores y huecos?**
   Determina si nuestros puntajes de especificidad son comparables con los suyos.
6. **¿Tienen datos propios de eficacia en *D. maidis*, y sobre todo datos
   negativos** —ARNdc probados que no silenciaron—? Es exactamente lo que le
   falta a cualquier validación retrospectiva, y lo que el sesgo de publicación
   garantiza que no esté publicado.
7. **¿En qué escalón de su propia escalera de precisión están los candidatos:**
   ARNdc largo canónico, ARNdc ingenierizado, plataforma de precisión, o siRNA de
   24 nt con RdDM? Nuestro cálculo sólo está calibrado para los dos primeros.
8. **¿Contemplan la co-entrega de ARNdc contra *Dmai-dsRNase-2*,** y sus
   candidatos son de extremos romos o contemplan diseños estructurados (extremos
   en lazo, apareamientos G-U, protuberancias)? Hay validación húmeda de agosto
   de 2026 en *Varroa* que duplica la estabilidad sin tocar la hebra antisentido.
9. ¿Qué transcriptoma o anotación de *D. maidis* considera válido el laboratorio:
   el TSA `GITV00000000` o uno propio?
10. ¿Qué especies no objetivo son relevantes para el agroecosistema del maíz
    argentino, y cuáles tienen transcriptoma público?
11. ¿Cuál es la cifra correcta de pérdida de la campaña 2023/24 y qué mide
    exactamente?
12. ¿Cuál es el marco regulatorio argentino aplicable a un ARNdc pulverizado
    —SENASA, CONABIA— y hay precedente de consulta?
13. ¿Existe alguna vía institucional ya abierta por la que un bioensayo de
    alimentación pueda correrse sobre un candidato priorizado por nosotros?
14. ¿Su proceso entrega un orden puntual de candidatos, o alguna forma de
    incertidumbre sobre ese orden?
15. ¿Nos pueden pasar el PDF del trabajo de dsRNasas en *D. maidis* (PubMed
    37945254), que no pudimos abrir?
