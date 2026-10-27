# R8 — La quitinasa que impacta `eth_Dm` 193-392: tiene ortólogo en tres de las seis, y la ventana cae en zona variable

**Fecha:** 2026-10-27. **Issue:** #32. **Entrada 21** de la sección de la ola 6 de
`00_meta/PREGUNTAS_ABIERTAS.md`. **Antecedentes:** `D73` (la firma) y `D72` (la compuerta).

## El resultado, en un párrafo

La coincidencia perfecta de 21 nt que `eth_Dm` 193-392 tiene contra *Homalodisca vitripennis*
impacta un gen que **sí tiene ortólogo recíproco en tres de las cinco referencias restantes**
del panel —*Harmonia axyridis*, *Apis mellifera* y *Folsomia candida*, las tres anotadas
«probable chitinase 2»— y **no lo tiene en maíz ni en humano**, donde el mejor acierto existe
pero no es recíproco `[M]`. Ahora bien, eso **no traslada el riesgo**: la ventana cae en los
codones 101-108 del marco de lectura de la quitinasa, que es un tramo **variable** y no un
dominio conservado, y la mejor casi-coincidencia del 21-mero contra cada uno de esos
transcriptos ortólogos es de **8 desajustes sobre 21**, que es exactamente la mediana de lo
que da el azar `[M]`. `[H]` La lectura es que el acierto es una coincidencia de 21 nt
específica de `LOC124369889` de *H. vitripennis* y no una zona del gen que convenga evitar
por pertenecer a una familia conservada: **la firma de `D73` queda confirmada, no cambiada**,
y su condición sigue siendo la misma, la decisión abierta sobre la exposición de
*H. vitripennis*, que esta línea **no** resuelve.

## 1. En qué máquina y con qué herramienta

Siguiendo la regla de `D71` —antes de declarar una corrida imposible por entorno hay que
decir en cuál máquina—, corresponde decir también dónde sí se pudo correr.

Se corrió en **la máquina de Joaquín** (macOS, el mismo árbol de trabajo donde se cerró
`R7`), con **BLAST+ 2.17.0+** (`tblastn: 2.17.0+`) y **Biopython 1.88** sobre Python 3.11.17.

`[M]` **El issue declaraba que BLAST+ faltaba en las dos máquinas, y en ésta ya no falta:**
se instaló desde `bioconda` en un entorno conda aparte (`blastn`, `tblastn`, `blastp`,
`makeblastdb`). Esto importa más allá de R8, porque la falta de BLAST+ es lo que el propio
issue nombra como freno de `F1` (entrada 12) y de parte de `O3`. No se usó `miniprot`, que
sigue sin estar acá; la máquina de Luca lo tiene (0.18-r281, WSL) y para esta pregunta no
hizo falta.

Nada salió de la máquina: las seis referencias del panel se leyeron de disco, como exige la
regla de confidencialidad.

## 2. Cómo se midió, y por qué así

La pregunta es de **homología**, no de coincidencia exacta, así que `offtarget_21nt.py` no
la cubre: Aho-Corasick es exacto por construcción y no ve un ortólogo que difiera en unos
pocos nucleótidos. Tres decisiones de método, cada una con su antecedente medido en el repo:

1. **A nivel proteína.** `C5` midió 77-84 % de identidad en nucleótido contra **0,866** de
   mediana en proteína: el ADN codificante diverge en la tercera posición del codón sin
   cambiar la proteína, así que buscar el ortólogo en nucleótido subdeclara.
2. **Ortología recíproca, nunca el gen con el mismo nombre.** `C12` midió 78,2 % de
   concordancia sobre 1.152 pares recíprocos, y el repositorio tiene medido que elegir por
   nombre mueve el conteo de ventanas eficientes un 65 %. La ida es `tblastn` de la proteína
   de la quitinasa contra cada referencia; la vuelta toma el ORF más largo del mejor acierto
   y lo devuelve contra el transcriptoma de *H. vitripennis*. El par es recíproco **sólo** si
   vuelve a `LOC124369889`.
3. **La consulta es el ORF más largo** del transcripto `XM_046828031.1`, 470 aa, marco 0,
   que arranca en el nt 133. El criterio de corte es `e-value ≤ 1e-5` y el mejor acierto se
   elige por `bitscore`.

