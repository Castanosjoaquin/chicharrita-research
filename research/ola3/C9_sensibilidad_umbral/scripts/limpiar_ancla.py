"""Quita la columna `seq` de los TSV del ancla antes de versionarlos.

Por que existe: `run_sifi.py` escribe un 21-mero por ventana, y como las ventanas
se solapan de a 1 nt esa columna reconstruye el gen completo. Dos de los cuatro
genes son secuencias de EPILAB, que por la regla de CLAUDE.md no se publican. El
ancla no las necesita: reproduce conteos y regiones con posiciones y booleanos.

Uso (desde la raiz del repositorio, despues de correr run_sifi.py):
    python research/ola3/C9_sensibilidad_umbral/scripts/limpiar_ancla.py
"""
import re
from pathlib import Path

ANCLA = Path(__file__).resolve().parents[1] / "resultados" / "ancla"

for p in sorted(ANCLA.glob("*_vienna.tsv")):
    lines = p.read_text(encoding="utf-8").rstrip("\n").split("\n")
    cols = lines[0].split("\t")
    if "seq" not in cols:
        print(p.name, "ya estaba limpio")
        continue
    i = cols.index("seq")
    out = ["\t".join(c for j, c in enumerate(l.split("\t")) if j != i) for l in lines]
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(p.name, "columna seq quitada")

rachas = sum(len(re.findall(r"[ACGT]{21,}", f.read_text(encoding="utf-8", errors="ignore")))
             for f in ANCLA.parent.rglob("*") if f.is_file())
print("rachas de 21 nt o mas en resultados/:", rachas)
assert rachas == 0, "quedan secuencias largas en resultados/"
