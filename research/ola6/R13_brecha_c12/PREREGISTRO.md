# De dónde sale la brecha entre `C12` y el par completo — preregistro

**Escrito antes de calcular nada.** Pregunta abierta **62**, abierta por `D86` al cerrar `F1`
(issue #25). Commiteado antes de la primera corrida; lo que cambie después va como enmienda
fechada al final, nunca editando lo de arriba.

## La pregunta

`C12` (Validación A) publicó que la concordancia de nombre entre ortólogos recíprocos de
*M. quadrilineatus* y *H. vitripennis* es **78,2 %** sobre 1.152 pares, y ésa es la tabla de bandas
que `F1` usa para rotular cada anotación que transfiere. Al validar el supuesto de esas bandas,
`D86` corrió el **mismo par de proteomas completo** y obtuvo **85,1 %** sobre 12.075 pares, con los
tres tramos altos entre 6 y 10 puntos por encima. Son 6,9 puntos de brecha en el total.

Hasta que se sepa de dónde sale, **las bandas publicadas de `C12` están en duda**, y las usa `F1` y
cualquier documento que cite el 78,2 %.

## Las tres causas candidatas

La entrada 62 listaba dos. Leer los scripts versionados de `C12` saca una tercera, que es la que
antes no estaba escrita:

1. **El normalizador de nombres.** El código original de `C12` **no quedó versionado**; `F1` lo
   reimplementó desde su descripción en prosa y lo declaró como desvío. Un normalizador más
   agresivo —que colapse más variantes de un mismo nombre— sube la concordancia sin que cambie
   ningún alineamiento.
2. **El protocolo.** `C12` interrumpió el `blastp` directo por lento y se quedó con las **primeras
   24.856 consultas por orden del archivo** (no una muestra aleatoria del proteoma), de ahí una
   submuestra aleatoria de 4.000 con semilla 0, y corrió el reverso sólo para los mejores hits de
   esas 4.000. `D86` corrió todo.
3. **El alineador.** `C12` usó BLAST+ 2.17.0; `D86` usó `diamond` 2.2.8. No dan la misma `pident`
   ni necesariamente los mismos hits.

## El diseño: descomponer la brecha en tres sumandos

Los alineamientos de `C12` **están en disco** (`work/C12/MQ_vs_HV.tsv`, 132.467 líneas, y
`work/C12/HVsub_vs_MQ.tsv`, 15.680; más `work/C12/muestra_mq.txt` con la submuestra exacta). Eso
permite aislar cada causa cambiando **una sola cosa por vez**, sin correr ningún alineamiento
nuevo.

- **Paso A — el normalizador, con todo lo demás de `C12` fijo.** Reconstruir los pares recíprocos
  desde los TSV de `C12`, con su protocolo y su alineador, y calcular la concordancia por banda
  usando el **normalizador de `F1`**.
- **Paso B — el protocolo, con el alineador y el normalizador fijos.** Sobre los alineamientos de
  `diamond` de `D86` (par completo), aplicar el **recorte de `C12`**: las mismas 4.000 consultas de
  `muestra_mq.txt`, y el reverso restringido a los mejores hits de esas 4.000.
- **Paso C — el alineador.** Con protocolo y normalizador fijos en los de `C12`/`F1`, la diferencia
  entre el paso A (BLAST+) y el paso B (`diamond`) es el efecto del alineador.

Los tres pasos usan el mismo código de normalización y de bandas, importado de
`research/ola6/F1_transferencia_homologia/scripts/transferir_anotacion.py`.

## El control que decide si el paso A sirve

El paso A es además la **réplica de `C12`**. Si el método descrito en su informe basta para
reconstruir lo que hizo, debe devolver del orden de **1.152 pares**:

- **Reproduce el número de pares y da ≈ 78,2 %** → el normalizador no explica la brecha, y la
  réplica es fiel: los pasos B y C quedan interpretables.
- **Reproduce el número de pares y da ≈ 85 %** → **el normalizador es la causa principal**, y las
  bandas de `C12` no están mal medidas sino mal comparadas.
- **No reproduce el número de pares** (fuera de ± 10 %) → el informe de `C12` no alcanza para
  reconstruir su análisis. Eso es un hallazgo sobre la reproducibilidad de `C12` y se reporta como
  tal; la descomposición se publica igual, declarando que su paso A no es la réplica sino una
  reconstrucción aproximada.

## Criterio de atribución, fijado ahora

Sobre la brecha del total (6,9 puntos), con cada paso aportando un sumando:

- Si **un** componente explica **≥ 2/3** de la brecha, se le atribuye y se dice cuál.
- Si ninguno llega a 2/3, se declara **multicausal** y se publican los tres pesos, sin elegir uno.
- Un sumando puede salir **negativo** (un componente que empuja en contra); se reporta con su signo
  y no se descarta.

## Qué se hace con `C12` según el resultado

Esto está decidido **antes** de ver el número, para no elegir después:

- Si la causa es el **normalizador**, las bandas de `C12` quedan **válidas para su propio
  normalizador** y lo que hay que corregir es la nota de `F1` que las usa con otro. No se toca la
  tabla de `C12`.
- Si la causa es el **protocolo** o el **alineador**, las bandas de `C12` quedan **sesgadas como
  estimación del par completo**, y eso se anota en su informe con la convención del repositorio
  —frase vieja tachada, nueva al lado— con un puntero a la medición del par completo. **No se
  recalcula ni se reemplaza la tabla de `C12`**: su corrida es lo que es, y reescribirla sería
  borrar el registro de lo que se publicó.

## Lo que este diseño NO hace

- **No corre ningún alineamiento nuevo.** Todo sale de archivos que ya están en disco, así que no
  se puede separar el efecto del alineador de cualquier otra diferencia entre las dos corridas que
  no esté en los TSV (parámetros, versión de la base, orden de las secuencias).
- **No reconstruye el normalizador de `C12`.** Su código no existe; el paso A mide qué pasa al
  aplicar el de `F1` a sus pares, no cuál era el suyo. Si la brecha se explica por ahí, sabremos
  **que** el normalizador importa, no **cuál** usaba.
- **No valida ninguna de las dos mediciones contra verdad experimental.** Las dos miden
  consistencia entre anotaciones de RefSeq, igual que antes.
- **No cambia nada de `F1`.** El 81 % de `F1` sigue publicado como cota conservadora por `D86`, y
  esta investigación no lo mueve en ninguna dirección.

## Salidas comprometidas

`resultados/descomposicion.json` (los tres sumandos con su signo, el control de réplica y el
veredicto según el criterio de arriba), `resultados/bandas_por_paso.tsv` (una fila por paso × banda,
con n, aciertos, concordancia e IC95 de Wilson) y `REPORT.md`. Ninguna salida lleva secuencia.

---

## Enmienda 1 — los tres pasos usan la misma regla de reciprocidad (2026-10-27)

**Escrita después de una primera corrida y antes de la que se publica.** Es una corrección de
método, no un cambio de criterio: el criterio de atribución y el control de réplica siguen siendo
los de arriba, sin tocar.

La primera implementación del **paso B** tomaba los pares ya clasificados de la validación de
`D86`, que aplican la **regla estricta de `F1`**: un empate en el primer puesto descalifica el par.
El **paso A**, en cambio, reconstruye los pares desde los TSV de `C12` con «el mejor hit del mejor
hit», sin tratamiento de empates, porque es lo que describe `C12`. Con eso, la diferencia A → B no
aislaba el alineador: lo confundía con la regla de empates, y se veía en el conteo —1.081 pares en
A contra 690 en B sobre las mismas 4.000 consultas—.

**Corrección:** los pasos B y C se recalculan leyendo los TSV crudos de `diamond`
(`work/F1v/trabajo/`) con la **misma función y la misma regla de reciprocidad** que el paso A. Así
entre A y B cambia únicamente el alineador, y entre B y C únicamente el recorte. El paso C deja de
tomarse del resumen de `D86` y se recalcula igual que los otros dos.

**Consecuencia sobre la comparación con `D86`:** al usar la regla sin empates, el total del paso C
no es el 85,1 % que `D86` publicó para la lectura inclusiva, y la brecha a descomponer se mide
contra el total del paso C, que es el homogéneo con `C12`. El número que `D86` publicó no cambia;
cambia cuál de sus lecturas es la comparable, y el informe lo dice.
