"""Marca las ventanas de baja complejidad, que inflan el conteo de off-targets.

Por que existe este modulo. Corriendo el tamizaje del genoma publico del MRFV
(`NC_002786.2`) contra el transcriptoma de *Harmonia axyridis* aparecieron nueve ventanas con
coincidencia perfecta de 21/21 nt. Nueve coincidencias exactas de un 21-mero son unas trece
ordenes de magnitud mas de lo que da el azar, asi que o es biologia o es un artefacto.
Mirandolas, las nueve son las posiciones 6338-6346: **la cola de poli-A del genoma viral**.
Todo transcriptoma tiene poli-A, asi que esa coincidencia no dice nada sobre el riesgo de un
ARNdc: dice que los dos extremos son poli-A. `[M]`

El si-Fi21 original tiene exactamente el mismo agujero y no lo marca: corre `bowtie -a -v N -y`
y suma aciertos, ciego a la complejidad igual que a la posicion del desajuste. Un conteo de
off-targets que mete la cola de poli-A en la misma bolsa que una homologia real no se puede
usar para decidir nada.

Lo que hacemos: no se descartan las ventanas —descartar en silencio es el otro error— se
**marcan**, y los conteos se informan en dos cifras: el total y cuanto de ese total es de baja
complejidad. Quien lee decide.

El criterio es nuestro `[H]` y esta declarado aca para que se pueda discutir:

    baja complejidad  =  la racha de un mismo nucleotido mide 10 nt o mas
                      o  en la ventana aparecen 2 nucleotidos distintos o menos

Es deliberadamente grosero y transparente, no un puntaje con umbral ajustado. Las dos
condiciones se eligieron porque atrapan el caso real —colas de poli-A y repeticiones simples—
sin tocar nada con composicion normal: en los 6.346 21-meros de `NC_002786.2`, marca 9.

Pendiente declarado: el repositorio ya tiene una corrida de `dustmasker` sobre los genes en
`research/ola2/W5_secuencias_epilab/analisis/dustmasker_full.txt`. Contrastar este criterio
contra esa salida es el paso que falta para reemplazarlo por el estandar en vez de por uno
propio; no se hizo todavia y por eso la marca va con `[H]` y no con `[E]`.
"""

from __future__ import annotations

HOMOPOLIMERO_MAX = 10   # nt de racha de un mismo nucleotido
BASES_MIN = 2           # cuantos nucleotidos distintos tiene que haber, como minimo, mas uno


def homopolimero(s: str) -> int:
    """El largo de la racha mas larga de un mismo nucleotido."""
    if not s:
        return 0
    mejor = actual = 1
    for i in range(1, len(s)):
        actual = actual + 1 if s[i] == s[i - 1] else 1
        if actual > mejor:
            mejor = actual
    return mejor


def bases_distintas(s: str) -> int:
    return len(set(s))


def es_baja(s: str) -> bool:
    """El criterio, en una linea, para que se pueda leer y discutir."""
    return homopolimero(s) >= HOMOPOLIMERO_MAX or bases_distintas(s) <= BASES_MIN


def ficha(s: str) -> dict:
    return {"homopolimero": homopolimero(s), "bases_distintas": bases_distintas(s),
            "baja_complejidad": es_baja(s)}


def marcar(ventanas) -> dict[int, dict]:
    """{posicion: ficha} para cada ventana."""
    return {w.pos: ficha(w.seq) for w in ventanas}


def posiciones_bajas(ventanas) -> set[int]:
    return {w.pos for w in ventanas if es_baja(w.seq)}
