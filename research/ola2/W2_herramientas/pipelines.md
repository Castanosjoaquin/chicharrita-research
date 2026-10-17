# pipelines.md — el flujo de cada herramienta, paso a paso

Los formatos que circulan entre pasos están puestos tal como los vimos, no como
los supondríamos. Cuando un paso no se pudo verificar, está dicho.

---

## 1. dsRNAEngineer — flujo II (gen blanco provisto por el usuario)

Es el que corrimos, con el proyecto `6fab2304bf273f5e`.

**Paso 1 — Entrada.** El usuario pega FASTA o sube un archivo `.fa/.fasta/.fna`
de hasta 1 MB. *Formato que sale:* JSON a `POST /v1/api/project/design` con
`uid` (epoch en ms más un dígito; un UUID devuelve 500), `name`, `sequence`
(texto FASTA completo, con encabezado), `conserved_list`, `off_target_list`,
`email`, `parent_id`. Cada especie de las listas viaja como objeto con
`species_id`, `match_id`, `match_length`, `match_mismatch` y `option`
(los dos tamaños adicionales con su presupuesto de desapareamientos).

**Paso 2 — Selección de especies.** Hasta 10 on-target y 10 off-target por
corrida para usuarios sin privilegios. El modelo de coincidencia no lo elige el
usuario: viene atado a la especie (Model I = 21 pb, II = 22 pb, III = 20 pb),
salvo en modo personalizado (`match_id` 999), que permite 20/21/22 pb como
condición mayor y dos condiciones libres de 14 a 27 pb con 0 a 2
desapareamientos.

**Paso 3 — Troceado en ventanas.** El servidor corta la secuencia en ventanas
deslizantes de paso 1 para los tres tamaños del modelo. *Formato que sale:* no se
expone, pero su huella queda en el nombre de consulta de la salida de Bowtie,
`<nombre>_sliding`, con las coordenadas de cada ventana.

**Paso 4 — Alineamiento con Bowtie, una corrida por especie y por tamaño.**
*Formato que sale:* un archivo `<especie>.<k>.bwt` por combinación. En nuestra
corrida: `dalbulus_maidis.16/21/26.bwt`, `zea_mays_l.16/21/26.bwt`,
`apis_mellifera.16/22/26.bwt`. Nueve columnas separadas por tabulación: nombre de
la consulta, inicio y fin de la ventana (1-based, inclusive), hebra, transcripto
blanco, desplazamiento en el blanco, secuencia alineada, cadena de calidades
ficticias y un entero final cuyo significado no confirmamos.

**Paso 5 — Conteo.** Suma sin ponderar de las líneas de los tres archivos por
especie. *Verificado:* 190 (21 nt) + 47 (16 nt) + 0 (26 nt) = 237 on-targets en
*D. maidis*; 70 + 0 + 0 = 70 en *Zea mays*; 67 + 0 + 0 = 67 en *Apis mellifera*.
*Formato que sale:* cadenas de texto del tipo
`"Dalbulus maidis (Model I, 237 on-targets)"` en `GET /v1/api/project/detail`.

**Paso 6 — Ventana deslizante exhaustiva sobre el perfil de conteos.** Por cada
intervalo de tamaño de fragmento de ARNdc (50-100 pb, 100-150, … hasta 650-700),
barre todas las posiciones, produce una secuencia óptima por ventana y reordena
todas para quedarse con las diez mejores. *Formato que sale:* `GET
/v1/api/project/match-result` con `section_length`, `position`, `match_times`,
`target_gene` y `off_target_gene`. **No hay campo de puntaje**, de modo que el
criterio de ordenamiento no es reconstruible desde la salida.

**Paso 7 — Descarga.** `GET /v1/api/project/get-download-url` devuelve la URL y
`project/download-file` entrega un `.tar.gz` con el FASTA de entrada y los nueve
`.bwt`. 5.323 bytes en nuestro caso.

**Paso 8 (opcional) — Multiblanco.** Concatena fragmentos de distintos genes y
reordena la concatenación recalculando los mismos conteos. No lo corrimos.

