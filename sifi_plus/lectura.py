"""Lo comun a las vistas de lectura: abrir un archivo versionado y decir de donde salio.

Las vistas de esta linea **leen resultados y no calculan criterios** (PREREGISTRO_DEMO.md).
Este modulo es la plomeria de esa regla, y son tres cosas:

1. **Abrir un archivo declarando si estaba.** Un insumo ausente produce «no corrido» con su
   ruta y el comando que lo genera. Nunca un cero, nunca una lista vacia: el repositorio ya
   decidio que un cero tranquilizador que en realidad significa «no se miro» es el patron a
   evitar, y la interfaz lo respeta en sus tiras desde el principio.
2. **La etiqueta de procedencia.** Ningun numero sale solo: viaja con modo, motor, panel y
   archivo de origen. Si el archivo no declara su configuracion, la etiqueta dice
   «procedencia no declarada» y **no se adivina**: ni del nombre del archivo, ni del vecino,
   ni del script que lo genero.
3. **Los cuatro estados que no son el mismo estado**, que la interfaz ya distingue en sus
   tiras: sin medir, no aplica, declarado faltante y cero medido. Solo el ultimo se dibuja
   como cero.

Lo que este modulo **no** importa, a proposito y verificado por `test_api.py`: `api.py` y
cualquier cosa de `tools/sifi21_port/`. Las vistas entran por encima de la frontera que
`LEEME.md` ya trazo —`servidor.py` rutea y serializa, `api.py` traduce pedidos al motor— y por
eso no pueden mover ningun numero del motor: no lo llaman.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent

# Los tres literales con los que una vista dice que NO sabe algo. Son cadenas y no `None`
# porque viajan al navegador y se dibujan distinto, que es el punto entero: `None` en JSON es
# indistinguible de «no vino la clave».
NO_APLICA = "no aplica"
NO_DECLARADA = "procedencia no declarada"
SIN_MEDIR = "sin medir"

# Como se nombran los dos motores en la etiqueta. Los mismos nombres que `LEEME.md`, porque un
# conteo de un motor no es intercambiable con el del otro y la etiqueta tiene que dejarlo
# evidente al leerla, no al buscarla.
MOTORES = {
    "vienna": "ViennaRNA 2.7.2",
    "exe": "RNAplfold 2.1.5 (el de si-Fi21)",
}


def rel(ruta: Path) -> str:
    """La ruta como se cita en el repositorio: relativa a la raiz y con barras POSIX.

    Con el separador de la plataforma la misma ruta se escribe distinto en Windows y en macOS,
    y despues no se puede buscar en un REPORT. `compuerta.py` ya se habia tropezado con esto.
    """
    try:
        return Path(ruta).resolve().relative_to(RAIZ).as_posix()
    except ValueError:
        return Path(ruta).as_posix()


def falta(ruta: Path, comando: str = "") -> dict:
    """El bloque «no corrido» de una vista: que archivo falta y como se genera.

    No lleva ninguna cifra. Una vista que recibe esto dibuja el aviso y nada mas; si pusiera
    un cero al lado, el cero seria una afirmacion sobre algo que nadie midio.
    """
    return {"estado": "no corrido", "archivo": rel(ruta),
            "motivo": "no esta en disco", "comando": comando}


def leer_tsv(ruta: Path, comando: str = "") -> tuple[list[dict], dict | None]:
    """Las filas de un TSV, o el bloque «no corrido» si el archivo no esta.

    Devuelve `(filas, problema)`: una de las dos es siempre vacia. Los TSV de `research/` se
    escribieron desde Windows y vienen con CRLF; `newline=""` deja que `csv` lo resuelva en vez
    de que un `\\r` quede pegado al final de la ultima columna de cada fila.
    """
    ruta = Path(ruta)
    if not ruta.is_file():
        return [], falta(ruta, comando)
    with ruta.open(encoding="utf-8", newline="") as fh:
        filas = [f for f in csv.DictReader(fh, delimiter="\t")
                 if any((v or "").strip() for v in f.values())]
    return filas, None


def leer_json(ruta: Path, comando: str = "") -> tuple[dict | list | None, dict | None]:
    """Lo mismo para un JSON. Un archivo ilegible tampoco es un cero: es un «no corrido»."""
    ruta = Path(ruta)
    if not ruta.is_file():
        return None, falta(ruta, comando)
    try:
        with ruta.open(encoding="utf-8") as fh:
            return json.load(fh), None
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        p = falta(ruta, comando)
        p["motivo"] = "esta en disco pero no se puede leer: %s" % e
        return None, p


def procedencia(archivo, *, modo=NO_DECLARADA, motor=NO_DECLARADA,
                panel=NO_DECLARADA, nota: str = "") -> dict:
    """La etiqueta que acompana a cada numero. Los cuatro campos van siempre.

    El valor por defecto de los tres campos es **«procedencia no declarada»** y no una cadena
    vacia: una vista que se olvida de pasar el modo tiene que mostrar que no lo sabe, no un
    hueco que se lee como que no hacia falta. `NO_APLICA` se pasa explicitamente, porque «esta
    cifra no depende del motor» es una afirmacion sobre la cifra y alguien la tiene que hacer.
    """
    if isinstance(panel, (list, tuple, set)):
        panel = sorted(panel)
    return {"modo": modo, "motor": motor, "panel": panel, "archivo": rel(archivo),
            "declarada": NO_DECLARADA not in (modo, motor, panel),
            "nota": nota}


def entero(v, por_defecto=None):
    """Un entero de una celda de TSV, o `por_defecto` si la celda no lo tiene.

    Una celda vacia **no es un cero**: devuelve `None` y la vista la dibuja como «sin medir».
    `estado_regiones.tsv` tiene celdas con el literal «no aplica» en las filas de juntura, que
    es un tercer estado y tampoco es cero.
    """
    s = str(v if v is not None else "").strip()
    if not s:
        return por_defecto
    try:
        return int(s)
    except ValueError:
        return por_defecto


def tramos(posiciones) -> list[list[int]]:
    """Posiciones consecutivas agrupadas en tramos `[inicio, fin]`.

    El mismo recorte que `app.js` hace para las tiras: una marca por tramo y no por posicion.
    Las veintidos ventanas de `BicC_Dm` 264-563 son dos tramos, no veintidos marcas.
    """
    out: list[list[int]] = []
    for p in sorted(set(int(x) for x in posiciones)):
        if out and p == out[-1][1] + 1:
            out[-1][1] = p
        else:
            out.append([p, p])
    return out
