# Formato de salida de `conteo_por_acierto.py`, sobre secuencias de juguete

**Esto no es una medicion del caso real.** Lo genera `scripts/demo_sintetico.py` con una secuencia al azar de semilla fija (7) de 60 nt y tres referencias construidas a mano, y sirve para dos cosas: fijar el formato de la tabla que va a llenar la matriz de bases reales, y mostrar que la regla del original mueve el conteo en los dos sentidos. La celda `identidad` reproduce el conteo por ventana; `isolado_variante` lo baja, porque una sola sustitucion saca de la tabla a las ventanas que la cubren; `con_repeticion` lo sube, porque las ventanas del tramo repetido cuentan dos veces. `[M]` con insumos sinteticos.

Regenerar: `python scripts/demo_sintetico.py --salida resultados/ejemplo_formato_sintetico.md`

---

## Conteos por base, con la regla del original

Declarado por la planilla: gen = 10.

### Agregacion `suma_filas`

| Base | gen | Distancia L1 | Reproduce |
|---|---|---|---|
| `con_repeticion` | 12 | 2 | no |
| `identidad` | 10 | 0 | si |
| `isolado_variante` | 5 | 5 | no |

### Agregacion `fila_max`

| Base | gen | Distancia L1 | Reproduce |
|---|---|---|---|
| `con_repeticion` | 12 | 2 | no |
| `identidad` | 10 | 0 | si |
| `isolado_variante` | 5 | 5 | no |

### Agregacion `fila_homonima`

| Base | gen | Distancia L1 | Reproduce |
|---|---|---|---|
| `con_repeticion` | - | - | no |
| `identidad` | 10 | 0 | si |
| `isolado_variante` | - | - | no |

### Detalle por celda

| Base | Gen | Ventanas | (a) eficientes | (b) aciertos `+` | (c) cualquier hebra | (d) sin acierto | (e) multiple | Filas | Origen |
|---|---|---|---|---|---|---|---|---|---|
| `con_repeticion` | gen | 40 | 10 | 12 | 12 | 0 | 2 | 1 | local:mm0:con_repeticion.fasta |
| `identidad` | gen | 40 | 10 | 10 | 10 | 0 | 0 | 1 | local:mm0:identidad.fasta |
| `isolado_variante` | gen | 40 | 10 | 5 | 5 | 5 | 0 | 1 | local:mm0:isolado_variante.fasta |
