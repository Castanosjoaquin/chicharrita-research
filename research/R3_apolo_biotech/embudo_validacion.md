# Embudo de validación: de candidato a tratamiento probado

**Qué es este documento.** La reconstrucción, etapa por etapa, del camino que
recorre una secuencia de ARN desde que es una idea hasta que es un producto
registrado, con la **entrada** y la **salida** de cada etapa explicitadas. Está
reconstruido para APOLO Biotech y para el EPILAB, cruzando lo que dicen sus
fuentes con lo que exige la norma argentina y con lo que describe la literatura.

**Por qué importa tanto la precisión acá.** Porque si no sabemos qué consume
cada etapa como entrada, cualquier herramienta computacional que el equipo
proponga cae al vacío. El objetivo de este archivo no es describir el embudo en
abstracto: es ubicar **el punto exacto de inserción** de un aporte nuestro.

**Cómo leer los marcadores.** Cada etapa lleva un bloque de procedencia:

- `DOCUMENTADO` — hay fuente abierta que lo dice. Se nombra la fuente.
- `NORMATIVO` — lo exige la Resolución SENASA 1004/2023, texto leído.
- `INFERENCIA NUESTRA [H]` — reconstrucción del equipo. No está publicado.

---

## Vista general

```
Etapa 0   Definir el sistema y el agente a intervenir
Etapa 1   Recursos genómicos y transcriptómicos          ← cuello de botella de datos
Etapa 2   Selección del gen blanco
Etapa 3   Diseño de la secuencia y tamizaje de especificidad in silico
   ▸▸▸  AQUÍ ENTRA LA PREGUNTA DEL ORGANIZADOR: ¿cuáles merecen validación?  ◂◂◂
Etapa 4   Producción del ARN para ensayo
Etapa 5   Tamizaje in vitro / ex vivo
Etapa 6   Bioensayo sobre el organismo blanco
Etapa 7   Formulación y vía de entrega                    ← cuello de botella declarado
Etapa 8   Ensayo de invernáculo sobre planta
Etapa 9   Ensayo a campo
Etapa 10  Organismos no objetivo y toxicología
Etapa 11  Trámite regulatorio
Etapa 12  Escalado productivo y costo por hectárea
```

Las etapas 1 a 3 son el **tramo seco**, el único donde un equipo sin
laboratorio puede trabajar con las manos. Todo lo demás necesita banco, cámara
de cría, invernáculo, parcela y plata.

---

## Etapa 0 — Definir el sistema y el agente a intervenir

**Entrada:** el problema agronómico. En nuestro caso, el complejo de
achaparramiento del maíz y su vector.

**Salida:** la decisión de contra qué organismo se dirige el ARN.

`DOCUMENTADO` — El material del organizador nombra cuatro patógenos (MRFV,
MSMV, un fitoplasma y *Spiroplasma kunkelii*), el vector *Dalbulus maidis* con
sus tres funciones relevantes —alimentación, supervivencia y transmisión— y el
maíz como cultivo a proteger, y remarca que son "agentes con biologías
diferentes".

**La restricción que define toda la rama.** El RNAi es una vía eucariota: las
bacterias no tienen maquinaria de interferencia de ARN `[E]`. El fitoplasma y
*S. kunkelii* son molicutes, bacterias sin pared celular. Eso deja tres rutas
plausibles para una estrategia de ARN exógeno —silenciar al **vector**,
silenciar los **virus** del complejo, o **modular la defensa de la planta**— y
deja fuera la ruta directa contra los molicutes. El esquema oficial del
organizador cierra en "inhibición del crecimiento del patógeno", lo que merece
la pregunta directa y figura en `preguntas_abiertas.md`.

**Consecuencia para el embudo:** la rama del vector y la rama del virus tienen
embudos **distintos**. Un dsRNA contra *D. maidis* tiene que atravesar el
intestino de un insecto; uno contra MRFV actúa dentro de la planta. Las
barreras de entrega no son las mismas y los bioensayos tampoco.

---

## Etapa 1 — Recursos genómicos y transcriptómicos

**Entrada:** genoma y transcriptoma del organismo blanco; genomas de los
organismos que hay que preservar.

