# Qué hicimos con lo que pidieron, y qué agregamos

**Cómo se lee según la guía.** La página de siete casillas del checkpoint 2 es el resumen: [`checkpoint2-una-pagina.html`](checkpoint2-una-pagina.html), con su fuente en [`checkpoint2-una-pagina.md`](checkpoint2-una-pagina.md). Sigue la guía del checkpoint 2: pregunta, hipótesis, evidencia, avance propio, alternativas, validación y dudas abiertas. Este documento es el detalle de esas casillas, y sus cifras están verificadas contra los archivos de origen.

**Para quién es esto.** Para el investigador del EPILAB que nos orientó en el checkpoint. Se lee en unos diez minutos, o en cinco si se lee sólo la parte A y las preguntas de la parte D, y termina en siete preguntas que sólo él puede contestar. Cada número tiene detrás un informe del repositorio con su fuente; acá van los resultados, no la demostración.

**Cómo leerlo.** La parte A es **lo que pidieron**, punto por punto. La parte B es **lo que agregamos por iniciativa propia**, y está separada a propósito para que se vea qué fue pedido y qué no. La parte C dice lo que **no sabemos**, y la D son las preguntas.

**Una aclaración sobre los números.** No tenemos RNAplfold 2.1.5 (el que instala si-Fi21 es un ejecutable de Windows), así que todo lo que corrimos nosotros usa ViennaRNA 2.7.2. Los conteos absolutos no son comparables con los del programa original; las comparaciones dentro de cada informe sí valen, porque usan el mismo motor de los dos lados.

## En cinco líneas

Los cuatro diseños de la planilla se auditaron, no se reprodujeron, porque no hay un resultado validado que reproducir. El ranking se presenta en **dos listas, una por mecanismo** (D38): en el virus dentro de la planta, `MP_MRFV` va antes que `CP_MRFV`; en el insecto, con las regiones recomendadas, `BicC_Dm` va primero en escala absoluta y `ATPaseD_Dm` último, y `eth` y `burs-α` no tienen orden firme entre sí. Las dos listas no se comparan: juntarlas pondría arriba a los virales por un artefacto. Lo más accionable es mover la región dentro del gen en `BicC_Dm`, por el veto contra un cicadélido no objetivo y por conservación. La crítica más fuerte es que **la accesibilidad, una de las tres condiciones de si-Fi21, no mostró valor predictivo en los datos independientes que pudimos revisar**. Y intentamos validar el criterio contra el único conjunto abierto que existe en insectos: el dato **no alcanza** ni para validarlo ni para refutarlo.

## A. Lo que pidieron

| Pedido | Qué entregamos | Resultado, en una línea |
| --- | --- | --- |
| 1. Entender si-Fi21 | `entregables/que-significa-eficiente.md` y una reimplementación verificada contra el original | «Eficiente» es un **booleano por ventana de 21 nt**, no un puntaje: tres condiciones combinadas con un `and`. De los seis valores que lo deciden, **dos no tienen fuente primaria** (la brecha de 1,00 kcal/mol y los 22 °C), y el 0,1 de accesibilidad es convención. `[M]` |
| 2. Benchmarking de las tres herramientas | `research/ola2/W7_ranking/benchmark_tres_herramientas.md` | si-Fi21 mide eficiencia y no especificidad; BLAST mide similitud y no eficiencia; dsRNA-Engineer dice medir las dos, y corrió sobre los dos genes virales y no sobre los del insecto. Dos implementaciones independientes de off-target **coinciden exactamente en las 20 celdas** de bloque perfecto. `[M]` |
| 3. Un ranking con el criterio explícito | `research/ola2/W7_ranking/REPORT.md` y `research/ola3/C7_ranking_v2/` | Dos listas, una por mecanismo (D38). **Virus en la planta:** `MP_MRFV` > `CP_MRFV` en escala absoluta, en al menos 78,5 % de 2.000 juegos de pesos. **Insecto, con las regiones recomendadas:** `BicC_Dm` primero en escala absoluta (76 a 100 % de los sorteos, según largo y combinación), `ATPaseD_Dm` último, `BicC_Dm` antes que `eth` sólo a 21 nt, y `eth` antes que `burs-α` en escala absoluta pero sin orden firme en min-max. Con las regiones de la planilla, decir «`BicC_Dm` es tercero» sería reportar una elección de pesos. `[M]` |
| 4. Evaluación de las regiones elegidas | W7 §2.2 y §2.3, revisado en `research/ola3/C8_conservacion/` | En `BicC_Dm` la región elegida está en el percentil 44 de su propio gen y **22 de sus 300 ventanas coinciden perfecto en 21 nt con *Homalodisca vitripennis***. La región recomendada pasa a **922-1221** (36 ventanas que pasan el filtro, 32 idénticas en los tres transcriptomas públicos). La de `ATPaseD_Dm` (72-371) se mantiene. `[M]` |
| 5. Crítica de las herramientas | `entregables/critica-herramientas.md` | La condición de accesibilidad no mostró valor predictivo: razón de probabilidades **1,00 [0,89–1,12]** sobre 300 siRNA humanos, y cociente de riesgo **0,9994 (P = 0,853)** en *Tribolium castaneum* con 29 siRNA. Afirmamos algo acotado: usarla como filtro booleano con umbral fijo no está justificado con la evidencia abierta que revisamos. `[M]` |

