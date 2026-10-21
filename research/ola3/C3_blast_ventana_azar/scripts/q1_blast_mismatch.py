#!/usr/bin/env python3
"""Q1 - que configuracion de BLAST+ encuentra un 21-mero con un desajuste, y donde falla.

Dos partes.

A. Valores por defecto MEDIDOS en el binario (no copiados de la documentacion).
   Se construye un par consulta/sujeto cuyo unico calce exacto posible es un bloque
   plantado, porque el fondo de la consulta usa solo {A,C} y el del sujeto solo
   {G,T}. Se corre con `-strand plus`: sin eso, la hebra menos de la consulta es
   {T,G} y calza con el fondo del sujeto, y la medicion se arruina.
     - tamano de palabra: el menor bloque exacto L que produce un acierto.
     - premio: puntaje crudo de un bloque perfecto, S = L * premio.
     - penalidad: bloque con un desajuste central, S = (L-1) * premio + penalidad.
     - costos de hueco: bloques con deleciones de 1, 2 y 3 nt; se resuelve el sistema
       y se verifica con la tercera ecuacion (si no cierra, se declara ambiguo).
     - max_hsps, perc_identity y qcov_hsp_perc: un sujeto con tres copias del mismo
       bloque, y aciertos de identidad y cobertura bajas.

B. Sensibilidad por posicion del desajuste. Se toman 21-meros de la propia
   referencia, se planta un desajuste en cada posicion 1..21 y se mide que fraccion
   recupera cada configuracion, exigiendo que el acierto caiga en el locus de origen.
   Control: por construccion cada consulta tiene un calce de 21 nt con exactamente
   un desajuste en ese locus; se verifica por comparacion de subcadenas en Python,
   que es busqueda exacta y no heuristica.

Uso:
    python q1_blast_mismatch.py --salida <dir>
"""
from __future__ import annotations

import argparse
import gzip
import json
import random
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path("/Users/joaquin/Documents/investigaton/chicharrita-research")
TRABAJO = RAIZ / "work/C3/blast"
DBDIR = RAIZ / "work/W5/db"
REFDIR = RAIZ / "work/W5/ref"
ALT = {"A": "CGT", "C": "AGT", "G": "ACT", "T": "ACG"}
HILOS = "8"
COMANDOS: list[str] = []


def corr(cmd, **kw):
    COMANDOS.append(" ".join(cmd))
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


# --- Parte A ---------------------------------------------------------------

