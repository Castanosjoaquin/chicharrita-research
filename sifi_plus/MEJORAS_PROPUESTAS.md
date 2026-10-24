# Mejoras propuestas, no implementadas

Ocho cosas que detectamos leyendo y midiendo si-Fi21, que **no** cambiamos. Cada una dice qué
hace hoy el programa, qué sabemos, qué cambiaría si se tocara, y qué nos falta para decidir.

Están sin implementar a propósito. Varias mueven números que ya están en circulación —los de
la planilla del EPILAB entre ellos— y cambiar el criterio por nuestra cuenta convierte una
discrepancia discutible en dos criterios incomparables. La idea es decidirlas con vos.

Están ordenadas por cuánto mueven el resultado, no por cuánto cuestan.

---

## 1. El índice de la regla terminal: posición 2 contra posición 1

**Es la más grande y la que menos nos animamos a tocar solos.**

La regla del nucleótido terminal 5′ habla del extremo 5′ de la hebra opuesta, que en la
geometría del propio si-Fi —ventana de 21 nt con 2 nt de saliente (*overhang*)— es la
**posición 1** del 21-mero. El código comprueba `sirna_sequence[1]`, que es la **posición 2**
(`sifi_pipeline.py:528` y `:543`).

Medido: corregir el índice **cambia la rama que decide en el 51,4 % de las ventanas** —3.265 de
6.346— `[M]`. No es un ajuste fino: reparte las ventanas entre las cuatro ramas de otra manera.

No lo implementamos porque no sabemos si es un error de transcripción o una decisión. Si es lo
primero, hay una década de resultados calculados con el índice corrido. La propuesta es
agregarlo como un **tercer modo**, al lado de fiel y corregido, y no como el comportamiento por
defecto.

**Lo que necesitamos de vos:** si en el laboratorio la regla se entiende sobre la posición 1 o
sobre la 2.

## 2. Ponderar los desajustes por su posición en el siRNA

si-Fi corre `bowtie -a -v N -y` y cuenta aciertos extremo a extremo, **ciego a dónde cayó el
desajuste** (`sifi_pipeline.py:332`). Químicamente no es lo mismo: un desajuste en la región
semilla (*seed*, nt 2-8) gobierna la nucleación, y en las posiciones 10-11 el apareamiento es
indispensable para el corte. Un siRNA con el desajuste en la semilla y otro con el desajuste en
la posición 15 cuentan igual, y no deberían.

Es la crítica a la herramienta que creemos más sólida y la única claramente pendiente. No la
implementamos porque pertenece al módulo de off-targets y meterla en el criterio de eficiencia
mezcla dos cosas; además cambia el ordenamiento de candidatos que ya entregamos.

**Lo que necesitamos de vos:** si tenés una referencia de cuánto pesa cada posición, o si
preferís que la propongamos nosotros con lo publicado y la marquemos como hipótesis.

## 3. La baja complejidad, contrastada contra el estándar

Esto sí lo implementamos, pero con un criterio propio, y queremos reemplazarlo.

Encontramos que las coincidencias perfectas de 21/21 nt del genoma del *Maize rayado fino
virus* en tres transcriptomas no objetivo son **todas la cola de poli-A** `[M]`: descontándolas,
9, 11 y 13 pasan a cero. si-Fi no marca esto en ningún lado, así que su conteo de off-targets
mezcla poli-A con homología real.

Nuestra marca es grosera y está declarada en `complejidad.py`: racha de un mismo nucleótido de
10 nt o más, o dos nucleótidos distintos o menos `[H]`. Lo correcto es contrastarla contra
`dustmasker`, que es el estándar y del que el repositorio ya tiene una corrida sobre los genes.
No lo hicimos todavía.

## 4. El umbral de 1 kcal/mol y los 22 °C no tienen fuente primaria

De los seis filtros que deciden el veredicto, **dos tienen fuente primaria empírica abierta y
específica** —el tamaño de 21 nt y la regla del nucleótido terminal—, **dos tienen fuente para
el principio pero no para el número** —la asimetría y la accesibilidad— y **dos no tienen
ninguna**: el 1 kcal/mol de estabilidad de extremos y los 22 °C `[R]`.