Los dos opcionales del checkpoint también están: la comparación de 21 contra 22 nt, y el catálogo de genes blanco con evidencia en cicadélidos, que sumó `eth` y `burs-alpha` (con evidencia funcional en *D. maidis*) al ranking.

## B. Lo que agregamos por iniciativa propia

Nada de esto fue pedido. Lo hicimos porque la crítica del punto 5 deja una pregunta incómoda: si el umbral no tiene fuente, ¿cuánto depende nuestra recomendación de él?

**B.1. Cuánto depende la recomendación del umbral.** Barrimos los dos umbrales sin fuente primaria sobre una grilla de 546 puntos por modo (ViennaRNA 2.7.2, modos fiel y corregido). **El candidato superior es robusto** —`MP_MRFV` queda primero en el 99,1 % de la grilla en modo fiel y en el 98,2 % en el corregido— pero **la región exacta de 200 nt no lo es**: coincide con la de defecto en apenas el 11,7 % y el 25,8 % de los puntos, y hay puntos con solapamiento cero. El par `ATPaseD_Dm` contra `CP_MRFV` es un empate práctico, que se invierte en casi la mitad de la grilla. Esto mide fragilidad de la recomendación, **no** si el umbral es correcto: eso exigiría etiquetas de eficacia que no existen. Lo defendible es entregar una región candidata y no un sitio `[H]`. Las cifras de este párrafo son `[M]`. Informe: `research/ola3/C9_sensibilidad_umbral/REPORT.md`.

**Una conciliación que hay que decir.** El tablero de límites reporta que elegir la mejor región de 300 pb dentro de un gen mejora cerca de un 7,2 % sobre el promedio de ese gen, y que no es significativo en 0 de 20 genes. Eso no contradice mover la región de `BicC_Dm`. El estadístico de ese nulo es la media de un puntaje biofísico, no el conteo de ventanas que pasan el filtro, y el nulo permuta bloques de 30 ventanas: conserva las rachas cortas de ventanas buenas y, por eso, no tiene poder para detectarlas. La recomendación de `BicC_Dm` se apoya en el veto por *Homalodisca vitripennis* y en la conservación entre transcriptomas, no en ese 7,2 %. `[M]` `[H]` Informe: `research/ola2/W7_ranking/REPORT.md` §1.1.

**B.2. Una corrección a cómo presentamos el barrido de pesos.** El gráfico B.3 de nuestro ranking se leía como robustez del orden y es sensibilidad a la escala: con la otra escala (min-max) el orden modal de las regiones propuestas cae del 98,7 % al 33,7 % y `MP_MRFV` pasa de primero a tercero. Además la limpieza casi no tiene palanca sobre el orden (varía un factor 1,015–1,064 entre candidatos, contra 2,38–2,50 de la eficacia). La afirmación vieja quedó tachada en el informe, con la corrección al lado. `[M]`

