# C13 — La quimera armada con las regiones que recomendamos: qué cambia cuando las dos partes ya son las mejores

**Ola 3, línea C13.** La pregunta que abre esta línea es del usuario, y tiene dos partes: cómo
se llama bien la técnica de pegar las mejores regiones de dos genes y volver a evaluarlas, y si
se puede hacer todas las combinaciones de a dos con los cuatro genes de EPILAB y meterlas en el
ranking. La segunda parte parecía estar hecha: la línea C4 ya había medido las doce quimeras
ordenadas. **No lo estaba.** C4 concatenó las regiones *tal como las eligió EPILAB*, y desde
entonces el proyecto movió las cuatro regiones a las que propone nuestra cascada (C7 nivel 3) y
una de ellas otra vez por conservación (D25). Una quimera armada con las regiones nuevas es
otra molécula: el empalme es secuencia distinta y hay que recalcular todo.

**Lo que se midió acá, en una línea:** las 12 quimeras ordenadas de las regiones vigentes, con
el port de si-Fi21 sin modificar y en sus dos modos, el tamizaje de off-targets de las 240
ventanas de empalme contra las seis referencias locales, los dos ejes del ranking de W7
calculados con su propio motor, y el control de recorte que C4 había dejado planteado como
hipótesis.

**El veredicto corto, en tres frases.** Con las regiones nuevas la quimera **ya no suma**: el
empalme aporta 4 ventanas eficientes de 240, contra 48 en las mismas doce uniones de C4, y el
total queda entre −4 y +3 respecto de la suma de las partes `[M]`. Ninguna de las doce supera a
su mejor parte en ninguno de los dos ejes del ranking, y una queda por debajo de las dos, así
que **meterlas en la misma lista que las regiones sueltas no cambia el orden: lo ensucia** `[M]`.
Y el empalme no es neutro en riesgo: uno de los doce fabrica un bloque de 19 nt que no existe
en ninguno de los dos genes y **sí existe en tres transcriptos de maíz**, y dos adquieren un
veto que ninguna de sus partes tenía `[M]`.

---

## 1. Cómo se llama la técnica

La palabra que usó el investigador, según nuestra transcripción del Checkpoint 1, es
**quimera** (`research/checkpoints/checkpoint1.md`, apartado «Quimeras: combinar regiones de
genes distintos»), y la receta que describió es exactamente la que el usuario recuerda: se
extraen los 200 nucleótidos de mayor densidad de un gen, los 200 del otro, se pegan y se vuelve
a evaluar la secuencia de 400 `[R]`.

En la literatura el mismo objeto aparece con tres nombres, y conviene conocer los tres porque
las búsquedas no se cruzan entre sí `[R]`:

| Nombre | Dónde | Qué es |
| --- | --- | --- |
| **ARNdc quimérico** (*chimeric dsRNA*), también **multiblanco** (*multi-target*) | el título de `dsRNAmax`, la herramienta de diseño de Fletcher 2025 (`S07` de C4) | el término más usado y el que conviene para buscar |
| **recombinación artificial de fragmentos de ARNdc** (*artificial recombination*) | Luo *et al.* 2026 en *Apolygus lucorum* (`S11` de C4), la molécula `Udw` de 262 pb con fragmentos de tres genes | el mismo objeto, nombrado por la operación |
| **ARNdc de fusión** (*fusion dsRNA*) | Kong *et al.* 2025 en *Bemisia tabaci* (`S21` de C4), tres fragmentos de 100 pb | el mismo objeto, nombrado por la construcción |

**No hay ninguna técnica de ARNi que se llame «mecha».** Buscamos el término y no existe en este
campo; lo más probable es que sea la memoria de «quimera». Si el mentor usó otra palabra, el
candidato es alguno de los tres de la tabla. Hay una cuarta palabra que sí circula en el
proyecto y puede ser la que se mezcló: **empalme**, que es como nuestros documentos llaman al
punto de unión entre los dos fragmentos. Las tres fuentes de la tabla las abrió y leyó la línea
C4; **en C13 no se reabrieron**, y por eso la afirmación terminológica va con `[R]` y no con
`[E]`. Queda una cita pendiente sin abrir, registrada en `00_meta/PREGUNTAS_ABIERTAS.md`.

