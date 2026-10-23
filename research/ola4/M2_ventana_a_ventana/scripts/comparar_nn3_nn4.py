"""El par `RNA_NN3` contra `RNA_NN4` de la linea M2, que era el insumo que faltaba.

Por que estaba pendiente. De los cuatro pares de M2, tres se podian armar con TSV ya
publicados; este no, porque `RNA_NN4` es la tabla propia de `sifi21INTA` y es la unica
que **no** sale de Biopython. Sin el fuente del INTA en la maquina no habia de donde
sacarla, y quedo declarado como insumo faltante y no como pregunta para el investigador.
El fuente estaba en `work/C2/sifi21INTA/` (commit 92df4449, archivos del 2024-03-27),
asi que la tabla se transcribio al port --verificada celda por celda contra
`freeEnergy.py:61-74`-- y el par se pudo correr.

Que hace: compara dos TSV por ventana del port que difieren solo en la tabla de
apilamiento, y para cada ventana que cambia de clase informa **que termino cruzo el
corte**, que es lo que vuelve util a la comparacion. Un conteo que cambia no dice nada;
una ventana que cambia porque su `ddg` paso de 1,0561 a 0,9885 y cruzo el umbral de 1,0,
si.

    python3 research/ola4/M2_ventana_a_ventana/scripts/comparar_nn3_nn4.py \\
            --nn3 <dir_nn3> --nn4 <dir_nn4> --salida <dir>

Los dos directorios se generan con el port:

    python3 tools/sifi21_port/run_sifi.py <fasta...> --modo fiel --backend vienna \\
            --salida <dir_nn3>
    python3 tools/sifi21_port/run_sifi.py <fasta...> --modo fiel --backend vienna \\
            --salida <dir_nn4> --tabla-nn NN4
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

GENES = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]
MODOS = ["fiel", "corregido"]
# Los cuatro booleanos del veredicto, en el orden en que el motor los evalua.
BOOLEANOS = ["strand_selection", "end_stability", "target_site_accessibility",
             "thermo_efficient"]
CONTINUOS = ["dg_sense5", "dg_antisense5", "ddg", "accessibility"]


def leer(ruta: Path) -> dict[int, dict]:
    with ruta.open(encoding="utf-8") as fh:
        filas = {int(r["pos"]): r for r in csv.DictReader(fh, delimiter="\t")}
    if not filas:
        raise SystemExit(f"{ruta}: vacio")
    return filas


def comparar(a: dict[int, dict], b: dict[int, dict]) -> tuple[dict, list[dict]]:
    """Matriz de confusion y lista de posiciones que cambian, con el termino que cruzo."""
    if set(a) != set(b):
        raise SystemExit("los dos TSV no cubren las mismas posiciones")

    conf = {"ambos_si": 0, "ambos_no": 0, "solo_nn3": 0, "solo_nn4": 0}
    cambios: list[dict] = []
    for pos in sorted(a):
        ea = a[pos]["is_efficient"] == "True"
        eb = b[pos]["is_efficient"] == "True"
        if ea and eb:
            conf["ambos_si"] += 1
        elif not ea and not eb:
            conf["ambos_no"] += 1
        elif ea:
            conf["solo_nn3"] += 1
        else:
            conf["solo_nn4"] += 1
        if ea == eb:
            continue
        fila = {
            "pos": pos,
            "nn3": ea,
            "nn4": eb,
            "terminos_que_cruzan": ",".join(
                c for c in BOOLEANOS if a[pos][c] != b[pos][c]
            ),
            "rama_terminal": a[pos].get("rama_terminal", ""),
        }
        for c in CONTINUOS:
            va, vb = float(a[pos][c]), float(b[pos][c])
            fila[f"{c}_nn3"] = round(va, 6)
            fila[f"{c}_nn4"] = round(vb, 6)
            fila[f"{c}_delta"] = round(vb - va, 6)
        cambios.append(fila)
    return conf, cambios


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--nn3", required=True, type=Path)
    ap.add_argument("--nn4", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    a = ap.parse_args()
    a.salida.mkdir(parents=True, exist_ok=True)

    resumen: dict[str, dict] = {}
    todas: list[dict] = []
    for gen in GENES:
        for modo in MODOS:
            f3 = [p for p in sorted(a.nn3.glob(f"{gen}*_{modo}_*.tsv"))
                  if "_nn4" not in p.name and "_features" not in p.name]
            f4 = [p for p in sorted(a.nn4.glob(f"{gen}*_{modo}_*_nn4.tsv"))
                  if "_features" not in p.name]
            if not f3 or not f4:
                continue
            conf, cambios = comparar(leer(f3[0]), leer(f4[0]))
            resumen[f"{gen}:{modo}"] = {
                "ventanas": sum(conf.values()),
                "eficientes_nn3": conf["ambos_si"] + conf["solo_nn3"],
                "eficientes_nn4": conf["ambos_si"] + conf["solo_nn4"],
                "confusion": conf,
                "cambian": len(cambios),
                "terminos": sorted(
                    {t for c in cambios for t in c["terminos_que_cruzan"].split(",") if t}
                ),
            }
            for c in cambios:
                todas.append({"gen": gen, "modo": modo, **c})

    if not resumen:
        raise SystemExit("no se encontraron pares de TSV")

    (a.salida / "par_nn3_nn4_resumen.json").write_text(
        json.dumps(resumen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    if todas:
        cols = list(todas[0].keys())
        with (a.salida / "par_nn3_nn4_cambios.tsv").open("w", encoding="utf-8", newline="") as fh:
            fh.write("\t".join(cols) + "\n")
            for f in todas:
                fh.write("\t".join(str(f.get(c, "")) for c in cols) + "\n")

    print(f"{'gen':12s} {'modo':10s} {'NN3':>5s} {'NN4':>5s} {'cambian':>8s}  terminos")
    for clave, d in resumen.items():
        gen, modo = clave.split(":")
        print(f"{gen:12s} {modo:10s} {d['eficientes_nn3']:5d} {d['eficientes_nn4']:5d} "
              f"{d['cambian']:8d}  {','.join(d['terminos']) or '-'}")
    print(f"\nescrito en {a.salida}: par_nn3_nn4_resumen.json y par_nn3_nn4_cambios.tsv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
