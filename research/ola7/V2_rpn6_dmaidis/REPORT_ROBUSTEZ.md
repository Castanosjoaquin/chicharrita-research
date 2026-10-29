# V2 — Robustez y nulo de `Rpn6` 325-624: aguanta la grilla, y su ventaja de limpieza no se distingue del azar

> ## ⚠ CORREGIDO — leer [`REPORT_CORRECCION_IDENTIDAD.md`](REPORT_CORRECCION_IDENTIDAD.md) primero
>
> El gen que este informe trata como candidato, `GITV01002940.1` (subunidad 11), **no es el del
> fenotipo publicado**. Elegí por nombre y no por secuencia: el paper lo llama `Rpn6` y en
> *Drosophila* ese nombre es la subunidad 11, pero `C5` ya había medido que la secuencia del gen
> silenciado es **PSMD6**. Verificado con `tblastx`: los transcritos del paper en *S. titanus* y
> *E. variegatus* alinean al **96,7 %** y **96,5 %** con `GITV01002972.1` —el que acá figura como
> control de parálogo— y **no** con `GITV01002940.1`. Con el gen correcto, `BicC_Dm` 922-1221
> **gana en eficacia** (79,3 % y 96,1 % de las configuraciones) y la ventaja de limpieza no se
> sostiene (percentil 9,8 del nulo). Todo lo que estos informes dicen de `GITV01002940.1` sigue
> siendo una medición válida **de la subunidad 11**, que no es el candidato.



**Veredicto: la región aguanta el barrido de parámetros y la elección es estable, pero el nulo
desarma el argumento de limpieza — la ventaja de 0,9910 contra 0,9884 cae en el percentil 51,6
del azar.** Criterio en [`PREREGISTRO_ROBUSTEZ.md`](PREREGISTRO_ROBUSTEZ.md), commiteado
(`1f63ad8`, 2026-10-29 18:41:22 -0300) **antes** de calcular nada de esto. Scripts:
[`01_robustez_rpn6.py`](scripts/01_robustez_rpn6.py),
[`02_fuentes_y_criterios.py`](scripts/02_fuentes_y_criterios.py),
[`03_nulo.py`](scripts/03_nulo.py). El motor de `M7` se importa **sin tocarlo**.

## 1. Las anclas del §2 pasan

- Las de `grilla_parametros.anclas()` sobre los cuatro genes de `W5`: 142/39/223/35 en `fiel` y
  123/30/171/29 en `corregido`, más las cuatro regiones vigentes (38, 21, 36, 21) `[M]`.
- `verificar_vectorizacion()` sobre el gen de `Rpn6` y su región recortada `[M]`.
- **Reproducción de `BicC`: 20 de 20 filas** de `grilla_parametros.tsv` recalculadas con el motor
  local coinciden, en los dos marcos `[M]`. Sin esto no se habría leído ningún número de `Rpn6`.
- **`RNAplfold 2.1.5`: NO CORRIDO.** El único binario del repo es el `.exe` de Windows. El eje del
  motor queda declarado, no en cero. De los cinco ejes de `M7`, éste barre cuatro:
  **2.184 configuraciones** (21 brechas × 26 accesibilidades × 2 modos × 2 tablas, sólo `vienna`).

## 2. P1 — La eficacia frente a `BicC_Dm` 922-1221 depende del marco, y hay que decirlo así

Comparación configuración por configuración, contra las cifras publicadas de `M7` `[M]`:

| Marco | n | `Rpn6` gana | empata | pierde | Dif. mediana | Rango |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| **recorte** (la molécula que se sintetizaría, `D63`) | 2.184 | **64,1 %** | 6,4 % | 29,4 % | **+3** | −14 a +13 |
| **contexto** (ventanas que arrancan en la región) | 2.184 | 32,1 % | 8,0 % | **59,9 %** | **−2** | −18 a +8 |

