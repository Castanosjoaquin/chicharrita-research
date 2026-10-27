# Eje 2, esencialidad: la escala, declarada antes de leer la literatura

**2026-10-27, antes de abrir ninguna fuente nueva.** El `PREREGISTRO.md` §3 define el eje 2
—«sale de `funcion` y `familia_proteina`, contra literatura»— pero no fija su escala. Esto la
fija. Se commitea antes de la primera búsqueda por la misma razón que el preregistro se
commiteó antes del primer cálculo: una escala definida después de leer se acomoda a lo que se
encontró.

Decidido con el usuario el 2026-10-27: el eje se llena **abriendo literatura por vía**, no por
gen. El repositorio tiene 12 papers fichados y 11 abiertos (`research/ola2/W1_papers/papers.json`)
y ninguno es un tamizaje de esencialidad, así que la evidencia de este eje hay que traerla.

## La escala

| Nivel | Puntaje | Qué hace falta para asignarlo |
| --- | ---: | --- |
| `E3` | **1,00** | Pérdida de función **letal demostrada en un insecto**, por RNAi o por mutante, en esta vía, con fuente abierta. |
| `E2` | **0,66** | Vía de función celular central cuya esencialidad está establecida, con fuente abierta, pero **sin** letalidad por pérdida de función reportada en un insecto. |
| `E1` | **0,33** | Función condicional: reproducción, cutícula, inmunidad, conducta o interacción con el patógeno. La pérdida afecta la aptitud pero **no es letal por sí misma**. |
| `E0` | **sin puntaje** | No hay fuente abierta que lo sostenga. Se **declara** «sin fuente abierta», no se puntúa con cero. |

## Las cinco reglas que la vuelven auditable

1. **La fuente tiene que estar abierta.** Un título en una lista de resultados de búsqueda no
   es una fuente abierta, y un resumen que no se leyó tampoco. Es `CLAUDE.md` y acá es
   especialmente fácil de violar, porque la esencialidad de la V-ATPasa o del proteasoma es
   «lo que todo el mundo sabe»: justamente por eso hay que abrirla.

2. **El puntaje es de la vía, no del gen, y todos los candidatos de la vía lo heredan.** La
   salida nombra la vía y la fuente al lado del puntaje, de modo que se vea cuántos
   candidatos descansan sobre la misma lectura.

3. **La regla que impide que este eje sea el de fenotipo disfrazado.** Una vía **no** puede
   puntuarse con evidencia que venga del propio catálogo de `C5` ni de las filas de fenotipo
   del eje 1. Si la única evidencia de que la vía es esencial es que silenciarla mató insectos
   en una de las 36 filas, entonces el eje 2 estaría midiendo el eje 1 otra vez, con otro
   nombre y sumando 0,25 más de peso al mismo dato. La evidencia de este eje tiene que ser
   **independiente** del catálogo: función celular, tamizajes de esencialidad, mutantes,
   trabajos sobre la vía en otros organismos.

4. **La especie donde se demostró se registra, y no se exige que sea la nuestra.** Un `E3`
   demostrado en *Tribolium castaneum* vale como `E3`, pero la salida dice en qué especie fue.
   La extrapolación entre especies es lo que este eje aporta y también su límite.

5. **Un nivel `E0` no baja el puesto de nadie.** Un candidato cuya vía quedó en `E0` sale a la
   cohorte de los que no tienen el eje 2, por la regla de cohortes de `D87`: no se compara con
   los que sí lo tienen.

## Las 16 vías a cubrir, y cuántos candidatos dependen de cada una

De los 25 candidatos con mecanismo de fenotipo:

| Vía | n | candidatos |
| --- | ---: | --- |
| V-ATPasa (bomba de protones vacuolar) | 4 | `DM-02`, `DM-03`, `DE-01`, `HE-02` |
| Fosforilación oxidativa (ATP sintasa β) | 3 | `CI-03`, `CI-04`, `CI-06` |
| Oogénesis (Bicaudal-C) | 3 | `DM-01`, `HE-01`, `HE-05` |
| Proteasoma 26S (tapa, Rpn6) | 2 | `CI-01`, `CI-02` |
| Esclerotización (lacasa-2) | 2 | `CI-11`, `CI-12` |
| Citoesqueleto muscular (actina) | 1 | `CI-05` |
| Contracción muscular (troponina C) | 1 | `CI-10` |
| Ecdisis (hormona ETH) | 1 | `DM-05` |
| Esclerotización tras la muda (bursicón α) | 1 | `DM-06` |
| Remodelado de cromatina (RuvBL1) | 1 | `DE-02` |
| Determinación sexual (transformer-2) | 1 | `DE-03` |
| Transporte dependiente de ATP (ABC) | 1 | `DE-04` |
| Exporte núcleo-citoplasma (exportina 1) | 1 | `DE-05` |
| Endocitosis mediada por clatrina | 1 | `CI-07` |
| Proteínas de intestino (natterina, legumaína) | 1 | `CI-09` |
| Proteína salival de la ingestión de floema | 1 | `HE-07` |

Las cuatro primeras vías cubren 12 de los 25 candidatos, así que ahí es donde la calidad de la
lectura más pesa. Cada fuente que se abra entra a
`research/ola2/W1_papers/papers.json` y a `00_meta/FUENTES.md`, incluso si termina descartada
por no sostener nada: saber qué se descartó es parte del resultado (`CLAUDE.md`).
