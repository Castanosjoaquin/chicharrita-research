# Fase 1 — Decisión del ranking y de las etiquetas de evidencia

Fecha: 2026-10-22. Fase del plan del checkpoint 2 (`docs/plan_checkpoint2/FASE_1_decision_ranking_y_etiquetas.md`). Estado: las dos decisiones las tomó el usuario; el ADR D38 y el ADR D39 están escritos en `00_meta/DECISIONS.md`; el diff de etiquetas está aplicado a `CLAUDE.md` y `00_meta/GLOSARIO.md`. No hay commit.

Marcadores según `CLAUDE.md`, con la nueva categoría `[M]` que esta fase introdujo. Los números salen de `research/ola3/C7_ranking_v2/resultados/ranking_v2.json` y de `research/ola3/C7_ranking_v2/resultados/por_estrategia.json`; las tablas se generaron desde esos archivos, no se retiparon.

## 1. Decisiones tomadas

**Decisión 1: estructura del ranking.** Se eligió la opción A: dos listas, una por mecanismo. Una lista es la del insecto (*Dalbulus maidis* como blanco); la otra es la del virus dentro de la planta. Es la aplicación de D34, que el entregable no había aplicado. Se descartaron la opción B (lista única con una columna cualitativa de «se entiende cómo llegaría el ARN», que sería un juicio nuestro sin medición) y la opción C (dejar la lista única con una advertencia, que deja la tensión sin resolver). `[H]` La razón de fondo es la que ya estaba en D20: los off-targets no significan lo mismo para un blanco viral que para uno del insecto, y el ranking mide calidad de diseño, no valor del blanco.

**Decisión 2: etiquetas de evidencia.** Se eligió la opción (i): un marcador nuevo `[M]` («medido por nosotros, reproducible desde el repo») para conteos, tasas y concordancias calculados por el equipo, y `[H]` para la lectura de esos números. Se descartó la opción (ii), rotular todo lo propio como `[H]`, porque un conteo exacto quedaría con la misma etiqueta que una idea sin respaldo. El diff aplicado está en `docs/plan_checkpoint2/salidas/F1_propuesta_etiquetas.diff`. Los cambios reales son: una definición de `[M]` en `CLAUDE.md`, una aclaración de que un resultado computacional propio nunca es `[E]`, y una frase en el encabezado de `00_meta/GLOSARIO.md`.

## 2. Lista del insecto (regiones recomendadas por C7)

| `BicC_Dm` | 264-563 | 2121-2420 | 2119-2418 | 35 / 40 | 0,117 / 0,133 | 0,9852 | Insecto (*D. maidis*) | Reducción de oviposición y alteración del oocito; el resumen dice hasta 170 veces de baja de transcripto, sin día ni letalidad `[R]` (DM-01, sólo resumen) |
| `eth_Dm` | no estaba en la planilla de EPILAB (la región 114-313 la propone nuestra cascada, C7 §4) | 114-313 | 193-392 | 19 / 26 | 0,095 / 0,130 | 0,9856 | Insecto (*D. maidis*) | Falla de muda; supervivencia de `eth` no separada en el texto (la cifra de 10 % a cinco días de la frase siguiente puede referirse a ambos genes), microinyección `[R]` (P3; DM-05) |
| `bursA_Dm` | no estaba en la planilla de EPILAB (la región 13-212 la propone nuestra cascada, C7 §4) | 13-212 | 44-243 | 16 / 18 | 0,080 / 0,090 | 1,0000 | Insecto (*D. maidis*) | Letalidad y falla de muda: supervivencia 10 % al día 4 en *D. maidis* según el texto, frente a >95 % de control a cinco días; microinyección `[R]` (P3; DM-06) |
| `ATPaseD_Dm` | 151-450 | 72-371 | 71-370 | 21 / 25 | 0,070 / 0,083 | 0,9774 | Insecto (*D. maidis*) | Supervivencia ≈18 % al día 4 por ingesta, frente a ≈37 % del control GFP y ≈52 % sin dsRNA; alas sin efecto significativo `[R]` (P8; DM-03) |

Las regiones recomendadas son las del nivel 3 de C7: cada gen en la mejor región que encuentra la cascada (`research/ola3/C7_ranking_v2/REPORT.md` §4 y §5). `[M]` Las regiones de 300 nt son para `BicC_Dm` y `ATPaseD_Dm`; las de 200 nt, para los demás. La evidencia de fenotipo `[R]` viene del catálogo `research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.md` (filas DM-01, DM-03, DM-05 y DM-06). Esas filas declaran apertura de texto completo leído en la ola 2, y la cifra de supervivencia de DM-03 aparece también en C7 §6; en esta fase no se reabrieron los artículos originales, así que las cifras de fenotipo se citan a través del catálogo.

