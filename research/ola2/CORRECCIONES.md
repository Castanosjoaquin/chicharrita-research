# CORRECCIONES — lo que el corpus oficial cambia de la ola 1

Reconciliación hecha el 17 de octubre de 2026, con los cinco reportes de la ola 2
en mano. Una entrada por punto donde el material oficial **confirma, matiza,
corrige o refuta** algo que la ola 1 había escrito sin acceso a él.

Cada entrada dice qué decíamos y dónde, qué dice la evidencia nueva y de qué
archivo sale, el veredicto y la consecuencia para nuestras líneas de trabajo.

Veredictos: **confirmado** (el corpus sostiene lo que decíamos) · **corregido**
(decíamos algo inexacto y ahora sabemos lo correcto) · **refutado** (lo que
decíamos es falso) · **incierto `[?]`** (la evidencia queda en conflicto).

Regla que se aplicó en todo el documento: **el corpus no gana automáticamente por
ser oficial.** Donde el corpus y la literatura pública se contradicen, se reportan
las dos. Donde dos investigaciones de esta ola se contradijeron entre sí, se
adjudica con la evidencia y se deja dicho cómo.

---

# Parte I — Los tres supuestos de la ola 1

## S1 — La identidad de los patógenos y qué síntoma causa cada uno

**Qué decíamos.** Cuatro agentes: MRFV, MSMV, un fitoplasma y *Spiroplasma
kunkelii* (`SINTESIS_v1.md` §2; `R1/REPORT.md` §3). La asignación de síntomas que el
equipo traía de la charla —uno afecta los granos, el otro el tallo— ya había sido
**corregida en la ola 1** con un experimento de inoculación separada: la reducción
de grano fue significativamente mayor con el espiroplasma (P < 0,01) y la
reducción de altura no fue significativamente distinta entre agentes.

**Qué dice el corpus.** Nada sobre esto. Ningún paper compara patógenos del
complejo ni asigna síntomas, y MSMV no aparece en ninguno
(`ola2/W1_papers/REPORT.md`). El corpus **no es la fuente** para S1.

**Veredicto: la corrección de la ola 1 queda en pie, y el corpus no la toca.**
Lo que sí cambia es la identidad de dos de los cuatro agentes, abajo.

### S1.a — El fitoplasma: confirmado y ahora medido

La ola 1 (R5) había corregido que el agente es *'Candidatus* Phytoplasma zeae',
con genoma completo desde 2016. Esta ola lo verificó por consulta directa a NCBI
Datasets, **bajó el genoma y lo midió con sus propios scripts**: `GCF_001712875.1`,
una sola secuencia `NZ_CP015149.1`, cepa M3, 576.118 pb, 28,462 % GC, cero N, 565
genes y 540 CDS, reanotación RefSeq del 07-06-2026 (`ola2/W4_genomas/REPORT.md` e
`inventario_genomico.json`). **Confirmado y cuantificado.**

> **Nota de adjudicación.** La primera entrega de W4 afirmó lo contrario —que el
> taxón 202462 no tenía ningún ensamblado— porque consultó el NCBI por el nombre
> común «maize bushy stunt phytoplasma» en lugar del taxid. El orquestador
> verificó las tres consultas (`/genome/accession/GCA_001712875.1`,
> `/genome/taxon/202462` con `total_count: 2`, y `/taxonomy/taxon/202462`) y le
> devolvió la corrección, que W4 aplicó y midió. **La ola 1 tenía razón.** La
> lección operativa quedó incorporada al script de consulta: resolver el taxid
> primero, porque un cero por nombre común no es una ausencia.

### S1.b — MSMV: el cuarto agente sigue sin definir, y ahora sabemos por qué `[?]`

**Qué decíamos.** «MSMV quedó sin identificar taxonómicamente», con dos taxid
candidatos anotados sin resolver (`00_meta/PREGUNTAS_ABIERTAS.md`, pendiente 7 de
R2).

**Qué dice la evidencia nueva.** La sigla mapea a **dos taxones de familias
virales distintas, con vectores distintos**: *maize striate mosaic virus* (TaxID
2025388, Geminiviridae, género *Mastrevirus*, ensamblados `GCF_004788335.1` y
`GCF_004130985.1`) y *Tenuivirus zeae* (TaxID 3052767, Phenuiviridae,
`GCF_002867025.1`) (`ola2/W3_bases_datos/REPORT.md` y `bases.json`).

