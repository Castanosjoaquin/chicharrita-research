# Viabilidad de las líneas de ataque de la ola 1, contra el material genómico real

Cruce entre `research/R4_frontier_ml_rna/lineas_de_ataque.md` y lo que efectivamente
bajamos y medimos el 17 de octubre de 2026 (`inventario_genomico.json`, `REPORT.md`).
Cada línea recibe **un** veredicto: *viable con lo que hay*, *viable sumando X*, o
*inviable*. Sin "habría que ver".

Marcadores: `[E]` establecido, `[R]` reportado, `[H]` hipótesis nuestra, `[?]` incierto.

> **Corrección del 17 de octubre de 2026.** Una versión anterior de estos archivos decía
> que el agente del achaparramiento rojo no tenía genoma. Sí lo tiene: el taxid 202462 es
> '*Candidatus* Phytoplasma zeae' y su cromosoma está completo y anotado desde 2016
> (`GCF_001712875.1`, 576.118 bp, 565 genes en nuestro conteo). No cambia ningún veredicto
> de esta tabla —ninguna de las cuatro líneas depende de ese genoma, porque los mollicutes
> no tienen maquinaria de RNAi—, pero sí agrega un genoma anotado más al panel contra el
> que se puede tamizar off-targets en L3 `[E]`.

## Veredicto en una pantalla

| Línea | Veredicto | El dato que lo decide |
| --- | --- | --- |
| **L1** Tamizaje multiobjetivo auditable con incertidumbre | **Viable con lo que hay** | Todo lo genómico que pedía está descargado y medido; los candidatos del EPILAB, que la ola 1 daba por faltantes, llegaron en el corpus (`YHat-Biotech/Sequences_EPILAB.xlsx`) |
| **L2** Validación retrospectiva en hemípteros | **Viable con lo que hay** | No depende de genomas; las cuatro accesiones de ARNm del trabajo de referencia (PZ371507–PZ371510) están verificadas y vigentes |
| **L3** Mapa de riesgo fuera de blanco ponderado | **Viable sumando iBeetle-Base y un mapeo de ortología** | El panel de seis transcriptomas no objetivo corre en 27,6 s; lo que falta son las etiquetas de esencialidad, que no son datos de secuencia |
| **L4** Ajuste fino de un modelo fundacional | **Inviable** | El material genómico no aporta ni una etiqueta de eficacia; el cuello de botella de L4 sigue intacto |

---

## L1 — Tamizaje multiobjetivo auditable con incertidumbre explícita

| Dato que pide la línea | ¿Está? | Evidencia concreta |
| --- | --- | --- |
| Candidatos del EPILAB para puntuar | **Sí** `[E]` | Cuatro, con región elegida, en `YHat-Biotech/Sequences_EPILAB.xlsx` (manifiesto, sección 6). Era la única dependencia externa declarada de L1 |
| Transcriptoma de maíz para el off-target en el cultivo | **Sí** `[E]` | `GCF_902167145.1`, 76.549 transcriptos, 162.712.215 bp, GC 49,5 %, anotación RefSeq `-RS_2025_02`; descargado y medido |
| Genoma del vector para el off-target intraespecífico | **Sí, el genoma; no, los transcriptos** `[?]` | `GCA_975739785.1`, 972,2 Mb, completitud 97,7 %, **sin anotación**. El filtro corre contra el genoma; contra un conjunto de transcriptos, no, porque no existe (TSA = 0) |
| Ubicar los genes blanco en el vector | **Sí** `[E]` | 64/64 proteínas de *Macrosteles quadrilineatus* (Dicer, Ago-2, bicaudal C, 16 subunidades de V-ATPasa, bursicona) alinean con cobertura 1,00 sobre el ensamblado; `work/W4/ortologos/dmaidis_vs_macrosteles.json` |
| Transcriptomas de organismos no objetivo | **Sí, especies modelo** `[?]` | *A. mellifera*, *C. septempunctata*, *C. carnea*, *F. candida*: 575,1 Mb escaneables en 27,6 s. No son las especies del agroecosistema argentino |
| ViennaRNA para accesibilidad y plegado | No es un dato genómico | Fuera del alcance de W4; se instala desde Bioconda |
| Características y coeficientes de dsRIP | No es un dato genómico | Figshare, según la ola 1; W4 no lo verificó |

