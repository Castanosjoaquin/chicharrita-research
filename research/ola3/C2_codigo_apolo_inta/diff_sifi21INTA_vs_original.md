# Q1 — Qué cambió sifi21INTA respecto de si-Fi21 original

Comparación archivo por archivo entre `snowformatics/siFi21-` en el commit
`d6296b73c08a2176e9d0257e0a175278cff8c231` (2025-03-18, cabeza de `master`, verificado con
`git ls-remote`) y `bioinformaticaInta/sifi21INTA` en el commit
`92df44494373551d86eb1aee1b72d82858c581b2` (2024-03-27, cabeza de `main`, idem). Los dos
árboles están en `work/C2/sifi21_orig/` y `work/C2/sifi21INTA/`, fuera del control de
versiones. Las líneas citadas son las de esos dos commits.

## Qué es sifi21INTA respecto del original

La API de GitHub no marca el repositorio como fork, pero el código es derivado y se puede
mostrar: `freeEnergy.py` tiene **423 de 431 líneas idénticas** a `free_energy.py` del original
(medido con `difflib.SequenceMatcher` sobre las dos listas de líneas, 0,981 de coincidencia), y
el bloque de decisión de la regla terminal de `Sirna.py:66-96` es una transcripción rama por
rama de `sifi_pipeline.py:525-555`, con los mismos cuatro casos, el mismo orden y las mismas
comparaciones contra literales en mayúscula. Las constantes son las mismas y en el mismo orden
(`SifiPipeline.py:54-59` contra `sifi_pipeline.py:60-65`). `[E]`

La reescritura es estructural: de una aplicación Qt4 de un solo archivo de 27.902 bytes a cinco
módulos con clases (`SifiPipeline`, `Sirna`, `TargetSequence`), importables y sin interfaz
gráfica. Eso es lo que cambia casi todas las líneas; lo que importa para un número es mucho más
chico y está en la tabla.

## La tabla

«Efecto medido» quiere decir que hay una corrida en `corridas/` que lo produjo. «Sin efecto
medido» quiere decir que se leyó el código y no se midió, y está dicho como tal.

