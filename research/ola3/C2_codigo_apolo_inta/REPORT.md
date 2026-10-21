# C2 — El código de sifi21INTA y Apolo Rocket, leído y corrido

Ola 3, a partir del Checkpoint 1. Fecha: 2026-10-20. Repositorios leídos y corridos en
`work/C2/`, fuera del control de versiones. Entregables de esta carpeta:
[`diff_sifi21INTA_vs_original.md`](diff_sifi21INTA_vs_original.md) (Q1),
[`apolorocket_arquitectura.md`](apolorocket_arquitectura.md) (Q3),
[`corridas/`](corridas/README.md) (los comandos y las salidas reales),
[`repos_inventario.json`](repos_inventario.json), `sources.json` y `NOTAS_PARA_META.md`.

---

## Las tres respuestas

**Q1 — Qué cambió sifi21INTA respecto de si-Fi21.** Mucho de forma y una sola cosa de química.
La forma: de una aplicación Qt4 de Python 2.7 a una librería de Python 3 con clases, sin interfaz,
con anotación por GFF3 y figuras de Plotly. La química: **cambiaron la tabla de vecinos más
cercanos (nearest neighbours), de `RNA_NN3` (Chen et al. 2012) a una tabla nueva que el comentario
del código atribuye a Zuber et al. 2022** (`freeEnergy.py:306`, tabla en `:61-74`, contra
`free_energy.py:278` del original). Es el único parámetro termodinámico que se tocó. Además
cambiaron **qué cuenta la fila «Efficients»**: el original contaba un registro por hit de Bowtie
(`general_helpers.py:113`) y sifi21INTA cuenta una fila por ventana (`SifiPipeline.py:430-448`), y
agregaron una columna nueva de eficientes sin off-targets. Todo lo demás del criterio —las tres
condiciones termodinámicas, los umbrales 1,0 y 0,1, la ventana u=8, los 21 nt, los 22 °C, los
parámetros de RNAplfold y de Bowtie— está igual, **incluida la rama de la regla terminal que
devuelve «eficiente» sin mirar la termodinámica**, transcrita literal en `Sirna.py:66-96`. `[E]`
El diff completo, archivo por archivo y línea por línea, con el efecto medido de cada diferencia,
está en [`diff_sifi21INTA_vs_original.md`](diff_sifi21INTA_vs_original.md).

**Q2 — ¿Reproduce los 114, 35, 199 y 33? No.** Corrido sobre las cuatro secuencias completas con
todos sus valores por defecto, con RNAplfold 2.7.2 y bowtie 1.3.1 locales, sifi21INTA da
**138, 40, 218 y 35**, contra los 114, 35, 199 y 33 de la planilla. No falla por poco y no falla
parejo. Tres cosas más, todas medidas: forzando la tabla de energía del original, sifi21INTA da
**142, 39, 223 y 35**, que es **exactamente lo mismo que nuestro port en modo fiel, ventana por
ventana, en las 4.722 ventanas y en los cinco términos del veredicto**; un barrido de 22.176
configuraciones de la propia librería **no encuentra ninguna** que dé los cuatro conteos, y lo que
más se acerca —error 4 sobre 381— es subir el umbral de estabilidad de extremos de 1,0 a **1,75**,
que da 117, **35**, **199** y 32; y la base de datos **no explica nada**, porque en esta librería
el conteo de eficientes es por ventana y medimos que no se mueve ni una unidad contra tres bases
distintas. `[E]` Los comandos y las salidas están en [`corridas/`](corridas/README.md).

**Q3 — Qué hace Apolo Rocket por dentro.** Diecinueve funciones de Python que reciben un JSON y
devuelven rutas de archivos, sobre PostgreSQL, Bowtie 1 y ViennaRNA, en tres pasos: blancos
principales, eficiencia y off-targets. **El motor de eficiencia es el criterio de si-Fi21: `Sirna.py`
y `freeEnergy.py` son los mismos archivos que en sifi21INTA** —`freeEnergy.py` tiene el mismo md5—,
con la tabla de Zuber 2022 por defecto y con el bypass de la regla terminal intacto. Tres hallazgos
que importan para nosotros: **no hay ningún puntaje ni ningún orden** —lo único ordenable es el
número de blanco, que es orden de inserción—; **la eficiencia no se guarda por siRNA sino como la
curva del gráfico** (`efficiency_data INT[]`), de modo que no se puede auditar qué ventana fue
eficiente; y el parámetro `method` está documentado como «'sifi21' or 'IA'» y viaja a la base, pero
**no hay ninguna implementación del método «IA»** en el repositorio. El detalle, con los endpoints,
el esquema y el criterio de off-target, está en
[`apolorocket_arquitectura.md`](apolorocket_arquitectura.md). `[E]`

