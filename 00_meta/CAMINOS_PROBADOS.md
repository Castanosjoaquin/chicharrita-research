# Caminos probados

Qué se intentó, qué se descartó y por qué. Un descarte bien documentado vale
tanto como un hallazgo: evita que el equipo vuelva a gastar horas en algo que ya
se cerró, y es material directo para la defensa ante el jurado, que casi siempre
pregunta por qué no se hizo lo otro.

Formato de cada entrada: qué se intentó, qué pasó, estado (`descartado`,
`descartado por ahora`, `en pie`), y qué lo reabriría.

---

## Nivel proyecto

### Competir en el eje de biología y evidencia experimental
**Qué se intentó:** se evaluó como estrategia de participación.
**Qué pasó:** descartado antes de esta sesión. Sin laboratorio húmedo ni
formación formal en biología, no hay forma de producir evidencia experimental
propia en el plazo del evento.
**Estado:** descartado. Ver `DECISIONS.md` D1.
**Qué lo reabriría:** una colaboración con un laboratorio que ya tenga el
bioensayo andando y quiera un socio computacional. Es una posibilidad para
después del Investigathon, no para el evento.

### Tomar las notas de la charla como punto de partida técnico
**Qué se intentó:** usar directamente lo anotado de la charla del investigador
invitado como descripción del estado del arte y del pipeline de la industria.
**Qué pasó:** descartado al detectar al menos tres puntos dudosos en las notas
—la asignación de síntomas a cada patógeno, la atribución de cálculo
termodinámico a BLAST, y la fusión de "dsRNA exógeno" con "ARN no
codificante"—. Pasaron a ser los supuestos S1, S2 y S3, cada uno con
verificación asignada.
**Estado:** descartado como fuente directa; en pie como mapa de hipótesis.
**Qué lo reabriría:** nada. Son notas de segunda mano de una charla oral; el
valor que tienen es señalar dónde mirar, no afirmar.

---

## Nivel método

Cada camino cerrado dentro de R1 a R5 —un enfoque que no se sostiene, un dataset
que no existe, una herramienta que no corre en una notebook, un modelo cuyos
pesos no están disponibles— se consolida acá con el puntero al reporte que tiene
el argumento completo.

### La idea original de attention: tokens de ARN con la termodinámica de BLAST como loss
**Qué se intentó:** tratar las porciones de ARN como tokens de un modelo de
lenguaje, mirar la atención entre secuencias y usar como función de pérdida
(loss) "el factor de termodinámica que usa BLAST".
**Qué pasó:** descartada tal como fue formulada, por tres razones
independientes, cada una suficiente. Primero, la premisa es falsa: BLAST no
calcula termodinámica, su puntaje son log-odds de sustitución y su E-value es
estadística de similitud bajo un modelo nulo, no un modelo físico. Segundo, la
termodinámica, aun bien calculada con ViennaRNA, no puede ser la loss: es una
variable de entrada (feature). La loss sólo puede ser el fenotipo medido, y no
existen datos de fenotipo en Hemiptera para supervisar nada. Tercero, la
arquitectura está publicada al menos cuatro veces —OligoFormer, AttSiOff,
BERT-siRNA, DeepSipred—, todas con embeddings de RNA-FM y atención, y todas para
siRNA corto en líneas celulares humanas.
**Estado:** descartada. El argumento completo está en
`research/R2_attention_diseno_arn/REPORT.md`, secciones 1 y 2.
**Qué se rescata:** la forma del problema, que es correcta —señal posicional a lo
largo del transcrito—, y la intuición de "ver la relación entre las distintas
secuencias", que se satisface mejor con un perfil posicional explícito del
puntaje que con pesos de atención.
**Qué lo reabriría:** un conjunto de datos de eficacia en Hemiptera con fenotipo
medido y n de tres dígitos. Hoy hay seis construcciones publicadas en la
especie.

### Fine-tuning de un modelo de secuencia sobre datos de eficacia de RNAi
**Qué se intentó:** ajustar un modelo fundacional de ácidos nucleicos sobre datos
de eficacia para predecir knockdown en *Dalbulus maidis*.
**Qué pasó:** descartado por ausencia de datos en el orden correcto de insectos.
El dataset más grande disponible, iBeetle-Base, tiene etiquetas binarias y
groseras, con dosis y vía de administración no controladas entre genes, y es
Coleoptera. Entrenar sobre datos humanos y transferir es precisamente lo que la
evidencia desaconseja: el contenido de GC en las posiciones 9 a 14 del
antisentido **invierte su signo** entre humano e insecto, y la accesibilidad del
ARNm, pilar de la literatura humana, no resultó predictor significativo de
eficacia insecticida.
**Estado:** descartado para el plazo del Investigathón. Es un plan de tesis.
**Qué lo reabriría:** los mismos datos que el punto anterior.

### Generar secuencias nuevas por búsqueda en el espacio de secuencias
**Qué se intentó:** algoritmo genético, búsqueda guiada por gradiente o muestreo
sobre el espacio de secuencias, usando el puntaje como objetivo.
**Qué pasó:** descartado por dos motivos. Técnicamente, el espacio de candidatos
legítimos está restringido a subcadenas del transcrito blanco —por definición del
mecanismo, no se puede inventar secuencia que no esté en el blanco—, y una
ventana deslizante ya es la búsqueda exhaustiva de ese espacio.
Epistemológicamente, si se relaja esa restricción se obtienen secuencias que
optimizan nuestro propio puntaje sin ninguna forma de verificarlas sin
laboratorio: optimizar contra un sustituto (proxy) es el modo de falla clásico.
**Estado:** descartado.

### Proponer una plataforma bioinformática de diseño de ARN con chequeo de off-targets
**Qué se intentó:** considerarlo como posible aporte del equipo.
**Qué pasó:** descartado como novedad. Ya existe y se llama **Apolo Rocket**:
corre en la nube, consume datos de secuenciación masiva, evalúa más de 140
organismos a la vez y emite reportes automáticos. La construyó APOLO Biotech con
el IABIMO (INTA-CONICET) y la Fundación Sadosky. Proponérsela a alguien del
EPILAB es proponerle la herramienta que usa todos los días.
**Estado:** descartado como novedad; sigue en pie como baseline a superar o
alimentar. Ver `research/R3_apolo_biotech/REPORT.md`, sección 6.1.
**Qué se rescata:** lo que nadie publicó es el **criterio de agregación** que
convierte esos reportes en un orden defendible. El hueco no es la herramienta:
es la función de decisión.

### Proponer encapsulación del ARN para protegerlo de nucleasas y UV
**Qué se intentó:** considerarlo como aporte posible en el eje de entrega, que es
la barrera que el organizador declara central.
**Qué pasó:** descartado como novedad. Está publicado desde 2017 con al menos
seis químicas distintas: BioClay con nanoláminas de hidróxido doble laminar,
quitosano, policationes en estrella, liposomas, cápsulas peptídicas y
minicélulas anucleadas. Además, la entrega controlada por nanotecnología es el
objetivo declarado y financiado de la cátedra AXA del fundador de APOLO para
2025-2029.
**Estado:** descartado como novedad, y además el cuello de botella es
experimental y de capital, no computacional: ninguna cantidad de cómputo decide
si un portador sobrevive al intestino medio del insecto a campo.
**Qué se rescata:** los datos de persistencia y eficacia de portadores publicados
**no son comparables entre sí** —vienen de especies, cultivos, dosis y
laboratorios distintos—. Construir ese conjunto curado y normalizado sí es
trabajo de datos puro.

### Proponer la co-entrega de dsRNA contra la dsRNasa del insecto
**Qué se intentó:** considerarlo como solución a la barrera de nucleasas.
**Qué pasó:** descartado como novedad. Ya está publicado en 2023 por el grupo de
María Inés Catalano (CEBIO-UNNOBA / CIT NOBA): identificaron tres ribonucleasas
de doble cadena en *Dalbulus maidis*, señalaron *Dmai-dsRNase-2* como la más
expresada en intestino medio y glándulas salivales, y mostraron que silenciarla
mejora la respuesta al dsRNA dirigido al gen de interés, proponiendo la
co-administración.
**Estado:** descartado como novedad. Lo que queda abierto —si esa co-entrega
funciona por una vía aplicable a campo— es la pregunta textual del organizador y
es experimental.

### Incluir la accesibilidad del sitio blanco con peso alto en la función de puntuación
**Qué se intentó:** usar la accesibilidad del sitio blanco como término central,
que es lo que hace la literatura humana y lo que haría cualquiera que lea el
campo sin mirar los datos de insectos.
**Qué pasó:** descartado como término con peso. El único experimento controlado
en insectos lo contradice dos veces: no significativo en el ensayo de siRNA
individuales y P = 0,41 en el de dsRNA largo. Se calcula y se reporta para
trazabilidad y para la ablación, pero entra con peso cero por defecto.
**Estado:** en pie como variable reportada, descartado como término ponderado.
Es uno de los puntos donde una propuesta nuestra se diferencia de aplicar una
herramienta existente a ciegas.

### Resolver el tamizaje de off-target con un modelo fundacional en lugar de alineamiento
**Qué se intentó:** evaluarlo como alternativa a contar coincidencias con Bowtie.
**Qué pasó:** descartado con evidencia directa. En BEACON, el benchmark
independiente de trece tareas de ARN, la tarea de efecto fuera de blanco de
CRISPR —la más parecida que está medida: predecir desde secuencia la
consecuencia de un apareamiento imperfecto— da correlación de Spearman de 12,6
para el método específico y 11,40 para una red convolucional entrenada desde
cero, contra 2,49 a 5,00 para *todos* los modelos de lenguaje de ARN evaluados.
RNA-FM, el más usado como fuente de representaciones en este campo, queda último.
**Estado:** descartado. El índice se construye sobre alineamiento y conteo
ponderado, que además es auditable. Ver `research/R4_frontier_ml_rna/REPORT.md` y
la línea L3 de `lineas_de_ataque.md`.

