# O3 — La quimera `BicC_Dm` + `V-ATPase B`, con las tres cuentas separadas

**Veredicto: la quimera se puede armar, pero el gen que aporta la segunda mitad entra al
diseño por un solo lugar, y el orden de los dos fragmentos se decide por el empalme y no
por el conteo.** Con el panel de seis referencias que fija `PREREGISTRO.md` §2.4 —el que
incluye la humana con peso 1,00— la subunidad B de la V-ATPasa de *Dalbulus maidis* tiene
**71 ventanas con coincidencia perfecta de 21 nt**, y de las **1.184** regiones de 300 nt
que caben en su secuencia codificante **sobrevive exactamente una**: 517-816 `[M]`. Sobre
esa región, las dos moléculas posibles quedan sin veto y rinden casi lo mismo —41 ventanas
eficientes el orden `V-ATPase B` + `BicC_Dm` y 40 el inverso, contra 40 de la suma de las
partes—, pero **sólo uno de los dos empalmes fabrica riesgo nuevo**: el del orden que gana
por una ventana crea un bloque perfecto de 19 nt que no existe en ninguno de los dos genes
y sí existe en dos transcriptos de *Zea mays* `[M]`. El criterio de terminado de este issue
dice que lo que descartaría la quimera es el perfil de riesgo del empalme, así que **el
orden que queda en pie es `BicC_Dm` + `V-ATPase B`**, que pierde esa ventana y no fabrica
nada.

**Fecha de corrida:** 2026-10-27, en la máquina de Santino (Windows 11, `python` 3.13.15 de
miniconda, ViennaRNA 2.7.2, `pyahocorasick`), que es la misma con la que corrió `C13`.
**Ninguna secuencia salió de la máquina.**

**El criterio no lo eligió esta corrida.** Lo fija
[`PREREGISTRO.md`](PREREGISTRO.md), escrito y commiteado antes de medir. Este bloque lo
ejecuta; donde se desvía, lo dice.

---

## 1. Las tres anclas, y la que costó arreglar

`PREREGISTRO.md` §6 es terminante: si una ancla no pasa, la línea para y lo dice, sin leer
ningún número nuevo. Las tres corren juntas en `scripts/00_anclas.py` y el script devuelve 1
si alguna falla. Las tres pasan `[M]`:

| Ancla | Qué verifica | Resultado |
| --- | --- | --- |
| A | `quimeras_v2.py --conjunto epilab` reproduce la tabla de `C4`, en los **dos** modos | 12 filas × 17 columnas, idénticas |
| B | `--conjunto vigentes --modo corregido` reproduce la tabla versionada de `C13` §5 | idéntica celda por celda; las tres sumas que el preregistro nombra (47→50, 47→44, 50→46), 4 ventanas de juntura eficientes y 61 heredadas cambiadas |
| C | `ranking.ejes()` da los cuatro conteos del nivel 3 de `C7` y sus `buenos_limpios` | 38/37, 21/20, 35/34, 21/17 |

**El ancla C falló al principio, y la causa importa más que el arreglo.** `CP_MRFV` daba 21
`buenos_limpios` contra los 20 publicados y `ATPaseD_Dm` daba 19 contra 17: en los dos casos
**más** ventanas limpias de las esperadas, que es la dirección que delata una referencia
ausente. El preregistro anticipaba otra causa —que `tools/sifi21_port/ranking.py` lo estaba
editando la sesión del issue #30— y no era eso. Era que el tamizado que vive en
`work/sifi_check/` se había corrido con **cinco** referencias más el genoma del vector, sin
la humana. Regenerado con las seis —`offtarget_full` sin `--mm1` como el original, y los
cuatro `offtarget_mm1_<gen>` con `--mm1`, todos en local— los cuatro pares dan exacto `[M]`.

