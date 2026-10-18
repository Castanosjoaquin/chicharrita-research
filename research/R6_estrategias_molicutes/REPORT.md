# R6 — Estrategias contra los mollicutes del achaparramiento sin RNAi directo al patógeno

*Candidatus* Phytoplasma zeae (MBSP) y *Spiroplasma kunkelii*, vector *Dalbulus maidis*. Corte: 2026-10-17. Marcadores: `[E]` establecido, `[R]` reportado, `[H]` hipótesis del equipo, `[?]` incierto o contradictorio. Las referencias `R6-xx` están en `sources.json` con su nivel de lectura; el cómputo está registrado en `datos/COMANDOS.md`.

## Veredicto

**No hay una línea nueva, contra el patógeno, que valga la pena abrir como línea principal. Hay una extensión acotada de lo que el equipo ya tiene y una línea complementaria pequeña, condicionada a una respuesta del organizador.**

La extensión es incorporar a L1 de `SINTESIS_V2.md` (priorización auditable, 18 `[H]`) un eje de anotación sobre genes del vector que median la transmisión del mollicute, es decir, RNAi indirecto. Es la única de las vías estudiadas que entra en la pregunta oficial del track. Cuesta unas 40 a 50 horas-persona `[H]` y su límite es duro: el signo del efecto no es predecible y toda la evidencia es de otro fitoplasma en otro cicadélido (R6-16, R6-18; Línea 2 de `lineas_candidatas.md`, 13 `[H]`).

La línea complementaria es la interfaz vector–espiroplasma: proteínas de *S. kunkelii* con ortólogo de papel experimental en adhesión, entrada y transmisión en *S. citri*. Corrió de punta a punta con datos abiertos (PGK con 93,7 % de identidad en 412/412 aminoácidos; modelo en AlphaFold DB para 1.750 de 1.755 entradas del espiroplasma), pero **no entra en la pregunta oficial** porque no usa RNAi, y su verdad de terreno son unos tres a seis determinantes, todos de otra especie (Línea 1, 13 `[H]`). Sólo vale la pena si el organizador acepta propuestas no-RNAi como complemento.

Contra el patógeno directo, **nada es demostrable sin laboratorio**: los antibióticos, los péptidos y los inhibidores de efectores tienen respaldo en otras especies o en cultivo, ninguno en MBSP o *S. kunkelii* en maíz, y no existe verdad de terreno propia para dos de las tres cosas que se querían validar (genes de resistencia mapeados en maíz y esencialidad génica en un mollicute fitopatógeno). Un vacío documentado vale como resultado, y acá hay varios.

**Por qué un equipo de IA aporta donde aporta.** No por un método nuevo (D7, D8) sino porque la decisión puede quedar auditable: cada paso de la verificación corrió con entradas, versiones y salidas registradas, y varias creencias del repositorio cambiaron al abrir los originales. Esa es la ventaja defendible. La desconfianza que pide R4 se aplica a todo lo que propongo: los predictores de efectores publicados se evaluaron sin terceros y con negativos fáciles (sección 6).

**Cuatro cosas que cambian respecto del repositorio** (detalle en la sección 2): (1) el puntero de R1 §4.4 sí tiene fuentes primarias, pero en *S. citri*; (2) la corrección B5 de la ola 2 no se sostiene del todo: el texto y la figura del artículo de ETH y Burs-α discrepan para *eth* en *D. maidis*; (3) la revisión S44 trata de vectores, no de estrategias contra fitoplasmas en general; (4) la ausencia de dominios de RNAi se confirmó por perfiles HMM en los dos genomas y es robusta al umbral.

**Lo que este reporte no hizo** (sección 11): ningún predictor local de péptido señal ni de estructura corrió, y las fuentes se leyeron por pasajes, no linealmente.

---

## 1. Cobertura y nivel de lectura

