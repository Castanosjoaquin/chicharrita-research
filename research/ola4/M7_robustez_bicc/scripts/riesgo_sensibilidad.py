"""M7 eje 3 - cuanto depende la comparacion del criterio de riesgo que se elija.

**Esto NO implementa la regla de alertas.** M6 (#10) tiene que decidir que alertas se
aceptan con justificacion y cuales siguen siendo bloqueantes, y esa decision es del
usuario. Lo que hace este script es lo contrario de decidir: **mide cuanto cambia la
comparacion entre las tres regiones de `BicC_Dm` segun cual de los cuatro criterios se
elija**, para que la decision de M6 se tome con el numero a la vista. Si las cuatro
combinaciones dicen lo mismo, la eleccion no cambia esta recomendacion y se puede decir
asi; si dicen cosas distintas, hay que saberlo antes y no despues.

Las cuatro combinaciones son el cruce de:

  umbral de coincidencia (D28)   `perfecto_21` (21/21 exacto, con bioensayo detras) y
                                 `perfecto_ge19` (bloque contiguo perfecto de >= 19 nt,
                                 convencion del campo sin experimento). Nunca se mezclan
                                 en un numero: se reportan los dos, diciendo cual es cual.
  regla de riesgo (D17)          conservadora, donde una ventana con coincidencia en un
                                 no objetivo cuenta como riesgo sea eficiente o no; y
                                 mecanicista, donde solo cuenta si ademas es eficiente.

Que cambia y que no entre las dos reglas. El conteo de ventanas **eficientes y limpias**
—eficiente y sin coincidencia— es el mismo bajo las dos, porque una ventana eficiente con
coincidencia es riesgosa para ambas. Lo que cambia es **el tamano del riesgo declarado**
de la region: todas las ventanas con coincidencia, o solo las eficientes. Por eso se
reportan dos cosas distintas por combinacion, y no una sola.

Los pesos de D18 **no se aplican**: cada referencia se cuenta por separado y el agregado
es sin ponderar. M5 (#9) va a partir ese vector en exposicion y conservacion, de modo que
ponderar hoy seria fijar lo que esa linea tiene que decidir.

El panel es el de C7 v2, seis referencias, con *Dalbulus maidis* excluido por ser el
blanco. Las coincidencias se calculan con `tools/sifi21_port/offtarget_21nt.py`, que busca
coincidencia exacta con un automata de Aho-Corasick sobre las referencias en disco; nada
sale de la maquina. El ancla es que los conteos del gen entero por referencia reproduzcan
los de `research/ola3/C7_ranking_v2/resultados/ranking_v2.json`.

Uso (desde la raiz del repositorio):

    python tools/sifi21_port/offtarget_21nt.py --consulta work/W5/fasta/BicC_Dm_full.fasta \\
        --db work/W5/ref/GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna.fna.gz \\
             work/W5/ref/GCF_914767665.1_icHarAxyr1.1_rna.fna.gz \\
             work/W5/ref/GCF_003254395.2_Amel_HAv3.1_rna.fna.gz \\
             work/W5/ref/GCF_021130785.1_UT_GWSS_2.1_rna.fna.gz \\
             work/W5/ref/GCF_002217175.1_ASM221717v1_rna.fna.gz \\
             work/W5/ref/humano_rna.fna.gz \\
        --salida work/m7_offtarget
    SIFI_RNAPLFOLD=/ruta/a/RNAplfold-2.1.5 \\
        python research/ola4/M7_robustez_bicc/scripts/riesgo_sensibilidad.py

El TSV de `offtarget_21nt.py` lleva una columna `sirna`, asi que vive en `work/` y **no se
versiona**. Los primitivos del motor se cachean en `/tmp/m7_prims/`: son deterministas y
recalcularlos cuesta media hora.
"""

from __future__ import annotations

import csv
import itertools
import json
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
SALIDA = AQUI.parents[1] / "resultados"
CACHE = Path("/tmp/m7_prims")
sys.path.insert(0, str(AQUI.parent))
sys.path.insert(0, str(RAIZ))
from sifi_plus.complejidad import es_baja  # noqa: E402  (criterio de D59)
from grilla_parametros import (ACC_GRID, BACKENDS, DEF_ACC, DEF_END, END_GRID,  # noqa: E402
                               FOCO, K, MODOS, REGIONES, RIVALES, TABLAS,
                               eficientes, leer_fasta, primitivos)

