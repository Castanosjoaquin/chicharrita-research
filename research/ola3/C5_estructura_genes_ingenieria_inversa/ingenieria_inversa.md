# El circuito de ingeniería inversa, contrastado y corrido

Investigación C5 de la ola 3. Corridas del **20 de octubre de 2026**, todas locales, sobre el
material que W4 bajó del NCBI (`work/W4/downloads/`, fuera de git). Marcadores según `CLAUDE.md`.

---

## La respuesta, antes de todo

**El circuito que describió el investigador es la práctica estándar, y la parte que él marcó como
la crítica —chequear identidad en cada paso— es efectivamente donde se rompe.** Lo corrimos de
punta a punta sobre un gen nuevo y medimos los tres puntos de falla: el umbral de 99 % de identidad
que él propuso como señal de conservación **no se alcanza casi nunca entre géneros de cicadélidos**
(244 de 12.540 loci, el 1,9 %, con una mediana de 0,866); buscar el gen **por nombre** en el
transcriptoma de la especie cercana devuelve un gen distinto del que devuelve la homología, con un
65 % de diferencia en el conteo de ventanas eficientes; y la secuencia recuperada en la especie
cercana **no sirve para diseñar**, porque entre el 0,7 % y el 11,1 % de sus ventanas de 21 nt
existen idénticas en el genoma de *Dalbulus maidis*.

**Sobre 384 o 684: no es ninguna de las dos, y eso ya estaba resuelto en la memoria del proyecto
antes de que esta investigación corriera su conteo.** `00_meta/PREGUNTAS_ABIERTAS.md` registra la
adjudicación —ninguna de las dos cifras corresponde a una cantidad producida por el equipo— y
`research/checkpoints/checkpoint1.md` ya lleva la corrección. Lo que C5 agrega es una **quinta
cifra, producida con un comando reproducible y con la referencia que el propio circuito pide**: con
el proteoma anotado de un cicadélido, el circuito recupera **12.540 loci distintos** en el genoma no
anotado del vector, a partir de 32.269 de 34.269 proteínas consulta. El detalle y el porqué de que
«genes recuperados» no tenga un número único está en la sección 5.

---

## 1. El circuito, paso por paso, contra la práctica publicada y contra nuestro pipeline

El investigador describió cinco pasos: partir de un gen anotado con papers asociados; correr BLAST
de ese gen en NCBI para ver qué organismos parecidos aparecen; mirar la identidad, donde un 99 %
indicaría conservación entre las dos especies; si la especie cercana tiene transcriptoma, buscar
ahí los genes de interés; y hacer BLAST de esos genes contra el genoma no anotado de la chicharrita
`[R]`.

| Paso del investigador | Práctica estándar | Qué hace `pipeline/` | Qué midió C5 |
|---|---|---|---|
| 1. Gen anotado con papers | igual | catálogo curado a mano en `blancos_hemipteros.py` | se partió de `Rpn6` de *Scaphoideus titanus*, publicado en 2025, con su accesión TSA pública |
| 2. BLAST contra NCBI | BLAST o búsqueda por proteína; para genomas sin anotar, `tblastn` o `miniprot` | `hemip_mapear.py` con `miniprot` | `blastn -task dc-megablast` local contra los dos transcriptomas de cicadélido anotados |
| 3. Mirar identidad; 99 % = conservado | los umbrales dependen del nivel (nucleótido / proteína) y del taxón | pondera la evidencia por distancia filogenética (§2 de su informe) | la identidad entre géneros de cicadélidos es 77-84 % en nucleótidos y 0,866 mediana en proteína; el 99 % es excepcional |
| 4. Buscar en el transcriptoma de la especie cercana | ortología recíproca, no coincidencia de nombre | selección **por nombre** en el proteoma de referencia, con el límite declarado en W4 §6.1 | la selección por nombre devolvió el gen equivocado; la homología corrigió |
| 5. BLAST contra el genoma no anotado | `miniprot` o `tblastn`; completitud con BUSCO | `miniprot` + `resumir_miniprot.py` | 34.269 proteínas → 32.269 con locus → 12.540 loci, en 568 s y 3,7 GB de memoria |

