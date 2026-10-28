# Recuperación por accesión de 6 filas del catálogo de genes blanco (issue #43, línea F3)

## Qué se hizo

Se leyó, para cada una de las seis filas del catálogo (`research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.json`), el texto del paper citado en `fuente` y se buscaron accesiones de GenBank escritas en el texto, las tablas o la sección de disponibilidad de datos. Para HE-04 y DE-06 se usó el texto ya en disco (`work/W1_papers/txt/Dcitri.txt` y `finsc-6-1811933.txt`); para DE-01, DE-03, CI-07 y CI-13 se bajó el texto completo en XML desde Europe PMC (PMC3737204, PMC11025951, PMC9905606, PMC7180231; copias en `work/F3_recuperacion/papers/`, carpeta no versionada). No se buscó ninguna secuencia por nombre de gen o especie y no se usó ninguna accesión de memoria. Las búsquedas en NCBI para el paso de verificación (E-utilities `esummary`/`efetch` sobre `nuccore`) fallaron: el proxy del sandbox devolvió 403 para `eutils.ncbi.nlm.nih.gov` («not on the allowlist»). Siguiendo el encargo, no se pidió aprobación ni se intentó otra vía; las filas con accesión citada quedan `bloqueado_por_red`. En consecuencia **no hay ninguna FASTA ni `sha256_secuencia`** y ninguna accesión de este informe está verificada contra NCBI [?].

## Resultado por fila

**HE-04, *Diaphorina citri* (Galdeano et al. 2017): `sin_accesion_en_el_paper`.** Los métodos dicen que los genes de catepsina D, quitina sintasa e inhibidor de apoptosis se identificaron por BlastX contra el transcriptoma de psyllid.org, sin dar ningún identificador de transcripto. La Table 1 trae sólo cebadores, y el material suplementario son dos figuras (S1 Fig, S2 Fig) según sus leyendas. [R] Sólo se leyeron las leyendas de los suplementos, no los archivos mismos.

**DE-01, *Peregrinus maidis* (Yao et al. 2013): `bloqueado_por_red`.** El texto y la Table 2 dan KC473163 para V-ATPase B (2495 nt en el texto; ORF de 1500 nt en la tabla y 1503 nt en el texto) y KC473162 para V-ATPase D (985 nt; ORF de 741 nt). [R] Los dos números de largo son los que declara el paper, no los medidos en NCBI. El paper cita además GO438398 (dbEST) como el gen de referencia RPL10, que no es blanco. Pendiente: confirmar organismo, producto y largo en NCBI.

**DE-03, *P. maidis* tra-2 (PMC11025951): `sin_accesion_en_el_paper`.** El texto no da accesión propia de Pmtra-2: las secuencias están en el suplemento «S1 File» (DOCX, no abierto) y el producto de PCR secuenciado en «S2 File». Las accesiones que sí aparecen (en la leyenda de la Fig 1) son proteínas de otras especies (*Apis mellifera*, *Bombyx mori*, *Ceratitis capitata*, *Drosophila melanogaster*, *Tribolium castaneum*, *Nilaparvata lugens*, *Cimex lectularius*, *Halyomorpha halys*) y no se usaron. [H] Una vía posible, fuera del encargo, es abrir S1 File; daría la secuencia pero no una accesión verificable.

**CI-07, *Euscelidius variegatus* chc (Sci Rep 2023): `sin_accesion_en_el_paper`.** La disponibilidad de datos cita el ensamblado de transcriptoma completo GFTU00000000.1 (TSA), no un transcripto de chc. Extraer el contig de chc de ese ensamblado equivaldría a elegir por nombre de gen, lo que el encargo prohíbe y que ya movió un conteo un 65 % en este proyecto (`PREREGISTRO.md` §4.1). La Supplementary Table S1 no se abrió. El artículo de Microbiol Res 2026 se ignoró, como indicaba el encargo.

