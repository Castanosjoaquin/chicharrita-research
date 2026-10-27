# R11 — Los tres limites que quedaron abiertos de la compuerta de D72

Issue **#35**, entradas **24**, **26**, **30** y **31** de la ola 6 de
`00_meta/PREGUNTAS_ABIERTAS.md`. Antecedentes: `D69`, `D70`, `D72`, `D74` y `D75`.

Tres cosas, y conviene decir primero cual es el tamano real de cada una. La primera es un
defecto de correctitud de la compuerta que **hoy no mueve ningun resultado** y que ahora
esta cerrado (`D77`). La segunda es una pregunta de cobertura —cuantas regiones publicadas
hay sin tamizar— que estaba abierta porque nadie la habia **contado**, y que esta pasada
contesta para los dos JSON publicados del ranking: **ninguna region publicada como
recomendacion esta sin tamizar**, y los cuarenta y un pares restantes salen todos de bloques
que no producen recomendaciones: ordenes de alternativas, regiones de maximo conteo y
regiones por defecto de barridos de sensibilidad `[M]`. La tercera
son dos decisiones de diseno que estaban pendientes y que quedan tomadas (`D78`), con la
corrida que las implementa declarada como pendiente y con su receta.

## 1. La compuerta ahora sabe contra que panel se le pregunta

`alertas.exigir_decidida()` consultaba la tabla de alertas completa y no tenia forma de
saber que referencias tenia el panel de la corrida que la llamaba. El caso concreto esta
en `ranking_v2.efecto_humano()`, que corre dos ramas: en la rama `sin_humano` una region
se evaluaba contra filas de *Homo sapiens* que esa misma rama habia sacado del panel
`[?]`.

`D77` decide que una alerta de un organismo fuera del panel **frena igual**, y que la
compuerta lo diga. El argumento esta completo en el ADR y se resume en una linea: la
coincidencia perfecta de 21 nt esta en el ARN que se sintetizaria, no en el panel con el
que una corrida lo puntua; sacar al humano del panel es una decision de analisis —aislar su
efecto— y no una afirmacion de que el humano no importa.

En el codigo son tres cosas. `estado_decision()` y `exigir_decidida()` toman `panel`, que
es el conjunto de `organismo_corto` de la corrida; el estado devuelve `panel`,
`organismos_fuera_del_panel` y `pendientes_fuera_del_panel`; y el mensaje de
`AlertaSinDecidir` nombra las filas que frenan desde fuera del panel y dice por que frenan.
`ranking.region_recomendada()` no le pide el panel a quien llama: lo resuelve con
`ranking.panel_actual()`, que lee el `REFERENCIAS` vivo —el mismo que `ranking_v2.con_panel()`
reescribe—, asi que la rama `sin_humano` queda declarada sin que nadie se acuerde de
pasarlo. `D_maidis` esta siempre en ese panel: su matriz entra por un archivo aparte y para
los genes del insecto se excluye por ser **on-target**, que no es lo mismo que estar fuera
del panel.

La prueba que pide el issue es la seccion 10 de `tools/sifi21_port/test_alertas.py`: **la
misma region, el mismo umbral, con y sin el organismo en el panel**. Frena las dos veces,
en los dos umbrales de `D28`, y lo unico que cambia entre las dos es que el mensaje de la
segunda nombra al humano y dice por que frena igual `[M]`. La prueba tambien distingue
`panel=None` —«no se declaro panel»— de un panel vacio declarado, que no son lo mismo, y
verifica que una fila **decidida** de un organismo fuera del panel pasa, porque el panel no
decide nada. Contra la tabla real, `BicC_Dm` 922-1221 pasa con el panel de W7 y su fila
humana queda nombrada `[M]`.

**Cifras que se mueven:** ninguna. `test_alertas.py` pasa entero y ninguna de las nueve
secciones anteriores cambio de veredicto. El unico archivo de resultados que cambia es
`research/ola4/M6_alertas/resultados/compuerta.json`, que gana tres claves informativas en
cada uno de sus treinta y ocho bloques de region x umbral —`panel: null` y las dos listas
vacias— sin que se mueva un conteo ni un veredicto `[M]`. De paso, ese archivo escribia la
ruta de la tabla con el separador de la plataforma; `compuerta.py` pasa a `as_posix()`.

