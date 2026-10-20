# si-Fi21 desde las fuentes primarias: qué declara «eficiente», con qué umbral y con qué evidencia

Investigación C1 de la ola 3. Fecha de la corrida: 2026-10-20. Lo que sigue se escribió
después de leer, en este orden, `CLAUDE.md`, `tools/sifi21_port/README.md` y `CAMBIOS.md`,
`research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md`, la sección de herramientas de
`research/ola2/W2_herramientas/REPORT.md`, el apartado «Port de si-Fi21» de
`00_meta/PREGUNTAS_ABIERTAS.md` y los tres apartados pedidos de
`research/checkpoints/checkpoint1.md`. **No se repite nada de eso**: el port ya leyó el
código y ya midió los conteos. El aporte de esta investigación es el **artículo**, el
**manual del programa** —que no estaba leído en el repositorio— y la **fuente primaria de
cada umbral**, abierta una por una.

Fuentes abiertas por esta investigación, con el nivel de lectura declarado en `sources.json`:
el artículo de Lück y colaboradores de 2019 en *Frontiers in Plant Science* (texto completo,
12 páginas, PDF de acceso abierto); el `Quick_help.pdf` que viaja dentro del repositorio
oficial, que es el manual y no estaba citado en ningún informe del proyecto (texto completo,
13 páginas); el fuente de GitHub en el commit `d6296b7`, descargado a
`work/C1/siFi21--d6296b7/` (todas las líneas que se citan); y once fuentes primarias de los
umbrales, de las cuales cinco en texto completo y seis sólo en resumen.

---

## P1. Qué umbral exacto marca una ventana como eficiente, y cómo se combinan energía libre, identidad y estructura secundaria

**La respuesta corta, y conviene decirla antes de la tabla: «eficiente» en si-Fi21 es una
conjunción de tres condiciones booleanas sobre cada ventana de 21 nt, más una cuarta regla
sobre dos nucleótidos, y ninguno de los dos umbrales numéricos que aparecen en ella —1 kcal/mol
y 0,1— tiene fuente primaria que lo fije.** `[E]` El artículo los enuncia como valores de la
herramienta, sin citar de dónde salen: la única formulación compacta de la regla está en la
Discusión, página 8, y dice que aplicar las reglas de selección de hebra (U o A en el extremo
5'; MFE del extremo 5' mayor que el del extremo 5' de la hebra opuesta; ΔMFE de los primeros
tres nucleótidos de cada hebra > 1 kcal/mol) identifica los siRNA que se incorporarán al RISC
con alta probabilidad, y que el cálculo de accesibilidad local (u = 8, umbral 0,1) identifica
los que apuntan a partes accesibles del ARN blanco. No hay en el artículo ni una ecuación
numerada, ni un ajuste, ni una curva ROC: el criterio se presenta enunciado.

Sobre **«identidad»**, que es lo que el investigador mencionó como tercer término del criterio:
**no existe ningún filtro de identidad dentro de la regla de eficiencia**, y por eso el port no
tiene uno con ese nombre. `[E]` La identidad entra en si-Fi21 por dos vías que no son el cálculo
de eficiencia. La primera es operativa: cada ventana de 21 nt se busca con BOWTIE contra la base
de datos elegida, con un presupuesto fijo de desajustes que por defecto es cero (manual, página 7;
`main.py:335` y `main.py:358`), de modo que «identidad» quiere decir coincidencia exacta del
21-mero, y nada más fino. La segunda es experimental y es del propio artículo: la serie del
«reloj molecular» mide qué pasa cuando la identidad global entre el disparador y el blanco baja,
y encuentra que la eficacia del silenciamiento cae rápido por debajo del 92 % de similitud
(Discusión, página 8, construcción 4MY de la Figura 3), mientras que los hits de 21-meros caen a
cero a partir de la construcción 10MY, con 89,4 % de identidad observada (Tabla 1). Esa es la
única cifra de identidad que el artículo respalda con experimento, y es una propiedad del par
secuencia-blanco, no un filtro por ventana.

Y un detalle de arquitectura que vale más que cualquier umbral: **las tres condiciones no se
combinan con pesos, se combinan con un `and`, y después una regla de secuencia decide por
ramificación.** `[E]` El código compone primero el veredicto termodinámico
(`work/C1/siFi21--d6296b7/sifi_pipeline.py:459-505`, función `check_efficient`, que es un árbol
de siete ramas según qué casillas haya tildado el usuario) y recién después aplica la regla de
los nucleótidos terminales (`sifi_pipeline.py:525-555`). Esa segunda regla no multiplica ni suma:
elige qué mirar. Es el defecto que el port ya midió y no se repite acá.

### La tabla: una fila por filtro

