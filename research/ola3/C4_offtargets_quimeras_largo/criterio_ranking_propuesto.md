# Criterio de ranking propuesto: reglas candidatas, parámetros libres y cuánto del orden es nuestro

Todo este documento es `[H]` salvo donde se indique: son reglas candidatas del equipo, no un
resultado. El pedido del investigador fue explicitar «qué le damos más importancia, por
ejemplo a los off-targets» (`research/checkpoints/checkpoint1.md`, «Qué espera como
entregable»), y el criterio de evaluación que él mismo fijó es el razonamiento, no el acierto.
Por eso lo que sigue separa, con cuidado, tres capas: lo que la evidencia sostiene, lo que es
convención del campo, y lo que elegimos nosotros sin respaldo.

**No se implementa ningún motor nuevo.** `pipeline/motor.py` y `pipeline/puntuar_candidatos.py`
ya resuelven la agregación —media geométrica ponderada, barrido del espacio de pesos,
descomposición contra la mediana (`pipeline/REPORT.md` §5)— y lo que falta no es código sino
decidir qué entra como término y con qué peso. Este documento es esa lista.

---

## 1. Las cuatro reglas candidatas

### Regla 1 — El riesgo se suma por acierto, no se binariza ni se promedia

Una región con un acierto perfecto no es «riesgosa» y otra con doce «riesgosa» igual. Y el
promedio diluye: 12 aciertos en 280 ventanas da un número chico que no dice nada. Proponemos
riesgo = **suma de los pesos de los aciertos**, reportada en crudo y además normalizada por
cada 100 ventanas para poder comparar regiones de 200 y de 300 nt.

El respaldo de que sumar es lo razonable es indirecto pero existe: un solo bloque de 21 nt
idénticos dentro de un ARNdc largo alcanza para matar (`S02`, CL50 de 13,8–20,3 ng/mL), así
que ningún acierto perfecto se puede descartar por aislado; y la herramienta SIREN construye
su puntaje justamente sobre el **efecto acumulado** de los siRNA de un ARNdc largo (`S20`).
`[E]` para el primer hecho, `[R]` para el segundo, `[H]` para la decisión de sumar.

Esto es una diferencia explícita con `pipeline/`, que guarda el riesgo **desagregado por
especie** y usa máximo y conteo de especies (`pipeline/REPORT.md` §4.4). Las dos cosas son
compatibles: el desagregado es para el dossier, la suma ponderada es para ordenar.

### Regla 2 — Cada acierto se pondera por el criterio de coincidencia que lo detectó

Mezclar en un solo número los aciertos de 21/21, los de bloque de 19 nt y los de 21 nt con un
desajuste es el error que W2 documentó en dsRNA-Engineer, donde **los 70 off-targets en maíz y
67 de 67 en abeja salieron de la condición de 16 pb y ninguno de la de 21**, de modo que el
número que la herramienta muestra como riesgo lo decide una condición que ni ella considera
mecánicamente relevante (`research/ola2/W2_herramientas/REPORT.md` §1.4). `[E]`

Pesos propuestos: **21/21 perfecto = 1,0**; **bloque perfecto de 19–20 nt = 0,5**; **21 nt con
un desajuste = 0,25**. El 1,0 es el único con respaldo de bioensayo (`S01`, `S02`, `S03`); los
otros dos son invención nuestra sobre una convención del campo, y la convención misma —que
≥ 19 nt complementarios alcanzan para marcar un off-target potencial, y que se consideran
hasta dos desajustes— está enunciada en `S06` con fundamento mecánico y sin experimento en
insectos detrás. Si el laboratorio prefiere trabajar sólo con 21/21, el parámetro es poner los
otros dos en cero, y conviene saber que eso **borra todo el riesgo en maíz salvo un acierto**
en nuestro conjunto.

### Regla 3 — Cada acierto se pondera por dónde cae

Es el criterio que entregó el investigador, medido en `genoma_vs_transcriptoma.md`. Pesos
propuestos: **exón codificante anotado = 1,0; unión exón-exón del ARNm maduro = 1,0; ARN no
codificante anotado = 0,6; intrón = 0,3; intergénico sin anotación = 0,1.**

