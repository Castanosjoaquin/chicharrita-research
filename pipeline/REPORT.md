# Pipeline de priorización: qué calcula, cómo, y qué dio

Cadena reproducible que va del genoma de *Dalbulus maidis* (chicharrita del maíz) a candidatos
de ARN de doble cadena (dsRNA) priorizados, con el criterio escrito y la incertidumbre medida.
Todo corre sobre datos públicos, sin entrenar ningún modelo, y se regenera con un comando.

Este documento es la fuente de los números que citan `plan/` y `tablero/`. Cada resultado dice
con qué script se reproduce, sobre qué conjunto se midió, y con qué marcador de evidencia.

```
python pipeline/correr_todo.py --revisar   # qué hay, qué falta, en qué orden
python pipeline/correr_todo.py             # corre lo que falte, de punta a punta
python pipeline/test_features.py           # 17 pruebas de las features biofísicas
```

---

## 1. Qué problema resuelve, y por qué hizo falta

El genoma de *D. maidis* no tiene anotación pública. La base Gene del NCBI tiene 37 registros de
la especie y los 37 son mitocondriales `[E]`. Sin anotación no se sabe dónde está un gen, y sin
eso no se puede ni evaluar un candidato ni compararlo contra una alternativa.

Anotar el genoma entero es un proyecto en sí mismo. La cadena toma un atajo: alinea proteínas de
referencia de otras especies contra el genoma y se queda con el locus de cada una. No produce una
anotación completa, produce exactamente lo que hace falta, que son los loci de los genes que ya
tienen fenotipo conocido en otro insecto.

El ensamblado de referencia es `ihDalMaid1.1` (972 Mb, nivel cromosoma), que es el mismo sobre el
que están identificados los cuatro candidatos preliminares del laboratorio, de modo que las
coordenadas son comparables sin traducción `[E]`.

---

## 2. El mapeo, y su control

El mapeo completo corre en alrededor de **66 segundos** sobre una notebook con WSL: 18 segundos
para indexar el genoma y 48 para alinear 3.904 proteínas de referencia. De esas, **2.814
encontraron locus (72,1 %)** y el **87,8 %** de los loci no tiene errores de marco de lectura ni
codones de parada internos `[H]`.

**El control de recuperación es el que importa.** Siete proteínas elegidas porque los dos trabajos
publicados sobre la especie ya confirmaron, cada uno por su cuenta, que esos genes existen. Se
recuperaron **las siete, cada una con un solo locus**.

| Proteína | Identidad | Exones |
| --- | ---: | ---: |
| V-ATPasa B (`Vha55`) | 0,978 | 10 |
| V-ATPasa A (`Vha68-1`) | 0,881 | 11 |
| V-ATPasa D (`Vha36-1`) | 0,858 | 6 |
| V-ATPasa E (`Vha26`) | 0,743 | 5 |
| Bicaudal C (`BicC`) | 0,380 | 13 |
| Argonauta-2 (`AGO2`) | 0,354 | 18 |
| Dicer-2 (`Dcr-2`) | 0,297 | 28 |

Los tres de identidad baja son justamente los que se sabe que evolucionan rápido, y aun así el
alineamiento recupera la estructura de exones completa `[H]`.

**Control negativo.** Los loci se reparten por cromosoma en 340, 331, 330, 306, 303, 277, 263,
234, 227 y 186. Siguen el tamaño de cada cromosoma en vez de amontonarse en regiones repetitivas,
que es lo que pasaría si fueran artefactos `[H]`.

**La especie de referencia importa, y está medido.** Mapeando con *Nilaparvata lugens*, del mismo
orden que la chicharrita, en vez de con *Drosophila melanogaster*, las cuatro métricas mejoran a
la vez: recuperación 77,6 % contra 72,1 %, identidad mediana 0,634 contra 0,545, fracción con
identidad ≥ 0,8 del 20,6 % contra 10,9 %, y loci limpios 93,8 % contra 87,8 % `[H]`. La evidencia
hay que ponderarla por distancia filogenética.

> Se reproduce con `hemip_mapear.py` y `resumir_miniprot.py`.

---

