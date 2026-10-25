"""N10 - La funcion historica de conteo aplicada a regiones, no a genes completos.

La pregunta que abre el hallazgo de N1 y que nadie habia medido. N1 midio que la funcion
historica esconde entre el 5,7 % y el 17,4 % de las ventanas eficientes **de un gen completo**,
segun el gen. Pero las cifras que se comparan para elegir una region candidata son conteos de
region, no de gen. Si la planilla del laboratorio construyo esos conteos con el mismo contador,
entonces nuestro conteo directo y el suyo no son el mismo numero **y el orden entre candidatas
podria no ser el mismo tampoco**. Eso es lo que se mide aca.

Tres conteos por region y por marco, y el script no elige entre ellos. Es la misma decision de
diseno que tomo M1 con las tres agregaciones de la tabla del original: cuando no se sabe cual
es la regla que uso el laboratorio, se reportan las lecturas posibles en paralelo y ninguna se
declara la verdadera.

  directo           la cantidad de ventanas eficientes. Es lo que publicamos hoy.
  historico_region  los incrementos positivos tomando la region como universo: una ventana
                    eficiente en `p` no se cuenta si la de `p - 20` tambien es eficiente **y
                    cae dentro de la region**. Es la lectura si la curva se construye sobre el
                    fragmento.
  historico_gen     los incrementos positivos de la curva del **gen completo**, contando solo
                    los que caen dentro de la region: una ventana en el borde izquierdo puede
                    quedar tapada por una vecina que esta afuera de la region. Es la lectura si
                    la curva se construye sobre el gen y despues se lee un tramo.

Para el marco de la molecula recortada `historico_gen` no existe: la molecula es el universo,
no hay afuera, asi que las dos lecturas coinciden y se informa una sola.

Configuracion: punto por defecto, modo `corregido` --el del ranking--, ViennaRNA 2.7.2, tabla
`RNA_NN3`. Las mismas seis regiones y las mismas anclas que N3.

Uso (desde la raiz del repositorio):
    python research/ola5/N10_conteo_historico_por_region/scripts/conteo_region.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
SALIDA = AQUI.parents[1] / "resultados"
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))
sys.path.insert(0, str(RAIZ / "research" / "ola5" / "N1_regla_de_conteo" / "scripts"))
sys.path.insert(0, str(RAIZ / "research" / "ola5" / "N3_marcos" / "scripts"))

from conteo_por_curva import ANCHO_HISTORICO as A  # noqa: E402
from conteo_por_curva import contar_por_incrementos  # noqa: E402
from tres_marcos import (ANCLA_MARCO1, ANCLA_TRES, GENES, REGIONES,  # noqa: E402
                         FASTA, eficientes, leer_fasta)

K = 21
#: Las tres regiones de `BicC_Dm` que compara el eje 1 de M7, en orden de preferencia actual.
COMPARACION = [("BicC_Dm", 922), ("BicC_Dm", 2121), ("BicC_Dm", 264)]


def tapadas_en(s: set[int], universo: set[int]) -> list[int]:
    """Los arranques de `s` que quedan tapados por un vecino a 20 posiciones de `universo`."""
    return sorted(p for p in s if p - A in universo)


def main() -> int:
    faltan = [g for g in GENES if not FASTA[g].exists()]
    if faltan:
        raise SystemExit("faltan los FASTA de %s en work/sifi_check/; `work/` no esta en git"
                         % ", ".join(faltan))

    en_gen = {g: eficientes(leer_fasta(FASTA[g])) for g in GENES}

    filas, roto = [], []
    for gen, ini, fin, nota in REGIONES:
        seq = leer_fasta(FASTA[gen])
        molecula = seq[ini - 1:fin]
        gen_efic = en_gen[gen]
        ult = fin - (K - 1)

        m1 = {p for p in gen_efic if ini <= p <= fin}
        m2 = {p for p in gen_efic if ini <= p <= ult}
        mol = eficientes(molecula)
        m3 = {ini + q - 1 for q in mol}

        if ANCLA_MARCO1.get((gen, ini)) not in (None, len(m1)):
            roto.append("%s %d-%d marco 1: %d, publicado %d"
                        % (gen, ini, fin, len(m1), ANCLA_MARCO1[(gen, ini)]))
        if (gen, ini) in ANCLA_TRES:
            esp = ANCLA_TRES[(gen, ini)]
            if (len(m1), len(m2), len(m3)) != esp:
                roto.append("%s %d-%d tres marcos: %s, publicado %s"
                            % (gen, ini, fin, (len(m1), len(m2), len(m3)), esp))

        fila = {"gen": gen, "inicio": ini, "fin": fin, "nota": nota, "marcos": {}}
        for nombre, s, universo in (("contexto_todos", m1, gen_efic),
                                    ("contexto_comparables", m2, gen_efic),
                                    ("molecula", m3, m3)):
            d = {
                "directo": len(s),
                "historico_region": contar_por_incrementos(s, A),
                "tapadas_region": len(tapadas_en(s, s)),
            }
            if nombre != "molecula":
                # La curva del gen completo: el vecino tapante puede estar afuera.
                d["historico_gen"] = sum(1 for p in s if p - A not in universo)
                d["tapadas_gen"] = len(tapadas_en(s, universo))
                d["tapadas_por_un_vecino_de_afuera"] = d["tapadas_gen"] - d["tapadas_region"]
            fila["marcos"][nombre] = d
        filas.append(fila)

    if roto:
        raise SystemExit("anclas rotas:\n  " + "\n  ".join(roto))

    por_clave = {(f["gen"], f["inicio"]): f for f in filas}
    ordenes = {}
    for marco in ("contexto_todos", "contexto_comparables", "molecula"):
        for lectura in ("directo", "historico_region", "historico_gen"):
            vals = []
            for clave in COMPARACION:
                d = por_clave[clave]["marcos"][marco]
                if lectura not in d:
                    vals = None
                    break
                vals.append((clave[1], d[lectura]))
            if vals is None:
                continue
            orden = [p for p, _ in sorted(vals, key=lambda x: -x[1])]
            ordenes["%s/%s" % (marco, lectura)] = {
                "valores": dict(vals), "orden": orden,
                "gana_922_a_2121": dict(vals)[922] > dict(vals)[2121],
                "empate_922_2121": dict(vals)[922] == dict(vals)[2121],
            }

    SALIDA.mkdir(parents=True, exist_ok=True)
    cols = ["gen", "region", "marco", "directo", "historico_region", "historico_gen",
            "tapadas_region", "tapadas_de_afuera"]
    lineas = ["\t".join(cols)]
    for f in filas:
        for marco, d in f["marcos"].items():
            lineas.append("\t".join([
                f["gen"], "%d-%d" % (f["inicio"], f["fin"]), marco,
                str(d["directo"]), str(d["historico_region"]),
                str(d.get("historico_gen", "-")), str(d["tapadas_region"]),
                str(d.get("tapadas_por_un_vecino_de_afuera", "-"))]))
    (SALIDA / "conteo_region.tsv").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    (SALIDA / "conteo_region.json").write_text(
        json.dumps({"ancho": A, "configuracion": {"modo": "corregido", "backend": "vienna",
                                                  "tabla_nn": "NN3"},
                    "filas": filas, "ordenes": ordenes}, indent=2, ensure_ascii=False),
        encoding="utf-8")

    print("%-12s %-10s %-22s %7s %9s %9s" % ("gen", "region", "marco", "directo",
                                             "hist_reg", "hist_gen"))
    for f in filas:
        for marco, d in f["marcos"].items():
            print("%-12s %-10s %-22s %7d %9d %9s"
                  % (f["gen"], "%d-%d" % (f["inicio"], f["fin"]), marco,
                     d["directo"], d["historico_region"],
                     d.get("historico_gen", "-")))
    print("\nLas tres regiones de BicC_Dm, por lectura:")
    for k, v in ordenes.items():
        print("  %-38s %s  -> orden %s%s"
              % (k, v["valores"], v["orden"],
                 "  (EMPATE 922 vs 2121)" if v["empate_922_2121"] else ""))
    cambia = {k for k, v in ordenes.items() if not v["gana_922_a_2121"]}
    print("\nlecturas en las que 922-1221 NO le gana a 2121-2420: %s"
          % (sorted(cambia) if cambia else "ninguna"))
    print("resultados en %s" % SALIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
