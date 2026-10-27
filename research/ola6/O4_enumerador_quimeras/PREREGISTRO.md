# O4 — Preregistro: el objetivo del ranking y la grilla, declarados antes de enumerar

**Fecha y hora de escritura:** 2026-10-27, 11:22 (−03). **Issue:** #24.
**Qué se preregistra:** el **objetivo** bajo el cual el enumerador de quimeras ordena sus
combinaciones, la **grilla** que enumera, el **orden** en que poda y la lista de lo que se
reporta. Se escribe y se commitea **antes de enumerar una sola combinación**.

## 1. Por qué este preregistro existe, y por qué es sobre el objetivo y no sobre una región

El criterio de terminado del issue #24 pide textualmente que «el objetivo del ranking esté
declarado en el código y en la salida, no implícito». Un enumerador que devuelve «la mejor
quimera» sin objetivo declarado tiene un grado de libertad que no se ve: con tres cuentas
por combinación —heredadas, juntura y riesgo del empalme— y dos órdenes posibles, quien
elige qué cuenta ordena después de ver los resultados puede obtener casi cualquier ganador
sin mentir en ningún número. `D67` ya decidió que una quimera **no** se evalúa por densidad
de ventanas eficientes, así que «la mejor» no es una opción disponible: hay que decir mejor
para qué.

El precedente es de esta misma ola y está documentado: en `O3` la sesión empezó a medir con
un criterio de región elegido en paralelo al preregistro, ese criterio corría con cinco
referencias en vez de seis y eligió una región que el panel completo veta; la medición
entera quedó descartada (`CAMINOS_PROBADOS.md`, `PREGUNTAS_ABIERTAS.md` 21). El costo de
escribir esto antes es media hora; el costo de no escribirlo ya se pagó una vez.

## 2. El objetivo, que es un parámetro obligatorio y sin valor por defecto

`--objetivo` no tiene default. Omitirlo es un error de la línea de comandos, no una corrida
con el objetivo implícito de nadie —misma forma que `D72` le dio al parámetro `inventario`
de la compuerta, y por el mismo motivo: un default se adopta olvidándolo—. Los valores
admitidos son tres, y cada uno dice qué ordena:

1. **`cobertura_fenotipica`** — el de `D67`, y el único que la feature recomienda usar. Exige
   que los dos genes traigan **eje de fenotipo declarado y distinto** (reproducción,
   movilidad, letalidad) con el identificador de la fila del catálogo de `C5` que lo
   respalda. Ordena por el **eje de riesgo**: primero las combinaciones cuyo empalme no
   fabrica ningún bloque nuevo contra el panel, y entre ésas por cantidad de ventanas
   heredadas eficientes, que entra como **desempate y no como puntaje**.
2. **`riesgo_minimo`** — ordena sólo por el empalme: bloques fabricados, primero los de
   coincidencia perfecta de 21 nt, después los de ≥ 19 nt. No mira eficiencia.
3. **`eficiencia_heredada`** — ordena por ventanas heredadas eficientes y por nada más. Es
   el objetivo que el issue pide **no vender**, y existe para poder medir cuánto se pierde
   al no usarlo. Toda salida bajo este objetivo lleva al lado, en la misma tabla, que el
   criterio de eficiencia de si-Fi21 no está validado en hemípteros: ρ = +0,142, IC95
   [−0,247, +0,492], n = 29 `[M]`.

No existe un valor `mejor`, ni un `--objetivo` que combine los tres en un número. La cadena
del objetivo viaja en **cada fila** del TSV de salida y en el JSON de metadatos, no sólo en
el encabezado, para que una fila copiada a otro documento no pueda perder su objetivo por el
camino.

El **eje de fenotipo es entrada declarada, no inferencia**. El catálogo de `C5` tiene 36
filas y sus columnas son `funcion` y `resultado` en texto libre: **no tiene columna de eje**
`[M]`, así que el eje lo declara quien corre la feature y la fila del catálogo queda como su
fuente. Los tres que `D67` ya asignó, leídos de sus filas: `BicC` (`DM-01`, oogénesis,
oviposición casi nula) → reproducción; `V-ATPase B` (`DM-02`, alas deformes, supervivencia
16 % al día 4 contra 37 % del control) → movilidad; `V-ATPase D` (`DM-03`, supervivencia
18 % al día 4, efecto en alas **no** significativo) → letalidad `[M]`. Un gen sin fila en el
catálogo entra como `sin_fenotipo_publicado` y **no puede** correrse bajo
`cobertura_fenotipica`: el objetivo que exige ejes distintos no puede cumplirse con un eje
desconocido.

