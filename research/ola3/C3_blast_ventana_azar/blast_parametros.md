# Q1 — Los parámetros de BLAST+ que deciden «cuán parecidas son dos secuencias», y cuál sirve para 21 nt con desajustes

Todo lo que sigue está medido con **BLAST+ 2.17.0+ (build del 22 de agosto de 2026)**, el
mismo binario de Bioconda que instaló la ola 2, en el entorno conda `w5bio` de esta máquina.
La versión sale de `blastn -version` y queda registrada en
[`resultados/blastn_help_2.17.0.txt`](resultados/blastn_help_2.17.0.txt).

## 1. El parámetro que nombró el investigador

La transcripción del Checkpoint 1 escribió «HCP» y dejó anotado que no corresponde a ningún
parámetro conocido. El orquestador propuso como hipótesis que fuera **HSP** (*high-scoring
segment pair*, par de segmentos de alto puntaje). La evaluamos contra la documentación de línea
de comandos del propio binario.

«HSP» **no es un parámetro** de `blastn`: es la unidad de resultado, el alineamiento local que
el programa devuelve. Lo que sí existen son parámetros *sobre* los HSP, y el texto de ayuda de
2.17.0 los nombra con esa sigla textualmente: `-max_hsps` («Set maximum number of HSPs per
subject sequence to save for each query», línea 300-301), `-qcov_hsp_perc` («Percent query
coverage per hsp», línea 298-299) y `-sorthsps` («0 = Sort by hsp evalue», línea 213). `[E]`

Nuestra lectura, marcada como hipótesis porque la transcripción tiene pérdida de audio en ese
tramo y nadie puede confirmar qué dijo: **«HCP» es con alta probabilidad «HSP», y lo que el
investigador describió —«BLAST tiene parámetros propios para decidir cuán parecidas son dos
secuencias»— no es un parámetro único sino el conjunto de la tabla de abajo.** `[H]` El
candidato alternativo, que el investigador haya nombrado directamente el E-value o el percent
identity, no se puede descartar. Queda como pregunta para él.

Lo que sí se puede afirmar sin hipótesis es cuál de todos esos parámetros **decide de verdad**
sobre una ventana de 21 nt, y la respuesta medida es que no es el E-value ni el percent
identity: es el **tamaño de palabra** (`-word_size`), porque gobierna si el alineamiento
siquiera se intenta.

## 2. Tabla de parámetros, con los valores por defecto medidos en el binario

Los valores por defecto por tarea no están impresos en `blastn -help`: el texto de ayuda sólo
da el de `-evalue`, `-dust`, `-soft_masking`, `-max_target_seqs` y `-strand`. El apéndice
oficial que los lista (tabla C2 del *BLAST Command Line Applications User Manual*,
`NBK279684`) **no se pudo abrir desde este entorno**: `www.ncbi.nlm.nih.gov/books/` devuelve
una página de reCAPTCHA a un cliente programático, y no se falseó el user-agent para
esquivarla (regla de entorno). Así que los medimos en el binario, que además es evidencia más
fuerte que la documentación.

**Cómo se midieron.** Se arma un par consulta/sujeto donde el único calce exacto posible es un
bloque plantado de largo *L*, porque el fondo de la consulta usa sólo {A,C} y el del sujeto
sólo {G,T}. Hace falta `-strand plus`: sin eso la hebra menos de la consulta es {T,G} y calza
con el fondo del sujeto, lo que arruina la medición (nos pasó en el primer intento). El menor
*L* que produce un acierto es el tamaño de palabra efectivo. El premio sale del puntaje crudo
de un bloque perfecto (S = L·premio), la penalidad de un bloque con un desajuste central
(S = (L−1)·premio + penalidad) y los costos de hueco de bloques con deleciones de 1, 2 y 3 nt.
Script: [`scripts/q1_blast_mismatch.py`](scripts/q1_blast_mismatch.py), parte A. Salidas crudas
en `work/C3/blast/defaults/`; valores en
[`resultados/q1_defaults_medidos.json`](resultados/q1_defaults_medidos.json). `[E]`

