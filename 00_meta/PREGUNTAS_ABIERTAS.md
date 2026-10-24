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

---

## Pendiente interno: enlaces de fuentes de R1 que no se registraron
**Fecha:** 2026-10-17

Seis fuentes de `research/R1_fundamentos/sources.json` tienen `url: null` y una
`url_nota`. R1 las abrió (cinco hasta el resumen, una a texto completo) pero no
anotó el enlace de la página, y ningún otro archivo del repositorio lo conserva.
Hay que reencontrarlas por título y completar el campo antes de usarlas como cita
en una presentación:

- `S12` Gomes et al. 2004, *Pesquisa Agropecuária Brasileira* 39(1):61-65 (acceso abierto).
- `S27` Arricau-Bouvery et al. 2026, *Microbiological Research* 305:128416.
- `S30` Natterin-like y legumaina de intestino de insecto (multiplicación de un patógeno).
- `S31` y `S32` Los dos informes del mastrevirus de maíz transmitido por *D. maidis*.
- `S39` Bioeficacia de *Chromobacterium piscinae* contra *D. maidis*.

`S17` (dsRNasas de *D. maidis*, Dalaisón-Fuentes et al. 2023) se completó desde el
DOI que ya consignan R2 y R3. Sigue valiendo la pregunta 15 de arriba: solo se leyó
el resumen.

---

# Ola 2 — después del corpus oficial (2026-10-17)

## Cerradas por el corpus

- **Los candidatos preliminares del EPILAB.** Era la pregunta número uno y la
  única dependencia externa de toda la propuesta. **Están**: cuatro candidatos en
  `Sequences_EPILAB.xlsx`, dos contra MRFV (proteína de movimiento y cápside) y
  dos contra el vector (Bicaudal C y subunidad D de la V-ATPasa), con su región
  elegida, su posición y un conteo de siRNA eficientes por gen. Los cuatro quedaron
  identificados por alineamiento local con confianza alta
  (`research/ola2/W5_secuencias_epilab/`).
- **¿Contra qué organismo apuntan?** Dos al virus, dos al vector, **ninguno a los
  mollicutes**. La predicción de la ola 1 se cumplió exactamente, y el corpus de
  papers tampoco contiene un solo trabajo que proponga silenciar un gen de
  fitoplasma o espiroplasma.
- **El trabajo de entrega mediada por planta en cicadélidos** (P6), que en la ola 1
  había quedado como rechazo de herramienta sin reformular: está en el corpus,
  abierto y leído.
- **BioClay frente a nucleasas:** el paper primario sí lo mide. Ver
  `CORRECCIONES.md` B1.
- **El original del SCMV en maíz:** abierto, y corrige nuestra cifra por seis
  órdenes de magnitud. Ver `CORRECCIONES.md` B2.
- **El genoma del fitoplasma:** descargado y medido con nuestros scripts
  (`GCF_001712875.1`, 576.118 pb, 565 genes).
- **¿Existe transcriptoma público del vector?** Sí, tres. Deja de ser el camino
  crítico.
- **¿Qué herramientas usa el organizador?** dsRNA-Engineer y BLAST del NCBI, y
  ninguna de las dos calcula termodinámica ni estima eficacia.

## Nuevas, y son más precisas porque están ancladas en archivos

Ordenadas por cuánto cambian el plan. Las cuatro primeras son las que hay que
hacer sí o sí.

1. **¿De dónde sale la columna «Nro de eficientes por gen» de
   `Sequences_EPILAB.xlsx`?** Declara 114, 35, 199 y 33. Ninguna de 2.132
   combinaciones de parámetros de una reimplementación local de los criterios
   publicados reproduce esos cuatro números, y dsRNA-Engineer no clasifica siRNA
   como eficientes: cuenta aciertos. Saber la herramienta y la versión cambia cómo
   hay que leer los cuatro candidatos.
2. **¿Sobre qué aislado de MRFV se diseñaron los dos candidatos virales?** La
   región de cápside es 100 % idéntica sólo al aislado de Costa Rica y cae a
   91,5-93,5 % contra los 45 registros brasileños, con una mediana de 44 de 180
   siRNA conservados. En GenBank no hay ninguna secuencia argentina de MRFV.
   ¿Tienen secuencias propias de aislados locales?
3. **¿Cuál de los cuatro transcriptomas del vector usa el laboratorio?** Hay tres
   públicos en TSA, uno de novo dentro de dsRNA-Engineer, y el que usa el grupo que
   publica en la especie es propio y no publicado, respaldado por una tesis de
   maestría de la UNNOBA de 2018. ¿Nos pasan el suyo? También define si las
   posiciones de la planilla (BicC_Dm 264-563, ATPaseD_Dm 151-450) son
   reproducibles con datos públicos.
4. **¿Cuál de los dos taxones es «MSMV»?** La sigla mapea a *maize striate mosaic
   virus* (TaxID 2025388, Geminiviridae) y a *Tenuivirus zeae* (TaxID 3052767,
   Phenuiviridae), con vectores distintos. Hasta resolverlo, cualquier diseño
   contra ese agente apunta a un blanco indefinido.
5. **¿El ARN exógeno llega al floema en maíz, o la vía realista es la adquisición
   durante el sondeo de xilema?** Tres trabajos del corpus, con tres técnicas
   distintas, lo encuentran en apoplasto, xilema y vaina del haz, y ninguno en
   floema, que es donde se alimenta *D. maidis*. Es la pregunta que más condiciona
   el modo de aplicación.
6. **¿Qué desenlace mide el laboratorio: knockdown, mortalidad o transmisión?** En
   el corpus, en entrega oral a un hemíptero, la mortalidad sube con la dosis
   mientras el knockdown no correlaciona, y el ARNdc control ya mata a dosis alta.
   No son la misma variable.
7. **¿Contemplan que un ARNdc sobre la región de MP_MRFV ataque dos marcos a la
   vez?** El tblastn local alinea ahí la poliproteína en el marco +3 y la proteína
   de movimiento en el +1, los dos al 100 % `[H]`.
8. **¿Evaluaron cicadélidos no objetivo?** Es donde está el riesgo medido: 30
   siRNA de ≥19 nt de la región de BicC sobre el ortólogo de *Homalodisca
   vitripennis*, contra cero en abeja, vaquita y colémbolo y sólo tres bloques de
   19 nt en maíz. Y falta lo que no existe: transcriptomas de cicadélidos nativos
   no plaga y de parasitoides de *Dalbulus*.
9. **La planilla tiene un corrimiento de coordenadas en CP_MRFV:** declara 200-400
   pero la región empieza en la posición 201. ¿Es base 0 en esa fila, o un error?
10. **¿El tamaño de siRNA de 21 pb que dsRNA-Engineer asigna a *D. maidis* está
    medido en la especie, o es un valor por defecto?** No tiene fuente ni en el
    paper ni en el servicio, y la asignación no sigue la filogenia.

## Pendientes internos nuevos

- **Materiales suplementarios:** los PDF del corpus traen sólo el artículo
  principal. Quedan sin ver los datos por insecto de P6 (tablas S2-S5), las
  secuencias exactas de los ARNdc de P3 (tabla S1 y figura S1) y la microscopía de
  captación de P4. Pedirlos.
- **La versión revisada por pares de dsRNA-Engineer** (*Trends in Biotechnology*)
  está tras muro de pago; toda la descripción algorítmica viene del preprint, del
  cliente desplegado y de la corrida real.
- **Incoherencia interna en el paper del SCMV** (tablas 2 y 3, controles no
  inoculados 18/20 susceptibles): sus porcentajes no se usan hasta resolverla.
- **La completitud de los ensamblados** es un proxy con miniprot, no BUSCO
  oficial: compleasm no resuelve en Bioconda. Está calibrado, pero es proxy.
- **El panel de no objetivo sigue siendo de especies modelo.** Los ceros de
  *Apis*, *Harmonia* y *Folsomia* son reales; la ausencia de riesgo en cicadélidos
  nativos y parasitoides **no está medida**, porque no hay transcriptomas.
- **Licencias sin verificar:** UniProt y KEGG quedaron consignadas sin abrir sus
  páginas de términos.
- **Sin resolver de la ola 1:** el trabajo de dsRNasas en *D. maidis* (PubMed
  37945254) no está en el corpus y sigue sin abrirse.

## R6 (2026-10-17) — pendientes y vacíos

Todo lo de abajo viene de `research/R6_estrategias_molicutes/`. Los pendientes ya resueltos se tachan en el texto del reporte, no acá.

- **ETH y Burs-α, *eth* en *D. maidis* (abierta).** El texto de `finsc-6-1811933.pdf` dice 10 % de supervivencia a los cinco días; la barra de la figura 5A mide ≈17,5 % y la leyenda fija el día 4. `CORRECCIONES.md` B5 siguió el texto. Pregunta 3 de `preguntas_investigador.md`. (La asignación de especie a cada panel quedó resuelta: A = *D. maidis*, B = *D. kuscheli*.)
- **Puntero de R1 §4.4 (resuelta en parte).** Tiene fuentes primarias, en *S. citri* (ver REPORT.md §2.2); sigue sin haber ninguna en *S. kunkelii* ni *D. maidis*.
- **Cultivabilidad de fitoplasmas, y de *Ca.* P. zeae en particular (abierta, `[?]`).** Hay una afirmación de cultivo axénico (2012) y revisiones de 2021 y 2025 que los llaman en gran parte no cultivables. No se halló reporte para *Ca.* P. zeae.
- **Vacíos de búsqueda, sin resultado abierto:** QTL o GWAS de achaparramiento en maíz (dos búsquedas); cribado moderno de moléculas pequeñas contra *S. kunkelii*; evaluación de terceros de predictores de efectores de fitoplasma; ensayo de adhesión de *S. kunkelii* a *D. maidis*; ninguna fuente para SAP54 en MBSP.
- **No buscadas en R6:** evaluación independiente de cribado virtual y de diseño de péptidos; microbioma de la planta.
- **Lecturas parciales:** de las 39 fuentes bibliográficas externas de R6, 10 se leyeron en texto completo por pasajes, 5 parcial, 7 sólo resumen (dsRNasa 2023 y el cribado de antimicrobianos son de pago) y 17 sólo fragmentos. Ver `sources.json`.
- **Bloqueo de red (registrado, no esquivado):** `git clone https://github.com/BioComputingUP/DeepSig` pide credenciales y falla desde este entorno. No se pidió acceso (no era fatal) y no se usó ningún espejo. Con ese acceso se podría correr DeepSig; los predictores de uso común (SignalP, TMHMM, Phobius) requieren licencia.
- **ORF sin anotar:** la búsqueda por perfiles cubre sólo proteínas anotadas. Falta un tblastn de las Argonautas y Dicer de control contra los genomas completos.
- **Año de S27 en R1 (abierta).** R1 lo registra como 2026; un listado de ResearchGate lo fecha en diciembre de 2025.
- **Transcriptomas y ensamblado de *D. maidis* en la Línea 2:** accesiones tomadas de W3 y de nombres de archivo de W5, no re-verificadas en R6.
- **Rechazo de una herramienta (registrado, no esquivado).** Al cerrar R6, una escritura en la memoria persistente del agente (resumen de siete hallazgos de R6) fue rechazada por un clasificador de seguridad («posible inyección de prompt») y no se guardó. No se reformuló ni se reintentó. Los hallazgos están completos en `research/R6_estrategias_molicutes/` (REPORT.md, `datos/COMANDOS.md`); lo único que no quedó es el resumen en la memoria del agente. Decidir si se quiere guardarlo a mano.

## Port de si-Fi21 (2026-10-19) — pendientes y preguntas

Todo lo de abajo viene de `tools/sifi21_port/` y de
`research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md`.

### Para el investigador

1. **¿Qué parámetros químicos cambió exactamente?** En el checkpoint dijo que tuvo
   que actualizar parámetros desactualizados. El si-Fi21 que se distribuye **ya**
   usa las tablas de Chen et al. 2012 y **ya** calcula a 22 °C, así que los dos
   candidatos obvios no son. La respuesta decide si nuestro modo «fiel» es fiel a
   lo que ellos corren, y es la que explicaría por qué los conteos no se
   reproducen. Pregunta de alto rendimiento: barata para él, y nos desbloquea.