### Los cuatro números, todos juntos

| Gen | Planilla EPILAB | si-Fi21 original (W5, RNAplfold 2.1.5) | sifi21INTA, defaults (2.7.2) | sifi21INTA con `RNA_NN3` = nuestro port fiel (2.7.2) | Mejor configuración del barrido |
|---|---|---|---|---|---|
| `MP_MRFV` | 114 | 133 | **138** | 142 | 117 |
| `CP_MRFV` | 35 | 32 | **40** | 39 | **35** |
| `BicC_Dm` | 199 | 212 | **218** | 223 | **199** |
| `ATPaseD_Dm` | 33 | 42 | **35** | 35 | 32 |
| Error acumulado | — | 44 | 50 | 58 | **4** |

**Advertencia de comparabilidad, y es importante:** las columnas no son todas comparables entre sí.
La del programa original se midió con RNAplfold 2.1.5, el que trae el instalador de si-Fi; en esta
máquina sólo hay 2.7.2, y W5 ya había medido que las dos versiones difieren en varios eficientes por
gen. Las columnas de sifi21INTA y del port **sí** son comparables entre ellas, porque usan el mismo
RNAplfold. Con 2.1.5 no se pudo correr sifi21INTA, y eso queda como vacío declarado. `[E]`

---

## ¿Son éstos los repositorios del laboratorio?

Hay que separar dos afirmaciones que es fácil mezclar.

**Que estos dos repositorios son el código público del grupo que mantiene la reescritura de si-Fi21
y el backend de Apolo Rocket: confirmado.** `[E]` El repositorio `apolorocket` se describe a sí
mismo como «backend endpoints for apolorocket application to predict siRNAs», su PDF de
documentación se titula «Documentación endpoints de aplicación ApoloRocket» y apunta a su propia URL
de GitHub, y el código es un derivado demostrable de si-Fi21: `freeEnergy.py` tiene 423 de 431
líneas idénticas al `free_energy.py` del original y la regla terminal está transcrita rama por rama.
Los dos repositorios están en la cuenta de bioinformática del INTA, y R3 ya había registrado `[R]`
que la plataforma se construyó con el IABIMO (INTA-CONICET) y la Fundación Sadosky; la constante
`REFERENCEDIR` y todos los `outputDir` de ejemplo del PDF cuelgan de un directorio llamado
`sadosky` (`constants.py:11`). La pista del orquestador era correcta.

**Que el laboratorio del investigador corrió este código para llenar la planilla de EPILAB: sigue
siendo hipótesis, y nuestras mediciones la debilitan.** `[H]` Nadie lo confirmó. En los dos
repositorios no aparece ni una vez *Dalbulus maidis*, ni maíz, ni MRFV, ni EPILAB: los datos de
ejemplo son *Arabidopsis thaliana*, *Oryza sativa*, *Homo sapiens*, *Drosophila melanogaster* y
*Botrytis cinerea*, y el único dato de prueba de sifi21INTA es una quitina sintasa de *Diaphorina
citri* contra un índice del genoma de ese psílido —un hemíptero vector, que es el único indicio de
que el grupo aplica esto a insectos plaga—. Y sobre todo: **con sus valores por defecto este código
da 138, 40, 218 y 35, que está más lejos de la planilla que el propio si-Fi original**, aunque la
comparación esté confundida por la versión de ViennaRNA. Si el laboratorio usó esta librería, usó
además otros parámetros. `[E]`

Lo que sí cerramos con medición: **la hipótesis de la base de datos ya no sirve como explicación si
el laboratorio corrió esta librería.** En sifi21INTA el conteo de eficientes es por ventana y es
invariante a la base; lo verificamos contra los cuatro genes, contra los 71 registros públicos de
MRFV y contra el transcriptoma TSA GITV01 de *D. maidis*: 138, 40, 218 y 35 en los tres casos. Lo
que sí cambia es la columna nueva, «eficientes sin off-targets», que para `ATPaseD_Dm` contra el
transcriptoma cae de 35 a 12, para `BicC_Dm` cae de 218 a 214 contra ese mismo transcriptoma, y
para los genes virales contra los aislados de MRFV cae a 0. Ninguno de esos valores es el de la
planilla. `[E]`