**CI-13, *Nephotettix cincticeps* NcHig (Front Microbiol 2020): `bloqueado_por_red`.** El paper da MN815919 para NcHig y dice que el marco de lectura de 1911 pb se amplificó y se secuenció. [R] Es un ORF clonado; que sea el transcripto completo es [?]. Las demás accesiones del texto (AIS74715, MT043161, NP_620499.1) son de otras especies o del virus y no se usaron. Pendiente la verificación en NCBI.

**DE-06, *Delphacodes kuscheli* eth y burs-alpha (Andrada et al. 2026): `bloqueado_por_red`.** El texto (métodos y declaración de disponibilidad de datos) asigna PZ371507 y PZ371508 a eth y burs-alpha de *Dalbulus maidis*, y PZ371509 y PZ371510 a eth y burs-alpha de *D. kuscheli*. [R] El título del paper nombra las dos especies («*Dalbulus maidis* and *Delphacodes kuscheli*»), no sólo *D. maidis*. Por lo tanto, según el texto, la fila DE-06 con especie *D. kuscheli* y accesiones PZ371509/PZ371510 **no es un error de rotulado**: el paper cubre las dos especies. [?] La especie de las cuatro accesiones en NCBI no se pudo verificar y queda pendiente. En el repo (`research`, `00_meta`, `pipeline`) no se encontró el uso de PZ371507/PZ371508 que menciona el encargo; no se revisó el resto del árbol.

## Qué no se pudo

No se verificó ninguna accesión en NCBI (organismo, producto, largo), de modo que tres filas (DE-01, CI-13, DE-06) tienen accesión citada pero no recuperada. No se escribió ninguna FASTA. No se abrieron los suplementos DOCX/XLSX de ningún paper. No se modificó el catálogo ni ningún archivo existente. Para completar: habilitar `eutils.ncbi.nlm.nih.gov` y verificar KC473162, KC473163, MN815919, PZ371507–PZ371510 (y bajar FASTA a `work/F3_recuperacion/`).

---

## Verificación en NCBI (agregada el 2026-10-28 por la sesión principal)

El subagente que leyó los papers no tuvo red hacia `eutils.ncbi.nlm.nih.gov` (403 del proxy de **su**
sandbox) y dejó tres filas como `bloqueado_por_red`. Desde la sesión principal ese dominio sí es
accesible, y `scripts/08_verificar_recuperacion.py` hizo la parte pendiente: pidió el resumen y el
FASTA de las cinco accesiones **citadas en los papers**, sin buscar nada por nombre de gen ni de
especie. Salida: `recuperacion_6filas_verificacion.tsv`. Las secuencias quedan en
`work/F3_recuperacion/` y no se versionan.

| fila | accesión | organismo en NCBI | producto en NCBI | largo (NCBI) | largo que declara el paper |
| --- | --- | --- | --- | ---: | ---: |
| `DE-01` | `KC473163.1` | *Peregrinus maidis* | V-ATPase B, mRNA, cds completo | 2.391 | 2.495 |
| `DE-01` | `KC473162.1` | *Peregrinus maidis* | V-ATPase D, mRNA, cds completo | 1.002 | 985 |
| `CI-13` | `MN815919.1` | *Nephotettix cincticeps* | hikaru genki (Hig), mRNA, cds completo | 1.911 | 1.911 |
| `DE-06` | `PZ371509.1` | *Delphacodes kuscheli* | eth, mRNA, cds completo | 645 | — |
| `DE-06` | `PZ371510.1` | *Delphacodes kuscheli* | burs alpha, mRNA, cds completo | 480 | — |

`[M]` Organismo y producto **coinciden en las cinco**, con secuencia de ARNm y no de proteína. Con
esto las tres filas pasan de `bloqueado_por_red` a **recuperadas y verificadas**; `HE-04`, `DE-03` y
`CI-07` siguen `sin_accesion_en_el_paper`.

`DE-06` **no** es un error de rotulado del catálogo: el título del paper nombra *D. maidis* y
*D. kuscheli*, `PZ371507.1` y `PZ371508.1` son los de *D. maidis* (615 y 468 nt) y las dos de
*D. kuscheli* son las de arriba. La sospecha de error de rotulado que figuraba en el encargo era
mía y estaba equivocada; la corrigió el subagente al leer el texto.

