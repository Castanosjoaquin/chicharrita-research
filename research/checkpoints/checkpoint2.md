# Checkpoint 2 — reunión con el investigador invitado

**Fecha de la reunión:** 2026-10-26.

**Fuentes.** Cinco audios, y **no son todos la misma cosa**. Conviene tener clara la
diferencia antes de leer, porque el peso de cada uno es distinto:

| Archivo | Qué es | Duración | Peso |
| --- | --- | --- | --- |
| `3-audio investigador.m4a` | **La voz del investigador**, segunda parte de la reunión | 7 min 20 s | es la fuente; manda sobre todo lo demás |
| `1-lo que se corto.opus` | Nota de voz de un compañero | 20 s | propuesta del equipo |
| `2-primera_parte que no se grabo.opus` | Nota de voz de un compañero | 1 min 27 s | propuesta del equipo |
| `4-lo que sugiere.opus` | Nota de voz de un compañero | 1 min 1 s | propuesta del equipo |
| `5-final.opus` | Nota de voz de un compañero | 28 s | propuesta del equipo |

**Una aclaración que cambia cómo se leen los cuatro audios cortos.** Se nos pasaron como
«lo que entendió un amigo de la primera parte del audio del investigador que no se grabó».
Al transcribirlos resultó que **no son un resumen de lo que dijo el investigador**: son la
propuesta propia de un compañero, grabada después de la reunión. El audio 4 lo dice con
todas las letras —*«ese fue un audio que me acabo de mandar a mí mismo para cerrar una
idea»*— y el audio 5 la encuadra como *«basado en lo que nos dijo el tipo (…) agregarle
todo lo que nos dijo él»*. Así que en este documento van en una sección aparte y marcados
`[H]`, que es lo que son: una idea del equipo para el producto final, informada por la
reunión pero no dicha por él. Tratarlas como palabra del investigador sería atribuirle algo
que no dijo. **La primera parte de la reunión sigue sin registro.**

**Transcripción:** local, faster-whisper `large-v3`, español, VAD activado, decodificación
greedy y segunda pasada con haz de 5 sobre el audio del investigador. Los audios no se
subieron a ningún servicio; el modelo corre en esta máquina. Las salidas crudas del modelo y
los scripts con los que se produjeron están en
[`checkpoint2_transcripciones/`](checkpoint2_transcripciones/), para que cada cita de este
documento se pueda auditar. Los audios originales no están versionados.

**Marcadores.** Lo que dijo el investigador es `[R]` —es una persona en una reunión, no
literatura revisada—, salvo donde presenta mecanismo consolidado, que va `[E]`. Las
propuestas del equipo son `[H]`. Lo que ya está medido en el repositorio y se cita acá para
contrastar va `[M]` con su ruta.

---

## Resumen

La reunión no corrigió nada de fondo. Eso es el titular, y conviene decirlo sin adornos
porque es raro: después de cuatro días de correcciones por correo —el contador histórico, el
veto que pasó a alerta, los dos ejes del panel— esta vez el investigador escuchó la
recomendación, la validó en los dos puntos donde el equipo había puesto la carne, y dedicó el
tiempo a **una línea de trabajo nueva**.

Lo que validó. Primero, la lectura biológica de `BicC_Dm`: cuando el equipo le dijo que ese
gen apunta a bajar la población y no a cortar la transmisión, contestó *«claro, porque tiene
que ver con la oviposición»*. Es exactamente la tesis de `entregables/recomendacion-defendida.md`
§1, y la confirmó sin que se la argumentaran. Segundo, el método del barrido de pesos: pidió
*«si probás un par de pesos distintos y cambia mucho, o todo medio parecido»*, que es
literalmente el barrido de 2.000 sorteos y la grilla de 4.368 configuraciones que ya están
hechos. Tercero, la ruta de homología para conseguir candidatos nuevos sobre el genoma no
anotado: *«totalmente»*.

