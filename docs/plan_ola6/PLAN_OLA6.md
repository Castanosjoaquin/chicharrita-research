# Plan de la ola 6 — cerrar el checkpoint 2 y construir el encadenamiento

**Fecha del plan:** lunes 2026-10-26, después del checkpoint 2 y después de
[`docs/plan_cierre/PLAN_CIERRE.md`](../plan_cierre/PLAN_CIERRE.md).

**Qué agrega sobre el plan de cierre.** `PLAN_CIERRE` contestó una pregunta acotada —cuáles de
los quince pendientes sueltos se pueden ejecutar ya— y la contestó bien: sus seis tareas siguen
vigentes y **este plan no las rebautiza ni las reordena**, las hereda con su nombre (`R1` a
`R6`). Lo que `PLAN_CIERRE` no tiene, porque no era su pregunta, son tres cosas:

1. **La línea de cómputo nueva que dejó la reunión.** La quimera por fenotipos complementarios
   figura en `PLAN_CIERRE` §8 solamente como un insumo que espera el zip. No tiene tarea, ni
   criterio de terminado, ni el aviso de que el evaluador de quimeras hoy **no acepta un gen
   que no sea uno de los cuatro de EPILAB**.
2. **El entregable.** El investigador nombró la contabilidad de la juntura como el diferencial
   posible, y hoy vive enterrada en un `REPORT` de la ola 5. Mover un resultado medido al
   entregable no está en la lista de los quince.
3. **El encadenamiento como producto.** Las tres features que discutimos —transferencia de
   anotación por homología, lectura de la evidencia en lenguaje natural y recomendador de
   genes— no son pendientes de cierre: son desarrollo. Y la primera dejó de ser opcional,
   porque es la única forma de leer el archivo que él va a mandar.

**Lo que este plan no reabre.** `D62` a `D67` son del 25 y 26 de octubre y están escritas. En
particular `D66` (la exposición del no objetivo se declara, no se le pide un número) y `D67`
(las quimeras se arman por combinación de fenotipos y la juntura se cuenta aparte) ya fijan el
criterio que varias tareas de acá aplican. La entrada de `CAMINOS_PROBADOS.md` que descarta
categorizar genes con un modelo de lenguaje también está escrita. **Nada de eso es tarea
pendiente: es el marco.**

---

## 0. La corrección técnica que ordena el plan de quimeras

Antes de las tareas hay que dejar escrita una corrección, porque la intuición natural sobre las
quimeras —y la que el equipo venía usando— es medible y está medida como **a medias**.

La intuición es: *si las dos partes son regiones que ya se validaron, el único lugar donde la
quimera puede dar distinto es la unión, donde la ventana toma una porción de cada gen.*

**Para el eje de riesgo eso es exactamente cierto, y es un resultado nuestro con consecuencia
operativa.** El estado de off-target de una ventana depende sólo de su secuencia, y toda ventana
heredada es base por base una ventana de su región de origen: lo único nuevo son los 40 nt que
cruzan cada unión. `C13` §6 lo usa para tamizar **1.160 ventanas en vez de 5.760** y obtener el
resultado idéntico a tamizar las doce moléculas enteras `[M]`. Quien quiera defender la idea
tiene acá su mejor argumento, y no es retórico: es una pasada en vez de siete.

**Para el eje de eficacia es falso, y el número que lo desmiente ya está en el repositorio.** La
eficiencia de una ventana no depende sólo de sus 21 nt: depende de la accesibilidad, que el
original calcula sobre un tramo de 8 nt terminal dentro de una ventana de plegado de 80 nt. Esa
ventana de plegado **cruza la unión**, así que la secuencia del otro gen cambia el veredicto de
ventanas que están enteramente dentro de un fragmento. El techo es asimétrico y está derivado
del código: la secuencia ajena influye hasta **72 nt corriente abajo** del final de una ventana
y hasta **59 nt corriente arriba** de su comienzo (`C13` §4) `[M]` el número, `[H]` la
derivación.

Cuánto pesa, en las doce quimeras de las regiones vigentes, modo `corregido`
(`research/ola3/C13_quimeras_region_recomendada/resultados/quimeras_ventanas_cambiadas_vigentes_corregido_vienna.tsv`):

