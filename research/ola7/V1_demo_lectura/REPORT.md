# V1 — Cinco vistas de lectura en si-Fi+

Issue **#45**. Antecedentes: `D48`, `D68`, `D69`, `D72`, `D73`, `D74`, `D77`, `D78`, `D88`, y el
preregistro de la línea en `sifi_plus/PREREGISTRO_DEMO.md`, commiteado antes del primer renglón
de código de las vistas (`fbb8eab`).

La línea existe por una distinción que el proyecto venía mezclando: **el motor de registro y la
demo no son la misma cosa.** El motor existe para que un número se pueda volver a producir y
auditar; la demo existe para que se vea qué podría ser la herramienta. No compiten —la demo no
reemplaza al motor, lo muestra— y la forma de que no compitan es una regla, que es también el
criterio de terminado de la línea:

> La demo lee resultados. No calcula criterios.

Las cinco vistas están y la regla se sostiene. Lo que sigue dice qué quedó mostrado, qué **no**
se pudo mostrar y qué archivo haría falta para mostrarlo, porque esa última lista es resultado
de la línea y no una disculpa: varias líneas de este proyecto valen porque el criterio se
commitea antes del primer cálculo y la corrida aborta si un ancla no coincide, y un botón que
corre un pipeline preregistrado en silencio destruye eso. Una pantalla que lee lo que el
pipeline ya escribió no tiene ese problema en absoluto.

## 1. Lo que quedó mostrado

Cinco pestañas nuevas, cuatro de lectura y una que además escribe. Cada una lee archivos
versionados que escribieron corridas verificadas, y **ningún número aparece solo**: todos viajan
con modo, motor, panel y archivo de origen.

| Vista | Qué muestra | De dónde |
|---|---|---|
| **Mover la región** | dos regiones del mismo gen en el mismo eje, con una marca por ventana con alerta y el organismo que la produce | `alertas_por_ventana.tsv` + los 21 archivos de `alertas_por_region/` |
| **Tres marcos** | las tres cifras de conteo de una región, con la del marco 3 destacada | `tres_marcos.tsv`, configuración de `tres_marcos.json` |
| **Juntura** | los dos órdenes con el bloque heredado separado del fabricado, y las ventanas heredadas que cambiaron de veredicto | `juntura_resumen_*.tsv`, `juntura_detalle_*.json`, `quimeras_ventanas_cambiadas_*.tsv` |
| **Ejes** | los dos ejes de los cuatro objetos, bajo las dos reglas, sin combinarlos | `ejes_ranking_*.tsv` |
| **Bandeja de firmas** | las 32 filas de alerta por estado, con sus cuatro campos obligatorios y el formulario de firma | `alertas.tsv`, `estado_regiones.tsv`, `decisiones.tsv` |

La vista de ejes es la cuarta de lectura y resuelve una inconsistencia del pedido, que enumeraba
cuatro vistas de lectura pero describía tres más la bandeja: `ejes_ranking_o3_corregido_vienna.tsv`
estaba listado como insumo de la vista de juntura sin que ninguna pantalla lo mostrara. Darle
vista propia usa todos los insumos declarados y deja la de juntura con una sola cosa que contar.

**La arquitectura no se tocó.** Las vistas entran por encima de la frontera que `LEEME.md` ya
tenía trazada: `servidor.py` gana seis rutas y `estatico/app.js` el dibujo, y cada vista es un
módulo de lectura propio —`lectura.py` con lo común y cinco `vista_*.py`—. **`api.py` y
`tools/sifi21_port/` no se tocaron, ni una línea**, y tampoco se importan: `test_api.py` lo
verifica leyendo el árbol sintáctico de cada módulo y no con un `grep`, porque `import api`
adentro de un comentario no es un import y un `grep` no sabe la diferencia.

## 2. Las verificaciones

`python test_api.py` pasa de **75** a **189 verificaciones**, todas en verde, con los mismos
cinco bloques declarados «no corrido» antes y después `[M]`.

