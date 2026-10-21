# Evidencia de largo: cuánta coincidencia hace falta (Q1) y cuán largo conviene el ARNdc (Q4)

Las dos tablas de esta investigación. Cada fila sale de un trabajo que abrimos y leímos;
el identificador remite a `sources.json`. Donde el dato es de contexto experimental
—especie, forma de entrega, n, medida— se transcribe tal como lo declara el trabajo, y
donde no lo pudimos extraer se dice «no extraído» en lugar de completarlo por verosimilitud.

Dos advertencias de lectura. La primera: casi toda la evidencia de largo mínimo de
coincidencia viene de **Coleoptera**, de un solo sistema experimental (el ARNdc DvSnf7
contra *Diabrotica virgifera virgifera*), y de un solo grupo de autores; no hay un
equivalente en Hemiptera. La segunda: «no hubo actividad» en un bioensayo de mortalidad
no es lo mismo que «no hubo silenciamiento»: la mayoría de los trabajos miden fenotipo
—mortalidad, peso, muda— y no transcrito del gen no objetivo, así que los umbrales que
sostienen están calibrados contra un efecto letal y no contra una caída de ARN mensajero.

---

## Q1 — Largo mínimo de identidad y desajustes tolerados

### Lo medido en insectos

| Fuente | Especie y sistema | ARN y entrega | n | Medida | Qué muestra sobre el umbral |
| --- | --- | --- | --- | --- | --- |
| `S01` Bachman et al. 2013 | *Diabrotica virgifera virgifera* (Coleoptera) y *Leptinotarsa decemlineata*, alimentados con ARNdc de ortólogos de Snf7 de 10 coleópteros | ARNdc de 240 pb en dieta artificial, 500–5.000 ng/mL (50–1.000 × la CL50 conespecífica) | según especie, 3–5 réplicas de 10–20 larvas (p. ej. 4 × 20 = 80 insectos por tratamiento en el bioensayo de *C. maculata*) | supervivencia a 12 días, peso, desarrollo | Los ortólogos con **≥ 3 coincidencias de 21 nt** fueron activos; los que tienen **cero coincidencias de 21 nt**, con bloque contiguo máximo de 14, 17 o 19 nt y 78–82 % de identidad global, **no** fueron activos. `[E]` |
| `S02` Bolognesi et al. 2012 | *Diabrotica undecimpunctata howardi* (Coleoptera) | serie de ARNdc sintéticos: 27 pb de DvSnf7 embebidos en acarreador neutro hasta 40, 50, 60, 70, 80, 90, 100, 150 y 240 pb; dieta, 23 ng/mL | bioensayo de dieta de 12 días (n por réplica no extraído) | mortalidad corregida por Abbott | Con 27 pb de identidad alcanza para matar **si el ARNdc total llega a 60 pb**: 0 % a 27 y 40 pb, 16 % a 50, 68 % a 60, 95–96 % de 70 a 240. El acarreador solo da 0 %. `[E]` |
| `S02` Bolognesi et al. 2012 | ídem | seis tramos distintos de **21 pb** de DvSnf7, embebidos en acarreador hasta 240 pb, contra el mismo tramo de 21 pb desnudo | ídem | CL50 a 12 días | **Un solo bloque de 21 nt idénticos basta**: CL50 de 13,8 a 20,3 ng/mL embebido, contra > 100 ng/mL desnudo. `[E]` |
| `S03` Tan et al. 2015 | *Apis mellifera* (Hymenoptera), adultos y larvas | DvSnf7 en dieta | no extraído (de este trabajo leímos el enunciado del criterio, no su bioensayo) | mortalidad y desarrollo | Enuncia el criterio conjunto que surge de `S01` y `S02`: hace falta **un tramo 100 % complementario de ≥ 21 nt contiguos embebido en un ARNdc de ≥ 60 nt** para que haya actividad biológica contra *D. virgifera*. `[E]` |
| `S18` Castellanos et al. 2022 (sólo resumen; texto completo cerrado) | *Telenomus podisi* (Hymenoptera, parasitoide) frente a ARNdc específico de *Euschistus heros* (Hemiptera) | ARNdc en alimentación | 76,4 ± 9,9 % y 76,7 ± 8,8 % de mortalidad con ARNdc propio | expresión de los genes de mayor similitud y mortalidad | Los genes del parasitoide con **17 a 21 nt de coincidencia** con el ARNdc del chinche **no cambiaron su expresión** y no hubo efectos letales ni subletales. Es el dato más cercano a un control negativo de umbral en un no objetivo. `[R]` |
| `S04` Allen et al. 2017 | *Coleomegilla maculata* (Coleoptera, enemigo natural) frente a secuencias de ARNi usadas contra *L. decemlineata* | comparación de secuencia contra transcriptomas del benéfico, sin bioensayo | — | tramos idénticos | El gen de actina del benéfico **no tiene ningún tramo idéntico de más de 21 nt** —que los autores llaman «el largo canónico de siRNA efectivo»— pero sí un tramo de 56 nt con sólo cuatro desajustes, y por eso lo señalan como caso a evaluar. Muestra que identidad alta sin bloque perfecto largo no se descarta sola. `[R]` |

