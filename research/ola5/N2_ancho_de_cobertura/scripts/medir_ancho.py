"""N2 - Que ancho de cobertura tiene la curva que le mostramos, 20 o 21.

El problema. `sifi_plus/perfil.solapamiento` construye la curva roja del «RNAi design plot»
asignando `size` posiciones a cada ventana, o sea 21. La carta del investigador del
2026-10-25 dice que la funcion historica asigna **20** `[R]`, y N1 midio que con 20 —y solo
con 20— se reproducen los cuatro conteos de la planilla `[M]`. Queda por saber si la curva
que verificamos «tramo por tramo» contra la pantalla del programa distingue las dos
convenciones, porque `sifi_plus/test_api.py:152` fija cantidad de tramos, maximo y altura en
cuatro posiciones, pero **no fija los bordes de los tramos**.

Lo que mide este script. Sobre `ATPaseD_Dm`, que es el gen con el que se verifico la curva,
con el motor del original (RNAplfold 2.1.5) y la tabla del original (`RNA_NN3`): los tramos,
el maximo y las cuatro alturas de referencia, con ancho 20 y con ancho 21. Si las dos
convenciones dan lo mismo en esas cuatro aserciones, la verificacion no discriminaba y hay
que agregarle los bordes; si dan distinto, la curva es una segunda via —independiente de los
conteos— para saber que ancho usa el original.

Las cuatro referencias vienen de la pantalla del programa, no de nosotros:
`research/ola2/W5_secuencias_epilab/sifi21_reproduccion.md` lineas 85-89 `[R]`.

Uso (desde la raiz del repositorio):

    SIFI_RNAPLFOLD='/c/Users/.../siFi2015/RNAplfold/RNAplfold.exe' \
        python research/ola5/N2_ancho_de_cobertura/scripts/medir_ancho.py

Sin esa variable el motor del original se declara no corrido y la medicion se hace con
ViennaRNA, que es otro conjunto de ventanas eficientes: sirve para saber si el test
discrimina, no para decidir el ancho del original.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
SALIDA = AQUI.parents[1] / "resultados"
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))
sys.path.insert(0, str(RAIZ / "research" / "ola5" / "N1_regla_de_conteo" / "scripts"))

from conteo_por_curva import tramos  # noqa: E402
from sifi_core import DEFAULTS, RNAPLFOLD_EXE, SifiEngine  # noqa: E402
from sifi_plus.perfil import solapamiento, todos  # noqa: E402

GEN = "ATPaseD_Dm"
FASTA = RAIZ / "work" / "sifi_check" / f"{GEN}_full.fasta"

#: Lo que se leyo de la pantalla del programa original para `ATPaseD_Dm` `[R]`.
#: «ocho tramos separados, en las mismas posiciones, con las mismas alturas (maximo 9 en
#: 150-156, luego 8 en 287-297), y la linea azul plana en 21.»
REFERENCIA = {"tramos": 8, "maximo": 9,
              "alturas": {150: 9, 156: 9, 287: 8, 297: 8},
              "meseta_9": [150, 156], "meseta_8": [287, 297], "azul_plana_en": 21}
ANCHOS = (20, 21)


def altura_en(ts, p):
    return next((alt for a, b, alt in ts if a <= p <= b), None)


def mesetas(curva, altura):
    """Los tramos donde la curva vale exactamente `altura`, 1-based."""
    out, ini = [], None
    for i, v in enumerate(curva, start=1):
        if v == altura and ini is None:
            ini = i
        elif v != altura and ini is not None:
            out.append([ini, i - 1])
            ini = None
    if ini is not None:
        out.append([ini, len(curva)])
    return out


def main() -> int:
    if not FASTA.exists():
        raise SystemExit("falta %s; `work/` no esta en git" % FASTA)

    exe = Path(os.environ.get("SIFI_RNAPLFOLD", RNAPLFOLD_EXE))
    backend = "exe" if exe.is_file() else "vienna"
    if backend == "vienna":
        print("AVISO: no se encontro RNAplfold.exe en %s. El motor del original queda "
              "declarado no corrido y la medicion usa ViennaRNA." % exe)

    seq = "".join(l.strip() for l in FASTA.read_text().splitlines()
                  if not l.startswith(">"))
    eng = SifiEngine(mode="fiel", temp_c=22.0, tabla_nn="NN3", **DEFAULTS)
    ventanas, resumen = eng.run(seq, backend=backend)
    efic = [w.pos for w in ventanas if w.is_efficient]
    largo = resumen["largo"]

    out = {"gen": GEN, "backend": backend, "ruta_exe": str(exe) if backend == "exe" else None,
           "tabla_nn": "NN3", "modo": "fiel", "largo": largo,
           "eficientes": len(efic), "referencia": REFERENCIA, "por_ancho": {}}

    for ancho in ANCHOS:
        curva = solapamiento(efic, largo, ancho)
        ts = tramos(curva)
        m9, m8 = mesetas(curva, 9), mesetas(curva, 8)
        out["por_ancho"][str(ancho)] = {
            "tramos": len(ts),
            "maximo": max(curva) if curva else 0,
            "alturas": {str(p): altura_en(ts, p) for p in REFERENCIA["alturas"]},
            "bordes": [[a, b, alt] for a, b, alt in ts],
            "meseta_9": m9[0] if len(m9) == 1 else m9,
            "meseta_8_en_287": next((t for t in m8 if t[0] == 287), None),
            "azul_plana_en": max(todos(len(ventanas), largo, ancho)),
        }

    for ancho, d in out["por_ancho"].items():
        # Las cuatro aserciones que el test ya tiene.
        d["pasa_el_test_actual"] = bool(
            d["tramos"] == REFERENCIA["tramos"]
            and d["maximo"] == REFERENCIA["maximo"]
            and all(d["alturas"][str(p)] == v
                    for p, v in REFERENCIA["alturas"].items()))
        # Las tres marcas de la pantalla que si fijan el ancho.
        d["coincide_con_la_pantalla"] = bool(
            d["meseta_9"] == REFERENCIA["meseta_9"]
            and d["meseta_8_en_287"] == REFERENCIA["meseta_8"]
            and d["azul_plana_en"] == REFERENCIA["azul_plana_en"])

    pasan = [a for a, d in out["por_ancho"].items() if d["pasa_el_test_actual"]]
    coinciden = [a for a, d in out["por_ancho"].items() if d["coincide_con_la_pantalla"]]
    out["el_test_discrimina"] = len(pasan) < 2
    out["anchos_que_pasan"] = pasan
    out["ancho_de_la_pantalla"] = coinciden[0] if len(coinciden) == 1 else None

    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "ancho_de_cobertura.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print("%s, motor %s, tabla NN3, modo fiel: %d ventanas eficientes"
          % (GEN, backend, len(efic)))
    for ancho, d in out["por_ancho"].items():
        print("  ancho %s: %d tramos, maximo %d | meseta de 9 en %s, de 8 en %s, "
              "azul plana en %d -> %s, %s"
              % (ancho, d["tramos"], d["maximo"], d["meseta_9"], d["meseta_8_en_287"],
                 d["azul_plana_en"],
                 "pasa el test actual" if d["pasa_el_test_actual"] else "no pasa el test",
                 "coincide con la pantalla" if d["coincide_con_la_pantalla"]
                 else "NO coincide con la pantalla"))
    print("\nel test actual %s las dos convenciones"
          % ("DISTINGUE" if out["el_test_discrimina"] else "NO distingue"))
    print("el ancho que reproduce la pantalla del original es %s"
          % (out["ancho_de_la_pantalla"] or "ninguno / ambiguo"))
    print("resultados en %s" % (SALIDA / "ancho_de_cobertura.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
