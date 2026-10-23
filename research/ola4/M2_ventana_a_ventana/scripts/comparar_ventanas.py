"""Compara dos perfiles por ventana del port y dice **que termino cruzo el corte**.

Es la tarea 1 del issue #6. Diego lo pidio asi: «seria util comparar cuales son las
ventanas especificas que cambian de clasificacion, en lugar de considerar unicamente el
conteo final». Un conteo que cambia no dice nada; una ventana que cambia porque su `ddg`
paso de 1,0561 a 0,9885 y cruzo el umbral de 1,0, si.

Para cada par devuelve tres cosas:
  - la matriz de confusion (eficiente/no por lado);
  - la lista de posiciones que cambian de clase;
  - para cada una, cual de los cuatro booleanos del veredicto cambio y cuanto se movieron
    los cuatro terminos continuos.

Sobre el alineamiento de posiciones. Tres de los cuatro pares comparan perfiles de la
misma secuencia, asi que `pos` alinea directo. El par de recorte contra contexto no: la
ventana que en el gen esta en 922 es la 1 del recorte, de modo que hay que pasar
`--offset-b` con el inicio de la region (1-based). Las posiciones que no existen de los
dos lados se informan como `solo_a` o `solo_b` y no entran a la matriz: en el recorte son
las 20 ultimas posiciones de inicio, que el gen tiene y la molecula recortada no.

    python3 research/ola4/M2_ventana_a_ventana/scripts/comparar_ventanas.py \\
            --a <tsv_a> --b <tsv_b> [--offset-b N] [--etiquetas A,B] \\
            --salida <prefijo>

Escribe `<prefijo>_resumen.json` y, si hay cambios, `<prefijo>_cambios.tsv`.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

# Los cuatro booleanos del veredicto, en el orden en que el motor los evalua. El quinto,
# `is_efficient`, es el veredicto mismo y por eso no entra en la lista de terminos.
BOOLEANOS = ["strand_selection", "end_stability", "target_site_accessibility",
             "thermo_efficient"]
CONTINUOS = ["dg_sense5", "dg_antisense5", "ddg", "accessibility"]


def leer(ruta: Path) -> dict[int, dict]:
    with ruta.open(encoding="utf-8") as fh:
        filas = {int(r["pos"]): r for r in csv.DictReader(fh, delimiter="\t")}
    if not filas:
        raise SystemExit(f"{ruta}: vacio o sin columna pos")
    if "is_efficient" not in next(iter(filas.values())):
        raise SystemExit(f"{ruta}: falta la columna is_efficient")
    return filas


def _bool(valor: str) -> bool:
    return str(valor).strip().lower() == "true"


def comparar(a: dict[int, dict], b: dict[int, dict], offset_b: int = 1,
             etiquetas: tuple[str, str] = ("a", "b")) -> tuple[dict, list[dict]]:
    """`offset_b` es la posicion del gen que corresponde a la posicion 1 de `b`."""
    ea, eb = etiquetas
    # pos_a = pos_b + offset_b - 1
    comunes = sorted(p for p in a if (p - offset_b + 1) in b)
    conf = {"ambos_si": 0, "ambos_no": 0, f"solo_{ea}": 0, f"solo_{eb}": 0}
    cambios: list[dict] = []

    for pa in comunes:
        pb = pa - offset_b + 1
        fa, fb = a[pa], b[pb]
        va, vb = _bool(fa["is_efficient"]), _bool(fb["is_efficient"])
        if va and vb:
            conf["ambos_si"] += 1
        elif not va and not vb:
            conf["ambos_no"] += 1
        elif va:
            conf[f"solo_{ea}"] += 1
        else:
            conf[f"solo_{eb}"] += 1
        if va == vb:
            continue
        fila = {
            "pos": pa,
            f"pos_{eb}": pb,
            ea: va,
            eb: vb,
            "terminos_que_cruzan": ",".join(
                c for c in BOOLEANOS if c in fa and c in fb and fa[c] != fb[c]
            ),
            "rama_terminal": fa.get("rama_terminal", ""),
        }
        for c in CONTINUOS:
            if c not in fa or c not in fb:
                continue
            x, y = float(fa[c]), float(fb[c])
            fila[f"{c}_{ea}"] = round(x, 6)
            fila[f"{c}_{eb}"] = round(y, 6)
            fila[f"{c}_delta"] = round(y - x, 6)
        cambios.append(fila)

    resumen = {
        "etiquetas": [ea, eb],
        "offset_b": offset_b,
        "ventanas_comparadas": len(comunes),
        f"ventanas_solo_en_{ea}": len(a) - len(comunes),
        f"ventanas_solo_en_{eb}": len(b) - len(comunes),
        f"eficientes_{ea}": conf["ambos_si"] + conf[f"solo_{ea}"],
        f"eficientes_{eb}": conf["ambos_si"] + conf[f"solo_{eb}"],
        "confusion": conf,
        "cambian": len(cambios),
        "terminos": sorted({t for c in cambios
                            for t in c["terminos_que_cruzan"].split(",") if t}),
    }
    return resumen, cambios


def escribir(prefijo: Path, resumen: dict, cambios: list[dict]) -> None:
    prefijo.parent.mkdir(parents=True, exist_ok=True)
    prefijo.with_name(prefijo.name + "_resumen.json").write_text(
        json.dumps(resumen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if cambios:
        cols = list(cambios[0].keys())
        destino = prefijo.with_name(prefijo.name + "_cambios.tsv")
        with destino.open("w", encoding="utf-8", newline="") as fh:
            fh.write("\t".join(cols) + "\n")
            for f in cambios:
                fh.write("\t".join(str(f.get(c, "")) for c in cols) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True, type=Path)
    ap.add_argument("--b", required=True, type=Path)
    ap.add_argument("--offset-b", type=int, default=1, dest="offset_b",
                    help="posicion del gen que corresponde a la posicion 1 de --b")
    ap.add_argument("--etiquetas", default="a,b",
                    help="dos nombres separados por coma, para las columnas de salida")
    ap.add_argument("--salida", required=True, type=Path, help="prefijo de los archivos")
    args = ap.parse_args()

    ea, eb = (args.etiquetas.split(",") + ["b"])[:2]
    resumen, cambios = comparar(leer(args.a), leer(args.b), args.offset_b, (ea, eb))
    escribir(args.salida, resumen, cambios)

    print(f"  {ea} {resumen[f'eficientes_{ea}']:5d} | {eb} {resumen[f'eficientes_{eb}']:5d}"
          f" | comparadas {resumen['ventanas_comparadas']:5d}"
          f" | cambian {resumen['cambian']:4d}"
          f" | {','.join(resumen['terminos']) or '-'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