**Veredicto: incierto `[?]`, y la incertidumbre está ahora acotada con precisión.**
W4 reportó el cuarto agente como «resuelto: *Mastrevirus striatis*, 2 RefSeq de
2.746 nt», que es una de las dos ramas; W3 mostró que la sigla no distingue entre
ambas. Se adjudica a favor de W3 por ser estrictamente más completo: los dos
taxones existen y el corpus no dice cuál es. **Consecuencia:** mientras no se
resuelva, cualquier diseño contra MSMV apunta a un blanco indefinido, y es
pregunta directa para el investigador.

## S2 — «BLAST separa en porciones y calcula la termodinámica»: **cerrado**

Este era el supuesto prioritario y es el que el corpus permitía responder como
corresponde: mirando las herramientas reales, no la literatura general.

**Qué decíamos.** Que la frase mezclaba dos cosas: alineamiento local (BLAST,
Bowtie) para tamizaje de off-targets y elección de regiones conservadas, y
termodinámica de hibridación y estructura (ΔG, accesibilidad, asimetría de
extremos) que calculan herramientas tipo ViennaRNA (`R2/REPORT.md` §1;
`R1/REPORT.md` §6).

**Qué dice el corpus.** Las dos herramientas oficiales son dsRNA-Engineer y BLAST
del NCBI (`Links de interes.docx`). Sobre ellas, con cita a archivo y línea
(`ola2/W2_herramientas/REPORT.md`):

1. **Ninguna de las dos calcula termodinámica.** El preprint de dsRNAEngineer no
   contiene ni una ocurrencia de *thermodynamic*, *free energy*, *Gibbs*,
   *Vienna*, *fold*, *melting*, *Tm*, *accessibility*, *GC content* ni
   *asymmetry*; y los 48 campos de salida tabular de `blastn` 2.17.0 no incluyen
   ninguno de energía (`ejemplos/salidas/blastn_help_2.17.0.txt`, líneas 95-182).
2. **El motor del tamizaje de off-target no es BLAST: es Bowtie.** Lo declara la
   propia API del servicio (`GET /v1/api/info/option-list`: «the length and
   mismatch parameters of bowtie») y lo prueban los nueve archivos
   `<especie>.<k>.bwt` que el servicio entregó en el paquete de resultados de una
   corrida real.
3. **BLAST hace la otra mitad dentro de la misma herramienta**: homología entre
   plagas en el módulo *screen-target* y anotación contra NR de los ensamblados de
   novo (preprint, p. 8 líneas 127-137 y p. 6 líneas 101-103).
4. **De dónde sale probablemente la frase original `[H]`:** la única termodinámica
   alcanzable desde el enlace que entregó el organizador es **Primer-BLAST**, que
   combina Primer3 con BLAST y calcula la temperatura de fusión de cebadores de
   PCR con la tabla «SantaLucia 1998». Es termodinámica, está dentro de BLAST, y
   no tiene nada que ver con diseñar un ARNdc.

**Veredicto: la hipótesis de la ola 1 era correcta en lo conceptual y algo
imprecisa en la atribución.** Los dos ejes son ortogonales, como decíamos. Pero la
ola 1 atribuía el tamizaje a «BLAST/Bowtie» como familia, y en la herramienta real
las funciones están reparticidas: Bowtie tamiza, BLAST elige región conservada y
anota.

**Consecuencia, y es grande.** En el corpus **no hay ninguna herramienta que
estime eficacia**: ni termodinámica, ni reglas de secuencia, ni modelo entrenado.
Las dos oficiales sólo responden a qué se parece una secuencia. El eslabón de
eficacia es un hueco verificado del material oficial, y eso **baja la vara y corre
el eje de nuestro aporte**: no se trata de modelar mejor que el estado del arte,
sino de decidir mejor con lo que ya se calcula.

## S3 — ARN exógeno frente a ARN no codificante: confirmado, y con una vuelta de tuerca

**Qué decíamos.** Que son cosas distintas: una vía de administración y una clase
de molécula (`SINTESIS_v1.md` §2).

