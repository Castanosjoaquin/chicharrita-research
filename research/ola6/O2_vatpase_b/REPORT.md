# O2 — La secuencia de `V-ATPase B` de *Dalbulus maidis*, recuperada por homologia local

**Veredicto: la secuencia existe y esta recuperada, por las dos vias, y el insumo que bloqueaba
`O3` deja de faltar.** El locus de la subunidad B de la V-ATPasa esta en el cromosoma 2 del
ensamblado `ihDalMaid1.1` de *Dalbulus maidis* (`OZ319705.1`, 38.943.269-38.957.327, hebra `+`,
diez exones), su CDS mide **1.503 nt** y codifica una proteina de **500 aminoacidos** `[M]`. El
mismo transcripto esta completo en **dos de los tres transcriptomas publicos** —`GHCC01013224.1`
en el TSA de Pergamino y `GITV01003502.1` en el de Ohio, los dos con la proteina entera al
100 % de identidad— y **partido en dos contigs** en el tercero, `GCWP01` de Illinois, que deja
sin cubrir las posiciones 145-264 de la proteina `[M]`. Los dos CDS independientes —el del
genoma y el del transcriptoma argentino— difieren en **3 nucleotidos de 1.503** (99,80 %) y
codifican **la misma proteina, letra por letra** `[M]`.

**Fecha de corrida:** 2026-10-27. **Via:** homologia local con `miniprot` 0.18-r281 en WSL
(Ubuntu 24.04). **Ninguna secuencia salio de la maquina**: las consultas son accesiones publicas
que se bajaron del NCBI y de UniProt, los transcriptomas son los tres TSA publicos bajados del
FTP del GenBank, y todo el alineamiento corrio en local.

---

## 1. Por que a nivel proteina, y por que reciproco

Las dos restricciones del issue estan medidas en el repositorio y las dos se confirmaron en esta
pasada.

**A nivel proteina.** `C5` midio que entre generos de cicadelidos la identidad de nucleotido va
de 77 a 84 % y la mediana en proteina es 0,866 `[M]`. Lo que midio esta corrida es el mismo
fenomeno sobre este gen: la proteina predicha en *D. maidis* es **identica en 500 de 500
posiciones** a la de *Macrosteles quadrilineatus*, mientras que los dos CDS comparten apenas el
**90,35 %** de sus nucleotidos y solo **136 de 1.483 ventanas de 21 nt** (9,17 %) `[M]`. Buscar
este gen en nucleotido entre generos habria dado senal debil justamente donde la proteina la da
perfecta.

**Reciproco y no mejor acierto.** `C5` midio que elegir el gen por nombre en el transcriptoma de
la especie cercana devolvio un gen distinto del que devolvio la homologia, con 65 % de diferencia
en el conteo de ventanas eficientes `[M]`; `C11` reprodujo la leccion con otra especie cuando la
entrada que *Drosophila* llama `Rpn6` resulto ser PSMD11 y la que llama `Rpn7` resulto ser PSMD6,
cada una reciproca de una proteina distinta `[M]`. Aca la ida y la vuelta
se corrieron las dos, con el mismo motor y el mismo umbral, y se exigio que la vuelta cayera en
el ARNm de **la misma subunidad**.

---

## 2. La ida: cinco proteinas de referencia contra el genoma

Las consultas son accesiones publicas, elegidas para que la ida no dependa de una sola especie ni
de una sola familia.

| Consulta | Organismo | Familia | Largo | Por que esta |
| --- | --- | --- | ---: | --- |
| `AGJ51963.1` | *Peregrinus maidis* | Delphacidae | 500 aa | es la subunidad B del `DE-01` del catalogo de `C5`, con bioensayo publicado |
| `XP_054288745.1` | *Macrosteles quadrilineatus* | Cicadellidae | 500 aa | es el ortologo reciproco estricto que `C11` ya habia resuelto por `blastp` bidireccional |
| `XP_054260731.1` | *M. quadrilineatus* | Cicadellidae | 614 aa | subunidad **A**: control de paralogo del mismo complejo |
| `XP_054264527.1` | *M. quadrilineatus* | Cicadellidae | 245 aa | subunidad **D**: control de paralogo y ancla contra `ATPaseD_Dm` |
| `sp\|P31409\|VATB_DROME` | *Drosophila melanogaster* | Drosophilidae | 490 aa | es `Vha55`, una de las siete proteinas de control de `pipeline/` |