No es un error y no proponemos moverlos. Proponemos **declararlo**: son convenciones heredadas,
no constantes medidas, y conviene que quien lee un conteo lo sepa. Conviene aclarar dos cosas
que circulan al revés, porque las verificamos en el código: si-Fi **no** calcula a 37 °C —son
22 °C, fijados en dos lugares independientes— y **no** calcula a 1 M de NaCl, son ~70 mM `[M]`.

## 5. El paper escribe `>` y el código aplica `>=`

En el umbral de estabilidad de extremos, el artículo y el código no dicen lo mismo `[?]`. El
efecto es chico —afecta sólo a las ventanas que caen exactamente en el umbral— pero es
exactamente el tipo de cosa que hace que dos implementaciones del «mismo» criterio no cierren.
Mantuvimos el `>=` del código, porque la pregunta era reproducir el programa.

## 6. Generalizar la regla terminal a 22 nt

La ventana de 21 nt está fijada, pero en el checkpoint quedó que 21-22 nt es lo que tiene
respaldo biológico. El CLI ya acepta `--sirna-size 22` y la interfaz también, pero **la regla
terminal sigue mirando las mismas posiciones absolutas** (19 y 2), que en una ventana de 22 nt
no son el mismo lugar relativo. Hoy el port las toma como `size - 3` y `1`, que es lo que hace
el original, pero nadie verificó que eso sea lo que corresponde a 22 nt.

## 7. Las tablas de desapareamiento son de ADN dentro de un cálculo de ARN

`free_energy.py:278-279` usa `RNA_NN3` y `RNA_DE2` para apilamientos y extremos colgantes —ARN,
correcto— pero `DNA_IMM1` y `DNA_TMM1` para los desajustes internos y terminales, que son de
ADN/ADN. Consecuencia concreta: un par G-U no se trata como wobble de ARN.

**No las sustituimos**, y la razón es metodológica: hace falta una tabla de desajustes de ARN
publicada y verificada, y no la tenemos de una fuente que hayamos abierto. Lo que hicimos es
instrumentar: contamos cada consulta a una tabla de desajustes. **En los cuatro casos corridos
dio cero** `[M]`. Así que la mezcla existe, está mal, y **no afecta a este uso**. Afectaría si
el cálculo se extendiera a secuencias desapareadas.

## 8. Bowtie de 64 bits

El `bowtie.exe` 0.11.3 que trae el instalador es de 32 bits y **aborta con `-v 1` en bases de
más de ~114 MB** `[M]`: no termina ni en el transcriptoma del maíz ni en el genoma del vector.
Con `-v 0` corre bien en las once bases que probamos. Un Bowtie 1.3.x de 64 bits resuelve el
caso, y es la pieza que falta para reproducir la regla de conteo del original sobre las bases
grandes.

## 9. Conservación entre poblaciones del vector

Un blanco que funciona en la población medida y no en la de al lado no sirve. El repositorio ya
tiene el cálculo de conservación por ventana (`tools/sifi21_port/conservacion.py`), pero no
está integrado a la interfaz: hoy el perfil mira eficiencia y riesgo, no estabilidad del blanco.
Es la tercera columna que falta, y es barata porque el cálculo ya existe.

---

## Preguntas que no son mejoras

1. **La licencia.** El artículo dice CC BY-SA 4.0 y SourceForge dice CC BY-NC 2.0 `[?]`. ¿Cuál
   rige? Mientras no se sepa, nuestra carpeta no lleva archivo de licencia y el nombre queda en
   suspenso.
2. **Contra qué base corriste el modo diseño.** Con una base distinta el mismo criterio da otro
   número, porque la columna «Efficient siRNA hits» cuenta un registro por acierto de Bowtie y
   no una ventana: contra un transcriptoma con parálogos e isoformas el conteo sube sin que
   cambie un solo parámetro `[H]`.
3. **Qué versión de RNAplfold.** La 2.1.5 que instala si-Fi y la 2.7.2 de las ligaduras de
   Python **no dan lo mismo**: difieren en 9 eficientes sobre 1.243 ventanas en `MP_MRFV` `[M]`.
   Cualquier comparación de conteos tiene que decir cuál corrió.
4. **Si querés correrlo en tu máquina.** Hoy está documentado pero no empaquetado. Si lo vas a
   usar, el empaquetado para Windows es una tarea aparte y la hacemos.