**Qué dice el corpus.** Lo confirma en los hechos: los siete papers aplican ARN
desde afuera y ninguno discute ARN no codificante endógeno como tratamiento. Y
agrega el dato que **más mueve la estrategia de entrega**, que no está enunciado
en ningún paper individual y aparece al cruzar tres:

> **El ARN exógeno entra al apoplasto y al xilema, y no hay evidencia de que entre
> al floema.** Tres sistemas y tres técnicas distintas: P6 lo encuentra restringido
> a xilema y apoplasto; P7 detecta señal en células de la vaina del haz y ninguna
> en tráquea ni floema; P4 documenta captación en xilema y mesófilo esponjoso.

**Consecuencia:** como *Dalbulus maidis* se alimenta de **floema**, la vía de
entrega que el corpus habilita no es la que uno supondría. La hipótesis viable es
la **adquisición durante el sondeo de xilema**, documentada por
electropenetrografía y con antecedente en la propia especie. Esto es nuevo, es del
corpus, y hay que preguntarlo.

---

# Parte II — Biología, eficacia y entrega

## B1 — BioClay y las nucleasas: mitad corregido, mitad confirmado

**Ola 1:** `R3/panorama_industria.md` afirmaba que ninguna fuente abierta atribuía
a BioClay protección medida frente a fotodegradación por UV **ni frente a
nucleasas** `[?]`.
**Corpus:** el paper primario **sí mide** protección frente a RNasa A, con cuatro
réplicas y figura dedicada (`Papers/nplants2016207 (1).pdf`, *Stability of dsRNA
loaded into LDH*, fig. 3e). **No mide UV**: la palabra aparece una sola vez, en la
frase que enuncia el objetivo.
**Veredicto: corregido en la mitad de nucleasas (pasa a `[E]`), confirmado en la
mitad de UV.** Fuerza alta en ambas direcciones.

## B2 — El número del SCMV en maíz estaba mal por seis órdenes de magnitud

**Ola 1:** `R3/REPORT.md` §3.2, citando de segunda mano una revisión: «ARNdc de
origen bacteriano a 3 µg/L logró inhibición total a 30 días».
**Corpus:** el original dice **3 µg de ácido nucleico total por µL**, no por litro;
la dosis aplicada fue 1 mL de una dilución al medio por planta; y **no fue total**:
16/20 y 14/20 plantas resistentes, es decir 4/20 y 6/20 susceptibles
(`Papers/s00299-010-0911-z.pdf`, tabla 3).
**Veredicto: corregido.** Es el ejemplo más claro del costo de citar de segunda
mano, y justifica la regla del repositorio.

## B3 — Y ese mismo paper tiene una incoherencia interna `[?]`

Observación nuestra: en las tablas 2 y 3 de `Papers/s00299-010-0911-z.pdf` la fila
*Non-inoculated controls* figura como S 18/20 —dieciocho de veinte plantas no
inoculadas registradas como susceptibles— con títulos de ELISA comparables a los
de las inoculadas. Tal como está impreso es internamente incoherente.
**Consecuencia:** mientras no se resuelva, los porcentajes de protección de ese
trabajo **no son utilizables** como línea de base cuantitativa; sólo vale su
resultado cualitativo.

## B4 — Saturación del RISC: matizada y endurecida

**Ola 1:** `R1/REPORT.md` §2.5 recogía de *Bactericera cockerelli* que más ARNdc no
siempre es más silenciamiento, con saturación hacia 100 ng/µL.
**Corpus:** en *Diaphorina citri* la mortalidad **sigue subiendo** hasta 1000 ng/µL
mientras el knockdown no correlaciona con la dosis, y el control de ARNdc-GFP a 500
y 1000 ng/µL ya mata significativamente más que el control de sacarosa
(`Papers/Dcitri.pdf`).
**Veredicto: matizado, y en una dirección incómoda.** No hay un umbral universal
de saturación: hay **dos desenlaces que se mueven en direcciones distintas**, y
parte de la mortalidad a dosis alta **no es específica de secuencia**.
**Consecuencia directa sobre nuestro plan:** los experimentos V1 y V3 de
`R2/PROPUESTA.md` tratan hazard ratio y reducción de transcripto como si midieran
lo mismo. No lo hacen, y hay que separarlos.