Las dos diferencias de fondo con la práctica publicada no son de herramienta sino de **control**.
La primera es que el circuito no tiene paso de **completitud**: no dice cómo saber si el genoma al
que se le está preguntando tiene los genes. W4 ya lo resolvió para este ensamblado con un sustituto
de BUSCO —97,7 % de ortólogos de insecto recuperados en `ihDalMaid1.1` contra 68,8 % en el borrador
del CIAP-INTA (`research/ola2/W4_genomas/REPORT.md` §2)—, y esa diferencia decide sobre qué
ensamblado tiene sentido correr el circuito `[R]`. La segunda es que el circuito no distingue
**ortólogo de parálogo**: un BLAST devuelve el mejor hit, no el ortólogo, y en familias grandes —la
troponina C tiene al menos cuatro parálogos anotados en *Macrosteles quadrilineatus*; las
subunidades de la V-ATPasa, dieciséis— el mejor hit y el ortólogo pueden no coincidir.

---

## 2. Qué identidades son interpretables, y cuáles no

Ésta es la pregunta que el investigador marcó como la crítica, y tiene tres respuestas distintas
según qué se esté comparando. Conviene no mezclarlas, porque los números no son comparables entre
sí.

**Identidad de nucleótidos entre ortólogos de especies distintas.** Es la que sale de un `blastn` y
la que el investigador asoció al 99 %. Nuestra medición, con el gen `Rpn6` de *S. titanus* contra
los dos transcriptomas de cicadélido anotados: **83,6 % sobre 1.223 nt** contra
*M. quadrilineatus* —misma subfamilia, otro género— y **77,3 % sobre 1.227 nt** contra
*Homalodisca vitripennis* —misma familia, otra subfamilia—. El trabajo que publicó ese gen reporta
**82,9 %** de identidad del ADNc entre *S. titanus* y *Euscelidius variegatus*, que es el mismo
orden `[E]`. **Entre géneros de cicadélidos, un ortólogo se parece entre el 77 % y el 84 %, no el
99 %.** Un 99 % de identidad de nucleótidos entre dos especies distintas no es la señal normal de
conservación: es una anomalía que obliga a preguntarse si no se trata de la misma especie, de
contaminación o de una secuencia depositada dos veces.

**Identidad de proteína en el alineamiento proteína-genoma.** Es la que devuelve `miniprot` y la que
usa nuestro pipeline. Sobre los 12.540 loci recuperados con el proteoma del cicadélido anotado, la
mediana es **0,866**, el decil inferior 0,554 y el superior 0,968. Con corte en 0,8 quedan 8.347
loci; con corte en 0,9, 4.840; **con corte en 0,99, sólo 244, el 1,9 %** (`resultados/conteo_genes_recuperados.json`).
Con la referencia de *Drosophila melanogaster*, el mismo pipeline obtuvo una identidad mediana de
0,545 (`pipeline/REPORT.md` §2): la distancia filogenética de la referencia mueve la mediana
0,32 puntos, que es más que cualquier umbral que uno quiera fijar a mano `[H]`.

**Identidad como predictor de riesgo de ARNi.** Es la única que decide un diseño, y no se mide en
porcentaje promedio sino en tramos perfectos. La literatura abierta que encontramos da tres
referencias, y conviene citarlas juntas porque no coinciden: ARNdc con **más del 80 % de identidad**
con el gen blanco dispara ARNi eficientemente en varias especies de insecto, y **fragmentos de 16 o
más nucleótidos perfectamente apareados, o de 26 o más casi perfectos (con uno o dos desajustes mal
distribuidos), también alcanzan** para inducirlo; para *Diabrotica virgifera virgifera* se requiere
un tramo compartido de 21 nt; y especies de *Drosophila* cercanas entre sí se pueden controlar
selectivamente con ARNdc dirigidos a regiones sin ningún tramo compartido de 19 a 21 nt
(Ripamonti et al. 2022, *Int J Mol Sci* 23(2):765, §3, con las referencias que ese trabajo cita)
`[E]`/`[?]` —el `[?]` es porque las tres afirmaciones conviven en el mismo párrafo sin que nadie
las haya conciliado experimentalmente—.

El trabajo de `Rpn6` de 2025 aplica esa lógica en el formato más útil que vimos: su tabla de diseño
no reporta sólo identidad, sino **número de tramos idénticos de más de 16 nt y largo del tramo más
largo**. Entre *S. titanus* y *E. variegatus*: 82,9 % de identidad, 5 tramos de más de 16 nt,
máximo 29 nt —y el ARNdc silencia en las dos especies—. Contra *Apis mellifera*: 53,7 % y 54,5 %,
**cero** tramos de más de 16 nt, máximo 7 y 6 nt —y no se espera efecto— `[E]`. Es la misma
conclusión que W5 §5 había obtenido por cómputo propio —75 % de identidad distribuida no produce ni
un 19-mero idéntico— ahora con respaldo publicado.

