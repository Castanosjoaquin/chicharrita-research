# Plan de equipo: cuatro personas, cuatro ramas, un entregable que decide

Versión 1.1, 2026-10-17.

Cambios de la v1.0 a la v1.1, hechos al ampliar las fuentes para `REPORT.md` y
explicados en el lugar donde ocurren: P1 suma el genoma completo del fitoplasma
del maíz, que la v1.0 daba por inexistente; P2 suma el tamizaje con el criterio
de off-target de la EFSA, con su costo en horas declarado y de dónde salen; P4
suma tres precedentes regulatorios nuevos; y el plan B 6.2 suma a dsRNAEngineer
como sustituto web si se cae la rama de tamizaje.

## 0. Supuestos de capacidad, declarados

Cuatro estudiantes de tercer año de Ingeniería en IA con cursada en paralelo.
El presupuesto realista es **8 horas por persona por semana**, en bloques de 2 a
4 horas, no en jornadas completas: 32 horas-persona por semana para el equipo.
Tres semanas de preparación antes del evento son **96 horas-persona**, y ese es
el número con el que está dimensionado todo lo que sigue. Si el plazo real es
menor, se recorta por la sección 7, que dice explícitamente qué se cae primero.

`[?]` La fecha del evento no está fijada en el material que tenemos. El plan está
escrito en semanas relativas (S-3, S-2, S-1, evento) y hay que anclarlo en
cuanto se sepa la fecha.

## 1. El principio de diseño del plan: contratos antes de datos

El riesgo real de un equipo de cuatro con poco tiempo no es la falta de
capacidad: es que tres esperen a uno. Acá se resuelve con una decisión concreta
y verificable, y no con una metodología: **el primer entregable del equipo, en
las primeras cuatro horas, son dos archivos de contrato y sus datos de prueba.**

- `esquema_candidato.json` — los ocho campos de la ficha de entrada de
  `RUBRICA.md` sección 1.
- `esquema_score.json` — la salida: un objeto por candidato con los ocho
  criterios, su puntaje, su marcador de evidencia, su marca (P), su cita, y los
  totales conservador y optimista.
- `fixtures/` — cinco candidatos de juguete que cumplen el esquema, con
  secuencias cortas inventadas y marcadas como tales.

Con esos tres artefactos, **cada rama puede avanzar contra datos falsos mientras
los reales llegan**. La herramienta se construye y se testea sin esperar el
tamizaje; el tamizaje se desarrolla sin esperar la rúbrica poblada; la rúbrica se
puebla sin esperar la herramienta. Es la única dependencia dura del plan y se
paga el primer día.

## 2. Reparto: quién hace qué y qué entrega

### P1 — Datos y genómica

**Rama:** `datos/`. **Entregable propio:** un **paquete de datos congelado y
versionado** (*data package*), con su manifiesto de hashes, su licencia por
insumo y su procedencia, más el conjunto de ORF del vector sobre el que se
diseña.

Qué hace, en orden, con lo ya verificado en `notes/evidencia_verificada.md`:

1. Baja y congela el transcriptoma de referencia: los 56.116 transcriptos del
   TSA `GITV00000000` (Xu et al. 2021), que tiene 82,4 % de completitud BUSCO.
   Es el insumo central y no requiere permiso.
2. Baja el transcriptoma y proteoma de *Zea mays* del FTP de Ensembl Plants, que
   es la URL verificada que sí entrega archivos.
3. Baja el ensamblado cromosómico `GCA_975739785.1` del Sanger y el CIAP v1 del
   INTA `GCA_054756405.1`, y **documenta el hallazgo que condiciona todo: ninguno
   de los dos tiene anotación de genes en el NCBI.** Por eso el diseño se hace
   sobre el transcriptoma y no sobre el genoma.
4. Baja los genomas de patógenos que existen: *S. kunkelii* `GCA_001274875.1`
   (completo y anotado, 1.685 genes codificantes) y —**corrección del
   2026-10-17**— el del fitoplasma del achaparramiento arbustivo del maíz, que
   también está completo y anotado y que la v1.0 de este plan daba por
   inexistente: `GCA_001712875.1` / `GCF_001712875.1`, cepa M3, 576.118 pb en una
   sola secuencia, aislado de un *Dalbulus maidis* colectado en Piracicaba
   (Brasil) en 2013, hoy nombrado '*Candidatus* Phytoplasma zeae'. El error venía
   de buscar por el nombre informal en lugar del taxón, que recién recibió nombre
   formal en 2026 (Pellegrinetti et al., *IJSEM* 76(10), doi
   10.1099/ijsem.0.007301). Baja además los cuatro de '*Candidatus* Phytoplasma
   asteris', consignando que ninguno es un aislado del complejo del maíz, y
   consigna que los tres genomas nuevos de ese trabajo (`PRJNA1294367`) no
   devuelven ensamblados registrados y hay que buscarlos por BioSample.