## B5 — Atribución cruzada de los números de ETH y Burs-α

**Ola 1:** `R1/REPORT.md` decía «supervivencia a día 4 de ~10 % y ~15 %» para
*burs-α* y *eth*.
**Corpus:** en *D. maidis* **los dos genes** dejaron 10 % de supervivientes (día 4
para *burs-α*, día 5 para *eth*); el 17,5 % y el 20 % son de *Delphacodes kuscheli*
(`Papers/finsc-6-1811933.pdf`, fig. 5). El método y los porcentajes de knockdown de
la ola 1 eran exactos.
**Veredicto: corregido.** Es un error de atribución entre especies, del tipo que
sólo aparece leyendo el original.

## B6 — El 95 % de knockdown no es un punto de calibración

**Corpus:** ese valor descansa sobre **tres réplicas biológicas de tres ninfas cada
una** (`Papers/finsc-6-1811933.pdf`, RT-qPCR analyses); las 40 son el n de
supervivencia, no el de la medición molecular.
**Veredicto: matizado.** La prueba de rango V3 de `R2/PROPUESTA.md` sigue siendo
legítima, pero el dato contra el que compara es más blando que su porcentaje.

## B7 — Detectar siRNA no prueba protección, y ahora tampoco lo contrario

**Ola 1:** `R1/REPORT.md` ya advertía la primera mitad.
**Corpus:** P4 agrega la recíproca: con protección sostenida demostrada a 20 días,
**no se detectaron** siRNA de 21-24 nt derivados del ARNdc aplicado por encima del
ruido, pese a sí detectarse los ARN grandes.
**Veredicto: ampliado.** Ni la presencia ni la ausencia de siRNA sirve como
desenlace. Dato `[E]`, mecanismo `[?]`.

## B8 — La entrega mediada por planta funciona en cicadélidos, pero no mata

**Corpus (P6, el trabajo que la ola 1 no había podido abrir):** hoja cortada
sumergida en 7 µg de ARNdc silencia legumaína y naterina a 17 y 24 días
post-alimentación —no a 13— y ATP sintasa β en *Euscelidius variegatus* y
*Scaphoideus titanus* a 14 días. La hoja cortada sube la eficiencia de entrega de
40 % a cerca de 80 % frente a planta entera. **Ninguno de los tres genes afectó la
supervivencia** (`Papers/s10340-023-01670-0.pdf`).
**Veredicto: pendiente resuelto.** Era el rechazo de herramienta registrado en la
ola 1. Confirma que la vía existe en cicadélidos vectores de fitoplasmas, y
advierte que silenciar no es matar.

## B9 — Un método de entrega puede no transferirse entre hemípteros

**Corpus:** la inmersión de ninfas en ARNdc con lipofectamina al 13 % **falló** en
un cicadélido: expresión 0,561 ± 0,036 (n=48) contra 0,414 ± 0,025 (n=21) del
control, es decir **por encima** del control (P6, tabla 1). La misma técnica está
publicada como funcional en *Diaphorina citri* y *Aedes aegypti*.
**Veredicto: matiz fuerte a `R3/panorama_industria.md`.** Nuestra advertencia era
que las magnitudes de persistencia entre portadores no son comparables. El corpus
dice algo peor: **el método puede no transferirse en absoluto**, y hay un resultado
negativo medido y publicado que lo muestra.

## B10 — El largo del disparador no tiene una banda única

**Ola 1:** `R2` daba por típico el rango de 200 a 500 pb.
**Corpus:** depende del organismo que procesa. En insecto, P3 usó 578 y 544 pb; en
planta, P5 usó 147 y 140 pb, P7 un solo siRNA de 21 nt, y P2 reporta
explícitamente que subir de 120 a 231 nt **no dio ganancias** de silenciamiento.
**Veredicto: corregido para la mitad vegetal.** La restricción de 200-500 pb no es
defendible para un candidato dirigido a la planta, **y dos de los cuatro
candidatos del EPILAB apuntan al MRFV**.

## B11 — Qué es y qué no es el paper de MRFV del corpus

