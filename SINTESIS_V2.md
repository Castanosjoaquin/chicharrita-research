# Síntesis v2 — después del corpus oficial

Investigación del equipo para el Investigathón de Y-Hat (UBA), track
*La chicharrita del maíz: un desafío de diseño y validación con ARN*
(EPILAB · IFIBYNE, UBA-CONICET). Cerrada el 17 de octubre de 2026.

Este documento **reemplaza a `SINTESIS_v1.md`**, que queda en el repositorio como
el estado de lo que sabíamos antes de recibir el material oficial. La v1 se hizo
con fuentes públicas y supuestos explícitos; esta v2 la contrasta contra el
corpus del organizador, que son siete papers, dos enlaces a bases de datos, dos
enlaces a herramientas y **los cuatro candidatos preliminares del EPILAB**.

El detalle entrada por entrada de qué cambió está en
`research/ola2/CORRECCIONES.md`. El inventario del corpus, en
`research/ola2/MANIFEST.md`.

---

## (a) Qué cambió respecto de la v1

**La propuesta sobrevive, el plan se acorta y el argumento mejora.** No hubo que
tirar nada estructural: el encuadre de la v1 —priorizar candidatos dados, con
criterio escrito, evidencia citada e incertidumbre propagada— es exactamente lo
que el corpus pide y lo que las herramientas oficiales no hacen. Lo que cambió es
de qué lado están las dificultades.

Tres cosas se volvieron **más fáciles**. Los candidatos del EPILAB, que eran «la
única dependencia externa» y el riesgo número uno de la v1, están: son cuatro, y
ya los caracterizamos. El transcriptoma del vector, que la v1 declaraba camino
crítico y presupuestaba en cuatro días-persona, **no hay que construirlo**: hay
tres transcriptomas públicos descargables y un cuarto, propio del grupo que
publica, que conviene pedir. Y el tamizaje de off-target, que imaginábamos caro,
corre en 27,6 segundos sobre 575 Mb.

Dos se volvieron **más incómodas**. El ARN exógeno, según tres trabajos del
corpus con tres técnicas distintas, llega al apoplasto, al xilema y a la vaina del
haz, y **no hay evidencia de que entre al floema**, que es donde se alimenta
*Dalbulus maidis*: la vía de entrega que el corpus habilita es la adquisición
durante el sondeo de xilema, y eso hay que preguntarlo antes de dar nada por
sentado. Y en entrega oral a un hemíptero la mortalidad sube con la dosis mientras
el knockdown no correlaciona, con el control inespecífico matando a dosis alta: el
desenlace que midamos no es intercambiable con el otro.

Una se volvió **más valiosa de lo que esperábamos**. El término de conservación
del scoring, que en la v1 era el peor fundado de todos porque no había datos
poblacionales, tiene ahora un caso real y medido: la región de cápside elegida por
el EPILAB es 100 % idéntica **sólo al aislado de Costa Rica**, y contra los 45
registros brasileños la identidad cae a 91,5-93,5 %, con una mediana de 44 de 180
siRNA de 21 nt conservados. En GenBank no hay ninguna secuencia argentina de MRFV.

Y una conclusión general que corre el eje del aporte: **la herramienta oficial no
estima eficacia de ninguna forma.** dsRNA-Engineer cuenta coincidencias exactas de
k-meros con Bowtie y las suma; BLAST hace homología y anotación; ninguna de las
dos calcula termodinámica. La vara a superar es más baja de lo que suponía la v1,
y el trabajo no es modelar mejor que el estado del arte sino **decidir mejor con
lo que ya se calcula**.

### Los tres supuestos, cerrados

- **S1 — los patógenos y sus síntomas.** El corpus no los toca: ningún paper
  compara agentes del complejo. La corrección de la v1 —la reducción de grano es
  significativamente mayor con el espiroplasma y la de altura no difiere entre
  agentes— **queda en pie**. Lo que sí se movió es la identidad de dos agentes: el
  fitoplasma es *'Candidatus* Phytoplasma zeae', con genoma completo que
  descargamos y medimos (576.118 pb, 565 genes); y «MSMV» **sigue sin definirse**,
  porque la sigla mapea a dos taxones de familias virales distintas `[?]`.
