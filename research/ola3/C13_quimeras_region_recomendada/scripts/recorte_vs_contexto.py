"""La region recomendada evaluada dentro del gen contra la misma region recortada.

Por que hace falta este control antes de mirar una sola quimera. Las cifras que el
entregable publica para las regiones recomendadas (C7 nivel 3: 38, 21, 35 y 21
ventanas eficientes) se calcularon **sobre el perfil del gen completo**, contando las
ventanas cuya posicion de inicio cae en la region. La molecula que se sintetizaria es
el recorte, y en el recorte dos cosas cambian:

  1. Desaparecen las ultimas 20 posiciones de inicio. Una region de 200 nt tiene 200
     posiciones de inicio dentro del gen, porque las ventanas que arrancan al final se
     completan con el nucleotido de al lado; recortada, tiene 180 ventanas de 21 nt.
  2. Las ventanas que quedan cerca de los dos bordes pierden el contexto de plegado.
     si-Fi21 calcula la accesibilidad con RNAplfold y ventana de plegado de 80 nt, asi
     que el veredicto de una ventana puede cambiar hasta ~59 nt del borde.

C4 anticipo el punto 2 como hipotesis al medir las quimeras («la evaluacion de una
region elegida sobre el perfil del gen completo hereda el mismo sesgo de borde»,
`research/ola3/C4_offtargets_quimeras_largo/quimeras.md` seccion 3) y no lo midio.
Esto lo mide, y separa cuanto de la diferencia es el punto 1 y cuanto el punto 2.

Dos anclas antes de medir: el conteo de eficientes del gen completo tiene que dar los
cuatro numeros que `tools/sifi21_port/ranking_v2.py` fija como ancla de W7 (123, 30,
171, 29) y el conteo en contexto de cada region recomendada tiene que dar los cuatro
de C7 nivel 3 (38, 21, 35, 21). Si alguna falla, aborta.

**Las anclas son del modo `corregido`**, y eso no es un detalle. El ranking de W7 y de
C7 se construyo con los perfiles `<gen>_full_corregido_vienna.tsv`
(`tools/sifi21_port/ranking.py` linea 118), mientras que las quimeras de C4 se
midieron en modo `fiel`, el que reproduce al programa original. Los dos modos no dan
el mismo conteo: en modo `fiel` el gen `MP_MRFV` tiene 142 ventanas eficientes y no
123. Por eso el control se corre en `corregido` cuando el punto de comparacion es el
ranking, y las anclas solo se verifican en ese modo.

Uso:
    python research/ola3/C13_quimeras_region_recomendada/scripts/recorte_vs_contexto.py \
        --modo corregido
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
BLOQUE = Path(__file__).resolve().parents[1]
RESULTADOS = BLOQUE / "resultados"
TRABAJO = RAIZ / "work/C13"
FULL = RAIZ / "work/sifi_check"
VENTANA = 21

sys.path.insert(0, str(Path(__file__).resolve().parent))
import quimeras_v2 as QV  # noqa: E402

ANCLA_GEN = {"MP_MRFV": 123, "CP_MRFV": 30, "BicC_Dm": 171, "ATPaseD_Dm": 29}
# Eficientes de cada region contada DENTRO del gen, que es como las publicaron C7
# (nivel 3) y, para `BicC_Dm` 922-1221, D25 con los datos de C8 (36 eficientes).
ANCLA_REGION = {
    "recomendadas": {"MP_MRFV": 38, "CP_MRFV": 21, "BicC_Dm": 35, "ATPaseD_Dm": 21},
    "vigentes": {"MP_MRFV": 38, "CP_MRFV": 21, "BicC_Dm": 36, "ATPaseD_Dm": 21},
}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--conjunto", choices=("recomendadas", "vigentes"),
                    default="vigentes")
    ap.add_argument("--modo", choices=("fiel", "corregido"), default="corregido")
    ap.add_argument("--backend", choices=("exe", "vienna"), default="vienna")
    a = ap.parse_args(argv)
    suf = "%s_%s" % (a.modo, a.backend)
    sufc = "%s_%s_%s" % (a.conjunto, a.modo, a.backend)
    ancla_region = ANCLA_REGION[a.conjunto]
    # Las anclas publicadas son del modo del ranking; en `fiel` se mide igual pero no
    # se verifica contra ellas, porque los dos modos no dan el mismo conteo.
    anclar = a.modo == "corregido"
    if not anclar:
        print("AVISO: modo %s; las anclas de W7 y C7 son del modo corregido y no se "
              "verifican en esta corrida" % a.modo)

    dir_sifi = TRABAJO / "sifi" / ("genes_completos_%s" % suf)
    dir_sifi.mkdir(parents=True, exist_ok=True)
    faltan = [g for g in QV.REGIONES
              if not (dir_sifi / ("%s_full_%s.tsv" % (g, suf))).exists()]
    if faltan:
        cmd = [sys.executable, str(RAIZ / "tools/sifi21_port/run_sifi.py"),
               *[str(FULL / ("%s_full.fasta" % g)) for g in QV.REGIONES],
               "--modo", a.modo, "--backend", a.backend, "--salida", str(dir_sifi)]
        print("$ " + " ".join(cmd), flush=True)
        r = subprocess.run(cmd, cwd=str(RAIZ), text=True, capture_output=True)
        if r.returncode != 0:
            print(r.stdout[-2000:]); print(r.stderr[-2000:])
            raise SystemExit("run_sifi.py fallo con codigo %d" % r.returncode)

    # El recorte ya lo corrio quimeras_v2.py (regiones.fasta, nombre <gen>_sel).
    dir_rec = TRABAJO / "sifi" / sufc

    filas, detalle = [], []
    for g in QV.REGIONES:
        ini, fin = QV.CONJUNTOS[a.conjunto][g]
        ctx = {int(f["pos"]): QV.es_eficiente(f)
               for f in QV.leer_tsv(dir_sifi / ("%s_full_%s.tsv" % (g, suf)))}
        if anclar and sum(ctx.values()) != ANCLA_GEN[g]:
            raise SystemExit("ancla del gen %s: %d eficientes, se esperaban %d"
                             % (g, sum(ctx.values()), ANCLA_GEN[g]))
        rec = {int(f["pos"]): QV.es_eficiente(f)
               for f in QV.leer_tsv(dir_rec / ("%s_sel_%s.tsv" % (g, suf)))}

        largo = fin - ini + 1
        en_contexto = [p for p in range(ini, fin + 1) if p in ctx]
        ef_contexto = sum(1 for p in en_contexto if ctx[p])
        if anclar and ef_contexto != ancla_region[g]:
            raise SystemExit("ancla de region de C7 en %s: %d, se esperaban %d"
                             % (g, ef_contexto, ancla_region[g]))

        # las 20 posiciones de inicio que el recorte pierde
        perdidas = [p for p in en_contexto if p > fin - VENTANA + 1]
        ef_perdidas = sum(1 for p in perdidas if ctx[p])

        # las compartidas: misma ventana de 21 nt en los dos calculos
        flips = []
        for p in en_contexto:
            if p in perdidas:
                continue
            q = p - ini + 1                       # posicion dentro del recorte
            if ctx[p] != rec.get(q):
                dist = min(q - 1, (largo - VENTANA + 1) - q)
                flips.append({"gen": g, "pos_gen": p, "pos_recorte": q,
                              "en_contexto": ctx[p], "recortada": rec.get(q),
                              "nt_hasta_el_borde": dist})
        detalle.extend(flips)
        gana = sum(1 for f in flips if f["recortada"])
        pierde = sum(1 for f in flips if not f["recortada"])
        ef_rec = sum(rec.values())
        filas.append({
            "gen": g, "region": "%d-%d" % (ini, fin), "largo_nt": largo,
            "ventanas_en_contexto": len(en_contexto), "ef_en_contexto": ef_contexto,
            "ventanas_recortada": len(rec), "ef_recortada": ef_rec,
            "delta": ef_rec - ef_contexto,
            "ventanas_perdidas": len(perdidas), "ef_perdidas": ef_perdidas,
            "flips": len(flips), "flips_a_eficiente": gana,
            "flips_a_no_eficiente": pierde,
            "cierra": ef_rec - ef_contexto == -ef_perdidas + gana - pierde,
            "eficacia_en_contexto": round(ef_contexto / len(en_contexto), 4),
            "eficacia_recortada": round(ef_rec / len(rec), 4),
            "flip_mas_lejano_nt": max((f["nt_hasta_el_borde"] for f in flips),
                                      default=None),
        })

    with open(RESULTADOS / ("recorte_vs_contexto_%s.tsv" % sufc), "w",
              encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()), delimiter="\t")
        w.writeheader(); w.writerows(filas)
    with open(RESULTADOS / ("recorte_vs_contexto_flips_%s.tsv" % sufc), "w",
              encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(detalle[0].keys()), delimiter="\t")
        w.writeheader(); w.writerows(detalle)
    (RESULTADOS / ("recorte_vs_contexto_meta_%s.json" % sufc)).write_text(json.dumps({
        "anclas_gen_completo": ANCLA_GEN, "conjunto": a.conjunto, "anclas_region": ancla_region,
        "las_dos_anclas_pasaron": anclar, "modo": a.modo, "backend": a.backend,
        "python": sys.version.split()[0],
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print("ANCLAS: gen completo y region en contexto, las ocho coinciden\n")
    print("%-12s %-12s %5s %5s %6s %6s %6s %6s %6s %6s" % (
        "gen", "region", "vctx", "efct", "vrec", "efrec", "delta", "perd", "gana",
        "pierde"))
    for f in filas:
        print("%-12s %-12s %5d %5d %6d %6d %6d %6d %6d %6d" % (
            f["gen"], f["region"], f["ventanas_en_contexto"], f["ef_en_contexto"],
            f["ventanas_recortada"], f["ef_recortada"], f["delta"],
            f["ef_perdidas"], f["flips_a_eficiente"], f["flips_a_no_eficiente"]))
    print("\ncontabilidad cierra en las cuatro: %s" % all(f["cierra"] for f in filas))
    print("flip mas lejano del borde: %s nt" % max(
        f["flip_mas_lejano_nt"] for f in filas if f["flip_mas_lejano_nt"] is not None))
    print("escrito en %s" % RESULTADOS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
