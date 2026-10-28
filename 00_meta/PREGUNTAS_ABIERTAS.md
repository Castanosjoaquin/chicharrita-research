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

## Pendientes abiertos por la interfaz del port (2026-10-23)

### Para preguntarle al investigador

1. **La licencia, otra vez, y ahora bloquea algo concreto.** D32 la dejó sin resolver: el
   artículo de si-Fi declara CC BY-SA 4.0 y SourceForge declara CC BY-NC 2.0 `[?]`. Mientras
   no se sepa cuál rige, `sifi_plus/` **no lleva archivo de licencia** y el nombre público
   queda en suspenso («si-Fi+» es nombre de trabajo). Es el pedido 6 del lunes y ahora tiene
   consecuencia práctica, no sólo formal.
2. **Si la regla terminal se entiende sobre la posición 1 o sobre la 2.** El código comprueba
   `sirna_sequence[1]`, que es la posición 2, donde la regla habla del extremo 5′ de la hebra
   opuesta —la posición 1 en la geometría del propio si-Fi—. Corregir el índice cambia la rama
   que decide en el **51,4 %** de las ventanas, 3.265 de 6.346 `[M]`. No lo tocamos: si es un
   error de transcripción, hay una década de resultados calculados con el índice corrido.
   Propuesta: agregarlo como tercer modo, nunca como el comportamiento por defecto.
3. **Si quiere correrlo en su máquina.** Hoy la instalación está documentada pero no
   empaquetada, y la decisión fue que el lunes la demo la corre el equipo. Si lo va a usar, el
   empaquetado para Windows es una tarea aparte.
4. **Si tiene una referencia para ponderar los desajustes por posición** (región semilla nt 2-8
   contra posiciones 10-11), o si prefiere que lo propongamos nosotros con lo publicado y lo
   marquemos como hipótesis.

### Pendientes internos

5. **Contrastar nuestra marca de baja complejidad contra `dustmasker`.** El criterio que
   implementamos es nuestro `[H]` y está declarado en `sifi_plus/complejidad.py`; el
   repositorio ya tiene una corrida del estándar en
   `research/ola2/W5_secuencias_epilab/analisis/dustmasker_full.txt`. Hasta hacerlo, la marca
   no puede subir de `[H]`.
6. **Releer los tamizajes ya publicados con el descuento de baja complejidad.** Todo lo que
   está en `research/` se corrió sin la marca. No cambia ningún número, pero sí puede cambiar
   qué se afirma con él: cualquier afirmación sobre coincidencia perfecta de 21 nt en un no
   objetivo hay que volver a mirarla. Afecta en particular a la lectura de que el riesgo está
   concentrado en *Homalodisca vitripennis* —40 ventanas de `BicC_Dm` con 21/21 perfecto—, que
   es una de las conclusiones más fuertes del entregable. **Esto es lo primero que haría antes
   de la reunión** `[M]`.
7. **La regla terminal con ventana de 22 nt.** El CLI y la interfaz ya aceptan
   `--sirna-size 22`, pero la regla sigue mirando `size - 3` y `1`, que es lo que hace el
   original. Nadie verificó que esas sean las posiciones que corresponden en 22 nt, y el
   investigador confirmó que 21-22 es lo que tiene respaldo biológico (D35).
8. **Integrar la conservación al perfil.** `tools/sifi21_port/conservacion.py` ya calcula
   conservación por ventana y no está en la interfaz: hoy el perfil mira eficiencia y riesgo,
   no estabilidad del blanco entre poblaciones del vector. Es la tercera columna que falta y el
   cálculo ya existe.
9. **Bowtie de 64 bits.** El 0.11.3 de 32 bits del instalador aborta con `-v 1` en bases de más
   de ~114 MB `[M]`: ni el transcriptoma del maíz ni el genoma del vector. Es la pieza que
   falta para reproducir la regla de conteo del original sobre las bases grandes.
10. **Activar el gancho de pre-commit.** `git config core.hooksPath tools/verificacion/hooks`
    sigue sin correrse (M9 §6), y ahora importa más: la carpeta nueva tiene fixtures de prueba
    con nucleótidos, y aunque están exceptuadas con su motivo, el chequeo es lo que mantiene la
    excepción honesta.
11. **Mirar el resto de los gráficos del repositorio.** El pendiente de
    `CAMINOS_PROBADOS.md:542` se cerró sólo para la interfaz nueva, que se abrió en Chrome y se
    miró. Las cuatro fichas de gen de W5 y el informe de M7 siguen verificados nada más que
    numéricamente. El caso nombrado como riesgo —el gráfico de `BicC_Dm`, que dibuja 2.500
    marcas— sigue sin mirarse; en la interfaz nueva ese problema se resolvió dibujando una
    marca por tramo contiguo y no por ventana, pero `informe_html.py` no tiene ese arreglo.

## Cuatro agujeros conocidos de `tools/verificacion/sin_secuencias.py` (M9, 2026-10-24)

Los cuatro salieron de la revisión del cambio de hoy y ninguno se arregló en él. No
cambian ninguna cifra publicada, pero cada uno es un punto ciego que conviene cerrar antes
de apoyarse en la herramienta para decidir que algo se puede compartir.

1. **El modo historial no corre la pasada 2.** Recorre línea de diff por línea de diff, así
   que las columnas de k-meros solapados —el patrón del incidente de C9 cuando los k-meros
   miden menos de 21 nt— no se ven en el historial, sólo en el árbol. Por la misma razón, la
   pasada 3 pierde todo k-mero partido por un salto de línea. Arreglo: reconstruir el texto
   agregado por archivo y por commit, y correrle las tres pasadas.
2. **El descarte de «tramo dentro de un token mayor» es más ancho que su motivo.** Se
   escribió para las fuentes woff2 en base64, pero descarta cualquier tramo con un vecino
   alfanumérico que no sea nucleótido, en los dos modos. Un tramo pegado a una etiqueta
   —`seqACGTACGT...`— se saltea. Arreglo: exigir contexto de base64 real en vez de
   cualquier letra.
3. **Las excepciones son por archivo entero.** El motivo describe el dato que había el día
   que se escribió; cualquier fila agregada después a un archivo exceptuado queda fuera de
   las pasadas 1 y 2 sin que nadie la mire. Arreglo: exceptuar por huella del tramo. Esto
   ya no afecta a la pasada 3, que desde hoy no se exceptúa nunca.
4. **En el historial, una línea agregada cuyo contenido empieza con `++` se confunde con
   una cabecera de diff y se saltea.** Improbable, pero es un `startswith` sobre texto que
   escribe cualquiera. Arreglo: reconocer cabeceras sólo fuera de los *hunks*.

## 2026-10-25 — Lo que abre y lo que cierra la carta del investigador del 25 de octubre

La carta resuelve la discrepancia de los cuatro conteos (D62). Esto es el saldo: qué preguntas se
cierran, cuáles quedan y cuáles son nuevas.

### Se cierran

- **Por qué la planilla declara 114, 35, 199 y 33 y cualquier corrida da más.** Explicado por la
  función histórica de conteo y **reproducido** por nosotros `[M]`
  (`research/ola5/N1_regla_de_conteo/`).
- **Si el umbral de estabilidad de extremos estaba en 1,75.** No era la causa; la coincidencia era
  circunstancial `[R]`.
- **El pedido 1 de la reunión**, la clasificación por ventana de su corrida: ya no hace falta.

### Siguen abiertas

- **Los FASTA exactos de los índices de Bowtie de cada corrida histórica.** La carta nombra las
  referencias principales —`Dalbulus_maidis_genome_v1` y `Maize_rayado_fino_virus_genome_v1`— y
  dice explícitamente que **no verificó los FASTA**, así que prefiere no dar la equivalencia por
  confirmada `[?]`. Sin eso no se puede cerrar qué base produjo cada fila de la tabla del
  original, que es lo que M1 dejó medido y sin explicar.
- **La regla terminal: rama fiel contra filtro adicional.** Las dos quedan como hipótesis hasta
  tener evidencia que permita evaluar cuál predice mejor los resultados experimentales `[R]`, y M4
  midió que la evidencia abierta no alcanza: harían falta 2.784 siRNA replicando el único diseño
  etiquetado que encontramos `[M]`. Coincidimos con él; no es una pregunta que podamos cerrar
  nosotros.

### Nuevas

1. **¿Con qué tabla de apilamiento corre el método histórico `siFi21_8_1.0_0.1_1111`?** Las curvas
   reconstruyen 138, 40, 218 y 35, que son los valores de `sifi21INTA` por defecto —tabla de Zuber
   *et al.* 2022— y no los 133, 32, 212 y 42 del si-Fi21 original. Si corre con Zuber, la línea
   base para comparar contra la planilla cambia `[?]`.
2. **¿El contador por incrementos produjo también las cifras de las doce regiones candidatas de la
   planilla, o sólo las de los cuatro genes completos?** Sigue abierta, pero ya no a ciegas:
   `N10` midió qué pasaría si fue el mismo. El sesgo por región va de **0 % a 22,2 %** —la región
   vigente de `ATPaseD_Dm` no pierde ninguna ventana y la de `MP_MRFV` pierde más de un quinto— y
   en el marco de contexto el «36 contra 35» de `BicC_Dm` **se vuelve un empate, 33 a 33** `[M]`.
   Lo que falta es sólo saber si lo fue `[?]`.
3. **¿El ancho de cobertura de la curva histórica es 20 confirmado, y la línea de todos los siRNA
   también?** Si la línea azul de su curva usa 20, su meseta es 20 y no 21; es un chequeo de un
   minuto del lado de ellos y cierra la distinción de N2 `[?]`.
4. **¿Qué objetivo manda: cortar transmisión en la temporada o reducir la población entre
   generaciones?** Decide el eje y, con él, el blanco: el fenotipo publicado de `BicC` es de
   oviposición, así que actúa sobre la generación siguiente y no sobre la transmisión del individuo
   ya expuesto `[H]`. Es la pregunta que más cambia la recomendación y no es una medición nuestra.
5. **¿Cuál es la ventana de latencia del MRFV?** La cifra de unos 20 días que usamos es del
   investigador (D34) `[R]` y la única fuente abierta que pudimos abrir da 18 a 22 días para
   *Spiroplasma kunkelii*, que no es el patógeno que nos importa `[?]`.
6. **¿Qué exposición le asignan a *Homalodisca vitripennis*?** Es el único peso con palanca de todo
   el ranking: con exposición cero se mudan tres de las seis regiones recomendadas `[M]`.
7. ~~El tercer marco cruzado con la grilla.~~ **Contestado el 2026-10-25** (`N3` §6): en el marco
   intermedio 922-1221 le gana a 2121-2420 en el **41,1 %** de las 4.368 configuraciones, con 640
   empates y margen mediano cero, y a 264-563 en el **99,9 %**, que es la fracción más alta de los
   tres marcos `[M]`. Cruzado con el eje de referencia (`N3` §7) se corrió **una de las cuatro
   fuentes**: `GITV01`, la única cuya base está en esta máquina, donde el orden no se mueve y el
   margen se abre. **Las otras tres quedan no corridas y el motivo es de insumos, no de método:**
   en esta máquina no hay `blastn` ni `makeblastdb` y `work/W5/db/` no está en el árbol, así que
   `GHCC01` y `GCWP01` no tienen base en disco y el genoma del Reino Unido, que sí la tiene, no se
   puede recorrer sin un alineador de consultas largas `[?]`.
8. **Las ventanas de juntura con apareamiento parcial.** Medimos que de las 240 ventanas de
   juntura de las doce quimeras, 4 son eficientes y ninguna de esas 4 tiene blanco continuo de
   21 nt `[M]`. Lo que no sabemos es si una complementariedad incompleta les da alguna actividad,
   que es lo que decidiría si son inútiles o sólo menos útiles `[?]`.

### Una limitación operativa, para quien clone el repositorio

El gancho de pre-commit llama a `python3`, y en la máquina donde se corrió la ola 5 el `python3`
del PATH **no tiene `openpyxl`**, mientras el intérprete de Anaconda sí. El gancho entonces
rechaza con «no se pudo verificar», que es el comportamiento correcto —es fail-closed— pero obliga
a correr las dos pasadas a mano con el intérprete que tenga la dependencia. Queda anotado porque
es la segunda vez que ese gancho cuesta tiempo por el mensaje y no por el hallazgo.

## 2026-10-26 — Lo que abre y lo que cierra el checkpoint 2

La reunión del 26 de octubre está transcripta y mapeada en
[`research/checkpoints/checkpoint2.md`](../research/checkpoints/checkpoint2.md). A diferencia
de la carta del 25, esta vez **no corrigió nada de fondo**: validó la recomendación y abrió una
línea de diseño nueva. Este es el saldo.

### Se cierran

- **La exposición de *Homalodisca vitripennis*.** Era el único peso con palanca y lo pedíamos
  como número. **No va a haber número, y la pregunta se retira.** Dijo las dos cosas a la vez:
  que el organismo no está en la Argentina y *«puede no importar»*, y que *«puede venir
  eventualmente y tal vez si la querés matar»* `[R]`. Lo que pidió en cambio es que la decisión
  esté a la vista: *«mostrar que esas posibles decisiones están presentes es como el extra»*
  `[R]`. Pasa de pendiente bloqueante a decisión declarada del equipo, con la consecuencia ya
  medida al lado —con exposición cero se mudan tres de las seis regiones recomendadas,
  `research/ola4/M5_dos_ejes/` `[M]`.
- **Qué transcriptoma de *D. maidis* usan.** No está en NCBI, *«está en otro lado»*, y se
  comprometió a mandarlo en un zip `[R]`. La pregunta se cierra; lo que queda es el insumo.
- **Si la lectura de `BicC_Dm` como gen poblacional es correcta.** Confirmada por él:
  *«claro, porque tiene que ver con la oviposición»* `[R]`. Sostiene
  `entregables/recomendacion-defendida.md` §1.
- **Con qué nivel de justificación hay que defender los pesos del ranking.** Pidió exactamente
  el análisis de sensibilidad que ya está hecho —*«si probás un par de pesos distintos y cambia
  mucho, o todo medio parecido»*— y cerró con el argumento de por qué no hace falta más:
  *«al final, de vuelta, vas a tener que ir a la planta y probar»* `[R]`.

### Siguen abiertas

- **Qué objetivo manda: cortar transmisión en la temporada o bajar población entre
  generaciones.** Es la misma pregunta que abrió la carta del 25 y sigue sin respuesta. Él
  confirmó el fenotipo de `BicC` y dijo explícitamente que **no sabe si eso cambia la
  decisión** `[?]`. Es la que más mueve la recomendación y no es una medición nuestra.
- **Si una complementariedad incompleta da actividad en las ventanas de juntura.** No se la
  preguntamos y él no la tocó. Sigue siendo el límite declarado de `research/ola5/N4_quimeras/`
  `[?]`.
- Todo lo que la carta del 25 dejó abierto y esta reunión no tocó: los FASTA de los índices de
  Bowtie, la tabla de apilamiento del método histórico, el marco con el que la planilla contó
  las doce regiones, el ancho de cobertura de la línea azul y la latencia del MRFV.

### Nuevas

1. **La secuencia de `V-ATPase B` de *Dalbulus maidis*.** Propuso armar quimeras combinando
   fenotipos que no se solapan y dio tres ejes: reproducción, alas y letalidad `[R]`. Al
   revisar el catálogo contra ese pedido apareció que **los tres ejes ya tienen candidato en
   la especie**: `BicC` (`DM-01`, oviposición casi nula), **`V-ATPase B` (`DM-02`, alas
   deformes** y supervivencia 16 % al día 4) y `V-ATPase D` (`DM-03`, supervivencia 18 % al
   día 4 y efecto en alas **no** significativo), los tres de fuente leída completa `[M]`. Las
   dos subunidades del mismo complejo se separan justo por el eje que él nombró. Lo que falta
   no es bibliografía: es **la secuencia de `V-ATPase B`**, que no está en el panel de
   trabajo y puede salir del transcriptoma que va a mandar `[?]`.
2. **Qué quimeras de fenotipos complementarios tienen sentido biológico.** La maquinaria de
   evaluación existe y la juntura ya está medida; lo que no existe es el criterio de qué
   combinar con qué. Es la única línea de cómputo nueva que deja la reunión `[H]`.
3. **Cuándo llega el zip del transcriptoma.** Lo ofreció él en la reunión. Mientras no esté,
   la línea `C11` —conservación de `eth` y `burs-alpha`— sigue bloqueada por insumo, y no se
   puede verificar contra la fuente del laboratorio ninguna posición de la planilla. Si no
   llega en un par de días conviene recordárselo `[?]`.
4. **Los identificadores de ese transcriptoma no van a servir para buscar por nombre.** Avisó
   que *«los IDs están hechos por el que hizo el transcriptoma, no coinciden los nombres, no
   vas a poder encontrar, pero sí por identidad o homología»* `[R]`. O sea que la entrada es
   alineamiento y hay que presupuestar esa pasada, no leer una anotación.

### Ola 6 (2026-10-26)

