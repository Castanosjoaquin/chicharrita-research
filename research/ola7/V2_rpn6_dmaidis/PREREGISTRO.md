# V2 — Preregistro: recuperar `Rpn6` en *D. maidis* y medirle los dos ejes

**Escrito y commiteado ANTES del primer cálculo.** Fecha: 2026-10-29.
ID provisorio. Motivo: `F3` dejó a `Rpn6` primero de su cohorte (0,8403 y 0,8383) pero en la
cohorte `A+3`, con el eje 3 calculado sobre **secuencia sustituta**. Hoy `tblastn` encontró el
gen en el transcriptoma de *D. maidis* al 97 % de identidad proteica. Esta línea recalcula los
ejes 3 y 4 sobre la secuencia propia para ver si sube a la cohorte comparable.

## 1. Insumos, fijados

- Contigs, que son los mejores aciertos de `tblastn` ya corridos y no se re-eligen:
  `GITV01002972.1` (3.584 nt, subunidad 6-like, 97,5 % sobre 398 aa) y
  `GITV01002940.1` (4.059 nt, subunidad 11, 97,1 % sobre 413 aa).
- Proteínas de consulta: `XP_054282698.1` y `XP_054288549.1` de *M. quadrilineatus*.
- Panel de seis de `PREREGISTRO.md` de O3 §2.4, en `work/R8/db/`: humano, maíz,
  *H. vitripennis*, *H. axyridis*, *F. candida*, *A. mellifera*. El humano pesa 1,00.
- Motor: `run_sifi.py`, backend `vienna` (ViennaRNA 2.7.2), tabla `NN3`, 22 °C.

## 2. El control que autoriza a seguir, y aborta si falla

El ORF se extrae del contig y **se traduce**. Si la traducción no alinea con la proteína de
consulta con al menos **95 % de identidad** sobre la región que `tblastn` reportó, la línea
**para** y no se lee ningún número de eficiencia ni de off-target. Un contig de TSA puede ser
un fragmento o una quimera de ensamblado; sin este control no se sabe cuál.

## 3. Qué se calcula, en este orden

1. Perfil de eficiencia del CDS entero, en los **dos modos** (`fiel` y `corregido`).
2. Tamizaje contra el panel de seis: `--size 21 --min-block 19 --mm1`.
3. Fracción limpia = ventanas sin ningún bloque ≥19 nt en ninguna de las seis, sobre todas las
   ventanas. Misma definición que el eje 3 de `F3`, para que sea comparable.
4. Región de **300 nt** por cascada, con **veto duro** por coincidencia perfecta de 21 nt
   contra el panel, igual que O3 §2. Se excluyen de antemano las bandas de 59 nt de los dos
   extremos del CDS.
5. Los tres marcos de conteo de `D63`. La cifra que se publica es la del marco 3.

## 4. Las comparaciones permitidas, y la prohibida

Se compara contra **`BicC_Dm` 922-1221** —26 eficientes en la molécula, 0 coincidencias
perfectas con el panel, limpieza 0,9884— y contra los anclajes de eje 3 de `F3`
(burs-alpha 1,0000 · eth 0,9815 · BicC 0,9660 · V-ATPase D 0,9639 · V-ATPase B 0,8827).

**Prohibido:** recalcular el puntaje de `F3` y ponerlo en la misma columna que los genes de la
cohorte `A+3+4`. El eje 1 (fenotipo, peso 0,40) **no cambia** con esta línea: sigue medido en
*S. titanus* y *E. variegatus*. Esta línea mueve los ejes 3 y 4, nada más.

## 5. Qué resultado cuenta como cuál

- **Si quedan cero regiones admisibles de 300 nt:** ése es el resultado y se reporta así. Es el
  desenlace de `V-ATPase B`, que dejó una sola de 1.184.
- **Si la fracción limpia cae por debajo de 0,8827** (la de `V-ATPase B`): el gen es el peor del
  panel en especificidad y no se propone.
- **Si queda por encima de 0,9660** (la de `BicC`) **y hay región admisible:** es un candidato
  real cuyo único eje flojo es el fenotipo en otra especie, y se dice exactamente así.

## 6. Límites declarados de antemano

- Es la **ida** sin la vuelta: no se corre la recíproca desde la proteína predicha en
  *D. maidis* contra el transcriptoma del pariente. La ortología queda **no confirmada**.
- Los aciertos secundarios de `tblastn` (`GITV01002452.1`, `GITV01001189.1`,
  `GITV01003958.1`, `GITV01004786.1`) no se resuelven: no se sabe si son fragmentos del mismo
  transcripto, isoformas o parálogos.
- El contig es de un TSA, no de un genoma anotado: no hay estructura exónica que verificar.
- El criterio de eficiencia sigue sin validar (ρ = +0,142, IC95 [−0,247; +0,492], n = 29).
- `Rpn6` es nombre de los autores. `C11` midió que ese nombre resuelve a proteínas distintas
  según la base; acá el gen se identifica por la proteína de consulta y su contig, no por nombre.