| Lugar donde la quimera difiere de la suma de sus partes | Cuánto |
| --- | ---: |
| Ventanas de juntura eficientes (las 240 de las doce uniones) | **4** |
| Ventanas **heredadas** que cambiaron de veredicto | **61** — 31 pierden eficiencia y 30 la ganan |
| Distancia máxima a la unión de una heredada que cambió | **66 nt** |

Y el remate, textual de `C13` §5: con las regiones vigentes **«todo el Δ viene de la banda de
contexto y nada del empalme» en diez de las doce** `[M]`. O sea que el lugar que la intuición
señala como el único problemático aporta 4 cambios, y el lugar que la intuición da por seguro
aporta 61.

`[H]` **La lectura para el plan.** Hay **tres** sitios donde una quimera difiere de la suma de
sus partes, no uno: las veinte ventanas de cada juntura, la banda de contexto de ±66 nt
observados alrededor de la unión, y los extremos de la molécula —donde el fragmento de la
izquierda deja de tener su cola como final de molécula, que es el mecanismo de `end_stability`
con nucleótidos colgantes que `C13` aisló en una posición—. De los tres, dos no se pueden
heredar de la validación de las partes y hay que recalcular. Que los 61 cambios casi se cancelen
—31 contra 30, y por eso el Δ total queda entre −4 y +3— **no autoriza a saltearlos**: es un
resultado de estas cuatro regiones, no una propiedad de las quimeras.

> **Por qué esto importa más allá de la prolijidad.** Si el entregable afirma que la quimera
> hereda la validación de sus partes salvo en la unión, afirma algo que nuestras propias tablas
> contradicen, y es exactamente el tipo de cosa que el investigador revisa. Lo correcto es la
> versión fuerte: **el riesgo se hereda y la eficacia se recalcula**, con las dos cuentas por
> separado y cada una con su número.

---

## 1. Las líneas

Cuatro grupos. El primero es el cierre heredado; el segundo, lo que la reunión dejó sin tarea;
el tercero, el desarrollo; el cuarto, lo que depende del equipo.

### Grupo A — el cierre (heredado de `PLAN_CIERRE`, sin cambios)

| Línea | Qué | Cómputo | Marca |
| --- | --- | --- | --- |
| `R1` | Firmar las 17 alertas, con la persistencia primero | no | — |
| `R2` | Que algún entregable llame a la compuerta | no | depende de `R1` |
| `R3` | `estado.html` con la ola 5 y el checkpoint 2 | no | — |
| `R4` | `UMBRAL_OFF_ALERTA` contra el piso de `D28` | no | — |
| `R5` | Las dos cifras viejas de los entregables | no | **cambia cifras publicadas** |
| `R6` | El tercer marco y el empate declarado | no | **cambia cifras publicadas** |

El detalle ejecutable de las seis está en `PLAN_CIERRE` §2 a §7 y no se repite acá. Lo único que
este plan agrega es una advertencia de orden: **`R3` depende de que `R5` y `R6` se hayan decidido
o no**, porque la lista `FALTA` de `generar_estado.py` nombra las dos. Si `R3` se hace primero,
hay que dejar esas dos filas en `FALTA` y no borrarlas.

### Grupo B — lo que la reunión dejó y el plan de cierre no tiene

#### `O1` — La juntura sube al entregable, y con la contabilidad completa

**Por qué.** Él lo nombró como *«los detalles que está bueno tener en cuenta y que pueden dar un
diferencial»* `[R]`, y la frase con la que lo resumió es la más citable de la reunión: *«me puede
decir que es el mejor eficiente del mundo, pero si no va a encontrar su target en la planta o en
el insecto, no va a ser»* `[R]`. Está medido desde el 25 de octubre y vive en
`research/ola5/N4_quimeras/REPORT.md`. **Es mover un resultado, no producirlo.**

**Qué hay que hacer.** Llevar al entregable las tres cifras de `N4` —4 de 240 ventanas de juntura
eficientes, ninguna con blanco continuo, y las 8 con blanco que son todas de los extremos y
ninguna eficiente— junto con la contabilidad del canje: una quimera no agrega ventanas, cambia
los veinte arranques de cola de cada fragmento por veinte de juntura. Y **con la corrección de
§0 al lado**: la juntura no es el único lugar que cambia, son 4 contra 61.

**Lo que no hay que hacer.** Presentarlo como una objeción a las quimeras. `D67` ya decidió que
se arman por fenotipo; esta cifra dice cómo se cuentan, no si se hacen.

**Criterio de terminado.**

