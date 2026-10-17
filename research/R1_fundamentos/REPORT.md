# R1 — Fundamentos: biología del RNAi y del sistema chicharrita–achaparramiento–maíz

**Para quién es esto.** Para cuatro ingenieros en IA que tienen que discutir de
igual a igual con un investigador de biología molecular dentro de pocos días, y
que necesitan poder decidir si una idea computacional propia tiene sentido
biológico antes de gastar una semana en programarla. Se asume álgebra lineal,
probabilidad, estructuras de datos y optimización. No se asume nada de biología:
cada término se define la primera vez que aparece y está además en
`glosario_parcial.md`.

**Cómo leerlo.** Las seis secciones están construidas una sobre la otra y se leen
de corrido en treinta o cuarenta minutos. La sección 4 es la bisagra: contesta,
con evidencia, la pregunta de si se puede silenciar a los patógenos, y de esa
respuesta dependen casi todas las decisiones de diseño que vienen después. El
cierre, "Lo que esto implica para nuestro proyecto", traduce la biología a
restricciones de diseño.

**Convención de evidencia.** Cada afirmación relevante lleva un marcador:
`[E]` establecido (consenso en literatura revisada por pares), `[R]` reportado
(una o pocas fuentes, preprint, nota técnica, web de empresa), `[H]` hipótesis
nuestra sin respaldo todavía, `[?]` incierto o con contradicción entre fuentes.
Los identificadores entre corchetes tipo `S15` remiten a `sources.json` y a las
notas crudas en `notes/`. Todos los números vienen con su contexto experimental
—laboratorio, invernáculo o campo; especie; tamaño de muestra— porque un número
sin contexto en este dominio es casi siempre engañoso.

---

## 1. Base molecular: qué son el ADN, el ARN y un gen

### 1.1 El flujo de información

Una célula guarda su información en ADN (ácido desoxirribonucleico), un polímero
de cuatro monómeros —A, C, G, T— organizado en dos hebras complementarias y
antiparalelas: donde una tiene A la otra tiene T, donde una tiene G la otra tiene
C. Esa complementariedad es la razón de que todo lo que sigue funcione, porque
convierte la información en algo copiable y, para nosotros, en algo *buscable*:
la pregunta "¿esta secuencia se parece a aquella?" tiene sentido físico, no sólo
combinatorio.

Un **gen** es un tramo de ADN que se lee para producir una molécula funcional.
La lectura se llama **transcripción** y produce **ARN** (ácido ribonucleico), un
polímero similar pero de una sola hebra, con ribosa en lugar de desoxirribosa y
con U (uracilo) en lugar de T. El producto concreto de transcribir un gen en un
momento dado es un **transcrito**. La distinción entre gen y transcrito importa
más de lo que parece: un mismo gen puede dar varios transcritos distintos según
qué fragmentos se empalmen (*splicing*), y lo que nuestros algoritmos van a
tomar como entrada son transcritos, no genes `[E]`.

Si el transcrito codifica una proteína se llama **ARN mensajero (ARNm, mRNA)**, y
el proceso por el cual el ribosoma lo recorre de a tres nucleótidos (codones) y
ensambla la cadena de aminoácidos correspondiente se llama **traducción**. La
secuencia que efectivamente se traduce es el **marco abierto de lectura (ORF,
*open reading frame*)**; por delante y por detrás quedan las **regiones no
traducidas (UTR, *untranslated regions*)** 5′ y 3′, que no codifican proteína
pero sí regulan estabilidad y traducción del mensaje. Esta geografía del
transcrito —UTR 5′, ORF, UTR 3′— va a reaparecer en la sección 6 como una
variable de diseño con efecto medido `[R]`.

### 1.2 ARN que no codifica proteínas

No todo el ARN se traduce. El **ARN no codificante (ncRNA)** es ARN funcional que
no produce proteína, y dentro de esa categoría hay clases con biogénesis y
función distintas. Para nuestro problema importan tres.

Los **microARN (miRNA)** son ARN endógenos cortos, de **20 a 24 nucleótidos**, que
en general regulan negativamente la expresión de otros genes `[E]` `S51`. Son
parte del programa normal de la célula: están codificados en el genoma, se
transcriben como precursores con estructura de horquilla (*hairpin*) y regulan
genes propios, muchas veces con apareamiento imperfecto.

Los **ARN pequeños de interferencia (siRNA, *small interfering RNA*)** tienen un
largo parecido pero otro origen: provienen del corte de un ARN de doble cadena
largo, y apárean con su blanco de manera perfecta o casi perfecta. En plantas los
siRNA se subclasifican todavía más —phasiRNA, tasiRNA, easiRNA— según cómo se
generan `[E]` `S51`. La distinción operativa es: el miRNA es un regulador
endógeno con muchos blancos posibles, el siRNA es un ejecutor de alta
especificidad contra un blanco definido.

Los **ARN largos no codificantes (lncRNA)** se definen simplemente como moléculas
de ARN funcionales de más de **200 nucleótidos** sin potencial de codificar
proteína `[E]` `S51`. Se caracterizan por baja abundancia, menos exones que el
ARNm, expresión tejido-específica y baja conservación de secuencia frente a los
genes codificantes `[E]` `S51`. No son el blanco ni la herramienta de este
proyecto, pero conviene conocerlos para no confundirlos con los anteriores: son
largos, regulatorios y casi siempre actúan por estructura o por interacción con
proteínas, no por complementariedad de secuencia corta.

### 1.3 Por qué el ARN de doble cadena es distinto

Casi todo el ARN de una célula eucariota es de cadena simple. El **ARN de doble
cadena (ARNdc, dsRNA)** —dos hebras complementarias apareadas— es raro en
condiciones normales y, en cambio, es exactamente lo que produce un virus de ARN
cuando se replica. Por eso la célula lo trata como señal de alarma: el dsRNA
largo es, en la práctica, una firma molecular de infección. Esa es la base de
todo lo que viene. En insectos, el dsRNA funciona a la vez como disparador de
silenciamiento y como patrón molecular asociado a patógeno, y la maquinaria que
lo procesa es parte del sistema de inmunidad antiviral `[E]` `S50`.

La consecuencia conceptual es importante para gente que viene de ingeniería: el
dsRNA exógeno no es una droga que inhibe una proteína por acoplamiento
estructural. Es **información** que se entrega a una maquinaria que ya existe en
la célula, y que esa maquinaria usa como molde de búsqueda. Si la maquinaria no
está, el dsRNA no hace nada. Toda la sección 4 es una aplicación de esta frase.

---

## 2. El mecanismo de RNAi, con precisión

### 2.1 Dicer: la regla molecular que corta

El **RNAi (RNA interference, interferencia por ARN)** empieza cuando una
ribonucleasa de la familia RNasa III llamada **Dicer** reconoce un dsRNA largo y
lo corta en dúplex cortos. Dicer no corta al azar. Su dominio **PAZ** —el nombre
viene de las proteínas PIWI, Argonaute y Zwille— reconoce específicamente el
extremo característico de los intermediarios de RNAi: un saliente de dos
nucleótidos en el extremo 3′ y un fosfato en el 5′ `[E]` `S41`. Con ese extremo
anclado, los dominios PAZ y RNasa III "actúan juntos como una regla molecular"
que mide una distancia fija desde el extremo hasta el centro catalítico y define
el largo del producto `[E]` `S41`. En la estructura de Dicer de *Giardia
intestinalis* esa distancia es de **65 Å**, y en otras versiones de la enzima los
dominios se reordenan para dar productos de largo distinto `[E]` `S41`.

Esto tiene una consecuencia que el equipo debería internalizar, porque es
contraintuitiva: **el largo del siRNA no lo elige quien diseña el dsRNA, lo elige
la enzima del organismo que lo procesa**. Y no es el mismo en todos lados. En
insectos, Dicer-2 produce siRNA de largo específico de orden: dípteros y
coleópteros principalmente **21 nt**, himenópteros y ortópteros enriquecidos en
**22 nt**, lepidópteros predominantemente **20 nt**, y el patrón se mantiene
frente a virus distintos y a disparadores sintéticos, lo que indica que el largo
lo dicta la maquinaria del hospedador y no el disparador `[E]` `S50`. Para
hemípteros —el orden de la chicharrita— ese trabajo no reporta perfil de largo:
es un hueco `[?]` `S50`.

### 2.2 Argonaute y el RISC: la búsqueda guiada

El dúplex producido por Dicer se entrega a una proteína **Argonaute (AGO)**, que
forma con él el **RISC (RNA-induced silencing complex)**. La geometría del
ensamblado está resuelta estructuralmente: el extremo 3′ de la hebra lo une el
dominio PAZ y el fosfato 5′ lo une el dominio **MID** `[E]` `S41`. Argonaute es
bilobular: un lóbulo con los dominios N y PAZ, el otro con MID y **PIWI** `[E]`
`S41`.

De las dos hebras del dúplex, sólo una queda como **hebra guía**; la otra, la
**hebra pasajera**, se degrada o se disocia. "Su selección es un determinante
clave del silenciamiento que sigue" `[E]` `S41`. Esta frase es, traducida a
nuestro lenguaje, la razón por la cual el diseño de dsRNA es un problema de
optimización y no una elección arbitraria de ventana: si se carga la hebra
equivocada, el complejo busca la secuencia equivocada.

