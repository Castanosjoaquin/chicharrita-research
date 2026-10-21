"""Conservacion de cada ventana de 21 nt entre fuentes independientes, y que region sobrevive.

Contesta una pregunta que ninguna herramienta del corpus se hace: de las ventanas que el
ranking llama eficientes y limpias, cuantas existen identicas en otras poblaciones y
aislados? Una region muy limpia que funciona en un solo aislado no sirve.

Tres partes, cada una con su fuente:

  amplicon   Donde caen los cebadores de Andrada et al. 2026 (Tabla 1) sobre la secuencia
             publica de `eth` y `burs-alpha`, para saber que porcion de nuestras regiones
             de 200 nt esta dentro de la molecula que SI se probo. La orientacion de los
             cebadores se infiere de donde aparece cada uno sobre la secuencia; las
             posiciones no estan en el texto del articulo (estan en la Figura S1, que no
             se leyo) y por eso es una inferencia nuestra.
  insecto    Ventanas de BicC_Dm, ATPaseD_Dm, eth_Dm y bursA_Dm contra: los transcriptomas
             de D. maidis (alineamiento local contra los contigs TSA que ya habia ubicado
             W5, que son de Illinois, de Ohio State y de Argentina (depositado desde el CeBio, Pergamino)) y los tres
             ensamblados genomicos (UK haplotipo 1 y 2, que son del mismo individuo, y CIAP
             v1, de Cordoba, Argentina; este ultimo es solo ONT y se lee con tolerancia de
             un desajuste, porque la tasa de error del ensamblado es del orden de la
             variacion que se quiere medir).
  virus      Ventanas de MP_MRFV y CP_MRFV contra los 71 registros de MRFV en GenBank, por
             alineamiento local de cada gen contra cada registro.

Nada sale de la maquina: las secuencias de EPILAB (BicC_Dm, ATPaseD_Dm) se alinean contra
datos publicos bajados a disco; los unicos servicios web usados son NCBI para BAJAR
registros publicos.

Uso:
    python conservacion.py --trabajo work/sifi_v2 --datos <dir con cons/> \
        --json research/ola3/C8_conservacion/resultados/conservacion.json
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import numpy as np
from Bio.Align import PairwiseAligner

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ranking as R  # noqa: E402
import ranking_v2 as V2  # noqa: E402

K = 21
COMP = str.maketrans("ACGT", "TGCA")


def rc(s: str) -> str:
    return s.translate(COMP)[::-1]


def leer_fasta(ruta: Path) -> list[tuple[str, str]]:
    out, nom, buf = [], None, []
    for l in ruta.read_text().splitlines():
        if l.startswith(">"):
            if nom:
                out.append((nom, "".join(buf).upper().replace("U", "T")))
            nom, buf = l[1:].strip().split()[0], []
        else:
            buf.append(l.strip())
    if nom:
        out.append((nom, "".join(buf).upper().replace("U", "T")))
    return out


# ---------------------------------------------------------------- 1. amplicones

# Tabla 1 de Andrada et al. 2026 (Front Insect Sci 6:1811933), leida en PMC13279319.
# Los rotulos F/R del articulo no coinciden con la orientacion real sobre la secuencia
# (el "forward" de eth es antisentido), asi que se mapea cada cebador en las dos hebras.
CEBADORES = {
    "eth_Dm": {"largo_amplicon": 544,
               "dsRNA_a": "TCTCCTCCCTCCATAGCGTT", "dsRNA_b": "TCACCCCAGGAGCACAGAAT",
               "qPCR_a": "GTCCTTGAAAAGGTGCACTCC", "qPCR_b": "ACGCTATGGAGGGAGGAGAA",
               "qPCR_largo": 96},
    "bursA_Dm": {"largo_amplicon": 578,
                 "dsRNA_a": "AAGTCCTCCCCTGTCTCCTC", "dsRNA_b": "AGCCAACAAAGATAGCTGAGT",
                 "qPCR_a": "TGTGTGTTTCTTCCCTGATGGC", "qPCR_b": "CCCACAACAGGGCTACCAAC",
                 "qPCR_largo": 90},
}


def ubicar(seq: str, p: str) -> dict | None:
    for hebra, q in (("sentido", p), ("antisentido", rc(p))):
        i = seq.find(q)
        if i >= 0:
            return {"hebra_del_cebador": "sentido" if hebra == "sentido" else "antisentido",
                    "inicio": i + 1, "fin": i + len(q)}
    return None


def amplicones(seqs: dict[str, str]) -> dict:
    """Cobertura de la molecula probada, en coordenadas de la secuencia publica.

    Un cebador con la secuencia del sentido se extiende hacia 3'; uno con la del
    antisentido se extiende hacia 5'. Con un solo cebador mapeado y el largo declarado
    del amplicon se ubica el otro extremo, que cae fuera de la secuencia publica (es
    UTR). Es una inferencia nuestra, no una lectura del articulo.
    """
    out = {}
    for gen, c in CEBADORES.items():
        s = seqs[gen]
        d = {"largo_secuencia_publica": len(s), "largo_amplicon": c["largo_amplicon"]}
        for n in ("dsRNA_a", "dsRNA_b", "qPCR_a", "qPCR_b"):
            d[n] = ubicar(s, c[n])
        m = d["dsRNA_a"] or d["dsRNA_b"]
        L = c["largo_amplicon"]
        if m["hebra_del_cebador"] == "sentido":
            lo, hi = m["inicio"], m["inicio"] + L - 1
        else:
            lo, hi = m["fin"] - L + 1, m["fin"]
        d["amplicon_coordenadas"] = [lo, hi]
        d["en_secuencia_publica"] = [max(lo, 1), min(hi, len(s))]
        d["fuera_de_la_secuencia_publica_nt"] = (max(0, 1 - lo) + max(0, hi - len(s)))
        qs = [d["qPCR_a"], d["qPCR_b"]]
        if all(qs):
            d["qPCR_amplicon"] = [min(q["inicio"] for q in qs), max(q["fin"] for q in qs)]
        out[gen] = d
    return out


def solapa(region: tuple[int, int], k: int, cubierto: tuple[int, int]) -> dict:
    """Cuanto de una region (de ventanas) cae dentro del tramo probado.

    Una region [a, b] cuenta ventanas que EMPIEZAN en a..b, asi que ocupa a..b+k-1.
    """
    a, b = region
    lo, hi = max(a, cubierto[0]), min(b + k - 1, cubierto[1])
    n = max(0, hi - lo + 1)
    return {"ocupa": [a, b + k - 1], "nt_dentro": n, "nt_total": b + k - a,
            "fraccion": round(n / (b + k - a), 3)}


# ----------------------------------------------------------------- alineamientos

def alineador() -> PairwiseAligner:
    al = PairwiseAligner()
    al.mode = "local"
    al.match_score, al.mismatch_score = 2, -3
    al.open_gap_score, al.extend_gap_score = -6, -2
    return al


def estado_por_posicion(gen: str, otro: str, al: PairwiseAligner, minimo: int = 40):
    """Alinea `gen` contra `otro` en las dos hebras. Devuelve un vector por posicion:
    0 sin cobertura, 1 alineada e identica, 2 alineada con desajuste, 3 dentro del
    tramo alineado pero en un hueco (indel). Y el span alineado."""
    mejor = None
    for hebra, t in (("+", otro), ("-", rc(otro))):
        try:
            aln = al.align(gen, t)[0]
        except (IndexError, ValueError):
            continue
        if mejor is None or aln.score > mejor[0].score:
            mejor = (aln, t, hebra)
    n = len(gen)
    est = np.zeros(n, dtype=np.int8)
    if mejor is None or mejor[0].score < minimo:
        return est, None
    aln, t, hebra = mejor
    bloques = aln.aligned
    q0, q1 = int(bloques[0][0][0]), int(bloques[0][-1][1])
    est[q0:q1] = 3
    ident = 0
    cortes = []
    prev = None
    for (qa, qb), (ta, tb) in zip(bloques[0], bloques[1]):
        for i, j in zip(range(qa, qb), range(ta, tb)):
            est[i] = 1 if gen[i] == t[j] else 2
            ident += gen[i] == t[j]
        # insercion en el otro (contiguo en `gen`, saltado en el otro): corte entre qa-1 y qa
        if prev is not None and qa == prev[0] and ta > prev[1]:
            cortes.append(int(qa))
        prev = (qb, tb)
    return est, {"hebra": hebra, "span": [q0 + 1, q1],
                 "identidad": round(ident / max(1, (est[q0:q1] > 0).sum()), 4),
                 "puntaje": float(aln.score), "cortes": cortes}


def ventanas(est: np.ndarray, cortes=(), k: int = K) -> np.ndarray:
    """Por ventana: 0 sin datos, 1 conservada exacta, 2 variante (desajuste o indel).
    Una ventana solo tiene datos si sus k posiciones caen dentro del tramo alineado."""
    n = len(est)
    out = np.zeros(n - k + 1, dtype=np.int8)
    for i in range(n - k + 1):
        w = est[i:i + k]
        if (w == 0).any():
            continue
        corte = any(i < c <= i + k - 1 for c in cortes)
        out[i] = 1 if ((w == 1).all() and not corte) else 2
    return out


def combinar(estados: list[np.ndarray]) -> np.ndarray:
    """Varios contigs de la misma fuente: gana la mejor evidencia (conservada > variante)."""
    n = len(estados[0])
    out = np.zeros(n, dtype=np.int8)
    for e in estados:
        out = np.where((e == 1) | ((e == 2) & (out == 0)), e, out)
    return out


# ---------------------------------------------------------------------- insecto

TSA_FUENTES = {
    "GCWP01 (Illinois, 454)": ["GCWP01003535.1", "GCWP01003534.1", "GCWP01004693.1",
                               "GCWP01004692.1", "GCWP01010867.1"],
    "GITV01 (Ohio State, Illumina)": ["GITV01000968.1", "GITV01001458.1"],
    "GHCC01 (Argentina, Illumina)": ["GHCC01002326.1", "GHCC01051703.1"],
}


def tsa_estados(datos: Path, gen: str, seq: str, al) -> dict:
    out = {}
    for fuente, ids in TSA_FUENTES.items():
        ests, info = [], []
        for i in ids:
            ruta = datos / "tsa" / ("%s.fa" % i)
            if not ruta.exists():
                continue
            otro = leer_fasta(ruta)[0][1]
            e, meta = estado_por_posicion(seq, otro, al)
            w_ = ventanas(e, meta["cortes"]) if meta else None
            # un contig del otro gen alinea mal: se descarta por identidad baja
            if meta and meta["identidad"] >= 0.9 and (meta["span"][1] - meta["span"][0]) >= 100:
                ests.append(w_)
                info.append(dict(meta, contig=i))
        if ests:
            out[fuente] = {"estado": combinar(ests), "contigs": info}
    return out


def genoma_estado(tsv: Path, gen: str, n_vent: int) -> tuple[np.ndarray, np.ndarray]:
    """De la salida de offtarget_21nt.py: por ventana, presente exacta y presente con un desajuste."""
    ex = np.zeros(n_vent, dtype=bool)
    m1 = np.zeros(n_vent, dtype=bool)
    with tsv.open(encoding="utf-8") as fh:
        r = csv.DictReader(fh, delimiter="\t")
        cols = [c for c in r.fieldnames if "|" in c]
        for f in r:
            if f["consulta"] != "%s_full" % gen:
                continue
            i = int(f["pos"]) - 1
            if 0 <= i < n_vent:
                for c in cols:
                    if c.endswith("|perfecto_21") and int(f[c] or 0) > 0:
                        ex[i] = True
                    if c.endswith("|mm1_21") and int(f[c] or 0) > 0:
                        m1[i] = True
    return ex, m1


# ------------------------------------------------------------------------ virus

def mrfv_meta(gb: Path) -> dict[str, dict]:
    out = {}
    for r in gb.read_text().split("\n//\n"):
        if "LOCUS" not in r:
            continue
        v = re.search(r"^VERSION\s+(\S+)", r, re.M).group(1)
        g = re.search(r'/geo_loc_name="([^"]+)"', r) or re.search(r'/country="([^"]+)"', r)
        i = re.search(r'/isolate="([^"]+)"', r) or re.search(r'/strain="([^"]+)"', r)
        f = re.search(r'/collection_date="([^"]+)"', r)
        out[v] = {"pais": g.group(1).split(":")[0] if g else "sin dato",
                  "aislado": i.group(1) if i else "", "fecha": f.group(1) if f else ""}
    return out


def virus_conservacion(datos: Path, seqs: dict[str, str], al) -> dict:
    """Por gen y por ventana, en cuantos registros de GenBank esta identica.

    Guarda el estado por registro para poder recortar por pais despues. Un registro entra
    si alinea con identidad de al menos 0,8 sobre un tramo de 60 nt o mas."""
    regs = leer_fasta(datos / "mrfv" / "MRFV_all.fasta")
    meta = mrfv_meta(datos / "mrfv" / "MRFV_all.gb")
    out = {}
    for gen in ("MP_MRFV", "CP_MRFV"):
        s = seqs[gen]
        por_reg = []
        for nom, otro in regs:
            e, m = estado_por_posicion(s, otro, al, minimo=60)
            if m is None or m["identidad"] < 0.8:
                continue
            w = ventanas(e, m["cortes"])
            por_reg.append({"registro": nom, "pais": meta.get(nom, {}).get("pais", "sin dato"),
                            "aislado": meta.get(nom, {}).get("aislado", ""),
                            "span": m["span"], "identidad": m["identidad"],
                            "ventanas_con_datos": int((w > 0).sum()),
                            "ventanas_identicas": int((w == 1).sum()), "_w": w})
        out[gen] = por_reg
    return out


def resumen_virus(regs: list[dict], n_v: int, paises=None) -> tuple[np.ndarray, np.ndarray]:
    cob = np.zeros(n_v, dtype=int)
    con = np.zeros(n_v, dtype=int)
    for r in regs:
        if paises and r["pais"] not in paises:
            continue
        cob += (r["_w"] > 0)
        con += (r["_w"] == 1)
    return cob, con


# -------------------------------------------------------------------- regiones

def mejor_region(eficiente, limpia, conservada, largo, lo=1, hi=None):
    """La region de `largo` con mas ventanas eficientes y limpias y conservadas."""
    n = len(eficiente)
    ok = (eficiente & limpia & conservada).astype(int)
    acum = np.concatenate([[0], np.cumsum(ok)])
    hi = hi or n
    mejor, nm = None, -1
    for a in range(lo, hi - largo + 2):
        b = a + largo - 1
        if b > n:
            break
        c = int(acum[b] - acum[a - 1])
        if c > nm:
            nm, mejor = c, (a, b)
    return mejor, nm


def clasificar_ventanas(trabajo: Path, genes: dict) -> dict:
    """Eficiente y limpia por ventana, de los mismos objetos que usa el ranking v2."""
    out = {}
    for g, d in genes.items():
        n = d["n"]
        hayalgo = np.zeros(n, dtype=bool)
        for ref, crits in d["riesgo"].items():
            if ref == R.DMAIDIS and g in ("BicC_Dm", "ATPaseD_Dm", "eth_Dm", "bursA_Dm"):
                continue
            for c in R.CRITERIOS:
                hayalgo |= crits[c]
        out[g] = {"eficiente": d["eficiente"], "limpia": ~hayalgo, "n": n}
    return out


def region_stats(cl, cons, sin_datos, ini, fin):
    sl = slice(ini - 1, fin)
    e, l, c, sd = cl["eficiente"][sl], cl["limpia"][sl], cons[sl], sin_datos[sl]
    return {"ventanas": int(len(e)), "eficientes": int(e.sum()),
            "eficientes_conservadas": int((e & c).sum()),
            "eficientes_sin_datos": int((e & sd).sum()),
            "eficientes_limpias_conservadas": int((e & l & c).sum())}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trabajo", default="work/sifi_v2")
    ap.add_argument("--datos", required=True, help="dir con tsa/, mrfv/ y gen/")
    ap.add_argument("--v2", default="research/ola3/C7_ranking_v2/resultados/ranking_v2.json")
    ap.add_argument("--json", required=True)
    a = ap.parse_args(argv)
    trabajo, datos = Path(a.trabajo), Path(a.datos)
    seqs = {g: leer_fasta(trabajo / "fasta" / ("%s_full.fasta" % g))[0][1]
            for g in ("MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm", "eth_Dm", "bursA_Dm")}
    v2 = json.loads(Path(a.v2).read_text(encoding="utf-8"))
    al = alineador()
    res = {"amplicones": amplicones(seqs)}
    V2.con_panel(sin_humano=False)
    genes = V2.cargar(trabajo, 21, list(seqs))
    cl = clasificar_ventanas(trabajo, genes)
    regiones_epilab = {c["gen"]: c["region"] for c in R.CANDIDATOS}
    reg_v2 = {g: tuple(int(x) for x in r.split("-")) for g, r in v2["k"]["21"]["regiones"].items()}
    reg_rec = {g: tuple(int(x) for x in r.split("-")) for g, r in v2["k"]["21"]["regiones_recomendadas"].items()}
    largo = {g: (reg_v2[g][1] - reg_v2[g][0] + 1) for g in reg_v2}

    # ----------------------------------------- que parte de la molecula probada cubrimos
    wr, wc = R.pesos_base()
    rp = {}
    for kk in (21, 22):
        gk = V2.cargar(trabajo, kk, ["eth_Dm", "bursA_Dm"])
        rp[str(kk)] = {}
        for g in ("eth_Dm", "bursA_Dm"):
            cub = tuple(res["amplicones"][g]["en_secuencia_publica"])
            cand = {"gen": g, "estrategia": "insecto"}
            reg_k = tuple(int(x) for x in v2["k"][str(kk)]["regiones"][g].split("-"))
            item = {"cubierto": list(cub), "propuesta_v2": {"region": list(reg_k),
                                                           **solapa(reg_k, kk, cub)}}
            mejor = None
            for ini in range(cub[0], cub[1] - 200 - kk + 3):
                fin = ini + 199
                if fin + kk - 1 > cub[1]:
                    break
                e = R.ejes(gk[g], ini, fin, wr, wc, R.excluidas_de(cand, "off"), False)
                if e["vetada"]:
                    continue
                clave = (e["buenos_limpios"], -ini)
                if mejor is None or clave > mejor[0]:
                    mejor = (clave, ini, fin, e)
            if mejor:
                _, ini, fin, e = mejor
                item["mejor_dentro_de_lo_probado"] = {
                    "region": [ini, fin], "eficientes": e["eficientes"],
                    "limpias_y_eficientes": e["buenos_limpios"], "limpieza": round(e["limpieza"], 4),
                    **solapa((ini, fin), kk, cub)}
            e0 = R.ejes(gk[g], reg_k[0], reg_k[1], wr, wc, R.excluidas_de(cand, "off"), False)
            item["propuesta_v2"].update({"eficientes": e0["eficientes"],
                                         "limpias_y_eficientes": e0["buenos_limpios"]})
            rp[str(kk)][g] = item
    res["region_probada"] = rp

    # ---------------------------------------------------------------- insecto
    ins = {}
    for g in ("BicC_Dm", "ATPaseD_Dm", "eth_Dm", "bursA_Dm"):
        s, nv = seqs[g], len(seqs[g]) - K + 1
        tsa = tsa_estados(datos, g, s, al)
        gen = {}
        for etiqueta, d in (("UK hap1", trabajo / "offtarget_dm_k21"),
                            ("UK hap2", trabajo / "cons_hap2"),
                            ("Cordoba CIAP", trabajo / "cons_ciap")):
            t = d / "offtarget_por_sirna.tsv"
            if t.exists():
                gen[etiqueta] = genoma_estado(t, g, nv)
        r = {"n_ventanas": nv, "transcriptomas": {}, "genomas": {}}
        for f, x in tsa.items():
            e = x["estado"]
            r["transcriptomas"][f] = {"con_datos": int((e > 0).sum()), "conservadas": int((e == 1).sum()),
                                      "variantes": int((e == 2).sum()), "contigs": x["contigs"]}
        base = gen.get("UK hap1")
        for f, (ex, m1) in gen.items():
            r["genomas"][f] = {"exactas": int(ex.sum()), "un_desajuste": int((m1 & ~ex).sum()),
                               "ausentes": int((~ex & ~m1).sum())}
            if base is not None and f != "UK hap1":
                b = base[0]
                r["genomas"][f].update({
                    "presentes_en_hap1": int(b.sum()),
                    "de_esas_exactas": int((ex & b).sum()),
                    "de_esas_con_un_desajuste": int((m1 & ~ex & b).sum()),
                    "de_esas_ausentes": int((b & ~ex & ~m1).sum())})
        # Criterio de conservacion: SOLO los transcriptomas, que no tienen intrones ni
        # la tasa de error del ONT. El haplotipo 2 del UK es un ensamblado alternativo
        # incompleto (no tiene el locus de ATPaseD, eth ni burs-alpha) y CIAP es solo
        # ONT: los dos se reportan como descripcion, no entran al criterio.
        n_eval = np.zeros(nv, dtype=int)
        n_ok = np.zeros(nv, dtype=int)
        for f, x in tsa.items():
            e = x["estado"]
            n_eval += (e > 0)
            n_ok += (e == 1)
        cons = (n_eval >= 2) & (n_ok == n_eval)
        sin = n_eval < 2
        arg = next((x["estado"] for f, x in tsa.items() if "Argentina" in f), None)
        cons_arg = (arg == 1) if arg is not None else np.zeros(nv, dtype=bool)
        ciap = gen.get("Cordoba CIAP")
        ins[g] = {"cons": cons, "sin_datos": sin, "cons_arg": cons_arg, "n_eval": n_eval,
                  "n_ok": n_ok, "nv": nv, "hap1": base[0] if base else None,
                  "ciap_ex": ciap[0] if ciap else None, "ciap_m1": ciap[1] if ciap else None}
        r["fuentes_transcriptoma_por_ventana"] = {str(k): int((n_eval == k).sum()) for k in range(0, 4)}
        r["ventanas_conservadas_en_los_transcriptomas"] = int(cons.sum())
        r["ventanas_conservadas_en_Argentina"] = int(cons_arg.sum())
        r["ventanas_sin_transcriptoma_suficiente"] = int(sin.sum())
        # SNPs: tramos de ventanas variantes en transcriptomas
        r["variantes_en_transcriptomas"] = {}
        for f, x in tsa.items():
            e = x["estado"]
            tr, i = [], 0
            while i < len(e):
                if e[i] == 2:
                    j = i
                    while j < len(e) and e[j] == 2:
                        j += 1
                    tr.append([i + 1, j + K - 1])
                    i = j
                else:
                    i += 1
            r["variantes_en_transcriptomas"][f] = tr
        res.setdefault("insecto", {})[g] = r

    reg_ins = {}

    def stats_ins(g, d, rg):
        ini, fin = rg
        sl = slice(ini - 1, fin)
        e, l = cl[g]["eficiente"][sl], cl[g]["limpia"][sl]
        out = {"region": list(rg), "ventanas": int(len(e)), "eficientes": int(e.sum())}
        ev = R.ejes(genes[g], ini, fin, wr, wc, R.excluidas_de({"gen": g, "estrategia": "insecto"}, "off"), False)
        out.update({"con_21_perfecto": ev["con_21_perfecto"], "vetada": ev["vetada"],
                    "limpieza": round(ev["limpieza"], 4), "limpias_y_eficientes": ev["buenos_limpios"]})
        if g in ("BicC_Dm", "ATPaseD_Dm"):
            c, ca = d["cons"][sl], d["cons_arg"][sl]
            out.update({"eficientes_conservadas_en_todos_los_transcriptomas": int((e & c).sum()),
                        "eficientes_conservadas_en_Argentina": int((e & ca).sum()),
                        "eficientes_limpias_conservadas": int((e & l & c).sum())})
        h, ex, m1 = d["hap1"], d["ciap_ex"], d["ciap_m1"]
        if h is not None and ex is not None:
            ev = e & h[sl]
            out.update({"eficientes_presentes_en_hap1": int(ev.sum()),
                        "de_esas_exactas_en_CIAP": int((ev & ex[sl]).sum()),
                        "de_esas_con_un_desajuste_en_CIAP": int((ev & ~ex[sl] & m1[sl]).sum()),
                        "de_esas_ausentes_en_CIAP": int((ev & ~ex[sl] & ~m1[sl]).sum())})
        return out

    for g, d in ins.items():
        item = {}
        for et, rg in (("v2_nivel1", reg_v2[g]), ("v2_recomendada", reg_rec[g])):
            item[et] = stats_ins(g, d, rg)
        if g in regiones_epilab:
            item["epilab"] = stats_ins(g, d, regiones_epilab[g])
        if g in ("BicC_Dm", "ATPaseD_Dm"):
            b, nb = mejor_region(cl[g]["eficiente"], cl[g]["limpia"], d["cons"], largo[g])
            item["mejor_por_conservacion"] = stats_ins(g, d, b)
            b2, nb2 = mejor_region(cl[g]["eficiente"], np.ones(d["nv"], dtype=bool), d["cons"], largo[g])
            item["mejor_por_conservacion_sin_filtro_off_target"] = stats_ins(g, d, b2)
        reg_ins[g] = item
    res["regiones_insecto"] = reg_ins

    # ------------------------------------------------------------------ virus
    vreg = virus_conservacion(datos, seqs, al)
    res["virus"] = {}
    res["regiones_virus"] = {}
    for g in ("MP_MRFV", "CP_MRFV"):
        nv = len(seqs[g]) - K + 1
        regs = vreg[g]
        cob, con = resumen_virus(regs, nv)
        cob_br, con_br = resumen_virus(regs, nv, {"Brazil"})
        res["virus"][g] = {
            "n_ventanas": nv, "registros_con_alineamiento": len(regs),
            "por_pais": {p: sum(1 for r in regs if r["pais"] == p) for p in sorted({r["pais"] for r in regs})},
            "cobertura_mediana": int(np.median(cob)), "cobertura_max": int(cob.max()),
            "registros": [{k: v for k, v in r.items() if k != "_w"} for r in regs]}
        out_g = {}
        for etiqueta, (c_, k_) in (("todos", (cob, con)), ("solo_Brasil", (cob_br, con_br))):
            frac = np.where(c_ >= 10, k_ / np.maximum(c_, 1), np.nan)
            out_g[etiqueta] = {"ventanas_con_al_menos_10_registros": int((c_ >= 10).sum()),
                               "conservadas_ge_90": int(np.nansum(frac >= 0.9)) if (c_ >= 10).any() else 0,
                               "conservadas_ge_75": int(np.nansum(frac >= 0.75)) if (c_ >= 10).any() else 0,
                               "conservadas_ge_50": int(np.nansum(frac >= 0.5)) if (c_ >= 10).any() else 0,
                               "mediana_fraccion": (round(float(np.nanmedian(frac)), 3)
                                                    if (c_ >= 10).any() else None)}
        res["virus"][g]["resumen"] = out_g
        # regiones, con el umbral >=75 % de los registros que cubren la ventana (>=10)
        reg_g = {}
        for etiqueta, (c_, k_) in (("todos", (cob, con)), ("solo_Brasil", (cob_br, con_br))):
            ok = (c_ >= 10) & (k_ >= 0.75 * np.maximum(c_, 1))
            sd = c_ < 10
            item = {}
            for et, rg in (("epilab", regiones_epilab[g]), ("v2_recomendada", reg_rec[g])):
                item[et] = {"region": list(rg), **region_stats(cl[g], ok, sd, *rg)}
            b, nb = mejor_region(cl[g]["eficiente"], cl[g]["limpia"], ok, 200)
            item["mejor_por_conservacion"] = ({"region": list(b), "eficientes_limpias_conservadas": nb,
                                               **region_stats(cl[g], ok, sd, *b)} if nb >= 0 else None)
            reg_g[etiqueta] = item
        res["regiones_virus"][g] = reg_g

    # ---- el ranking v2 de nivel 3, con la region de BicC_Dm cambiada por la mejor por conservacion
    cands = V2.completar_regiones(genes, wr, wc)
    rec = V2.recomendadas(cands, genes, wr, wc)
    mejor_bicc = tuple(res["regiones_insecto"]["BicC_Dm"]["mejor_por_conservacion"]["region"])
    rec_c = []
    for c in rec:
        d = dict(c)
        if d["gen"] == "BicC_Dm":
            d["region"] = mejor_bicc
        rec_c.append(d)
    rk = {}
    for etiqueta, conj in (("v2_recomendadas", rec), ("con_BicC_por_conservacion", rec_c)):
        r = R.barrer(conj, genes, "geometrica", False, "off", 2000, np.random.default_rng(7), "absoluta")
        rc_ = R.barrer(conj, genes, "cascada", False, "off", 2000, np.random.default_rng(7), "absoluta")
        rk[etiqueta] = {"regiones": {d["gen"]: "%d-%d" % d["region"] for d in conj},
                        "geometrica_conservadora_absoluta": {"frecuencia": r["frecuencia"],
                                                              "orden_modal": r["ordenes"][0]},
                        "cascada": {"orden_modal": rc_["ordenes"][0]}}
    res["ranking_con_region_conservada"] = rk

    out = Path(a.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=lambda o: o.item()
                              if hasattr(o, "item") else str(o)), encoding="utf-8")
    print("escrito", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
