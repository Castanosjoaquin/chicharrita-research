# W5 — Las secuencias de EPILAB: qué son, qué tocan y cómo las aprovechamos

**Material.** `YHat-Biotech/Sequences_EPILAB.xlsx`, una planilla de 11.617 bytes con
cuatro candidatos y ocho secuencias (cuatro «completas» y cuatro «regiones elegidas
para RNAi»). Es el material no publicado del corpus. Todo el análisis de esta
investigación se corrió **local** sobre copias en `work/W5/`: BLAST+ 2.17.0 de
Bioconda, ViennaRNA 2.7.2 y código propio. Ninguna de estas secuencias se subió al
BLAST web del NCBI, a dsRNA-Engineer ni a ningún servidor de plegado. Lo único que
usó la red fue la **descarga** de referencias públicas desde el NCBI. El detalle de
cada corrida, con sus comandos y versiones, está en `analisis/COMANDOS.md`.

**Convención de evidencia.** `[E]` establecido, `[R]` reportado por una o pocas
fuentes, `[H]` hipótesis nuestra, `[?]` incierto o con fuentes en conflicto. Cuando
la afirmación es una medición nuestra, dice con qué herramienta se midió.

---

## Resumen de la sección 6: cómo aprovechamos estas cuatro secuencias

Las cuatro sirven, pero no para lo mismo, y conviene decirlo en orden de retorno
sobre el esfuerzo. Están desarrolladas, con requisitos y riesgos, en
`aprovechamiento.md`.

**Primero: son el conjunto de validación que nos faltaba.** Son cuatro candidatos
reales, ya elegidos por el laboratorio que organiza el track, con su región
seleccionada y su posición dentro del gen. Cualquier método de priorización que
propongamos —el ranking por atención de R2, un scoring de riesgo, una métrica de
conservación— tiene ahora cuatro casos con los que calibrarse y una pregunta
concreta que contestar: la del organizador, «¿cuáles merecen validación y por qué?».
Es el uso de menor costo y mayor impacto para cuatro personas sin laboratorio.

**Segundo: habilitan una ingeniería inversa parcial de los criterios de diseño.** La
columna «Nro de eficientes por gen» (114, 35, 199 y 33) implica un tamizaje previo
que clasifica siRNA como eficientes. Reimplementamos localmente los criterios
publicados que mejor encajan con esa terminología y **no logramos reproducir los
cuatro números**: nuestra versión más literal queda corta (87, 21, 136, 26) y la
variante que acepta cualquiera de las dos hebras como guía se pasa (179, 43, 259,
62). Los valores declarados caen entre ambas. Es un vacío documentado y una pregunta
de una línea para el investigador, no un detalle menor: sin ese criterio no se puede
auditar ni extender el tamizaje de EPILAB.

**Tercero: el hallazgo de riesgo que el tamizaje local sí produjo.** La región
elegida de `CP_MRFV` es 100 % idéntica al aislado de referencia de Costa Rica
(`NC_002786.2`) y diverge 6,5-8,5 % de los 45 registros brasileños de MRFV; de los
180 siRNA posibles, la mediana de los que mantendrían apareamiento perfecto contra
un aislado brasileño es **44**. En GenBank **no hay ninguna secuencia de MRFV de
Argentina** (71 registros: 45 de Brasil, 4 de Estados Unidos, 2 de Ecuador, 1 de
Costa Rica, 19 sin país declarado). Un disparador diseñado sobre la referencia
centroamericana puede perder buena parte de su población de siRNA efectivos frente
al virus local `[H]`, y verificarlo requiere secuencia del aislado argentino, que no
existe públicamente. Esto es una contribución directa a la pregunta de priorización.

**Cuarto: los dos candidatos del insecto están limpios donde importa y no donde se
suele mirar.** Con el criterio estándar de coincidencia perfecta de 19 nt
contiguos, ninguno de los 920 siRNA derivados de las cuatro regiones tiene blanco
perfecto en abeja (*Apis mellifera*), vaquita (*Harmonia axyridis*) ni colémbolo
(*Folsomia candida*), y en maíz apenas hay tres coincidencias de 19 nt exactos por
región, ninguna de 21/21. Pero contra *Homalodisca vitripennis* —un cicadélido no
objetivo, usado acá como proxy de otros cicadélidos— la región de `BicC_Dm` tiene
**30 siRNA con coincidencia perfecta, 22 de ellos de los 21 nt completos**, y la de
`ATPaseD_Dm` tiene 7. El riesgo de estos diseños no está en el maíz ni en los
polinizadores: está en los parientes cercanos del vector.

---

## 1. Inventario: qué hay exactamente en la planilla

La planilla tiene una sola hoja (`Hoja1`), ocho columnas y cuatro filas de datos.
Los metadatos del documento declaran a **Johan Rodríguez** como creador y último
modificador, con creación el 17 de octubre de 2026 a las 15:03:07 UTC y última
modificación siete minutos después, 15:10:01 UTC, desde Microsoft Excel 16.0300
`[E]` (`docProps/core.xml` y `docProps/app.xml` del propio archivo). Es el mismo
nombre que figura como autor del PDF de la sesión técnica oficial según el
manifiesto, lo que ata la planilla al organizador y no a un tercero `[R]`.

