#!/usr/bin/env python3
"""Q2 - benchmark de ventanas de 21 contra 22 nt con el criterio de eficiencia de si-Fi21.

Importa el port de `tools/sifi21_port/` SIN modificarlo. El largo de ventana SI es un
parametro del port: `SifiEngine(..., sirna_size=k)` y `DEFAULTS["sirna_size"]`, de modo
que la comparacion se hace con el mismo motor y no con una reimplementacion.

Advertencia que hay que leer junto con los numeros: la regla de nucleotidos terminales
del original mira `sirna[size-3]` (el nucleotido 19 de una ventana de 21) y `sirna[1]`.
Con `sirna_size=22` el port la aplica al nucleotido 20, es decir, mantiene «el tercero
desde el final». Eso es una generalizacion del port, no una regla validada para 22 nt.

Backend: ViennaRNA instalado en el entorno (no el RNAplfold 2.1.5 de si-Fi21, que es un
ejecutable de Windows). Los conteos absolutos no son comparables con los de W5; lo que
se compara aca es 21 contra 22 con el mismo backend.

Uso:
    python q2_ventana_21_vs_22.py --salida <dir>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RAIZ = Path("/Users/joaquin/Documents/investigaton/chicharrita-research")
sys.path.insert(0, str(RAIZ / "tools/sifi21_port"))
import sifi_core  # noqa: E402

GENES = ["ATPaseD_Dm", "CP_MRFV", "MP_MRFV", "BicC_Dm"]
REGION = 200


def leer(ruta):
    s = []
    for ln in Path(ruta).read_text().splitlines():
        if not ln.startswith(">"):
            s.append(ln.strip())
    return "".join(s).upper().replace("U", "T")


def spearman(a, b):
    def rangos(x):
        orden = sorted(range(len(x)), key=lambda i: x[i])
        r = [0.0] * len(x)
        i = 0
        while i < len(orden):
            j = i
            while j + 1 < len(orden) and x[orden[j + 1]] == x[orden[i]]:
                j += 1
            prom = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[orden[k]] = prom
            i = j + 1
        return r
    ra, rb = rangos(a), rangos(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    da = sum((x - ma) ** 2 for x in ra) ** 0.5
    db = sum((y - mb) ** 2 for y in rb) ** 0.5
    return num / (da * db) if da and db else float("nan")


def perfil_regiones(posiciones, largo_gen, size, region=REGION):
    """Para cada inicio de region, cuantas ventanas eficientes caen adentro."""
    ult = max(1, largo_gen - size + 1 - region + 1)
    s = set(posiciones)
    return [sum(1 for p in range(ini, ini + region) if p in s) for ini in range(1, ult + 1)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True)
    ap.add_argument("--modos", nargs="+", default=["fiel", "corregido"])
    a = ap.parse_args()
    sal = Path(a.salida); sal.mkdir(parents=True, exist_ok=True)
    crudo = RAIZ / "work/C3/q2"; crudo.mkdir(parents=True, exist_ok=True)

    print("port: %s   ViennaRNA via backend 'vienna'" % (RAIZ / "tools/sifi21_port"))
    import RNA
    print("ViennaRNA", RNA.__version__)
    filas, detalle = [], {}
    for modo in a.modos:
        for gen in GENES:
            seq = leer(RAIZ / ("work/W5/fasta/%s_full.fasta" % gen))
            res = {}
            for k in (21, 22):
                eng = sifi_core.SifiEngine(mode=modo, sirna_size=k)
                w, r = eng.run(seq, backend="vienna")
                eff = [x.pos for x in w if x.is_efficient]
                mejor = sifi_core.best_region(w, REGION)
                res[k] = {"ventanas": len(w), "eficientes": len(eff), "pos": eff,
                          "resumen": r, "mejor_region": mejor,
                          "perfil": perfil_regiones(eff, len(seq), k)}
                sifi_core.to_tsv(w, crudo / ("%s_%s_k%d.tsv" % (gen, modo, k)))
            p21, p22 = set(res[21]["pos"]), set(res[22]["pos"])
            # solapamiento por posicion de inicio
            inter = p21 & p22
            # solapamiento por nucleotidos cubiertos
            cob21 = set()
            for p in p21:
                cob21 |= set(range(p, p + 21))
            cob22 = set()
            for p in p22:
                cob22 |= set(range(p, p + 22))
            n = min(len(res[21]["perfil"]), len(res[22]["perfil"]))
            rho = spearman(res[21]["perfil"][:n], res[22]["perfil"][:n])
            m21, m22 = res[21]["mejor_region"], res[22]["mejor_region"]
            # cuantas eficientes de 22 caen en la mejor region de 21, y viceversa
            def cuenta(pos, reg):
                return sum(1 for p in pos if reg["inicio"] <= p <= reg["fin"])
            fila = {
                "modo": modo, "gen": gen, "largo": len(seq),
                "eficientes_21": len(p21), "eficientes_22": len(p22),
                "delta_pct": 100.0 * (len(p22) - len(p21)) / max(1, len(p21)),
                "inicios_compartidos": len(inter),
                "jaccard_inicios": len(inter) / max(1, len(p21 | p22)),
                "jaccard_nucleotidos_cubiertos": len(cob21 & cob22) / max(1, len(cob21 | cob22)),
                "mejor_region_21": "%d-%d" % (m21["inicio"], m21["fin"]) if m21 else None,
                "eficientes_en_mejor_region_21": m21["eficientes"] if m21 else None,
                "mejor_region_22": "%d-%d" % (m22["inicio"], m22["fin"]) if m22 else None,
                "eficientes_en_mejor_region_22": m22["eficientes"] if m22 else None,
                "desplazamiento_inicio_mejor_region": (m22["inicio"] - m21["inicio"])
                                                      if (m21 and m22) else None,
                "eff22_en_mejor_region_de_21": cuenta(p22, m21) if m21 else None,
                "eff21_en_mejor_region_de_22": cuenta(p21, m22) if m22 else None,
                "spearman_perfil_regiones_200nt": rho,
                "ranking_region_21_top_en_22": None,
            }
            # posicion en el ranking de 22 de la mejor region segun 21
            if m21 and m22:
                perf22 = res[22]["perfil"]
                i21 = m21["inicio"] - 1
                if i21 < len(perf22):
                    v = perf22[i21]
                    fila["ranking_region_21_top_en_22"] = 1 + sum(1 for x in perf22 if x > v)
            filas.append(fila)
            detalle["%s|%s" % (modo, gen)] = {
                "21": {kk: vv for kk, vv in res[21].items() if kk != "perfil"},
                "22": {kk: vv for kk, vv in res[22].items() if kk != "perfil"},
            }
            print("  %-10s %-10s 21:%4d  22:%4d  compartidos:%4d  rho=%.3f  top21=%s top22=%s"
                  % (modo, gen, len(p21), len(p22), len(inter), rho,
                     fila["mejor_region_21"], fila["mejor_region_22"]), flush=True)

    with open(sal / "q2_21_vs_22.tsv", "w") as fh:
        cols = list(filas[0].keys())
        fh.write("\t".join(cols) + "\n")
        for f in filas:
            fh.write("\t".join(str(f[c]) for c in cols) + "\n")
    (sal / "q2_21_vs_22.json").write_text(json.dumps(
        {"filas": filas, "detalle": detalle, "viennarna": RNA.__version__},
        indent=1, ensure_ascii=False))
    print("escrito en", sal)


if __name__ == "__main__":
    main()
