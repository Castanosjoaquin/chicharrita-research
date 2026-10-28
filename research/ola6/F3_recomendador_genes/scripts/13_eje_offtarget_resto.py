#!/usr/bin/env python3
"""Eje 3 de F3 para las cuatro filas con accesion recuperada en la segunda vuelta (issue #43).

Criterio: PREREGISTRO_EJE3_FILAS_NUEVAS.md §0-§3 sin cambios — es el mismo caso que cubre ese
documento (fila recuperada del paper, secuencia de la especie del paper), asi que la lectura vuelve a
ser `proxy_especie_del_paper`. Lo unico propio de esta vuelta esta en §0 de abajo.

Las accesiones salen de `recuperacion_resto.tsv` (leidas del texto de cada paper) y se bajan de NCBI.

Uso: python research/ola6/F3_recomendador_genes/scripts/13_eje_offtarget_resto.py
Versionado: solo conteos. Secuencias y salidas por siRNA quedan en work/F3_eje3_resto/.
"""
import csv, hashlib, json, random, statistics, subprocess, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parents[1] / "resultados"
W = RAIZ / "work/F3_eje3_resto"
EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
SEMILLA, N_PERM, K, LOTE = 20261031, 50, 21, 6000
COMP = str.maketrans("ACGT", "TGCA")
rc = lambda s: s.translate(COMP)[::-1]
canon = lambda s: min(s, rc(s))
PANEL = [("GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna", "maiz"), ("GCF_914767665.1_icHarAxyr1.1_rna", "H_axyridis"),
         ("GCF_003254395.2_Amel_HAv3.1_rna", "A_mellifera"), ("GCF_021130785.1_UT_GWSS_2.1_rna", "H_vitripennis"),
         ("GCF_002217175.1_ASM221717v1_rna", "F_candida"), ("humano_rna", "humano")]
CRIT = ("perfecto_21", "perfecto_ge19", "mm1_21")

# (fila, accesion de nucleotido, gen, de donde salio la accesion). Ninguna se busco por nombre.
SEQS = [
    # OJO HE-06: la secuencia es de Homalodisca vitripennis, que ESTA en el panel de seis. Su
    # fraccion limpia es un autoacierto (la secuencia contra si misma), igual que el caso de
    # M. quadrilineatus de D99, y NO se lee como riesgo. Se calcula igual y se rotula.
    ("HE-06", "AY588061.1", "actina muscular", "citada en el texto del paper (metodos del ARNdc)"),
    ("HE-07", "LC009512.1", "NcSP75",
     "el paper cita la proteina BAQ94503; su propio registro de NCBI declara coded_by LC009512.1"),
    ("HE-10", "MF101769.1", "V-ATPasa (1 de los 4 blancos)", "Tabla 1 del paper, accesion por gen"),
    ("CI-06", "GFTU01013594.1", "ATP synthase beta", "metodos 2.2 del paper (TSA, BioProject PRJNA393620)"),
]


def fasta_txt(acc):
    u = EU + f"efetch.fcgi?db=nuccore&rettype=fasta&retmode=text&id={acc}"
    return urllib.request.urlopen(u, timeout=60).read().decode()