5. **La secuencia de `V-ATPase B` tiene una segunda vía que no espera el zip.** La entrada 1 de
   esta sección la dejó como «puede salir del transcriptoma que va a mandar», y
   `docs/plan_cierre/PLAN_CIERRE.md` §8 la clasifica como insumo bloqueado. Hay otra ruta con lo
   que ya está en disco: los **tres transcriptomas públicos de *Dalbulus maidis*** están como
   bases de búsqueda en `work/C11/` (`db_GHCC01`, `db_GCWP01`, `db_GITV01`), y la V-ATPasa es un
   complejo conservado con proteína disponible en parientes —incluido *Peregrinus maidis*
   (`DE-01`), que tiene las dos subunidades con bioensayo publicado—. O sea que la subunidad B se
   puede **intentar recuperar por homología a nivel proteína** antes de que llegue el archivo. Si
   sale, desbloquea la quimera; si no sale, el resultado útil es saber que esos transcriptomas no
   la contienen, que es la misma respuesta que `C11` necesita para `eth` y `burs-alpha` `[H]`.
6. **Esta máquina no puede correr nada de lo que necesita alineador o plegado.** Verificado con
   `command -v`: no hay `blastn`, `tblastn`, `makeblastdb`, `miniprot`, `diamond`, `bowtie` ni
   `bowtie2`, no está el módulo `RNA` de ViennaRNA ni `RNAplfold`/`RNAfold`, y el `python3` del
   PATH es 3.9.6 con numpy 2.0.2 `[M]`. `C13` corrió con Python 3.13.15, numpy 2.5.4 y ViennaRNA
   2.7.2, y las bases de `work/C11/` se construyeron en otra máquina. No es una pregunta de
   método sino de asignación: hay tareas que sólo corren en la máquina del equipo que tiene el
   entorno, y conviene saber cuál es antes de repartir trabajo.
7. **Hasta dónde llega la banda de contexto de una quimera con otras regiones.** Los 61 cambios
   de veredicto en heredadas y el máximo de 66 nt son de las doce quimeras de las cuatro regiones
   vigentes. El techo derivado del código es 72 nt corriente abajo y 59 corriente arriba, y no se
   violó en 204 ventanas cambiadas de cuatro tablas distintas, pero **con un gen nuevo —`V-ATPase
   B`— no sabemos cuántas heredadas se van a mover ni en qué dirección** `[?]`. Se mide al correr,
   no se estima.
8. **`entregables/critica-herramientas.html` no sale de `md_a_html.py`.** Regenerarlo desde su
   `.md` da un archivo distinto en 26 líneas de texto, y la diferencia no es del conversor: el
   `.html` commiteado tiene una cabecera que el `.md` no tiene —«Investigathon Y-Hat · track
   chicharrita / ARNi · entregable · pedido 5 del checkpoint»— y otro subtítulo `[M]`. O sea que
   se escribió o se editó a mano, y la regla del repositorio —el markdown es la fuente de verdad
   y el HTML sólo la vista de lectura— no se cumple en ese par. **No se regeneró a propósito:**
   regenerarlo borraría esa cabecera, que puede ser deliberada. Hay que decidir cuál de los dos
   manda antes de tocarlo `[?]`. Los otros tres pares `.md`/`.html` de `entregables/` sí
   reproducen desde el conversor, verificado.

9. **La compuerta de alertas no distingue «se tamizó y no hay» de «no se tamizó».** `R2` dejó
   `alertas.exigir_decidida()` llamada desde `ranking.region_recomendada()`, que es el único punto
   del port donde una región se vuelve recomendación (D69). Lo que esa compuerta **no** puede
   hacer cumplir es que la región haya sido evaluada: una región que no tiene ninguna fila en
   `research/ola4/M6_alertas/resultados/alertas.tsv` pasa como «sin alertas en este umbral», y eso
   es correcto para una región tamizada sin aciertos y falso para una que nunca se tamizó. Lo que
   queda protegido, entonces, son las **doce** regiones del inventario de `M6` y no una propuesta
   nueva; el caso concreto es el ranking a 22 nt, cuyas seis regiones recomendadas
   —`MP_MRFV` 162-361, `CP_MRFV` 77-276, `BicC_Dm` 2119-2418, `ATPaseD_Dm` 71-370, `eth_Dm`
   193-392 y `bursA_Dm` 44-243, en `research/ola3/C7_ranking_v2/resultados/ranking_v2.json`— no
   están en el inventario y hoy pasan la compuerta sin que nadie haya tamizado sus alertas `[M]`.
   Cerrarlo pide exigir que la región esté en el inventario antes de recomendarla, y eso haría
   fallar una corrida cuyo resultado está publicado (el `jaccard_21_22` de C7), así que **no se
   hizo por cuenta propia**: es una decisión del equipo, y el costo de no tomarla es que la
   compuerta protege lo evaluado y no lo nuevo `[?]`.
10. **El último eslabón entre el cómputo y lo publicado sigue siendo una persona.** Los documentos
   de `entregables/` son Markdown escrito a mano: no hay código que los genere, así que no hay
   punto de generación donde poner una compuerta. `R2` se cumplió en el port —que es donde se
   produce la recomendación— pero una cifra copiada a mano a un entregable no pasa por ninguna
   verificación automática, y eso es exactamente el modo de fallar que los commits del 26 y 27 de
   octubre vinieron corrigiendo tres veces `[H]`. Si se quiere cerrar, lo que hace falta es que la
   recomendación publicada salga de un generador, no de una copia.

### Ola 6, cierre de `O2` (2026-10-27)

11. **Se cierra la entrada 5 de esta seccion, y de la entrada 1 de la ola 5 la parte de la
    secuencia.** La subunidad B esta recuperada por homologia local: los tres transcriptomas
    publicos **si la contienen** —dos de ellos entera, al 100 % de identidad sobre las 500
    posiciones— y el genoma `ihDalMaid1.1` tiene su locus en el cromosoma 2 con el CDS verificado
    `[M]`. Ver `D71` y `research/ola6/O2_vatpase_b/REPORT.md`. El zip del investigador sigue
    valiendo, pero como **verificacion** del CDS y no como condicion para arrancar `O3`.
12. **La entrada 6 de esta seccion vale para una maquina y no para la otra, y eso hay que decirlo
    al asignar.** En la maquina de Luca hay `miniprot` 0.18-r281 compilado en WSL
    (`~/yhat/tools/miniprot/`), el ensamblado `ihDalMaid1.1` con su indice `genome.mpi` ya
    construido y los transcriptomas RefSeq de dos cicadelidos parientes en `~/yhat/data/` `[M]`.
    Lo que sigue faltando en las dos es **ViennaRNA y BLAST+**, que es lo que todavia frena `O3`
    y `F1`. La regla de no confundir «no pude buscar» con «no esta» necesita, para aplicarse, que
    cada entrada de entorno diga **en que maquina** se verifico.
13. **Las tres posiciones en que difieren los dos CDS de `V-ATPase B`.** El CDS del genoma y el
    del transcriptoma de Pergamino coinciden en 1.500 de 1.503 nucleotidos y codifican la misma
    proteina; las tres diferencias estan en las posiciones 615, 678 y 1254 del CDS y son
    sinonimas `[M]`. No se puede distinguir en esta pasada variacion entre poblaciones de un
    error de ensamblado en cualquiera de los dos `[?]`. Para la proteina da lo mismo, pero **una
    ventana de 21 nt que caiga sobre una de las tres tiene veredicto dependiente de cual CDS se
    use**, y al disenar sobre este gen hay que mirarlo.
14. **Cuantas copias del gen tiene el genoma.** La vuelta del reciproco devuelve, en los dos
    parientes, pares de transcriptos de la **misma** subunidad para A y D, y `GITV01` devuelve
    dos contigs con la proteina completa de B. Parece redundancia de ensamblado, pero el numero
    de copias no se midio y con una pasada de alineamiento no se decide `[?]`.

### Ola 6, cierre de `R7` (2026-10-27)

15. **Se cierra la entrada 9 de esta sección.** La compuerta ya distingue «se tamizó y no
    hay» de «no se tamizó»: `exigir_decidida()` exige presencia en el inventario de
    `research/ola4/M6_alertas/resultados/estado_regiones.tsv` y una región ausente levanta
    `RegionNoTamizada` (D72). Las seis regiones de k=22 entraron al inventario, así que lo
    protegido pasa de doce a dieciocho regiones `[M]`. La entrada 10 —el último eslabón
    entre el cómputo y lo publicado, que sigue siendo una persona copiando un número—
    **no** se cierra y no la toca nada de esto.
16. **La fila de `eth_Dm` 193-392 está sin firmar, y es lo que frena la corrida de 22 nt.**
    Tiene una coincidencia perfecta de 21 nt contra *Homalodisca vitripennis*
    (`LOC124369889`, quitinasa 2 probable, posición 347 del gen, transcriptos
    `XM_046828031.1` y `XM_046828033.1`) `[M]`. Hace falta que alguien del equipo la lea y
    la acepte o la bloquee con su argumento escrito, citando la fila, como `D48` pide y
    `D68` hizo con las diecisiete anteriores. Las otras tres filas nuevas con alertas sólo
    en el umbral laxo de `D28` —`MP_MRFV` 162-361, `BicC_Dm` 2119-2418 y `ATPaseD_Dm`
    71-370— **no** frenan nada en el umbral vigente, pero frenarían si alguna vez se
    adoptara `perfecto_ge19` `[M]`. Mientras `eth_Dm` 193-392 siga sin firma, una
    regeneración de `research/ola3/C7_ranking_v2/resultados/ranking_v2.json` no puede
    completarse: el valor publicado de `jaccard_21_22` está intacto y verificado, pero el
    generador no lo reproduce. **No se firmó por cuenta propia:** firmar es del equipo.
17. **Por qué correr la ventana de `eth_Dm` introduce un acierto perfecto, no se sabe.** La
    región vigente del gen, 114-313, tiene cero aciertos de 21/21; la propuesta a 22 nt,
    193-392, tiene uno `[M]`. Es un hecho sobre dónde cae la ventana, pero **si el acierto
    es una coincidencia de 21 nt sin consecuencia biológica o una región del gen que
    conviene evitar al diseñar, esta pasada no lo decide** `[?]`. Lo que haría falta es
    mirar si la quitinasa impactada tiene ortólogo en los no objetivo del panel y con qué
    conservación, que es trabajo de homología y no de coincidencia exacta.
18. **`work/sifi_v2/salida_k22` no está en esta máquina, y por eso la corrida de 22 nt no
    se pudo regenerar para verla frenarse.** Están los perfiles de ViennaRNA de k=21 y no
    los de k=22, así que `ranking_v2.py` se detendría en ese insumo faltante **antes** de
    llegar a la compuerta `[M]`. Lo que sí está medido es la compuerta en sí, llamada con
    las seis coordenadas publicadas de k=22 contra la tabla real. Siguiendo la regla que
    `D71` dejó: esto se verificó en la máquina de Joaquín (macOS, entorno conda
    `~/.claude-science/conda/envs/python`, Python 3.11.17, con `numpy`, `RNA` 2.7.2, `Bio`
    y —desde hoy— `ahocorasick` 2.3.1). En `/usr/bin/python3` (3.9.6) de la misma máquina
    faltan `RNA`, `Bio` y `ahocorasick`, así que la §6 de `test_alertas.py` ahí queda
    salteada y declarada. **Siguen faltando en las dos: BLAST+.**

### Ola 6, firma de `eth_Dm` 193-392 (2026-10-27)

19. **Se cierra la entrada 16: la fila está firmada.** `eth_Dm` 193-392 / *H. vitripennis* /
    `LOC124369889` quedó **`bloqueante` con la exposición de *H. vitripennis* como
    condición escrita** (`D73`). La compuerta pasa a 18 de 18 en el umbral literal de
    `D48`, con cuatro bloqueantes y ninguna vigente `[M]`. Las otras cinco filas de las
    regiones de 22 nt siguen en «pendiente» y sólo obligarían si se adoptara
    `perfecto_ge19`; no son urgentes y están declaradas.
20. **Una región bloqueante que el ranking recomienda igual, y nadie la descarta.** Es
    nuevo y es consecuencia de la firma. `ranking.region_recomendada()` **devuelve**
    `eth_Dm` 193-392 aunque esté firmada bloqueante —verificado, devuelve `(193, 392)`—
    porque `D69` decidió que bloquear es decidir y que descartar es del que llama `[M]`.
    Hasta hoy esa decisión no tenía filo: las tres bloqueantes de `D68` no las recomienda
    ninguna corrida, así que nunca se ejerció sobre una recomendación real. Ahora sí.
    El modo de fallar se corrió un casillero: de «se recomienda una región cuya alerta
    nadie leyó» a «se recomienda una región que alguien leyó **y bloqueó**» `[H]`. Las
    salidas posibles son tres y ninguna es obvia: que `region_recomendada()` se niegue a
    devolver una región bloqueante —pero eso cambia `D69` y además una bloqueante
    condicional no es lo mismo que una llana—; que devuelva la región **con su estado**,
    de modo que ignorarlo sea explícito; o que el descarte viva en quien consume la
    recomendación, que es lo que `D69` decidió y que hoy no tiene ningún código detrás.
    Es una decisión del equipo y **no se tocó** al firmar.
21. **Si la quitinasa impactada tiene ortólogo en los demás no objetivo del panel, no se
    sabe.** Issue **#32**. La firma de `D73` no lo afirma ni lo niega. Es trabajo de homología y no de
    coincidencia exacta, y **esta máquina no tiene ningún alineador**: verificado con
    `command -v`, faltan `blastn`, `tblastn`, `makeblastdb`, `miniprot`, `diamond`,
    `bowtie` y `bowtie2` `[M]`. En la máquina de Luca hay `miniprot` 0.18-r281 (`D71`),
    así que la pasada se puede asignar ahí. Es lo que decidiría si el acierto es una
    coincidencia de 21 nt sin consecuencia o una zona del gen que conviene evitar `[?]`.
22. **`work/sifi_v2/salida_k22` y las matrices de off-target de 22 nt se pueden generar en
    esta máquina, y antes no.** Lo que faltaba era `pyahocorasick`, que se instaló con
    `R7`. El perfil de eficiencia sale de `run_sifi.py --sirna-size 22 --backend vienna`,
    que usa el módulo `RNA` de ViennaRNA 2.7.2 —presente en el entorno conda— y las
    matrices de `offtarget_k22` y `offtarget_dm_k22` salen de `offtarget_21nt.py --size 22`
    contra las referencias de `work/W5/ref/`, que están en disco `[M]`. La receta exacta
    está en `research/ola3/C7_ranking_v2/REPORT.md` §9. **No se hizo, y no debería hacerse
    sin decisión escrita:** regenerar eso habilita regenerar
    `research/ola3/C7_ranking_v2/resultados/ranking_v2.json`, que es un archivo publicado,
    y además es la línea `C7` de la ola 3 y no `M6`. Merece su propio issue y su propio
    ADR, sobre todo porque la corrida que se regeneraría ahora incluye una región firmada
    bloqueante (entrada 20).

### Ola 6, cierre de las entradas 20 y 22 (2026-10-27)

