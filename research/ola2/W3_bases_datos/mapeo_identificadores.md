# Cómo se cruzan los identificadores entre las bases

Esta es la parte que después permite juntar fuentes. Todo lo que figura acá se
verificó con una consulta ejecutada; los comandos y las salidas están en
`consultas/07_mapeo_ids_ejecutado.md`.

## El mapa en una página

```
                         TaxID  (NCBI Taxonomy, p. ej. 74065 = Dalbulus maidis)
                           |
     +---------------------+---------------------+--------------------+
     |                     |                     |                    |
  assembly              nuccore               protein              sra / biosample
  GCA_*/GCF_*        accesión.versión      WP_/NP_/XP_/           SRR* / SAMN*
     |                     |                 traducción              |
     |  GCA  <--- mismo genoma, dos anotaciones --->  GCF            |
     |                     |                     |                   |
     |                     |                   IPG id  <-- une INSDC con RefSeq
     |                     |                     |
     |                  GeneID (NCBI Gene) ------+
     |                     |
     |                     +--> UniProt (accesión) --> KEGG (org:gen) --> KO
     |
     +--> BioProject PRJ* --> BioSample SAM* --> corridas SRR*
```

## Las reglas, una por una

**TaxID es la llave maestra.** Todas las bases de secuencia aceptan
`txid<N>[Organism:exp]`, que expande el taxón a sus descendientes. Sin el
sufijo `:exp` se pierden las cepas: `GCF_001274875.1` está bajo
*Spiroplasma kunkelii* CR2-3x, TaxID 273035, que es hija de 47834. El conteo de
proteínas cambia de 3.530 a 3.647 según se use una u otra, y eso explica
discrepancias que de otro modo parecen errores. [E]

**La accesión de ensamblado dice en qué mundo estás.** `GCA_` es el depósito
original del autor en GenBank; `GCF_` es la copia de RefSeq del mismo
ensamblado, con la anotación del NCBI. Comparten los nueve dígitos y la versión:
`GCA_001712875.1` y `GCF_001712875.1` son el mismo genoma del fitoplasma. Lo que
no comparten es la anotación: la de GenBank es la que envió Academia Sinica en
2016 y la de RefSeq es `GCF_001712875.1-RS_2026_06_07`. Si dos resultados no
coinciden, lo primero que hay que mirar es esto. [E]

**Los contigs siguen la misma regla:** `CP015149.1` en GenBank, `NZ_CP015149.1`
en RefSeq. El prefijo `NZ_` marca un contig de RefSeq de origen WGS; `NC_` es
una secuencia completa de referencia, como `NC_002786.2` (MRFV) o `NC_070066.1`
(mitogenoma del vector). [E]

**Para cruzar proteínas entre los dos mundos, Identical Protein Groups.** Una
sola llamada devuelve las dos caras:

```
efetch -db protein -id AOF54549 -rettype ipg
117106682  INSDC   CP015149.1     1  1524  +  AOF54549.1       GCA_001712875.1
117106682  RefSeq  NZ_CP015149.1  1  1524  +  WP_069027986.1   GCF_001712875.1
```

El grupo 117106682 une la proteína depositada por el autor con la de RefSeq,
con contig, coordenadas, hebra y ensamblado de cada una. Es el puente más
confiable que encontramos, y el único que resuelve el caso de KEGG, abajo. [E]

**GeneID sólo existe si hay anotación RefSeq.** Es el identificador de la base
`gene` y la bisagra hacia transcriptos, proteínas y literatura:
`elink -dbfrom gene -db protein -id 921087` devuelve la proteína RefSeq y la de
GenBank, y `-db pubmed` devuelve el artículo que describe el gen. Pero para
*Dalbulus maidis* esa bisagra no existe fuera de la mitocondria, y para
'*Candidatus* Phytoplasma zeae' no existe en absoluto: cero registros en `gene`
con 524 genes codificantes anotados. **Toda nuestra tubería tiene que estar
pensada para funcionar sin GeneID.** [E]

