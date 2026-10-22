# C9 — Sensibilidad de la recomendación a los umbrales de si-Fi21 (sin etiquetas)

**Qué mide y qué no.** Este informe mide **cuán frágil es nuestra recomendación** frente a los dos umbrales de si-Fi21 que no tienen fuente primaria (brecha de estabilidad de extremos, 1,00 kcal/mol; corte de accesibilidad, 0,1). **No mide si 0,1 y 1,00 son los valores correctos**: eso exige etiquetas de eficacia que no existen para *Dalbulus maidis*. `[H]`

**Declaración de motor.** Todo corre con el backend `vienna` (ViennaRNA 2.7.2), a 22 °C, ventana de 21 nt, `u = 8`. RNAplfold 2.1.5 (ejecutable de Windows de si-Fi21) no está disponible, de modo que **los conteos absolutos no son comparables con los verificados contra el programa original en la ola 2**; las comparaciones internas sí valen porque ambos lados usan el mismo motor. Cada número se declara en modo `fiel` (rama terminal original) o `corregido`.

## Respuesta

La **identidad del candidato superior es robusta** y la **posición exacta de la región de 200 nt no lo es**.

El candidato de mayor eficacia, `MP_MRFV`, queda primero en el 99,1 % de la grilla en modo fiel y en el 98,2 % en modo corregido (546 puntos por modo: 21 brechas de 0,0 a 2,0 kcal/mol × 26 accesibilidades de 0,05 a 0,30). Con la otra variable en su valor por defecto, sigue primero en todo el rango barrido de accesibilidad (0,05–0,30) y, para la brecha, en 0,0–1,9 (fiel) y 0,0–2,0 (corregido). Los pares de la tabla de abajo, salvo uno, no se invierten en más del 6 % de la grilla.

El **par `ATPaseD_Dm` / `CP_MRFV` es un empate práctico**: en el valor por defecto difiere en 0,015 (fiel) y 0,010 (corregido) de eficacia de región, es decir 3 y 2 ventanas de 200, y se invierte en el 47,4 % y el 48,9 % de la grilla, con 15,6 % y 23,4 % de empates exactos. ~~Cualquier afirmación sobre cuál de los dos queda tercero o cuarto **no se sostiene** con estos umbrales.~~ **Corrección de alcance (2026-10-21, T1 bis).** Eso vale para la ventana libre de 200, que no es la regla con la que se eligieron las regiones del entregable. La ventana libre de `ATPaseD_Dm` en modo corregido es 272–471 y contiene las tres coincidencias perfectas con *Homalodisca vitripennis* de 392–394, de modo que **está vetada** en el ranking: el empate comparaba la región que sí proponemos para `CP_MRFV` contra una de `ATPaseD_Dm` que no proponemos. Con la región propuesta y el veto aplicado la diferencia en el defecto es 0,035 y el orden se da vuelta en el 3,3 % de la grilla (21 nt, modo corregido). Ver la sección **T1 bis**. `[H]`

La **región recomendada sí se mueve**. En modo fiel la región por defecto de `MP_MRFV` (75–274) se conserva exacta en un intervalo de accesibilidad de 0,09–0,11 y en todo el rango de brecha barrido; en modo corregido (72–271) en 0,06–0,13. Sobre la grilla completa, la región superior de `MP_MRFV` coincide exactamente con la de defecto en el 11,7 % (fiel) y el 25,8 % (corregido) de los puntos. Un solapamiento de al menos 100 nt con la región por defecto ocurre para `MP_MRFV` en el 24,4 % (fiel) y el 30,2 % (corregido), y hay puntos con solapamiento cero. `CP_MRFV` es la excepción estable (solapamiento mínimo 104 y 103 nt). `BicC_Dm` (2.520 nt) tiene el solapamiento mínimo en cero.

**Lectura para la reunión.** Decir «el umbral no cambia la recomendación» es cierto a nivel de candidato y falso a nivel de ventana. Lo defendible es: *elegiríamos el mismo gen aunque el umbral fuera otro, pero las coordenadas de la región dependen de él y deben tratarse como una región candidata y no como un sitio.* `[H]` T1 bis mide esa frase: reeligiendo con la regla del ranking el gen no cambia en el 100 % de la grilla a 21 nt, y lo que no aguanta es **congelar las coordenadas**, que deja a `MP_MRFV` primero en apenas el 62 %.

## Ancla

Antes de usar la grilla se verificó que el punto por defecto (1,00 kcal/mol, 0,1) reproduce, gen por gen y en los dos modos, el conteo y la región que da el CLI de producción (`run_sifi.py --backend vienna`). Coinciden los ocho casos. Conteos de eficientes en el punto por defecto: fiel 35 / 223 / 39 / 142 y corregido 29 / 171 / 30 / 123 para `ATPaseD_Dm` / `BicC_Dm` / `CP_MRFV` / `MP_MRFV`. Archivos en `resultados/ancla/`.

## Resultados por par (modo fiel / corregido)

