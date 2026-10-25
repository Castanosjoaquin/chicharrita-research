# N1 — La función histórica de conteo, reproducida con insumos propios

**Ola 5, línea N1.** Fecha: 2026-10-25. Contesta los puntos 1 y 2 de la carta del investigador
del 25 de octubre de 2026, que resuelve la discrepancia de los cuatro conteos y declara una
limitación de la función histórica que van a revisar internamente. Reproducible con los tres
scripts de [`scripts/`](scripts/); los números salen de [`resultados/`](resultados/). Marcadores
de `CLAUDE.md`.

## El resultado, en un párrafo

**La explicación del investigador es correcta y la pudimos verificar sin pedirle un archivo.** Lo
que dice su carta es que la curva de eficiencia se construye asignando 20 posiciones de cobertura
a cada ventana de 21 nt y que el contador identifica siRNAs nuevos a partir de los incrementos
positivos de esa curva, de modo que cuando una ventana eficiente termina donde otra empieza los
dos efectos se compensan y la segunda no se registra `[R]`. Implementada esa regla y aplicada a
las ventanas eficientes de nuestro propio port con la configuración que reconstruye las curvas
—modo `fiel`, ViennaRNA 2.7.2, tabla `RNA_NN4`—, los cuatro conteos de 138, 40, 218 y 35 pasan a
**114, 35, 199 y 33**, que son los cuatro valores de la planilla, exactos `[M]`. Y el ancho de
cobertura queda identificado: con 19 y con 21 no se reproducen los cuatro `[M]`. Nada de esto
necesitó la clasificación por ventana que habíamos pedido como pedido 1 de la reunión, así que
ese pedido **se cae**.

> **Lo que se deduce** `[H]`. (1) El umbral de estabilidad de extremos no era la causa, y la
> coincidencia de 1,75 con algunos valores de la planilla era circunstancial, como dice la carta.
> (2) Nuestra hipótesis del conteo por acierto de Bowtie no era la causa de estos cuatro números;
> sigue siendo un hallazgo sobre la herramienta original y se conserva como tal
> ([`CAMINOS_PROBADOS.md`](../../../00_meta/CAMINOS_PROBADOS.md)). (3) El sesgo que introduce la
> función de conteo **no es constante entre genes**, y eso vuelve incomparables entre sí las
> cifras de la planilla. (4) Si las curvas históricas reconstruyen 138/40/218/35, el método
> `siFi21_8_1.0_0.1_1111` corre con la tabla de Zuber y un motor equivalente a las ligaduras de
> ViennaRNA, y no con el si-Fi21 original: eso cambia cuál es la línea base para comparar contra
> la planilla y hay que preguntárselo.

## 1. De dónde parte la cuenta

El conjunto de ventanas sobre el que se aplica la regla no es cualquiera, y conviene decir por
qué es ése. La carta dice que las curvas almacenadas permiten reconstruir 138, 40, 218 y 35
ventanas eficientes `[R]`. Esos cuatro valores son exactamente los que la corrida 1 de la ola 3
obtuvo con `sifi21INTA` en sus valores por defecto
(`research/ola3/C2_codigo_apolo_inta/corridas/README.md`) `[M]`, y el driver de esta línea los
vuelve a obtener desde el port con `--tabla-nn NN4 --modo fiel --backend vienna`: el script
**aborta** si alguno de los cuatro no da, porque un conteo por incrementos sobre otro conjunto de
ventanas no se puede leer.

El si-Fi21 original con su propio RNAplfold da 133, 32, 212 y 42, que es otro punto de partida.
La regla se mide sobre el conjunto del que salieron las curvas, no sobre otro.

## 2. La regla, tal como quedó implementada

Con arranques de a 1 nt, el incremento de la curva en la posición `p` vale +1 exactamente cuando
la ventana de `p` es eficiente y la de `p − ancho` no lo es, y vale 0 o −1 en todo otro caso. Así
que el conteo es

> la cantidad de arranques eficientes `p` tales que `p − 20` **no** es un arranque eficiente,

y una ventana eficiente queda invisible cuando la de veinte posiciones antes también lo es. El
módulo implementa las dos formas —la cuenta por conjunto y la suma de los incrementos positivos
de la curva construida— y el test verifica que coinciden, para que el resultado no dependa de
dónde se recorta la curva.

Hay un caso que conviene decir porque es contraintuitivo y lo aprendimos equivocándonos al
escribir el test: **un bloque de ventanas eficientes contiguas no pierde nada**. Como las
ventanas se desplazan de a 1 nt, cada arranque de un bloque contiguo sube la curva en 1 y se
cuenta. Lo que la función pierde no es la contigüidad: es la distancia de exactamente veinte.

## 3. Los cuatro conteos

