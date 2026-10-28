# Preregistro de las vistas de lectura de la demo (V1, issue #45)

Esto se escribe **antes** del primer renglón de código de las vistas, y por el mismo motivo por
el que varias líneas de este proyecto escriben su criterio antes de medir: una pantalla que
puede elegir qué número mostrar después de verlo no prueba nada. Acá el riesgo es más chico
que en una corrida —una vista no produce cifras nuevas— pero el documento sirve para otra
cosa: fijar **qué archivo lee cada vista**, de modo que el día que una vista muestre un número
que no esté en ninguno de estos archivos se note que algo se calculó por el camino.

## El motivo de la línea

El motor de registro y la demo no son la misma cosa. El motor existe para que un número se
pueda volver a producir y auditar; la demo existe para que se vea qué podría ser la
herramienta. No compiten: **la demo no reemplaza al motor, lo muestra.**

La distinción importa porque el proyecto las venía mezclando, y mezclarlas tiene un costo
concreto. Varias líneas valen porque el criterio se commitea antes del primer cálculo y la
corrida aborta si un ancla no coincide; un botón que corre un pipeline preregistrado en
silencio destruye eso. Una pantalla que lee lo que el pipeline ya escribió no tiene ese
problema en absoluto.

## La regla, que es el criterio de terminado

> **La demo lee resultados. No calcula criterios.**

Todo número que una vista muestre sale de un archivo versionado que escribió una corrida
verificada, y viaja con la etiqueta de procedencia que lo produjo. Ninguna vista de esta línea
recalcula un veredicto de eficiencia, un tamizado de off-target ni un puntaje de ranking.
**Si una vista necesitara un número que no está en ningún archivo, el resultado correcto de
esta línea es decir que falta ese archivo, no calcularlo.** La sección «Lo que no se va a poder
mostrar» es parte del entregable, no una disculpa.

## El contrato de procedencia

Ningún número aparece solo. Cada uno viaja con cuatro cosas:

| Campo | Qué dice |
|---|---|
| **modo** | `fiel` o `corregido`, que es cómo se aplicó la regla terminal |
| **motor** | `RNAplfold 2.1.5` (el de si-Fi21) o `ViennaRNA 2.7.2` |
| **panel** | contra qué referencias se tamizó |
| **archivo** | la ruta exacta del archivo del que salió la cifra |

El argumento ya está en `LEEME.md` y vale igual acá: un conteo sin su modo y su motor no
significa nada, porque los mismos cuatro genes dan cuatro números distintos según cuál de los
dos RNAplfold corrió.

**Si un archivo no declara su configuración, la vista muestra «procedencia no declarada» y no
adivina.** No la deduce del nombre del archivo, no la copia del vecino y no la lee del script
que lo generó para presentarla como si el archivo la dijera. Que el generador fije el modo en
una ruta literal de su código fuente no es que el resultado lo declare.

Y los cuatro estados que no son el mismo estado, que la interfaz ya distingue en sus tiras y
que las vistas nuevas heredan:

1. **sin medir** — no se corrió. No se dibuja como cero.
2. **no aplica** — la cifra no depende de ese campo. El conteo de coincidencias exactas no
   depende del modo ni del motor: es apareamiento de cadenas, no termodinámica.
3. **declarado faltante** — el archivo existe y dice que ese eje no está.
4. **cero medido** — se miró y hay cero. Es el único que se dibuja como cero.

## Cuántas vistas, y por qué estas cinco

El pedido dice «cuatro vistas de lectura más una que además escribe» y después enumera cuatro
(A, B, C y la bandeja). Las dos frases no cierran, así que queda escrito cómo se resuelve: se
toman **cuatro de lectura** —A, B, C y E— **más la bandeja, que escribe**. La vista E es el
cuarto insumo que el pedido lista para la vista C y que no ubica en ninguna pantalla:
`ejes_ranking_o3_corregido_vienna.tsv`, «los dos ejes por objeto». Darle vista propia usa todos
los insumos declarados y deja la vista C con una sola cosa que contar.

---

## Vista A — antes y después de mover la región

**Qué contesta.** Qué cambia, ventana por ventana, cuando una región se mueve dentro del mismo
gen. El caso que la motiva: `BicC_Dm` 264-563 contra 922-1221.

