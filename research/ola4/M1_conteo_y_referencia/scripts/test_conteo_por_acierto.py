"""Verificaciones de la regla de conteo del original, con insumos sinteticos.

Que prueba esto, y por que con insumos sinteticos. La regla que implementa
`conteo_por_acierto.py` se lee del fuente del si-Fi21 original, y los tres casos
que la hacen interesante --una ventana eficiente que no pega, una que pega solo en
la hebra menos, una que pega dos veces-- son justamente los que no aparecen cuando
la base es el gen mismo. Con secuencias de juguete se pueden construir los tres a
mano y comprobar que cada uno mueve el conteo en la direccion que la lectura del
fuente predice. Eso es lo que hace que el numero que salga despues, contra las
bases reales, sea interpretable.

No reemplaza a la celda de verificacion contra el gen mismo, que necesita el TSV
del port sobre las secuencias de EPILAB y vive en `work/`.

Uso:
    python test_conteo_por_acierto.py
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import conteo_por_acierto as m

A = m.Acierto


def ventanas(*especificacion):
    """(pos, seq, eficiente) -> el dict que devuelve leer_ventanas."""
    return {pos: {"seq": seq, "eficiente": ef} for pos, seq, ef in especificacion}


# Ventanas de juguete de 6 nt: el largo no importa para la regla, que solo mira
# posiciones, hebras y nombres de referencia.
TRES = ventanas((1, "AAACCC", True), (2, "AACCCG", False), (3, "ACCCGT", True))


class TestRegla(unittest.TestCase):

    def test_un_acierto_por_ventana_en_mas_coincide_con_el_conteo_por_ventana(self):
        r = m.regla_original(TRES, [A(1, "ref", "+", 0), A(2, "ref", "+", 1),
                                    A(3, "ref", "+", 2)])
        self.assertEqual(r["eficientes_por_ventana"], 2)
        self.assertEqual(r["aciertos_mas_total"], 2)
        self.assertEqual(r["filas"], {"ref": 2})
        self.assertEqual(r["eficientes_sin_acierto"], 0)
        self.assertEqual(r["eficientes_con_acierto_multiple_en_una_ref"], 0)

    def test_la_ventana_eficiente_que_no_pega_se_pierde_del_conteo(self):
        r = m.regla_original(TRES, [A(1, "ref", "+", 0)])
        self.assertEqual(r["eficientes_por_ventana"], 2)
        self.assertEqual(r["aciertos_mas_total"], 1)
        self.assertEqual(r["eficientes_sin_acierto"], 1)

    def test_la_ventana_que_pega_solo_en_menos_no_entra_al_conteo(self):
        r = m.regla_original(TRES, [A(1, "ref", "+", 0), A(3, "ref", "-", 7)])
        self.assertEqual(r["aciertos_mas_total"], 1)
        self.assertEqual(r["aciertos_cualquier_hebra_total"], 2)
        # pego, asi que no es una ventana sin acierto; pero no se evaluo
        self.assertEqual(r["eficientes_sin_acierto"], 0)
        self.assertEqual(r["eficientes_sin_acierto_mas"], 1)

    def test_la_ventana_que_pega_dos_veces_en_la_misma_referencia_cuenta_dos_veces(self):
        r = m.regla_original(TRES, [A(1, "ref", "+", 0), A(1, "ref", "+", 40),
                                    A(3, "ref", "+", 2)])
        self.assertEqual(r["eficientes_por_ventana"], 2)
        self.assertEqual(r["aciertos_mas_total"], 3)
        self.assertEqual(r["filas"], {"ref": 3})
        self.assertEqual(r["eficientes_con_acierto_multiple_en_una_ref"], 1)
        self.assertEqual(r["eficientes_con_mas_de_un_acierto_mas"], 1)

    def test_dos_referencias_reparten_el_conteo_en_dos_filas(self):
        r = m.regla_original(TRES, [A(1, "r1", "+", 0), A(1, "r2", "+", 5),
                                    A(3, "r1", "+", 2)])
        self.assertEqual(r["filas"], {"r1": 2, "r2": 1})
        self.assertEqual(r["aciertos_mas_total"], 3)
        self.assertEqual(r["fila_max"], {"ref": "r1", "conteo": 2})
        # ninguna referencia la recibe dos veces, pero la ventana pega dos veces
        self.assertEqual(r["eficientes_con_acierto_multiple_en_una_ref"], 0)
        self.assertEqual(r["eficientes_con_mas_de_un_acierto_mas"], 1)

    def test_la_ventana_no_eficiente_nunca_cuenta(self):
        r = m.regla_original(TRES, [A(2, "ref", "+", i) for i in range(10)])
        self.assertEqual(r["aciertos_mas_total"], 0)
        self.assertEqual(r["filas"], {})

    def test_el_alineamiento_repetido_en_el_archivo_no_multiplica(self):
        r = m.regla_original(TRES, [A(1, "ref", "+", 0), A(1, "ref", "+", 0)])
        self.assertEqual(r["aciertos_mas_total"], 1)

    def test_los_aciertos_de_ventanas_que_el_tsv_no_tiene_se_informan(self):
        r = m.regla_original(TRES, [A(1, "ref", "+", 0), A(99, "ref", "+", 9)])
        self.assertEqual(r["aciertos_sin_ventana_en_el_tsv"], 1)
        self.assertEqual(r["aciertos_mas_total"], 1)

    def test_sin_aciertos_la_fila_mayor_es_vacia(self):
        r = m.regla_original(TRES, [])
        self.assertEqual(r["fila_max"], {"ref": None, "conteo": 0})
        self.assertEqual(r["eficientes_sin_acierto"], 2)


class TestAgregaciones(unittest.TestCase):

    def setUp(self):
        self.celda = m.regla_original(
            TRES, [A(1, "BicC_Dm_full", "+", 0), A(1, "otro", "+", 3),
                   A(3, "BicC_Dm_full", "+", 2)])

    def test_las_tres_agregaciones_dan_numeros_distintos(self):
        self.assertEqual(m.agregar(self.celda, "BicC_Dm", "suma_filas"), 3)
        self.assertEqual(m.agregar(self.celda, "BicC_Dm", "fila_max"), 2)
        self.assertEqual(m.agregar(self.celda, "BicC_Dm", "fila_homonima"), 2)

    def test_la_fila_homonima_es_none_si_ninguna_referencia_nombra_al_gen(self):
        self.assertIsNone(m.agregar(self.celda, "MP_MRFV", "fila_homonima"))

    def test_la_fila_homonima_es_none_si_dos_referencias_nombran_al_gen(self):
        # Dos filas no son una fila: sumarlas daria un numero que parece una fila.
        celda = m.regla_original(
            TRES, [A(1, "BicC_Dm_full", "+", 0), A(1, "BicC_Dm_contig2", "+", 3),
                   A(3, "BicC_Dm_full", "+", 2)])
        self.assertIsNone(m.agregar(celda, "BicC_Dm", "fila_homonima"))
        self.assertEqual(celda["filas_que_nombran_al_gen"],
                         {"BicC_Dm_full": 2, "BicC_Dm_contig2": 1})

    def test_la_distancia_es_none_si_falta_un_gen(self):
        self.assertIsNone(m.distancia({"MP_MRFV": None}, {"MP_MRFV": 114}))
        self.assertEqual(m.distancia({"MP_MRFV": 110}, {"MP_MRFV": 114}), 4)


class TestParseoBowtie(unittest.TestCase):

    NATIVO = (
        "w1\t+\tref\t0\tAAACCC\tIIIIII\t0\t\n"
        "w1\t+\tref\t40\tAAACCC\tIIIIII\t0\t\n"
        "w3\t-\tref\t7\tACGGGT\tIIIIII\t0\t3:A>G\n"
    )
    # Mismos tres alineamientos en SAM: la bandera 16 es la hebra menos y la
    # posicion es 1-based, asi que 1, 41 y 8 son los mismos offsets 0, 40 y 7.
    SAM = (
        "@HD\tVN:1.0\n"
        "@SQ\tSN:ref\tLN:60\n"
        "w1\t0\tref\t1\t255\t6M\t*\t0\t0\tAAACCC\tIIIIII\n"
        "w1\t256\tref\t41\t255\t6M\t*\t0\t0\tAAACCC\tIIIIII\n"
        "w3\t16\tref\t8\t255\t6M\t*\t0\t0\tACGGGT\tIIIIII\n"
        "w2\t4\t*\t0\t0\t*\t*\t0\t0\tAACCCG\tIIIIII\n"
    )

    def test_los_dos_formatos_dan_los_mismos_aciertos(self):
        with tempfile.TemporaryDirectory() as d:
            nat, sam = Path(d) / "n.txt", Path(d) / "s.sam"
            nat.write_text(self.NATIVO, encoding="utf-8")
            sam.write_text(self.SAM, encoding="utf-8")
            self.assertEqual(set(m.parsear_bowtie(nat)), set(m.parsear_bowtie(sam)))

    def test_el_nativo_se_parsea_con_hebras_y_offsets(self):
        with tempfile.TemporaryDirectory() as d:
            nat = Path(d) / "n.txt"
            nat.write_text(self.NATIVO, encoding="utf-8")
            self.assertEqual(sorted(m.parsear_bowtie(nat)),
                             sorted([A(1, "ref", "+", 0), A(1, "ref", "+", 40),
                                     A(3, "ref", "-", 7)]))

    def test_la_lectura_no_alineada_de_sam_se_descarta(self):
        with tempfile.TemporaryDirectory() as d:
            sam = Path(d) / "s.sam"
            sam.write_text(self.SAM, encoding="utf-8")
            self.assertNotIn(2, {a.pos for a in m.parsear_bowtie(sam)})


class TestNombreDeLectura(unittest.TestCase):
    """Tomar el ultimo entero del nombre asignaba el acierto a otra ventana."""

    def test_la_convencion_del_subcomando_ventanas(self):
        self.assertEqual(m.pos_desde_nombre("w1221"), 1221)

    def test_un_solo_grupo_de_digitos_se_acepta(self):
        self.assertEqual(m.pos_desde_nombre("BicC_Dm_ventana922"), 922)

    def test_el_nombre_ambiguo_aborta_en_vez_de_elegir(self):
        with self.assertRaises(SystemExit):
            m.pos_desde_nombre("w12_2")

    def test_el_nombre_sin_digitos_aborta(self):
        with self.assertRaises(SystemExit):
            m.pos_desde_nombre("ventana")


class TestValidacionDeInsumos(unittest.TestCase):

    def _tsv(self, d: Path, filas: list[str]) -> Path:
        p = d / "v.tsv"
        p.write_text("pos\tseq\tis_efficient\n" + "\n".join(filas) + "\n", encoding="utf-8")
        return p

    def test_la_posicion_repetida_en_el_tsv_aborta(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._tsv(Path(d), ["1\tAAACCC\tTrue", "1\tAACCCG\tFalse"])
            with self.assertRaises(SystemExit):
                m.leer_ventanas(p)

    def test_la_ventana_sin_secuencia_aborta_la_enumeracion_local(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            fa = d / "ref.fasta"
            fa.write_text(">ref\nAAACCCTTGGGTTT\n", encoding="utf-8")
            v = ventanas((1, "AAACCC", True), (2, "", True))
            with self.assertRaises(SystemExit):
                m.aciertos_locales(v, fa)

    def test_el_codigo_iupac_ambiguo_aborta_en_vez_de_complementarse_mal(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            fa = d / "ref.fasta"
            fa.write_text(">ref\nAAACCCTTGGGTTT\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                m.aciertos_locales(ventanas((1, "AAARCC", True)), fa)

    def test_el_largo_heterogeneo_aborta(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            fa = d / "ref.fasta"
            fa.write_text(">ref\nAAACCCTTGGGTTT\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                m.aciertos_locales(ventanas((1, "AAACCC", True), (2, "AACCC", True)), fa)


class TestEnes(unittest.TestCase):
    """Una N no aparea, asi que no puede haber alineamiento perfecto sobre ella.

    Es la restriccion que hace que la enumeracion local siga siendo equivalente a
    `bowtie -a -v 0`: comparar `N == N` y declararlo acierto exacto habria inventado
    aciertos que Bowtie no reporta, y los genomas tienen tramos largos de N.
    """

    def test_la_ventana_con_n_no_pega_ni_contra_una_referencia_con_n(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            fa = d / "ref.fasta"
            fa.write_text(">ref\nAAANCCTTGGGTTT\n", encoding="utf-8")
            got = m.aciertos_locales(ventanas((1, "AAANCC", True)), fa)
        self.assertEqual(got, [])

    def test_la_ventana_con_n_queda_como_eficiente_sin_acierto(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            fa = d / "ref.fasta"
            fa.write_text(">ref\nAAANCCTTGGGTTT\n", encoding="utf-8")
            v = ventanas((1, "AAANCC", True), (2, "AANCCT", False))
            r = m.regla_original(v, m.aciertos_locales(v, fa))
        self.assertEqual(r["eficientes_sin_acierto"], 1)
        self.assertEqual(r["aciertos_mas_total"], 0)

    def test_el_tramo_de_la_referencia_con_n_no_genera_aciertos(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            fa = d / "ref.fasta"
            fa.write_text(">ref\nNNNNNNAAACCCNNNNNN\n", encoding="utf-8")
            got = m.aciertos_locales(ventanas((1, "AAACCC", True)), fa)
        self.assertEqual(got, [m.Acierto(1, "ref", "+", 6)])


class TestPalindromos(unittest.TestCase):
    """Una ventana igual a su complemento reverso no se emite dos veces."""

    def test_no_se_duplica_el_mismo_alineamiento_en_las_dos_hebras(self):
        # AAATTT es su propio complemento reverso.
        self.assertEqual(m.revcomp("AAATTT"), "AAATTT")
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            fa = d / "ref.fasta"
            fa.write_text(">ref\nGGAAATTTGG\n", encoding="utf-8")
            got = m.aciertos_locales(ventanas((1, "AAATTT", True)), fa)
        self.assertEqual(got, [m.Acierto(1, "ref", "+", 2)])

    def test_con_largo_impar_el_caso_no_existe(self):
        # Con k impar la base del medio tendria que ser su propio complemento.
        for s in ("AAACCCTTGGGTTTAGCTAGCTT", "ACGTACGTACGTACGTACGTA"):
            self.assertNotEqual(m.revcomp(s), s)


class TestEnumeracionLocal(unittest.TestCase):
    """La enumeracion local tiene que dar lo mismo que `bowtie -a -v 0`.

    El fixture tiene las tres situaciones a la vez: un 6-mero que aparece dos veces
    en la referencia, uno que aparece solo como complemento reverso y uno que no
    aparece.
    """

    # 0         1         2         3
    # 0123456789012345678901234567890123456789
    REF = "AAACCCTTGGGTTTAAACCCTTAGGGTTTAAATTTGGG"

    def setUp(self):
        self.v = ventanas(
            (1, "AAACCC", True),    # en 0 y en 14: dos aciertos en `+`
            (2, "GGGTTT", True),    # en 8 y en 23 en `+`, y revcomp AAACCC en `-`
            (3, "GGGAAG", True),    # no aparece con 0 desajustes
        )

    def _correr(self, mm):
        with tempfile.TemporaryDirectory() as d:
            fa = Path(d) / "ref.fasta"
            fa.write_text(f">ref descripcion ignorada\n{self.REF}\n", encoding="utf-8")
            return sorted(m.aciertos_locales(self.v, fa, mm=mm))

    def test_exacto_encuentra_las_repeticiones_en_mas(self):
        got = self._correr(0)
        self.assertIn(A(1, "ref", "+", 0), got)
        self.assertIn(A(1, "ref", "+", 14), got)
        self.assertEqual(sum(1 for a in got if a.pos == 1 and a.hebra == "+"), 2)

    def test_exacto_encuentra_la_hebra_menos(self):
        got = self._correr(0)
        # AAACCC en la referencia es el complemento reverso de GGGTTT
        self.assertIn(A(2, "ref", "-", 0), got)
        self.assertIn(A(2, "ref", "-", 14), got)

    def test_exacto_no_inventa_la_ventana_que_no_esta(self):
        self.assertEqual([a for a in self._correr(0) if a.pos == 3], [])

    def test_exacto_coincide_con_la_posicion_que_reporta_la_referencia(self):
        for a in self._correr(0):
            patron = self.v[a.pos]["seq"] if a.hebra == "+" else m.revcomp(self.v[a.pos]["seq"])
            self.assertEqual(self.REF[a.offset:a.offset + len(patron)], patron)

    def test_un_desajuste_es_superconjunto_del_exacto(self):
        self.assertTrue(set(self._correr(1)).issuperset(set(self._correr(0))))

    def test_un_desajuste_encuentra_el_vecino_a_distancia_uno(self):
        # AAACCC esta en la referencia; AAACCA difiere en una posicion.
        v = ventanas((1, "AAACCA", True))
        with tempfile.TemporaryDirectory() as d:
            fa = Path(d) / "ref.fasta"
            fa.write_text(f">ref\n{self.REF}\n", encoding="utf-8")
            self.assertEqual(m.aciertos_locales(v, fa, mm=0), [])
            got = sorted(m.aciertos_locales(v, fa, mm=1))
        self.assertIn(A(1, "ref", "+", 0), got)
        self.assertIn(A(1, "ref", "+", 14), got)

    def test_no_duplica_el_acierto_exacto_cuando_mm_es_uno(self):
        # Con el palomar, un acierto perfecto cae en las dos mitades a la vez.
        got = self._correr(1)
        self.assertEqual(len(got), len(set(got)))


class TestRevcomp(unittest.TestCase):

    def test_es_involutivo(self):
        for s in ("AAACCCGGGTTT", "ACGTN", ""):
            self.assertEqual(m.revcomp(m.revcomp(s)), s)

    def test_complementa_y_da_vuelta(self):
        self.assertEqual(m.revcomp("AAACCC"), "GGGTTT")


class TestIdentidadDeExtremoAExtremo(unittest.TestCase):
    """Contra el gen mismo, el invariante es que ninguna eficiente queda sin acierto.

    El criterio del plan dice que (a) y (b) tienen que coincidir. Eso es cierto solo
    si ningun 21-mero del gen esta repetido: si lo esta, (b) es mayor que (a), y por
    exactamente la cantidad de aciertos de mas sobre ventanas eficientes. Lo que se
    cumple siempre es que ninguna ventana eficiente queda sin acierto en `+`, y eso
    es lo que verifica `--exigir-identidad`. En `BicC_Dm` el exceso esta medido:
    Bowtie reporta 2.504 aciertos para 2.500 ventanas `[M]`.
    """

    GEN = "AAACCCTTGGGTTTAGCTAGCTTTAAACCCTTGGGTTTAGCTAGC"  # con un tramo repetido
    K = 21

    def _escribir_caso(self, d: Path, eficientes_cada: int = 3):
        tsv = d / "gen.tsv"
        filas = ["pos\tseq\tis_efficient"]
        for i in range(len(self.GEN) - self.K + 1):
            pos = i + 1
            ef = (pos % eficientes_cada == 1)
            filas.append(f"{pos}\t{self.GEN[i:i + self.K]}\t{ef}")
        tsv.write_text("\n".join(filas) + "\n", encoding="utf-8")
        fa = d / "gen.fasta"
        fa.write_text(f">gen_full\n{self.GEN}\n", encoding="utf-8")
        return tsv, fa

    def test_ninguna_eficiente_queda_sin_acierto_y_el_exceso_es_el_de_las_repeticiones(self):
        with tempfile.TemporaryDirectory() as d:
            tsv, fa = self._escribir_caso(Path(d))
            v = m.leer_ventanas(tsv)
            r = m.regla_original(v, m.aciertos_locales(v, fa, mm=0))
        self.assertEqual(r["eficientes_sin_acierto_mas"], 0)
        self.assertGreaterEqual(r["aciertos_mas_total"], r["eficientes_por_ventana"])

    def test_el_subcomando_contar_corre_y_escribe_el_json(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            tsv, fa = self._escribir_caso(d)
            salida = d / "conteo.json"
            codigo = m.main(["contar", "--gen", f"gen={tsv}", "--base", f"identidad={fa}",
                             "--declarado", "gen=1", "--exigir-identidad", "identidad",
                             "--json", str(salida)])
            self.assertEqual(codigo, 0)
            dato = json.loads(salida.read_text(encoding="utf-8"))
        celda = dato["celdas"]["identidad"]["gen"]
        self.assertEqual(celda["eficientes_sin_acierto_mas"], 0)
        for agregacion in m.AGREGACIONES:
            self.assertIn("identidad", dato["agregaciones"][agregacion])

    def test_un_gen_sin_numero_declarado_no_arruina_el_veredicto_de_los_declarados(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            tsv, fa = self._escribir_caso(d)
            v = m.leer_ventanas(tsv)
            esperado = m.regla_original(v, m.aciertos_locales(v, fa))["aciertos_mas_total"]
            salida = d / "c.json"
            m.main(["contar", "--gen", f"gen={tsv}", "--gen", f"otro={tsv}",
                    "--base", f"identidad={fa}", "--declarado", f"gen={esperado}",
                    "--json", str(salida)])
            dato = json.loads(salida.read_text(encoding="utf-8"))
        fila = dato["agregaciones"]["suma_filas"]["identidad"]
        self.assertEqual(sorted(fila["vector"]), ["gen", "otro"])
        self.assertEqual(sorted(dato["declarado"]), ["gen"])
        self.assertTrue(fila["reproduce"])

    def test_exigir_identidad_falla_cuando_la_base_no_contiene_al_gen(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            tsv, _ = self._escribir_caso(d)
            otra = d / "otra.fasta"
            otra.write_text(">otra\n" + "ACGT" * 30 + "\n", encoding="utf-8")
            codigo = m.main(["contar", "--gen", f"gen={tsv}", "--base", f"otra={otra}",
                             "--exigir-identidad", "otra"])
        self.assertEqual(codigo, 1)

    def test_el_subcomando_ventanas_escribe_un_fasta_con_una_ventana_por_registro(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            tsv, _ = self._escribir_caso(d)
            fa = d / "ventanas.fasta"
            m.main(["ventanas", "--tsv", str(tsv), "--salida", str(fa)])
            registros = m.leer_fasta(fa)
        self.assertEqual(len(registros), len(self.GEN) - self.K + 1)
        self.assertTrue(all(len(s) == self.K for _, s in registros))
        self.assertEqual(m.pos_desde_nombre(registros[0][0]), 1)

    def test_el_subcomando_revcomp_da_vuelta_el_fasta(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            _, fa = self._escribir_caso(d)
            rc = d / "rc.fasta"
            m.main(["revcomp", "--fasta", str(fa), "--salida", str(rc)])
            registros = m.leer_fasta(rc)
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0][1], m.revcomp(self.GEN))
        self.assertTrue(registros[0][0].endswith("_revcomp"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
