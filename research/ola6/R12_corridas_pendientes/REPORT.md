# R12 — El barrido de corridas pendientes del issue #37, corrido donde los insumos estaban

El issue **#37** inventarió las corridas que habían quedado pendientes «por falta de insumo,
no por falta de decisión», con una casilla por corrida y su línea **Necesita**. Este bloque es
el resultado de agarrar ese inventario en la máquina donde los insumos están —la de Joaquín,
con `work/` en disco— y correrlo entero.

El resultado corto: **de las catorce casillas, nueve se cerraron con la corrida hecha, tres
cambiaron de naturaleza al medirlas y dos siguen abiertas con el motivo corregido.** Y el
hallazgo que atraviesa todo el barrido no es ninguna de las mediciones nuevas: es que **de los
cinco bloqueos que el inventario atribuía a falta de insumo, tres no eran de insumo**. Uno era
un parámetro que el propio censo cambiaba, otro era el directorio desde donde se corre un
test, y el tercero un número publicado que estaba mal por tres órdenes de magnitud.

## 1. El entorno, que era la premisa de todo el inventario

El issue reparte trabajo entre dos máquinas según qué herramienta tiene cada una, y esa
tabla venía mal medida tres veces: la entrada 54 la corrigió para `command -v`, la 55 para
«en qué máquina», y este barrido cierra la última celda que quedaba en pie. De los doce
entornos de `micromamba` de esta máquina, **uno solo corre la línea entera**: `w5bio`, con
Python 3.11.17, ViennaRNA 2.7.2 —la misma versión que usó `C13`, que es lo que hace
comparables las cifras—, Biopython 1.88, `ahocorasick`, numpy 2.4.6, BLAST+ 2.17.0 y los
veintinueve ejecutables de ViennaRNA, `RNAfold` y `RNAplfold` incluidos `[M]`.

Esos dos últimos son la celda que faltaba: `PLAN_OLA6.md` los daba por ausentes con la
salvedad de que no se habían vuelto a medir contra los `envs/`. Están. **De la lista original
de herramientas faltantes de esta máquina no falta ninguna** `[M]`.

## 2. Los ocho generadores, de 2 de 8 a 7 de 8

La casilla principal del #35 pedía correr los ocho generadores de punta a punta y dejar que
la compuerta señalara las regiones sin tamizar. Iban 2 de 8. Van **7 de 8** `[M]`, y de los
tres que fallaban en la primera pasada **ninguno fallaba por falta de insumo**:

| Generador | Antes | Ahora | Por qué |
| --- | --- | --- | --- |
| `ranking.py ranking` | no corría | **OK** | tenía los insumos en esta máquina |
| `ranking.py nulo` | no corría | **OK** | idem |
| `ranking_v2.py` | no corría | **OK** | el censo lo invocaba con `--muestras 50` y eso rompía un ancla por construcción (§3) |
| `M6 tabla_alertas.py` | no corría | **OK** | tenía los insumos |
| `M6 compuerta.py` | OK | OK | no cuenta para el criterio: itera sobre el inventario |
| `M6 umbral_compuerta.py` | OK | OK | idem |
| `M5 sensibilidad_reparto.py` | no corría | **frena en una firma** | llegó al final de la cadena de insumos (§4) |
| `O3 01_region_vatpase_b.py` | no corría | **OK** | desencuentro de rutas en `work/O3/`, no falta de datos (§5) |

## 3. El ancla que el censo rompía solo

`ranking_v2.py` reportaba **ANCLA ROTA**, que es el peor mensaje posible porque es el que
nadie ignora. No era el motor: el censo lo invocaba con `--muestras 50` para abaratar la
corrida, y el ancla del barrido compara frecuencias contra `W7` con **igualdad exacta**, lo
que sólo tiene sentido con el mismo número de sorteos. Las frecuencias obtenidas eran
múltiplos de 2,0 —o sea, de 50 muestras— contra las décimas finas de las 2.000 publicadas.

