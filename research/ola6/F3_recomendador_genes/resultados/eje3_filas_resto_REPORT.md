# F3 eje 3 — segunda vuelta de recuperación: tres filas más, y un segundo autoacierto

**Fecha: 2026-10-28.** Issue [#43](../../../../../issues/43). Criterio:
[`PREREGISTRO_EJE3_FILAS_NUEVAS.md`](../PREREGISTRO_EJE3_FILAS_NUEVAS.md) §0–§3 **sin cambios**: es el mismo caso
que ese documento ya cubría (fila recuperada del paper, secuencia de la especie del paper,
`proxy_especie_del_paper`). Script: [`13_eje_offtarget_resto.py`](../scripts/13_eje_offtarget_resto.py). Salidas:
`eje3_filas_resto.tsv`, `eje3_filas_resto_nulo.tsv`, `eje3_filas_resto_meta.json`. Las accesiones y su
procedencia salen de [`recuperacion_resto_REPORT.md`](recuperacion_resto_REPORT.md), con las referencias
completas de cada paper. Control: `eth_Dm` reproduce `work/sifi_v2/` en sus 595 ventanas, columna por columna `[M]`.

## Lo primero: un segundo autoacierto, y ahora es una regla

`HE-06` es **actina de *Homalodisca vitripennis***, y *H. vitripennis* es **una de las seis referencias del
panel**. Su fracción limpia es **0,0054**: el 98,6 % de sus ventanas coincide con esa referencia `[M]`. No es
riesgo, es la secuencia contra sí misma, igual que el caso de *M. quadrilineatus* de `D99`. **La fila queda con el
valor publicado y rotulado, y fuera del puntaje** (columna `autoacierto_especie_en_el_panel`); `03_orden.py` la
excluye por esa columna, no a mano.

`[H]` Dos casos en dos vueltas dejan de ser casualidad. **Regla para lo que venga: antes de tamizar una
secuencia, comprobar que su especie no esté en el panel.** Es barato y los dos casos lo habrían atrapado.

## Resultado de las otras tres

| fila | gen | accesión | de dónde salió la accesión | ventanas | **fracción limpia** | nulo (rango) | frente al nulo |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| `HE-07` | NcSP75 | `LC009512.1` | el paper cita la proteina BAQ94503; su propio regist | 2.256 | **0.9597** | 0.9660–0.9934 | fuera del rango del nulo |
| `HE-10` | varios | `MF101769.1` | Tabla 1 del paper. accesion por gen | 1.981 | **0.9561** | 0.9864–1.0000 | fuera del rango del nulo |
| `CI-06` | ATP synthase beta (efect | `GFTU01013594.1` | metodos 2.2 del paper (TSA. BioProject PRJNA393620) | 2.034 | **0.8820** | 0.9872–1.0000 | fuera del rango del nulo |

Las tres quedan **fuera del rango de su nulo**, o sea con más coincidencias que el azar. `CI-06` es la más
marcada (0,8820), y su exceso viene sobre todo de *H. vitripennis* (8,2 % de sus ventanas) `[M]`: es ATP synthase
beta, un gen de función muy conservada, y *E. variegatus* y *H. vitripennis* son los dos cicadélidos. `HE-07` y
`HE-10` quedan cerca de su nulo (0,9597 y 0,9561 contra mínimos de 0,9660 y 0,9864).

**`HE-05` no se pudo usar**, aunque su paper sí cita accesión: `KQ034133` es un **andamio genómico de 1,8 Mb**
de *Rhodnius prolixus*, no un transcripto (el paper dice que el ARNm no está depositado). Extraer el gen de ahí
sería elegirlo por anotación, que es lo que el equipo descartó. Queda con el eje ausente y el motivo escrito.

**`HE-07` tiene una vuelta que vale explicar.** Su paper cita `BAQ94503`, que es una accesión de **proteína**. El
nucleótido salió del propio registro de NCBI de esa proteína, que declara `coded_by LC009512.1` `[M]`: es un
enlace del registro, no una búsqueda por nombre de gen, así que respeta la regla.

## Qué le hace al orden

`HE-06` y `HE-10` están **fuera del orden** (`sin_fenotipo_publicado`) y su eje 3 se publica sólo acá. Las dos que
sí están pasan de cohorte:

- **`CI-06`** sale de la cohorte A y entra a **A+3**, en el puesto 5 con 0,6694. Era parte del empate de cinco del
  primer puesto de A; al irse, ese empate queda en cuatro.
- **`HE-07`** sale de B y entra a **B+3** con 0,5722, dentro del empate de `DE-03`, `DE-05` y `CI-10`.
- **Las cinco filas `DM` no se mueven** `[M]`, los pesos de `D87` no se tocan, `segundo_orden` sigue en «sí» y las
  tres anclas de `F4` pasan.

## Cobertura final del eje 3, declarada

**19 de las 36 filas del catálogo tienen secuencia** (`manifiesto_secuencias_eje3.tsv`), y **18 tienen un valor de
eje 3 que entra al puntaje** —`HE-06` queda afuera por autoacierto—, en tres lecturas que **no se comparan entre
sí**: 5 `D_maidis`, 7 `proxy_especie_del_paper` y 6 `proxy_sustituto_declarado`.

Las 17 filas sin secuencia quedan **declaradas, no rellenadas**, que es lo que el equipo decidió. Pero el motivo
no es el mismo en todas, y la diferencia importa:

| situación | filas | qué significa |
| --- | --- | --- |
| el paper no trae accesión, **texto completo leído** | `HE-04`, `CI-07`, `CI-08` | ausencia comprobada |
| **sólo se leyó el resumen** (muro de pago) | `HE-01`, `HE-02`, `HE-03`, `HE-09`, `HE-11`, `DM-04`, `CI-09`, `CI-11`, `CI-12` | **provisional**: «no está en el resumen» no es «no está en el paper» |
| sin texto ni resumen | `HE-08` | la fila no nombra un gen (es el control de dosis) |
| **bloqueadas por la red** | `CI-04`, `CI-05` (`iris.unito.it`), `DE-04` (`onlinelibrary.wiley.com`) | el PDF es abierto pero el dominio no está en la lista permitida |
| accesión citada pero no usable | `HE-05` | andamio genómico, no transcripto |

`[?]` **Las nueve provisionales no son un hallazgo de ausencia**, y no deben leerse como que esos papers no
depositaron secuencias. Para cerrarlas hace falta el texto completo. Las tres bloqueadas se destraban autorizando
dos dominios.