- [ ] Un entregable publica las tres cifras de `N4` con su fuente y su alcance declarado.
- [ ] La corrección de §0 está en el mismo lugar, con los dos números (4 y 61) y el techo
      asimétrico.
- [ ] El `.html` se regeneró con `python tools/md_a_html.py entrada.md salida.html`.
- [ ] El límite de `N4` viaja con la cifra: medimos coincidencia exacta de 21 nt, no
      apareamiento parcial `[?]`.

#### `O2` — La secuencia de `V-ATPase B`, por las dos vías

**Por qué.** Es el único insumo que bloquea la quimera de fenotipos complementarios. `DM-02` está
en el catálogo de `C5` con fenotipo publicado en la especie —alas deformes, supervivencia 16 % al
día 4 contra 37 % del control de GFP, Jones, Bernal y Medina 2021, leído completo— pero **sin
secuencia en el panel de trabajo** `[M]`.

**La vía que `PLAN_CIERRE` no consideró.** El plan de cierre lo clasifica como «espera el
transcriptoma». Hay una segunda vía que no depende de él: los **tres transcriptomas públicos de
*Dalbulus maidis*** ya están en disco como bases de datos de búsqueda
(`work/C11/db_GHCC01`, `db_GCWP01`, `db_GITV01`), y la V-ATPasa es un complejo conservado con
proteína disponible en parientes —incluido `DE-01`, *Peregrinus maidis*, que tiene las dos
subunidades con bioensayo publicado—. O sea que la subunidad B se puede **intentar recuperar por
homología a nivel proteína** antes de que llegue el zip. Si sale, desbloquea `O3` sin esperar
nada; si no sale, el resultado útil es saber que ese transcriptoma no la contiene, que es la
misma respuesta que `C11` necesita para `eth` y `burs-alpha`.

**La restricción de entorno, que hay que decir antes de asignar la tarea.** En esta máquina
—verificado— **no hay `blastn`, `tblastn`, `makeblastdb`, `miniprot`, `diamond`, `bowtie` ni el
módulo `RNA` de ViennaRNA**, y el `python3` del PATH es 3.9.6 con numpy 2.0.2. Las bases de
`work/C11/` se construyeron en otra máquina. Esta tarea necesita un alineador de proteína contra
nucleótido, así que corre donde haya uno o empieza por instalarlo; **no es trabajo de escritorio**.

**Qué hay que hacer.**

1. Conseguir la proteína de `V-ATPase B` de un pariente con anotación, por accesión pública.
2. Alinearla contra los tres transcriptomas con `tblastn` o `miniprot`, **a nivel proteína**:
   `C5` midió que entre géneros de cicadélidos la identidad en nucleótido es 77–84 % y en
   proteína la mediana es 0,866, así que buscar en nucleótido tira señal real `[M]`.
3. Exigir **ortología recíproca**, no el mejor acierto. El número que lo justifica es nuestro:
   en `C5`, elegir el gen por nombre en el transcriptoma de la especie cercana devolvió un gen
   distinto del que devolvió la homología, con un **65 %** de diferencia en el conteo de ventanas
   eficientes `[M]`.
4. Registrar la identidad del alineamiento y la banda de concordancia que le corresponde, no
   sólo el nombre del gen.

**Criterio de terminado.** Una de las dos salidas, y las dos sirven:

- [ ] Hay un CDS candidato de `V-ATPase B` con su transcriptoma de origen, su identidad, su
      cobertura y su recíproco verificado; **o**
- [ ] queda escrito que los tres transcriptomas públicos no la contienen, con el método y el
      umbral con el que se buscó, y la tarea pasa a esperar el zip.
- [ ] La vía usada queda declarada: homología local, nunca un servicio web que procese las
      secuencias (`CLAUDE.md`).

#### `O3` — La quimera `BicC_Dm` + `V-ATPase B`, evaluada con las tres cuentas separadas

**Por qué es la primera prioridad de cómputo.** Es **lo único realmente nuevo que salió de la
reunión**, y la combinación cubre los dos ejes que a `BicC_Dm` le faltan: él tiene el mejor
perfil de riesgo con un fenotipo que no bloquea transmisión, y `V-ATPase B` aporta movilidad
—alas deformes— y mortalidad. Que `V-ATPase B` y `V-ATPase D` sean dos subunidades del mismo
complejo y se separen justo por el eje que él nombró es lo que vuelve armable la combinación y no
una ocurrencia `[H]`.

