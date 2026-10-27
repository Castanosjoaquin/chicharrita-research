# O4 — El enumerador de quimeras como feature: dos genes, un largo total y un objetivo declarado

**Línea:** `O4` del plan de la ola 6, issue #24. **Fecha:** 2026-10-27.
**Qué entrega:** una feature que recibe dos genes y un largo total, enumera todas las
combinaciones de la grilla y las ordena bajo un objetivo que quien corre tiene que declarar
antes, con las tres cuentas de `D67` separadas y la alerta de juntura al lado.
**Qué no entrega:** ninguna recomendación. Un candidato se adopta por decisión del equipo,
con su ADR, y antes tiene que pasar por el inventario de alertas de `M6`, donde `D78` ya le
dio a la juntura una clave propia —`(quimera <nombre>, "juntura")`— que **todavía no está
implementada**.

## 1. La pregunta, y por qué la parte difícil no es enumerar

El issue pide «pasale dos genes y un largo total, y que devuelva la mejor quimera variando
las secuencias y las proporciones, para después comparar contra las regiones sueltas». La
enumeración en sí es aritmética de índices: para dos genes con largo total fijo los
parámetros libres son tres —el arranque y el largo del fragmento izquierdo, con
`l2 = L − l1`, y el arranque del derecho— más el orden, que es discreto con dos valores y
que entra porque está medido que cambia el resultado (`C13`: +3 y −3 con las mismas dos
regiones; `O3`: 41 contra 40, y sólo uno de los dos órdenes fabrica riesgo nuevo) `[M]`.

Las dos partes difíciles son otras. La primera es **qué quiere decir «la mejor»**, que es de
lo que trata este reporte entero y terminó en `D79`. La segunda es **que la grilla sea
finita**: con largo total 600 sobre `BicC_Dm` (2.520 nt) y `V-ATPase B` (1.503 nt) la grilla
tiene **47.833.512** combinaciones con paso 50, y cada una pide plegar una molécula de 600
nt `[M]`. Lo que la vuelve enumerable no es un optimizador: es podar por riesgo primero.

## 2. El objetivo se declara antes, y «la mejor» no existe

`D67` decidió que una quimera no se evalúa por densidad de ventanas eficientes, así que
«mejor» no es una opción disponible: hay que decir mejor para qué. El parámetro `--objetivo`
es **obligatorio y no tiene valor por defecto** —omitirlo es un error de línea de comandos,
no una corrida con el objetivo implícito de nadie—, admite tres valores con nombre y la
cadena viaja en **cada fila** de la salida, no sólo en el encabezado, para que una fila
copiada a otro documento no pueda perder su objetivo por el camino.

| Objetivo | Qué ordena |
| --- | --- |
| `cobertura_fenotipica` | El de `D67`. Exige eje de fenotipo declarado y **distinto** para los dos genes. Ordena por el eje de riesgo —primero las que no fabrican ningún bloque— y usa las heredadas eficientes como **desempate**, no como puntaje |
| `riesgo_minimo` | Sólo lo que fabrica el empalme. No mira eficiencia |
| `eficiencia_heredada` | Sólo ventanas heredadas eficientes. Es el que el issue pide **no vender**, y existe para medir cuánto se pierde al no usarlo |

El eje de fenotipo es **entrada declarada, no inferencia**: el catálogo de `C5` tiene 36
filas y sus columnas son `funcion` y `resultado` en texto libre, sin columna de eje `[M]`,
así que el eje lo declara quien corre y la fila del catálogo queda como su fuente. Los dos de
esta corrida son los que `D67` ya había asignado: `BicC` (`DM-01`, oogénesis) → reproducción,
y `V-ATPase B` (`DM-02`, alas deformes) → movilidad `[R]`. Un gen sin fila entra como
`sin_fenotipo_publicado` y **no puede** correr bajo `cobertura_fenotipica`.

Que esto no es ceremonia está medido: **el primer puesto cambia según el objetivo**, y el de
eficiencia pura asciende un candidato que fabrica un bloque de ≥ 19 nt contra el panel,
mientras que los primeros de `cobertura_fenotipica` no fabrican ninguno `[M]`.

## 3. El riesgo poda primero, y es lo único que vuelve finita la grilla

Es el orden que `D70` fijó y `D74` aplicó. Por gen se calcula una **máscara de veto por
ventana** —vetada si tiene coincidencia perfecta de 21 nt contra el panel de seis, con la
humana a peso 1,00 y el genoma del vector excluido por on-target— y un fragmento es
admisible si **ninguna** de sus ventanas está vetada. La máscara se calcula **una vez por
gen**, porque el estado de off-target de una ventana depende sólo de sus 21 nt (`C13` §6).

