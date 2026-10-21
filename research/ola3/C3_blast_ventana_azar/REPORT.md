# C3 — BLAST para ventanas de 21 nt, el largo de la ventana, y qué parte de las coincidencias es azar

Ola 3 · sale del Checkpoint 1 · tres preguntas de tamizaje de off-targets, resueltas con
medición propia y literatura abierta.

Todo lo medido corre en esta máquina con **BLAST+ 2.17.0+** (build del 22 de agosto de 2026,
Bioconda, entorno `w5bio`), **ViennaRNA 2.7.2** y **Python 3.11**. Ninguna secuencia de EPILAB
salió de la máquina. Los tres documentos de detalle son
[`blast_parametros.md`](blast_parametros.md), [`ventana_21_vs_22.md`](ventana_21_vs_22.md) y
[`azar_vs_real.md`](azar_vs_real.md); los scripts y las salidas crudas están en
[`scripts/`](scripts/) y [`resultados/`](resultados/).

---

## Las tres respuestas

### Q1 — El parámetro, y la configuración correcta

**«HCP» es casi con seguridad «HSP», pero no es un parámetro: es la unidad de resultado de
BLAST.** `[H]` El texto de ayuda de `blastn` 2.17.0 usa la sigla en tres parámetros que sí
existen —`-max_hsps`, `-qcov_hsp_perc` y `-sorthsps`— y ninguno de ellos es el que decide sobre
una ventana de 21 nt. `[E]`

**El que decide es `-word_size`,** y la razón es que gobierna si el alineamiento se intenta
siquiera. Un 21-mero con un desajuste en la posición *p* queda partido en dos bloques exactos
de *p*−1 y 21−*p* nucleótidos; si ninguno llega al tamaño de palabra, BLAST no siembra y el
acierto no existe. El `megablast` por defecto usa palabra **28** y por eso da **sensibilidad
cero en las 21 posiciones**. `-task blastn` usa **11** y pierde exactamente la posición 11.
Hace falta `word_size ≤ 10 = ⌊(21−1)/2⌋`; bajar de 10 a 8, 7 o 4 **no agrega nada** y cuesta
veinte veces más tiempo. `[E]`

**Y aun así ninguna configuración lo logra.** Medimos trece configuraciones sobre 3.150
consultas con desajustes plantados en cada posición. El techo es **0,762** (`-task blastn`) y
**0,619** (cualquier `blastn-short`). Lo que falta no es semilla: es que la **extensión con
corte X recorta un desajuste cercano al extremo en vez de cruzarlo**, porque cruzarlo no paga.
Con premio 1 y penalidad −3 hacen falta ≥ 4 calces del otro lado y se pierden las posiciones
1-4 y 18-21 (13/21 = 0,619); con premio 2 y penalidad −3 alcanzan 2 y se pierden 1, 2, 20, 21
más la 11 (16/21 = 0,762). **La fórmula predice las dos columnas enteras.** El criterio de
éxito del encargo —una configuración que no pierda ninguna posición— **no se puede cumplir con
BLAST**: para este tamizaje hace falta coincidencia exacta con presupuesto de desajustes, que
es lo que ya hacen Bowtie y el `offtarget_21nt.py` del repositorio. `[E]` los números, `[H]` la
conclusión.

Un hallazgo adicional que cambia la práctica: a escala de genoma el **E-value sí decide**. En
5 Mb, pedir `-evalue 0.05` —el valor por defecto del formulario web del NCBI— no cambia nada;
contra los 972 Mb del genoma de *Dalbulus maidis* lleva la sensibilidad de **0,619 a 0,000**.
`[E]`

Configuración recomendada, con su postfiltro obligatorio:

```bash
blastn -task blastn-short -word_size 10 -ungapped -dust no -soft_masking false \
       -evalue 1000 -max_target_seqs 5000 -query ventanas.fa -db referencia \
       -outfmt "6 qseqid sseqid pident length mismatch gapopen sstart send evalue bitscore" \
 | awk -F'\t' '$4>=20 && $5<=1 && $6==0'
```

### Q2 — 21 o 22, y por qué no menos

**El largo lo fija la geometría de la enzima.** Dicer corta a una distancia fija del extremo
del dúplex porque el dominio PAZ lo ancla y los centros catalíticos RNasa III están a una
separación física determinada: el modelo de la regla molecular de Macrae et al. 2006
(*Science* 311:195-198, **sólo resumen abierto**). No es una convención de software: pedir 18
no es relajar un parámetro, es pedir una molécula que la enzima no produce. `[E]`

**En insectos el largo es 20, 21 o 22 según el orden, y está medido.** Santos et al. 2019
(*Viruses* 11:738): dípteros y coleópteros 21 nt; himenópteros y ortópteros 22 nt; lepidópteros
20 nt. Zotti et al. 2026 (*Viruses* 18:285) correlaciona eso con distancias PAZ–RNasa III
modeladas de 58,3 a 62,3 Å. `[E]` lo experimental, `[R]` lo estructural, que es modelado.