**Orden dentro del grupo.** El orden no es uniforme, y la regla que se aplicó es la siguiente: un par se reporta como orden sólo si el primer elemento precede al segundo en más del 50 % de los sorteos de pesos, en todas las combinaciones de la escala absoluta y de la escala min-max, y a los dos largos (21 y 22 nt). La cascada no entra en esa prueba porque es determinista; se trata aparte. Los números de la tabla siguiente son `[M]`:

| Par | 21 nt, absoluta (%) | 21 nt, min-max (%) | 22 nt, absoluta (%) | 22 nt, min-max (%) | Veredicto |
|---|---|---|---|---|---|
| `BicC_Dm` > `ATPaseD_Dm` | 98,9–100,0 | 91,3–100,0 | 98,3–99,9 | 90,7–94,2 | sostenido a ambos largos |
| `BicC_Dm` > `eth_Dm` | 96,4–100,0 | 72,3–91,9 | 82,5–96,6 | 24,1–68,4 | sólo a 21 nt |
| `BicC_Dm` > `bursA_Dm` | 86,5–100,0 | 54,1–88,0 | 87,3–99,8 | 63,7–71,4 | sostenido a ambos largos |
| `eth_Dm` > `bursA_Dm` | 76,1–99,8 | 36,9–72,6 | 84,3–100,0 | 47,9–100,1 | sólo en absoluta; no firme (regla D38) |
| `eth_Dm` > `ATPaseD_Dm` | 99,7–99,9 | 95,0–98,4 | 95,1–100,0 | 79,1–100,0 | sostenido a ambos largos |
| `bursA_Dm` > `ATPaseD_Dm` | 100,0–100,0 | 100,0–100,0 | 100,0–100,0 | 100,0–100,0 | sostenido a ambos largos |

**Lectura.** `BicC_Dm` queda primero sobre `ATPaseD_Dm` y sobre `bursA_Dm` a ambos largos, y `ATPaseD_Dm` queda último frente a los tres demás en las escalas continuas. `BicC_Dm` sobre `eth_Dm` se sostiene sólo a 21 nt: a 22 nt, con la escala min-max, `eth_Dm` pasa a primero en el 75,9 % de los sorteos de la combinación geométrica y mecanicista (`por_estrategia.json`, bloque `insecto_recomendados|k22`). El par `eth_Dm`–`bursA_Dm` no tiene orden firme. En escala absoluta `eth_Dm` precede a `bursA_Dm` en 76,1 a 99,8 % de los sorteos a 21 nt y en 84,3 a 100 % a 22 nt. En min-max el par es inestable (36,9 a 72,6 % a 21 nt; 47,9 a 100,1 % a 22 nt), porque esa escala estira una diferencia de limpieza de unos 0,015 hasta el rango completo. A favor de `eth_Dm` están sus más ventanas eficientes en ambos largos (19 contra 16 a 21 nt; 26 contra 18 a 22 nt) y su eficacia a 22 nt (0,13 contra 0,09). La regla de D38 exige que un orden se sostenga en las dos escalas, así que el par se reporta como no firme. Si la regla fuera sólo la absoluta, el orden sería `eth_Dm` > `bursA_Dm`; esa elección es nuestra y se declara. `[M]`

**Dos advertencias sobre el último puesto.** Primera: la cascada (veto más eficientes limpias, `[M]` determinista) pone a `ATPaseD_Dm` por delante de `bursA_Dm`, a los dos largos. La razón, según C7 §4, es que la cascada cuenta ventanas y no tasas, y favorece a las regiones de 300 nt sobre las de 200. Eso invierte el resultado de las escalas continuas, así que `bursA_Dm` frente a `ATPaseD_Dm` es **dependiente del método** `[?]`. Segunda: el orden de todo el grupo del insecto depende del criterio de agregación. Con la escala min-max a 22 nt, `BicC_Dm` deja de ser primero de forma mayoritaria: gana el 49,6 % de los sorteos en la combinación geométrica y conservadora, y el 24,1 % en la geométrica y mecanicista. Eso es sensibilidad a la escala, no una propiedad de los genes.

**Matar contra esterilizar.** No es un problema de cómputo: es una falta de datos. Para comparar los dos objetivos hace falta, por gen, un desenlace de letalidad y otro de reproducción medidos en la misma especie. Lo que hay:
- `eth` y `burs-alpha` (P3, Andrada *et al.* 2026): letalidad y falla de muda medidas; la descendencia y la reproducción no se midieron, y el propio artículo lo deja como trabajo futuro `[R]`.
- `BicC` (Dalaisón-Fuentes *et al.* 2022, resumen en PubMed): reducción de oviposición y alteración del desarrollo del oocito; el resumen no reporta letalidad ni el día del efecto `[R]`. El texto completo no es de acceso abierto (Europe PMC no tiene la versión OA), así que el resto de la evidencia no se pudo verificar `[?]`.
- `ATPaseD` (Jones *et al.* 2021, preprint con texto completo leído ahora): supervivencia y alas, sin reproducción `[R]`.
Con eso no se puede ordenar «matar» contra «esterilizar» entre los cuatro: sólo `BicC` tiene una medida de reproducción y no tiene una de letalidad verificada. La comparación queda como límite declarado y como pregunta para el investigador, no como eje del ranking. `[?]`

