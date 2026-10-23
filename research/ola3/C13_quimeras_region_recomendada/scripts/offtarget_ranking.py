"""Off-targets de las 12 quimeras completas y los ejes del ranking, con el panel de W7.

Que pregunta contesta: si una quimera armada con dos regiones recomendadas se puede
poner en el ranking, y si alguna queda distinta de sus dos partes.

Tres decisiones de metodo que conviene leer antes de los numeros.

1. **No se tamizan las 5.760 ventanas de las 12 quimeras, sino 1.160.** El estado de
   off-target de una ventana depende solo de su secuencia de 21 nt, y toda ventana
   heredada es, base por base, una ventana de su region de origen. Lo unico nuevo son
   las 20 ventanas de cada empalme. Asi que se tamizan las 4 regiones completas y,
   por quimera, el tramo de 40 nt que cruza la union (los ultimos 20 nt de la region
   izquierda mas los primeros 20 de la derecha), que da exactamente esas 20 ventanas.
   El riesgo de cada quimera se recompone por posicion. Es identico a tamizar la
   molecula entera y cuesta una pasada en vez de siete.

2. **El riesgo se evalua con `ranking.ejes`, importado sin tocarlo**, para que los
   ejes sean los de W7: eficacia = fraccion de ventanas eficientes; limpieza = 1
   menos la exposicion ponderada; `buenos_limpios` = eficientes sin ningun acierto;
   veto = al menos un 21/21. Los pesos por referencia y por criterio son los base de
   `ranking.pesos_base()`.

3. **El genoma de *Dalbulus maidis* en una quimera mixta.** Para un gen del insecto es
   on-target y sale del riesgo; para uno viral entra (D5, con el valor por defecto
   `--dmaidis-viral off`). Una quimera que pega una region viral con una del insecto
   no es ninguno de los dos casos, y la regla de `ranking.excluidas_de` no alcanza.
   Se reporta de tres formas: `viral` (cuenta en toda la molecula), `insecto` (no
   cuenta en ninguna parte) y `mixto`, que es nuestra propuesta: cuenta en las
   ventanas heredadas de la mitad viral y no en las de la mitad del insecto. Las 20
   ventanas del empalme son sequencia que no pertenece a ninguno de los dos genes;
   en `mixto` se cuentan, que es la lectura conservadora. El motor no se modifica: lo
   que se construye distinto es la matriz de riesgo que se le pasa.

Nada sale de la maquina: las seis referencias se leen de disco.

Uso:
    python research/ola3/C13_quimeras_region_recomendada/scripts/offtarget_ranking.py \
        --conjunto recomendadas --modo fiel --backend vienna
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[4]
BLOQUE = Path(__file__).resolve().parents[1]
RESULTADOS = BLOQUE / "resultados"
TRABAJO = RAIZ / "work/C13"
DB = RAIZ / "work/offtarget_db"

sys.path.insert(0, str(RAIZ / "tools/sifi21_port"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ranking as R           # noqa: E402  el motor de W7, sin tocar
import quimeras_v2 as QV      # noqa: E402  las coordenadas y los recortes

VENTANA = 21
VIRALES = {"MP_MRFV", "CP_MRFV"}


def escribir_consultas(regiones: dict, quimeras: dict, ruta: Path):
    """Las 4 regiones y, por quimera, el tramo de 40 nt que cruza la union."""
    with open(ruta, "w", encoding="utf-8") as fh:
        for g in QV.REGIONES:
            fh.write(">%s_sel\n%s\n" % (g, regiones[g]))
        for n, d in quimeras.items():
            corte = d["corte"]
            tramo = d["seq"][corte - 20:corte + 20]
            assert len(tramo) == 40, n
            fh.write(">J_%s\n%s\n" % (n, tramo))


def leer_por_sirna(ruta: Path):
    """(consulta, pos) -> {columna: bool}. Columna es 'base|criterio'."""
    out, cols = {}, []
    with ruta.open(encoding="utf-8") as fh:
        r = csv.DictReader(fh, delimiter="\t")
        cols = [c for c in (r.fieldnames or []) if "|" in c]
        for fila in r:
            out[(fila["consulta"], int(fila["pos"]))] = {
                c: int(fila[c] or 0) > 0 for c in cols}
    return out, cols


def origen(p: int, corte: int, izq: str, der: str, nombre_q: str):
    """De donde viene la ventana que empieza en la posicion p de la quimera."""
    if p <= corte - VENTANA + 1:
        return ("%s_sel" % izq, p, "izq")
    if p > corte:
        return ("%s_sel" % der, p - corte, "der")
    return ("J_%s" % nombre_q, p - (corte - 20), "empalme")


def matriz(n: int, filas_off, cols, claves, cero_dmaidis=None):
    """Matriz de riesgo con la forma que espera `ranking.ejes`.

    `claves[p]` es la (consulta, pos) de la ventana p (1-based). `cero_dmaidis` es
    el conjunto de posiciones donde el genoma del vector NO cuenta (on-target).
    """
    riesgo: dict[str, dict[str, np.ndarray]] = {}
    for c in cols:
        ref, crit = c.split("|", 1)
        riesgo.setdefault(ref, {})[crit] = np.zeros(n, dtype=bool)
    for p in range(1, n + 1):
        d = filas_off.get(claves[p])
        if d is None:
            continue
        for c, hay in d.items():
            if not hay:
                continue
            ref, crit = c.split("|", 1)
            if cero_dmaidis and ref == R.DMAIDIS and p in cero_dmaidis:
                continue
            riesgo[ref][crit][p - 1] = True
    for ref in riesgo:
        for crit in R.CRITERIOS:
            riesgo[ref].setdefault(crit, np.zeros(n, dtype=bool))
    return riesgo


def ejes_de(n, eficiente, riesgo, excluir, solo_eficientes):
    wr, wc = R.pesos_base()
    g = {"gen": "x", "n": n, "eficiente": eficiente,
         "presente": np.ones(n, dtype=bool), "riesgo": riesgo}
    return R.ejes(g, 1, n, wr, wc, excluir, solo_eficientes)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--conjunto", choices=tuple(QV.CONJUNTOS), default="recomendadas")
    ap.add_argument("--modo", choices=("fiel", "corregido"), default="fiel")
    ap.add_argument("--backend", choices=("exe", "vienna"), default="vienna")
    ap.add_argument("--rehacer-tamizaje", action="store_true", dest="rehacer")
    a = ap.parse_args(argv)
    suf = "%s_%s_%s" % (a.conjunto, a.modo, a.backend)

    regiones = QV.recortar(a.conjunto)
    quimeras = {}
    for izq, der in itertools.permutations(QV.REGIONES, 2):
        quimeras["Q_%s__%s" % (izq, der)] = {
            "izq": izq, "der": der,
            "seq": regiones[izq] + regiones[der], "corte": len(regiones[izq])}

    dir_off = TRABAJO / "offtarget" / a.conjunto
    dir_off.mkdir(parents=True, exist_ok=True)
    consultas = dir_off / "consultas.fasta"
    escribir_consultas(regiones, quimeras, consultas)
    tsv_off = dir_off / "offtarget_por_sirna.tsv"
    if a.rehacer or not tsv_off.exists():
        cmd = [sys.executable, str(RAIZ / "tools/sifi21_port/offtarget_21nt.py"),
               "--consulta", str(consultas), "--mm1",
               "--db", *[str(p) for p in sorted(DB.glob("*.fna.gz"))],
               "--salida", str(dir_off)]
        print("$ " + " ".join(cmd), flush=True)
        r = subprocess.run(cmd, cwd=str(RAIZ), text=True)
        if r.returncode != 0:
            raise SystemExit("offtarget_21nt.py fallo con codigo %d" % r.returncode)
    else:
        print("tamizaje ya hecho: %s (--rehacer-tamizaje para repetirlo)" % tsv_off)

    filas_off, cols = leer_por_sirna(tsv_off)
    print("tamizaje: %d ventanas, %d columnas" % (len(filas_off), len(cols)))

    # perfiles de eficiencia que dejo quimeras_v2.py
    dir_sifi = TRABAJO / "sifi" / suf

    def perfil_de(nombre, n):
        ruta = dir_sifi / ("%s_%s_%s.tsv" % (nombre, a.modo, a.backend))
        if not ruta.exists():
            raise SystemExit("falta %s; corre primero quimeras_v2.py" % ruta)
        v = np.zeros(n, dtype=bool)
        for f in QV.leer_tsv(ruta):
            p = int(f["pos"])
            if 1 <= p <= n:
                v[p - 1] = QV.es_eficiente(f)
        return v

    filas, detalle = [], {}
    for solo in (False, True):
        regla = "mecanicista" if solo else "conservadora"

        for g in QV.REGIONES:
            n = len(regiones[g]) - VENTANA + 1
            claves = {p: ("%s_sel" % g, p) for p in range(1, n + 1)}
            riesgo = matriz(n, filas_off, cols, claves)
            excluir = set() if g in VIRALES else {R.DMAIDIS}
            e = ejes_de(n, perfil_de("%s_sel" % g, n), riesgo, excluir, solo)
            filas.append({"objeto": g, "clase": "region", "trato_dmaidis":
                          "viral" if g in VIRALES else "insecto", "regla": regla,
                          "largo_nt": len(regiones[g]), **{k: e[k] for k in
                          ("n_ventanas", "eficientes", "eficacia", "limpieza",
                           "buenos_limpios", "con_off_target", "con_21_perfecto",
                           "vetada")}})

        for nombre, d in quimeras.items():
            izq, der, corte = d["izq"], d["der"], d["corte"]
            n = len(d["seq"]) - VENTANA + 1
            claves, lado = {}, {}
            for p in range(1, n + 1):
                c, po, l = origen(p, corte, izq, der, nombre)
                claves[p], lado[p] = (c, po), l
            efi = perfil_de(nombre, n)
            mezcla = (izq in VIRALES) != (der in VIRALES)
            tratos = ["viral", "insecto", "mixto"] if mezcla else (
                ["viral"] if izq in VIRALES else ["insecto"])
            for trato in tratos:
                if trato == "viral":
                    riesgo, excluir = matriz(n, filas_off, cols, claves), set()
                elif trato == "insecto":
                    riesgo, excluir = matriz(n, filas_off, cols, claves), {R.DMAIDIS}
                else:
                    cero = {p for p in range(1, n + 1)
                            if (lado[p] == "izq" and izq not in VIRALES)
                            or (lado[p] == "der" and der not in VIRALES)}
                    riesgo, excluir = matriz(n, filas_off, cols, claves, cero), set()
                e = ejes_de(n, efi, riesgo, excluir, solo)
                filas.append({"objeto": nombre, "clase": "quimera",
                              "trato_dmaidis": trato, "regla": regla,
                              "largo_nt": len(d["seq"]), **{k: e[k] for k in
                              ("n_ventanas", "eficientes", "eficacia", "limpieza",
                               "buenos_limpios", "con_off_target", "con_21_perfecto",
                               "vetada")}})
            if not solo:
                emp = [p for p in range(1, n + 1) if lado[p] == "empalme"]
                detalle[nombre] = {
                    "ventanas_empalme": len(emp),
                    "empalme_eficientes": int(efi[[p - 1 for p in emp]].sum()),
                    "empalme_con_acierto": {},
                }
                for ref in sorted({c.split("|")[0] for c in cols}):
                    for crit in R.CRITERIOS:
                        k = "%s|%s" % (ref, crit)
                        if k not in cols:
                            continue
                        cuenta = sum(1 for p in emp
                                     if filas_off.get(claves[p], {}).get(k))
                        if cuenta:
                            detalle[nombre]["empalme_con_acierto"][
                                "%s|%s" % (R.corto(ref), crit)] = cuenta

    with open(RESULTADOS / ("ejes_ranking_%s.tsv" % suf), "w", encoding="utf-8",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()), delimiter="\t")
        w.writeheader(); w.writerows(filas)
    (RESULTADOS / ("empalmes_offtarget_%s.json" % suf)).write_text(
        json.dumps(detalle, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\nregla conservadora, trato del vector segun la clase")
    print("%-26s %-9s %5s %5s %7s %8s %7s %5s" % (
        "objeto", "dmaidis", "vent", "efic", "eficac", "limpieza", "lim+ef", "veto"))
    for f in filas:
        if f["regla"] != "conservadora":
            continue
        if f["clase"] == "quimera" and f["trato_dmaidis"] == "insecto" and \
                (f["objeto"].count("MRFV") == 1):
            continue
        print("%-26s %-9s %5d %5d %7.4f %8.4f %7d %5s" % (
            f["objeto"], f["trato_dmaidis"], f["n_ventanas"], f["eficientes"],
            f["eficacia"], f["limpieza"], f["buenos_limpios"],
            "SI" if f["vetada"] else "no"))
    print("\nescrito en %s" % RESULTADOS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