El RISC cargado hace vigilancia citoplasmática: une ARN de cadena simple
complementario a su guía. La unión la inician los **nucleótidos 2 a 6 de la guía,
la secuencia semilla (*seed*)** `[E]` `S41`. Si la complementariedad es
suficiente, el dominio PIWI corta el blanco. PIWI adopta un plegamiento tipo
RNasa H y lleva una tríada catalítica **DDX** (X = Asp o His) que está presente en
las Argonautas con actividad de corte —llamada actividad *slicer*— y ausente en
las que no cortan `[E]` `S41`. No todas las Argonautas cortan: de las cuatro
Argonautas humanas, sólo Ago2 tiene actividad slicer `[E]` `S41`. El RISC también
puede reprimir la traducción sin cortar, antes o después de la iniciación `[E]`
`S41`.

Dos detalles mecanísticos tienen valor directo para el diseño. Primero, para que
el corte ocurra, el extremo 3′ de la guía tiene que soltarse del dominio PAZ: con
un blanco de 12 nt sigue unido, con uno de 15 nt se libera para acomodar la
extensión más allá de una vuelta completa de hélice `[E]` `S41`. Segundo, una
burbuja (*bulge*) en la región semilla **de la guía** impide el corte, mientras
que la misma burbuja en esa región **del blanco** lo permite `[E]` `S41`. La
asimetría importa: lo que se tolera de un lado no se tolera del otro.

### 2.3 Silenciamiento post-transcripcional y transcripcional

Lo descrito hasta acá es **silenciamiento post-transcripcional (PTGS,
*post-transcriptional gene silencing*)**: el gen se sigue transcribiendo y lo que
se destruye es el transcrito. Existe una segunda ruta, el **silenciamiento
transcripcional (TGS)**, donde el ARN pequeño no corta el mensaje sino que dirige
la metilación del ADN del locus para que deje de transcribirse. En plantas esa
ruta se llama **RdDM (RNA-directed DNA methylation)**: siRNA de 24 nt se cargan en
AGO4, que hace de andamio sobre el transcrito naciente y recluta
metiltransferasas que metilan el molde de ADN `[E]` `S21`. El RdDM silencia
elementos transponibles y **puede actuar sobre el ADN geminiviral**, es decir que
funciona como defensa epigenética contra virus de ADN `[E]` `S21`. Esto no es un
detalle académico: uno de los cuatro patógenos del complejo es un geminivirus
(sección 3), y la diapositiva oficial del organizador pone explícitamente a
AGO4/RdDM como el cuarto nivel de su espacio de diseño.

### 2.4 Amplificación y sistemia: acá los reinos se separan

Esta subsección es la más importante de la sección 2 y la que más veces se
malinterpreta.

En **plantas**, el silenciamiento se amplifica. Existen **ARN polimerasas
dependientes de ARN (RdRP, RDR)** que toman los fragmentos como molde y
sintetizan más dsRNA, generando siRNA secundarios. *Arabidopsis thaliana* tiene
seis RDR; RDR1, RDR2 y RDR6 pertenecen al clado RDRα con el motivo catalítico
DLDGD `[E]` `S21`. Las RDR amplifican la producción de siRNA derivados de virus
(vsiRNA) y su diseminación a tejidos distantes, montando una respuesta antiviral
fuerte `[E]` `S21`. Las plantas tienen además cuatro Dicer-like (DCL1–DCL4) y
diez Argonautas `[E]` `S21`. En la defensa antiviral, **DCL4 genera el vsiRNA de
21 nt, la especie dominante**, y DCL3 genera siRNA de 24 nt en plantas infectadas
por virus de ADN, crucial para la defensa por metilación contra geminivirus `[E]`
`S21`.

En **nematodos** existe transporte activo de la señal de silenciamiento entre
células y tejidos, mediado por las proteínas SID-1 y SID-2.

En **insectos** la situación es distinta y es decisiva para nuestro problema.
**No se ha encontrado un homólogo claro de RdRP en insectos** `[E]` `S08`. Y los
insectos **carecen de homólogos de Sid-1 y Sid-2**, de modo que el mecanismo de
diseminación de la señal no está resuelto `[E]` `S08`. Respuestas fuertes y
duraderas en algunos escarabajos sugieren algún mecanismo de amplificación no
identificado, pero no hay una vía demostrada `[?]` `S08`.

La consecuencia práctica es dura y hay que decirla sin adornos: **en un insecto
no se puede contar con que una dosis pequeña se amplifique sola.** La cantidad de
disparador que entra es, aproximadamente, la que hay. De ahí que la eficiencia
varíe tanto entre órdenes: especies recalcitrantes muestran *knockdown*
—reducción de la expresión— de alrededor del 60 % o menos, y a menudo
transitorio, mientras que algunos coleópteros alcanzan 90 % o más, a veces con
efectos duraderos o heredables `[E]` `S08`.

### 2.5 Qué significa "ARN exógeno"

**ARN exógeno** es ARN aplicado desde afuera del organismo: pulverizado sobre la
hoja, incorporado a una dieta, inyectado, absorbido por la raíz. La idea
completa, a veces llamada **RNAi ambiental**, es que ese ARN entre a las células
y sea tomado por la maquinaria endógena descrita arriba como si fuera propio
`[E]` `S07`. No hay transgénesis: no se modifica el genoma de nada, se entrega
información.

Las rutas de captación en insectos documentadas son proteínas canal tipo Sid-1
en algunas especies y endocitosis mediada por receptor en otras —el escarabajo de
la papa de Colorado usa ambas— y **el escape del endosoma al citoplasma es un
paso crítico** `[E]` `S08`. En plantas, la vía principal implicada en la
captación foliar de dsRNA es la **entrada por los estomas**, y las RNasas
apoplásticas degradan el dsRNA expuesto antes de que entre `[R]` `S43`.

Y hay un límite cuantitativo que contradice la intuición de "más dosis, más
efecto": **más dsRNA no siempre es más silenciamiento**, porque la
sobresaturación puede alterar la vía de miRNA y causar letalidad inespecífica
`[E]` `S08`. En el psílido de la papa (*Bactericera cockerelli*), con siete
concentraciones ensayadas de 0,1 a 500 ng/µL sobre adultos y ninfas de tercer
estadio, la concentración más efectiva o segunda más efectiva fue **100 ng/µL
para los tres genes blanco, y concentraciones mayores no dieron más knockdown**,
con saturación del RISC como explicación propuesta `[R]` `S26`. En ese mismo
trabajo el silenciamiento persistió sólo **3 a 5 días** después de retirar la
fuente de dsRNA, de donde los autores concluyen que el disparador "debe estar
disponible continuamente" `[R]` `S26`.

---

## 3. El sistema patógeno: un vector, cuatro agentes y un cultivo

### 3.1 *Dalbulus maidis*, la chicharrita del maíz

*Dalbulus maidis* (Hemiptera: Cicadellidae) es un **fitófago de floema**:
inserta su estilete en los haces vasculares de la hoja y se alimenta de la savia
elaborada. Es especialista del género *Zea* y se reproduce sólo sobre *Zea*
`[E]` `S01`. Tiene **cinco estadios ninfales**; del huevo al primer estadio pasan
entre cuatro y seis días `[R]` `S01`. La longevidad promedio del adulto reportada
es de unos **78 días en machos y 30 en hembras**, con alrededor de **15 huevos
por día** `[R]` `S01`. Se distribuye por casi toda América y el Caribe, con
centro de origen reportado en México `[R]` `S01`. Era plaga secundaria en Brasil
y **desde 2015 aumentó mucho su población**, junto con la incidencia de los
achaparramientos, hasta volverse plaga principal `[R]` `S38`.

Lo que convierte a este insecto en un problema de otra categoría no es el daño
directo de su alimentación sino su rol de **vector**. Y el modo de transmisión
tiene un nombre técnico con consecuencias enormes: **transmisión persistente
propagativa**. Persistente significa que, una vez adquirido, el patógeno queda en
el insecto; propagativa significa que el patógeno **se multiplica dentro del
insecto** antes de ser transmitido `[E]` `S12` `S22`. El recorrido es: el insecto
adquiere el agente alimentándose de floema infectado —la adquisición puede
ocurrir en minutos—, el agente atraviesa el epitelio del intestino medio, pasa a
la hemolinfa, circula, coloniza tejidos secundarios y finalmente llega a las
**glándulas salivales**, desde donde se inocula en la próxima planta al
alimentarse `[E]` `S01` `S44`. En *Spiroplasma kunkelii* ese **período latente es
de 18 a 22 días** hasta las glándulas salivales, y varía con el aislamiento, el
título, el biotipo y la edad del insecto `[R]` `S01`. No hay transmisión
transovárica: ninfas y adultos deben adquirir cada uno por su cuenta `[R]` `S10`.
Y por ser persistente-propagativa, los insectos que adquieren el patógeno
**permanecen inoculativos durante toda su vida** `[E]` `S45`.

Esto reordena por completo el espacio de intervención, y vale detenerse acá
porque es el argumento que justifica casi toda la estrategia posterior. Primero,
hay un período de latencia de dos a tres semanas entre que el insecto adquiere y
que puede transmitir: es una ventana temporal donde una intervención sobre el
insecto todavía sirve. Segundo, y en sentido contrario, matar al insecto después
de que inoculó no salva a la planta. Tercero, cualquier agente de control que
tarde en matar llega tarde: los hongos entomopatógenos tienen justamente ese
problema (sección 5). Cuarto, los insecticidas reducen la abundancia del vector
dentro del cultivo pero **no previenen los eventos de infección inicial causados
por insectos infectivos que llegan de afuera**, porque la transmisión puede
ocurrir apenas empieza la alimentación `[R]` `S44`.