Tres aclaraciones que son el aporte de esta investigación al criterio que él propuso. La
primera: el caso existe y es el peor acierto del conjunto —la **única** coincidencia perfecta
de 21 nt de las 920 ventanas contra todo el maíz cae en una región **intergénica**— así que la
regla no es teórica, cambia el número de nuestro candidato más expuesto. La segunda: la
asimetría **va en los dos sentidos**, porque los tres aciertos de `BicC_Dm` sobre un gen
expresado de maíz existen sólo en el ARNm y no en el ADN —los nueve bloques cruzan una unión
exón-exón, verificado contra el GFF—, de modo que **usar el genoma como sustituto del
transcriptoma no es conservador: pierde justamente los aciertos sobre secuencia expresada**.
La tercera: «intergénico» significa «fuera de todo gen anotado», no «no transcrito», y por eso
el peso es 0,1 y no 0. `[E]` las mediciones, `[H]` los pesos.

### Regla 4 — La eficiencia entra como término, no como filtro previo

La alternativa sería filtrar primero por off-targets y ordenar después por eficiencia. La
descartamos por una razón medida en `quimeras.md`: el conteo de ventanas eficientes de una
región **depende del contexto** en que se la calcula —hasta 10 ventanas de diferencia entre la
región sola y la misma región dentro de una quimera, y el efecto llega a 54 nt de la unión—,
así que es un número con ruido de método y no merece la última palabra. Entra como término,
con su peso, y el peso se reporta.

---

## 2. Los parámetros libres, en una lista

Son nueve, y conviene que se vean todos juntos porque la discusión con el laboratorio es sobre
esta lista y no sobre el código:

| Parámetro | Valor propuesto | Estado |
| --- | --- | --- |
| peso del criterio 21/21 | 1,0 | respaldado `[E]` |
| peso del bloque de 19–20 nt | 0,5 | **nuestro** `[H]`, sobre convención `S06` |
| peso del 21 nt con un desajuste | 0,25 | **nuestro** `[H]` |
| peso de exón y de unión exón-exón | 1,0 | respaldado como clase `[E]`, el valor es nuestro |
| peso de ARN no codificante | 0,6 | **nuestro** `[H]` |
| peso de intrón | 0,3 | **nuestro** `[H]` |
| peso de intergénico | 0,1 | **nuestro** `[H]` |
| importancia relativa por organismo | sin fijar | **decisión del laboratorio**, no nuestra |
| peso de la eficiencia frente al riesgo | sin fijar | **nuestro**, y es el que más mueve el orden |

---

## 3. Cuánto del orden depende de esos pesos

La pregunta que el investigador va a hacer —y la que la rúbrica pide contestar— es qué parte
del ranking es un hecho y qué parte es una elección nuestra. Se contesta midiendo, no
argumentando.

Barrido con `scripts/ranking_sensibilidad.py`: cuatro términos (densidad de eficientes, aciertos
en transcriptoma de cultivo, aciertos sólo en genoma de cultivo, aciertos en transcriptoma de
insecto no objetivo), con los conteos medidos, normalizados por 100 ventanas; **20.000 juegos de
pesos tomados al azar sobre el símplex** (Dirichlet uniforme, semilla 20261020), igual que el
barrido que ya había hecho `pipeline/` con 2.000 juegos sobre otro conjunto.

Los vectores de entrada, por 100 ventanas:

| Región | Eficientes | Transcriptoma de maíz | Sólo genoma de maíz | *H. vitripennis* |
| --- | ---: | ---: | ---: | ---: |
| `MP_MRFV` | 11,11 | −1,67 | −1,67 | 0 |
| `CP_MRFV` | 8,89 | 0 | 0 | 0 |
| `BicC_Dm` | 7,86 | −1,07 | −2,86 | −10,71 |
| `ATPaseD_Dm` | 6,79 | 0 | 0 | −2,50 |

Resultado:

| Qué | Valor |
| --- | --- |
| pares cuyo orden **ningún peso no negativo puede invertir** | `CP_MRFV` > `BicC_Dm` y `CP_MRFV` > `ATPaseD_Dm` (dominancia en las cuatro variables) |
| quién queda primero | `CP_MRFV` en el **67,1 %** del espacio de pesos, `MP_MRFV` en el **32,9 %**; nunca los otros dos |
| órdenes completos distintos que aparecen | **5** de los 24 posibles |
| orden más frecuente | `CP_MRFV` > `MP_MRFV` > `ATPaseD_Dm` > `BicC_Dm`, en el 41,3 % |
| par que decide el primer puesto | `MP_MRFV` vs `CP_MRFV`: depende enteramente de cuánto pese la eficiencia contra el riesgo |
| último puesto | `BicC_Dm` en el 98,4 % del espacio |

