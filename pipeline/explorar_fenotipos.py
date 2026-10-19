"""Exploracion rapida de los datos crudos de iBeetle: que hay y con que forma.

No produce nada del pipeline, solo imprime para entender el formato antes de
construir la tabla unificada.

Uso:
    python3 explorar_fenotipos.py <dir_ibeetle>
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path


def main() -> int:
    base = Path(sys.argv[1])

    print("=== iBeetle_lethality.csv ===")
    with (base / "iBeetle_lethality.csv").open(encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f, delimiter=";"))
    print(f"filas: {len(filas)}  columnas: {list(filas[0])}")
    print(f"fases: {Counter(f['phase'] for f in filas)}")
    for col in ("dali11", "dali22", "dapi11"):
        valores = [f[col] for f in filas]
        vacios = sum(1 for v in valores if v.strip() == "")
        numeros = [float(v) for v in valores if v.strip() != ""]
        print(f"  {col}: vacios={vacios} min={min(numeros)} max={max(numeros)} "
              f"distintos={len(set(numeros))}")

    print()
    print("=== iBeetle_grouped_phenotypes.ndjson ===")
    genes = 0
    n_fen = 0
    topics: Counter[str] = Counter()
    descripciones: Counter[str] = Counter()
    experimentos: Counter[str] = Counter()
    con_penetrancia = 0
    with (base / "iBeetle_grouped_phenotypes.ndjson").open(encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            obj = json.loads(linea)
            genes += 1
            for fen in obj.get("phenotypes", []):
                n_fen += 1
                topics[fen.get("iBeetleTopic", "(sin topic)")] += 1
                descripciones[fen.get("description", "")] += 1
                experimentos[fen.get("iBeetleExperiment", "")] += 1
                if "penetrance" in fen:
                    con_penetrancia += 1
    print(f"genes con alguna anotacion: {genes}")
    print(f"anotaciones de fenotipo totales: {n_fen}")
    print(f"con penetrancia declarada: {con_penetrancia}")
    print(f"experimentos: {experimentos}")
    print(f"topics distintos: {len(topics)}")
    for t, n in topics.most_common(40):
        print(f"  {n:>7}  {t}")
    print(f"descripciones distintas: {len(descripciones)}")
    for d, n in descripciones.most_common(40):
        print(f"  {n:>7}  {d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
