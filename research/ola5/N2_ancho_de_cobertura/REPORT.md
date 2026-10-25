# N2 — El ancho de cobertura: son dos curvas distintas, no una convención equivocada

**Ola 5, línea N2.** Fecha: 2026-10-25. Sale de una duda propia que abrió
[`N1`](../N1_regla_de_conteo/REPORT.md): si la función histórica asigna 20 posiciones por ventana
y nuestro módulo de curvas asigna 21, ¿cuál de las dos está mal? Reproducible con
`scripts/medir_ancho.py`. Marcadores de `CLAUDE.md`.

## El resultado, en un párrafo

**Ninguna de las dos está mal: son dos curvas distintas, y la nuestra reproduce la del si-Fi21
original.** La pantalla del programa original dejó tres marcas registradas en
`research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md` líneas 85-89: en `ATPaseD_Dm` la
meseta de altura 9 va de 150 a 156, la de altura 8 de 287 a 297, y la línea azul queda plana en 21
`[R]`. Con ancho de cobertura 21 las tres coinciden; con ancho 20 las tres caen un nucleótido
antes —150-155, 287-296 y línea azul plana en 20— `[M]`. Así que el «20 posiciones por ventana de
21 nt» de la carta describe la curva que EPILAB guarda en su base, no el gráfico del si-Fi21, y el
`21` de `sifi_plus/perfil.py` queda confirmado en vez de corregido.

**Pero la verificación que teníamos no distinguía las dos convenciones, y eso sí era un defecto.**
`sifi_plus/test_api.py` fijaba cantidad de tramos, máximo y altura en cuatro posiciones: las
cuatro aserciones pasan con ancho 20 y con ancho 21, porque miden alturas dentro de un tramo y no
sus bordes `[M]`. Cuando le escribimos al investigador que reproducimos la curva «tramo por
tramo», la afirmación era cierta a esa granularidad y no fijaba el ancho. Ahora lo fija.

## 1. La medición

`[M]` `ATPaseD_Dm`, modo `fiel`, tabla `RNA_NN3`, RNAplfold 2.1.5 del instalador de si-Fi2015 —el
motor del programa original—, 42 ventanas eficientes, que es el conteo publicado para esa
configuración. Fuente: `resultados/ancho_de_cobertura.json`.

| | Tramos | Máximo | Meseta de altura 9 | Meseta de altura 8 | Línea azul | Pasa el test viejo | Coincide con la pantalla |
|---|---:|---:|---|---|---:|---|---|
| **Pantalla del original** `[R]` | 8 | 9 | 150-156 | 287-297 | 21 | — | — |
| ancho 20 | 8 | 9 | 150-155 | 287-296 | 20 | sí | **no** |
| ancho 21 | 8 | 9 | **150-156** | **287-297** | **21** | sí | **sí** |

Los ocho tramos terminan un nucleótido antes con ancho 20 y empiezan en la misma posición: la
diferencia es sistemática y de un solo nucleótido, que es exactamente lo que un test de alturas
interiores no puede ver.

## 2. Qué se cambió

`[M]` Dos cosas, y ninguna mueve un número publicado.

**El parámetro tiene nombre propio.** `sifi_plus.perfil.solapamiento` pasó de recibir `size` a
recibir `ancho_cobertura`, con el encabezado del módulo explicando que hay dos curvas en este
problema y cuál es cuál. Antes el ancho se derivaba del tamaño del siRNA porque para esta curva
coinciden; ahora quien llama elige, y `contrato` pasa `size` con la razón escrita. Los dos
llamadores con palabra clave de `test_api.py` se actualizaron.

**El test fija el ancho.** Se agregaron tres aserciones a `test_curva_del_rnai_design_plot`: la
meseta de altura 9 es exactamente `[(150, 156)]`, la de altura 8 que empieza en 287 es exactamente
`[(287, 297)]`, y el máximo de la línea azul es 21. `sifi_plus/test_api.py` pasa de 87 a **93
verificaciones, todas en verde** `[M]`. Con ancho 20 las tres fallan, que es lo que se pedía.

## 3. Por qué importa para el lunes

`[H]` Porque sostiene una afirmación nuestra con medición en vez de con una impresión, y porque
sostiene la de él con más precisión que su propia carta: el 20 no es una propiedad del si-Fi21 sino
de la representación que su plataforma guarda. Las dos cosas pueden ser verdad a la vez —el
gráfico con 21, la curva almacenada con 20— y distinguirlas es lo que evita que la revisión
interna que él anunció busque el problema en el lugar equivocado.

## 4. Lo que queda abierto

`[?]` La medición se hizo en un gen, `ATPaseD_Dm`, porque es el único del que tenemos las marcas
leídas de la pantalla. No hace falta más para decidir el ancho —un nucleótido de corrimiento
sistemático no depende del gen— pero conviene decir que es una verificación y no cuatro.

`[?]` No sabemos si la línea azul de la curva histórica de EPILAB también usa 20. Si usa 20, su
meseta es 20 y no 21, y es un chequeo de un minuto del lado de ellos.

## Archivos

| Archivo | Qué es |
|---|---|
| `scripts/medir_ancho.py` | la medición de los dos anchos contra las tres marcas de la pantalla |
| `resultados/ancho_de_cobertura.json` | tramos, mesetas, línea azul y los dos veredictos por ancho |