**B.3. Una validación retrospectiva, pre-registrada.** Una aclaración antes de los números: los dos conjuntos de datos que usamos **ya estaban citados en nuestra crítica de herramientas** (son los 29 siRNA y los 28 ARNdc de Cedden *et al.* 2025), así que esto es un reanálisis de una línea de evidencia ya contada, con otro predictor, y no una línea nueva. Escribimos **antes de mirar los datos** qué conjunto usaríamos, qué estadístico, qué contaría como éxito y qué como fracaso, y la corrimos. Son los 31 siRNA de *Tribolium* de Cedden *et al.* 2025 con mortalidad medida, de los cuales 29 se pudieron ubicar en el transcrito. **Resultado: no concluyente.** La correlación de rangos entre el booleano de si-Fi21 y el desenlace es **ρ = +0,142 con intervalo de confianza del 95 % de [−0,247, +0,492]**, que contiene tanto el cero como el valor que se vería si el criterio fuera bueno. Con los 28 ARNdc del mismo trabajo (confirmatorio) da +0,236 [−0,161, +0,568]. `[M]`

![Resultados de la validación retrospectiva](validacion_retrospectiva.png)

La curva de precisión contra el umbral de accesibilidad cuenta lo mismo de otra forma. De los 29 siRNA, **24 son positivos**, de modo que decir «todos son eficientes» ya acierta el 82,8 %. En el umbral por defecto (0,1) el filtro marca 5, acierta 4, y da precisión 0,800 con una cobertura del 17 %: por debajo de esa base. Sólo la supera en el umbral más bajo del barrido (0,875 en 0,02), con un intervalo [0,529, 0,978] que contiene a la propia base. `[M]`

Dos salvedades que hay que decir junto con esto. **No es evidencia independiente de lo ya publicado:** los dos conjuntos son los mismos que ya citamos en la crítica de herramientas, y los autores analizaron sus propios descriptores sobre ellos. Y **un resultado nulo no refuta el criterio**: con n = 29 y la fiabilidad medida del desenlace (dos ARNdc contra el mismo gen correlacionan 0,245), un criterio bueno y uno inútil producen intervalos casi idénticos. Lo que quedó medido, y ya no sólo argumentado, es que **con los datos abiertos que existen no se puede distinguir entre los dos**. Informe: `research/ola3/C9_sensibilidad_umbral/RESULTADOS_validacion_retrospectiva.md`.

**B.4. Una búsqueda de datos de ARN pequeños virales.** Si el hospedador corta el virus en ciertos puntos, ese mapa sería una observación de qué ventanas se procesan de verdad. Para el *Maize rayado fino virus* y para *D. maidis* **no existen** esos datos: cero registros en SRA y GEO. Los dos sustitutos abiertos —*Mal de Río Cuarto virus* en trigo y su delfácido, y *Rice dwarf virus* en arroz y su cicadélido— muestran que los puntos calientes **no se correlacionan con la estructura del ARN** (probado con RNAfold) y **dependen del hospedador**. Por eso no los usamos para elegir regiones. `[M]` Informe: `research/ola3/C10_vsirna_virus/REPORT.md`.

## C. Lo que no sabemos

**La tensión central de la propuesta.** El eje que ordena el ranking es la eficacia, porque la limpieza casi no tiene palanca; y es justamente el eje cuyo vínculo con la eficacia medida no está demostrado. El eje que sí es un hecho de alineamiento —que una ventana exista o no en un transcriptoma no es una predicción— casi no mueve el orden. No invalida la propuesta, porque nunca afirmó predecir eficacia y declara su incertidumbre en cada número, pero preferimos plantearla nosotros. `[H]`

**Lo que no pudimos cerrar.** `MP_MRFV`, el primero del ranking, no se puede evaluar por conservación: sólo 4 de 71 registros de GenBank cubren su región y dos son la referencia. No hay un catálogo de genes nucleares anotados de *D. maidis*, así que trabajamos con tres transcriptomas. La entrega oral es mucho más débil que la inyección en los datos que revisamos, y no encontramos evidencia de que el ARN exógeno entre al floema. Y todo el trabajo de validación es *Tribolium*, un coleóptero: no hay validación en hemípteros. `[M]` Las cifras son nuestras; la entrega oral y el floema son lectura de las fuentes que revisamos `[R]`.