`sources.json` registra 45 entradas. Las 39 fuentes bibliográficas externas se reparten así: **10 en texto completo** (descargado y consultado por búsqueda dirigida de pasajes y cifras, no por lectura lineal), 5 parciales, 7 sólo con resumen (dos de ellas de acceso cerrado) y 17 sólo con fragmentos que devolvió un buscador. A eso se suman 5 bases de datos consultadas y el conjunto de archivos locales del repositorio. El detalle por fuente está en `sources.json`; esta frase no reemplaza ese desglose.

Las cifras de las secciones siguientes llevan, en cada caso, la referencia. Una cifra que viene de un fragmento o de un resumen lo dice. El repositorio se leyó en R1 §4.2 y §4.4–4.6 completos, CORRECCIONES B5–B8, la matriz de `SINTESIS_V2.md`, `CAMINOS_PROBADOS.md` y `DECISIONS.md` (D1–D8). **No se reabrieron completos** R1 §5, W1, W3, W4 ni R4 y R5.

## 2. Lo que el repositorio ya decía y qué resultó al verificarlo

### 2.1 Los mollicutes del complejo no tienen dominios de RNAi (cierra, para dos genomas, la limitación de D9)

R1 §4.2 contó cero proteínas con dominio PIWI o PAZ en 126.874 proteínas de mollicutes mediante consultas de anotación a UniProtKB/InterPro, y D9 reconoce que no fue una búsqueda por perfiles. En R6 se corrió esa búsqueda sobre los dos genomas del problema con `pyhmmer 0.12.3` y perfiles Pfam fijos (Piwi `PF02171.24`, PAZ `PF02170.29`, Dicer_dimer `PF03368.20`) más RNasa III `PF00636.32` como control de familia. Resultado: **0 aciertos de Piwi, PAZ y Dicer_dimer** en las 522 proteínas únicas de *Ca.* P. zeae (M3), las 1.715 de *S. kunkelii* (CR2-3x) y las 13 del plásmido pSKU146, también en una pasada sin umbral (E ≤ 10). Cada genoma tiene exactamente un acierto de RNasa III, anotado como «ribonuclease III». Los controles positivos (AGO2 y DICER1 humanas, y la Argonauta de *Thermus thermophilus*) aciertan donde corresponde, con e-values de 1e-121 a 1e-27 para los eucariotas.

Hay un matiz de sensibilidad que no se debe ocultar: la Argonauta bacteriana pasa el corte por muy poco (32,1 bits contra 28,9 de umbral). Una Argonauta de mollicute muy divergente podría quedar bajo el corte, pero la pasada sin umbral no muestra ningún acierto, ni siquiera débil. **El cero es robusto para estos tres perfiles y estos dos genomas; no prueba la ausencia de toda maquinaria de silenciamiento ni cubre ORF sin anotar** (falta un tblastn contra el genoma). Sigue valiendo `[E]` para la conclusión de R1 §4.4.

### 2.2 El puntero de R1 §4.4 («molécula pequeña, adhesinas, entrada a células del insecto»): sí tiene fuentes, en otra especie

R1 §4.4 dice que el mollicute no es invulnerable y remite a §4.6, que no lo desarrolla. Se buscó y las tres ramas tienen fuente primaria, pero ninguna en el complejo del maíz:

- *Moléculas pequeñas.* Las tetraciclinas son los únicos antibióticos con efecto supresor demostrado sobre fitoplasmas, y la erradicación completa es difícil (R6-05, texto completo; sin una sola mención de maíz ni de *Dalbulus*). Un cribado in vitro de 40 antimicrobianos contra *Ca.* P. asteris halló cuatro que reducen la acumulación y dos que eliminaron el fitoplasma de las plantas (R6-14, sólo resumen). Para *Spiroplasma*, hay péptidos antimicrobianos con actividad in vitro contra *S. kunkelii* y *S. citri* (R6-29, fuente secundaria que se vio como fragmento), anticuerpos scFv anti-espiralina (R6-28) y la globomicina, que inhibe la peptidasa de señal II (R6-27).
- *Interferencia con adhesinas.* En *S. citri*, anticuerpos anti-Rep3d y competencia con Rep3d recombinante redujeron la invasión de células de cicadélido (R6-11), y el mutante G/6, que carece de los plásmidos pSci1–5 (que codifican las ScARP y otras proteínas), tuvo 82 % menos adhesión y 84 % menos internalización. Las ScARP están descritas como conservadas en *S. kunkelii* (R6-11).
- *Bloqueo de la entrada.* La PGK de *S. citri* se une a la actina del vector y su exceso inhibe la internalización en células (R6-15, sólo resumen). **In vivo**, inyectar PGK o su región mínima PGK-FL5 en cicadélidos infectados redujo la transmisión: la proporción de lotes de tres insectos con cultivo positivo pasó de 58 % con tampón (149/257) a 30 % con PGK (52/176) y 34 % con PGK-FL5 (38/112), p < 0,0001 (R6-10, texto completo). Es una reducción relativa de 41 a 48 %, no «casi 50 %» sin más, y la intervención fue una inyección.

