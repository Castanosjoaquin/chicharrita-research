"""Punto de entrada unico: corre la cadena completa desde cero y dice que falta.

Un pipeline que solo corre en la maquina del que lo escribio no sirve de entregable. Esto
chequea las dependencias, avisa que falta y en que orden, y corre las etapas que puede.

Cada etapa declara que necesita y que produce. Si la salida ya existe se saltea, salvo
que se pase --forzar.

Uso:
    python3 correr_todo.py              # corre lo que falte
    python3 correr_todo.py --revisar    # solo dice que hay y que falta, no corre nada
    python3 correr_todo.py --forzar     # rehace todo
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SALIDA = AQUI / "salida"
DATOS = Path.home() / "yhat" / "data"
MINIPROT = Path.home() / "yhat" / "tools" / "miniprot" / "miniprot"

# (nombre, que necesita, que produce, como correrlo)
ETAPAS: list[tuple[str, list[Path], list[Path], list[str] | None]] = [
    ("herramienta miniprot", [], [MINIPROT], None),
    ("genoma de referencia", [], [DATOS / "genome.fna.gz"], None),
    ("indice del genoma", [DATOS / "genome.fna.gz"], [DATOS / "genome.mpi"],
     [str(MINIPROT), "-t", "20", "-d", str(DATOS / "genome.mpi"), str(DATOS / "genome.fna.gz")]),
    ("proteomas de referencia", [DATOS / "genome.mpi"],
     [DATOS / "dmel.gff", DATOS / "nilaparvata.gff"], ["python3", str(AQUI / "hemip_mapear.py")]),
    ("tabla unificada de loci", [DATOS / "tcas.gff"], [SALIDA / "tabla_unificada.csv"],
     ["python3", str(AQUI / "tabla_unificada.py")]),
    ("transcriptomas no objetivo", [], [DATOS / "maiz_rna.fna.gz", DATOS / "abeja_rna.fna.gz"],
     ["python3", str(AQUI / "bajar_no_objetivo.py")]),
    ("tests de features", [], [], ["python3", str(AQUI / "test_features.py")]),
    ("cadena completa", [SALIDA / "tabla_unificada.csv", DATOS / "genome.mpi"],
     [SALIDA / "sirna_finales.csv"],
     ["python3", str(AQUI / "cadena_completa.py"), "120", "letal"]),
]

VERDE, ROJO, GRIS, FIN = "\033[32m", "\033[31m", "\033[90m", "\033[0m"


def existe(rutas: list[Path]) -> bool:
    return all(r.exists() and (r.is_dir() or r.stat().st_size > 0) for r in rutas)


def main() -> None:
    solo_revisar = "--revisar" in sys.argv
    forzar = "--forzar" in sys.argv

    print(f"{'etapa':<28}{'estado':<14}{'detalle'}")
    print("-" * 74)
    hubo_bloqueo = False

    for nombre, necesita, produce, comando in ETAPAS:
        if not existe(necesita):
            faltan = [n.name for n in necesita if not n.exists()]
            print(f"{nombre:<28}{ROJO}bloqueada{FIN:<9}  falta: {', '.join(faltan)}")
            hubo_bloqueo = True
            continue

        if produce and existe(produce) and not forzar:
            print(f"{nombre:<28}{GRIS}ya esta{FIN:<11}  {produce[0].name}")
            continue

        if comando is None:
            print(f"{nombre:<28}{ROJO}falta{FIN:<13}  hay que conseguirlo a mano, ver README")
            hubo_bloqueo = True
            continue

        if solo_revisar:
            print(f"{nombre:<28}correria      {' '.join(comando[:2])}...")
            continue

        inicio = time.time()
        print(f"{nombre:<28}corriendo...", flush=True)
        resultado = subprocess.run(comando, capture_output=True, text=True)
        seg = time.time() - inicio
        if resultado.returncode != 0:
            print(f"{'':<28}{ROJO}fallo{FIN}  codigo {resultado.returncode}")
            print("  " + (resultado.stderr or resultado.stdout or "").strip()[-400:])
            hubo_bloqueo = True
            break
        print(f"{'':<28}{VERDE}ok{FIN}  {seg:.1f}s")

    print("-" * 74)
    if hubo_bloqueo:
        print("Quedaron etapas sin correr. Las que dicen 'falta' necesitan una descarga manual:")
        print("  genoma   : ver pipeline/README.md, seccion Reproducirlo")
        print("  miniprot : git clone https://github.com/lh3/miniprot && make")
        sys.exit(1)
    print("Cadena completa. Resultados en pipeline/salida/")


if __name__ == "__main__":
    main()