**Depende de `O2`.** Y **necesita ViennaRNA**, que no está en esta máquina.

**El obstáculo de código que nadie anotó.** `quimeras_v2.py:51` tiene
`REGIONES = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]` **fija**, y `CONJUNTOS` trae las
coordenadas de los tres conjuntos conocidos. El evaluador de hoy no acepta un gen nuevo: hay que
generalizarlo, y conviene hacerlo en `O3` y no inventar un script paralelo.

**Qué hay que hacer.**

1. Generalizar el evaluador para que tome dos genes y dos regiones cualesquiera, **conservando
   el ancla**: el script actual aborta si no reproduce la tabla de `C4` fila por fila, y esa
   verificación es lo que autoriza a leer los números nuevos. No se pierde.
2. Correr los **dos órdenes**. El orden importa y está medido: `ATPaseD_Dm` + `MP_MRFV` da +3 y
   el orden inverso da −3 con las mismas dos regiones `[M]`.
3. Reportar **tres cuentas separadas**, que es lo que §0 obliga:
   - eficientes heredadas, con la cuenta de cuántas cambiaron de veredicto y a qué distancia de
     la unión;
   - eficientes de juntura, y de ésas cuántas tienen blanco continuo de 21 nt;
   - riesgo del empalme, tamizando sólo los 40 nt nuevos contra el panel de seis referencias.
4. **Alerta explícita si la unión fabrica una coincidencia que ninguno de los dos padres tenía.**
   No es hipotético: en `MP_MRFV` + `ATPaseD_Dm` el empalme fabrica un bloque perfecto de 19 nt
   que no existe en ninguno de los dos genes y **sí existe en tres transcriptos de *Zea mays***,
   y dos de las doce adquieren un veto que ninguna de sus partes tenía `[M]`.

**Criterio de terminado.**

- [ ] El ancla de `C4` sigue pasando después de generalizar el evaluador.
- [ ] Las dos quimeras (los dos órdenes) tienen sus tres cuentas y su tabla versionada.
- [ ] La fila de riesgo del empalme está tamizada y, si fabrica algo nuevo, tiene su alerta con
      los cuatro campos de `D48`.
- [ ] El resultado se lee contra `D67`: si la quimera no supera a sus partes en conteo, **eso no
      la descarta**, porque el objetivo declarado es cubrir dos fenotipos. Lo que la descartaría
      es el perfil de riesgo del empalme.

**La salvedad biológica que va escrita junto al resultado.** Silenciando dos genes a la vez, si
el bioensayo da negativo no se sabe cuál mitad falló. No invalida el diseño —el objetivo es
justamente cubrir los dos efectos— pero es un argumento para testear las partes por separado
primero `[H]`.

#### `O4` — El enumerador de quimeras como feature

**Por qué, y por qué después de `O3`.** La feature que se discutió es: pasale dos genes y que te
devuelva la mejor quimera, variando las secuencias y las proporciones. Vale, pero **no se vende
como «la quimera con más ventanas eficientes»**, porque está medido que por ese lado no hay nada
que ganar: con las regiones vigentes el empalme aporta 4 eficientes de 240 —el 1,7 %, contra el
7–15 % de las regiones recortadas— y **ninguna de las doce supera a su mejor parte en ninguno de
los dos ejes del ranking**, y una queda por debajo de las dos `[M]`. El «bonus gratis» que `C4`
había encontrado era una propiedad de las regiones de EPILAB, que eran mediocres dentro de su
gen, no de las quimeras.

**Sobre las proporciones: no hace falta optimización.** Para dos genes con largo total fijo los
parámetros libres son los dos arranques y el punto de corte: es una grilla enumerable. `W2` §4 ya
documentó que ninguna metaheurística mejora la enumeración exhaustiva en la elección de región, y
acá pasa lo mismo. Enumerar es más barato, más rápido y **auditable**, que es lo que este
proyecto necesita `[H]`.

**Qué hay que hacer.** Una entrada de dos genes y un largo total; una salida que ordene las
combinaciones **bajo un objetivo declarado antes de rankear**, no «la mejor» a secas; las tres
cuentas de `O3` por combinación; y la alerta de juntura nueva.

**Criterio de terminado.**

- [ ] El objetivo del ranking está declarado en el código y en la salida, no implícito.
- [ ] La salida nunca suma ventanas de juntura a ventanas heredadas en una sola cifra.
- [ ] La grilla es enumerable y está documentada; no hay metaheurística.

