"""Valida el supuesto de las bandas de C12 en F1 (pregunta abierta 56, issue #25).

El mismo organismo (Macrosteles quadrilineatus) leido de las dos maneras contra la misma
referencia (Homalodisca vitripennis): brazo P con sus proteinas RefSeq curadas, que es lo que
midio C12, y brazo O con los ORF de seis marcos de sus transcriptos, que es lo que hace F1.
Metodo y criterio de decision: ../PREREGISTRO.md, commiteado antes de esta corrida.

Importa el modulo de F1 y usa sus funciones tal cual: se valida el codigo que corrio.

Uso, desde la raiz del repositorio:
    python research/ola6/F1_transferencia_homologia/validacion_bandas/scripts/validar_bandas.py
"""
from __future__ import annotations

import collections
import csv
import gzip
import hashlib
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import transferir_anotacion as F1  # noqa: E402

REF = Path("work/F1v/ref")
TRABAJO = Path("work/F1v/trabajo")
SALIDA = Path("research/ola6/F1_transferencia_homologia/validacion_bandas/resultados")
DIAMOND = str(Path.home() / ".claude-science/conda/envs/alineador/bin/diamond")

MQ_FAA = Path("work/C11_diseno_nuevo/blast/mq_proteome.faa")
HV_FAA = REF / "GCF_021130785.1_UT_GWSS_2.1_protein.faa"
MQ_RNA = REF / "GCF_028750875.1_UCM_ALF_1.0_rna.fna.gz"
TABLA = REF / "GCF_028750875.1_UCM_ALF_1.0_feature_table.txt.gz"

BANDAS = ["<40", "40-60", "60-80", "80-90", ">=90"]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def wilson(aciertos: int, n: int) -> tuple[float, float]:
    """IC95 de Wilson, el mismo que uso C12."""
    if n == 0:
        return (float("nan"), float("nan"))
    z, p = 1.959963984540054, aciertos / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    s = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - s), min(1.0, c + s))


# --------------------------------------------------------------- insumos
def productos_de_faa(ruta: Path) -> dict[str, str]:
    return {i: F1.producto_refseq(f">{i} {d}" if d else f">{i}")
            for i, d, _ in leer_con_descripcion(ruta)}


def leer_con_descripcion(ruta: Path):
    ident = desc = None
    partes: list[str] = []
    abrir = gzip.open if ruta.suffix == ".gz" else open
    with abrir(ruta, "rt") as fh:
        for linea in fh:
            if linea.startswith(">"):
                if ident:
                    yield ident, desc, "".join(partes)
                cab = linea[1:].strip()
                ident, _, desc = cab.partition(" ")
                partes = []
            else:
                partes.append(linea.strip())
    if ident:
        yield ident, desc, "".join(partes)


def mapa_xm_a_xp(ruta: Path) -> dict[str, str]:
    out = {}
    with gzip.open(ruta, "rt") as fh:
        for f in csv.reader(fh, delimiter="\t"):
            if len(f) > 13 and f[0] == "CDS" and f[10] and f[12]:
                out[f[12]] = f[10]
    return out


# --------------------------------------------------------------- brazos
def correr_par(consulta: Path, etiqueta_q: str, ref: Path, etiqueta_r: str):
    """Recíproco consulta<->ref. Devuelve (mejores directo, mejores inverso)."""
    TRABAJO.mkdir(parents=True, exist_ok=True)
    for faa, et in ((consulta, etiqueta_q), (ref, etiqueta_r)):
        db = TRABAJO / f"db_{et}"
        if not db.with_suffix(".dmnd").exists():
            F1.correr([DIAMOND, "makedb", "--in", str(faa), "-d", str(db)])
    fwd, rev = TRABAJO / f"{etiqueta_q}_a_{etiqueta_r}.tsv", TRABAJO / f"{etiqueta_r}_a_{etiqueta_q}.tsv"
    if not fwd.exists():
        F1.diamond_blastp(DIAMOND, consulta, TRABAJO / f"db_{etiqueta_r}", fwd)
    if not rev.exists():
        F1.diamond_blastp(DIAMOND, ref, TRABAJO / f"db_{etiqueta_q}", rev)
    return F1.mejores(fwd), F1.mejores(rev)