**Estado del puntero: con fuente, pero en *S. citri* y *Circulifer haematoceps*.** No se halló ningún ensayo de este tipo con *S. kunkelii* en *D. maidis* ni con MBSP, y la revisión del patosistema declara que los estudios moleculares de esa interfaz faltan (R6-12). Se propone que R1 §4.4 deje de ser un puntero sin fuente y pase a citar estas.

### 2.3 La revisión S44 trata de vectores, no de estrategias contra fitoplasmas en general

El brief y R1 §4.4 dicen que S44 (Balog et al., *Plants* 15:1664, 2026) concluye que todas las estrategias contra fitoplasmas apuntan al vector o a la planta, nunca al patógeno. En el texto completo (R6-01) el alcance es el manejo de vectores: el artículo dice que los fitoplasmas no son directamente atacables por su vida restringida al floema y que la nanotecnología puede reducir la enfermedad de forma indirecta, y menciona de pasada agentes antimicrobianos entregados con nanopartículas a nivel de planta. **No menciona antibióticos ni tetraciclinas (cero coincidencias).** Lo que el artículo muestra es cuál es su universo, no que la literatura no tenga estrategias dirigidas al patógeno: las tetraciclinas actúan sobre el fitoplasma en la planta (R6-05), aunque no sean aplicables a un cultivo extensivo. La frase correcta para el repositorio es que *en la literatura de manejo de vectores* ninguna estrategia apunta al patógeno directamente.

### 2.4 La corrección B5 (ETH y Burs-α) no se sostiene del todo

CORRECCIONES B5 afirma que en *D. maidis* los dos genes dejaron 10 % de supervivientes (día 4 para *burs-α*, día 5 para *eth*) y que el 17,5 % y el 20 % son de *Delphacodes kuscheli*. Con el texto completo (R6-02) y la figura 5 extraída del PDF y medida en píxeles contra los ejes:

| Gen | Especie | Texto del artículo | Barra de la figura 5 (medida) |
| --- | --- | --- | --- |
| *burs-α* | *D. maidis* | 10 %, día 4 | 9,7 % |
| *burs-α* | *D. kuscheli* | 17,5 %, día 4 | 17,4 % |
| *eth* | *D. maidis* | 10 %, día 5 (con la figura 5A como referencia) | **17,5 %**, leyenda de la figura: día 4 |
| *eth* | *D. kuscheli* | 20 %, día 5 | 20,0 % |

Todas las barras caen en múltiplos de 2,5 %, lo esperable con n = 40 por tratamiento (4/40, 7/40, 8/40). **Para *burs-α* en las dos especies y para *eth* en *D. kuscheli* todo coincide; para *eth* en *D. maidis* el texto (10 %, día 5) y la barra (≈17,5 %, día 4) no coinciden.** B5 siguió el texto. No puedo decir cuál es el valor correcto: puede ser un cambio de día entre texto y figura o un error. Queda `[?]` y es la pregunta 3 de `preguntas_investigador.md`. La conclusión práctica es que el valor de mortalidad de *eth* en *D. maidis* a usar como calibración debe citarse con ese rango (10 a 17,5 %), no como un punto. La afirmación original de R1 («~10 % y ~15 %») tampoco era exacta. Por qué R1 puso ~15 % no se sabe `[?]`; una descripción automática de la figura que devolvió un buscador mostraba valores distintos de las barras reales.

