"""M7 eje 1 - la ventaja de `BicC_Dm` 922-1221 frente a los parametros del modelo.

Que contesta. Diego pidio comprobar la robustez de la ventaja de la region que
recomendamos «frente a los parametros del modelo, la referencia utilizada y los criterios
de riesgo». Este script cubre el primer eje: en que fraccion de las configuraciones
922-1221 le gana a 2121-2420 (la region de C7) y a 264-563 (la que eligio el laboratorio).
Las tres regiones tienen 300 nt, asi que los conteos se comparan sin normalizar.

Cinco ejes, cruzados todos contra todos (4.368 configuraciones):

  brecha de estabilidad   21 valores, 0,0 a 2,0 kcal/mol   (la grilla de C9)
  accesibilidad           26 valores, 0,05 a 0,30          (la grilla de C9)
  modo del port           fiel / corregido
  tabla de apilamiento    RNA_NN3 (la del original) / RNA_NN4 (la de sifi21INTA)
  motor de accesibilidad  ViennaRNA 2.7.2 / RNAplfold 2.1.5 (el del si-Fi original)

Los dos ultimos no estaban en la grilla de C9. El de la tabla lo pide el issue #11; el del
motor lo agrega esta linea porque M1 midio que el motor mueve los conteos en direcciones
distintas segun el gen, de modo que es un eje con efecto conocido y sin medir sobre la
eleccion de region.

**Los conteos de los dos motores no son comparables entre si.** Cada fila del TSV declara
`backend` y `tabla_nn`, y las fracciones se calculan comparando regiones dentro de una
misma configuracion, nunca entre motores.

Dos marcos por configuracion, porque son dos preguntas distintas:

  contexto   la ventana se evalua dentro del gen de 2.520 nt; la region cuenta las
             ventanas que ARRANCAN en ella (300 arranques). Es la cifra que venia
             publicando el proyecto.
  recorte    la molecula recortada de 300 nt se pliega sola: 280 arranques y, en las dos
             primeras posiciones, extremos sin nucleotidos colgantes (`_ends_plain`),
             porque el contexto de dos posiciones antes no existe. Es la cifra de lo que
             se sintetizaria (C13 §4, remedido por M2 en el par 4).

El recorte se reporta ademas sin sus dos primeras posiciones, que es donde M2 encontro el
artefacto de borde, para que se vea si la ventaja depende de ellas.

Anclas, que corren antes de cualquier medicion y abortan el script si fallan:

  1. el gen entero, punto por defecto (brecha 1,0, accesibilidad 0,1, u = 8, 22 C, NN3):
     142/39/223/35 en fiel y 123/30/171/29 en corregido con ViennaRNA 2.7.2;
     133/32/212/42 y 114/25/162/34 con RNAplfold 2.1.5;
  2. las cuatro regiones vigentes en contexto: 38, 21, 36 y 21.

Uso (desde la raiz del repositorio):

    SIFI_RNAPLFOLD=/ruta/a/RNAplfold-2.1.5 \\
        python research/ola4/M7_robustez_bicc/scripts/grilla_parametros.py

Sin esa variable el eje del motor se declara **no corrido** y no cero, y el resto de la
grilla corre igual. El binario se compila desde el tag v2.1.5 del fuente oficial con la
receta del encabezado de `research/ola4/M2_ventana_a_ventana/scripts/correr_pares.py`.
"""

from __future__ import annotations

import itertools
import json
import os
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
SALIDA = AQUI.parents[1] / "resultados"
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))
from sifi_core import (SifiEngine, accessibility_exe, accessibility_vienna,  # noqa: E402
                       apply_rules)

GENES = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]
FASTA = {g: RAIZ / "work" / "W5" / "plfold" / f"{g}.rna.fa" for g in GENES}

# Regiones vigentes al 2026-10-23 (1-based inclusive). `BicC_Dm` por D25.
VIGENTES = {"MP_MRFV": (72, 271), "CP_MRFV": (99, 298),
            "BicC_Dm": (922, 1221), "ATPaseD_Dm": (72, 371)}

# Las tres regiones de 300 nt que compite este eje.
REGIONES = {"922-1221": (922, 1221),     # vigente, D25, por conservacion (C8)
            "2121-2420": (2121, 2420),   # la de C7, por densidad
            "264-563": (264, 563)}       # la que eligio EPILAB
FOCO = "922-1221"
RIVALES = ["2121-2420", "264-563"]

K = 21
U = 8
TEMP = 22.0
END_GRID = [round(0.1 * i, 2) for i in range(21)]          # 0,0 .. 2,0 kcal/mol
ACC_GRID = [round(0.05 + 0.01 * i, 2) for i in range(26)]  # 0,05 .. 0,30
DEF_END, DEF_ACC = 1.0, 0.1
MODOS = ["fiel", "corregido"]
TABLAS = ["NN3", "NN4"]

