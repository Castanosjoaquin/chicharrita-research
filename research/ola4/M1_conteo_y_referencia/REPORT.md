# M1 — Reconciliacion de conteos: la regla quedo implementada y verificada, la matriz de bases no se pudo correr aca

**Ola 4, linea M1.** La pregunta que abre esta linea viene de la carta del investigador del 22
de octubre de 2026 y de lo que aparecio al seguir su pista hasta el fuente: la columna
«Efficient siRNA hits» del si-Fi21 original no cuenta ventanas, cuenta aciertos de Bowtie, asi
que comparar nuestros 133, 32, 212 y 42 contra los 114, 35, 199 y 33 de la planilla fue, desde
el principio, comparar dos unidades distintas. M1 tenia que medir cuanto de la brecha explica
esa diferencia de unidad y cual es la referencia que la produce.

**Lo que se entrega, en una linea.** La regla de conteo del original esta implementada en
`scripts/conteo_por_acierto.py` y verificada con 29 pruebas sobre insumos sinteticos que cubren
los tres casos que la hacen interesante `[M]`. **La matriz de bases no corrio**, y no por falta
de tiempo: la maquina donde se ejecuto esta linea no tiene ni las secuencias ni las herramientas
que la matriz necesita, y eso se declara abajo con nombre y apellido en vez de resolverse con
una corrida aproximada. Lo que si se pudo hacer sin ningun insumo nuevo fue acotar la hipotesis
con numeros que la ola 3 ya habia medido, y el resultado de ese acotamiento cambia la pregunta
que conviene hacer el lunes.

---

## 1. La regla, tal como quedo implementada

La lectura del fuente es la de la seccion 3 del plan de la ola 4 y no se repite aca. Lo que
importa para el codigo son tres frases, las tres `[R]`:

En `general_helpers.py:107-123`, `get_table_data` arma la tabla con
`Counter(player['hit_name'] for player in query if player['is_efficient'])`: **un registro por
acierto**, agrupado por el nombre de la referencia. En `sifi_pipeline.py:195-221`, si no hay
acierto el registro sale con `hit_name = False` y `strand = None`. Y como todo el bloque de
eficiencia vive dentro de `if strand == '+'`, una ventana sin acierto y una que pego solo en la
hebra menos **nunca se evaluan**.

El script devuelve, por cada par de gen y base, los cinco numeros que pide la tarea 1 y ademas
la tabla desagregada por referencia, que es la unidad en la que el original presenta sus filas:

| Numero | Que es | Depende de la base |
|---|---|---|
| (a) `eficientes_por_ventana` | ventanas eficientes, una fila por ventana | no |
| (b) `aciertos_mas_total` | registros por acierto en la hebra `+`, la regla del original | si |
| (c) `aciertos_cualquier_hebra_total` | lo mismo sin el filtro de hebra | si |
| (d) `eficientes_sin_acierto` | ventanas eficientes que no pegan en ninguna parte | si |
| (e) `eficientes_con_acierto_multiple_en_una_ref` | ventanas eficientes que pegan dos o mas veces en la misma referencia | si |

Hay una decision de diseno que conviene dejar explicita, porque es la que hace el resultado
interpretable incluso si la hipotesis falla. **No sabemos que fila de la tabla leyo el
laboratorio**, y con una base de 71 registros la tabla del original tiene hasta 71 filas. Asi
que el script no elige: reporta tres agregaciones en paralelo y ninguna se declara la verdadera
—`suma_filas`, la suma de todas las filas; `fila_max`, la fila mayor, que es el orden en que el
original presenta la lista; y `fila_homonima`, la unica fila cuya referencia nombra al gen, que devuelve `None` si hay dos,
porque dos filas sumadas no son una fila— y calcula la distancia L1 de cada una al vector
declarado. Si alguna celda reproduce (114, 35, 199, 33),
queda dicho con que agregacion; si ninguna, queda dicho cual es la mas cercana y bajo que
supuesto.