**La consecuencia operativa para el paso 3 del circuito:** mirar el porcentaje de identidad sirve
para decidir si vale la pena seguir, y nada más. Lo que decide es el conteo de tramos perfectos, y
ése hay que calcularlo aparte; el porcentaje que devuelve BLAST no lo contiene.

---

## 3. El paso 4 falla por el nombre: un caso medido

El circuito dice «si esa especie tiene transcriptoma disponible, buscar ahí los genes
interesantes». Buscar **cómo** es el punto fino, y la diferencia es medible.

Partimos del gen que los autores llaman `Rpn6` en *S. titanus* (TSA `GJQL01135962.1`). Buscado
**por nombre** en el proteoma anotado de *M. quadrilineatus*, el candidato obvio es «26S proteasome
non-ATPase regulatory subunit 11» (`XM_054432574.1`), porque en la nomenclatura de UniProt el gen
`Rpn6` de *Drosophila melanogaster* es justamente la subunidad 11 (`Q7KLV9`, `GN=Rpn6`). Buscado
**por homología** con `blastn`, el mejor hit es otro: «26S proteasome non-ATPase regulatory subunit
6-like» (`XM_054426723.1`), con 83,6 % de identidad sobre 1.223 nt, mientras que la subunidad 11 no
aparece entre los primeros cinco hits.

Lo resolvimos con una tercera medición, traduciendo el transcrito publicado y comparándolo contra
proteínas revisadas de UniProt: `blastx` lo ubica en **PSMD6 humano con 45,2 % de identidad sobre
409 aminoácidos** (E = 3·10⁻¹¹⁴) y en **Rpn7 de *Drosophila* con 43,4 % sobre 396** (E = 4·10⁻¹⁰⁸),
contra apenas **20,4 % sobre 167 aminoácidos** para PSMD11/Rpn6 (E = 4·10⁻⁴). Por secuencia, **el
gen silenciado en ese trabajo pertenece a la familia PSMD6, que en la numeración Rpn de UniProt es
`Rpn7` y no `Rpn6`** `[?]`. No adjudicamos si el error está en el nombre del paper, en la anotación
automática del transcriptoma de *S. titanus* o en una convención distinta: lo que afirmamos es la
medición. El resultado experimental del trabajo no cambia —el ARNdc se diseñó sobre ese transcrito
y ese transcrito se silenció—, pero **el gen que hay que buscar en *D. maidis* es el que indica la
secuencia, no el que indica el nombre**.

Cuánto cuesta equivocarse: sobre el ortólogo elegido por homología, si-Fi21 cuenta **98 ventanas
eficientes de 1.331** y su mejor región de 200 nt es 289-488 con 25; sobre el elegido por nombre,
**162 de 1.412** y la mejor región es 579-778 con 41. Un 65 % de diferencia en el número que el
laboratorio usa para decidir, por elegir el gen con el criterio equivocado `[H]`.

Y cuesta además apuntar a otro lugar del genoma. Cerrando el paso 5 con los dos candidatos a la
vez (`resultados/rpn6_en_dmaidis.gff`), el ortólogo elegido por homología cae en
**`OZ319707.1:3.659.542-3.665.386 (+)`**, con identidad proteica de **0,978** y sus dos isoformas
coincidiendo en el mismo locus, mientras que el elegido por nombre cae en **otro cromosoma**,
`OZ319708.1:67.220.266-67.221.513 (−)`, con identidad 0,971. **Los dos existen en *D. maidis*, los
dos están bien recuperados, y son genes distintos** `[H]`.

Esos loci permiten medir la pregunta del 99 % sobre **un solo par de genes y las dos escalas a la
vez**, que es lo que faltaba. Alineando el transcrito del cicadélido anotado contra la región del
genoma del vector que `miniprot` devolvió (`blastn -task dc-megablast` con el locus como sujeto,
`resultados/ortologos_vs_locus_dmaidis.tsv`): el ortólogo elegido por homología alinea en **seis
bloques exónicos con identidades de nucleótidos de 83,7 % a 88,7 %, 85,7 % ponderado por largo
sobre 1.232 nt alineados**, mientras que su identidad **proteica** en el mismo locus es **0,978**.
El gen elegido por nombre, que es intrónico simple, da un solo bloque de **88,6 % sobre 1.248 nt**
contra **0,971** de identidad proteica.