### Grupo C — el encadenamiento como producto

Las tres entran en este orden por relación valor/riesgo, y la primera cambió de categoría después
de la reunión: **dejó de ser opcional.**

#### `F1` — Transferencia de anotación por homología

**Por qué ya no es una feature extra.** Él se comprometió a mandar el transcriptoma y avisó cómo
viene: *«los IDs están hechos por el que hizo el transcriptoma, no coinciden los nombres, no vas
a poder encontrar, pero sí por identidad o homología»* `[R]`. **El archivo que va a mandar no se
puede leer sin esto.** Y para este organismo no hay alternativa: *Dalbulus maidis* tiene tres
ensamblados públicos y **ninguno está anotado**, ni tiene par en RefSeq `[M]`.

**Qué está medido y es la base de la feature**, no una promesa:

| Medición | Resultado | Fuente |
| --- | --- | --- |
| Concordancia de anotación entre dos cicadélidos, pares recíprocos | **78,2 %** sobre 1.152 pares; de 76,1 % en identidad 40–60 % a **86,2 %** en ≥ 90 % | `C12` A |
| Loci recuperados en el genoma no anotado del vector | **12.540** distintos, desde 32.269 de 34.269 proteínas consulta, 568 s y 3,7 GB | `C5` |
| Poliproteína del MRFV transferida a sus parientes | 11 de 11 marafivirus | `C12` B |

Y el 78,2 % es cota inferior: parte de los desacuerdos en los tramos altos son **sinónimos**, no
funciones distintas —*glycogen synthase kinase-3 beta* contra *shaggy*, con 99,2 % de identidad,
es el mismo gen con dos nombres `[M]`—.

**Las seis correcciones de método que la vuelven defendible.**

1. **Alineamiento, no coincidencia exacta.** Un autómata de Aho-Corasick busca coincidencias
   idénticas y la homología es parecido con sustituciones e indels. Aho-Corasick es la
   herramienta correcta para el paso de off-target de 21-meros —y ahí ya la usamos,
   `offtarget_21nt.py`— y la incorrecta para éste.
2. **A nivel proteína**, por lo que midió `C5`: 77–84 % en nucleótido contra 0,866 de mediana en
   proteína.
3. **Ortología recíproca, nunca el gen con el mismo nombre.** El 65 % de diferencia en el conteo
   de ventanas eficientes al elegir por nombre es nuestro y es el argumento más fuerte.
4. **Cada anotación transferida viaja con su identidad y su banda de concordancia.** No «es una
   subunidad de la V-ATPasa», sino «con 94 % de identidad a su ortólogo recíproco, tramo en el
   que la concordancia medida es 86 % (IC 80,9–90,2)». Sin la banda, la feature miente por
   omisión.
5. **Cortafuego duro: la anotación transferida nunca toca el diseño.** Contesta *qué gen
   considerar*; el diseño se hace **siempre** sobre la secuencia propia del vector. Es `D37`, y
   es la línea que vuelve segura toda la idea — las ventanas de 21 nt de la especie cercana que
   existen idénticas en *D. maidis* son **0,7 % a 11,1 %** `[M]`, así que diseñar sobre la
   secuencia del pariente no funciona y eso quedó cerrado.
6. **«Uncharacterized» se reporta, no se esconde.** `C12` excluyó los pares sin nombre
   informativo; una plataforma que los descarte en silencio sobredeclara su cobertura.

**Criterio de terminado.**

- [ ] Toma un transcriptoma sin anotar y devuelve, por locus, el ortólogo recíproco con
      identidad, cobertura y banda de concordancia.
- [ ] Ninguna salida de esta feature entra al diseño de ARNdc; hay una prueba que lo demuestra.
- [ ] Los loci sin anotación informativa aparecen contados, no filtrados.
- [ ] La primera corrida real es sobre el zip cuando llegue, y su resultado se compara contra
      `GHCC01` para chequear la hipótesis de que puedan ser el mismo transcriptoma `[?]`.

#### `F2` — La evidencia recuperada, leída en lenguaje natural

**Por qué.** El cuello de botella del biólogo no es calcular: es leer 12.540 loci.

