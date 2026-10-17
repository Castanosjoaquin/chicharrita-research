# Contradicciones y matices: el corpus contra nuestros reportes de la ola 1

Cada punto trae cuatro cosas: qué decíamos, qué dice el corpus, de qué archivo y
sección sale, y qué tan fuerte es la evidencia. La regla del proyecto se aplica
tal cual: **el corpus no gana automáticamente por ser oficial**, y donde la
discrepancia no se resuelve queda marcada `[?]`.

Están ordenados por cuánto cambian una decisión nuestra.

---

## 1. BioClay y las nucleasas: medio corregido, medio confirmado

**Qué decíamos.** `R3/panorama_industria.md`, sección "Portadores y protección
frente a nucleasas y UV": *"ninguna fuente que se haya podido abrir atribuye a
BioClay protección medida frente a fotodegradación por UV ni frente a nucleasas.
Las fuentes atribuyen la ventana extendida a liberación sostenida y resistencia
al lavado. Si la afirmación «BioClay protege del UV y de las nucleasas» circula
—y circula— está sin respaldo en lo verificable"* `[?]`. La fila de la tabla
marcaba explícitamente "paper no abierto".

**Qué dice el corpus.** El paper primario está abierto y la afirmación se parte
en dos.

- **Nucleasas: sí lo mide, y la advertencia nuestra era incorrecta.** Hay un
  experimento dedicado, con cuatro réplicas: ARNdc control y ARNdc-LDH expuestos
  a RNasa A, con el ARNdc liberado del LDH por disolución ácida antes de correr
  el gel. Resultado: *"el tratamiento con RNasa degradó el ARNdc desnudo en
  mayor medida que el ARNdc-LDH"* (`nplants2016207 (1).pdf`, sección "Stability
  of dsRNA loaded into LDH" y figura 3e; método en "Stability of dsRNA bound to
  LDH"). Los autores concluyen que las nanoláminas *"pueden proteger ARNdc
  grandes de las nucleasas"*.
- **UV: no lo mide, y la advertencia nuestra era correcta.** La palabra
  "sunlight" aparece una sola vez en todo el artículo, en la frase que enuncia
  el desiderátum —que el ARNdc debe *"resistir condiciones de campo, como lluvia,
  luz solar y nucleasas"*—, y no hay ningún experimento de UV ni de
  fotodegradación. Los tres ensayos de estabilidad son RNasa A, lavado por
  pipeteo vigoroso, y persistencia en hoja a 30 días bajo condiciones de
  invernáculo.

**Fuerza de la evidencia.** Alta en las dos direcciones: experimento directo con
réplicas declaradas para las nucleasas, y ausencia verificada por lectura
completa para el UV.

**Consecuencia.** La fila de BioClay en `R3/panorama_industria.md` hay que
corregirla: protección frente a nucleasas pasa de `[?]` a `[E]`; protección
frente a UV sigue sin respaldo y conviene seguir no repitiéndola. De paso, el
mismo archivo confirma lo que R3 daba como `[R]`: Nufarm Australia Ltd. figura
en los agradecimientos como socio industrial `[E]`.

---

## 2. El número del SCMV en maíz estaba mal por seis órdenes de magnitud, y "total" no era total

**Qué decíamos.** `R3/REPORT.md`, sección 3.2, citando de segunda mano la
revisión de Vatanparast et al.: *"contra el virus del mosaico de la caña de
azúcar en maíz, dsRNA de origen bacteriano a 3 µg/L logró inhibición total a 30
días post-inoculación. Es el precedente de que el maíz absorbe y moviliza dsRNA
aplicado exógenamente de modo útil contra un virus"* `[R]`.

**Qué dice el corpus.** Tres correcciones sobre el mismo enunciado.

