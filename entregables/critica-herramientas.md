# Crítica de las herramientas, y qué mejoras haríamos

**Para qué es este documento.** En el checkpoint 1 pediste explícitamente la crítica de las
herramientas, aclarando que no hacía falta implementarla: *«probamos el programa, este es una
porquería por tal cosa (…) ¿qué mejoras le haría? No hace falta hacerlo.»* Esto es eso.

**Regla que nos impusimos:** cada crítica va con la medición o la línea de código que la respalda.
Una crítica sin evidencia no entra. Donde decimos «medido», lo corrimos. Donde decimos «leído»,
leímos el fuente y no lo ejecutamos, y lo aclaramos.

Marcadores: `[E]` establecido, `[R]` reportado, `[H]` hipótesis nuestra, `[?]` incierto.

---

## Resumen: qué usaríamos para qué

**Para eficiencia, si-Fi21, y no hay alternativa.** Es la única de las tres que estima si un
fragmento va a silenciar. dsRNA-Engineer no calcula termodinámica ni tiene modelo entrenado, y
BLAST menos.

**Para off-targets, el tamizaje exacto local, y no dsRNA-Engineer.** Tres razones: no se le puede
dar material no publicado; su número está dominado por una condición de 16 pb; y suma sin ponderar
tres condiciones contando líneas en vez de ventanas.

**Para BLAST, exploración y nada más.** Sirve para ver a qué se parece una secuencia. Para tamizar
ventanas de 21 nt, medimos que no puede hacerlo sin perder casos.

---

## 1. si-Fi21

### Lo que está mal y cambia el resultado

**La regla del nucleótido terminal no filtra, ramifica.** Una de sus ramas devuelve «eficiente»
sin mirar el veredicto termodinámico. Medido ventana por ventana sobre los cuatro genes: aporta
19 de 133 eficientes en `MP_MRFV`, 7 de 32 en `CP_MRFV`, 50 de 212 en `BicC_Dm` y 8 de 42 en
`ATPaseD_Dm` — **entre el 14 % y el 24 %**, y ninguna ventana va en sentido contrario. `[E]`

**El conteo depende del procedimiento, no sólo del gen.** Recortar la región y correrla aparte no
da lo mismo que leer esas posiciones de la corrida del gen entero: hasta **47 %** de diferencia
(16 contra 30 en `MP_MRFV`). `[E]` No es un defecto del programa, es una propiedad del cálculo de
accesibilidad, pero si no se declara cuál se usó los números no son comparables.

**El conteo depende de la base de datos.** si-Fi suma un registro por acierto de BOWTIE en hebra
positiva, no un siRNA único. Lo vimos funcionando en `BicC_Dm`: 2.504 aciertos sobre 2.500
ventanas, por dos pares de 21-meros repetidos dentro del propio gen. `[E]`

**Mezcla química de ADN dentro de un cálculo de ARN.** Los apilamientos y los extremos colgantes
usan parámetros de ARN, pero los desapareamientos usan tablas de ADN, porque el cálculo entero
corre en alfabeto de ADN tras convertir U en T. Consecuencia: un par G-U no se trata como wobble
de ARN. **Medimos que en la ruta que si-Fi usa para la eficiencia esas tablas no se consultan
nunca** —cero consultas en los cuatro casos—, así que el error existe y no afecta a este uso.
Afectaría a cualquier extensión a secuencias desapareadas. `[E]`

### Lo que falta de evidencia

**Dos de los seis valores que deciden el veredicto no tienen ninguna fuente**: el margen de
1,00 kcal/mol y los 22 °C. Y el valor 0,1 de accesibilidad es convención: la fuente sostiene el
principio y el tamaño de ventana, no el corte. `[E]`

**Y la condición de accesibilidad no muestra valor predictivo en los datos independientes que
pudimos revisar**: razón de probabilidades 1,00 con intervalo [0,89–1,12] sobre 300 casos humanos
de siRecords, y en *Tribolium castaneum* un cociente de riesgo de 0,9994 con P = 0,853, y P = 0,41
a nivel de ARNdc. `[E]` Es la crítica de fondo más importante de esta lista, porque toca una de las
tres patas del criterio. No afirmamos que la accesibilidad no importe: afirmamos que en los datos
disponibles no se ve.

