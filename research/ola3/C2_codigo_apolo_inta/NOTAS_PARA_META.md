# NOTAS_PARA_META.md — C2 (ola 3)

Para que el orquestador integre esto en `00_meta/`. No edité nada de `00_meta/` ni ningún
`REPORT.md` ajeno, y no hice commits (D5).

## Decisiones candidatas para DECISIONS.md

**D-cand-1. El port en modo fiel está verificado contra una segunda implementación
independiente, no sólo contra el programa original.** sifi21INTA, forzando su tabla de energía a la
del original, coincide con `tools/sifi21_port/` en modo fiel **ventana por ventana** en las 4.722
ventanas de los cuatro genes y en los cinco términos del veredicto, con cero diferencias. Dos
implementaciones escritas sin conocerse dan lo mismo. Consecuencia: cuando el equipo diga «nuestro
port reproduce si-Fi», ahora hay dos verificaciones, una contra el binario (W5) y otra contra una
librería de terceros (C2). Alternativa considerada: dar por suficiente la verificación de W5; se
descartó porque la coincidencia con un tercero descarta además errores compartidos entre el port y
nuestra lectura del fuente.

**D-cand-2. No reutilizar ni parecerse al código de los repositorios del INTA en la parte
versionada.** Los dos son GPL-3.0. El port nuestro deriva del fuente de `snowformatics`, no de
ellos, y su linaje está documentado desde antes; de acá en adelante hay que mantenerlo así. El
código de terceros quedó en `work/C2/`, fuera de git. Consecuencia práctica: si alguna vez se
publica el port, hay que resolver antes la licencia del original (ver contradicción abajo).

**D-cand-3. La pregunta para el investigador deja de ser «qué parámetros cambiaste» y pasa a ser
«¿pusiste el umbral de estabilidad de extremos en 1,75 o 2,0?».** Dos barridos independientes
—el de W5 sobre nuestro port y el de C2 sobre sifi21INTA— apuntan al mismo parámetro y no a la
química.

## Caminos probados, para CAMINOS_PROBADOS.md

**Cerrado con medición: la base de datos no explica los conteos de la planilla, si el laboratorio
corrió sifi21INTA.** En esa librería el conteo de eficientes es por ventana
(`SifiPipeline.py:430-448`) y no por hit de Bowtie como en el original (`general_helpers.py:113`).
Medido contra tres bases —los cuatro genes, los 71 registros públicos de MRFV y el transcriptoma TSA
GITV01 de *Dalbulus maidis*—: 138, 40, 218 y 35 en las tres, sin mover una unidad. La columna que sí
depende de la base es la nueva, «eficientes sin off-targets», y ninguno de sus valores (0, 0, 214,
12) es el declarado. Esto responde a la pregunta 2 de la lista consolidada de
`PREGUNTAS_ABIERTAS.md`, **pero sólo bajo el supuesto de que corrieron esta librería**: si corrieron
el programa original, la hipótesis de la base sigue viva tal como estaba.

**Descartado: que la tabla de energía nueva explique la diferencia.** Es el único cambio químico
—`RNA_NN4`, atribuida en el comentario a Zuber et al. 2022, `freeEnergy.py:61-74`— y mueve los
conteos sólo −4, +1, −5 y 0.

**Descartado por SHA, sin bajar contenido: seis de los ocho forks de si-Fi21.** Su cabeza es un
commit de la historia de upstream. Método barato y reutilizable: `git ls-remote` contra la lista de
commits de la API.

**Camino que no se pudo tomar: clonar con git.** El entorno no permite crear ningún directorio
llamado `.git` (falla también `git clone --bare` sobre `repo.git`). Se resolvió bajando tarballs por
`api.github.com/repos/<owner>/<repo>/tarball[/<ref>]` y verificando cada commit con `git ls-remote`,
que sí funciona. Vale anotarlo porque va a volver a pasar.

## Preguntas abiertas nuevas, para PREGUNTAS_ABIERTAS.md

1. **¿Qué versión de ViennaRNA usa el servidor de Apolo Rocket?** Sin eso no hay forma de comparar
   contra nuestras corridas. Entre 2.1.5 y 2.7.2 hay varios eficientes de diferencia por gen.
