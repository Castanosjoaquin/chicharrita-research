# O3 — La quimera `BicC_Dm` + `V-ATPase B`, con las tres cuentas separadas

**Veredicto: la quimera se puede armar, su empalme no fabrica ningún riesgo nuevo y el
orden importa.** Pegando la región vigente de `BicC_Dm` (922-1221) con una región de 300
nt de la subunidad B de la V-ATPasa de *Dalbulus maidis* recuperada en `O2`, las dos
moléculas posibles quedan **sin veto**: ninguno de los 240 bloques de 19 a 21 nt que
cruzan las dos junturas coincide en maíz, en *Harmonia axyridis*, en *Apis mellifera*, en
*Folsomia candida* ni en *Homalodisca vitripennis*; los 19 bloques con acierto caen todos
en el genoma del propio vector, que para dos genes del insecto es blanco y no riesgo `[M]`.
El orden `V-ATPase B` + `BicC_Dm` rinde **34 ventanas eficientes** contra 31 de la suma de
sus partes (Δ+3) y el orden inverso rinde 32 (Δ+1), los dos con **una sola** de sus 20
ventanas de juntura eficiente y **ninguna** ventana eficiente de juntura con blanco
continuo de 21 nt `[M]`. Lo que no mejora es la tasa: por ventana, la quimera queda por
debajo de `BicC_Dm` sola en los dos ejes del ranking, porque la región de `V-ATPase B` que
sobrevive al veto es pobre en eficientes. Leído contra `D67` eso **no la descarta** —el
objetivo declarado es cubrir dos fenotipos, no maximizar el conteo— y lo que la
descartaría, el perfil de riesgo del empalme, está limpio.

**Fecha de corrida:** 2026-10-27, en la máquina de Santino (Windows 11, `python` 3.13.15
de miniconda, ViennaRNA 2.7.2, `pyahocorasick`). Es la misma máquina y la misma versión
con las que corrió `C13`, verificado en el `comando_run_sifi` de
`research/ola3/C13_quimeras_region_recomendada/resultados/quimeras_meta_vigentes_corregido_vienna.json`.
**Ninguna secuencia salió de la máquina.**

---

## 1. El ancla, antes de leer un número nuevo

El issue #23 pide generalizar el evaluador de quimeras, que hasta ahora tenía los cuatro
genes de EPILAB fijos en `quimeras_v2.py:51`, y pide conservar lo que autoriza a leer
cualquier número que salga de él: que el conjunto `epilab` siga reproduciendo la tabla de
`C4` fila por fila. **Pasa en los dos modos, después de la generalización**: 12 filas × 17
columnas idénticas en `fiel` y en `corregido` `[M]`. Las salidas regeneradas del conjunto
`epilab` coinciden además con las que ya estaban versionadas, lo que dice que el refactor
no movió nada: el único archivo que `git status` marca como cambiado es el script.

La generalización es `--gen NOMBRE=a-b[:ruta_fasta]`, repetible, con `--nombre` para el
conjunto y `--resultados` para que una corrida de otro bloque escriba en el suyo y no
ensucie el registro de `C13`. Los tres conjuntos publicados (`epilab`, `recomendadas`,
`vigentes`) no se tocan, y `registrar_conjunto` aborta si un conjunto ad hoc intenta usar
uno de esos tres nombres. El mismo par de banderas entró en `offtarget_ranking.py`, que
comparte las coordenadas con el evaluador.

## 2. Por qué esta combinación, y por qué hubo que elegirle una región