El script tambien resuelve una dependencia que, en esta linea, era un riesgo: **no necesita
Bowtie**. Toma los aciertos de una salida de Bowtie (`-a -v 0`, o `-v 1` como sensibilidad), en
formato nativo o SAM, o los enumera localmente contra un FASTA. Con cero desajustes la
enumeracion local es lo que reporta `bowtie -a -v 0` —todas las coincidencias perfectas de
extremo a extremo, en las dos hebras— y se indexa la consulta recorriendo la referencia una sola
vez, que es el criterio que ya usa `tools/sifi21_port/offtarget_21nt.py`. Con un desajuste
equivale a `-a -v 1` por el palomar sobre dos mitades, y es correcto pero lento: sirve para
bases chicas, no para un genoma. La celda de verificacion, que es el gen contra si mismo, entra
holgada en el camino local.

Esa equivalencia se apoya en tres restricciones, y conviene leerlas antes de usar el camino
local en lugar de Bowtie, porque son el lugar donde «equivalente» quiere decir «equivalente bajo
un supuesto declarado»:

- **Alfabeto.** Solo ACGTN. Un codigo IUPAC ambiguo aborta la corrida en vez de complementarse
  mal en silencio, que es lo que haria la tabla de complemento con una R o una Y. Los cuatro
  genes de EPILAB son ACGT en mayusculas `[M]`, asi que la restriccion no muerde en el caso real.
- **N.** Ni una ventana con N ni un tramo de la referencia con N entran a la comparacion. Es lo
  correcto y no una simplificacion: una N no aparea, asi que no puede haber un alineamiento
  perfecto sobre ella, y comparar `N == N` habria inventado aciertos que Bowtie no reporta. Las
  ventanas con N quedan contadas en (d), que es lo que tambien les pasaria con Bowtie. Con
  `--mm 1` la regla es algo mas estricta que Bowtie, que por `--nceil` tolera algunas N en la
  lectura y podria gastar su unico desajuste en una `[?]`.
- **Palindromos.** Una ventana igual a su propio complemento reverso se indexa solo en la hebra
  `+`: es el mismo alineamiento y emitirlo dos veces inflaria (c). Con ventanas de 21 nt el caso
  es imposible —la base del medio tendria que ser su propio complemento— asi que la restriccion
  es para largos pares.

Las dos primeras no estaban en la primera version del script y las encontro la revision; las
tres estan verificadas con pruebas.

## 2. Una correccion al criterio de terminado, antes de usarlo

El criterio (a) del plan dice que, contra una base que es el gen mismo, el conteo por ventana y
el conteo por acierto **tienen que coincidir**. Eso no es cierto en general, y el propio
proyecto tiene el contraejemplo medido: en `BicC_Dm`, Bowtie reporta **2.504 aciertos para 2.500
ventanas** `[M]`
(`research/ola3/C2_codigo_apolo_inta/diff_sifi21INTA_vs_original.md`, fila 3). Si un 21-mero del
gen esta repetido, la ventana que lo contiene pega dos veces contra el gen mismo y el conteo por
acierto queda **por encima** del conteo por ventana.

El invariante que si se cumple siempre, y que el script verifica con `--exigir-identidad`, es
otro: contra el gen mismo **ninguna ventana eficiente puede quedar sin acierto en la hebra `+`**,
porque la ventana es, literalmente, un trozo de la referencia. Y el exceso de (b) sobre (a) es,
exactamente, la cantidad de aciertos de mas que caen sobre ventanas eficientes. Formulado asi, el
criterio es verificable y sigue sirviendo para lo que estaba pensado: si (d) no da cero contra el
gen mismo, el script esta mal o los insumos no corresponden, y aborta.

Esto no es una objecion menor al plan: es el mismo error de unidad que M1 vino a medir,
reapareciendo en el criterio con el que ibamos a cerrarla.

## 3. Verificacion

