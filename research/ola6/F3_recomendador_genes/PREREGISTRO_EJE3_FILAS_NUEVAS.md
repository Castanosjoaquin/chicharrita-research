# F3 — Eje 3 para las cuatro filas recuperadas de papers: el criterio, escrito antes de tamizar

**Fecha de escritura: 2026-10-28.** Extiende [`PREREGISTRO_EJE3.md`](PREREGISTRO_EJE3.md) y su enmienda 1.
Issue [#43](../../../../issues/43). Se commitea **antes** de tamizar ninguna de estas secuencias.

## 0. Lo que se corrige del preregistro anterior, y lo que este documento es

`PREREGISTRO_EJE3.md` §1 dice que las filas de otras especies «salen con el eje ausente» porque no
tienen el ortólogo de *D. maidis*. **Eso no es lo que `C5` hizo ni lo que el #43 pide.** Las 8 filas del
catálogo que traen conteos de off-target los traen para **la secuencia de su propia especie**
(*Scaphoideus titanus*, *Nephotettix cincticeps*, …), y el #43 es «recuperar las 28 secuencias de transcripto
de 15 especies». Este documento sigue esa línea, y lo declara con todas las letras:

> **El eje 3 de estas cuatro filas es un proxy.** Mide el off-target del gen **de la especie del paper**
> (*P. maidis*, *N. cincticeps*, *D. kuscheli*), no el del transcripto de *D. maidis*. El diseño de
> ARNdc se hace siempre sobre la secuencia propia del vector (`D37`), y un gen ortólogo puede tener
> otro perfil de coincidencias. Un valor de estas filas **no es comparable con el de las cinco filas
> `DM`**, y se publica rotulado como `proxy_especie_del_paper`.

## 1. Qué filas, y de dónde sale cada secuencia

Las cuatro con secuencia en mano tras el paso anterior (`recuperacion_6filas_REPORT.md`):

| Fila | Especie | Secuencias | Origen y referencia |
| --- | --- | --- | --- |
| `DE-01` | *Peregrinus maidis* | `KC473163.1` (V-ATPase B), `KC473162.1` (V-ATPase D) | NCBI, verificadas; citadas en R1 (Yao *et al.* 2013, PMID 23950915) |
| `CI-13` | *Nephotettix cincticeps* | `MN815919.1` (Hig) | NCBI, verificada; citada en R4 (Wang *et al.* 2020, PMID 32362876) |
| `DE-06` | *Delphacodes kuscheli* | `PZ371509.1` (eth), `PZ371510.1` (burs-alpha) | NCBI, verificadas; citadas en R6 (Andrada *et al.* 2026, PMID 42328018) |
| `DE-03` | *Peregrinus maidis* | `Pmtra-2_167888_1` y `_2` | S1 File de R2 (Wang *et al.* 2024, PMID 38635824); **sin accesión**, identidad por los cebadores del paper |

Las FASTA están en `work/F3_recuperacion/` (no versionadas). `HE-04` y `CI-07` no tienen secuencia y salen
con el eje ausente. `DE-01` usa las secuencias de NCBI y **no** los largos que declara el paper, que
difieren (entrada 101).

## 2. La medida: la misma, con tres reglas para filas con más de una secuencia

Idéntica a `PREREGISTRO_EJE3.md` §2: ventana de 21 nt, paso 1, sin filtrar por eficiencia; **limpia** si
`perfecto_ge19` vale 0 en las seis referencias de `D76` (maíz, *H. axyridis*, *A. mellifera*,
*H. vitripennis*, *F. candida*, humano), pesos iguales; puntaje = ventanas limpias / ventanas totales.
Mismas columnas publicadas (fracción por referencia, `perfecto_21`, `mm1_21`, limpia sin humano).
Mismo motor (`tools/sifi21_port/offtarget_21nt.py --size 21 --mm1`) y mismas referencias.

Lo nuevo, porque tres de las filas tienen más de una secuencia:

1. **La unidad de la fila son sus ventanas distintas.** Se juntan las ventanas de todas las secuencias de la
   fila y se **deduplican** (por ventana canónica, la menor de la ventana y su complemento reverso). Así dos
   isoformas de `DE-03` que comparten tramo no cuentan dos veces ese tramo.
2. **Una fila con dos genes distintos** (`DE-01`: B y D; `DE-06`: eth y burs-alpha) puntúa con **sus
   ventanas juntas**, y se publica además el puntaje de **cada secuencia por separado**. Se elige juntas y
   no «el peor gen» porque el catálogo define la fila como una unidad y porque un mínimo dependería de
   cuántos genes agrupe cada fila.
3. **Ancla de control.** El tamizado de estas secuencias se corre una vez, con una secuencia ya tamizada
   (`eth_Dm`, `work/sifi_v2/`) en el mismo lote. **Si sus conteos por ventana no son idénticos a los
   publicados, la corrida se aborta** y se informa, porque querría decir que el motor o las referencias
   no son los de `sifi_v2`.

## 3. El nulo

Igual que en `PREREGISTRO_EJE3.md` §3: 50 permutaciones **por secuencia** que conservan la composición, semilla fija
`20261029`, mismo motor y panel. La permutación `j` de todas las secuencias de una fila se junta y deduplica
como en la regla 1, de modo que cada fila tiene 50 valores nulos. Se publica mediana y rango junto al valor real,
y el nulo **no entra al puntaje**. Se lee igual: si el valor real cae dentro del rango, no se distingue de
una secuencia sin homología.

## 4. Qué le pasa al orden, y lo que se anota antes de verlo

**Dos de las cuatro filas no están en el orden, y por eso no se ordenan.** `CI-13` está fuera por
`fenotipo_invertido` (silenciar *NcHig* aumenta la infección) y `DE-06` por `sin_fenotipo_publicado`
(`fuera_del_orden.tsv`). Su eje 3 **se publica en una tabla aparte, sin puesto ni puntaje compuesto**: una fila
que `PREREGISTRO.md` §6.2 y §7.1 sacó del orden no vuelve a entrar por tener un eje más.

**`DE-01` y `DE-03` sí están en el orden** (hoy en las cohortes A, puesto 1 del empate, y B, puesto 2). Estas filas
**no tienen eje 4** (no hay secuencia de *D. maidis*), así que pasan a la cohorte **A+3** (ejes 1, 2 y 3; `DE-01`) y
**B+3** (ejes 1 y 3; `DE-03`), con los pesos de `D87` renormalizados sobre los ejes presentes (§4.2 de
`PREREGISTRO.md`). **Entre cohortes no se compara.**

Consecuencias previstas, para que no parezcan elegidas después:
- **Cada una queda sola en su cohorte nueva.** Una cohorte de un solo candidato no tiene orden que informar: el eje
  3 de esas dos filas se lee por sus columnas (fracción, referencias, nulo), no por un puesto.
- **La cohorte A pierde a `DE-01`**: su empate de primer puesto pasa de `CI-01`, `CI-02`, `CI-03`, `DE-01` a los
  tres primeros. Y **la cohorte B pierde a `DE-03`**. Si eso cambia la respuesta de `04_segundo_orden.py` («¿cambia
  el orden según el objetivo?»), se reporta en las dos lecturas que ya usa, y no se elige la que convenga.
- **Las cinco filas `DM` no se mueven**: su cohorte A+3+4 y sus puntajes no dependen de estas filas.

`orden_genes.tsv` y `segundo_orden` se regeneran, y el informe publica el `diff` fila por fila.

## 5. Reglas que siguen valiendo

Todas las de `PREREGISTRO.md` §7 y `PREREGISTRO_EJE3.md` §5: ninguna salida versionada lleva nucleótidos de
21 nt o más (el tamizado por siRNA trae la columna `sirna` y vive en `work/`); este eje no entra al diseño del
ARNdc (`D37`); y **toda cifra tomada de un paper lleva su referencia** (pedido del equipo): las citas
completas están en `resultados/referencias_recuperacion.tsv`.

## 6. Qué se miró antes de escribir

Sólo los identificadores, largos y verificaciones de organismo del paso anterior. **No se tamizó ninguna de
estas secuencias** ni se calculó ninguna fracción para ellas. Sí se conoce, por el paso 1 de este issue, que
`DE-03` contiene los cebadores del paper y que `CI-07` y `HE-04` no tienen secuencia.