## 3. De loci a candidatos: el objetivo de control es un parámetro

El cruce del mapeo con los fenotipos del cribado de *Tribolium castaneum* da **6.295 de 7.416
loci con fenotipo asociado, el 84,9 %** `[H]`, y de ahí salen 494 candidatos de alta confianza.

La decisión de método más importante de esta etapa fue **no cablear el objetivo**. Un ranking que
asume que lo que se busca es matar al insecto descarta los blancos elegidos para bajar la
descendencia, y no por un error de cálculo sino por tener un supuesto escondido en el código.

| Blanco publicado | Elegido por, y para qué | Objetivo «letal» | Objetivo «estéril» |
| --- | --- | ---: | ---: |
| `Vha55` · V-ATPasa B | Texas A&M, para matar | **1 de 4.929** | no entra |
| `Vha36-1` · V-ATPasa D | Texas A&M, para matar | 81 (1,6 %) | 2.050 (58 %) |
| `BicC` · Bicaudal C | Catalano, para esterilizar | 4.385 (último 11 %) | **621 (17,6 %)** |

Cada blanco sube en el objetivo para el que su grupo lo eligió y baja en el otro `[H]`. Con la
lista anterior de 494 candidatos y sin el objetivo como parámetro, `Vha55` salía 16 (top 3 %) y
`BicC` directamente no entraba.

**Esto conecta con los candidatos del laboratorio.** `BicC_Dm` y `ATPaseD_Dm` caen en loci de este
mismo mapeo —cromosomas 3 y 8 del mismo ensamblado—, así que se pueden puntuar contra los otros
7.414 loci sin pedir ningún dato adicional `[H]`.

> Se reproduce con `tabla_unificada.py` y `objetivo_candidatos.py`.

---

## 4. Especificidad: el umbral decide más que el método

Un ARN pequeño silencia un gen cuando coincide con un tramo de ese gen. El chequeo es, entonces,
buscar cada ventana de 21 nucleótidos del candidato en los transcriptomas de los organismos que
no se quieren tocar, por **coincidencia exacta de k-meros en las dos hebras**.

La búsqueda no se hace con alineamiento local. Un umbral de identidad en BLAST no filtra sobre la
consulta completa sino sobre el fragmento que encuentra, de modo que leer sus líneas como
off-targets sobreestima el riesgo por un factor grande; es el motivo por el que las herramientas
del campo usan Bowtie `[E]`.

El catálogo pasó de dos especies a **30**, con una razón escrita por especie dentro del código,
en seis grupos: cultivo, polinizadores, enemigos naturales, hemípteros no objetivo, fauna del
suelo y fauna acuática, más humano y ganado. **25 tienen transcriptoma anotado en RefSeq** y
suman 752 MB.

### 4.1 La curva del umbral

Sobre **10.950 ventanas de 438 genes**, porcentaje que sobrevive al filtro `[H]`:

| Corte | Maíz + abeja | 4 hemípteros | Catálogo de 25 |
| --- | ---: | ---: | ---: |
| 15 nt | 33,5 % | 14,6 % | 0,3 % |
| 16 nt | 72,3 % | 47,1 % | 7,4 % |
| 17 nt | 91,1 % | 70,8 % | 36,2 % |
| 18 nt | 97,3 % | 83,5 % | 66,7 % |
| 19 nt | 99,0 % | 87,9 % | 81,4 % |
| 20 nt | 99,5 % | 90,1 % | 86,8 % |
| 21 nt | 99,8 % | 92,4 % | 90,7 % |

La caída fuerte está entre 17 y 15 nucleótidos; de 18 para arriba la curva es casi plana. Eso
convierte la pregunta al investigador en algo contestable: no hace falta un número exacto, alcanza
con saber si el corte va por arriba o por debajo de 17.

> Sobre un conjunto anterior y más chico, de 1.759 ventanas contra maíz y abeja únicamente, la
> supervivencia a 15 nt era del 41,0 %. No es una discrepancia: es otro conjunto de candidatos.
> El valor a 21 nt coincide exacto en los dos (99,8 %).

### 4.2 Qué especies descartan de verdad

