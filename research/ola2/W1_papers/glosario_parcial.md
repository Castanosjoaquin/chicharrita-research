# Glosario parcial — términos nuevos que trae el corpus de papers

Sólo términos que **no** están ya en `00_meta/GLOSARIO.md`. Formato del
proyecto: término, definición en una línea, y por qué nos importa. Entre
paréntesis, el paper del corpus donde aparece.

Al final hay una sección de términos que conviene **no** confundir entre sí,
porque son los que más fácil se mezclan al hablar rápido.

---

## Entrega y formulación

| Término | Qué es | Por qué nos importa |
| --- | --- | --- |
| **Absorción por peciolo** (*petiole absorption*) | Cortar una hoja basal y poner el peciolo que sobresale en un tubo con la solución, para que la planta la absorba por el sistema vascular (P6) | Es la vía que entrega ARNdc al xilema de una planta entera, y el punto de partida del método de P6 antes de pasar a hoja cortada |
| **Absorción por hoja cortada** (*detached leaf absorption*) | Sumergir parcialmente una hoja separada de la planta en la solución de ARNdc y alimentar insectos sobre ella (P1, P6) | Es la vía que funcionó: sube la eficiencia de entrega de 40 % a cerca de 80 % al concentrar el ARNdc en menos tejido |
| **Inmersión de insectos** (*soaking*) | Sumergir ninfas directamente en la solución de ARNdc, con o sin coadyuvante (P6) | Es la vía que **falló** en un cicadélido pese a estar publicada como funcional en otros hemípteros: el resultado negativo más útil del corpus |
| **Lipofectamina** | Reactivo catiónico de transfección usado como coadyuvante para favorecer la internalización de ácidos nucleicos; en P6 al 13 % final | Es el coadyuvante concreto que no alcanzó para vencer la barrera cuticular del cicadélido |
| **Dieta artificial en sobre de parafilm** | Sacarosa al 15 % con colorante, encerrada entre dos capas de parafilm sobre un vial, de la que el insecto chupa a través de la membrana (P1) | Es el bioensayo estándar para tamizar muchos ARNdc en un hemíptero adulto; no sirve para ninfas porque la dieta ya las mata |
| **Hidróxido doble laminar (LDH, *layered double hydroxide*)** | Arcilla inorgánica laminar de carga positiva, fórmula general con M²⁺ y M³⁺, que adsorbe ácidos nucleicos; en P4, nanoláminas de 45 nm de diámetro Z | Es el portador de BioClay; su degradación por ácido carbónico atmosférico es lo que libera el ARNdc de a poco |
| **Razón de carga ARNdc:LDH** | Proporción en masa entre el ARNdc y la arcilla; la carga completa se alcanza a 1:4 y P4 usó 1:3 a propósito, para dejar algo de ARNdc libre y disponible de inmediato (P4) | Es un parámetro de formulación con una lógica explícita: liberación inmediata más liberación sostenida |
| **Pulverización a alta presión / inundación de estomas abaxiales** | Técnicas para forzar la entrada de ARN a través de la cutícula y la pared celular (P7, citando a Bennett et al. 2020) | Cuando un paper reporta "captación foliar", hay que mirar cómo forzó la entrada antes de generalizar a una pulverización de campo |
| **Vaina foliar abierta** | El cartucho de hojas jóvenes todavía enrollado de una plántula de maíz, con paredes flexibles y cutícula delgada; el sitio de aplicación de P7 | Es una variable de diseño que no teníamos: dónde se aplica cambia si entra o no |

## Células, tejidos y recorrido del ARN