Conviene ser preciso con el número, porque el pedido hablaba de 90 y en esta máquina no son 90:
las 90 de `LEEME.md` son con todos los insumos en disco, y acá faltan el RNAplfold 2.1.5 del
original —es el `.exe` que instala si-Fi21 en Windows— y `work/sifi_check/NC_002786.2.fasta`. Los
cinco bloques que dependen de eso **se declaran no corridos en vez de pasar como verdes**, que es
el patrón del repositorio. Medido antes de tocar nada: 75 pasan, 0 fallan, 5 no corren. Después:
189 pasan, 0 fallan, los mismos 5 no corren `[M]`.

**Los conteos ancla no se movieron ni un dígito.** Los ocho que sí corren en esta máquina —los
de ViennaRNA 2.7.2 en los dos modos sobre los cuatro genes— dan `[142, 39, 223, 35]` en modo
fiel y `[123, 30, 171, 29]` en corregido, que es exactamente lo publicado `[M]`. Los ocho de
RNAplfold 2.1.5 no corren acá y quedan declarados. Que no se muevan no es suerte: las vistas no
llaman al motor, así que no tienen por dónde moverlos.

Las verificaciones nuevas miran **lectura y procedencia, no criterio**:

1. Cada vista levanta su archivo y devuelve exactamente las filas que el archivo tiene —contadas
   contra el archivo en disco, no contra un número escrito en el test.
2. Un insumo ausente produce «no corrido» y **ni un solo número** en la respuesta. Se verifica
   apuntando cada módulo a una ruta inexistente, no renombrando el archivo de verdad: renombrar
   el resultado de otra línea para correr una prueba es la clase de cosa que queda renombrada.
3. Falta sólo el JSON de configuración de la vista de marcos: las cifras siguen estando y salen
   con «procedencia no declarada». Es el caso intermedio y el más fácil de hacer mal.
4. Ningún módulo de vista importa `api` ni nada del port.
5. Las constantes de validación de firma de la vista **coinciden con las de
   `tools/sifi21_port/alertas.py`**, leído como texto y parseado, sin importarlo. Es el tripwire
   contra que las dos copias se separen en silencio.
6. Las cinco formas de rechazar una firma, y que el inventario no quede tocado.
7. Ninguna vista de lectura tiene una llamada de escritura —verificado sobre el árbol
   sintáctico— y correr las cuatro no cambia la huella de ninguno de los ocho archivos que leen.
8. El servidor sigue atado a `127.0.0.1` y no hay ninguna cadena `0.0.0.0` en su código.

Sobre la última: `0.0.0.0` **sí** aparece en `servidor.py`, en la prosa que explica por qué no se
usa, y esa frase es parte de la garantía. La verificación separa las dos cosas sacando los
docstrings del árbol, que es la diferencia entre documentar una decisión y tomarla al revés.

El contador de pendientes de la bandeja da **13**, que son las 13 filas en `pendiente` del
inventario `[M]`. Y la cadena de procedencia se siguió hasta el archivo para tres números de tres
vistas distintas: el marco 3 de `BicC_Dm` 922-1221 (26, columna `marco3_molecula`, con el ancla
`[36, 29, 26]` del propio JSON), los tres bloques fabricados de `Q_VATPaseB_Dm__BicC_Dm` (3 en el
resumen y 3 fichas con `cruza_la_union` en el detalle) y las 13 pendientes `[M]`.

## 3. La bandeja de firmas, que es la que justifica la línea

Una bandeja de entrada sin interfaz es un TSV que nadie firma. `D48` reemplazó la compuerta
booleana del veto por una tabla de alertas, el motor completa los cuatro campos obligatorios y
deja la decisión vacía a propósito, y hoy quedan 13 filas en `pendiente`.

