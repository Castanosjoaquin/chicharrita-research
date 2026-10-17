# ejemplos/ — corridas reales de W2

Todas las entradas son **secuencias públicas de referencia del NCBI**. Ninguna
secuencia de la planilla de EPILAB fue usada, ni local ni remotamente.

## Entradas (`entradas/`)

| Archivo | Qué es | Origen |
| --- | --- | --- |
| `eth_PZ371507.1.fa` | ARNm de *ecdysis triggering hormone* de *Dalbulus maidis*, 615 nt | NCBI nuccore `PZ371507.1` |
| `dmaidis_public_mrnas.fa` | el anterior más bursicón α (`PZ371508.1`, 468 nt) | NCBI nuccore |
| `MRFV_NC_002786.2.fa` | genoma de referencia de *Maize rayado fino virus*, 6.366 nt | NCBI RefSeq `NC_002786.2` |
| `eth_16mers.fa`, `eth_21mers.fa`, `eth_26mers.fa` | 600, 595 y 590 ventanas deslizantes de paso 1 sobre `eth` | generadas por nosotros |
| `db_demo_zmays40_amel40_mrfv.fa` | base de **demostración**: 40 ARNm RefSeq de *Zea mays* + 40 de *Apis mellifera* + genoma de MRFV; 81 secuencias, 138.269 bases | NCBI E-utilities |

La base de demostración **no sirve para tamizar off-targets en serio**: el maíz
tiene 57.091 ARNm RefSeq y bajamos 40. Está para exhibir el comportamiento de los
parámetros de BLAST, no para medir riesgo.

## Corrida local de BLAST+ y ViennaRNA

Script: `corrida_blast_local.sh` (reproducible, un solo archivo). Los archivos binarios de las
bases de BLAST (`db_demo.n*`, `db_dmaidis.n*`) no se versionan: los regenera el script. Entorno conda
`w2tools` con **BLAST+ 2.17.0+** (build 22-ago-2026) y **ViennaRNA 2.7.2**,
instalados desde Bioconda/conda-forge. Comando:

    bash corrida_blast_local.sh

| Salida | Qué muestra |
| --- | --- |
| `salidas/blastn_help_2.17.0.txt` | texto de ayuda completo del binario; líneas 95-182, los 48 campos de salida tabular, ninguno termodinámico |
| `salidas/E1_makeblastdb.log` | construcción de las dos bases: 81 secuencias / 138.269 bases (`blastdbcmd -info`) y 2 secuencias |
| `salidas/E2_blastn_megablast_pairwise.txt`, `E2_blastn_megablast.tsv` | `blastn` por defecto del ARNm completo contra la base de demostración |
| `salidas/E3_21mers_perfect.tsv` | condición mayor del Model I (21 nt perfecto): **0 aciertos** |
| `salidas/E3_16mers_perfect.tsv` | condición adicional de 16 nt: **1 acierto**, ventana 550-565 de `eth` contra `NM_001346803.1` de *Zea mays*, hebra menos, E=1,66e-04, bit score 32,2 |
| `salidas/E3_26mers_2mm.tsv` | 827 filas con `-perc_identity 92`, de las que **ninguna** es un alineamiento de 26 nt con ≤2 desapareamientos (largos de 11 a 16 nt) |
| `salidas/E4_sensibilidad_umbrales.tsv` | barrido de `perc_identity` x `word_size`: 0 aciertos con palabra 21, 578 con palabra 11, 139.004 con palabra 7 |
| `salidas/E5_21mers_ontarget.tsv` | lado on-target: 595 de 595 ventanas con acierto perfecto contra su propio transcripto |
| `salidas/E6_RNAfold.txt`, `E6_vienna_completo.txt` | ViennaRNA: MFE -186,90 kcal/mol del ARNm, ΔG -26,00 del dúplex de 21 nt |
| `salidas/E7_param_set.txt` | el juego de parámetros por defecto es Turner 2004 (-186,90 idéntico; Turner 1999 da -202,90) |

## Corrida real de dsRNAEngineer (servicio web)

Proyecto **`6fab2304bf273f5e`**, enviado el 17 de octubre de 2026 por
`POST https://dsrna-engineer.cn/v1/api/project/design` con la secuencia pública
`PZ371507.1`, *Dalbulus maidis* como única especie on-target (Model I) y *Zea
mays* (Model I) y *Apis mellifera* (Model II) como off-target.

| Salida | Qué contiene |
| --- | --- |
| `salidas/E8_dsrnaengineer_request.json` | el cuerpo exacto del pedido |
| `salidas/E8_detail.json` | el resumen: 237 on-targets en *D. maidis*, 70 off-targets en maíz, 67 en abeja |
| `salidas/E8_match_result.json` | los diez fragmentos candidatos, de 51 a 91 pb, sin ningún campo de puntaje |
| `salidas/E8_dsrnaengineer_resultado/` | el `.tar.gz` desempaquetado: FASTA de entrada y **nueve archivos `.bwt` de Bowtie**, uno por especie y tamaño de ventana |
| `salidas/E8_dsrnaengineer_option-list.json` | catálogo oficial de modelos de coincidencia; incluye la frase «parameters of bowtie» |
| `salidas/E8_dsrnaengineer_categorias_especies.csv` | las 23 categorías del panel con su número de especies |
| `salidas/E8_dsrnaengineer_fuente_de_los_transcriptomas.csv` | 443 RefSeq, 577 ensamblados de novo desde el SRA, 49 secuencias sueltas, 34 sin identificador |
| `salidas/E8_dsrnaengineer_especies_clave.csv` | las ocho especies que nos importan, con su `species_id` y su modelo |
| `salidas/E8_dsrnaengineer_poll.log` | el sondeo del estado del proyecto hasta su finalización |
| `salidas/E9_bowtie_formato_columnas.txt` | qué es la novena columna de los `.bwt`: Bowtie 1.3.1 local con `-v 0` y `-v 2`, comparado con las líneas del servicio |

Descomposición verificada por nosotros contra los archivos crudos: on-target
237 = 190 (21 nt) + 47 (16 nt) + 0 (26 nt); maíz 70 = 70 (16 nt) + 0 + 0; abeja
67 = 67 (16 nt) + 0 + 0. Las 374 líneas son coincidencias exactas de la ventana
correspondiente de la consulta, comparadas una por una contra la secuencia de la
consulta: **ninguna tiene desapareamientos**. La novena columna de esos archivos no es
el campo de desapareamientos sino el campo 7 de Bowtie 1 («otras instancias»), según el
manual de Bowtie 1, según nuestra reproducción local con Bowtie 1.3.1 —donde los
desapareamientos aparecen en un octavo campo y como descriptores del tipo `2:G>C,4:T>C`,
nunca como un entero suelto— y según el hecho de que esa columna llega a 9 bajo una
condición de apareamiento perfecto, valor imposible para un conteo de desapareamientos.
La verificación está en `salidas/E9_bowtie_formato_columnas.txt`. Los 190 aciertos de 21 nt caen todos en un único contig
(`TRINITY_DN64958_c0_g1_i1`) que cubre las posiciones 215-424 de un ARNm de 615
nt.

## Lo que no se ejecutó

- **BLAST web del NCBI** (`Blast.cgi`): no se envió ninguna consulta. Se leyeron
  el formulario vivo y la documentación oficial. Lo que había que medir se mide
  mejor con BLAST+ local y es reproducible.
- **Primer-BLAST**: fuera del problema (Tm de cebadores de PCR). Sólo se leyó su
  documentación oficial.
- **Módulo *screen-target* de dsRNAEngineer**: no se corrió; la pregunta
  prioritaria no lo requería.
