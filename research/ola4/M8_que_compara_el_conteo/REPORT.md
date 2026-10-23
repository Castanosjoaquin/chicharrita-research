# M8 — Hasta donde compara el numero de siRNAs eficientes, y que variables faltan

**Ola 4, linea M8.** Es la ultima de las preguntas de la carta del investigador del 22 de octubre
de 2026 y la unica de las nueve lineas que no pide correr nada: «¿hasta que punto el numero de
siRNAs eficientes predichos permite comparar estrategias dirigidas a genes diferentes? ¿Que otras
variables biologicas incorporarian?» `[R]`. No hace falta medir nada nuevo porque el repositorio
ya midio cuatro veces, sin proponerselo, que ese numero se mueve cuando no deberia moverse. Lo
que faltaba era escribirlo ordenado como respuesta.

**La respuesta, en una linea.** El numero de ventanas eficientes compara **regiones dentro de un
mismo gen, contadas con la misma configuracion, la misma referencia y la misma unidad**, y no
compara genes entre si: cuatro cosas que no son el blanco biologico lo mueven lo suficiente como
para invertir el orden de los candidatos, y **las cuatro ya estan medidas en este
repositorio**. Para comparar estrategias dirigidas a genes distintos el conteo es, como maximo,
uno de los terminos; el que decide es la evidencia de fenotipo, y para nuestro objetivo la
comparacion que manda no esta en el diseño sino entre el tiempo hasta el efecto y la ventana de
latencia del patogeno.

---

## 1. El conteo crudo no es comparable entre genes de largo distinto

`BicC_Dm` tiene 2.520 nt y `CP_MRFV` 528 (`research/ola2/W5_secuencias_epilab/REPORT.md`,
tabla de datos) `[M]`. A 21 nt eso son 2.500 ventanas contra 508: casi cinco veces mas
oportunidades de que alguna pase el filtro. Un conteo mayor, entonces, puede no decir nada sobre
el diseño y decir todo sobre el largo del gen.

No es una objecion teorica. Normalizando los conteos ya publicados por la cantidad de ventanas
—aritmetica sobre numeros nuestros, reproducible con `scripts/densidad.py`— el orden cambia en
las cuatro configuraciones que el repositorio tiene medidas, incluida la columna declarada por
EPILAB `[M]`:

| Configuracion | Orden por conteo crudo | Orden por densidad (eficientes por 100 ventanas) |
| --- | --- | --- |
| Original con sus valores por defecto | `BicC_Dm` 212 > `MP_MRFV` 133 > `ATPaseD_Dm` 42 > `CP_MRFV` 32 | `MP_MRFV` 10,70 > `ATPaseD_Dm` 8,92 > `BicC_Dm` 8,48 > `CP_MRFV` 6,30 |
| Port, modo fiel, ViennaRNA 2.7.2 | `BicC_Dm` 223 > `MP_MRFV` 142 > `CP_MRFV` 39 > `ATPaseD_Dm` 35 | `MP_MRFV` 11,42 > `BicC_Dm` 8,92 > `CP_MRFV` 7,68 > `ATPaseD_Dm` 7,43 |
| Port, modo corregido (ancla de W7) | `BicC_Dm` 171 > `MP_MRFV` 123 > `CP_MRFV` 30 > `ATPaseD_Dm` 29 | `MP_MRFV` 9,90 > `BicC_Dm` 6,84 > `ATPaseD_Dm` 6,16 > `CP_MRFV` 5,91 |
| Planilla de EPILAB (declarado) | `BicC_Dm` 199 > `MP_MRFV` 114 > `CP_MRFV` 35 > `ATPaseD_Dm` 33 | `MP_MRFV` 9,17 > `BicC_Dm` 7,96 > `ATPaseD_Dm` 7,01 > `CP_MRFV` 6,89 |

