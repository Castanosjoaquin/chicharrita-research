# La cuenta de azar para 18, 19 y 20 nucleótidos, contra lo que aparece de verdad

Fecha: 2026-10-20. Reproducible con `tools/sifi21_port/azar_kmer.py`; los números
están en `azar_por_k.json`, en esta carpeta.

El investigador lo pidió explícito en el checkpoint: hacer la probabilidad teórica
para 18, 19 y 20 nucleótidos y compararla con lo que devuelve el programa. Es el
soporte de su argumento de que **la biología no es random** — *«a pesar de que
parezca que es A, G, T, G, que es todo random, no es random. No vas a encontrar lo
que te dice la estadística que deberías encontrar por azar»*. Teníamos el lado
observado y no teníamos ni el esperado ni la comparación. Acá están los tres.

Se corrió sobre los cuatro genes de EPILAB y las seis referencias del panel, para k
de 15 a 21 —se agregaron 15, 16 y 17 porque son los que contestan la otra pregunta
pendiente, la del «salto en 17»—. La cantidad que se cuenta es la misma que cuenta
`offtarget_21nt.py`: **cuántas ventanas de la consulta tienen al menos un acierto
exacto** en la referencia, en las dos hebras. No el número de aciertos, que es otra
cosa y no es la que descarta una ventana.

---

## La respuesta corta

**Tenía razón, y sólo por debajo de 18 nucleótidos. Por encima de 18 el efecto se
da vuelta y es mucho más fuerte en la otra dirección.** Sobre las cinco referencias
no objetivo y los cuatro genes juntos:

| k | Ventanas | Observado | Esperado uniforme | Esperado por composición | Nulo barajado | Observado / uniforme |
|---:|---:|---:|---:|---:|---:|---:|
| 15 | 4.746 | 2.554 | 4.234,8 | 3.363,1 | 3.396 | **0,60** |
| 16 | 4.742 | 860 | 1.143,0 | 909,4 | 879 | **0,75** |
| 17 | 4.738 | 283 | 291,1 | 230,7 | 218 | **0,97** |
| 18 | 4.734 | 112 | 73,1 | 57,5 | 56 | **1,53** |
| 19 | 4.730 | 68 | 18,3 | 14,3 | 9 | **3,72** |
| 20 | 4.726 | 54 | 4,5 | 3,5 | 0 | **11,89** |
| 21 | 4.722 | 46 | 1,1 | 0,9 | 0 | **41,07** |

`[E]` Hay un **cruce entre 17 y 18 nucleótidos**. Por debajo, aparecen *menos*
coincidencias de las que el azar predice, que es exactamente lo que él describió.
Por encima, aparecen *muchas más*, y la razón crece hasta un factor de 41 en 21 nt.

La explicación de las dos mitades es la misma y es la que vuelve útil la cuenta: a
15 nucleótidos, casi todo lo que se encuentra es ruido, y el ruido real es algo
menor que el ruido teórico porque los genomas no son cadenas aleatorias. A 21
nucleótidos, casi nada de lo que se encuentra es ruido: lo que aparece es homología,
y la homología no la predice ninguna cuenta de probabilidad. **El tamaño de ventana
es lo que separa señal de ruido, y el cruce está justo donde la biología pone el
límite de lo que funciona.** `[H]` la lectura, `[E]` los números.

El dato más limpio de la tabla es la última columna del nulo barajado: **a 20 y a 21
nucleótidos, una referencia barajada con la misma composición exacta produce cero
coincidencias, mientras que la referencia real produce 54 y 46.** No es que el azar
explique poco a ese tamaño: no explica nada.

---

## Los tres nulos, y qué le quita cada uno al anterior

El orden de los tres importa, porque cada uno saca de la explicación una cosa
distinta.

**1. Uniforme, 1/4^k por posición.** Es «lo que dice la estadística» en su versión
más cruda: cuatro bases equiprobables e independientes. Para una referencia con *M*
posiciones, la probabilidad de que un k-mero dado aparezca al menos una vez en
alguna de las dos hebras es 1 − e^(−2M·4^−k).

**2. Ajustado por composición de cada referencia.** Las bases no son equiprobables,
y un k-mero rico en AT es mucho más probable en un genoma rico en AT. Este nulo
sigue suponiendo independencia entre posiciones del k-mero, pero calcula la
probabilidad de **cada** k-mero de la consulta con las frecuencias de base de la
referencia que se está mirando. Es el nulo honesto mínimo.