5. Corre TransDecoder sobre el TSA para tener los ORF, porque la evidencia dice
   que apuntar al ORF supera a apuntar a las UTR.
6. Corre BUSCO sobre el transcriptoma para tener nuestro propio número y no
   citar el del paper.

**Horas estimadas:** 20 horas-persona. La descarga es lenta pero desatendida; el
trabajo real son el manifiesto, las licencias y TransDecoder.

**Lo que NO hace, decidido de antemano:** no ensambla transcriptoma *de novo*
(1.727 millones de lecturas a ~1 GB de RAM por millón es inalcanzable y el
ensamblado ya está publicado) y no anota el genoma de 972 Mb. Si hace falta un
paso pesado, va a Galaxy Europe, que es gratis y es lo que usó el grupo que
publicó RNAi en esta especie.

### P2 — Diseño y tamizaje de especificidad

**Rama:** `tamizaje/`. **Entregable propio:** el **informe de especificidad por
candidato**, que es la evidencia de los criterios C1b, C2 y C3 de la rúbrica, y
el que el ejemplo trabajado identifica como la medición que más mueve el orden.

Qué hace:

1. Implementa el derivado de siRNA: ventana deslizante de 21 nt sobre el
   disparador, con 19 a 23 nt como parámetro.
2. Implementa las cuatro features con evidencia de Cedden et al. (2025):
   asimetría termodinámica, autoplegado de la hebra antisentido, GC en las
   posiciones 9 a 14 de la antisentido y adenina en la posición 10. Usa
   ViennaRNA, que corre nativo en macOS y Linux. **No usa si-Fi**, porque corre
   solo en Windows, y en cambio reimplementa sus reglas de selección de hebra
   guía, que el paper describe explícitamente.
3. Corre el tamizaje de off-target con Bowtie 1 con 0, 1 y 2 mismatches contra
   maíz, contra *D. maidis* y contra los taxones no objetivo que le pasa P4.
   Aplica el umbral de 19 nt complementarios de Cedden (2026). **Agregado del
   2026-10-17:** corre además el conjunto de reglas de la guía de la EFSA de
   2025 (doi 10.2903/j.efsa.2025.9321) descrito en la compuerta G2 de
   `RUBRICA.md`, y reporta los dos resultados por separado. No son
   intercambiables: Bowtie con hasta 2 mismatches no evalúa huecos, pares G:U,
   restricciones de posición ni el cociente de energía libre, y el criterio de la
   EFSA devuelve un superconjunto de hits. Reporta también **cuántos ARN pequeños
   distintos coinciden con el mismo transcripto**, que es lo que la guía pide
   usar como foco del análisis. Esta tarea agrega del orden de 4 horas-persona a
   la rama, que se toman de las 28 ya asignadas recortando la exploración de
   largos de siRNA distintos de 21 nt.
4. Cruza con Rfam para no diseñar sobre una familia de ARN no codificante
   conservada.
5. Produce, por candidato, el objeto que cumple `esquema_score.json` para C1b,
   C2 y C3, con los conteos de hits y la lista de taxones **donde no se pudo
   mirar**.

**Horas estimadas:** 28 horas-persona, la rama más cargada. Es también la que
produce la evidencia más decisiva, así que es el lugar correcto para poner las
horas.

### P3 — Herramienta y reproducibilidad

**Rama:** `herramienta/`. **Entregable propio:** el **artefacto de decisión**:
una herramienta que toma las fichas de candidatos y los informes de tamizaje y
emite el orden, las fichas de decisión y el análisis de sensibilidad, de forma
reproducible y auditable. El detalle de arquitectura, stack y riesgos está en
`REPORT.md` sección 2; acá va el compromiso de entrega.

Qué hace:

1. El día uno, los contratos y los *fixtures* de la sección 1.
2. El motor de puntaje: lee fichas, aplica pesos, aplica los topes de la sección
   5.2 de la rúbrica, calcula los totales conservador y optimista, y corre el
   análisis de sensibilidad con los dos esquemas de pesos.
