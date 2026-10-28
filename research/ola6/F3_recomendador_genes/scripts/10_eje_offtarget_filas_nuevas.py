#!/usr/bin/env python3
"""Eje 3 de F3 para las cuatro filas recuperadas de papers (DE-01, DE-03, CI-13, DE-06) y su nulo.

Criterio: PREREGISTRO_EJE3_FILAS_NUEVAS.md (commit 43c7fa0, anterior a este calculo). Es un PROXY: mide
el off-target de la secuencia de la especie del paper, no del transcripto de D. maidis.

Uso (entorno con pyahocorasick): python research/ola6/F3_recomendador_genes/scripts/10_eje_offtarget_filas_nuevas.py
Versionado: solo conteos y fracciones. Secuencias, ventanas y salidas por siRNA quedan en work/F3_eje3_nuevas/.
"""
import csv, hashlib, json, random, statistics, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1] / "resultados"
W = RAIZ / "work/F3_eje3_nuevas"
REC = RAIZ / "work/F3_recuperacion"
SEMILLA, N_PERM, K, LOTE = 20261029, 50, 21, 6000
COMP = str.maketrans("ACGT", "TGCA")
rc = lambda s: s.translate(COMP)[::-1]
canon = lambda s: min(s, rc(s))
PANEL = [("GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna", "maiz"), ("GCF_914767665.1_icHarAxyr1.1_rna", "H_axyridis"),
         ("GCF_003254395.2_Amel_HAv3.1_rna", "A_mellifera"), ("GCF_021130785.1_UT_GWSS_2.1_rna", "H_vitripennis"),
         ("GCF_002217175.1_ASM221717v1_rna", "F_candida"), ("humano_rna", "humano")]
CRIT = ("perfecto_21", "perfecto_ge19", "mm1_21")
# (fila, nombre de la secuencia, fasta). Todas verificadas en recuperacion_6filas_REPORT.md
SEQS = [("DE-01", "KC473163", REC / "DE-01_KC473163.fasta"), ("DE-01", "KC473162", REC / "DE-01_KC473162.fasta"),
        ("CI-13", "MN815919", REC / "CI-13_MN815919.fasta"), ("DE-06", "PZ371509", REC / "DE-06_PZ371509.fasta"),
        ("DE-06", "PZ371510", REC / "DE-06_PZ371510.fasta")]
INFO = {"DE-01": ("Peregrinus maidis", "en el orden (cohorte A)"), "DE-03": ("Peregrinus maidis", "en el orden (cohorte B)"),
        "CI-13": ("Nephotettix cincticeps", "fuera del orden: fenotipo_invertido"),
        "DE-06": ("Delphacodes kuscheli", "fuera del orden: sin_fenotipo_publicado")}


def fasta(p):
    nom, buf, out = None, [], []
    for l in Path(p).read_text().splitlines():
        if l.startswith(">"):
            if nom is not None: out.append((nom, "".join(buf).upper()))
            nom, buf = l[1:].split()[0], []
        else: buf.append(l.strip())
    if nom is not None: out.append((nom, "".join(buf).upper()))
    return out


def leer_tamizado(ruta):
    """-> {consulta: [(sirna, {ref_corto: {crit: int}}), ...]} en orden de posicion."""
    por, cols = {}, {}
    with open(ruta, encoding="utf-8") as fh:
        rd = csv.reader(fh, delimiter="\t"); cab = next(rd)
        for i, c in enumerate(cab[3:], 3):
            ref, crit = c.split("|"); cols[(ref, crit)] = i
        assert {r for r, _ in cols} == {a for a, _ in PANEL}, sorted({r for r, _ in cols})
        for f in rd:
            por.setdefault(f[0], []).append((f[2], {c: {k: int(f[cols[(r, k)]]) for k in CRIT} for r, c in PANEL}))
    return por


def resumir(vent):
    """vent: lista de (canon, dict). Deduplica por canon y resume."""
    vistos, v = set(), []
    for k, d in vent:
        if k not in vistos: vistos.add(k); v.append(d)
    n = len(v)
    out = {"ventanas_distintas": n, "limpias": sum(all(d[c]["perfecto_ge19"] == 0 for c in d) for d in v)}
    out["fraccion_limpia"] = out["limpias"] / n
    out["fraccion_limpia_sin_humano"] = sum(all(d[c]["perfecto_ge19"] == 0 for c in d if c != "humano") for d in v) / n
    out["fraccion_con_perfecto_21"] = sum(any(d[c]["perfecto_21"] for c in d) for d in v) / n
    out["fraccion_con_mm1_21"] = sum(any(d[c]["mm1_21"] for c in d) for d in v) / n
    for _, c in PANEL: out["ge19_" + c] = sum(d[c]["perfecto_ge19"] > 0 for d in v) / n
    return out


def correr_motor(fq, salida, refs):
    if not (salida / "offtarget_por_sirna.tsv").exists():
        subprocess.run([sys.executable, str(RAIZ / "tools/sifi21_port/offtarget_21nt.py"), "--size", "21", "--mm1",
                        "--consulta", str(fq), "--db", *map(str, refs), "--salida", str(salida)], check=True, capture_output=True)
    return leer_tamizado(salida / "offtarget_por_sirna.tsv")