Hay tres rangos combinados: `G1:H1`, que convierte el encabezado «Position dentro
del gen» en una cabecera de dos columnas —inicio y fin—, y `A2:A3` y `A4:A5`, que
agrupan las filas de a dos por organismo. Las ocho columnas son, en orden:
organismo (rotulado «Patógenos», lo cual es impreciso porque *Dalbulus maidis* es el
vector y no un patógeno `[E]`), gen elegido, función, secuencia completa, número de
siRNA eficientes por gen, secuencia elegida para RNAi, e inicio y fin de esa región
dentro del gen.

Los nombres de los genes codifican un esquema transparente: **gen_organismo**, con
`_MRFV` para el virus y `_Dm` para el insecto (`MP_MRFV`, `CP_MRFV`, `BicC_Dm`,
`ATPaseD_Dm`). No hay número de versión, ni identificador de construcción, ni
referencia a un acceso de base de datos, ni fecha, ni autor del diseño: los
metadatos describen el **blanco**, no el **producto**. Esto importa para la sección
6: no sabemos si estas secuencias ya fueron sintetizadas, ni si corresponden a una
construcción concreta con promotores y regiones flanqueantes; lo que tenemos es la
elección de blanco y de región `[?]`.

Las ocho secuencias están escritas en alfabeto `ACGT` estricto, sin ambigüedades ni
caracteres raros: verificado con el conteo de bases, que da exactamente cuatro
símbolos distintos en las ocho. Los largos y el contenido GC, calculados por
nosotros, son los siguientes.

| Candidato | Completa | GC completa | Región elegida | GC región | Posición declarada | siRNA «eficientes» |
| --- | --- | --- | --- | --- | --- | --- |
| `MP_MRFV` | 1.263 nt | 63,10 % | 200 nt | 61,50 % | 1-200 | 114 |
| `CP_MRFV` | 528 nt | 65,91 % | 200 nt | 65,00 % | 200-400 | 35 |
| `BicC_Dm` | 2.520 nt | 51,90 % | 300 nt | 49,33 % | 264-563 | 199 |
| `ATPaseD_Dm` | 491 nt | 46,03 % | 300 nt | 47,00 % | 151-450 | 33 |

Dos verificaciones que hicimos y que conviene registrar. La primera: **cada región
elegida es subcadena exacta de su secuencia completa**, sin un solo cambio de base,
así que las «regiones elegidas» son recortes y no rediseños `[E]` (búsqueda de
subcadena exacta, local). La segunda: **la convención de coordenadas no es uniforme**.
`MP_MRFV` arranca en la posición 1 y mide 200 nt, es decir 1-200 inclusivo, en base
1. `BicC_Dm` arranca en la 264 y mide 300, o sea 264-563 inclusivo, también en base
1. `ATPaseD_Dm`, igual: 151-450. Pero `CP_MRFV` dice 200-400 y su región empieza
realmente en la posición **201**: ahí el 200 es un índice en base 0, o un extremo
abierto. Es una inconsistencia menor de una celda, pero si alguien reconstruye las
regiones por coordenadas en vez de por búsqueda de subcadena, introduce un
corrimiento de un nucleótido en un candidato `[?]`.

Un último dato de inventario, que es el que reordena la ola 1: **no hay ningún
candidato dirigido al fitoplasma ni al espiroplasma**. Los cuatro apuntan a un virus
(dos) o al vector (dos). La ola 1 había predicho exactamente eso, por la ausencia de
maquinaria de RNAi en mollicutes, y el corpus lo confirma: de los cuatro agentes del
complejo que el propio organizador enumera, los candidatos preliminares cubren uno
solo, y los otros dos candidatos atacan al insecto. No es una omisión de la planilla;
es una decisión biológica coherente con el mecanismo `[E]`.

---

## 2. Qué son: identificación por alineamiento local

Las cuatro secuencias completas son **ADN que representa ARN**: están escritas con T
en vez de U, pero MRFV es un virus de ARN de cadena simple positiva `[E]` (R1,
sección 3) y las dos del insecto corresponden a transcritos. Las cuatro son
codificantes. La identificación se hizo con BLAST+ local contra referencias públicas
descargadas a disco, nunca enviando la consulta a un servidor.

### 2.1 `MP_MRFV` — el gen de la proteína de movimiento, tomado tal cual de la referencia

`blastn` local contra los 71 registros públicos de MRFV da **1.263 de 1.263
nucleótidos con 100,000 % de identidad** en las posiciones 332 a 1.594 de
`NC_002786.2`, el genoma de referencia del aislado Costa Rican, y lo mismo contra
`AF265566.2`, que es el registro de GenBank equivalente. Al abrir el GenBank de esa
referencia, esas posiciones **son exactamente los límites del CDS anotado**
`332..1594`, `locus_tag IM012_gp2`, producto «putative movement protein», nota «43
kD», proteína `NP_115455.2` `[E]`. Dicho de otro modo: la secuencia no es un recorte
elegido por criterio propio, es **el gen anotado copiado de extremo a extremo**,
codón de inicio y codón de terminación incluidos (420 codones más el stop = 1.263 nt,
consistente con nuestro escaneo de ORF, que encuentra 420 aminoácidos sin
interrupción en el marco +1).

