# Catálogo de genes blanco con evidencia en Auchenorrhyncha y su vínculo con *Dalbulus maidis*

Investigación C5 de la ola 3. Fecha: 2026-10-20. Una fila por gen y por estudio.
La fuente de verdad estructurada es [`catalogo_genes_blanco.json`](catalogo_genes_blanco.json); este
documento es la lectura en prosa. Marcadores según `CLAUDE.md`.

## Qué agrega este catálogo y qué hereda

El catálogo tiene **36 filas**: **16** vienen de `pipeline/blancos_hemipteros.py` y no se
rehicieron, y **20** las agrega esta investigación. El campo `estado` de cada fila dice cuál
es cuál, y el campo `apertura` dice con qué profundidad se abrió la fuente: texto completo leído por C5,
resumen de PubMed abierto por C5 vía E-utilities, texto completo ya leído en la ola 2 (`W1_papers`), o
fila heredada que C5 no abrió. Esa distinción importa porque el catálogo del pipeline cita varias filas
de segunda mano —«citado por Jones 2021», «citado por Dalaison-Fuentes 2022»— y una cita de segunda mano
no habilita a reportar dosis ni magnitudes.

De las 36 filas, **25 son de Cicadellidae**, la familia de la chicharrita, y de ésas
**cinco corresponden a la propia *D. maidis***. El resto reparte entre Delphacidae —delfácidos del maíz,
que son el pariente funcional más cercano con literatura abundante— y otros hemípteros que el pipeline
ya tenía.

## Lo que cambia el panorama

Tres cosas que el catálogo anterior no tenía y que esta investigación aporta.

**Hay un blanco letal *y* esterilizante probado en dos géneros de cicadélidos, publicado en 2025.** El
trabajo sobre la subunidad reguladora del proteasoma 26S que los autores llaman `Rpn6` es el estudio más
directamente transferible del catálogo: *Scaphoideus titanus* y *Euscelidius variegatus* son cicadélidos
de la misma subfamilia que *Dalbulus* (Deltocephalinae), la entrega es microinyección abdominal de 0,5 µL
a 160 ng/µL —80 ng por insecto—, y el resultado es a la vez mortalidad y esterilidad femenina `[E]`. En
*E. variegatus* la progenie cae a 0,03 ninfas por día de oviposición contra 1,5 de los no tratados, y los
cruzamientos muestran que el efecto es de la hembra y no del macho.

**La misma línea de trabajo publicó el dato de especificidad en el formato que nos sirve.** Para diseñar
el ARNdc eligieron la región *menos* conservada del gen usando *Apis mellifera* como referencia de
polinizador, y reportan la tabla que hacía falta: identidad del ADNc de 82,9 % entre *S. titanus* y
*E. variegatus*, con 5 tramos idénticos de más de 16 nt y un máximo de 29 nt consecutivos; contra las dos
entradas de *A. mellifera*, 53,7 % y 54,5 % de identidad y **cero** tramos de más de 16 nt, con un máximo
de 7 y 6 nt `[E]`. Es exactamente el criterio que el repositorio ya usaba —identidad promedio no predice
riesgo, tramos perfectos sí— pero publicado y con números.

**Hay dos contraejemplos, y valen tanto como los blancos.** Silenciar `uk1_LRR` en *E. variegatus*
**aumentó** la colonización del vector por el fitoplasma, y silenciar `NcHig` en *Nephotettix cincticeps*
**aumentó** la infección del sistema nervioso por un rabdovirus `[R]`. Un gen cuyo silenciamiento favorece
al patógeno es un gen a excluir explícitamente, y ninguno de los dos aparecería como riesgoso en un
tamizaje de esencialidad o de off-targets.

## Las filas nuevas

