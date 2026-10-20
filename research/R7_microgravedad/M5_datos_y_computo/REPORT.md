# R7 · M5 — Datos abiertos de vuelo y métodos computacionales: qué hay, qué puede reanalizar una notebook de 16 GB y si algo encaja

Corte: 2026-10-19. Ventana principal: octubre de 2024 a octubre de 2026; lo anterior se marca «fundacional» cuando es la única evidencia o la base del campo. Marcadores de `CLAUDE.md`: `[E]` establecido, `[R]` reportado, `[H]` hipótesis o cálculo del equipo, `[?]` incierto. Las referencias `M5-xx` están en `sources.json` con su nivel de lectura; cada consulta está en `datos/COMANDOS.md`; el inventario por estudio, en `inventario_osdr.json`; las opciones, en `opciones.md`; las preguntas y los dominios que fallaron, en `preguntas_pendientes.md`. «Real» es microgravedad en órbita, vuelo parabólico o suborbital; «simulada» es clinostato, RPM, RWV, levitación magnética y similares. No se mezclan en ninguna tabla.

## Veredicto

**Los datos abiertos de vuelo espacial no tocan al insecto ni a los mollicutes, tocan apenas al maíz, y no hay en ellos nada que valga horas de L1 a L3. La pregunta de R7 sobre los dos mollicutes que el RNAi no alcanza tiene, en este eje, una respuesta de «no sirve» `[H]`.**

*Qué datos existen.* En el OSDR de la NASA hay 642 estudios OSD (índice consultado el 2026-10-19; el resto de los 138.413 registros del índice son registros federados de GEO, PRIDE y MG-RAST que no son de vuelo y no cuentan) `[R]` M5-01. Entre ellos, *Zea mays* aparece 0 veces, Hemiptera 0, mollicutes (*Spiroplasma*, *Mycoplasma*, fitoplasmas) 0, y estudios de ARN pequeño en plantas, insectos o microbios 0: los 21 estudios con archivos de miARN son de ratón (18) o humano (3) `[R]` M5-01, M5-02. Hay 76 estudios de plantas (61 de *Arabidopsis thaliana*), 19 de insectos (17 de *Drosophila melanogaster* y 2 de avispas parasitoides *Leptopilina*), y tres de cereales: *Brachypodium distachyon* en la ISS (OSD-375), trigo en la ISS (OSD-622) y raigrás en regolito simulado, sin factor de gravedad (OSD-581). Fuera del OSDR, en NCBI, hay un microarray de maíz etiolado crecido en la ISS (BioProject PRJDB11348, cultivar Golden Cross Bantam, frente a 1 g en Tierra) cuyo archivo de datos no se pudo localizar, y un conjunto de arroz (callos) en vuelo con control de 1 g en vuelo (GSE78839, 10 arrays) que sí se pudo medir `[R]` M5-05, M5-06. La consulta cruzada por organismo y términos de gravedad en GEO y BioProject da 0 para Hemiptera, *Dalbulus*, *Spiroplasma*, *Candidatus* Phytoplasma y Mollicutes `[R]` M5-04.

*Qué se puede hacer con ellos.* En tamaño todo es cómodo: las tablas de conteos sin normalizar de los seis estudios de *Arabidopsis* cuyos archivos se listaron en detalle pesan de 2,3 a 6,0 MB cada una, y el arroz de GSE78839 pesa 2,8 MB más 1,5 MB de anotación (ya descargados, 4,3 MB) `[R]` M5-02, M5-06, M5-07. Pero **no se pudo descargar ningún archivo de datos del OSDR** (el host de almacenamiento no está en la lista permitida; ver `preguntas_pendientes.md`), así que lo medido son tamaños, nombres y metadatos, no contenido. Y los dos cereales del OSDR no son reanalizables en una notebook: OSD-375 solo tiene lecturas crudas (unos 463 GB, 48 muestras) y OSD-622 es un microarray de 2006 en archivos `.xls` y documentos.

*¿Vale alguna opción las horas del equipo?* Una sí, y por poco: empaquetar el inventario y los ceros como «vacío documentado» para el eje de innovación abierta, 4 a 6 h `[H]` (4 a 6 % de las 96). Una segunda, preguntar si la maquinaria de silenciamiento de la planta cambia en vuelo (*Arabidopsis* y arroz), cuesta 10 a 12 h en su versión mínima `[H]`, no mueve L1, L2 ni L3 y solo debería hacerse si la primera corrida punta a punta ya está cerrada. **Se descartan** la dinámica molecular con gravedad alterada (la gravedad vale unas 2×10⁻⁹ veces la energía térmica a escala de una proteína, cálculo propio `[H]`), el ML de cristalizabilidad (ningún predictor usa microgravedad como variable y entrenar uno viola D8), el ajuste fino de modelos fundacionales con datos de vuelo (viola D8; los datos son pocos y confundidos por diseño) y el reanálisis de los dos cereales del OSDR. Los análogos terrestres no son opción para el equipo: necesitan laboratorio (D1).

*No evaluado a esta profundidad.* El contenido de los datos (nada se descargó del OSDR), el archivo de maíz PRJDB11348 (ubicación y licencia sin verificar), otros repositorios de vuelo fuera de NCBI y OSDR (China, ESA, JAXA), y la licencia de cada estudio. 13 de las 44 fuentes se leyeron solo en resumen y 9 solo como fragmento del buscador. Detalle en «Qué no se pudo establecer».

