# W5 — comandos y salidas reales

Todo lo que sigue se corrió el 17 de octubre de 2026 en el entorno conda `w5bio`
(creado para esta investigación: `biopython 1.88`, `blast 2.17.0`, `viennarna 2.7.2`,
`python 3.11`, canales conda-forge y bioconda). **Ninguna secuencia de EPILAB salió
de la máquina**: no se usó el BLAST web del NCBI, ni dsRNA-Engineer, ni ningún
servidor de plegado. Lo único que viajó por la red fue la descarga de referencias
públicas desde el NCBI (sentido entrante) y consultas de metadatos por E-utilities
sobre accesos públicos.

Copias de trabajo y material pesado: `work/W5/` (fuera del control de versiones).
Las salidas crudas de BLAST con decenas de miles de líneas quedaron en
`work/W5/blast_crudo/`; en esta carpeta están las tablas resumidas y las salidas
chicas. Las secuencias en sí no se reproducen en ningún archivo de `research/`.

## 0. Lectura de la planilla

```bash
cp YHat-Biotech/Sequences_EPILAB.xlsx work/W5/          # md5 048833f606d9aba2a1220a7dc280d9a9, idéntico al original
python  # descompresión del .xlsx y parseo del XML (xl/worksheets/sheet1.xml, xl/sharedStrings.xml)
```

Resultado: una hoja (`Hoja1`), ocho columnas, cuatro filas de datos, tres rangos
combinados (`G1:H1`, `A2:A3`, `A4:A5`). Metadatos del documento: creador y último
modificador `Johan Rodríguez`, creado 2026-10-17T15:03:07Z, modificado 15:10:01Z,
Microsoft Excel 16.0300. Verificado además que cada «secuencia elegida» es
subcadena exacta de su «full sequence».

## 1. Referencias públicas descargadas (entrantes, a disco local)

```bash
# genomas y transcriptomas de referencia
curl -O https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/975/739/785/GCA_975739785.1_ihDalMaid1.1/GCA_975739785.1_ihDalMaid1.1_genomic.fna.gz
curl -O https://ftp.ncbi.nlm.nih.gov/genomes/refseq/plant/Zea_mays/latest_assembly_versions/GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0/..._rna.fna.gz
curl -O .../Apis_mellifera/.../GCF_003254395.2_Amel_HAv3.1_rna.fna.gz
curl -O .../Harmonia_axyridis/.../GCF_914767665.1_icHarAxyr1.1_rna.fna.gz
curl -O .../Folsomia_candida/.../GCF_002217175.1_ASM221717v1_rna.fna.gz
curl -O .../Homalodisca_vitripennis/.../GCF_021130785.1_UT_GWSS_2.1_rna.fna.gz
# los 71 registros de MRFV y el GenBank de la referencia, por E-utilities
efetch db=nuccore rettype=fasta  -> ref/MRFV_all_nuccore.fasta
efetch db=nuccore id=NC_002786.2 rettype=gb -> ref/NC_002786.2.gb
# proteínas públicas para tblastn: NP_115454.2, NP_115455.2, bicaudal C (4 especies), V-ATPasa D (6 registros)
# transcriptomas TSA de D. maidis, por lotes de 300 accesos (efetch POST):
#   GITV01 56.117 contigs (Xu et al., Ohio State), GHCC01 55.286, GCWP01 25.662 (Johnson et al., INHS)
```

Salidas: `work/W5/logs/01_ncbi_query.log`, `02_assemblies.log`, `03_descargas.log`,
`04_efetch.log`, `05_efetch_vatpase.log`.

## 2. Bases de datos locales y alineamientos de identificación

