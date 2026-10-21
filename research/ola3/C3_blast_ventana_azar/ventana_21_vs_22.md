# Q2 — ¿21 o 22 nt, y por qué no menos?

Dos cosas distintas, separadas a propósito: la **evidencia biológica** de qué largo produce la
maquinaria del insecto, y el **benchmark computacional** de qué cambia en nuestros cuatro genes
si se corre la ventana a 22 en vez de 21.

## Parte A — La evidencia biológica

### A.1 El largo lo fija la geometría de la enzima, no una convención

Dicer corta a una distancia fija del extremo del dúplex porque el dominio PAZ ancla ese extremo
y los dos dominios RNasa III cortan a una distancia determinada por la separación física entre
ellos. Es el modelo de la **regla molecular** (*molecular ruler*): en la estructura
cristalográfica de la Dicer de *Giardia intestinalis* la distancia PAZ–RNasa III es de 65 Å y
coincide con lo que ocupan 25 pares de bases, que es el producto de esa enzima. Macrae et al.
2006, *Science* 311:195-198 (`10.1126/science.1121638`) — **de este artículo sólo pudimos leer
el resumen**: está cerrado y ninguna de las vías de acceso abierto lo tiene. `[E]` el concepto,
que es consenso; `[R]` el número de 65 Å, que viene del resumen y no del texto completo.

La consecuencia para nosotros es directa: **el 21 no es una convención de software.** Cambiar
de 21 a 18 no es relajar un parámetro, es pedir una molécula que la enzima no produce.

### A.2 En insectos el largo es 20, 21 o 22 según el orden, y está medido

El trabajo experimental que fija esto es Santos et al. 2019, *Viruses* 11:738
(`10.3390/v11080738`), que secuenció los siRNA derivados de virus y de ARNdc en **seis especies
de cinco órdenes**. El resultado, según su propio resumen y el uso que de él hace la revisión
de 2026: dípteros (*Drosophila melanogaster*) y coleópteros (*Tribolium castaneum*) producen
mayoritariamente **21 nt**; himenópteros (*Bombus terrestris*) y ortópteros (*Locusta
migratoria*) están enriquecidos en **22 nt**; lepidópteros (*Spodoptera exigua*, *Trichoplusia
ni*) producen sobre todo **20 nt**. `[E]`

La correlación estructural la propone Zotti et al. 2026, *Viruses* 18:285
(`10.3390/v18030285`), con modelado por homología de la Dicer-2 de esas especies sobre la
estructura cristalográfica de la de *D. melanogaster* (PDB 7V6C). Las distancias promedio
PAZ–RNasa III que miden son 60,3 Å en *D. melanogaster* (~21 nt), 59,8 Å en *T. castaneum*
(~21 nt), 62,2 Å en *B. terrestris* (~22 nt), 62,3 Å en *L. migratoria* (~22 nt) y 58,3 Å en
*T. ni* (~20 nt); diferencias de 1 a 2 Å entre especies. **Son modelos, no estructuras
experimentales**, y los propios autores piden confirmación con secuenciación comparada de ARN
pequeños. `[R]`

> Que el largo cambie de especie en especie por geometría de la enzima es, para nuestro
> problema, la mejor justificación posible de por qué el benchmark 21 contra 22 que pidió el
> investigador vale la pena: **no sabemos en qué lado del borde cae la chicharrita.**

### A.3 Hemiptera: el dato que hay, y el que no