Lo que pidió que es nuevo, y es lo único nuevo: **quimeras que combinen genes de fenotipos
distintos**. No quimeras para sumar ventanas eficientes —eso ya lo habíamos hecho— sino para
combinar efectos biológicos que no se solapan: la reproducción por un lado, las alas por
otro, algo esencial que mate por otro. *«Si no tiene alas, por más que ande ahí, no
importa.»* Es una idea de diseño, no de cómputo, y es la que mejor encaja con lo que él
mismo llama el diferencial.

Y marcó un detalle de las quimeras que resulta que ya teníamos medido: las ventanas que caen
sobre la juntura son eficientes termodinámicamente pero **no tienen a quién pegarle**, porque
esa secuencia no existe en ningún gen. Lo dijo como advertencia —*«me puede decir que es el
mejor eficiente del mundo, pero si no va a encontrar su target (…) no va a ser»*— y la
respuesta está en `research/ola5/N4_quimeras/`: de las 240 ventanas de juntura de las doce
quimeras, 4 son eficientes y **ninguna de esas 4 tiene blanco continuo** `[M]`. Es la primera
vez en el proyecto que nos adelantamos a una observación suya en vez de absorberla.

Y hay un segundo hallazgo, que no salió de la reunión sino de revisarla contra el repositorio:
**los tres ejes de fenotipo que pidió ya tienen candidato en nuestro propio catálogo, los tres
en *Dalbulus maidis* y con la fuente leída completa.** `BicC` para reproducción, `V-ATPase D`
—el `ATPaseD_Dm` de la planilla— para letalidad, y `V-ATPase B` para alas, con **alas
deformes** como fenotipo reportado `[M]`. Las dos subunidades del mismo complejo se separan
justo por el eje que él nombró. Así que la quimera por fenotipos complementarios no arranca
con una búsqueda bibliográfica: arranca con una secuencia que hay que conseguir.

Sobre el único número que habíamos pedido —cuánta exposición asignarle a *Homalodisca
vitripennis*, el cicadélido norteamericano— **no dio un número, y conviene no inventarle
uno**. Dijo las dos cosas a la vez: que no está en la Argentina y *«puede no importar»*, y
que *«puede venir eventualmente»*. Lo que sí dejó claro es qué espera que hagamos con eso:
*«mostrar que esas posibles decisiones están presentes es como el extra»*. O sea que lo que
valora no es el valor del peso sino que la decisión esté explicitada y se vea su consecuencia
—que es, otra vez, lo que ya entrega `research/ola4/M5_dos_ejes/`.

Se comprometió a mandar **el transcriptoma de *Dalbulus maidis* en un zip**, con la
advertencia de que los identificadores no van a coincidir con ningún nombre conocido y que
hay que entrar por identidad u homología. Eso destraba la medición de conservación de `eth` y
`burs-alpha`, que estaba bloqueada por falta de ese insumo.

Y reiteró el criterio de evaluación del checkpoint 1, ahora con el código explícitamente
afuera: *«no te la voy a evaluar (…) en el sentido del código»*. Lo que evalúa es
*«el por qué lo hicieron, para qué lo hicieron, qué compararon, qué cosas medio biológicas
vieron»*.

---

## Transcripción por temas — lo que dijo el investigador

### El objetivo, como marco de todo

Abre recordando para qué es todo esto. `[E]` Lo que se quiere es que una molécula de ARN
genere, con la mayor precisión que se pueda predecir, fragmentos de 21 nucleótidos que
encuentren su blanco en la planta o en el insecto, lo corten y produzcan el efecto. El inciso
que mete al pasar es el que importa: *«con la mayor precisión que podamos predecir, que no lo
sabemos»*. Es la misma limitación que marcó en el checkpoint 1 —no hay dato empírico
suficiente— y la repite como encuadre, no como novedad.

### La región nueva, y el cicadélido que no está en la Argentina

`[R]` Sobre la propuesta de mover la región dentro del gen reacciona bien: *«está buenísima
la ventana esa»*. Reconstruye el argumento del equipo —se proponen ventanas nuevas porque son
más eficientes y porque los off-targets dieron mejor— y pasa al punto que le interesa, que es
el organismo no objetivo.