Hay además un dato que el equipo necesita tener presente: *D. maidis* **expresa
los genes de la vía de RNAi** `[R]` `S19`. Su transcriptoma, ensamblado a partir
de 1.727.369.026 lecturas pareadas de 100 nt de adultos enteros, tiene 56.116
transcriptos y contiene, además de la vía de RNAi, las vías Toll, Imd, Jak/Stat,
el sistema activador de profenoloxidasa, PGRP y péptidos antimicrobianos `[R]`
`S19`. Dicho de otro modo: la maquinaria que necesitamos para que el dsRNA
funcione está, en el insecto, presente y anotada.

### 3.2 Los cuatro agentes del complejo

El complejo de achaparramiento del maíz (*corn stunt disease complex*, CSDC)
está causado por **cuatro** patógenos, que aparecen solos o combinados `[E]`
`S10` `S46` `S47`:

**1. *Spiroplasma kunkelii* (corn stunt spiroplasma, CSS).** Es un **mollicute**:
una bacteria **sin pared celular**, de genoma pequeño y bajo contenido GC, con
morfología helicoidal y movilidad propia `[E]` `S12`. Su cromosoma circular tiene
**1.463.926 pares de bases** más cuatro plásmidos `[E]` `S40`. Vive **restringido
al tejido de floema** de la planta `[E]` `S12`, y dentro del insecto recorre el
camino descrito arriba, con retención en el lumen intestinal de hasta 45 días
`[R]` `S01`. Causa el **achaparramiento pálido** (*enfezamento pálido*) `[E]`
`S12`: estrías cloróticas que van de la base a la punta o al margen de la hoja,
estrías rojo-púrpura, y achaparramiento por acortamiento de internodios; en casos
severos, múltiples espigas pequeñas con granos flojos o ausentes `[R]` `S01`.
Los síntomas aparecen entre 15 y 40 días post-transmisión según una fuente `[R]`
`S01`, de tres a cinco semanas según otra `[E]` `S45`, y típicamente tres a
cuatro semanas según una tercera `[R]` `S10`: las tres son compatibles.

**2. *'Candidatus* Phytoplasma asteris', subgrupo 16SrI-B (maize bushy stunt
phytoplasma, MBSP).** También mollicute, también **sin pared celular**, también
restringido al floema `[E]` `S12`. Causa el **achaparramiento rojo** (*enfezamento
vermelho*) `[E]` `S12`: hojas pequeñas rojizas, nervadura central roja, estrías
amarillas o cloróticas, y achaparramiento similar al del espiroplasma `[R]`
`S01`. Los fitoplasmas han perdido buena parte de su genoma y "sus funciones son
más similares a las de los virus" `[R]` `S44`; son de los pocos procariotas que
colonizan el citoplasma de células vegetales, específicamente las células
cribosas del floema `[R]` (nota: afirmación tomada de la introducción de `S44`).

**3. Maize rayado fino virus (MRFV).** Es un **marafivirus de ARN de cadena
simple de sentido positivo (+ssRNA)**, transmitido de manera persistente
propagativa `[E]` `S19`. Es decir: un virus que, como los mollicutes, se
multiplica dentro del insecto.

**4. Maize striate mosaic virus (MSMV), especie *Mastrevirus striatis*.** Es un
**virus de ADN de cadena simple** del género *Mastrevirus*, familia
*Geminiviridae* `[E]` `S31` `S33`. Su genoma es circular, de **2.746
nucleótidos**, con menos de 63 % de identidad pareada con otros aislamientos de
mastrevirus del mundo `[R]` `S31`. Fue descubierto en 2018 muestreando *D.
maidis* en Itumbiara, Goiás, Brasil `[R]` `S31`, y sólo *D. maidis* lo transmite:
no lo transmiten ni el pulgón *Rhopalosiphum maidis* ni la inoculación mecánica
`[R]` `S32`. Las tasas de transmisión reportadas son **29,4 % y 39,5 %** desde
plantas infectadas de campo y **18,5 %** desde plantas infectadas en laboratorio,
con períodos de acceso a adquisición y a inoculación de cuatro días y diez
individuos por planta test `[R]` `S32`. En invernáculo, con 17 especies
vegetales, de 9 a 30 plantas por especie y 20 chicharritas virulíferas por planta
durante 48 h, se detectó MSMV en cuatro gramíneas además del maíz, y en maíz se
detectó en **51,8 % de las plantas inoculadas, de las cuales sólo 45,9 % mostró
síntomas típicos** `[R]` `S33`. Sus síntomas en maíz son **moteado con estrías
cloróticas leves** `[R]` `S33`.

Dos aclaraciones de alcance geográfico y de modo de transmisión. CSS, MBSP y MRFV
están reportados en Estados Unidos, mientras que **MSMV asociado a achaparramiento
está reportado sólo en Brasil y Argentina** `[R]` `S10`. Y sobre el modo de
transmisión del MSMV las fuentes se contradicen: un trabajo de Embrapa afirma que
todos se transmiten de manera persistente propagativa "excepto MSMV, que se
transmite de manera persistente circulativa" `[R]` `S46`, mientras que un trabajo
argentino del mismo período declara que el modo de transmisión del MSMV sigue
siendo desconocido `[R]` `S47`. Lo dejamos como `[?]` y lo anotamos en
`preguntas_abiertas.md`, porque la diferencia no es trivial: circulativa
significa que el virus **no se multiplica** en el insecto, y eso cambia qué genes
del insecto son relevantes para bloquear esa transmisión en particular.

### 3.3 Verificación pedida: ¿cuál afecta los granos y cuál el tallo?

El prompt pide verificar específicamente si uno de los patógenos afecta los
granos por mazorca y el otro el crecimiento del tallo. **La asignación, tal como
está formulada, no se sostiene con la evidencia que encontramos.**

El trabajo que resuelve esto es un experimento de Embrapa diseñado exactamente
para eso: fitoplasma y *S. kunkelii* inoculados **por separado o
simultáneamente** en **cinco cultivares**, en macetas hasta cosecha, con plantas
sanas como control, dos plantas por maceta, y detección por PCR a 30, 60 y 100
días post-inoculación en hojas inferiores, medianas y apicales `S13`. Los
resultados `[E]` `S13`:

- La reducción en producción de grano **fue significativamente diferente
  (P < 0,01) entre fitoplasma y espiroplasma, y fue mayor cuando las plantas
  fueron infectadas por espiroplasma**.
- La reducción en altura de planta **no fue significativamente diferente** entre
  plantas inoculadas con fitoplasma, con espiroplasma o con ambos.
- La inoculación simultánea **no** produjo efecto sinergístico.

O sea: los dos achaparran, y achaparran parecido; el que castiga más el grano es
el espiroplasma. No hay un reparto de síntomas "uno el grano, el otro el tallo".
A esto se suma que la fuente de extensión más reciente que revisamos **no
atribuye síntomas por patógeno separado en absoluto**: describe el cuadro
combinado y aclara que varía con el híbrido, el estadio, el ambiente y la
combinación de patógenos presentes `[R]` `S10`. Los síntomas comunes del cuadro
combinado son estriado clorótico o amarillo sobre las nervaduras, enrojecimiento
o púrpura de márgenes y nervadura central, achaparramiento con internodios
cortos, macollaje o producción excesiva de espigas, espigas reducidas con granos
arrugados o ausentes, y el aspecto llamado *stay-green* o "planta zombi" `[R]`
`S10`.

Hay un matiz experimental importante en el mismo trabajo de los cinco cultivares:
la variabilidad fue alta (**CV = 66,7 %**) porque varias plantas inoculadas
simplemente **no se infectaron**, y los autores concluyen que la magnitud de la
reducción de producción por cultivar depende esencialmente de la **frecuencia de
plantas susceptibles a la infección**, no de un nivel de resistencia que atenúe
el daño en las ya infectadas `[E]` `S13`. El cultivar BR 201 tuvo la menor
reducción, pero también menos del 50 % de plantas infectadas `[E]` `S13`. Esto
anticipa un problema de medición que va a reaparecer cuando hablemos de
resistencia: una planta que "resiste" puede ser una planta que no se infectó, no
una planta que toleró.

### 3.4 Magnitud del daño

Las cifras disponibles son heterogéneas en método y en contexto, y conviene no
mezclarlas.

A escala de pérdida de rendimiento atribuida a los patógenos transmitidos por
*D. maidis*, el rango reportado es de **40 a 100 %** `[R]` `S01`, y otra fuente
afirma que el complejo puede causar pérdidas de hasta 100 % del rendimiento `[R]`
`S46`. En el episodio histórico del sur de Florida en 1979–1980, la caída fue del
**98,5 % del rendimiento esperado** del maíz del estado, por alimentación directa
más enfermedad, con pérdidas estimadas de hasta **60 millones de dólares** en
producción de semilla híbrida y viveros de mejoramiento `[R]` `S01` `S10`.

A escala regional y con método epidemiológico, el dato más limpio que abrimos es
de Paraná, Brasil, en safrinha: síntomas de achaparramiento en todos los cultivos
evaluados, con **incidencia de 6,2 % a 49,9 % y promedio de 20,7 %**, *D. maidis*
presente en 20 de 24 áreas y constituyendo el 66,6 % de las chicharritas
colectadas, y **pérdida estimada por molicutes de unos 16,5 millones de dólares**
`[R]` `S11`.

Para Argentina, la fuente primaria que pudimos abrir es un ensayo a campo de la
campaña **2023–2024 en cinco localidades del Noroeste argentino (NOA)** con
**14 híbridos comerciales**, confirmación de *S. kunkelii* por DAS-ELISA con
reactivos de IPAVE–CIAP–INTA, e incidencia evaluada sobre treinta plantas
consecutivas por repetición en estadio R4 `S47`. Ese trabajo reporta
**incidencias de 8 % a 100 %** según híbrido y sitio, y enuncia que en la campaña
2023–2024 Argentina sufrió un brote que afectó toda la región agrícola, "llevando
a una reducción estimada del 20 % de la producción nacional de maíz" `[R]` `S47`.
Atención con esta última cifra: en el propio artículo es **cita secundaria** de la
Bolsa de Comercio de Rosario, 2024, no un resultado del trabajo. La registramos
con esa cadena de atribución explícita.

