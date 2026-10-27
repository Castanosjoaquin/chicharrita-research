#!/usr/bin/env python3
"""Eje 4 de F3 (conservacion entre los tres TSA de D. maidis). Criterio: PREREGISTRO_EJE4.md.

Uso (entorno con BLAST+, biopython y pyahocorasick):
    python research/ola6/F3_recomendador_genes/scripts/05_eje_conservacion.py
Escribe lo versionado en resultados/ (solo conteos) y lo crudo en work/F3_eje4/.
"""
import csv, hashlib, json, subprocess, sys
from pathlib import Path
import ahocorasick

RAIZ = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1] / "resultados"
W = RAIZ / "work/F3_eje4"; W.mkdir(parents=True, exist_ok=True)
REF = RAIZ / "work/W5/ref"
TSAS = ["GCWP01", "GHCC01", "GITV01"]
CAND = {
 "DM-01": ("BicC", "work/sifi_v2/fasta/BicC_Dm_full.fasta"),
 "DM-02": ("V-ATPase B", "research/ola6/O2_vatpase_b/resultados/VATPaseB_Dm_cds.fna"),
 "DM-03": ("V-ATPase D", "work/sifi_v2/fasta/ATPaseD_Dm_full.fasta"),
 "DM-05": ("eth", "work/sifi_v2/fasta/eth_Dm_full.fasta"),
 "DM-06": ("burs-alpha", "work/sifi_v2/fasta/bursA_Dm_full.fasta"),
}
K = 21; MIN_COB = 0.50
COMP = str.maketrans("ACGT", "TGCA")
rc = lambda s: s.translate(COMP)[::-1]

def fasta(p):
    nom, buf = None, []
    for l in Path(p).read_text().splitlines():
        if l.startswith(">"):
            if nom is not None: yield nom, "".join(buf).upper()
            nom, buf = l[1:].split()[0], []
        else: buf.append(l.strip())
    if nom is not None: yield nom, "".join(buf).upper()

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

seqs = {i: next(fasta(RAIZ / r))[1] for i, (_, r) in CAND.items()}
ver = subprocess.run(["blastn", "-version"], capture_output=True, text=True).stdout.splitlines()[1]
meta = {"blastn": ver, "tsa_sha256": {}, "consultas": {i: CAND[i][1] for i in CAND}}
# presencia exacta: automata sobre ventanas de los 5 candidatos, ambas hebras, un pase por TSA
ven = {i: [s[j:j + K] for j in range(len(s) - K + 1)] for i, s in seqs.items()}
A = ahocorasick.Automaton()
for i, vs in ven.items():
    for w in set(vs): A.add_word(w, w)
    for w in set(map(rc, vs)): A.add_word(w, rc(w))
A.make_automaton()
presentes, blast = {}, {}
for t in TSAS:
    f = REF / f"TSA_{t}01.fasta" if not (REF / f"TSA_{t}.fasta").exists() else REF / f"TSA_{t}.fasta"
    meta["tsa_sha256"][t] = sha(f)
    hit = set()
    for _, s in fasta(f):
        for _, w in A.iter(s): hit.add(w)
    presentes[t] = hit
    db = W / f"db_{t}"
    if not Path(str(db) + ".nsq").exists() and not Path(str(db) + ".ndb").exists():
        subprocess.run(["makeblastdb", "-in", str(f), "-dbtype", "nucl", "-out", str(db)], check=True, capture_output=True)
    for i in CAND:
        q = W / f"{i}.fa"; q.write_text(f">{i}\n{seqs[i]}\n")
        r = subprocess.run(["blastn", "-task", "megablast", "-query", str(q), "-db", str(db), "-evalue", "1e-20",
            "-max_target_seqs", "50", "-outfmt", "6 sseqid qstart qend sstart send pident length bitscore"],
            capture_output=True, text=True, check=True).stdout
        (W / f"{i}_{t}.blast.tsv").write_text(r)
        rows = [x.split("\t") for x in r.strip().splitlines()]
        blast[(i, t)] = rows

filas = []
for i, (gen, ruta) in CAND.items():
    L = len(seqs[i]); n = L - K + 1
    cob = {}; ids = {}
    for t in TSAS:
        rows = blast[(i, t)]
        if not rows: cob[t] = set(); ids[t] = "ausente"; continue
        mejor = max(rows, key=lambda x: float(x[7]))[0]
        c = set()
        for x in rows:
            if x[0] != mejor: continue
            a, b = sorted((int(x[1]), int(x[2])))
            c.update(range(a - 1, b))
        ids[t] = mejor
        cob[t] = {j for j in range(n) if all(p in c for p in range(j, j + K))}
    idt = {t: {j for j in cob[t] if ven[i][j] in presentes[t]} for t in TSAS}
    ev3 = set.intersection(*cob.values()); id3 = set.intersection(*(idt[t] & ev3 for t in TSAS))
    r = {"id": i, "gen": gen, "ruta_consulta": ruta, "largo_nt": L, "ventanas_totales": n,
         "contig_GCWP01": ids["GCWP01"], "contig_GHCC01": ids["GHCC01"], "contig_GITV01": ids["GITV01"]}
    for t in TSAS: r[f"con_dato_{t}"] = len(cob[t]); r[f"identicas_{t}"] = len(idt[t])
    r["evaluables_en_los_3"] = len(ev3); r["identicas_en_los_3"] = len(id3)
    r["cobertura"] = round(len(ev3) / n, 4)
    if "ausente" in ids.values(): r["fraccion"], r["estado"] = "", "ausente en algun TSA: cobertura insuficiente"
    elif r["cobertura"] < MIN_COB: r["fraccion"], r["estado"] = "", "cobertura insuficiente"
    else: r["fraccion"], r["estado"] = round(len(id3) / len(ev3), 4), "puntuado"
    filas.append(r)
with open(OUT / "eje4_conservacion.tsv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(filas[0]), delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(filas)
(OUT / "eje4_meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
for r in filas: print({k: r[k] for k in ("id", "ventanas_totales", "evaluables_en_los_3", "identicas_en_los_3", "cobertura", "fraccion", "estado")})
