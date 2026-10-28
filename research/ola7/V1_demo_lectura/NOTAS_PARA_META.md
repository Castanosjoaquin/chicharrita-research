# V1 — decisiones candidatas para `00_meta/DECISIONS.md`

Issue **#45**. Lo que sigue son candidatas, con su hecho motivador y su alternativa descartada,
para que quien integre a `DECISIONS.md` tenga el ADR casi escrito. La numeración queda para el
merge.

## Candidata 1 — La demo lee resultados y no calcula criterios

**Decisión.** Las vistas de `sifi_plus/` que muestran resultados de otras líneas **leen archivos
versionados y no recalculan nada**. Todo número que una vista muestra sale de un archivo que
escribió una corrida verificada y viaja con su etiqueta de procedencia. Si una vista necesitara
un número que no está en ningún archivo, el resultado correcto es **decir que falta ese
archivo**, no calcularlo.

**Hecho que la motiva.** El proyecto venía mezclando el motor de registro con la demo. La mezcla
tiene un costo concreto y no es higiene de código: varias líneas valen porque el criterio se
commitea antes del primer cálculo y la corrida aborta si un ancla no coincide, y un botón que
corre un pipeline preregistrado en silencio destruye esa garantía. Una pantalla que lee lo que el
pipeline ya escribió no tiene ese problema en absoluto.

**Alternativas consideradas.** (a) Que las vistas llamen al motor y muestren el resultado fresco,
que es lo que haría cualquier demo; (b) que lo llamen pero cacheando; (c) la elegida.

**Criterio.** Sobre (a) y (b): las dos ponen un camino de cálculo que no pasa por el preregistro
de la línea que definió el criterio. El costo de la elegida es visible y es el precio correcto —
hay cinco cosas que las vistas **no** pueden mostrar porque falta el archivo, y están
enumeradas—. El beneficio es que las verificaciones del motor no pueden romperse desde una
pantalla: las vistas no lo importan.

**Consecuencia.** `sifi_plus/PREREGISTRO_DEMO.md` fija por vista qué archivo lee y qué muestra.
Toda vista futura de esta clase entra por ahí.

## Candidata 2 — Ningún número se muestra sin modo, motor, panel y archivo

**Decisión.** La etiqueta de procedencia es **parte del contrato de datos** de la interfaz, no
una cortesía. Un archivo que no declara su configuración produce **«procedencia no declarada»**,
y la vista **no la adivina**: ni del nombre del archivo, ni del vecino, ni del script que lo
generó.

**Hecho que la motiva.** El argumento ya estaba escrito en `LEEME.md` para los rangos guardados y
valía igual para las vistas nuevas: un conteo sin su modo y su motor no significa nada, porque
los mismos cuatro genes dan cuatro números distintos según cuál de los dos RNAplfold corrió.
Medido al implementar: **ningún archivo de `research/ola4/M6_alertas/resultados/` declara su
configuración**, y dos de sus columnas dependen de ella `[M]`.

**Alternativas consideradas.** (a) Leer el modo del código del generador y mostrarlo como si el
archivo lo declarara; (b) no mostrar esas columnas; (c) la elegida, mostrarlas con la etiqueta
que dice que la procedencia no está.

**Criterio.** Sobre (a): que `tabla_alertas.py` fije el modo en una ruta literal de su fuente **no
es que el resultado lo declare**, y presentarlo como declarado convierte una lectura del código en
una propiedad del dato. Sobre (b): esconder la columna pierde información que sí está medida. La
elegida deja las dos cosas visibles: la cifra y el hueco.

**Consecuencia.** Falta un sidecar de configuración en `M6`, como el que `O3` sí tiene. Queda
anotado como archivo faltante y no como pendiente de esta línea.

## Candidata 3 — Los organismos con alerta no son el panel de referencias

**Decisión.** Ninguna vista deriva el panel de una corrida de los organismos que aparecen en su
tabla de alertas. Cuando el panel no está declarado en un archivo, se muestra como no declarado,
y la lista de organismos con alerta se rotula como lo que es.