Dice algo que no sabíamos y que ordena la discusión: **ese insecto no estaba en su panel**.
*«El bicho ese yo no lo tenía.»* Lo describe como *«una chicharrita de Estados Unidos (…) que
no está en Argentina»* —es *Homalodisca vitripennis*— y confirma el hallazgo: la ventana que
estaba propuesta tenía muchas coincidencias con ese organismo.

> `[?]` La palabra exacta en esa frase no se resuelve: las tres pasadas del modelo dan
> «coincidencias», «eficiencias» y «exigencias». «Coincidencias» es la única que encaja con el
> resto de la frase y con lo que medimos, pero queda anotado que es lectura nuestra.

Y ahí deja la decisión abierta, a propósito y en voz alta, con los dos lados:

- *«Esa no está en Argentina, o sea que puede no importar.»*
- *«Puede venir eventualmente y tal vez si la querés matar.»*

`[R]` **No dio un número de exposición.** Lo que dio fue el criterio de qué hacer con la
ambigüedad: *«igual si vos querés ser específico para esta (…) mostrar que esas posibles
decisiones están presentes es como el extra que me parece»*. La lectura nuestra `[H]`: el
entregable no tiene que resolver el peso, tiene que mostrar que la decisión existe, que es
binaria y que mueve tres de las seis regiones recomendadas.

> **Nota de transcripción.** Un integrante pregunta si esos organismos eran «ortogonales»
> —casi seguro quiso decir **ortólogos**— y él corrige: *«ortogonales es otra cosa, como que
> era algo evolutivo»*. El sentido es que el valor de ese cicadélido en el panel es
> filogenético. Coincide con lo que D23 ya había declarado: entró como sustituto filogenético
> del resto de los Deltocephalinae. `[?]` La frase quedó entrecortada por diafonía.

### Qué evalúa, y qué no

`[R]` Acota de nuevo las expectativas, y esta vez saca el código del tablero de forma
explícita. *«Va a estar buenísimo lo que me muestres (…) no te la voy a evaluar (…) en el
sentido del código.»*

Lo que sí evalúa, enumerado por él:

1. **Por qué lo hicieron.**
2. **Para qué lo hicieron.**
3. **Qué compararon.**
4. **Qué cosas medio biológicas vieron.**

Y lo resume como *«ese mix entre la propuesta, el algo superador o lo que vos pensás que es
mejor, y el para qué»*. Es la misma regla del checkpoint 1 —se evalúa el razonamiento, no el
acierto— con un agregado útil: la comparación y la lectura biológica son parte del
razonamiento, no adorno.

### El transcriptoma: lo manda él

`[R]` Es el compromiso concreto de la reunión. Cuenta que otros equipos le preguntaron por el
transcriptoma y que **el que usan no está en NCBI**: *«no está, está en otro lado»*. Y se
ofrece: *«les mando el transcriptoma en un zip, que creo es chiquito, con el transcriptoma
que está publicado»*.

La advertencia operativa que agrega vale tanto como el archivo: `[R]` *«los IDs están hechos
por el que hizo el transcriptoma, no coinciden los nombres, no vas a poder encontrar, pero sí
por identidad o homología»*. O sea: el archivo no trae anotación utilizable por nombre, y la
única entrada es alineamiento.

### La ruta de homología para candidatos nuevos: validada otra vez

`[R]` El equipo le plantea que, como el genoma no está anotado, se podría buscar un genoma
mejor anotado y transferir la anotación por homología o BLAST. Responde *«totalmente»* y
desarrolla el circuito, que es el mismo del checkpoint 1 pero ahora apuntado al transcriptoma
que va a mandar:

1. Partir de un organismo mejor anotado y buscar ahí genes esenciales para ese insecto.
2. Hacer homología —BLAST— contra el transcriptoma de *D. maidis*.
3. El gen que aparece no tiene nombre útil; se lo asocia por parecido con el mejor acierto.
4. Ese gen pasa a ser un candidato nuevo para diseñar.
5. Se lo mete en la herramienta y se lo evalúa como a los demás.