23. **Se cierran las entradas 20 y 22.** El estado de alertas viaja con la región
    recomendada (`ranking.Region`, con `estado` y `bloqueante`) y el JSON de `C7` lo
    publica como `estado_alertas_recomendadas` y `recomendadas_bloqueantes`; la corrida de
    22 nt está regenerada, con sus tres insumos construidos en esta máquina (`D75`).
    Ninguna cifra publicada se movió: el JSON es idéntico valor por valor y sólo agrega
    esas dos claves por bloque `[M]`. La entrada 21 **sigue abierta** y pasó a ser el
    issue `R8` (#32), porque necesita un alineador y esta máquina no tiene ninguno.
24. **Una región publicada más que nadie había tamizado, y la encontró la compuerta.**
    Lo que queda por hacer está en el issue **#35**, parte 2.
    `BicC_Dm` 2123-2422 hizo fallar la primera regeneración de `ranking_v2.json` con
    `RegionNoTamizada` `[M]`. Sale del bloque `efecto_humano` —la corrida con la referencia
    humana fuera del panel— y está publicada en
    `efecto_humano.fichas.sin_humano_recomendada` y en `regiones_recomendadas_w7`. Ya entró
    al inventario, que pasa a **diecinueve** regiones, y sus tres filas no tienen 21/21, así
    que no frenan nada. **Lo que queda abierto es la lección, no el caso:** `D70` y el issue
    de `R7` buscaron las regiones sin tamizar mirando `regiones_recomendadas` de las dos
    corridas, y esta no estaba ahí. `[H]` No sabemos si hay más regiones publicadas que
    salgan de otros bloques de otros generadores y que nadie haya tamizado; la forma de
    saberlo no es buscarlas a mano otra vez sino que la compuerta las encuentre, que es lo
    que acaba de pasar. Mientras cada generador no se corra de punta a punta, no hay garantía.
25. **~~`ranking_v2.json` no es byte-reproducible~~ — RESUELTA por `D76` (issue #34), con una
    corrección al planteo.** El orden de las claves dentro de `riesgo_por_referencia` lo
    heredaba del orden en que se pasaron las referencias a `offtarget_21nt.py`, que no estaba
    registrado en ninguna parte. Ahora lo fija `ranking.por_referencia_ordenado()` al escribir,
    con el orden del panel y el vector al final. **Lo que el planteo tenía mal:** la salida (a)
    no costaba otro diff grande. El `ranking_v2.json` publicado **ya estaba** en el orden del
    panel —36 de 36 objetos, cero fuera de orden— porque `625f128` ya había pagado el
    reordenamiento, y reescribirlo con el orden canónico devuelve el archivo **byte a byte
    idéntico** `[M]`. El que no estaba era `research/ola2/W7_ranking/ranking.json`, 4 de 4
    fuera de orden, que se alineó en el mismo commit: 30 líneas movidas, ninguna cifra `[M]`.
    Queda `tools/verificacion/comparar_json.py` para revisar la próxima regeneración por valor
    y no por texto. **Lo que sigue pendiente es la corrida de punta a punta**, que es el único
    criterio del issue que no se pudo cumplir: regenerar el archivo desde `work/sifi_v2/` y
    verificar que una segunda regeneración seguida da el mismo byte a byte. En esta máquina no
    existe `work/sifi_v2/` ni hay ViennaRNA, así que el generador no arranca. El comando, para
    donde los insumos estén:

    ```
    python tools\sifi21_port\ranking_v2.py --trabajo work\sifi_v2 --json research\ola3\C7_ranking_v2\resultados\ranking_v2.json
    python tools\verificacion\comparar_json.py research\ola3\C7_ranking_v2\resultados\ranking_v2.json <copia_previa.json>
    ```

    Lo esperado es «idénticos valor por valor, y con el mismo orden de claves» `[H]`.
26. **La compuerta no sabe qué referencias tiene el panel en cada corrida.** Issue **#35**,
    parte 1. Consulta la
    tabla de alertas completa, de modo que en la rama `sin_humano` de `efecto_humano` una
    región se evalúa contra filas de *Homo sapiens* que esa rama **excluyó** del panel
    `[?]`. Hoy no cambia ningún resultado —ninguna de las filas en juego en esa rama tiene
    coincidencia perfecta de 21 nt— pero es una inconsistencia real: una región podría
    quedar frenada por una alerta de un organismo que la corrida no está considerando. Si
    alguna vez una fila humana de esas regiones pasa a tener 21/21, esto empieza a importar.

### Ola 6, cierre de `O3` (2026-10-27)

> Estas siete entradas se publicaron numeradas **15 a 21**, que ya estaban
> usadas por las secciones de `R7` y de la firma de `eth_Dm`. Se renumeraron a **27 a
> 33** para que el archivo tenga una sola numeración. La equivalencia, por si alguien
> llega desde un commit o un informe que cita los números viejos: 15→27, 16→28, 17→29,
> 18→30, 19→31, 20→32, 21→33.


27. **Dónde caen los aciertos con un desapareo de las ventanas de juntura.**
    `02_juntura_detalle.py` localiza coincidencia exacta de 19 a 21 nt; de los aciertos con
    un desapareo tiene la cuenta del tamizado y no el bloque ni el transcripto `[?]`.
    Ubicarlos pide extender la auditoría al caso de un desapareo, que es la misma lógica
    con un autómata por posición de error.
28. **El ranking de regiones se sigue armando en el marco 1 y la cifra que se publica es la
    del marco 3.** Esto **no es un hallazgo de `O3`**: los tres marcos, sus nombres y la
    regla de que la cifra publicable es la de la molécula son `D63` y
    `research/ola5/N3_marcos/`. Lo que `O3` agrega es la séptima fila, con la misma
    herramienta y con las seis anclas reproducidas en la misma corrida: `V-ATPase B`
    517-816 da **15 / 15 / 14** `[M]`. Lo que queda abierto es lo que `D63` ya decía: **un
    ranking armado en el marco 1 no es el ranking de las moléculas**, y rehacer la elección
    en el marco 3 cambiaría el orden de las 1.184 candidatas y no se midió `[?]`. Vecino
    del issue #20 y no se adelanta acá.
29. **Si conviene testear las dos mitades por separado antes de la quimera.** Silenciando
    dos genes a la vez, un bioensayo negativo no dice cuál mitad falló. Dos datos vuelven la
    pregunta concreta: la mitad de `V-ATPase B` aporta 14 ventanas eficientes contra 26 de
    `BicC_Dm`, y su región es **la única admisible del gen** `[M]`, así que si el efecto de
    movilidad y mortalidad depende de esa mitad, la molécula apuesta a la parte más
    restringida del diseño `[H]`. Es una pregunta para el investigador y la contesta un
    experimento.
30. **Si la región candidata de `V-ATPase B` entra al inventario de alertas.** Issue **#35**,
    parte 3. Hoy no tiene
    fila en las de `M6`, y desde `D72` la compuerta la **rechaza** con
    `alertas.RegionNoTamizada` en vez de dejarla pasar. Son siete regiones nuevas a tamizar
    contando las seis de 22 nt, no una.
31. **Las junturas no tienen lugar en el inventario de `M6`.** Issue **#35**, parte 3. El generador tamiza
    **regiones**, y una juntura no es una región de ningún gen: es secuencia que fabrica el
    ensamblado. La fila de alerta de `O3` está escrita con el esquema de columnas de `M6`
    para que se pueda pegar, pero nadie la pegó, y mientras no se integre una quimera puede
    pasar la compuerta con su empalme sin tamizar `[?]`.
32. **`ranking.py ranking` no termina desde `D72`.** La compuerta dispara dentro de
    `cmd_ranking` y aborta con `RegionNoTamizada` porque la cascada elige para `BicC_Dm` la
    región 2123-2422, que no está entre las 18 del inventario `[M]`. El mensaje de error
    dice cómo arreglarlo —agregarla a `REGIONES` en `tabla_alertas.py` y correr el script—
    pero hasta que alguien lo haga, el comando que regenera el ranking no corre. Es de la
    línea del issue #30 y `O3` no lo tocó porque toca números publicados.
33. **El panel de `work/sifi_check/` estaba incompleto y nadie lo había notado.** El
    tamizado que vivía ahí se había corrido con cinco referencias más el genoma del vector,
    **sin la humana**, y por eso dos de los cuatro `buenos_limpios` del nivel 3 de `C7` no
    se reproducían. Regenerado con las seis, los cuatro dan exacto `[M]`. Queda la pregunta
    de **qué otros números del repositorio se calcularon con el insumo incompleto**: `C6` y
    `C7` tienen la humana en sus propias salidas, pero cualquier corrida posterior que haya
    leído `work/sifi_check/offtarget_full/` sin regenerarlo arrastra el faltante `[?]`.
    `work/` no se versiona, así que esto no se puede auditar desde git.

### Ola 6, `ranking.py ranking` vuelto a correr (2026-10-27)

34. **Se cierra la entrada 32: `ranking.py ranking` termina, y hacían falta las dos cosas.**
    Los insumos que faltaban no había que conseguirlos de ningún lado, se generaron acá:
    `work/sifi_check/salida/` con el criterio de `research/ola3/C7_ranking_v2/scripts/perfil_k.py`
    —corregido, ViennaRNA 2.7.2, 21 nt, los cuatro genes de EPILAB; los conteos de eficientes
    dan 1243/123, 508/30, 2500/171 y 471/29, idénticos a los de `work/sifi_v2/salida_k21`
    `[M]`— y `work/sifi_check/offtarget_full/` con `offtarget_21nt.py --size 21 --mm1`. El
    comando **sale con 0** `[M]`.
    Hubo **dos** causas y las dos había que arreglarlas. La primera es la que reporta la
    entrada 32 y la resolvió `D75`: la cascada elige `BicC_Dm` **2123-2422**, que no estaba
    en el inventario. **La entrada 32 tenía razón** —ver la entrada 35, donde esto se midió
    con cuidado porque en una primera pasada pareció lo contrario—. La segunda **no tiene
    nada que ver con `D72`**: el subparser `ranking` nunca declaró `--json`, mientras
    `cmd_ranking` termina con `if a.json:`, así que el comando corría entero, imprimía los
    tres niveles y los barridos y recién al final moría con `AttributeError`. Está desde el
    commit de `C1`, `478f165` del 2026-10-20 `[M]`: ese comando **nunca** había terminado.
    Se agregó la opción que faltaba.
35. **Los dos juegos de anclas publicadas piden paneles distintos, y no se pueden satisfacer
    con el mismo archivo.** Issue **#33**, con las tres salidas posibles escritas. Esto es lo que la entrada 33 dejó planteado, ahora medido por los
    dos lados. `work/sifi_check/offtarget_full/` se construyó de las dos maneras `[M]`:

    | | panel de W7 (cinco referencias + genoma del vector) | con la humana (seis + genoma) |
    | --- | --- | --- |
    | ancla §4 de `test_ranking.py` | **pasa**: 6 / 0 / 33 / **7** | **falla**: `ATPaseD_Dm` da **11** y no 7 |
    | `test_ranking.py` entero | **46 de 46, sin ninguna salteada** | 1 falla |
    | la cascada elige para `BicC_Dm` | **2123-2422** | 2121-2420 |
    | `buenos_limpios` del nivel 3 contra `C7` k=21 | 37, **21**, **36**, **19** | **37, 20, 34, 17: los cuatro exactos** |

    O sea: con la humana reproducen las cifras de `C7` y se rompe el ancla de `§4`; sin la
    humana pasa todo `test_ranking.py` y no reproducen tres de las cuatro de `C7`. Las dos
    cifras están publicadas y **se contradicen** `[?]`. En disco quedó el archivo **sin la
    humana**, porque es el que hace pasar la batería de pruebas del repositorio, y porque
    cambiar las cifras de `§4` sería mover números publicados sin decisión escrita. La
    diferencia es de **una sola** de las cuatro regiones y de cuatro ventanas: las de
    `ATPaseD_Dm` 151-450 que dan en la referencia humana. **Es decisión del equipo cuál de
    los dos paneles es el correcto para este archivo**, y mientras no se tome, cualquier
    número que salga de `work/sifi_check/` hay que leerlo diciendo con qué panel se corrió.
36. **Una lección sobre cómo leer un `RegionNoTamizada`, que casi me lleva a la conclusión
    equivocada.** En la primera pasada, con el archivo que incluía la humana, la cascada
    elegía 2121-2420 —que ya estaba en el inventario— y parecía que la entrada 32 se
    explicaba sola por el panel incompleto y que agregar 2123-2422 había sido innecesario.
    Es al revés: con el panel que el repositorio verifica, 2123-2422 **es** la región que la
    cascada pide, y sin ella en el inventario el comando no corre. `[H]` Lo que falla cuando
    el insumo está mal no es la compuerta: la compuerta señala con precisión una región real
    que nadie tamizó. Pero **qué región señala depende del insumo**, así que un
    `RegionNoTamizada` hay que leerlo junto con el panel con el que se corrió.

### Nota de numeración (2026-10-27, arreglada)

Las dos líneas numeraron en paralelo y la sección de `O3` se publicó con los números **15 a
21**, que ya usaban las secciones de `R7` y de la firma de `eth_Dm`. **Quedó arreglado:** esas
siete entradas son ahora **27 a 33** y la sección se movió detrás de la de las entradas 20 y
22, de modo que el archivo tiene una sola numeración y asciende. La equivalencia, por si
alguien llega desde un commit o un informe que cita los números viejos, está al principio de
esa sección: 15→27, 16→28, 17→29, 18→30, 19→31, 20→32, 21→33.

### Ola 6, cierre de la entrada 25 (`D76`, issue #34, 2026-10-27)

37. **Una referencia que no está en el panel entra a la salida como `D_maidis` y choca con
    el vector, en silencio.** Salió al probar `D76` a través de los escritores de verdad.
    `ranking.corto()` dobla **toda** referencia que no esté en `REFERENCIAS` al nombre corto
    del vector, así que una columna del TSV de off-targets de una referencia que el panel no
    tiene no levanta nada: se escribe bajo la clave `D_maidis` y la última que escribe gana,
    de modo que **cuál gana depende del orden de las columnas del TSV** `[M]`
    (`tools/sifi21_port/test_orden_salida.py`, tercera prueba: con una intrusa y el vector en
    la misma matriz, la salida queda con `maiz` y `D_maidis` y de la intrusa no queda rastro).
    Es la misma clase de problema que `D76` cerró para el orden de las claves, en un lugar
    donde sigue abierto. La guarda `KeyError` de `por_referencia_ordenado()` **no lo alcanza**,
    porque la colisión ocurre antes de que la vea. `[H]` Hoy no mueve ninguna cifra publicada:
    las corridas publicadas usan el panel de siete referencias y sus matrices tienen
    exactamente esas columnas, así que no hay intrusa posible. Pero no hay nada que lo impida
    si alguna vez una matriz se construye con una referencia de más. **No se hizo:** arreglarlo
    es cambiar `corto()` para que distinga «el vector» de «no la conozco», y eso toca el
    linaje de `ranking.py` entero, no el formato de salida de `C7`. La pregunta es si `corto()`
    debe fallar ante una referencia desconocida o devolver un centinela propio.

### Ola 6, cierre de `R11` (issue #35, 2026-10-27)

38. **Se cierra la entrada 26: la compuerta sabe contra que panel se le pregunta, y una
    alerta de fuera del panel frena igual.** `D77`. `exigir_decidida()` y
    `estado_decision()` toman el panel de la corrida, lo publican en el estado
    (`panel`, `organismos_fuera_del_panel`, `pendientes_fuera_del_panel`) y lo nombran en el
    mensaje de `AlertaSinDecidir`, pero **no filtran**: la coincidencia perfecta esta en el
    ARN y no en el panel con el que una corrida lo puntua.
    `ranking.region_recomendada()` lo resuelve solo con `ranking.panel_actual()`, que lee el
    `REFERENCIAS` vivo, asi que la rama `sin_humano` de `efecto_humano()` queda declarada sin
    que nadie se acuerde de pasarlo. La prueba que pedia el issue —la misma region, el mismo
    umbral, con y sin el organismo en el panel— es la seccion 10 de `test_alertas.py` y frena
    las dos veces en los dos umbrales de `D28` `[M]`. Ninguna cifra publicada se mueve: lo
    unico que cambia en disco es `research/ola4/M6_alertas/resultados/compuerta.json`, que
    gana tres claves informativas en sus 38 bloques `[M]`.
    **Nota, por la entrada 37:** `panel_actual()` arma el panel desde `REFERENCIAS` y agrega
    `D_maidis` a mano, sin pasar por `corto()`, asi que la colision que esa entrada describe
    no lo alcanza. Son dos problemas vecinos y distintos, y el de la 37 sigue abierto.
39. **De la entrada 24 queda abierta la corrida, no la cobertura: esta medida.** La leccion
    era que buscar a mano no alcanza. Esta pasada no busco a mano: barrio los **409** JSON de
    `research/` —salteando otro proyecto y su propia salida—, recogio toda cadena con forma de
    region, la clasifico por gen y cruzo contra `estado_regiones.tsv`
    (`research/ola6/R11_compuerta_y_panel/scripts/regiones_publicadas.py`). **Trece** archivos
    traen coordenadas de los genes del panel: 407 coordenadas, **60** pares (gen, region) y
    **41** fuera del inventario `[M]`. Lo que importa es de que bloque sale cada una, y ahi el
    resultado es limpio: los 41 salen **todos** de bloques que no producen recomendaciones
    —orden de alternativas, region de maximo conteo de un nulo, region por defecto de un
    barrido de sensibilidad en `C9` y `C3`, y la candidata de `V-ATPase B`— y en los bloques
    que **si** recomiendan no hay **una sola** coordenada fuera del inventario `[M]`. Y el
    censo estatico de caminos (`censo_generadores.py`) da que de los siete archivos del
    repositorio con marcas de generador, **uno solo** llama a `alternativas()` sin llamar a la
    compuerta, y es a proposito (`01_region_vatpase_b.py`, `D74`) `[M]`. `[H]` O sea que el
    conjunto de lugares donde una region puede nacer es cerrado y conocido, y lo que falta
    para la garantia fuerte es correr cada generador, no seguir buscando.
    **Nota de metodo:** la primera version de ese script tenia los archivos escritos a mano
    —tres— y decia «los tres publicados»; era el mismo error de esta entrada un piso mas
    abajo, y lo encontro la revision de esta pasada. Por eso barre.
40. **Lo que falta de la entrada 24 es `work/`, y se puede pedir.** De los ocho generadores
    declarados corrieron **dos** en la maquina de Luca, y son justamente los dos que no
    pueden encontrar nada nuevo: `compuerta.py` y `umbral_compuerta.py` iteran sobre el
    inventario `[M]`. Los otros seis mueren en el primer insumo de `work/`, que en esta
    maquina **no existe** —verificado con `ls work/` y tambien en WSL, donde hay
    `~/yhat/tools` y `~/yhat/data` pero no una copia del repositorio— `[M]`. El comando exacto
    de cada uno esta en `research/ola6/R11_compuerta_y_panel/resultados/censo_corridas.tsv` y
    la lista de lo que hay que pedir, en `PENDIENTE.md` del mismo bloque. **Al pedir
    `work/sifi_check/`, decir con que panel se construyo:** el issue #33 tiene abierto que los
    dos juegos de anclas publicadas piden paneles distintos.
41. **Se cierran las entradas 30 y 31 en lo que eran —decisiones— y queda el insumo.** `D78`:
    `V-ATPase B` 517-816 entra al inventario como una region mas, y las junturas entran con
    clave propia, `(quimera <nombre>, "juntura")`, con granularidad quimera x organismo x gen
    impactado y con los `j` fuera de la clave. Entran **las dos** quimeras, incluida
    `Q_BicC_Dm__VATPaseB_Dm`, que fabrica cero bloques: es la distincion que `D72` existe para
    hacer `[M]`. **No se implemento ninguna de las dos** y el motivo es de insumo, no de
    criterio: `tabla_alertas.py` necesita `work/m6_alertas/identidad_por_ventana.tsv` y
    `work/W5/ref/`, y la region de `V-ATPase B` ademas necesita su matriz de off-target contra
    el panel, que no existe porque el gen no esta entre los seis que el generador tamiza.
    Agregar las entradas sin poder correr el script dejaria la tabla y el inventario
    describiendo algo que el generador ya no produce. Mientras tanto sigue siendo cierto que
    **una quimera puede pasar la compuerta con su empalme sin tamizar** `[?]`.
42. **Una coordenada publicada que no es una recomendacion se ve igual que una que si, y de
    las 41 no se sabe si alguna tiene 21/21.** Es nuevo y sale de contar. Los 41 pares sin
    tamizar son ordenes de alternativas, regiones de maximo conteo de los nulos y regiones por
    defecto de barridos de sensibilidad, y ninguno pretende ser usable; pero estan publicados
    con la misma forma `ini-fin` que una recomendacion y lo unico que hoy los distingue es el
    bloque del JSON en el que aparecen `[M]`. **Su estado de 21/21 es desconocido**, y no se
    puede afirmar que no lo tengan: medirlo es tamizarlos, que es exactamente lo que no esta
    hecho `[?]`. `[H]` Si alguna vez alguien copia una alternativa a un documento, no hay nada
    que lo frene: la compuerta protege el punto donde una region **se vuelve recomendacion**, y
    una coordenada leida de `alternativas` no pasa por ahi. Es la entrada 10 de esta ola vista
    desde el otro lado, y la salida posible —marcar en el propio JSON que una coordenada es un
    orden y no una recomendacion— es formato de salida de `C7`, no de `M6`. **No se hizo.**
43. **El censo cubre generadores, no documentos.** `censo_generadores.py` busca marcas en el
    codigo, asi que una region publicada como texto ya calculado en un `REPORT.md` o en un TSV
    escrito a mano no tiene ninguna marca y el censo no la ve `[?]`. No es una laguna del
    censo sino el limite de lo que se puede verificar desde el codigo, y es la misma de la
    entrada 10: entre el cometido del port y el numero que aparece en un documento de
    `entregables/` hay una persona copiandolo.

### Ola 6, cierre de `R6` (2026-10-27)

44. **Qué forma de agregación se publica como la lista ordenada.** Issue **#20** cerró cómo se
    reporta el tercer puesto (`D80`: empate declarado, con los dos órdenes y la decisión que los
    separa), pero **no** cuál de las formas —geométrica, suma o cascada, en escala absoluta o
    min-max— es la lista que se publica con orden. Es la decisión abierta de la parte B.2 de
    `entregables/para-el-investigador.md`, anterior a `M5`, y pesa: en la cascada con exposición
    cero el orden de los seis cambia entero, y en la forma geométrica el mismo par no se mueve
    `[M]` (`research/ola4/M5_dos_ejes/`). Hasta decidirla, cada orden que se cite lleva su forma
    de agregación al lado `[?]`.
45. **Si la pregunta que manda para elegir región es la molécula sintetizada o la accesibilidad en
    el blanco.** `D79` conserva 26 (molécula, marco 3) como la cifra publicada y declara 29 (marco
    2) al lado. Lo que lo haría reabrir es una respuesta del laboratorio sobre en qué marco
    cuenta su planilla (pregunta 4 de `entregables/recomendacion-defendida.md` §7) o una decisión
    del equipo de privilegiar la accesibilidad en el transcrito `[?]`. Si el laboratorio cuenta en
    contexto, la comparación contra sus cifras se hace en **su** marco y la publicada no cambia.

### Ola 6, cierre de `O4` (issue #24, 2026-10-27)

46. **El eje de riesgo se evalúa en el marco 1, donde veinte ventanas por región no existen
    en la molécula.** Es el complemento de las entradas 28 y 45, que ya dejaron planteado que un
    ranking armado en marco 1 no es el ranking de las moléculas: eso es sobre el eje de
    **eficacia** y está declarado desde `D63`. Lo que ninguna de las dos cubre es que
    `ranking.ejes()` calcula también el **veto** sobre el tramo del marco 1, así que una
    región puede quedar vetada por un 21-mero que la molécula **no contiene**. Medido, con
    el caso concreto: en `V-ATPase B` la ubicación 232-531 de 300 nt tiene **cero** ventanas
    vetadas entre las 280 que existen en la molécula, y en marco 1 la vetan las ventanas
    **514, 515 y 516**, cuyos 21-meros terminan en los nucleótidos 534-536 —afuera de una
    molécula que llega hasta el 531— y la referencia que las veta es la **humana** `[M]`. Por
    eso `D74` encuentra **una** región admisible de «300 nt» y la lectura en marco 2
    encuentra **24**, más 22 de 301 nt `[M]`; la cláusula de `D74` «ocupa el único hueco
    libre de 300 ventanas consecutivas» es exacta y las otras tres cifras de esa misma
    oración son la misma medición leída en la otra unidad.
    **La dirección del error es la tranquilizadora:** evaluar el riesgo en marco 1 descarta
    de más, porque veta por ventanas que no van a existir. No se parece al faltante de la
    referencia humana, que fallaba optimista. Ninguna cifra publicada queda insegura por
    esto; lo que cambia es **cuántas opciones cree tener el proyecto**. Y **la quimera que
    `O3` midió no se mueve:** su fragmento son los nt 517-816, ventanas 517-796, limpio en
    los dos marcos `[M]`.
    Quedan dos cosas, de tamaños distintos. La chica: la oración de `D74` es una afirmación
    de marco 1 escrita en lenguaje de nucleótidos, y corregir la redacción no mueve nada
    medido. La grande: `[?]` si el eje de riesgo debería leerse en marco 2 —el de los
    21-meros que la molécula tiene—, porque si se adoptara, la elección de región en
    `V-ATPase B` se reabre con 24 ubicaciones en vez de una y eso mueve una afirmación
    publicada, «la única región admisible del gen», sin mover ningún conteo. Vecina del
    issue #20, y acá no se adelanta.
    **Una nota sobre cómo se encontró, que es la parte reusable:** la primera versión de esta
    entrada afirmaba que la unidad del largo de región no estaba declarada en ninguna parte,
    y era falso —`D63` la declara, `N3` le puso nombre a los marcos y hay fila de glosario
    que se llama «marco de conteo»—. Mis conteos reproducían `N3` celda por celda, o sea que
    era un ancla pasando y la leí como hallazgo. Busqué «unidad de conteo», que es como lo
    llamó `M1`, y el proyecto le dice «marco»: antes de declarar que algo no está declarado
    hay que abrir el REPORT del bloque que mide ese eje.
47. **Cuál es el mínimo de largo por gen que tiene sentido en una quimera.** Es el agujero
    que dejó ver el objetivo declarado de `D81`, y es biológico, no de código. El mejor
    conteo de ventanas heredadas **crece con la asimetría**: con largo total 600 el máximo es
    64 con un corte de 500 + 100 y cae a 49 en las proporciones equilibradas de 250 a 350
    `[M]`. Así que `cobertura_fenotipica`, tal como está escrito, premia darle casi todo el
    largo al gen de perfil más denso —`BicC_Dm`— y dejar el fenotipo de movilidad en 100 nt,
    que es lo contrario de para qué `D67` quiere una quimera. `[H]` El parámetro que lo
    arregla es un mínimo por gen, pero fijarlo pide saber **cuánto ARNdc de un gen hace falta
    para silenciarlo**, que es dato de bioensayo y no de nuestro cómputo: el catálogo de `C5`
    registra dosis por insecto, no largo mínimo de disparador. Es pregunta para el
    investigador y la contesta un experimento.
48. **La grilla fina no se corrió, y no sabemos si mueve el primer puesto.** La corrida
    publicada usa `--paso 50` con la retícula anclada a las islas, que da 3.204 combinaciones
    y 3.405 plegados. Con `--paso 1` la misma grilla pide **136.446** plegados `[M]`, que
    entran en unas horas de esta máquina pero exceden el tope declarado de 5.000, así que la
    corrida se detuvo y lo dijo en vez de muestrear. `[?]` Lo que no se puede afirmar es que
    el primer puesto de la grilla gruesa sea el de la fina: el paso engruesa los tres
    parámetros libres a la vez, y el hallazgo de las islas angostas —la de `V-ATPase B` mide
    21 nt y la retícula de paso 50 no la tocaba— muestra que el paso puede esconder
    exactamente lo que importa. Conviene correrla recién cuando el mínimo por gen de la
    entrada 47 esté fijado, porque ese mínimo recorta la grilla.
49. **Los aciertos con un desapareo del empalme no están localizados.** El tamizado de
    juntura de `O4` busca bloques **exactos** de 19, 20 y 21 nt que cruzan la unión, que es
    lo que permite afirmar que un bloque es fabricado y no heredado; `mm1_21` queda fuera,
    porque un desapareo no tiene bloque contiguo que localizar — es la misma limitación que
    declaró el paso 2 de `O3` y es vecina de la entrada 27. `[?]` Entonces no sabemos si
    alguna de las 3.204 combinaciones fabrica una coincidencia con un desapareo que el
    conteo exacto no ve, ni en qué dirección eso movería el orden bajo `riesgo_minimo`.
    `[H]` Y hay una lectura que sí se puede hacer con lo exacto, y conviene no perderla: de
    las 515 combinaciones que fabrican algún bloque del panel, en **262 —la mitad— el bloque
    más repartido toma un solo nucleótido del segundo gen**, y sólo 118 tienen alguno
    repartido 5/5 o mejor `[M]`. Un bloque de 19 nt con 18 de un gen y 1 del otro existe por
    azar en una de cada cuatro referencias que contengan al gen padre, así que el conteo de
    alertas no se lee sin el aporte al lado.

### Ola 6, cierre de `R9` (`D83`, issue #33, 2026-10-27)

50. **Se cierra la entrada 35, y se cierra dándola vuelta: las dos tandas de cifras nunca
    compitieron por el mismo archivo.** La entrada 35 mide bien los dos lados y los lee como
    una contradicción entre cifras publicadas; no lo son. Son dos mediciones distintas, cada
    una con su panel declarado en su propio informe y **cada una con su propio directorio de
    trabajo**. El nivel 3 de `C7` nunca salió de `work/sifi_check/`: sale de `work/sifi_v2/`,
    con los comandos de `C7` §9, y ese directorio está completo en esta máquina. Regenerado
    hoy entero reproduce `research/ola3/C7_ranking_v2/resultados/ranking_v2.json` **idéntico
    valor por valor y con el mismo orden de claves** —`tools/verificacion/comparar_json.py`—
    y sus cuatro `buenos_limpios` del nivel 3 dan 37, 20, 34 y 17 exactos, con `BicC_Dm` en
    2121-2420 `[M]`. El panel de `work/sifi_check/offtarget_full/`, por su lado, tiene una
    prueba más dura que la prosa: reconstruido con el comando de `sifi21_reproduccion.md` §4
    reproduce **byte a byte** el `md5` que `tools/sifi21_port/README.md` publica desde el
    commit `478f165`, `a3229e733e4dc70c308c901583b4e4c3` `[M]`. Lo que estaba mal era el
    ancla C de `O3`, que pedía el nivel 3 de `C7` leyendo el directorio de otra línea; ahora
    lee `work/sifi_v2/` y **sus cuatro números esperados no se tocaron**. Con el archivo
    devuelto a su panel, `test_ranking.py` pasa 55 de 55 sin saltear ninguna, las tres anclas
    de `O3` pasan y `ranking.py ranking` sale con 0 — las tres cosas **a la vez**, que hasta
    hoy no había pasado `[M]`. Ninguna cifra publicada se movió.
51. **Se contesta la pregunta general de la entrada 33, y la respuesta es corta.** Quiénes
    leen `work/sifi_check/offtarget_full/`: las anclas de `test_ranking.py`, `ranking.py` por
    su valor por defecto —y a través de él `research/ola2/W7_ranking/ranking.json`—,
    `cruce.py`, `informe_html.py` y el ancla C de `O3`. Todos menos el último son de la
    línea `W5`/`W7` y por lo tanto del panel correcto por construcción: la referencia humana
    entra al proyecto recién en `C6`, que la puso en un directorio aparte
    (`offtarget_panel_nuevo/`), y `C7` armó el suyo desde cero en `work/sifi_v2/`. El único
    consumidor que leyó el directorio con la expectativa de otro panel era el ancla C, y es
    el que se corrigió. O sea que **ninguna otra salida del repositorio arrastra el
    faltante**, y la entrada 33 se cierra con eso `[M]`.
52. **La otra salida publicada que lee ese directorio también se regeneró, y tampoco se
    movió.** `research/ola2/W7_ranking/ranking.json` se rehízo de punta a punta con el
    comando de `W7` §«Cómo reproducirlo» —2.000 muestras, el `offtarget_full/` ya devuelto a
    su panel y los cuatro `work/sifi_check/offtarget_mm1_<gen>/`, que no estaban en esta
    máquina y se reconstruyeron en esta corrida con el mismo panel de §4— y
    `tools/verificacion/comparar_json.py` lo da **idéntico valor por valor y con el mismo
    orden de claves** contra el publicado `[M]`. Con eso quedan verificados los dos únicos
    archivos de resultados del repositorio que dependen de este insumo. Lo que **no** se
    pudo comprobar es el respaldo: `work/O3/respaldo/`, el directorio donde `O3` dice haber
    dejado los archivos de cinco referencias, **no existe** en esta máquina, así que
    `offtarget_full/` no se restauró sino que se **reconstruyó** —que es más fuerte, porque
    reproduce el `md5` publicado— pero significa que en otra máquina el respaldo puede estar
    o no estar `[?]`.
53. **Lo que sigue sin estar decidido, y no es de esta línea.** Si el panel de seis es el
    panel **correcto** para decidir una molécula es la pregunta de `C6` y sigue abierta;
    `D83` sólo dice cuál panel corresponde a cuál archivo. Y sigue abierto que la compuerta
    no sabe si el panel con el que se la llama es el adecuado para esa corrida, que es el
    límite que `D77` se puso a sí mismo.

### Ola 6, el entorno de la máquina de Joaquín, vuelto a medir (2026-10-27)

54. **Sí hay alineadores en esta máquina, y el hecho anotado que decía lo contrario estaba
    midiendo mal.** El índice de la ola 6 (issue #29) y el issue #25 (`F1`) registran, con
    `command -v`, que no hay `blastn`, `tblastn`, `makeblastdb`, `miniprot`, `diamond`,
    `bowtie` ni `bowtie2`, y sobre eso se decidió mandar `F1` y `R8` a otra máquina. **La
    medición era correcta y la conclusión no:** `command -v` mira el `PATH`, y las
    herramientas están instaladas en entornos de `micromamba` que no están activados. Hay
    **BLAST+ 2.17.0** (`blastn`, `blastp`, `blastx`, `tblastn`, `makeblastdb`) y **DIAMOND
    2.2.8** en `~/.claude-science/conda/envs/alineador/bin/`, **miniprot 0.18-r281** en
    `envs/bioinfo/bin/`, otro BLAST+ 2.17.0 completo en `envs/w5bio/bin/` y `bowtie` en
    `envs/w2tools/bin/` y `envs/c2sifi/bin/` `[M]`. No es que respondan `--version`: se
    corrió una prueba de verdad, `makeblastdb` sobre `work/sifi_check/BicC_Dm_full.fasta` y
    `tblastn` con `work/W5/ref/prot_BicC.faa` contra esa base, que devuelve alineamientos
    reales —`XP_001944274.2` a 46,8 % de identidad sobre 743 aminoácidos con *e*-valor 0,0, y
    `NP_723949.1` a 55,3 % sobre 360 con 2,6e-124— y `miniprot` sobre el mismo par devuelve
    seis líneas de salida `[M]`.
    `[H]` La consecuencia práctica es que **`F1` (#25) no está bloqueado por entorno en esta
    máquina**: tiene las dos piezas que el issue pide, un alineador de proteína contra
    nucleótido (`tblastn` y `miniprot`) y uno de proteína contra proteína para la ortología
    recíproca (`diamond`, `blastp`). Lo que falta para la primera corrida real es el
    transcriptoma del investigador. La etiqueta `necesita-entorno` del issue se deja puesta
    porque sigue siendo cierta para quien lo tome en otra máquina — por `D78`, en la de Luca
    no hay BLAST+ ni ViennaRNA. **[Corregido por la entrada 61: la cita es a `D71`, no a
    `D78`, y ViennaRNA sí está en el `python3` de WSL de esa máquina. BLAST+ sí falta.]**
    `[H]` Y la lección de método, que es hermana de la de `D83`: **`command -v` contesta «no
    está en el `PATH`», no «no está instalado»**, y la diferencia entre las dos cosas
    reasignó trabajo entre máquinas. Antes de declarar que una herramienta falta conviene
    mirar también los entornos de `micromamba`: `micromamba env list` y un `ls` de cada
    `bin/`.

### Ola 6, cierre de `F1` (`D84`, issue #25, 2026-10-27)

55. **¿Por qué 25.812 de los 56.117 contigs de `GITV01` (46,0 %) no tienen ningún ORF de ≥ 100 aa?**
    Sólo 1.071 miden menos de 300 nt, así que el tamaño no lo explica. Puede ser ruido no
    codificante, UTR, fragmentos o marcos rotos por errores de ensamblado. No se midió `[?]`.
56. **¿Aplican las bandas de concordancia de `C12` a ORF de un TSA?** Se midieron entre dos
    proteomas RefSeq completos y anotados; un ORF de un transcriptoma puede ser parcial, quimérico
    o con el marco corrido. `F1` las aplica por supuesto `[H]`, y el 81 % esperado de la lectura
    inclusiva vale sólo si el supuesto vale. Una validación posible: tomar un subconjunto de
    contigs cuyos genes tengan anotación independiente (los de la curación de `C5`).
57. **¿Cuál es la regla de empate correcta para un transcriptoma redundante?** La mitad de los ORF
    con hit queda en empate bajo la regla estricta, y el 46,3 % de los empates inversos no son copias
    idénticas. Falta saber si esos ORF son isoformas, parálogos o fragmentos del mismo gen. Una
    medida es agrupar los contigs por gen (`cd-hit` o equivalente) y repetir la reciprocidad entre
    grupos; no se hizo.
58. **Taxonomía de los dos proteomas de referencia, sin fuente abierta.** El preregistro dice que
    *Macrosteles* y *Dalbulus* son Deltocephalinae y *Homalodisca* un Cicadellinae. Para *Dalbulus* el
    catálogo de `C5` lo registra; para los otros dos no abrí ninguna fuente taxonómica. Queda
    pendiente antes de repetirlo en un entregable.
59. **¿Confirmación del investigador de que `GITV01` es lo que quería mandar?** El archivo es el TSA
    público de Ohio State, que el repositorio ya conocía; no se sabe si él lo eligió por eso o si el
    otro transcriptoma que mencionó es distinto. Pregunta para la próxima comunicación.
60. **`F2` necesita lo que `F1` no entrega.** Los términos GO, los dominios conservados y los papers
    no están en la salida de `F1` (sólo nombre de producto, identidad, cobertura y banda), y no hay
    ninguno versionado. Sin una fuente de esos tres, `F2` sólo puede resumir el nombre de producto.

### Ola 6, el entorno de la máquina de Luca, medido por primera vez (issue #29, 2026-10-27)

*Esta entrada se escribió como 55 y se renumeró a 61 al mergear: la sesión de `F1` escribió
55-60 el mismo día y ya estaban en `origin`. Mismo caso que `D85`.*

61. **En la máquina de Luca hay ViennaRNA, y la entrada 54 dice que no.** La entrada 54 cierra
    con «por `D78`, en la de Luca no hay BLAST+ ni ViennaRNA». Las dos mitades fallan. La cita
    es a la decisión equivocada: `D78` es la que mete `V-ATPase B` y las junturas al inventario,
    y la que habla de esta máquina es `D71`, que dice otra cosa —«vale para la máquina que se
    verificó y **no** para la de Luca, donde hay `miniprot` 0.18-r281 en WSL con el ensamblado
    indexado»—. `D71` **no menciona ViennaRNA en ningún lado**; de BLAST+ sí habla, pero para
    decir que faltaba **en la máquina del issue**, que es la otra. Y la mitad de ViennaRNA
    tampoco se sostiene: aplicando a esta máquina la propia lección de la entrada 54, el módulo
    `RNA` (ViennaRNA 2.7.2, el mismo que usó `C13`) **está instalado**, en el `python3` de WSL
    `[M]`. La mitad de BLAST+ sí es correcta: acá no está `[M]`. El intérprete donde estaba
    ViennaRNA no es el del `PATH` de Windows; de qué intérprete salió el hecho viejo no consta
    (`PLAN_OLA6.md` §1 dice que la máquina de ese diagnóstico tampoco consta).
    Medido hoy, aquí, con `command -v` sobre los dos lados y `importlib` sobre los dos
    intérpretes `[M]`:

    | | Windows (`python` 3.10.11) | WSL (`/usr/bin/python3` 3.12.3) |
    | --- | --- | --- |
    | módulo `RNA` (ViennaRNA) | **no está** | **está**: 2.7.2, rueda de `pip` |
    | módulo `Bio` (Biopython) | **no está** | **no está** |
    | módulo `ahocorasick` | **no está** | **no está** |
    | `numpy`, `scipy`, `pandas` | 1.26.3 / 1.11.4 / 2.3.3 | **no están** |
    | `openpyxl` | **está**: 3.1.5 | no medido |
    | `RNAfold`, `RNAplfold` (ejecutables) | **no están** | **no están**: la rueda de `pip` trae el módulo y no los binarios |
    | `blastn`, `tblastn`, `makeblastdb`, `diamond` | **no están** | **no están** |
    | `bowtie`, `bowtie2` | **no están** | **no están** |
    | `miniprot` | **no está** | **está**: 0.18-r281, compilado en `~/yhat/tools/miniprot/`, fuera del `PATH` |
    | `micromamba`, `conda` | **no están** | sin entornos en `~` |

    No hay aquí el reparto de `micromamba` que tiene la máquina de Joaquín: lo que hay está
    repartido entre los dos intérpretes, y **ninguno de los dos corre el port entero solo**. El
    de Windows tiene `numpy` y no ViennaRNA; el de WSL tiene ViennaRNA y no `numpy`. `[H]` El
    backend `exe` del port no debería correr en ninguno de los dos: necesita `RNAfold` y
    `RNAplfold`, que no están en ninguno `[M]`, pero no se corrió para comprobarlo. `work/` y
    `YHat-Biotech/` **no existen** en esta máquina `[M]`, así que todo script que los lea queda
    sin correr aquí. `[H]` Y el gancho de pre-commit debería rechazar aunque `openpyxl` esté,
    porque su código pide además la planilla de EPILAB (`tools/verificacion/hooks/pre-commit`,
    líneas 26-30); leído, no corrido.
    `[H]` La consecuencia para el reparto de trabajo: `F1` (#25) **sigue necesitando otra
    máquina o una instalación**, porque aquí falta el alineador proteína contra proteína que
    pide la ortología recíproca —no hay `diamond` ni `blastp`— aunque `miniprot` cubra la otra
    mitad, que es exactamente lo que `D71` ya había usado para `O2`. Lo que **sí** destraba la
    corrección es el eje de ViennaRNA: una corrida que solo necesite el módulo `RNA` y no
    `numpy` corre aquí, y hasta hoy el plan la daba por imposible en esta máquina.
    `[H]` La lección, que es la de la entrada 54 una vuelta más: **decir en qué máquina no
    alcanza si la máquina tiene dos intérpretes.** Hay que decir en cuál, y medirlo en los dos.
    En la de Joaquín el reparto lo hacía `micromamba`; en esta lo hace la frontera
    Windows/WSL. Y al anotar un hecho de entorno sobre una máquina ajena conviene citar la
    decisión que de verdad lo registra: la entrada 54 citó `D78` por `D71`.

### Ola 6, validación del supuesto de las bandas y cierre de `F1` (`D86`, issue #25, 2026-10-27)

**Se cierra la 56.** El supuesto se midió y se sostiene: el paso por ORF de seis marcos no degrada
la concordancia (85,0 % contra 85,0 % sobre los 11.727 genes presentes en los dos brazos, sin que
ningún IC95 se separe en ninguna de las cinco bandas). La diferencia máxima entre brazos es de
**0,6 puntos** y cae en la banda < 40 %, que por preregistro no decide porque no llega a n = 100;
entre las cuatro que sí deciden, la máxima es de 0,3 puntos. Detalle en `research/ola6/F1_transferencia_homologia/validacion_bandas/REPORT.md`.

62. **¿Por qué el par completo no reproduce lo que publicó `C12`?** El brazo P es el diseño de
    `C12` —MQ contra HV, proteínas curadas, recíproco— corrido entero, y da 85,1 % contra el 78,2 %
    publicado, con los tres tramos altos entre 6 y 10 puntos por encima y diez veces más pares
    `[M]`. Las candidatas son dos y no se separaron: `C12` usó una submuestra de 4.000 consultas con
    un **reverso parcial** (sólo los 3.100 mejores hits), que puede declarar recíprocos pares que no
    lo son, y corrió con BLAST+ en vez de `diamond`, que no dan la misma `pident`. Separarlas es
    barato: repetir el brazo P con `blastp` del entorno `alineador`. **Hasta que se haga, las bandas
    publicadas de `C12` quedan en duda, y las usa `F1` y cualquier cosa que cite el 78,2 %.**
63. **¿Cuánto cuesta el error de ensamblado de novo, que la validación no cubre?** Se midió el
    efecto de traducir en seis marcos sobre transcriptos **curados** de RefSeq. La quimera, el
    fragmento y el marco roto de un TSA ensamblado de novo no están en ese diseño; sólo se acotó por
    cobertura, que estima 1,1 puntos. Medirlo exigiría un organismo con TSA de novo **y** proteoma
    anotado, los dos públicos, y no se buscó si existe.
64. **El rótulo de cobertura separa «alta» del resto, pero no separa `parcial` de `fragmento`.**
    La concordancia del par `fragmento` (71,4 %, IC95 65,1–76,9, n = 220) es nominalmente mayor que
    la del `parcial` (68,6 %, IC95 65,7–71,4, n = 1.032) `[M]`: los intervalos se solapan de lado a
    lado, así que la inversión **no** es un hallazgo, pero tampoco hay evidencia de que el corte en
    30 % de cobertura ordene nada. Si los dos rótulos miden lo mismo, conviene colapsarlos en «no
    alta» y no sugerir una gradación que no se midió. No se revisó el umbral.

65. **`D67` define tres mecanismos y el catálogo tiene cuatro.** Las quimeras se arman por
    combinación de fenotipos que no se solapan —reproducción, movilidad, letalidad— y al
    asignarle su mecanismo a cada una de las 36 filas de `C5` aparecen cuatro que no entran
    en ninguno de los tres: `CI-07` (clatrina, baja la colonización del fitoplasma), `CI-09`
    (natterina y lectina, reduce la multiplicación), `HE-07` (`NcSP75`, proteína salival de
    la transmisión) y `HE-11` (*Graminella nigrifrons*, interacción con *Maize fine streak
    virus*). Describen **menos transmisión con el insecto vivo** `[R]`, que es el mecanismo
    más alineado con el objetivo sanitario del proyecto y el que menos se parece a los otros
    tres: no reduce la población ni mata, corta la cadena. `F3` lo agrega como categoría
    declarada `transmision` en su propia salida (`D87`), pero **ampliar `D67` no es de esta
    línea**: hay que decidir si el cuarto mecanismo entra al armado de quimeras, y si entra,
    si una quimera «letalidad + transmisión» tiene sentido biológico o si son el mismo eje
    visto a dos tiempos `[H]`. Pregunta para el investigador.

66. **Los dos candidatos cuyo silenciamiento empeora las cosas, y la pregunta que abren.**
    `CI-08` (`uk1_LRR`, receptor putativo de adhesión) dice que silenciarlo **aumentó** la
    colonización del vector por el fitoplasma, y `CI-13` (`NcHig`, factor neural antiviral)
    que silenciarlo **aumenta** la infección del sistema nervioso por el virus `[R]`. `F3`
    los deja fuera del orden y los publica como `fenotipo_invertido` (`D87`), que es lo
    correcto para un recomendador. Pero la lectura interesante es la inversa y no es nuestra:
    si silenciar esos genes aumenta la colonización, son parte de la **defensa del vector**
    contra el patógeno, y entonces la pregunta de diseño es si hay algo que hacer con eso en
    la dirección opuesta —no silenciarlos— que esté fuera de lo que este proyecto hace con
    ARNi `[H]`. Preguntar, no suponer.

67. **Faltan `work/sifi_v2/` y los tres TSA de *Dalbulus maidis* en la máquina de Santino, y
    son los insumos de dos de los cinco ejes de `F3`.** Verificado con `test -d` y con un
    `find` sobre todo el disco del proyecto: `work/sifi_v2/` **no existe** —ni `salida_k21`,
    ni `offtarget_k21`, ni `offtarget_dm_k21`— y `work/W5/ref/` tiene **sólo**
    `humano_rna.fna.gz` y su `.sha256`, no los `TSA_GCWP01/GHCC01/GITV01.fasta` `[M]`. Sin
    el primero no hay eje de off-target por gen; sin los segundos no hay eje de conservación
    entre poblaciones. Se piden al grupo —los tiene la máquina de Joaquín, según `D83`— y con
    el pedido va la advertencia que `PENDIENTE.md` de `R11` ya dejó escrita: **no se
    regeneran acá con otra versión del motor**, porque el conteo de ventanas eficientes se
    mueve con la versión de ViennaRNA y con la tabla de vecinos, y un `work/` reconstruido en
    otro entorno convierte un pendiente de insumo declarado en una discrepancia nueva.

68. **«Esta máquina», dos veces el mismo día, sin nombrar la máquina.** `D71` pide que cada
    verificación de entorno diga **en qué máquina** se hizo, y es la regla que vuelve
    utilizables los pendientes de `R11`. Dos artefactos del 27 de octubre no la siguen:
    `prompts/F3.md` dice «**esta máquina** tiene `work/` completo» y `D83` dice que
    `work/sifi_v2/` «**existe y está completo en esta máquina**». Las dos afirmaciones son
    ciertas en la máquina de Joaquín, que es donde se escribieron, y **falsas en la de
    Santino**, que es donde se leyeron `[M]`. No es un reproche: es que el costo de la
    omisión no lo paga quien escribe. Leída en la máquina equivocada, la primera hace creer
    que un eje es calculable y la segunda invita a «arreglar» el hueco regenerando el
    insumo, que es justo lo que la entrada 67 dice que no hay que hacer. La forma barata de
    cerrarlo: cuando una afirmación de entorno entra a un archivo versionado, el nombre de la
    máquina va en la misma oración, como lo hace `PENDIENTE.md` de `R11`.

69. **Se contesta la sub-pregunta del issue #27 sobre el zip, y la respuesta es no.** El
    issue dejaba planteado, sobre el eje de expresión en el tejido expuesto, «habría que ver
    si el zip lo trae». No lo trae: `work/zip_diego/` tiene **un solo archivo**, el
    transcriptoma `Dalbulus_maidis_transcriptome_GITV01.fas`, sin tabla de expresión ni
    metadatos de muestra, y sus cuatro estadísticas reproducen exactamente las del TSA
    público que `W3` bajó del FTP del NCBI en la ola 2 —56.117 secuencias, 94.702.486 pb, la
    más larga 205.383, la más corta 200 `[M]`—. No es una omisión del envío: un TSA es un
    ensamblado y no contiene abundancia por muestra, y las 56.117 cabeceras son uniformes,
    con **cero** menciones de tejido, cobertura, TPM o librería `[M]`. El eje 5 queda
    declarado faltante, como el `PREREGISTRO.md` lo escribió **antes** de abrir el zip
    (`research/ola6/F3_recomendador_genes/resultados/verificacion_zip_expresion.md`).
    **Lo que queda abierto es otra cosa, y conviene no confundirlas:** el único proyecto de
    lecturas fichado, `PRJNA631706` (16 corridas, 42.305 MB), contrasta *naive* contra
    expuesto a MRFV a 4 h y 7 días, y **ninguna muestra nombra un tejido**: es insecto
    entero. Daría un eje de **respuesta de expresión a la exposición al virus**, que no
    tenemos y que es interesante por sí mismo, pero no contesta si el gen se expresa donde
    el ARNdc ingerido llega `[H]`. Costaría 42 GB y un mapeador que esta máquina no tiene.

70. **El mecanismo `movilidad` de `D67` tiene un solo candidato en las 36 filas de `C5`, y
    su réplica más cercana es negativa.** Al asignar el mecanismo de fenotipo de las 36 filas
    desde el campo `resultado`, el reparto queda: letalidad 16, reproducción 13,
    **transmisión 4** y **movilidad 1** `[M]`. El único de movilidad es `DM-02`
    (`V-ATPase B` de *Dalbulus maidis*), y su apoyo es la frase «alas deformes», sin magnitud
    ni estadístico. `DM-03` es la otra subunidad de la misma bomba, en la misma especie y con
    la misma vía de entrega, y ahí el efecto sobre alas **se midió y no dio significativo**
    `[M]`. `[H]` Si las quimeras se arman combinando mecanismos que no se solapan (`D67`),
    una de las tres patas del esquema se apoya en una fila cuya replicación más cercana
    falló, y el mecanismo que `D67` no reconoce —transmisión, entrada 65— tiene cuatro veces
    más candidatos. No es de esta línea decidirlo: `F3` publica el reparto y la quimera de
    `O3` no se toca. Lo que hay que preguntar es si «movilidad» sigue siendo una pata del
    esquema con este respaldo, o si el tercer eje del armado debería ser transmisión.

71. **Dos filas del catálogo traen mortalidad que su propia fuente desatribuye del blanco, y
    una de las dos trae un número grande.** `HE-08` lo dice directamente («mortalidad alta
    por la dosis, no por el blanco») y ya estaba visto. `HE-04` es el mismo caso y es más
    peligroso: trae 64 % de mortalidad a 120 h creciente con la dosis, **y** la fuente aclara
    que el knockdown no correlaciona con la dosis y que el control de dsGFP a 500 y
    1000 ng/µL ya mata más que el de sacarosa `[R]`. Las dos quedaron etiquetadas
    `sin_fenotipo_atribuible_al_blanco` y fuera del orden. `[H]` La pregunta que abren no es
    de `F3`: si a esas dosis el dsRNA mata por sí mismo, cualquier bioensayo de ingesta del
    proyecto que use dosis de ese orden necesita su propio control de dsRNA no relacionado, y
    conviene saber si los trabajos que sostienen nuestras cifras de letalidad lo tienen. Es
    una pregunta para el investigador.

72. **Cinco fuentes que el eje de esencialidad de `F3` necesita y no se pudieron abrir, con el
    motivo de cada una.** `CLAUDE.md` pide anotarlas en vez de citarlas, así que acá están.
    *(a)* **Park y colaboradores 2002**, *Development*, el nulo de `eth`: HTTP 403. Es la
    primaria del único número del eje que hoy se cita desde una ficha secundaria —el 98 % de
    mortalidad en la transición del primer al segundo estadio larval, tomado de la ficha de
    InteractiveFly—, así que es la más importante de recuperar. *(b)* El trabajo de `Laccase2`
    en *Bemisia tabaci*: HTTP 403 desde DOAJ. Sería la fuente más pertinente de esa vía por ser
    un hemíptero, y cubre dos candidatos (`CI-11`, `CI-12`), hoy en `E0`. *(c)* La revisión de
    *Frontiers in Physiology* doi 10.3389/fphys.2020.591569, que según la búsqueda describe a
    `Lac2` como esencial para pigmentación y endurecimiento: el PDF llegó como binario
    ilegible. *(d)* La ficha de FlyBase de `pontin` (`FBgn0040078`): se descargó vacía; dejaría
    `DE-02` en `E2` en vez de `E0`. *(e)* **Collier y colaboradores 2000**, *Genetics*, que
    según la búsqueda describe alelos letales recesivos de `emb` —el ortólogo de XPO1— que
    mueren sin pasar al tercer estadio: no se abrió, y dejaría `DE-05` en `E3`. Además quedan
    **tres vías sin búsqueda propia** en esta pasada, y conviene decirlo como lo que es —falta
    de trabajo, no falta de fuente—: troponina C (`CI-10`), transformer-2 (`DE-03`), y
    natterina y legumaína (`CI-09`), más la proteína salival `NcSP75` (`HE-07`).

73. **Una contradicción entre dos tamizajes de la misma especie sobre la actina, que afecta a
    `CI-05`.** `Ulrich` y colaboradores 2015 ponen al grupo de organización del citoesqueleto
    como el tercero más predictivo de letalidad en *Tribolium castaneum*, con 37 de 66 genes
    nuevos letales `[R]`. `Buer` y colaboradores 2024, el tamizaje genómico de **la misma
    especie** y nueve años posterior, dice explícitamente que la β-actina **no** quedó en
    ninguno de sus conjuntos de blancos efectivos `[R]`. Las dos cosas pueden ser ciertas a la
    vez —la vía como grupo es letal y ese gen puntual no es un buen blanco— pero para el eje de
    esencialidad de un candidato cuyo gen **es** actina muscular la diferencia importa. Se
    resolvió bajando la vía a `E2` y declarando el `[?]`, no promediando. `[H]` Si alguien
    consigue el dato por gen del segundo trabajo, esto se cierra en una dirección o en la otra.

74. **«Matar o esterilizar» queda contestada en parte, y conviene ser preciso sobre cuánto.**
    El issue #27 decía que `F3` es lo que volvería decidible esta pregunta, que venía abierta
    desde el checkpoint 2. **Lo que ahora sí se puede afirmar:** el ranking tiene eje de
    fenotipo, que antes no tenía, y con él se ve que de los 25 candidatos ordenados hay 16 con
    letalidad, 13 con reproducción, 4 con transmisión y 1 con movilidad `[M]`; que los tres
    primeros de la cohorte A son de letalidad (`DM-02`, `DM-03`, `DM-05`); y que el mejor
    candidato de reproducción, `DM-01` (`BicC`), queda en el grupo del puesto 5 porque su vía
    **esteriliza y no mata**, lo que el eje 2 puntúa `E1` por ser función condicional.
    **Lo que sigue sin poder afirmarse, y es el centro de la pregunta:** que el orden *cambie*
    según el objetivo. El criterio de `D87` **no tiene un parámetro de objetivo**: tiene un eje
    de fenotipo que promedia mecanismos en vez de filtrar por ellos, así que la diferencia de
    puesto entre `DM-05` y `DM-01` no sale de haber elegido matar en vez de esterilizar —sale
    del nivel de esencialidad de sus vías—. `[H]` Lo que haría falta es un **segundo orden** con
    el eje de fenotipo filtrado por mecanismo y no promediado, corrido dos veces, y comparar los
    dos. Es una línea nueva y no un parámetro de ésta, y es barata: los dos ejes ya están
    calculados y versionados. Mientras eso no se haga, la respuesta honesta a si el orden de los
    candidatos del insecto cambia según el objetivo sigue siendo que **no se sabe**, con la
    diferencia de que ahora se sabe exactamente qué falta para saberlo.

75. **Se cierra la entrada 74, y la respuesta es que sí: el orden de los candidatos del insecto
    cambia según el objetivo.** El segundo orden de `F3`
    (`research/ola6/F3_recomendador_genes/scripts/04_segundo_orden.py`) corre el criterio de
    `D87` dos veces con todo idéntico —pesos, escalas, cohortes, umbral de empate— y lo único
    que cambia es quién es elegible: «matar» exige el mecanismo `letalidad`, «esterilizar»
    exige `reproduccion`. La regla de lectura se declaró en el script antes de mirar el
    resultado. El primer puesto de la cohorte A es `DM-02`, `DM-03` y `DM-05` para matar, con
    puntaje 1,0000, y `CI-01`, `CI-02`, `CI-03`, `DE-01` y `DM-01` para esterilizar, con
    0,7908: **los dos grupos no comparten un solo candidato** `[M]`. Con eso queda contestada
    la pregunta que venía abierta desde el checkpoint 2, y que el investigador había dicho que
    no sabía si cambiaba la decisión `[?]`.
    **Las tres lecturas que valen más que el sí.** *(a)* La vía de esterilizar está **peor
    sostenida**: ningún candidato de ese objetivo llega a 1,0000, porque los tres que están en
    el máximo de los dos ejes son todos de letalidad; no tenemos ningún candidato que esterilice
    y a la vez tenga evidencia de primer nivel en nuestra especie y vía de esencialidad
    demostrada `[M]`. *(b)* Esterilizar **saca a *Dalbulus maidis* del podio**: de los cinco del
    grupo líder sólo `DM-01` es de nuestra especie, y entra empatado con dos cicadélidos y un
    delfácido, así que el objetivo cambia también de qué especie viene la evidencia en la que
    uno se apoya. *(c)* La quimera de `O3` resulta ser **un miembro del grupo líder de cada
    objetivo** —`BicC_Dm` de esterilizar, `V-ATPase B` de matar—, lo que es una confirmación
    independiente de su armado, porque `O3` eligió esos dos genes por `D67` y por disponibilidad
    de secuencia, antes de que este eje existiera `[H]`.
    **Lo que sigue abierto, y no es poco:** elegir el objetivo. `F3` no lo elige y no debe; es
    decisión del equipo y del investigador, y ahora tiene la tabla que antes no tenía.
### Ola 6, el barrido de corridas pendientes del issue #37 (2026-10-27)

> Se publicaron como **65 a 74** y se renumeraron a **76 a 85** al mergear: `F3` (issue #27)
> había usado 65 a 75 en la misma jornada. La equivalencia, por si alguien llega desde un
> commit que cita los números viejos: 65→76, 66→77, 67→78, 68→79, 69→80, 70→81, 71→82,
> 72→83, 73→84, 74→85.

> Todas estas se midieron en **la máquina de Joaquín** (macOS, Darwin 27.0.0), con `work/`
> en disco (14 GB) y el entorno `w5bio` de `micromamba`, que es el único de los doce que
> corre la línea entera: Python 3.11.17, ViennaRNA 2.7.2 —la misma versión que usó `C13`—,
> Biopython 1.88, `ahocorasick`, numpy 2.4.6, BLAST+ 2.17.0 y los ejecutables `RNAfold` y
> `RNAplfold` `[M]`.

76. **El entorno estaba medido mal otra vez, y en la dirección de siempre.** `PLAN_OLA6.md`
    dice que en esta máquina «faltan `RNAplfold` y `RNAfold`», con la salvedad de que eso
    «no se volvió a medir contra los `envs/`» `[?]`. Medido ahora: **están**, los dos, en
    `envs/w5bio/bin/` junto con los otros veintisiete ejecutables de ViennaRNA `[M]`. Esa
    era la última celda que quedaba en pie de la tabla de entorno, así que de la lista
    original de herramientas faltantes de esta máquina **no falta ninguna**. `[H]` La
    lección es la tercera vuelta de la misma: la entrada 54 la enunció para `command -v`,
    la 55 para «en qué máquina», y ésta la cierra para los entornos sin activar. Cuando un
    hecho de entorno viene marcado `[?]` porque no se volvió a medir, lo que corresponde no
    es arrastrarlo: es medirlo, que cuesta un `ls`.

77. **El censo de generadores pasó de 2 de 8 a 8 de 8, y ninguno de los seis que se
    destrabaron lo estaba por el motivo que el inventario le atribuía.**
    Corrido de punta a punta con `work/` en disco, terminan con código 0 **los ocho** `[M]`.
    Llegó ahí en tres pasos: cinco en la primera pasada, siete tras las dos correcciones que
    siguen, y el octavo —`sensibilidad_reparto.py`— cuando el equipo firmó la fila que lo
    frenaba (`D92`). Los tres que fallaban en la primera pasada lo hacían por tres motivos
    distintos y **ninguno era falta de insumo**:

    * `ranking_v2.py` **no fallaba por insumo**: el censo lo invoca con `--muestras 50`
      para ir rápido, y el ancla del barrido compara frecuencias contra `W7` con igualdad
      exacta, lo que sólo tiene sentido con el mismo número de sorteos. Las frecuencias
      obtenidas eran múltiplos de 2,0 —o sea, de 50 muestras— contra las décimas finas de
      las 2.000 publicadas. Con el default corre entero y pasa todas las anclas `[M]`.
      `[H]` Es un defecto del censo, no del motor: un comando de censo que cambia un
      parámetro para abaratar la corrida puede romper un ancla por construcción y
      reportarlo como «ANCLA ROTA», que es el peor mensaje posible porque es el que nadie
      ignora. Conviene que el censo corra los generadores con sus defaults, o que declare
      al lado qué parámetro cambió.
    * `sensibilidad_reparto.py` llegó hasta el final de la cadena de insumos y se detuvo
      donde el proyecto quiere que se detenga: en una firma. Su error pasó de
      `RegionNoTamizada` a `AlertaSinDecidir` —un paso de avance: la región ya estaba
      tamizada y lo que faltaba era que una persona la firmara— y **terminó el mismo día**,
      cuando esa firma se escribió (`D92`). Ver la entrada 78.
    * `01_region_vatpase_b.py` fallaba con `StopIteration` por un desencuentro de rutas, no
      por falta de datos. Ver la entrada 79.

78. **La compuerta encontró una región nueva, y es la misma ventana de siempre vista desde
    un nucleótido más adelante.** `sensibilidad_reparto.py` levantó
    `RegionNoTamizada: eth_Dm 194-393`. Medida la cosa entera en vez de iterar —los nueve
    `rho` del barrido de exposición, los seis genes, sin dejar que la compuerta corte en la
    primera—, de los **54 pares gen × rho** esa es la **única** que no estaba en el
    inventario de 19, y aparece **sólo en `rho` = 0,00**, el reparto de `D47` con el peso
    de exposición de *Homalodisca vitripennis* en cero `[M]`. Con cualquier `rho` mayor la
    recomendada de `eth_Dm` vuelve a ser 114-313.

    Agregada al inventario, **trae una coincidencia perfecta de 21 nt**, y es la misma que
    ya tenía `eth_Dm` 193-392: mismo organismo (*H. vitripennis*), mismo locus
    (`LOC124369889`, quitinasa 2 probable), **misma posición 347**, los mismos conteos de
    `D28` (1 de 21/21 y 5 de ≥ 19 nt, 0 eficientes) `[M]`. La fila salió **sin firmar**, que
    es lo que corresponde: la firma la escribe una persona. Y mientras estuvo sin firmar,
    `sensibilidad_reparto.py` **no terminaba** —levantaba `AlertaSinDecidir`—, lo que
    convirtió ese pendiente de «falta `work/`» en «falta una firma»: una clase distinta de
    pendiente, en manos del equipo y no de una máquina.

    **Firmada el mismo día, bloqueante, por `D92`.** Con la firma puesta el generador
    termina y el censo llega a 8 de 8 `[M]`. Lo que la firma agrega y no estaba en la de
    193-392 es que **acá la región y el peso están acoplados**: ésta aparece sólo con
    `rho` = 0,00, así que si la exposición de *H. vitripennis* se cerrara en 0,60 la fila no
    se vuelve más fuerte —como pasaría con 193-392— sino que **la región desaparece**. Al
    revisarla hay que mirar primero si sigue siendo recomendada con el peso que se decida.

    `[H]` Y el argumento contra la propuesta de 22 nt para `eth_Dm` —correr la ventana
    introduce un acierto perfecto que la región vigente 114-313 no tiene— ahora tiene
    **dos** regiones que lo sostienen en vez de una.

79. **`work/O3/` de esta máquina tiene otro layout que el que el script de `O3` pide, y la
    diferencia no era de datos.** `01_region_vatpase_b.py` busca
    `work/O3/sifi/full_corregido/`, `work/O3/offtarget/` y `work/O3/offtarget_humano/`, y lo
    que hay en disco es `work/O3/salida/` y `work/O3/offtarget/cds_completo/`, de otra
    corrida. Regenerado el layout que el script declara —`run_sifi.py` sobre el gen entero y
    los dos tamizados, con ViennaRNA 2.7.2— el script corre entero y reproduce `D74` **celda
    por celda**: 1.184 regiones posibles, **una** no vetada (517-816), y el veto por
    referencia en el CDS entero con maíz 12, *H. vitripennis* 38 y humano 21 `[M]`.
    Comparado por valor contra el `region_vatpase_b.json` publicado, las diferencias son
    **cuatro y ninguna es una cifra**: el nombre de la consulta, dos separadores de ruta de
    Windows y la versión de Python `[M]`. El archivo publicado se dejó como estaba, porque
    es el registro de la corrida que lo generó.

    `[?]` Queda algo sin resolver: el `REPORT.md` de `O3` §12 nombra
    `work/O3/fasta/consultas_pasoA.fasta` como la consulta del tamizado, y **ningún script
    versionado lo genera**. La corrida original usó una cabecera
    `VATPaseB_Dm_OZ319705.1_38943269_38957327` y la reproducción usó `VATPaseB_Dm_full`; que
    todos los conteos coincidan prueba que la secuencia es la misma, pero el generador de
    ese FASTA no está en el repositorio.

80. **La grilla fina de `O4` no pide 136.446 plegados: pide 129.761.738.** La entrada 48
    publica «136.446 plegados `[M]`, que entran en unas horas de esta máquina». Medido hoy,
    con los insumos en disco y el enumerador versionado: con `--paso 1` la grilla tiene
    **2.133.868.568 combinaciones antes de podar**, de las cuales **129.430.632** son
    admisibles en marco 2, y con los 331.106 fragmentos el total es **129.761.738
    plegados** `[M]`. Son **tres órdenes de magnitud** más que la cifra publicada. Al ritmo
    medido de esta máquina —la grilla gruesa hizo 3.405 plegados en 162 s, o sea 21 por
    segundo `[M]`— eso no son «unas horas» sino del orden de **71 días** de una máquina
    sola. `[?]` De dónde salió 136.446 no consta: la cifra aparece sólo en prosa, en
    `REPORT.md` §8 y en la entrada 48, sin ningún archivo de salida que la respalde, y la
    corrida que la habría producido es justamente la que el mismo texto dice que no se hizo.
    `[H]` Un número que nunca se pudo reproducir no debería llevar `[M]`, que es la marca de
    lo medido y reproducible desde el repositorio; éste parece una estimación.

    Lo que el enumerador ofrece como pasos intermedios, medido en la misma corrida:
    `--paso 2` pide 16.816.657, `--paso 5` pide 1.177.056 y `--paso 10` pide **173.289**
    `[M]`. El último es el único que entra en una tarde, y **se corrió**: 169.648
    combinaciones más 3.641 fragmentos, en unas cinco horas de esta máquina `[M]`.

    **Y contesta la pregunta: el paso mueve el primer puesto.** La grilla gruesa daba
    `Q_BicC_Dm_1951-2450__VATPaseB_Dm_1001-1100` con 64 ventanas heredadas eficientes. Con
    `--paso 10` el primero es `Q_BicC_Dm_1961-2460__VATPaseB_Dm_1001-1100` con **65**, y el
    de la gruesa cae al **puesto 2** `[M]`. El ganador nuevo arranca diez nucleótidos más
    adelante, en una ubicación que la retícula de paso 50 **no tocaba**, que es exactamente
    el mecanismo que la entrada 48 temía cuando lo planteó para las islas angostas. Las
    combinaciones con alerta de juntura nueva pasan de 515 de 3.204 (16,1 %) a 15.763 de
    169.648 (9,3 %) `[M]`.

    `[H]` Pero el margen es **una ventana** sobre 65, así que conviene no leerlo como «la
    grilla gruesa eligió mal». Lo que queda medido es más modesto y más útil: el orden de
    esta grilla **no es estable al paso**, de modo que el primer puesto de cualquiera de las
    dos es un artefacto de la retícula tanto como del criterio. Eso refuerza lo que `D65` ya
    había decidido por otra vía —que el conteo no es lo que decide entre candidatos— y se
    suma al aviso que viaja con este objetivo: el criterio de eficiencia de si-Fi21 no está
    validado en hemípteros, ρ = +0,142, IC95 [−0,247, +0,492], n = 29. Un reordenamiento por
    una ventana, bajo un criterio con ese intervalo, no mueve ninguna recomendación.
    `[?]` Y lo que sigue sin saberse es si `--paso 1` movería **otra vez** el primer puesto:
    la sucesión 50 → 10 lo movió una vez, y de ahí no se sigue que haya convergido.

81. **El eje de off-target por gen de `F3` no se desbloquea con `work/`, y la casilla lo
    decía mal.** Esta entrada completa la **67** y el §4 del `REPORT.md` de `F3`, que
    declararon el eje faltante «por falta de `work/sifi_v2/`» desde una máquina donde ese
    directorio no existe. Medido desde la máquina donde **sí** está: no alcanza, y el
    segundo motivo que `F3` ya había identificado —que los conteos de las 8 filas están
    contra otro panel, el de cinco referencias— no es el único que queda en pie. El issue
    #37 lo anota como «Necesita: `work/sifi_v2/`». Medido: las 28
    filas del catálogo de `C5` que no tienen `ventanas_21nt` son de **15 especies
    distintas** —*Euscelidius variegatus*, *Nephotettix cincticeps*, *Nilaparvata lugens*,
    *Rhodnius prolixus* y once más—, y `work/sifi_v2/salida_k21` tiene **seis** genes, los
    del ranking, de los cuales sólo `eth_Dm` y `bursA_Dm` están entre las 8 filas ya
    calculadas `[M]`. Las otras 6 de esas 8 usan secuencias que el catálogo nombra por
    accesión (`Rpn6_Stitanus_GJQL01135962`, `ATPsynBeta_Mquadrilineatus_XM_054410120` y
    cuatro más) y que no viven en `work/sifi_v2/`. O sea que lo que falta para ese eje no es
    un directorio de trabajo: son **28 secuencias de transcripto** que hay que recuperar una
    por una. `[H]` La consecuencia para el pedido de la entrada 67: mandar `work/sifi_v2/` a
    la máquina de Santino destraba el eje de **conservación** —que sólo necesita los tres
    TSA— y **no** el de off-target por gen, que seguirá faltando con el directorio en disco.
    Vale pedirlo igual, pero conviene que el pedido diga cuál de los dos ejes destraba. `[H]` Y hay una segunda diferencia que conviene no pasar por alto antes de
    mezclar las 8 con cualquier fila nueva: las 8 publicadas se tamizaron contra un panel de
    **cinco** referencias (*D. maidis*, *M. quadrilineatus*, *H. vitripennis*, *Zea mays*,
    *Apis mellifera*), que no es el panel de seis de `C7` v2 y `M6`.

    El **otro** eje de `F3`, el de conservación entre poblaciones, sí tiene su insumo: los
    tres TSA están en `work/W5/ref/` con 25.662, 55.286 y 56.117 secuencias `[M]`. No se
    corrió a propósito: el issue #27 pide que el criterio y los pesos se escriban **antes**
    de la primera corrida, y ese preregistro todavía no existe. La casilla queda
    desbloqueada por insumo y frenada por preregistro, que no es lo mismo.

82. **La vuelta de la reciprocidad de `R8` contra un proteoma anotado confirma lo publicado,
    y de paso mide la limitación de las variantes de empalme.** El §7 de `R8` declara que
    ninguna de las seis referencias es un proteoma y que por eso la vuelta usó el ORF más
    largo del transcripto. En esta máquina **sí hay** un proteoma anotado del organismo de
    origen: `GCF_021130785.1_UT_GWSS_2.1_protein.faa`, 31.163 proteínas de *H. vitripennis*,
    en `work/F1v/ref/` `[M]`. Rehecha la vuelta con `blastp` contra él, reusando los mismos
    ORF que dejó el paso 1 para que la única variable sea contra qué se devuelve:

    * comparando **accesiones de proteína**, cambian **2 de 5** veredictos
      (*H. axyridis* y *A. mellifera* pasarían de recíprocos a no recíprocos);
    * pero los dos caen en `XP_046683989.1`, que es la **isoforma X2 del mismo producto**
      que la consulta `XP_046683987.1` (`probable chitinase 2`), o sea el mismo gen;
    * colapsando por producto, cambian **0 de 5** `[M]`.

    O sea que la limitación de método estaba bien declarada y **no afectaba el resultado**.
    Los dos no recíprocos lo siguen siendo, y ahora se sabe por qué con más precisión: la
    vuelta de maíz cae en `chitinase-3-like protein 1` y la de humano en
    `probable chitinase 10`, que son otras quitinasas `[M]`. `[H]` La segunda limitación de
    §7 —un transcripto por acierto, con variantes de empalme— resultó estar del lado del
    **proteoma** y no del transcripto, y se resuelve comparando productos y no accesiones.
    Un ortólogo recíproco evaluado por accesión de proteína sobre un proteoma con isoformas
    declara no recíprocos pares que sí lo son, y el error va en la dirección conservadora.

83. **Cuatro de las diez anclas «salteadas por insumo» no eran de insumo: eran del
    directorio desde donde se corre el test.** El issue #37 dice que hay que correr los
    tests a mano con `cd tools\sifi21_port && python test_alertas.py`. Hecho así,
    `test_ranking.py` saltea cuatro anclas diciendo que falta
    `work/sifi_check/offtarget_full/offtarget_por_sirna.tsv`. **El archivo está.** Corrido
    desde la raíz del repositorio, el mismo test pasa las cuatro sin saltear ninguna `[M]`.
    Y los dos que «no colectan» con `python -m pytest` —`pipeline/test_features.py` y
    `tools/sifi21_port/test_sifi.py`— son scripts igual que los otros cuatro y corren
    directo, sin pytest, que además no está en ninguno de los doce entornos `[M]`.
    `[H]` Las seis suites pasan enteras y **sin una sola ancla salteada**, que es lo que la
    casilla transversal pedía. La lección es vecina de la de `command -v`: un «salteada
    porque falta X» que se cumple sólo desde cierto directorio informa mal, y lo que
    conviene es que el mensaje diga la ruta que se intentó, no la ruta relativa.

84. **El panel de `work/sifi_check/offtarget_full/` es el de las seis sin la humana, y ahora
    está dicho.** El issue #37 advierte que al pedir ese archivo hay que decir con qué panel
    se construyó, porque los dos juegos de anclas publicadas piden paneles distintos
    (`D83`). Medido sobre su propio `offtarget_resumen.json`: las bases son **seis** —
    *D. maidis*, *F. candida*, *A. mellifera*, *H. vitripennis*, maíz y *H. axyridis*— y
    **no incluye la referencia humana** `[M]`. Con ese archivo `test_ranking.py` pasa sus
    cuatro anclas de `sifi21_reproduccion.md` §4.

85. **El gancho de pre-commit corrió completo por primera vez, y la predicción de que
    rechazaría igual era falsa.** La entrada 55 anotaba, leído y no corrido: «el gancho de
    pre-commit debería rechazar aunque `openpyxl` esté, porque su código pide además la
    planilla de EPILAB» `[H]`. Medido al commitear este barrido: con `w5bio` en el `PATH`
    —el único de los doce entornos que tiene `openpyxl`, 3.1.5— y la planilla en
    `YHat-Biotech/Sequences_EPILAB.xlsx`, que **está** en esta máquina, el gancho corre la
    pasada contra EPILAB —4 regiones, 18.737 21-meros— y devuelve **0 hallazgos** `[M]`.
    No rechaza.

    `[H]` Lo que sí se confirmó es el otro lado del gancho, y conviene dejarlo escrito
    porque es la parte bien diseñada: con el `python3` del sistema **rechaza**, y su mensaje
    distingue las dos cosas que importan —«no es un hallazgo: es que la verificación no
    corrió»— y nombra el remedio exacto, incluido el `PATH=<env con openpyxl>/bin:$PATH`.
    Un verificador que falla cerrado y explica cómo abrirlo es la razón por la que este
    commit no se hizo con `--no-verify`.

    **Y lo que la pasada encontró no es nuevo, que es la parte importante.** Corrido
    `--solo-epilab` sobre el árbol entero da **6 hallazgos no exceptuados**, y son
    **exactamente los que `D61` ya había medido y decidido** el 2026-10-25: las dos regiones
    virales en `MRFV_NC_002786.2.fa` y `db_demo_zmays40_amel40_mrfv.fa` —subcadenas del
    genoma público `NC_002786.2`, confidencialidad nominal— y las dos de
    `q2_aciertos_localizados.tsv`, con los mismos números que esa ADR publica: 46 de 200 nt
    de `MP_MRFV` (23,0 %) y 48 de 300 de `BicC_Dm` (16,0 %), tramos contiguos máximos de 23
    y 25 nt `[M]`. O sea que la línea base de seis está **caracterizada y decidida**, no sólo
    contada, y esta corrida la reproduce.

    Que la pasada contra EPILAB los siga reportando como «no exceptuados» es el diseño y no
    un problema: `D61` metió esos dos archivos en la lista blanca **y** dejó escrito que eso
    «no los exime de la pasada 3», porque la lista blanca no tapa los hallazgos contra la
    planilla. El gancho da cero sobre el índice porque este barrido no toca esos archivos.
    `[H]` Lo único que conviene corregir es la redacción de la consecuencia de `D61` —«el
    árbol y el historial dan cero hallazgos no exceptuados»— que vale para las otras pasadas
    y no para la tercera: hoy el número de la tercera es seis y debería estar dicho al lado,
    porque si no, un lector que corre el verificador completo ve seis donde la ADR le
    prometió cero y no tiene forma de saber si eso es lo esperado.

## 2026-10-27 — Lo que deja abierto el alineamiento del nivel de alerta (`D90`, issue #18)

86. **Las columnas de alerta de `baseline_dsrip/region_multigen_resultados.csv` quedaron viejas y
   nadie las puede regenerar hoy.** `frac_regiones_con_alerta` y `alerta_en_mejor_media`
   reproducen exactamente el umbral 17 en los 20 de 20 loci, y con el 19 ya no `[M]`; igual
   `alerta_en_mejor_limpios`, `desc_en_mejor_limpios`, `solape_limpios_dsrip` y
   `solape_buenos_vs_limpios`. Los insumos (`investigathon/dsrip_baseline/multigen/`) no estan
   en esta maquina. **Que hay que decidir:** si cuando vuelva el corpus se regenera el archivo
   —y entonces cambian numeros que ningun documento cita pero que estan commiteados— o si se le
   agrega al propio CSV una nota de procedencia que diga con que umbral se produjo. No se toco
   porque no es archivo de esta linea `[H]`.
87. **`tools/generar_estado.py:306` todavia lista el issue #18 en `FALTA`.** La fila describe la
   contradiccion como pendiente y ya no lo esta. No se edito porque ese archivo es de la linea
   `R3`, que se cerro en otra sesion: hay que actualizar esa fila o confirmar que la pagina se
   regenera sola `[?]`.

### Ola 6, la brecha con `C12` descompuesta (`D91`, pregunta 62, 2026-10-27)

**Se cierra la 62.** La brecha es el normalizador de nombres (+7,0 de 6,45 puntos); el alineador
aporta +0,18 y el protocolo −0,73. La tabla de `C12` queda como está, válida para su propio
criterio. Detalle en `research/ola6/R13_brecha_c12/REPORT.md`.

88. **¿Cuál de los dos criterios de nombre es el que hay que usar?** No se decidió y no se midió.
    El de `F1` colapsa `isoform Xn`, `-like` y `homolog`; el de `C12` no colapsaba al menos los dos
    primeros. Que *ankyrin-3-like isoform X2* y *ankyrin-3-like isoform X8* sean el mismo gen es
    evidente, pero `-like` es otra cosa: *proteína X* y *proteína X-like* pueden ser parálogos
    distintos, y el normalizador de `F1` los cuenta como acuerdo. **El 21,6 % de los pares que
    recupera son por `-like`**, así que la elección mueve cerca de 1,5 puntos. Separar los dos
    sufijos y medirlos aparte es barato y no se hizo `[?]`.
89. **El normalizador de `C12` no existe como código y no se puede reconstruir.** Sólo sabemos, por
    diferencia, que dejaba pasar los sufijos de isoforma. Cualquier intento de reproducir
    exactamente su 78,2 % va a fallar por esto, y conviene saberlo antes de intentarlo. La lección
    general ya está en `CAMINOS_PROBADOS.md`: una regla de comparación descrita en prosa y no
    versionada no es reproducible aunque los datos sí lo sean.
90. **El censo de generadores escribía su salida de prueba encima de las cifras publicadas,
    y el defecto estuvo invisible mientras el generador fallaba.** `sensibilidad_reparto.py`
    escribe en `research/ola4/M5_dos_ejes/resultados/`, que es un directorio versionado, y
    no tenía forma de mandar la salida a otro lado. El censo de `R11` lo corre con
    `--muestras 50` para ir rápido. Mientras el generador moría por insumo eso no tenía
    consecuencia, porque no llegaba a escribir nada; **al destrabarse y terminar, la primera
    corrida reemplazó los dos archivos publicados de esa línea con una corrida de cincuenta
    sorteos en vez de los dos mil del default** `[M]`: 39.675 líneas insertadas y 101.943
    borradas entre `sensibilidad_reparto.json` y `.tsv`. Se revirtió antes de commitear y se
    le agregó `--resultados` al script, con el patrón que `quimeras_v2.py` y `ranking_v2.py`
    ya usaban; el censo ahora escribe en `work/R11_censo/m5_sensibilidad`.

    `[H]` Es el hermano del defecto de la entrada 77 y el más caro de los dos, porque no
    avisa: aquél rompía un ancla y gritaba «ANCLA ROTA», éste deja los archivos **con
    aspecto normal** y sólo se nota en el `git diff`. Y tiene una forma general que conviene
    mirar en el resto del repositorio: **un verificador que corre generadores hereda el
    poder de escritura de todo lo que corre**, así que un script que no sabe separar «dónde
    publico» de «dónde escribo cuando me están probando» no se puede censar sin riesgo. Lo
    que lo hizo invisible durante tres corridas del censo es justamente lo que el censo
    estaba midiendo: que el generador fallara.

91. **Barrido del defecto de la entrada 90 en el resto del repositorio: ninguno más estaba
    perdiendo datos, y la razón no es la que parecía.** La entrada 90 dejó el patrón y esto
    lo busca en todo el árbol, con un auditor que lo mide en vez de una lista a mano
    (`research/ola6/R12_corridas_pendientes/scripts/auditar_escrituras.py`). De **64 módulos
    que escriben y declaran su destino**, **43 escriben en el árbol versionado sin poder
    redirigir la salida** `[M]`. Pero el conteo que importa es otro:

    | | módulos |
    | --- | --- |
    | con riesgo de pérdida (el censo les cambia parámetros) | **0** |
    | regeneración benigna (el censo los corre con sus defaults) | 1 |
    | latentes (nadie los censa todavía) | 42 |

    **La tercera parte del defecto no es «lo corre el censo», y ahí estaba el error de
    planteo.** Los cuatro generadores censados que escribían en versionado sin bandera —los
    tres de `M6` y el de `O3`— el censo los corre **con sus defaults**, así que lo que
    escribían era exactamente lo que publicarían: regeneraban el mismo archivo. El único que
    tenía el defecto completo era `sensibilidad_reparto.py`, porque el censo le pasaba
    `--muestras 50`, que **sí** mueve el resultado. O sea que el riesgo no lo crea escribir
    en versionado sin bandera: lo crea escribir en versionado sin bandera **y** que alguien
    te corra con un parámetro distinto del publicado. Verificado corriendo los cuatro: los
    tres de `M6` dejan `git status` limpio, y el de `O3` **no** —reescribe
    `region_vatpase_b.json` en cada corrida, sin mover ninguna cifra, pero dejando el árbol
    sucio y un `git status` posterior al censo que parece un cambio de resultados `[M]`—.

    Arreglados los cuatro del censo: `compuerta.py` y `umbral_compuerta.py` tienen `--salida`
    (no tenían `argparse`), `01_region_vatpase_b.py` tiene `--resultados`, y el censo manda
    las tres a `work/R11_censo/`. Tras una corrida completa del censo, **ningún
    `resultados/` del árbol queda tocado** `[M]`. El quinto, `tabla_alertas.py`, se deja
    escribiendo donde escribe y queda declarado en la propia lista del censo: **es el
    generador del inventario**, no hay un segundo lugar donde un inventario tenga sentido, y
    corre con sus defaults.

    Los **42 latentes** —9 de la ola 3, 10 de la 4, 9 de la 5 y 14 de la 6— **no se
    tocaron**. No tienen el defecto completo: nadie los corre con parámetros de prueba.
    `[H]` Y tocar 42 scripts de líneas ya cerradas para agregarles una bandera que nadie usa
    es más riesgo que beneficio; lo que sí conviene es la regla para lo que venga: **un
    generador que alguien pueda querer correr sin publicar necesita saber dónde escribir**, y
    la lista está en `resultados/auditoria_escrituras.tsv` para cuando a uno de esos 42 le
    toque entrar a un censo.

    `[H]` Y dos lecciones del auditor mismo, que son del tipo que este archivo viene
    juntando. Primera: `git check-ignore` sobre `pipeline/salida` contesta **«no ignorado»**
    aunque el `.gitignore` lo ignore en su línea 16, porque el patrón termina en `/` y el
    directorio **no existe en disco**; con la barra final contesta «ignorado». Preguntar una
    sola vez daba cinco falsos positivos, los cinco del `pipeline/`, que es justo el
    directorio que `D61` declara ignorado. Segunda: `Path(__file__).parent / "salida"`
    resuelto contra la raíz del repositorio en vez de contra el directorio del script
    convertía esos mismos cinco en «escribe en versionado». Las dos son del mismo tipo que
    la de `command -v` (entrada 54): **la herramienta contestó con precisión una pregunta
    que no era la que había que hacerle.**

### Ola 6, cierre de `F4` (`D93`, issue #39, 2026-10-27)

*Nota de numeración: estas cinco entradas se escribieron como 88 a 92 contra el `main` de la
mañana, que llegaba hasta la 87 y tenía un hueco entre la 75 y la 86. Al integrar, el hueco
estaba lleno y las cuatro que faltaban ya existían, así que las cinco se corrieron a **92-96**
y el ADR de esta línea, escrito como `D91`, pasó a **`D93`**: `D91` y `D92` se los quedaron
`R13` y `R12`. Ninguna entrada ajena se tocó y ninguna cifra cambió al renumerar.*

92. **El cuarto mecanismo no tiene ni un candidato en nuestra especie, y eso le pone precio a la
    pregunta de la entrada 70.** Esa entrada dejó planteado si «movilidad» sigue siendo una pata
    del esquema de `D67` con el respaldo que tiene —una fila, `DM-02`, con la réplica más cercana
    negativa— o si el tercer eje debería ser transmisión, que tiene cuatro veces más candidatos y
    es el mecanismo más alineado con el objetivo sanitario. `F4` midió el otro platillo: de los
    cuatro candidatos de `transmision`, **ninguno es de *Dalbulus maidis*** `[M]`. Son tres de
    *Euscelidius variegatus* —uno compartido con *Scaphoideus titanus*— y uno de *Peregrinus
    maidis*. Así que **ninguna** de las 118 combinaciones con transmisión tiene las dos mitades
    medidas en nuestra especie (cero de 51, cero de 63 y cero de 4), contra 8 de las 229 del
    esquema de tres mecanismos `[M]`. `[H]` La elección queda entre una pata que descansa en
    **una fila de nuestra especie** y una que descansa en **cuatro filas de otras especies**, con
    la transferencia de ortología en el medio (`F1`, con su banda de concordancia). No es un
    argumento en contra de transmisión: es lo que hay que poner al lado del argumento a favor.
    Pregunta para el investigador, y si entra al armado pide su propio ADR (entrada 65).

93. **La entrada 65 nombra cuatro filas de transmisión y la tabla que se publicó tiene otras
    cuatro.** La 65 dice que al asignar mecanismo aparecen «cuatro que no entran en ninguno de
    los tres: `CI-07`, `CI-09`, `HE-07` y `HE-11`». Las cuatro filas que `eje_fenotipo.tsv`
    publica con `transmision` son `CI-06`, `CI-07`, `CI-09` y `DE-05` `[M]`. Las dos listas
    tienen cuatro elementos y comparten dos, lo que vuelve la discrepancia fácil de no ver. La
    tabla es la que manda y el motivo está en ella: `HE-07` quedó en `letalidad|reproduccion`
    porque «la FUNCIÓN es una proteína salival de la ingestión de floema, lo que invita a leerlo
    como transmisión» pero `resultado` mide longevidad, desarrollo y huevos, y se asignó por el
    resultado; `HE-11` quedó en `sin_fenotipo_publicado` porque la interacción con el virus no es,
    por sí sola, una reducción de transmisión medida; y entraron `CI-06` (menos adquisición de
    fitoplasma) y `DE-05` (menor acumulación del rabdovirus MMV). O sea que la 65 se escribió a
    mitad de la asignación y quedó vieja en sus ejemplos, no en su planteo: el cuarto mecanismo
    existe y tiene cuatro candidatos. **Qué hay que hacer:** corregir los cuatro identificadores
    de la entrada 65 o agregarle una línea que diga cuáles son hoy. No se editó acá porque es
    entrada de otra línea y conviene que el cambio lo vea quien la escribió `[?]`.

94. **«Fenotipos que no se solapan» tiene dos lecturas, y toda combinación de letalidad con
    movilidad falla la segunda.** `D67` arma las quimeras «por combinación de fenotipos que no se
    solapan» y `O4` lo implementa sobre los dos ejes **declarados**: exige que el eje de cada gen
    sea distinto. Con la tabla de `F3` en la mano se puede medir la otra lectura —que los
    **conjuntos** de mecanismos de los dos candidatos sean disjuntos— y da que **las 15 de 15**
    combinaciones de letalidad con movilidad la fallan `[M]`. El motivo es aritmético y por eso
    inevitable: el único candidato de movilidad, `DM-02`, **también** tiene letalidad, así que
    cualquier par que lo use para esa pata trae letalidad por partida doble. En reproducción +
    letalidad el solape aparece en 147 de 201 asignaciones `[M]`. `[H]` La consecuencia práctica
    es que la segunda pata de esas quimeras agrega menos de lo que su rótulo promete, y el
    bioensayo no lo va a distinguir: `O3` §6 ya advirtió que silenciando dos genes a la vez un
    resultado negativo no dice cuál mitad falló. **Qué hay que decidir:** si `D67` se lee sobre
    los ejes declarados o sobre los conjuntos. `F4` informa el solape por par y **no** cambió el
    criterio, porque mover la lectura vigente de `D67` movería lo que `O4` ya verifica y lo que
    `O3` ya midió. Pregunta para el equipo y para el investigador.

95. **Cuatro filas del catálogo son más de un gen, y hasta que no se diga cuál, los pares que las
    usan no son insumo del enumerador.** Una quimera se arma con un gen; una fila, no siempre lo
    es. `DE-01` es `V-ATPase B` **y** `V-ATPase D`; `DE-04` agrupa tres transportadores ABC con
    desenlaces **distintos** —la letalidad es de `ABCE` y `ABCF`, la reproducción de `ABCB`—;
    `CI-09` agrupa tres genes y además dos especies; `CI-11` agrupa `NcLac2` y `NcLac5` y el
    desenlace descrito es del primero `[R]`. De las 201 asignaciones de reproducción + letalidad,
    **63 involucran una de esas filas** `[M]`. `F4` las detecta con dos detectores y aborta si no
    coinciden, pero detectarlas no las resuelve: hay que abrir la fuente y decir qué gen sostiene
    qué mecanismo. En `DE-04` la propia nota del catálogo ya lo dice y alcanzaría con partir la
    fila; en las otras tres hace falta leer el trabajo. **Es falta de trabajo, no falta de
    fuente** `[H]`, y es la misma clase de pendiente que la entrada 72 declara para el eje de
    esencialidad.

96. **Cuatro citas de `PREGUNTAS_ABIERTAS.md` apuntaban al ADR equivocado, y se corrigieron
    acá.** Las entradas 65, 66, 74 y 75 citaban el criterio del recomendador de genes de `F3`
    como **`D84`**, y `D84` es el ADR de `F1` —transferencia de anotación por ortología
    recíproca—. El criterio de `F3` es **`D87`**, «los pesos del recomendador de genes: cohortes
    por ejes disponibles, y ningún hueco rellenado» `[M]`. Las cuatro son inequívocas: una dice
    «corre el criterio de `D84` dos veces con todo idéntico —pesos, escalas, cohortes, umbral de
    empate—» y `D84` no tiene pesos, ni cohortes, ni umbral de empate. **Causa:** la línea `F3`
    escribió esas entradas con la numeración que tenía antes de integrarse, y al mergear `main`
    su ADR se renumeró de `D84` a `D87`; las entradas se renumeraron y estas cuatro citas
    internas quedaron apuntando al número viejo, que entretanto se lo había quedado `F1`. Es el
    modo de falla propio de renumerar: lo que se arregla son los encabezados y lo que queda viejo
    son las referencias en el cuerpo. **Se corrigieron las cuatro** —el `D84` del encabezado del
    cierre de `F1`, línea 2252, es correcto y se dejó—. `[H]` La forma barata de que no vuelva a
    pasar: cuando una renumeración toca un ADR, buscar el número viejo en todo `00_meta/` antes
    de cerrar, no sólo en los títulos.

97. **Issue #43 (eje 3 de `F3`): recuperar las 28 secuencias «por accesión» no se puede hacer
    desde los enlaces de GenBank.** De los doce PMID que el catálogo de `C5` cita para las filas
    sin `ventanas_21nt`, **diez no tienen ningún registro de nucleótido ni de proteína enlazado**
    al paper, y los otros dos tienen muy pocos: 32362876 (`CI-13`) enlaza 2 y 36912710 (`DE-04`)
    enlaza 1 `[M]` (`research/ola6/F3_recomendador_genes/scripts/06_enlaces_genbank_por_paper.py`,
    salida en `resultados/eje3_enlaces_genbank_por_paper.tsv`; consulta pública a E-utilities,
    sin secuencias propias). Además, diez de las veintiocho filas citan un trabajo que `C5` no
    abrió (`apertura: no_abierta`), de modo que su accesión, si existe, está en un texto que
    nadie leyó. **Lo que falta no es insumo de máquina sino trabajo de lectura**, fila por fila,
    o la decisión de usar el ortólogo recíproco en una especie anotada como sustituto, como ya
    hizo `C5` con *Macrosteles quadrilineatus* (`CI-03`, `CI-10`, `DE-02`, `DE-05`), declarándolo
    en `secuencia_usada`. `[H]` Varias filas no tienen una secuencia única que recuperar
    (`HE-08` es un control de dosis, `HE-10` dice «varios», `HE-11` «respuesta inmune»): para
    ellas el eje 3 se declara no aplicable, no faltante. Pendiente de decisión del equipo antes
    de correr nada.

98. **`C8` dio `eth` y `bursA` sin transcriptoma que los cubra, y el eje 4 de `F3` los encontró en
    dos de los tres.** `conservacion.json` de `C8` declara las 595 ventanas de `eth_Dm` y las 448
    de `bursA_Dm` «sin transcriptoma suficiente», con cero fuentes. `blastn` contra los TSA
    completos (`research/ola6/F3_recomendador_genes/scripts/05_eje_conservacion.py`) los ubica en
    `GHCC01` y `GITV01`: `eth` con 595 y 420 ventanas con dato, `burs-alpha` con 419 y 419; en
    `GCWP01` no aparece ninguno de los dos `[M]`. En cambio `ATPaseD_Dm` (450 de 471) y `BicC_Dm`
    en `GHCC01` (2.417 de 2.500) **coinciden** exactamente con `C8`. `[?]` **La causa no se
    averiguó.** La explicación más simple es que `C8` partía de los contigs que `W5` ya había
    ubicado y esos dos genes no estaban entre ellos, pero no se abrió `W5` ni `generar_informes.py`
    para comprobarlo. **Qué cambia si es eso:** la conclusión de `C8` sobre `eth` y `burs-alpha`
    («la región propuesta para `eth` queda entera dentro de lo probado», conservación de
    `burs-alpha` sólo en un 70 %) usaba el amplicón y no la conservación entre fuentes, así que no
    se mueve; lo que sí cambiaría es la frase de que no hay transcriptoma que los cubra. Para
    cerrarla: leer cómo `C8` eligió los contigs y repetir su alineamiento local sobre los dos
    contigs que `blastn` encontró (`GHCC01027218.1` y `GITV01054587.1` para `eth`;
    `GHCC01014529.1` y `GITV01010186.1` para `burs-alpha`).

99. **El eje 4 de `F3` sólo llega a 5 de las 36 filas, y las otras 31 no son falta de cálculo sino
    falta de secuencia.** Reciben el eje `DM-01`, `DM-02`, `DM-03`, `DM-05` y `DM-06`
    (`PREREGISTRO_EJE4.md` §2). `DM-04` es de la propia especie pero no hay secuencia en esta
    máquina, y las 30 restantes son genes de otras especies: lo que habría que medir es la
    conservación de **su ortólogo en *D. maidis***, que nadie recuperó `[M]`. Se descartó usar los
    4.110 contigs de `GITV01` que `F1` dejó con ortólogo recíproco, por dos razones declaradas en
    el preregistro: ese contig es de uno de los tres TSA y su presencia ahí estaría garantizada
    por construcción, y el emparejamiento pasaría por el nombre del producto. **Es la misma
    recuperación que pide el eje de off-target (#43)**, y la entrada 97 ya midió que los enlaces de
    GenBank por paper no alcanzan para hacerla, así que conviene hacerla una sola vez:
    28 secuencias de transcripto de 15 especies para el eje 3, y el ortólogo en *D. maidis* de
    cada candidato para el eje 4. `[H]` Quien tome #43 debería dejar la tabla candidato → secuencia
    con su accesión, para que sirva a los dos ejes.

100. **Una secuencia sin homología trae un 0,5 % de ventanas con un bloque ≥19 nt coincidente contra
    el panel de seis, y no se sabe por qué.** El nulo del eje 3 de `F3` (50 permutaciones que
    conservan la composición, por gen) da una fracción limpia mediana de 0,9933 a 0,9950 y mínimos
    de 0,9660 a 0,9872 `[M]` (`resultados/eje3_nulo.tsv`). Por azar puro de 4^19 contra transcriptomas de
    algunos cientos de Mb se esperaba bastante menos, así que el piso es más alto que la intuición.
    `[?]` **No se averiguó la causa.** La hipótesis es que parte de las referencias tiene regiones de baja
    complejidad o repeticiones (poli-A, microsatélites) que coinciden con ventanas de composición
    sesgada; no se probó. **Qué cambia:** cualquier conteo de off-target que no traiga su nulo puede
    estar leyendo ese piso como señal. `V-ATPase B` (0,8827) está por encima de él; `eth` (0,9815) y
    `burs-alpha` (1,0000) están dentro. Para cerrarla: repetir el nulo con permutaciones que además
    conserven los dinucleótidos y ver si el piso baja, y mirar qué ventanas permutadas coinciden.

101. **El largo que el paper declara para las dos V-ATPasas de *Peregrinus maidis* (`DE-01`) no
    coincide con el de las accesiones que cita.** Yao *et al.* 2013 dicen 2.495 nt para la subunidad
    B y 985 nt para la D; NCBI da `KC473163.1` en 2.391 nt y `KC473162.1` en 1.002 nt, las dos
    «mRNA, complete cds» `[M]` (`research/ola6/F3_recomendador_genes/resultados/recuperacion_6filas_verificacion.tsv`).
    La diferencia es de −104 y +17 nt. En cambio `MN815919.1` (`CI-13`) coincide exacto con los 1.911 pb
    del paper. `[?]` **No se averiguó la causa**; la lectura más barata es que el paper cuente UTR o
    una versión previa de la secuencia, y no se probó. **Qué cambia:** hasta saberlo, la secuencia que
    se tamice para `DE-01` es la de NCBI y no la que describe el texto. Para cerrarla: leer la
    sección de métodos de la que sale el 2.495 y comparar con el registro de GenBank.
