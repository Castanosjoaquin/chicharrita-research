# Después del checkpoint 2: los mejores resultados, qué se hizo y cómo se usa la plataforma

**Fecha: 2026-10-28.** Resumen de la **ola 6** —el plan que siguió al checkpoint 2— con sus 26 issues,
lo que cada línea midió y el estado en el que queda la plataforma. Todas las cifras salen de archivos
versionados y cada una enlaza su fuente. Marcadores de `CLAUDE.md`: `[E]` establecido en literatura,
`[R]` reportado por una fuente, `[M]` medido por nosotros, `[H]` hipótesis nuestra, `[?]` incierto.

> **Cómo leer este documento.** La parte 1 es el punteo de resultados con sus estadísticas. La parte 2
> cuenta de qué trató el plan y qué se hizo en cada issue. La parte 3 describe la plataforma y cómo se
> corre. La parte 4 dice qué quedó abierto.

---

## 1. Los mejores resultados, con sus estadísticas

### 1.1 La recomendación que sostenemos: `BicC_Dm` 922-1221

Es la única recomendación que el proyecto defiende como tal, y está argumentada en
[`recomendacion-defendida.md`](recomendacion-defendida.md). Una molécula de ARNdc de 300 nt.

| | `BicC_Dm` 922-1221 |
| --- | --- |
| Ventanas de 21 nt que pasan el criterio de eficiencia | **26** en la molécula recortada (la cifra que se publica, `D79`); 36 contando todos los arranques en contexto y 29 contando los comparables `[M]` |
| Coincidencias perfectas de 21 nt contra el panel de seis no objetivo | **0** `[M]` |
| Alertas por bloque de ≥ 19 nt | **3**, contra 6 de la región 2121-2420 y 33 de 264-563 `[M]` |
| Ventanas de baja complejidad | 0 de las 2.500 del gen; el homopolímero más largo mide 7 nt `[M]` |
| Conservación | 36 de 36 ventanas idénticas en el transcriptoma argentino y en el genoma del Reino Unido; 32 de 36 en el de Ohio `[M]` |
| Robustez contra la región del laboratorio (264-563) | gana en el **99,1 %** de 4.368 configuraciones en contexto y en el **99,6 %** en la molécula `[M]` |
| Robustez contra la región de `C7` (2121-2420) | gana en el **36,4 %** en contexto y en el **75,6 %** en la molécula `[M]` |

**Lo que hace fuerte a esta recomendación no es el conteo.** El gen cae del primer al tercer puesto si
se ordena por densidad de ventanas eficientes `[M]`. Gana porque aguanta los tres ejes a la vez, y el
eje en el que gana —el de riesgo— es el único de los tres que no es una predicción.

**El mecanismo, dicho con precisión:** reduce la población **entre generaciones**, no corta la
transmisión de la temporada en curso. El fenotipo publicado del gen es de oviposición y ovario `[R]`.
`[H]` Si el ARNdc se aplica sobre adultos que ya adquirieron el patógeno, el efecto sobre la
transmisión de esos individuos es nulo por construcción del mecanismo.

### 1.2 Las regiones recomendadas de los seis genes del ranking

De [`ranking_v2.json`](../research/ola3/C7_ranking_v2/resultados/ranking_v2.json), a 21 nt, con el
panel de seis referencias y el humano con peso 1,00 `[M]`:

| Gen | Región recomendada | Estado de alertas |
| --- | --- | --- |
| `MP_MRFV` | 72-271 | sin alertas en este umbral |
| `CP_MRFV` | 99-298 | sin alertas en este umbral |
| `BicC_Dm` | 2121-2420 (la defendida es 922-1221, `D25`) | sin alertas en este umbral |
| `ATPaseD_Dm` | 72-371 | sin alertas en este umbral |
| `eth_Dm` | 114-313 | sin alertas en este umbral |
| `bursA_Dm` | 13-212 | sin alertas en este umbral |

**Los dos ejes no se comparan entre sí.** Por `D38`, las listas del vector y del patógeno se presentan
separadas: el número de ventanas eficientes no compara estrategias dirigidas a genes distintos, y menos
a organismos distintos.

### 1.3 El contrapunto de la V-ATPasa, que es el resultado más incómodo y más útil

