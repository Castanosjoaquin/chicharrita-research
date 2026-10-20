#!/usr/bin/env python3
"""Q1 - que configuracion de BLAST+ encuentra un 21-mero con un desajuste, y donde falla.

Dos partes.

A. Valores por defecto MEDIDOS en el binario (no copiados de la documentacion):
   - tamano de palabra: se construye un par consulta/sujeto cuyo unico calce exacto
     posible es un bloque plantado de largo L, porque el fondo de la consulta usa
     solo {A,C} y el del sujeto solo {G,T}. Se corre con `-strand plus` (sin eso, la
     hebra menos de la consulta es {T,G} y calza con el fondo del sujeto). El menor L
     que produce un acierto es el tamano de palabra efectivo de la tarea.
   - premio y penalidad: del puntaje crudo de un bloque perfecto (S = L*premio) y de
     uno con un desajuste central (S = (L-1)*premio + penalidad).
   - costos de hueco: de bloques con deleciones de 1 y 2 nt, resolviendo el sistema.
   - max_hsps y los filtros de identidad y cobertura: un sujeto con tres copias del
     mismo bloque, y un acierto de cobertura baja.

B. Sensibilidad por posicion del desajuste. Se toman 21-meros de la propia base,
   se planta un desajuste en cada posicion 1..21 (con cada una de las tres bases
   alternativas), y se mide que fraccion recupera cada configuracion. El control es
   que, por construccion, cada consulta TIENE un calce de 21 nt con exactamente un
   desajuste en el locus de origen: se verifica por subcadena extraida con blastdbcmd.

Uso:
    python q1_blast_mismatch.py --salida <dir> [--fuentes 50]
"""
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path("/Users/joaquin/Documents/investigaton/chicharrita-research")
TRABAJO = RAIZ / "work/C3/blast"
DBDIR = RAIZ / "work/W5/db"
COMP = str.maketrans("ACGT", "TGCA")
ALT = {"A": "CGT", "C": "AGT", "G": "ACT", "T": "ACG"}

COMANDOS: list[str] = []


def corr(cmd, **kw):
    COMANDOS.append(" ".join(cmd))
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


# --- Parte A ---------------------------------------------------------------

def fondo(rnd, n, alfa):
    return "".join(rnd.choice(alfa) for _ in range(n))