---

## 1. Inventario OSDR

### 1.1 Método y universo

El buscador de OSDR (`https://osdr.nasa.gov/osdr/data/search`) mezcla estudios de vuelo con registros federados. Se midió la composición del índice con `size=1` por `type`: 138.413 registros sin filtrar; `cgene` 572, `alsda` 84 (13 registros con ambos tipos), GEO 122.472, PRIDE 12.569, MG-RAST 2.729. La suma cierra: 572 + 84 − 13 = 643 = 138.413 − 122.472 − 12.569 − 2.729. Esos 643 registros llevan accesión `OSD-*` y corresponden a 642 estudios únicos (OSD-729 está duplicado), entre OSD-1 y OSD-1015 `[R]` M5-01. La accesión está en `_source.Accession`, no en `_id`; un primer filtro por `_id` dio cero OSD y era erróneo. Se volcó el universo completo (`type=cgene` y `type=alsda`, paginado) y se aplicaron filtros locales de organismo y de texto sobre ese volcado, además de una batería de 93 consultas por término con el conteo de OSD tras el filtro (tabla completa en `datos/COMANDOS.md`, parte A). Los hits del buscador son difusos (subcadenas y texto libre) y se usaron solo como consulta registrada; los conteos que respaldan los ceros salen del volcado local. De los 642 estudios, 347 tienen tipo de proyecto «Spaceflight Study» y 273 «Ground Study»; por organismo hay 399 de mamíferos, 121 de microbios o microbiota, 76 de plantas, 21 de otros animales, 19 de insectos, 2 de algas y 4 sin organismo.

Las rutas de metadatos y archivos con prefijo (`/osdr/data/osd/meta/OSD-375`) devuelven vacío para todos los estudios probados; funcionan con el número solo (`/meta/375`, `/files/375`). El caso OSD-118 del prompt es coherente con eso: con prefijo la respuesta viene vacía; con número se obtuvo sin error.

### 1.2 Cuatro grupos, separados por tipo de gravedad

El inventario (`inventario_osdr.json`) tiene 155 entradas: las 76 de plantas, las 19 de insectos, 13 de microbios elegidos por ser fitopatógenos, entomopatógenos, aislados de la ISS de interés fitosanitario o por mencionar patógenos de plantas, y 47 de ARN pequeño o miARN (de los cuales los que no están en otro grupo son de mamíferos y *Caenorhabditis elegans*). La clase gravitacional se asignó por tipo de proyecto, misión y plataforma del registro, con revisión manual de los casos de borde; es heurística y cada entrada la declara.

| grupo | entradas | real orbital | real parabólico o suborbital | simulada o alterada en tierra | sin factor gravitacional |
| --- | ---: | ---: | ---: | ---: | ---: |
| plantas | 76 | 34 | 5 + 3 | 3 + 1 (levitación magnética y RPM, OSD-8) | 30 |
| insectos | 19 | 14 | 0 | 2 simulada o alterada (OSD-27, OSD-34) + 2 hipergravedad terrestre (OSD-70, OSD-85) | 1 (OSD-590, laboratorio subterráneo) |
| microbios seleccionados | 13 | 9 | 0 | 1 (OSD-729) | 3 |
| ARN pequeño o miARN | 47 | 30 | 0 | 6 | 11 |

«Sin factor gravitacional» agrupa estudios de radiación, regolito, baja presión o genomas de aislados; no son microgravedad real ni simulada. Los términos de plataforma devuelven, como hits difusos del buscador con filtro OSD: «spaceflight» 434, «International Space Station» 319, «microgravity» 299, «simulated microgravity» 79, «centrifuge» 45, «space shuttle» 44, «clinostat» 21, «hypergravity» 20, «random positioning machine» 13, «rotating wall vessel» 12, «parabolic flight» 9, «sounding rocket» 2 y «Tiangong» 0. No son conteos curados.

### 1.3 Maíz y cereales: cero en el OSDR, tres cereales, y maíz fuera del OSDR

El filtro de maíz (`Zea`, `maize`, `corn` en cualquier campo de los 642 estudios) devuelve un solo registro, OSD-855, que es un falso positivo: «Iowa corn soil» como sustrato en un ensayo de regolito lunar con lechuga y rábano `[R]` M5-01. Con consulta por nombre científico y por nombre común: «Zea mays» da 505 hits mixtos y 0 OSD; «maize», 535 y 0; «corn», 147 y 1 (el falso positivo). Los 505 registros federados de «Zea mays» se revisaron buscando términos de gravedad: ninguno es de vuelo. El índice no expone taxid, de modo que este cero es por organismo y texto, no por taxid (cf. D12).

| estudio | especie | plataforma | ensayo | muestras | datos | tamaño | lectura |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| OSD-375 | *Brachypodium distachyon* | real, ISS (SpaceX-14, Veggie/APEX) | RNA-seq Illumina | 48 | solo crudos | 96 FASTQ, ~463 GB; MultiQC de 2,2 MB | inviable en 16 GB |
| OSD-622 | *Triticum aestivum* (trigo enano) | real, ISS (STS-110, BPS) | microarray | 11 | crudos y normalizados (xls, doc, ppt) | 27,7 MB | pequeño y heterogéneo; cobertura de sondas no verificada |
| OSD-581 | *Lolium multiflorum* | tierra, regolito marciano simulado | proteómica | 12 archivos | solo crudos | ~3,4 GB | no es gravedad |