Con la regla escrita antes: en **recorte**, `Rpn6` gana o empata en el **70,5 %** — «misma eficacia
que `BicC`» queda **sostenida**. En **contexto**, `BicC` gana en el 59,9 %, más de la mitad —
queda **refutada**. **El veredicto depende del marco de conteo**, que es exactamente el eje de
decisión que `N3` y `D63` declararon y que el proyecto arrastra desde entonces.

Por cortes, en marco recorte: modo `corregido` 73,9 % y modo `fiel` 54,4 %; `NN3` 63,3 % y `NN4`
65,0 % —la tabla de apilamiento no mueve nada—. **En el punto por defecto exacto** (brecha 1,0,
accesibilidad 0,1) `Rpn6` **pierde** en recorte: 26 contra 28 en `corregido` y dif −2. O sea: la
ventaja del 64,1 % **no incluye el punto que el proyecto usa por defecto**, y conviene decirlo
antes de que lo pregunten `[M]`.

## 3. P2 — La elección de la región es estable

De las **828** posiciones de inicio admisibles por borde, **680** no tienen ninguna ventana con
coincidencia perfecta de 21 nt contra el panel de seis. En cada configuración se buscó si 325-624
está entre las de **máximo conteo**, empates incluidos `[M]`:

- **1.478 de 2.184 configuraciones (67,7 %)** → **estable** con la regla del §3 (≥ 50 %).
- La **brecha mediana** entre el máximo y el conteo de 325-624 es **0**.
- Cuando no está en el máximo, los reemplazos más frecuentes son 497-796 (113 veces), 312-611 (80),
  513-812 (76) y 309-608 (72). **Son dos vecindarios**: uno pegado a 325 y otro alrededor de 500.

## 4. P3 — Lo que cuesta el veto, contra la región de máximo conteo

El rival es **309-608**, la de máximo conteo sin veto en el punto por defecto (30 eficientes en
contexto) `[M]`:

| Marco | `Rpn6` 325-624 gana | empata | pierde |
| --- | ---: | ---: | ---: |
| contexto | 12,0 % | **78,2 %** | 9,9 % |
| recorte | 59,8 % | 25,7 % | 14,4 % |

`[H]` En contexto las dos son indistinguibles en el 78 % de la grilla: **el veto casi no cuesta
eficacia en este gen**, al revés de lo que pasó con `V-ATPase B`, donde dejó una sola región de
1.184.

## 5. P4 — La secuencia de las otras dos fuentes cambia el conteo, poco

Los 300 nt tal como los escriben los dos contigs, con los dos extremos hallados y largo 300 `[M]`:

| Fuente | Hebra | Posiciones distintas de 300 | Eficientes (`corregido`) | Conservadas | Perdidas | Ganadas |
| --- | :-: | --- | ---: | ---: | ---: | ---: |
| `GITV01` (la propia) | — | — | 26 | — | — | — |
| `GHCC01050726.1` (Argentina) | + | **21 y 261** | **25** | 23 | 3 | 2 |
| `GCWP01019967.1` (Illinois) | − | **21 y 261** | **25** | 23 | 3 | 2 |

`[M]` Las dos fuentes dan **exactamente el mismo resultado**, y son las dos posiciones sinónimas de
`REPORT.md` §3ter. En modo `fiel`: 30 → 29, con 27 conservadas. La elección de fuente mueve **una
ventana** sobre 26.

## 6. P5 — Todo el riesgo de la región es de un solo criterio, el más débil

| Criterio activo | Limpieza conservadora | Mecanicista | Limpias y eficientes | Ventanas con acierto |
| --- | ---: | ---: | ---: | ---: |
| sólo `perfecto_21` | **1,0000** | 1,0000 | 26 | **0** |
| sólo `perfecto_ge19` | **1,0000** | 1,0000 | 26 | **0** |
| `perfecto_21` + `ge19` (sin `mm1`) | **1,0000** | 1,0000 | 26 | **0** |
| **los tres (oficial)** | **0,9910** | 0,9989 | 25 | **12** |
| `BicC_Dm` 922-1221 (`O3`) | 0,9884 | 0,9974 | 22 | 19 |

