#!/usr/bin/env python3
"""Pruebas de F1. Correr con: python test_transferir_anotacion.py (env f1_homologia)."""
import ast
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import transferir_anotacion as T

RAIZ = Path(__file__).resolve().parents[4]
COMP = str.maketrans("ACGT", "TGCA")


def rc(s):
    return s.translate(COMP)[::-1]


import random

_AZAR = random.Random(1)
_CODONES_POR_AA = {}
for _i, _aa in enumerate(T._AA_TABLA):
    _CODONES_POR_AA.setdefault(_aa, []).append("ACGT"[_i // 16] + "ACGT"[_i // 4 % 4] + "ACGT"[_i % 4])
_AAS = [a for a in _CODONES_POR_AA if a != "*"]


def proteina_al_azar(n, semilla):
    r = random.Random(semilla)
    return "M" + "".join(r.choice(_AAS) for _ in range(n))


def cds(prot, semilla=0):
    r = random.Random(semilla)
    return "".join(r.choice(_CODONES_POR_AA[a]) for a in prot)


def traducir(nt):
    c = T._BASE[[ord(x) for x in nt]]
    return T.traducir_marco(c, 0).tobytes().decode()


class Traduccion(unittest.TestCase):
    def test_tabla_estandar(self):
        casos = {"ATG": "M", "TGG": "W", "TAA": "*", "TAG": "*", "TGA": "*", "AAA": "K",
                 "GAT": "D", "TTT": "F", "CGA": "R", "AGA": "R", "ATA": "I", "NNN": "X", "ACN": "X"}
        for cod, aa in casos.items():
            self.assertEqual(traducir(cod), aa, cod)

    def test_64_codones_son_21_simbolos(self):
        self.assertEqual(len(T._AA_TABLA), 64)
        self.assertEqual(T._AA_TABLA.count("*"), 3)
        self.assertEqual(len(set(T._AA_TABLA)), 21)


class Orf(unittest.TestCase):
    PROT = proteina_al_azar(300, 11)

    def armar(self):
        return "TAA" + cds(self.PROT) + "TAA" + "GGA"

    def test_hebra_mas_con_coordenadas(self):
        seq = self.armar()
        prot, hebra, a, b = T.orf_mas_largo(seq)
        self.assertEqual(hebra, "+")
        self.assertEqual(prot, self.PROT)
        self.assertEqual(traducir(seq[a - 1:b]), self.PROT)

    def test_hebra_menos_misma_proteina_y_coordenadas(self):
        seq = rc(self.armar())
        prot, hebra, a, b = T.orf_mas_largo(seq)
        self.assertEqual(hebra, "-")
        self.assertEqual(prot, self.PROT)
        self.assertEqual(traducir(rc(seq[a - 1:b])), self.PROT)

    def test_corto_no_cuenta(self):
        self.assertIsNone(T.orf_mas_largo(cds(proteina_al_azar(50, 3)) + "TAA"))

    def test_gana_el_mas_largo(self):
        corto = cds(proteina_al_azar(120, 5)) + "TAA"
        largo = cds(proteina_al_azar(250, 6)) + "TAA"
        self.assertIn(proteina_al_azar(250, 6), T.orf_mas_largo(corto + "C" + largo)[0])


class Nombres(unittest.TestCase):
    def test_normalizacion(self):
        n = T.normalizar_nombre
        self.assertEqual(n("Glycogen synthase kinase-3 beta isoform X2"), "glycogen synthase kinase-3 beta")
        self.assertEqual(n("shaggy-like"), "shaggy")
        self.assertEqual(n("bicaudal C homolog 1"), "bicaudal c")
        self.assertEqual(n("V-type proton ATPase subunit B"), "v-type proton atpase subunit b")

    def test_producto_refseq(self):
        self.assertEqual(T.producto_refseq("XP_1.1 foo bar isoform X1 [Macrosteles quadrilineatus]"),
                         "foo bar isoform X1")

    def test_informativo(self):
        for n in ["uncharacterized protein LOC1", "hypothetical protein", "LOW QUALITY PROTEIN: x", ""]:
            self.assertFalse(T.es_informativo(n), n)
        self.assertTrue(T.es_informativo("tubulin alpha-1 chain"))


class Bandas(unittest.TestCase):
    def test_bordes(self):
        self.assertEqual(T.banda(39.99)[0], "<40")
        self.assertEqual(T.banda(40.0)[0], "40-60")
        self.assertEqual(T.banda(89.99)[0], "80-90")
        self.assertEqual(T.banda(90.0)[0], ">=90")
        self.assertEqual(T.banda(100.0)[0], ">=90")

    def test_coinciden_con_c12(self):
        tsv = RAIZ / "research/ola3/C12_validacion_homologia/resultados/concordancia_por_identidad.tsv"
        filas = [l.split("\t") for l in tsv.read_text().splitlines()[1:]]
        for fila, b in zip(filas, T.BANDAS_C12):
            self.assertAlmostEqual(float(fila[3]), b[2], places=3)
            self.assertAlmostEqual(float(fila[4]), b[3], places=3)
            self.assertAlmostEqual(float(fila[5]), b[4], places=3)
            self.assertEqual(int(fila[2]), b[5])

    def test_rotulos_de_cobertura(self):
        self.assertEqual(T.rotulo_cobertura(95, 90), "cobertura_alta")
        self.assertEqual(T.rotulo_cobertura(95, 50), "parcial")
        self.assertEqual(T.rotulo_cobertura(95, 10), "fragmento")


def hit(sujeto, bit=100.0, pident=95.0, empate=False):
    return dict(sujeto=sujeto, bitscore=bit, pident=pident, evalue=1e-50, qcov=99.0,
                scov=98.0, longitud=300, empate=empate)


class Clasificacion(unittest.TestCase):
    PROD = {"P1": "tubulin alpha chain", "P2": "uncharacterized protein LOC2"}

    def cat(self, orf, d, i):
        return T.clasificar(orf, d, i, self.PROD)["categoria"]

    def test_las_seis_categorias(self):
        self.assertEqual(self.cat(None, {}, {}), "a_sin_orf")
        self.assertEqual(self.cat("o", {}, {}), "b_sin_hit")
        self.assertEqual(self.cat("o", {"o": hit("P1")}, {"P1": hit("otro")}), "c_hit_no_reciproco")
        self.assertEqual(self.cat("o", {"o": hit("P1")}, {}), "c_hit_no_reciproco")
        self.assertEqual(self.cat("o", {"o": hit("P1", empate=True)}, {"P1": hit("o")}), "d_empate")
        self.assertEqual(self.cat("o", {"o": hit("P1")}, {"P1": hit("o", empate=True)}), "d_empate")
        self.assertEqual(self.cat("o", {"o": hit("P2")}, {"P2": hit("o")}), "e_reciproco_sin_nombre")
        self.assertEqual(self.cat("o", {"o": hit("P1")}, {"P1": hit("o")}), "f_reciproco_con_nombre")

    def test_sin_nombre_no_transfiere_nombre_normalizado(self):
        r = T.clasificar("o", {"o": hit("P2")}, {"P2": hit("o")}, self.PROD)
        self.assertEqual(r["nombre_normalizado"], "")
        self.assertEqual(r["ref_producto"], "uncharacterized protein LOC2")  # se reporta, no se esconde

    def test_la_banda_viaja_con_la_identidad(self):
        r = T.clasificar("o", {"o": hit("P1", pident=94.0)}, {"P1": hit("o")}, self.PROD)
        self.assertEqual((r["banda_identidad"], r["banda_concordancia"], r["banda_ic_lo"], r["banda_ic_hi"]),
                         (">=90", 0.862, 0.809, 0.902))


class Cortafuego(unittest.TestCase):
    """D37: la anotacion transferida nunca entra al diseno de ARNdc."""

    def test_nadie_mas_importa_el_modulo(self):
        ignorar = {".git", "work", ".claude", "node_modules"}
        propio = Path(__file__).resolve().parent
        ofensores = []
        for p in RAIZ.rglob("*.py"):
            if ignorar & set(p.relative_to(RAIZ).parts) or propio in p.resolve().parents:
                continue
            try:
                arbol = ast.parse(p.read_text())
            except (SyntaxError, UnicodeDecodeError):
                continue
            for nodo in ast.walk(arbol):
                nombres = []
                if isinstance(nodo, ast.Import):
                    nombres = [a.name for a in nodo.names]
                elif isinstance(nodo, ast.ImportFrom):
                    nombres = [nodo.module or ""] + [a.name for a in nodo.names]
                if any("transferir_anotacion" in n for n in nombres):
                    ofensores.append(str(p.relative_to(RAIZ)))
        self.assertEqual(ofensores, [])

    def test_la_salida_no_lleva_secuencia(self):
        prohibidas = {"seq", "sequence", "secuencia", "nt", "orf_seq", "proteina", "cds", "fasta"}
        self.assertFalse(prohibidas & set(T.COLUMNAS))
        for c in T.COLUMNAS:
            self.assertNotIn("seq", c)

    def test_tablas_versionadas_sin_nucleotidos(self):
        import re
        base = Path(__file__).resolve().parent.parent / "resultados"
        for t in base.glob("transferencia_*.tsv"):
            for linea in t.read_text().splitlines()[1:]:
                for campo in linea.split("\t"):
                    self.assertIsNone(re.fullmatch(r"[ACGTNacgtn]{30,}", campo), t.name)


if __name__ == "__main__":
    unittest.main(verbosity=1)
