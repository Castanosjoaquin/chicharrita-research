"""Verificaciones de `ejes_separados.py`, el modulo de D47.

Tres clases de prueba:

- **El codigo no puede combinar los dos ejes.** Toda operacion entre un eje de
  exposicion y uno de conservacion levanta `TypeError`, y tambien `float()`. Es la
  verificacion que pide el issue #9: «prohibir en el codigo que se combinen en uno».
- **Invariancia.** Mover el vector de conservacion —ponerlo en cero, multiplicarlo por
  siete, dárselo a otra referencia— no cambia **ni un digito** del orden ni de los
  puntajes. Esta es la prueba fuerte: la barrera sintactica se puede esquivar
  escribiendo los dos nombres a proposito, la invariancia dice que el motor no lo hace.
- **Anclas con datos**, que necesitan `work/sifi_v2/` (no se versiona). Con el vector de
  exposicion igual a los pesos de D18 sin partir, el eje de exposicion reproduce exacto
  el numero que publica `ranking_v2.json`. Si los insumos no estan, se saltean y se dice.

    python tools/sifi21_port/test_ejes_separados.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import ejes_separados as E        # noqa: E402
import ranking as R               # noqa: E402
import ranking_v2 as V            # noqa: E402

FALLAS, SALTEADAS = [], []
TRABAJO = RAIZ / "work" / "sifi_v2"
PUBLICADO = RAIZ / "research/ola3/C7_ranking_v2/resultados/ranking_v2.json"
HV = "GCF_021130785.1_UT_GWSS_2.1_rna"


def check(cond, msg):
    print("  %s %s" % ("ok  " if cond else "FALLA", msg))
    if not cond:
        FALLAS.append(msg)


def levanta(fn, msg):
    try:
        fn()
    except TypeError:
        check(True, msg)
        return
    except Exception as ex:                                   # pragma: no cover
        check(False, "%s (levanto %s, no TypeError)" % (msg, type(ex).__name__))
        return
    check(False, "%s (NO levanto)" % msg)


# ------------------------------------------------- 1. los dos ejes no se combinan

def test_operaciones_entre_ejes_distintos():
    print("\nlas operaciones entre los dos ejes estan prohibidas")
    a, b = E.Eje("exposicion", 0.07), E.Eje("conservacion", 0.31)
    levanta(lambda: a + b, "exposicion + conservacion")
    levanta(lambda: a - b, "exposicion - conservacion")
    levanta(lambda: a * b, "exposicion * conservacion")
    levanta(lambda: a / b, "exposicion / conservacion")
    levanta(lambda: a < b, "exposicion < conservacion")
    levanta(lambda: a >= b, "exposicion >= conservacion")
    levanta(lambda: sum([a, b]), "sum([exposicion, conservacion])")
    levanta(lambda: sorted([a, b]), "sorted([exposicion, conservacion])")
    levanta(lambda: max(a, b), "max(exposicion, conservacion)")
    levanta(lambda: a + 0.5, "exposicion + un numero suelto")
    check(a != b, "un eje nunca es igual a otro de distinto nombre")


def test_no_se_pueden_colapsar_a_numero():
    print("\nun eje no se deja colapsar a un numero sin unidad")
    a = E.Eje("exposicion", 0.07)
    levanta(lambda: float(a), "float(eje)")
    levanta(lambda: int(a), "int(eje)")
    levanta(lambda: [0, 1][a], "usar el eje como indice")
    levanta(lambda: a.valor_de("conservacion"), "pedir el valor con el nombre del otro eje")
    check(a.valor_de("exposicion") == 0.07, "el valor sale nombrando su propio eje")


def test_operaciones_dentro_del_mismo_eje():
    print("\ndentro de un mismo eje las operaciones si estan definidas")
    a, b = E.Eje("exposicion", 0.2), E.Eje("exposicion", 0.5)
    check((a + b).valor_de("exposicion") == 0.7, "dos exposiciones se suman")
    check((b * 2).valor_de("exposicion") == 1.0, "una exposicion se escala por un numero")
    check(a < b, "dos exposiciones se comparan")
    check(sorted([b, a])[0] == a, "una lista de exposiciones se ordena")


def test_doseejes_no_se_colapsa():
    print("\nel par de una region no se colapsa ni se itera")
    d = E.DosEjes(E.Eje("exposicion", 0.07), E.Eje("conservacion", 0.31), {})
    levanta(lambda: float(d), "float(DosEjes)")
    levanta(lambda: list(d), "iterar DosEjes")
    levanta(lambda: d.exposicion + d.conservacion, "sumar los dos campos")
    check(d.como_par() == (0.07, 0.31), "como_par() devuelve los dos numeros, separados")
    check(not hasattr(d, "total") and not hasattr(d, "puntaje"),
          "DosEjes no tiene ningun metodo que devuelva un solo numero")


def test_los_dos_vectores_son_disjuntos():
    print("\nlos dos vectores de peso de la propuesta no se pisan")
    w, s = E.vector_exposicion(), E.vector_conservacion()
    cruce = [r for r in w if w[r] > 0 and s[r] > 0]
    check(not cruce, "ninguna referencia tiene peso en los dos ejes a la vez")
    check(s[HV] == 1.00 and w[HV] == 0.00,
          "H. vitripennis: conservacion 1,00 y exposicion 0,00 en la propuesta")
    cicadelidos = [r for r, d in E.PANEL_EJES.items() if d["s_conservacion"] > 0]
    check(cicadelidos == [HV], "el unico cicadelido no objetivo del panel es H. vitripennis")


# ----------------------------------------------------------------- 2. invariancia

def _cands_y_genes():
    V.con_panel(sin_humano=False)
    genes = V.cargar(TRABAJO, 21, V.GENES_EPILAB + V.GENES_NUEVOS)
    pub = json.loads(PUBLICADO.read_text(encoding="utf-8"))["k"]["21"]["regiones"]
    cands = []
    for c in list(R.CANDIDATOS) + V.NUEVOS:
        d = dict(c)
        d["region"] = tuple(int(x) for x in pub[d["gen"]].split("-"))
        cands.append(d)
    return cands, genes, pub


def test_invariancia_del_eje_de_conservacion():
    print("\nmover el eje de conservacion no mueve el orden (prueba fuerte)")
    if not TRABAJO.exists():
        SALTEADAS.append("invariancia (falta work/sifi_v2)")
        print("  SALTEADA: falta %s" % TRABAJO)
        return
    cands, genes, _ = _cands_y_genes()
    w = E.vector_exposicion()
    salidas = []
    for s in (E.vector_conservacion(),
              {r: 0.0 for r in E.PANEL_EJES},
              {r: 7.0 * v for r, v in E.vector_conservacion().items()},
              {r: 1.0 for r in E.PANEL_EJES}):
        r = E.barrer_exposicion(cands, genes, w, "geometrica", False, 300,
                                np.random.default_rng(7), "absoluta")
        pc = {"perfecto_21": 1.0, "perfecto_ge19": 0.6, "mm1_21": 0.3}
        ejes = [E.dos_ejes(genes, c, w, s, pc).exposicion.valor_de("exposicion")
                for c in cands]
        salidas.append((json.dumps(r, sort_keys=True), ejes))
    check(len({x[0] for x in salidas}) == 1,
          "el barrido es identico con cuatro vectores de conservacion distintos")
    check(len({tuple(x[1]) for x in salidas}) == 1,
          "el eje de exposicion de las seis regiones es identico con los cuatro")
    s0, s7 = (E.vector_conservacion(), {r: 7.0 * v for r, v in E.vector_conservacion().items()})
    pc = {"perfecto_21": 1.0, "perfecto_ge19": 0.6, "mm1_21": 0.3}
    c0 = [E.dos_ejes(genes, c, w, s0, pc).conservacion.valor_de("conservacion") for c in cands]
    c7 = [E.dos_ejes(genes, c, w, s7, pc).conservacion.valor_de("conservacion") for c in cands]
    check(c0 == c7, "y el eje de conservacion es invariante a la escala de su propio vector")


# ------------------------------------------------------------- 3. anclas con datos

def test_ancla_contra_el_motor_de_hoy():
    print("\ncon los pesos de D18 sin partir, el eje de exposicion es el numero publicado")
    if not TRABAJO.exists() or not PUBLICADO.exists():
        SALTEADAS.append("ancla D18 (falta work/sifi_v2)")
        print("  SALTEADA: falta %s" % TRABAJO)
        return
    cands, genes, _ = _cands_y_genes()
    pub = json.loads(PUBLICADO.read_text(encoding="utf-8"))["k"]["21"]
    w_d18 = E.vector_exposicion(tau_hv=0.60)       # el vector unico de D18
    s = E.vector_conservacion()
    _, wc = R.pesos_base()
    ok = 0
    for c in cands:
        d = E.dos_ejes(genes, c, w_d18, s, wc)
        esperado = next(f for f in pub["fichas"] if f["gen"] == c["gen"])["conservadora"]
        mio = round(d.exposicion.valor_de("exposicion"), 4)
        if mio == round(esperado["exposicion"], 4):
            ok += 1
        else:
            print("    %s: %s contra %s publicado" % (c["gen"], mio, esperado["exposicion"]))
    check(ok == len(cands), "las seis exposiciones reproducen ranking_v2.json (%d/%d)"
          % (ok, len(cands)))


def test_veto_con_exposicion_cero():
    print("\nel veto con exposicion cero deja de ser veto")
    if not TRABAJO.exists():
        SALTEADAS.append("veto (falta work/sifi_v2)")
        print("  SALTEADA: falta %s" % TRABAJO)
        return
    cands, genes, _ = _cands_y_genes()
    por_gen = {c["gen"]: c for c in cands}
    for gen, region in (("BicC_Dm", (264, 563)), ("ATPaseD_Dm", (151, 450))):
        excl = R.excluidas_de(por_gen[gen], "off")
        hoy = E.veto(genes[gen], region[0], region[1], None, excl)
        con_cero = E.veto(E.vista(genes, E.vector_exposicion())[gen], region[0], region[1],
                          E.vector_exposicion(), excl)
        check(hoy, "%s %d-%d esta vetada con la regla de hoy" % (gen, *region))
        check(not con_cero, "%s %d-%d deja de estarlo con exposicion cero en H. vitripennis"
              % (gen, *region))


def main() -> int:
    for t in (test_operaciones_entre_ejes_distintos, test_no_se_pueden_colapsar_a_numero,
              test_operaciones_dentro_del_mismo_eje, test_doseejes_no_se_colapsa,
              test_los_dos_vectores_son_disjuntos,
              test_invariancia_del_eje_de_conservacion, test_ancla_contra_el_motor_de_hoy,
              test_veto_con_exposicion_cero):
        t()
    print()
    if SALTEADAS:
        print("SALTEADAS %d: %s" % (len(SALTEADAS), ", ".join(SALTEADAS)))
    if FALLAS:
        print("FALLARON %d verificaciones" % len(FALLAS))
        return 1
    print("todas las verificaciones pasaron")
    return 0


if __name__ == "__main__":
    sys.exit(main())
