# Glosario parcial — R1 Fundamentos

Todos los términos usados en `REPORT.md`, con definición de una línea y por qué
nos importa. Orden temático, no alfabético, para que se pueda leer de corrido
junto con el reporte. Los términos en inglés van entre paréntesis.

## Lo básico de la información biológica

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **ADN** | Polímero de doble hebra de A, C, G, T que almacena la información genética; las hebras son complementarias. | La complementariedad es lo que hace que "buscar una secuencia parecida" tenga sentido físico y no sólo combinatorio. |
| **ARN** | Polímero de una sola hebra, con ribosa y con U en lugar de T, producido al leer el ADN. | Es la molécula que diseñamos, la que aplicamos y la que destruimos. |
| **Gen** | Tramo de ADN que se lee para producir una molécula funcional. | Es la unidad que elegimos silenciar. |
| **Transcripción** | Lectura de un gen para producir ARN. | El silenciamiento post-transcripcional no la detiene; el transcripcional sí. |
| **Transcrito** (*transcript*) | El producto concreto de transcribir un gen en un momento dado. | Es la entrada real de nuestros algoritmos: un gen puede dar varios transcritos distintos. |
| **Traducción** | Lectura del ARNm por el ribosoma para ensamblar una proteína. | El RISC puede reprimirla sin cortar el mensaje. |
| **ARN mensajero (ARNm, mRNA)** | Transcrito que codifica una proteína. | Es el blanco del RNAi post-transcripcional. |
| **ORF** (*open reading frame*, marco abierto de lectura) | La porción del ARNm que efectivamente se traduce. | Apuntar al ORF se asoció con mayor eficacia del dsRNA que apuntar al UTR. |
| **UTR** (*untranslated region*, región no traducida) | Las regiones 5′ y 3′ del ARNm que no codifican proteína pero regulan su estabilidad y traducción. | Es una de las decisiones de diseño: qué región del transcrito usar. |

## Clases de ARN

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **ARN no codificante (ncRNA)** | ARN funcional que no produce proteína. | Categoría que contiene a todos los reguladores que usamos. |
| **microARN (miRNA)** | ARN endógeno corto, de 20 a 24 nt, que regula negativamente otros genes, muchas veces con apareamiento imperfecto. | Es la vía que la sobresaturación de dsRNA puede alterar, causando letalidad inespecífica. |
| **siRNA** (*small interfering RNA*) | ARN pequeño derivado del corte de un dsRNA largo, que aparea con su blanco de forma perfecta o casi perfecta. | Es la molécula efectora que nuestro diseño produce indirectamente. |
| **lncRNA** (ARN largo no codificante) | ARN funcional de más de 200 nt sin potencial codificante, de baja abundancia y baja conservación. | No es nuestra herramienta; se incluye para no confundirlo con las clases anteriores. |
| **ARN de doble cadena (ARNdc, dsRNA)** | Dos hebras de ARN complementarias apareadas; raro en condiciones normales y firma típica de infección viral. | Es el disparador que aplicamos; la célula lo trata como alarma. |
| **vsiRNA** | siRNA derivado de un virus, generado por la planta a partir del ARN viral. | Su presencia indica que la defensa se activó, pero no prueba que la planta esté protegida. |
| **syn-tasiRNA / atasiRNA** | Dúplex de 21 nt diseñados y expresados desde precursores *TAS* ingenierizados, con registro de corte definido. | Es el extremo de "precisión" del espacio de diseño que plantea el organizador: dúplex predefinidos en vez de pool heterogéneo. |

