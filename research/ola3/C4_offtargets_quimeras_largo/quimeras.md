# Q3 — Qué se recalcula en una quimera y cuánto cambia el número

El investigador describió la quimera así: se elige la mejor región de un gen, se repite con
otro gen y se pegan los dos fragmentos en una sola molécula que se vuelve a evaluar; y marcó
el punto fino, que la eficiencia total *«en general siempre era la suma entre uno y otro,
salvo en la unión»*, porque las ventanas de 21 que caen a caballo del empalme son secuencia
nueva y hay que recalcular, y que después hay que correr off-targets sobre la quimera
completa y no sobre los fragmentos por separado (`research/checkpoints/checkpoint1.md`,
apartado «Quimeras»). `[R]`

Lo medimos con las cuatro regiones de EPILAB, con las herramientas del repositorio y sin
tocarlas. El veredicto corto: **la observación se cumple en lo esencial y falla en un detalle
que importa para el diseño.** El empalme es, en efecto, el único lugar donde aparece secuencia
nueva, pero el cambio de eficiencia no se queda en el empalme: se extiende a una banda de
hasta 54 nucleótidos a cada lado, y esa banda tiene una explicación mecánica exacta en los
parámetros con los que si-Fi21 calcula accesibilidad.

---

## 1. Cómo se midió

Doce quimeras ordenadas —las 4 × 3 combinaciones de a dos, en los dos órdenes, porque el
empalme de A+B no es el mismo que el de B+A— construidas concatenando las regiones elegidas
tal como están en `work/W5/fasta/`: 200 nt cada región viral y 300 nt cada región del insecto,
así que las quimeras miden 400, 500 o 600 nt.

```bash
python research/ola3/C4_offtargets_quimeras_largo/scripts/quimeras_sifi.py --modo fiel      --backend vienna
python research/ola3/C4_offtargets_quimeras_largo/scripts/quimeras_sifi.py --modo corregido --backend vienna
python research/ola3/C4_offtargets_quimeras_largo/scripts/quimeras_offtarget.py
python research/ola3/C4_offtargets_quimeras_largo/scripts/q3_empalme_contexto.py
```

El script arma los FASTA y llama por línea de comandos a `tools/sifi21_port/run_sifi.py`, sin
modificarlo (md5 de los módulos del port en `NOTAS_PARA_META.md`). Versiones: port de si-Fi21
en modo **fiel** —el que reproduce el programa original, verificado contra él en los cuatro
genes— con backend **vienna**, ViennaRNA 2.7.2, Python 3.11.17. El modo `corregido` se corrió
como control de sensibilidad. **No se usó el backend `exe`**: necesita el RNAplfold 2.1.5 que
instala si-Fi21 en Windows, que no está en esta máquina; los dos backends no dan lo mismo
porque cambiaron los parámetros de energía, así que todos los números de abajo son del
backend `vienna`. `[E]`

Un punto de método que conviene explicitar: la eficiencia de cada región suelta se calcula
**sobre la región recortada**, no sobre el gen entero. Es la opción 1 de las dos que el
investigador propuso —recortar la región y subirla como archivo nuevo— y es la comparación
correcta para esta pregunta, porque la molécula que se sintetizaría es el recorte. Por eso
estos conteos de eficientes (20, 16, 22 y 19) no son los de W5, que corrió los genes
completos.

---

## 2. La tabla de los empalmes

Modo fiel. «Suma de partes» es la suma de eficientes de las dos regiones sueltas; «empalme»
son siempre las 20 ventanas que quedan a caballo de la unión; «cambiadas» son las ventanas
heredadas que cambiaron de veredicto respecto de la región de origen.