**Y la regla dura, que no se negocia.** El modelo **resume anotaciones recuperadas, con la cita
al lado; nunca genera función**. La entrada son los nombres de producto, los términos GO, los
dominios y los papers encontrados; la salida es un párrafo que dice qué hace el gen **y de dónde
sale eso**. El modo de falla ya está documentado en el repositorio: una cabecera FASTA sin
paréntesis no es un transcripto anotado, y la regla escrita es que inventarle un símbolo al
cromosoma sería el peor error posible. Un modelo de lenguaje lo inventa con toda naturalidad.
Entonces: **sin anotación, no hay párrafo** — devuelve «sin anotación de gen» en vez de una
conjetura plausible.

> Esta feature es la versión que sobrevive del paso 2 de la propuesta del equipo. La versión
> original —categorizar genes con un modelo de lenguaje para decidir cuáles son esenciales— ya
> está en `CAMINOS_PROBADOS.md` como camino reemplazado por la transferencia por homología. **No
> se reabre.**

**Criterio de terminado.**

- [ ] Cada párrafo generado tiene, al lado, la fuente de cada afirmación que contiene.
- [ ] Hay una prueba con un locus sin anotación que verifica que la salida es «sin anotación de
      gen» y no un párrafo.

#### `F3` — Recomendador de genes

**Por qué es la que más valor agrega.** Elegir la **región** dentro de un gen está resuelto y es
enumerable por fuerza bruta. Elegir el **gen** es el paso que el proyecto dejó abierto, y es el
nivel donde el investigador trabaja: *«hiciste una búsqueda biológica, de contexto biológico, y
lo pusiste en el nuevo programita y chequeaste, y tal vez ese gen es mejor porque tiene cero
off-targets»* `[R]`.

**Sólo es defendible si el criterio se declara antes de rankear**, como todo lo demás acá. Los
ejes, con lo que hay y lo que no:

| Eje | ¿Lo tenemos? |
| --- | --- |
| Evidencia de fenotipo por RNAi en un insecto emparentado | sí — catálogo de `C5`, 36 filas |
| Esencialidad o vía metabólica (V-ATPasa, proteasoma, COPI) | sí, de literatura |
| Perfil de off-target contra el panel de seis | sí, la maquinaria ya está, y **no depende del criterio de eficiencia sin validar** |
| Conservación entre poblaciones de *D. maidis* | sí, los tres transcriptomas |
| **Expresión en el tejido expuesto** | **no.** Los transcriptomas públicos son de cuerpo entero y huevos |

`[H]` Esa última fila es un agujero real y es **el eje que más importa para una vía de entrega
oral**: si el gen no se expresa en el intestino, el ARNdc ingerido no tiene qué silenciar. La
versión honesta ordena sobre cuatro ejes y **declara el quinto como faltante** — que es
exactamente la forma del entregable actual, y la que a él le funcionó. Habría que ver si el zip
lo trae.

**Y el eje de fenotipo se vuelve obligatorio después de `D67`.** Si las quimeras se arman por
combinación de mecanismos, el recomendador tiene que saber a qué eje pertenece cada candidato:
reproducción, movilidad o letalidad. Hoy `tablero/orden.html` sólo cubre `BicC` y la V-ATPasa, y
el ranking no tiene eje de fenotipo.

**Criterio de terminado.**

- [ ] El criterio y los pesos están escritos antes de la primera corrida, con su ADR.
- [ ] La salida declara el eje faltante en el mismo lugar donde publica el orden.
- [ ] Cada candidato trae su eje de fenotipo, o «sin fenotipo publicado».

### Grupo D — lo que depende del equipo

| Línea | Qué | Estado |
| --- | --- | --- |
| `E1` | Fecha y texto del correo enviado | El repositorio sigue sin registrarlo. El borrador tiene siete preguntas y `PLAN_DESARROLLO.md` §8 decía cinco: sin el texto no se puede cotejar ninguna numeración |
| `E2` | El canal por el que se le entrega el port | La auditoría está hecha y en verde: 36 archivos, cero hallazgos sin exceptuar (`N9`). Lo pidió dos veces. **El canal se abrió solo:** él va a escribir para mandar el zip, y responder ese correo con el paquete es el momento natural |

---

## 2. Lo que no se cierra con trabajo de escritorio

Las tres están bien declaradas y conviene tenerlas a mano como respuesta, no como deuda.

1. **Matar o esterilizar.** Sigue abierta y es la que más podría reordenar el ranking. Él
   confirmó la lectura del fenotipo de `BicC` —reduce población entre generaciones, no corta
   transmisión en la temporada— y dijo explícitamente que no sabe si eso cambia la decisión
   `[?]`. Hoy el ranking no tiene eje de fenotipo, así que **no se puede afirmar si el orden de
   los candidatos del insecto cambia según el objetivo**. `F3` es lo que lo volvería decidible.