## El mecanismo

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **RNAi** (*RNA interference*, interferencia por ARN) | Mecanismo por el cual un ARN pequeño guía la destrucción o represión secuencia-específica de un transcrito complementario. | Es el mecanismo entero del proyecto. |
| **Dicer** | RNasa III que reconoce dsRNA largo y lo corta en dúplex cortos de largo definido. | Define el largo del siRNA, y ese largo depende del organismo, no del diseñador. |
| **Dicer-2** | La Dicer de insectos especializada en dsRNA largo exógeno y viral. | Su variación entre órdenes explica por qué el largo del siRNA cambia de 20 a 22 nt según el insecto. |
| **DCL** (*Dicer-like*) | Las Dicer de plantas; *Arabidopsis* tiene cuatro (DCL1–DCL4). | DCL4 hace el vsiRNA de 21 nt dominante y DCL3 el de 24 nt que alimenta el RdDM. |
| **Dominio PAZ** | Dominio que reconoce el extremo característico del dúplex (saliente de 2 nt en 3′), presente en Dicer y en Argonaute. | Junto con RNasa III forma la "regla molecular" que mide el largo del producto. |
| **Dominio PIWI** | Dominio catalítico de Argonaute, con plegamiento tipo RNasa H y tríada DDX cuando corta. | Su ausencia en un genoma es evidencia directa de que no hay Argonaute: es el dominio que contamos en los mollicutes. |
| **Dominio MID** | Dominio de Argonaute que une el fosfato 5′ de la hebra guía. | Mutarlo abole el corte, a diferencia de mutar PAZ: el extremo 5′ manda. |
| **RNasa III** | Familia de endonucleasas que cortan ARN de doble cadena; ubicua en bacterias. | Que un mollicute la tenga **no** significa que tenga Dicer: es la tijera genérica, no la regla. |
| **Argonaute (AGO)** | Proteína que carga la hebra guía y ejecuta el silenciamiento; *Arabidopsis* tiene diez. | Es el efector; sin ella no hay RNAi. |
| **RISC** (*RNA-induced silencing complex*) | El complejo Argonaute + hebra guía que busca y corta el transcrito blanco. | Es el "motor de búsqueda" biológico; se satura a dosis altas de dsRNA. |
| **Hebra guía / hebra pasajera** | De las dos hebras del dúplex, la que se conserva en el RISC y la que se degrada. | Si se carga la equivocada, el complejo busca la secuencia equivocada: es el núcleo del problema de diseño. |
| **Semilla** (*seed*) | Los nucleótidos 2 a 6 de la hebra guía, que inician la unión al blanco. | Determina la especificidad efectiva y, por lo tanto, el riesgo de off-target. |
| ***Slicer*** | La actividad de corte endonucleolítico del dominio PIWI. | No todas las Argonautas la tienen; de las cuatro humanas, sólo Ago2. |
| **Knockdown** | Reducción parcial de la expresión de un gen, medida típicamente por RT-qPCR. | Es la métrica de eficacia que reportan los papers (por ejemplo ~95 % para *burs-α* en *D. maidis*). |
| **PTGS** (silenciamiento post-transcripcional) | El gen se sigue transcribiendo y lo que se destruye es el transcrito. | Es el modo de acción del dsRNA clásico. |
| **TGS** (silenciamiento transcripcional) | El locus deja de transcribirse por modificación epigenética. | Es otra categoría, con otra persistencia; el organizador la pone como cuarto nivel de su espacio de diseño. |
| **RdDM** (*RNA-directed DNA methylation*) | Vía vegetal donde siRNA de 24 nt cargados en AGO4 dirigen la metilación del ADN del locus. | Es la defensa epigenética contra virus de ADN, y uno de los cuatro patógenos es un virus de ADN. |
| **RdRP / RDR** (ARN polimerasa dependiente de ARN) | Enzima que usa ARN como molde para sintetizar más ARN y amplificar la señal de silenciamiento. | Las plantas la tienen y amplifican; en insectos no se encontró homólogo claro, así que no se puede contar con amplificación. |
| **SID-1 / SID-2** | Proteínas del sistema de diseminación sistémica del silenciamiento en nematodos. | Los insectos carecen de homólogos: la señal no se disemina sola. |
| **ARN exógeno / RNAi ambiental** | ARN aplicado desde afuera (pulverizado, ingerido, inyectado, por raíz) que la maquinaria endógena toma como propio. | Es el formato de intervención del desafío. |

