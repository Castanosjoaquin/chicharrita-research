# M6 — Del veto binario a la alerta justificada (issue #10)

Implementa **D48**. Entregables:

- [`REPORT.md`](REPORT.md) — la tabla leída, el estado de las regiones bajo la regla
  nueva, cuáles vuelven a la mesa, qué se pierde al cambiar el booleano por un párrafo y
  las dos cifras de D59. Los addenda del 26 y del 27 de octubre agregan, en orden: dónde
  vive la firma, por qué la compuerta se llama desde el port y con qué umbral, y el
  tamizado de las seis regiones de 22 nt con la exigencia de presencia (D72), la firma de
  `eth_Dm` 193-392 (D73) y la región diecinueve que la compuerta encontró al regenerar la
  corrida de 22 nt (D75).
- [`NOTAS_PARA_META.md`](NOTAS_PARA_META.md) — separado por destino.
- `resultados/alertas.tsv` — una fila por coincidencia (región × organismo × gen) con los
  cuatro campos obligatorios; el mismo contenido partido en `resultados/alertas_por_region/`.
- `resultados/estado_regiones.tsv` — las diecinueve regiones bajo las tres reglas. Desde
  D72 es además **el inventario** que la compuerta exige: es el único archivo que puede
  decir «tamizada, cero aciertos», porque en `alertas.tsv` eso y «nunca tamizada» son las
  mismas cero filas.
- `resultados/alertas_por_ventana.tsv` — el respaldo por ventana, sin columna de secuencia.
- `resultados/anclas_m6.json` — las anclas, que abortan los scripts si fallan.
- `resultados/compuerta.json` — la compuerta corrida en los dos umbrales de D28.
- `resultados/umbral_compuerta.json` — cuánto cambia la compuerta según el umbral de D28 que
  se le exija, con y sin las firmas de D68. Es la medición que fundamenta D69.
- `scripts/identidad.py`, `scripts/tabla_alertas.py`, `scripts/compuerta.py` y
  `scripts/umbral_compuerta.py` — reproducibles desde la raíz.

El código del veto modificado vive en `tools/sifi21_port/ejes_separados.py`
(`regla_veto="alerta"`, `estado_region`, `CompuertaRetirada`) y el motor de la tabla en
`tools/sifi21_port/alertas.py`, que además trae la compuerta de decisión
(`exigir_decidida`, `RegionNoTamizada`, `AlertaSinDecidir` y su base `CompuertaCerrada`),
con su prueba en
`tools/sifi21_port/test_alertas.py`. Quien **aplica** esa compuerta, desde D69, es
`ranking.region_recomendada()` en `tools/sifi21_port/ranking.py`: el único punto del port
donde una región se vuelve recomendación. `scripts/compuerta.py` es sólo el inventario.

**Ninguna región se acepta ni se descarta acá.** Eso lo decide el usuario.
