"""Demostracion de los dos mecanismos de la regla de conteo, con secuencias de juguete.

Por que existe. La matriz de bases reales no se puede correr en toda maquina: necesita
`work/`, Bowtie y el TSV por ventana del port sobre las secuencias de EPILAB. Este
script no la reemplaza. Lo que hace es mostrar, con una secuencia al azar de semilla
fija y tres referencias construidas a mano, que la regla del original mueve el conteo
en los dos sentidos y por que:

  - contra la referencia que es el gen mismo, el conteo por acierto en `+` coincide
    con el conteo por ventana;
  - contra un isolado con **una** sustitucion, las ventanas que cubren esa posicion
    dejan de pegar con `-v 0` y el conteo **baja**;
  - contra una referencia que **repite** un tramo del gen, las ventanas de ese tramo
    pegan dos veces y el conteo **sube**.

Esos son exactamente los dos signos que hacen falta para explicar la forma del
desajuste de la planilla, que baja en tres genes y sube en uno. Aca estan demostrados
sobre secuencias inventadas: es una demostracion del mecanismo, no una medicion del
caso real.

Uso:
    python demo_sintetico.py --salida ../resultados/ejemplo_formato_sintetico.md
"""

from __future__ import annotations

import argparse
import random
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import conteo_por_acierto as cpa

SEMILLA = 7
LARGO = 60
K = 21
# Una de cada cuatro ventanas se declara eficiente. El criterio de eficiencia real lo
# calcula el port; aca no se simula, porque la regla de conteo no lo mira.
CADA = 4
SUSTITUCION = 30  # 1-based, en el medio del gen


def construir(d: Path) -> tuple[Path, dict[str, Path]]:
    random.seed(SEMILLA)
    gen = "".join(random.choice("ACGT") for _ in range(LARGO))

    filas = ["pos\tseq\tis_efficient"]
    for i in range(len(gen) - K + 1):
        pos = i + 1
        filas.append(f"{pos}\t{gen[i:i + K]}\t{pos % CADA == 1}")
    tsv = d / "gen.tsv"
    tsv.write_text("\n".join(filas) + "\n", encoding="utf-8")

    i = SUSTITUCION - 1
    variante = gen[:i] + ("A" if gen[i] != "A" else "C") + gen[i + 1:]

    bases = {
        "identidad": (">gen_full\n" + gen + "\n"),
        "isolado_variante": (">isolado_X\n" + variante + "\n"),
        "con_repeticion": (">ref_repetida\n" + gen + "NNNNN" + gen[:25] + "\n"),
    }
    rutas = {}
    for nombre, texto in bases.items():
        ruta = d / f"{nombre}.fasta"
        ruta.write_text(texto, encoding="utf-8")
        rutas[nombre] = ruta
    return tsv, rutas


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida", required=True, help="markdown de salida")
    a = ap.parse_args(argv)

    with tempfile.TemporaryDirectory() as d:
        tsv, bases = construir(Path(d))
        # El declarado de juguete es el conteo por ventana: la celda de identidad lo
        # reproduce y las otras dos muestran cuanto se alejan, en cada sentido.
        argumentos = ["contar", "--gen", f"gen={tsv}"]
        for nombre, ruta in bases.items():
            argumentos += ["--base", f"{nombre}={ruta}"]
        argumentos += ["--declarado", "gen=10", "--exigir-identidad", "identidad",
                       "--md", str(Path(a.salida))]
        codigo = cpa.main(argumentos)

    salida = Path(a.salida)
    cabecera = (
        "# Formato de salida de `conteo_por_acierto.py`, sobre secuencias de juguete\n\n"
        "**Esto no es una medicion del caso real.** Lo genera "
        "`scripts/demo_sintetico.py` con una secuencia al azar de semilla fija "
        f"({SEMILLA}) de {LARGO} nt y tres referencias construidas a mano, y sirve "
        "para dos cosas: fijar el formato de la tabla que va a llenar la matriz de "
        "bases reales, y mostrar que la regla del original mueve el conteo en los dos "
        "sentidos. La celda `identidad` reproduce el conteo por ventana; "
        "`isolado_variante` lo baja, porque una sola sustitucion saca de la tabla a "
        "las ventanas que la cubren; `con_repeticion` lo sube, porque las ventanas del "
        "tramo repetido cuentan dos veces. `[M]` con insumos sinteticos.\n\n"
        "Regenerar: `python scripts/demo_sintetico.py --salida "
        "resultados/ejemplo_formato_sintetico.md`\n\n---\n\n")
    salida.write_text(cabecera + salida.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"-> {salida}")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
