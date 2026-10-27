# F1 — comandos exactos

Todo desde la raíz del repositorio. Nada de esto sube una secuencia a un servicio.

```bash
# 1. Entorno (diamond 2.2.8 de bioconda para Apple Silicon; brew no sirvió: pedía aceptar la licencia de Xcode)
conda create -y -n f1_homologia -c bioconda -c conda-forge diamond=2.2.8 python=3.11 numpy

# 2. Insumos en work/F1 (no se versiona). Los dos proteomas son RefSeq públicos del NCBI.
mkdir -p work/F1/ref && cd work/F1/ref
curl -O https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/028/750/875/GCF_028750875.1_UCM_ALF_1.0/GCF_028750875.1_UCM_ALF_1.0_protein.faa.gz
curl -O https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/021/130/785/GCF_021130785.1_UT_GWSS_2.1/GCF_021130785.1_UT_GWSS_2.1_protein.faa.gz
gunzip -k *.faa.gz && cd ../../..
cp ~/Downloads/Dalbulus_maidis_transcriptome_GITV01.fas work/F1/GITV01.fas   # md5 bee70da94d1541fb371f10e4e358b6c8

# 3. Pruebas, corrida, controles y resumen
P=/opt/miniconda3/envs/f1_homologia/bin/python; F=research/ola6/F1_transferencia_homologia
$P $F/scripts/test_transferir_anotacion.py
$P $F/scripts/transferir_anotacion.py work/F1/GITV01.fas $F/resultados \
  MQ=work/F1/ref/GCF_028750875.1_UCM_ALF_1.0_protein.faa HV=work/F1/ref/GCF_021130785.1_UT_GWSS_2.1_protein.faa
$P $F/scripts/controles.py
$P $F/scripts/resumir.py
```

Los md5 de los dos proteomas se verifican contra `md5checksums.txt` de cada directorio del NCBI.
La corrida entera tarda unos tres minutos en un portátil con Apple Silicon.