El efecto es de cuatro órdenes de magnitud `[M]`:

| | |
| --- | --- |
| combinaciones antes de podar | **47.833.512** |
| admisibles en marco 2 | **3.204** |
| plegados que hacen falta | 3.405 (3.204 moléculas + 201 fragmentos) |

Lo que **no** se hereda es lo que fabrica el empalme, y eso se tamiza por candidato. Acá hay
una distinción que costó una iteración entera y conviene leerla: el tamizado de ventanas de
`offtarget_21nt.py` dice si una ventana tiene un bloque de ≥ 19 nt en una referencia, pero
**no dice cuál bloque ni dónde cae**, así que no puede distinguir un bloque que el empalme
fabrica de uno que la quimera **hereda** de un gen. Con el tamizado de ventanas, los dos
órdenes de la quimera de `O3` levantaban alerta; `D74` dice que el inverso fabrica cero. La
definición correcta es la del paso 2 de `O3`: **fabricado es el bloque que toma al menos un
nucleótido de cada uno de los dos genes**. Son 57 bloques por juntura —20 de 21 nt, 19 de 20
y 18 de 19—, se buscan exactos y en las dos hebras, y el autómata se arma **sólo** con ellos,
de modo que todo acierto es fabricado por construcción. Con eso reproduce `D74`.

## 4. Una grilla gruesa anclada en el origen no ve las islas angostas

Este es el hallazgo de método de la línea, y salió de leer la primera corrida real: **no
había ni una combinación con `l1 = 300`**. El motivo es que las ubicaciones admisibles no
están repartidas a lo largo del gen sino concentradas en islas, y **las islas que el veto
deja son angostas**: la única de 300 nt de `V-ATPase B` arranca en 517 y mide 21 nt de ancho.
La retícula de paso 50 —1, 51, 101, …— no toca ninguna de esas 21 posiciones, así que la
región que el proyecto eligió en `D74` **no aparecía en la grilla** `[M]`.

Una grilla gruesa anclada en el origen no es una muestra uniforme del gen: es una que ignora
justamente las islas más angostas, que son las que el veto deja. La enumeración pasa a
agregar los **dos extremos de cada racha admisible**, lo que cuesta dos posiciones por isla,
conserva el determinismo y no es muestreo. Con eso la grilla pasa de 1.124 a **3.204**
combinaciones y aparecen 256 con `l1 = 300`, 64 de ellas con la región de `D74` `[M]`.

## 5. Las tres cuentas, separadas, y qué dicen

Nunca se suman en una sola cifra (`D67`, y es criterio de terminado del issue). La prueba lo
verifica de dos formas: una lista blanca de columnas, que falla si alguien agrega una cifra
total, y la comprobación de que ninguna columna vale `heredadas + juntura`.

**Heredadas, contra las regiones sueltas.** Es la comparación que el issue pide, y la suma de
las partes viaja en su propia columna justamente para poder hacerla sin sumar nada. De las
3.204 combinaciones, **913 (28,5 %)** superan la suma de sus dos partes, con **mediana −1**
ventana y un rango de **−11 a +10** `[M]`. O sea que la quimera promedio rinde un poco menos
que sus partes por separado, y el mejor caso gana diez ventanas sobre un total de 580. El
«bonus gratis» que `C4` había encontrado no reaparece.

**Juntura.** 4.400 ventanas eficientes sobre 64.080 ventanas de juntura, **6,9 %** `[M]`,
que cae dentro de la banda de 7-15 % que el plan ya declaraba para regiones recortadas y
muy por encima del 1,7 % de las regiones vigentes. Y de esas 64.080, **2.164 (3,4 %)** tienen
blanco continuo de 21 nt en alguno de los dos genes: el resto es capacidad de silenciamiento
que no se va a usar, porque la unión es secuencia que fabrica el ensamblado.

**Riesgo del empalme.** **515 de 3.204 (16,1 %)** fabrican al menos un bloque que coincide
con el panel `[M]`. Por referencia: humano 249, *Homalodisca vitripennis* 145, maíz 113,
*Harmonia axyridis* 32, *Folsomia candida* 7, *Apis mellifera* 5. No es un caso raro: el de
`D74` era el primero que miramos, no el único que hay.