**Veredicto: viable con lo que hay.** Los dos insumos genómicos críticos —transcriptoma de
maíz y genoma del vector— están en disco y medidos, y los candidatos a puntuar llegaron
con el corpus. La tubería de cinco módulos se puede construir y correr esta semana.

**Con dos salvedades que hay que escribir en la ficha de cada candidato, no en una nota al
pie.** Primera: el módulo 4 (tamizaje por semilla) **contra el propio vector** corre sobre
genoma y no sobre transcriptos, de modo que no distingue un acierto en un exón de uno en
un intrón ni pondera por expresión; eso se resuelve recién cuando exista el transcriptoma
ensamblado desde las 23 corridas de SRA `[H]`. Segunda: las coordenadas de la planilla de
EPILAB (`BicC_Dm` 264-563, `ATPaseD_Dm` 151-450) están referidas a **una secuencia que la
planilla trae entera**, no a un transcripto público; mientras no exista anotación del
vector, cualquier traducción de esas coordenadas a posiciones genómicas la tenemos que
hacer nosotros por alineamiento, y conviene declararla como paso del método `[H]`.

---

## L2 — Validación retrospectiva del puntaje contra el RNAi publicado en hemípteros

| Dato que pide la línea | ¿Está? | Evidencia concreta |
| --- | --- | --- |
| dsRNA publicados en hemípteros con efecto medido | **Sí, decenas** `[R]` | Es trabajo de lectura, no de descarga; el corpus aporta tres artículos directamente usables (`Papers/finsc-6-1811933.pdf`, `Papers/s10340-023-01670-0.pdf`, `Papers/Dcitri.pdf`) |
| Secuencias de los transcriptos blanco de esos trabajos | **Sí, para los cuatro del trabajo en la especie blanco** `[E]` | PZ371507 (*eth* *D. maidis*, 615 nt), PZ371508 (*burs-α* *D. maidis*, 468 nt), PZ371509 (*eth* *D. kuscheli*, 645 nt), PZ371510 (*burs-α* *D. kuscheli*, 480 nt); verificadas por E-utilities, actualizadas al 13-06-2026 |
| Genoma del vector para ubicar esas regiones | **Sí** `[E]` | `GCA_975739785.1`; `eth` no tiene ortólogo anotado por nombre en ningún proteoma de hemíptero RefSeq, así que el camino es la accesión de GenBank, no la ortología `[E]` |
| Partición por gen y por especie | No es un dato | Es diseño experimental del protocolo |
| Un conjunto público curado de eficacia en hemípteros | **No existe** `[E]` | Construirlo es el entregable de la línea |

**Veredicto: viable con lo que hay.** L2 es la línea que menos depende de W4: su insumo es
literatura, y el material genómico sólo sirve para anclar las secuencias. El riesgo que la
ola 1 le anotó —n de dos dígitos y sesgo de publicación— no lo cambia ningún archivo que
hayamos bajado.

---

## L3 — Mapa de riesgo fuera de blanco ponderado por consecuencia