`ATPaseD_Dm` es **el único candidato con evidencia de fenotipo por la vía que se quiere usar**: por
dieta, la supervivencia a cuatro días fue de ~18 % contra ~37 % del control de GFP `[R]`. Y es el que
peor perfil de riesgo tiene `[M]`:

- Su región vigente 72-371 tiene **7 ventanas con bloque perfecto de ≥ 19 nt contra humano**, frente a
  las **2,4 esperadas por azar** `[H]`.
- Sus dos regiones más conservadas son dos de las tres únicas del panel con coincidencia **perfecta de
  21 nt** contra *Homalodisca vitripennis*, y ahí el transcripto impactado es **el ortólogo del mismo
  gen que se quiere silenciar** `[M]`.

`[H]` Mejor evidencia de fenotipo y peor perfil de off-target, en el mismo candidato. Esa tensión es
un resultado, no un problema de los datos.

### 1.4 Quimeras: la contabilidad, que corrigió nuestra propia intuición

De [`quimeras-juntura-y-contexto.md`](quimeras-juntura-y-contexto.md), sobre doce quimeras `[M]`:

> **El riesgo de off-target se hereda de las partes. La eficacia no: hay que recalcularla.**

| | Cuánto |
| --- | ---: |
| Ventanas de juntura de las doce quimeras | 240 |
| De ellas, eficientes | **4** |
| De ellas, con blanco continuo de 21 nt en alguno de los genes | 8 |
| **Eficientes y con blanco continuo** | **0** |
| **Ventanas heredadas que cambiaron de veredicto** | **61** (31 pierden eficiencia, 30 la ganan) |
| Distancia máxima a la unión de una heredada que cambió | 66 nt |

`[M]` **Las cuatro ventanas de juntura eficientes no tienen blanco continuo.** Un siRNA que se produce
y no tiene a qué unirse ocupa la maquinaria y cuenta en el número sin silenciar nada. Es la advertencia
del investigador convertida en cifra: *«me puede decir que es el mejor eficiente del mundo, pero si no
va a encontrar su target en la planta o en el insecto, no va a ser»* `[R]`.

Y el hallazgo que desarma la intuición: **61 ventanas heredadas cambiaron de veredicto**, una de ellas
a 66 nt de la unión. O sea que no alcanza con revisar la juntura.

### 1.5 La quimera concreta: `BicC_Dm` + `V-ATPase B`

De [`O3`](../research/ola6/O3_quimera_bicc_vatpase_b/REPORT.md) `[M]`:

- La subunidad B de la V-ATPasa de *D. maidis* tiene **71 ventanas con coincidencia perfecta de 21 nt**,
  y de las **1.184** regiones de 300 nt que caben en su secuencia codificante **sobrevive exactamente
  una: 517-816**.
- Sobre esa región las dos moléculas posibles rinden casi lo mismo: **41** ventanas eficientes el orden
  `V-ATPase B` + `BicC_Dm` y **40** el inverso, contra **40** de la suma de las partes.
- **Sólo uno de los dos empalmes fabrica riesgo nuevo:** el orden que gana por una ventana crea un
  bloque perfecto de 19 nt que no existe en ninguno de los dos genes.

`[H]` El orden de los dos fragmentos se decide por el empalme, no por el conteo. Es el caso que mejor
muestra para qué sirve contar la juntura aparte.

### 1.6 El enumerador y el límite de la grilla

[`O4`](../research/ola6/O4_enumerador_quimeras/REPORT.md) enumera combinaciones de dos genes y las
ordena bajo un objetivo declarado antes. Lo medido sobre la retícula `[M]`:

| Paso de la grilla | Plegados | Corrida |
| --- | ---: | --- |
| 1 | 129.761.738 | **no se corre** (~71 días de una máquina; `D95`) |
| 2 | 16.816.657 | no corrida (~9 días, repartible) |
| 5 | 1.177.056 | no corrida |
| 10 | 173.289 | **corrida**, ~5 h |

**El paso mueve el primer puesto.** Con paso 50 ganaba `Q_BicC_Dm_1951-2450__VATPaseB_Dm_1001-1100` con
64 ventanas heredadas; con paso 10 gana `Q_BicC_Dm_1961-2460__VATPaseB_Dm_1001-1100` con **65**, y el
anterior cae al segundo puesto `[M]`. El margen es de **una ventana sobre 65**, así que lo medido es que
**el orden de esa grilla no es estable al paso**, no que la gruesa eligiera mal. `[?]` Si `--paso 1` lo
movería otra vez sigue sin saberse.