| Especie | Descarta | Solo ella |
| --- | ---: | ---: |
| *Macrosteles quadrilineatus* | 700 | 613 |
| *Homalodisca vitripennis* | 128 | 64 |
| *Nilaparvata lugens* | 65 | 30 |
| *Trichogramma* sp. | 36 | 18 |
| *Bos taurus* | 35 | 12 |
| *Apis mellifera* | 11 | 2 |
| *Zea mays* | 10 | 3 |

*Macrosteles quadrilineatus* descarta **70 veces más que el maíz**, y 613 de sus 700 descartes no
los detecta ninguna otra especie del catálogo: explica el **60 % de los 1.021 descartes totales**.
Maíz y abeja juntos explican **18, el 1,8 %** `[H]`.

El orden sigue el parentesco, no la importancia ecológica. **Cuatro hemípteros** —*Macrosteles
quadrilineatus*, *Homalodisca vitripennis*, *Nilaparvata lugens* y *Acyrthosiphon pisum*—
encuentran **829 de los 1.021 descartes, el 81,2 %, con el 9,6 % del cómputo** del catálogo
completo `[H]`. Sirven para iterar diseño; el catálogo de 25 queda para el dossier regulatorio.

Hay una decisión que no nos corresponde: *Macrosteles quadrilineatus* es a su vez plaga y vector
de fitoplasmas, así que si cuenta como organismo no objetivo es una pregunta para el laboratorio `[?]`.

### 4.3 Ser estricto casi no cuesta candidatos

El filtro completo descarta el **63,8 % de las ventanas** y deja sin ninguna ventana limpia a solo
**2 genes de 438**: `Arf1` y la calmodulina (`Cam`). Es decir, **436 de 438 genes siguen
usables** `[H]`. El argumento de que un filtro duro deja al proyecto sin material no se sostiene.

### 4.4 El maíz aparece igual

Al correr el chequeo sobre blancos publicados, tres ventanas resultaron **idénticas en 21
nucleótidos a la bomba de protones vacuolar del maíz** (`NM_001319777.2`), que es el cultivo que
se quiere proteger `[E]`. Apuntar a lo más esencial y conservado maximiza la letalidad y el riesgo
no objetivo por la misma razón.

El riesgo se guarda **desagregado por especie** —máximo, en cuántas especies pega, cuál es la
peor, y el detalle con el transcripto exacto—, porque un único número agregado iguala casos
distintos: de las 18 ventanas con coincidencia de 21 nucleótidos, 3 pegan en más de un organismo
a la vez, y eso es señal de región conservada entre reinos, no de mala suerte `[H]`.

### 4.5 El hueco declarado

Los enemigos naturales de la chicharrita **no tienen genoma anotado**. Las familias de los
parasitoides de huevos —Mymaridae, Dryinidae, Halictophagidae— tienen cero ensamblados anotados
en RefSeq `[E]`. El parasitismo de huevos de *D. maidis* en el noroeste argentino promedia
**16,4 %, con picos de 56,7 %** en algunos sitios (Luft Albarracin et al. 2017, *Neotropical
Entomology*, PMID 28643143) `[E]`.

Es control biológico que hoy funciona sin costo, y es exactamente el riesgo que no se puede medir.
Las cinco especies sin anotación quedan en el catálogo con su estado explícito. Usando genoma
crudo sin anotar aparecen 49 descartes más, de los cuales **25 no los ve ninguna de las 25
especies con transcriptoma** `[H]`.

> Se reproduce con `no_objetivo_catalogo.py`, `no_objetivo_genomas.py`, `no_objetivo_correr.py`
> y `sirna_offtarget.py`.

---

## 5. La agregación, y cuánto del orden es nuestro

Tres decisiones de método, cada una con su motivo.

**Media geométrica ponderada en lugar de suma ponderada.** La suma deja que un criterio muy bueno
compense a otro cercano a cero; la media geométrica no. Los dos top-10 coinciden en **8 de 10**
sobre el mismo conjunto, y la diferencia es instructiva: una ventana entra tercera por suma
ponderada con una accesibilidad de 0,0388 compensada por una asimetría de 6,4, y con media
geométrica no entra `[H]`.

