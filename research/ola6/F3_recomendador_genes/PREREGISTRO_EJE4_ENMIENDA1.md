# F3 eje 4 — Enmienda 1: «al menos dos de tres TSA», escrita después de ver la primera corrida

**Fecha: 2026-10-27.** Enmienda a `PREREGISTRO_EJE4.md` §3 y §5. El original **no se edita**. Se
commitea **antes** de recalcular con la regla nueva. Decidida por el usuario, que delegó la
elección en esta sesión («la que te parezca más óptima»).

## Lo que se declara primero: esto es una enmienda posterior al resultado

La primera corrida (`resultados/eje4_REPORT.md`, commit `dc8a277`) dio puntaje a **una** de cinco
filas. Esta enmienda se escribe **sabiendo** que `DM-05` y `DM-06` quedaron afuera por estar
ausentes de `GCWP01`, y que `DM-02` quedó a 0,033 del umbral. No es un criterio escrito a ciegas, y
no se presenta como tal. Dos cosas lo acotan:

1. **Se publican las dos reglas lado a lado**, la original y la enmendada, en la misma tabla.
   Quien quiera la lectura estricta la tiene intacta en `eje4_conservacion.tsv`.
2. **La regla nueva sale de dos principios que el preregistro ya contenía**, no de los números:
   §3 paso 2 («separar “con dato” de “sin dato”») y §5.1 («ausencia del gen en un TSA no es
   conservación cero»). La redacción original los violó en su propia aritmética: pedía denominador
   sólo de ventanas evaluables, pero lo calculaba como intersección de **los tres**, así que un TSA
   sin cobertura anulaba el denominador entero. Eso es un defecto de implementación del §3, no una
   elección de método.

## Por qué dos de tres, con lo que el repositorio ya midió

- **`GCWP01` es el ensamblado menos apto para sostener una exigencia de presencia.** Es 454/Newbler,
  el más antiguo de los tres, y `C8` midió que cubre sólo fragmentos de `BicC_Dm` —569 ventanas con
  dato de 2.500— `[M]`. La primera corrida lo confirmó: 404 evaluables en `BicC`, 693 en V-ATPase B,
  cero en `eth` y `burs-alpha`.
- **Que un gen no aparezca en un transcriptoma no dice que no esté en el insecto.** Un TSA recoge lo
  que se expresó en el tejido y el estadio muestreados, y se ensambló con la profundidad que se
  tuvo. `eth` y `burs-alpha` son hormonas peptídicas, y esperar baja representación en un
  transcriptoma de cuerpo entero o de huevos es una hipótesis razonable `[H]`, no un hecho medido
  acá. Por eso la ausencia es «sin dato», no «sin conservación».
- **El control con `C8` ya mostró el costo de leer ausencia como dato.** `C8` declaró `eth` y `bursA`
  «sin transcriptoma suficiente» y esta corrida los encontró en dos de los tres ensamblados: una
  lectura binaria de «hay/no hay en el ensamblado» cambió con la herramienta.

No se cita literatura externa: no se abrió ninguna fuente para esto, y `CLAUDE.md` prohíbe citar lo
que no se abrió. Lo anterior es argumento del repositorio sobre sus propias mediciones.

## La regla enmendada

Para cada candidato y ventana de 21 nt:

1. Una ventana es **evaluable** si tiene dato (cae dentro de los tramos alineados del mejor contig,
   como en §3 paso 2) en **al menos dos de los tres** TSA. La ausencia del gen en un TSA no aporta
   dato ahí, y no suma ni resta.
2. Una ventana es **conservada** si, siendo evaluable, aparece exacta en **todos** los TSA donde
   tiene dato.
3. **fracción = conservadas / evaluables.** Cobertura = evaluables / ventanas totales.
4. **Umbral sin cambios:** menos de **0,50** de cobertura, sin puntaje. Es el mismo número de antes y
   no se ajusta.
5. Se publica además, por fila, **cuántos TSA aportaron dato** (2 o 3), porque una fracción sobre
   dos fuentes es evidencia más débil que sobre tres y el lector debe poder verlo.

**Lo que esta enmienda debilita, dicho con todas las letras:** con dos TSA el eje no distingue una
ventana conservada en tres poblaciones de una conservada en dos. Una ventana presente en dos y sin
dato en la tercera cuenta como conservada. No tapa la diferencia: la columna del punto 5 la expone.

## Consecuencia sobre el orden

Los candidatos con eje 4 pasan a cohorte nueva —«A+4: ejes 1, 2 y 4» o «B+4: ejes 1 y 4», según
tengan o no eje 2— y los pesos de `D87` se renormalizan sobre los ejes presentes (§4.2 del
preregistro original, sin cambios). `orden_genes.tsv` se regenera y el `REPORT` del eje publica el
`diff`. El umbral de empate sigue en 0,05.