2. **¿Contra qué base de datos corrió el modo diseño?** El conteo de «eficientes»
   del original suma **un registro por hit de Bowtie en hebra +**, no un siRNA
   único (`general_helpers.py:113`), así que el número depende de la base. Sin eso
   no hay forma de reproducirlo aunque el criterio sea idéntico.
3. **¿La región 1-200 se eligió por off-targets y no por densidad de eficientes?**
   Él mismo lo sospechó y dijo no recordarlo. Medido: en `CP_MRFV_full` la región
   1-200 tiene 8-9 siRNA eficientes y la región 195-394 tiene 21, más del doble. Si
   fue por off-targets, cerramos el punto; si no, la elección es mejorable y eso es
   un resultado nuestro.
4. **¿El «130» que mencionó existe?** En el checkpoint citó «114, 130» como
   ejemplos de la columna. Nuestros cuatro declarados son 114, 35, 199 y 33. No hay
   ningún 130. Puede ser un recuerdo impreciso o una columna que no tenemos. `[?]`

### Pendientes internos

- **Dos de los cuatro genes no se pudieron verificar.** `BicC_Dm_full` (199
  declarados) y `ATPaseD_Dm_full` (33) son transcritos multiexónicos con 97,6-100 %
  y 99,3-100 % de identidad contra el ensamblado, así que reconstruirlos desde
  coordenadas públicas daría una secuencia distinta. Hace falta que alguien con el
  corpus corra `barrido.py` sobre los cuatro. El comando está en el informe.
- **El corpus no está en esta máquina.** `work/` está fuera del control de
  versiones y `baseline_dsrip/` quedó vacío: ese trabajo se hizo en otro equipo con
  rutas absolutas. Para repetir cualquier medición sobre las secuencias de EPILAB
  hay que volver a copiar el corpus.
- **Tablas de mismatch de ARN.** El original usa tablas de ADN para mismatches
  dentro de un cálculo de ARN, de modo que un par G-U no se trata como wobble. No
  se corrigió porque no hay una fuente abierta con los parámetros de ARN
  equivalentes, y porque se midió que en esta ruta de cálculo esas tablas no se
  consultan nunca. Si alguna vez se extiende el cálculo a secuencias desapareadas,
  hay que conseguir esos parámetros de una fuente que se pueda abrir.
- **Ponderación por posición de los mismatches en off-targets.** Es la única
  crítica de la lista revisada que resultó correcta y sigue pendiente: `bowtie -v N`
  cuenta mismatches ciego a la posición, cuando la región semilla (nt 2-8) y las
  posiciones catalíticas 10-11 no valen lo mismo. Pertenece al módulo de
  off-targets, no al de eficiencia.
- **Las dos versiones de ViennaRNA no dan lo mismo** y no está decidido cuál es la
  nuestra. RNAplfold 2.1.5 (el que trae si-Fi) contra 2.7.2 (las ligaduras de
  Python) difieren en 9 eficientes sobre 1.243 ventanas en `MP_MRFV_full`. Por
  ahora se reporta cuál se usó en cada corrida.
- **El fuente de GitHub no es el binario de 2017.** `Resources/ui_sifi2015.py` mide
  23.791 bytes en la instalación y 23.787 en el clon. No se investigó en qué
  difieren. `[?]`
- **Licencia del original en conflicto:** el artículo dice CC BY-SA 4.0 y
  SourceForge dice CC BY-NC 2.0. Para uso académico no cambia nada; si algo de esto
  se publicara, hay que resolverlo. `[?]`

## Con la planilla en mano (2026-10-19) — qué se cerró y qué se abrió

La planilla `Sequences_EPILAB.xlsx` llegó y permitió correr los cuatro genes. Esto
actualiza la sección anterior.

### Cerradas

- **«¿La región se eligió por off-targets?»** Contestada por nuestra cuenta, y la
  respuesta es no. Ver `CAMINOS_PROBADOS.md`. Deja de ser pregunta para el
  investigador y pasa a ser un resultado a mostrarle.
- **Los dos genes que faltaban** (`BicC_Dm` y `ATPaseD_Dm`) ya están medidos. El
  barrido con los cuatro a la vez sigue sin reproducir los conteos declarados, con
  un error mínimo de 8 sobre ~381 siRNA.
- **El «130» que mencionó el investigador no existe en la planilla.** Las cuatro
  filas declaran 114, 35, 199 y 33. La columna 9, «Nro de eficientes por región?»,
  está vacía. Probablemente fue un recuerdo impreciso de la columna que falta
  llenar, no un dato que no tengamos.

### Abiertas, y la primera sigue siendo la misma

1. **¿Qué parámetros químicos cambió?** Sigue siendo la pregunta de mayor
   rendimiento. Con los cuatro genes el barrido de 15.120 configuraciones no
   reproduce nada, así que la versión que corrió el laboratorio no es la que se
   distribuye. Dato que puede ayudarlo a recordar: las configuraciones que más se
   acercan usan **umbral de estabilidad de extremos 2,0 kcal/mol**, no el 1,0 por
   defecto, y 25 °C en vez de 22.
2. **¿Contra qué base de datos corrió el modo diseño?** Sin eso el conteo no es
   reproducible aunque el criterio sea idéntico, porque el original suma un
   registro por hit de Bowtie.
3. **¿Con qué procedimiento quiere la columna 9?** Recortar la región y correrla
   sola da 16, 14, 17 y 16; contar las mismas ventanas dentro del gen entero da 30,
   17, 20 y 18. La diferencia llega al 47 %. Entregamos la primera porque es la que
   él describió, pero conviene confirmarlo.
4. **¿Hay un criterio que no medimos detrás de la elección de regiones?**
   Conservación entre aislados virales, restricciones de clonado, accesibilidad para
   la construcción. Es la única salida que le queda a la elección de `BicC_Dm`.

### Riesgos que el cruce puso arriba de la mesa

- **`BicC_Dm` tiene 40 ventanas con coincidencia perfecta de 21/21 en
  *Homalodisca vitripennis*** y 3 en *Harmonia axyridis*. La primera es una
  chicharrita no objetivo; la segunda es una vaquita predadora, o sea un enemigo
  natural del propio blanco. Bicaudal C está conservado entre cicadélidos, así que
  esto es esperable y hay que tratarlo como restricción de diseño, no como
  sorpresa. La región 2123-2422 reduce la exposición de 33 a 3 ventanas sin perder
  eficiencia: es una recomendación concreta que podemos llevar.
- **Cero coincidencias en *Apis mellifera*** para los cuatro genes, en las seis
  referencias. Es el dato más tranquilizador del cuadro y conviene decirlo con el
  alcance correcto: es ausencia de homología de secuencia en un transcriptoma de
  referencia, no un ensayo de toxicidad.
- **El panel sigue siendo de especies modelo.** Ya estaba anotado y sigue valiendo:
  la ausencia de riesgo en cicadélidos nativos y parasitoides **no está medida**
  porque no hay transcriptomas. Seis referencias no son el ambiente. `[?]`

### Pendientes internos

- **El corpus quedó suelto en la raíz del repositorio.** `Sequences_EPILAB.xlsx`
  estaba sin ignorar y un `git add .` lo habría subido. Se agregó al `.gitignore`
  sin moverlo (la regla prohíbe mover originales). **Conviene moverlo a
  `YHat-Biotech/`**, que es donde el `CLAUDE.md` dice que vive el corpus y que ya
  está ignorado. Lo tiene que hacer una persona, no el agente.
- **El md5 difiere del que registró W5, y está explicado.** El original era
  `048833f606d9aba2a1220a7dc280d9a9`; esta copia es
  `dcf234e1ba6d5584f1c9c1e4db59c34b`. No es otro documento: el `dc:creator`
  («Johan Rodríguez») y la fecha de creación (2026-10-17T15:03:07Z) coinciden
  exacto con lo que registró W5, pero **todas las entradas del ZIP tienen fecha de
  hoy** y desaparecieron los campos de modificación que W5 sí había visto
  (`modified 15:10:01Z`, `lastModifiedBy`). Es una reexportación del mismo
  documento, probablemente por el camino de subida y bajada.
  Dos verificaciones independientes confirman que el **contenido** es el mismo: las
  secuencias virales coinciden byte a byte con la reconstrucción desde
  `NC_002786.2`, y nuestro tamizaje de off-targets reproduce los conteos de bloque
  perfecto de W5 en las 20 celdas. `[E]` El análisis no está afectado.
- **Las referencias pesan 379 MB** en `work/offtarget_db/`, fuera del control de
  versiones. Si alguien reproduce desde cero, se vuelven a bajar.
- **Falta el criterio de un desajuste sobre los genes completos.** Se corrió exacto
  solo sobre las regiones elegidas (920 ventanas); sobre los cuatro genes completos
  se corrió solo bloque perfecto, para no inflar el autómata a 600.000 patrones.

## Cierre del criterio de un desajuste (2026-10-19)

- **Cerrado:** el criterio de un desajuste ya está corrido sobre **los cuatro genes
  completos**, no sólo sobre las regiones elegidas. Se resolvió el límite de memoria
  corriendo un gen por vez (entre 61.000 y 324.000 patrones cada uno en lugar de
  600.000 juntos). **La comparación de regiones no se da vuelta en ningún gen**: en
  `BicC_Dm` la región elegida pasa de 33 a 44 ventanas comprometidas y la
  alternativa de 3 a 6, así que la conclusión se refuerza. En `MP_MRFV` queda 11
  contra 9 y en `CP_MRFV` y `ATPaseD_Dm` empatan.
- **Abierto, nuevo:** **los gráficos no se miraron.** Se verificaron numéricamente
  (overflow, colisión de etiquetas, cobertura de CSS, parseo del JSON) y los cuatro
  pasan, pero nadie los abrió en un navegador: la extensión de Chrome no respondió y
  los rasterizadores disponibles no aplican el CSS externo. **Hace falta que una
  persona abra `research/ola2/W5_secuencias_epilab/genes/index.html` y confirme que
  no hay nada roto**, sobre todo el escalonado de etiquetas en `ATPaseD_Dm`, donde
  quedan a 28 px, y el gráfico de `BicC_Dm`, que dibuja 2.500 marcas.
- **Abierto:** el salto más grande al agregar el criterio de un desajuste está en
  **maíz contra `MP_MRFV`: de 3 a 18 ventanas**. El cultivo es el no objetivo que más
  importa, así que esas 18 merecen revisarse una por una antes de construir nada.
  No está hecho.
- **Abierto:** falta cruzar el perfil de `CP_MRFV` con la conservación entre aislados
  que W5 ya midió. La región elegida es 100 % idéntica sólo al aislado de Costa Rica
  y cae a 91,5-93,5 % contra los 45 registros brasileños. Una región más densa que
  funcione sólo en un aislado no sirve, y es la única explicación que le queda a la
  elección de ese gen.

## La pregunta para el investigador, afilada con la verificación (2026-10-19)

Ya no hace falta preguntar en abstracto qué cambió. **Se corrió si-Fi21 original,
sin modificar, sobre los cuatro genes**, y nuestro port en modo fiel reproduce sus
cuatro conteos exacto. Así que ahora la comparación con la planilla es directa:

| Gen | si-Fi21 **sin modificar** | Declarado en la planilla | Diferencia |
| --- | --- | --- | --- |
| `MP_MRFV` | 133 | 114 | +19 |
| `CP_MRFV` | 32 | 35 | −3 |
| `BicC_Dm` | 212 | 199 | +13 |
| `ATPaseD_Dm` | 42 | 33 | +9 |

`[E]` **Los cuatro difieren, y no en la misma dirección.** Tres por encima y uno por
debajo descarta una explicación simple de tipo «cuenta de más» o «cuenta de menos»:
no es un desplazamiento constante ni un factor.

La pregunta concreta, entonces: **si si-Fi sin modificar da 133, 32, 212 y 42, y tu
planilla dice 114, 35, 199 y 33, ¿qué versión corriste?** Dos pistas que pueden
ayudarlo a recordar, las dos nuestras y medidas:

1. Las configuraciones que más se acercan en el barrido usan **umbral de estabilidad
   de extremos 2,0 kcal/mol** —no el 1,0 por defecto— y **25 °C** en vez de 22.
2. **La base de datos cambia el número sin que cambie el criterio.** si-Fi cuenta un
   registro por hit de Bowtie, no un siRNA único. Lo vimos funcionando en `BicC_Dm`:
   2.504 hits sobre 2.500 ventanas, por dos pares de 21-meros repetidos dentro del
   propio gen. Ahí no infló el conteo de eficientes porque los repetidos resultaron
   no eficientes, pero contra un transcriptoma con parálogos e isoformas sí
   inflaría. **Por eso saber contra qué base corrió el modo diseño dejó de ser un
   detalle.**

Las dos preguntas siguen siendo las mismas que antes —qué parámetros cambió y contra
qué base corrió— pero ahora cada una viene con un número que la respalda, que es lo
que las vuelve baratas de contestar para él.

## R7 (2026-10-20) — pendientes y vacíos

Todo lo de abajo viene de `research/R7_microgravedad/`; las preguntas completas están en `preguntas_investigador.md`.

- **Preguntas para el investigador (abiertas).** (1) De dónde viene el interés en la microgravedad, del organizador o de un socio con plataforma de vuelo. (2) Si hay una pregunta estructural concreta sobre una proteína de los mollicutes. (3) Si hay un laboratorio socio con proteínas de mollicutes expresadas. (4) Si existe un ensayo de adhesión de *S. kunkelii* a *D. maidis*. (5) Si el organizador acepta propuestas sin RNAi (ya abierta en R6). (6) Si les interesa la maquinaria de silenciamiento de la planta.
- **Rechazo de un subagente por el filtro de seguridad (registrado, no esquivado).** La pista M3 (plantas, insectos y patógenos en microgravedad) terminó dos veces en error con «Model refused the request (content safety filters)» y sin escribir archivos. No se relanzó con otra redacción ni con otro modelo. La investigación de M3 se hizo después por fuera de la sesión que orquesta (la commiteó el usuario, 661f94e, 2026-10-20 09:33; archivos escritos el 2026-10-19 entre 20:54 y 21:01 hora local) y no se sabe en qué sesión ni con qué modelo se produjo. Se comprobó en Crossref que sus fuentes clave existen y coinciden en título, pero no se repitió su búsqueda. El propio M3 registra el rechazo de una consulta web por el servicio, no reformulada. Pregunta propia de M3, de prioridad baja: si el track espera alguna condición de gravedad alterada en la validación.
- **Bloqueo de red (registrado, no esquivado).** `www.mdpi.com` y `hwi.buffalo.edu` (M1) impiden abrir en texto completo el metaanálisis de 507 experimentos, la base BμCDB y la revisión de 2021 de Snell y Helliwell. `genelab-repo-prod.s3.amazonaws.com`, `genelab-data.ndc.nasa.gov`, `visualization.osdr.nasa.gov` y `ddbj.nig.ac.jp` (M5) impidieron descargar cualquier dato del OSDR y el maíz de PRJDB11348. No se pidió acceso a ninguno: no eran fatales para el veredicto.
- **Vacíos de búsqueda, sin resultado abierto:** cristalización de proteínas de fitopatógenos, de insectos vectores o de mollicutes en microgravedad; evidencia comparativa espacio-tierra para proteínas de membrana, glicoproteínas y complejos; estudios de ARN en microgravedad simulada; siRNA o dsRNA exógeno probado en vuelo; RNAi en un insecto en vuelo; cualquier hemíptero en vuelo; cualquier mollicute en vuelo o clinostato; datos de cristalización de Tiangong y de programas europeos actuales; precios públicos de JAXA, Space BD y CASIS.
- **Lecturas parciales.** De las 259 entradas de `research/R7_microgravedad/sources.json`, 24 se leyeron en texto completo (varias son registros de bases de datos), 92 parcial, 115 solo resumen y 28 solo fragmento de buscador. Hay que dar el desglose y no el total.
- **Verificar antes de citar.** La cifra «28 %» de JAXA (ambigua entre 61/215 y 40/144), el vínculo de la cadena pembrolizumab–ISS (descrito como «presumido»), la discrepancia texto–tabla en la mosaicidad de la PfGST, y el código PDB de la estructura de Vallazza 2002.
- **No evaluado en R7:** ARN regulatorio de los mollicutes (solo ARNr 16S), homología remota por perfiles o plegamiento de los blancos sin homólogo, modelado local de 480 proteínas de *Ca.* P. zeae, repositorios de vuelo de China, ESA y JAXA, y la licencia de cada estudio del OSDR.

---

# Ranking de candidatos (2026-10-20) — qué se cerró y qué queda

## Cerradas en esta corrida

- **De dónde salía el nulo del 7,2 %.** No estaba en `region_scoring.py`, donde la
  palabra «nulo» no aparece: está en **`baseline_dsrip/region_nulo_multigen.py`**.
  Es reproducible —con las rutas corregidas da la misma ganancia mediana de 7,2 % y
  los mismos 0 de 20 genes— y lo que mide es más angosto de lo que el registro
  sugería: permuta bloques contiguos de 30 ventanas, que preserva la estructura
  local, y el estadístico es la media del puntaje y no un conteo por umbral. Ver D15.

- **La contradicción entre `pipeline/REPORT.md` §6 y `sifi21_reproduccion.md` §3.**
  Adjudicada con medición, no con un argumento sobre incomparabilidad. Ver D15.

- **384 o 684 genes recuperados del mapeo.** `[E]` **Ninguno de los dos.** Ni 384 ni
  684 corresponde a ninguna cantidad que hayamos producido. Las cifras reales del
  mapeo son **2.814 proteínas con locus** de 3.904 alineadas (72,1 %), **7.416 loci**
  en la tabla unificada, **494 candidatos de alta confianza** y **438 genes** en el
  tamizaje de especificidad. La más parecida a «384» es **438**, que es una
  transposición de dígitos plausible en un audio; «684» no se parece a ninguna.
  Corregido en `research/checkpoints/checkpoint1.md`. No hay que preguntárselo.

- **El parámetro de BLAST que se transcribió como «HCP».** `[R]` Casi con seguridad
  es **HSP**, *high-scoring segment pair*, que sí es un término central de BLAST y no
  «ningún parámetro conocido» como decía nuestra nota anterior —esa nota estaba mal—.
  En `blastn` 2.17.0 hay dos parámetros que lo usan: **`-qcov_hsp_perc`** («percent
  query coverage per HSP») y **`-max_hsps`**, los dos verificados en el texto de
  ayuda del binario. **Cuál de los dos nombró sigue siendo `[?]`** y se le pregunta,
  pero la pregunta ahora es barata. Detalle que vale la pena: `-qcov_hsp_perc` es
  justamente el parámetro que evita la trampa de `-perc_identity` que medimos en W2
  §2.4, así que si era ése, estaba usando el correcto.

- **Qué hace el veto duro sobre los cuatro candidatos.** Deja afuera a las regiones
  elegidas de `BicC_Dm` y `ATPaseD_Dm` y no a las dos virales, y hay 1.384 de 2.201 y
  92 de 172 regiones alternativas que lo escapan. La decisión D2 tenía consecuencia
  medible y ya está medida.

- **La cuenta de azar para 18, 19 y 20 nt**, que él pidió explícito. Hecha, con tres
  nulos y el cruce localizado entre 17 y 18. Ver `research/ola2/W7_ranking/azar_por_k.md`.

- **El «salto en 17»**, que no estaba documentado con números. Ahora lo está, y el
  resultado es mixto: **no hay un salto discreto en 17** —la curva se empina
  progresivamente desde 19 hacia abajo, con factores de 2,5, 3,0 y 3,0 al bajar de
  18 a 17, de 17 a 16 y de 16 a 15— pero **17-18 sí es un umbral real**, porque es
  donde lo observado cruza a lo esperado por azar. Lo que el equipo recordaba como
  un salto de conteo es, medido, un cruce de régimen.

## Abiertas, y son para el investigador

En orden de cuánto cambian lo que hacemos:

1. **¿Qué versión de si-Fi21 corriste y contra qué base de datos?** Sigue siendo la
   primera. si-Fi21 sin modificar da 133, 32, 212 y 42, y la planilla dice 114, 35,
   199 y 33; los cuatro difieren y no en la misma dirección. Las dos pistas medidas
   están en la sección anterior de este archivo.

2. **¿Cuánto te importa un cicadélido no objetivo como *Homalodisca vitripennis*?**
   Ésta es nueva y es la que más mueve el entregable. El tercer puesto del ranking
   se da vuelta según el peso que lleve esa referencia, porque `BicC_Dm` concentra
   ahí toda su exposición: 56 ventanas con bloque ≥19 nt en el gen entero, 40 de
   ellas con coincidencia perfecta de 21 nt. Es una pregunta de política de riesgo,
   no técnica, y no nos corresponde contestarla.

3. **¿El veto por coincidencia perfecta de 21 nt con un no objetivo te parece
   bien como descarte duro, o preferís que sea una penalización?** Con el veto, las
   regiones que elegiste para `BicC_Dm` y `ATPaseD_Dm` quedan descartadas, y hay
   alternativas dentro del mismo gen que lo escapan y además son más eficientes.
   Sin el veto, se ordenan pero no se descartan. Nosotros tomamos la posición dura y
   está argumentada, pero la consecuencia es tuya.

4. **¿Un desajuste en la región semilla pesa igual que uno en el extremo 3'?** No
   tenemos evidencia para distinguirlos y por eso nuestro criterio de un desajuste no
   mira la posición. Si tenés una regla del laboratorio, cambia el peso de ese
   criterio.

5. **¿«HCP» era `-qcov_hsp_perc` o `-max_hsps`?** Ver arriba.

6. **La grafía del apellido y el dominio del correo.** `[?]` No se infiere y sigue
   pendiente. La parte local es `apolo.d.zaballo` —«Apolo» con una sola L, «D» de
   Diego— y el apellido se deletreó con una corrección en el medio que la
   transcripción automática resolvió de varias formas. **El dominio no quedó
   registrado en el audio.** Hay que preguntarlo o conseguirlo por otra vía antes de
   escribirle; es lo único que bloquea el envío.

## Pendientes internos nuevos

- **El cruce de `CP_MRFV` con la conservación entre aislados sigue sin hacerse**, y
  ahora importa más que antes: `CP_MRFV` resultó el candidato más limpio de los
  cuatro —cero off-targets en todo el gen contra las seis referencias, bajo los tres
  criterios— así que lo único que puede descalificarlo es que su región funcione en
  un solo aislado. La región elegida es 100 % idéntica sólo al aislado de Costa Rica
  y cae a 91,5-93,5 % contra los 45 registros brasileños. **Es el pendiente con mejor
  relación entre costo y consecuencia que queda.**

- **Las 18 ventanas de `MP_MRFV` contra maíz bajo el criterio de un desajuste** siguen
  sin revisarse una por una. El cultivo es el no objetivo que más importa.

- **El barajado del nulo empírico es de mononucleótidos, no de dinucleótidos.** `[?]`
  La consecuencia es que la caída que atribuimos a «estructura» (24,8 % a k = 15)
  incluye lo que un nulo de dinucleótidos habría atribuido a composición de pares, de
  modo que **ese número es un máximo y no una estimación puntual**. Se corrió además
  una sola réplica por referencia, así que no hay intervalo.

- **La condición de 26 pb con hasta 2 desajustes de dsRNA-Engineer no está
  implementada** en nuestro tamizaje local. Es la única de sus tres condiciones que
  falta para poder reproducir su criterio exacto sobre los genes que no se le pueden
  subir.

- **`project/download-file` de dsRNA-Engineer devolvió `Error!` en esta corrida**,
  donde en octubre entregó un `.tar.gz` con los archivos Bowtie crudos. `[?]` Sin
  esos archivos no se puede desagregar su conteo por condición desde su lado; se hizo
  desde el nuestro. No sabemos si es transitorio, un cambio de la API o algo propio de
  estos proyectos.