**Ni Santos 2019 ni Zotti 2026 incluyen un solo hemíptero.** Lo verificamos sobre los textos
completos que abrimos: el primero declara cinco órdenes y Hemiptera no está entre ellos; el
segundo no contiene la cadena «Hemipter», «aphid», «whitefly», «planthopper» ni «leafhopper` en
ninguna parte. El marco de referencia que el campo usa para elegir 21 nt **no fue construido
con el orden al que pertenece nuestro blanco.** `[E]`

Lo que sí hay, especie por especie:

- ***Bemisia tabaci*** (mosca blanca, Hemiptera: Aleyrodidae). Mondal, Brown y Flynt 2020,
  *Life Science Alliance* 3(10):e202000731 (`10.26508/lsa.202000731`). La distribución de
  tamaños de ARN pequeños es **bimodal, con un pico en 22 nt que corresponde a productos de
  Dicer (siRNA y miRNA) y otro en 29-30 nt de piRNA**. Y el análisis de solapamientos con
  voladizo de 2 nt lo refuerza: las lecturas de **22 nt son las que más evidencia de
  procesamiento por Dicer muestran**, y los autores concluyen que ése es probablemente el
  tamaño del producto de Dicer-2. Además, en esta especie los piRNA son **más abundantes que
  los siRNA**, y de los productos de Dicer alrededor del 56 % son miRNA. `[E]`
- ***Bactericera cockerelli*** (psílido del tomate, Hemiptera: Triozidae). El ARNdc introducido
  se procesa a siRNA de **21 nt**. Dato tomado de la revisión de Sattar y Thompson 2016,
  *Front. Plant Sci.* 7:1241 (`10.3389/fpls.2016.01241`), que lo atribuye a Wuriyanghan et al.
  2011; **no abrimos el trabajo primario**. `[R]`
- ***Laodelphax striatellus*** (delfácido, Hemiptera: Delphacidae). Los siRNA derivados del
  virus HiPV son de **21-22 nt** en su mayoría, pero con una distribución ancha de 18 a 30 nt.
  Misma revisión, atribuido a Li J. et al. 2014; tampoco abrimos el primario. `[R]`
- **Cicadellidae**, la familia de *Dalbulus maidis*. **No encontramos ninguna distribución de
  tamaños de siRNA.** La revisión de 2016 lista al único cicadélido con perfil de ARN pequeños,
  *Homalodisca vitripennis*, y lo que reporta de él es perfilado de miRNA y mapeo de siRNA
  virales a los genomas de HoCV-1 y HoVRV, no un histograma de largos de productos de Dicer.
  **Para *Dalbulus maidis* no hay nada.** Este es un vacío documentado, no una omisión nuestra.
  `[E]` la ausencia en lo que revisamos; `[?]` si existe en literatura que no alcanzamos.

El marco general que la misma revisión da para insectos —miRNA típicamente 22 nt, endo-siRNA
21 nt, piRNA 24-30 nt— es consistente con todo lo anterior y marca dónde están las excepciones
reales: **los piRNA, que no requieren Dicer y miden 24-30 nt**, y que en un hemíptero pueden
ser la clase dominante. `[E]`

### A.4 Las excepciones, y por qué no rescatan a 18 nt

Las excepciones al 21 que encontramos van **hacia arriba** (22 nt en himenópteros, ortópteros y
mosca blanca; 24-30 nt en la vía de piRNA) o a 20 nt en lepidópteros. **Ninguna va a 18.** La
afirmación del investigador —«si pones 18, no hay molécula funcional que funcione»— es
consistente con todo lo que abrimos: no hay en la literatura que revisamos ninguna Dicer de
insecto que produzca un siRNA de 18 nt como producto mayoritario. `[E]`

Esto no dice que un bloque de 18 nt compartido no tenga ninguna consecuencia: dice que **18 no
es el largo de una molécula, es un fragmento de una de 21 o 22**. Qué efecto tiene un
apareamiento parcial de 18 nt dentro de un siRNA de 21 es una pregunta distinta, y la respuesta
conocida apunta a otro mecanismo: el silenciamiento fuera de blanco mediado por la región
semilla (posiciones 2 a 8 de la hebra guía), que necesita **6 a 8 nt** de complementariedad, no
18. Jackson et al. 2006, *RNA* 12:1179 (`10.1261/rna.25706`), del que sólo pudimos abrir el
resumen y cuyo sistema es cultivo de células humanas. `[R]`

## Parte B — El benchmark computacional, 21 contra 22

### B.1 El largo de ventana sí es parámetro del port, y hay una letra chica

`tools/sifi21_port/` expone el largo de ventana como parámetro: `DEFAULTS["sirna_size"] = 21`
y `SifiEngine(mode=..., sirna_size=k)`, que se propaga al corte de ventanas, al cálculo de ΔG
de extremos y a la llamada a RNAplfold. **No hubo que tocar el port**: el script
[`scripts/q2_ventana_21_vs_22.py`](scripts/q2_ventana_21_vs_22.py) lo importa y le pasa
`sirna_size=22`.

Dos advertencias que hay que leer junto con los números:

1. **La regla de nucleótidos terminales se generaliza, no se valida.** El original mira el
   nucleótido 19 y el 2 de una ventana de 21; el port lo implementa como `sirna[size-3]` y
   `sirna[1]`, de modo que con `sirna_size=22` mira el nucleótido 20. Es «el tercero desde el
   final», que es la lectura razonable, pero **no es una regla que alguien haya validado para
   22 nt**. `[H]`
2. **El backend no es el de si-Fi21.** La verificación de W5 contra el programa original usó el
   `RNAplfold.exe` de ViennaRNA 2.1.5 que instala si-Fi21, que es un ejecutable de Windows y no
   corre acá. Usamos las ligaduras de Python de **ViennaRNA 2.7.2**, con el que el modo fiel a
   21 nt da 35, 39, 142 y 223 ventanas eficientes contra las 42, 32, 133 y 212 verificadas con
   2.1.5. **Los conteos absolutos no son comparables con los de W5**; lo que se compara acá es
   21 contra 22 con el mismo backend, y para eso la diferencia de versión se cancela. `[E]`

`offtarget_21nt.py`, el otro módulo del port, **no** tiene el largo como parámetro: `SIZE = 21`
y `MIN_BLOCK = 19` son constantes de módulo. Para el tamizaje a 22 nt habría que cambiarlas, y
no lo hicimos.

### B.2 Resultado

Modo **corregido** (el que el equipo usa para diseñar), ViennaRNA 2.7.2, los cuatro genes de
EPILAB completos. Comando:

```bash
python research/ola3/C3_blast_ventana_azar/scripts/q2_ventana_21_vs_22.py \
       --salida research/ola3/C3_blast_ventana_azar/resultados
