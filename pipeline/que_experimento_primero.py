"""Si el laboratorio puede correr 12 ensayos, cuales 12 conviene correr?

Esta es la pregunta que el resto del pipeline no contesta. Rankear candidatos dice cual es
el mejor; esto dice **cual conviene medir**, que no es lo mismo. El mejor candidato suele ser
el que ya sabemos que es bueno: medirlo no ensena nada.

Y es la pregunta que importa economicamente: un ensayo lleva unas tres semanas con colonia
viva e invernadero. El dsRNA es lo barato; el tiempo de laboratorio es lo caro. Elegir mal
los doce primeros cuesta una temporada.

El experimento, simulado con lo que tenemos:
  - Universo: los genes de la tabla unificada con fenotipo conocido en Tribolium.
  - Las etiquetas se **esconden**, y el laboratorio simulado las revela de a tandas.
  - Se comparan estrategias de eleccion de tanda:
      azar          elegir al azar (el baseline honesto)
      mejor_score   medir los que el modelo cree mejores (lo que uno haria sin pensar)
      incertidumbre medir los que el modelo no sabe clasificar (aprendizaje activo clasico)
      diverso       incertidumbre, pero sin repetir familias de genes parecidos
  - Metrica: AUC del modelo en el resto del universo, despues de cada tanda.

Lo que se quiere ver: cuantos ensayos ahorra elegir bien. Si no ahorra ninguno, tambien es
resultado y vale reportarlo.

Uso:
    python3 que_experimento_primero.py [--tanda 12] [--tandas 10] [--repeticiones 20]
"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from esencialidad_modelo import auc, cargar, entrenar, estandarizar, predecir  # noqa: E402


def elegir(estrategia: str, disponibles: list[int], modelo, X, grupos, k: int,
           rnd: random.Random, ya_vistos: set[str]) -> list[int]:
    if estrategia == "azar" or modelo is None:
        return rnd.sample(disponibles, min(k, len(disponibles)))

    puntajes = [(i, predecir(modelo, X[i])) for i in disponibles]

    if estrategia == "mejor_score":
        puntajes.sort(key=lambda t: -t[1])
        return [i for i, _ in puntajes[:k]]

    # incertidumbre: lo mas cerca de 0,5 es lo que el modelo menos sabe
    puntajes.sort(key=lambda t: abs(t[1] - 0.5))
    if estrategia == "incertidumbre":
        return [i for i, _ in puntajes[:k]]

    # diverso: incertidumbre pero sin repetir familia de genes ya medida
    elegidos, familias = [], set(ya_vistos)
    for i, _ in puntajes:
        fam = grupos[i]
        if fam in familias:
            continue
        familias.add(fam)
        elegidos.append(i)
        if len(elegidos) >= k:
            break
    # si la diversidad no alcanza, se completa con incertidumbre pura
    for i, _ in puntajes:
        if len(elegidos) >= k:
            break
        if i not in elegidos:
            elegidos.append(i)
    return elegidos


def main() -> None:
    def arg(nombre: str, por_defecto: int) -> int:
        return int(sys.argv[sys.argv.index(nombre) + 1]) if nombre in sys.argv else por_defecto

    tanda = arg("--tanda", 12)
    n_tandas = arg("--tandas", 10)
    repeticiones = arg("--repeticiones", 20)

    X, y, nombres, grupos = cargar()
    Xs = estandarizar(X)
    print(f"universo: {len(Xs)} genes con fenotipo · {sum(y)} letales "
          f"({sum(y) / len(y) * 100:.0f} %)")
    print(f"simulacion: tandas de {tanda} ensayos, {n_tandas} tandas, "
          f"{repeticiones} repeticiones\n")

    estrategias = ["azar", "mejor_score", "incertidumbre", "diverso"]
    curvas: dict[str, list[list[float]]] = {e: [] for e in estrategias}

    for rep in range(repeticiones):
        rnd = random.Random(rep)
        # Conjunto de evaluacion fijo por repeticion: no se puede medir sobre lo ya medido
        indices = list(range(len(Xs)))
        rnd.shuffle(indices)
        evaluacion = indices[:len(indices) // 4]
        universo = indices[len(indices) // 4:]
        Xev = [Xs[i] for i in evaluacion]
        yev = [y[i] for i in evaluacion]

        for estrategia in estrategias:
            disponibles = list(universo)
            medidos: list[int] = []
            vistos: set[str] = set()
            modelo = None
            curva = []
            for _ in range(n_tandas):
                nuevos = elegir(estrategia, disponibles, modelo, Xs, grupos, tanda, rnd, vistos)
                medidos.extend(nuevos)
                vistos.update(grupos[i] for i in nuevos)
                disponibles = [i for i in disponibles if i not in set(nuevos)]
                etiquetas = [y[i] for i in medidos]
                if len(set(etiquetas)) < 2:
                    curva.append(0.5)
                    continue
                modelo = entrenar([Xs[i] for i in medidos], etiquetas, pasos=150)
                curva.append(auc(yev, [predecir(modelo, f) for f in Xev]))
            curvas[estrategia].append(curva)

    print(f"{'ensayos':>8}" + "".join(f"{e:>15}" for e in estrategias))
    for t in range(n_tandas):
        fila = f"{(t + 1) * tanda:>8}"
        for e in estrategias:
            vals = [c[t] for c in curvas[e]]
            fila += f"{sum(vals) / len(vals):>15.3f}"
        print(fila)

    print()
    tope = {e: sum(c[-1] for c in curvas[e]) / len(curvas[e]) for e in estrategias}
    mejor = max(tope, key=tope.get)
    print(f"Al final de {n_tandas * tanda} ensayos: " +
          " · ".join(f"{e} {tope[e]:.3f}" for e in estrategias))

    # Cuantos ensayos necesita cada estrategia para llegar a donde llega el azar al final
    objetivo = tope["azar"]
    print(f"\nEnsayos necesarios para alcanzar el AUC que el azar logra con "
          f"{n_tandas * tanda} ({objetivo:.3f}):")
    for e in estrategias:
        promedio = [sum(c[t] for c in curvas[e]) / len(curvas[e]) for t in range(n_tandas)]
        alcanzo = next((t for t, v in enumerate(promedio) if v >= objetivo), None)
        if alcanzo is None:
            print(f"  {e:<14} no lo alcanza en {n_tandas * tanda}")
        else:
            n = (alcanzo + 1) * tanda
            ahorro = (n_tandas * tanda - n) / (n_tandas * tanda) * 100
            print(f"  {e:<14} {n:>4} ensayos" +
                  (f"  ({ahorro:.0f} % menos)" if ahorro > 0 else ""))

    print(f"\nMejor estrategia: {mejor}")


if __name__ == "__main__":
    main()
