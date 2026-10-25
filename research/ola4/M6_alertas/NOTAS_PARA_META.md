# M6 — lo que va a `00_meta/`, separado por destino

Fecha: 2026-10-25. Fuente de todo lo de acá: [`REPORT.md`](REPORT.md) y `resultados/`.


## Para `DECISIONS.md`

**Enmienda a D48, a redactar con el usuario: la granularidad de la fila es región ×
organismo × gen, y está medida.** D48 pide «una fila por coincidencia» sin decir qué es
una coincidencia. Medido: por ventana × transcripto la tabla tiene **143 filas** sobre
las doce regiones y por región × organismo × gen tiene **17** `[M]`. La diferencia no es
de resolución sino de isoformas: las 3 ventanas de `BicC_Dm` 2121-2420 contra humano caen
en **ocho transcriptos del mismo gen** (`SLC24A4`) y las 3 contra maíz de 264-563 en
**tres variantes de la misma esterasa** (LOC100281777). En el umbral de 21/21 las dos
granularidades casi coinciden —28 filas contra 3— porque todos los aciertos caen en un
único transcripto. Criterio propuesto: la fila es la unidad sobre la que se escribe el
párrafo, y el párrafo es sobre un gen, no sobre una isoforma. La tabla por ventana se
conserva igual en `resultados/alertas_por_ventana.tsv`.

**Entrada nueva: el nivel de alerta de `pipeline/region_scoring.py` contradice a D28, y
la contradicción es grande.** D28 declaró que «no se reportan coincidencias de 16 a 18 nt
como off-targets»; `UMBRAL_OFF_ALERTA = 17` (línea 51) sigue alertando desde 17. Las dos
cifras, medidas sobre `baseline_dsrip/ventanas_multigen.csv`, 23.612 ventanas, que es el
único archivo del repositorio con la columna `off_target_max`: con umbral 17 quedan
**2.338 ventanas en alerta**; con umbral 19, **436** `[M]`. La banda de 17 a 18 nt son
1.902 ventanas, el **81,4 %** de las alertas de hoy, y está íntegramente por debajo del
piso de D28, en el rango donde la propia medición de D28 dice que el azar explica el
total. **M6 no cambió la constante**: tocar ese módulo mueve una cifra publicada que no
es de esta línea. Propuesta: alinear el nivel de alerta con el bloque de ≥ 19 nt y dejar
el descarte donde está. Nada de este informe depende de esa constante: la tabla de
alertas se construye con `offtarget_21nt.py` y los dos criterios de D28.

**Para la consecuencia de D48, que hoy no está escrita: una alerta no leída queda
operativamente igual que una alerta aceptada.** El veto descartaba por omisión y la tabla
no descarta nada, así que el default se invierte y la regla nueva es permisiva cuando
nadie presta atención. Las columnas `decision_usuario` y `justificacion_usuario` salen en
«pendiente», pero **nada en el código impide usar una región cuya fila sigue en
pendiente** `[H]`. Si se adopta D48 conviene que la decisión diga explícitamente quién
firma y en qué momento del proceso, porque eso no lo puede hacer cumplir el software.

**Insumo para la decisión sobre los dos pesos de M5, medido acá.** Las tres regiones que
el veto de hoy descarta —`BicC_Dm` 264-563, `ATPaseD_Dm` 151-450 y 137-436— dejan de
estar vetadas bajo la regla ponderada por exposición **sin que nadie escriba nada**,
porque *H. vitripennis* tiene exposición cero `[M]`. Bajo D48 la alerta no desaparece: la
tabla es ciega al peso y la fila sigue ahí con su exposición declarada en cero. Ésa es la
salida intermedia que M5 dijo que no existía con la regla de riesgo de hoy.


## Para `PREGUNTAS_ABIERTAS.md`

1. **El cuarto campo está completo y no tiene ni un bioensayo.** Las 17 filas de
   `alertas.tsv` pasan la validación y las 17 llevan `evidencia_bioensayo =
   sin_bioensayo_consultado` `[M]`: esta línea no abrió ninguna fuente experimental sobre
   el silenciamiento de esos genes en esos organismos. Falta, en orden de importancia:
   evidencia sobre RNAi en *Homalodisca vitripennis* —que es donde están las tres alertas
   de 21/21 y donde el transcripto impactado es el ortólogo del blanco—, y sobre captación
   de ARNdc en *Zea mays* y en humano para los aciertos de ≥ 19 nt. Mientras eso falte, el
   campo 4 informa identidad y conteos, no evidencia de efecto.
2. **La clase de blanco de D28 no está resuelta para los aciertos genómicos.** Las dos
   filas de `MP_MRFV` contra *D. maidis* caen en el ensamblado genómico (cromosomas 6 y
   X), que no trae anotación de gen: no se puede decir si el acierto está en exón,
   intrón o región intergénica, que es justamente la clasificación que pide D28. Se
   declara como `sin_anotacion_de_gen` y no se inventa un gen. Resolverlo necesita el GFF
   del ensamblado, que no está en `work/W5/ref/`.
3. **Qué valor toma la exposición de *H. vitripennis*** (pedido 4 del lunes). Es la
   decisión que cambia la lectura de las tres filas de 21/21 —señal de conservación o
   riesgo ecológico de primer orden sobre el ortólogo exacto del blanco— y la tabla está
   construida para servir con los dos valores sin recalcularse.
4. **Quién escribe y quién firma las justificaciones.** D48 cambia la carga de la prueba
   pero no dice de quién es la carga. Dos personas pueden justificar la misma fila en
   direcciones opuestas y las dos pasar la validación mecánica.
5. **El criterio de baja complejidad sigue sin contrastarse contra `dustmasker`**, que es
   lo que D59 dejó pendiente. No afecta a esta tabla, donde el descuento es cero.


## Para `CAMINOS_PROBADOS.md`

**Probado y descartado: la fila por ventana × transcripto.** Da 143 filas sobre las doce
regiones y pediría veinticuatro párrafos idénticos para un solo gen humano, porque ocho
de esos transcriptos son isoformas de `SLC24A4` alcanzadas por las mismas tres ventanas.
Se conserva como tabla de respaldo, no como unidad de decisión.

**Probado y descartado: hacer que la cascada siga ordenando bajo la regla de alerta.** La
forma `cascada` de `ranking.py` resta 1.000 a la región vetada, o sea que **es** la
compuerta que D48 retira. Neutralizarla sin tocar el promedio ponderado exigía
desarmar la matriz de riesgo, que es lo que alimenta los números publicados. Se resolvió
al revés: `barrer_exposicion(regla_veto="alerta")` levanta `CompuertaRetirada` si se le
pide la cascada, con el mensaje que explica por qué. Las formas ponderadas siguen
andando y dan lo mismo, que es lo que M5 ya había medido.

**No se tocó `UMBRAL_OFF_ALERTA`.** Ver la nota para `DECISIONS.md`: se midió la
contradicción, se reportó con las dos cifras y se dejó la constante donde estaba.

**No se corrió el tamizaje con `--mm1`.** El tercer criterio no entra en D28 y la tabla de
alertas no lo usa.