La combinación sale de la reunión del checkpoint 2 y de `D67`: las quimeras se arman por
**combinación de fenotipos**, no por suma de conteos. `BicC_Dm` tiene el mejor perfil de
riesgo del panel pero su fenotipo reduce la población entre generaciones sin cortar la
transmisión en la temporada; `V-ATPase B` aporta los dos ejes que le faltan, movilidad
—alas deformes— y mortalidad, con fenotipo reportado en la especie por entrega oral `[R]`
(supervivencia 16 % al día 4 contra 37 % del control de GFP; Jones, Bernal y Medina 2021,
**preprint de bioRxiv sin revisión por pares**, registrado como leído en texto completo en
`00_meta/FUENTES.md` `S18` y en `research/ola2/W6_agentes_ciencia/sources.json` `PRB-04`).
Que la única evidencia de fenotipo de este gen sea un preprint es parte del resultado y no
una nota al pie. Que `V-ATPase B` y
`V-ATPase D` sean dos subunidades del mismo complejo y se separen justo por el eje que el
investigador nombró es lo que vuelve armable la combinación y no una ocurrencia `[H]`.

`BicC_Dm` ya tenía su región elegida y publicada. `V-ATPase B` no tenía ninguna: el gen se
recuperó recién en `O2`. Así que antes de armar la quimera hubo que elegirla, y el criterio
está escrito en el encabezado de `scripts/01_region_vatpase_b.py` **antes de la primera
corrida**: 300 nt como los dos genes del insecto vigentes, perfil de eficiencia en el
contexto del gen entero y modo `corregido` como en `C7`, riesgo con el panel de seis y los
pesos de `ranking.pesos_base()` sin tocar, el genoma del vector fuera del cómputo por
on-target, regla conservadora, forma `cascada` —veto duro por coincidencia perfecta de 21
nt y orden por eficientes limpias— y la regla de no pisarse de `ranking.alternativas`.

### Lo que la elección encontró, y que vale por sí solo

**`V-ATPase B` es un gen riesgoso por el propio criterio del proyecto.** De las 1.184
regiones de 300 nt que caben en su CDS de 1.503 nt, **784 están vetadas**: contienen al
menos una ventana con coincidencia perfecta de 21 nt en una referencia que no es el vector.
Sólo 400 sobreviven `[M]`. El gen entero tiene 12 ventanas con coincidencia perfecta de 21
nt en el transcriptoma de *Zea mays* y 38 en *Homalodisca vitripennis* `[M]`; `BicC_Dm`, en
su región vigente, tiene **cero** en todo el panel. La conservación que vuelve atractivo a
un gen esencial es la misma que le trae off-targets, y acá está medida en un caso.

La región elegida es **242-541**, no vetada, con limpieza 0,9598 y el primer puesto entre
las 1.184 `[M]`. Su conteo de eficientes depende del marco, y `D63` obliga a decir cuál:
los tres marcos dan **13 / 6 / 5** —13 en contexto con todos los arranques, 6 en contexto
con los comparables, 5 en la molécula recortada—, con 7 ventanas de límite físico y 1 de
contexto neto `[M]`. **La cifra que se publica de esta región es 5**, la del marco 3,
porque es la molécula que existiría (`D63`); el ranking que la eligió corre en el marco 1,
que es el marco en el que `C7` eligió las regiones publicadas. Los tres números salen de
`research/ola5/N3_marcos/scripts/tres_marcos.py`, al que `O3` le agregó una bandera `--gen`
para medir una región de un gen nuevo sin tocar las seis de `N3`: en la misma corrida las
seis anclas publicadas se reprodujeron. Dos cosas más hay que leer al lado:

**Las dos formas del ranking no coinciden, y la discrepancia es el eje de riesgo.** La
forma `geometrica` pone primera a 858-1157, que tiene 25 eficientes —casi el doble— y
**16 ventanas con coincidencia perfecta de 21 nt**, o sea vetada por la cascada `[M]`. El
criterio declarado antes era la cascada, así que la elección es 242-541; pero quien quiera
más eficacia en este gen la paga en veto, y eso es una propiedad del gen, no del método.

