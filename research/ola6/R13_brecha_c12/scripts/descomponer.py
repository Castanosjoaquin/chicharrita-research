"""De donde sale la brecha entre el 78,2 % de C12 y el 85,1 % del par completo (pregunta 62).

Tres pasos, cada uno cambiando UNA sola cosa (ver ../PREREGISTRO.md):

  A  pares de C12 (BLAST+, su protocolo) + normalizador de F1
  B  alineamientos de diamond de D86 + recorte de C12 (sus 4.000 consultas) + normalizador de F1
  C  A contra B, que con protocolo y normalizador fijos deja solo el alineador

Insumos que ya estan en disco; no corre ningun alineamiento nuevo.

Uso, desde la raiz del repositorio:
    python research/ola6/R13_brecha_c12/scripts/descomponer.py [ruta/a/work/C12]
"""
from __future__ import annotations

import collections
import csv
import gzip
import json
import math
import sys
from pathlib import Path

F1DIR = Path("research/ola6/F1_transferencia_homologia")
sys.path.insert(0, str(F1DIR / "scripts"))
import transferir_anotacion as F1  # noqa: E402

SALIDA = Path("research/ola6/R13_brecha_c12/resultados")
VALID = F1DIR / "validacion_bandas/resultados"
BANDAS = ["<40", "40-60", "60-80", "80-90", ">=90"]
C12_PUBLICADO = {"<40": 0.250, "40-60": 0.761, "60-80": 0.768, "80-90": 0.786, ">=90": 0.862}
C12_TOTAL, C12_PARES = 0.782, 1152


def wilson(a: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    z, p = 1.959963984540054, a / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    s = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - s), min(1.0, c + s))


def productos(faa: Path) -> dict[str, str]:
    out = {}
    with open(faa) as fh:
        for l in fh:
            if l.startswith(">"):
                out[l[1:].split()[0]] = F1.producto_refseq(l.strip())
    return out


def mejores_blast(tsv: Path, ncols: int = 9) -> dict[str, tuple[str, float]]:
    """Mejor hit por consulta (bitscore), formato de C12: ... evalue bitscore qcovs."""
    best: dict[str, tuple[str, float, float]] = {}
    with open(tsv) as fh:
        for l in fh:
            f = l.rstrip("\n").split("\t")
            if len(f) != ncols:
                continue
            q, s, pid, bits = f[0], f[1], float(f[2]), float(f[7])
            if q not in best or bits > best[q][1]:
                best[q] = (s, bits, pid)
    return best


def concordancia(pares: list[tuple[str, str, float]]) -> dict:
    """pares = (nombre verdadero, nombre transferido, pident), ya normalizados."""
    out = {}
    for b in BANDAS:
        sel = [p for p in pares if F1.banda(p[2])[0] == b]
        a = sum(1 for p in sel if p[0] == p[1])
        lo, hi = wilson(a, len(sel))
        out[b] = dict(n=len(sel), aciertos=a,
                      conc=round(a / len(sel), 4) if sel else None,
                      lo=round(lo, 4) if sel else None, hi=round(hi, 4) if sel else None)
    a, n = sum(1 for p in pares if p[0] == p[1]), len(pares)
    out["total"] = dict(n=n, aciertos=a, conc=round(a / n, 4) if n else None, lo=None, hi=None)
    return out


def armar_pares(best_f, best_r, prod_q, prod_s, consultas) -> list:
    """Reciproco = el mejor hit del mejor hit vuelve a la consulta. Nombre informativo en ambos."""
    pares = []
    for q in consultas:
        h = best_f.get(q)
        if not h:
            continue
        s = h[0]
        inv = best_r.get(s)
        if not inv or inv[0] != q:
            continue
        nq, ns = prod_q.get(q, ""), prod_s.get(s, "")
        if not (F1.es_informativo(nq) and F1.es_informativo(ns)):
            continue
        pares.append((F1.normalizar_nombre(nq), F1.normalizar_nombre(ns), h[2]))
    return pares


def paso_A(workc12: Path, prod_mq, prod_hv):
    """Pares de C12 con su propio BLAST+ y su protocolo; normalizador de F1."""
    bf = mejores_blast(workc12 / "MQ_vs_HV.tsv")
    br = mejores_blast(workc12 / "HVsub_vs_MQ.tsv")
    muestra = [l.strip() for l in open(workc12 / "muestra_mq.txt") if l.strip()]
    return armar_pares(bf, br, prod_mq, prod_hv, muestra), len(muestra)


DIAMOND_DIR = Path("work/F1v/trabajo")


def paso_B(prod_mq, prod_hv, muestra):
    """diamond crudo, recortado a las mismas consultas de C12.

    Lee los TSV de diamond con la MISMA funcion y la MISMA regla de reciprocidad que el paso A
    (mejor hit del mejor hit, sin el tratamiento de empates de F1): entre A y B cambia el
    alineador y nada mas. Usar la tabla ya clasificada de F1 confundiria el alineador con su
    regla de empates (Enmienda 1 del preregistro).
    """
    bf = mejores_blast(DIAMOND_DIR / "MQprot_a_HV.tsv", ncols=10)
    br = mejores_blast(DIAMOND_DIR / "HV_a_MQprot.tsv", ncols=10)
    return armar_pares(bf, br, prod_mq, prod_hv, muestra)