**Barrido del espacio de pesos.** Sobre las 1.825 ventanas del marco de lectura de la V-ATPasa A,
con **2.000 juegos de pesos** tomados al azar sobre el simplex (Dirichlet uniforme): **124
candidatos distintos** pasaron alguna vez por el top-10, y solo **5** están ahí en más de la
mitad de los casos `[H]`.

| Posición | Frecuencia en top-10 |
| ---: | ---: |
| 1404 | 67,5 % |
| 1340 | 62,3 % |
| 1339 | 54,9 % |
| 1053 | 53,7 % |
| 182 | 52,2 % |

Dicho de otra forma: 119 de esos 124 candidatos llegaron al top-10 por una elección de pesos que
nadie justificó. Lo defendible no es «el mejor», son los cinco que aguantan.

**Descomposición contra la mediana, no contra cero.** La descomposición absoluta destaca siempre
el criterio de mayor peso y no distingue un candidato de otro. Contra la mediana, cada término
dice cuánto separa a ese candidato del candidato típico. Para el primero del ranking: punto de
partida 0,5770, asimetría +0,1591, accesibilidad +0,0976, GC −0,0023, puntaje final 0,8314 `[H]`.
Es una decisión de diseño nuestra y no está validada con usuarios `[?]`.

> Se reproduce con `sirna_enumerar.py`, `motor.py` y `puntuar_candidatos.py`.

---

## 6. Los resultados negativos

Son parte del aporte y se reportan como tales.

**Afinar la región dentro del gen no discrimina.** Elegir la mejor región de 300 pares de bases
dentro de un gen mejora alrededor del **7,2 %** sobre el promedio de ese mismo gen, y contra un
modelo nulo la diferencia **no es significativa en 0 de 20 genes** `[H]`. Lo que discrimina es qué
gen se ataca y el filtro de especificidad.

> **Precisión agregada el 2026-10-20, porque este resultado se usó para adjudicar una
> contradicción y hay que saber qué mide exactamente.** El nulo está en
> `baseline_dsrip/region_nulo_multigen.py` —no en `region_scoring.py`, como decía el registro— y
> es reproducible: con las rutas corregidas da la misma ganancia mediana de 7,2 % y los mismos
> 0 de 20. Dos cosas lo acotan. Primero, el estadístico es la **media del puntaje** de la región,
> no un conteo de ventanas que pasan un umbral, y un promedio sobre 280 valores tiene rango
> dinámico chico por construcción. Segundo, y es lo que importa: el nulo **permuta bloques
> contiguos de 30 ventanas**, de modo que conserva la estructura local y sólo reordena los grupos;
> si las ventanas buenas se agrupan en rachas de menos de 30, este nulo las reproduce y no tiene
> poder para detectarlas. Corrido sobre los cuatro genes de EPILAB con el conteo de eficientes de
> si-Fi21, el mismo nulo de bloques da 0 de 4 significativos y un nulo que baraja la etiqueta
> entre todas las ventanas da **3 de 4**. **El resultado negativo es correcto y es una afirmación
> sobre el nulo tanto como sobre la biología.** Ver `research/ola2/W7_ranking/REPORT.md` §1 y
> `00_meta/DECISIONS.md` D15.

**El techo del dato es bajo.** Dos dsRNA distintos dirigidos al mismo gen, en datos publicados,
correlacionan **0,245** (Spearman) dentro de la misma fase experimental y 0,076 mezclando fases,
sobre 410 genes. El acuerdo binario es del 61 % contra un 52 % esperable por azar `[H]`. Ningún
método puede ser más confiable que la reproducibilidad del dato con el que se lo mide.

**El acuerdo con dsRIP es grueso, no fino.** Ventana a ventana la correlación es 0,62, pero de
los diez mejores candidatos de cada método **ninguno coincide**. El solape de la región elegida
tiene una mediana de **31-57 % sobre 20 genes**, con cuatro genes en los que es cero `[H]`. El
88 % de solape que se obtuvo en el primer gen probado era un caso particular y no se usa.