**El archivo de firmas no hubo que inventarlo: ya existe.** `D68` sacó la firma de la tabla y la
puso en `research/ola4/M6_alertas/decisiones.tsv`, que es **entrada** del generador y no salida
suya, precisamente porque `tabla_alertas.py` reconstruye `alertas.tsv` desde cero en cada corrida
y una firma escrita sobre la tabla se perdía sin aviso. Son diez columnas, con los dos conteos de
`D28` como huella. La vista escribe ahí y **no edita el inventario en el lugar**; después dice,
con el comando exacto, que el inventario se regenera corriendo el generador. El formato resultó
compatible y no hizo falta improvisar nada.

Dos cosas que la vista hace y vale la pena que estén escritas. La huella **se lee de la fila que
la vista muestra**, no de lo que manda el navegador: una firma cuya huella la pone quien firma no
verifica nada. Y la escritura es por reemplazo atómico, porque el archivo de firmas es la única
cosa de esta línea que no se puede regenerar desde un cálculo —son decisiones escritas por
personas— y un `open(..., "w")` que falla a la mitad lo deja truncado.

### El hecho medido que la bandeja tiene que decir y no suavizar

**Las 13 filas pendientes tienen todas cero ventanas con coincidencia perfecta de 21 nt** `[M]`.
Como el umbral con el que la compuerta exige decisión es `perfecto_21` —`D48` literal,
`ranking.UMBRAL_COMPUERTA`— firmarlas **no destraba ninguna región en el umbral vigente**: en
`perfecto_21` ya pasan las 23 regiones del inventario. Cuentan en el umbral laxo de `D28`,
`perfecto_ge19`, donde son seis las regiones frenadas y **ninguna de ellas vigente**
(`umbral_compuerta.json`) `[M]`.

La bandeja muestra las dos columnas, dice cuál es la vigente y lo repite por fila. Presentar «13
firmas pendientes» como si fueran 13 regiones trabadas sería inventar una urgencia que la
medición no respalda, y es exactamente el tipo de cosa que una pantalla hace fácil.

**Esta línea no firmó ninguna alerta.** Construye la bandeja; firmar es del equipo. Las pruebas
del camino de escritura corren contra una copia en un directorio temporal, no contra
`decisiones.tsv`.

## 4. Lo que no se pudo mostrar, y qué archivo haría falta

Esto es resultado de la línea. La regla dice que si una vista necesita un número que no está en
ningún archivo, el resultado correcto es decir que falta ese archivo.

**1. La geometría de 221 de los 240 bloques de la juntura.** `juntura_detalle_o3_corregido_vienna.json`
trae **19 fichas**, las de los bloques con acierto, bajo la clave `bloques_con_acierto` `[M]`. Los
otros 221 bloques existen —son los que la juntura enumera— pero ninguna de sus propiedades está
en un archivo versionado, así que el dibujo marca los 19 medidos y deja el resto como **no
medido**: ni heredado ni sin acierto. Deducir su geometría sería calcular. *Falta* un archivo con
una ficha por bloque enumerado, con `cruza_la_union`, `nt_de_izquierda` y `nt_de_derecha`.

**2. El modo y el motor de las dos columnas de eficiencia de `M6`.** Ningún archivo de
`research/ola4/M6_alertas/resultados/` declara su configuración `[M]`. `ventanas_21_eficientes` y
`ventanas_ge19_eficientes` dependen del modo y del motor, así que salen marcadas con «procedencia
no declarada». No se dedujeron de `tabla_alertas.py`, que las fija en una ruta literal de su
código: que el generador fije el modo en su fuente no es que el resultado lo declare. *Falta* un
sidecar de configuración, como el que `O3` sí tiene.

**3. El panel de referencias, en dos lugares distintos.** En `M6` no está declarado en ningún
archivo, y en los ejes de `O3` no lo declaran ni `ejes_ranking_*.tsv` ni su sidecar
`quimeras_meta_*.json`, pese a que `limpieza`, `con_off_target` y `con_21_perfecto` dependen de
él `[M]`. Las dos vistas lo muestran como no declarado.