---

## 2. Qué estaba hecho y qué no

C4 contestó la pregunta que había hecho el investigador —si la eficiencia total es la suma de
las partes salvo en la unión— y la contestó bien: no lo es, porque además del empalme hay un
reajuste en una banda a cada lado. Para eso usó las cuatro regiones de EPILAB. Las regiones del
proyecto ya no son ésas:

| Gen | Región de EPILAB (la que usó C4) | Región vigente | La movió |
| --- | --- | --- | --- |
| `MP_MRFV` | 1-200 | **72-271** | C7 nivel 3 |
| `CP_MRFV` | 201-400 | **99-298** | C7 nivel 3 |
| `BicC_Dm` | 264-563 | **922-1221** | C7, y después D25 por conservación (C8) |
| `ATPaseD_Dm` | 151-450 | **72-371** | C7 nivel 3 |

Ninguna de las cuatro coincide con la de EPILAB, y en `MP_MRFV` y `BicC_Dm` la región se mudó
cientos de nucleótidos. Como el empalme son los últimos 20 nt de una región pegados a los
primeros 20 de la otra, **las doce uniones de C13 no comparten una sola base con las doce de
C4** `[M]`.

---

## 3. Cómo se midió, y la trampa del modo

Tres corridas, todas con `tools/sifi21_port/run_sifi.py` llamado por línea de comandos y sin
modificarlo:

```bash
# verificación: reproducir C4 con las regiones de EPILAB, en los dos modos
python research/ola3/C13_quimeras_region_recomendada/scripts/quimeras_v2.py --conjunto epilab --modo fiel
python research/ola3/C13_quimeras_region_recomendada/scripts/quimeras_v2.py --conjunto epilab --modo corregido
# lo nuevo
python research/ola3/C13_quimeras_region_recomendada/scripts/quimeras_v2.py --conjunto vigentes --modo corregido
python research/ola3/C13_quimeras_region_recomendada/scripts/recorte_vs_contexto.py --conjunto vigentes --modo corregido
python research/ola3/C13_quimeras_region_recomendada/scripts/offtarget_ranking.py --conjunto vigentes --modo corregido
python research/ola3/C13_quimeras_region_recomendada/scripts/empalme_maiz_detalle.py
```

**La verificación primero.** El script de C13 reproduce la tabla de C4 **fila por fila, 12
filas por 17 columnas, en los dos modos** `[M]`, corriendo en Python 3.13.15 contra el 3.11.17
de C4. Eso es lo que autoriza a leer los números nuevos: la contabilidad es la misma y lo único
que cambió son las regiones de entrada.

**La trampa, y es importante para cualquiera que siga esta línea.** El port tiene dos modos.
Las quimeras de C4 se midieron en modo **`fiel`**, el que reproduce al programa original y está
verificado contra él. El ranking de W7 y de C7 se construyó con los perfiles
`<gen>_full_corregido_vienna.tsv`, es decir en modo **`corregido`** (`tools/sifi21_port/ranking.py`
línea 118). Los dos modos no dan el mismo conteo: en modo `fiel` el gen `MP_MRFV` tiene **142**
ventanas eficientes y en `corregido` tiene **123** `[M]`. Por eso esta línea reporta las dos
cosas: el modo `fiel` cuando compara contra C4, y el modo `corregido` cuando compara contra el
ranking. Mezclarlos produce diferencias que parecen hallazgos y son el modo.

Versiones: ViennaRNA 2.7.2, backend `vienna`, Python 3.13.15, numpy 2.5.4. El backend `exe`
sigue sin poder usarse (necesita el RNAplfold que instala si-Fi21 en Windows, que no está en
esta máquina), igual que en C4.