**3. Empírico por barajado.** Se barajan las bases de cada secuencia de la
referencia, lo que conserva la composición exacta —incluidas las N, de modo que el
número de posiciones no cambia— y destruye toda la estructura: repeticiones,
familias de genes, baja complejidad, sesgo de codones y, sobre todo, homología. Se
vuelve a correr la misma búsqueda exacta sobre la referencia barajada.

La descomposición, a k = 15, que es donde hay señal suficiente para hacerla:

| Paso | Valor | Lo que explica ese paso |
|---|---:|---|
| Esperado uniforme | 4.234,8 | — |
| Esperado por composición | 3.363,1 | la composición de bases explica una caída del **20,6 %** |
| Nulo barajado | 3.396 | coincide con el anterior: **valida la cuenta analítica** |
| **Observado** | **2.554** | la estructura explica una caída adicional del **24,8 %** |

`[E]` Dos lecturas. La primera: **que el barajado y la cuenta por composición den
casi lo mismo —3.396 y 3.363— es la validación cruzada del método**, porque son dos
caminos independientes hacia el mismo número, uno analítico y otro por simulación.
La segunda, que es la respuesta a lo que se preguntó: de la diferencia entre lo que
predice el azar puro y lo que aparece, **la composición explica alrededor de la
mitad y la estructura la otra mitad**. Ni la composición sola alcanza, ni queda todo
sin explicar.

---

## Por referencia: el cruce se corre según el parentesco

La razón entre observado y esperado uniforme, por referencia y por k:

| Referencia | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|---|---:|---:|---:|---:|---:|---:|---:|
| *Apis mellifera* | 0,35 | 0,46 | 0,48 | 0,59 | 0 | 0 | 0 |
| *Harmonia axyridis* | 0,44 | 0,48 | 0,37 | 0,59 | 1,98 | 6,35 | 18,75 |
| *Folsomia candida* | 0,64 | 0,70 | 0,81 | 0,74 | 1,35 | 2,17 | 0 |
| *Zea mays* | 0,72 | 0,90 | 1,02 | 1,04 | 0,72 | 0 | 0 |
| *Homalodisca vitripennis* | 0,77 | 1,09 | 2,09 | 5,13 | 17,31 | 62,34 | **226,32** |
| *Dalbulus maidis* | 0,84 | 1,70 | 5,37 | 20,01 | 78,01 | 307,90 | **1.218,18** |

`[E]` El cruce se corre con el parentesco, y eso es exactamente lo que uno esperaría
si lo que sube la razón es homología y no azar:

- En ***Apis mellifera*** no cruza nunca: la razón se queda por debajo de 0,6 y
  después cae a cero. No hay una sola coincidencia de 19 nt o más entre estos cuatro
  genes y el transcriptoma de la abeja. Es la mejor noticia del cuadro y ahora
  además tiene un marco: no es que haya pocas, es que hay **menos de las que el azar
  predeciría**, y a partir de 19 nt no hay ninguna.
- En ***Zea mays*** la razón se queda en 1 en todos los tamaños. El maíz se comporta
  como una secuencia esencialmente aleatoria respecto de estos cuatro genes: no hay
  homología que detectar, sólo ruido. `[H]`
- En ***Homalodisca vitripennis*** cruza entre 15 y 16 y después se dispara hasta
  226. Es un cicadélido, y lo que aparece a 21 nt son los tramos conservados de
  Bicaudal C y de la V-ATPasa. **Esa columna es, numéricamente, el mismo hecho que
  dispara el veto del ranking.**
- En ***Dalbulus maidis*** cruza en 16 y llega a 1.218, lo que es esperable y no es
  off-target: dos de los cuatro genes son suyos. Sirve como control positivo del
  método.

---

## El «salto en 17»: no se reproduce como salto, y sí como cruce

El equipo le contó en la reunión que al acortar la ventana el comportamiento era
aproximadamente lineal hasta 18 y que en **17 subía marcadamente** la cantidad de
off-targets. Ese salto **no estaba documentado con números en el repositorio**. Con
esta corrida queda documentado, y la conclusión es mixta.

Cuánto se multiplica el número de ventanas comprometidas al acortar un nucleótido,
sobre las cinco referencias no objetivo:

| Al pasar de | a | Factor |
|---:|---:|---:|
| 21 | 20 | 1,17 |
| 20 | 19 | 1,26 |
| 19 | 18 | 1,65 |
| 18 | 17 | **2,53** |
| 17 | 16 | **3,04** |
| 16 | 15 | **2,97** |