Tres cosas que se leen de esa tabla. **`BicC_Dm` es primero por conteo en las cuatro columnas y
no es primero por densidad en ninguna**; con los conteos del programa original cae del primer al
tercer puesto `[M]`. **`MP_MRFV` es primero por densidad en las cuatro** y segundo por conteo en
las cuatro. Y el ultimo puesto tambien se da vuelta: en el modo corregido y en la planilla,
`CP_MRFV` es tercero por conteo y ultimo por densidad, mientras `ATPaseD_Dm` hace el camino
inverso. O sea que la eleccion de unidad no mueve un detalle del medio de la tabla: mueve las dos
puntas.

La unidad comparable, entonces, es la densidad, o mejor el conteo **de la region de largo fijo
que efectivamente se va a sintetizar**, que es como el entregable ya reporta las regiones
recomendadas (200 y 300 nt) precisamente para no comparar un gen de 2.520 nt contra uno de 528.
Y queda una advertencia sobre la densidad misma: el entregable tiene medido que elegir region
discrimina en los genes largos y no en los cortos —con el nulo de bloques de 30 nt ni `eth` ni
`burs-alpha` se distinguen del azar, p = 0,364 y 0,459 (`research/ola3/C7_ranking_v2/REPORT.md`
§3) `[M]`—, asi que en un gen de 468 nt, donde una region de 200 nt cubre casi la mitad, la
densidad del gen y la de la region son casi el mismo numero y no hay nada que elegir.

## 2. Depende de la referencia y de la unidad de conteo

El segundo limite es el que midio la linea M1, y las dos mitades ya estan cerradas.

Lo cerrado es la unidad. La columna «Efficient siRNA hits» del si-Fi21 original **no cuenta
ventanas: cuenta aciertos de Bowtie en la hebra `+`, agrupados por nombre de referencia**
(`general_helpers.py:113`), y eso se ve en el propio dato: para `BicC_Dm` el programa informa
2.504 hits sobre un gen que tiene 2.500 ventanas, porque dos pares de 21-meros estan repetidos
dentro del gen y esas cuatro consultas pegan en dos lugares cada una
(`research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md` §0) `[E]`. Esos cuatro registros de
mas son ventanas no eficientes, asi que ahi el conteo de eficientes no se inflo; la cuestion es
que **puede** inflarse, y por una via que no tiene nada que ver con el gen blanco.

Lo medido es la referencia, y ya no es una hipotesis: la matriz de M1 corrio sobre once bases y
treinta y ocho celdas con el motor verificado, y **ninguna celda reproduce los cuatro valores
declarados** (`research/ola4/M1_conteo_y_referencia/REPORT.md` y
`resultados/matriz.md`, D52) `[M]`. Lo que la matriz muestra es mas fuerte que la hipotesis que
venia a probar. Para `BicC_Dm`, **el mismo gen con la misma configuracion y la misma regla da 0,
191, 200 o 212 segun contra que base se cuente** —cero contra maiz, *Apis mellifera*, *Harmonia
axyridis* y *Folsomia candida*; 191 contra el genoma de su propia especie; 200 contra los contigs
blanco de la ensambladura TSA `GITV01`, que es la unica celda de toda la matriz que se acerca a
un valor declarado; 212 contra el gen mismo— `[M]`. Y el caso extremo es `ATPaseD_Dm` contra el
genoma de *Dalbulus maidis*: **cuenta 0**, porque 40 de sus 42 ventanas eficientes pegan solo en
la hebra menos del cromosoma `OZ319711.1` y la regla del original evalua unicamente la hebra `+`
`[M]`.

A eso se agrega que la agregacion tambien es una eleccion. Para `CP_MRFV` contra el conjunto de
registros publicos de MRFV, sumar las filas de la tabla da **779** y tomar la fila mayor da
**32**: el mismo gen, la misma referencia, la misma corrida de Bowtie, dos reglas de agregacion
`[M]`. **El numero, entonces, no es comparable ni consigo mismo entre dos corridas**, y la
pregunta para el lunes pasa de ser «contra que base corrieron» a «contra que registro contaron,
y sumando que».