**Salida:** un conjunto de secuencias anotadas sobre el cual buscar blancos.

`DOCUMENTADO` — Apolo Rocket "almacenará y recuperará datos genómicos de bases
públicas y de origen propio, obtenidos mediante secuenciación masiva de ácidos
nucleicos (NGS)", según la descripción del proyecto de la Fundación Sadosky, y
procesa información genómica proveniente de secuenciaciones masivas según La
Nación. Es decir: la empresa **genera secuenciación propia** además de usar
bases públicas.

`DOCUMENTADO` — Para *D. maidis* existe genoma: el CIAP del INTA lo secuenció,
ensambló y anotó a partir de 20 ejemplares de una colonia sana de invernáculo.
Pero está publicado como **"versión actualizable v0.1", proyecto en curso**, y
fue descrito por uno de sus autores como "un primer borrador".

`DOCUMENTADO` — Para el gen de ovogénesis, el grupo de Catalano identificó el
candidato **a partir del transcriptoma de todos los estadios** del insecto.
Esto es un dato metodológico valioso: el transcriptoma por estadio es la
entrada real de la etapa 2, no el genoma solo.

**El cuello de botella de esta etapa es de datos y es nuestro.** Un genoma
borrador v0.1 pone un techo a todo lo que venga después: si la anotación está
incompleta, **los off-targets no se pueden descartar con confianza**. Nadie
puede prometer especificidad por encima de la calidad de su referencia.
Pendiente de alta prioridad: verificar disponibilidad, completitud de la
anotación y licencia del genoma del INTA. No lo pudimos abrir.

---

## Etapa 2 — Selección del gen blanco

**Entrada:** el conjunto anotado de la etapa 1.

**Salida:** una lista de genes candidatos.

`DOCUMENTADO` — El criterio general es **gen esencial**: la revisión del propio
equipo y el material del organizador coinciden en que el dsRNA se diseña contra
genes esenciales del objetivo. La web de la empresa lo dice para hongos y
virus; la diapositiva del organizador lo dice para el circuito del desafío.

`DOCUMENTADO` — "La eficacia de SIGS depende de la eficiencia de captación de
ARN por el patógeno y **de los genes blanco elegidos**" (Attallah et al., 2025).
La elección del gen es, según ellos mismos, un determinante de primer orden.

`DOCUMENTADO` — Los blancos ya probados en *D. maidis* por el grupo de Catalano
dan el precedente de qué clases de gen funcionan en esta especie: un gen de
**ovogénesis** (efecto reproductivo, no letal) y las **dsRNasas** del propio
insecto (blanco habilitante, no de control). Son dos lógicas distintas de
blanco y conviene no confundirlas.

`INFERENCIA NUESTRA [H]` — Los criterios concretos de ranking de genes
—esencialidad, nivel y tejido de expresión, conservación intraespecífica,
divergencia respecto de especies a preservar— no están publicados por APOLO ni
por el EPILAB para ningún blanco. Sabemos que los usan; no sabemos con qué
pesos ni en qué orden.

---

## Etapa 3 — Diseño de la secuencia y tamizaje de especificidad in silico

**Entrada:** los genes candidatos de la etapa 2.

**Salida:** secuencias de ARN concretas, con su evaluación de especificidad.

`DOCUMENTADO` — Es la etapa donde vive **Apolo Rocket**: corre en la nube, no
exige conocimientos avanzados de bioinformática, **evalúa más de 140 organismos
a la vez** —"antes se analizaban manualmente unos pocos"—, registra cada
consulta en una base de datos y **emite reportes automáticos** para orientar el
diseño. El CTO lo justifica así: "reduce significativamente el riesgo de efectos
no deseados". La empresa declara además que verifica patrones de secuencia para
que las moléculas no impacten en humanos ni en abejas.

`DOCUMENTADO` — "**Bioinformatic analyses play an essential role in the
development of dsRNA-based pesticides**", principalmente para asegurar
especificidad y limitar off-targets (Attallah et al., 2025). Y, de la misma
fuente, la contracara: "los potenciales off-targets requieren consideración
cuidadosa y **pruebas de toxicidad adicionales en laboratorio**".

