# Ola 5 — lo que fue a `00_meta/`, ya aplicado

A diferencia de la ola 4, esta ola **no deja notas pendientes de volcar**: los cinco archivos de
`00_meta/` se actualizaron en la misma pasada, que es lo que pide `CLAUDE.md`. Esto es el índice de
qué entró y dónde, para poder auditarlo.

## `DECISIONS.md`

| ADR | Qué decide |
|---|---|
| **D62** | La discrepancia de los cuatro conteos es de la función de conteo, no de la termodinámica. Retira la hipótesis del conteo por aciertos de Bowtie como causa, sin retirarla como hallazgo. Deja abierto con qué tabla de apilamiento corre el método histórico. |
| **D63** | Cada conteo se publica con su marco declarado, y hay tres marcos con nombre. La cifra de una región candidata es la de la molécula recortada. |
| **D64** | La razón escrita de D25 se reemplaza por la cobertura declarada por fuente. La decisión de recomendar 922-1221 no se revierte. |
| **D63**, nota de aplicación | el marco intermedio cruzado con la grilla y con el eje de referencia: el marco cambia cuánta sensibilidad tiene el conteo a todo lo demás, no sólo su valor. |
| **D65** | El conteo de eficientes deja de ser argumento entre 922-1221 y 2121-2420: tres mediciones independientes lo vuelven un empate. Lo que sostiene la preferencia es el off-target y la conservación por fuente. Contra 264-563 nada de esto aplica. |

## `CAMINOS_PROBADOS.md`

Tres entradas, y las tres tienen lección:

1. **Explicar los cuatro conteos con el conteo por aciertos de Bowtie** — descartado como causa. La
   lección es la que más rinde: una explicación candidata que acierta una de cuatro cosas con error
   de uno no está «casi bien», está sin confirmar.
2. **Corregir a 20 el ancho de cobertura de nuestra curva** — descartado: son dos curvas distintas,
   y la nuestra reproduce la del original.
3. **Pedirle al laboratorio la clasificación por ventana** — retirado por innecesario. Un pedido de
   datos se justifica por la pregunta que contesta; cuando la pregunta se cierra, el pedido se
   retira en vez de quedar en la lista.

## `PREGUNTAS_ABIERTAS.md`

Una entrada fechada el 2026-10-25 con el saldo de la carta: tres preguntas que se cierran, dos que
siguen abiertas —los FASTA de los índices y la regla terminal— y **ocho nuevas**, de las cuales
cuatro son pedidos directos al investigador: qué objetivo manda, la latencia del MRFV, la
exposición de *Homalodisca vitripennis* y el marco con el que cuenta la planilla. Más la limitación
operativa del gancho de pre-commit en esta máquina.

## `GLOSARIO.md`

Cuatro términos nuevos: **conteo por incrementos**, **ancho de cobertura**, **marco de conteo** y
**ventana de juntura**.

## `FUENTES.md`

La carta del 2026-10-25, declarada como comunicación personal no publicada: todo lo que se cite de
ella va `[R]`, y lo que reprodujimos nosotros va `[M]` con el script que lo reproduce.

## Documentos que afirmaban lo que la carta corrige, y se corrigieron

| Archivo | Qué cambió |
|---|---|
| `research/ola4/M1_conteo_y_referencia/REPORT.md` | nota de encabezado: la discrepancia quedó explicada por otra vía, el «200 contra 199» era coincidencia, y qué de M1 sigue valiendo |
| `research/ola4/M8_que_compara_el_conteo/REPORT.md` | sección **4 bis**, el quinto límite, con la tabla del sesgo por gen |
| `research/ola4/README.md` | la fila de M1 y un aviso nuevo al principio de «lo que hay que leer» |
| `entregables/respuesta-al-mentor.md` | nota: la carta se envió, qué quedó confirmado y qué se cayó |
| `sifi_plus/perfil.py` | el encabezado distingue las dos curvas; `solapamiento` recibe `ancho_cobertura` y no `size` |
| `sifi_plus/test_api.py` | tres aserciones que fijan el ancho; de 87 a 93 verificaciones |
| `00_meta/DECISIONS.md`, nota de D18 y alternativa (a) de D25 | las dos citas del «36 ventanas contra 35» como criterio, corregidas por D65 |
| `00_meta/PREGUNTAS_ABIERTAS.md`, preguntas 2 y 7 | la 7 queda contestada por `N3` §6 y §7, con tres fuentes declaradas no corridas por falta de insumos; la 2 queda acotada por `N10`, que midió la consecuencia aunque no el hecho |
| `research/ola4/M7_robustez_bicc/REPORT.md` §4 | matizado: «la eficiencia casi no se mueve al cambiar de referencia» vale en el marco de la molécula y no en los de contexto |