**Corpus:** P2 **no demuestra silenciamiento del MRFV**: convierte al MRFV en
herramienta para silenciar genes del maíz. Es la confusión más probable al citarlo.
Lo que sí aporta: arquitectura del genoma (6.337 nt, dos cápsides
carboxi-coterminales CP1 y CP2, marafibox, ORF P43), el único sitio que tolera
inserciones (unión HEL/POL, nt 3709/3710; el 3'UTR, POL/CP1 y el inicio de la
poliproteína son letales) y la primera tasa de transmisión del MRFV por *D. maidis*
de fuente primaria: **19/49 plantas, 39 %**.

## B12 — El corpus no cubre MRFV ni MSMV como blancos de ARNdc `[?]`

No hay ni un trabajo de ARNdc, SIGS o HIGS contra ninguno de los dos. Los dos virus
de maíz del corpus, SCMV y MDMV, son potyvirus transmitidos por pulgones y **no
pertenecen al complejo del achaparramiento**. Lo que el corpus sí demuestra es que
el maíz es hospedador competente para la tecnología, que es un prerrequisito
distinto. **El hueco que la ola 1 había declarado sigue abierto.**

## B13 — Cero evaluaciones de no objetivo, y criterios de diseño mínimos

**Corpus:** ninguno de los siete papers evalúa organismos no objetivo: ni
polinizador, ni enemigo natural, ni fauna del suelo, ni homología in silico contra
otra especie. El único control de especificidad es intraespecífico. Y los criterios
de diseño son mínimos: ningún paper usa asimetría termodinámica, accesibilidad
estructural ni selección de hebra guía; el tratamiento más completo es tBLASTn para
el ortólogo más BLASTn contra el transcriptoma propio (P3).
**Veredicto: confirmado desde el material oficial.** El riesgo no objetivo es un
hueco de la **práctica publicada**, no sólo de nuestra información. Es la medida
exacta del espacio que puede ocupar un equipo de bioinformática.

---

# Parte III — Herramientas y datos

## H1 — Qué es realmente dsRNA-Engineer

Corrida real sobre secuencia pública (proyecto `6fab2304bf273f5e`, PZ371507.1):
237 on-targets en *D. maidis*, 70 off-targets en *Zea mays*, 67 en *Apis
mellifera*. Descompuesto contra los archivos Bowtie crudos: 237 = 190 (21 nt) + 47
(16 nt); maíz 70 = 70 (16 nt); abeja 67 = 67 (16 nt)
(`ola2/W2_herramientas/REPORT.md` y `ejemplos/`).

Tres cosas que esto revela y que ningún folleto dice:

1. **El conteo de off-target está dominado por la condición de 16 pb**, no por el
   tamaño de corte de Dicer-2 que la propia herramienta declara relevante: 70/70 y
   67/67 de los aciertos vienen de los 16 pb.
2. **El conteo mezcla ventanas riesgosas con parálogos alcanzados:** los 70
   aciertos en maíz son 28 posiciones distintas de la consulta repartidas en 60
   transcriptos; los 67 en abeja, 22 posiciones en 39 transcriptos.
3. **Su conteo on-target mide cobertura de ensamblado, no identidad de blanco:**
   su *D. maidis* es un ensamblado de novo de una sola corrida pública
   (SRR15166998, Trinity) y los 190 aciertos perfectos cayeron todos en un contig
   que cubre 210 de los 615 nt de un ARNm publicado.

**Consecuencia:** el número que la herramienta oficial devuelve **no es
interpretable como riesgo** sin desagregarlo. Esa desagregación es un aporte
nuestro, barato y defendible.

## H2 — Hay un transcriptoma del vector, y hay tres, y ninguno es el que usa el grupo

**Ola 1:** `R2/REPORT.md` declaró que no existe anotación génica pública de *D.
maidis* y trató la construcción del transcriptoma como el **camino crítico** del
proyecto.
**Evidencia nueva, de tres fuentes que se complementan:**

- Hay **tres** transcriptomas TSA, no uno: `GITV00000000` (56.117 secuencias,
  94.702.486 pb), `GHCC00000000` (55.286) y `GCWP00000000` (25.662)
  (`ola2/W3_bases_datos/REPORT.md`). La ola 1 conocía sólo el primero, y con
  56.116 secuencias tomado del artículo contra 56.117 que declara el NCBI `[?]`.