| Quimera | Largo | Suma de partes | Total de la quimera | Δ | Eficientes del empalme | Heredadas cambiadas |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `MP_MRFV` + `ATPaseD_Dm` | 500 | 39 | 58 | **+19** | 15 | 6 |
| `CP_MRFV` + `ATPaseD_Dm` | 500 | 35 | 45 | +10 | 10 | 0 |
| `BicC_Dm` + `MP_MRFV` | 500 | 42 | 51 | +9 | 6 | 5 |
| `MP_MRFV` + `CP_MRFV` | 400 | 36 | 44 | +8 | 5 | 5 |
| `BicC_Dm` + `CP_MRFV` | 500 | 38 | 46 | +8 | 6 | 2 |
| `BicC_Dm` + `ATPaseD_Dm` | 600 | 41 | 48 | +7 | 8 | 1 |
| `CP_MRFV` + `MP_MRFV` | 400 | 36 | 39 | +3 | 3 | 2 |
| `ATPaseD_Dm` + `MP_MRFV` | 500 | 39 | 42 | +3 | 2 | 3 |
| `ATPaseD_Dm` + `CP_MRFV` | 500 | 35 | 37 | +2 | 1 | 5 |
| `MP_MRFV` + `BicC_Dm` | 500 | 42 | 43 | +1 | 1 | 10 |
| `CP_MRFV` + `BicC_Dm` | 500 | 38 | 36 | **−2** | 1 | 3 |
| `ATPaseD_Dm` + `BicC_Dm` | 600 | 41 | 37 | **−4** | 0 | 4 |

Tabla cruda, con el desglose por lado, en `resultados/quimeras_eficiencia_fiel_vienna.tsv`;
la versión en modo `corregido` está al lado y da el mismo patrón con conteos más bajos
(Δ de −4 a +17).

Tres cosas que se leen directo. **Primera: el orden importa.** `MP_MRFV` + `ATPaseD_Dm` suma
+19 y `ATPaseD_Dm` + `MP_MRFV` suma +3, con la misma secuencia de partida y las mismas 200 +
300 bases; la diferencia es qué queda pegado con qué en los 20 lugares del empalme. Una
quimera no es una bolsa de fragmentos: es una secuencia, y el orden es un parámetro de diseño
gratis que hoy nadie está eligiendo. `[E]`

**Segunda: el empalme puede restar.** En dos de las doce el total queda por debajo de la suma
de las partes. Y la razón no es que el empalme tenga ventanas malas —eso sólo puede sumar cero
o más—, sino que **ventanas heredadas perdieron su condición de eficientes**.

**Tercera: la contabilidad cierra exactamente.** En las doce quimeras, Δ es igual a los
eficientes del empalme más el saldo neto de las heredadas que cambiaron: por ejemplo, `CP_MRFV`
+ `BicC_Dm` tiene Δ = −2 con 1 eficiente de empalme y 3 heredadas cambiadas, de las cuales el
neto es −3. No hay ningún otro término. `[E]`

---

## 3. Por qué cambia una ventana que no toca el empalme

Las 46 ventanas heredadas que cambiaron de veredicto (modo fiel, en las doce quimeras) se
distribuyen así respecto de su distancia a la unión:

| Distancia a la unión | Ventanas cambiadas |
| --- | ---: |
| 0–19 nt | 19 |
| 20–39 nt | 10 |
| 40–59 nt | 17 |
| ≥ 60 nt | **0** |

Mínimo 0, máximo **54 nt**, mediana 30. Y el cambio va en los dos sentidos: 26 pasaron de no
eficientes a eficientes y 20 al revés. `resultados/quimeras_ventanas_cambiadas_fiel_vienna.tsv`.

Ese techo de 54 no es casualidad. De los tres filtros de si-Fi21, dos son locales a la ventana
—selección de hebra y estabilidad de extremos dependen sólo de los 21 nt— y el tercero,
**accesibilidad del sitio blanco, se calcula con RNAplfold con ventana de plegado de 80 nt**
(`-W 80 -L 40 -u 21`), que es lo que el original tiene fijado y el port reproduce
(`tools/sifi21_port/README.md`). Una ventana de 21 nt comparte ventana de plegado con la
secuencia del otro gen mientras su distancia a la unión más sus 21 nt no supere los 80, es
decir hasta 59 nt de distancia. Observamos 54. **El alcance del efecto de contexto está
acotado por un parámetro de la herramienta, no por la biología.** `[E]` el número, `[H]` la
atribución causal, que es una inferencia nuestra sobre el parámetro y no un experimento.

