#!/usr/bin/env python3
"""Q3 - coincidencias esperadas por azar contra coincidencias observadas, k = 16..22.

Para cada ventana de largo k de los cuatro genes de EPILAB (y de un control barajado
que conserva la composicion de dinucleotidos) y para cada referencia, calcula:

  (i)   esperado uniforme      E_u = 2 * N / 4^k        (las dos hebras)
  (ii)  esperado Markov        E_m = N * (P_o(w) + P_o(rc w)), o = 3, 4, 5,
        con el modelo ajustado a la propia referencia en la misma pasada
  (iii) observado              busqueda exacta de la ventana y su complemento reverso

N es el numero de posiciones de arranque validas (solo A, C, G, T) de la referencia.

Uso:
    python q3_azar_vs_real.py --salida <dir>
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kmers  # noqa: E402

RAIZ = Path("/Users/joaquin/Documents/investigaton/chicharrita-research")
GENES = RAIZ / "work/W5/fasta/epilab_full.fasta"
REFS = [
    ("A_mellifera_transcriptoma", RAIZ / "work/W5/ref/GCF_003254395.2_Amel_HAv3.1_rna.fna.gz",
     "transcriptoma RefSeq de *Apis mellifera* (ARN, insecto no objetivo)"),
    ("Z_mays_transcriptoma", RAIZ / "work/W5/ref/GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna.fna.gz",
     "transcriptoma RefSeq de *Zea mays* (ARN, planta hospedadora)"),
    ("D_maidis_genoma", RAIZ / "work/W5/ref/GCA_975739785.1_ihDalMaid1.1_genomic.fna.gz",
     "genoma completo de *Dalbulus maidis* (ADN, sin anotar)"),
]
KS = list(range(16, 23))


def leer_genes(ruta):
    out = []
    for nombre, seq in kmers.iter_fasta(ruta):
        s = seq.decode().upper().replace("U", "T")
        out.append((nombre, "".join(c for c in s if c in "ACGT")))
    return out


def barajar_dinuc(s: str, semilla: int) -> str:
    """Barajado que conserva el conteo de dinucleotidos (Altschul-Erickson por
    recorrido euleriano aleatorio del grafo de dinucleotidos)."""
    rnd = random.Random(semilla)
    for _ in range(200):
        # arbol de salida aleatorio hacia el ultimo simbolo, metodo estandar
        aristas = {b: [] for b in "ACGT"}
        for a, b in zip(s, s[1:]):
            aristas[a].append(b)
        ultimo = s[-1]
        # arbol: para cada vertice != ultimo, elegir una arista hacia el ultimo
        padre = {}
        ok = True
        for v in "ACGT":
            if v == ultimo or not aristas[v]:
                continue
            padre[v] = rnd.choice(aristas[v])
        # verificar que todos los vertices llegan al ultimo
        for v in list(padre):
            visto, cur = set(), v
            while cur != ultimo:
                if cur in visto or cur not in padre:
                    ok = False
                    break
                visto.add(cur)
                cur = padre[cur]
            if not ok:
                break
        if not ok:
            continue
        resto = {v: list(aristas[v]) for v in "ACGT"}
        for v, w in padre.items():
            resto[v].remove(w)
        for v in "ACGT":
            rnd.shuffle(resto[v])
            if v in padre:
                resto[v].append(padre[v])
        out, cur = [s[0]], s[0]
        for _ in range(len(s) - 1):
            nxt = resto[cur].pop(0)
            out.append(nxt)
            cur = nxt
        cand = "".join(out)
        if len(cand) == len(s):
            return cand
    raise RuntimeError("no se pudo barajar")


def markov_prob(w: str, mcount, orden: int) -> float:
    """P(w) bajo Markov de orden `orden` ajustado por conteos de m-meros."""
    o = orden
    Co = mcount[o]
    Co1 = mcount[o + 1]
    tot = Co.sum()
    ini = Co[kmers.code_of(w[:o])] / tot
    if ini == 0:
        return 0.0
    logp = np.log(ini)
    for i in range(o, len(w)):
        ctx = kmers.code_of(w[i - o:i])
        num = Co1[ctx * 4 + "ACGT".index(w[i])]
        den = Co1[ctx * 4:ctx * 4 + 4].sum()
        if num == 0 or den == 0:
            return 0.0
        logp += np.log(num / den)
    return float(np.exp(logp))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True)
    ap.add_argument("--bloque", type=int, default=8_000_000)
    a = ap.parse_args()
    sal = Path(a.salida)
    sal.mkdir(parents=True, exist_ok=True)

    genes = leer_genes(GENES)
    print("genes:", [(n, len(s)) for n, s in genes], flush=True)

    # consultas: ventanas reales + control barajado por dinucleotidos
    ventanas = {k: [] for k in KS}
    meta = {k: [] for k in KS}      # (gen, conjunto, pos)
    for nombre, s in genes:
        sb = barajar_dinuc(s, semilla=abs(hash(nombre)) % 10 ** 6)
        for etiqueta, sec in (("real", s), ("barajado", sb)):
            for k in KS:
                for i in range(len(sec) - k + 1):
                    w = sec[i:i + k]
                    ventanas[k].append(w)
                    meta[k].append((nombre, etiqueta, i + 1))
    print("ventanas por k:", {k: len(ventanas[k]) for k in KS}, flush=True)

    cons = kmers.Consultas(ventanas)
    filas = []
    detalle = {}
    for etiqueta, ruta, desc in REFS:
        if not ruta.exists():
            print("FALTA", ruta, flush=True)
            continue
        t0 = time.time()
        print("== escaneando %s" % etiqueta, flush=True)
        r = kmers.escanear(str(ruta), cons, bloque=a.bloque)
        dt = time.time() - t0
        print("   %.1f s, %d registros, %d bases" % (dt, r["registros"], r["bases"]), flush=True)
        mc = r["mcount"]
        gc = (mc[1][1] + mc[1][2]) / mc[1].sum()
        detalle[etiqueta] = {"descripcion": desc, "archivo": str(ruta),
                             "registros": r["registros"], "bases": r["bases"],
                             "gc": gc, "segundos": dt,
                             "neff": {str(k): int(r["neff"][k]) for k in KS}}
        for k in KS:
            N = r["neff"][k]
            obs = r["observado"][k]
            nrec = r["registros_distintos"][k]
            eu = 2.0 * N / 4.0 ** k
            for conjunto in ("real", "barajado"):
                sel = np.array([m[1] == conjunto for m in meta[k]])
                ob = obs[sel]
                em = {}
                for o in (3, 4, 5):
                    ps = np.array([markov_prob(w, mc, o) + markov_prob(kmers.rc(w), mc, o)
                                   for w, m in zip(ventanas[k], meta[k]) if m[1] == conjunto])
                    em[o] = N * ps
                filas.append({
                    "referencia": etiqueta, "conjunto": conjunto, "k": k,
                    "N_posiciones": int(N), "ventanas": int(sel.sum()),
                    "obs_total": int(ob.sum()),
                    "obs_media_por_ventana": float(ob.mean()),
                    "frac_ventanas_con_acierto": float((ob > 0).mean()),
                    "esp_uniforme_por_ventana": eu,
                    "esp_uniforme_total": eu * int(sel.sum()),
                    "esp_markov3_por_ventana": float(em[3].mean()),
                    "esp_markov4_por_ventana": float(em[4].mean()),
                    "esp_markov5_por_ventana": float(em[5].mean()),
                    "razon_obs_esp_uniforme": float(ob.mean() / eu) if eu > 0 else None,
                    "razon_obs_esp_markov5": float(ob.mean() / em[5].mean()) if em[5].mean() > 0 else None,
                    "frac_poisson_uniforme": float(1 - np.exp(-eu)),
                    "frac_poisson_markov5": float(np.mean(1 - np.exp(-em[5]))),
                    "max_registros_distintos": int(nrec[sel].max()),
                    "ventanas_en_mas_de_500_registros": int((nrec[sel] > 500).sum()),
                })
                print("   k=%2d %-9s obs=%8d  E_u=%10.3g  E_m5=%10.3g  frac_hit=%.4f"
                      % (k, conjunto, ob.sum(), eu * sel.sum(), em[5].mean() * sel.sum(),
                         (ob > 0).mean()), flush=True)
        # guardado incremental
        (sal / "q3_tabla.json").write_text(json.dumps(
            {"filas": filas, "referencias": detalle}, indent=1, ensure_ascii=False))

    with open(sal / "q3_tabla.tsv", "w") as fh:
        cols = list(filas[0].keys())
        fh.write("\t".join(cols) + "\n")
        for f in filas:
            fh.write("\t".join(str(f[c]) for c in cols) + "\n")
    print("escrito en", sal, flush=True)


if __name__ == "__main__":
    main()
