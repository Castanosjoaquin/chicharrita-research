"""Verificaciones de `comparar_ventanas.py` sobre insumos sinteticos.

Que prueba esto. Los controles fuertes de la linea son los de C1 y C13, que la
herramienta reproduce numero por numero, pero esos necesitan el corpus de EPILAB
y una corrida del motor. Estas pruebas corren en cualquier maquina con la
biblioteca estandar y cubren lo otro: las formas de devolver un numero plausible
y equivocado sin avisar. Que es lo que importa cuando el numero sale impreso en
un informe.

Tres grupos. El primero es la aritmetica que el informe usa como si fuera
obvia: que la matriz de confusion sume las ventanas comparadas, y que dos
corridas puedan informar el mismo conteo senalando ventanas distintas, que es
justamente el caso que la linea vino a mostrar. El segundo es la atribucion:
que el termino que cruzo el corte sea el que de verdad cambio, y no cualquiera
de los cuatro. El tercero son los modos de fallar en silencio.

Sobre el tercer grupo hay una limitacion conocida que estas pruebas **fijan como
comportamiento, no como error**: si el TSV de entrada no trae las columnas de
los cuatro booleanos, la herramienta sigue dando la matriz y las posiciones que
cambian, pero `terminos_que_cruzan` sale vacio. La misma columna sale vacia, con
las entradas completas, cuando lo que movio el veredicto fue la regla terminal,
que no es uno de los cuatro booleanos: es lo que pasa en el par 1 de modos. O
sea que una celda vacia no distingue «no hubo causa entre los cuatro terminos»
de «no me pasaste las columnas». Esta anotado en
`00_meta/PREGUNTAS_ABIERTAS.md`, seccion de la linea M2, porque la respuesta
depende de que columnas mande el investigador.

Uso:
    python test_comparar.py
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import comparar_ventanas as cv

# Las columnas que escribe el port, en su orden. `rama_terminal` es informativa:
# el comparador la copia a la salida pero no decide nada con ella.
COLS = ["pos", "seq", "dg_sense5", "dg_antisense5", "ddg", "accessibility",
        "strand_selection", "end_stability", "target_site_accessibility",
        "thermo_efficient", "is_efficient", "rama_terminal"]

SEQ = "ACGT" * 5 + "A"  # 21 nt, no se usa para decidir nada aca


def fila(pos, ddg=2.0, acc=0.20, eff=None, rama="1"):
    """Arma una fila coherente: los booleanos se derivan de los numeros.

    Los cortes son los del original: la brecha de ddG pasa si es >= 1,0 y la
    seleccion de hebra si es >= 0,0; la apertura pasa si es >= 0,1. `eff` fuerza
    `is_efficient` para poder construir un veredicto que la termodinamica no
    sostiene, que es como se ve una ventana movida por la regla terminal.
    """
    strand = ddg >= 0.0
    end = ddg >= 1.0
    acc_ok = acc >= 0.1
    thermo = strand and end and acc_ok
    return {"pos": pos, "seq": SEQ, "dg_sense5": 0.0, "dg_antisense5": round(ddg / 2, 4),
            "ddg": ddg, "accessibility": acc, "strand_selection": strand,
            "end_stability": end, "target_site_accessibility": acc_ok,
            "thermo_efficient": thermo,
            "is_efficient": thermo if eff is None else eff,
            "rama_terminal": rama}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="m2test_"))

    def escribir(self, filas, nombre, cols=COLS):
        destino = self.tmp / nombre
        with destino.open("w", encoding="utf-8", newline="") as fh:
            fh.write("\t".join(cols) + "\n")
            for f in filas:
                fh.write("\t".join(str(f[c]) for c in cols) + "\n")
        return destino

    def comparar(self, filas_a, filas_b, offset_b=1, etiquetas=("a", "b"),
                 cols_a=COLS, cols_b=COLS):
        a = cv.leer(self.escribir(filas_a, "a.tsv", cols_a))
        b = cv.leer(self.escribir(filas_b, "b.tsv", cols_b))
        return cv.comparar(a, b, offset_b, etiquetas)


class TestMatrizDeConfusion(Base):
    def test_las_cuatro_celdas_suman_las_comparadas(self):
        a = [fila(1), fila(2, ddg=0.5), fila(3, acc=0.02), fila(4)]
        b = [fila(1), fila(2), fila(3, acc=0.02), fila(4, ddg=0.5)]
        res, _ = self.comparar(a, b)
        conf = res["confusion"]
        suma = conf["ambos_si"] + conf["ambos_no"] + conf["solo_a"] + conf["solo_b"]
        self.assertEqual(suma, res["ventanas_comparadas"])
        self.assertEqual(suma, 4)

    def test_mismo_conteo_con_ventanas_distintas(self):
        # El caso que la linea vino a mostrar: una ventana se gana y otra se
        # pierde, el conteo final no se mueve y sin embargo dos posiciones
        # cambiaron de clase. Mirar solo el conteo lo daria por «sin cambios».
        a = [fila(1), fila(2, ddg=0.5), fila(3), fila(4)]
        b = [fila(1), fila(2), fila(3), fila(4, ddg=0.5)]
        res, cambios = self.comparar(a, b)
        self.assertEqual(res["eficientes_a"], res["eficientes_b"])
        self.assertEqual(res["cambian"], 2)
        self.assertEqual(res["confusion"]["solo_a"], 1)
        self.assertEqual(res["confusion"]["solo_b"], 1)

    def test_los_eficientes_salen_de_la_matriz(self):
        a = [fila(1), fila(2), fila(3, ddg=0.5)]
        b = [fila(1), fila(2, ddg=0.5), fila(3, ddg=0.5)]
        res, _ = self.comparar(a, b)
        self.assertEqual(res["eficientes_a"], 2)
        self.assertEqual(res["eficientes_b"], 1)

    def test_las_etiquetas_nombran_las_columnas(self):
        res, cambios = self.comparar([fila(1)], [fila(1, ddg=0.5)],
                                     etiquetas=("contexto", "recorte"))
        self.assertIn("eficientes_contexto", res)
        self.assertIn("solo_contexto", res["confusion"])
        self.assertIn("contexto", cambios[0])
        self.assertIn("ddg_contexto", cambios[0])


class TestAtribucion(Base):
    def test_la_apertura_que_cruza_su_corte(self):
        _, cambios = self.comparar([fila(1, acc=0.20)], [fila(1, acc=0.05)])
        self.assertEqual(len(cambios), 1)
        self.assertIn("target_site_accessibility", cambios[0]["terminos_que_cruzan"])

    def test_la_brecha_que_cruza_su_corte(self):
        _, cambios = self.comparar([fila(1, ddg=2.0)], [fila(1, ddg=0.5)])
        self.assertIn("end_stability", cambios[0]["terminos_que_cruzan"])
        self.assertNotIn("target_site_accessibility", cambios[0]["terminos_que_cruzan"])

    def test_una_brecha_negativa_cruza_dos_cortes(self):
        # ddG por debajo de 0 falla la seleccion de hebra ademas de la
        # estabilidad de extremos: la fila tiene que nombrar los dos.
        _, cambios = self.comparar([fila(1, ddg=2.0)], [fila(1, ddg=-0.5)])
        terminos = cambios[0]["terminos_que_cruzan"]
        self.assertIn("end_stability", terminos)
        self.assertIn("strand_selection", terminos)

    def test_los_terminos_continuos_traen_los_dos_valores_y_el_delta(self):
        _, cambios = self.comparar([fila(1, acc=0.20)], [fila(1, acc=0.05)])
        c = cambios[0]
        self.assertEqual(c["accessibility_a"], 0.2)
        self.assertEqual(c["accessibility_b"], 0.05)
        self.assertAlmostEqual(c["accessibility_delta"], -0.15, places=6)

    def test_el_resumen_junta_los_terminos_sin_repetir(self):
        a = [fila(1, acc=0.20), fila(2, ddg=2.0)]
        b = [fila(1, acc=0.05), fila(2, ddg=0.5)]
        res, _ = self.comparar(a, b)
        self.assertEqual(res["terminos"],
                         sorted(set(res["terminos"])))
        self.assertIn("target_site_accessibility", res["terminos"])
        self.assertIn("end_stability", res["terminos"])

    def test_un_veredicto_movido_por_la_regla_terminal_no_inventa_causa(self):
        # Misma fisica de los dos lados y veredictos distintos: es como se ve
        # una ventana que movio la regla terminal, que no es uno de los cuatro
        # booleanos. La herramienta deja la atribucion vacia en vez de elegir un
        # termino que no cambio. Es el caso del par 1, y por eso ese par sale
        # con `terminos` vacio en su resumen.
        _, cambios = self.comparar([fila(1, eff=True)], [fila(1, eff=False)])
        self.assertEqual(len(cambios), 1)
        self.assertEqual(cambios[0]["terminos_que_cruzan"], "")


class TestDesplazamiento(Base):
    def test_el_recorte_se_alinea_con_su_posicion_en_el_gen(self):
        # La ventana 922 del gen es la 1 del recorte. Las posiciones se
        # informan en coordenadas del gen, que es como las lee C13.
        a = [fila(p) for p in (922, 923, 924)]
        b = [fila(p, acc=0.02) for p in (1, 2, 3)]
        res, cambios = self.comparar(a, b, offset_b=922,
                                     etiquetas=("contexto", "recorte"))
        self.assertEqual(res["ventanas_comparadas"], 3)
        self.assertEqual([c["pos"] for c in cambios], [922, 923, 924])
        self.assertEqual([c["pos_recorte"] for c in cambios], [1, 2, 3])

    def test_las_ventanas_de_un_solo_lado_no_son_cambios_de_clase(self):
        # Al recortar, las ultimas posiciones de inicio del gen no existen en la
        # molecula. Desaparecer no es cambiar de veredicto, y meterlas en la
        # matriz inflaria el desacuerdo.
        a = [fila(p) for p in (1, 2, 3)]
        b = [fila(p) for p in (1, 2)]
        res, cambios = self.comparar(a, b, etiquetas=("contexto", "recorte"))
        self.assertEqual(cambios, [])
        self.assertEqual(res["ventanas_comparadas"], 2)
        self.assertEqual(res["ventanas_solo_en_contexto"], 1)
        self.assertEqual(res["ventanas_solo_en_recorte"], 0)


class TestFallarEnSilencio(Base):
    def test_una_posicion_repetida_aborta(self):
        # Sin esto la segunda fila pisa a la primera y el conteo sale mas chico
        # sin una sola linea de aviso.
        with self.assertRaises(SystemExit):
            cv.leer(self.escribir([fila(1), fila(1, ddg=0.5)], "dup.tsv"))

    def test_un_veredicto_que_no_es_true_ni_false_aborta(self):
        # Un TSV que escriba 1/0 en vez de True/False daria todo False y por lo
        # tanto cero eficientes de los dos lados, con la matriz cerrando igual.
        f = fila(1)
        f["is_efficient"] = 1
        with self.assertRaises(SystemExit):
            a = cv.leer(self.escribir([f], "uno.tsv"))
            cv.comparar(a, a)

    def test_un_tsv_sin_is_efficient_aborta(self):
        cols = [c for c in COLS if c != "is_efficient"]
        with self.assertRaises(SystemExit):
            cv.leer(self.escribir([fila(1)], "sin.tsv", cols))

    def test_un_tsv_vacio_aborta(self):
        destino = self.tmp / "vacio.tsv"
        destino.write_text("\t".join(COLS) + "\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            cv.leer(destino)

    def test_sin_las_columnas_de_terminos_la_atribucion_sale_vacia(self):
        # Limitacion conocida, fijada aca para que se vea: la herramienta no
        # distingue «ningun termino cambio» de «no me pasaste los terminos».
        # Las dos salen con la celda vacia. Ver el encabezado de este archivo.
        cols = [c for c in COLS if c not in cv.BOOLEANOS]
        _, cambios = self.comparar([fila(1, acc=0.20)], [fila(1, acc=0.05)],
                                   cols_a=cols, cols_b=cols)
        self.assertEqual(len(cambios), 1)
        self.assertEqual(cambios[0]["terminos_que_cruzan"], "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
