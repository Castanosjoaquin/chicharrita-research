"""Tamizaje de off-targets de ventanas de 21 nt contra referencias locales, por siRNA.

Por qué no BLAST: para lo que importa en RNAi —bloques contiguos perfectos de 19 a
21 nt— la coincidencia exacta es la respuesta correcta y no una heurística. BLAST
con `blastn-short` aproxima eso con semillas, perc_identity y e-value, y hay que
filtrar después. Acá se busca exacto, en una sola pasada por cada base, con un
autómata de Aho-Corasick. Ventaja práctica: el resultado es por siRNA, no un
conteo agregado, que es lo que hace falta para cruzarlo con el perfil de eficiencia.

Criterios, con las mismas definiciones que usó W5 (`analisis/COMANDOS.md` §4):

  perfecto_21     el 21-mero aparece idéntico en la referencia.
  perfecto_ge19   algún bloque contiguo de 19 nt o más del 21-mero aparece idéntico.
  mm1_21          el 21-mero aparece con exactamente un desajuste (opcional, --mm1).

Se busca en las dos hebras: se generan los complementos reversos de las consultas,
que es equivalente a recorrer las dos hebras de la referencia y mucho más barato.

Nada sale de la máquina: las referencias se leen de disco. Uso:

    python offtarget_21nt.py --consulta work/sifi_check/BicC_Dm_sel.fasta \
        --db work/offtarget_db/*.fna.gz --salida work/sifi_check/offtarget --mm1
"""

from __future__ import annotations

import argparse
import glob
import gzip
import json
import sys
from pathlib import Path

import ahocorasick

COMP = str.maketrans("ACGT", "TGCA")
SIZE = 21
MIN_BLOCK = 19


def rc(s: str) -> str:
    return s.translate(COMP)[::-1]


def leer_fasta(ruta):
    nombre, buf = None, []
    for linea in Path(ruta).read_text().splitlines():
        if linea.startswith(">"):
            if nombre is not None:
                yield nombre, "".join(buf)
            nombre, buf = linea[1:].strip().split()[0], []
        else:
            buf.append(linea.strip())
    if nombre is not None:
        yield nombre, "".join(buf)


def iter_db(ruta):
    """Itera (nombre, secuencia) de un FASTA, con o sin gzip, sin cargarlo entero."""
    abrir = gzip.open if str(ruta).endswith(".gz") else open
    nombre, buf = None, []
    with abrir(ruta, "rt") as fh:
        for linea in fh:
            if linea.startswith(">"):
                if nombre is not None:
                    yield nombre, "".join(buf)
                nombre, buf = linea[1:].strip().split()[0], []
            else:
                buf.append(linea.strip().upper())
    if nombre is not None:
        yield nombre, "".join(buf)


def variantes_1mm(s: str):
    """Las 63 variantes del 21-mero con exactamente un desajuste."""
    for i, base in enumerate(s):
        for alt in "ACGT":
            if alt != base:
                yield s[:i] + alt + s[i + 1:]


def construir(consultas, con_mm1: bool):
    """Arma el autómata y el mapa patrón -> (siRNA, criterio).

    Devuelve (automata, sirnas) donde sirnas es la lista de dicts por ventana.
    """
    aut = ahocorasick.Automaton()
    sirnas = []
    # patron -> lista de (indice_sirna, criterio)
    for ruta in consultas:
        for nombre, seq in leer_fasta(ruta):
            seq = seq.upper().replace("U", "T")
            for i in range(len(seq) - SIZE + 1):
                w = seq[i:i + SIZE]
                if any(b not in "ACGT" for b in w):
                    continue
                idx = len(sirnas)
                sirnas.append({"consulta": nombre, "pos": i + 1, "sirna": w})

                pats = [(w, "perfecto_21"), (rc(w), "perfecto_21")]
                # bloques contiguos de MIN_BLOCK; si alguno esta, hay >=19 perfecto
                for j in range(SIZE - MIN_BLOCK + 1):
                    b = w[j:j + MIN_BLOCK]
                    pats.append((b, "perfecto_ge19"))
                    pats.append((rc(b), "perfecto_ge19"))
                if con_mm1:
                    for v in variantes_1mm(w):
                        pats.append((v, "mm1_21"))
                        pats.append((rc(v), "mm1_21"))

                for p, crit in pats:
                    if aut.exists(p):
                        aut.get(p).append((idx, crit))
                    else:
                        aut.add_word(p, [(idx, crit)])
    aut.make_automaton()
    return aut, sirnas


