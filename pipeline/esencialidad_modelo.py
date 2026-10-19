"""Se puede rankear genes por esencialidad SIN usar el cribado de Tribolium?

Por que importa: iBeetle-Base no tiene licencia abierta, asi que apoyar todo el ranking en sus
fenotipos compromete lo que podamos publicar (modalidad D). Y ademas su cribado cubre 13.009
genes: los que quedan afuera no tienen con que puntuarse.

La pregunta honesta: la senal de esencialidad, se puede recuperar desde datos abiertos?

Diseno del experimento, pensado para NO hacer trampa:
  - Etiqueta: el fenotipo letal reportado en Tribolium. Es la verdad que queremos predecir.
  - Features: SOLO las de los alineamientos de *Drosophila* y *Nilaparvata*. Se excluye a
    proposito todo lo que venga de Tribolium, porque esa es la fuente de la etiqueta. Si se
    dejara entrar, el modelo estaria leyendo la respuesta.
  - Evaluacion: validacion cruzada estratificada, mas un baseline que siempre dice la clase
    mayoritaria. Se reporta AUC, que no se deja enganar por el desbalance de clases.

Lo que un resultado positivo significaria: que la conservacion entre especies abiertas ya trae
buena parte de la senal de esencialidad, y que el cribado cerrado sirve para validar, no como
insumo obligatorio.

Uso:
    python3 esencialidad_modelo.py
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path

SALIDA = Path(__file__).parent / "salida"
TABLA = SALIDA / "tabla_unificada.csv"

# Deliberadamente NINGUNA columna tcas_*: esa es la fuente de la etiqueta.
FEATURES = [
    "dmel_identidad", "dmel_positivos", "dmel_exones",
    "dmel_frameshift", "dmel_stop_interno", "dmel_n_hits_de_esa_proteina",
    "nlug_identidad", "nlug_positivos", "nlug_exones",
    "nlug_frameshift", "nlug_stop_interno", "nlug_n_hits_de_esa_proteina",
]


def flotante(valor: str) -> float | None:
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


def etiquetas_por_fase(fase: str = "I", umbral: float = 30.0) -> dict[str, int]:
    """Letalidad por gen de Tribolium, usando SOLO una fase del cribado.

    Hace falta porque medimos que la fase es un efecto de lote grande: mezclando fases, la
    reproducibilidad entre dos construcciones del mismo gen cae de 0,245 a 0,076. Una etiqueta
    construida sobre fases mezcladas arrastra ese ruido.
    """
    ibeetle = Path.home() / "yhat" / "data" / "ibeetle"
    ib_a_gen: dict[str, str] = {}
    with (ibeetle / "iB_TC.csv").open(encoding="utf-8-sig") as fh:
        for linea in fh:
            if linea.startswith("#") or "," not in linea:
                continue
            ib, gen = linea.strip().split(",")[:2]
            ib_a_gen[ib.strip()] = gen.strip()

    por_gen: dict[str, list[float]] = {}
    with (ibeetle / "iBeetle_lethality.csv").open(encoding="utf-8-sig") as fh:
        for fila in csv.DictReader(fh, delimiter=";"):
            if (fila.get("phase") or "").strip() != fase:
                continue
            gen = ib_a_gen.get((fila.get("iB") or "").strip())
            valor = flotante((fila.get("dali11") or "").strip())
            if gen and valor is not None:
                por_gen.setdefault(gen, []).append(valor)

    return {g: int(max(v) >= umbral) for g, v in por_gen.items()}


def cargar() -> tuple[list[list[float]], list[int], list[str], list[str]]:
    """Devuelve (X, y, nombres de features, grupo de cada fila).

    El grupo es el gen de Drosophila. Dos loci de D. maidis que mapean al MISMO gen de
    Drosophila son parálogos o fragmentos del mismo gen: si uno cae en entrenamiento y el
    otro en test, el modelo ya vio la respuesta. Agrupar por ese gen cierra esa fuga.
    """
    por_fase = etiquetas_por_fase()
    X: list[list[float]] = []
    y: list[int] = []
    grupos: list[str] = []
    usadas_de_fase = 0
    with TABLA.open(encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            etiqueta_fase = por_fase.get((fila.get("mejor_hit_tribolium") or "").strip())
            if etiqueta_fase is None and not fila.get("fenotipo_categoria"):
                continue
            # Solo filas con al menos una via abierta (Drosophila o Nilaparvata)
            vals = [flotante(fila.get(c, "")) for c in FEATURES]
            if all(v is None for v in vals):
                continue
            X.append([v if v is not None else 0.0 for v in vals])
            # ausencia_dmel / ausencia_nlug: que no haya hit tambien es informacion
            X[-1] += [float(flotante(fila.get("dmel_identidad", "")) is None),
                      float(flotante(fila.get("nlug_identidad", "")) is None)]
            if etiqueta_fase is not None:
                y.append(etiqueta_fase)
                usadas_de_fase += 1
            else:
                y.append(int(fila.get("fenotipo_categoria") == "letal"))
            grupos.append(fila.get("gen_drosophila") or fila.get("mejor_hit_drosophila")
                          or f"solo_{fila['locus']}")
    print(f"etiquetas tomadas de una sola fase del cribado: {usadas_de_fase} de {len(y)}")
    return X, y, FEATURES + ["sin_hit_dmel", "sin_hit_nlug"], grupos


def estandarizar(X: list[list[float]]) -> list[list[float]]:
    n_cols = len(X[0])
    medias = [sum(f[j] for f in X) / len(X) for j in range(n_cols)]
    desvios = []
    for j in range(n_cols):
        var = sum((f[j] - medias[j]) ** 2 for f in X) / len(X)
        desvios.append(math.sqrt(var) or 1.0)
    return [[(f[j] - medias[j]) / desvios[j] for j in range(n_cols)] for f in X]


def entrenar(X: list[list[float]], y: list[int], pasos: int = 400, lr: float = 0.3) -> list[float]:
    """Regresion logistica por descenso de gradiente. Sin dependencias externas."""
    w = [0.0] * (len(X[0]) + 1)
    n = len(X)
    for _ in range(pasos):
        grad = [0.0] * len(w)
        for fila, etiqueta in zip(X, y):
            z = w[0] + sum(w[j + 1] * fila[j] for j in range(len(fila)))
            p = 1 / (1 + math.exp(-max(-30, min(30, z))))
            err = p - etiqueta
            grad[0] += err
            for j in range(len(fila)):
                grad[j + 1] += err * fila[j]
        for j in range(len(w)):
            w[j] -= lr * grad[j] / n
    return w


def predecir(w: list[float], fila: list[float]) -> float:
    z = w[0] + sum(w[j + 1] * fila[j] for j in range(len(fila)))
    return 1 / (1 + math.exp(-max(-30, min(30, z))))


def auc(y: list[int], p: list[float]) -> float:
    pares = sorted(zip(p, y))
    pos = sum(y)
    neg = len(y) - pos
    if pos == 0 or neg == 0:
        return float("nan")
    rango_pos = 0.0
    for i, (_, etiqueta) in enumerate(pares, start=1):
        if etiqueta:
            rango_pos += i
    return (rango_pos - pos * (pos + 1) / 2) / (pos * neg)


def main() -> None:
    X, y, nombres, grupos = cargar()
    pos = sum(y)
    print(f"genes con fenotipo y al menos una via abierta: {len(X)}")
    print(f"  letales: {pos} ({pos / len(X) * 100:.1f} %)  ·  no letales: {len(X) - pos}")
    print(f"features usadas: {len(nombres)} (ninguna de Tribolium, que es la fuente de la etiqueta)")
    print(f"grupos distintos (gen de Drosophila): {len(set(grupos))}")

    Xs = estandarizar(X)
    k = 5

    def evaluar(asignar) -> tuple[float, float, list[float]]:
        aucs = []
        for pliegue in range(k):
            test = {i for i in range(len(Xs)) if asignar[i] == pliegue}
            if not test or len(test) == len(Xs):
                continue
            Xtr = [Xs[i] for i in range(len(Xs)) if i not in test]
            ytr = [y[i] for i in range(len(Xs)) if i not in test]
            Xte = [Xs[i] for i in sorted(test)]
            yte = [y[i] for i in sorted(test)]
            if len(set(yte)) < 2:
                continue
            w = entrenar(Xtr, ytr)
            aucs.append(auc(yte, [predecir(w, f) for f in Xte]))
        media = sum(aucs) / len(aucs)
        desvio = math.sqrt(sum((a - media) ** 2 for a in aucs) / len(aucs))
        return media, desvio, aucs

    rnd = random.Random(0)
    indices = list(range(len(Xs)))
    rnd.shuffle(indices)
    al_azar = [0] * len(Xs)
    for orden, i in enumerate(indices):
        al_azar[i] = orden % k

    claves = sorted(set(grupos))
    rnd.shuffle(claves)
    pliegue_de = {g: i % k for i, g in enumerate(claves)}
    agrupado = [pliegue_de[g] for g in grupos]

    m_azar, d_azar, _ = evaluar(al_azar)
    m_grupo, d_grupo, aucs_grupo = evaluar(agrupado)

    print(f"\n{'evaluacion':<34}{'AUC':>8}{'desvio':>9}")
    print(f"{'split al azar (optimista)':<34}{m_azar:>8.3f}{d_azar:>9.3f}")
    print(f"{'split agrupado por gen (honesto)':<34}{m_grupo:>8.3f}{d_grupo:>9.3f}")
    print(f"{'azar':<34}{0.5:>8.3f}")
    print(f"\ncaida por cerrar la fuga de parálogos: {m_azar - m_grupo:+.3f}")
    print("pliegues del split agrupado: " + ", ".join(f"{a:.3f}" for a in aucs_grupo))
    media = m_grupo

    w = entrenar(Xs, y)
    print("\nPeso de cada feature (que mira el modelo):")
    for nombre, peso in sorted(zip(nombres, w[1:]), key=lambda t: -abs(t[1]))[:8]:
        print(f"  {nombre:<32}{peso:>8.3f}")

    if media > 0.6:
        print("\nHay senal: la conservacion entre especies abiertas predice esencialidad")
        print("por encima del azar, SIN mirar el cribado de Tribolium.")
    else:
        print("\nNo hay senal util. Resultado negativo, y vale reportarlo igual.")


if __name__ == "__main__":
    main()