### Diseño generativo o inverso de secuencias de ARN
**Qué se intentó:** considerar la generación de secuencias nuevas, con el
antecedente de que la técnica funciona y tiene validación húmeda: gRNAde igualó a
expertos humanos en una competencia ciega y logró 31,5 % de variantes activas de
una ribozima contra 15,0 % del diseño racional filtrado.
**Qué pasó:** descartado por **asimetría del ensayo**. Esos resultados se pudieron
validar porque existía una biblioteca de alto rendimiento con lectura de
actividad sobre casi dos mil secuencias. En RNAi de insecto la lectura es un
bioensayo de mortalidad con decenas de individuos por tratamiento. Sin
laboratorio y sin ensayo de alto rendimiento, generar secuencias produce
candidatos que nadie puede evaluar.
**Estado:** descartado, y coincide con el descarte que R2 ya había hecho por la
vía de la búsqueda en el espacio de secuencias.

### Aprendizaje automático para formulación y entrega
**Qué se intentó:** buscar activamente, por ser el cuello de botella que declara
el organizador, si existe algo aplicable del lado computacional.
**Qué pasó:** descartado. Lo que hay son modelos de eficiencia de transfección de
nanopartículas lipídicas para terapéutica humana, evaluados sobre unas 1.100
estructuras de lípido ionizable derivadas de un único conjunto en una línea
celular, cuya generalización fuera de ese conjunto no está demostrada ni en la
propia fuente. Y el objetivo de optimización es otro: resistencia a nucleasas
intestinales y paso del epitelio, no transfección de una línea celular.
**Estado:** descartado. **Qué se rescata:** la vía de entrega sí se puede atacar
desde la secuencia, con un disparador quimérico que incluya un tramo contra las
dsRNasas del propio insecto; entra como módulo opcional, no como línea propia.

### Automatizar la extracción de datos de la literatura para armar el conjunto de validación
**Qué se intentó:** reemplazar el curado manual de papers —que es el costo
principal de la validación retrospectiva— por un sistema de extracción asistida.
**Qué pasó:** descartado como reemplazo, con números. El mejor sistema publicado
alcanza 85,2 % de precisión contra 73,8 % de anotadores con doctorado, pero su
exactitud es 66,0 % contra 67,7 %: la diferencia es significativa en precisión y
**no lo es en exactitud**, y la precisión superior se consigue absteniéndose en el
21,9 % de los casos. Su sistema de resúmenes deja 13,5 % de afirmaciones citadas
y no sostenidas, una de cada siete, que es incompatible con la regla número uno de
este repositorio.
**Estado:** descartado como sustituto; **en pie como triador** para encontrar y
preseleccionar los trabajos candidatos. El curado sigue siendo humano.

### Construir un tablero de exploración como artefacto principal
**Qué se intentó:** considerarlo como el entregable del eje de desarrollo
computacional.
**Qué pasó:** descartado por dos razones convergentes. El organizador dice,
textual, que un equipo no debería ganar por construir la interfaz más vistosa
sino por producir la mejor decisión científica posible. Y las tres herramientas
publicadas del campo muestran dónde está el valor: si-Fi corre sólo en Windows
con Python 2.7, dsRIP es web y hay que exportar su salida para versionarla, y
dsRNAEngineer publica su stack pero su valor real son los 942 transcriptomas
precargados. El valor está en los datos y en la decisión, no en la pantalla.
**Estado:** descartado como artefacto principal. La herramienta puede tener una
vista de lectura, pero el argumento es la ficha de decisión por candidato.

### Depender de si-Fi dentro del pipeline
**Qué se intentó:** usar la herramienta establecida de diseño de ARNdc como
componente.
**Qué pasó:** descartado como dependencia. Corre sólo en Windows 7 o superior,
con interfaz en Python 2.7 y Qt4: no corre en las máquinas del equipo y rompe la
reproducibilidad. Se reimplementan sus reglas de selección de hebra guía con
ViennaRNA y Bowtie, que es lo que el propio artículo describe.
**Estado:** descartado como dependencia; **en pie como línea de base** a la que
compararse, asumiendo la fricción de hacerlo correr una vez.
**Actualización 2026-10-19:** la línea de base ya está construida y no requiere la
herramienta original. El instalador de si-Fi21 trae `bowtie.exe` 0.11.3 y
`RNAplfold.exe` 2.1.5 como ejecutables de línea de comandos, y el criterio está
portado a Python 3 en `tools/sifi21_port/`. La decisión de no depender del
programa original se mantiene; lo que cambia es que ahora hay con qué compararse.

### Ensamblar el transcriptoma de *Dalbulus maidis* de novo
**Qué se intentó:** ensamblar desde las corridas públicas de RNA-seq, que R2
había identificado como el camino crítico del proyecto.
**Qué pasó:** descartado por innecesario y por costo. El ensamblado ya está
publicado y depositado: 56.116 transcriptos en el TSA `GITV00000000`, con 82,4 %
de completitud BUSCO. Ensamblar de nuevo 1.727 millones de lecturas, a razón de
aproximadamente 1 GB de RAM por millón, es inalcanzable con el equipamiento del
equipo y no agrega nada.
**Estado:** descartado. Se descarga, se congela y se corre TransDecoder para
obtener los marcos de lectura. El camino crítico que R2 declaraba **deja de
serlo**, y eso cambia el plan: es el tipo de corrección que justifica haber
hecho las cinco investigaciones en paralelo y no en serie.

### Buscar el genoma del fitoplasma del maíz por su nombre informal
**Qué se intentó:** localizar en el NCBI el genoma del fitoplasma del complejo de
achaparramiento buscando por nombre común y por *Candidatus* Phytoplasma asteris.
**Qué pasó:** llevó a una conclusión falsa que estuvo escrita en el repositorio:
que *Spiroplasma kunkelii* era el único patógeno del complejo con genoma completo
y anotado. El genoma del fitoplasma existe desde 2016 —`GCA_001712875.1`, cepa
M3, 576.118 pb en una sola secuencia, aislado de un *Dalbulus maidis* colectado
en Piracicaba en 2013— y se había escapado por nomenclatura: el taxón recibió
nombre formal recién en 2026, '*Candidatus* Phytoplasma zeae'.
**Estado:** corregido. **La lección operativa:** en bases taxonómicas hay que
buscar por taxón y por accesión, no por nombre común, y hay que revisar si el
nombre cambió. Queda como advertencia para la rama de datos.

---

## Nivel corpus — lo que la ola 2 deja cerrado (2026-10-17)

### Ensamblar el transcriptoma del vector desde las corridas públicas
**Qué se intentó:** la ola 1 lo declaró el **camino crítico** del proyecto y le
asignó cuatro días-persona, porque daba por inexistente el transcriptoma de
*Dalbulus maidis*.
**Qué pasó:** descartado por innecesario, esta vez con la verificación hecha. Hay
**tres** transcriptomas TSA descargables —`GITV00000000` con 56.117 secuencias,
`GHCC00000000` con 55.286 y `GCWP00000000` con 25.662—, y además el grupo que
publica en la especie usa un cuarto, propio y no publicado. La ola 1 conocía sólo
el primero y lo daba por no depositado.
**Estado:** descartado. El camino crítico deja de serlo y libera el presupuesto
de tiempo más grande del plan.
**Qué lo reabriría:** que el laboratorio necesite un ensamblado con criterios
propios, o que los tres públicos resulten insuficientes para las regiones de
interés.

### Tomar el conteo de off-target de la herramienta oficial como medida de riesgo
**Qué se intentó:** usar el número que devuelve dsRNA-Engineer como el término de
seguridad del scoring.
**Qué pasó:** descartado como medida directa, al desagregarlo contra los archivos
crudos de una corrida real. El conteo **está dominado por la condición de 16 pb**
—70 de 70 aciertos en maíz y 67 de 67 en abeja vienen de ahí, ninguno del tamaño
de corte de Dicer-2 que la propia herramienta declara relevante— y **mezcla
ventanas riesgosas con parálogos alcanzados**: los 70 de maíz son 28 posiciones
distintas de la consulta repartidas en 60 transcriptos.
**Estado:** descartado como número; **en pie como insumo**, una vez desagregado.
Esa desagregación es ahora uno de nuestros entregables.

### Usar el conteo on-target de la herramienta como verificación del blanco
**Qué se intentó:** leer los aciertos dentro del organismo blanco como evidencia
de que el candidato efectivamente apunta a su gen.
**Qué pasó:** descartado. El *D. maidis* de la herramienta es un ensamblado de
novo de **una sola corrida pública** (SRR15166998, Trinity), y los 190 aciertos
perfectos de una corrida real cayeron todos en un contig que cubre 210 de los 615
nt de un ARNm publicado. Ese conteo **mide cobertura de ensamblado, no identidad
de blanco**.
**Estado:** descartado.