## 3. La grilla, y por qué es enumerable

Para dos genes y un largo total `L` fijo los parámetros libres son **tres**: el arranque del
fragmento izquierdo `a1`, el largo del fragmento izquierdo `l1` —con `l2 = L − l1`, que no es
libre— y el arranque del fragmento derecho `a2`. El **orden** de los dos genes es un cuarto
grado de libertad discreto con exactamente dos valores, y entra en la enumeración porque
está medido que cambia el resultado: en `C13`, las mismas dos regiones dan +3 y −3 ventanas
según el orden, y en `O3` los dos órdenes rinden 41 y 40 eficientes y **sólo uno de los dos
fabrica riesgo nuevo** `[M]`.

Eso es una grilla y se enumera. `W2` §4 ya documentó que ninguna metaheurística mejora la
enumeración exhaustiva en la elección de región, y acá el argumento es el mismo más uno
nuevo: una metaheurística sobre tres parámetros con un objetivo de riesgo que es casi todo
ceros y unos no tendría gradiente que seguir `[H]`. **No hay metaheurística, no hay muestreo
aleatorio y no hay optimizador.**

Lo que se declara ahora, porque elegirlo después de ver los resultados sería elegir el
ganador:

- **`--paso`**, default **10 nt**, aplicado a `a1`, `a2` y `l1`. Es un engrosamiento
  declarado de una grilla continua, no la grilla continua: dos candidatos a 10 nt de
  distancia no son independientes, porque la banda de contexto que los distingue mide
  59-72 nt (§4). `--paso 1` corre la grilla fina y cuesta cien veces más; el valor usado
  queda en el JSON.
- **`--largo-total`**, obligatorio, y **`--l1-min` / `--l1-max`**, default 100 y `L − 100`:
  un fragmento de menos de 100 nt aporta menos de 80 ventanas propias y es más banda de
  contexto que región.
- **`--tope-plegados`**, default **5.000**. Si la grilla que sobrevive a la poda de riesgo
  lo excede, la corrida **se detiene y lo dice**, con el tamaño que encontró y el paso que
  haría falta. No muestrea, no recorta por su cuenta y no cambia de algoritmo: degradar en
  silencio es lo que convierte una enumeración auditable en una heurística sin declarar.
  El tope está calibrado contra lo medido ahora: una evaluación completa de una molécula de
  600 nt —las 580 ventanas, modo `corregido`, backend `vienna`— tarda **0,21 s** incluyendo
  el arranque del proceso `[M]`, así que 5.000 plegados son unos 18 minutos por el camino
  más lento, y menos llamando al motor en proceso.

## 4. El orden: el riesgo poda primero, y es lo que vuelve finita la grilla

**Primero el tamizado, después la eficacia.** Es el orden que `D70` fijó, el que `D74`
aplicó y el que `CAMINOS_PROBADOS.md` registra como la lección de `C4`: elegir por conteo
antes de mirar el veto lleva a elegir regiones vetadas.

Por fragmento, una **máscara de veto por ventana**: la ventana queda vetada si tiene
coincidencia perfecta de 21 nt contra el panel de **seis** referencias no objetivo —con la
humana a peso 1,00, vía `ranking_v2.con_panel(sin_humano=False)`— y con el genoma de
*Dalbulus maidis* **excluido por ser on-target** cuando el gen es del insecto
(`ranking.excluidas_de()`, `estrategia = "insecto"`). Un fragmento es admisible si **ninguna**
de sus ventanas está vetada, de modo que los fragmentos admisibles de largo `l` son las
rachas de ventanas no vetadas de largo `l − 20`, que se leen de la máscara en una pasada.

Esta poda no es cosmética y es la que hace enumerable el problema: en `V-ATPase B` hay **71
ventanas con coincidencia perfecta de 21 nt**, y de las **1.184** regiones de 300 nt que
caben en su CDS sobrevive **exactamente una**, 517-816, sin un nucleótido de holgura; a 301
nt no sobrevive ninguna `[M]` (`D74`). `BicC_Dm` en su región vigente tiene cero en todo el
panel `[M]`.