| Parámetro | Qué gobierna | `megablast` (defecto de `blastn`) | `blastn` | `blastn-short` | Qué le hace a una ventana de 21 nt |
| --- | --- | --- | --- | --- | --- |
| `-task` | esquema de semilla, premios y penalidades | `megablast` | — | — | define todo lo demás; el defecto es el peor de los tres para 21 nt |
| `-word_size` | largo de la semilla exacta que hay que encontrar para intentar el alineamiento | **28** (medido) | **11** (medido) | **7** (medido) | **el que decide**: con 28 > 21 no hay semilla posible y la consulta no se alinea nunca |
| `-reward` | puntaje por calce | **1** (medido) | **2** (medido) | **1** (medido) | con la penalidad, decide si la extensión cruza el desajuste o lo recorta |
| `-penalty` | castigo por desajuste | **−2** (medido) | **−3** (medido) | **−3** (medido) | idem |
| `-gapopen` / `-gapextend` | costo de hueco | costo lineal de 2,5 por posición (ver nota) | **5 / 2** (medido) | **5 / 2** (medido) | irrelevante si se usa `-ungapped`, que es lo correcto acá |
| `-evalue` | significancia mínima para guardar un acierto | **10** (ayuda, línea 64-65) | 10 | **1000** (ayuda, línea 64-65; y la exportación de estrategia da `1e3`) | **sí decide, y mucho, cuando la base es grande**: ver §4 |
| `-perc_identity` | identidad mínima **del HSP**, no de la consulta | sin filtro | sin filtro | sin filtro | engañoso: filtra sobre el fragmento alineado, no sobre los 21 nt (ya cuantificado en W2) |
| `-qcov_hsp_perc` | cobertura mínima de la consulta **por HSP** | sin filtro | sin filtro | sin filtro | es el parámetro que *debería* usarse para exigir que el HSP cubra los 21 nt |
| `-max_hsps` | HSP por par consulta-sujeto que se guardan | sin límite | sin límite | sin límite | con el defecto no se pierden copias múltiples dentro de un mismo sujeto |
| `-max_target_seqs` | sujetos distintos que se guardan | **500** (ayuda, línea 314-317) | 500 | 500 | **trunca en silencio** si una ventana corta pega en más de 500 transcriptos |
| `-dust` | enmascarado de baja complejidad de la consulta | `20 64 1` (ayuda, línea 221-223) | `20 64 1` | **`no`** | con las tareas que lo traen prendido, una ventana repetitiva puede enmascararse |
| `-soft_masking` | el enmascarado se aplica sólo a la semilla | `true` (ayuda, línea 232-234) | `true` | `true` | atenúa lo anterior, no lo elimina |
| `-ungapped` | prohíbe huecos | apagado | apagado | apagado | conviene prenderlo: un hueco en un siRNA no es un off-target de 21 nt |

**Verificaciones que respaldan las tres últimas filas.** Un sujeto con tres copias del mismo
bloque de 40 nt devuelve **3 HSP** en las tres tareas, de modo que `-max_hsps` no limita por
defecto. Sin fijar `-perc_identity` ni `-qcov_hsp_perc`, `blastn-short` reportó un HSP de 90 nt
con **90,0 % de identidad** y un acierto con **3 % de cobertura de la consulta**: ninguno de
los dos filtra por defecto. `[E]`

> **Nota sobre los huecos de `megablast`.** Los puntajes medidos para deleciones de 1, 2 y 3 nt
> son 57, 54 y 50. Un modelo afín de enteros (apertura 1, extensión 2) reproduce los dos
> primeros y falla en el tercero (predice 51). Un **costo lineal de 2,5 por posición de hueco**
> (apertura 0) reproduce los tres exactamente si se trunca a entero: 60−2,5 = 57,5 → 57;
> 59−5 = 54; 58−7,5 = 50,5 → 50. Reportamos eso y no un par apertura/extensión. Para `blastn` y
> `blastn-short` el modelo afín cierra con las tres ecuaciones: apertura 5, extensión 2. `[E]`

> **`dc-megablast` no entra en la comparación.** El diseño de bloque contiguo le mide un
> «tamaño de palabra» de 36, que no significa nada: la tarea siembra con una plantilla
> discontinua. La exportación de estrategia del binario registra para esa tarea
> `MBTemplateLength 18`, `WordSize 11` y `WindowSize 40`. Para ventanas de 21 nt no sirve:
> la plantilla de 18 ya ocupa casi toda la consulta. `[E]`

## 3. La medición: sensibilidad por posición del desajuste

**Diseño.** Se toman 21-meros de la propia base de datos, se planta un desajuste en cada
posición 1 a 21, y se mide qué fracción de esas consultas recupera cada configuración **en el
locus de origen** (se exige que el sujeto y las coordenadas coincidan con el lugar de donde
salió el 21-mero; un acierto en otro lado no cuenta). El control de verdad terreno es exacto y
no heurístico: por construcción cada consulta tiene distancia de Hamming 1 con la referencia en
ese locus, y el script lo verifica por comparación de subcadenas en Python antes de correr nada
(`assert` en `consultas_mutadas`). La búsqueda exacta pura, que es `-task blastn -word_size 21`,
se corre como control negativo: da **cero**, porque ningún 21-mero mutado existe idéntico.

