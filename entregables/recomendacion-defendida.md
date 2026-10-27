# La recomendación, defendida: qué proponemos, por qué, y qué la haría caer

Fecha: 2026-10-25. Línea **N6** de la ola 5. Contesta el pedido final de la carta del investigador
del 25 de octubre de 2026: «me interesa que puedan defender una recomendación biológica y
explicitar sus principales incertidumbres, no solamente elegir la región que tenga más ventanas
predichas como eficientes» `[R]`. Marcadores de `CLAUDE.md`.

---

## 1. La recomendación, en tres frases

Sobre el eje del vector recomendamos **`BicC_Dm` 922-1221**, una molécula de ARN de doble cadena
(double-stranded RNA, dsRNA) de 300 nt con **26** ventanas de 21 nt que pasan el criterio de
eficiencia contando la molécula que se sintetizaría `[M]`. La recomendamos **para reducir la
población del vector entre generaciones, no para cortar la transmisión de la temporada en curso**,
y esa distinción es la parte biológica de la propuesta, no una salvedad: el fenotipo publicado del
gen es de oviposición y ovario, no de mortalidad rápida. Y la recomendamos **condicionada a una
pregunta que no es nuestra**: si el objetivo de la intervención es cortar transmisión dentro de la
temporada, el blanco no debería ser éste.

## 2. El blanco y el mecanismo esperado

`BicC` es el homólogo de *bicaudal C*. En *Dalbulus maidis* el silenciamiento del gen afectó la
oviposición y produjo un fenotipo ovárico; es la única evidencia de fenotipo que tenemos para este
gen y **la tenemos sólo desde el resumen**, porque el texto completo de Dalaison-Fuentes 2022 no es
de acceso abierto `[R]`. El mecanismo esperado, entonces, es una caída en la postura de las
hembras tratadas, que se traduce en menos individuos en la generación siguiente `[H]`.

Lo que ese mecanismo **no** hace es impedir que una hembra ya infectiva transmita. Si el ARNdc se
aplica sobre adultos que ya adquirieron el patógeno, el efecto sobre la transmisión de esos
individuos es nulo por construcción del mecanismo `[H]`.

**Agregado el 2026-10-26, después del checkpoint 2.** Esa limitación tiene ahora una vía declarada,
y no es cambiar de gen: el investigador propuso armar **quimeras que combinen fenotipos que no se
solapan** —reproducción, movilidad, letalidad— y los tres ejes ya tienen candidato en *D. maidis*
en nuestro propio catálogo `[M]`, así que la combinación que cubre lo que a `BicC` le falta es
armable con lo que hay (`D67`). La contabilidad de cómo se evalúa una quimera —qué se hereda de las
partes y qué hay que recalcular, con la advertencia de la juntura que él señaló como el diferencial
posible— está en [`quimeras-juntura-y-contexto.md`](quimeras-juntura-y-contexto.md). **Nada de esto
cambia la recomendación de este documento**, que es sobre una región de un gen; abre la línea que
la complementa.

## 3. El argumento que decide, y no es el conteo

La comparación que manda para nuestro objetivo no está en el diseño: está entre **el tiempo hasta
el efecto** y **la ventana de latencia del patógeno**. Si el insecto transmite antes de que el
silenciamiento haga efecto, matarlo no corta la transmisión.

Y ahí tenemos una asimetría incómoda y declarada: la ventana de latencia es de unos **20 días**
—cifra del investigador, aceptada en el checkpoint 1 (D34) `[R]`— y todos los ensayos abiertos en
la especie miden el desenlace a los **4 o 5 días** `[R]`. La única fuente abierta de latencia que
pudimos abrir (Jones y Medina 2020) da 18 a 22 días para *Spiroplasma kunkelii*, **no** para el
virus del rayado fino del maíz (maize rayado fino virus, MRFV) `[?]`, y no hay seguimientos
publicados más largos que cinco días que digan si el efecto dura.

Por qué entonces `BicC_Dm` y no los otros candidatos, con lo que cada uno tiene a favor y en
contra:

**La V-ATPasa (`ATPaseD_Dm`) es el único con evidencia por la vía que se quiere usar.** Por dieta,
la supervivencia a cuatro días fue de ~18 % contra ~37 % del control de GFP `[R]`: es mortalidad y
es por ingesta, que es la vía de una aplicación de campo. En contra tiene dos cosas medidas por
nosotros: su región vigente 72-371 tiene **7 ventanas con bloque perfecto de 19 nt o más contra
humano frente a las 2,4 esperadas por azar** `[H]`, compatible con que la subunidad D esté
conservada, y las dos regiones más conservadas del gen —151-450 y 137-436— son dos de las tres
únicas regiones del panel con coincidencia **perfecta de 21 nt** contra *Homalodisca vitripennis*,
donde además el transcripto impactado es el ortólogo del mismo gen que se quiere silenciar `[M]`.
Es el candidato con mejor evidencia de fenotipo y peor perfil de off-target.

**`eth` y `burs-alpha` tienen el knockdown más fuerte y la vía equivocada.** Knockdown de ~90 % y
~95 %, con la supervivencia cayendo al 10 % al día 4 en `burs-alpha`, n = 40, pero **por
microinyección en ninfas de quinto estadio** `[R]`. Y acá hay una tensión que vale más que cada
pieza por separado: las ninfas ya transmiten y el tercer estadio fue el más sensible al RNAi en un
cicadélido emparentado `[R]`, pero el bioensayo estándar de dieta en sobre de parafilm **no sirve
para ninfas, porque la dieta ya las mata** `[R]`. Si el estadio más sensible es el que no se puede
tratar por la vía que se quiere usar, la comparación entre candidatos cambia `[H]`.

**Los blancos virales (`MP_MRFV`, `CP_MRFV`) juegan otro partido.** Actúan sobre el patógeno y no
sobre el vector, y por **D38** el proyecto presenta las dos listas sin compararlas entre sí: el
número de ventanas eficientes no compara estrategias dirigidas a genes distintos, y menos a
organismos distintos ([`M8`](../research/ola4/M8_que_compara_el_conteo/REPORT.md)).

`[H]` **La defensa de `BicC_Dm`, entonces, es ésta:** de los candidatos del vector es el que tiene
un fenotipo publicado en la especie, una región con perfil de off-target limpio en el panel
completo —cero coincidencias perfectas de 21 nt— y la mejor conservación entre las fuentes que
cubren la región. No es el que tiene más ventanas eficientes: por densidad el gen cae del primer
al tercer puesto `[M]`. Y no es el que tiene la evidencia de fenotipo más fuerte: ése es
`burs-alpha`, por una vía que no se puede usar. Es el que mejor aguanta los tres ejes a la vez, y
el eje en el que gana —el de riesgo— es el único de los tres que no es una predicción.

## 4. La región, con su marco y su riesgo

`[M]` Todo en el punto por defecto, modo `corregido`, ViennaRNA 2.7.2, tabla `RNA_NN3`.

| | `BicC_Dm` 922-1221 |
|---|---|
| ventanas eficientes, con su marco (`D63`) | **26** en el marco 3, la molécula de 300 nt recortada y plegada sola: es la cifra que se publica (`D79`). Al lado, **36** en el marco 1 (contexto, todos los arranques) y **29** en el marco 2 (contexto, los comparables), que es el que contesta cuán accesible es el sitio en el transcrito blanco. Los tres valen y no se mezclan `[M]` |
| coincidencias perfectas de 21 nt contra el panel de seis no objetivo | **0** |
| alertas por bloque de ≥ 19 nt | 3 (contra 6 de 2121-2420 y 33 de 264-563) |
| ventanas de baja complejidad | 0 de las 2.500 del gen: el homopolímero más largo mide 7 nt |
| conservación | 36 de 36 idénticas en el transcriptoma argentino y en el genoma del Reino Unido; 32 de 36 en el de Ohio; sin datos en el de Illinois |
| robustez contra la región del laboratorio | gana en el 99,1 % de 4.368 configuraciones en contexto y en el 99,6 % en la molécula |
| robustez contra C7 (2121-2420) | gana en el 36,4 % en contexto y en el 75,6 % en la molécula |
| al recortarse | pierde 3 ventanas y gana 0: la única de las seis regiones medidas que no gana ninguna |

