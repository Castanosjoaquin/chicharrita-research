# M9 — Auditoría de secuencia antes de compartir el repo o el port

Línea M9 de la ola 4 (issue #13). Cubre las tareas 1 a 3: promover la verificación a
`tools/verificacion/sin_secuencias.py`, correrla sobre el árbol y sobre el historial, y
dejarla como gancho de pre-commit. **La tarea 4 —cómo se comparte el port— no se toca
acá: es decisión del usuario y es una acción hacia afuera.**

## 1. Qué reemplaza

`research/ola3/C9_sensibilidad_umbral/scripts/limpiar_ancla.py` miraba una sola carpeta
(`C9/resultados/ancla/`) y quitaba la columna `seq`. Servía para el incidente que lo
motivó y no para el repositorio. La herramienta nueva recorre los 933 archivos
versionados —898 de ellos legibles como texto; el resto son binarios e índices de
Bowtie—, el índice y los 128 commits del historial `[M]`.

## 2. Las tres pasadas, y por qué hacen falta las tres

| Pasada | Qué busca | Hallazgos en el árbol |
|---|---|---|
| 1. Rachas | tramos de 21 nt o más de alfabeto de nucleótidos | 56.504 `[M]` |
| 2. k-meros solapados | columnas donde el sufijo de uno es el prefijo del siguiente | 43 cadenas `[M]` |
| 3. Contra EPILAB | 21-meros de las cuatro regiones que entregó el laboratorio | 6 `[M]` |

La pasada 1 sola no sirve para decidir: 56.504 hallazgos de los que la enorme mayoría son
datos públicos. La pasada 3 es la que contesta la pregunta que hace la regla de
confidencialidad de `CLAUDE.md`, y por eso es la que corre primero en el gancho.

La pasada 2 existe porque **el umbral de 21 nt no atrapa el incidente de C9 en general**.
Una columna de 15-meros solapados de a 1 nt reconstruye el gen igual y no produce ni una
racha de 21. Verificado con seis casos sintéticos: la columna de 15-meros da 0 rachas y 1
cadena de 60 k-meros que reconstruye 74 nt `[M]`.

## 3. Hallazgos en el árbol versionado

### 3.1 El único hallazgo de secuencias de EPILAB

`research/ola3/C4_offtargets_quimeras_largo/resultados/q2_aciertos_localizados.tsv`,
commiteado en `0c810a6` el 2026-10-20 y ya en el remoto `[M]`:

| Región | nt cubiertos | de | % | Tramo contiguo mayor |
|---|---|---|---|---|
| `MP_MRFV` | 46 | 200 | 23,0 % | 23 nt |
| `BicC_Dm` | 48 | 300 | 16,0 % | 25 nt |

Son 25 filas con una columna `sirna` de 21-meros: las coincidencias perfectas con maíz
que C4 localizó, con su posición en los cromosomas `NC_050098.1`, `NC_050100.1` y
`NC_050102.1`. **No reconstruyen las regiones**: el tramo contiguo mayor es de 25 nt
sobre regiones de 200 y 300 nt, y las ventanas son las que pegan en maíz, no una serie
consecutiva. `ATPaseD_Dm` y `CP_MRFV` no aparecen `[M]`.

Es un hallazgo real y acotado, y la decisión de qué hacer con él no es técnica (§6).

### 3.2 Las dos regiones virales ya estaban publicadas, por una vía que no es nuestra

`research/ola2/W2_herramientas/ejemplos/entradas/MRFV_NC_002786.2.fa` cubre el 90,5 % de
`MP_MRFV` y el 96,5 % de `CP_MRFV`, en tramos contiguos de 181 y 193 nt `[M]`.

Eso **no es una fuga**: el archivo es el genoma de referencia de *Maize rayado fino
virus*, accesión RefSeq `NC_002786.2`, declarada en el README de la carpeta `[R]`. Lo que
el hallazgo dice es otra cosa, y conviene tenerla a mano para la reunión: **las dos
regiones virales que entregó EPILAB son subcadenas del genoma público del virus**, así
que su confidencialidad es nominal. Las dos del insecto no están en esa situación `[M]`.

Que la cobertura sea 90,5 % y no 100 % es esperable si la región de EPILAB viene de un
aislado distinto del de la referencia; no se midió cuántas posiciones difieren `[H]`.

### 3.3 Dos archivos que reconstruyen un CDS completo, y no son de EPILAB

- `baseline_dsrip/ventanas_multigen.csv`: 47.224 rachas y 40 cadenas, la mayor de **3.528
  nt reconstruidos** `[M]`. Son CDS de *Tribolium castaneum* armados por
  `baseline_dsrip/gen_multi.py` desde el genoma y el GFF de referencia, que son públicos.
  Exceptuado con ese motivo. Lo que no tiene licencia abierta son los fenotipos de
  iBeetle-Base, y no están en este archivo.
- `baseline_dsrip/dsrip_vatpaseA.csv`: 5.473 rachas y 3 cadenas, la mayor de **1.845 nt**,
  que es exactamente el largo del CDS de V-ATPase A de *D. maidis* declarado en el README
  de la carpeta `[M]`. **No es ninguna de las cuatro regiones de EPILAB** (pasada 3 da
  cero) `[M]`. La primera corrida lo dejó sin exceptuar porque el README sólo decía que el
  CDS se había reconstruido desde `pipeline/salida/sirna_vatpaseA.csv`, que no se versiona,
  y un cero contra la planilla no es una procedencia. **Ahora está verificado y
  exceptuado** (§3.3 bis).

Este archivo es la razón por la que la pasada 2 reporta la dirección: la columna
`antisense_5_3` es el complemento reverso de la ventana, así que encadena al revés.
Mirando un solo sentido no se veía, y reconstruye igual.

### 3.3 bis La procedencia del CDS de V-ATPase A, resuelta sin salir de la máquina

La pregunta no necesitaba al NCBI ni a quien corrió la línea: la respuesta estaba en las
salidas del propio pipeline. De las 1.825 ventanas del CDS, **25 sobreviven al tamizaje y
aparecen en `sirna_finales.csv` y en `sirna_cercanos.csv` con su columna `locus`**, y las
25 caen en el mismo: `L06020`, que `candidatos_alto.csv` ubica en
**`OZ319711.1:47.265.953-47.286.132`, hebra `+`, 11 exones** `[M]`. `OZ319711.1` es uno de
los diez cromosomas de `GCA_975739785.1` (ihDalMaid1.1, Wellcome Sanger), el ensamblado
público de *Dalbulus maidis* sobre el que el pipeline mapeó con miniprot las proteínas de
referencia; la de este locus es `A0A1I9WLH3_NILLU`, de UniProt. El ortólogo de *Drosophila*
que le asigna la tabla es `Vha68-2`, que es la subunidad A de la V-ATPasa, así que el
nombre del archivo también cierra `[M]`.

El CDS reconstruido es un marco de lectura limpio: **1.845 nt, ATG inicial, 614 codones
más el stop `TAA`, cero stops internos** `[M]`. Eso es consistente con una subunidad A de
V-ATPasa y descarta que la concatenación de ventanas haya armado un artefacto.

Con la procedencia escrita, el archivo pasa a la lista blanca. Se reproduce con
`scripts/procedencia_vatpasea.py`, **con insumos locales**: `pipeline/salida/` está en
`.gitignore` porque sus derivados llevan fenotipos de iBeetle-Base. Si falta, el script lo
dice y no devuelve nada. Salida en `resultados/procedencia_vatpasea.json`.

### 3.4 El resto

`research/ola3/C13_quimeras_region_recomendada/resultados/empalme_maiz_detalle.json`: 3
ventanas de 21 nt del empalme de C13. La pasada 3 no las marca porque un empalme, por
construcción, no es subcadena de ninguna región; pero el bloque de 19 nt que ya está en
`PREGUNTAS_ABIERTAS.md` mezcla 4 nt de `MP_MRFV` con 15 de `ATPaseD_Dm` `[M]`. Queda sin
exceptuar para que lo decida quien decida 3.1, porque es el mismo criterio.

## 3.5 Un supuesto de M3 que esta línea tenía que verificar, y es falso

El issue #7 (M3) propone agregar al TSV por ventana las columnas `nt19`, `nt2` y
`rama_terminal`, y afirma: «son dos letras y un entero: no reconstruyen secuencia, así que
no chocan con la regla de confidencialidad». El propio issue pide que M9 lo verifique.

**No se sostiene.** Como las ventanas del port se solapan de a 1 nt, cada una de esas
columnas, concatenada en orden, es una subcadena literal del gen. Medido sobre un gen
sintético de 500 nt y 480 ventanas: la columna `nt19` da 480 nt que aparecen en el gen con
desplazamiento 18, `nt2` da otros 480 con desplazamiento 1, y entre las dos reconstruyen
497 de 500 nt, el 99,4 % `[M]` (`scripts/prueba_columnas_terminales.py`, sin datos reales).

El archivo no tendría **ninguna** racha de 21 nt: la fuga está en la columna, no en la
celda, y es justamente la clase de caso para la que existe la pasada 2. Si M3 publica esas
columnas para los cuatro genes, publica los cuatro genes.

Dos salidas, y la elección es de quien tome M3: emitir `--features` sin esas dos columnas,
o emitirla sobre ventanas no consecutivas, que rompe la cadena. Conviene decidirlo antes
de implementar.

## 4. Historial

Sobre los 128 commits, en modo `--solo-epilab`, el único hallazgo es el mismo
`q2_aciertos_localizados.tsv` en `0c810a6` `[M]`. Los TSV del incidente de C9 **no
aparecen**, lo que confirma que la reescritura de aquellos tres commits locales funcionó
y que nunca llegaron al historial publicado `[M]`.

**Las tres pasadas sobre el historial, y un filtro que faltaba.** La corrida del 23 de
octubre fue en `--solo-epilab`; corriendo las tres pasadas sobre los 159 commits de hoy
aparecieron tres archivos más, y uno de ellos destapó un defecto de la herramienta.
`sifi_plus/datos_ejemplo/NM_001111367.2.fasta` y `sifi_plus/test_api.py` son de la línea
de la interfaz y ya estaban exceptuados en el árbol, con su accesión. El tercero,
`research/ola2/W6_agentes_ciencia/index.html`, era **el mismo falso positivo de base64 que
§5 da por corregido**: el descarte de tramos que son el interior de otro token vivía sólo
en `buscar_rachas`, que es la pasada 1 del modo árbol, y el modo historial repetía el
recorrido por su cuenta sin ese filtro. Un filtro que existe en un camino y no en el otro
no es un filtro: ahora el modo historial llama a la misma función. Corregido, el historial
da **28 hallazgos no exceptuados, exactamente los mismos dos archivos que el árbol** `[M]`.

**Lo que el modo historial sigue sin mirar, y conviene no olvidarlo:** corre la pasada 1 y
la pasada 3, pero **no corre la pasada 2**, la de columnas de k-meros solapados, que es
justamente la que atrapa el patrón del incidente de C9 cuando los k-meros miden menos de
21 nt. Y la pasada 3 se aplica línea de diff por línea de diff, así que un k-mero partido
por un salto de línea no se ve. Las dos cosas son consecuencia de recorrer líneas sueltas
en vez de reconstruir el texto agregado por archivo. Quedan anotadas en
`00_meta/PREGUNTAS_ABIERTAS.md`: mientras tanto, **el modo historial contesta «esto estuvo»
y no «esto no estuvo»**.

**Limitación del modo historial, declarada:** la cobertura se calcula por línea agregada
del diff, no por archivo, así que los porcentajes de ese modo son un piso y no la cifra
real (una línea de FASTA de 70 nt reporta 35 % de una región de 200). Para la cifra hay
que usar el modo árbol. El modo historial sirve para contestar si algo estuvo, no cuánto.

## 5. Lista blanca

Catorce entradas, cada una con su motivo y su accesión cuando la tiene: el CSV de Cedden
(D41), los ejemplos de W2 (accesiones del NCBI declaradas en su README),
`candidatos_c5.fa` (accesión en cada cabecera), `ventanas_multigen.csv` (*T. castaneum*
público), `dsrip_vatpaseA.csv` (locus `L06020` de `GCA_975739785.1`, §3.3 bis), los datos
de R7 (PDB 8P6P, 7P6Z, 7OOC y ARNr 16S), el dato de ejemplo de la interfaz
(`NM_001111367.2`, ferredoxina-6 de maíz), los cebadores de `conservacion.py` (Tabla 1 de
Andrada *et al.* 2026, PMC13279319) y cinco archivos con fixtures de prueba o 21-meros
citados en el cuerpo de un informe.

Una excepción sin motivo escrito no es una excepción. El motivo tiene que decir por qué
el dato es público, no por qué molesta el hallazgo.

### Falso positivo corregido

`research/ola2/W6_agentes_ciencia/index.html` daba 3 hallazgos: son fuentes woff2
embebidas en base64 que por azar contienen tramos largos de A, C, G y T. Se corrigió en
la herramienta y no por excepción, porque el problema es general: si el carácter pegado
al tramo es alfanumérico y no es un nucleótido, el tramo es el interior de otro token.

## 5 bis. «No pude mirar» no es «miré y no encontré»

La línea M7 anotó que el gancho rechazaba con el mensaje equivocado: cuando falta la
planilla o falta `openpyxl`, la pasada contra EPILAB no corre y el gancho decía
«RECHAZADO: hay secuencias de EPILAB en lo que estas por commitear». Rechazar es lo
correcto —es fail-closed, y el proyecto ya se quemó una vez tomando un archivo vacío por
un cero medido—, pero el texto afirmaba un hallazgo que no hubo y mandaba a buscar
secuencias que no existen.

La herramienta ya distinguía los dos casos en su código de salida: **0 sin hallazgos, 1
hallazgos no exceptuados, 2 no se pudo verificar**. El gancho era el que no los miraba.
Ahora ramifica por código, y el 1 queda reservado para «miré y encontré»: cualquier otro
código —127 si falta `python3`, una excepción que se escapa, un Ctrl-C— cae en «no pude
verificar», que rechaza igual pero no manda a buscar secuencias que no existen. De paso,
el aviso decía siempre «no esta en disco» aunque la causa fuera `openpyxl`: la razón se
calcula una sola vez en `motivo_sin_epilab()` y se imprime tal cual. Los dos casos tienen
prueba en `scripts/prueba_detector.py`.

## 5 ter. Tres defectos que encontró la revisión de este mismo cambio

Los tres estaban en la herramienta desde antes y los tres la debilitaban en silencio.

**La lista blanca tapaba también los hallazgos de la pasada 3.** Era el peor: una
excepción dice «en este archivo hay nucleótidos y son públicos», y se estaba leyendo como
«en este archivo no hay nada de EPILAB», que es justo lo que la excepción no puede
contestar. Con un comodín como `ejemplos/*` o `datos/*` alcanzaba con que un archivo
exceptuado tuviera una región del laboratorio para que `--solo-epilab` diera cero y el
gancho pasara. **Los hallazgos de EPILAB ya no se exceptúan nunca**, con lista blanca o
sin ella.

**`git` fallaba hacia el lado abierto.** El envoltorio descartaba el código de salida, así
que un `index.lock`, un objeto ausente o el directorio equivocado devolvían una cadena
vacía, y una cadena vacía se lee como «no hay nada que reportar». El gancho podía pasar
sin haber mirado un solo archivo. Ahora una falla de `git` levanta `GitFallo` y sale 2, el
código de «no pude verificar».

**El recorrido del árbol usaba `git ls-files` sin `-z`.** Un path no ASCII sale
entrecomillado y con escapes octales, no existe en disco con ese nombre, y se salteaba sin
aviso. Hoy no hay ninguno versionado, así que no cambia ninguna cifra; se arregla porque
el día que lo haya el salteo sería invisible.

## 6. Lo que queda, y es del usuario

1. **Qué se hace con `q2_aciertos_localizados.tsv`** (§3.1) y con las 3 ventanas del
   empalme (§3.4). Las opciones son dejarlo y declararlo, como hizo D41; quitar la
   columna `sirna` con un commit nuevo, que lo deja en el historial; o reescribir el
   historial, que es destructivo para quien ya clonó. **Recomendación: la primera o la
   segunda, nunca la tercera**, con el mismo criterio de D41: retirar algo ya publicado
   no lo borra de las copias existentes. El dato está en un repositorio privado y son 25
   ventanas que no reconstruyen la región.
2. ~~Confirmar la procedencia de `dsrip_vatpaseA.csv` con Luca~~ **Resuelto sin
   preguntar** (§3.3 bis): sale del genoma público `GCA_975739785.1` y está exceptuado.
3. ~~Activar el gancho~~ **Hecho en este clon**: `git config core.hooksPath
   tools/verificacion/hooks` corre y queda en `.git/config`. Sigue haciendo falta una vez
   por clon. **Ojo con la consecuencia:** el gancho es fail-closed, así que mientras no
   estén `YHat-Biotech/Sequences_EPILAB.xlsx` en disco **y** `openpyxl` en el `python3` del
   PATH, rechaza todos los commits. En esta máquina faltan los dos, de modo que hoy hay
   que commitear con un intérprete que tenga `openpyxl` y el corpus a mano, o con
   `--no-verify` cuando el commit no toca secuencias. El mensaje del rechazo ahora
   distingue los dos casos (§5 bis).
4. **Cómo se comparte el port.** Es la tarea 4 del issue y no se hace sin confirmación. La
   recomendación del issue sigue en pie: un paquete con `tools/sifi21_port/` y nada más,
   porque es autocontenido y no arrastra `work/` ni los resultados derivados. Nótese que
   `tools/sifi21_port/` tiene dos archivos con secuencias (`conservacion.py` y
   `test_sifi.py`), los dos exceptuados por público, así que el paquete pasa la
   verificación `[M]`. Sigue abierta la pregunta de licencia de D32 `[?]`, que es el
   pedido 6 del lunes.

## 7. Criterio de terminado

El issue pide que la verificación corra sobre el árbol y sobre el historial y dé cero
hallazgos no exceptuados, **o** que los hallazgos estén listados y resueltos. Al 24 de
octubre los dos modos dan **la misma cifra y los mismos dos archivos**: 28 hallazgos no
exceptuados, 25 en `q2_aciertos_localizados.tsv` y 3 en `empalme_maiz_detalle.json`
`[M]`. De los tres archivos que la primera corrida dejó abiertos, el de §3.3 está
resuelto y exceptuado con su motivo; los otros dos son el mismo caso y esperan una sola
decisión, que es la del §6.1. Las tareas 1 a 3 están hechas y el gancho está activo; la 4
espera al usuario.

## 8. Reproducir

```sh
python3 tools/verificacion/sin_secuencias.py --solo-epilab          # la pasada que decide
python3 tools/verificacion/sin_secuencias.py --solo-epilab --historial
python3 tools/verificacion/sin_secuencias.py                        # las tres pasadas
python3 tools/verificacion/sin_secuencias.py --staged                # lo que corre el gancho
python3 research/ola4/M9_auditoria_secuencias/scripts/prueba_detector.py       # casos sinteticos
python3 research/ola4/M9_auditoria_secuencias/scripts/procedencia_vatpasea.py  # insumos locales
```

La pasada contra EPILAB necesita `YHat-Biotech/Sequences_EPILAB.xlsx` en disco, que no se
versiona, y `openpyxl`. Si falta, la herramienta **declara que la pasada no se corrió** en
vez de devolver un cero tranquilizador. Salidas en `resultados/`: `epilab_arbol.json`,
`epilab_historial.json` y `arbol_resumen.json`. El detalle por línea de la pasada 1 no se
versiona —son 30 MB de huellas— y se regenera con `--json`.