Tres criterios de éxito, porque la diferencia entre ellos es el resultado:

- **21/21 con 1 desajuste** — el HSP tiene largo 21, un desajuste y cero huecos. Es lo que uno
  cree que va a obtener.
- **≥ 20 nt con ≤ 1 desajuste** — admite que BLAST recorte un extremo.
- **algún HSP en el locus** — detecta el lugar, aunque sea con un fragmento.

**Escala.** Base sintética: 50 21-meros fuente × 21 posiciones × las 3 bases alternativas =
**3.150 consultas**, n = 150 por posición. Transcriptoma de maíz y genoma de *Dalbulus maidis*:
15 fuentes × 21 posiciones × 1 base alternativa = **315 consultas**, n = 15 por posición
(reducido por costo de cómputo; se declara).

### 3.1 Resultado por posición (base sintética de 5 Mb, n = 150 por posición)

Fracción con éxito **21/21 con 1 desajuste**. Columnas: C1 `megablast` por defecto;
C2 `-task blastn` por defecto; C3 `-task blastn-short` por defecto (palabra 7);
C4 `blastn-short -word_size 11`; C5 `blastn-short -word_size 10`; C9 `blastn-short -word_size 4`;
C10 `blastn -word_size 21` (control exacto).

| Posición del desajuste | C1 (ws 28) | C2 (ws 11, premio 2) | C3 (ws 7) | C4 (ws 11) | C5 (ws 10) | C9 (ws 4) | C10 (ws 21) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 2 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 3 | 0,00 | **1,00** | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 4 | 0,00 | **1,00** | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 5–10 | 0,00 | **1,00** | **1,00** | **1,00** | **1,00** | **1,00** | 0,00 |
| **11** | 0,00 | **0,00** | **1,00** | **0,00** | **1,00** | **1,00** | 0,00 |
| 12 | 0,00 | 0,99 | **1,00** | **1,00** | **1,00** | **1,00** | 0,00 |
| 13–17 | 0,00 | **1,00** | **1,00** | **1,00** | **1,00** | **1,00** | 0,00 |
| 18 | 0,00 | **1,00** | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 19 | 0,00 | **1,00** | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 20 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 21 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| **global** | **0,000** | **0,762** | **0,619** | **0,571** | **0,619** | **0,619** | **0,000** |

La tabla completa, con las tres métricas, las trece configuraciones y las tres bases, está en
[`resultados/q1_sensibilidad_posicion.tsv`](resultados/q1_sensibilidad_posicion.tsv); los
comandos exactos, uno por línea, en
[`resultados/q1_comandos.txt`](resultados/q1_comandos.txt). `[E]`

### 3.2 Qué explica cada cero, y por qué no hay configuración perfecta

Hay **dos** mecanismos de pérdida, y sólo uno es el que la nota de W2 ya había identificado.

**Pérdida por semilla.** Un 21-mero con el desajuste en la posición *p* queda partido en dos
bloques exactos de largo *p*−1 y 21−*p*. Para que la tarea siembre hace falta que el mayor de
los dos llegue al tamaño de palabra. Con palabra 28 nunca pasa (C1 y el `megablast` por defecto
dan cero en todas las posiciones). Con palabra 11, el único caso perdido es *p* = 11, donde los
dos bloques miden 10: es exactamente lo que W2 había anotado en el README del port y acá queda
medido (C2 y C4 dan 0,00 en la posición 11 y 1,00 alrededor). Con palabra ≤ 10 el problema
desaparece, y bajar de 10 a 8, 7 o 4 **no agrega nada**: C5, C3, C6 y C9 dan el mismo 0,619.
El umbral exacto es `word_size ≤ 10 = ⌊(21−1)/2⌋`. `[E]`

**Pérdida por extensión, que es la que no esperábamos.** Aun con semilla, la extensión con
corte X recorta un desajuste cercano al extremo en vez de cruzarlo, porque cruzarlo no paga.
Con premio 1 y penalidad −3 (`blastn-short`) cruzar cuesta 3 y cada calce posterior gana 1, así
que hacen falta ≥ 4 calces del otro lado: se pierden las posiciones 1-4 y 18-21, ocho en total,
y 21 − 8 = 13; 13/21 = 0,619, que es el número medido. Con premio 2 y penalidad −3 (`blastn`)
alcanzan 2 calces: se pierden 1, 2, 20 y 21, más la 11 por semilla, cinco en total, y
16/21 = 0,762, que es el número medido. **La fórmula predice las dos columnas enteras.** `[E]`