Leyendo el código de dsRIP aparecen además tres cosas a tener en cuenta si se lo usa como línea de
base: los pesos están fijos y no ajustados con los datos que el propio trabajo reporta, el término
de accesibilidad entra con peso cero, y hay un posible error en el cálculo de la asimetría que
hace que el 83 % de las ventanas reciba la misma bonificación `[?]`.

**El modelo de esencialidad rinde poco, y menos de lo que parecía.** Con validación cruzada
agrupada por gen, el área bajo la curva es **0,604**. Con división al azar daba 0,685, inflado
porque el mismo gen aparece a los dos lados de la partición `[H]`.

**El aprendizaje activo aporta poco.** Reduce alrededor del **25 %** de los ensayos necesarios, no
un factor de ocho como sugería una medición anterior con ocho repeticiones. Y medir primero los
mejores candidatos resulta **peor que medir al azar** (0,541 contra 0,574) `[H]`.

> Se reproduce con `region_scoring.py`, `techo_reproducibilidad.py`, `esencialidad_modelo.py` y
> `que_experimento_primero.py`; la comparación con dsRIP está en `baseline_dsrip/`.

---

## 7. Evidencia de literatura con verificación de citas

Para cada gen candidato, un lector automático busca en literatura abierta y llena una ficha
estructurada con cita textual obligatoria. Un verificador que no es un modelo comprueba que la
cita exista literalmente y que sea coherente con lo que la ficha afirma; el puntaje se agrega con
reglas determinísticas, no con el modelo.

Sobre 21 genes, con dos modelos de distinto tamaño: **6,3 % de citas no verificables** con el
modelo chico contra **10,0 %** con el grande, que además costó **19 veces más** (0,06 contra 1,12
dólares) `[H]`. El modelo caro produjo más citas no verificables que el barato.

Alrededor del **20 % de las citas textuales son literalmente correctas pero no respaldan la
afirmación** que acompañan `[H]`. Una cita real mal atribuida pasa el verificador automático: eso
solo lo ataja una revisión humana, y la línea se presenta con ese límite declarado.

El lector pone a `BicC` cuarto entre 21 genes, cuando el cribado por fenotipo lo tiene en el
puesto 621 `[H]`. Las dos fuentes de evidencia no miden lo mismo.

> Se reproduce con `agente_evidencia.py`.

---

## 8. Cobertura, sesgos y lo que no se sostiene

**La cobertura con doble respaldo es chica.** De los 7.416 loci, solo **62** tienen a la vez
fenotipo de cribado y un blanco de ARN de interferencia ya probado en un hemíptero; 44 de esos son
letales `[H]`. Los otros 7.354 se apoyan en un cribado hecho en *Tribolium castaneum*, que es
Coleoptera, mientras que *D. maidis* es Hemiptera. **La transferencia de fenotipo entre órdenes de
insectos es la incertidumbre dominante del proyecto y ningún experimento computacional la
resuelve** `[?]`.

**Hay un sesgo de catálogo que hay que declarar.** De las 917 proteínas de hemípteros descargadas,
**456 son V-ATPasa**. Concluir «la V-ATPasa es el mejor blanco» a partir de ese catálogo sería
circular: `Vha55` aparece primero por tres caminos que no son independientes entre sí `[?]`.

**Dos ensamblados del vector no son equivalentes.** `ihDalMaid1.1` (972,2 Mb, N50 93,7 Mb) y el
del CIAP-INTA (585,2 Mb, 22.333 contigs, N50 50,5 kb) difieren en 387 Mb. Las coordenadas de uno
no se trasladan al otro sin recalcular `[E]`.

---

## 9. Licencia de los datos derivados

Los fenotipos de silenciamiento provienen de **iBeetle-Base** (Universidad de Gotinga), que se
descarga libremente pero cuyo aviso legal reserva todos los derechos: reproducir ese material en
otra publicación electrónica requiere consentimiento expreso, y no hay licencia abierta declarada
en el sitio `[E]`.

