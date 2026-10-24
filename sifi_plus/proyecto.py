"""Los rangos candidatos: guardarlos, listarlos, compararlos.

El original no tiene nada de esto. Se corre, se mira el grafico, y si uno quiere anotar «la
region 264-563 de este gen daba 199 eficientes» lo escribe en un papel. Elegir region es la
decision que la herramienta existe para apoyar, asi que la decision tiene que quedar guardada
con los numeros que la justificaron y con la configuracion que los produjo: un conteo sin su
modo y su motor no significa nada, porque los cuatro genes dan cuatro numeros distintos segun
cual de los dos RNAplfold corrio.

Donde se guarda y por que: `work/sifi_plus/proyectos/`, fuera del control de versiones. Un
rango guardado son coordenadas y conteos, nunca secuencia, y eso se impone en el codigo
—`_sin_secuencias` descarta cualquier valor con pinta de nucleotidos— en vez de confiar en
que el que llame se acuerde. El repositorio ya tuvo un incidente de 21-meros commiteados
(C9), y la leccion que dejo es que la contencion se escribe, no se recuerda.
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

from api import SALIDAS  # noqa: E402

CARPETA = SALIDAS / "proyectos"
RE_NT = re.compile(r"^[ACGTUacgtu]{12,}$")

# Lo que se guarda de un rango. Explicito, para que agregar un campo sea una decision y no un
# descuido: cualquier clave que no este aca no se escribe.
CAMPOS = ("nombre", "gen", "inicio", "fin", "largo", "eficientes", "densidad",
          "off_perfecto", "off_mm1", "modo", "motor", "config", "etiqueta", "nota",
          "temp_c", "tabla_nn", "creado")


def _sin_secuencias(d: dict) -> dict:
    """Descarta valores que parezcan secuencia. La contencion se impone, no se recuerda."""
    out = {}
    for k, v in d.items():
        if isinstance(v, str) and RE_NT.match(v.strip()):
            continue
        out[k] = v
    return out


def _slug(s: str) -> str:
    s = "".join(c if (c.isalnum() or c in "-_") else "_" for c in (s or "").strip())
    return (s or "rango")[:60]


def guardar(rango: dict) -> dict:
    """Escribe un rango candidato y devuelve lo que quedo guardado."""
    limpio = _sin_secuencias({k: v for k, v in rango.items() if k in CAMPOS})
    for req in ("gen", "inicio", "fin"):
        if limpio.get(req) in (None, ""):
            raise ValueError("falta %r: un rango sin gen y sin coordenadas no se puede "
                             "comparar con nada" % req)
    limpio["inicio"] = int(limpio["inicio"])
    limpio["fin"] = int(limpio["fin"])
    if limpio["fin"] < limpio["inicio"]:
        limpio["inicio"], limpio["fin"] = limpio["fin"], limpio["inicio"]
    limpio["largo"] = limpio["fin"] - limpio["inicio"] + 1
    limpio["creado"] = time.strftime("%Y-%m-%d %H:%M:%S")
    limpio.setdefault("nombre", "%s %d-%d" % (limpio["gen"], limpio["inicio"], limpio["fin"]))

    CARPETA.mkdir(parents=True, exist_ok=True)
    archivo = "%s__%s_%d-%d.json" % (_slug(limpio["nombre"]), _slug(limpio["gen"]),
                                     limpio["inicio"], limpio["fin"])
    limpio["id"] = archivo
    (CARPETA / archivo).write_text(
        json.dumps(limpio, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return limpio


def listar() -> list[dict]:
    """Todos los rangos guardados, el mas reciente primero."""
    if not CARPETA.is_dir():
        return []
    out = []
    for p in CARPETA.glob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            # Un archivo ilegible se informa, no se adivina ni se borra.
            out.append({"id": p.name, "nombre": p.name, "error": "no se pudo leer"})
            continue
        d["id"] = p.name
        out.append(d)
    out.sort(key=lambda d: d.get("creado", ""), reverse=True)
    return out


def borrar(ident: str) -> bool:
    """Borra un rango por su id. Devuelve si existia."""
    p = CARPETA / Path(ident).name
    if p.is_file() and p.parent == CARPETA:
        p.unlink()
        return True
    return False
