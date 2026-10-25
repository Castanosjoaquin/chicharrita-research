# Plan de la ola 5 — la carta del 25 de octubre y la reunión del lunes

**Fecha del plan:** domingo 2026-10-25. **La reunión es mañana, lunes 26** («nos vemos mañana»).
Queda un día y hay cuatro personas, así que el plan está ordenado por lo que llega a la reunión y
lo que no: la sección [§8](#8-mínimo-viable-antes-de-la-reunión) dice qué se cae primero si el
tiempo no alcanza.

La carta que este plan contesta es la respuesta de Diego a `entregables/respuesta-al-mentor.md`.
Resuelve la discrepancia de los cuatro conteos, descarta nuestra hipótesis como *causa* de esos
cuatro números sin descartarla como hallazgo, confirma el marco de la molécula, abre un tercer
marco, abre el problema de las quimeras y pide cinco cosas para la reunión. Nueve líneas, `N1` a
`N9`.

> **Lo que cambia la prioridad de todo el plan.** Antes de escribir este plan se reprodujo su
> explicación con insumos propios: el port con la tabla del INTA da 138, 40, 218 y 35, y la regla
> de conteo que él describe —curva de cobertura de 20 posiciones por ventana de 21 nt, un siRNA
> nuevo por incremento positivo— convierte esos cuatro en **114, 35, 199 y 33**, que son los
> cuatro de la planilla, exactos `[M]`. Está medido en el borrador de sesión
> (`…\scratchpad\curva.py`, `…\scratchpad\nn4\`) y **todavía no está en el repositorio**: eso es
> `N1`, y es lo primero.


## 1. Trazabilidad: cada cosa que pide, y quién la contesta

| # | Lo que dice o pide la carta | Línea | Estado de partida |
|---|---|---|---|
| P1 | La discrepancia se explica por la función histórica de conteo, no por la termodinámica `[R]` | `N1` | **reproducido** `[M]`, sin versionar |
| P2 | Identificaron una limitación real de esa función y la van a revisar internamente `[R]` | `N1` | nuestra función y su prueba son el aporte |
| P3 | Nuestra observación sobre los `Efficient siRNA hits` sigue válida, pero no era la responsable | `N8` | hay que reencuadrar `M1` y dos entregables |
| P4 | Las referencias son `Dalbulus_maidis_genome_v1` y `Maize_rayado_fino_virus_genome_v1`, **sin FASTA confirmado** | `N8` | el pedido 2 queda abierto, no se puede cerrar |
| P5 | Para qué siRNAs se producen vale la molécula final: 280 ventanas en 300 nt, no 300 | `N3` | coincide con lo que ya publicamos (26) |
| P6 | Propone explorar un tercer marco: los 21-meros que existen en la molécula, con accesibilidad evaluada en el transcrito blanco | `N3` | **ya medido**: es 29 |
| P7 | En quimeras: ventanas nuevas en las junturas, y que un siRNA de juntura no necesariamente tiene complemento continuo en un blanco. «Conviene evaluarlo por separado» | `N4` | nuevo, nada medido |
| P8 | Mantener los dos modelos de la regla terminal como hipótesis, y no mezclar la comparación INTA-contra-original con el problema de conteo | `N6`, `N8` | `M4` ya tiene la potencia; es encuadre |
| P9 | Distinguir qué parte de las diferencias de 922-1221 viene del modelo de eficiencia, cuál de los límites físicos y cuál del contexto de accesibilidad | `N3` | **ya medido**: 36 = 29 + 7, 26 = 29 − 3 |
| P10 | Qué son exactamente las 4.368 configuraciones, y cuál es la identidad de la región C7 | `N5` | está en `M7`, hay que escribirlo como ficha |
| P11 | Para la reunión: exposición frente a conservación, alertas de off-target, referencias nuevas de `BicC`, y cómo comparar eficiencia entre genes distintos | `N7` | `M5`, `M6`, `M7`§4 y `M8` están escritos |
| P12 | «Defender una recomendación biológica y explicitar sus principales incertidumbres, no solamente elegir la región que tenga más ventanas predichas» | `N6` | **no existe**; es lo que más pesa |
| P13 | Le interesa la implementación del port; no necesita datos internos de EpiLab | `N9` | es la promesa de nuestra carta |

Lo que **no** entra al plan, y conviene decirlo: el pedido 1 de la reunión —la clasificación por
ventana de su corrida— **muere**. Lo pedimos para explicar los conteos y los conteos quedaron
explicados por otra vía. Pedirlo igual sería pedir un archivo para una pregunta que ya no tenemos.


## 2. `N1` — La regla de conteo histórica, reproducida, probada y empaquetada

**Por qué es la primera.** Es el único resultado nuevo de todo el plan, convierte un `[R]` suyo en
un `[M]` nuestro sin pedirle un archivo ni mover una secuencia de la máquina, y es lo que él mismo
dijo que va a revisar internamente. Llegar con la función y su prueba es el aporte más concreto que
podemos hacer a la plataforma nueva.

**Qué hay que hacer.**

1. Crear `research/ola5/N1_regla_de_conteo/` con la estructura de las líneas de la ola 4
   (`REPORT.md`, `index.html`, `NOTAS_PARA_META.md`, `scripts/`, `resultados/`).
2. `scripts/conteo_por_curva.py`, con dos funciones puras y una CLI:
   - `curva_de_cobertura(posiciones, largo, ancho)` → la curva, acumulada por diferencias como
     ya lo hace `sifi_plus/perfil.py`;
   - `contar_por_incrementos(posiciones, largo, ancho)` → la suma de los incrementos positivos,
     que es `#{p : p eficiente y p−ancho no eficiente}`;
   - la CLI lee los TSV por ventana del port (columna `pos` y `is_efficient`) y escribe la tabla.
3. `scripts/test_conteo_por_curva.py`, con tres grupos de casos:
   - **sintéticos**, que fijan el mecanismo sin depender de ningún dato: una ventana sola cuenta 1;
     dos a distancia exactamente `ancho` cuentan 1; a distancia `ancho ± 1` cuentan 2; el conjunto
     vacío cuenta 0; una corrida de `k` ventanas contiguas cuenta 1;
   - **invariantes**: el conteo por incrementos nunca supera el conteo por ventana, y nunca es
     menor que la cantidad de tramos no nulos de la curva;
   - **el ancla real**: con los cuatro TSV de `--tabla-nn NN4 --modo fiel --backend vienna`, el
     ancho 20 da 114, 35, 199 y 33, y los anchos 19 y 21 **no** dan los cuatro. La prueba declara
     «no corrida» si falta el corpus, como hace `sifi_plus/test_api.py`, y no falla.
4. `resultados/conteo_por_curva.tsv` y `.json`: por gen, eficientes, tapadas, visibles, sesgo
   relativo y la lista de arranques tapados. Son posiciones, no nucleótidos, así que pasa el gancho.
5. `REPORT.md` con cuatro cosas: qué dice la carta, qué medimos, qué significa el sesgo
   gen-dependiente, y qué queda abierto.

**La tabla que tiene que salir, y que ya está medida** `[M]`:

| Gen | Eficientes (NN4, fiel, ViennaRNA) | Tapadas | Conteo por incrementos | Planilla | Sesgo |
|---|---|---|---|---|---|
| `MP_MRFV` | 138 | 24 | 114 | 114 | 17,4 % |
| `CP_MRFV` | 40 | 5 | 35 | 35 | 12,5 % |
| `BicC_Dm` | 218 | 19 | 199 | 199 | 8,7 % |
| `ATPaseD_Dm` | 35 | 2 | 33 | 33 | 5,7 % |

**Lo que hay que escribir y no es el número.** El sesgo **no es constante**: va de 5,7 % a 17,4 %
y depende de cuán agrupadas están las ventanas eficientes, no del largo del gen ni de la calidad
del diseño `[M]`. La consecuencia es que dos cifras cualesquiera de la planilla —entre genes o
entre regiones— perdieron fracciones distintas, así que **la planilla no es comparable consigo
misma** `[H]`. Eso es un quinto límite para `M8` y va al archivo del lunes.

**Criterio de terminado.** Los cuatro valores exactos con ancho 20; los anchos vecinos fallando;
la prueba corriendo desde la raíz del repositorio; `procedencia.json` con versiones de Python,
ViennaRNA y Biopython y los md5 de los cuatro FASTA de entrada.

**Una pregunta que esto abre y hay que llevar.** Si las curvas históricas reconstruyen
138/40/218/35, el método `siFi21_8_1.0_0.1_1111` corre con la tabla de Zuber y un motor
equivalente a las ligaduras de ViennaRNA, y **no** con el si-Fi21 original `[H]`. Si es así,
nuestra línea base para comparar contra la planilla deja de ser 133/32/212/42. Hay que
preguntárselo derecho, porque cambia qué número es «el de ellos».


## 3. `N2` — El ancho de cobertura en nuestra propia curva

**El problema.** `sifi_plus/perfil.py:38` construye el solapamiento con `size` posiciones por
ventana, o sea 21; la carta dice que el original asigna 20 `[R]`. El test
`sifi_plus/test_api.py:152` fija cantidad de tramos (ocho), máximo (9) y altura en cuatro
posiciones, pero **no fija los bordes de los tramos**, así que nuestra verificación «tramo por
tramo» no distingue 20 de 21 `[M]`. En la carta le dijimos que reproducimos la curva tramo por
tramo: es cierto a esa granularidad, y hay que decir con qué convención.

**Qué hay que hacer.**

1. Correr el test de la curva con ancho 20 y con 21 y registrar si cambian los ocho tramos, el
   máximo y las cuatro alturas. Necesita el backend `exe`, que está en
   `%LOCALAPPDATA%\siFi2015\`.
2. `solapamiento()` toma el ancho como parámetro explícito (`ancho_cobertura`), separado del
   tamaño del siRNA, con **20 como valor por defecto y la razón escrita al lado**.
3. Agregar al test la aserción que sí discrimina: los bordes exactos de por lo menos dos tramos.
4. Si la curva de paridad cambia al pasar a 20, es un cambio de salida publicada y va con ADR.

**Criterio de terminado.** Queda escrito, con número, si la convención del ancho cambia o no la
curva que le mostramos; y el test deja de poder pasar con las dos convenciones.


## 4. `N3` — Los tres marcos, y la partición de la diferencia

**Lo bueno de esta línea es que casi no hay que medir.** `M7` §3 ya tiene la descomposición y las
tres columnas por región; lo que falta es nombrarlas como lo que él nombró y cerrar la partición
que pide en P9.

| Marco | Qué es | 922-1221 |
|---|---|---|
| contexto, 300 arranques | los 300 arranques que caen dentro de la región, plegados en el gen completo | 36 |
| **contexto, 280 comparables** | **los 21-meros que existen en la molécula, con accesibilidad en el gen** — el tercer marco que propone | **29** |
| molécula recortada | los 280 de la molécula de 300 nt plegada sola | **26** |

**La partición que pide, ya medida** `[M]`: de 36 a 29 son **7 arranques que la molécula no tiene**
(límite físico); de 29 a 26 son **3 ventanas que cambian de veredicto al plegarse sin contexto**
(contexto de accesibilidad: 2 por accesibilidad y 1 por estabilidad de extremos en la posición 1).
Del modelo de eficiencia no sale ninguna de las diez: el modelo es el mismo en los tres marcos, y
lo que cambia es qué se le da de comer.

**Qué hay que hacer.**

1. Extender `research/ola4/M7_robustez_bicc/scripts/recorte_vs_contexto.py` para que emita el
   marco intermedio como columna con nombre propio, y correrlo sobre las tres regiones de `BicC_Dm`
   y las cuatro regiones vigentes de los otros genes.
2. Una tabla única de tres marcos × siete regiones, con la partición de la diferencia en las dos
   causas (límite físico / contexto) y el término que cruza en cada ventana que cambia.
3. Declarar la asimetría que ya se midió y que incomoda: las tres regiones cambian de conteo al
   recortarse y **cambian en direcciones distintas** (922-1221 pierde 10, 2121-2420 pierde 13,
   264-563 pierde 3), así que un ranking armado en contexto no es el ranking de las moléculas
   `[M]`.
4. Dejar escrito qué marco usa cada cifra que publicamos. **La que va al entregable es 26.**

**Criterio de terminado.** Las siete regiones con sus tres marcos y la partición; y una frase por
cifra publicada que diga en qué marco está.


## 5. `N4` — Quimeras: las dos preguntas que él separó

Es lo único del plan que no tiene nada medido, y es lo más interesante que abre la carta. Él
separa dos cosas que nuestro pipeline hoy no distingue: **qué siRNAs puede producir la molécula**
y **si cada uno encuentra complementariedad continua en algún blanco**.

**Qué hay que hacer.**

1. `research/ola5/N4_quimeras/scripts/junturas.py`: dadas dos o más regiones y su orden de
   ensamblado, construir la molécula y clasificar sus ventanas en tres clases: **propias** de un
   fragmento, **de juntura** (cruzan el empalme sintético) y **perdidas** (existían en el gen y no
   en la molécula).
2. Para cada ventana de juntura, dos preguntas por separado:
   - ¿es eficiente en la molécula ensamblada? (el criterio del port, sobre la molécula);
   - ¿existe como tramo continuo de 21 nt en alguno de los blancos pretendidos? Esto es
     `offtarget_21nt.py` usado al revés: el autómata de Aho-Corasick ya está escrito, y lo que
     cambia es que el conjunto de búsqueda son los blancos y no el panel de no objetivo.
3. La cifra que sale de ahí: cuántas ventanas de la quimera son **eficientes y sin blanco**, o sea
   capacidad de silenciamiento gastada en una secuencia que no existe en ningún transcrito. Hoy no
   la medimos y el conteo de eficientes de una quimera la cuenta como si valiera.
4. En una quimera de dos fragmentos de 300 nt hay 20 ventanas de juntura y el total pasa de
   2 × 280 = 560 a 580 ventanas: el marco de conteo de una quimera no es la suma de los marcos de
   sus partes `[H]`, y hay que verificarlo con el script y no con la aritmética.

**Alcance.** Esto mide **pérdida** de eficacia sobre blancos propios y gasto de molécula. No es, y
no se escribe como, una vía para ampliar el rango de ningún agente: cualquier resultado que se
leyera así queda fuera de alcance por `CLAUDE.md`.

**Si no entra hoy.** Va como diseño escrito, con el esqueleto del script y las dos preguntas
separadas, y se declara como no medido. Es honesto y además le contesta: lo que pidió fue que se
evalúen por separado, y el diseño ya las separa.


## 6. `N5` — La ficha de la grilla y la identidad de C7

Media hora, y cierra los dos pedidos explícitos de P10.

**Las 4.368 configuraciones** son el producto de cinco ejes, y cada una se mide en dos marcos, de
donde salen las 13.104 filas de `M7/resultados/grilla_parametros.tsv` `[M]`:

| Eje | Valores | Cuántos |
|---|---|---|
| brecha de estabilidad de extremos | 0,0 a 2,0, paso 0,1 | 21 |
| corte de accesibilidad | 0,05 a 0,30, paso 0,01 | 26 |
| modo del port | `fiel`, `corregido` | 2 |
| tabla de apilamiento | `RNA_NN3` (original), `RNA_NN4` (`sifi21INTA`, Zuber 2022) | 2 |
| motor de plegado | RNAplfold 2.1.5, ViennaRNA 2.7.2 | 2 |

Lo que queda fijo: tamaño de siRNA 21, ventana de accesibilidad `u = 8`, 22 °C y las cuatro
casillas del criterio en `1111` — o sea la cadena `siFi21_8_1.0_0.1_1111` con la que él declaró su
configuración, con los dos umbrales barridos.

**C7** es `BicC_Dm` **2121-2420**, la región que recomendaba la línea C7 del ranking v2 y que
`D25` desplazó por conservación. Y acá hay que llevar nosotros la autocorrección: el argumento del
«32 de 36 idénticas contra 22 de 35» **no es sostenible**, porque `GCWP01` (Illinois) no cubre un
solo nucleótido de 922-1221 y el criterio contaba la ausencia de datos como ausencia de
contradicción `[M]`. La decisión no se cae —el genoma del Reino Unido y el ensamblado de Córdoba
sí la favorecen— pero su razón escrita hay que reescribirla con la cobertura declarada.


## 7. `N6` — La recomendación biológica, defendida

**Es lo que más pesa de toda la carta y es lo único que no existe escrito.** El párrafo que lo
pide es explícito: «me interesa que puedan defender una recomendación biológica y explicitar sus
principales incertidumbres, no solamente elegir la región que tenga más ventanas predichas como
eficientes» `[R]`.

Un documento corto, `entregables/recomendacion-defendida.md`, con cinco partes y en este orden:

1. **El blanco y el mecanismo esperado.** Qué gen, qué hace en el insecto, qué fenotipo se espera
   y en qué plazo. Con fuente para cada afirmación de función.
2. **Por qué `BicC_Dm` y no la V-ATPasa ni un blanco viral.** El argumento que manda no es el
   conteo: es el de `M8`, la comparación entre el tiempo hasta el efecto y la ventana de latencia
   del patógeno. Un blanco letal lento no sirve si el insecto transmite antes de morir.
3. **La región, con su marco.** 922-1221, **26** ventanas eficientes en la molécula de 300 nt que
   se sintetizaría, 0 coincidencias perfectas de 21 nt contra el panel de seis no objetivo, y 3
   alertas de bloque ≥ 19 nt bajo el umbral laxo.
4. **Las tres incertidumbres principales, cada una con su número.**
   - *El valor predictivo del criterio no está establecido.* `M4`: con los 29 siRNA de Cedden la
     comparación de los dos modos no podía salir distinta (un solo discordante, p exacto 1,00), y
     replicando ese diseño harían falta 2.784 `[M]`. Y en este gen, 134 de 223 eficientes del modo
     fiel —el 60,1 %— entran por la rama 2 de la regla terminal, que decide mirando sólo la
     accesibilidad `[M]`.
   - *El marco de conteo decide tanto como los umbrales.* `N3` y `M7`: contra 2121-2420 la ventaja
     se da vuelta según el marco (36,4 % de 4.368 configuraciones en contexto, 75,6 % en la
     molécula) `[M]`.
   - *La exposición no objetivo es una ponderación sin decidir.* `M5`: con exposición cero para
     *Homalodisca vitripennis* tres de las seis regiones recomendadas se mudan `[M]`.
5. **Qué la falsea.** El ensayo discriminante de `M4`: 32 siRNA por brazo en un diseño prospectivo.
   Es lo que convierte la recomendación en una propuesta y no en una preferencia.

**Criterio de terminado.** Que un lector hostil pueda decir, leyéndolo, **qué resultado
experimental la refutaría**. Si no se puede, no está terminado.

Sobre la regla terminal, acá no hay nada que defender y conviene decirlo así: él mantiene los dos
modelos como hipótesis hasta tener evidencia, y `M4` midió que la evidencia disponible no alcanza
para elegir. Coincidimos, y presentarlo como coincidencia es mejor que presentarlo como posición.


## 8. `N7` — El archivo del lunes

Un HTML autocontenido, corto, **que no repite `resumen_checkpoint2.html`**. Ese archivo es el
relato de cómo llegamos; este es la carpeta de la reunión: una sección por cada cosa que pide la
carta, con el número y la lectura al lado.

`entregables/reunion-lunes.html`, siete secciones:

| § | Qué va | De dónde sale |
|---|---|---|
| 0 | El conteo, resuelto y reproducido por nosotros: 138/40/218/35 → 114/35/199/33, con el sesgo gen-dependiente | `N1` |
| 1 | Exposición ecológica frente a conservación de secuencia: los dos ejes separados, y que el veto tiene palanca y el promedio ponderado no | `M5` |
| 2 | Las alertas de off-target: las 17 alertas sobre doce regiones, los cuatro campos, y que las cuatro regiones vigentes no tienen ninguna de 21/21 | `M6` |
| 3 | Las referencias nuevas de `BicC`, con la autocorrección de `D25` y la cobertura declarada por fuente | `M7` §4 |
| 4 | Los tres marcos y la partición 36 = 29 + 7, 26 = 29 − 3 | `N3` |
| 5 | Qué permite comparar el conteo de eficientes: los cuatro límites, la densidad que da vuelta el orden, y el quinto límite nuevo | `M8` + `N1` |
| 6 | La recomendación defendida y sus tres incertidumbres | `N6` |
| 7 | Lo que queda abierto: los FASTA de los índices, qué tabla usa el método histórico, y las quimeras | `N4`, `N8` |

**Restricciones de forma.** Autocontenido y sin red (los SVG inline, las dos figuras del
repositorio en base64, como hizo Lorenzo). Pasa `tools/verificacion/chequear_svg.py` y
`sin_secuencias.py`. **Ninguna racha de nucleótidos**, ni en texto ni en figura. Largo objetivo:
que se lea en pantalla en diez o quince minutos, con tablas chicas y la lectura de cada número al
lado, que es lo que el equipo ya pidió para los bloques F y G del resumen.


## 9. `N8` — La memoria del proyecto, que no es opcional

Por `CLAUDE.md` esto va con cada línea y no al final. Lo que hay que escribir:

- **ADR nuevo.** «La discrepancia de los cuatro conteos se explica por la función histórica de
  conteo, no por la termodinámica.» Alternativas consideradas: el umbral de 1,75, la tabla de
  vecinos más cercanos, la referencia de Bowtie y la unidad de conteo. Criterio: la reproducción
  exacta de los cuatro con ancho 20 y el fallo con 19 y 21. Consecuencia: qué cifras de la planilla
  dejan de ser comparables entre sí.
- **ADR o nota de aplicación.** Cuál es la línea base contra la planilla, si el método histórico
  corre con `RNA_NN4`. Queda como `[H]` hasta que él lo confirme.
- **`CAMINOS_PROBADOS.md`.** La hipótesis del conteo por acierto de Bowtie: descartada como causa
  de los cuatro números, conservada como hallazgo sobre la herramienta original. Y la lección, que
  vale como criterio de parada: **una explicación candidata que acertó un gen de cuatro con error
  de uno era coincidencia**, y el mecanismo verdadero da los cuatro exactos.
- **`PREGUNTAS_ABIERTAS.md`.** Cerrar el pedido 1. Dejar abierto el pedido 2: nombró
  `Dalbulus_maidis_genome_v1` y `Maize_rayado_fino_virus_genome_v1` y **no** confirmó los FASTA.
  Preguntas nuevas: ¿qué tabla de apilamiento usa el método histórico?; ¿el conteo por incrementos
  se usó también para las doce regiones de la planilla o sólo para los cuatro genes?; ¿cuál es el
  ancho de cobertura exacto de su curva, 20 confirmado?
- **`GLOSARIO.md`.** Cuatro términos: conteo por incrementos, ancho de cobertura, marco de conteo
  (los tres) y ventana de juntura.
- **`FUENTES.md`.** La carta del 25-10 como fuente `[R]`, con fecha.

Y los documentos que hoy afirman lo que la carta corrige:

| Archivo | Qué cambia |
|---|---|
| `research/ola4/M1_conteo_y_referencia/REPORT.md` | el encabezado y el titular; el «200 contra 199» pasa a coincidencia declarada; la hipótesis queda como hallazgo independiente |
| `research/ola4/M8_que_compara_el_conteo/REPORT.md` | el quinto límite, y la fila «Planilla de EPILAB» de la tabla de densidad anotada con el sesgo de cada gen |
| `research/ola4/README.md` | la fila de `M1` y el bloque «lo que hay que leer antes de usar estos números» |
| `entregables/critica-herramientas.{md,html}` | la hipótesis deja de presentarse como explicación de la planilla |
| `entregables/respuesta-al-mentor.md` | nota al pie: qué de esa carta quedó confirmado y qué no |


## 10. `N9` — El port, listo para mostrar

Él cerró el tema: «no necesitan compartir datos internos de EpiLab ni archivos intermedios de
nuestros diseños» `[R]`. Entonces la revisión se acota y se puede terminar hoy.

1. Definir el subconjunto que se le pasa: `tools/sifi21_port/` y `sifi_plus/` (código, pruebas y
   `README.md`), **sin** ningún TSV derivado y **sin** `work/`.
2. Correr `sin_secuencias.py` sobre ese subconjunto exacto y guardar la salida como constancia.
3. Un `README` de entrada de media página: qué hace, los dos modos, los dos motores, cómo se corre
   y contra qué está verificado.
4. Decidir cómo se le entrega. No se publica nada sin que el equipo lo decida.


## 11. Mínimo viable antes de la reunión

Si el día no alcanza, este es el orden en que se cae, elegido por cuánto mejora la conversación:

1. **`N1`**, siempre. Es el único resultado nuevo y es el que le interesó.
2. **`N6`**, la recomendación defendida. Es lo que pidió explícitamente y lo único que no existe.
3. **`N7`**, el archivo. Sin esto los dos anteriores existen pero no se muestran.
4. **`N5`**, media hora, cierra dos pedidos suyos.
5. **`N3`**, que es escritura sobre números ya medidos.
6. **`N8`**, que es obligatorio pero puede ir en paralelo y seguir después de la reunión.
7. **`N2`** y **`N4`** son los que no entran. Si no entran, **se declaran como no hechos** en §7
   del archivo, con lo que sí está escrito de cada uno.

**Reparto sugerido para cuatro personas.** `N1` más `N2` son una persona, porque son el mismo
código. `N6` es una persona sola y sin interrupciones, porque es el documento que hay que pensar.
`N7` es una persona, y empieza cuando `N1` y `N6` tienen sus números, no antes. `N3` más `N5` más
`N8` son una persona: es escritura sobre cosas medidas.

**Trampas conocidas de este repositorio**, que ya costaron tiempo y están en la memoria:

- El gancho de pre-commit **no está instalado en este clon** (`core.hooksPath` vacío). Instalarlo
  antes del primer commit: `git config core.hooksPath tools/verificacion/hooks`.
- Cuando el gancho no puede verificar, rechaza con el mensaje de hallazgo equivocado. Si rechaza,
  leer el código de salida antes de buscar secuencias que no existen.
- `autocrlf` falsea los diffs de las salidas: comparar un archivo generado contra el commiteado da
  «difieren» aunque sean iguales.
- Las herramientas del original están en `%LOCALAPPDATA%\siFi2015\` y no hay que instalar nada.
- `work/` no está en git y puede no estar en la máquina. Lo que una línea necesite leer dos veces,
  va versionado o se regenera con su driver.