def leer_tamizado(ruta):
    por, cols = {}, {}
    with open(ruta, encoding="utf-8") as fh:
        rd = csv.reader(fh, delimiter="\t"); cab = next(rd)
        for i, c in enumerate(cab[3:], 3):
            ref, crit = c.split("|"); cols[(ref, crit)] = i
        assert {r for r, _ in cols} == {a for a, _ in PANEL}
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
    seqs, meta_seq = {}, {}
    for fila, acc, gen, origen in SEQS:
        txt = fasta_txt(acc)
        s = "".join(l.strip() for l in txt.splitlines() if not l.startswith(">")).upper()
        (W / f"{fila}_{acc.split('.')[0]}.fasta").write_text(txt)
        seqs[fila] = s
        meta_seq[fila] = {"accesion": acc, "gen": gen, "origen_de_la_accesion": origen, "largo_nt": len(s),
                          "sha256": hashlib.sha256(s.encode()).hexdigest(), "cabecera": txt.splitlines()[0][1:][:110]}
        print(fila, acc, len(s), "nt |", meta_seq[fila]["cabecera"][:70])
    ctrl = "".join(l.strip() for l in (RAIZ / "work/sifi_v2/fasta/eth_Dm_full.fasta").read_text().splitlines()
                   if not l.startswith(">")).upper()

    fq = W / "real.fasta"
    fq.write_text("".join(f">{i}\n{s}\n" for i, s in seqs.items()) + f">CTRL__eth_Dm\n{ctrl}\n")
    tam = motor(fq, W / "real", refs)
    pub = leer_tamizado(RAIZ / "work/sifi_v2/offtarget_k21/offtarget_por_sirna.tsv")["eth_Dm_full"]
    assert len(tam["CTRL__eth_Dm"]) == len(pub) and all(a[1] == b[1] for a, b in zip(tam["CTRL__eth_Dm"], pub)), "ANCLA ROTA"
    print("ancla: eth_Dm reproduce sifi_v2 en", len(pub), "ventanas")

    cat = {r["id"]: r for r in json.loads((RAIZ / "research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.json").read_text())["filas"]}
    filas = []
    for fila in seqs:
        r = {"id": fila, "especie_catalogo": cat[fila]["especie"], "gen_catalogo": cat[fila]["gen"],
             "lectura": "proxy_especie_del_paper", **meta_seq[fila], **resumir([(canon(w), d) for w, d in tam[fila]])}
        # la especie de la secuencia no puede estar en el panel: si esta, el valor es autoacierto
        esp = (r["especie_catalogo"] or "").lower()
        r["autoacierto_especie_en_el_panel"] = ("si: Homalodisca vitripennis es una de las seis referencias; "
                                                "la fraccion limpia NO es riesgo" if "homalodisca" in esp else "no")
        filas.append(r)
    def w(nombre, fs):
        with open(OUT / nombre, "w", newline="", encoding="utf-8") as fh:
            d = csv.DictWriter(fh, fieldnames=list(fs[0]), delimiter="\t", lineterminator="\n"); d.writeheader()
            for x in fs: d.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in x.items()})
    w("eje3_filas_resto.tsv", filas)
    for r in filas:
        print(r["id"], r["gen_catalogo"][:16], "ventanas", r["ventanas_distintas"], "frac", round(r["fraccion_limpia"], 4))

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
    for i in seqs:
        fr = [resumir([(canon(x), d) for x, d in todo[f"{i}__p{j:02d}"]])["fraccion_limpia"] for j in range(N_PERM)]
        real = next(r for r in filas if r["id"] == i)["fraccion_limpia"]
        nulo.append({"id": i, "n_permutaciones": N_PERM, "fraccion_limpia_mediana": statistics.median(fr),
                     "minimo": min(fr), "maximo": max(fr),
                     "real_frente_al_nulo": "dentro del rango del nulo" if min(fr) <= real <= max(fr) else "fuera del rango del nulo"})
        print("nulo", i, round(statistics.median(fr), 4), nulo[-1]["real_frente_al_nulo"], flush=True)
    w("eje3_filas_resto_nulo.tsv", nulo)
    (OUT / "eje3_filas_resto_meta.json").write_text(json.dumps(
        {"semilla_nulo": SEMILLA, "permutaciones": N_PERM, "panel_orden_D76": [c for _, c in PANEL],
         "preregistro": "PREREGISTRO_EJE3_FILAS_NUEVAS.md (43c7fa0), mismo caso",
         "ancla": "eth_Dm reproduce work/sifi_v2 columna por columna",
         "accesiones": {f: meta_seq[f]["accesion"] for f in meta_seq}}, indent=1, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