### Lo que usan las herramientas y los documentos de diseño

| Fuente | Umbral declarado | Justificación que da | Clasificación |
| --- | --- | --- | --- |
| `S06` Cedden y Bucher 2026 (revisión de métodos, *Insect Molecular Biology*) | Para un siRNA de 21 nt, **≥ 19 nucleótidos complementarios** a un transcrito no objetivo alcanzan para marcarlo como off-target potencial; en general se consideran riesgosas las coincidencias perfectas o **con hasta dos desajustes** | la capacidad del complejo RISC de tolerar unos pocos desajustes, con cita a dos trabajos que no abrimos | **convención del campo con fundamento mecánico declarado, no bioensayo** `[E]` para la existencia de la convención |
| `S07` Fletcher 2025 (dsRNAmax) | k-mero de **21 nt** por defecto; se descarta todo k-mero con **coincidencia contigua** a cualquier secuencia no objetivo, en las dos orientaciones | el 21 es la clase más abundante de siRNA en muchos organismos | convención, explícita y sin desajustes `[E]` |
| `S05` Bulgarella et al. 2025 | **21 nt, cero desajustes**, para contar off-targets de un ARNdc comercial de 402 pb en 39 especies | tamaño del producto de Dicer por orden: ~21 nt en Coleoptera, 20 en Lepidoptera, y **22 nt o mezcla de 21–22 en Hemiptera**, Orthoptera, Hymenoptera y Diptera | convención, con el detalle de que para nuestro orden el tamaño declarado es 21–22 `[E]` |
| `S08` Lück et al. 2019 (si-Fi21) | parte el disparador en todos los x-meros del largo de siRNA elegido y los busca con Bowtie contra una base de **ARNm o ADNc**; informa el número de desajustes por acierto | — | convención; el umbral de desajustes lo fija el usuario `[R]` |
| `S20` Vargas-Mejía et al. 2026 (SIREN) | predicción de off-target **acumulativa** sobre transcriptomas definidos por el usuario, con modelado termodinámico | los ARNdc largos generan muchos siRNA y el riesgo se suma | convención, con el agregado de que el riesgo se cuenta, no se binariza `[R]` |
| interno `W2` | dsRNA-Engineer: condición mayor de 21, 22 o 20 pb perfectos **por especie**, más 16 pb perfecto y 26 pb con ≤ 2 desajustes | el preprint no cita fuente para el 16 ni para la asignación de tamaño por especie | **convención sin respaldo**; en la corrida de W2, los 70 off-targets en maíz y 67 de 67 en abeja salieron de la condición de 16 pb y ninguno de la de 21 `[E]` el hecho, `[?]` la justificación |
| interno `W5`, `pipeline/` | bloque contiguo perfecto de **≥ 19 nt** como criterio de riesgo, más 21/21 y 21 nt con un desajuste como columnas separadas | se declara «el estándar del campo» sin fuente | convención, ahora respaldada como convención por `S06` `[E]` |
| `S14` Andrada et al. 2026 (nuestra propia especie) | especificidad verificada con **BLASTn contra el transcriptoma de la especie**, criterio de «sin similitud significativa» | — | el antecedente publicado en *Dalbulus maidis* **no usa un umbral en nucleótidos**, usa significancia de alineamiento `[R]` |

### La frase honesta