2. **Si una complementariedad incompleta da actividad en las ventanas de juntura.** Medimos
   coincidencia exacta de 21 nt. Si una parcial sirve, esas ventanas no serían inútiles sino
   menos útiles, y no lo sabemos `[?]`. Es el límite declarado de `N4`.
3. **Cuál de los dos modelos de la regla terminal predice mejor.** `M4` midió que harían falta
   **2.784** siRNA replicando el único diseño etiquetado que encontramos, y él coincidió en que
   hace falta un experimento `[R]`.

Y una advertencia transversal que hay que decir en cualquier presentación del encadenamiento:
**toda la cadena hereda el criterio de eficiencia sin validar.** Agregar etapas río arriba no
arregla lo que él viene señalando desde la primera carta, así que el argumento de venta no puede
ser «predice mejor». Lo que sí puede ser, y es más fuerte: **cada paso lleva su propia tasa de
error medida** — la transferencia tiene 78–86 %, la elección de región tiene su percentil contra
todas las regiones deslizantes con dos nulos, el riesgo tiene coincidencia exacta con dos
umbrales, y la quimera tiene la contabilidad del empalme `[H]`.

---

## 3. El entorno de cómputo, antes de asignar nada

Verificado en esta máquina, y es la restricción que más cambia quién puede hacer qué:

| Herramienta | Estado acá |
| --- | --- |
| `blastn`, `tblastn`, `makeblastdb` | **no están** |
| `miniprot`, `diamond` | **no están** |
| `bowtie`, `bowtie2` | **no están** |
| módulo `RNA` de ViennaRNA, `RNAplfold`, `RNAfold` | **no están** |
| `python3` del PATH | 3.9.6, numpy 2.0.2 |

`C13` corrió con Python 3.13.15, numpy 2.5.4 y ViennaRNA 2.7.2, y las bases de `work/C11/` se
construyeron en otra máquina. **Conclusión operativa:** `R1` a `R6`, `O1` y `O4` (la parte de
diseño) son trabajo de escritorio y corren acá. `O2`, `O3` y `F1` necesitan entorno y van a la
máquina que tenga ViennaRNA y un alineador, o empiezan por instalarlo. Asignar `O3` a esta
máquina es asignarlo a que se trabe en el primer import.

---

## 4. El orden sugerido, y el mínimo viable

**Primero lo que no mueve ninguna cifra publicada y no espera a nadie:**

1. `R3` · `estado.html` — la más barata, y la que hoy miente más.
2. `R4` · `UMBRAL_OFF_ALERTA` — contenida en un módulo.
3. `O1` · la juntura al entregable — es mover un resultado medido, y él lo nombró como el
   diferencial.
4. `R1` · firmar las alertas — la persistencia **primero**, o el trabajo se pierde.

**En paralelo, en la máquina con entorno:**

5. `O2` · la secuencia de `V-ATPase B`, que es el único insumo que bloquea lo nuevo.
6. `O3` · la quimera por fenotipos complementarios, en cuanto `O2` dé una de sus dos salidas.

**Con el OK del equipo, lo que toca lo publicado:**

7. `R5` · las dos cifras viejas.
8. `R6` · el tercer marco y el empate.

**Al final:**

9. `R2` · que la compuerta se llame de verdad, cuando `R1` esté.
10. `F1` · la transferencia de anotación, que se vuelve urgente el día que llegue el zip.
11. `O4`, `F2`, `F3` · el encadenamiento como producto.

**Mínimo viable:** `R3`, `R5` y `O1`. Las dos primeras hacen que un lector externo —él abriendo
el repositorio— vea números coherentes; la tercera pone en el entregable lo único que él nombró
como diferencial. `O3` es lo único realmente nuevo, así que si hay una sola persona con entorno,
va ahí.

**Lo que conviene no hacer:** empezar por `F2` o `F3`. Son las dos más vistosas y las dos que
dependen de criterios que todavía no están escritos. Y él fue explícito en que no evalúa el
código —*«no te la voy a evaluar en el sentido del código»*— sino por qué lo hicieron, para qué,
qué compararon y qué cosas biológicas vieron `[R]`. Construir más software no suma por sí mismo:
suma el razonamiento que lo rodea.