- **S2 — «BLAST separa en porciones y calcula la termodinámica».** **Cerrado**,
  con cita a archivo y línea, desde las herramientas reales y no desde la
  literatura general. Ninguna de las dos calcula termodinámica. El tamizaje lo
  hace **Bowtie**; BLAST queda para homología entre plagas y anotación. Y el
  probable origen de la frase es **Primer-BLAST**, que sí calcula temperatura de
  fusión de cebadores con la tabla SantaLucia 1998, dentro del mismo sitio. La
  hipótesis de la v1 era correcta en lo conceptual e imprecisa en la atribución.
- **S3 — ARN exógeno frente a ARN no codificante.** Confirmado, y con la vuelta de
  tuerca del floema que está arriba.

---

## (b) Qué nos habilita el corpus, concretamente

Qué herramienta corre, con qué dato, y qué produce. Todo esto ya se ejecutó al
menos una vez en esta ola: no es una lista de intenciones.

| Herramienta | Dato de entrada | Qué produce | Estado |
| --- | --- | --- | --- |
| **BLAST+ 2.17.0** (local, Bioconda) | Los cuatro candidatos y los transcriptomas de referencia descargados | Identificación de cada candidato, y tamizaje por coincidencia perfecta de ≥19 nt contra maíz, polinizadores y cicadélidos | **Corrido.** Identificó los cuatro con confianza alta y produjo el mapa de off-target |
| **Bowtie 1.3.1** (local) | Ventanas de 16, 21 y 26 nt | El mismo tamizaje que hace la herramienta oficial, pero reproducible y desagregable | **Corrido**, y sirvió para determinar el formato de salida del servicio oficial |
| **ViennaRNA 2.7.2** (local) | Las ocho secuencias de la planilla | Energía libre y estructura secundaria por región | **Corrido.** La región de MP_MRFV es la menos estructurada de las cuatro |
| **dsRNA-Engineer** (web, oficial) | Secuencia **pública** de referencia | Conteo de on-target y off-target por especie, más los archivos Bowtie crudos | **Corrido** con PZ371507.1. **Nunca con las secuencias de EPILAB** |
| **NCBI Datasets y E-utilities** | Taxones del sistema | 17 conjuntos descargados, 43 archivos medidos con scripts propios | **Corrido.** 7,0 GB en `work/` |
| **miniprot + insecta_odb10** | Los tres ensamblados del vector | Completitud comparada: 97,7 %, 68,8 % y 35,5 % | **Corrido.** Proxy de BUSCO, calibrado |

Y lo que el corpus **no** habilita, dicho sin rodeos: no hay ninguna herramienta
que estime eficacia; no hay evaluación de organismos no objetivo en ninguno de los
siete papers; no hay un solo trabajo de ARNdc contra MRFV ni contra MSMV; y no hay
transcriptoma público de cicadélidos nativos no plaga ni de parasitoides de
*Dalbulus*, que son los no objetivo que de verdad importan acá.

---

## (c) La cartera re-priorizada

Misma matriz que la v1: cuatro ejes de 1 a 5, el riesgo entra invertido porque 5
es el peor caso, y *total = impacto + factibilidad + diferenciación + (6 −
riesgo)*, con rango de 4 a 20. Lo que cambia es que **la factibilidad ya no es una
estimación: está evaluada contra datos y herramientas que existen y que corrimos**.
Los puntajes siguen siendo juicio del equipo `[H]`.

| Línea | Impacto | Factibilidad | Diferenciación | Riesgo | **Total** | v1 |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| **L1** Priorización auditable con incertidumbre | 5 | 5 | 5 | 3 | **18** | 16 |
| **L3** Mapa de riesgo fuera de blanco ponderado | 5 | 3 | 5 | 3 | **16** | 14 |
| **L2** Validación retrospectiva | 3 | 4 | 3 | 4 | **12** | 13 |
| **L4** Ajuste fino de un modelo fundacional | 1 | 1 | 2 | 5 | **5** | 5 |