**Archivos que lee.**

- `research/ola4/M6_alertas/resultados/alertas_por_ventana.tsv` — 279 filas `[M]`. Columnas que
  usa: `gen`, `region`, `pos`, `organismo_corto`, `criterio`, `transcripto`, `gen_simbolo`,
  `gen_locus`.
- `research/ola4/M6_alertas/resultados/alertas_por_region/<gen>_<región>.tsv` — 21 archivos en
  disco `[M]`, un archivo por región, con el mismo esquema de 34 columnas que `alertas.tsv`.
  Columnas que usa: `organismo_corto`, `organismo_especie`, `organismo_rol`, `gen_simbolo`,
  `gen_locus`, `gen_transcriptos`, `ventanas_perfecto_21`, `ventanas_perfecto_ge19`,
  `baja_complejidad_perfecto_21`, `baja_complejidad_perfecto_ge19`, `ventanas_21_eficientes`,
  `ventanas_ge19_eficientes`, `estado_region`, `vigente`, `que_es`.

**Qué muestra.** Las dos regiones del par lado a lado, en el mismo eje de posición del gen, con
una marca por ventana con alerta y el organismo que la produce. Toma **cualquier par** del
directorio, no sólo el de `BicC_Dm`: el desplegable se arma leyendo el directorio.

**Procedencia de cada número.**

- Los conteos de coincidencia (`ventanas_perfecto_21`, `ventanas_perfecto_ge19`) y las marcas
  por posición: modo y motor **no aplican** (estado 2); panel = los organismos del panel de M6,
  leídos de la columna `organismo_corto` de la tabla; archivo = la ruta de arriba.
- Las dos columnas de eficiencia (`ventanas_21_eficientes`, `ventanas_ge19_eficientes`) **sí**
  dependen del modo y del motor, y **ningún archivo de `research/ola4/M6_alertas/resultados/`
  los declara** `[M]`. Se muestran con la etiqueta **«procedencia no declarada»**. No se
  deducen de `tabla_alertas.py`, que las fija en una ruta literal de su código.

**Si falta el archivo.** «No corrido», con la ruta que falta y el comando que lo genera
(`research/ola4/M6_alertas/scripts/tabla_alertas.py`). No cero, no tira vacía.

---

## Vista B — los tres marcos de conteo

**Qué contesta.** Cuántas ventanas eficientes tiene una región, en los tres marcos que el
proyecto distingue, que contestan tres preguntas distintas.

**Archivos que lee.**

- `research/ola6/O3_quimera_bicc_vatpase_b/resultados/tres_marcos.tsv` — 7 filas `[M]`.
  Columnas: `gen`, `inicio`, `fin`, `largo`, `nota`, `arranques_marco1`,
  `arranques_comparables`, `marco1_contexto_todos`, `marco2_contexto_comparables`,
  `marco3_molecula`, `limite_fisico`, `contexto_neto`, `pierden`, `ganan`.
- `.../tres_marcos.json` — de acá sale **sólo la configuración**, no las cifras: bloque
  `configuracion` con `modo`, `backend`, `tabla_nn`, `temp_c` y el `criterio` completo.

**Qué muestra.** Las tres cifras de una región a la vez. **La cifra de cabecera es la del marco
3** —`marco3_molecula`, la molécula que existiría— y las otras dos van al lado, nunca en vez
de. El texto dice qué pregunta contesta cada marco. No se promedian y la vista no elige.

**Procedencia.** modo `corregido`, motor `ViennaRNA 2.7.2`, tabla NN3, 22 °C, leídos de
`tres_marcos.json`; panel **no aplica** (un conteo de eficientes no consulta ninguna
referencia); archivo = `tres_marcos.tsv`.

**Si falta el archivo.** Falta el TSV: «no corrido». Falta **sólo** el JSON: las cifras se
muestran con «procedencia no declarada», porque sin él la configuración no está declarada en
ningún lado.

---

## Vista C — la juntura de la quimera

**Qué contesta.** Qué bloques de la juntura entran enteros desde un solo gen y cuáles los
fabrica el empalme. Esa distinción es la que decide la alerta, y el dibujo tiene que hacerla
obvia.

**Archivos que lee.**

