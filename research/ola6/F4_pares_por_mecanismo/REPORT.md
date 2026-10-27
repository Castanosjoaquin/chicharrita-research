# F4 — El eje de fenotipo de `F3`, conectado al enumerador de quimeras de `O4`

**Issue [#39](../../../../issues/39). Ola 6. Fecha: 2026-10-27.**
Criterio: [`PREREGISTRO.md`](PREREGISTRO.md), commiteado antes de enumerar un solo par
(`1562e46`). Entrada: la asignación de mecanismo de las 36 filas del catálogo de `C5` que dejó
`F3` en
[`eje_fenotipo.tsv`](../F3_recomendador_genes/resultados/eje_fenotipo.tsv), más
[`contraevidencia.tsv`](contraevidencia.tsv), que es **entrada** de esta línea y no salida suya
—la forma que `D68` le dio a las firmas de `M6`—. Las tres anclas del §6 pasan.
**Máquina:** la de Santino, Windows 11 Pro for Workstations 10.0.26300, Python 3.13.15. Esta
línea no lee ninguna secuencia y no usa ViennaRNA, `ahocorasick` ni alineador; la corrida de
verificación del enumerador sí, y se declara en §4.

## 1. Qué estaba desconectado, y qué se conectó

`O4` entrega el enumerador de quimeras y su propio informe dice que la parte difícil no es
enumerar sino qué quiere decir «la mejor», que terminó en su ADR. Y `D67` exige, para armar una
quimera, saber a qué mecanismo pertenece cada candidato. Hasta ahora eso no existía en forma
legible por máquina: las combinaciones de `O3` se eligieron a mano, por `D67` y por qué secuencia
había disponible, y el enumerador de `O4` recibía el eje de cada gen como dos cadenas escritas en
la línea de comandos. Era correcto mientras el eje no existiera, y su preregistro lo declaraba
así: «el eje de fenotipo es entrada declarada, no inferencia».

Lo que se conectó son dos piezas con una frontera deliberada entre ellas.

La primera es un **selector de pares**,
[`scripts/pares_por_mecanismo.py`](scripts/pares_por_mecanismo.py): pedile «uno de reproducción
con uno de letalidad» y devuelve los pares de candidatos elegibles leyendo la tabla. La segunda
es un **puente** en el enumerador de `O4`: `--mecanismos X,Y` con un `--candidato ID=NOMBRE` por
gen resuelve el eje de cada gen **desde la tabla** en vez de recibirlo escrito, y si el par
pedido no es elegible **no enumera nada**. Las dos vías son excluyentes: pasar `--eje` y
`--mecanismos` a la vez aborta, porque dejaría sin decidir cuál manda.

La frontera está donde está por un motivo que conviene decir: el selector trabaja sobre
**identificadores del catálogo** y el enumerador sobre **secuencias**, y de los 25 candidatos
elegibles sólo dos tienen el gen entero en esta máquina —`BicC_Dm` y `V-ATPase B`, en
`work/O3/fasta/`—. Un par elegible no es un par corrible, y mezclar las dos cosas en un solo
paso habría hecho que la falta de una secuencia se leyera como falta de elegibilidad.

## 2. La regla de elegibilidad, y lo que no puede aparecer

De las **36 filas** del catálogo, **25 son elegibles** y **11 quedan afuera por su etiqueta**
`[M]`: cinco sin fenotipo publicado, dos con mortalidad que su propia fuente desatribuye del
blanco (`HE-04` y `HE-08`, entrada 71), dos de signo invertido (`CI-08` y `CI-13`), el
potenciador de entrega sin fenotipo propio (`DM-04`) y una con un desenlace que no entra en
ninguno de los cuatro mecanismos (`HE-09`).

Lo que importa no es la lista: es de dónde sale. **Ningún identificador de candidato está
escrito en el código que decide.** La elegibilidad se deriva de tres columnas de la propia tabla
—`etiqueta_de_ausencia` vacía, `entra_al_orden_por_fenotipo` en `si`, `mecanismos` no vacío— y
las tres tienen que coincidir o la corrida **aborta**. Lo único declarado a mano es el
vocabulario de `F3`: sus cuatro mecanismos y sus cinco etiquetas. Si la tabla trae una etiqueta
que no está en esa lista, la corrida para y la nombra, porque una etiqueta nueva puede querer
decir «excluir» o «admitir» y el programa no tiene con qué decidirlo.

Esa forma no es una preferencia de estilo. Una lista de identificadores escrita a mano —aunque
sea correcta hoy— queda muerta cuando el catálogo cambia: sigue publicando la asignación vieja
sin romperse. Y acá la versión específica del problema es peor que un pendiente, porque dos de
las filas tienen el **signo invertido**: silenciar `CI-08` aumentó la colonización del vector por
el fitoplasma y silenciar `CI-13` aumenta la infección del sistema nervioso por el virus `[R]`.
Una quimera que los incluya es peor que no hacer nada, y `C5` ya los había marcado como «genes a
excluir explícitamente».

Las pruebas que sostienen esto son del §1, §2 y §9 de
[`scripts/test_pares.py`](scripts/test_pares.py), y conviene decir qué prueban exactamente:

- Los cinco que el issue nombra **no aparecen en ninguna** de las **694** asignaciones de rol
  que salen de los seis pares de los cuatro mecanismos, ni ninguna de las once filas excluidas
  `[M]`. Se prueba exhaustivamente y no por muestreo.
- Una fila **nueva** con `fenotipo_invertido` queda afuera sin tocar el código, y una fila hoy
  excluida que cambiara de etiqueta en la tabla **entraría**. Las dos mitades prueban lo mismo:
  la regla vive en la tabla.
- El AST del selector no tiene ningún identificador como literal en su código ejecutable. Es la
  forma de desactivar la regla sin tocarla —volver a escribir al lado la lista que reemplaza— y
  la prueba es del mismo tipo que la última de `test_alertas.py` §9, que existe por el mismo
  motivo.

## 3. Las tres anclas

Las tres del §6 del preregistro corren juntas en [`scripts/00_anclas.py`](scripts/00_anclas.py),
que devuelve 1 si alguna falla. Ninguna mide algo nuevo: las tres comparan lo que esta línea
deriva contra cifras y archivos que produjo otro código, y por eso valen.

1. **Contra el reparto publicado.** El respaldo de los cuatro mecanismos sobre las filas
   elegibles da **letalidad 16, reproducción 13, transmisión 4 y movilidad 1**, con 25 elegibles
   y 11 excluidas de 36 `[M]`. Reproduce la entrada 70 y el `REPORT.md` de `F3` §6, celda por
   celda.
2. **Contra las dos salidas de `F3`.** El conjunto de elegibles es **exactamente** el de las 25
   filas de `orden_genes.tsv` y el de excluidos **exactamente** el de las 11 de
   `fuera_del_orden.tsv` `[M]`. Es el ancla que prueba que la regla del §2 no es una lista que
   coincide por casualidad: se llega al mismo conjunto por otro camino y desde otro archivo.
3. **Contra `D67` y `O3`.** Pedido `reproduccion + movilidad` restringido a *Dalbulus maidis*, el
   **único** par elegible es `DM-01` cubriendo reproducción con `DM-02` cubriendo movilidad, y el
   eje que el puente resuelve es **idéntico** a la clave `ejes_declarados` del JSON commiteado de
   `O4` `[M]`. O sea que el camino nuevo reproduce el viejo en el único caso donde el viejo
   existe.

## 4. La corrida que importa: el puente reproduce el ancla de `O4` de punta a punta

El ancla 3 compara ejes, que es barato. Para que la conexión no quedara verificada sólo en la
resolución, se corrió el enumerador **completo** por la vía nueva sobre la grilla del ancla 2 de
`O4` —`BicC_Dm` 922-1221 y `V-ATPase B` 517-816, largo total 600, los dos órdenes— con el eje
resuelto desde la tabla y no escrito. Las siete referencias se escanearon de disco; la salida fue
a un directorio temporal y **ninguna de las tres salidas commiteadas de `O4` se regeneró**.

| Orden | heredadas ef. | juntura ef. | total | suma de las partes | fabricados ≥ 19 nt | alerta |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `BicC_Dm` + `V-ATPase B` | 38 | 2 | **40** | 40 | ninguno | no |
| `V-ATPase B` + `BicC_Dm` | 41 | 0 | **41** | 40 | 1, contra maíz, aporte 1 | sí |

`[M]` Los dos órdenes dan **40 y 41** ventanas eficientes contra **40** de la suma de las partes,
y el bloque fabricado de 19 nt aparece **sólo** en el orden `V-ATPase B` + `BicC_Dm`, contra
maíz, con aporte 1 del gen menos representado; el orden inverso fabrica cero. Es exactamente lo
que `D74` reportó y lo que el ancla 2 de `O4` exige. Las cuatro anclas propias de `O4` se
volvieron a correr después de la edición y pasan.

Dos detalles de forma que hacen que esto no mueva nada publicado: **ninguna columna se agregó ni
se sacó** —el `test_enumerador.py` de `O4` afirma la lista exacta a propósito y sigue pasando— y
la clave `par_por_mecanismo` del JSON aparece **sólo** cuando se usa la vía nueva, así que una
corrida por `--eje` sigue produciendo el mismo archivo.

## 5. Los pares, con sus dos cuentas

Los tres pares que `D67` permite, sobre las 25 filas elegibles `[M]`:

| Pedido | sostenido por | asignaciones de rol | pares de genes distintos | con mecanismos solapados | con las dos mitades en *D. maidis* |
| --- | --- | ---: | ---: | ---: | ---: |
| reproducción + letalidad | 13 y 16 | 201 | 180 | 147 | 4 |
| reproducción + movilidad | 13 y 1 | 13 | 13 | 7 | 1 |
| letalidad + movilidad | 16 y 1 | 15 | 15 | **15** | 3 |

Las dos cuentas de la derecha existen porque una sola engaña. Una **asignación de rol** es qué
candidato entra cubriendo qué mecanismo; un **par de genes** es la molécula. Cuando los dos
candidatos tienen los dos mecanismos pedidos, el mismo par de genes admite las dos asignaciones y
son dos filas, porque el eje declarado de cada gen es distinto en cada una y es lo que `O4`
escribe en sus columnas. Por eso 201 asignaciones son 180 moléculas, y leer 201 como «201
quimeras posibles» sería contar veintiuna dos veces.

Y las tres filas de la tabla tampoco se suman sin cuidado: los tres pedidos dan **229**
asignaciones de rol, pero los pares de genes **globalmente distintos** son **188** y no 208,
porque un mismo par puede ser elegible bajo dos pedidos `[M]`. `DM-01` + `DM-02` es el ejemplo
que ya conocemos: elegible como reproducción + movilidad y también como reproducción +
letalidad, porque `DM-02` tiene los dos mecanismos. Trece pares de genes están en más de un
pedido `[M]`.

El par **no está ordenado**: que el fragmento izquierdo sea uno o el otro es un grado de libertad
de la grilla de `O4`, que lo enumera, y está medido que cambia el resultado —la tabla del §4 lo
muestra en el caso más concreto posible: un orden fabrica un bloque contra maíz y el otro no—.

## 6. Las cuatro cosas que hay que saber antes de usar estos pares

**`movilidad` es una sola fila, y su réplica más cercana está en contra.** De los 25 elegibles,
uno solo sostiene movilidad: `DM-02`, con la frase «alas deformes» y sin magnitud ni estadístico.
`DM-03` es la otra subunidad de la misma bomba, en la misma especie y con la misma vía de
entrega, y ahí el efecto sobre alas **se midió y no dio significativo** `[M]`. Eso viaja en cada
fila de la salida —el respaldo del rol, el `si` de «descansa en un solo candidato» y la frase de
la contraevidencia, verificada textual contra la tabla— y lo imprime también el enumerador cuando
se le pide un par con movilidad. La lectura es la de la entrada 70 y no es nuestra de ahora: si
las quimeras se arman combinando mecanismos que no se solapan, una de las tres patas del esquema
se apoya en una fila cuya replicación más cercana falló `[H]`.

**Toda combinación «letalidad + movilidad» tiene los mecanismos solapados, y no puede no
tenerlos.** Las **15 de 15** `[M]`. El motivo es aritmético y por eso es inevitable: el único
candidato de movilidad **también** tiene letalidad, así que cualquier par que lo use para la pata
de movilidad trae letalidad por partida doble. Los dos ejes *declarados* son distintos —que es lo
que `D67` pide y lo que `O4` verifica— pero los conjuntos de mecanismos se solapan siempre, y
entonces la segunda pata agrega menos de lo que su rótulo promete `[H]`. La salida lo informa por
par y no descarta nada: cambiar la lectura de `D67` de «ejes declarados distintos» a «conjuntos
de mecanismos disjuntos» movería un criterio vigente y no es de esta línea.

**Casi ningún par tiene las dos mitades en nuestra especie.** De las 229 asignaciones de los tres
pares de `D67`, **8** tienen las dos mitades en *Dalbulus maidis* `[M]`: cuatro de reproducción +
letalidad (`DM-01` con cada uno de `DM-02`, `DM-03`, `DM-05`, `DM-06`), una de reproducción +
movilidad (`DM-01` + `DM-02`, que es la quimera de `O3`) y tres de letalidad + movilidad
(`DM-03`, `DM-05` o `DM-06` con `DM-02`). Las otras 221 tienen al menos una mitad medida en otra
especie, y eso no las descalifica pero cambia lo que son: una quimera sobre el **ortólogo** en
nuestra especie, que hay que tener y anotar —es la línea `F1`, con su banda de concordancia— y no
sobre el gen medido. La columna de especie de cada mitad está en todas las filas.

**Una fila del catálogo no siempre es un gen.** De las 201 asignaciones de reproducción +
letalidad, **63** involucran una fila que agrupa varios genes `[M]`. `DE-01` es `V-ATPase B` **y**
`V-ATPase D`; `DE-04` agrupa tres transportadores ABC con desenlaces **distintos**, donde la
letalidad es de dos de ellos y la reproducción del tercero; `CI-09` agrupa tres genes y además
dos especies; `CI-11` agrupa dos lacasas y el desenlace descrito es del primero. Una quimera se
arma con un gen, así que esas filas no son directamente un insumo del enumerador: hay que abrir
la fuente y decir cuál de los genes es. La detección se hace con dos detectores sobre la fila —la
frase `fila que agrupa` de la nota, que el script de `F3` ya verificó contra la fuente, y la
forma del campo `gen`— y si los dos no coinciden sobre una fila elegible la corrida **aborta**.
Hoy coinciden en las 25.

## 7. El cuarto mecanismo, medido sin adoptarlo, y lo que la medición muestra

`F3` publica `transmision` como categoría declarada con cuatro candidatos y `D67` define tres. La
entrada 65 dice que ampliar `D67` no es de esa línea, y tampoco es de ésta. Pero medir no es
adoptar: un pedido que incluya transmisión **aborta** nombrando que falta el ADR, y con
`--ampliar-d67` corre con la condición estampada en **cada** fila de la salida
(`ampliacion_de_d67_sin_adr = si`), en el encabezado del JSON y en lo que imprime. Es la misma
forma que `O4` le dio a la advertencia de `eficiencia_heredada`.

Medido así, la ampliación da **118** asignaciones de rol: 51 de reproducción + transmisión, 63 de
letalidad + transmisión y 4 de movilidad + transmisión `[M]`. Y aparece el número que esta línea
agrega a la pregunta de la entrada 70:

> De los cuatro candidatos de transmisión, **ninguno es de *Dalbulus maidis*** `[M]`. Los cuatro
> son de *Euscelidius variegatus* (tres, uno de ellos compartido con *Scaphoideus titanus*) y de
> *Peregrinus maidis*. Así que **ninguna** de las 118 combinaciones con transmisión tiene las dos
> mitades medidas en nuestra especie —cero de 51, cero de 63 y cero de 4—, contra 8 de las 229
> del esquema de tres mecanismos.

Eso le pone una contracara a la lectura que la entrada 70 dejaba planteada. El argumento a favor
de transmisión era que tiene cuatro veces más candidatos que movilidad y que corta la cadena en
vez de reducir la población, que es lo más alineado con el objetivo sanitario. Sigue en pie. Lo
que la medición agrega es el costo: adoptar transmisión como tercera pata cambia la pata que
descansa en **una fila de nuestra especie** por una que descansa en **cuatro filas de otras
especies** `[M]`, con la transferencia de ortología en el medio. No es un argumento en contra;
es el otro platillo, y la decisión es del equipo y del investigador con su propio ADR `[H]`.

## 8. Lo que esta línea no hace

No recomienda ningún par: enumera y mide, no hay puntaje, no hay puesto y el orden de las filas
es alfabético por identificador y no significa nada. La prueba §7 lo verifica sobre los nombres
de las columnas, para que no se cuele una.

No afirma eficacia. Hereda la condición de toda la cadena: el criterio de eficiencia de si-Fi21
**no está validado** en hemípteros —ρ = +0,142, IC95 [−0,247, +0,492], n = 29 `[M]`— así que un
par elegible es una hipótesis sobre eficacia y no una prueba.

No decide si movilidad sigue siendo una pata del esquema ni si el tercer eje debería ser
transmisión; deja las dos cosas medibles. No amplía `D67` y no escribe el ADR que la ampliación
pediría. No cambia la lectura de «fenotipos que no se solapan» que `O4` implementa. Y no toca
ninguna cifra publicada: las tres salidas de `O4` no se regeneraron, nada de
`tools/sifi21_port/` cambió y todas las salidas de este bloque son archivos nuevos.

Y falta un paso que esta línea no puede saltear y que conviene no perder de vista: antes de que un
par se vuelva una recomendación tiene que pasar por el inventario de alertas de `M6`, y la clave
de juntura que `D78` le dio a una quimera **todavía no está implementada** (entrada 41, issue #35
parte 3). Hoy una quimera puede pasar la compuerta con su empalme sin tamizar, y la salida declara
esa condición en lugar de taparla.

## 9. Cómo reproducirlo

```
python research/ola6/F4_pares_por_mecanismo/scripts/00_anclas.py
python research/ola6/F4_pares_por_mecanismo/scripts/test_pares.py
python research/ola6/F4_pares_por_mecanismo/scripts/pares_por_mecanismo.py \
    --mecanismos reproduccion,letalidad \
    --mecanismos reproduccion,movilidad \
    --mecanismos letalidad,movilidad
python research/ola6/F4_pares_por_mecanismo/scripts/pares_por_mecanismo.py \
    --ampliar-d67 --nombre d67_mas_transmision \
    --mecanismos reproduccion,transmision \
    --mecanismos letalidad,transmision \
    --mecanismos movilidad,transmision
python research/ola6/F4_pares_por_mecanismo/scripts/pares_por_mecanismo.py \
    --especie "Dalbulus maidis" --nombre solo_dmaidis \
    --mecanismos reproduccion,letalidad \
    --mecanismos reproduccion,movilidad \
    --mecanismos letalidad,movilidad
```

Los tres son deterministas, no leen nada de `work/` y no necesitan más que la biblioteca
estándar: la entrada es material versionado. La corrida del §4, que sí necesita las secuencias y
las siete referencias de `work/`, es:

```
python research/ola6/O4_enumerador_quimeras/scripts/enumerar_quimeras.py \
    --gen BicC_Dm=work/O3/fasta/BicC_Dm_full.fasta:922-1221 \
    --gen VATPaseB_Dm=work/O3/fasta/VATPaseB_Dm_full.fasta:517-816 \
    --candidato DM-01=BicC_Dm --candidato DM-02=VATPaseB_Dm \
    --mecanismos reproduccion,movilidad \
    --largo-total 600 --l1-min 300 --l1-max 300 --paso 1 \
    --objetivo cobertura_fenotipica --nombre puente_f4 --resultados <temporal>
```

El `--resultados <temporal>` no es decorativo: sin él la corrida escribiría en
`research/ola6/O4_enumerador_quimeras/resultados/` con otro nombre de archivo, y lo que esta
línea no quiere es dejar salidas nuevas en el bloque de otra.