Corregido el comando del censo, `ranking_v2.py` corre entero en unos 60 s y pasa **todas** sus
anclas `[M]`. `[H]` La lección es de diseño de censos: un comando que cambia un parámetro para
ir rápido puede romper un ancla sin que el ancla esté mal, y conviene que corra con los
defaults o que declare al lado qué cambió.

## 4. La región que la compuerta encontró, y el pendiente que cambió de dueño

`sensibilidad_reparto.py` levantó `RegionNoTamizada: eth_Dm 194-393`. En vez de agregarla e
iterar —que es lo que el issue proponía, «hasta que termine»—, se midió la cosa entera de una
pasada: los nueve `rho` del barrido de exposición por los seis genes, replicando la elección
de `ranking_v2.recomendadas()` pero sin llamar a la compuerta, para ver todas las regiones que
el barrido elegiría en vez de la primera que lo corta.

De los **54 pares gen × rho**, `eth_Dm` 194-393 es la **única** que no estaba en el inventario
de 19, y aparece **sólo en `rho` = 0,00** `[M]`: el reparto de `D47`, con el peso de exposición
de *Homalodisca vitripennis* en cero. Con cualquier `rho` mayor la recomendada de `eth_Dm`
vuelve a ser 114-313, que ya estaba.

Agregada al inventario, **trae una coincidencia perfecta de 21 nt** —y hay que decirlo con
todas las letras, como el issue pide—, pero es **la misma que ya tenía `eth_Dm` 193-392**:
mismo organismo, mismo locus (`LOC124369889`, quitinasa 2 probable), **misma posición 347**,
los mismos conteos de `D28` `[M]`. Es un acierto visto desde una región corrida un nucleótido.

La fila queda **sin firmar**, que es lo correcto. Y la consecuencia es la parte que importa
para el inventario de pendientes: mientras siga sin firmar, `sensibilidad_reparto.py` **no
termina**, y su error pasó de `RegionNoTamizada` a `AlertaSinDecidir`. O sea que ese pendiente
dejó de ser «falta `work/`» y pasó a ser «falta una firma», que es **otra clase de pendiente**
y está en manos del equipo, no de una máquina.

## 5. `work/O3/` tenía otro layout, y ninguna cifra se movió al rehacerlo

`01_region_vatpase_b.py` moría con `StopIteration`. Busca `work/O3/sifi/full_corregido/` y los
dos tamizados; lo que había en disco era `work/O3/salida/` y `work/O3/offtarget/cds_completo/`,
de otra corrida. Regenerado el layout que el script declara, con ViennaRNA 2.7.2, el script
corre entero y reproduce `D74` **celda por celda**: 1.184 regiones posibles, **una** no vetada
(517-816) y el veto por referencia con maíz 12, *H. vitripennis* 38 y humano 21 `[M]`.

Comparado por valor contra el `region_vatpase_b.json` publicado, las diferencias son **cuatro
y ninguna es una cifra**: el nombre de la consulta, dos separadores de ruta de Windows y la
versión de Python `[M]`. El archivo publicado se dejó como estaba: es el registro de la
corrida que lo generó.

`[?]` Queda un cabo: el `REPORT.md` de `O3` nombra `work/O3/fasta/consultas_pasoA.fasta` como
consulta del tamizado y **ningún script versionado lo genera**. Que todos los conteos
coincidan prueba que la secuencia es la misma; el generador de ese FASTA no está.

## 6. `ranking_v2.json` es byte-reproducible, y además reproduce el publicado

El único criterio del issue **#34** que no se había podido cumplir era regenerar
`ranking_v2.json` de punta a punta desde `work/sifi_v2/` y verificar que una segunda
regeneración seguida da el mismo archivo byte a byte. Hecho, y el resultado va más lejos que
lo que el criterio pedía: **las dos regeneraciones y el archivo publicado tienen el mismo
`sha256`** `[M]`. `comparar_json.py` lo confirma por valor: «idénticos valor por valor, y con
el mismo orden de claves».

Eso cierra también la casilla del **#30**, cuyo pendiente era que el orden en que fallaría una
regeneración completa estaba «inferido del código, no medido»: la regeneración completa, con
las seis regiones de 22 nt en el inventario, **no falla en ningún punto** `[M]`.

