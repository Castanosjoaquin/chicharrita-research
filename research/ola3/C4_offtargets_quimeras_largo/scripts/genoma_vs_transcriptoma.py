"""Dónde cae cada acierto: genoma, transcriptoma, y en qué clase de región.

Q2 de C4. Toma la salida cruda de `tools/sifi21_port/offtarget_21nt.py` (corrido sin
modificarlo contra genoma y transcriptoma del MISMO organismo) y contesta dos cosas:

  1. Para cada región de EPILAB y cada criterio de riesgo, cuántos siRNA aciertan
     sólo en el genoma, sólo en el transcriptoma, o en los dos. Los que aciertan
     sólo en el transcriptoma son, por construcción, candidatos a unión exón-exón;
     los que aciertan sólo en el genoma son el caso que el investigador propuso
     ponderar menos.
  2. Para los aciertos de genoma, dónde caen contra la anotación: exón de un gen,
     intrón, o intergénico. Esto se mide buscando la posición exacta del k-mero en
     el ensamblado y cruzándola con el GFF de RefSeq.

Sólo se usan organismos que tengan los dos recursos localmente. Los que tienen uno
solo se listan como faltantes y no se cuentan.

Uso:
    python research/ola3/C4_offtargets_quimeras_largo/scripts/genoma_vs_transcriptoma.py
"""

from __future__ import annotations

import bisect
import csv
import gzip
import json
import sys
from collections import defaultdict
from pathlib import Path

import ahocorasick

RAIZ = Path(__file__).resolve().parents[4]
RESULTADOS = Path(__file__).resolve().parents[1] / "resultados"
TSV = RAIZ / "work/C4/offtarget/gen_vs_tx/offtarget_por_sirna.tsv"
PARES = {                      # organismo -> (base_genoma, base_transcriptoma)
    "Zea mays": ("Zmays_genoma.fna", "Zmays_transcriptoma.fna"),
    "Apis mellifera": ("Amel_genoma.fna", "Amel_transcriptoma.fna"),
}
GFF = {
    "Zea mays": RAIZ / "work/W4/downloads/GCF_902167145.1/ncbi_dataset/data/"
                       "GCF_902167145.1/genomic.gff",
    "Apis mellifera": RAIZ / "work/W4/downloads/GCF_003254395.2/ncbi_dataset/data/"
                             "GCF_003254395.2/genomic.gff",
}
GENOMAS = {
    "Zea mays": RAIZ / "work/C4/db/Zmays_genoma.fna",
    "Apis mellifera": RAIZ / "work/C4/db/Amel_genoma.fna",
}
CRITERIOS = ("perfecto_21", "perfecto_ge19", "mm1_21")
COMP = str.maketrans("ACGT", "TGCA")
SIZE, MIN_BLOCK = 21, 19


def rc(s): return s.translate(COMP)[::-1]


def iter_fasta(ruta):
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