El escaneo de los seis marcos devuelve algo que al principio parece un error y no lo
es: hay **dos marcos largos y abiertos a la vez**, el +1 con 420 codones y un solo
stop, y el +3 con 420 codones y ninguno. El `tblastn` local lo explica: la
poliproteína `NP_115454.2` alinea con 100 % de identidad en el marco +3 (residuos 70
a 485) y la proteína de movimiento `NP_115455.2` en el marco +1. Es la arquitectura
conocida de los marafivirus, con el gen de movimiento solapado y desfasado respecto
del gen de la replicasa `[E]`. Consecuencia práctica, y es concreta: **un ARNdc
diseñado sobre esta región ataca simultáneamente dos productos del virus**, la
proteína de movimiento y una porción de la poliproteína de replicación, porque el
mismo tramo de genoma se lee de dos maneras `[H]` (la inferencia es nuestra; los
alineamientos que la sostienen son `blastn`/`tblastn` locales).

### 2.2 `CP_MRFV` — la región de la cápside, dentro de la poliproteína

`blastn` local: **528 de 528 nt, 100,000 % de identidad**, posiciones 5.674 a 6.201
de `NC_002786.2`. Esa ventana cae dentro del CDS de la poliproteína (`127..6213`,
producto «polyprotein», 224 kD, cuya nota declara que contiene
metiltransferasa, helicasa, proteasa, replicasa y **proteínas de la cápside**). El
cálculo de marco es exacto: (5.674 − 127) = 5.547, divisible por tres, así que la
región empieza justo en un codón, el 1.850 de la poliproteína, y termina en el 2.025,
cuatro codones antes del final. El `tblastn` confirma el tramo (residuos 1.859-2.025
de `NP_115454.2`, 100 % de identidad) y nuestro escaneo de ORF encuentra 176 codones
sin stop en el marco +1, que es exactamente 528/3.

La asignación «proteína de cápside» que trae la planilla es correcta y está
sostenida por una segunda evidencia independiente: la región tiene 97-99 % de
identidad con los registros `U97721.1`-`U97725.1`, depositados en GenBank como
«coat protein mRNA, partial cds» de distintos aislados. MRFV expresa más de una
forma de cápside y cuál de ellas cubre esta ventana no lo podemos decidir con el
material local `[?]`; lo que sí está establecido es que el tramo es la región
codificante de cápside en el extremo 3′ de la poliproteína `[E]`.

### 2.3 `BicC_Dm` — Bicaudal C de *Dalbulus maidis*, un transcrito de 17 exones

Acá la identificación necesitó dos pasos, porque no existe ningún ARNm de *D.
maidis* anotado para este gen en GenBank (la búsqueda `"Dalbulus maidis"[Organism]
AND bicaudal` devuelve **cero** registros, y la especie tiene en total 92 registros
de nucleótidos, casi todos de COI mitocondrial).

Primer paso, organismo: `blastn` local contra el ensamblado cromosómico
`GCA_975739785.1` (ihDalMaid1.1, Wellcome Sanger Institute, colonia del insectario
del John Innes Centre, Norwich, noviembre de 2024) alinea la secuencia completa en
**17 bloques, todos en el cromosoma 3** (`OZ319706.1`), entre las posiciones
38.450.006 y 38.513.708, con identidades de 97,6 a 100 %. Los bloques son exones: el
patrón de tramos de 110 a 248 nt separados por intrones de varios kb es
inequívoco `[E]`. La secuencia es, entonces, un **transcrito de *D. maidis***, no una
secuencia genómica ni de otra especie, con confianza alta.

Segundo paso, gen: `tblastn` local de proteínas públicas contra la secuencia da
**72,6 % de identidad de aminoácidos en 809 residuos** con «protein bicaudal C
homolog 1-A» de *Homalodisca vitripennis* (`XP_046672835.1`), 50,8 % con Bicaudal C
de *Drosophila melanogaster* (`NP_476865.1`) y 46-47 % con los ortólogos de
*Acyrthosiphon pisum* y *Nilaparvata lugens*, siempre en el marco +2, que es el marco
en el que nuestro escaneo encuentra 794 codones sin interrupción. La asignación
«Bicaudal Protein» de la planilla es correcta `[E]`.

### 2.4 `ATPaseD_Dm` — subunidad D de la ATPasa vacuolar, y una corrección a la ola 1

Mismo procedimiento. `blastn` local contra el ensamblado de *D. maidis*: tres
bloques en el **cromosoma 8** (`OZ319711.1`), entre 30.146.313 y 30.151.197, en la
hebra menos, con 99,3 a 100 % de identidad. Es un transcrito de tres exones de *D.
maidis* `[E]`. `tblastn`: **99,4 % de identidad de aminoácidos en 163 residuos** con
la subunidad D de la V-ATPasa de *H. vitripennis* (`XP_046663925.1`), 98,2 % con la
de *N. lugens*, 95,1 % con `VATD1_DROME` (Q9V7D2) y 94,5 % con la de *A. mellifera*.
El marco +2 está abierto en 163 codones sin codón de terminación, y el alineamiento
cubre los residuos 37 a 199 de la proteína de referencia: la secuencia es un
**fragmento parcial del CDS**, al que le faltan los primeros 36 codones y que no
incluye el stop.