def escanear(aut, sirnas, ruta_db):
    """Una pasada por la base. Devuelve {criterio: {idx_sirna: set(referencias)}}."""
    hits = {"perfecto_21": {}, "perfecto_ge19": {}, "mm1_21": {}}
    for ref, seq in iter_db(ruta_db):
        if not seq:
            continue
        for _, cargas in aut.iter(seq):
            for idx, crit in cargas:
                hits[crit].setdefault(idx, set()).add(ref)
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--consulta", nargs="+", required=True)
    ap.add_argument("--db", nargs="+", required=True,
                    help="FASTA de referencia, admite comodines y .gz")
    ap.add_argument("--mm1", action="store_true",
                    help="buscar tambien 21-meros con exactamente un desajuste")
    ap.add_argument("--salida", required=True)
    a = ap.parse_args(argv)

    dbs = []
    for patron in a.db:
        dbs.extend(sorted(glob.glob(patron)) or [patron])

    print("construyendo automata...", flush=True)
    aut, sirnas = construir(a.consulta, a.mm1)
    print("  %d siRNA, %d patrones%s" % (
        len(sirnas), len(aut), ", con 1 desajuste" if a.mm1 else ""), flush=True)

    salida = Path(a.salida)
    salida.mkdir(parents=True, exist_ok=True)

    # por_sirna[idx][db] = {criterio: n_referencias}
    por_sirna = [{} for _ in sirnas]
    resumen = []
    for ruta in dbs:
        base = Path(ruta).name.replace(".fna.gz", "").replace(".fasta", "")
        print("escaneando %s ..." % base, flush=True)
        hits = escanear(aut, sirnas, ruta)
        for idx in range(len(sirnas)):
            d = {}
            for crit in ("perfecto_21", "perfecto_ge19", "mm1_21"):
                refs = hits[crit].get(idx)
                if refs:
                    d[crit] = len(refs)
            if d:
                por_sirna[idx][base] = d

        # resumen por consulta, con las definiciones de W5
        consultas = sorted({s["consulta"] for s in sirnas})
        for c in consultas:
            ids = [i for i, s in enumerate(sirnas) if s["consulta"] == c]
            n21 = sum(1 for i in ids if i in hits["perfecto_21"])
            n19 = sum(1 for i in ids if i in hits["perfecto_ge19"])
            nmm = sum(1 for i in ids if i in hits["mm1_21"] and i not in hits["perfecto_21"])
            refs = set()
            for crit in ("perfecto_21", "perfecto_ge19"):
                for i in ids:
                    refs |= hits[crit].get(i, set())
            fila = {"base_de_datos": base, "consulta": c,
                    "siRNA_perfecto_ge19": n19, "siRNA_perfecto_21": n21,
                    "siRNA_1mm_21": nmm if a.mm1 else None,
                    "referencias_distintas": len(refs)}
            resumen.append(fila)
            print("   %-14s ge19=%-5d 21/21=%-5d 1mm=%-5s refs=%d" % (
                c, n19, n21, nmm if a.mm1 else "-", len(refs)), flush=True)

    with open(salida / "offtarget_por_sirna.tsv", "w", encoding="utf-8", newline="") as fh:
        bases = [Path(r).name.replace(".fna.gz", "").replace(".fasta", "") for r in dbs]
        fh.write("consulta\tpos\tsirna\t" + "\t".join(
            "%s|%s" % (b, c) for b in bases
            for c in ("perfecto_21", "perfecto_ge19", "mm1_21")) + "\n")
        for s, d in zip(sirnas, por_sirna):
            celdas = []
            for b in bases:
                dd = d.get(b, {})
                for c in ("perfecto_21", "perfecto_ge19", "mm1_21"):
                    celdas.append(str(dd.get(c, 0)))
            fh.write("%s\t%d\t%s\t%s\n" % (s["consulta"], s["pos"], s["sirna"],
                                           "\t".join(celdas)))

    (salida / "offtarget_resumen.json").write_text(
        json.dumps(resumen, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nescrito en %s" % salida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
