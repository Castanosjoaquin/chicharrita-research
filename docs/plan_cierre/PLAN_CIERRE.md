# Plan de cierre — lo que se puede hacer sin esperar nada más

**Fecha del plan:** lunes 2026-10-26, después del checkpoint 2.
**Qué contesta:** la reunión de hoy, transcripta en
[`research/checkpoints/checkpoint2.md`](../../research/checkpoints/checkpoint2.md).

**Para qué sirve este archivo.** Después del checkpoint quedaron quince pendientes sueltos
entre el issue #14, el generador de estado y las notas de la ola 5. Se verificaron uno por uno
contra el repositorio y se cruzaron con lo que el investigador dijo hoy. El resultado es que
**seis se pueden hacer ya**, cuatro esperan un archivo que él va a mandar, dos dependen de una
decisión del equipo y uno ya estaba hecho. Este plan separa los cuatro grupos y deja cada tarea
del primero con todo lo que hace falta para ejecutarla sin releer la conversación.

**Cómo usarlo.** Las seis tareas de §2 a §7 son **independientes entre sí**: no comparten
archivos salvo donde se dice, y cada una se puede commitear sola. Abrí una sesión, pedile que
lea la sección de la tarea y la ejecute. El orden sugerido está en §11.

> **La regla que más importa acá.** Tres de las seis tareas **no mueven ninguna cifra
> publicada** y se pueden hacer sin consultar a nadie. Las otras tres sí tocan algo que ya está
> escrito en un entregable, y están marcadas **«cambia cifras publicadas»**: esas no se hacen
> por cuenta propia. Cada una dice a quién le toca decidir.

---

## 0. Qué cambió hoy, en cuatro líneas

La reunión **no corrigió nada de fondo**. Validó la lectura de `BicC_Dm` como gen poblacional,
pidió el análisis de sensibilidad a los pesos que ya está hecho, y volvió a validar la ruta de
homología. Lo único nuevo que pidió son quimeras que combinen fenotipos que no se solapan.

Lo que **destrabó**, y es la razón de que este plan exista: dio, en sus propias palabras, el
razonamiento que faltaba para firmar las alertas de *Homalodisca vitripennis*, y cerró la
espera por el peso de exposición diciendo que no va a haber número. Las dos cosas estaban
bloqueando tareas que ahora se pueden hacer.

Lo que **prometió mandar**: el transcriptoma de *Dalbulus maidis* en un zip.

---

## 1. Las quince, clasificadas

| # | Pendiente | Estado | Dónde |
| --- | --- | --- | --- |
| 1 | Firmar las 17 alertas | **se puede ya** — hoy lo destrabó | §2 |
| 2 | Que un entregable llame a la compuerta | **se puede ya** | §3 |
| 3 | `estado.html` sin ola 5 ni checkpoint 2 | **se puede ya** | §4 |
| 4 | `UMBRAL_OFF_ALERTA = 17` contra D28 | **se puede ya** | §5 |
| 5 | Las dos cifras viejas de los entregables | **se puede ya**, cambia cifras publicadas | §6 |
| 6 | El tercer marco y el empate declarado | **se puede ya**, cambia cifras publicadas | §7 |
| 7 | `C11` — conservación de `eth` y `burs-alpha` | espera el transcriptoma | §8 |
| 8 | La secuencia de `V-ATPase B` para la quimera | espera el transcriptoma | §8 |
| 9 | El marco intermedio en `GHCC01` | espera el transcriptoma (quizá sea el mismo archivo) | §8 |
| 10 | Verificar las posiciones de la planilla | espera el transcriptoma | §8 |
| 11 | Fecha y texto del correo enviado | depende del equipo | §9 |
| 12 | Cómo se le entrega el port | depende del equipo | §9 |
| 13 | El mensaje del gancho de pre-commit | **ya estaba hecho**, no lo rehagas | §10 |
| 14 | Apareamiento parcial de las ventanas de juntura | abierto, necesita experimento | §10 |
| 15 | Cuál modelo de la regla terminal predice mejor | abierto, él mismo dijo que no se cierra | §10 |

---

## 2. `R1` — Firmar las 17 alertas

**Por qué es la primera.** Es la que la reunión destrabó, y arregla un problema real: hoy
**una alerta no leída queda operativamente igual que una aceptada**. Las 17 filas de
`research/ola4/M6_alertas/resultados/alertas.tsv` tienen `decision_usuario = "pendiente"` y
`justificacion_usuario = "pendiente: la escribe el usuario, no el motor"`, verificado. El veto
viejo descartaba por omisión; la tabla que lo reemplazó no descarta nada.