**La región no depende de la fuente del CDS.** Los dos CDS independientes de `O2` —el del
genoma y el del contig `GHCC01013224.1` del transcriptoma de Pergamino— difieren en tres
nucleótidos, en las posiciones 615, 678 y 1254. Ninguna cae en 242-541 ni en los 20 nt de
arrastre de sus ventanas, así que el veredicto de la región es el mismo con cualquiera de
los dos `[M]`. Lo que sí la toca es la cobertura: `GCWP01` tiene el gen partido y no cubre
las posiciones 145-264 de la proteína, que son los nucleótidos 433-792, de modo que el
tramo 433-541 de esta región va **sin datos** y no como cero en cualquier tabla de
conservación por fuente (`D64`).

## 3. Las tres cuentas separadas

`§0` del plan de la ola 6 obliga a no sumar en una sola cifra lo que se hereda y lo que se
recalcula. Las tres cuentas, modo `corregido`, backend `vienna`:

| | `V-ATPase B` + `BicC_Dm` | `BicC_Dm` + `V-ATPase B` |
| --- | ---: | ---: |
| Eficientes de las partes sueltas (26 + 5) | 31 | 31 |
| **Eficientes heredadas** en la quimera | **33** (5 + 28) | **31** (26 + 5) |
| Ventanas heredadas que cambiaron de veredicto | 4 — 3 ganan, 1 pierde | 4 — 2 ganan, 2 pierden |
| Distancia máxima a la unión de una heredada que cambió | 47 nt | 32 nt |
| **Eficientes de juntura**, de 20 ventanas | **1** (j = 20) | **1** (j = 4) |
| De ésas, con blanco continuo de 21 nt | **0** | **0** |
| **Bloques del empalme con acierto fuera del vector** | **0** | **0** |
| Eficientes totales | 34 | 32 |
| Δ contra la suma de las partes | **+3** | **+1** |

**El orden importa, y acá se ve por qué.** Las dos moléculas tienen la misma composición y
difieren en 2 ventanas eficientes. La diferencia no está en el empalme —las dos tienen
exactamente una ventana de juntura eficiente— sino en la banda de contexto: con `BicC_Dm`
a la derecha, sus ventanas heredadas pasan de 26 a 28, y con `BicC_Dm` a la izquierda se
quedan en 26. Es el mismo mecanismo que `C13` midió en las doce quimeras de las regiones
vigentes, donde `ATPaseD_Dm` + `MP_MRFV` daba +3 y el orden inverso −3 `[M]`.

**Las cuatro ventanas que cambiaron, en el orden bueno, están a 0, 2, 46 y 47 nt de la
unión** `[M]`, dentro del techo asimétrico que `C13` derivó del código: la secuencia ajena
influye hasta 72 nt corriente abajo del final de una ventana y hasta 59 corriente arriba
de su comienzo, porque la ventana de plegado de 80 nt con la que el original calcula
accesibilidad cruza la unión `[M]` el número, `[H]` la derivación. Que acá sean 4 y no 61
—lo que dieron las doce quimeras vigentes— no es una propiedad de las quimeras: es el
resultado de estas dos regiones.

## 4. El riesgo del empalme, y la alerta que no hubo

El tamizado de `offtarget_ranking.py` evalúa sólo lo que es nuevo: las regiones completas
una vez y, por quimera, el tramo de 40 nt que cruza la unión, que da exactamente sus 20
ventanas. Es la economía que `C13` justificó —1.160 ventanas en vez de 5.760, con
resultado idéntico— y vale porque el estado de off-target de una ventana depende sólo de
su secuencia.

Sobre eso, `scripts/02_juntura_detalle.py` hace lo que el tamizado no hace: enumera los
bloques de 19, 20 y 21 nt de cada ventana de juntura, los busca exactos y en las dos
hebras en las seis referencias con un autómata de Aho-Corasick, y de cada acierto reporta
cuántos nucleótidos aporta cada gen. La distinción que decide la alerta es ésa: **un bloque
de 19 nt que entra entero en el aporte de un solo gen no lo fabrica el empalme**, ya existía
en ese gen y la quimera lo hereda; fabricado es el bloque que toma al menos un nucleótido
de cada lado.