- `.../juntura_resumen_o3_corregido_vienna.tsv` — 2 filas, una por orden. Columnas:
  `quimera`, `ventanas_de_juntura`, `juntura_eficientes`, `juntura_eficientes_j`,
  `juntura_con_blanco_continuo_21nt`, `bloques_con_acierto`,
  `bloques_fabricados_por_el_empalme`, `referencias_fabricadas`.
- `.../juntura_detalle_o3_corregido_vienna.json` — las fichas de bloque. Claves que usa:
  `modo`, `backend`, `min_bloque`, `coordenadas`, `panel`, `limite`, `resumen`,
  `bloques_con_acierto`; y de cada ficha `quimera`, `j`, `pos_en_la_quimera`,
  `ventana_eficiente`, `bloque_largo`, `bloque_offset`, `nt_de_izquierda`, `nt_de_derecha`,
  `cruza_la_union`, `aciertos`, `on_target_del_vector`.
- `.../quimeras_ventanas_cambiadas_o3_corregido_vienna.tsv` — 5 filas. Columnas: `quimera`,
  `pos_quimera`, `lado`, `antes`, `ahora`, `nt_hasta_la_union`.

**Qué muestra.** Los dos órdenes dibujados, con los bloques en dos colores: **heredado**
(`cruza_la_union` falso: entra entero en el aporte de un solo gen) y **fabricado**
(`cruza_la_union` verdadero: toma al menos un nucleótido de cada lado). Al lado, las ventanas
heredadas que cambiaron de veredicto con su distancia a la unión.

**Procedencia.** modo `corregido`, motor `ViennaRNA 2.7.2`, `min_bloque` 19, panel de siete
referencias y coordenadas, todo declarado en `juntura_detalle_...json`; archivo = el TSV para
las cifras de cabecera y el JSON para las fichas.

**Lo que esta vista no puede dibujar, y es un resultado de la línea.** El archivo de detalle
**no trae las 240 fichas de bloque: trae las 19 que tienen acierto** `[M]`. Los otros 221
bloques existen —son los que enumera la juntura— pero ninguna de sus propiedades está en un
archivo versionado, así que el dibujo marca los 19 medidos y deja el resto como **no medido**,
no como heredado ni como sin acierto. Deducir la geometría de los 221 restantes sería calcular,
que es justo lo que esta línea no hace.

Esto además **contradice una frase publicada** y, por la convención del repositorio, se anota
en vez de corregirse: `research/ola6/O3_quimera_bicc_vatpase_b/REPORT.md:371` describe el
archivo como «los 240 bloques, con aporte por gen y sin secuencias», y el archivo en disco
tiene 19 fichas bajo la clave `bloques_con_acierto`. La línea 218 del mismo REPORT dice bien
que «de las 240 fichas de bloque, 19 tienen acierto», así que lo que está mal escrito es la
tabla de archivos, no la medición.

**Si falta un archivo.** Cada panel declara «no corrido» por separado: el resumen sin el
detalle muestra las cifras de cabecera y dice que el dibujo de bloques no está disponible.

---

## Vista E — los dos ejes por objeto

**Qué contesta.** Cómo se ordenan las dos regiones sueltas y las dos quimeras en los dos ejes
que O3 publicó, bajo las dos reglas de trato del vector.

**Archivo que lee.** `.../ejes_ranking_o3_corregido_vienna.tsv` — 8 filas `[M]`. Columnas:
`objeto`, `clase`, `trato_dmaidis`, `regla`, `largo_nt`, `n_ventanas`, `eficientes`,
`eficacia`, `limpieza`, `buenos_limpios`, `con_off_target`, `con_21_perfecto`, `vetada`.

**Qué muestra.** Los cuatro objetos con sus dos ejes, separados por regla (`conservadora` y
`mecanicista`), sin combinarlos en un puntaje. La vista **no ordena por un índice compuesto**:
ponderar los dos ejes es un criterio, y el criterio no es de la demo.

**Procedencia.** modo `corregido` y motor `ViennaRNA 2.7.2`, leídos de
`quimeras_meta_o3_corregido_vienna.json`, que es el sidecar de la misma corrida; **panel: no
declarado en el archivo** —ni el TSV ni su sidecar lo dicen, y `limpieza` y `con_off_target`
dependen del panel—, así que esas dos columnas van con «procedencia no declarada» `[M]`.