Eso deja dos cosas escritas. Primero: **los `buenos_limpios` publicados de `C7` se
calcularon con la humana adentro**, así que el panel de seis no es una preferencia del
preregistro sino la reconstrucción de lo que ya estaba publicado. Segundo: un insumo
incompleto en `work/` —que no se versiona— puede hacer pasar por buenos unos números que no
reproducen lo publicado, y el único motivo por el que se detectó es que el preregistro pidió
el ancla. Los archivos viejos quedaron respaldados en `work/O3/respaldo/`.

**Corrección de diagnóstico (2026-10-27, `D83`, issue #33).** La primera frase sigue siendo
cierta y es la que vale: los `buenos_limpios` de `C7` llevan la humana. ~~La segunda lectura
—que el tamizado de `work/sifi_check/` «estaba incompleto»— era equivocada, y el arreglo que
salió de ella hizo daño.~~ `work/sifi_check/offtarget_full/` **no estaba incompleto**: es el
directorio de `sifi21_reproduccion.md` §4, cuyo panel esa sección publica por accesión
—cinco referencias más el genoma del vector, sin humana— y que `work/offtarget_db/` contiene
exactamente. El nivel 3 de `C7` nunca salió de ahí: sale de `work/sifi_v2/`, con los comandos
de `C7` §9, y desde ahí reproduce exacto hoy `[M]`. Reconstruir `offtarget_full/` con la
humana hizo pasar el ancla C **rompiendo** las anclas §2, §3 y §4 de `test_ranking.py` y el
`md5` publicado en `tools/sifi21_port/README.md`, sin que nadie lo viera. Lo que estaba mal
era el ancla C, que leía el directorio de otra línea: ahora lee `work/sifi_v2/` y sus cuatro
números esperados **no cambiaron**. Con `offtarget_full/` devuelto a su panel, las tres
anclas de `O3` y las 55 verificaciones de `test_ranking.py` pasan **a la vez** `[M]`, cosa
que hasta ahora no había pasado. Los respaldos que esta sección menciona no existen en la
máquina donde se corrió esto, así que el archivo no se recuperó: se **reconstruyó** con el
comando de §4, y reproduce el `md5` publicado `a3229e733e4dc70c308c901583b4e4c3` `[M]`.

## 2. Por qué esta combinación, y la región que hubo que elegirle

La combinación sale de la reunión del checkpoint 2 y de `D67`: las quimeras se arman por
**combinación de fenotipos**, no por suma de conteos. `BicC_Dm` tiene el mejor perfil de
riesgo del panel pero su fenotipo reduce la población entre generaciones sin cortar la
transmisión en la temporada; `V-ATPase B` aporta los dos ejes que le faltan, movilidad —alas
deformes— y mortalidad, con fenotipo reportado en la especie por entrega oral `[R]`
(supervivencia 16 % al día 4 contra 37 % del control de GFP; Jones, Bernal y Medina 2021,
**preprint de bioRxiv sin revisión por pares**, registrado como leído en texto completo en
`00_meta/FUENTES.md` `S18` y en `research/ola2/W6_agentes_ciencia/sources.json` `PRB-04`).
Que la única evidencia de fenotipo de este gen sea un preprint es parte del resultado y no
una nota al pie.

`BicC_Dm` ya tenía región elegida y publicada (922-1221, que `D25` movió por conservación).
`V-ATPase B` no tenía ninguna: el gen se recuperó recién en `O2`. El criterio para elegirla
es el de `PREREGISTRO.md` §2 y está ejecutado en `scripts/01_region_vatpase_b.py`: 300 nt,
forma `cascada` con veto duro por coincidencia perfecta de 21 nt, regla conservadora, pesos
base sin sortear, panel de seis con la humana, vector excluido por on-target, y las bandas
de 59 nt de los dos extremos del CDS excluidas de antemano porque el CDS viene del genoma y
no tiene UTR.

### El gen entra por un solo lugar, y entra justo

| Largo de región | Regiones sin ninguna ventana vetada |
| ---: | ---: |
| 150 nt | 342 |
| 200 nt | 192 |
| 250 nt | 84 |
| 280 nt | 24 |
| 295 nt | 6 |
| **300 nt** | **1** — 517-816 |
| 301 nt | **0** |

Las 71 ventanas vetadas del gen dejan un único hueco libre de 300 ventanas consecutivas, y
ese hueco **mide exactamente 300**: la región admisible no es una entre varias, es el hueco
entero sin un nucleótido de holgura `[M]`. A 301 nt el gen no tiene ninguna región
admisible. El largo de 300 lo fijó el issue por simetría con los otros dos genes del
insecto, no para que entrara, y cae en el filo; conviene decirlo antes de que alguien lea
«elegimos la mejor región de 300 nt» como si hubiera habido entre qué elegir `[H]`.

La restricción de borde de §2.5 **no cambia** la elección: 517-816 arranca en 517, bien
dentro de los inicios admisibles 60 a 1.145, y es primera con y sin restricción. El
ordenador restringido, corrido sin restricción, reproduce `ranking.alternativas()` celda por
celda, que es la verificación de que la restricción está bien aplicada y no inventada.

**De dónde viene el veto, por referencia**, en el CDS entero `[M]`:

| Referencia | Peso | 21/21 | ≥ 19 nt | 1 desapareo |
| --- | ---: | ---: | ---: | ---: |
| *Homalodisca vitripennis* | 0,60 | 38 | 82 | 187 |
| **humano** | **1,00** | **21** | 59 | 106 |
| maíz | 1,00 | 12 | 22 | 41 |
| *Harmonia axyridis* | 0,80 | 0 | 8 | 67 |
| *Folsomia candida* | 0,40 | 0 | 3 | 23 |
| *Apis mellifera* | 0,80 | 0 | 0 | 3 |

`BicC_Dm`, en su región vigente, tiene **cero** coincidencias perfectas de 21 nt en todo el
panel `[M]`. La conservación que vuelve atractivo a un gen esencial de un complejo como la
V-ATPasa es la misma que le trae off-targets, y acá está medida: el gen es defendible, pero
en un solo tramo.

**Los tres marcos de `D63` de la región**, con la herramienta de `N3` —a la que este bloque
le agregó una bandera `--gen` y que en la misma corrida reprodujo las seis anclas
publicadas— son **15 / 15 / 14**, con límite físico 0 y contexto neto 1 `[M]`. **La cifra
que se publica de esta región es 14**, la del marco 3, porque es la molécula que existiría.

**La región no depende de la fuente del CDS.** Los dos CDS independientes de `O2` difieren
en las posiciones 615, 678 y 1254; la 615 y la 678 caen dentro de 517-816, así que el
veredicto de **dos** de sus 280 ventanas depende de cuál CDS se use. **El CDS declarado es
el del genoma** (`D71`), y queda anotado como límite. Y `GCWP01` no cubre los nucleótidos
433-792, de modo que el tramo 517-792 va **sin datos** y no como cero en una tabla de
conservación por fuente (`D64`).

## 3. Las tres cuentas separadas

`§0` del plan de la ola 6 y §5 del preregistro obligan a no sumar en una sola cifra lo que
se hereda y lo que se recalcula. Modo `corregido`, backend `vienna`, tabla `NN3`, que es el
punto por defecto del preregistro `[M]`:

| | `BicC_Dm` + `V-ATPase B` | `V-ATPase B` + `BicC_Dm` |
| --- | ---: | ---: |
| Eficientes de las partes sueltas (26 + 14) | 40 | 40 |
| **Eficientes heredadas** | **38** (26 + 12) | **41** (14 + 27) |
| Heredadas que cambiaron de veredicto | 2 — las dos pierden | 3 — 2 ganan, 1 pierde |
| Distancia a la unión de las que cambiaron | 19 y 20 nt | 2, 46 y 47 nt |
| **Eficientes de juntura**, de 20 | **2** (j = 4 y 7) | **0** |
| De ésas, con blanco continuo de 21 nt | **0** | — |
| **Bloques del empalme con acierto fuera del vector** | **0** | **3, en maíz** |
| Eficientes totales | 40 | 41 |
| Δ contra la suma de las partes | **0** | **+1** |

**El orden importa, y acá se ve dónde.** Las dos moléculas tienen la misma composición y
difieren en una ventana eficiente, y las dos cuentas que la producen van en direcciones
opuestas. Con `BicC_Dm` a la derecha, sus heredadas suben de 26 a 27 y la juntura no aporta
ninguna; con `BicC_Dm` a la izquierda, la juntura aporta dos pero las heredadas de
`V-ATPase B` bajan de 14 a 12. Es el mismo mecanismo de banda de contexto que `C13` midió en las doce
quimeras de las regiones vigentes, donde `ATPaseD_Dm` + `MP_MRFV` daba +3 y el inverso −3
`[M]`.

Las cinco ventanas que cambiaron de veredicto están a 2, 19, 20, 46 y 47 nt de la unión
`[M]`, dentro del techo asimétrico que `C13` derivó del código: la secuencia ajena influye
hasta 72 nt corriente abajo del final de una ventana y hasta 59 corriente arriba de su
comienzo, porque la ventana de plegado de 80 nt con la que el original calcula accesibilidad
cruza la unión `[M]` el número, `[H]` la derivación.

**Ninguna ventana de juntura tiene blanco continuo de 21 nt**, en ninguno de los dos
órdenes, medido con el método de `research/ola5/N4_quimeras/scripts/junturas.py` que manda
el preregistro §5.2: un 21-mero tiene blanco continuo si existe como tramo contiguo en uno
de los dos genes que se quieren silenciar, en cualquiera de las dos hebras. O sea que las
dos ventanas de juntura eficientes del orden que queda en pie son capacidad de
silenciamiento que el conteo cuenta y que no tiene qué silenciar, que es exactamente lo que
`N4` había encontrado en las doce quimeras vigentes `[M]`.

Los ejes del ranking, regla conservadora `[M]`:

| Objeto | Ventanas | Eficientes | Eficacia | Limpieza | Limpias y eficientes | Veto |
| --- | ---: | ---: | ---: | ---: | ---: | :---: |
| `BicC_Dm` 922-1221 | 280 | 26 | 0,0929 | 0,9884 | 22 | no |
| `V-ATPase B` 517-816 | 280 | 14 | 0,0500 | 0,9432 | 10 | no |
| `BicC_Dm` + `V-ATPase B` | 580 | 40 | 0,0690 | 0,9670 | 32 | no |
| `V-ATPase B` + `BicC_Dm` | 580 | 41 | 0,0707 | 0,9639 | 33 | no |

**Cómo se lee esta tabla sin hacerle trampa.** Las dos quimeras tienen más eficientes
limpias en términos absolutos que cualquiera de sus partes (32 y 33 contra 22), pero miden
600 nt contra 300: el conteo absoluto no es comparable entre largos distintos, y el propio
`ranking.ejes` lo dice al definir los dos ejes como tasas «y por eso comparables entre
candidatos de largo distinto». Por tasa, las dos quimeras están **por debajo** de `BicC_Dm`
sola en los dos ejes. La quimera no compra rendimiento por nucleótido; compra cobertura de
un segundo fenotipo, que es lo que `D67` declaró como objetivo.

## 4. El empalme: lo que fabrica, y la alerta

El tamizado evalúa sólo lo que es nuevo: las dos regiones completas una vez y, por quimera,
el tramo de 40 nt que cruza la unión, que da exactamente sus 20 ventanas. Es la economía que
`C13` justificó y vale porque el estado de off-target de una ventana depende sólo de su
secuencia.

Sobre eso, `scripts/02_juntura_detalle.py` hace lo que el tamizado no hace: enumera los
bloques de 19, 20 y 21 nt de cada ventana de juntura, los busca exactos y en las dos hebras
en las seis referencias con un autómata de Aho-Corasick, y de cada acierto reporta cuántos
nucleótidos aporta cada gen. **La distinción que decide la alerta es ésa**: un bloque de 19
nt que entra entero en el aporte de un solo gen no lo fabrica el empalme —ya existía en ese
gen y la quimera lo hereda—; fabricado es el bloque que toma al menos un nucleótido de cada
lado.

De las 240 fichas de bloque, 19 tienen acierto, y se parten en dos grupos que no se parecen
`[M]`:

- **Heredados, 16.** Doce en el genoma del vector, que para dos genes del insecto es blanco
  y no riesgo. Y **cuatro en el transcriptoma humano**, en las ventanas j = 19 y 20 del
  orden `BicC_Dm` + `V-ATPase B`, con aporte 0+19 y 0+20: son bloques que están **enteros
  dentro de la mitad de `V-ATPase B`**, así que no los fabrica el empalme y vienen con el
  gen. Es coherente con el veto del gen entero, donde la humana aporta 21 ventanas con
  21/21.
- **Fabricados, 3, y los tres en maíz.** Son las ventanas j = 1, 2 y 3 del orden
  `V-ATPase B` + `BicC_Dm`: un bloque perfecto de 19 nt con 18 nt del primer gen y 1 del
  segundo, que no existe en ninguno de los dos y coincide en `NM_001153025.1` —proteína
  putativa de la superfamilia del citocromo P450— y `XM_020544485.2` —premnaspirodiene
  oxigenasa predicha—. Ninguna de las tres ventanas es eficiente.

Es el mismo fenómeno que `C13` había encontrado en `MP_MRFV` + `ATPaseD_Dm`, y acá aparece
en un gen nuevo y con una consecuencia de diseño concreta: **el orden `V-ATPase B` +
`BicC_Dm` queda descartado y el inverso no**, porque el orden inverso fabrica cero.

La fila de alerta está escrita en `resultados/alertas_juntura_d48_o3_corregido_vienna.tsv`,
con el esquema de columnas del inventario de `M6` para que se pueda pegar ahí, y con **los
cuatro campos obligatorios de `D48` completos**: organismo (maíz, *Zea mays*, peso 1,00),
exposición (peso de referencia y de criterio, con la fuente, y la decisión declarada abierta
por `D66`), gen involucrado (los dos loci con su anotación leída de la cabecera FASTA local,
sin inventarle símbolo a ninguno) y evidencia biológica (`gen_no_relacionado`, porque dos
oxigenasas de maíz no son el ortólogo de `BicC` ni de la V-ATPasa, más
`sin_bioensayo_consultado`). `decision_usuario` y `justificacion_usuario` van **vacías**: la
fila nace pendiente, que es lo que `D48` quiere, y la justificación la escribe el usuario y
no el motor.

**Lo que esa fila no es.** Una fila del inventario de `M6`. El generador de `M6` tamiza
**regiones**, y una juntura no es una región de ningún gen: es secuencia que fabrica el
ensamblado. Integrar las junturas al inventario es trabajo de la línea que mantiene `M6`.

## 5. Lo que estos números no dicen

**La región de `V-ATPase B` no es una región recomendada.** Es el insumo de esta medición
(`PREREGISTRO.md` §3). Desde `D72` la compuerta **rechaza** una región ausente del
inventario de `M6` con `alertas.RegionNoTamizada`, así que esta región no puede presentarse
como recomendada ni por descuido: hay que tamizarla primero, y son siete regiones nuevas
contando las seis de 22 nt de `R7`.

**El límite del tamizado de juntura.** La auditoría localiza coincidencia exacta de 19 a 21
nt. Los aciertos con un desapareo quedan como cuenta del tamizado, sin bloque ni transcripto
`[?]`.

**El límite que `N4` ya tenía.** «Blanco continuo» se mide como coincidencia exacta de 21
nt. Si una complementariedad incompleta diera actividad, las ventanas de juntura no serían
inútiles sino menos útiles, y no lo sabemos `[?]`.

**Dos ventanas de la región dependen de la fuente del CDS**, las que caen sobre las
posiciones 615 y 678.

**Y el límite que hereda toda la cadena.** El criterio de eficiencia del port no está
validado: en hemípteros ρ = +0,142, IC95 [−0,247, +0,492], n = 29 `[M]`. Un resultado in
silico es una hipótesis sobre eficacia, no una prueba.

## 6. La salvedad biológica, que va junto al resultado

Silenciando dos genes a la vez, si el bioensayo da negativo no se sabe cuál mitad falló. No
invalida el diseño —el objetivo declarado es cubrir dos efectos— pero es un argumento para
testear las partes por separado primero `[H]`. Y hay un dato que vuelve la salvedad
concreta: la mitad de `V-ATPase B` aporta 14 ventanas eficientes contra 26 de `BicC_Dm`, y
su región es la única admisible del gen. Si el efecto de movilidad y mortalidad depende de
esa mitad, la molécula está apostando a la mitad más restringida del diseño, y eso es una
predicción contrastable con las partes sueltas `[H]`.

## 7. Reproducibilidad

El CDS de `V-ATPase B` **no está versionado** —`sin_secuencias.py` rechaza toda racha de 21
nt— y se regenera en dos segundos desde el GFF de `O2`, que sí está versionado, y el genoma
público que ya está en disco, **sin necesidad de `miniprot`**. `BicC_Dm` es una de las
cuatro secuencias de EPILAB, así que ninguna salida de este bloque escribe bases: las
ventanas y los bloques van por hash corto.

La referencia humana no está en `work/offtarget_db/` y hay que bajarla del FTP del NCBI. Es
la misma que registró `research/ola3/C6_panel_y_largo/REPORT.md` §192, y **el nombre del
archivo importa**: el identificador del panel es `humano_rna`, y `offtarget_21nt.py` toma el
nombre de la base del nombre del archivo.

```bash
# 0. la referencia humana del panel, si no esta (135 MB; sha256 en el archivo .sha256)
mkdir -p work/W5/ref && curl -o work/W5/ref/humano_rna.fna.gz \
  https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_rna.fna.gz

# 0b. el tamizado de los cuatro genes de EPILAB con las SEIS referencias, que es lo que
#     el ancla C necesita. `offtarget_full` va sin --mm1, como el original.
python tools/sifi21_port/offtarget_21nt.py --consulta work/sifi_check/*_full.fasta \
    --db work/offtarget_db/*.fna.gz work/W5/ref/humano_rna.fna.gz \
    --salida work/sifi_check/offtarget_full
python tools/sifi21_port/offtarget_21nt.py --consulta work/sifi_check/*_full.fasta --mm1 \
    --db work/offtarget_db/*.fna.gz work/W5/ref/humano_rna.fna.gz \
    --salida work/O3/offtarget_mm1_seis       # y se reparte en offtarget_mm1_<gen>/

# 1. el CDS, desde el GFF de O2 y el genoma publico local
python research/ola6/O2_vatpase_b/scripts/02_extraer_cds.py research/ola6/O2_vatpase_b \
    work/offtarget_db/GCA_975739785.1_ihDalMaid1.1_genomic.fna.gz XP_054288745.1 VATPaseB_Dm
mkdir -p work/O3/fasta
cp research/ola6/O2_vatpase_b/resultados/VATPaseB_Dm_cds.fna work/O3/fasta/VATPaseB_Dm_full.fasta

# 2. las tres anclas del preregistro. Si alguna falla, la linea para aca.
python research/ola6/O3_quimera_bicc_vatpase_b/scripts/00_anclas.py

# 3. perfil de eficiencia del gen entero y tamizado del panel de seis
python tools/sifi21_port/run_sifi.py work/O3/fasta/VATPaseB_Dm_full.fasta \
    --modo corregido --backend vienna --salida work/O3/sifi/full_corregido
python tools/sifi21_port/offtarget_21nt.py --consulta work/O3/fasta/consultas_pasoA.fasta \
    --mm1 --db work/offtarget_db/*.fna.gz --salida work/O3/offtarget
python tools/sifi21_port/offtarget_21nt.py --consulta work/O3/fasta/consultas_pasoA.fasta \
    --mm1 --db work/W5/ref/humano_rna.fna.gz --salida work/O3/offtarget_humano

# 4. la region, por el criterio de PREREGISTRO.md seccion 2
python research/ola6/O3_quimera_bicc_vatpase_b/scripts/01_region_vatpase_b.py

# 5. los tres marcos de D63; re-verifica las seis anclas de N3
python research/ola5/N3_marcos/scripts/tres_marcos.py \
    --gen VATPaseB_Dm=517-816:work/O3/fasta/VATPaseB_Dm_full.fasta \
    --nota "region de O3, D74" \
    --salida research/ola6/O3_quimera_bicc_vatpase_b/resultados

# 6. las dos quimeras, los dos ordenes, en el punto por defecto
GEN="--gen BicC_Dm=922-1221 --gen VATPaseB_Dm=517-816:work/O3/fasta/VATPaseB_Dm_full.fasta"
python research/ola3/C13_quimeras_region_recomendada/scripts/quimeras_v2.py --nombre o3 \
    $GEN --modo corregido --backend vienna \
    --resultados research/ola6/O3_quimera_bicc_vatpase_b/resultados

# 7. ejes del ranking y riesgo del empalme, con la humana en el panel
python research/ola3/C13_quimeras_region_recomendada/scripts/offtarget_ranking.py \
    --nombre o3 $GEN --modo corregido --backend vienna --rehacer-tamizaje \
    --db work/offtarget_db/*.fna.gz work/W5/ref/humano_rna.fna.gz \
    --resultados research/ola6/O3_quimera_bicc_vatpase_b/resultados

# 8. la auditoria de la juntura, que es la que decide la alerta, y la fila de D48
python research/ola6/O3_quimera_bicc_vatpase_b/scripts/02_juntura_detalle.py --modo corregido
python research/ola6/O3_quimera_bicc_vatpase_b/scripts/03_alerta_d48.py
```

Tiempos medidos: perfil del CDS 10 s, cada tamizado de las seis locales 70 s, la humana
sola 42 s, el tamizado con `--mm1` de los cuatro genes de EPILAB 2 min 54 s, la auditoría de
juntura 26 s, los tres marcos menos de 1 s, las tres anclas 2 min.

### Archivos

| Archivo | Qué es |
| --- | --- |
| `PREREGISTRO.md` | el criterio, escrito antes de medir. Manda sobre todo lo demás |
| `scripts/00_anclas.py` | las tres anclas de §6; devuelve 1 si alguna falla |
| `resultados/region_vatpase_b.json` | el criterio ejecutado, las 1.184 regiones, los dos top-3 y el veto por referencia |
| `resultados/tres_marcos.{tsv,json}` | los tres marcos de `D63` de la región (15/15/14) y las seis anclas de `N3` |
| `resultados/quimeras_eficiencia_o3_corregido_vienna.tsv` | las tres cuentas por orden |
| `resultados/quimeras_ventanas_cambiadas_o3_corregido_vienna.tsv` | las cinco heredadas que cambiaron, con su distancia |
| `resultados/ejes_ranking_o3_corregido_vienna.tsv` | los dos ejes de las partes y de las quimeras, en las dos reglas |
| `resultados/empalmes_offtarget_o3_corregido_vienna.json` | aciertos del empalme por referencia y criterio |
| `resultados/juntura_detalle_o3_corregido_vienna.json` | los 240 bloques, con aporte por gen y sin secuencias |
| `resultados/juntura_resumen_o3_corregido_vienna.tsv` | las dos cuentas de juntura y los bloques fabricados |
| `resultados/juntura_alertas_o3_corregido_vienna.json` | los tres bloques fabricados, crudos |
| `resultados/alertas_juntura_d48_o3_corregido_vienna.tsv` | la fila de alerta con el esquema de `M6` y los cuatro campos de `D48` |