Esto es lo que hay que corregirle, con todo respeto, a la frase del checkpoint: la eficiencia
total **no** es la suma salvo en la unión. Es la suma, más lo que aporte la unión, más un
reajuste de signo variable en una banda de unos 60 nt a cada lado. En nuestras doce quimeras
ese reajuste fue de hasta 10 ventanas en una sola molécula —el 23 % de las eficientes de esa
quimera—, así que no es un decimal. `[E]`

Y tiene una consecuencia práctica que va más allá de las quimeras: **si la región se recorta
del gen y se sintetiza sola, sus ventanas de los primeros y últimos ~60 nt tampoco valen lo
que valían dentro del gen entero.** La evaluación de una región elegida sobre el perfil del gen
completo hereda el mismo sesgo de borde. Es la misma aritmética, aplicada al recorte en lugar
del pegado. `[H]`

---

## 4. Off-targets del empalme

Las 240 ventanas de empalme (12 quimeras × 20) se tamizaron con
`tools/sifi21_port/offtarget_21nt.py` contra las seis referencias de W5: genoma de *Dalbulus
maidis*, y transcriptomas de *Zea mays*, *Homalodisca vitripennis*, *Apis mellifera*,
*Harmonia axyridis* y *Folsomia candida*.

| Base de datos | Aciertos de ventanas heredadas | Aciertos de ventanas de empalme |
| --- | ---: | ---: |
| *Zea mays* (transcriptoma) | 3 a 6 según quimera | **0** |
| *Homalodisca vitripennis* | 7 a 30 según quimera | **0** |
| *Apis mellifera* | 0 | **0** |
| *Harmonia axyridis* | 0 | **0** |
| *Folsomia candida* | 0 | **0** |
| *Dalbulus maidis* (genoma; **on-target** para los genes del vector) | 220 a 442 | **24** |

Es decir: **la secuencia nueva del empalme no aportó ni un solo off-target en ninguna base no
objetivo** (criterios de bloque perfecto ≥ 19 nt y 21/21). `[E]`
`resultados/q3_offtarget_empalmes.tsv`.

Los 24 aciertos contra el genoma del blanco merecen el detalle, porque muestran que «ventana
de empalme» y «secuencia nueva» no son lo mismo bajo un criterio de 19 nt. Las posiciones son
siempre las mismas: 281 y 282 en las quimeras con región izquierda de 300 nt, 199 y 200 en las
de 200 nt. Son **las dos primeras ventanas de la banda**, las que todavía conservan 20 y 19
nucleótidos puros del gen de la izquierda, así que uno de sus bloques de 19 nt sigue existiendo
en el gen de origen. Con el criterio estricto de 21/21, esas ventanas dejan de contar: de los
24 aciertos, sólo 3 son de 21/21, y los tres están en una sola quimera.

Esos tres merecieron su propia verificación, porque un 21/21 en una ventana de empalme sólo
puede existir si el pegado reconstruye, base por base, el vecindario genómico. Lo medimos
leyendo el flanco real en el ensamblado (`scripts/q3_empalme_contexto.py`): la región de
`BicC_Dm` aparece una sola vez en el genoma, en `OZ319706.1:38458360`, y la base que la
precede es **A**, que es exactamente la última base de la región de `ATPaseD_Dm`, la que queda
pegada; y del otro lado, la región de `ATPaseD_Dm` aparece una sola vez en `OZ319711.1`, en
hebra menos, y las dos bases que la siguen en orientación de transcrito son **TA**, que son las
dos primeras de `BicC_Dm` («TAG»). Eso explica, y predice, exactamente los tres aciertos
observados: uno en la posición 300 (una base de coincidencia del lado derecho) y dos en las
281 y 282 (dos bases del lado izquierdo). `[E]`

Es una coincidencia de azar —una base acierta una de cada cuatro veces— pero la moraleja es
general y vale para el diseño: **la quimera puede, sin que nadie lo pretenda, fabricar un
21-mero que existe en el genoma**, y por eso correr el tamizaje sobre la molécula completa y
no sobre los fragmentos, como indicó el investigador, es necesario y no una formalidad. En
este caso el acierto es contra el propio blanco y por lo tanto no es un riesgo; si el vecino
genómico reconstruido hubiera sido el de un gen de maíz, sí lo sería. `[H]`

