# C9 — Sensibilidad de la recomendación a los umbrales de si-Fi21 (sin etiquetas)

**Qué mide y qué no.** Este informe mide **cuán frágil es nuestra recomendación** frente a los dos umbrales de si-Fi21 que no tienen fuente primaria (brecha de estabilidad de extremos, 1,00 kcal/mol; corte de accesibilidad, 0,1). **No mide si 0,1 y 1,00 son los valores correctos**: eso exige etiquetas de eficacia que no existen para *Dalbulus maidis*. `[H]`

**Declaración de motor.** Todo corre con el backend `vienna` (ViennaRNA 2.7.2), a 22 °C, ventana de 21 nt, `u = 8`. RNAplfold 2.1.5 (ejecutable de Windows de si-Fi21) no está disponible, de modo que **los conteos absolutos no son comparables con los verificados contra el programa original en la ola 2**; las comparaciones internas sí valen porque ambos lados usan el mismo motor. Cada número se declara en modo `fiel` (rama terminal original) o `corregido`.

## Respuesta

La **identidad del candidato superior es robusta** y la **posición exacta de la región de 200 nt no lo es**.

El candidato de mayor eficacia, `MP_MRFV`, queda primero en el 99,1 % de la grilla en modo fiel y en el 98,2 % en modo corregido (546 puntos por modo: 21 brechas de 0,0 a 2,0 kcal/mol × 26 accesibilidades de 0,05 a 0,30). Con la otra variable en su valor por defecto, sigue primero en todo el rango barrido de accesibilidad (0,05–0,30) y, para la brecha, en 0,0–1,9 (fiel) y 0,0–2,0 (corregido). Los pares de la tabla de abajo, salvo uno, no se invierten en más del 6 % de la grilla.

El **par `ATPaseD_Dm` / `CP_MRFV` es un empate práctico**: en el valor por defecto difiere en 0,015 (fiel) y 0,010 (corregido) de eficacia de región, es decir 3 y 2 ventanas de 200, y se invierte en el 47,4 % y el 48,9 % de la grilla, con 15,6 % y 23,4 % de empates exactos. Cualquier afirmación sobre cuál de los dos queda tercero o cuarto **no se sostiene** con estos umbrales. `[H]`

La **región recomendada sí se mueve**. En modo fiel la región por defecto de `MP_MRFV` (75–274) se conserva exacta en un intervalo de accesibilidad de 0,09–0,11 y en todo el rango de brecha barrido; en modo corregido (72–271) en 0,06–0,13. Sobre la grilla completa, la región superior de `MP_MRFV` coincide exactamente con la de defecto en el 11,7 % (fiel) y el 25,8 % (corregido) de los puntos. Un solapamiento de al menos 100 nt con la región por defecto ocurre para `MP_MRFV` en el 24,4 % (fiel) y el 30,2 % (corregido), y hay puntos con solapamiento cero. `CP_MRFV` es la excepción estable (solapamiento mínimo 104 y 103 nt). `BicC_Dm` (2.520 nt) tiene el solapamiento mínimo en cero.

**Lectura para la reunión.** Decir «el umbral no cambia la recomendación» es cierto a nivel de candidato y falso a nivel de ventana. Lo defendible es: *elegiríamos el mismo gen aunque el umbral fuera otro, pero las coordenadas de la región dependen de él y deben tratarse como una región candidata y no como un sitio.* `[H]`

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

## Alcance y límites

La grilla es de 21 × 26 puntos por modo y cuatro genes; las cifras de «fracción de la grilla» dependen de qué tan ancha se elija la grilla, así que son una medida de fragilidad relativa y no una probabilidad. Los dos ejes del ranking (limpieza contra el panel de referencias) **no se calcularon**: el barrido usa solo la eficacia de región, y la limpieza tiene una palanca acotada (factor 1,015–1,064 entre candidatos, frente a 2,38–2,50 de la eficacia). `eth` y `burs-alpha` no se incluyeron. La referencia humana no se descargó y no hizo falta, porque lo barrido son los umbrales de eficiencia y no el panel. Los umbrales de corte de 200 nt y `u = 8` no se barrieron. `[H]`

## Archivos

`scripts/barrido_umbral.py` (comando en el encabezado); `resultados/grilla_umbral.tsv` (4.368 filas), `resultados/decisiones_por_punto.tsv`, `resultados/intervalos_estabilidad.json`, `resultados/pares_orden.json`, `resultados/ancla/`.

**Nota de confidencialidad sobre el ancla.** Los TSV de `resultados/ancla/` salen de `run_sifi.py`, cuya salida incluye una columna `seq` con el 21-mero de cada ventana. Como las ventanas se solapan de a 1 nt, esa columna **permite reconstruir el gen entero**, y dos de los cuatro genes son secuencias de EPILAB. Por eso la columna se quitó antes de versionar los archivos, con `scripts/limpiar_ancla.py`: lo que queda son las posiciones, las energías, la accesibilidad y los booleanos, que es lo que el ancla necesita para reproducir conteos y regiones. Para regenerar el ancla hay que correr `run_sifi.py` y después ese script, en ese orden. Verificado: no queda ninguna racha de 21 nt o más de A, C, G o T en toda la carpeta.