`[?]` **`DE-01` difiere del largo que declara el paper** en −104 nt (B) y +17 nt (D). No se averiguó
por qué: podría ser que el paper cuente UTR de un ensamblado previo y la entrada de NCBI sea el
`cds completo` curado, pero no se comparó. `CI-13` coincide exacto.

**Lo que esto no es todavía.** Es recuperación y verificación de accesión: ningún tamizado
off-target ni ranking se corrió con estas secuencias. Tampoco se abrieron los suplementarios de
`DE-03` (S1 File, DOCX) ni de `CI-07` (Supplementary Table S1), y es el siguiente paso más barato.

---

## Suplementarios abiertos y referencias (agregado el 2026-10-28)

Pedido del equipo: **todo lo que sale de un paper lleva su referencia**. Abajo van las citas
completas de los seis papers usados, tomadas de Europe PMC por DOI o PMID (`referencias_recuperacion.tsv`,
`scripts/09_suplementarios_y_referencias.py`) y no de memoria. Cada dato de este informe que viene de un
paper lleva `[R]` y el número de su referencia. Los resultados propios (verificación en NCBI, ORF, cebadores)
son `[M]`.

### Referencias

**[R1]** Yao J, Rotenberg D, Afsharifar A, Barandoc-Alviar K, Whitfield AE (2013). Development of RNAi methods for Peregrinus maidis, the corn planthopper. *PloS one* 8(8):e70243. doi:10.1371/journal.pone.0070243; PMID 23950915; PMC3737204. (fila `DE-01`)

**[R2]** Wang YH, Rivera DE, Klobasa W, Lorenzen MD (2024). Evaluation of Peregrinus maidis transformer-2 as a target for CRISPR-based control. *PloS one* 19(4):e0295335. doi:10.1371/journal.pone.0295335; PMID 38635824; PMC11025951. (fila `DE-03`)

**[R3]** Arricau-Bouvery N, Dubrana MP, Canuto F, Duret S, Brocard L, Claverol S, Malembic-Maher S, Foissac X (2023). Flavescence dorée phytoplasma enters insect cells by a clathrin-mediated endocytosis allowing infection of its insect vector. *Scientific reports* 13(1):2211. doi:10.1038/s41598-023-29341-1; PMID 36750707; PMC9905606. (fila `CI-07`)

**[R4]** Wang H, Liu Y, Mo L, Huo C, Wang Z, Zhong P, Jia D, Zhang X, Chen Q, Chen H, Wei T (2020). A Neuron-Specific Antiviral Mechanism Modulates the Persistent Infection of Rice Rhabdoviruses in Leafhopper Vectors. *Frontiers in microbiology* 11:513. doi:10.3389/fmicb.2020.00513; PMID 32362876; PMC7180231. (fila `CI-13`)

**[R5]** Galdeano DM, Breton MC, Lopes JR, Falk BW, Machado MA (2017). Oral delivery of double-stranded RNAs induces mortality in nymphs and adults of the Asian citrus psyllid, Diaphorina citri. *PloS one* 12(3):e0171847. doi:10.1371/journal.pone.0171847; PMID 28282380; PMC5345766. (fila `HE-04`)

**[R6]** Andrada NL, Crespo M, Baricalla AA, Dalaisón-Fuentes LI, Sterkel M, Catalano MI (2026). ETH and Burs-α are necessary for the normal molting in &lt;i&gt;Dalbulus maidis&lt;/i&gt; and &lt;i&gt;Delphacodes kuscheli&lt;/i&gt;. *Frontiers in insect science* 6:1811933. doi:10.3389/finsc.2026.1811933; PMID 42328018; PMC13279319. (fila `DE-06`)

`[M]` Tres de estos papers figuraban en el catálogo de `C5` sin autores («autores no verificados» o sin
DOI): `DE-03` (R2), `CI-07` (R3) y `CI-13` (R4). Quedan verificados con estas citas. El catálogo no se
modificó.

### Cada fila y su referencia