## 3. Depende de la version del motor, de la tabla termodinamica y del largo de ventana

Este limite esta medido tres veces, con el mismo diseño en las tres: se cambia una sola cosa de
la implementacion, nada del gen ni de la biologia, y se cuenta otra vez.

**La version del motor de accesibilidad.** Nuestro port en modo fiel con RNAplfold 2.1.5
reproduce exacto los cuatro conteos del programa original —133, 32, 212 y 42 para `MP_MRFV`,
`CP_MRFV`, `BicC_Dm` y `ATPaseD_Dm`— y el mismo port, el mismo modo y las mismas secuencias con
las ligaduras de ViennaRNA 2.7.2 dan **142, 39, 223 y 35** `[M]`
(`research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md` §0 y
`research/ola3/C2_codigo_apolo_inta/corridas/README.md`). Lo que importa no es solo que los
cuatro numeros se muevan, sino **como**: tres suben y uno baja, de modo que `ATPaseD_Dm` y
`CP_MRFV` intercambian el tercer y el cuarto puesto por un cambio de version de una libreria.

**La tabla de vecinos mas cercanos.** La reescritura del INTA cambia la tabla con la que se
calcula el ΔG de los extremos, de Chen *et al.* 2012 a la de Zuber *et al.* 2022, y con todo lo
demas igual los conteos pasan de 142, 39, 223 y 35 a **138, 40, 218 y 35**: catorce ventanas
cambian de veredicto, tres entran y once salen
(`research/ola3/C2_codigo_apolo_inta/diff_sifi21INTA_vs_original.md`, diferencia 1) `[M]`.

**El largo de ventana.** A 22 nt en vez de 21, el mismo motor y las mismas secuencias en modo
fiel mueven los cuatro conteos asi: `ATPaseD_Dm` 35 a 40 (+14,3 %), `CP_MRFV` 39 a 30 (−23,1 %),
`MP_MRFV` 142 a 136 (−4,2 %) y `BicC_Dm` 223 a 210
(`research/ola3/C3_blast_ventana_azar/ventana_21_vs_22.md`) `[M]`, con signo distinto segun el
gen. Y no es una variacion caprichosa
que podamos descartar: no hay perfil de siRNA publicado para ningun hemiptero, y el largo lo
dicta la maquinaria del hospedador (Zotti *et al.* 2026, *Viruses* 18:285) `[R]`, asi que **no
sabemos cual de los dos numeros corresponde a nuestro insecto**.

Sumados, los tres dicen lo mismo: una parte de la diferencia entre dos conteos es diferencia de
software, y si dos equipos comparan estrategias con «numero de siRNAs eficientes» sin declarar
version, tabla y largo, estan comparando dos cosas que no son la misma.

## 4. El conteo en el contexto del gen no es el de la molecula recortada

El cuarto limite es el que mas incomoda, porque afecta a las cifras que nuestro propio entregable
publica. Las ventanas eficientes de una region se contaron **sobre el perfil del gen completo**,
pero la molecula que se sintetizaria es el recorte, y sus primeros y ultimos nucleotidos ya no
tienen al lado la secuencia que tenian dentro del gen. Medido en modo corregido
(`research/ola3/C13_quimeras_region_recomendada/REPORT.md` §4) `[M]`:

| Gen | Region | Eficientes en contexto | Eficientes recortada | Δ |
| --- | --- | ---: | ---: | ---: |
| `MP_MRFV` | 72-271 | 38 | **27** | −11 |
| `CP_MRFV` | 99-298 | 21 | 23 | +2 |
| `BicC_Dm` | 922-1221 | 36 | **26** | −10 |
| `ATPaseD_Dm` | 72-371 | 21 | 20 | −1 |