`DOCUMENTADO` — El límite del método, según literatura independiente: las
herramientas pueden marcar secuencias con homología parcial a genes no blanco,
pero **los vacíos de conocimiento limitan su exactitud**; la tolerancia a
desapareamientos (mismatches) y la posición del desapareamiento agregan
complejidad; y **la bioinformática no reemplaza al ensayo empírico en organismos
diversos** (Vatanparast et al., 2024).

`DOCUMENTADO` — El eje de diseño del organizador agrega una dimensión que no es
de especificidad sino de **plataforma**: dsRNA largo canónico → dsRNA
ingenierizado → plataformas de ARN pequeño de precisión (miRNA artificial,
syn-tasiRNA, dúplex maduro listo para AGO) → siRNA de 24 nt por RdDM. Moverse
hacia la derecha de esa tabla es una forma legítima de aportar, con un dato de
viabilidad que conviene tener a mano: la aplicación exógena de **precursores de
miRNA parece menos viable** porque el procesamiento depende de la estructura
secundaria (Attallah et al., 2025), lo que empuja hacia **dúplex maduros** y
lejos de precursores.

`INFERENCIA NUESTRA [H]` — El criterio de corte no está publicado: cuántos
nucleótidos contiguos de coincidencia con un organismo no objetivo descalifican
un candidato, cómo se pondera una coincidencia en un polinizador frente a una
en un artrópodo benéfico, y cómo se agregan los reportes de 140 organismos en
una sola decisión. Esto es **exactamente el hueco** de la sección 6.2(a) del
reporte.

### ▸▸▸ El punto de inserción ◂◂◂

Acá termina el tramo que se puede hacer sin laboratorio, y acá está la pregunta
textual del organizador: tiene **candidatos preliminares diseñados por el equipo
del EPILAB** y pregunta **cuáles merecen validación y por qué**.

Eso significa que el aporte **no es generar candidatos** —ya los tienen, y ya
tienen con qué generarlos— **sino ordenar un conjunto existente con un criterio
explicitable y auditable**. La entrada de la etapa 4 es, por lo tanto, lo que
hay que producir:

| Lo que la etapa siguiente necesita recibir | Estado |
| --- | --- |
| Una lista **ordenada** de secuencias candidatas | es la salida que hay que producir |
| El criterio de orden, **escrito y con sus pesos** | no publicado por nadie `[H]` |
| La evidencia que respalda cada posición | construible desde literatura |
| El riesgo de off-target por candidato, con su umbral declarado | construible, con el techo de la etapa 1 |
| La **incertidumbre** de cada candidato, propagada desde la calidad del genoma | nadie lo está haciendo `[H]` |
| El costo experimental estimado de validar cada uno | permite ordenar por relación valor/costo |

`[?]` **Lo que no sabemos y hay que preguntar:** en qué formato quiere el
laboratorio esa lista, cuántos candidatos tiene, de qué clase de gen son, y si
la priorización que esperan es para la rama del vector, la del virus o la de la
planta. Sin eso, el entregable puede ser correcto y aun así inutilizable. Está
en `preguntas_abiertas.md` como pregunta 1.

---

## Etapa 4 — Producción del ARN para ensayo

**Entrada:** la secuencia priorizada.

**Salida:** ARN en cantidad y pureza suficientes para ensayar.

`DOCUMENTADO` — APOLO tiene planta piloto desde abril de 2024: 120 m² en el
Puerto de la Innovación, que **combina producción y testeo** y produce **ARN,
enzimas y estabilizantes**. Capacidad declarada de hasta 200.000 hectáreas según
cultivo y aplicación. Badano, sobre el método: "lo sintetizamos".

`INFERENCIA NUESTRA [H]` — **Ninguna fuente pública dice con qué método
producen.** Que la planta fabrique **enzimas propias** apunta a transcripción in
vitro con polimerasa recombinante antes que a fermentación, porque una planta
de fermentación no necesita producir enzimas. Es inferencia, no dato.