Y acá hay una contradicción que el equipo debe conocer antes de poner cualquier
número en una presentación. Una revisión de control biológico cita, también de
manera secundaria, que "en Brasil este insecto redujo la producción de maíz en
cerca de **40 % en 2020–2022**, y en Argentina la producción de maíz se redujo
**77 % en 2023–2024**" `[R]` `S22`. El 77 % y el 20 % no son el mismo número ni
miden lo mismo, y ninguna de las dos cifras pudimos rastrearla hasta su fuente
primaria. La diapositiva oficial del Investigathón, por su parte, muestra para la
campaña 2023/2024 las cifras de **11,5 millones de toneladas** y **2.045 millones
de dólares**, sin rótulo que aclare qué mide cada una. Conclusión operativa: la
magnitud de la epifitia argentina de 2023/24 **no está resuelta con las fuentes
que abrimos** `[?]`, y cualquier presentación nuestra debería usar la cifra
atribuida (20 %, vía Bolsa de Comercio de Rosario citada en un paper revisado por
pares) o declarar el rango con su incertidumbre. Lo que no se puede hacer es
elegir el número más grande.

---

## 4. Por qué los patógenos son blancos difíciles

Esta es la pregunta central del documento: **¿hay evidencia de RNAi funcional en
bacterias y mollicutes?** Si no la hay, ¿qué implica eso para la estrategia de
"silenciar al patógeno" frente a "silenciar al vector" frente a "preparar la
defensa de la planta"? La respuesta corta es que el RNAi no opera sobre los
mollicutes, opera sobre los virus **a través de la planta**, y opera directamente
sobre el insecto. La respuesta larga, con evidencia, es ésta.

### 4.1 Lo que el RNAi necesita para existir

De la sección 2 se desprende un requisito mínimo verificable. Para que haya RNAi
canónico hacen falta, como mínimo, dos piezas: una **Dicer** —una RNasa III con
dominio PAZ que mida y corte el dsRNA— y una **Argonaute** —una proteína con
dominio PIWI que cargue la hebra guía y corte el blanco. Esto convierte una
pregunta biológica en una pregunta de bioinformática comparativa que podemos
responder nosotros mismos en minutos: ¿están esos dominios en los genomas de los
mollicutes del complejo?

### 4.2 Nuestra propia verificación sobre los mollicutes

Consultamos UniProtKB por dominio InterPro y por taxón, el 17 de octubre de 2026
(la consulta completa, reproducible, está en `notes/fuentes-nuevas.md` como
`D01`). Contamos proteínas con el dominio **PIWI** (IPR003165, el dominio
catalítico de Argonaute), con **PAZ** (IPR003100, reconocimiento del extremo del
dúplex), con el **dominio de dimerización de Dicer** (IPR005034) y, como control
positivo, con el dominio **RNasa III** (IPR000999), que es ubicuo en bacterias.

| Taxón | PIWI | PAZ | Dicer-dim. | RNasa III | proteínas en UniProtKB |
| --- | --- | --- | --- | --- | --- |
| Mollicutes | **0** | **0** | **0** | 154 | 126.874 |
| *Spiroplasma* | **0** | **0** | **0** | 30 | 36.551 |
| *Spiroplasma kunkelii* | **0** | — | — | 1 | 1.755 |
| *'Candidatus* Phytoplasma' | **0** | **0** | **0** | 43 | 24.307 |
| *Zea mays* | 79 | 66 | 15 | 43 | — |
| Hemiptera | 284 | 351 | 98 | 143 | — |
| Bacteria (todo el dominio) | 757 | 8 | 14 | 21.593 | — |

El cero no es un artefacto de falta de datos: hay 126.874 proteínas de mollicutes
anotadas, 1.755 de *S. kunkelii* sola, y el control de RNasa III da positivo en
todos los taxones. El maíz y los hemípteros tienen el juego completo de dominios.
Las bacterias como dominio sí tienen 757 proteínas con dominio PIWI —las
Argonautas procariotas— pero casi ninguna con PAZ (8) ni con el dominio de
dimerización de Dicer (14): **no hay un Dicer bacteriano**. Y dentro de
Mollicutes el conteo de PIWI es cero.

Es importante no sobreinterpretar el dato de RNasa III. Que *S. kunkelii* tenga
una proteína con dominio RNasa III no significa que tenga Dicer: RNasa III es una
familia de endonucleasas de dsRNA que en bacterias cumple funciones de
maduración de ARN ribosomal y de regulación, y Dicer es un miembro
*especializado* de esa familia que, además, necesita PAZ, helicasa y la
arquitectura de doble dominio catalítico para medir y cortar en un largo definido
`[E]` `S41` `S50`. Tener la tijera genérica no es tener la regla.

### 4.3 Qué dice la literatura sobre Argonautas procariotas

Las proteínas Argonauta sí existen en procariotas: aparecen en alrededor del
**30 % de los genomas de arqueas** y del **10 % de los genomas bacterianos**
secuenciados `[E]` `S02`. Pero su funcionamiento es otro. La evidencia
experimental proviene sobre todo de dos proteínas, TtAgo y RsAgo, y las
Argonautas procariotas "actúan preferentemente sobre blancos de ADN" `[E]` `S02`.
TtAgo genera sus propias guías de ADN a partir de ADN invasor por *chopping*;
RsAgo recoge ARN pequeños procesados por nucleasas celulares `[E]` `S02`. La
mayoría de las estudiadas son **guiadas por ADN y con blanco de ADN** (TtAgo,
MjAgo, PfAgo); algunas usan guías de ARN (RsAgo, MpAgo), y RsAgo tiene blanco de
ADN y carece de actividad slicer `[E]` `S02`. Varias pueden cortar blancos de ARN
*in vitro*, pero **el rol funcional *in vivo* es desconocido** `[?]` `S02`. La
revisión concluye que el mecanismo de represión guiada por ARN en procariotas es
**"conceptualmente muy diferente" del RNAi eucariota**, y no describe homólogos
de Dicer en bacterias ni RNAi canónico bacteriano `[E]` `S02`. De manera
coincidente, el trabajo estructural sobre la Argonauta de *Marinitoga piezophila*
enuncia la separación de plano en su apartado de significancia: las Argonautas
"son efectores clave del RNA interference **eucariota** y, en procariotas,
funcionan en la defensa del genoma del hospedador", y todas las de ese subtipo
están codificadas dentro de loci CRISPR-cas `[E]` `S42`.

### 4.4 La conclusión sobre el patógeno mollicute

Juntando las tres piezas —la ausencia verificada de los dominios en 126.874
proteínas de mollicutes, la naturaleza distinta de las Argonautas procariotas, y
el hecho de que las revisiones del campo no proponen el silenciamiento del
mollicute como estrategia— la conclusión es:

> **No existe evidencia de una vía de RNAi funcional en *Spiroplasma kunkelii*
> ni en el fitoplasma del achaparramiento, y no hay mecanismo conocido por el
> cual un dsRNA exógeno pueda silenciar un gen de esos organismos.** `[E]`

Dos observaciones que refuerzan esto desde la literatura aplicada, y que son
quizá más elocuentes que cualquier argumento. Primero: una revisión de 2026 sobre
SIGS para protección de cultivos **no discute fitoplasmas y no presenta patógenos
bacterianos como blancos de SIGS**; las bacterias aparecen únicamente como
hospedadores de expresión para producir dsRNA, como vehículos de alimentación
para insectos y como agentes de biocontrol `[E]` `S07`. Segundo: una revisión de
2026 dedicada específicamente a estrategias innovadoras contra vectores de
fitoplasmas repasa control genético, impulsores génicos, técnica del insecto
estéril, semioquímicos, nanotecnología, simbiontes y control biológico, y
**todas** sus propuestas son dirigidas al vector o a la planta; el RNAi aparece
siempre como "RNAi dirigido a la fisiología del vector" `[E]` `S44`. Esa revisión
lo dice con todas las letras: "aunque los fitoplasmas no son directamente
atacables debido a su estilo de vida restringido al floema, los tratamientos
basados en nanopartículas pueden reducir indirectamente la enfermedad al afectar
la supervivencia o el comportamiento alimenticio del vector" `[E]` `S44`.

Hay que ser preciso sobre el alcance de esta conclusión: lo que decimos es que
**no hay vía de RNAi en el mollicute**, no que el mollicute sea invulnerable. Es
perfectamente posible atacarlo por otros mecanismos —inhibidores de molécula
pequeña, interferencia con sus adhesinas, bloqueo de su entrada a las células del
insecto— y de hecho esa línea existe (sección 4.6). Lo que no existe es la
versión ingenua del esquema: pulverizar dsRNA contra un gen del espiroplasma y
esperar que el espiroplasma lo procese.

Esto tiene una implicancia directa sobre el material del organizador. La
diapositiva oficial del Investigathón describe un circuito de cuatro pasos que
termina en "inhibición del crecimiento del patógeno". Con la evidencia de esta
sección, ese enunciado **no puede leerse como silenciamiento directo del
mollicute**. O es una simplificación de la charla, o se refiere a los virus, o
implica una vía indirecta —silenciar al vector, o preparar la defensa de la
planta—. Es la primera pregunta que hay que hacerle al investigador, y está
anotada como tal.

### 4.5 Los virus: sí son blanco, pero el RNAi no ocurre "en" el virus