Fuera del OSDR, la consulta por organismo y términos de gravedad en BioProject y GEO encuentra los conjuntos de Poaceae de la tabla siguiente `[R]` M5-04, M5-05, M5-06, M5-08, M5-09. Dos observaciones. El índice del OSDR no contiene el maíz de PRJDB11348 ni el arroz de GSE78839, así que «cero en el OSDR» no es «cero datos de vuelo»; la propia revisión de Manzano et al. reconoce que su búsqueda se centró en GeneLab y que puede haber omitido trabajos (M5-18). Y los dos conjuntos de trigo marcados «espacial» (PRJNA386075, PRJNA374931) son transcriptomas de mutantes inducidos por vuelo de semillas, medidos en tierra: son mutagénesis espacial, no medición en microgravedad.

| BioProject o serie | especie | qué es | diseño | plataforma |
| --- | --- | --- | --- | --- |
| PRJDB11348 | *Zea mays* cv. Golden Cross Bantam, etiolado | microgravedad real, ISS, frente a 1 g en Tierra | expresión, microarray Agilent (Design ID 016047) | datos sin localizar |
| GSE78839 | *Oryza sativa*, callos de 4 días, 324 h | vuelo real; control de 1 g en vuelo y control en tierra | 4 de vuelo, 3 de 1 g en vuelo, 3 de tierra; Affymetrix, 57.381 sondas | descargado (2,8 MB) |
| PRJDB12879 | *Oryza sativa*, punta de raíz | microgravedad simulada (clinostato) | RNA-seq | no evaluado |
| PRJNA761100 / GSE183508 | *Triticum aestivum*, raíz | hipergravedad terrestre (10 g, 12 h) | 4 muestras RNA-seq | ficha leída |
| PRJNA386075, PRJNA374931 | *Triticum aestivum* | mutantes inducidos por vuelo, medidos en tierra | RNA-seq | no evaluado |

El vínculo de PRJDB11348 con los artículos publicados es inferido `[?]`: los resúmenes del experimento «Auxin Transport» (ISS, módulo JEM, 2016 y 2017) describen maíz Golden Cross Bantam etiolado en microgravedad y un control de 1 g por centrífuga a bordo (CBEF), y la descripción del BioProject coincide en cultivar, tejido y plataforma `[R]` M5-20, M5-21, M5-22. Asimismo, GSE78839 coincide en duración (324 h) y diseño con el experimento de callos de arroz en el incubador Simbox de una nave Shenzhou descrito en la revisión de Manzano et al., que menciona un control de 1 g por centrífuga integrada; la revisión no cita el accesión, así que el vínculo es inferido `[?]` M5-18. Un hallazgo adicional de la literatura: un estudio de maíz sobre RPM a 0,38 g con regolito marciano simulado (simulada, no vuelo) midió expresión por qPCR de genes PIN sin depositar datos ómicos `[R]` M5-17.

### 1.4 Insectos: 19 estudios, ningún hemíptero

Hay 17 estudios de *Drosophila melanogaster* y 2 de avispas parasitoides *Leptopilina heterotoma* y *L. boulardi* (OSD-609, OSD-610, 8 muestras de RNA-seq cada uno, en la ISS con SpaceX-14). Catorce son de vuelo orbital real, dos de simulación o alteración en tierra (levitación magnética, OSD-27; instalaciones de gravedad alterada, OSD-34), dos de hipergravedad terrestre (OSD-70, OSD-85) y uno de laboratorio subterráneo (OSD-590). El filtro de hemípteros (cicadélidos, delfácidos, áfidos, moscas blancas, chinches) devuelve un solo registro, OSD-144, falso positivo por «aphidicolin», un inhibidor del ciclo celular en cultivo de *Arabidopsis*. La consulta cruzada en GEO y BioProject por *Dalbulus* y Hemiptera con términos de gravedad da 0 en ambas bases `[R]` M5-01, M5-04. Los datos de insectos son grandes: de 20 a 340 GB de lecturas crudas por estudio de RNA-seq, con tablas procesadas de decenas a cientos de MB por estudio (por ejemplo OSD-609: 65 GB crudos y 44,5 MB de tablas procesadas).

Un hallazgo de la literatura, sin condiciones y sin propuesta derivada: el registro OSD-278 describe un aumento de virulencia de una bacteria en *Drosophila* en vuelo y en microgravedad simulada; el listado de Europe PMC trae además el título de un trabajo sobre la «hipervirulencia» de un aislado de *Beauveria bassiana* (hongo entomopatógeno) mutado por vuelo, para control integrado (solo título visto, no abierto) `[R]` M5-01, `[?]` M5-44. No se propone cultivar ni exponer patógeno alguno.

### 1.5 Microbios y mollicutes: cero mollicutes