**Lo que hay que saber antes de tocar nada.** La validación de una firma está implementada en
`tools/sifi21_port/alertas.py:230` (`validar_decision`) y es estricta a propósito. Una firma
pasa sólo si cumple las tres:

1. `decision_usuario` está en el vocabulario cerrado: `pendiente`, `aceptada` o `bloqueante`
   (`alertas.py:202`).
2. `justificacion_usuario` **no empieza con «pendiente»** y tiene **al menos 40 caracteres**
   (`PROSA_MINIMA`, `alertas.py:69`). Cambiar una palabra no alcanza, y eso es deliberado.
3. La justificación **cita la fila**: tiene que nombrar el `gen_locus` o una de las accesiones
   de `gen_transcriptos` de esa fila (`cita_la_fila`, `alertas.py:216`). Es un piso mecánico y
   grosero —se cumple pegando una accesión— pero distingue una justificación escrita sobre esa
   fila de un párrafo genérico copiado a las diecisiete.

**Las tres filas que importan, con sus datos.** Son las únicas con coincidencia perfecta de
21 nt, las tres contra *H. vitripennis*, y en las tres el transcripto impactado es el ortólogo
del gen que se quiere silenciar:

| gen | región | 21/21 | ≥19 | `gen_locus` | `gen_transcriptos` |
| --- | --- | --- | --- | --- | --- |
| `BicC_Dm` | 264-563 | 22 | 30 | `LOC124362408` | `XM_046816879.1` |
| `ATPaseD_Dm` | 151-450 | 3 | 7 | `LOC124356774` | `XM_046807969.1` |
| `ATPaseD_Dm` | 137-436 | 3 | 7 | `LOC124356774` | `XM_046807969.1` |

**El argumento que ahora existe y antes no.** Hoy el investigador dijo tres cosas que juntas
son la justificación de esas tres filas, y conviene **citarlo a él** en vez de inventar un
criterio nuestro `[R]`:

- Que el organismo **no estaba en su panel**: *«el bicho ese yo no lo tenía»*.
- Que no está en la Argentina y por eso *«puede no importar»*, pero que *«puede venir
  eventualmente y tal vez si la querés matar»*.
- Que lo que corresponde no es resolverlo sino mostrarlo: *«si vos querés ser específico para
  esta, mostrar que esas posibles decisiones están presentes es como el extra»*.

Las citas exactas están en `research/checkpoints/checkpoint2.md`, sección «La región nueva, y
el cicadélido que no está en la Argentina», y las transcripciones crudas al lado.

**Las otras catorce.** Son 0 de 21/21, con 2 a 4 coincidencias de ≥19 nt, y `evidencia_clave`
es `gen_no_relacionado` o `sin_anotacion_de_gen`. Verificado: ninguna de las seis filas de
regiones **vigentes** tiene una coincidencia perfecta de 21 nt. Se firman con un argumento
breve por fila, que igual tiene que citar su propio locus para pasar el validador.

**Qué hay que hacer.**

1. **Primero, el problema de persistencia.** `tabla_alertas.py:289` escribe `"pendiente"`
   **fijo**, así que regenerar la tabla borra cualquier firma escrita a mano. Antes de firmar
   hay que decidir dónde viven las decisiones para que sobrevivan a una regeneración. La opción
   recomendada: un archivo aparte —`decisiones.tsv`, con clave `gen` + `region` +
   `organismo_corto`— que `tabla_alertas.py` lea y vuelque sobre las filas que genera, cayendo
   a `pendiente` para las que no estén. Es poco código y evita el fallo obvio de que la firma
   se pierda la próxima vez que alguien corra el script.
2. Escribir la decisión y la justificación de las tres filas de *H. vitripennis*, con sus
   citas y nombrando el locus o la accesión.
3. Escribir las catorce restantes.
4. Correr la prueba: `tools/sifi21_port/test_alertas.py` ya cubre el validador y la compuerta.
5. Registrar en `00_meta/DECISIONS.md` el ADR de la firma, apoyado en D48 y en D66.

**Criterio de terminado.**

- [ ] `alertas.validar_decision` pasa sobre las 17 filas.
- [ ] Ninguna justificación empieza con «pendiente» ni tiene menos de 40 caracteres.
- [ ] Las tres filas de *H. vitripennis* citan al investigador con la cita textual.
- [ ] Regenerar la tabla con `tabla_alertas.py` **no borra** ninguna firma.
- [ ] El ADR está escrito.

