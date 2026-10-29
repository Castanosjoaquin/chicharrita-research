# V2 — Preregistro del barrido de robustez y del nulo de permutaciones de `Rpn6`

**Escrito y commiteado ANTES de calcular ninguna de las dos cosas.** Fecha: 2026-10-29.
Antecedente: `PREREGISTRO.md` (`486aeb1`) y `REPORT.md`, que en §0 corrige la limpieza de la
región a la definición oficial de `ranking.ejes()` (`bb9e666`). Esta línea responde a la pregunta
«¿`Rpn6` aguanta lo mismo que `BicC_Dm`?» con las mismas pruebas que `M7` le hizo a `BicC_Dm` 922-1221
y el mismo nulo que `F3` le hizo al gen entero.

## 1. Qué se fija y no se re-elige

- Región de `Rpn6`: `GITV01002940.1`, CDS `GITV01002940_1_cds`, **325-624**, tal como la dejó
  `REPORT.md`. No se vuelve a elegir con la grilla: lo que se mide es si **esa** elección aguanta.
- Región de `BicC_Dm`: **922-1221**. Sus conteos **no se recalculan**: se leen de
  `research/ola4/M7_robustez_bicc/resultados/grilla_parametros.tsv` (filas `backend = vienna`).
- Motor: `grilla_parametros.py` de `M7`, **importado sin tocar** (`primitivos`, `eficientes`,
  `verificar_vectorizacion`). La grilla es la de `M7`: brecha de estabilidad 0,0 a 2,0 (21 valores) ×
  accesibilidad 0,05 a 0,30 (26) × modo (`fiel`, `corregido`) × tabla (`NN3`, `NN4`) =
  **2.184 configuraciones**, sólo `vienna`.
- **RNAplfold 2.1.5 no corre en esta máquina** (el único binario del repo es el `.exe` de Windows).
  El eje del motor se declara **no corrido**, no cero; es la regla de `M7`.

## 2. Anclas, que corren antes de medir y abortan la corrida si fallan

1. Las anclas de `grilla_parametros.anclas()` sobre los cuatro genes de `W5` con `vienna`/`NN3`
   (142/39/223/35 en `fiel`, 123/30/171/29 en `corregido`; regiones vigentes 38, 21, 36, 21).
2. `verificar_vectorizacion()` sobre el gen de `Rpn6` y sobre su región recortada.
3. **Reproducción de `BicC`:** con mi motor se recalcula `BicC_Dm` 922-1221 en 12 configuraciones
   —las seis esquinas de la grilla y el punto por defecto, en los dos modos— y deben coincidir **todas**
   con las de `grilla_parametros.tsv`, en marco contexto y marco recorte. Si una falla, no se lee
   ningún número de `Rpn6`.

## 3. Las preguntas, con la regla de lectura escrita antes

**P1. ¿La eficacia de `Rpn6` es comparable a la de `BicC`?** En cada configuración, en marco
**recorte** (la molécula que se sintetizaría, `D63`) y en marco **contexto**, se compara el número
de eficientes de `Rpn6` 325-624 contra el de `BicC_Dm` 922-1221 en la misma configuración. Se
reportan las tres fracciones (gana / empata / pierde), la diferencia mediana y su rango.
- «Misma eficacia que `BicC`» queda **refutada** si `BicC` gana en **más de la mitad** de las
  configuraciones, y **sostenida** si `Rpn6` gana o empata en **al menos la mitad**.
- No se declara superioridad de `Rpn6` por ganar más de la mitad; sólo «no peor».

**P2. ¿La elección de la región es estable?** En cada configuración se calcula, en marco contexto, el
número de eficientes de **todas** las regiones de 300 nt **admisibles** del gen (inicio entre 60 y
`cds_nt − 59 − 299`, sin ninguna ventana con coincidencia perfecta de 21 nt contra el panel de seis)
y se mira si 325-624 está **entre las de máximo conteo, empates incluidos**. Se reporta la fracción
de configuraciones en que lo está y, cuando no, cuál región la reemplaza y con qué frecuencia.
- Estable si lo está en **≥ 50 %**; si no, «la elección depende de los parámetros» y se lista el
  reemplazo. Es la misma pregunta que `M7` le hizo a 922-1221 contra 2121-2420 (36,4 % en contexto).