Las pruebas corren con la biblioteca estandar, sin ViennaRNA, sin Biopython y sin Bowtie, asi
que cualquier integrante las puede correr en su maquina:
`python scripts/test_conteo_por_acierto.py`. **44 pruebas, las 44 pasan**; la salida cruda esta
en `resultados/verificacion_regla.txt` `[M]`.

Lo que cubren, en orden de importancia: que una ventana eficiente que no pega se pierde del
conteo; que una que pega solo en la hebra menos no entra en (b) y si en (c); que una que pega
dos veces en la misma referencia cuenta dos veces; que una ventana no eficiente no cuenta por
mas aciertos que tenga; que dos referencias reparten el conteo en dos filas y que eso mueve
`suma_filas` y `fila_max` en sentidos distintos; que los formatos nativo y SAM de Bowtie dan el
mismo conjunto de aciertos; que la enumeracion local encuentra las repeticiones, encuentra la
hebra menos y no inventa la ventana que no esta; y que, contra el gen mismo, ninguna eficiente
queda sin acierto.

Quince de esas pruebas salieron de una revision del script y cubren formas de fallar en silencio,
que es la clase de error que importa cuando el numero que sale va a un reporte: una posicion
repetida en el TSV, una ventana sin secuencia, un codigo IUPAC, una N, un nombre de lectura
ambiguo —`w12_2` le asignaba el acierto a la ventana 2— y dos referencias que nombran al mismo
gen, que no son una fila aunque se puedan sumar. Las seis abortan o devuelven `None` en vez de
dar un numero plausible y equivocado.

Por que las pruebas usan secuencias de juguete y no las de EPILAB. Los tres casos que definen la
regla **no aparecen** cuando la base es el gen mismo, que es la unica base que tenemos
verificada: una ventana que no pega y una que pega solo en la hebra menos son imposibles contra
el propio gen. Construirlos a mano es la unica forma de probar la implementacion antes de
aplicarla, y es lo que vuelve interpretable el numero que salga despues.

Sobre eso hay una demostracion del mecanismo que vale leer, en
`resultados/ejemplo_formato_sintetico.md`, generada por `scripts/demo_sintetico.py` con una
secuencia al azar de semilla fija: 40 ventanas, 10 eficientes. Contra el gen mismo la regla da
10. Contra un isolado con **una sola sustitucion** en el medio, da **5**, porque las ventanas que
cubren esa posicion dejan de pegar con `-v 0`. Contra una referencia que repite un tramo de 25
nt del gen, da **12**. `[M]` con insumos sinteticos. Son los dos signos que hacen falta para
explicar la forma del desajuste de la planilla, que baja en tres genes y sube en uno, y quedan
demostrados sobre el mecanismo. Lo que no demuestran es que ese sea el mecanismo del caso real:
eso es `[H]` y lo mide la matriz.

## 4. Por que la matriz de bases no corrio, y donde tiene que correr

La maquina donde se ejecuto esta linea **no tiene ninguno de los cuatro insumos** que la matriz
necesita, y conviene que quede escrito con precision porque afecta a varias lineas de la ola 4,
no solo a esta:

1. **No existe `work/`.** Esta en `.gitignore` por la regla de confidencialidad, asi que los
   cuatro FASTA de EPILAB, el TSV por ventana del port y las seis bases de `work/offtarget_db/`
   no estan.
2. **No hay Bowtie ni BLAST+.**
3. **No hay ViennaRNA ni Biopython**, asi que el port tampoco puede generar el TSV por ventana
   desde cero.
4. **No esta instalado si-Fi21**, asi que el backend `exe` con RNAplfold 2.1.5 —el unico que
   reproduce los 133, 32, 212 y 42 del original— no es alcanzable.