El resultado, en las dos moléculas y en los dos modos `[M]`:

- **Cero bloques fabricados con acierto fuera del vector.** De las 240 fichas de bloque,
  19 tienen acierto y **las 19 caen únicamente en el genoma de *D. maidis***, que para dos
  genes del insecto es on-target.
- Los bloques que sí cruzan la unión y aciertan son los de j = 1, 2 y 3 del orden
  `V-ATPase B` + `BicC_Dm`, y aciertan en `OZ319705.1`, que es el cromosoma donde vive
  `V-ATPase B`: son el arrastre de los 18 a 20 nt que ese bloque toma del propio gen.
- **Ninguna de las 20 ventanas de juntura, en ninguno de los dos órdenes, tiene
  coincidencia en maíz, en el polinizador, en el enemigo natural, en la fauna del suelo ni
  en el cicadélido no objetivo.** Ni perfecta de 21, ni bloque de ≥ 19.
- Por eso **no se emitió ninguna fila de alerta** y `juntura_alertas_*.json` no existe. Es
  lo contrario del caso que `C13` encontró en `MP_MRFV` + `ATPaseD_Dm`, donde el empalme
  fabricaba un bloque perfecto de 19 nt inexistente en los dos genes y presente en tres
  transcriptos de *Zea mays* `[M]`.

**La única ventana de juntura con blanco continuo de 21 nt es j = 1 del orden `V-ATPase B`
+ `BicC_Dm`, y no es eficiente.** Su 21-mero completo existe en `OZ319705.1` por una
coincidencia de un solo nucleótido: toma 20 nt del final de la región de `V-ATPase B` y 1
de `BicC_Dm`, y ese nucleótido es el que el gen tiene en su contexto genómico. Es el mismo
patrón que `N4` describió —las ventanas con blanco son todas de los extremos y ninguna
eficiente— y confirma su lectura en un caso nuevo: la ventana de juntura que silenciaría
algo es la que casi no es de juntura.

Los ejes del ranking quedan así, regla conservadora `[M]`:

| Objeto | Ventanas | Eficientes | Eficacia | Limpieza | Limpias y eficientes | Veto |
| --- | ---: | ---: | ---: | ---: | ---: | :---: |
| `BicC_Dm` 922-1221 | 280 | 26 | 0,0929 | 0,9884 | 22 | no |
| `V-ATPase B` 242-541 | 280 | 5 | 0,0179 | 0,9580 | 5 | no |
| `V-ATPase B` + `BicC_Dm` | 580 | 34 | 0,0586 | 0,9731 | 30 | no |
| `BicC_Dm` + `V-ATPase B` | 580 | 32 | 0,0552 | 0,9741 | 28 | no |

**Cómo se lee esta tabla sin hacerle trampa.** Las dos quimeras tienen más eficientes
limpias en términos absolutos que cualquiera de sus partes (30 y 28 contra 22), pero miden
600 nt contra 300: el conteo absoluto no es comparable entre largos distintos y el propio
`ranking.ejes` lo dice al definir los dos ejes como tasas «y por eso comparables entre
candidatos de largo distinto». Por tasa, las dos quimeras están **por debajo** de `BicC_Dm`
sola en eficacia y en limpieza. La quimera no compra rendimiento por nucleótido; compra
cobertura de un segundo fenotipo, que es exactamente lo que `D67` declaró como objetivo.

## 5. Lo que estos números no dicen

**El límite del tamizado de juntura.** La auditoría localiza coincidencia exacta de 19 a 21
nt. Los aciertos con un desapareo quedan como cuenta del tamizado, sin bloque ni
transcripto: en el orden `V-ATPase B` + `BicC_Dm` hay **2 ventanas de juntura con
`mm1_21` en maíz** `[M]`, que ninguna de las dos moléculas hereda de sus partes y que esta
auditoría no puede ubicar. No son veto —el veto es la coincidencia perfecta de 21 nt
(`D48`) y el peso de `mm1_21` es 0,30 contra 1,00— pero son señal residual y quedan
declaradas, no omitidas `[?]`.

