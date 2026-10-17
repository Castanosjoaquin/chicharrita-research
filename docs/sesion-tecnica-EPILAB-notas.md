# Notas de la sesión técnica oficial del Investigathón 2026

**Fuente:** `Sesion_tecnica_Investigathon_60min_v2.pptx.pdf`, 17 diapositivas,
material del organizador. Texto extraído con `pdftotext -layout`. El PDF no está
en el control de versiones por tamaño (`DECISIONS.md`, D6), así que lo que se
use de acá queda transcrito en este archivo.

**Nivel de evidencia:** material institucional del organizador del desafío. Es
primario sobre lo que el desafío pide y sobre qué tiene el laboratorio, y es
`[R]` para las afirmaciones científicas que enuncia sin cita: son resúmenes de
una charla, no el paper. Donde una afirmación de acá importe para una decisión,
hay que rastrear la publicación que la respalda.

## Quién organiza

EPILAB · IFIBYNE (UBA–CONICET). El desafío se titula "La chicharrita del maíz:
un desafío de diseño y validación con ARN". Esto corrige de entrada una
suposición del equipo: el investigador invitado viene del ámbito académico
UBA–CONICET, y la relación con Apolo Biotech —si existe— es una pregunta
separada que investiga R3. No hay que asumir que el pipeline descrito en la
charla sea el de una empresa.

## El sistema a intervenir: son cuatro agentes

La diapositiva del sistema nombra explícitamente **cuatro** patógenos, lo que
resuelve la parte del supuesto S1 que preguntaba por el cuarto agente:

- **MRFV** (virus)
- **MSMV** (virus)
- **Fitoplasma**
- ***Spiroplasma kunkelii***

Más el vector (*Dalbulus maidis*), caracterizado por sus tres funciones
relevantes —alimentación, supervivencia y transmisión—, y el maíz como cultivo a
proteger. La diapositiva remarca que los patógenos son "agentes con biologías
diferentes", que es exactamente la razón por la que no se les puede aplicar la
misma estrategia de silenciamiento.

Lo que la diapositiva **no** dice es qué síntoma causa cada uno ni qué pérdida
se le atribuye por separado: esa parte de S1 sigue abierta y la verifica R1 con
bibliografía.

## Magnitud del problema (campaña 2023/2024)

La diapositiva muestra dos cifras, con el rótulo "Campaña 2023/2024":
**11,5 millones de toneladas** y **2.045 millones de USD**. `[?]` El sentido
exacto de cada cifra no está escrito en la diapositiva: la primera es
compatible con la pérdida de producción atribuida a la epifitia, y la segunda,
con notación decimal española, se lee como 2045 millones de dólares, lo que es
coherente con una pérdida económica a escala nacional pero no está rotulado como
tal. Hay que confirmar ambas con fuente antes de usarlas en la presentación.

## La molécula y el esquema de intervención

ARNdc (dsRNA) diseñado contra **genes esenciales del objetivo**, con un circuito
de cuatro pasos: diseño del ARNdc dirigido a genes esenciales → aplicación por
**pulverización sobre la planta** → ingreso y silenciamiento génico →
inhibición del crecimiento del patógeno.

Que el esquema oficial termine en "inhibición del crecimiento del patógeno" es
llamativo y merece la pregunta directa al investigador, porque la pregunta de si
un mollicute sin pared responde a RNAi es precisamente la que R1 tiene que
contestar con evidencia. Puede ser una simplificación de la diapositiva, o puede
implicar una vía indirecta (silenciar al vector o preparar la defensa de la
planta y con eso frenar al patógeno). No asumir ninguna de las dos.

## Las plataformas de ARN, según el organizador

Una diapositiva ordena el espacio de diseño en cuatro niveles de precisión
creciente, con nomenclatura de maquinaria vegetal (DCL, RDR, AGO):

| Plataforma | Producto | Maquinaria citada | Efecto |
| --- | --- | --- | --- |
| dsRNA largo canónico | pool heterogéneo de siRNA | DCL2/4 → AGO1/2 | PTGS amplio o general |
| dsRNA ingenierizado (*engineered*) | pool enriquecido de siRNA | DCL2/4 → AGO1/2 | PTGS optimizado |
| plataformas de ARN pequeño de precisión: miRNA artificial, syn-tasiRNA, dúplex maduro listo para AGO | dúplex predefinido | DCL2/4, DCL3 (con signo de pregunta en la propia diapositiva), DCL4, RDR6 → AGO1/2 | PTGS predefinido y multiplexado |
| siRNA de 24 nt / RdDM | — | carga en AGO4 | TGS (silenciamiento epigenético transcripcional) |

Esto importa por tres razones. Primero, el eje de "dsRNA largo → dúplex de
precisión" es un eje de diseño explícito del organizador, no una invención
nuestra: moverse hacia la derecha de esa tabla es una forma legítima de aportar.
Segundo, la última columna es silenciamiento transcripcional, una categoría
distinta del resto, con otra persistencia y otras implicancias. Tercero, el
signo de pregunta en "DCL3?" está en la diapositiva original: el propio
organizador marca ahí una incertidumbre.

## Lo que el organizador declara saber y lo que declara no saber

Esta es la diapositiva más valiosa del material, porque define el hueco que el
desafío quiere que llenemos.

| Evidencia publicada | Pregunta abierta |
| --- | --- |
| RNAi experimental en *D. maidis* | ¿Funcionará por una vía de entrega aplicable? |
| Las RNasas limitan la entrega oral del ARN | ¿Qué estrategia resuelve esa barrera? |
| Candidatos preliminares diseñados por el equipo del EPILAB | ¿Cuáles merecen validación y por qué? |

Tres consecuencias directas para nuestro plan:

1. **Hay RNAi experimental publicado en *D. maidis*.** No es un supuesto
   nuestro: el organizador lo pone como evidencia publicada. Encontrar ese
   trabajo y leerlo entero es prioridad alta para R1, porque fija qué genes se
   probaron, por qué vía, con qué dosis y con qué efecto.
2. **El cuello de botella declarado es la entrega, no el diseño.** Las RNasas
   degradan el ARN antes de que llegue. Eso le da peso al eje de formulación y
   modo de aplicación, que es justo lo que R3 tiene que relevar en la industria.
3. **Existen candidatos preliminares del EPILAB y la pregunta es cuáles merecen
   validación y por qué.** Esto es, textualmente, un problema de priorización
   con criterio explicitable: exactamente lo que un equipo de IA puede resolver
   sin laboratorio. Es la señal más fuerte del material sobre dónde conviene
   pararse.

## Cómo se evalúa

La última diapositiva, textual:

> Un equipo no debería ganar por construir la interfaz más vistosa, sino por
> producir la mejor decisión científica posible con el tiempo y los datos
> disponibles.

Es una instrucción de diseño para nosotros. Un dashboard lindo no gana; una
priorización defendible, con su criterio escrito, su evidencia y sus
incertidumbres marcadas, sí. La rúbrica que construye R5 tiene que ser capaz de
sostener eso, y el artefacto que construyamos vale por la decisión que produce,
no por la pantalla.
