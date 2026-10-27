# Validación del supuesto de las bandas — preregistro

**Escrito antes de correr nada.** Pregunta abierta **56** del issue #25. Commiteado antes de la
primera corrida; cualquier cambio posterior va como enmienda fechada al final, nunca editando lo
de arriba.

## La pregunta

`F1` publica, para cada ortólogo transferido, la banda de concordancia que `C12` (Validación A)
midió para ese tramo de identidad, y de ahí sale su única cifra de calidad: **el 81 % esperado**
sobre los 10.280 ORF recíprocos con nombre de la lectura inclusiva. Las bandas de `C12` se
midieron **entre dos proteomas RefSeq completos y anotados** (*Macrosteles quadrilineatus* contra
*Homalodisca vitripennis*, pares recíprocos por `blastp`). `F1` las aplica a pares en los que el
lado consulta **no es una proteína curada sino un ORF de seis marcos de un transcriptoma**, que
puede ser parcial, quimérico o con el marco corrido. El informe de `F1` lo declara `[H]`:
supuesto, no medición. Esto lo mide.

## Por qué no la ruta que sugería la pregunta 56

La entrada 56 proponía validar contra «un subconjunto de contigs cuyos genes tengan anotación
independiente (los de la curación de `C5`)». `research/ola3/C5_.../catalogo_genes_blanco.json` es
un catálogo de genes blanco de RNAi con una fila por gen y por estudio: del orden de una docena de
genes. Con ese n no se puede estimar una concordancia por banda de identidad —`C12` necesitó
1.152 pares para cinco bandas—. Se descarta por potencia, no por pertinencia, y se usa el diseño
de abajo, que da miles de pares.

## El diseño: el mismo organismo leído de las dos maneras

*M. quadrilineatus* tiene en RefSeq **las dos cosas**: su proteoma anotado y sus transcriptos. Eso
permite comparar las dos lecturas sobre el mismo organismo, los mismos genes y la misma
referencia, cambiando **una sola cosa**: si el lado consulta es la proteína curada o un ORF
derivado de su transcripto.

- **Brazo P (proteína curada; es lo que midió `C12`).** Las 34.269 proteínas RefSeq de MQ contra
  el proteoma de HV (31.163), recíproco, `diamond blastp --more-sensitive`, e ≤ 1e-10.
- **Brazo O (ORF de seis marcos; es lo que hace `F1`).** Los transcriptos RefSeq de MQ
  (`rna.fna`, 36.629) traducidos en seis marcos, todos los ORF de parada a parada de ≥ 100 aa,
  contra el mismo proteoma de HV, recíproco, los mismos parámetros.

En los dos brazos el **nombre transferido** es el producto RefSeq del ortólogo recíproco en HV. El
**nombre verdadero** de la consulta es el producto RefSeq de MQ: en el brazo P, el de la proteína
misma; en el brazo O, el de la proteína que RefSeq asocia al transcripto de origen
(`feature_table`, `CDS`: `product_accession` XP ↔ `related_accession` XM ↔ `name`, 34.256 filas).
Es el mismo campo en los dos lados.

**Código.** Se importa `scripts/transferir_anotacion.py` de `F1` y se usan sus funciones tal cual
—`todos_los_orfs`, `diamond_blastp`, `mejores`, `clasificar`, `clasificar_ampliada`,
`normalizar_nombre`, `es_informativo`, `rotulo_cobertura`— con sus constantes (`MIN_AA` 100,
e ≤ 1e-10, `-k` 5, `--max-hsps` 1). No se reimplementa nada: lo que se valida es el código que
corrió, no una versión parecida.

## La métrica

Concordancia = fracción de pares recíprocos **con nombre informativo en los dos lados** en los que
el nombre normalizado transferido desde HV es igual al nombre normalizado verdadero de MQ,
tabulada por banda de identidad (`<40`, `40-60`, `60-80`, `80-90`, `>=90`) con IC95 de Wilson. Es
exactamente la cantidad que `C12` tabuló. Se reporta para los dos brazos, con la regla **estricta**
y con la **inclusiva**, por separado.

