# si-Fi+ — el port de si-Fi21 con interfaz

Esto es el mismo criterio de eficiencia de si-Fi21 reimplementado en Python 3, con una
interfaz que se abre en el navegador. El cálculo no es nuestro: es el de si-Fi, verificado
contra el programa original. Lo nuestro es que se pueda usar, que se pueda auditar y que
diga lo que no sabe.

**«si-Fi+» es un nombre de trabajo, no una decisión.** La licencia del original está en
conflicto entre tres declaraciones —el artículo dice CC BY-SA 4.0 y SourceForge dice
CC BY-NC 2.0 `[?]`— y un trabajo derivado no puede resolver eso por su cuenta. Hasta que se
aclare, esta carpeta no lleva archivo de licencia y el nombre queda en suspenso.

## Cómo se abre

Doble clic en `abrir.bat`. Levanta un servidor local y abre el navegador. Si falta Python o
alguna dependencia, lo dice y deja la ventana abierta para que se pueda leer.

Desde la línea de comandos es `python servidor.py`, y acepta `--puerto` y `--no-abrir`.

**El servidor escucha sólo en `127.0.0.1`.** No es una promesa en un documento: el socket no
está atado a ninguna interfaz de red, así que no hay a dónde salir. Es lo que exige la regla
de confidencialidad del proyecto para las secuencias no publicadas.

Hace falta Python 3.10 o más nuevo y las cuatro dependencias del port
(`tools/sifi21_port/requirements.txt`: Biopython, ViennaRNA, numpy y pyahocorasick). La
interfaz misma no agrega ninguna: es biblioteca estándar.

## Qué hace

**Vista de diseño.** Se pega una secuencia o se abre un FASTA, se ajusta el criterio y se
corre. El resultado son dos gráficos que comparten el eje de posición:

- Arriba, la curva del «RNAi design plot» del original: cuántos siRNA eficientes se
  superponen a cada posición del ARNm, con la línea de referencia de todos los siRNA. Es la
  curva que ya conocés.
- Abajo, lo que el original no tiene: cuántos siRNA eficientes tendría una región de largo
  *L* centrada en cada posición. Elegir región es elegir un punto de esa curva, así que esa
  curva es la variable de decisión.

Van en dos paneles y no en un eje porque son dos medidas con escalas distintas: la de arriba
no puede pasar del tamaño de la ventana y la de abajo llega a decenas.

Debajo, tres tiras con una marca por ventana: eficiente, con off-target de bloque perfecto, y
con un desajuste. Una tira sin medir dice «sin medir», que no es lo mismo que cero.

Pasando el puntero se lee cualquier posición con los términos de esa ventana. Arrastrando se
marca un rango, y el rango se puede guardar con un nombre.

**Vista de off-target.** Una consulta contra varias referencias en una sola corrida, con una
tabla comparativa. El original elige una base en un desplegable y hay que correrlo una vez por
cada una; su gráfico, además, topea en cinco objetivos.

El dato de ejemplo sirve de control de cordura: como es un ARNm de *Zea mays*, corrido contra
el transcriptoma del maíz da **1.116 coincidencias perfectas sobre 1.116 ventanas** —se
encuentra a sí mismo— y **cero** contra *Harmonia axyridis* `[M]`. Si alguna vez esos dos
números dejan de dar eso, el tamizaje está roto.

**Rangos guardados.** Cada rango queda con sus coordenadas, sus conteos y la configuración que
los produjo. Esto último importa: un conteo sin su modo y su motor no significa nada, porque
los mismos cuatro genes dan cuatro números distintos según cuál de los dos RNAplfold corrió.

## Los dos modos, que es el punto

si-Fi compone un veredicto termodinámico —selección de hebra (*strand selection*), estabilidad
de extremos (*end stability*) y accesibilidad del sitio blanco (*target site accessibility*),
en conjunción— y después aplica una regla sobre los nucleótidos terminales. Esa segunda regla
**no es un filtro: es una ramificación**, y una de sus cuatro ramas devuelve «eficiente» sin
mirar el veredicto termodinámico (`sifi_pipeline.py:535-541`).

