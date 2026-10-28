# Recuperacion de accesiones para el eje 3 (off-target): las 19 filas restantes

Issue #43, linea F3. Continuacion de `recuperacion_6filas_REPORT.md`. El objetivo
es el mismo: completar la secuencia del gen que nombra cada fila del catalogo
`research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.json`
usando **unicamente** accesiones de GenBank/RefSeq citadas en el texto o en los
suplementarios del paper de esa fila. No se busco en el NCBI por nombre de gen ni
se propuso ningun ortologo o sustituto: el equipo descarto esa via (`DECISIONS`).
Una fila sin accesion en su paper es un resultado valido y queda con el eje ausente
y el motivo escrito. Tabla: `recuperacion_resto.tsv`.

## Resultado en una linea

De las 19 filas, **5 quedaron con accesion** (`HE-05`, `HE-06`, `HE-07`, `HE-10`,
`CI-06`), **11 sin accesion en el paper** y **3 bloqueadas por la red** (`CI-04`,
`CI-05`, `DE-04`). Ninguna quedo `no identificada`: las cuatro filas que el catalogo
citaba de segunda mano se emparejaron con su paper [M]. De las 11 "sin accesion",
**solo 1 (`CI-08`) se cierra habiendo leido el texto completo**. De las otras 10,
`HE-08` es un caso aparte: no se abrio ni el texto ni el resumen -solo se
recuperaron sus metadatos bibliograficos- pero la fila no nombra ningun gen (es el
control de dosis alta de ARNdc), asi que no hay un gen para el cual buscar
accesion. Las 9 restantes son **provisionales**, apoyadas solo en el resumen, porque el
texto completo esta detras de un muro de pago y ninguna de las vias abiertas
(Europe PMC, PMC, Unpaywall, Semantic Scholar, enlace TDM de Crossref) devolvio el
articulo. Esa distincion importa: "no esta en el resumen" no es lo mismo que
"no esta en el paper".

## Tarea A: las cuatro filas citadas de segunda mano

El catalogo nombraba `HE-02`, `HE-07`, `HE-08` y `HE-10` solo por autor y anio,
"citado por Dalaison-Fuentes 2022" o "citado por Jones 2021". La via de
identificacion fue la lista de referencias de los dos papers que las citan, que es
evidencia directa del emparejamiento y no una reconstruccion: el endpoint
`references` de Europe PMC para Dalaison-Fuentes 2022 (`MED/35442515`, 80
referencias) y para el preprint de Jones, Bernal y Medina 2021 (`PPR/PPR402665`,
89 referencias), mas el texto de la lista de referencias del preprint de
Dalaison-Fuentes (ref. 5), que numera cada cita y permite leerla completa cuando
Europe PMC no la resuelve. Las cuatro quedaron con confianza alta [M]:

**`HE-02`** (V-ATPase A en *Nezara viridula*) es Sharma, Christiaens, Taning y
Smagghe 2020 (ref. 1). Aparece en la lista de referencias del preprint de Jones
2021, que es quien la cita; coinciden autor, anio y especie, y el resumen nombra
`dsvATPase A` entre los dos blancos con mortalidad significativa por ingesta
(43% y 45% a los 14 dias), que es exactamente el gen de la fila.

**`HE-07`** (NcSP75 en *Nephotettix cincticeps*) es Matsumoto y Hattori 2018
(ref. 2), ref. 50 del preprint de Dalaison-Fuentes. El titulo nombra la especie y
el gen, y el PMID coincide con el que la nota del catalogo ya tenia anotado
(30183736), asi que la fila estaba bien apuntada desde C5.

**`HE-08`** (*N. cincticeps*, dosis alta de ARNdc como control) es Tomizawa y Noda
2013 (ref. 3), ref. 48 del preprint de Dalaison-Fuentes, que da titulo, revista,
volumen y paginas completos. El DOI se confirmo en Crossref con los mismos autores,
volumen y paginas. **No esta indexado en Europe PMC**: las busquedas por autor
(`AUTH:"Tomizawa M" AND AUTH:"Noda H"`) y por titulo devuelven cero, por eso la
fila no tiene PMID ni PMCID. La revista, *Applied Entomology and Zoology*, no esta
en PubMed para ese anio [?].