Resultado, con `miniprot --gff --outn=5 --outs=0.5` sobre el indice ya construido del ensamblado
(`genome.mpi`), 0,56 s de pared `[M]`:

| Consulta | Contig | Cromosoma | Tramo | Hebra | Identidad | Cobertura de la consulta | Rango 2 |
| --- | --- | ---: | --- | :-: | ---: | ---: | :-: |
| `XP_054288745.1` (B) | `OZ319705.1` | 2 | 38.943.269-38.957.327 | + | **1,0000** | 1-500, 100 % | ninguno |
| `AGJ51963.1` (B) | `OZ319705.1` | 2 | 38.943.269-38.957.327 | + | 0,9660 | 1-500, 100 % | ninguno |
| `P31409` (B, `Vha55`) | `OZ319705.1` | 2 | 38.943.287-38.957.312 | + | 0,9776 | 1-490, 100 % | ninguno |
| `XP_054260731.1` (A) | `OZ319711.1` | 8 | 47.265.953-47.286.132 | + | 0,9919 | 1-614, 100 % | ninguno |
| `XP_054264527.1` (D) | `OZ319711.1` | 8 | 30.145.193-30.154.045 | − | 0,9633 | 1-245, 100 % | ninguno |

**Tres consultas de tres familias distintas caen en el mismo locus, y las otras dos caen en loci
distintos.** Con el umbral de secundarios en 0,5 del mejor puntaje no aparece ningun competidor
para ninguna de las cinco: el locus de la subunidad B no compite con el de A ni con el de D.

### El CDS, y la verificacion que lo autoriza

`scripts/02_extraer_cds.py` saca los exones del GFF, los concatena en orden de traduccion y
**aborta si la traduccion no reproduce, letra por letra, la proteina que `miniprot` predijo** en
su propia salida `--trans`. Un CDS que no reproduce la proteina predicha no sirve de insumo. Para
la subunidad B la verificacion pasa: 1.503 nt, 500 aa, diez exones, sin codon de parada interno
`[M]`. La salida esta en `resultados/VATPaseB_Dm_cds.fna` y
`resultados/VATPaseB_Dm_prot.faa`.

**Control de circularidad.** `miniprot` alinea guiado por la consulta, asi que una proteina
predicha podria estar arrastrando residuos del query. No es el caso: el CDS extraido con la
consulta de *P. maidis* —que difiere de la de *M. quadrilineatus* en **17 de 500 residuos**, el
96,6 % de identidad, que es exactamente la identidad que `miniprot` reporta para esa consulta
contra el genoma `[M]`— da
**exactamente la misma proteina de 500 aa** que el extraido con la consulta de *M.
quadrilineatus* `[M]`. La prediccion no depende de con que se la busco.

Con la consulta de *Drosophila* la extraccion **no produjo CDS**: el guion la rechazo porque su
traduccion sale de 491 aa contra los 490 de la prediccion de `miniprot`, un residuo de
diferencia en el borde. No se forzo: esa consulta se usa solo como ancla de locus y de identidad,
que es para lo que entro.

---

## 3. La vuelta: la proteina de *D. maidis* contra los transcriptomas anotados de dos parientes

La vuelta usa como consulta la proteina predicha en *D. maidis* y como base los transcriptomas
RefSeq completos de los dos cicadelidos con genoma anotado (36.629 y 33.294 transcriptos).

