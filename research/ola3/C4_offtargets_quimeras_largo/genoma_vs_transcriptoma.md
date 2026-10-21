# Q2 — Un off-target que cae en el genoma y no en el transcriptoma

El investigador entregó este criterio como parámetro de ranking: un acierto que cae en el
genoma pero no en el transcriptoma —en una región que no se expresa— es menos grave que uno
que cae sobre un gen activo; *«ese off-target vos podés marcarlo como, bueno, es off-target,
pero no tanto»* (`research/checkpoints/checkpoint1.md`, apartado «Genoma vs. transcriptoma
como criterio de ranking»). `[R]`

Este documento hace tres cosas: revisa qué hace el campo con esa distinción, la mide en
nuestros propios datos —y encuentra que el asunto es simétrico, no unidireccional— y propone
una ponderación explícita con su prueba de sensibilidad.

---

## 1. Qué hace el campo con la distinción

**Las herramientas de diseño de ARNdc resuelven esto por omisión: buscan contra
transcriptomas.** si-Fi21 parte el disparador en x-meros y los busca con Bowtie contra una
base de «ARNm o ADNc» (`S08`); dsRNAmax descarta todo k-mero de 21 nt con coincidencia
contigua en las secuencias no objetivo, que entran como transcriptomas o incluso como datos
metagenómicos (`S07`); SIREN acepta transcriptomas definidos por el usuario y suma el riesgo
de todos los siRNA (`S20`); y la revisión de métodos de 2026 describe que los programas del
campo —dsRIP, dsRNAmax, dsRNAEngineer, dsOMG— convergen en el mismo circuito: trocear la
entrada en siRNA y buscarlos «contra los transcriptomas de los organismos no objetivo
seleccionados» (`S06`). `[E]` Nuestro propio `pipeline/` hace lo mismo: el catálogo de 30
especies se tamiza contra los 25 transcriptomas RefSeq disponibles (`pipeline/REPORT.md` §4).

**El único trabajo que encontramos que mide explícitamente dónde cae el acierto es
`S05`.** Bulgarella et al. 2025 tamizaron un ARNdc comercial de 402 pb contra 39 especies y
dejaron escrito el argumento y su límite: como la eficacia del siRNA depende en última
instancia de la homología a nivel de ARN mensajero —porque exones distantes terminan
empalmados en el ARNm maduro—, comparar contra el transcriptoma «es preferible»; pero como
no había transcriptoma para todas las especies, usaron también los genomas, y cuando un
genoma daba un acierto de 21 nt clasificaron su ubicación como **exón, intrón o unión
exón-intrón**. Su resultado: todos los aciertos de 21 nt en otros organismos provenían de la
secuencia codificante de un homólogo de calmodulina, el mismo gen blanco. `[E]`

No encontramos ningún trabajo experimental que mida si un ARNdc con coincidencia perfecta
contra un intrón o contra una región intergénica produce o no algún efecto. Es un vacío
documentado. Lo que sí es consenso mecánico es dónde actúa el RISC: el silenciamiento que
describen todas estas herramientas es post-transcripcional, sobre ARN mensajero
citoplasmático (`S08`, `S06`), y nuestra propia R1 ya documentó que existe además una rama
transcripcional en otros sistemas (`research/R1_fundamentos/REPORT.md` §2.3). De ahí que la
pregunta por el pre-ARNm nuclear y por el ARN no codificante quede abierta y no cerrada:
un intrón sí se transcribe —está en el pre-ARNm— y lo que no suele estar es en el ARNm
maduro, que es la referencia que usan los transcriptomas de RefSeq. **«No está en el
transcriptoma» no es sinónimo de «no se transcribe»; es «no está en el conjunto de ARNm
maduros anotados».** `[H]` Esa es la distinción fina que conviene explicitarle al
investigador, porque cambia cómo se interpreta la ponderación.

---

## 2. Qué se puede medir con lo que hay en esta máquina

La comparación exige que del **mismo organismo** existan los dos recursos. De los **17
conjuntos descargados** en `work/W4/downloads/`, sólo **dos tienen genoma y transcriptoma**
en disco:

| Organismo | Ensamblado | Genoma | Transcriptoma | ¿Comparable? |
| --- | --- | --- | --- | --- |
| *Zea mays* | GCF_902167145.1 | sí, 2.210 MB | sí, 76.549 secuencias | **sí** |
| *Apis mellifera* | GCF_003254395.2 | sí, 228 MB | sí, 27.887 secuencias | **sí** |
| *Dalbulus maidis* | GCA_975739785.1 | sí | no existe transcriptoma anotado: el ensamblado no está anotado | no |
| *Dalbulus maidis* (TSA) | GITV01, GHCC01, GCWP01 | — | sólo transcriptomas de novo | no |
| *Homalodisca vitripennis* | GCF_021130785.1 | no bajado | sí | no |
| *Folsomia candida* | GCF_002217175.1 | no bajado | sí | no |
| *Chrysoperla carnea* | GCF_905475395.1 | no bajado | sí | no |
| *Coccinella septempunctata* | GCF_907165205.1 | no bajado | sí | no |
| *Harmonia axyridis* | GCF_914767665.1 | no bajado | sí (en `work/W5/ref/`) | no |
| GCF_014356525.2, GCF_028750875.1 | — | no bajado | sí | no |
| mollicutes, virus, *Dalbulus elimatus*, haplotipo alternativo | — | varios | no corresponde (procariotas y virus no tienen intrones ni transcriptoma RefSeq separado) | no |

Así que la medición de Q2 **usa dos organismos, maíz y abeja**, y lo dice. Para
*H. vitripennis*, que es donde W5 encontró el riesgo real, **no hay genoma local** y por lo
tanto no se puede saber si sus aciertos son exónicos o no; bajarlo es trabajo pendiente y
barato.

---

## 3. La medición

Herramienta: `tools/sifi21_port/offtarget_21nt.py`, **sin modificar**, con pyahocorasick,
Python 3.11.17. Consulta: las 920 ventanas de 21 nt de las cuatro regiones elegidas
(`work/C4/fasta/epilab_sel.fasta`, copia de `work/W5/fasta/`). Criterios: bloque contiguo
perfecto de ≥ 19 nt, 21/21 perfecto, y 21 nt con exactamente un desajuste.

```bash
python tools/sifi21_port/offtarget_21nt.py \
    --consulta work/C4/fasta/epilab_sel.fasta \
    --db work/C4/db/Zmays_genoma.fna work/C4/db/Zmays_transcriptoma.fna \
         work/C4/db/Amel_genoma.fna work/C4/db/Amel_transcriptoma.fna \
    --mm1 --salida work/C4/offtarget/gen_vs_tx
python research/ola3/C4_offtargets_quimeras_largo/scripts/genoma_vs_transcriptoma.py
python research/ola3/C4_offtargets_quimeras_largo/scripts/q2_empalme_exonico.py
```

Control de que la corrida es la misma que la de W5: sobre las mismas cuatro regiones y las
seis referencias de W5, este tamizaje reproduce exactamente los números publicados —222 y 205
para `ATPaseD_Dm` y 220 y 204 para `BicC_Dm` contra el genoma de *D. maidis*, 30 y 22 y 7 y 3
contra *H. vitripennis*, 3 y 3 contra transcritos de maíz— así que lo que sigue no es un
cambio de método sino el mismo método con una base de datos más. `[E]`

### 3.1 El cruce, por región y criterio

| Organismo | Región | Criterio | Sólo genoma | Sólo transcriptoma | En los dos |
| --- | --- | --- | ---: | ---: | ---: |
| *Zea mays* | `BicC_Dm` | 21/21 perfecto | **1** | 0 | 0 |
| *Zea mays* | `BicC_Dm` | bloque ≥ 19 nt | **8** | **3** | **0** |
| *Zea mays* | `BicC_Dm` | 21 nt con 1 desajuste | 8 | 1 | 1 |
| *Zea mays* | `MP_MRFV` | bloque ≥ 19 nt | 3 | 0 | 3 |
| *Zea mays* | `MP_MRFV` | 21 nt con 1 desajuste | 4 | 0 | 1 |
| *Zea mays* | `CP_MRFV` | 21 nt con 1 desajuste | 4 | 0 | 4 |
| *Zea mays* | `ATPaseD_Dm` | 21 nt con 1 desajuste | 7 | 0 | 1 |
| *Apis mellifera* | `BicC_Dm` | 21 nt con 1 desajuste | 2 | 0 | 3 |
| *Apis mellifera* | `MP_MRFV` | 21 nt con 1 desajuste | 1 | **2** | 1 |

Las celdas vacías son ceros: con los criterios perfectos, **en abeja no hay un solo acierto,
ni en el genoma ni en el transcriptoma**, y las dos regiones virales no aciertan en maíz salvo
por `MP_MRFV`. Tabla completa en `resultados/q2_cruce_genoma_transcriptoma.tsv`.

### 3.2 Dónde caen los aciertos de genoma

Para los 14 siRNA con acierto en el ensamblado de maíz, localizamos la posición exacta del
k-mero y la cruzamos con el GFF de RefSeq. Los 25 aciertos resultantes se reparten en **seis
loci**:

| Clase | Aciertos | Locus | Qué es |
| --- | ---: | --- | --- |
| exón | 3 | NC_050100.1:138.170.650 (`LOC103626931`) | el gen que W5 ya había nombrado; es el mismo acierto que aparece en el transcriptoma |
| intrón | 3 | NC_050100.1:71.307.242 (`LOC103626522`) | tres ventanas de `BicC_Dm` sobre un intrón anotado |
| intergénico | 18 | NC_050098.1:15.202.499 · NC_050098.1:189.908.025-45 · NC_050098.1:226.786.343 · NC_050102.1:131.212.454 | tres de esos cuatro loci son el **mismo** bloque de 19 nt rico en GC repetido en el genoma; el cuarto concentra las ventanas 255-259 de `BicC_Dm` |
| intergénico, 21/21 | 1 | NC_050098.1:189.908.025 | **la única coincidencia perfecta de 21 nt de las 920 ventanas en todo el maíz cae en una región intergénica** |

Detalle por acierto en `resultados/q2_aciertos_localizados.tsv`.

Dos lecturas, con su marcador. La primera: **el caso que el investigador describió existe de
verdad en nuestros datos y es justamente el peor acierto del conjunto.** El único 21/21
perfecto contra maíz —el acierto que con el criterio más estricto sería descalificante— no
toca ningún gen anotado. Si el criterio de ranking no distingue dónde cae, ese acierto pesa
igual que uno sobre un exón, y la región de `BicC_Dm` queda penalizada por algo que, bajo el
mecanismo post-transcripcional, no tiene blanco. `[H]`

La segunda, que matiza la primera: **«intergénico» acá quiere decir «fuera de todo gen
anotado en RefSeq», y el genoma del maíz es en su mayor parte elementos repetidos.** Que el
mismo 19-mero rico en GC aparezca en tres loci intergénicos distintos es la firma de una
región repetida, no de un gen desconocido; pero que una región no esté anotada no prueba que
no se transcriba. Conviene tratar «intergénico» como «sin blanco de ARNm conocido», no como
«inocuo». `[?]`

### 3.3 El hallazgo simétrico: hay aciertos que existen sólo en el ARN

La fila que más enseña de la tabla 3.1 es la de `BicC_Dm` con bloque ≥ 19 nt: **8 sólo en el
genoma, 3 sólo en el transcriptoma, 0 en los dos.** Los tres del transcriptoma son los que W5
reportó sobre `LOC100281777`. Que no aparezcan en el genoma sólo puede querer decir dos cosas,
y las separamos midiendo: localizamos los nueve bloques (3 ventanas × 3 variantes de
transcrito) en el ARN y reconstruimos las coordenadas de las uniones exón-exón de cada
transcrito desde el GFF.

| Ventana de la región | Transcrito | Gen | Posición en el transcrito | Exones | ¿Cruza una unión? |
| --- | --- | --- | --- | ---: | --- |
| 123, 124, 125 | NM_001154697.2 | `LOC100281777` | 1.272–1.290 | 10 | **sí, la unión en 1.279** |
| 123, 124, 125 | XM_008677183.3 | `LOC100281777` | 1.408–1.426 | 11 | **sí, la unión en 1.415** |
| 123, 124, 125 | XR_564801.3 | `LOC100281777` | 1.408–1.426 | 11 | **sí, la unión en 1.415** |

**Nueve de nueve.** `[E]` El único off-target sobre secuencia expresada de maíz existe
exclusivamente en el ARN mensajero: en el ADN genómico sus dos mitades están separadas por un
intrón. La asimetría, entonces, va en los dos sentidos —el genoma tiene aciertos que el ARNm
no tiene, y el ARNm tiene aciertos que el genoma no tiene—, y es exactamente el mismo
fenómeno que W5 ya había cuantificado del lado del blanco, cuando explicó la diferencia
280 − 220 por las tres uniones exón-exón de la región de `BicC_Dm`.

La consecuencia práctica es incómoda para la idea de «usar el genoma cuando no hay
transcriptoma»: **el genoma no es un sustituto conservador del transcriptoma, porque pierde
las ventanas de unión de exones**, que son las únicas que tocaron un gen expresado de maíz en
todo este conjunto. En abeja se ve lo mismo en versión pequeña: dos aciertos con un desajuste
de `MP_MRFV` aparecen sólo en el transcriptoma (no verificamos si cruzan uniones; es trabajo
de media hora con el mismo script). `[E]` el conteo, `[H]` la generalización.

---

## 4. La ponderación propuesta

Todo este apartado es `[H]`: es una propuesta del equipo, con parámetros libres, no un
resultado. La forma, deliberadamente simple para que se pueda auditar y discutir:

> **peso de un acierto = (clase de blanco) × (criterio de coincidencia) × (importancia del
> organismo)**, y el riesgo de una región es la **suma** de los pesos de sus aciertos, no el
> máximo ni el promedio. Cada acierto se cuenta **una sola vez, por su criterio más fuerte**:
> la ventana que tiene 21/21 no se vuelve a contar como bloque de 19 nt.

