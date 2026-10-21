# Contraste: qué de lo que el repositorio ya afirmaba sobre si-Fi21 confirma, matiza o contradice el artículo

Una fila por afirmación. Las afirmaciones se citan abreviadas y con su origen; **no se
reescriben** los informes de donde salen (`tools/sifi21_port/CAMBIOS.md` y `README.md`,
`research/ola2/W2_herramientas/REPORT.md`, `research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md`).
El veredicto es contra el texto completo del artículo de Lück y colaboradores 2019, el manual
`Quick_help.pdf` del repositorio oficial y el fuente en `work/C1/siFi21--d6296b7/`.

| # | Afirmación del repositorio | Origen | Veredicto | Fundamento |
|---|---|---|---|---|
| 1 | Los tres filtros son selección de hebra guía por ΔG con extremos colgantes, estabilidad de extremos ≥ 1 kcal/mol y accesibilidad ≥ 0,1 con u = 8 | `CAMBIOS.md`, `README.md` del port | **Confirma** | El artículo enuncia los tres, juntos, en la Discusión (página 8), y el manual los lista como campos del modo diseño (página 7). Los valores coinciden exactamente |
| 2 | La regla terminal «no es un filtro: es una ramificación», y una rama declara eficiente sin mirar la termodinámica | `CAMBIOS.md` C1; `sifi21_reproduccion.md` §0 | **Confirma el hallazgo y contradice al código** | El artículo dice dos veces lo contrario de lo que el código hace: página 4, «se aplica una combinación de reglas de secuencia y termodinámicas»; página 6, «las reglas de secuencia de la versión anterior fueron reemplazadas por una combinación de cálculo termodinámico y reglas de secuencia». El modo «corregido» del port es el que respeta el artículo; el modo «fiel», el que respeta el programa |
| 3 | El umbral de 1 kcal/mol y el de 0,1 «son los valores del artículo y de la interfaz. No hay motivo para moverlos sin datos» | `CAMBIOS.md`, sección de lo que no se cambió | **Matiza** | Que son los del artículo es cierto (página 8 y pie de Figura 2A). Lo que el artículo **no** trae es la fuente del número: ninguna de las fuentes primarias abiertas fija 1 kcal/mol, y la única cifra medida comparable es la diferencia de 0,5 kcal/mol entre dúplex funcionales y no funcionales de Khvorova 2003. Son convenciones de los autores, no umbrales derivados de datos |
| 4 | «si-Fi no calcula a 37 °C»: está fijado a 22 °C en dos lugares | `CAMBIOS.md` C4 | **Confirma, y agrega** | Confirmado en `work/C1/siFi21--d6296b7/free_energy.py:420` y `sifi_pipeline.py:62`. Lo que agrega esta investigación: **el artículo no menciona ninguna temperatura en sus 12 páginas**, así que los 22 °C no se pueden atribuir a la publicación ni justificar con ella |
| 5 | «si-Fi ya está en las tablas modernas»: usa `RNA_NN3`, que es Chen 2012 | `CAMBIOS.md` C6 | **Confirma el código, matiza la atribución** | El default es `RNA_NN3` (`free_energy.py:278`) y Chen 2012 (texto completo) es fusión óptica de 29 dúplex de ARN en 1 M NaCl, reportada como ΔG°37. Pero el artículo **no nombra ninguna tabla termodinámica**, así que «si-Fi usa Chen 2012» es una afirmación sobre el código, no sobre el método publicado |
| 6 | La mezcla de tablas de ADN para desapareamientos dentro de un cálculo de ARN existe y está mal, pero no se alcanza en este uso | `CAMBIOS.md` C3 | **Confirma el código; el artículo no dice nada** | `free_energy.py:279` trae `tmm_table=DNA_TMM1`, `imm_table=DNA_IMM1`. El artículo no documenta el cálculo a ese nivel, de modo que no hay contraste posible: es un defecto del código sin contraparte en el texto |
| 7 | El conteo suma «un registro por hit de Bowtie, no un siRNA único» (`general_helpers.py:113`), por lo que depende de la base de datos | `sifi21_reproduccion.md` §0; `PREGUNTAS_ABIERTAS.md` | **Confirma, y el artículo y el manual lo respaldan** | El manual llama a la columna «Number of found siRNA hits (total and efficient) to the corresponding target» (página 12) y las Tablas 2 y 3 del artículo cuentan **hits por secuencia blanco**. La dependencia de la base no es una hipótesis del repositorio: es la unidad de conteo que la herramienta documenta |
| 8 | El perfil de eficiencia «es función únicamente de la secuencia» una vez que la base contiene el gen consultado | `CAMBIOS.md` C7 | **Confirma** | El veredicto por ventana depende sólo de la secuencia del siRNA, la del siRNA dos posiciones antes y el valor de accesibilidad (`sifi_pipeline.py:509-556`). Bowtie decide **qué** ventanas se registran, no **cómo** se clasifican. El manual describe el mismo flujo (página 2) |
| 9 | No hay en si-Fi un filtro llamado «identidad» | implícito en `CAMBIOS.md` y en el pendiente 4 del checkpoint | **Confirma, y explica de dónde viene la palabra** | No hay filtro de identidad. En el artículo, identidad es una variable experimental: la eficacia cae por debajo del 92 % de similitud global (Discusión, página 8; Tabla 1). En el programa, identidad es el presupuesto de desajustes de Bowtie, cero por defecto |
| 10 | si-Fi21 no busca la región de diseño; nuestra búsqueda de la región de 200 nt más densa es un agregado del port | `README.md` del port, implícito | **Confirma** | El fuente tiene un parámetro `region_plot_lst`, documentado como «Plot for suggested RNAi design region» (`show_plot.py:27` y `:41`, `create_plots.py:13` y `:23`), que **no se usa en ninguna línea**. El manual sólo da un criterio cualitativo de lectura del gráfico (página 9) |
| 11 | Conflicto de licencia: el artículo dice CC BY-SA 4.0 y SourceForge dice CC BY-NC 2.0 | `CAMBIOS.md`, `README.md`, `PREGUNTAS_ABIERTAS.md` | **Matiza y amplía** | El artículo dice CC BY-SA 4.0 (página 9). El **README de GitHub**, que abrimos, dice CC BY-NC-SA 2.0 —no CC BY-NC 2.0— y la última página del manual dice CC BY-NC-SA sin versión. O sea que hay **tres** declaraciones del licenciamiento del software, dos de ellas con cláusula NonCommercial incompatible con CC BY-SA. La declaración de SourceForge **no se pudo verificar**: el dominio está bloqueado en este entorno |
| 12 | El fuente de GitHub no es idéntico al binario de 2017 (`ui_sifi2015.py`: 23.791 contra 23.787 bytes) | `CAMBIOS.md`, advertencia de alcance | **No verificable acá; coherente con el artículo** | No pudimos abrir el binario (SourceForge bloqueado), así que la diferencia de bytes no se reprodujo. Lo que sí respalda la precaución: el artículo apunta a **tres artefactos distintos** —instalador en e!DAL `10.5447/ipk/2017/9`, fuente en Zenodo `10.5281/zenodo.845056` y la página del proyecto en GitHub— y el README de GitHub avisa que la herramienta no está actualizada |
| 13 | El port está verificado contra el original: 42, 32, 133 y 212 eficientes en los cuatro genes | `sifi21_reproduccion.md` §0 | **Fuera del alcance del artículo; no se tocó** | Es una verificación contra el programa, no contra el texto. Esta investigación no la repitió ni la necesitó |
| 14 | Bowtie, y no BLAST, hace el tamizaje de off-targets, y por eso lo eligen dsRNAEngineer, si-Fi21 y dsRIP | `W2/REPORT.md` §2.4 | **Confirma para si-Fi21, con la razón declarada** | Implementación, página 3: BOWTIE fue elegido por su exactitud, velocidad y eficiencia de memoria. El comando real es `bowtie -a -v N -y` (`sifi_pipeline.py:332`) |
| 15 | «En el corpus no hay ninguna herramienta que estime eficacia» | `W2/REPORT.md`, respuesta prioritaria | **Confirma, y vale también para si-Fi21** | si-Fi21 sí calcula termodinámica, pero su salida no es una eficacia estimada: es un booleano de reglas. Una revisión de 2026 sobre métodos de aprendizaje automático para diseño de siRNA (PMC13527166) lo clasifica explícitamente como herramienta sin componente predictivo entrenado |
| 16 | si-Fi21 es «la línea de base del campo» | `README.md` del port | **Matiza** | 128 citas en Europe PMC al 2026-10-20, con uso dominante en patosistemas de planta y hongo. En insectos el uso es escaso; en hemípteros encontramos **dos** trabajos, los dos de especificidad entre especies y ninguno de diseño de región, y **cero** en cicadélidos. Es la línea de base **declarada por el laboratorio**, que no es lo mismo |

