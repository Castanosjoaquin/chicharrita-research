"""Control de D59 sobre los SEIS genes: todo conteo de coincidencia, en dos cifras.

D59 (linea `sifi_plus/`) obliga a informar cada conteo de off-target como total y
cuanto de ese total es de baja complejidad, y a releer con ese descuento los tamizajes
ya corridos. El criterio es el de `sifi_plus/complejidad.py` (`es_baja`): homopolimero
de 10 nt o mas, o 2 nucleotidos distintos o menos en la ventana. Es un criterio nuestro
`[H]`, pendiente de contrastar contra `dustmasker`.

M7 ya lo habia medido en `BicC_Dm` y dio cero. En los otros cinco genes no estaba
medido, y una cola de poli-A en un gen del insecto inflaria justo la referencia que mas
pesa en la discusion de M5. Esto lo mide en los seis.

Las secuencias salen de `work/sifi_v2/offtarget_k21/offtarget_por_sirna.tsv`, que no se
versiona porque tiene la columna `sirna` de genes de EPILAB. La salida son conteos.

    python research/ola4/M5_dos_ejes/scripts/complejidad_seis_genes.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))

from sifi_plus.complejidad import BASES_MIN, HOMOPOLIMERO_MAX, bases_distintas, es_baja, \
    homopolimero  # noqa: E402
import ranking as R      # noqa: E402
import ranking_v2 as V   # noqa: E402

TRABAJO = RAIZ / "work" / "sifi_v2"
SALIDA = RAIZ / "research/ola4/M5_dos_ejes/resultados"
CRITERIOS = ("perfecto_21", "perfecto_ge19", "mm1_21")


def leer(ruta: Path) -> tuple[list[dict], list[str]]:
    with ruta.open(encoding="utf-8") as fh:
        r = csv.DictReader(fh, delimiter="\t")
        filas = list(r)
        cols = [c for c in (r.fieldnames or []) if "|" in c]
    return filas, cols


def main() -> int:
    V.con_panel(sin_humano=False)
    filas, cols = leer(TRABAJO / "offtarget_k21" / "offtarget_por_sirna.tsv")
    dm, cols_dm = leer(TRABAJO / "offtarget_dm_k21" / "offtarget_por_sirna.tsv")
    por_gen: dict[str, dict] = {}
    for f in filas + dm:
        gen = f["consulta"].replace("_full", "")
        por_gen.setdefault(gen, {})[int(f["pos"])] = f

    # Que referencias entran a cada gen (el vector es on-target para los del insecto)
    por_cand = {c["gen"]: c for c in list(R.CANDIDATOS) + V.NUEVOS}

    salida, resumen = [], {}
    for gen in V.GENES_EPILAB + V.GENES_NUEVOS:
        excl = R.excluidas_de(por_cand[gen], "off")
        celdas = por_gen[gen]
        seqs = {p: f["sirna"] for p, f in celdas.items()}
        bajas = {p for p, s in seqs.items() if es_baja(s)}
        homo = max(homopolimero(s) for s in seqs.values())
        bmin = min(bases_distintas(s) for s in seqs.values())
        resumen[gen] = {"ventanas": len(seqs), "baja_complejidad": len(bajas),
                        "homopolimero_max": homo, "bases_distintas_min": bmin,
                        "umbral_homopolimero": HOMOPOLIMERO_MAX, "umbral_bases": BASES_MIN}
        salida.append({"gen": gen, "referencia": "(todas las ventanas del gen)",
                       "criterio": "-", "total": len(seqs), "baja_complejidad": len(bajas),
                       "homopolimero_max": homo, "bases_distintas_min": bmin})
        for col in sorted(set(cols) | set(cols_dm)):
            ref, crit = col.split("|")
            if ref in excl:
                continue
            pos = [p for p, f in celdas.items() if int(f.get(col) or 0) > 0]
            if not pos:
                continue
            nb = sum(1 for p in pos if p in bajas)
            salida.append({"gen": gen, "referencia": R.corto(ref), "criterio": crit,
                           "total": len(pos), "baja_complejidad": nb,
                           "homopolimero_max": max(homopolimero(seqs[p]) for p in pos),
                           "bases_distintas_min": min(bases_distintas(seqs[p]) for p in pos)})

    SALIDA.mkdir(parents=True, exist_ok=True)
    with (SALIDA / "complejidad_seis_genes.tsv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(salida[0]), delimiter="\t")
        w.writeheader()
        w.writerows(salida)
    (SALIDA / "complejidad_seis_genes.json").write_text(json.dumps(
        {"criterio": "sifi_plus/complejidad.py: homopolimero >= %d o bases distintas <= %d"
                     % (HOMOPOLIMERO_MAX, BASES_MIN),
         "fuente": "work/sifi_v2/offtarget_k21 y offtarget_dm_k21 (insumos locales)",
         "por_gen": resumen,
         "conteos_con_coincidencia": [f for f in salida if f["criterio"] != "-"]},
        indent=1, ensure_ascii=False), encoding="utf-8")

    print("%-12s%10s%10s%8s%8s" % ("gen", "ventanas", "baja", "homop.", "bases"))
    for gen, d in resumen.items():
        print("%-12s%10d%10d%8d%8d" % (gen, d["ventanas"], d["baja_complejidad"],
                                       d["homopolimero_max"], d["bases_distintas_min"]))
    con = [f for f in salida if f["criterio"] != "-"]
    print("\nconteos con coincidencia: %d filas, %d ventanas en total, %d de baja complejidad"
          % (len(con), sum(f["total"] for f in con), sum(f["baja_complejidad"] for f in con)))
    print("escrito en %s" % (SALIDA / "complejidad_seis_genes.tsv").relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