Un virus tampoco tiene maquinaria de RNAi: no tiene ribosomas, no tiene Dicer, no
tiene Argonaute, y en el caso del MSMV tiene 2.746 nucleótidos de genoma `[R]`
`S31`. Y sin embargo los virus **sí son blancos legítimos de RNAi**, porque el
silenciamiento no ocurre en el virus sino **en la célula vegetal infectada**: es
la planta la que corta el ARN viral con su propia maquinaria.

La defensa antiviral vegetal es un sistema completo y bien caracterizado.
Depende de DCL, AGO y RDR, y genera siRNA derivados de virus (vsiRNA) `[E]`
`S21`. DCL4 genera el vsiRNA de 21 nt, la especie dominante que dirige la defensa
potente, y además reprime la acumulación del vsiRNA de 22 nt generado por DCL2,
que es menos efectivo `[E]` `S21`. Los mutantes *dcl* simples o dobles de
*A. thaliana* son hipersusceptibles: acumulan más ARN y proteínas virales y
muestran síntomas más severos `[E]` `S21`. AGO2 es más efectiva que AGO1 para
regular la resistencia a algunos virus `[E]` `S21`. Y contra virus de ADN existe
la capa adicional del RdDM descrita en la sección 2.3: DCL3 genera altos niveles
de siRNA de 24 nt en plantas infectadas por virus de ADN, AGO4 dirige la
metilación, y esto puede actuar sobre el ADN geminiviral `[E]` `S21`. Como
contracara, los virus codifican **supresores del silenciamiento (RSS)**, ARN no
codificantes resistentes a exorribonucleasas y manipulaciones indirectas de las
vías del hospedador `[E]` `S21`: la defensa existe y el virus pelea contra ella.

Que esto se pueda disparar con dsRNA aplicado desde afuera está documentado en
muchos sistemas. La revisión más reciente que abrimos sobre control de virus
vegetales por SIGS tabula **25 combinaciones virus–cultivo** con dsRNA exógeno,
con blancos típicos en la RdRp viral, en el supresor de silenciamiento y en la
cápside `[E]` `S43`. Dos entradas de esa tabla nos tocan de cerca: una en
**maíz**, contra *sugarcane mosaic virus*, con blanco en la cápside, que reporta
inhibición de la replicación y menor acumulación del virus en maíz `[R]` `S43`;
y una contra *tomato yellow leaf curl virus*, descrita como "vacunación basada en
dsRNA contra un virus de ADN monopartito" `[R]` `S43`, que es el precedente más
cercano a un geminivirus como el MSMV.

Ahora las restricciones, que son severas. La protección antiviral del dsRNA
pulverizado **típicamente dura sólo unos pocos días** y requiere reaplicaciones
frecuentes, lo que los autores califican de impracticable para cultivos
extensivos de ciclo largo `[E]` `S43`. Una hora de exposición a UV degrada el
dsRNA y abole su actividad biológica `[R]` `S43`. Lluvias de más de 20 mm en 24 h
remueven una proporción significativa de los depósitos foliares `[R]` `S43`. Y
hay un dato que conviene tener a mano para no confundir señal con efecto: las
plantas susceptibles infectadas **generan siRNA derivados del virus en abundancia
y aun así permiten replicación, movimiento y síntomas** `[E]` `S43`. Detectar
siRNA no es demostrar protección.

Sobre los dos virus que nos importan específicamente —MRFV y MSMV— **no
encontramos ningún trabajo de dsRNA, SIGS o HIGS**. Es un hueco documentado, no
una ausencia de posibilidad `[?]`.

### 4.6 Entonces: ¿vector, patógeno o planta?

La respuesta estratégica que se desprende de todo lo anterior tiene tres vías con
pesos de evidencia muy distintos, y ordenarlas es probablemente el aporte más
útil de este documento.

**Vía 1 — silenciar al vector. Es la única con evidencia funcional directa en
nuestra especie.** Hay RNAi eficiente demostrado en *D. maidis*: se
caracterizaron sus genes centrales de RNAi y se evaluó la funcionalidad de la
maquinaria, con dsRNA entregado por inyección o por ingestión a hembras adultas
contra el gen *Bicaudal C*, obteniendo reducción significativa de transcriptos
con cambios de hasta 170 veces, menos oviposturas y alteraciones del desarrollo
de los oocitos; los autores lo declaran el primer reporte de RNAi eficiente en
*D. maidis* `[E]` `S16`. Un trabajo posterior en el mismo sistema, por
microinyección en ninfas de quinto estadio recién mudadas —n = 40 por
tratamiento, 0,25 µL por ninfa a 500 ng/µL, es decir 125 ng por insecto, con
dsRNA de β-lactamasa como control negativo— logró knockdown de **~95 % para
*burs-α* y ~90 % para *eth*** por RT-qPCR, con ecdisis incompleta, deformidad de
alas y **supervivencia a día 4 de ~10 % y ~15 % respectivamente, contra ~100 %
del control** `[E]` `S15`. Y por vía oral en dieta artificial, contra las
subunidades B y D de la ATP sintasa vacuolar, se reportó expresión reducida de
ambos genes con mortalidad significativamente mayor y deformación de alas, en un
preprint no revisado por pares `[R]` `S18`.

> **Corrección de la ola 2 — 2026-10-17.** Al abrir el original
> (`YHat-Biotech/Papers/finsc-6-1811933.pdf`, fig. 5) aparecen dos errores en el
> párrafo de arriba, que se dejan tal como se escribieron porque el historial de
> lo que creíamos es parte del valor del repositorio:
>
> 1. **Los porcentajes de supervivencia están cruzados entre especies.** En
>    *Dalbulus maidis* **los dos** genes dejaron 10 % de supervivientes —día 4
>    para *burs-α*, día 5 para *eth*—; el 17,5 % y el 20 % corresponden a
>    *Delphacodes kuscheli*. El método y los porcentajes de knockdown sí eran
>    exactos. Ver `research/ola2/CORRECCIONES.md`, entrada B5.
> 2. **El ~95 % de knockdown no es un punto de calibración:** descansa sobre tres
>    réplicas biológicas de tres ninfas cada una; las 40 son el n de
>    supervivencia, no el de la medición molecular. Entrada B6.
> 3. **Nomenclatura:** el blanco de la vía oral no es la «ATP sintasa vacuolar»
>    sino la **subunidad D de la ATPasa vacuolar de protones (V-ATPasa)**, que es
>    un complejo distinto de la ATP sintasa (F-ATPasa). Lo identificó sin
>    ambigüedad el tblastn local de W5 sobre el candidato `ATPaseD_Dm` del
>    EPILAB. Entrada E7.

**Vía 2 — silenciar al patógeno. Para los mollicutes no hay mecanismo; para los
virus, el blanco real es la planta.** Ya desarrollado. Lo que sí existe, y es
conceptualmente distinto, es **silenciar genes del vector que el patógeno
necesita**: no se ataca al patógeno, se le saca la escalera. La evidencia viene
del sistema de la flavescencia dorada en el vector experimental *Euscelidius
variegatus*: el fitoplasma entra a las células del insecto por **endocitosis
mediada por clatrina**, y el knockdown de la cadena pesada de clatrina por RNAi
inhibió la entrada a células S2 `[E]` `S29`; *in vivo*, **silenciar *clathrin*
redujo significativamente la colonización del insecto y la transmisión** a haba,
mientras que silenciar el receptor putativo *uk1_LRR* **aumentó** la colonización
sin efecto sobre la transmisión `[R]` `S27`. En la misma línea, el silenciamiento
de proteínas intestinales del vector del tipo natterin y legumaína altera la
multiplicación del patógeno `[R]` `S30`. Es la prueba de concepto más clara de
que el eje "bloquear la transmisión" es atacable por RNAi, y también la prueba de
que el signo del efecto no es predecible: uno de los dos genes probados empeoró
la colonización.

**Vía 3 — preparar la defensa de la planta.** Técnicamente viable para los dos
virus, por lo descrito en 4.5. Para los mollicutes, en cambio, "preparar la
defensa" no puede significar RNAi contra el patógeno: tendría que significar otra
cosa —tolerancia, resistencia genética, interferencia con los efectores— y eso ya
no es nuestro problema de diseño de ARN. Vale una advertencia honesta: no
encontramos evidencia de que el RNAi vegetal controle mollicutes, y la propia
lógica del mecanismo dice que no debería, porque el mollicute no traduce ARN
vegetal ni importa siRNA de la planta por ninguna vía conocida `[E]`/`[H]`.

Una última consideración que atraviesa las tres vías y que conviene tener
presente desde el principio: los patógenos limitados al floema tienen genomas
pequeños y **carecen de muchos genes requeridos para procesos metabólicos
centrales**, en parte como adaptación al ambiente del floema `[E]` `S34`. Eso
significa que, incluso si existiera una vía de entrega, la lista de genes
esenciales candidatos en el mollicute es corta y está fuertemente restringida.

---

## 5. Tratamientos existentes, con ARN y sin ARN

### 5.1 Insecticidas y el problema de la resistencia

El manejo convencional sigue dependiendo fuertemente de insecticidas, con
resistencia, efectos no objetivo y preocupaciones ambientales como límites
crecientes `[E]` `S37`. En este sistema la dependencia es casi total: **no hay
curativo para los patógenos**, de modo que el control químico apunta al vector
`[E]` `S10`.

