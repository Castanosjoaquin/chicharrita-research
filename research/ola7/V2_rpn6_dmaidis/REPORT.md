# V2 — `Rpn6` recuperado en *D. maidis*: la región gana a `BicC_Dm` 922-1221 en los dos ejes

**Veredicto: el gen existe en *D. maidis*, y la región que elige la cascada iguala a
`BicC_Dm` 922-1221 en eficacia y la supera en limpieza — pero la ortología no está
confirmada y el eje de fenotipo sigue medido en otra especie.** Criterio en
[`PREREGISTRO.md`](PREREGISTRO.md), commiteado (`486aeb1`, 2026-10-29 18:20:42 -0300)
**antes** del primer cálculo. Fecha de corrida: 2026-10-29. Ninguna secuencia salió de la
máquina: el transcriptoma y las seis referencias se leyeron de disco.

## 1. El control del §2 pasa, y acota qué se midió

| Contig | Hebra | ORF | Tramo que alinea | Identidad | Consulta |
| --- | :-: | ---: | ---: | ---: | --- |
| `GITV01002940.1` (4.059 nt) | + | 415 aa | **415 aa / 1.245 nt** | **97,11 %** sobre 415 | `XP_054288549.1`, subunidad **11** |
| `GITV01002972.1` (3.584 nt) | − | 1.025 aa | 398 aa / 1.194 nt | 97,49 % sobre 398 | `XP_054282698.1`, subunidad **6-like** |

`[M]` `GITV01002940.1` alinea **de punta a punta** con la consulta (415 de 415 aa), que es el
caso limpio. `GITV01002972.1` tiene un ORF de 1.025 aa que **excede** la consulta: el CDS se
acotó al tramo alineado, y eso queda como límite —no se sabe si el ORF largo es una lectura
corrida del ensamblado o una fusión real.

**Cuál es «`Rpn6`».** El catálogo dice `Rpn6 (según los autores)`. `C11` midió que lo que
*Drosophila* llama `Rpn6` resuelve a **PSMD11** y lo que llama `Rpn7` resuelve a PSMD6. Por esa
cadena, el gen con el fenotipo publicado es **`GITV01002940.1`** (subunidad 11) y
`GITV01002972.1` entró como **control de parálogo**, no como candidato. `[H]` la cadena de
nomenclaturas; `[M]` las identidades.

## 2. Los dos ejes del gen entero

Panel de seis con el humano a peso 1,00, `--size 21 --min-block 19 --mm1`, modo `corregido`,
backend `vienna`, `NN3`, 22 °C `[M]`:

| | `GITV01002940.1` (subunidad 11) | `GITV01002972.1` (subunidad 6-like) |
| --- | ---: | ---: |
| Ventanas | 1.225 | 1.174 |
| Eficientes, `fiel` / `corregido` | 104 (8,5 %) / 84 (6,9 %) | 81 (6,9 %) / 66 (5,6 %) |
| **Fracción limpia** | **0,9624** | **0,9796** |
| **Ventanas con 21/21 perfecto (veto)** | **14** | **0** |
| Regiones de 300 nt admisibles | 660 de 808 | 757 de 757 |

**Las 14 ventanas vetadas de la subunidad 11 son todas contra *H. vitripennis*** (26 bloques
≥19 nt y 14 perfectos de 21). Contra humano son 6 bloques ≥19 nt y **cero** perfectos; contra
maíz 3 y cero `[M]`. El control de parálogo, en cambio, **no tiene una sola coincidencia
perfecta en todo el panel**.

Leído contra los anclajes de `F3` (burs-alpha 1,0000 · eth 0,9815 · `BicC` 0,9660 ·
V-ATPase D 0,9639 · V-ATPase B 0,8827): la subunidad 11 cae en **0,9624**, apenas por debajo de
`BicC` y de V-ATPase D, y muy por encima de V-ATPase B. El §5 del preregistro nombró las dos
puntas y no esta banda intermedia; se reporta como lo que es y no se fuerza a una casilla.

## 3. La región, y la comparación que el preregistro autorizó