### 1.7 Los pares por mecanismo, que es lo que el investigador pidió

[`F4`](../research/ola6/F4_pares_por_mecanismo/REPORT.md) conecta el eje de fenotipo al enumerador: en
vez de elegir por densidad, arma pares de candidatos **cuyos mecanismos no se solapan** (`D67`) `[M]`:

| Alcance | Pares elegibles |
| --- | ---: |
| Los tres mecanismos de `D67` (reproducción, movilidad, letalidad) | **229** |
| Con la cuarta categoría, transmisión, declarada pero sin ADR | 118 |
| **Restringido a *D. maidis*** | **8** |

`[H]` La restricción a la propia especie es la que importa para un diseño, y deja **ocho** pares. El
mecanismo `movilidad` **descansa en un solo candidato** del catálogo, `DM-02`, y su réplica más cercana
—`DM-03`, la otra subunidad de la misma bomba, misma especie, misma vía— midió el efecto sobre alas y
**no dio significativo** `[M]`. Es una pata frágil del esquema de `D67`.

### 1.8 El recomendador de genes, y su resultado más honesto

[`F3`](../research/ola6/F3_recomendador_genes/REPORT.md) ordena **genes**, no regiones, sobre las 36
filas del catálogo de `C5`: 25 entran al orden y 11 quedan afuera por su etiqueta de fenotipo `[M]`.
No usa una suma ponderada global: agrupa en **cohortes por ejes disponibles** y no compara entre
cohortes, porque imputar un eje ausente fabrica un número que la fuente no da (`D87`).

El primer puesto de la cohorte con los cuatro ejes es un **empate declarado de tres**: `DM-05` (`eth`,
0,9868), `DM-03` (`V-ATPase D`, 0,9865) y `DM-02` (`V-ATPase B`, 0,9664) `[M]`.

**Y el resultado que más vale, que es negativo:** el eje de off-target —el único de los cinco que **no**
depende del criterio de eficiencia sin validar en hemípteros— **no cambió ningún primer puesto**. El
empate de tres sigue intacto y los cuatro primeros de la cohorte siguiente caen dentro de **0,021**
contra un umbral de empate de 0,05 `[M]`. Refuerza por otra vía lo que `D65` ya había decidido: el
conteo no decide entre candidatos.

### 1.9 Dos lecciones de método que valen más que los números

**Primera: el panel se autoacierta si contiene la especie de la secuencia.** Pasó dos veces `[M]`:

| Caso | Qué publicaba | Qué era |
| --- | --- | --- |
| Cuatro filas de `C5` con secuencia sustituta de *M. quadrilineatus*, panel que la incluía | 1835/1835, 663/663, 1487/1487, 4409/4409 ventanas con coincidencia perfecta | la secuencia contra sí misma (`D99`) |
| `HE-06`, actina de *H. vitripennis*, que está en el panel de seis | 98,6 % de sus ventanas con bloque ≥ 19 nt | lo mismo (`D100`) |

`[H]` Ninguno es un error de quien lo midió: la sustitución estaba declarada fila por fila. Es lo que
pasa cuando el panel contiene la especie de la que se tomó prestada la secuencia. **La regla queda
escrita y es verificable antes de tamizar.**

**Segunda: un conteo de off-target sin su nulo puede estar leyendo un piso.** Una secuencia **sin
homología** —permutada conservando su composición— trae **0,5 a 0,7 %** de ventanas con bloque de
≥ 19 nt coincidente, y en el peor caso 3,4 % `[M]`. No es cero. Por eso `eth` (0,9815) y `burs-alpha`
(1,0000) **no se distinguen del azar**, y sólo `V-ATPase B` (0,8827) queda claramente por encima.
`[?]` La causa del piso no se averiguó.

---

## 2. De qué trató el plan, y qué se hizo en cada issue

El [plan de la ola 6](../docs/plan_ola6/PLAN_OLA6.md) se escribió el 26 de octubre, después del
checkpoint 2, y agrupó el trabajo en cuatro frentes. **26 issues, 25 cerrados.**

### Grupo A — cerrar lo que quedaba abierto (`R1` a `R6`)