## 3. El ortólogo, referencia por referencia

`[M]` `research/ola6/R8_quitinasa_eth/resultados/ortologos_quitinasa.tsv`

| Referencia | Mejor acierto | Anotación | Identidad | Cobertura | *e*-value | ¿Recíproco? | ¿Ortólogo? |
|---|---|---|---:|---:|---:|---|---|
| *Harmonia axyridis* | `XM_045615311.1` | probable chitinase 2 (`LOC123678324`) | **55,4 %** | 81 % | 4,6e-160 | sí | **sí** |
| *Apis mellifera* | `XM_026445083.1` | probable chitinase 2 (`LOC551344`) | **51,0 %** | 80 % | 2,0e-134 | sí | **sí** |
| *Folsomia candida* | `XM_022095532.2` | probable chitinase 2 (`LOC110848341`) | **47,9 %** | 81 % | 5,5e-122 | sí | **sí** |
| *Homo sapiens* | `NM_201653.4` | chitinase acidic (**CHIA**) | 36,4 % | 79 % | 3,5e-83 | **no** | no, no recíproco |
| *Zea mays* | `XM_008682752.4` | **uncharacterized protein** (`LOC100191620`) | 23,8 % | 69 % | 2,4e-23 | **no** | no, no recíproco |
| *H. vitripennis* | `XM_046828031.1` | la fuente, `LOC124369889` | 100 % | 100 % | 0 | n/a | es la consulta |

Tres precisiones que hacen falta para leer la tabla sin sobredeclarar:

- **Que las tres anotaciones recíprocas digan «probable chitinase 2» es corroboración
  independiente**, no el criterio: el nombre no se usó para decidir, se leyó después.
- **«No recíproco» no quiere decir «la familia no está».** En humano el mejor acierto es
  `CHIA`, que **es** una quitinasa de verdad; lo que la prueba recíproca dice es que no es un
  par 1:1 con `LOC124369889`, no que *Homo sapiens* carezca de quitinasas. La distinción
  importa porque de ella depende cómo se lee el riesgo, y mezclarlas sería el mismo error que
  `C12` evitó al exigir reciprocidad.
- **El acierto de maíz es literalmente «uncharacterized protein»** y se reporta contado, no
  escondido, que es la regla que `F1` fijó para los pares sin nombre informativo. A 23,8 % de
  identidad y 69 % de cobertura, es lo esperable entre una quitinasa de insecto y una planta,
  que tiene su propia familia de quitinasas sin relación 1:1 con ésta.

## 4. La ventana: dónde cae y cuánto se parece

`[M]` `research/ola6/R8_quitinasa_eth/resultados/ventana_conservacion.tsv`

La ventana —`eth_Dm` 347-367, la única con 21/21 de esa región— se aparea con el transcripto
`XM_046828031.1` en los **nt 434-454, en la hebra reverso-complementaria**, que es la
orientación con capacidad de silenciamiento. Eso cae **dentro del CDS**: el ORF arranca en el
nt 133, así que son los **codones 101-108** de la proteína.

| Referencia | Identidad de la proteína entera | Identidad en los 8 codones de la ventana | Desajustes mínimos del 21-mero |
|---|---:|---:|---:|
| *H. axyridis* | 49,6 % | **25,0 %** | **8** |
| *A. mellifera* | 45,1 % | 50,0 % | **8** |
| *F. candida* | 45,1 % | **25,0 %** | **8** |
| *Homo sapiens* | 32,1 % | **25,0 %** | **8** |
| *Zea mays* | 21,7 % | **0,0 %** | **8** |

**La ventana cae en zona variable, no en un dominio conservado.** En cuatro de las cinco
referencias la identidad de proteína en esos ocho codones está **por debajo** de la identidad
de la proteína entera; la excepción es *A. mellifera* (50,0 contra 45,1), y sobre ocho
residuos esa diferencia es una sola posición, así que no se lee como señal.

## 5. Los dos controles, sin los cuales el «8» no se puede leer

Que las cinco referencias dieran **exactamente** 8 desajustes es lo bastante raro como para
exigir control antes de interpretarlo. Los dos corren dentro del script y con semilla fija:

- **Control positivo.** La misma ventana contra su propio transcripto `XM_046828031.1` da
  **0 desajustes**, como tiene que dar. El script aborta si no da cero.
- **Nulo.** Cuarenta 21-meros al azar contra el mismo transcripto ortólogo
  (`XM_045615311.1`) dan **mínimo 6, mediana 8, máximo 10** desajustes.

`[H]` O sea que **8 es la mediana del azar**: la mejor casi-coincidencia del 21-mero real
contra los ortólogos es indistinguible de la de una ventana inventada. Es la diferencia entre
«hay 8 desajustes, poco» y «hay 8 desajustes, que es lo que da cualquier secuencia»: lo
segundo es lo que se midió, y es lo que permite decir que el acierto **no se extiende** a los
ortólogos. Un siRNA que dirige corte necesita apareamiento contiguo y casi perfecto; 8 de 21
no es eso por ningún criterio del campo.

## 6. Qué se concluye, y qué no

`[H]` **La firma de `D73` queda confirmada y no se reescribe.** Lo que la firma declaró
faltante era si el gen impactado pertenecía a una familia conservada en el resto del panel.
La respuesta es mixta y, leída entera, no mueve el veredicto: el **gen** tiene ortólogo
recíproco en tres referencias, pero la **ventana** cae en su tramo variable y ningún ortólogo
la reproduce ni de lejos. El riesgo medible sigue confinado a `LOC124369889` de
*H. vitripennis*, que es exactamente lo que la fila decía. **Una firma confirmada también es
resultado**, y por eso no hay ADR nuevo: no hay nada que corregir en `decisiones.tsv`.

**La condición de la firma sigue abierta y R8 no la toca.** El veredicto bloqueante depende
de la exposición de *H. vitripennis* (pedido 4, `D47` contra `D18`), que es una decisión
aparte y del equipo.

**Sobre la propuesta de 22 nt para `eth_Dm`, que el issue pide decir aparte.** `[H]` Este
resultado **baja** la consecuencia biológica que se le puede atribuir al único acierto
perfecto de `eth_Dm` 193-392: no es un acierto en un dominio conservado de una familia
multigénica, es una coincidencia en un tramo variable de un gen sin relación funcional con el
blanco. Lo que **no** hace es despejar la región: sigue teniendo una coincidencia perfecta de
21 nt contra un cicadélido no objetivo, y la región **vigente** del mismo gen, `eth_Dm`
114-313, sigue teniendo **cero** contra todo el panel `[M]`. Si hubiera que elegir entre las
dos por este eje, la vigente sigue ganando, y nada de lo medido acá cambia eso.

## 7. Límites

- `tblastn` contra referencias de **ARN** encuentra transcriptos, no genes: una ausencia de
  acierto es ausencia en el transcriptoma publicado, no en el genoma. Ninguna de las seis
  referencias es un proteoma, así que la vuelta se hace sobre el ORF más largo del
  transcripto y no sobre la proteína anotada.
- La reciprocidad se evaluó con **un** transcripto por acierto, el de mejor `bitscore`. Para
  genes con variantes de empalme eso puede elegir una variante y no la canónica.
- El nulo son 40 sorteos contra **un** ortólogo, suficiente para situar el 8 y no para dar
  un intervalo.
- No se midió si la ventana cae en un dominio catalítico nombrado: haría falta `InterPro` o
  `hmmer` con `Pfam`, que no están en la máquina. Lo que se midió es conservación empírica
  entre los ortólogos recuperados, que es lo que el issue pedía.

## 8. Cómo reproducirlo

```bash
# paso 1: el ortologo en cada referencia del panel, con ida y vuelta (BLAST+ en el PATH)
python3 research/ola6/R8_quitinasa_eth/scripts/01_ortologos.py

# paso 2: donde cae la ventana, cuanto se conserva, y los dos controles (Biopython)
python3 research/ola6/R8_quitinasa_eth/scripts/02_ventana_conservada.py
```

Las secuencias intermedias quedan en `work/R8/`, que no se versiona. Las salidas versionadas
no llevan nucleótidos: sólo coordenadas, identidades y conteos de desajustes.