Esto no es un hallazgo nuevo, es una consecuencia de como se reparte el trabajo: las corridas de
la ola 3 se hicieron en otra maquina, y su propio registro lo dice
(`research/ola3/C2_codigo_apolo_inta/corridas/README.md`: Darwin arm64, entorno conda `c2sifi`,
Bowtie 1.3.1, ViennaRNA 2.7.2). Los `scripts/run_inta.py`, `run_db.py` y `barrido_inta.py` que
ese README documenta **viven en `work/C2/` y no estan versionados**, asi que tampoco se pueden
releer desde el repositorio.

La matriz queda entonces como **pendiente declarado**, no como resultado nulo. La diferencia
importa: un nulo seria haber corrido las celdas y que ninguna reproduzca los cuatro numeros, y
eso todavia no se sabe. Lo que sigue es la secuencia exacta, para correrla en la maquina que
tiene el corpus:

```bash
# 1. el TSV por ventana, en modo fiel y con el backend que corresponda
python tools/sifi21_port/run_sifi.py work/sifi_check/{MP_MRFV,CP_MRFV,BicC_Dm,ATPaseD_Dm}_full.fasta \
    --modo fiel --backend exe --salida work/M1/port_fiel

# 2. el FASTA de ventanas que alimenta a Bowtie, con el nombre `w<pos>`
for g in MP_MRFV CP_MRFV BicC_Dm ATPaseD_Dm; do
  python research/ola4/M1_conteo_y_referencia/scripts/conteo_por_acierto.py ventanas \
      --tsv work/M1/port_fiel/${g}_full.tsv --salida work/M1/ventanas/${g}.fasta
done

# 3. Bowtie, una corrida por base y por gen, con todos los aciertos
bowtie -a -v 0 -f work/offtarget_db/indices/tsa_gitv01 work/M1/ventanas/BicC_Dm.fasta \
    > work/M1/hits/tsa_gitv01_BicC_Dm.txt

# 4. la regla del original sobre la matriz
python research/ola4/M1_conteo_y_referencia/scripts/conteo_por_acierto.py contar \
    --gen MP_MRFV=work/M1/port_fiel/MP_MRFV_full.tsv \
    --gen CP_MRFV=work/M1/port_fiel/CP_MRFV_full.tsv \
    --gen BicC_Dm=work/M1/port_fiel/BicC_Dm_full.tsv \
    --gen ATPaseD_Dm=work/M1/port_fiel/ATPaseD_Dm_full.tsv \
    --aciertos tsa_gitv01:BicC_Dm=work/M1/hits/tsa_gitv01_BicC_Dm.txt \
    --base epilab4=work/C2/runs/epilab_full.fasta \
    --exigir-identidad epilab4 \
    --json research/ola4/M1_conteo_y_referencia/resultados/matriz.json \
    --md   research/ola4/M1_conteo_y_referencia/resultados/matriz.md

# 5. control de orientacion: el complemento reverso de cada gen, y de ahi otra vez al paso 1
python research/ola4/M1_conteo_y_referencia/scripts/conteo_por_acierto.py revcomp \
    --fasta work/sifi_check/BicC_Dm_full.fasta --salida work/M1/revcomp/BicC_Dm_full.fasta
```

El paso 5 merece una aclaracion, porque el plan lo trata como barato y es un poco menos barato
de lo que parece: el complemento reverso cambia **las ventanas**, no solo los aciertos, asi que
el control de orientacion obliga a volver a correr el motor de eficiencia sobre el gen dado
vuelta y recien despues contar. El script escribe el FASTA invertido; el costo esta en el paso 1.

Confidencialidad: el TSV del port y el FASTA de ventanas contienen secuencias de EPILAB, y por
eso los dos van a `work/` y nunca a `research/`. El script no sube nada a ninguna parte: Bowtie
y la enumeracion local son locales.

## 5. Lo que si se puede acotar hoy, con numeros ya medidos

Sin correr nada nuevo, la corrida 4 de C2 ya midio contra que referencia pega cada gen en tres
bases, y eso alcanza para descartar una parte del espacio de hipotesis. La tabla, con la de
energia por defecto `[M]`
(`research/ola3/C2_codigo_apolo_inta/corridas/04_resumen_base_datos.json`):

