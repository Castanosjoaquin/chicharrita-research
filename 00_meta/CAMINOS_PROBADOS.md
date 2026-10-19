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