- **La unidad.** La preparación era de *"3 µg de ácido nucleico total por µL"*,
  no por litro (`s00299-010-0911-z.pdf`, "Crude bacterial preparations to
  inhibit SCMV infection"). Son seis órdenes de magnitud de diferencia, y es la
  clase de cifra que, mal citada, vuelve la tecnología mil veces más barata de
  lo que es en una diapositiva.
- **La dosis aplicada.** No se aplicaron 3 µg/µL: se aplicó **1 mL de una
  dilución al medio por planta** en los ensayos de protección, y la serie de
  diluciones mostró que a 1/20 la protección desaparece, con 68,3 % de
  incidencia de enfermedad.
- **"Inhibición total" no es lo que reporta la tabla.** Los lisados con ARNdc
  dieron 16/20 y 14/20 plantas resistentes para CP1 y CP2 respectivamente, es
  decir **4/20 y 6/20 plantas susceptibles** (`s00299-010-0911-z.pdf`, tabla 3).
  Es una protección del 80 % y del 70 % de plantas, no una inhibición total.

**Y una observación nuestra que obliga a usar esas tablas con pinzas.** En las
tablas 2 y 3 del mismo paper, la fila *"Non-inoculated controls"* figura con
fenotipo **S 18/20**, es decir dieciocho de veinte plantas **no inoculadas**
registradas como susceptibles, con títulos de ELISA comparables a los de los
controles inoculados. Tal como está impreso, es internamente incoherente: o la
fila está mal rotulada, o hubo infección cruzada, o los controles no eran tales.
No lo resolvemos `[?]`, pero mientras no se resuelva **los porcentajes de
protección de ese paper no son utilizables como línea de base cuantitativa**, y
sólo vale su resultado cualitativo: el lisado con ARNdc protege y el lisado
vacío no.

**Fuerza de la evidencia.** Alta para las tres correcciones: están en el texto y
en las tablas del artículo original. Media para la incoherencia de los
controles, que es lectura nuestra de una tabla, no una declaración de los
autores.

---

## 3. Mortalidad y knockdown se desacoplan, y el ARNdc control también mata

**Qué decíamos.** `R1/REPORT.md` sección 2.5 recogía, de *Bactericera
cockerelli*, que *"más dsRNA no siempre es más silenciamiento"*, con la
concentración más efectiva en torno a **100 ng/µL** y saturación del RISC como
explicación propuesta `[R]` `S26`. Y el punto 8 de las implicancias advertía que
"el título del patógeno no predice el daño".

**Qué dice el corpus.** P1 mide dosis y knockdown a la vez en un hemíptero de
floema, con tres concentraciones, y el resultado va más lejos que nuestra
versión.

- La **mortalidad sí escala con la dosis**, hasta 64 % a 1000 ng/µL para
  *inhibitor of apoptosis* a las 120 h (`Dcitri.pdf`, Resultados, figura 1D).
  No hay meseta a 100 ng/µL: la dosis más baja ensayada fue 200 ng/µL y la
  mortalidad siguió subiendo hasta 1000.
- El **knockdown no escala con la dosis**: *"no hubo correlación entre las dosis
  altas de ARNdc y las reducciones en los niveles de expresión del ARNm"*
  (`Dcitri.pdf`, Discusión). Para *cathepsin D* y *chitin synthase* la expresión
  residual reportada **aumenta** al subir la dosis.
- El **control de ARNdc-GFP a 500 y 1000 ng/µL causó mortalidad
  significativamente mayor que el control de sacarosa al 15 %** (`Dcitri.pdf`,
  Resultados, figuras 1B y 1C). Una parte de la mortalidad a dosis alta no es
  específica de secuencia.

**Fuerza de la evidencia.** Alta: experimento con tres dosis, control de
secuencia no relacionada a cada dosis, y n declarado (30 individuos por réplica,
tres réplicas).

**Consecuencia, y es la más importante de este archivo.** No es una contradicción
de R1 sino una generalización que lo endurece: **la mortalidad no es un
sustituto del knockdown ni al revés**, y cualquier función de puntuación nuestra
que use una como proxy de la otra —o que valide contra datos de mortalidad un
modelo calibrado sobre knockdown— está asumiendo una relación que el único
experimento del corpus que la mide no encuentra. Afecta directamente al diseño
de V1 y V3 en `R2/PROPUESTA.md`, donde el desenlace medido de Cedden et al. es
hazard ratio de supervivencia y el de los trabajos en *D. maidis* es reducción
de transcripto: **no son la misma variable y no deberían entrar al mismo
Spearman sin declararlo.**

Y agrega una recomendación de diseño experimental que vale la pena llevar al
evento: el control correcto no es "sin ARNdc" sino **ARNdc no relacionado a la
misma concentración, corrido a cada dosis**. Los tres papers de insecto del
corpus lo hacen y es la única razón por la que el efecto inespecífico se ve.

---

## 4. Los números de ETH y Burs-α: correctos, con una atribución cruzada entre especies

**Qué decíamos.** `R1/REPORT.md` sección 4.6, fuente `S15`: *"por microinyección
en ninfas de quinto estadio recién mudadas —n = 40 por tratamiento, 0,25 µL por
ninfa a 500 ng/µL, es decir 125 ng por insecto, con dsRNA de β-lactamasa como
control negativo— logró knockdown de ~95 % para burs-α y ~90 % para eth por
RT-qPCR, con ecdisis incompleta, deformidad de alas y supervivencia a día 4 de
~10 % y ~15 % respectivamente, contra ~100 % del control"*.

**Qué dice el corpus.** El método y los porcentajes de knockdown son exactos:
n=40 por tratamiento, 0,25 µL a 500 ng/µL, control de b-lactamasa amplificada de
pRSET B, ~95 % para *burs-a* y ~90 % para *eth* en *D. maidis*
(`finsc-6-1811933.pdf`, "RNAi experiments" y "Expression levels after RNAi
administration"). **La supervivencia está mezclada entre especies.** Los valores
reales son:

| | *D. maidis* | *D. kuscheli* |
| --- | --- | --- |
| ds-*burs-a* | **10 %** a día 4 | 17,5 % a día 4 |
| ds-*eth* | **10 %** a día 5 | 20 % a día 5 |

El "~15 %" de nuestro reporte no corresponde a *eth* en *D. maidis* sino,
aproximadamente, a *burs-a* en *D. kuscheli*. En la especie blanco los dos genes
dejaron 10 % de supervivientes. El control fue *">95 %"*, no ~100 %.

**Dos precisiones que no teníamos.** Los ARNdc miden **578 pb** (*burs-a*) y
**544 pb** (*eth*) (`finsc-6-1811933.pdf`, tabla 1), por encima de la banda de
200-500 pb que `R1/REPORT.md` sección 6.1 recoge como típica de los ARNdc
pesticidas. Y el knockdown descansa sobre **tres réplicas biológicas de tres
ninfas cada una**, no sobre las 40 ("RT-qPCR analyses"): las 40 son el n de
supervivencia.

**Fuerza de la evidencia.** Alta, lectura directa del artículo.

**Consecuencia.** Corregir la atribución en `R1/REPORT.md` y, sobre todo, dejar
de tratar el "~95 %" como un punto de calibración: con n=3 réplicas biológicas
es una demostración de que el gen es esencial, no una medida de eficacia
comparable.

---

## 5. El largo del disparador no tiene una banda única: depende de quién lo procesa

**Qué decíamos.** `R1/REPORT.md` sección 6.1: mínimo de ~60 pb para captación
celular eficiente, *"la mayoría de los estudios usa 140 a 500 nt"*, los ARNdc
pesticidas *"típicamente de 200 a 500 pb"*, recomendación general de 200 a 1000
pb, y ledprona de 490 pb. Y `R2/REPORT.md` sección 3.1 fija el candidato como
"una secuencia de 200 a 500 pb".

**Qué dice el corpus.** En el insecto la banda se queda corta por arriba y en la
planta se queda corta por abajo.

- *D. maidis*, por inyección: **578 pb** y **544 pb**, ambos efectivos
  (`finsc-6-1811933.pdf`, tabla 1).
- Maíz, horquilla producida en bacteria: tallos de **147 pb** y **140 pb**,
  efectivos contra el SCMV (`s00299-010-0911-z.pdf`, "PCR conditions and plasmid
  constructs" y "Construction of inverted-repeat expression vectors").
- Maíz, inserto en vector viral: **120 nt** silenció **mejor** que **231 nt**, y
  los autores lo dicen explícitamente —el inserto mayor *"no tuvo ganancias
  fenotípicas de silenciamiento"* frente al menor— (`PLD3-4-e00224.pdf`,
  sección 4).
- Maíz dulce, siRNA sintético: **21 nt**, suficiente para cebar la vía y bajar
  la carga viral (`s12298-024-01500-2.pdf`, "Plant material, growth conditions
  and treatments").

**Fuerza de la evidencia.** Alta para cada dato individual; la generalización
—"el óptimo depende del organismo que procesa"— es inferencia nuestra sobre
cuatro observaciones del corpus `[H]`, coherente con el principio de
`R1/REPORT.md` sección 2.1 de que el largo del siRNA lo elige la enzima del
organismo y no quien diseña.

**Consecuencia.** La restricción "200 a 500 pb" de `R2/REPORT.md` es defendible
para un candidato dirigido al **insecto** y no lo es para uno dirigido a la
**planta**. Como dos de los cuatro candidatos del EPILAB apuntan al MRFV vía
planta, el método tiene que tratar el largo como un parámetro condicionado al
organismo blanco, no como una constante.

---

## 6. Detectar siRNA no prueba protección, y ahora tampoco lo contrario

**Qué decíamos.** `R1/REPORT.md` sección 4.5 y punto 8 de las implicancias: las
plantas susceptibles infectadas *"generan siRNA derivados del virus en
abundancia y aun así permiten replicación, movimiento y síntomas"*, de donde
"detectar siRNA no es demostrar protección" `[E]` `S43`.

**Qué dice el corpus.** Lo confirma y agrega la implicación recíproca, que es
más rara y más incómoda. En P4, con protección antiviral sostenida demostrada a
20 días, los autores reportan que ni por northern blot ni por
secuenciación de ARN pequeños pudieron detectar, *"por encima del ruido de
fondo"*, siRNA de 21 a 24 nt de CMV2b derivados del ARNdc aplicado, **pese a sí
detectar los ARN grandes específicos de CMV2b en hojas pulverizadas y
sistémicas** (`nplants2016207
(1).pdf`, sección "Stability of dsRNA loaded into LDH", párrafo final). Y en las
plantas tratadas y luego desafiadas, los siRNA derivados del **virus** bajaron
al menos un orden de magnitud respecto del control, precisamente porque hubo
menos virus que procesar (figura 6).

**Fuerza de la evidencia.** Alta para el dato; su interpretación mecanística es
incierta `[?]`. El propio paper no explica por qué hay protección sin siRNA
detectables del disparador, y deja el mecanismo del transporte sistémico como
"foco de investigación futura".

**Consecuencia.** Si alguna vez proponemos un ensayo de validación barato
basado en "medir si aparecen siRNA del disparador", el corpus dice que puede
dar negativo en un sistema que **sí** está protegido. Ni la presencia ni la
ausencia de siRNA es un buen desenlace. El desenlace tiene que ser carga del
patógeno, síntoma o rendimiento, que es justo lo que `R5/RUBRICA.md` ya exige en
el criterio C1 y lo que hay que preguntarle al investigador (pregunta 3 de
`00_meta/PREGUNTAS_ABIERTAS.md`).

---

## 7. Hay un tercer transcriptoma de *D. maidis*, y es el que usa el grupo que publica

**Qué decíamos.** `R2/REPORT.md` sección 4: *"el transcriptoma de Xu et al. 2021,
con 56.116 transcriptos, está publicado pero no se encontró depositado"* `[?]`;
y la integración del 2026-10-17 en `00_meta/PREGUNTAS_ABIERTAS.md` lo dio por
cerrado: *"está depositado: 56.116 transcriptos en el TSA GITV00000000, con
82,4 % de completitud BUSCO"*. La pregunta 9 de la lista consolidada pregunta al
investigador cuál de los dos considera válido el laboratorio.

**Qué dice el corpus.** P3 no usa ninguno de los dos. Identificó *eth* y
*burs-a* en *"conjuntos de datos transcriptómicos ensamblados en nuestro
laboratorio"*, y la referencia que respalda el de *D. maidis* es la número 32:
una **tesis de maestría de la UNNOBA de 2018** (Palacio V., *Secuenciación del
transcriptoma de Dalbulus maidis*), alojada en el repositorio institucional
(`finsc-6-1811933.pdf`, "In silico identification of eth and burs-a" y lista de
referencias). El de *D. kuscheli* figura como **no publicado**.

**Fuerza de la evidencia.** Alta: es la declaración de métodos de los autores.

**Consecuencia.** La pregunta 9 al investigador hay que reformularla. No es
"¿el TSA o el de Xu?": es **"¿cuál de los tres, y nos pasan el ensamblado que
usan?"**. Y el tamizaje de off-target de P3 se hizo contra ese ensamblado
propio, lo que significa que su garantía de especificidad intraespecífica está
acotada a la cobertura de un transcriptoma que no es público. Es un buen pedido
concreto para el día del evento, y es barato de conceder.

---

## 8. Un método de entrega que funciona en un hemíptero puede fallar en otro

**Qué decíamos.** Nada explícito en contra, pero `R3/panorama_industria.md`
presenta la tabla de portadores como un menú de opciones con ventanas de
protección comparables, y advierte con razón que los números *"no son
comparables entre sí"* por venir de especies y laboratorios distintos. La
advertencia era sobre la comparabilidad de las magnitudes.

**Qué dice el corpus.** Es más fuerte que eso: no es sólo que las magnitudes no
se comparen, es que **el método puede no transferirse en absoluto**. La
inmersión de ninfas en solución de ARNdc con lipofectamina al 13 % no indujo
silenciamiento en *Euscelidius variegatus* —expresión de 0,561 ± 0,036 (n=48) en
el grupo tratado contra 0,414 ± 0,025 (n=21) en el control de dsGFP, es decir
**por encima** del control— y los autores la descartaron
(`s10340-023-01670-0.pdf`, tabla 1 y "Insect soaking"). La misma técnica está
publicada como funcional en *Diaphorina citri* y en *Aedes aegypti*, según las
referencias que ellos mismos citan, y los autores declaran no poder determinar
si falló la entrega o si el ARNdc se degradó.

**Fuerza de la evidencia.** Alta: resultado negativo medido, con n grande para
este tipo de ensayo (48 contra 21) y publicado con su tabla.

**Consecuencia.** Es el argumento más limpio que tenemos para el eje de riesgo
de la propuesta: cuando el método de entrega se transfiere entre especies de
hemípteros, la evidencia del corpus es que **falló una vez de las que lo
intentaron**, y esa vez fue en un cicadélido. Cualquier propuesta nuestra que
apoye su vía de entrega en un precedente de otra especie tiene que declarar esto
como el riesgo dominante, exactamente igual que `R2/REPORT.md` declara la
transferencia de Coleoptera a Hemiptera como la incertidumbre dominante del lado
del modelo.

---

## Lo que el corpus confirma sin matices

Para que la lista de arriba no se lea como que la ola 1 estaba mal. Estas cosas
quedaron confirmadas por fuente primaria:

- **La ventana de protección del ARNdc desnudo se mide en días.**
  `R1/REPORT.md` decía "típicamente dura sólo unos pocos días" `[E]` `S43`. P4
  la cifra en **5 a 7 días** citando sus dos referencias primarias, y P5 la mide:
  buena protección si se inocula hasta 5 días después de pulverizar, 43,3 % de
  plantas con síntomas si se inocula a los 7.
- **La lluvia anula el tratamiento, y más rotundamente de lo que decíamos.**
  `R1/REPORT.md` recogía que lluvias de más de 20 mm remueven "una proporción
  significativa" `[R]` `S43`. P5 reporta que, tras pulverizar la preparación de ARNdc
  y la lluvia subsiguiente, *"todas las plantas mostraron síntomas
  sistémicos"* (`s00299-010-0911-z.pdf`, Discusión).
- **El cuello de botella es la entrega a chupadores de savia, y es consenso.**
  P6 abre y cierra con eso, y lo llama *"un desafío mayor para la aplicación del
  RNAi en protección de cultivos"* (`s10340-023-01670-0.pdf`, Abstract e
  Introducción). Confirma la declaración del organizador y el diagnóstico de
  `R3/REPORT.md` sección 3.2.
- **No hay RdRP en insectos.** P6 lo enuncia con cuatro referencias
  (`s10340-023-01670-0.pdf`, Introducción), igual que `R1/REPORT.md` sección 2.4.
- **El maíz genera siRNA de 21 nt como clase dominante.** P2 lo observa en los
  tres fondos genéticos que probó: *"predominantemente siRNA de 21 nt"*
  (`PLD3-4-e00224.pdf`, secciones 3.3 y 3.8), coherente con lo que
  `R1/REPORT.md` sección 2.4 atribuye a DCL4.
- **La co-entrega contra dsRNasas sigue en pie como estrategia propuesta.** P3
  la recomienda citando al mismo grupo (`finsc-6-1811933.pdf`, Discusión), que
  es lo que `R3/REPORT.md` sección 5 ya había registrado.
- **Ninguna revisión ni paper propone silenciar al mollicute.** Ver
  `REPORT.md` sección 3.1.