def paso_C(prod_mq, prod_hv):
    """diamond crudo, par completo: misma regla que A y B, sin el recorte de C12."""
    bf = mejores_blast(DIAMOND_DIR / "MQprot_a_HV.tsv", ncols=10)
    br = mejores_blast(DIAMOND_DIR / "HV_a_MQprot.tsv", ncols=10)
    return armar_pares(bf, br, prod_mq, prod_hv, list(prod_mq))


def main() -> None:
    workc12 = Path(sys.argv[1] if len(sys.argv) > 1 else "work/C12")
    SALIDA.mkdir(parents=True, exist_ok=True)
    prod_mq = productos(Path("work/C11_diseno_nuevo/blast/mq_proteome.faa"))
    prod_hv = productos(Path("work/F1v/ref/GCF_021130785.1_UT_GWSS_2.1_protein.faa"))

    pA, n_muestra = paso_A(workc12, prod_mq, prod_hv)
    muestra = [l.strip() for l in open(workc12 / "muestra_mq.txt") if l.strip()]
    pB = paso_B(prod_mq, prod_hv, muestra)
    cA, cB = concordancia(pA), concordancia(pB)

    pC = paso_C(prod_mq, prod_hv)
    cComp = concordancia(pC)

    tA, tB, tC = cA["total"]["conc"], cB["total"]["conc"], cComp["total"]["conc"]
    brecha = tC - C12_TOTAL
    sum_norm = tA - C12_TOTAL          # mismo protocolo y alineador, cambia el normalizador
    sum_alin = tB - tA                 # mismo protocolo y normalizador, cambia el alineador
    sum_prot = tC - tB                 # mismo alineador y normalizador, cambia el protocolo

    pesos = {"normalizador": sum_norm, "alineador": sum_alin, "protocolo": sum_prot}
    dom = max(pesos, key=lambda k: abs(pesos[k]))
    veredicto = (f"{dom} explica {abs(pesos[dom]) / abs(brecha):.0%} de la brecha"
                 if abs(pesos[dom]) >= 2 / 3 * abs(brecha) else
                 "multicausal: ningun componente llega a 2/3 de la brecha")

    repl = len(pA)
    control = ("replica fiel" if abs(repl - C12_PARES) <= 0.10 * C12_PARES
               else f"NO reproduce el n de C12 ({repl} contra {C12_PARES}): el paso A es "
                    "reconstruccion aproximada, no replica")

    out = dict(
        pregunta="62: de donde sale la brecha entre el 78,2 % de C12 y el 85,1 % del par completo",
        preregistro="research/ola6/R13_brecha_c12/PREREGISTRO.md",
        C12_publicado=dict(total=C12_TOTAL, pares=C12_PARES, por_banda=C12_PUBLICADO),
        consultas_de_la_submuestra=n_muestra,
        paso_A_blastp_protocoloC12_normF1=dict(total=tA, pares=cA["total"]["n"], por_banda=cA),
        paso_B_diamond_protocoloC12_normF1=dict(total=tB, pares=cB["total"]["n"], por_banda=cB),
        paso_C_diamond_completo_normF1=dict(total=tC, pares=cComp["total"]["n"], por_banda=cComp),
        brecha_total=round(brecha, 4),
        sumandos={k: round(v, 4) for k, v in pesos.items()},
        control_de_replica=control,
        veredicto=veredicto)
    (SALIDA / "descomposicion.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))

    with open(SALIDA / "bandas_por_paso.tsv", "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["paso", "banda", "n", "aciertos", "concordancia", "ic95_lo", "ic95_hi",
                    "c12_publicado"])
        for et, c in (("A_blastp_protoC12", cA), ("B_diamond_protoC12", cB),
                      ("C_diamond_completo", cComp)):
            for b in BANDAS + ["total"]:
                d = c[b]
                w.writerow([et, b, d["n"], d["aciertos"], d["conc"], d["lo"], d["hi"],
                            C12_PUBLICADO.get(b, C12_TOTAL)])

    print(f"C12 publicado   {C12_TOTAL:.4f}  ({C12_PARES} pares)")
    print(f"A blastp+protoC12+normF1  {tA:.4f}  ({cA['total']['n']} pares)   -> {control}")
    print(f"B diamond+protoC12+normF1 {tB:.4f}  ({cB['total']['n']} pares)")
    print(f"C diamond completo        {tC:.4f}  ({cComp['total']['n']} pares)")
    print(f"\nbrecha {brecha:+.4f} = normalizador {sum_norm:+.4f} + alineador {sum_alin:+.4f} "
          f"+ protocolo {sum_prot:+.4f}")
    print("VEREDICTO:", veredicto)


if __name__ == "__main__":
    main()