La corrección: R1 llama a este blanco «subunidades B y D de la ATP sintasa
vacuolar» (sección 4.6, citando `S18`). El nombre correcto del complejo es **ATPasa
vacuolar de protones (V-ATPasa)**, que bombea protones hidrolizando ATP; la ATP
sintasa es el complejo F-ATPasa, que hace lo contrario. Nuestro `tblastn` lo
identifica sin ambigüedad como «V-type proton ATPase subunit D» en seis especies
`[E]`. Conviene unificar el término en el glosario antes de hablar con el
investigador.

### 2.5 De dónde salieron: una pista de procedencia, no una certeza

Descargamos los tres transcriptomas TSA públicos de *D. maidis* (137.065 contigs en
total) y alineamos localmente contra ellos. `ATPaseD_Dm` es **100,000 % idéntica en
sus 491 nt** a las posiciones 190-680 del contig `GCWP01010867.1`, de 1.917 nt, del
ensamblado de Johnson et al. 2018 depositado por el Illinois Natural History Survey.
`BicC_Dm` no tiene equivalente exacto: su mejor coincidencia es `GITV01000968.1`, del
transcriptoma de Xu et al. (Ohio State) que la ola 1 ya había registrado como `S19`,
con **99,72 % en los 2.520 nt (7 desajustes)**, y 98,47 % contra el contig
correspondiente del tercer ensamblado.

La lectura honesta de esto: la identidad perfecta en 491 nt hace muy probable que la
secuencia de la V-ATPasa provenga de ese transcriptoma público, o de una fuente
idéntica a él `[H]`; los siete desajustes de Bicaudal C son compatibles con
diferencias de población o con un ensamblado propio, y no permiten decidir `[?]`.
Que `ATPaseD_Dm` sea un fragmento interno de un contig más largo, recortado en medio
de un codón, refuerza la idea de un recorte manual sobre una secuencia preexistente
`[H]`. Es una pregunta de una línea para el investigador y cambia bastante: si el
insumo es público, podemos reproducir el pipeline completo; si es material propio no
publicado, no.

---

## 3. Caracterización por secuencia

Composición y complejidad. Los dos candidatos virales son **ricos en GC y, sobre
todo, ricos en C**: `MP_MRFV` tiene 519 C contra 177 A en 1.263 nt, y `CP_MRFV` 219 C
contra 78 A en 528. No es un artefacto de la planilla ni de la región elegida: el
genoma de referencia completo que descargamos tiene la misma firma —2.432 C (38,2 %)
contra 987 A (15,5 %) en sus 6.366 nt, 61,7 % de GC— medido por nosotros sobre
`NC_002786.2` `[E]`. Los dos del insecto están en
el rango habitual de un transcrito de insecto (51,9 % y 46,0 % de GC). A escala de
ventana, el contenido GC de las regiones elegidas casi no se aparta del de su gen
completo —61,5 contra 63,1; 65,0 contra 65,9; 49,3 contra 51,9; 47,0 contra 46,0—,
de modo que **la región no se eligió por contenido GC** `[H]`.

`dustmasker` (BLAST+ 2.17.0, local) encuentra **un solo intervalo de baja
complejidad en las ocho secuencias**: las posiciones 354-360 de `BicC_Dm`, que caen
dentro de la región elegida (posiciones 91-97 de esos 300 nt). Siete nucleótidos no
comprometen nada, pero conviene saber que están. Los 21-meros son únicos en todas
las secuencias salvo dos repeticiones en `BicC_Dm` completa (2.498 distintos de
2.500), así que no hay regiones repetitivas internas que generen siRNA redundantes.

Estructura secundaria, con RNAfold 2.7.2 local (`-p --noPS --noDP -T 25`, con las
secuencias convertidas a ARN). Las energías libres mínimas son las esperables para
cadenas de este largo y de este contenido GC; lo informativo es la energía por
nucleótido, que permite comparar entre largos distintos.

| Secuencia | Largo | ΔG MFE | ΔG por nt | ΔG del ensamble | Frecuencia de la MFE |
| --- | --- | --- | --- | --- | --- |
| `MP_MRFV` completa | 1.263 | −509,30 | −0,403 | −529,26 | 2,4 × 10⁻¹⁵ |
| `MP_MRFV` región | 200 | −54,74 | **−0,274** | −59,42 | 3,7 × 10⁻⁴ |
| `CP_MRFV` completa | 528 | −237,35 | −0,450 | −244,16 | 1,0 × 10⁻⁵ |
| `CP_MRFV` región | 200 | −80,18 | −0,401 | −83,44 | 4,1 × 10⁻³ |
| `BicC_Dm` completa | 2.520 | −1.024,44 | −0,407 | −1.061,15 | 1,2 × 10⁻²⁷ |
| `BicC_Dm` región | 300 | −103,69 | −0,346 | −107,97 | 7,3 × 10⁻⁴ |
| `ATPaseD_Dm` completa | 491 | −181,50 | −0,370 | −189,18 | 2,3 × 10⁻⁶ |
| `ATPaseD_Dm` región | 300 | −108,21 | −0,361 | −112,68 | 5,2 × 10⁻⁴ |