Es decir: **para el mismo par de genes y la misma pareja de especies, la identidad salta de ~86 % en
nucleótidos a ~98 % en proteína**. Un 99 % es plausible en proteína para un gen muy conservado
entre cicadélidos —el proteasoma lo es— y no se alcanza en nucleótidos entre especies distintas. Si
lo que el investigador mira en la salida de BLAST es identidad de nucleótidos, el umbral de 99 %
descarta ortólogos verdaderos; si es identidad de proteína, acepta genes cuyo ARNdc no compartiría
casi ningún 21-mero —y de hecho, de las 1.331 ventanas de ese ortólogo sólo 9 existen idénticas en
el genoma del vector—. Es la misma confusión que el proyecto ya había identificado entre homología
y riesgo de ARNi, ahora medida de punta a punta sobre un gen.

---

## 4. El paso 5, corrido entero, y qué tan lejos llega

Comando, tal cual corrió (`scripts/01_recuperar_genes_miniprot.sh`):

```
miniprot -t 9 -d work/C5/miniprot/dmaidis.mpi \
    work/W4/downloads/GCA_975739785.1/.../GCA_975739785.1_ihDalMaid1.1_genomic.fna
miniprot -t 9 --gff work/C5/miniprot/dmaidis.mpi \
    work/W4/downloads/GCF_028750875.1/.../protein.faa > macrosteles_vs_dmaidis.gff
python3 pipeline/resumir_miniprot.py macrosteles_vs_dmaidis.gff --csv loci_macrosteles.csv
python3 scripts/05_contar_genes_recuperados.py loci_macrosteles.csv
```

Salida: **49.202 alineamientos** a partir de **34.269 proteínas** de *M. quadrilineatus*, de las
cuales **32.269 encontraron al menos un locus (94,2 %)**, con **30.391 loci sin corrimiento de
marco ni codón de parada interno**. El alineamiento tardó **567,9 segundos** con 9 hilos y 3,71 GB
de memoria máxima en esta máquina; el índice del genoma de 972 Mb pesa 1,87 GB.

Por qué `miniprot` y no sólo `tblastn`, que es lo que el circuito nombra: `tblastn` alinea una
proteína contra el genoma traducido pero no modela intrones, de modo que un gen de insecto con
diez exones aparece como diez alineamientos sueltos que hay que volver a unir a mano. `miniprot`
devuelve el locus con su estructura de exones en una sola corrida. Es la razón por la que el
pipeline ya lo usaba, y conviene decirlo porque es la única diferencia real entre el circuito
descripto y la práctica actual.

**Hasta dónde llega el resultado.** Recuperar el locus no es recuperar la secuencia que se va a
transcribir. El alineamiento proteína-genoma da coordenadas y estructura exónica aproximada, no los
extremos no traducidos ni las isoformas (W4 §6.1 ya lo había declarado). Y la pregunta siguiente
—si, mientras tanto, se puede diseñar sobre el ortólogo de la especie cercana— tiene respuesta
cuantitativa y es que no: de las ventanas de 21 nt de cada ortólogo, las que existen idénticas en
el genoma de *D. maidis* son 9 de 1.331 para `Rpn6` de *M. quadrilineatus* (0,7 %), 14 de 1.393
para el de *S. titanus* (1,0 %), 58 de 1.487 para `Ruvbl1` (3,9 %), 271 de 4.409 para `XPO1`
(6,1 %) y 203 de 1.835 para la ATP sintasa β (11,1 %), contra 539 de 595 y 398 de 448 para los dos
genes que sí son de *D. maidis* (`resultados/ventanas_y_especificidad.csv`) `[H]`. El contraste
entre 11 % y 90 % es la medida exacta de por qué el paso 5 del circuito es obligatorio y no
opcional.

---

## 5. 384 o 684: qué cuenta cada cifra

La pregunta pedía resolverlo contra nuestros propios resultados, con el comando, y decir qué cuenta
cada número. El resultado tiene dos partes.