**Para contraste de industria** `[R]`: GreenLight describe un proceso **libre de
células** que degrada ARN de levadura a nucleósidos monofosfato y lo
reconstruye, donde **lo único que varía entre productos es el molde de ADN**;
Renaissance BioScience usa **fermentación de levadura** donde la levadura es
simultáneamente fábrica y vehículo; RNAissance Ag usa **fermentación
microbiana**. Son tres arquitecturas de producción con consecuencias distintas
sobre el encaje regulatorio (ver etapa 11).

---

## Etapa 5 — Tamizaje in vitro / ex vivo

**Entrada:** el ARN producido.

**Salida:** confirmación de que la molécula silencia su blanco y sobrevive el
tiempo necesario.

`DOCUMENTADO` — Para *D. maidis* hay un ensayo *ex vivo* publicado y es
precisamente el que mide la barrera del desafío: el grupo de Catalano expuso
dsRNA a **homogenatos de tejido** del insecto y mostró que es **muy inestable**.
Ese ensayo es el tamizaje de supervivencia de la molécula, y es barato
comparado con un bioensayo.

`INFERENCIA NUESTRA [H]` — Qué tamizaje in vitro usa APOLO para hongos —cultivo
del patógeno con dsRNA, medición de germinación de esporas o de crecimiento
micelial— no está publicado. La literatura de terceros lo hace así, pero no
encontramos descripción del protocolo de la empresa.

**Nota de orden de etapas.** Para la rama del vector, el ensayo de estabilidad
en homogenato debería ir **antes** del bioensayo, porque una molécula que se
degrada en el intestino va a fallar el bioensayo por una razón que no tiene nada
que ver con la calidad de su diseño. Confundir esas dos causas de fracaso es un
riesgo real de interpretación, y es un argumento a favor de que la priorización
computacional incluya un criterio de estabilidad y no sólo de especificidad.
`[H]` — el orden es inferencia nuestra.

---

## Etapa 6 — Bioensayo sobre el organismo blanco

**Entrada:** el ARN validado in vitro.

**Salida:** efecto medido sobre el organismo, con su endpoint y su n.

`DOCUMENTADO` — Para *D. maidis*, los dos resultados publicados por el grupo de
Catalano: hembras tratadas que **depositaron menos huevos** que los controles,
con defectos estructurales en los ovarios revelados por disección —la nota del
CONICET **no da cifras, no informa mortalidad y no informa el método de
administración**— y la mejora de la respuesta al dsRNA del gen blanco cuando se
silencia **Dmai-dsRNase-2**.

`DOCUMENTADO` — Los endpoints que usa la literatura del campo: mortalidad por
estadio, consumo de follaje, reducción de transcripto del gen blanco, y
—advertencia explícita de Vatanparast et al.— **endpoints no letales y de ciclo
de vida**, porque los productos de RNAi pueden actuar lentamente. El caso
Calantha lo ilustra: las larvas **dejan de alimentarse en 2-3 días pero mueren
recién en 7-10 días** `[E]`, de la etiqueta de la EPA. Un bioensayo que mida
sólo mortalidad a 72 horas declararía fracaso a un producto registrado.

`[?]` Para la chicharrita, el gran faltante: **no hay publicado ningún dato de
mortalidad, ni dosis-respuesta, ni vía de administración** en lo que pudimos
abrir. El intento de leer el preprint con los métodos fue rechazado por el
filtro de la herramienta y no se reformuló.

---

## Etapa 7 — Formulación y vía de entrega

**Entrada:** un ARN con efecto demostrado en bioensayo.

**Salida:** un producto aplicable que lleva el ARN hasta donde tiene que actuar.

**Es la etapa que el organizador declara como barrera central.** "Las RNasas
limitan la entrega oral del ARN", y la pregunta abierta es qué estrategia
resuelve esa barrera.

`DOCUMENTADO` — Lo que hace APOLO: **pulverización foliar** y nada más.
"Es un líquido. Se aplica con un pulverizador sobre las hojas" (Badano); "se
aplica igual que cualquier insumo" (Zuljan). Más dos propiedades declaradas:
**estabilización que permite conservación a temperatura ambiente**, y **efecto
sistémico** con la planta haciendo circular el ARN para proteger hojas nuevas,
evidenciado por una observación cualitativa en maní.

