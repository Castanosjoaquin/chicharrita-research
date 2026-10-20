# si-Fi21, dsRNA-Engineer y BLAST sobre los cuatro genes, en un eje común

Fecha: 2026-10-20. El punto 2 de lo que el investigador pidió en el checkpoint era
un benchmarking de las tres herramientas sobre los cuatro genes que nos dio. Hasta
hoy si-Fi21 había corrido sobre los cuatro, el tamizaje exacto de 21 nt también, y
**dsRNA-Engineer solamente sobre `PZ371507.1`**, una secuencia pública que no es
ninguno de los cuatro. Este documento cierra lo que se puede cerrar y declara lo que
no.

El eje comparable es el de **off-targets**, porque es el único que las tres tocan:
si-Fi21 mide eficiencia y no mide especificidad, BLAST mide similitud y no mide
eficiencia, y dsRNA-Engineer dice medir las dos. Los datos de la corrida están en
`dsrnaengineer_corrida.json`.

---

## 1. La compuerta de confidencialidad: qué se subió, qué no, y por qué

Las secuencias de EPILAB no se suben a servicios de terceros. dsRNA-Engineer corre
**sólo** como servicio web, con procesamiento del lado del servidor, sin política de
retención declarada y sin cuenta. El procedimiento que se siguió, en este orden:

**Paso 1 — reverificación byte a byte en esta corrida.** No alcanza con que lo diga
otro documento nuestro. Se recalculó contra la copia local de `NC_002786.2`
(6.366 nt, SHA-256 `6770e446cbf0a9ab1c72acb45c8fb01c5f3f703be4a47f517350f07543b4d5c9`):

| Gen | Largo | ¿Subcadena exacta de `NC_002786.2`? |
|---|---:|---|
| `MP_MRFV` | 1.263 | **sí**, posiciones 332-1594, hebra + |
| `CP_MRFV` | 528 | **sí**, posiciones 5674-6201, hebra + |
| `BicC_Dm` | 2.520 | **no** |
| `ATPaseD_Dm` | 491 | **no** |

`[E]` Las dos virales son material ya publicado en el NCBI: subirlas no revela nada
que no esté ahí. Las dos del insecto no lo son.

**Paso 2 — confirmación explícita de la persona.** Se pidió antes de subir nada,
mostrando qué secuencia iba y a dónde. Se autorizó para `MP_MRFV` y `CP_MRFV`
únicamente.

**Paso 3 — lo que efectivamente salió de la máquina.** Se subieron `MP_MRFV` y
`CP_MRFV` a `https://dsrna-engineer.cn`, proyectos `ff5138f6b1e5a91c` y
`c816ff87893b36a4`. **`BicC_Dm` y `ATPaseD_Dm` no se subieron y no se van a subir.**
El benchmark de los dos genes del insecto se hace con dos herramientas, no con tres,
y el hueco está en la sección 4.

---

## 2. Una sorpresa que mejora el cotejo: el panel es el mismo

Antes de comparar hay que saber si las dos herramientas miran las mismas secuencias,
porque si no, cualquier diferencia podría ser de base de datos y no de método. Se
consultó la lista de especies del servicio y el resultado es mejor de lo esperable:

| Referencia | En nuestro tamizaje local | En dsRNA-Engineer | ¿Mismo ensamblado? |
|---|---|---|---|
| *Zea mays* | `GCF_902167145.1` | `GCF_902167145.1` | **sí** |
| *Apis mellifera* | `GCF_003254395.2` | `GCF_003254395.2` | **sí** |
| *Folsomia candida* | `GCF_002217175.1` | `GCF_002217175.1` | **sí** |
| *Harmonia axyridis* | `GCF_914767665.1` | `GCF_914767665.1` | **sí** |
| *Homalodisca vitripennis* | `GCF_021130785.1` | `GCF_021130785.1` | **sí** |
| *Dalbulus maidis* | `GCA_975739785.1` (genoma) | `SRR15166998` (Trinity de novo) | **no** |

`[E]` **Las cinco referencias no objetivo son exactamente los mismos ensamblados**,
así que las diferencias de resultado son atribuibles al método y no al dato. Es la
condición que vuelve interpretable todo lo que sigue. La única que difiere es la del
vector, donde ellos usan un ensamblado propio desde una corrida del SRA y nosotros el
genoma de referencia; ahí los números no son comparables y se marcan como tales.

Y un hallazgo que condiciona la estrategia viral: **el *Maize rayado fino virus* no
está en el panel de dsRNA-Engineer.** Hay tres virus de maíz —*Maize chlorotic mottle
virus* `NC_003627.1`, *Maize dwarf mosaic virus* `NC_003377.1` y *Maize rough dwarf
virus* `NC_077726.1`— y MRFV no está entre ellos. Para los dos candidatos virales,
entonces, **la herramienta no puede calcular on-target**: no tiene contra qué. Se
corrió poniendo a *D. maidis* en la lista de on-target, que es lo que la interfaz
exige, y su conteo se lee como lo que es —aciertos sobre el vector— y no como
on-target. `[E]`