OFFTARGET = RAIZ / "work" / "m7_offtarget" / "offtarget_por_sirna.tsv"
RANKING = RAIZ / "research" / "ola3" / "C7_ranking_v2" / "resultados" / "ranking_v2.json"
GEN = RAIZ / "work" / "W5" / "plfold" / "BicC_Dm.rna.fa"

# Nombre del archivo de referencia -> etiqueta del panel de C7 v2.
PANEL = {
    "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna": "maiz",
    "GCF_914767665.1_icHarAxyr1.1_rna": "H_axyridis",
    "GCF_003254395.2_Amel_HAv3.1_rna": "A_mellifera",
    "GCF_021130785.1_UT_GWSS_2.1_rna": "H_vitripennis",
    "GCF_002217175.1_ASM221717v1_rna": "F_candida",
    "humano_rna": "humano",
}
UMBRALES = ["perfecto_21", "perfecto_ge19"]
REGLAS = ["conservadora", "mecanicista"]


def prims(seq: str, backend: str, tabla: str, clave: str) -> dict:
    """`primitivos` con cache en disco: la cuenta es determinista y cuesta minutos."""
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / ("%s_%s_%s.npz" % (clave, backend, tabla))
    if f.exists():
        d = np.load(f, allow_pickle=True)
        return {k: d[k] for k in ("dg_s", "dg_as", "acc", "nt19_at", "nt2_gc")}
    P = primitivos(seq, backend, tabla)
    np.savez(f, **{k: P[k] for k in ("dg_s", "dg_as", "acc", "nt19_at", "nt2_gc")})
    return P


def mascaras_alerta(n_vent: int) -> dict:
    """Por ventana y por umbral: hay coincidencia en alguna referencia del panel.

    Desde D59 cada conteo se informa en dos cifras, el total y cuanto de ese total es de
    **baja complejidad**: la cola de poli-A de un transcrito coincide con la de cualquier
    otro y eso no dice nada sobre el riesgo de un ARNdc. El criterio es el de
    `sifi_plus/complejidad.py` —racha de un mismo nucleotido de 10 nt o mas, o dos
    nucleotidos distintos o menos— y es nuestro `[H]`, no un estandar. Las ventanas **no
    se descartan**: se marcan y se descuentan a la vista.
    """
    if not OFFTARGET.exists():
        raise SystemExit("falta %s: corre offtarget_21nt.py (ver encabezado). "
                         "NO se declara cero." % OFFTARGET)
    m = {u: np.zeros(n_vent, dtype=bool) for u in UMBRALES}
    baja = np.zeros(n_vent, dtype=bool)
    por_ref = {u: {} for u in UMBRALES}
    with OFFTARGET.open(encoding="utf-8") as fh:
        r = csv.DictReader(fh, delimiter="\t")
        cols = [c for c in r.fieldnames if "|" in c]
        for u in UMBRALES:
            for c in cols:
                base, crit = c.split("|")
                if crit == u and base in PANEL:
                    por_ref[u][PANEL[base]] = np.zeros(n_vent, dtype=bool)
        for fila in r:
            if fila["consulta"] != "BicC_Dm_full":
                continue
            i = int(fila["pos"]) - 1
            if not 0 <= i < n_vent:
                continue
            if fila.get("sirna") and es_baja(fila["sirna"]):
                baja[i] = True
            for c in cols:
                base, crit = c.split("|")
                if crit not in UMBRALES or base not in PANEL:
                    continue
                if int(fila[c] or 0) > 0:
                    m[crit][i] = True
                    por_ref[crit][PANEL[base]][i] = True
    return {"total": m, "por_referencia": por_ref, "baja_complejidad": baja}