`DOCUMENTADO` — Lo que hace el grupo académico del mismo fundador: la cátedra
AXA declara que la **entrega controlada de ARN** se aborda **mediante
nanotecnología** ("controlled delivery of RNAs using nanotechnology"), y el
laboratorio tuvo financiamiento 2022-2025 en nanotecnología para cultivo
orgánico de maní. La vía de nanoportadores está **en el programa académico, no
en el producto**.

`DOCUMENTADO` — Lo que resolvió la industria y la academia, con número:
BioClay/LDH llevó la protección antiviral de 5-7 días a **al menos 20 días** con
una sola pulverización, con dsRNA detectable a 30 días y resistencia al lavado;
minicélulas de *E. coli* dieron **12 días** en frutilla; cápsulas peptídicas
**40 días** en *Tribolium*; policationes en estrella **más del 97% a 7 días en
*Sogatella furcifera***, un hemíptero de floema como la chicharrita; y la
formulación por sí sola llevó la mortalidad de *Spodoptera exigua* de **16% a
53%**. Dato de contraste importante: en Calantha **no hay diferencia de
persistencia entre el dsRNA técnico y el formulado**, y los coadyuvantes que la
etiqueta recomienda son de **base látex o aceites minerales parafínicos** —es
decir, el único producto registrado del mundo para cultivo **no usa
nanoportador**.

`[?]` Advertencia de precisión que conviene no perder: **ninguna fuente abierta
atribuye a BioClay protección medida frente a fotodegradación UV ni frente a
nucleasas.** Las fuentes atribuyen la ventana extendida a **liberación sostenida
y resistencia al lavado**. Si esa afirmación circula, está sin respaldo.

`[?]` **De APOLO no hay ningún dato público de número de aplicaciones por
campaña, dosis por hectárea ni persistencia en días.** Para la etapa más
importante del embudo, es el hueco documental más grande del reporte.

---

## Etapa 8 — Ensayo de invernáculo sobre planta

**Entrada:** el producto formulado.

**Salida:** eficacia en planta entera bajo condiciones controladas.

`DOCUMENTADO` — APOLO declara un ensayo de **lechuga en invernáculo (2024)**
contra *Botrytis cinerea*, dentro del conjunto de 9 ensayos de severidad de
2023/2024 con "hasta 65% de reducción de severidad". Autoafirmación: los
resultados se muestran en gráficos, sin n ni estadística ni publicación.

`DOCUMENTADO` — El antecedente científico de la empresa en planta entera es el
experimento fundacional: **APOLO transcrito in vitro y pulverizado sobre
*Arabidopsis* activó sus genes blanco** (Attallah et al., 2025), y la aplicación
directa sobre hojas aumentó rápidamente la señalización de auxinas (Mammarella
et al., 2023, cuyo texto completo **no abrimos**).

`INFERENCIA NUESTRA [H]` — El criterio de pase de invernáculo a campo —umbral
de eficacia, número de repeticiones, diseño experimental— no está publicado.

---

## Etapa 9 — Ensayo a campo

**Entrada:** el producto que pasó invernáculo.

**Salida:** eficacia en condiciones reales, y los datos que exige el registro.

`DOCUMENTADO` — APOLO declara ensayos a campo en **frutilla (2024)**, **maní**
en Argentina, Brasil, Nicaragua y Estados Unidos, y **banano** en Ecuador,
Colombia y Costa Rica, además de tomate y vid. Es una red de ensayos
multi-país, lo que es coherente con el requisito normativo de abajo.

`NORMATIVO` — La Resolución SENASA 1004/2023 exige, para un producto sin
antecedentes de registro en el país, ensayos de eficacia agronómica en **al
menos tres zonas agroecológicas durante al menos dos campañas agrícolas**. La
alternativa es **seis ensayos mínimos en una sola campaña**, si la Dirección de
Agroquímicos y Biológicos verifica variabilidad climática. Para nuevas
formulaciones o **nuevas técnicas de aplicación**, se exige al menos una
campaña.

**Esto fija el reloj del embudo.** Dos campañas agrícolas son dos años
calendario, y son irreductibles por cómputo. Cualquier cronograma que el equipo
presente tiene que respetar este número o declarar que lo ignora.

---