También se confirmó B6: el knockdown (~95 % para *burs-α* y ~90 % para *eth*) descansa en tres réplicas biológicas de tres ninfas cada una (R6-02).

### 2.5 Genomas: tamaños, número de proteínas y un cuarto plásmido

R1 §3.2 y W3 §4.2 daban 1.463.926 pb y 1.514.561 pb para *S. kunkelii* y la diferencia no estaba conciliada. Con el reporte de secuencias de NCBI Datasets: el cromosoma mide 1.463.926 pb y los tres plásmidos de RefSeq suman 22.558 + 20.501 + 7.576 = 50.635 pb, que da exactamente 1.514.561. No se contradecían: contaban objetos distintos. Además, el anuncio del genoma describe cuatro plásmidos (R6-37, fragmento); el cuarto, pSKU146 (14.615 pb), es la accesión aparte `NC_006400.1` y **no está en el ensamblado RefSeq**. Se bajó (13 CDS) y se agregó a la búsqueda de dominios.

Las dos accesiones RefSeq siguen vigentes y completas (`GCF_001712875.1`, anotación `RS_2026_06_07`; `GCF_001274875.1`, anotación `RS_2025_12_13`), con fecha de descarga 2026-10-17. El FASTA tiene 522 y 1.715 proteínas, pero el reporte de NCBI cuenta 524 y 1.775 genes codificantes, porque RefSeq asigna un mismo accesión WP_ a proteínas idénticas (41 repetidas en *S. kunkelii*, hasta 5 copias). **Para análisis por gen hay que usar el GFF, no sólo el FASTA.**

### 2.6 La vía indirecta de R1 §4.6 es real pero estrecha

Las tres fuentes de R1 para el RNAi indirecto (S27, S29, S30) tratan del fitoplasma de la flavescencia dorada en *Euscelidius variegatus*, y en R1 se leyeron como resumen (dos de pago). R6 las vio también como resumen o fragmento (R6-16 a R6-18). Dicen que silenciar la clatrina redujo la colonización y la transmisión; que silenciar el receptor putativo uk1_LRR *aumentó* la colonización; y que silenciar ATP sintasa β reduce el fitoplasma pero también la supervivencia y la fertilidad del insecto. Esto último vuelve ambiguo el resultado: una caída de patógeno en un vector enfermo no es una caída específica. Nada se probó en *D. maidis* ni con espiroplasma ni con MBSP. R1 registra S27 como de 2026 y un listado la fecha en diciembre de 2025: año sin reconciliar.

### 2.7 La entrega oral es mucho más débil que la inyección

R1 resume la evidencia de RNAi en *D. maidis* como favorable. Con el texto completo de los preprints (R6-03, R6-04), el cuadro es más matizado. Para Bicaudal C, la inyección bajó el transcripto 3,2 veces el día 1 y más de 170 veces el día 7; la ingestión, 2,6 y 3,7 veces; la supervivencia de las hembras no cambió (p = 0,9475 por inyección y p = 0,1406 por ingestión), de modo que el efecto es sobre la fertilidad. Para V-ATPasa por vía oral en dieta artificial, la supervivencia a cuatro días fue ≈52 % sin dsRNA, ≈37 % con dsRNA de GFP y ≈18 % y ≈16 % con las subunidades D y B (720 insectos, 6 réplicas): el efecto es de unos 20 puntos porcentuales sobre un testigo que ya muere mucho. Para L1 de `SINTESIS_V2.md`, la vía de entrega debe ser un parámetro explícito de la función de decisión y no un supuesto: lo que mata con fuerza se inyecta.

## 3. Mapa de estrategias

`estrategias.json` tiene 25 entradas (9 del patógeno, 9 del vector, 5 de la planta y 2 de otro tipo), cada una con nivel de validación, madurez, datos públicos, si es computable sin laboratorio y qué evidencia experimental faltaría.