Los tres registros que coinciden con *Mycoplasma* son estudios de células humanas que mencionan la prueba de contaminación por micoplasma (OSD-344, OSD-812, OSD-999): falsos positivos. No hay *Spiroplasma*, fitoplasma ni *Acholeplasma* en el OSDR. Los fitopatógenos que aparecen son aislados de la ISS o de plantas cultivadas en la ISS, y los estudios son de genoma o de metagenómica, sin la gravedad como factor experimental: *Fusarium oxysporum* (OSD-177 y OSD-264, esta con «potencial de virulencia» en el título), *Agrobacterium* genomoespecie 3 (OSD-306), un hongo oportunista sobre plantas cultivadas en vuelo (OSD-358) y un método de diagnóstico de enfermedades de plantas en el espacio (OSD-594) `[R]` M5-01. La literatura trae además trabajos con bacterias beneficiosas de plantas en microgravedad simulada y revisiones sobre inmunidad vegetal frente a patógenos humanos en microgravedad (M5-39, M5-40), pero ningún estudio de un fitopatógeno del achaparramiento ni de un mollicute en vuelo.

### 1.6 ARN pequeño, miARN y silenciamiento

Las categorías de archivo `miRNA-Seq`, `miRNA` o `small RNA` aparecen en 21 de los 642 estudios, todos *Mus musculus* (18) o *Homo sapiens* (3), tras revisar los listados de archivos de todo el universo `[R]` M5-02. Con un criterio más amplio por texto en título o tipo de ensayo hay 47 candidatos, de los cuales los no mamíferos son dos estudios de *C. elegans* (OSD-41, OSD-75). Ningún estudio de planta, insecto o microbio tiene archivos de ARN pequeño. Lo más cercano en plantas es epigenética: metilación en *Arabidopsis* en vuelo con mutantes `met1-7` y `elp2-5` (OSD-416, OSD-427, OSD-625, OSD-217), donde la descripción vincula esos genes con la respuesta a patógenos y la revisión de Manzano et al. señala que ELP2 interactúa con la maquinaria de siRNA para guiar metilación (M5-18) `[R]`. El estudio OSD-437 (*Arabidopsis*, EMCS, 19 muestras) que M3 identifica como probable experimento de regulación de ARN solo contiene RNA-seq en masa: sus 376 archivos no incluyen ninguno de ARN pequeño `[R]` M5-02.

### 1.7 Estado y tamaño de los datos de plantas de vuelo

De los 42 estudios de plantas de vuelo real (34 orbitales, 5 parabólicos, 3 suborbitales), 24 tienen RNA-seq (20 de *Arabidopsis*, y uno de *B. rapa*, *Eruca*, *Brachypodium* y tomate) y 11 tienen microarray. De los 24, 21 traen tablas de conteos o de expresión diferencial listadas; los tres que no las traen son OSD-301, OSD-375 y OSD-480. La mediana de lecturas crudas por estudio de RNA-seq es de unos 135 GB (14 a 1.548 GB) y la de muestras por tabla, 36. Lo que importa para una notebook son las tablas de conteos: en OSD-437, OSD-678, OSD-427, OSD-120 y OSD-37, los conteos sin normalizar pesan 2,31; 4,49; 5,87; 4,03 y 6,0 MB, las normalizadas de 7 a 23 MB y las de expresión diferencial de 51 a 272 MB `[R]` M5-02. Las listas por archivo están en `datos/osdr_meta/tablas_procesadas_candidatas.json`. Esos tamaños no se pudieron contrastar con una descarga.

---

## 2. Análogos terrestres de microgravedad y sus límites

Ningún análogo reduce la gravedad: los clinostatos, el RPM y el recipiente de pared rotatoria cambian su dirección relativa a la muestra para que el promedio temporal tienda a cero, y de esa diferencia salen sus artefactos `[E]` M5-13. Esto separa a los análogos del vuelo real, y los resultados de uno no se trasladan al otro de forma automática.

| análogo | qué simula | qué no, y artefactos documentados | fuente |
| --- | --- | --- | --- |
| clinostato de un eje (lento) | promedio de la dirección de gravedad en muestras pequeñas | la aceleración centrífuga crece con el radio: a_c = ω²·r; hay que acercar la muestra al eje | M5-11, M5-13 |
| clinostato rápido (50 a 120 rpm) | anula la sedimentación en un líquido para organismos pequeños | solo sirve para unicelulares o bacterias, no para plantas | M5-13 |
| máquina de posicionamiento aleatorio (RPM) | orientaciones aleatorias en dos ejes; ~10⁻² a 10⁻³ g de g medio residual en un modelo reciente | aceleración centrífuga dependiente del tiempo (pico aproximado de 2,41·ω²·r en el peor caso); no hay estudio sistemático de límites aceptables; la cizalla del fluido es mayor en el modo aleatorio que en clinorrotación a 60 rpm en un bioensayo con un dinoflagelado | M5-11, M5-12, M5-15 |
| recipiente de pared rotatoria (RWV) | caída libre de agregados con baja cizalla | la velocidad adecuada varía mucho con la densidad del cultivo y del medio; en bacterias, los análogos remedan aspectos de la respuesta a gravedad reducida (según el resumen) | M5-10, M5-12, M5-16 |
| levitación diamagnética (magnética) | gravedad efectiva reducida o aumentada por gradiente magnético | campos de unos 15 T y gradientes de unos 1.400 T²/m que pueden alterar el movimiento de iones y la expresión génica; volumen útil mínimo, costo alto | M5-13 |
| centrífugas de gran radio e hipergravedad | gravedad mayor que 1 g; «paradigma de gravedad reducida» al bajar de un nivel adaptado | exige un sistema estable en el nivel alto; no es microgravedad | M5-13 |