Dos observaciones. La primera: **la región elegida de `MP_MRFV` es, con diferencia,
la menos estructurada de las cuatro** (−0,274 kcal/mol por nucleótido, contra −0,346
a −0,401 de las otras tres). Si uno quisiera leer en los datos un criterio de
accesibilidad, este sería el único indicio, y es débil: una sola región de cuatro, y
`CP_MRFV` va en el sentido contrario. La segunda, metodológica y vale para cualquier
cosa que hagamos con estos números: la frecuencia de la estructura de mínima energía
en el ensamble es de 10⁻⁴ a 10⁻²⁷, es decir que **la estructura puntual no significa
casi nada** a estos largos; lo que tiene sentido usar es la energía del ensamble o,
mejor, probabilidades de apareamiento por posición, que es lo que calculamos con
RNAplfold para el tamizaje de la sección 5 `[E]`.

---

## 4. Función e interpretación biológica

Una aclaración de método antes de los cuatro casos: los papers del corpus son el
insumo de W1 y no los abrimos acá. Cuando esta sección se apoya en ellos, cita la
**entrada del manifiesto** (`research/ola2/MANIFEST.md`, sección 1), que sí fue hecha
abriendo cada archivo, y lo marca como `[R]`. Lo que se apoya en la ola 1 cita la
sección de `research/R1_fundamentos/REPORT.md` y conserva su marcador original.

### 4.1 Los dos candidatos virales actúan en la planta, no en el insecto

MRFV es un marafivirus de ARN de cadena simple positiva, transmitido de manera
**persistente propagativa**, es decir que se multiplica también dentro del insecto
`[E]` (R1, sección 3). Eso abre dos lugares posibles de acción para un ARNdc
antiviral, y conviene no mezclarlos. En la **planta**, el ARNdc entregado por
pulverización o por vía sistémica se procesa con la maquinaria de RNAi del maíz y
los siRNA resultantes pueden cortar el ARN viral que se replica en el floema; es el
esquema de los trabajos de ARNdc contra virus de plantas que el corpus incluye —el
de las nanoláminas de arcilla y el del ARNdc producido en bacteria contra SCMV en
maíz `[R]` (manifiesto, P4 y P5). En el **insecto**, el mismo ARNdc tendría que
entrar por alimentación y encontrar al virus replicándose en los tejidos del vector,
una vía mucho menos documentada.

Para MRFV en particular la ola 1 registró que **no existe ningún trabajo publicado
de ARNdc, SIGS o HIGS** `[?]` (R1, sección 4.5). El corpus no lo desmiente: lo que
trae es un trabajo que **convierte a MRFV en vector de silenciamiento** inducido por
virus en maíz `[R]` (manifiesto, P2), que es casi lo inverso —usar el virus como
herramienta en vez de silenciarlo—, aunque demuestra de paso que la maquinaria del
maíz procesa ARN derivado de MRFV. Dicho esto, el blanco elegido tiene sentido
funcional: la proteína de movimiento es la que permite el tránsito del virus entre
células a través de los plasmodesmos, y la cápside es la que lo encapsida y lo hace
transmisible; ambas son indispensables para el ciclo `[E]`. Y el solapamiento de
marcos descrito en 2.1 agrega una ventaja no declarada en la planilla: el ARNdc de
`MP_MRFV` cubre también parte del gen de la replicasa `[H]`.

Hay un punto que no pudimos cerrar y que es importante para priorizar entre los dos
virales: existe literatura reciente sobre cuál de las formas de cápside de MRFV es
necesaria para la transmisión por el cicadélido, pero **no la abrimos** y no la
citamos como evidencia `[?]`. Si esa necesidad es específica de una de las formas,
la región elegida de `CP_MRFV` puede estar cubriéndola o no, y eso cambia el
argumento de priorización. Queda anotado como pregunta abierta.

### 4.2 Los dos candidatos del vector son los dos blancos con antecedente publicado

`BicC_Dm` no es una elección cualquiera: **Bicaudal C es el primer blanco con RNAi
eficiente demostrado en *Dalbulus maidis***, con reducción de transcritos de hasta
170 veces, menos oviposturas y alteraciones del desarrollo de los oocitos, por
inyección y por ingestión en hembras adultas `[E]` (R1, sección 4.6, fuente `S16`).
El mecanismo es la ovogénesis: no mata al insecto, le baja la descendencia. Y el
grupo que lo publicó es el mismo que firma uno de los papers del corpus sobre RNAi
por microinyección en la especie blanco `[R]` (manifiesto, P3), lo cual explica la
elección mejor que cualquier criterio bioinformático: **es el blanco que ese
laboratorio sabe que funciona en sus manos**.

`ATPaseD_Dm` corresponde al otro antecedente: RNAi oral en dieta artificial contra
las subunidades B y D de la V-ATPasa de *D. maidis*, con expresión reducida,
mortalidad significativamente mayor y deformación de alas, reportado en un preprint
no revisado por pares `[R]` (R1, sección 4.6, fuente `S18`). La V-ATPasa es la bomba
de protones que acidifica compartimentos y energiza el epitelio del intestino y los
túbulos de Malpighi; silenciarla es letal y es uno de los blancos canónicos del RNAi
en insectos `[E]`. A diferencia de Bicaudal C, acá el efecto esperado es
**mortalidad**, no reducción de puesta.

