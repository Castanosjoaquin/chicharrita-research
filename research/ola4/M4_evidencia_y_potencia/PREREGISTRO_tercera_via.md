# Pre-registro — el analisis de la tercera via (los terminos continuos de M3)

**Estado: escrito el 2026-10-23, antes de que exista una sola etiqueta nueva y antes de ajustar
ningun modelo sobre la tabla de M3.** Cualquier cambio posterior se agrega como enmienda fechada
al final, sin borrar el texto original. Es la misma convencion que
`research/ola3/C9_sensibilidad_umbral/PREREGISTRO_validacion_retrospectiva.md`, y por la misma
razon: el valor de lo que salga depende de que las decisiones esten tomadas antes.

## Que se preregistra y por que ahora

El investigador propuso «conservar los valores termodinamicos, las preferencias terminales y la
accesibilidad como variables independientes del proceso de clasificacion, para evaluar
posteriormente como contribuyen a la eficiencia» `[R]`. La linea M3 (#7) implementa la primera
mitad: emite la tabla de terminos continuos por ventana, **sin ningun booleano**. La segunda mitad
—evaluar como contribuyen— es un ajuste, y ajustar necesita etiquetas que hoy no existen: hay 29
siRNA con eficacia medida en el mundo publico y la seccion 2 de [`REPORT.md`](REPORT.md) muestra
que con eso no se distingue ni entre dos criterios que difieren en una rama. Con 29 etiquetas y
seis terminos, cualquier modelo que ajustemos va a describir el ruido de Cedden.

Entonces esto no es un analisis: es el plan del analisis, escrito ahora para que cuando aparezcan
etiquetas —del ensayo de la seccion 4 del reporte, de iBeetle-Base si resulta usable, o de un
trabajo de terceros— no se elija el modelo mirando los datos. **Si nunca aparecen etiquetas, este
documento queda sin ejecutar y eso tambien es un resultado reportable.**

## Condicion de disparo: cuando se corre y cuando no

El analisis **no se corre** hasta que se cumplan las tres condiciones, y se declara incumplido con
el numero que falte:

1. **n ≥ 100 siRNA** con eficacia medida en la misma unidad que la tabla de M3 (una ventana de
   21 nt, con su contexto de ARNm para la accesibilidad). El umbral no es convencional: con seis
   terminos, diez etiquetas por termino son el minimo habitual `[E]` y darian 60, y se pide 100
   porque la validacion cruzada por gen necesita que cada grupo retenido tenga tamano razonable.
2. **Al menos 3 genes blanco distintos.** Con un solo gen no se puede separar el efecto del gen
   del efecto de los terminos, y el propio trabajo de Cedden mide que el gen domina el desenlace
   `[R]`.
3. **Las etiquetas provienen de una medicion de silenciamiento o de eficacia, no de una
   prediccion de otra herramienta.** Ajustar contra la salida de otro predictor mide acuerdo
   entre herramientas, no eficacia.

Con menos que eso se publica la tabla de M3 y se dice lo que M3 ya dice: **es la tabla sobre la
que se podria ajustar un modelo, no un modelo.**

## Las variables, congeladas

Las seis columnas de `run_sifi.py --features`, y nada mas:

| Termino | Tipo | Signo esperado, fijado aca |
|---|---|---|
| `dg_sense5` | continuo (kcal/mol) | — |
| `dg_antisense5` | continuo (kcal/mol) | — |
| `ddg` (brecha de extremos) | continuo (kcal/mol) | positivo: mas asimetria, mas carga de la hebra guia `[E]` |
| `accessibility` | continuo (0 a 1) | positivo: sitio mas accesible, mas silenciamiento `[R]` |
| `nt19` es A o T | indicador binario | positivo `[R]` |
| `nt2` es G o C | indicador binario | positivo `[R]` |

**No se agregan terminos despues de ver las etiquetas**: ni interacciones, ni potencias, ni
contenido GC, ni largo, ni nada derivado de la secuencia. `rama_terminal` **no entra** como
variable propia, porque es una funcion de `nt19` y `nt2` y meter las tres cuenta dos veces la misma
informacion; entra solo como variable de estratificacion para describir la muestra. Los signos
esperados quedan fijados arriba para que un coeficiente con el signo contrario se reporte como lo
que seria —una contradiccion con la literatura— y no se narre como un hallazgo.

## El modelo

**Primario, unico.** Regresion lineal con penalizacion L2 (ridge) sobre los seis terminos
estandarizados, con el parametro de penalizacion elegido por validacion cruzada **interna** dentro
de cada pliegue de entrenamiento. Se elige ridge y no seleccion de variables porque la pregunta es
cuanto contribuye cada termino y no cuales sobreviven: un procedimiento que elimina variables da
una respuesta binaria a una pregunta de magnitud, y con n de tres cifras la seleccion es
inestable `[E]`.

**Prohibido de antemano:** ningun procedimiento por pasos (stepwise), ningun ajuste de
hiperparametros mirando el pliegue retenido, ningun cambio de familia de modelo despues de ver el
resultado. Si el desenlace es una proporcion de silenciamiento se modela su transformacion logit,
declarada aca; si trae ceros o unos exactos se usa la transformacion con media empirica
(`(y·(n−1)+0,5)/n`), tambien declarada aca.

**Desenlace.** El silenciamiento del transcrito como reduccion porcentual respecto del control
negativo, si las etiquetas vienen del ensayo de la seccion 4. Si vienen de un desenlace de
supervivencia, el desenlace es el logaritmo de la razon de riesgo y se declara como tal, con la
atenuacion que eso implica.

## La validacion cruzada

**Dejar un gen afuera** (leave-one-group-out, agrupando por gen blanco). Es la unica forma de no
confundir el efecto del gen con el de los terminos, y esta decidido antes de ver nada. Si hubiera
mas de 15 genes se pasa a 5 pliegues por grupo de genes, por costo; el criterio es el numero de
genes y no el resultado.

**Metrica primaria:** rho de Spearman entre predicho y observado, calculado **una sola vez sobre
el conjunto de las predicciones retenidas** de todos los pliegues, no como promedio de rho por
pliegue. Se reporta con intervalo de confianza del 95 % por bootstrap **de genes**, que es la
unidad de agrupamiento. **No se reporta valor p de la metrica primaria.**

## La medida de contribucion, declarada

Para cada uno de los seis terminos: **la caida de la metrica primaria al quitarlo** (dejar uno
afuera, reajustando el modelo completo dentro de cada pliegue), con intervalo por el mismo
bootstrap de genes. Es una medida de contribucion fuera de muestra, que es lo que la pregunta
pide; los coeficientes se reportan al lado, estandarizados y con su signo, pero **no son la medida
de contribucion**, porque con terminos correlacionados —y `ddg` con los dos `dg` lo estan por
construccion— el coeficiente individual no se puede leer solo.

Se reporta ademas, como descriptivo y no como inferencia, la matriz de correlacion entre los seis
terminos, para que se vea cuanta informacion comparten.

## La comparacion con los dos booleanos, que es el punto

Los tres modelos —fiel, corregido y continuo— se comparan **con la misma validacion cruzada y la
misma metrica**, y la comparacion entre dos de ellos usa la prueba de aleatorizacion por
intercambio de `scripts/potencia_dos_modelos.py`, que es la que corresponde a dos predictores
evaluados sobre las mismas ventanas. La cota de la seccion 1 del reporte vale igual aca: si los
dos modelos comparados discrepan en menos de 6 casos, la prueba no puede rechazar y se reporta eso
en vez de un p.

**Regla de decision, fijada ahora.** El modelo continuo se reporta como mejor **solo si** su rho de
validacion cruzada supera al del mejor booleano por **0,10 o mas** y la prueba de aleatorizacion da
p ≤ 0,05. Si supera por menos, se reporta como **«no distinguible del booleano»**, aunque el numero
sea mas alto. Si no supera, se reporta que el booleano no pierde nada y que la tercera via no
mejora la prediccion, que es un resultado tan publicable como el otro y contradiria nuestra propia
hipotesis de T5 sobre que el `and` tira informacion.

## Que resultado falsa que

- **Si la contribucion de `accessibility` es nula y la de `ddg` no**, la critica de T5 queda
  reforzada con una medicion y no con un argumento: el termino que si-Fi21 usa como filtro
  booleano con umbral fijo no aporta fuera de muestra.
- **Si la contribucion de los dos indicadores terminales es nula**, la discusion entre modo fiel y
  corregido pierde importancia practica: estariamos discutiendo una rama que no predice nada.
- **Si el modelo continuo no supera a los booleanos**, la propuesta de reemplazar el `and` por un
  puntaje graduado se queda sin apoyo empirico y hay que decirlo.

## Lo que este pre-registro no cubre

No cubre la seleccion de candidatos del ranking, que se decide por otros criterios (D25, C7). No
cubre off-targets ni limpieza, que son hechos de alineamiento y no predicciones. No autoriza a
usar las etiquetas humanas de la seccion 3 del reporte para el ajuste: con ese cambio de reino, de
maquinaria y de via de entrega, un modelo ajustado ahi no se transfiere a un hemiptero, y si
alguna vez se corre sera como ejercicio rotulado `[?]` y con esta misma validacion cruzada, nunca
como el modelo del entregable.

## Enmiendas

*(ninguna todavia)*
