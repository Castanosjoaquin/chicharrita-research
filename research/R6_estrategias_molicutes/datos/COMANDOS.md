# Registro de cómputo de factibilidad — R6 (corrido el 2026-10-17)

Regla D8: no se entrenó ni ajustó ningún modelo. Todo lo de abajo es consulta, alineamiento y búsqueda por perfiles. Ninguna secuencia de `YHat-Biotech/` se usó ni se subió a ningún servicio (todas las secuencias son públicas: RefSeq, UniProt).

## 1. Resolución de taxid y accesiones (NCBI Datasets API v2, 2026-10-17)
- `GET https://api.ncbi.nlm.nih.gov/datasets/v2/taxonomy/taxon/{nombres}` → *Ca.* Phytoplasma zeae = **202462**, *Spiroplasma kunkelii* = **47834**, *Dalbulus maidis* = **74065**.
- `GET .../genome/taxon/{taxid}/dataset_report` → 2 ensamblados por taxón, ambos «Complete Genome», `assembly_status: current`.
  - *Ca.* P. zeae cepa M3: `GCA_001712875.1` (GenBank) = `GCF_001712875.1` (RefSeq, anotación `RS_2026_06_07`), 576.118 pb, un cromosoma (`NZ_CP015149.1`).
  - *S. kunkelii* cepa CR2-3x: `GCA_001274875.1` = `GCF_001274875.1` (RefSeq, anotación `RS_2025_12_13`), 1.514.561 pb en total = cromosoma `NZ_CP010899.1` (1.463.926 pb) + 3 plásmidos `NZ_CP012423.1` (22.558), `NZ_CP012424.1` (20.501), `NZ_CP012425.1` (7.576).
- Salida cruda: `datos/datasets_reports_2026-10-17.json`.
- **El cuarto plásmido (pSKU146, 14.615 pb) no está en ese ensamblado**: es la accesión aparte `NC_006400.1` (= `AY528560.1`, según el anuncio del genoma). Se bajó con E-utilities (`efetch db=nuccore rettype=fasta_cds_aa`): 13 CDS, `datos/pSKU146_NC_006400.1_cds_aa.faa`. Reconcilia la diferencia de tamaño entre R1 §3.2 (1.463.926 = sólo el cromosoma) y W3 §4.2 (1.514.561 = cromosoma + 3 plásmidos): no se contradicen, cuentan objetos distintos.

## 2. Descarga de proteomas (`GET .../genome/accession/{acc}/download?include_annotation_type=PROT_FASTA&include_annotation_type=GENOME_GFF`)
- md5 de los 4 archivos de cada paquete verificado contra `md5sum.txt`: todos correctos.
- `protein.faa`: M3 = **522** proteínas; CR2-3x = **1.715** proteínas.
- Conciliación con el reporte de NCBI (524 y 1.775 genes `protein_coding`): el FASTA deduplica por accesión WP_ (RefSeq asigna un mismo WP_ a proteínas de secuencia idéntica). Contado en el GFF: M3 = 524 CDS con `protein_id` → 522 únicos (1 WP_ repetido, hasta 3 copias); CR2-3x = 1.775 CDS → 1.715 únicos (41 WP_ repetidos, hasta 5 copias). Pseudogenes (16 y 137) se cuentan aparte. **Para análisis por gen hay que usar el GFF, no sólo el FASTA.**

## 3. Búsqueda por perfiles HMM de dominios de RNAi (cierra, para estos dos genomas, la limitación D9)
- Herramienta: `pyhmmer 0.12.3` (HMMER integrado), entorno `w5bio`. Script: `scripts/01_hmm_rnai_dominios.py` (umbral GA de cada perfil) y `scripts/02_hmm_sensibilidad.py` (mejor acierto con E ≤ 10, sin umbral).
- Perfiles (InterPro API, `GET https://www.ebi.ac.uk/interpro/api/entry/pfam/{PF}?annotation=hmm`): `PF02171.24` Piwi, `PF02170.29` PAZ, `PF03368.20` Dicer_dimer, `PF00636.32` Ribonuclease_3 (control de familia). Archivos en `datos/pfam/`.
- Entradas: M3 (522), CR2-3x (1.715), pSKU146 (13) y 3 controles positivos de UniProt: AGO2 humana `Q9UKV8`, DICER1 humana `Q9UPY3`, Argonauta bacteriana de *Thermus thermophilus* `Q746M7`.
- Resultado (`datos/hmm_resumen.tsv`, `datos/hmm_hits.tsv`, `datos/hmm_sensibilidad.tsv`): **0 aciertos de Piwi, PAZ y Dicer_dimer en M3, CR2-3x y pSKU146**, también sin umbral (E ≤ 10). Ribonuclease_3: 1 acierto en M3 (`WP_069028106.1`, «ribonuclease III», 82,1 bits) y 1 en CR2-3x (`WP_053391309.1`, «ribonuclease III», 79,2 bits); 0 en pSKU146.
- Controles: AGO2 → Piwi (392,7 bits, E 1,7e-121) y PAZ (111,0); DICER1 → PAZ (66,4), Dicer_dimer (83,1) y Ribonuclease_3 (142,0); TtAgo → Piwi **32,1 bits contra un corte GA de 28,9: pasa por muy poco**. Lectura: el perfil Piwi detecta con holgura una Argonauta eucariota y sólo en el límite una procariota; una Argonauta de mollicute muy divergente podría quedar bajo el corte, pero en la pasada sin umbral no hay ni un acierto, de modo que el cero es robusto para estos tres perfiles.
- Límites: sólo proteínas anotadas (una ORF no anotada no se vio; falta un tblastn contra el genoma), sólo tres perfiles Pfam, sólo dos cepas. R1 §4.2 cubre 126.874 proteínas de mollicutes por anotación; esto no lo reemplaza, lo complementa con otro método sobre los dos genomas del problema.