| Dato que pide la línea | ¿Está? | Evidencia concreta |
| --- | --- | --- |
| Transcriptoma de maíz | **Sí** `[E]` | `GCF_902167145.1` rna.fna, 76.549 secuencias |
| Transcriptoma de *D. maidis* | **No** `[E]` | TSA = 0; hay que ensamblarlo desde 23 corridas de RNA-seq (110,1 Gbases) |
| Transcriptoma de *Apis mellifera* | **Sí** `[E]` | `GCF_003254395.2`, 27.887 transcriptos; genoma y GFF3 también descargados |
| Enemigos naturales y fauna del suelo | **Sí, subrogantes modelo** `[?]` | *C. septempunctata* 25.480, *C. carnea* 19.671, *F. candida* 42.425 transcriptos. No son las especies locales |
| Que el conteo de coincidencias sea computable | **Sí, y es barato** `[E]` | 6.067 21-meros contra 575,1 Mb en 27,6 s con `scripts/08_tamizaje_factibilidad.py`, sin índice |
| Etiquetas de esencialidad génica | **No, y no están en el NCBI** `[E]` | iBeetle-Base (*Tribolium castaneum*); no se descargó ni se verificó su licencia en esta ola |
| Ortología entre *T. castaneum* y el panel | **Construible** `[H]` | Con las proteínas RefSeq de los no objetivo (31.163 a 34.269 por especie, ya bajadas) y `miniprot`, igual que la corrida 6.1 del reporte |
| Benchmark para validar el índice | **No existe** `[E]` | Lo declara el propio relevamiento del subcampo (ola 1) |

**Veredicto: viable sumando las etiquetas de esencialidad de iBeetle-Base y un mapeo de
ortología que las transfiera al panel.** Ninguna de las dos cosas que faltan es un dato de
secuencia: todo lo genómico que L3 pedía está descargado. El costo del proyecto está, como
la ola 1 anticipó, en el curado y en la ortología, no en el algoritmo.

Un resultado de W4 que L3 debería incorporar tal cual: con el criterio binario de
coincidencia exacta 21/21, una secuencia viral pública inocua ya produce **tres 21-meros
solapados en *Coccinella septempunctata* y uno en *Macrosteles quadrilineatus***, y cero
en maíz y en *Apis*. El conteo crudo marca riesgo donde no hay ninguna consecuencia
conocida, que es exactamente el argumento de la línea `[H]`.

---

## L4 — Ajuste fino de un modelo fundacional de ARN para eficacia de dsRNA en insectos

| Dato que pide la línea | ¿Está? | Evidencia concreta |
| --- | --- | --- |
| Cientos de dsRNA en hemípteros con lectura cuantitativa | **No** `[E]` | Ninguna base del NCBI contiene etiquetas de eficacia de RNAi; la búsqueda de material genómico no cambia el conteo de la ola 1 (6 construcciones en la especie blanco) |
| Negativos reales (dsRNA probados que no silenciaron) | **No** `[E]` | No publicados |
| Secuencias de entrada abundantes | Sí, irrelevante | Hay 972 Mb de genoma del vector y 162 Mb de transcriptos de maíz; sobran secuencias y faltan etiquetas |
| Protocolo de partición sin fuga | No es un dato | Es diseño |

**Veredicto: inviable, y el material genómico no la mueve.** La condición explícita que la
ola 1 fijó para reactivarla —cientos de dsRNA en hemípteros con negativos reales— sigue
sin cumplirse, y nada de lo que se puede bajar del NCBI la acerca. Vale la pena decirlo
con precisión porque es contraintuitivo: ahora tenemos **más** datos genómicos que en la
ola 1 (un genoma del vector de calidad de referencia, con 97,7 % de completitud) y eso
**no reduce en nada** la distancia a L4. Lo que falta no es secuencia.

---

## Una línea que el material genómico habilita y la ola 1 no tenía

No reemplaza a ninguna de las cuatro y no compite por el mismo lugar, pero sería negligente
no anotarla: **ensamblar y anotar el transcriptoma de referencia de *Dalbulus maidis***
desde las 23 corridas públicas de RNA-seq (110,1 Gbases, seis BioProjects), guiado por el
ensamblado de nivel cromosoma de Sanger, y publicarlo. Es el insumo que bloquea
parcialmente a L1 y a L3; no lo tiene nadie en forma descargable (TSA = 0); es trabajo
computacional sin laboratorio; y es exactamente el tipo de recurso abierto y reutilizable
que el eje de innovación abierta del Investigathón pide `[H]`. El riesgo es que consuma
el plazo: un ensamblado *de novo* de ese volumen no es una tarde de trabajo.