Usarlo para decidir internamente qué validar no tiene problema; publicar una tabla que contenga
sus fenotipos, sí. Por eso **en este repositorio se publica el generador y no la tabla**:
`tabla_unificada.py` está versionado y las salidas que contienen fenotipos quedan fuera del
control de versiones. Quien quiera reproducirlas descarga la fuente original y corre un comando.

El resto del catálogo —loci, coordenadas, identificadores y la justificación por especie del panel
de organismos no objetivo— es propio y no tiene esa restricción.

---

## 10. Qué falta

### 10.1 Resuelto: la ficha por candidato ya no espera ninguna respuesta

Esta sección decía que la **ficha de decisión por candidato** para los cuatro candidatos del
laboratorio estaba pendiente de dos respuestas del investigador —el umbral de identidad del filtro
de especificidad y los pesos de los criterios— y que las dos estaban en `plan/paso-01.html`.

**Las dos dejaron de ser bloqueantes, y por el mismo motivo: un parámetro que no se puede
justificar no se espera, se barre.** La ficha está hecha y vive en
`research/ola2/W7_ranking/REPORT.md` §4.

**Los pesos.** En vez de pedir un vector se barren 2.000 juegos sobre el símplex completo
—reparto entre los dos ejes, pesos por referencia no objetivo y pesos por criterio de riesgo— y se
reporta la frecuencia de cada candidato en cada posición. El resultado es que `MP_MRFV` sale
primero en entre el 76 % y el 100 % de los sorteos y `CP_MRFV` segundo en entre el 76 % y el
100 %, mientras que los dos genes del insecto **no se ordenan entre sí** bajo ningún criterio
defendible. Un vector de pesos del investigador habría producido un orden puntual que no
distinguiría esas dos situaciones `[E]`.

**El umbral de identidad.** Se trató igual, y la medición que lo reemplaza está en
`research/ola2/W7_ranking/azar_por_k.md`: se barrió *k* de 15 a 21 y se comparó lo observado
contra tres nulos. Hay un **cruce entre 17 y 18 nucleótidos** donde lo que se encuentra deja de
ser menos de lo que predice el azar y pasa a ser más —la razón observado/esperado va de 0,97 en 17
a 1,53 en 18 y a 41 en 21— y a 20 y 21 nt una referencia barajada con la misma composición produce
**cero** coincidencias donde la real produce 54 y 46 `[E]`. O sea: por encima de 18 el umbral no
cambia la decisión porque todo lo que aparece es homología, y por debajo de 17 la ensucia porque
casi todo es ruido. **El rango sobre el que el orden no cambia es 18-21**, que es donde ya
estábamos. La pregunta al investigador se vuelve innecesaria: la curva de §4.1 de este mismo
documento ya decía que de 18 para arriba es casi plana, y ahora se sabe por qué.

### 10.2 Lo que sigue abierto de verdad

**La transferencia de fenotipo entre órdenes de insectos**, que §8 declara como la incertidumbre
dominante y que ningún experimento computacional resuelve.

**El panel de no objetivo no cubre lo que más importa.** Los parasitoides de huevos de
*D. maidis* siguen sin ensamblado anotado en RefSeq (§4.5), y el ranking de la ola 2 corre sobre
seis referencias. Un peso sobre una referencia que no existe es cero por omisión, no por
evidencia.

**El ranking ordena calidad de diseño, no valor del blanco.** Dice qué tan bien está elegida una
región dentro de un gen que alguien ya eligió; no dice si ese gen es un buen blanco. Juntar los
cuatro candidatos en un solo orden exigiría una equivalencia entre «ventanas eficientes por
nucleótido» y «cuántos patógenos del complejo corta», y esa equivalencia no la tenemos. Está
registrado como D20 en `00_meta/DECISIONS.md`.

**Las dos regiones alternativas que se recomiendan —`BicC_Dm` 2123-2422 y `ATPaseD_Dm` 72-371— no
están verificadas contra la conservación dentro de *D. maidis*.** Están elegidas por densidad de
eficientes y por ausencia de coincidencia perfecta con no objetivo, pero no sabemos si esos tramos
están conservados entre poblaciones argentinas del vector. Es el mismo problema, con otro
organismo, que el cruce pendiente de `CP_MRFV` contra los aislados de MRFV.
