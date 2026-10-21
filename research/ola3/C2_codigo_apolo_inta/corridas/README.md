# Corridas — comandos, entradas, salidas y versiones

Todo corrió el 2026-10-20 en esta máquina (Darwin 27.0.0 arm64, 10 núcleos), en un entorno conda
propio llamado `c2sifi`, creado para esta investigación. **Ninguna secuencia de EPILAB salió de la
máquina**: RNAplfold y Bowtie son locales, y lo único que viajó por la red fueron las descargas de
los repositorios desde GitHub y las consultas de metadatos a su API pública.

Los archivos por ventana con las secuencias de 21 nt **no se copian acá**: quedan en
`work/C2/runs/`, fuera del control de versiones, igual que hizo W5. En esta carpeta están los logs
y los resúmenes, que no contienen secuencias (verificado con `grep -c "[ACGT]\{21,\}"`, que da 0 en
los cuatro logs).

## Versiones

| Componente | Versión | Cómo se obtuvo |
|---|---|---|
| Python | 3.11.17 | `python -c "import sys; print(sys.version)"` |
| ViennaRNA / RNAplfold | **2.7.2** | `RNAplfold --version` |
| Bowtie | **1.3.1** (`bowtie-align-s`, 64-bit) | `bowtie --version` |
| bowtie-build | 1.3.1 | `bowtie-build --version` |
| Biopython | **1.81** | `python -c "import Bio; print(Bio.__version__)"` |
| plotly | 7.1.0 | idem |
| pandas | 3.0.6 | idem |
| numpy | 2.4.6 | idem |
| pypdf | 6.21.1 | idem, para extraer el PDF de endpoints |
| bcbio-gff | instalado por conda | requerido por `generalFunctions.py` |

**Por qué Biopython 1.81 y no la última.** El entorno se creó con Biopython 1.88 y sifi21INTA
aborta: `freeEnergy.py:384` llama a `Bio.SeqUtils.GC`, eliminado en Biopython 1.82. Con 1.81 la
función existe (emite `BiopythonDeprecationWarning`, visible en los logs) y el paquete corre. Es una
restricción real de la librería, no una elección nuestra.

**Lo que no se pudo usar: RNAplfold 2.1.5.** El W5 original comparó las dos versiones de ViennaRNA
porque si-Fi21 trae la 2.1.5 en su instalador de Windows. Acá sólo hay 2.7.2, así que todas las
comparaciones con nuestro port se hicieron contra el backend `vienna` (2.7.2), que es el que
corresponde.

---

## Corrida 1 — sifi21INTA con sus valores por defecto

**Qué responde:** Q2, la pregunta central.

```bash
cd work/C2
python scripts/run_inta.py RNA_NN4 nn4          # RNA_NN4 es el default del paquete
```

`scripts/run_inta.py` es un driver propio de 40 líneas que **no modifica el paquete**: lo importa,
instancia `SifiPipeline(bowtieDB=..., queryFile=..., outputDir=..., mode=0)` por cada gen con todos
los demás parámetros en su valor por defecto, llama a `runPipeline()` y vuelca `getResultSummary()`.
Lo único que reemplaza es `builtins.input`, porque `selectMainTargets` abre un prompt interactivo;
el driver responde «1», que es el único blanco que existe con esta base.

**Entrada:** los cuatro FASTA completos de EPILAB, copiados de `work/W5/fasta/` a `work/C2/runs/`
(md5 de las copias: `2ea7643b1f094159937ec6dcc2301a1e` MP, `26bab87e62424da9ea526ef63f0503e4` CP,
`3b9d24326705e7524e397f128d67571d` BicC, `f98df5205fa72db1021862f20d1471b5` ATPaseD). Base de
Bowtie: `bowtie-build` sobre `epilab_full.fasta`, los cuatro genes juntos, igual que hizo W5 con el
programa original.

**Salida obtenida** (`01_sifi21INTA_defaults.log`, `01_resumen_defaults.json`):

| Gen | Ventanas | Hits de Bowtie | Eficientes | Eficientes sin off-targets | Declarado en la planilla |
|---|---|---|---|---|---|
| `MP_MRFV_full` | 1.243 | 1.243 | **138** | 138 | 114 |
| `CP_MRFV_full` | 508 | 508 | **40** | 40 | 35 |
| `BicC_Dm_full` | 2.500 | 2.504 | **218** | 218 | 199 |
| `ATPaseD_Dm_full` | 471 | 471 | **35** | 35 | 33 |