---

## 4. El control que faltaba: la región recortada no vale lo que valía dentro del gen

C4 dejó esto escrito como hipótesis y sin medir: «si la región se recorta del gen y se
sintetiza sola, sus ventanas de los primeros y últimos ~60 nt tampoco valen lo que valían
dentro del gen entero». Hay que medirlo antes de mirar una quimera, porque si no se comparan
cifras que no son comparables. Las cifras que el entregable publica para las regiones
recomendadas se contaron **sobre el perfil del gen completo**; la molécula que se sintetizaría
es el recorte.

Modo `corregido`. Las dos anclas pasan: el conteo del gen completo da los cuatro números que
`ranking_v2.py` fija como ancla de W7 (123, 30, 171, 29) y el conteo en contexto de cada región
da los cuatro publicados (38, 21, 36 y 21, el de `BicC_Dm` por D25) `[M]`.

| Gen | Región | Ventanas en contexto | Eficientes en contexto | Ventanas recortada | Eficientes recortada | Δ | de las que: se pierden | pasan a eficientes | dejan de serlo |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `MP_MRFV` | 72-271 | 200 | 38 | 180 | **27** | **−11** | 7 | 1 | 5 |
| `CP_MRFV` | 99-298 | 200 | 21 | 180 | **23** | +2 | 1 | 6 | 3 |
| `BicC_Dm` | 922-1221 | 300 | 36 | 280 | **26** | **−10** | 7 | 0 | 3 |
| `ATPaseD_Dm` | 72-371 | 300 | 21 | 280 | **20** | −1 | 4 | 4 | 1 |

La contabilidad cierra exacto en las cuatro: Δ = −(las que se pierden) + (las que ganan) −
(las que pierden). `resultados/recorte_vs_contexto_vigentes_corregido_vienna.tsv`.

Dos lecturas. **La primera es de método y hay que decirla sin rodeos:** la cifra que mejor
resume a nuestros dos primeros candidatos —38 ventanas eficientes en `MP_MRFV`, 36 en
`BicC_Dm`— **baja a 27 y a 26 en la molécula que se sintetizaría** `[M]`. Un cuarto del número.
No cambia qué región se recomienda —el orden de los cuatro se mantiene— pero sí cambia la
cifra, y es la cifra que está en el entregable. De la diferencia, una parte es aritmética
—dentro del gen la región tiene 200 posiciones de inicio porque las ventanas del final se
completan con el nucleótido de al lado, y recortada tiene 180— y la otra es el borde: 27
ventanas cambiaron de veredicto en las cuatro regiones.

**La segunda corrige a C4 en su parte mecánica.** C4 observó que el cambio de veredicto llega
hasta 54 nt de la unión y lo atribuyó a que si-Fi21 calcula la accesibilidad con una ventana de
plegado de 80 nt, de donde deducía un techo de 59 nt. Acá aparecieron flips a **64 y 66 nt** del
borde, que ese techo prohibiría. No es un error de medición: son dos ventanas cuyos 21
nucleótidos son idénticos en los dos cálculos y a las que sólo les cambió el valor de
accesibilidad (0,1158 a 0,0890 y 0,1143 a 0,0960, cruzando el umbral). La explicación está en
el código, y el techo correcto es **asimétrico** `[M]` el número, `[H]` la derivación:

> El original no mide la accesibilidad de los 21 nt de la ventana: mide la del tramo de **8 nt
> que termina en el último nucleótido** de la ventana (`sifi_core.py`, `accessibility_window = 8`,
> y la lectura `up[pos + size - 1][u]`). Una ventana de plegado de 80 nt que contenga ese
> tramo de 8 puede empezar hasta en `p+13`, y por lo tanto llegar hasta `p+92`. De ahí: la
> secuencia ajena influye hasta **72 nt corriente abajo** del final de la ventana, pero sólo
> hasta **59 nt corriente arriba** de su comienzo.

