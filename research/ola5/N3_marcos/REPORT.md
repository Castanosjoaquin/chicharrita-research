# N3 — Los tres marcos de conteo, y de dónde sale cada diferencia

**Ola 5, línea N3.** Fecha: 2026-10-25. Contesta el punto 3 de la carta del investigador del 25 de
octubre de 2026 —que confirma el marco de la molécula y propone explorar un tercero— y el punto 5,
que pide distinguir qué parte de las diferencias viene del modelo de eficiencia, cuál de los
límites físicos de la molécula y cuál del contexto de accesibilidad. Reproducible con
`scripts/tres_marcos.py`. Marcadores de `CLAUDE.md`.

## El resultado, en un párrafo

**El tercer marco que propone ya lo teníamos medido para `BicC_Dm` 922-1221: es 29.** La región
tiene 36 ventanas eficientes contando los 300 arranques que caen dentro de ella en el gen, 29
contando sólo los 280 que existen físicamente en la molécula pero con la accesibilidad evaluada en
el gen —que es el marco que él propone— y 26 contando la molécula de 300 nt plegada sola `[M]`.
Con eso la diferencia se parte en dos causas que no se parecen: **siete ventanas son límite físico
de la molécula** —arranques que el gen tiene y la molécula no— y **tres son contexto de
accesibilidad** —ventanas que existen en los dos lados y cambian de veredicto porque el plegado
cambia—. Del **modelo de eficiencia no sale ninguna**: es el mismo criterio, los mismos umbrales y
la misma tabla en los tres marcos; lo que cambia es qué se le da de comer. Extendido a las seis
regiones, aparece algo que la medición de `M7` había visto en tres y que conviene decir con las
seis: **el recorte no baja los conteos, los mueve en direcciones distintas** —baja en tres
regiones y sube en las otras tres— así que un ranking armado en contexto no es el ranking de las
moléculas que se sintetizarían `[M]`.

## 1. Los tres marcos, con nombre

| Marco | Arranques | Accesibilidad calculada sobre | Qué pregunta contesta |
|---|---|---|---|
| 1 · contexto, todos | los `L` que caen dentro de la región | el gen completo | ninguna sola: mezcla ventanas que la molécula no tiene |
| 2 · contexto, comparables | los `L − 20` que existen en la molécula | el gen completo | ¿qué tan accesible es el sitio en el ARN blanco **en su contexto**? |
| 3 · molécula recortada | los `L − 20` | la molécula sola | ¿qué siRNAs puede producir el ARNdc aplicado? |

La distinción es la que hace el investigador y es biológica, no contable: una cosa es qué siRNAs se
producen a partir del ARNdc —y ahí manda la molécula final— y otra es cuán accesible resulta el
sitio de unión en el ARN endógeno del blanco, donde lo representativo es el transcrito en su
contexto `[R]`. En el modelo heredado de si-Fi21 las dos preguntas no están separadas, porque
RNAplfold trabaja sobre la secuencia que se le pasa. El marco 2 es el que las separa.

`[M]` En un fragmento de 300 nt hay 280 ventanas completas de 21 nt y no 300, como dice su carta.
El marco 1 no está mal por eso: cuenta arranques que en el gen **sí** tienen 21 nt por delante. Lo
que está mal es publicarlo como si fuera el conteo de la molécula, y eso ya lo corrigió `M7`.

## 2. Las seis regiones en los tres marcos

`[M]` Punto por defecto, modo `corregido` —el del ranking—, ViennaRNA 2.7.2, tabla `RNA_NN3`,
22 °C. Las cuatro primeras son las regiones vigentes; las dos últimas, las rivales de `BicC_Dm` que
compara el eje 1 de `M7`. Fuente: `resultados/tres_marcos.tsv`.

| Región | Largo | M1 contexto | M2 comparables | M3 molécula | Límite físico | Contexto, neto | Pierden | Ganan |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `MP_MRFV` 72-271 | 200 | 38 | 31 | 27 | 7 | 4 | 5 | 1 |
| `CP_MRFV` 99-298 | 200 | 21 | 20 | **23** | 1 | −3 | 3 | 6 |
| `BicC_Dm` 922-1221 | 300 | 36 | 29 | **26** | 7 | 3 | 3 | 0 |
| `ATPaseD_Dm` 72-371 | 300 | 21 | 17 | **20** | 4 | −3 | 1 | 4 |
| `BicC_Dm` 2121-2420 | 300 | 35 | 27 | 22 | 8 | 5 | 6 | 1 |
| `BicC_Dm` 264-563 | 300 | 20 | 15 | **17** | 5 | −2 | 2 | 4 |