El panel de seis no objetivo es maíz, *Harmonia axyridis*, *Apis mellifera*, *Homalodisca
vitripennis*, *Folsomia candida* y humano, con *Dalbulus maidis* excluido por ser el blanco.

## 5. Las tres incertidumbres principales, cada una con su número

**Primera: el valor predictivo del criterio de eficiencia no está establecido, y no lo podemos
establecer con datos abiertos.** Con los 29 siRNA de la única serie etiquetada que encontramos, la
comparación entre los dos modelos de la regla terminal **no podía salir distinta**: hay un solo
caso discordante y el p exacto es 1,00; replicando ese diseño harían falta **2.784** siRNA, y 232
es el piso optimista `[M]`. La correlación entre el filtro y la eficacia medida da ρ = +0,142, IC
95 % [−0,247, +0,492], n = 29, en *Tribolium castaneum*: no concluyente `[M]`. Y en este gen, 134
de las 223 ventanas eficientes del modo `fiel` —el 60,1 %— entran por una rama de la regla
terminal que saltea el veredicto termodinámico y decide mirando sólo la accesibilidad `[M]`. **Una
ventana que pasa el filtro no demuestra silenciamiento.**

**Segunda: el marco de conteo decide tanto como los umbrales.** La ventaja de 922-1221 sobre C7 se
da vuelta según el marco: gana en el 36,4 % de las 4.368 configuraciones contando dentro del gen y
en el 75,6 % contando la molécula `[M]`. El margen en el punto por defecto es de una ventana en
contexto y de cuatro en la molécula. Contra la región del laboratorio, en cambio, la ventaja no
depende de nada: 99,1 % y 99,6 %, con margen mediano de 10 a 12 ventanas `[M]`. `[H]` La
recomendación que sostenemos con firmeza es «no 264-563»; la de «922-1221 antes que 2121-2420» es
más débil y la presentamos como tal.