---

## 5. Qué dice la literatura abierta sobre ARNdc quimérico en insectos

| Fuente | Sistema | Construcción | Resultado |
| --- | --- | --- | --- |
| `S11` Luo et al. 2026 | *Apolygus lucorum* (Hemiptera: Miridae), ninfas de tercer estadio, microinyección de 41,4 nL a 5 µg/µL, 30 ninfas × 3 réplicas | **Udw, 262 pb**: concatenación de *Ubx*-ss-1 (75 pb) + *Dpp*-ss-2 (65 pb) + *wupA*-ss-12 (122 pb, a su vez dos fragmentos unidos) | 7 días de mortalidad acumulada: 64,4 % a 0,5 µg/µL hasta 72,2 % a 5 µg/µL. **Menos que el mejor gen solo** (*wupA* 310 pb, 94,4 %), pero con **inicio más rápido** —significativamente mayor que todos los grupos de un solo gen en los días 2 y 3—. Los autores verificaron con BLAST que la secuencia recombinante no introducía off-targets adicionales. `[E]` |
| `S21` Kong et al. 2025 | *Bemisia tabaci* MEAM1 (Hemiptera), ninfas de cuarto estadio, nanoacarreador SPc, tres réplicas | **GKP, 300 pb**: tres fragmentos de 100 pb de *BtNAG1*, *BtNAGK* y *BtUAP* concatenados en ese orden | ~80 % de mortalidad de ninfas y 70 % de inhibición de la emergencia de adultos, con inicio del silenciamiento más temprano que los ARNdc individuales. `[E]` |
| `S07` Fletcher 2025 | herramienta, validada en nematodos | **dsRNAmax**: ensambla ARNdc quiméricos por k-meros de 21 nt para cubrir varias secuencias blanco a la vez, descartando todo k-mero con coincidencia contigua en las bases no objetivo; largo por defecto del constructo, 300 nt | El ARNdc diseñado inhibió varias especies de nematodo agalladores y no una especie no objetivo. Es la prueba de concepto de que la quimera se puede diseñar *para* especificidad, no sólo *a pesar de* ella. `[E]` |
| `S15` Mlotshwa et al. 2020 (corpus) | maíz, vector viral MRFV | insertos de 120, 231 y 210 nt en distintas uniones génicas del genoma viral | Sólo la unión helicasa/polimerasa toleró insertos; en otras posiciones el mismo inserto fue letal para la infectividad. No es una quimera de ARNdc, pero es el mismo principio: **dónde se pega determina si funciona**. `[E]` |

Lo que no encontramos: ningún trabajo que compare una quimera contra la **suma** de sus partes
administradas por separado —que es la comparación que haría falta para saber si concatenar
cuesta algo— ni ningún límite publicado de largo total para quimeras en insectos. Los dos casos
hemípteros que sí existen usan 262 y 300 pb, dentro del rango que el laboratorio ya usa para
una región sola, y ambos reportan el mismo beneficio: no más mortalidad final, sino
**silenciamiento más temprano**. Es un vacío documentado. `[?]`

---

## 6. Lo que esto implica para el diseño

Tres reglas candidatas, todas `[H]`:

**Recalcular la quimera entera, no sólo el empalme.** El empalme es donde aparece secuencia
nueva, pero el cambio de veredicto llega hasta ~60 nt de la unión, así que el atajo «sumo los
dos conteos y le agrego las 20 del medio» puede errar por hasta 10 ventanas en una molécula de
500 nt.

**Elegir el orden.** Con las mismas dos regiones, el orden cambió el total de eficientes entre
+3 y +19 sobre la suma de partes. Probar los dos órdenes cuesta dos corridas de un segundo.

**Correr off-targets sobre la molécula completa**, como indicó el investigador, y además
hacerlo con el criterio estricto explicitado, porque bajo el criterio de 19 nt las dos primeras
ventanas del empalme son aciertos heredados y no secuencia nueva: se contarían dos veces si uno
sumara los fragmentos por separado.