`[M]` Punto por defecto, modo `fiel`, ViennaRNA 2.7.2, tabla `RNA_NN4`, 22 °C.
Fuente: `resultados/conteo_por_curva.tsv`.

| Gen | Ventanas | Eficientes | Tapadas | `a=19` | **`a=20`** | `a=21` | Planilla | Sesgo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `MP_MRFV` | 1.243 | 138 | 24 | 120 | **114** | 115 | 114 | 17,4 % |
| `CP_MRFV` | 508 | 40 | 5 | 35 | **35** | 36 | 35 | 12,5 % |
| `BicC_Dm` | 2.500 | 218 | 19 | 196 | **199** | 197 | 199 | 8,7 % |
| `ATPaseD_Dm` | 471 | 35 | 2 | 35 | **33** | 33 | 33 | 5,7 % |

`[M]` **El ancho está identificado.** El ancho 19 acierta `CP_MRFV` y falla los otros tres; el 21
acierta `ATPaseD_Dm` y falla los otros tres. Sólo el 20 acierta los cuatro. No es una regla
ajustada a un número: son cuatro ecuaciones y un parámetro entero.

`[M]` **El sesgo no es una constante.** Va del 5,7 % en `ATPaseD_Dm` al 17,4 % en `MP_MRFV`, y no
sigue ni el largo del gen —`BicC_Dm` es cinco veces más largo que `CP_MRFV` y pierde una fracción
menor— ni la cantidad de eficientes. Lo que lo fija es cuán agrupadas están las ventanas
eficientes: cada par a distancia veinte cuesta una unidad. `[H]` La consecuencia es la que importa
para leer la planilla: **dos cifras de la planilla perdieron fracciones distintas, así que no son
comparables entre sí**. Es un quinto límite para
[`M8`](../../ola4/M8_que_compara_el_conteo/REPORT.md), que había medido cuatro.

`[M]` Los arranques que la curva no registra están listados en `resultados/conteo_por_curva.json`
(`detalle.<gen>.tapados`): 24 en `MP_MRFV`, 5 en `CP_MRFV`, 19 en `BicC_Dm` y 2 en `ATPaseD_Dm`.
Son posiciones, no nucleótidos.

## 4. Las verificaciones

`[M]` `scripts/test_conteo_por_curva.py`: **17 verificaciones, todas en verde**, en tres grupos.
Los nueve sintéticos fijan el mecanismo sin depender de ningún dato —dos ventanas a distancia
veinte cuentan una, a diecinueve o veintiuno cuentan dos, un bloque contiguo cuenta todos sus
arranques y un bloque más largo que el ancho se corta en el ancho—. Los cuatro invariantes acotan
la función por arriba (nunca cuenta más ventanas de las que hay) y por abajo (nunca menos tramos
de los que tiene la curva), y verifican que la curva y el conjunto den el mismo número en los tres
anchos. Los cuatro del ancla real son los de la tabla de arriba, y se declaran **no corridos** si
falta `work/sifi_check/`, que no está en git.

## 5. Lo que esto no dice

`[H]` No dice que la función histórica esté mal: dice qué esconde. El investigador ya la declaró
como una limitación a revisar, y la cuenta de arriba da el tamaño de la revisión, gen por gen.

`[?]` No dice con qué tabla termodinámica corre el método histórico. Que las curvas reconstruyan
exactamente los valores de `sifi21INTA` por defecto es compatible con la tabla de Zuber, pero
también con otro motor que dé los mismos cuatro números. Es la pregunta de
`PREGUNTAS_ABIERTAS.md` y la contesta él, no una corrida nuestra.

`[?]` No dice si el mismo contador produjo las cifras de las doce regiones candidatas de la
planilla o sólo las de los cuatro genes completos. Si fue el mismo, las comparaciones entre
regiones de la planilla arrastran el mismo sesgo desparejo.

`[M]` Confidencialidad: el motor corre local, ninguna secuencia salió de la máquina, y los TSV por
ventana —que tienen una columna de 21-meros solapados y reconstruyen el gen— se escriben fuera del
repositorio por construcción del driver (`--trabajo`).

## Archivos

| Archivo | Qué es |
|---|---|
| `scripts/conteo_por_curva.py` | la curva, el conteo por incrementos, las tapadas y los tramos, más la CLI que lee TSV del port |
| `scripts/correr_n1.py` | driver: del FASTA al conteo, con las anclas y la procedencia |
| `scripts/test_conteo_por_curva.py` | las 17 verificaciones |
| `resultados/conteo_por_curva.tsv` | la tabla de la sección 3 |
| `resultados/conteo_por_curva.json` | lo mismo con los arranques eficientes y los tapados |
| `resultados/procedencia.json` | versiones, configuración y md5 de los cuatro FASTA |
