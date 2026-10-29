# V2 — Corrección: el gen que medí no es el del fenotipo publicado

**Veredicto: elegí la subunidad equivocada, y con la correcta el candidato deja de ser
equivalente a `BicC_Dm` 922-1221 — es peor en eficacia.** Esta corrección anula las conclusiones
de `REPORT.md` y `REPORT_ROBUSTEZ.md` sobre cuál contig es el candidato. Fecha: 2026-10-29,
posterior a los dos informes. El error lo encontré al rastrear el origen del gen, no una
verificación planificada; conviene decirlo así.

## 1. El error, y que el repo ya lo había anticipado

El paper lo llama **`Rpn6`**, y en la nomenclatura de UniProt el `Rpn6` de *Drosophila* es la
**subunidad 11** (`Q7KLV9`). Tomé ese nombre y recuperé la subunidad 11. **`C5` ya había medido que
eso es incorrecto para este gen**: traduciendo el transcrito publicado y comparándolo contra UniProt
con `blastx`, cae en **PSMD6 humano con 45,2 % de identidad sobre 409 aa** (E = 3·10⁻¹¹⁴) y en
**Rpn7 de *Drosophila* con 43,4 %**, contra apenas **20,4 % sobre 167 aa** para PSMD11/Rpn6
(`ingenieria_inversa.md` §3). La lección estaba escrita en `NOTAS_PARA_META.md` de `C5`:
*«resolver la identidad de un gen por secuencia antes que por nombre»*. No la apliqué.

**Verificación propia, con las dos especies del paper** (`tblastx`, transcrito publicado contra mis
dos CDS de *D. maidis*) `[M]`:

| Transcrito del paper | Alinea con | Identidad | Con `GITV01002940.1` |
| --- | --- | ---: | --- |
| `GJQL01135962.1` (*S. titanus*, `CI-01`) | **`GITV01002972.1`** | **96,73 %** sobre 398 aa | sin acierto (sólo ruido a E = 10) |
| `GFTU01006765.1` (*E. variegatus*, `CI-02`) | **`GITV01002972.1`** | **96,48 %** sobre 398 aa | sin acierto |

**El gen con el fenotipo publicado es `GITV01002972.1`** —la subunidad 6-like, PSMD6— que en los
informes anteriores figura como **control de parálogo**. `GITV01002940.1`, que presenté como
candidato, es la subunidad 11 y **no es el gen del paper**.

Que el control de parálogo resultara ser el candidato es, visto en frío, lo que el control estaba
diseñado para detectar; lo que falló fue que no miré su resultado a la luz de `C5`.

## 2. Los dos ejes del gen correcto

Mismo panel de seis, modo `corregido`, backend `vienna`, `NN3` `[M]`:

| | `GITV01002972.1` (correcto) | `GITV01002940.1` (el que presenté) |
| --- | ---: | ---: |
| CDS | 1.194 nt / 398 aa | 1.245 nt / 415 aa |
| Ventanas | 1.174 | 1.225 |
| Eficientes `fiel` / `corregido` | 81 (6,9 %) / 66 (5,6 %) | 104 (8,5 %) / 84 (6,9 %) |
| **Fracción limpia del gen (def. `F3`)** | **0,9796** | 0,9624 |
| **Ventanas con 21/21 perfecto** | **0** | 14 |
| Regiones de 300 nt admisibles | **777 de 777** | 680 de 828 |

El gen correcto es **más limpio** —cero coincidencias perfectas en todo el CDS, contra 14— y
**menos eficiente**. Contra los anclajes de `F3` (burs-alpha 1,0000 · eth 0,9815 · `BicC` 0,9660 ·
V-ATPase D 0,9639 · V-ATPase B 0,8827), su 0,9796 queda **segundo del panel**, detrás de
`burs-alpha` y empatando con `eth`.

## 3. La región, y la comparación que importa

Región elegida por la misma cascada: **345-644**. Marco molécula, `ranking.ejes()` oficial `[M]`:

| Objeto | Ventanas | Eficientes | Eficacia | Limpieza | Limpias y eficientes | Con acierto |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **`GITV01002972.1` 345-644** | 280 | 26 | 0,0929 | **0,9901** | **26** | 11 |
| `BicC_Dm` 922-1221 | 280 | 26 | 0,0929 | 0,9884 | 22 | 19 |