| Término | Qué es | Por qué nos importa |
| --- | --- | --- |
| **Células de la vaina del haz** (*bundle sheath cells*) | Capa de células parenquimáticas que rodea el haz vascular; en maíz, plantas C4, es donde ocurre el ciclo de Calvin (P7) | Es el lugar exacto donde se detectó el siRNA exógeno dentro de la planta de maíz, y el que no es ni floema ni xilema |
| **Electropenetrografía (EPG)** | Registro eléctrico del recorrido del estilete de un insecto chupador, que permite distinguir si está sondeando floema, xilema o parénquima (P6) | Es la evidencia de que los fitófagos de floema **también** beben de xilema, que es el único mecanismo por el que la entrega mediada por planta puede funcionar |
| **Tráquea** (en corte vegetal) | Elemento conductor del xilema (P7) | En P7 el siRNA **no** apareció ahí, lo que acota por dónde se mueve |
| **Melaza / *honeydew*** | Excreción azucarada del insecto chupador; en P6 se tiñó de azul al alimentarse sobre hoja tratada | Es la prueba barata de que el insecto efectivamente ingirió lo que la planta absorbió |

## Blancos génicos que aparecen en el corpus

| Término | Qué es | Por qué nos importa |
| --- | --- | --- |
| **Bursicón (Burs-α / Burs-β)** | Neurohormona heterodimérica que endurece y melaniza la cutícula nueva y expande las alas tras la muda; Burs-α tiene 11 cisteínas conservadas (P3) | Es uno de los dos blancos con mejor fenotipo publicado en *D. maidis*: 10 % de supervivencia a día 4 |
| **Hormona desencadenante de la ecdisis (ETH)** | Neuropéptido producido por las células INKA de las glándulas epitraqueales que dispara la secuencia conductual de la ecdisis (P3) | El otro blanco de P3; su silenciamiento deja al insecto atrapado dentro de la exuvia vieja |
| **Células INKA / glándulas epitraqueales** | El grupo de células que secreta ETH (P3) | Ubica anatómicamente al blanco: no es intestino ni glándula salival |
| **Exuvia** | La cutícula vieja que el insecto desecha al mudar (P3) | El fenotipo de ds-*eth* se define como no poder desprenderse de ella |
| **Legumaína** | Cisteín-proteasa de tipo asparaginil endopeptidasa, expresada en intestino (P6); en *E. variegatus* se expresa 2.500 veces más en intestino que en glándulas salivales | Blanco de "primer órgano que toca el ARNdc ingerido": la lógica de elegir un gen por **dónde** se expresa y no sólo por qué hace |
| **Naterina (*natterin*)** | Proteína de intestino de insecto, originalmente descrita en veneno de pez, asociada a la interacción con patógenos (P6) | Ídem; y en la ola 1 figuraba como fuente `S30` sin enlace, con el rótulo "natterin-like y legumaína de intestino de insecto" |
| **ATP sintasa beta** | Subunidad catalítica de la ATP sintasa mitocondrial, de expresión sistémica, implicada en la transmisión del fitoplasma (P6) | Es el blanco que une "matar al vector" con "desarmar la transmisión", y el que P6 silenció en las dos especies por vía de planta |
| **Cathepsin D** | Proteinasa aspártica lisosomal del intestino medio posterior de hemípteros, implicada en la metamorfosis (P1) | Uno de los tres blancos de entrega oral en *D. citri* |
| **Quitina sintasa A / B** (*chitin synthase*) | Enzimas que sintetizan la quitina de tráquea, cutícula e intestino medio; la B produce la matriz peritrófica (P1) | Blanco clásico de RNAi en insectos; en P1 funcionó por vía oral |
| **Inhibidor de apoptosis (IAP)** | Proteína que bloquea la maquinaria apoptótica y participa en señalización, ubiquitinación y división celular (P1) | Fue el blanco **más letal** de los tres en *D. citri*: 64 % de mortalidad a 1000 ng/µL |
| **Fitoeno desaturasa (PDS)** | Enzima de la biosíntesis de carotenoides cuyo silenciamiento produce fotoblanqueo visible de la hoja (P2) | Es el gen reportero estándar de VIGS en plantas: no es un blanco de control, es un semáforo |
| **ZmlspH / lemon white1 (lw1)** | Gen de maíz necesario para el desarrollo del cloroplasto; silenciado da un fenotipo albino amarillo (P2) | El segundo reportero que P2 usa para mostrar que su vector sirve para más de un gen |
| **AGO18a** | Argonauta específica de monocotiledóneas, inducible por virus, que secuestra microARN del hospedador para liberar a AGO1 (P7) | En P7 es el gen de la vía de RNAi que más responde a la infección: 16 veces de inducción |
| **MOP1 (*mediator of paramutation 1*)** | Homólogo de RDR2 en maíz, necesario para la paramutación y el silenciamiento transcripcional (P7) | Conecta la vía de RNAi del maíz con el RdDM, que es el cuarto escalón de la escalera de precisión del organizador |