**Sobre el patógeno, sin RNAi.** Las tetraciclinas suprimen síntomas y multiplicación en fitoplasmas de árboles, palmas y vinca, pero el uso agrícola de antibióticos está prohibido en muchos países (R6-05). El cribado in vitro de antimicrobianos (R6-14) es sobre *Ca.* P. asteris y no sobre MBSP. *S. kunkelii* es cultivable in vitro, y es el espiroplasma fitopatógeno más exigente (R6-38); no se halló un cribado moderno de moléculas pequeñas. Sobre la cultivabilidad de los fitoplasmas hay contradicción: una afirmación de cultivo axénico en medios complejos (R6-30, 2012) frente a revisiones de 2021 y 2025 que los describen como en gran parte no cultivables (R6-05, R6-07), y ningún reporte para *Ca.* P. zeae `[?]`. Esto condiciona qué se puede probar: un bioensayo sobre el fitoplasma requiere co-cultivo con tejido vegetal.

El efector SAP11 de MBSP está validado a nivel de mecanismo (R6-06, texto completo): desestabiliza sólo los TCP del maíz de tipo TB1/CYC, impide el desarrollo de la inflorescencia femenina imitando mutantes *tb1* y ningún SAP11 aumentó la fecundidad del vector en maíz; es idéntico entre aislados de México y Brasil, lo que los autores atribuyen a selección purificadora. No se halló ningún inhibidor. En el proteoma M3 existe una proteína 100 % idéntica (116/116 aa) a una SAP11-like de UniProt (`WP_069028078.1`); no puede afirmarse que sea el SAP11_MBSP del artículo, que no da accesión `[H]`. Para SAP54 el único acierto de BLASTP fue débil (40,6 % sobre 32 aa) y no prueba ni homología ni ausencia.

**Sobre la transmisión, del lado del vector.** Hay RNAi funcional en *D. maidis* con cuatro blancos (BicC, V-ATPasa, *burs-α* y *eth*, sección 2) y una dsRNasa cuyo silenciamiento mejora la respuesta oral, con sólo el resumen leído por ser de acceso cerrado (R6-13). Los simbiontes y la paratransgénesis están en estado de hipótesis: un trabajo de 2026 analiza 41 metagenomas públicos de *D. maidis*, se declara exploratorio y correlativo y pide validación experimental (R6-09); los precedentes de RNAi mediado por simbiontes que cita son de pulgón y abeja. El comportamiento (efecto pull–push) es de laboratorio (R6-34). Sobre el control biológico, la aplicación directa de conidios de hongos entomopatógenos no mejoró la mortalidad frente a superficies contaminadas, y los nematodos dieron más de 50 % de mortalidad de adultos sólo en laboratorio (R6-31, R6-32, fragmentos).

**Del lado de la planta.** Los híbridos DK79-10 (retraso de síntomas) y DKB390 (antixenosis y resistencia a *S. kunkelii*) se caracterizaron en cuatro híbridos en Argentina (R6-19, fragmento): sólo fenotipos. La herencia de la resistencia se describe como compleja, con efectos aditivos y de dominancia o epistasia, en un dialelo de cuatro líneas (R6-20, fragmento). **No se halló ningún QTL ni estudio de asociación de achaparramiento en dos búsquedas**: es un vacío documentado. Las pasturas forrajeras evaluadas son hospedantes transitorios o sin salida para MBSP (R6-33).

**2024–2026 que no encajan en las tres categorías.** El trabajo de microbioma ya citado (R6-09) y un preprint de 2026 con AlphaFold 3 para interacciones entre proteínas secretadas de *Liberibacter* o fitoplasma y proteínas del huésped (R6-23, fragmento), sin evaluación seria hallada.

## 4. Qué se puede hacer con cómputo y datos abiertos

