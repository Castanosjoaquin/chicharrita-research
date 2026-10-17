# Investigathon Y-Hat — ARN exógeno contra la chicharrita del maíz

Repositorio de la investigación previa de un equipo de cuatro estudiantes de
Ingeniería en IA (UdeSA) para el Investigathon de Y-Hat (UBA).

La pregunta del track, textual:

> ¿Cómo diseñar y priorizar una solución basada en la aplicación de ARN exógeno
> que utilice el mecanismo de RNAi para silenciar genes del vector y/o de los
> patógenos asociados, de manera biológicamente informada y reproducible, con
> mayor probabilidad de acción y menor riesgo para el maíz, los organismos no
> objetivo y el ecosistema?

El equipo no aporta laboratorio. Aporta bioinformática y datos, desarrollo
computacional e innovación abierta, y compite en esos tres ejes en lugar del eje
de biología y evidencia experimental (`00_meta/DECISIONS.md`, D1). Todo lo que
propongamos tiene que ser demostrable sin un solo experimento húmedo.

## Para qué sirve este repositorio

Es la investigación que hacemos **antes** de que nos entreguen las herramientas,
las bases de datos y la bibliografía oficiales del evento. Su objetivo es que el
día del Investigathon no se nos vaya la primera mitad entendiendo el dominio:
que lleguemos sabiendo qué silencia qué, qué hace ya la industria, qué datos
existen y qué vamos a construir cada uno.

## Por dónde empezar

| Si querés… | Leé |
| --- | --- |
| el panorama completo en una sentada | `SINTESIS_V2.md` |
| qué cambió al llegar el material oficial | `research/ola2/CORRECCIONES.md` |
| los cuatro candidatos del EPILAB | `research/ola2/W5_secuencias_epilab/REPORT.md` |
| entender la biología desde cero | `research/R1_fundamentos/REPORT.md` |
| saber qué significa cada término | `00_meta/GLOSARIO.md` |
| la versión navegable, para leer en el celular | `index.html` y el `index.html` de cada carpeta |

`SINTESIS_V2.md` es el entregable del equipo: qué cambió al contrastar con el
corpus oficial, qué nos habilita concretamente cada herramienta y cada dato, la
cartera de enfoques re-priorizada con su matriz, el reparto para cuatro personas
y las preguntas concretas para el investigador.

`SINTESIS_v1.md` es la versión anterior y se conserva a propósito: es el estado
de lo que sabíamos **antes** de recibir el material oficial. El historial de lo
que creíamos y por qué cambiamos de opinión es parte del valor del repositorio, y
por eso las correcciones se agregan fechadas en lugar de reescribir los reportes.

## Las dos olas

| Ola | Qué es | Dónde |
| --- | --- | --- |
| **Ola 1** | Investigación previa con fuentes públicas, sin el material oficial. Cinco investigaciones, R1 a R5. | `research/R1_*` a `research/R5_*`, `SINTESIS_v1.md` |
| **Ola 2** | Contraste contra el corpus oficial del Investigathón: papers, bases de datos, herramientas y los candidatos del EPILAB. Cinco investigaciones, W1 a W5. | `research/ola2/`, `SINTESIS_V2.md` |

El corpus oficial vive en `YHat-Biotech/` y **no está en el control de
versiones**: contiene secuencias no publicadas del EPILAB y PDF con derechos de
autor, y este repositorio tiene remoto público (`00_meta/DECISIONS.md`, D10). Su
inventario completo, archivo por archivo, está en `research/ola2/MANIFEST.md`.

## Las cinco investigaciones

| Carpeta | Qué responde |
| --- | --- |
| `research/R1_fundamentos/` | La biología, desde ADN hasta el complejo de achaparramiento, escrita para gente de IA sin biología. Incluye la pregunta que define la estrategia: ¿sobre qué actores funciona realmente el RNAi? |
| `research/R2_attention_diseno_arn/` | Evaluación de una idea del equipo (usar *attention* para diseñar el ARN): qué parte se sostiene, qué parte era un malentendido, y qué queda reformulado con rigor. Veredicto en la primera página. |
| `research/R3_apolo_biotech/` | Qué hace Apolo Biotech y qué hace el resto de la industria del ARN aplicado al agro. Sirve para no proponer como novedad algo que ya está hecho. |
| `research/R4_frontier_ml_rna/` | Estado del arte en aprendizaje automático aplicado a biotecnología de ARN: modelos fundacionales, estructura, predicción de eficacia. Nuestro eje de mayor ventaja comparativa. |
| `research/R5_metodologias_ejes/` | Cómo se trabaja en cada uno de los tres ejes, la rúbrica de priorización y el plan para cuatro personas. |

Cada carpeta contiene `REPORT.md` (la fuente de verdad, con el contenido
completo y citado), `index.html` (la vista de lectura), `sources.json` (las
fuentes estructuradas) y `notes/` con el material de trabajo.

## La memoria del proyecto

`00_meta/` es lo que sobrevive a cualquier sesión de trabajo:

- `GLOSARIO.md` — cada término con su definición en una línea y por qué nos importa.
- `DECISIONS.md` — una entrada por decisión, en formato ADR liviano.
- `CAMINOS_PROBADOS.md` — qué se intentó y qué se descartó, con el motivo.
- `PREGUNTAS_ABIERTAS.md` — lo que no sabemos y lo que hay que pedir o preguntar.
- `FUENTES.md` — la bibliografía consolidada, con nivel de evidencia y acceso.

## Reglas de trabajo

Están en `CLAUDE.md` y rigen para todo el repositorio. Las tres que más se
notan al leer:

- Toda afirmación técnica lleva fuente, y nadie cita una fuente que no abrió.
  Sin fuente, no entra al reporte.
- Cada afirmación relevante va marcada `[E]` establecido, `[R]` reportado, `[H]`
  hipótesis nuestra o `[?]` incierto. Cuando dos fuentes se contradicen se
  reportan las dos y se marca `[?]`.
- Un vacío documentado es un resultado válido; un vacío tapado con texto
  plausible, no.

El alcance es control fitosanitario agrícola con información pública. Queda
fuera, sin excepción, cualquier cosa que aumente la virulencia, la
transmisibilidad o el rango de hospedadores de un patógeno, y cualquier diseño
dirigido a dañar especies no objetivo. Toda propuesta de diseño va con su
contracara de riesgo.

## Los HTML

Cada `index.html` es un archivo autocontenido, sin build: se abre con doble clic
y se lee en el celular. Son la vista de lectura; el `REPORT.md` es la fuente de
verdad y no hay nada afirmado en un HTML que no esté en su `REPORT.md` con su
fuente.
