#!/usr/bin/env python3
"""Eje 3 de F3 para las seis filas de C5 con conteos contra el panel de cinco, y su nulo (issue #43).

Criterio: PREREGISTRO_EJE3_FILAS_NUEVAS.md enmienda 1 (commit e166438, anterior a este calculo).
Lectura: `proxy_sustituto_declarado` — la secuencia es la sustituta que C5 declaro en `secuencia_usada`,
de una tercera especie; en cuatro de las seis es M. quadrilineatus, que el panel de cinco de C5 INCLUIA
(autoacierto del 100 %) y el panel de seis de D76 no.

Uso: python research/ola6/F3_recomendador_genes/scripts/11_eje_offtarget_filas_c5.py
Versionado: solo conteos y fracciones. Permutaciones y salidas por siRNA quedan en work/F3_eje3_c5/.
"""
import csv, hashlib, json, random, statistics, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1] / "resultados"
W = RAIZ / "work/F3_eje3_c5"
CAT = RAIZ / "research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.json"
FA = RAIZ / "research/ola3/C5_estructura_genes_ingenieria_inversa/resultados/candidatos_c5.fa"
SEMILLA, N_PERM, K, LOTE = 20261030, 50, 21, 6000
COMP = str.maketrans("ACGT", "TGCA")
rc = lambda s: s.translate(COMP)[::-1]
canon = lambda s: min(s, rc(s))
PANEL = [("GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna", "maiz"), ("GCF_914767665.1_icHarAxyr1.1_rna", "H_axyridis"),
         ("GCF_003254395.2_Amel_HAv3.1_rna", "A_mellifera"), ("GCF_021130785.1_UT_GWSS_2.1_rna", "H_vitripennis"),
         ("GCF_002217175.1_ASM221717v1_rna", "F_candida"), ("humano_rna", "humano")]
CRIT = ("perfecto_21", "perfecto_ge19", "mm1_21")
FILAS = ["CI-01", "CI-02", "CI-03", "CI-10", "DE-02", "DE-05"]


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


def motor(fq, salida, refs):
    if not (salida / "offtarget_por_sirna.tsv").exists():
        subprocess.run([sys.executable, str(RAIZ / "tools/sifi21_port/offtarget_21nt.py"), "--size", "21", "--mm1",
                        "--consulta", str(fq), "--db", *map(str, refs), "--salida", str(salida)], check=True, capture_output=True)
    return leer_tamizado(salida / "offtarget_por_sirna.tsv")