---

## 3. Las dos herramientas sobre los mismos genes y los mismos ensamblados

Conteos para los dos genes virales. La columna de dsRNA-Engineer es lo que el
servicio informa: una **suma sin ponderar** de sus tres condiciones (21 pb perfecto,
16 pb perfecto, 26 pb con hasta 2 desajustes) y contando **líneas de Bowtie**, no
ventanas distintas. Las tres columnas de la derecha son nuestro tamizaje exacto,
contando **ventanas** con al menos un acierto.

### `MP_MRFV` (1.263 nt)

| Referencia | dsRNA-Engineer | exacto k=16 | exacto k=21 | exacto bloque ≥19 |
|---|---:|---:|---:|---:|
| *Zea mays* | 215 | 97 | **0** | 3 |
| *Folsomia candida* | 63 | 35 | **0** | 7 |
| *Apis mellifera* | 56 | 21 | **0** | 0 |
| *Homalodisca vitripennis* | 50 | 25 | **0** | 3 |
| *Harmonia axyridis* | 9 | 6 | **0** | 0 |
| *D. maidis* (otro ensamblado) | 68 | 129 | 0 | 9 |

### `CP_MRFV` (528 nt)

| Referencia | dsRNA-Engineer | exacto k=16 | exacto k=21 | exacto bloque ≥19 |
|---|---:|---:|---:|---:|
| *Zea mays* | 87 | 48 | **0** | 0 |
| *Apis mellifera* | 49 | 11 | **0** | 0 |
| *Folsomia candida* | 31 | 13 | **0** | 0 |
| *Homalodisca vitripennis* | 29 | 11 | **0** | 0 |
| *Harmonia axyridis* | 9 | 5 | **0** | 0 |
| *D. maidis* (otro ensamblado) | 20 | 37 | 0 | 0 |

`[E]` **Lo que dice la tabla, y es el resultado del benchmark:** dsRNA-Engineer
informa 87 off-targets en maíz para `CP_MRFV`, un gen en el que nuestro tamizaje no
encuentra **ni una sola** coincidencia de 19 nt o más contra ninguna de las seis
referencias. Para `MP_MRFV` informa 215 contra 3. La diferencia es de dos órdenes de
magnitud y no es un desacuerdo: es que **no están contando lo mismo**.

**De dónde salen esos números, verificado.** Si el conteo estuviera dominado por la
condición de 21 pb —la que la propia herramienta considera el tamaño de corte de
Dicer-2— nuestro conteo a k = 21 debería ser del mismo orden, y es **cero en las
doce celdas**. Si estuviera dominado por la condición de 16 pb, nuestro conteo a
k = 16 debería serlo, y lo es: 97 contra 215, 48 contra 87, 21 contra 56, y así, con
una razón entre 1,5 y 4,5 que es exactamente lo que se espera cuando uno cuenta
líneas (una por parálogo alcanzado) y el otro cuenta ventanas.

**O sea: el 100 % del riesgo de off-target que dsRNA-Engineer le muestra al usuario
para estos dos genes viene de la condición de 16 pb, y el 0 % de la de 21-22 pb.**
`[E]` Esto **replica sobre dos genes nuevos y cinco referencias** lo que W2 ya había
medido sobre `PZ371507.1`, donde los 70 de 70 aciertos en maíz y los 67 de 67 en
abeja venían de la condición de 16 pb. Era una medición sobre un gen; ahora son
tres.

### BLAST sobre los cuatro genes

BLAST no se volvió a correr: las mediciones que hacen falta ya están y son las que
el prompt pedía poner en un solo lugar. Dos, y las dos son sobre las regiones
elegidas de los cuatro genes.

La primera, de acuerdo: el tamizaje exacto y la corrida de BLAST+ local de W5
**coinciden exactamente en las 20 celdas** para los criterios de bloque perfecto
(≥19 nt y 21/21). Dos implementaciones independientes —coincidencia exacta contra
heurística de semillas— dan el mismo número, lo que valida las dos. `[E]`

La segunda, de desacuerdo, y es la que importa para quien vaya a usar BLAST:

| Gen | 1 desajuste, BLAST+ local | 1 desajuste, exacto | Razón |
|---|---:|---:|---:|
| `BicC_Dm` | 5 | 16 | 3,2 |
| `ATPaseD_Dm` | 9 | 17 | 1,9 |

`[E]` **El criterio de un desajuste medido con BLAST es una subestimación, por hasta
un factor de tres.** La causa es identificable y no es un defecto de BLAST sino de
usarlo para esto: `blastn-short` con `word_size 11` no puede sembrar un 21-mero cuyo
único desajuste cae en la posición 11, porque deja dos bloques de 10 y ninguno
alcanza la semilla. Quien pondere el riesgo con el número de BLAST está ponderando
un número bajo por construcción.