**Si falta el archivo.** «No corrido».

---

## Vista D — la bandeja de firmas, que es la única que escribe

**Qué contesta.** Qué alertas están sin firmar, qué dicen sus cuatro campos obligatorios y qué
se destraba al firmarlas.

**Archivos que lee.**

- `research/ola4/M6_alertas/resultados/alertas.tsv` — 32 filas × 34 columnas `[M]`. Estado
  medido al 2026-10-28: **14 aceptada, 13 pendiente, 5 bloqueante** `[M]`.
- `research/ola4/M6_alertas/resultados/estado_regiones.tsv` — 23 filas. Columnas que usa:
  `gen`, `region`, `que_es`, `vigente`, `filas_de_alerta`, `estado_D48`, `estado_firmado_21`,
  `estado_firmado_ge19`, `decide`.
- `research/ola4/M6_alertas/decisiones.tsv` — el archivo de firmas, 19 filas hoy `[M]`.

**Qué muestra.** Las filas agrupadas por estado, con los cuatro campos obligatorios de D48
completos —organismo, exposición, gen involucrado y evidencia— y un formulario para escribir
`decision_usuario` y `justificacion_usuario`. Y, leído de `estado_regiones.tsv`, **qué región
destraba cada firma**.

**Un hecho medido que la vista tiene que decir y no suavizar.** Las 13 filas pendientes tienen
todas **cero** ventanas con coincidencia perfecta de 21 nt `[M]`. Como el umbral con el que la
compuerta exige decisión es `perfecto_21` —D48 literal, `ranking.UMBRAL_COMPUERTA`— firmarlas
**no destraba ninguna región en el umbral vigente**: en `perfecto_21` ya pasan las 23 regiones.
En el umbral laxo de D28, `perfecto_ge19`, son seis las regiones frenadas y ninguna vigente
(`resultados/umbral_compuerta.json`) `[M]`. La bandeja muestra las dos columnas y dice cuál es
la vigente. Presentar «13 firmas pendientes» como si fueran 13 regiones trabadas sería inventar
una urgencia que la medición no respalda.

### El archivo de firmas

**No se inventa un formato: ya existe.** D68 sacó la firma de la tabla y la puso en
`research/ola4/M6_alertas/decisiones.tsv`, que es **entrada** del generador y no salida suya,
precisamente porque `tabla_alertas.py` reconstruye `alertas.tsv` desde cero en cada corrida y
una firma escrita sobre la tabla se perdía sin aviso. El esquema son diez columnas:

| Columna | Qué es |
|---|---|
| `gen`, `region`, `organismo_corto`, `gen_locus` | la clave de la fila: región × organismo × **gen impactado** |
| `huella_21`, `huella_ge19` | los dos conteos de D28 al momento de firmar |
| `firmado_por`, `fecha` | quién firmó y cuándo |
| `decision_usuario` | `pendiente`, `aceptada` o `bloqueante` |
| `justificacion_usuario` | el párrafo |

La huella es lo que tiene que seguir siendo cierto para que la firma siga valiendo: si los
conteos de la fila cambian, **no es la fila que alguien firmó** y el generador levanta
`FirmaVencida`. La vista escribe la huella leyéndola de la fila que muestra, que es la única
forma de que la firma quede atada a lo que el firmante tenía delante.

**La vista no edita `alertas.tsv`.** Escribe una fila en `decisiones.tsv` y después dice, con
el comando exacto, que el inventario se regenera corriendo `tabla_alertas.py`. El resultado de
otra línea no se toca en el lugar.

### Las cuatro formas de rechazar una firma

Se reimplementan en la vista porque **no puede importar `tools/sifi21_port/alertas.py`**, y el
riesgo de que las dos copias se separen se cubre con una verificación que compara las
constantes de las dos (ver más abajo).

1. **Sin justificación.** Menos de 40 caracteres se rechaza: D48 pide un párrafo, no un clic.
2. **Con el texto de relleno.** Una justificación que empieza con `pendiente` se rechaza:
   cambiar una palabra no es decidir.
3. **Sin citar la fila.** La justificación tiene que nombrar el LOC del gen impactado o una de
   las accesiones de transcripto de esa fila. Es un piso mecánico y grosero a propósito, pero
   distingue un párrafo escrito sobre esta fila de uno genérico copiado a todas. Vale para toda
   fila decidida, no sólo para la que pasa de `bloqueante` a `aceptada`.