**Pero ese 16,1 % hay que leerlo con el aporte, y baja bastante.** De las 515, en **262 —la
mitad— el bloque más repartido toma un solo nucleótido del segundo gen**, y sólo **118**
tienen algún bloque repartido 5/5 o mejor `[M]`. Un bloque de 19 nt con 18 de un gen y 1 del
otro es casi el gen solo, y **existe por azar en una de cada cuatro** referencias que
contengan al gen padre, porque basta con que el nucleótido siguiente del padre coincida — por
eso el proyecto necesita el aporte y no sólo el conteo, y por eso el caso de `D74`, que era
justamente 18 + 1, se firmó mirando también en qué transcriptos caía. La misma aritmética
explica que 1.362 de las 3.204 junturas tengan un bloque que existe en el **genoma del
vector**: eso no es riesgo, es on-target, y por eso la columna del aporte cuenta sólo los
bloques que coinciden en el panel y el vector viaja en su propia columna.

## 6. La asimetría, que es el agujero del objetivo y no de la grilla

El mejor conteo de heredadas por proporción, con largo total 600 `[M]`:

| `l1` | 100 | 150 | 200 | 250 | 300 | 350 | 400 | 450 | 500 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mejor heredadas | 60 | 56 | 56 | 49 | 49 | 49 | 57 | 56 | **64** |

La curva tiene forma de U: el máximo está en los dos extremos y el mínimo en las
proporciones equilibradas. O sea que `cobertura_fenotipica`, tal como está escrito, **premia
darle casi todo el largo al gen de perfil más denso** —`BicC_Dm`— y dejar el fenotipo de
movilidad en un fragmento testimonial de 100 nt. Eso es lo contrario de para qué `D67` quiere
una quimera, y es un defecto **del objetivo**, no de la enumeración: el objetivo ordena por
riesgo y desempata por eficiencia, y nada en él pide que las dos mitades sirvan para algo.

`[H]` No se arregla cambiando de objetivo sino poniéndole un **mínimo por gen** a las
proporciones, y fijar ese mínimo pide saber cuánto ARNdc de un gen hace falta para
silenciarlo, que es dato de bioensayo: el catálogo de `C5` registra dosis por insecto, no
largo mínimo de disparador. Queda en `PREGUNTAS_ABIERTAS.md` 45 como pregunta para el
investigador.

Vale la pena leer al lado dónde quedó la quimera de `O3`: las 64 combinaciones que usan la
región 517-816 de `V-ATPase B` entran en la grilla, y la mejor de ellas sale **177ª de
3.204** bajo `cobertura_fenotipica` `[M]`. Eso **no** dice que `D74` eligió mal: `D74` eligió
con un largo fijado por simetría con los otros genes del proyecto y sobre la única región que
el veto dejaba en marco 1, mientras que acá el largo y la ubicación son libres. Dice que
cuando se liberan las proporciones aparecen combinaciones con más ventanas heredadas, todas
con el mismo defecto de asimetría del párrafo anterior.

## 7. Las unidades, y el ancla que no cerró

El ancla 3 contra `D74` no cerró, y la causa no fue una medición sino la unidad. Está contado
entero en `D80` y en la entrada 44 de `PREGUNTAS_ABIERTAS.md`; el resumen es que `D63` ya
declara tres marcos de conteo, que el enumerador trabaja en **marco 2** —el largo total son
nucleótidos, porque es lo que se sintetiza— y reporta la lectura de **marco 1** al lado, y
que las cifras de `D74` son de marco 1 aunque su redacción diga «nt». El eje de riesgo
también se lee en marco 2, que es una desviación declarada: en marco 1 una región puede
quedar vetada por un 21-mero que la molécula **no contiene**, y el caso está medido.

Antes de seguir se midió el alcance en las regiones vigentes, que es lo que importaba: los
cuatro genes de EPILAB con insumo en esta máquina reproducen **celda por celda** los dos
marcos que `N3` publicó —38/31, 21/20, 36/29 y 21/17— y **ninguna de las cuatro gana un
acierto perfecto de 21 nt** al leerse en marco 1, así que el inventario de alertas de `M6`
no se mueve `[M]`. `eth_Dm` y `bursA_Dm` quedan sin medir por falta de `work/C11/`.

## 8. Cómo se reproduce

Desde la raíz del repositorio. Los dos primeros comandos son el insumo —el tamizado del panel
de seis sobre los genes **enteros**, que el de `O3` no cubría para `BicC_Dm`— y tardan unos
minutos cada uno.

