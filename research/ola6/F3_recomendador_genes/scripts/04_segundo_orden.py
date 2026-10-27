#!/usr/bin/env python3
"""Paso 5 de F3 — el segundo orden: ¿cambia el orden segun el objetivo?

La pregunta
-----------
«Matar o esterilizar» viene abierta desde el checkpoint 2 y el issue #27 decia que `F3` es
lo que la volveria decidible. El orden de `03_orden.py` **no** la contesta, y el `REPORT.md`
§6 dice por que: el eje de fenotipo puntua la *fuerza de la evidencia* —`F3` medido en
*D. maidis* con `[E]`, `F2` `[E]` en otra especie, `F1` `[R]`— y los mecanismos viajan como
columna sin entrar al puntaje. Asi que el orden sale igual quiera uno matar o esterilizar.

Lo que hace este script
-----------------------
Corre **el mismo criterio dos veces**, filtrando por mecanismo en vez de promediarlo:

  objetivo «matar»       -> solo los candidatos cuyo mecanismo incluye `letalidad`
  objetivo «esterilizar» -> solo los candidatos cuyo mecanismo incluye `reproduccion`

Todo lo demas es idéntico: los pesos de `D87`, las dos escalas, las cohortes por ejes
disponibles y el umbral de empate de 0,05. **Los puntajes no se recalculan** —no dependen del
mecanismo— asi que cada orden es una subsecuencia del orden global. Lo que cambia es *quien es
elegible*, y por lo tanto quien queda primero.

La regla de lectura, declarada antes de mirar el resultado
----------------------------------------------------------
El orden **cambia segun el objetivo** si y solo si el grupo del primer puesto de la cohorte A
no es el mismo conjunto en los dos objetivos. Si es el mismo, la respuesta a la pregunta
abierta es «no cambia», y eso tambien es una respuesta. No se mira ningun otro puesto para
decidirlo: una diferencia en el medio de la tabla no es lo que la pregunta pide.

Un candidato con los dos mecanismos aparece en los dos ordenes, y eso es correcto: `DE-05`
tiene letalidad, reproduccion y transmision medidas a la vez.

Uso:
    python research/ola6/F3_recomendador_genes/scripts/04_segundo_orden.py
"""

import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
BLOQUE = Path(__file__).resolve().parents[1]

PESOS_D87 = {"fenotipo": 0.40, "esencialidad": 0.25}
UMBRAL_EMPATE = 0.05

OBJETIVOS = {
    "matar": {
        "mecanismo_exigido": "letalidad",
        "glosa": "reducir la poblacion matando al vector dentro de la temporada",
    },
    "esterilizar": {
        "mecanismo_exigido": "reproduccion",
        "glosa": "reducir la poblacion entre generaciones, sin cortar la transmision "
                 "de la temporada en curso (es la lectura del fenotipo de BicC que el "
                 "investigador confirmo)",
    },
}


def agrupar_por_empate(cohorte: list) -> list:
    """Grupos consecutivos a menos de UMBRAL_EMPATE del primero del grupo (no en cadena)."""
    grupos, actual = [], []
    for r in sorted(cohorte, key=lambda r: (-r["puntaje"], r["id"])):
        if actual and abs(actual[0]["puntaje"] - r["puntaje"]) >= UMBRAL_EMPATE:
            grupos.append(actual)
            actual = []
        actual.append(r)
    if actual:
        grupos.append(actual)
    return grupos


def ordenar(candidatos: list) -> dict:
    """Mismo criterio que 03_orden.py: cohortes por ejes disponibles y pesos renormalizados."""
    coh_a = [r for r in candidatos if r["eje2_puntaje"]]
    coh_b = [r for r in candidatos if not r["eje2_puntaje"]]
    base = PESOS_D87["fenotipo"] + PESOS_D87["esencialidad"]
    w_f, w_e = PESOS_D87["fenotipo"] / base, PESOS_D87["esencialidad"] / base
    for r in coh_a:
        r["puntaje"] = w_f * float(r["eje1_puntaje"]) + w_e * float(r["eje2_puntaje"])
    for r in coh_b:
        r["puntaje"] = float(r["eje1_puntaje"])
    salida = {}
    for nombre, cohorte in (("A", coh_a), ("B", coh_b)):
        grupos = agrupar_por_empate(cohorte)
        puesto, filas = 0, []
        for g in grupos:
            puesto += 1
            for r in g:
                filas.append({**r, "puesto": puesto,
                              "empate_con": [x["id"] for x in g if x is not r]})
            puesto += len(g) - 1
        salida[nombre] = {"filas": filas,
                          "primer_puesto": sorted(x["id"] for x in grupos[0]) if grupos else []}
    return salida