3. El generador de fichas de decisión, que es el entregable que lee un jurado:
   una carilla por candidato con puntaje, marcador, cita y "dónde no pudimos
   mirar".
4. El entorno reproducible: `environment.yml` con versiones fijas desde Bioconda,
   semilla fijada donde haya cualquier muestreo, datos versionados por hash con
   DVC, un `Makefile` o un flujo de Snakemake que regenere todo con un comando, y
   un DOI por el flujo de GitHub-Zenodo para la versión que se presenta.
5. Tests: los topes y el orden son lógica discreta y se testean con los
   *fixtures*. Un test que falla es más defendible ante un jurado que una
   pantalla linda.

**Horas estimadas:** 26 horas-persona.

### P4 — Rúbrica aplicada, riesgo, regulación e innovación abierta

**Rama:** `evidencia/`. **Entregable propio:** el **dossier de evidencia**: la
rúbrica poblada candidato por candidato con su cita verificada, la lista de
taxones no objetivo con su justificación, el estado regulatorio, y el paquete de
apertura del proyecto.

Qué hace:

1. Construye la lista de taxones no objetivo para C3 y se la pasa a P2 el primer
   día, porque es su dependencia. Usa las dos fuentes verificadas: los grupos de
   dsRIP y los nueve taxones representativos de Ahmad et al. (2016), declarando
   que es un trabajo de autores de Monsanto financiado por Monsanto.
2. Cura la evidencia de C1a por gen blanco: los tres trabajos del grupo de
   Catalano en *D. maidis* (Dalaisón-Fuentes 2022 y 2023, Andrada 2026) con sus
   números y sus vías de entrega.
3. Arma el argumento regulatorio de C7 con el precedente de ledprona de la EPA
   y, **desde el 2026-10-17**, con tres piezas más que ya están verificadas: la
   guía de la EFSA de 2025 para plantas modificadas por RNAi —con sus dos límites
   de alcance declarados, que es para plantas modificadas y que no cubre riesgo
   ambiental—, el número de registro de ledprona como bioplaguicida (EPA
   94614-2) y el expediente presentado en Estados Unidos, la Unión Europea y
   Brasil para un dsRNA contra *Erysiphe necator* (*Pest Management Science*
   2026, doi 10.1002/ps.70806). El expediente brasileño importa: mueve el ancla
   regulatoria de la clase de producto en la región.
4. Arma el paquete de apertura, que es el entregable del eje de innovación
   abierta y está detallado en `REPORT.md` sección 3: licencias de salida,
   declaración de licencias de entrada (incluida la cláusula no comercial del
   ensamblado del INTA), el registro de resultados negativos, y el aporte
   concreto de datos.
5. Mantiene `00_meta/` al día: glosario, decisiones, caminos probados y
   preguntas abiertas. No es trabajo administrativo: es lo que hace que el
   descarte de una opción valga tanto como un hallazgo.

**Horas estimadas:** 22 horas-persona.

## 3. Paralelismo real: el grafo de dependencias

Una sola dependencia dura, y se paga el primer día:

```
      DÍA 1 (4 h, los cuatro juntos)
      contratos + fixtures + lista de taxones (P4 → P2)
                        |
     +---------+--------+--------+---------+
     |         |                 |         |
    P1        P2                P3        P4
   datos   tamizaje         herramienta  evidencia
     |         |                 |         |
     |  (usa fixtures hasta      |         |
     |   que P1 entrega)         |         |
     +----> paquete de datos ----+         |
               |                 |         |
               +---> informe de tamizaje --+
                                 |         |
                                 +--> ORDEN + FICHAS <--+
```

Las dependencias blandas y cómo se neutralizan:

| Dependencia | Riesgo | Cómo se neutraliza |
| --- | --- | --- |
| P2 necesita los datos de P1 | P2 bloqueado | P1 entrega en 48 horas un paquete mínimo con un solo transcripto real; P2 desarrolla contra los *fixtures* |
| P3 necesita salidas de P2 | P3 bloqueado | los *fixtures* cumplen el mismo esquema que la salida real |
| P4 necesita la herramienta para poblar la rúbrica | P4 bloqueado | P4 puebla en una planilla o en YAML a mano; la herramienta la lee después. La rúbrica es aplicable a mano y eso es deliberado |
| P2 necesita la lista de taxones de P4 | P2 bloqueado | se entrega el día 1, antes que cualquier otra cosa de P4 |

