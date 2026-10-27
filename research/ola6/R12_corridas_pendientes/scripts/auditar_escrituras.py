"""R12: que generadores escriben en el arbol versionado sin poder redirigir la salida.

Por que existe. El issue #37 destrabo `sensibilidad_reparto.py`, y al terminar por primera
vez aparecio un defecto que mientras fallaba estaba invisible: escribe en
`research/ola4/M5_dos_ejes/resultados/`, que se versiona, y **no tenia como mandar la salida
a otro lado**. El censo de generadores de `R11` lo corre con `--muestras 50` para ver si
termina, asi que la primera corrida que no fallo reemplazo las cifras publicadas de esa linea
con una corrida de cincuenta sorteos (entrada 90 de `PREGUNTAS_ABIERTAS.md`). Esto busca el
mismo patron en el resto del repositorio **antes** de que otro generador se destrabe.

El defecto tiene tres partes y las tres hacen falta:

  1. el script **escribe** en un directorio que esta **versionado** (lo decide
     `git check-ignore`, no una lista nuestra);
  2. **no acepta** una bandera para redirigir la salida (`--salida`, `--resultados`,
     `--json`, `--destino`, `--out`);
  3. alguien lo **corre con parametros que cambian el resultado**: hoy eso es el censo de
     `R11`, y es la parte que convierte un defecto latente en una perdida de datos.

Las tres se informan por separado a proposito. Un script con 1 y 2 y sin 3 no perdio nada
todavia, pero es exactamente el estado en el que estaba `sensibilidad_reparto.py` **antes**
de entrar al censo, asi que es la lista de la que salen los proximos.

**La tercera parte no es «lo corre el censo», y la diferencia importa.** De los generadores
censados, cuatro escriben en el arbol versionado sin bandera —los tres de `M6` y el de `O3`—
y el censo los corre **con sus defaults**, asi que lo que escriben es exactamente lo que
publicarian: regeneran el mismo archivo y no pierden nada. El unico que tenia el defecto
completo era `sensibilidad_reparto.py`, porque el censo le pasaba `--muestras 50`, que **si**
mueve el resultado. Por eso la columna que decide es `censo_cambia_parametros` y no
`lo_corre_el_censo`: un censo que corre un generador con sus defaults es inofensivo aunque el
generador no sepa redirigir.

Lo que este auditor **no** puede ver, y conviene tenerlo escrito: detecta las constantes de
salida a nivel de modulo y las banderas declaradas con `add_argument`, las dos por texto. Un
script que arme la ruta de salida adentro de una funcion, o que la reciba por `sys.argv`
posicional, no aparece como «sin bandera» aunque lo este. Se mira el codigo, no se importa:
importar estos modulos pide los insumos que justamente no siempre estan.

Y un modulo que escribe **solo** cuando se le pasa la bandera —`ranking.py`, cuyo `--json`
viene en `None` y sin el no escribe nada— no declara constante de salida y por eso no aparece
en la tabla. No es un hueco: no tiene el defecto, porque sin bandera no escribe. Pero
tampoco cuenta como «revisado», asi que no hay que leer el total como el universo de modulos
que escriben.

    python research/ola6/R12_corridas_pendientes/scripts/auditar_escrituras.py
    python research/ola6/R12_corridas_pendientes/scripts/auditar_escrituras.py --todos
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
SALIDA = Path(__file__).resolve().parents[1] / "resultados"

#: Las constantes de salida a nivel de modulo. Se buscan por nombre y no por valor: lo que
#: define a una es que el modulo la use como destino, y los nombres que el repositorio usa
#: son estos cuatro.
CONSTANTE = re.compile(
    r"^(SALIDA|RESULTADOS|OUT|DESTINO)([A-Z_]*)\s*=\s*(.+)$", re.MULTILINE)
#: Las banderas con las que un script puede redirigir su salida.
BANDERA = re.compile(r"add_argument\(\s*[\"'](--[a-z-]*"
                     r"(?:salida|resultados|json|destino|out)[a-z-]*)[\"']")
#: Que el modulo escriba algo, para no listar los que solo leen.
ESCRIBE = re.compile(r"write_text\(|DictWriter\(|json\.dump\(|to_csv\(|\.open\(\s*[\"']w")
SALTAR = (".git", "__pycache__", ".venv", "node_modules")
SALTAR_RUTA = (".claude/worktrees",)


def ignorado(ruta: Path) -> bool:
    """Si `git` ignora esa ruta. Es la unica fuente de verdad sobre «esto se versiona».

    Se pregunta **dos veces**, con y sin barra final, y eso no es por prolijidad: un patron
    de `.gitignore` que termina en `/` —`pipeline/salida/`, `pipeline/datos/`— solo matchea
    directorios, y si el directorio **no existe en disco** `git check-ignore` sin la barra
    contesta que no esta ignorado. Medido: `pipeline/salida` da «no» y `pipeline/salida/` da
    «ignorado», con la misma linea 16 del `.gitignore` de por medio. Preguntar una sola vez
    daba cinco falsos positivos, los cinco del `pipeline/`, que es justo el directorio que
    `D61` declara ignorado.
    """
    for cand in (str(ruta), str(ruta) + "/"):
        if subprocess.run(["git", "check-ignore", "-q", cand], cwd=RAIZ,
                          capture_output=True).returncode == 0:
            return True
    return False


def resolver(expr: str, archivo: Path) -> Path | None:
    """La ruta de una constante de salida, sin importar el modulo.

    Resuelve las tres formas que el repositorio usa —`RAIZ / "..."`,
    `Path(__file__)...parents[n] / "..."` y `BLOQUE / "..."`— y devuelve `None` para
    cualquier otra, que es lo honesto: una expresion que no se sabe resolver no se adivina.
    """
    expr = expr.split("#")[0].strip()
    partes = re.findall(r"[\"']([^\"']+)[\"']", expr)
    if not partes:
        return None
    cola = "/".join(partes)
    m = re.search(r"parents\[(\d+)\]", expr)
    if expr.startswith("RAIZ"):
        return RAIZ / cola
    if m:
        return archivo.resolve().parents[int(m.group(1))] / cola
    if expr.startswith(("BLOQUE", "AQUI")):
        # las dos apuntan al directorio del bloque, que es el padre de `scripts/`
        return archivo.resolve().parents[1] / cola
    # `Path(__file__).parent / "..."`, sin `parents[n]`: el directorio del propio script.
    # Mandarlo a la raiz, que es lo que hacia antes, convertia los cinco `pipeline/*.py`
    # en falsos positivos: su `SALIDA` es `pipeline/salida`, que el `.gitignore` ignora,
    # y resuelta contra la raiz daba `salida`, que no existe y por lo tanto «se versiona».
    if re.match(r"Path\(__file__\)\.parent\b", expr):
        return archivo.resolve().parent / cola
    if expr.startswith("Path("):
        return RAIZ / cola
    return None


#: Banderas que **redirigen la salida** y por lo tanto no mueven el resultado.
DE_SALIDA = ("--json", "--salida", "--resultados", "--destino", "--out")


def generadores_del_censo() -> dict[str, list[str]]:
    """Ruta -> banderas con las que el censo de `R11` corre ese generador.

    Las banderas hacen falta para la tercera parte del defecto: lo que convierte una
    regeneracion en una perdida es que el censo pase un parametro que **mueve el
    resultado**, no el hecho de correrlo. Las de redireccion de salida no cuentan, y una
    ruta que el censo corre dos veces con comandos distintos acumula las de las dos.
    """
    ruta = RAIZ / "research/ola6/R11_compuerta_y_panel/scripts/censo_generadores.py"
    if not ruta.exists():
        return {}
    txt = ruta.read_text(encoding="utf-8")
    bloque = txt[txt.index("GENERADORES = ["):] if "GENERADORES = [" in txt else ""
    out: dict[str, list[str]] = {}
    for m in re.finditer(r"\"ruta\":\s*\"([^\"]+)\".*?\"comando\":\s*\[([^]]*)\]",
                         bloque, re.DOTALL):
        flags = [f for f in re.findall(r"\"(--[a-z-]+)\"", m.group(2))
                 if f not in DE_SALIDA]
        out.setdefault(m.group(1), []).extend(flags)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--todos", action="store_true",
                    help="lista tambien los que no tienen el defecto")
    a = ap.parse_args(argv)

    censo = generadores_del_censo()
    print("generadores que el censo de R11 corre: %d" % len(censo))
    for ruta, flags in sorted(censo.items()):
        print("  %-62s %s" % (ruta, ", ".join(sorted(set(flags)))
                              or "(con sus defaults)"))

    filas = []
    for py in sorted(RAIZ.rglob("*.py")):
        rel = py.relative_to(RAIZ).as_posix()
        if any(p in py.parts for p in SALTAR) or any(s in rel for s in SALTAR_RUTA):
            continue
        txt = py.read_text(encoding="utf-8", errors="replace")
        if not ESCRIBE.search(txt):
            continue
        destinos, sin_resolver = [], []
        for nombre, _suf, expr in CONSTANTE.findall(txt):
            d = resolver(expr, py)
            (destinos if d else sin_resolver).append(d or expr.strip()[:60])
        if not destinos and not sin_resolver:
            continue
        versionados = sorted({str(d.relative_to(RAIZ)) if d.is_relative_to(RAIZ) else str(d)
                              for d in destinos if not ignorado(d)})
        banderas = sorted(set(BANDERA.findall(txt)))
        fila = {
            "archivo": rel,
            "destinos_versionados": ";".join(versionados) or "-",
            "banderas": ",".join(banderas) or "-",
            "sin_resolver": ";".join(sin_resolver) or "-",
            "escribe_en_versionado": bool(versionados),
            "puede_redirigir": bool(banderas),
            "lo_corre_el_censo": rel in censo,
            "censo_cambia_parametros": bool(censo.get(rel)),
            "flags_del_censo": ",".join(sorted(set(censo.get(rel, [])))) or "-",
        }
        fila["defecto"] = fila["escribe_en_versionado"] and not fila["puede_redirigir"]
        fila["riesgo"] = (
            "perdida de datos" if fila["defecto"] and fila["censo_cambia_parametros"]
            else "regeneracion benigna" if fila["defecto"] and fila["lo_corre_el_censo"]
            else "latente" if fila["defecto"] else "-")
        filas.append(fila)

    con = [f for f in filas if f["defecto"]]
    urgentes = [f for f in con if f["censo_cambia_parametros"]]
    benignos = [f for f in con if f["lo_corre_el_censo"]
                and not f["censo_cambia_parametros"]]
    latentes = [f for f in con if not f["lo_corre_el_censo"]]
    print()
    print("modulos que escriben y declaran destino: %d" % len(filas))
    print("  escriben en el arbol versionado sin poder redirigir: %d" % len(con))
    print("    con riesgo de perdida (el censo les cambia parametros): %d" % len(urgentes))
    print("    regeneracion benigna (el censo los corre con defaults): %d" % len(benignos))
    print("    latentes (nadie los censa todavia): %d" % len(latentes))
    print()
    print("RIESGO DE PERDIDA DE DATOS (las tres partes del defecto):")
    for f in urgentes:
        print("  %-62s -> %s  [%s]" % (f["archivo"], f["destinos_versionados"],
                                       f["flags_del_censo"]))
    if not urgentes:
        print("  ninguno")
    print()
    print("REGENERACION BENIGNA (escriben en versionado sin bandera, pero el censo los")
    print("corre con sus defaults, asi que reproducen lo publicado):")
    for f in benignos:
        print("  %-62s -> %s" % (f["archivo"], f["destinos_versionados"]))
    print()
    print("DEFECTO LATENTE (escribe en versionado, sin bandera, no censado): %d"
          % len(latentes))
    for f in latentes:
        print("  %-62s -> %s" % (f["archivo"], f["destinos_versionados"]))
    if a.todos:
        print()
        print("SIN DEFECTO:")
        for f in filas:
            if not f["defecto"]:
                print("  %-62s banderas=%s" % (f["archivo"], f["banderas"]))

    SALIDA.mkdir(parents=True, exist_ok=True)
    cols = ["archivo", "escribe_en_versionado", "puede_redirigir", "lo_corre_el_censo",
            "censo_cambia_parametros", "flags_del_censo", "defecto", "riesgo",
            "destinos_versionados", "banderas", "sin_resolver"]
    with (SALIDA / "auditoria_escrituras.tsv").open("w", encoding="utf-8",
                                                    newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for f in filas:
            w.writerow(f)
    (SALIDA / "auditoria_escrituras.json").write_text(json.dumps(
        {"modulos_revisados": len(filas), "con_defecto": len(con),
         "con_riesgo_de_perdida": len(urgentes),
         "regeneracion_benigna": len(benignos), "latentes": len(latentes),
         "generadores_del_censo": {k: sorted(set(v)) for k, v in censo.items()},
         "filas": filas},
        indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print()
    print("escrito en %s" % SALIDA.relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
