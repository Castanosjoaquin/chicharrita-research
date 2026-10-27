"""Recalcula el esperado de concordancia de F1 con las bandas medidas, no con las de C12.

Insumo: la tabla real de F1 sobre GITV01 (distribucion por banda y por cobertura de los 10.280
ORF reciprocos con nombre de la lectura inclusiva) y las concordancias del brazo O medidas por
validar_bandas.py. Tres cifras:

  1. con las bandas de C12          -> reproduce el 81 % que publica F1
  2. con las bandas del brazo O     -> preregistrado ("recalcular el esperado con las bandas de O")
  3. reponderado banda x cobertura  -> POST HOC, Enmienda 1 del PREREGISTRO: corrige que GITV01
     tiene mas ORF parciales y fragmentos que el brazo O

Uso, desde la raiz del repositorio:
    python research/ola6/F1_transferencia_homologia/validacion_bandas/scripts/recalcular_esperado.py
"""
from __future__ import annotations

import collections
import csv
import gzip
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import transferir_anotacion as F1  # noqa: E402

BASE = Path("research/ola6/F1_transferencia_homologia")
SALIDA = BASE / "validacion_bandas/resultados"
MIN_CELDA = 20  # una celda banda x cobertura con menos pares no se usa para reponderar
BANDAS = ["<40", "40-60", "60-80", "80-90", ">=90"]


def conc_brazo_O():
    """Concordancia del brazo O por banda, por cobertura y por banda x cobertura."""
    tab: dict = collections.defaultdict(lambda: [0, 0])
    with gzip.open(SALIDA / "pares_O_ampliada.tsv.gz", "rt") as fh:
        for p in csv.DictReader(fh, delimiter="\t"):
            a = int(p["acierta"])
            for k in (p["banda"], ("cob", p["cobertura"]), (p["banda"], p["cobertura"])):
                tab[k][0] += a
                tab[k][1] += 1
    return tab


def distribucion_gitv01():
    """Los ORF reciprocos con nombre de la lectura inclusiva, por banda y por cobertura."""
    banda: dict = collections.Counter()
    celda: dict = collections.Counter()
    cob: dict = collections.Counter()
    with gzip.open(BASE / "resultados/transferencia_MQ.tsv.gz", "rt") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["categoria_ampliada"] != "f_reciproco_con_nombre":
                continue
            c = F1.rotulo_cobertura(float(r["ampliada_cob_orf"]), float(r["ampliada_cob_ref"]))
            b = r["ampliada_banda_identidad"]
            banda[b] += 1
            cob[c] += 1
            celda[(b, c)] += 1
    return banda, cob, celda


def main() -> None:
    tab = conc_brazo_O()
    banda, cob, celda = distribucion_gitv01()
    n = sum(banda.values())
    c12 = {b: c for _, b, c, _, _, _ in F1.BANDAS_C12}

    esp_c12 = sum(banda[b] * c12[b] for b in banda) / n
    esp_O = sum(banda[b] * tab[b][0] / tab[b][1] for b in banda) / n
    num = den = 0.0
    for (b, c), k in celda.items():
        v = tab[(b, c)]
        if v[1] >= MIN_CELDA:
            num += k * v[0] / v[1]
            den += k
    esp_rep = num / den

    out = dict(
        n_orfs=n,
        esperado_con_bandas_C12=round(esp_c12, 4),
        esperado_con_bandas_brazo_O=round(esp_O, 4),
        esperado_reponderado_por_cobertura=round(esp_rep, 4),
        cobertura_cubierta_por_el_reponderado=f"{den:.0f}/{n}",
        concordancia_brazo_O=dict(
            por_banda={b: dict(conc=round(tab[b][0] / tab[b][1], 4), n=tab[b][1]) for b in BANDAS},
            por_cobertura={c: dict(conc=round(tab[("cob", c)][0] / tab[("cob", c)][1], 4),
                                   n=tab[("cob", c)][1])
                           for c in ("cobertura_alta", "parcial", "fragmento")}),
        distribucion_GITV01=dict(por_banda=dict(banda), por_cobertura=dict(cob)),
        nota=("La cifra que F1 publica es la primera. El preregistro de esta validacion fija que "
              "no se corrige nada hacia arriba, asi que las otras dos se reportan como medicion "
              "y no reemplazan al 81 % del informe de F1."))
    (SALIDA / "esperado_recalculado.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in out.items() if k.startswith("esperado") or k == "n_orfs"},
                     indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
