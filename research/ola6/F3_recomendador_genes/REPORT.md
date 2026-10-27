# F3 — Recomendador de genes: el orden, con su criterio al lado

**Issue [#27](../../../../issues/27). Ola 6, grupo C. Fecha: 2026-10-27.**
Criterio: [`PREREGISTRO.md`](PREREGISTRO.md), commiteado antes del primer cálculo
(`5880625`). Pesos: `D84`, confirmados por el equipo el 2026-10-27. Escalas de los dos ejes
calculados: [`resultados/escala_fenotipo.md`](resultados/escala_fenotipo.md) y
[`resultados/escala_esencialidad.md`](resultados/escala_esencialidad.md), las dos commiteadas
antes del cálculo que las usa.

> **Expresión en el tejido expuesto: eje faltante.** No existe para ninguno de los 36
> candidatos, y es el eje que más importaría para una vía de entrega oral: si el gen no se
> expresa en el intestino, el ARNdc ingerido no tiene qué silenciar `[H]`. El zip del
> investigador no lo trae y no podía traerlo
> ([verificación](resultados/verificacion_zip_expresion.md)). Está declarado acá, en el
> encabezado, y en una columna de todas las filas de `orden_genes.tsv`.

## 1. Qué se ordenó, y qué quedó afuera

De las **36 filas** del catálogo de `C5`, **25 entraron al orden** y **11 quedaron afuera**
con una etiqueta que dice por qué `[M]`. Las que quedaron afuera están en
[`resultados/fuera_del_orden.tsv`](resultados/fuera_del_orden.tsv): cinco sin fenotipo
publicado, dos con mortalidad que su propia fuente desatribuye del blanco (`HE-04` y `HE-08`),
dos de signo invertido —`CI-08` y `CI-13`, donde silenciar **aumenta** la colonización por el
patógeno—, un potenciador de entrega sin fenotipo propio (`DM-04`, la dsRNasa) y una con un
desenlace que no entra en ninguno de los cuatro mecanismos (`HE-09`, respuesta inmune).

Las dos de signo invertido no llevan puntaje negativo: un puntaje sugeriría que compiten. Esa
decisión coincide con la que `C5` ya había tomado al llamarlos «genes a excluir
explícitamente», y es bueno que coincida, porque se llegó por caminos distintos.

## 2. El orden

Hay **dos cohortes** y no un ranking único, porque de los cinco ejes sólo dos son calculables
y no todos los candidatos tienen los dos. Entre cohortes **no se compara**: es la regla de
`D84` §4.2, y existe para que nadie mejore ni empeore su puesto por un eje que no tiene.

### Cohorte A — ejes 1 y 2 (17 candidatos)

Pesos renormalizados sobre los dos ejes presentes: fenotipo **0,615**, esencialidad **0,385**.

| Puesto | id | gen | eje 1 | eje 2 | puntaje |
| ---: | --- | --- | --- | --- | ---: |
| **1** | `DM-02` | `V-ATPase B` | `F3` | `E3` | **1,0000** |
| **1** | `DM-03` | `V-ATPase D` | `F3` | `E3` | **1,0000** |
| **1** | `DM-05` | `eth` | `F3` | `E3` | **1,0000** |
| 4 | `DM-06` | `burs-alpha` | `F3` | `E2` | 0,8692 |
| 5 | `CI-01` | `Rpn6` (*Scaphoideus titanus*) | `F2` | `E3` | 0,7908 |
| 5 | `CI-02` | `Rpn6` (*Euscelidius variegatus*) | `F2` | `E3` | 0,7908 |
| 5 | `CI-03` | `ATP synthase β` | `F2` | `E3` | 0,7908 |
| 5 | `DE-01` | `V-ATPase B` y `D` (*Peregrinus maidis*) | `F2` | `E3` | 0,7908 |
| 5 | `DM-01` | `BicC` | `F3` | `E1` | 0,7423 |
| 10 | `CI-04`, `CI-06`, `CI-07`, `DE-04`, `HE-02` | — | `F1` | `E3` | 0,5877 |
| 15 | `CI-05` | `muscle actin` | `F1` | `E2` | 0,4569 |
| 16 | `HE-01`, `HE-05` | `Bicaudal-C` | `F1` | `E1` | 0,3300 |

Los puestos 1, 5, 10 y 16 son **empates declarados** por la regla de los 0,05 de `D84` §4.3.
El grupo del puesto 5 tiene cinco miembros y es el caso que la regla existe para manejar:
`DM-01` queda a **0,0485** de los otros cuatro, por debajo del umbral, así que el grupo se
declara en vez de desempatarse. No es que `DM-01` «empate con `CI-01`»; es que la diferencia
entre ellos es más chica que la resolución que este criterio puede sostener, y `DM-01` llega
ahí por un camino distinto —`F3` con `E1` en vez de `F2` con `E3`—, lo que hace la comparación
todavía menos fina de lo que un número sugiere.

El umbral se mide **contra el primero de cada grupo** y no en cadena, para que una sucesión de
diferencias chicas no termine agrupando a dos candidatos realmente separados.

### Cohorte B — sólo el eje 1 (8 candidatos)

| Puesto | id | gen | eje 1 | eje 2 | puntaje |
| ---: | --- | --- | --- | --- | ---: |
| 1 | `DE-02` | `Ruvbl1` | `F2` | `E0` | 0,6600 |
| 2 | `CI-09`, `CI-10`, `CI-11`, `CI-12`, `DE-03`, `DE-05`, `HE-07` | — | `F1` | `E0` | 0,3300 |

## 3. El resultado que importa: el primer puesto no depende de los pesos

La pregunta que el preregistro se comprometió a contestar era en qué rango del peso de
fenotipo cambia el primer puesto. **La respuesta es que no cambia** `[M]`.

Barriendo el peso de fenotipo de 0 a 1 en 2.001 pasos, el líder de la cohorte A es el mismo
trío —`DM-02`, `DM-03`, `DM-05`— en **todo el interior del intervalo**. Sólo cambia en los dos
extremos exactos: con peso 0, es decir ordenando *sólo* por esencialidad, hay un empate de 12
candidatos; con peso 1, ordenando *sólo* por fenotipo, se suman `DM-01` y `DM-06` al empate.
Cualquier combinación que use los dos ejes da el mismo trío.

El motivo es aritmético y conviene decirlo sin adornos: esos tres están en el **máximo de los
dos ejes** a la vez, y cualquier promedio ponderado de dos máximos es el máximo. No es un
hallazgo biológico; es la forma del dato. Pero tiene una consecuencia práctica fuerte: **la
discusión de pesos, que era la decisión más delicada de esta línea, no afecta la cabeza del
orden.** Si alguien quiere discutir el criterio, el lugar donde la discusión cambiaría algo es
el medio de la tabla, no el podio.

## 4. Las cuatro cosas que hay que saber antes de usar este orden

**La cohorte B no es un grupo biológico: es el grupo de las fuentes que no se pudieron abrir.**
Los ocho candidatos de la cohorte B están ahí porque su vía quedó en `E0`, y `E0` significa
«sin fuente abierta», no «no esencial». Dos casos son claros: `DE-02` (`Ruvbl1`) quedó en `E0`
porque la ficha de FlyBase de `pontin` se descargó vacía, y hay indicios de letalidad
embrionaria en ratón y de nulo no viable en levadura que lo dejarían en `E2`; `DE-05` (`XPO1`)
quedó en `E0` porque Collier y colaboradores 2000 no se abrió, y según la búsqueda describe
alelos letales recesivos que lo dejarían en `E3`. Es decir que **el límite entre las dos
cohortes depende hoy de qué páginas cargaron**, y eso es un artefacto de método que hay que
arreglar, no una propiedad de los genes. Está anotado como entrada 61 de la ola 6, con las
cinco fuentes y el motivo de cada una.

**El criterio premia la evidencia en la propia especie, y los tres primeros son los tres genes
de *Dalbulus maidis*.** El nivel `F3` del eje 1 exige que el fenotipo se haya medido en
*D. maidis*, y las cinco filas que cumplen eso son justamente las del gen que el proyecto ya
viene trabajando. Así que el orden **reproduce lo que el equipo ya estaba haciendo**, y eso se
puede leer de dos maneras. La lectura favorable es que un criterio declarado antes, construido
sobre la tabla del plan y no sobre nuestras preferencias, llega a las mismas moléculas: es una
confirmación independiente de que el foco del proyecto está bien puesto `[H]`. La lectura
escéptica es que un eje que premia «medido en nuestra especie» va a premiar siempre a los
genes sobre los que nuestra especie tiene mediciones, que son los que ya elegimos. **Las dos
lecturas son válidas al mismo tiempo** y el orden no distingue entre ellas; decir sólo la
primera sería vender el resultado.

**Dos de los cinco ejes están declarados faltantes, y uno de ellos tiene dos motivos.** El eje
de off-target no se puede calcular por falta de `work/sifi_v2/` **y** porque los conteos que el
catálogo sí trae, para 8 de las 36 filas, están contra **otro panel**: cinco referencias, con
*Macrosteles quadrilineatus* adentro —que para un gen del insecto es señal de conservación y no
de riesgo— y sin *Harmonia axyridis* ni *Folsomia candida*. Omitir dos organismos no objetivo
da un conteo **optimista**. Esos números se publican igual, en columnas cuyo encabezado dice
`panelC5_NO_es_el_de_seis__…`, y **ningún candidato se ordena por ellos**. El eje de
conservación entre poblaciones falta porque no están los tres TSA en esta máquina.

**El eje 2 de `DM-05`, que es uno de los tres primeros, se apoya en una fuente secundaria.** El
98 % de mortalidad del nulo de `eth` sale de la ficha de InteractiveFly, que se leyó; la
primaria que esa ficha cita, Park y colaboradores 2002 en *Development*, devolvió HTTP 403 y
**no se abrió**. La columna `eje2_fuente_primaria_abierta` lo dice fila por fila, y es el único
caso del eje.

## 5. Lo que esta línea no hace

No elige el gen: ordena y mide, y la elección es del equipo y del investigador, igual que en
`M5` y `M7`. No afirma eficacia: toda la cadena hereda el criterio de eficiencia de si-Fi21,
que no está validado en hemípteros —ρ = +0,142, IC95 [−0,247, +0,492], n = 29 `[M]`— así que
un orden in silico es una hipótesis sobre eficacia y no una prueba. Y no toca ninguna cifra
publicada: no modifica `ranking.py`, `ranking_v2.py` ni `research/ola4/M6_alertas/`, y todas
sus salidas son archivos nuevos.

## 6. Sobre «matar o esterilizar», que es lo que esta línea tenía que volver decidible

El issue decía que `F3` es lo que volvería decidible esa pregunta. Lo volvió **parcialmente**,
y conviene ser preciso sobre cuánto.

Lo que ahora sí se puede afirmar: el orden **tiene** eje de fenotipo, que antes no tenía, y con
él se puede ver que de los 25 ordenados hay 16 con letalidad, 13 con reproducción, 4 con
transmisión y **1 con movilidad** `[M]`. Y que los tres primeros de la cohorte A son dos de
letalidad pura (`DM-02` con movilidad además, `DM-03`, `DM-05`) mientras que el mejor candidato
de reproducción, `DM-01` (`BicC`), queda en el grupo del puesto 5 —por `E1`, porque su vía
esteriliza y no mata—.

Lo que **no** se puede afirmar: que el orden cambie según el objetivo. Para eso habría que
ordenar dos veces con dos objetivos distintos, y el criterio de `D84` no tiene un parámetro de
objetivo: tiene un eje de fenotipo que no distingue entre «quiero matar» y «quiero
esterilizar». La diferencia entre `DM-05` (puesto 1, letalidad) y `DM-01` (puesto 5,
reproducción) **no sale de un objetivo**, sale del nivel de esencialidad de sus vías. `[H]` Lo
que haría falta es un segundo orden con el eje de fenotipo filtrado por mecanismo en vez de
promediado, y es una línea nueva, no un parámetro de ésta.

## 7. Cómo reproducirlo

```
python research/ola6/F3_recomendador_genes/scripts/01_eje_fenotipo.py
python research/ola6/F3_recomendador_genes/scripts/02_eje_esencialidad.py
python research/ola6/F3_recomendador_genes/scripts/03_orden.py
```

Los tres son deterministas y no leen nada de `work/`: los dos ejes calculados salen de
material versionado. El primero **falla** si alguna asignación de mecanismo cita una frase que
no está textual en el catálogo, y el segundo **falla** si alguna vía con puntaje no trae cita,
especie y número, o si alguna se puntuara con evidencia del propio catálogo (regla 3 de la
escala, la que impide que el eje 2 sea el eje 1 con otro nombre).

**Entorno declarado**, como en `R8`: máquina de Santino, Windows 11 Pro for Workstations
10.0.26300, Python 3.13.15, numpy 2.5.4. Esta línea **no** usa ViennaRNA, Biopython,
`ahocorasick` ni alineador. `work/` presente pero sin `sifi_v2`, y `work/W5/ref/` con sólo la
referencia humana `[M]`. El detalle de la corrida está en
[`resultados/meta.json`](resultados/meta.json).
