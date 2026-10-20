# El panel ampliado y el largo de la ventana: dos huecos de W7, medidos

Fecha: 2026-10-20. Complementa `research/ola2/W7_ranking/REPORT.md`, no lo reemplaza: el
ranking, los nulos y el barrido de pesos siguen siendo los de ahí. Acá se contestan dos
preguntas que ese informe no se hizo, y las dos tocan su recomendación central.
Reproducible con `tools/sifi21_port/panel_y_k.py`; los números están en
`resultados/panel_y_k.json`. Marcadores de `CLAUDE.md`.

## El resultado, en un párrafo

**La recomendación de W7 de mover la región en los dos genes del insecto no sobrevive a
agregar al panel el cicadélido más cercano a la chicharrita con genoma anotado.** En
`BicC_Dm` la región que W7 propone (2123-2422) tiene **19 ventanas con coincidencia perfecta
de 21 nt en el transcriptoma de *Macrosteles quadrilineatus***, casi el doble que la región
que eligió EPILAB (10): en ese eje la recomendación empeora las cosas. En `ATPaseD_Dm` las
dos regiones contienen las mismas 12 ventanas comprometidas, así que la mudanza no cambia
nada. Los dos genes virales quedan intactos: cero coincidencias perfectas, igual que antes.
**Hay salida y está medida**, y es distinta para cada gen: en `BicC_Dm` la región **922-1221
tiene 36 ventanas eficientes contra las 37 de la que W7 propone y escapa al veto**, así que
se pierde una ventana y se ganan las 19 comprometidas; en `ATPaseD_Dm` **ninguna región de
300 nt del gen escapa**, y hay que bajar a 200 nt, donde 94 de 272 escapan y la mejor
(88-287) tiene 17 eficientes.

Y sobre el largo de la ventana: **el conteo de eficientes casi no cambia entre 21 y 22 nt,
pero el conjunto de ventanas eficientes sí cambia casi entero** —el índice de Jaccard va de
0,20 a 0,39—, de modo que la pregunta «cuántas» es estable y la pregunta «cuáles» no lo es.
En `MP_MRFV` la mejor región de 200 nt se muda de 72-271 a **820-1019**, al otro extremo del
gen.

---

## 1. Por qué faltaban estas dos cosas

**El panel.** W7 corrió el veto contra seis referencias y declaró como límite que faltan
cicadélidos nativos y parasitoides, que no tienen ensamblado. Lo que no registró es que
**falta la especie que el propio proyecto midió como la que más descarta**: `pipeline/REPORT.md`
§4.2 encontró que *Macrosteles quadrilineatus* descarta 700 ventanas contra 128 de
*Homalodisca vitripennis* y 10 del maíz, **70 veces más que el cultivo**, y que 613 de esos
700 descartes no los ve ninguna otra especie del catálogo. El catálogo de
`pipeline/no_objetivo_catalogo.py` la describe como «el control positivo bueno»: es
Cicadellidae, subfamilia Deltocephalinae, la misma que *Dalbulus*, y además vector de
fitoplasmas. `[E]`

También falta **humano**, que el investigador nombró explícitamente en el checkpoint
—*«puede resultar que también le pegue al humano y al maíz»*— y que `CLAUDE.md` pide entre
los organismos no objetivo. No estaba en el panel de W7 ni declarado como ausencia. `[E]`

**El largo.** El investigador pidió en el checkpoint un benchmark de 21 contra 22 nt y el
plan de desarrollo lo lista como opcional 2. No se había hecho: `azar_por_k.md` barre *k* de
15 a 21 pero para la cuenta de azar en off-targets, que es otra pregunta. Y hay un argumento
del propio repositorio que lo vuelve más que opcional: `R1_fundamentos` §2.1 establece `[E]`
que **el largo del siRNA lo fija la Dicer del organismo que procesa, no quien diseña**
—dípteros y coleópteros 21 nt, himenópteros y ortópteros 22, lepidópteros 20— y que **para
hemípteros, el orden de la chicharrita, no hay perfil publicado** `[?]`. Correr sólo a 21 nt
es fijar un parámetro que nadie midió en la especie.