## Virología del MRFV y herramientas de silenciamiento

| Término | Qué es | Por qué nos importa |
| --- | --- | --- |
| **Silenciamiento inducido por virus (VIGS)** | Usar un vector viral recombinante que lleva un fragmento de un gen del hospedador para silenciar ese gen en la planta (P2) | Es lo que hace P2: silencia genes **del maíz**, no del virus. Es la confusión más probable al citar ese paper |
| **Inoculación por punción vascular (VPI)** | Inocular un virus pinchando el tejido vascular del embrión de la semilla con agujas finas y una herramienta de grabado (P2) | El MRFV **no** se transmite por frote de savia; sin VPI o sin el insecto no hay experimento |
| ***Marafibox*** | Promotor conservado de 16 nucleótidos de los marafivirus que dirige la síntesis del ARN subgenómico; equivalente al *tymobox* de los tymovirus (P2) | Es el elemento que controla la expresión de CP2, una de las dos cápsides |
| **CP1 y CP2 carboxi-coterminales** | Las dos proteínas de cápside del MRFV, que comparten el extremo carboxilo; CP1 se escinde de la poliproteína y CP2 se expresa desde el ARN subgenómico, en razón 1:3 en la partícula (P2) | Importa para interpretar el candidato `CP_MRFV` del EPILAB: "la cápside" del MRFV son dos productos distintos |
| **Unión HEL/POL** | La unión predicha de corte entre helicasa y polimerasa de la poliproteína del MRFV, nucleótidos 3709/3710 (P2) | Es el **único** sitio del genoma del MRFV que tolera una inserción; los otros tres probados son letales |
| **Peptidasa 2A del virus de la fiebre aftosa (FMDV 2A)** | Secuencia corta de 51 nt que provoca la separación cotraduccional de dos proteínas, usada para insertar una secuencia dentro de una poliproteína sin romper su procesamiento (P2) | Es el truco de ingeniería que hace viable la inserción: no duplica el sitio de corte nativo, lo sustituye |
| **Proteína P43** | ORF pequeño solapado del extremo 5' del MRFV, de función desconocida, **no** requerido para el movimiento sistémico ni para la transmisión por cicadélidos (P2) | Es el único ORF accesorio anotado del MRFV, y es parte de por qué el rótulo "Movement Protein" del candidato del EPILAB queda abierto |
| **Recuperación** (*recovery*) | Fenómeno por el cual una planta infectada va bajando el título viral a medida que crece y monta una defensa más fuerte (P2) | Explica por qué el fenotipo de VIGS se desvanece aunque el inserto siga intacto: el inductor es también el blanco |
| **Período de acceso a adquisición (AAP)** | El tiempo que el insecto pasa alimentándose sobre la fuente infectada para adquirir el patógeno; en P2, tres semanas para el MRFV (P2) | Es el parámetro que define cualquier bioensayo de transmisión, y el que hay que pedir si se propone uno |
| **Pasaje seriado** (*serial passage*) | Reinocular sucesivamente usando extracto de la planta anterior, para medir si una construcción pierde su inserto (P2) | Es cómo se mide la estabilidad genética de una herramienta de ARN viva; el ARNdc sintético no tiene este problema |