| Filtro | Qué mide | Umbral por defecto (modo diseño) | Fuente primaria del umbral, abierta por nosotros | ¿Empírica o convención? | Qué dice el paper | Qué hace el código | ¿Coinciden? |
|---|---|---|---|---|---|---|---|
| **Tamaño de ventana** | Largo del siRNA que se simula | 21 nt | Elbashir, Lendeckel y Tuschl 2001, *Genes Dev* 15:188-200 (texto completo): los fragmentos de 21 y 22 nt son los mediadores de la interferencia en lisado de embrión de *Drosophila melanogaster* | **Empírica** (in vitro, lisado de *Drosophila*) | Introducción, página 1: los siRNA «suelen» medir 21 nt, citando Zamore 2000 y Elbashir 2001; el nombre si-Fi21 viene de ahí | `main.py:334` y `main.py:357` fijan 21; las ventanas se generan corriendo de a 1 nt (`sifi_pipeline.py:282-305`) | **Sí** |
| **Desajustes permitidos** | Identidad exacta del 21-mero contra la base | 0 | Langmead y colaboradores 2009, *Genome Biol* 10:R25 (texto completo): es la herramienta de alineamiento, no una medición de eficacia | **Convención** | Implementación, página 3: BOWTIE se eligió por exactitud, velocidad y uso de memoria | `comboBox_miss` en 0 (`main.py:335`, `main.py:358`); `bowtie -a -v N -y` (`sifi_pipeline.py:332`). Si se permite ≥ 1 desajuste, la eficiencia se apaga entera (`main.py:114-118` → `sifi_pipeline.py:513-514`: todo siRNA queda `False`) | **Sí**, y el manual explica el apagado: no hay datos confiables (páginas 7 y 11) |
| **Selección de hebra guía** | ΔG de los 3 pares del extremo 5' antisentido contra los 3 del extremo 5' sentido | ΔG(5' antisentido) ≥ ΔG(5' sentido); sin margen | Schwarz y colaboradores 2003, *Cell* 115:199-208 (sólo resumen) y Khvorova, Reynolds y Jayasena 2003, *Cell* 115:209-216 (sólo resumen): la estabilidad absoluta y relativa de los pares de los extremos 5' determina qué hebra entra al RISC | **Empírica** para la dirección del efecto; el umbral es la desigualdad sin margen, o sea sin umbral | Asimetría y selección de hebra, página 4, y Figura 1: la guía es la hebra con estabilidad significativamente menor en su nucleótido 5' terminal | `sifi_pipeline.py:423-426`: `anti >= sense`. Tres nucleótidos por `end_nucleotides = 3` (`sifi_pipeline.py:65`), con extremos colgantes del dúplex desplazado dos posiciones (`sifi_pipeline.py:388-411`) | **Sí** |
| **Estabilidad de extremos** | La misma diferencia, pero exigiendo una brecha mínima | **1,00 kcal/mol** | **Ninguna.** Khvorova 2003 (resumen) reporta que los dúplex funcionales tienen **0,5 kcal/mol** menos de estabilidad interna en el extremo 5' antisentido que los no funcionales: el umbral de si-Fi es el doble de esa diferencia medida y no se deriva de ella | **Convención** | Discusión, página 8: enuncia «ΔMFE de los primeros tres nucleótidos de cada hebra > 1 kcal/mol» sin citar fuente para el valor. El manual lo presenta como campo editable con default 1,00 (página 7) | `sifi_pipeline.py:442`: `(anti - sense) >= self.end_stability_treshold`, con el valor puesto en `main.py:359` | **Sí** en el valor; el paper escribe `>` y el código aplica `>=` |
| **Regla del nucleótido terminal 5'** | Preferencia de U/A en el 5' de la guía y de G/C en el 5' de la pasajera | Casilla tildada, sin número | Ui-Tei y colaboradores 2004, *Nucleic Acids Research* 32:936-948 (texto completo): 62 blancos de seis genes en células de mamífero, *Drosophila* y embrión de pollo; las cuatro condiciones incluyen A/U en el 5' de la antisentido y G/C en el 5' de la sentido. Reynolds y colaboradores 2004, *Nat Biotechnol* 22:326-330 (sólo resumen): 180 siRNA sobre dos genes, con preferencias de base en las posiciones 3, 10, 13 y 19 de la hebra sentido | **Empírica** (células de mamífero; en *Drosophila* in vivo los mismos autores no detectaron preferencia de secuencia) | Página 4: U o A como nucleótido 5' terminal predetermina esa hebra como guía, «especialmente si se combina» con G o C en el 5' de la opuesta. Página 4 y página 6: las reglas de secuencia son una **combinación** con las termodinámicas, no un reemplazo | `sifi_pipeline.py:525-555`. Dos apartamientos: (a) no es un filtro sino una ramificación, y la rama de `sifi_pipeline.py:534-541` devuelve «eficiente» mirando **sólo** accesibilidad; (b) comprueba `sirna_sequence[1]`, la **posición 2** del 21-mero (líneas 528 y 543), donde la regla habla del nucleótido 5' terminal de la hebra opuesta, que en la geometría del propio si-Fi es la **posición 1** —la que su cálculo de ΔG trata como extremo 5' del sentido en `sifi_pipeline.py:377`, índices 0 a 2 | **No** |
| **Accesibilidad del sitio blanco** | Probabilidad de que un tramo de 8 nt del ARNm esté desapareado | **≥ 0,1**, con u = 8, L = 40, W = 80 | Tafer y colaboradores 2008, *Nat Biotechnol* 26:578-583 (sólo resumen): calibran sobre 573 siRNA de 38 genes y prueban sobre 360 siRNA de 4 genes; Bernhart y colaboradores 2006, *Bioinformatics* 22:614-615 (sólo resumen): RNAplfold y las probabilidades locales de apareamiento; Ameres, Martinez y Schroeder 2007, *Cell* 130:101-112 (sólo resumen): la accesibilidad del sitio correlaciona directamente con la eficiencia de corte, in vitro e in vivo. **Ninguna de las tres fija 0,1** | **Empírica** para el principio y para u = 8 como escala de la semilla; **convención** para el valor 0,1 | Pie de la Figura 2A: «umbral LAP por defecto de si-Fi de 0,1», con u = 8, L = 40, W = 80, y la aclaración —importante— de que un LAP alto es condición **necesaria pero no suficiente** y que la altura del pico probablemente no es decisiva mientras supere el umbral | `sifi_pipeline.py:60-61` fija W = 80 y L = 40; la llamada es `RNAplfold -W 80 -L 40 -u 21 -T 22` (`sifi_pipeline.py:351`) y del `_lunp` se lee la columna 8 (`sifi_pipeline.py:252`), así que el u del veredicto es 8; el umbral se aplica en `sifi_pipeline.py:454` con `>=` | **Sí** |
| **Temperatura** | Temperatura de todo el cálculo | 22 °C | **Ninguna.** El artículo no menciona temperatura en ninguna de sus 12 páginas | **Convención no documentada** | Nada | `free_energy.py:420`: `tao = 273.15 + 22`, que entra en `deltaG = (ΔH·1000 − tao·ΔS)/1000` (línea 421); y `sifi_pipeline.py:62` manda `-T 22` a RNAplfold | **No se puede comparar**: el paper calla |
| **Tablas de energía** | Parámetros de vecinos más cercanos y de extremos colgantes | `RNA_NN3` y `RNA_DE2` por defecto | Chen y colaboradores 2012, *Biochemistry* 51:3508-3522 (texto completo): fusión óptica de 29 dúplex de ARN con pares G·U en 1 M NaCl, parámetros reportados como ΔG°37. Turner y Mathews 2010, *Nucleic Acids Res* 38:D280-D282 (texto completo): la NNDB publica los juegos de parámetros y las ecuaciones para extrapolar a temperaturas distintas de 37 °C | **Empírica**, pero medida en 1 M NaCl sobre oligos cortos | El artículo no nombra ninguna tabla termodinámica | `free_energy.py:278-281`: `nn_table=RNA_NN3`, `de_table=RNA_DE2`, y `tmm_table=DNA_TMM1`, `imm_table=DNA_IMM1` —las dos últimas, de ADN, dentro de un cálculo de ARN | **No se puede comparar**: el paper calla |
| **«Identidad»** | No es un filtro | — | Lück y colaboradores 2019 (texto completo), Tabla 1 y Discusión página 8 | **Empírica**, con una especie y un gen | La eficacia cae por debajo del 92 % de similitud global; los hits caen a cero con 89,4 % de identidad observada | La identidad se resuelve por fuera, en BOWTIE, como coincidencia exacta con N desajustes | **No aplica**: no hay filtro que comparar |

