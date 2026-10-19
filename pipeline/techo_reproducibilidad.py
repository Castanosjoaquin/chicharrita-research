"""Cuanto se parecen dos dsRNA distintos contra el MISMO gen?

Es la pregunta que pone el techo a todo lo demas. Si dos construcciones independientes
dirigidas al mismo gen dan resultados muy distintos, entonces ningun modelo que prediga
desde la secuencia puede superar ese ruido: estaria prediciendo algo que el propio ensayo
no reproduce.

El cribado de iBeetle da justo los datos para medirlo: cada construccion (iB_*) tiene su
letalidad medida, y varias construcciones distintas apuntan al mismo gen (TC*).

Lo que se mide:
  - correlacion de Spearman entre la letalidad de dos construcciones del mismo gen
  - concordancia binaria (las dos matan / las dos no matan) y kappa de Cohen
  - lo mismo entre construcciones de genes DISTINTOS, como control negativo

Uso:
    python3 techo_reproducibilidad.py
"""

from __future__ import annotations

import csv
import math
import random
from collections import defaultdict
from pathlib import Path

IBEETLE = Path.home() / "yhat" / "data" / "ibeetle"
UMBRAL_LETAL = 30.0  # % de letalidad a partir del cual se llama "letal"


def cargar_letalidad(columna: str = "dali11", misma_fase: bool = False):
    """iB -> (letalidad, fase). El cribado trae tres medidas distintas; se prueban todas,
    porque una conclusion fuerte no puede depender de cual columna elegimos."""
    valores: dict[str, float] = {}
    fases: dict[str, str] = {}
    with (IBEETLE / "iBeetle_lethality.csv").open(encoding="utf-8-sig") as fh:
        for fila in csv.DictReader(fh, delimiter=";"):
            ib = (fila.get("iB") or "").strip()
            try:
                valores[ib] = float((fila.get(columna) or "").strip())
            except ValueError:
                continue
            fases[ib] = (fila.get("phase") or "").strip()
    return (valores, fases) if misma_fase else valores


def cargar_ib_a_gen() -> dict[str, str]:
    mapa: dict[str, str] = {}
    with (IBEETLE / "iB_TC.csv").open(encoding="utf-8-sig") as fh:
        for fila in fh:
            if fila.startswith("#") or "," not in fila:
                continue
            ib, gen = fila.strip().split(",")[:2]
            mapa[ib.strip()] = gen.strip()
    return mapa