## 2. Cuantas regiones publicadas quedan sin tamizar

La leccion de la entrada 24 es que la forma de encontrarlas no es buscarlas a mano:
`D70` y el issue #30 miraron `regiones_recomendadas` de las dos corridas y por eso
`BicC_Dm` 2123-2422 —que sale del bloque `efecto_humano`— se les escapo. La forma fuerte es
correr cada generador de punta a punta y dejar que la compuerta las senale, y eso **no se
pudo hacer en esta maquina**: la seccion 4 dice cual corrio, cual no y que le falta a cada
uno. Lo que si se pudo hacer, y que ninguna de las dos busquedas anteriores habia hecho, es
contar.

**Censo de caminos.** `scripts/censo_generadores.py` barre todo el `.py` del repositorio
—salteando `.git`, `__pycache__` y `.claude/worktrees`— buscando las cuatro marcas que
distinguen a un generador de regiones: que llame a `alternativas()`, que llame a
`region_recomendada()`, que llame a `exigir_decidida()` y que arme la region a mano desde
`["mejores"][0]["region"]`. Las marcas se cuentan sobre codigo, no sobre prosa: se sacan
comentarios, docstrings y cadenas de una linea, porque en este repositorio los modulos
explican en comentarios lo que hacen y porque tanto `test_alertas.py` como el propio censo
llevan las marcas **como dato**.

Dan **siete** archivos con alguna marca, y **uno solo** llama a `alternativas()` sin llamar
a ninguna compuerta: `research/ola6/O3_quimera_bicc_vatpase_b/scripts/01_region_vatpase_b.py`
`[M]`. Es a proposito y esta declarado en `D74`: la region de `V-ATPase B` es el insumo de
una medicion y no una recomendacion, y el propio JSON lo dice en su campo
`es_region_recomendada: false`. O sea que **el conjunto de lugares donde una region puede
nacer es cerrado y conocido**, y eso es lo que faltaba para poder decir «esto es todo» en
vez de «no sabemos». `[H]` Lo que el barrido no puede ver es una region publicada como
texto ya calculado en un `REPORT.md` o en un TSV escrito a mano: el censo cubre
generadores, no documentos, y el ultimo eslabon entre el computo y lo publicado sigue
siendo una persona (entrada 10 de la ola 6).

**Censo de coordenadas.** `scripts/regiones_publicadas.py` hace lo contrario: no mira el
codigo sino los JSON publicados, los recorre **enteros** —no la clave
`regiones_recomendadas`, que es lo que fallo antes— y cruza cada cadena con forma de region
contra `estado_regiones.tsv`. Y **no** mira una lista de archivos escrita a mano: barre
`research/` entero. La primera version de este script si tenia la lista escrita a mano, con
tres archivos, y era el mismo error de la entrada 24 un piso mas abajo —buscar donde uno se
acuerda—; lo encontro la revision de esta misma pasada `[M]`. Se saltean la salida de esta
linea, que se contaria a si misma, y `research/R7_microgravedad/`, que es otro proyecto cuyos
volcados de RCSB y Europe PMC traen rangos de residuos y numeros de ISSN con la misma forma
`ini-fin` que una region.

De **409** JSON barridos, **trece** traen coordenadas de los genes del panel: 415
coordenadas en total, 407 de genes del panel, **60** pares (gen, region) distintos y **41**
fuera del inventario `[M]`. Cada coordenada se clasifica antes de cruzarla, porque no todo lo
que tiene forma de region es una region candidata de nuestros genes: el catalogo de `C5`
publica la mejor region de 200 nt de blancos de la literatura —troponina C, ATP sintasa
beta—, que el inventario de `M6` no tiene por que tamizar.