| Issue | Qué se hizo |
| --- | --- |
| **#15 `R1`** | Firmar las alertas, con la persistencia primero para que el trabajo no se pierda |
| **#16 `R2`** | Que un entregable **llame de verdad** a la compuerta de alertas, en vez de describirla |
| **#17 `R3`** | `estado.html` con la ola 5 y el checkpoint 2 adentro |
| **#18 `R4`** | `UMBRAL_OFF_ALERTA` de 17 a 19, alineado con el piso de `D28`: de 23.612 ventanas, el umbral 17 marcaba 2.338 alertas y el 19 marca 436, o sea que **1.902 alertas (81,4 %) eran ruido** bajo el piso `[M]`. Ninguna región pasa a apta o inapta (`D90`) |
| **#19 `R5`** | Las dos cifras viejas de los entregables, corregidas |
| **#20 `R6`** | El tercer marco de conteo y el empate declarado (`D66`, `D80`) |

### Grupo B — lo que dejó la reunión

| Issue | Qué se hizo |
| --- | --- |
| **#21 `O1`** | La contabilidad de la juntura **sube al entregable**: el investigador la nombró como el diferencial posible y vivía enterrada en un `REPORT` de la ola 5 |
| **#22 `O2`** | La secuencia de `V-ATPase B` por dos vías; el CDS se regenera y se autoverifica (1.503 nt, 500 aa, 10 exones) `[M]` |
| **#23 `O3`** | La quimera `BicC_Dm` + `V-ATPase B` con las tres cuentas separadas (§1.5) |
| **#24 `O4`** | El enumerador de quimeras como feature, con el objetivo declarado antes (§1.6) |

### Grupo C — el encadenamiento como producto

| Issue | Qué se hizo |
| --- | --- |
| **#25 `F1`** | Transferencia de anotación por homología. Es lo que permite leer el transcriptoma que el investigador iba a mandar: *D. maidis* tiene tres ensamblados públicos y **ninguno anotado** `[M]`. Sobre `GITV01` (56.117 contigs), la regla estricta preregistrada deja **4.110 contigs (7,3 %)** con ortólogo recíproco y nombre informativo; la lectura inclusiva de empates, que es la que pasó el control, deja **7.832 (14,0 %)** `[M]` |
| **#26 `F2`** | La evidencia leída en lenguaje natural, como **plantilla determinista más verificador determinista** y no como llamada a un modelo (`D85`). El verificador audita cada párrafo contra su ficha y no mira quién lo escribió |
| **#27 `F3`** | El recomendador de genes, con el criterio escrito antes de rankear (§1.8) |
| **#39 `F4`** | El eje de fenotipo de `F3` conectado al enumerador de `O4` (§1.7) |

### Grupo D — lo que depende del equipo

| Issue | Estado |
| --- | --- |
| **#28 `E1`/`E2`** | **Abierto.** Falta registrar la fecha y el texto del correo enviado, y elegir el canal por el que se le entrega el port |

### Las líneas que salieron del propio trabajo (`R7` a `R13`, y el inventario)

No estaban en el plan: aparecieron al verificar lo que el plan produjo.

| Issue | Qué se hizo |
| --- | --- |
| **#30 `R7`** | La compuerta exige presencia en el inventario, y las seis regiones de 22 nt |
| **#32 `R8`** | ¿Tiene ortólogo en el panel la quitinasa que impacta `eth_Dm` 193-392? Rehecho contra un proteoma anotado: comparando accesiones cambian **2 de 5** veredictos, pero los dos caen en la **isoforma X2 del mismo producto**, y colapsando por producto cambian **0 de 5** `[M]`. La limitación estaba bien declarada y **no afectaba el resultado** |
| **#33 `R9`** | Dos tandas de cifras publicadas pedían paneles distintos: no había contradicción, cada medición tiene su panel y su directorio (`D83`) |
| **#34 `R10`** | `ranking_v2.json` no era byte-reproducible porque el orden de claves no estaba fijado (`D76`). Las dos regeneraciones y el archivo publicado tienen hoy el mismo `sha256` `[M]` |
| **#35 `R11`** | Los tres límites abiertos de la compuerta de `D72`; el censo de generadores pasó de **2 de 8 a 8 de 8** `[M]` |
| **#37** | **El inventario de corridas pendientes.** Barrió las 14 casillas y encontró que **de los cinco bloqueos que atribuía a falta de insumo, tres no eran de insumo**: uno era el propio censo rompiendo un ancla con `--muestras 50`, otro era el directorio desde donde se corría el test, y el tercero era una cifra mal estimada por tres órdenes de magnitud `[M]` |
| **#41 `R13`** | De dónde salía la brecha con `C12`: **es enteramente el normalizador de nombres** (+7,0 puntos; el alineador +0,2 y la submuestra −0,7). De los 515 desacuerdos que el criterio de `F1` convierte en acuerdos, el **77,9 % se separaba sólo por el sufijo de isoforma** `[M]`. La tabla de `C12` no se tocó |
| **#42, #43, #44** | Las tres decisiones que el inventario dejó: archivar la grilla fina (`D95`), recuperar secuencias para el eje de off-target (`D97` a `D100`) y el límite de `F2` (`D96`) |

