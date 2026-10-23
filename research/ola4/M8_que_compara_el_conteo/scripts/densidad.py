"""Normaliza por largo los conteos de ventanas eficientes ya medidos.

No corre el motor de eficiencia ni ningun alineador: toma los conteos que ya
estan medidos y publicados en el repositorio, los divide por la cantidad de
ventanas de cada gen y escribe la tabla con los dos ordenes, el del conteo crudo
y el de la densidad. Es la cuenta que sostiene el primero de los cuatro limites
del informe de M8.

Procedencia de cada numero, para que la tabla sea auditable sin salir del repo:

- Largos de las cuatro secuencias de EPILAB: `research/ola2/W5_secuencias_epilab/
  REPORT.md` (tabla de la seccion de datos) y `research/ola2/MANIFEST.md`.
- `original_2.1.5`: el programa original con sus valores por defecto, que nuestro
  port reproduce exacto en modo fiel con RNAplfold 2.1.5
  (`research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md` §0).
- `fiel_vienna_2.7.2`: el mismo port, el mismo modo, el backend `vienna` con
  ViennaRNA 2.7.2 (`research/ola3/C2_codigo_apolo_inta/corridas/README.md`, que
  tambien registra que `sifi21INTA` da esos mismos cuatro numeros).
- `corregido_vienna`: modo corregido, que es el ancla que `ranking_v2.py` exige
  antes de medir (`research/ola3/C7_ranking_v2/REPORT.md` §1).
- `planilla_epilab`: la columna de eficientes declarada en `Sequences_EPILAB.xlsx`,
  que ninguna configuracion nuestra reproduce (W5 §1 y la linea M1 de la ola 4).

Uso:
    python densidad.py            # escribe ../resultados/densidad.tsv
    python densidad.py --stdout   # lo escribe por salida estandar
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

TAMANO_SIRNA = 21

# Largo de la secuencia completa, en nucleotidos.
LARGOS = {
    "MP_MRFV": 1263,
    "CP_MRFV": 528,
    "BicC_Dm": 2520,
    "ATPaseD_Dm": 491,
}

# Ventanas eficientes sobre la secuencia completa, por configuracion.
CONTEOS = {
    "original_2.1.5": {
        "MP_MRFV": 133,
        "CP_MRFV": 32,
        "BicC_Dm": 212,
        "ATPaseD_Dm": 42,
    },
    "fiel_vienna_2.7.2": {
        "MP_MRFV": 142,
        "CP_MRFV": 39,
        "BicC_Dm": 223,
        "ATPaseD_Dm": 35,
    },
    "corregido_vienna": {
        "MP_MRFV": 123,
        "CP_MRFV": 30,
        "BicC_Dm": 171,
        "ATPaseD_Dm": 29,
    },
    "planilla_epilab": {
        "MP_MRFV": 114,
        "CP_MRFV": 35,
        "BicC_Dm": 199,
        "ATPaseD_Dm": 33,
    },
}


def ventanas(largo: int, tamano: int = TAMANO_SIRNA) -> int:
    """Ventanas de `tamano` nt que caben en una secuencia de `largo` nt."""
    return largo - tamano + 1


def densidad(eficientes: int, ventanas_totales: int) -> float:
    """Eficientes por cada 100 ventanas."""
    return 100.0 * eficientes / ventanas_totales


def orden_por_conteo(conteos: dict[str, int]) -> list[str]:
    return sorted(conteos, key=lambda gen: (-conteos[gen], gen))


def orden_por_densidad(conteos: dict[str, int]) -> list[str]:
    def clave(gen: str) -> tuple[float, str]:
        return (-densidad(conteos[gen], ventanas(LARGOS[gen])), gen)

    return sorted(conteos, key=clave)


def tabla() -> list[list[str]]:
    filas = [
        [
            "configuracion",
            "gen",
            "largo_nt",
            "ventanas",
            "eficientes",
            "densidad_por_100_ventanas",
            "puesto_por_conteo",
            "puesto_por_densidad",
        ]
    ]
    for nombre, conteos in CONTEOS.items():
        por_conteo = orden_por_conteo(conteos)
        por_densidad = orden_por_densidad(conteos)
        for gen in por_conteo:
            totales = ventanas(LARGOS[gen])
            filas.append(
                [
                    nombre,
                    gen,
                    str(LARGOS[gen]),
                    str(totales),
                    str(conteos[gen]),
                    f"{densidad(conteos[gen], totales):.2f}",
                    str(por_conteo.index(gen) + 1),
                    str(por_densidad.index(gen) + 1),
                ]
            )
    return filas


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="escribir la tabla por salida estandar en vez del archivo",
    )
    args = parser.parse_args(argv)

    texto = "\n".join("\t".join(fila) for fila in tabla()) + "\n"
    if args.stdout:
        sys.stdout.write(texto)
        return 0

    salida = Path(__file__).resolve().parent.parent / "resultados" / "densidad.tsv"
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(texto, encoding="utf-8")
    print(f"escrito {salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