La predicción se puede probar contra las tablas que ya existen, y se cumple: en las cuatro
tablas de flips disponibles —las dos de C4 y las dos de C13— **hay 204 ventanas cambiadas y
ninguna viola el techo asimétrico**; el máximo corriente abajo llega a 67 nt y el máximo
corriente arriba se queda en 50 `[M]`.

| Tabla | n | máx. con la secuencia ajena corriente abajo (techo 72) | máx. corriente arriba (techo 59) | violaciones |
| --- | ---: | ---: | ---: | ---: |
| C4, EPILAB, `fiel` | 46 | 54 | 50 | 0 |
| C4, EPILAB, `corregido` | 36 | 54 | 50 | 0 |
| C13, vigentes, `fiel` | 55 | 67 | 39 | 0 |
| C13, vigentes, `corregido` | 67 | 66 | 32 | 0 |

---

## 5. Las doce quimeras con las regiones vigentes

Modo `corregido`, el del ranking. «Suma de partes» es la suma de eficientes de las dos regiones
**recortadas**; «empalme» son siempre las 20 ventanas a caballo de la unión.

| Quimera | Largo | Suma de partes | Total | Δ | Eficientes del empalme | Heredadas cambiadas |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ATPaseD_Dm` + `MP_MRFV` | 500 | 47 | 50 | **+3** | 0 | 9 |
| `MP_MRFV` + `CP_MRFV` | 400 | 50 | 52 | +2 | 0 | 8 |
| `MP_MRFV` + `BicC_Dm` | 500 | 53 | 55 | +2 | 0 | 4 |
| `ATPaseD_Dm` + `BicC_Dm` | 600 | 46 | 48 | +2 | 1 | 7 |
| `CP_MRFV` + `BicC_Dm` | 500 | 49 | 50 | +1 | 1 | 12 |
| `BicC_Dm` + `CP_MRFV` | 500 | 49 | 50 | +1 | 1 | 4 |
| `ATPaseD_Dm` + `CP_MRFV` | 500 | 43 | 44 | +1 | 1 | 4 |
| `BicC_Dm` + `MP_MRFV` | 500 | 53 | 53 | 0 | 0 | 0 |
| `CP_MRFV` + `ATPaseD_Dm` | 500 | 43 | 42 | −1 | 0 | 3 |
| `BicC_Dm` + `ATPaseD_Dm` | 600 | 46 | 45 | −1 | 0 | 1 |
| `MP_MRFV` + `ATPaseD_Dm` | 500 | 47 | 44 | −3 | 0 | 3 |
| `CP_MRFV` + `MP_MRFV` | 400 | 50 | 46 | **−4** | 0 | 6 |

**El hallazgo principal de esta línea está en la columna del empalme.** Cuando las partes eran
las regiones de EPILAB, las 240 ventanas de empalme aportaban 48 eficientes en modo `corregido`
(58 en `fiel`). Con las regiones vigentes aportan **4** (5 en `fiel`) `[M]`:

| Conjunto de regiones | Modo | Eficientes de las 240 ventanas de empalme | Δ sobre la suma de partes |
| --- | --- | ---: | --- |
| EPILAB (C4) | `fiel` | 58 | −4 a **+19** |
| EPILAB (C4) | `corregido` | 48 | −4 a **+17** |
| vigentes (C13) | `fiel` | 5 | −4 a +4 |
| vigentes (C13) | `corregido` | **4** | −4 a +3 |

Lo que esto dice es que **el «bonus gratis» de la quimera que C4 encontró era una propiedad de
las regiones de EPILAB, no de las quimeras.** Las regiones de EPILAB son regiones mediocres
dentro de su gen —C7 midió que `BicC_Dm` estaba en el percentil 44 de su propio gen— y pegarlas
creaba veinte ventanas nuevas que fácilmente superaban ese nivel. Una vez que cada parte es la
mejor región de su gen, el empalme es secuencia que nadie eligió y rinde por debajo incluso del
promedio del gen: 4 de 240 es el 1,7 %, contra el 7 a 15 % de las regiones recortadas `[M]`. La
atribución causal es nuestra y es `[H]`; además el número de uniones independientes es 12 y no
240, porque las 20 ventanas de una unión comparten secuencia y contexto de plegado, así que la
comparación es descriptiva y no una prueba estadística.

Y el reajuste de las heredadas sigue ahí, más fuerte que antes: con las regiones vigentes
**todo el Δ viene de la banda de contexto y nada del empalme** en diez de las doce. El atajo
«sumo los dos conteos y le agrego las del medio» erraría por hasta 4 ventanas y con el signo
equivocado.

El orden sigue importando, y eso no cambió: `ATPaseD_Dm` + `MP_MRFV` da +3 y `MP_MRFV` +
`ATPaseD_Dm` da −3, con las mismas dos regiones `[M]`.

---

## 6. Off-targets del empalme: lo que la unión fabrica

Las 240 ventanas de empalme se tamizaron con `tools/sifi21_port/offtarget_21nt.py` contra las
seis referencias locales. Un detalle de método que vale la pena: **no hace falta tamizar las
5.760 ventanas de las doce quimeras, sino 1.160.** El estado de off-target de una ventana
depende sólo de su secuencia, y toda ventana heredada es base por base una ventana de su región
de origen; lo único nuevo son los 40 nt que cruzan cada unión. El resultado es idéntico a
tamizar la molécula entera y cuesta una pasada en vez de siete.

**En maíz, el empalme fabrica un acierto que no existe en ninguno de los dos genes.** En
`MP_MRFV` + `ATPaseD_Dm`, tres ventanas de empalme tienen un bloque perfecto de 19 nt en el
transcriptoma de *Zea mays*. Las tres comparten el mismo bloque, así que es **un** acierto
detectado por tres ventanas solapadas, y la auditoría lo identifica exactamente
(`scripts/empalme_maiz_detalle.py`) `[M]`:

> bloque `GGCAAGGTGATGAAGGAGG`, 19 nt = **4 nt de `MP_MRFV` + 15 nt de `ATPaseD_Dm`**, presente
> en `XR_004852610.1`, `XR_004856333.1` y `XR_562605.3`.

Ninguna de las dos regiones por separado tiene ese bloque: `MP_MRFV` sola tiene 3 aciertos ≥19
nt en maíz y `ATPaseD_Dm` sola tiene **cero**, y ninguno es éste. Es exactamente el riesgo que
el investigador anticipó cuando dijo que los off-targets se corren sobre la quimera completa y
no sobre los fragmentos, y en C4 no se había materializado: ahí **ninguna** de las 240 ventanas
de empalme tocaba una base no objetivo. Con las regiones nuevas, sí. Los tres transcriptos
llevan prefijo `XR_`, que en RefSeq es ARN no codificante, la clase a la que el criterio de
ranking propuesto le asigna peso 0,6 y no 1,0.

El mecanismo es predecible y da una regla de diseño: los primeros ~18 nt de la región que va a
la derecha quedan pegados al empalme, y si les faltan pocas bases para completar un 19-mero que
existe en el cultivo, **el socio de la izquierda se las puede dar**. Acá `ATPaseD_Dm` aporta 15
de los 19 nt y `MP_MRFV` los 4 que faltan. Con `CP_MRFV` a la izquierda, las cuatro bases son
otras y el acierto no aparece. `[H]`

**Contra el genoma del vector, cuatro empalmes crean una coincidencia perfecta de 21/21** (2 en
`CP_MRFV` + `ATPaseD_Dm`, 1 en `BicC_Dm` + `MP_MRFV`, y bloques de ≥19 nt en diez de los doce).
Para una quimera de dos genes del insecto eso es on-target y no es riesgo. Para una que mezcla
un gen viral con uno del insecto, el veto depende de una decisión nuestra, y es el tema de la
sección siguiente.

En las cuatro referencias no objetivo restantes —*Apis mellifera*, *Harmonia axyridis*,
*Homalodisca vitripennis* y *Folsomia candida*— los doce empalmes de las regiones vigentes no
produjeron **ningún** acierto, ni perfecto ni con un desajuste `[M]`. (Con el conjunto anterior,
el de C7 con `BicC_Dm` en 2121-2420, había aparecido un acierto con un desajuste en *F.
candida*, en el empalme de `BicC_Dm` + `ATPaseD_Dm`; ese conjunto también está medido y sus
tablas están en `resultados/`.) Falta el panel humano, que el ranking v2 agregó como
séptima referencia y que no está en esta máquina: **los empalmes no están tamizados contra
humano**, y queda registrado como pendiente.

---

## 7. ¿Se pueden poner en el ranking?

Se pueden calcular con el mismo motor —`ranking.ejes`, importado sin tocarlo— y el resultado es
que **no conviene ponerlas en la misma lista**, por tres razones medidas y una estructural.

Modo `corregido`, regla conservadora. Para las mixtas se reporta el trato `mixto` del genoma del
vector, que se explica abajo.

| Objeto | Ventanas | Eficientes | Eficacia | Limpieza | Limpias y eficientes | ¿Vetada? |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `MP_MRFV` (región sola) | 180 | 27 | **0,1500** | 0,9820 | 26 | no |
| `CP_MRFV` (región sola) | 180 | 23 | 0,1278 | 0,9917 | 23 | no |
| `BicC_Dm` (región sola) | 280 | 26 | 0,0929 | 0,9884 | 22 | no |
| `ATPaseD_Dm` (región sola) | 280 | 20 | 0,0714 | 0,9919 | 18 | no |
| `MP_MRFV` + `CP_MRFV` | 380 | 52 | 0,1368 | 0,9875 | 51 | no |
| `CP_MRFV` + `MP_MRFV` | 380 | 46 | 0,1211 | 0,9875 | 45 | no |
| `MP_MRFV` + `BicC_Dm` | 480 | 55 | 0,1146 | 0,9850 | 50 | no |
| `BicC_Dm` + `MP_MRFV` | 480 | 53 | 0,1104 | 0,9838 | 48 | **sí** |
| `ATPaseD_Dm` + `MP_MRFV` | 480 | 50 | 0,1042 | 0,9870 | 46 | no |
| `CP_MRFV` + `BicC_Dm` | 480 | 50 | 0,1042 | 0,9886 | 45 | no |
| `BicC_Dm` + `CP_MRFV` | 480 | 50 | 0,1042 | 0,9886 | 45 | no |
| `MP_MRFV` + `ATPaseD_Dm` | 480 | 44 | 0,0917 | 0,9832 | 41 | no |
| `ATPaseD_Dm` + `CP_MRFV` | 480 | 44 | 0,0917 | 0,9906 | 42 | no |
| `CP_MRFV` + `ATPaseD_Dm` | 480 | 42 | 0,0875 | 0,9881 | 40 | **sí** |
| `ATPaseD_Dm` + `BicC_Dm` | 580 | 48 | 0,0828 | 0,9905 | 42 | no |
| `BicC_Dm` + `ATPaseD_Dm` | 580 | 45 | 0,0776 | 0,9905 | 39 | no |

**Primera razón: en los ejes que son tasas, la quimera queda entre sus dos partes y nunca por
encima de la mejor.** La eficacia de una quimera es el promedio ponderado de las dos mitades
más un empalme que aporta casi cero, así que no puede ganarle a su mejor parte: el máximo de
las doce es 0,1368 y `MP_MRFV` sola tiene 0,1500 `[M]`. Lo que sí puede es quedar **por debajo
de las dos**, y pasa una vez: `CP_MRFV` + `MP_MRFV` da 0,1211 contra 0,1278 y 0,1500 de sus
partes, porque la banda de contexto le apagó cuatro ventanas.

**Segunda razón: en el eje que es conteo, gana cualquiera, y eso no es un hallazgo sino el
largo.** «Limpias y eficientes» sube de 26 a 51 porque la molécula pasa de 180 a 380 ventanas.
Es la misma objeción que C7 ya le había hecho a la cascada —que cuenta ventanas y no tasas, y
por eso favorece a las regiones de 300 sobre las de 200— y con quimeras de 400 a 600 nt se
vuelve dominante. Comparar una quimera con una región suelta en ese eje es comparar dos largos.

**Tercera razón, y es un defecto del eje que vale para todo el ranking: la limpieza es una tasa
y se diluye.** En el trato que reportamos ninguna quimera supera a sus dos partes en limpieza, y
dos quedan por debajo de las dos —`CP_MRFV` + `ATPaseD_Dm` con 0,9881 y `ATPaseD_Dm` +
`CP_MRFV` con 0,9906, contra 0,9917 y 0,9919 de sus partes— por los aciertos que fabrica el
empalme. Pero basta cambiar el trato del vector para ver el defecto: con el trato `insecto`,
donde esos aciertos no cuentan, **cuatro quimeras quedan por encima de sus dos partes** (por
ejemplo `BicC_Dm` + `MP_MRFV`, 0,9891 contra 0,9884 y 0,9820), porque veinte ventanas limpias
de empalme bajan el promedio de exposición `[M]`. La consecuencia general es incómoda y hay que
decirla: **al eje de limpieza se le puede mejorar el número agregando secuencia limpia**, sea un
empalme o un relleno. Es un argumento más para reportar el riesgo también en crudo, como ya
propuso `criterio_ranking_propuesto.md` en su Regla 1. `[H]`

**La razón estructural: una quimera mixta no pertenece a ninguna de las dos listas.** El
entregable presenta dos listas separadas por mecanismo (D38, aplicando D34): la del insecto,
donde el genoma de *Dalbulus maidis* es on-target y sale del cómputo de riesgo, y la del virus
dentro de la planta, donde entra (D5, D20). De las doce quimeras, **dos son virales, dos son del
insecto y ocho mezclan**, y para esas ocho la regla de `ranking.excluidas_de` no alcanza. Lo
resolvimos por ventana, que es lo único que respeta las dos decisiones a la vez: los aciertos
contra el vector cuentan en las ventanas heredadas de la mitad viral y no cuentan en las de la
mitad del insecto. Las 20 del empalme no pertenecen a ningún gen y se cuentan, que es la lectura
conservadora. El efecto de esa elección es grande y conviene verlo:

| Trato del genoma del vector en una quimera mixta | Limpieza de `BicC_Dm` + `MP_MRFV` | Ventanas con 21/21 | ¿Vetada? |
| --- | ---: | ---: | --- |
| como si fuera viral (cuenta en toda la molécula) | 0,6609 | 262 | sí |
| como si fuera del insecto (no cuenta en ninguna parte) | 0,9891 | 0 | no |
| **mixto, por ventana (nuestra propuesta)** | 0,9838 | **1** | **sí** |

Con el trato `mixto`, **2 de las 8 quimeras mixtas quedan vetadas, y el veto viene enteramente
del empalme**: `BicC_Dm` + `MP_MRFV` por una ventana de empalme con 21/21 contra el genoma del
vector y `CP_MRFV` + `ATPaseD_Dm` por dos `[M]`. Ninguna de las cuatro regiones sueltas está
vetada. Es decir: **pegar dos regiones limpias puede producir una molécula vetada**, y el veto
no aparece si uno mira los fragmentos por separado.

Hay que ser honestos con el alcance de ese resultado: el veto de esas dos depende de nuestra
decisión de contar el empalme como viral. Si se contara como del insecto, las dos quedarían sin
veto. Es un parámetro declarado, no un dato.

---

## 8. Qué implica para el diseño

Cinco reglas candidatas, todas `[H]` salvo donde se apoyan en un número de arriba.

**No se gana eficiencia pegando dos regiones buenas.** Medido: el empalme aporta 4 ventanas
eficientes de 240 y el total queda entre −4 y +3 de la suma. La razón para hacer una quimera
tiene que ser otra —cubrir dos blancos con una sola molécula, una sola síntesis y una sola
aplicación— y esa razón el ranking no la mide. Los dos antecedentes hemípteros publicados
coinciden con esto: en *Apolygus lucorum* la quimera de tres genes mató **menos** que el mejor
gen solo (72,2 % contra 94,4 %) pero empezó antes, y en *Bemisia tabaci* el beneficio reportado
también fue silenciamiento más temprano, no más mortalidad (`S11` y `S21` de C4, `[R]` acá
porque no se reabrieron).

**Correr el tamizaje sobre la molécula completa no es una formalidad.** Medido: un empalme
fabricó un bloque de 19 nt presente en tres transcriptos de maíz que no existe en ninguno de los
dos genes, y cuatro empalmes fabricaron coincidencias perfectas de 21 nt con el genoma del
vector. El investigador tenía razón y ahora hay un número detrás.

**Elegir el socio y el orden mirando los extremos.** Los últimos 18 nt de la región izquierda y
los primeros 18 de la derecha son los únicos que participan del empalme. Un tamizaje previo de
esos dos tramos cortos contra el cultivo —buscando bloques de 15 a 18 nt, que son los que quedan
«a pocas bases» de completar un 19-mero— predice el riesgo antes de armar la molécula y cuesta
una pasada.

**Reportar la eficiencia de la región recortada, no la del gen.** Medido: la cifra de
`MP_MRFV` baja de 38 a 27 y la de `BicC_Dm` de 36 a 26. Si el número va a representar a la
molécula que se sintetiza, hay que calcularlo sobre la molécula.

**Si se comparan quimeras, compararlas a igual largo total.** Una quimera de 400 nt contra dos
regiones de 200 administradas juntas es la comparación que el laboratorio necesita y que, según
lo que C4 buscó en la literatura, nadie publicó. A igual largo, el eje de conteo deja de ser
una medida del largo.

---

## 9. Qué no se hizo

**Las ternas y la cuádruple.** El usuario preguntó por «todos con todos» de a dos, que es lo que
está hecho (12 ordenadas). Con cuatro genes hay además 24 ternas ordenadas y 24 cuádruples, de
900 a 1.000 nt. No se corrieron por dos motivos: el largo queda muy por encima de los 262 y 300
pb de los dos antecedentes hemípteros publicados, y con el empalme aportando 4 de 240 no hay
razón para esperar que sumar uniones mejore algo. El script las soporta cambiando una línea
(`itertools.permutations(REGIONES, 2)`).

**Los dos genes nuevos.** `eth_Dm` y `burs-alpha_Dm` no entraron: la pregunta era por los cuatro
genes de EPILAB, y sus secuencias no están en `work/` en esta máquina.

**El panel humano.** El tamizaje corrió contra las seis referencias locales. El ranking v2 usa
siete, con *Homo sapiens*. Por eso las columnas de limpieza de esta línea no son idénticas a las
de C7 ni deben compararse con ellas: dentro de C13 todo está medido con el mismo panel, y la
comparación válida es la de cada quimera contra sus dos regiones recortadas, que están en la
misma tabla.

**El barrido de pesos.** No se sortearon pesos sobre las quimeras. No haría falta para la
conclusión: que una quimera no supere a su mejor parte en ninguno de los dos ejes es una
propiedad de las tasas, y ningún peso no negativo da vuelta una dominancia.