---

## Q1 en detalle: qué cambió, y cuánto mueve cada cosa

La tabla completa, con archivo y línea de los dos lados, está en el documento aparte. Acá van las
tres diferencias que mueven un número, y una que no mueve ninguno pero vale la lectura.

**La tabla de energía nueva es el cambio químico, y es chico.** Medida sobre las cuatro secuencias,
con todo lo demás igual, mueve los conteos **−4, +1, −5 y 0**: 142→138, 39→40, 223→218 y 35→35.
Cambian 14 ventanas, 3 hacia eficiente y 11 hacia no eficiente, y **ninguna** de las 14 cae en la
rama del bypass de la regla terminal, que es la rama que no mira la termodinámica. Es decir: la
tabla de energía cambia el veredicto exactamente donde el veredicto depende de la energía, como
tiene que ser. `[E]` Que cambie en las dos direcciones es interesante, porque la planilla también
difiere en las dos direcciones respecto del original; pero el tamaño no alcanza ni de lejos.

**El conteo pasó a ser por ventana.** En el original, `general_helpers.py:113` arma un `Counter`
sobre los registros JSON, y hay un registro por hit de Bowtie en hebra +; en sifi21INTA,
`getResultSummary` recorre el diccionario de siRNA. La diferencia se ve en `BicC_Dm`, donde Bowtie
reporta 2.504 hits y el resumen dice 2.500 ventanas: son los dos pares de 21-meros repetidos dentro
del gen que W5 ya había identificado. `[E]`

**La temperatura no cambió, y sigue sin ser parámetro.** Los 22 °C siguen fijos en dos lugares
independientes (`freeEnergy.py:446` para el ΔG y `SifiPipeline.py:56` para RNAplfold) y ninguno es
argumento del constructor. Forzando el atributo medimos que a 25 °C los cuatro conteos **suben** a
146, 45, 231 y 40, o sea que la temperatura se aleja de la planilla si se la sube con el umbral por
defecto. `[E]`

**Y lo que no cambió y conviene decir en voz alta:** la rama de la regla terminal que devuelve
«eficiente» mirando sólo la accesibilidad sigue ahí, en `Sirna.py:75-82`, igual que en
`sifi_pipeline.py:535-541`. Es el defecto C1 de nuestro `CAMBIOS.md`, el que infla entre el 14 % y
el 24 % de los eficientes. **No lo corrigieron, y nosotros no somos los únicos que lo vimos:** el
fork `rj-price/siFi-2.0`, una reescritura independiente de agosto de 2026, también lo conserva y lo
documenta como comportamiento del original a preservar (`src/sifi2/efficiency.py:148-158`). Tres
implementaciones, el mismo bypass. `[E]`

---

## Q2 en detalle: qué se midió y qué quedó descartado

Cinco corridas, todas con su comando y su salida en [`corridas/`](corridas/README.md).

La **primera** es la respuesta a la pregunta: defaults, 138, 40, 218 y 35, terminó bien, no está
vacía. La **segunda** aísla la tabla de energía. La **tercera** es la que da confianza en las otras:
nuestro port en modo fiel y sifi21INTA con la tabla vieja coinciden en las 4.722 ventanas, en
selección de hebra, estabilidad de extremos, accesibilidad, valor de accesibilidad y veredicto
final, con cero diferencias. Son dos implementaciones independientes del mismo criterio, escritas
sin conocerse, y dan lo mismo: eso cierra la duda de si nuestro port era fiel. `[E]`

La **cuarta** mide la base de datos, y es la que cierra una hipótesis abierta del proyecto. La
**quinta** es el barrido: 22.176 configuraciones de los parámetros que la propia librería expone
—tabla de energía, temperatura de plegado, ventana de accesibilidad, umbral de extremos, umbral de
accesibilidad y regla terminal—, calculadas con las funciones del paquete y evaluadas vectorizado,
con la evaluación verificada contra la salida real del paquete en ocho casos antes de usarla.
**Ninguna reproduce los cuatro conteos.** La mejor, con error acumulado 4 sobre 381 siRNA
declarados, es la tabla del original a 22 °C con u=8 y accesibilidad 0,1 pero **umbral de extremos
1,75**: da 117, 35, 199 y 32, con dos de los cuatro exactos. La segunda mejor, error 6, es la tabla
nueva a 25 °C con umbral 2,0: 113, 36, 201 y 31. `[E]`