| # | Tema | Original | sifi21INTA | Qué hacía → qué hace | Efecto sobre el conteo de eficientes |
|---|---|---|---|---|---|
| 1 | **Tabla de vecinos más cercanos (nearest neighbours)** | `free_energy.py:278` (`nn_table=RNA_NN3`) | `freeEnergy.py:306` (`nn_table=RNA_NN4`), tabla nueva en `freeEnergy.py:61-74` | El ΔG de los extremos se calculaba con Chen et al. 2012; ahora con una tabla nueva atribuida en el comentario a Zuber et al. 2022, *Nucleic Acids Research* 50(9):5251-5262 | **Medido.** Con todo lo demás igual: 142→**138**, 39→**40**, 223→**218**, 35→**35**. Cambian 14 ventanas en total: **3 pasan a eficiente y 11 dejan de serlo** (`corridas/03_comparacion_port_vs_inta.json`) |
| 2 | **Regla terminal: sigue siendo ramificación, no filtro** | `sifi_pipeline.py:525-555`; la rama del bypass en `:535-541` | `Sirna.py:66-96`; el bypass en `:75-82` | Cuando el nucleótido 19 es A o T y el 2 no lo es, se decide **sólo por accesibilidad**, sin mirar el veredicto termodinámico. Igual en los dos | **Ninguno: está conservado.** Es el defecto C1 de `tools/sifi21_port/CAMBIOS.md` y sigue vivo |
| 3 | **Qué cuenta la fila «Efficients»** | `general_helpers.py:107-123`: `Counter` sobre los registros JSON, o sea **un registro por hit de Bowtie** | `SifiPipeline.py:430-448` (`getResultSummary`): recorre `self.sirnaData`, o sea **una fila por ventana** | El conteo dependía de la base de datos; ahora no | **Medido.** Mismo gen, tres bases distintas: 138, 40, 218 y 35 en las tres. En `BicC_Dm` Bowtie reporta 2.504 hits y el resumen dice 2.500 ventanas |
| 4 | **Nueva columna «Efficients without off targets»** | No existe: la tabla del original es nombre de hit, hits y eficientes | `SifiPipeline.py:430-448` | Ahora hay dos conteos y el segundo sí depende de la base y del blanco principal elegido | **Medido.** `ATPaseD_Dm` contra el transcriptoma TSA GITV01 de *Dalbulus maidis*: 35 eficientes y **12** eficientes sin off-targets |
| 5 | **Eficiencia para todas las ventanas** | `sifi_pipeline.py:221`: todo el bloque está dentro de `if strand == '+'` | `SifiPipeline.py:228-235`: recorre todo `sirnaData`, sin mirar la hebra | Bowtie decidía qué ventanas se evaluaban; ahora el perfil se calcula entero | Sin efecto en diseño contra una base que contiene el gen (todas las ventanas tienen hit en +). Lo confirma la coincidencia ventana por ventana con nuestro port |
| 6 | **Temperatura** | Fija en 22 °C en dos lugares: `free_energy.py:420` (`tao`) y `sifi_pipeline.py:62` | **Igual de fija**: `freeEnergy.py:446` y `SifiPipeline.py:56`; no es argumento del constructor (`SifiPipeline.py:17`) | No cambió nada. Sigue sin poder moverse desde la API | **Medido** forzando el atributo: a 25 °C en RNAplfold (con `tao` en 22) los cuatro conteos suben a 146, 45, 231 y 40 |
| 7 | **Umbrales de estabilidad de extremos y de accesibilidad** | Vienen de la interfaz, con 1,00 y 0,10 por defecto en modo diseño (`main.py:351-361`) | Mismos valores, ahora como argumentos con default (`SifiPipeline.py:17`: `endStabilityTreshold=1.0`, `targetSiteAccessibilityTreshold=0.1`, `accessibilityWindow=8`) | Mismos números, ahora programables | Sin cambio con los defaults. En el barrido, mover el umbral de extremos a 1,75 es lo que más acerca a la planilla |
| 8 | **Ventana de accesibilidad y su índice** | `sifi_pipeline.py:252`: toma la columna `accessibility_window` de la matriz `_lunp` después de borrar las primeras 20 filas | `SifiPipeline.py:218-226` y `Sirna.py:59`: guarda la fila sin la primera columna y toma el índice `accessibilityWindow-1` | Indexado equivalente: los dos terminan en u=8 | Ninguno. Los valores de accesibilidad coinciden ventana por ventana con los de nuestro port (diferencia máxima < 1e-6) |
| 9 | **Parámetros de RNAplfold** | `sifi_pipeline.py:351`: `-W 80 -L 40 -u <tamaño> -T 22` | `SifiPipeline.py:208`: los mismos cuatro | Sin cambio | Ninguno |
| 10 | **Cómo se lanza RNAplfold** | `sifi_pipeline.py:345-354`: `os.chdir()` al directorio de la herramienta y además `cwd=<temporal>` en el `Popen` | `SifiPipeline.py:203-216`: crea un subdirectorio junto a la salida, pasa `cwd` y confía en el `PATH` | Desaparece el `os.chdir` global; el ejecutable tiene que estar en el `PATH` | Ninguno sobre el número. Es el defecto por el que el original «no anda» en Windows; acá no aplica |
| 11 | **Parámetros de Bowtie** | `sifi_pipeline.py:332-334`: `bowtie -a -v <mm> -y <ruta+db> -f <query> <salida>` | `SifiPipeline.py:174`: `bowtie -a -v <mm> -y -x <db> -f <query> <salida>` | Mismo criterio de off-target: `-v`, desapareamientos extremo a extremo, ciego a la posición. Sólo se agrega `-x` explícito | Ninguno |
| 12 | **Tablas de desapareamiento de ADN en un cálculo de ARN** | `free_energy.py:278-279`: `tmm_table=DNA_TMM1`, `imm_table=DNA_IMM1` | `freeEnergy.py:306-307`: **los mismos defaults**, con comentarios nuevos que documentan de qué paper sale cada bloque (`freeEnergy.py:83-131`) | No se corrigió; se documentó | Ninguno en esta ruta de cálculo: el port midió cero consultas a esas tablas (`CAMBIOS.md` C3). Acá no se volvió a medir |
| 13 | **Cálculo de Tm muerto** | `free_energy.py:424-431`: calcula Tm y retorna `deltaG` | `freeEnergy.py:450-457`: idéntico | Conservado, con `dnac1`, `dnac2` y `selfcomp` como parámetros muertos | Ninguno |
| 14 | **`sequence.upper()` sin asignar** | `sifi_pipeline.py:299` | `SifiPipeline.py:163` (y `apolorocket/inputOutputFunctions.py:42`) | El resultado de `upper()` se descarta en los dos. La secuencia sigue como vino | **Medido.** La misma secuencia en minúsculas da **0 eficientes de 1.243 ventanas**, sin un solo aviso, porque las comparaciones de la regla terminal son contra literales en mayúscula |
| 15 | **Elección del blanco principal** | `sifi_pipeline.py:268-280`: diálogo modal de Qt sobre la lista de hits ordenada por cantidad | `SifiPipeline.py:237-248`: `input()` por consola, pidiendo números separados por coma después de mirar una figura HTML | Sigue siendo manual e irreproducible, ahora sin interfaz | Ninguno sobre «Efficients»; decide «Efficients without off targets» |
| 16 | **Figuras** | matplotlib dentro de Qt (`show_plot.py`, `create_plots.py`) | Plotly a HTML (`SifiPipeline.py:250-293`) | Salida interactiva y archivo, en vez de ventana | Ninguno sobre el conteo. **Pero la curva perdió una posición**: el original cubre las 21 posiciones de cada siRNA eficiente (`show_plot.py:237`) y sifi21INTA cubre 20 (`SifiPipeline.py:311`, `range(startQueryPos, endQueryPos)`) |
| 17 | **Anotación y regiones (funcionalidad nueva)** | No existe | `generalFunctions.py:26-132` y `TargetSequence.py`: agrupa hits en regiones con un tamaño de hueco máximo y les pega anotación de un GFF3 con BCBio | Agrega contexto genómico a los hits | Ninguno sobre el conteo de eficientes |
| 18 | **Dependencias** | Python 2.7, PyQt4, numpy, Biopython | Python 3, Biopython, plotly, pandas, BCBio (`README.md` del repo) | Ya no hay interfaz gráfica ni numpy | **Medido, y es una trampa:** `freeEnergy.py:384` llama a `Bio.SeqUtils.GC`, que Biopython eliminó en la versión 1.82. Con Biopython 1.88 el paquete aborta; hubo que instalar 1.81 para correrlo |

