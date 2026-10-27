# F1 — Transferencia de anotación por homología: el transcriptoma del investigador, leído

**Veredicto: el método funciona, pero su regla estricta no pasó el control que ella misma fijó, y
la lectura que se puede usar es una enmienda escrita después de ver el fallo.** Sobre `GITV01`
(56.117 contigs) la regla estricta preregistrada deja **4.110 contigs (7,3 %) con ortólogo
recíproco y nombre informativo** en *Macrosteles quadrilineatus*; la lectura inclusiva de empates,
que sí pasa el control, deja **7.832 (14,0 %)** `[M]`. Todo se corrió en local con `diamond` 2.2.8; ninguna
secuencia salió de la máquina. Fecha: 2026-10-27. Issue #25. Método y umbrales:
`PREREGISTRO.md` (commit `e98877e`, anterior a la primera corrida) y sus dos enmiendas.

## Qué se corrió

El archivo que mandó el investigador, `Dalbulus_maidis_transcriptome_GITV01.fas`, es el TSA
(*Transcriptome Shotgun Assembly*) público de Ohio State: sus 56.117 secuencias y 94.702.486 pb
coinciden con lo que el NCBI publica para `GITV01` y que el repositorio ya había registrado
(`research/ola2/W3_bases_datos/consultas/05_tsa_y_ftp.md`), con md5 `bee70da94d1541fb371f10e4e358b6c8`. Las
cabeceras no traen nombre de gen, como él avisó. La última casilla del criterio de terminado de
F1 preguntaba si este transcriptoma podía ser el mismo que `GHCC01`: **no lo es**, son accesiones
distintas del NCBI, una respuesta por identificador y no por alineamiento.

Cada contig se tradujo en los seis marcos y se tomaron todos los ORF de parada a parada de al
menos 100 aminoácidos (105.871 ORF en 30.305 contigs). Con `diamond blastp --more-sensitive`
(e ≤ 1e-10) se alineó cada ORF contra el proteoma RefSeq de *M. quadrilineatus* (34.269
proteínas, `GCF_028750875.1`) y cada proteína contra el conjunto de ORF, y se exigió que el par
fuera el mejor hit en las dos direcciones. Se repitió contra *Homalodisca vitripennis*
(`GCF_021130785.1`, 31.163 proteínas) como contraste. Los dos proteomas son públicos y se
verificaron contra el `md5checksums.txt` del NCBI. A cada par se le agregó la identidad, las dos
coberturas y la banda de concordancia que `C12` midió para ese tramo de identidad.

## Dónde cae cada contig

La contabilidad cierra en los dos niveles (el script aborta si no suma), y cada contig cae en una
sola categoría, la mejor de las de sus ORF. Las cifras son contra *M. quadrilineatus*.

| categoría del contig | regla estricta (preregistrada) | lectura inclusiva (`[H]`, post hoc) |
| --- | --- | --- |
| a · sin ORF de ≥ 100 aa | 25.812 (46,0 %) | 25.812 |
| b · con ORF, sin hit con e ≤ 1e-10 | 8.261 (14,7 %) | 8.261 |
| c · hit, pero no recíproco | 6.110 (10,9 %) | 10.383 (18,5 %) |
| d · empate en el primer puesto | 10.586 (18,9 %) | 2.266 (4,0 %) |
| e · recíproco, nombre «sin anotación informativa» | 1.238 (2,2 %) | 1.563 (2,8 %) |
| f · recíproco, nombre informativo | 4.110 (7,3 %) | 7.832 (14,0 %) |

La fila a no se explicó: casi la mitad de los contigs no tiene ningún ORF de 100 aa, y no se
midió cuánto es ruido no codificante, cuánto fragmento corto y cuánto contig con marco roto. Está
declarado como pregunta abierta, no como resultado. Las filas e quedan **contadas y no filtradas**,
como pedía el issue: son recíprocos cuyo nombre en RefSeq es *uncharacterized* o *hypothetical*.

Por ORF, la lectura inclusiva da 10.280 recíprocos con nombre informativo, distribuidos por
identidad así: ≥ 90 %, 4.467; 80–90 %, 3.233; 60–80 %, 2.132; 40–60 %, 401; < 40 %, 47. Con la
concordancia de `C12` en cada tramo, el valor esperado sobre esos 10.280 es cerca del **81 %** `[H]`:
una cifra que sólo vale si las bandas de proteoma contra proteoma se pueden aplicar a ORF de un
TSA, que es el supuesto central ~~y no está probado~~ **y quedó probado después** (`D86`,
`validacion_bandas/`): el paso por ORF no degrada la concordancia, y las bandas de `C12` resultaron
ser una **cota conservadora**, de modo que el esperado medido es 87–89 % y no 81 %. **El 81 % se
deja como está** —el preregistro de esa validación prohibía corregir hacia arriba—; lo que cambia
es cómo se lee. La cobertura alta (≥ 70 % en los dos lados)
alcanza a 8.574 de esos 10.280; el resto es parcial (1.400) o fragmento (306) y viaja rotulado,
sin filtrar. ~~Las proteínas de referencia distintas alcanzadas son 9.567 (28 % del proteoma)~~ **Las
proteínas de referencia distintas alcanzadas son 9.567 (27,9 % del proteoma) contando todos los
recíprocos de la lectura inclusiva; si se cuentan sólo los que tienen nombre informativo —el
universo de los 10.280 del que viene hablando este párrafo— son 7.942 (23,2 %)** `[M]`, pero son
proteínas y no genes: RefSeq tiene varias isoformas por gen.

