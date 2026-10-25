# N4 — Las ventanas de juntura: eficientes y sin blanco

**Ola 5, línea N4.** Fecha: 2026-10-25. Contesta el punto 3 de la carta del investigador del 25 de
octubre de 2026, en su segunda mitad: «que un siRNA atraviese una juntura no significa que
encuentre una región complementaria continua en alguno de los targets. Son aspectos diferentes que
convendría evaluar por separado» `[R]`. Reproducible con `scripts/junturas.py`. Marcadores de
`CLAUDE.md`.

## El resultado, en un párrafo

**De las 240 ventanas de juntura de las doce quimeras, cuatro son eficientes y ninguna de esas
cuatro tiene un blanco continuo: son capacidad de silenciamiento gastada** `[M]`. Ocho de las 240
sí existen como tramo contiguo de 21 nt en alguno de los cuatro genes blanco, y las ocho son las de
los extremos de la unión —las que toman uno, dos o tres nucleótidos de un fragmento y el resto del
otro—, donde los nucleótidos prestados coinciden por azar con el flanco que ese fragmento tenía en
su propio gen; ninguna de las ocho es eficiente `[M]`. La contabilidad general es la que conviene
llevar escrita: **una quimera cambia los veinte arranques de la cola de cada fragmento por veinte
ventanas de juntura que no existen en ningún blanco**, y eso es del mismo orden de magnitud que la
diferencia entre los marcos de conteo de [`N3`](../N3_marcos/REPORT.md).

## 1. Lo que ya estaba medido, y por eso esta línea es corta

`C4` y `C13` ya midieron las 240 ventanas de empalme de las doce quimeras: cuántas son eficientes
—48 con las regiones de EPILAB y **4** con las vigentes, en modo `corregido`— y qué off-targets
fabrica la unión contra las seis referencias no objetivo, incluido un bloque perfecto de 19 nt en
maíz que no existe en ninguno de los dos genes de origen `[M]`
(`research/ola3/C13_quimeras_region_recomendada/REPORT.md` §5 y §6). Eso contesta qué produce la
molécula y a qué no objetivo pega.

Lo que faltaba es la otra mitad, y es la que nadie había mirado: de esas ventanas, **cuántas tienen
blanco**. El conteo de eficientes de una quimera las cuenta como si valieran.

## 2. La contabilidad de una quimera

Con fragmentos de largo `L_i` y ventanas de 21 nt, la molécula ensamblada tiene `Σ L_i − 20`
ventanas, y se reparten así: por cada fragmento, los `L_i − 20` arranques que existen también en su
gen —los mismos del marco 2 de `N3`— y por cada unión, veinte ventanas nuevas. La cuenta cierra:
`Σ (L_i − 20) + 20 (n − 1) = Σ L_i − 20` `[M]`, y el script lo verifica en las doce.

`[H]` Dicho en una frase: la quimera no agrega ventanas, las **canjea**. Pierde los veinte
arranques de cola de cada fragmento —que existían en el blanco— y recibe veinte por unión que no
existen en ninguno. Si el canje es bueno o malo depende de cuántas de cada lado son eficientes, y
eso es lo que miden `C13` y esta línea juntas.

## 3. Las doce quimeras

`[M]` Modo `corregido`, ViennaRNA 2.7.2, tabla `RNA_NN3`, punto por defecto. Partes: las cuatro
regiones vigentes. Blancos pretendidos: los cuatro genes de EPILAB, en las dos hebras. Fuente:
`resultados/junturas.tsv`. El script **aborta** si la columna de eficientes no reproduce la de
`C13` quimera por quimera, y la reprodujo en las doce.