Ninguna rama tiene a otra en su camino crítico después del día 1. Eso es lo que
responde la pregunta de verificación de si el plan asigna trabajo paralelo real.

## 4. Cronograma

| Cuándo | Qué pasa | Quién |
| --- | --- | --- |
| **S-3, día 1** (4 h, juntos) | Contratos, *fixtures*, lista de taxones. Se declaran los pesos de la rúbrica **antes** de ver ningún candidato y se registra la decisión en `00_meta/DECISIONS.md` | los cuatro |
| **S-3, resto** (28 h) | P1 descarga y congela; P2 implementa features y derivado de siRNA; P3 motor de puntaje y topes con tests; P4 taxones, C1a y C7 | en paralelo |
| **Sincronización 1** (30 min, fin de S-3) | ¿Existe el paquete mínimo? ¿Corre el motor sobre *fixtures*? Si alguna respuesta es no, se activa la sección 7 | los cuatro |
| **S-2** (32 h) | P1 TransDecoder y BUSCO; P2 tamizaje completo sobre nuestros cinco candidatos de ejemplo; P3 fichas de decisión y entorno reproducible; P4 dossier y paquete de apertura | en paralelo |
| **Sincronización 2** (30 min, fin de S-2) | Primera corrida punta a punta sobre los cinco candidatos propios. **A partir de acá el equipo tiene un entregable completo aunque no pase nada más.** Este es el hito que hay que proteger | los cuatro |
| **S-1** (32 h) | Endurecimiento: tests, DOI, documentación de una página por rama, y el **paquete offline congelado** de la sección 7.4. Ensayo de la presentación con los candidatos propios | en paralelo |
| **Sincronización 3** (2 h, fin de S-1) | Integración y ensayo completo. Se congela la versión que se presenta | los cuatro |
| **Evento** | Se reemplazan nuestros candidatos por los del EPILAB y se vuelve a correr. Si el formato lo permite, se presenta el orden, la sensibilidad y la medición faltante | los cuatro |

El punto no obvio de este cronograma es que **la fase de evento es una
sustitución de entrada, no una construcción**. Lo que se construye antes es la
capacidad de producir una decisión; lo que se hace el día del evento es
producirla sobre los candidatos reales. Si los candidatos del EPILAB llegan
antes, mejor: se corre antes.

## 5. Qué se entrega y qué se presenta

**Se entrega** (el repositorio, con DOI): la rúbrica, la herramienta con sus
tests y su entorno, el paquete de datos con su manifiesto y sus licencias, los
informes de tamizaje, las fichas de decisión por candidato, el dossier de
evidencia, el paquete de apertura y la memoria del proyecto en `00_meta/`.

**Se presenta**, y esto es deliberadamente austero porque el organizador dice
que no gana la interfaz más vistosa:

1. **Una decisión**, en una oración: qué candidato merece validación primero y
   por qué.
2. **Una tabla**: los candidatos por criterio, con los marcadores de evidencia
   visibles. Que se vea dónde el puntaje es `[E]` y dónde es `[?]`.
3. **Un gráfico de sensibilidad**: cómo cambia el orden al cambiar los pesos y
   al resolver los criterios marcados (P). Es lo que demuestra que entendimos la
   incertidumbre en lugar de taparla.
4. **Una frase sobre qué medir después**, con su costo. Es la parte que convierte
   el ranking en una decisión científica.

Lo que **no** se presenta: una pantalla con filtros. La herramienta puede tener
una vista de lectura, pero no es el argumento.

## 6. Plan B: el escenario de que no existan los datos para entrenar nada

Este es el escenario de fracaso más probable y hay que decir algo incómodo
primero: **ya es verdad hoy, y el plan está construido para que no importe.**

No existe un conjunto de datos de pares secuencia-eficacia en *Dalbulus maidis*
con el que entrenar un modelo. Lo más cercano son 31 siRNA probados en
*Tribolium castaneum* (Cedden et al. 2025), de los cuales 29 entraron al modelo
de Cox, con una C de Harrell de 0,76; eso es un conjunto de datos de un
coleóptero, con n = 29, para un modelo de supervivencia, no un conjunto de
entrenamiento para un modelo de aprendizaje automático en un hemíptero. Y los
propios autores marcan que falta validación fuera de coleópteros.

