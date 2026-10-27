# si-Fi21 portado: criterio de eficiencia, en Python 3 y sin interfaz gráfica

Reimplementación del motor de eficiencia de **si-Fi21**, la herramienta en la que
el investigador invitado dijo que se basa el pipeline de diseño de EPILAB. Corre
desde la línea de comandos, es reproducible y versionable, y tiene dos modos: uno
que reproduce el programa original tal cual —para auditar números hechos con él— y
uno con los arreglos documentados en [`CAMBIOS.md`](CAMBIOS.md).

Origen: Lück et al. 2019, *Front Plant Sci* 10:1023, `10.3389/fpls.2019.01023`;
fuente en `github.com/snowformatics/siFi21-`. Licencia del original en conflicto
entre el artículo (CC BY-SA 4.0) y SourceForge (CC BY-NC 2.0); uso académico. `[?]`

> **Verificado contra el original, en los cuatro genes.** si-Fi21, corrido con su
> interfaz y sus valores por defecto, da 42, 32, 133 y 212 siRNA eficientes para
> `ATPaseD_Dm`, `CP_MRFV`, `MP_MRFV` y `BicC_Dm`. Este port en modo fiel, con el
> mismo RNAplfold 2.1.5, da **los mismos cuatro números**. La curva del «RNAi design
> plot» también se reproduce tramo por tramo. Detalle y salidas crudas en
> `research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md` §0.
>
> **Para correr el original hace falta un arreglo:** si-Fi no encuentra su propio
> RNAplfold —pasa `cwd` a `Popen` con el ejecutable por nombre pelado— y falla en
> silencio, con el botón Start sin hacer nada. Hay que lanzarlo con
> `%LOCALAPPDATA%\siFi2015\RNAplfold` y `...\Bowtie` en el PATH. Y su tabla de
> resultados no se muestra en pantalla: sale por **Save as → Table (CSV)**,
> escribiendo la extensión a mano.

## Por qué existe

si-Fi21 original es una aplicación Qt4 de escritorio que solo corre en Windows con
Python 2.7, abre diálogos modales en medio del cálculo y no es automatizable. No
sirve como dependencia de un pipeline. Pero es la línea de base del campo y la
referencia declarada del laboratorio, así que hace falta poder correrlo y
compararse con él. Ver `00_meta/CAMINOS_PROBADOS.md`.

## Qué calcula

Por cada ventana de 21 nt de la secuencia, los tres filtros de si-Fi:

- **Selección de hebra guía:** ΔG del extremo 5' antisentido ≥ ΔG del 5' sentido,
  por vecinos más cercanos con extremos colgantes (tablas de ARN de Chen et al.
  2012 y de extremos colgantes de Turner & Mathews 2010).
- **Estabilidad de extremos:** la diferencia anterior ≥ 1 kcal/mol. Implica la
  condición de selección de hebra, así que con las dos activadas la primera no
  aporta nada; vale saberlo al leer el desglose.
- **Accesibilidad del sitio blanco:** probabilidad de que los últimos 8 nt de la
  ventana estén desapareados ≥ 0,1, con RNAplfold (`-W 80 -L 40 -u 21 -T 22`).

Y después la regla de los nucleótidos terminales (19 y 2), que es donde los dos
modos difieren. Todo a **22 °C**, que es lo que el original tiene fijado.

No hace tamizaje de off-targets: eso ya está resuelto en el repositorio con Bowtie
y BLAST+ locales. Acá solo se calcula el perfil de eficiencia.

## Instalación

```
python -m pip install biopython ViennaRNA numpy
```

El backend `exe` necesita además el `RNAplfold.exe` que instala si-Fi21 (ViennaRNA
2.1.5), por defecto en
`C:\Program Files (x86)\siFi21\ToCopy\RNAplfold\RNAplfold.exe`.
El backend `vienna` usa las ligaduras de Python de ViennaRNA 2.7.2 y no necesita la
instalación de si-Fi. **Los dos no dan lo mismo** —los parámetros de energía
cambiaron entre versiones— así que conviene reportar cuál se usó.

## Uso

```bash
# perfil de eficiencia, modo corregido (el que usamos para diseñar)
python run_sifi.py work/sifi_check/MP_MRFV_full.fasta --salida work/sifi_check/salida

# reproducir lo que daría el original, con su mismo RNAplfold
python run_sifi.py mi_gen.fasta --modo fiel --backend exe

# buscar si alguna configuración reproduce conteos declarados
python barrido.py work/sifi_check/MP_MRFV_full.fasta=114 \
                  work/sifi_check/CP_MRFV_full.fasta=35

# verificaciones
python test_sifi.py
```

