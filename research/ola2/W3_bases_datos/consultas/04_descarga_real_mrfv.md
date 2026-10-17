<!-- Generado por W3 el 2026-10-17. Cada bloque es una consulta realmente ejecutada; la salida es la devuelta por el servidor, recortada donde se indica. -->
# 04 — Descarga real por API: genoma y anotación de *Maize rayado fino virus*

Secuencia pública de referencia, elegida justamente para no tocar material del corpus.

```
GET https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_000862485.2/download?include_annotation_type=GENOME_FASTA&include_annotation_type=GENOME_GFF&include_annotation_type=PROT_FASTA&include_annotation_type=CDS_FASTA
```

Respuesta: HTTP 200. 10.394 bytes de ZIP. Contenido:

```
README.md                                                                  1593 bytes
ncbi_dataset/data/assembly_data_report.jsonl                               1124 bytes
ncbi_dataset/data/GCF_000862485.2/cds_from_genomic.fna                     7779 bytes
ncbi_dataset/data/GCF_000862485.2/GCF_000862485.2_ViralProj15381_genomic.fna     6520 bytes
ncbi_dataset/data/GCF_000862485.2/genomic.gff                              1268 bytes
ncbi_dataset/data/GCF_000862485.2/protein.faa                              2596 bytes
ncbi_dataset/data/dataset_catalog.json                                      845 bytes
md5sum.txt                                                                  512 bytes
```

Primeras líneas del FASTA genómico:

```
>lcl|NC_002786.2_cds_NP_115454.2_1 [locus_tag=IM012_gp1] [db_xref=GeneID:921087] [protein=polyprotein] [protein_id=NP_115454.2] [location=127..6213] [gbkey=CDS]
ATGTCTAGTTTCCTGCGTGGTGGTCATCTCCTTAGCGGAGTCGAGTCCCTTACCCCCACCACCCATCGCGACACCATCAC
TGCACCCATTGTCGAGTCCCTTGCCACTCCTCTTCGCCGATCCCTCGAACGCTACCCTTGGTCCATCCCAAAGGAGTTCC
```

El GFF3 completo, que son 1.268 bytes, declara dos CDS sobre `NC_002786.2`:

```
NC_002786.2	RefSeq	CDS	127	6213	.	+	0	ID=cds-NP_115454.2;Parent=gene-IM012_gp1;Dbxref=GenBank:NP_115454.2,GeneID:921087;Name=NP_115454.2;Note=contains methyltransferase%2C helicase%2C protease%2C replicase%2C capsid proteins;gbkey=CDS;locus_tag=IM012_gp1;product=polyprotein;protein_id=NP_115454.2
NC_002786.2	RefSeq	CDS	332	1594	.	+	0	ID=cds-NP_115455.2;Parent=gene-IM012_gp2;Dbxref=GenBank:NP_115455.2,GeneID:921088;Name=NP_115455.2;gbkey=CDS;locus_tag=IM012_gp2;product=putative movement protein;protein_id=NP_115455.2
```

Verificación de que el archivo bajado es usable: se abrió el ZIP, se leyó el FASTA y el GFF desde el propio archivo.