ANCLA_GEN = {
    ("fiel", "vienna"): {"MP_MRFV": 142, "CP_MRFV": 39, "BicC_Dm": 223, "ATPaseD_Dm": 35},
    ("corregido", "vienna"): {"MP_MRFV": 123, "CP_MRFV": 30, "BicC_Dm": 171, "ATPaseD_Dm": 29},
    ("fiel", "exe"): {"MP_MRFV": 133, "CP_MRFV": 32, "BicC_Dm": 212, "ATPaseD_Dm": 42},
    ("corregido", "exe"): {"MP_MRFV": 114, "CP_MRFV": 25, "BicC_Dm": 162, "ATPaseD_Dm": 34},
}
ANCLA_REGION = {"MP_MRFV": 38, "CP_MRFV": 21, "BicC_Dm": 36, "ATPaseD_Dm": 21}

HAY_EXE = bool(os.environ.get("SIFI_RNAPLFOLD")) and Path(
    os.environ.get("SIFI_RNAPLFOLD", "")).exists()
BACKENDS = ["vienna"] + (["exe"] if HAY_EXE else [])


def leer_fasta(ruta: Path) -> str:
    return "".join(l.strip() for l in ruta.read_text().splitlines()
                   if not l.startswith(">")).upper().replace("U", "T")


def primitivos(seq: str, backend: str, tabla_nn: str) -> dict:
    """Los terminos que no dependen de los umbrales, como `sifi_core.primitives`.

    Misma cuenta que el port, con dos diferencias: se le pasa la tabla de apilamiento
    (`primitives` fija NN3) y devuelve vectores de numpy en vez de una lista de dict,
    para poder barrer la grilla sin recalcular. La equivalencia con `apply_rules` se
    verifica en `verificar_vectorizacion`.
    """
    eng = SifiEngine(mode="fiel", temp_c=TEMP, sirna_size=K, tabla_nn=tabla_nn)
    s = "".join(b for b in seq.upper().replace("U", "T") if b in "ACGT")
    sirnas = [s[i:i + K] for i in range(len(s) - K + 1)]
    if backend == "vienna":
        up = accessibility_vienna(s, K, TEMP)
    else:
        up = accessibility_exe(s, K, TEMP)
    dg_s, dg_as, acc, n19, n2g = [], [], [], [], []
    for idx, sirna in enumerate(sirnas):
        pos = idx + 1
        # El original calcula los extremos con nucleotidos colgantes tomando el siRNA de
        # dos posiciones antes; en las dos primeras ventanas ese contexto no existe.
        n2 = None if pos <= 2 else sirnas[pos - 3]
        a, b = eng._ends_plain(sirna) if n2 is None else eng._ends_dangling(sirna, n2)
        dg_s.append(a)
        dg_as.append(b)
        acc.append(up[pos + K - 1][U])
        n19.append(sirna[K - 3] in ("A", "T"))
        n2g.append(sirna[1] in ("G", "C"))
    return {"dg_s": np.array(dg_s), "dg_as": np.array(dg_as),
            "acc": np.array(acc, dtype=float),
            "nt19_at": np.array(n19), "nt2_gc": np.array(n2g),
            "sirnas": sirnas}


def eficientes(P: dict, modo: str, end_thr: float, acc_thr: float) -> np.ndarray:
    """El veredicto por ventana, vectorizado. Replica `sifi_core.apply_rules`."""
    strand = P["dg_as"] >= P["dg_s"]
    end_ok = (P["dg_as"] - P["dg_s"]) >= end_thr
    with np.errstate(invalid="ignore"):
        acc_ok = P["acc"] >= acc_thr          # NaN -> False, como en el port
    thermo = strand & end_ok & acc_ok
    if modo == "fiel":
        # nt19 A/T: si nt2 es G/C decide SOLO la accesibilidad (la rama 2, el atajo).
        return np.where(P["nt19_at"], np.where(P["nt2_gc"], acc_ok, thermo),
                        np.where(P["nt2_gc"], thermo, False))
    return thermo & (P["nt19_at"] | P["nt2_gc"])


