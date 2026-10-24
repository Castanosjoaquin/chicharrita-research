"""Anclas de M5: el motor reconstruido tiene que reproducir `ranking_v2.json`.

Dos anclas, las dos abortan el proceso si fallan (`sys.exit`), y las dos corren antes
de cualquier medicion de esta linea:

  A1  los conteos del gen entero, por referencia y por criterio, de los seis genes.
      M7 ya habia verificado los doce de `BicC_Dm` con las seis bases; aca van los
      seis genes completos.
  A2  con los pesos de D18 **sin partir**, el barrido de 2.000 sorteos reproduce las
      frecuencias por posicion publicadas, en las diez combinaciones de forma, regla
      y escala, para los cinco conjuntos del JSON.

Si algo no coincide es un hallazgo y se reporta; no se pisa.

    python research/ola4/M5_dos_ejes/scripts/anclas.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))
import ranking as R          # noqa: E402
import ranking_v2 as V       # noqa: E402

PUBLICADO = RAIZ / "research/ola3/C7_ranking_v2/resultados/ranking_v2.json"
TRABAJO = RAIZ / "work" / "sifi_v2"
GENES = V.GENES_EPILAB + V.GENES_NUEVOS


def cargar_todo(k: int = 21):
    """Los seis genes con el panel completo de seis referencias mas el vector."""
    V.con_panel(sin_humano=False)
    return V.cargar(TRABAJO, k, GENES)


def candidatos(genes, wr, wc):
    """Los seis candidatos con la region que publica el JSON (no se reeligen)."""
    pub = json.loads(PUBLICADO.read_text(encoding="utf-8"))["k"]["21"]["regiones"]
    cands = []
    for c in list(R.CANDIDATOS) + V.NUEVOS:
        d = dict(c)
        ini, fin = (int(x) for x in pub[d["gen"]].split("-"))
        d["region"] = (ini, fin)
        cands.append(d)
    return cands


def a1_gen_entero(genes, publicado) -> list[dict]:
    """Conteos del gen entero por referencia y criterio contra el JSON publicado."""
    filas = []
    por_gen = {c["gen"]: c for c in list(R.CANDIDATOS) + V.NUEVOS}
    for gen in GENES:
        mio = V.gen_entero(genes[gen], R.excluidas_de(por_gen[gen], "off"))
        suyo = publicado["gen_entero"][gen]
        for campo in ("ventanas", "eficientes"):
            filas.append({"ancla": "A1", "gen": gen, "referencia": "-", "criterio": campo,
                          "mio": mio[campo], "publicado": suyo[campo],
                          "coincide": mio[campo] == suyo[campo]})
        refs = sorted(set(mio["por_referencia"]) | set(suyo["por_referencia"]))
        for ref in refs:
            a, b = mio["por_referencia"].get(ref, {}), suyo["por_referencia"].get(ref, {})
            for crit in ("perfecto_21", "perfecto_ge19", "mm1_21", "perfecto_21_eficientes"):
                x, y = a.get(crit, 0), b.get(crit, 0)
                filas.append({"ancla": "A1", "gen": gen, "referencia": ref, "criterio": crit,
                              "mio": x, "publicado": y, "coincide": x == y})
            x, y = a.get("perfecto_21_posiciones", []), b.get("perfecto_21_posiciones", [])
            filas.append({"ancla": "A1", "gen": gen, "referencia": ref,
                          "criterio": "perfecto_21_posiciones",
                          "mio": len(x), "publicado": len(y), "coincide": list(x) == list(y)})
    return filas


def a2_barrido(genes, cands, publicado, muestras: int, semilla: int) -> list[dict]:
    """El barrido con los pesos de D18 sin partir, contra las frecuencias publicadas."""
    rec = V.recomendadas(cands, genes, *R.pesos_base())
    conj = {"los_seis": cands,
            "insecto": [c for c in cands if c["estrategia"] == "insecto"],
            "virus": [c for c in cands if c["estrategia"] == "virus"],
            "los_seis_recomendados": rec,
            "insecto_recomendados": [c for c in rec if c["estrategia"] == "insecto"]}
    filas = []
    for nombre, cs in conj.items():
        for clave, esperado in publicado["barridos"][nombre].items():
            forma, regla, *resto = clave.split("/")
            escala = resto[0] if resto else "absoluta"
            r = R.barrer(cs, genes, forma, regla == "mecanicista", "off", muestras,
                         np.random.default_rng(semilla), escala)
            filas.append({"ancla": "A2", "conjunto": nombre, "clave": clave,
                          "mio": r["frecuencia"], "publicado": esperado["frecuencia"],
                          "coincide": r["frecuencia"] == esperado["frecuencia"]})
        # y las regiones recomendadas, que el motor reelige
        if nombre == "los_seis_recomendados":
            mias = {c["gen"]: "%d-%d" % c["region"] for c in cs}
            filas.append({"ancla": "A2", "conjunto": "regiones_recomendadas", "clave": "-",
                          "mio": mias, "publicado": publicado["regiones_recomendadas"],
                          "coincide": mias == publicado["regiones_recomendadas"]})
    return filas


def correr(muestras: int = 2000, semilla: int = 7, verboso: bool = True) -> dict:
    publicado = json.loads(PUBLICADO.read_text(encoding="utf-8"))["k"]["21"]
    genes = cargar_todo(21)
    wr, wc = R.pesos_base()
    cands = candidatos(genes, wr, wc)
    f1 = a1_gen_entero(genes, publicado)
    f2 = a2_barrido(genes, cands, publicado, muestras, semilla)
    rotas = [f for f in f1 + f2 if not f["coincide"]]
    if verboso:
        print("A1  conteos del gen entero: %d de %d coinciden"
              % (sum(f["coincide"] for f in f1), len(f1)))
        print("A2  barridos con los pesos de D18: %d de %d coinciden"
              % (sum(f["coincide"] for f in f2), len(f2)))
    if rotas:
        for f in rotas[:20]:
            print("ANCLA ROTA  %s" % f, file=sys.stderr)
        sys.exit("ANCLAS ROTAS: %d de %d comparaciones no coinciden con %s"
                 % (len(rotas), len(f1) + len(f2), PUBLICADO.relative_to(RAIZ)))
    return {"genes": genes, "candidatos": cands, "publicado": publicado,
            "a1": f1, "a2": f2, "muestras": muestras, "semilla": semilla}


if __name__ == "__main__":
    res = correr()
    salida = RAIZ / "research/ola4/M5_dos_ejes/resultados/anclas.json"
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps(
        {"fuente": str(PUBLICADO.relative_to(RAIZ)),
         "muestras": res["muestras"], "semilla": res["semilla"],
         "A1_comparaciones": len(res["a1"]), "A1_coinciden": sum(f["coincide"] for f in res["a1"]),
         "A2_comparaciones": len(res["a2"]), "A2_coinciden": sum(f["coincide"] for f in res["a2"]),
         "A1": res["a1"], "A2": [{k: v for k, v in f.items() if k != "mio"} | {"mio": f["mio"]}
                                 for f in res["a2"]]},
        indent=1, ensure_ascii=False), encoding="utf-8")
    print("escrito en %s" % salida.relative_to(RAIZ))
