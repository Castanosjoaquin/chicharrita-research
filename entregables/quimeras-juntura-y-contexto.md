# Quimeras: qué se hereda de las partes y qué hay que recalcular

**Qué es esto.** Una quimera es una molécula de ARNdc armada pegando la mejor región de un gen a
la mejor región de otro, para cubrir dos blancos con una sola construcción. Es la técnica que el
investigador describió en el checkpoint 1 y volvió a plantear en el checkpoint 2, y desde `D67` es
criterio de diseño del proyecto: **se arman por combinación de fenotipos que no se solapan**
—reproducción, movilidad, letalidad— y no por densidad de ventanas eficientes.

Este documento contesta la pregunta que él separó en dos y pidió evaluar por separado, y la
contesta con la contabilidad completa. La conclusión cabe en una línea, y conviene leerla antes
que los números:

> **El riesgo de off-target se hereda de las partes. La eficacia no: hay que recalcularla.**

La intuición natural es la contraria, y es la que veníamos usando: *si las dos regiones ya se
validaron, el único lugar donde la quimera puede dar distinto es la unión, donde la ventana toma
una porción de cada gen*. Para el riesgo eso es exactamente cierto y es un resultado útil. Para la
eficacia es falso, y el número que lo desmiente estaba en nuestras propias tablas.

---

## 1. La contabilidad, que conviene escribir una sola vez

Con fragmentos de largo `L_i` y ventanas de 21 nt, la molécula ensamblada tiene `Σ L_i − 20`
ventanas, repartidas así: por cada fragmento, los `L_i − 20` arranques que existen también en su
gen de origen; por cada unión, veinte ventanas nuevas. La cuenta cierra exacto: `Σ (L_i − 20) +
20 (n − 1) = Σ L_i − 20` `[M]`.

`[H]` Dicho de otro modo: **una quimera no agrega ventanas, las canja.** Pierde los veinte
arranques de la cola de cada fragmento —que existían en el blanco— y recibe veinte por unión que
no existen en ninguno. Si el canje conviene o no depende de cuántas de cada lado son eficientes, y
eso se mide.

## 2. Lo que midieron las doce quimeras

Las doce combinaciones ordenadas de las cuatro regiones vigentes, con el port de si-Fi21 sin
modificar, modo `corregido`, ViennaRNA 2.7.2. Fuente: `research/ola5/N4_quimeras/` y
`research/ola3/C13_quimeras_region_recomendada/`.

### Las ventanas de juntura

| De las 240 ventanas de juntura de las doce quimeras | Cuántas |
| --- | ---: |
| Eficientes | **4** |
| Con blanco continuo de 21 nt en alguno de los cuatro genes | 8 |
| **Eficientes y sin blanco continuo** | **4** |

`[M]` **Las cuatro eficientes no tienen blanco continuo.** Un siRNA que se produce y no tiene a
qué unirse de forma continua no silencia nada: ocupa la maquinaria y cuenta en el número. Es la
advertencia del investigador convertida en cifra — *«me puede decir que es el mejor eficiente del
mundo, pero si no va a encontrar su target en la planta o en el insecto, no va a ser»* `[R]`.

`[M]` **Las ocho que sí tienen blanco son todas de los extremos de la unión**, las que toman uno,
dos o tres nucleótidos de un fragmento y el resto del otro: los nucleótidos prestados coinciden
por azar con el flanco que ese fragmento tenía en su propio gen. **Ninguna de las ocho es
eficiente.** `[H]` No es un hallazgo biológico, es aritmética de azar; lo que vale es la
consecuencia metodológica: **«cruza la juntura» y «no tiene blanco» no son sinónimos**, y hay que
medirlo en vez de suponerlo.

### Las ventanas heredadas, que es la mitad que la intuición da por segura

`[M]` La eficiencia de una ventana no depende sólo de sus 21 nucleótidos: depende de la
accesibilidad, y el original no mide la del tramo de 21 sino la del tramo de **8 nt que termina en
el último nucleótido** de la ventana, calculada dentro de una ventana de plegado de 80 nt. Esa
ventana de plegado **cruza la unión**, así que la secuencia del otro gen cambia el veredicto de
ventanas que están enteramente dentro de un fragmento.

`[M]` el número, `[H]` la derivación: el techo es **asimétrico**. La secuencia ajena influye hasta
**72 nt corriente abajo** del final de una ventana y hasta **59 nt corriente arriba** de su
comienzo. La predicción se probó contra las cuatro tablas de ventanas cambiadas que existen: **204
ventanas y ninguna viola el techo** `[M]`.

