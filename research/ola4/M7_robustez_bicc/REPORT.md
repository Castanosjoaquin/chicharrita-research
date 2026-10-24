# Robustez de la región `BicC_Dm` 922-1221: parámetros, referencia y criterios de riesgo

Fecha: 2026-10-23, ampliado el 2026-10-24 con el tercer eje. Línea **M7** de la ola 4 (issue [#11](https://github.com/Castanosjoaquin/chicharrita-research/issues/11)), plan en [`docs/plan_ola4/PLAN_OLA4.md`](../../../docs/plan_ola4/PLAN_OLA4.md) §5. Contesta los tres ejes que pidió Diego: «antes de considerarla superior a la original, sería importante comprobar la robustez de esa ventaja frente a los parámetros del modelo, la referencia utilizada y los criterios de riesgo» `[R]`. El tercero se contesta **como sensibilidad y no como adopción**: cuál regla de riesgo se adopta lo decide M6 (#10) y el usuario, y §5 mide cuánto depende la comparación de esa elección en vez de hacerla. Reproducible con los cuatro scripts de `scripts/`; los números salen de `resultados/`. Marcadores de `CLAUDE.md`.


## El resultado, en un párrafo

**La ventaja de 922-1221 sobre la región del laboratorio es robusta; la ventaja sobre 2121-2420 depende de cómo se cuente, y en el marco que veníamos publicando se da vuelta.** Sobre 4.368 configuraciones —21 brechas de estabilidad por 26 cortes de accesibilidad por dos modos por dos tablas de apilamiento por dos motores de plegado— 922-1221 le gana a **264-563** en el **99,1 %** de ellas contando las ventanas dentro del gen y en el **99,6 %** contando la molécula recortada `[M]`. Contra **2121-2420**, en cambio, le gana sólo en el **36,4 %** de las configuraciones en contexto —en el modo `corregido`, que es el del ranking, en el **15,7 %**— y en el **75,6 %** en el recorte `[M]`. La diferencia entre los dos marcos no es un detalle de contabilidad: al recortar la molécula, 2121-2420 pierde cinco ventanas netas y 264-563 gana dos, todas por cambio de accesibilidad al plegarse sola, de modo que **el marco de conteo decide el resultado tanto como los umbrales** `[M]`. En el eje de referencia, 922-1221 le gana a las dos rivales en las tres fuentes que permiten compararla —el transcriptoma argentino, el de Ohio y el genoma del Reino Unido— y en la cuarta, el de Illinois, **no se la puede evaluar**: no cubre un solo nucleótido de la región `[M]`. Eso obliga a corregir la lectura del criterio que movió la región en D25: el «32 idénticas en los tres transcriptomas contra 22» compara una región que Illinois contradice con una que Illinois no mira, y por fuente separada la conservación de las dos es equivalente `[M]`. En el tercer eje, el de criterios de riesgo, la elección entre los dos umbrales de D28 y las dos reglas de D17 **no cambia quién gana** —la fracción se mueve de 36,4 % a 35,3 % en contexto y de 75,6 % a 75,9 % en el recorte—, pero sí cambia cuántas alertas hay que justificar, y bajo la regla mecanicista el riesgo de las tres regiones es cero `[M]`.

> **Lo que se deduce, en seis líneas** `[H]`. (1) Contra la región del laboratorio la recomendación aguanta: gana en el 99 % de la grilla y por un margen mediano de 10 a 12 ventanas. (2) Contra 2121-2420 la ventaja es de una ventana en el punto por defecto y no sobrevive a la grilla en contexto; sí sobrevive en el recorte, que es el marco correcto. (3) El eje que más mueve el resultado no es ninguno de los que pedía el issue —ni la tabla de apilamiento ni el criterio de riesgo mueven casi nada— sino el **motor de plegado** y el **marco de conteo**. (4) La cifra que se publica tiene que ser **26**, no 36. (5) La razón de conservación con la que se justificó D25 hay que reescribirla: el resultado se sostiene, el argumento del «32 contra 22» no. (6) Para la reunión: adoptar la regla mecanicista de D17 apagaría el criterio de off-target como separador entre regiones en este gen, porque ninguna ventana con coincidencia es además eficiente.


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

`[M]` **Contra 264-563 la ventaja es robusta y grande.** Pierde en 13 de 4.368 configuraciones en contexto y en 11 en el recorte, y todas ellas están en el extremo del eje de estabilidad: brecha de 1,9 o 2,0 en el marco de contexto y de 1,8 a 2,0 en el recorte, contra un valor por defecto de 1,0. En contexto las trece pierden por exactamente una ventana; en el recorte los márgenes van de una a cinco, y sólo tres de las once son de una. El margen mediano sobre toda la grilla es de 10 ventanas en contexto y 12 en el recorte. `[H]` Para la pregunta de Diego —si la región que proponemos es superior a la que eligió el laboratorio— la respuesta no depende de los parámetros.

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


## 5. Eje de criterios de riesgo: medido como sensibilidad, no adoptado

**Esta sección no elige una regla de riesgo.** Elegirla es de M6 (#10) y la decide el usuario: qué alertas se aceptan con justificación y cuáles siguen siendo bloqueantes. Lo que se mide acá es lo contrario de decidir: **cuánto cambia la comparación entre las tres regiones según cuál de los cuatro criterios se elija**, para que esa decisión se tome con el número a la vista. Son los dos umbrales de **D28** —`perfecto_21`, con bioensayo detrás, y `perfecto_ge19`, convención del campo sin experimento, que nunca se mezclan en un número— por las dos reglas de **D17** —la conservadora, que cuenta como riesgosa toda ventana con coincidencia en un no objetivo, y la mecanicista, que sólo cuenta las que además son eficientes—.

Las coincidencias se recalcularon con `offtarget_21nt.py`, que busca coincidencia exacta con un autómata de Aho-Corasick sobre las referencias en disco, contra el panel de seis de C7 v2 —maíz, *Harmonia axyridis*, *Apis mellifera*, *Homalodisca vitripennis*, *Folsomia candida* y humano—, con *Dalbulus maidis* excluido por ser el blanco. El ancla es que los conteos del gen entero por referencia reproducen los doce de `ranking_v2.json` `[M]`. Los pesos de D18 **no se aplican**: M5 (#9) va a partir ese vector en exposición y conservación, así que ponderar hoy sería fijar lo que esa línea tiene que decidir. En el gen hay 43 ventanas con coincidencia perfecta de 21 nt y 85 con bloque de ≥ 19 nt `[M]`.

| Umbral (D28) | Marco | Config. | 922-1221 gana a 2121-2420 | gana a 264-563 | Alertas, regla conservadora (922 / 2121 / 264) | Alertas, regla mecanicista |
|---|---|---|---|---|---|---|
| `perfecto_21` | contexto | 4368 | 36,4 % | 99,1 % | 0 / 0 / 22 | 0 / 0 / 0 |
| `perfecto_ge19` | contexto | 4368 | 35,3 % | 99,1 % | 3 / 6 / 33 | 0 / 0 / 0 |
| `perfecto_21` | recorte | 4368 | 75,6 % | 99,6 % | 0 / 0 / 22 | 0 / 0 / 0 |
| `perfecto_ge19` | recorte | 4368 | 75,9 % | 99,6 % | 3 / 6 / 33 | 0 / 0 / 0 |

Las columnas de «gana» cuentan ventanas **eficientes y limpias** —eficiente y sin coincidencia—, que es el mismo número bajo las dos reglas de D17: una ventana eficiente con coincidencia es riesgosa para ambas. Lo que la regla cambia es el tamaño del riesgo declarado, que es la columna siguiente. Las alertas están medidas con ViennaRNA 2.7.2, tabla NN3, modo `corregido` y punto por defecto; el conteo de la regla conservadora no depende de la configuración, porque es coincidencia exacta de secuencia.

`[M]` **Control de baja complejidad, que D59 dejó como obligatorio.** La línea de la interfaz midió que las coincidencias perfectas del genoma del MRFV contra tres transcriptomas no objetivo eran, todas, la cola de poli-A del virus, y decidió que cada conteo de off-target se informe en dos cifras —el total y cuánto es baja complejidad— y que las tablas ya corridas se relean con ese descuento. Hecho acá con el criterio de `sifi_plus/complejidad.py`: de las 43 ventanas de `BicC_Dm` con coincidencia perfecta de 21 nt y de las 85 con bloque de ≥ 19 nt, **ninguna** es de baja complejidad, y en las 2.500 ventanas del gen tampoco hay ninguna: el homopolímero más largo mide 7 nt contra un umbral de 10, y la ventana más pobre tiene 3 nucleótidos distintos contra un umbral de 2. Las cifras de esta sección se sostienen sin descuento `[M]`. El criterio de complejidad es nuestro y está pendiente de contrastar contra `dustmasker`, así que la marca viaja como `[H]`.

`[M]` **El criterio de riesgo no cambia quién gana.** Pasar de 21/21 a bloque de ≥ 19 nt mueve la fracción de victorias de 36,4 % a 35,3 % en contexto y de 75,6 % a 75,9 % en el recorte: menos de lo que mueve cualquiera de los otros ejes, y en direcciones opuestas según el marco. La conclusión del eje 1 se sostiene bajo las cuatro combinaciones.

`[M]` **Lo que sí cambia es cuántas alertas hay que justificar, y ahí el umbral importa mucho.** Con 21/21 perfecto, 922-1221 y 2121-2420 empatan en cero y 264-563 tiene 22. Con el bloque de ≥ 19 nt aparecen 3 en 922-1221 y 6 en 2121-2420, y 264-563 sube a 33. Es decir que bajo el umbral más laxo —el que no tiene experimento detrás— la región recomendada pasa a tener estrictamente menos alertas que las dos rivales, y bajo el estricto empata con una de ellas. `[H]` Si el lunes se adopta el umbral de ≥ 19 nt, la recomendación gana un argumento que hoy no tiene; si se adopta el de 21/21, no lo pierde, simplemente no lo tiene.

`[M]` **Y hay un resultado que conviene llevar a la discusión de M6: la regla mecanicista no discrimina.** Bajo esa regla, el riesgo de las tres regiones es **cero** en las ocho celdas del punto por defecto, con una sola excepción de una ventana en 922-1221 con el umbral laxo en modo `fiel`. Ninguna ventana con coincidencia en el panel es, además, eficiente. `[H]` La lectura no es que no haya riesgo: es que, en este gen, adoptar la regla mecanicista equivale a apagar el criterio de off-target como separador entre regiones, y deja la decisión enteramente en manos del conteo de eficiencia, que es justamente el componente cuyo valor predictivo no pudimos establecer. Es el argumento de D17 —no poner la seguridad en el eslabón más débil— apareciendo ahora como número y no como posición.

### Lo que sigue faltando de este eje

`[H]` Lo medido es la sensibilidad, no la regla. Falta lo que M6 tiene que producir y que ninguna medición reemplaza: la tabla de alertas con los cuatro campos que pidió Diego —qué organismo, su posibilidad de exposición, qué gen y qué evidencia biológica—, y la decisión de cuáles se aceptan con justificación. También falta el reparto de pesos de M5, sin el cual el agregado entre referencias es un conteo sin jerarquía: hoy una coincidencia con maíz y una con *Folsomia candida* suman igual, y no deberían.


## 6. Límites y confidencialidad

`[H]` Nada de esto es evidencia de eficacia: son conteos de un criterio in silico cuyo valor predictivo el proyecto no pudo establecer ([`M4_evidencia_y_potencia`](../M4_evidencia_y_potencia/REPORT.md)). En este gen, 134 de las 223 ventanas eficientes del modo `fiel` —el 60,1 %— entran por la rama 2 de la regla terminal, que saltea el veredicto termodinámico y decide mirando sólo la accesibilidad ([`M3_features`](../M3_features/REPORT.md) §2), y la tabla de arriba muestra que el corte de accesibilidad es justamente el eje que decide la comparación. `[H]` Una lectura honesta del eje 1 es que **estamos comparando dos regiones con un instrumento que no sabemos leer**, y que el margen de una ventana del punto por defecto nunca fue una diferencia.

`[M]` Las secuencias de EPILAB no salieron de la máquina: las bases BLAST son locales, el motor de plegado corre local y ningún TSV versionado de esta línea lleva columna `seq` —los perfiles por ventana que usó el comparador se escribieron en `/tmp/` y no se versionan—. Los TSV de `resultados/` tienen posiciones, términos y veredictos, no nucleótidos.


## Archivos

| Archivo | Qué es |
|---|---|
| `scripts/grilla_parametros.py` | eje 1: las 4.368 configuraciones, los dos marcos, las anclas y las fracciones |
| `scripts/eje_referencia.py` | eje 2: blastn local contra las cuatro fuentes, recálculo y coincidencias |
| `scripts/recorte_vs_contexto.py` | el par recorte-contra-contexto de las tres regiones, con el término que cruza |
| `scripts/riesgo_sensibilidad.py` | eje 3: las cuatro combinaciones de D28 × D17 cruzadas con la grilla, sin adoptar ninguna |
| `scripts/tabla_unica.py` | arma `resultados/tabla_unica.md` desde los tres JSON |
| `resultados/grilla_parametros.tsv` | 13.104 filas: una por configuración y marco, con los tres conteos |
| `resultados/fracciones_parametros.json` | fracciones por eje y en conjunto, anclas y conteos en el punto por defecto |
| `resultados/referencia_por_region.tsv` | por fuente y región: cobertura, coincidencias y recálculo |
| `resultados/referencia_resumen.json` | lo mismo, con el detalle por fuente y el veredicto |
| `resultados/recorte_*_cambios.tsv` | las ventanas que cambian al recortar, con el término que cruzó |
| `resultados/riesgo_sensibilidad.tsv` | por configuración, marco y umbral: limpias-eficientes y riesgo bajo las dos reglas |
| `resultados/riesgo_sensibilidad.json` | fracciones por combinación, el ancla del panel y los conteos por defecto |
| `resultados/tabla_unica.md` | las tres tablas, generadas |