Dos consecuencias de la tabla que conviene tener a mano para la reunión. La primera: de los seis
filtros que deciden el veredicto, **dos tienen fuente primaria empírica abierta y específica**
—el tamaño de 21 nt y la regla del nucleótido terminal—, **dos tienen fuente para el principio
pero no para el número** —asimetría y accesibilidad— y **dos no tienen ninguna fuente**
—el 1 kcal/mol y los 22 °C—. La segunda: el único filtro donde paper y código **no** coinciden
es justamente el que el port ya había señalado, y ahora hay además un segundo apartamiento en la
misma regla, el de la posición 2 contra la posición 1.

**Cuánto pesa ese segundo apartamiento, medido.** `[E]` Sobre el genoma público del virus del
rayado fino del maíz (`NC_002786.2`, 6.366 nt, copia local en `work/W2/MRFV_NC_002786.2.fa`,
6.346 ventanas de 21 nt), cambiar el índice de la posición 2 a la posición 1 cambia **la rama
que decide en el 51,4 % de las ventanas** (3.265 de 6.346) y cambia el booleano de preferencia
terminal de la formulación corregida en el **31,4 %** (1.994 de 6.346). Eso acota la
sensibilidad de la regla al índice, no el cambio final de veredicto: cuántas ventanas pasarían de
eficiente a no eficiente depende además de los términos termodinámico y de accesibilidad, y esa
medición **no se hizo** acá (requiere correr el port con ViennaRNA, que es trabajo del módulo de
eficiencia y no de esta investigación).

---

## P2. Qué validó experimentalmente el paper, y qué sostiene realmente la regla

El desarrollo completo está en `validacion_paper.md`. El resumen que hay que poder decir en voz
alta es este. `[E]`

El artículo valida **la herramienta entera, en un patosistema de planta y hongo, con doce
construcciones**, y no valida **ningún umbral por separado**. El sistema es cebada (*Hordeum
vulgare* ssp. *vulgare*) transformada transitoriamente por bombardeo de partículas en epidermis
de hoja separada, inoculada con *Blumeria graminis* f. sp. *hordei* (aislado suizo de campo CH4.8,
150 a 200 conidios por milímetro cuadrado), con el gen *HvMlo* como blanco. La medida de eficacia
**no es la caída del ARN mensajero**: el propio artículo dice, en la Discusión de la página 8, que
medir directamente el descenso del transcrito no es viable en ese sistema, así que usa el fenotipo
—el índice de susceptibilidad relativa, normalizado contra vector vacío y transformado a log2— como
sustituto. Cada construcción se probó en un mínimo de cinco repeticiones biológicas independientes,
con ANOVA de una vía y corrección de Dunnett.

El resultado central, el que el equipo necesita citar: la correlación de Pearson entre la cantidad
de siRNA predichos y el efecto medio de silenciamiento, sobre las doce construcciones de la Tabla 2,
es **−0,61 en modo de alta eficiencia (HE, el de diseño)**, contra −0,37 en modo de alta
sensibilidad, −0,31 para el total de hits y −0,31 y −0,34 para la versión anterior de si-Fi. Esa
es toda la evidencia cuantitativa que sostiene «si-Fi predice un siRNA potente», y conviene leerla
con sus tres límites: **n = 12**, la unidad es la **construcción** y no el siRNA —ningún siRNA
individual fue medido— y la variable dependiente es un fenotipo de resistencia, no un nivel de
transcrito.

La distinción que pidió el prompt, dicha con precisión: **«si-Fi predice un siRNA potente» y
«si-Fi evita off-targets» tienen evidencias distintas y de calidad distinta.** `[E]` La primera se
apoya en esa correlación de −0,61 a nivel de construcción, en una sola especie vegetal, con un
fenotipo como sustituto. La segunda se apoya en un reanálisis de datos ajenos: Xu y colaboradores
2006 habían medido transcritos de *AtBTI1* y de sus parálogos en *Arabidopsis thaliana*, y si-Fi21
en modo HS predijo como off-target a los cuatro genes con reducción confirmada y dio cero hits al
único que no se había afectado (Tabla 3, cinco secuencias). Es una correspondencia de 5 sobre 5,
pero con n = 5 y en un organismo distinto del de la validación propia.

Y lo que el artículo **no** prueba, que es la mitad del valor de esta respuesta: no prueba que
1 kcal/mol sea mejor que 0,5 o que 2; no prueba que 0,1 sea mejor que 0,05; no prueba que u = 8
sea mejor que u = 4 o 16; no prueba que la regla terminal aporte sobre la termodinámica ni al
revés; y **no hay un solo insecto en toda la validación**. La comparación con otras herramientas
—siDirect, dsCheck y RNAi Designer, en la Tabla Suplementaria S1— tampoco cierra el punto: el
propio artículo aclara que ninguna de esas herramientas admite una base de cebada, así que no
pudo compararlas contra el experimento y las comparó por cantidad de siRNA recomendados.

---

## P3. De dónde sale que la región útil mide entre 150 y 250 nt, y la frase «con largos no funciona»

**No está en el paper, no está en el manual y no está en el código. Es un vacío declarado y una
pregunta para el investigador.** `[E]` para las tres ausencias, que se verificaron una por una.

En el artículo no hay ninguna recomendación de largo de región. Lo que hay es lo contrario a una
regla de regiones cortas: las construcciones del reloj molecular son de **500 pb** (Materiales y
Métodos, página 2: ADN sintético de 500 pb, nucleótidos 1.275 a 1.774 de la región codificante) y
el experimento de accesibilidad usa **ventanas de 100 pb rellenadas hasta 500 pb** con secuencia
aleatoria (página 5 y Figura 2B). Las únicas apariciones de «150» y «250» en las doce páginas son
la densidad de conidios del bioensayo y un número de página de la bibliografía.

En el manual tampoco. El `Quick_help.pdf` describe el modo diseño y cómo leer el gráfico, y su
criterio de región es cualitativo: una región ideal para diseñar contiene sólo área verde —sin
off-targets— y la mayor cantidad posible de área cubierta por la línea roja, que es la de los
siRNA eficientes (página 9). No da un largo, ni mínimo ni máximo.

