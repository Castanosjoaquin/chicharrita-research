"""Que colapsa el normalizador de F1, sobre los mismos pares reciprocos de C12 (pregunta 62).

Salida declarada en el informe, no en el preregistro: cuantifica POR QUE el normalizador mueve
siete puntos, separando los pares que pasan de desacuerdo a acuerdo segun el patron que los
separaba. Sin normalizar = comparar los productos de RefSeq en minuscula y nada mas.

Uso, desde la raiz del repositorio:
    python research/ola6/R13_brecha_c12/scripts/patrones_normalizador.py [ruta/a/work/C12]
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path("research/ola6/F1_transferencia_homologia/scripts")))
sys.path.insert(0, str(Path("research/ola6/R13_brecha_c12/scripts")))
import descomponer as D  # noqa: E402
import transferir_anotacion as F1  # noqa: E402

SALIDA = Path("research/ola6/R13_brecha_c12/resultados")
MAX_EJEMPLOS = 8


def patron(a: str, b: str) -> str:
    la, lb = a.lower(), b.lower()
    if "isoform" in la or "isoform" in lb:
        return "sufijo de isoforma (isoform Xn)"
    if "-like" in la or "-like" in lb:
        return "sufijo -like"
    if "homolog" in la or "homolog" in lb:
        return "sufijo homolog"
    return "otro"


def main() -> None:
    w = Path(sys.argv[1] if len(sys.argv) > 1 else "work/C12")
    prod_mq = D.productos(Path("work/C11_diseno_nuevo/blast/mq_proteome.faa"))
    prod_hv = D.productos(Path("work/F1v/ref/GCF_021130785.1_UT_GWSS_2.1_protein.faa"))
    bf = D.mejores_blast(w / "MQ_vs_HV.tsv")
    br = D.mejores_blast(w / "HVsub_vs_MQ.tsv")
    muestra = [l.strip() for l in open(w / "muestra_mq.txt") if l.strip()]

    n = crudo = norm = 0
    recuperados: list[tuple[str, str]] = []
    perdidos: list[tuple[str, str]] = []
    for q in muestra:
        h = bf.get(q)
        if not h:
            continue
        s = h[0]
        inv = br.get(s)
        if not inv or inv[0] != q:
            continue
        nq, ns = prod_mq.get(q, ""), prod_hv.get(s, "")
        if not (F1.es_informativo(nq) and F1.es_informativo(ns)):
            continue
        n += 1
        c = nq.lower() == ns.lower()
        v = F1.normalizar_nombre(nq) == F1.normalizar_nombre(ns)
        crudo += c
        norm += v
        if v and not c:
            recuperados.append((nq, ns))
        if c and not v:
            perdidos.append((nq, ns))

    por_patron = collections.Counter(patron(a, b) for a, b in recuperados)
    out = dict(
        pares_reciprocos_con_nombre=n,
        acuerdos_sin_normalizar=crudo,
        acuerdos_con_normalizador_F1=norm,
        concordancia_sin_normalizar=round(crudo / n, 4),
        concordancia_con_normalizador_F1=round(norm / n, 4),
        pares_que_el_normalizador_convierte_en_acuerdo=len(recuperados),
        pares_que_el_normalizador_rompe=len(perdidos),
        por_patron={k: dict(n=v, pct=round(100 * v / len(recuperados), 1))
                    for k, v in por_patron.most_common()},
        ejemplos={k: [f"{a}  ||  {b}" for a, b in recuperados if patron(a, b) == k][:MAX_EJEMPLOS]
                  for k in por_patron})
    (SALIDA / "patrones_normalizador.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in out.items() if k != "ejemplos"}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
