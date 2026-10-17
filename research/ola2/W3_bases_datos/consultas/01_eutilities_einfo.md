<!-- Generado por W3 el 2026-10-17. Cada bloque es una consulta realmente ejecutada; la salida es la devuelta por el servidor, recortada donde se indica. -->
# 01 — E-utilities `einfo`: qué bases hay y cuándo se actualizaron

## Lista de bases Entrez

```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?retmode=json
```

Devuelve 38 bases:

```
pubmed, protein, nuccore, ipg, nucleotide, structure, genome, gap, grasp, annotinfo, assembly, bioproject, biosample, blastdbinfo, books, cdd, clinvar, dbvar, gene, gds, geoprofiles, medgen, mesh, nlmcatalog, omim, orgtrack, pmc, proteinclusters, pcassay, protfam, pccompound, pcsubstance, seqannot, snp, sra, taxonomy, biocollections, gtr
```

## Conteo y última actualización, base por base

```
GET einfo.fcgi?db=<db>&retmode=json   # campos count, lastupdate, description
```

| base | registros | última actualización (UTC) | descripción |
| --- | ---: | --- | --- |
| `gene` | 100.909.498 | 2026/10/17 08:08 | Gene database |
| `nuccore` | 743.915.950 | 2026/10/16 08:02 | Core Nucleotide db |
| `protein` | 1.657.446.902 | 2026/10/17 03:17 | Protein sequence record |
| `assembly` | 3.959.472 | 2026/10/16 22:09 | Genome Assembly Database |
| `sra` | 47.243.078 | 2026/10/17 09:06 | SRA Database |
| `bioproject` | 1.104.628 | 2026/10/14 15:32 | BioProject Database |
| `biosample` | 60.414.006 | 2026/10/17 00:43 | BioSample Database |
| `taxonomy` | 3.156.786 | 2026/10/13 20:58 | Taxonomy db |
| `gds` | 9.121.639 | 2026/10/16 19:51 | GEO DataSets |
| `geoprofiles` | 128.414.055 | 2024/02/20 03:42 | Genes Expression Omnibus |
| `pubmed` | 41.300.169 | 2026/10/17 06:15 | PubMed bibliographic record |
| `ipg` | 1.236.696.225 | 2026/10/17 03:13 | Identical Protein Groups DB |
| `cdd` | 67.160 | 2025/07/02 19:21 | Conserved Domain Database |
| `genome` | 88.333 | 2025/07/08 11:32 | Genomic sequences, contigs, and maps |
| `annotinfo` | 2.751 | 2026/10/16 15:10 | Annotinfo Database |
| `structure` | 260.631 | 2026/10/09 11:46 | Three-dimensional molecular model |

Observación cruda: `geoprofiles` declara `lastupdate` 2024/02/20, mientras que el resto de las bases consultadas figura actualizado en los últimos días.
