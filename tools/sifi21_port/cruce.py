"""Cruza el perfil de eficiencia de si-Fi21 con el tamizaje de off-targets de 21 nt.

Contesta tres cosas por gen:

  1. Cuantos siRNA eficientes tiene la region que eligio EPILAB, y cuantos de esos
     quedan limpios de off-targets. Es la columna que el investigador pidio llenar.
  2. Cual es la mejor region por densidad de eficientes, y cual por densidad de
     eficientes limpios. No tienen por que ser la misma.
  3. Si el perfil de off-targets explica la eleccion de EPILAB.

Un hit contra la referencia del propio organismo blanco es ON-target, no
off-target: para los genes de Dalbulus maidis hay que excluir su genoma del
computo, y eso va por parametro (`--ontarget`).

Uso:
    python cruce.py --gen BicC_Dm --region 264 563 \
        --ontarget GCA_975739785.1_ihDalMaid1.1_genomic \
        --dir work/sifi_check --offtarget work/sifi_check/offtarget_full
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sifi_core import SifiEngine

CRITERIO = "perfecto_ge19"  # el criterio de riesgo: bloque contiguo perfecto >=19 nt


def leer_fasta(ruta):
    return "".join(l.strip() for l in Path(ruta).read_text().splitlines()
                   if not l.startswith(">"))


def leer_offtarget(ruta_tsv, consulta, ontarget=None):
    """Devuelve {pos: {base: n_refs}} con las bases off-target solamente."""
    por_pos = {}
    with open(ruta_tsv, encoding="utf-8") as fh:
        r = csv.DictReader(fh, delimiter="\t")
        cols = [c for c in r.fieldnames or []
                if c.endswith("|" + CRITERIO) and (
                    ontarget is None or not c.startswith(ontarget))]
        for fila in r:
            if fila["consulta"] != consulta:
                continue
            d = {}
            for c in cols:
                n = int(fila[c] or 0)
                if n:
                    d[c.split("|")[0]] = n
            por_pos[int(fila["pos"])] = d
    return por_pos


def mejor(ventanas, largo, clave):
    """Region de `largo` nt que maximiza `clave`, por ventana deslizante."""
    marcas = [w["pos"] for w in ventanas if clave(w)]
    if not marcas:
        return None
    mejor_r, mejor_n = None, -1
    tope = max(w["pos"] for w in ventanas)
    for ini in range(1, tope + 1):
        fin = ini + largo - 1
        n = sum(1 for p in marcas if ini <= p <= fin)
        if n > mejor_n:
            mejor_n, mejor_r = n, (ini, fin)
    return {"inicio": mejor_r[0], "fin": mejor_r[1], "n": mejor_n}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gen", required=True)
    ap.add_argument("--region", nargs=2, type=int, required=True, metavar=("INI", "FIN"))
    ap.add_argument("--ontarget", default=None)
    ap.add_argument("--dir", default="work/sifi_check")
    ap.add_argument("--offtarget", default="work/sifi_check/offtarget_full")
    ap.add_argument("--modo", choices=("fiel", "corregido"), default="corregido")
    ap.add_argument("--backend", choices=("exe", "vienna"), default="vienna")
    a = ap.parse_args(argv)

    d = Path(a.dir)
    seq = leer_fasta(d / ("%s_full.fasta" % a.gen))
    ini, fin = a.region
    largo = fin - ini + 1

    eng = SifiEngine(mode=a.modo)
    vent, _ = eng.run(seq, backend=a.backend)
    off = leer_offtarget(Path(a.offtarget) / "offtarget_por_sirna.tsv",
                         "%s_full" % a.gen, a.ontarget)

    ventanas = []
    for w in vent:
        o = off.get(w.pos, {})
        ventanas.append({"pos": w.pos, "efic": w.is_efficient,
                         "off": o, "n_bases": len(o)})

    def en(r):
        return [w for w in ventanas if r[0] <= w["pos"] <= r[1]]

    def resumen(ws):
        ef = [w for w in ws if w["efic"]]
        limpios = [w for w in ef if not w["off"]]
        con_off = [w for w in ws if w["off"]]
        return len(ws), len(ef), len(limpios), len(con_off)

    print("=== %s  (modo %s, backend %s) ===" % (a.gen, a.modo, a.backend))
    print("criterio de riesgo: %s en bases no objetivo%s" % (
        CRITERIO, (", excluyendo %s como on-target" % a.ontarget) if a.ontarget else ""))
    print()

    tot = resumen(ventanas)
    print("gen entero          ventanas %-5d eficientes %-4d limpios %-4d con off-target %d" % tot)

    eleg = resumen(en((ini, fin)))
    print("region EPILAB %-5s ventanas %-5d eficientes %-4d limpios %-4d con off-target %d"
          % ("%d-%d" % (ini, fin), *eleg))

    m_ef = mejor(ventanas, largo, lambda w: w["efic"])
    if m_ef:
        r = resumen(en((m_ef["inicio"], m_ef["fin"])))
        print("mas eficientes %-5s ventanas %-5d eficientes %-4d limpios %-4d con off-target %d"
              % ("%d-%d" % (m_ef["inicio"], m_ef["fin"]), *r))

    m_lim = mejor(ventanas, largo, lambda w: w["efic"] and not w["off"])
    if m_lim:
        r = resumen(en((m_lim["inicio"], m_lim["fin"])))
        print("mas limpios    %-5s ventanas %-5d eficientes %-4d limpios %-4d con off-target %d"
              % ("%d-%d" % (m_lim["inicio"], m_lim["fin"]), *r))

    print()
    bases = {}
    for w in ventanas:
        for b, n in w["off"].items():
            bases.setdefault(b, [0, 0])
            bases[b][0] += 1
            if w["efic"]:
                bases[b][1] += 1
    if bases:
        print("off-targets por base (gen entero): ventanas afectadas / de esas, eficientes")
        for b, (n, ne) in sorted(bases.items(), key=lambda kv: -kv[1][0]):
            print("   %-52s %4d / %d" % (b, n, ne))
    else:
        print("sin off-targets en ninguna base no objetivo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