Consecuencia, que conviene decir en voz alta ante el jurado antes de que lo
pregunten: **no vamos a entrenar nada, y eso es una decisión, no una
limitación.** Lo que el track pide es una solución "biológicamente informada y
reproducible" que priorice, y priorizar con criterio explícito y evidencia citada
no requiere entrenamiento. La rúbrica y el tamizaje son cómputo determinista
sobre secuencias públicas: no tienen conjunto de entrenamiento porque no lo
necesitan, y por eso son reproducibles bit a bit.

Los niveles del plan B, del más probable al más grave:

### 6.1 No hay candidatos del EPILAB a tiempo

Se corre sobre los cinco candidatos propios de `RUBRICA.md` sección 7, que están
construidos sobre blancos con evidencia publicada y verificada (*BicC*,
*Dmai-dsRNase-2*, *eth*, un gen esencial de *S. kunkelii*, el genoma de MRFV).
El entregable no cambia de naturaleza: cambia la entrada. **Ya está hecho**, y
por eso la sincronización 2 es el hito a proteger.

### 6.2 Falta un insumo de datos

Para cada insumo hay un sustituto declarado, y es parte del entregable de P1:

| Si falta | Sustituto |
| --- | --- |
| el TSA `GITV00000000` | las lecturas de `PRJNA579843` y cuantificación con Salmon contra los transcriptos que sí se bajen; o el transcriptoma propio del laboratorio citado por Andrada et al. |
| el transcriptoma de maíz de Ensembl Plants | el proteoma de *Z. mays* de UniProtKB, con tamizaje por tBLASTn en lugar de Bowtie, como hizo el grupo de Catalano |
| transcriptomas de taxones no objetivo | se declara el vacío de datos en la ficha, que es parte del puntaje de C3, y se usan los grupos que ofrece dsRIP, o los 942 transcriptomas precargados de dsRNAEngineer, que incluyen especies de evaluación de seguridad (agregado 2026-10-17; es web, así que la salida hay que exportarla y versionarla) |
| el ensamblado del INTA (licencia no comercial) | el cromosómico del Sanger `GCA_975739785.1`, que además es de mejor calidad |

### 6.3 Un criterio de la rúbrica resulta no puntuable para ningún candidato

Se reporta con todos los candidatos en el mismo valor y se declara no
discriminante, **no se elimina**. Un criterio que no distingue sigue siendo
información: dice que la decisión no se juega ahí. Eliminarlo sería mover la
cancha después de ver los resultados.

### 6.4 No hay conectividad o los servicios web están caídos el día del evento

El riesgo más mundano y el más caro, porque dsRIP, Galaxy y las API del NCBI son
remotos. Mitigación, que se ejecuta en S-1 y es una acción concreta, no una
precaución: **el paquete offline congelado.** Transcriptoma de *D. maidis*
(decenas de MB), transcriptoma y proteoma de maíz, índices de Bowtie ya
construidos, binarios de ViennaRNA, el entorno de conda exportado, y los datos
de referencia de los taxones no objetivo. Cabe en un pendrive y en el disco de
cada integrante. Con eso, todo el camino crítico corre sin red.

### 6.5 Se cae una persona

Cada rama tiene un segundo responsable nombrado, y el reparto está hecho para que
el emparejamiento tenga sentido técnico: P1↔P2 comparten el terreno de datos y
secuencia, P3↔P4 comparten el de la decisión y su trazabilidad. Si se cae P3, la
rúbrica se aplica a mano sobre una planilla, porque fue diseñada para eso y el
ejemplo trabajado de la sección 7 se calculó así. Si se cae P2, se usa dsRIP por
web para los candidatos principales y se declara la dependencia. Si se cae P1,
se trabaja con el paquete mínimo. Si se cae P4, se usan las citas ya verificadas
en `notes/evidencia_verificada.md`, que para eso están escritas con su fuente.

## 7. Qué se recorta si el plazo se acorta, y en qué orden

Declarado de antemano para no tener que decidirlo bajo presión:

1. **Primero se cae** el análisis sobre patógenos (K4 y K5 del ejemplo). Son los
   candidatos con `C1a` más débil y los que más preguntas abiertas arrastran.
2. **Después**, el tamizaje contra la lista extendida de taxones no objetivo: se
   queda con polinizadores y enemigos naturales, y se declara el recorte.
3. **Después**, el DOI y el empaquetado formal: se entrega el repositorio con el
   `environment.yml` y el commit fijado, que es reproducible aunque no tenga DOI.
4. **Nunca se cae**: la rúbrica aplicada con su evidencia, el tamizaje de
   especificidad contra maíz, y las fichas de decisión. Son el entregable; el
   resto es andamiaje.