Las dos cifras que resumen a nuestros dos primeros candidatos, 38 y 36, **bajan a 27 y a 26 en la
molecula que se sintetizaria**: un cuarto del numero. Parte de la diferencia es aritmetica (una
region de 200 nt dentro del gen tiene 200 posiciones de inicio porque las ultimas ventanas se
completan con el nucleotido de al lado, y recortada tiene 180) y parte es el borde: 27 ventanas
cambiaron de veredicto en las cuatro regiones. El orden de los cuatro no cambia, pero el numero
si, y el signo no es parejo: `CP_MRFV` sube. Conviene decir con que ancho de borde pasa esto,
porque C13 tambien corrigio la mecanica: la secuencia ajena influye hasta **72 nt corriente abajo
del final de la ventana y 59 corriente arriba de su comienzo**, porque el criterio mide la
accesibilidad de un tramo de 8 nt que termina en el ultimo nucleotido de la ventana `[M]` el
numero, `[H]` la derivacion.

## 5. Lo que el numero si permite, para no tirar al chico con el agua

Los cuatro limites acotan el uso; no lo anulan. Dentro de un mismo gen, con una sola
configuracion declarada, una sola referencia y una sola unidad, el conteo **ordena regiones**, y
hay dos fuentes abiertas que sostienen que ese orden tiene algo que ver con la realidad: en
*Mythimna separata*, la posicion del fragmento de 200 pb dentro del gen *MsChi2* cambio la
eficacia, y esa eficacia correlaciono con el numero de siRNA eficientes predichos (Bao *et al.* 2026, *Insects*, doi 10.3390/insects17090931) `[E]`. La contracara, en un
hemiptero y por lo tanto mas cerca de nuestro caso: en *Apolygus lucorum*, fragmentos del mismo
largo del mismo gen dieron entre 58,9 % y 70,0 % de mortalidad **y otros del mismo largo no
dieron nada** (Luo *et al.* 2026, *Frontiers in Insect Science*, doi 10.3389/finsc.2026.1912427)
`[E]`. Las dos cosas a la vez: elegir region importa, y el numero no alcanza para predecir cuanto.

A eso se suma el limite que el entregable ya declara en su casilla de validacion: con los datos
abiertos que existen no se distingue un filtro bueno de uno inutil —ρ = +0,142, IC95 [−0,247,
+0,492], n = 29, en *Tribolium castaneum*, no concluyente `[M]`—. Una ventana que pasa el filtro
no demuestra silenciamiento. Por eso, y es la razon de fondo, el ranking del proyecto lee la
calidad del diseño y la evidencia publicada de fenotipo como **dos ejes separados que no se
suman** (D24), y presenta las listas del insecto y del virus sin compararlas entre si (D38).

## 6. Las variables que habria que incorporar

Van ordenadas por cuanto cambiarian la decision, no por cuanto nos costaria conseguirlas. De cada
una decimos que tenemos y que nos falta; lo que falta queda registrado en
`00_meta/PREGUNTAS_ABIERTAS.md`.

**La ventana de latencia del patogeno contra el tiempo hasta el efecto.** Es la que manda para
nuestro objetivo y la unica que puede volver irrelevante a todo lo demas: si el insecto transmite
antes de que el silenciamiento haga efecto, matarlo no corta la transmision. Lo que tenemos es
una asimetria incomoda: la ventana de latencia es de unos 20 dias —cifra del investigador,
aceptada en el checkpoint 1 (D34) `[R]`— y los ensayos abiertos en la especie miden el desenlace
a los 4 o 5 dias `[R]`. Lo que falta es el dato duro de los dos lados: la fuente abierta de
latencia que tenemos (Jones y Medina 2020) da 18 a 22 dias para *Spiroplasma kunkelii*, no para
el MRFV `[?]`, y no hay seguimientos publicados mas largos que 5 dias que nos digan si el efecto
dura. **Esta es la comparacion que decide si esterilizar alcanza o si hace falta matar**, y es
una pregunta para el investigador antes que un calculo nuestro.