| Quimera | Ventanas | De juntura | Juntura eficientes | Con blanco continuo | Eficientes **sin** blanco |
|---|---:|---:|---:|---:|---:|
| `CP_MRFV` + `BicC_Dm` | 480 | 20 | 1 | 1 | 1 |
| `BicC_Dm` + `CP_MRFV` | 480 | 20 | 1 | 0 | 1 |
| `ATPaseD_Dm` + `CP_MRFV` | 480 | 20 | 1 | 0 | 1 |
| `ATPaseD_Dm` + `BicC_Dm` | 580 | 20 | 1 | 0 | 1 |
| `MP_MRFV` + `BicC_Dm` | 480 | 20 | 0 | 3 | 0 |
| `CP_MRFV` + `ATPaseD_Dm` | 480 | 20 | 0 | 2 | 0 |
| `CP_MRFV` + `MP_MRFV` | 380 | 20 | 0 | 1 | 0 |
| `BicC_Dm` + `MP_MRFV` | 480 | 20 | 0 | 1 | 0 |
| las otras cuatro | — | 20 cada una | 0 | 0 | 0 |
| **total** | | **240** | **4** | **8** | **4** |

## 4. Qué se lee

`[M]` **Las cuatro ventanas de juntura eficientes no tienen blanco continuo.** Las cuatro
quimeras que las tienen son las que combinan `CP_MRFV`, `BicC_Dm` y `ATPaseD_Dm`. `[H]` Un siRNA
que se produce y no tiene a qué unirse de forma continua no silencia nada: ocupa la maquinaria y
cuenta en el número. Es el argumento del investigador convertido en cifra, y la cifra es chica
—4 de 240— porque las regiones vigentes ya son buenas y el empalme rinde por debajo del promedio
del gen, que es el hallazgo de `C13`.

`[M]` **Las ocho con blanco son todas de los extremos de la unión.** Toman 20, 19, 18 o 2 y 1
nucleótidos de la primera parte y el resto de la segunda: en `MP_MRFV` + `BicC_Dm` son tres
seguidas, lo que significa que los tres primeros nucleótidos de la región de `BicC_Dm` coinciden
con los tres que seguían a la región de `MP_MRFV` en su propio gen. `[H]` No es un hallazgo
biológico, es aritmética de azar: una ventana que presta un solo nucleótido tiene una probabilidad
cercana a un cuarto de seguir existiendo en el gen de origen. Lo que vale es la consecuencia
metodológica: **«cruza la juntura» y «no tiene blanco» no son sinónimos**, y hay que medirlo, no
suponerlo. Él tenía razón en pedir que se evalúen por separado.

`[M]` **Ninguna de las ocho es eficiente**, así que en este conjunto las dos clasificaciones no se
cruzan: las que tienen blanco no son eficientes y las eficientes no tienen blanco.

## 5. Alcance y lo que esto no es

`[H]` Esto mide **pérdida** de eficacia sobre los blancos propios y gasto de molécula. Una ventana
sin blanco continuo es una ventana que no silencia; las coincidencias con organismos no objetivo
son otra cosa y las miden `C4`, `C13` y [`M6`](../../ola4/M6_alertas/REPORT.md), que es donde viven
las alertas. Nada de esta línea se lee como una vía para ampliar el rango de ningún agente, y por
`CLAUDE.md` cualquier resultado que se leyera así queda fuera de alcance.

`[?]` El criterio de «blanco continuo» es la coincidencia exacta de los 21 nt en una de las dos
hebras de uno de los cuatro genes. No mide apareamiento parcial ni efecto tipo miARN, que podría
dar actividad con complementariedad incompleta: eso haría que una ventana de juntura no fuera
completamente inútil, y no lo sabemos.

`[?]` Las doce uniones son doce, no 240: las veinte ventanas de una unión comparten secuencia y
contexto de plegado, así que la comparación es descriptiva y no una prueba estadística. Es la misma
advertencia que puso `C13`.

`[M]` Las secuencias no salieron de la máquina: los blancos se leen de disco, la búsqueda es
`in` sobre cadenas en memoria y la salida versionada tiene posiciones, veredictos y nombres de
gen, no nucleótidos. Con 240 consultas la búsqueda directa da la misma respuesta que el autómata
de Aho-Corasick de `offtarget_21nt.py` y no agrega una dependencia.

## Archivos

| Archivo | Qué es |
|---|---|
| `scripts/junturas.py` | la clasificación de ventanas, el ancla de `C13` y la búsqueda de blanco continuo |
| `resultados/junturas.tsv` | la tabla de la sección 3 |
| `resultados/junturas.json` | por quimera, las veinte ventanas de juntura con su veredicto y sus blancos |