Con el criterio laxo de ≥ 20 nt se recuperan las posiciones 1 y 21, porque ahí el HSP sale
recortado a 20 nt perfectos: 0,857 para `blastn` y 0,714 para `blastn-short`. Las posiciones 2,
3, 4, 18, 19 y 20 siguen perdidas.

> **Conclusión del criterio de éxito que fijaba el prompt.** Ninguna de las trece
> configuraciones probadas recupera un 21-mero con un desajuste en **todas** las posiciones.
> El techo medido es 0,762 (`-task blastn`, que pierde la posición 11) y 0,619 para cualquier
> `blastn-short`. El límite no es de parametrización: es del modelo de puntaje de BLAST, que
> por diseño recorta extremos que no pagan. Para este tamizaje **hace falta otro método**:
> coincidencia exacta con presupuesto de desajustes, que es lo que hacen Bowtie y el
> `offtarget_21nt.py` del repositorio, y que no tiene este sesgo por posición. `[H]` la
> conclusión, `[E]` los números.

Esto importa biológicamente y no sólo como curiosidad: las posiciones que `blastn-short`
pierde incluyen la 2, la 3 y la 4, que están dentro de la **región semilla** del siRNA
(posiciones 2 a 8 de la hebra guía), que es donde un desajuste cambia más el perfil de
off-targets. Jackson et al. 2006 (*RNA* 12:1179) muestran que los transcriptos silenciados no
buscados tienen complementariedad en el 3'UTR con la región semilla, y que **meter desajustes
en la semilla no apaga el off-target sino que lo reemplaza por otro conjunto** —de ese
artículo sólo pudimos abrir el resumen, y el sistema experimental es cultivo de células
humanas, no insecto. `[R]`

### 3.3 Lo mismo contra referencias reales

| Base | Tamaño | C1 `megablast` | C2 `blastn` | C3/C8 `short` ws 7 | C4 ws 11 | C5/C12 ws 10 | C10 ws 21 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Sintética uniforme | 5 Mb | 0,000 | 0,762 | 0,619 | 0,571 | 0,619 | 0,000 |
| Transcriptoma de *Zea mays* | 163 Mb | 0,000 | 0,759 | 0,619 | 0,571 | 0,619 | 0,000 |
| Genoma de *Dalbulus maidis* | 972 Mb | 0,000 | 0,762 | no corrida | 0,571 | 0,619 | 0,000 |

El patrón por posición es idéntico en las tres: no depende de la composición ni del tamaño de
la base, lo que era de esperar si el mecanismo es el que describimos. En el genoma no se
corrieron las configuraciones con palabra ≤ 8 por costo de cómputo (se declara en las
desviaciones); la comparación completa de tamaños de palabra está en la base sintética y en el
transcriptoma de maíz.

## 4. El E-value sí decide, pero sólo cuando la base es grande

En la base sintética de 5 Mb, pedir `-evalue 0.05` —que es el valor por defecto del
**formulario web** de `blastn`, documentado en W2— no cambia nada: 0,619 contra 0,619. En el
genoma de *Dalbulus maidis*, de 972 Mb, el mismo filtro lleva la sensibilidad de **0,619 a
0,000** con el criterio estricto y a **0,095** con el criterio de ≥ 20 nt. `[E]`

La razón es aritmética: el E-value escala con el tamaño del espacio de búsqueda, y un HSP de
20 calces y un desajuste tiene alrededor de 34 bits, que contra 972 Mb da un E-value del orden
de 1. Con el umbral de 1000 de `blastn-short` entra; con 0,05 no. **Para tamizaje de ventanas
cortas el E-value hay que fijarlo alto y a mano, y el valor del formulario web es exactamente
el que no hay que usar.**

## 5. La configuración que recomendamos, y su letra chica

```bash
blastn -task blastn-short -word_size 10 -ungapped \
       -dust no -soft_masking false \
       -evalue 1000 -max_target_seqs 5000 \
       -query ventanas_21nt.fa -db referencia \
       -outfmt "6 qseqid sseqid pident length mismatch gapopen sstart send evalue bitscore" \
   | awk -F'\t' '$4>=20 && $5<=1 && $6==0'
```