El script **aborta** si no reproduce las anclas publicadas, y las reprodujo todas: los cuatro
conteos del marco 1 de las regiones vigentes (38, 21, 36 y 21, `M7` §1) y las tres ternas de
`BicC_Dm` (36/29/26, 35/27/22 y 20/15/17, `M7` §3) `[M]`. Las cifras del marco 3 coinciden además
con las «sumas de partes» de las doce quimeras de `C13` §5, que se calcularon por otro camino:
27 + 23 = 50, 20 + 27 = 47, 27 + 26 = 53 `[M]`.

## 3. Qué se lee de la tabla

`[M]` **El límite físico es de 1 a 8 ventanas y no se puede discutir.** Son los últimos veinte
arranques de la región, que en el gen siguen teniendo 21 nt por delante y en la molécula se quedan
sin ellos. Cuántos de esos veinte eran eficientes es lo único que cambia entre regiones: siete en
922-1221, ocho en 2121-2420, uno en `CP_MRFV`.

`[M]` **El contexto de accesibilidad cambia de signo entre regiones.** En `MP_MRFV`, `BicC_Dm`
922-1221 y 2121-2420 el recorte **quita** ventanas (4, 3 y 5 netas); en `CP_MRFV`, `ATPaseD_Dm` y
`BicC_Dm` 264-563 el recorte **agrega** (3, 3 y 2 netas). Y el bruto es mayor que el neto en las
seis: hay 20 ventanas que pierden y 16 que ganan en total, así que el efecto no es un corrimiento
sino una redistribución. `[H]` La lectura es que plegar la molécula sola no es ni más estricto ni
más laxo: es distinto, y cuánto depende de qué estructura tenía la región dentro del gen.

`[M]` **La región recomendada es la única de las seis que no gana ni una ventana al recortarse.**
922-1221 pierde tres y gana cero. `[H]` Eso la hace la más conservadora de las seis en el marco que
se publica, y conviene decirlo porque es el único sentido en el que su ventaja no depende del
marco.

`[M]` **El orden entre las dos rivales de `BicC_Dm` no cambia en los tres marcos** —36 > 35,
29 > 27 y 26 > 22— pero el margen pasa de una ventana a cuatro. Lo que sí cambia con el marco es
la fracción de la grilla de 4.368 configuraciones en la que ese orden se sostiene: 36,4 % en
contexto y 75,6 % en el recorte (`M7` §2) `[M]`. Un margen de una ventana en el punto por defecto
nunca fue una diferencia.

## 4. Qué cifra se publica

`[M]` **26**, el marco 3, para `BicC_Dm` 922-1221. Es la decisión de `M7` §3 y la carta la
confirma: para evaluar qué ventanas puede generar un diseño se considera la secuencia de la
molécula de ARNdc que efectivamente se va a producir `[R]`. Las otras dos cifras no se tiran: el
marco 1 es el que hay que usar para comparar contra cualquier número histórico que se haya contado
en contexto, y el marco 2 es el que contesta la pregunta de accesibilidad en el blanco.

`[H]` La regla operativa que sale de acá, y que vale para todo lo que publiquemos: **cada conteo
viaja con su marco**, igual que viaja con su configuración. Un conteo sin marco declarado no se
puede comparar con otro, y las seis filas de arriba son la prueba.

## 5. Qué término cruza el corte

**Agregado el 2026-10-25**, con `scripts/terminos_por_region.py`. Para las tres regiones de
`BicC_Dm` esto ya estaba medido en `M7`: quince de las dieciséis ventanas que cambian cruzan por
accesibilidad y una por estabilidad de extremos en la posición 1 `[M]`. Faltaban las tres regiones
vigentes de los otros genes, y se corrieron con el mismo comparador de `M2` —el que pidió el
investigador en su carta del 22 de octubre— manejado igual que lo maneja `M7`, con `offset_b` en
el inicio de la región. El script reproduce las tres anclas de la sección 2 y aborta si no.

| Región | Modo | Contexto | Recorte | Cambian | Pierden | Ganan | En las dos primeras posiciones |
|---|---|---:|---:|---:|---:|---:|---:|
| `MP_MRFV` 72-271 | corregido | 31 | 27 | 6 | 5 | 1 | **0** |
| `CP_MRFV` 99-298 | corregido | 20 | 23 | 9 | 3 | 6 | **0** |
| `ATPaseD_Dm` 72-371 | corregido | 17 | 20 | 5 | 1 | 4 | **0** |
| `MP_MRFV` 72-271 | fiel | 33 | 29 | 6 | 5 | 1 | **0** |
| `CP_MRFV` 99-298 | fiel | 24 | 27 | 11 | 4 | 7 | **0** |
| `ATPaseD_Dm` 72-371 | fiel | 22 | 23 | 7 | 3 | 4 | **0** |

