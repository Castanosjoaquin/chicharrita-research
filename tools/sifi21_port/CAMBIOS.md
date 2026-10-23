# Cambios respecto de si-Fi21, con su justificación

Base: si-Fi21, fuente oficial en `github.com/snowformatics/siFi21-`, commit `d6296b7`
(2025-03-18). Artículo: Lück S, Kreszies T, Strickert M, Schweizer P, Kuhlmann M,
Douchkov D. «siRNA-Finder (si-Fi) Software for RNAi-Target Design and Off-Target
Prediction». *Frontiers in Plant Science* 2019;10:1023.
`https://doi.org/10.3389/fpls.2019.01023`

Cada cambio dice qué hacía el original, dónde, qué hace ahora y por qué era
necesario. Los que cambian un resultado numérico están marcados como tales.

Advertencia de alcance: el fuente de GitHub **no es idéntico** al binario de 2017
que distribuye SourceForge. `Resources/ui_sifi2015.py` mide 23.791 bytes en la
instalación y 23.787 en el clon. Todo lo que sigue describe el fuente. `[?]`

---

## C1 — La regla terminal dejó de poder saltear la termodinámica

**Afecta el resultado.** Es el cambio importante.

El original, en `sifi_pipeline.py:525-550`, compone primero un veredicto
termodinámico —selección de hebra guía, estabilidad de extremos y accesibilidad
del sitio blanco, en conjunción— y después aplica una regla sobre los nucleótidos
terminales. Esa segunda regla no es un filtro: es una ramificación, y una de sus
ramas devuelve «eficiente» sin mirar el veredicto termodinámico. Concretamente,
cuando el nucleótido 19 es A o T y el 2 no lo es, las líneas 535-541 deciden
mirando **solo la accesibilidad**. Un siRNA que falla la selección de hebra y la
estabilidad de extremos puede quedar clasificado como eficiente por esa vía.

Medido sobre los datos del corpus, comparando ventana por ventana los dos modos con
el mismo RNAplfold 2.1.5:

| Gen | Fiel | Corregido | Entran por el bypass | En sentido contrario |
|---|---|---|---|---|
| `MP_MRFV_full` | 133 | 114 | **19** (14 %) | 0 |
| `CP_MRFV_full` | 32 | 25 | **7** (22 %) | 0 |
| `BicC_Dm_full` | 212 | 162 | **50** (24 %) | 0 |
| `ATPaseD_Dm_full` | 42 | 34 | **8** (19 %) | 0 |

Entre el 14 % y el 24 % de lo que si-Fi reporta como eficiente lo es **sólo porque
la regla terminal se saltea la física**. Las 84 ventanas caen todas en la rama de
`sifi_pipeline.py:535-541`, ninguna en otra, y **ninguna ventana va en sentido
contrario**: el modo corregido es un subconjunto estricto del fiel.

> **Corrección de una versión anterior de este documento.** Decía «11 de 133, un
> 8,3 %», y estaba mal: ese número salía de restar dos totales (133 eficientes menos
> 122 que pasan la termodinámica), y el total termodinámico incluye ventanas de la
> rama 4 que **los dos modos rechazan igual**. Restar totales no cuenta ventanas. La
> cifra correcta, contando ventana por ventana, es 19 de 133.

**Por qué el efecto es de ese tamaño.** La rama del bypass cubre entre el 24 % y el
29 % de las ventanas de cada gen —son las que tienen A o T en la posición 19 y G o C
en la 2—, y ahí el original exige **sólo accesibilidad** en lugar de las tres
condiciones. Que un 6 % de esa franja pase de más es poco sobre el gen entero, pero
mucho sobre el conjunto de eficientes, que ronda el 10 % de las ventanas. De ahí que
un efecto chico en términos absolutos se traduzca en una inflación de dos dígitos.

El modo `corregido` aplica la preferencia terminal como filtro adicional sobre el
veredicto termodinámico, que nunca se saltea:

```python
eff = thermo and ((nt19 in "AT") or (nt2 in "GC"))
```

Justificación biológica: la preferencia del bolsillo MID de Argonauta por un 5'
terminal U o A es una regla de afinidad que **suma** evidencia sobre cuál hebra se
carga; no es un mecanismo que vuelva innecesaria la asimetría termodinámica del
dúplex, que es lo que gobierna el desenrollado. Tratarla como sustituto invierte
la jerarquía causal. El propio artículo presenta las reglas de secuencia como
complemento de las termodinámicas, no como reemplazo.

El modo `fiel` conserva la rama tal cual, porque hace falta para auditar cualquier
número producido con si-Fi.

## C2 — Python 2.7 a Python 3

El original no importa en un intérprete moderno: usa `print` como sentencia
(`sifi_pipeline.py:222`, `free_energy.py:284`), `np.float` (eliminado en numpy
≥ 1.24) y división entera implícita. El README oficial reconoce que la herramienta
«no está actualizada» y que necesitaría una reescritura.

Sin este cambio no hay nada que correr: es la condición para todo lo demás.

## C3 — Tablas de mismatch de ADN dentro de un cálculo de ARN: instrumentadas, no sustituidas