La resistencia está documentada con números duros y es el argumento más fuerte a
favor de buscar modos de acción nuevos. Los piretroides fueron la estrategia
primaria en Brasil y se reportaron fallas de control; una cepa seleccionada en
laboratorio alcanzó una **CL50 de 2.055,72 µg i.a. mL⁻¹ frente a 0,64 µg i.a.
mL⁻¹ de la cepa susceptible, es decir una razón de resistencia de 3.170 veces**,
con herencia autosómica, incompletamente dominante y poligénica `[E]` `S23`.
Para los inhibidores de la acetilcolinesterasa el cuadro es el mismo en
desarrollo: una cepa derivada de una población de campo de Goiás pasó de una razón
de resistencia de **9,73 a 163,42 veces en 26 generaciones** de presión de
selección con metomil `[E]` `S24`.

El tratamiento de semilla, muy usado en la región, tiene una ventana corta y bien
medida. En un ensayo de Embrapa, imidacloprid/tiodicarb fue el más efectivo en
estadio **V2**, con **100 % de mortalidad de chicharritas sanas y 85,7 % de las
infectivas**, previniendo la transmisión del espiroplasma; tiametoxam y
metomil + fipronil/tiametoxam dieron alta mortalidad total a las 72 h sólo para
las infectivas, con mortalidad de las sanas en torno al 40 %, y redujeron el
número de plantas con síntomas en **80 % y 90 %** respectivamente `[R]` `S46`.
Dos hallazgos de ese trabajo merecen subrayado: el tratamiento de semilla **fue
efectivo sólo hasta V2**, y las chicharritas infectadas resultaron **más
susceptibles** a los insecticidas que las sanas `[R]` `S46`.

### 5.2 Resistencia y tolerancia genética del maíz

Hay híbridos con susceptibilidad diferencial reportados en Brasil y Argentina,
pero **sin información para híbridos comerciales de Estados Unidos** `[R]` `S10`.
La investigación argentina separó los componentes de esa resistencia en cuatro
híbridos comerciales —dos de la región templada y dos de la tropical— mediante
ensayos de **antixenosis** (la planta es un hospedador no preferido, lo que
reduce el tiempo de contacto y con él la eficiencia de transmisión) y de
**antibiosis** (la planta afecta la biología del insecto que sí se alimenta), más
resistencia al patógeno bajo inoculación artificial con alta presión de insectos
infectivos en condiciones de no elección `S45`. Resultados: DK72-10 mostró
antixenosis y antibiosis al vector; DK79-10 mostró resistencia a *S. kunkelii*
como retraso en la aparición de síntomas; DKB390 mostró antixenosis al vector y
resistencia al patógeno `[E]` `S45`.

El hallazgo de ese trabajo que más nos sirve es otro, y es casi un aviso
metodológico: **hubo asociación entre severidad de síntomas y reducción de
rendimiento, pero no entre acumulación del patógeno y severidad, ni entre
acumulación y rendimiento** `[E]` `S45`. El título del patógeno no predice el
daño. Si alguna vez proponemos un indicador de eficacia, "menos patógeno" no es
automáticamente "menos pérdida".

A campo y a escala de campaña, el ensayo de 14 híbridos en cinco localidades del
NOA en 2023–2024 cuantificó la relación: con un modelo de regresión lineal mixta
con efecto aleatorio de localidad, **el índice de severidad explica el 72 % de la
variabilidad del desempeño, y cada unidad adicional de severidad se asocia a una
reducción promedio de 15,96 kg/ha** `[E]` `S47`. Las incidencias fueron de 8 % a
100 % según híbrido y sitio `[E]` `S47`.

### 5.3 Manejo cultural y control biológico

