"""Traduce pedidos de la interfaz al motor del port. No tiene logica de criterio.

Regla de este archivo: aca no se decide nunca si una ventana es eficiente. Eso lo hace
`tools/sifi21_port/sifi_core.py` y nada mas. Este modulo arma los parametros, llama, y
devuelve el contrato de `perfil.py`. Si alguna vez aparece un `if` sobre nucleotidos en este
archivo, esta mal.

Todo lo que se escribe en disco va a `work/sifi_plus/`, que esta fuera del control de
versiones (`work/` en `.gitignore`). La carpeta `sifi_plus/` guarda codigo, no resultados: es
lo que hace que la entrega al investigador no dependa de una auditoria archivo por archivo.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
PORT = RAIZ / "tools" / "sifi21_port"
SALIDAS = RAIZ / "work" / "sifi_plus"

# Mismo patron que los scripts del port: cada modulo agrega lo que necesita, asi todo
# funciona con `python -I`, que no pone el directorio actual en el path.
sys.path.insert(0, str(PORT))
sys.path.insert(0, str(AQUI))

from sifi_core import (  # noqa: E402
    DEFAULTS,
    RUTAS_RNAPLFOLD,
    SifiEngine,
    best_region,
    resolver_rnaplfold,
)

import perfil  # noqa: E402

# --- Que motores hay en esta maquina ---------------------------------------
# El si-Fi21 original falla aca y en silencio: `run_rnaplfold` le pasa `cwd` a Popen con el
# ejecutable por nombre pelado, no lo encuentra, cae en un `else` que nunca asigna
# `lunp_data`, y el UnboundLocalError se lo traga el slot de Qt. El sintoma es que el boton
# Start no hace nada. Aca se averigua al arrancar y se dice que falta y por que.


def motores() -> list[dict]:
    """Los motores de accesibilidad, con su disponibilidad y el motivo si falta."""
    out = []

    try:
        import RNA
        out.append({"id": "vienna", "nombre": "ViennaRNA %s" % RNA.__version__,
                    "disponible": True, "motivo": ""})
    except ImportError as e:
        out.append({"id": "vienna", "nombre": "ViennaRNA (ligaduras de Python)",
                    "disponible": False,
                    "motivo": "no se puede importar el modulo RNA: %s. "
                              "Instalalo con: pip install ViennaRNA==2.7.2" % e})

    exe = Path(resolver_rnaplfold())
    if exe.is_file():
        out.append({"id": "exe", "nombre": "RNAplfold 2.1.5 (el de si-Fi21)",
                    "disponible": True, "motivo": "", "ruta": str(exe)})
    else:
        out.append({"id": "exe", "nombre": "RNAplfold 2.1.5 (el de si-Fi21)",
                    "disponible": False,
                    "motivo": "no lo encontre. Busque en: %s. Es el binario que trae el "
                              "instalador de si-Fi2015 (ViennaRNA 2.1.5); si lo tenes en "
                              "otro lugar, o lo compilaste fuera de Windows, exporta "
                              "SIFI_RNAPLFOLD con su ruta absoluta."
                              % "; ".join(RUTAS_RNAPLFOLD)})
    return out


# --- Parametros ------------------------------------------------------------
# Superconjunto estricto del panel del original (`Resources/sifi2015.ui`): tamano de siRNA,
# las cuatro casillas, umbral de extremos, umbral de accesibilidad y ventana de
# accesibilidad. Encima: modo, motor, temperatura, tabla de vecinos y largo de region.

PRESETS = {
    # Los dos perfiles del manual (paginas 7 y 11), que el original pone en el boton
    # «Default Settings» segun el modo con el que se abrio.
    "diseno": {"strand_check": True, "end_check": True, "accessibility_check": True,
               "terminal_check": True, "end_stability_threshold": 1.0,
               "accessibility_threshold": 0.1, "accessibility_window": 8,
               "sirna_size": 21},
    "offtarget": {"strand_check": True, "end_check": False, "accessibility_check": False,
                  "terminal_check": True, "end_stability_threshold": 1.0,
                  "accessibility_threshold": 0.1, "accessibility_window": 8,
                  "sirna_size": 21},
}

CASILLAS = ["strand_check", "end_check", "accessibility_check", "terminal_check"]


def cadena_config(p: dict) -> str:
    """La configuracion en el formato en que el investigador declaro la suya.

    `siFi21_8_1.0_0.1_1111` se decodifica contra `main.py:344-362` del fuente original como
    ventana de accesibilidad, umbral de extremos, umbral de accesibilidad y las cuatro
    casillas (D45). El orden de los cuatro digitos es el del panel —seleccion de hebra,
    estabilidad de extremos, accesibilidad del sitio, regla terminal—; con `1111` el dato
    original no permite distinguirlo, asi que ese orden es nuestra lectura `[H]`.
    """
    bits = "".join("1" if p.get(c, DEFAULTS[c]) else "0" for c in CASILLAS)
    return "siFi21_%d_%s_%s_%s" % (
        p.get("accessibility_window", DEFAULTS["accessibility_window"]),
        _num(p.get("end_stability_threshold", DEFAULTS["end_stability_threshold"])),
        _num(p.get("accessibility_threshold", DEFAULTS["accessibility_threshold"])),
        bits)


def _num(v: float) -> str:
    """1.0 y 0.1 como los escribe el investigador, sin ceros de relleno."""
    s = ("%g" % float(v))
    return s if "." in s else s + ".0"


def parsear_config(s: str) -> dict:
    """Lee una cadena `siFi21_u_end_acc_bbbb` y devuelve los parametros.

    Levanta ValueError con un mensaje legible si no tiene la forma: es un campo que el
    usuario escribe a mano y el error tiene que decir que esperaba.
    """
    partes = s.strip().split("_")
    if len(partes) != 5 or partes[0].lower() != "sifi21":
        raise ValueError("se esperaba siFi21_<ventana>_<extremos>_<accesibilidad>_<4 bits>, "
                         "por ejemplo siFi21_8_1.0_0.1_1111")
    bits = partes[4]
    if len(bits) != 4 or set(bits) - {"0", "1"}:
        raise ValueError("los cuatro ultimos digitos son las cuatro casillas, 0 o 1 cada "
                         "una; recibi %r" % bits)
    try:
        p = {"accessibility_window": int(partes[1]),
             "end_stability_threshold": float(partes[2]),
             "accessibility_threshold": float(partes[3])}
    except ValueError:
        raise ValueError("ventana entera y los dos umbrales numericos; recibi %r, %r, %r"
                         % (partes[1], partes[2], partes[3])) from None
    for c, b in zip(CASILLAS, bits):
        p[c] = (b == "1")
    return p


def normalizar(crudo: dict) -> dict:
    """Valida lo que llega del navegador y lo deja listo para SifiEngine.

    Se valida en el servidor y no en el formulario porque el formulario se puede saltear, y
    un parametro fuera de rango que llega hasta ViennaRNA aborta con un error que no dice
    nada util.
    """
    p = dict(DEFAULTS)
    p.update({k: v for k, v in crudo.items() if k in DEFAULTS})

    size = int(p["sirna_size"])
    if not 10 <= size <= 50:
        raise ValueError("el tamano de siRNA tiene que estar entre 10 y 50 nt; recibi %d"
                         % size)
    u = int(p["accessibility_window"])
    if not 1 <= u <= size:
        raise ValueError("la ventana de accesibilidad va de 1 al tamano del siRNA (%d); "
                         "recibi %d. El original la fija en 8." % (size, u))
    acc = float(p["accessibility_threshold"])
    if not 0.0 <= acc <= 1.0:
        raise ValueError("el umbral de accesibilidad es una probabilidad, entre 0 y 1; "
                         "recibi %s" % acc)
    p["sirna_size"] = size
    p["accessibility_window"] = u
    p["accessibility_threshold"] = acc
    p["end_stability_threshold"] = float(p["end_stability_threshold"])
    for c in CASILLAS:
        p[c] = bool(p[c])
    return p


# --- Correr ----------------------------------------------------------------


def leer_fasta(texto: str) -> list[tuple[str, str]]:
    """[(nombre, secuencia)] de un FASTA simple o multiple, o de secuencia pelada.

    Misma semantica que `run_sifi.leer_fastas` (el nombre es el primer token del encabezado),
    pero sobre texto en memoria, porque aca la secuencia llega pegada en un formulario y
    nunca toca el disco si el usuario no exporta.
    """
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    if ">" not in texto:
        seq = "".join(texto.split())
        return [("secuencia_pegada", seq)] if seq else []

    nombre, buf, out = None, [], []
    for linea in texto.split("\n"):
        if linea.startswith(">"):
            if nombre is not None:
                out.append((nombre, "".join(buf)))
            cab = linea[1:].strip()
            nombre = (cab.split()[0] if cab.split() else "sin_nombre")
            buf = []
        elif nombre is not None:
            buf.append(linea.strip())
    if nombre is not None:
        out.append((nombre, "".join(buf)))
    return [(n, s) for n, s in out if s]


def correr_diseno(secuencia: str, *, nombre="secuencia", modo="corregido",
                  backend="vienna", temp_c=22.0, tabla_nn="NN3", largo_region=200,
                  params=None, bandas=None, off_perfecto=None, off_mm1=None):
    """Corre el criterio sobre una secuencia y devuelve (ventanas, resumen, contrato).

    El motor es `SifiEngine`, importado en proceso: la interfaz no recalcula nada y no puede
    discrepar del CLI, porque es el mismo objeto.
    """
    p = normalizar(params or {})
    eng = SifiEngine(mode=modo, temp_c=temp_c, tabla_nn=tabla_nn, **p)
    ventanas, resumen = eng.run(secuencia, backend=backend)

    L = min(largo_region, len(ventanas))
    mejor = best_region(ventanas, L)
    resumen["nombre"] = nombre
    resumen["tabla_nn"] = tabla_nn
    resumen["mejor_region_%dnt" % L] = mejor
    resumen["config"] = cadena_config(p)
    resumen["params"] = p

    etq = "modo %s · %s · %.0f °C · %s" % (
        modo, _nombre_motor(backend), temp_c, tabla_nn)

    c = perfil.contrato(
        nombre=nombre, ventanas=ventanas, resumen=resumen,
        largo=resumen["largo"], size=p["sirna_size"], largo_region=L, mejor=mejor,
        off_perfecto=off_perfecto, off_mm1=off_mm1, bandas=bandas, etiqueta=etq)
    return ventanas, resumen, c


def _nombre_motor(backend: str) -> str:
    for m in motores():
        if m["id"] == backend:
            return m["nombre"]
    return backend


def cuenta_en(rango: tuple[int, int], posiciones) -> int:
    """Cuantas posiciones de `posiciones` caen en el rango cerrado `rango`."""
    if posiciones is None:
        return 0
    a, b = rango
    return sum(1 for p in posiciones if a <= p <= b)