**Corrección al brief de la fase.** La fase dice que, con `eth` y `burs-alpha`, el catálogo de C5 «sesga a esterilidad». El catálogo registra **letalidad** para los dos (supervivencia del 10 % al día 4 frente a más del 95 % del control; filas DM-05 y DM-06). La esterilidad es el fenotipo de `BicC` (DM-01). Esta salida usa el catálogo como fuente.

## 3. Lista del virus dentro de la planta (regiones recomendadas por C7)

| `MP_MRFV` | 1-200 | 72-271 | 162-361 | 38 / 30 | 0,190 / 0,150 | 0,9796 | Virus dentro de la planta de maíz | Sin medición propia del ARNi sobre el gen `[?]` |
| `CP_MRFV` | 201-400 | 99-298 | 77-276 | 21 / 22 | 0,105 / 0,110 | 0,9910 | Virus dentro de la planta de maíz | Sin medición propia del ARNi sobre el gen `[?]` |

**Orden.** `MP_MRFV` queda primero y `CP_MRFV` segundo en las escalas absolutas, en todas las combinaciones, con un mínimo de 78,5 % (`por_estrategia.json`, bloque `virus|k22`). Con la escala min-max la prueba no es informativa: con dos candidatos, min-max manda uno a 0 y el otro a 1 en cada eje, y el resultado queda determinado por la escala y no por la magnitud de la diferencia. A 21 nt, las cuatro combinaciones que usan min-max dan 51,5 % (`por_estrategia.json`, bloque `virus|k21`). W7 §2.1 lo advierte y `test_ranking.py` lo fija como prueba, así que no se cita como hallazgo. `[M]`

**Qué respalda este orden y qué no.** `MP_MRFV` tiene la mayor eficacia en la región recomendada, pero su evaluación por conservación es débil: sólo 4 de 71 registros de GenBank cubren su región y dos son la referencia (`research/ola3/C8_conservacion/REPORT.md`, resumen). `[M]` Ninguno de los dos genes virales tiene medición propia del ARNi, y su mecanismo antiviral ocurre en la planta, no en el insecto (C7 §6). `[?]`

## 4. Por qué las dos listas no se comparan

Las dos listas no se comparan entre sí. Los off-targets no significan lo mismo en un gen viral que en uno del insecto: para los genes del insecto el genoma de *D. maidis* se excluye por ser on-target, mientras que para los virales entra como off-target (D20). Además, el ranking mide calidad de diseño dentro de un gen, no el valor del blanco, y el valor del blanco se mide por fenotipo, que el ranking no mide (C7 §6, que remite a W7 §5). `[H]` Si se forzara un orden único, los dos virales quedarían arriba, y eso sería un artefacto del ranking, no una conclusión sobre el blanco.

## 5. Regla de etiquetas para la Fase 5 (definida, no aplicada)

La regla que la Fase 5 debe aplicar sobre `entregables/para-el-investigador.md` es la siguiente. Hay 11 líneas con `[E]` en ese archivo. Cada una se revisa:

1. Si la afirmación es consenso de literatura revisada, se deja como `[E]`.
2. Si el número o la comparación salen de un script propio del repo, pasa a `[M]` y se agrega la ruta del archivo de salida.
3. Si es la lectura de un `[M]` (lo que significa, a qué lleva), pasa a `[H]`.
4. En la página y en la diapositiva, «ventana eficiente» se reemplaza por «ventana que pasa el filtro de si-Fi21».

No se aplicó. Esa edición le corresponde a la Fase 5.

## 6. Qué quedó sin hacer y por qué

1. **Escala z contra min-max.** La fase pide comparar una escala z con la min-max. `ranking_v2.json` y el código tienen sólo las escalas absoluta y min-max, así que la z no se calculó. La comparación se hizo contra min-max, que es la alternativa que ya usa W7 (`research/ola2/W7_ranking/REPORT.md` §2.1).
2. **Matar contra esterilizar sobre `eth` y `burs-alpha`.** Ver §2. Pendiente.
3. **Fuentes originales.** La revisión posterior (§8) reabrió P3 (PDF local, con la figura 5 renderizada) y el preprint de Jones 2021 (texto completo en bioRxiv). Dalaisón-Fuentes 2022 no es de acceso abierto y se verificó sólo el resumen. `[?]`
4. **Cómputo nuevo.** No hubo cómputo nuevo. `research/ola3/C7_ranking_v2/scripts/resumen_por_estrategia.py` relee los barridos de 2.000 sorteos ya guardados y los reagrupa por par y por escala; no recalcula puntajes.
5. **Aplicación de la regla de etiquetas.** Se definió, no se aplicó (§5). Pasa a la Fase 5.
6. **Commit, push y `estado.html`.** No se hizo commit ni push, como pidió el usuario. `estado.html` no se regeneró; le corresponde a la Fase 5.