def parte_a(sal: Path):
    rnd = random.Random(7)
    d = TRABAJO / "defaults"
    d.mkdir(parents=True, exist_ok=True)
    B = lambda n: "".join(rnd.choice("ACGT") for _ in range(n))

    # A1 tamano de palabra
    q, s = [], []
    for L in range(4, 41):
        b = B(L)
        q.append(">L%02d\n%s%s%s\n" % (L, fondo(rnd, 100, "AC"), b, fondo(rnd, 100, "AC")))
        s.append(">L%02d\n%s%s%s\n" % (L, fondo(rnd, 100, "GT"), b, fondo(rnd, 100, "GT")))
    (d / "ws_q.fa").write_text("".join(q))
    (d / "ws_s.fa").write_text("".join(s))

    # A2/A3/A4 premio, penalidad, huecos, max_hsps, filtros
    q2, s2 = [], []
    b41 = B(41)
    b41m = b41[:20] + ("A" if b41[20] != "A" else "G") + b41[21:]
    q2.append(">mm1\n%s%s%s\n" % (fondo(rnd, 80, "AC"), b41, fondo(rnd, 80, "AC")))
    s2.append(">mm1\n%s%s%s\n" % (fondo(rnd, 80, "GT"), b41m, fondo(rnd, 80, "GT")))
    b57 = B(57)                       # lados de 28, para que megablast tambien siembre
    b57m = b57[:28] + ("A" if b57[28] != "A" else "G") + b57[29:]
    q2.append(">mm1mb\n%s%s%s\n" % (fondo(rnd, 80, "AC"), b57, fondo(rnd, 80, "AC")))
    s2.append(">mm1mb\n%s%s%s\n" % (fondo(rnd, 80, "GT"), b57m, fondo(rnd, 80, "GT")))
    b61 = B(61)
    q2.append(">gap1\n%s%s%s\n" % (fondo(rnd, 80, "AC"), b61, fondo(rnd, 80, "AC")))
    s2.append(">gap1\n%s%s%s\n" % (fondo(rnd, 80, "GT"), b61[:30] + b61[31:], fondo(rnd, 80, "GT")))
    q2.append(">gap2\n%s%s%s\n" % (fondo(rnd, 80, "AC"), b61, fondo(rnd, 80, "AC")))
    s2.append(">gap2\n%s%s%s\n" % (fondo(rnd, 80, "GT"), b61[:30] + b61[32:], fondo(rnd, 80, "GT")))
    b40 = B(40)
    q2.append(">hsp\n%s%s%s\n" % (fondo(rnd, 40, "AC"), b40, fondo(rnd, 40, "AC")))
    s2.append(">hsp\n%s%s%s%s%s%s\n" % (fondo(rnd, 40, "GT"), b40, fondo(rnd, 40, "GT"),
                                        b40, fondo(rnd, 40, "GT"), b40))
    b90 = B(90)                        # identidad 90 %: desajuste cada 10 nt
    lo = list(b90)
    for i in range(4, 90, 10):
        lo[i] = {"A": "C", "C": "A", "G": "T", "T": "G"}[lo[i]]
    q2.append(">id90\n%s%s%s\n" % (fondo(rnd, 60, "AC"), b90, fondo(rnd, 60, "AC")))
    s2.append(">id90\n%s%s%s\n" % (fondo(rnd, 60, "GT"), "".join(lo), fondo(rnd, 60, "GT")))
    (d / "pen_q.fa").write_text("".join(q2))
    (d / "pen_s.fa").write_text("".join(s2))

    fmt = "6 qseqid sseqid pident length mismatch gapopen gaps score bitscore evalue qcovhsp"
    out = {}
    for tarea in ("megablast", "blastn", "blastn-short", "dc-megablast"):
        r1 = corr(["blastn", "-task", tarea, "-query", str(d / "ws_q.fa"),
                   "-subject", str(d / "ws_s.fa"), "-strand", "plus", "-evalue", "1e9",
                   "-dust", "no", "-soft_masking", "false", "-outfmt", fmt])
        (d / ("ws_%s.tsv" % tarea)).write_text(r1.stdout)
        minL, premio = None, None
        for ln in r1.stdout.splitlines():
            c = ln.split("\t")
            if c[0] != c[1]:
                continue
            L = int(c[0][1:])
            if int(c[3]) == L and int(c[4]) == 0 and int(c[5]) == 0:
                if minL is None or L < minL:
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
        g1 = mejor("gap1", lambda c: int(c[6]) == 1)
        g2 = mejor("gap2", lambda c: int(c[6]) == 2)
        ext = aper = None
        if g1 and g2 and premio:
            s1, s2_ = int(g1[7]), int(g2[7])
            ext = (60 * premio - s1) - (59 * premio - s2_) + 2 * (0)   # placeholder
            ext = (59 * premio - s2_) - (60 * premio - s1)
            aper = (60 * premio - s1) - ext
        nh = len([c for c in filas if c[0] == "hsp" and int(c[3]) == 40])
        id90 = mejor("id90", lambda c: int(c[3]) >= 80)
        out[tarea] = {
            "word_size_medido": minL, "reward_medido": premio, "penalty_medido": pen,
            "gapextend_medido": ext, "gapopen_medido": aper,
            "hsp_de_40nt_reportados_en_un_sujeto": nh,
            "menor_cobertura_reportada_pct": min((float(c[10]) for c in filas), default=None),
            "menor_identidad_reportada_pct": min((float(c[2]) for c in filas), default=None),
            "acierto_identidad_90pct": None if not id90 else {
                "largo": int(id90[3]), "pident": float(id90[2]), "qcovhsp": float(id90[10])},
        }
    (sal / "q1_defaults_medidos.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    return out


# --- Parte B ---------------------------------------------------------------

CONFIGS = [
    ("C1_megablast_defecto",      ["-task", "megablast"]),
    ("C2_blastn_defecto",         ["-task", "blastn"]),
    ("C3_blastn-short_defecto",   ["-task", "blastn-short"]),
    ("C4_short_ws11",             ["-task", "blastn-short", "-word_size", "11"]),
    ("C5_short_ws10",             ["-task", "blastn-short", "-word_size", "10"]),
    ("C6_short_ws8",              ["-task", "blastn-short", "-word_size", "8"]),
    ("C7_blastn_ws11_ungapped",   ["-task", "blastn", "-word_size", "11", "-ungapped",
                                   "-dust", "no", "-soft_masking", "false"]),
    ("C8_short_ws7_ungapped",     ["-task", "blastn-short", "-word_size", "7", "-ungapped",
                                   "-dust", "no", "-soft_masking", "false",
                                   "-evalue", "1000", "-max_target_seqs", "5000"]),
    ("C9_short_ws4",              ["-task", "blastn-short", "-word_size", "4"]),
    ("C10_blastn_ws21",           ["-task", "blastn", "-word_size", "21"]),
    ("C11_short_ws7_evalue0.05",  ["-task", "blastn-short", "-word_size", "7", "-ungapped",
                                   "-dust", "no", "-soft_masking", "false",
                                   "-evalue", "0.05", "-max_target_seqs", "5000"]),
]
SOLO_CHICAS = {"C9_short_ws4"}
CONFIGS_GENOMA = {"C1_megablast_defecto", "C2_blastn_defecto", "C3_blastn-short_defecto",
                  "C4_short_ws11", "C5_short_ws10", "C8_short_ws7_ungapped",
                  "C11_short_ws7_evalue0.05"}


def rc(s):
    return s.translate(COMP)[::-1]


def db_sintetica(path: Path, nbases=5_000_000, semilla=2026):
    rnd = random.Random(semilla)
    seq = "".join(rnd.choice("ACGT") for _ in range(nbases))
    fa = path.with_suffix(".fa")
    with open(fa, "w") as fh:
        fh.write(">sintetica_uniforme_%d\n" % nbases)
        for i in range(0, nbases, 80):
            fh.write(seq[i:i + 80] + "\n")
    r = corr(["makeblastdb", "-in", str(fa), "-dbtype", "nucl", "-out", str(path)])
    assert r.returncode == 0, r.stderr
    return seq


def muestrear_21meros(db: Path, n: int, semilla: int, seq_mem: str | None = None):
    """Devuelve 21-meros tomados de la base, validados por subcadena."""
    rnd = random.Random(semilla)
    fuentes = []
    if seq_mem is not None:
        while len(fuentes) < n:
            i = rnd.randrange(0, len(seq_mem) - 21)
            w = seq_mem[i:i + 21]
            if set(w) <= set("ACGT"):
                fuentes.append((("sintetica_uniforme_%d" % len(seq_mem)), i + 1, w))
        return fuentes
    info = corr(["blastdbcmd", "-db", str(db), "-info"]).stdout
    ids = corr(["blastdbcmd", "-db", str(db), "-entry", "all", "-outfmt", "%i %l"]).stdout.splitlines()
    ids = [l.split() for l in ids if l.strip()]
    ids = [(a, int(b)) for a, b in ids if int(b) > 2000]
    intentos = 0
    while len(fuentes) < n and intentos < n * 40:
        intentos += 1
        sid, L = ids[rnd.randrange(len(ids))]
        ini = rnd.randrange(1, L - 25)
        r = corr(["blastdbcmd", "-db", str(db), "-entry", sid,
                  "-range", "%d-%d" % (ini, ini + 20), "-outfmt", "%s"])
        w = r.stdout.strip().upper()
        if len(w) == 21 and set(w) <= set("ACGT"):
            fuentes.append((sid, ini, w))
    return fuentes


def unicos(db: Path, fuentes, etiqueta, tmp: Path):
    """Deja solo los 21-meros con una unica aparicion exacta (las dos hebras)."""
    fa = tmp / ("fuentes_%s.fa" % etiqueta)
    fa.write_text("".join(">f%03d\n%s\n" % (i, w) for i, (_, _, w) in enumerate(fuentes)))
    r = corr(["blastn", "-task", "blastn", "-word_size", "21", "-ungapped", "-dust", "no",
              "-soft_masking", "false", "-evalue", "1000", "-perc_identity", "100",
              "-max_target_seqs", "5000", "-num_threads", "6",
              "-query", str(fa), "-db", str(db), "-outfmt", "6 qseqid length mismatch"])
    cuenta = {}
    for ln in r.stdout.splitlines():
        c = ln.split("\t")
        if int(c[1]) == 21 and int(c[2]) == 0:
            cuenta[c[0]] = cuenta.get(c[0], 0) + 1
    return [f for i, f in enumerate(fuentes) if cuenta.get("f%03d" % i, 0) == 1], cuenta


def consultas_mutadas(fuentes, tmp: Path, etiqueta, todas_las_bases=True, semilla=5):
    rnd = random.Random(semilla)
    reg, lineas = [], []
    for i, (sid, ini, w) in enumerate(fuentes):
        for p in range(1, 22):
            alts = ALT[w[p - 1]] if todas_las_bases else rnd.choice(ALT[w[p - 1]])
            for b in alts:
                qid = "f%03d_p%02d_%s" % (i, p, b)
                mut = w[:p - 1] + b + w[p:]
                assert sum(x != y for x, y in zip(mut, w)) == 1
                reg.append({"qid": qid, "fuente": i, "sid": sid, "ini": ini,
                            "pos": p, "base": b, "orig": w, "mut": mut})
                lineas.append(">%s\n%s\n" % (qid, mut))
    fa = tmp / ("consultas_%s.fa" % etiqueta)
    fa.write_text("".join(lineas))
    return fa, reg


def correr_configs(db: Path, fa: Path, etiqueta, configs, tmp: Path, hilos=6):
    fmt = "6 qseqid sseqid pident length mismatch gapopen sstart send evalue bitscore"
    res = {}
    for nombre, args in configs:
        out = tmp / ("blast_%s_%s.tsv" % (etiqueta, nombre))
        t0 = time.time()
        cmd = (["blastn"] + args + ["-query", str(fa), "-db", str(db),
                                    "-num_threads", str(hilos), "-outfmt", fmt,
                                    "-out", str(out)])
        r = corr(cmd)
        dt = time.time() - t0
        if r.returncode != 0:
            print("   FALLO %s: %s" % (nombre, r.stderr.strip()[:200]), flush=True)
            res[nombre] = None
            continue
        estricto, practico, cualquiera = {}, {}, {}
        n = 0
        for ln in out.read_text().splitlines():
            n += 1
            c = ln.split("\t")
            q, L, mm, go = c[0], int(c[3]), int(c[4]), int(c[5])
            cualquiera[q] = True
            if L == 21 and mm == 1 and go == 0:
                estricto[q] = True
            if L >= 20 and mm <= 1 and go == 0:
                practico[q] = True
        res[nombre] = {"estricto": estricto, "practico": practico,
                       "cualquiera": cualquiera, "filas": n, "segundos": dt,
                       "salida": str(out)}
        print("   %-28s %6.1f s  filas=%-8d estricto=%d" %
              (nombre, dt, n, len(estricto)), flush=True)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True)
    ap.add_argument("--fuentes", type=int, default=50)
    ap.add_argument("--saltar-genoma", action="store_true")
    a = ap.parse_args()
    sal = Path(a.salida); sal.mkdir(parents=True, exist_ok=True)
    tmp = TRABAJO; tmp.mkdir(parents=True, exist_ok=True)

    print("== Parte A: valores por defecto medidos en el binario", flush=True)
    defaults = parte_a(sal)
    for t, v in defaults.items():
        print("   %-14s ws=%s reward=%s penalty=%s gapopen=%s gapext=%s hsps=%s" %
              (t, v["word_size_medido"], v["reward_medido"], v["penalty_medido"],
               v["gapopen_medido"], v["gapextend_medido"],
               v["hsp_de_40nt_reportados_en_un_sujeto"]), flush=True)

    print("== Parte B: sensibilidad por posicion del desajuste", flush=True)
    bases = []
    dbs = tmp / "sintetica"
    seq = db_sintetica(dbs)
    bases.append(("sintetica_5Mb", dbs, seq, True))
    bases.append(("Zmays_transcriptoma", DBDIR / "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna", None, True))
    if not a.saltar_genoma:
        bases.append(("Dmaidis_genoma", DBDIR / "GCA_975739785.1_ihDalMaid1.1_genomic", None, False))

    filas, resumen = [], []
    for etiqueta, db, seqmem, todas in bases:
        print(" -- base %s" % etiqueta, flush=True)
        fuentes = muestrear_21meros(db, a.fuentes, semilla=31, seq_mem=seqmem)
        fuentes, _ = unicos(db, fuentes, etiqueta, tmp)
        print("    %d 21-meros fuente con aparicion unica" % len(fuentes), flush=True)
        fa, reg = consultas_mutadas(fuentes, tmp, etiqueta, todas_las_bases=todas)
        # control exacto: el locus de origen tiene Hamming 1 con cada consulta
        ctrl_ok = 0
        for r in reg:
            if sum(x != y for x, y in zip(r["mut"], r["orig"])) == 1:
                ctrl_ok += 1
        cfgs = [c for c in CONFIGS if c[0] not in SOLO_CHICAS or etiqueta == "sintetica_5Mb"]
        if etiqueta == "Dmaidis_genoma":
            cfgs = [c for c in cfgs if c[0] in CONFIGS_GENOMA]
        res = correr_configs(db, fa, etiqueta, cfgs, tmp)
        for nombre, r in res.items():
            if r is None:
                continue
            for p in range(1, 22):
                sub = [x for x in reg if x["pos"] == p]
                filas.append({
                    "base": etiqueta, "config": nombre, "pos_desajuste": p,
                    "n": len(sub),
                    "sens_estricta": sum(1 for x in sub if x["qid"] in r["estricto"]) / len(sub),
                    "sens_practica": sum(1 for x in sub if x["qid"] in r["practico"]) / len(sub),
                    "frac_algun_hsp": sum(1 for x in sub if x["qid"] in r["cualquiera"]) / len(sub),
                })
            resumen.append({"base": etiqueta, "config": nombre, "consultas": len(reg),
                            "fuentes": len(fuentes), "control_hamming1_ok": ctrl_ok,
                            "sens_estricta_global": len(r["estricto"]) / len(reg),
                            "sens_practica_global": len(r["practico"]) / len(reg),
                            "filas_salida": r["filas"], "segundos": r["segundos"],
                            "salida_cruda": r["salida"]})
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