- dsRNA-Engineer tiene el suyo propio, de novo, parcial y **no descargable**
  (`ola2/W2_herramientas/REPORT.md`).
- **El grupo que publica usa un cuarto, propio y no publicado:** P3 no usa ninguno
  de los anteriores, sino un ensamblado del laboratorio respaldado por una tesis de
  maestría de la UNNOBA de 2018 (`Papers/finsc-6-1811933.pdf`, ref. 32).

**Veredicto: corregido, y la consecuencia es buena.** El camino crítico **deja de
serlo**: hay transcriptomas descargables hoy. Y la pregunta 9 al investigador se
reformula: no es «cuál de los dos» sino «cuál de los cuatro, y nos pasan el suyo».

## H3 — El vector no tiene genes anotados, y eso no bloquea tanto como creíamos

**Verificado al 17-10-2026** (`ola2/W4_genomas/REPORT.md`): *D. maidis* tiene tres
ensamblados y **ninguno está anotado**; la base Gene tiene 37 registros y **los 37
son mitocondriales** —cero genes nucleares—, contra 24.178 de *Macrosteles
quadrilineatus* (`ola2/W3_bases_datos/REPORT.md`).

Pero la falta de anotación **no impide ubicar genes**: 64 de 64 proteínas de *M.
quadrilineatus* —Dicer, Argonauta-2, exportina-5, bicaudal C, bursicona y 16
subunidades de V-ATPasa— alinean con cobertura 1,00 contra el genoma del vector, y
8 de 8 de la familia SID1 con cobertura ≥ 0,98.
**Consecuencia:** el rótulo «database general de genes» del `.docx` **no aplica a
la especie blanco**, y el camino practicable es la ortología desde el cicadélido
anotado más cercano.

## H4 — Los tres ensamblados del vector no son equivalentes

**Ola 1:** los listaba en pie de igualdad.
**Medido:** completitud estilo BUSCO (proxy con miniprot sobre insecta_odb10) de
**97,7 %** para el de Sanger `GCA_975739785.1`, **68,8 %** para el borrador
CIAP-INTA y **35,5 %** para el haplotipo alternativo, que tiene 55,89 % de
ortólogos ausentes. El proxy se calibró contra el 68,6 % de BUSCO que publica el
preprint del ensamblado CIAP-INTA: nuestro valor sobre el mismo ensamblado es
68,76 % (`ola2/W4_genomas/REPORT.md`).
**Veredicto: corregido.** Hay una referencia claramente mejor, y el haplotipo
alternativo no es utilizable. **Límite declarado:** no se corrió BUSCO oficial
—compleasm no resuelve en Bioconda—, así que los tres porcentajes son de un proxy
propio, calibrado pero propio.

## H5 — Más datos públicos de los que la ola 1 registraba

- **37 corridas SRA**, de las cuales 23 de RNA-seq (110,1 Gbases) y 10 de WGS
  (129,8 Gbases), contra las 20 que anotaba la ola 1.
- **PRJNA631706**: 16 corridas de RNA-seq del vector **expuesto al MRFV contra
  naive**, a 4 h y 7 días. La ola 1 no lo registraba y es directamente relevante.
- ***Dalbulus elimatus*** tiene genoma (`GCA_976225285.1`, nivel cromosoma, sin
  anotar): el congénere más cercano, que la ola 1 no registraba.
- La anotación vigente de *S. kunkelii* es del 13-12-2025, con 1.951 genes.
- **Genoma anotado no implica genes indexados:** *'Ca.* P. zeae' tiene 0 registros
  en la base Gene pese a sus 581 genes; la anotación hay que sacarla del GFF3 o de
  la base protein.

## H6 — El tamizaje de off-target es barato

6.067 ventanas de 21 nt de los CDS públicos del MRFV contra 575,1 Mb de seis
transcriptomas **en 27,6 segundos** (`ola2/W4_genomas/REPORT.md`). Con cero
coincidencias exactas en maíz y en *Apis mellifera*, 3 en *Coccinella
septempunctata* y 1 en *Macrosteles quadrilineatus*.
**Consecuencia:** el costo computacional **nunca fue el problema**. Lo caro es el
criterio, no el cómputo.