| Consulta (predicha en *D. maidis*) | Base | Mejor acierto | Producto anotado del acierto | Identidad | Cobertura | Rango 2 |
| --- | --- | --- | --- | ---: | ---: | --- |
| subunidad **B** | *M. quadrilineatus* | `XM_054432770.1` (40-1542) | V-type proton ATPase **subunit B** | **1,0000** | 1-500, 100 % | **ninguno** |
| subunidad **B** | *H. vitripennis* | `XM_046812795.1` (61-1563) | V-type proton ATPase **subunit B** | 0,9940 | 1-500, 100 % | ninguno |
| subunidad A | *M. quadrilineatus* | `XM_054404756.1` | subunit **A** | 0,9919 | 100 % | `XM_054404748.1`, tambien subunit A |
| subunidad D | *M. quadrilineatus* | `XM_054408552.1` | subunit **D** | 0,9633 | 100 % | `XM_054407659.1`, tambien subunit D |

**La ortologia reciproca cierra.** La ida salio de `XP_054288745.1` y la vuelta cae en
`XM_054432770.1`, que es exactamente el ARNm que codifica esa proteina —la cabecera del CDS que
el NCBI entrega para ese transcripto dice `protein_id=XP_054288745.1`— y es **el mismo ARNm que
`C11` habia identificado** como el ortologo de `V-ATPase B` en esa especie `[M]`. La vuelta de la
subunidad B no tiene competidor de rango 2 en ninguna de las dos bases; las de A y D si tienen,
pero sus competidores son **otra copia de la misma subunidad**, no una subunidad distinta. O sea
que el metodo no confunde subunidades del complejo, que es justo el riesgo que el issue pedia
descartar.

---

## 4. La via que pedia el issue: los tres transcriptomas publicos

El issue nombraba las bases de `work/C11/` (`db_GHCC01`, `db_GCWP01`, `db_GITV01`). **Esas bases
no estan en esta maquina y `work/` no existe**, asi que no se usaron. En su lugar se bajaron los
tres TSA de su fuente publica, del FTP del GenBank, y se verifico que son los mismos: 25.662 +
55.286 + 56.117 = **137.065 contigs**, que es exactamente el total que `C11` reporta para los
tres `[M]`. Las sumas SHA-256 de los tres archivos quedan en `resultados/tsa_sha256.txt`.

| TSA | Origen | Contigs | Acierto de `V-ATPase B` | Identidad | Cobertura de la proteina |
| --- | --- | ---: | --- | ---: | --- |
| `GHCC01` | Pergamino (Argentina) | 55.286 | `GHCC01013224.1`, 30-1532 | **1,0000** | **1-500, completa** |
| `GITV01` | Ohio | 56.117 | `GITV01003502.1`, 53-1555 | **1,0000** | **1-500, completa** |
| `GCWP01` | Illinois | 25.662 | `GCWP01020173.1` 265-500 **y** `GCWP01025234.1` 1-144 | 1,0000 cada uno | **partida: faltan 145-264** |

La respuesta a la pregunta del issue, entonces, **no es la segunda salida**: los transcriptomas
publicos **si contienen** la subunidad B, y dos de los tres la contienen entera. El metodo con el
que se busco fue `miniprot --gff --outn=5 --outs=0.5` con la proteina de referencia y tambien con
la proteina predicha en la propia especie; el umbral de reporte es el 0,5 del mejor puntaje y la
cobertura minima el 0,1 de la consulta, que son los valores con los que corrio. Que `GCWP01`
quede partido no es un fallo de la busqueda: es el mismo ensamblado del que `D64` midio que no cubre un solo
nucleotido de la region vigente de `BicC_Dm` y cubre 609 de 2.520 posiciones de ese gen `[M]`,
asi que una cobertura parcial en `GCWP01` es lo esperable y no un fallo de la busqueda.

`GITV01` devuelve **dos** contigs con la proteina completa y la misma identidad
(`GITV01003502.1` y `GITV01002810.1`): es redundancia del ensamblado, no dos genes. Nada en esta
pasada permite afirmar cuantas copias del gen tiene la especie `[?]`.

### Los dos CDS independientes, comparados