def spearman(xs: list[float], ys: list[float]) -> float:
    def rangos(v: list[float]) -> list[float]:
        orden = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(orden):
            j = i
            while j + 1 < len(orden) and v[orden[j + 1]] == v[orden[i]]:
                j += 1
            medio = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[orden[k]] = medio
            i = j + 1
        return r

    rx, ry = rangos(xs), rangos(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else float("nan")


def kappa(a: list[int], b: list[int]) -> tuple[float, float]:
    n = len(a)
    obs = sum(1 for x, y in zip(a, b) if x == y) / n
    pa1, pb1 = sum(a) / n, sum(b) / n
    esp = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    return obs, (obs - esp) / (1 - esp) if esp < 1 else float("nan")


def robustez(ib_a_gen: dict[str, str]) -> None:
    """Repite la medicion con las tres columnas del cribado, y restringiendo a misma fase."""
    print(f"\n{'medida':<24}{'genes':>8}{'Spearman':>11}{'acuerdo':>10}{'kappa':>9}{'control':>10}")
    for columna in ("dali11", "dali22", "dapi11"):
        for solo_fase in (False, True):
            valores, fases = cargar_letalidad(columna, misma_fase=True)
            por_gen: dict[str, list[tuple[str, float]]] = defaultdict(list)
            for ib, v in valores.items():
                gen = ib_a_gen.get(ib)
                if gen:
                    por_gen[gen].append((ib, v))
            rnd = random.Random(0)
            xs, ys = [], []
            for valores_gen in por_gen.values():
                if solo_fase:
                    valores_gen = [p for p in valores_gen if fases.get(p[0])]
                    agrupado: dict[str, list] = defaultdict(list)
                    for ib, v in valores_gen:
                        agrupado[fases[ib]].append((ib, v))
                    valores_gen = next((v for v in agrupado.values() if len(v) >= 2), [])
                if len(valores_gen) < 2:
                    continue
                a, b = rnd.sample(valores_gen, 2)
                xs.append(a[1])
                ys.append(b[1])
            if len(xs) < 30:
                print(f"{columna + (' misma fase' if solo_fase else ''):<24}{len(xs):>8}   pocos pares")
                continue
            rho = spearman(xs, ys)
            ba = [int(v >= UMBRAL_LETAL) for v in xs]
            bb = [int(v >= UMBRAL_LETAL) for v in ys]
            ac, k = kappa(ba, bb)
            mez = ys[:]
            rnd.shuffle(mez)
            etiqueta = columna + (" misma fase" if solo_fase else "")
            print(f"{etiqueta:<24}{len(xs):>8}{rho:>11.3f}{ac*100:>9.1f}%{k:>9.3f}"
                  f"{spearman(xs, mez):>10.3f}")


def main() -> None:
    letalidad = cargar_letalidad()
    ib_a_gen = cargar_ib_a_gen()
    print(f"construcciones con letalidad medida: {len(letalidad)}")
    print(f"construcciones con gen asignado    : {len(ib_a_gen)}")

    por_gen: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for ib, valor in letalidad.items():
        gen = ib_a_gen.get(ib)
        if gen:
            por_gen[gen].append((ib, valor))

    repetidos = {g: v for g, v in por_gen.items() if len(v) >= 2}
    print(f"genes con 2 o mas construcciones independientes: {len(repetidos)}")
    if not repetidos:
        return

    rnd = random.Random(0)
    xs, ys = [], []
    for valores in repetidos.values():
        a, b = rnd.sample(valores, 2)
        xs.append(a[1])
        ys.append(b[1])

    rho = spearman(xs, ys)
    ba = [int(v >= UMBRAL_LETAL) for v in xs]
    bb = [int(v >= UMBRAL_LETAL) for v in ys]
    acuerdo, k = kappa(ba, bb)

    # control negativo: parejas de genes DISTINTOS
    mezclado = ys[:]
    rnd.shuffle(mezclado)
    rho_ctrl = spearman(xs, mezclado)
    acuerdo_ctrl, k_ctrl = kappa(ba, [int(v >= UMBRAL_LETAL) for v in mezclado])

    print(f"\nPares comparados: {len(xs)} genes, dos construcciones independientes cada uno")
    print(f"{'':<36}{'mismo gen':>12}{'genes distintos':>18}")
    print(f"{'Spearman de la letalidad':<36}{rho:>12.3f}{rho_ctrl:>18.3f}")
    print(f"{'acuerdo binario (letal si >=30 %)':<36}{acuerdo*100:>11.1f}%{acuerdo_ctrl*100:>17.1f}%")
    print(f"{'kappa de Cohen':<36}{k:>12.3f}{k_ctrl:>18.3f}")

    print(f"\nDistribucion de la letalidad medida (n={len(letalidad)}):")
    vals = sorted(letalidad.values())
    for etiqueta, v in [("minimo", vals[0]), ("p25", vals[len(vals)//4]),
                        ("mediana", vals[len(vals)//2]), ("p75", vals[3*len(vals)//4]),
                        ("maximo", vals[-1])]:
        print(f"  {etiqueta:<10}{v:>8.1f}")
    print(f"  construcciones llamadas letales (>= {UMBRAL_LETAL:.0f} %): "
          f"{sum(1 for v in vals if v >= UMBRAL_LETAL)} ({sum(1 for v in vals if v >= UMBRAL_LETAL)/len(vals)*100:.1f} %)")

    robustez(ib_a_gen)

    print(f"\nLECTURA: {rho:.3f} de Spearman entre dos dsRNA contra el mismo gen es el TECHO.")
    print("Ningun modelo que prediga desde la secuencia puede superar de forma consistente")
    print("el ruido del ensayo que genera sus propias etiquetas.")


if __name__ == "__main__":
    main()
