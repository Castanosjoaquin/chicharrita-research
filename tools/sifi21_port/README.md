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
| `offtarget_21nt.py` | Tamizaje de off-targets de 21 nt por siRNA, por coincidencia exacta con Aho-Corasick. No necesita BLAST. |
| `cruce.py` | Cruza el perfil de eficiencia con el de off-targets y compara regiones. |
| `test_sifi.py` | Verificaciones, incluida la equivalencia de tablas y la coherencia entre el motor y el barrido. |
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

## Advertencias

- El fuente de GitHub no es idéntico al binario de 2017 de SourceForge
  (`Resources/ui_sifi2015.py`: 23.791 bytes instalado contra 23.787 en el clon), así
  que el modo «fiel» es fiel al fuente, no necesariamente al binario. `[?]`
- El modo fiel **puede contar como eficientes siRNA que fallan la termodinámica**:
  es la rama del original, no un error del port. Está en `CAMBIOS.md` C1.
- La mezcla de tablas de ADN y ARN del original existe pero no se alcanza en este
  uso: medido, cero consultas. `CAMBIOS.md` C3.