### Lo que está mal como programa

Tres defectos operativos que cualquiera que intente correrlo se va a cruzar. `[E]`

1. **No encuentra su propio RNAplfold.** Hace `chdir` al directorio de la herramienta y después
   llama al ejecutable por nombre pelado pasando `cwd`, así que la búsqueda se hace desde el
   directorio equivocado. El error cae en una rama que deja una variable sin asignar y Qt se lo
   traga: **el síntoma es que el botón Start no hace nada**. Se resuelve poniendo los directorios
   de RNAplfold y Bowtie en el PATH. `[H]` Es probable que sea a lo que te referiste cuando
   dijiste que el programa «no anda bien»: quien tenga ViennaRNA instalado aparte nunca lo ve.
2. **La tabla de resultados no se muestra nunca.** La ventana de resultados muestra la imagen y
   nada más; el número de eficientes, que es el resultado principal, sólo sale por
   **Save as → Table (CSV)**, escribiendo la extensión a mano.
3. **El detalle por ventana no existe fuera del gráfico.** Lo que el programa exporta son tres
   columnas y una fila por gen: `Targets; Total siRNA hits; Efficient siRNA hits`. Qué ventana
   concreta fue eficiente y por qué sólo está dibujado. Por eso, para poder auditar cualquier
   número, hubo que reimplementar el motor.

### Qué mejoras le haríamos

**Lo primero y más barato: persistir el veredicto por ventana con sus términos**, en vez de sólo
la curva. Es una tabla más y habilita auditar, rankear y recalcular sin volver a correr. **Lo
segundo: que la regla terminal filtre en vez de ramificar**, que es una línea. **Lo tercero:
exponer la temperatura como parámetro**, porque el veredicto depende de ella y hoy está fija en dos
lugares distintos del código. Y **declarar en la salida contra qué base y con qué versión de
ViennaRNA se corrió**, porque las dos cosas cambian el número.

---

## 2. dsRNA-Engineer

### El problema que no es técnico y es el principal

**La herramienta que el corpus señala como la de diseño y verificación de off-targets es
exactamente la que no se puede usar con el material que nos dieron.** Corre sólo como servicio
web, procesa del lado del servidor, no declara política de retención y no tiene cuenta. Los dos
genes del insecto son material no publicado, y un dato subido no se puede desubir. Corrimos los dos
genes virales, que verificamos byte a byte que son subcadenas exactas de un registro público del
NCBI y que se autorizaron explícitamente; **`BicC_Dm` y `ATPaseD_Dm` no se subieron y no se van a
subir**. El benchmark de esos dos genes se hizo con dos herramientas, no con tres. `[E]`

### Lo que está mal en lo que informa

**El 100 % del riesgo que le muestra al usuario viene de la condición de 16 pb y el 0 % de la de
21-22 pb.** `[E]` Para `CP_MRFV` informa 87 off-targets en maíz, un gen donde nuestro tamizaje
exacto no encuentra **ni una sola** coincidencia de 19 nt o más contra ninguna de las seis
referencias; para `MP_MRFV` informa 215 contra 3. La atribución está verificada: si el conteo
estuviera dominado por la condición de 21 pb, nuestro conteo a k = 21 debería ser del mismo orden,
y es **cero en las doce celdas**; si lo estuviera por la de 16 pb, nuestro conteo a k = 16 debería
serlo, y lo es. Esto replica sobre dos genes nuevos y cinco referencias lo que ya habíamos medido
sobre un gen público.

**Y la condición de 16 pb es ruido.** Medimos las coincidencias esperadas por azar: sobre los
cuatro genes y las cinco referencias no objetivo, a 16 nucleótidos se observan **860 ventanas
comprometidas contra 909 esperadas** por un nulo que conserva la composición de cada referencia
(y 1.143 por azar uniforme) — una razón de **0,75**, es decir **por debajo del azar**. Recién en
17 nt la razón llega a 0,97 y empieza a tener sentido leerla como señal. Un número que aparecería
igual, o más, con secuencia aleatoria no es una medida de riesgo. `[E]`