| Gen | Base | Ventanas | Aciertos totales | Referencias | Blanco principal | Aciertos del blanco principal |
|---|---|---|---|---|---|---|
| `MP_MRFV` | `epilab4` | 1.243 | 1.243 | 1 | `MP_MRFV_full` | 1.243 |
| `MP_MRFV` | `mrfv_all` | 1.243 | 2.841 | 4 | `NC_002786.2` | 1.243 |
| `CP_MRFV` | `epilab4` | 508 | 508 | 1 | `CP_MRFV_full` | 508 |
| `CP_MRFV` | `mrfv_all` | 508 | 11.019 | 65 | `AF265566.2` | 508 |
| `BicC_Dm` | `epilab4` | 2.500 | 2.504 | 1 | `BicC_Dm_full` | 2.500 |
| `BicC_Dm` | `tsa_gitv01` | 2.500 | 2.430 | 6 | `GITV01000968.1` | 2.353 |
| `ATPaseD_Dm` | `epilab4` | 471 | 471 | 1 | `ATPaseD_Dm_full` | 471 |
| `ATPaseD_Dm` | `tsa_gitv01` | 471 | 736 | 2 | `GITV01001458.1` | 450 |

De ahi salen tres cosas.

**Contra el gen mismo, la regla del original no puede bajar el conteo.** Toda ventana pega al
menos una vez, asi que (b) es mayor o igual que (a). La base `epilab4` no puede producir 114
partiendo de 133, ni 199 partiendo de 212, ni 33 partiendo de 42: solo puede producir numeros
iguales o mayores. Para que la regla explique una **baja** hace falta una referencia en la que
ventanas eficientes **no peguen**, y eso es una propiedad de la referencia, no del criterio
`[H]`.

**En los dos genes del insecto, el transcriptoma publico de *Dalbulus maidis* pierde ventanas, y
en la direccion correcta.** El blanco principal de `BicC_Dm` en `tsa_gitv01` recibe 2.353 de
2.500, y el de `ATPaseD_Dm`, 450 de 471 `[M]`. Si la proporcion de perdida fuera parecida entre
las ventanas eficientes, la fila de ese blanco caeria de 212 a alrededor de 200 y de 42 a
alrededor de 40, contra los 199 y 33 declarados. El primero cae casi exacto; el segundo se queda
corto. Eso es aritmetica de servilleta y no reemplaza la medicion, porque la perdida no tiene
por que repartirse igual entre eficientes y no eficientes: es justo lo que mide (d) por gen y por
base `[H]`.

**En los dos genes virales, ninguna base medida pierde una sola ventana.** El blanco principal de
`MP_MRFV` en `mrfv_all` es `NC_002786.2` y recibe las 1.243; el de `CP_MRFV` es `AF265566.2` y
recibe las 508 `[M]`. O sea que las secuencias de EPILAB son subcadenas exactas de esos dos
registros publicos, y contra ellos la regla del original tampoco puede bajar el conteo. Para que
`MP_MRFV` baje de 133 a 114 hace falta una referencia que **difiera** de la secuencia que
diseñaron: otro aislamiento de MRFV, no el conjunto completo de registros publicos. Y la
demostracion sintetica de la seccion 3 muestra que **una sola sustitucion** alcanza para sacar
de la tabla a las veintiuna ventanas que la cubren, lo que convierte a esa hipotesis en una que
mueve numeros del orden de la brecha.

Eso reordena el pedido del lunes. La pregunta no es solo «contra que base corrieron el diseño»,
sino **contra que registro**, con su numero de acceso o su archivo: para los dos genes virales,
la unica forma de que la regla por acierto baje el conteo es que la referencia sea un aislamiento
distinto del que ellos secuenciaron.

## 6. Una inconsistencia de unidad en nuestro propio resumen