- **El ranking no mide valor del blanco y eso no se arregla con más cómputo.** Ordena
  qué tan bien está diseñada una región dentro de un gen que alguien ya eligió. Si se
  forzara un solo orden de los cuatro, los dos virales quedarían arriba, y eso sería
  un artefacto. Ver D20.

- **Las regiones alternativas que recomendamos no se verificaron contra la
  conservación dentro de *D. maidis*.** `BicC_Dm` 2123-2422 y `ATPaseD_Dm` 72-371
  están elegidas por eficiencia y por ausencia de off-target, pero no sabemos si esos
  tramos están conservados entre poblaciones argentinas del vector. Una región
  excelente que varíe entre poblaciones no sirve, y es el mismo problema que el de
  los aislados de `CP_MRFV`.

## Panel ampliado y largo de ventana (2026-10-20) — lo que abre

### Para el investigador

- **¿*Macrosteles quadrilineatus* cuenta como organismo no objetivo?** Es la pregunta que
  decide la recomendación de los dos genes del insecto. Es el cicadélido con genoma anotado
  más cercano a la chicharrita, de la misma subfamilia, y a su vez es plaga y vector de
  fitoplasmas, así que la respuesta no es técnica. **Si cuenta**, la región que W7 propone
  para `BicC_Dm` es peor que la de EPILAB en ese eje (19 ventanas con 21/21 contra 10) y hay
  que ir a 922-1221; y `ATPaseD_Dm` no tiene ninguna región de 300 nt limpia, hay que
  acortar a 200. **Si no cuenta**, vale lo que dice W7. Ya estaba anotada como pregunta en
  `pipeline/REPORT.md` §4.2 y ahora tiene consecuencia medida.
- **¿A qué largo de ventana quieren que elijamos la región, 21 o 22 nt?** El conteo total de
  eficientes casi no cambia, pero el conjunto sí, y en `MP_MRFV` la mejor región de 200 nt se
  muda de 72-271 a 820-1019 según el largo. Para hemípteros no hay perfil de largo publicado
  (`R1_fundamentos` §2.1), así que no lo podemos decidir con evidencia.
- **¿Tienen una regla terminal para 22 nt?** La de si-Fi21 mira el nucleótido 19 de 21.
  Nosotros conservamos la posición relativa (el tercero desde el final), que es una decisión
  nuestra.

### Pendientes internos

- **Faltan dieciocho especies del catálogo propio.** `pipeline/no_objetivo_catalogo.py` tiene
  26 y el panel ahora cubre 8. Por el patrón de hasta ahora —el riesgo se concentra en los
  cicadélidos— las siguientes a bajar son *Nilaparvata lugens* y *Acyrthosiphon pisum*.
- **Las regiones que propone C6 no están verificadas contra la conservación dentro de
  *D. maidis***, igual que las de W7. `BicC_Dm` 922-1221 y `ATPaseD_Dm` 88-287 heredan ese
  pendiente entero.
- **El puntaje de limpieza completo no se recalculó.** Se corrieron sólo las dos referencias
  nuevas, que alcanza para el veto pero no para el eje continuo del ranking. Para rehacer el
  ranking con ocho referencias hay que volver a bajar las seis originales (379 MB).
- **El criterio de un desajuste no se corrió contra las dos referencias nuevas**, para no
  inflar el autómata. Sólo bloque perfecto y 21/21.

## Ranking v2 (2026-10-21) — lo que abre

### Para el investigador

- **¿Una sola ventana de 21 nt con coincidencia perfecta en un cicadélido no objetivo debe vetar la
  molécula completa?** En `eth` hay una (posición 347, *H. vitripennis*, no eficiente). La región
  propuesta la evita a costa de 3 ventanas eficientes; la molécula de 544 pb que se probó la
  contiene. Es el único punto que separa a `eth` de `burs-alpha`.
- **¿Qué porción del transcrito cubren los amplicones publicados de `eth` (544 pb) y `burs-alpha`
  (578 pb)?** Nuestras regiones de 200 nt son una extrapolación de esas moléculas. Las posiciones
  exactas no se leyeron en esta sesión; hay que abrir la tabla 1 del artículo (Andrada *et al.* 2026).
- **¿Qué cuenta como organismo no objetivo entre los cicadélidos?** D23 deja fuera a *Macrosteles*
  con el argumento de que no está en Argentina; si los hermanos nativos cuentan, hay que
  reincorporarlo o buscar un sustituto.

### Pendientes internos

- **La diagonal de B.3 mide la escala, no la robustez del orden. Hay que decirlo donde se muestra
  el gráfico** (auditoría propia, 2026-10-21, sobre `research/ola2/W7_ranking/ranking.json`). El
  barrido informa frecuencias de posición sobre 2.000 juegos de pesos, y en la escala **absoluta**
  los dos ejes tienen rangos incomparables: entre los cuatro candidatos la eficacia varía un factor
  2,4-2,5 y la limpieza un factor 1,015-1,064. En la media geométrica eso deja a la limpieza sin
  palanca, y el resultado es que **en tres de las cuatro variantes de escala absoluta el orden modal
  es exactamente el orden por eficacia sola** —`MP > CP > BicC > ATPaseD` con las regiones de EPILAB
  y `MP > BicC > CP > ATPaseD` con las propuestas—. `[E]` La cuarta, `suma/conservadora/absoluta`
  sobre las regiones de EPILAB, da `MP > CP > ATPaseD > BicC` en el 65,9 %: invierte justamente el
  par en conflicto, que es lo esperable, porque la suma ponderada sí deja que la limpieza compense
  —`BicC_Dm` es el candidato con el déficit de limpieza grande— mientras que la media geométrica no.
  Con las regiones propuestas, donde ese déficit ya no existe, las dos formas coinciden. `[E]` Calculado el peso de cruce de cada par:
  con las regiones de EPILAB hay un cruce dentro del rango, `BicC_Dm` contra `ATPaseD_Dm` en
  w* = 0,32, que es el bloque 75/25 que se ve en A.3; con las regiones propuestas los tres cruces
  caen en w* ≈ 0,02, al borde, y por eso B.3 sale diagonal. No es que un candidato domine a otro en
  los dos ejes: en los dos paneles hay 3 pares en conflicto de 6. `[E]` La prueba está en el propio
  informe, que publica la escala **min-max**: ahí el orden modal de las regiones propuestas cae del
  **98,7 % al 33,7 %**, aparecen 14 órdenes distintos y `MP_MRFV`, que figura primero en el 99 % de
  los sorteos, **pasa a tercero**. `[E]` Lo que hay que corregir no es el cálculo, que está bien y
  tiene las dos escalas: es la lectura de que «la diagonal se arma sola», que sin la escala al lado
  se lee como robustez y es sensibilidad al rango de los ejes. Afecta a W7 y al v2 por igual.
- **La validación retrospectiva está sub-potenciada por un factor 2,4 en n, y hay que declararlo
  antes de correrla** (cálculo propio, 2026-10-21, sobre la maquinaria de
  `research/ola2/W6_agentes_ciencia/notas/PRB_scripts/prb_potencia.py` más la fiabilidad medida en
  `pipeline/REPORT.md` §6). El conjunto etiquetado abierto más grande que tenemos en insectos son
  los **28 ARNdc** de la Tabla S1 de Cedden 2025 (CC BY, 8 genes de *Tribolium*, en el repo) y los
  **29 siRNA** del modelo publicado. La potencia nominal con n = 28 para rechazar ρ = 0 es 0,32 si
  la correlación verdadera es 0,3, 0,76 si es 0,5 y 0,99 si es 0,7 (PRB). **Pero esa potencia
  ignora el error de medición del desenlace, que está medido:** dos ARNdc contra el mismo gen
  correlacionan 0,245, de modo que la atenuación es √0,245 = 0,495. Con eso, una correlación
  verdadera de 0,7 **se observa como 0,35**, y la potencia con n = 28 cae de 0,99 a **0,42**; para
  80 % de potencia harían falta **n = 67**. `[E]` Una ρ observada de 0,35 con n = 28 tiene IC95
  [−0,04, +0,65], que ni siquiera excluye el cero. **Consecuencia de método:** un resultado nulo en
  esta validación **no es evidencia de que el puntaje no sirva**, y hay que escribirlo en el
  pre-registro antes de mirar los datos, junto con la decisión de reportar el intervalo y no el
  valor p. Y distinguir entre dos proxies es directamente inviable: con n = 15 la potencia para
  separar ρ = 0,7 de ρ = 0,3 es 0,26 (PRB §5), y **con los n que de verdad tenemos, 28 y 29, es
  0,48 y 0,50** —reproducido con la misma aproximación de PRB, que devuelve sus mismos valores para
  n = 5, 8, 10 y 15—; para 80 % harían falta n = 57. `[E]` Y eso es la potencia **nominal**: si se
  arrastra la atenuación por fiabilidad del desenlace, las dos correlaciones verdaderas se observan
  como 0,346 y 0,148, y la potencia con n = 28 cae a **0,11**, con n = 374 para llegar al 80 %.
  Conclusión de método: **el ejercicio sirve para acotar un puntaje, no para comparar dos.**
- **Cuánta palanca puede llegar a tener la limpieza, medido como cota** (misma auditoría). Como el
  riesgo por ventana es un **máximo** ponderado y los pesos viven en el simplex, la exposición de
  una región no puede superar la fracción de sus ventanas con algún off-target, cualquiera sea el
  sorteo. Eso da un piso duro de limpieza por candidato, con las regiones de EPILAB: `MP_MRFV`
  0,9450, `CP_MRFV` 0,9750, `BicC_Dm` 0,8533 y `ATPaseD_Dm` 0,9300. `[E]` Entonces la palanca
  máxima concebible de la limpieza en la media geométrica es log(1/0,8533) = 0,159, contra una
  dispersión de la eficacia de log(0,1500/0,0600) = 0,916: **un factor 5,8 a favor de la eficacia,
  y eso en el peor caso; con los pesos base la dispersión real de la limpieza es 0,062, quince
  veces menor**. `[E]` La consecuencia práctica, que es la que hay que tener presente al leer el
  barrido: **sortear los pesos por referencia y por criterio sólo puede cambiar el orden de un par
  que ya esté casi empatado en eficacia.** Es exactamente el caso de `BicC_Dm` contra `ATPaseD_Dm`
  —log(0,0667/0,0600) = 0,106, del mismo tamaño que su brecha de limpieza, log(0,9804/0,9334) =
  0,049, y de ahí sale el cruce en w* = 0,32—. En los demás pares el sorteo es inerte por
  construcción, no por casualidad. `[H]` la lectura, `[E]` los números.
- ~~**Verificar la distribución de *Macrosteles quadrilineatus*** con un catálogo (GBIF, Biodiversidad
  Virtual o un catálogo de Cicadellidae argentinos) antes de dar D23 por cerrada.~~ **Cerrado el
  2026-10-21 contra GBIF** (`api.gbif.org`, `taxonKey` 2039662, consulta de ocurrencias por país):
  de **3.592 ocurrencias**, 2.929 son de Canadá y 549 de Estados Unidos, y hay **cero en Argentina
  y cero en todo Sudamérica** (se consultaron AR, BR, CL, UY, PY, BO y PE, las siete en 0). Los
  registros neotropicales son cuatro, de una ocurrencia cada uno: México, Panamá, Jamaica y Puerto
  Rico. El género sí llega al país, con **una** ocurrencia en Argentina (`taxonKey` 2039592). `[E]`
  La premisa fáctica de D23 queda verificada. La salvedad de método: GBIF registra esfuerzo de
  muestreo, de modo que la ausencia de registros no es prueba de ausencia, y Sudamérica está
  submuestreada para Cicadellidae; lo que sostiene la conclusión es la razón 0 sobre 3.592 con la
  distribución concentrada en América del Norte, no el cero aislado. `[H]`
- **La regla terminal a 22 nt sigue siendo nuestra decisión** (posición relativa), no la del original.
- **Las regiones propuestas de `eth` y `burs-alpha` no están verificadas contra la conservación
  dentro de *D. maidis***, igual que las de W7.