| Tarea | Herramienta y versión | Datos | Evaluación independiente hallada | Qué se demuestra sin laboratorio | Resultado de R6 |
| --- | --- | --- | --- | --- | --- |
| Ausencia de dominios de RNAi | `pyhmmer 0.12.3` + Pfam (PF02171.24, PF02170.29, PF03368.20) | RefSeq `GCF_001712875.1`, `GCF_001274875.1`, `NC_006400.1` | Perfiles Pfam con corte GA curado; sensibilidad medida acá con tres controles | Que los dos genomas anotados no codifican esos dominios | **Corrió**: 0 aciertos, robusto al umbral; ver 2.1 |
| Transferencia de blancos por ortología (patógeno) | BLAST+ 2.17.0+, `-seg no`, E ≤ 1e-5 | UniProt `Q7WTU1`, `Q9EV58`, `P19215` vs `GCF_001274875.1` | No buscada | Conservación de determinantes conocidos | **Corrió**: PGK 93,7 % (412/412 aa); espiralina 61,1 % (239/241); P89-like ~62 % |
| Transferencia de blancos hacia *D. maidis* | miniprot, BLAST+ (W4/W5) | Ensamblado y TSA del vector | W4 la mostró funcional sin anotación (no re-verificado) | Una lista de ortólogos y sus off-target | **No se re-corrió** en R6 |
| Estructura de proteínas, bases de modelos | AlphaFold DB API (modelos v6) | UniProt por taxón | AF2 vs cristal en efectores de fitoplasma: RMSD 0,74 y 0,70 Å, n = 2, por los mismos autores (R6-07) | Disponibilidad y confianza de modelos | **Corrió**: *S. kunkelii* 1.750/1.755 (99,7 %); *Ca.* P. zeae 5/485 (1,0 %); sin PDB en ambos |
| Estructura local de proteínas sin modelo | AF2/ColabFold | — | Mismo n = 2 | Un modelo, no una función | **No corrió** (sin GPU; secuencias a un servicio de terceros) |
| Péptido señal, transmembrana, efectores | SignalP, TMHMM, Phobius (licencia); DeepSig 0.9 (sin modelos) | — | PhyEffector: F1 0,9761 con 64 negativos de KEGG; LEAPH 95,3 % (fragmento); sin evaluación de terceros | Un inventario de candidatos | **No corrió**: ver `datos/COMANDOS.md` §7 |
| Esencialidad génica | Ortología hacia datos de Tn5 | JCVI-syn3.0/3A, *M. genitalium*, *Mesoplasma florum* | Modelo metabólico vs transposones en syn3A: coeficiente de Matthews 0,59 (R6-25) | Una priorización retrospectiva en el espiroplasma | **No corrió** |
| Cribado virtual de moléculas | — | — | No buscada | Poses, no actividad | **No corrió** |
| Diseño de péptidos | — | — | No buscada | Secuencias, no actividad | **No corrió** |
| Interacción patógeno–receptor del vector | AlphaFold 3 (SPIN, preprint) | — | Sin evaluación seria hallada | Una predicción | **No corrió** |

Dos advertencias de lectura. La evaluación independiente de la mayoría de estas tareas **no se buscó** en R6 y se escribe así, no como ausencia. Y las cifras de la fila de estructura no se interpretan como precisión de los modelos, sólo como cobertura.

## 5. Qué pueden hacer los agentes de IA y dónde fallan

Los agentes sirven para extraer y triar literatura, orquestar herramientas y dejar un rastro. Esa utilidad se vio acá: el cómputo de la sección 4 corrió con comandos y versiones registrados, y las fuentes quedaron con su nivel de lectura. Los fallos que ocurrieron en esta investigación son del tipo que el repositorio ya conoce.

El primer borrador de este reporte se hizo con fragmentos de buscador y declaraba una línea como veredicto. **La lectura dirigida de los textos completos cambió al menos cuatro afirmaciones**: la figura de ETH y Burs-α (sección 2.4), el contexto de mortalidad de la V-ATPasa (2.7), el estatus del puntero de R1 §4.4 (2.2) y la cultivabilidad de los fitoplasmas, que era una frase de un agregador y resultó contradictoria. Una descripción automática de una figura, devuelta por un buscador, mostraba valores que no coinciden con las barras reales medidas. Un `git clone` dentro del repo del usuario falló al escribir `.git` y se reintentó fuera de él, para no crear un repositorio anidado; el reintento falló por otra causa (GitHub no es alcanzable desde el entorno). Y dos fuentes críticas son de pago, de modo que se leyeron sólo en resumen.

