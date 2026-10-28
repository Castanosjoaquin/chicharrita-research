# F3 eje 3 — las seis filas de `C5` re-tamizadas contra el panel de seis

**Fecha: 2026-10-28.** Issue [#43](../../../../../issues/43). Criterio:
[`PREREGISTRO_EJE3_FILAS_NUEVAS.md`](../PREREGISTRO_EJE3_FILAS_NUEVAS.md) **enmienda 1**, commit `e166438`,
anterior a este cálculo. Script: [`11_eje_offtarget_filas_c5.py`](../scripts/11_eje_offtarget_filas_c5.py).
Salidas: `eje3_filas_c5.tsv`, `eje3_filas_c5_nulo.tsv`, `eje3_filas_c5_meta.json`. Máquina de Joaquín,
entorno `w5bio`. Secuencias: `research/ola3/C5_estructura_genes_ingenieria_inversa/resultados/candidatos_c5.fa`,
la que cada fila declara en `secuencia_usada`.

> **Lectura: `proxy_sustituto_declarado`.** La secuencia no es la de *D. maidis* ni la de la especie del
> catálogo: es la sustituta que `C5` eligió, de una tercera especie. **No es comparable** ni con las cinco filas
> `DM` (`eje3_REPORT.md`) ni con las cuatro recuperadas de papers (`eje3_filas_nuevas_REPORT.md`).

## El hallazgo: el autoacierto que el panel de cinco producía

Cuatro de las seis usan una secuencia de ***Macrosteles quadrilineatus***, y el panel de cinco de `C5`
**incluye** a *M. quadrilineatus*. Por eso esas filas publicaban el **100 % de sus ventanas** como coincidencia
perfecta contra esa referencia: era la secuencia coincidiendo consigo misma, no un off-target. El panel de seis
de `D76` no la incluye, y al quitarla queda esto `[M]`:

| fila | `C5` publicaba en *M. quadrilineatus* | fracción limpia con el panel de seis |
| --- | --- | ---: |
| `CI-03` | 1835/1835 (el 100 %) | 0,8943 |
| `CI-10` | 663/663 (el 100 %) | 0,9080 |
| `DE-02` | 1487/1487 (el 100 %) | 0,9644 |
| `DE-05` | 4409/4409 (el 100 %) | 0,9585 |

`[H]` No es un error de `C5`, que declaró la sustitución fila por fila; es lo que pasa cuando el panel contiene
la especie de la que se tomó prestada la secuencia. Es el mismo tipo de problema que `D83` ya había señalado:
el panel equivocado produce números plausibles, acá en la dirección pesimista.

## Resultado

Misma medida de `D97`: fracción de ventanas de 21 nt sin ningún bloque ≥19 nt idéntico en las seis referencias.
Nulo de 50 permutaciones por secuencia que conservan la composición, semilla `20261030`, mismo motor y panel.
**Control:** `eth_Dm` corrió en el mismo lote y reprodujo `work/sifi_v2/` en sus 595 ventanas, columna por
columna `[M]`; el script aborta si no.

| fila | gen | especie del catálogo | secuencia sustituta | ventanas | limpias | **fracción limpia** | nulo (mediana, rango) | frente al nulo |
| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `CI-01` | Rpn6 (segun los autores) | *Scaphoideus titanus* | `Rpn6_Stitanus_GJQL01135962` | 1.393 | 1.340 | **0,9620** | 0,9914 (0,9835–0,9978) | fuera del rango del nulo |
| `CI-02` | Rpn6 (segun los autores) | *Euscelidius variegatus* | `Rpn6_Evariegatus_GFTU01006765` | 1.463 | 1.418 | **0,9692** | 0,9938 (0,9815–1,0000) | fuera del rango del nulo |
| `CI-03` | ATP synthase beta | *Scaphoideus titanus* | `ATPsynBeta_Mquadrilineatus_XM_054410120` | 1.835 | 1.641 | **0,8943** | 0,9951 (0,9853–1,0000) | fuera del rango del nulo |
| `CI-10` | Nc-TnC (troponina C) | *Nephotettix cincticeps* | `TnC_Mquadrilineatus_XM_054409464` | 663 | 602 | **0,9080** | 0,9947 (0,9729–1,0000) | fuera del rango del nulo |
| `DE-02` | Ruvbl1 | *Peregrinus maidis* | `Ruvbl1_Mquadrilineatus_XM_054402769` | 1.487 | 1.434 | **0,9644** | 0,9899 (0,9818–1,0000) | fuera del rango del nulo |
| `DE-05` | XPO1 (exportina 1) | *Peregrinus maidis* | `XPO1_Mquadrilineatus_XM_054404977` | 4.409 | 4.226 | **0,9585** | 0,9882 (0,9794–0,9936) | fuera del rango del nulo |

### Cómo se lee

**Las seis quedan fuera del rango del nulo**, o sea que todas tienen más coincidencias que una secuencia sin
homología. Es el primer grupo donde pasa con todas, y conviene no sobreleerlo: el nulo mide si hay exceso sobre
el azar, no si el exceso importa. Las dos más marcadas son `CI-03` (0,8943 contra un mínimo del nulo de 0,9853)
y `CI-10` (0,9080 contra 0,9729); las otras cuatro quedan a menos de 0,03 de su mínimo.

| fila | maíz | *H. axyridis* | *A. mellifera* | *H. vitripennis* | *F. candida* | humano | con `perfecto_21` | con `mm1_21` | limpia sin humano |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `CI-01` | 0,0057 | 0,0000 | 0,0043 | 0,0129 | 0,0050 | 0,0122 | 0,0050 | 0,0510 | 0,9720 |
| `CI-02` | 0,0021 | 0,0000 | 0,0041 | 0,0123 | 0,0021 | 0,0123 | 0,0055 | 0,0738 | 0,9795 |
| `CI-03` | 0,0125 | 0,0000 | 0,0016 | 0,0676 | 0,0158 | 0,0223 | 0,0441 | 0,1956 | 0,9090 |
| `CI-10` | 0,0377 | 0,0060 | 0,0045 | 0,0498 | 0,0060 | 0,0151 | 0,0166 | 0,1750 | 0,9186 |
| `DE-02` | 0,0020 | 0,0047 | 0,0027 | 0,0121 | 0,0027 | 0,0121 | 0,0034 | 0,0525 | 0,9765 |
| `DE-05` | 0,0029 | 0,0016 | 0,0088 | 0,0188 | 0,0007 | 0,0091 | 0,0077 | 0,0889 | 0,9671 |

`[H]` El exceso viene sobre todo de *H. vitripennis* —cicadélido emparentado, donde una coincidencia es
esperable— y en `CI-10` también de **maíz** (3,8 % de sus ventanas con bloque ≥19 nt), que es la referencia que
más pesa para un cultivo. `CI-03` (ATP synthase beta) y `CI-10` (troponina C) son genes de función conservada, y
eso coincide en dirección con tener más coincidencias; no se midió la causa `[?]`.

## Qué le hace al orden

Las seis pasan a las cohortes nuevas **A+3** (`CI-01`, `CI-02`, `CI-03`) y **B+3** (`CI-10`, `DE-02`, `DE-05`).
Con `DE-01` y `DE-03`, esas cohortes quedan con cuatro candidatos cada una:

| cohorte | candidatos | primer puesto |
| --- | ---: | --- |
| A+3+4 (las cinco `DM`) | 5 | empate declarado `DM-05`, `DM-03`, `DM-02` — **sin cambios** |
| A+3 (ejes 1, 2 y 3, proxy) | 4 | empate declarado `CI-02` (0,8403), `CI-01` (0,8383), `DE-01` (0,8307), `CI-03` (0,8195) |
| B+3 (ejes 1 y 3, proxy) | 4 | `DE-02` (0,7771); después empate de `DE-03`, `DE-05`, `CI-10` |
| A (ejes 1 y 2) | 8 | empate de cinco en 0,5877 |
| B (solo eje 1) | 4 | empate de cuatro en 0,3300 |

1. **Las cinco filas `DM` no cambian**: verificado fila por fila contra la versión anterior `[M]`.
2. **La cohorte A perdió su empate de primer puesto**, como anticipó la enmienda: `CI-01`, `CI-02` y `CI-03` se
   fueron a A+3 y el primer puesto de A lo heredan `CI-04`, `CI-06`, `CI-07`, `DE-04` y `HE-02`, que **no
   ascendieron por mérito**: siguen en 0,5877, los mismos puntajes de antes. Lo mismo en B.
3. **El empate de A+3 es de los cuatro**, dentro de 0,021, muy por debajo del umbral de 0,05: el eje 3 **no
   ordena** entre ellos.
4. `segundo_orden` sigue en **sí** (el orden cambia según el objetivo) en las dos lecturas `[M]`, y las tres
   anclas de `F4` pasan. Los pesos de `D87` no se tocaron.

## Lo que no se hizo ni se concluye

- El catálogo de `C5` **no se editó**: sus columnas `panelC5_NO_es_el_de_seis__…` se siguen publicando fuera del
  puntaje. Lo que cambia es que ahora esas seis filas **también** tienen un valor contra el panel de seis.
- Sigue sin medirse el gen de la especie del catálogo: para cuatro de estas filas la secuencia es de una tercera
  especie, y recuperar la propia es parte de lo que queda del #43.
- Las seis referencias pesan igual (`D47`); el eje es el perfil de la molécula entera, no de la región elegida; y
  el nulo es un piso (no conserva uso de codones ni repeticiones).
- Ejecución: 110 lotes de unas 6.000 ventanas, 6 a la vez, 70 min.