| Par | Diferencia en el defecto (fiel / corr.) | Invertido en la grilla (fiel / corr.) |
| --- | --- | --- |
| `ATPaseD_Dm` – `CP_MRFV` | −0,015 / −0,010 | 47,4 % / 48,9 % |
| `BicC_Dm` – `CP_MRFV` | +0,045 / +0,020 | 1,5 % / 5,9 % |
| `ATPaseD_Dm` – `BicC_Dm` | −0,060 / −0,030 | 0,4 % / 2,7 % |
| `BicC_Dm` – `MP_MRFV` | −0,035 / −0,065 | 0,0 % / 0,5 % |
| `ATPaseD_Dm` – `MP_MRFV` | −0,095 / −0,095 | 0,0 % / 0,0 % |
| `CP_MRFV` – `MP_MRFV` | −0,080 / −0,085 | 0,0 % / 0,0 % |

## T1 bis · El mismo barrido, sobre la región que proponemos y con el veto

**Por qué hizo falta.** El barrido de arriba elige en cada punto de la grilla la ventana de 200
posiciones más densa del gen: sin veto, libre de moverse a cualquier parte y con el mismo largo
para los cuatro genes. Esa no es la regla con la que se armaron las regiones del entregable. El
ranking ([W7 nivel 3](../../ola2/W7_ranking/REPORT.md), [C7 v2](../C7_ranking_v2/REPORT.md))
elige la región más densa **que escapa al veto de coincidencia perfecta de 21 nt contra el panel
de referencias** y **conserva el largo al que fue elegida**: 200 posiciones en los dos genes
virales y 300 en los dos del insecto, que es el largo del amplicón de la planilla de EPILAB. Con
la ventana libre la comparación entre esos dos grupos enfrenta densidades sobre denominadores
distintos, y en el caso de `ATPaseD_Dm` enfrenta además una región vetada. `[E]`

**Qué se corrió.** `scripts/barrido_region_propuesta.py`: la misma grilla (21 brechas × 26
accesibilidades por modo), ahora **a 21 y a 22 nt** y sobre los **seis candidatos** del ranking
v2 —se suman `eth_Dm` y `burs-alpha`, que el barrido anterior no incluía—, con cuatro escenarios
en cada punto: la región de la planilla fija, la región que proponemos fija, la región reelegida
en ese punto con la regla del ranking (largo propio del gen más veto) y la ventana libre de 200
del barrido anterior, que queda de ancla. 52.416 filas. Las posiciones vetadas se leen de
`C7_ranking_v2/resultados/ranking_v2.json`; no dependen de los umbrales de si-Fi21, porque son
coincidencia de secuencia contra el panel.

**Anclas.** El escenario de ventana libre reproduce `grilla_umbral.tsv` en **4.368 de 4.368
filas**: inicio, fin y conteo de la región, en los dos modos y en los cuatro genes. El punto por defecto en modo corregido reproduce las
fichas de C7 v2 —eficientes del gen, ventanas del gen y eficientes de la región— en **12 de 12**
casos (seis genes × dos largos de ventana). `[E]`

**La regla reencuentra la región propuesta.** En el punto por defecto, a 21 nt y modo corregido,
reelegir con la regla devuelve exactamente la región del entregable en `MP_MRFV` (72–271),
`CP_MRFV` (99–298), `ATPaseD_Dm` (72–371) y `eth_Dm` (114–313); difiere en 2 nt en `BicC_Dm`
(2123–2422 contra 2121–2420) y en 32 en `burs-alpha` (45–244 con 17 ventanas eficientes, contra
13–212 con 16). Las dos diferencias tienen la misma causa, y es una limitación declarada de este
barrido: la regla que se barre es la **cascada reducida** —veto duro más densidad de eficientes—
y no la cascada completa, que cuenta «eficientes limpios» y es la que produce el corrimiento de
dos nucleótidos de `BicC_Dm` (el que introduce la referencia humana) y la ventana de
`burs-alpha`. `[R]`

### El par `ATPaseD_Dm` / `CP_MRFV`, que era el empate

| Escenario | k | fiel: dif. en el defecto / invertido | corregido: dif. / invertido |
| --- | --- | --- | --- |
| Ventana libre de 200 (barrido anterior) | 21 | −0,015 / 47,4 % | −0,010 / 48,9 % |
| Región que proponemos, congelada | 21 | −0,035 / 30,4 % | −0,035 / 21,4 % |
| Región reelegida con la regla | 21 | −0,035 / 13,4 % | −0,035 / **3,3 %** |
| Ventana libre de 200 | 22 | +0,010 / 1,1 % | −0,005 / 78,8 % |
| Región que proponemos, congelada | 22 | −0,008 / 81,9 % | −0,027 / 33,9 % |
| Región reelegida con la regla | 22 | −0,008 / 73,3 % | −0,027 / 20,0 % |

**A 21 nt el par deja de ser un empate práctico.** Con la regla del ranking la diferencia en el
punto por defecto es 0,035 en vez de 0,010 —`ATPaseD_Dm` tiene 21 ventanas eficientes sobre 300
y `CP_MRFV` 21 sobre 200, que es el mismo numerador sobre denominadores distintos— y el orden se
da vuelta en el **3,3 %** de la grilla en modo corregido y en el 13,4 % en fiel, contra 47–49 %
de la ventana libre. A 22 nt el par se afloja otra vez (20,0 % en corregido) y en modo fiel a
22 nt no se sostiene nada (73,3 %), que es el único cruce donde la ventana libre es más estable
que la regla. `[H]`