def ancla_panel(al: dict) -> dict:
    """Los conteos del gen entero por referencia tienen que ser los de C7 v2."""
    d = json.loads(RANKING.read_text(encoding="utf-8"))
    pr = d["k"]["21"]["gen_entero"]["BicC_Dm"]["por_referencia"]
    out, fallan = {}, []
    for ref, crits in pr.items():
        for u in UMBRALES:
            esperado = crits.get(u, 0)
            obtenido = int(al["por_referencia"][u].get(ref, np.zeros(1)).sum())
            out["%s/%s" % (ref, u)] = {"obtenido": obtenido, "esperado": esperado,
                                       "coincide": obtenido == esperado}
            if obtenido != esperado:
                fallan.append("%s/%s: %d != %d" % (ref, u, obtenido, esperado))
    if fallan:
        raise SystemExit("ANCLA FALLIDA del panel de C7 v2: " + "; ".join(fallan))
    return out


def main() -> int:
    SALIDA.mkdir(parents=True, exist_ok=True)
    gen = leer_fasta(GEN)
    n_vent = len(gen) - K + 1
    al = mascaras_alerta(n_vent)
    anc = ancla_panel(al)
    print("ancla del panel OK: %d de %d conteos por referencia y umbral"
          % (sum(v["coincide"] for v in anc.values()), len(anc)), flush=True)
    for u in UMBRALES:
        print("  %s: %d ventanas del gen con coincidencia en el panel"
              % (u, int(al["total"][u].sum())), flush=True)

    P_gen, P_rec = {}, {}
    for backend, tabla in itertools.product(BACKENDS, TABLAS):
        P_gen[(backend, tabla)] = prims(gen, backend, tabla, "gen")
        for nom, (ini, fin) in REGIONES.items():
            P_rec[(backend, tabla, nom)] = prims(gen[ini - 1:fin], backend, tabla,
                                                 "rec_" + nom.replace("-", "_"))
    print("primitivos listos", flush=True)

    filas = []
    for backend, tabla, modo, e, a in itertools.product(BACKENDS, TABLAS, MODOS,
                                                        END_GRID, ACC_GRID):
        eff_gen = eficientes(P_gen[(backend, tabla)], modo, e, a)
        base = {"backend": backend, "tabla_nn": tabla, "modo": modo, "end_thr": e,
                "access_thr": a, "es_defecto": int(e == DEF_END and a == DEF_ACC)}
        for marco in ("contexto", "recorte"):
            for u in UMBRALES:
                fila = dict(base, marco=marco, umbral=u)
                for nom, (ini, fin) in REGIONES.items():
                    sl = slice(ini - 1, fin)
                    alerta = al["total"][u][sl]
                    if marco == "contexto":
                        ef = eff_gen[sl]
                    else:
                        ef_rec = eficientes(P_rec[(backend, tabla, nom)], modo, e, a)
                        # La ventana i del recorte es la posicion ini+i-1 del gen, asi
                        # que la alerta se mapea directo; el recorte tiene 20 arranques
                        # menos que la region.
                        ef = np.zeros(len(alerta), dtype=bool)
                        ef[:len(ef_rec)] = ef_rec
                    bc = al["baja_complejidad"][sl]
                    fila["%s|limpias_eficientes" % nom] = int((ef & ~alerta).sum())
                    fila["%s|riesgo_conservadora" % nom] = int(alerta.sum())
                    fila["%s|riesgo_conservadora_baja_compl" % nom] = int((alerta & bc).sum())
                    fila["%s|riesgo_mecanicista" % nom] = int((ef & alerta).sum())
                    fila["%s|riesgo_mecanicista_baja_compl" % nom] = int((ef & alerta & bc).sum())
                    fila["%s|eficientes" % nom] = int(ef.sum())
                filas.append(fila)

    cols = list(filas[0].keys())
    with (SALIDA / "riesgo_sensibilidad.tsv").open("w", encoding="utf-8") as fh:
        fh.write("\t".join(cols) + "\n")
        for f in filas:
            fh.write("\t".join(str(f[c]) for c in cols) + "\n")

    # -- fracciones por combinacion -----------------------------------------------------
    res = {"que_es_esto": "sensibilidad al criterio de riesgo; NO adopta ninguna regla. "
                          "La eleccion es de M6 (#10) y del usuario.",
           "panel": sorted(PANEL.values()), "pesos_D18_aplicados": False,
           "ancla_panel": anc,
           "criterio_de_baja_complejidad": "sifi_plus/complejidad.py (D59): racha de un "
                                           "mismo nucleotido >= 10 nt, o <= 2 nucleotidos "
                                           "distintos en la ventana. Es nuestro [H].",
           "ventanas_con_coincidencia_en_el_gen": {
               u: {"total": int(al["total"][u].sum()),
                   "de_baja_complejidad": int((al["total"][u] & al["baja_complejidad"]).sum())}
               for u in UMBRALES},
           "ventanas_de_baja_complejidad_en_el_gen": int(al["baja_complejidad"].sum()),
           "por_combinacion": {}, "en_el_punto_por_defecto": {}}
    for marco, u in itertools.product(("contexto", "recorte"), UMBRALES):
        sel = [f for f in filas if f["marco"] == marco and f["umbral"] == u]
        bloque = {"configuraciones": len(sel)}
        for riv in RIVALES:
            gana = sum(f["%s|limpias_eficientes" % FOCO] > f["%s|limpias_eficientes" % riv]
                       for f in sel)
            empata = sum(f["%s|limpias_eficientes" % FOCO] == f["%s|limpias_eficientes" % riv]
                         for f in sel)
            bloque["limpias_eficientes_vs_%s" % riv] = {
                "gana": gana, "empata": empata, "pierde": len(sel) - gana - empata,
                "gana_pct": round(100 * gana / len(sel), 1)}
        for regla in REGLAS:
            clave = "riesgo_%s" % regla
            menor = sum(all(f["%s|%s" % (FOCO, clave)] < f["%s|%s" % (riv, clave)]
                            for riv in RIVALES) for f in sel)
            bloque["riesgo_%s_menor_que_las_dos_pct" % regla] = round(100 * menor / len(sel), 1)
            # La celda de referencia se declara: ViennaRNA 2.7.2, NN3, modo corregido,
            # punto por defecto. Con otra celda los numeros son otros.
            ref = [f for f in sel if f["es_defecto"] and f["backend"] == "vienna"
                   and f["tabla_nn"] == "NN3" and f["modo"] == "corregido"]
            bloque["riesgo_%s_en_vienna_NN3_corregido_defecto" % regla] = {
                nom: ref[0]["%s|%s" % (nom, clave)] for nom in REGIONES} if ref else None
            bloque["riesgo_%s_de_baja_complejidad" % regla] = {
                nom: ref[0]["%s|%s_baja_compl" % (nom, clave)]
                for nom in REGIONES} if ref else None
            # Rango sobre las ocho celdas del punto por defecto, para que se vea si la
            # celda elegida es representativa.
            todas = [f for f in sel if f["es_defecto"]]
            bloque["riesgo_%s_rango_en_las_celdas_por_defecto" % regla] = {
                nom: [min(f["%s|%s" % (nom, clave)] for f in todas),
                      max(f["%s|%s" % (nom, clave)] for f in todas)] for nom in REGIONES}
        res["por_combinacion"]["%s / %s" % (marco, u)] = bloque
    for f in filas:
        if f["es_defecto"]:
            k = "%s/%s/%s/%s/%s" % (f["backend"], f["tabla_nn"], f["modo"], f["marco"],
                                    f["umbral"])
            res["en_el_punto_por_defecto"][k] = {
                nom: {"limpias_eficientes": f["%s|limpias_eficientes" % nom],
                      "riesgo_conservadora": f["%s|riesgo_conservadora" % nom],
                      "riesgo_mecanicista": f["%s|riesgo_mecanicista" % nom]}
                for nom in REGIONES}
    (SALIDA / "riesgo_sensibilidad.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

    for clave, b in res["por_combinacion"].items():
        print("%-26s n=%5d | limpias-eficientes: gana a 2121 %5.1f%%, a 264 %5.1f%% | "
              "riesgo conservador (vienna/NN3/corregido) %s"
              % (clave, b["configuraciones"],
                 b["limpias_eficientes_vs_2121-2420"]["gana_pct"],
                 b["limpias_eficientes_vs_264-563"]["gana_pct"],
                 b["riesgo_conservadora_en_vienna_NN3_corregido_defecto"]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
