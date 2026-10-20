"""Dos complementos a W7: el panel ampliado y el barrido de 21 contra 22 nt.

1. **Panel ampliado.** W7 corrio el veto contra seis referencias. Falta la especie que
   `pipeline/REPORT.md` s.4.2 midio como la que mas descarta —*Macrosteles quadrilineatus*,
   el cicadelido con genoma anotado mas cercano a *Dalbulus maidis*— y falta *Homo sapiens*,
   que el investigador nombro en el checkpoint y que `CLAUDE.md` pide. Agregar referencias
   solo puede AGREGAR vetos, nunca sacarlos, asi que correr las dos nuevas por separado basta
   para contestar si las regiones recomendadas por W7 sobreviven.

2. **21 contra 22 nt.** El investigador lo pidio en el checkpoint y `R1_fundamentos` s.2.1
   establece que el largo del siRNA lo fija la Dicer del orden y que **para hemipteros no hay
   perfil publicado**. El motor de `sifi_core` toma `sirna_size` como parametro, asi que el
   barrido es directo. Lo que NO es directo es la regla terminal: mira el nucleotido 2 y el
   tercero desde el final (`sirna[size-3]`), de modo que a 22 nt el "19" pasa a ser el 20.
   Se conserva la posicion relativa, que es la lectura mecanicista (el extremo 3' de la guia),
   y queda declarado porque es una decision y no una propiedad del original.

Nada sale de la maquina: las referencias se leen de disco y las secuencias de EPILAB nunca
se suben a ningun servicio. Uso:

    python panel_y_k.py --perfil work/sifi_check/salida \
        --offtarget-nuevo work/sifi_check/offtarget_panel_nuevo/offtarget_por_sirna.tsv \
        --fasta work/sifi_check --json research/ola3/C6_panel_y_largo/resultados/panel_y_k.json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sifi_core import SifiEngine  # noqa: E402

# Region que eligio EPILAB y la que W7 recomienda, por gen, con su largo nativo.
GENES = {
    "MP_MRFV":    {"epilab": (1, 200),    "w7": (72, 271),     "largo": 200},
    "CP_MRFV":    {"epilab": (201, 400),  "w7": (99, 298),     "largo": 200},
    "BicC_Dm":    {"epilab": (264, 563),  "w7": (2123, 2422),  "largo": 300},
    "ATPaseD_Dm": {"epilab": (151, 450),  "w7": (72, 371),     "largo": 300},
}
# Anclas publicadas: eficientes en modo corregido con ViennaRNA 2.7.2 (W7 s.2.0 y
# sifi21_reproduccion.md s.1). Si no coinciden, el entorno no es el de W7 y se aborta.
ANCLAS_21 = {"MP_MRFV": 123, "CP_MRFV": 30, "BicC_Dm": 171, "ATPaseD_Dm": 29}


def leer_fasta(p: Path) -> str:
    return "".join(l.strip() for l in p.read_text().splitlines() if not l.startswith(">"))


def perfil(dir_salida: Path, gen: str) -> list[int]:
    """Posiciones de las ventanas eficientes, del TSV que deja run_sifi.py."""
    f = dir_salida / f"{gen}_full_corregido_vienna.tsv"
    with f.open() as fh:
        return [int(r["pos"]) for r in csv.DictReader(fh, delimiter="\t")
                if r["is_efficient"] == "True"]


def en(ps, a, b):
    return sum(1 for p in ps if a <= p <= b)


def mejor_region(ps, largo, tope, vetadas=frozenset()):
    """Region de `largo` con mas eficientes, saltando las que contienen una posicion vetada."""
    mejor, n_mejor = None, -1
    for a in range(1, tope - largo + 2):
        b = a + largo - 1
        if any(a <= v <= b for v in vetadas):
            continue
        n = en(ps, a, b)
        if n > n_mejor:
            n_mejor, mejor = n, (a, b)
    return (mejor, n_mejor) if mejor else (None, 0)


def escapan(largo, tope, vetadas):
    return sum(1 for a in range(1, tope - largo + 2)
               if not any(a <= v <= a + largo - 1 for v in vetadas))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--perfil", required=True, help="dir con los TSV de run_sifi.py a 21 nt")
    ap.add_argument("--offtarget-nuevo", required=True, dest="off_nuevo")
    ap.add_argument("--fasta", required=True, help="dir con los *_full.fasta")
    ap.add_argument("--off22", default=None, help="TSV de off-targets corrido con --size 22")
    ap.add_argument("--json", required=True)
    a = ap.parse_args()

    dir_perfil, dir_fasta = Path(a.perfil), Path(a.fasta)
    res = {"anclas_21nt": {}, "panel_ampliado": {}, "k21_vs_k22": {}}

    # ---- 0. anclas: el entorno tiene que reproducir W7 antes de medir nada nuevo
    perfiles = {}
    for g in GENES:
        perfiles[g] = perfil(dir_perfil, g)
        got, esp = len(perfiles[g]), ANCLAS_21[g]
        res["anclas_21nt"][g] = {"obtenido": got, "publicado": esp, "coincide": got == esp}
        if got != esp:
            sys.exit(f"ANCLA ROTA en {g}: {got} eficientes contra {esp} publicados. "
                     "El entorno no reproduce W7; no se sigue.")
    print("anclas 21 nt: los cuatro conteos de W7 reproducidos exacto")

    # ---- 1. panel ampliado: que regiones quedan vetadas por las dos referencias nuevas
    filas = list(csv.DictReader(open(a.off_nuevo), delimiter="\t"))
    refs = sorted({c.split("|")[0] for c in filas[0] if "|" in c})
    por_gen = {}
    for r in filas:
        por_gen.setdefault(r["consulta"].replace("_full", ""), []).append(r)

    for g, cfg in GENES.items():
        rs, ps, L = por_gen[g], perfiles[g], cfg["largo"]
        tope = max(int(r["pos"]) for r in rs)
        veto = {ref: sorted(int(r["pos"]) for r in rs if r[f"{ref}|perfecto_21"] != "0")
                for ref in refs}
        todas = sorted(set().union(*veto.values())) if veto else []
        d = {"ventanas": tope, "largo_region": L,
             "veto_por_referencia": {k: len(v) for k, v in veto.items()},
             "regiones": {}, "regiones_que_escapan": escapan(L, tope, set(todas)),
             "regiones_totales": tope - L + 1}
        for et, (x, y) in (("epilab", cfg["epilab"]), ("w7_recomendada", cfg["w7"])):
            d["regiones"][et] = {
                "region": [x, y], "eficientes": en(ps, x, y),
                "veto_nuevo": {k: en(v, x, y) for k, v in veto.items()},
                "vetada_por_panel_nuevo": any(en(v, x, y) for v in veto.values())}
        if todas:
            reg, n = mejor_region(ps, L, tope, set(todas))
            d["mejor_sin_veto_ampliado"] = {"region": list(reg) if reg else None, "eficientes": n}
        res["panel_ampliado"][g] = d

    # ---- 2. 21 contra 22 nt
    for g, cfg in GENES.items():
        seq = leer_fasta(dir_fasta / f"{g}_full.fasta")
        fila = {"largo_gen": len(seq)}
        for k in (21, 22):
            w, resumen = SifiEngine(mode="corregido", sirna_size=k).run(seq, backend="vienna")
            pos = [x.pos for x in w if x.is_efficient]
            reg, n = mejor_region(pos, cfg["largo"], len(pos) and max(x.pos for x in w))
            fila[f"k{k}"] = {
                "ventanas": len(w), "eficientes": len(pos),
                "tasa": round(len(pos) / len(w), 4),
                "epilab": en(pos, *cfg["epilab"]),
                "w7": en(pos, *cfg["w7"]),
                "mejor_region": list(reg) if reg else None, "mejor_eficientes": n,
                "posiciones": pos,
            }
        p21, p22 = set(fila["k21"]["posiciones"]), set(fila["k22"]["posiciones"])
        fila["solapamiento"] = {
            "en_ambos": len(p21 & p22), "solo_21": len(p21 - p22), "solo_22": len(p22 - p21),
            "jaccard": round(len(p21 & p22) / len(p21 | p22), 4) if (p21 | p22) else None}
        for k in ("k21", "k22"):
            fila[k].pop("posiciones")
        res["k21_vs_k22"][g] = fila
        print(f"  {g:11s} k21 {fila['k21']['eficientes']:>4d} ({fila['k21']['tasa']:.1%})  "
              f"k22 {fila['k22']['eficientes']:>4d} ({fila['k22']['tasa']:.1%})  "
              f"jaccard {fila['solapamiento']['jaccard']}")

    if a.off22:
        f22 = list(csv.DictReader(open(a.off22), delimiter="\t"))
        res["off_target_22nt"] = {}
        for r in f22:
            g = r["consulta"].replace("_full", "")
            d = res["off_target_22nt"].setdefault(g, {})
            for c, v in r.items():
                if "|" in c and v != "0":
                    d[c] = d.get(c, 0) + 1

    Path(a.json).parent.mkdir(parents=True, exist_ok=True)
    Path(a.json).write_text(json.dumps(res, indent=1, ensure_ascii=False))
    print("escrito", a.json)


if __name__ == "__main__":
    main()