**El límite que `N4` ya tenía y acá se repite.** «Blanco continuo» se mide como
coincidencia exacta de 21 nt. Si una complementariedad incompleta diera actividad, las
ventanas de juntura no serían inútiles sino menos útiles, y no lo sabemos `[?]`.

**El marco del ranking no es el marco de la cifra publicada, y eso ya estaba decidido.** La
región figura con 13 eficientes en el ranking y con 5 como molécula, y la tentación es
leerlo como una contradicción nueva: no lo es. `D63` nombró los tres marcos, midió los seis
casos y decidió que la cifra publicable es la de la molécula; `O3` sólo agrega la séptima
fila con la misma herramienta. Lo que sí queda abierto, y es de `D63` y no de acá: **el
ranking se arma en el marco 1 y la región candidata se eligió ahí**, porque es el camino
que eligió las regiones publicadas. Rehacer la elección en el marco 3 cambiaría el orden de
las 1.184 candidatas y no se midió `[?]`. Es vecino del issue #20 y no se adelanta.

**La región de `V-ATPase B` no es una región recomendada.** Es **región candidata de O3** y
viaja así a todas las tablas. `ranking.region_recomendada()` exige que las alertas de la
región estén decididas, pero no distingue «se tamizó y no hay alertas» de «no se tamizó», y
esta región no tiene fila en el inventario de doce de `M6`: pasaría la compuerta por
ausencia de datos, no por estar limpia. Es el agujero que `D70` y el issue #30 cierran, y
convertir esta región en recomendación pide ese tamizado primero.

**Y el límite que hereda toda la cadena.** El criterio de eficiencia del port no está
validado experimentalmente. Un resultado in silico es una hipótesis sobre eficacia, no una
prueba.

## 6. La salvedad biológica, que va junto al resultado

Silenciando dos genes a la vez, si el bioensayo da negativo no se sabe cuál mitad falló. No
invalida el diseño —el objetivo declarado es justamente cubrir dos efectos— pero es un
argumento para testear las partes por separado primero, y conviene decirlo antes de que lo
pregunten `[H]`. A eso se suma que la mitad de `V-ATPase B` aporta 5 ventanas eficientes
contra 26 de `BicC_Dm`: si el efecto de movilidad y mortalidad depende de que esa mitad
silencie, la molécula está apostando a la mitad floja del diseño, y eso es una predicción
contrastable con las partes sueltas `[H]`.

## 7. Reproducibilidad

El CDS de `V-ATPase B` **no está versionado** —`sin_secuencias.py` rechaza toda racha de 21
nt— y se regenera en dos segundos desde el GFF de `O2`, que sí está versionado, y el genoma
público que ya está en disco. `BicC_Dm` es una de las cuatro secuencias de EPILAB, así que
ninguna salida de este bloque escribe bases: las ventanas y los bloques van por hash corto.