def escribir_orfs(xm_a_xp: dict[str, str]) -> tuple[Path, int, int, int]:
    """Seis marcos de cada transcripto con CDS anotado. Mismo MIN_AA que F1."""
    destino = TRABAJO / "orfs_MQ.faa"
    TRABAJO.mkdir(parents=True, exist_ok=True)
    n_orf = n_tx = sin_cds = 0
    if destino.exists():
        with open(destino) as fh:
            n_orf = sum(1 for l in fh if l.startswith(">"))
        return destino, n_orf, -1, -1
    with open(destino, "w") as out:
        for ident, _desc, seq in leer_con_descripcion(MQ_RNA):
            if ident not in xm_a_xp:
                sin_cds += 1
                continue
            n_tx += 1
            for aa, hebra, ini, fin in F1.todos_los_orfs(seq):
                n_orf += 1
                out.write(f">{ident}|{hebra}|{ini}-{fin}\n{aa}\n")  # sin espacios: diamond trunca el id ahi
    return destino, n_orf, n_tx, sin_cds


# --------------------------------------------------------------- metrica
def concordancia(pares: list[dict]) -> dict:
    """Por banda: n, aciertos, concordancia, IC95. `pares` ya filtrado a los comparables."""
    out = {}
    for b in BANDAS:
        sel = [p for p in pares if p["banda"] == b]
        ac = sum(1 for p in sel if p["acierta"])
        lo, hi = wilson(ac, len(sel))
        out[b] = dict(n=len(sel), aciertos=ac,
                      conc=round(ac / len(sel), 4) if sel else None,
                      lo=round(lo, 4) if sel else None, hi=round(hi, 4) if sel else None)
    ac, n = sum(p["acierta"] for p in pares), len(pares)
    out["total"] = dict(n=n, aciertos=ac, conc=round(ac / n, 4) if n else None,
                        lo=None, hi=None)
    return out


def pares_del_brazo(ids, verdad, directo, inverso, productos_ref, regla):
    """Una entrada por consulta recíproca con nombre informativo en los dos lados."""
    pares = []
    clasif = F1.clasificar if regla == "estricta" else F1.clasificar_ampliada
    kcat = "categoria" if regla == "estricta" else "categoria_ampliada"
    kref = "ref_producto" if regla == "estricta" else "ampliada_ref_producto"
    kpid = "pident" if regla == "estricta" else "ampliada_pident"
    kcob = ("cob_orf", "cob_ref") if regla == "estricta" else ("ampliada_cob_orf", "ampliada_cob_ref")
    for i in ids:
        r = clasif(i, directo, inverso, productos_ref)
        if r[kcat] != "f_reciproco_con_nombre":
            continue
        v = verdad.get(i)
        if not v or not F1.es_informativo(v):
            continue
        pid = float(r[kpid])
        pares.append(dict(consulta=i, verdad=F1.normalizar_nombre(v),
                          transferido=F1.normalizar_nombre(r[kref]),
                          acierta=F1.normalizar_nombre(v) == F1.normalizar_nombre(r[kref]),
                          pident=pid, banda=F1.banda(pid)[0],
                          cobertura=F1.rotulo_cobertura(float(r[kcob[0]]), float(r[kcob[1]])),
                          gen=verdad_xp[i]))
    return pares


