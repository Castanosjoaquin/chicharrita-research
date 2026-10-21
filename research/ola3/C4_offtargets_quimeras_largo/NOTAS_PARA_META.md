# Notas para la memoria del proyecto — línea C4 (ola 3)

Para que el orquestador integre en `00_meta/`. No editamos `00_meta/` ni los REPORT.md de
otras investigaciones, y no hicimos commits (D5).

---

## Decisiones candidatas para `DECISIONS.md`

**D-C4-1. El umbral de off-target se declara en dos niveles y no en uno.** Se reporta siempre
el conteo con 21/21 perfecto *y* el conteo con bloque perfecto de ≥ 19 nt, y se dice cuál es
cuál. Motivo: el de 21 nt tiene bioensayo detrás en insectos (`S01`, `S02`, `S03`) y el de 19
nt es convención del campo con fundamento mecánico declarado pero sin experimento (`S06`).
Consecuencia: en nuestro conjunto de 920 ventanas, pasar de 19 a 21 nt borra todo el riesgo en
maíz salvo un acierto, y ese acierto cae en región intergénica. Alternativa descartada: elegir
un solo umbral «del campo», que es lo que veníamos haciendo sin fuente.

**D-C4-2. Los aciertos se ponderan por clase de blanco, y «genoma» no es una clase.** Las
clases son exón codificante, unión exón-exón del ARNm maduro, ARN no codificante anotado,
intrón e intergénico sin anotación. Motivo: medimos que la asimetría entre genoma y
transcriptoma va en los dos sentidos, y que el genoma pierde las ventanas de unión de exones,
que fueron las únicas que tocaron secuencia expresada de maíz. Consecuencia: el criterio que
entregó el investigador se implementa, pero con una corrección —no alcanza con preguntar «¿está
en el transcriptoma?», hay que preguntar «¿en qué parte cae?»—.

**D-C4-3. Las quimeras se recalculan enteras y en los dos órdenes.** Motivo: medido, el orden
cambia el total de eficientes entre +3 y +19 sobre la suma de partes, y el cambio de veredicto
de ventanas heredadas llega hasta 54 nt de la unión. Consecuencia: el atajo de sumar los
conteos de las partes puede errar por hasta 10 ventanas en una molécula de 500 nt.

**D-C4-4. El rango 150–250 nt se adopta como convención declarada, no como restricción
respaldada.** Motivo: no encontramos fuente que lo sostenga como techo y sí evidencia en
contra en la propia especie blanco (`S14`, 544 y 578 pb). Consecuencia: si una región candidata
quedara mejor con 300 nt, el largo no es argumento para descartarla; la restricción que sí hay
es el piso de ~60 pb.

---

## Caminos probados para `CAMINOS_PROBADOS.md`

**OpenAlex quedó fuera por falta de clave.** El conector de literatura del entorno requiere una
clave de API que no está configurada; devolvió `CredentialUnavailable`. No se intentó ninguna
llamada anónima. Se usó **Europe PMC** (búsqueda y `fullTextXML`), que resolvió 21 de 23 textos
completos. No es un bloqueo de red: es una credencial ausente.

**Dos textos completos cerrados.** `S18` (Castellanos et al. 2022, *Sci Total Environ*) sólo
devolvió resumen y se cita explícitamente como tal; `S23` (Whyard et al. 2009, *IBMB*) no
devolvió ni resumen y **no se cita de primera mano** —de ese trabajo sólo reportamos lo que
`S01` dice de él—. No se usaron espejos ni proxies.

**El backend `exe` del port no se pudo usar.** Necesita el RNAplfold 2.1.5 que instala si-Fi21
en Windows. Todos los números de eficiencia de esta línea son del backend `vienna` con
ViennaRNA 2.7.2, y los dos no dan lo mismo.

**La comparación genoma contra transcriptoma sólo es posible en 2 de los 17 conjuntos
locales.** Maíz y abeja. Se verificó antes de prometer el análisis, como pedía el encargo.
Falta el genoma de *Homalodisca vitripennis*, que es la comparación que más valdría porque ahí
están los 30 y 7 aciertos de W5.

**No se intentó clasificar los aciertos de abeja por clase de blanco.** Hay dos aciertos con un
desajuste que aparecen sólo en el transcriptoma y son candidatos a unión exón-exón; el script
`q2_empalme_exonico.py` los resolvería cambiando dos constantes.

---

## Preguntas abiertas para `PREGUNTAS_ABIERTAS.md`

1. **¿De dónde sale el 150–250 nt?** Si hay un ensayo propio del laboratorio con largos
   comparados en *Dalbulus maidis*, ese dato es más informativo que toda nuestra tabla de
   literatura, porque sería el único en el rango exacto, la especie exacta y la vía de entrega
   que ellos usan. Hoy la literatura abierta sostiene el piso de ~60 pb y no sostiene ningún
   techo; en su propia especie hay publicado silenciamiento con 544 y 578 pb.
2. **¿Qué peso relativo tiene un hemíptero no objetivo frente al maíz?** Es el único parámetro
   del criterio de ranking que no nos corresponde fijar, y es el que decide si `BicC_Dm` queda
   última o no. Se enlaza con la pregunta ya registrada sobre *Macrosteles quadrilineatus*,
   que es plaga y vector a la vez.
