<!-- Generado por W3 el 2026-10-17. Cada bloque es una consulta realmente ejecutada; la salida es la devuelta por el servidor, recortada donde se indica. -->
# 02 — Cobertura por organismo en cada base Entrez
Consulta ejecutada, una por celda de la tabla:

```
GET esearch.fcgi?db=<db>&term=txid<TAXID>[Organism:exp]&rettype=count&retmode=json
```

`[Organism:exp]` expande el taxón a todos sus descendientes. Los taxid se resolvieron con `esearch.fcgi?db=taxonomy&term="<nombre>"[Scientific Name]`.

| organismo | taxid | gene | nuccore | protein | assembly | sra | biosample | bioproject | gds (GEO) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dalbulus maidis | 74065 | 37 | 92 | 87 | 3 | 37 | 45 | 17 | 0 |
| Dalbulus (género) | 74053 | 37 | 124 | 98 | 5 | 40 | 52 | 21 | 0 |
| Cicadellidae (familia) | 30102 | 56.026 | 347.492 | 333.699 | 59 | 2.930 | 3.930 | 636 | 25 |
| Zea mays | 4577 | 72.398 | 4.890.322 | 377.650 | 204 | 186.342 | 167.801 | 6.499 | 24.701 |
| Spiroplasma kunkelii | 47834 | 20 | 507 | 3.647 | 1 | 1 | 6 | 3 | 0 |
| Ca. Phytoplasma zeae | 202462 | 0 | 78 | 1.066 | 1 | 6 | 6 | 4 | 0 |
| Mollicutes (clase) | 31969 | 51.249 | 98.477 | 885.140 | 3.104 | 1.548 | 8.365 | 935 | 47 |
| Maize rayado fino virus | 59749 | 3 | 71 | 67 | 2 | 0 | 0 | 0 | 0 |
| Maize striate mosaic virus | 2025388 | 9 | 19 | 73 | 2 | 0 | 0 | 0 | 0 |
| Maize stripe virus | 3052767 | 9 | 77 | 131 | 1 | 0 | 0 | 0 | 0 |
| Diaphorina citri | 121845 | 31.912 | 252.391 | 95.854 | 10 | 808 | 1.248 | 86 | 14 |
| Nephotettix cincticeps | 94400 | 37 | 535 | 441 | 1 | 40 | 33 | 17 | 25 |
| Macrosteles quadrilineatus | 74068 | 24.179 | 38.771 | 35.221 | 3 | 34 | 41 | 15 | 0 |
| Graminella nigrifrons | 30127 | 0 | 37.565 | 25 | 0 | 56 | 56 | 8 | 0 |
| Euscelidius variegatus | 13064 | 0 | 142 | 132 | 1 | 19 | 61 | 5 | 0 |
| Nilaparvata lugens | 108931 | 29.502 | 338.438 | 35.943 | 4 | 2.187 | 2.261 | 200 | 36 |
| Tribolium castaneum | 7070 | 19.371 | 129.093 | 42.666 | 7 | 2.636 | 2.579 | 149 | 793 |
| Apis mellifera | 7460 | 21.375 | 398.812 | 62.955 | 17 | 26.520 | 35.878 | 728 | 3.272 |
| Bombus terrestris | 30195 | 15.804 | 303.519 | 28.096 | 5 | 4.860 | 5.665 | 101 | 224 |
| Chrysoperla carnea | 189513 | 15.868 | 20.224 | 17.827 | 5 | 23 | 20 | 13 | 0 |
| Coccinella septempunctata | 41139 | 16.934 | 26.554 | 24.091 | 3 | 293 | 297 | 30 | 5 |
| Daphnia magna | 35525 | 33.021 | 601.688 | 622.453 | 14 | 6.791 | 6.856 | 184 | 3.037 |
| Eisenia fetida | 6396 | 37 | 5.544 | 764 | 2 | 582 | 704 | 68 | 586 |
| Homo sapiens | 9606 | 360.659 | 29.885.237 | 2.183.220 | 3.220 | 7.271.118 | 16.837.648 | 153.982 | 4.753.639 |

## Perfil de la base Gene para los organismos críticos

```
GET esearch.fcgi?db=gene&term=txid<TAXID>[Organism:exp]
GET esearch.fcgi?db=gene&term=txid<TAXID>[Organism:exp] AND "genetype protein coding"[Properties]
```

| organismo | registros en Gene | de ellos, codificantes de proteína |
| --- | ---: | ---: |
| *Dalbulus maidis* | 37 | 13 |
| *Macrosteles quadrilineatus* | 24.179 | 21.979 |
| *Spiroplasma kunkelii* | 20 | 18 |
| '*Candidatus* Phytoplasma zeae' | 0 | 0 |
| *Zea mays* | 72.398 | 50.644 |

## Los 37 registros de *Dalbulus maidis* en Gene, uno por uno

```
GET esearch.fcgi?db=gene&term=txid74065[Organism:exp]&retmax=100
GET esummary.fcgi?db=gene&id=<37 uid>&retmode=json
```

Salida resumida: los 37 registros tienen `chromosome = MT` y `chraccver = NC_070066.1`. Son los 13 genes codificantes del mitogenoma (ND1-ND6, ND4L, COX1-COX3, CYTB, ATP6, ATP8), los 2 ARNr (12S y 16S) y 22 ARNt. **No hay un solo gen nuclear.**
