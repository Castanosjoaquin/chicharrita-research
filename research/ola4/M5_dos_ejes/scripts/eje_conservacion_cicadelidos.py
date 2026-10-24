"""El eje de conservacion con DOS cicadelidos, medido como sensibilidad (no adoptado).

Por que. D47 parte el peso de D18 en exposicion y conservacion. Eso reabre **D23**, que
saco a *Macrosteles quadrilineatus* del panel con un argumento **de exposicion** —«la
especie no esta en Argentina y por lo tanto no es un organismo expuesto»— y que ya
anotaba que se lo habia incorporado «como sustituto filogenetico del resto de los
Deltocephalinae, no por exposicion directa, y ese uso no se descarta con su ausencia en
Argentina». Con los dos ejes separados, la ausencia en la Argentina lo saca del eje de
exposicion y **no** del de conservacion.

Esta medicion NO lo agrega al panel ni mueve ningun numero de orden: el eje de
exposicion no lo ve (su `w_exposicion` es cero y la vista de exposicion lo filtra). Lo
que se mide es cuanto cambia el **segundo numero** de cada region al pasar de un
cicadelido a dos.

Anclas del tamizaje, contra numeros ya publicados que no son de esta linea:
  * `BicC_Dm` gen entero: 101 ventanas con 21/21 contra *Macrosteles*
    (`research/ola3/C6_panel_y_largo/REPORT.md`).
  * `BicC_Dm` 2123-2422: 19 ventanas; la region de EPILAB 264-563: 10 (idem).
  * `ATPaseD_Dm`: las dos regiones contienen las mismas 12 ventanas (idem).
  * `eth_Dm` gen entero: 21 ventanas con 21/21 (D23, consecuencia).
Si alguna falla, aborta.

Todo conteo va en dos cifras por D59: total y de baja complejidad.

    python research/ola4/M5_dos_ejes/scripts/eje_conservacion_cicadelidos.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import anclas                     # noqa: E402
import ejes_separados as E        # noqa: E402
import ranking as R               # noqa: E402
import ranking_v2 as V            # noqa: E402
from sifi_plus.complejidad import es_baja  # noqa: E402

TRABAJO = RAIZ / "work" / "sifi_v2"
SALIDA = RAIZ / "research/ola4/M5_dos_ejes/resultados"
MQ = "Macrosteles_quadrilineatus_rna"
INFO_MQ = {"corto": "M_quadrilineatus", "especie": "Macrosteles quadrilineatus",
           "rol": "cicadelido no objetivo, fuera del panel por D23 (argumento de "
                  "exposicion); entra solo al eje de conservacion",
           "peso": 0.00}
HV = "GCF_021130785.1_UT_GWSS_2.1_rna"
ANCLAS = [("BicC_Dm", None, 101), ("BicC_Dm", (2123, 2422), 19), ("BicC_Dm", (264, 563), 10),
          ("ATPaseD_Dm", (151, 450), 12), ("ATPaseD_Dm", (72, 371), 12),
          ("eth_Dm", None, 21)]


def cargar_mq(genes: dict) -> None:
    """Suma la columna de *Macrosteles* al dato de cada gen, como una referencia mas."""
    ruta = TRABAJO / "offtarget_cicadelidos_k21" / "offtarget_por_sirna.tsv"
    if not ruta.exists():
        sys.exit("falta %s: correr reconstruir_insumos.py --paso conservacion" % ruta)
    R.REFERENCIAS[MQ] = INFO_MQ
    for gen, g in genes.items():
        for clave, vec in R.leer_offtarget(ruta, "%s_full" % gen, g["n"]).items():
            ref, crit = clave.split("|")
            g["riesgo"].setdefault(MQ, {})[crit] = vec
        for crit in R.CRITERIOS:
            g["riesgo"][MQ].setdefault(crit, np.zeros(g["n"], dtype=bool))


def main() -> int:
    anc = anclas.correr(verboso=False)
    genes, cands = anc["genes"], anc["candidatos"]
    cargar_mq(genes)

    rotas = []
    for gen, region, esperado in ANCLAS:
        v = genes[gen]["riesgo"][MQ]["perfecto_21"]
        got = int(v.sum() if region is None else v[region[0] - 1:region[1]].sum())
        if got != esperado:
            rotas.append("%s %s: %d contra %d publicado" % (gen, region or "gen entero",
                                                            got, esperado))
    if rotas:
        sys.exit("ANCLAS ROTAS del tamizaje contra Macrosteles:\n  " + "\n  ".join(rotas))
    print("anclas del tamizaje contra Macrosteles: %d de %d reproducen C6 y D23"
          % (len(ANCLAS), len(ANCLAS)))

    # Las secuencias, para el control de D59 sobre este conteo
    seqs = {}
    with (TRABAJO / "offtarget_cicadelidos_k21" / "offtarget_por_sirna.tsv").open(
            encoding="utf-8") as fh:
        for f in csv.DictReader(fh, delimiter="\t"):
            seqs.setdefault(f["consulta"].replace("_full", ""), {})[int(f["pos"])] = f["sirna"]

    w = E.vector_exposicion()                       # sin cambios: Mq no entra al panel
    s1 = E.vector_conservacion()                    # un cicadelido
    s2 = dict(s1, **{MQ: 1.00})                     # dos cicadelidos
    _, wc = R.pesos_base()
    extra = dict(next(c for c in cands if c["gen"] == "ATPaseD_Dm"))
    extra["region"] = (137, 436)
    extra["etiqueta"] = "D25 alternativa b"

    filas = []
    for c in list(cands) + [extra]:
        gen, (ini, fin) = c["gen"], c["region"]
        d1 = E.dos_ejes(genes, c, w, s1, wc)
        d2 = E.dos_ejes(genes, c, w, s2, wc)
        det1, det2 = d1.detalle, d2.detalle
        hv = det1["conservacion_por_referencia"].get("H_vitripennis", {})
        mq = det2["conservacion_por_referencia"].get("M_quadrilineatus", {})
        pos_mq = [p for p in range(ini, fin + 1)
                  if genes[gen]["riesgo"][MQ]["perfecto_21"][p - 1]]
        pos_hv = [p for p in range(ini, fin + 1)
                  if genes[gen]["riesgo"][HV]["perfecto_21"][p - 1]]
        filas.append({
            "gen": gen, "etiqueta": c.get("etiqueta", "region del ranking v2"),
            "region": "%d-%d" % (ini, fin),
            "eje_exposicion": round(d1.exposicion.valor_de("exposicion"), 6),
            "eje_conservacion_1_cicadelido": round(d1.conservacion.valor_de("conservacion"), 6),
            "eje_conservacion_2_cicadelidos": round(d2.conservacion.valor_de("conservacion"), 6),
            "Hv_perfecto_21": hv.get("perfecto_21", 0),
            "Hv_perfecto_21_baja_complejidad": sum(1 for p in pos_hv if es_baja(seqs[gen][p])),
            "Hv_perfecto_ge19": hv.get("perfecto_ge19", 0),
            "Mq_perfecto_21": mq.get("perfecto_21", 0),
            "Mq_perfecto_21_baja_complejidad": sum(1 for p in pos_mq if es_baja(seqs[gen][p])),
            "Mq_perfecto_ge19": mq.get("perfecto_ge19", 0),
            "ventanas_en_algun_cicadelido": len(set(pos_hv) | set(pos_mq)),
            "ventanas_en_los_dos": len(set(pos_hv) & set(pos_mq))})

    SALIDA.mkdir(parents=True, exist_ok=True)
    with (SALIDA / "eje_conservacion_cicadelidos.tsv").open("w", newline="",
                                                            encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(filas[0]), delimiter="\t")
        wr.writeheader()
        wr.writerows(filas)
    (SALIDA / "eje_conservacion_cicadelidos.json").write_text(json.dumps(
        {"anclas": [{"gen": g, "region": r, "publicado": e} for g, r, e in ANCLAS],
         "nota": "Macrosteles quadrilineatus entra SOLO al eje de conservacion; su "
                 "w_exposicion es cero y la vista de exposicion lo filtra, de modo que "
                 "ningun numero de orden cambia. D23 lo saco del panel por exposicion.",
         "filas": filas}, indent=1, ensure_ascii=False), encoding="utf-8")

    print("\n%-12s%-20s%-11s%12s%12s%10s%10s" % ("gen", "etiqueta", "region", "conserv 1",
                                                 "conserv 2", "Hv 21/21", "Mq 21/21"))
    for f in filas:
        print("%-12s%-20s%-11s%12.4f%12.4f%10d%10d" % (
            f["gen"], f["etiqueta"][:19], f["region"], f["eje_conservacion_1_cicadelido"],
            f["eje_conservacion_2_cicadelidos"], f["Hv_perfecto_21"], f["Mq_perfecto_21"]))
    print("\nbaja complejidad (D59): %d de %d ventanas 21/21 contra los dos cicadelidos"
          % (sum(f["Hv_perfecto_21_baja_complejidad"] + f["Mq_perfecto_21_baja_complejidad"]
                 for f in filas),
             sum(f["Hv_perfecto_21"] + f["Mq_perfecto_21"] for f in filas)))
    print("escrito en %s" % (SALIDA / "eje_conservacion_cicadelidos.tsv").relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