**P3. ¿Y contra la región por densidad?** El rival es la región de 300 nt de **máximo conteo sin
veto** en el punto por defecto (`corregido`, `vienna`, `NN3`, 1,0, 0,1), que `REPORT.md` §2 ya
midió en 309-608 con 30. Se reporta la fracción gana / empata / pierde de 325-624 contra ella.
Es **sólo descriptivo**: perder en eficacia contra la región por densidad es esperable, porque
esa región no pasó el veto; lo que se mira es cuánto cuesta el veto.

**P4. ¿Depende de la fuente de la secuencia?** Se toman los 300 nt de `Rpn6` 325-624 **tal como los
escriben** `GHCC01050726.1` (Argentina) y `GCWP01019967.1` (Illinois), delimitados por la coincidencia
exacta de los primeros y los últimos 19 nt de la región (en cualquiera de las dos hebras). Si no
aparecen los dos extremos o el largo no es 300, la fuente se declara **no corrida**. Se recalcula la
eficiencia de la molécula en el punto por defecto, en los dos modos, y se reporta cuántas de las
26 eficientes se conservan y cuántas se ganan. Misma pregunta que `eje_referencia.py` de `M7`.

**P5. ¿Depende del criterio de riesgo?** Para la región de `Rpn6`, con las seis referencias, se
reporta el número de ventanas con acierto bajo cada criterio por separado (`perfecto_21`,
`perfecto_ge19`, `mm1_21`) y la limpieza oficial de `ranking.ejes()` bajo la regla conservadora y la
mecanicista. Para `BicC_Dm` se citan los valores ya publicados en `O3` (0,9884 y 0,9974). No se
recalcula `BicC_Dm` por criterio: sus columnas de `M7` usan otra definición de riesgo.

## 4. El nulo de permutaciones

Mismo diseño que el eje 3 de `F3`: **50 permutaciones** de la secuencia `GITV01002940_1_cds`
que conservan la composición de mononucleótidos, **semilla 20261029**, tamizadas con
`offtarget_21nt.py --mm1` contra las mismas seis referencias, con el mismo motor.

- **N1, nivel gen.** Estadístico: fracción limpia con la definición de `F3` (ventanas sin ningún bloque
  ≥ 19 nt en ninguna de las seis, sobre todas las ventanas). Se compara el 0,9624 observado con el
  rango del nulo. Regla de `F3`, sin cambios: si el observado cae **dentro** del rango del nulo, el
  eje **no distingue el gen del azar** y se dice así.
- **N2, nivel región.** Estadístico: limpieza de `ranking.ejes()` (conservadora, marco molécula de 280
  ventanas) de **todas** las regiones de 300 nt de las 50 permutaciones. Se reporta el percentil del
  0,9910 observado dentro de ese nulo, y qué fracción de las regiones del nulo trae alguna ventana con
  coincidencia perfecta de 21 nt (la tasa base del veto). «Exceso de coincidencias sobre el azar» si el
  observado queda por **debajo del percentil 5** del nulo; «no distinguible del azar» si queda dentro
  del rango intercuartílico.
- **Límite declarado antes de medir:** el nulo conserva composición, **no** uso de codones ni
  repeticiones, así que es un **piso** y no una cota (`F3` lo dijo igual).

## 5. Qué NO se concluye, escrito antes

- Nada de esto toca el eje 1 de `F3` (fenotipo, peso 0,40), que sigue medido en *S. titanus* y
  *E. variegatus*.
- Una región que aguanta la grilla **no queda validada**: el criterio de eficiencia sigue sin validar
  (ρ = +0,142, IC95 [−0,247; +0,492], n = 29). Robustez a los parámetros no es validez del criterio.
- El eje 4 de conservación ya se reportó en `REPORT.md` §3ter como medición posterior y no se repite.
- Que `Rpn6` aguante igual que `BicC` **no** lo pone en la cohorte `A+3+4` ni recalcula el puntaje de `F3`.
- Los resultados se reportan **sean cuales sean**. Si `Rpn6` no aguanta, ése es el resultado.