`[M]` **Las veinte ventanas que cambian en el modo del ranking cruzan por accesibilidad, las
veinte.** Ninguna cruza por selección de hebra y ninguna por estabilidad de extremos. Y **ninguna
de las veinte cae en las dos primeras posiciones del recorte**, que es donde vive el artefacto de
dG que encontró `M2` —el original calcula ahí los extremos sin nucleótidos colgantes porque el
siRNA de dos posiciones antes no existe—. Así que en estas tres regiones ese artefacto no explica
nada: **el cambio de marco es borde de plegado y nada más**.

`[M]` En el modo `fiel` cambian veinticuatro, y hay cuatro que cruzan accesibilidad **sin** que se
mueva el veredicto termodinámico: las cuatro son de **rama terminal 2**, el atajo que saltea el
veredicto termodinámico y decide mirando sólo la accesibilidad. Son ventanas cuya estabilidad de
extremos ya no pasaba de los dos lados, de modo que el término termodinámico era falso en ambos y
el veredicto igual se dio vuelta. `[H]` Es la misma asimetría que midió `M3` —en `BicC_Dm`, 134 de
las 223 eficientes del modo fiel entran por esa rama— apareciendo ahora en el cambio de marco: el
atajo hace que el conteo del modo fiel sea **más** sensible al plegado que el del modo corregido,
no menos.

## 6. El marco intermedio en las 4.368 configuraciones

**Agregado el 2026-10-25**, con `scripts/marco2_en_la_grilla.py`. Era el hueco que esta línea dejó
declarado: `M7` había cruzado la grilla con los marcos 1 y 3, y el intermedio estaba medido sólo en
el punto por defecto. Como el investigador propone explorar ese marco, la pregunta es si la
comparación aguanta ahí.

`[M]` El script importa `primitivos` y `eficientes` de `M7/scripts/grilla_parametros.py` —las
mismas rutinas verificadas contra `apply_rules` del port— y **reproduce las cuatro fracciones
publicadas por M7**, que es su ancla, además de los nueve conteos del punto por defecto.

| Marco | vs 2121-2420 | empates | margen mediano | vs 264-563 | margen mediano |
|---|---:|---:|---:|---:|---:|
| 1 · contexto, todos | 36,4 % | 291 | −1,5 | 99,1 % | +10,0 |
| **2 · comparables** | **41,1 %** | **640** | **0,0** | **99,9 %** | **+10,0** |
| 3 · molécula | 75,6 % | 315 | +3,0 | 99,6 % | +12,0 |

`[M]` **El marco intermedio no rescata la comparación contra C7: la deja en una moneda al aire.**
41,1 % de las 4.368 configuraciones, con 640 empates —el número más alto de los tres marcos— y un
**margen mediano de exactamente cero**. Queda entre los otros dos, como era de esperar, y más cerca
del de contexto que del de la molécula.

`[M]` **Y es el marco donde la ventaja sobre la región del laboratorio es más fuerte de las tres:**
99,9 %, con sólo 2 empates en 4.368 configuraciones.

`[H]` La conclusión práctica para la reunión: **cualquiera de los tres marcos que se adopte, «no
264-563» se sostiene entre el 99,1 % y el 99,9 %; «922-1221 antes que 2121-2420» no se sostiene en
dos de los tres.** Eso vuelve la elección del marco irrelevante para la afirmación que defendemos y
decisiva para la que no.

## 7. El marco intermedio en el eje de referencia

**Agregado el 2026-10-25**, con `scripts/marco2_por_fuente.py`. Era el último hueco de cómputo de
la ola. `M7` §4 recalculó la eficiencia **sobre la molécula recortada tal como la escribe cada
fuente** —el marco 3— contra cuatro fuentes; faltaba el marco intermedio, que necesita reconstruir
el **gen entero** por fuente y no sólo la región.

### Tres de las cuatro fuentes no se pueden correr en esta máquina

`[M]` Y conviene escribir el motivo, no el resultado faltante. `eje_referencia.py` de `M7` alinea
con `blastn` local contra `work/W5/db/`. En esta máquina **no hay `blastn` ni `makeblastdb`**
—verificado con `shutil.which`— y `work/W5/` no está en el árbol.

| Fuente | Estado | Motivo |
|---|---|---|
| GHCC01 (Pergamino) | **no corrida** | la base no está en disco |
| GCWP01 (Illinois) | **no corrida** | la base no está en disco; y no cubre un solo nucleótido de 922-1221 |
| genoma del Reino Unido | **no corrida** | está en `work/offtarget_db/`, pero son 984 MB y sin alineador de consultas largas no se ubica el gen ni sus exones |
| **GITV01 (Ohio State)** | **corrida** | los dos contigs que la ola 3 identificó como blanco principal están en `work/M1/bases/` |

