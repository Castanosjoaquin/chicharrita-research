#!/usr/bin/env python3
"""Eje 3 de F3 (off-target contra el panel de seis) y los nulos de los ejes 3 y 4.

Criterio: PREREGISTRO_EJE3.md y su enmienda 1. Lee los tamizados que ya existen en work/ (no
los regenera, R12) y corre el nulo con el MISMO motor, panel y parametros.

Uso (entorno con pyahocorasick y biopython):
    python research/ola6/F3_recomendador_genes/scripts/07_eje_offtarget.py [--sin-nulo]
Versionado: solo conteos y fracciones, en resultados/. Permutaciones y salidas por siRNA quedan
en work/F3_eje3/ (el tamizado por siRNA trae la columna `sirna`, 21 nt: no se copia).
"""
import argparse, csv, hashlib, json, random, statistics, subprocess, sys
from pathlib import Path
import ahocorasick

RAIZ = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1] / "resultados"
W = RAIZ / "work/F3_eje3"
SEMILLA, N_PERM, K = 20261028, 50, 21
COMP = str.maketrans("ACGT", "TGCA")
rc = lambda s: s.translate(COMP)[::-1]

# orden normativo del panel (D76) -> nombre corto
PANEL = [("GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna", "maiz"),
         ("GCF_914767665.1_icHarAxyr1.1_rna", "H_axyridis"),
         ("GCF_003254395.2_Amel_HAv3.1_rna", "A_mellifera"),
         ("GCF_021130785.1_UT_GWSS_2.1_rna", "H_vitripennis"),
         ("GCF_002217175.1_ASM221717v1_rna", "F_candida"),
         ("humano_rna", "humano")]
CAND = {  # id: (gen, consulta, tsv de tamizado, fasta de la secuencia)
    "DM-01": ("BicC", "BicC_Dm_full", "work/sifi_v2/offtarget_k21", "work/sifi_v2/fasta/BicC_Dm_full.fasta"),
    "DM-02": ("V-ATPase B", "VATPaseB_Dm_full", "work/O3/offtarget/cds_completo",
              "research/ola6/O2_vatpase_b/resultados/VATPaseB_Dm_cds.fna"),
    "DM-03": ("V-ATPase D", "ATPaseD_Dm_full", "work/sifi_v2/offtarget_k21", "work/sifi_v2/fasta/ATPaseD_Dm_full.fasta"),
    "DM-05": ("eth", "eth_Dm_full", "work/sifi_v2/offtarget_k21", "work/sifi_v2/fasta/eth_Dm_full.fasta"),
    "DM-06": ("burs-alpha", "bursA_Dm_full", "work/sifi_v2/offtarget_k21", "work/sifi_v2/fasta/bursA_Dm_full.fasta"),
}
TSAS = ["GCWP01", "GHCC01", "GITV01"]


def leer_fasta(p):
    return "".join(l.strip() for l in Path(p).read_text().splitlines() if not l.startswith(">")).upper()


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def leer_tamizado(dir_):
    """-> {consulta: [fila,...]} con fila = {referencia_corta: {crit: int}}; valida panel y parametros."""
    res = json.loads((RAIZ / dir_ / "offtarget_resumen.json").read_text())
    for r in res:
        assert r["size"] == K and r["min_block"] == 19, (dir_, r["size"], r["min_block"])
    ruta = RAIZ / dir_ / "offtarget_por_sirna.tsv"
    with open(ruta, encoding="utf-8") as fh:
        rd = csv.reader(fh, delimiter="\t")
        cab = next(rd)
        cols = {}
        for i, c in enumerate(cab[3:], 3):
            ref, crit = c.split("|")
            cols[(ref, crit)] = i
        refs = {ref for ref, _ in cols}
        assert refs == {a for a, _ in PANEL}, (dir_, sorted(refs))
        por = {}
        for fila in rd:
            d = {corto: {crit: int(fila[cols[(ref, crit)]]) for crit in ("perfecto_21", "perfecto_ge19", "mm1_21")}
                 for ref, corto in PANEL}
            por.setdefault(fila[0], []).append(d)
    return por, sha(ruta)