La literatura de plantas es explícita en que los análogos y el vuelo difieren mucho. Kiss et al. concluyen que existen grandes diferencias entre plantas crecidas en estos dispositivos y en ingravidez, y que la rotación en ciertos clinostatos puede ser perjudicial para algunos sistemas biológicos; piden estudios pareados con el mismo hardware y las mismas semillas y el mismo medio (M5-13) `[E]`. Wuest et al. (RPM, células de mamífero) documentan buen acuerdo en leucocitos, pero en los dos experimentos pareados con vuelo y RPM simultáneos (condrocitos y la línea de tiroides FTC-133) las muestras en RPM mostraron efectos intermedios, y los autores especulan que algunos procesos moleculares serían demasiado rápidos para el RPM (M5-11) `[R]`. Hauslage et al. muestran con un bioensayo de bioluminiscencia que el modo aleatorio del RPM genera más cizalla que la clinorrotación de un eje, y que hay que reportar el hardware, el cambio de medio y los efectos no gravitacionales (M5-12) `[R]`; es un solo organismo, no una planta ni un insecto. Un estudio reciente en raíces de *Arabidopsis* en RPM muestra que la oscuridad más la rotación hacen perder la percepción vertical y que 10 µmol m⁻² s⁻¹ de luz blanca la compensan, es decir, que la luz confunde la lectura de «microgravedad» (M5-14) `[R]`. El estudio de maíz en RPM a 0,38 g reconoce como limitación que los ensayos en placas verticales pueden elevar el etileno por contacto mecánico y que la rotación misma puede estimular etileno, y mitiga con sellos permeables y con el monitoreo de un gen de la vía (M5-17) `[R]`. Quienes defienden el RPM lo hacen con condiciones explícitas, y conviene leerlo con ese sesgo: Wuest et al. lo consideran una alternativa válida una vez tomadas en cuenta las restricciones (rotación más rápida que el proceso biológico, sin efectos secundarios indeseados) (M5-11); Pica et al. caracterizan un RPM con unidades de medición inercial y un modelo computacional de dispersión de gravedad, con aceleración centrífuga inferior a 0,08 g en todos los modos y efectos biológicos más suaves en modo clinostato en una línea celular neuronal (M5-15) `[R]`.

De la bibliografía abierta salen las condiciones que **invalidarían** una conclusión basada en un análogo: que la muestra esté lejos del eje de rotación (centrífuga y cizalla), que la velocidad no sea mayor que el tiempo de respuesta biológico, que haya una fase de espera sin rotar antes de la fijación (la rotación se detiene para cosechar), que el hardware, el medio y la luz difieran del control, que el organismo sea sensible a cizalla (cultivos en suspensión) y que el control de 1 g no esté montado a otra distancia del eje (consecuencia del argumento de Wuest sobre la distancia al eje `[H]`). Para el equipo, la consecuencia es que una conclusión extraída de un análogo no se puede usar para predecir el vuelo, ni al revés, y que cualquier validación de RNAi con análogos requeriría laboratorio, fuera de D1.

---

## 3. Métodos computacionales

### 3.1 Dinámica molecular con gravedad alterada: no hay, y la física explica por qué

Se buscó en Europe PMC y en la web una simulación de dinámica molecular o de plegamiento con un término de gravedad distinto de 1 g y no se encontró ninguna. El único cruce de «dinámica molecular» con microgravedad es un estudio que simula, con GROMACS y un campo de fuerzas estándar, dos estructuras cristalinas depositadas de una lipasa, una crecida en el espacio y otra en la Tierra, y concluye que la primera es más estable; usa una trayectoria por estructura (de al menos 14 ns según las curvas de RMSD leídas) y no incluye ningún término de gravedad `[R]` M5-25. Es dinámica molecular *sobre* un cristal de origen espacial, no *con* gravedad alterada. El cálculo propio de orden de magnitud `[H]` (`datos/calculo_gravedad_escala_molecular.txt`; aproximación de Stokes, 300 K, con volumen específico parcial de 0,73 cm³/g para proteína y 0,55 para ARN y un Δρ de cristal de 250 kg/m³, todos supuestos y declarados) da lo siguiente.

| objeto | m·g·h con h = 10 nm | (m·g·h)/(kB·T) | velocidad de sedimentación | número de Péclet de sedimentación |
| --- | ---: | ---: | ---: | ---: |
| proteína de 50 kDa | 8,1×10⁻³⁰ J | 2,0×10⁻⁹ | 4,8×10⁻¹² m/s | 1,3×10⁻¹⁰ |
| ARN de ~32 kDa (100 nt) | 5,2×10⁻³⁰ J | 1,3×10⁻⁹ | 6,5×10⁻¹² m/s | 1,1×10⁻¹⁰ |
| proteína de 150 kDa | 2,4×10⁻²⁹ J | 5,9×10⁻⁹ | 1,0×10⁻¹¹ m/s | 5,6×10⁻¹⁰ |
| cristal de 100 µm (radio 50 µm) | — | — | 1,4×10⁻³ m/s | 1,6×10⁷ |

