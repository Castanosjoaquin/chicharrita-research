#!/usr/bin/env python3
"""Resume, por estrategia (insecto / virus), cuanto del orden depende de la escala.

Lee resultados/ranking_v2.json (salida de tools/sifi21_port/ranking_v2.py) y NO recalcula
ningun puntaje: solo reagrupa los barridos ya guardados (2.000 sorteos de pesos por combinacion).
Escribe resultados/por_estrategia.json. Fase 1 del plan del checkpoint 2.
"""
import json, itertools, pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[1]
d = json.load(open(RAIZ / "resultados" / "ranking_v2.json"))

GRUPOS = {"insecto_recomendados": "insecto, regiones recomendadas",
          "insecto": "insecto, regiones de EPILAB",
          "virus": "virus, regiones de EPILAB"}

def pares(ordenes, cands):
    """P(a antes que b) desde la lista de ordenes completa; devuelve tambien la cobertura."""
    cobertura = sum(o["pct"] for o in ordenes)
    out = {}
    for a, b in itertools.combinations(cands, 2):
        p = sum(o["pct"] for o in ordenes if o["orden"].index(a) < o["orden"].index(b))
        out[f"{a}>{b}"] = round(p, 1)
    return out, round(cobertura, 1)

res = {}
for k in ("21", "22"):
    for g, etiqueta in GRUPOS.items():
        barr = d["k"][k]["barridos"][g]
        cands = list(next(iter(barr.values()))["frecuencia"].keys())
        filas = {}
        for comb, v in barr.items():
            pp, cob = pares(v["ordenes"], cands)
            filas[comb] = {"primero_pct": v["primero_pct"],
                           "orden_modal": v["ordenes"][0]["orden"],
                           "orden_modal_pct": v["ordenes"][0]["pct"],
                           "pares_pct": pp, "cobertura_ordenes_pct": cob}
        res[f"{g}|k{k}"] = {"grupo": etiqueta, "k": int(k), "candidatos": cands, "combinaciones": filas}

json.dump(res, open(RAIZ / "resultados" / "por_estrategia.json", "w"), ensure_ascii=False, indent=1)
print("escrito resultados/por_estrategia.json con", len(res), "bloques")