## 7. `V-ATPase B` y las junturas, al inventario (`D78`, implementada en `D87`)

`D78` había decidido que las dos entraran y dejado la corrida pendiente. Al correrla apareció
que faltaba algo más que la corrida: **soporte en el generador**. Agregar la región a
`REGIONES` falla con `KeyError`, porque cada gen se resuelve contra el catálogo del ranking, y
el camino obvio —meter el gen ahí— habría movido `ranking_v2.json`. El razonamiento y la
alternativa elegida están en `D87`; acá va lo medido.

**La matriz de `V-ATPase B` 517-816**, cuatro filas, **cero coincidencias perfectas de 21 nt**
en las cuatro, y tres de ellas contra el **ortólogo del blanco** en un no objetivo `[M]`:

| Organismo | Gen impactado | 21/21 | ≥ 19 nt | de ésas, eficientes |
| --- | --- | --- | --- | --- |
| *Harmonia axyridis* | `LOC123679872`, subunidad B de V-ATPasa | 0 | 4 | 0 |
| *Homalodisca vitripennis* | `LOC124359774`, subunidad B de V-ATPasa | 0 | 8 | **2** |
| *Homo sapiens* | `ATP6V1B1` | 0 | 4 | 0 |
| *Zea mays* | `LOC103630847`, signalosoma COP9 subunidad 3 | 0 | 3 | 0 |

`[H]` Que un gen tan conservado dé sus bloques de ≥ 19 nt contra sus propios ortólogos y no
contra genes al azar es lo esperado, y es el argumento que la firma va a tener que atender: la
fila de *H. vitripennis* es la única que además aporta ventanas eficientes, y el peso de
exposición de ese organismo es justamente la decisión que `D47` dejó abierta. Las cuatro filas
quedan en «pendiente»: la firma la escribe una persona.

**Las dos junturas**, con la clave `(quimera <nombre>, "juntura")` que `D78` fija —sin los
`j`, que se mueven a la columna de contexto—. El agujero que `D78` nombraba, «una quimera
puede pasar la compuerta con su empalme sin tamizar», queda cerrado y verificado con las tres
propiedades que no son la misma `[M]`:

* `Q_BicC_Dm__VATPaseB_Dm`, que fabrica cero bloques, **pasa** en los dos umbrales: se la miró
  y no hay nada. Es la distinción que `D72` existe para hacer, porque en `alertas.tsv` esto y
  «nunca se tamizó» son las mismas cero filas.
* `Q_VATPaseB_Dm__BicC_Dm`, que fabrica tres bloques de 19 nt contra maíz, **pasa** en
  `perfecto_21` y **frena** en `perfecto_ge19` sin firma.
* una quimera cuyo empalme nadie tamizó levanta `RegionNoTamizada`.

El inventario pasa de 19 a **21 regiones más 2 junturas**, y las filas de alerta de 26 a
**32**. Las cinco anclas de `M6` siguen pasando y **ninguna fila que ya estaba se movió**: el
diff de `alertas.tsv` no tiene una sola línea borrada `[M]`.

## 8. La suite entera, sin una sola ancla salteada

La casilla transversal pedía que las diez anclas salteadas por insumo dejaran de saltearse.
Las seis suites pasan **enteras y sin saltear ninguna** `[M]` — y cuatro de esas diez no eran
de insumo:

* `test_ranking.py` salteaba cuatro anclas diciendo que faltaba
  `work/sifi_check/offtarget_full/offtarget_por_sirna.tsv`. **El archivo está.** Salteaba
  porque el issue manda correr los tests con `cd tools/sifi21_port`, y desde ahí la ruta
  relativa no resuelve. Desde la raíz pasa las cuatro.
* `pipeline/test_features.py` y `tools/sifi21_port/test_sifi.py` «no colectan» con
  `python -m pytest`, y son scripts como los otros cuatro: corren directo, sin pytest, que
  además no está en ninguno de los doce entornos `[M]`.