El contig argentino cubre la proteina entera, asi que se le saco el CDS con el mismo guion
verificador y se comparo con el del genoma, codon a codon:

| | CDS del genoma (`OZ319705.1`) | CDS del TSA argentino (`GHCC01013224.1`) |
| --- | --- | --- |
| largo | 1.503 nt | 1.503 nt |
| proteina | 500 aa | 500 aa, **identica** |
| nucleotidos distintos | — | **3** (posiciones 615, 678 y 1254) |
| identidad de nucleotido | — | **99,80 %** |

Las tres diferencias son sinonimas, porque la proteina es la misma `[M]`. Son dos ensamblados
independientes, de dos origenes distintos —el genoma de referencia y una colecta de Pergamino—,
asi que la coincidencia es una validacion cruzada y no una repeticion. `[H]` Que haya tres
posiciones distintas es lo esperable para variacion entre poblaciones y no se puede distinguir en
esta pasada de un error de ensamblado en cualquiera de los dos; para `O3` da lo mismo, porque la
proteina y el marco son identicos, pero **si una ventana de 21 nt cae sobre una de las tres
posiciones, el veredicto de esa ventana depende de cual CDS se use**, y eso hay que mirarlo al
disenar.

---

## 5. La banda de concordancia que le corresponde

El issue pedia registrar «la banda de concordancia que le corresponde, no solo el nombre del
gen». Medida con `scripts/04_banda_concordancia.py`, que compara codon a codon y **aborta si los
largos no coinciden**, porque sin huecos la comparacion solo vale si no hay indels:

| Comparacion | Identidad de nt | Tramo exacto maximo | Ventanas de 21 nt identicas |
| --- | ---: | ---: | --- |
| *D. maidis* (genoma) vs *M. quadrilineatus* `XM_054432770.1` | **90,35 %** | 62 nt | 136 de 1.483 (**9,17 %**) |
| *D. maidis* (genoma) vs *H. vitripennis* `XM_046812795.1` | 85,70 % | 36 nt | 38 de 1.483 (2,56 %) |
| *D. maidis* (genoma) vs *D. maidis* (TSA de Pergamino) | **99,80 %** | — | — |

Contra lo ya medido en el repositorio: `C5` puso la banda entre generos de cicadelidos en 77-84 %
de nucleotido, y `C11` la midio en 83,0-92,5 % sobre once familias, con **88,2 % para
`V-ATPase B`** y 233 ventanas de 21 nt identicas (el 10,9 % del ARNm de 2.158 nt) `[M]`. Los
90,35 % y el 9,17 % de esta pasada caen dentro de esa banda y la corroboran con un insumo
distinto —el CDS del genoma, no el contig del TSA— y con otro motor. **La lectura operativa no
cambia:** con 136 ventanas compartidas sobre 1.483, una ventana disenada sobre el pariente no se
traslada; hay que disenar sobre la secuencia de *D. maidis*, que es justamente lo que esta pasada
deja disponible `[H]`.

---

## 6. Las anclas, que son lo que autoriza a leer los numeros

Tres controles independientes, ninguno elegido despues de ver el resultado.

1. **`Vha55` reproduce la cifra ya versionada.** `pipeline/resultados.json` declara, como control
   de siete proteinas confirmadas por dos papers publicados, la identidad **0,978** para `Vha55`
   con un solo locus. Esta pasada, con la misma proteina (`P31409`) contra el mismo ensamblado,
   da **0,9776** y un solo locus `[M]`. Es la misma medicion hecha en otra sesion y con otra
   consulta de entrada.
2. **La subunidad D cae donde el proyecto ya la habia puesto.** `pipeline/resultados.json` dice
   que `ATPaseD_Dm` cae en el **cromosoma 8** y coincide con el locus de `Vha36-1`. Esta pasada
   pone la subunidad D en `OZ319711.1`, que es el cromosoma 8 `[M]`. El gen que el laboratorio ya
   tiene secuenciado sirve de ancla para el gen que no tenia.
