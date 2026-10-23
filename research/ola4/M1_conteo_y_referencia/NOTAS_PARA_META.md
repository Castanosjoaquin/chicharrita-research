# Notas de la linea M1 (ola 4)

Esta linea la corrio la sesion principal, asi que `00_meta/` se actualizo directamente: D51 en
`DECISIONS.md`, dos entradas en `CAMINOS_PROBADOS.md` y tres en `PREGUNTAS_ABIERTAS.md`. Aca
queda lo que es propio del bloque: versiones, que se verifico, confidencialidad y que sirve de lo
que salio.

---

## Donde corrio, y por que eso limita el resultado

Windows 11, **Python 3.10.11, solo biblioteca estandar**. Sin ViennaRNA, sin Biopython, sin
Bowtie, sin BLAST+, sin si-Fi21 instalado y **sin `work/`**, que esta en `.gitignore`. La maquina
de esta sesion no es la que corrio la ola 3: ese registro declara Darwin arm64 con el entorno
conda `c2sifi`, Bowtie 1.3.1 y ViennaRNA 2.7.2
(`research/ola3/C2_codigo_apolo_inta/corridas/README.md`).

Consecuencia directa, y es la mitad de esta linea: la matriz de bases **no corrio**. El REPORT lo
declara como pendiente con la secuencia exacta de comandos, no como resultado nulo. La diferencia
no es retorica: un nulo habria sido correr las celdas y que ninguna reproduzca los cuatro
numeros.

Por eso el script se escribio con una restriccion que no estaba en el plan: **solo biblioteca
estandar**. No importa numpy, ni Biopython, ni `pyahocorasick`, y no necesita Bowtie. Asi las
verificaciones corren en la maquina de cualquier integrante y la unica cosa que hace falta pedir
prestada es el TSV por ventana.

## Que se verifico antes de medir nada

`python scripts/test_conteo_por_acierto.py` -> **44 de 44**, salida cruda en
`resultados/verificacion_regla.txt`. Tres anclas, en orden de importancia:

1. **Los tres casos que definen la regla**, construidos a mano porque contra el gen mismo son
   imposibles: la ventana eficiente que no pega, la que pega solo en la hebra menos y la que pega
   dos veces en la misma referencia.
2. **Los dos formatos de Bowtie** —nativo y SAM— dan el mismo conjunto de aciertos, con la
   bandera 16 leida como hebra menos y la posicion de SAM normalizada a 0-based.
3. **La enumeracion local contra el gen mismo** deja cero ventanas eficientes sin acierto en `+`,
   que es el invariante correcto de la celda de verificacion (el criterio del plan, que pedia
   igualdad entre el conteo por ventana y el conteo por acierto, es falso cuando hay 21-meros
   repetidos, y en `BicC_Dm` los hay: 2.504 aciertos para 2.500 ventanas `[M]`).

El script aborta con codigo 1 si `--exigir-identidad` falla.

**Una cuarta ancla, agregada despues de revisar el script:** seis formas de fallar en silencio
que ahora abortan o devuelven `None` en vez de dar un numero plausible y equivocado —posicion
repetida en el TSV, ventana sin secuencia, codigo IUPAC ambiguo, N en la ventana o en la
referencia, nombre de lectura con dos grupos de digitos (`w12_2` le asignaba el acierto a la
ventana 2) y dos referencias que nombran al mismo gen—. Esa clase de error es la que importa
cuando el numero sale impreso en un reporte.

## Por que no hay `sources.json`

Las lineas de las olas 2 y 3 lo llevan porque leyeron fuentes externas y hay que declarar el
nivel de lectura de cada una. M1 **no leyo ninguna fuente nueva**: trabaja sobre el fuente del
si-Fi21 original ya leido y citado por linea en C2, sobre salidas nuestras ya medidas y sobre la
carta del investigador. Todas las referencias del REPORT son rutas del repositorio o archivos del
corpus ya inventariados. Si la matriz, al correr, obliga a mirar un registro publico nuevo
—por ejemplo el aislamiento de MRFV que la seccion 5 propone pedir—, ese archivo se agrega
entonces.

## Confidencialidad

No se toco ninguna secuencia de EPILAB en esta sesion, por la razon trivial de que no estan en
esta maquina. Para cuando la matriz corra, las dos reglas que el script respeta por diseno: el
TSV por ventana y el FASTA de ventanas que escribe `ventanas` **contienen** secuencias de EPILAB
y van a `work/`, nunca a `research/`; y la enumeracion de aciertos es local, con Bowtie o con el
camino propio, asi que nada sale de la maquina.

Lo unico que se versiona de esta linea son scripts, el log de las verificaciones y una tabla
sobre secuencias inventadas con semilla fija. Auditoria del bloque con
`grep -rno -E "[ACGT]{21,}"`: dos coincidencias, las dos en
`scripts/test_conteo_por_acierto.py` lineas 178 y 254, y las dos son los fixtures escritos a mano
—`AAACCCTT...`, con tramos repetidos a proposito— que ninguna relacion tienen con el corpus. La
tabla de `resultados/` no contiene secuencias: solo conteos. El gen de `demo_sintetico.py` se
genera al vuelo con `random.seed(7)` y no se escribe en el repositorio.

## Que sirve de lo que salio, y que no

**Sirve:** `scripts/conteo_por_acierto.py` como implementacion de la regla del original, con sus
tres subcomandos, y la lectura de la seccion 5 del REPORT, que acota la hipotesis con numeros que
la ola 3 ya habia medido y mueve el pedido del lunes de «contra que base» a «contra que
registro».

**No sirve como medicion del caso real:** `resultados/ejemplo_formato_sintetico.md`. Es una
demostracion del mecanismo sobre secuencias inventadas. Fija el formato de la tabla y muestra que
la regla mueve el conteo en los dos sentidos; no dice nada sobre `MP_MRFV`, `CP_MRFV`, `BicC_Dm`
ni `ATPaseD_Dm`.

## Para quien siga la linea

El trabajo que queda es correr los pasos 1 a 5 de la seccion 4 del REPORT en la maquina que tiene
el corpus. No necesita ninguna decision del usuario y no toca el script. El unico cuidado: el
control de orientacion obliga a volver a correr el motor de eficiencia sobre el gen invertido,
porque el complemento reverso cambia las ventanas y no solo los aciertos.