Con lo que abrimos: **el umbral respaldado por bioensayo en insectos es el de 21 nt contiguos
perfectos, y está respaldado en los dos sentidos** —un solo bloque de 21 nt dentro de un ARNdc
largo alcanza para matar (`S02`), y la ausencia de bloques de 21 nt predice ausencia de
actividad aun con 78–82 % de identidad global (`S01`)—, pero **toda esa evidencia viene de
Coleoptera y del mismo sistema experimental**. El umbral de **19 nt que usamos en W5 y en
`pipeline/` es convención**, con fundamento mecánico declarado en una revisión de 2026 (`S06`)
y no con un experimento que muestre silenciamiento a 19 nt en un insecto; es un umbral
*conservador*, que incluye casos que `S01` no detectó como activos. El umbral de **16 pb de
dsRNA-Engineer no tiene respaldo** en su propia documentación y domina su conteo de riesgo.
Sobre **desajustes**, no encontramos un experimento en insectos que mida silenciamiento en
función del número y la posición del desajuste: lo que hay es la convención de «hasta dos» y
el reconocimiento explícito, en `S06`, de que la distribución posicional de los desajustes y
los pares G–U no se modelan. Es un vacío documentado, no una laguna de nuestra búsqueda. `[?]`

---

## Q4 — Largo del ARNdc y eficacia

| Fuente | Especie | Largos comparados | Entrega | n | Medida | Resultado |
| --- | --- | --- | --- | --- | --- | --- |
| `S02` Bolognesi et al. 2012 | *D. undecimpunctata howardi* (Coleoptera) | 27, 40, 50, 60, 70, 80, 90, 100, 150, 240 pb | dieta, 23 ng/mL | 12 días (n por réplica no extraído) | mortalidad | **Piso de ~60 pb.** Meseta de 70 a 240 pb: 95, 95, 95, 95, 96 y 95 %. No se probó nada más largo que 240 pb. `[E]` |
| `S10` Bao et al. 2026 | *Mythimna separata* (Lepidoptera), larvas de tercer estadio | 60, 200, 500 y 1.000 pb del gen *MsChi2* | dieta artificial, 3 µg por día durante 7 días | 60 larvas por tratamiento (3 réplicas × 20) | peso, supervivencia, expresión, contenido de quitina | **200 pb fue el mejor**: 59 % de inhibición de peso, 65,9 % de mortalidad y 62 % de silenciamiento; 500 pb también significativo; 60 y 1.000 pb, peores. Dentro de los 200 pb, la **posición** del fragmento cambió la eficacia, y la eficacia correlacionó con el número de siRNA eficientes predichos. `[E]` |
| `S11` Luo et al. 2026 | *Apolygus lucorum* (Hemiptera: Miridae), ninfas de tercer estadio | genes enteros 308–358 pb; fragmentos «s» de 100–150 pb; fragmentos «ss» de 30–90 pb; recombinante de 262 pb | microinyección de 41,1–41,4 nL a 5 µg/µL | 30 ninfas × 3 réplicas por tratamiento | mortalidad acumulada a 7 días | *wupA* 310 pb → 94,4 ± 1,1 %; *Dpp* 358 pb → 92,2 ± 1,1 %; *Ubx* 336 pb → 56,7 ± 3,3 %; *PP1* 308 pb → 40,0 ± 1,9 % (no significativo). Fragmentos de 132–140 pb dieron 58,9–70,0 %, **y otros del mismo largo no dieron nada**. `[E]` |
| `S21` Kong et al. 2025 | *Bemisia tabaci* MEAM1 (Hemiptera), ninfas de cuarto estadio | tres fragmentos de 100 pb concatenados = 300 pb | nanocarrier SPc, por tres réplicas | tres réplicas | mortalidad de ninfas, emergencia de adultos | El ARNdc de fusión de 300 pb dio ~80 % de mortalidad de ninfas y 70 % de inhibición de la emergencia, con inicio más temprano del silenciamiento. `[E]` |
| `S14` Andrada et al. 2026 | ***Dalbulus maidis*** y *Delphacodes kuscheli* (Hemiptera), ninfas de quinto estadio | *burs-α* **578 pb** y *eth* **544 pb** en *D. maidis*; *burs-α* 326 pb en *D. kuscheli* | microinyección de 0,25 µL a 500 ng/µL = 125 ng por insecto | n = 40 por tratamiento | mRNA por RT-qPCR, supervivencia, fenotipo de muda | Reducción significativa del transcrito y mortalidad alta **con ARNdc de 544 y 578 pb**, es decir más del doble del techo de 250 nt. `[E]` |
| `S09` Mendoza-Alatorre et al. 2025 (revisión) | varias | — | — | — | — | «**No existe consenso** sobre el largo óptimo»: en *L. decemlineata* se silenció con 141, 228, 298, 350, 357, 361, 438, 445, 469, 521, 530, 670 y 1.506 pb; en *D. virgifera*, con 240 y 184 pb; los ARNdc cortos (< 27 nt) rinden menos que los > 60 nt por menor captación en intestino medio y menos siRNA generados. `[E]` |
| `S11` Luo et al. 2026, introducción | varias, por cita | — | — | — | — | Resultados **contrarios** a un techo bajo: en *Drosophila*, 400–540 pb silenciaron *cyclin E* mientras 200–300 pb fueron débiles y 50–100 pb inactivos; el mínimo eficiente en células S2 fue 211 pb; en *Manduca sexta*, 2.222 pb dieron más mortalidad (56,8 %) que 259 pb (47,8 %). Son citas de esa introducción, no trabajos que abrimos. `[R]` |
| `S12` Merkel et al. 2026 | *Acyrthosiphon pisum* (Hemiptera) | ARNdc de 481, 250 y 223 pb | extracto de insecto, ex vivo | no extraído | degradación en gel y fluorescencia | El ARNdc desnudo **ya se degrada a las 2 h** en extracto del áfido, a las 3 h no se detecta el largo completo y a las 5 h la degradación es casi total. El cuello de botella medido es estabilidad, no largo. `[E]` |
| `S13` Zielińska et al. 2026 (revisión de Heteroptera) | Hemiptera | — | — | — | — | La degradación extracelular es la restricción mejor documentada; en *Apolygus lucorum* se midió degradación en fluido del intestino medio y una ARNasa específica; la evidencia causal que liga una nucleasa a la respuesta de ARNi oral existe sólo en *Nezara viridula*. El largo no aparece como la variable limitante. `[E]` |
| `S22` Zhu et al. 2026 | — | > 500 nt | — | — | producción y formulación | Argumento **no biológico** a favor de lo corto: los ARNdc de más de 500 nt comprometen el rendimiento de expresión bacteriana y complican la carga uniforme en nanoacarreadores. `[R]` |
| `S15` Mlotshwa et al. 2020 (corpus) | maíz, vector viral MRFV | insertos de 120 y 231 nt | transcriptos in vitro, inoculación por punción vascular | 35–51 plantas inoculadas por experimento, 3 experimentos | infectividad y silenciamiento de *PDS* | No es largo de ARNdc sino de inserto en un vector: **sólo la unión helicasa/polimerasa toleró insertos**, con 120 y 231 nt; en otra posición el inserto de 120 nt resultó letal para la infectividad. El largo tolerado depende de **dónde** se pega. `[E]` |