Y explica por qué le parece valioso: `[R]` *«hiciste una búsqueda biológica, de contexto
biológico, y lo pusiste en el nuevo programita y chequeaste, y tal vez ese gen es mejor
porque tiene cero off-targets, genera mucho más eficientes según la fórmula»*.

### Los pesos: pide exactamente el barrido que ya está hecho

`[R]` Sobre la fórmula de decisión de eficiencia, baja el nivel de exigencia de «justificar el
número» a «mostrar la sensibilidad». Textual, con la estructura intacta:

> *«Mostrame qué cosas, qué características hiciste, cuál tiene más peso. O no: si probás un
> par de pesos distintos y cambia mucho, o todo medio parecido y en realidad tal vez esos
> pesos no importan tanto.»*

Y lo cierra con el argumento de por qué no hace falta más: *«al final, de vuelta, vas a tener
que ir a la planta y probar»*.

`[M]` Esto ya está medido dos veces y con más resolución de la que pide: el barrido de 2.000
sorteos de pesos de `research/ola2/W7_ranking/` y `research/ola3/C7_ranking_v2/`, y la grilla
de 4.368 configuraciones de `research/ola3/C9_sensibilidad_umbral/` y `research/ola4/M7_robustez_bicc/`.
El saldo es el que él anticipa como posible: para algunas afirmaciones los pesos no mueven
nada —seis de siete afirmaciones publicadas se sostienen entre el 96,0 % y el 100 %— y para
otras deciden todo —la comparación entre las dos regiones de `BicC_Dm` queda en 36,4 % a
75,6 % según el marco, que es una moneda al aire.

### Los conteos: el tema queda cerrado

`[R]` Un integrante le explica la diferencia entre 130 y 114 —la función que asigna 20
posiciones de cobertura a cada ventana de 21 nt— y él la acompaña sin corregir nada. No
reabre el tema.

`[M]` Es D62 y está reproducido con insumos propios en `research/ola5/N1_regla_de_conteo/`:
138, 40, 218 y 35 pasan a 114, 35, 199 y 33, los cuatro valores de la planilla, exactos.
Un integrante agrega que el ejercicio sirvió para dimensionar la incertidumbre, y él lo toma
como válido.

### `BicC_Dm` reduce población, no corta transmisión: lo confirma

`[R]` El intercambio más corto y el más importante para la recomendación. El equipo dice que
`BicC` probablemente apunte a disminuir la población; él contesta:

> *«Claro, porque tiene que ver con la oviposición, o sea, para que tenga hijitos.»*

> **Nota de transcripción.** En el turno del equipo una pasada transcribe «el `BicC`» y otra
> «el virus». La respuesta de él resuelve la ambigüedad sin margen: la oviposición es el
> fenotipo de `BicC` y no tiene nada que ver con los genes virales. Se lee `BicC`.

Y agrega, honestamente, que no sabe si eso cambia la decisión o no.

`[H]` Lo que esto vale: la distinción entre «reducir la población entre generaciones» y
«cortar la transmisión de la temporada» —que el equipo había puesto como el núcleo biológico
de `entregables/recomendacion-defendida.md`, no como una salvedad— queda confirmada por él.
Y su «no sé si cambia la decisión» es, leído de nuestro lado, la pregunta que seguimos
teniendo abierta: cuál de los dos objetivos manda.

### Quimeras por fenotipos complementarios: lo nuevo de la reunión

`[R]` Acá está el pedido que no estaba en ninguna carta ni en el checkpoint 1. Cuenta cómo lo
plantean ellos:

> *«En general, los planteos que hacemos nosotros son tratar de armar quimeras, justamente
> atacando genes que tengan distintas características.»*

Y da los tres ejemplos, que son tres mecanismos distintos y no tres genes cualesquiera:

| Eje | Ejemplo que dio | Efecto buscado |
| --- | --- | --- |
| reproducción | la oviposición del insecto | menos individuos en la generación siguiente |
| movilidad | *«algún gen que esté involucrado en las alas»* | *«si no tiene alas, por más que ande ahí, no importa»* |
| letalidad | *«otro que sea súper esencial, y que si no lo tiene se muere»* | mortalidad |

**Y los tres ejes ya tienen candidato en nuestro propio catálogo, los tres en la especie.**
Esto no estaba visto cuando terminó la reunión y es el hallazgo más útil de revisarla
`[M]` (`research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.md`):

| Eje que pidió | Gen | Fenotipo publicado en *Dalbulus maidis* |
| --- | --- | --- |
| reproducción | `BicC` (`DM-01`) | oviposición casi nula; el transcripto baja más de 170 veces al día 7 por inyección |
| **movilidad** | **`V-ATPase B` (`DM-02`)** | **alas deformes**, y además supervivencia del 16 % al día 4 contra 37 % del control de GFP |
| letalidad | `V-ATPase D` (`DM-03`, nuestro `ATPaseD_Dm`) | supervivencia del 18 % al día 4; **efecto en alas no significativo** |

`[H]` El dato que vuelve esto accionable: `V-ATPase B` y `V-ATPase D` son dos subunidades del
mismo complejo y se separan justamente por el eje que él nombró —la B deforma las alas y la D
no—, con la fuente leída completa (Jones, Bernal y Medina 2021). O sea que la quimera de
fenotipos complementarios no hay que salir a buscarla a la literatura: hay al menos una
combinación armable con lo que ya está en el catálogo, y es `BicC` —reproducción— con
`V-ATPase B` —alas y mortalidad—, que son exactamente los dos ejes que a `BicC_Dm` le faltan.

`[H]` La lectura: una quimera deja de ser un truco para juntar ventanas eficientes y pasa a
ser una forma de cubrir varios fenotipos con una sola molécula. Eso ataca de frente la
debilidad que el propio equipo declaró en `recomendacion-defendida.md` —que `BicC_Dm` tiene
el mejor perfil de riesgo pero un fenotipo que no bloquea transmisión, mientras que la
V-ATPasa tiene mortalidad por ingesta pero peor perfil de off-target—. Una quimera de los dos
ejes es, en su marco, la respuesta natural a esa tensión. **No lo dijo él de esa forma**: la
combinación de su idea con nuestro problema es nuestra.

### La juntura de las quimeras: la advertencia que ya teníamos medida

`[R]` Sigue sobre quimeras y mete el detalle técnico, que presenta como el diferencial
posible. Reconstruido:

Cuando se pegan dos regiones, al calcular eficiencia a lo largo de la molécula el programa
sigue dando valores también en la zona de empalme. Pero esas ventanas son secuencia nueva:
*«biológicamente, una molécula que se genera acá, ¿a quién le va a pegar? A este, a este, a
ninguno. No va a encontrar.»* Y la moraleja general, que es la frase más citable de la
reunión:

> *«Me puede decir que es el mejor eficiente del mundo, pero si no va a encontrar su target en
> la planta o en el insecto, no va a ser.»*

Lo encuadra como *«los detalles que está bueno tener en cuenta y que pueden dar un
diferencial»*.

`[M]` **Esto ya está medido**, en `research/ola5/N4_quimeras/`: de las 240 ventanas de juntura
de las doce quimeras evaluadas, **4 son eficientes y ninguna de esas 4 tiene blanco continuo
de 21 nt** en ninguno de los cuatro genes; y las 8 que sí tienen blanco son todas de los
extremos de la unión y ninguna es eficiente. Más la contabilidad que lo explica: una quimera
no agrega ventanas, **canjea** los veinte arranques de la cola de cada fragmento por veinte de
juntura. Es decir: su advertencia es correcta, está cuantificada, y el número de ventanas
eficientes de una quimera cuenta como válidas unas ventanas que no pueden silenciar nada.