```bash
# 0. el FASTA de consultas con los dos genes enteros (no se versiona)
python research/ola6/O4_enumerador_quimeras/scripts/00_consultas.py

# 1. el tamizado del panel de seis sobre los dos genes enteros
python tools/sifi21_port/offtarget_21nt.py \
    --consulta work/O4/fasta/consultas_genes_enteros.fasta --mm1 \
    --db work/offtarget_db/*.fna.gz --salida work/O4/offtarget
python tools/sifi21_port/offtarget_21nt.py \
    --consulta work/O4/fasta/consultas_genes_enteros.fasta --mm1 \
    --db work/W5/ref/humano_rna.fna.gz --salida work/O4/offtarget_humano

# 2. las cuatro anclas del preregistro. Si alguna falla, la linea para aca.
python research/ola6/O4_enumerador_quimeras/scripts/00_anclas.py

# 3. las ocho pruebas de la feature; no necesitan datos de work/
python research/ola6/O4_enumerador_quimeras/scripts/test_enumerador.py

# 4. la corrida publicada, una por objetivo declarado
python research/ola6/O4_enumerador_quimeras/scripts/enumerar_quimeras.py \
    --gen BicC_Dm=work/O3/fasta/BicC_Dm_full.fasta \
    --gen VATPaseB_Dm=work/O3/fasta/VATPaseB_Dm_full.fasta \
    --eje BicC_Dm=reproduccion:C5/DM-01 \
    --eje VATPaseB_Dm=movilidad:C5/DM-02 \
    --largo-total 600 --paso 50 --objetivo cobertura_fenotipica \
    --nombre o4_cobertura_fenotipica
```

El paso 0 existe porque el tamizado que dejó `O3` cubre `V-ATPase B` entero pero de
`BicC_Dm` sólo su región de 300 nt, y para enumerar fragmentos a lo largo del gen hace falta
la máscara del gen completo. Su salida **no se versiona** —son las dos secuencias, y
`BicC_Dm` es una de las cuatro de EPILAB—, así que el `.gitignore` del bloque rechaza
`*.fasta` y `*.fna`. Si falta el CDS de `V-ATPase B`, que tampoco se versiona, lo regenera
`research/ola6/O2_vatpase_b/scripts/02_extraer_cds.py`, y `mascara.py` **aborta** si el
tamizado no cubre el gen entero, para que ese faltante no produzca una grilla podada con una
máscara parcial.

Con `--paso 1` la misma grilla pide **136.446** plegados, que exceden el tope declarado de
5.000: la corrida **se detiene y lo dice**, con el tamaño medido y el paso más fino que
entraría, en vez de muestrear o cambiar de algoritmo. Esa corrida fina no se hizo y queda en
`PREGUNTAS_ABIERTAS.md` 46.

## 9. Las cuatro anclas

Corren juntas en `scripts/00_anclas.py`, que devuelve 1 si alguna falla, y las cuatro pasan
`[M]`:

1. **Contra `C13` §5:** las doce quimeras vigentes reproducen la tabla publicada en doce
   columnas, celda por celda, más las tres sumas —240 ventanas de juntura, 4 eficientes, 61
   heredadas que cambiaron—.
2. **Contra `O3` y `D74`:** 41 y 40 ventanas eficientes contra 40 de la suma de las partes,
   el bloque fabricado de 19 nt sólo en el orden `V-ATPase B` + `BicC_Dm`, ninguna de sus
   ventanas eficiente, cero en el orden inverso.
3. **Contra la máscara de veto, en marco 1:** 71 ventanas vetadas, 1.184 regiones que caben,
   una sola admisible, ninguna una unidad más grande.
4. **Motor en proceso contra `run_sifi.py`:** 580 ventanas, cero distintas.

## 10. Límites, declarados

- **El criterio de eficiencia no está validado en hemípteros:** ρ = +0,142, IC95
  [−0,247, +0,492], n = 29 `[M]`. Todo conteo de ventanas eficientes de este bloque hereda
  ese límite, y un resultado in silico es una hipótesis sobre eficacia, no una prueba.
- **La juntura ya tiene clave en el inventario de alertas de `M6`, pero nadie la escribió
  todavía.** `D78` decidió que entra como `(quimera <nombre>, "juntura")`, con granularidad
  quimera × organismo × gen impactado y los `j` fuera de la clave, y la entrada 41 declara
  que **no se implementó** por falta de insumo. O sea que una quimera todavía puede pasar la
  compuerta con su empalme sin tamizar: la salida de esta feature declara la clave que le
  corresponde en vez de dar el hueco por cerrado, y la fila completa con el esquema de `M6`
  la produce `03_alerta_d48.py` de `O3`, que resuelve las anotaciones de cada acierto.
- **Los aciertos con un desapareo del empalme no están localizados.** El tamizado de juntura
  busca coincidencia exacta, porque un desapareo no tiene bloque contiguo que localizar; es
  la misma limitación del paso 2 de `O3`. `mm1_21` queda fuera de la cuenta
  (`PREGUNTAS_ABIERTAS.md` 47).
- **La grilla fina no se corrió** (entrada 46) y **el mínimo por gen no está fijado**
  (entrada 45).
- **Esta línea no recomienda nada.** Produce un orden bajo un objetivo declarado; adoptar un
  candidato es del equipo.
