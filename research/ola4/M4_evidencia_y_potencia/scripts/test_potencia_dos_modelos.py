"""Verificaciones del calculo de potencia de M4.

Que prueba esto, y por que importa que este probado. El numero que M4 entrega
--cuantos siRNA con eficacia medida hacen falta para distinguir el modo fiel del
corregido-- sale de un remuestreo, no de una formula de libro. Un remuestreo mal
implementado da un numero plausible y mudo: no hay forma de mirarlo y darse cuenta.
Asi que cada pieza se prueba contra algo verificable por fuera del remuestreo.

Las anclas son cuatro:
  1. El rho de Spearman del modulo reproduce los dos coeficientes ya publicados en
     `research/ola3/C9_sensibilidad_umbral/resultados/validacion_resumen.json`
     (+0,142 modo fiel, +0,024 corregido, n = 29). Si no los reproduce, el
     remuestreo esta midiendo otra cosa que la validacion de C9.
  2. La prueba de permutacion por intercambio devuelve p = 1 cuando los dos
     predictores son identicos, porque entonces no hay nada que intercambiar.
  3. La potencia crece con n y, en un caso construido sin senal, se queda en el
     nivel nominal alpha.
  4. El tamano de muestra de dos grupos reproduce el valor de libro: con una
     diferencia de una desviacion estandar, alfa 0,05 a dos colas y potencia 0,80
     hacen falta 17 por grupo.

Uso:
    python test_potencia_dos_modelos.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import potencia_dos_modelos as pot

RAIZ = Path(__file__).resolve().parents[3]
TSV_C9 = (
    RAIZ / "ola3" / "C9_sensibilidad_umbral" / "resultados" / "validacion_31sirna.tsv"
)


class TestCargaYRho(unittest.TestCase):
    def setUp(self) -> None:
        if not TSV_C9.exists():
            self.skipTest(f"falta el insumo de C9: {TSV_C9}")
        self.datos = pot.cargar_cedden(TSV_C9)

    def test_n_es_29(self) -> None:
        self.assertEqual(len(self.datos.hr), 29)
        self.assertEqual(len(self.datos.fiel), 29)
        self.assertEqual(len(self.datos.corregido), 29)

    def test_reproduce_los_rho_publicados(self) -> None:
        rho_f = pot.rho_spearman(self.datos.fiel, self.datos.hr)
        rho_c = pot.rho_spearman(self.datos.corregido, self.datos.hr)
        self.assertAlmostEqual(rho_f, 0.142, places=3)
        self.assertAlmostEqual(rho_c, 0.024, places=3)

    def test_el_corregido_es_subconjunto_del_fiel(self) -> None:
        # C1 de CAMBIOS.md: ninguna ventana va en sentido contrario.
        self.assertTrue(np.all(self.datos.corregido <= self.datos.fiel))

    def test_hay_un_solo_discordante(self) -> None:
        # Es el hecho que gobierna toda la potencia de esta comparacion.
        self.assertEqual(pot.n_discordantes(self.datos), 1)


class TestRhoSpearman(unittest.TestCase):
    def test_monotona_perfecta(self) -> None:
        x = np.array([1.0, 2.0, 3.0, 4.0])
        y = np.array([10.0, 20.0, 30.0, 40.0])
        self.assertAlmostEqual(pot.rho_spearman(x, y), 1.0)

    def test_invierte_el_signo(self) -> None:
        x = np.array([1.0, 2.0, 3.0, 4.0])
        y = np.array([40.0, 30.0, 20.0, 10.0])
        self.assertAlmostEqual(pot.rho_spearman(x, y), -1.0)

    def test_predictor_constante_es_nan(self) -> None:
        x = np.ones(5)
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertTrue(np.isnan(pot.rho_spearman(x, y)))

    def test_usa_rangos_y_no_valores(self) -> None:
        # Un desenlace con un valor extremo no debe cambiar el rho de rangos.
        x = np.array([0.0, 0.0, 1.0, 1.0])
        y1 = np.array([1.0, 2.0, 3.0, 4.0])
        y2 = np.array([1.0, 2.0, 3.0, 4000.0])
        self.assertAlmostEqual(pot.rho_spearman(x, y1), pot.rho_spearman(x, y2))


class TestPruebaDePermutacion(unittest.TestCase):
    def test_predictores_identicos_dan_p_uno(self) -> None:
        rng = np.random.default_rng(0)
        x = np.array([0.0, 0.0, 1.0, 1.0, 0.0, 1.0])
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        p = pot.p_permutacion(x, x, y, n_perm=199, rng=rng)
        self.assertEqual(p, 1.0)

    def test_discordancia_fuerte_da_p_chico(self) -> None:
        # 40 siRNA, todos discordantes y todos en el mismo sentido: el fiel acierta
        # y el corregido no. Es el caso extremo en el que la prueba debe rechazar.
        rng = np.random.default_rng(1)
        n = 40
        fiel = np.r_[np.ones(n // 2), np.zeros(n // 2)]
        corregido = np.zeros(n)
        hr = np.r_[np.arange(n // 2) + 100.0, np.arange(n // 2) * 1.0]
        p = pot.p_permutacion(fiel, corregido, hr, n_perm=999, rng=rng)
        self.assertLess(p, 0.05)

    def test_p_esta_en_el_rango_valido(self) -> None:
        rng = np.random.default_rng(2)
        x = rng.integers(0, 2, 30).astype(float)
        z = np.minimum(x, rng.integers(0, 2, 30).astype(float))
        y = rng.normal(size=30)
        p = pot.p_permutacion(x, z, y, n_perm=99, rng=rng)
        self.assertGreaterEqual(p, 1.0 / 100.0)
        self.assertLessEqual(p, 1.0)


class TestCotaCombinatoria(unittest.TestCase):
    """El techo de la prueba: con pocos discordantes no hay p chico posible."""

    @staticmethod
    def _caso_favorable(k: int, n: int = 200) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        # Configuracion mas favorable que existe: los k discordantes son los siRNA
        # de mayor eficacia y el fiel los marca a todos.
        fiel = np.zeros(n)
        corregido = np.zeros(n)
        fiel[:k] = 1.0
        hr = np.arange(n, 0, -1).astype(float)
        return fiel, corregido, hr

    def test_con_un_discordante_el_p_es_uno(self) -> None:
        f, c, hr = self._caso_favorable(1)
        self.assertEqual(pot.p_exacto_enumerado(f, c, hr), 1.0)

    def test_cinco_discordantes_no_alcanzan(self) -> None:
        f, c, hr = self._caso_favorable(5)
        self.assertAlmostEqual(pot.p_exacto_enumerado(f, c, hr), 2.0 / 32.0)
        self.assertGreater(pot.p_exacto_enumerado(f, c, hr), 0.05)

    def test_seis_discordantes_alcanzan(self) -> None:
        f, c, hr = self._caso_favorable(6)
        self.assertAlmostEqual(pot.p_exacto_enumerado(f, c, hr), 2.0 / 64.0)
        self.assertLessEqual(pot.p_exacto_enumerado(f, c, hr), 0.05)

    def test_la_cota_coincide_con_la_enumeracion(self) -> None:
        self.assertEqual(pot.k_minimo_para_rechazar(0.05), 6)
        for k in range(1, 9):
            f, c, hr = self._caso_favorable(k)
            puede = pot.p_exacto_enumerado(f, c, hr) <= 0.05
            self.assertEqual(puede, k >= pot.k_minimo_para_rechazar(0.05))

    def test_el_enumerado_coincide_con_el_sorteado(self) -> None:
        rng = np.random.default_rng(7)
        f, c, hr = self._caso_favorable(8)
        exacto = pot.p_exacto_enumerado(f, c, hr)
        sorteado = pot.p_permutacion(f, c, hr, n_perm=20000, rng=rng)
        self.assertAlmostEqual(exacto, sorteado, places=2)


class TestPotenciaPorRemuestreo(unittest.TestCase):
    def test_sin_discordancia_la_potencia_no_pasa_de_alpha(self) -> None:
        # Si los dos modelos coinciden en las 29 filas, no hay nada que detectar y
        # la prueba no puede rechazar nunca.
        rng = np.random.default_rng(3)
        x = rng.integers(0, 2, 29).astype(float)
        datos = pot.Datos(nombres=None, fiel=x, corregido=x.copy(), hr=rng.normal(size=29))
        p = pot.potencia_remuestreo(datos, n=200, b=60, n_perm=99, rng=rng)
        self.assertEqual(p.potencia, 0.0)

    def test_la_potencia_crece_con_n(self) -> None:
        rng = np.random.default_rng(4)
        n0 = 20
        fiel = np.r_[np.ones(6), np.zeros(n0 - 6)]
        corregido = np.r_[np.ones(3), np.zeros(n0 - 3)]
        hr = np.r_[np.arange(6) + 50.0, np.arange(n0 - 6) * 1.0]
        datos = pot.Datos(nombres=None, fiel=fiel, corregido=corregido, hr=hr)
        chica = pot.potencia_remuestreo(datos, n=25, b=120, n_perm=199, rng=rng)
        grande = pot.potencia_remuestreo(datos, n=400, b=120, n_perm=199, rng=rng)
        self.assertLess(chica.potencia, grande.potencia)

    def test_el_reservorio_reemplaza_el_desenlace_de_los_discordantes(self) -> None:
        # Propiedad verificable del mecanismo: con un reservorio de un solo valor
        # absurdo, toda fila discordante sorteada tiene que quedar con ese valor, y
        # entonces los discordantes son indistinguibles del tope de rangos.
        rng = np.random.default_rng(8)
        fiel = np.array([1.0, 0.0, 0.0, 0.0])
        corregido = np.array([0.0, 0.0, 0.0, 0.0])
        hr = np.array([1.0, 2.0, 3.0, 4.0])
        datos = pot.Datos(nombres=None, fiel=fiel, corregido=corregido, hr=hr)
        con_pool = pot.potencia_remuestreo(
            datos, n=60, b=40, n_perm=99, rng=rng, pool_discordantes=np.array([999.0])
        )
        # Con el desenlace del discordante siempre en el tope, el modo fiel ordena
        # perfecto y la prueba rechaza casi siempre.
        self.assertGreater(con_pool.potencia, 0.9)

    def test_el_reservorio_por_defecto_son_los_eficientes_del_fiel(self) -> None:
        fiel = np.array([1.0, 0.0, 1.0])
        datos = pot.Datos(
            nombres=None,
            fiel=fiel,
            corregido=np.zeros(3),
            hr=np.array([10.0, 20.0, 30.0]),
        )
        self.assertEqual(
            sorted(pot.pool_discordantes_por_defecto(datos).tolist()), [10.0, 30.0]
        )

    def test_dar_varianza_a_los_discordantes_no_sube_la_potencia(self) -> None:
        # El punto metodologico: el remuestreo sin reservorio copia el unico
        # discordante observado, asi que su clase tiene varianza cero y la potencia
        # sale optimista. Con varianza real no puede salir mas alta.
        if not TSV_C9.exists():
            self.skipTest(f"falta el insumo de C9: {TSV_C9}")
        datos = pot.cargar_cedden(TSV_C9)
        rng = np.random.default_rng(9)
        sin = pot.potencia_remuestreo(datos, n=232, b=200, n_perm=299, rng=rng)
        con = pot.potencia_remuestreo(
            datos,
            n=232,
            b=200,
            n_perm=299,
            rng=rng,
            pool_discordantes=pot.pool_discordantes_por_defecto(datos),
        )
        self.assertLessEqual(con.potencia, sin.potencia)

    def test_n_minimo_devuelve_un_n_con_potencia_suficiente(self) -> None:
        rng = np.random.default_rng(5)
        n0 = 20
        fiel = np.r_[np.ones(6), np.zeros(n0 - 6)]
        corregido = np.r_[np.ones(3), np.zeros(n0 - 3)]
        hr = np.r_[np.arange(6) + 50.0, np.arange(n0 - 6) * 1.0]
        datos = pot.Datos(nombres=None, fiel=fiel, corregido=corregido, hr=hr)
        res = pot.n_minimo_remuestreo(
            datos, objetivo=0.8, b=120, n_perm=199, rng=rng, n_max=3200
        )
        self.assertIsNotNone(res.n)
        self.assertGreaterEqual(res.potencia, 0.8)


class TestEnsayoDeDosGrupos(unittest.TestCase):
    def test_reproduce_el_valor_de_libro(self) -> None:
        # Diferencia de una desviacion estandar, alfa 0,05 a dos colas, potencia
        # 0,80: el resultado clasico es 17 por grupo.
        self.assertEqual(pot.n_por_grupo(delta=1.0, sd=1.0, alpha=0.05, objetivo=0.8), 17)

    def test_mas_efecto_pide_menos_muestra(self) -> None:
        chico = pot.n_por_grupo(delta=10.0, sd=20.0)
        grande = pot.n_por_grupo(delta=30.0, sd=20.0)
        self.assertGreater(chico, grande)

    def test_alfa_mas_estricto_pide_mas_muestra(self) -> None:
        laxo = pot.n_por_grupo(delta=20.0, sd=20.0, alpha=0.05)
        estricto = pot.n_por_grupo(delta=20.0, sd=20.0, alpha=0.025)
        self.assertGreaterEqual(estricto, laxo)

    def test_la_potencia_en_el_n_devuelto_alcanza_el_objetivo(self) -> None:
        n = pot.n_por_grupo(delta=15.0, sd=18.0, alpha=0.05, objetivo=0.8)
        self.assertGreaterEqual(pot.potencia_dos_grupos(15.0, 18.0, n, 0.05), 0.8)
        self.assertLess(pot.potencia_dos_grupos(15.0, 18.0, n - 1, 0.05), 0.8)


class TestEquivalencia(unittest.TestCase):
    def test_tost_pide_mas_que_la_prueba_de_diferencia(self) -> None:
        # Concluir «silencian igual» es una afirmacion de equivalencia y cuesta mas
        # muestra que concluir «silencian distinto» con el mismo margen.
        n_dif = pot.n_por_grupo(delta=15.0, sd=18.0)
        n_tost = pot.n_por_grupo_tost(margen=15.0, sd=18.0)
        self.assertGreater(n_tost, n_dif)

    def test_margen_mas_chico_pide_mas_muestra(self) -> None:
        self.assertGreater(
            pot.n_por_grupo_tost(margen=10.0, sd=18.0),
            pot.n_por_grupo_tost(margen=20.0, sd=18.0),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
