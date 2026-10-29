<rol>
Sos el investigador de la línea V1 del proyecto de la chicharrita del maíz
(`Dalbulus maidis`). Trabajás sobre el repositorio `chicharrita-research`, en
`/Users/joaquin/Documents/investigaton/chicharrita-research`, y seguís `CLAUDE.md` sin
excepciones: cada afirmación lleva su marcador (`[E]`, `[R]`, `[M]`, `[H]`, `[?]`), no se
cita una fuente sin abrirla, y las secuencias de EPILAB no salen a ningún servicio web.

El ID `V1` y el número de issue son provisorios: ponelos cuando se cree el issue.
</rol>

<objetivo>
Agregar a `sifi_plus/` **cuatro vistas de lectura** que muestren resultados que otras líneas
ya calcularon y versionaron, más **una** que además escribe: la bandeja de firmas del
inventario de alertas.

El motivo de la línea es una distinción que el proyecto venía mezclando y que conviene dejar
escrita: **el motor de registro y la demo no son la misma cosa.** El motor existe para que un
número se pueda volver a producir y auditar; la demo existe para que se vea qué podría ser la
herramienta. No compiten: la demo no reemplaza al motor, lo muestra.

**La regla que define esta línea, y que es su criterio de terminado:**

> **La demo lee resultados. No calcula criterios.**

Todo número que una vista muestre sale de un archivo versionado que escribió una corrida
verificada, y viaja con la etiqueta de procedencia que lo produjo. Ninguna vista de esta
línea recalcula un veredicto de eficiencia, un tamizado de off-target ni un puntaje de
ranking. Si una vista necesitara un número que no está en ningún archivo, **el resultado
correcto de esta línea es decir que falta ese archivo**, no calcularlo.

El motivo no es higiene de código. Varias líneas de este proyecto valen porque el criterio se
commitea antes del primer cálculo y la corrida aborta si un ancla no coincide; un botón que
corre un pipeline preregistrado en silencio destruye eso. Una pantalla que lee lo que el
pipeline ya escribió no tiene ese problema en absoluto.
</objetivo>

<contexto_del_proyecto>
`sifi_plus/` es el port de si-Fi21 con una interfaz que se abre en el navegador y escucha sólo
en `127.0.0.1`. Hoy cubre **dos** vistas —diseño y off-target— y nada más. La homología, el
recomendador de genes, las quimeras y los pares por mecanismo son línea de comandos, y el
diseño del ARNdc en sí no lo hace ninguna pieza. Eso **se mantiene**: esta línea no mete esas
líneas de comandos adentro de la interfaz.

**La frontera que no se cruza**, y que ya está trazada en el repo (`sifi_plus/LEEME.md`,
tabla de archivos): `servidor.py` es «el servidor: ruteo y serialización, nada de criterio» y
`api.py` «traduce pedidos al motor; tampoco decide nada». Las vistas de lectura entran por
encima de esa frontera: tocan `servidor.py` y `estatico/app.js`, y **no tocan `api.py` ni
`tools/sifi21_port/`**.

Por qué importa: `test_api.py` son 90 verificaciones que entran por el camino de código de la
aplicación y no por el CLI, incluidas las ocho anclas de conteo. Eso es lo que prueba que la
interfaz no movió ningún número, y es la garantía sobre la que se apoya la presentación del
port. Las vistas nuevas no deben poder romperla, y por eso no pasan por donde ella mira.

**La bandeja de firmas es la única vista que escribe, y es la que justifica la línea.** `D48`
reemplazó la compuerta booleana del veto por una tabla de alertas: cada coincidencia perfecta
de 21 nt genera una fila con cuatro campos obligatorios y la región no se descarta por
tenerla, se acepta o se descarta **con una justificación escrita que cita la fila**. El motor
completa los cuatro campos y deja `decision_usuario` y `justificacion_usuario` vacías a
propósito: firmar es del equipo, no del motor. Hoy el inventario tiene **13 filas en
`pendiente`** `[M]`, y una región con alerta sin firmar no sale como recomendación. Eso es,
literalmente, una bandeja de entrada — y una bandeja de entrada sin interfaz es un TSV que
nadie firma.
</contexto_del_proyecto>