## 2. Cómo se midió, y la verificación previa

Las dos referencias nuevas se bajaron de NCBI a disco: *M. quadrilineatus*
`GCF_028750875.1_UCM_ALF_1.0_rna` (36.629 secuencias, 102,7 Mb) y *H. sapiens*
`GCF_000001405.40_GRCh38.p14_rna` (186.185 secuencias, 718,6 Mb). Son transcriptomas, igual
que las cinco no objetivo del panel de W7, así que el criterio de genoma contra transcriptoma
sigue cumplido por construcción. Sólo entró tráfico: **las secuencias de EPILAB no salieron de
la máquina** y el tamizaje corre local con `offtarget_21nt.py`.

**Agregar referencias sólo puede agregar vetos, nunca sacarlos**, así que correr las dos
nuevas por separado basta para contestar si las regiones de W7 sobreviven, sin volver a bajar
las seis originales (379 MB).

Antes de medir nada nuevo, el script verifica que este entorno reproduce W7. Con ViennaRNA
2.7.2 y modo corregido da **123, 30, 171 y 29** ventanas eficientes, los cuatro conteos
publicados exactos; en modo fiel da 142, 39, 223 y 35, que es la columna «fiel + 2.7.2» de
`sifi21_reproduccion.md` §1. Si alguno no coincide, `panel_y_k.py` aborta antes de calcular.
`[E]`

## 3. El panel ampliado

Coincidencias perfectas de 21 nt, el mismo criterio con el que W7 define su veto:

| Gen | Región | Eficientes | 21/21 en *M. quadrilineatus* | 21/21 en humano | ¿Vetada? |
|---|---|---:|---:|---:|---|
| `MP_MRFV` | 1-200 (EPILAB) | 30 | 0 | 0 | no |
| `MP_MRFV` | 72-271 (W7) | 38 | 0 | 0 | no |
| `CP_MRFV` | 201-400 (EPILAB) | 17 | 0 | 0 | no |
| `CP_MRFV` | 99-298 (W7) | 21 | 0 | 0 | no |
| `BicC_Dm` | 264-563 (EPILAB) | 20 | **10** | 0 | **sí** |
| `BicC_Dm` | 2123-2422 (W7) | 37 | **19** | 0 | **sí** |
| `ATPaseD_Dm` | 151-450 (EPILAB) | 18 | **12** | 0 | **sí** |
| `ATPaseD_Dm` | 72-371 (W7) | 21 | **12** | 0 | **sí** |

`[E]` Tres lecturas, en orden de consecuencia.

**La recomendación de `BicC_Dm` se da vuelta en este eje.** W7 propone 2123-2422 porque deja
afuera las 22 ventanas que coinciden con *H. vitripennis*. Contra *M. quadrilineatus* esa
misma región tiene 19 ventanas comprometidas y la de EPILAB tiene 10: **mudarse ahí duplica
la exposición al pariente más cercano para evitar la del más lejano**. En el gen entero hay
101 ventanas con 21/21 contra *Macrosteles*, repartidas en 11 tramos, y el de 2189-2207 cae
justo adentro de la región propuesta.

**En `ATPaseD_Dm` la mudanza es indiferente y el problema es peor de lo que parecía.** Las 12
ventanas comprometidas del gen están todas juntas en 294-305, dentro de las dos regiones. Y
como el gen tiene 471 ventanas, **ninguna región de 300 nt puede evitarlas**: las 172 posibles
quedan vetadas, 0 escapan.

**Humano da cero en los cuatro genes, bajo el criterio de bloque perfecto.** Es el dato
tranquilizador, y conviene decirlo con su alcance: es ausencia de homología de secuencia en
un transcriptoma de referencia, no un ensayo de toxicidad. Bajo el criterio laxo de bloque
≥19 nt sí aparecen ventanas (3, 2, 12 y 7), que es el mismo patrón que ya tenían las otras
referencias.