Y el panel del archivo que el issue pedía declarar: `work/sifi_check/offtarget_full/` tiene
**las seis referencias sin la humana** `[M]`, leído de su propio `offtarget_resumen.json`.

Tres anclas de `test_alertas.py` **fallaron** al agregar las regiones nuevas, y eso es el ancla
haciendo su trabajo: fijaban el inventario anterior —cuatro regiones pendientes, cuatro filas
con 21/21— y ahora son siete y cinco. Se actualizaron declarando el cambio, y una de ellas
hubo que **partirla en dos**: «las pendientes» y «ninguna trae 21/21» eran la misma afirmación
y dejaron de serlo, porque `eth_Dm` 194-393 está pendiente **y** trae un acierto perfecto.

## 9. `tblastn` sobre las bases de `work/C11/` (#22)

La vía que el issue #22 pedía y que se cerró con `miniprot` porque «no había BLAST+ en ninguna
de las dos máquinas» —lo que la entrada 54 midió falso—. Corrida contra las tres bases ya
construidas por `C11`, sin reconstruirlas, para consultar el mismo índice publicado: **31
filas** `[M]`, en `research/ola6/O2_vatpase_b/resultados/tblastn_tsa.tsv`.

Esto **no corrige** ningún número de `O2`: agrega el del otro algoritmo. `XP_054288745.1` da
100 % de identidad sobre las 500 posiciones contra `GHCC01013224.1`, que es el mismo
transcripto que `miniprot` había recuperado. `[?]` Las identidades de los dos algoritmos **no
son intercambiables**: `miniprot` alinea con modelo de *splicing* sobre el genoma y `tblastn`
alinea bloques sin intrón sobre transcriptos ya ensamblados.

## 10. La vuelta de `R8` contra un proteoma anotado (#32)

El §7 de `R8` declaraba que ninguna referencia era un proteoma y que por eso la vuelta usó el
ORF más largo. **Hay uno en esta máquina**: 31.163 proteínas de *H. vitripennis* en
`work/F1v/ref/`. Rehecha con `blastp`, reusando los mismos ORF del paso 1 para que la única
variable sea contra qué se devuelve:

| Lectura | Veredictos que cambian |
| --- | --- |
| comparando accesiones de proteína | **2 de 5** |
| de ésos, son otra isoforma del mismo producto | **2 de 2** |
| comparando productos (isoformas colapsadas) | **0 de 5** |

O sea que la limitación estaba bien declarada y **no afectaba el resultado** `[M]`. Los dos que
cambiaban caen en `XP_046683989.1`, la isoforma X2 del mismo producto que la consulta. Y los
dos no recíprocos lo siguen siendo, ahora con más precisión: la vuelta de maíz cae en
`chitinase-3-like protein 1` y la de humano en `probable chitinase 10`, otras quitinasas `[M]`.

`[H]` La segunda limitación de §7 —variantes de empalme— resultó estar del lado del
**proteoma**, no del transcripto, y se resuelve comparando productos y no accesiones. El error
va en la dirección conservadora: declara no recíprocos pares que sí lo son.

## 11. Lo que sigue abierto, con el motivo corregido