## Producción y detección

| Término | Qué es | Por qué nos importa |
| --- | --- | --- |
| ***Escherichia coli* HT115 (DE3)** | Cepa deficiente en RNasa III y con T7 ARN polimerasa inducible, que por eso acumula ARNdc en lugar de degradarlo (P4, P5) | Es **la** cepa de producción barata de ARNdc, y la que usan tanto P5 como P4 |
| **IPTG** | Análogo de lactosa que induce el promotor T7 en esa cepa (P5) | El disparador de la producción; `R1/REPORT.md` ya registraba que la lactosa a 6 g/L puede sustituirlo y multiplicar el rendimiento |
| **ARN en horquilla (hpRNA) y vector de repetición invertida** | Construcción donde el fragmento se clona en sentido y en antisentido separados por un intrón o espaciador, de modo que el transcrito se pliega sobre sí mismo formando ARNdc (P4, P5) | Es la forma concreta de producir ARNdc en una bacteria o en una planta; en P5 el tallo mide 147 y 140 pb y el lazo 199 pb |
| **Lisado crudo sonicado** | Extracto bacteriano roto por ultrasonido y centrifugado, aplicado sin purificar (P5) | Es la versión más barata posible del producto, y la que P5 demuestra que funciona |
| **Cy3 y ALEXA FLUOR 488** | Fluoróforos conjugados al ARN para seguirlo por microscopía (P4 y P7 respectivamente) | Es cómo se "ve" el ARN dentro del tejido; y en P4 los propios autores advierten que ver el fluoróforo no prueba que el ARNdc esté intacto |
| **Cuantificación absoluta por qPCR con sonda** | Asignar una concentración real a cada Ct contra una curva de calibración hecha con un fragmento sintético de referencia (P7) | Es la diferencia entre "bajó" y "bajó de X a Y": P7 reporta carga viral en attomol/µL, no en veces de cambio |
| **GeNorm y valor M** | Método para evaluar la estabilidad de un gen de referencia en RT-qPCR; en P1, M de 0,05 y 0,07 para actina | Es el control de calidad que decide si un porcentaje de knockdown significa algo |
| **Método de Pfaffl** | Cuantificación relativa de qPCR que corrige por la eficiencia real de cada par de cebadores, a diferencia del 2^-ΔΔCt que la asume en 2 (P7) | Dos papers del corpus usan métodos distintos: sus porcentajes no son estrictamente comparables entre sí |
| **Criterio de exclusión por rango intercuartílico (IQR)** | Descartar del análisis los individuos cuyo valor supera 1,5 o 3 veces el rango intercuartílico; en P6, los tratados con expresión por encima de la media y la mediana del control | Es la decisión metodológica que convierte el silenciamiento reportado en el del subconjunto que sí recibió el ARNdc, y hay que leerla antes de usar el número |

## Taxonomía y biología del insecto

