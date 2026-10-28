# F3 — notas para los archivos de memoria, separadas por destino

Estado al cierre de la línea, 2026-10-27. Todo lo que sigue está **ya aplicado** en los
archivos de `00_meta/`; esta página es el registro de qué fue a dónde y por qué.

## A `DECISIONS.md`

**`D87` — los pesos del recomendador.** Aplicado, y **confirmado por el usuario** el
2026-10-27 sobre cuatro opciones presentadas. Fenotipo 0,40, esencialidad 0,25, off-target
0,25, conservación 0,10, expresión en tejido expuesto 0,00 y declarada faltante; agregación por
**cohortes** según qué ejes tiene calculado cada candidato, sin comparar entre cohortes y sin
rellenar ningún hueco. Se escribió como propuesta antes de rankear (`5880625`) y pasó a
decisión al confirmarse (`44e156d`).

## A `PREGUNTAS_ABIERTAS.md`

De la ola 6, entradas **65 a 75**:

- **65** — `D67` define tres mecanismos y el catálogo tiene un cuarto: menos transmisión con el
  insecto vivo, cuatro filas. Ampliar `D67` no es de esta línea.
- **66** — los dos candidatos de signo invertido abren la pregunta contraria a la nuestra: si
  silenciarlos favorece al patógeno, son parte de la defensa del vector.
- **67** — faltan `work/sifi_v2/` y los tres TSA en esta máquina, con la advertencia de no
  regenerarlos con otra versión del motor.
- **68** — «esta máquina» sin nombrar la máquina, dos veces el mismo día, contra lo que pide
  `D71`.
- **69** — el zip del investigador no trae el eje de expresión, y no podía traerlo.
- **70** — el mecanismo `movilidad` de `D67` tiene **un** candidato en 36 filas, y su réplica
  más cercana es negativa.
- **71** — dos filas traen mortalidad que su propia fuente desatribuye del blanco, y una trae
  un número grande (64 %).
- **72** — las cinco fuentes que el eje 2 necesita y no se pudieron abrir, con el motivo de
  cada una, más las tres vías sin búsqueda propia.
- **73** — dos tamizajes de la misma especie se contradicen sobre la actina; se resolvió
  bajando el nivel y declarando el `[?]`, no promediando.
- **74** — «matar o esterilizar» quedó contestada **en parte** por el orden de §2, y la entrada
  dice exactamente qué faltaba: un segundo orden con el eje de fenotipo filtrado por mecanismo.
- **75** — **cierra la 74, y la respuesta es que sí**: el orden cambia según el objetivo, y los
  dos grupos del primer puesto no comparten un solo candidato. Con las tres lecturas que valen
  más que el sí —la vía de esterilizar está peor sostenida, esterilizar saca a *Dalbulus
  maidis* del podio, y la quimera de `O3` resulta ser un miembro del grupo líder de cada
  objetivo—. Lo que sigue abierto es **elegir** el objetivo, que no es de esta línea.

## A `CAMINOS_PROBADOS.md`

**La suma ponderada sobre los 36 candidatos, descartada antes de implementarla.** Aplicada. La
forma obvia, reemplazada por cohortes porque 28 de 36 filas no tienen el eje de off-target y
sumar obliga a imputar.

## A `FUENTES.md`

Aplicado. Las cinco fuentes abiertas del eje 2 —fichadas `P13` a `P17` en
`research/ola2/W1_papers/papers.json`, que pasa de 12 a 17 entradas sin tocar el conteo del
manifiesto del corpus, que sigue en 7— más la ficha de InteractiveFly de la que sale el 98 %
del nulo de `eth`, **con la aclaración de que su primaria no se abrió**. Y la lista de las
cinco que se intentaron y no cargaron, con el código de error de cada una.

## Lo que NO va a ningún archivo de memoria

El orden de los candidatos. Está en
[`resultados/orden_genes.tsv`](resultados/orden_genes.tsv) y leído en el
[`REPORT.md`](REPORT.md), y no sube a `00_meta/` porque no es una decisión ni una pregunta
abierta: es un resultado con su criterio al lado, y el criterio puede cambiar. Lo que sí subió
es el ADR que lo gobierna.

Tampoco sube la lectura de que «el recomendador confirma lo que ya estábamos haciendo». Es
cierto que los tres primeros son los tres genes de *Dalbulus maidis* sobre los que el proyecto
ya trabaja, y es cierto que el criterio se escribió antes; pero el eje 1 premia explícitamente
la evidencia medida en la propia especie, así que el resultado estaba en parte construido. El
`REPORT.md` §4 publica las dos lecturas juntas. Convertir la favorable en una línea de memoria
sería quedarse con la mitad que conviene.

---

## Adenda del 2026-10-27 (issue #37): el eje 4 se calculó

Posterior al cierre de la línea. El eje de conservación, que arriba figura como faltante, se
calculó en la máquina de Joaquín. Todo está **ya aplicado**:

- **`DECISIONS.md`: `D94`.** La enmienda 1 del preregistro del eje (dato en al menos dos de tres
  TSA), declarada como posterior al resultado, con las dos reglas publicadas lado a lado.
- **`PREGUNTAS_ABIERTAS.md`: entradas 98 y 99.** La 98, la diferencia con `C8` para `eth` y
  `burs-alpha`, sin causa averiguada `[?]`. La 99, que el eje sólo llega a 5 de 36 filas por falta
  de secuencia, no de cálculo, y que la recuperación es la misma que pide #43.
- **`CAMINOS_PROBADOS.md`:** dos descartes, las consultas desde contigs de `F1` y los genomas como
  fuente, y la regla de los tres TSA.

Lo que **no** sube: los puntajes del eje (`resultados/eje4_REPORT.md`) ni el cambio de cohorte,
que son un resultado con su criterio al lado. El orden de los candidatos tampoco: el empate de
tres del primer puesto sigue declarado y no es una decisión.