**Terminó bien.** Código de salida 0, las cuatro tablas de resumen impresas, cuatro JSON y cuatro
figuras HTML escritas, ninguna salida vacía.

---

## Corrida 2 — sifi21INTA forzando la tabla de energía del original

**Qué responde:** Q1, aislar el efecto del único cambio químico.

```bash
python scripts/run_inta.py RNA_NN3 nn3
```

El driver envuelve `freeEnergy.calculateFreeEnergy` para pasarle `nn_table=freeEnergy.RNA_NN3`,
que es el default del si-Fi original. **No se tocó ningún archivo del paquete.**

**Salida** (`02_sifi21INTA_RNA_NN3.log`, `02_resumen_RNA_NN3.json`): **142, 39, 223 y 35**, contra
138, 40, 218 y 35 de la corrida 1. Terminó bien.

---

## Corrida 3 — nuestro port en modo fiel, para comparar ventana por ventana

```bash
python tools/sifi21_port/run_sifi.py work/C2/runs/{MP_MRFV,CP_MRFV,BicC_Dm,ATPaseD_Dm}_full.fasta \
       --modo fiel --backend vienna --salida work/C2/runs/port_fiel
```

**Salida** (`03_port_fiel_vienna.log`): 142, 39, 223 y 35. **Los mismos cuatro números que la
corrida 2.**

La comparación fina está en `03_comparacion_port_vs_inta.json`: para los cuatro genes, las 4.722
ventanas coinciden en **los cinco términos** del veredicto —selección de hebra, estabilidad de
extremos, accesibilidad, valor de accesibilidad (diferencia < 1e-6) y veredicto final—, con **cero**
diferencias. Terminó bien.

---

## Corrida 4 — dependencia de la base de datos

**Qué responde:** si la base explica los conteos de la planilla.

```bash
python scripts/run_db.py
```

Ocho combinaciones de gen y base, por cada tabla de energía. Bases: `epilab4` (los cuatro genes),
`mrfv_all` (los 71 registros públicos de MRFV que bajó W5) y `tsa_gitv01` (el transcriptoma TSA
GITV01 de *Dalbulus maidis*, 56.117 contigs, indexado acá con `bowtie-build --threads 8`). El driver
reemplaza la selección interactiva por «el blanco con más hits», que es el orden en que el programa
original presenta la lista.

**Salida** (`04_dependencia_base_datos.log`, `04_resumen_base_datos.json`), con la tabla por defecto:

| Gen | Base | Blancos | Hits | Eficientes | Eficientes sin off-targets |
|---|---|---|---|---|---|
| `MP_MRFV_full` | epilab4 | 1 | 1.243 | 138 | 138 |
| `MP_MRFV_full` | mrfv_all | 4 | 2.841 | **138** | **0** |
| `CP_MRFV_full` | epilab4 | 1 | 508 | 40 | 40 |
| `CP_MRFV_full` | mrfv_all | 65 | 11.019 | **40** | **0** |
| `BicC_Dm_full` | epilab4 | 1 | 2.504 | 218 | 218 |
| `BicC_Dm_full` | tsa_gitv01 | 6 | 2.430 | **218** | **214** |
| `ATPaseD_Dm_full` | epilab4 | 1 | 471 | 35 | 35 |
| `ATPaseD_Dm_full` | tsa_gitv01 | 2 | 736 | **35** | **12** |

Terminó bien. Lectura: en sifi21INTA el conteo de eficientes **no se mueve** con la base; el que se
mueve es el de eficientes sin off-targets, y ninguno de sus valores es 114, 35, 199 ni 33.

---

## Corrida 5 — barrido de 22.176 configuraciones

**Qué responde:** Q2, cuál de las diferencias acerca los conteos a la planilla.

```bash
python scripts/barrido_inta.py
```

El barrido calcula los términos **con las funciones del propio paquete** —`Sirna.freeEnergy`,
`Sirna.freeEnergyDanglingEnds` y `SifiPipeline.runRnaplfold`, una corrida de RNAplfold por gen y por
temperatura— y evalúa el veredicto vectorizado con numpy. Esa evaluación vectorizada **se verifica
antes de usarla**: reproduce exactamente, ventana por ventana, la salida de las corridas 1 y 2 en
los ocho casos (cuatro genes por dos tablas), con cero diferencias; el script aborta con un `assert`
si eso no se cumple. La verificación está adentro de `05_barrido_22176_configs.json`.