def main() -> int:
    with (BLOQUE / "resultados/orden_genes.tsv").open(encoding="utf-8") as fh:
        global_ = list(csv.DictReader(fh, delimiter="\t"))

    resultados, filas_salida = {}, []
    for nombre, cfg in OBJETIVOS.items():
        elegibles = [dict(r) for r in global_
                     if cfg["mecanismo_exigido"] in r["mecanismos"].split("|")]
        orden = ordenar(elegibles)
        resultados[nombre] = orden
        for coh, datos in orden.items():
            for r in datos["filas"]:
                filas_salida.append({
                    "objetivo": nombre,
                    "mecanismo_exigido": cfg["mecanismo_exigido"],
                    "cohorte": coh,
                    "puesto_en_su_cohorte": r["puesto"],
                    "empate_declarado_con": "|".join(r["empate_con"]) or "no",
                    "id": r["id"], "gen": r["gen"], "especie": r["especie"],
                    "puntaje": f"{r['puntaje']:.4f}",
                    "eje1_nivel": r["eje1_nivel"], "eje2_nivel": r["eje2_nivel"],
                    "mecanismos_del_candidato": r["mecanismos"],
                    "aparece_en_los_dos_objetivos":
                        "si" if ("letalidad" in r["mecanismos"].split("|")
                                 and "reproduccion" in r["mecanismos"].split("|")) else "no",
                })

    salida = BLOQUE / "resultados/segundo_orden.tsv"
    with salida.open("w", encoding="utf-8", newline="") as fh:
        esc = csv.DictWriter(fh, fieldnames=list(filas_salida[0]), delimiter="\t",
                             lineterminator="\n")
        esc.writeheader()
        esc.writerows(filas_salida)

    primero_matar = resultados["matar"]["A"]["primer_puesto"]
    primero_ester = resultados["esterilizar"]["A"]["primer_puesto"]
    cambia = primero_matar != primero_ester

    meta = {
        "pregunta": "¿cambia el orden de los candidatos del insecto segun el objetivo?",
        "regla_de_lectura_declarada_antes": (
            "cambia si y solo si el grupo del primer puesto de la cohorte A no es el mismo "
            "conjunto en los dos objetivos"),
        "criterio": "el mismo de D87 y de 03_orden.py; los puntajes NO se recalculan, solo "
                    "cambia quien es elegible",
        "objetivos": {k: {"mecanismo_exigido": v["mecanismo_exigido"], "glosa": v["glosa"],
                          "elegibles": sum(1 for f in filas_salida if f["objetivo"] == k),
                          "primer_puesto_cohorte_A": resultados[k]["A"]["primer_puesto"]}
                      for k, v in OBJETIVOS.items()},
        "respuesta": ("SI, el orden cambia segun el objetivo" if cambia
                      else "NO, el orden no cambia segun el objetivo"),
        "candidatos_en_los_dos_objetivos": sorted(
            {f["id"] for f in filas_salida if f["aparece_en_los_dos_objetivos"] == "si"}),
    }
    (BLOQUE / "resultados/segundo_orden_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    for nombre in OBJETIVOS:
        print(f"--- objetivo «{nombre}» (exige {OBJETIVOS[nombre]['mecanismo_exigido']}) ---")
        for coh in ("A", "B"):
            filas = resultados[nombre][coh]["filas"]
            print(f"  cohorte {coh}: {len(filas)} candidatos")
            for r in filas[:6]:
                emp = (f"  [empata con {', '.join(r['empate_con'])}]"
                       if r["empate_con"] else "")
                print(f"    {r['puesto']:>2}. {r['id']} {r['puntaje']:.4f} "
                      f"{r['eje1_nivel']}/{r['eje2_nivel']} {r['gen'][:24]}{emp}")
            if len(filas) > 6:
                print(f"       … y {len(filas) - 6} mas")
        print()
    print(f"primer puesto de A, matar      : {primero_matar}")
    print(f"primer puesto de A, esterilizar: {primero_ester}")
    print()
    print(f"RESPUESTA: {meta['respuesta']}")
    print(f"escrito: {salida.relative_to(RAIZ)}, segundo_orden_meta.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