Pero el barrido desarma la igualdad aparente. Mismas 2.184 configuraciones, mismo motor de `M7`,
anclas de `BicC` 20 de 20 `[M]`:

| Marco | gana | empata | **pierde** | Dif. mediana |
| --- | ---: | ---: | ---: | ---: |
| recorte | 16,4 % | 4,3 % | **79,3 %** | **−5** |
| contexto | 3,1 % | 0,8 % | **96,1 %** | **−11** |

Con la regla del preregistro, **«misma eficacia que `BicC`» queda REFUTADA en los dos marcos**: el
empate de 26 a 26 del punto por defecto es un punto aislado, y en la grilla `BicC_Dm` 922-1221 gana
con holgura. La región sigue siendo **estable** (está entre las de máximo conteo en el **58,1 %** de
las configuraciones), y contra la región de máximo conteo sin veto del propio gen (47-346) gana en
recorte el 88,6 %.

## 4. El nulo del gen correcto

**N1, gen:** fracción limpia **0,9796** contra un nulo de mediana 0,9949 y rango 0,9830–1,0000 →
**fuera del rango**. Hay homología real `[M]`.

**N2, región:** limpieza **0,9901** contra un nulo de mediana 0,9974, intercuartílico 0,9936–0,9991
y percentil 5 en 0,9852. El observado cae en el **percentil 9,8** `[M]`. No llega al umbral de
«exceso sobre el azar» (p5) ni queda dentro del intercuartílico: **la región es algo más sucia que
la región típica del azar**, no más limpia. La ventaja aparente de 0,9901 contra 0,9884 **no se
sostiene**.

Un matiz que vale: en el gen real **ninguna** región de 300 nt trae una coincidencia perfecta de
21 nt (0,00 %), contra **1,19 %** en el nulo. Las coincidencias duras están por debajo del azar; lo
que empuja la limpieza hacia abajo son los aciertos con un desapareo (`mm1_21`, peso 0,30).

## 5. Qué queda en pie

**En pie `[M]`:** el gen del fenotipo publicado existe en *D. maidis* (`GITV01002972.1`, 96,7 % con
el transcrito del paper); es **el segundo gen más limpio del panel** y **no tiene una sola
coincidencia perfecta de 21 nt en todo el CDS**; su región 345-644 es estable en el 58,1 % de la
grilla; y los dos transcritos del paper, de dos géneros distintos, aterrizan en el mismo contig.

**Caído:** ~~«`Rpn6` iguala a `BicC_Dm` 922-1221»~~. Con el gen correcto, **`BicC_Dm` gana en
eficacia** (79,3 % y 96,1 % de las configuraciones) y la limpieza de la región no es mejor de forma
distinguible (percentil 9,8 del nulo). **`Rpn6` no es un candidato equivalente: es un candidato
más limpio a nivel gen y menos eficaz a nivel región.**

**Y un límite que ahora pesa más:** la **vuelta recíproca de `GITV01002972.1` NO cierra** — cuatro
aciertos con puntajes casi iguales (819, 816, 813, 813 en *M. quadrilineatus*; 781, 781, 780, 780
en *H. vitripennis*). Cuando era el control eso era el resultado esperado; como candidato, es una
ortología sin confirmar. Además su ORF mide 1.025 aa y excede la consulta de 426, así que el CDS se
acotó al tramo alineado.

## 6. Lo que esto no cambia

La recomendación defendida del proyecto sigue siendo **`BicC_Dm` 922-1221**, y esta corrección la
**refuerza** en vez de debilitarla. El eje de fenotipo sigue medido en *S. titanus* y
*E. variegatus*. Ninguna de las dos regiones de `Rpn6` está en el inventario de alertas de `M6`.

## 7. Decisión candidata para `00_meta/`

**Antes de recuperar un gen publicado, resolver su identidad por secuencia y no por nombre, aunque
el nombre venga del paper.** `C5` ya lo había propuesto y lo midió sobre este mismo gen; esta línea
es la prueba de que sin un paso explícito la lección no se aplica sola. Propuesta concreta: que el
preregistro de toda recuperación incluya un `blastx` del transcrito publicado contra UniProt como
**ancla que aborta**, al mismo nivel que la verificación de traducción.