## Etapa 10 — Organismos no objetivo y toxicología

**Entrada:** el producto y su principio activo.

**Salida:** el dossier de seguridad.

`NORMATIVO` — La evaluación de organismos no objetivo se hace **en cuatro
fases**, y la **fase I incluye aves, peces de agua dulce, abejas, lombrices y
artrópodos benéficos**, entre otros. Las fases II a IV sólo se exigen si la
fase I muestra resultados significativos. La toxicología es escalonada:
toxicidad aguda oral y cutánea, irritación cutánea y ocular con enfoque que
empieza por métodos in vitro, sensibilización cutánea, y mutagenicidad con
estudio inicial in vitro y estudios in vivo sólo si los in vitro dan positivo.

**Esto es una lista corta y concreta de genomas contra los cuales hay que
mostrar ausencia de coincidencia**, y es la razón por la que el tamizaje in
silico de la etapa 3 debería alinearse con **esta** lista y no con una genérica.
Es el hueco 6.2(d) del reporte.

`DOCUMENTADO` — Las rutas de exposición que nombra la literatura: alimentación
sobre planta tratada, acicalamiento tras aplicación tópica, contacto con suelo o
agua, y **depredación de la plaga expuesta**, que afecta a los enemigos
naturales. Y el precedente regulatorio concreto: para ledprona, EPA emitió
determinación de **"No Effect"** bajo la Endangered Species Act, con LD50 de
contacto agudo en abeja melífera **mayor a 24,3 µg ai/abeja** y oral crónico
**mayor a 47,2**, pero con la advertencia de que la especificidad abarca
**Coleoptera** como orden —hay riesgo potencial para coleópteros no blanco
dentro del lote tratado. La especificidad de un dsRNA es taxonómicamente más
ancha de lo que sugiere el nombre de la plaga.

`DOCUMENTADO` — Y la crítica que conviene anticipar, del caso belga: los
objetores señalaron que **la evaluación cubrió al ledprona solo, no al Calantha
formulado con coadyuvantes**. Es el argumento técnico más fuerte contra un
dossier de dsRNA, y aplica directamente a una empresa cuyo diferencial es la
formulación estabilizante.

---

## Etapa 11 — Trámite regulatorio

**Entrada:** el dossier completo.

**Salida:** el registro que habilita la venta.

`DOCUMENTADO` — Estado de APOLO: en trámite ante SENASA desde abril de 2024, sin
producto comercial en enero de 2025, y con el encaje regulatorio descrito por el
CEO en junio de 2025 como "our main issue right now" porque los productos no
entran en las categorías existentes.

`NORMATIVO` — La grieta, leída en la norma: el artículo 3 inciso c) define
bioinsumo como "producto que consista o haya sido producido por microorganismos
o macroorganismos de origen animal o vegetal" más "extractos o compuestos
bioactivos obtenidos a partir de ellos". **Ninguna de las categorías de
protección vegetal del artículo 2 nombra ácidos nucleicos ni ARN de doble
cadena.**

**Y acá el método de producción de la etapa 4 se vuelve regulatoriamente
decisivo** `[H]`: un ARN obtenido por **fermentación bacteriana** puede
argumentarse como "compuesto bioactivo obtenido a partir de" un microorganismo
y entrar por la definición; uno obtenido por **transcripción in vitro con
enzimas purificadas**, no tan fácilmente. Si la inferencia de la etapa 4 es
correcta y APOLO produce por vía enzimática, su arquitectura productiva le
complica el encaje en la única categoría que podría recibirlo. Es inferencia
nuestra y es, probablemente, la pregunta más interesante que se le puede hacer
al investigador.

`DOCUMENTADO` — Los marcos comparados, para contexto: Estados Unidos trata los
productos SIGS como **pesticidas bioquímicos** bajo FIFRA/FFDCA y la frase
operativa es que "no se consideran OGM a menos que contengan organismos
modificados viables"; Australia los define desde octubre de 2019 como
"agricultural chemical products" bajo APVMA y no bajo la OGTR —el marco más
limpio y explícito que existe; la Unión Europea los trata como **nueva clase de
sustancia activa** bajo el Reglamento 1107/2009, sin guía de datos dedicada; y
Brasil tiene el precedente más útil para la región, porque **CTNBio dictaminó
que un dsRNA pulverizable no es OGM** y lo encuadró como TIMP, lo que lo saca de
la vía OGM y lo deja como fitosanitario común. Argentina, en cambio, tiene un
marco de bioinsumos que no nombra al dsRNA y una vía CONABIA pensada para OGM.