## Las plataformas de aplicación

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **SIGS** (*spray-induced gene silencing*) | Aplicar dsRNA o siRNA sobre la superficie vegetal, sin transgénesis. | Es el escenario que plantea la diapositiva oficial: pulverización sobre la planta. |
| **HIGS** (*host-induced gene silencing*) | Que la planta transgénica exprese el dsRNA y se lo entregue al organismo que la ataca. | Precedente comercial: el maíz MON87411 con el casete DvSnf7. |
| **VIGS** (*virus-induced gene silencing*) | Usar un vector viral recombinante para expresar la secuencia dentro de la planta. | Es uno de los formatos de salida de los diseñadores de siRNA vegetales. |
| **Portador / nanoportador** | Material que encapsula el dsRNA para protegerlo y liberarlo gradualmente (quitosano, liposomas, nanoarcillas LDH). | Las nanoarcillas LDH ("BioClay") protegen del lavado y la degradación por al menos 30 días. |
| **Pirimidina 2′-F** | Nucleótido modificado químicamente en la posición 2′ del azúcar, más resistente a nucleasas. | Con 32–55 % de incorporación aumentó la mortalidad 12–35 % en varios hemípteros. |
| **dsRNasa** | Nucleasa que degrada específicamente ARN de doble cadena. | *D. maidis* tiene tres, una muy expresada en intestino medio y glándulas salivales: es el cuello de botella declarado de la entrega oral. |

## El sistema patógeno

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **Floema** | Tejido vascular que transporta la savia elaborada. | Es donde se alimenta el vector y donde viven los cuatro patógenos. |
| **Fitófago de floema** | Insecto que se alimenta perforando el floema con su estilete. | Explica por qué el dsRNA pulverizado en superficie le llega mal: depende de captación vascular. |
| **Vector** | Organismo que transporta un patógeno de un hospedador a otro. | *D. maidis* es el único vector natural confirmado del complejo. |
| **Transmisión persistente propagativa** | El patógeno se multiplica dentro del insecto y éste queda infectivo de por vida. | Define la ventana de intervención y explica por qué matar tarde no sirve. |
| **Transmisión persistente circulativa** | El patógeno circula por el insecto pero **no** se multiplica en él. | Una fuente atribuye este modo al MSMV y otra lo da por desconocido: queda como incertidumbre. |
| **Período latente** | Tiempo entre la adquisición y el momento en que el insecto puede transmitir. | En *S. kunkelii* es de 18 a 22 días: es la ventana donde una intervención sobre el insecto todavía sirve. |
| **AAP / IAP** (*acquisition / inoculation access period*) | Tiempo de acceso del insecto a la planta fuente y a la planta test en un ensayo de transmisión. | Son los parámetros que definen la comparabilidad entre ensayos de transmisión. |
| **Transmisión transovárica** | Paso del patógeno de la madre a la descendencia por el huevo. | No ocurre en este sistema: cada individuo debe adquirir por su cuenta. |
| **Mollicute** | Bacteria sin pared celular, de genoma pequeño y bajo contenido GC. | *S. kunkelii* y el fitoplasma lo son, y es la razón central de que no respondan a RNAi. |
| **Espiroplasma** | Mollicute helicoidal y móvil; acá, *Spiroplasma kunkelii*, agente del achaparramiento pálido. | Es el patógeno que más castiga la producción de grano. |
| **Fitoplasma** | Mollicute no cultivable restringido al floema; acá, *'Candidatus* Phytoplasma asteris' 16SrI-B, agente del achaparramiento rojo. | Es el segundo mollicute del complejo. |
| **Marafivirus** | Género de virus de ARN de cadena simple de sentido positivo; acá, MRFV. | Es uno de los dos virus del complejo, y se multiplica dentro del insecto. |
| **Mastrevirus / Geminiviridae** | Género y familia de virus de ADN de cadena simple transmitidos por chicharritas; acá, MSMV (*Mastrevirus striatis*). | Es el único patógeno del complejo contra el cual la planta puede usar la vía RdDM. |
| **+ssRNA / ssDNA** | ARN de cadena simple de sentido positivo / ADN de cadena simple. | Son los tipos de genoma de MRFV y MSMV: determinan qué vía de defensa vegetal aplica. |
| **CSDC** (*corn stunt disease complex*) | El conjunto de los cuatro patógenos transmitidos por *D. maidis*. | Es el objeto del desafío: no es una enfermedad, son cuatro agentes con biologías distintas. |
| ***Stay-green*** / "planta zombi" | Planta que permanece verde sin llenar grano. | Es uno de los síntomas del cuadro combinado. |
| **Maíz guacho** | Plantas voluntarias de maíz que sobreviven entre campañas y sirven de "puente verde" al vector. | Eliminarlo es una de las pocas medidas culturales con lógica epidemiológica clara. |
| ***Safrinha*** | Segunda zafra brasileña de maíz, sembrada después de la soja. | Es el contexto de la mayoría de los datos de incidencia brasileños. |
| **Brocosomas** | Partículas proteicas que las chicharritas secretan y esparcen sobre su cutícula. | Son una barrera física que limita la eficacia de los hongos entomopatógenos. |
| **Antixenosis** | Resistencia por no preferencia: el insecto evita la planta. | Reduce el tiempo de contacto y con él la eficiencia de transmisión. |
| **Antibiosis** | Resistencia que afecta la biología del insecto que sí se alimenta. | Es el otro componente separable de la resistencia del híbrido. |
| **Incidencia / severidad** | Proporción de plantas con síntomas / intensidad del cuadro en las plantas afectadas. | A campo, el índice de severidad explicó el 72 % de la variabilidad del rendimiento; la acumulación del patógeno no lo explicó. |
| **Estadio V2 / R4** | Etapas fenológicas del maíz: dos hojas desarrolladas / grano pastoso. | El tratamiento de semilla fue efectivo sólo hasta V2; la incidencia se evaluó en R4. |
| **DAS-ELISA** | Inmunoensayo de doble sándwich para detectar un antígeno. | Es la técnica con la que se confirmó *S. kunkelii* en el ensayo argentino. |
| **CL50** | Concentración letal 50: la dosis que mata a la mitad de los individuos. | Es la unidad en la que se mide la resistencia a insecticidas. |
| **Razón de resistencia (RR)** | Cociente entre la CL50 de una cepa resistente y la de una susceptible. | 3.170 veces para bifentrina: la magnitud del problema que justifica buscar otro modo de acción. |