def resumir(filas):
    n = len(filas)
    limpia = sum(all(d[c]["perfecto_ge19"] == 0 for c in d) for d in filas)
    sin_h = sum(all(d[c]["perfecto_ge19"] == 0 for c in d if c != "humano") for d in filas)
    out = {"ventanas": n, "limpias": limpia, "fraccion_limpia": limpia / n,
           "fraccion_limpia_sin_humano": sin_h / n,
           "fraccion_con_perfecto_21": sum(any(d[c]["perfecto_21"] for c in d) for d in filas) / n,
           "fraccion_con_mm1_21": sum(any(d[c]["mm1_21"] for c in d) for d in filas) / n}
    for _, corto in PANEL:
        out["ge19_" + corto] = sum(d[corto]["perfecto_ge19"] > 0 for d in filas) / n
    return out


def permutar(seq, rng):
    l = list(seq); rng.shuffle(l); return "".join(l)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--sin-nulo", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(exist_ok=True); W.mkdir(parents=True, exist_ok=True)
    tam, shas = {}, {}
    for d in {c[2] for c in CAND.values()}:
        tam[d], shas[d] = leer_tamizado(d)
    filas = []
    for ident, (gen, consulta, d, fa) in CAND.items():
        seq = leer_fasta(RAIZ / fa)
        v = tam[d][consulta]
        assert len(v) == len(seq) - K + 1, (ident, len(v), len(seq) - K + 1)   # todas las ventanas tienen dato
        r = {"id": ident, "gen": gen, "consulta": consulta, "tamizado": d}
        r.update(resumir(v)); filas.append(r)
    campos = list(filas[0])
    with open(OUT / "eje3_offtarget.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in filas:
            w.writerow({k: (f"{x:.4f}" if isinstance(x, float) else x) for k, x in r.items()})
    meta = {"panel_orden_D76": [c for _, c in PANEL], "size": K, "min_block": 19,
            "sha256_tamizados": {d: s for d, s in shas.items()}, "semilla_nulo": SEMILLA, "permutaciones": N_PERM}
    for r in filas:
        print(r["id"], r["gen"], "ventanas", r["ventanas"], "limpias", r["limpias"], "frac", round(r["fraccion_limpia"], 4))
    if a.sin_nulo:
        (OUT / "eje3_meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n"); return 0

    # ---- nulo: permutaciones que conservan la composicion, semilla fija, mismo motor y panel ----
    rng = random.Random(SEMILLA)
    perms = {i: [permutar(leer_fasta(RAIZ / c[3]), rng) for _ in range(N_PERM)] for i, c in CAND.items()}
    refs = sorted((RAIZ / "work/offtarget_db").glob("*_rna.fna.gz")) + [RAIZ / "work/W5/ref/humano_rna.fna.gz"]
    assert {p.name[:-7] for p in refs} == {a for a, _ in PANEL}, [p.name for p in refs]
    # El tamizador no escala con un archivo de ~125.000 ventanas (una corrida asi no termino en
    # 55 min); se ejecuta en lotes de ~6.000 ventanas, que es el tamano de la corrida real, y
    # varios lotes a la vez. Es forma de ejecutar: mismas permutaciones, motor, panel y parametros.
    from concurrent.futures import ThreadPoolExecutor
    lotes, actual, n_act = [], [], 0
    for i_, (gen, consulta, d, fa) in CAND.items():
        for j_, s_ in enumerate(perms[i_]):
            nv = len(s_) - K + 1
            if actual and n_act + nv > 6000:
                lotes.append(actual); actual, n_act = [], 0
            actual.append((i_, j_, s_)); n_act += nv
    if actual: lotes.append(actual)

    def correr(k):
        sal = W / f"lote_{k:03d}"
        if not (sal / "offtarget_por_sirna.tsv").exists():          # reanudable
            fq = W / f"lote_{k:03d}.fasta"
            fq.write_text("".join(f">{i_}_p{j_:02d}\n{s_}\n" for i_, j_, s_ in lotes[k]))
            subprocess.run([sys.executable, str(RAIZ / "tools/sifi21_port/offtarget_21nt.py"), "--size", "21", "--mm1",
                            "--consulta", str(fq), "--db", *map(str, refs), "--salida", str(sal)],
                           check=True, capture_output=True)
        filas_p, cols = {}, {}
        with open(sal / "offtarget_por_sirna.tsv", encoding="utf-8") as fh:
            rd = csv.reader(fh, delimiter="\t"); cab = next(rd)
            for kk, c in enumerate(cab[3:], 3):
                ref, crit = c.split("|"); cols[(ref, crit)] = kk
            for f in rd:
                filas_p.setdefault(f[0], []).append(
                    {corto: {crit: int(f[cols[(ref, crit)]]) for crit in ("perfecto_21", "perfecto_ge19", "mm1_21")}
                     for ref, corto in PANEL})
        print("lote", k + 1, "de", len(lotes), flush=True)
        return {q: resumir(v)["fraccion_limpia"] for q, v in filas_p.items()}
    with ThreadPoolExecutor(max_workers=6) as ex:
        por_perm = {}
        for r_ in ex.map(correr, range(len(lotes))):
            por_perm.update(r_)
    nulo3 = []
    for i_, (gen, consulta, d, fa) in CAND.items():
        fr = [por_perm[f"{i_}_p{j_:02d}"] for j_ in range(N_PERM)]
        nulo3.append({"id": i_, "gen": gen, "n_permutaciones": N_PERM,
                      "fraccion_limpia_mediana": statistics.median(fr), "minimo": min(fr), "maximo": max(fr)})
        print("nulo eje 3", i_, round(statistics.median(fr), 4), round(min(fr), 4), round(max(fr), 4), flush=True)
    with open(OUT / "eje3_nulo.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(nulo3[0]), delimiter="\t", lineterminator="\n"); w.writeheader()
        for r in nulo3:
            w.writerow({k: (f"{x:.4f}" if isinstance(x, float) else x) for k, x in r.items()})

    # ---- nulo del eje 4 (enmienda 1): presencia exacta de ventanas permutadas, por TSA ----
    A = ahocorasick.Automaton()
    todas = {}
    for i, ps in perms.items():
        for j, s in enumerate(ps):
            for k in range(len(s) - K + 1):
                w_ = s[k:k + K]; todas.setdefault(w_, set()).add((i, j))
    for w_ in todas:
        A.add_word(w_, w_); A.add_word(rc(w_), w_)
    A.make_automaton()
    nulo4 = []
    for t in TSAS:
        hit = set()
        with open(RAIZ / f"work/W5/ref/TSA_{t}.fasta") as fh:
            buf = []
            def vac():
                s = "".join(buf).upper()
                for _, w_ in A.iter(s): hit.add(w_)
            for l in fh:
                if l.startswith(">"):
                    if buf: vac()
                    buf = []
                else: buf.append(l.strip())
            if buf: vac()
        for i, ps in perms.items():
            fr = [sum(1 for k in range(len(s) - K + 1) if s[k:k + K] in hit) / (len(s) - K + 1) for s in ps]
            nulo4.append({"id": i, "tsa": t, "n_permutaciones": N_PERM,
                          "fraccion_presente_mediana": statistics.median(fr), "minimo": min(fr), "maximo": max(fr)})
    with open(OUT / "eje4_nulo.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(nulo4[0]), delimiter="\t", lineterminator="\n"); w.writeheader()
        for r in nulo4:
            w.writerow({k: (f"{x:.6f}" if isinstance(x, float) else x) for k, x in r.items()})
    print("nulo eje 4: maximo de presencia en cualquier permutacion y TSA =", max(r["maximo"] for r in nulo4))
    (OUT / "eje3_meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
