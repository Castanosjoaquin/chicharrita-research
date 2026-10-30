# ARN exógeno contra la chicharrita del maíz

Investigación de un equipo de cuatro estudiantes de Ingeniería en Inteligencia
Artificial (Universidad de San Andrés) para el Investigathón de Y-Hat (UBA), en
el track de diseño de soluciones basadas en ARN interferente (RNAi) contra
*Dalbulus maidis* —la chicharrita del maíz— y los patógenos que transmite.

La pregunta del track, textual:

> ¿Cómo diseñar y priorizar una solución basada en la aplicación de ARN exógeno
> que utilice el mecanismo de RNAi para silenciar genes del vector y/o de los
> patógenos asociados, de manera biológicamente informada y reproducible, con
> mayor probabilidad de acción y menor riesgo para el maíz, los organismos no
> objetivo y el ecosistema?

El equipo no aporta laboratorio. Aporta bioinformática, datos y desarrollo
computacional: todo lo que hay acá es reproducible sin un solo experimento
húmedo.

## Qué construimos

Un sistema de **priorización auditable de candidatos a silenciamiento**, que
toma un gen blanco y devuelve no sólo un puntaje sino la evidencia que lo
sostiene y el riesgo que arrastra.

Tres piezas:

1. **Priorización con incertidumbre declarada** (`pipeline/`). Cada candidato
   se ordena por evidencia de esencialidad, conservación y facilidad de entrega,
   y cada número viaja con su fuente y su grado de confianza. Las herramientas
   del estado del arte devuelven un conteo; nosotros devolvemos una ficha que se
   puede discutir.
2. **Mapa de riesgo fuera de blanco ponderado** (`tools/sifi21_port/`). El
   tamizaje habitual cuenta coincidencias y las suma. Nosotros las desagregamos
   por tamaño de ventana, por posición y por transcripto afectado, y las medimos
   contra organismos que no son el objetivo: maíz, abeja, enemigos naturales,
   fauna del suelo.
3. **Validación retrospectiva** (`baseline_dsrip/`, `research/ola4/`). Un
   ranking que nunca se midió contra resultados conocidos es una opinión. Acá se
   mide cuánto discrimina.

Dos resultados que salieron del camino y vale la pena mirar:

- La **conservación entre aislados** del virus del rayado fino (MRFV) rompe
  candidatos que parecían sólidos: una región de cápside que funciona contra el
  aislado costarricense pierde la mayoría de sus siRNA contra los brasileños.
- El riesgo fuera de blanco **no estaba donde lo buscábamos**: aparece
  concentrado en el ortólogo de *Homalodisca vitripennis*, no en los organismos
  no objetivo que suelen evaluarse.

## Por dónde empezar

| Si querés… | Andá a |
| --- | --- |
| el resumen de la investigación completa | [`SINTESIS_V2.md`](SINTESIS_V2.md) |
| el póster y el informe | [`entregables/`](entregables/) |
| la recomendación con su defensa | [`entregables/recomendacion-defendida.md`](entregables/recomendacion-defendida.md) |
| el código que produce los números | [`pipeline/`](pipeline/), [`tools/`](tools/) |
| la investigación cruda, por tema | [`research/`](research/) |
| por qué decidimos cada cosa | [`00_meta/DECISIONS.md`](00_meta/DECISIONS.md) |
| lo que probamos y descartamos | [`00_meta/CAMINOS_PROBADOS.md`](00_meta/CAMINOS_PROBADOS.md) |

## Cómo correrlo

El pipeline es Python puro y se ejecuta de punta a punta con un comando:

```bash
python pipeline/correr_todo.py
```

Las salidas (`pipeline/salida/`) no están versionadas: se regeneran. Algunos
módulos necesitan ViennaRNA y BLAST+ instalados; los que dependen de datos de
terceros sin licencia abierta publican el generador, no el dato.

Las pruebas:

```bash
python -m pytest pipeline tools -q
```

## Cómo leer las afirmaciones

Todo lo que se afirma en este repositorio lleva una etiqueta que dice de dónde
viene. No es decoración: es la regla con la que trabajamos.

| | |
| --- | --- |
| `[E]` | establecido: consenso en literatura revisada por pares |
| `[R]` | reportado: una o pocas fuentes, preprint, patente, web de empresa |
| `[M]` | medido por nosotros, reproducible desde este repositorio |
| `[H]` | hipótesis del equipo, todavía sin respaldo |
| `[?]` | incierto, o fuentes que se contradicen |

Un resultado computacional propio nunca es `[E]`, por más estándar que sea la
herramienta. Un resultado *in silico* es una hipótesis sobre eficacia, no una
prueba.

## Alcance

Esto es control fitosanitario agrícola construido con información pública. Queda
explícitamente fuera de alcance cualquier trabajo que aumente la virulencia, la
transmisibilidad o el rango de hospedadores de un patógeno, y cualquier diseño
dirigido a dañar especies no objetivo. Toda propuesta de diseño viene con su
contracara de riesgo: efectos fuera de blanco en maíz y en organismos no
objetivo, persistencia ambiental y resistencia.

Las secuencias no publicadas que nos facilitaron no se versionan ni se suben a
servicios de terceros; lo que está acá son coordenadas y resultados derivados.

## Equipo

Joaquín Castaños · Santino Cardelli · Lorenzo Door · Luca Fassio

Ingeniería en Inteligencia Artificial, Universidad de San Andrés.