### 3.1 Cuánto material queda, y la salida para cada gen

La objeción obvia a un filtro más duro es que deje al proyecto sin material. Se mide:

| Gen | Largo | Regiones que escapan | Mejor región sin veto | Eficientes | Mejor sin restricción |
|---|---:|---:|---|---:|---|
| `BicC_Dm` | 300 | 497 / 2.201 | **922-1221** | **36** | 2123-2422 con 37 |
| `BicC_Dm` | 250 | 741 / 2.251 | 973-1222 | 29 | la misma |
| `BicC_Dm` | 200 | 991 / 2.301 | 1022-1221 | 25 | la misma |
| `ATPaseD_Dm` | 300 | **0 / 172** | — | — | 136-435 con 24 |
| `ATPaseD_Dm` | 250 | 44 / 222 | 38-287 | 17 | 122-371 con 21 |
| `ATPaseD_Dm` | 200 | 94 / 272 | **88-287** | **17** | 272-471 con 19 |
| `ATPaseD_Dm` | 150 | 161 / 322 | 136-285 | 15 | la misma |

`[E]` **En `BicC_Dm` el costo de respetar el veto ampliado es una sola ventana eficiente**:
922-1221 tiene 36 contra las 37 de la región que W7 propone, y a cambio pasa de 19 ventanas
comprometidas a cero. `[H]` Es la recomendación que sale de este informe y es estrictamente
mejor que la de W7 en los dos ejes a la vez.

`[E]` **En `ATPaseD_Dm` la salida no es mudarse, es acortar.** A 300 nt el gen no tiene
ninguna región limpia; a 200 nt tiene 94, y la mejor (88-287) tiene 17 eficientes contra las
18 de la región que eligió EPILAB. `[H]` Acortar además devuelve el diseño al rango de
150-250 nt que el propio investigador declaró, del que las dos regiones de 300 nt se salen.

## 4. Veintiuno contra veintidós

Mismo motor, mismo modo corregido, misma versión de ViennaRNA; lo único que cambia es
`sirna_size`.

| Gen | Eficientes a 21 | a 22 | En la región de EPILAB, 21 → 22 | Mejor región a 21 | Mejor a 22 | Jaccard |
|---|---:|---:|---|---|---|---:|
| `MP_MRFV` | 123 (9,9 %) | 123 (9,9 %) | 30 → 21 | 72-271 (38) | **820-1019 (32)** | 0,37 |
| `CP_MRFV` | 30 (5,9 %) | 29 (5,7 %) | 17 → 15 | 99-298 (21) | 77-276 (22) | 0,20 |
| `BicC_Dm` | 171 (6,8 %) | 174 (7,0 %) | 20 → 16 | 2123-2422 (37) | 2122-2421 (41) | 0,32 |
| `ATPaseD_Dm` | 29 (6,2 %) | 32 (6,8 %) | 18 → 23 | 136-435 (24) | 135-434 (28) | 0,39 |

`[E]` **El agregado es estable y el detalle no.** Las tasas de eficiencia se mueven menos de
un punto porcentual, pero los conjuntos de ventanas eficientes casi no se superponen: **entre
el 41 % y el 67 % de las ventanas que son eficientes a 21 nt no lo son a 22**, y la cifra es
casi igual en la otra dirección. El índice de Jaccard —la intersección sobre la unión— va de
0,20 a 0,39. En `CP_MRFV`, el caso extremo, sólo 10 ventanas son eficientes a los dos largos,
contra 20 que lo son sólo a 21 y 19 sólo a 22. No es ruido numérico: la regla de eficiencia
está evaluando otra molécula.

La consecuencia práctica aparece en `MP_MRFV`, que es el mejor candidato del ranking: su
mejor región de 200 nt se muda de 72-271 a 820-1019, **al otro extremo del gen**. En los dos
genes del insecto, en cambio, la mejor región se corre una sola posición, así que ahí la
elección sí es robusta al largo. `[E]`