`run_sifi.py` imprime el resumen con el desglose por filtro y la región de 200 nt
con mayor densidad de eficientes, y con `--salida` escribe un TSV con una fila por
ventana y todos los términos del veredicto, más un `resumen.json`.

Con `python -I` también funciona: los scripts agregan su propio directorio al path.

## Archivos

| Archivo | Qué es |
|---|---|
| `sifi_energy.py` | ΔG de hibridación por vecinos más cercanos. Tablas tomadas de Biopython, con la equivalencia verificada contra el fuente original. |
| `sifi_core.py` | El criterio de eficiencia, los dos modos, los dos backends de accesibilidad, y la búsqueda de región más densa. |
| `run_sifi.py` | Línea de comandos. |
| `barrido.py` | Barre configuraciones y busca cuáles reproducen conteos declarados. Vectorizado. |
| `offtarget_21nt.py` | Tamizaje de off-targets por siRNA, por coincidencia exacta con Aho-Corasick. No necesita BLAST. El tamaño va por `--size`, 21 por defecto. |
| `cruce.py` | Cruza el perfil de eficiencia con el de off-targets y compara regiones. |
| `ranking.py` | El ranking de candidatos y el barrido de pesos (`ranking`), y el percentil de la región elegida con sus dos nulos (`nulo`). Consume los mismos TSV que `cruce.py`. Trae además `region_recomendada()`, el único punto donde el primer puesto del orden se vuelve una región recomendada: llama a la compuerta de alertas de D48 y frena una región con una fila en «pendiente» (D69). El umbral es `UMBRAL_COMPUERTA`, `perfecto_21` por defecto, movible con `--umbral-compuerta`. |
| `azar_kmer.py` | Observado contra esperado por k, bajo tres nulos: uniforme, por composición y por barajado de la referencia. |
| `test_sifi.py` | Verificaciones, incluida la equivalencia de tablas y la coherencia entre el motor y el barrido. |
| `test_ranking.py` | Verificaciones del ranking: propiedades del criterio, más anclas contra los conteos ya publicados en `sifi21_reproduccion.md` §2, §3 y §4. |
| `CAMBIOS.md` | Qué se cambió respecto del original y por qué. |

## Tamizaje de off-targets

`offtarget_21nt.py` busca coincidencias **exactas** de cada ventana de 21 nt contra
referencias locales, en las dos hebras, en una sola pasada por base. Criterios:
bloque contiguo perfecto de ≥19 nt, 21/21 perfecto y, con `--mm1`, 21 nt con
exactamente un desajuste.

No usa BLAST a propósito: para bloques perfectos la coincidencia exacta es la
respuesta correcta y no una heurística. Verificado contra la corrida con BLAST+ de
W5: los criterios de bloque perfecto coinciden en las 20 celdas. El de un desajuste
**no** coincide, y el exacto encuentra más, porque `blastn-short` con `word_size 11`
no puede sembrar un 21-mero cuyo desajuste cae en la posición 11.

```bash
# bajar referencias a work/offtarget_db/ (publicas, del NCBI) y tamizar
python offtarget_21nt.py --consulta work/sifi_check/*_full.fasta \
    --db work/offtarget_db/*.fna.gz --salida work/sifi_check/offtarget_full

# cruzar con la eficiencia; el genoma del propio blanco va como on-target
python cruce.py --gen BicC_Dm --region 264 563 \
    --ontarget GCA_975739785.1_ihDalMaid1.1_genomic \
    --dir work/sifi_check --offtarget work/sifi_check/offtarget_full
```

Dependencia extra: `pyahocorasick`.

### Un directorio de trabajo por panel, y cuál es cuál (D83)

Un tamizado no se identifica por el gen ni por *k*: se identifica por el **panel**. El
mismo comando con una referencia de más da números distintos y plausibles, así que un
directorio reconstruido con otro panel no se nota como «otro panel» sino como una cifra
publicada que cambió sola. Por eso cada panel tiene su directorio, y acá está cuál es cuál.
`work/` no se versiona, así que esta tabla es el único registro de qué tiene que haber en
cada máquina.

| Directorio | Panel | Quién lo publica | Lo leen |
| --- | --- | --- | --- |
| `work/sifi_check/offtarget_full/` | las cinco de RefSeq de `work/offtarget_db/` **más el genoma del vector**, sin humano | `research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md` §4 | las anclas §2, §3 y §4 de `test_ranking.py`, `ranking.py ranking`, `cruce.py`, `informe_html.py` |
| `work/sifi_check/offtarget_panel_nuevo/`, `offtarget_22nt/` | *Macrosteles* y humano, aparte | `research/ola3/C6_panel_y_largo/REPORT.md` §9 | `panel_y_k.py` |
| `work/sifi_v2/offtarget_k21/` + `offtarget_dm_k21/` | las cinco **más humano**, con el vector en el segundo archivo | `research/ola3/C7_ranking_v2/REPORT.md` §2 y §9 | `ranking_v2.py`, el ancla C de `research/ola6/O3_quimera_bicc_vatpase_b/scripts/00_anclas.py` |

