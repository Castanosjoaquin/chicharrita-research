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
