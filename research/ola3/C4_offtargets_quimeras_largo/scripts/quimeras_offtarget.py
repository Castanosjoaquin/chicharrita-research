"""Cuántos off-targets aportan las ventanas de empalme de una quimera.

Q3, segunda mitad. Lee la salida cruda de `tools/sifi21_port/offtarget_21nt.py`
corrido (sin modificarlo) sobre las 12 quimeras y las 4 regiones sueltas contra las
seis referencias de W5, y separa, por quimera y por base de datos, los aciertos que
vienen de ventanas heredadas de los aciertos que vienen de las 20 ventanas nuevas
del empalme.

Para los genes del propio blanco, el genoma de *Dalbulus maidis* es ON-target y se
marca como tal en la salida en vez de descontarse en silencio.

Uso:
    python research/ola3/C4_offtargets_quimeras_largo/scripts/quimeras_offtarget.py
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
RESULTADOS = Path(__file__).resolve().parents[1] / "resultados"
TSV = RAIZ / "work/C4/offtarget/quimeras/offtarget_por_sirna.tsv"
META = RESULTADOS / "quimeras_meta_fiel_vienna.json"
CRITERIOS = ("perfecto_21", "perfecto_ge19")
VENTANA = 21
ONTARGET = "GCA_975739785.1_ihDalMaid1.1_genomic"


def main():
    meta = json.loads(META.read_text(encoding="utf-8"))
    largos = meta["regiones"]
    filas = list(csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"))
    bases = sorted({c.split("|")[0] for c in filas[0] if "|" in c})
    print("bases:", ", ".join(bases))

    out = []
    for consulta in sorted({f["consulta"] for f in filas}):
        if not consulta.startswith("Q_"):
            continue
        izq, der = consulta[2:].split("__")
        corte = largos[izq]
        sub = [f for f in filas if f["consulta"] == consulta]
        for base in bases:
            for crit in CRITERIOS:
                col = "%s|%s" % (base, crit)
                emp = [f for f in sub if corte - VENTANA + 1 < int(f["pos"]) <= corte
                       and int(f[col] or 0)]
                her = [f for f in sub if not (corte - VENTANA + 1 < int(f["pos"]) <= corte)
                       and int(f[col] or 0)]
                if emp or her:
                    out.append({"quimera": consulta, "izquierda": izq, "derecha": der,
                                "base": base, "criterio": crit,
                                "es_on_target_del_blanco":
                                    base == ONTARGET and (izq.endswith("_Dm") or der.endswith("_Dm")),
                                "aciertos_heredados": len(her),
                                "aciertos_de_empalme": len(emp),
                                "pos_empalme": ",".join(f["pos"] for f in emp)})

    with open(RESULTADOS / "q3_offtarget_empalmes.tsv", "w", encoding="utf-8",
              newline="") as fh:
        if out:
            w = csv.DictWriter(fh, fieldnames=list(out[0].keys()), delimiter="\t")
            w.writeheader(); w.writerows(out)
        else:
            fh.write("sin_aciertos\n")

    print("\n%-24s %-42s %-14s %8s %8s" % ("quimera", "base", "criterio", "hered.", "empalme"))
    for o in out:
        print("%-24s %-42s %-14s %8d %8d%s" % (
            o["quimera"], o["base"][:42], o["criterio"], o["aciertos_heredados"],
            o["aciertos_de_empalme"], "  (ON-target)" if o["es_on_target_del_blanco"] else ""))

    tot_emp = sum(o["aciertos_de_empalme"] for o in out
                  if not o["es_on_target_del_blanco"])
    tot_emp_on = sum(o["aciertos_de_empalme"] for o in out
                     if o["es_on_target_del_blanco"])
    print("\nventanas de empalme examinadas: 12 quimeras x 20 = 240")
    print("aciertos de empalme en bases NO objetivo: %d" % tot_emp)
    print("aciertos de empalme en el genoma del blanco (on-target): %d" % tot_emp_on)
    (RESULTADOS / "q3_offtarget_resumen.json").write_text(json.dumps(
        {"ventanas_de_empalme_examinadas": 240,
         "aciertos_de_empalme_no_objetivo": tot_emp,
         "aciertos_de_empalme_on_target": tot_emp_on,
         "bases": bases, "criterios": list(CRITERIOS)},
        indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nescrito en %s" % RESULTADOS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
