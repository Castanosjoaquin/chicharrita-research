"""Verificaciones del conversor de markdown a HTML.

Existe porque en la ola 4 el conversor paso de cubrir titulos, parrafos y tablas a
cubrir tambien cercas de codigo y listas, y las listas tienen cuatro formas que es
facil romper sin que se note en la pagina: la continuacion de un item, la sublista
anidada, una cerca indentada adentro de un item y la regla horizontal escrita con
espacios (`- - -`), que no es un item.

Uso:
    python tools/test_md_a_html.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import md_a_html as m


def html_de(md: str) -> str:
    return m.convertir(md)[1]


class TestListas(unittest.TestCase):

    def test_una_viñeta_simple(self):
        self.assertEqual(html_de("- uno\n- dos\n"), "<ul><li>uno</li><li>dos</li></ul>")

    def test_una_numerada_simple(self):
        self.assertEqual(html_de("1. uno\n2. dos\n"), "<ol><li>uno</li><li>dos</li></ol>")

    def test_la_continuacion_indentada_entra_al_mismo_item(self):
        self.assertEqual(html_de("- uno\n  sigue\n- dos\n"),
                         "<ul><li>uno sigue</li><li>dos</li></ul>")

    def test_la_continuacion_sin_sangria_tambien(self):
        # Markdown la mantiene adentro del item; antes quedaba como parrafo suelto.
        self.assertEqual(html_de("- uno\nsigue\n"), "<ul><li>uno sigue</li></ul>")

    def test_la_sublista_queda_anidada_y_no_aplanada(self):
        self.assertEqual(html_de("- uno\n  - a\n  - b\n- dos\n"),
                         "<ul><li>uno<ul><li>a</li><li>b</li></ul></li>"
                         "<li>dos</li></ul>")

    def test_la_viñeta_despues_de_una_numerada_son_dos_listas(self):
        self.assertEqual(html_de("1. uno\n- dos\n"),
                         "<ol><li>uno</li></ol>\n<ul><li>dos</li></ul>")

    def test_el_blanco_cierra_la_lista(self):
        self.assertEqual(html_de("- uno\n\ntexto\n"),
                         "<ul><li>uno</li></ul>\n<p>texto</p>")

    def test_la_tabla_despues_de_una_lista_cierra_la_lista(self):
        salida = html_de("- uno\n| a | b |\n|---|---|\n| 1 | 2 |\n")
        self.assertTrue(salida.startswith("<ul><li>uno</li></ul>"))
        self.assertIn("<table>", salida)


class TestReglaHorizontal(unittest.TestCase):

    def test_los_guiones_pegados(self):
        self.assertEqual(html_de("---\n"), "<hr>")

    def test_la_regla_con_espacios_no_es_un_item(self):
        # `- - -` entraba como item de lista con el texto `- -`.
        for s in ("- - -", "* * *", "___", "***"):
            self.assertEqual(html_de(s + "\n"), "<hr>", s)

    def test_la_regla_cierra_la_lista(self):
        self.assertEqual(html_de("- uno\n\n---\n"), "<ul><li>uno</li></ul>\n<hr>")


class TestCercas(unittest.TestCase):

    def test_la_cerca_conserva_los_saltos_de_linea(self):
        self.assertEqual(html_de("```bash\nuno \\\n    dos\n```\n"),
                         "<pre>uno \\\n    dos</pre>")

    def test_la_cerca_escapa_el_html(self):
        self.assertIn("&lt;pos&gt;", html_de("```\nw<pos>\n```\n"))

    def test_la_cerca_indentada_no_corta_la_numeracion(self):
        # Antes cerraba la lista y el `2.` abria un <ol> nuevo, que se dibuja como 1.
        salida = html_de("1. uno\n\n   ```\n   comando\n   ```\n\n2. dos\n")
        self.assertEqual(salida.count("<ol>"), 1, salida)
        self.assertEqual(salida.count("<li>"), 2, salida)
        self.assertIn("<pre>comando</pre>", salida)

    def test_la_cerca_indentada_pierde_la_sangria_comun(self):
        salida = html_de("- uno\n\n  ```\n  a\n    b\n  ```\n")
        self.assertIn("<pre>a\n  b</pre>", salida)

    def test_la_cerca_sin_cerrar_igual_se_emite(self):
        self.assertEqual(html_de("```\nuno\n"), "<pre>uno</pre>")


class TestNoRompeLoQueYaFuncionaba(unittest.TestCase):

    def test_titulo_subtitulos_y_parrafo(self):
        titulo, cuerpo = m.convertir("# T\n\n## Dos\n\nparrafo\ncontinua\n")
        self.assertEqual(titulo, "T")
        self.assertEqual(cuerpo, "<h2>Dos</h2>\n<p>parrafo continua</p>")

    def test_la_tabla_sigue_saliendo_igual(self):
        salida = html_de("| a | b |\n|---|---|\n| 1 | 2 |\n")
        self.assertIn("<th>a</th><th>b</th>", salida)
        self.assertIn("<td>1</td><td>2</td>", salida)

    def test_el_codigo_en_linea_y_la_negrita(self):
        self.assertEqual(html_de("**x** y `z`\n"), "<p><b>x</b> y <code>z</code></p>")


class TestDocumentosDelRepositorio(unittest.TestCase):
    """Ancla contra el disco: los HTML ya generados no tienen que cambiar.

    Solo se comparan los documentos cuyo markdown no usa listas ni cercas, que son
    los que el cambio de la ola 4 no deberia tocar. Los que si las usan cambian a
    proposito, y se regeneran cuando corresponda.
    """

    RAIZ = Path(__file__).resolve().parents[1]
    PARES = [("entregables/para-el-investigador.md", "entregables/para-el-investigador.html"),
             ("entregables/checkpoint2-una-pagina.md", "entregables/checkpoint2-una-pagina.html")]

    def test_los_html_sin_listas_ni_cercas_salen_identicos(self):
        for md, htm in self.PARES:
            fuente, destino = self.RAIZ / md, self.RAIZ / htm
            if not (fuente.exists() and destino.exists()):
                self.skipTest(f"falta {md} o {htm}")
            texto = fuente.read_text(encoding="utf-8")
            if "```" in texto or any(m.marca(l) for l in texto.split("\n")):
                continue
            titulo, cuerpo = m.convertir(texto)
            self.assertIn(cuerpo, destino.read_text(encoding="utf-8"), md)


if __name__ == "__main__":
    unittest.main(verbosity=2)