| id | especie | gen | entrega | dosis | resultado medido | apertura |
|---|---|---|---|---|---|---|
| `DM-05` | *Dalbulus maidis* | `eth` | microinyeccion en ninfa V recien mudada | 0,25 uL a 500 ng/uL = 125 ng por insecto | knockdown ~90 %; supervivencia 10 % a dia 4 contra >95 % del control de b-lactamasa | texto_completo_ola2 |
| `DM-06` | *Dalbulus maidis* | `burs-alpha` | microinyeccion en ninfa V recien mudada | 0,25 uL a 500 ng/uL = 125 ng por insecto | knockdown ~95 %; supervivencia 10 % a dia 4 contra >95 % del control | texto_completo_ola2 |
| `CI-01` | *Scaphoideus titanus* | `Rpn6 (segun los autores)` | microinyeccion abdominal | 0,5 uL a 160 ng/uL = 80 ng por insecto | transcripto baja 6,3x (3 dpi), 8,7x (7), 7,9x (14) y 14,9x (21 dpi); supervivencia menor que dsGFP (p=0,028), que buffer (p=0,027) y que no tratados (p<0,001); ovarios sin huevos y morfologia anormal | texto_completo_C5 |
| `CI-02` | *Euscelidius variegatus* | `Rpn6 (segun los autores)` | microinyeccion abdominal del ARNdc disenado sobre S. titanus | 0,5 uL a 160 ng/uL = 80 ng por insecto | transcripto baja 12,6x (7 dpi), 11,2x (14) y 5,8x (21 dpi); supervivencia menor que dsGFP (p<0,001); progenie 0,03 ninfas por dia de oviposicion contra 1,5 (no tratados), 1,1 (buffer) y 0,3 (dsGFP); en cruzamientos el efecto es de la hembra (0,25 contra 1,19) | texto_completo_C5 |
| `CI-03` | *Scaphoideus titanus* | `ATP synthase beta` | microinyeccion abdominal | 0,5 uL a 160 ng/uL = 80 ng por insecto | transcripto baja de 5x (3 dpi) a 46x (20 dpi), p<0,001 salvo 8 dpi (p=0,007); SIN efecto sobre la supervivencia hasta 14 dpi; morfologia de huevos alterada a 20 dpi; hexamerina sobreexpresada | texto_completo_C5 |
| `CI-04` | *Euscelidius variegatus* | `ATP synthase beta` | microinyeccion | no extraida (texto completo no accesible) | reduccion exponencial de la expresion desde las 72 h y hasta 14 dias, casi completa; caida significativa de la supervivencia frente al control de dsGFP; efecto dependiente de tiempo y dosis para actina | resumen_C5 |
| `CI-05` | *Euscelidius variegatus* | `muscle actin` | microinyeccion | no extraida | silenciamiento casi completo y caida significativa de la supervivencia frente a dsGFP | resumen_C5 |
| `CI-06` | *Euscelidius variegatus* | `ATP synthase beta (efecto sobre el patogeno)` | microinyeccion | no extraida | silenciamiento sostenido hasta al menos 37 dpi, reduccion media de 100 veces; menos adquisicion de fitoplasma; pico de 21 nt en los ARN pequenos derivados | resumen_C5 |
| `CI-07` | *Euscelidius variegatus* | `chc (clathrin heavy chain)` | alimentacion artificial con ARNdc | no extraida | baja la expresion en intestino y cabeza y reduce la colonizacion de intestino y glandulas salivales; en el trabajo de 2026, menos colonizacion y menos transmision a haba | resumen_C5 |
| `CI-08` | *Euscelidius variegatus* | `uk1_LRR` | RNAi in vivo | no extraida | silenciarlo AUMENTO la colonizacion del vector por el fitoplasma, sin efecto sobre la transmision a planta | resumen_C5 |
| `CI-09` | *Euscelidius variegatus y Scaphoideus titanus* | `natterin y legumain` | microinyeccion (2024) y hoja cortada con 7 ug por tubo (2024, metodo) | 7 ug por tubo en la via mediada por planta | reduccion significativa de la multiplicacion del fitoplasma tras la adquisicion; silenciamiento a 17 y 24 dias por via vegetal; ninguno de los tres genes afecto la supervivencia | resumen_C5 |
| `CI-10` | *Nephotettix cincticeps* | `Nc-TnC (troponina C)` | microinyeccion y alimentacion por membrana | no extraida | baja la supervivencia, la capacidad de alimentacion, el peso y la fecundidad | resumen_C5 |
| `CI-11` | *Nephotettix cincticeps* | `NcLac2 y NcLac5` | RNAi en ninfas | no extraida | alta mortalidad; las ninfas con NcLac2 silenciado se despigmentan, quedan con cuticula blanda y mueren | resumen_C5 |
| `CI-12` | *Nephotettix cincticeps* | `NcLac2 (RNAi parental)` | microinyeccion a la madre | 9 ng por hembra | fuerte knockdown en ninfas de primer estadio, alta mortalidad y despigmentacion; efecto sostenido 12-14 dias tras la inyeccion | resumen_C5 |
| `CI-13` | *Nephotettix cincticeps* | `NcHig` | RNAi | no extraida | silenciarlo AUMENTA la infeccion del sistema nervioso por el rabdovirus RYSV | resumen_C5 |
| `DE-02` | *Peregrinus maidis* | `Ruvbl1` | microinyeccion | no localizada en el texto extraido | sin ovocitos maduros a 8 y 12 dias; menos huevos puestos a 8 y 12 dias; caida drastica de la eclosion en todos los tiempos; aumento de masa corporal de las hembras | texto_completo_C5 |
| `DE-03` | *Peregrinus maidis* | `tra-2 (transformer-2)` | RNAi en ninfas (y CRISPR aparte) | no extraida | las hembras se transforman en pseudomachos con ovipositor deformado; los machos quedan esteriles | resumen_C5 |
| `DE-04` | *Peregrinus maidis* | `PmABCB_160306_3, PmABCE_118332_5, PmABCF_24241_1` | RNAi | no extraida | ABCE y ABCF: alta mortalidad en menos de 5 dias; ABCB: desarrollo ovarico impedido; ABCE: melanizacion localizada | resumen_C5 |
| `DE-05` | *Peregrinus maidis* | `XPO1 (exportina 1)` | microinyeccion | no extraida | menor supervivencia y reproduccion de las hembras y menor acumulacion del rabdovirus MMV a 12 y 15 dias | resumen_C5 |
| `DE-06` | *Delphacodes kuscheli* | `eth y burs-alpha` | microinyeccion en ninfa V | 0,25 uL a 500 ng/uL = 125 ng por insecto | mismo diseno experimental que en D. maidis; ver fuente para la magnitud por especie | texto_completo_ola2 |