### Un defecto de método que el barrido encontró, y que vale aparte

Al destrabarse, un generador **empezó a escribir en una carpeta versionada**, y la primera corrida del
censo —con `--muestras 50`— **reemplazó dos cifras publicadas con una corrida de cincuenta sorteos**:
39.675 líneas insertadas y 101.943 borradas `[M]`. Se revirtió antes de commitear.

`[H]` Es el defecto más caro de los dos que aparecieron, porque **no avisa**: deja los archivos con
aspecto normal y sólo se nota en el `git diff`. El auditor que lo buscó en todo el árbol encontró **43
módulos** que escriben en versionado sin poder redirigir la salida, pero contar sus tres partes por
separado mostró que los accionables eran **cuatro** y que de esos **uno solo** había perdido datos.
Contar «43 módulos con el defecto» habría pedido 43 arreglos.

---

## 3. Cómo quedó la plataforma, y cómo se usa

La plataforma no es un servicio: es un conjunto de herramientas de línea de comandos, reproducibles y
versionadas, más una vista de lectura en HTML. **El markdown es la fuente de verdad; el HTML es sólo la
vista.**

### 3.1 El motor: el port de si-Fi21

[`tools/sifi21_port/`](../tools/sifi21_port/README.md) es la reimplementación del criterio de eficiencia
de si-Fi21, la herramienta en la que el investigador dijo que se basa el pipeline de EPILAB. Corre sin
interfaz gráfica y tiene **dos modos**: `fiel`, que reproduce el programa original para auditar números
hechos con él, y `corregido`, con los arreglos documentados.

**Está verificado contra el original en los cuatro genes** `[M]`: si-Fi21 con su interfaz y sus valores
por defecto da 42, 32, 133 y 212 siRNA eficientes para `ATPaseD_Dm`, `CP_MRFV`, `MP_MRFV` y `BicC_Dm`, y
el port en modo fiel con el mismo RNAplfold 2.1.5 da **los mismos cuatro números**.

```bash
# el criterio de eficiencia sobre un FASTA
python tools/sifi21_port/run_sifi.py --modo fiel --backend vienna <entrada>

# off-targets por siRNA contra referencias locales (Aho-Corasick, no BLAST)
python tools/sifi21_port/offtarget_21nt.py --size 21 --mm1 \
    --consulta <fasta> --db <refs>/*.fna.gz --salida <dir>

# el ranking v2, con las anclas adelante
python tools/sifi21_port/ranking_v2.py --trabajo work/sifi_v2 \
    --json research/ola3/C7_ranking_v2/resultados/ranking_v2.json
```

### 3.2 Las features del encadenamiento

| Qué | Dónde | Cómo se corre |
| --- | --- | --- |
| Transferencia de anotación por homología (`F1`) | `research/ola6/F1_transferencia_homologia/scripts/` | `transferir_anotacion.py`, con `diamond` local |
| Evidencia en lenguaje natural (`F2`) | `pipeline/evidencia_en_prosa.py` | plantilla + `verificar_procedencia()`, deterministas |
| Recomendador de genes (`F3`) | `research/ola6/F3_recomendador_genes/scripts/` | `01_eje_fenotipo.py` → `02_eje_esencialidad.py` → `03_orden.py` → `04_segundo_orden.py` |
| Ejes 3 y 4 del recomendador | mismos `scripts/` | `05_eje_conservacion.py`, `07_eje_offtarget.py`, `10`–`13` para las filas recuperadas |
| Pares por mecanismo (`F4`) | `research/ola6/F4_pares_por_mecanismo/scripts/` | `00_anclas.py` primero: si las tres anclas no pasan, no se sigue |
| Inventario de alertas y compuerta | `research/ola4/M6_alertas/scripts/` | `identidad.py` → `tabla_alertas.py` → `compuerta.py` |