Mientras se leia esa tabla aparecio algo que conviene registrar, porque es el mismo problema de
M1 un nivel mas abajo. En la fila de `BicC_Dm` contra `epilab4`, el resumen dice
`hits_bowtie: 2504` y `hits_blanco_principal: 2500`, **con una sola referencia** `[M]`. Con una
sola referencia los dos campos deberian ser el mismo numero, asi que **no estan en la misma
unidad**: uno cuenta alineamientos y el otro, casi con seguridad, ventanas. Cual es cual no se
puede resolver desde el repositorio, porque el driver que los calculo (`work/C2/scripts/run_db.py`)
no esta versionado `[?]`. Queda anotado en `00_meta/PREGUNTAS_ABIERTAS.md`. No invalida nada de
lo que esta arriba —los 2.353 y los 450 son del mismo campo y se comparan entre si— pero sin
resolverlo esos dos numeros no se pueden mezclar con los aciertos de Bowtie en una sola cuenta.

## 7. Estado del criterio de terminado

| # | Criterio | Estado |
|---|---|---|
| 1 | El script reproduce los cuatro numeros verificados cuando la base es el gen mismo | **parcial.** La regla esta implementada y el invariante correcto esta verificado con insumos sinteticos; la celda real necesita el TSV del port sobre las secuencias de EPILAB. Y el criterio, como estaba escrito, era falso: ver seccion 2 |
| 2 | Una tabla con una fila por base y los cuatro conteos | **no.** El formato esta fijado y demostrado en `resultados/ejemplo_formato_sintetico.md`; las celdas reales no corrieron |
| 3 | Esta dicho si alguna celda reproduce (114, 35, 199, 33) | **no**, y no se finge. Lo que si esta dicho es que `epilab4` y `mrfv_all` **no pueden** reproducirlo por una razon estructural, y que el candidato vivo es un registro distinto del que secuenciaron (seccion 5) |
| 4 | El control de orientacion esta corrido e informado | **no.** El subcomando esta escrito y probado; correrlo necesita el motor de eficiencia sobre el gen invertido |

La tarea 4 del plan —los puntos intermedios del motor de accesibilidad, 2.4.x y 2.6.x— **no
corresponde todavia**: el plan la condiciona a que M1 no cierre con la referencia, y M1 no
cerro ni fallo, quedo sin correr. Abrir ese eje ahora seria exactamente el error que D45 acaba de
registrar.

## 8. Lo que falta, y en que orden

1. **Correr los pasos 1 a 5 de la seccion 4 en la maquina que tiene el corpus.** Es la mitad que
   falta de esta linea y no necesita ninguna decision.
2. **Pedir el lunes la salida por ventana de la corrida `siFi21_8_1.0_0.1_1111`** y, con el
   detalle que agrega la seccion 5, **el numero de acceso o el archivo de la referencia de
   Bowtie contra la que corrieron el diseño**, por gen. Con eso la comparacion es exacta.
3. **Resolver la unidad de los dos campos de `04_resumen_base_datos.json`** (seccion 6), que
   cuesta minutos en la maquina que tiene `work/C2/`.
4. **Versionar los tres drivers de C2** que hoy viven solo en `work/`. No es de esta linea, pero
   es la razon por la que el punto 3 no se pudo contestar leyendo el repositorio.

---

## Archivos

| Ruta | Que es |
|---|---|
| `scripts/conteo_por_acierto.py` | La regla del original. Tres subcomandos: `contar`, `ventanas`, `revcomp`. Solo biblioteca estandar |
| `scripts/test_conteo_por_acierto.py` | 29 verificaciones con insumos sinteticos |
| `scripts/demo_sintetico.py` | Demostracion de los dos mecanismos, con semilla fija |
| `resultados/verificacion_regla.txt` | Salida cruda de las verificaciones |
| `resultados/ejemplo_formato_sintetico.md` | El formato de la tabla de la matriz, sobre secuencias de juguete |
