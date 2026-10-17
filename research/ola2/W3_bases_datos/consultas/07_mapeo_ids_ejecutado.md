<!-- Generado por W3 el 2026-10-17. Cada bloque es una consulta realmente ejecutada; la salida es la devuelta por el servidor, recortada donde se indica. -->
# 07 — Cruce de identificadores, ejecutado

## INSDC ↔ RefSeq con Identical Protein Groups

```
GET efetch.fcgi?db=protein&id=AOF54549&rettype=ipg&retmode=text
```

```
Id	Source	Nucleotide Accession	Start	Stop	Strand	Protein	Protein Name	Organism	Strain	Assembly
117106682	INSDC	CP015149.1	1	1524	+	AOF54549.1	chromosomal replication initiation protein	Candidatus Phytoplasma zeae	M3	GCA_001712875.1
117106682	RefSeq	NZ_CP015149.1	1	1524	+	WP_069027986.1	chromosomal replication initiator protein DnaA	Candidatus Phytoplasma zeae	M3	GCF_001712875.1
```

Una sola fila de IPG une la proteína de la versión GenBank del genoma del fitoplasma con la de la versión RefSeq, con su contig, sus coordenadas y las dos accesiones de ensamblado.

## KEGG ↔ NCBI

```
GET https://rest.kegg.jp/find/genome/kunkelii
GET https://rest.kegg.jp/find/genome/zeae
```

```
T04056	skn; Spiroplasma kunkelii CR2-3x
T04456	mbp; Candidatus Phytoplasma zeae M3 (Maize bushy stunt phytoplasma M3)
```

```
GET https://rest.kegg.jp/conv/ncbi-proteinid/mbp     # 485 líneas
```

```
mbp:MBSPM3_v1c0010	ncbi-proteinid:AOF54549
mbp:MBSPM3_v1c0020	ncbi-proteinid:AOF54550
mbp:MBSPM3_v1c0030	ncbi-proteinid:AOF54551
...
```

```
GET https://rest.kegg.jp/conv/uniprot/skn           # 1685 líneas
```

```
skn:SKUN_001	up:A0A0K2JET4
skn:SKUN_0010	up:A0A0K2JEC0
skn:SKUN_00100	up:A0A0K2JEL5
...
```

```
GET https://rest.kegg.jp/conv/ncbi-geneid/mbp       -> HTTP 400, respuesta vacía
```

## RefSeq ↔ UniProtKB

```
POST https://rest.uniprot.org/idmapping/run  from=RefSeq_Protein to=UniProtKB ids=WP_053391442.1
GET  https://rest.uniprot.org/idmapping/status/<jobId>
```

```
{
 "from": "WP_053391442.1",
 "primaryAccession": "A0A0K2JJJ7",
 "uniProtkbId": "A0A0K2JJJ7_SPIKU",
 "entryType": "UniProtKB unreviewed (TrEMBL)",
 "organism": "Spiroplasma kunkelii CR2-3x",
 "taxonId": 273035
}
```

Y el caso que falla, que también es información:

```
POST .../idmapping/run  ids=NP_115454.2   (poliproteína de MRFV en RefSeq)
-> {"results":[],"suggestedIds":[{"from":"NP_115454.2","to":"UPI001164A0BC"}],"obsoleteCount":0}
```

La proteína viral no tiene entrada en UniProtKB; lo único que devuelve es un identificador de UniParc.

## Cadena Entrez con `elink`

```
GET elink.fcgi?dbfrom=assembly&db=biosample&id=15950891   -> assembly_biosample: 32944381
GET elink.fcgi?dbfrom=assembly&db=bioproject&id=15950891 -> assembly_bioproject: 944995, 928792
GET elink.fcgi?dbfrom=biosample&db=sra&id=32944381       -> biosample_sra: 43844714
GET elink.fcgi?dbfrom=gene&db=protein&id=921087          -> gene_protein: 1916861540, 1701843498; gene_protein_refseq: 1916861540
GET elink.fcgi?dbfrom=gene&db=pubmed&id=921087           -> gene_pubmed: 11289816
```

El uid 15950891 es el de `GCF_028750875.1` en la base `assembly`; el GeneID 921087 es el de la poliproteína de MRFV.