El de `sifi_check` se reconstruye **con este comando y no otro**, que es el de `§4` y el
que reproduce el `md5` de más abajo; el `*_full.fasta` del glob son los cuatro genes de
EPILAB y nada más, y va **sin** `--mm1` (el de un desajuste vive en
`work/sifi_check/offtarget_mm1_<gen>/`):

```bash
python tools/sifi21_port/offtarget_21nt.py \
    --consulta work/sifi_check/MP_MRFV_full.fasta work/sifi_check/CP_MRFV_full.fasta \
               work/sifi_check/BicC_Dm_full.fasta work/sifi_check/ATPaseD_Dm_full.fasta \
    --db work/offtarget_db/*.fna.gz --salida work/sifi_check/offtarget_full
```

Los cuatro `work/sifi_check/offtarget_mm1_<gen>/`, que son el **mismo panel** con el
criterio de un desajuste y van uno por gen —los necesita `ranking.py ranking --mm1`, y por
él `research/ola2/W7_ranking/ranking.json`—, se construyen así:

```bash
for g in MP_MRFV CP_MRFV BicC_Dm ATPaseD_Dm; do
  python tools/sifi21_port/offtarget_21nt.py --mm1 \
      --consulta work/sifi_check/${g}_full.fasta \
      --db work/offtarget_db/*.fna.gz --salida work/sifi_check/offtarget_mm1_${g}
done
```

Y el de `sifi_v2`, con los comandos de `C7` §9. `test_ranking.py` comprueba el panel del
primero contra la lista de accesiones de `§4` **antes** de leer ninguna ancla, y si no
coincide dice qué referencia sobra o falta en vez de dejar que el número cambie solo.

> **El tamaño de ventana está parametrizado y la equivalencia en 21 está
> verificada.** `--size` cambia *k* y `--min-block` el bloque; con los valores por
> defecto la salida es **idéntica byte a byte** a la de antes de parametrizar
> —`md5sum` `a3229e733e4dc70c308c901583b4e4c3` sobre `offtarget_por_sirna.tsv`, los
> cuatro genes contra las seis referencias—, que es lo que permite seguir citando
> esos conteos. Los nombres de las columnas no cambian con `--size`: el *k* efectivo
> va en `offtarget_resumen.json`.

## Ranking y cuenta de azar

```bash
# el ranking, el barrido de pesos sobre el simplex y las regiones alternativas
python ranking.py ranking --perfil work/sifi_check/salida \
    --offtarget work/sifi_check/offtarget_full/offtarget_por_sirna.tsv \
    --mm1 "work/sifi_check/offtarget_mm1_{gen}/offtarget_por_sirna.tsv" \
    --muestras 2000 --json research/ola2/W7_ranking/ranking.json

# el percentil de la region elegida, los dos nulos y la correlacion con el pipeline
python ranking.py nulo --perfil work/sifi_check/salida --reps 2000 --correlacion

# observado contra esperado por azar, por tamano de ventana
python azar_kmer.py --consulta work/sifi_check/*_full.fasta \
    --db "work/offtarget_db/*.fna.gz" --k 15 16 17 18 19 20 21 \
    --salida research/ola2/W7_ranking/azar_por_k.json

python test_ranking.py
```

Los resultados y su justificación están en `research/ola2/W7_ranking/`.

## Advertencias

- El fuente de GitHub no es idéntico al binario de 2017 de SourceForge
  (`Resources/ui_sifi2015.py`: 23.791 bytes instalado contra 23.787 en el clon), así
  que el modo «fiel» es fiel al fuente, no necesariamente al binario. `[?]`
- El modo fiel **puede contar como eficientes siRNA que fallan la termodinámica**:
  es la rama del original, no un error del port. Está en `CAMBIOS.md` C1.
- La mezcla de tablas de ADN y ARN del original existe pero no se alcanza en este
  uso: medido, cero consultas. `CAMBIOS.md` C3.

## Ranking v2

`ranking_v2.py` reusa el motor de `ranking.py` con seis candidatos (los cuatro de EPILAB más `eth` y `burs-alpha`),
humano en el panel y 21 y 22 nt. Reproduce primero las anclas de W7 y aborta si no coinciden. Informe en
`research/ola3/C7_ranking_v2/`.