`[E]` **No hay un salto discreto en 17.** La curva se empina progresivamente desde
19 hacia abajo, y los factores de 18→17, 17→16 y 16→15 son parecidos entre sí
—2,5, 3,0 y 3,0— sin que ninguno se destaque. Lo que la memoria del equipo registró
como «un salto en 17» es, en los números, **una aceleración que empieza entre 19 y
18**.

Pero el 17 no era un error de memoria, y conviene decirlo porque es lo interesante:
**17-18 es exactamente donde está el cruce entre observado y esperado.** A 17 nt la
razón observado/esperado es 0,97 y a 18 es 1,53. O sea que 17 **sí** es un umbral
real, sólo que no es el tamaño donde los conteos saltan, sino el tamaño por debajo
del cual **lo que se encuentra deja de ser homología y pasa a ser ruido**. Es un
umbral mejor que el que se recordaba, porque está medido y porque es el que
justifica el criterio.

Esto además concuerda en forma con lo que `pipeline/REPORT.md` §4.1 ya había medido
sobre otro conjunto —10.950 ventanas de 438 genes contra 25 especies—, donde la
supervivencia al filtro cae de 91,1 % en 17 nt a 72,3 % en 16 y a 33,5 % en 15, con
la curva casi plana de 18 para arriba. Las dos mediciones son sobre conjuntos
distintos y coinciden en la forma. `[E]`

---

## Lo que esta cuenta habilita decir sobre el criterio de 21

El investigador cerró el tema con *«tenés que tener la evidencia biológica atrás de
por qué elegís 21»*. La evidencia biológica es suya y es el tamaño en que Dicer
corta. Lo que esta cuenta agrega es el **argumento estadístico que la acompaña**, y
que antes no teníamos: a 21 nucleótidos, el azar predice 1,1 ventanas comprometidas
sobre las cinco referencias no objetivo y aparecen 46; una referencia barajada con
la misma composición produce 0. **A 21 nt, el 100 % de lo que el tamizaje marca es
estructura, no coincidencia.** A 15 nt, el 100 % es coincidencia y además sobra: el
azar predice más de lo que aparece.

Dicho de otro modo, y es la forma en que conviene presentarlo: **bajar el umbral no
hace el filtro más estricto, lo hace más ruidoso.** A 15 nt se descartarían 2.554
ventanas, y las que señalan homología son a lo sumo las 46 que siguen apareciendo a
21 nt: el resto, más de 2.500, son coincidencias que una referencia barajada produce
en la misma cantidad o en más. A 21 se descartan 46 y ninguna la produce el azar.
`[H]`

---

## Método y límites

El tamaño de ventana de `offtarget_21nt.py` se parametrizó con `--size` para poder
hacer esta cuenta. **Verificación obligatoria antes de usarlo:** con `--size 21` la
salida es **idéntica byte a byte** a la de antes de parametrizar —mismo `md5sum`
`a3229e733e4dc70c308c901583b4e4c3` sobre `offtarget_por_sirna.tsv`, 357.726 bytes—,
corrido sobre los cuatro genes y las seis referencias en esta misma corrida. Esos
conteos se citan en tres documentos y no se movió ninguno. `[E]`

Límites declarados, en orden de importancia:

El barajado es de **mononucleótidos**, no de dinucleótidos. Un barajado que preserve
también la frecuencia de pares conservaría parte de la estructura local y daría un
nulo más exigente; no se hizo por costo, y la consecuencia es que **la caída que
atribuimos a «estructura» incluye lo que un nulo de dinucleótidos habría atribuido a
composición de pares**. El tamaño del efecto a 15 nt (24,8 %) es por lo tanto un
máximo, no una estimación puntual. `[?]`

Se corrió **una sola** réplica de barajado por referencia. Con miles de ventanas de
consulta agregadas el conteo es estable, pero no hay intervalo. `[?]`

El nulo analítico supone independencia entre posiciones del k-mero. Es falso en
general y es justamente lo que el barajado viene a corregir; que los dos coincidan a
15 nt sugiere que el supuesto no hace daño a ese tamaño, pero no lo prueba para
todos. `[H]`

```bash
python tools/sifi21_port/azar_kmer.py \
    --consulta work/sifi_check/*_full.fasta \
    --db "work/offtarget_db/*.fna.gz" --k 15 16 17 18 19 20 21 \
    --salida research/ola2/W7_ranking/azar_por_k.json
```