**Qué movió cada número.**

*L1 sube de 16 a 18.* **Factibilidad de 4 a 5:** desaparecieron los dos
obstáculos que la frenaban —los candidatos llegaron y el transcriptoma no hay que
construirlo—, y las tres herramientas del cálculo están instaladas y corridas.
**Diferenciación de 4 a 5:** la herramienta oficial no estima eficacia ni declara
incertidumbre, y su conteo de off-target no es interpretable como riesgo sin
desagregarlo. **Riesgo sigue en 3:** la transferencia de coleóptero a hemíptero
sigue sin resolverse y ningún dato del corpus la toca.

*L3 sube de 14 a 16 y pasa al segundo lugar.* **Impacto de 4 a 5:** hay un riesgo
medido y concentrado donde no lo buscábamos —30 siRNA de ≥19 nt de la región de
BicC sobre el ortólogo de *Homalodisca vitripennis*, contra cero en abeja, vaquita
y colémbolo y sólo tres bloques de 19 nt en maíz—. **Diferenciación de 4 a 5:**
ninguno de los siete papers del corpus evalúa organismos no objetivo, así que el
hueco es de la práctica publicada y no sólo de nuestra información.
**Factibilidad sigue en 3:** el tamizaje es barato, pero faltan los transcriptomas
de las especies que importan y las etiquetas de esencialidad para hemípteros.

*L2 baja de 13 a 12, y se ejecuta igual.* **Riesgo de 3 a 4:** el corpus muestra
que los desenlaces se desacoplan —la mortalidad sube con la dosis y el knockdown
no correlaciona— y que el ~95 % de knockdown en la especie blanco descansa sobre
tres réplicas de tres ninfas. Validar es más difícil de lo que pensábamos. **Pero
L2 no es una alternativa a L1: es su condición de validez**, y un ranking sin
medir cuánto discrimina sigue siendo una opinión. Lo que cambia es cómo se diseña:
hazard ratio y reducción de transcripto se miden y se reportan por separado.

*L4 sigue muerta, y ahora por partida doble.* A la falta de etiquetas en
hemípteros se suma que la herramienta que el organizador entrega bajo el rótulo de
diseño **no estima eficacia de ninguna forma**. No hay contra qué calibrar ni qué
superar con un modelo. **No se hace.**

### Dos módulos nuevos dentro de L1, los dos baratos

Son lo que el corpus agregó y no estaba en la v1. Ninguno es una línea nueva:
entran como parte del entregable de L1.

1. **Lectura desagregada del tamizaje oficial, candidato por candidato.** El
   número que devuelve dsRNA-Engineer suma coincidencias de tres tamaños de
   ventana y mezcla posiciones distintas de la consulta con parálogos alcanzados.
   Desagregarlo por tamaño de ventana, por posición y por transcripto afectado
   convierte un número opaco en una ficha interpretable. Es cómputo que ya
   corrimos una vez.
2. **Conservación entre aislados, que es el hallazgo más accionable de la ola.**
   Medir, para cada candidato antiviral, cuántos de sus siRNA sobreviven a la
   variación entre aislados. Está hecho para los dos candidatos de MRFV y el
   resultado es incómodo: la región de cápside sirve contra el aislado
   costarricense y pierde la mayoría de sus siRNA contra los brasileños. **Es un
   aporte que se puede llevar al investigador el día uno.**

---

## (d) El reparto para cuatro personas

Mismo presupuesto declarado que la v1: 8 horas por persona por semana, 96
horas-persona en tres semanas. La dependencia dura sigue siendo la misma y se paga
el primer día: cuatro horas los cuatro juntos para fijar los contratos de datos y
los casos de prueba. Lo que cambia es el contenido de cada rama, porque parte del
trabajo de la v1 ya está hecho.