### La frase honesta

**El rango 150–250 nt no está respaldado como techo por nada de lo que abrimos, y en nuestra
propia especie blanco hay evidencia publicada en contra**: `S14` silenció *burs-α* y *eth* en
*Dalbulus maidis* con ARNdc de 578 y 544 pb. Lo que sí está respaldado es el **piso**: ~60 pb
(`S02`, `S03`). Lo que está respaldado como tendencia, y sólo en algunas especies, es que pasar
de unos cientos de pares de bases no agrega y puede restar: 200 pb superó a 500 y 1.000 pb en
*Mythimna separata* (`S10`), y hay un argumento de manufactura por encima de 500 nt (`S22`).
Y hay resultados en el sentido inverso: 2.222 pb mejor que 259 pb en *Manduca sexta* y
400–540 pb mejor que 200–300 pb en *Drosophila*, citados por `S11`.

Nuestra lectura, marcada como tal: **150–250 nt es una convención de laboratorio razonable y
compatible con la evidencia, no una conclusión de ella.** Es razonable porque está cómodamente
por encima del piso de 60 pb, porque cae en el rango donde las herramientas del campo ponen
sus valores por defecto —300 nt en dsRNAmax (`S07`)— y porque un fragmento más corto se
sintetiza y se formula mejor (`S22`); y es convención porque la evidencia de que «con largos no
funciona» es específica de especie y de gen, y en Hemiptera convive con éxitos a 326, 481, 544 y
578 pb. `[H]`

Queda una pregunta para el investigador, que es la que cerraría el punto: **si el 150–250 del
laboratorio sale de un ensayo propio con largos comparados en *D. maidis*, ese dato es más
informativo que toda esta tabla**, porque sería el único hecho en el rango exacto, en la especie
exacta y con la vía de entrega que ellos usan.