**`HE-10`** (*Amrasca biguttula*) es Singh, Gupta, Pandher, Kaur, Rathore y Palli
2018 (ref. 4), ref. 43 del preprint de Dalaison-Fuentes y referencia resuelta por
Europe PMC en la lista de Dalaison-Fuentes 2022. Coinciden autor, anio y especie, y
el contenido del paper -seleccion de genes de referencia y primera demostracion de
RNAi en la especie- es lo que la fila describe como "varios". Observacion
colateral: el catalogo atribuia esta cita a Dalaison-Fuentes y el encargo a Jones;
la lista de referencias confirma que quien la cita es Dalaison-Fuentes.

## Tarea B: lo que dio cada paper

### Las cinco filas con accesion

**`HE-06`** (actina en *Homalodisca vitripennis*, Rosa et al. 2010, ref. 6) es el
caso mas limpio. El paper es de acceso abierto en Europe PMC (PMC2902141) y la
seccion de produccion de ARNdc define el blanco sobre la region 1-1000 de
**AY588061** (actina muscular putativa); el primer parrafo de Resultados aclara que
la otra actina disponible en GenBank, **AY588060** (actina citoplasmatica
putativa), comparte 85% de identidad nucleotidica global con la anterior y es la
que el trabajo mide como off-target. Las dos accesiones sirven al eje 3: una es el
blanco y la otra es el off-target documentado dentro de la misma especie [R].

**`HE-07`** (NcSP75) trae **BAQ94503** en Resultados y en Metodos (el fragmento de
469 pb que amplifican para el ARNdc se define sobre esa accesion). Hay una
limitacion importante: BAQ94503 es una accesion de **proteina** de DDBJ/GenBank,
no del ARNm, y el eje 3 necesita nucleotidos. El contig del sialotranscriptoma que
el paper menciona para NcSP75 no es una accesion publica. El gen de referencia
EF-1 (AB836664) no es el gen de la fila y no se arrastra.

