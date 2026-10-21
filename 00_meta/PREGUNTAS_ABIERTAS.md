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
