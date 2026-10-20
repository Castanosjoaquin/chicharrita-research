"""Tamizaje de off-targets de ventanas de 21 nt contra referencias locales, por siRNA.

Por qué no BLAST: para lo que importa en RNAi —bloques contiguos perfectos de 19 a
21 nt— la coincidencia exacta es la respuesta correcta y no una heurística. BLAST
con `blastn-short` aproxima eso con semillas, perc_identity y e-value, y hay que
filtrar después. Acá se busca exacto, en una sola pasada por cada base, con un
autómata de Aho-Corasick. Ventaja práctica: el resultado es por siRNA, no un
conteo agregado, que es lo que hace falta para cruzarlo con el perfil de eficiencia.

Criterios, con las mismas definiciones que usó W5 (`analisis/COMANDOS.md` §4):

  perfecto_21     el k-mero aparece idéntico en la referencia.
  perfecto_ge19   algún bloque contiguo de `--min-block` nt o más aparece idéntico.
  mm1_21          el k-mero aparece con exactamente un desajuste (opcional, --mm1).

Los nombres de esas columnas **no cambian** con `--size`: siguen diciendo 21 y 19
aunque k sea otro. Es a propósito, para que la salida con los valores por defecto
sea idéntica a la de antes de parametrizar; el k efectivo va en el resumen JSON, en
los campos `size` y `min_block`, y quien corra con otro k tiene que mirarlo ahí.

Se busca en las dos hebras: se generan los complementos reversos de las consultas,
que es equivalente a recorrer las dos hebras de la referencia y mucho más barato.

El tamaño de ventana es parametrizable con `--size` y el del bloque con
`--min-block`. Los dos valores por defecto son los de siempre —21 y 19— y la salida
con `--size 21` es **idéntica byte a byte** a la de antes de parametrizarlo, lo que
está verificado en esta corrida y registrado en
`research/ola2/W7_ranking/azar_por_k.md`, porque esos conteos se citan en tres
documentos. El parámetro existe para la cuenta de azar por k.

Nada sale de la máquina: las referencias se leen de disco. Uso:

    python offtarget_21nt.py --consulta work/sifi_check/BicC_Dm_sel.fasta \
        --db work/offtarget_db/*.fna.gz --salida work/sifi_check/offtarget --mm1

    python offtarget_21nt.py --size 18 --consulta ... --db ... --salida ...
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
SIZE = 21        # por defecto; `--size` lo cambia y `main` lo propaga
MIN_BLOCK = 19   # por defecto; `--min-block` lo cambia


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
    """Las 3k variantes del k-mero con exactamente un desajuste (63 si k = 21)."""
    for i, base in enumerate(s):
        for alt in "ACGT":
            if alt != base:
                yield s[:i] + alt + s[i + 1:]


def construir(consultas, con_mm1: bool, size: int = SIZE,
              min_block: int = MIN_BLOCK):
    """Arma el autómata y el mapa patrón -> (siRNA, criterio).

    Devuelve (automata, sirnas) donde sirnas es la lista de dicts por ventana.
    """
    aut = ahocorasick.Automaton()
    sirnas = []
    # patron -> lista de (indice_sirna, criterio)
    for ruta in consultas:
        for nombre, seq in leer_fasta(ruta):
            seq = seq.upper().replace("U", "T")
            for i in range(len(seq) - size + 1):
                w = seq[i:i + size]
                if any(b not in "ACGT" for b in w):
                    continue
                idx = len(sirnas)
                sirnas.append({"consulta": nombre, "pos": i + 1, "sirna": w})

                pats = [(w, "perfecto_21"), (rc(w), "perfecto_21")]
                # bloques contiguos de min_block; si alguno esta, hay >=min_block perfecto
                for j in range(size - min_block + 1):
                    b = w[j:j + min_block]
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
                    help="buscar tambien k-meros con exactamente un desajuste")
    ap.add_argument("--size", type=int, default=SIZE,
                    help="tamano de ventana (por defecto 21)")
    ap.add_argument("--min-block", type=int, default=None, dest="min_block",
                    help="tamano del bloque contiguo perfecto (por defecto min(19, size))")
    ap.add_argument("--salida", required=True)
    a = ap.parse_args(argv)
    size = a.size
    min_block = a.min_block if a.min_block is not None else min(MIN_BLOCK, size)
    if not 1 <= min_block <= size:
        sys.exit("--min-block debe estar entre 1 y --size")

    dbs = []
    for patron in a.db:
        dbs.extend(sorted(glob.glob(patron)) or [patron])

    print("construyendo automata...", flush=True)
    aut, sirnas = construir(a.consulta, a.mm1, size, min_block)
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
                    "referencias_distintas": len(refs),
                    "size": size, "min_block": min_block}
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
