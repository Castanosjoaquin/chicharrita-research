<!-- Generado por W3 el 2026-10-17 ejecutando cada comando y redirigiendo su salida real a este archivo. -->
# 06 — EDirect en línea de comandos: la vía reproducible

Entorno: conda, canal bioconda, paquetes `entrez-direct` y `ncbi-datasets-cli`.

```
$ esearch -version
26.0
$ datasets --version
datasets version: 18.39.0
```

## E1 — Los ensamblados de *Dalbulus maidis*, con su ruta FTP

```
$ esearch -db assembly -query "txid74065[Organism:exp]" | esummary | \
    xtract -pattern DocumentSummary -element AssemblyAccession,AssemblyName,AssemblyStatus,SubmitterOrganization,FtpPath_GenBank
GCA_975739835.1	ihDalMaid1.1 alternate haplotype	Scaffold	WELLCOME SANGER INSTITUTE	ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/975/739/835/GCA_975739835.1_ihDalMaid1.1_alternate_haplotype
GCA_975739785.1	ihDalMaid1.1	Chromosome	WELLCOME SANGER INSTITUTE	ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/975/739/785/GCA_975739785.1_ihDalMaid1.1
GCA_054756405.1	CIAP v1	Contig	Instituto de Patologia Vegetal CIAP-INTA	ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/054/756/405/GCA_054756405.1_CIAP_v1
```

## E2 — Los registros maestros de TSA del vector

```
$ esearch -db nuccore -query "txid74065[Organism:exp] AND tsa_master[Properties]" | \
    efetch -format docsum | xtract -pattern DocumentSummary -element Caption,Slen,CreateDate,Title
GCWP00000000	25662	2018/11/30	TSA: Dalbulus maidis breed wildtype, transcriptome shotgun assembly
GHCC00000000	55286	2020/01/06	TSA: Dalbulus maidis, transcriptome shotgun assembly
GITV00000000	56117	2021/06/17	TSA: Dalbulus maidis, transcriptome shotgun assembly
```

## E3 — Diseño experimental de PRJNA631706 (respuesta del vector a MRFV)

```
$ esearch -db sra -query "PRJNA631706[BioProject]" | efetch -format runinfo | \
    cut -d, -f1,4,8,13,30
Run,spots,size_MB,LibraryStrategy,SampleName
SRR11822344,19098652,2549,RNA-Seq,Transcriptome of Dalbulus maidis MRFV exposed at 30C at 7 days
SRR11822347,21895394,2856,RNA-Seq,Transcriptome of Dalbulus maidis naive at 30C at 4hrs
SRR11822348,11495904,1507,RNA-Seq,Transcriptome of Dalbulus maidis naive at 30C at 4hrs
SRR11822345,24240856,3235,RNA-Seq,Transcriptome of Dalbulus maidis naive at 30C at 7 days
SRR11822346,21146219,2818,RNA-Seq,Transcriptome of Dalbulus maidis naive at 30C at 7 days
SRR11822341,23039932,3090,RNA-Seq,Transcriptome of Dalbulus maidis MRFV exposed at 30C at 7 days
SRR11822342,18493274,2546,RNA-Seq,Transcriptome of Dalbulus maidis MRFV exposed at 30C at 7 days
SRR11822343,21434834,2865,RNA-Seq,Transcriptome of Dalbulus maidis MRFV exposed at 30C at 7 days
SRR11822339,17037522,2270,RNA-Seq,Transcriptome of Dalbulus maidis naive at 30C at 4hrs
SRR11822340,22519390,2957,RNA-Seq,Transcriptome of Dalbulus maidis naive at 30C at 4hrs
SRR11822335,20926914,2750,RNA-Seq,Transcriptome of Dalbulus maidis MRFV exposed at 30C at 4hrs
SRR11822336,25686310,3372,RNA-Seq,Transcriptome of Dalbulus maidis MRFV exposed at 30C at 4hrs
SRR11822337,20268217,2660,RNA-Seq,Transcriptome of Dalbulus maidis MRFV exposed at 30C at 4hrs
SRR11822338,12396776,1634,RNA-Seq,Transcriptome of Dalbulus maidis MRFV exposed at 30C at 4hrs
SRR11822334,21336935,2801,RNA-Seq,Transcriptome of Dalbulus maidis naive at 30C at 7 days
SRR11822333,18027176,2395,RNA-Seq,Transcriptome of Dalbulus maidis naive at 30C at 7 days
```

## E4 — Suma de tamaños de ese proyecto, para el plan de ingesta

```
$ esearch -db sra -query "PRJNA631706[BioProject]" | efetch -format runinfo | \
    awk -F, 'NR>1 && $1~/SRR/ {s+=$8; b+=$5; n++} END {printf "runs=%d size_MB=%.0f bases=%.3e\n", n, s, b}'
runs=16 size_MB=42305 bases=6.381e+10
```

## E5 — Lo que NO corrió: el cliente `datasets`

El binario se instaló y responde `--version`, pero toda llamada de red falla contra el proxy TLS del entorno. Se intentó también con `SSL_CERT_FILE` apuntando al bundle de certifi, sin cambio. `curl` contra el mismo endpoint devuelve 200, así que el bloqueo es del cliente Go, no del dominio.

```
$ datasets summary genome accession GCF_001712875.1 --report ids_only
Error: [gateway] Post "https://api.ncbi.nlm.nih.gov/datasets/v2/genome/dataset_report": POST https://api.ncbi.nlm.nih.gov/datasets/v2/genome/dataset_report giving up after 11 attempt(s): Post "https://api.ncbi.nlm.nih.gov/datasets/v2/genome/dataset_report": tls: failed to verify certificate: x509: OSStatus -26276
$ curl -s -o /dev/null -w "status=%{http_code}\n" https://api.ncbi.nlm.nih.gov/datasets/v2/version
status=200
```

Las mismas consultas se resolvieron por REST con Python (archivo 03); el servicio y la versión son los mismos, 18.39.0.