3. **La prediccion no depende de la consulta**, como dice §2: dos consultas que difieren en 17
   residuos dan la misma proteina de 500 aa.

---

## 7. Lo que esta pasada no dice

- **No dice que este gen funcione como blanco en *D. maidis*.** El fenotipo de `DM-02` —alas
  deformes, supervivencia 16 % al dia 4 contra 37 % del control de GFP— es de la fuente que el
  catalogo de `C5` registra como leida completa en la ola 2, y es evidencia sobre la especie, no
  sobre esta secuencia `[R]`. Lo que esta pasada agrega es la secuencia, no la eficacia.
- **No reemplaza al archivo del investigador.** Si llega el zip con el transcriptoma del
  laboratorio, lo que corresponde es alinear este CDS contra el, con el mismo guion, y reportar
  las diferencias. Que la secuencia ya este no vuelve inutil ese insumo: lo vuelve verificable.
- **No resuelve el numero de copias.** Los dos contigs de `GITV01` y los pares de rango 2 en los
  parientes son redundancia de ensamblado por lo que se ve, pero el numero de copias del gen en
  el genoma no se midio `[?]`.
- **No hay modelo de gen anotado para el locus.** El CDS sale de un alineamiento proteina-genoma,
  no de una anotacion: los limites de exon son los que `miniprot` propuso y no estan confirmados
  por evidencia de ARN sobre el genoma, aunque el CDS del TSA argentino —que si viene de ARN— da
  el mismo marco y la misma proteina `[M]`.
- **La corrida de `tblastn` del issue no se hizo.** No hay BLAST+ en esta maquina; se uso
  `miniprot`, que es el otro alineador que el propio issue admitia y el que ya usa `pipeline/`.
  Los dos resuelven proteina contra nucleotido con intrones; no son el mismo algoritmo y los
  numeros de identidad no son intercambiables entre los dos `[?]`.

---

## 8. Reproducibilidad

El entorno del issue era el de otra maquina. En esta —la de Luca, con WSL— **si hay alineador**:
`miniprot` 0.18-r281 compilado en `~/yhat/tools/miniprot/`, el ensamblado `ihDalMaid1.1` en
`~/yhat/data/genome.fna.gz` con su indice `genome.mpi` ya construido, y los transcriptomas RefSeq
de los dos cicadelidos parientes en el mismo directorio. Lo que sigue faltando es ViennaRNA y
BLAST+.

```bash
O2=/mnt/c/Proyectos/yHat/research/ola6/O2_vatpase_b
bash     "$O2/scripts/01_forward_genoma.sh" "$O2"
python3  "$O2/scripts/02_extraer_cds.py" "$O2" "$HOME/yhat/data/genome.fna.gz" XP_054288745.1 VATPaseB_Dm
python3  "$O2/scripts/02_extraer_cds.py" "$O2" "$HOME/yhat/data/genome.fna.gz" XP_054260731.1 VATPaseA_Dm
python3  "$O2/scripts/02_extraer_cds.py" "$O2" "$HOME/yhat/data/genome.fna.gz" XP_054264527.1 VATPaseD_Dm
bash     "$O2/scripts/03_reciproco.sh" "$O2"
python3  "$O2/scripts/04_banda_concordancia.py" "$O2"
bash     "$O2/scripts/05_tsa_publicos.sh" "$O2" "$HOME/yhat/o2_tsa"
python3  "$O2/scripts/06_cds_tsa_vs_genoma.py" "$O2" "$HOME/yhat/o2_tsa/tsa.GHCC.1.fsa_nt.gz" GHCC01013224.1
python3  "$O2/scripts/07_tabla.py" "$O2"
```

Los tres TSA se bajan del FTP del GenBank, no se versionan (47 MB):

```bash
mkdir -p "$HOME/yhat/o2_tsa" && cd "$HOME/yhat/o2_tsa"
for p in GCWP GHCC GITV; do
  curl -O "https://ftp.ncbi.nlm.nih.gov/genbank/tsa/G/tsa.$p.1.fsa_nt.gz"
done
sha256sum -c tsa_sha256.txt
```

