# Pre-registro — validación retrospectiva del puntaje sobre los 28 ARNdc de Cedden 2025

**Estado: escrito el 2026-10-21, antes de calcular ninguna correlación sobre estos datos. No se corrió la validación en la sesión que lo escribió.** Cualquier cambio posterior a este documento se agrega como enmienda fechada debajo de la última sección, sin borrar el texto original.

## Por qué este documento va primero

Con la fiabilidad medida del desenlace, la validación está sub-potenciada, y eso hay que dejarlo escrito antes de ver un solo coeficiente, porque un resultado nulo se interpretará de modo distinto si la decisión de cómo leerlo se tomó después. Los números siguientes vienen de `00_meta/PREGUNTAS_ABIERTAS.md` (cálculo propio del 2026-10-21 sobre `research/ola2/W6_agentes_ciencia/notas/PRB_scripts/prb_potencia.py`) y no se recalcularon aquí: con n = 28, la potencia nominal para rechazar ρ = 0 es 0,32, 0,76 y 0,99 si la correlación verdadera es 0,3, 0,5 y 0,7. Pero dos ARNdc contra el mismo gen correlacionan 0,245 (`pipeline/REPORT.md` §6, según esa fuente), la atenuación es √0,245 = 0,495, una correlación verdadera de 0,7 se observa como 0,35 y la potencia cae a **0,42**; para 80 % harían falta **n = 67**. `[E]` Comparar dos proxies entre sí es inviable: potencia nominal 0,48 (n = 28) y **0,11** con atenuación. `[E]`

## Conclusión que se declara de antemano

**Un resultado nulo no es evidencia de que el puntaje no sirva.** Con este n y esta fiabilidad, una correlación nula o débil es el resultado más probable aun si el puntaje fuera bueno. Este ejercicio **acota** cuánto discrimina el puntaje; no lo valida ni lo refuta, y no se presentará como validación aunque el coeficiente salga alto (ver «Interpretación»).

## Conjunto de datos

Los 28 ARNdc de la Tabla S1 de Cedden 2025 (licencia CC BY), en `research/ola2/W6_agentes_ciencia/notas/PRB_scripts/cedden2025_tablaS1.csv`: 28 filas, 8 genes de *Tribolium castaneum* (3 o 4 ARNdc por gen), 21 de región ORF y 7 de UTR, columnas `gene, sirna, access, region, hr`. Se usan los 28, sin exclusiones. Si alguna fila se excluyera por un motivo no previsto aquí, se declara como enmienda y se reportan ambos resultados.

**Dos vacíos que hay que cerrar antes de calcular, no después.** (a) El significado exacto de `hr` y su dirección (si un valor mayor es más eficaz o menos) debe confirmarse en el texto del artículo y registrarse en una enmienda **antes** de correr nada; el signo del coeficiente se fija entonces y no se elige mirando los datos. `[?]` (b) La tabla no trae las secuencias de los ARNdc. El puntaje de si-Fi21 por ARNdc exige recuperarlas de fuente pública; si no se consiguen, el análisis primario usa solo las columnas de la tabla (ver abajo) y la comparación con si-Fi21 queda como no realizada. `[?]`

## Qué se calcula y qué estadístico

El **análisis primario, único**, es la correlación de rangos de Spearman (ρ) entre el puntaje y `hr` sobre los 28 ARNdc agrupados. Puntaje primario: la fracción de ventanas de 21 nt eficientes de cada ARNdc según si-Fi21 en modo `fiel`, backend `vienna`, 22 °C, umbrales por defecto, si se logran las secuencias; en su defecto, la columna `access` de la tabla. Se fija un solo puntaje primario para no abrir múltiples comparaciones.

Se reportan como **análisis de sensibilidad, rotulados como tales y sin peso para la decisión**: (i) ρ dentro de cada gen y su promedio, porque los ARNdc de un mismo gen no son independientes; (ii) un bootstrap por gen (8 conglomerados) del ρ agrupado; (iii) la misma correlación solo con los 21 ARNdc de ORF.

## Qué se reporta: el intervalo, no el valor p

Se reporta **ρ con su intervalo de confianza del 95 %**, calculado por transformación de Fisher con varianza de Fieller para Spearman (1,06/(n − 3)), junto al IC del bootstrap por gen. **No se reporta ni se usa el valor p** para decidir. Una ρ observada de 0,35 con n = 28 tiene un IC95 de aproximadamente [−0,04, +0,65], que no excluye el cero (misma fuente). `[E]`

## Qué contaría como éxito y qué como fracaso

Se fijan **tres resultados posibles**, definidos sobre el IC95 del análisis primario.

1. **Compatible con utilidad.** El límite inferior del IC95 es mayor que 0. Se reporta como «los datos son compatibles con un puntaje que discrimina»; no se dice que el puntaje está validado.
2. **Fracaso del puntaje, acotado.** El límite superior del IC95 es menor que 0,20: los datos excluyen una correlación observada del orden de la atenuada esperada (0,35). Un límite superior negativo se reporta aparte como señal en dirección contraria. Se avisa desde ahora que este umbral es **casi inalcanzable** con n = 28, porque el IC es del orden de ±0,5; solo ocurriría con una ρ observada claramente negativa.
3. **No concluyente.** Todo lo demás, que es el resultado esperado. Un IC95 que contiene a la vez el 0 y el 0,35 **no distingue** entre «no sirve» y «sirve con ruido». Se reporta como no concluyente, no como nulo informativo.

## Interpretación

Un resultado del tipo 1 con ρ observada alta no se lee como validación: la unidad de análisis es *Tribolium*, un coleóptero, y no hay validación en hemípteros. Un resultado del tipo 3 no se lee como fracaso. Ningún resultado se usa para elegir entre dos proxies. Si el ρ observado es mayor que 0,35, se avisa que supera el techo atenuado esperado y se revisa el cálculo en busca de un error antes de reportarlo.

## Lo que este pre-registro no cubre

No se barre el umbral de decisión ni se construye una curva de precisión y cobertura (opción 5 del plan §3 ter): hereda la misma falta de potencia. No se entrenó ningún modelo con estos 28 datos. Las etiquetas y el evaluador quedan fuera del alcance de cualquier agente que corra el cálculo, y el código se revisa por un humano antes de correrse (hallazgos de W6/AQB en la memoria del proyecto, no reabiertos aquí).

## Enmiendas

(ninguna al 2026-10-21)