---

# Parte IV — Los candidatos de EPILAB

La ola 1 giraba alrededor de un conjunto de candidatos que no teníamos y que era
«la única dependencia externa» de la propuesta
(`R2/PROPUESTA.md` §8, riesgo 1; `00_meta/PREGUNTAS_ABIERTAS.md`, pregunta 2).
**Ya están.** Son cuatro, y esto es lo que resultó de caracterizarlos.

## E1 — Identificación: los cuatro, con confianza alta y por alineamiento local

- **MP_MRFV** es el CDS anotado 332..1594 de `NC_002786.2`, copiado de extremo a
  extremo (1263/1263 nt, 100,000 %, *putative movement protein* `NP_115455.2`).
- **CP_MRFV** es la región codificante de cápside en 5674..6201 dentro del CDS de
  la poliproteína (528/528 nt, residuos 1850-2025 de `NP_115454.2`).
- **BicC_Dm** es el transcrito de Bicaudal C con 17 bloques exónicos en el
  cromosoma 3 (`OZ319706.1`), 72,6 % de identidad de aminoácidos con el ortólogo de
  *H. vitripennis*.
- **ATPaseD_Dm** es un fragmento parcial del CDS de la **subunidad D de la ATPasa
  vacuolar de protones**, 3 exones en el cromosoma 8 (`OZ319711.1`), 99,4 % de
  identidad en 163 residuos.

Todo con herramientas locales; ninguna secuencia salió del entorno
(`ola2/W5_secuencias_epilab/REPORT.md` y `analisis/`).

## E2 — La predicción central de la ola 1 se cumplió: cero de cuatro contra mollicutes

Ninguno de los cuatro candidatos apunta al fitoplasma ni al espiroplasma. Dos van
al virus y dos al vector. Es exactamente lo que la ola 1 predijo desde la ausencia
de maquinaria de RNAi en mollicutes, verificada sobre 126.874 proteínas anotadas.
**Veredicto: confirmado, y por partida doble**, porque el corpus de papers tampoco
contiene un solo trabajo que proponga silenciar un gen de mollicute
(`ola2/W1_papers/REPORT.md`).

Y el argumento se endurece: ahora **no se apoya en falta de datos**. Los dos
mollicutes del complejo tienen genoma completo y anotado —*S. kunkelii* 1.514.561
pb y *'Ca.* P. zeae' 576.118 pb—, así que la ausencia de maquinaria no se puede
atribuir a genomas faltantes.

## E3 — El hallazgo más accionable de toda la ola 2: la región de cápside no cubre los aislados de la región

La región elegida de **CP_MRFV es 100 % idéntica sólo al aislado de Costa Rica**.
Contra los 45 registros brasileños de MRFV la identidad cae a **91,5-93,5 %**, y la
mediana de siRNA de 21 nt con apareamiento perfecto es **44 de 180** (mínimo
10/180). La región de MP_MRFV sólo tiene 3 registros con los que compararse:
180/180 en la referencia y 54/180 en el aislado de EE. UU. Y **en GenBank no hay
ninguna secuencia de MRFV de la Argentina**: de 71 registros, 45 son de Brasil, 4
de EE. UU., 2 de Ecuador, 1 de Costa Rica y 19 sin país.

Calculado dos veces por métodos independientes —btop y búsqueda de subcadena
exacta— con resultados idénticos (`ola2/W5_secuencias_epilab/REPORT.md`).

**Consecuencia, y es una decisión, no una observación.** El mecanismo de RNAi
exige apareamiento casi perfecto. Un candidato diseñado sobre el aislado
costarricense puede perder la mayor parte de sus siRNA efectivos frente a un
aislado local. **Esto es exactamente lo que el término de conservación de nuestra
propuesta existía para detectar, y ahora tiene un caso real y medido.** Es, además,
un aporte que podemos llevar al investigador el día uno.

## E4 — El riesgo de off-target no está donde lo buscábamos