- **Modo fiel** conserva esa rama tal cual. Hace falta para auditar cualquier número producido
  con si-Fi.
- **Modo corregido** aplica la preferencia terminal como filtro adicional sobre el veredicto
  termodinámico, que nunca se saltea.

La diferencia, medida ventana por ventana con el mismo RNAplfold 2.1.5: entre el 14 % y el
24 % de lo que si-Fi reporta como eficiente lo es **sólo porque la regla terminal se saltea la
física** `[M]`. Ninguna ventana va en sentido contrario: el corregido es un subconjunto
estricto del fiel.

En la interfaz los dos modos están a la vista y cada número lleva su etiqueta de modo y motor.
Nada obliga a elegir uno: la herramienta no decide cuál tiene razón.

## Lo que está verificado

`python test_api.py` — 90 verificaciones, y las que importan entran **por el camino de código
de la aplicación**, no por el CLI. Eso es lo que prueba que la interfaz no movió ningún número:

| Motor | Modo | MP_MRFV | CP_MRFV | BicC_Dm | ATPaseD_Dm |
|---|---|---|---|---|---|
| RNAplfold 2.1.5 (el de si-Fi21) | fiel | 133 | 32 | 212 | 42 |
| RNAplfold 2.1.5 | corregido | 114 | 25 | 162 | 34 |
| ViennaRNA 2.7.2 | fiel | 142 | 39 | 223 | 35 |
| ViennaRNA 2.7.2 | corregido | 123 | 30 | 171 | 29 |

La fila de arriba son los cuatro conteos que imprimió **el programa original** con su interfaz
y sus valores por defecto, y el test los lee de su propio CSV para compararlos `[M]`.

La curva también: ocho tramos separados, en las mismas posiciones y con las mismas alturas
—máximo 9 en 150-156, luego 8 en 287-297 en `ATPaseD_Dm`— y la línea de referencia plana en
21 `[M]`.

Si falta el binario de RNAplfold o alguno de los FASTA, el bloque correspondiente **se declara
no corrido** en vez de dar un cero tranquilizador.

## Los defectos del original que esto corrige

1. **El botón Start que no hace nada.** `run_rnaplfold` le pasa `cwd` a `Popen` con el
   ejecutable por nombre pelado, no lo encuentra, cae en un `else` que nunca asigna
   `lunp_data`, y el `UnboundLocalError` se lo traga el slot de Qt. Acá los binarios se llaman
   por ruta absoluta, y al arrancar se informa qué motor hay y, si falta, por qué.
2. **La tabla de resultados no se muestra nunca.** En el original el número de eficientes sale
   únicamente por `Save as → Table (CSV)`, escribiendo la extensión a mano. Acá está en
   pantalla, con una fila por ventana y todos los términos del veredicto.
3. **No se pueden guardar las secuencias de los siRNA.** El README oficial de si-Fi21 dice que
   la función «no está implementada» y manda a buscar un `tmpXXXX.json` en `%TEMP%` para
   parsearlo a mano. Acá se exportan en FASTA.
4. **La exportación corrompe el nombre del archivo**: `filename += filename + '.csv'` concatena
   la ruta consigo misma.
5. **El tope de cinco objetivos** en el gráfico de off-target.
6. **Los desajustes apagan la eficiencia.** Si se permite más de cero, el original deshabilita
   las ocho casillas y marca todo como no eficiente. Acá no hace falta: el veredicto no
   depende del alineamiento en absoluto, son dos cálculos separados.
7. **El conteo de off-targets mete la baja complejidad en la misma bolsa.** Ver abajo.

## La baja complejidad, que es un hallazgo y no una función

