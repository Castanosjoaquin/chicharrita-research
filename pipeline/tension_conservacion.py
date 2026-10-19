"""Cuanto mas conservado el gen, mas riesgo de off-target? Lo medimos.

Lo vimos dos veces por separado y siempre como anecdota: la V-ATPase del insecto chocando con
la bomba de protones del maiz, y los doce finales siendo todos maquinaria basica. Si la relacion
es real y medible, deja de ser anecdota y pasa a ser una ley del problema:

  **lo que hace a un gen buen blanco (ser esencial, y por eso estar conservado) es lo mismo que
  lo hace peligroso (parecerse a genes de especies que no queremos tocar).**

Y de ahi sale el argumento central del pipeline: si la tension existe a nivel GEN, la unica
salida es decidir a nivel VENTANA, porque dentro de un gen conservado igual hay tramos que no
se parecen a nada de afuera.

Uso:
    python3 tension_conservacion.py
"""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

SALIDA = Path(__file__).parent / "salida"
UMBRAL_RIESGO = 17  # nt identicos a partir de los cuales contamos la ventana como riesgosa


def numero(v, por_defecto=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return por_defecto


def spearman(xs, ys):
    def rangos(v):
        orden = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(orden):
            j = i
            while j + 1 < len(orden) and v[orden[j + 1]] == v[orden[i]]:
                j += 1
            for k in range(i, j + 1):
                r[orden[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = rangos(xs), rangos(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else float("nan")


def main() -> None:
    conservacion: dict[str, float] = {}
    for fila in csv.DictReader((SALIDA / "tabla_unificada.csv").open(encoding="utf-8")):
        ident = [numero(fila.get(f"{p}_identidad")) for p in ("tcas", "dmel", "nlug")]
        ident = [v for v in ident if v > 0]
        if ident:
            conservacion[fila["locus"]] = max(ident)

    ventanas: dict[str, list[int]] = defaultdict(list)
    for fila in csv.DictReader((SALIDA / "sirna_finales.csv").open(encoding="utf-8")):
        ventanas[fila["locus"]].append(int(numero(fila.get("off_target_max"))))

    datos = []
    for locus, offs in ventanas.items():
        if locus not in conservacion or len(offs) < 5:
            continue
        riesgosas = sum(1 for o in offs if o >= UMBRAL_RIESGO) / len(offs)
        datos.append((conservacion[locus], riesgosas, max(offs), locus))

    if len(datos) < 10:
        print(f"pocos genes con datos ({len(datos)}); correr antes cadena_completa.py")
        return

    xs = [d[0] for d in datos]
    ys = [d[1] for d in datos]
    rho = spearman(xs, ys)
    rho_max = spearman(xs, [d[2] for d in datos])

    print(f"genes analizados: {len(datos)}")
    print(f"Spearman(conservacion, fraccion de ventanas riesgosas) = {rho:+.3f}")
    print(f"Spearman(conservacion, peor coincidencia del gen)      = {rho_max:+.3f}")

    print(f"\nPor tramo de conservacion:")
    print(f"{'identidad':<16}{'genes':>7}{'ventanas riesgosas':>21}{'peor coincidencia':>20}")
    tramos = [(0.0, 0.5), (0.5, 0.7), (0.7, 0.85), (0.85, 1.01)]
    for bajo, alto in tramos:
        grupo = [d for d in datos if bajo <= d[0] < alto]
        if not grupo:
            continue
        media_riesgo = sum(d[1] for d in grupo) / len(grupo)
        media_peor = sum(d[2] for d in grupo) / len(grupo)
        print(f"{bajo:.2f} a {alto:.2f}      {len(grupo):>7}{media_riesgo * 100:>20.1f}%"
              f"{media_peor:>20.1f}")

    # La pregunta que importa: aun en los genes mas conservados, quedan ventanas limpias?
    muy_conservados = [d for d in datos if d[0] >= 0.85]
    if muy_conservados:
        limpios = sum(1 for d in muy_conservados if d[1] < 0.5)
        print(f"\nGenes con identidad >= 0,85: {len(muy_conservados)}")
        print(f"  de esos, con MENOS de la mitad de sus ventanas riesgosas: {limpios} "
              f"({limpios / len(muy_conservados) * 100:.0f} %)")
        print("\nEsa es la salida al problema: el gen entero es riesgoso, pero adentro del gen")
        print("siguen quedando tramos limpios. Por eso se decide a nivel ventana y no a nivel gen.")


if __name__ == "__main__":
    main()