Y la trampa mayor, ya cuantificada en W2 §2.4 y que conviene repetir acá porque es
el error que un equipo nuevo comete: **`-perc_identity` no filtra sobre la consulta
completa sino sobre el alineamiento que BLAST encontró.** Pidiendo 590 ventanas de
26 nt con `-perc_identity 92`, BLAST devolvió 827 filas y **cero** eran alineamientos
de 26 nt; los largos eran 11, 12, 13, 14, 15 y 16 nt. Contar líneas de salida de
BLAST como «cantidad de off-targets» sobreestima el riesgo por un factor de
cientos. `[E]`

---

## 4. El hueco, que es un resultado

**Los dos genes del insecto no tienen corrida de dsRNA-Engineer y no la van a
tener.** `BicC_Dm` y `ATPaseD_Dm` son material no publicado de EPILAB, la
herramienta procesa del lado del servidor, no hay política de retención ni cuenta, y
un dato subido no se puede desubir.

Dicho con todas las letras, porque va a la presentación: **la herramienta que el
organizador señala como la de diseño y verificación de off-targets es exactamente la
que no se puede usar con el material que el mismo organizador entregó.** No es un
tecnicismo nuestro; es el principal condicionante operativo de toda la ola 2.

Lo que sí se pudo hacer, y es la respuesta práctica: **su criterio está completamente
especificado y es reproducible local.** Tamaño mayor por especie, 16 pb perfecto,
26 pb con hasta 2 desajustes, Bowtie. Nuestro `offtarget_21nt.py` cubre los criterios
de bloque perfecto y el de un desajuste sobre los cuatro genes sin que nada salga de
la máquina, y con `--size` cubre cualquier k. La pieza que falta para igualar su
criterio exacto es la condición de 26 pb con hasta 2 desajustes, que no está
implementada. `[H]` Conviene presentarlo como lo que es —un puente, no un aporte
metodológico—.

### Una limitación nueva del servicio, observada hoy

En esta corrida, `project/download-file` devolvió el texto `Error!` (6 bytes) para
los dos proyectos, con GET y agregando el `uid`. En octubre, el mismo endpoint
entregó un `.tar.gz` de 5.323 bytes con los archivos `.bwt` crudos. **Sin esos
archivos no se puede desagregar el conteo por condición desde el lado de la
herramienta**, que es por lo que la atribución de la sección 3 se hizo desde el
nuestro. Queda como `[?]`: no sabemos si es una falla transitoria, un cambio de la
API o algo ligado a estos proyectos en particular.

Un segundo dato operativo: los fragmentos que la herramienta recomendó para
`MP_MRFV` tienen entre **51 y 91 pb**, igual que en la corrida de octubre sobre
`PZ371507.1`. El investigador dijo que el laboratorio trabaja con regiones de
**150 a 250 nt** y las regiones de la planilla son de 200 y 300. **Los largos que
dsRNA-Engineer recomienda no se superponen con el régimen que EPILAB sintetiza**, de
modo que su módulo de recomendación de fragmentos no es utilizable tal cual aunque
el de off-targets lo fuera. `[E]`

---

## 5. La conclusión operativa: cuál usaríamos para qué

**Para eficiencia, si-Fi21, y no hay alternativa.** Es la única de las tres que
estima si un fragmento va a silenciar. dsRNA-Engineer no calcula termodinámica ni
tiene modelo entrenado, y BLAST menos. Con dos advertencias que son nuestras y están
medidas: el conteo depende de si la región se plega sola o dentro del gen —hasta
47 % de diferencia— y entre el 14 % y el 24 % de lo que el original marca como
eficiente lo es por una regla terminal que se saltea la física, que es el motivo de
que usemos el modo corregido.

**Para off-targets, el tamizaje exacto local, y no dsRNA-Engineer.** Tres razones,
en orden: no se le puede dar el material del corpus; su número está dominado por una
condición de 16 pb que esta misma corrida muestra que es ruido —ver
[`azar_por_k.md`](azar_por_k.md), donde a 16 nt lo observado está *por debajo* de lo
que predice el azar—; y suma sin ponderar tres condiciones y cuenta líneas en vez de
ventanas, de modo que el número que muestra mezcla «cuántas ventanas son riesgosas»
con «a cuántos parálogos llegan», que son decisiones distintas.

**Para BLAST, exploración y nada más.** Sirve para ver a qué se parece una secuencia
y para encontrar regiones conservadas entre organismos. Para tamizaje de ventanas de
21 nt hay que postfiltrar por `length` y `mismatch`, o fijar `-word_size` igual al
largo de la ventana con `-ungapped`; sin eso, el resultado no significa lo que
parece. Su pregunta es otra.

**Lo que dsRNA-Engineer sí tiene y nosotros no, y conviene decirlo:** un panel de
1.103 especies con 127 hemípteros, 27 polinizadores, 94 plantas de cultivo y 97
artrópodos no blanco. Nuestro panel tiene seis referencias. Si el laboratorio
quisiera un tamizaje amplio sobre material ya publicado, esa es la herramienta; para
material propio, no puede serlo.