En el código, menos todavía: **si-Fi21 no busca regiones.** `[E]` La única huella de esa idea es
un parámetro llamado `region_plot_lst`, documentado en el propio fuente como «Plot for suggested
RNAi design region» (`work/C1/siFi21--d6296b7/show_plot.py:27` y `:41`;
`work/C1/siFi21--d6296b7/create_plots.py:13` y `:23`), que se guarda en el objeto y **no se usa
en ninguna otra línea del programa**: es una función que quedó sin implementar. La búsqueda de la
ventana de 200 nt con mayor densidad de eficientes que tiene nuestro port es un agregado nuestro,
no una reimplementación de algo que si-Fi haga.

Lo que sí se puede decir con fuente abierta es que la práctica publicada con esta misma
herramienta va en la dirección opuesta al «con largos no funciona». `[E]` En el único estudio en
insecto que abrimos y que usa si-Fi21 para diseñar —*Aedes albopictus*, *Parasites & Vectors* 2025,
PMC12619383—, las regiones que si-Fi21 identifica se convierten en construcciones de **400 y 500 pb**,
diseñadas con Primer-BLAST. Y el propio artículo de si-Fi valida con 500 pb. Eso no refuta el
criterio del laboratorio, que puede venir de su experiencia de entrega oral en insecto —un terreno
donde el largo del ARN de doble cadena interactúa con nucleasas intestinales y con la captación, y
que esta investigación no abrió—, pero sí deja establecido que **el criterio no proviene de
si-Fi21 ni de su artículo**. Queda como pregunta: de qué ensayo, de qué especie y con qué medida
salió el rango de 150 a 250 nt. `[?]`

---

## 1. Ficha: autores, versión, licencia y qué cambia entre versiones

El artículo es Lück S, Kreszies T, Strickert M, Schweizer P, Kuhlmann M y Douchkov D,
«siRNA-Finder (si-Fi) Software for RNAi-Target Design and Off-Target Prediction»,
*Frontiers in Plant Science* 10:1023, recibido el 14 de febrero de 2019, aceptado el 22 de julio
y publicado el 15 de agosto de 2019, DOI `10.3389/fpls.2019.01023`. `[E]` Es un artículo de la
sección Bioinformática y Biología Computacional, con el rótulo de tipo «METHODS» en la primera
página. Patrick Schweizer figura *in memoriam*. El financiamiento es del propio IPK de
Gatersleben. En Europe PMC la entrada es PMID 31475020, PMCID PMC6704232, acceso abierto, y
registra **128 citas** al día de esta consulta.

**Las versiones son cuatro cosas distintas y conviene no mezclarlas.** `[E]`

La primera es **si-Fi «a secas»**, la versión previa a 2019, que el artículo reconoce como ya
usada en la comunidad antes de publicarse, citando cuatro trabajos (Nowara y colaboradores 2010;
Lee 2015; Chen 2016; Wang 2018) en la sección de comparación con versiones previas, página 6.
Esa versión definía los siRNA eficientes **sólo con reglas de secuencia**.

La segunda es **si-Fi21**, la del artículo, y el artículo dice exactamente qué cambió, en tres
puntos (página 6): las reglas de secuencia se reemplazaron por una combinación de cálculo
termodinámico y reglas de secuencia; se agregó el cálculo de accesibilidad local del sitio
blanco; y se partió el criterio en dos juegos de reglas, uno para diseño (HE, alta eficiencia) y
otro para búsqueda de off-targets (HS, alta sensibilidad). El cambio de nombre a «si-Fi21» es
explícito y su motivo es distinguirla de todas las anteriores. La versión concreta es
**siFi21_1.2.3-0008**, según la portada del manual, el título de la ventana
(`work/C1/siFi21--d6296b7/main.py:25`) y el README del repositorio.

La tercera es el **código de GitHub**, `github.com/snowformatics/siFi21-`, que el propio artículo
declara como página del proyecto en la sección «Availability and Requirements» (página 9). El
commit que descargamos es `d6296b7`, del 18 de marzo de 2025, y es la cabeza de `master`: los tres
commits más recientes del repositorio son de ese mismo día y los dos anteriores son la carga del
manual y una edición del README. Es decir que **el repositorio no tuvo cambios de código después
de marzo de 2025**, y su propio README avisa que la herramienta no está actualizada y que
necesitaría una reescritura completa para los estándares actuales de Python.

La cuarta es el **binario de SourceForge**, enlazado desde el README como
`sifi1.2.3-0008.exe`. El artículo, en cambio, apunta a dos depósitos distintos para los artefactos
que usó: el instalador de Windows en e!DAL con DOI `10.5447/ipk/2017/9` (referencia «Lück et al.
2017a») y el código fuente en Zenodo con DOI `10.5281/zenodo.845056` (referencia «Lück et al.
2017b»). **Ninguno de los tres se pudo abrir desde este entorno**: `sourceforge.net`, `zenodo.org`
y `doi.ipk-gatersleben.de` están fuera de la lista de dominios permitidos y la conexión se corta
en el proxy. No se usaron espejos. `[?]`

**Manual.** Existe y está dentro del repositorio: `Quick_help.pdf`, 13 páginas, firmado por
Stefanie Lück y Dimitar Douchkov, IPK-Gatersleben 2017. Es la fuente más explícita sobre los
valores por defecto de cada modo, y no estaba citado en ningún informe previo del proyecto. Su
página 7 lista los defaults del modo diseño y su página 11 los del modo off-target; su página 3
explica la regla del nucleótido terminal con sus referencias; su página 4 explica la accesibilidad
con las suyas; su página 9 explica cómo leer el gráfico.

**El conflicto de licencia: queda documentado, y es de tres puntas, no de dos.** `[?]` El artículo
declara, en «Availability and Requirements» (página 9), licencia *Creative Commons
Attribution-ShareAlike 4.0 International* (CC BY-SA 4.0), y el resumen repite «open-source (CC BY-SA
license)». El README del repositorio oficial declara, en cambio, *Attribution-NonCommercial-ShareAlike
2.0 Generic* (CC BY-NC-SA 2.0). Y la última página del manual declara *Attribution-NonCommercial-ShareAlike*
(CC BY-NC-SA), sin versión. Las tres las abrimos nosotros. A eso se suma que el artículo en sí
—el texto, no el software— está bajo CC BY, según su propia leyenda de copyright y según el campo
de licencia de Europe PMC. La diferencia que importa es la cláusula **NC**: una licencia con
NonCommercial es incompatible con CC BY-SA 4.0, así que el software tiene dos declaraciones que no
pueden ser ciertas a la vez. La nota previa del repositorio, que atribuía a SourceForge una
*CC BY-NC 2.0*, **no se pudo verificar** porque el dominio está bloqueado; lo que sí se verificó es
que el README de GitHub dice CC BY-NC-SA 2.0, que no es exactamente lo mismo. Para uso académico
interno no cambia nada; para cualquier cosa que se publique o se distribuya, hay que preguntarle a
los autores cuál rige, y esa pregunta no la hacemos nosotros (está fuera de alcance contactar a
nadie).