4. **Decisión fuera del vocabulario.** Sólo `pendiente`, `aceptada` o `bloqueante`.

Lo que ninguna de las cuatro verifica —y la vista lo dice en pantalla— es si el párrafo es
cierto, pertinente o suficiente. Es la contracara declarada de D48: «un párrafo puede estar mal
escrito de un modo en que un booleano no puede».

**Y la línea no firma nada.** Construye la bandeja; firmar es del equipo.

---

## Lo que esta línea no va a poder mostrar, por falta de archivo

Esto es resultado, no pendiente de trabajo.

1. **La geometría de 221 de los 240 bloques de la juntura.** `juntura_detalle_...json` trae las
   19 fichas con acierto. Falta un archivo con una ficha por bloque enumerado.
2. **El modo y el motor de las columnas de eficiencia de M6.** Ningún archivo de
   `research/ola4/M6_alertas/resultados/` declara su configuración. Falta un sidecar de
   configuración, como el que O3 sí tiene.
3. **El panel de los ejes de ranking de O3.** Ni `ejes_ranking_...tsv` ni
   `quimeras_meta_...json` lo declaran, y `limpieza` y `con_off_target` dependen de él.
4. **La matriz de off-target de `V-ATPase B` contra el panel completo.** D78 la declaró
   faltante y sigue faltando; la región 517-816 entra a la bandeja con las filas que tiene.
5. **Cualquier comparación que pida correr algo.** Si el par de regiones que alguien quiere ver
   no está entre los 21 archivos del directorio, la vista dice que falta ese archivo. No lo
   tamiza.

## La frontera que no se cruza

- No se hace una interfaz nueva: la arquitectura ya separa ruteo, motor y dibujo.
- Las vistas tocan `servidor.py` y `estatico/app.js` y agregan módulos de lectura propios.
  **No tocan `api.py` ni `tools/sifi21_port/`, ni una línea**, y no los importan.
- No entran a la interfaz el recomendador de genes, la transferencia por homología, los pares
  por mecanismo ni el enumerador de quimeras.
- El servidor sigue atado a `127.0.0.1`. Ninguna vista escribe secuencia: las ventanas se
  solapan de a 1 nt y una columna de secuencia reconstruye el gen entero.
- Todo lo que el programa escribe va a `work/sifi_plus/`, fuera del control de versiones. **La
  excepción es el archivo de firmas**, que sí se versiona porque es una decisión del equipo y
  no una salida de cómputo.
- Ninguna vista publica una región como recomendación. `V-ATPase B` 517-816 es insumo de una
  medición y la compuerta de D72 la rechaza como recomendada: la vista la muestra con ese
  estado y no lo cambia.

## Cómo se verifica

Las verificaciones nuevas de `test_api.py` miran **lectura y procedencia, no criterio**:

1. Cada vista levanta su archivo y devuelve las filas que el archivo tiene.
2. Un archivo de insumo ausente produce «no corrido» y **no** un cero.
3. Ninguna vista escribe fuera del archivo de firmas.
4. Ningún módulo de vista importa `api` ni `tools/sifi21_port/`, verificado leyendo los
   imports del archivo.
5. Las constantes de validación de firma de la vista coinciden con las de
   `tools/sifi21_port/alertas.py`, que es el tripwire contra que las dos copias se separen.
6. Una firma sin justificación, con el texto de relleno o sin citar la fila se rechaza, y
   `alertas.tsv` no queda modificado.
7. El contador de pendientes de la bandeja coincide con las filas en `pendiente` del
   inventario.

Y las verificaciones que ya estaban pasan antes y después, con los conteos ancla sin moverse un
dígito. Medido en esta máquina **antes** de tocar nada: **75 verificaciones pasan, 0 fallan y 5
bloques se declaran «no corrido»** —falta el RNAplfold 2.1.5 del original, que es un `.exe` de
Windows, y `work/sifi_check/NC_002786.2.fasta` `[M]`. Las 90 del `LEEME.md` son con todos los
insumos en disco; acá corren 75 y los cinco bloques que no corren se declaran en vez de pasar
como verdes.
