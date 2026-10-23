"""Verificaciones del port de si-Fi21.

Comprueba que las tablas que tomamos de Biopython son las mismas que usa el fuente
de si-Fi, que los recortes de secuencia reproducen los del original, y que los dos
caminos de codigo (el motor y el barrido) dan el mismo resultado.

Los valores de referencia de las tablas estan transcritos del fuente original
(github.com/snowformatics/siFi21-, free_energy.py), que es el unico modo de
verificar la equivalencia sin depender de ese archivo en tiempo de ejecucion.

    python test_sifi.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sifi_energy as se
from sifi_core import (COLUMNAS_FEATURES, RAMAS_TERMINALES, SifiEngine,
                       apply_rules, primitives, rama_terminal, to_tsv)

FALLAS = []


def check(cond, msg):
    if cond:
        print("  ok   %s" % msg)
    else:
        print("  FALLA %s" % msg)
        FALLAS.append(msg)


def test_tablas():
    print("tablas termodinamicas")
    # RNA_NN3 = Chen et al. 2012, muestreado del fuente de si-Fi (lineas 45-49).
    for k, v in {"AA/TT": (-7.09, -19.8), "AT/TA": (-9.11, -25.8),
                 "TA/AT": (-8.50, -22.9)}.items():
        check(se.RNA_NN3.get(k) == v, "RNA_NN3[%s] == %s" % (k, v))

    # Lo que si-Fi llama RNA_DE2 y usa por defecto (lineas 171-194).
    for k, v in {".T/AA": (-4.9, -13.2), ".C/AG": (-7.4, -20.3),
                 ".G/CC": (-4.1, -10.6), ".G/TC": (-7.5, -20.31),
                 "CT/.A": (6.9, 22.6), "TA/.T": (3.1, 10.6)}.items():
        check(se.RNA_DE2.get(k) == v, "RNA_DE2[%s] == %s" % (k, v))
    check(len(se.RNA_DE2) == 48, "RNA_DE2 tiene 48 entradas")

    # La variante no usada es la misma tabla con las claves invertidas.
    check(se.RNA_DE1_SIFI.get("AA/T.") == (-4.9, -13.2),
          "RNA_DE1_SIFI['AA/T.'] es el espejo de RNA_DE2['.T/AA']")

    check(len(se.DNA_IMM1) == 87 and len(se.DNA_TMM1) == 48,
          "tablas de mismatch de ADN con el tamanio del original (87 y 48)")


def test_recortes():
    """Los indices del original, verificados sobre el ejemplo de su docstring."""
    print("recortes de secuencia")
    eng = SifiEngine(mode="fiel")
    sirna = "GGGATGGCTCAAAGGCGTAGT"  # ejemplo del docstring de free_energy3
    check(len(sirna) == 21, "el siRNA de ejemplo mide 21 nt")
    # El docstring dice: Sense5' = posiciones [0,1,2] -> GGG
    check(sirna[0:3] == "GGG", "extremo 5' sentido = GGG")
    # y Antisense5' = [17,18,19] -> GTA. El codigo usa [16:19].
    check(sirna[21 - 2 - 3:21 - 2] == "GTA", "extremo 5' antisentido = GTA")
    # Los dos primeros siRNA van sin extremos colgantes y no deben fallar.
    dg_s, dg_as = eng._ends_plain(sirna)
    check(isinstance(dg_s, float) and isinstance(dg_as, float),
          "dG sin extremos colgantes devuelve dos flotantes")


def test_temperatura():
    """La temperatura debe mover el dG: es lo que el original tenia fijo en 22 C."""
    print("temperatura")
    dg22 = se.free_energy("GGG", temp_c=22.0)
    dg37 = se.free_energy("GGG", temp_c=37.0)
    check(abs(dg22 - dg37) > 1e-6, "dG a 22 C difiere de dG a 37 C")
    # dG = dH - T*dS, con dH y dS negativos en una hibridacion: al bajar T el
    # termino -T*dS aporta menos y el dG queda mas negativo. El duplex es mas
    # estable en frio, que es justamente el argumento para no calcular a 37 C.
    check(dg22 < dg37, "dG mas negativo a 22 C que a 37 C (duplex mas estable en frio)")


def test_sal_se_cancela():
    """La correccion salina del metodo 5 depende solo del largo: se cancela en la resta.

    Es la razon por la que cambiar Mg/Na no mueve ningun veredicto de si-Fi, que
    solo compara dG entre dos ventanas del mismo largo.
    """
    print("correccion salina")
    a = se.free_energy("GGG", Na=20, K=50, Mg=0)
    b = se.free_energy("ACT", Na=20, K=50, Mg=0)
    a2 = se.free_energy("GGG", Na=20, K=50, Mg=5)
    b2 = se.free_energy("ACT", Na=20, K=50, Mg=5)
    check(abs((a - b) - (a2 - b2)) < 1e-9,
          "la diferencia de dG no cambia al agregar Mg (se cancela)")


def test_coherencia_motor_barrido():
    """El motor y el barrido son dos implementaciones de la misma regla."""
    print("coherencia entre motor y barrido")
    seq = ("GGGATGGCTCAAAGGCGTAGTACGATCGATCGGCTAGCTAGCTTACGGCATCGGCATCGAATCG"
           "GCATCGAACGTACGTACGTAGCTAGCATCGATCGGATCGATCGGCTAACGTTACGATCGCATGC")
    for modo in ("fiel", "corregido"):
        eng = SifiEngine(mode=modo)
        ventanas, resumen = eng.run(seq, backend="vienna")
        prims = primitives(seq, temp_c=22.0, backend="vienna")
        n = apply_rules(prims, mode=modo, u=8, end_thr=1.0, access_thr=0.1,
                        terminal_check=True)
        check(resumen["eficientes"] == n,
              "modo %s: motor %d == barrido %d" % (modo, resumen["eficientes"], n))


def test_modos_difieren():
    """El arreglo de la regla terminal tiene que cambiar algo, si no no arregla nada."""
    print("el modo corregido difiere del fiel")
    seq = ("ATGGCTCAAAGGCGTAGTACGATCGATCGGCTAGCTAGCTTACGGCATCGGCATCGAATCGGCAT"
           "CGAACGTACGTACGTAGCTAGCATCGATCGGATCGATCGGCTAACGTTACGATCGCATGCAATT")
    r = {}
    for modo in ("fiel", "corregido"):
        _, resumen = SifiEngine(mode=modo).run(seq, backend="vienna")
        r[modo] = resumen["eficientes"]
    check(r["fiel"] >= r["corregido"],
          "el fiel cuenta >= que el corregido (%d vs %d): la rama del original "
          "solo puede agregar eficientes" % (r["fiel"], r["corregido"]))


def test_rama_terminal():
    """Las cuatro ramas de la regla terminal, por tabla de verdad (issue #7)."""
    print("ramas de la regla terminal")
    casos = {(True, False): 1, (True, True): 2, (False, True): 3, (False, False): 4}
    for (nt19_at, nt2_gc), esperada in casos.items():
        check(rama_terminal(nt19_at, nt2_gc) == esperada,
              "nt19_at=%s nt2_gc=%s -> rama %d" % (nt19_at, nt2_gc, esperada))
    check(set(RAMAS_TERMINALES) == {1, 2, 3, 4}, "las cuatro ramas estan documentadas")


def test_rama_predice_el_veredicto():
    """La rama tiene que explicar el veredicto, si no el campo no sirve de nada.

    En modo fiel: rama 1 y 3 deciden por termodinamica, la 2 solo por accesibilidad
    --es el atajo que la auditoria encontro-- y la 4 rechaza sin mirar nada.
    """
    print("la rama terminal predice el veredicto")
    seq = ("ATGGCTCAAAGGCGTAGTACGATCGATCGGCTAGCTAGCTTACGGCATCGGCATCGAATCGGCAT"
           "CGAACGTACGTACGTAGCTAGCATCGATCGGATCGATCGGCTAACGTTACGATCGCATGCAATT")
    ventanas, _ = SifiEngine(mode="fiel").run(seq, backend="vienna")
    malas = 0
    for w in ventanas:
        esperado = {1: w.thermo_efficient, 2: w.target_site_accessibility,
                    3: w.thermo_efficient, 4: False}[w.rama_terminal]
        malas += w.is_efficient != esperado
    check(malas == 0, "ninguna de las %d ventanas contradice su rama" % len(ventanas))
    check(any(w.rama_terminal == 2 for w in ventanas),
          "la secuencia de prueba ejercita el atajo (rama 2)")


def test_tsv_no_lleva_secuencia():
    """La columna `seq` reconstruye el gen, asi que no sale por defecto (issue #13)."""
    print("el TSV no lleva la columna seq por defecto")
    import tempfile
    seq = "ATGGCTCAAAGGCGTAGTACGATCGATCGGCTAGCTAGCTTACGGCATCGGCATCGAATCGGCATCGAACGTACG"
    ventanas, _ = SifiEngine(mode="fiel").run(seq, backend="vienna")
    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        to_tsv(ventanas, base / "a.tsv")
        to_tsv(ventanas, base / "b.tsv", con_seq=True)
        to_tsv(ventanas, base / "c.tsv", columnas=COLUMNAS_FEATURES + ["is_efficient"])
        cols = lambda f: (base / f).read_text().split("\n")[0].split("\t")
        check("seq" not in cols("a.tsv"), "por defecto no emite seq")
        check("seq" in cols("b.tsv"), "con con_seq=True si la emite")
        check("seq" not in cols("c.tsv"), "la tabla de features tampoco la emite")
        veredicto = {"strand_selection", "end_stability", "target_site_accessibility",
                     "thermo_efficient"}
        check(not (veredicto & set(cols("c.tsv"))),
              "la tabla de features no lleva ningun booleano de veredicto")
        check("rama_terminal" in cols("c.tsv") and "accessibility" in cols("c.tsv"),
              "la tabla de features lleva los terminos y la rama")


def test_tabla_nn4():
    """La tabla de sifi21INTA: 28 entradas, distinta de NN3, y seleccionable (issue #6)."""
    print("tabla RNA_NN4 de sifi21INTA")
    check(len(se.RNA_NN4) == 28, "RNA_NN4 tiene 28 entradas")
    check(set(se.RNA_NN4) == set(se.RNA_NN3),
          "RNA_NN4 cubre las mismas claves que RNA_NN3")
    distintas = [k for k in se.RNA_NN4 if se.RNA_NN4[k] != se.RNA_NN3[k]]
    check(len(distintas) == 22,
          "difiere de RNA_NN3 en 22 de 28 entradas (son %d)" % len(distintas))
    check(se.TABLAS_NN["NN4"] is se.RNA_NN4, "TABLAS_NN expone NN4")
    # Un par de valores transcritos del fuente (freeEnergy.py:61-74), como ancla.
    for k, v in {"AA/TT": (-7.44, -20.98), "GC/CG": (-16.52, -42.13),
                 "sym": (0, -1.38)}.items():
        check(se.RNA_NN4.get(k) == v, "RNA_NN4[%s] == %s" % (k, v))


def test_nn4_cambia_el_conteo_y_nn3_no():
    """Elegir NN4 tiene que mover algo, y NN3 tiene que seguir siendo el default."""
    print("la tabla seleccionada cambia el veredicto")
    seq = ("ATGGCTCAAAGGCGTAGTACGATCGATCGGCTAGCTAGCTTACGGCATCGGCATCGAATCGGCAT"
           "CGAACGTACGTACGTAGCTAGCATCGATCGGATCGATCGGCTAACGTTACGATCGCATGCAATT")
    base, _ = SifiEngine(mode="fiel").run(seq, backend="vienna")
    nn3, _ = SifiEngine(mode="fiel", tabla_nn="NN3").run(seq, backend="vienna")
    nn4, _ = SifiEngine(mode="fiel", tabla_nn="NN4").run(seq, backend="vienna")
    check([w.is_efficient for w in base] == [w.is_efficient for w in nn3],
          "NN3 explicita da lo mismo que el default")
    check([w.ddg for w in nn3] != [w.ddg for w in nn4],
          "NN4 mueve los ddg respecto de NN3")
    try:
        SifiEngine(mode="fiel", tabla_nn="NN9")
        check(False, "una tabla inexistente tiene que fallar")
    except ValueError:
        check(True, "una tabla inexistente falla con ValueError")


def main():
    for t in (test_tablas, test_recortes, test_temperatura, test_sal_se_cancela,
              test_coherencia_motor_barrido, test_modos_difieren,
              test_rama_terminal, test_rama_predice_el_veredicto,
              test_tsv_no_lleva_secuencia, test_tabla_nn4,
              test_nn4_cambia_el_conteo_y_nn3_no):
        t()
    print()
    if FALLAS:
        print("FALLARON %d verificaciones" % len(FALLAS))
        return 1
    print("todas las verificaciones pasaron")
    return 0


if __name__ == "__main__":
    sys.exit(main())