### Flujo I (screen-target), no corrido

Arranca eligiendo una especie de plaga principal y hasta cuatro co-objetivo,
corre BLAST pairwise a nivel transcriptoma entre ellas, muestra un diagrama de
Venn de genes homólogos y deja fijar los cortes de identidad de secuencia y largo
de acierto; los genes elegidos pasan al flujo anterior. La recomendación del
preprint es identidad ≥ 80 %, y su caso de validación usó ≥ 97 % con largo
≥ 300 pb.

---

## 2. BLAST+ local — el tamizaje que sí podemos correr sobre material propio

**Paso 1 — Base de datos.** `makeblastdb -in <fasta> -dbtype nucl -parse_seqids
-out <db>`. *Formato que sale:* el conjunto de archivos `.n*` de BLASTDB v5, más
el informe de `blastdbcmd -db <db> -info` con número de secuencias y bases.

**Paso 2 — Ventanas.** Generar las ventanas de k nt de paso 1 desde el
transcripto. *Formato que sale:* FASTA con un registro por ventana, con la
posición en el identificador. Es el paso que hay que escribir a mano: BLAST no lo
hace.

**Paso 3 — Alineamiento.** Para una condición de coincidencia de ventana
completa:

    blastn -task blastn-short -query ventanas.fa -db <db> \
           -word_size <k> -perc_identity 100 -ungapped -dust no \
           -evalue 1000 -max_target_seqs 5000 \
           -outfmt "6 qaccver saccver pident length mismatch gapopen sstrand evalue bitscore"

*Formato que sale:* TSV sin encabezado con los campos pedidos.

**Paso 4 — Postfiltro, que no es opcional.** Filtrar por `length == k` y
`mismatch <= m`. Sin este paso el conteo no significa lo que parece: con
`-perc_identity 92` sobre ventanas de 26 nt obtuvimos 827 filas y **ninguna** era
un alineamiento de 26 nt; eran alineamientos de 11 a 16 nt con alta identidad
local.

**Paso 5 — Agregación.** Contar posiciones distintas de la consulta con acierto,
no líneas de salida, y separar «cuántas ventanas» de «cuántos transcriptos».

---

## 3. ViennaRNA — la otra familia de señal (no es del corpus)

**Paso 1.** FASTA o texto plano a `RNAfold`; con `-p` agrega función de partición.
*Formato que sale:* secuencia, estructura en paréntesis y energía libre en
kcal/mol entre paréntesis; con `-p`, estructura del ensamble entre corchetes y
centroide entre llaves, más la frecuencia de la estructura de mínima energía.

**Paso 2.** Dos secuencias por línea a `RNAduplex` para la energía de
hibridación. *Formato que sale:* estructura del dúplex con `&` separando hebras,
coordenadas de cada hebra y la energía en kcal/mol.

**Paso 3.** El juego de parámetros se cambia con `-P <archivo>.par`; el que trae
por defecto equivale a `rna_turner2004.par`, verificado por igualdad del
resultado.

---

## 4. El pipeline combinado, tal como quedaría hoy

De los cinco programas analizados, el flujo que un equipo sin laboratorio puede
armar con material no publicado es este, y el salto entre el paso 3 y el 4 es el
que hoy se da a mano:

1. Transcriptoma de referencia del blanco y panel de no objetivo, armados desde
   el NCBI (trabajo de W4; dsRNAEngineer tiene un panel mucho mejor pero no es
   descargable).
2. Ventanas de k nt del candidato, con k justificado por especie (hoy sin fuente
   para *D. maidis*).
3. Tamizaje de especificidad con Bowtie o con BLAST+ más postfiltro, separando
   condiciones por plausibilidad mecánica y contando posiciones, no líneas.
4. **Hueco**: estimación de eficacia. Ninguna herramienta del corpus la calcula.
   La única señal calibrada en insecto son las cuatro variables de dsRIP, que
   requieren ViennaRNA para dos de ellas.
5. Ordenamiento multiobjetivo con los términos sin colapsar, que es lo que R2
   especificó y lo que el organizador pide como pregunta abierta.