| archivo | coords. del panel | pares | sin tamizar |
| --- | --- | --- | --- |
| `research/ola3/C7_ranking_v2/resultados/ranking_v2.json` | 138 | 53 | 34 |
| `research/ola3/C9_sensibilidad_umbral/resultados/pares_region_propuesta.json` | 96 | 30 | 13 |
| `research/ola4/M6_alertas/resultados/compuerta.json` | 38 | 19 | 0 |
| `research/ola2/W7_ranking/ranking.json` | 32 | 20 | 11 |
| `research/ola4/M7_robustez_bicc/resultados/referencia_resumen.json` | 28 | 3 | 0 |
| `research/ola3/C3_blast_ventana_azar/resultados/q2_21_vs_22.json` | 16 | 10 | 7 |
| `research/ola3/C8_conservacion/resultados/conservacion.json` | 12 | 7 | 0 |
| `research/ola4/M5_dos_ejes/resultados/anclas.json` | 12 | 6 | 0 |
| `research/ola5/N3_marcos/resultados/marco2_por_fuente.json` | 9 | 3 | 0 |
| `research/ola2/W5_secuencias_epilab/genes/resumen.json` | 8 | 8 | 1 |
| `research/ola2/W7_ranking/nulo_region.json` | 8 | 8 | 1 |
| `research/ola4/M5_dos_ejes/resultados/eje_conservacion_cicadelidos.json` | 7 | 7 | 0 |
| `research/ola6/O3_.../resultados/region_vatpase_b.json` | 3 | 1 | 1 |

El numero que importa no es el total sino **de que bloque sale cada una**, y ahi el resultado
es limpio: los 41 pares fuera del inventario salen **todos** de bloques que no producen
recomendaciones `[M]`. Son de cuatro clases y ninguna pretende ser una region usable: el
orden de alternativas de la cascada (`alternativas`, en los dos JSON del ranking), la region
de maximo conteo de un nulo (`nulo_epilab`, `nulo_nuevos`, `genes`, `mejor`), la region por
defecto de un barrido de sensibilidad (`estabilidad_region` en `C9`, `filas` en `C3`) y la
region candidata de `V-ATPase B` (`region_de_o3` y las dos variantes de borde en `O3`).

Del otro lado: en los bloques que **si** producen recomendaciones —`regiones`,
`regiones_recomendadas`, `fichas`, `fichas_recomendadas`, `efecto_humano`, `candidatos`, el
`detalle` de `compuerta.json` y las anclas de `M5`, `M7`, `N3` y `C8`— no hay **una sola**
coordenada fuera del inventario `[M]`.

Eso contesta la pregunta de la entrada 24, y la contesta en los dos sentidos. `[H]` Los
cuarenta y un pares sin tamizar no son un agujero equivalente al de 2123-2422, que si era
una recomendacion publicada. Lo que vale la pena dejar escrito es que **estan publicados
igual**, con la misma forma `ini-fin`, y que lo unico que hoy distingue a una recomendacion
de una alternativa es el bloque del JSON en el que aparece. Y algo que el censo **no** puede
decir: de esos cuarenta y un pares **no se sabe** si alguno tiene coincidencia perfecta de 21
nt, porque medirlo es tamizarlos y eso es justamente lo que no esta hecho `[?]`. No se afirma
que no la tengan: se afirma que no son recomendaciones. El listado completo, una fila por
aparicion y con su camino dentro del JSON, esta en `resultados/regiones_publicadas.tsv`.

La unica coordenada sin tamizar que **no** es un orden ni un descriptivo es `V-ATPase B`
517-816, que es el caso de la seccion 3 y de `D78` `[M]`.

## 3. `V-ATPase B` y las junturas: las dos entran al inventario

`D78` decide las dos cosas que la linea `O3` dejo abiertas, y conviene leer la segunda
junto con la primera porque no son del mismo tipo.

La region candidata de `V-ATPase B` entra como una region mas. No tiene fila en `alertas.tsv`
y desde `D72` la compuerta la rechaza con `RegionNoTamizada`, que es el comportamiento
correcto mientras no se la tamice. Lo que falta no es una decision sino un insumo: su matriz
de off-target contra el panel, que necesita `work/W5/ref/`.

Las junturas son el caso incomodo, porque es un agujero del mismo tipo que `D72` cerro para
las regiones: hay un objeto que se usa y que la compuerta no cubre `[?]`. Una juntura no es
una region de ningun gen —es secuencia que fabrica el ensamblado—, asi que el inventario
necesita una clave que no tiene. `D78` le da una: `(quimera <nombre>, "juntura")`, con la
granularidad de siempre, una fila por quimera x organismo x gen impactado. Los bloques
fabricados concretos no van en la clave: la fila que `O3` escribio dice
`region = "juntura, j=1,2,3"`, y si los `j` entran en la clave entonces un ensamblado que
fabrique bloques en otras posiciones produce otra clave y el inventario lee como objeto
nuevo lo que es el mismo empalme medido otra vez.

