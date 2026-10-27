"""Verificaciones de `comparar_json.py`.

Son todas propiedades del comparador sobre pares construidos a mano: no dependen de
ningun archivo del repo ni de `work/`, asi que corren en cualquier maquina.

Lo que importa que quede fijado es la distincion que motiva la herramienta (D76): el
orden de las claves de un objeto **no** es una diferencia, y una cifra que se mueve **si**
lo es. Un comparador que confundiera las dos cosas no serviria para lo que hace falta.

    python tools/verificacion/test_comparar_json.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import comparar_json as C

FALLAS = []


def check(cond, msg):
    if cond:
        print("  ok   %s" % msg)
    else:
        print("  FALLA %s" % msg)
        FALLAS.append(msg)


def test_orden_de_claves_no_es_diferencia():
    print("el orden de las claves de un objeto no es una diferencia de valor")
    a = {"maiz": 1, "humano": 2, "F_candida": 3}
    b = {"F_candida": 3, "maiz": 1, "humano": 2}
    r = C.comparar(a, b)
    check(r.valores == [], "sin diferencias de valor")
    check(r.iguales, "los dos JSON son iguales por valor")
    check([o.ruta for o in r.orden] == [""], "el reordenamiento se reporta aparte, en la raiz")
    check(r.orden[0].antes == ["maiz", "humano", "F_candida"], "deja ver el orden de A")
    check(r.orden[0].despues == ["F_candida", "maiz", "humano"], "deja ver el orden de B")


def test_una_cifra_que_se_mueve_si_lo_es():
    print("una cifra que se mueve es una diferencia, con su ruta")
    a = {"k": {"21": {"fichas": [{"gen": "MP_MRFV", "ventanas": 123}]}}}
    b = {"k": {"21": {"fichas": [{"gen": "MP_MRFV", "ventanas": 124}]}}}
    r = C.comparar(a, b)
    check(not r.iguales, "no son iguales")
    check(len(r.valores) == 1, "una sola diferencia")
    d = r.valores[0]
    check(d.ruta == "/k/21/fichas/0/ventanas", "la ruta es %r" % d.ruta)
    check((d.antes, d.despues) == (123, 124), "dice el antes y el despues")
    check(d.clase == "valor", "clase 'valor', es %r" % d.clase)


def test_clave_agregada_y_clave_que_falta():
    print("una clave nueva y una que desaparece se distinguen entre si")
    a = {"x": 1, "se_va": 9}
    b = {"x": 1, "llega": 8}
    r = C.comparar(a, b)
    clases = sorted((d.clase, d.ruta) for d in r.valores)
    check(clases == [("solo_en_a", "/se_va"), ("solo_en_b", "/llega")],
          "las dos clases con su ruta: %r" % (clases,))
    check(r.valores[0].antes == 9 or r.valores[1].antes == 9,
          "el valor que se va queda registrado")


def test_listas_se_comparan_por_indice_y_por_largo():
    print("las listas se comparan por indice, y un largo distinto se reporta una vez")
    r = C.comparar({"l": [1, 2, 3]}, {"l": [1, 7, 3]})
    check([(d.ruta, d.clase) for d in r.valores] == [("/l/1", "valor")],
          "un elemento distinto apunta a su indice")
    r = C.comparar({"l": [1, 2]}, {"l": [1, 2, 3]})
    check([(d.ruta, d.clase) for d in r.valores] == [("/l", "largo")],
          "el largo se reporta en la lista y no elemento por elemento")
    check((r.valores[0].antes, r.valores[0].despues) == (2, 3), "con los dos largos")


def test_entero_y_flotante_con_el_mismo_valor_no_mueven_ninguna_cifra():
    print("1 y 1.0 son la misma cifra; True y 1 no son lo mismo")
    check(C.comparar({"n": 1}, {"n": 1.0}).iguales, "1 contra 1.0: iguales")
    check(C.comparar({"n": 0.5000}, {"n": 0.5}).iguales, "0.5000 contra 0.5: iguales")
    r = C.comparar({"n": 1}, {"n": True})
    check(not r.iguales and r.valores[0].clase == "tipo",
          "1 contra true: diferencia de tipo, no de valor")
    r = C.comparar({"n": None}, {"n": 0})
    check(not r.iguales and r.valores[0].clase == "tipo", "null contra 0: diferencia de tipo")


def test_un_objeto_contra_una_lista_es_diferencia_de_tipo():
    print("un objeto donde antes habia una lista es una diferencia de tipo")
    r = C.comparar({"x": {"a": 1}}, {"x": [1]})
    check([(d.ruta, d.clase) for d in r.valores] == [("/x", "tipo")],
          "se reporta en /x y no se intenta recorrer dentro")


def test_el_orden_se_reporta_en_cada_objeto_anidado():
    print("el reordenamiento se reporta en el objeto donde ocurre")
    a = {"fichas": [{"r": {"maiz": 1, "humano": 2}}]}
    b = {"fichas": [{"r": {"humano": 2, "maiz": 1}}]}
    r = C.comparar(a, b)
    check(r.iguales, "iguales por valor")
    check([o.ruta for o in r.orden] == ["/fichas/0/r"], "la ruta del objeto reordenado")


def test_resumen_cuenta_las_dos_cosas_por_separado():
    print("el resumen separa diferencias de valor de objetos reordenados")
    a = {"r": {"maiz": 1, "humano": 2}, "n": 5}
    b = {"r": {"humano": 2, "maiz": 1}, "n": 6}
    r = C.comparar(a, b)
    check(r.resumen() == "1 diferencia de valor, 1 objeto con otro orden de claves",
          "resumen: %r" % r.resumen())
    r = C.comparar({"n": 1}, {"n": 1})
    check(r.resumen() == "identicos valor por valor, y con el mismo orden de claves",
          "resumen de iguales: %r" % r.resumen())


def main():
    for t in (test_orden_de_claves_no_es_diferencia,
              test_una_cifra_que_se_mueve_si_lo_es,
              test_clave_agregada_y_clave_que_falta,
              test_listas_se_comparan_por_indice_y_por_largo,
              test_entero_y_flotante_con_el_mismo_valor_no_mueven_ninguna_cifra,
              test_un_objeto_contra_una_lista_es_diferencia_de_tipo,
              test_el_orden_se_reporta_en_cada_objeto_anidado,
              test_resumen_cuenta_las_dos_cosas_por_separado):
        t()
    print()
    if FALLAS:
        print("FALLARON %d verificaciones" % len(FALLAS))
        return 1
    print("todas las verificaciones pasaron")
    return 0


if __name__ == "__main__":
    sys.exit(main())