**Qué no hacer.** No firmar las diecisiete con el mismo párrafo: el validador lo permite si
cada una nombra su locus, pero vacía de sentido el mecanismo. Y no convertir la firma en un
veto automático: D48 decidió lo contrario, y el investigador lo confirmó en su carta del 22.

---

## 3. `R2` — Que algún entregable llame a la compuerta

**Por qué.** `alertas.exigir_decidida()` está implementada en `tools/sifi21_port/alertas.py:298`
y tiene prueba, pero **ningún entregable la llama** —verificado: las únicas referencias fuera
de la prueba están en `research/ola4/M6_alertas/scripts/compuerta.py:53` y en los REPORT—. Una
compuerta que nadie llama no es una compuerta. La consecuencia concreta es que nada en el
código impide usar una región cuya fila sigue en «pendiente».

**Depende de `R1`**, porque la compuerta recién sirve cuando las filas están firmadas. Si se
corre antes, falla sobre las seis regiones vigentes y eso es correcto.

**Qué hay que hacer.** Hacer que la ruta que produce una recomendación llame a
`exigir_decidida(filas, gen, region)` y falle si la región no está decidida. El lugar natural es
donde se arma la recomendación publicada, no un script suelto de la ola 4.

**Criterio de terminado.**

- [ ] Existe al menos un punto en el código del port o del pipeline que no puede producir una
      región recomendada sin que su fila esté decidida.
- [ ] Hay una prueba que lo demuestra fallando con una fila en «pendiente».

---

## 4. `R3` — `estado.html` con la ola 5 y el checkpoint 2

**Por qué.** Verificado: `estado.html` y `tools/generar_estado.py` son del 24 de octubre y
tienen **cero** menciones de `ola5`, `N1_regla`, `N3_marcos` o `N4_quimeras`. O sea que la
página de estado del proyecto no tiene el hallazgo del conteo, los tres marcos, las quimeras ni
el expediente de la región — y tampoco el checkpoint 2.

**Ojo con la convención:** `estado.html` **no se edita a mano**. Se genera con
`python tools/generar_estado.py` desde la raíz, y la lista HECHO/FALTA está codificada dentro
del script. Lo que hay que editar es el script.

**Qué hay que hacer.**

1. Agregar a `HECHO` las siete líneas de la ola 5 (`N1` a `N5`, `N9`, `N10`) con sus rutas, y
   el checkpoint 2 con `research/checkpoints/checkpoint2.md`.
2. Revisar `FALTA` (`generar_estado.py:133`) contra este plan: varias filas quedaron viejas.
   En particular, «Los dos pesos de M5» tiene que reescribirse según §7, y «Qué cifra de
   ventanas eficientes se publica» se cierra o no según §6 — **si §6 no se hizo, esa fila
   se queda**.
3. Regenerar y mirar la página en el navegador, no sólo el diff.

**Criterio de terminado.**

- [ ] La página menciona las siete líneas de la ola 5 y el checkpoint 2.
- [ ] Ninguna fila de `FALTA` describe algo que ya se hizo.
- [ ] La página se abrió y se miró.

---

## 5. `R4` — `UMBRAL_OFF_ALERTA` contra el piso de D28

**Por qué.** `pipeline/region_scoring.py:51` tiene `UMBRAL_OFF_ALERTA = 17`, y D28 decidió no
reportar coincidencias de 16 a 18 nt. Es una contradicción entre el código y una decisión
escrita.

**El alcance ya está verificado y es chico: no mueve ninguna cifra publicada**, y el cambio
queda contenido en ese módulo. Por eso esta tarea no lleva la marca de cifras publicadas.

**Qué hay que hacer.** Leer D28 en `00_meta/DECISIONS.md`, alinear la constante con su piso, y
correr lo que dependa de `region_scoring.py` para confirmar que ninguna salida cambia. Si
alguna cambia, **parar**: entonces el alcance no era el verificado y pasa a ser una tarea con
cifras publicadas.

**Criterio de terminado.**

- [ ] La constante respeta el piso de D28, o el código explica por escrito por qué no debe.
- [ ] Se confirmó que ninguna cifra publicada se mueve.

---

## 6. `R5` — Las dos cifras viejas · **cambia cifras publicadas**

**Quién decide:** el equipo. No se hace por cuenta propia.

**Por qué.** Dos entregables publican una cifra que la ola 5 ya corrigió, y si el investigador
abre los documentos viejos ve números que contradicen lo que se le contó hoy. Verificado:

| Archivo | Qué dice todavía |
| --- | --- |
| `entregables/checkpoint2-una-pagina.md` | «pasa de **20 a 36** ventanas que pasan el filtro» y «**32 de sus 36** ventanas son idénticas en los tres transcriptomas» |
| `entregables/para-el-investigador.md` | «922-1221 (**36 ventanas** que pasan el filtro, **32 idénticas** en los tres transcriptomas públicos)» |

Mientras que `entregables/recomendacion-defendida.md` y `entregables/reunion-lunes.html`
publican **26** y declaran que el «32 contra 22» **no es sostenible**.

**Lo que ya está decidido y no hay que volver a discutir:** D63 fijó que la cifra que se publica
para una región candidata es la del marco de la molécula, que es **26**; D64 retiró el «32
contra 22» y lo reemplazó por la cobertura declarada por fuente, porque `GCWP01` no cubre un
solo nucleótido de 922-1221; y D65 le retiró al conteo el papel de argumento entre 922-1221 y
2121-2420. Las tres son del 25 de octubre.

**Lo que agrega la reunión de hoy:** el argumento de la juntura —*«me puede decir que es el
mejor eficiente del mundo, pero si no va a encontrar su target en la planta o en el insecto, no
va a ser»*— empuja en la misma dirección, porque lo que vale es la molécula que se sintetiza y
no el conteo en contexto `[R]`. O sea que la corrección quedó más sostenida que antes.

**Qué hay que hacer.** Corregir las dos cifras **dejando la frase vieja tachada con la nueva al
lado**, que es la convención de corrección del repositorio —se usó ya en
`PLAN_DESARROLLO.md` y en el documento del investigador—. No se borra: se corrige a la vista.

**Criterio de terminado.**

- [ ] Los cuatro entregables dicen la misma cifra para la misma región y el mismo marco.
- [ ] Cada corrección dice qué decía antes, qué dice ahora y por qué (D63, D64, D65).
- [ ] Los `.html` se regeneraron con `python tools/md_a_html.py entrada.md salida.html`.

---

## 7. `R6` — El tercer marco y el empate declarado · **cambia cifras publicadas**

**Quién decide:** el equipo. Son dos decisiones chicas y ninguna necesita cómputo: las dos
mediciones ya están hechas.

**La primera: adoptar o no el tercer marco.** Él lo propuso en la carta del 25 —contar las
ventanas de la molécula pero con la accesibilidad evaluada en el transcrito blanco— y
`research/ola5/N3_marcos/` lo midió: da **29**, contra 36 en contexto y 26 en la molécula. Se
sigue publicando 26 y la adopción quedó sin decidir. **Hoy no lo volvió a mencionar**, así que
la decisión es nuestra. El argumento de la juntura respalda seguir publicando 26 y declarar 29
al lado, pero conviene escribirlo como decisión y no dejarlo implícito.

**La segunda: el tercer puesto.** Queda abierto si se reporta como **empate declarado** o se
sigue ordenando. Hoy él pidió exactamente el análisis que lo respalda: *«si probás un par de
pesos distintos y cambia mucho, o todo medio parecido y en realidad tal vez esos pesos no
importan tanto»* `[R]`. Con eso, reportar un empate medido es contestar su pregunta, no
esquivarla.

**Y una advertencia que hay que tener presente.** La medición de `M5` dice que la decisión sobre
*H. vitripennis* **no es cuánto sino cero o no cero**: entre 0,05 y 1,00 de peso relativo al
maíz no cambia nada. Si se adopta cero a secas, **dejan de estar sostenidas tres afirmaciones
publicadas**, listadas en `research/ola4/M5_dos_ejes/NOTAS_PARA_META.md`. Por eso D66 decidió no
adoptar un valor sino declarar la decisión abierta y mostrar los dos extremos — que además es
literalmente lo que él pidió. **Esta tarea aplica D66, no lo reabre.**

**Criterio de terminado.**

- [ ] Hay un ADR por cada una de las dos decisiones, con su alternativa y su consecuencia.
- [ ] El entregable muestra, en el mismo lugar, qué pasa con exposición cero y con exposición
      no cero, incluido que tres de las seis regiones recomendadas se mudan.
- [ ] Ninguna de las tres afirmaciones de `M5_dos_ejes/NOTAS_PARA_META.md` quedó publicada sin
      su condición al lado.

---

## 8. Lo que espera el transcriptoma

Él se comprometió a mandarlo en un zip, con una advertencia operativa que hay que presupuestar:
*«los IDs están hechos por el que hizo el transcriptoma, no coinciden los nombres, no vas a
poder encontrar, pero sí por identidad u homología»* `[R]`. **La entrada es alineamiento, no
leer una anotación.**