def main() -> None:
    global verdad_xp
    SALIDA.mkdir(parents=True, exist_ok=True)
    print("[1/6] insumos", flush=True)
    prod_hv = productos_de_faa(HV_FAA)
    prod_mq = productos_de_faa(MQ_FAA)
    xm_xp = mapa_xm_a_xp(TABLA)
    print(f"      HV {len(prod_hv)} proteinas, MQ {len(prod_mq)}, CDS con XM->XP {len(xm_xp)}", flush=True)

    print("[2/6] brazo P: proteinas curadas de MQ contra HV", flush=True)
    dP, iP = correr_par(MQ_FAA, "MQprot", HV_FAA, "HV")

    print("[3/6] ORF de seis marcos de los transcriptos de MQ", flush=True)
    orf_faa, n_orf, n_tx, sin_cds = escribir_orfs(xm_xp)
    print(f"      {n_orf} ORF de {n_tx} transcriptos con CDS ({sin_cds} sin CDS, excluidos)", flush=True)

    print("[4/6] brazo O: esos ORF contra HV", flush=True)
    dO, iO = correr_par(orf_faa, "MQorf", HV_FAA, "HV")

    print("[5/6] concordancia", flush=True)
    verdad_xp = {}
    verdad_P = {}
    for xp, p in prod_mq.items():
        verdad_P[xp] = p
        verdad_xp[xp] = xp
    ids_P = list(prod_mq)

    verdad_O, ids_O = {}, []
    with open(orf_faa) as fh:
        for l in fh:
            if l.startswith(">"):
                oid = l[1:].strip()
                xm = oid.split("|")[0]
                xp = xm_xp.get(xm)
                if xp and xp in prod_mq:
                    verdad_O[oid] = prod_mq[xp]
                    verdad_xp[oid] = xp
                    ids_O.append(oid)

    res, pares_guardar = {}, {}
    for regla in ("estricta", "ampliada"):
        pP = pares_del_brazo(ids_P, verdad_P, dP, iP, prod_hv, regla)
        pO = pares_del_brazo(ids_O, verdad_O, dO, iO, prod_hv, regla)
        if not pP or not pO:  # un brazo vacio es un error de identificadores, no un resultado
            sys.exit(f"ABORTA: regla {regla} dio {len(pP)} pares en P y {len(pO)} en O")
        genes = {p["gen"] for p in pP} & {p["gen"] for p in pO}
        res[regla] = dict(
            no_pareado=dict(P=concordancia(pP), O=concordancia(pO)),
            pareado=dict(P=concordancia([p for p in pP if p["gen"] in genes]),
                         O=concordancia([p for p in pO if p["gen"] in genes]),
                         genes_en_comun=len(genes)),
            cobertura_O=dict(collections.Counter(p["cobertura"] for p in pO)))
        pares_guardar[regla] = (pP, pO)

    print("[6/6] veredicto y salidas", flush=True)
    veredicto = {}
    for regla in ("estricta", "ampliada"):
        par = res[regla]["pareado"]
        v = {}
        for b in BANDAS:
            P, O = par["P"][b], par["O"][b]
            if P["n"] < 100 or O["n"] < 100:
                v[b] = "no decide (n < 100)"
            elif O["conc"] < P["lo"]:
                v[b] = "sobredeclara"
            elif O["conc"] > P["hi"]:
                v[b] = "subdeclara"
            else:
                v[b] = "se sostiene"
        veredicto[regla] = v

    with open(SALIDA / "bandas_por_brazo.tsv", "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["regla", "analisis", "brazo", "banda", "n", "aciertos", "concordancia",
                    "ic95_lo", "ic95_hi", "c12_concordancia", "c12_n"])
        c12 = {b: (c, n) for _, b, c, _, _, n in F1.BANDAS_C12}
        for regla in ("estricta", "ampliada"):
            for an in ("no_pareado", "pareado"):
                for brazo in ("P", "O"):
                    for b in BANDAS + ["total"]:
                        d = res[regla][an][brazo][b]
                        w.writerow([regla, an, brazo, b, d["n"], d["aciertos"], d["conc"],
                                    d["lo"], d["hi"], *(c12.get(b, ("", "")))])

    for regla, (pP, pO) in pares_guardar.items():
        for brazo, pares in (("P", pP), ("O", pO)):
            with gzip.open(SALIDA / f"pares_{brazo}_{regla}.tsv.gz", "wt", newline="") as fh:
                w = csv.writer(fh, delimiter="\t")
                w.writerow(["consulta", "gen_xp", "verdad", "transferido", "acierta",
                            "pident", "banda", "cobertura"])
                for p in pares:
                    w.writerow([p["consulta"], p["gen"], p["verdad"], p["transferido"],
                                int(p["acierta"]), p["pident"], p["banda"], p["cobertura"]])

    resumen = dict(
        pregunta="56 (issue #25): valen las bandas de C12 sobre ORF de un transcriptoma",
        preregistro="validacion_bandas/PREREGISTRO.md",
        diamond=F1.correr([DIAMOND, "version"]).strip(),
        insumos={k: dict(ruta=str(p), sha256=sha256(p)) for k, p in
                 (("MQ_proteoma", MQ_FAA), ("HV_proteoma", HV_FAA),
                  ("MQ_rna", MQ_RNA), ("feature_table", TABLA))},
        conteos=dict(MQ_proteinas=len(prod_mq), HV_proteinas=len(prod_hv),
                     transcriptos_con_CDS=n_tx, transcriptos_sin_CDS=sin_cds, orfs=n_orf),
        resultados=res, veredicto=veredicto)
    (SALIDA / "resumen.json").write_text(json.dumps(resumen, indent=1, ensure_ascii=False))
    print(json.dumps(veredicto, indent=1, ensure_ascii=False))
    for regla in ("estricta", "ampliada"):
        for an in ("pareado", "no_pareado"):
            extra = (f" ({res[regla]['pareado']['genes_en_comun']} genes en comun)"
                     if an == "pareado" else "")
            print(f"\n-- {regla}, {an}{extra}")
            for b in BANDAS + ["total"]:
                P, O = res[regla][an]["P"][b], res[regla][an]["O"][b]
                print(f"   {b:7s} P {str(P['conc']):7s} [{P['lo']},{P['hi']}] (n={P['n']:5d})   "
                      f"O {str(O['conc']):7s} [{O['lo']},{O['hi']}] (n={O['n']:5d})")
        print(f"   cobertura de los pares O: {res[regla]['cobertura_O']}")


if __name__ == "__main__":
    main()
