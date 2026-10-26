# M6 — Del veto binario a la alerta justificada (issue #10)

Implementa **D48**. Entregables:

- [`REPORT.md`](REPORT.md) — la tabla leída, el estado de las doce regiones bajo la regla
  nueva, cuáles vuelven a la mesa, qué se pierde al cambiar el booleano por un párrafo y
  las dos cifras de D59.
- [`NOTAS_PARA_META.md`](NOTAS_PARA_META.md) — separado por destino.
- `resultados/alertas.tsv` — una fila por coincidencia (región × organismo × gen) con los
  cuatro campos obligatorios; el mismo contenido partido en `resultados/alertas_por_region/`.
- `resultados/estado_regiones.tsv` — las doce regiones bajo las tres reglas.
- `resultados/alertas_por_ventana.tsv` — el respaldo por ventana, sin columna de secuencia.
- `resultados/anclas_m6.json` — las anclas, que abortan los scripts si fallan.
- `resultados/compuerta.json` — la compuerta corrida en los dos umbrales de D28.
- `scripts/identidad.py`, `scripts/tabla_alertas.py` y `scripts/compuerta.py` —
  reproducibles desde la raíz.

El código del veto modificado vive en `tools/sifi21_port/ejes_separados.py`
(`regla_veto="alerta"`, `estado_region`, `CompuertaRetirada`) y el motor de la tabla en
`tools/sifi21_port/alertas.py`, que además trae la compuerta de decisión
(`exigir_decidida`, `AlertaSinDecidir`), con su prueba en
`tools/sifi21_port/test_alertas.py`.

**Ninguna región se acepta ni se descarta acá.** Eso lo decide el usuario.