| Qué | Qué hacer cuando llegue |
| --- | --- |
| `C11` — conservación de `eth` y `burs-alpha` | Es la línea que estaba bloqueada por este insumo: ninguno de los tres transcriptomas públicos contiene esos dos genes |
| La secuencia de `V-ATPase B` | Es el candidato del eje de alas (`DM-02`, alas deformes) y el único insumo que bloquea la quimera de fenotipos complementarios |
| El marco intermedio en `GHCC01` | Necesitaba el contig `GHCC01002326.1`, que no está en la máquina |
| Las posiciones de la planilla | Verificarlas contra la fuente que el laboratorio usa de verdad |

> **Una hipótesis que conviene chequear apenas llegue.** `GHCC01` es el transcriptoma argentino
> de Pergamino, y él dijo que el suyo *«no está en NCBI, está en otro lado»* pero que es *«el
> transcriptoma que está publicado»*. Puede que sean el mismo. Si lo es, el zip cierra de una
> el hueco del marco intermedio además de los otros tres. **No se da por cierto: se verifica
> comparando contra lo que ya tenemos de `GHCC01`** `[?]`.

**Lo que NO espera el transcriptoma, aunque lo parezca:** `GCWP01` no es un pendiente sino un
límite —cubre 609 de 2.520 posiciones y ninguna de 922-1221—, y se informa como «sin datos», no
como cero (D64).

---

## 9. Lo que depende del equipo, no de él

- **Fecha y texto del correo enviado.** El repositorio sigue sin registrarlo. El borrador tiene
  siete preguntas y `PLAN_DESARROLLO.md` §8 decía cinco. Sin el texto enviado no se puede
  cotejar ninguna numeración.
- **Cómo se le entrega el port.** La auditoría está hecha y en verde: 36 archivos, cuatro con
  nucleótidos y los cuatro con fuente pública escrita, cero hallazgos sin exceptuar
  (`research/ola5/N9_paquete_port/`). Lo pidió dos veces y se le dijo que se le mandaba después
  de revisarlo, y ya está revisado. **Hoy se abrió el canal solo:** él va a escribir para mandar
  el zip, y responder ese correo con el paquete es el momento natural.

---

## 10. Lo que no hay que hacer

**El mensaje del gancho de pre-commit: ya está bien.** Circuló la idea de que rechaza con
«RECHAZADO: hay secuencias de EPILAB» también cuando no pudo verificar. **Es falso, verificado
en el código:** `sin_secuencias.py` reserva el código 1 para «miré y encontré» y sale 2 en
cualquier otro caso, incluido `openpyxl` ausente (`sin_secuencias.py:637` y `:747`); el gancho
manda todo lo que no sea 0 ni 1 a `no_pude_verificar()`, que tiene su propio texto y explica
cómo seguir. Lo que sí sigue siendo cierto es la molestia operativa: el `python3` del PATH puede
no tener `openpyxl` aunque el de Anaconda sí.

**Dos preguntas que ningún trabajo de escritorio cierra**, y las dos están bien declaradas:

- Si una complementariedad incompleta les da actividad a las ventanas de juntura. Medimos la
  coincidencia exacta de 21 nt; si una parcial sirve, esas ventanas no serían inútiles sino
  menos útiles, y no lo sabemos `[?]`.
- Cuál de los dos modelos de la regla terminal predice mejor. `M4` midió que harían falta 2.784
  siRNA replicando el único diseño etiquetado que encontramos, y él coincidió en que hace falta
  un experimento `[R]`.

---

## 11. El orden sugerido

**Primero las tres que no mueven ninguna cifra publicada**, porque no necesitan que nadie
decida nada y dejan el repositorio consistente:

1. `R3` · `estado.html` (§4) — la más barata, y es la que hoy miente más.
2. `R4` · `UMBRAL_OFF_ALERTA` (§5) — contenida en un módulo.
3. `R1` · firmar las alertas (§2) — la más larga de las tres, y la que la reunión destrabó.
   Hacer **primero** la persistencia de las firmas, o el trabajo se pierde.

**Después, con el OK del equipo**, las dos que tocan lo publicado:

4. `R5` · las dos cifras viejas (§6).
5. `R6` · el tercer marco y el empate (§7).

**Y al final, cuando `R1` esté:**

6. `R2` · que la compuerta se llame de verdad (§3).

**Mínimo viable si el tiempo no alcanza:** `R3` y `R5`. Son las dos que hacen que un lector
externo —el investigador abriendo el repositorio— vea números coherentes. Las demás mejoran el
mecanismo, pero no se contradicen solas.