Un dato más de la ficha, verificado de primera mano y útil para la reproducibilidad: el
repositorio **trae los binarios de sus dependencias** en `ToCopy/`, y el `RNAplfold.exe` que
distribuye declara en sus cadenas internas la versión **2.1.5** de ViennaRNA, junto con el
`bowtie.exe` y `bowtie-build.exe`. `[E]` Eso confirma por medición propia la versión de ViennaRNA
que el port del repositorio venía declarando.

## 2. El método paso a paso, según el artículo y el manual

El artículo describe el flujo en la sección «Implementation» (páginas 3 y 4), lo resume en la
Figura 5 y lo ilustra con capturas en la Figura 6; el manual lo dibuja en su página 2. `[E]`

**Entrada.** En modo diseño, la secuencia del ARN mensajero que se quiere silenciar, lo más
completa posible, en FASTA, pegada o cargada desde archivo (manual, página 7). En modo
off-target, la secuencia del disparador de ARNi que ya existe (manual, página 11). Además, y es
obligatorio, una base de datos de nucleótidos construida desde un multi-FASTA, idealmente el
transcriptoma completo del organismo (manual, página 6).

**Ventana.** La secuencia de consulta se parte en todos los x-meros posibles, con x el largo de
siRNA elegido —21 por defecto— (Implementación, página 3). En el código eso es un corrimiento de a
un nucleótido (`sifi_pipeline.py:282-305`), de modo que una secuencia de n nucleótidos produce
n − 20 ventanas.

**Búsqueda de blancos.** Los x-meros se buscan con BOWTIE contra la base. El artículo justifica la
elección por exactitud, velocidad y eficiencia de memoria (página 3). En modo diseño, el usuario
elige después cuáles de las secuencias con hit son el blanco principal, y **todo lo no
seleccionado pasa a ser off-target** (manual, página 8). En el código esa elección es un diálogo
modal (`sifi_pipeline.py:268`), que es lo que vuelve no automatizable al programa.

**Filtros de eficiencia.** Para cada ventana se calculan las tres condiciones de la tabla de P1 y
se combinan según qué casillas estén tildadas (`sifi_pipeline.py:459-505`), y después se aplica la
regla de los nucleótidos terminales (`sifi_pipeline.py:525-555`). La accesibilidad se obtiene de una
única corrida de RNAplfold sobre la secuencia de consulta entera (`sifi_pipeline.py:343-363`), de la
que se descartan las primeras 20 filas por incompletas (línea 360).

**Tamizaje de off-targets.** No es un paso aparte: es la misma corrida de BOWTIE. Lo que cambia
entre los dos modos es **qué parámetros de eficiencia se aplican a los hits**. El manual lo dice
sin rodeos: en modo diseño se calcula la eficiencia de cada hit con «parámetros de alta
eficiencia» y en modo off-target con «parámetros de alta sensibilidad» (página 2). Los defaults
del modo off-target son las tres casillas termodinámicas apagadas salvo selección de hebra, y los
umbrales desactivados (manual, página 11; `main.py:336-339`), que es exactamente lo que el artículo
llama modo HS en la página 8.

**Salida.** Un gráfico y una tabla. El gráfico —el «RNAi design plot» que el investigador mostró
en el checkpoint— lleva en el eje x la posición del nucleótido en el ARNm y en el eje y **cuántos
siRNA se superponen a esa posición**: la línea azul es el total de siRNA con hit en el blanco
principal y la roja es cuántos de ellos pasan el criterio de eficiencia; el área verde marca los
tramos cuyos siRNA sólo pegan en el blanco elegido y el área roja los tramos que además pegan en
otra cosa (manual, página 9; artículo, Figura 6). La tabla resume, por cada secuencia de la base
con hit, el total de hits y cuántos son eficientes (manual, página 12). Es importante para
interpretar los conteos: lo que se cuenta son **hits**, no siRNA únicos.

## 3. Las fuentes primarias, una por una, y qué evidencia aportan

La tabla de P1 tiene la asignación filtro por filtro; acá va lo que cada fuente aporta como
evidencia empírica, con organismo, n y medida, que es lo que permite decidir cuánto pesa.

**Elbashir, Lendeckel y Tuschl 2001** (*Genes Dev*, texto completo) `[E]`: en un sistema in vitro
de *Drosophila melanogaster* muestran que los fragmentos de 21 y 22 nt son los mediadores
específicos de la interferencia, que se generan desde ARN de doble cadena largo por una reacción
tipo RNasa III, y que dúplex sintéticos con extremos 3' salientes cortan el ARN blanco cerca del
centro de la región apareada. Es la base física del «21»: no es un parámetro ajustable sino el
producto de la enzima.

**Ui-Tei y colaboradores 2004** (*NAR*, texto completo) `[E]`: 62 blancos de cuatro genes exógenos
y dos endógenos, en tres líneas de mamífero y en *Drosophila*, con cuatro condiciones de secuencia
que, cumplidas a la vez, dan silenciamiento altamente efectivo: A/U en el extremo 5' de la
antisentido; G/C en el extremo 5' de la sentido; al menos cinco residuos A/U en el tercio 5'
terminal de la antisentido; y ausencia de tramos G/C de más de 9 nt. Las dos primeras son las que
si-Fi implementa; **las dos últimas no están en si-Fi**. Y hay un matiz que importa para nuestro
caso: los mismos autores reportan que en *Drosophila* in vivo **casi no se detecta preferencia de
secuencia**, es decir que la regla tiene soporte en células de mamífero y soporte débil en un
insecto.

**Reynolds y colaboradores 2004** (*Nat Biotechnol*, sólo resumen) `[E]` del resumen: análisis
sistemático de 180 siRNA contra dos genes, del que salen ocho características asociadas a
funcionalidad, entre ellas bajo contenido G/C, baja estabilidad interna en el extremo 3' de la
hebra sentido y preferencias de base en las posiciones 3, 10, 13 y 19. La posición 19 es la que
si-Fi comprueba.

