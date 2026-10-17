<!-- Generado por W3 el 2026-10-17. Cada bloque es una consulta realmente ejecutada; la salida es la devuelta por el servidor, recortada donde se indica. -->
# 05 — Transcriptomas ensamblados (TSA) y rutas FTP, con tamaños medidos

## Los registros maestros de TSA de *Dalbulus maidis*

```
GET esearch.fcgi?db=nuccore&term=txid74065[Organism:exp] AND tsa_master[Properties]
GET esummary.fcgi?db=nuccore&id=2054345881,1789777666,1524754193&retmode=json
```

| accesión maestra | secuencias | fecha | título |
| --- | ---: | --- | --- |
| `GITV00000000` | 56.117 | 2021/06/17 | TSA: Dalbulus maidis, transcriptome shotgun assembly |
| `GHCC00000000` | 55.286 | 2020/01/06 | TSA: Dalbulus maidis, transcriptome shotgun assembly |
| `GCWP00000000` | 25.662 | 2018/11/30 | TSA: Dalbulus maidis breed wildtype, transcriptome shotgun assembly |

## Estadísticas oficiales de cada conjunto TSA

```
GET https://ftp.ncbi.nlm.nih.gov/genbank/tsa/G/stats.tsa.{GITV,GHCC,GCWP}
```

```
NCBI_TSA_master|GITV|01|NT-Sequences|56117|Basepairs|94702486|NT-Largest|205383|NT-Smallest|200
NCBI_TSA_master|GHCC|01|NT-Sequences|55286|Basepairs|38748947|NT-Largest|8162|NT-Smallest|201
NCBI_TSA_master|GCWP|01|NT-Sequences|25662|Basepairs|28305469|NT-Largest|9283|NT-Smallest|203
```

Es decir: GITV01 son 56.117 secuencias y 94.702.486 pb, con la más larga de 205.383 nt y la más corta de 200 nt.

## Tamaños de archivo medidos con HTTP HEAD

```
HEAD https://ftp.ncbi.nlm.nih.gov/<ruta>   # se lee Content-Length y Last-Modified
```

| archivo | tamaño | última modificación |
| --- | ---: | --- |
| `genbank/tsa/G/tsa.GITV.1.fsa_nt.gz` | 31,44 MB | 2021-06-18 |
| `genbank/tsa/G/tsa.GITV.1.gbff.gz` | 45,89 MB | 2021-06-18 |
| `genbank/tsa/G/tsa.GHCC.1.fsa_nt.gz` | 10,74 MB | 2020-03-30 |
| `genbank/tsa/G/tsa.GCWP.1.fsa_nt.gz` | 7,20 MB | 2018-12-01 |
| `genomes/all/GCF/028/750/875/GCF_028750875.1_UCM_ALF_1.0/..._rna.fna.gz` | 21,38 MB | 2023-03-22 |
| `genomes/all/GCF/902/167/145/GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0/..._rna.fna.gz` | 37,78 MB | 2025-02-20 |

Ruta que **no** existe, probada y descartada: `sra/wgs_aux/GI/TV/GITV01/` devuelve HTTP 404. Los TSA de GenBank viven en `genbank/tsa/<inicial>/`.