La gravedad es irrelevante a escala molecular y dominante a escala de cristal y de flujo `[H]`; por eso la literatura de cristalización en microgravedad habla de transporte, convección y zonas de depleción de proteína e impurezas, no de cambios de plegamiento, y lo único «numérico» ligado a microgravedad que se leyó son los análisis numéricos de esas zonas de depleción que el programa de JAXA menciona como apoyo de su diseño, citados solo en la introducción (M5-24) `[R]`. M2 llega por su cuenta a una conclusión de la misma forma, con un cálculo de orden de magnitud propio.

### 3.2 ML sobre cristalización y estabilidad

Los predictores de cristalizabilidad por secuencia están bien establecidos en tierra. El benchmark más reciente leído (Mall et al., 2025) compara clasificadores sobre embeddings de modelos de lenguaje de proteínas (ESM2, Ankh, ProtT5-XL, ProstT5, xTrimoPGLM, SaProt) con DeepCrystal, ATTCrys y CLPred y reporta ganancias de 3 a 5 % en AUPR, AUC y F1 en conjuntos independientes para los mejores embeddings de ESM2 `[R]` M5-28. Esas comparaciones son contra predictores de tierra: el texto no menciona la microgravedad ni una variable de vuelo (0 apariciones del término). Un fragmento de otro predictor reciente muestra métricas muy desiguales entre conjuntos de prueba, lo que sugiere cautela con cifras de un solo conjunto, pero no sostiene ninguna cifra por sí solo `[?]` M5-35. En el lado de vuelo, las revisiones sobre cristalización en microgravedad reportan que la mejora es irregular: el propio texto de McPherson y DeLucas cita la revisión del NRC que juzgó los resultados inconclusivos, con mejoras incrementales y dificultades para tener controles adecuados, y discute que el control de «mismo hardware en Tierra» no es el más exigente (M5-23) `[R]`. Un estudio de 2025 con un bioensamblador en la ISS reporta cristales de alta resolución pero agrietados, y declara inviable una comparación de calidad con los de la Tierra (M5-27) `[R]`. El único indicio de «predecir qué proteínas se benefician» es una frase de un resumen sobre transporte de agregados (M5-26), no un modelo. **Ningún modelo de ML sobre resultados de cristalización en microgravedad se encontró.**

### 3.3 Reanálisis y metaanálisis de transcriptomas de vuelo

Es la parte con precedentes serios, y con una advertencia común: el diseño experimental pesa más que el vuelo. Morrison y Nicholson estandarizaron ocho conjuntos bacterianos de GeneLab con una canalización común y no encontraron ningún gen ni conjunto de genes compartido entre todos; el análisis de componentes principales mostró que la mayor parte de la variación proviene de las diferencias entre experimentos (medio, hardware, tiempo de incubación) y no de vuelo frente a control `[R]` M5-30. Barker et al. reanalizaron 15 experimentos de *Arabidopsis* de GeneLab con un solo flujo para microarray y otro para RNA-seq, construyeron una matriz de metadatos y concluyeron que el tipo de ensayo y el hardware tienen efectos de confusión importantes; confirmaron cambios en procesos de pared celular y estrés oxidativo y destacaron la respuesta conservada de un gen de respuesta al frío (*COR78*) `[R]` M5-29. La revisión de Manzano et al. añade que la remodelación de pared, el estrés oxidativo, la respuesta de defensa y la fotosíntesis son procesos comunes alterados en plantas en vuelo, aunque con una búsqueda centrada en GeneLab `[E]` M5-18. En ML, GLARE (preprint) aplica aprendizaje de representaciones a un conjunto de raíz de *Arabidopsis* en vuelo (luz, oscuridad y microgravedad) y sugiere que sustenta los hallazgos del estudio original y añade patrones de hipoxia (solo el resumen) `[R]` M5-32; un preprint de 2026 usa 10 conjuntos humanos del OSDR (N = 136) con correlación gen–gen (resumen) `[R]` M5-33. Fragmentos de buscador apuntan a más trabajo de este tipo (un metaanálisis entre especies sobre datos del OSDR, un trabajo de ML ratón-humano y un análisis de redes sobre *Arabidopsis*); no sostienen cifras `[?]` M5-34, M5-36, M5-37, M5-38, M5-41. En conjunto, el ML y el metaanálisis publicados sobre el OSDR son sobre todo de mamíferos y de *Arabidopsis*; no hay ninguno sobre maíz, hemípteros o mollicutes.

### 3.4 Modelos fundacionales con datos de vuelo

No se encontró ningún modelo fundacional de ARN o de proteínas usado con datos de vuelo (búsqueda web 6; ver `datos/COMANDOS.md`, parte C). La perspectiva más reciente de los equipos del OSDR (Costes et al., 2026, preprint) propone afinar modelos fundacionales de transcriptomas de célula única con datos de vuelo, y reconoce que preentrenar uno desde cero con el catálogo actual del OSDR no es realista (los conjuntos de preentrenamiento de Geneformer y scGPT son al menos un orden de magnitud mayores que el catálogo de célula única del OSDR); las tres referencias que da como precedentes en esa fila de su tabla están rotuladas como biomédicas terrestres o de ML, no como de vuelo (solo se leyeron el resumen, la tabla y ese pasaje) `[R]` M5-31. Es consistente con D8, que reservaba los datos y descartaba el ajuste fino.