## Lo que esta investigación agrega y el repositorio todavía no tenía

Tres cosas, por orden de impacto.

**Primero, un segundo apartamiento en la regla terminal.** El código comprueba la **posición 2**
del 21-mero (`sifi_pipeline.py:528` y `:543`) donde la fuente primaria (Ui-Tei 2004, condición ii)
y la propia geometría de si-Fi ponen la **posición 1**: el extremo 5' de la hebra sentido es el
que su propio cálculo de ΔG toma como tal en `sifi_pipeline.py:377`, con los índices 0 a 2.
El modo «corregido» del port hereda el índice: `tools/sifi21_port/sifi_core.py:192` y `:344` usan
`sirna[1]`. Medido sobre el genoma público `NC_002786.2` (6.346 ventanas), cambiar el índice
cambia la rama que decide en el 51,4 % de las ventanas y el booleano de preferencia terminal en el
31,4 %; cuántos veredictos finales cambian **no se midió**. `[E]` la medición, `[H]` llamarlo error
en vez de decisión no documentada.

**Segundo, el manual existía y no estaba leído.** `Quick_help.pdf`, dentro del propio repositorio
oficial, es la fuente más clara de los valores por defecto de cada modo, de la razón por la que la
eficiencia se apaga cuando se permiten desajustes, y de la lectura del gráfico. Varias preguntas
que el repositorio tenía abiertas sobre el comportamiento de la interfaz se contestan ahí.

**Tercero, el artículo respalda la decisión del modo corregido.** Hasta ahora esa decisión se
justificaba con un argumento biológico propio. Ahora tiene respaldo textual: el artículo describe
una combinación de reglas, no una ramificación, y es el código el que se aparta.