Cascada de 300 nt, veto duro por 21/21 contra el panel, bandas de 59 nt de los extremos
excluidas. Marco 3 (`D63`): la molécula recortada, que es la cifra que se publica `[M]`.

| Objeto | Ventanas | Eficientes | Eficacia | Limpieza | Limpias y eficientes | Veto |
| --- | ---: | ---: | ---: | ---: | ---: | :-: |
| **`GITV01002940.1` 325-624** | 280 | **26** | **0,0929** | **1,0000** | **26** | no |
| `GITV01002972.1` 345-644 | 280 | 26 | 0,0929 | 0,9857 | 26 | no |
| `BicC_Dm` 922-1221 (publicado) | 280 | 26 | 0,0929 | 0,9884 | 22 | no |

`[M]` **Las tres regiones dan 26 eficientes de 280 ventanas.** La coincidencia es exacta en los
tres casos y no significa nada: 280 es el número de ventanas de cualquier molécula de 300 nt, y
26 salió tres veces. Se reporta como coincidencia.

`[M]` **La región 325-624 de la subunidad 11 tiene limpieza 1,0000** —ninguna de sus 280
ventanas tiene un bloque de 19 nt o más en ninguna de las seis referencias— contra 0,9884 de
`BicC_Dm` 922-1221, y **26 de 26 ventanas eficientes son además limpias**, contra 22 de 26.
Con la misma eficacia, en los dos ejes del ranking medidos igual, **la región nueva gana**.

`[H]` Y el patrón repite la tesis del proyecto: el **gen** es más sucio que el de `BicC`
(0,9624 contra 0,9660) y la **región** es más limpia (1,0000 contra 0,9884). Lo que limpia no
es cambiar de gen, es mover la región dentro del gen.

## 4. Lo que este resultado NO autoriza a decir

1. **La ortología no está confirmada.** Es la ida sin la vuelta: no se corrió la recíproca desde
   la proteína predicha en *D. maidis* contra el transcriptoma del pariente. `GITV01002940.1`
   podría ser un parálogo de la subunidad 11 y no su ortólogo.
2. **Los aciertos secundarios siguen sin resolver**: `GITV01001189.1` (98,6 % sobre 277 aa),
   `GITV01003958.1` (96,0 % sobre 225) y, para el control, `GITV01002452.1` y
   `GITV01004786.1`. No se sabe si son fragmentos del mismo transcripto, isoformas o parálogos.
3. **El eje 1 no se movió y pesa 0,40.** El fenotipo de `Rpn6` —ovarios sin huevos, progenie de
   0,03 ninfas por día de oviposición contra 1,5, supervivencia menor que el control de dsGFP—
   está medido en *S. titanus* y *E. variegatus*, **no** en *D. maidis*. Esta línea movió los
   ejes 3 y 4; el 1 se cierra con un bioensayo, no con cómputo. `[R]`
4. **No se recalculó el puntaje de `F3`** ni se puso a este gen en la cohorte `A+3+4`, que es lo
   que el §4 del preregistro prohíbe.
5. **El criterio de eficiencia sigue sin validar** (ρ = +0,142, IC95 [−0,247; +0,492], n = 29).
   Las 26 ventanas son una hipótesis sobre eficacia, no una prueba.
6. **La región no está en el inventario de alertas de `M6`**, así que la compuerta de `D72` la
   rechaza como recomendación. Es un resultado de medición, no una región recomendada.
7. El contig viene de un TSA: no hay estructura exónica que verificar, y el eje 4
   (conservación entre los tres transcriptomas) **no se corrió**.

## 5. Reproducibilidad

El CDS **no se versiona** —`sin_secuencias.py` rechaza toda racha de 21 nt— y se regenera desde
`work/W5/ref/TSA_GITV01.fasta` tomando `GITV01002940.1`, traduciendo los seis marcos, eligiendo
el ORF de mayor puntaje contra `XP_054288549.1` y acotándolo al tramo alineado. Las seis
referencias están en `work/R8/db/`. Salidas de la corrida en `work/V2/`, no versionado.