La vía de entrada que importa para los dos es la oral, porque el insecto se alimenta
del floema y la aplicación realista es sobre la planta: el corpus trae justamente un
método de laboratorio para entrega de ARNdc **mediada por planta** a cicadélidos de
floema y un trabajo de entrega **oral** en otro hemíptero de floema `[R]`
(manifiesto, P6 y P1). La contracara, también registrada por la ola 1 y declarada
por el organizador, es que las dsRNasas del insecto limitan la entrega oral.

### 4.3 Qué dice el conjunto, leído como decisión

Los cuatro candidatos, vistos juntos, dibujan una estrategia conservadora y
defendible: **dos tiros al virus sobre sus dos proteínas estructurales
indispensables, y dos tiros al vector sobre los dos únicos blancos con antecedente
experimental en la especie**, uno que reduce la puesta y otro que mata. Ninguno
apunta a los mollicutes, donde no hay mecanismo. Ninguno es un blanco exótico. Si
hay una crítica de diseño que hacerle al conjunto —y es nuestra `[H]`—, es que
**ningún candidato ataca la transmisión en sí**: ni la clatrina ni los otros genes
del vector que el patógeno necesita para colonizarlo, que es la vía con evidencia en
el sistema de la flavescencia dorada que R1 describe en la sección 4.6. Es
exactamente el hueco donde una propuesta nuestra puede aportar algo nuevo sin
competir con lo que el laboratorio ya tiene.

---

## 5. Tamizaje de off-targets con herramientas y genomas locales

El tamizaje se corrió sobre las **cuatro regiones elegidas**, que son las que se
transcribirían como ARNdc: se generaron las 920 ventanas de 21 nt posibles (180 para
cada región viral de 200 nt y 280 para cada región del insecto de 300 nt) y se
alinearon con `blastn -task blastn-short` contra seis conjuntos de referencia
descargados del NCBI: el transcriptoma RefSeq de maíz (76.549 secuencias), el
ensamblado cromosómico de *D. maidis*, y los transcriptomas RefSeq de *Homalodisca
vitripennis* (cicadélido no objetivo, 33.294), *Apis mellifera* (polinizador,
27.887), *Harmonia axyridis* (enemigo natural, 28.108) y *Folsomia candida* (fauna
del suelo, 42.425). El criterio de corte es el estándar del campo: **coincidencia
perfecta de al menos 19 nt contiguos**, que es el umbral por debajo del cual un
siRNA deja de ser un buen sustrato de corte; se contaron además las coincidencias de
21/21 y las de 21 nt con un solo desajuste.

| Conjunto | `MP_MRFV` | `CP_MRFV` | `BicC_Dm` | `ATPaseD_Dm` |
| --- | --- | --- | --- | --- |
| *Zea mays* (transcritos) | 3 | 0 | 3 | 0 |
| *Dalbulus maidis* (genoma, **blanco** para los dos últimos) | 3 | 0 | **220** | **222** |
| *Homalodisca vitripennis* | 0 | 0 | **30** | **7** |
| *Apis mellifera* | 0 | 0 | 0 | 0 |
| *Harmonia axyridis* | 0 | 0 | 0 | 0 |
| *Folsomia candida* | 0 | 0 | 0 | 0 |

(Número de siRNA con coincidencia perfecta de ≥19 nt; tabla completa con los tres
criterios en `analisis/offtarget_resumen.tsv`.)

**En el blanco, el pipeline se valida solo.** De los 280 siRNA de `BicC_Dm`, 220
tienen coincidencia perfecta en el cromosoma 3 y 204 son perfectos en los 21 nt; de
los 280 de `ATPaseD_Dm`, 222 y 205 en el cromosoma 8. Los que faltan no son un
problema del diseño sino **una consecuencia de alinear un transcrito contra un
genoma**: la región elegida de `BicC_Dm` se alinea en cuatro bloques exónicos
(posiciones 1-31, 30-99, 98-179 y 179-300 de la región), así que los siRNA que
cruzan una de las tres uniones exón-exón no existen en el ADN genómico; 3 uniones ×
20 ventanas = 60, que es exactamente la diferencia 280 − 220. Para `ATPaseD_Dm` son
dos uniones (40 ventanas) más los dos desajustes puntuales frente al genoma de
referencia, que invalidan unas 17 ventanas cada uno; 58 faltantes observados contra
~57 esperados. Que las cuentas cierren con esa precisión es la mejor evidencia de
que **sabemos correr el pipeline** `[E]`.

**En maíz el resultado es tranquilizador, con una salvedad de criterio.** Las únicas
coincidencias son un bloque de 19 nt exactos de tres siRNA de `BicC_Dm` sobre el gen
`LOC100281777` (serine esterase family protein, en sus tres variantes de transcrito)
y otro bloque de 19 nt de tres siRNA de `MP_MRFV` sobre `XM_008647293.4` (rop
guanine nucleotide exchange factor 10). **Ninguna llega a 21/21.** Con el criterio
más estricto, cero; con el de 19 nt, seis siRNA en todo el conjunto. La salvedad: 19
nt perfectos sí pueden dirigir corte, así que no es cero riesgo, es riesgo bajo y
localizado en dos genes de maíz que convendría nombrar en cualquier evaluación
`[E]` para el dato, `[H]` para la interpretación de riesgo.