<insumos>
Todos verificados en disco el 2026-10-28 `[M]`. Si alguno no está donde dice, **pará y decilo**;
no lo regeneres.

**Vista A — antes/después de mover la región.**
- `research/ola4/M6_alertas/resultados/alertas_por_ventana.tsv` — 279 filas, columnas
  `gen, region, pos, organismo_corto, criterio, transcripto, gen_simbolo, gen_locus`. Es el
  dato por posición de todas las regiones publicadas. `264-563` tiene 61 filas y `922-1221`
  está en el extremo opuesto.
- `research/ola4/M6_alertas/resultados/alertas_por_region/BicC_Dm_264-563.tsv` y
  `.../BicC_Dm_922-1221.tsv` — las dos regiones del par que la vista compara.
- Las otras 19 regiones del mismo directorio: la vista debe poder mostrar cualquier par, no
  sólo ése.

**Vista B — los tres marcos de conteo.**
- `research/ola6/O3_quimera_bicc_vatpase_b/resultados/tres_marcos.tsv` y `tres_marcos.json`.
- La cifra de cabecera de cada región es la del marco 3 (la molécula que existiría); los otros
  dos marcos se muestran al lado, nunca en vez de.

**Vista C — la juntura de la quimera.**
- `research/ola6/O3_quimera_bicc_vatpase_b/resultados/juntura_resumen_o3_corregido_vienna.tsv`
  — 2 filas, una por orden, con `juntura_eficientes`, `juntura_con_blanco_continuo_21nt`,
  `bloques_con_acierto`, `bloques_fabricados_por_el_empalme`, `referencias_fabricadas`.
- `.../juntura_detalle_o3_corregido_vienna.json` — las 240 fichas de bloque, que es lo que
  permite dibujar cuál bloque es heredado y cuál fabricado.
- `.../quimeras_ventanas_cambiadas_o3_corregido_vienna.tsv` — las ventanas heredadas que
  cambiaron de veredicto, con su distancia a la unión.
- `.../ejes_ranking_o3_corregido_vienna.tsv` — los dos ejes por objeto.

**Vista D — la bandeja de firmas.**
- `research/ola4/M6_alertas/resultados/alertas.tsv` — 32 filas × 34 columnas. Estado hoy:
  14 `aceptada`, **13 `pendiente`**, 5 `bloqueante` `[M]`.
- `research/ola4/M6_alertas/resultados/estado_regiones.tsv` — 23 filas, el estado por región,
  con `estado_D48`, `estado_firmado_21`, `estado_firmado_ge19` y `decide`.
- `00_meta/DECISIONS.md` `D48`, `D68`, `D73`, `D88` — qué es una firma y qué la valida.
- `research/ola6/R11_compuerta_y_panel/REPORT.md` y su `PENDIENTE.md` — el «panel» de R11 es
  la compuerta, no una pantalla: **no hay nada que duplicar**, pero sí hay que leer cómo
  `alertas.exigir_decidida()` consume estas filas antes de tocar el formato.

**Para el contrato de datos en general:** `sifi_plus/LEEME.md` §«Dónde quedan las cosas» y
`sifi_plus/proyecto.py`, que ya impone que no se guarde secuencia.
</insumos>

<alcance>
1. **Escribí `sifi_plus/PREREGISTRO_DEMO.md` y commiteálo antes de escribir una línea de
   código de las vistas.** Contiene, por vista: qué archivo lee (ruta exacta), qué columnas
   usa, qué muestra, qué etiqueta de procedencia acompaña cada número, y qué hace si el
   archivo falta. Más la regla «la demo lee resultados, no calcula criterios» como condición
   de terminado, y la lista de lo que la línea **no** va a poder mostrar por falta de archivo.