### 3.3 Las verificaciones que corren antes que nada

Esto es lo que distingue a la plataforma de un montón de scripts, y conviene usarlo:

- **Anclas.** Varias líneas empiezan reproduciendo un número ya publicado y **abortan si no coincide**.
  El tamizado de las filas nuevas, por ejemplo, corre `eth_Dm` en el mismo lote y verifica que reproduce
  `work/sifi_v2/` **columna por columna** antes de leer un solo resultado nuevo.
- **Fuga de secuencias.** `python tools/verificacion/sin_secuencias.py` busca nucleótidos en el árbol
  versionado, en el índice y en el historial. Hay un gancho de pre-commit que es *fail-closed*.
- **Existencia en disco.** `python tools/generar_estado.py` valida que **cada archivo que la página
  nombra exista de verdad** e imprime cuántos faltan.
- **Preregistro.** El criterio se escribe y se commitea **antes** del primer cálculo, y lo que cambia
  después entra como enmienda con fecha. Si una enmienda se escribe sabiendo el resultado, se dice.

### 3.4 La vista de lectura

`index.html` en la raíz es la portada; [`estado.html`](../estado.html) dice qué está hecho, qué falta y
qué decisiones están abiertas, y **se genera con su script, no se escribe a mano**. Cada `.md` de
`entregables/` tiene su `.html` hecho con `python tools/md_a_html.py <entrada.md> <salida.html>`.

### 3.5 La memoria del proyecto

Cuatro archivos en `00_meta/` que se actualizan siempre, no al final:
[`DECISIONS.md`](../00_meta/DECISIONS.md) (100 ADR), `CAMINOS_PROBADOS.md` (los descartes, que valen
tanto como los hallazgos), `PREGUNTAS_ABIERTAS.md` (102 entradas) y `FUENTES.md`.

---

## 4. Qué quedó abierto

**Del plan, una sola cosa:** el issue **#28**, que es del equipo —registrar la fecha y el texto del
correo enviado, y elegir el canal de entrega del port—.

**Decisiones que esperan a una persona, no a una máquina:**

- **13 filas del inventario de alertas siguen en «pendiente»**, entre ellas las cuatro de `V-ATPase B`
  517-816. Ninguna la firma el motor (`D48`, `D68`, `D73`), y una región con alerta sin firmar **no sale
  como recomendada**, así que esto frena de hecho a la compuerta.
- El peso de exposición de *H. vitripennis*, que `D47` dejó abierto y que varias lecturas necesitan.
- Escribir el criterio de commits como enmienda a `D5`, porque la práctica real difiere de lo escrito.

**Límites del dato, que no se cierran con trabajo:**

- **No hay etiquetas de eficacia para el vector.** Ningún dato experimental de silenciamiento en
  *D. maidis* respalda el umbral, así que los barridos miden **fragilidad de la recomendación**, no si el
  umbral es correcto. La correlación entre el filtro y la eficacia medida da ρ = +0,142, IC 95 %
  [−0,247, +0,492], n = 29, en *Tribolium castaneum* `[M]`: no concluyente.
- **La asimetría temporal.** La ventana de latencia del patógeno es de unos **20 días** `[R]` y todos los
  ensayos abiertos en la especie miden el desenlace a los **4 o 5 días** `[R]`. `[H]` Si el insecto
  transmite antes de que el silenciamiento haga efecto, matarlo no corta la transmisión.
- **El eje de expresión en el tejido expuesto no existe para ningún candidato** y es el que más
  importaría para una vía de entrega oral `[H]`: los tres transcriptomas públicos son de cuerpo entero y
  huevos.

**Del eje de off-target, con su matiz:** cubre **19 de las 36 filas**. De las 17 restantes, tres tienen
ausencia de accesión **comprobada sobre el texto completo**; **nueve son provisionales**, porque sólo se
pudo leer el resumen, y «no está en el resumen» no es «no está en el paper» `[?]`; tres tienen el **PDF
abierto** pero su dominio no está en la lista permitida del entorno; y una cita un andamio genómico en
vez de un transcripto.
