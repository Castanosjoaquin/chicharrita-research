# R7 · M4 — Estructura de proteínas y ARN de los dos mollicutes del achaparramiento y papel de la microgravedad

*Candidatus* Phytoplasma zeae (taxid 202462, cepa M3, GCF_001712875.1) y *Spiroplasma kunkelii* (taxid 47834, cepa CR2-3x, GCF_001274875.1; plásmido pSKU146, NC_006400.1). Corte: 2026-10-19; ventana principal octubre de 2024 a octubre de 2026, con lo anterior marcado como fundacional cuando es la única evidencia. Marcadores de `CLAUDE.md`: `[E]` establecido, `[R]` reportado, `[H]` hipótesis del equipo, `[?]` incierto. Las referencias `M4-xx` están en `sources.json` con su nivel de lectura; cada consulta a una API está en `datos/COMANDOS.md` y su respuesta cruda en `datos/`. **De las 45 fuentes bibliográficas, 26 se leyeron solo en resumen, 11 en texto parcial, 4 en texto completo (por pasajes) y 4 solo como título; ninguna se leyó linealmente**; las cifras que dependen de un resumen lo dicen.

## Veredicto

**La estructura aporta poco para atacar a los dos mollicutes sin RNAi, y la microgravedad no aporta nada demostrable. El faltante estructural no es un problema de cristalización: es de ensayo, de cultivo y de que nadie estudió estos blancos.**

De los **16 blancos con evidencia funcional** que se pudieron armar con fuentes abiertas (9 de *Ca.* P. zeae y 7 de *S. kunkelii*; 14 proteínas y 2 ARN ribosomales), **ninguno tiene estructura experimental propia**: RCSB devuelve cero entradas para los taxid 47834 y 202462 y para cada una de las accesiones UniProt de la tabla (consulta del 2026-10-19). Solo uno (la enzima málica de *Ca.* P. zeae, Z06) tiene un homólogo ≥ 90 % resuelto (95,9 % con el 5CEE de AYWB, 2,5 Å). Con predicción hay **6 de 14 proteínas, todas de *S. kunkelii*** (pLDDT medio de 71,8 a 96,1) y **0 de 8 de *Ca.* P. zeae**; y ese cero es de fecha, no de dificultad: 480 de las 485 entradas UniProt de *Ca.* P. zeae se crearon el 2025-10-08, después del corte de modelos de AlphaFold DB (§2.2).

**Causa del faltante, contada por blanco (§3):** en 9 nadie lo intentó (no se halló ningún intento publicado `[?]`: puede haber sesgo de publicación), en 4 la proteína es de membrana, en 1 falta el ensayo funcional, en 1 no hay cultivo del fitoplasma (ARNr) y en 1 no hay faltante. **«No cristaliza pese a intentarlo», la única causa que justificaría la microgravedad, no aparece en ninguno (0 de 16), ni «no se logró expresar» (0 de 16).** En las 20 estructuras de rayos X de proteínas de *Spiroplasma* y fitoplasmas del PDB (1,4–2,5 Å, mediana 2,09 Å) los cristales salieron por difusión de vapor terrestre (16 en gota sedente, 4 en gota colgante) y los obstáculos documentados fueron otros: las fases del Imp (resueltas con un modelo de AlphaFold 2) y la estabilidad de MreB5 (resuelta con KCl).

**Regla de decisión (§3.3):** la microgravedad sería una respuesta razonable solo si un blanco cumple a la vez cinco condiciones (proteína purificable, intento terrestre con cristales deficientes por crecimiento, una decisión que dependa de más resolución, un ensayo que valide, y acceso a vuelo y laboratorio). **Cumplen las cinco 0 de 16.** La C2 falla en todos y la C5 falla por D1. Nada une microgravedad (real o simulada) con estos organismos: 0 de 193 entradas de mollicutes del PDB tiene cristales de microgravedad, 0 resultados en NASA OSDR para *Spiroplasma* o fitoplasma, y el único cruce de la bibliografía usa un biorreactor de pared rotatoria (simulada) para armar tejido humano, no para cultivar el micoplasma (§6).

**Qué conviene hacer en cambio.** (1) No abrir una línea de microgravedad ni de cristalización. (2) Usar la tabla de §1–§2 como un eje de anotación estructural de L1 (D7): es una priorización auditable con fuente, fecha de consulta y distancia al homólogo; encaja con R6 (Línea 1 y Línea 3) sin repetirlo. (3) Si el equipo quiere predicción de interfaz, hacerlo solo donde hay verdad de terreno retrospectiva sin laboratorio: los 8 complejos SAP05–SPL/GATA/RPN10 del PDB (con un candidato SAP05-like en M3, 43,2 % en 81 aa `[H]`) y la región PGK-FL5 (n = 1). Para los otros 12 blancos no hay decisión demostrable sin laboratorio (§4). (4) Registrar como pendiente el modelado de las 480 proteínas de M3 sin modelo, que exige GPU y no se hizo (§7). (5) Las dos preguntas que cambiarían decisiones son del organizador, no de la bibliografía (`preguntas_pendientes.md`).

**Límites que condicionan el veredicto.** La mayor parte de la evidencia funcional es de otra especie (*S. citri*, AYWB, *Ca.* P. mali) y de resumen. La BLAST local contra proteínas con PDB puede subestimar la identidad (faltan entradas TrEMBL) y no detecta homología remota. «Nadie lo intentó» es ausencia de evidencia, no evidencia de ausencia.

---

## 1. Lista de blancos (método 1)

Un blanco entra solo si tiene una fuente abierta que sostiene su papel en infección, transmisión o supervivencia; la distancia entre el organismo de la evidencia y el blanco va siempre explícita. `blancos_estructura.json` tiene una entrada por fila con el detalle completo. Z01 a Z09 son de *Ca.* P. zeae y K01 a K07 de *S. kunkelii*; S01 y S02 son parientes con estructura y sin papel en infección demostrado, y no entran en ningún conteo de blancos.