El contraste entre las dos referencias da una consistencia de nombres de **86,3 %** (6.455 de 7.478
ORF recíprocos con nombre informativo en ambas; 84,3 % con la regla estricta, sobre 2.599). Es
consistencia entre anotaciones de RefSeq que ya derivan de homología, no verdad experimental.

## Los controles, y cuál falló

El positivo era la subunidad B de la V-ATPasa en `GITV01003502.1`, conocida por `O2`. **La v1
(un ORF por contig) lo falló:** el contig mide 8.004 nt, la V-ATPasa B es un ORF de 517 aa en la
hebra `+` y hay otro gen más largo en la hebra `-` (622 aa, una vitelogenina); «el ORF más largo»
eligió el otro. Se descartó la v1 y se tomaron todos los ORF (Enmienda 1). **La v2 con la regla
estricta lo falló de nuevo, por otra causa:** el ORF de 517 aa encuentra la V-ATPasa B de
*Macrosteles* con 100 % de identidad y 100 % de la referencia cubierta, pero del lado inverso la
proteína empata en bitscore con otros ORF del transcriptoma y la regla preregistrada lo clasifica
como empate. Con la lectura inclusiva pasa. Que pase **no prueba** que la regla esté bien: la escribí
después de ver el fallo (Enmienda 2).

La cordura con `BicC` (el contig `GITV01000968.1`, que `W5` había identificado por BLAST) da un ORF de
799 aa recíproco con *protein bicaudal C-like*, 88,4 % de identidad `[M]`; no era criterio de éxito.
El señuelo, 1.000 ORF barajados residuo a residuo, dio **0 hits de 1.000** contra las dos
referencias, así que el umbral no deja pasar falsos positivos en esa escala `[M]`; con 0 sobre
1.000 la tasa verdadera puede ser de hasta unos 0,3 % (regla de tres), no cero.

Sobre los empates, lo medido (`resultados/diagnostico_empates.json`): la mitad de los ORF con hit
cae en empate bajo la regla estricta (16.233 de 32.372, 50,1 %), y de los empates del lado inverso
sólo el 53,7 % son copias de secuencia idéntica (el 44,5 % contra *Homalodisca*). El resto son ORF
distintos con el mismo bitscore, así que **no puede decirse que los empates sean simple
redundancia del transcriptoma**. En el lado directo, 8.458 de 11.492 empates son isoformas con el
mismo nombre normalizado `[H]`.

## El cortafuego

La salida no tiene ninguna columna de secuencia de nucleótidos ni de proteína, y las pruebas lo
verifican de dos maneras: un recorrido del AST de todos los `.py` del repositorio falla si alguno
fuera de F1 importa el módulo, y un patrón busca corridas de ≥ 30 nucleótidos en las tablas
versionadas. Eso es una verificación estructural y no una garantía: nada impide que alguien
copie una tabla a mano al diseño. La anotación transferida contesta qué gen mirar; la secuencia
del ARNdc se diseña siempre sobre la secuencia propia del vector (`D37`).

## Desvíos respecto del plan, todos a la vista

La v1 se descartó por su control (Enmienda 1). La definición de empate se amplió con una lectura
secundaria post hoc (Enmienda 2) y se corrigió una cifra mía de esa misma enmienda: dije 16 % y
el empate sobre los ORF con hit es 50,1 %. La regla de normalización de nombres de `C12` no quedó
versionada como código, y está reimplementada desde su descripción, de modo que la concordancia
de nombres puede diferir en décimas de la que `C12` habría medido con la suya. `diamond` y `blastp`
no dan idénticas `pident`; las bandas de `C12` se calcularon con BLAST+ y no se corrigió.

## Lo que esto no dice

No dice qué hace un gen en *D. maidis*: dice con qué frecuencia el nombre de un ortólogo
recíproco coincide con el de otro, en dos cicadélidos anotados por homología. No dice nada de
expresión en el intestino (`GITV01` es de cuerpo entero). No cuenta genes: un contig no es un gen y
una proteína de referencia no es un locus. Y las pruebas del método (ORF, clasificación, bandas,
cortafuego) son 30 y pasan, pero comprueban el código y no la biología.

## Cómo reproducirlo

Entorno `conda create -n f1_homologia -c bioconda -c conda-forge diamond=2.2.8 python=3.11 numpy`.
Los comandos exactos están en `COMANDOS.md` de esta carpeta. Las tablas completas son
`resultados/transferencia_MQ.tsv.gz` y `transferencia_HV.tsv.gz`, una fila por ORF.