**Hecho que la motiva.** Una referencia con cero aciertos **no deja ninguna fila** en
`alertas.tsv`, así que leer el panel de las filas confunde «no tiene aciertos» con «no se miró».
Es exactamente la distinción que `D72` existe para hacer —y que motivó pedir el inventario de
regiones tamizadas aparte— aplicada al eje de las referencias en vez del de las regiones.

**Alternativas consideradas.** (a) Derivar el panel de las filas, que es la lectura natural y
estaba a un renglón de distancia; (b) la elegida.

**Criterio.** Sobre (a): produce un panel que parece medido y es una inferencia, y además es
sistemáticamente **más chico** que el real —le faltan justo las referencias limpias—. El modo de
fallar es silencioso y favorece la conclusión tranquilizadora, que es el patrón que este
repositorio evita.

**Consecuencia.** El panel queda como archivo faltante en `M6` y en los ejes de `O3`.

## Candidata 4 — La bandeja dice qué destraba cada firma, y sobre todo qué no

**Decisión.** La bandeja de firmas muestra, por fila, si esa fila cuenta en el umbral con el que
la compuerta exige decisión (`perfecto_21`, `D48` literal) o sólo en el laxo de `D28`.

**Hecho que la motiva.** Medido al construirla: **las 13 filas en «pendiente» tienen todas cero
coincidencias perfectas de 21 nt**, así que en el umbral vigente ya pasan las 23 regiones del
inventario y firmarlas **no destraba ninguna** `[M]`. En `perfecto_ge19` son seis las regiones
frenadas y ninguna vigente.

**Alternativas consideradas.** (a) Mostrar «13 pendientes» a secas, que es lo que un contador
hace; (b) la elegida.

**Criterio.** Sobre (a): un contador de 13 sobre una bandeja de entrada se lee como 13 cosas
trabadas, y acá no hay ninguna trabada en el umbral vigente. La pantalla habría inventado una
urgencia que la medición no respalda, y lo habría hecho sin decir una sola cosa falsa. Es el
riesgo propio de una demo y por eso la decisión es de la demo.

**Consecuencia.** Las dos columnas de umbral se muestran siempre y el texto dice cuál es la
vigente.

## Candidata 5 — Una constante duplicada por la frontera lleva su tripwire

**Decisión.** Cuando una regla tiene que estar escrita de los dos lados de una frontera que no se
cruza —la vista no puede importar el motor y el motor no puede importar la interfaz— la
duplicación se acepta **con una verificación que compara las dos copias**, leyendo el archivo del
otro lado como texto y parseándolo, sin importarlo.

**Hecho que la motiva.** Las reglas de validación de firma de `D48` —el vocabulario de
decisiones, el mínimo de prosa, el esquema de diez columnas y las columnas de los cuatro campos
obligatorios— quedaron en `sifi_plus/vista_firmas.py` y en `tools/sifi21_port/alertas.py`. Dos
copias sin red se separan en silencio, y la que se separa acá deja pasar una firma que el
generador después rechaza, o al revés.

**Alternativas consideradas.** (a) Importar el módulo del motor desde la vista, que rompe la
frontera; (b) mover las constantes a un tercer módulo compartido, que crea una dependencia nueva
entre la interfaz y el port; (c) duplicar y confiar; (d) la elegida.

**Criterio.** Sobre (c), es la que falla el día que alguien cambia una de las dos. Sobre (b), es
defendible y quedó descartada sólo porque el alcance de la línea prohibía tocar
`tools/sifi21_port/`: si alguna vez se puede tocar, es mejor que la elegida.

**Consecuencia.** Si alguien cambia `PROSA_MINIMA`, `DECISIONES`, `COLUMNAS_DECISION` o las
columnas de un campo obligatorio en cualquiera de los dos lados, `test_api.py` falla y nombra
cuál.