| ID | Organismo | Blanco (UniProt) | Papel funcional (resumido) | Fuente | Distancia de la evidencia | Marcador |
| --- | --- | --- | --- | --- | --- | --- |
| Z01 | *Ca. P. zeae* | SAP11-like (A0ABM6DLD7) | desestabiliza TCP TB1/CYC; impide la inflorescencia femenina en maíz transgénico; no sube la fecundidad del vector | M4-01 | propio (SAP11_MBSP); mapeo a la entrada [H] | [E] función de SAP11-MBSP |
| Z02 | *Ca. P. zeae* | candidato SAP05-like (A0ABM6DM10) | SAP05 de otros fitoplasmas degrada SPL/GATA vía RPN10 sin ubiquitina; para el candidato de M3 no hay función | M4-06, M4-D4 | pariente: 43,2 % en 81 aa | [H] (homología parcial, sin función demostrada en M3) |
| Z03 | *Ca. P. zeae* | «Phytoplasmal effector causing phyllody 1» (A0ABN4RYC3) | PHYL1/SAP54 de otros fitoplasmas induce filodia vía MADS y RAD23; para M3 solo un nombre de UniProt | M4-08 | pariente sin similitud detectable | [?] |
| Z04 | *Ca. P. zeae* | Imp (A0ABM6DLQ2) | se une a F-actina; en PnWB interactúa con PHYL1; secuencia muy diversa entre especies | M4-04, M4-05 | pariente (Ca. P. mali, PnWB); sin similitud BLASTP | [R] |
| Z05 | *Ca. P. zeae* | Imp, segundo parálogo (A0ABN4S0Q5) | ídem Z04 (segundo parálogo; sin dato propio) | M4-04, M4-05 | ídem | [R] |
| Z06 | *Ca. P. zeae* | Enzima málica (A0ABM6DLE7) | malato → piruvato; fuente de energía propuesta; presente en todos los genomas de fitoplasma | M4-27, M4-28 | pariente AYWB: 95,9 % | [R] función (resumen) |
| Z07 | *Ca. P. zeae* | Simportador malato:citrato (A0ABM6DLD1) | transporte de malato (hipótesis a partir del genoma) | M4-27 | pariente AYWB (hipótesis) | [?] |
| Z08 | *Ca. P. zeae* | Timidina quinasa (A0ABN4RZ55) | proliferación y virulencia en un sistema heterólogo; actividad solo predicha in silico | M4-09 | pariente PaWB (identidad no medida) | [R] |
| Z09 | *Ca. P. zeae* | ARNr 16S (—) | tetraciclinas suprimen fitoplasmas (otras especies); diana ribosomal según R6 | M4-11, M4-L1 | otras especies | [E] tetraciclinas en fitoplasmas (otras especies) |
| K01 | *S. kunkelii* | Fosfoglicerato quinasa (A0A0K2JFN2) | se une a actina del vector; PGK o PGK-FL5 reducen entrada a células y transmisión en cicadélidos | M4-02, M4-18 | S. citri: 93,7 % | [R] (S. citri |
| K02 | *S. kunkelii* | Espiralina (A0A0K2JG54) | mutantes se transmiten peor; lectina in vitro; scFv anti-espiralina inhiben crecimiento in vitro | M4-19, M4-20, M4-21, M4-38 | S. citri: 61,1 % | [R] |
| K03 | *S. kunkelii* | Arp1 / SkARP1 (Q5VCC1) | homólogo de SARP1; ScARP3d dispara la entrada a células del vector; G/6: −82 % adhesión, −84 % internalización | M4-03, M4-22, M4-10 | S. citri P89: 76,5 % en 532 aa | [R] |
| K04 | *S. kunkelii* | Componente IIABC específico de fructosa del PTS (A0A0K2JFE3) | mutantes del operón de fructosa: síntomas leves y tardíos en pervinca | M4-23 | S. citri: 92,6 % | [R] |
| K05 | *S. kunkelii* | 1-fosfofructoquinasa (A0A0K2JGE0) | ídem K04 (misma operón; sin dato específico) | M4-23 | S. citri: 91,0 % | [R] |
| K06 | *S. kunkelii* | Componente IIBC de glucosa del PTS (A0A0K2JFE4) | mutante ptsG igual de patógeno que el salvaje: control negativo | M4-24 | S. citri (identidad no medida) | [R] |
| K07 | *S. kunkelii* | ARNr 16S (—) | crecimiento inhibido por AMPs «como tetraciclina»; diana ribosomal según R6 | M4-25, M4-L1 | cultivo de S. kunkelii | [R] |
| S01 | *S. kunkelii* | MreB (A0A0K2JEY9) | MreB5 necesaria para la forma helicoidal; papel en infección no demostrado | M4-26, M4-07 | S. citri MreB5: 98,3 % | [R] |
| S02 | *S. kunkelii* | FtsZ (A0A0K2JH33) | división celular; papel en infección no demostrado | M4-D4 | S. melliferum: 97,1 % | [E] estructura |

Tres precisiones sobre esta lista. Primera, **SAP11_MBSP está validado por transgénesis en maíz `[E]` (M4-01), pero el artículo no da accesión**: asociarlo con la entrada A0ABM6DLD7 (116/116 aa con una SAP11-like de UniProt, según R6) sigue siendo `[H]`. Segunda, **UniProt nombra «Effector» a 37 de las 485 entradas de *Ca.* P. zeae** (varias con nombres tipo «AYWB SAP11-like»; entradas creadas el 2025-10-08), pero un nombre no es una función: la entrada que UniProt llama «Phytoplasmal effector causing phyllody 1» (A0ABN4RYC3, 74 aa) no tiene similitud detectable con ningún PHYL1 con estructura (mejor E = 0,16), y queda `[?]`. Tercera, **el ortólogo de FruR de *S. kunkelii* no está claro**: la proteína de 86 aa anotada como regulador del operón de fructosa alinea con 80 % de identidad solo sobre el 36 % de la FruR de *S. citri* (233 aa), así que se excluyó. La lista no es un inventario del proteoma: es lo que tiene fuente abierta; los modelos de las 1.750 entradas de *S. kunkelii* y de las 5 de *Ca.* P. zeae que tienen modelo están resumidos en `datos/afdb_resumen_por_proteina_*.csv`.

Sobre el ARN: de los dos ARNr 16S se pudo medir la distancia al ribosoma con estructura más cercano (§2). **El ARN regulatorio no se evaluó** (no se halló literatura funcional en estos dos organismos y Rfam no está entre los dominios autorizados), y lo declaro como no evaluado a esta profundidad y no como ausencia.

## 2. Cobertura estructural medida (método 2)

### 2.1 PDB

La consulta a RCSB por linaje taxonómico devolvió **204 (sin resultados) para los taxid 47834 y 202462**, y la consulta por accesión UniProt dio cero entradas para las 14 accesiones de proteína de la tabla (Z01–Z08, K01–K06) y para las demás consultadas (los cinco MreB, FtsZ, LspA, HPr, el fragmento A0A0K2JJY7 y FruR de *S. kunkelii*): 24 accesiones en total. `[E]` (consulta de base de datos). El censo de parientes, que sí tiene entradas, es el siguiente, y se verificó con tres métodos independientes (linaje por identificador, linaje por nombre y nombre científico) que dieron el mismo número:

*Spiroplasma* (taxid 2132): **9 entradas**, de 4 proteínas de otras especies: HU de *S. melliferum* (5L8Z, 1,4 Å; 5OGU, RMN), MreB5 de *S. citri* (7BVY, 7BVZ), MreB3 de *S. eriocheiris* (7E1C, 7E1G) y FtsZ de *S. melliferum* (7YOP, 7YSZ, 8GRW). *Candidatus* Phytoplasma (taxid 33926): **12 entradas** de 4 proteínas: enzima málica de AYWB (5CEE), PHYL1/SAP54-like (6JQA, 6INR), SAP05 en complejo con proteínas de *Arabidopsis* (8 entradas: 8J48, 8J49, 8J4A, 8J4B, 8JTL de OY; 8JTK, 8PFC, 8PFD de AYWB) e Imp del fitoplasma del maní (8J8Y). **No hay ninguna estructura de SAP11, de TENGU ni de ARN de fitoplasma**: las búsquedas de texto libre «SAP11» y «TENGU» devolvieron cero entradas. De las 21 entradas, 20 son de rayos X (resolución 1,4–2,5 Å, mediana 2,09 Å) y la más reciente se liberó el 2024-05-08, antes de la ventana principal.

Dos advertencias de método con consecuencias. La búsqueda por la clase Mollicutes (taxid 31969) **omite** *Mycoplasmoides pneumoniae* (101 entradas con su taxón) y *M. genitalium* (42), porque en la taxonomía actual de NCBI *Mycoplasmoides* cuelga de Mycoplasmoidales; el censo «Mollicutes» de RCSB (47 entradas) subestima, y el conteo de 193 entradas de mollicutes que uso en §6 es la unión de siete búsquedas. Y UniProt tiene un rezago frente a RCSB: tres accesiones de estructuras recientes (A0A037USE5, A0ABF7PLP1, A0ABF7PLM3) no tenían todavía su referencia cruzada al PDB y hubo que agregarlas a mano a la base de homólogos.

### 2.2 AlphaFold DB

Se consultó la API para las 1.755 accesiones UniProt de *S. kunkelii* y las 485 de *Ca.* P. zeae (`datos/afdb_bulk_*.jsonl`). *S. kunkelii*: **1.750 de 1.755 (99,7 %)** tienen modelo, con pLDDT medio por proteína de 73,0 (mediana 76,75): 327 proteínas (18,7 %) con pLDDT medio ≥ 90, 771 (44,1 %) entre 70 y 90, 412 (23,5 %) entre 50 y 70 y 240 (13,7 %) por debajo de 50; el 62,7 % de las proteínas está en el rango confiable. Las cinco sin modelo tienen entre 1.290 y 1.454 aa (ADN polimerasa PolC, subunidad beta de la ARN polimerasa, una helicasa y dos permeasas ABC), una longitud compatible con un tope de largo de AlphaFold DB `[?]` (no se verificó en su documentación). *Ca.* P. zeae: **5 de 485 (1,0 %)**, que son la chaperonina GroEL (pLDDT 91,6), la proteína ribosomal uL22 (88,3), una transposasa (80,7), una N6-treonilcarbamoiladenosina sintasa (92,9) y una proteína no caracterizada (74,2).

**La brecha de *Ca.* P. zeae es de fecha y no de dificultad.** Las 480 entradas sin modelo tienen todas la misma fecha de creación en UniProt, 2025-10-08, mientras que las 5 con modelo se crearon entre 2004 y 2016 y sus modelos son del 2022-06-01 (`datos/uniprot_fechas_*.txt`). `[E]` para el hecho; `[H]` que un modelado local o una actualización futura de AlphaFold DB lo cierre, lo que cambia la lectura de R6 («solo 1,0 %»): no es que estas proteínas sean difíciles de predecir, es que nadie las corrió aún.

### 2.3 Cobertura por blanco

La identidad es el `pident` del mejor acierto de `blastp` local contra 12.450 secuencias UniProt con estructura experimental (parámetros en `datos/COMANDOS.md` §1), siempre con la cobertura de la consulta; no es una identidad global.

| ID | Blanco | PDB propio | AlphaFold DB: pLDDT medio (% de residuos < 70) | Mejor homólogo con estructura (identidad / cobertura de la consulta) | Estructura(s) del homólogo (método, resolución) |
| --- | --- | --- | --- | --- | --- |
| Z01 | SAP11-like | no | sin modelo | ninguno funcional (acierto N-terminal débil con SAP05: 31,6 % / 77 %, E 4e-4) | — |
| Z02 | candidato SAP05-like | no | sin modelo | SAP05 de OY: 43,2 % en 81 aa (20 % de la proteína de M3; región 214–292) | 8 complejos SAP05: 8J48, 8J49, 8J4A, 8J4B, 8JTL (OY); 8JTK, 8PFC, 8PFD (AYWB); rayos X 1,6–2,2 Å |
| Z03 | «Phytoplasmal effector causing phyllody 1» | no | sin modelo | ninguno detectable (mejor E = 0,16) | —  (PHYL1 de otros fitoplasmas: 6JQA 2,4 Å, 6INR 2,3 Å; sin similitud detectable) |
| Z04 | Imp | no | sin modelo | ninguno detectable (E ≤ 10) | —  (Imp de PnWB: 8J8Y 2,0 Å; no transferible por BLASTP) |
| Z05 | Imp, segundo parálogo | no | sin modelo | ninguno detectable (E ≤ 10) | —  (ídem Z04) |
| Z06 | Enzima málica | no | sin modelo | Aster yellows witches'-broom phytoplasma: 95,9 % / 100 % | 5CEE (rayos X, 2,5 Å) |
| Z07 | Simportador malato:citrato | no | sin modelo | K. pneumoniae CitS: 27,4 % / 84 % | 5X9R, 5XAR, 5XAS, 5XAT (rayos X 3,5–4,0 Å); 9LSH–9LSK (crio-EM 2,9–3,8 Å) |
| Z08 | Timidina quinasa | no | sin modelo | Staphylococcus aureus: 49,5 % / 91 % | 8Y7W (rayos X, 2,3 Å) |
| Z09 | ARNr 16S | no | n/a (ARN) | 16S de M. pneumoniae: 84,9 % | 8P6P (crio-EM 3,2 Å), 8P8B (2,9 Å), 7OOC (3,7 Å), 7P6Z (3,5 Å) |
| K01 | Fosfoglicerato quinasa | no | 96,1 (0 %) | Streptococcus pneumoniae serotype 2: 57,4 % / 99 % | 3ZLB (rayos X, 1,8 Å) |
| K02 | Espiralina | no | 88,7 (11 %) | ninguno detectable (E ≤ 10) | — |
| K03 | Arp1 / SkARP1 | no | 71,8 (39 %) | ninguno detectable (E ≤ 10) | — |
| K04 | Componente IIABC específico de fructosa del PTS | no | 84,2 (11 %) | Bacillus subtilis: 34,3 % / 98 % | 2R4Q (rayos X, 1,6 Å) |
| K05 | 1-fosfofructoquinasa | no | 95,6 (0 %) | Enterococcus faecalis: 28,6 % / 98 % | 2AWD (rayos X, 2,0 Å), 2F02 (rayos X, 1,9 Å) |
| K06 | Componente IIBC de glucosa del PTS | no | 77,6 (25 %) | Bacillus subtilis: 38,7 % / 42 % | 1GPR (rayos X, 1,9 Å) |
| K07 | ARNr 16S | no | n/a (ARN) | 16S de M. pneumoniae: 84,3 % | ídem Z09 |
| S01 | MreB | no | 90,1 (8 %) | Spiroplasma citri: 98,3 % / 100 % | 7BVY (rayos X, 2,5 Å), 7BVZ (rayos X, 2,3 Å) |
| S02 | FtsZ | no | 76,7 (32 %) | Spiroplasma melliferum: 97,1 % / 100 % | 7YOP (rayos X, 2,2 Å), 7YSZ (rayos X, 2,3 Å), 8GRW (rayos X, 2,4 Å) |

Lectura: los 6 blancos de proteína de *S. kunkelii* tienen modelo de pLDDT ≥ 70 (promedio de los seis: 85,7); el más dudoso es SkARP1 (K03, pLDDT 71,8 con 38,6 % de los residuos bajo 70, por sus repeticiones). Cinco blancos (Z03, Z04, Z05, K02, K03) no tienen ningún homólogo con estructura detectable por BLASTP (con E ≤ 10 solo aparecen aciertos espurios), de modo que la transferencia por homología no está disponible para los de mayor interés biológico (Imp, espiralina, SkARP1); **la homología remota por perfiles o por plegamiento (HHblits, Foldseek) no se evaluó**. Un resultado a mirar: el Imp de PnWB (8J8Y) no es detectable en M3 por BLASTP, coherente con que Imp sea muy diverso entre especies (M4-05).

## 3. Diagnóstico del faltante (método 3)

### 3.1 Conteo por causa

| Causa del faltante (vocabulario del método) | Blancos con esa causa principal (n = 16) | Blancos con esa causa entre las principales o secundarias |
| --- | :---: | :---: |
| No se logró expresar | 0 | 0 |
| **No cristaliza pese a intentarlo** (la única que justificaría microgravedad) | **0** | **0** |
| De membrana | 4 (Z07, K02, K04, K06) | 7 |
| Nadie lo intentó (no se halló intento publicado) | 9 (Z01–Z05, K01, K03, K05, K07) | 11 |
| Ausencia de ensayo funcional | 1 (Z08) | 9 |
| Imposibilidad de cultivo axénico | 1 (Z09, ARNr de *Ca.* P. zeae) | 7 |
| Otra (fecha de corte de AlphaFold DB, ribosoma ya resuelto por crio-EM) | 0 | 3 |
| Sin faltante (homólogo ≥ 90 % ya resuelto) | 1 (Z06, enzima málica) | 1 |

Los conteos de la columna central son por blanco (16 filas); la columna de la derecha cuenta cada causa cuando aparece como principal o secundaria. El criterio de asignación está en `blancos_estructura.json` (`causa_del_faltante`, `causas_secundarias`).

### 3.2 Qué dice la evidencia sobre dónde está el cuello de botella

**No se logró expresar: no aparece, y hay un obstáculo conocido y salvable.** *Spiroplasma* usa la tabla de código genético 4 (UGA codifica triptófano) y *Ca.* P. zeae la tabla 11 (UGA es parada) `[E]` (NCBI Taxonomy, `datos/taxonomia_efetch_codigo_genetico.xml`). En la PGK de *S. citri*, los autores sustituyeron los dos codones UGA por UGG para expresarla en *E. coli* (M4-02), lo que vale también para *S. kunkelii*. Los fitoplasmas no se cultivan (según R6 hay una afirmación de cultivo axénico de 2012 que revisiones de 2021 y 2025 no sostienen `[?]`), pero **eso no impide la estructura**: el Imp de PnWB se produjo recombinante en *E. coli* BL21 y cristalizó (M4-04), y hay estructuras de SAP05, PHYL1 y enzima málica de fitoplasmas.

**No cristaliza pese a intentarlo: no se halló ni un caso.** En el Imp del PnWB los cristales (60 mg/ml, PEG 8000 al 30 %, gota sedente, 20 °C según el artículo) difractaron a 2,0 Å, y lo que faltaba eran las fases: la proteína carece de metioninas y no tiene cisteína ni histidina capaz de unir metales pesados, y los intentos de introducir Met y Cys por mutagénesis para derivados no funcionaron, así que se resolvió por reemplazo molecular con un modelo de AlphaFold 2 (M4-04). Es la única frase de la bibliografía leída que habla de intentos fallidos (los autores dicen que no lograron expresar y cristalizar homólogos de otras especies, sin cifras y dentro de la búsqueda de una solución de fases); no cuenta como evidencia de «no cristaliza» ni tiene relación con la gravedad. En MreB5 de *S. citri* el problema fue la agregación al sobreexpresarse, resuelto con tampón con KCl (M4-07); y las 20 estructuras de rayos X de los dos géneros son difusión de vapor estándar.

**De membrana (4 blancos) y sin ensayo (1).** Spiralina, FruA, PtsG y el simportador de malato son proteínas de membrana o lipoproteínas; el primer paso sería producirlas solubles, no cristalizarlas mejor. Entre los parientes, los transportadores homólogos al CitS se resolvieron por rayos X a 3,5–4,0 Å y por crio-EM a 2,9–3,8 Å (RCSB), y los ribosomas de *M. pneumoniae* se resolvieron por crio-EM en células (2,9–3,5 Å en las entradas de subunidades y 70S), sin cristales. En ambos casos la ruta que avanzó es otra, aunque no hay una comparación controlada.

**Nadie lo intentó (9 blancos): es ausencia de evidencia.** Una búsqueda por título y resumen en Europe PMC (2026-10-19) con términos de estructura devolvió 6 resultados para *Spiroplasma* y 6 para fitoplasmas, ninguno sobre PGK, espiralina, SkARP1, operón de fructosa, SAP11, Imp de *Ca.* P. zeae ni timidina quinasa. El único trabajo estructural sobre la espiralina es un péptido sintético de 20 aa por RMN (1995), cuyo resumen dice que su estructura cristalográfica no se conocía (M4-38). Los resultados negativos no publicados no aparecen en ninguna base, de modo que `[?]`.

**Imposibilidad de cultivo axénico.** Afecta al origen nativo del ARNr de *Ca.* P. zeae, pero el ribosoma de *M. pneumoniae* (84,9 % de identidad de 16S) ya está resuelto; para proteínas, el cultivo no es necesario si se expresa recombinante.

### 3.3 Regla de decisión

La microgravedad solo es una respuesta razonable a un faltante estructural cuando el problema es el crecimiento del cristal, no la expresión, las fases, la estabilidad o el ensayo. Se traduce en cinco condiciones simultáneas; la tabla dice cuántos blancos cumplen cada una.

| Condición | Qué exige | Blancos que la cumplen |
| --- | --- | --- |
| C1 | La proteína (o un homólogo ≥ 90 %) se expresó y purificó soluble y monodispersa | Z06, K01 (en *S. citri*), S01, S02 |
| C2 | Hay un intento terrestre publicado con cristales deficientes por el crecimiento (pequeños, maclados, mosaicidad alta) o sin cristales tras un cribado amplio, y la resolución es lo que limita | **0** |
| C3 | Una decisión concreta depende de una resolución mejor (diseño de inhibidor, validación de modelo, mapa de interfaz) | 0 |
| C4 | Existe un ensayo funcional que pueda validar lo que la estructura sugiera | Z01 (planta transgénica), K01–K04 y K06 (solo en *S. citri*), parcial en otros |
| C5 | El equipo puede acceder a un vuelo y a un laboratorio (D1 lo excluye) | **0** |
| **Cumplen C1 a C5** | | **0 de 16 (0 de 18 con los dos parientes)** |

Ningún blanco necesita la microgravedad porque ningún blanco llegó al punto donde el crecimiento del cristal es lo que limita. Que la microgravedad mejore cristales en general no se evalúa acá (es de M1); lo que se mide acá es que, para estos organismos, el paso previo no está dado.

## 4. Qué agregaría una estructura (método 4)

Se asume la restricción D1 (demostrable sin un solo experimento húmedo) y D7/D8 (priorización auditable, no diseño ni entrenamiento).

| ID | Decisión que cambiaría una estructura mejor | ¿Demostrable sin laboratorio? |
| --- | --- | --- |
| Z01 | Mapa de interfaz SAP11–TCP; no hay complejo experimental de ningún SAP11 contra el cual validar | no |
| Z02 | Evaluar una predicción de interfaz contra 8 complejos SAP05 del PDB; utilidad práctica baja | parcial |
| Z03 | Ninguna: sin similitud con PHYL1 con estructura | no |
| Z04, Z05 | Modelo de Imp (en PnWB un modelo de AlphaFold 2 resolvió las fases); sin complejo con actina para validar | parcial |
| Z06 | Ninguna: modelo por homología sobre 5CEE al 95,9 % | no |
| Z07, Z08 | Ninguna: sin ensayo de transporte ni enzimático con la proteína del fitoplasma | no |
| Z09, K07 | Conservación in silico del sitio de unión de antibióticos sobre ribosomas de *M. pneumoniae* (84–85 %); sin ensayo en maíz | no |
| K01 | Ubicar FL5 en el modelo (pLDDT 96,1) y evaluar una predicción PGK–actina contra FL5 (n = 1) | parcial |
| K02, K03 | Mapa de epítopos para anticuerpos o scFv; sin receptor del vector ni ensayo con *S. kunkelii* | no |
| K04, K05 | Ninguna: ensayo de patogenicidad en planta con mutantes de *S. citri*; sin ensayo enzimático ni de transporte en *S. kunkelii* | no |
| K06 | Bajar la prioridad del blanco (la propia fuente lo descarta) | no |

**12 de 16 blancos no tienen ninguna decisión demostrable sin laboratorio, y 4 la tienen parcial** (Z02, Z04, Z05, K01). Z02 ofrece la única validación retrospectiva con más de un caso (8 entradas del PDB), pero con baja utilidad práctica: en *Arabidopsis*, un cambio de dos aminoácidos de RPN10 vuelve a la planta resistente a la actividad de SAP05 y, aun así, las plantas con RPN10 resistente no producen más tejido vegetativo y mueren antes durante la infección (M4-06): bloquear al efector no es lo mismo que proteger a la planta `[R]`. En SAP11 la predicción de interfaz tiene un antecedente débil: AlphaFold-Multimer modeló SAP11-AYWB con AtTCP10 con un ipTM de 0,705, que los autores llaman consistente con la evidencia experimental, pero no hay ninguna estructura experimental del complejo (M4-08). Para PGK, la verdad de terreno es una sola región (FL5) en una especie distinta.

## 5. Estrategias de proteína o ARN sin RNAi (método 5)

Se excluye lo que cubrió R6 (moléculas pequeñas y tetraciclinas, adhesinas, bloqueo de entrada, RNAi indirecto) salvo para marcar lo que M4 agrega o corrige. Toda la evidencia de abajo es de resumen o de texto parcial, salvo lo indicado.

**Aptámeros de ARN o ADN.** No se halló ninguno contra *Spiroplasma*, fitoplasmas ni micoplasmas fitopatógenos. La evidencia es de micoplasmas de cultivos celulares y de mamíferos: un cóctel de aptámeros marcados con colorante para detectar micoplasmas en cultivos celulares (diagnóstico, M4-16) y un aptámero ssDNA (ZY3A) obtenido por cell-SELEX contra *Mycoplasma hyorhinis* que se une a la proteína p37, neutraliza la infección en células de carcinoma esofágico y reduce metástasis en un modelo in vivo (M4-33; los autores lo presentan como primera prueba de concepto de un aptámero para controlar una infección por micoplasma). No agrega nada a R6, que no cubrió aptámeros; es un precedente en sistema de cultivo y animal, no en planta ni en insecto, y su diana (p37) es de un micoplasma sin equivalente conocido en los dos blancos.

**Oligonucleótidos antisentido y PNA.** No se halló ningún uso terapéutico contra mollicutes. Lo hallado: sondas PNA de detección de mollicutes (familia de patentes y una técnica de PCR con PNA para mutaciones del 23S de *M. pneumoniae*; solo títulos, `fragmento_buscador`, M4-39 y M4-41) y un trabajo de 1996 sobre la sorción de antisentido por células de *Mycoplasma* (solo título, M4-40). Lo más cercano es un sistema de CRISPR de interferencia (dCas9) en *M. gallisepticum* y *M. hominis*, con caída de unas diez veces del ARNm de genes diana, en cultivo (M4-12): es silenciamiento guiado por ARN pero no RNAi, sirve para esencialidad génica en un mollicute cultivable y no se probó en *Spiroplasma* ni en fitoplasma; *S. kunkelii* se cultiva (R6), de modo que sería un experimento de laboratorio fuera de D1. Agrega a R6 (que anotó «esencialidad génica» sin verdad de terreno propia) una herramienta de cultivo, no un dato.

**Nanocuerpos y scFv.** Es la familia con más evidencia, y la más desfavorable en el sistema que importa. In vitro, scFv y anticuerpos policlonales anti-espiralina inhibieron el crecimiento de *S. citri* en medio líquido y su motilidad, sin efecto sobre el metabolismo de glucosa (M4-21). Pero un scFv construido a partir de anticuerpos contra el espiroplasma del achaparramiento, expresado en una línea celular de maíz, **no dio plantas regeneradas con resistencia clara en invernáculo** (M4-32, solo resumen, 1998; los propios autores atribuyen el resultado a la afinidad y funcionalidad in vivo y a la localización). En tabaco, un scFv contra el fitoplasma stolbur dejó crecer sin síntomas los brotes de una línea transgénica injertados sobre un portainjerto infectado (M4-29), pero en un trabajo posterior (2005, con ensayos de invernáculo y de campo) el scFv secretado dio un retraso de hasta 2 semanas con injerto y **ninguna resistencia significativa cuando transmitía el insecto**, y la versión citoplasmática no produjo proteína detectable ni resistencia (M4-30). Un scFv contra Imp de *Ca.* P. aurantifolia se unió a Imp y a células de fitoplasma y se expresó en *N. benthamiana*, sin ensayo de resistencia en el resumen (M4-31). No se halló ningún nanocuerpo (VHH) contra mollicutes. Una salvedad para anticuerpos en micoplasmas de animales: el sistema MIB-MIP, que degrada inmunoglobulinas, está en la mayoría de las especies de micoplasma y pasó por transferencia horizontal a especies de los grupos Spiroplasma y Pneumoniae, pero la ATPasa F1-like X0 asociada no tiene homólogo en *Spiroplasma* ni *Acholeplasma* (M4-15, texto parcial); no hay dato de que importe en un floema o una hemolinfa sin inmunoglobulinas. **Corrige a R6**, que dejaba como faltante «una planta que exprese el scFv» (E08): el experimento se hizo, con el espiroplasma del achaparramiento y con un fitoplasma, y no mostró protección sólida `[R]` (solo resúmenes).

**Péptidos antimicrobianos.** *S. kunkelii* y *S. citri*: Novispirin T7 y Caerin 1.1 inhibieron el crecimiento in vitro con una eficacia que el resumen describe como comparable a la de la tetraciclina, con deformación celular y CMI determinadas (M4-25; resumen, valores de CMI no leídos). Ese es el original del que R6 tenía un fragmento secundario. En *M. pneumoniae*, tres péptidos sintéticos (derivados de magainina 2 o diseñados racionalmente) inhibieron en cultivo a 8–30 µM, con indicios de interacción directa con la membrana (M4-13) y hay un estudio de cecropina en ratones del que solo se vio el título (M4-42). Una revisión sobre micoplasmas plantea que la resistencia a antimicrobianos puede deberse a cambios amplios del genoma, el proteoma y el secretoma, no solo a mutaciones puntuales (M4-17, resumen). La evidencia crítica es de resistencia: *Acholeplasma laidlawii* se adapta rápido a antimicrobianos, incluidos los péptidos, y se obtuvo una cepa resistente a melitina (M4-14). No se halló ninguna prueba en planta o en insecto. Agrega a R6 la confirmación desde el resumen original y el riesgo de resistencia; no cambia la conclusión de que es una vía sin verdad de terreno en maíz.

**Inhibidores de efectores.** No se halló ningún inhibidor, de molécula pequeña ni peptídico, de ningún efector de fitoplasma, y R6 tampoco lo había hallado para SAP11. Lo que existe es del lado de la planta y de la estructura: SAP05 tiene 8 complejos resueltos y una variante vegetal de RPN10 con dos sustituciones resistente a SAP05, con el costo antes descrito (M4-06). SAP11, el efector validado en maíz, no tiene estructura experimental y su único modelo de complejo es predicho (M4-08). Agrega a R6 la base estructural de SAP05 y PHYL1 y un resultado crítico (resistir al efector no basta para proteger).

## 6. Cruce con microgravedad (método 6)

**No se halló ningún trabajo que una microgravedad, real o simulada, con *Ca.* P. zeae, *S. kunkelii* o parientes cercanos, con estructura o con ensayos.** Cuatro comprobaciones independientes:

1. *Europa PMC* (título y resumen): microgravedad, vuelo espacial, clinostato, RPM, RWV, ISS o vuelo parabólico combinados con *Spiroplasma*, fitoplasma o corn stunt: 0 resultados. Combinados con mollicutes en general: 4, y ninguno tiene un mollicute como sujeto de la microgravedad (dos usan un biorreactor de pared rotatoria, que es **microgravedad simulada**, para armar un epitelio endocervical humano tridimensional (M4-36 con infección por *M. genitalium*; M4-43 con productos microbianos); uno es sobre amino oxidasa en ratas (M4-44) y otro sobre ratones de Apolo XVII (M4-45)). Combinados con cristalización y mollicutes: 9, que coinciden por «space group» y no mencionan microgravedad (se leyeron los resúmenes). Con vectores (*Dalbulus*, cicadélidos, planthoppers): 1, sobre un hongo entomopatógeno (más abajo).
2. *RCSB:* 13 entradas del PDB tienen un método de crecimiento que menciona microgravedad y 86 mencionan microgravedad en el texto; la intersección con las 193 entradas de mollicutes (unión de siete búsquedas) es **0**. Las 20 estructuras de rayos X de *Spiroplasma* y fitoplasmas se cristalizaron por difusión de vapor terrestre.
3. *NASA OSDR:* 0 resultados para *Spiroplasma*, fitoplasma, *Acholeplasma* y mollicutes, y 3 para *Mycoplasma*, todos estudios en humanos sin un mollicute como organismo.
4. *Otras líneas, fuera de M4 y solo como hallazgos de la literatura:* el RNAi funciona en *C. elegans* en órbita baja (M4-34, resumen), y un aislado del hongo entomopatógeno *Beauveria bassiana* generado por mutagénesis en vuelo espacial mostró mayor virulencia contra insectos plaga en laboratorio (M4-35, resumen; es un agente de biocontrol de otro sistema y no se reportan ni se proponen condiciones). Ambos son para M2 y M3.

Distinción pedida: **real** (cristales de microgravedad en el PDB, flagged por los depositantes; OSDR) y **simulada** (RWV en las dos referencias de *M. genitalium*, donde la simulación es del cultivo celular humano y no del micoplasma). Ningún resultado de uno se transfiere al otro, y para estos organismos no hay datos de ninguno.

## 7. Lo que ya cubrió R6 y lo que agrega M4

**R6 ya había cubierto** (no se repite): la ausencia de maquinaria de RNAi por HMM; la cobertura de AlphaFold DB (1.750/1.755 y 5/485) y el 0 de PDB en los dos taxones; PGK, espiralina, P89 y SARP como determinantes en *S. citri* con 93,7 %, 61,1 % y ~62 % de identidad; SAP11 de MBSP y su entrada A0ABM6DLD7; tetraciclinas, cribado de antimicrobianos, AMPs, scFv y bloqueo de entrada como vías con sus riesgos.

**M4 agrega** (con la fuente): (a) la causa de la brecha de AlphaFold DB en *Ca.* P. zeae, que es de fecha; (b) el censo de estructuras de parientes por linaje, con 21 entradas de *Spiroplasma* y *Candidatus* Phytoplasma, que incluyen SAP05 (8), PHYL1 (2), Imp, enzima málica, MreB y FtsZ; (c) la distancia de cada blanco al homólogo estructurado, y que cinco blancos no tienen ninguno detectable; (d) la causa del faltante por blanco y la regla de decisión sobre microgravedad con su conteo (0 de 16); (e) la evidencia de que los cuellos de botella documentados fueron fases y estabilidad, no el crecimiento de cristales; (f) resultados críticos sobre scFv, resistencia a SAP05 y resistencia a péptidos; (g) la ausencia de cualquier cruce con microgravedad; (h) los candidatos SAP05-like y PHYL1-like de M3, con su estatus `[H]` y `[?]`.

## Contradicciones con el repo

| Qué dice el repo | Dónde | Qué dice mi fuente | Fuerza |
| --- | --- | --- | --- |
| R6 deja como faltante «una planta que exprese el scFv» para espiralina | `estrategias.json` E08 | Hay un scFv contra el espiroplasma del achaparramiento expresado en una línea celular de maíz sin resistencia clara en invernáculo (M4-32), y un scFv anti-stolbur en tabaco con retraso de hasta 2 semanas y sin resistencia significativa con el vector (M4-30) | `[R]`, solo resúmenes |
| «Solo 1 de las 522 anotaciones de M3 nombra efector» | R6 `datos/COMANDOS.md` §4 | UniProt (anotación 2025-10-08) nombra «Effector» a 37 de 485 entradas de M3, con nombres tomados de efectores de AYWB; la diferencia es de fuente (RefSeq vs UniProt) y los nombres de UniProt son automáticos y sin verificar | `[E]` los conteos; `[?]` las anotaciones |
| AlphaFold DB cubre «solo el 1,0 %» de *Ca.* P. zeae y haría falta predicción local | R6 §4 y §11, Línea 3 | Se confirma 5/485, pero 480 entradas se crearon el 2025-10-08, después del corte de modelos, de modo que es un faltante de fecha y no de dificultad | `[E]` |
| «Sin PDB en ambos» (taxones) | R6 `datos/COMANDOS.md` §6 | Se confirma para los dos taxid y para cada accesión de la tabla, pero hay 21 entradas de los géneros *Spiroplasma* y *Candidatus* Phytoplasma, incluidos 8 complejos SAP05 y 2 de PHYL1, que R6 no registró | `[E]` |
| «Universo de 126.874 proteínas de mollicutes» para la ausencia de PIWI/PAZ | R6 §2.1, que cita R1 §4.2 | UniProt cuenta 126.874 entradas bajo el taxid 31969 (Mollicutes) pero 193.091 bajo 544448 (Mycoplasmatota): el universo de R1 excluye Mycoplasmoidales (*M. pneumoniae*, *M. genitalium*). No afecta a los dos genomas del problema, que sí están en Mollicutes y se verificaron por HMM en R6 | `[E]` conteos de UniProt |
| El único acierto de SAP54 en M3 fue débil (40,6 % en 32 aa) y no prueba ni homología ni ausencia | R6 §3 y Línea 3 | Se confirma con las secuencias de PHYL1 con PDB (mejor E = 0,16 contra 6JQA/6INR), pero UniProt anota A0ABN4RYC3 como PHYL1, anotación sin respaldo de similitud | `[?]` |
| Línea 3 de R6: factibilidad 2 porque «la cobertura de estructura es del 1,0 %» | `lineas_candidatas.md` | Un candidato de M3 (A0ABM6DM10) comparte una región con el dominio de SAP05 (43,2 % en 81 aa, E 1e-11) y hay 8 estructuras de SAP05: para ese candidato la transferencia de estructura es posible, aunque su función es desconocida | `[H]` |

## Qué no se pudo establecer

No se pudo establecer si alguien intentó cristalizar y falló con alguno de estos blancos: la ausencia de publicaciones no distingue «nadie lo intentó» de «se intentó y no se publicó». Tampoco el valor de las CMI de Novispirin T7 y Caerin 1.1 (solo se leyó el resumen, sin cifras), si el scFv contra *S. kunkelii* de 1998 tuvo una prueba de afinidad (resumen) ni el desenlace del scFv contra Imp de *Ca.* P. aurantifolia en planta. Quedan **26 fuentes bibliográficas leídas solo en resumen** y 4 solo como título; ninguna de las 41 abiertas se leyó linealmente. No se verificó en una fuente abierta que la diana de las tetraciclinas sea el ribosoma (viene del registro de R6), ni la globomicina y la peptidasa de señal II en *Spiroplasma* (R6 la registra como `[R]`; una búsqueda en Europa PMC no la sostuvo y por eso LspA no entró a la tabla). No se verificó la identidad entre la PtsG de *S. citri* y la de *S. kunkelii*, ni la de la timidina quinasa de M3 con la del fitoplasma de Paulownia. Ninguna medición de pLDDT es una medida de precisión: se interpreta solo como confianza del modelo, y la única validación independiente hallada es el reemplazo molecular del Imp de PnWB con un modelo de AlphaFold 2 (n = 1, M4-04).

**No evaluado a esta profundidad:** (1) ARN regulatorio y ARN distinto del 16S (sin Rfam); (2) búsqueda de homología remota por perfiles o plegamiento sobre los blancos sin homólogo (HHblits, Foldseek); (3) modelado local de las 480 proteínas de M3 sin modelo (sin GPU y sin subir secuencias a servicios de terceros); (4) si la microgravedad mejora cristales de proteínas de membrana en general (es de M1); (5) la totalidad del proteoma, ya que la lista es solo lo que tiene fuente abierta de función; (6) TrEMBL bacteriano con PDB en la base de homólogos; (7) la medición de identidad al ortólogo de *S. citri* para PtsG y la de TDK.

**Contracara de riesgo y alcance.** Nada de lo propuesto aumenta la virulencia, la transmisibilidad ni el rango de hospedadores; el trabajo sobre efectores es solo anotación y evaluación retrospectiva de predicciones. No se propone ningún diseño de secuencias de ARN ni de péptidos, ni ningún cultivo de un patógeno bajo microgravedad. Los blancos de proteínas conservadas (PGK, FruK, TDK, enzima málica, ribosoma) tienen riesgo de efecto sobre simbiontes y no objetivo (`[H]`; no se evaluó). La revisión del patosistema del achaparramiento señala el conocimiento molecular limitado de los mecanismos de la enfermedad (M4-37, texto parcial), lo que coincide con la escasez de ensayos hallada. Todas las secuencias usadas son públicas (UniProt, RefSeq, PDB); no se leyó `YHat-Biotech/` ni `work/` y ninguna secuencia se envió a un servicio de terceros. Ninguna página recuperada traía instrucciones dirigidas a sistemas de IA.