**Schwarz y colaboradores 2003** y **Khvorova, Reynolds y Jayasena 2003** (*Cell*, sólo resumen)
`[E]` del resumen: las dos hebras del dúplex no son igualmente elegibles, y la estabilidad
absoluta y relativa de los pares de los extremos 5' determina el grado de participación de cada
hebra; los dúplex funcionales muestran 0,5 kcal/mol menos de estabilidad interna en el extremo 5'
antisentido que los no funcionales. Esa cifra es la que hace que el 1 kcal/mol de si-Fi sea una
convención: es el doble de la diferencia media medida, y ninguna de las dos fuentes propone un
corte.

**Ameres, Martinez y Schroeder 2007** (*Cell*, sólo resumen) `[E]` del resumen: la accesibilidad
del sitio blanco correlaciona directamente con la eficiencia de corte, in vitro e in vivo, y el
RISC no es capaz de desplegar ARN estructurado. Es la justificación mecanística del filtro de
accesibilidad.

**Tafer y colaboradores 2008** (*Nat Biotechnol*, sólo resumen) `[E]` del resumen: calibran su
método sobre dos conjuntos con 573 siRNA de 38 genes y lo prueban sobre 360 siRNA de 4 genes,
combinando criterios conocidos de funcionalidad con accesibilidad del sitio blanco, y construyen
RNAxs. Es el antecedente directo del módulo de accesibilidad de si-Fi, y el artículo de si-Fi lo
cita como tal («un algoritmo desarrollado por Tafer y colaboradores»). Vale anotar un defecto
editorial del artículo de si-Fi: **su entrada bibliográfica de Tafer 2008 está fusionada con otra
referencia** —mezcla el título del trabajo de accesibilidad con el de RNAplex y los datos de
volumen y páginas de ambos—, lo que obliga a reconstruir la cita desde el DOI. `[?]`

**Bernhart y colaboradores 2006** (*Bioinformatics*, sólo resumen) `[E]` del resumen: método para
calcular probabilidades locales de pares de bases en secuencias largas de forma robusta frente a
la ventana elegida; el programa es RNAplfold. No propone umbrales de diseño de siRNA: es la pieza
de cálculo.

**Chen y colaboradores 2012** (*Biochemistry*, texto completo) y **Turner y Mathews 2010**
(*NAR*, texto completo) `[E]`: los parámetros de vecinos más cercanos que el código usa por
defecto vienen de fusión óptica de dúplex cortos en 1 M NaCl y se reportan como ΔG°37; la NNDB
publica además las ecuaciones para extrapolar a otras temperaturas. Son fuentes empíricas sólidas
**para lo que miden**, que es la estabilidad de un dúplex corto en una sal concreta, y no para la
eficacia de un siRNA.

**Langmead y colaboradores 2009** (*Genome Biol*, texto completo) `[E]`: BOWTIE, el alineador. Su
aporte al criterio no es un umbral biológico sino la definición operativa de «coincide»: ventana
completa con un presupuesto fijo de desajustes.

## 4. Qué es la energía libre en este contexto, para alguien que viene de IA

`[E]` salvo donde se indique.

**Qué se calcula.** No es la energía de plegado del siRNA entero, ni la energía de unión entre el
siRNA y su blanco. Es la **energía libre de hibridación de tres pares de bases**: los tres del
extremo 5' de la hebra sentido, por un lado, y los tres del extremo 5' de la hebra antisentido, por
el otro, cada uno con la corrección por el extremo colgante de la hebra opuesta
(`sifi_pipeline.py:365-411`, con `end_nucleotides = 3` en la línea 65). Se obtiene sumando
incrementos tabulados de entalpía y entropía por cada par de vecinos —el modelo de vecinos más
cercanos— y combinándolos con ΔG = ΔH − T·ΔS (`free_energy.py:421`).

**Entre qué moléculas.** Entre **las dos hebras del propio siRNA**. En el modelo de si-Fi, la
hebra sentido es el 21-mero de la ventana y la antisentido es el complemento inverso del 21-mero
que empieza dos posiciones antes, que es como se representa el dúplex con extremos 3' salientes de
2 nt (`sifi_pipeline.py:223-235`). La interacción con el ARN mensajero **no entra como energía**:
entra como el término de accesibilidad, que se calcula sobre el ARNm solo, sin el siRNA, con
RNAplfold.

**A qué temperatura.** A 22 °C, fijos en el código en dos lugares independientes
(`free_energy.py:420` para el ΔG y `sifi_pipeline.py:62` para el `-T` de RNAplfold). El artículo no
menciona ninguna temperatura. Y la temperatura no se cancela en la comparación, porque el veredicto
depende de ΔΔG = ΔΔH − T·ΔΔS y ΔΔS no es cero.

**Por qué una diferencia y no un valor absoluto.** Porque lo que la biología sugiere que importa
no es cuán estable es el dúplex sino **cuál de sus dos extremos es más fácil de abrir**: el
complejo se queda con la hebra cuyo extremo 5' es menos estable (Schwarz 2003, Khvorova 2003). Por
eso si-Fi nunca usa un ΔG solo: compara ΔG(5' antisentido) con ΔG(5' sentido) y exige además que
la brecha supere 1 kcal/mol. La consecuencia práctica, y es un buen ejemplo de por qué conviene
mirar la resta y no los términos, es que cualquier corrección que afecte igual a los dos extremos
—la corrección salina, por ejemplo— **se cancela exacto** y no mueve ningún veredicto. Esto el
port ya lo había verificado con un test; acá sólo se agrega que el artículo tampoco declara
condiciones de sal, así que el valor de `Na=20, K=50, Mg=0` de `free_energy.py:280` no tiene
respaldo en la publicación.

**Qué NO es.** No es una eficacia medida, ni una probabilidad de knockdown, ni un puntaje
calibrado. Tres razones concretas, y conviene tenerlas las tres: primero, los parámetros vienen
de fusión óptica de oligonucleótidos en 1 M de NaCl y se reportan a 37 °C (Chen 2012), y acá se
extrapolan a 22 °C y a unos 70 mM de monovalentes, fuera de las condiciones de calibración.
Segundo, el número no se ajustó nunca contra datos de silenciamiento: no hay regresión, no hay
pesos, no hay conjunto de entrenamiento; es una regla escrita a mano con dos constantes. Tercero,
el propio artículo trata el resultado como una **condición necesaria y no suficiente** —lo dice
explícitamente del término de accesibilidad en el pie de la Figura 2A— y su mejor evidencia de
poder predictivo es una correlación de −0,61 sobre doce construcciones, no una métrica por siRNA.