Esto refuerza, con otra implementación, lo que W5 ya había encontrado barriendo nuestro port: **lo
que acerca los conteos a la planilla no es la química, es el umbral de estabilidad de extremos**.
Que dos barridos independientes, sobre dos implementaciones distintas, apunten al mismo parámetro es
el resultado más accionable de esta investigación: convierte la pregunta abierta «qué parámetros
cambiaste» en una pregunta cerrada, «¿pusiste el umbral de extremos en 1,75 o en 2,0 en vez de
1,0?», que el investigador puede contestar en diez segundos. `[H]` sobre su respuesta; `[E]` sobre
la medición.

**Lo que depende de datos que no tenemos.** Ninguna de las dos librerías necesita una base de datos
para el conteo de eficientes, así que nada quedó bloqueado por eso. Lo que sí faltó es **RNAplfold
2.1.5**, el que trae el instalador de si-Fi: sin él no se puede comparar sifi21INTA contra la
corrida del programa original de W5 en igualdad de condiciones. Queda como vacío declarado, y es
barato de cerrar para quien tenga la instalación de Windows.

---

## Licencias: qué implica el GPL-3.0, y un conflicto que ya estaba anotado

Los dos repositorios del INTA traen el texto completo de la **GNU GPL versión 3** como archivo
`LICENSE` (idéntico en los dos, md5 `1ebbd3e34237af26da5dc08a4e440464`), y la API de GitHub los
reporta como `GPL-3.0`. `[E]` Esto no es asesoría legal, es una advertencia con fuente, y tiene tres
consecuencias prácticas.

La primera es que **leer el código para entender el algoritmo no contamina nada**. Lo que el
copyleft alcanza es la distribución de obras derivadas: si publicáramos algo que incorpora,
traduce o transcribe de cerca esos archivos, el conjunto tendría que distribuirse bajo GPL-3.0. Por
eso el código de terceros quedó en `work/C2/`, fuera del repositorio versionado, y por eso en estos
documentos se cita archivo y línea y se parafrasea en vez de copiar.

La segunda es que **nuestro port no hereda nada de esto**, porque no deriva de sifi21INTA sino del
fuente de `snowformatics/siFi21-`, y su linaje está documentado en `tools/sifi21_port/CAMBIOS.md`
desde antes de que leyéramos los repositorios del INTA. Lo que sí hay que cuidar de acá en adelante
es no transcribir nada de lo que acabamos de leer: la coincidencia ventana por ventana que medimos
es una coincidencia de resultados, no de código.

La tercera es el conflicto que el proyecto ya tenía anotado como `[?]` y que ahora tiene una fuente
abierta: **el si-Fi21 original no está bajo GPL**. Su repositorio no trae archivo de licencia y su
README declara, en la línea 19, una licencia Creative Commons Attribution-NonCommercial-ShareAlike
2.0 Generic. `[E]` Una licencia con cláusula no comercial y con *share alike* no es compatible con
relicenciar un derivado bajo GPL-3.0, que explícitamente permite el uso comercial. O sea que la
cadena licencia del original → derivado del INTA **tiene una inconsistencia declarada en las propias
fuentes**, y no la resolvemos acá: la dejamos anotada por si alguna vez se publica algo. Nota al
margen que la complica más: la parte más copiada, `free_energy.py`, es a su vez una copia de
`Bio.SeqUtils.MeltingTemp` de Biopython, que tiene su propia licencia. `[?]`

---

## Crítica del código y puntos de enganche

El investigador pidió explícitamente la crítica de las herramientas aunque no las mejoremos. Lo que
sigue sale de leer el código y, donde dice «medido», de correrlo.

