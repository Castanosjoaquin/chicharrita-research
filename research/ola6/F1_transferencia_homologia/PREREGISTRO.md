# F1 — Transferencia de anotación por homología: preregistro del método y los umbrales

**Fijado el 2026-10-27, antes de la primera corrida.** Issue #25. Este documento se commitea
antes de que exista ninguna tabla de resultados; lo que se mida después se lee contra lo escrito
acá, y todo desvío queda anotado en el informe como desvío.

## Qué es F1 y qué no es

Toma un transcriptoma sin anotar y devuelve, por secuencia, el ortólogo recíproco en un
cicadélido con proteoma anotado, con su identidad, su cobertura y la banda de concordancia que
`C12` midió para esa identidad. **Contesta qué gen considerar. Nunca contesta con qué secuencia
diseñar** (`D37`): el diseño del ARNdc se hace siempre sobre la secuencia propia del vector. Por
eso la salida de F1 **no lleva secuencia de nucleótidos** y ningún módulo de diseño la lee.

## Insumos

| Rol | Qué | Fuente | Verificación |
| --- | --- | --- | --- |
| Consulta | `Dalbulus_maidis_transcriptome_GITV01.fas`, 56.117 secuencias, 94.702.486 pb | TSA público de Ohio State (Xu et al.), enviado por el investigador | md5 `bee70da94d1541fb371f10e4e358b6c8`; los totales coinciden con `research/ola2/W3_bases_datos/consultas/05_tsa_y_ftp.md` |
| Referencia principal | proteoma RefSeq de *Macrosteles quadrilineatus*, `GCF_028750875.1` (34.269 proteínas) | NCBI, FTP de genomas | md5 contra `md5checksums.txt` del NCBI |
| Referencia de contraste | proteoma RefSeq de *Homalodisca vitripennis*, `GCF_021130785.1` (31.163 proteínas) | NCBI, FTP de genomas | ídem |

*Macrosteles* y *Dalbulus* son los dos Deltocephalinae; *Homalodisca* es un Cicadellinae. Es el
mismo par de cicadélidos con el que `C12` midió la concordancia, y por eso las bandas se pueden
aplicar. *N. lugens* se deja afuera porque `C12` no corrió ese par. Todo corre local; ninguna
secuencia sale de la máquina.

## Método (parámetros fijados)

1. **Del contig a proteína.** Traducción en los seis marcos, ORF de codón de parada a codón de
   parada (sin exigir ATG: los contigs de un TSA pueden ser parciales), **el ORF más largo por
   contig**, mínimo **100 aminoácidos**. Un contig sin ORF de ese largo no se descarta: se cuenta
   en su propia categoría. Código genético estándar; los IUPAC ambiguos traducen a `X`.
2. **Alineamiento.** `diamond blastp`, ORF contra proteoma y proteoma contra ORF, `--more-sensitive`,
   `-e 1e-10` (el mismo umbral que `C12`), hasta 5 hits por consulta.
3. **Ortología recíproca.** Un par (ORF *a*, proteína *p*) es recíproco si *p* es el mejor hit de
   *a* **y** *a* es el mejor hit de *p*, por bitscore. Un empate en el primer puesto (mismo
   bitscore) **no** se resuelve: el par se declara «empate» y no cuenta como recíproco.
4. **Identidad y cobertura.** Identidad de aminoácidos del mejor alineamiento (`pident`), y las
   dos coberturas del alineamiento (sobre el ORF y sobre la proteína de referencia). **Ninguna
   cobertura filtra**: se reportan, y se rotula `cobertura alta` si las dos son ≥ 0,70, `parcial`
   si la menor está en [0,30; 0,70) y `fragmento` si la menor es < 0,30. Los rótulos son
   `[H]` (elegidos por nosotros, sin respaldo en la literatura); sirven para leer, no para excluir.
5. **Banda de concordancia.** La de `C12` (Validación A), por tramo de identidad, sin recalcular:

| identidad | concordancia | IC95 (Wilson) | pares en C12 |
| --- | --- | --- | --- |
| < 40 % | 25,0 % | 10,2–49,5 | 16 |
| 40–60 % | 76,1 % | 68,2–82,5 | 134 |
| 60–80 % | 76,8 % | 72,7–80,4 | 456 |
| 80–90 % | 78,6 % | 73,9–82,6 | 336 |
| ≥ 90 % | 86,2 % | 80,9–90,2 | 210 |

   Fuente: `research/ola3/C12_validacion_homologia/resultados/concordancia_por_identidad.tsv`
   `[M]`. El tramo < 40 % se rotula `no concluyente` (16 pares).
