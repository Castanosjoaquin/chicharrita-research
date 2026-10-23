# Notas de la linea M1 (ola 4)

Esta linea se hizo en dos sesiones y en dos maquinas distintas. La primera dejo la regla
implementada y verificada y declaro la matriz como pendiente por falta de insumos; la segunda,
del 2026-10-23, corrio la matriz. `00_meta/` se actualizo directamente en las dos: D51 y **D52**
en `DECISIONS.md`, cinco entradas en `CAMINOS_PROBADOS.md` —dos de ellas con su actualizacion— y
dos bloques en `PREGUNTAS_ABIERTAS.md`, uno de los cuales **cierra** un pendiente anterior. Aca
queda lo que es propio del bloque: versiones, que se verifico, confidencialidad y que sirve de lo
que salio.

---

## Donde corrio, y por que eso importa

**Segunda sesion (2026-10-23), la que midio.** Windows 11, Python 3.13.15. Con `work/`, con los
cuatro FASTA de EPILAB, con las seis bases de `work/offtarget_db/`, con Biopython 1.88 y
ViennaRNA 2.7.2, y —esto es lo que desbloqueo la linea— con **si-Fi2015 instalado**, que trae en
`%LOCALAPPDATA%\siFi2015\` su propio `RNAplfold.exe` 2.1.5 y su propio `bowtie.exe` 0.11.3 con
`bowtie-build.exe`. Son los binarios con los que corrio el programa original.

**Primera sesion (2026-10-22), la que implemento la regla.** Python 3.10.11, solo biblioteca
estandar, sin `work/`, sin Bowtie, sin ViennaRNA, sin BLAST+ y sin si-Fi21. Esa sesion declaro los
cuatro insumos como ausentes y escribio los comandos para otra maquina.

La leccion operativa, que vale mas que la anecdota: **el insumo que se declaro ausente estaba
dentro del programa cuya salida queriamos reproducir**. Antes de declarar una herramienta
faltante conviene mirar en el directorio del instalador. Quedo registrado en
`CAMINOS_PROBADOS.md` como actualizacion del descarte correspondiente, porque un descarte que
despues resulto evitable es informacion y no se borra.

La restriccion de la primera sesion —solo biblioteca estandar en `conteo_por_acierto.py`— se
conserva a proposito, y rindio: las 44 verificaciones y el conteo mismo corren en la maquina de
cualquier integrante sin instalar nada. El driver `correr_matriz.py` si necesita Bowtie y el port,
y lo dice al fallar en vez de aproximar.

## Que se verifico, y en que orden

Primero el ancla, porque sin ella la matriz no se puede leer: `run_sifi.py --modo fiel --backend
exe` sobre los cuatro genes devuelve **133, 32, 212 y 42** eficientes `[M]`, los cuatro numeros
verificados contra el programa original. Cada celda de la matriz es un conteo sobre ese conjunto
de ventanas, asi que si el ancla se mueve, la matriz entera cambia de significado.

Despues la compuerta: `--exigir-identidad epilab4`, que falla con codigo 1 si contra el gen mismo
alguna ventana eficiente queda sin acierto en la hebra `+`. La corrida completa la pasa.

Y las pruebas: `python scripts/test_conteo_por_acierto.py` -> **44 de 44**, salida cruda en
`resultados/verificacion_regla.txt`.

Hay tres concordancias independientes que no se buscaron y sirven como verificacion cruzada
`[M]`:

1. **Los 2.504 aciertos de `BicC_Dm` contra `epilab4`** se reproducen exactos, y eran el numero
   que la ola 3 habia medido en otra maquina con otro Bowtie.
2. **Los 2.353 y los 450** del blanco principal en el transcriptoma publico de *D. maidis* se
   reproducen exactos bajando los dos contigs por numero de acceso.
3. **El backend `vienna` da 142, 39, 223 y 35**, que son los mismos cuatro numeros que
   `sifi21INTA` reporta con la tabla `RNA_NN3`. El port queda verificado en un segundo punto del
   eje del motor, no solo en el de RNAplfold 2.1.5.

## Un error de medicion que se cometio y se corrigio

Vale anotarlo porque es la clase de error que esta linea vino a evitar. En la primera corrida de
la matriz, cuatro celdas de la tabla con un desajuste permitido aparecieron como **cero**. No
eran cero: Bowtie habia abortado y un intento anterior habia dejado el archivo de salida vacio,
asi que el paso de conteo lo leyo como «corrio y no encontro nada». Un nulo medido y una celda
que no corrio son cosas distintas y el reporte se apoya en la diferencia.

La correccion no fue borrar los archivos a mano: `correr_matriz.py` ahora **borra la salida cuando
Bowtie aborta**, de modo que un archivo vacio escrito por el driver significa siempre que Bowtie
corrio bien y no encontro nada. Las celdas fallidas quedan en `resultados/procedencia.json` bajo
`celdas_fallidas` y **ausentes** de la tabla.

## Confidencialidad

Esta sesion si toco secuencias de EPILAB, asi que las dos reglas estuvieron en juego de verdad y
no en abstracto.

**Nada salio de la maquina.** El port, Bowtie, `bowtie-build` y el conteo corren locales. Lo unico
que viajo a la red fueron **numeros de acceso** a la API de NCBI, para bajar los sesenta y cinco
registros publicos de MRFV y los dos contigs de la ensambladura TSA `GITV01`. Son identificadores
publicos; ninguna secuencia nuestra fue parte de ninguna consulta, y bajar un registro publico es
lo contrario de subir uno privado.

**Todo lo derivado quedo en `work/`.** Los TSV por ventana del port, los FASTA de ventanas de
21 nt, los indices de Bowtie y las salidas de aciertos viven en `work/M1/` y ninguno se versiona.
Lo que entra a `research/` son **solo conteos y procedencia**: `matriz.md`, `matriz_mm1.md`,
`matriz_vienna.md`, `orientacion.*`, `procedencia.json` y el log de las pruebas.

Auditoria del bloque con `tools/verificacion/sin_secuencias.py`, que es la herramienta de M9 y
mira rachas de 21 nt y columnas de k-meros solapados: ver la corrida en el commit. Los unicos
hallazgos esperables son los fixtures escritos a mano de `test_conteo_por_acierto.py`, que no
tienen relacion con el corpus, y el gen de `demo_sintetico.py`, que se genera al vuelo con
`random.seed(7)` y no se escribe.

Un cuidado que conviene dejar dicho para quien siga: el FASTA de ventanas que escribe el
subcomando `ventanas` es, literalmente, el gen entero en 21-meros solapados de a 1 nt. Es la
forma exacta del incidente de C9. Por eso va a `work/` y por eso el driver no tiene ninguna
opcion para escribirlo en otro lado.

## Que sirve de lo que salio, y que no

**Sirve como medicion del caso real:** `resultados/matriz.md` y las tres tablas hermanas, y las
secciones 4 a 8 del REPORT. En particular los tres mecanismos del fuente, que ahora tienen
instancia real y no solo sintetica: la ventana que no pega (12 de 212 en `BicC_Dm` contra el
contig publico), la que pega solo en la hebra menos (**40 de 42** en `ATPaseD_Dm` contra el
genoma, y la fila cae a 0) y la que pega dos veces (3 ventanas en `BicC_Dm` contra el gen mismo
con un desajuste permitido).

**Sirve como descarte:** el control de orientacion, L1 190 contra 44.

**No sirve como explicacion del desajuste:** nada, todavia. Un gen de cuatro cierra con un error
de uno y tres no cierran. La combinacion mejor por gen da L1 25 y **no se reporta como
resultado**: mezcla dos motores entre genes, asi que no es una corrida.

**No sirve como medicion del caso real:** `resultados/ejemplo_formato_sintetico.md`. Se conserva
porque aisla cada mecanismo con un solo cambio controlado, que es util para leer el codigo, pero
dejo de ser la evidencia principal.

## Para quien siga la linea

El trabajo que queda esta en la seccion 13 del REPORT y lo que mas rinde no es computo nuestro:
son las tres preguntas de la seccion 12, el lunes. De lo que si es computo, dos cosas necesitan la
maquina de la ola 3 —`-v 1` contra las bases grandes, con un Bowtie de 64 bits, y los puntos
intermedios del motor— y una necesita `work/C2/`, que es la lista de los cinco contigs que faltan
de la ensambladura TSA.