2. **RNAplfold 2.1.5 no está en esta máquina.** Por eso la comparación de sifi21INTA contra la
   corrida del programa original de W5 queda confundida por la versión. Es barato de cerrar para
   quien tenga la instalación de Windows de si-Fi.
3. **¿Los números de la planilla son «eficientes» o «eficientes sin off-targets»?** En sifi21INTA son
   dos columnas distintas y la segunda depende de la base y del blanco principal elegido a mano.
4. **¿El método «IA» de Apolo Rocket existe fuera del esquema?** El campo `method` está documentado
   como «'sifi21' or 'IA'» y viaja a la base, pero no hay implementación en el backend público.
5. **La tabla RNA_NN4: ¿los valores son realmente los de Zuber et al. 2022?** No abrimos el artículo;
   la atribución es del comentario del código.

## Contradicción resuelta, y una nueva

**Resuelta a medias, con fuente abierta: la licencia del si-Fi21 original.** El repositorio no trae
archivo de licencia y su README declara, en la línea 19, CC BY-NC-SA 2.0 Generic. Es decir que el
`[?]` que el proyecto tenía anotado —artículo CC BY-SA 4.0 contra SourceForge CC BY-NC 2.0— ahora
tiene un tercer valor, el del repositorio. Sigue sin resolverse cuál rige.

**Nueva `[?]`: los derivados del INTA están bajo GPL-3.0.** Una licencia con cláusula no comercial y
*share alike* no es compatible con relicenciar un derivado bajo GPL-3.0. La cadena de licencias
tiene una inconsistencia declarada en las propias fuentes. No es asesoría legal; queda anotado por si
se publica algo.

## Para el GLOSARIO

- **RNA_NN4**: tabla de parámetros de vecinos más cercanos (nearest neighbours) que sifi21INTA y
  Apolo Rocket usan por defecto en vez de la de Chen et al. 2012; el comentario del código la
  atribuye a Zuber et al. 2022. Nos importa porque es el único cambio químico entre si-Fi21 y la
  versión del INTA.
- **Blanco principal (main target)**: la región o secuencia que el usuario declara como objetivo
  deseado; todo hit fuera de ella cuenta como off-target. Nos importa porque es una decisión humana
  sin registro de la que depende por completo la columna de eficientes sin off-targets.
- **Bypass de la regla terminal**: la rama del criterio de si-Fi que devuelve «eficiente» mirando
  sólo la accesibilidad, sin el veredicto termodinámico. Nos importa porque está viva en las tres
  implementaciones públicas que leímos.

## Advertencias operativas

- **sifi21INTA no corre con Biopython ≥ 1.82** (`freeEnergy.py:384` usa `Bio.SeqUtils.GC`, eliminado
  en esa versión). Hay que fijar 1.81. Si alguien repite las corridas y le aborta, es esto.
- **Secuencias en minúsculas dan cero eficientes sin avisar**, en las dos librerías del INTA y en el
  original. Medido: 138 contra 0 en `MP_MRFV_full`. Si el equipo vuelve a correr cualquiera de estas
  herramientas sobre un FASTA enmascarado (soft-masked), el resultado va a ser cero y va a parecer
  válido.
- **El repositorio público de apolorocket trae credenciales de base de datos en claro**
  (`constants.py:11-16`: nombre, usuario, contraseña, host y puerto, más una ruta absoluta con un
  directorio personal). No reproduje los valores en ningún entregable y recomiendo no hacerlo. Si
  alguna vez hay contacto con el grupo, es algo que agradecerían saber.
- **Nada de lo leído intentó redirigir el trabajo.** El fork `rj-price/siFi-2.0` trae archivos de
  guía para asistentes de código (`CLAUDE.md`, `PLAN.md`); se leyeron **como dato**, para extraer su
  lista de defectos conocidos, y no se siguió ninguna instrucción escrita ahí. Ningún otro contenido
  de repositorio, PDF o volcado contenía texto dirigido a un agente.
- **Dos repositorios públicos nuevos para el radar del equipo**: `DanielHarley/zeaguard-drylab`
  (dsRNA contra *D. maidis*, Bicaudal C y dsRNase-2, push del 2026-10-15) y `MaxiSack/RNAival`
  (identificación de candidatos de siRNA, GPL-3.0, push del 2026-10-19). De los dos se leyó sólo el
  README.