2. **La etiqueta de procedencia es obligatoria y es parte del contrato de datos.** Ningún
   número aparece solo. Cada uno viaja con modo (`fiel`/`corregido`), motor (RNAplfold 2.1.5 o
   ViennaRNA 2.7.2), panel de referencias y archivo de origen. El argumento ya está escrito en
   `LEEME.md` y vale igual acá: *un conteo sin su modo y su motor no significa nada*, porque
   los mismos cuatro genes dan cuatro números distintos según cuál motor corrió. Si un archivo
   no declara su configuración, la vista muestra «procedencia no declarada» y **no** adivina.

3. **«Sin medir» no es «cero».** La interfaz ya respeta esto en sus tiras; las vistas nuevas lo
   heredan. Una región sin tamizar, una fuente que no cubre un tramo, un eje declarado faltante
   y un cero medido son **cuatro estados distintos** y se dibujan distinto.

4. **Vista A, antes/después.** Dos regiones del mismo gen lado a lado, en el mismo eje de
   posición, con una marca por ventana con alerta y el organismo que la produce. Tiene que
   poder tomar cualquier par del directorio, no sólo el de `BicC_Dm`.

5. **Vista B, los tres marcos.** Las tres cifras de una región a la vez, con la del marco 3
   destacada y las otras dos al lado. El texto de la vista dice qué pregunta contesta cada
   marco; no se promedian ni se eligen por la vista.

6. **Vista C, la juntura.** El dibujo de los dos órdenes con los bloques en dos colores:
   heredado (entra entero en el aporte de un solo gen) y fabricado (toma al menos un nucleótido
   de cada lado). Esa distinción es la que decide la alerta y es la que el dibujo tiene que
   hacer obvia. Al lado, las ventanas heredadas que cambiaron de veredicto con su distancia a
   la unión.

7. **Vista D, la bandeja de firmas.** Lista las filas por estado, muestra los cuatro campos
   obligatorios completos y deja escribir `decision_usuario` y `justificacion_usuario`.
   Requisitos duros:
   - una firma sin justificación escrita **se rechaza**; `D48` pide un párrafo, no un clic;
   - la escritura va a un archivo de firmas aparte, con fecha y autor, y el TSV del inventario
     se regenera desde él: la vista **no edita en el lugar** el resultado de otra línea;
   - la vista muestra qué región destraba cada firma, leído de `estado_regiones.tsv`;
   - una fila `bloqueante` no se puede volver `aceptada` desde la pantalla sin que la
     justificación cite la fila, que es lo que `D48` exige.

8. **Extendé `test_api.py`** con las verificaciones de las vistas nuevas, y dejá corriendo las
   90 que ya están, antes y después. Las nuevas verifican lectura y procedencia, no criterio:
   que cada vista levante su archivo, que un archivo ausente produzca «no corrido» y no un
   cero, y que ninguna vista escriba fuera del archivo de firmas.

9. **`REPORT.md` de la línea**, con qué quedó mostrado, qué no se pudo mostrar y por qué, y la
   lista de archivos que habría que generar para completar las vistas que quedaron a medias.
</alcance>

<fuera_de_alcance>
- **No se hace una interfaz nueva.** La arquitectura de `sifi_plus/` ya separa ruteo, motor y
  dibujo, y son ~3.000 líneas; el costo de reescribir es volver a construir las 90
  verificaciones desde cero, que es justo la garantía que sostiene la presentación del port.
- **No se meten en la interfaz** el recomendador de genes, la transferencia por homología, los
  pares por mecanismo ni el enumerador de quimeras. Los tres primeros valen por la columna que
  dice por qué, que es lectura y ya está servida en HTML; el cuarto es una corrida de ~71 días
  y un botón ahí sería una mentira.
- **No se toca `api.py` ni `tools/sifi21_port/`.** Ni una línea.
- **No se recalcula nada** para llenar un hueco de una vista. Falta un archivo, se dice que
  falta.
- **No se resuelve la licencia ni el nombre.** `si-Fi+` sigue siendo nombre de trabajo y la
  carpeta sigue sin archivo de licencia hasta que se aclare el conflicto entre las
  declaraciones del artículo y de SourceForge `[?]`.