## Las tres diferencias que mueven un número

**La tabla de energía (fila 1) es el cambio químico, y es chico.** La tabla nueva, que el
comentario del código atribuye a Zuber et al. 2022, está en `freeEnergy.py:61-74` y pasa a ser
el default en la línea 306. Es la única diferencia de la lista que cambia un ΔG, y por lo tanto
la única candidata a ser «los parámetros desactualizados» que el investigador dijo haber
tocado. Medida sobre las cuatro secuencias: mueve el conteo **−4, +1, −5 y 0**. Cambia en las
dos direcciones, que es lo que necesitaría una explicación de la planilla —tres conteos por
encima y uno por debajo—, pero el tamaño no alcanza: la planilla pide −28, −5, −24 y −2
respecto de esta misma corrida. `[E]`

Dónde caen esas 14 ventanas también es consistente con el mecanismo: **ninguna** cae en la rama
del bypass, que no mira termodinámica, y las 14 se reparten entre las dos ramas que sí la miran,
7 en la rama «A/T en 19 y A/T en 2» y 7 en la rama «no A/T en 19 y G/C en 2»
(`corridas/06_ramas_cambios_NN4.json`). Esa es la clasificación por rama, que es otra cosa que la
dirección del cambio: por dirección, 3 ventanas pasan a eficiente y 11 dejan de serlo, de donde
sale el neto de −8 sobre los cuatro genes. Una tabla de energía sólo puede cambiar el veredicto
donde el veredicto depende de la energía. `[E]`

**El conteo por ventana en vez de por hit (fila 3) cambia qué significa el número.** En el
original, `general_helpers.py:113` cuenta un registro JSON por hit de Bowtie, así que el mismo
criterio sobre la misma secuencia da otro número según la base. En sifi21INTA el conteo es por
ventana y deja de depender de la base: medido contra tres bases distintas —los cuatro genes de
EPILAB, los 71 registros públicos de MRFV y el transcriptoma TSA GITV01 de *Dalbulus maidis*—
el número de eficientes no se movió ni una unidad. `[E]` Eso **cierra** una de las hipótesis
abiertas del proyecto: si el laboratorio corrió esta librería, la base de datos no explica la
diferencia con la planilla.

**La columna nueva «sin off-targets» (fila 4) sí depende de la base, y mucho.** Con la base de
los cuatro genes, eficientes y eficientes-sin-off-target coinciden. Contra el transcriptoma de
*D. maidis*, `ATPaseD_Dm` pasa de 35 a 12 y `BicC_Dm` de 218 a 214; contra los 71 registros de
MRFV, los dos genes virales caen a 0, porque casi toda ventana tiene hit en algún otro aislado
y todos esos hits cuentan como off-target. Ninguno de esos valores es 114, 35, 199 ni 33. `[E]`

## Lo que el diff deja intacto, y conviene decir en voz alta

El criterio de eficiencia de si-Fi21 **no cambió**. Las tres condiciones termodinámicas, el
orden en que se componen, los dos umbrales, la ventana de accesibilidad, el tamaño de 21 nt,
los 2 nt de extremo saliente (overhang), los 3 nt de extremo que entran al ΔG y la regla
terminal con su rama que saltea la física son los mismos. El tamizaje de off-targets sigue
siendo `bowtie -a -v N -y`, ciego a la posición del desapareamiento: la región semilla
(nt 2-8) y las posiciones catalíticas 10-11 valen lo mismo que el resto. `[E]`

La comprobación más fuerte de todo esto es que, forzando el único parámetro químico que cambió
—la tabla de vecinos— al valor del original, **sifi21INTA y nuestro port en modo fiel dan
exactamente lo mismo, ventana por ventana, en los cuatro genes**: 142, 39, 223 y 35 eficientes,
y cero diferencias en las 4.722 ventanas en los cinco términos del veredicto (selección de
hebra, estabilidad de extremos, accesibilidad, valor de accesibilidad y veredicto final). Son
dos implementaciones independientes del mismo criterio, y coinciden. `[E]`