## D. Las siete preguntas

Van en orden de cuánto cambian el resultado. Las cuatro primeras se pueden contestar de memoria.

**1. ¿En qué modo corriste si-Fi21 y con qué umbral de estabilidad de extremos?** Tu planilla declara 114, 35, 199 y 33 eficientes. Si-Fi21 original da 133, 32, 212 y 42, y la reescritura del grupo da 138, 40, 218 y 35. Barrimos 22.176 configuraciones y ninguna da los cuatro valores; lo más cercano es subir el umbral de extremos de 1,0 a 1,75 (117, 35, 199 y 32). ¿Fue modo diseño o alta sensibilidad, y esos números son «eficientes» o «eficientes sin off-targets»?

**2. ¿La región 1–200 la elegiste por off-targets o por densidad de siRNA?** Lo medimos: en uno de los genes la región elegida tiene menos de la mitad de ventanas que pasan el filtro que la mejor región del mismo largo. Si fue por off-targets, el criterio se sostiene y lo decimos así.

**3. ¿Qué transcriptoma de *D. maidis* usan, y nos lo podrían pasar?** De eso depende que las posiciones de la planilla sean reproducibles con datos públicos, y que podamos medir conservación de `eth` y `burs-alpha`. La búsqueda local (C11, 2026-10-21) encuentra secuencia de ambos en el transcriptoma de Pergamino (GHCC01), con identidad completa en el tramo alineado; los hits de Ohio (GITV01) no están verificados. Lo que falta es verificar que sean el mismo transcrito y no un parálogo. `[M]`

**4. ¿Qué pesos le darías a cada criterio, y qué peso tiene un hemíptero no objetivo frente al maíz?** El segundo es el único parámetro que no nos corresponde fijar: decide si uno de los candidatos del insecto queda último.

**5. ¿Les interesa matar o esterilizar?** El ranking ordena distinto según el objetivo, así que presentamos los dos ejes sin elegir uno (D40). Si el objetivo es cortar transmisión, esterilizar puede no alcanzar dentro de la ventana de latencia.

**6. ¿De dónde sale el rango de 150 a 250 nt?** No está en el artículo, en el manual ni en el código. Lo que encontramos sostiene un piso de unos 60 pb. Lo tratamos como convención razonable, no como conclusión.

**7. Dos sobre BLAST.** ¿Usan el BLAST web con sus valores por defecto para verificar off-targets? Contra algo del tamaño de un genoma el resultado es cero por construcción: `megablast` con palabra 28 no puede sembrar una consulta de 21 nt. Y «HCP»: entendemos que querías decir «HSP», que es la unidad de resultado y no un parámetro; ¿te referías a `-max_hsps`, al E-value o al porcentaje de identidad?

---

Cualquiera de estas que puedas contestar nos sirve; no hace falta que sean todas ni que sea rápido.

## Dónde está cada cosa

La portada del repositorio es `index.html`, y `estado.html` dice qué está hecho y qué falta. Los dos documentos de entregable son `entregables/que-significa-eficiente.md` y `entregables/critica-herramientas.md`. El ranking está en `research/ola2/W7_ranking/` y `research/ola3/C7_ranking_v2/`; la conservación en `research/ola3/C8_conservacion/`; la sensibilidad y la validación en `research/ola3/C9_sensibilidad_umbral/`; y la búsqueda de ARN pequeños virales en `research/ola3/C10_vsirna_virus/`.

Lo del checkpoint 2 está en `entregables/checkpoint2-una-pagina.md` (y su `.html`) y en `docs/plan_checkpoint2/`. Las salidas de cada fase están en `docs/plan_checkpoint2/salidas/`: `F1_decision_ranking.md` (ranking y etiquetas), `F2_entrega_y_mecanismo.md` (entrega y mecanismo, con el estado de apertura de cada fuente), `F3_hipotesis_alternativas_validacion.md` (hipótesis, alternativas y esbozo de validación) y `PENDIENTES_FASES_1_A_3.md` (lo que queda por hacer, y por quién).