def main():
    W.mkdir(parents=True, exist_ok=True); OUT.mkdir(exist_ok=True)
    refs = sorted((RAIZ / "work/offtarget_db").glob("*_rna.fna.gz")) + [RAIZ / "work/W5/ref/humano_rna.fna.gz"]
    assert {p.name[:-7] for p in refs} == {a for a, _ in PANEL}
    seqs = {}   # (fila, nombre) -> secuencia
    for fila, nom, f in SEQS: seqs[(fila, nom)] = fasta(f)[0][1]
    for nom, s in fasta(REC / "DE-03_S1File.fasta"): seqs[("DE-03", nom)] = s
    ctrl = fasta(RAIZ / "work/sifi_v2/fasta/eth_Dm_full.fasta")[0][1]

    # ---- real, con el ancla de control en el mismo lote ----
    fq = W / "real.fasta"
    fq.write_text("".join(f">{f}__{n}\n{s}\n" for (f, n), s in seqs.items()) + f">CTRL__eth_Dm\n{ctrl}\n")
    tam = correr_motor(fq, W / "real", refs)
    pub = leer_tamizado(RAIZ / "work/sifi_v2/offtarget_k21/offtarget_por_sirna.tsv")["eth_Dm_full"]
    mio = tam["CTRL__eth_Dm"]
    assert len(mio) == len(pub) and all(a[1] == b[1] for a, b in zip(mio, pub)), "ANCLA ROTA: eth_Dm no reproduce sifi_v2"
    print("ancla de control: eth_Dm reproduce sifi_v2 en", len(pub), "ventanas, columna por columna")

    filas_ids = ["DE-01", "DE-03", "CI-13", "DE-06"]
    por_seq, por_fila = [], []
    for fila in filas_ids:
        pool = []
        for (f, n), s in seqs.items():
            if f != fila: continue
            vent = [(canon(w), d) for w, d in tam[f"{f}__{n}"]]
            r = resumir(vent); pool += vent
            por_seq.append({"fila": fila, "secuencia": n, "largo_nt": len(s), "sha256": hashlib.sha256(s.encode()).hexdigest(), **r})
        r = resumir(pool)
        por_fila.append({"id": fila, "especie": INFO[fila][0], "estado_en_el_orden": INFO[fila][1],
                         "lectura": "proxy_especie_del_paper", "n_secuencias": sum(1 for k in seqs if k[0] == fila), **r})
    def w(nombre, filas):
        with open(OUT / nombre, "w", newline="", encoding="utf-8") as fh:
            d = csv.DictWriter(fh, fieldnames=list(filas[0]), delimiter="\t", lineterminator="\n"); d.writeheader()
            for r in filas: d.writerow({k: (f"{x:.4f}" if isinstance(x, float) else x) for k, x in r.items()})
    w("eje3_filas_nuevas.tsv", por_fila); w("eje3_filas_nuevas_por_secuencia.tsv", por_seq)
    for r in por_fila: print(r["id"], r["especie"], "ventanas", r["ventanas_distintas"], "limpias", r["limpias"], "frac", round(r["fraccion_limpia"], 4))
    meta = {"semilla_nulo": SEMILLA, "permutaciones": N_PERM, "ancla": "eth_Dm reproduce work/sifi_v2 columna por columna",
            "preregistro": "PREREGISTRO_EJE3_FILAS_NUEVAS.md (43c7fa0)"}
    (OUT / "eje3_filas_nuevas_meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")

    # ---- nulo: 50 permutaciones por secuencia, en lotes de ~6.000 ventanas, reanudable ----
    rng = random.Random(SEMILLA)
    perms = {k: ["".join(rng.sample(s, len(s))) for _ in range(N_PERM)] for k, s in seqs.items()}
    items, lotes, act, n_act = [(k, j, p) for k, ps in perms.items() for j, p in enumerate(ps)], [], [], 0
    for k, j, p in items:
        nv = len(p) - K + 1
        if act and n_act + nv > LOTE: lotes.append(act); act, n_act = [], 0
        act.append((k, j, p)); n_act += nv
    if act: lotes.append(act)

    def lote(i):
        fqi = W / f"nulo_{i:03d}.fasta"
        fqi.write_text("".join(f">{k[0]}__{k[1]}__p{j:02d}\n{p}\n" for k, j, p in lotes[i]))
        t = correr_motor(fqi, W / f"nulo_{i:03d}", refs)
        print("lote", i + 1, "de", len(lotes), flush=True)
        return t
    todo = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        for t in ex.map(lote, range(len(lotes))): todo.update(t)
    nulo = []
    for fila in filas_ids:
        fr = []
        for j in range(N_PERM):
            pool = []
            for (f, n) in seqs:
                if f == fila: pool += [(canon(x), d) for x, d in todo[f"{f}__{n}__p{j:02d}"]]
            fr.append(resumir(pool)["fraccion_limpia"])
        real = next(r for r in por_fila if r["id"] == fila)["fraccion_limpia"]
        nulo.append({"id": fila, "n_permutaciones": N_PERM, "fraccion_limpia_mediana": statistics.median(fr), "minimo": min(fr),
                     "maximo": max(fr), "real_frente_al_nulo": "dentro del rango del nulo" if min(fr) <= real <= max(fr) else "fuera del rango del nulo"})
        print("nulo", fila, round(statistics.median(fr), 4), round(min(fr), 4), round(max(fr), 4), nulo[-1]["real_frente_al_nulo"], flush=True)
    w("eje3_filas_nuevas_nulo.tsv", nulo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