El original mezcla química. En `free_energy.py:278-279` los defaults son:

| Argumento | Tabla | Química |
|---|---|---|
| `nn_table` | `RNA_NN3` (Chen et al. 2012) | ARN, correcta |
| `de_table` | `RNA_DE2` (Turner & Mathews 2010) | ARN, correcta |
| `tmm_table` | `DNA_TMM1` | **ADN/ADN** |
| `imm_table` | `DNA_IMM1` (Allawi & SantaLucia 1998) | **ADN/ADN** |

Los apilamientos canónicos y los extremos colgantes usan parámetros de ARN, pero
los mismatches terminales e internos usan parámetros de ADN. Es consecuencia de
que `_check()` hace `back_transcribe()` y convierte U→T: el cálculo entero corre
en alfabeto de ADN, que es lo que permite indexar tablas de ADN sin que falle.
Consecuencia concreta: **un par G-U no se trata como wobble de ARN**; después de la
conversión es un mismatch G-T buscado en `DNA_IMM1`.

**No las sustituí**, y la razón es metodológica: reemplazarlas exige parámetros de
mismatch de ARN publicados y verificados, y no los tengo de una fuente que haya
abierto. Inventar valores o trasladarlos de memoria violaría la regla de evidencia
del proyecto. Lo que hice es instrumentar: `free_energy(..., track=dict)` cuenta
cada consulta a una tabla de mismatch, y `run_sifi.py` avisa si hubo alguna.

Resultado de la medición sobre los cuatro casos corridos: **cero consultas**. En la
ruta que si-Fi usa para la eficiencia —dos ventanas de 3 nt contra su
complementario con un extremo colgante— las claves de mismatch no se alcanzan
nunca. Así que la mezcla ADN/ARN existe, está mal, y **no afecta a este uso**.
Afectaría al cálculo con secuencias desapareadas, que si-Fi no hace acá.

Queda anotado como pendiente por si alguna vez se extiende el cálculo.

## C4 — La temperatura pasó a ser un parámetro

**Afecta el resultado.**

El original la tiene fijada en 22 °C, en dos lugares independientes:
`free_energy.py:420` (`tao = 273.15 + 22`, que entra en el ΔG) y
`sifi_pipeline.py:62` (`self.temperature = 22`, que va a RNAplfold como `-T 22`).

Conviene decirlo con claridad porque circula lo contrario: **si-Fi no calcula a
37 °C**. Ya está en el rango ambiente que corresponde a un ectotermo y a un cultivo
a campo. No había nada que corregir ahí.

Lo que sí hacía falta es poder moverla, porque la temperatura **no se cancela** en
la comparación que hace si-Fi: el veredicto depende de ΔΔG = ΔΔH − T·ΔΔS, y
ΔΔS ≠ 0. Ahora es argumento (`--temp`), con 22 °C por defecto para no cambiar el
comportamiento sin pedirlo.

Verificado en `test_sifi.py`: el ΔG es más negativo a 22 °C que a 37 °C, que es el
signo correcto —un dúplex es más estable en frío.

## C5 — Se eliminó el cálculo de Tm, que no se usaba

`free_energy.py:424` calcula una temperatura de fusión y la descarta: la función
retorna `deltaG` en la línea 431. Por lo tanto `dnac1`, `dnac2` y `selfcomp` son
parámetros muertos que no influyen en nada.

No cambia ningún resultado. Se elimina porque son tres parámetros que invitan a
perder tiempo ajustándolos, y uno de ellos (`dnac1=25`) parece significativo.

## C6 — Las tablas se toman de Biopython en vez de copiarse

El `free_energy.py` del original es una copia de `Bio.SeqUtils.MeltingTemp` con un
retorno de ΔG agregado. Biopython mantiene las mismas tablas, con los mismos
valores, para Python 3. Tomarlas de ahí evita arrastrar una copia de datos de hace
una década y hace verificable la equivalencia.

**Trampa de nomenclatura, documentada porque cuesta horas:** lo que si-Fi llama
`RNA_DE2` —y usa por defecto— es exactamente la tabla que Biopython llama
`RNA_DE1`, con el mismo formato de clave (`.G/CC`). Lo que si-Fi llama `RNA_DE1`
es la misma tabla con las claves invertidas (`CC/G.`) y **no se usa en ninguna
parte del programa**. Derivar una de la otra al revés produce un `KeyError`.

Igual advertencia con los apilamientos: el original define `RNA_NN1` (Freier et al.
1986) y `RNA_NN2` (Xia et al. 1998) pero **no las usa**; el default es `RNA_NN3`,
que es Chen et al. 2012. Es decir que si-Fi ya está en las tablas modernas. La
presencia de las viejas en el archivo hace fácil concluir lo contrario.

`test_sifi.py` verifica clave por clave, contra valores transcritos del fuente, que
las tablas de Biopython son las de si-Fi.

## C7 — Corre sin interfaz gráfica, y Bowtie quedó desacoplado

El original es una aplicación Qt4 de escritorio: el cálculo está entrelazado con la
ventana, y `get_main_target()` abre un diálogo modal que espera que una persona
elija el blanco principal de una lista. No es automatizable ni reproducible.