**`HE-10`** cierra con el rango **MF101761-MF101776**, declarado en Metodos ("las
secuencias de todos los genes seleccionados se depositaron en el NCBI") y
desglosado gen por gen en la Tabla 1. La Tabla 1 lista 15 accesiones: no aparece
MF101770 [?]. El matiz relevante para el eje 3 es que los cuatro blancos de ARNdc
del trabajo son Snf7, IAP, AQP y VATPase, y de esos **solo VATPase tiene accesion**
(MF101769); para Snf7, IAP y AQP la Tabla 2 da unicamente cebadores. El resto del
rango son genes de referencia, utiles como control pero no como blanco.

**`HE-05`** (BicC en *Rhodnius prolixus*, Pascual et al. 2021, ref. 7) se leyo
completo desde el PDF de Springer que devolvio Unpaywall. La unica accesion que
cita para el gen es el supercontig genomico **KQ034133**, dentro del cual estan las
unidades anotadas RPRC0001612 y RPRC001613 -identificadores de VectorBase, no de
GenBank- que el trabajo demuestra que son un solo transcripto de 14 exones y 1986
pb. El ARNm en si proviene de RNA-seq propio no publicado y no esta depositado, asi
que la accesion sirve como ubicacion genomica, no como secuencia del transcripto.
Queda a criterio de quien corra el eje 3 si un supercontig es un insumo aceptable [H].

**`CI-06`** (ATP synthase beta en *Euscelidius variegatus*, Galetto et al. 2021,
ref. 8) trae en Metodos 2.2 la secuencia codificante completa del gen en la base
TSA: **GFTU01013594.1**, BioProject **PRJNA393620**. Advertencia metodologica: el
texto que se leyo es la **version preprint en bioRxiv**, que es la ubicacion green
OA que Unpaywall devuelve para ese DOI; no se leyo la version publicada en
*Journal of Insect Physiology*. La accesion deberia verificarse contra la version
final antes de darla por firme [?]. El mismo texto cita GFTU01001708.1 para Sid-1,
que no es el gen de esta fila.

### La fila cerrada con el texto completo a la vista, y el caso aparte de `HE-08`

**`CI-08`** (uk1_LRR en *E. variegatus*, Arricau-Bouvery et al. 2026, ref. 9) se
leyo completo en la copia depositada en HAL (hal-05448108, CC BY). El paper
**no cita ninguna accesion**: en Metodos 2.4 las secuencias de uk1_LRR, de la
cadena pesada de clatrina y de AP2b se amplifican por PCR desde ADNc con cebadores
de la Tabla 1, y la seccion de disponibilidad de datos dice que los datos se
entregan a pedido. Un barrido con expresiones regulares sobre todo el texto no
encontro ninguna cadena con forma de accesion de GenBank o RefSeq. El material
suplementario (Apendice A) solo existe en el sitio de Elsevier. Es el mismo patron
que ya se habia visto en `CI-07`, del mismo grupo: trabajan sobre su propio
transcriptoma sin depositar los genes individuales [M].

**`HE-08`** se cierra por otro motivo: la fila no nombra un gen -es el control de
dosis alta de ARNdc-, de modo que no hay un gen para el cual buscar accesion. Del
paper solo se recuperaron los metadatos bibliograficos; ni el resumen se pudo abrir.

### Las nueve filas provisionales (solo resumen)

`HE-01`, `HE-02`, `HE-03`, `HE-09`, `HE-11`, `DM-04`, `CI-09`, `CI-11` y `CI-12`
quedaron con el resumen como unica fuente. En ninguno de esos resumenes aparece
una cadena con forma de accesion. Los motivos difieren y conviene dejarlos
anotados porque definen si vale la pena reintentar:

`HE-01` (Zhang et al. 2015, ref. 10), `HE-02` (ref. 1), `HE-09` (Eliautout et al.
2016, ref. 11), `HE-11` (Chen, Redinbaugh y Michel 2015, ref. 12) y `DM-04`
(Dalaison-Fuentes et al. 2023, ref. 13) son `closed` en Unpaywall: no hay ninguna
copia abierta declarada. `CI-09` (Galetto et al. 2025, ref. 14) y `DE-04` figuran
como `hybrid` pero Unpaywall no devuelve PDF. `CI-12` (Matsumoto y Hattori 2016,
ref. 15) es `bronze`. `CI-11` (Matsumoto y Hattori 2019, ref. 16) es el caso mas
prometedor para un reintento: Europe PMC lo marca `green`, es decir que deberia
haber una copia en algun repositorio, pero Unpaywall no devolvio la ubicacion y
Semantic Scholar fallo con 503 [?]. `HE-03` (Ghosh et al. 2018, ref. 17) es un caso
aparte: esta en PMC (PMC6101104) pero `fullTextXML` responde 500 y solo se
recupero el frente del articulo; sus PDF libres estan en europepmc.org -bloqueado
por la allowlist- y en jove.com, que no se intento por la regla de no reintentar
por otra via.

### Las tres filas bloqueadas por la red

`CI-04` y `CI-05` (Abba et al. 2019, ref. 18) tienen un unico texto completo
gratuito segun Europe PMC: el PDF del repositorio institucional **iris.unito.it**,
dominio fuera de la allowlist. `DE-04` (Wang et al. 2023, ref. 19) tiene el PDF
marcado como Open access en **onlinelibrary.wiley.com**, tambien fuera de la
allowlist, y Unpaywall no ofrece alternativa. Las tres se marcan
`bloqueado_por_red` con el dominio anotado; no se reintentaron por otra via ni se
pidio aprobacion, segun la regla del encargo.

Vale registrar una observacion sobre `CI-04` que **no** se tomo como accesion de esa
fila: el paper de `CI-06` (mismo grupo, misma especie, mismo gen) cita
GFTU01013594.1 para ATP synthase beta de *E. variegatus*. Tomar esa accesion para
`CI-04` seria importar un dato desde otro paper, que es justo lo que las reglas de
esta tarea prohiben. Queda como decision de una persona [H].

## Lo que esto deja para el eje 3

Sumando a las recuperaciones anteriores, el eje 3 pasa de 15 a 20 filas con
secuencia disponible, pero solo 3 de las 5 nuevas (`HE-06`, `HE-10` y `CI-06`) dan
un nucleotido directamente usable; `HE-07` da una proteina y `HE-05` un supercontig
genomico. Las 14 filas restantes del catalogo siguen sin eje, con el motivo escrito
por fila en `recuperacion_resto.tsv`. No se descargo ninguna secuencia ni se
verifico ninguna accesion contra el NCBI: eso queda explicitamente fuera de esta
tarea.

## Referencias

Todas tomadas de Europe PMC (endpoint `search`, `resultType=core`) salvo la ref. 3,
tomada de Crossref, y las refs. 5 y 20, que son los preprints. Autores, revista,
volumen, numero, paginas, DOI, PMID y PMCID tal como los devuelve el servicio.

1. Sharma R, Christiaens O, Taning CN, Smagghe G. RNAi-mediated mortality in southern green stinkbug *Nezara viridula* by oral delivery of dsRNA. *Pest Management Science* 2021;77(1):77-84. doi 10.1002/ps.6017. PMID 32696565. Sin PMCID.
2. Matsumoto Y, Hattori M. The green rice leafhopper, *Nephotettix cincticeps* (Hemiptera: Cicadellidae), salivary protein NcSP75 is a key effector for successful phloem ingestion. *PLoS One* 2018;13(9):e0202492. doi 10.1371/journal.pone.0202492. PMID 30183736. PMCID PMC6124752.
3. Tomizawa M, Noda H. High mortality caused by high dose of dsRNA in the green rice leafhopper *Nephotettix cincticeps* (Hemiptera: Cicadellidae). *Applied Entomology and Zoology* 2013;48(4):553-559. doi 10.1007/s13355-013-0211-5. Sin PMID ni PMCID (no indexado en Europe PMC).
4. Singh S, Gupta M, Pandher S, Kaur G, Rathore P, Palli SR. Selection of housekeeping genes and demonstration of RNAi in cotton leafhopper, *Amrasca biguttula biguttula* (Ishida). *PLoS One* 2018;13(1):e0191116. doi 10.1371/journal.pone.0191116. PMID 29329327. PMCID PMC5766320.
5. Dalaison-Fuentes LI, Pascual A, Gazza E, Welchen E, Rivera-Pomar R, Catalano MI. Development of efficient RNAi methods in the corn leafhopper *Dalbulus maidis*, a promising application for pest control. Preprint, bioRxiv 2022. doi 10.1101/2022.01.17.476645. Version publicada: *Pest Management Science* 2022;78(7):3108-3116, doi 10.1002/ps.6937, PMID 35442515, sin PMCID.
6. Rosa C, Kamita SG, Dequine H, Wuriyanghan H, Lindbo JA, Falk BW. RNAi effects on actin mRNAs in *Homalodisca vitripennis* cells. *Journal of RNAi and Gene Silencing* 2010;6(1):361-366. Sin DOI en Europe PMC. PMID 20628496. PMCID PMC2902141.
7. Pascual A, Vilardo ES, Taibo C, Sabio y Garcia J, Rivera-Pomar R. Bicaudal C is required for the function of the follicular epithelium during oogenesis in *Rhodnius prolixus*. *Development Genes and Evolution* 2021;231(1-2):33-45. doi 10.1007/s00427-021-00673-0. PMID 33704576. Sin PMCID.
8. Galetto L, Abba S, Rossi M, Ripamonti M, Palmano S, Bosco D, Marzachi C. Silencing of ATP synthase beta reduces phytoplasma multiplication in a leafhopper vector. *Journal of Insect Physiology* 2021;128:104176. doi 10.1016/j.jinsphys.2020.104176. PMID 33253714. Sin PMCID. Version leida: preprint bioRxiv doi 10.1101/2020.10.02.324350.
9. Arricau-Bouvery N, Dubrana MP, Duret S, Foissac X, Malembic-Maher S. Gene silencing targeting uk1_LRR or clathrin in the experimental vector *Euscelidius variegatus* modifies insect colonization by "flavescence doree" phytoplasma. *Microbiological Research* 2026;305:128416. doi 10.1016/j.micres.2025.128416. PMID 41401619. Sin PMCID. Copia leida: HAL hal-05448108 (CC BY).
10. Zhang BX, Huang HJ, Yu B, Lou YH, Fan HW, Zhang CX. Bicaudal-C plays a vital role in oogenesis in *Nilaparvata lugens* (Hemiptera: Delphacidae). *Journal of Insect Physiology* 2015;79:19-26. doi 10.1016/j.jinsphys.2015.05.006. PMID 26025198. Sin PMCID.
11. Eliautout R, Dubrana MP, Vincent-Monegat C, Vallier A, Braquart-Varnier C, Poirie M, Saillard C, Heddi A, Arricau-Bouvery N. Immune response and survival of *Circulifer haematoceps* to *Spiroplasma citri* infection requires expression of the gene hexamerin. *Developmental and Comparative Immunology* 2016;54(1):7-19. doi 10.1016/j.dci.2015.08.007. PMID 26279217. Sin PMCID.
12. Chen Y, Redinbaugh MG, Michel AP. Molecular interactions and immune responses between Maize fine streak virus and the leafhopper vector *Graminella nigrifrons* through differential expression and RNA interference. *Insect Molecular Biology* 2015;24(3):391-401. doi 10.1111/imb.12166. PMID 25693649. Sin PMCID.
13. Dalaison-Fuentes LI, Pascual A, Crespo M, Andrada NL, Welchen E, Catalano MI. Knockdown of double-stranded RNases (dsRNases) enhances oral RNA interference (RNAi) in the corn leafhopper, *Dalbulus maidis*. *Pesticide Biochemistry and Physiology* 2023;196:105618. doi 10.1016/j.pestbp.2023.105618. PMID 37945254. Sin PMCID.
14. Galetto L, Lucetti G, Bucci L, Canuto F, Rossi M, Abba S, Vallino M, Parise C, Palmano S, Manfredi M, Bosco D, Marzachi C. Natterin-like and legumain insect gut proteins promote the multiplication of a vector-borne bacterial plant pathogen. *Microbiological Research* 2025;291:127984. doi 10.1016/j.micres.2024.127984. PMID 39616656. Sin PMCID.
15. Matsumoto Y, Hattori M. Gene silencing by parental RNA interference in the green rice leafhopper, *Nephotettix cincticeps* (Hemiptera: Cicadellidae). *Archives of Insect Biochemistry and Physiology* 2016;91(3):152-164. doi 10.1002/arch.21315. PMID 26728387. Sin PMCID.
16. Matsumoto Y, Hattori M. Characterization of multicopper oxidase genes in the green rice leafhopper, *Nephotettix cincticeps* (Hemiptera: Cicadellidae), with focus on salivary gland-specific genes. *Archives of Insect Biochemistry and Physiology* 2019;102(2):e21602. doi 10.1002/arch.21602. PMID 31328822. Sin PMCID.
17. Ghosh SKB, Hunter WB, Park AL, Gundersen-Rindal DE. Double-stranded RNA oral delivery methods to induce RNA interference in phloem and plant-sap-feeding hemipteran insects. *Journal of Visualized Experiments* 2018;(135):e57390. doi 10.3791/57390. PMID 29782023. PMCID PMC6101104.
18. Abba S, Galetto L, Ripamonti M, Rossi M, Marzachi C. RNA interference of muscle actin and ATP synthase beta increases mortality of the phytoplasma vector *Euscelidius variegatus*. *Pest Management Science* 2019;75(5):1425-1434. doi 10.1002/ps.5263. PMID 30417535. Sin PMCID.
19. Wang YH, Klobasa W, Chu FC, Huot O, Whitfield AE, Lorenzen M. Structural and functional insights into the ATP-binding cassette transporter family in the corn planthopper, *Peregrinus maidis*. *Insect Molecular Biology* 2023;32(4):412-423. doi 10.1111/imb.12840. PMID 36912710. Sin PMCID.
20. Jones TL, Bernal JS, Medina RF. Assessing the functionality of RNA interference (RNAi) in the phloem-feeding maize pest *Dalbulus maidis*. Preprint, bioRxiv 2021. doi 10.1101/2021.09.29.462424. Europe PMC PPR402665. Sin PMID ni PMCID.

## Trazabilidad

Copias de los textos abiertos y los volcados de las consultas (listas de
referencias, metadatos `core`, resumenes) quedaron en
`work/F3_recuperacion2/` (no versionado). Ningun archivo existente del repositorio
se modifico; no se corrio `git add`, `commit` ni `push`.
