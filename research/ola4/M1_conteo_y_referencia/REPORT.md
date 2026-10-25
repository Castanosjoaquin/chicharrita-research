# M1 — Reconciliacion de conteos: la matriz corrio, y explica un gen de cuatro

> **Nota del 2026-10-25, que cambia el titular de esta linea.** La discrepancia de los cuatro
> conteos **quedo explicada, y no por esta via**. La carta del investigador del 25 de octubre
> informa que la funcion historica de conteo asigna 20 posiciones de cobertura a cada ventana de
> 21 nt y cuenta los incrementos positivos de esa curva `[R]`; aplicada esa regla a nuestras
> propias ventanas eficientes, los cuatro valores de la planilla salen exactos `[M]`
> ([`research/ola5/N1_regla_de_conteo/`](../../ola5/N1_regla_de_conteo/REPORT.md), D62). Lo que
> sigue valiendo de M1, sin cambios: que la columna «Efficient siRNA hits» del original cuenta
> aciertos de Bowtie en la hebra `+` y no ventanas, que una base genomica puede borrar un gen
> entero de la tabla —`ATPaseD_Dm` da 0— y la matriz de once bases con sus treinta y ocho celdas.
> Lo que hay que leer distinto: **el «200 contra 199» de `BicC_Dm` era coincidencia**, no un
> acierto parcial de la hipotesis; el mecanismo verdadero da 199 clavado. Y el pedido 1 de la
> reunion, la clasificacion por ventana de su corrida, se retira porque ya no contesta nada
> (`00_meta/CAMINOS_PROBADOS.md`).

**Ola 4, linea M1.** La pregunta que abre esta linea viene de la carta del investigador del 22
de octubre de 2026 y de lo que aparecio al seguir su pista hasta el fuente: la columna
«Efficient siRNA hits» del si-Fi21 original no cuenta ventanas, cuenta aciertos de Bowtie, asi
que comparar nuestros 133, 32, 212 y 42 contra los 114, 35, 199 y 33 de la planilla fue, desde
el principio, comparar dos unidades distintas. M1 tenia que medir cuanto de la brecha explica
esa diferencia de unidad y cual es la referencia que la produce.

**Lo que se entrega, en una linea.** La regla esta implementada en
`scripts/conteo_por_acierto.py`, verificada con 44 pruebas sobre insumos sinteticos, y **la
matriz de bases corrio**: once bases y treinta y ocho celdas con el motor verificado —el control
de orientacion incluido—, mas una corrida de sensibilidad con un desajuste permitido y un cruce
con el eje del motor de accesibilidad `[M]`. El resultado es parcial y conviene decirlo
en el titulo: la regla del conteo por acierto contra el transcriptoma publico de *Dalbulus
maidis* explica `BicC_Dm` **con un error de uno** —da 200 contra los 199 declarados— y **no
explica los otros tres**. Para `MP_MRFV`, que es el gen de la brecha mas grande, ninguna
referencia que tengamos puede producir 114, y ahora sabemos por que: el conteo por acierto
sobre ese gen es practicamente una funcion escalon.

La mitad anterior de esta linea (commit `6cf0306`) habia declarado la matriz como pendiente
porque la maquina de esa sesion no tenia el corpus ni las herramientas. Esta maquina si los
tiene, y una parte de lo que aparecio contradice lo que ese reporte dejo escrito. Donde eso
pasa queda marcado.

---

## 1. Donde corrio, y con que