**Tercera: la exposición de los organismos no objetivo es una decisión nuestra, declarada abierta, y tiene
palanca.** *Actualizado el 2026-10-27 (issue #20, `D66`, `D80`).* No le pedimos al investigador un número
y no lo fijamos nosotros. Preguntado dos veces qué exposición asignarle a un cicadélido norteamericano
en un lote argentino, contestó que el organismo *«no está en Argentina, o sea que puede no importar»* y
también que *«puede venir eventualmente y tal vez si la querés matar»*, y que lo útil es mostrar que
esas decisiones están presentes `[R]`. Lo que mostramos es el resultado en los dos extremos, uno al lado
del otro:

| | exposición de *H. vitripennis* **distinta de cero** (cualquier valor de 0,05 a 1,00) | exposición **exactamente cero** |
|---|---|---|
| `BicC_Dm` 264-563 (la de EPILAB) | con veto: 22 ventanas idénticas de 21 nt | sin veto: pasan a ser señal de conservación |
| `ATPaseD_Dm` 151-450 (la de EPILAB) | con veto: 3 ventanas | sin veto |
| región que elige la cascada para `BicC_Dm` | 2121-2420 | **922-1221** |
| región que elige la cascada para `ATPaseD_Dm` | 72-371 | **137-436** (24 ventanas eficientes contra 18) |
| región que elige la cascada para `eth_Dm` | 114-313 | **194-393** |
| `CP_MRFV` antes que `ATPaseD_Dm`, en la cascada (2.000 sorteos) | **100 %** | **0 %** |
| orden de los seis en la cascada | `MP_MRFV` > `eth` > `CP_MRFV` > `burs-α` > `BicC_Dm` > `ATPaseD_Dm` | `MP_MRFV` > `BicC_Dm` > `ATPaseD_Dm` > `eth` > `CP_MRFV` > `burs-α` |

`[M]` Fuente: `research/ola4/M5_dos_ejes/resultados/` (`regiones_recomendadas_por_reparto.tsv`,
`vetos_por_reparto.tsv`, `tabla_afirmaciones.tsv`), cifras leídas de los archivos versionados. **Tres de
las seis regiones recomendadas se mudan**, y una de ellas es `ATPaseD_Dm` 137-436, la región más
conservada del gen, que `D25` había descartado justamente por estar vetada. El efecto **no es gradual**:
entre 0,05 y 1,00 de peso relativo al maíz no cambia nada, porque el veto es binario, y todo el cambio
está en el cero exacto. `[H]` Por eso la respuesta a si los pesos importan es «casi nunca, salvo el
cero», y por eso el tercer puesto se reporta como **empate declarado** (`D80`): lo que separa los dos
órdenes no es un candidato mejor que otro sino una decisión que no es nuestra tomar por la ventana. En
las formas ponderadas el mismo par casi no se mueve (99,9 % de los sorteos con exposición cero), y cuál de
las dos formas se publica como la lista ordenada sigue siendo una decisión abierta anterior a esto.

Lo que **no** cambia con la exposición es la recomendación de este documento: para `BicC_Dm`
recomendamos 922-1221 por conservación entre fuentes y por su perfil de off-target (`D25`, `D64`), y con
exposición cero la cascada llega sola al mismo lugar, así que dos criterios independientes coinciden. Lo
que sí cambia son tres afirmaciones que publicamos y que **dejarían de sostenerse** con exposición cero, y
que por eso llevan su condición al lado: que las dos regiones de EPILAB quedan vetadas
(`checkpoint2-una-pagina.md`, casilla 4), que la región vigente de `ATPaseD_Dm` se mantiene
(`para-el-investigador.md`, parte A, pedido 4) y el desempate del tercer puesto entre `ATPaseD_Dm` y
`CP_MRFV`. `[H]` La apuesta es que *H. vitripennis*, plaga cuarentenaria ausente de la Argentina, siga
ausente: si cambia su estatus, la revisión es leer esta tabla y no recalcular. Y queda declarado lo que
no pudimos medir: la sensibilidad del reparto a 22 nt **no está corrida**, y el eje de exposición no tiene
ningún cicadélido nativo argentino contra el cual medirse `[?]`.

**Y una cuarta, que es nueva de esta semana.** Las cifras históricas de la planilla pasaron por una
función de conteo que esconde entre el 5,7 % y el 17,4 % de las ventanas eficientes según el gen
`[M]`. El sesgo no es constante, así que **dos cifras de la planilla no son comparables entre sí**,
y cualquier comparación nuestra contra ellas tiene que aplicar la misma transformación o declarar
que no la aplica.

## 6. Qué haría caer esta recomendación

`[H]` Tres resultados la refutarían, y los tres son experimentos, no cálculos:

1. **Un bioensayo de dieta con oviposición medida más allá de la ventana de latencia.** Si el ARNdc
   de `BicC` por ingesta no reduce la postura, o la reduce sólo después de los 20 días en los que
   el insecto ya transmitió, la recomendación pierde su mecanismo. Es el experimento que más
   necesitamos y el que no podemos hacer.
2. **El ensayo prospectivo de 32 siRNA por brazo** que diseñó `M4`: discrimina los dos modelos de
   la regla terminal y, con eso, dice si el criterio con el que elegimos la región separa señal de
   ruido. Si no la separa, el «26 contra 17» deja de ser un argumento.
3. **Un conteo de la región en el marco que use el laboratorio.** Si la planilla cuenta en contexto
   y con la función histórica, nuestro 26 y su cifra no son el mismo número, y la comparación hay
   que rehacerla antes de defender nada.

## 7. Lo que pedimos para cerrarla

Tres cosas, y ninguna es un archivo con secuencias (la tercera dejó de ser un pedido):

1. **Qué objetivo manda**: cortar transmisión en la temporada o reducir la población entre
   generaciones. Decide el eje y, con él, el blanco.
2. **El dato de latencia del MRFV**, que hoy tenemos sólo para *Spiroplasma kunkelii* y de una
   fuente que no es la del patógeno que nos importa `[?]`.
3. ~~**La exposición que le asignan a *Homalodisca vitripennis***, que es el único peso con palanca
   en todo el ranking.~~ **Ya no se pide** (`D66`, `D80`): es una decisión nuestra, declarada abierta, y
   el resultado en los dos extremos está en §5. Si el laboratorio tiene una práctica propia con
   cicadélidos no objetivo, nos sirve, pero no la esperamos.
4. **El marco y la función de conteo de la planilla**, para saber si nuestras cifras y las suyas
   son el mismo número.