**Si hubiera que correr la via de `tblastn` del issue** —que es la unica parte que quedo sin
hacer—, en una maquina con BLAST+ y con las bases de `work/C11/` presentes, el comando es:

```bash
cat work/W5/ref/TSA_GCWP01.fasta work/W5/ref/TSA_GHCC01.fasta work/W5/ref/TSA_GITV01.fasta > tsa_all.fasta
makeblastdb -in tsa_all.fasta -dbtype nucl -out tsa_db
tblastn -query research/ola6/O2_vatpase_b/consultas/consultas_vatpase.faa -db tsa_db \
        -evalue 1e-30 -max_target_seqs 5 \
        -outfmt "6 qseqid sseqid pident length qstart qend sstart send evalue bitscore" \
        -out tblastn_tsa.tsv
```

### Archivos

| Archivo | Que es |
| --- | --- |
| `consultas/consultas_vatpase.faa` | las cinco proteinas de referencia, por accesion publica |
| `resultados/VATPaseB_Dm_prot.faa` | **la proteina de 500 aa**, que es la mitad versionable del insumo de `O3` |
| `resultados/VATPaseA_Dm_prot.faa`, `VATPaseD_Dm_prot.faa` | las subunidades A y D, controles de paralogo |
| `resultados/ortologia_vatpase_b.tsv` | las 40 filas de ida, vuelta y TSA, con identidad y cobertura |
| `resultados/banda_concordancia.json`, `cds_tsa_vs_genoma.json` | las dos mediciones de §5 y §4 |
| `resultados/forward_genoma.gff`, `tsa_*.gff`, `reciproco_*.gff` | salida cruda de `miniprot` |
| `resultados/genoma_contigs.txt` | las 141 cabeceras del ensamblado, para resolver contig a cromosoma |
| `resultados/tsa_sha256.txt` | las sumas de los tres TSA bajados |
| `fuentes.json` | las accesiones y las URL, con fecha de consulta |

**Lo que no se versiona, y por que.** `tools/verificacion/sin_secuencias.py` rechaza toda racha de
21 nt o mas en el arbol versionado: es la regla de confidencialidad del proyecto, con el umbral de
`D28` y el incidente de `C9` como motivo. Asi que **ningun archivo de nucleotido de este bloque
entra al repositorio**, ni siquiera los que vienen de fuentes publicas, y el bloque tiene su
propio `.gitignore` para que no entren por descuido. Lo que se versiona es el generador, como ya
hace `pipeline/`. En el indice de este commit el verificador da **0 hallazgos no exceptuados**
`[M]`; la pasada contra el corpus de EPILAB **no se pudo correr** —falta
`YHat-Biotech/Sequences_EPILAB.xlsx` y falta `openpyxl` en el interprete— pero no tiene nada que
encontrar por construccion, porque una fuga de esas secuencias seria necesariamente una racha de
nucleotido y no quedo ninguna.

Los cinco archivos de nucleotido quedan en disco, sin versionar, y cada uno se regenera con un
comando de §8: `VATPaseB_Dm_cds.fna` (**el insumo de `O3`**, 1.503 nt) y los de las subunidades A
y D con `02_extraer_cds.py`; `VATPaseB_Dm_cds_desde_TSA_GHCC.fna` con `06_cds_tsa_vs_genoma.py`;
y los dos CDS de referencia de los parientes se bajan del NCBI con las URL de `fuentes.json`.
Para `O3`, el camino mas corto es correr `01` y `02` —menos de dos segundos con el indice ya
construido— o pedirle el archivo a esta linea.

Las cuatro tareas del issue quedan hechas. La unica parte declarada **no alcanzada** es la
corrida con `tblastn` sobre las bases de `work/C11/`: la herramienta no esta en esta maquina y el
directorio `work/` tampoco, y en vez de declararla nula se resolvio la misma pregunta con el otro
alineador que el issue admitia y con los mismos tres transcriptomas bajados de su fuente publica.