`[H]` **Lectura.** Que el conteo total no se mueva es lo que permite seguir usando si-Fi21 a
21 nt para comparar genes entre sí, que es lo que hace el ranking de W7; ese resultado no
queda tocado. Lo que no se puede hacer es defender una región concreta de `MP_MRFV` sin
decir a qué largo se la eligió, porque a 22 nt la respuesta es otra parte del gen. Y como
para hemípteros no hay perfil de largo publicado, **no hay forma de saber hoy cuál de las dos
respuestas es la correcta**: lo honesto es reportar las dos.

Sobre off-targets el largo casi no importa: a 22 nt *Macrosteles* da 90 ventanas con
coincidencia perfecta en `BicC_Dm` contra 101 a 21 nt, y 11 contra 12 en `ATPaseD_Dm`. El
veto se dispara igual con los dos largos. `[E]`

## 5. Lo que esto no mide

No mide **si *M. quadrilineatus* debe contar como organismo no objetivo**. Es a su vez plaga
y vector de fitoplasmas, y `pipeline/REPORT.md` §4.2 ya lo había marcado como una pregunta
para el laboratorio `[?]`. Lo que este informe muestra es que **la recomendación de W7
depende de esa respuesta**, que es distinto de afirmar que esté mal.

No mide **el resto del catálogo**. `pipeline/no_objetivo_catalogo.py` tiene 26 especies y acá
se agregaron dos. Las otras dieciocho que faltan podrían mover esto de nuevo, y el patrón de
hasta ahora —el riesgo se concentra en los cicadélidos— sugiere que *Nilaparvata lugens* y
*Acyrthosiphon pisum* son las siguientes a mirar.

No mide **eficacia**, ni cambia nada de lo que W7 estableció sobre nulos, percentiles y
barrido de pesos. Y las regiones que propone acá heredan todos los pendientes de W7: no están
verificadas contra la conservación dentro de *D. maidis*, y el panel sigue sin parasitoides.

## 6. Cómo reproducirlo

```bash
# referencias nuevas (sólo entra tráfico; las secuencias no salen)
curl -o macrosteles_rna.fna.gz https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/028/750/875/GCF_028750875.1_UCM_ALF_1.0/GCF_028750875.1_UCM_ALF_1.0_rna.fna.gz
curl -o humano_rna.fna.gz      https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_rna.fna.gz

# perfil de eficiencia a 21 nt (el mismo de W7)
python tools/sifi21_port/run_sifi.py work/sifi_check/*_full.fasta \
    --modo corregido --backend vienna --salida work/sifi_check/salida

# off-targets contra las dos referencias nuevas, a 21 y a 22 nt
python tools/sifi21_port/offtarget_21nt.py --consulta work/sifi_check/*_full.fasta \
    --db macrosteles_rna.fna.gz humano_rna.fna.gz --salida work/sifi_check/offtarget_panel_nuevo
python tools/sifi21_port/offtarget_21nt.py --size 22 --consulta work/sifi_check/*_full.fasta \
    --db macrosteles_rna.fna.gz humano_rna.fna.gz --salida work/sifi_check/offtarget_22nt

# el análisis, con la verificación de anclas adelante
python tools/sifi21_port/panel_y_k.py --perfil work/sifi_check/salida \
    --offtarget-nuevo work/sifi_check/offtarget_panel_nuevo/offtarget_por_sirna.tsv \
    --fasta work/sifi_check --off22 work/sifi_check/offtarget_22nt/offtarget_por_sirna.tsv \
    --json research/ola3/C6_panel_y_largo/resultados/panel_y_k.json
```

Necesita `ViennaRNA`, `biopython`, `pyahocorasick` y `numpy`, y las secuencias de EPILAB en
`work/sifi_check/` (fuera del control de versiones).
