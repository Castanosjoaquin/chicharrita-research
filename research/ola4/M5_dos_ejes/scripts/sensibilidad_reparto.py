"""M5: en que fraccion del espacio de repartos se sostiene cada afirmacion publicada.

NO elige un reparto. Barre el unico parametro que D47 deja abierto y que decide el
usuario —cuanta **exposicion** conserva *Homalodisca vitripennis*— y mide, en cada punto
de ese barrido, la fraccion de sorteos en la que cada afirmacion ya publicada se
sostiene. Un resultado que diga «el tercer puesto se da vuelta en la mitad de los
repartos» vale igual que el contrario.

El parametro es **rho = w_exposicion(H. vitripennis) / w_exposicion(maiz)**, que es la
forma en que D18 lo fijo (0,60) y la forma en que D47 lo propone (0,00). En cada rho se
sortean los pesos de las otras seis referencias con el mismo Dirichlet(1,...,1) del
barrido de W7 y los tres pesos de criterio con el mismo Dirichlet ordenado, y
`w_exposicion(H. vitripennis)` se fija en rho veces el peso sorteado del maiz.

El eje de conservacion **no entra** a ninguna de estas cuentas: se reporta aparte, por
region, en `dos_ejes_por_region.tsv`.

Las anclas de `anclas.py` corren primero y abortan el proceso si fallan.

    python research/ola4/M5_dos_ejes/scripts/sensibilidad_reparto.py --muestras 2000
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import anclas                     # noqa: E402
import ejes_separados as E        # noqa: E402
import ranking as R               # noqa: E402
import ranking_v2 as V            # noqa: E402

SALIDA = RAIZ / "research/ola4/M5_dos_ejes/resultados"
HV = "GCF_021130785.1_UT_GWSS_2.1_rna"
MAIZ = "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna"
OTRAS = [r for r in E.PANEL_EJES if r != HV]
RHOS = [0.00, 0.05, 0.10, 0.20, 0.30, 0.45, 0.60, 0.80, 1.00]
FORMAS = [("geometrica", "absoluta"), ("geometrica", "minmax"),
          ("suma", "absoluta"), ("suma", "minmax"), ("cascada", "absoluta")]
REGLAS = [("conservadora", False), ("mecanicista", True)]
# La region mas conservada de `ATPaseD_Dm`, descartada por D25 (alternativa b) porque
# esta vetada. Es la primera candidata a volver a la mesa si el veto se debilita.
D25_ALT_B = ("ATPaseD_Dm", (137, 436))


def pesos_exposicion(rng, rho: float) -> dict[str, float]:
    """Un sorteo del vector de exposicion con rho fijo."""
    w = {r: float(x) for r, x in zip(OTRAS, rng.dirichlet(np.ones(len(OTRAS))))}
    w[HV] = rho * w[MAIZ]
    return w


def pesos_criterio(rng) -> dict[str, float]:
    wc = np.sort(rng.dirichlet(np.ones(3)))[::-1]
    return {c: float(x) for c, x in zip(R.CRITERIOS, wc)}


def conjuntos_de(cands, genes, w_base, ciego: bool = False) -> dict[str, list[dict]]:
    """Los cinco conjuntos del JSON publicado, con las recomendadas reelegidas en w_base.

    `ciego` reelige con la regla de veto de hoy —todas las referencias del panel vetan,
    tenga el peso que tenga— para que la rama de comparacion no mezcle dos cambios.
    """
    _, wc = R.pesos_base()
    g = genes if ciego else E.vista(genes, w_base)
    rec = V.recomendadas([dict(c) for c in cands], g, w_base, wc)
    return {"los_seis": cands,
            "insecto": [c for c in cands if c["estrategia"] == "insecto"],
            "virus": [c for c in cands if c["estrategia"] == "virus"],
            "los_seis_recomendados": rec,
            "insecto_recomendados": [c for c in rec if c["estrategia"] == "insecto"]}


def barrer(conj: dict, genes: dict, rho: float, muestras: int, semilla: int,
           regla_veto: str) -> dict:
    """Frecuencias por posicion y por par, en todas las formas, reglas y escalas."""
    out = {}
    for forma, escala in FORMAS:
        for regla, solo in REGLAS:
            clave = ("%s/%s" % (forma, regla) if forma == "cascada"
                     else "%s/%s/%s" % (forma, regla, escala))
            for nombre, cands in conj.items():
                rng = np.random.default_rng(semilla)
                nombres = [c["gen"] for c in cands]
                frec = {n: [0] * len(nombres) for n in nombres}
                pares = {(a, b): 0 for a in nombres for b in nombres if a < b}
                ordenes: dict[tuple, int] = {}
                g = (E.vista(genes, {r: 1.0 for r in E.PANEL_EJES}) if regla_veto == "ciego"
                     else None)
                for _ in range(muestras):
                    w = pesos_exposicion(rng, rho)
                    wc = pesos_criterio(rng)
                    w_ef = float(rng.random())
                    gg = g if g is not None else E.vista(genes, w)
                    orden = R.ordenar(cands, gg, w_ef, w, wc, forma, solo, "off", escala)
                    pos = {n: i for i, (n, _) in enumerate(orden)}
                    for n, i in pos.items():
                        frec[n][i] += 1
                    for (a, b) in pares:
                        if pos[a] < pos[b]:
                            pares[(a, b)] += 1
                    cl = tuple(n for n, _ in orden)
                    ordenes[cl] = ordenes.get(cl, 0) + 1
                out.setdefault(nombre, {})[clave] = {
                    "frecuencia": {n: [round(100.0 * v / muestras, 1) for v in frec[n]]
                                   for n in nombres},
                    "pares_pct": {"%s>%s" % (a, b): round(100.0 * v / muestras, 1)
                                  for (a, b), v in pares.items()},
                    "ordenes": sorted(({"orden": list(k),
                                        "pct": round(100.0 * v / muestras, 1)}
                                       for k, v in ordenes.items()), key=lambda d: -d["pct"]),
                    "muestras": muestras}
    return out


def vetos_por_rho(genes: dict, cands: list[dict], w_base: dict, rho: float) -> list[dict]:
    """Que regiones estan vetadas y cuantas escapan al veto, con ese reparto."""
    filas = []
    g = E.vista(genes, w_base)
    por_gen = {c["gen"]: c for c in cands}
    for c in cands:
        gen = c["gen"]
        ini, fin = c["region"]
        largo = fin - ini + 1
        excl = R.excluidas_de(c, "off")
        n_reg = genes[gen]["n"] - largo + 1
        escapan = sum(1 for i in range(1, n_reg + 1)
                      if not E.veto(g[gen], i, i + largo - 1, w_base, excl))
        filas.append({"rho": rho, "gen": gen, "region": "%d-%d" % (ini, fin),
                      "vetada": E.veto(g[gen], ini, fin, w_base, excl),
                      "vetada_regla_actual": E.veto(genes[gen], ini, fin, None, excl),
                      "regiones_posibles": n_reg, "regiones_sin_veto": escapan})
    gen, (ini, fin) = D25_ALT_B
    excl = R.excluidas_de(por_gen[gen], "off")
    filas.append({"rho": rho, "gen": gen + " (D25 alt. b)", "region": "%d-%d" % (ini, fin),
                  "vetada": E.veto(g[gen], ini, fin, w_base, excl),
                  "vetada_regla_actual": E.veto(genes[gen], ini, fin, None, excl),
                  "regiones_posibles": None, "regiones_sin_veto": None})
    return filas


def tabla_dos_ejes(genes: dict, cands: list[dict], rho_prop: float = 0.00) -> list[dict]:
    """Los DOS numeros por region, mas los conteos que los sostienen."""
    w = E.vector_exposicion(tau_hv=rho_prop * E.PANEL_EJES[MAIZ]["w_exposicion"])
    s = E.vector_conservacion()
    _, wc = R.pesos_base()
    filas = []
    extra = dict(next(c for c in cands if c["gen"] == D25_ALT_B[0]))
    extra["region"] = D25_ALT_B[1]
    extra["etiqueta"] = "D25 alternativa b"
    for c in list(cands) + [extra]:
        d = E.dos_ejes(genes, c, w, s, wc)
        exp, cons = d.como_par()
        det = d.detalle
        cons_ref = det["conservacion_por_referencia"].get("H_vitripennis", {})
        filas.append({
            "gen": c["gen"], "etiqueta": c.get("etiqueta", "region del ranking v2"),
            "region": det["region"], "n_ventanas": det["n_ventanas"],
            "eficientes": det["eficientes"],
            "eje_exposicion": round(exp, 6), "eje_conservacion": round(cons, 6),
            "exposicion_detalle": json.dumps(det["exposicion_por_referencia"],
                                             ensure_ascii=False, sort_keys=True),
            "conservacion_perfecto_21": cons_ref.get("perfecto_21", 0),
            "conservacion_perfecto_ge19": cons_ref.get("perfecto_ge19", 0),
            "conservacion_mm1_21": cons_ref.get("mm1_21", 0),
            "vetada_por_exposicion": det["vetada_por_exposicion"],
            "vetada_regla_actual": det["vetada_regla_actual"]})
    return filas


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--muestras", type=int, default=2000)
    ap.add_argument("--semilla", type=int, default=7)
    a = ap.parse_args()

    t0 = time.time()
    # Las anclas corren SIEMPRE con los 2.000 sorteos y la semilla 7 con los que se
    # publico `ranking_v2.json`: son una reproduccion exacta, no una medicion propia, y
    # con otro numero de sorteos no pueden coincidir. `--muestras` solo mueve el barrido.
    anc = anclas.correr(muestras=2000, semilla=7)
    genes, cands = anc["genes"], anc["candidatos"]
    print("anclas pasadas (%d + %d comparaciones), %.0fs"
          % (len(anc["a1"]), len(anc["a2"]), time.time() - t0), flush=True)

    SALIDA.mkdir(parents=True, exist_ok=True)
    res = {"rho": {}, "muestras": a.muestras, "semilla": a.semilla,
           "definicion_rho": "w_exposicion(H. vitripennis) / w_exposicion(maiz); "
                             "D18 = 0,60, propuesta de D47 = 0,00",
           "publicado": {n: {k: v["frecuencia"] for k, v in d.items()}
                         for n, d in anc["publicado"]["barridos"].items()}}
    vetos, recomendadas = [], []
    for rho in RHOS:
        t1 = time.time()
        w_base = E.vector_exposicion(tau_hv=rho * E.PANEL_EJES[MAIZ]["w_exposicion"])
        conj = conjuntos_de(cands, genes, w_base)
        res["rho"]["%.2f" % rho] = barrer(conj, genes, rho, a.muestras, a.semilla,
                                          "exposicion")
        vetos.extend(vetos_por_rho(genes, cands, w_base, rho))
        for nombre in ("los_seis_recomendados",):
            for c in conj[nombre]:
                recomendadas.append({"rho": rho, "gen": c["gen"],
                                     "region_recomendada": "%d-%d" % c["region"]})
        print("  rho=%.2f  %.0fs" % (rho, time.time() - t1), flush=True)

    # Con rho = 0 y la regla de veto de HOY (ciega al peso): aisla cuanto del cambio
    # viene de la ponderacion y cuanto de que el veto deje de mirar a una referencia
    # sin exposicion.
    conj0 = conjuntos_de(cands, genes, E.vector_exposicion(tau_hv=0.0), ciego=True)
    res["rho_0_veto_ciego"] = barrer(conj0, genes, 0.0, a.muestras, a.semilla, "ciego")

    (SALIDA / "sensibilidad_reparto.json").write_text(
        json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")

    filas = []
    for rho, d in res["rho"].items():
        for conjunto, porclave in d.items():
            for clave, r in porclave.items():
                for par, pct in r["pares_pct"].items():
                    filas.append({"rho": rho, "conjunto": conjunto, "combinacion": clave,
                                  "tipo": "par", "afirmacion": par, "pct": pct,
                                  "muestras": r["muestras"]})
                filas.append({"rho": rho, "conjunto": conjunto, "combinacion": clave,
                              "tipo": "orden_modal",
                              "afirmacion": " > ".join(r["ordenes"][0]["orden"]),
                              "pct": r["ordenes"][0]["pct"], "muestras": r["muestras"]})
                for gen, f in r["frecuencia"].items():
                    for i, p in enumerate(f):
                        if p:
                            filas.append({"rho": rho, "conjunto": conjunto,
                                          "combinacion": clave, "tipo": "posicion",
                                          "afirmacion": "%s en el puesto %d" % (gen, i + 1),
                                          "pct": p, "muestras": r["muestras"]})
    with (SALIDA / "sensibilidad_reparto.tsv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]), delimiter="\t")
        w.writeheader()
        w.writerows(filas)

    with (SALIDA / "vetos_por_reparto.tsv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(vetos[0]), delimiter="\t")
        w.writeheader()
        w.writerows(vetos)

    with (SALIDA / "regiones_recomendadas_por_reparto.tsv").open(
            "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(recomendadas[0]), delimiter="\t")
        w.writeheader()
        w.writerows(recomendadas)

    dos = tabla_dos_ejes(genes, cands)
    with (SALIDA / "dos_ejes_por_region.tsv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(dos[0]), delimiter="\t")
        w.writeheader()
        w.writerows(dos)

    print("escritas %d filas de sensibilidad en %s  (%.0fs en total)"
          % (len(filas), SALIDA.relative_to(RAIZ), time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
