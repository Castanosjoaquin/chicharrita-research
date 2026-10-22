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

**Enmienda 2 (2026-10-21, escrita y commiteada ANTES de calcular ninguna asociación entre predictor y desenlace).** Decisión del equipo: el conjunto primario pasa a ser otro, y el original queda como confirmatorio. Ambos quedan fijados acá, antes de mirar resultados.

*Motivo del cambio.* Revisando el material suplementario apareció un segundo conjunto en el mismo trabajo, estrictamente mejor para esta pregunta en tres aspectos verificados: (a) el empalme entre secuencia y desenlace es por **nombre**, y cierra **31 de 31**, contra el empalme por orden del conjunto de 28, que no tiene clave publicada y quedó marcado `[?]`; (b) la unidad es un siRNA de **21 nt**, que es exactamente la unidad del booleano de si-Fi21, mientras que un ARNdc de ~300 pb obliga a agregar ventanas; (c) los 31 apuntan a **un solo gen** (TC006679, *Tc-gawky*), de modo que desaparece el confusor del gen que en el conjunto de 28 domina la razón de riesgo, y con él la decisión pendiente entre correlación agrupada y dentro de cada gen. `[E]`

*Conjunto primario.* Los **31 siRNA** de la hoja `Fig 1 log-rank` del archivo adicional 2, unidos por nombre a sus secuencias de 21 nt de la hoja `Primer list 1` del archivo adicional 1. Los nombres codifican la posición en el transcrito (`si2730` está en 2730), lo que permite calcular la accesibilidad **en contexto del ARNm completo**, que es como si-Fi21 la define; con un siRNA suelto no sería posible. Requiere bajar el transcrito de `TC006679`, y la posición de cada siRNA se verificará localizando su secuencia en el transcrito antes de usarla: si alguna no cae donde dice el nombre, se reporta y se excluye.

*Predictor primario.* El booleano `is_efficient` de si-Fi21 para la ventana de 21 nt en esa posición, en **modo fiel**, backend `vienna`, 22 °C, `u = 8` y los umbrales por defecto (brecha de extremos 1,00 kcal/mol, accesibilidad 0,1). Es el que usa el entregable; no se lo reemplaza por ninguna variante continua.

*Estadístico primario.* ρ de Spearman entre ese booleano y la razón de riesgo, con **intervalo de confianza del 95 %**, que con un predictor binario equivale a una comparación de rangos entre los dos grupos. No se usa el valor p para decidir. Análisis de sensibilidad declarados, rotulados como tales: (i) el conteo ordinal de condiciones satisfechas (0 a 3) en lugar del booleano; (ii) el modo corregido además del fiel.

*Criterios, con el mismo esquema que el texto original.* Compatible con utilidad si el límite inferior del IC95 es mayor que 0. Fracaso acotado si el límite superior es menor que 0,20. No concluyente en todo lo demás, que sigue siendo el resultado más probable: con n = 31 y la atenuación por fiabilidad del desenlace la potencia es del mismo orden que la calculada para n = 28. **Un nulo no refuta el puntaje.**

*Curva precisión-recall.* Se reporta como salida de este análisis, no como línea aparte. Binarización del desenlace **declarada ahora**: es positivo el siRNA cuyo IC95 de la razón de riesgo **excluye el 1**, es decir el que mata significativamente más que el control dsmGFP; como sensibilidad, la mediana de la razón de riesgo. El umbral que se barre es el de accesibilidad, con el mismo rango de C9.

*Conjunto confirmatorio.* Los **28 ARNdc** tal como los fija el texto original y la enmienda 1, con su empalme por orden declarado `[?]`. Se corre y se reporta aunque el primario ya haya dado un resultado, y no se elige entre los dos según cuál quede mejor.

*Límite que no se puede sortear.* Los autores ya publicaron análisis de **sus propios** descriptores sobre estos mismos 31 siRNA —asimetría termodinámica, ausencia de estructura secundaria y adenina en la posición 10 como los más predictivos—, y dos de esos tres se solapan conceptualmente con las condiciones de si-Fi21. Nuestra prueba **no es independiente** de lo ya publicado sobre este dato, y se reporta como lo que es: un contraste de nuestro filtro contra un desenlace ya analizado por otros, no un descubrimiento. `[R]`

**Enmienda 1 (2026-10-21, posterior al texto de arriba y anterior a cualquier correlación).** Se abrió el artículo y sus dos archivos adicionales; no se calculó ninguna correlación entre puntaje y `hr`. Cierra los dos vacíos marcados `[?]`.

(a) **Qué es `hr` y en qué dirección.** Es la razón de riesgo de mortalidad del grupo tratado con el ARNdc frente al control con dsmGFP, calculada por el método de log-rank sobre larvas de *Tribolium castaneum* inyectadas; un valor mayor que 1 indica más mortalidad, es decir más eficacia (Cedden *et al.* 2025, BMC Biology 23:114, sección de Métodos). `[R]` **El signo esperado de ρ es positivo**, y queda fijado aquí. Además, las columnas `sirna` y `access` de la Tabla S1 son los puntajes de la plataforma dsRIP de los autores y no de si-Fi21.

(b) **Las secuencias existen.** Están en el archivo adicional 1 (hoja `Primer list 2`), bajado de Europe PMC (PMC12039203). Se unieron a los 28 `hr` por orden dentro de cada gen, con comprobaciones internas de consistencia (20 de 20) pero sin clave publicada; la unión es `[?]`. Detalle y tabla en `datos/LEEME.md` y `datos/cedden2025_28dsrna_con_secuencia.csv`. **Consecuencia sobre el puntaje primario:** ya no hace falta el plan de reserva. El puntaje primario es la fracción de ventanas de 21 nt eficientes de cada ARNdc según si-Fi21, modo `fiel`, backend `vienna`, 22 °C y umbrales por defecto. **Se retira la columna `access` como reserva**, porque es el puntaje de accesibilidad de dsRIP y la propia regresión de los autores no le encuentra efecto (P = 0,41), así que usarla probaría algo que ya se sabe.

(c) **Dos advertencias de diseño que cambian cómo se lee el resultado, escritas antes de verlo.** Primero, los 28 ARNdc no son una muestra al azar: los autores los eligieron por su puntaje (alto, bajo, mejor accesibilidad, UTR), lo que fabrica un contraste en el puntaje. Segundo, el gen blanco domina `hr` en su propia regresión (efecto del gen P = 0,047, de la región ORF P = 0,011, R² ajustado 0,40), de modo que la correlación agrupada mezcla el efecto del gen con el del puntaje. Ninguna de las dos cosas invalida el ejercicio, pero **un ρ agrupado alto no se puede atribuir al puntaje**.

**Pendiente de decisión del equipo, antes de calcular:** si el análisis primario sigue siendo el ρ agrupado de arriba o pasa a ser el ρ dentro de cada gen (8 genes, 3 o 4 ARNdc cada uno, que quita el efecto del gen). Hasta que se decida, rige el texto original.