## 4. Homología de efectores (UniProt REST + BLAST+ 2.17.0+, entorno `w2tools`)
- Consulta UniProt `protein_name:SAP11/SAP54 AND taxonomy_id:33926` (género *Candidatus* Phytoplasma). Todas las entradas devueltas son no revisadas (TrEMBL). Existe una anotada para *Ca.* P. zeae: `A0ABM6DLD7` (SAP11-like, 116 aa) y otra `A0ABN4RXW7` (SAP08-like).
- `blastp -query datos/efectores_consulta.faa -db datos/db_M3 -evalue 1e-2 -seg no`: `A0ABM6DLD7` ↔ `WP_069028078.1` **100 % de identidad, 116/116 aa, E 1,3e-80**. SAP11 de *Ca.* P. citri 43,1 % (E 9,5e-27) y SAP11-like de loofah WB 33,7 % (E 2,7e-12) contra la misma proteína. Para SAP54: único acierto 40,6 % sobre 32 aa (E 0,004), **insuficiente para afirmar homología** y no es evidencia de ausencia (los SAP54 son divergentes; haría falta un perfil HMM). *S. kunkelii*: 0 aciertos (esperable).
- Anotaciones por nombre en M3: `WP_069028031.1` «effector protein» (en UniProt `A0ABN4RXW7`, «AYWB SAP08-like»). Sólo 1 de las 522 anotaciones de M3 nombra efector (la otra coincidencia del patrón de búsqueda, «cyclic-di-AMP receptor», es un falso positivo por la sigla AMP).

## 5. Transferencia por ortología desde *S. citri* hacia *S. kunkelii* (BLAST+ 2.17.0+; `datos/blastp_spiroplasma_vs_CR2-3x.tsv`)
- PGK de *S. citri* (`Q7WTU1`, 412 aa) ↔ `WP_053390413.1` de *S. kunkelii*: **93,7 % de identidad en 412/412 aa**, E 0.
- Adhesina putativa P89 (`Q9EV58`, 798 aa) ↔ `WP_144416799.1` «ligand-binding sensor domain-containing protein» (61,7 % sobre 593 aa) y `WP_144416800.1` (73,4 % sobre 229 aa).
- Espiralina (`P19215`, 241 aa) ↔ `WP_053390819.1` «spiralin lipoprotein» (61,1 % sobre 239 aa).
- Peptidasa de señal II: en CR2-3x `WP_053390804.1`; en M3 ninguna anotación con ese nombre (sólo por nombre: no prueba ausencia génica).

## 6. Cobertura de estructuras predichas (UniProt REST + AlphaFold DB API, 2026-10-17)
- `taxonomy_id:47834` (*S. kunkelii*): 1.755 entradas UniProtKB, **1.750 con referencia a AlphaFold DB (99,7 %)**, 0 con PDB.
- `taxonomy_id:202462` (*Ca.* P. zeae): 485 entradas, **5 con AlphaFold DB (1,0 %)**, 0 con PDB. Las dos proteínas probadas (`A0ABM6DLD7`, `A0ABN4RXW7`) devuelven 404 en la API.
- Ejemplos con modelo: espiralina `A0A0K2JG54` (pLDDT medio 88,69) y RNasa III `A0A0K2JJ62` (87,62), versión 6 del modelo (2022-06-01).

## 7. Lo que NO se logró
- **Predicción de péptido señal / transmembrana local:** SignalP, TMHMM y Phobius requieren licencia y descarga con registro. Se creó el entorno `r6sp` (Python 3.10) y se instaló `deepsig-biocomp 0.9` (TensorFlow 2.21.0) desde PyPI, pero el paquete trae sólo el código: los modelos están en el repositorio de GitHub (`BioComputingUP/DeepSig`), y `git clone` falló («could not read Username for 'https://github.com'»), es decir, GitHub no es alcanzable desde este entorno. No se pidió acceso (no era fatal) y no se corrió ningún predictor de señal. Un primer intento de clonar dentro del repo falló al escribir `.git` (Operation not permitted) y no dejó archivos.
- **Predicción de estructura local** (AF2/ColabFold) para proteínas de *Ca.* P. zeae: no se corrió (sin GPU; las secuencias irían a un servicio de MSA de terceros). Sería necesaria porque AlphaFold DB cubre sólo el 1,0 % del taxón.
- `pip` por consola falla por un error de certificado SSL del entorno; las instalaciones se hicieron con el gestor de paquetes de la plataforma.