**Ninguno de los dos incluye un solo hemíptero.** Verificado sobre los textos completos. Lo que
hay de Hemiptera apunta a los dos lados: en la mosca blanca *Bemisia tabaci* el pico de
productos de Dicer está en **22 nt** y son las lecturas de 22 las que muestran la firma de
voladizo de 2 nt (Mondal, Brown y Flynt 2020); en un psílido el ARNdc se procesa a **21 nt** y
en un delfácido los siRNA virales son de **21-22 nt** (los dos vía la revisión de Sattar y
Thompson 2016, sin abrir el primario). **Para Cicadellidae, la familia de la chicharrita, no
hay ninguna distribución de tamaños publicada que hayamos podido encontrar.** `[E]` el vacío en
lo revisado.

**El benchmark computacional.** Con el criterio de eficiencia del port de si-Fi21 sin modificar
—`sirna_size` sí es parámetro— sobre los cuatro genes: el conteo de ventanas eficientes cambia
menos del 11 % en modo corregido y el perfil de densidad por región de 200 nt correlaciona
fuerte (ρ de Spearman 0,74 a 0,96). **Pero en los dos genes largos la región elegida se muda de
lugar del gen**: MP_MRFV pasa de 72-271 a 820-1019 y BicC_Dm de 1022-1221 a 2013-2212, y la
región ganadora a 21 nt cae al **puesto 166** en el ranking a 22 nt. El cambio de largo es una
variación chica en el total y una variación grande en la decisión. `[E]`

### Q3 — Cuántas coincidencias da el azar y cuántas hay de verdad

Medido para k de 16 a 22 contra el genoma de *D. maidis* (972 Mb), el transcriptoma de *Zea
mays* (163 Mb) y el de *Apis mellifera* (99 Mb), con búsqueda exacta y con un control barajado
que conserva los dinucleótidos de cada gen y no tiene homología.

**La intuición del investigador falla en el total.** Para secuencias sin homología, el número
total de coincidencias exactas en el genoma real es **el que predice el modelo**: razones
observado/esperado de **1,235, 1,197, 1,016, 1,035 y 1,000** para k de 16 a 20 con un Markov de
orden 5 ajustado a la propia referencia. El uniforme `2N/4^k` se queda corto por un factor de
1,7 a 4,3 en maíz, que es sesgo de composición y el Markov lo corrige. **La cuenta de
probabilidad pura no está rota; está sin corregir por composición, y el error es un factor
chico, no órdenes de magnitud.** `[E]`

**Y acierta en la distribución, que es lo que importa.** En el genoma, con k = 16, el azar
predice que el **36,4 %** de las ventanas tendría al menos una coincidencia y lo observado es
**15,9 %**. Al mismo tiempo el total coincide. La razón: la varianza del conteo es **66 veces
la media** y un solo 16-mero del control barajado aparece **325 veces**. Las coincidencias no
se reparten, se amontonan sobre los k-meros que caen en familias repetidas. **Hay las mismas
coincidencias que predice la estadística, repartidas entre menos ventanas.** `[E]`

**Y el salto de 16 a 17 de nuestra tabla es la saturación de una exponencial, no un umbral.**
El número esperado de aciertos por ventana de 21 nt con umbral k es
`λ(k) = (21−k+1)·2N/4^k`, y la fracción tocada es `1−e^(−λ)`, que es casi λ mientras λ es chico
y se satura cuando λ pasa de 1. Entre 21 y 18 nt λ va de 0,0004 a 0,11 y la supervivencia
medida en el control va de 99,9 % a 95,6 %: parece plana. Entre 17 y 16, λ va de 0,57 a 2,72 y
la supervivencia cae de 82,8 % a 54,5 %. **El salto está donde λ cruza 1, y para una referencia
de 10^8 a 10^9 bases eso cae exactamente entre 16 y 17.** Para el catálogo de 752 MB del
pipeline la cuenta da supervivencias de 12,2 %, 64,6 % y 91,6 % a 16, 17 y 18 nt, que es la
forma de la tabla medida (7,4 %, 36,2 %, 66,7 %). `[E]` la cuenta, `[H]` la correspondencia con
esa tabla, que se midió sobre otro conjunto.

---

## Cierre de juicio `[H]`

Lo que sigue es opinión del equipo apoyada en lo medido arriba, no evidencia.

**Qué umbral mínimo de coincidencia contigua conviene usar.** Conviene **21 nt con hasta un
desajuste, y 19 nt perfecto como segundo criterio**, que es lo que el repositorio ya hace en
`offtarget_21nt.py`. El argumento es ahora cuantitativo y no una preferencia: a 19 nt y más, en
el control sin homología, la razón observado/esperado es 1,0 y el número absoluto de
coincidencias por azar en el genoma entero es de **25 sobre 4.730 ventanas**; a 16 nt son
1.979, y de esas el 100 % es azar por construcción del control. **Todo lo que se gana bajando
de 19 a 16 es ruido medido, no riesgo detectado.**

**Qué ventanas de 16 a 18 nt tiene sentido reportar y cuáles no.** No tiene sentido reportar
una coincidencia de 16, 17 o 18 nt como un off-target: a esos largos el azar explica el total.
Sí tiene sentido reportarlas en dos casos acotados, y en los dos el valor viene de que son
**anómalas respecto del azar**, no de que sean largas:

1. **Cuando la misma ventana acumula coincidencias muy por encima de la media.** Un 16-mero con
   decenas o cientos de apariciones no está marcando homología: está marcando que el candidato
   cae en una familia repetida. Eso es una señal de diseño —conviene correrse de ahí— y no una
   señal de off-target.
2. **Cuando el bloque de 16-18 nt cae en el extremo 5' de la hebra guía.** La región semilla,
   posiciones 2 a 8, es la que gobierna el silenciamiento fuera de blanco de tipo miRNA
   (Jackson et al. 2006, resumen, en células humanas). Pero eso necesita 6 a 8 nt de
   complementariedad, no 18: **bajar el umbral a 16 nt no aproxima ese riesgo, porque un calce
   de 7 nt aparece en todas partes.** El riesgo de semilla no se tamiza con un umbral de largo;
   es un vacío de método que hay que declarar, no tapar.

**Y una advertencia sobre lo que no se puede concluir.** Nuestros k ≥ 21 del control barajado
tienen 0 a 4 coincidencias contra esperados de 0,05 a 2: con esos números no se puede afirmar
ni un exceso ni un déficit. Todas las conclusiones de Q3 se apoyan en k de 16 a 20. Y la
sensibilidad de BLAST en las referencias reales se midió con n = 15 por posición, no 150: el
patrón se repite idéntico al de la base sintética, pero los decimales de esas dos columnas no
son firmes.

## Puntos de enganche para el ranking

Tres cosas medidas que se pueden convertir en columna o en advertencia, sin trabajo nuevo de
investigación:

**Columna «razón observado/esperado» por candidato.** Para cada ventana, el cociente entre las
coincidencias exactas observadas en una referencia y las esperadas bajo el Markov de orden 5
ajustado a esa referencia. Es adimensional, compara entre referencias de tamaño distinto, y
separa en un solo número lo que es homología de lo que es composición: una ventana con razón
cercana a 1 contra el maíz no tiene parentesco con el maíz aunque tenga coincidencias. El
escáner que la calcula ya está escrito ([`scripts/kmers.py`](scripts/kmers.py)) y procesa el
genoma de 972 Mb en 61 s.

**Columna «concentración» o bandera de repetición.** El número de apariciones de la ventana en
el genoma del propio vector. Un 21-mero del candidato que aparece decenas de veces en el genoma
de *D. maidis* está en una familia repetida, y eso predice problemas de especificidad que el
conteo de off-targets en otras especies no ve. En nuestra muestra de Q1, de 15 21-meros
tomados al azar del genoma, uno aparecía **68 veces** y nueve una sola vez.

**Advertencia de método en el reporte del tamizaje.** Si en algún momento el tamizaje se corre
con BLAST, el reporte tiene que decir que la sensibilidad por posición del desajuste **no es
uniforme**: con `blastn-short` se pierden las posiciones 1-4 y 18-21, y las posiciones 2, 3 y 4
están dentro de la región semilla. Un «cero off-targets» obtenido con BLAST no es un cero
medido; es un cero con un sesgo conocido y cuantificado. Y si alguien corre el BLAST web con
sus valores por defecto contra algo del tamaño de un genoma, el resultado es **cero por
construcción**.

## Lo que no pudimos hacer

- **El apéndice oficial de parámetros de BLAST+** (tabla C2 de `NBK279684`) no se pudo abrir:
  `www.ncbi.nlm.nih.gov/books/` devuelve reCAPTCHA a un cliente programático. No se falseó el
  user-agent ni se usó espejo. Se reemplazó por medición directa sobre el binario, que es
  evidencia más fuerte, y por el texto de ayuda de `blastn -help`, que sí es documentación
  oficial.
- **Macrae et al. 2006 y Jackson et al. 2006**: cerrados; sólo resumen.
- **Wuriyanghan et al. 2011 y Li J. et al. 2014**, los dos datos de Hemiptera que no son la
  mosca blanca, se citan **vía la revisión de 2016**, sin abrir el primario.
- En el genoma de *D. maidis* no se corrieron las configuraciones de BLAST con palabra ≤ 8 por
  costo de cómputo, y la sensibilidad en las dos referencias reales se midió con 15 fuentes por
  posición en vez de 150.
- El benchmark de Q2 usa ViennaRNA 2.7.2 y no el RNAplfold 2.1.5 que instala si-Fi21, de modo
  que sus conteos absolutos **no son comparables** con los verificados en W5.

## Reproducir todo

```bash
conda activate w5bio
cd /Users/joaquin/Documents/investigaton/chicharrita-research
S=research/ola3/C3_blast_ventana_azar
python $S/scripts/q1_blast_mismatch.py   --salida $S/resultados   # ~10 min
python $S/scripts/q2_ventana_21_vs_22.py --salida $S/resultados   # ~1 min
python $S/scripts/q3_azar_vs_real.py     --salida $S/resultados   # ~6 min
python $S/scripts/q3b_salto_16_17.py     --salida $S/resultados   # ~10 s
```