**El riesgo de las ventanas heredadas se hereda; el del empalme no.** El estado de
off-target de una ventana depende sólo de sus 21 nt (`C13` §6), así que la máscara se
calcula **una vez por gen** y no por candidato. Lo que no se hereda es lo que el empalme
fabrica: en `O3`, un bloque perfecto de **19 nt** con 18 nt de un gen y 1 del otro, que no
existe en ninguno de los dos y coincide con dos transcriptos de *Zea mays* —`NM_001153025.1`
y `XM_020544485.2`— en las ventanas j = 1, 2 y 3, ninguna eficiente `[M]`. Por eso las
ventanas de juntura de **todos** los candidatos que sobreviven se tamizan, y se tamizan en
**una sola pasada** sobre el panel: un autómata con los 21-meros de juntura de todos los
candidatos, y las referencias leídas una vez. Lo que no se hace es una pasada por candidato.

## 5. Las tres cuentas, separadas desde antes de medir

Por combinación y por orden, tres números que **no se suman entre sí para dar «la cifra de
la quimera»** (`D67`, y es criterio de terminado del issue):

1. **Heredadas.** Ventanas heredadas eficientes, cuántas cambiaron de veredicto respecto de
   su fragmento plegado solo, en qué dirección y a qué distancia de la unión. La banda en la
   que un cambio es posible está derivada del código en `C13` §4: la secuencia ajena influye
   hasta **72 nt corriente abajo** del final de una ventana y **59 corriente arriba** de su
   comienzo, y el máximo observado en las doce quimeras vigentes fue **66 nt**, con **cero
   violaciones** del techo sobre n = 67 `[M]`.
2. **Juntura.** Las 20 ventanas a caballo de cada unión: cuántas son eficientes y, de ésas,
   cuántas tienen blanco continuo de 21 nt en alguno de los dos genes, con el método de
   `research/ola5/N4_quimeras/scripts/junturas.py`. Una quimera **canjea** los 20 arranques
   de cola de cada fragmento por 20 de juntura, y los de juntura no existen en ningún
   blanco.
3. **Riesgo del empalme.** Los bloques que la unión fabrica contra el panel de seis, con los
   tres criterios del port (`perfecto_21`, `perfecto_ge19`, `mm1_21`), y la alerta de juntura
   nueva con el esquema de columnas de `M6` para que se pueda pegar al inventario.

## 6. La configuración de medición, fijada ahora

Punto por defecto de lo que publica el proyecto: **`--modo corregido --backend vienna
--tabla-nn NN3`**, 22 °C. La cifra principal de cada candidato es la del marco **molécula**
de `D63` —la molécula ensamblada, plegada entera— porque es la que se sintetiza y la que el
proyecto publica. El motor es `tools/sifi21_port/sifi_core.py` llamado **sin modificarlo**;
si se lo llama en proceso en vez de por línea de comandos, el resultado tiene que ser
idéntico y eso es una de las anclas. Entorno de esta máquina: Python 3.13.15, numpy 2.5.4,
ViennaRNA 2.7.2, Biopython 1.88 `[M]`.

## 7. Las anclas que tienen que pasar antes de leer cualquier número nuevo

- **Contra `O3`.** Con la grilla restringida a `BicC_Dm` 922-1221 y `V-ATPase B` 517-816, los
  dos órdenes tienen que dar **41 y 40** ventanas eficientes contra **40** de la suma de las
  partes, y el bloque fabricado de 19 nt tiene que aparecer **sólo** en el orden
  `V-ATPase B` + `BicC_Dm`, en j = 1, 2 y 3, ninguna eficiente. El otro orden fabrica cero.
- **Contra `C13` §5.** Con la grilla restringida a las coordenadas vigentes de los cuatro
  genes de EPILAB, las doce quimeras tienen que dar **4** ventanas de juntura eficientes de
  240 y **61** heredadas que cambiaron de veredicto, 31 que pierden y 30 que ganan.
- **Contra la máscara de veto.** `V-ATPase B` tiene que dar 71 ventanas con coincidencia
  perfecta de 21 nt y **una** región admisible de 300 nt, 517-816, y ninguna a 301 nt.
- **Motor en proceso contra motor por línea de comandos.** El mismo candidato evaluado por
  las dos vías tiene que dar la misma lista de ventanas eficientes, ventana por ventana.

**Si una de las cuatro no pasa, esta línea para y lo dice, sin leer ningún número nuevo.**

## 8. Lo que esta línea no decide