**El riesgo real está en los cicadélidos no objetivo.** La región de `BicC_Dm` tiene
30 siRNA con coincidencia perfecta sobre `XM_046816879.1`, el ortólogo de bicaudal C
de *H. vitripennis*, y 22 de ellos son perfectos en los 21 nt; se agrupan en dos
bloques conservados de la secuencia (posiciones 444-465 y 510-517 del gen). La de
`ATPaseD_Dm` tiene 7 sobre `XM_046807969.1`, la subunidad D de la V-ATPasa de esa
especie. *H. vitripennis* no está en la Argentina, así que el dato no es un riesgo
directo: es un **proxy cuantitativo** de lo que pasaría con otros cicadélidos de la
misma familia, y dice que una fracción no trivial de los siRNA —10,7 % en Bicaudal C
y 2,5 % en la V-ATPasa— son compartidos con un pariente a nivel de género distinto
`[H]`. El tamizaje que haría falta es contra cicadélidos nativos no plaga, y para
esos no hay transcriptoma público: es un hueco documentado, no un resultado
negativo.

Vale distinguir homología de riesgo de RNAi, porque es un error frecuente. A nivel
de **región completa**, la de `ATPaseD_Dm` tiene identidad de nucleótidos con los
ortólogos de todas las especies del panel: 84,7 % con *H. vitripennis*, 76,8 % con
*H. axyridis*, 73,4 % con *F. candida*, 72,0 % con *A. mellifera* y 71,7 % en un
tramo de 113 nt con los transcritos de la V-ATPasa D de maíz. Y sin embargo el
tamizaje de 21-meros da **cero** coincidencias perfectas en cuatro de esas cinco
especies. La razón es que el RNAi no se rige por identidad promedio sino por tramos
perfectos: 75 % de identidad distribuida no produce ni un solo 19-mero idéntico
`[E]`. Esto también significa que el margen es delgado y que un gen tan conservado
exige el tamizaje explícito, no una intuición.

### 5.1 El hallazgo no pedido: divergencia entre aislados de MRFV

El tamizaje contra las referencias virales no era un control de off-target sino de
**on-target**, y ahí apareció lo más accionable del informe. Alineando las regiones
virales contra los 71 registros públicos de MRFV y contando, para cada registro,
cuántas de las 180 ventanas de 21 nt mantienen apareamiento perfecto —calculado dos
veces, una reconstruyendo las posiciones de desajuste desde el `btop` del
alineamiento y otra por búsqueda de subcadena exacta, con resultados idénticos—, el
panorama es este: la región de `CP_MRFV` da **180/180 contra las tres entradas del
aislado Costa Rican** y una **mediana de 44/180 contra los demás**, con mínimo de
10/180; contra los 45 registros brasileños la identidad de la ventana cae a 91,5-93,5
% y los conteos van de 18 a 44. La región de `MP_MRFV` sólo tiene con qué
compararse en tres registros, porque casi no hay genomas completos de MRFV: 180/180
en la referencia y **54/180** en el aislado de Estados Unidos.

Y el dato de contexto: **en GenBank no hay una sola secuencia de MRFV de Argentina**
(71 registros, de los cuales 45 de Brasil, 4 de Estados Unidos, 2 de Ecuador, 1 de
Costa Rica y 19 sin país declarado; consulta a E-utilities, 17-oct-2026). Los dos
candidatos virales están diseñados sobre la referencia centroamericana de 2001, y la
población viral más parecida a la argentina para la que hay secuencia es la
brasileña, contra la cual tres cuartas partes de los siRNA dejarían de aparear
perfecto `[H]`. No es un defecto del diseño —no había otra referencia— pero sí es,
muy concretamente, el argumento más fuerte que tenemos para la pregunta «cuáles
merecen validación y por qué».

---

## 6. Cómo los aprovechamos

Las cinco opciones, con lo que requiere cada una, lo que demuestra y su riesgo,
están en `aprovechamiento.md`. Acá va el orden y el porqué.

La primera es usarlas como **conjunto de validación y de calibración**: cuatro
candidatos reales con su región elegida, contra los que correr cualquier scoring que
propongamos, verificando que los ordena de manera coherente con lo que ya se sabe
—que Bicaudal C tiene antecedente oral publicado y la V-ATPasa uno en preprint, que
los virales no tienen antecedente de RNAi y además arrastran el problema de
divergencia entre aislados—. Requiere sólo lo que ya está corrido y es lo que
contesta la pregunta del organizador.

La segunda es la **ingeniería inversa del criterio de eficiencia**, que quedó a
medio camino y hay que cerrarla preguntando. Lo hecho: reimplementamos localmente la
regla de nucleótido terminal, la asimetría termodinámica con parámetros de vecino
más cercano y la accesibilidad local con RNAplfold, que son los tres criterios
documentados de la herramienta cuya terminología coincide con la de la planilla
—si-Fi habla literalmente de «efficient siRNAs»— y obtuvimos 87, 21, 136 y 26 contra
los 114, 35, 199 y 33 declarados; aceptando cualquiera de las dos hebras como guía,
179, 43, 259 y 62. Los declarados caen **entre** las dos variantes, lo que sugiere
que el criterio real es de esta familia pero con una implementación distinta `[H]`.
Barrimos además 2.132 combinaciones de filtros simples (rango de GC × regla terminal
× asimetría × umbral de accesibilidad) y **ninguna reproduce los cuatro números**; la
mejor queda a 6,1 % de error relativo máximo, que con ese tamaño de búsqueda no es
evidencia de nada. Las reglas de Reynolds con umbral de puntaje ≥6 dan cero en las
cuatro secuencias, así que no es eso. Conclusión: **no es identificable con cuatro
números**, y la pregunta al investigador cuesta una línea.

