"""Ranking v2: los cuatro de EPILAB mas los dos genes nuevos, a 21 y a 22 nt.

Reusa el motor de `ranking.py` sin tocarlo (los ejes, la media geometrica, la cascada, el
barrido de pesos y las regiones alternativas son los de W7) y agrega cuatro cosas:

  1. Dos candidatos nuevos de *Dalbulus maidis*, `eth` y `burs-alpha`, con la secuencia
     publica de la propia especie (GenBank PZ371507.1 y PZ371508.1, via C5). No tienen
     region elegida por el laboratorio: se les propone la mejor region de 200 nt por la
     misma cascada con la que W7 recomienda regiones para los otros.
  2. *Homo sapiens* como septima referencia del panel, con peso base 1,00. El
     investigador lo nombro en el checkpoint y C6 ya lo habia medido (cero 21/21).
     *Macrosteles quadrilineatus* NO entra: es una decision del equipo (D23), no un
     olvido, y queda declarada en el informe.
  3. El mismo ranking a 21 y a 22 nt, porque para hemipteros no hay perfil de largo
     publicado. Las columnas del TSV de off-targets se siguen llamando `perfecto_21`
     aunque k sea 22 (ver `offtarget_21nt.py`); el k efectivo lo da el directorio.
  4. Anclas: antes de medir nada nuevo se reproducen los numeros de W7 con el mismo
     motor (los cuatro conteos de eficientes y las frecuencias del barrido sobre los
     cuatro genes sin humano). Si algo no coincide, aborta.

Nada sale de la maquina: las referencias se leen de disco y las secuencias de EPILAB
nunca se suben a ningun servicio.

Uso:
    python ranking_v2.py --trabajo work/sifi_v2 \
        --json research/ola3/C7_ranking_v2/resultados/ranking_v2.json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ranking as R  # noqa: E402

HUMANO = "humano_rna"
INFO_HUMANO = {"corto": "humano", "especie": "Homo sapiens",
               "rol": "no objetivo de maxima consecuencia; lo nombro el investigador",
               "peso": 1.00}

# Los dos candidatos nuevos. No tienen region del laboratorio: `region` se completa
# con la propuesta de la cascada. `largo` es el de las regiones virales de EPILAB
# (200 nt), que cae en el rango 150-250 nt que el investigador declaro.
NUEVOS = [
    {"gen": "eth_Dm", "region": None, "largo": 200, "estrategia": "insecto",
     "organismo": "Dalbulus maidis", "funcion": "hormona disparadora de la ecdisis (ETH)",
     "genbank": "PZ371507.1"},
    {"gen": "bursA_Dm", "region": None, "largo": 200, "estrategia": "insecto",
     "organismo": "Dalbulus maidis", "funcion": "bursicon alfa (burs-alpha)",
     "genbank": "PZ371508.1"},
]
GENES_EPILAB = [c["gen"] for c in R.CANDIDATOS]
GENES_NUEVOS = [c["gen"] for c in NUEVOS]
ANCLAS_EFICIENTES_21 = {"MP_MRFV": 123, "CP_MRFV": 30, "BicC_Dm": 171, "ATPaseD_Dm": 29}


def con_panel(sin_humano: bool):
    """Fija el panel global de `ranking.py`. Sin humano es el de W7, para las anclas."""
    base = {k: v for k, v in R.REFERENCIAS.items() if k != HUMANO}
    R.REFERENCIAS = base if sin_humano else {**base, HUMANO: INFO_HUMANO}


def cargar(trabajo: Path, k: int, genes: list[str]) -> dict:
    """Perfil y matriz de riesgo por gen. El genoma de *D. maidis* se corre aparte (es el
    mas pesado) y se funde aca: para los genes virales cuenta como off-target (D5 de W7),
    para los del insecto es on-target y `excluidas_de` lo saca del calculo."""
    perfil = trabajo / ("salida_k%d" % k)
    off = trabajo / ("offtarget_k%d" % k) / "offtarget_por_sirna.tsv"
    dm = trabajo / ("offtarget_dm_k%d" % k) / "offtarget_por_sirna.tsv"
    out = {}
    for gen in genes:
        g = R.cargar_gen(gen, perfil, off, None)
        for clave, vec in R.leer_offtarget(dm, "%s_full" % gen, g["n"]).items():
            ref, crit = clave.split("|")
            g["riesgo"].setdefault(ref, {})[crit] = vec
        for ref in g["riesgo"]:
            for crit in R.CRITERIOS:
                g["riesgo"][ref].setdefault(crit, np.zeros(g["n"], dtype=bool))
        out[gen] = g
    return out


def quitar_humano(genes: dict) -> dict:
    """El mismo dato sin la columna de humano: el panel de W7, para aislar su efecto.

    Hay que sacarla de `riesgo` y no solo de los pesos, porque el veto y los conteos de
    la cascada miran todas las referencias presentes sin importar su peso."""
    out = {}
    for n, g in genes.items():
        h = dict(g)
        h["riesgo"] = {r: v for r, v in g["riesgo"].items() if r != HUMANO}
        out[n] = h
    return out


def ficha(g: dict, cand: dict, wr, wc) -> dict:
    """Los dos ejes con las dos reglas de D2, y el riesgo desglosado por referencia."""
    ini, fin = cand["region"]
    excl = R.excluidas_de(cand, "off")
    out = {"gen": cand["gen"], "region": "%d-%d" % (ini, fin), "largo_region": fin - ini + 1,
           "estrategia": cand["estrategia"], "eficientes_gen": int(g["eficiente"].sum()),
           "ventanas_gen": int(g["presente"].sum())}
    for regla, solo in (("mecanicista", True), ("conservadora", False)):
        e = R.ejes(g, ini, fin, wr, wc, excl, solo)
        out[regla] = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in e.items()}
        out[regla]["puntaje_geometrico_w05"] = round(R.puntaje(e, 0.5, "geometrica"), 4)
    por_ref = {}
    for ref, crits in g["riesgo"].items():
        if ref in excl:
            continue
        d = {}
        for crit in R.CRITERIOS:
            v = crits[crit][ini - 1:fin]
            if v.any():
                d[crit] = {"ventanas": int(v.sum()),
                           "de_esas_eficientes": int((v & g["eficiente"][ini - 1:fin]).sum())}
        if d:
            por_ref[R.corto(ref)] = d
    out["riesgo_por_referencia"] = por_ref
    return out


def gen_entero(g: dict, excl: set) -> dict:
    """El riesgo de la molecula completa. Para eth y burs-alpha es lo que tiene evidencia:
    el ARNdc publicado mide 544 y 578 pb, que es casi todo el gen."""
    n = g["n"]
    out = {"ventanas": int(g["presente"].sum()), "eficientes": int(g["eficiente"].sum()),
           "por_referencia": {}}
    for ref, crits in g["riesgo"].items():
        if ref in excl:
            continue
        d = {c: int(crits[c].sum()) for c in R.CRITERIOS if crits[c].any()}
        if d:
            d["perfecto_21_posiciones"] = [int(i + 1) for i in np.flatnonzero(crits["perfecto_21"])]
            d["perfecto_21_eficientes"] = int((crits["perfecto_21"] & g["eficiente"]).sum())
            out["por_referencia"][R.corto(ref)] = d
    return out


def completar_regiones(genes: dict, wr, wc, umbral=None, tabla=None) -> list[dict]:
    """Region propuesta para los nuevos: la mejor por cascada, igual que W7 recomienda.

    Pasa por `R.region_recomendada()`, o sea por la compuerta de alertas de D48: una
    region con una fila de alerta en «pendiente» no sale de aca (D69).
    """
    cands = []
    for c in R.CANDIDATOS:
        cands.append(dict(c))
    for c in NUEVOS:
        d = dict(c)
        d["region"] = (1, d["largo"])
        alt = R.alternativas(genes[d["gen"]], d["largo"], d, wr, wc, False, "off", 0.5,
                             "cascada")
        d["region"] = R.region_recomendada(alt, d["gen"], umbral, tabla)
        cands.append(d)
    return cands


def recomendadas(cands, genes, wr, wc, umbral=None, tabla=None) -> list[dict]:
    """Las regiones que el ranking recomienda, cada una pasada por la compuerta de D48."""
    out = []
    for c in cands:
        largo = c["region"][1] - c["region"][0] + 1
        alt = R.alternativas(genes[c["gen"]], largo, c, wr, wc, False, "off", 0.5, "cascada")
        d = dict(c)
        d["region"] = R.region_recomendada(alt, c["gen"], umbral, tabla)
        out.append(d)
    return out


def barridos(conjuntos: dict, genes, muestras, semilla, formas=("geometrica", "suma",
                                                                "cascada")) -> dict:
    res = {}
    for nombre, conj in conjuntos.items():
        res[nombre] = {}
        for forma in formas:
            for regla, s in (("mecanicista", True), ("conservadora", False)):
                for escala in ("absoluta", "minmax"):
                    if forma == "cascada" and escala == "minmax":
                        continue
                    r = R.barrer(conj, genes, forma, s, "off", muestras,
                                 np.random.default_rng(semilla), escala)
                    clave = ("%s/%s" % (forma, regla) if forma == "cascada"
                             else "%s/%s/%s" % (forma, regla, escala))
                    res[nombre][clave] = r
    return res


def nulo_gen(g: dict, largo: int, reps: int, semilla: int) -> dict:
    """Los dos nulos de W7 sobre un gen, para saber si elegir region discrimina ahi."""
    rng = np.random.default_rng(semilla)
    cuenta = R.conteo_por_region(g["eficiente"], largo)
    obs = int(cuenta.max())
    ne, _ = R.nulo_etiquetas(g["eficiente"], largo, reps, rng)
    nb, _ = R.nulo_bloques(g["eficiente"], largo, reps, rng)
    return {"largo_region": largo, "regiones_posibles": int(len(cuenta)),
            "eficientes_gen": int(g["eficiente"].sum()),
            "minimo": int(cuenta.min()), "p25": float(np.percentile(cuenta, 25)),
            "mediana": float(np.median(cuenta)), "p75": float(np.percentile(cuenta, 75)),
            "maximo": obs,
            "region_maxima": "%d-%d" % (int(cuenta.argmax()) + 1, int(cuenta.argmax()) + largo),
            "nulo_etiquetas_media": round(float(ne.mean()), 1),
            "nulo_etiquetas_z": round(float((obs - ne.mean()) / ne.std()), 2),
            "nulo_etiquetas_p": round(float((ne >= obs).mean()), 4),
            "nulo_bloques30_media": round(float(nb.mean()), 1),
            "nulo_bloques30_z": round(float((obs - nb.mean()) / nb.std()), 2),
            "nulo_bloques30_p": round(float((nb >= obs).mean()), 4)}


def jaccard(trabajo: Path, gen: str) -> dict:
    pos = {}
    for k in (21, 22):
        pos[k] = {int(f["pos"]) for f in csv.DictReader(
            open(trabajo / ("salida_k%d" % k) / ("%s_full_corregido_vienna.tsv" % gen)),
            delimiter="\t") if f["is_efficient"] == "True"}
    inter, uni = pos[21] & pos[22], pos[21] | pos[22]
    return {"k21": len(pos[21]), "k22": len(pos[22]), "en_ambos": len(inter),
            "solo_21": len(pos[21] - pos[22]), "solo_22": len(pos[22] - pos[21]),
            "jaccard": round(len(inter) / len(uni), 3) if uni else None}


def alternativas_de(cands, genes, wr, wc) -> dict:
    out = {}
    for c in cands:
        largo = c["region"][1] - c["region"][0] + 1
        out[c["gen"]] = {}
        for forma in ("geometrica", "cascada"):
            out[c["gen"]][forma] = R.alternativas(genes[c["gen"]], largo, c, wr, wc,
                                                  False, "off", 0.5, forma)
    return out


def verificar_anclas(trabajo: Path, w7_json: Path, muestras: int, semilla: int) -> dict:
    """Reproduce W7 con el motor de ahora. Aborta si algo no coincide."""
    res = {"eficientes_21nt": {}, "fichas": {}, "barrido": {}}
    genes = quitar_humano(cargar(trabajo, 21, GENES_EPILAB))
    for g, esp in ANCLAS_EFICIENTES_21.items():
        got = int(genes[g]["eficiente"].sum())
        res["eficientes_21nt"][g] = {"obtenido": got, "publicado": esp, "coincide": got == esp}
        if got != esp:
            sys.exit("ANCLA ROTA en %s: %d eficientes contra %d de W7." % (g, got, esp))
    w7 = json.loads(w7_json.read_text(encoding="utf-8"))
    con_panel(sin_humano=True)
    wr, wc = R.pesos_base()
    for c in R.CANDIDATOS:
        mia = ficha(genes[c["gen"]], c, wr, wc)["conservadora"]
        ref = next(x for x in w7["candidatos"] if x["gen"] == c["gen"])["conservadora"]
        ok = all(mia[k] == ref[k] for k in ("n_ventanas", "eficientes", "eficacia",
                                             "limpieza", "exposicion", "buenos_limpios",
                                             "con_off_target", "con_21_perfecto", "vetada"))
        res["fichas"][c["gen"]] = {"coincide": ok,
                                   "eficacia": mia["eficacia"], "exposicion": mia["exposicion"]}
        if not ok:
            sys.exit("ANCLA ROTA en la ficha de %s:\n  v2 %s\n  W7 %s" % (c["gen"], mia, ref))
    # El barrido: mismas semillas, mismo panel -> las frecuencias tienen que ser iguales.
    r = R.barrer(R.CANDIDATOS, genes, "geometrica", False, "off", muestras,
                 np.random.default_rng(semilla), "absoluta")
    esp = w7["barridos"]["los_cuatro"]["geometrica/conservadora/absoluta"]["frecuencia"]
    res["barrido"] = {"obtenido": r["frecuencia"], "w7": esp, "coincide": r["frecuencia"] == esp}
    if r["frecuencia"] != esp:
        sys.exit("ANCLA ROTA en el barrido: %s contra %s" % (r["frecuencia"], esp))
    con_panel(sin_humano=False)
    return res


def efecto_humano(trabajo: Path, semilla: int, muestras: int, w7_json: Path,
                  umbral=None, tabla=None) -> dict:
    """Que cambia, sobre los cuatro de EPILAB, por agregar humano al panel de W7."""
    w7 = json.loads(w7_json.read_text(encoding="utf-8"))
    out = {"regiones_recomendadas_w7": w7["regiones_recomendadas"], "fichas": {}, "barrido": {}}
    base = cargar(trabajo, 21, GENES_EPILAB)
    for etiqueta, genes, sin in (("sin_humano", quitar_humano(base), True),
                                 ("con_humano", base, False)):
        con_panel(sin_humano=sin)
        wr, wc = R.pesos_base()
        cands = [dict(c) for c in R.CANDIDATOS]
        rec = recomendadas(cands, genes, wr, wc, umbral, tabla)
        out["fichas"][etiqueta] = {
            c["gen"]: {k: ficha(genes[c["gen"]], c, wr, wc)["conservadora"][k]
                       for k in ("eficacia", "limpieza", "buenos_limpios", "con_off_target")}
            for c in cands}
        out["fichas"][etiqueta + "_recomendada"] = {c["gen"]: "%d-%d" % c["region"] for c in rec}
        out["barrido"][etiqueta] = {
            "como_estan": R.barrer(cands, genes, "geometrica", False, "off", muestras,
                                   np.random.default_rng(semilla), "absoluta")["frecuencia"],
            "recomendadas": R.barrer(rec, genes, "geometrica", False, "off", muestras,
                                     np.random.default_rng(semilla), "absoluta")["frecuencia"]}
    con_panel(sin_humano=False)
    return out


def correr_k(trabajo: Path, k: int, muestras: int, semilla: int, completo: bool,
             umbral=None, tabla=None) -> dict:
    t0 = time.time()
    con_panel(sin_humano=False)
    genes = cargar(trabajo, k, GENES_EPILAB + GENES_NUEVOS)
    wr, wc = R.pesos_base()
    cands = completar_regiones(genes, wr, wc, umbral, tabla)
    cands_rec = recomendadas(cands, genes, wr, wc, umbral, tabla)
    por_gen = {c["gen"]: c for c in cands}
    est = lambda e: [c for c in cands if c["estrategia"] == e]  # noqa: E731
    est_rec = lambda e: [c for c in cands_rec if c["estrategia"] == e]  # noqa: E731

    res = {"k": k, "muestras": muestras, "semilla": semilla,
           "panel": {R.corto(r): {"accesion": r, "peso_base": R.REFERENCIAS[r]["peso"],
                                  "especie": R.REFERENCIAS[r]["especie"]}
                     for r in R.REFERENCIAS},
           "pesos_base_criterio": wc,
           "regiones": {c["gen"]: "%d-%d" % c["region"] for c in cands},
           "regiones_recomendadas": {c["gen"]: "%d-%d" % c["region"] for c in cands_rec},
           "fichas": [ficha(genes[c["gen"]], c, wr, wc) for c in cands],
           "fichas_recomendadas": [ficha(genes[c["gen"]], c, wr, wc) for c in cands_rec],
           "gen_entero": {g: gen_entero(genes[g], R.excluidas_de(por_gen[g], "off"))
                          for g in GENES_EPILAB + GENES_NUEVOS},
           "alternativas": alternativas_de(cands, genes, wr, wc)}
    print("  k=%d fichas y alternativas: %.0fs" % (k, time.time() - t0), flush=True)

    conj = {"los_seis": cands, "insecto": est("insecto"), "virus": est("virus"),
            "los_seis_recomendados": cands_rec, "insecto_recomendados": est_rec("insecto")}
    if not completo:
        conj = {n: conj[n] for n in ("los_seis", "los_seis_recomendados")}
    res["barridos"] = barridos(conj, genes, muestras, semilla)
    print("  k=%d barridos: %.0fs" % (k, time.time() - t0), flush=True)

    res["nulo_nuevos"] = {g: nulo_gen(genes[g], 200, 2000, semilla) for g in GENES_NUEVOS}
    # Y para los de EPILAB, al largo de EPILAB, con el mismo codigo, por si cambio algo.
    res["nulo_epilab"] = {c["gen"]: nulo_gen(genes[c["gen"]],
                                             c["region"][1] - c["region"][0] + 1, 2000, semilla)
                          for c in R.CANDIDATOS}
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trabajo", default="work/sifi_v2")
    ap.add_argument("--w7", default="research/ola2/W7_ranking/ranking.json")
    ap.add_argument("--muestras", type=int, default=2000)
    ap.add_argument("--semilla", type=int, default=7)
    ap.add_argument("--json", required=True)
    ap.add_argument("--alertas", default=None, type=Path,
                    help="tabla de alertas de M6 que consulta la compuerta de D48; por "
                         "defecto %s" % R.TABLA_ALERTAS)
    ap.add_argument("--umbral-compuerta", dest="umbral_compuerta",
                    choices=("perfecto_21", "perfecto_ge19"), default=R.UMBRAL_COMPUERTA,
                    help="umbral de D28 con el que la compuerta exige decision; por "
                         "defecto %s, que es D48 literal (D69)" % R.UMBRAL_COMPUERTA)
    a = ap.parse_args(argv)
    trabajo = Path(a.trabajo)

    anclas = verificar_anclas(trabajo, Path(a.w7), a.muestras, a.semilla)
    print("anclas: los cuatro conteos, las cuatro fichas y el barrido de W7 reproducidos exacto",
          flush=True)

    res = {"anclas_w7": anclas, "nuevos": NUEVOS, "k": {}}
    for k, completo in ((21, True), (22, True)):
        res["k"][str(k)] = correr_k(trabajo, k, a.muestras, a.semilla, completo,
                                    a.umbral_compuerta, a.alertas)
    res["efecto_humano"] = efecto_humano(trabajo, a.semilla, a.muestras, Path(a.w7),
                                         a.umbral_compuerta, a.alertas)
    res["jaccard_21_22"] = {g: jaccard(trabajo, g) for g in GENES_EPILAB + GENES_NUEVOS}

    Path(a.json).parent.mkdir(parents=True, exist_ok=True)
    Path(a.json).write_text(json.dumps(res, indent=1, ensure_ascii=False, default=int),
                            encoding="utf-8")
    print("escrito en %s" % a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