Acá hay una distinción que era fácil de pasar por alto y que conviene dejar escrita: **los
organismos que aparecen en la tabla de alertas no son el panel**. Son los que *tuvieron* alerta.
Una referencia con cero aciertos no deja ninguna fila, así que leer el panel de las filas
confundiría «no tiene aciertos» con «no se miró», que es justo la distinción que `D72` existe
para hacer. La vista lista los organismos con alerta y dice con todas las letras que eso no es el
panel.

**4. La matriz de off-target de `V-ATPase B` contra el panel completo.** `D78` la declaró
faltante y sigue faltando. La región 517-816 entra a la bandeja con las filas que tiene y con el
estado que la compuerta de `D72` le da.

**5. Cualquier par de regiones que no esté entre los 21 archivos del directorio.** La vista dice
que falta ese archivo. No lo tamiza.

## 5. Una cifra publicada que no cierra, anotada y no corregida

`research/ola6/O3_quimera_bicc_vatpase_b/REPORT.md:371` describe
`resultados/juntura_detalle_o3_corregido_vienna.json` como «los 240 bloques, con aporte por gen y
sin secuencias». El archivo en disco tiene **19 fichas** bajo `bloques_con_acierto` `[M]`.

La línea 218 del mismo REPORT lo dice bien —«de las 240 fichas de bloque, 19 tienen acierto»— así
que lo que está mal escrito es la tabla de archivos y no la medición. Siguiendo la convención del
repositorio, la frase vieja queda tachada con la nueva al lado, en vez de borrarse. La vista
muestra las dos cifras con sus dos rutas y declara la diferencia como no medida.

## 6. Lo que esta línea no hizo, a propósito

- No se hizo una interfaz nueva. La arquitectura ya separa ruteo, motor y dibujo, y reescribirla
  costaba volver a construir las verificaciones desde cero, que es la garantía que sostiene la
  presentación del port.
- No entraron a la interfaz el recomendador de genes, la transferencia por homología, los pares
  por mecanismo ni el enumerador de quimeras.
- No se recalculó nada para llenar un hueco.
- No se resolvió la licencia ni el nombre. «si-Fi+» sigue siendo nombre de trabajo y la carpeta
  sigue sin archivo de licencia hasta que se aclare el conflicto entre las declaraciones del
  artículo y de SourceForge `[?]`.
- No se publicó ninguna vista como recomendación. `V-ATPase B` 517-816 es insumo de una medición
  y la compuerta la rechaza como recomendada: la vista la muestra con ese estado.
- No se firmó ninguna alerta.

Y dos cosas de higiene que la regla de la línea pedía revisar: ningún `LIMITES` de
`tools/generar_estado.py` quedó falso —los cinco son límites de investigación y esta línea no
mueve ninguna medición— y las dependencias de la interfaz siguen siendo biblioteca estándar: las
vistas no agregan ninguna.

## 7. Los archivos

| Archivo | Qué es |
|---|---|
| `sifi_plus/PREREGISTRO_DEMO.md` | el contrato de las cinco vistas, commiteado antes del primer código |
| `sifi_plus/lectura.py` | lo común: abrir un archivo declarando si estaba, y la etiqueta de procedencia |
| `sifi_plus/vista_region.py` | vista A, el par de regiones sobre el mismo eje |
| `sifi_plus/vista_marcos.py` | vista B, los tres marcos de conteo |
| `sifi_plus/vista_juntura.py` | vista C, el heredado contra el fabricado |
| `sifi_plus/vista_ejes.py` | vista E, los dos ejes por objeto |
| `sifi_plus/vista_firmas.py` | vista D, la bandeja: la única que escribe |
| `sifi_plus/servidor.py` | seis rutas nuevas; `firmar` es la única POST |
| `sifi_plus/estatico/app.js` | el dibujo de las cinco vistas |
| `sifi_plus/test_api.py` | 189 verificaciones, de 75 |

El archivo de firmas sigue siendo `research/ola4/M6_alertas/decisiones.tsv`, con su esquema
documentado en el preregistro y en `tools/sifi21_port/alertas.py`. No se le cambió el formato.