Con el criterio de coincidencia perfecta de ≥19 nt contiguos, las regiones del
vector tienen **30 siRNA (22 de ellos 21/21)** sobre el ortólogo de bicaudal C de
*H. vitripennis* y **7** sobre la ATPasa. En *Apis mellifera*, *Harmonia axyridis*
y *Folsomia candida*: **cero**. En maíz: sólo tres siRNA con un bloque de 19 nt
exactos, ninguno 21/21.
**Veredicto: reordena la prioridad del eje de riesgo.** El riesgo está en los
**cicadélidos no objetivo**, no en el maíz ni en los polinizadores.
**Límite declarado:** *H. vitripennis* es un sustituto; no existe transcriptoma
público de cicadélidos nativos no plaga ni de parasitoides de *Dalbulus*, que
serían los no objetivo relevantes. Los ceros de esas categorías son provisionales
por sustitución de especie.

## E5 — No pudimos reproducir la columna «Nro de eficientes por gen»

La planilla declara 114, 35, 199 y 33 siRNA eficientes por gen. Una
reimplementación local de los criterios publicados da 87/21/136/26 contando una
hebra y 179/43/259/62 contando cualquiera, y **ninguna de las 2.132 combinaciones
de parámetros probadas reproduce los cuatro números declarados**
(`ola2/W5_secuencias_epilab/REPORT.md`).
**Veredicto: incierto `[?]`, y es la primera pregunta técnica para el
investigador.** W2 agrega por qué importa: dsRNA-Engineer **no clasifica siRNA como
eficientes**, cuenta aciertos dentro y fuera del blanco. Saber de dónde sale esa
columna cambia cómo hay que leer los cuatro candidatos.
**Límite declarado:** si-Fi21 no es ejecutable en este entorno (binario de Windows
con interfaz gráfica) y dsRNA-Engineer no se pudo correr con estas secuencias por
la regla de confidencialidad, así que lo corrido es una reimplementación propia.

## E6 — Dos detalles que hay que arreglar antes de usar la planilla

- **Corrimiento de coordenadas:** tres regiones usan base 1 inclusiva, pero la de
  CP_MRFV, declarada 200-400, **empieza en la posición 201**. Reconstruir por
  coordenada en vez de por subcadena introduce un corrimiento de un nucleótido en
  ese candidato.
- **Procedencia:** ATPaseD_Dm es 100,000 % idéntica a las posiciones 190-680 del
  contig `GCWP01010867.1` del transcriptoma TSA público de Johnson et al. 2018, lo
  que hace muy probable ese origen `[H]`; BicC_Dm no tiene equivalente exacto
  (mejor coincidencia 99,72 %, 7 desajustes, contra `GITV01000968.1`), así que su
  origen es indecidible `[?]`.

## E7 — Corrección de nomenclatura

`R1/REPORT.md` §4.6 llama al blanco «subunidades B y D de la ATP sintasa
vacuolar». El tblastn local lo identifica sin ambigüedad como **subunidad D de la
ATPasa vacuolar de protones (V-ATPasa)**, que es un complejo distinto de la ATP
sintasa (F-ATPasa). Unificado en el glosario.

## E8 — Un dato que puede ser una ventaja de diseño `[H]`

MP_MRFV tiene **dos marcos largos simultáneos**: tblastn local alinea la
poliproteína `NP_115454.2` en el marco +3 y la proteína de movimiento
`NP_115455.2` en el +1, los dos al 100 %. Un ARNdc sobre esa región atacaría a la
vez la proteína de movimiento y parte del gen de la replicasa. Es hipótesis
nuestra y hay que verificarla con el investigador.

---

# Qué queda abierto después de esta ola

Las preguntas nuevas, más precisas que las de la ola 1 porque están ancladas en
archivos concretos, están en `00_meta/PREGUNTAS_ABIERTAS.md` y resumidas en
`SINTESIS_V2.md`. Las cuatro que más mueven el plan:

1. ¿De dónde sale la columna «Nro de eficientes por gen», que no pudimos
   reproducir con ningún criterio publicado?
2. ¿Sobre qué referencia se eligieron las posiciones de la planilla, y sobre qué
   aislado de MRFV, dado que la región de cápside sólo coincide al 100 % con el
   aislado costarricense y no hay secuencias argentinas públicas?
3. ¿Cuál de los cuatro transcriptomas del vector usa el laboratorio, y nos pasan
   el suyo?
4. ¿Cuál de los dos taxones es «MSMV»?