**Lo que está mal y cambia un resultado.** El bypass de la regla terminal, ya descrito, es el
primero. El segundo es nuevo y lo medimos acá: **una secuencia en minúsculas produce cero
eficientes, en silencio**. `createSirnas` llama a `sequence.upper()` sin asignar el resultado
(`SifiPipeline.py:163`, y lo mismo en `apolorocket/inputOutputFunctions.py:42`), y como la regla
terminal compara contra literales en mayúscula, ninguna ventana entra por ninguna rama. Medido sobre
`MP_MRFV_full`: 138 eficientes en mayúsculas, **0 en minúsculas**, con Bowtie alineando igual las
1.243 ventanas, de modo que la corrida parece exitosa. `[E]` En una plataforma web que recibe la
secuencia como texto en un JSON, eso es un resultado erróneo servido con cara de resultado válido.
Se arregla con una línea.

**Lo que está mal y no cambia el conteo pero sí el gráfico.** La curva de eficientes cubre 20 de las
21 posiciones de cada siRNA (`SifiPipeline.py:311`, `figuresFunctions.py:168`), mientras que el
original cubría las 21 (`show_plot.py:237`). Se ve en los datos guardados de Apolo Rocket: la suma
de la curva dividida por 20 da entero exacto en las dos filas del volcado. `[E]`

**Lo que es arbitrario o manual.** La elección del blanco principal sigue siendo una decisión humana
sin registro: `input()` por consola en sifi21INTA, una lista de números en el JSON de Apolo Rocket.
De esa decisión depende por completo la columna de eficientes sin off-targets, que es la única que
mira especificidad. La elección de la región también es humana y, en Apolo Rocket, **no se valida**:
el volcado de ejemplo contiene una consulta con región «800-100» y secuencia de largo cero,
insertada igual en la base. `[E]` Y el criterio de off-target sigue siendo desapareamientos ciegos a
la posición, con el agravante de que al fusionar alineamientos en bloques los desapareamientos se
**suman** (`figuresFunctions.py:39`), así que la columna de desapareamientos de la tabla no
significa lo que su nombre dice.

**Lo que es frágil como software.** `freeEnergy.py:384` usa `Bio.SeqUtils.GC`, que Biopython eliminó
en la versión 1.82: con Biopython actual el paquete **aborta**, y hubo que instalar 1.81 para
correrlo (medido). `databaseFunctions.py:202` hace `eval()` sobre un campo de texto de la base que
proviene de un GFF3 de usuario. `constants.py:11-16` trae en claro el nombre de la base, el usuario,
la contraseña, el host y el puerto, además de una ruta absoluta con un directorio personal —no
reproducimos los valores, pero están en el repositorio público y conviene que lo sepan—. Y en modo
off-target sin ningún alineamiento, `bowtieFigure` devuelve una variable que nunca se asignó, así
que `offTargetPipeline` (`SifiPipeline.py:120-155`) termina en `UnboundLocalError`; leído, no
corrido. `[E]`

**Lo que no está, y es el hueco.** No hay priorización. No hay score, ni orden, ni umbral de corte,
ni función de agregación en ninguno de los dos repositorios; la salida es «acá están las ventanas
eficientes y acá los alineamientos», y la decisión queda del lado del humano. R3 había inferido esto
de la prensa; el código lo confirma más fuerte. Y en el esquema de la base está el lugar donde
enchufarlo, con nombre y todo: la columna `method` de la tabla `efficiency`, documentada como
«'sifi21' or 'IA'», sin implementación. `[E]`

**Qué propondríamos, sin implementarlo.** Persistir el veredicto por ventana con sus cinco términos
en vez de sólo la curva —es una tabla más y habilita auditar, rankear y recalcular sin volver a
correr—; ponderar los desapareamientos por posición en el tamizaje de off-targets, separando la
región semilla (nt 2-8) y las posiciones catalíticas 10-11 del resto; normalizar mayúsculas y
validar coordenadas en la entrada; exponer la temperatura como parámetro, porque el veredicto
depende de ella y hoy está fija en dos lugares distintos; y, para el gancho `IA`, que un modelo
devuelva un puntaje por ventana en vez de un booleano, lo que exige cambiar el tipo de
`efficiency_data` pero no el resto del esquema. Ninguna de estas cinco cosas la implementamos:
D7/D8 dice que nuestro aporte es la priorización auditable, no mejorar herramientas ajenas.

---

## Inventario de repositorios