**La frase que el equipo puede defender:** de los seis pares de candidatos, **dos están
decididos por los datos** y no por nosotros —`CP_MRFV` está por encima de `BicC_Dm` y de
`ATPaseD_Dm` bajo cualquier ponderación no negativa, porque les gana en las cuatro
variables— y **uno, el que define el primer puesto, lo decidimos nosotros**: poner a `MP_MRFV`
primero requiere pesar la eficiencia por encima del riesgo, y poner a `CP_MRFV` primero
requiere lo contrario. El último puesto de `BicC_Dm` es robusto: 98,4 % del espacio. `[H]` la
construcción, `[E]` los conteos que la alimentan.

Y la honestidad obliga a decir algo más: con **cuatro** candidatos y una diferencia de
eficiencia de 11,11 contra 6,79 por cada 100 ventanas, este barrido es un ejercicio de
transparencia, no una demostración estadística. El barrido que sí tiene masa es el de
`pipeline/`, con 1.825 ventanas y 2.000 juegos de pesos, donde **124 candidatos distintos
pasaron alguna vez por el top-10 y sólo 5 estuvieron en más de la mitad de los casos**
(`pipeline/REPORT.md` §5). Esa es la magnitud real del problema de los pesos, y ya está medida
en el repositorio.

---

## 4. Qué cambia, con lo hallado, en la evaluación de las regiones 1–200

Sin rehacer el análisis de W5, tres correcciones de lectura:

**Las regiones no son «1–200» para los cuatro.** Las dos virales son 1–200 y 200–400 y las dos
del insecto son 151–450 y 264–563, de 300 nt (`research/ola2/W5_secuencias_epilab/REPORT.md`).
El largo de las cuatro cae dentro o apenas por encima del rango 150–250 que el laboratorio
declara, y ese rango **no tiene respaldo como techo**: en la propia *Dalbulus maidis* hay
evidencia publicada de silenciamiento con ARNdc de 544 y 578 pb (`S14`). Así que, de las dos
dimensiones del diseño viejo, el largo no es el problema.

**El riesgo en maíz de `BicC_Dm` es menor de lo que parecía, y el de la unión de exones es el
que queda.** De sus 9 aciertos contra maíz con criterio de 19 nt, 8 están sólo en el ADN —uno
intrónico, el resto intergénico, incluida la única coincidencia perfecta— y los 3 que tocan un
gen expresado existen sólo en el ARNm. Con la ponderación propuesta, el riesgo en maíz pasa de
11 unidades a 2,25, y **el 67 % de lo que queda viene de los tres aciertos de unión exón-exón**.
Ese es el riesgo que W5 ya había nombrado bien y el único que la ponderación no diluye. `[H]`

**El orden del ranking no cambia por lo medido acá**, y eso también es un resultado: `CP_MRFV`
sigue siendo la región limpia, `BicC_Dm` sigue siendo la más expuesta —por *H. vitripennis*,
no por maíz— y el par que decide el primer puesto sigue dependiendo de un peso nuestro. Lo que
cambió es que ahora cada número de la tabla tiene una clase de blanco detrás y se puede
discutir con el investigador acierto por acierto.

---

## 5. Lo que este criterio no cubre

No cubre la **dosis**, que en toda la literatura abierta pesa tanto como la secuencia (`S02`,
`S11`); no cubre la **estabilidad**, que en Hemiptera es la restricción mejor documentada —el
ARNdc desnudo desaparece en horas en extracto de áfido (`S12`) y hay nucleasas de intestino
medio en *Apolygus lucorum* (`S13`)—; no cubre los organismos no objetivo **sin genoma ni
transcriptoma**, que para los parasitoides de huevos de *D. maidis* son todos
(`pipeline/REPORT.md` §4.5); y no cubre la **variación del blanco**, que para las dos regiones
virales es el hallazgo más accionable que tiene el proyecto: contra los aislados brasileños de
MRFV, tres cuartas partes de los siRNA de `CP_MRFV` dejan de aparear perfecto
(`research/ola2/W5_secuencias_epilab/REPORT.md` §5.1). Un criterio de ranking que ordene por
especificidad y eficiencia y deje eso afuera estaría ordenando bien una lista equivocada.