**Evidencia de fenotipo tras silenciamiento, en la especie o en un pariente.** Es lo unico que
conecta el diseño con el efecto buscado, y es el eje que nuestro ranking ya separa de la eficacia
de diseño (D24). Tenemos bastante y desparejo: en `eth` y `burs-alpha`, knockdown de ~90 % y
~95 % y supervivencia cayendo al 10 % al dia 4 en `burs-alpha` —la cifra de `eth` no esta en el
texto y hay que leerla de la figura 5A `[?]`—, n = 40, pero **por microinyeccion en ninfas de
quinto estadio**, no por ingesta (Andrada *et al.* 2026, *Frontiers in Insect Science* 6:1811933)
`[E]`; en la V-ATPasa, supervivencia por dieta a 4 dias de ~18 % contra ~37 % del control de GFP
`[R]`; en `BicC`, oviposicion y fenotipo ovarico, **solo desde el resumen** porque el texto
completo de Dalaison-Fuentes 2022 no es abierto `[R]`. Lo que falta es lo que haria comparables
esas cifras: los desenlaces no son el mismo (oviposicion en adultas, supervivencia de ninfas por
via oral, supervivencia y muda por inyeccion), los estadios no son el mismo y los controles no
son el mismo (β-lactamasa, GFP, sin ARNdc), con n de tres replicas de tres ninfas en los ensayos
moleculares (`research/ola2/W6_agentes_ciencia/notas/PRB_notas.md`) `[R]`. Hay ademas un sesgo de
supervivencia declarado: el knockdown se mide en los insectos vivos al momento del muestreo
`[H]`.

**Nivel de expresion en el tejido que el ARNdc ingerido efectivamente alcanza.** Aca no tenemos
nada, y el hueco es doble. Ninguna fuente abierta identifica que celula del insecto recibe el
ARNdc por ingesta `[?]`, y los transcriptomas con los que trabajamos no pueden contestarlo: el
que usa el grupo que publica en la especie es de **ARN de cuerpo entero de individuos agrupados
de varios estadios** (tesis de Palacio, UNNOBA 2018, citada en metodos por Andrada *et al.* 2026)
`[E]`, de modo que no da expresion por tejido ni por estadio. Un gen muy expresado en un tejido
que el ARNdc no alcanza es un candidato peor que su conteo de ventanas sugiere, y hoy no tenemos
forma de distinguirlos.

**Redundancia por parologos.** Silenciar un miembro de una familia puede no hacer nada, y eso no
aparece en ningun conteo de ventanas. No lo medimos. Lo mas cerca que estamos son dos señales
indirectas: `ATPaseD_Dm` tiene 7 ventanas con bloque perfecto de 19 nt o mas contra humano frente
a las 2,4 esperadas por azar, compatible con que la subunidad D de la V-ATPasa este conservada
`[H]` (`research/ola3/C7_ranking_v2/REPORT.md` §1), y los dos pares de 21-meros repetidos dentro
de `BicC_Dm`, que son repeticion interna y no parologia. Es una corrida local posible y no hecha:
buscar los parologos de cada candidato en el genoma de *Dalbulus maidis* `GCA_975739785.1` con las
herramientas que ya usamos.

**Esencialidad del gen.** Tenemos la via de anotacion funcional declarada (KEGG, usada en C1a
para el argumento de esencialidad) `[E]` pero ninguna medicion propia, y no hay panel de
esencialidad para hemipteros: el unico panel grande de RNAi es iBeetle, en *Tribolium castaneum*,
un coleoptero holometabolo, del que salio el techo de ruido de 0,245 que el entregable declara
como calculo propio sin reproducir `[H]`. Falta un criterio operativo que no sea «la via parece importante».

**Recambio de la proteina.** Fija cuanto tarda el efecto, y por lo tanto entra directo en la
comparacion con la ventana de latencia: bajar el transcripto no sirve si la proteina que ya esta
en la celula dura mas que la ventana. No tenemos ningun dato, ni propio ni de fuente abierta,
para ninguno de los seis candidatos.