**La grilla fina de `O4` (#24).** No se corrió, y el motivo cambió: la entrada 48 decía 136.446
plegados y «unas horas de esta máquina». Son **129.761.738** `[M]`, unos 71 días a las 21
plegados por segundo que mide esta máquina. El tope hizo exactamente su trabajo —detener y
declarar el tamaño medido— y de paso dejó el costo de las cuatro retículas, que es lo que
faltaba para decidir. La decisión está en `D88`; la retícula de `--paso 10` (173.289 plegados,
unas 5,4 h) quedó lanzada y no terminó dentro de la sesión.

**Los dos ejes de `F3` (#27).** El de off-target por gen **no se desbloquea con `work/`**, y la
casilla lo decía mal: las 28 filas del catálogo sin `ventanas_21nt` son de **15 especies
distintas**, y lo que falta son sus 28 secuencias de transcripto, no un directorio de trabajo
`[M]`. El de conservación entre poblaciones **sí** tiene su insumo —los tres TSA están, con
25.662, 55.286 y 56.117 secuencias `[M]`— y no se corrió a propósito: el issue #27 pide que el
criterio y los pesos se escriban **antes** de la primera corrida, y ese preregistro no existe
todavía. Desbloqueada por insumo, frenada por preregistro, que no es lo mismo.

**`F2` sobre fichas completas (#26).** Sigue necesitando una decisión, no un insumo, y el
propio issue #37 ya lo decía: no hay fuente versionada de términos GO, dominios conservados ni
papers por locus, y crearla es una corrida de `F1` ampliada o una fuente nueva.

**Las cinco filas nuevas del inventario, sin firmar.** Cuatro de `V-ATPase B`, una de
`eth_Dm` 194-393 y una de juntura. Ninguna la firma el motor.

## 12. Cómo se reproduce

Desde la raíz, con el entorno `w5bio` (es el único con todo: §1).

```bash
E=~/.claude-science/conda/envs/w5bio/bin
# el censo de los ocho generadores
$E/python research/ola6/R11_compuerta_y_panel/scripts/censo_generadores.py
# el inventario de M6, con la region de V-ATPase B y las dos junturas
$E/python research/ola4/M6_alertas/scripts/identidad.py
$E/python research/ola4/M6_alertas/scripts/tabla_alertas.py
$E/python research/ola4/M6_alertas/scripts/compuerta.py
$E/python research/ola4/M6_alertas/scripts/umbral_compuerta.py
# ranking_v2 byte a byte (dos veces, y contra el publicado)
$E/python tools/sifi21_port/ranking_v2.py --trabajo work/sifi_v2 --json /tmp/a.json
$E/python tools/sifi21_port/ranking_v2.py --trabajo work/sifi_v2 --json /tmp/b.json
cmp /tmp/a.json /tmp/b.json && cmp /tmp/a.json research/ola3/C7_ranking_v2/resultados/ranking_v2.json
# las seis suites, DESDE LA RAIZ (ver seccion 8)
for t in test_alertas test_ranking test_ejes_separados test_orden_salida; do
  $E/python tools/sifi21_port/$t.py; done
$E/python pipeline/test_features.py; $E/python tools/sifi21_port/test_sifi.py
# tblastn sobre las bases de work/C11 (#22)
PATH="$E:$PATH" bash research/ola6/O2_vatpase_b/scripts/08_tblastn_tsa.sh
# la vuelta de R8 contra el proteoma anotado (#32)
PATH="$E:$PATH" $E/python research/ola6/R8_quitinasa_eth/scripts/03_vuelta_proteoma.py
```

El layout de `work/O3/` que pide `01_region_vatpase_b.py`, si no está (§5):

```bash
cp work/sifi_check/BicC_Dm_full.fasta work/O3/fasta/BicC_Dm_full.fasta
$E/python tools/sifi21_port/run_sifi.py work/O3/fasta/VATPaseB_Dm_full.fasta \
    --modo corregido --backend vienna --salida work/O3/sifi/full_corregido
$E/python tools/sifi21_port/offtarget_21nt.py --consulta work/O3/fasta/VATPaseB_Dm_full.fasta \
    --mm1 --db work/offtarget_db/*.fna.gz --salida work/O3/offtarget
$E/python tools/sifi21_port/offtarget_21nt.py --consulta work/O3/fasta/VATPaseB_Dm_full.fasta \
    --mm1 --db work/W5/ref/humano_rna.fna.gz --salida work/O3/offtarget_humano
```

### Archivos

| Archivo | Qué es |
| --- | --- |
| `resultados/o4_paso1_costo.log` | la salida del enumerador midiendo el costo de `--paso 1`: la fuente de los 129.761.738 de §11 |

Las mediciones de este barrido viven en los bloques que les corresponden y no se copiaron acá:
el censo en `research/ola6/R11_compuerta_y_panel/resultados/`, el inventario en
`research/ola4/M6_alertas/resultados/`, `tblastn` en `research/ola6/O2_vatpase_b/resultados/`
y la vuelta de `R8` en `research/ola6/R8_quitinasa_eth/resultados/`.