La tercera es el **caso de estudio de criterios de diseño**: qué eligieron y qué no.
Eligieron el gen anotado completo en un caso (`MP_MRFV` es el CDS 332..1594 copiado
tal cual), un recorte interno de un contig en otro, regiones de 200 nt para el virus
y de 300 para el insecto, y posiciones que no se explican por contenido GC ni, salvo
en un caso, por estructura. Reconstruir esa lógica es barato y es material directo
para la conversación técnica.

La cuarta es **el punto de partida para optimizar**, con una restricción ética y una
práctica. La restricción ética: el alcance es control fitosanitario, así que
«optimizar» acá significa reducir riesgo —evitar los dos bloques conservados con
*H. vitripennis*, evitar los dos tramos de 19 nt que tocan transcritos de maíz— y
aumentar cobertura de población viral, no aumentar potencia sobre organismos no
objetivo. La práctica: esta ola no pide diseñar secuencias nuevas y no las
diseñamos; lo que queda listo es el pipeline que evaluaría un rediseño.

La quinta es usarlas como **ejemplos positivos para entrenar o calibrar un modelo**,
y es la que menos recomendamos: cuatro candidatos, sin etiquetas de eficacia
experimental, no alcanzan ni para calibrar un umbral. Como semilla de un conjunto
mayor construido con literatura, sí.

---

## Lo que esto cambia respecto de la ola 1

Tres cosas. **Uno:** los «candidatos preliminares del EPILAB» que la ola 1 dio por no
disponibles y anotó como la primera pregunta abierta
(`00_meta/PREGUNTAS_ABIERTAS.md`) ya están, son cuatro, tienen región elegida y
posición, y ahora sabemos qué son con confianza alta. **Dos:** la predicción de la
ola 1 de que no habría candidatos contra fitoplasma ni espiroplasma, por ausencia de
maquinaria de RNAi en mollicutes, se cumple exactamente: cero de cuatro. Es una
confirmación fuerte del razonamiento mecanicista, y conviene presentarla como tal.
**Tres:** la ola 1 nombró el blanco de `S18` como «subunidades B y D de la ATP
sintasa vacuolar»; el `tblastn` local lo identifica como subunidad D de la **ATPasa
vacuolar de protones (V-ATPasa)**, que es un complejo distinto. Es una corrección de
nomenclatura, no de fondo, pero hay que hacerla antes de la reunión.

No encontramos ninguna contradicción entre el corpus y la literatura pública en lo
que toca a estas secuencias: las identificaciones por alineamiento coinciden con lo
que declara la planilla en los cuatro casos.

## Huecos y preguntas para el investigador

Los huecos, en orden de cuánto nos frenan. **No sabemos con qué herramienta ni con
qué criterio se contaron los siRNA «eficientes»**, y sin eso no podemos auditar ni
extender el tamizaje. **No hay secuencia pública de MRFV de Argentina**, así que la
cobertura real de los dos candidatos virales sobre el virus local es indecidible con
material público. **No hay transcriptoma público de cicadélidos nativos no plaga**,
así que el tamizaje de no objetivo más relevante no se puede correr. **No sabemos si
estas cuatro secuencias ya fueron sintetizadas o ensayadas**, ni si corresponden a
construcciones con regiones flanqueantes. Y **no abrimos la literatura sobre cuál
forma de cápside de MRFV es necesaria para la transmisión**, que afecta la
priorización entre los dos candidatos virales.

Las preguntas, en el orden en que las haríamos: ¿con qué herramienta y qué umbral
salieron los números de la columna «Nro de eficientes por gen»? ¿De dónde salieron
las secuencias del insecto —`ATPaseD_Dm` es 100 % idéntica a un contig del
transcriptoma público `GCWP01010867.1`, ¿es la fuente? ¿Por qué 200 nt para el virus
y 300 para el insecto? ¿Hay secuencia del aislado argentino de MRFV en el
laboratorio, aunque no esté publicada? ¿Y alguna de estas cuatro ya se sintetizó o se
ensayó?

## Dependencias de esta investigación

La ingeniería inversa de la sección 6 depende de lo que W2 determine sobre
dsRNA-Engineer. Al momento de escribir, `research/ola2/W2_herramientas/` tiene las
corridas de ejemplo pero todavía no el REPORT; de sus salidas se desprende que
dsRNA-Engineer informa, por sección de la secuencia, el número de coincidencias en el
blanco y en los no objetivo, y **no un conteo de eficiencia** `[R]`
(`research/ola2/W2_herramientas/ejemplos/salidas/E8_match_result.json`), lo que
inclina la hipótesis hacia si-Fi y en contra de dsRNA-Engineer como origen de la
columna. Cuando el REPORT de W2 esté, conviene releer esa sección.