**Mezcla dos preguntas distintas en un solo número.** Suma sin ponderar sus tres condiciones y
cuenta **líneas de Bowtie**, no ventanas distintas, así que el número confunde «cuántas ventanas
son riesgosas» con «a cuántos parálogos llegan». Son decisiones diferentes.

**Los fragmentos que recomienda no sirven para lo que ustedes sintetizan.** Para `MP_MRFV`
recomendó fragmentos de entre **51 y 91 pb**, igual que en una corrida anterior sobre otro gen.
Ustedes trabajan con regiones de 150 a 250 nt y las de la planilla son de 200 y 300. **Los dos
rangos no se superponen**, así que su módulo de recomendación no es utilizable tal cual aunque el
de off-targets lo fuera. `[E]`

**Una limitación nueva, observada en esta corrida:** el endpoint de descarga devolvió el texto
`Error!` para los dos proyectos. En una corrida anterior el mismo endpoint entregaba los archivos
crudos de Bowtie. Sin esos archivos no se puede desagregar el conteo desde el lado de la
herramienta. Queda como `[?]`: no sabemos si es transitorio o un cambio de la API.

### Lo que sí tiene y nosotros no

Conviene decirlo: **un panel de 1.103 especies**, con 127 hemípteros, 27 polinizadores, 94 plantas
de cultivo y 97 artrópodos no blanco. El nuestro tiene seis referencias. Para un tamizaje amplio
sobre material ya publicado, esa es la herramienta.

### Qué mejoras le haríamos

**Separar el número en sus condiciones** en vez de sumarlas, y contar ventanas en vez de líneas.
**Quitar la condición de 16 pb del indicador de riesgo** o marcarla como exploratoria, porque hoy
domina el resultado y no discrimina del azar. **Ofrecer una versión que corra local**, que es lo
único que la volvería usable con material no publicado. Y **alinear el largo de los fragmentos
recomendados** con el régimen que los laboratorios efectivamente sintetizan.

---

## 3. BLAST

No es una crítica a BLAST, que hace exactamente lo que dice hacer. Es una crítica a usarlo para
este tamizaje.

**No puede encontrar todos los 21-meros con un desajuste, y medimos el techo.** Sobre 3.150
consultas con desajustes plantados en cada una de las 21 posiciones, la mejor configuración
alcanza **0,762** de sensibilidad, y el `megablast` por defecto da **cero en las 21 posiciones**.
`[E]` Dos causas, las dos identificadas: el tamaño de palabra gobierna si el alineamiento se
intenta siquiera —un 21-mero con un desajuste en la posición 11 queda partido en dos bloques de 10
y con palabra 11 no siembra—, y la extensión **recorta un desajuste cercano al extremo en vez de
cruzarlo**, porque cruzarlo no paga con los premios y penalidades por defecto. La fórmula predice
qué posiciones se pierden en cada configuración.

**La consecuencia medida sobre nuestros datos:** el criterio de un desajuste calculado con BLAST+
queda por debajo del exacto por un factor de hasta **3,2** (5 contra 16 en `BicC_Dm`, 9 contra 17
en `ATPaseD_Dm`). Quien pondere el riesgo con el número de BLAST está ponderando un número bajo por
construcción. `[E]`

**Y la trampa que más fácil se comete:** `-perc_identity` **no filtra sobre la consulta completa
sino sobre el alineamiento que BLAST encontró**. Pidiendo 590 ventanas de 26 nt con
`-perc_identity 92`, BLAST devolvió 827 filas y **cero** eran alineamientos de 26 nt: los largos
eran de 11 a 16 nt. Contar líneas de salida de BLAST como «cantidad de off-targets» sobreestima el
riesgo por un factor de cientos. `[E]`

**Qué haríamos en su lugar, y es lo que hacemos:** coincidencia exacta con presupuesto de
desajustes, que para bloques perfectos es la respuesta correcta y no una heurística. Verificado
contra la corrida de BLAST+: los criterios de bloque perfecto **coinciden en las 20 celdas**, lo
que valida las dos implementaciones; el de un desajuste no coincide, y el exacto encuentra más. Si
alguien quiere seguir con BLAST, hay que postfiltrar por largo y desajustes, o fijar `-word_size`
igual al largo de la ventana con `-ungapped`.