El detalle está en [`repos_inventario.json`](repos_inventario.json), con commit, licencia, fechas y
si se leyó o no. En resumen: los dos repositorios del INTA leídos y uno de ellos corrido; el
original de `snowformatics` en el commit `d6296b7`, que es el que cita nuestro `CAMBIOS.md` y que
verificamos como cabeza actual de `master`; y los ocho forks del original, de los cuales **seis no
tienen ningún cambio propio** —su cabeza es un commit de la historia de upstream, verificado con
`git ls-remote` contra la lista de commits de la API— y dos sí: `dakilaledesma/siFi21-`, que es una
migración mecánica a Python 3 y PyQt5 sin tocar el criterio, y `rj-price/siFi-2.0`, que es una
reescritura completa de agosto de 2026 con CLI y tests que preserva la numérica del original a
propósito. De la cuenta `ApoloBiotech` se confirmó que tiene un solo repositorio público y que no es
de siRNA. `[E]`

Buscando otros repositorios públicos relevantes aparecieron dos que conviene que el equipo sepa que
existen. **`DanielHarley/zeaguard-drylab`**, con push del 2026-10-15, se describe a sí mismo como un
espacio de trabajo computacional para diseñar y evaluar dsRNA contra *Dalbulus maidis*, con Bicaudal
C y dsRNase-2 como blancos y las parálogas dsRNase-1 y dsRNase-3 como referencia de especificidad:
es el mismo problema, el mismo gen y el mismo ensamblado TSA que estamos usando nosotros, y no
menciona si-Fi ni Apolo Rocket. **`MaxiSack/RNAival`**, GPL-3.0, con push del 2026-10-19, es un
programa de Python con interfaz gráfica para identificar candidatos de siRNA y evaluar el
procesamiento de dsRNA. De los dos se leyó sólo el README; ninguno se corrió. `[E]`

---

## Preguntas para el investigador

Todas salen del código y todas son baratas de contestar.

1. **¿Corriste sifi21INTA, Apolo Rocket, o el si-Fi21 original de Windows?** Con los defaults, esta
   librería da 138, 40, 218 y 35; el programa original da 133, 32, 212 y 42; tu planilla dice 114,
   35, 199 y 33.
2. **¿Subiste el umbral de estabilidad de extremos?** Con 1,75 en vez de 1,0, y todo lo demás por
   defecto, salen 117, **35**, **199** y 32: dos de los cuatro exactos. Es la única configuración de
   22.176 que llega a error 4.
3. **La tabla de energía que pusieron, ¿es la de Zuber et al. 2022?** Es el único parámetro químico
   que cambió respecto del original, y querríamos poder citar el paper correcto.
4. **Los números de la columna 9, ¿son «eficientes» o «eficientes sin off-targets»?** Son dos
   columnas distintas en esta librería, y si es la segunda, necesitamos saber contra qué referencia,
   porque esa sí depende de la base.
5. **¿Alguna de las secuencias se cargó en minúsculas?** Medimos que eso da cero eficientes sin
   avisar.
6. **¿El método «IA» de Apolo Rocket llegó a implementarse?** En el backend público está el campo
   pero no el modelo. Si existe, con qué datos se entrenó y qué devuelve.
7. **¿Qué versión de ViennaRNA usa el servidor?** Entre 2.1.5 y 2.7.2 hay varios eficientes de
   diferencia por gen.
8. **La rama de la regla terminal que da «eficiente» sin mirar la termodinámica, ¿es intencional?**
   Está en el original, en sifi21INTA y en Apolo Rocket.

---

## Lo que no se pudo hacer

No se corrió Apolo Rocket: necesita PostgreSQL con el esquema, el árbol de referencias indexadas en
disco y una capa HTTP que no está publicada; se leyó el código, el PDF de endpoints y los dos
volcados, y de ahí salen todos los números de Q3. No se consiguió RNAplfold 2.1.5, así que la
comparación con la corrida del programa original de W5 queda confundida por la versión de ViennaRNA.
No se clonó nada con `git`: el entorno no permite crear directorios llamados `.git`, así que el
contenido se bajó por tarball y cada commit se verificó con `git ls-remote`. Y no se leyeron enteras
las seis figuras HTML de ejemplo de Apolo Rocket, de 3,4 a 3,8 MB cada una: de una se extrajo sólo el
arreglo de la curva de eficiencia, que resultó idéntico al guardado en la base.