3. **¿EPILAB corre el tamizaje de off-targets contra transcriptomas, contra genomas, o contra
   los dos?** De eso depende si la ponderación por clase de blanco es una mejora o una
   corrección. El antecedente publicado en la especie (`S14`) usó BLASTn contra transcriptomas
   con criterio de significancia, sin umbral en nucleótidos.
4. **¿Se verificó alguna vez que un off-target predicho ocurra?** Ninguna de las herramientas
   que leímos valida sus predicciones con un experimento; `S05` es lo más cercano y es
   in silico más bioensayo de fenotipo, no medición de transcrito del gen no objetivo.
5. **¿Importa el sesgo de borde al recortar una región?** Medimos que el veredicto de
   eficiencia de una ventana cambia con el contexto hasta 54 nt de distancia. Eso implica que
   las ventanas de los primeros y últimos ~60 nt de una región recortada no valen lo que valían
   dentro del gen entero. Si el laboratorio elige región mirando el perfil del gen completo,
   este sesgo está presente y no está contabilizado.

---

## Fuentes nuevas para `FUENTES.md`

23 fuentes externas en `sources.json`, de las cuales **21 abiertas y leídas** por Europe PMC,
1 leída sólo en su resumen y 1 no abierta. Las que más cambian lo que el proyecto puede
afirmar: `S01` y `S02` (umbral de 21 nt y piso de 60 pb, con bioensayo), `S06` (la convención
de 19 nt, por fin con una fuente), `S05` (clasificación de aciertos en exón, intrón y unión),
`S11` y `S21` (ARNdc concatenado en dos hemípteros), `S14` (ARNdc de 544 y 578 pb que funciona
en *Dalbulus maidis*) y `S09` (no hay consenso de largo óptimo).

---

## Versiones y sumas de verificación

Entorno conda `w5bio`: Python 3.11.17, ViennaRNA 2.7.2, BLAST+ 2.17.0, Biopython 1.88,
`pyahocorasick` instalado para esta línea con pip dentro del entorno.

Port de si-Fi21 usado **sin modificar por nosotros**; md5 de los módulos al cierre de esta
investigación:

| Archivo | md5 |
| --- | --- |
| `barrido.py` | 26e0143363ec15fd45e636156b9df4fe |
| `cruce.py` | 8380923573caff8451f50ccc91e450a8 |
| `informe_html.py` | e22d4d5c6816a38c2c05ad825d354c9a |
| `offtarget_21nt.py` | 273068ea2707808fe535125617ddabe5 **al momento de nuestras corridas**; `caa84c037a043ab45560305968e80222` al cierre |
| `run_sifi.py` | c10604398e5ad8265caae6118a596adf |
| `sifi_core.py` | 52ad5dd8e611179c8ae74510cfe87a34 |
| `sifi_energy.py` | 9d7bffa234d80dde88de9fff17b58bf7 |
| `test_sifi.py` | cf562d5b908b9bc688198c7f938ddeaa |

**Concurrencia con otra línea de la ola 3.** Mientras corríamos, otra línea parametrizó
`offtarget_21nt.py` con `--size` y `--min-block` y lo commiteó (commit `478f165`, 16:43),
después de nuestros dos tamizajes. Los valores por defecto siguen siendo 21 y 19. Para no
firmar un número con una herramienta distinta de la que lo produjo, **volvimos a correr los dos
tamizajes con la versión nueva y comparamos**: los dos `offtarget_por_sirna.tsv` salen
**idénticos byte a byte** a los de la versión anterior (`work/C4/offtarget/gen_vs_tx_rev2` y
`quimeras_rev2`). Todos los conteos de esta línea valen para las dos versiones.

---

## Rechazos del filtro de seguridad

Ninguno. Ninguna búsqueda ni herramienta devolvió un rechazo de filtro de contenido en esta
línea.

## Contenido que intentó redirigirnos

Ninguno. Revisamos 21 textos completos y ninguno contenía instrucciones dirigidas al lector
automático. Se mantiene la regla de tratar todo lo traído de la web como dato.

## Confidencialidad

Las cuatro secuencias de EPILAB se procesaron sólo con herramientas locales. El único tráfico
de red fue entrante, contra Europe PMC, para buscar y bajar literatura pública. Los originales
de `YHat-Biotech/` no se tocaron: se trabajó sobre las copias de `work/C4/fasta/`, que a su vez
son copias de `work/W5/fasta/`.

## Archivos sobrantes que conviene borrar

En `resultados/` quedaron tres archivos sin sufijo de modo —`quimeras_eficiencia.tsv`,
`quimeras_ventanas_cambiadas.tsv` y `quimeras_meta.json`— de la primera corrida, antes de que
el script escribiera con el modo en el nombre. **Su contenido se reemplazó por una línea que
dice que están obsoletos y adónde ir**, para que nadie los lea como datos; no los borramos
porque no ejecutamos borrados dentro del repositorio. Conviene eliminarlos a mano. Los datos
buenos están en los pares con sufijo `_fiel_vienna` y `_corregido_vienna`.