### Reproducir la columna «Nro de eficientes por gen» con criterios publicados
**Qué se intentó:** ingeniería inversa del criterio con el que EPILAB clasificó
siRNA como eficientes, reimplementando localmente los criterios de la literatura.
**Qué pasó:** no se logró. Contra los 114, 35, 199 y 33 declarados, la
reimplementación da 87/21/136/26 contando una hebra y 179/43/259/62 contando
cualquiera, y **ninguna de 2.132 combinaciones de parámetros** reproduce los
cuatro números. W2 agrega por qué: dsRNA-Engineer **no clasifica siRNA como
eficientes**, cuenta aciertos.
**Estado:** descartado por ahora, y convertido en la primera pregunta técnica
para el investigador.
**Qué lo reabriría:** que nos digan la herramienta y la versión.
**Actualización 2026-10-19: el descarte se refuerza, ahora con la herramienta.**
Ya sabemos la herramienta —el investigador confirmó en el checkpoint que si-Fi21
es la base— y sigue sin reproducirse. Con un port fiel del programa, **ninguna de
15.120 configuraciones** (3 temperaturas × 2 versiones de ViennaRNA × 2 modos ×
21 ventanas de accesibilidad × 5 umbrales de extremos × 6 de accesibilidad × regla
terminal sí/no) reproduce a la vez los 114 de `MP_MRFV_full` y los 35 de
`CP_MRFV_full`. Antes falló nuestra reimplementación de los criterios publicados;
ahora falla el programa mismo. Medición completa en
`research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md`.
**Qué lo reabriría:** que nos pasen la versión modificada que usó el laboratorio
(el investigador dijo que cambió parámetros), o la base de datos de la corrida —el
conteo del original suma un registro por hit de Bowtie, no un siRNA único, así que
depende de la base.

### Correr si-Fi21 para comparar criterios
**Qué se intentó:** usarlo como línea de base, como preveía la ola 1.
**Qué pasó:** descartado en este entorno. Es un binario de Windows con interfaz
gráfica y no es ejecutable acá, lo que la ola 1 ya sospechaba y ahora está
confirmado en la práctica.
**Estado:** descartado como dependencia; se reimplementan sus reglas, que el
propio artículo describe.
**Reabierto y resuelto, 2026-10-19.** El descarte era correcto en cuanto a la
interfaz gráfica y equivocado en cuanto al cálculo. Dos cosas lo reabrieron: el
instalador se puede correr en la máquina Windows del equipo, y **trae los dos
motores de cálculo como ejecutables de línea de comandos** (`bowtie.exe` 0.11.3 y
`RNAplfold.exe` 2.1.5, en `ToCopy/`), que sí son invocables. Además el fuente está
en GitHub y es legible. Con eso se armó `tools/sifi21_port/`, que corre el criterio
sin interfaz, en dos modos: fiel al original y corregido.
**Lección de método:** «es una aplicación gráfica» no implica «su cálculo es
inalcanzable». Conviene mirar qué binarios empaqueta un instalador antes de
descartarlo.

### Subir las secuencias de EPILAB a dsRNA-Engineer o al BLAST web
**Qué se intentó:** nada: quedó vedado de entrada por la regla de
confidencialidad del corpus.
**Qué pasó:** se corrió todo con BLAST+, Bowtie y ViennaRNA locales, y la corrida
del servicio se hizo con una secuencia pública de referencia. El servicio, además,
**no declara licencia, no publica código y no documenta política de retención**,
lo que confirma que la regla era la correcta.
**Estado:** descartado de forma permanente. No es una limitación técnica: es una
condición del trabajo.

### Diseñar sobre la secuencia de referencia de un virus sin mirar los aislados
**Qué se intentó:** nada todavía, y por eso entra acá antes de que alguien lo
haga.
**Qué pasó:** el caso real apareció medido en el propio corpus. La región de
cápside elegida por EPILAB es 100 % idéntica **sólo al aislado de Costa Rica**;
contra los 45 registros brasileños la identidad cae a 91,5-93,5 % y la mediana de
siRNA de 21 nt con apareamiento perfecto es **44 de 180**. Y en GenBank no hay
ninguna secuencia argentina de MRFV.
**Estado:** descartado como práctica. Todo candidato antiviral se evalúa contra el
conjunto de aislados disponibles, no contra una referencia.

### Buscar genomas en el NCBI por nombre común
**Qué se intentó:** localizar el genoma del fitoplasma del achaparramiento
consultando por «maize bushy stunt phytoplasma».
**Qué pasó:** devolvió cero y llevó a afirmar, dentro de esta misma ola, que el
agente no tenía genoma secuenciado. Es falso: consultado **por taxid**, el 202462
devuelve dos ensamblados del genoma completo de 576.118 pb.
**Estado:** descartado como método. Se resuelve el taxid primero y después se
consulta; el script de consulta del repositorio ya lo hace así.
**La lección, que vale más que el caso:** un cero devuelto por una consulta por
nombre no es una ausencia.


---

## Nivel corpus — lo que R6 deja cerrado (2026-10-17)

### Tomar S44 como prueba de que ninguna estrategia apunta al patógeno
**Qué se intentó:** usar la revisión de Balog et al. (2026) como respaldo de que todas las estrategias contra fitoplasmas apuntan al vector o a la planta.
**Qué pasó:** en el texto completo es una revisión de manejo de vectores y no menciona antibióticos ni tetraciclinas; esos sí actúan sobre el fitoplasma dentro de la planta (aunque no sean aplicables a campo). Lo que S44 respalda es que *en la literatura de manejo de vectores* ninguna estrategia apunta al patógeno.
**Estado:** descartado como respaldo de la frase general. **Qué lo reabriría:** una revisión de alcance más amplio que diga lo mismo.

### Dar por correcta la corrección B5 sin mirar la figura
**Qué se intentó:** aceptar que en *D. maidis* los dos genes dejaron 10 % de supervivientes.
**Qué pasó:** la figura 5A mide ≈17,5 % para *eth* (día 4); el texto dice 10 % (día 5). Se confirma el resto de B5.
**Estado:** descartado como cifra única; queda con rango 10 a 17,5 % hasta que el autor aclare. **Qué lo reabriría:** respuesta del autor (pregunta 3 de R6).

### Leer valores de figuras desde una descripción automática de un buscador
**Qué pasó:** la descripción devuelta por un buscador para la figura 5 no coincidía con las barras reales medidas en píxeles. Las cifras de figuras se leen del PDF.
**Estado:** descartado como método.

### Predictores locales de péptido señal y transmembrana en este entorno
**Qué se intentó:** SignalP, TMHMM, Phobius (licencia y registro) y DeepSig 0.9 (instalado desde PyPI sin modelos; los modelos están en GitHub, no alcanzable).
**Qué pasó:** ninguno corrió. Ver `research/R6_estrategias_molicutes/datos/COMANDOS.md` §7.
**Estado:** descartado por ahora. **Qué lo reabriría:** acceso a GitHub o una licencia académica.

### Diseñar o variar efectores (SAP11, SAP54) para aumentar su función
**Qué se intentó:** nada; entra acá antes de que alguien lo haga.
**Qué pasó:** queda fuera de alcance, sin excepción: aumentaría la virulencia, la transmisibilidad o el rango de hospedadores. El trabajo sobre efectores sólo es válido en modo defensivo (inventario y candidatos a inhibición).
**Estado:** descartado de forma permanente. No es una limitación técnica: es una condición del trabajo.

---

## Nivel herramienta — el port de si-Fi21 (2026-10-19)

### Dar por desactualizadas las tablas termodinámicas de si-Fi21
**Qué se intentó:** aplicar una lista de «parámetros químicos a actualizar» que
asumía que si-Fi usa las tablas de Freier et al. (1986) y Xia et al. (1998), y que
calcula a 37 °C como las herramientas de cultivo de mamífero.
**Qué pasó:** descartado al abrir el fuente. `free_energy.py:278` declara
`nn_table=RNA_NN3`, que es **Chen et al. 2012**, o sea las tablas modernas. Las
viejas están definidas en el archivo pero no se usan, y de ahí sale la confusión. Y
la temperatura está fijada en **22 °C** en dos lugares independientes
(`free_energy.py:420` y `sifi_pipeline.py:62`), no en 37. Los dos cambios más
prominentes de la lista ya estaban hechos en el programa.
**Estado:** descartados los dos. **Lección de método:** un diagnóstico de software
razonado desde el artículo y la época de la herramienta acierta donde el
razonamiento general aplica y falla donde hacía falta abrir el archivo. Se abre el
archivo.

### Cambiar la corrección salina de si-Fi para acercarla al medio intracelular
**Qué se intentó:** agregar Mg²⁺ y llevar la fuerza iónica a condiciones
fisiológicas, sobre el supuesto de que el original calcula a 1 M de NaCl.
**Qué pasó:** descartado por dos razones. El original ya aplica corrección salina a
~70 mM de monovalentes (`Na=20, K=50, saltcorr=5`). Y cambiarla **no puede mover
ningún veredicto**: el método 5 es `0.368·(len−1)·ln(mon)`, función solo del largo,
y si-Fi nunca usa un ΔG absoluto —compara dos ventanas de 3 nt del mismo largo—, así
que la corrección se cancela exacto en la resta. Verificado como test.
**Estado:** descartado como cambio con efecto. El parámetro sigue expuesto, con la
aclaración de que no hace nada en esta ruta de cálculo.

### Sustituir las tablas de mismatch de ADN por equivalentes de ARN
**Qué se intentó:** arreglar una inconsistencia química real del original, que usa
`DNA_IMM1` y `DNA_TMM1` (Allawi & SantaLucia 1998, ADN/ADN) dentro de un cálculo
por lo demás de ARN, de modo que un par G-U no se trata como wobble.
**Qué pasó:** no se hizo, por dos motivos. Primero, sustituirlas exige parámetros
de mismatch de ARN publicados y verificados, y no hay ninguno abierto: inventarlos
o trasladarlos de memoria viola la regla de evidencia. Segundo, se midió si hacía
falta: se instrumentó el contador de consultas a esas tablas y en los cuatro casos
corridos dio **cero**. En la ruta que si-Fi usa para la eficiencia, las claves de
mismatch no se alcanzan nunca.
**Estado:** no corregido, instrumentado y documentado. El defecto existe y no
afecta a este uso. **Qué lo reabriría:** extender el cálculo a secuencias
desapareadas, o conseguir las tablas de ARN de una fuente que se pueda abrir.