def main():
    W.mkdir(parents=True, exist_ok=True)
    refs = sorted((RAIZ / "work/offtarget_db").glob("*_rna.fna.gz")) + [RAIZ / "work/W5/ref/humano_rna.fna.gz"]
    assert {p.name[:-7] for p in refs} == {a for a, _ in PANEL}
    cat = {r["id"]: r for r in json.loads(CAT.read_text())["filas"]}
    secs = dict(fasta(FA))
    usa = {i: cat[i]["ventanas_21nt"]["secuencia_usada"] for i in FILAS}
    seqs = {i: secs[usa[i]] for i in FILAS}
    for i in FILAS:   # el catalogo declara cuantas ventanas tiene cada fila: tiene que coincidir
        assert len(seqs[i]) - K + 1 == cat[i]["ventanas_21nt"]["ventanas_totales"], i
    ctrl = fasta(RAIZ / "work/sifi_v2/fasta/eth_Dm_full.fasta")[0][1]

    fq = W / "real.fasta"
    fq.write_text("".join(f">{i}\n{s}\n" for i, s in seqs.items()) + f">CTRL__eth_Dm\n{ctrl}\n")
    tam = motor(fq, W / "real", refs)
    pub = leer_tamizado(RAIZ / "work/sifi_v2/offtarget_k21/offtarget_por_sirna.tsv")["eth_Dm_full"]
    mio = tam["CTRL__eth_Dm"]
    assert len(mio) == len(pub) and all(a[1] == b[1] for a, b in zip(mio, pub)), "ANCLA ROTA"
    print("ancla: eth_Dm reproduce sifi_v2 en", len(pub), "ventanas")

    filas = []
    for i in FILAS:
        v = [(canon(w), d) for w, d in tam[i]]
        c5 = cat[i]["ventanas_21nt"]
        filas.append({"id": i, "especie_catalogo": cat[i]["especie"], "gen": cat[i]["gen"],
                      "secuencia_usada": usa[i], "lectura": "proxy_sustituto_declarado",
                      "largo_nt": len(seqs[i]), "sha256": hashlib.sha256(seqs[i].encode()).hexdigest(),
                      **resumir(v),
                      "panelC5_21meros_perfectos_en_M_quadrilineatus": c5.get("21meros_perfectos_en_M_quadrilineatus", ""),
                      "M_quadrilineatus_esta_en_el_panel_de_seis": "no"})
    def w(nombre, fs):
        with open(OUT / nombre, "w", newline="", encoding="utf-8") as fh:
            d = csv.DictWriter(fh, fieldnames=list(fs[0]), delimiter="\t", lineterminator="\n"); d.writeheader()
            for r in fs: d.writerow({k: (f"{x:.4f}" if isinstance(x, float) else x) for k, x in r.items()})
    w("eje3_filas_c5.tsv", filas)
    for r in filas:
        print(r["id"], r["gen"][:18], "ventanas", r["ventanas_distintas"], "limpias", r["limpias"],
              "frac", round(r["fraccion_limpia"], 4), "| C5 decia en Mq:", r["panelC5_21meros_perfectos_en_M_quadrilineatus"])
    (OUT / "eje3_filas_c5_meta.json").write_text(json.dumps(
        {"semilla_nulo": SEMILLA, "permutaciones": N_PERM, "panel_orden_D76": [c for _, c in PANEL],
         "preregistro": "PREREGISTRO_EJE3_FILAS_NUEVAS.md enmienda 1 (e166438)",
         "ancla": "eth_Dm reproduce work/sifi_v2 columna por columna",
         "fuente_secuencias": "research/ola3/C5_.../resultados/candidatos_c5.fa (secuencia_usada del catalogo)"},
        indent=1, ensure_ascii=False) + "\n")

    # ---- nulo ----
    rng = random.Random(SEMILLA)
    perms = {i: ["".join(rng.sample(s, len(s))) for _ in range(N_PERM)] for i, s in seqs.items()}
    items, lotes, act, n_act = [(i, j, p) for i, ps in perms.items() for j, p in enumerate(ps)], [], [], 0
    for i, j, p in items:
        nv = len(p) - K + 1
        if act and n_act + nv > LOTE: lotes.append(act); act, n_act = [], 0
        act.append((i, j, p)); n_act += nv
    if act: lotes.append(act)

    def lote(k):
        fqk = W / f"nulo_{k:03d}.fasta"
        fqk.write_text("".join(f">{i}__p{j:02d}\n{p}\n" for i, j, p in lotes[k]))
        t = motor(fqk, W / f"nulo_{k:03d}", refs)
        print("lote", k + 1, "de", len(lotes), flush=True)
        return t
    todo = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        for t in ex.map(lote, range(len(lotes))): todo.update(t)
    nulo = []
    for i in FILAS:
        fr = [resumir([(canon(x), d) for x, d in todo[f"{i}__p{j:02d}"]])["fraccion_limpia"] for j in range(N_PERM)]
        real = next(r for r in filas if r["id"] == i)["fraccion_limpia"]
        nulo.append({"id": i, "n_permutaciones": N_PERM, "fraccion_limpia_mediana": statistics.median(fr),
                     "minimo": min(fr), "maximo": max(fr),
                     "real_frente_al_nulo": "dentro del rango del nulo" if min(fr) <= real <= max(fr) else "fuera del rango del nulo"})
        print("nulo", i, round(statistics.median(fr), 4), round(min(fr), 4), round(max(fr), 4), nulo[-1]["real_frente_al_nulo"], flush=True)
    w("eje3_filas_c5_nulo.tsv", nulo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