| línea | qué existe | evaluado con seriedad | es demostración |
| --- | --- | --- | --- |
| MD con gravedad alterada | nada | no | — |
| MD de estructuras de origen espacial | un estudio de lipasa (M5-25) | una trayectoria por estructura | sí |
| ML de cristalizabilidad | predictores de tierra con benchmark (M5-28) | sí, en tierra | sin variable de microgravedad |
| ML sobre cristalización en microgravedad | nada | no | — |
| metaanálisis de transcriptomas de vuelo | bacterias, *Arabidopsis*, humano (M5-29, M5-30, M5-33) | sí, con confusión por diseño reconocida | — |
| ML de representaciones sobre transcriptomas de vuelo | GLARE (preprint, un conjunto) | un conjunto | sí |
| modelos fundacionales con datos de vuelo | propuestas (M5-31) | no | sí |

---

## 4. Factibilidad para el equipo

Lo que se midió sin descargar del OSDR y lo que se descargó se resume aquí; los esbozos completos (datos, pasos, control, qué se concluye y qué no, horas y riesgo) están en `opciones.md`.

**Prueba mínima descargable (GEO).** Se descargó la matriz de la serie GSE78839 (2,78 MB, 10 arrays y 57.381 sondas) y la anotación de la plataforma GPL2025 (1,51 MB, 23.850 sondas anotadas de 57.381) y se buscó por expresión regular la anotación de componentes de silenciamiento: 46 sondas candidatas únicas (17 de Argonauta/PIWI/PAZ, 5 de Dicer, 5 de RDR y 19 de otros), todas presentes en la matriz. La lista no está curada y puede tener falsos positivos (por ejemplo, un gen «phytolongin» entró por texto de anotación). Esto prueba que un chequeo de cobertura es posible en minutos en una notebook; **no se calculó expresión ni se hizo ningún análisis**. Descarga total de datos de expresión: 4,3 MB; el tope de 1 GB no se tocó (el total descargado de metadatos y listados fue de unos 200 MB, estimado).

**Lo que no se pudo medir.** El contenido de cualquier archivo del OSDR (el host de almacenamiento al que redirige la descarga devolvió 403 del proxy) y el archivo de maíz de PRJDB11348. Por eso los tamaños de las tablas de conteos salen de los listados de archivos de OSDR y no de una descarga.

**Qué responden las opciones.** La pregunta que el prompt plantea de ejemplo, si los componentes del silenciamiento de la planta cambian de expresión en vuelo en un cereal, es contestable en tamaño con arroz (GSE78839) y con *Arabidopsis* (OSD-437, OSD-678, OSD-427, OSD-120, OSD-37), no con maíz, y exige controles calibrados (conjuntos aleatorios igualados en expresión y permutación de etiquetas) por el tamaño de los grupos (4, 3 y 3 en el arroz). Cambios de expresión de la maquinaria no son cambios de eficacia de un dsRNA exógeno, y M2 informa un único experimento primario de RNAi en vuelo (*C. elegans*, sin cambios en 16 genes de la maquinaria).

---

## 5. Encaje con el track y con L1 a L3

| opción | pregunta oficial del track | L1 priorización auditable | L2 validación retrospectiva | L3 riesgo off-target | innovación abierta | horas de 96 `[H]` |
| --- | --- | --- | --- | --- | --- | ---: |
| 1. Paquete de vacío documentado | no | no | no | no | sí: datos y consulta reutilizables, resultado negativo documentado | 4–6 |
| 2a. Silenciamiento y defensa, mínima | no | no | no | no | sí: cuaderno reproducible | 10–12 |
| 2b. ampliada | no | no | no | no | igual que 2a, más costosa | 24–30 |
| 3. Extensión a maíz | no | no | no | no | igual que 2a | +8–12 |
| 4 a 7 (descartadas) | no | no | no | no | no | 0 |

Con franqueza: nada de este eje entra en la pregunta oficial del track (priorizar y validar ARN exógeno contra el insecto y los patógenos que transmite), y nada alimenta L1, L2 ni L3. L2 necesita datos de eficacia de RNAi en hemípteros, que los datos de vuelo no tienen; L1 necesita candidatos y evidencia de eficacia, que tampoco; y L3 necesita transcriptomas de organismos no objetivo del agroecosistema del maíz, que el OSDR solo tiene en el caso de los parasitoides de *Drosophila*, no de *Dalbulus* (ver «Si vale la pena y no está pedido»). Este eje aporta, como máximo, apertura y un resultado negativo bien documentado.

---

## Contradicciones con el repo