### Tomar un acierto numérico en un solo gen como reproducción del criterio
**Qué se intentó:** nada todavía, y por eso entra acá antes de que alguien lo haga.
**Qué pasó:** el caso apareció medido. El modo corregido con el RNAplfold del
instalador da **exactamente 114** en `MP_MRFV_full`, que es el número declarado por
EPILAB. Parecía la respuesta. Esa misma configuración da 25 en `CP_MRFV_full` contra
35 declarados: era coincidencia. Con un espacio de 15.120 configuraciones y
conteos de dos o tres cifras, los aciertos aislados son esperables.
**Estado:** descartado como criterio. **La regla operativa:** una configuración vale
solo si reproduce **todos** los conteos a la vez, y si además cae cerca de los
valores por defecto. Casi-aciertos dispersos en parámetros mutuamente
incompatibles son firma de casualidad, no de hallazgo.

### Explicar la elección de regiones de EPILAB por el perfil de off-targets
**Qué se intentó:** la hipótesis del propio investigador. Dijo que en teoría debió
elegir las regiones con más siRNA eficientes, que tal vez no lo hizo y que quizá
fue por off-targets, pero que no lo recordaba.
**Qué pasó:** descartada, y en un gen refutada. Con el tamizaje exacto de 21 nt
contra seis referencias: en `CP_MRFV` el gen entero tiene **cero** off-targets, así
que no había nada que optimizar; en `MP_MRFV` y `ATPaseD_Dm` la exposición de la
región elegida es **idéntica** a la de la mejor región (6 y 6; 7 y 7); y en
`BicC_Dm` la región elegida es a la vez **menos eficiente y once veces más
expuesta** —20 eficientes y 33 ventanas con off-target, contra 37 y 3 de la región
2123-2422—, o sea que la alternativa domina en los dos ejes y no hay compromiso que
justifique la elección.
**Estado:** descartada como explicación. Las cuatro regiones están entre un 19 % y
un 46 % por debajo del óptimo por densidad y eso no se explica por seguridad.
**Qué lo reabriría:** un criterio que no hayamos medido —conservación entre
aislados virales, accesibilidad para la construcción, restricciones de clonado— o
que el investigador recuerde el motivo. Medición en
`research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md` §4.

### Usar BLAST para contar coincidencias de 21 nt con un desajuste
**Qué se intentó:** reutilizar los conteos de «21 nt con 1 desajuste» que W5 produjo
con `blastn -task blastn-short -word_size 11`.
**Qué pasó:** descartado como completo. Son subestimaciones, por hasta un factor de
tres: 5 contra 16 reales en `BicC_Dm`, 9 contra 17 en `ATPaseD_Dm`. La causa es
identificable y no es un error de parámetros: un 21-mero cuyo único desajuste cae
en la posición 11 deja dos bloques exactos de 10 nt, y con `word_size 11` BLAST no
tiene semilla con la que encontrarlo.
**Estado:** descartado para el criterio de un desajuste; **en pie** para los
criterios de bloque perfecto, donde coincide exacto con la enumeración en las 20
celdas comparadas. Para un desajuste se enumeran las 63 variantes por ventana.
**Lección de método:** un umbral de identidad no sustituye al tamaño de semilla.
BLAST no puede encontrar lo que no puede sembrar.

### Comparar conteos de eficientes por región entre procedimientos distintos
**Qué se intentó:** nada todavía, y por eso entra acá antes de que alguien lo haga.
**Qué pasó:** hay dos procedimientos y **no son comparables**. Recortar la región y
correrla sola —que es lo que describió el investigador— da 16 eficientes en la
región 1-200 de `MP_MRFV`; contar las mismas ventanas dentro de la corrida del gen
entero da 30. Una diferencia del 47 % sobre el mismo tramo de secuencia. La causa
es el término de accesibilidad: RNAplfold evalúa plegado local y un fragmento
recortado pierde el contexto de sus extremos.
**Estado:** descartado comparar números de procedimientos distintos. Hay que fijar
uno y declararlo. Para llenar la planilla se usa el aislado, que es el que el
investigador describió.

## Nivel herramienta — el criterio de un desajuste y los gráficos (2026-10-19)

### Dar por cerrado el riesgo en polinizadores con el criterio de bloque perfecto
**Qué se intentó:** concluir «cero coincidencias en *Apis mellifera* en los cuatro
genes», que es cierto con el criterio de bloque contiguo perfecto de ≥19 nt.
**Qué pasó:** descartado como formulación. Al correr el criterio de un desajuste
sobre los genes completos, *Apis* **no** da cero: `MP_MRFV` tiene 7 ventanas,
`BicC_Dm` 7, `CP_MRFV` 2 y `ATPaseD_Dm` 1. Son coincidencias más débiles, pero
existen.
**Estado:** la frase defendible es **«sin homología perfecta en abeja»**, no «sin
riesgo en abeja». Y en ningún caso es un ensayo de toxicidad: es ausencia de
homología de secuencia en un transcriptoma de referencia.
**Lección de método:** un cero siempre lleva pegado el criterio con el que se midió.

### Decir que `CP_MRFV` no tiene off-targets
**Qué se intentó:** la conclusión de la versión anterior del informe, basada sólo en
el criterio de bloque perfecto.
**Qué pasó:** descartado. Con bloque perfecto el gen entero da cero, que sigue
siendo cierto y lo vuelve el más limpio de los cuatro. Con un desajuste tiene 14
ventanas, 6 de ellas en maíz.
**Estado:** corregido en el informe y en la página del gen. **Lo que sí se sostiene**
es la conclusión sobre la elección de región: con el criterio principal no hay nada
que esquivar en ningún tramo, así que acá la región no pudo elegirse por off-targets.

### Usar dos colores distintos para los dos niveles de riesgo en los gráficos
**Qué se intentó:** una lane roja para el bloque perfecto y otra naranja o amarilla
para el desajuste, que es la lectura intuitiva de severidad.
**Qué pasó:** descartado por el validador de paleta del skill de dataviz, corrido
contra las superficies reales de estas páginas. Rojo contra naranja da ΔE 10,8 en
visión normal y amarillo contra naranja 13,6, los dos bajo el piso de 15, que es
falla dura y no se excusa con codificación secundaria.
**Estado:** reemplazado por codificación **ordinal**, que además es la correcta:
los dos niveles están ordenados (perfecto > un desajuste), así que es un solo hue en
dos pasos —rojo pleno y el mismo rojo atenuado—, no dos hues. La paleta final
(azul para eficiencia, rojo para riesgo) pasa los seis chequeos en los dos modos y
con todos los pares.
**Lección de método:** cuando dos categorías están ordenadas, dos hues no son sólo
arriesgados: son el trabajo de color equivocado.

### Verificar los gráficos visualmente en este entorno
**Qué se intentó:** abrir los HTML en Chrome para mirarlos, y después rasterizar los
SVG para poder verlos como imagen.
**Qué pasó:** las dos vías fallaron. La extensión de Chrome no respondió en dos
intentos, en dos momentos distintos de la sesión. `cairosvg` no carga porque faltan
las DLL de cairo, y los rasterizadores en Python puro no aplican el CSS externo del
que dependen estos SVG, así que su salida no sería fiel.
**Estado:** verificado **numéricamente** en su lugar: overflow del viewBox, colisión
de etiquetas de banda, cobertura de clases CSS, variables CSS definidas y parseo del
JSON embebido. Los cuatro pasan. **Lo que no está hecho es mirarlos**, y eso queda
anotado como pendiente en `PREGUNTAS_ABIERTAS.md`.
**Qué lo reabriría:** que la extensión de Chrome responda, o instalar las DLL de
cairo.

### Dar por buena la equivalencia del port sin correr el programa original
**Qué se intentó:** sostener las conclusiones del modo fiel sobre la lectura del
fuente, sin ejecutar si-Fi21.
**Qué pasó:** **ya no hace falta: se corrió y coincide.** si-Fi21 original, con su
interfaz y sus valores por defecto, da **471 hits totales y 42 siRNA eficientes**
sobre `ATPaseD_Dm_full`; nuestro port en modo fiel con el mismo RNAplfold da 471 y
42. Además la curva del «RNAi design plot» se reprodujo tramo por tramo: ocho
tramos, mismas posiciones, mismas alturas.
**Estado:** el port queda **verificado contra el original**, no inferido de él, y en
**los cuatro genes**: 42, 32, 133 y 212 eficientes, los cuatro idénticos. Eso
convierte la diferencia entre los dos modos en una medición y no en una hipótesis.
Salidas crudas en `analisis/sifi21_original_*.csv`.
**Hallazgo de paso:** en `BicC_Dm` si-Fi reporta 2.504 hits sobre 2.500 ventanas,
porque cuenta registros de Bowtie y no siRNA únicos y el gen tiene dos pares de
21-meros repetidos. Los cuatro involucrados son no eficientes, así que el conteo no
se infla acá — pero **el mecanismo existe** y con una base de datos que tenga
parálogos sí inflaría. Es evidencia directa para la hipótesis de por qué los
conteos de EPILAB no se reproducen.

### Suponer que «el botón no hace nada» es un problema de instalación
**Qué se intentó:** interpretar que si-Fi no arrancaba el cálculo por una
instalación incompleta o por la máquina.
**Qué pasó:** descartado. Es un bug del programa, reproducido y aislado:
`run_rnaplfold` pasa `cwd=<temporal>` a `Popen` con el ejecutable por nombre pelado,
y en Windows eso rompe la búsqueda del binario. El error termina en un
`UnboundLocalError` que Qt se traga, de ahí el silencio. `run_bowtie` no lo tiene
porque no pasa `cwd`.
**Estado:** resuelto lanzando el programa con los directorios de RNAplfold y Bowtie
en el PATH. **La lección de método:** antes de culpar al entorno, reproducir la
llamada exacta del programa en aislamiento. Tres variantes de la misma llamada —sin
PATH, con PATH, y con ruta completa— localizaron el bug en una línea.

