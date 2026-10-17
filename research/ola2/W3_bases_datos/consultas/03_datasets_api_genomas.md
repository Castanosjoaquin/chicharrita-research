<!-- Generado por W3 el 2026-10-17. Cada bloque es una consulta realmente ejecutada; la salida es la devuelta por el servidor, recortada donde se indica. -->
# 03 — NCBI Datasets v2: informes de ensamblado, anotación y tamaños

Versión del servicio en el momento de la corrida:

```
GET https://api.ncbi.nlm.nih.gov/datasets/v2alpha/version   -> {"version":"18.39.0","major_ver":18,"minor_ver":39}
GET https://api.ncbi.nlm.nih.gov/datasets/v2/version        -> {"version":"18.39.0","major_ver":18,"minor_ver":39}
```

## Todos los ensamblados de un taxón

```
GET /datasets/v2alpha/genome/taxon/{TAXID}/dataset_report?filters.assembly_version=all_assemblies&page_size=100
```

| taxón | accesión | nivel | nombre | secuencias | largo total (pb) | N50 de contig | anotación |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| Dalbulus maidis | `GCA_975739785.1` | Chromosome | ihDalMaid1.1 | 499 | 972.206.121 | 5.293.657 | (ninguna) |
| Dalbulus maidis | `GCA_975739835.1` | Scaffold | ihDalMaid1.1 alternate haplotype | 8.928 | 488.450.451 | 328.147 | (ninguna) |
| Dalbulus maidis | `GCA_054756405.1` | Contig | CIAP v1 | 22.333 | 585.210.080 | 50.514 | (ninguna) |
| Spiroplasma kunkelii | `GCA_001274875.1` | Complete Genome | ASM127487v1 | 4 | 1.514.561 | 1.463.926 | Annotation submitted by Beltsville Agricultural Research Center / 2015-11-05 |
| Spiroplasma kunkelii | `GCF_001274875.1` | Complete Genome | ASM127487v1 | 4 | 1.514.561 | 1.463.926 | GCF_001274875.1-RS_2025_12_13 / 2025-12-13 |
| Ca. Phytoplasma zeae | `GCA_001712875.1` | Complete Genome | ASM171287v1 | 1 | 576.118 | 576.118 | Annotation submitted by Academia Sinica / 2016-08-25 |
| Ca. Phytoplasma zeae | `GCF_001712875.1` | Complete Genome | ASM171287v1 | 1 | 576.118 | 576.118 | GCF_001712875.1-RS_2026_06_07 / 2026-06-07 |
| Maize rayado fino virus | `GCA_000862485.2` | Complete Genome | ViralProj15381 | 1 | 6.366 | 6.366 | (ninguna) |
| Maize rayado fino virus | `GCF_000862485.2` | Complete Genome | ViralProj15381 | 1 | 6.366 | 6.366 | Annotation submitted by NCBI RefSeq / 2020-10-13 |
| Maize rayado fino virus | `GCA_000862485.1` | Complete Genome | ViralProj15381 | 1 | 6.305 | 6.305 | (ninguna) |
| Maize rayado fino virus | `GCF_000862485.1` | Complete Genome | ViralProj15381 | 1 | 6.305 | 6.305 | Annotation submitted by NCBI RefSeq / 2015-02-13 |
| Macrosteles quadrilineatus | `GCA_028750875.1` | Scaffold | UCM_ALF_1.0 | 2.177 | 1.317.891.973 | 3.405.181 | (ninguna) |
| Macrosteles quadrilineatus | `GCF_028750875.1` | Scaffold | UCM_ALF_1.0 | 2.177 | 1.317.891.973 | 3.405.181 | GCF_028750875.1-RS_2023_03 / 2023-03-16 |
| Macrosteles quadrilineatus | `GCA_976628355.1` | Chromosome | ihMacQuai1.hap1.1 | 1.118 | 1.090.416.117 | 20.951.441 | (ninguna) |
| Macrosteles quadrilineatus | `GCA_976823985.1` | Scaffold | ihMacQuai1.hap2.1 | 796 | 1.025.595.532 | 21.274.608 | (ninguna) |

## Ficha por accesión, con conteo de genes de la anotación

```
GET /datasets/v2alpha/genome/accession/{ACC}/dataset_report
```

| accesión | organismo | nivel | largo (pb) | anotación | genes totales | codificantes | no codificantes | pseudogenes |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: |
| `GCA_975739785.1` | Dalbulus maidis | Chromosome | 972.206.121 | (ninguna) | — | — | — | — |
| `GCA_054756405.1` | Dalbulus maidis | Contig | 585.210.080 | (ninguna) | — | — | — | — |
| `GCF_001274875.1` | Spiroplasma kunkelii CR2-3x | Complete Genome | 1.514.561 | GCF_001274875.1-RS_2025_12_13 | 1.951 | 1.775 | 39 | 137 |
| `GCF_001712875.1` | Candidatus Phytoplasma zeae | Complete Genome | 576.118 | GCF_001712875.1-RS_2026_06_07 | 581 | 524 | 41 | 16 |
| `GCF_000862485.2` | Maize rayado fino virus | Complete Genome | 6.366 | Annotation submitted by NCBI RefSeq | 2 | 2 | 0 | 0 |
| `GCF_028750875.1` | Macrosteles quadrilineatus | Scaffold | 1.317.891.973 | GCF_028750875.1-RS_2023_03 | 24.178 | 21.979 | 2.096 | 103 |
| `GCF_902167145.1` | Zea mays | Chromosome | 2.182.075.994 | GCF_902167145.1-RS_2025_02 | 49.888 | 34.313 | 10.353 | 5.222 |

## Tamaños de descarga declarados por el servicio

```
GET /datasets/v2alpha/genome/accession/{ACC}/download_summary?include_annotation_type={TIPO}
```

Campo `available_files`, en MB (valores devueltos por el NCBI, no estimados por nosotros):

| accesión | genoma FASTA | GFF3 | GTF | ARN FASTA | proteína FASTA | CDS FASTA | GBFF |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `GCA_975739785.1` | 268.629 | — | — | — | — | — | 361.275 |
| `GCA_054756405.1` | 171.581 | — | — | — | — | — | 235.475 |
| `GCF_902167145.1` | 619.975 | 15.403 | 15.352 | 36.026 | 12.188 | 17.510 | 881.222 |
| `GCF_028750875.1` | 374.544 | 8.934 | 8.693 | 20.389 | 7.704 | 14.491 | 511.191 |
| `GCF_001274875.1` | 0.396 | 0.128 | 0.169 | — | 0.216 | 0.384 | 0.991 |
| `GCF_001712875.1` | 0.155 | 0.047 | 0.061 | — | 0.092 | 0.148 | 0.382 |
| `GCF_000862485.2` | 0.002 | 0.001 | 0.000 | — | 0.002 | 0.002 | 0.006 |