`[H]` La que quedó es la más informativa de las cuatro para esta pregunta: es la única donde los
conteos recalculados **bajan** y la única donde 2121-2420 conserva una fracción mayor de sus
eficientes que 922-1221 (33 de 35 contra 32 de 36). Si el marco intermedio tenía que aguantar en
algún lugar, era ahí.

### El método es otro, y eso salió a favor

`[M]` El alineamiento se hizo con `PairwiseAligner` de Biopython —el método de `C8`— contra los
contigs que la ola 3 ya había ubicado. `GITV01000968.1` cubre el gen **entero, 2.520 de 2.520
posiciones, en un solo bloque sin huecos**, con **7 desajustes** contra la secuencia de EPILAB. El
script exige esa cobertura y aborta si no la tiene: rellenar posiciones con bases de EPILAB daría
una quimera y no una fuente.

`[M]` **El ancla se reprodujo con el otro alineador.** En el marco 3 la reconstrucción da 25, 19 y
17, que son exactamente los tres conteos que `M7` publicó con blastn. Dos métodos de alineamiento
distintos dan los mismos tres números, así que **la reconstrucción no depende del alineador**.

### Los tres marcos con la secuencia de GITV01

`[M]` Modo `corregido`, ViennaRNA 2.7.2, tabla `RNA_NN3`, punto por defecto.

| Región | EPILAB m1 / m2 / m3 | GITV01 m1 / m2 / m3 | Desajustes en la región |
|---|---|---|---:|
| 922-1221 | 36 / 29 / 26 | **34 / 27 / 25** | 2 |
| 2121-2420 | 35 / 27 / 22 | **27 / 19 / 19** | 3 |
| 264-563 | 20 / 15 / 17 | **20 / 15 / 17** | 0 |

`[M]` **El orden no se mueve en ninguno de los tres marcos, y el margen se abre.** Con la
secuencia de GITV01, 922-1221 le gana a 2121-2420 por 7 ventanas en el marco 1, por 8 en el marco
2 y por 6 en el marco 3, contra 1, 2 y 4 con la secuencia de EPILAB.

### Y esto corrige una lectura nuestra

`[M]` `M7` §4 escribió que «la eficiencia casi no se mueve al cambiar de referencia» y que «que la
secuencia cambie en tres o siete bases y el conteo se mueva en una o tres ventanas es consistente
con lo que ya sabíamos del criterio». **En el marco 3 eso es cierto; en los marcos de contexto
no.** Las mismas tres bases que mueven el conteo de 2121-2420 en tres ventanas al plegar la
molécula sola lo mueven en **ocho** al plegar el gen completo: de 27 a 19 en el marco 2, que es el
30 % del conteo por el 1 % de la secuencia.

`[H]` El mecanismo es coherente y vale decirlo: **el marco de contexto amplifica el efecto de un
cambio de secuencia, porque el plegado es global.** Un desajuste puede cambiar la accesibilidad de
ventanas que están lejos de él, y la molécula recortada acota ese alcance por construcción. La
consecuencia práctica es incómoda y es la misma de toda esta línea: el marco no es una convención
de contabilidad, decide cuánta sensibilidad tiene el número a cada cosa que se cambie.

## 8. Lo que esta línea todavía no hace

`[?]` El marco intermedio en las otras tres fuentes del eje de referencia, por los motivos de la
tabla de arriba. Hace falta `blastn` en el PATH y las bases de `work/W5/db/`; con eso, el camino
corto es agregarle el marco intermedio a `eje_referencia.py` de `M7`, que ya hace las cuatro.

## Archivos

| Archivo | Qué es |
|---|---|
| `scripts/tres_marcos.py` | los tres marcos de las seis regiones, con las anclas que abortan |
| `scripts/marco2_en_la_grilla.py` | el marco intermedio en las 4.368 configuraciones, con las cuatro fracciones de M7 como ancla |
| `scripts/terminos_por_region.py` | el comparador de M2 sobre las tres regiones que M7 no cubrió, con las anclas de la sección 2 |
| `scripts/marco2_por_fuente.py` | la reconstrucción del gen desde GITV01 y los tres marcos sobre esa secuencia, con el ancla de M7 §4 |
| `resultados/tres_marcos.tsv` | la tabla de la sección 2 |
| `resultados/tres_marcos.json` | lo mismo, con las posiciones que ganan y pierden en cada región |
| `resultados/marco2_en_la_grilla.json` | las seis fracciones de la sección 6, con empates y margen mediano |
| `resultados/terminos_*_cambios.tsv` | una fila por ventana que cambia, con el término que cruzó y cuánto se movió cada término continuo |
| `resultados/terminos_por_region.json` | los seis pares de la sección 5 y el recuento por término |
| `resultados/marco2_por_fuente.json` | los tres marcos con la secuencia de GITV01, los desajustes posición por posición y las tres fuentes no corridas con su motivo |