```bash
makeblastdb -in fasta/epilab_full.fasta -dbtype nucl -out db/epilab_full
makeblastdb -in ref/MRFV_all_nuccore.fasta -dbtype nucl -out db/MRFV_all
# (idem para los seis conjuntos de referencia y los tres TSA)
blastn  -query fasta/epilab_full.fasta -db db/MRFV_all      -evalue 1e-10   # -> blastn_epilab_vs_MRFV.tsv
tblastn -query ref/prot_all.faa        -db db/epilab_full   -evalue 1e-5    # -> tblastn_proteinas_vs_epilab.tsv
blastn  -query fasta/epilab_full.fasta -db db/GCA_975739785.1_ihDalMaid1.1_genomic -evalue 1e-20  # -> full_vs_DalMaid_genoma.tsv
blastn  -query fasta/{BicC_Dm,ATPaseD_Dm}_full.fasta -db db/TSA_{GITV01,GHCC01,GCWP01} -evalue 1e-50  # -> provenencia_tsa.tsv
```

## 3. Caracterización de secuencia y estructura

```bash
sed '/^>/!y/Tt/Uu/' fasta/epilab_full.fasta > fold/epilab_full_rna.fa
RNAfold -p --noPS --noDP -T 25 < fold/epilab_full_rna.fa   # -> rnafold_resumen.tsv
RNAfold -p --noPS --noDP -T 25 < fold/epilab_sel_rna.fa
RNAplfold -u 8 -L 40 -W 80 < plfold/<gen>.rna.fa           # -> probabilidades de tramo desapareado
dustmasker -in fasta/epilab_full.fasta -outfmt acclist     # -> dustmasker_full.txt
```

Composición, ORF en los seis marcos y unicidad de 21-meros: código propio con
Biopython (`work/W5/composicion.json`).

## 4. Tamizaje de off-targets

```bash
# 920 ventanas de 21 nt de las cuatro regiones elegidas (4 x 280 o 180)
blastn -task blastn-short -query fasta/sirnas_21nt_sel.fasta -db db/<cada_referencia> \
       -word_size 11 -perc_identity 85 -dust no -evalue 100 -max_target_seqs 20 -num_threads 8
# filtro posterior (awk): coincidencia perfecta >=19 nt contiguos, 21/21 perfecto, 21 nt con 1 desajuste
# -> offtarget_resumen.tsv ; crudos en work/W5/blast_crudo/
blastn -task blastn -query fasta/epilab_sel.fasta -db db/<cada_referencia> -evalue 1e-3 -word_size 11
# -> region_vs_<referencia>.tsv
```

## 5. Conservación de las regiones virales entre aislados

```bash
blastn -query fasta/epilab_sel.fasta -db db/MRFV_all -outfmt "... btop" -evalue 1e-5 -max_target_seqs 100
# reconstrucción de posiciones con desajuste desde el btop -> mrfv_conservacion_aislados.txt
# control independiente por búsqueda de subcadena exacta de cada 21-mero en cada registro
# -> mrfv_sirna_identicos_por_aislado.txt  (los dos métodos coinciden: 158, 151, 113, 96, 77, mediana 44)
```

## 6. Ingeniería inversa de «Nro de eficientes por gen»

Reimplementación local de las reglas publicadas (nucleótido terminal, asimetría
termodinámica por vecino más cercano de Xia et al. 1998, accesibilidad local con
RNAplfold, Reynolds et al. 2004, Ui-Tei et al. 2004, Tuschl) y búsqueda en rejilla
de 2.132 combinaciones de filtros.

Salidas: `sirna_criterios_conteos.tsv`, `sirna_grid_busqueda.tsv`.

## Lo que NO se corrió, y por qué

- **dsRNA-Engineer sobre las secuencias de EPILAB**: es un servicio web que procesa
  del lado del servidor. Prohibido por la regla de confidencialidad. W2 lo corrió
  con una secuencia pública (`research/ola2/W2_herramientas/ejemplos/`).
- **BLAST web del NCBI**: mismo motivo. Todo el BLAST de esta investigación es
  BLAST+ 2.17.0 local.
- **si-Fi21 original**: es un ejecutable de Windows con interfaz gráfica; no se
  instaló. Lo que se corrió es nuestra reimplementación de sus criterios
  documentados, que no es lo mismo y se reporta como tal.
- **Validación experimental de cualquier tipo**: el equipo no tiene laboratorio.