`[M]` **Los 12 aciertos de la región son todos `mm1_21`** —un desapareo— y el peso de ese criterio
es 0,30, el más bajo de los tres. Cero coincidencias perfectas de 21 nt y **cero bloques de
≥ 19 nt** contra las seis referencias. Bajo los dos criterios que `D28` considera duros la
limpieza es **1,0000**; toda la diferencia con 1 la aporta el criterio más laxo.

## 7. El nulo, que es el resultado que hay que llevar

**N1, nivel gen.** Fracción limpia observada **0,9624** contra un nulo de 50 permutaciones con
mediana 0,9882 y rango **0,9739–0,9976** `[M]`. **Fuera del rango del nulo**: el gen tiene un
exceso real de coincidencias sobre el azar, igual que `BicC` (0,9660) y `V-ATPase B` (0,8827) en
`F3`. Es homología, no ruido.

**N2, nivel región — y éste desarma el argumento de §0.** La limpieza de 325-624 es **0,9910**;
el nulo de **todas** las regiones de 300 nt de las 50 permutaciones tiene mediana **0,9908**,
rango intercuartílico **0,9846–0,9949** y percentil 5 en 0,9756. El observado cae en el
**percentil 51,6** `[M]`.

`[M]` Con la regla escrita antes de medir —«no distinguible del azar si queda dentro del rango
intercuartílico»—: **la limpieza de la región no se distingue del azar.** Y como `BicC_Dm`
922-1221 está en 0,9884, también dentro de ese rango, la conclusión es más fuerte y más útil:
**la diferencia de limpieza entre las dos regiones, 0,0026, es menor que la dispersión del propio
azar, y no sostiene ninguna preferencia.**

`[M]` Lo que sí se distingue: **en el nulo, el 9,26 % de las regiones trae alguna ventana con
coincidencia perfecta de 21 nt; en el gen real, el 17,87 %.** El veto tiene una tasa base no nula
—como `F3` ya había medido— y el gen real casi la duplica, lo que es coherente con N1.

**Límite declarado antes:** el nulo conserva composición de mononucleótidos pero no uso de codones
ni repeticiones, así que es un **piso** y no una cota.

## 8. Qué queda en pie, y qué no

**En pie `[M]`:** el gen existe en *D. maidis* con ortología recíproca cerrada; la región 325-624
es estable frente a 2.184 configuraciones (67,7 %); su eficacia iguala o supera a la de `BicC` en
el 70,5 % de la grilla **en marco recorte**; no tiene ni una coincidencia perfecta de 21 nt ni un
bloque de ≥ 19 nt contra el panel de seis; el gen entero tiene homología real sobre el azar; y la
elección de fuente mueve una ventana sobre 26.

**Ya no en pie:** ~~«la región gana a `BicC_Dm` en limpieza»~~. La ventaja es de 0,0026 y cae
dentro de la dispersión del azar (percentil 51,6). Lo correcto es **«las dos regiones son
indistinguibles en limpieza, y ninguna tiene coincidencias duras»**.

**Sin cambios:** el eje 1 de `F3` (fenotipo, peso 0,40) sigue medido en *S. titanus* y
*E. variegatus*; el criterio de eficiencia sigue sin validar (ρ = +0,142, n = 29); la región no
está en el inventario de alertas de `M6`, así que la compuerta de `D72` la rechaza como
recomendación; y nada de esto recalcula el puntaje de `F3` ni mueve a `Rpn6` de cohorte.

`[H]` **La lectura honesta del conjunto:** `Rpn6` 325-624 es un candidato **equivalente** a
`BicC_Dm` 922-1221 en los dos ejes que sabemos medir, no superior. Lo que lo distingue no es un
número del ranking sino el **mecanismo** —reproducción y letalidad, contra reproducción sola— y lo
que le falta es el mismo bioensayo que a todos.