Además, en el original todo el bloque de eficiencia está dentro de un
`if strand == '+'` (`sifi_pipeline.py:221`), así que Bowtie decide **qué** ventanas
se registran. Pero el veredicto de cada ventana no depende de Bowtie en absoluto:
`calculate_efficiency()` recibe solo la secuencia del siRNA, la del siRNA de dos
posiciones antes y un número de accesibilidad. En el uso normal del modo diseño la
base contiene el gen consultado, todas las ventanas tienen hit perfecto en hebra +,
y entonces el perfil de eficiencia es función únicamente de la secuencia.

Este port calcula ese perfil completo, sin base de datos y sin diálogos. El
tamizaje de off-targets con Bowtie es un paso separado y **no está incluido acá**:
el repositorio ya tiene esa parte resuelta con Bowtie y BLAST+ locales.

## C8 — La corrección salina quedó documentada como inocua

`free_energy.py:280` trae `Na=20, K=50, Mg=0, saltcorr=5`. Son ~70 mM de
monovalentes con la corrección entrópica de SantaLucia. Conviene aclararlo porque
también circula lo contrario: **si-Fi no calcula a 1 M de NaCl**.

Es cierto que `Mg=0`, o sea que no hay magnesio, y que eso no refleja el medio
intracelular. Pero cambiarlo **no mueve ningún veredicto**, y la razón es
estructural: el método 5 es `corr = 0.368 · (len(seq) − 1) · ln(mon)`, función
únicamente del largo de la secuencia. si-Fi nunca usa un ΔG absoluto —compara
`anti ≥ sense` y `(anti − sense) ≥ 1`, siempre entre ventanas de 3 nt del mismo
largo—, así que la corrección es idéntica en los dos términos y se cancela exacto
en la resta.

Está verificado como test (`test_sal_se_cancela`): agregar 5 mM de Mg²⁺ no cambia
la diferencia de ΔG. Los parámetros siguen expuestos, pero sabiendo que no hacen
nada acá.

## C9 — Limpieza

Se eliminaron los `print` de depuración (`free_energy.py:284` imprime cada
secuencia procesada; `sifi_pipeline.py:222` imprime `'ok'` por cada siRNA). En un
gen de 1.263 nt eso son miles de líneas a stdout.

---

## C10 — La salida publica las categorías de la regla terminal, y ya no el 21-mero

El TSV por ventana suma `nt19_at`, `nt2_gc` y `rama_terminal` (1 a 4), y **deja de emitir
`seq` por defecto**. Las dos cosas son de la línea M3 de la ola 4 (issue #7) y están
decididas en el ADR D54.

Por qué categorías y no los nucleótidos: la regla terminal no mira la letra, mira si
`nt19` es A/T y si `nt2` es G/C (`_terminal_rule`, que reproduce `sifi_pipeline.py:525-550`).
Emitir la letra sí tiene un costo, medido por la línea M9: como las ventanas se solapan de
a 1 nt, la columna de una posición fija concatenada en orden es una subcadena literal del
gen, y `nt19` con `nt2` reconstruyen el 99,4 % de un gen de 500 nt **sin producir ninguna
racha de 21 nt**. Las categorías conservan todo el poder predictivo de la regla y bajan de
dos bits por posición a uno.

Por qué `seq` sale de la salida por defecto: un 21-mero por ventana, sobre ventanas que se
solapan de a 1 nt, reconstruye el gen entero. Fue el incidente de C9 del repositorio. Quien
la necesite para un paso local la pide con `--con-seq` y no versiona esa salida.

`--features` emite la tabla de los seis términos sin ningún booleano de veredicto, que es
la tercera alternativa que propuso Diego. Esa tabla no se versiona: ver
`research/ola4/M3_features/REPORT.md` §5.

**Ningún veredicto cambió:** las 4.722 ventanas de los cuatro genes, en los dos modos,
reproducen el ancla de C9 con cero discrepancias.

## Lo que deliberadamente NO cambié

- **La ponderación por posición de los mismatches en off-targets.** El original
  corre `bowtie -a -v N -y`, conteo extremo a extremo ciego a la posición
  (`sifi_pipeline.py:332`). Químicamente un mismatch no vale lo mismo en la región
  semilla (nt 2-8), que gobierna la nucleación, que en las posiciones 10-11, donde
  el apareamiento es indispensable para el corte. Es una mejora legítima y
  pendiente, pero pertenece al módulo de off-targets, que no es este. Meterla acá
  mezclaría dos cosas.
- **El umbral de estabilidad de extremos (1 kcal/mol) y el de accesibilidad (0,1).**
  Son los valores del artículo y de la interfaz. No hay motivo para moverlos sin
  datos.
- **La ventana de accesibilidad u=8 y el tamaño de 21 nt.** Idem. El investigador
  confirmó en el checkpoint que 21-22 es lo que tiene respaldo biológico.
- **La doble aplicación de `init_5T/A`** (`free_energy.py:366-371`), que suma la
  misma penalización si la secuencia empieza con T y otra vez si termina con A.
  Viene de Biopython y es el tratamiento simétrico correcto del dúplex, no un
  error.