Y entran **las dos** quimeras, no solo la que tiene aciertos: `Q_BicC_Dm__VATPaseB_Dm`
fabrica cero bloques y `Q_VATPaseB_Dm__BicC_Dm` fabrica tres, todos contra maiz y ninguno de
21/21 `[M]`. Dejar afuera a la que no tiene aciertos reabre, del lado por donde menos se
mira, la distincion que `D72` existe para hacer.

**Ninguna de las dos se implemento en esta pasada, y el motivo es de insumo.** Agregar las
entradas a `REGIONES` en `tabla_alertas.py` sin poder correr el script dejaria `alertas.tsv`
y `estado_regiones.tsv` describiendo un inventario que el generador ya no produce, que es
peor que el agujero declarado. La receta esta en `PENDIENTE.md`.

## 4. Que corrio y que no, y en que maquina

Siguiendo la regla de `D71`: esto se verifico en **la maquina de Luca**, Windows 11
(10.0.26300) con el Python 3.10.11 del sistema, que tiene `numpy`, `scipy` y `pandas` y
**no** tiene `RNA` (ViennaRNA), `Bio` (Biopython), `ahocorasick` ni BLAST+. En esa maquina
**`work/` no existe**, y tampoco dentro de WSL, donde hay `~/yhat/tools` y `~/yhat/data`
—con `miniprot` y los genomas de `O2`— pero no una copia del repositorio `[M]`.

`scripts/censo_generadores.py` intenta correr cada generador declarado y guarda el codigo de
salida y el archivo que falta, copiado del error y no interpretado. De **ocho** comandos,
corrieron **dos** `[M]`:

| generador | corrio | que le falta |
| --- | --- | --- |
| `ranking.py ranking` | no | `work/sifi_check/salida/MP_MRFV_full_corregido_vienna.tsv` |
| `ranking.py nulo` | no | `work/sifi_check/salida/MP_MRFV_full_corregido_vienna.tsv` |
| `ranking_v2.py` | no | `work/sifi_v2/salida_k21/MP_MRFV_full_corregido_vienna.tsv` |
| `M6 tabla_alertas.py` | no | `work/sifi_v2/salida_k21/...` (lo pide por las anclas de M5) |
| `M6 compuerta.py` | **si** | — |
| `M6 umbral_compuerta.py` | **si** | — |
| `M5 sensibilidad_reparto.py` | no | `work/sifi_v2/salida_k21/...` (idem) |
| `O3 01_region_vatpase_b.py` | no | `work/o3` y `work/W5/ref` (muere con `StopIteration`) |

Los dos que corrieron son justamente los que **no pueden** encontrar una region nueva:
`compuerta.py` y `umbral_compuerta.py` iteran sobre las regiones que ya estan en el
inventario, asi que por construccion no levantan `RegionNoTamizada`. O sea que el criterio
fuerte de la parte 2 —correr cada generador de punta a punta y dejar que la compuerta
senale— **no se cumplio en esta maquina y queda pendiente**, con el comando exacto de cada
uno en `resultados/censo_corridas.tsv` y los insumos que hay que pedir en `PENDIENTE.md`.

Una advertencia que la entrada 36 dejo medida y que vale al hacer esas corridas: con un
archivo de off-target distinto **la cascada elige otra region**, asi que la
`RegionNoTamizada` que aparece es otra. La compuerta siempre senala una region real que
nadie tamizo —hace bien su trabajo— pero **que region senala depende del insumo**, y eso se
cruza con el issue #33, que tiene abierto cual de los dos paneles es el correcto. Un
`RegionNoTamizada` hay que leerlo junto con el panel con el que se corrio.

## 5. Como reproducir

```
python research/ola6/R11_compuerta_y_panel/scripts/censo_generadores.py --sin-correr
python research/ola6/R11_compuerta_y_panel/scripts/regiones_publicadas.py
python tools/sifi21_port/test_alertas.py
```

El censo completo —con los intentos de corrida— es el mismo comando sin `--sin-correr`. Los
dos escriben en `resultados/` y no tocan nada mas; `test_alertas.py` no escribe nada.
