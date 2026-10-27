"""Compara dos JSON por valor y no por texto, y reporta el reordenamiento aparte.

Existe por un problema concreto (D76): al regenerar
`research/ola3/C7_ranking_v2/resultados/ranking_v2.json` el diff textual salio de unas
300 lineas sin que se moviera una sola cifra, porque el orden de las claves de los
objetos por referencia lo heredaba del orden de las columnas del TSV de off-targets.
Afirmar «ninguna cifra se movio» hizo falta una comparacion estructural escrita a mano.
Esto la deja hecha, para que la proxima regeneracion se pueda revisar sin rehacer el
trabajo.

La distincion que hace la herramienta:

  - **diferencia de valor**: una cifra que cambia, una clave que aparece o desaparece,
    un tipo que cambia, una lista de otro largo. Es lo que decide el codigo de salida.
  - **reordenamiento**: un objeto con las mismas claves y los mismos valores en otro
    orden. Se reporta, porque explica el diff textual, pero no es una diferencia.

Un entero y un flotante con el mismo valor son la misma cifra (`1` y `1.0`); `true` y
`1` no lo son, ni `null` y `0`.

    python tools/verificacion/comparar_json.py <a.json> <b.json> [--sin-orden] [--max N]

Sale 0 si no hay diferencias de valor, 1 si hay, y 2 si un archivo no se puede leer.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

NUMEROS = (int, float)


@dataclass
class Diferencia:
    ruta: str
    clase: str          # valor | tipo | largo | solo_en_a | solo_en_b
    antes: object = None
    despues: object = None

    def __str__(self) -> str:
        if self.clase == "solo_en_a":
            return "%s: solo en A (%s)" % (self.ruta or "/", _corto(self.antes))
        if self.clase == "solo_en_b":
            return "%s: solo en B (%s)" % (self.ruta or "/", _corto(self.despues))
        if self.clase == "largo":
            return "%s: lista de %d contra %d elementos" % (self.ruta or "/", self.antes,
                                                            self.despues)
        etiqueta = "tipo" if self.clase == "tipo" else "valor"
        return "%s: %s %s -> %s" % (self.ruta or "/", etiqueta, _corto(self.antes),
                                    _corto(self.despues))


@dataclass
class Reorden:
    ruta: str
    antes: list
    despues: list

    def __str__(self) -> str:
        return "%s: %s -> %s" % (self.ruta or "/", ", ".join(map(str, self.antes)),
                                 ", ".join(map(str, self.despues)))


@dataclass
class Resultado:
    valores: list = field(default_factory=list)
    orden: list = field(default_factory=list)

    @property
    def iguales(self) -> bool:
        """Iguales **por valor**. Puede ser True con objetos reordenados."""
        return not self.valores

    def resumen(self) -> str:
        if self.iguales and not self.orden:
            return "identicos valor por valor, y con el mismo orden de claves"
        partes = []
        if self.valores:
            partes.append(_plural(len(self.valores), "diferencia de valor",
                                  "diferencias de valor"))
        else:
            partes.append("identicos valor por valor")
        if self.orden:
            partes.append(_plural(len(self.orden), "objeto con otro orden de claves",
                                  "objetos con otro orden de claves"))
        return ", ".join(partes)


def _plural(n, uno, varios) -> str:
    return "%d %s" % (n, uno if n == 1 else varios)


def _corto(v, tope=60) -> str:
    t = json.dumps(v, ensure_ascii=False, sort_keys=True)
    return t if len(t) <= tope else t[:tope - 3] + "..."


def _familia(v) -> str:
    """La clase de valor JSON. `bool` va aparte de los numeros a proposito."""
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, NUMEROS):
        return "numero"
    if isinstance(v, str):
        return "texto"
    if isinstance(v, dict):
        return "objeto"
    if isinstance(v, list):
        return "lista"
    return type(v).__name__


def comparar(a, b, ruta: str = "") -> Resultado:
    """Recorre los dos arboles en paralelo y junta diferencias y reordenamientos."""
    r = Resultado()
    _recorrer(a, b, ruta, r)
    return r


def _recorrer(a, b, ruta: str, r: Resultado) -> None:
    fa, fb = _familia(a), _familia(b)
    if fa != fb:
        r.valores.append(Diferencia(ruta, "tipo", a, b))
        return
    if fa == "objeto":
        _objetos(a, b, ruta, r)
    elif fa == "lista":
        _listas(a, b, ruta, r)
    elif a != b:
        r.valores.append(Diferencia(ruta, "valor", a, b))


def _objetos(a: dict, b: dict, ruta: str, r: Resultado) -> None:
    # Las claves comunes se recorren en el orden de A, para que el reporte siga la
    # lectura del archivo publicado y no un orden inventado.
    comunes = [k for k in a if k in b]
    if [k for k in b if k in a] != comunes:
        r.orden.append(Reorden(ruta, list(a), list(b)))
    for k in a:
        if k not in b:
            r.valores.append(Diferencia("%s/%s" % (ruta, k), "solo_en_a", antes=a[k]))
    for k in comunes:
        _recorrer(a[k], b[k], "%s/%s" % (ruta, k), r)
    for k in b:
        if k not in a:
            r.valores.append(Diferencia("%s/%s" % (ruta, k), "solo_en_b", despues=b[k]))


def _listas(a: list, b: list, ruta: str, r: Resultado) -> None:
    if len(a) != len(b):
        # Con largos distintos no se intenta alinear: cualquier emparejamiento seria
        # una suposicion, y lo que hay que revisar a mano es el largo.
        r.valores.append(Diferencia(ruta, "largo", len(a), len(b)))
        return
    for i, (x, y) in enumerate(zip(a, b)):
        _recorrer(x, y, "%s/%d" % (ruta, i), r)


def _leer(ruta: Path):
    try:
        with ruta.open(encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as e:
        print("no pude leer %s: %s" % (ruta, e), file=sys.stderr)
        return None


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("a", type=Path, help="JSON de referencia")
    p.add_argument("b", type=Path, help="JSON a comparar contra el de referencia")
    p.add_argument("--sin-orden", action="store_true",
                   help="no listar los objetos reordenados (igual se cuentan)")
    p.add_argument("--max", type=int, default=40, metavar="N",
                   help="cuantas lineas listar por seccion (0 = todas)")
    a = p.parse_args(argv)

    da, db = _leer(a.a), _leer(a.b)
    if da is None or db is None:
        return 2

    r = comparar(da, db)
    print("A: %s" % a.a)
    print("B: %s" % a.b)
    print(r.resumen())
    for titulo, items, mostrar in (("diferencias de valor", r.valores, True),
                                   ("objetos con otro orden de claves", r.orden,
                                    not a.sin_orden)):
        if not items or not mostrar:
            continue
        print()
        print("%s (%d):" % (titulo, len(items)))
        tope = len(items) if a.max == 0 else min(a.max, len(items))
        for it in items[:tope]:
            print("   -", it)
        if tope < len(items):
            print("   ... y %d mas" % (len(items) - tope))
    return 1 if r.valores else 0


if __name__ == "__main__":
    sys.exit(main())