- **No recomienda ninguna quimera.** Produce un orden bajo un objetivo declarado; adoptar un
  candidato es una decisión del equipo con su ADR. Y hay un paso que falta antes y que esta
  feature no puede saltear: desde `D72` la compuerta rechaza una región ausente del
  inventario de `M6`, y **una juntura no es región de ningún gen**, así que hoy no tiene
  dónde entrar (`PREGUNTAS_ABIERTAS.md` 19). La salida declara esa condición en lugar de
  taparla.
- **No afirma eficacia.** El criterio de eficiencia no está validado en hemípteros, y el
  resultado in silico es una hipótesis sobre eficacia, no una prueba.
- **No decide el largo total ni las proporciones «óptimas».** Enumera lo que se le pide y
  reporta; el largo total lo fija quien corre, con su propio motivo.
- **No toca ninguna cifra publicada.** Si un número de esta línea contradijera uno
  publicado, eso va a `PREGUNTAS_ABIERTAS.md` y lo decide el equipo.

## 9. Confidencialidad

Ninguna secuencia sale de la máquina: las seis referencias se leen de disco, el plegado corre
con el módulo `RNA` local y el tamizado con un autómata en memoria. **Ninguna salida de este
bloque escribe bases**: las quimeras se identifican por gen, coordenadas, largo, offset y
hash corto, nunca por su secuencia, porque `BicC_Dm` es una de las cuatro secuencias de
EPILAB y una columna de ventanas solapadas reconstruye el gen —es el incidente de `C9`—. El
CDS de `V-ATPase B` no se versiona, igual que en `O2` y `O3`: se versiona el generador.
`tools/verificacion/sin_secuencias.py` tiene que seguir en **6 hallazgos no exceptuados**,
que es la línea base.

## 10. Enmienda del 2026-10-27, 11:45 (−03): la unidad del largo, con el nombre que ya tenía

El §3 de arriba declaró la grilla en «nucleótidos» sin nombrar el marco, y el §7 escribió el
ancla 3 contra `D74` como si las cifras de esa ADR fueran de nucleótidos. **El ancla falló y
la causa fue la unidad.** Lo que corresponde no es inventar vocabulario: el proyecto ya lo
tiene desde `D63`, y `N3` definió los dos marcos que importan acá —el **marco 1** cuenta los
`L` arranques que caen en la región, con las últimas veinte ventanas completadas por
nucleótidos de afuera, y el **marco 2** cuenta los `L − 20` 21-meros que existen físicamente
en la molécula—. Queda declarado así:

1. **La grilla enumera en marco 2.** El `--largo-total` son nucleótidos, porque es lo que se
   sintetiza, y un fragmento de `l` nt aporta `l − 20` ventanas propias.
2. **Cada candidato reporta las dos lecturas**, con los nombres de `D63`, y la salida nunca
   publica una sola de las dos sin decir cuál es.
3. **El ancla 3 corre en marco 1**, que es donde `D74` es reproducible: ahí da 71 ventanas
   vetadas, 1.184 regiones que caben, una sola admisible —517-816— y ninguna una unidad más
   grande, y **pasa** `[M]`. Imprime al lado la lectura de marco 2, que da 24 ubicaciones
   admisibles de 300 nt y 22 de 301 `[M]`.
4. **El eje de riesgo también se lee en marco 2**, y ésta es la desviación que hay que leer
   con cuidado: `ranking.ejes()` calcula el veto sobre el tramo del marco 1, de modo que una
   región puede quedar vetada por un 21-mero que la molécula no contiene. El caso medido está
   en `PREGUNTAS_ABIERTAS.md` 22. Enumerar el riesgo en marco 2 **no afloja** el criterio:
   descarta por los 21-meros que existen, que son los únicos que pueden pegar en algo. Cada
   candidato lleva igual la columna de si sería admisible también en marco 1, así que la
   lectura conservadora no se pierde.
5. **Lo que esta enmienda no hace:** no corrige `D74`, no mueve ninguna cifra publicada y no
   decide en qué marco debería leer el riesgo el resto del proyecto. Eso quedó planteado para
   el equipo. Y el alcance en las regiones vigentes quedó medido antes de seguir: los cuatro
   genes con insumo en esta máquina reproducen los dos marcos de `N3` celda por celda —38/31,
   21/20, 36/29 y 21/17— y **ninguna de las cuatro gana un acierto perfecto de 21 nt** al
   leerse en marco 1, así que el inventario de alertas de `M6` no se mueve `[M]`. `eth_Dm`
   114-313 y `bursA_Dm` 13-212 quedan sin medir por falta de `work/C11/` en esta máquina.