Cuánto pesa, en las doce quimeras:

| Dónde la quimera difiere de la suma de sus partes | Cuánto |
| --- | ---: |
| Ventanas de juntura eficientes (de 240) | **4** |
| **Ventanas heredadas que cambiaron de veredicto** | **61** |
| de ellas, pierden eficiencia | 31 |
| de ellas, la ganan | 30 |
| Distancia máxima a la unión de una heredada que cambió | 66 nt |

`[M]` Y el remate: con las regiones vigentes, **en diez de las doce quimeras todo el Δ viene de la
banda de contexto y nada del empalme**. El lugar que la intuición señala como el único problemático
aporta 4 cambios; el que da por seguro aporta 61.

> `[H]` Que los 61 casi se cancelen —31 contra 30, y por eso el Δ total de cada quimera quede
> entre −4 y +3— **no autoriza a saltear el recálculo**. Es un resultado de estas cuatro regiones,
> no una propiedad de las quimeras: con un gen nuevo no sabemos cuántas heredadas se van a mover
> ni en qué dirección `[?]`. El atajo «sumo los dos conteos y le agrego las del medio» erra por
> hasta 4 ventanas y con el signo equivocado.

### El tercer lugar, chico y bien localizado

`[M]` Los extremos. Al entrar en una quimera, la cola del fragmento de la izquierda deja de ser el
final de una molécula, y el arranque del de la derecha deja de ser su comienzo. El original calcula
los extremos con nucleótidos colgantes (*dangling ends*) tomando el contexto dos posiciones antes
de la ventana, y en las dos primeras posiciones de una molécula ese contexto no existe. Está acotado
a esas posiciones y se midió una vez: en `BicC_Dm`, la posición 922 del gen —la 1 del recorte— con
la brecha de ΔG pasando de 2,1764 a 0,6287. No es accesibilidad: es `end_stability`, y el techo
asimétrico de arriba no lo cubre.

## 3. El riesgo sí se hereda, y eso tiene una consecuencia práctica

`[M]` El estado de off-target de una ventana depende **sólo de su secuencia**. Toda ventana
heredada es base por base una ventana de su región de origen, así que su veredicto de riesgo es el
mismo que ya se midió. Lo único nuevo son los 40 nt que cruzan cada unión.

La consecuencia es concreta y es una economía real: para tamizar las doce quimeras **no hacen falta
5.760 ventanas, sino 1.160**, y el resultado es idéntico al de tamizar las doce moléculas enteras.
Una pasada en vez de siete `[M]`.

**Pero el empalme no es neutro en riesgo, y es el único lugar del pipeline donde se fabrica
secuencia nueva.** Tres hallazgos de las doce:

- `[M]` En `MP_MRFV` + `ATPaseD_Dm`, el empalme fabrica un bloque perfecto de **19 nt** que
  **existe en tres transcriptos de maíz** (*Zea mays*) y **no existe en ninguno de los dos genes
  de origen**: `MP_MRFV` sola tiene tres aciertos ≥ 19 nt en maíz y ninguno es éste, y `ATPaseD_Dm`
  sola tiene cero. El bloque es 4 nt de un gen y 15 del otro. Los tres transcriptos llevan prefijo
  `XR_`, que en RefSeq es ARN no codificante.
- `[H]` El mecanismo es predecible y da una regla de diseño: a los primeros ~18 nt de la región
  que va a la derecha, si les faltan pocas bases para completar un 19-mero que existe en el
  cultivo, **el socio de la izquierda se las puede dar**. Con otro socio a la izquierda las bases
  son otras y el acierto no aparece.
- `[M]` **Dos de las doce adquieren un veto que ninguna de sus partes tenía** (`BicC_Dm` +
  `MP_MRFV` y `CP_MRFV` + `ATPaseD_Dm`).

`[M]` En las cuatro referencias no objetivo restantes —*Apis mellifera*, *Harmonia axyridis*,
*Homalodisca vitripennis* y *Folsomia candida*— los doce empalmes de las regiones vigentes no
produjeron **ningún** acierto, ni perfecto ni con un desajuste.

## 4. Cómo se presenta una quimera, entonces

`[H]` Tres reglas, y las tres salen de los números de arriba:

1. **Las tres cuentas van separadas y nunca se suman en una sola cifra:** eficientes heredadas
   (con cuántas cambiaron de veredicto y a qué distancia de la unión), eficientes de juntura (y de
   ésas, cuántas tienen blanco continuo), y riesgo del empalme.
2. **La mejor combinación se reporta bajo un objetivo declarado antes de rankear**, no «la mejor»
   a secas. Está medido que por densidad no hay nada que ganar: el empalme aporta 4 eficientes de
   240 —el 1,7 %, contra el 7 a 15 % de las regiones recortadas— y **ninguna de las doce supera a
   su mejor parte en ninguno de los dos ejes del ranking**; una queda por debajo de las dos. El
   «bonus gratis» que habíamos encontrado con las regiones de EPILAB era una propiedad de esas
   regiones —mediocres dentro de su gen— y no de las quimeras `[M]`.
3. **Alerta explícita cuando la juntura crea una coincidencia que ninguno de los dos padres
   tenía.** No es hipotético: ya pasó una vez en maíz.

`[H]` Y el valor de la quimera queda donde `D67` lo puso: **cubrir mecanismos que no se solapan con
una sola molécula.** Eso ataca de frente la tensión que el entregable ya declaraba —`BicC_Dm` tiene
el mejor perfil de riesgo con un fenotipo que no bloquea transmisión, y la V-ATPasa tiene mortalidad
medida por ingesta con peor perfil de off-target—. Si una quimera no le gana a sus partes en conteo,
eso **no la descarta**; lo que la descartaría es el perfil de riesgo de su empalme.

## 5. Los límites que viajan con estos números

- `[?]` **El criterio de «blanco continuo» es la coincidencia exacta de los 21 nt** en una de las
  dos hebras de uno de los cuatro genes. No mide apareamiento parcial ni efecto tipo miARN, que
  podría dar actividad con complementariedad incompleta: eso haría que una ventana de juntura no
  fuera completamente inútil **sino menos útil**, y no lo sabemos. No se lo preguntamos y él no lo
  tocó.
- `[?]` **Las doce uniones son doce, no 240.** Las veinte ventanas de una unión comparten secuencia
  y contexto de plegado, así que la comparación es descriptiva y no una prueba estadística.
- `[M]` **Los empalmes no están tamizados contra el panel humano**, que el ranking v2 agregó como
  séptima referencia y que no está en esta máquina. Queda registrado como pendiente.
- `[H]` **Atribución en el bioensayo:** silenciando dos genes a la vez, si el resultado es negativo
  no se sabe cuál mitad falló. No invalida el diseño —el objetivo es justamente cubrir los dos
  efectos— pero es un argumento para testear las partes por separado primero.
- `[H]` Nada de esto se lee como una vía para ampliar el rango de ningún agente. Por `CLAUDE.md`,
  cualquier resultado que se leyera así queda fuera de alcance: lo que se mide acá es **pérdida** de
  eficacia sobre los blancos propios y riesgo sobre organismos no objetivo.

---

## Dónde está cada número

| Afirmación | Fuente |
| --- | --- |
| Las 240 ventanas de juntura, sus 4 eficientes y sus 8 con blanco | `research/ola5/N4_quimeras/REPORT.md` |
| La contabilidad del canje, verificada en las doce | `research/ola5/N4_quimeras/scripts/junturas.py` |
| Las 61 heredadas cambiadas, con su distancia a la unión | `research/ola3/C13_quimeras_region_recomendada/resultados/quimeras_ventanas_cambiadas_vigentes_corregido_vienna.tsv` |
| El techo asimétrico de 72 y 59 nt, y las 204 ventanas que no lo violan | `research/ola3/C13_quimeras_region_recomendada/REPORT.md` §4 |
| El Δ de las doce y los dos ejes del ranking | `C13` §5 y §7 |
| El bloque de 19 nt en maíz, con sus tres transcriptos | `C13` §6 y `scripts/empalme_maiz_detalle.py` |
| El efecto de `end_stability` en la posición 1 del recorte | `C13` §4, corrección del 2026-10-23 |
| Las alertas de off-target y sus cuatro campos | `research/ola4/M6_alertas/REPORT.md` (D48) |
| El criterio de diseño por fenotipos | `00_meta/DECISIONS.md`, D67 |

Marcadores: `[E]` establecido · `[R]` reportado · `[M]` medido por nosotros · `[H]` hipótesis
nuestra · `[?]` incierto o en conflicto entre fuentes.