| Rama | Entregable | Qué cambia respecto de la v1 | Horas |
| --- | --- | --- | --- |
| **P1 · Datos** | Paquete de datos congelado, con manifiesto de hashes, licencia por insumo y procedencia | **Se achica mucho.** No hay que ensamblar nada: los 17 conjuntos ya están descargados y medidos en `work/`, y hay tres transcriptomas TSA públicos. El trabajo es congelar, licenciar y documentar | 12 |
| **P2 · Tamizaje y conservación** | Informe de especificidad por candidato, **desagregado**, más el análisis de conservación entre aislados | **Se agranda y es ahora la rama más valiosa.** Suma los dos módulos nuevos de L1 y hereda el pipeline ya corrido | 30 |
| **P3 · Herramienta y reproducibilidad** | El artefacto de decisión: motor de puntaje, ficha por candidato, análisis de sensibilidad, entorno fijado y tests | Igual que en la v1, pero con entrada real: los cuatro candidatos en vez de ejemplos de juguete | 26 |
| **P4 · Evidencia, riesgo y apertura** | Dossier con la rúbrica poblada y citada, el panel de no objetivo con su vacío declarado, el estado regulatorio y el paquete de apertura | Suma la curaduría del hueco de cicadélidos nativos y parasitoides, que es ahora el riesgo principal | 28 |

El hito a proteger sigue siendo el mismo y ahora está más cerca: **la primera
corrida punta a punta sobre los cuatro candidatos reales**. Desde ahí el equipo
tiene un entregable completo aunque no pase nada más.

Y el plan B de la v1 —que no existan datos para entrenar nada— ya no es un
escenario: **es el hecho confirmado**, y el plan está construido para que no
importe. No entrenamos nada, el cálculo es determinista y por eso es reproducible
bit a bit.

---

## (e) Las preguntas para el investigador

Más precisas que las de la v1 porque están ancladas en archivos concretos. La
lista completa, con diez, está en `00_meta/PREGUNTAS_ABIERTAS.md`. Las cinco que
más mueven el plan:

1. **¿De dónde sale la columna «Nro de eficientes por gen» de
   `Sequences_EPILAB.xlsx`?** Declara 114, 35, 199 y 33, y ninguna de 2.132
   combinaciones de parámetros de una reimplementación local reproduce esos cuatro
   números. dsRNA-Engineer, además, no clasifica siRNA como eficientes: cuenta
   aciertos.
2. **¿Sobre qué aislado de MRFV se diseñaron los dos candidatos virales?** La
   región de cápside coincide al 100 % sólo con el aislado de Costa Rica y cae a
   91,5-93,5 % contra los brasileños. ¿Tienen secuencias de aislados argentinos?
3. **¿Cuál de los cuatro transcriptomas del vector usan, y nos pasan el suyo?**
   De eso depende si las posiciones de la planilla son reproducibles con datos
   públicos.
4. **¿El ARN exógeno llega al floema, o la vía real es el sondeo de xilema?** Tres
   trabajos del corpus lo encuentran en apoplasto, xilema y vaina del haz, y
   ninguno en floema.
5. **¿Cuál de los dos taxones es «MSMV»?** Mientras no se resuelva, cualquier
   diseño contra ese agente apunta a un blanco indefinido.

---

## Qué leer, y en qué orden

1. Este documento.
2. `research/ola2/CORRECCIONES.md` — qué cambió de la v1, entrada por entrada.
3. `research/ola2/W5_secuencias_epilab/REPORT.md` — los cuatro candidatos.
4. `research/ola2/W2_herramientas/REPORT.md` — qué hacen por dentro las dos
   herramientas oficiales, y la respuesta a S2.
5. `research/ola2/W1_papers/REPORT.md` — el corpus de papers y su lectura
   obligatoria.
6. `research/ola2/W4_genomas/viabilidad_lineas.md` y
   `research/ola2/W3_bases_datos/plan_ingesta.md` — con qué datos contamos.
7. `SINTESIS_v1.md` y los cinco reportes de la ola 1 — el marco, que sigue
   vigente salvo donde las correcciones dicen lo contrario.
8. `00_meta/` — glosario, decisiones, caminos probados, preguntas abiertas y
   fuentes.

Cada carpeta tiene su `index.html`, y la portada del repositorio es `index.html`.
