"""La funcion historica de conteo de siRNAs eficientes, reimplementada.

Que resuelve. La planilla de EPILAB declara 114, 35, 199 y 33 siRNAs eficientes para
`MP_MRFV`, `CP_MRFV`, `BicC_Dm` y `ATPaseD_Dm`, y cualquier corrida del criterio sobre esas
mismas secuencias da mas: 138, 40, 218 y 35 con `sifi21INTA` por defecto. La carta del
investigador del 2026-10-25 explica la diferencia y no es termodinamica `[R]`:

  - la curva de eficiencia se construye asignando **20 posiciones de cobertura** a cada
    ventana de 21 nt;
  - el contador identifica siRNAs nuevos a partir de los **incrementos positivos** de esa
    curva.

La consecuencia es que, cuando una ventana eficiente termina y otra empieza en la misma
posicion de la curva, los dos efectos se compensan y el contador no registra la segunda.
Con ventanas que arrancan de a 1 nt y un ancho de cobertura de 20, eso pasa exactamente
cuando la ventana de `p` y la de `p - 20` son las dos eficientes.

Este modulo no decide si la regla es correcta: la implementa para poder medir cuanto
esconde. La lectura de los numeros esta en el `REPORT.md` de esta linea.

Unidades. Las posiciones son arranques de ventana, 1-based, como en los TSV del port. El
ancho de cobertura es un parametro **separado** del tamano del siRNA, justamente porque el
hallazgo de la carta es que no son el mismo numero: el siRNA mide 21 y la cobertura 20.

Uso (desde la raiz del repositorio):

    python research/ola5/N1_regla_de_conteo/scripts/conteo_por_curva.py <tsv> [...]
    python research/ola5/N1_regla_de_conteo/scripts/conteo_por_curva.py <tsv> --ancho 21

Cada TSV es una salida por ventana del port (`run_sifi.py --salida`), con las columnas
`pos` e `is_efficient`.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

#: Ancho de cobertura de la curva historica: 20 posiciones por ventana de 21 nt `[R]`.
ANCHO_HISTORICO = 20

#: Lo que declara la planilla de EPILAB para el metodo `siFi21_8_1.0_0.1_1111` `[R]`.
PLANILLA = {"MP_MRFV": 114, "CP_MRFV": 35, "BicC_Dm": 199, "ATPaseD_Dm": 33}


def curva_de_cobertura(posiciones, largo: int, ancho: int = ANCHO_HISTORICO) -> list[int]:
    """Cuantas ventanas eficientes cubren cada posicion 1..largo.

    Una ventana que arranca en `p` cubre `p .. p + ancho - 1`. Se acumula por diferencias,
    igual que `sifi_plus.perfil.solapamiento`, para no pagar `ancho` operaciones por
    ventana. La curva se recorta en `largo`: es la que se dibuja.
    """
    if ancho < 1:
        raise ValueError("el ancho de cobertura tiene que ser >= 1")
    delta = [0] * (largo + 2)
    for p in posiciones:
        ini, fin = max(1, p), min(largo, p + ancho - 1)
        if ini > fin:
            continue
        delta[ini] += 1
        delta[fin + 1] -= 1
    out, acc = [], 0
    for x in range(1, largo + 1):
        acc += delta[x]
        out.append(acc)
    return out


def contar_por_incrementos(posiciones, ancho: int = ANCHO_HISTORICO) -> int:
    """La suma de los incrementos positivos de la curva de cobertura.

    Es la cuenta de la funcion historica. No hace falta construir la curva: con arranques
    de a 1 nt el incremento en `p` vale +1 exactamente cuando la ventana de `p` es
    eficiente y la de `p - ancho` no, y vale 0 o -1 en todo otro caso. Se implementa asi
    para que el resultado no dependa de donde se recorta la curva, y
    `test_conteo_por_curva.py` verifica que las dos formas coinciden.
    """
    s = set(posiciones)
    return sum(1 for p in s if p - ancho not in s)


def tapadas(posiciones, ancho: int = ANCHO_HISTORICO) -> list[int]:
    """Los arranques eficientes que la curva no registra, en orden."""
    s = set(posiciones)
    return sorted(p for p in s if p - ancho in s)


def suma_de_incrementos_positivos(curva: list[int]) -> int:
    """La misma cuenta, leida de la curva ya construida. Para la verificacion cruzada."""
    anterior, total = 0, 0
    for v in curva:
        if v > anterior:
            total += v - anterior
        anterior = v
    return total


def tramos(curva: list[int]) -> list[tuple[int, int, int]]:
    """Los tramos no nulos de la curva, como (inicio, fin, altura maxima), 1-based.

    Es la descomposicion con la que se verifico el «RNAi design plot» del original
    (`sifi_plus/test_api.py`), y sirve de invariante: el conteo por incrementos nunca
    puede ser menor que la cantidad de tramos.
    """
    out, ini = [], None
    for i, v in enumerate(curva, start=1):
        if v > 0 and ini is None:
            ini = i
        elif v == 0 and ini is not None:
            out.append((ini, i - 1, max(curva[ini - 1:i - 1])))
            ini = None
    if ini is not None:
        out.append((ini, len(curva), max(curva[ini - 1:])))
    return out


def leer_tsv(ruta: Path) -> tuple[list[int], int]:
    """Devuelve (arranques eficientes, cantidad de ventanas) de un TSV del port."""
    with open(ruta, newline="", encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh, delimiter="\t"))
    if not filas or "pos" not in filas[0] or "is_efficient" not in filas[0]:
        raise SystemExit("%s no parece una salida por ventana del port" % ruta)
    efic = [int(f["pos"]) for f in filas if f["is_efficient"] == "True"]
    return efic, len(filas)


def medir(nombre: str, efic: list[int], ventanas: int,
          anchos=(19, ANCHO_HISTORICO, 21)) -> dict:
    """La fila de un gen: eficientes, conteo por cada ancho, tapadas y sesgo."""
    fila = {
        "nombre": nombre,
        "ventanas": ventanas,
        "eficientes": len(efic),
        "conteo": {str(a): contar_por_incrementos(efic, a) for a in anchos},
        "tapadas": len(tapadas(efic, ANCHO_HISTORICO)),
        "arranques_tapados": tapadas(efic, ANCHO_HISTORICO),
    }
    fila["sesgo_relativo"] = (
        round(fila["tapadas"] / fila["eficientes"], 4) if fila["eficientes"] else 0.0)
    gen = nombre.split("_full")[0]
    if gen in PLANILLA:
        fila["planilla"] = PLANILLA[gen]
        fila["reproduce_planilla"] = fila["conteo"][str(ANCHO_HISTORICO)] == PLANILLA[gen]
    return fila


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tsv", nargs="+", help="salidas por ventana del port")
    ap.add_argument("--ancho", type=int, default=None,
                    help="un solo ancho de cobertura, en vez de 19, 20 y 21")
    ap.add_argument("--json", default=None, help="archivo donde volcar las filas")
    a = ap.parse_args(argv)

    anchos = (a.ancho,) if a.ancho else (19, ANCHO_HISTORICO, 21)
    filas = []
    for ruta in a.tsv:
        efic, ventanas = leer_tsv(Path(ruta))
        filas.append(medir(Path(ruta).name.split("_fiel")[0], efic, ventanas, anchos))

    cab = ["gen", "ventanas", "eficientes"] + ["a=%d" % x for x in anchos] + ["planilla"]
    print("\t".join(cab))
    for f in filas:
        print("\t".join([f["nombre"], str(f["ventanas"]), str(f["eficientes"])]
                        + [str(f["conteo"][str(x)]) for x in anchos]
                        + [str(f.get("planilla", "-"))]))

    if a.json:
        Path(a.json).write_text(json.dumps(filas, indent=2, ensure_ascii=False),
                                encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