El insumo que la mitad anterior declaro ausente estaba en un lugar que no se habia mirado: **el
instalador de si-Fi2015 trae sus propias herramientas**, y con eso alcanza. En
`%LOCALAPPDATA%\siFi2015\` viven `RNAplfold.exe` 2.1.5 y `bowtie.exe` 0.11.3 con su
`bowtie-build.exe`, que son exactamente los binarios con los que corrio el programa original
`[M]`. No hace falta instalar nada: la dependencia que parecia faltar la trae el programa cuya
salida queremos reproducir.

| Insumo | Estado en esta maquina |
|---|---|
| `work/sifi_check/` con los cuatro FASTA de EPILAB | si |
| `work/offtarget_db/` con las seis bases comprimidas | si |
| RNAplfold 2.1.5 (backend `exe`, el verificado) | si, del instalador de si-Fi2015 |
| Bowtie | si, 0.11.3 del instalador de si-Fi2015 |
| ViennaRNA | si, 2.7.2 por las ligaduras de Python |
| Biopython | si, 1.88 |
| `work/C2/` con los drivers de la ola 3 | **no**, siguen sin versionar |
| BLAST+ | **no**, y esta linea no lo necesita |

Lo primero que se corrio fue el ancla: `tools/sifi21_port/run_sifi.py --modo fiel --backend exe`
sobre los cuatro genes devuelve **133, 32, 212 y 42** eficientes `[M]`, que son los cuatro
numeros verificados contra el programa original. Sin ese ancla la matriz no se puede leer,
porque cada celda es un conteo sobre el conjunto de ventanas eficientes y ese conjunto depende
del motor.

Todo el recorrido quedo en un driver versionado, `scripts/correr_matriz.py`, que va del FASTA al
conteo en un comando y escribe `resultados/procedencia.json` con las versiones, las bases que
corrieron, las que no y las celdas que fallaron. Eso responde al punto 4 de la lista de
pendientes del reporte anterior, al menos para esta linea: el reclamo era que los drivers de la
ola 3 viven en `work/` y no se pueden releer desde el repositorio, y repetir el error aca no
tenia sentido.

## 2. La regla, tal como quedo implementada

La lectura del fuente es la de la seccion 3 del plan de la ola 4 y no se repite. Lo que importa
para el codigo son tres frases, las tres `[R]`:

En `general_helpers.py:107-123`, `get_table_data` arma la tabla con
`Counter(player['hit_name'] for player in query if player['is_efficient'])`: **un registro por
acierto**, agrupado por el nombre de la referencia. En `sifi_pipeline.py:195-221`, si no hay
acierto el registro sale con `hit_name = False` y `strand = None`. Y como todo el bloque de
eficiencia vive dentro de `if strand == '+'`, una ventana sin acierto y una que pego solo en la
hebra menos **nunca se evaluan**.

El script devuelve, por cada par de gen y base, los cinco numeros que pide la tarea 1 y la tabla
desagregada por referencia, que es la unidad en la que el original presenta sus filas:

| Numero | Que es | Depende de la base |
|---|---|---|
| (a) `eficientes_por_ventana` | ventanas eficientes, una fila por ventana | no |
| (b) `aciertos_mas_total` | registros por acierto en la hebra `+`, la regla del original | si |
| (c) `aciertos_cualquier_hebra_total` | lo mismo sin el filtro de hebra | si |
| (d) `eficientes_sin_acierto` | ventanas eficientes que no pegan en ninguna parte | si |
| (e) `eficientes_con_acierto_multiple_en_una_ref` | ventanas eficientes que pegan dos o mas veces en la misma referencia | si |

Hay una decision de diseno que conviene dejar explicita, porque es la que hace el resultado
interpretable incluso si la hipotesis falla. **No sabemos que fila de la tabla leyo el
laboratorio**, y con una base de sesenta y cinco registros la tabla del original tiene hasta
sesenta y cinco filas. Asi que el script no elige: reporta tres agregaciones en paralelo y
ninguna se declara la verdadera —`suma_filas`, la suma de todas las filas; `fila_max`, la fila
mayor, que es el orden en que el original presenta la lista; y `fila_homonima`, la unica fila
cuya referencia nombra al gen, que devuelve `None` si hay dos, porque dos filas sumadas no son
una fila— y calcula la distancia L1 de cada una al vector declarado.

Esa decision resulto ser la que mas rindio de todo el diseno. Con la matriz corrida, las tres
agregaciones **no coinciden** en las bases de varios registros: para `CP_MRFV` contra los
sesenta y cinco registros de MRFV, `suma_filas` da 779 y `fila_max` da 32 `[M]`. Si el script
hubiera elegido una, la celda habria dicho una cosa y la otra lectura habria quedado invisible.

## 3. Una correccion al criterio de terminado, y lo que la medicion dice de ella

El criterio (a) del plan dice que, contra una base que es el gen mismo, el conteo por ventana y
el conteo por acierto **tienen que coincidir**. La mitad anterior de esta linea objeto el
criterio y tenia razon en general: si un 21-mero del gen esta repetido, la ventana que lo
contiene pega dos veces contra el gen mismo y el conteo por acierto queda **por encima** del
conteo por ventana. En `BicC_Dm`, Bowtie reporta 2.504 aciertos para 2.500 ventanas `[M]`, lo
que se confirmo en esta maquina contra la misma base.

Pero conviene agregar lo que la medicion dice, porque matiza la objecion: **en los cuatro genes
reales el criterio se cumple igual**. Contra `epilab4`, (a) y (b) dan 133, 32, 212 y 42, con
(d) = 0 y (e) = 0 en los cuatro `[M]`. Los cuatro aciertos de mas de `BicC_Dm` caen sobre
ventanas **no eficientes**, asi que no entran al conteo. El criterio del plan era frágil, no
falso en este caso.

Donde si se rompe es con un desajuste permitido: con `bowtie -a -v 1` contra el gen mismo,
`BicC_Dm` da (b) = 215 sobre (a) = 212, con (e) = 3 `[M]`. Tres ventanas eficientes tienen un
casi-vecino dentro del propio gen.

El invariante que el script verifica con `--exigir-identidad` sigue siendo el correcto y es el
que se uso como compuerta de toda la matriz: contra el gen mismo **ninguna ventana eficiente
puede quedar sin acierto en la hebra `+`**. La corrida completa lo pasa.

## 4. La matriz

Once bases. Las dos primeras son el control; la tercera y la cuarta son las candidatas reales de
diseño; las ultimas cinco son el panel de no objetivo, que entra como control negativo y no como
hipotesis de que el laboratorio haya diseñado contra ellas.

| Base | Que es | Genes |
|---|---|---|
| `epilab4` | los cuatro genes de EPILAB: la celda de verificacion | los cuatro |
| `epilab4_rc` | lo mismo, complemento reverso: control de orientacion | los cuatro |
| `mrfv_nc` | `NC_002786.2`, genoma de referencia de MRFV, aislamiento Costa Rican | los dos virales |
| `mrfv_all` | los 65 registros publicos de MRFV de GenBank analizados en W5 | los dos virales |
| `gitv01_blancos` | `GITV01000968.1` y `GITV01001458.1`, los dos contigs del transcriptoma publico de *D. maidis* que la ola 3 identifico como blanco principal | los dos del insecto |
| `dmaid_genoma` | genoma de *D. maidis* `GCA_975739785.1` | los cuatro |
| `hvitri` | transcriptoma de *Homalodisca vitripennis* `GCF_021130785.1` | los cuatro |
| `zmays` | transcriptoma de maiz `GCF_902167145.1` | los cuatro |
| `amel` | transcriptoma de *Apis mellifera* `GCF_003254395.2` | los cuatro |
| `haxyr` | transcriptoma de *Harmonia axyridis* `GCF_914767665.1` | los cuatro |
| `fcandida` | transcriptoma de *Folsomia candida* `GCF_002217175.1` | los cuatro |

El conteo de la regla, por base y por gen, con el motor verificado (RNAplfold 2.1.5). La fila es
`fila_max`, que es la agregacion mas favorable a la hipotesis; la tabla completa con las tres
agregaciones esta en `resultados/matriz.md` `[M]`:

| Base | `MP_MRFV` | `CP_MRFV` | `BicC_Dm` | `ATPaseD_Dm` |
|---|---|---|---|---|
| **declarado por la planilla** | **114** | **35** | **199** | **33** |
| nuestras ventanas eficientes (a) | 133 | 32 | 212 | 42 |
| `epilab4` | 133 | 32 | 212 | 42 |
| `mrfv_nc` | 133 | 32 | — | — |
| `mrfv_all` | 133 | 32 | — | — |
| `gitv01_blancos` | — | — | **200** | 42 |
| `dmaid_genoma` | 0 | 0 | 191 | **0** |
| `hvitri` | 0 | 0 | 0 | 3 |
| `zmays` | 0 | 0 | 0 | 0 |
| `amel` | 0 | 0 | 0 | 0 |
| `haxyr` | 0 | 0 | 0 | 0 |
| `fcandida` | 0 | 0 | 0 | 0 |

Tres lecturas, y la tercera es la que vale la linea.

**`BicC_Dm` queda explicado, con un error de uno.** Contra `GITV01000968.1`, el contig del
transcriptoma publico de *D. maidis*, doce de las 212 ventanas eficientes no pegan y la fila de
la tabla cae a **200**, contra los **199** declarados `[M]`. El reporte anterior habia estimado
«alrededor de 200» con una regla de tres sobre la perdida total de ventanas; la medicion sobre
las ventanas eficientes da 200. Eso no prueba que sea la referencia que usaron —un error de uno
sobre 212 es tambien lo que daria una coincidencia— pero es la unica celda de toda la matriz que
aterriza sobre un numero declarado `[H]`.

**`ATPaseD_Dm` no queda explicado, y contra el genoma se cae a cero.** Contra
`GITV01001458.1` las 42 ventanas eficientes pegan todas, asi que la fila da 42 y no 33 `[M]`.
Contra el genoma pasa algo distinto y peor: de las 42, cuarenta pegan **solo en la hebra menos**
y dos no pegan, asi que (b) da **0** `[M]`. El gen esta anotado en la hebra reversa del cromosoma
`OZ319711.1` y los 376 aciertos estan todos en `-`. Bajo la regla del original, ese gen
**desaparece entero de la tabla** si la base es el genoma en vez del transcriptoma. Es la
consecuencia 2 del fuente, en el caso real y con el signo mas fuerte posible.

**`MP_MRFV` es el que no cierra, y ahora se sabe por que.** Su conteo por acierto es casi una
funcion escalon. Las filas de la tabla contra los sesenta y cinco registros publicos de MRFV son
133 (`AF265566.2`), 133 (`NC_002786.2`) y 30 (`KM523134.1`), y nada en el medio `[M]`. Las dos
primeras son 133 porque la secuencia de EPILAB es una **subcadena exacta** de esos dos registros,
asi que ninguna ventana se pierde; la tercera se cae a 30 porque `KM523134.1` difiere lo
suficiente para que casi toda ventana de 21 nt tenga al menos un desajuste. Con un desajuste
permitido la tercera fila sube a 85, y sigue sin ser 114 `[M]`. Para que la fila valga 114 hace
falta un registro que difiera del que secuenciaron **en la medida justa**: mas parecido que
`KM523134.1` y no identico a `AF265566.2`. Ninguno de los 65 registros publicos lo es.

`CP_MRFV` tiene el problema inverso y es el mas duro de los cuatro. El declarado, 35, esta
**por encima** de nuestras 32 ventanas eficientes. La regla del original solo puede superar (a)
si alguna ventana eficiente pega dos o mas veces en la misma referencia, y eso es exactamente lo
que mide (e): contra las sesenta y cinco referencias de MRFV, **(e) = 0 en todas** `[M]`. La
fila mas alta de las sesenta y cinco es 32 y las demas bajan hasta 2. **Ninguna referencia de
MRFV puede dar 35 bajo esta regla**, ni con cero desajustes ni con uno. Ese numero no sale de la
referencia: sale del motor o del criterio.

## 5. Los tres mecanismos, ahora sobre datos reales

El reporte anterior tuvo que demostrar los tres casos que definen la regla con secuencias de
juguete, y lo justificaba bien: contra el gen mismo son imposibles. Con la matriz corrida los
tres aparecen en el corpus, y eso cambia el estatus de la demostracion.

| Consecuencia del fuente | Instancia real medida |
|---|---|
| 1. La ventana eficiente que **no pega** se pierde del conteo | `BicC_Dm` contra `GITV01000968.1`: 12 de 212. Contra `dmaid_genoma`: 21 de 212 `[M]` |
| 2. La que pega **solo en la hebra menos** no se evalua | `ATPaseD_Dm` contra `dmaid_genoma`: **40 de 42**, y la fila cae a 0 `[M]` |
| 3. La que pega **dos veces en la misma referencia** cuenta dos veces | `BicC_Dm` contra el gen mismo con `-v 1`: 3 ventanas, (b) = 215 sobre (a) = 212 `[M]` |

La demostracion sintetica de `resultados/ejemplo_formato_sintetico.md` se conserva porque sigue
sirviendo para lo que fue hecha —aislar cada mecanismo con un solo cambio controlado— pero deja
de ser la evidencia principal. La evidencia ahora es la tabla de arriba.

El caso 2 merece un parrafo propio porque no es solo una curiosidad del conteo. Si uno diseña
contra un transcriptoma y verifica contra un genoma, o al reves, el conteo de eficientes de un
gen anotado en la hebra reversa puede pasar de 42 a 0 sin que cambie una sola decision de diseño.
Eso es una trampa de la herramienta, no de nuestros datos, y afecta a cualquiera que use el
si-Fi21 original con una base genomica `[H]`. Va a `00_meta/CAMINOS_PROBADOS.md` y conviene
mencionarselo al investigador.

## 6. Control de orientacion: descartado, y con margen

El plan trata este control como barato y no lo es tanto: el complemento reverso cambia **las
ventanas**, no solo los aciertos, asi que hay que volver a correr el motor de eficiencia sobre el
gen invertido y recien despues contar. Hecho, con el mismo motor verificado:

| | `MP_MRFV` | `CP_MRFV` | `BicC_Dm` | `ATPaseD_Dm` | Distancia L1 |
|---|---|---|---|---|---|
| declarado | 114 | 35 | 199 | 33 | — |
| orientacion directa | 133 | 32 | 212 | 42 | **44** |
| complemento reverso | 47 | 22 | 108 | 52 | **190** |

El control queda **descartado con holgura** `[M]`. El complemento reverso no solo no acerca: se
aleja en un factor de cuatro, y mueve tres genes en el sentido equivocado. La orientacion de
entrada del laboratorio es la misma que la nuestra, que era la primera de las cuatro cosas que el
investigador pidio verificar y ahora esta verificada con un numero y no con un argumento. El
detalle esta en `resultados/orientacion.json`.

Vale notar por que el control es informativo a pesar de ser negativo: la asimetria es grande
—`BicC_Dm` cae a la mitad y `ATPaseD_Dm` sube— porque el criterio de si-Fi21 no es simetrico
respecto de la hebra. Un resultado parecido entre las dos orientaciones habria significado que el
control no distingue nada; este distingue mucho.

## 7. El eje del motor, cruzado con el de la referencia

El plan condiciona la tarea 4 —puntos intermedios del motor de accesibilidad— a que M1 no cierre
con la referencia. Cierra para un gen de cuatro, asi que el eje **vuelve a estar en juego** para
los otros tres, y conviene dejar medido lo que se puede medir sin instalar nada. Los dos ejes
nunca se habian cruzado: la ola 3 barrio el motor con una sola base y esta linea barrio la base
con un solo motor.

Con el backend `vienna` (ViennaRNA 2.7.2) en lugar de `exe` (RNAplfold 2.1.5), el mismo port y el
mismo modo `fiel` dan 142, 39, 223 y 35 eficientes `[M]`, que son los mismos cuatro numeros que
`sifi21INTA` reporta con la tabla `RNA_NN3`
(`research/ola3/C2_codigo_apolo_inta/corridas/04_resumen_base_datos.json`) — una concordancia que
vale como verificacion cruzada del port en un segundo punto. Cruzado con la referencia:

| Motor | Base | `MP_MRFV` | `CP_MRFV` | `BicC_Dm` | `ATPaseD_Dm` |
|---|---|---|---|---|---|
| declarado | — | **114** | **35** | **199** | **33** |
| RNAplfold 2.1.5 | gen mismo | 133 | 32 | 212 | 42 |
| RNAplfold 2.1.5 | publico de *D. maidis* | — | — | **200** | 42 |
| ViennaRNA 2.7.2 | gen mismo | 142 | 39 | 223 | **35** |
| ViennaRNA 2.7.2 | publico de *D. maidis* | — | — | 209 | **35** |

Lo que esto dice es incomodo y hay que decirlo asi: **cada gen tiene su mejor celda, y no son la
misma celda** `[M]`. `BicC_Dm` se acerca a 199 con el motor viejo (200) y se aleja con el nuevo
(209). `ATPaseD_Dm` se acerca a 33 con el motor nuevo (35) y se aleja con el viejo (42).
`CP_MRFV` queda encerrado: 32 con el viejo, 39 con el nuevo, y el declarado 35 justo en el medio.
`MP_MRFV` no se acerca con ninguno.

De ahi sale la conclusion que ordena el resto. **No existe una configuracion unica, entre las que
podemos construir, que reproduzca los cuatro numeros.** La combinacion mejor por gen da
(133, 32, 200, 35) y una distancia L1 de 25, contra los 44 de la celda de verificacion, pero esa
combinacion **mezcla dos motores distintos entre genes** y por lo tanto no es una corrida: es un
artefacto de elegir lo mejor de cada columna. Presentarla como explicacion seria el mismo error
que D45 registro con el umbral de 1,75, un barrido mas grande `[H]`.

## 8. La unidad de los dos campos, resuelta

El reporte anterior dejo abierto, como `[?]`, que en la fila de `BicC_Dm` contra `epilab4` el
resumen de la ola 3 dice `hits_bowtie: 2504` y `hits_blanco_principal: 2500` con una sola
referencia, y que cual campo esta en que unidad no se podia resolver leyendo el repositorio.
**Se resolvio midiendo.** La misma corrida en esta maquina, contra la misma base, da 2.504 lineas
de alineamiento y **2.500 nombres de lectura distintos** `[M]`. Asi que `hits_bowtie` cuenta
alineamientos y `hits_blanco_principal` cuenta ventanas. La confirmacion independiente esta en
`gitv01_blancos`: 2.357 alineamientos y 2.353 ventanas distintas, y 2.353 es exactamente el
numero que el resumen de la ola 3 declara para ese campo.

No hizo falta el driver sin versionar: hizo falta correr Bowtie una vez. La entrada de
`PREGUNTAS_ABIERTAS.md` se cierra y el pendiente de versionar los tres drivers de C2 queda igual,
por otras razones.

Esto tambien corrige un detalle de redaccion del reporte anterior, que leia la tabla de la ola 3
como si los campos fueran comparables entre si: los 2.353 de `BicC_Dm` y los 450 de
`ATPaseD_Dm` son ventanas, no aciertos, y por eso la regla de tres que estimaba «alrededor de
200» estaba hecha sobre la unidad correcta por casualidad y no por diseño.

## 9. Una correccion al plan y al issue, sobre una base mal nombrada

El plan de la ola 4 y el issue #5 describen `GCF_002217175.1` como «transcriptoma de
*D. maidis*». **No lo es.** La cabecera del primer registro del archivo dice *Folsomia candida*
`[M]`, que es el colembolo del panel de no objetivo, con peso 0,40 en D18. Las seis bases de
`work/offtarget_db/` incluyen el **genoma** de *D. maidis* pero **ningun transcriptoma** de
*D. maidis*; el que la ola 3 uso con el nombre `tsa_gitv01` es la ensambladura TSA `GITV01`, que
no esta en esa carpeta ni en el repositorio.

Esto no invalida ninguna medicion de la ola 3 —ahi la base se llamaba por su nombre— pero si
afecta a como se lee el inventario del plan, que cuenta «tres transcriptomas publicos de
*D. maidis*» cuando hay uno y no esta descargado. Queda corregido en el driver, en el issue y en
`PREGUNTAS_ABIERTAS.md`.

## 10. Lo que no corrio, y la limitacion de la herramienta

Dos cosas, y las dos se declaran en lugar de aproximarse.

**La ensambladura TSA completa de *D. maidis* no se bajo.** Lo que se uso son los **dos contigs**
que la ola 3 identifico como blanco principal, bajados por numero de acceso. Para la **fila de la
tabla** eso es exacto, y es lo que importa: una fila depende solo de su propia referencia. Lo que
queda subestimado es (d) —una ventana que no pega en `GITV01000968.1` podria pegar en otro contig
de la misma ensambladura— y por lo tanto `suma_filas`. La ola 3 midio que `BicC_Dm` toca seis
referencias de esa base y `ATPaseD_Dm` dos, asi que faltan cuatro y una; con la ensambladura
completa, la fila de 200 **no cambia** y el total si. La lista de los otros cinco contigs no esta
en el repositorio: es lo que habria que recuperar de `work/C2/` para completar la celda `[?]`.

**`bowtie -a -v 1` no corre contra las dos bases mas grandes.** El binario de 32 bits que trae
si-Fi2015 aborta con `Error reading _rstarts[] array` sobre un indice grande `[M]`. Con `-v 0`
corre bien en las once bases; con `-v 1` corre bien hasta `fcandida` (114 MB de FASTA) y aborta
en `zmays` (172 MB) y en `dmaid_genoma` (984 MB), asi que el limite esta entre 114 y 172 MB. Las
ocho celdas afectadas quedan registradas como fallidas en `resultados/procedencia.json` y
**ausentes** de `matriz_mm1.md`, no como ceros: el driver borra el archivo de salida cuando Bowtie
aborta, justamente para que una celda que no corrio no se lea como una que midio cero. Esa
distincion no es teorica —durante esta sesion una corrida fallida dejo un archivo vacio y la
celda aparecio como un cero medido en la primera version de la tabla—, y es la razon por la que
el driver ahora lo borra. Correrlas necesita un Bowtie de 64 bits, 1.3.x, que es el que tiene la
maquina de la ola 3.

## 11. Estado del criterio de terminado

| # | Criterio | Estado |
|---|---|---|
| 1 | El script reproduce los cuatro numeros verificados cuando la base es el gen mismo | **si.** Contra `epilab4`, (a) y (b) dan 133, 32, 212 y 42, con (d) = 0 y (e) = 0, y el invariante `--exigir-identidad` pasa `[M]` |
| 2 | Una tabla con una fila por base y los cuatro conteos | **si.** Once bases en `resultados/matriz.md`, con las tres agregaciones, el detalle por celda y la distancia L1; mas `matriz_mm1.md` y `matriz_vienna.md` |
| 3 | Esta dicho si alguna celda reproduce (114, 35, 199, 33) y, si ninguna, cual es la mas cercana y que dato falta | **si, y ninguna reproduce.** La mas cercana es `epilab4` con L1 = 44; con la referencia publica de *D. maidis* para los dos genes del insecto baja a 32. El dato que falta es su salida por ventana y el numero de acceso de su referencia de MRFV (seccion 12) |
| 4 | El control de orientacion esta corrido e informado | **si.** Descartado con L1 = 190 contra 44 `[M]` |

La tarea 4 del plan —puntos intermedios 2.4.x y 2.6.x del motor— **queda habilitada y no
corrida**. El plan la condicionaba a que M1 no cerrara con la referencia, y no cierra para tres
de los cuatro genes. Lo que esta linea agrega es el cruce de los dos ejes (seccion 7), que
muestra que el eje del motor mueve los numeros en direcciones **distintas segun el gen**, asi que
un barrido de versiones intermedias tiene ahora una pregunta concreta que contestar y no es un
barrido a ciegas. Instalar dos versiones mas de ViennaRNA es trabajo de la maquina de la ola 3.

## 12. Que cambia para el lunes

El pedido se afina por tercera vez y ahora tiene tres piezas, en orden de rendimiento.

**Uno, el mismo de siempre y sigue siendo el que mas rinde:** la salida por ventana de la corrida
`siFi21_8_1.0_0.1_1111`. Con eso la comparacion es exacta y las cuatro brechas se cierran o se
explican en una tarde.

**Dos, el numero de acceso de la referencia de Bowtie, por gen.** Esto ya estaba en el reporte
anterior, pero ahora se puede acompañar de una prediccion verificable, que es lo que lo hace util
preguntarlo: para `MP_MRFV`, **ninguno de los 65 registros publicos de MRFV da 114**. Las filas
posibles son 133, 133 y 30. Si nos dicen el acceso, o esta en esa lista —y entonces el conteo no
sale de la referencia— o es un aislamiento que no esta publicado, y entonces hace falta el
archivo. Preguntar asi es mejor que preguntar abierto: la respuesta discrimina.

**Tres, una pregunta nueva, que sale de la seccion 4:** si para los dos genes del insecto
corrieron contra un **transcriptoma** o contra el **genoma**. No es un detalle de bookkeeping. Si
fue contra el genoma, el conteo de `ATPaseD_Dm` que sale de la herramienta es **0**, porque el gen
esta en la hebra reversa y la regla del original solo evalua la hebra `+`; el 33 declarado no
podria salir de ahi. Y si fue contra un transcriptoma, queremos saber cual, porque el contig
publico `GITV01000968.1` da 200 para `BicC_Dm` contra sus 199 y eso es la unica coincidencia de
toda la matriz.

Lo que **no** conviene hacer es presentar la combinacion mejor por gen como si fuera una
explicacion. No es una corrida: mezcla motores entre genes, y la leccion de D45 es exactamente
esa.

## 13. Lo que falta, y en que orden

1. **Pedir las tres cosas de la seccion 12**, el lunes. Sin eso lo que se puede hacer es acotar,
   y acotar ya se hizo.
2. **Completar la celda de la ensambladura TSA** con los cinco contigs que faltan, que estan
   nombrados en `work/C2/` y no en el repositorio. Cambia `suma_filas` y (d), no la fila.
3. **Correr `-v 1` contra el genoma** con un Bowtie de 64 bits, en la maquina de la ola 3.
4. **Versionar los tres drivers de C2.** Sigue pendiente, pero ya no bloquea nada de esta linea:
   la pregunta que dependia de ellos se contesto midiendo (seccion 8).
5. **Los puntos intermedios del motor**, con la pregunta concreta de la seccion 7.

---

## Archivos

| Ruta | Que es |
|---|---|
| `scripts/conteo_por_acierto.py` | La regla del original. Tres subcomandos: `contar`, `ventanas`, `revcomp`. Solo biblioteca estandar |
| `scripts/correr_matriz.py` | El driver: del FASTA al conteo en un comando, con procedencia. Encuentra Bowtie y RNAplfold en el instalador de si-Fi2015 |
| `scripts/test_conteo_por_acierto.py` | 44 verificaciones con insumos sinteticos |
| `scripts/demo_sintetico.py` | Demostracion aislada de los tres mecanismos, con semilla fija |
| `resultados/matriz.md` y `.json` | La matriz con `-v 0`: once bases, tres agregaciones, detalle por celda |
| `resultados/matriz_mm1.md` y `.json` | Lo mismo con `-v 1` como sensibilidad, sin las celdas que Bowtie no pudo correr |
| `resultados/matriz_vienna.md` y `.json` | El cruce con el eje del motor (ViennaRNA 2.7.2) |
| `resultados/orientacion.md` y `.json` | El control de orientacion |
| `resultados/procedencia.json` | Versiones, bases corridas, bases ausentes, celdas fallidas |
| `resultados/verificacion_regla.txt` | Salida cruda de las 44 verificaciones |
| `resultados/ejemplo_formato_sintetico.md` | La demostracion de los mecanismos sobre secuencias de juguete |
