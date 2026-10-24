# M5 — lo que va a `00_meta/`, separado por destino

Fecha: 2026-10-24. Fuente de todo lo de acá: [`REPORT.md`](REPORT.md) y `resultados/`.


## Para `DECISIONS.md`

**Enmienda a D47, con la medición al lado.** D47 está bien planteada y su consecuencia estaba mal estimada en un punto y subestimada en otro. Lo medido `[M]`:

- La consecuencia que D47 anticipa —«el veto se debilita y el empate vuelve»— es correcta en la dirección y **mucho más fuerte** en la magnitud: en la cascada el par `ATPaseD_Dm` / `CP_MRFV` no se empata, **se invierte**, del 100 % al 0 % de 2.000 sorteos. Y arrastra el orden entero: los dos genes del insecto suben cuatro puestos.
- El «47,4 % y 48,9 % de la grilla» que D47 cita como respaldo es de la ventana libre de 200 nt y ya estaba rectificado a **3,3 %** por C9 T1 bis. Conviene corregir la cita dentro de D47, que hoy repite una cifra superada.
- Lo que D47 no dice y es la consecuencia operativa principal: **el efecto no es gradual**. Entre `w_exposicion` = 0,05 y 1,00 (relativa al maíz) no cambia nada en la cascada; todo el cambio está entre 0,00 y 0,05. Con la regla de riesgo de hoy **no existe** el reparto intermedio que uno esperaría negociar, porque el veto es binario y sólo mira si la referencia está adentro. Hacerlo existir es exactamente D48 y la línea M6.
- Lo que D47 sí acierta y conviene dejar escrito con número: el orden de los dos primeros **aguanta** todo el rango, entre 96,0 % y 97,4 %.

**Entrada nueva a redactar con el usuario: el reparto se declara con fecha y con condición de revisión.** Si se adopta `w_exposicion`(*H. vitripennis*) = 0, la decisión depende de un hecho que puede cambiar —es plaga cuarentenaria ausente de la Argentina—, así que la entrada debería fijar que se revisa si cambia el estatus cuarentenario, y que las dos cifras (con y sin exposición) quedan publicadas para que esa revisión sea una lectura de tabla. Están en `research/ola4/M5_dos_ejes/resultados/tabla_afirmaciones.tsv`.

**Reabre D23 (*Macrosteles quadrilineatus* fuera del panel).** D23 lo sacó con un argumento **de exposición** —«la especie no está en Argentina y por lo tanto no es un organismo expuesto»— y la propia D23 anota que se lo había incorporado «como sustituto filogenético […], y ese uso no se descarta con su ausencia en Argentina». Con los dos ejes separados, la ausencia lo saca del eje de exposición y **no** del de conservación. Medido sin agregarlo al panel `[M]`: con un solo cicadélido el eje de conservación de `eth_Dm` es 0,0045 y con dos es 0,1050; el de `ATPaseD_Dm` pasa de 0,0310 a 0,1070. Con n = 1 referencia el eje no distingue «región poco conservada» de «región que esa fuente no cubre». D23 ya preveía esto: «reabrir si el investigador dice que los cicadélidos hermanos cuentan como no objetivo».

**Control de D59 extendido a los seis genes, con resultado negativo (que es el buen resultado).** De las 338 ventanas con coincidencia contra el panel —35 celdas de gen × referencia × criterio— **ninguna** es de baja complejidad, y de las 71 con 21/21 contra los dos cicadélidos, ninguna tampoco. En los seis genes el homopolímero más largo mide 7 nt contra un umbral de 10 y la ventana más pobre tiene 3 nucleótidos distintos contra un umbral de 2 `[M]`. Las 22 ventanas de `BicC_Dm` con *H. vitripennis*, de las que depende toda la discusión de M5, no son un artefacto de poli-A.


## Para `PREGUNTAS_ABIERTAS.md`