def main():
    RESULTADOS.mkdir(parents=True, exist_ok=True)
    filas = list(csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"))
    print("siRNA en la tabla: %d" % len(filas))

    # --- 1. cruce genoma / transcriptoma -------------------------------------
    cruce, interes = [], defaultdict(set)   # interes[organismo] = {secuencias 21nt}
    for org, (bg, bt) in PARES.items():
        for consulta in sorted({f["consulta"] for f in filas}):
            sub = [f for f in filas if f["consulta"] == consulta]
            for crit in CRITERIOS:
                cg = "%s|%s" % (bg, crit)
                ct = "%s|%s" % (bt, crit)
                solo_g = [f for f in sub if int(f[cg] or 0) and not int(f[ct] or 0)]
                solo_t = [f for f in sub if int(f[ct] or 0) and not int(f[cg] or 0)]
                ambos = [f for f in sub if int(f[cg] or 0) and int(f[ct] or 0)]
                cruce.append({"organismo": org, "region": consulta, "criterio": crit,
                              "ventanas": len(sub),
                              "solo_genoma": len(solo_g),
                              "solo_transcriptoma": len(solo_t),
                              "en_los_dos": len(ambos),
                              "pos_solo_genoma": ",".join(f["pos"] for f in solo_g),
                              "pos_solo_transcriptoma": ",".join(f["pos"] for f in solo_t)})
                if crit in ("perfecto_21", "perfecto_ge19"):
                    for f in solo_g + ambos:
                        interes[org].add(f["sirna"])

    with open(RESULTADOS / "q2_cruce_genoma_transcriptoma.tsv", "w", encoding="utf-8",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cruce[0].keys()), delimiter="\t")
        w.writeheader(); w.writerows(cruce)
    for c in cruce:
        if c["solo_genoma"] or c["solo_transcriptoma"] or c["en_los_dos"]:
            print("%-16s %-24s %-14s solo_gen=%d solo_tx=%d ambos=%d" % (
                c["organismo"], c["region"], c["criterio"],
                c["solo_genoma"], c["solo_transcriptoma"], c["en_los_dos"]))

    # --- 2. localizar los aciertos en el ensamblado y clasificarlos -----------
    localizados = []
    for org, sirnas in interes.items():
        if not sirnas:
            continue
        print("\n%s: localizando %d siRNA en el ensamblado" % (org, len(sirnas)))
        aut = ahocorasick.Automaton()
        for s in sorted(sirnas):
            pats = [(s, "perfecto_21", "+"), (rc(s), "perfecto_21", "-")]
            for j in range(SIZE - MIN_BLOCK + 1):
                b = s[j:j + MIN_BLOCK]
                pats.append((b, "perfecto_ge19", "+"))
                pats.append((rc(b), "perfecto_ge19", "-"))
            for p, crit, hebra in pats:
                carga = (s, crit, hebra, len(p))
                if aut.exists(p):
                    aut.get(p).append(carga)
                else:
                    aut.add_word(p, [carga])
        aut.make_automaton()

        hits = []
        for ref, seq in iter_fasta(GENOMAS[org]):
            for fin, cargas in aut.iter(seq):
                for sirna, crit, hebra, largo in cargas:
                    hits.append({"organismo": org, "ref": ref,
                                 "inicio": fin - largo + 2, "fin": fin + 1,
                                 "sirna": sirna, "criterio": crit,
                                 "hebra": hebra, "largo_bloque": largo})
        print("   aciertos en el ensamblado: %d" % len(hits))

        # anotación: exones y genes por secuencia de referencia
        exones, genes = defaultdict(list), defaultdict(list)
        with open(GFF[org], encoding="utf-8", errors="ignore") as fh:
            for linea in fh:
                if linea.startswith("#"):
                    continue
                c = linea.rstrip("\n").split("\t")
                if len(c) < 9:
                    continue
                if c[2] == "exon":
                    exones[c[0]].append((int(c[3]), int(c[4]), c[8]))
                elif c[2] in ("gene", "pseudogene"):
                    genes[c[0]].append((int(c[3]), int(c[4]), c[8]))
        for d in (exones, genes):
            for k in d:
                d[k].sort()

        def solapa(tabla, ref, ini, fin):
            lst = tabla.get(ref, [])
            if not lst:
                return None
            starts = [x[0] for x in lst]
            i = bisect.bisect_right(starts, fin)
            for j in range(max(0, i - 200), i):
                s, e, attr = lst[j]
                if s <= fin and e >= ini:
                    return attr
            return None

        for h in hits:
            at_ex = solapa(exones, h["ref"], h["inicio"], h["fin"])
            at_gen = solapa(genes, h["ref"], h["inicio"], h["fin"])
            if at_ex:
                h["clase"] = "exon"
            elif at_gen:
                h["clase"] = "intron"
            else:
                h["clase"] = "intergenico"
            h["gen"] = ""
            if at_gen:
                for campo in at_gen.split(";"):
                    if campo.startswith("gene="):
                        h["gen"] = campo[5:]
            localizados.append(h)

    if localizados:
        cols = ["organismo", "ref", "inicio", "fin", "hebra", "criterio",
                "largo_bloque", "clase", "gen", "sirna"]
        with open(RESULTADOS / "q2_aciertos_localizados.tsv", "w", encoding="utf-8",
                  newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
            w.writeheader(); w.writerows(localizados)
        resumen = defaultdict(int)
        for h in localizados:
            resumen["%s|%s|%s" % (h["organismo"], h["criterio"], h["clase"])] += 1
        print("\nclasificación de los aciertos en el ensamblado:")
        for k in sorted(resumen):
            print("   %-46s %d" % (k, resumen[k]))
        (RESULTADOS / "q2_resumen.json").write_text(json.dumps(
            {"conteo_por_clase": dict(resumen),
             "pares_usados": {k: list(v) for k, v in PARES.items()}},
            indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nescrito en %s" % RESULTADOS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