def verificar_vectorizacion(P: dict, nombre: str) -> None:
    """Un punto de control: el vector tiene que dar lo mismo que `apply_rules` del port."""
    prims = [{"pos": i + 1, "sirna": P["sirnas"][i], "dg_s": P["dg_s"][i],
              "dg_as": P["dg_as"][i], "lunp": [np.nan] * U + [P["acc"][i]]}
             for i in range(len(P["sirnas"]))]
    for modo, e, a in itertools.product(MODOS, (0.0, 1.0, 2.0), (0.05, 0.1, 0.3)):
        mio = int(eficientes(P, modo, e, a).sum())
        port = apply_rules(prims, mode=modo, u=U, end_thr=e, access_thr=a, sirna_size=K)
        if mio != port:
            raise SystemExit("vectorizacion != apply_rules en %s (%s, %.2f, %.2f): %d vs %d"
                             % (nombre, modo, e, a, mio, port))


def anclas(prim_gen: dict[tuple, dict]) -> dict:
    """Las dos anclas del alcance. Aborta si alguna falla."""
    out = {"gen_entero": {}, "regiones_vigentes": {}}
    for (backend, tabla), P in prim_gen.items():
        if tabla != "NN3":
            continue
        for modo in MODOS:
            eff = {g: eficientes(P[g], modo, DEF_END, DEF_ACC) for g in GENES}
            obt = {g: int(eff[g].sum()) for g in GENES}
            esp = ANCLA_GEN[(modo, backend)]
            out["gen_entero"]["%s/%s" % (backend, modo)] = {
                "obtenido": obt, "esperado": esp, "coincide": obt == esp}
            if obt != esp:
                raise SystemExit("ANCLA FALLIDA gen entero %s/%s: %s != %s"
                                 % (backend, modo, obt, esp))
            if (backend, modo) == ("vienna", "corregido"):
                reg = {g: int(eff[g][VIGENTES[g][0] - 1:VIGENTES[g][1]].sum()) for g in GENES}
                out["regiones_vigentes"] = {"obtenido": reg, "esperado": ANCLA_REGION,
                                            "coincide": reg == ANCLA_REGION,
                                            "medido_con": "vienna/corregido/NN3, punto por defecto"}
                if reg != ANCLA_REGION:
                    raise SystemExit("ANCLA FALLIDA regiones vigentes: %s != %s"
                                     % (reg, ANCLA_REGION))
    return out


def fraccion(filas: list[dict], marco: str, filtro=None) -> dict:
    """Sobre cuantas configuraciones gana el foco, y por cuanto, en un corte de la grilla."""
    sel = [f for f in filas if f["marco"] == marco and (filtro is None or filtro(f))]
    out = {"configuraciones": len(sel)}
    for riv in RIVALES:
        gana = sum(f[FOCO] > f[riv] for f in sel)
        empata = sum(f[FOCO] == f[riv] for f in sel)
        difs = [f[FOCO] - f[riv] for f in sel]
        out["vs_%s" % riv] = {
            "gana": gana, "empata": empata, "pierde": len(sel) - gana - empata,
            "gana_pct": round(100 * gana / len(sel), 1) if sel else None,
            "dif_mediana": float(np.median(difs)) if sel else None,
            "dif_min": int(min(difs)) if sel else None,
            "dif_max": int(max(difs)) if sel else None}
    gana_a_los_dos = sum(all(f[FOCO] > f[riv] for riv in RIVALES) for f in sel)
    out["gana_a_los_dos"] = gana_a_los_dos
    out["gana_a_los_dos_pct"] = round(100 * gana_a_los_dos / len(sel), 1) if sel else None
    return out