6. **Nombre transferido.** El nombre de producto de la proteína de referencia, tal como lo
   escribe RefSeq, más el nombre normalizado con la misma regla que `C12` (sin «isoform Xn»,
   «-like», «homolog», números de isoforma, mayúsculas). Un nombre que contenga
   `uncharacterized`, `hypothetical` o `LOW QUALITY` es **«sin anotación informativa»** y no se
   transfiere como si fuera un nombre.
7. **Contraste entre las dos referencias.** Donde un contig tiene par recíproco con las dos
   referencias, se reporta si los dos nombres normalizados coinciden. Es una consistencia, no una
   verdad: ambos nombres de RefSeq ya derivan de homología.

## Contabilidad: todas las secuencias caen en una categoría, y las categorías suman el total

Cada contig de GITV01 cae en **exactamente una** de: (a) sin ORF ≥ 100 aa; (b) con ORF pero sin
hit con e ≤ 1e-10; (c) con hit pero no recíproco, ni empate; (d) empate en el primer puesto;
(e) recíproco con nombre «sin anotación informativa»; (f) recíproco con nombre informativo. La
suma debe dar **56.117**; si no da, el script aborta. Se reporta por separado el número de
**proteínas de referencia distintas** alcanzadas: es una cota inferior del número de genes, porque
varios contigs pueden ser isoformas o fragmentos del mismo gen, y por eso **el informe habla de
contigs y no de loci**.

## Controles, escritos antes de correr

* **Positivo.** La subunidad B de la V-ATPasa está en `GITV01003502.1` con la proteína completa de
  500 aa, idéntica a la de *M. quadrilineatus* (`research/ola6/O2_vatpase_b/REPORT.md`, `[M]`).
  F1 debe devolver ese contig como recíproco de la V-ATPase B de *Macrosteles* con identidad ≥ 99 %.
  Si no lo hace, **la corrida no se lee**: hay un error de método.
* **Negativo (señuelo).** 1.000 ORF de GITV01 elegidos al azar (semilla 0) se barajan
  residuo a residuo, conservando la composición, y pasan por el mismo `blastp`. El número de
  hits con e ≤ 1e-10 es la tasa de falsos positivos del umbral. Si supera 0,1 % (1 hit de 1.000)
  se declara y se endurece el umbral antes de leer nada.
* **Cortafuego.** Una prueba que (i) recorre el AST de todos los `.py` del repositorio y falla si
  alguno fuera de F1 importa `transferir_anotacion`, y (ii) verifica que la tabla de salida no
  tiene ninguna columna de secuencia de nucleótidos.
* **Lo que se mide ya** contra lo que ya está en el repo: `BicC` de EPILAB tiene su mejor
  coincidencia en `GITV01000968.1` (99,72 %, `research/ola2/W5_secuencias_epilab/REPORT.md`);
  F1 debe asignar a ese contig una proteína de nombre compatible con *bicaudal C*. No es criterio
  de éxito, es una verificación de cordura, y se reporta tal cual salga.

## Límites declarados antes de mirar

1. **Las bandas de `C12` son de proteoma contra proteoma, ambos anotados por RefSeq.** Un ORF
   de un TSA puede ser parcial, quimérico o tener errores de ensamblado; que la banda le
   aplique es `[H]`, y la cifra es una cota de coherencia entre anotaciones, no de función.
2. **El 78,2 % de `C12` es una cota inferior de la función compartida** (sinónimos como
   *glycogen synthase kinase-3 beta* contra *shaggy* cuentan como desacuerdo), pero también es
   consistencia entre nombres que ya derivan de homología, no verdad experimental.
3. **El ORF más largo por contig** pierde el segundo gen de un contig quimérico y se equivoca si
   el ORF más largo es espurio. No se mide la tasa de ambas cosas en esta corrida.
4. **GITV01 es de cuerpo entero**: F1 no dice nada de expresión en el intestino.
5. **Un contig no es un gen.** La cantidad de contigs con par recíproco no es una cantidad de
   genes.
6. `diamond` y `blastp` no son idénticos: la `pident` de `diamond` puede diferir en décimas de
   la de BLAST+, con la que se calcularon las bandas. No se corrige.

## Qué cuenta como resultado

Los números tal como salgan, con los controles. No hay umbral de éxito para la fracción de contigs
anotados: lo que se busca es la contabilidad completa y las bandas. La primera corrida real
contesta la pregunta del issue sobre `GHCC01` por el accesión (`GITV01` ≠ `GHCC01`) y no por
alineamiento.