Dicho en los términos del equipo: `[H]` si-Fi21 es un **clasificador de reglas con umbrales
duros**, no un modelo. Su salida por ventana es un booleano obtenido de tres comparaciones y una
ramificación, y la riqueza está toda en los términos continuos que ese booleano tira a la basura
—la brecha de ΔG en kcal/mol y la probabilidad de apertura entre 0 y 1—. Para priorizar
candidatos, el vector continuo es más informativo que el conteo de booleanos, y no hace falta
ningún modelo nuevo para usarlo: ya está calculado.

## 5. Quién usó si-Fi21 después, y qué comparaciones o críticas hay publicadas

Búsqueda en Europe PMC el 2026-10-20, con tres consultas complementarias: la lista de citas del
artículo (135 registros devueltos, 128 contabilizadas como citas), la búsqueda de texto completo
por `"si-Fi21"` (14), por `"siFi21"` (30) y por `"siRNA-Finder"` (73). Los registros crudos
quedaron en `work/C1/citas_sifi_epmc.json` y las menciones extraídas en
`work/C1/sifi_menciones.json`. `[E]`

**En insectos el uso es escaso, y en hemípteros es casi inexistente.** La consulta
`"si-Fi21" AND (Hemiptera OR leafhopper OR whitefly OR aphid OR psyllid)` devuelve **cero**
resultados en Europe PMC. Ampliando a `"si-Fi"` y `"siRNA-Finder"` aparecen dos usos en hemípteros,
y los dos son de **especificidad entre especies, no de diseño**: la evaluación de ARNi en la
cochinilla de la vid *Pseudococcus maritimus* (*Insects* 2020, PMC7692628), que corrió si-Fi «con
los valores por defecto, 21 pb y cero desajustes» para contar cuántos 21-meros de sus ARNdc
coinciden perfecto en *Planococcus citri*, *Planococcus ficus* y dos pulgones; y el estudio de
efectos no deseados de ARNdc en hemípteros (*Genes* 2021, PMC8000911), que usa si-Fi para la misma
cuenta cruzada entre *Acyrthosiphon pisum*, *Myzus persicae*, *P. maritimus* y *Bemisia tabaci*.
En ninguno de los dos se usa el criterio de eficiencia para elegir región. `[E]`

**El uso más cercano a nuestro problema está en otro insecto vector.** En *Aedes albopictus*
(*Parasites & Vectors* 2025, PMC12619383) se identificaron regiones con si-Fi21, se tamizó cada
secuencia contra una base local del genoma de la especie, y se construyeron dos ARNdc por gen, de
400 y 500 pb. La Tabla 1 de ese trabajo publica los «hits de siRNA eficientes» de cada candidato:
237 y 240 para β-tubulina, 195 y 202 para el inhibidor de apoptosis, 197 y 214 para Dre4, 218 y 181
para nucampholina, 239 y 226 para Ras opposite. `[E]` El resultado experimental fue que **sólo
uno** de esos diez ARNdc —IAP 2, con 202— redujo la viabilidad celular, que todos los genes se
silenciaron en células, y que no hubo mortalidad larval significativa. `[H]` Nuestra lectura: en
ese conjunto el conteo de eficientes se mueve entre 181 y 240, un rango estrecho, y no separa al
candidato que funcionó de los nueve que no; es un indicio —no una prueba, porque el estudio no
estaba diseñado para evaluar a si-Fi— de que el conteo de eficientes discrimina poco cuando todas
las secuencias son largas y del mismo orden de tamaño.

**El uso más riguroso que encontramos es de evaluación de riesgo, no de diseño.** El análisis in
silico de off-targets de un acaricida de ARNdc contra *Varroa* (*Insects* 2025, PMC11942661) corre
si-Fi21 v.1.2.3.-0008 sobre genomas de organismos no objetivo, contando hits totales y hits
eficientes, y **contrasta la salida con una búsqueda exhaustiva con `bwa-aln`** para confirmarla.
Es el precedente publicado más parecido a lo que W5 hizo acá con Aho-Corasick y BLAST+, y conviene
citarlo como antecedente metodológico. `[E]`

**Críticas y comparaciones publicadas.** Hay tres, y ninguna es un benchmark con datos medidos.
`[E]` La primera es la del propio artículo (Tabla Suplementaria S1), contra siDirect, dsCheck y
RNAi Designer, que el artículo mismo aclara que no pudo hacer contra el experimento. La segunda
está en el artículo de la plataforma dsRIP (*BMC Biology* 2025, PMC12039203), que menciona a si-Fi
entre las herramientas previas y apunta dos cosas: que **nunca fue una herramienta en línea** y que
las herramientas previas se basaron en datos de siRNA **humanos**, mientras que ellos determinaron
sus parámetros en un modelo de insecto plaga. Esa es la crítica publicada más pertinente para
nuestro caso y coincide, por otro camino, con lo que muestra la tabla de P1: la evidencia primaria
de las reglas de secuencia es de células de mamífero. La tercera está en una revisión de métodos
de aprendizaje automático para diseño de siRNA (*NAR Genomics and Bioinformatics* 2026,
PMC13527166), que ubica a si-Fi entre las herramientas que enumeran sitios complementarios a la
semilla y los ponderan por accesibilidad, y la clasifica explícitamente como **«No (predictive)»**
en su tabla comparativa, es decir sin componente entrenado con datos experimentales. Dos
precisiones sobre esa revisión, porque el equipo va a leerla: describe a si-Fi como usuaria de
«RNAfold» cuando usa RNAplfold, y la marca con disponibilidad de servidor web, que es justo lo que
el artículo de dsRIP niega. `[?]` Las fuentes secundarias describen a si-Fi de manera
inconsistente; para cualquier afirmación sobre la herramienta conviene ir al artículo, al manual o
al código.

**Qué no encontramos, y es un vacío con valor.** No hay ningún trabajo publicado que use si-Fi21
en *Dalbulus maidis* ni en ningún cicadélido; no hay ninguna validación experimental del criterio
de eficiencia en un insecto; y no hay ningún benchmark que compare si-Fi21 con otra herramienta
contra eficacia medida. `[E]` sobre la búsqueda hecha, con el alcance que tiene: Europe PMC,
tres consultas de texto completo y la lista de citas; no se consultó Scopus ni Web of Science, ni
literatura no indexada.

## 6. Contraste con lo que el repositorio ya afirmaba

Está en `contraste_con_repo.md`, con una fila por afirmación. El titular es que **el artículo
respalda la decisión más discutible del port**: el modo «corregido» aplica la preferencia terminal
como filtro adicional sobre el veredicto termodinámico, y eso es exactamente lo que el artículo
describe en dos lugares —página 4, «se aplica una combinación de reglas de secuencia y
termodinámicas», y página 6, «las reglas de secuencia se reemplazaron por una combinación de
cálculo termodinámico y reglas de secuencia»— mientras que el código hace otra cosa. El modo fiel
reproduce el programa; el modo corregido reproduce el paper. `[E]`