## Nivel R7 — microgravedad (2026-10-20)

Todo lo de abajo viene de `research/R7_microgravedad/`.

### Abrir una línea de cristalización o de estructura en microgravedad para los dos mollicutes
**Qué se intentó:** evaluar si la cristalización de proteínas en microgravedad resuelve el faltante estructural de los blancos de *Ca.* P. zeae y *S. kunkelii*.
**Qué pasó:** de 16 blancos con función documentada, ninguno tiene estructura experimental propia y en ninguno el cuello de botella documentado es el crecimiento del cristal (9 nadie lo intentó, 4 membrana, 1 sin ensayo, 1 sin cultivo, 1 sin faltante). Ninguno cumple las cinco condiciones de la regla de M4 ni las seis de la de M1. No hay estudio que una microgravedad con estos organismos.
**Estado:** descartado. **Qué lo reabriría:** un cristal terrestre deficiente de un blanco concreto, un laboratorio socio y una decisión que dependa de más resolución (preguntas 2 a 4 de R7).

### Usar microgravedad (real o simulada) para validar o seleccionar dsRNA o siRNA
**Qué se intentó:** buscar estudios que lo hayan hecho, en proteínas, ARN, plantas, insectos y patógenos.
**Qué pasó:** ninguno; seis formulaciones de búsqueda con las cadenas registradas. El único experimento de eficacia de RNAi en órbita es CERISE (*C. elegans*), cualitativo y de una misión. La eficacia de un dsRNA no depende de la gravedad a escala molecular `[H]`.
**Estado:** descartado como vía de validación. **Qué lo reabriría:** un estudio que compare la eficacia de silenciamiento entre microgravedad y 1 g con siRNA o dsRNA exógeno.

### Simulación molecular con gravedad alterada y ML de cristalizabilidad
**Qué pasó:** no se halló ninguna simulación ni modelo que use la gravedad como variable; el cálculo de orden de magnitud da una energía gravitatoria de 10⁻⁹ a 10⁻⁷ de la térmica a escala de proteína o ARN. Entrenar un predictor viola D8.
**Estado:** descartado.

### Tomar los porcentajes de «mejora» de los metaanálisis de microgravedad como tamaño de efecto
**Qué pasó:** los metaanálisis (77 a 90 %) cuentan estudios publicados mejorados en al menos una métrica, sin tamaño de efecto ni control del sesgo de publicación, y no se pudieron abrir completos. Las tasas de JAXA dependen del denominador (19 %, 28 % o 5 %).
**Estado:** descartado como respaldo de una cifra. Se citan como conteos de estudios, con el denominador.

### Relanzar una pista rechazada por el filtro de seguridad con otra redacción o con otro modelo
**Qué se intentó:** nada; queda registrado porque pasó (ver `PREGUNTAS_ABIERTAS.md`, sección R7).
**Estado:** no se reformula ni se reenvía desde la sesión que orquesta para esquivar un rechazo (`CLAUDE.md`). Cómo cubrir ese tema es decisión del equipo.

---

## Ranking de candidatos (2026-10-20)

### Descartado: resolver la contradicción del 7,2 % con un argumento en vez de una medición

La salida fácil estaba a mano y era defendible a medias: `pipeline/REPORT.md` §6 mide
la media de un puntaje biofísico continuo y `sifi21_reproduccion.md` §3 cuenta
ventanas que pasan un umbral, así que no son la misma cantidad y no tienen por qué
coincidir. **Eso explica la discrepancia pero no la adjudica**, y el ranking depende
de cuál de las dos manda. Se descartó y se construyó el nulo que faltaba.

Valió la pena por algo que el argumento nunca habría dado: al correr los dos nulos
sobre el mismo dato quedó claro que **la diferencia no está en la cantidad medida
sino en el nulo**. Con el nulo que baraja etiquetas, el efecto de región resiste en
3 de 4 genes; con el nulo de bloques de 30 —el que usó el 7,2 %— en 0 de 4. Si nos
hubiéramos quedado con el argumento, habríamos seguido creyendo que las dos
mediciones miden cosas incomparables, cuando en realidad miden lo mismo con nulos de
exigencia muy distinta.

### Descartado: normalizar los dos ejes contra su máximo teórico

La primera versión del ranking normalizaba la exposición dividiendo por el peor caso
concebible —todas las ventanas pegando en todas las referencias con el criterio más
fuerte—. El resultado fue que la limpieza de los cuatro candidatos quedaba entre
0,98 y 1,00, o sea **sin rango dinámico**, y el orden salía determinado enteramente
por la eficacia. Peor: el barrido de pesos informaba que el orden sobrevivía al
símplex completo, lo que era cierto y **profundamente engañoso**, porque el eje de
exposición había sido aplastado hasta volverse una constante. Un barrido que no
puede mover nada no demuestra robustez: demuestra que el segundo eje no está.

Se reemplazó por dos escalas que se reportan juntas: la **absoluta**, donde los dos
ejes son tasas sobre las ventanas de la región y son directamente comparables, y la
**min-max sobre el conjunto**, que es la convención de `pipeline/motor.py` y le da al
eje de exposición palanca real. La lección, que vale para cualquier ranking que
hagamos: **antes de celebrar que un orden sobrevive al barrido, hay que mirar si los
ejes tienen rango dinámico suficiente para darlo vuelta.** Un barrido sobre un eje
constante es teatro.

### Descartado: leer el 50/50 de los rankings por estrategia como un empate

Con dos candidatos, la normalización min-max manda uno a 0 y el otro a 1 en cada eje,
de modo que si se ordenan al revés en los dos el resultado es exactamente una moneda,
cualquiera sea la magnitud de la diferencia. La primera lectura de la salida fue que
`MP_MRFV` y `CP_MRFV` empataban; no empatan, **la escala borró la diferencia**. Con
escala absoluta `MP_MRFV` gana entre el 90,7 % y el 100 % de los sorteos.

Quedó fijado como prueba en `test_ranking.py` —`test_minmax_con_dos_candidatos_es_degenerado`—
para que nadie lo cite como hallazgo, y escrito en el reporte.

### Descartado: ordenar las regiones vetadas entre sí

La primera implementación de la cascada le daba a toda región vetada el mismo puntaje
y las imprimía ordenadas, lo que las mostraba como un ranking cuando era un empate en
«descartada»: el orden que se veía era el orden de entrada, que no eligió nadie. Se
cambió para que las vetadas se reporten como **lista** y no como posiciones, y para
que el desempate entre puntajes iguales sea por nombre y no por orden de llegada,
que es la convención de `motor.py:rankear`.

### Descartado: atribuir el conteo de dsRNA-Engineer desde sus propios archivos crudos

El plan era bajar el `.tar.gz` con los archivos Bowtie y contar líneas por condición,
como se había hecho en octubre con `PZ371507.1`. En esta corrida
`project/download-file` devolvió el texto `Error!` para los dos proyectos, con GET y
agregando el `uid`. Se probaron cuatro variantes de endpoint y se paró ahí en vez de
seguir sondeando la API.

La atribución se hizo **desde nuestro lado y salió mejor**: corriendo el tamizaje
exacto a k = 16 y a k = 21 sobre las mismas referencias y los mismos ensamblados, el
conteo a 21 es cero en las doce celdas y el de 16 está en la misma escala que el
número que informa el servicio. La conclusión —que el 100 % de su riesgo viene de la
condición de 16 pb— queda demostrada sin depender de que su servicio entregue
archivos. Es una atribución más robusta que la original, porque no depende de leer
sus archivos sino de reproducir su criterio.

### Descartado: correr BLAST de nuevo sobre los cuatro genes

No hacía falta. Las dos mediciones que el benchmark necesitaba ya existían y están
verificadas: el acuerdo exacto en las 20 celdas para los criterios de bloque perfecto
y el desacuerdo por hasta un factor de tres en el de un desajuste, con causa
identificada (`blastn-short` con `word_size 11` no puede sembrar un 21-mero cuyo
desajuste cae en la posición 11). Correr BLAST otra vez habría producido los mismos
números con más ruido en el repositorio.

## Nivel panel y largo de ventana — complemento de W7 (2026-10-20)

### Correr sólo las dos referencias nuevas en vez de rebajar las seis de W7
**Qué se intentó:** contestar si las regiones que W7 recomienda sobreviven a un panel más
grande, sin volver a bajar los 379 MB de referencias originales.
**Qué pasó:** funcionó, y el argumento es que **agregar referencias sólo puede agregar vetos,
nunca sacarlos**, así que para falsar «esta región está limpia» alcanza con las nuevas. Costó
156 MB de descarga y veinte segundos de cómputo. Lo que **no** se puede contestar así es el
puntaje de limpieza completo, que necesita las seis.
**Estado:** vigente. Para rehacer el ranking entero hay que bajar las seis otra vez.

### Dar por bueno el entorno sin verificar que reproduce a W7
**Qué se intentó:** nada; se evitó a propósito. `panel_y_k.py` aborta si los cuatro conteos
de eficientes no son 123, 30, 171 y 29.
**Qué pasó:** el entorno nuevo (venv con ViennaRNA 2.7.2, biopython, pyahocorasick) los
reproduce exacto, y en modo fiel da 142, 39, 223 y 35, que es la columna «fiel + 2.7.2» ya
publicada. Recién con eso se midió algo nuevo.
**Estado:** es la práctica que ya había introducido el port y conviene mantenerla.