## Herramientas y conceptos de cómputo

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **BLAST** | Búsqueda heurística de similitud de secuencias por semilla y extensión. | **No calcula termodinámica**: pertenece al eje de especificidad, no al de eficacia. |
| **E-value** | Número esperado de alineamientos de igual o mejor puntaje por azar en una base de ese tamaño. | Es la salida estadística de BLAST, y no dice nada sobre si un siRNA va a funcionar. |
| **Bit score** | Puntaje de alineamiento normalizado, independiente del tamaño de la base. | Idem: mide parecido, no función. |
| **Bowtie** | Alineador de lecturas cortas con índice Burrows-Wheeler y backtracking consciente de la calidad. | Es el motor que usan si-Fi y dsRIP para buscar off-targets; tampoco calcula energía. |
| **MFE** (*minimum free energy*, mínima energía libre) | La energía libre de la estructura secundaria más estable de una secuencia de ARN. | Es la cantidad termodinámica central, y la calcula ViennaRNA, no BLAST. |
| **Accesibilidad** | Probabilidad de que un tramo del ARN esté de cadena simple y disponible para aparear. | Es predictiva en plantas (si-Fi) y **no** resultó significativa en el análisis en insectos de dsRIP. |
| **Asimetría termodinámica** | Diferencia de energía de apareamiento entre los dos extremos del dúplex de siRNA. | Determina qué hebra se carga como guía: es el término de eficacia mejor sostenido en insectos. |
| **Off-target** | Coincidencia no deseada entre el siRNA y un transcrito que no es el blanco. | Es la contracara de riesgo obligatoria: maíz, polinizadores, enemigos naturales, fauna del suelo. |
| **Mismatch** | Posición donde el siRNA y el transcrito no aparean. | Los minimizadores de off-target cuentan coincidencias permitiendo 1 o 2 mismatches. |
| **Ortólogo** | Gen de otra especie derivado del mismo gen ancestral. | Es como se transfieren blancos efectivos de una plaga modelo a la plaga objetivo. |
| **Transcriptoma** | Conjunto de todos los transcritos de un organismo o tejido. | Es el insumo mínimo para cualquier análisis de off-target; el de *D. maidis* tiene 56.116 transcriptos. |
| **si-Fi21 / si-Fi** | Diseñador de disparadores largos y predictor de off-targets. | Hace la enumeración de x-meros que el equipo creía que hacía BLAST, y usa Bowtie + RNAplfold. |
| **dsRIP** | Plataforma de diseño de dsRNA para manejo de plagas. | Es la herramienta con el tratamiento cuantitativo más explícito de eficacia y de riesgo no objetivo. |
| **pssRNAit / P-SAMS** | Diseñadores de ARN pequeños **para plantas**. | Importante: no sirven para diseñar contra un insecto; sus bases y reglas son vegetales. |