- **El largo de siRNA en hemípteros no tiene perfil publicado**: el ranking reporta 21 y 22 y no elige.
- **Qué hebra carga AGO2 no está modelado** (ficha del investigador, 19-26/10): si-Fi21 filtra por
  estabilidad de extremos 5′, pero la elección de hebra depende de más factores.

## Conservación y amplicones (2026-10-21) — lo que abre

### Para el investigador

- **¿Qué porción del transcrito cubren sus amplicones de `eth` (544 pb) y `burs-alpha` (578 pb)?** Con los
  cebadores de la Tabla 1 lo inferimos: `eth` 1–446 de la secuencia codificante más 98 nt de 5′UTR; `burs-alpha`
  79–468 más 188 nt de 3′UTR. Confirmarlo requiere la Figura S1 del artículo, que no se leyó.
- **¿Tienen secuencias de MRFV de aislados argentinos, o de la porción que codifica `MP_MRFV`?** En GenBank no hay
  ninguna argentina, y solo 4 de 71 registros cubren `MP_MRFV` (2 son la referencia). El primero del ranking
  de diseño no se puede evaluar frente a la variación entre aislados.
- **¿Qué colonia o población fue la fuente de `BicC_Dm` y de `ATPaseD_Dm`?** `ATPaseD_Dm` es idéntica al 100 % al
  contig de Illinois y difiere en un nucleótido de los transcriptomas de Ohio y de Argentina.

### Pendientes internos

- **Corregir la frase de D21** "no son subcadenas de nada publicado": `ATPaseD_Dm` es un fragmento exacto del
  contig público `GCWP01010867.1` (posiciones 190-680, W5 §2.5). La decisión no cambia —las dos siguen siendo
  confidenciales y no se subieron—, pero la frase es imprecisa.
- **Un transcriptoma de *D. maidis* que contenga `eth` y `burs-alpha`** para medir su conservación como se hizo
  con `BicC_Dm` y `ATPaseD_Dm`; hoy solo hay el genoma de Córdoba, que es la fuente menos confiable.
- **Repetir la conservación a 22 nt**, que no se hizo.
- **Si una pool de siRNA con algunos desajustes sigue silenciando** no lo podemos cuantificar; limita cuánto pesa
  que `CP_MRFV` tenga solo 7 eficientes conservadas de 17 en su región.

## Ola 3 (2026-10-21) — lo que abren las cinco investigaciones del checkpoint

Integrado desde los `NOTAS_PARA_META.md` de `research/ola3/C1` a `C5`. Lo que ya estaba en esta
lista y quedó cerrado por la ola 3 está marcado donde corresponde.

### Para el investigador, en orden de cuánto mueven el plan

1. **¿Modo diseño (HE) o modo off-target (HS)?** Los valores por defecto son distintos —el de alta
   sensibilidad **apaga** estabilidad de extremos y accesibilidad— y el conteo de eficientes cambia
   por completo. Sin esto, los conteos declarados y los nuestros no son comparables. Es la pregunta
   más barata de la lista.
2. **¿Corren con desajustes permitidos?** Si se permite ≥ 1, si-Fi **desactiva el cálculo de
   eficiencia por completo**, y el manual explica que es porque no hay datos confiables. Es una
   explicación candidata para los conteos que no reproducimos.
3. **¿Pusieron el umbral de estabilidad de extremos en 1,75 o en 2,0?** Dos barridos independientes
   —el de W5 sobre nuestro port y el de C2 sobre `sifi21INTA`— apuntan al mismo parámetro y no a la
   química. Reemplaza a la pregunta anterior, más vaga, de «qué parámetros cambiaste».
4. **¿Los números de la planilla son «eficientes» o «eficientes sin off-targets»?** En `sifi21INTA`
   son dos columnas distintas, y la segunda depende de la base y del blanco principal elegido a mano.
5. **¿De dónde sale el rango de 150 a 250 nt?** Si hay un ensayo propio con largos comparados en
   *Dalbulus maidis*, ese dato vale más que toda nuestra tabla de literatura, porque sería el único
   en el rango exacto, la especie exacta y la vía de entrega que ellos usan. Ver D29.
6. **¿Qué peso relativo tiene un hemíptero no objetivo frente al maíz?** Es el único parámetro del
   criterio de ranking que no nos corresponde fijar, y es el que decide si `BicC_Dm` queda última
   o no. Se enlaza con la pregunta ya registrada sobre *Macrosteles quadrilineatus*.
7. **¿Les interesa matar o esterilizar?** Los candidatos nuevos de cicadélidos están sesgados a
   esterilidad: `Rpn6` mata y esteriliza, `Ruvbl1` esteriliza, y la ATP sintasa β silenciada de 5 a
   46 veces en *Scaphoideus titanus* **no afectó la supervivencia** hasta 14 dpi. El ranking ordena
   distinto según el objetivo.
8. **¿EPILAB corre el tamizaje de off-targets contra transcriptomas, contra genomas, o contra los
   dos?** De eso depende si la ponderación por clase de blanco (D28) es una mejora o una corrección.
   El antecedente publicado en la especie usó BLASTn contra transcriptomas con criterio de
   significancia, sin umbral en nucleótidos.
9. **¿Usan el BLAST web con sus valores por defecto para verificar off-targets?** Si es así, contra
   algo del tamaño de un genoma el resultado es **cero por construcción**: `megablast` con palabra
   28 no puede sembrar una consulta de 21 nt, y un Expect de 0,05 descarta los HSP de 20-21 nt
   contra una base grande.
10. **¿«HCP» era «HSP»?** Nuestra lectura es que sí, pero HSP no es un parámetro sino la unidad de
    resultado. ¿Se refería a `-max_hsps` / `-qcov_hsp_perc`, al E-value o al percent identity? La
    diferencia cambia qué le recomendamos configurar.
11. **¿Tiene dato de distribución de tamaños de ARN pequeños en algún cicadélido?** No encontramos
    ninguno, ni para *D. maidis* ni para la familia. El hemíptero mejor caracterizado (mosca blanca)
    apunta a **22 nt**, no a 21, y el marco de referencia del campo no incluye Hemiptera. Si no hay
    dato, ¿corremos todo a 21 y a 22 y entregamos las dos?
12. **¿Cómo quiere que tratemos el riesgo por región semilla?** Necesita 6-8 nt de
    complementariedad, así que **ningún umbral de largo entre 16 y 21 nt lo tamiza**. Hoy es un
    vacío de método declarado.
13. **¿Se verificó alguna vez que un off-target predicho ocurra?** Ninguna de las herramientas que
    leímos valida sus predicciones con un experimento.
14. **¿Conocen el trabajo del proteasoma 26S en *S. titanus* y *E. variegatus* (2025)?** Y si lo
    conocen, cómo leen la discrepancia de nomenclatura: el transcrito que usan como `Rpn6` alinea
    con la familia PSMD6 y no con PSMD11/`Rpn6`. Es la única pregunta de C5 que no se puede
    contestar con bibliografía.
15. **¿Qué versión de ViennaRNA usa el servidor de Apolo Rocket?** Sin eso no hay forma de comparar
    contra nuestras corridas: entre 2.1.5 y 2.7.2 hay varios eficientes de diferencia por gen.
16. **¿El método «IA» de Apolo Rocket existe fuera del esquema?** El campo `method` está
    documentado como «'sifi21' or 'IA'» y viaja a la base, pero no hay implementación en el backend
    público.
17. **¿Cuál de las tres declaraciones de licencia de si-Fi21 rige?** Ver D32.
18. **¿Tienen acceso institucional a *Pest Manag Sci* 2019 (PMID 30417535)?** Es el único estudio de
    mortalidad por ARNi en *Euscelidius variegatus* y quedó en resumen.

### Pendientes internos

- **Falta medir cuántos veredictos finales cambian al corregir el índice de la regla terminal.** El
  fuente comprueba la posición 2 del 21-mero donde Ui-Tei 2004 y la propia geometría de si-Fi ponen
  la posición 1. Medido el efecto sobre la rama (51,4 %) y sobre el booleano terminal (31,4 %);
  falta el cambio de veredicto, que requiere correr el port con ViennaRNA.
- **RNAplfold 2.1.5 no está en esta máquina.** Es barato de cerrar para quien tenga la instalación
  de Windows de si-Fi, y cierra la comparación de `sifi21INTA` contra la corrida del original.
- **La regla de nucleótidos terminales del port a 22 nt es una generalización, no una regla
  validada**: mira el tercero desde el final. Nadie publicó esa regla para 22 nt.
- **Los k ≥ 21 del análisis de azar no son interpretables** (0 a 4 coincidencias contra esperados de
  0,05 a 2). Para medir el exceso a 21-22 nt haría falta un conjunto de consultas mucho mayor.
- **Los dos datos de Hemiptera que no son mosca blanca** (psílido 21 nt, delfácido 21-22 nt) están
  citados vía revisión. Si el largo de ventana se vuelve una decisión de diseño, hay que abrir los
  primarios.
- **No se clasificaron por clase de blanco los aciertos de abeja**: hay dos con un desajuste que
  aparecen sólo en el transcriptoma y son candidatos a unión exón-exón. El script los resolvería
  cambiando dos constantes.
- **Sesgo de borde al recortar una región, medido y no contabilizado:** el veredicto de eficiencia
  de una ventana cambia con el contexto hasta **54 nt** de distancia, así que las ventanas de los
  primeros y últimos ~60 nt de una región recortada no valen lo que valían dentro del gen entero.
- **Fuentes que no se pudieron abrir:** `10.1002/ps.5263` (muro de pago; se buscaba dosis, n y
  curvas de supervivencia) y el conjunto de calibración de si-Fi en e!DAL. Bloqueos de red
  registrados y no esquivados: `sourceforge.net`, `zenodo.org`, `doi.ipk-gatersleben.de`,
  `cell.com`, `nature.com` y `academic.oup.com`; y el apéndice de parámetros de BLAST+ en el
  NCBI Bookshelf, que devuelve reCAPTCHA a un cliente programático —se reemplazó por medición
  directa sobre el binario, que es mejor evidencia—.
- **Fuente que no se buscó y debería:** el cribado genómico de blancos de ARNi en *Tribolium* (Buer
  *et al.* 2025) que el trabajo de `Rpn6` cita como fundamento. Es el puente entre el cribado que ya
  usa el pipeline y los candidatos nuevos.
- **Cero resultados de ARNi funcional en *Macrosteles quadrilineatus*** en la consulta a PubMed,
  pese a ser el cicadélido mejor anotado. Vale como vacío: el genoma anotado y la literatura
  funcional están en especies distintas.
- **Defecto editorial del artículo de si-Fi21:** su entrada bibliográfica de Tafer 2008 está
  fusionada con la de RNAplex, con volúmenes y páginas mezclados. Si se cita, citar por DOI.
- **El repositorio público de `apolorocket` trae credenciales de base de datos en claro.** No se
  reproducen en ningún entregable y conviene no hacerlo. Si alguna vez hay contacto con el grupo,
  es algo que agradecerían saber.
- **Dos repositorios públicos nuevos para el radar del equipo**, de los que se leyó sólo el README:
  `DanielHarley/zeaguard-drylab` (ARNdc contra *D. maidis*, Bicaudal C y dsRNasa-2) y
  `MaxiSack/RNAival` (identificación de candidatos de siRNA, GPL-3.0).

### Rechazos de herramienta y contenido dirigido a agentes

**Ningún rechazo de filtro de seguridad** en ninguna de las cinco investigaciones. **Ningún
contenido intentó redirigir el trabajo**: se revisaron 21 textos completos en C4 y ninguno traía
instrucciones dirigidas al lector automático. Dos aclaraciones que vale registrar porque podrían
confundirse con lo contrario. El README del repositorio oficial de si-Fi21 incluye un texto que
pide buscar archivos temporales en el directorio del usuario para recuperar las secuencias de
siRNA: es una nota de uso de los autores, no una instrucción dirigida a un agente, y no se ejecutó
nada a partir de ella. Y el fork `rj-price/siFi-2.0` trae archivos de guía para asistentes de
código (`CLAUDE.md`, `PLAN.md`): se leyeron **como dato**, para extraer su lista de defectos
conocidos, y no se siguió ninguna instrucción escrita ahí.