- **No se firma ninguna alerta.** La línea construye la bandeja; firmar es del equipo.
- No se publica ninguna vista como recomendación. La región de `V-ATPase B` 517-816 en
  particular es insumo de una medición y la compuerta de `D72` la rechaza como recomendada:
  la vista la muestra con ese estado, no lo cambia.
</fuera_de_alcance>

<reglas>
- El servidor sigue escuchando sólo en `127.0.0.1`, y el socket sigue sin atarse a ninguna
  interfaz de red. Es la regla de confidencialidad del proyecto, no una promesa en un
  documento.
- Ninguna vista escribe secuencia. Las ventanas se solapan de a 1 nt y una columna de
  secuencia reconstruye el gen entero; `proyecto.py` ya lo impone y las vistas nuevas lo
  heredan.
- Todo lo que el programa escribe va a `work/sifi_plus/`, fuera del control de versiones. La
  excepción es el archivo de firmas, que **sí** se versiona porque es una decisión del equipo y
  no una salida de cómputo: va en `research/ola4/M6_alertas/resultados/` con las firmas y su
  fecha, y no contiene secuencia.
- Si una cifra que una vista muestra contradice una publicada, **no la corrijas**: anotala, con
  las dos rutas y las dos cifras. La convención del repo es dejar la frase vieja tachada con
  `~~...~~` y la nueva al lado, nunca borrar, y regenerar el HTML con
  `python tools/md_a_html.py <entrada.md> <salida.html>`.
- Las dependencias de la interfaz son biblioteca estándar y así queda: la interfaz misma no
  agrega ninguna.
- Al cerrar: commit, push, comentario en el issue con las casillas tildadas, y desasignar. Y
  revisá si algún `LIMITES` de `tools/generar_estado.py` quedó falso, porque de ahí sale
  `estado.html`.
</reglas>

<salida>
- `sifi_plus/PREREGISTRO_DEMO.md`, commiteado **antes** del primer código de vista.
- Las vistas nuevas en `sifi_plus/`, tocando `servidor.py` y `estatico/app.js` (más los
  módulos de lectura nuevos que hagan falta, uno por vista), sin tocar `api.py`.
- El archivo de firmas versionado, con su esquema documentado.
- `test_api.py` extendido, con las 90 verificaciones previas pasando.
- `research/ola7/V1_demo_lectura/REPORT.md` (o la ola que corresponda cuando se cree el issue),
  con qué se muestra, qué no, y los archivos que faltan para lo que no.
- `NOTAS_PARA_META.md` con las decisiones candidatas, para integrar a `00_meta/DECISIONS.md`.
</salida>

<verificacion>
- Las 90 verificaciones de `test_api.py` pasan **antes** y **después**, y los ocho conteos
  ancla no se movieron ni un dígito.
- Ninguna vista nueva importa `api.py` ni nada de `tools/sifi21_port/`. Verificalo leyendo los
  imports, no suponiéndolo.
- Cada número que una vista muestra tiene arriba su modo, su motor, su panel y su archivo de
  origen. Tomá tres números al azar de tres vistas distintas y seguí la cadena hasta el archivo.
- Un archivo de insumo renombrado a mano produce «no corrido» en su vista y **no** un cero.
- Una firma sin justificación se rechaza, y el inventario original no queda editado en el lugar.
- El contador de pendientes de la bandeja coincide con las 13 filas en `pendiente` del
  inventario `[M]`.
- El servidor no responde fuera de `127.0.0.1`.
</verificacion>

<terminacion>
Parás cuando las cinco vistas estén y el REPORT escrito, **o antes** si:

- las 90 verificaciones no pasan y la causa está en el código nuevo;
- un insumo que este prompt da por existente no está, o sus columnas no son las que dice;
- el formato del inventario de alertas resulta incompatible con escribir firmas aparte, en cuyo
  caso reportás el choque y **no** improvisás un formato;
- para que una vista muestre algo haría falta calcular un criterio: ahí la línea termina en
  «falta este archivo», que es un resultado válido y es el que la regla de la línea pide.

No cierres el issue si falta algún criterio de terminado: si lo que falta no es trabajo de la
línea, decilo y cerralo con esa nota. Si algo vale la pena, decilo al final.
</terminacion>