Corriendo el genoma público del *Maize rayado fino virus* (`NC_002786.2`) contra tres
transcriptomas no objetivo aparecieron 9, 11 y 13 ventanas con coincidencia perfecta de
21/21 nt. Son unas trece órdenes de magnitud más de lo que da el azar, así que o es homología o
es un artefacto. Mirándolas: **las de las tres bases son la cola de poli-A del genoma viral**
`[M]`. Todo transcriptoma tiene poli-A.

(El dato de ejemplo que viene con la carpeta no es ese genoma sino un ARNm de maíz. El del
virus se usó para medir esto y vive en `work/`, que no se versiona: cubre el 90,5 % de
`MP_MRFV` y el 96,5 % de `CP_MRFV`, porque esas dos regiones son subcadenas del genoma público
del virus. Eso es público y no es una fuga, pero no corresponde mandártelo de vuelta adentro
de nuestra herramienta.)

Descontando las ventanas de baja complejidad, las tres cifras caen a cero. En el criterio de
bloque perfecto de ≥19 nt queda señal real: 8, 7 y 19.

La herramienta no las descarta —descartar en silencio es el otro error— las **marca**, y cada
celda se informa en dos cifras: el total y cuánto de ese total es baja complejidad. El criterio
está declarado en `complejidad.py` y es nuestro `[H]`: una racha de un mismo nucleótido de 10 nt
o más, o dos nucleótidos distintos o menos en la ventana. Contrastarlo contra la corrida de
`dustmasker` que el repositorio ya tiene es el paso que falta para reemplazarlo por el estándar.

## Qué NO hace

- **No corre Bowtie.** El tamizaje propio es exacto, local y sin el límite de los 32 bits, pero
  la regla de conteo del original —un registro por acierto de Bowtie, no por ventana— vive
  aparte, en `research/ola4/M1_conteo_y_referencia/scripts/conteo_por_acierto.py`. Son dos
  preguntas distintas y mezclarlas en un mismo número es lo que hacía que los conteos no
  cerraran.
- **No pondera los desajustes por posición.** Un desajuste en la región semilla (*seed*, nt 2-8)
  no vale lo que uno en las posiciones 10-11. El original tampoco lo hace. Es la mejora
  pendiente más clara y está en `MEJORAS_PROPUESTAS.md`.
- **No diseña el ARNdc.** Da el perfil por ventana y el riesgo por región; armar el constructo
  es otra cosa.
- **No decide.** Muestra los dos modos, los dos motores y las cifras con y sin baja
  complejidad, y dice cuál es cuál.

## Dónde quedan las cosas

Todo lo que el programa escribe va a `work/sifi_plus/`, que está fuera del control de
versiones. Esta carpeta guarda código y documentación, nada más: por eso se puede compartir
sin revisarla archivo por archivo.

Las dos salidas que llevan secuencia —el FASTA de los siRNA y el TSV con la columna `seq`—
salen con un aviso adentro. Como las ventanas se solapan de a 1 nt, esa columna reconstruye el
gen entero: no se versionan ni se suben a ningún servicio web.

## Los archivos

| Archivo | Qué es |
|---|---|
| `servidor.py` | el servidor: ruteo y serialización, nada de criterio |
| `api.py` | traduce pedidos al motor del port; tampoco decide nada |
| `perfil.py` | el contrato de datos del gráfico: una fuente, dos dibujantes |
| `complejidad.py` | la marca de baja complejidad, con su criterio declarado |
| `offtarget.py` | el tamizaje contra varias bases, como trabajo con progreso |
| `proyecto.py` | los rangos guardados; impone que no se guarde secuencia |
| `exportar.py` | TSV, CSV en el formato del original, y FASTA de los siRNA |
| `estatico/app.js` | el dibujo interactivo y la interacción |
| `test_api.py` | las 90 verificaciones, incluidas las ocho anclas de conteo |
| `datos_ejemplo/` | `NM_001111367.2`, el ARNm de la ferredoxina-6 de *Zea mays* |

El motor está en `tools/sifi21_port/`, y sus diez cambios respecto del original, cada uno con
su justificación, en `tools/sifi21_port/CAMBIOS.md`.