## T5 — lo que la crítica de herramientas no pudo sostener (2026-10-21)

Al escribir `entregables/critica-herramientas.md` no hizo falta medir nada nuevo, pero quedaron
tres cosas que el documento declara y que conviene tener registradas acá:

- **La tabla de energía de `sifi21INTA` atribuida a Zuber et al. 2022.** La atribución sale del
  comentario del código (`freeEnergy.py:306`, tabla en `:61-74`) y no del artículo, que no se
  abrió. Es el único parámetro de química que el laboratorio cambió respecto del original: está
  identificado, pero no verificado contra su fuente. `[?]`
- **El respaldo de Jackson et al. 2006 (*RNA* 12:1179) para el argumento de la región semilla**,
  que es lo que vuelve biológicamente relevante que BLAST pierda las posiciones 2, 3 y 4. De ese
  artículo sólo se abrió el resumen, y su sistema experimental es cultivo de células humanas, no
  insecto. Va marcado `[R]`; si alguna vez se abre entero, sube a `[E]`.
- **La crítica de la accesibilidad contradice trabajos que reportan lo contrario** —Tafer *et al.*
  2008 (*Nature Biotechnology*) y Shao *et al.* 2007 (*RNA*)—, de los que sólo se abrió el resumen
  porque no son de acceso abierto. El entregable lo declara y acota la afirmación a lo que se pudo
  revisar. Si alguien del jurado conoce esos trabajos, la respuesta preparada es que lo que
  decimos es que **el umbral booleano fijo no está justificado con la evidencia abierta**, no que
  la accesibilidad sea biológicamente irrelevante. `[?]`

### W7 · El index.html y el REPORT.md ya no dicen lo mismo (detectado 2026-10-21)

Al revisar W7 para la corrección de B.3, se comparó el `research/ola2/W7_ranking/index.html` con su `REPORT.md`: tienen estructura de secciones distinta (la página usa A.1 a B.4, el informe 1 a 6) y **25 porcentajes del informe no aparecen en la página**, con solo 14 en común. Los dos archivos se escribieron a mano (no hay generador), así que no hay una fuente que gane. Lo que se corrigió en esta sesión (§2.1 bis del informe y el pie de B.3) es la única parte sincronizada. Decisión pendiente: reescribir la página desde el informe, o generar el informe desde la página. Hasta entonces, la página no debe citarse como fuente de cifras.

---

## `eth` y `burs-alpha`: el paso que faltaba no es conseguir el transcriptoma (2026-10-21)

Ya estaba registrado más arriba que el transcriptoma del grupo que publica en la especie es propio
y no publicado, respaldado por una tesis de maestría de la UNNOBA de 2018. Se confirmó la cita
exacta y se encontró algo que cambia el pendiente de C8.

**La cita, completa.** Andrada *et al.* 2026 (*Frontiers in Insect Science*, PMC13279319) dicen en
métodos que los candidatos salen de *«transcriptomic datasets assembled in our laboratory for
Dalbulus maidis»*, y citan la tesis de V. Palacio, *Secuenciación del transcriptoma de Dalbulus
maidis*, UNNOBA 2018 (`repositorio.unnoba.edu.ar/xmlui/handle/23601/481`), de ARN de cuerpo entero
de individuos agrupados de varios estadios. No hay accesión de TSA ni BioProject para ese
ensamblado; lo único depositado son las dos secuencias codificantes, **PZ371507** (`eth`) y
**PZ371508** (`burs-alpha`). `[E]`

**Lo nuevo, y es un error de método nuestro, no una falta de dato.** C8 cerró el punto diciendo que
no ubicó contigs de los dos genes, después de que el BLAST web contra el TSA del NCBI quedara en
cola media hora y se cancelara. Pero **los tres transcriptomas que C8 ya usa están descargados**
—con ellos alineó `BicC_Dm` y `ATPaseD_Dm`—, así que la búsqueda que correspondía es local contra
`GCWP01`, `GITV01` y `GHCC01`, no contra todo el TSA. Y como las consultas serían PZ371507 y
PZ371508, que son públicas, no hay compuerta de confidencialidad que lo impida. `[H]` Es una
corrida de minutos y no se hizo.

**El orden, por costo:** (1) buscar las dos secuencias públicas localmente contra los tres
ensamblados, con el tamizador del repositorio; si no están, eso también es informativo y declarable.
(2) Si no aparecen, ver si la tesis de Palacio 2018 trae el ensamblado como archivo y no sólo como
texto. (3) Pedírselo a los autores: `GHCC01`, la fuente argentina que C8 califica como la de mejor
calidad, está depositada desde el CeBio de Pergamino (PRJNA505619) y el grupo de Andrada es de la
UNNOBA, también en Pergamino, así que es plausible que haya contacto directo `[H]`, no verificado.
(4) Si nada resulta, el pendiente se cierra como hueco declarado y no como tarea, igual que
`MP_MRFV`.

**Lo que no se hizo acá:** ninguna búsqueda —los transcriptomas no están en esta máquina— y no se
abrió la tesis de Palacio, sólo su cita dentro del artículo. El paso 1 queda sin ejecutar.


## Pendientes de la Fase 1 del checkpoint 2 (2026-10-22)

- **Matar contra esterilizar sobre `eth` y `burs-alpha`.** El ranking no tiene eje de fenotipo, y `tablero/orden.html` sólo cubre `BicC` y la V-ATPasa. No se puede afirmar si el orden de los candidatos del insecto cambia según el objetivo. Pendiente de decisión del equipo sobre si se agrega ese eje o se deja como límite declarado.
- **Criterio para comparar regiones de 200 y 300 nt.** La cascada cuenta ventanas y favorece a las regiones de 300 nt; las escalas continuas cuentan tasas. Con eso, `ATPaseD_Dm` frente a `bursA_Dm` cambia de orden según el método. Hay que elegir un criterio antes de reportar ese par.
- **Escala z.** La fase pedía comparar z contra min-max. El código tiene sólo absoluta y min-max; la z no se calculó.
- **Brief de la Fase 1.** El texto de la fase dice que C5 sesga `eth` y `burs-alpha` a esterilidad. El catálogo registra letalidad para los dos (DM-05, DM-06); la esterilidad es de `BicC` (DM-01). Corregir en la Fase 3 o 4 antes de usar esa frase.
- **Fuentes de fenotipo de la Fase 1.** Las cifras de DM-01, DM-03, DM-05 y DM-06 se citan a través de `catalogo_genes_blanco.md`. Los artículos no se reabrieron en esta fase.

- **Corrección del catálogo y de C7 (pendiente, Fase 5 o antes).** DM-05 (`eth`) y C7 §6 dan 10 % de supervivencia a día 4, cifra que el texto atribuye a `burs-alpha`. La cifra de `eth` no está en el texto y hay que leerla de la figura 5A. DM-06 (`burs-alpha`) sí tiene 10 %. DM-01 (`BicC`) dice «esterilidad» y «>170 veces al día 7», y el resumen no lo dice. DM-03 (`ATPaseD`) no registra el control GFP (≈37 %). Ver `docs/plan_checkpoint2/salidas/F1_decision_ranking.md` §8.
- **FUENTES S18 (Jones 2021).** Dice «texto completo no accesible»; el texto se leyó el 2026-10-22 desde bioRxiv.
- **Figura 5A de Andrada 2026 (P3).** La supervivencia de `ds-eth` a día 4 no está en el texto y no se pudo leer de forma verificable. Hay que leerla con la figura en pantalla o con los datos de la fuente antes de citar una cifra.

## Preguntas de la Fase 2 (2026-10-22)

- Qué célula del insecto recibe el dsRNA por ingesta: ninguna fuente abierta lo identifica. Pregunta para el investigador y para la literatura de dsRNasas.
- Cuánto reduce la degradación por dsRNasas en la saliva de hemípteros la eficacia oral: sin cuantificar en fuentes abiertas. Dalaisón-Fuentes 2023 no está abierto.
- Dalaisón-Fuentes 2022: falta el texto completo para verificar el día del efecto, la letalidad y el término «esterilidad».
- Gan 2010: falta leer el texto completo del PDF del repo.
- MRFV: no hay ensayos de spray ni de ARN pequeños en maíz en fuentes abiertas.

## Datos que faltan para completar la Fase 1 (2026-10-22)

- **Dato por ventana no está en disco.** El barrido completo con escala z (y cualquier recálculo del ranking) necesita las tablas por ventana de eficiencia y de off-target. `ranking_v2.json` sólo guarda conteos por región y frecuencias del barrido. `work/sifi_v2/` no existe y los FASTA de EPILAB (`work/sifi_v2/fasta/`) están fuera del control de versiones. Para recalcular hay que reconstruir `work/sifi_v2/` con `tools/sifi21_port/ranking_v2.py` a partir de las secuencias de EPILAB (`YHat-Biotech/Sequences_EPILAB.xlsx`) y de las siete referencias de C7 §9, todo local. Pregunta: ¿se reconstruye ese directorio o se declara la escala z fuera de alcance? El barrido reducido que se hizo sólo sobre eficacia no está calibrado (hasta 38 puntos porcentuales de diferencia con el guardado) y no se reporta como resultado.
- **Texto completo de Dalaisón-Fuentes 2022 (BicC).** No es de acceso abierto. Sin él no se puede verificar el día del efecto, la letalidad ni el término «esterilidad» de DM-01.
- **Cifra de supervivencia de `ds-eth` (Andrada 2026, figura 5A).** No está en el texto; hay que leerla con la figura en pantalla.

## Preguntas de la Fase 3 (2026-10-22)

- **Respuesta del investigador al correo.** No se sabe si contestó. Si hay respuesta, hace falta el texto (sobre todo la pregunta de matar o esterilizar) antes de la Fase 4.
- **Latencia del MRFV.** La fuente abierta (Jones y Medina 2020) da 18 a 22 días para *Spiroplasma kunkelii*, no para el virus. D34 usa «unos 20 días» dicho por el investigador; falta una fuente para MRFV.
- **Duración del efecto en *D. maidis*.** Los ensayos abiertos miden 4 a 5 días; la ventana de latencia es de unos 20. Pregunta para el investigador: ¿hay seguimientos más largos?
- **Varianza del knockdown entre dsRNA independientes del mismo gen en *D. maidis*.** Sin ese dato no se puede fijar n ni umbrales numéricos.
- **Gen blanco a ensayar.** Propuesta conceptual: `eth` o `burs-α` para el eje letal y `BicC` para el reproductivo. La elección es del investigador.
- **Método para detectar siRNA en *D. maidis*** y **comparación de dsRNA libre contra formulado en insectos**: sin método ni estudio abierto.
- **Techo de 0,245.** Cálculo del repo sobre iBeetle (*Tribolium*, letalidad); los datos están fuera del repo (`~/yhat/data/ibeetle`) y no se reprodujo. Pendiente de reproducir o declarar sólo como `[H]`.
- **Límite del ensayo de región.** Un ensayo con dos regiones de `BicC` sólo acota la fragilidad de la región; no valida si-Fi21 ni evalúa el veto por *H. vitripennis*.

## Escala para ordenar pares dentro de un grupo (2026-10-22)

- `eth_Dm` precede a `bursA_Dm` en escala absoluta (76–100 % de los sorteos) pero el par es inestable en min-max, que estira una diferencia de limpieza de unos 0,015. La regla de D38 pide que el orden se sostenga en las dos escalas; si se exigiera sólo la absoluta, el orden sería `eth_Dm` > `bursA_Dm`. Pregunta de método para el equipo, no para el investigador. Ver `docs/plan_checkpoint2/salidas/F1_decision_ranking.md` §2.

## Resuelto en la Fase 5 (2026-10-22)

- **Grafía del apellido y dominio del correo** (ítem 6 de la lista anterior): resuelto, el correo se envió según confirmó el usuario. Queda abierto sólo registrar la fecha y el texto enviado.- **CSV de Cedden** (28 secuencias): resuelto por D41. Ya estaba en el remoto desde el 2026-10-21 y se deja publicado con la advertencia de que la unión no tiene clave. Los archivos adicionales originales (`MOESM1` y `MOESM2`) no están en disco.