---

## 4. El código del laboratorio: sifi21INTA y Apolo Rocket

Encontramos los dos repositorios públicos, los leímos y corrimos `sifi21INTA`. Esto es lo que
vimos, y va con el mismo criterio que lo demás: cada punto con su línea o su medición.

### Lo que está mal y cambia el resultado

**Una secuencia en minúsculas produce cero eficientes, en silencio.** `createSirnas` llama a
`sequence.upper()` **sin asignar el resultado**, y como la regla terminal compara contra literales
en mayúscula, ninguna ventana entra por ninguna rama. Medido sobre `MP_MRFV_full`: **138 eficientes
en mayúsculas, 0 en minúsculas**, con Bowtie alineando igual las 1.243 ventanas, de modo que la
corrida parece exitosa. `[E]` En una plataforma web que recibe la secuencia como texto, eso es un
resultado erróneo servido con cara de resultado válido. Se arregla con una línea, y es lo primero
que arreglaríamos.

**Conserva la rama de la regla terminal**, transcrita literal del original, con el mismo efecto del
14 al 24 %. `[E]`

**La curva del gráfico cubre 20 de las 21 posiciones de cada siRNA**, donde el original cubría las
21. Se ve en los propios datos de ejemplo de Apolo Rocket: la suma de la curva dividida por 20 da
entero exacto. No cambia el conteo pero sí el gráfico. `[E]`

### Lo que es arbitrario o no se valida

**La elección del blanco principal es una decisión humana sin registro** —`input()` por consola en
uno, una lista de números en el JSON en el otro—, y de ella depende por completo la única columna
que mira especificidad. **La elección de región tampoco se valida**: el volcado de ejemplo contiene
una consulta con región «800-100» y secuencia de largo cero, insertada igual en la base. `[E]` Y al
fusionar alineamientos en bloques, **los desapareamientos se suman**, así que la columna de
desapareamientos no significa lo que su nombre dice.

### Lo que falta, y es el hueco donde entra nuestro aporte

**No hay priorización.** No hay puntaje, ni orden, ni umbral de corte, ni función de agregación en
ninguno de los dos repositorios: la salida es «acá están las ventanas eficientes y acá los
alineamientos», y la decisión queda del lado de la persona. `[E]` Y en el esquema de la base está
el lugar donde enchufarlo, con nombre y todo: la columna `method` de la tabla `efficiency`,
documentada como «'sifi21' or 'IA'», **sin implementación**.

### Qué mejoras le haríamos, sin implementarlas

Cinco, en orden de costo: **normalizar mayúsculas y validar coordenadas en la entrada** (una línea
y un chequeo); **persistir el veredicto por ventana con sus términos** en vez de sólo la curva, que
es lo que habilita auditar y rankear sin volver a correr; **ponderar los desapareamientos por
posición** en el tamizaje, separando la región semilla (nt 2-8) y las posiciones catalíticas 10-11
del resto; **exponer la temperatura como parámetro**; y para el gancho `IA`, **que devuelva un
puntaje por ventana en vez de un booleano**, lo que exige cambiar el tipo de una columna pero no el
resto del esquema.

Un apunte que no es sobre el método y conviene que sepan: el archivo de constantes del repositorio
público trae en claro el nombre de la base, el usuario, la contraseña, el host y el puerto. No
reproducimos los valores acá.

Ninguna de estas mejoras la implementamos, y es deliberado: nuestro aporte declarado es la
priorización auditable, no mejorar herramientas ajenas.

---

## 5. Lo que estas críticas no son

No son una lista de razones para descartar si-Fi21. Es la línea de base del campo, es lo que usan
ustedes, y nuestro port reproduce sus cuatro conteos exacto, lo que quiere decir que entendimos el
criterio y no que lo estemos reemplazando. Lo que las críticas hacen es fijar **cómo hay que leer
cada número**: con qué modo, contra qué base, con qué versión de ViennaRNA y bajo qué
procedimiento de región. Esa es la diferencia entre un conteo y un dato.