Es la configuración C12 de la medición. `-word_size 10` es el máximo que no pierde la posición
11, y sale mucho más barato que bajar a 7 sin ganar nada para un desajuste: sobre la base
sintética con 3.150 consultas, `blastn-short` con palabra 10 tarda **2,4 s** y con palabra 7
tarda **46,5 s** (con palabra 4, 102,5 s), y los tres dan la misma sensibilidad de 0,619. En
el genoma de 972 Mb con 315 consultas, la configuración completa tarda **20,7 s**.
`-ungapped` porque un hueco no es un off-target de 21 nt.
`-dust no -soft_masking false` para que una ventana repetitiva no se enmascare.
`-evalue 1000` por §4. `-max_target_seqs 5000` porque el defecto de 500 trunca en silencio.
El postfiltro por `length` y `mismatch` es obligatorio, por lo que W2 ya había cuantificado.

**Y aun así pierde las posiciones 2, 3, 4, 18, 19 y 20.** Si lo que se quiere es el conteo
honesto de 21-meros con un desajuste, la herramienta correcta no es BLAST.

Si el presupuesto de desajustes sube a 2, el tamaño de palabra tiene que bajar a
⌊(21−2)/3⌋ = **6**; con 3 desajustes, a ⌊18/4⌋ = **4**, que es el mínimo que `blastn` acepta
(`-word_size <Integer, >=4>`, línea 66). Con 4 desajustes BLAST ya no puede garantizar la
semilla sobre 21 nt. `[E]` la fórmula del palomar, `[H]` la consecuencia operativa.

## 6. Qué parámetros usa de verdad cada herramienta del corpus

Contrastado con lo que W2 dejó documentado en `research/ola2/W2_herramientas/REPORT.md` y en
`herramientas.json`:

**dsRNAEngineer** no usa BLAST para el tamizaje de off-targets: usa **Bowtie**, con dos campos
por condición (`length` y `mismatch`), y su propio texto de ayuda dice que lo que el usuario
define son «the length and mismatch parameters of bowtie». Las condiciones que corre son 16 nt
perfecto, 20/21/22 nt según la especie, y 26 nt con 0-2 desajustes. BLAST aparece sólo en su
módulo *screen-target*, con el E-value elegido de una lista cerrada de cinco valores
(1e-5 a 1e-1) y una identidad recomendada ≥ 80 %. **Eso coincide con nuestra tabla y la
confirma por el lado que importa**: una lista de E-values que llega hasta 1e-1 es, para
ventanas cortas contra una base grande, mucho más restrictiva que el 1000 que hace falta —ese
módulo no está pensado para ventanas de 21 nt sino para transcriptos enteros. `[E]`

**si-Fi21** tampoco: usa Bowtie para el tamizaje y no toca BLAST. El port verificado en
`tools/sifi21_port/` lo deja escrito en el encabezado de `sifi_core.py`.

**El BLAST web del NCBI**, que es la otra herramienta del corpus, trae por defecto Megablast
con palabra 28 y Expect 0,05, y además una casilla marcada —«Short queries: Automatically
adjust parameters for short input sequences»— que **cambia los parámetros por su cuenta y no
informa cuáles usó**. Con nuestra medición en la mano: la palabra 28 da cero en todas las
posiciones y el Expect 0,05 contra una base grande da cero también. Si el ajuste automático lo
lleva a `blastn-short`, el techo sigue siendo 0,619. `[E]` los defectos, `[H]` la inferencia
sobre el ajuste automático, que no probamos porque no se manda material propio a servicios de
terceros.

## 7. Reproducir

```bash
conda activate w5bio              # BLAST+ 2.17.0+, Bioconda
python research/ola3/C3_blast_ventana_azar/scripts/q1_blast_mismatch.py \
       --salida research/ola3/C3_blast_ventana_azar/resultados
```

Las 25 corridas de tamizaje de la parte B suman **346 s** con 8 hilos; con la parte A, el
muestreo de las referencias y la construcción de la base sintética, la corrida completa ronda
los 10 minutos. Deja `q1_defaults_medidos.json`, `q1_sensibilidad_posicion.tsv`,
`q1_resumen.json` y `q1_comandos.txt` en `resultados/`, y las salidas tabulares crudas de las
**36 invocaciones de `blastn`** y la de `makeblastdb` en `work/C3/blast/`. El archivo
`q1_comandos.txt` tiene los 37 comandos exactos, uno por línea, en orden de ejecución.