| qué dice el repo o el prompt | dónde | qué dice mi fuente | fuerza |
| --- | --- | --- | --- |
| La ruta `https://osdr.nasa.gov/osdr/data/osd/meta/OSD-<n>` entrega los metadatos de un estudio. | prompt de M5, «datos prácticos ya verificados» | Con el prefijo `OSD-` devuelve `hits: 0` para todos los estudios probados (375, 622, 751, 118, 37); funciona con el número solo (`/meta/375`). | `[R]`, probado directamente el 2026-10-19; M5-01, M5-03 |
| «El maíz aparece solo para auxina (STS-95), mutagénesis de semillas y gravedad simulada con regolito.» Y «no hay medición de defensa ni de silenciamiento en *Zea mays* en vuelo real». | `research/R7_microgravedad/M3_plantas_insectos_patogenos/REPORT.md`, veredicto | Existe un microarray de maíz etiolado en la ISS (PRJDB11348), de un experimento de auxina de 2016–2017, que M3 no registra. No contradice «solo auxina», pero hace que el maíz tenga un transcriptoma de vuelo de genoma completo en el que, en principio, se podrían leer genes de silenciamiento o de defensa; su cobertura y acceso no están verificados. | `[?]`; M5-05, M5-20 a M5-22 (solo resúmenes) |
| «Ningún estudio mide Dicer, Argonauta o RDR de forma dirigida en una planta en vuelo» y «DCL, AGO y RDR en GeneLab: no evaluado». | M3, REPORT.md | Coincide. Este reporte añade que en el OSDR no hay archivos de ARN pequeño de plantas y que los conteos de varios estudios de *Arabidopsis* pesan de 2 a 7 MB, de modo que el chequeo es barato en tamaño; no se ejecutó. | `[R]`; M5-02 |
| 42 estudios de *Arabidopsis* en GeneLab. | M3, `busquedas.md` (consulta por término) | 61 estudios del OSDR tienen *Arabidopsis thaliana* en el campo organismo del volcado completo (más algunos mixtos). La diferencia probablemente se deba al término de consulta. | `[?]`; M5-01 |
| SINTESIS_V2: «no hay transcriptoma público de … parasitoides de *Dalbulus*». | `SINTESIS_V2.md`, sección (b) | Sigue siendo cierto. Matiz: el OSDR tiene dos transcriptomas de avispas parasitoides (*Leptopilina*), pero de parásitos de *Drosophila*. | `[R]`; M5-01 |

No hay contradicción con D1, D7 ni D8; este reporte las confirma (ver §5 y opciones 5 a 7). Tampoco con R1 §4 ni con R6 sobre la ausencia de maquinaria de RNAi en los dos mollicutes: no se reabrió.

---

## Qué no se pudo establecer

1. **Contenido de los datos del OSDR.** Ningún archivo de datos se descargó: la descarga redirige a un host de almacenamiento (`genelab-repo-prod.s3.amazonaws.com`) que el proxy bloquea; tampoco son alcanzables la API de GeneLab ni la de visualización. Por eso no se sabe si los arrays de trigo (OSD-622) tienen sondas de silenciamiento, ni se verificó una sola tabla de conteos.
2. **Maíz de PRJDB11348.** No se localizó el archivo (NCBI no enlaza a GEO, SRA ni BioSample, y el DDBJ está fuera de la lista permitida), ni su licencia, ni la anotación de las sondas.
3. **Vínculos inferidos.** Que PRJDB11348 sea el microarray del experimento «Auxin Transport» y que GSE78839 sea el experimento de callos de arroz de Shenzhou son inferencias por coincidencia de diseño, no confirmadas por un accesión citado.
4. **Otros repositorios de vuelo.** No se consultaron datos depositados en repositorios chinos, de ESA o de JAXA, ni la copia del OSDR en el Registro de Datos Abiertos de AWS (M5-42), ni NASA NTRS para datos.
5. **Ceros por taxid.** El índice del OSDR no expone taxid; los ceros son por campo de organismo y texto, y por consulta con nombre científico en NCBI. Un cero así no es una ausencia demostrada.
6. **Clasificación real o simulada.** Es heurística (tipo de proyecto, misión, plataforma y texto del registro) con revisión manual de los casos de borde; algunas entradas de «ARN pequeño» se clasificaron sin leer el artículo.
7. **Licencias.** Solo se vio CC0-1.0 en dos registros (fragmentos); no se revisó cada uno de los 155 estudios del inventario.
8. **Profundidad de lectura.** De las 44 fuentes, 3 se leyeron completas (registros de base de datos), 19 de forma parcial, 13 solo en resumen y 9 solo como fragmento del buscador. Herranz et al. (2013) y Nickerson et al. (2024) solo en resumen; los tres artículos del experimento de maíz en la ISS, solo en resumen.
9. **Horas.** Todas las horas-persona son estimaciones del equipo `[H]`, no mediciones.
10. **Efecto de la microgravedad sobre el RNAi exógeno.** No hay dato de vuelo que permita contestar si la eficacia de un dsRNA exógeno cambia; M2 encuentra un único experimento primario de RNAi en vuelo, en un nematodo.

---

## Si vale la pena y no está pedido

Dos cosas que no hice. La primera, una consulta por *Leptopilina* (avispas parasitoides de *Drosophila*, OSD-609 y OSD-610: 8 muestras cada una, 65 y 55 GB crudos, tablas procesadas de 44,5 y 32,6 MB) como sustituto distante de enemigos naturales para un cribado de off-target en L3 `[H]`: SINTESIS_V2 identifica la falta de transcriptomas de parasitoides de *Dalbulus* como el hueco principal de L3, y estos son de otro hospedador; las lecturas ya están, además, en las bases de secuencias generales, de modo que el OSDR no aporta acceso adicional. La segunda, si se decide ejecutar la opción 2 o la 3, pedir al orquestador acceso a `genelab-repo-prod.s3.amazonaws.com` y a `ddbj.nig.ac.jp`; hoy esas dos opciones quedan en «medido solo por listados».