Ejes barridos: tabla de energía (`RNA_NN4`, `RNA_NN3`) × temperatura de RNAplfold (22, 25, 37 °C) ×
ventana de accesibilidad u (1 a 21) × umbral de estabilidad de extremos (11 valores de 0 a 3,0) ×
umbral de accesibilidad (8 valores de 0,01 a 0,3) × regla terminal (sí, no).

**Salida:** ninguna de las 22.176 configuraciones reproduce los cuatro conteos declarados. El mejor
error acumulado es **4** sobre 381 siRNA declarados, con `RNA_NN3`, 22 °C, u=8, accesibilidad 0,1 y
**umbral de extremos 1,75** en vez de 1,0: da 117, **35**, **199** y 32 —dos de cuatro exactos—.
Le sigue `RNA_NN4` a 25 °C con umbral 2,0, con error 6. Terminó bien.

Cortes por temperatura y umbral (`barrido_cortes.json` en `work/C2/runs/`, mismo script con los ejes
recortados), con u=8, accesibilidad 0,1 y regla terminal activada:

| Tabla | T de RNAplfold | Umbral de extremos | MP | CP | BicC | ATPaseD | Error |
|---|---|---|---|---|---|---|---|
| RNA_NN4 | 22 | 1,00 (default) | 138 | 40 | 218 | 35 | 50 |
| RNA_NN4 | 22 | 1,75 | 115 | 34 | 194 | 28 | 12 |
| RNA_NN4 | 25 | 2,00 | 113 | 36 | 201 | 31 | 6 |
| RNA_NN3 | 22 | 1,00 | 142 | 39 | 223 | 35 | 58 |
| RNA_NN3 | 22 | 1,75 | **117** | **35** | **199** | 32 | **4** |
| RNA_NN3 | 25 | 2,00 | 117 | 37 | 202 | 32 | 9 |
| RNA_NN3 | 37 | 1,00 | 198 | 64 | 325 | 74 | 280 |

---

## Corrida 6 — sensibilidad a minúsculas

**Qué responde:** una crítica que se podía medir en dos minutos.

```bash
cd work/C2
python scripts/minusculas.py     # se corrio como heredoc; el archivo tiene el contenido exacto
```

**Entrada:** `MP_MRFV_full.fasta` y una copia con la secuencia pasada a minúsculas.

**Salida** (`07_resumen_minusculas.json`): mayúsculas, 1.243 ventanas y **138 eficientes**;
minúsculas, 1.243 ventanas y **0 eficientes**. Bowtie alinea igual las 1.243 ventanas (es
insensible a mayúsculas), así que la corrida parece exitosa y el resultado es cero sin un solo
aviso. Terminó bien, en el sentido de que no falló: ése es justamente el problema.

---

## Corrida 7 — curva de eficiencia de Apolo Rocket: HTML contra base

**Qué responde:** Q3, qué guarda y qué dibuja la plataforma.

De `exampleData/example.efficiency.figure.html` (3,6 MB) se extrajo **sólo** el arreglo del trace
«Efficient siRNAs» con una expresión regular, sin leer el archivo entero ni abrirlo en un navegador,
y se comparó con el `INT[]` de la tabla `efficiency` del volcado con resultados.

**Salida** (`08_curva_eficiencia_html_vs_volcado.json`): idénticos valor por valor —1.635 enteros,
máximo 14, suma 3.380— para la consulta 6 del volcado (*Drosophila melanogaster* FBtr0070438,
`method = 'sifi21'`). La suma dividida por 20 da 169 exacto, que es el número de siRNA eficientes y
a la vez la prueba de que cada uno cubre 20 posiciones y no 21.

---

## Lo que no se corrió

- **Apolo Rocket.** Necesita PostgreSQL con el esquema cargado, el árbol de referencias indexadas en
  disco y una capa HTTP que no está publicada. Se leyó el código, el PDF y los dos volcados.
- **si-Fi21 original.** Ya está corrido y verificado en W5 (`sifi21_reproduccion.md` §0); acá se usó
  nuestro port como sustituto verificado, y se dice cada vez que se lo usa.
- **RNAplfold 2.1.5**, el que trae si-Fi: no está en esta máquina.
- **Los forks** `rj-price/siFi-2.0` y `dakilaledesma/siFi21-`: se leyeron, no se corrieron.