## 7. Entregas de la fase

- Esta salida: `docs/plan_checkpoint2/salidas/F1_decision_ranking.md`.
- Diff de etiquetas: `docs/plan_checkpoint2/salidas/F1_propuesta_etiquetas.diff` (aplicado).
- Cómputo de reagrupación: `research/ola3/C7_ranking_v2/scripts/resumen_por_estrategia.py` y su salida `research/ola3/C7_ranking_v2/resultados/por_estrategia.json`.
- ADR D38 y ADR D39 en `00_meta/DECISIONS.md`.
- Cambios de reglas: `CLAUDE.md` y `00_meta/GLOSARIO.md`.

## 8. Revisión posterior (2026-10-22): cifras verificadas y correcciones

**Qué se reabrió.**
- *Andrada et al.* 2026 (P3, `YHat-Biotech/Papers/finsc-6-1811933.pdf`): texto completo y figura 5 renderizada. Esta fue la fuente de las correcciones de `eth` y `burs-alpha`.
- *Jones, Bernal y Medina* 2021 (preprint, doi 10.1101/2021.09.29.462424): texto completo en bioRxiv, leído ahora (ver nota de conflicto más abajo).
- *Dalaisón-Fuentes et al.* 2022 (doi 10.1002/ps.6937): sólo resumen, vía PubMed. Europe PMC no tiene la versión de acceso abierto.

**Correcciones a lo escrito antes.**
1. **`eth`, supervivencia en *D. maidis*.** El 10 % a día 4 que aparecía en el catálogo (DM-05) y en C7 §6 es el de `burs-alpha`, según el texto. Para `eth` el texto no da cifra propia. La frase «sólo 10 % de *D. maidis* y 20 % de *D. kuscheli* completaron la muda y siguieron vivos a cinco días» sigue al párrafo de `eth` y puede referirse a ambos genes. La figura 5A no se pudo leer de forma verificable en esta sesión `[?]`.
2. **Control de supervivencia.** El texto dice «>95 %» de supervivencia en los controles *a cinco días*, no a día 4 como se escribió antes. El pie de la figura 5 dice que la medición es a cuatro días; su valor de control no se pudo leer de forma verificable.
3. **`BicC` como «esterilidad».** El resumen dice reducción de oviposición y alteración del oocito. No dice que sea esterilidad ni letalidad. «Esterilidad», «>170 veces al día 7» y «casi nula» no aparecen en el resumen. Quedan `[?]` hasta tener el texto completo.
4. **`ATPaseD`, control.** Jones 2021 tiene un control GFP (≈37 % a día 4) y un control sin dsRNA (≈52 %). La cifra de 18 % no es frente a «nada»: es frente al GFP. Las alas no difieren de forma significativa para V-ATPase D (χ² = 2,13, p = 0,144).
5. **Conflicto de fuentes.** `00_meta/FUENTES.md` (S18) dice que el texto completo de Jones 2021 «no es accesible», pero el catálogo C5 lo marca como leído en la ola 2. Ahora se leyó desde bioRxiv; FUENTES debe corregirse.

**Escala z, pedido en la revisión.**
- No se pudo correr el barrido completo con z: hace falta el dato por ventana (`work/sifi_v2/` y los FASTA de EPILAB no están en disco), y `ranking_v2.json` sólo tiene conteos por región.
- Se hizo un barrido reducido con z y min-max sólo sobre la eficacia, con pesos base fijos. Al compararlo con el barrido guardado (min-max, `insecto_recomendados`), las diferencias llegan a 38 puntos porcentuales. No está calibrado, así que no se reporta como resultado.
- Con dos candidatos, z y min-max dan lo mismo por construcción (50 % a 50 %). Además, z puede dar valores negativos, que no son válidos dentro de una media geométrica.
- Conclusión: la escala z no agrega información a lo ya medido. Queda declarada como no hecha.

**Lo que no se verificó.**
- Dalaisón-Fuentes 2022: sólo resumen.
- La figura 5B (*D. kuscheli*) no se usó en el texto de F1.
- El control de ARN de `burs-α` (`ds-βlac`) y su dosis se tomaron del texto del artículo.