La columna `apertura` no es un detalle administrativo: de las filas nuevas, **seis** se apoyan en texto
completo abierto (cuatro por C5, dos por la ola 2) y el resto en el resumen de PubMed. Para esas últimas,
el catálogo registra el fenotipo pero no la dosis ni el `n`, porque el resumen no los trae. Son filas
utilizables para decidir a qué paper ir, no para citar una magnitud.

## Las filas heredadas del pipeline

| id | especie | gen | resultado reportado | fuente | apertura |
|---|---|---|---|---|---|
| `DM-01` | *Dalbulus maidis* | `BicC` | oviposicion casi nula; transcripto baja >170x por inyeccion al dia 7 | Dalaison-Fuentes et al. 2022, Pest Manag Sci (PMID 35442515, doi 10.1002/ps.6937) | texto_completo_ola2 |
| `DM-02` | *Dalbulus maidis* | `V-ATPase B` | supervivencia 16 % a dia 4 contra 37 % del control de GFP; alas deformes | Jones, Bernal y Medina 2021 (leido completo en ola 2) | texto_completo_ola2 |
| `DM-03` | *Dalbulus maidis* | `V-ATPase D` | supervivencia 18 % a dia 4; efecto en alas no significativo | Jones, Bernal y Medina 2021 (leido completo en ola 2) | texto_completo_ola2 |
| `DM-04` | *Dalbulus maidis* | `Dmai-dsRNase-2` | silenciarla mejora la respuesta al ARNdc del gen de interes | Pestic Biochem Physiol 2023 (PMID 37945254, doi 10.1016/j.pestbp.2023.105618) | resumen_C5 |
| `DE-01` | *Peregrinus maidis* | `V-ATPase B y V-ATPase D` | al menos 27x de reduccion del transcrito a 2 dias por inyeccion y ~2x tras 6 dias de ingesta; mayor mortalidad y menor fecundidad que el control de dsGFP | Yao, Rotenberg, Afsharifar, Barandoc-Alviar y Whitfield 2013, PLoS ONE 8(8):e70243 (doi 10 | texto_completo_C5 |
| `HE-01` | *Nilaparvata lugens* | `Bicaudal-C` | papel vital en oogenesis | Zhang et al. 2015, citado por Dalaison-Fuentes 2022 | no_abierta |
| `HE-02` | *Nezara viridula* | `V-ATPase A` | 45 % de mortalidad | Sharma et al. 2020, citado por Jones 2021 | no_abierta |
| `HE-03` | *Halyomorpha halys* | `JHAMT y vitelogenina` | silenciamiento por varias vias de entrega | Ghosh et al. 2018, citado por Jones 2021 | no_abierta |
| `HE-04` | *Diaphorina citri* | `catepsina D, quitina sintasa, IAP` | mortalidad hasta 64 % a 120 h, creciente con la dosis, pero el knockdown NO correlaciona con la dosis y el control de dsGFP a 500 y 1000 ng/uL ya mata mas que e | Galdeano, Breton, Spotti Lopes, Falk y Machado 2017, PLoS ONE 12(3):e0171847 (doi 10.1371/ | texto_completo_ola2 |
| `HE-05` | *Rhodnius prolixus* | `BicC` | necesario para el epitelio folicular | Pascual et al. 2021, citado por Dalaison-Fuentes 2022 | no_abierta |
| `HE-06` | *Homalodisca vitripennis* | `actina` | efecto sobre el ARNm de actina | Rosa et al. 2010 y 2012, citados por Dalaison-Fuentes 2022 | no_abierta |
| `HE-07` | *Nephotettix cincticeps* | `NcSP75` | longevidad a la mitad, retraso del desarrollo, menos huevos | Matsumoto y Hattori 2018, citado por Dalaison-Fuentes 2022 | no_abierta |
| `HE-08` | *Nephotettix cincticeps* | `dosis alta de dsRNA (control)` | mortalidad alta por la dosis, no por el blanco | Tomizawa y Noda 2013, citado por Dalaison-Fuentes 2022 | no_abierta |
| `HE-09` | *Circulifer haematoceps* | `hexamerina` | necesaria para la respuesta inmune | Eliautout et al. 2016, citado por Dalaison-Fuentes 2022 | no_abierta |
| `HE-10` | *Amrasca biguttula* | `varios` | demostracion de RNAi en un cicadelido del algodon | Singh et al. 2018, citado por Dalaison-Fuentes 2022 | no_abierta |
| `HE-11` | *Graminella nigrifrons* | `respuesta inmune` | RNAi funcional en la interaccion con el virus | Chen, Redinbaugh y Michel 2015, citado por Dalaison-Fuentes 2022 | no_abierta |

## Ventanas de 21 nt eficientes, sólo donde hay secuencia pública

El investigador pidió, para cada gen nuevo, cuántas ventanas de 21 nt eficientes tendría y cuál sería su
mejor región. Eso se calculó **sólo donde existe secuencia pública**, con el port de si-Fi21 sin
modificar (`tools/sifi21_port/run_sifi.py`, modo `fiel`, backend ViennaRNA 2.7.2, ventana de región de
200 nt). Ocho filas del catálogo tienen el cálculo. Para los genes de *D. maidis* la secuencia es de la
propia especie (GenBank `PZ371507.1` y `PZ371508.1`); para los demás hubo que usar el ortólogo del
cicadélido anotado *Macrosteles quadrilineatus* o el transcrito TSA publicado del propio estudio, y eso
**es un sustituto declarado, no la secuencia que se sintetizaría** `[H]`.

| gen (secuencia usada) | largo | ventanas | eficientes | % | mejor región de 200 nt | eficientes en la región |
|---|---:|---:|---:|---:|---|---:|
| `eth_Dmaidis_PZ371507` | 615 | 595 | **44** | 7.4 | 194-393 | 24 |
| `bursA_Dmaidis_PZ371508` | 468 | 448 | **33** | 7.4 | 45-244 | 20 |
| `Rpn6_Stitanus_GJQL01135962` | 1413 | 1393 | **179** | 12.8 | 1123-1322 | 51 |
| `Rpn6_Evariegatus_GFTU01006765` | 1483 | 1463 | **112** | 7.7 | 87-286 | 36 |
| `ATPsynBeta_Mquadrilineatus_XM_054410120` | 1855 | 1835 | **111** | 6.0 | 78-277 | 29 |
| `TnC_Mquadrilineatus_XM_054409464` | 683 | 663 | **38** | 5.7 | 453-652 | 21 |
| `Ruvbl1_Mquadrilineatus_XM_054402769` | 1507 | 1487 | **123** | 8.3 | 1-200 | 26 |
| `XPO1_Mquadrilineatus_XM_054404977` | 4429 | 4409 | **397** | 9.0 | 1310-1509 | 43 |

Para dimensionarlo contra lo que ya sabemos: los cuatro candidatos de EPILAB dan 42, 32, 133 y 212
siRNA eficientes con el programa original (`research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md` §0),
y la densidad de los candidatos nuevos —entre 5,7 % y 12,8 % de ventanas eficientes— cae en el mismo
rango. **Ningún gen nuevo se destaca por densidad de eficientes**, lo que es coherente con el resultado
negativo que el pipeline ya había medido: lo que discrimina es qué gen se ataca y el filtro de
especificidad, no la densidad de ventanas `[H]`.

## El riesgo de especificidad de cada candidato nuevo

El tamizaje corrió con `tools/sifi21_port/offtarget_21nt.py`, por coincidencia exacta en las dos hebras,
contra cinco referencias locales. La tabla da `21-meros perfectos / bloques perfectos de ≥19 nt`.

| gen (secuencia usada) | genoma *D. maidis* | *M. quadrilineatus* | *H. vitripennis* | *Z. mays* | *A. mellifera* |
|---|---|---|---|---|---|
| `eth_Dmaidis_PZ371507` | 539/553 | 21/52 | 1/5 | 0/0 | 0/0 |
| `bursA_Dmaidis_PZ371508` | 398/410 | 0/4 | 0/0 | 0/0 | 0/0 |
| `Rpn6_Stitanus_GJQL01135962` | 14/89 | 18/37 | 6/18 | 1/8 | 0/6 |
| `Rpn6_Evariegatus_GFTU01006765` | 22/91 | 15/34 | 6/18 | 0/3 | 2/6 |
| `ATPsynBeta_Mquadrilineatus_XM_054410120` | 203/336 | 1835/1835 | 65/124 | 3/23 | 0/3 |
| `TnC_Mquadrilineatus_XM_054409464` | 17/72 | 663/663 | 9/33 | 2/25 | 0/3 |
| `Ruvbl1_Mquadrilineatus_XM_054402769` | 58/101 | 1487/1487 | 4/18 | 0/3 | 0/4 |
| `XPO1_Mquadrilineatus_XM_054404977` | 271/592 | 4409/4409 | 29/83 | 0/13 | 3/39 |

Dos lecturas, y las dos cambian decisiones.

**La primera columna no es un off-target: es la prueba de transferencia.** Los dos genes de *D. maidis*
recuperan casi todas sus ventanas en el genoma del vector —539 de 595 en `eth` y 398 de 448 en
`burs-alpha`—, que es lo que se espera al alinear un transcrito contra el genoma de su propia especie, con
las uniones exón-exón como diferencia. En cambio, los ortólogos de otras especies retienen entre el 0,7 %
y el 11,1 % de sus 21-meros: 14 de 1.393 para `Rpn6` de *S. titanus*, 9 de 1.331 para el ortólogo de
*M. quadrilineatus*, 203 de 1.835 para la ATP sintasa β. **Un ARNdc diseñado sobre el ortólogo de un
cicadélido pariente no sirve para *D. maidis***: hay que recuperar la secuencia del vector antes de
diseñar, y eso es exactamente lo que el circuito de ingeniería inversa tiene que producir `[H]`.

**La tercera columna es el riesgo que ya conocíamos, cuantificado por gen.** *Homalodisca vitripennis* es
el cicadélido no objetivo del panel (`research/ola2/W5_secuencias_epilab/REPORT.md` §5). La ATP sintasa β
comparte 65 21-meros perfectos con su transcriptoma, el valor más alto del conjunto; `XPO1` 29, la
troponina C 9, y los tres `Rpn6` entre 1 y 6. En la escala de este catálogo eso ordena a los candidatos
nuevos por riesgo en cicadélidos no objetivo: **la ATP sintasa β es el más conservado y por eso el más
penalizado**, y la familia del proteasoma es la más limpia `[H]`. La ATP sintasa β además aparece con 3
21-meros perfectos en el transcriptoma de maíz, que es el cultivo a proteger.

## Lista corta para sumar al ranking, ordenada por evidencia

El orden es por calidad de evidencia y cercanía filogenética, no por conveniencia de cálculo.

1. **`eth` y `burs-alpha` de *D. maidis*.** Única evidencia funcional en la especie objetivo además de
   `BicC` y la V-ATPasa: knockdown de ~90 % y ~95 % y supervivencia del 10 % al día 4 contra más del 95 %
   del control, con n=40 por tratamiento y 125 ng por insecto `[E]`. Tienen ARNm público de la propia
   especie, se les calcularon las ventanas, y su mejor región de 200 nt es 194-393 (24 eficientes) y
   45-244 (20 eficientes). Es el candidato de menor riesgo de extrapolación del catálogo entero.

2. **La subunidad del proteasoma 26S que los autores llaman `Rpn6`.** Mortalidad y esterilidad en dos
   géneros de cicadélidos de nuestra subfamilia, con diseño de especificidad publicado `[E]`. Entra con una
   advertencia de identidad de gen que está en la fila `CI-01` y que hay que resolver antes de diseñar
   nada: por secuencia, el transcrito usado pertenece a la familia PSMD6 y no a PSMD11/Rpn6 `[?]`.

3. **`Ruvbl1`.** Esterilización en un delfácido del maíz, con texto completo abierto `[E]`. Es el mejor
   candidato para el objetivo «estéril» del pipeline entre los genes nuevos, y tiene ortólogo anotado en
   el cicadélido de referencia.

4. **`XPO1` (exportina 1).** Supervivencia, reproducción *y* acumulación del rabdovirus en el mismo
   experimento `[R]`, sobre resumen únicamente. Es el único candidato del catálogo que ataca al vector y a
   un patógeno a la vez, y ese doble efecto es argumentable aunque la fuente esté sin abrir del todo.

5. **ATP sintasa β.** La evidencia en cicadélidos es la más repetida del catálogo —tres estudios, dos
   especies— pero es también la peor noticia de especificidad: 65 21-meros perfectos en el cicadélido no
   objetivo y 3 en maíz. Entra al ranking como caso de prueba del filtro, no como candidato preferido `[H]`.
   Y en *S. titanus* el silenciamiento de 5 a 46 veces **no afectó la supervivencia** hasta 14 dpi: sirve
   para esterilizar, no para matar.

Fuera de la lista corta, pero anotados: la troponina C tiene al menos cuatro parálogos anotados en el
cicadélido de referencia, de modo que el off-target intraespecífico es alto antes de empezar; `NcLac2` no
tiene ortólogo localizable por nombre en los proteomas de cicadélido disponibles; y `chc`, `natterin` y
`legumain` son blancos de la vía «patógeno dentro del vector», que la decisión vigente del equipo dejó en
segundo plano.

## Qué datos de EPILAB harían falta para validar estos candidatos

Cuatro cosas, en orden de cuánto destraban.

La primera es el **transcriptoma de *D. maidis* ensamblado**, si lo tienen sin publicar. Sin él, para
todos los candidatos nuevos salvo `eth` y `burs-alpha` estamos calculando ventanas sobre el ortólogo de
otra especie, y la propia medición de transferencia de arriba muestra que eso no sirve para diseñar. Es el
mismo pedido que W4 ya había hecho, ahora con una medición que lo cuantifica.

La segunda es **cuál de los dos objetivos de control les interesa**, matar o esterilizar. El catálogo
nuevo está sesgado hacia esterilidad —`Rpn6`, `Ruvbl1`, `tra-2`, ATP sintasa β en *S. titanus*— y el
ranking del pipeline ordena distinto según el objetivo.

La tercera es **si cuentan a *Macrosteles quadrilineatus* y a otros cicadélidos como organismos no
objetivo**. Es la pregunta que el pipeline ya dejó abierta y que decide si la ATP sintasa β queda dentro o
fuera.

La cuarta es **acceso al texto completo de las cinco fuentes que quedaron en resumen**, empezando por
Pest Manag Sci 2019 (PMID 30417535), que es el único estudio de mortalidad por ARNi en *E. variegatus* y
está detrás de muro de pago.