| fila | qué se tomó del paper | dónde | referencia |
| --- | --- | --- | --- |
| `DE-01` | accesiones `KC473163` (V-ATPase B) y `KC473162` (V-ATPase D); largos de 2.495 y 985 nt `[R]` | texto y Table 2 | R1 |
| `DE-03` | las secuencias de *Pmtra-2* (S1 File), y los tres cebadores (S1 Table) `[R]` | suplementarios S1 File y S1 Table | R2 |
| `CI-07` | que su única accesión es el TSA `GFTU00000000.1` `[R]`; su suplementario es una tabla proteómica | sección de disponibilidad de datos; Supplementary Table S1 | R3 |
| `CI-13` | accesión `MN815919`; ORF de 1.911 pb `[R]` | métodos y resultados | R4 |
| `HE-04` | que los transcriptos se identificaron por BlastX sin citar ID `[R]` | métodos | R5 |
| `DE-06` | accesiones `PZ371509` y `PZ371510` asignadas a *D. kuscheli* `[R]` | métodos y *data availability statement* | R6 |

### `DE-03`: recuperada desde el suplementario del paper, sin accesión de NCBI

El texto de R2 dice que las secuencias de *Pmtra-2* «pueden encontrarse» en el S1 File `[R]`, y ese archivo
es un DOCX abierto en PMC con dos secuencias: `Pmtra-2_167888_1` (1038 nt) y `Pmtra-2_167888_2` (1139 nt)
`[R]` (R2, S1 File). **No traen accesión de GenBank** y el paper no la cita. Lo medido `[M]`
(`recuperacion_suplementarios.tsv`): las dos contienen los **tres cebadores** que el mismo paper publica en
su S1 Table —los dos de la primera ronda de PCR (la plantilla del dsRNA) y el directo de qPCR— completos, lo que las ata al
gen que el paper silenció; y su ORF más largo es de 308 y 312 aa. Están en **orientación inversa** a la de
los cebadores. El sha256 de cada una está en el TSV. **Lo que no se pudo hacer:** verificarlas en NCBI, porque no
tienen accesión; su identidad descansa en R2 y en la coincidencia con los cebadores. `[?]` El número
`167888` parece un identificador del transcriptoma de *P. maidis* del paper, y ese transcriptoma no se abrió.

### `CI-07`: sigue sin accesión

El Supplementary Table S1 de R3 (`41598_2023_29341_MOESM1_ESM.pdf`, 3 páginas) es una tabla de proteínas que
interactúan con VmpA en un pull-down con LC-MS/MS, clasificadas por KEGG `[R]`. No contiene secuencias ni
clatrina. La única accesión que R3 cita es el ensamblado completo `GFTU00000000.1`, y extraer de ahí el
transcripto de `chc` sería elegirlo por nombre. La fila queda `sin_accesion_en_el_paper`.

### Estado de las seis filas, actualizado

| fila | estado |
| --- | --- |
| `DE-01` | recuperada y verificada en NCBI (R1) |
| `CI-13` | recuperada y verificada en NCBI (R4) |
| `DE-06` | recuperada y verificada en NCBI (R6) |
| `DE-03` | **recuperada desde suplementario**, sin accesión; coincide con los cebadores del paper (R2) |
| `HE-04` | sin accesión en el paper (R5) |
| `CI-07` | sin accesión en el paper; el suplementario no la trae (R3) |

Con `DE-03`, son **4 de las 6** filas con secuencia en mano. `HE-04` y `CI-07` no se pueden recuperar desde
estos papers.

`[M]` **Nota de método.** Los cebadores no se escriben en el script: se leen del DOCX de R2 en cada corrida, porque dos de ellos son rachas de 21 nt o más y el repo no las versiona (`tools/verificacion/sin_secuencias.py` da 0 hallazgos en `F3`). **Una versión anterior del script (`4e22f09`) sí llevaba uno de esos cebadores escrito**; es un cebador público de R2, no de EPILAB, y queda en el historial porque no se reescribe lo ya pusheado. El rótulo de «dsRNA» que figuraba en ese commit era incorrecto: son cebadores de la primera ronda de PCR.