### Generalizar la regla terminal de si-Fi21 a 22 nt
**Qué se intentó:** correr el criterio de eficiencia con ventana de 22 nt.
**Qué pasó:** se puede, porque el motor toma `sirna_size`, pero la regla terminal mira el
nucleótido 2 y `sirna[size-3]` —el tercero desde el final—, que a 21 nt es el 19 y a 22 pasa
a ser el 20. Se conservó la **posición relativa** (el extremo 3' de la guía), que es la
lectura mecanicista. Es una decisión nuestra y no una propiedad del original: si-Fi21 no
contempla 22 nt. Queda declarada acá y en el informe.
**Estado:** abierto. Si el investigador tiene la regla del laboratorio para 22, hay que
reemplazarla.

## Ranking v2 (2026-10-21)

### Dar el ancla por buena sin el genoma del vector
**Qué se intentó:** verificar el motor contra W7 con las cinco referencias y humano, sin el genoma de
*D. maidis*.
**Qué pasó:** la ficha de `MP_MRFV` dio una ventana de diferencia (10 contra 11 con off-target) y
la exposición 0,0135 contra 0,0198. Para los genes virales el genoma del vector cuenta como
off-target (D20), así que había que bajarlo (281,7 MB) y correrlo. Con él, los cuatro conteos,
las cuatro fichas y el barrido de 2.000 sorteos coinciden exacto.
**Estado:** descartado como atajo; `ranking_v2.py` aborta si el ancla no cierra.

### Usar los conteos de C5 (modo fiel) para los genes nuevos
**Qué se intentó:** tomar 44 y 33 eficientes de C5 para `eth` y `burs-alpha`.
**Qué pasó:** son del modo fiel; en el corregido son 37 y 25, la misma diferencia que W5 midió
(14 % a 24 % entra por la rama de la regla terminal). No son comparables con los otros cuatro.
**Estado:** descartado; el ranking usa el modo corregido en los seis.

### Comparar los genes nuevos en el nivel 1
**Qué se intentó:** ranking con las regiones de EPILAB tal como están y las nuestras para los nuevos.
**Qué pasó:** `eth` queda segundo y `burs-alpha` cuarto, pero la comparación mezcla regiones elegidas con y sin
ver los off-targets, y favorece a los nuevos. Con todos en su mejor región (nivel 3) quedan cuarto y quinto.
**Estado:** el nivel 3 es el resultado; el nivel 1 se reporta como contexto.

### Sumar la evidencia publicada al puntaje
**Qué se intentó:** pensarlo; no se implementó.
**Qué pasó:** exigiría equivalencia entre microinyección e ingesta y entre letalidad y esterilidad. No la tenemos.
**Estado:** descartado; segundo eje descriptivo, sin puntaje (D24).

### Leer la cascada como ranking de candidatos de distinto largo de región
**Qué se intentó:** la cascada cuenta ventanas limpias y eficientes, no tasas.
**Qué pasó:** favorece a las regiones de 300 nt: a 22 nt pone a `BicC_Dm` primero con 39 contra 30 de `MP_MRFV`, y
a `ATPaseD_Dm` por delante de `burs-alpha`. Además, los empates se resuelven por posición, un desempate arbitrario.
**Estado:** se reporta, y el orden de las puntas se lee con la escala absoluta.

## Conservación entre poblaciones y aislados (2026-10-21)

### Usar el haplotipo alternativo del genoma del Reino Unido como una fuente más
**Qué se intentó:** contar `GCA_975739835.1` como segunda fuente genómica de conservación.
**Qué pasó:** es un ensamblado alternativo de 488 Mb que no contiene los loci de `ATPaseD_Dm` (0 de 471
ventanas exactas), `eth` (1 de 539) ni `burs-alpha` (0 de 398), y contó como variación lo que era un hueco:
daba 77, 12 y 1 ventanas conservadas. **Estado:** descartado como criterio; se reporta como descripción.

### Usar el genoma de Córdoba (CIAP v1, ONT) como criterio de conservación
**Qué se intentó:** aceptar ventanas con hasta un desajuste en ese genoma.
**Qué pasó:** con un ensamblado solo ONT a 20x, una ventana con un desajuste puede ser variación o error:
en `burs-alpha` 118 de las 398 ventanas presentes en la línea de base aparecen con un desajuste. **Estado:**
se reporta en tres categorías (exacta, un desajuste, ausente) y no excluye ventanas.

### Un alineamiento local que no ve las inserciones del otro
**Qué se intentó:** marcar como conservada toda ventana cuyas 21 posiciones alinean y son idénticas.
**Qué pasó:** una inserción en el otro transcrito deja las posiciones de la consulta contiguas y pasaba
inadvertida; el transcriptoma argentino de `BicC_Dm` tiene una de 36 nt. Se agregó el corte entre bloques
alineados. **Estado:** corregido; es el mismo defecto que daría falsos "idénticos" en los 71 registros virales.

### Etiquetar una fuente por una localidad que no se había leído
**Qué se intentó:** rotular el transcriptoma `GHCC01` como "Junín".
**Qué pasó:** el registro dice "Argentina" y el remitente es el CeBio, Pergamino; la localidad de colecta no
figura. **Estado:** corregido a "Argentina (depositado desde el CeBio, Pergamino)".

### Buscar `eth` y `burs-alpha` en el TSA de NCBI por la API web de BLAST
**Qué se intentó:** ubicar contigs de estos genes en los transcriptomas de *D. maidis*, con las secuencias
públicas PZ371507 y PZ371508 (no con las de EPILAB).
**Qué pasó:** quedó en cola más de media hora sin resultado y se canceló. **Estado:** pendiente; sin eso la
conservación de estos dos genes solo se describe con el genoma de Córdoba.


---

## Ola 3 — las cinco investigaciones del checkpoint (2026-10-20/21)

Integrado desde los `NOTAS_PARA_META.md` de `research/ola3/C1` a `C5`.

### Lo que se cerró

**El manual del programa existía y nadie lo había leído.** `Quick_help.pdf`, 13 páginas, viaja
dentro del repositorio oficial de si-Fi21. Contesta los valores por defecto de cada modo y explica
por qué la eficiencia se apaga cuando se permiten desajustes. Copia en
`work/C1/siFi21--d6296b7/` y texto extraído en `work/C1/quick_help.txt`.

**si-Fi21 no busca regiones.** El único rastro es un parámetro `region_plot_lst`, documentado como
«Plot for suggested RNAi design region», **que nunca se usa**. La búsqueda de la región de 200 nt
más densa es un agregado nuestro, y hay que presentarlo así.

**La base de datos no explica los conteos de la planilla, si el laboratorio corrió `sifi21INTA`.**
En esa librería el conteo es por ventana y no por acierto de Bowtie como en el original. Medido
contra tres bases —los cuatro genes, los 71 registros públicos de MRFV y el transcriptoma TSA
GITV01—: 138, 40, 218 y 35 en las tres, sin mover una unidad. **Pero sólo bajo ese supuesto**: si
corrieron el programa original, la hipótesis de la base sigue viva tal como estaba.

**Verificación independiente del port.** `sifi21INTA`, forzando su tabla de energía a la del
original, coincide con `tools/sifi21_port/` en modo fiel **ventana por ventana** en las 4.722
ventanas de los cuatro genes y en los cinco términos del veredicto, con cero diferencias. Dos
implementaciones escritas sin conocerse dan lo mismo, lo que descarta además errores compartidos
entre el port y nuestra lectura del fuente.

### Lo que se descartó, con su motivo

- **Que la tabla de energía nueva explique la diferencia de conteos.** Es el único cambio químico
  entre si-Fi21 y la versión del INTA y mueve los conteos sólo −4, +1, −5 y 0.
- **Diseñar sobre el ortólogo de un cicadélido pariente.** Medido: de las ventanas de 21 nt de
  cada ortólogo, las que existen idénticas en el genoma del vector son entre el **0,7 % y el
  11,1 %**, contra 89-91 % para los dos genes que sí son de *D. maidis*. El camino que queda es
  recuperar la secuencia del vector primero.
- **Elegir ortólogos por nombre en el proteoma de referencia.** Descartado por el caso de `Rpn6`
  (ver D30). W4 §6.1 ya lo había declarado como límite; ahora hay un caso con número.
- **Seis de los ocho forks de si-Fi21**, descartados por SHA sin bajar contenido: su cabeza es un
  commit de la historia de upstream. Método barato y reutilizable, `git ls-remote` contra la lista
  de commits de la API.
- **Medir cuántos veredictos finales cambian al corregir el índice de la regla terminal.** Requiere
  correr el port con ViennaRNA. Se midió en cambio el efecto sobre la rama (51,4 % de las ventanas)
  y sobre el booleano terminal (31,4 %), que acota el problema.

### Advertencias de método que van a volver a pasar

- **No se puede crear ningún directorio `.git` dentro de la carpeta concedida**, así que `git
  clone` falla —también `--bare`—. Se resuelve bajando el tarball del commit por
  `api.github.com/repos/<owner>/<repo>/tarball/<ref>` y verificando el commit con `git ls-remote`,
  que sí funciona.
- **`sifi21INTA` no corre con Biopython ≥ 1.82**: usa `Bio.SeqUtils.GC`, eliminado en esa versión.
  Hay que fijar 1.81. Si a alguien le aborta, es esto.
- **Una secuencia en minúsculas da cero eficientes sin avisar**, en las dos librerías del INTA y en
  el original. Medido: 138 contra 0 en `MP_MRFV_full`. Si se corre cualquiera de estas herramientas
  sobre un FASTA enmascarado, el resultado va a ser cero y va a parecer válido.
- **Medir tamaño de palabra con fondos de alfabeto disjunto exige `-strand plus`.** Si la consulta
  tiene fondo de {A,C} y el sujeto de {G,T}, la hebra menos de la consulta calza con el fondo del
  sujeto. Costó una corrida.
- **`blastdbcmd` sobre las bases de W5 es inviable**: se construyeron sin `-parse_seqids`. Se
  muestrea directamente de los FASTA de `work/W5/ref/`.
- **Lanzar trabajos largos con `nohup … &` dentro de una celda corta: se mueren.** Hay que lanzar el
  comando en primer plano dentro de una celda en segundo plano.
- **Semilla derivada de `hash()` de Python: no reproducible entre procesos.** Cambiado a semilla
  determinista; una versión anterior de un TSV puede diferir en ±2 coincidencias en el control
  barajado.
- **Un DOI tampoco se reconstruye de memoria.** Se conjeturó el DOI de la versión revisada de
  Ribonanza; el DOI existía y correspondía a un artículo de neurociencia sin relación. Se descartó
  sin usarlo. Es la regla de `CLAUDE.md` extendida a los identificadores.
- **OpenAlex quedó fuera por falta de clave de API**, no por bloqueo de red. Se usó Europe PMC, que
  resolvió 21 de 23 textos completos en C4. No se intentó ninguna llamada anónima.
- **El backend `exe` del port no se pudo usar en ninguna línea de la ola 3**: necesita el RNAplfold
  2.1.5 que instala si-Fi21 en Windows. Todos los números de eficiencia de la ola 3 son del backend
  `vienna` con ViennaRNA 2.7.2, y los dos no dan lo mismo.
- **La comparación genoma contra transcriptoma sólo es posible en 2 de los 17 conjuntos locales**
  (maíz y abeja). Falta el genoma de *Homalodisca vitripennis*, que es la comparación que más
  valdría porque ahí están los 30 y 7 aciertos de W5.
- **Archivos obsoletos que conviene borrar a mano:** en
  `research/ola3/C4_offtargets_quimeras_largo/resultados/` quedaron `quimeras_eficiencia.tsv`,
  `quimeras_ventanas_cambiadas.tsv` y `quimeras_meta.json` de una primera corrida. Su contenido se
  reemplazó por una línea que dice que están obsoletos y adónde ir. Los datos buenos están en los
  pares con sufijo `_fiel_vienna` y `_corregido_vienna`.

---

## Contar cifras compartidas no sirve para detectar divergencia entre un informe y su página (2026-10-21)

**Qué se intentó.** `estado.html` declaraba como trabajo pendiente «resolver la divergencia del
`index.html` de W7», con el argumento de que 25 porcentajes del `REPORT.md` no aparecen en la
página y sólo 14 coinciden, y concluía que hasta resolverlo la página no se cita como fuente de
cifras.

**Qué se encontró al revisarlo.** **No hay divergencia.** El conteo mide otra cosa. Se extrajeron
todos los porcentajes de los dos archivos y se clasificó cada diferencia:

- Los **25 que están sólo en el informe** son omisiones, no contradicciones: la página es un
  resumen y el informe tiene 722 líneas. Que un resumen no repita una cifra no la contradice.
- De los **6 que están sólo en la página**, cuatro (`0 %`, `1 %`, `17 %`, `25 %`) son celdas de las
  matrices A.3 y B.3 o redondeos de cifras que el informe sí trae con decimal —el `17 %` de la
  página es el `17,0 %` del informe, y su `46 %` es el `46,3 %`—.
- Los **dos restantes** (`20,6 %` y `24,8 %`) sí eran números sin respaldo en el `REPORT.md`, pero
  **tienen fuente**: la tabla de 15 nt de `azar_por_k.md`, archivo hermano en la misma carpeta. Se
  agregó la cita a la página.

Y se verificó una por una que las cifras que **sí** aparecen en los dos digan lo mismo: 98,7 %,
33,7 %, 89,7 %, w* ≈ 0,02, los factores 2,38–2,50 y 1,015–1,064. Coinciden todas. `[E]`

**La sospecha más seria también se descartó.** Parecía que la página seguía afirmando sin tachar
«la diagonal se arma sola», que es justo lo que C9 retractó en §2.1 bis del informe. Está dentro de
un `<del>` con la corrección completa al lado; lo que falló fue el extractor de texto, que borra
las etiquetas y por lo tanto borra el tachado.

**La lección, que es el motivo de registrar esto.** Un verificador automático que compara un
documento con su resumen contando cifras **produce falsos positivos por diseño**, y además no ve
las fuentes en archivos hermanos ni distingue un número tachado de uno afirmado. Para comparar un
informe con su página hay que comparar **afirmaciones sobre la misma magnitud**, no inventarios de
números. El item se sacó de `tools/generar_estado.py`.


---

## Fase 2 y C12 (2026-10-22): diseño nuevo por homología y su validación

**Qué se intentó.** Resolver por secuencia la ortología de los genes del catálogo de C5 en *M. quadrilineatus* y medir cuántos llegan a un ortólogo con nucleótido suficiente en *D. maidis*; después validar la regla de homología entre cicadélidos (A) y con marafivirus parientes del MRFV (B). Detalle en `research/ola3/C11_diseno_nuevo/` y `research/ola3/C12_validacion_homologia/`.

**Qué se descartó y por qué.** Diseñar a partir de otro género: 2 de 11 familias superan 300 nt con 90 %. Usar un virus pariente del MRFV como fuente de ventanas: ≤ 0,66 % del genoma compartido. Cruzar por símbolo de gen: el `Rpn6` de *Drosophila* es PSMD11 y PSMD6 se llama `Rpn7`.

**Lecciones de proceso.** Un primer cálculo de pares recíprocos dio 0 por identificadores sin normalizar (`ref|XP_..|` contra `sp|..`). El `blastp` completo entre dos proteomas de ~30.000 proteínas era demasiado lento en la máquina local y se recortó a una submuestra declarada. Un `git rebase --abort` sin comparar `orig-head` con HEAD sacó 32 archivos del disco: antes de abortar un rebase hay que verificar que `orig-head` coincide con HEAD.


## Escala min-max para ordenar un grupo de dos candidatos (2026-10-22)

Se intentó usar la escala min-max para ordenar el grupo viral (`MP_MRFV` y `CP_MRFV`) y el del insecto dentro de las regiones recomendadas. Con dos candidatos, la escala manda uno a 0 y otro a 1 en cada eje, y el resultado es una moneda determinada por la escala (51,5 % a 21 nt en el grupo viral). Descartado para ordenar pares; se conserva sólo como sensibilidad. Detalle en `docs/plan_checkpoint2/salidas/F1_decision_ranking.md` §3.

## Orden de `bursA_Dm` y `ATPaseD_Dm` según el método (2026-10-22)

Con escalas continuas, `bursA_Dm` queda por delante de `ATPaseD_Dm` a los dos largos (100 % de los sorteos). La cascada, que cuenta ventanas limpias y eficientes, invierte el par. Se descarta reportar ese par como orden firme. Ver `docs/plan_checkpoint2/salidas/F1_decision_ranking.md` §2.

## Fase 3 del checkpoint 2 (2026-10-22): lo que se descartó al armar el diseño

- **Citar «0 de 20 genes» como prueba de que la región no discrimina.** Descartado: W7 §1.1 muestra que mide la media de un puntaje con un nulo de bloques de 30 ventanas, y es una afirmación sobre el nulo tanto como sobre la biología.
- **Fijar tamaño de muestra y umbrales de knockdown.** Descartado: falta la varianza entre dsRNA del mismo gen en *D. maidis*.
- **Usar «unos 20 días» como latencia del MRFV.** Descartado: la fuente abierta es de *S. kunkelii*.
- **Control de región alternativa y control libre contra formulado con respaldo.** No tienen fuente abierta; quedan como `[H]` y `[?]`.
- **Plantear matar o esterilizar como eje único.** Descartado por D40: ninguna fuente abierta mide los dos desenlaces en el mismo gen.

## Fase 5 (2026-10-22): correcciones que salieron del reordenamiento

- **Pregunta 3 del entregable.** La versión que decía que `eth` y `burs-alpha` no estaban en ningún transcriptoma público fue corregida por C11 (2026-10-21). El texto tachado se quitó de `para-el-investigador.md`; la historia queda aquí.
- **Lectura del par `eth`–`burs-alpha`.** Se había escrito que no se distinguían. Ese enunciado dependía de exigir que el orden se sostenga en las dos escalas, y se corrigió (D38, enmienda de 2026-10-22).

## Quimeras con las regiones nuevas (2026-10-22, línea C13)

- **Rehacer las quimeras sobre las regiones de EPILAB.** Descartado como resultado: ya estaba hecho en C4 y no es lo que el proyecto recomienda hoy. Se corrió igual, pero **como verificación**: el script nuevo reproduce la tabla de C4 celda por celda en los dos modos, y recién entonces se usó con las regiones vigentes.
- **Comparar las quimeras contra las cifras publicadas de las regiones (38, 21, 36, 21).** Descartado: esas cifras se cuentan sobre el perfil del gen completo y la quimera se arma con el recorte. Se midió el control que faltaba y la diferencia llega a 11 ventanas en `MP_MRFV`, así que la comparación habría sido contra el número equivocado.
- **Mezclar los modos del port.** Evitado a tiempo: C4 midió las quimeras en modo `fiel` y el ranking de W7 y C7 se construyó en `corregido`. En `fiel`, `MP_MRFV` tiene 142 ventanas eficientes y en `corregido` 123. Todo lo que compara contra el ranking se corrió en `corregido`.
- **Tamizar las 5.760 ventanas de las doce quimeras.** Descartado por innecesario: toda ventana heredada es, base por base, una ventana de su región de origen, así que alcanza con tamizar las 4 regiones y los 40 nt que cruzan cada unión, 1.160 ventanas. El resultado es idéntico y cuesta una pasada por referencia en vez de siete.
- **Las ternas y la cuádruple.** No se corrieron: 900 a 1.000 nt, muy por encima de los 262 y 300 pb de los dos antecedentes hemípteros publicados, y con el empalme aportando 4 ventanas eficientes de 240 no hay motivo para esperar que agregar uniones mejore nada. El script las soporta cambiando el `2` de `itertools.permutations(REGIONES, 2)`.

## La respuesta del investigador (2026-10-22): tres correcciones

La carta está transcripta y mapeada en `docs/plan_checkpoint2/salidas/F6_respuesta_y_cambios.md`.
Lo que sigue es lo que nos corrigió, y de qué lado quedó cada cosa.

- **El 1,75 como explicación del desajuste de conteos. Descartado, y era nuestro.** Afirmábamos
  —en el correo y en la sección de la planilla de `entregables/critica-herramientas.md`— que
  subir el umbral de estabilidad de extremos de 1,0 a 1,75 era lo que más acercaba a los 114, 35,
  199 y 33 de la planilla, y que «dos barridos independientes apuntan al mismo parámetro». Él
  declaró la configuración de sus corridas, `siFi21_8_1.0_0.1_1111`, con el umbral en **1,0**
  `[R]`. La medición sobrevive: esa celda da 117, 35, 199 y 32, con dos valores exactos y un
  error total de 4 `[M]`. La lectura causal no: con 22.176 celdas barridas, que una acierte dos de
  cuatro números es lo que un barrido grande produce por sí solo. Queda como ADR D45, y la lección
  es general: el mejor punto de un barrido con muchos grados de libertad no es un hallazgo hasta
  que algo externo al barrido lo confirme.

- **El veto ecológico automático. Descartado, y lo habíamos construido nosotros sobre un criterio
  que él sí comparte.** El criterio de D17 —una ventana con coincidencia en un no objetivo cuenta
  como riesgo aunque el modelo no la prediga eficiente— él lo corre igual y por el mismo
  argumento, así que D17 queda confirmado por una fuente independiente. Lo que no hace es
  convertir la coincidencia en una compuerta: «no trataría todas las coincidencias de 21 nt como
  equivalentes ni las convertiría automáticamente en un veto ecológico universal» `[R]`. Pasa a
  ADR D48 como alerta con cuatro campos obligatorios y justificación escrita. **Y nos cuesta una
  conclusión:** el desempate del tercer puesto se apoyaba en el veto de `ATPaseD_Dm` por tres
  coincidencias con *Homalodisca vitripennis*, y sin veto el empate vuelve.

- **El peso único del panel no objetivo. Descartado por confundir dos funciones.** El 0,60 que
  D18 le daba a *H. vitripennis* servía a la vez como riesgo de exposición y como señal de
  conservación entre cicadélidos, que son cosas de signo opuesto. Él pide separarlas `[R]`; pasa
  a ADR D47 como dos vectores que el motor no combina. Lo que **no** se descarta es el organismo:
  pidió explícitamente conservarlo en el panel por su valor de conservación.

- **Comparar 133 contra 114 como si fueran la misma cifra. Descartado al leer el fuente.**
  Siguiendo su pista de «referencias y criterios de contabilización», la columna «Efficient siRNA
  hits» del original no cuenta ventanas: cuenta registros de acierto de Bowtie agrupados por
  nombre de referencia (`general_helpers.py:107-123`), y la eficiencia sólo se calcula para
  aciertos en la hebra `+` (`sifi_pipeline.py:195-221`) `[R]`. `sifi21INTA`, en cambio, cuenta una
  fila por ventana (`SifiPipeline.py:430-448`). Todas nuestras comparaciones contra la planilla
  venían midiendo unidades distintas. La nueva hipótesis —que el desajuste es de referencia y de
  unidad, no de parámetro— es la línea M1 de `docs/plan_ola4/PLAN_OLA4.md` y todavía es `[H]`.

- **Seguir barriendo parámetros hasta dar con los cuatro números. Evitado a tiempo.** Era el
  camino obvio después de que él dijera que el umbral no era 1,75: agregar ejes al barrido hasta
  que alguna celda coincida. Es el mismo error de D45 a mayor escala. El plan de la ola 4 lo
  prohíbe explícitamente: si M1 no cierra con la referencia, el resultado que se informa es la
  cota y el dato que falta, no otra corrida.

- **Correr la matriz de bases de M1 con insumos sustitutos. Descartado, y declarado como
  pendiente.** La máquina que ejecutó M1 no tiene `work/`, ni Bowtie, ni ViennaRNA, ni si-Fi21
  instalado, así que las celdas reales no se pudieron calcular. Las dos salidas tentadoras eran
  bajar secuencias públicas parecidas a las de EPILAB para los dos genes virales, o presentar la
  demostración sintética como si fuera la matriz. Las dos habrían producido una tabla con los
  cuatro números y ninguna habría medido el caso real. Lo que se entrega es la regla verificada
  más la secuencia exacta de comandos para la máquina que tiene el corpus, y el estado dice «no
  corrió» en los tres criterios que no se cumplieron.
  **Actualización del 2026-10-23:** la matriz corrió. El insumo que se declaró ausente estaba en
  el instalador de si-Fi2015, que trae su propio `RNAplfold.exe` 2.1.5 y su propio `bowtie.exe`.
  La lección es de inventario y no de método: antes de declarar una herramienta ausente conviene
  mirar dentro del programa cuya salida se quiere reproducir.

- **Abrir el eje de la versión del motor de accesibilidad (2.4.x, 2.6.x). Evitado por ahora.** Es
  la tarea 4 de M1 y el plan la condiciona a que la referencia no cierre el desajuste. La
  referencia no cerró **ni falló**: quedó sin correr. Agregar puntos a un barrido mientras la
  hipótesis principal sigue sin medirse es el error de D45 otra vez, así que el eje queda cerrado
  hasta que la matriz corra.
  **Actualización del 2026-10-23:** la matriz corrió y cierra un gen de cuatro, así que el eje
  queda **habilitado** para los otros tres. Lo que cambia es que ya no es un barrido a ciegas: el
  cruce de los dos ejes muestra que la versión del motor mueve los conteos en direcciones
  distintas según el gen, así que hay una pregunta concreta que contestar (sección 7 del REPORT
  de M1).

- **La orientación de entrada como explicación del desajuste. Descartada con medición.** Era uno
  de los cuatro ejes que el investigador nombró explícitamente el 2026-10-22 y había que
  cerrarlo. Se corrió el motor de eficiencia sobre el complemento reverso de los cuatro genes
  —hay que volver a correrlo, porque el complemento reverso cambia las ventanas y no sólo los
  aciertos— y el conteo da 47, 22, 108 y 52 contra los 114, 35, 199 y 33 declarados: una
  distancia L1 de 190, frente a 44 de la orientación directa `[M]`
  (`research/ola4/M1_conteo_y_referencia/resultados/orientacion.json`). No sólo no acerca: se
  aleja en un factor de cuatro y mueve tres genes en el sentido equivocado. El eje queda cerrado
  con número y no con argumento.

- **Que un aislamiento distinto de MRFV explique los conteos virales. Descartado para los 65
  registros públicos.** Era la hipótesis que el propio reporte anterior de M1 había propuesto
  como la candidata viva. Se bajaron los 65 registros públicos de MRFV de GenBank por número de
  acceso —los que W5 ya había inventariado— y se aplicó la regla: para `MP_MRFV` las filas
  posibles son 133, 133 y 30, y con un desajuste permitido 133, 133 y 85. **Ninguna es 114**, y
  no hay nada entre 30 y 133 `[M]`. Para `CP_MRFV` es peor: el declarado 35 está **por encima** de
  nuestras 32 ventanas eficientes, y la regla sólo puede superar el conteo por ventana si alguna
  ventana eficiente pega dos veces en la misma referencia, lo que no pasa en ninguna de las 65
  `[M]`. **Ninguna referencia de MRFV puede dar 35 bajo esta regla.** Lo que queda vivo es un
  aislamiento no publicado, y eso es un pedido y no una corrida nuestra.

- **Presentar la combinación mejor por gen como la explicación. Evitado.** Con la matriz corrida
  aparece la tentación: `BicC_Dm` se acerca a 199 con RNAplfold 2.1.5 (200) y `ATPaseD_Dm` se
  acerca a 33 con ViennaRNA 2.7.2 (35), así que eligiendo el mejor motor para cada gen el vector
  queda (133, 32, 200, 35) y la distancia L1 baja de 44 a 25 `[M]`. Eso **no es una corrida**:
  mezcla dos motores entre genes y por lo tanto no corresponde a ninguna configuración que el
  laboratorio pudiera haber usado. Es el error de D45 con otra variable, y el REPORT lo dice
  explícitamente en lugar de reportar el 25 como logro.

## Estimar por remuestreo un diseño enriquecido en discordantes (2026-10-23, línea M4)

- **Descartado, con motivo que vale como regla general.** Después de medir que replicando el diseño
  de Cedden harían falta 232 siRNA para distinguir los dos modos `[M]`, la idea natural es volver a
  remuestrear subiendo a propósito la proporción de siRNA discordantes y ver cuánto baja el número.
  No se puede: en las 29 filas de Cedden hay **un solo** siRNA discordante (`si778`), así que
  cualquier remuestreo que lo enriquezca reproduce su mismo desenlace, la variabilidad entre
  discordantes sería cero y la potencia se infla a voluntad. **Un remuestreo no puede inventar
  variabilidad que la población madre no tiene.** Es la razón por la que la sección 4 del REPORT de
  M4 cambia de estadístico —de una correlación de rangos a un contraste entre grupos con supuestos
  declarados— en vez de subir el n del mismo cálculo.
- **Comparar los dos modos con más datos del mismo tipo, sin mirar la discordancia. Evitado.** La
  objeción obvia a la validación de C9 es «poca muestra», y la respuesta obvia es pedir más siRNA.
  Pero la cuenta exacta muestra que el problema no es el n: con k siRNA discordantes, la prueba de
  aleatorización por intercambio no puede dar un p menor que 2/2^k, así que **con menos de 6
  discordantes ningún dato alcanza alfa 0,05** `[M]`. Pedir más datos del mismo tipo sin fijarse en
  la discordancia es gastar etiquetas para volver al mismo lugar.