## 7. Lo que el paper no dice y el equipo tiene que decidir `[H]`

Esta sección es juicio nuestro. Va ordenada por lo que conviene hacer con cada pieza del criterio.

**Conservar tal cual.** La ventana de 21 nt, porque es la única parte del criterio con fuente
primaria directa y mecanística, y porque el investigador ya la confirmó. La dirección de la
asimetría termodinámica: comparar los dos extremos y quedarse con el que tiene el 5' antisentido
menos estable. La accesibilidad como **condición necesaria y no suficiente**, leída tal como el
propio artículo la presenta, sin interpretar la altura del pico como una medida de calidad. Y el
tamizaje de off-targets por coincidencia exacta del 21-mero completo, que es lo que el campo
—si-Fi, dsRNAEngineer y dsRIP— hace con Bowtie.

**Reemplazar.** La regla del nucleótido terminal tal como está implementada, por dos motivos
independientes y acumulativos: la ramificación que permite declarar eficiente a un siRNA que falla
la termodinámica, que el port ya cuantificó entre 14 % y 24 % de los eficientes, y el índice de la
posición 2 donde la fuente primaria y el propio cálculo de ΔG del programa ponen la posición 1.
La propuesta concreta es la del modo corregido del port **más** el arreglo del índice, y declarar
los dos cambios al investigador como lo que son: desviaciones deliberadas del programa que él usa,
con la justificación del artículo, no mejoras silenciosas. Si el equipo prefiere no tocar el
índice sin medirlo primero, la medición es barata y está especificada en P1.

**Presentar como convención, con su incertidumbre explícita.** Los dos números: 1 kcal/mol y 0,1.
No tienen fuente, y uno de ellos —el de 1 kcal/mol— es el doble de la única diferencia medida que
encontramos publicada. También u = 8, W = 80 y L = 40, que vienen del linaje de RNAxs pero sin que
ninguna fuente abierta los fije para este uso, y los 22 °C, que no están en el artículo. La forma
honesta de presentarlos en el entregable es con un barrido de sensibilidad alrededor de cada uno
—el port ya tiene el barrido hecho— y diciendo cuánto cambia el ranking de candidatos, en vez de
defender los valores.

**Y una decisión de diseño que el paper directamente no aborda.** El criterio devuelve un booleano
por ventana y después se cuentan booleanos por región. Dos problemas: el conteo es de **hits** y no
de siRNA únicos, así que depende de la base de datos, cosa que el propio manual deja ver cuando
llama «hits» a lo que cuenta; y la binarización tira la información continua. Para el entregable de
priorización, nuestra recomendación es reportar por ventana el vector completo —brecha de ΔG en
kcal/mol, probabilidad de apertura, los dos nucleótidos de la regla terminal, y los off-targets por
clase de referencia— y usar el booleano de si-Fi sólo como columna de compatibilidad con lo que el
laboratorio ya tiene. Eso es defendible ante el investigador porque no reemplaza su criterio: lo
expone.

## 8. Vacíos declarados, bloqueos y preguntas

**Vacíos.** No hay fuente abierta para el rango de 150 a 250 nt ni para «con largos no funciona»
(P3). No hay fuente para 1 kcal/mol, para 0,1 ni para los 22 °C. No hay validación del criterio en
ningún insecto. No hay ningún uso publicado de si-Fi21 en cicadélidos. No se midió cuántas ventanas
cambian de veredicto al corregir el índice de la regla terminal; sí se midió cuántas cambian de rama.

**Bloqueos de red, sin espejos ni proxies.** `sourceforge.net`, `zenodo.org` y
`doi.ipk-gatersleben.de` están fuera de la lista de dominios permitidos, así que no se pudieron
abrir el binario de 2017, el código depositado en Zenodo ni el conjunto de calibración de e!DAL
(`10.5447/IPK/2018/2`), que es donde viven las secuencias sintéticas de la validación. Tampoco se
pudieron abrir `cell.com`, `nature.com` ni `academic.oup.com`, de modo que Schwarz 2003,
Khvorova 2003, Reynolds 2004, Tafer 2008, Bernhart 2006 y Ameres 2007 quedaron en nivel de lectura
«sólo resumen». No hubo ningún rechazo de filtro de seguridad en esta investigación.

**Preguntas para el investigador**, en orden de rendimiento:

1. El rango de 150 a 250 nt y «con largos no funciona»: ¿de qué ensayo salen? Especie, vía de
   entrega, largos comparados y medida. No está en si-Fi ni en su artículo, y la práctica publicada
   con si-Fi21 usa 400 y 500 pb.
2. ¿Qué entiende él por «identidad» dentro del criterio de eficiencia? En el programa, identidad es
   el presupuesto de desajustes de Bowtie, que por defecto es cero, y si se abre, la herramienta
   **apaga** el cálculo de eficiencia. Si su equipo corre con desajustes, los conteos no son
   comparables con los nuestros.
3. ¿Corre en modo diseño (HE) o en modo off-target (HS)? Los defaults son distintos y el conteo de
   eficientes cambia por completo: HS apaga estabilidad de extremos y accesibilidad.
4. La licencia del software: el artículo dice CC BY-SA 4.0 y el repositorio oficial dice
   CC BY-NC-SA 2.0. Si algo de esto se publica, ¿cuál rige?
5. ¿Está al tanto de que la regla del nucleótido terminal, tal como está en el fuente, puede
   declarar eficiente a un siRNA que falla la selección de hebra y la estabilidad de extremos? Es
   la diferencia entre nuestros dos modos y es la única discrepancia real entre su artículo y su
   código.

## Nota de método

Todo lo que esta investigación afirma del artículo lleva página, sección, tabla o figura; todo lo
que afirma del código lleva archivo y línea del clon en
`work/C1/siFi21--d6296b7/`, descargado del repositorio oficial en el commit `d6296b7` y dejado
fuera del control de versiones por ser de un tercero con licencia en conflicto: no se copió ningún
archivo suyo a la parte versionada del repositorio. Los papers se parafrasearon; las dos únicas
expresiones entrecomilladas del artículo son las que definen el criterio, donde la formulación
exacta importa. Ninguna secuencia de EPILAB se usó ni se envió a ningún servicio: la única
secuencia que se procesó es el genoma público `NC_002786.2`, y se procesó localmente. Los
originales de `YHat-Biotech/` no se tocaron.