> `[?]` Un tramo de esta explicación (06:25–06:30) quedó con diafonía y la frase
> *«estaría bueno tenerlas, ¿para qué tengo que hablar con ellos?»* no se entiende. Por el
> contexto parece ser «para que lo hablemos», pero no se reconstruye con confianza.

### Cierre

No trajo preguntas propias. Quedó abierto el canal de correo para lo que falte, y el
compromiso de mandar el transcriptoma.

---

## La propuesta del equipo — audios 1, 2, 4 y 5

`[H]` **Todo esto es del equipo, no del investigador.** Es la idea de un compañero sobre cuál
debería ser el producto final del Investigathon, grabada después de la reunión. Se resume acá
porque es una decisión de alcance que hay que tomar, no porque sea una indicación recibida.

La propuesta es **cerrar un pipeline completo dentro de la plataforma**, de transcriptoma a
diseño, en cuatro pasos:

1. **Subir un transcriptoma** del insecto o del patógeno a la plataforma.
2. **Categorizar los genes con un modelo de lenguaje** para saber qué hace cada uno y cuáles
   pueden servir como blanco. Es la parte más nueva y la más discutible (ver abajo).
3. **Correr lo que ya está hecho** sobre los genes elegidos: eficiencia, ventana óptima,
   off-targets.
4. **Generar quimeras** dentro de la misma plataforma.

Y una rama para el caso de que no se tenga el transcriptoma del organismo objetivo: si se
tiene el de un organismo parecido, llegar al gen blanco **por homología**. El audio 5 lo
cierra con el argumento de producto: *«mientras el razonamiento biológico esté bien, si
cerramos ese pipeline sin baches ni errores (…) es un buen producto final para este atón»*.

**Qué de esto ya existe y qué no**, para que la discusión sea sobre lo que falta:

| Paso de la propuesta | Estado real |
| --- | --- |
| Motor de eficiencia, ventana óptima, perfil | `[M]` existe y está verificado contra el original: `tools/sifi21_port/` y `sifi_plus/` |
| Off-targets contra panel de no objetivo | `[M]` existe: panel de seis, alertas con cuatro campos (D48) |
| Quimeras | `[M]` existe la evaluación, incluida la juntura: `research/ola5/N4_quimeras/` |
| Candidatos nuevos por homología | `[M]` existe como circuito y como catálogo: `pipeline/` y `research/ola3/C5_*/catalogo_genes_blanco.md` |
| Subir un transcriptoma y correr todo encadenado | `[H]` no existe como flujo único; las piezas están sueltas |
| Categorizar genes con un modelo de lenguaje | `[H]` no existe, y es la pieza que hay que mirar con cuidado |

`[H]` **La objeción que corresponde hacerle al paso 2**, y que conviene tener resuelta antes
de ponerlo en un entregable: usar un modelo de lenguaje para decidir qué gen es esencial
produce afirmaciones sin fuente verificable, que es exactamente lo que las reglas del
proyecto prohíben y lo que el investigador dice que evalúa —*«qué cosas medio biológicas
vieron»*—. La versión defendible del mismo paso es la que él validó en la reunión: la
anotación se transfiere **por homología contra un organismo mejor anotado**, con la identidad
del alineamiento como evidencia, y la literatura sostiene la esencialidad del gen en el
organismo de origen. Un modelo de lenguaje puede servir para **ordenar y resumir** esa
evidencia; no para generarla. Dicho de otro modo: el paso 2 ya tiene una versión con
evidencia, y es la que hay que construir.

---

## Qué pide el investigador, y qué tenemos

Esta es la tabla que decide el trabajo que queda. «Pedido» incluye lo que pidió explícitamente
y lo que ofreció mandar.