El paquete de manejo cultural recomendado es: sembrar lo más temprano posible,
**eliminar el maíz guacho** (plantas voluntarias que funcionan como "puente
verde" entre campañas) y rotar con cultivos no gramíneos como soja, algodón o
maní `[R]` `S10`. La lógica epidemiológica es la del puente verde: el vector es
especialista de *Zea* `[E]` `S01`, así que sin maíz vivo entre campañas la
cadena se corta.

En control biológico, el componente más prometedor son los **parasitoides de
huevo**. *Anagrus virlai* (Mymaridae) y *Paracentrobia subflava*
(Trichogrammatidae) presentan los porcentajes de parasitismo más altos de las
Américas, y en México, donde coexisten, **más del 80 % de las hojas
experimentales de maíz con huevos de *D. maidis* resultaron parasitadas**; en
Sudamérica *A. virlai* es el parasitoide de huevo más abundante `[R]` `S22`. La
ventaja conceptual es grande: atacan el huevo **antes de que emerjan las ninfas,
que ya pueden transmitir los tres patógenos** `[R]` `S22`. Hay además unas 40
especies de artrópodos predadores que atacan ninfas o adultos en las Américas
`[R]` `S22`.

Los **hongos entomopatógenos** (*Beauveria*, *Metarhizium*, *Cordyceps*) tienen
un problema estructural frente a la transmisión persistente propagativa: su uso
contra adultos portadores está limitado por el **retraso en matar al vector**, la
**baja tasa de mortalidad** y la barrera de los **brocosomas** que produce la
chicharrita `[R]` `S22`. Otras líneas exploradas son nematodos entomopatógenos
(*Heterorhabditis*, *Steinernema*), evaluados en laboratorio contra adultos `[R]`
`S38`, y *Chromobacterium piscinae*, con mortalidad de **74,5 % a 78,7 %** en
tratamientos con células y **sin relación dosis-respuesta** en un rango de
3,5×10⁴ a 6,7×10⁹ células/mL `[R]` `S39`.

### 5.4 El lado del ARN: las plataformas y su madurez

Conviene fijar el vocabulario antes de comparar, porque las tres siglas se
confunden todo el tiempo.

**SIGS (*spray-induced gene silencing*)** es aplicar dsRNA o siRNA sobre
superficies vegetales para que la plaga o el patógeno lo capte y silencie genes
blanco, sin plantas transgénicas; también se lo llama RNAi ambiental `[E]` `S07`.
La entrega puede ser por pulverización foliar, tratamiento de semilla, inyección
de tronco o captación por raíz `[E]` `S43`.

**HIGS (*host-induced gene silencing*)** es que la **planta transgénica** exprese
el dsRNA y lo entregue al organismo que la ataca `[E]` `S43`. El ejemplo
comercial relevante es el maíz MON87411, que combina proteínas Bt con el casete
**DvSnf7**, el cual produce dsRNA dirigido específicamente a los genes *Snf7* del
gusano de la raíz del maíz occidental (*Diabrotica virgifera virgifera*) `[E]`
`S20`.

**VIGS (*virus-induced gene silencing*)** usa un vector viral recombinante para
expresar la secuencia dentro de la planta y disparar el silenciamiento; en la
práctica se usa mucho como herramienta de genómica funcional y es uno de los
formatos de salida de los diseñadores de siRNA vegetales `[E]` `S49`.

Sobre **madurez y evidencia a campo** hay que ser francos. La mayoría de los
resultados publicados son de laboratorio, invernáculo o dieta artificial, y "se
realizaron pocos estudios de campo" `[E]` `S07`. Las barreras declaradas para la
comercialización son incertidumbre regulatoria, alto costo de producción del
dsRNA, **datos comparativos de eficacia a campo limitados**, preocupaciones
sociales y falta de validación amplia para la evaluación de riesgo ambiental
`[E]` `S20`. Dicho esto, la frontera ya se cruzó: **en 2023 la EPA aprobó el
primer insecticida basado en dsRNA, ledprona**, contra el escarabajo de la papa
de Colorado, registrado como biopesticida con **EPA Reg. No. 94614-2**; el dsRNA
es de **490 pares de bases** y se produce con una plataforma propietaria de
bioprocesamiento libre de células `[E]` `S20`. Un producto de dsRNA contra el
ácaro *Varroa*, vadescana, también llegó a comercialización `[R]` `S20`.

Sobre **costos**, los ingredientes activos de productos fitosanitarios
convencionales suelen costar **10 a 100 € por gramo** `[R]` `S20`. Para el dsRNA,
la síntesis química es precisa pero costosa e ineficiente para moléculas largas,
mientras que la síntesis biotecnológica en *E. coli* o *Bacillus subtilis*
permite reducciones sustanciales, con **costos proyectados por debajo de 1 USD/g**
y, en sistemas libres de células optimizados, **alrededor de 0,50 USD/g** `[R]`
`S20`. Detalles de proceso reportados: reemplazar LB por Terrific Broth aumenta
la producción un **118 %**, y la inducción con lactosa a 6 g L⁻¹ puede dar niveles
hasta diez veces mayores `[R]` `S20`. Otra fuente cita a RNAGri produciendo
toneladas a ~1 USD/g `[R]` `S07`, y una tercera confirma el umbral de menos de
1 USD/g con plataforma libre de células, contra varios cientos de dólares por
gramo de la síntesis *in vitro* clásica `[R]` `S43`.

Sobre **estabilidad ambiental y portadores**, ya vimos los números de
degradación. Las estrategias de encapsulación más citadas son quitosano,
liposomas y nanoláminas de arcilla; varios estudios reportan actividad mayor y
más prolongada con portadores frente a dsRNA desnudo `[E]` `S20`. El quitosano y
las nanoarcillas LDH extendieron la protección hasta **20 días** en un trabajo
`[R]` `S07`, y las nanoarcillas LDH —"BioClay"— protegen de la degradación y del
lavado **por al menos 30 días** en otro `[R]` `S43`. Un dato relevante para
cualquier cálculo de riesgo: la degradación rápida es ventajosa ambientalmente
pero compromete la eficacia si no hay captación `[E]` `S20`.

Sobre **regulación**, en Estados Unidos los productos de dsRNA se clasifican como
pesticidas bioquímicos y los regula la EPA bajo FIFRA y FFDCA `[E]` `S20` `S43`.
En la Unión Europea las plantas HIGS caen bajo la Directiva 2001/18 o el
Reglamento 1829/2003, y los productos de dsRNA no-OGM se evalúan bajo el
Reglamento 1107/2009 en un proceso de dos etapas `[E]` `S20`. En agosto de 2024
la EFSA aprobó el maíz MON95275 para uso pleno en alimentación humana y animal, y
en enero de 2025 completó un proyecto de tres años para mejorar las metodologías
de evaluación de riesgo de plantas GM basadas en RNAi, cuya opinión resultante
confirmó que los marcos existentes son en general adecuados para plantas HIGS
`[E]` `S20`. La ingestión de dsRNA por dieta se considera improbable que
represente riesgo para la salud, pero **la evaluación de riesgo ambiental debe
considerar interacciones específicas de secuencia y las limitaciones de
predicción** `[E]` `S20`. En Australia la OGTR considera a SIGS como no-OGM bajo
ciertas condiciones; en Corea del Sur todavía no hay lineamientos formales `[R]`
`S43`.

### 5.5 El cuello de botella declarado: las nucleasas del insecto

Hay una barrera específica de nuestro sistema que merece su propia subsección,
porque el propio organizador la declaró como la pregunta abierta número dos.

Las **nucleasas degradan el dsRNA** antes de que llegue a destino: hay dsRNasas
salivales y del intestino medio, demostradas en el pulgón del guisante, la
langosta del desierto y el gusano de seda `[E]` `S08`. En *D. maidis* esto está
caracterizado: se identificaron y caracterizaron **tres dsRNasas**, con
**Dmai-dsRNase-2 altamente expresada en intestino medio y glándulas salivales**,
y un ensayo de degradación *ex vivo* mostró actividad nucleasa significativa y
**alta inestabilidad del dsRNA** expuesto a homogenatos de tejido `[E]` `S17`.
Esa es la razón de que "el dsRNA administrado oralmente sea menos efectivo que
los protocolos de inyección" `[E]` `S17`. Y hay una salida propuesta y probada:
**silenciar Dmai-dsRNase-2 mejoró la respuesta del insecto al dsRNA del gen de
interés**, de donde los autores proponen coadministrar dsRNA contra la dsRNasa y
contra el gen blanco `[E]` `S17`.

La otra salida reportada es química. Incorporar **nucleótidos pirimidina 2′-F
modificados** al disparador, con 32 a 55 % de nucleótidos 2′-F, mejoró la
actividad de RNAi y **aumentó la mortalidad del insecto entre 12 y 35 %** frente a
disparadores no modificados de la misma secuencia, de manera repetible en
*Diaphorina citri*, *Bemisia tabaci* y la chicharrita *Homalodisca vitripennis*
`[R]` `S25`. El mecanismo propuesto es mayor resistencia a la degradación por
nucleasas, con mayor afinidad de unión al ARNm blanco `[R]` `S25`.

Y conviene cerrar la sección con la limitación general que afecta justamente a
los insectos chupadores de savia: "mientras los insectos masticadores pueden
ingerir eficientemente el dsRNA aplicado en superficie, las plagas chupadoras de
savia dependen fuertemente de la captación vascular, que a menudo es ineficiente"
`[E]` `S43`. *D. maidis* es exactamente eso: un chupador de floema.

---

## 6. Diseño de dsRNA como problema de ingeniería

### 6.1 Las variables de decisión

Diseñar un disparador de dsRNA es elegir, en orden: **qué gen** silenciar, **qué
región del transcrito** usar, **qué largo** darle, y **verificar** que esa
secuencia no coincida con transcritos de organismos no objetivo. Cada una de esas
decisiones tiene evidencia asociada.

**Elección del gen.** Los genes que funcionaron en *D. maidis* o en vectores
emparentados dan la pista: *Bicaudal C* por su rol en la ovogénesis `[E]` `S16`,
*burs-α* y *eth* por su rol en la ecdisis `[E]` `S15`, subunidades de la ATP
sintasa vacuolar `[R]` `S18`, la cadena pesada de clatrina por su rol en la
entrada del patógeno al insecto `[R]` `S27` `S29`, y la propia dsRNasa como
coadyuvante `[E]` `S17`. Una plataforma reciente ofrece además identificar
ortólogos en la plaga de genes que resultaron blancos efectivos en un tamizaje de
RNAi genoma-completo en *Tribolium castaneum* `[R]` `S06`.

**Largo del disparador.** Para captación celular eficiente se cita un mínimo de
alrededor de **60 pares de bases** `[R]` `S06`; en *Tribolium*, un dsRNA de 60 pb
dio ~70 % de knockdown y uno de 30 pb apenas ~30 % `[E]` `S08`. La mayoría de los
estudios usa **140 a 500 nt** `[E]` `S08`, los dsRNA pesticidas son típicamente
de **200 a 500 pb** `[R]` `S06`, y hay una recomendación general de **200 a 1000
pb** para asegurar silenciamiento eficiente `[R]` `S20`. El producto aprobado por
la EPA, ledprona, es de **490 pb** `[E]` `S20`.

**Región del transcrito.** Apuntar al ORF en lugar de al UTR se asoció con mayor
eficacia del dsRNA `[R]` `S06`. Dirigir el extremo 3′ funcionó mejor en un
estudio en mosquito pero no en el pulgón del guisante `[?]` `S08`. La
recomendación operativa de la literatura es tamizar varios dsRNA por gen en lugar
de confiar en uno `[E]` `S08`.

**Conservación entre poblaciones.** Es una variable de diseño real: si la
secuencia elegida varía entre poblaciones del objetivo, el producto funciona en
una región y no en otra. Para los patógenos, la variabilidad genética reportada
es muy estrecha —la espiralina de *S. kunkelii* tiene 98 % de similitud entre
aislamientos brasileños, y el 16S rDNA del fitoplasma es completamente similar
entre aislamientos brasileños `[R]` `S12`—, pero para *D. maidis* no tenemos esa
medida en las fuentes que abrimos `[?]`.

**Asimetría termodinámica y accesibilidad.** Son las dos variables físicas del
problema, y conviene enunciarlas con precisión porque es donde el equipo tenía un
malentendido. La **asimetría termodinámica** es la diferencia de energía de
apareamiento entre los dos extremos del dúplex de siRNA: la hebra cuyo extremo 5′
aparea más débilmente es la que se carga preferentemente como guía. La
**accesibilidad estructural** es la probabilidad de que la región del ARNm blanco
esté de cadena simple y por lo tanto disponible para el apareamiento, en lugar de
secuestrada en una estructura secundaria propia.

Las reglas concretas publicadas, con su fuente: en el diseñador si-Fi, **U o A en
el extremo 5′**, MFE del extremo 5′ mayor que el de la hebra opuesta, y **ΔMFE de
los tres primeros nucleótidos mayor que 1 kcal/mol**, con umbral de accesibilidad
por defecto de 0,1 `[E]` `S05`. En la herramienta de diseño de ARN pequeños
artificiales de plantas P-SAMS, **U en 5′ preferida por AGO1**, C en la posición
19 para que la pasajera tenga una G 5′ no preferida, y un apareamiento erróneo en
la posición 21 para limitar la transitividad `[E]` `S09`.

Y un resultado que contradice parte de la intuición heredada de la literatura de
siRNA humano, medido en insectos: en el análisis de la plataforma dsRIP, la
asimetría termodinámica y la estructura secundaria de la hebra antisentido
resultaron predictivas de eficacia, y la **adenina en la posición 10 del
antisentido** también; en cambio **la accesibilidad del ARNm no fue
significativa**, tampoco el contenido GC global ni la energía de unión
antisentido–blanco, y el contenido GC en las posiciones 9 a 14 del antisentido se
asoció **positivamente** con la eficacia, "lo opuesto a la literatura de siRNA
humano" `[R]` `S06`. Los números de validación de esa plataforma: modelo de Cox
sobre 31 siRNA en *T. castaneum* con **C de Harrell = 0,76 (IC 95 % 0,73–0,79)**,
regresión múltiple sobre bioensayos de dsRNA con **R múltiple = 0,79**, y dsRNA de
puntaje alto que produjeron en promedio **20,1 % más siRNA antisentido** que los
de puntaje bajo dirigidos al mismo gen (P = 0,018, en 7 de 8 genes) `[R]` `S06`.

**Ausencia de coincidencias en organismos no objetivo.** Es la contracara de
riesgo obligatoria. El minimizador de off-targets de dsRIP coteja todos los siRNA
posibles contra los transcriptomas de especies no objetivo seleccionadas,
permitiendo **1 a 2 mismatches**, y computa un puntaje de seguridad que pondera
más fuerte los hits a ortólogos de genes esenciales, con un peso **20:1 por
defecto** `[R]` `S06`. Es, hasta donde abrimos, el tratamiento cuantitativo más
explícito del riesgo no objetivo en una herramienta de diseño.

### 6.2 La corrección que el equipo necesitaba: BLAST no calcula termodinámica

Las notas del equipo afirmaban que "BLAST separa en porciones y calcula la
termodinámica". **Es un malentendido, y conviene desarmarlo con precisión porque
dos de nuestras líneas de trabajo dependen de entender bien esta separación.**

**BLAST** es un programa de búsqueda de similitud de secuencias: busca
rápidamente en una base de datos coincidencias con una secuencia de consulta
`[E]` `S03`. Su arquitectura tiene tres módulos. *Setup* lee la consulta, filtra
opcionalmente regiones de baja complejidad y construye una tabla de lookup de
palabras. *Scanning* busca en cada secuencia sujeto los hits de palabra; los hits
inician alineamientos sin gaps, los que superan un umbral disparan alineamientos
con gaps, y los que superan un segundo umbral se guardan como coincidencias
preliminares. *Trace-back* calcula inserciones y deleciones de los alineamientos
guardados `[E]` `S03`. El puntaje usa una matriz de sustitución para proteínas, o
scores de match y mismatch con penalidades de gap para nucleótidos, y reporta un
valor *expect* (E-value) que da la significancia estadística del alineamiento
`[E]` `S03`. **El artículo primario de BLAST+ no menciona energía libre,
estructura secundaria de ARN ni ningún cálculo termodinámico** `[E]` `S03`.

La termodinámica la calcula otra familia de software. **ViennaRNA**: `RNAfold`
calcula la estructura de mínima energía libre (MFE) y, con la opción `-p`, usa el
algoritmo de McCaskill para la función de partición y la matriz de probabilidades
de apareamiento de bases; el modelo de energía por defecto es el de vecino más
cercano con **parámetros Turner 2004** `[E]` `S04`. `RNAplfold` calcula
probabilidades de apareamiento promediadas sobre ventanas y, con `-a`,
**accesibilidades locales**, es decir la probabilidad de que un intervalo esté de
cadena simple `[E]` `S04`. `RNAup` calcula primero **energías locales de apertura**
para ambas moléculas y luego energías de interacción para encontrar el mejor
sitio `[E]` `S04`. `RNAcofold` concatena las dos moléculas y calcula una
estructura secundaria común `[E]` `S04`.

Es decir: **son dos ejes ortogonales del problema.** BLAST y Bowtie viven en el
eje de la **especificidad** —¿a qué se parece esta secuencia, y por lo tanto qué
podría silenciar de más?—. ViennaRNA vive en el eje de la **eficacia física**
—¿esta hebra se va a cargar, este sitio está accesible?—. Confundirlos lleva a
dos errores concretos: creer que un buen E-value dice algo sobre si el siRNA va a
funcionar, y creer que un ΔG favorable dice algo sobre si el diseño es seguro
para organismos no objetivo. Ninguna de las dos cosas es cierta.

### 6.3 Qué calcula cada herramienta, concretamente

| Herramienta | Qué es | Qué calcula | Qué **no** calcula |
| --- | --- | --- | --- |
| **BLAST+** `S03` | Alineamiento local heurístico, semilla y extensión | Alineamientos, bit score, E-value; filtrado de baja complejidad | Energía libre, estructura secundaria, nada termodinámico `[E]` |
| **Bowtie** `S48` | Alineador de lecturas cortas con índice Burrows-Wheeler | Posiciones de alineamiento con mismatches, vía backtracking consciente de la calidad; >25 M lecturas/hora de CPU en genoma humano con ~1,3 GB de memoria | Energía libre, accesibilidad `[E]` |
| **ViennaRNA** (`RNAfold`, `RNAplfold`, `RNAup`, `RNAcofold`) `S04` | Paquete de termodinámica de ARN, modelo Turner 2004 | MFE, función de partición, probabilidades de apareamiento, accesibilidad local, energías de apertura e interacción | Similitud de secuencia, off-targets `[E]` |
| **si-Fi21 / si-Fi** `S05` | Diseñador de disparadores largos y predictor de off-targets | Enumera **todos los x-meros** del disparador por ventana deslizante, los mapea con **Bowtie** (no BLAST) contando mismatches, aplica reglas de selección de hebra y filtra por accesibilidad calculada con **RNAplfold** | No simula el corte real de Dicer; su "termodinámica" es la MFE de las regiones terminales del dúplex, no un ΔG completo `[E]` |
| **dsRIP** `S06` | Plataforma de diseño para control de plagas | Buscador de blancos efectivos por ortología con el tamizaje de *T. castaneum*, optimizador de eficacia por región, minimizador de off-targets con 1–2 mismatches y puntaje de seguridad 20:1, diseñador de primers; usa ViennaRNA, Bowtie1, Primer3, OrthoFinder, TransDecoder, CD-HIT | No usa BLAST ni RNAup; no predice entrega ni formulación `[R]` |
| **pssRNAit** `S49` | Servidor de diseño de siRNA **de plantas** | Pool de siRNA para silenciar **genes vegetales**, para armar dsRNA largo y expresarlo por VIGS o syn-tasiRNA; evaluación de off-targets genoma-completo; >160 especies vegetales | No sirve para diseñar contra un insecto: sus bases y reglas son vegetales `[R]` |
| **P-SAMS** `S09` | Diseñador de ARN pequeños artificiales de plantas | Dúplex definidos con reglas de nucleótido en posiciones 5′, 19 y 21 | Idem: dominio vegetal `[E]` |

Un detalle de si-Fi que vale la pena porque es exactamente lo que el equipo creía
que hacía BLAST: si-Fi **sí** "divide el disparador en todos los x-meros
posibles" con x elegido por el usuario, por enumeración exhaustiva con ventana
deslizante `[E]` `S05`. Esa operación existe, pero no la hace BLAST; la hace el
diseñador, y después usa Bowtie para mapear. Y su modo de alta eficiencia —reglas
más estrictas de selección de hebra más filtro de accesibilidad— **correlacionó
mejor con los datos experimentales de silenciamiento** que el modo de alta
sensibilidad `[E]` `S05`. Es decir: la parte termodinámica aporta, pero aporta
dentro de la herramienta de diseño, no dentro del alineador.

---

## Lo que esto implica para nuestro proyecto

**1. El blanco realista es el vector, no el patógeno.** La verificación propia
sobre 126.874 proteínas de mollicutes —cero dominios PIWI, cero PAZ, cero
dimerización de Dicer, con control positivo de RNasa III— más la literatura sobre
Argonautas procariotas y el hecho de que ninguna revisión del campo propone
silenciar al mollicute, convergen en lo mismo: **no hay mecanismo por el cual un
dsRNA silencie un gen de *Spiroplasma kunkelii* o del fitoplasma**. Cualquier
propuesta nuestra que prometa eso es falsa. Los dos virus sí son atacables, pero
a través de la maquinaria de la planta, y para MRFV y MSMV en particular no
existe ni un solo trabajo publicado que hayamos podido encontrar. Queda el
vector, donde hay RNAi funcional demostrado en la especie exacta, con genes,
dosis y fenotipos medidos.

**2. Hay un segundo blanco elegante: los genes del vector que el patógeno
necesita.** Silenciar *clathrin* en un vector de fitoplasma redujo la
colonización del insecto y la transmisión a la planta; silenciar el receptor
putativo la aumentó. Eso define un objetivo de diseño distinto de "matar al
insecto" —"desarmar la transmisión"— con precedente experimental y con un
recordatorio de que el signo del efecto no es predecible sin medirlo.

**3. El problema de diseño es multiobjetivo y la mayoría de los términos ya
tienen fórmula publicada.** Eficacia por asimetría termodinámica y estructura de
la hebra antisentido; especificidad por conteo de coincidencias con 1–2
mismatches contra transcriptomas no objetivo, ponderando más los ortólogos de
genes esenciales; largo en la banda de 200 a 500 pb; preferencia por ORF sobre
UTR `S06` `S20`. Son términos calculables sobre secuencia, que es exactamente lo que un
equipo sin laboratorio puede computar.

**4. Dos parámetros tienen el signo invertido respecto de la literatura humana, y
eso es una trampa para cualquier modelo preentrenado.** En insectos, la
accesibilidad del ARNm no fue predictiva y el contenido GC en las posiciones 9–14
del antisentido se asoció positivamente con la eficacia, al revés que en siRNA
humano. Un modelo entrenado con datos de células humanas va a traer esos
coeficientes con el signo equivocado.

**5. El largo del siRNA lo decide el insecto, no nosotros, y para hemípteros no
está medido.** Dicer-2 produce 20, 21 o 22 nt según el orden, y no hay perfil
publicado para Hemiptera `S50`. Si nuestro pipeline enumera 21-meros por defecto, está
asumiendo un parámetro que nadie midió en nuestra especie. Conviene que sea un
parámetro explícito del modelo y no una constante escondida.

**6. La entrega es el cuello de botella, y es parcialmente modelable.** Tres
dsRNasas caracterizadas en *D. maidis*, con Dmai-dsRNase-2 en intestino medio y
glándulas salivales; dsRNA oral menos efectivo que inyectado; saturación del RISC
alrededor de 100 ng/µL en un hemíptero emparentado `S26`; silenciamiento que dura 3 a 5
días sin reaplicación `S26`; una hora de UV suficiente para abolir la actividad y más de
20 mm de lluvia suficientes para lavar el depósito `S43`; las tres dsRNasas vienen de `S17`. Nada de esto se resuelve con
secuencia, pero todo esto define **bajo qué condición** se propone cada candidato,
y declararlo es parte del entregable.

**7. Sin anotación del vector, no hay pipeline.** El transcriptoma de *D. maidis*
existe —56.116 transcriptos— pero el insumo más básico de cualquier análisis de
off-target es un conjunto de transcritos anotado del objetivo y de las especies
no objetivo del agroecosistema del maíz argentino. Es el primer costo fijo del
proyecto y conviene presupuestarlo antes que cualquier modelo.

**8. Y una restricción de honestidad que vale como criterio de evaluación.** El
título del patógeno no predice el daño: en híbridos argentinos hubo asociación
entre severidad y rendimiento, pero no entre acumulación del patógeno y severidad
ni rendimiento. Si alguna vez proponemos una métrica de éxito, "menos patógeno"
no es "menos pérdida". Y la generación de siRNA tampoco es prueba de protección:
las plantas susceptibles producen siRNA virales en abundancia y se infectan
igual.
