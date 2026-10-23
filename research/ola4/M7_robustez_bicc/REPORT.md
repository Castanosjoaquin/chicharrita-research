# Robustez de la región `BicC_Dm` 922-1221: parámetros y referencia

Fecha: 2026-10-23. Línea **M7** de la ola 4 (issue [#11](https://github.com/Castanosjoaquin/chicharrita-research/issues/11)), plan en [`docs/plan_ola4/PLAN_OLA4.md`](../../../docs/plan_ola4/PLAN_OLA4.md) §5. Contesta dos de los tres ejes que pidió Diego: «antes de considerarla superior a la original, sería importante comprobar la robustez de esa ventaja frente a los parámetros del modelo, la referencia utilizada y los criterios de riesgo» `[R]`. El tercero, criterios de riesgo, depende de la regla de alertas de M6 (#10) y **no se implementó**; §5 dice qué haría falta. Reproducible con los tres scripts de `scripts/`; los números salen de `resultados/`. Marcadores de `CLAUDE.md`.


## El resultado, en un párrafo

**La ventaja de 922-1221 sobre la región del laboratorio es robusta; la ventaja sobre 2121-2420 depende de cómo se cuente, y en el marco que veníamos publicando se da vuelta.** Sobre 4.368 configuraciones —21 brechas de estabilidad por 26 cortes de accesibilidad por dos modos por dos tablas de apilamiento por dos motores de plegado— 922-1221 le gana a **264-563** en el **99,1 %** de ellas contando las ventanas dentro del gen y en el **99,6 %** contando la molécula recortada `[M]`. Contra **2121-2420**, en cambio, le gana sólo en el **36,4 %** de las configuraciones en contexto —en el modo `corregido`, que es el del ranking, en el **15,7 %**— y en el **75,6 %** en el recorte `[M]`. La diferencia entre los dos marcos no es un detalle de contabilidad: al recortar la molécula, 2121-2420 pierde cinco ventanas netas y 264-563 gana dos, todas por cambio de accesibilidad al plegarse sola, de modo que **el marco de conteo decide el resultado tanto como los umbrales** `[M]`. En el eje de referencia, 922-1221 le gana a las dos rivales en las tres fuentes que permiten compararla —el transcriptoma argentino, el de Ohio y el genoma del Reino Unido— y en la cuarta, el de Illinois, **no se la puede evaluar**: no cubre un solo nucleótido de la región `[M]`. Eso obliga a corregir la lectura del criterio que movió la región en D25: el «32 idénticas en los tres transcriptomas contra 22» compara una región que Illinois contradice con una que Illinois no mira, y por fuente separada la conservación de las dos es equivalente `[M]`.

> **Lo que se deduce, en cinco líneas** `[H]`. (1) Contra la región del laboratorio la recomendación aguanta: gana en el 99 % de la grilla y por un margen mediano de 10 a 12 ventanas. (2) Contra 2121-2420 la ventaja es de una ventana en el punto por defecto y no sobrevive a la grilla en contexto; sí sobrevive en el recorte, que es el marco correcto. (3) El eje que más mueve el resultado no es ninguno de los dos que pedía el issue —la tabla de apilamiento casi no mueve nada— sino el **motor de plegado** y el **marco de conteo**. (4) La cifra que se publica tiene que ser **26**, no 36. (5) La razón de conservación con la que se justificó D25 hay que reescribirla: el resultado se sostiene, el argumento del «32 contra 22» no.


## 1. Las anclas, antes de medir

`[M]` Las dos anclas del alcance pasan y están en `resultados/fracciones_parametros.json` (clave `anclas`). El gen completo en el punto por defecto (brecha 1,0, accesibilidad 0,1, u = 8, 22 °C, tabla `RNA_NN3`) reproduce los ocho conteos publicados: 142/39/223/35 en `fiel` y 123/30/171/29 en `corregido` con ViennaRNA 2.7.2, y 133/32/212/42 y 114/25/162/34 con RNAplfold 2.1.5 —las cuatro de `MP_MRFV`, `CP_MRFV`, `BicC_Dm` y `ATPaseD_Dm`—. Las cuatro regiones vigentes en contexto dan 38, 21, 36 y 21. El script aborta si alguna falla, y además verifica que su propia cuenta vectorizada coincida con `apply_rules` del port en dieciocho puntos de la grilla.

`[M]` El motor del si-Fi original corre fuera de Windows: RNAplfold 2.1.5 se compiló desde el tag `v2.1.5` del fuente oficial con la receta de M2 y reproduce los cuatro conteos publicados del `.exe`, que es la prueba de que el binario compilado equivale al del instalador.


## 2. Eje de parámetros

La grilla cruza cinco ejes: los dos umbrales de C9 (brecha de estabilidad de 0,0 a 2,0 en 21 pasos; accesibilidad de 0,05 a 0,30 en 26), los dos modos del port, las dos tablas de apilamiento (`RNA_NN3` del original y `RNA_NN4` de `sifi21INTA`) y los dos motores de plegado. Son 4.368 configuraciones, y cada una se mide en dos marcos. **Los conteos de los dos motores no son comparables entre sí**: cada comparación es entre regiones dentro de una misma configuración, nunca entre motores.

### La tabla única

Fracción de configuraciones en las que 922-1221 tiene más ventanas eficientes que la rival. Fuente: `resultados/fracciones_parametros.json`; la tabla la genera `scripts/tabla_unica.py`.

| Corte de la grilla | Config. | vs 2121-2420 (contexto) | vs 2121-2420 (recorte) | vs 264-563 (contexto) | vs 264-563 (recorte) | a las dos a la vez (recorte) |
|---|---|---|---|---|---|---|
| **en conjunto** | 4368 | 36,4 % | 75,6 % | 99,1 % | 99,6 % | 75,5 % |
| modo `fiel` | 2184 | 57,1 % | 87,6 % | 100,0 % | 100,0 % | 87,6 % |
| modo `corregido` | 2184 | 15,7 % | 63,6 % | 98,2 % | 99,1 % | 63,4 % |
| tabla `RNA_NN3` | 2184 | 36,4 % | 76,8 % | 99,2 % | 99,7 % | 76,7 % |
| tabla `RNA_NN4` | 2184 | 36,3 % | 74,4 % | 99,0 % | 99,5 % | 74,3 % |
| ViennaRNA 2.7.2 | 2184 | 39,6 % | 88,8 % | 98,8 % | 99,1 % | 88,7 % |
| RNAplfold 2.1.5 | 2184 | 33,2 % | 62,3 % | 99,5 % | 100,0 % | 62,3 % |
| brecha 1,0, toda la accesibilidad | 208 | 36,1 % | 74,5 % | 100,0 % | 100,0 % | 74,5 % |
| accesibilidad 0,1, toda la brecha | 168 | 66,1 % | 93,5 % | 100,0 % | 100,0 % | 93,5 % |
| punto por defecto (8 celdas) | 8 | 75,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |
| recorte sin sus dos primeras posiciones | 4368 | — | 74,2 % | — | 99,6 % | 74,2 % |

Margen, en conjunto (ventanas de 922-1221 menos las de la rival; mediana y extremos sobre las 4.368 configuraciones):

| Marco | vs 2121-2420 | vs 264-563 |
|---|---|---|
| contexto | -1,5 (de -10 a +14) | +10,0 (de -1 a +28) |
| recorte | +3,0 (de -6 a +19) | +12,0 (de -5 a +26) |

### Qué dice la tabla

`[M]` **Contra 264-563 la ventaja es robusta y grande.** Pierde en 13 de 4.368 configuraciones en contexto y en 11 en el recorte, todas con la brecha de estabilidad en 1,8 o más —el extremo del eje, donde los dos conteos ya cayeron a cuatro o cinco ventanas— y por una sola ventana en casi todas. El margen mediano es de 10 ventanas en contexto y 12 en el recorte. `[H]` Para la pregunta de Diego —si la región que proponemos es superior a la que eligió el laboratorio— la respuesta no depende de los parámetros.

`[M]` **Contra 2121-2420 la ventaja depende del marco y del motor.** En contexto, con el modo `corregido`, 922-1221 gana en el 15,7 % de la grilla; en el punto por defecto son 36 contra 35, una ventana, y con el motor del si-Fi original esa única ventana se invierte: 30 contra 32 con `RNA_NN3` y 27 contra 31 con `RNA_NN4` `[M]`. En el recorte la fracción sube a 75,6 % y en el punto por defecto gana en las ocho celdas de motor × tabla × modo, por entre 2 y 8 ventanas.

`[M]` **Dónde se cae.** La dependencia es casi toda del corte de accesibilidad. En contexto, con accesibilidad de 0,05 a 0,10, 922-1221 gana en el 68,4 % de las celdas; de 0,20 a 0,25, en el 2,6 %; por encima de 0,25, en ninguna. En el recorte la misma progresión va de 94,4 % a 42,9 %. `[H]` La lectura es que 2121-2420 tiene más ventanas con accesibilidad intermedia-alta y 922-1221 más ventanas que pasan con el corte bajo: al endurecer el filtro de apertura del sitio blanco, la región de C7 conserva más ventanas. El umbral por defecto de si-Fi (0,1) está en el extremo blando de la grilla.

`[M]` **El eje que pedía el issue es el que menos mueve.** Cambiar `RNA_NN3` por `RNA_NN4` mueve la fracción de 36,4 % a 36,3 % en contexto y de 76,8 % a 74,4 % en el recorte, y baja los conteos absolutos en una o dos ventanas por región. El motor, que no estaba en el issue, mueve la fracción del recorte de 88,8 % a 62,3 %. `[H]` Si hay que elegir un eje para declarar en el entregable, es el motor y no la tabla.


## 3. La cifra que se publica: la molécula recortada

`[M]` En el punto por defecto, modo `corregido`, ViennaRNA 2.7.2 y tabla `RNA_NN3`, la región 922-1221 tiene **36** ventanas eficientes contando los 300 arranques que caen dentro de ella en el gen de 2.520 nt, y **26** contando la molécula de 300 nt plegada sola. **Es 26 la que se sintetizaría, y es la que tiene que ir al entregable.** Las dos cifras no se contradicen: de las diez de diferencia, siete son arranques que la molécula no tiene —los últimos veinte del tramo, que en el gen siguen teniendo 21 nt por delante y en la molécula se quedan sin ellos— y tres son ventanas que cambian de veredicto al plegarse sin contexto. La descomposición 36 = 29 + 7 está verificada sobre las mismas ventanas.

| Región | Contexto, 300 arranques | Contexto, los 280 comparables | Molécula recortada | Ventanas que cambian | Por qué cambian |
|---|---|---|---|---|---|
| 922-1221 | 36 | 29 | **26** | 3, todas pierden | 2 por accesibilidad, 1 por estabilidad de extremos (posición 1) |
| 2121-2420 | 35 | 27 | 22 | 7 (6 pierden, 1 gana) | 7 por accesibilidad |
| 264-563 | 20 | 15 | 17 | 6 (4 ganan, 2 pierden) | 6 por accesibilidad |

`[M]` Detalle por ventana en `resultados/recorte_<region>_<modo>_cambios.tsv`, con el término que cruzó el corte y cuánto se movió cada término continuo; el par de 922-1221 reproduce exactamente el `par4` de M2 (29 → 26, tres cambios). **El artefacto de borde que advirtió M2 no explica la ventaja**: de las dieciséis ventanas que cambian en las tres regiones, una sola cae en las dos primeras posiciones del recorte —la posición 1 de 922-1221, que pierde por estabilidad de extremos porque el original calcula ahí los extremos sin nucleótidos colgantes—, y excluir esas dos posiciones de toda la grilla mueve la fracción de 75,6 % a 74,2 % `[M]`. Lo que sí explica el cambio de marco es el **borde de plegado**: quince de las dieciséis cruzan por accesibilidad, y el efecto es asimétrico entre regiones.

`[H]` Esto deja una consecuencia incómoda y hay que decirla: las tres regiones cambian de conteo al recortarse, y **cambian en direcciones distintas**. Un ranking construido sobre conteos en contexto no es el mismo ranking que se obtiene sobre las moléculas que se sintetizarían. M7 mide; cambiar el ranking no es de esta línea.


## 4. Eje de referencia

Se alineó el gen contra cuatro fuentes con blastn local —nada se subió a ningún servicio— y de cada HSP se leyeron las dos secuencias alineadas para reconstruir, posición por posición, cómo escribe el gen cada fuente. Con eso se hicieron dos cosas distintas: **recalcular** la eficiencia sobre la molécula de 300 nt tal como la escribe esa fuente, y contar **coincidencias**, es decir cuántas de las ventanas eficientes de la secuencia de EPILAB existen idénticas ahí. Todo con ViennaRNA 2.7.2, tabla `RNA_NN3` y el punto por defecto.

| Fuente | Región | Cobertura | Eficientes recalculadas (corregido) | Eficientes (EPILAB, contexto) | Idénticas | Variantes | Cruzan empalme | Sin datos |
|---|---|---|---|---|---|---|---|---|
| GHCC01 (Argentina, Pergamino) | 922-1221 | completa | 26 | 36 | 36 | 0 | 0 | 0 |
| GHCC01 | 2121-2420 | completa | 22 | 35 | 35 | 0 | 0 | 0 |
| GHCC01 | 264-563 | completa | 17 | 20 | 20 | 0 | 0 | 0 |
| GITV01 (Ohio State) | 922-1221 | completa | 25 | 36 | 32 | 4 | 0 | 0 |
| GITV01 | 2121-2420 | completa | 19 | 35 | 33 | 2 | 0 | 0 |
| GITV01 | 264-563 | completa | 17 | 20 | 20 | 0 | 0 | 0 |
| GCWP01 (Illinois) | 922-1221 | **nula** | no corrida | 36 | 0 | 0 | 0 | **36** |
| GCWP01 | 2121-2420 | completa | 18 | 35 | 22 | 13 | 0 | 0 |
| GCWP01 | 264-563 | parcial | no corrida | 20 | 5 | 0 | 0 | 15 |
| genoma UK `GCA_975739785.1` | 922-1221 | completa | 26 | 36 | 36 | 0 | 0 | 0 |
| genoma UK | 2121-2420 | completa | 22 | 35 | 27 | 0 | 8 | 0 |
| genoma UK | 264-563 | parcial | no corrida | 20 | 12 | 0 | 8 | 0 |

`[M]` **La eficiencia casi no se mueve al cambiar de referencia, y el orden no se mueve nunca.** Con el transcriptoma argentino los tres conteos recalculados son idénticos a los de EPILAB (26, 22, 17), con el genoma del Reino Unido también (26 y 22; 264-563 no se puede recalcular porque 29 de sus ventanas no tienen datos), y con el de Ohio bajan a 25, 19 y 17. En las tres fuentes 922-1221 queda primera. `[H]` Que la secuencia cambie en tres o siete bases y el conteo se mueva en una o tres ventanas es consistente con lo que ya sabíamos del criterio: es sensible a los umbrales y poco a la identidad exacta de unas pocas bases.

`[M]` **Illinois no mide esta región: no la cubre.** `GCWP01` alinea con el gen en dos tramos —2044-2467 y 249-433— y nada más: cubre 609 de 2.520 posiciones. Las 36 ventanas eficientes de 922-1221 quedan sin datos, 15 de las 20 de 264-563 también, y la única región que esa fuente cubre entera es 2121-2420, donde contradice 13 de las 35. Declararlo como «no corrida» y no como cero es la diferencia entre una medición y un artefacto.

`[M]` **Y eso obliga a corregir la lectura de D25.** El criterio que movió la región decía «32 de 36 idénticas en los tres transcriptomas contra 22 de 35». Medido por fuente separada, el cuadro es otro: en el argentino las dos regiones conservan el 100 % de sus eficientes (36 de 36 y 35 de 35); en el de Ohio, 2121-2420 conserva 33 de 35 (94,3 %) y 922-1221 conserva 32 de 36 (88,9 %), o sea que ahí la región de C7 está **mejor**; y en el de Illinois 922-1221 no tiene una sola ventana con datos. El «32 contra 22» sale de contar la ausencia de datos como ausencia de contradicción: las trece ventanas que Illinois contradice en 2121-2420 descalifican, y las treinta y seis que Illinois no mira en 922-1221 no. `[H]` La decisión D25 **no se cae** —el genoma del Reino Unido sí favorece a 922-1221 (36 de 36 idénticas contra 27 idénticas y 8 que cruzan un empalme), y el ensamblado de Córdoba también, según C8—, pero su argumento principal, tal como está escrito en el ADR y en los entregables, no es sostenible. Hay que reescribirlo con la cobertura declarada.

`[M]` Un dato que aparece sólo con el genoma: **dentro de 922-1221 hay un empalme**. Veinte de sus 300 ventanas no existen como tramo contiguo del genoma —el intrón cae cerca de la posición 1118 del gen— y ninguna de esas veinte es eficiente, así que para el diseño no cambia nada; en 2121-2420 y en 264-563 hay ocho ventanas eficientes cada una que sí cruzan un empalme. `[H]` Para el ARNdc, que se sintetiza sobre el transcrito, esto es irrelevante; para cualquier búsqueda de off-targets contra base genómica, no: es la misma trampa que M1 documentó con `ATPaseD_Dm` en la hebra reversa.

### Lo que este eje no pudo hacer

`[?]` Falta el transcriptoma de *Dalbulus maidis* del laboratorio, que es el pedido 2 del lunes. Las tres fuentes públicas tienen un sesgo común: ninguna es una población de campo del noroeste argentino, y la única argentina (`GHCC01`, CeBio Pergamino) es una colecta de 2015 de huevos y cuerpo entero. Lo que este eje mide es robustez **entre fuentes públicas**, no entre poblaciones. El ensamblado ONT de Córdoba no entra al criterio por D25 y no se remidió acá; sus números siguen siendo los de C8.


## 5. Qué haría falta para cerrar el eje que queda

`[H]` El tercer eje —criterios de riesgo— es el cruce de los dos umbrales de coincidencia de **D28** (21/21 perfecto y bloque perfecto de ≥ 19 nt) con las dos reglas de riesgo de **D17** (la conservadora, que cuenta como riesgosa toda ventana con coincidencia en un no objetivo, y la mecanicista, que sólo cuenta las que además son eficientes). Son cuatro combinaciones, y hoy no se pueden correr por una razón que no es técnica: la regla de alertas de **M6 (#10)** está esperando una decisión del usuario —qué alertas se aceptan con justificación y cuáles siguen siendo bloqueantes— y la reunión del lunes. Correrlo antes significaría elegir nosotros el criterio cuyo efecto queremos medir.

Lo que hace falta, en concreto: (1) la decisión de M6 sobre alertas, que fija qué cuenta como bloqueante; (2) el panel de referencias con el que se evalúa la coincidencia, que ya existe en `C7_ranking_v2/resultados/ranking_v2.json` y no depende de los umbrales de si-Fi; (3) correr las cuatro combinaciones sobre las tres regiones y reportar, con la misma estructura de esta tabla, en qué fracción 922-1221 queda limpia y gana. El insumo (2) está; el (1) no. `[H]` Nuestra expectativa es que este eje sea el más duro para 264-563 y no para 922-1221 —264-563 tiene 22 ventanas con coincidencia perfecta de 21 nt contra el panel de referencias y 922-1221 tiene cero, según la tabla de [`C8_conservacion`](../../ola3/C8_conservacion/REPORT.md) §3—, pero eso es una expectativa y no una medición, y el sentido del eje es justamente que puede salir distinto.


## 6. Límites y confidencialidad

`[H]` Nada de esto es evidencia de eficacia: son conteos de un criterio in silico cuyo valor predictivo el proyecto no pudo establecer ([`M4_evidencia_y_potencia`](../M4_evidencia_y_potencia/REPORT.md)). En este gen, 134 de las 223 ventanas eficientes del modo `fiel` —el 60,1 %— entran por la rama 2 de la regla terminal, que saltea el veredicto termodinámico y decide mirando sólo la accesibilidad ([`M3_features`](../M3_features/REPORT.md) §2), y la tabla de arriba muestra que el corte de accesibilidad es justamente el eje que decide la comparación. `[H]` Una lectura honesta del eje 1 es que **estamos comparando dos regiones con un instrumento que no sabemos leer**, y que el margen de una ventana del punto por defecto nunca fue una diferencia.

`[M]` Las secuencias de EPILAB no salieron de la máquina: las bases BLAST son locales, el motor de plegado corre local y ningún TSV versionado de esta línea lleva columna `seq` —los perfiles por ventana que usó el comparador se escribieron en `/tmp/` y no se versionan—. Los TSV de `resultados/` tienen posiciones, términos y veredictos, no nucleótidos.


## Archivos

| Archivo | Qué es |
|---|---|
| `scripts/grilla_parametros.py` | eje 1: las 4.368 configuraciones, los dos marcos, las anclas y las fracciones |
| `scripts/eje_referencia.py` | eje 2: blastn local contra las cuatro fuentes, recálculo y coincidencias |
| `scripts/recorte_vs_contexto.py` | el par recorte-contra-contexto de las tres regiones, con el término que cruza |
| `scripts/tabla_unica.py` | arma `resultados/tabla_unica.md` desde los dos JSON |
| `resultados/grilla_parametros.tsv` | 13.104 filas: una por configuración y marco, con los tres conteos |
| `resultados/fracciones_parametros.json` | fracciones por eje y en conjunto, anclas y conteos en el punto por defecto |
| `resultados/referencia_por_region.tsv` | por fuente y región: cobertura, coincidencias y recálculo |
| `resultados/referencia_resumen.json` | lo mismo, con el detalle por fuente y el veredicto |
| `resultados/recorte_*_cambios.tsv` | las ventanas que cambian al recortar, con el término que cruzó |
| `resultados/tabla_unica.md` | la tabla única, generada |