def main() -> int:
    SALIDA.mkdir(parents=True, exist_ok=True)
    seqs = {g: leer_fasta(FASTA[g]) for g in GENES}
    bicc = seqs["BicC_Dm"]
    print("BicC_Dm: %d nt. Motores: %s%s" % (
        len(bicc), ", ".join(BACKENDS),
        "" if HAY_EXE else "  (RNAplfold 2.1.5 NO CORRIDO: falta SIFI_RNAPLFOLD)"), flush=True)

    # -- primitivos: una vez por motor y tabla, para el gen y para cada recorte ---------
    prim_gen: dict[tuple, dict] = {}
    prim_rec: dict[tuple, dict] = {}
    for backend, tabla in itertools.product(BACKENDS, TABLAS):
        prim_gen[(backend, tabla)] = {g: primitivos(seqs[g], backend, tabla) for g in GENES}
        prim_rec[(backend, tabla)] = {
            nom: primitivos(bicc[ini - 1:fin], backend, tabla)
            for nom, (ini, fin) in REGIONES.items()}
        print("primitivos listos: %s / %s" % (backend, tabla), flush=True)

    verificar_vectorizacion(prim_gen[("vienna", "NN3")]["BicC_Dm"], "BicC_Dm gen vienna/NN3")
    verificar_vectorizacion(prim_rec[("vienna", "NN3")][FOCO], "BicC_Dm %s recorte" % FOCO)

    anc = anclas(prim_gen)
    print("anclas OK: gen entero %d/%d, regiones vigentes %s"
          % (sum(v["coincide"] for v in anc["gen_entero"].values()), len(anc["gen_entero"]),
             anc["regiones_vigentes"]["coincide"]), flush=True)

    # -- la grilla ---------------------------------------------------------------------
    filas = []
    for backend, tabla, modo, e, a in itertools.product(BACKENDS, TABLAS, MODOS,
                                                        END_GRID, ACC_GRID):
        base = {"backend": backend, "tabla_nn": tabla, "modo": modo, "end_thr": e,
                "access_thr": a, "es_defecto": int(e == DEF_END and a == DEF_ACC)}
        eff_gen = eficientes(prim_gen[(backend, tabla)]["BicC_Dm"], modo, e, a)
        f_ctx = dict(base, marco="contexto", n_eficientes_gen=int(eff_gen.sum()))
        f_rec = dict(base, marco="recorte", n_eficientes_gen=int(eff_gen.sum()))
        f_sb = dict(base, marco="recorte_sin_bordes", n_eficientes_gen=int(eff_gen.sum()))
        for nom, (ini, fin) in REGIONES.items():
            f_ctx[nom] = int(eff_gen[ini - 1:fin].sum())
            eff_rec = eficientes(prim_rec[(backend, tabla)][nom], modo, e, a)
            f_rec[nom] = int(eff_rec.sum())
            f_sb[nom] = int(eff_rec[2:].sum())
        filas.extend([f_ctx, f_rec, f_sb])

    cols = ["backend", "tabla_nn", "modo", "end_thr", "access_thr", "es_defecto", "marco",
            "n_eficientes_gen"] + list(REGIONES)
    with (SALIDA / "grilla_parametros.tsv").open("w", encoding="utf-8") as fh:
        fh.write("\t".join(cols) + "\n")
        for f in filas:
            fh.write("\t".join(str(f[c]) for c in cols) + "\n")
    print("grilla escrita: %d filas (%d configuraciones por marco)"
          % (len(filas), len(filas) // 3), flush=True)

    # -- fracciones por eje y en conjunto ------------------------------------------------
    cortes = {"en conjunto": None}
    for m in MODOS:
        cortes["modo = %s" % m] = (lambda f, m=m: f["modo"] == m)
    for t in TABLAS:
        cortes["tabla = %s" % t] = (lambda f, t=t: f["tabla_nn"] == t)
    for b in BACKENDS:
        cortes["motor = %s" % b] = (lambda f, b=b: f["backend"] == b)
    cortes["brecha = 1,0 (defecto)"] = lambda f: f["end_thr"] == DEF_END
    cortes["accesibilidad = 0,1 (defecto)"] = lambda f: f["access_thr"] == DEF_ACC
    cortes["punto por defecto"] = lambda f: f["es_defecto"] == 1

    res = {"motor": {"vienna": "ViennaRNA 2.7.2",
                     "exe": "RNAplfold 2.1.5 (el del si-Fi original)" if HAY_EXE
                            else "NO CORRIDO (falta SIFI_RNAPLFOLD); no es un cero medido"},
           "grilla": {"end_thr": [END_GRID[0], END_GRID[-1]],
                      "access_thr": [ACC_GRID[0], ACC_GRID[-1]],
                      "modos": MODOS, "tablas": TABLAS, "backends": BACKENDS,
                      "configuraciones": len(filas) // 3},
           "regiones": {k: list(v) for k, v in REGIONES.items()},
           "anclas": anc, "fracciones": {}, "conteos_en_defecto": {}}
    for marco in ("contexto", "recorte", "recorte_sin_bordes"):
        res["fracciones"][marco] = {nombre: fraccion(filas, marco, filtro)
                                    for nombre, filtro in cortes.items()}
    for f in filas:
        if f["es_defecto"]:
            res["conteos_en_defecto"]["%s/%s/%s/%s" % (f["backend"], f["tabla_nn"],
                                                       f["modo"], f["marco"])] = {
                k: f[k] for k in REGIONES}
    (SALIDA / "fracciones_parametros.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

    for marco in ("contexto", "recorte"):
        c = res["fracciones"][marco]["en conjunto"]
        print("%s: sobre %d configuraciones, %s gana a 2121-2420 en %.1f%% y a 264-563 en "
              "%.1f%%; a los dos a la vez %.1f%%"
              % (marco, c["configuraciones"], FOCO, c["vs_2121-2420"]["gana_pct"],
                 c["vs_264-563"]["gana_pct"], c["gana_a_los_dos_pct"]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