Cada paso de una línea basada en estos datos tiene que ser auditable: entradas con accesión y fecha, versiones de herramientas, semillas (HMMER y BLAST son deterministas, no usan semilla) y registro de lo que falló. Eso es lo que `datos/COMANDOS.md` hace para lo corrido. Lo que ningún agente puede hacer es validar un blanco sin ensayo.

## 6. Antecedentes de pipelines computacionales y su validación

Para predicción de efectores en fitoplasmas hay al menos tres pipelines publicados. PhyEffector se evaluó sobre positivos construidos con 10 de los 21 efectores validados en la literatura más entradas de UniProt por palabra clave, y sobre negativos de 64 proteínas centrales de metabolismo de KEGG, con F1 de 0,56 a 1,0 según el pipeline y 0,9761 sobre genomas (R6-08, texto completo). Los negativos son fáciles: proteínas conservadas que no se secretan. LEAPH informa 95,3 % de precisión y recupera los 11 efectores clásicos validados y 4 de 6 no clásicos (R6-22, fragmento). Un análisis de 239 genomas con SignalP 3.0 y TMHMM 2.0 halló 7.162 efectores putativos y comparó modelos de AlphaFold 2 con dos estructuras cristalinas (R6-07, texto completo). **No se halló ninguna evaluación de terceros** de estos predictores, ni validación de un blanco predicho con un ensayo posterior. Para *Spiroplasma* y para plantas con otros patógenos limitados al floema no se halló un pipeline de descubrimiento de blancos con validación; la revisión del patosistema del maíz pide justamente ese trabajo (R6-12).

## 7. Validación sin laboratorio: verdades de terreno públicas

| Verdad de terreno | ¿Existe? | Qué hay | Límite |
| --- | --- | --- | --- |
| Esencialidad por transposones | Parcial | *M. genitalium*, *M. mycoides* JCVI-syn1.0/3.0/3A y *Mesoplasma florum* (R6-24 a R6-26) | Todos en cultivo axénico y ninguno fitopatógeno; esencial in vitro no es esencial en planta o insecto `[H]`; no se halló ninguna en *S. kunkelii* ni fitoplasma |
| Efectores validados | Sí, otra especie | ~21 en la literatura de fitoplasmas (R6-08) y SAP11_MBSP en maíz (R6-06) | Pocos y casi todos de otros fitoplasmas; ninguno de espiroplasma hallado |
| Adhesinas y determinantes de transmisión | Sí, otra especie | PGK, ScARP, P89 y espiralina en *S. citri* (R6-10, R6-11, R6-15) | n ≈ 3 a 6; ninguno en *S. kunkelii* |
| Genes de resistencia mapeados en maíz | **No hallada** | Sólo fenotipos de híbridos y un dialelo (R6-19, R6-20) | Es un resultado: no se puede evaluar retrospectivamente una priorización de genes de maíz |

La validación retrospectiva es posible para adhesinas y efectores con muy poca potencia estadística, y no lo es para los genes de resistencia del maíz.

## 8. Encaje con el track y presentación

La pregunta oficial habla de RNAi sobre genes del vector o de los patógenos asociados. **Entra** la Línea 2 (RNAi indirecto sobre genes del vector). **Complementa** la Línea 1 (interfaz vector–espiroplasma), que no usa RNAi, y la Línea 3 (efectores) queda entre complemento y fuera. Los antibióticos, los péptidos antimicrobianos y los inhibidores de efectores quedan fuera de la pregunta.

La presentación honesta es que el equipo verificó que no hay vía de RNAi en el mollicute, que la pregunta abierta nº 1 («inhibición del crecimiento del patógeno») sólo puede leerse como una vía indirecta o como una simplificación, y que lo indirecto es estrecho (sección 2.6). Antes de apostar a algo más hay que preguntarle al organizador si acepta propuestas no-RNAi; las preguntas están en `preguntas_investigador.md`.

## 9. Contracara de riesgo y alcance

