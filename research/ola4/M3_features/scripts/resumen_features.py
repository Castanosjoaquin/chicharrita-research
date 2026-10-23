"""Resumen agregado de la tabla de `--features`, que es lo unico que se versiona.

Por que un resumen y no la tabla. El issue #7 pide «research/ola4/M3_features/REPORT.md
con la tabla de los cuatro genes». La tabla por ventana **no se versiona**, y la razon la
midio M9: `nt19_at` y `nt2_gc` son un bit por posicion sobre ventanas que se solapan de a
1 nt, asi que la columna es un perfil del gen —no permite escribir la secuencia, pero
tampoco es independiente de ella—. Lo que se versiona es este resumen, que agrega por
gen y por rama y no conserva el orden de las ventanas, mas el comando para regenerar la
tabla completa en local. Es la misma politica que ya rige para la columna `seq`.

Que informa, y nada mas que eso: cuantas ventanas caen en cada rama de la regla
terminal, cuantas de ellas resultan eficientes, y el rango de cada termino continuo.
**No ajusta ningun modelo** y no estima ninguna contribucion: con 29 etiquetas de
eficacia medida no se ajusta un modelo de seis variables, y el plan de analisis se
preregistra en M4 (#8). Ver REPORT.md §4.

    python3 research/ola4/M3_features/scripts/resumen_features.py <dir_con_features_tsv>
"""

from __future__ import annotations

import csv
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

GENES = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]
CONTINUOS = ["dg_sense5", "dg_antisense5", "ddg", "accessibility"]
RAMAS = {
    1: "nt19 A/T, nt2 A/T: decide la termodinamica",
    2: "nt19 A/T, nt2 G/C: ATAJO, decide solo la accesibilidad",
    3: "nt19 G/C, nt2 G/C: decide la termodinamica",
    4: "nt19 G/C, nt2 A/T: no eficiente sin mirar nada mas",
}


def resumir(tsv: Path) -> dict:
    filas = list(csv.DictReader(tsv.open(encoding="utf-8"), delimiter="\t"))
    if not filas:
        raise SystemExit(f"{tsv}: vacio")

    por_rama: dict[int, Counter] = defaultdict(Counter)
    for f in filas:
        r = int(f["rama_terminal"])
        por_rama[r]["ventanas"] += 1
        por_rama[r]["eficientes"] += f["is_efficient"] == "True"

    continuos = {}
    for c in CONTINUOS:
        vals = [float(f[c]) for f in filas]
        continuos[c] = {
            "min": round(min(vals), 4),
            "mediana": round(statistics.median(vals), 4),
            "max": round(max(vals), 4),
        }

    efic = sum(1 for f in filas if f["is_efficient"] == "True")
    return {
        "ventanas": len(filas),
        "eficientes": efic,
        "por_rama": {
            str(r): {
                "descripcion": RAMAS[r],
                "ventanas": por_rama[r]["ventanas"],
                "eficientes": por_rama[r]["eficientes"],
                "pct_de_los_eficientes": round(100 * por_rama[r]["eficientes"] / efic, 1)
                if efic
                else 0.0,
            }
            for r in sorted(por_rama)
        },
        "continuos": continuos,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip().split("\n")[-1])
        return 2
    origen = Path(argv[1])
    salida_dir = Path(__file__).resolve().parents[1] / "resultados"
    salida_dir.mkdir(parents=True, exist_ok=True)

    todo: dict[str, dict] = {}
    for modo in ("fiel", "corregido"):
        for gen in GENES:
            cands = sorted(origen.glob(f"{gen}*_{modo}_*_features.tsv"))
            if not cands:
                continue
            todo[f"{gen}:{modo}"] = resumir(cands[0])

    if not todo:
        raise SystemExit(f"{origen}: no hay TSV de features (corré run_sifi.py --features)")

    (salida_dir / "resumen_features.json").write_text(
        json.dumps(todo, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    lineas = [
        "## Tabla de `--features`: resumen por gen y por rama terminal",
        "",
        "Agregado de la tabla por ventana, que no se versiona (ver el encabezado del",
        "script). Conteos con `--backend vienna`; con `--backend exe` los totales son",
        "otros y la conclusión sobre el peso de cada rama no cambia.",
        "",
    ]
    for modo in ("fiel", "corregido"):
        claves = [k for k in todo if k.endswith(f":{modo}")]
        if not claves:
            continue
        lineas += [
            f"### Modo `{modo}`",
            "",
            "| Gen | Ventanas | Eficientes | Rama 1 | Rama 2 (atajo) | Rama 3 | Rama 4 |",
            "|---|---|---|---|---|---|---|",
        ]
        for k in claves:
            gen = k.split(":")[0]
            d = todo[k]
            celdas = []
            for r in ("1", "2", "3", "4"):
                if r in d["por_rama"]:
                    v = d["por_rama"][r]
                    celdas.append(f"{v['eficientes']}/{v['ventanas']}")
                else:
                    celdas.append("-")
            lineas.append(
                f"| `{gen}` | {d['ventanas']} | {d['eficientes']} | " + " | ".join(celdas) + " |"
            )
        lineas.append("")
        lineas.append("Cada celda es eficientes/ventanas de esa rama.")
        lineas.append("")

    (salida_dir / "resumen_features.md").write_text("\n".join(lineas), encoding="utf-8")
    print(f"escrito en {salida_dir}: resumen_features.json y .md ({len(todo)} combinaciones)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