| # | Lo que salió de la reunión | Qué hay ya | Qué falta |
| --- | --- | --- | --- |
| 1 | **Quimeras por fenotipos complementarios** (reproducción + alas + letalidad) | `[M]` la maquinaria de quimeras y su evaluación, incluida la juntura (`N4`); y el catálogo (`C5`) **ya tiene un gen de cada uno de los tres ejes**, los tres en *D. maidis* (ver abajo) | **Lo único realmente nuevo**, y es menos de lo que parecía: falta armar las combinaciones y evaluarlas. Los candidatos ya están |
| 2 | **No contar las ventanas de juntura como si silenciaran** | `[M]` medido y cuantificado: 4 de 240 eficientes, ninguna con blanco (`N4`) | Nada de medición. Falta que el entregable lo **presente**: hoy está en un REPORT y él lo señaló como diferencial |
| 3 | **Mostrar la sensibilidad a los pesos** | `[M]` 2.000 sorteos (`W7`, `C7`) y 4.368 configuraciones (`C9`, `M7`, `N3`) | Nada. Está hecho con más resolución de la que pidió |
| 4 | **Que la decisión sobre el no objetivo esté explicitada**, no resuelta | `[M]` los dos ejes separados y el efecto medido: con exposición cero se mudan tres de las seis regiones (`M5`) | Nada de medición. Sigue sin número de él, y **ya no conviene esperarlo**: dijo las dos cosas |
| 5 | **El transcriptoma de *D. maidis*, en zip** | — | **Depende de él.** Cuando llegue: medir conservación de `eth` y `burs-alpha` (la línea `C11`, bloqueada por este insumo) y verificar las posiciones de la planilla |
| 6 | **Candidatos nuevos por homología contra ese transcriptoma** | `[M]` el circuito está corrido y hay catálogo (`pipeline/`, `C5`) | Rehacerlo contra el transcriptoma que mande, que es el que usa el laboratorio |
| 7 | **El razonamiento, no el código** | `[M]` todo el material está escrito como razonamiento con fuente | Nada. Confirma el formato que ya se eligió |
| 8 | **La lectura de `BicC_Dm` como gen poblacional** | `[M]` es la tesis de `recomendacion-defendida.md` §1 y §3 | Nada. Queda confirmada por él |

**El saldo, en una línea:** de ocho puntos, **cinco ya están cerrados**, uno depende de un
archivo que él tiene que mandar, uno es de presentación y **uno solo es trabajo nuevo** —las
quimeras por fenotipos complementarios—.

### Lo que conviene hacer para cerrar

> Esto es el resumen. El plan ejecutable, con una tarea autocontenida por pendiente y la
> separación entre lo que se puede hacer ya y lo que espera el transcriptoma, está en
> [`docs/plan_cierre/PLAN_CIERRE.md`](../../docs/plan_cierre/PLAN_CIERRE.md).

En orden, y con el criterio de que lo barato y de alto impacto va primero:

1. **Subir la juntura al entregable.** Está medido y él lo nombró como diferencial; hoy vive
   en un REPORT de la ola 5. Es mover un resultado de lugar, no producirlo.
2. **Armar la quimera `BicC` + `V-ATPase B` y evaluarla.** Los dos genes ya están en el
   catálogo con fenotipo publicado en la especie y cubren los tres ejes que pidió. Se evalúa
   con la maquinaria que ya existe, contando la juntura aparte. Es la única línea de cómputo
   nueva, y el insumo que parecía faltar no falta. `V-ATPase B` necesita que se le consiga la
   secuencia, que es el único paso previo.
3. **Cuando llegue el zip:** `C11` —conservación de `eth` y `burs-alpha`— y la verificación de
   las posiciones de la planilla contra ese transcriptoma.
4. **Dejar escrito que la exposición de *H. vitripennis* no tiene número y no lo va a tener**,
   con las dos frases suyas y la consecuencia medida al lado. Deja de ser un pendiente
   bloqueante y pasa a ser una decisión declarada, que es lo que él pidió.

---

## Calidad de la transcripción

El audio del investigador tiene diafonía constante: hay varias personas en la sala, se
superponen, y el modelo parte las frases en segmentos de dos o tres palabras. El contenido se
entiende, pero la segmentación no sirve para citar por tiempo con precisión. Las correcciones
sistemáticas aplicadas:

| En el audio | Lo correcto |
| --- | --- |
| «soft targets» | **off-targets** (el mismo error del checkpoint 1) |
| «trastectoma», «trangéptoma», «trascendentoma» | **transcriptoma** |
| «el BIC», «región del VIXE» | **`BicC`** |
| «cero targets» | **cero off-targets** |
| «ortogonales» (pregunta del equipo) | casi seguro **ortólogos**; él corrige y habla de parentesco evolutivo |
| «programita» | la herramienta propia del equipo (`sifi_plus` / el port) |
| «Delta G» | energía libre (ΔG) |
| «hortogonales» | **ortólogos** (pregunta del equipo) |
| «transportador» (03:48) | **transcriptoma** |

**Se corrió una segunda pasada** con decodificación por haz de 5 sobre el audio del
investigador, y todas las citas de este documento se verificaron contra ella. La primera
pasada con haz colapsó en un bucle de «Sí» a partir de 02:19 —el modo de repetición típico
cuando el modelo se condiciona al texto previo con audio ruidoso— y se repitió desactivando
ese condicionamiento. Las dos pasadas coinciden en todo lo sustantivo; las tres divergencias
quedaron anotadas donde aparecen.

Tramos con pérdida real de contenido, todos por diafonía: **01:50–01:56** (*«vaya que no te
voy a hablar tampoco de lo biológico»*, incoherente), **02:20–02:30** (varias voces a la vez
mientras se habla del candidato), **06:25–06:30** (*«¿para qué tengo que hablar con ellos?»*,
la frase de cierre sobre la juntura, igual de incomprensible en las dos pasadas) y
**07:00–07:16** (el cierre informal). `[?]` Si alguno de esos tramos importa, hay que volver
al audio.

Los cuatro audios del compañero son nota de voz limpia, con un solo hablante, y se
transcribieron sin problemas salvo la palabra «transcriptoma», que el modelo nunca acierta.

---

## Pendientes que salen de esta reunión

Para `00_meta/PREGUNTAS_ABIERTAS.md`:

1. **El transcriptoma en zip.** Es el único insumo comprometido. Mientras no llegue, `C11`
   sigue bloqueada. Si no llega en un par de días, conviene recordárselo por correo: lo
   ofreció él.
2. **Qué objetivo manda: cortar transmisión en la temporada o bajar población entre
   generaciones.** Sigue abierta. Él confirmó la lectura del fenotipo de `BicC` y dijo
   explícitamente que no sabe si eso cambia la decisión. `[?]`
3. **La secuencia de `V-ATPase B` de *D. maidis*.** Es el candidato del eje de movilidad
   —alas deformes, `DM-02`— y lo tenemos con fenotipo pero **sin secuencia** en el panel de
   trabajo. Es el único insumo que bloquea la quimera de fenotipos complementarios, y puede
   salir del transcriptoma que él va a mandar. `[?]`
4. ~~La exposición de *Homalodisca vitripennis*.~~ **Se cierra como pregunta al investigador.**
   No va a dar un número: dijo que el organismo no está en la Argentina y que *«puede no
   importar»*, y también que *«puede venir eventualmente»*. Lo que pidió es que la decisión
   esté explicitada. Pasa de pendiente a decisión declarada del equipo.
5. **Si una complementariedad incompleta da actividad en las ventanas de juntura.** No la
   preguntamos y él no la tocó; sigue siendo el límite declarado de `N4`. `[?]`

Para `00_meta/DECISIONS.md`, quedan al menos dos decisiones a formalizar: que la exposición
del no objetivo se declara como decisión abierta con su consecuencia medida en vez de
esperarle un número, y que las quimeras pasan a evaluarse por **combinación de fenotipos** y
no sólo por densidad de ventanas eficientes, con la juntura contada aparte.

Para `00_meta/CAMINOS_PROBADOS.md`: el paso de «categorizar genes con un modelo de lenguaje»
de la propuesta del equipo, con el motivo por el que se reemplaza por la transferencia de
anotación por homología —que es la versión que el investigador validó y la única que deja
evidencia verificable.