```bash
# 1. el CDS, desde el GFF de O2 y el genoma publico local (no necesita miniprot)
python research/ola6/O2_vatpase_b/scripts/02_extraer_cds.py research/ola6/O2_vatpase_b \
    work/offtarget_db/GCA_975739785.1_ihDalMaid1.1_genomic.fna.gz XP_054288745.1 VATPaseB_Dm
mkdir -p work/O3/fasta
cp research/ola6/O2_vatpase_b/resultados/VATPaseB_Dm_cds.fna work/O3/fasta/VATPaseB_Dm_full.fasta

# 2. perfil de eficiencia del gen entero y tamizado del panel de seis
python tools/sifi21_port/run_sifi.py work/O3/fasta/VATPaseB_Dm_full.fasta \
    --modo corregido --backend vienna --salida work/O3/sifi/full_corregido
python tools/sifi21_port/offtarget_21nt.py --consulta work/O3/fasta/consultas_pasoA.fasta \
    --mm1 --db work/offtarget_db/*.fna.gz --salida work/O3/offtarget

# 3. la region, con el criterio del encabezado del script
python research/ola6/O3_quimera_bicc_vatpaseb/scripts/01_region_vatpase_b.py

# 3b. los tres marcos de D63 de la region nueva; re-verifica las seis anclas de N3
python research/ola5/N3_marcos/scripts/tres_marcos.py \
    --gen VATPaseB_Dm=242-541:work/O3/fasta/VATPaseB_Dm_full.fasta \
    --nota "candidata de O3, D72" \
    --salida research/ola6/O3_quimera_bicc_vatpaseb/resultados

# 4. el ancla de C4, en los dos modos, ANTES de leer cualquier numero nuevo
for m in fiel corregido; do
  python research/ola3/C13_quimeras_region_recomendada/scripts/quimeras_v2.py \
      --conjunto epilab --modo $m --backend vienna
done

# 5. las dos quimeras, los dos ordenes, los dos modos
for m in corregido fiel; do
  python research/ola3/C13_quimeras_region_recomendada/scripts/quimeras_v2.py --nombre o3 \
      --gen BicC_Dm=922-1221 \
      --gen VATPaseB_Dm=242-541:work/O3/fasta/VATPaseB_Dm_full.fasta \
      --modo $m --backend vienna --resultados research/ola6/O3_quimera_bicc_vatpaseb/resultados
done

# 6. ejes del ranking y riesgo del empalme
python research/ola3/C13_quimeras_region_recomendada/scripts/offtarget_ranking.py --nombre o3 \
    --gen BicC_Dm=922-1221 --gen VATPaseB_Dm=242-541:work/O3/fasta/VATPaseB_Dm_full.fasta \
    --modo corregido --backend vienna \
    --resultados research/ola6/O3_quimera_bicc_vatpaseb/resultados

# 7. la auditoria de la juntura, que es la que decide la alerta
python research/ola6/O3_quimera_bicc_vatpaseb/scripts/02_juntura_detalle.py --modo corregido
python research/ola6/O3_quimera_bicc_vatpaseb/scripts/02_juntura_detalle.py --modo fiel
```

El paso 2 necesita `work/O3/fasta/consultas_pasoA.fasta`, que es la región de `BicC_Dm`
922-1221 seguida del CDS entero de `V-ATPase B`; el paso 6 vuelve a tamizar por su cuenta
los tramos de juntura. Entorno: `python` 3.13.15, ViennaRNA 2.7.2, `pyahocorasick`,
`numpy`. Tiempos medidos: perfil del CDS 10 s, cada tamizado del panel de seis 70 s, la
auditoría de juntura 90 s.

### Archivos

| Archivo | Qué es |
| --- | --- |
| `resultados/region_vatpase_b.json` | el criterio declarado, las 1.184 regiones, las dos formas y la elegida |
| `resultados/tres_marcos.{tsv,json}` | los tres marcos de `D63` de la región nueva (13/6/5) y las seis anclas publicadas reproducidas |
| `resultados/quimeras_eficiencia_o3_{corregido,fiel}_vienna.tsv` | las tres cuentas por orden |
| `resultados/quimeras_ventanas_cambiadas_o3_*.tsv` | las 4 heredadas que cambiaron, con su distancia |
| `resultados/ejes_ranking_o3_corregido_vienna.tsv` | los dos ejes de las partes y de las quimeras, en las dos reglas |
| `resultados/empalmes_offtarget_o3_corregido_vienna.json` | aciertos del empalme por referencia y criterio |
| `resultados/juntura_detalle_o3_*.json` | los 240 bloques, con aporte por gen y sin secuencias |
| `resultados/juntura_resumen_o3_*.tsv` | las dos cuentas de juntura y los bloques fabricados |