**Los transcriptos de TSA no tienen GeneID ni nombre de gen.** La accesión de un
transcripto de `GITV01` identifica una secuencia, nada más. El nombre funcional
hay que ponérselo nosotros, y la vía es la homología: `blastx` o `diamond`
contra el proteoma de *Macrosteles quadrilineatus* (`GCF_028750875.1`, 21.979
proteínas) o contra Swiss-Prot, y de ahí al nombre del gen. [H] Es una hipótesis
de método, no un procedimiento validado por nosotros.

**RefSeq ↔ UniProt, con la API de mapeo de UniProt.** Ejecutado:
`WP_053391442.1` → `A0A0K2JJJ7` (`A0A0K2JJJ7_SPIKU`, TrEMBL, *Spiroplasma
kunkelii* CR2-3x, TaxID 273035, proteoma `UP000062963`). Y el caso que falla
también enseña: `NP_115454.2`, la poliproteína de MRFV, no tiene entrada en
UniProtKB y lo único que devuelve el servicio es el identificador de UniParc
`UPI001164A0BC`. Para los virus del complejo, la anotación funcional hay que
buscarla en el GFF3 de RefSeq, no en UniProt. [E]

**KEGG ↔ NCBI, con una trampa.** Los dos patógenos están en KEGG: `skn`
(T04056, *S. kunkelii* CR2-3x) y `mbp` (T04456, '*Ca.* Phytoplasma zeae' M3).
`conv/ncbi-proteinid/mbp` devuelve 485 pares, pero apuntan a las accesiones de
**GenBank** (`mbp:MBSPM3_v1c0010` → `ncbi-proteinid:AOF54549`), no a las `WP_`
de RefSeq. Es decir: KEGG está anclado a la anotación de 2016 del depósito
original, y si nuestro proteoma viene de RefSeq hay que pasar por IPG para
cruzarlos. `conv/ncbi-geneid/mbp` devuelve HTTP 400, consistente con que el
fitoplasma no tenga GeneID. Para el espiroplasma, `conv/uniprot/skn` devuelve
1.685 pares, que es el camino corto hacia la anotación funcional. [E]

**BioProject y BioSample son el índice del material crudo.** `elink` encadena
`assembly → biosample → sra` y `assembly → bioproject`. Verificado sobre el
ensamblado de *Macrosteles*: uid 15950891 → BioSample 32944381 → corrida de SRA
43844714, y BioProjects 944995 y 928792. La misma cadena, en sentido inverso,
es la que responde «¿de qué muestra salió este ensamblado?». [E]

## Tabla de conversión rápida

| de | a | cómo | verificado |
| --- | --- | --- | --- |
| nombre científico | TaxID | `esearch -db taxonomy -query '"<nombre>"[Scientific Name]'` | sí, 24 taxones |
| TaxID | ensamblados | Datasets `genome/taxon/{taxid}/dataset_report` | sí |
| GCA_ | GCF_ | mismos dígitos y versión; confirmar con `dataset_report` | sí |
| accesión de proteína INSDC | accesión RefSeq | `efetch -db protein -rettype ipg` | sí |
| GeneID | proteína / nucleótido / PubMed | `elink -dbfrom gene -db protein\|nuccore\|pubmed` | sí |
| RefSeq de proteína | UniProt | `POST rest.uniprot.org/idmapping/run from=RefSeq_Protein` | sí |
| KEGG `org:gen` | proteína del NCBI | `rest.kegg.jp/conv/ncbi-proteinid/<org>` | sí |
| KEGG `org:gen` | UniProt | `rest.kegg.jp/conv/uniprot/<org>` | sí |
| ensamblado | BioSample / BioProject / SRA | `elink` en cadena | sí |
| transcripto de TSA | nombre de gen | no hay mapeo directo; homología contra un proteoma anotado | no: es una propuesta |