Los tres factores, con el valor que proponemos y el motivo:

**Clase de blanco**, que es lo que pidió el investigador. Exón de gen codificante anotado =
**1,0**; unión exón-exón del ARNm maduro = **1,0** (es ARNm real, y además es la clase que el
genoma no ve); ARN no codificante anotado = **0,6**, porque es transcrito pero el fenotipo de
silenciarlo es menos predecible; intrón = **0,3**, porque está en el pre-ARNm nuclear y no en
el blanco citoplasmático canónico; intergénico sin anotación = **0,1**, que no es cero porque
«no anotado» no es «no transcrito». La escala es nuestra; lo único que la evidencia sostiene
es el **orden**, y lo sostiene de forma indirecta: el mecanismo que describen las herramientas
es post-transcripcional sobre ARNm (`S06`, `S08`), y el único trabajo que clasifica ubicación
lo hace en estas mismas tres clases (`S05`).

**Criterio de coincidencia**, para no mezclar plausibilidades mecánicas distintas, que es el
error que W2 documentó en dsRNA-Engineer. 21/21 perfecto = **1,0**; bloque perfecto de 19–20
nt = **0,5**; 21 nt con un desajuste = **0,25**. El 1,0 del 21/21 es el único valor con
respaldo de bioensayo (`S01`, `S02`, `S03`); los otros dos son convención y se marcan como
tal.

**Importancia del organismo**, que no es una decisión técnica sino de política del proyecto.
Cultivo que se quiere proteger (*Zea mays*) = **1,0**; polinizador y enemigo natural = **1,0**;
hemíptero no objetivo = valor a definir por el laboratorio, con el problema ya registrado de
que *Macrosteles quadrilineatus* es a la vez plaga y vector (`pipeline/REPORT.md` §4.2); humano
y ganado = **1,0**. Dejamos este factor explícito y sin resolver a propósito: es el que el
investigador tiene que fijar.

### 4.1 Qué cambia en nuestros cuatro candidatos

Con los pesos de arriba y los aciertos medidos, el riesgo en maíz de la región de `BicC_Dm`
pasa de «9 aciertos ≥ 19 nt, uno de ellos perfecto» a:

| Región | Aciertos en maíz | Riesgo sin ponderar (cuenta de ≥ 19 nt) | Riesgo ponderado |
| --- | --- | ---: | ---: |
| `BicC_Dm` | 1 × 21/21 intergénico, 4 × ≥19 nt intergénico, 3 × ≥19 nt en intrón (genoma); 3 × ≥19 nt en unión exón-exón (ARNm) | 11 | 1×1,0×0,1 + 4×0,5×0,1 + 3×0,5×0,3 + 3×0,5×1,0 = **2,25** |
| `MP_MRFV` | 3 × ≥19 nt en exón (en los dos recursos), 3 × ≥19 nt sólo en genoma | 6 | 3×0,5×1,0 + 3×0,5×0,1 = **1,65** |
| `CP_MRFV` | ninguno | 0 | **0** |
| `ATPaseD_Dm` | ninguno perfecto | 0 | **0** |

Es decir: la ponderación **no cambia quién queda primero ni quién queda último**, cambia la
distancia entre `BicC_Dm` y `MP_MRFV` —de 11 contra 6 a 2,25 contra 1,65— y hace explícito
que la mayor parte del riesgo que le contábamos a `BicC_Dm` en maíz venía de ADN que no
produce ARNm anotado. `[H]`

### 4.2 Sensibilidad a los pesos

La prueba está en `criterio_ranking_propuesto.md` §3 y se corre con
`scripts/ranking_sensibilidad.py`. El resumen para este documento: barriendo 20.000 juegos de
pesos sobre el símplex, **el orden relativo de `CP_MRFV` frente a `BicC_Dm` y frente a
`ATPaseD_Dm` no se puede invertir con ningún peso no negativo** —son dominancias, no
elecciones—, mientras que el par `MP_MRFV` contra `CP_MRFV` **se da vuelta según los pesos**:
`MP_MRFV` queda primero en el 32,9 % del espacio. Ese par es, literalmente, la parte del
ranking que elegimos nosotros. `[H]`

---

## 5. Lo que no hicimos y conviene hacer

Bajar el genoma de *Homalodisca vitripennis* y repetir el cruce ahí, que es donde están los
aciertos que importan (30 y 7 ventanas); verificar si los dos aciertos con un desajuste de
abeja que aparecen sólo en el transcriptoma también cruzan uniones de exones; y, si el
laboratorio quiere usar la clase «ARN no codificante» con peso propio, separar en el GFF los
genes de ARN no codificante de los codificantes, que hoy entran los dos como «exón».