| Término | Qué es | Por qué nos importa |
| --- | --- | --- |
| **Auchenorrhyncha** | Suborden de Hemiptera que agrupa a casi la mitad de las especies del orden, en su mayoría fitófagas y muchas vectoras (P3) | Es el grupo al que pertenecen *D. maidis* y *D. kuscheli*, y la unidad taxonómica dentro de la cual P3 argumenta conservación funcional |
| **Cicadomorpha / Fulgoromorpha** | Las dos infraórdenes de Auchenorrhyncha: la primera incluye a los cicadélidos como *D. maidis*, la segunda a los delfácidos como *D. kuscheli* (P3) | P3 encontró que el número de motivos de ETH en el precursor sigue esa división: tres en *D. maidis*, dos en *D. kuscheli* |
| **Hemimetábolo** | Insecto con metamorfosis incompleta, sin estadio de pupa, que pasa por estadios ninfales parecidos al adulto (P3) | Distingue a nuestra plaga de los modelos clásicos de RNAi (*Tribolium*, *Drosophila*), que son holometábolos |
| **Adulto teneral** | Adulto recién emergido, con la cutícula todavía blanda y poco pigmentada (P1) | Es el estadio que P1 usa para los bioensayos de dieta, y conviene saberlo para comparar dosis entre trabajos |
| **Motivo FFLKAXXSXPRI** | La secuencia conservada del precursor de ETH, que se escinde en sitios básicos GRR para liberar el péptido maduro (P3) | Es la firma que permite identificar el gen por homología sin tener el genoma anotado |
| **tBLASTn** | Búsqueda de una consulta de proteína contra una base de nucleótidos traducida en los seis marcos | Es la herramienta con la que P3 identificó sus blancos; y es, junto con BLASTn, **todo** el cómputo de diseño del corpus |

## Virus de maíz que aparecen y no son del complejo

| Término | Qué es | Por qué nos importa |
| --- | --- | --- |
| **SCMV (*Sugarcane mosaic virus*)** | Potyvirus que causa el mosaico enanizante del maíz, transmitido por pulgones (P5) | Es el virus del precedente de maíz del corpus; **no** es transmitido por *D. maidis* ni pertenece al complejo del achaparramiento |
| **MDMV (*Maize dwarf mosaic virus*)** | Otro potyvirus de maíz, con hasta 70 % de pérdidas reportadas en maíz dulce (P7) | Ídem. Atención: el SCMV se llamó históricamente MDMV-B, y P5 rotula su propia tabla 2 como "MDMV disease ratings" aunque el trabajo sea sobre SCMV |
| **Necrosis letal del maíz (MLN)** | Enfermedad que aparece cuando un potyvirus y un machlomovirus co-infectan la misma planta (P7) | Es el precedente de que una co-infección viral puede ser cualitativamente peor que la suma, algo a tener en cuenta en un complejo de cuatro agentes |
| **PMMoV y CMV** | *Pepper mild mottle virus* y *Cucumber mosaic virus*, los dos virus modelo de P4 | Ninguno infecta maíz: los números de BioClay vienen de tabaco, Xanthi, caupí y *Arabidopsis* |

---

## Pares que conviene no confundir

- **VIGS no es SIGS.** VIGS entrega la secuencia dentro de un virus que infecta
  la planta; SIGS la pulveriza sobre la planta. P2 es VIGS y los demás son SIGS o
  entrega directa. Decir "P2 demuestra silenciamiento del MRFV" es invertir el
  paper.
- **Silenciar al MRFV no es usar al MRFV para silenciar.** Es la misma confusión
  dicha de otro modo, y es la más probable de todas.
- **Xilema no es floema.** Todo el corpus entrega al xilema y al apoplasto.
  *D. maidis* se alimenta de floema. El puente entre las dos cosas es el sondeo
  de xilema documentado por electropenetrografía, no el transporte floemático.
- **Knockdown no es mortalidad.** P6 tiene knockdown sin mortalidad; P1 tiene
  mortalidad que escala con la dosis mientras el knockdown no. Son dos
  desenlaces distintos y el corpus documenta las dos disociaciones.
- **Detectar el fluoróforo no es detectar el ARN.** Lo declaran los propios
  autores de P4.
- **Detectar siRNA no es demostrar protección, y no detectarlos no es demostrar
  que no la hay.** La primera mitad ya estaba en la ola 1; la segunda la agrega
  P4.
- **CP1 del MRFV no es CP1 del SCMV.** En P2, CP1 y CP2 son las dos cápsides del
  MRFV; en P5, CP1 y CP2 son dos *regiones* del único gen de cápside del SCMV.
  La coincidencia de nombres entre dos papers del mismo corpus es desafortunada
  y ya provocó una confusión en la primera lectura.