### Lo que se fortalece y lo que no

**El candidato superior sale más robusto, no menos.** Reeligiendo con la regla, `MP_MRFV` queda
primero en el **100 % de la grilla** a 21 nt en los dos modos, y en el 98,0 % (fiel) y el 99,6 %
(corregido) a 22 nt. Con la ventana libre eran 99,1 % y 98,0 %. `[E]`

**Congelar las coordenadas es lo frágil.** Si en vez de reelegir se dejan fijas las coordenadas
que propone el entregable y se mueve el umbral, `MP_MRFV` queda primero en apenas el 62 % de la
grilla a 21 nt y el 50 % a 22 nt. Es la versión medida de «región candidata, no un sitio»: lo que
se entrega no son coordenadas que aguanten cualquier umbral, sino **el resultado de correr una
regla**; si el umbral cambia, hay que volver a correrla, y el informe tiene que decir con qué
umbral se corrió. `[H]`

**`MP_MRFV` tiene una segunda región que compite de cerca.** Reeligiendo con la regla a 21 nt y
modo corregido, la región ganadora es 72–271 en el 30 % de los puntos y una familia alrededor de
**490–689 en el 67 %**. En el punto por defecto 72–271 tiene 38 ventanas eficientes y 491–690
tiene 32: seis ventanas de ventaja que el barrido da vuelta en dos tercios de la grilla. Es la
alternativa concreta que hay que mirar antes de comprometerse con un solo fragmento, y no estaba
nombrada en ningún informe. `[H]`

**Los empates que quedan son otros pares.** Con la regla, a 21 nt y modo corregido, los que no se
sostienen son `CP_MRFV` / `burs-alpha` (47,8 % invertido), `eth_Dm` / `burs-alpha` (49,6 %) y,
más flojos, `ATPaseD_Dm` / `eth_Dm` (22,9 %) y `ATPaseD_Dm` / `burs-alpha` (19,0 %). El orden
entre los tres últimos puestos del ranking de seis no es defendible con estos umbrales; el
primero sí, y a 21 nt el último también. La conclusión de C9 no se cae: cambia de par. `[H]`

**Lo que este barrido sigue sin medir.** El eje de limpieza ponderado, el sorteo de pesos (que es
otra perilla: ver §2.1 bis de W7), el largo de la región, `u = 8` y cualquier cosa que necesite
etiquetas de eficacia en *Dalbulus maidis*, que no existen. `[H]`

## Alcance y límites

La grilla es de 21 × 26 puntos por modo y cuatro genes; las cifras de «fracción de la grilla» dependen de qué tan ancha se elija la grilla, así que son una medida de fragilidad relativa y no una probabilidad. Los dos ejes del ranking (limpieza contra el panel de referencias) **no se calcularon**: el barrido usa solo la eficacia de región, y la limpieza tiene una palanca acotada (factor 1,015–1,064 entre candidatos, frente a 2,38–2,50 de la eficacia). ~~eth y burs-alpha no se incluyeron.~~ (T1 bis los incluye, y barre también 22 nt.) La referencia humana no se descargó y no hizo falta, porque lo barrido son los umbrales de eficiencia y no el panel. Los umbrales de corte de 200 nt y `u = 8` no se barrieron. `[H]` **Enmienda de T1 bis.** El veto duro de 21/21 contra el panel sí entra, y el largo de región pasa a ser el propio de cada gen (300 nt en los dos del insecto). Lo que sigue sin barrerse es el eje de limpieza ponderado —la exposición y el conteo de «eficientes limpios»—, que necesita la tabla de off-targets por ventana, y `u = 8`.

## Archivos

`scripts/barrido_umbral.py` (comando en el encabezado); `resultados/grilla_umbral.tsv` (4.368 filas), `resultados/decisiones_por_punto.tsv`, `resultados/intervalos_estabilidad.json`, `resultados/pares_orden.json`, `resultados/ancla/`. De T1 bis: `scripts/barrido_region_propuesta.py`, `resultados/grilla_region_propuesta.tsv` (52.416 filas) y `resultados/pares_region_propuesta.json`.

**Nota de confidencialidad sobre el ancla.** Los TSV de `resultados/ancla/` salen de `run_sifi.py`, cuya salida incluye una columna `seq` con el 21-mero de cada ventana. Como las ventanas se solapan de a 1 nt, esa columna **permite reconstruir el gen entero**, y dos de los cuatro genes son secuencias de EPILAB. Por eso la columna se quitó antes de versionar los archivos, con `scripts/limpiar_ancla.py`: lo que queda son las posiciones, las energías, la accesibilidad y los booleanos, que es lo que el ancla necesita para reproducir conteos y regiones. Para regenerar el ancla hay que correr `run_sifi.py` y después ese script, en ese orden. Verificado: no queda ninguna racha de 21 nt o más de A, C, G o T en toda la carpeta.