## Quimeras con las regiones vigentes (2026-10-22, línea C13)

- **El acierto en maíz que fabrica el empalme.** El empalme de `MP_MRFV` + `ATPaseD_Dm` crea el bloque `GGCAAGGTGATGAAGGAGG` (19 nt: 4 de `MP_MRFV` y 15 de `ATPaseD_Dm`), que está en tres transcriptos de maíz (`XR_004852610.1`, `XR_004856333.1`, `XR_562605.3`) y no existe en ninguno de los dos genes. Los tres llevan prefijo `XR_`, es decir ARN no codificante. Pregunta para el investigador: ¿alcanza un bloque de 19 nt contra un ARN no codificante de maíz para descartar un orden de quimera, o se exige 21/21?
- **El empalme, ¿es del insecto o del virus?** En una quimera mixta, las 20 ventanas del empalme no pertenecen a ningún gen. D44 las cuenta como off-target contra el genoma del vector, que es lo conservador, y de esa elección depende que dos de las ocho mixtas queden vetadas. Es una decisión de criterio y conviene confirmarla con el laboratorio.
- **Los empalmes no están tamizados contra humano.** El panel local tiene seis referencias; el ranking v2 usa siete, con *Homo sapiens*. Falta bajar el transcriptoma humano para cerrar el tamizaje de las 240 ventanas de empalme.
- **Fuente sin abrir sobre el nombre de la técnica.** Wang *et al.* 2021, «Chimeric Double-Stranded RNAs Could Act as Tailor-Made Pesticides for Controlling Storage Insects», *J. Agric. Food Chem.* 69(22):6166-6171. Apareció en una búsqueda web como la cita académica más temprana de «chimeric dsRNA» aplicado a plagas; es de ACS y no se consiguió versión abierta. **No se cita en ningún documento del proyecto.**
- **Por qué el empalme rinde tan poco.** Con las regiones de EPILAB las 240 ventanas de empalme daban 48 eficientes y con las vigentes dan 4. La explicación candidata —que una región elegida por densidad está enriquecida y el empalme es secuencia que nadie eligió— es nuestra y no está probada; además las 20 ventanas de una unión no son independientes, así que el n efectivo es 12 y no 240.

# Respuesta del investigador (2026-10-22) — qué cierra y qué abre

Fuente: correo de Diego del 22 de octubre de 2026, transcripto en
`docs/plan_checkpoint2/salidas/F6_respuesta_y_cambios.md`. Plan de ejecución:
`docs/plan_ola4/PLAN_OLA4.md`.

## Cerradas

- **En qué configuración corrieron si-Fi21.** `siFi21_8_1.0_0.1_1111`: modo diseño con los
  valores por defecto —ventana de accesibilidad 8, umbral de estabilidad de extremos **1,0**,
  corte de accesibilidad 0,1 y las cuatro casillas activas— `[R]`. El nombre se decodifica contra
  `main.py:344-362` del fuente original. Cierra la primera mitad de la pregunta 1 del correo y
  retira el 1,75 como explicación (ADR D45).
- **Si la planilla es «eficientes» o «eficientes sin off-targets».** Es la primera: conteos del
  análisis de diseño; los off-targets los evalúan por separado `[R]`. Cierra la segunda mitad de
  la pregunta 1 (ADR D46).
- **Si la rama de la regla terminal existe en el original.** Confirmada por él: «efectivamente, la
  rama que identificaron existe en el código original», y describe el atajo igual que nosotros
  —para ciertas combinaciones de nucleótidos el algoritmo prescinde de estabilidad de extremos y
  selección de hebra y deja sólo accesibilidad— `[R]`. La auditoría de `CAMBIOS.md` C1 queda
  confirmada por el laboratorio que usa la herramienta.
- **Si nuestra posición conservadora sobre off-targets es defendible.** Él corre el mismo criterio
  y por el mismo motivo `[R]`. D17 confirmado por una fuente independiente. Lo que corrige es la
  consecuencia, no el criterio (ADR D48).
- **Si *Homalodisca vitripennis* debía salir del panel.** No: pidió conservarla, separando
  exposición de conservación `[R]` (ADR D47).

## Siguen abiertas, y son los pedidos del lunes 26

En orden de cuánto desbloquean. Las seis son preguntas del correo que no contestó, más una nueva
que su propia carta hizo necesaria.

1. **La salida por ventana de su corrida `siFi21_8_1.0_0.1_1111`, y contra qué base de Bowtie
   corrieron el diseño.** Es nueva y es la que más rinde: con la clasificación por ventana la
   comparación es exacta y el desajuste de conteos se cierra en una tarde. La base importa porque
   la columna del original cuenta aciertos de Bowtie y no ventanas (ver más abajo).
2. **Qué transcriptoma de *Dalbulus maidis* usan, y si lo comparten.** Pregunta 3 del correo, sin
   contestar. Bloquea la conservación de `eth` y `burs-alpha` y es la referencia que la línea M7
   necesita.
3. **¿Matar o esterilizar?** Pregunta 5, sin contestar, y sigue siendo decisión suya.
4. **Los dos pesos del panel no objetivo**, ahora reformulados por su propia carta: no un peso
   sino `w_exposicion` y `s_conservacion` (ADR D47). Pregunta 4, reencuadrada.
5. **Por qué la región de `MP_MRFV` es 1–200.** Pregunta 2, sin contestar. Decide si la crítica de
   la región se sostiene o se reformula.
6. **De dónde sale el rango de 150 a 250 nt.** Pregunta 6, sin contestar. Nuestra lectura (D29:
   convención compatible con la evidencia, no conclusión de ella) queda como estaba.
7. **BLAST por defecto y qué quiso decir con «HCP».** Pregunta 7, sin contestar. La medición de C3
   y el ADR D27 no cambian.

## Nuevas, que abre la carta

- **¿Qué referencia reproduce los cuatro conteos?** La columna «Efficient siRNA hits» del original
  cuenta un registro por acierto de Bowtie en la hebra `+`, agrupado por nombre de referencia
  (`general_helpers.py:107-123` y `sifi_pipeline.py:195-221`) `[R]`, mientras `sifi21INTA` cuenta
  una fila por ventana (`SifiPipeline.py:430-448`). Entonces una ventana eficiente que no pega en
  la referencia no cuenta, una que pega sólo en la hebra menos no cuenta, y una que pega dos veces
  cuenta dos veces —y eso ocurre: 2.504 aciertos para 2.500 ventanas en `BicC_Dm` `[M]`—. Es la
  primera explicación que puede mover los conteos en los dos sentidos, que es la forma del
  desajuste: la planilla baja en tres genes y sube en uno. Es `[H]` hasta que la línea M1 la mida.
- **Del efecto del recorte, cuánto es plegamiento y cuánto es tratamiento de posiciones.** Lo
  pregunta en su punto 2 y está contestado a medias: C13 §4 separa la parte aritmética (200
  posiciones de inicio en contexto contra 180 recortada) de los cambios de veredicto por borde, y de
  esos hay dos identificados a 64 y 66 nt cuyos 21 nucleótidos son idénticos y a los que sólo les
  cambió la accesibilidad `[M]`. **Contestada por M2 (2026-10-23):** los cambios por borde son 23 y
  no 27 —los 27 eran del conjunto `recomendadas`— y la partición está hecha para los 23: **22
  cruzan por `target_site_accessibility` y 1 por `end_stability`** `[M]`. El de `end_stability` es
  un mecanismo que C13 no cubría, de extremos sin nucleótidos colgantes en las dos primeras
  ventanas del recorte. Detalle en `research/ola4/M2_ventana_a_ventana/` y corrección anotada en
  C13 §4.
- **Cuántas etiquetas de eficacia hacen falta para distinguir el modo fiel del corregido.** La
  validación retrospectiva da ρ = +0,142 [-0,247, +0,492] contra +0,024 [-0,356, +0,397], n = 29
  `[M]`: no se distinguen. El número de etiquetas necesario no está calculado. Línea M4.
- **¿Cuál es el ensayo prospectivo mínimo que discrimina los dos modelos?** Los dos difieren en 19,
  7, 50 y 8 ventanas en los cuatro genes, y ninguna va en sentido contrario `[M]`, así que el
  ensayo mide discordantes contra concordantes. Falta el diseño con su tamaño de muestra. Línea M4.
- **¿Cómo se comparte el port, y bajo qué licencia?** Nos pidió conocerlo. Dos pendientes antes de
  mandarlo: la auditoría de secuencia sobre el árbol y el historial (el repositorio ya tuvo un
  incidente de 21-meros commiteados, resuelto reescribiendo tres commits locales), y la licencia
  del original, en conflicto entre el artículo (CC BY-SA 4.0) y SourceForge (CC BY-NC 2.0) `[?]`,
  que D32 dejó sin resolver y que conviene preguntarle a él, que la usa. Línea M9.

## Pendientes internos nuevos

- Corregir la sección de la planilla de `entregables/critica-herramientas.md`, que hoy afirma el
  1,75 como la mejor explicación. Espera el resultado de M1 para no reemplazar una explicación
  equivocada por un agujero.
- Implementar D47 y D48, que cambian el ranking ya entregado. **Esperan confirmación del
  usuario**, y D47 además nos devuelve el empate del tercer puesto.
- Completar D26 agregando `nt19`, `nt2` y la rama terminal al TSV por ventana: hoy el ADR obliga a
  publicar los términos continuos y los nucleótidos terminales no están. Línea M3.
- La Parte 1 de la Fase 6 (diez preguntas anticipadas y agenda de cinco minutos) sigue sin hacerse.
- No se verificó el texto del correo realmente enviado contra el borrador de siete preguntas. El
  mapeo de la respuesta se hizo por contenido, no por número.
- **Registrar fecha y texto del mensaje de respuesta cuando se mande.** El usuario decidió el
  2026-10-22 enviarlo antes de la reunión del lunes 26, con revisión del equipo previa (D50); el
  envío lo hace el equipo. Es el mismo pendiente que quedó sin cerrar con el correo anterior, así
  que esta vez se anota al mandarlo. Si no se manda, dejarlo escrito también: el fallback es decir
  los tres contenidos en persona el lunes.

## Pendientes abiertos por la línea M1 (2026-10-22)

- **¿Contra qué registro, no contra qué base, corrieron el diseño?** La pregunta para el lunes se
  afina. En las tres bases que midió C2, el blanco principal de los dos genes virales recibe
  **todas** las ventanas —`MP_MRFV` contra `NC_002786.2`, 1.243 de 1.243; `CP_MRFV` contra
  `AF265566.2`, 508 de 508 `[M]`—, o sea que las secuencias de EPILAB son subcadenas exactas de
  esos registros públicos y contra ellos la regla por acierto **no puede bajar** el conteo. Para
  que `MP_MRFV` baje de 133 a 114 hace falta una referencia que difiera de la secuencia que
  diseñaron: otro aislamiento, no el conjunto completo de registros de MRFV. Hay que pedir el
  número de acceso o el archivo, por gen `[H]`.
- ~~**¿En qué unidad está cada campo de `04_resumen_base_datos.json`?**~~ **Resuelto el
  2026-10-23, midiendo.** La misma corrida de Bowtie contra la misma base, en la máquina que
  tiene el corpus, da 2.504 líneas de alineamiento y **2.500 nombres de lectura distintos** para
  `BicC_Dm` contra `epilab4` `[M]`, y la confirmación independiente está en el contig público de
  *D. maidis*: 2.357 alineamientos y 2.353 ventanas distintas, y 2.353 es exactamente el número
  que el resumen declara en `hits_blanco_principal`. Así que **`hits_bowtie` cuenta alineamientos
  y `hits_blanco_principal` cuenta ventanas**. No hizo falta el driver sin versionar; hizo falta
  correr Bowtie una vez.
- **Los tres drivers de C2 no están versionados.** `run_inta.py`, `run_db.py` y `barrido_inta.py`
  viven sólo en `work/C2/scripts/`, que está en `.gitignore`. El README de las corridas los
  documenta pero no los contiene, y por eso la pregunta anterior no se puede contestar desde el
  repositorio. Hay que versionarlos: no llevan secuencias, sólo rutas.

