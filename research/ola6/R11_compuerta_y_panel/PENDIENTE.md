# R11 — lo que queda pendiente, con el comando exacto y el insumo que falta

> **ESTADO AL 2026-10-27 (issue #37, bloque `R12`).** Este archivo se escribio desde una
> maquina sin `work/`, y las corridas que pide **se hicieron** en la maquina de Joaquin, donde
> los insumos estan. El censo pasa **7 de 8**; la matriz de `V-ATPase B` y las dos junturas
> **estan en el inventario** (`D88`); `ranking_v2.json` **es byte-reproducible** y reproduce el
> publicado. Lo que sigue pendiente ya no es insumo: son **cinco filas sin firmar** y una
> corrida que cuesta 71 dias (`D89`). El resultado completo esta en
> `research/ola6/R12_corridas_pendientes/REPORT.md`. Lo que sigue se deja como estaba, porque
> es el pedido tal como se escribio y vale para quien lo tome en otra maquina.

Esto es la contracara de `REPORT.md` §4. Las decisiones del issue **#35** estan tomadas
(`D77` y `D78`); lo que falta son corridas, y lo que falta para correrlas son insumos que
`work/` no versiona. Siguiendo la regla de `D71`, cada pendiente dice **en que maquina** se
verifico que falta.

Verificado en **la maquina de Luca**: Windows 11 (10.0.26300), Python 3.10.11 del sistema,
con `numpy`, `scipy` y `pandas`; **sin** `RNA` (ViennaRNA), `Bio` (Biopython),
`ahocorasick`, BLAST+ ni Bowtie. `work/` **no existe** —`ls work/` falla— y tampoco dentro
de WSL, donde hay `~/yhat/tools` y `~/yhat/data` pero no una copia del repositorio `[M]`.

**Precision del 2026-10-27 (entrada 61, issue #29):** lo de arriba vale para el Python de
**Windows**, que es el que se midio, y esta maquina tiene **dos** interpretes. En el
`python3` de **WSL** (3.12.3) el reparto es al reves: `RNA` (ViennaRNA 2.7.2) **si esta** y
`numpy` **no** `[M]`, asi que **ninguno de los dos corre el port entero solo**. `Bio`,
`ahocorasick`, BLAST+ y Bowtie faltan en los dos `[M]`. En WSL tambien hay `miniprot`
0.18-r281, fuera del `PATH`. El pedido de `work/` que sigue no cambia: sin esos archivos no
corre nada, en ninguno de los dos interpretes.

## Lo que hay que conseguir

Una copia de `work/` de la maquina donde se generaron los numeros publicados. En concreto,
y por orden de cuanto desbloquea:

1. `work/sifi_v2/` — `salida_k21`, `salida_k22`, `offtarget_k21`, `offtarget_k22`,
   `offtarget_dm_k21`, `offtarget_dm_k22`. Lo piden `ranking_v2.py`, las anclas de `M5` y,
   por ellas, `tabla_alertas.py`, `identidad.py` y `sensibilidad_reparto.py`. Sin esto no
   corre casi nada.
2. `work/W5/ref/` — los siete FASTA de referencia. Los pide todo tamizado nuevo, incluida
   la matriz de `V-ATPase B` que `D78` necesita.
3. `work/sifi_check/salida/` y `work/sifi_check/offtarget_full/` — los pide
   `ranking.py ranking` y `ranking.py nulo`. **Ojo con cual de los dos paneles trae**: el
   issue #33 tiene abierto que los dos juegos de anclas publicadas piden paneles distintos,
   y el archivo que esta en la maquina de Joaquin se dejo **sin la referencia humana**
   porque es el que hace pasar `test_ranking.py`. Pedir el archivo diciendo con que panel
   se construyo, o va a volver a pasar lo de la entrada 33.
4. `work/o3/` — lo pide `01_region_vatpase_b.py`.

Lo que **no** hay que hacer es regenerar esos insumos aca con otra version del motor: el
repositorio ya midio que el conteo de ventanas eficientes se mueve con la version de
ViennaRNA y con la tabla de vecinos (ver `research/ola4/M8_que_compara_el_conteo/`), asi
que un `work/` reconstruido con otro entorno no reproduce los numeros publicados y
convierte un pendiente de insumo en una discrepancia nueva.

## Parte 2 — correr cada generador de punta a punta

El criterio del issue es que la compuerta senale las regiones sin tamizar, no que alguien
las busque. Con `work/` en disco, en `cmd.exe`:

```
python research\ola6\R11_compuerta_y_panel\scripts\censo_generadores.py
```

Ese comando intenta los ocho generadores declarados y deja en
`resultados/censo_corridas.tsv` el codigo de salida y el insumo faltante de cada uno. Los
dos que ya corren hoy —`compuerta.py` y `umbral_compuerta.py`— no cuentan para el criterio:
iteran sobre las regiones que ya estan en el inventario y por construccion no pueden
levantar `RegionNoTamizada`.

Toda `RegionNoTamizada` que aparezca entra al inventario por `REGIONES` en
`research\ola4\M6_alertas\scripts\tabla_alertas.py`, como se hizo con `BicC_Dm` 2123-2422, y
**se vuelve a correr el generador** hasta que termine. Si alguna trae coincidencia perfecta
de 21 nt se dice con todas las letras y su fila queda **sin firmar**: firmar es del equipo
(`D48`, `D68`, `D73`).

Y se anota con que panel se corrio cada una. La entrada 36 lo dejo medido: con un archivo de
off-target distinto la cascada elige otra region, asi que **que region senala la compuerta
depende del insumo**.

## Parte 3 — `V-ATPase B` 517-816 al inventario

Decidido en `D78`. Son tres pasos y el primero es el que falta.

```
python research\ola4\M6_alertas\scripts\identidad.py
python research\ola4\M6_alertas\scripts\tabla_alertas.py
python research\ola4\M6_alertas\scripts\compuerta.py
```

Antes del primero hay que agregar la region a `REGIONES` en `tabla_alertas.py`:

```
("VATPaseB_Dm", (517, 816), "region candidata de O3 (D74), la unica admisible del gen", False),
```

y hacer que el tamizado cubra el gen, que hoy no esta entre los seis: `identidad.py` corre
los seis genes del panel contra las siete referencias, y `V-ATPase B` necesita su FASTA de
consulta —el CDS que `O2` recupero— y su matriz contra las mismas referencias. Esa matriz es
el insumo que no existe y que `R7` no invento a proposito.

La fila que salga va a tener los cuatro campos obligatorios de `D48` y su `decision_usuario`
en «pendiente», que es correcto: la firma la escribe una persona.

## Parte 3 — las junturas al inventario

Decidido en `D78`, con la clave `(quimera <nombre>, "juntura")` y granularidad quimera x
organismo x gen impactado. Son dos filas, una por quimera, y la segunda ya esta medida:

* `Q_BicC_Dm__VATPaseB_Dm` — cero bloques fabricados por el empalme `[M]`.
* `Q_VATPaseB_Dm__BicC_Dm` — tres bloques contra maiz, ninguno de 21/21 `[M]`.

La fila de la segunda ya esta escrita, en el esquema de columnas de `M6`, en
`research\ola6\O3_quimera_bicc_vatpase_b\resultados\alertas_juntura_d48_o3_corregido_vienna.tsv`.
Lo que falta es que el generador la produzca en vez de que este pegada al costado:
`tabla_alertas.py` tamiza regiones de los seis genes del panel y una juntura no es eso. Al
integrarla hay que cambiarle la `region` de `"juntura, j=1,2,3"` a `"juntura"`, por el
motivo que `D78` da: los `j` son el resultado de medir, no el objeto que se usa.

Y falta la fila de la quimera sin aciertos, que es la que hace la distincion de `D72`:
sin ella, «se tamizo y no hay nada» y «nunca se tamizo» vuelven a verse igual.

Mientras esto no se integre, **una quimera puede pasar la compuerta con su empalme sin
tamizar** `[?]`. Es lo que dice la entrada 31 de la ola 6 y sigue siendo cierto.