**Análisis pareado.** La comparación primaria se restringe a los genes de MQ presentes en los dos
brazos (misma proteína XP como verdad), para que la diferencia no sea por composición del
conjunto. El no pareado se reporta al lado.

**Unidad en el brazo O.** Un transcripto puede dar varios ORF. La unidad primaria es el **ORF**,
que es la unidad de la tabla de `F1` y la del 81 %. Como secundaria se reporta por transcripto,
tomando el ORF de mejor bitscore.

## Criterio de decisión, fijado ahora

Sobre las bandas con **n ≥ 100 pares en los dos brazos**, en el análisis pareado:

1. **El supuesto se sostiene** si en todas esas bandas la concordancia del brazo O cae dentro del
   IC95 del brazo P.
2. **Las bandas sobredeclaran** si en alguna de esas bandas la concordancia de O queda por debajo
   del límite inferior del IC95 de P. En ese caso se recalcula el esperado de `F1` usando las
   bandas del brazo O y se publica la cifra corregida al lado de la vieja, tachada, según la
   convención del repositorio.
3. **Las bandas subdeclaran** —O por encima del IC95 superior de P— se reporta igual y no se
   corrige nada hacia arriba.

Las bandas con n < 100 se tabulan pero no deciden.

## Lo que este diseño NO prueba, dicho antes de verlo

- **No cubre el error de ensamblado.** Un `rna.fna` de RefSeq es un transcripto curado y completo;
  un contig de un TSA ensamblado de novo puede estar fragmentado, ser quimérico o tener el marco
  roto. Este experimento aísla el efecto de **traducir en seis marcos y elegir ORF**, que es un
  componente del supuesto, no el supuesto entero. Para acotar la dirección del resto se compara la
  distribución de `rotulo_cobertura` del brazo O contra la de la corrida real sobre `GITV01`: si
  `GITV01` tiene proporcionalmente más `parcial` y `fragmento`, el brazo O es **optimista** y la
  concordancia real sobre `GITV01` sería menor o igual que la medida acá. Esa comparación acota el
  signo, no la magnitud.
- **El brazo P no es `C12`.** `C12` corrió con BLAST+ sobre una submuestra (4.000 consultas, 3.100
  en el reverso, 1.152 pares); acá se corre el par completo con `diamond`. Si el brazo P difiere de
  `C12`, eso es un hallazgo sobre `C12` —submuestra o alineador— y se reporta aparte. **La decisión
  de arriba se toma sobre O contra P**, que es la comparación interna y pareada, no sobre O contra
  las cifras publicadas de `C12`.
- **No valida la anotación de RefSeq.** Igual que `C12`, mide consistencia entre anotaciones que ya
  derivan de homología, no función experimental. Un acierto puede ser dos errores iguales.
- **No dice nada sobre *D. maidis*.** Mide sobre MQ, que es el organismo que tiene las dos
  lecturas. Que el resultado se traslade a `GITV01` supone que el paso ORF afecta igual a los dos
  transcriptomas.
- **No corrige** la reimplementación del normalizador de nombres de `C12` (su código no quedó
  versionado). Los dos brazos usan el mismo normalizador, así que la comparación O contra P es
  válida aunque el normalizador difiera del original.

## Salidas comprometidas

`resultados/bandas_por_brazo.tsv` (una fila por brazo × regla × banda, con n, aciertos,
concordancia e IC95), `resultados/resumen.json` (insumos con sus sha256, versión de `diamond`,
conteos, el veredicto según el criterio de arriba y el esperado recalculado) y `REPORT.md`. Las
tablas por par van en `resultados/pares_{P,O}.tsv.gz`. Ninguna salida lleva secuencia: rige el
cortafuego de `D37` igual que en `F1`.
