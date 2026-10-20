"""Verificaciones de `ranking.py`.

Dos clases de prueba, y la distincion importa:

- **Propiedades del criterio**, que no dependen de ningun dato: que los criterios
  anidados no se cuenten tres veces, que la media geometrica castigue un eje cerca
  de cero donde la suma lo compensa, que el veto sea monotono, y que el barrido
  sortee pesos de criterio en orden decreciente.
- **Anclas contra numeros ya publicados**, que si dependen de los TSV de
  `work/sifi_check/`. Son las que impiden que un cambio de convencion mueva en
  silencio un numero citado en `sifi21_reproduccion.md` §2 y §3. Si los TSV no
  estan —`work/` queda fuera del control de versiones— se saltean y se dice.

    python test_ranking.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ranking as R
from sifi_core import best_region

FALLAS = []
SALTEADAS = []


def check(cond, msg):
    if cond:
        print("  ok   %s" % msg)
    else:
        print("  FALLA %s" % msg)
        FALLAS.append(msg)


def _gen_falso(n, eficientes, riesgo=None):
    """Un gen sintetico: n ventanas, `eficientes` posiciones 1-indexadas marcadas."""
    efi = np.zeros(n, dtype=bool)
    efi[[p - 1 for p in eficientes]] = True
    g = {"gen": "falso", "n": n, "eficiente": efi,
         "presente": np.ones(n, dtype=bool), "riesgo": {}}
    for ref, por_crit in (riesgo or {}).items():
        g["riesgo"][ref] = {}
        for crit in R.CRITERIOS:
            v = np.zeros(n, dtype=bool)
            v[[p - 1 for p in por_crit.get(crit, [])]] = True
            g["riesgo"][ref][crit] = v
    return g


# --------------------------------------------------------- propiedades sin datos

def test_conteo_por_region():
    print("conteo por region: la convencion es por posicion de INICIO")
    marca = np.zeros(10, dtype=bool)
    marca[[0, 1, 5]] = True            # posiciones 1, 2 y 6
    c = R.conteo_por_region(marca, 3)
    check(len(c) == 8, "con n=10 y L=3 hay 8 regiones, no 10 (%d)" % len(c))
    check(c[0] == 2, "la region 1-3 cuenta las marcas en 1 y 2 (%d)" % c[0])
    check(c[3] == 1, "la region 4-6 cuenta solo la marca en 6 (%d)" % c[3])
    check(c[6] == 0, "la region 7-9 no cuenta ninguna (%d)" % c[6])
    check(int(c.max()) == 2, "el maximo es 2")


def test_conteo_coincide_con_best_region():
    """La convencion tiene que ser la MISMA que la de `sifi_core.best_region`.

    Es lo que hace que el percentil de T1 sea comparable con los conteos de
    `sifi21_reproduccion.md` §3, que salieron de `best_region`.
    """
    print("la convencion coincide con sifi_core.best_region")

    class W:
        def __init__(self, pos, ef):
            self.pos, self.is_efficient = pos, ef

    rng = np.random.default_rng(3)
    for largo in (50, 200):
        n = 600
        efi = rng.random(n) < 0.1
        ventanas = [W(i + 1, bool(efi[i])) for i in range(n)]
        esperado = best_region(ventanas, largo)
        c = R.conteo_por_region(efi, largo)
        check(int(c.max()) == esperado["eficientes"],
              "L=%d: el maximo coincide (%d vs %d)"
              % (largo, int(c.max()), esperado["eficientes"]))
        check(int(np.argmax(c)) + 1 == esperado["inicio"],
              "L=%d: el argmax coincide (%d vs %d)"
              % (largo, int(np.argmax(c)) + 1, esperado["inicio"]))


def test_criterios_no_se_suman():
    """Un 21-mero perfecto contiene bloques de 19: contar los tres seria triplicar."""
    print("los criterios anidados cuentan una vez, no tres")
    g = _gen_falso(5, [], riesgo={"ref": {"perfecto_21": [3], "perfecto_ge19": [3],
                                          "mm1_21": [3]}})
    pr, pc = {"ref": 1.0}, {"perfecto_21": 1.0, "perfecto_ge19": 0.6, "mm1_21": 0.3}
    riesgo = R.peso_por_ventana(g, pr, pc, set())
    check(abs(riesgo[2] - 1.0) < 1e-9,
          "la ventana con los tres criterios vale 1,0 y no 1,9 (%.4f)" % riesgo[2])
    check(riesgo.sum() == riesgo[2], "ninguna otra ventana aporta riesgo")


def test_riesgo_es_el_peor_acierto():
    """Entre referencias se toma el maximo: seis aciertos leves no son uno grave."""
    print("entre referencias el riesgo es el peor acierto, no la suma")
    leves = _gen_falso(3, [], riesgo={"a": {"mm1_21": [1]}, "b": {"mm1_21": [1]},
                                      "c": {"mm1_21": [1]}})
    grave = _gen_falso(3, [], riesgo={"a": {"perfecto_21": [1]}})
    pr = {"a": 1.0, "b": 1.0, "c": 1.0}
    pc = {"perfecto_21": 1.0, "perfecto_ge19": 0.6, "mm1_21": 0.3}
    r_leves = R.peso_por_ventana(leves, pr, pc, set())[0]
    r_grave = R.peso_por_ventana(grave, pr, pc, set())[0]
    check(abs(r_leves - 0.3) < 1e-9,
          "tres aciertos de un desajuste valen 0,3 y no 0,9 (%.4f)" % r_leves)
    check(r_grave > r_leves,
          "un 21/21 perfecto pesa mas que tres de un desajuste (%.2f > %.2f)"
          % (r_grave, r_leves))


def test_geometrica_castiga_el_eje_bajo():
    """La afirmacion de D1: la suma compensa y la media geometrica no."""
    print("media geometrica contra suma ponderada")
    # El desbalanceado suma un poco mas (0,305 contra 0,295) y lo consigue con una
    # limpieza de 0,01: es exactamente el caso que §5 del pipeline queria evitar.
    equilibrado = {"eficacia": 0.09, "limpieza": 0.50, "buenos_limpios": 0,
                   "vetada": False}
    desbalanceado = {"eficacia": 0.60, "limpieza": 0.01, "buenos_limpios": 0,
                     "vetada": False}
    s_eq = R.puntaje(equilibrado, 0.5, "suma")
    s_des = R.puntaje(desbalanceado, 0.5, "suma")
    g_eq = R.puntaje(equilibrado, 0.5, "geometrica")
    g_des = R.puntaje(desbalanceado, 0.5, "geometrica")
    check(s_des > s_eq, "por suma gana el desbalanceado (%.4f > %.4f)" % (s_des, s_eq))
    check(g_eq > g_des,
          "por media geometrica gana el equilibrado (%.4f > %.4f)" % (g_eq, g_des))


def test_veto_es_monotono():
    """Ninguna region vetada puede quedar arriba de una no vetada."""
    print("el veto de la cascada es duro, no una penalizacion")
    vetada = {"eficacia": 1.0, "limpieza": 1.0, "buenos_limpios": 999, "vetada": True}
    pobre = {"eficacia": 0.0, "limpieza": 0.0, "buenos_limpios": 0, "vetada": False}
    check(R.puntaje(pobre, 0.5, "cascada") > R.puntaje(vetada, 0.5, "cascada"),
          "la region sin un solo eficiente limpio supera a la vetada con 999")


def test_minmax_con_dos_candidatos_es_degenerado():
    """Con dos candidatos el min-max tira toda la magnitud: no es un hallazgo.

    Queda como prueba para que nadie lea el 50/50 del barrido por estrategia como
    si fuera un empate medido. Es la escala la que lo produce.
    """
    print("min-max con dos candidatos es degenerado")
    a = {"eficacia": 0.150, "limpieza": 0.980}
    b = {"eficacia": 0.085, "limpieza": 0.993}
    norms = R.normalizar_conjunto([a, b])
    check(norms == [(1.0, 0.0), (0.0, 1.0)],
          "los dos ejes quedan en 0 y 1 cualquiera sea la magnitud (%s)" % (norms,))
    casi_iguales = R.normalizar_conjunto([
        {"eficacia": 0.150, "limpieza": 0.980},
        {"eficacia": 0.149, "limpieza": 0.981}])
    check(casi_iguales == norms,
          "una diferencia de 0,001 da el mismo resultado que una de 0,065")


def test_barrido_ordena_los_pesos_de_criterio():
    print("el barrido sortea pesos de criterio en orden decreciente")
    rng = np.random.default_rng(11)
    for _ in range(200):
        w_ef, wr, wc = R.sortear_pesos(rng)
        if not (wc["perfecto_21"] >= wc["perfecto_ge19"] >= wc["mm1_21"]):
            check(False, "orden violado: %s" % wc)
            return
        if not 0.0 <= w_ef <= 1.0:
            check(False, "w_ef fuera de [0,1]: %s" % w_ef)
            return
        if abs(sum(wr.values()) - 1.0) > 1e-9:
            check(False, "los pesos por referencia no suman 1: %s" % sum(wr.values()))
            return
    check(True, "200 sorteos con el orden 21 >= ge19 >= mm1 y los simplex bien")


def test_dmaidis_sale_como_ontarget():
    print("el genoma de D. maidis sale del riesgo de los genes del insecto")
    insecto = {"gen": "BicC_Dm", "region": (1, 10), "estrategia": "insecto"}
    viral = {"gen": "MP_MRFV", "region": (1, 10), "estrategia": "virus"}
    check(R.DMAIDIS in R.excluidas_de(insecto, "off"),
          "para un gen del insecto se excluye siempre")
    check(R.DMAIDIS not in R.excluidas_de(viral, "off"),
          "para un gen viral con --dmaidis-viral off entra como off-target")
    check(R.DMAIDIS in R.excluidas_de(viral, "neutro"),
          "para un gen viral con --dmaidis-viral neutro se excluye")


# ------------------------------------------- anclas contra numeros ya publicados

def _datos():
    perfil = Path("work/sifi_check/salida")
    off = Path("work/sifi_check/offtarget_full/offtarget_por_sirna.tsv")
    faltan = [str(p) for p in (perfil, off) if not p.exists()]
    if faltan:
        return None, faltan
    for c in R.CANDIDATOS:
        p = perfil / ("%s_full_corregido_vienna.tsv" % c["gen"])
        if not p.exists():
            return None, [str(p)]
    return (perfil, off), []


def test_anclas_publicadas():
    """Los conteos de `sifi21_reproduccion.md` §2 («en contexto») y §3 («mejor»)."""
    print("anclas contra los numeros publicados en sifi21_reproduccion.md")
    rutas, faltan = _datos()
    if rutas is None:
        print("  SALTEADA faltan %s (work/ no esta en el control de versiones)"
              % ", ".join(faltan))
        SALTEADAS.append("anclas publicadas")
        return
    perfil, off = rutas
    # §2, columna «en contexto»; §3, region elegida y mejor region del mismo largo.
    esperado = {
        "MP_MRFV":    {"elegida": 30, "mejor": 38, "ini_mejor": 72},
        "CP_MRFV":    {"elegida": 17, "mejor": 21, "ini_mejor": 99},
        "BicC_Dm":    {"elegida": 20, "mejor": 37, "ini_mejor": 2123},
        "ATPaseD_Dm": {"elegida": 18, "mejor": 24, "ini_mejor": 136},
    }
    # §0: los conteos del gen entero en modo corregido + ViennaRNA 2.7.2 (§1).
    gen_entero = {"MP_MRFV": 123, "CP_MRFV": 30, "BicC_Dm": 171, "ATPaseD_Dm": 29}
    for c in R.CANDIDATOS:
        g = R.cargar_gen(c["gen"], perfil, None, None)
        ini, fin = c["region"]
        largo = fin - ini + 1
        conteo = R.conteo_por_region(g["eficiente"], largo)
        e = esperado[c["gen"]]
        check(int(g["eficiente"].sum()) == gen_entero[c["gen"]],
              "%s: gen entero %d eficientes" % (c["gen"], gen_entero[c["gen"]]))
        check(int(conteo[ini - 1]) == e["elegida"],
              "%s: region elegida %d-%d tiene %d eficientes (§2 en contexto)"
              % (c["gen"], ini, fin, e["elegida"]))
        check(int(conteo.max()) == e["mejor"],
              "%s: la mejor region tiene %d eficientes (§3)" % (c["gen"], e["mejor"]))
        check(int(np.argmax(conteo)) + 1 == e["ini_mejor"],
              "%s: la mejor region arranca en %d (§3)" % (c["gen"], e["ini_mejor"]))


def test_ancla_offtarget_region():
    """Las ventanas con off-target de la region elegida, de §4.

    §4 usa solo el criterio de bloque perfecto >=19 nt, asi que la comparacion se
    hace con ese criterio y no con el de un desajuste, que se midio despues.
    """
    print("anclas del cruce con off-targets (§4, criterio de bloque >=19 nt)")
    rutas, faltan = _datos()
    if rutas is None:
        print("  SALTEADA faltan %s" % ", ".join(faltan))
        SALTEADAS.append("anclas off-target")
        return
    perfil, off = rutas
    esperado = {"MP_MRFV": 6, "CP_MRFV": 0, "BicC_Dm": 33, "ATPaseD_Dm": 7}
    for c in R.CANDIDATOS:
        g = R.cargar_gen(c["gen"], perfil, off, None)   # sin mm1: el criterio de §4
        ini, fin = c["region"]
        excluir = R.excluidas_de(c, "off")
        afectadas = np.zeros(g["n"], dtype=bool)
        for ref, crits in g["riesgo"].items():
            if ref in excluir:
                continue
            afectadas |= crits["perfecto_ge19"]
        n = int(afectadas[ini - 1:fin].sum())
        check(n == esperado[c["gen"]],
              "%s: %d ventanas con off-target en la region elegida (§4)"
              % (c["gen"], esperado[c["gen"]]))


def test_ancla_veto():
    """Cuales regiones elegidas caen bajo el veto duro, y cuales no.

    Es el numero del que depende D2: si el veto no cambiara nada, la decision no
    importaria.
    """
    print("el veto duro sobre las cuatro regiones elegidas")
    rutas, faltan = _datos()
    if rutas is None:
        print("  SALTEADA faltan %s" % ", ".join(faltan))
        SALTEADAS.append("ancla del veto")
        return
    perfil, off = rutas
    esperado = {"MP_MRFV": False, "CP_MRFV": False, "BicC_Dm": True,
                "ATPaseD_Dm": True}
    wr, wc = R.pesos_base()
    for c in R.CANDIDATOS:
        g = R.cargar_gen(c["gen"], perfil, off, None)
        e = R.ejes(g, c["region"][0], c["region"][1], wr, wc,
                   R.excluidas_de(c, "off"), False)
        check(e["vetada"] == esperado[c["gen"]],
              "%s: vetada = %s" % (c["gen"], esperado[c["gen"]]))


def main():
    for t in (test_conteo_por_region, test_conteo_coincide_con_best_region,
              test_criterios_no_se_suman, test_riesgo_es_el_peor_acierto,
              test_geometrica_castiga_el_eje_bajo, test_veto_es_monotono,
              test_minmax_con_dos_candidatos_es_degenerado,
              test_barrido_ordena_los_pesos_de_criterio,
              test_dmaidis_sale_como_ontarget,
              test_anclas_publicadas, test_ancla_offtarget_region, test_ancla_veto):
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