## Términos biológicos de apoyo que aparecen en el reporte

| Término | Definición en una línea | Por qué nos importa |
| --- | --- | --- |
| **Estilete** | Pieza bucal alargada con la que el hemíptero perfora el tejido y succiona savia. | Es la vía física por la cual el insecto adquiere e inocula los patógenos. |
| **Ninfa / estadio ninfal** | Cada una de las etapas juveniles por las que pasa el insecto antes de ser adulto; *D. maidis* tiene cinco. | Las ninfas ya transmiten, y el tercer estadio fue el más sensible al RNAi en un psílido emparentado. |
| **Ecdisis / muda** | Proceso de desprenderse del exoesqueleto viejo para crecer. | Es el proceso que fallan los insectos con *burs-α* o *eth* silenciados, y por eso mueren. |
| **Hemolinfa** | El "sangre" de los insectos: fluido circulatorio del hemocele. | Es por donde circula el patógeno entre el intestino y las glándulas salivales. |
| **Glándulas salivales** | Órganos que producen la saliva que el insecto inyecta al alimentarse. | Colonizarlas es el último paso antes de que el insecto pueda transmitir. |
| **Ovogénesis** | Formación de los oocitos en el ovario. | Es el proceso que afecta el silenciamiento de *Bicaudal C*, el primer blanco validado en *D. maidis*. |
| **Virulífero** | Insecto que porta el patógeno y puede transmitirlo. | Es la condición que se cuenta en los ensayos de transmisión. |
| **Epifitia** | Brote epidémico de una enfermedad en una población vegetal. | Es la palabra que corresponde al episodio argentino de 2023/24. |
| **Efector** | Proteína que un patógeno secreta en el hospedador para manipular su fisiología. | Es la vía por la cual los mollicutes alteran la planta y el vector, y un blanco alternativo al RNAi. |
| **Supresor viral del silenciamiento (RSS)** | Proteína codificada por un virus que bloquea la maquinaria de RNAi del hospedador. | Explica que la defensa antiviral vegetal exista y aun así el virus se establezca. |
| **Apoplasto** | El espacio extracelular de la planta, fuera de la membrana celular. | Las RNasas apoplásticas degradan el ARNdc pulverizado antes de que entre a la célula. |
| **Estoma** | Poro regulable de la epidermis foliar que controla el intercambio gaseoso. | Es la vía principal implicada en la captación foliar de ARNdc. |
| **RT-qPCR** | PCR cuantitativa sobre ADN copiado desde ARN; mide cuánto transcrito hay. | Es la técnica con la que se mide el *knockdown* en todos los trabajos citados. |
| ***In vitro* / *in vivo* / *ex vivo*** | En tubo / en el organismo vivo / en tejido extraído del organismo. | Distingue, por ejemplo, el corte de ARN por Argonautas procariotas (demostrado *in vitro*, rol *in vivo* desconocido). |
| **x-mero** | Subcadena de largo *x* extraída de una secuencia; para nosotros, cada ventana de 21 nt del disparador. | Es la unidad que enumeran los diseñadores de ARNdc por ventana deslizante. |