```

| Gen | Largo | Eficientes 21 | Eficientes 22 | Δ | Inicios compartidos | Jaccard de inicios | Jaccard de nt cubiertos | ρ de Spearman del perfil de regiones |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ATPaseD_Dm | 491 | 29 | 32 | +10,3 % | 17 | 0,386 | 0,813 | 0,960 |
| CP_MRFV | 528 | 30 | 29 | −3,3 % | 10 | 0,204 | 0,735 | 0,925 |
| MP_MRFV | 1.263 | 123 | 123 | 0,0 % | 66 | 0,367 | 0,826 | 0,740 |
| BicC_Dm | 2.520 | 171 | 174 | +1,8 % | 83 | 0,317 | 0,778 | 0,927 |

Modo **fiel**, mismos genes: 35→40 (+14,3 %), 39→30 (−23,1 %), 142→136 (−4,2 %), 223→210
(−5,8 %). Tabla completa, incluida la del modo fiel, en
[`resultados/q2_21_vs_22.tsv`](resultados/q2_21_vs_22.tsv); el detalle por ventana de las 16
corridas en `work/C3/q2/`.

### B.3 Qué cambia en la región más densa — y acá está el resultado

| Gen (modo corregido) | Mejor región a 21 nt | Eficientes | Mejor región a 22 nt | Eficientes | Puesto de la mejor región de 21 en el ranking de 22 |
| --- | --- | ---: | --- | ---: | ---: |
| ATPaseD_Dm | 272-471 | 19 | 87-286 | 21 | (fuera del dominio de 22) |
| CP_MRFV | 99-298 | 21 | 77-276 | 22 | **6.º** |
| MP_MRFV | 72-271 | 38 | 820-1019 | 32 | **23.º** |
| BicC_Dm | 1022-1221 | 25 | 2013-2212 | 26 | **166.º** |

**El conteo total casi no se mueve y el ranking de regiones sí.** En los cuatro genes el número
de ventanas eficientes cambia menos del 11 % en modo corregido, y el perfil de densidad por
región de 200 nt está muy correlacionado entre los dos largos (ρ de Spearman 0,74 a 0,96). Pero
en dos de los cuatro genes —MP_MRFV y BicC_Dm, que son los largos— **la región de 200 nt que
sale primera cambia de lugar del gen**: de 72-271 a 820-1019 en MP_MRFV, y de 1022-1221 a
2013-2212 en BicC_Dm. En BicC_Dm la región que gana con ventana de 21 cae al puesto 166 con
ventana de 22. `[E]`

La razón es que el argmax de una ventana deslizante sobre un perfil con muchos picos de altura
parecida es **inestable**: con 171 y 174 eficientes repartidas en 2.520 nt, la diferencia entre
el primer y el segundo lugar es de unas pocas ventanas, y basta correr el largo un nucleótido
para que se den vuelta. En ATPaseD_Dm y CP_MRFV, que son cortos y tienen un único pico, la
elección es estable: la región de 22 nt solapa casi completamente con la de 21.

> **Lectura para el diseño.** Si la región se elige por el argmax de densidad, el resultado
> depende de una decisión —21 contra 22— que para la chicharrita **no está resuelta por la
> biología**, porque no hay dato de Cicadellidae y el hemíptero mejor caracterizado apunta a
> 22. Nuestra recomendación es no entregar un argmax: entregar el conjunto de regiones que
> quedan en el **top-5 con los dos largos**, que es un criterio estable y declarable, y usar el
> solapamiento por nucleótidos cubiertos (0,74 a 0,83 en modo corregido) como la medida honesta
> de cuánto comparten las dos elecciones. `[H]`

### B.4 Lo que este benchmark no contesta

No mide eficacia: mide el criterio de si-Fi21, que es un filtro termodinámico y de
accesibilidad, no un predictor validado. Que una región tenga más ventanas «eficientes» a 22 nt
no dice que un ARNdc contra ella silencie más. Y el conteo a 22 nt arrastra la generalización
de la regla terminal descrita arriba, que nadie validó.
