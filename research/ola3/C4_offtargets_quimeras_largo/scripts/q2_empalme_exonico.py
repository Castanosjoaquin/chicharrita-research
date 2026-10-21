"""Por qué hay aciertos que están en el transcriptoma y no en el genoma.

Complemento de Q2. La hipótesis es que un bloque perfecto presente en el ARN
mensajero y ausente en el ADN genómico está a caballo de una unión exón-exón: en el
genoma esas dos mitades están separadas por un intrón. Esto se verifica, no se
asume: se localiza el bloque en el transcrito, se reconstruyen las coordenadas de
las uniones de ese transcrito desde el GFF y se mira si el bloque las cruza.

Uso:
    python research/ola3/C4_offtargets_quimeras_largo/scripts/q2_empalme_exonico.py
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
RESULTADOS = Path(__file__).resolve().parents[1] / "resultados"
TX = RAIZ / "work/C4/db/Zmays_transcriptoma.fna"
GFF = (RAIZ / "work/W4/downloads/GCF_902167145.1/ncbi_dataset/data/"
              "GCF_902167145.1/genomic.gff")
REGION = RAIZ / "work/C4/fasta/BicC_Dm_sel.fasta"
POSICIONES = [123, 124, 125]        # ventanas solo-transcriptoma de q2_cruce_*
COMP = str.maketrans("ACGT", "TGCA")
SIZE, MIN_BLOCK = 21, 19


def rc(s): return s.translate(COMP)[::-1]


def main():
    seq = "".join(l.strip() for l in REGION.read_text().splitlines()
                  if not l.startswith(">"))
    consultas = {}
    for p in POSICIONES:
        w = seq[p - 1:p - 1 + SIZE]
        bloques = [w[j:j + MIN_BLOCK] for j in range(SIZE - MIN_BLOCK + 1)]
        consultas[p] = {"ventana": w, "bloques": bloques}

    # localizar en el transcriptoma
    hits = []
    nombre, buf = None, []
    def revisar(nombre, s):
        for p, d in consultas.items():
            for b in d["bloques"]:
                for hebra, pat in (("+", b), ("-", rc(b))):
                    i = s.find(pat)
                    while i != -1:
                        hits.append({"pos_region": p, "transcrito": nombre,
                                     "ini_tx": i + 1, "fin_tx": i + len(pat),
                                     "hebra": hebra, "bloque": pat})
                        i = s.find(pat, i + 1)
    with open(TX, encoding="utf-8") as fh:
        for linea in fh:
            if linea.startswith(">"):
                if nombre is not None:
                    revisar(nombre, "".join(buf))
                nombre, buf = linea[1:].strip().split()[0], []
            else:
                buf.append(linea.strip().upper())
    if nombre is not None:
        revisar(nombre, "".join(buf))
    print("aciertos en el transcriptoma: %d" % len(hits))
    transcritos = sorted({h["transcrito"] for h in hits})
    print("transcritos tocados:", ", ".join(transcritos))

    # estructura exónica de esos transcritos
    exones = defaultdict(list)
    genes = {}
    with open(GFF, encoding="utf-8", errors="ignore") as fh:
        for linea in fh:
            if linea.startswith("#"):
                continue
            c = linea.rstrip("\n").split("\t")
            if len(c) < 9 or c[2] != "exon":
                continue
            attr = c[8]
            padre = ""
            for campo in attr.split(";"):
                if campo.startswith("Parent=rna-"):
                    padre = campo[len("Parent=rna-"):]
            if padre in transcritos:
                exones[padre].append((int(c[3]), int(c[4]), c[6]))
                for campo in attr.split(";"):
                    if campo.startswith("gene="):
                        genes[padre] = campo[5:]

    salida = []
    for h in hits:
        ex = sorted(exones.get(h["transcrito"], []))
        if not ex:
            h.update({"n_exones": 0, "uniones_tx": "", "cruza_union": "sin_anotacion",
                      "gen": genes.get(h["transcrito"], "")})
            salida.append(h); continue
        hebra_tx = ex[0][2]
        largos = [e - s + 1 for s, e, _ in ex]
        if hebra_tx == "-":
            largos = largos[::-1]
        uniones, acum = [], 0
        for L in largos[:-1]:
            acum += L
            uniones.append(acum)          # última base del exón, en coord. de transcrito
        cruza = [u for u in uniones if h["ini_tx"] <= u < h["fin_tx"]]
        h.update({"n_exones": len(ex),
                  "uniones_tx": ",".join(map(str, uniones)),
                  "cruza_union": ",".join(map(str, cruza)) if cruza else "no",
                  "gen": genes.get(h["transcrito"], "")})
        salida.append(h)

    cols = ["pos_region", "transcrito", "gen", "ini_tx", "fin_tx", "hebra",
            "n_exones", "cruza_union", "uniones_tx", "bloque"]
    with open(RESULTADOS / "q2_empalme_exonico.tsv", "w", encoding="utf-8",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader(); w.writerows(salida)
    for h in salida:
        print("pos %-4d %-16s %-16s tx %d-%d exones %d  cruza_union %s" % (
            h["pos_region"], h["transcrito"], h["gen"], h["ini_tx"], h["fin_tx"],
            h["n_exones"], h["cruza_union"]))
    n_cruza = sum(1 for h in salida if h["cruza_union"] not in ("no", "sin_anotacion"))
    print("\nbloques que cruzan una unión exón-exón: %d de %d" % (n_cruza, len(salida)))
    (RESULTADOS / "q2_empalme_resumen.json").write_text(json.dumps(
        {"bloques_examinados": len(salida), "cruzan_union": n_cruza,
         "posiciones_region": POSICIONES}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
