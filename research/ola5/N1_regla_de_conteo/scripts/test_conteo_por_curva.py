"""Verificaciones de la funcion historica de conteo.

Tres grupos, y cada uno prueba algo distinto.

Los **sinteticos** fijan el mecanismo sin depender de ningun dato: dos ventanas eficientes
separadas por exactamente el ancho de cobertura cuentan una sola vez, y separadas por uno
mas o uno menos cuentan dos. Es el nucleo de lo que explica la carta del investigador, y se
puede construir a mano.

Los **invariantes** acotan la funcion por arriba y por abajo: nunca puede contar mas
ventanas de las que hay, ni menos tramos de los que tiene la curva. Un error de signo o un
recorte mal puesto rompen uno de los dos.

El **ancla real** es la que convierte la explicacion en medicion: con los cuatro genes de
EPILAB y la configuracion que reconstruye las curvas historicas, el ancho 20 da 114, 35,
199 y 33 —los cuatro de la planilla— y los anchos 19 y 21 **no** los dan. Si falta el
corpus local, el grupo se declara no corrido y no falla: `work/` no esta en git.

Uso:
    python research/ola5/N1_regla_de_conteo/scripts/test_conteo_por_curva.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
sys.path.insert(0, str(AQUI.parent))
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))

import conteo_por_curva as m

A = m.ANCHO_HISTORICO


class TestMecanismo(unittest.TestCase):
    """Los sinteticos: el mecanismo que describe la carta, caso por caso."""

    def test_sin_ventanas_eficientes_no_cuenta_nada(self):
        self.assertEqual(m.contar_por_incrementos([]), 0)

    def test_una_sola_ventana_cuenta_una(self):
        self.assertEqual(m.contar_por_incrementos([1]), 1)
        self.assertEqual(m.contar_por_incrementos([500]), 1)

    def test_dos_a_la_distancia_del_ancho_cuentan_una(self):
        """El caso de la carta: una termina y otra empieza, y los efectos se compensan."""
        self.assertEqual(m.contar_por_incrementos([10, 10 + A]), 1)
        self.assertEqual(m.tapadas([10, 10 + A]), [10 + A])

    def test_dos_a_una_posicion_de_distancia_del_ancho_cuentan_dos(self):
        """Es lo que hace al ancho identificable: con 19 o 21 el conteo es otro."""
        self.assertEqual(m.contar_por_incrementos([10, 10 + A - 1]), 2)
        self.assertEqual(m.contar_por_incrementos([10, 10 + A + 1]), 2)

    def test_una_corrida_contigua_cuenta_todos_sus_arranques(self):
        """Las ventanas se desplazan de a 1 nt, asi que cada arranque sube la curva.

        El bloque contiguo es el caso en que la funcion historica **no** pierde nada: la
        curva es una rampa y cada arranque es un incremento de +1. Lo que se pierde no es
        la contiguidad sino la distancia exacta del ancho.
        """
        self.assertEqual(m.contar_por_incrementos(list(range(100, 100 + A))), A)

    def test_una_corrida_mas_larga_que_el_ancho_se_corta_en_el_ancho(self):
        """Pasado el ancho, cada arranque nuevo tapa al de `ancho` posiciones antes."""
        self.assertEqual(m.contar_por_incrementos(list(range(100, 100 + A + 5))), A)
        self.assertEqual(m.tapadas(list(range(100, 100 + A + 5))),
                         list(range(100 + A, 100 + A + 5)))

    def test_el_ancho_es_un_parametro_y_no_el_tamano_del_sirna(self):
        """20 y 21 dan respuestas distintas sobre el mismo conjunto: es el hallazgo."""
        pos = [10, 10 + 20]
        self.assertEqual(m.contar_por_incrementos(pos, 20), 1)
        self.assertEqual(m.contar_por_incrementos(pos, 21), 2)

    def test_el_orden_y_las_repeticiones_no_cambian_el_conteo(self):
        self.assertEqual(m.contar_por_incrementos([30, 10, 30]),
                         m.contar_por_incrementos([10, 30]))

    def test_un_ancho_menor_a_uno_es_un_error(self):
        with self.assertRaises(ValueError):
            m.curva_de_cobertura([1], 10, 0)


class TestInvariantes(unittest.TestCase):
    """Las dos cotas, y que la curva y el conjunto dan lo mismo."""

    CASOS = ([], [1], [1, 2, 3], [10, 10 + A], [5, 25, 45, 46, 200],
             list(range(1, 60)), [1, 1 + A, 1 + 2 * A, 1 + 3 * A])

    def test_nunca_cuenta_mas_ventanas_de_las_que_hay(self):
        for pos in self.CASOS:
            self.assertLessEqual(m.contar_por_incrementos(pos), len(set(pos)), str(pos))

    def test_nunca_cuenta_menos_tramos_de_los_que_tiene_la_curva(self):
        for pos in self.CASOS:
            largo = (max(pos) if pos else 0) + 2 * A
            curva = m.curva_de_cobertura(pos, largo)
            self.assertGreaterEqual(m.contar_por_incrementos(pos), len(m.tramos(curva)),
                                    str(pos))

    def test_la_curva_y_el_conjunto_dan_el_mismo_numero(self):
        """La implementacion por conjunto no depende de donde se recorta la curva."""
        for pos in self.CASOS:
            for ancho in (19, A, 21):
                largo = (max(pos) if pos else 0) + 2 * ancho
                curva = m.curva_de_cobertura(pos, largo, ancho)
                self.assertEqual(m.suma_de_incrementos_positivos(curva),
                                 m.contar_por_incrementos(pos, ancho), str((pos, ancho)))

    def test_tapadas_es_exactamente_la_diferencia(self):
        for pos in self.CASOS:
            self.assertEqual(len(set(pos)) - m.contar_por_incrementos(pos),
                             len(m.tapadas(pos)), str(pos))


GENES = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]
FASTA = {g: RAIZ / "work" / "sifi_check" / f"{g}_full.fasta" for g in GENES}
HAY_CORPUS = all(p.exists() for p in FASTA.values())
NO_CORRIDO: list[str] = []


@unittest.skipUnless(HAY_CORPUS, "falta work/sifi_check/, que no esta en git")
class TestAnclaReal(unittest.TestCase):
    """El ancla: los cuatro de la planilla, y solo con el ancho 20."""

    @classmethod
    def setUpClass(cls):
        try:
            from sifi_core import DEFAULTS, SifiEngine
        except Exception as e:                                # pragma: no cover
            NO_CORRIDO.append("ancla real: no se pudo importar el port (%s)" % e)
            raise unittest.SkipTest(str(e))
        cls.efic = {}
        for gen in GENES:
            seq = "".join(l.strip() for l in FASTA[gen].read_text().splitlines()
                          if not l.startswith(">"))
            eng = SifiEngine(mode="fiel", temp_c=22.0, tabla_nn="NN4", **DEFAULTS)
            ventanas, _ = eng.run(seq, backend="vienna")
            cls.efic[gen] = [w.pos for w in ventanas if w.is_efficient]

    def test_el_conjunto_de_partida_es_el_de_las_curvas_historicas(self):
        self.assertEqual({g: len(v) for g, v in self.efic.items()},
                         {"MP_MRFV": 138, "CP_MRFV": 40,
                          "BicC_Dm": 218, "ATPaseD_Dm": 35})

    def test_el_ancho_20_reproduce_los_cuatro_valores_de_la_planilla(self):
        self.assertEqual({g: m.contar_por_incrementos(v, 20)
                          for g, v in self.efic.items()},
                         {g: m.PLANILLA[g] for g in GENES})

    def test_los_anchos_vecinos_no_reproducen_los_cuatro(self):
        for ancho in (19, 21):
            obtenido = {g: m.contar_por_incrementos(v, ancho)
                        for g, v in self.efic.items()}
            self.assertNotEqual(obtenido, {g: m.PLANILLA[g] for g in GENES},
                                "el ancho %d tambien reproduce la planilla: el ancho "
                                "dejaria de estar identificado" % ancho)

    def test_el_sesgo_es_distinto_en_cada_gen(self):
        """No es una constante: por eso dos cifras de la planilla no son comparables."""
        sesgos = {g: len(m.tapadas(v)) / len(v) for g, v in self.efic.items()}
        self.assertEqual(len(set(round(s, 3) for s in sesgos.values())), len(GENES))
        self.assertLess(sesgos["ATPaseD_Dm"], sesgos["MP_MRFV"])


if __name__ == "__main__":
    r = unittest.main(verbosity=2, exit=False).result
    if not HAY_CORPUS:
        NO_CORRIDO.append("ancla real: falta work/sifi_check/, que no esta en git")
    for linea in NO_CORRIDO:
        print("NO CORRIDO: %s" % linea)
    sys.exit(0 if r.wasSuccessful() else 1)