1. **Los dos pesos, que son el pedido 4 del lunes.** La medición está hecha y la decisión no es «cuánto», es **«cero o no cero»**: con la regla de riesgo de hoy no hay diferencia entre 0,05 y 1,00. Si se quiere un intermedio, hay que resolver antes M6 (#10).
2. **Cómo se reporta el tercer puesto.** Empate declarado o ranking ordenado. La medición dice que en la cascada el par se invierte y en las formas ponderadas no se mueve; o sea que la respuesta depende de qué forma de agregación se publica, y eso no está declarado en los entregables.
3. **Falta la referencia que el eje de exposición necesita y no existe: un cicadélido nativo argentino.** Los nativos sí están expuestos y no tienen genoma ni transcriptoma público con el que tamizar. Darle exposición cero a *H. vitripennis* —correcto por su ausencia— deja el eje de exposición **sin ningún representante de los cicadélidos no objetivo**, que son el grupo de riesgo más cercano al blanco por construcción del RNAi. Es un pendiente de datos, no un peso.
4. **k = 22 no se midió en esta línea.** Todo es a 21 nt. C9 T1 bis midió que el par `ATPaseD_Dm`/`CP_MRFV` se comporta distinto a 22 nt, así que la tabla de sensibilidad del reparto a 22 nt está **no corrida**, no en cero.
5. **El eje de conservación mide identidad contra transcriptomas, no conservación filogenética.** Lo que lo contestaría es un alineamiento múltiple de cicadélidos, que no existe en el repositorio.


## Para `CAMINOS_PROBADOS.md`

- **La separación no se implementó tocando `ranking.py`, y conviene que siga así.** `tools/sifi21_port/ejes_separados.py` define los dos vectores y **dos vistas disjuntas** del mismo dato de off-target, y le pasa al motor auditado de W7 sólo el vector de exposición. Dos consecuencias prácticas: el ancla contra `ranking_v2.json` sigue siendo exacta (6 de 6 exposiciones), y la prohibición de combinar los ejes se puede verificar por **invariancia** —correr el barrido con cuatro vectores de conservación distintos y comprobar que la salida es idéntica carácter por carácter— que es una prueba mucho más fuerte que la barrera sintáctica.
- **La barrera de tipos sirve, pero no es la verificación.** `Eje` levanta `TypeError` en toda operación entre ejes de nombre distinto y en `float()`. Nada impide escribir `a.valor_de("exposicion") + b.valor_de("conservacion")` a propósito; lo que está verificado es que el motor no lo hace.
- **Filtrar la referencia del dato, y no sólo ponerle peso cero.** Poner el peso en cero no alcanza: el veto, `con_off_target` y `buenos_limpios` de `ranking.ejes()` miran todas las referencias presentes sin mirar el peso. Una referencia con exposición cero tiene que salir de la **vista**, no sólo del promedio. Es el mismo patrón que `ranking_v2.quitar_humano()` ya usaba.
- **Anclas con el número de sorteos del original, no con el del barrido.** La primera corrida pasó `--muestras 300` también a las anclas y rompió 39 de 51 comparaciones: una frecuencia de 2.000 sorteos no se reproduce con 300. El abort funcionó como tenía que funcionar; las anclas quedaron fijadas en 2.000 y semilla 7, y `--muestras` sólo mueve el barrido propio.
- **`work/sifi_v2/` no existía y reconstruirlo costó tres minutos de cómputo, no un bloqueo.** Perfil de eficiencia de los seis genes con ViennaRNA, tamizaje contra las seis referencias del panel con `--mm1` (104 s) y contra el genoma del vector (40 s, sólo los dos genes virales, que son los únicos para los que entra al cómputo). La receta quedó en `scripts/reconstruir_insumos.py`.
- **Se probó medir el efecto del reparto con el veto de hoy y con el veto por exposición, y la comparación es la que explica todo.** Con las dos reglas, las formas ponderadas dan **exactamente lo mismo**, porque una referencia de peso cero ya aportaba cero al promedio. Todo el efecto de la separación corre por lo que mira la cascada. Sin esa rama de comparación, el resultado se habría atribuido a la ponderación.


## Contradicción con lo publicado en `entregables/` — no corregida por esta línea

Las tres afirmaciones de abajo dejan de estar sostenidas **si el usuario adopta `w_exposicion`(*H. vitripennis*) = 0**. Mientras no lo adopte, siguen valiendo tal como están publicadas. No se tocó ningún archivo de `entregables/` ni el ranking.

| Afirmación publicada | Dónde | Lo que mide M5 con exposición cero |
|---|---|---|
| «las dos regiones que EPILAB eligió para los genes del insecto quedan vetadas» | `entregables/checkpoint2-una-pagina.md`, punto 4 | **No quedan vetadas.** Las 22 ventanas de `BicC_Dm` 264-563 y las 3 de `ATPaseD_Dm` 151-450 son todas contra *H. vitripennis*: pasan a señal de conservación `[M]` |
| «La de `ATPaseD_Dm` (72-371) se mantiene» | `entregables/para-el-investigador.md`, fila 4, y D25 | El motor recomienda **137-436**, la región más conservada, que D25 descartó por estar vetada: 24 ventanas eficientes contra 18 `[M]` |
| el desempate del tercer puesto entre `ATPaseD_Dm` y `CP_MRFV` | D47, C9 T1 bis y el issue #9 | En la cascada **se invierte**: 0 % contra 100 % de 2.000 sorteos `[M]` |

Y una que **no** es efecto de esta línea pero conviene registrar: «`ATPaseD_Dm` último» (`entregables/para-el-investigador.md`, fila 3) se sostiene en escala absoluta en el 99,9-100 % de los sorteos en todo el rango, pero en la cascada es falsa en el 100 % —el último es `burs-α`— y eso ya estaba así en el `ranking_v2.json` publicado `[M]`.