def parte_a(sal: Path):
    rnd = random.Random(7)
    d = TRABAJO / "defaults"
    d.mkdir(parents=True, exist_ok=True)
    B = lambda n: "".join(rnd.choice("ACGT") for _ in range(n))
    F = lambda n, al: "".join(rnd.choice(al) for _ in range(n))

    q, s = [], []
    for L in range(4, 41):
        b = B(L)
        q.append(">L%02d\n%s%s%s\n" % (L, F(100, "AC"), b, F(100, "AC")))
        s.append(">L%02d\n%s%s%s\n" % (L, F(100, "GT"), b, F(100, "GT")))
    (d / "ws_q.fa").write_text("".join(q))
    (d / "ws_s.fa").write_text("".join(s))

    q2, s2 = [], []
    b41 = B(41)
    q2.append(">mm1\n%s%s%s\n" % (F(80, "AC"), b41, F(80, "AC")))
    s2.append(">mm1\n%s%s%s\n" % (F(80, "GT"),
                                  b41[:20] + ("A" if b41[20] != "A" else "G") + b41[21:],
                                  F(80, "GT")))
    b57 = B(57)   # lados de 28: megablast tambien puede sembrar
    q2.append(">mm1mb\n%s%s%s\n" % (F(80, "AC"), b57, F(80, "AC")))
    s2.append(">mm1mb\n%s%s%s\n" % (F(80, "GT"),
                                    b57[:28] + ("A" if b57[28] != "A" else "G") + b57[29:],
                                    F(80, "GT")))
    b61 = B(61)
    for g in (1, 2, 3):
        q2.append(">gap%d\n%s%s%s\n" % (g, F(80, "AC"), b61, F(80, "AC")))
        s2.append(">gap%d\n%s%s%s\n" % (g, F(80, "GT"), b61[:30] + b61[30 + g:], F(80, "GT")))
    b40 = B(40)
    q2.append(">hsp\n%s%s%s\n" % (F(40, "AC"), b40, F(40, "AC")))
    s2.append(">hsp\n%s%s%s%s%s%s\n" % (F(40, "GT"), b40, F(40, "GT"), b40, F(40, "GT"), b40))
    b90 = B(90)   # identidad 90 %: un desajuste cada 10 nt, corridas exactas de 9
    lo = list(b90)
    for i in range(4, 90, 10):
        lo[i] = {"A": "C", "C": "A", "G": "T", "T": "G"}[lo[i]]
    q2.append(">id90\n%s%s%s\n" % (F(60, "AC"), b90, F(60, "AC")))
    s2.append(">id90\n%s%s%s\n" % (F(60, "GT"), "".join(lo), F(60, "GT")))
    (d / "pen_q.fa").write_text("".join(q2))
    (d / "pen_s.fa").write_text("".join(s2))

    fmt = "6 qseqid sseqid pident length mismatch gapopen gaps score bitscore evalue qcovhsp"
    out = {}
    for tarea in ("megablast", "blastn", "blastn-short", "dc-megablast"):
        r1 = corr(["blastn", "-task", tarea, "-query", str(d / "ws_q.fa"),
                   "-subject", str(d / "ws_s.fa"), "-strand", "plus", "-evalue", "1e9",
                   "-dust", "no", "-soft_masking", "false", "-outfmt", fmt])
        (d / ("ws_%s.tsv" % tarea)).write_text(r1.stdout)
        minL = premio = None
        for ln in r1.stdout.splitlines():
            c = ln.split("\t")
            if c[0] != c[1]:
                continue
            L = int(c[0][1:])
            if int(c[3]) == L and int(c[4]) == 0 and int(c[5]) == 0 and (minL is None or L < minL):
                minL, premio = L, int(c[7]) / L
        r2 = corr(["blastn", "-task", tarea, "-query", str(d / "pen_q.fa"),
                   "-subject", str(d / "pen_s.fa"), "-strand", "plus", "-evalue", "1e9",
                   "-dust", "no", "-soft_masking", "false", "-outfmt", fmt])
        (d / ("pen_%s.tsv" % tarea)).write_text(r2.stdout)
        filas = [l.split("\t") for l in r2.stdout.splitlines()]
        filas = [c for c in filas if c[0] == c[1]]

        def mejor(q, cond):
            cs = [c for c in filas if c[0] == q and cond(c)]
            return max(cs, key=lambda c: int(c[7])) if cs else None

        pen = None
        for nombre, largo in (("mm1", 41), ("mm1mb", 57)):
            c = mejor(nombre, lambda c: int(c[3]) == largo and int(c[4]) == 1 and int(c[5]) == 0)
            if c and premio:
                pen = int(c[7]) - (largo - 1) * premio
                break
        # huecos: S(g) = (61-g)*premio - (apertura + g*extension), puntajes truncados
        sc = {}
        for g in (1, 2, 3):
            c = mejor("gap%d" % g, lambda c: int(c[6]) == g)
            sc[g] = int(c[7]) if c else None
        ext = aper = coherente = None
        if premio and all(sc[g] is not None for g in (1, 2, 3)):
            costo = {g: (61 - g) * premio - sc[g] for g in (1, 2, 3)}
            ext = costo[2] - costo[1]
            aper = costo[1] - ext
            coherente = abs((aper + 3 * ext) - costo[3]) < 1e-9
        nh = len([c for c in filas if c[0] == "hsp" and int(c[3]) == 40])
        id90 = mejor("id90", lambda c: int(c[3]) >= 80)
        out[tarea] = {
            "word_size_medido": minL, "reward_medido": premio, "penalty_medido": pen,
            "puntajes_hueco": sc, "gapextend_medido": ext, "gapopen_medido": aper,
            "modelo_de_hueco_coherente_con_g3": coherente,
            "hsp_de_40nt_reportados_en_un_sujeto": nh,
            "menor_cobertura_reportada_pct": min((float(c[10]) for c in filas), default=None),
            "menor_identidad_reportada_pct": min((float(c[2]) for c in filas), default=None),
            "acierto_identidad_90pct": None if not id90 else {
                "largo": int(id90[3]), "pident": float(id90[2]), "qcovhsp": float(id90[10])},
        }
    (sal / "q1_defaults_medidos.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    return out


# --- Parte B ---------------------------------------------------------------

CONFIGS = {
    "C1_megablast_defecto":     ["-task", "megablast"],
    "C2_blastn_defecto":        ["-task", "blastn"],
    "C3_short_defecto_ws7":     ["-task", "blastn-short"],
    "C4_short_ws11":            ["-task", "blastn-short", "-word_size", "11"],
    "C5_short_ws10":            ["-task", "blastn-short", "-word_size", "10"],
    "C6_short_ws8":             ["-task", "blastn-short", "-word_size", "8"],
    "C7_blastn_ws11_ungapped":  ["-task", "blastn", "-word_size", "11", "-ungapped",
                                 "-dust", "no", "-soft_masking", "false"],
    "C8_short_ws7_ungapped":    ["-task", "blastn-short", "-word_size", "7", "-ungapped",
                                 "-dust", "no", "-soft_masking", "false",
                                 "-evalue", "1000", "-max_target_seqs", "5000"],
    "C9_short_ws4":             ["-task", "blastn-short", "-word_size", "4"],
    "C10_blastn_ws21":          ["-task", "blastn", "-word_size", "21"],
    "C12_short_ws10_ungapped":  ["-task", "blastn-short", "-word_size", "10", "-ungapped",
                                 "-dust", "no", "-soft_masking", "false",
                                 "-evalue", "1000", "-max_target_seqs", "5000"],
}
# C11 no se corre: es C8 (o C12 en el genoma) filtrado por E-value <= 0,05, que es el
# valor por defecto del formulario web. Se deriva de la salida cruda.
PLAN = {
    "sintetica_5Mb":       list(CONFIGS),
    "Zmays_transcriptoma": ["C1_megablast_defecto", "C2_blastn_defecto", "C3_short_defecto_ws7",
                            "C4_short_ws11", "C5_short_ws10", "C6_short_ws8",
                            "C8_short_ws7_ungapped", "C10_blastn_ws21"],
    "Dmaidis_genoma":      ["C1_megablast_defecto", "C2_blastn_defecto", "C4_short_ws11",
                            "C5_short_ws10", "C12_short_ws10_ungapped", "C10_blastn_ws21"],
}


def leer_fasta_gz(ruta):
    op = gzip.open if str(ruta).endswith(".gz") else open
    name, buf = None, []
    with op(ruta, "rt") as fh:
        for line in fh:
            if line.startswith(">"):
                if name is not None:
                    yield name, "".join(buf)
                name, buf = line[1:].split()[0], []
            else:
                buf.append(line.strip().upper())
    if name is not None:
        yield name, "".join(buf)


def muestrear_de_fasta(ruta, n, semilla, min_largo=2000):
    """n 21-meros con su locus (id, inicio 1-based), muestreados en una sola pasada."""
    rnd = random.Random(semilla)
    res, vistos = [], 0
    for name, seq in leer_fasta_gz(ruta):
        if len(seq) < min_largo:
            continue
        vistos += 1
        # muestreo de reservorio a nivel de registro
        for _ in range(3):
            i = rnd.randrange(0, len(seq) - 21)
            w = seq[i:i + 21]
            if set(w) > set("ACGT"):
                continue
            cand = (name, i + 1, w)
            if len(res) < n:
                res.append(cand)
            else:
                j = rnd.randrange(vistos)
                if j < n:
                    res[j] = cand
    return res


def db_sintetica(path: Path, nbases=5_000_000, semilla=2026):
    rnd = random.Random(semilla)
    seq = "".join(rnd.choice("ACGT") for _ in range(nbases))
    fa = path.with_suffix(".fa")
    nombre = "sintetica_uniforme_%d" % nbases
    with open(fa, "w") as fh:
        fh.write(">%s\n" % nombre)
        for i in range(0, nbases, 80):
            fh.write(seq[i:i + 80] + "\n")
    r = corr(["makeblastdb", "-in", str(fa), "-dbtype", "nucl", "-out", str(path)])
    assert r.returncode == 0, r.stderr
    return seq, nombre


def multiplicidad(db: Path, fuentes, etiqueta, tmp: Path):
    fa = tmp / ("fuentes_%s.fa" % etiqueta)
    fa.write_text("".join(">f%03d\n%s\n" % (i, w) for i, (_, _, w) in enumerate(fuentes)))
    r = corr(["blastn", "-task", "blastn", "-word_size", "21", "-ungapped", "-dust", "no",
              "-soft_masking", "false", "-evalue", "1000", "-perc_identity", "100",
              "-max_target_seqs", "5000", "-num_threads", HILOS,
              "-query", str(fa), "-db", str(db), "-outfmt", "6 qseqid length mismatch"])
    cuenta = {}
    for ln in r.stdout.splitlines():
        c = ln.split("\t")
        if int(c[1]) == 21 and int(c[2]) == 0:
            cuenta["f%03d" % 0 if False else c[0]] = cuenta.get(c[0], 0) + 1
    return [cuenta.get("f%03d" % i, 0) for i in range(len(fuentes))]


def consultas_mutadas(fuentes, tmp: Path, etiqueta, todas_las_bases, semilla=5):
    rnd = random.Random(semilla)
    reg, lineas = [], []
    for i, (sid, ini, w) in enumerate(fuentes):
        for p in range(1, 22):
            alts = ALT[w[p - 1]] if todas_las_bases else rnd.choice(ALT[w[p - 1]])
            for b in alts:
                qid = "f%03d_p%02d_%s" % (i, p, b)
                mut = w[:p - 1] + b + w[p:]
                assert sum(x != y for x, y in zip(mut, w)) == 1, "control de Hamming"
                reg.append({"qid": qid, "fuente": i, "sid": sid, "ini": ini,
                            "pos": p, "base": b, "orig": w, "mut": mut})
                lineas.append(">%s\n%s\n" % (qid, mut))
    fa = tmp / ("consultas_%s.fa" % etiqueta)
    fa.write_text("".join(lineas))
    return fa, reg


def analizar(out: Path, reg, evalue_max=None):
    """Por consulta: mejor acierto EN EL LOCUS DE ORIGEN."""
    porq = {r["qid"]: r for r in reg}
    est = {}
    for ln in out.read_text().splitlines():
        c = ln.split("\t")
        q = c[0]
        r = porq.get(q)
        if r is None:
            continue
        sid, pid, L, mm, go = c[1], float(c[2]), int(c[3]), int(c[4]), int(c[5])
        ss, se, ev = int(c[6]), int(c[7]), float(c[8])
        if evalue_max is not None and ev > evalue_max:
            continue
        if sid != r["sid"] and not (sid in r["sid"] or r["sid"] in sid):
            continue
        lo, hi = min(ss, se), max(ss, se)
        if hi < r["ini"] or lo > r["ini"] + 20:      # debe solapar el locus plantado
            continue
        d = est.setdefault(q, {"len_mm1": 0, "len_perf": 0, "n": 0, "mejor_ev": None})
        d["n"] += 1
        if go == 0 and mm <= 1:
            d["len_mm1"] = max(d["len_mm1"], L)
        if go == 0 and mm == 0:
            d["len_perf"] = max(d["len_perf"], L)
        d["mejor_ev"] = ev if d["mejor_ev"] is None else min(d["mejor_ev"], ev)
    return est


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True)
    a = ap.parse_args()
    sal = Path(a.salida); sal.mkdir(parents=True, exist_ok=True)
    tmp = TRABAJO; tmp.mkdir(parents=True, exist_ok=True)

    print("== Parte A: valores por defecto medidos en el binario", flush=True)
    defaults = parte_a(sal)
    for t, v in defaults.items():
        print("   %-14s ws=%s reward=%s penalty=%s open=%s ext=%s coherente=%s hsps=%s" %
              (t, v["word_size_medido"], v["reward_medido"], v["penalty_medido"],
               v["gapopen_medido"], v["gapextend_medido"],
               v["modelo_de_hueco_coherente_con_g3"],
               v["hsp_de_40nt_reportados_en_un_sujeto"]), flush=True)

    print("== Parte B: sensibilidad por posicion del desajuste", flush=True)
    seq, nom = db_sintetica(tmp / "sintetica")
    bases = [
        ("sintetica_5Mb", tmp / "sintetica", None, 50, True),
        ("Zmays_transcriptoma", DBDIR / "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna",
         REFDIR / "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna.fna.gz", 15, False),
        ("Dmaidis_genoma", DBDIR / "GCA_975739785.1_ihDalMaid1.1_genomic",
         REFDIR / "GCA_975739785.1_ihDalMaid1.1_genomic.fna.gz", 15, False),
    ]
    filas, resumen = [], []
    for etiqueta, db, ref, nf, todas in bases:
        print(" -- base %s" % etiqueta, flush=True)
        if ref is None:
            rnd = random.Random(31)
            fuentes = []
            while len(fuentes) < nf:
                i = rnd.randrange(0, len(seq) - 21)
                fuentes.append((nom, i + 1, seq[i:i + 21]))
        else:
            t0 = time.time()
            fuentes = muestrear_de_fasta(ref, nf, semilla=31)
            print("    muestreo del FASTA en %.0f s" % (time.time() - t0), flush=True)
        mult = multiplicidad(db, fuentes, etiqueta, tmp)
        print("    %d fuentes; multiplicidad exacta: %s" % (len(fuentes), mult), flush=True)
        fuentes = [f for f, m in zip(fuentes, mult) if m >= 1]
        mult = [m for m in mult if m >= 1]
        fa, reg = consultas_mutadas(fuentes, tmp, etiqueta, todas_las_bases=todas)
        fmt = "6 qseqid sseqid pident length mismatch gapopen sstart send evalue bitscore"
        for nombre in PLAN[etiqueta]:
            out = tmp / ("blast_%s_%s.tsv" % (etiqueta, nombre))
            t0 = time.time()
            r = corr(["blastn"] + CONFIGS[nombre] +
                     ["-query", str(fa), "-db", str(db), "-num_threads", HILOS,
                      "-outfmt", fmt, "-out", str(out)])
            dt = time.time() - t0
            if r.returncode != 0:
                print("   FALLO %s: %s" % (nombre, r.stderr.strip()[:200]), flush=True)
                continue
            variantes = [(nombre, None)]
            if nombre in ("C8_short_ws7_ungapped", "C12_short_ws10_ungapped"):
                variantes.append(("C11_" + nombre.split("_", 1)[1] + "_evalue0.05", 0.05))
            for vname, evmax in variantes:
                est = analizar(out, reg, evalue_max=evmax)
                for p in range(1, 22):
                    sub = [x for x in reg if x["pos"] == p]
                    e = [est.get(x["qid"]) for x in sub]
                    filas.append({
                        "base": etiqueta, "config": vname, "pos_desajuste": p, "n": len(sub),
                        "sens_21nt_1mm": sum(1 for d in e if d and d["len_mm1"] == 21) / len(sub),
                        "sens_ge20nt": sum(1 for d in e if d and d["len_mm1"] >= 20) / len(sub),
                        "sens_algun_hsp_en_locus": sum(1 for d in e if d) / len(sub),
                        "largo_medio_recuperado": (sum(d["len_mm1"] for d in e if d) /
                                                   max(1, sum(1 for d in e if d))),
                    })
                g = [est.get(x["qid"]) for x in reg]
                resumen.append({
                    "base": etiqueta, "config": vname, "consultas": len(reg),
                    "fuentes": len(fuentes), "multiplicidad_exacta": mult,
                    "sens_21nt_1mm_global": sum(1 for d in g if d and d["len_mm1"] == 21) / len(reg),
                    "sens_ge20nt_global": sum(1 for d in g if d and d["len_mm1"] >= 20) / len(reg),
                    "sens_algun_hsp_global": sum(1 for d in g if d) / len(reg),
                    "segundos": dt if evmax is None else None,
                    "salida_cruda": str(out),
                    "comando": " ".join(["blastn"] + CONFIGS[nombre] +
                                        ["-query", str(fa), "-db", str(db),
                                         "-num_threads", HILOS, "-outfmt", '"%s"' % fmt,
                                         "-out", str(out)]) +
                               ("" if evmax is None else "   # + filtro E-value <= 0,05 sobre la salida"),
                })
                print("   %-34s %6.1f s  21/21+1mm=%.3f  >=20nt=%.3f" %
                      (vname, dt, resumen[-1]["sens_21nt_1mm_global"],
                       resumen[-1]["sens_ge20nt_global"]), flush=True)
        with open(sal / "q1_sensibilidad_posicion.tsv", "w") as fh:
            cols = list(filas[0].keys())
            fh.write("\t".join(cols) + "\n")
            for f in filas:
                fh.write("\t".join(str(f[c]) for c in cols) + "\n")
        (sal / "q1_resumen.json").write_text(json.dumps(resumen, indent=1, ensure_ascii=False))
        (sal / "q1_comandos.txt").write_text("\n".join(COMANDOS) + "\n")
    print("escrito en", sal, flush=True)


if __name__ == "__main__":
    main()