**Estadio de desarrollo en que se expone el insecto.** Tenemos dos piezas que no encajan entre
si, y la tension vale mas que cada una por separado: las ninfas ya transmiten y el tercer estadio
fue el mas sensible al RNAi en un cicadelido emparentado `[R]`, pero el bioensayo estandar de
dieta en sobre de parafilm **no sirve para ninfas, porque la dieta ya las mata**
(`00_meta/GLOSARIO.md`) `[R]`. Si el estadio mas sensible es el que no se puede tratar por la via
que se quiere usar, la comparacion entre candidatos cambia `[H]`. Falta el dato de sensibilidad
por estadio en *D. maidis*, que no esta publicado.

## 7. Que se lleva esto al entregable y a `00_meta/`

Para la casilla de validacion del entregable del checkpoint, un parrafo:

> `[M]` El numero de ventanas eficientes compara regiones dentro de un gen, no genes entre si, y
> lo tenemos medido cuatro veces: normalizando por largo, `BicC_Dm` pasa de primero por conteo a
> tercero por densidad (212 contra 8,48 por 100 ventanas, frente a 133 y 10,70 de `MP_MRFV`);
> cambiar RNAplfold 2.1.5 por ViennaRNA 2.7.2, con todo lo demas igual, mueve los cuatro conteos
> de 133/32/212/42 a 142/39/223/35 e intercambia el tercer y el cuarto puesto; cambiar la tabla de
> vecinos mas cercanos mueve catorce ventanas; y contar la region recortada en vez de la region
> dentro del gen baja 38 a 27 en `MP_MRFV` y 36 a 26 en `BicC_Dm`. `[H]` Para comparar estrategias
> dirigidas a genes distintos hace falta el eje de fenotipo, que el ranking ya separa, y la
> comparacion que decide es entre el tiempo hasta el efecto y la ventana de latencia del patogeno,
> que hoy es de unos 20 dias contra ensayos de 4 a 5 dias `[?]`.

Y a `PREGUNTAS_ABIERTAS.md` van las siete variables con lo que falta de cada una, agrupadas en una
sola entrada fechada, porque son pedidos que se le pueden hacer juntos al investigador el lunes.

## 8. Reproducibilidad y limites de este documento

La unica cuenta nueva es la normalizacion por largo de la seccion 1, y es aritmetica sobre
conteos ya publicados en el repositorio:

```
cd research/ola4/M8_que_compara_el_conteo/scripts
python test_densidad.py      # 7 de 7
python densidad.py           # escribe ../resultados/densidad.tsv
```

`scripts/densidad.py` documenta la procedencia de cada numero que usa, archivo por archivo, y
`scripts/test_densidad.py` verifica las tres afirmaciones que la seccion 1 hace: que la cantidad
de ventanas sale del largo (incluido el caso de `BicC_Dm`, donde son 2.500 y no los 2.504 hits que
informa el programa), que la densidad se calcula como se declara, y que en las cuatro
configuraciones el primero por conteo y el primero por densidad son genes distintos. Salida en
`resultados/densidad.tsv`.

Lo que este documento **no** hace: no corrio el motor de eficiencia, ningun alineador y ninguna
herramienta nueva, porque la linea no lo necesita. Ningun numero de las secciones 1 a 4 es nuevo;
todos salen de corridas ya hechas y citadas con su archivo, y los de la seccion 2 son de la
matriz que M1 corrio el 2026-10-23, posterior al borrador de esta linea. Y las tres cifras que
siguen pendientes de verificacion estan marcadas donde aparecen: la latencia del MRFV `[?]`, la
supervivencia de `ds-eth` al dia 4 (figura 5A de Andrada *et al.* 2026, no leida de forma
verificable) y el texto completo de Dalaison-Fuentes 2022.