**Ninguna de las dos cifras existe en el repositorio.** La búsqueda está guardada en
`resultados/384_684_busqueda.txt`: `grep` recursivo sobre `*.md`, `*.json`, `*.py`, `*.html` y
`*.csv` de todo el árbol versionado, más `git grep` sobre todos los commits. Las únicas apariciones
de «384» son un largo de cloroplasto (140.384 bp), un porcentaje de GC (51,384 %), una coordenada de
un SVG y un conteo de variantes de un paper de otra investigación; «684» no aparece como cantidad de
genes en ningún lado. Esto coincide con lo que `00_meta/PREGUNTAS_ABIERTAS.md` ya tenía registrado
el 20 de octubre: ninguna de las dos corresponde a una cantidad producida por el equipo, la más
parecida a «384» es **438** —los genes del tamizaje de especificidad, una transposición de dígitos
plausible en un audio— y «684» no se parece a ninguna `[E]`.

**Y «genes recuperados» no tiene un número único, que es la razón de fondo por la que la cifra se
pudo decir mal.** El circuito produce cuentas distintas en cada paso, y todas son legítimas:

| Qué se cuenta | Cuántos | Con qué referencia | Dónde se reproduce |
|---|---:|---|---|
| Proteínas consulta con al menos un locus | 2.814 de 3.904 (72,1 %) | *Drosophila melanogaster* | `pipeline/REPORT.md` §2, `hemip_mapear.py` |
| Proteínas consulta con al menos un locus | **32.269 de 34.269 (94,2 %)** | *Macrosteles quadrilineatus* | C5, `scripts/01` y `scripts/05` |
| **Loci distintos** tras fusionar isoformas y solapes | **12.540** | *Macrosteles quadrilineatus* | C5, `scripts/05` |
| Loci en la tabla unificada (varias referencias) | 7.416 | mezcla | `pipeline/REPORT.md` §3 |
| Loci con fenotipo de cribado asociado | 6.295 (84,9 %) | *Tribolium castaneum* como fuente de fenotipo | `tabla_unificada.py` |
| Candidatos de alta confianza | 494 | — | `objetivo_candidatos.py` |
| Genes que entraron al tamizaje de especificidad | 438 | — | `no_objetivo_correr.py` |
| Loci con doble respaldo (cribado **y** ARNi en hemíptero) | 62 | — | `cruzar_hemipteros.py` |

La fila que corresponde a lo que el investigador describió —«mapear contra genomas anotados para
recuperar genes»— es una de las dos primeras, y con la referencia que su propio circuito recomienda
(una especie cercana con transcriptoma) el número es **32.269 proteínas en 12.540 loci**, dos
órdenes de magnitud por encima de 384 o 684. Si lo que se contó en la reunión fue el conjunto
«potencialmente útil» que contiene a los candidatos de EPILAB, la cifra defendible es 494 o 438
según el corte, y las dos están a una transposición de dígitos de 384. **No adivinamos cuál dijo:
lo que corresponde es dejar de usar las dos cifras y citar la tabla.**

---

## 6. Qué le falta al circuito, en orden de cuánto cuesta agregarlo

Lo barato primero. **Resolver la identidad del gen por secuencia y no por nombre** no cuesta nada
—un `blastx` contra UniProt, como el de la sección 3— y evita el error más caro, que es diseñar
sobre el gen equivocado. **Contar tramos perfectos además del porcentaje de identidad** tampoco
cuesta: el repositorio ya tiene la herramienta (`offtarget_21nt.py`) y la literatura ya publicó el
umbral relevante, 16 nt.

Lo que cuesta algo. **Ortología recíproca** en lugar de mejor hit, para las familias con parálogos;
sin eso, cada candidato de una familia grande arrastra un riesgo de off-target intraespecífico que
no está medido. Y **completitud del ensamblado antes de concluir ausencia**: si un gen no aparece,
hay que poder distinguir «no está en el genoma» de «no está en esta versión del ensamblado», y para
eso el sustituto de BUSCO de W4 ya está corrido.

Lo que no se resuelve con cómputo. **El transcriptoma del vector.** Mientras no exista, el circuito
entrega loci y no transcritos, y el diseño de una ventana de 21 nt con precisión de nucleótido
—que es lo que el laboratorio necesita— se hace sobre una secuencia que todavía hay que ensamblar.
Es el mismo cuello de botella que W4 identificó como camino crítico, y esta investigación lo
confirma desde el otro lado: con el ortólogo de la especie cercana sólo transfiere entre el 0,7 % y
el 11 % de las ventanas.