## Pendientes después de correr la matriz de M1 (2026-10-23)

- **¿Contra un transcriptoma o contra el genoma corrieron los dos genes del insecto?** Es la
  pregunta nueva y la más barata de contestar para él. Si fue contra el genoma de *D. maidis*, el
  conteo de `ATPaseD_Dm` que sale de la herramienta es **0**: cuarenta de sus cuarenta y dos
  ventanas eficientes pegan sólo en la hebra menos del cromosoma `OZ319711.1` y la regla del
  original únicamente evalúa la hebra `+` `[M]`. El 33 declarado no puede venir de ahí, así que la
  respuesta discrimina. Y si fue contra un transcriptoma, queremos saber cuál: el contig público
  `GITV01000968.1` da 200 para `BicC_Dm` contra sus 199 declarados, que es la única coincidencia
  de toda la matriz.
- **¿Cuál es el número de acceso de su referencia de MRFV, por gen?** La pregunta ya estaba
  abierta; lo que se agrega es una predicción que la hace discriminante. Para `MP_MRFV`, ninguno
  de los sesenta y cinco registros públicos de MRFV da 114: las filas posibles son 133, 133 y 30,
  y con un desajuste permitido 133, 133 y 85 `[M]`. Si el acceso que nos den está en esa lista,
  el conteo no sale de la referencia; si no está, hace falta el archivo.
- **`CP_MRFV` = 35 no puede salir de la referencia, y hay que decidir de dónde sale.** El
  declarado está **por encima** de nuestras 32 ventanas eficientes, y la regla del original sólo
  puede superar el conteo por ventana si alguna ventana eficiente pega dos o más veces en la misma
  referencia; eso no ocurre en ninguna de las sesenta y cinco `[M]`. Quedan dos candidatos, los
  dos del lado del motor y no de la base: la versión del motor de accesibilidad —con ViennaRNA
  2.7.2 el mismo port da 39, y 35 cae justo entre 32 y 39 `[M]`— o una diferencia de criterio que
  todavía no identificamos `[?]`.
- **Faltan cinco contigs de la ensambladura TSA `GITV01` para completar esa celda.** Lo que se
  usó son los dos contigs que la ola 3 identificó como blanco principal, bajados por número de
  acceso. Para la **fila** de la tabla eso es exacto, porque una fila depende sólo de su propia
  referencia; lo que queda subestimado es (d) y por lo tanto `suma_filas`. La ola 3 midió que
  `BicC_Dm` toca seis referencias de esa base y `ATPaseD_Dm` dos, y la lista de las otras cinco
  está en `work/C2/` y no en el repositorio `[?]`.
- **`bowtie -a -v 1` no corre contra las dos bases más grandes** con el binario de 32 bits que
  trae si-Fi2015: aborta con `Error reading _rstarts[] array` en `zmays` (172 MB) y en el genoma
  de *D. maidis* (984 MB), y corre bien hasta 114 MB `[M]`. Las ocho celdas quedan declaradas como
  fallidas en `resultados/procedencia.json`, no como ceros. Necesitan un Bowtie 1.3.x de 64 bits,
  que es el de la máquina de la ola 3.
- **El plan y el issue #5 llaman a `GCF_002217175.1` «transcriptoma de *D. maidis*» y no lo es.**
  La cabecera del archivo dice *Folsomia candida* `[M]`. En `work/offtarget_db/` está el
  **genoma** de *D. maidis* y **ningún transcriptoma** suyo; el que la ola 3 usó como
  `tsa_gitv01` es la ensambladura TSA `GITV01`, que no está en esa carpeta. No invalida ninguna
  medición de la ola 3, donde la base se llamaba por su nombre, pero sí el inventario del plan,
  que cuenta tres transcriptomas de *D. maidis* donde hay uno y no está descargado.
## Las siete variables biológicas que faltan para comparar genes, por la línea M8 (2026-10-23)

M8 contestó hasta dónde compara el número de siRNAs eficientes
(`research/ola4/M8_que_compara_el_conteo/REPORT.md`) y la respuesta deja esta lista: son las
variables que habría que incorporar para comparar estrategias dirigidas a genes distintos, y lo
que falta de cada una. Van juntas porque son pedidos que se le pueden hacer al investigador en la
misma conversación del lunes, ordenadas por cuánto cambiarían la decisión y no por lo que cuesta
conseguirlas.

1. **Ventana de latencia del patógeno contra tiempo hasta el efecto.** Es la que manda: si el
   insecto transmite antes de que el silenciamiento haga efecto, matarlo no corta la transmisión.
   Falta la fuente de latencia del MRFV —la abierta (Jones y Medina 2020) es de *Spiroplasma
   kunkelii*, 18 a 22 días `[?]`— y faltan seguimientos más largos que los 4 o 5 días de los
   ensayos abiertos. **Esta comparación es la que decide si esterilizar alcanza.**
2. **Evidencia de fenotipo tras silenciamiento.** Tenemos cifras para los cuatro ejes pero no son
   comparables entre sí: distinto desenlace, distinto estadio, distinto control y n de tres
   réplicas de tres ninfas en lo molecular. Falta un desenlace común, y falta por ingesta lo que
   hoy sólo existe por microinyección.
3. **Nivel de expresión en el tejido que el ARNdc ingerido alcanza.** No tenemos nada y el hueco
   es doble: ninguna fuente abierta identifica qué célula recibe el ARNdc por ingesta, y el
   transcriptoma del grupo que publica en la especie es de cuerpo entero de individuos agrupados
   de varios estadios (Palacio, UNNOBA 2018), así que no da expresión por tejido ni por estadio.
4. **Redundancia por parálogos.** No medido, y es una corrida local posible que no se hizo: buscar
   los parálogos de cada candidato en `GCA_975739785.1` con las herramientas que ya usamos.
   Silenciar un miembro de una familia puede no hacer nada, y eso no aparece en ningún conteo.
5. **Esencialidad del gen.** Tenemos KEGG como vía de anotación y ninguna medición propia. No hay
   panel de esencialidad para hemípteros; iBeetle es *Tribolium*, coleóptero holometábolo. Falta
   un criterio operativo que no sea «la vía parece importante».
6. **Recambio de la proteína.** Fija cuánto tarda el efecto, y por eso entra directo en la
   comparación del punto 1. Sin dato, propio ni abierto, para ninguno de los seis candidatos.
7. **Estadio de desarrollo de la exposición.** Las ninfas ya transmiten y el tercer estadio fue el
   más sensible en un cicadélido emparentado `[R]`, pero la dieta en sobre de parafilm no sirve
   para ninfas porque las mata. Si el estadio más sensible es el que no se puede tratar por la vía
   que se quiere usar, el orden de los candidatos cambia `[H]`. Falta la sensibilidad por estadio
   en *D. maidis*, que no está publicada.

## Pendientes abiertos por la línea M4 (2026-10-23)

Los cinco salen de inventariar las fuentes de etiquetas posibles para comparar los dos modos del
port. Ninguna fuente se cita acá sin haberla abierto; lo que no se pudo abrir está marcado `[?]` y
es justamente el pendiente.

1. **iBeetle-Base: ¿hay dos fragmentos no solapados por gen?** Es la pregunta que decide si la
   única fuente grande de etiquetas del reino correcto sirve. El artículo de la base (Dönitz *et
   al.* 2015, *NAR* 43(D1):D720, `10.1093/nar/gku1054`, PMC4383896) dice que los fenotipos se
   guardan **por fragmento** y que hay 5.180 ARNdc distintos sobre 16.505 genes de *Tribolium
   castaneum*, pero **no menciona fragmentos no solapados** ni cuántos genes tienen dos reactivos
   independientes `[?]`. Si los hay, hay pares de reactivos contra el mismo blanco con desenlaces
   independientes, que es la estructura que M4 muestra como necesaria para comparar dos criterios;
   si no, la línea se cierra en una tarde. Se contesta consultando
   `ibeetle-base.uni-goettingen.de` o la actualización de 2017 (`10.1093/nar/gkx984`). Límites ya
   conocidos: licencia **CC BY-NC 4.0**, el reactivo es un fragmento de ~479 pb y no un siRNA de
   21 nt, y el desenlace son términos de ontología con penetrancia en tramos, no una eficacia
   continua.
2. **El conjunto de 2.431 siRNA de Huesken 2005 no tiene punto de descarga abierto que hayamos
   encontrado.** Los dos trabajos que lo usan y que sí abrimos —Vert *et al.* 2006
   (`10.1186/1471-2105-7-520`) y Thang *et al.* 2015 (`10.1186/s12859-015-0495-2`)— lo citan al
   original (`10.1038/nbt1118`) sin enlace ni archivo adjunto `[?]`. Queda pendiente revisar el
   material suplementario del original. No se citó contenido suyo más allá de lo que esos dos
   reportan, y de todas formas cambia de reino, de maquinaria y de vía de entrega.
3. **siRecords:** las 2.470 etiquetas de eficacia «muy alta» y 2.514 de «baja» aparecen reportadas
   en Thang *et al.* 2015, pero **no pudimos abrir la base** ni verificar su licencia o si sigue en
   línea `[?]`. Sus etiquetas son clases y no valores, así que no sirven para una correlación de
   rangos.
4. **GenomeRNAi no se pudo abrir** desde esta máquina (error de TLS en `genomernai.org`). No se
   cita nada de su contenido `[?]`.
5. **La dispersión del silenciamiento entre siRNA de una misma clase no la tenemos medida en ningún
   sistema comparable.** El tamaño de muestra del ensayo propuesto la supone en 20 puntos
   porcentuales `[H]`; si en el ensayo resulta 25, el n por brazo sube de 32 a 49. Es el primer
   supuesto a revisar con los datos del propio ensayo, y conviene preguntarle al investigador si
   tiene una estimación de su sistema.

## Pendientes abiertos por la línea M2 (2026-10-23)

Los tres salen de comparar los perfiles por ventana en vez de los conteos finales. El primero
condiciona qué puede hacer la herramienta cuando llegue el archivo del investigador; los otros dos
son variables del desajuste de conteos que M1 vino a reconciliar.

1. **¿La salida por ventana de Diego trae los términos intermedios o sólo el veredicto?** El
   comparador de M2 atribuye el término que cruzó el corte leyendo la brecha de ΔG, la
   accesibilidad y los cuatro booleanos de cada compuerta. Si su archivo trae sólo `is_efficient`,
   la herramienta sigue dando la matriz de confusión y la lista de posiciones que cambian, pero la
   columna `terminos_que_cruzan` sale vacía y el cambio queda sin causa atribuida. Es la primera
   cosa que hay que preguntarle cuando mande el archivo, y conviene pedirle las columnas en el
   mismo mensaje para no perder una vuelta.
2. **¿Qué tabla de vecinos más cercanos usó el laboratorio, si corrió si-Fi?** Es una pregunta que
   M2 hace inevitable: cambiar `RNA_NN3` por `RNA_NN4` mueve poco el conteo pero bastante el
   conjunto. En `BicC_Dm`, modo corregido, el conteo pasa de 171 a 168 mientras **once ventanas
   cambian de clase** `[M]`. O sea que dos corridas que informan casi el mismo número pueden no
   estar señalando las mismas ventanas, y la parametrización es una variable más del desajuste. Si
   corrieron si-Fi21 sin tocar nada es `RNA_NN3` y la pregunta se cierra sola; vale confirmarlo
   porque es gratis.
3. **Las dos primeras ventanas de un recorte: ¿se excluyen o se reportan con la advertencia?** M2
   midió que ahí el original calcula los extremos sin nucleótidos colgantes, porque el siRNA de dos
   posiciones antes no existe, y que una de las cuatro regiones vigentes cambia un veredicto por
   esa vía `[M]`. M7 la contestó a medias y propone **reportar con la advertencia, sin excluir**,
   porque excluirlas mueve la fracción de victorias de 75,6 % a 74,2 % `[M]`. Falta que el
   investigador lo confirme.