`[?]` Existe además la **Resolución SENASA 694/2024**, que habilita reconocer
equivalencia de ingredientes activos grado técnico químicos o bioquímicos ya
aprobados por autoridades de Estados Unidos, México, Unión Europea, Reino Unido,
Australia, Nueva Zelanda y Brasil. Podría ser la vía más corta de entrada a
Argentina para un producto ya registrado afuera. **No verificamos que SENASA la
haya aplicado a un dsRNA ni que considere al dsRNA un "ingrediente activo
bioquímico" a estos efectos.** La norma no se abrió: se reconstruyó con prensa
secundaria.

`DOCUMENTADO` — Costo y plazo citados por la literatura: **4 años y USD 3-7
millones** para registrar un producto de dsRNA, frente a 12 años y USD 280
millones para un pesticida convencional.

---

## Etapa 12 — Escalado productivo y costo por hectárea

**Entrada:** el producto registrado.

**Salida:** un precio que el productor pueda pagar.

`DOCUMENTADO` — Lo único que dice APOLO: capacidad de hasta 200.000 hectáreas y
"el costo de producción bajó hasta 80 veces en el último año" (abril de 2024).
Es una reducción relativa sin base absoluta: **no permite derivar costo por
hectárea**.

`[?]` **No hay ningún precio de venta publicado de ningún producto de ARN
exógeno del mundo** —ni de APOLO, ni de Calantha, ni de Norroa, ni de Oifirax.
Lo único que existe son proyecciones de costo de fabricación de las propias
empresas: GreenLight proyectó **menos de USD 0,50/g** en 2019 y **~USD 1/g** en
2022, y con una dosis de ~10 g/ha eso daría del orden de **USD 10/ha** —cálculo
de un artículo, no precio de lista.

**Por qué esta etapa cierra el embudo y no es un apéndice.** El costo por gramo
determina el costo por hectárea, y el costo por hectárea determina **qué
cultivos son viables**. Es la explicación completa de por qué APOLO entró por
frutilla, tomate, banano y vid, y por qué el maíz —extensivo, margen bajo,
muchas hectáreas— quedaba declarado para 2027. Cualquier propuesta del equipo
sobre maíz tiene que reconocer que está apuntando al cultivo económicamente más
difícil del embudo, y decir por qué vale la pena igual.

---

## Resumen: dónde puede y dónde no puede intervenir un equipo sin laboratorio

| Etapa | ¿Puede un equipo de IA sin laboratorio? | Por qué |
| --- | --- | --- |
| 0 Definir el sistema | Parcialmente | Se puede mapear qué ruta es plausible contra cada agente |
| 1 Recursos genómicos | **Sí** | Curaduría, evaluación de calidad, cuantificación de incertidumbre |
| 2 Selección del blanco | **Sí** | Criterios de esencialidad, expresión y conservación |
| 3 Diseño y especificidad | **Sí, y es el punto de inserción** | Es la pregunta textual del organizador |
| 4 Producción | No | Planta, enzimas, purificación |
| 5 Tamizaje in vitro | No | Banco |
| 6 Bioensayo | No | Cámara de cría, colonia de insectos |
| 7 Formulación y entrega | No, pero sí los **datos** | El hueco es la falta de una tabla normalizada y comparable |
| 8 Invernáculo | No | Invernáculo |
| 9 Campo | No | Tres zonas, dos campañas |
| 10 No objetivo | **Parcialmente** | Tamizaje in silico alineado con la lista de la norma |
| 11 Regulatorio | No | Dossier, plata, años |
| 12 Costo | No | Ingeniería de procesos |

Tres etapas enteras y dos parciales. Es menos de lo que suele prometerse y es
suficiente para un aporte real, siempre que se entregue en el formato que la
etapa 4 consume y con las incertidumbres declaradas.