Las estrategias del lado del vector comparten un riesgo: genes como clatrina, actina y ATP sintasa son esenciales, y un dsRNA mal elegido actúa como insecticida sobre cicadélidos nativos y parasitoides. L3 de `SINTESIS_V2.md` reporta 30 siRNA de ≥ 19 nt sobre el ortólogo de *Homalodisca vitripennis* para la región de BicC (cifra no re-verificada en R6). Del lado del patógeno, los antibióticos tienen riesgo de resistencia y de uso prohibido; los péptidos, de citotoxicidad; la PGK, al ser una enzima conservada, podría afectar a simbiontes `[H]`. Sobre SAP11, un inhibidor podría actuar sobre TCP no objetivo `[H]`.

**Alcance.** Ninguna línea propuesta aumenta la virulencia, la transmisibilidad ni el rango de hospedadores. El trabajo sobre efectores sólo es válido en modo defensivo; cualquier diseño de variantes que aumente la función de un efector queda descartado y se registra en `00_meta/CAMINOS_PROBADOS.md`. Todas las secuencias usadas son públicas (RefSeq, UniProt); no se usó ni se subió ninguna de `YHat-Biotech/`.

## 10. Vacíos documentados

No se halló: ningún QTL ni GWAS de achaparramiento en maíz (dos búsquedas); ningún cribado moderno de moléculas pequeñas contra *S. kunkelii*; ninguna evaluación de terceros de predictores de efectores; ningún ensayo de adhesión o transmisión de *S. kunkelii* con *D. maidis*; ningún reporte de cultivo de *Ca.* P. zeae; ningún trabajo de RNAi contra MRFV ni MSMV (según R1, no reabierto); ninguna fuente para SAP54 en MBSP. No se buscaron en R6: la evaluación independiente de cribado virtual, de diseño de péptidos ni del microbioma de la planta.

## 11. Lo que no se hizo

No corrió ningún predictor de péptido señal o transmembrana (los de uso común tienen licencia; DeepSig se instaló sin modelos porque GitHub no es alcanzable desde el entorno; no se pidió acceso por no ser fatal). No se predijo estructura localmente: AlphaFold DB cubre sólo el 1,0 % de *Ca.* P. zeae. No se re-corrió la transferencia de blancos hacia *D. maidis*. Las fuentes de acceso cerrado (dsRNasa, cribado de antimicrobianos) se leyeron sólo en resumen. Ninguna fuente se leyó linealmente: «texto completo» significa descargado y consultado por pasajes. R1 §5, W1, W3, W4, R4 y R5 no se reabrieron completos.

## Correcciones que se proponen al orquestador (D5)

Las integra el orquestador; R6 no editó los reportes de otras olas.

| # | Dónde | Propuesta |
| --- | --- | --- |
| 1 | `CORRECCIONES.md` B5 | Matizar: *eth* en *D. maidis* es 10 % (texto, día 5) o ≈17,5 % (figura 5A, día 4); el resto de B5 se confirma |
| 2 | R1 §4.4 | Reemplazar el puntero sin fuente por las fuentes de la sección 2.2, indicando que son de *S. citri* |
| 3 | R1 §4.4 y brief | Acotar S44: es una revisión de manejo de vectores; no evalúa antibióticos |
| 4 | R1 §3.2 | Cambiar «*Ca.* P. asteris» por «*Ca.* P. zeae» (el artículo de 2026 de R6-09 ya usa este nombre) |
| 5 | W3 §4.2 y R1 §3.2 | Anotar que 1.463.926 y 1.514.561 pb son el cromosoma y el genoma con 3 plásmidos, y que pSKU146 (`NC_006400.1`) es una accesión aparte |
| 6 | `DECISIONS.md` D9 | Anotar que la verificación por perfiles HMM se hizo para los dos genomas (sección 2.1) |
| 7 | R1 §4.6 | Agregar el contexto de V-ATPasa (control ya mortal) y de BicC (inyección vs ingestión) |
| 8 | R1 sources S27 | Reconciliar el año (2025 o 2026) |
