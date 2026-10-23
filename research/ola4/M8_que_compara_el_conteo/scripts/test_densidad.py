"""Verificaciones de la normalizacion por largo del conteo de eficientes.

Que prueba esto. La afirmacion del informe es que el conteo crudo de ventanas
eficientes no ordena igual que la densidad por ventana, y que la inversion no
depende de la configuracion con la que se conto. Eso es aritmetica sobre conteos
ya medidos y publicados en el repositorio, asi que se puede verificar sin correr
el motor: alcanza con comprobar (a) que la cuenta de ventanas sale del largo,
(b) que la densidad se calcula como se declara, y (c) que en las cuatro columnas
de conteos el primero por conteo crudo y el primero por densidad son genes
distintos.

Uso:
    python test_densidad.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import densidad as m


class TestVentanas(unittest.TestCase):
    def test_ventanas_salen_del_largo(self):
        # Son los «Hits de si-Fi» de la tabla de W5 §0 para tres de los cuatro
        # genes; `BicC_Dm` es el caso aparte y tiene su propia prueba.
        self.assertEqual(m.ventanas(491, 21), 471)
        self.assertEqual(m.ventanas(528, 21), 508)
        self.assertEqual(m.ventanas(1263, 21), 1243)

    def test_bicc_tiene_2500_ventanas_y_no_2504(self):
        # si-Fi reporta 2.504 hits porque cuenta un registro por acierto de
        # Bowtie y el gen tiene dos pares de 21-meros repetidos dentro de si.
        # El denominador de la densidad son las ventanas, que son 2.500.
        self.assertEqual(m.ventanas(2520, 21), 2500)


class TestDensidad(unittest.TestCase):
    def test_densidad_por_100_ventanas(self):
        self.assertAlmostEqual(m.densidad(42, 471), 8.917, places=3)
        self.assertAlmostEqual(m.densidad(212, 2500), 8.480, places=3)

    def test_densidad_de_un_gen_sin_eficientes_es_cero(self):
        self.assertEqual(m.densidad(0, 471), 0.0)


class TestInversionDelOrden(unittest.TestCase):
    def test_el_conteo_crudo_y_la_densidad_no_ordenan_igual(self):
        for nombre, conteos in m.CONTEOS.items():
            por_conteo = m.orden_por_conteo(conteos)
            por_densidad = m.orden_por_densidad(conteos)
            self.assertNotEqual(
                por_conteo,
                por_densidad,
                msg=f"la columna {nombre} ordena igual de las dos maneras",
            )

    def test_bicc_gana_por_conteo_y_mp_por_densidad_en_las_cuatro_columnas(self):
        for nombre, conteos in m.CONTEOS.items():
            self.assertEqual(
                m.orden_por_conteo(conteos)[0],
                "BicC_Dm",
                msg=f"columna {nombre}",
            )
            self.assertEqual(
                m.orden_por_densidad(conteos)[0],
                "MP_MRFV",
                msg=f"columna {nombre}",
            )

    def test_bicc_baja_del_primero_al_tercero_con_los_conteos_del_original(self):
        conteos = m.CONTEOS["original_2.1.5"]
        self.assertEqual(m.orden_por_conteo(conteos).index("BicC_Dm"), 0)
        self.assertEqual(m.orden_por_densidad(conteos).index("BicC_Dm"), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
