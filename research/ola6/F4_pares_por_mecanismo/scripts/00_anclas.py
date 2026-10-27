#!/usr/bin/env python3
"""F4 — Las tres anclas del §6 del preregistro. Devuelve 1 si alguna falla.

Ninguna de las tres mide algo nuevo: las tres comparan lo que esta linea deriva contra
cifras y archivos que produjo **otro** codigo, y por eso valen. Si una no pasa, esta linea
para y lo dice, sin leer ningun numero nuevo.

1. **Contra el reparto publicado.** El respaldo de los cuatro mecanismos sobre las filas
   elegibles tiene que dar letalidad 16, reproduccion 13, transmision 4 y movilidad 1, con
   25 elegibles y 11 excluidas de 36. Son las cifras de la entrada 70 de
   `PREGUNTAS_ABIERTAS.md` y del `REPORT.md` de `F3` §6.
2. **Contra las dos salidas de `F3`.** El conjunto de elegibles tiene que ser exactamente el
   de las 25 filas de `orden_genes.tsv` y el de excluidos exactamente el de las 11 de
   `fuera_del_orden.tsv`. Prueba que la regla del §2 no es una lista escrita a mano que
   coincide por casualidad: se llega al mismo conjunto por otro camino y desde otro archivo.
3. **Contra `D67` y `O3`, que es la que conecta con `O4`.** El unico par elegible de
   `reproduccion + movilidad` en *Dalbulus maidis* tiene que ser `DM-01` con `DM-02`, y el
   enumerador de `O4` resuelto por la via nueva tiene que devolver **los mismos ejes** que
   la corrida publicada recibio escritos a mano, comparados contra la clave
   `ejes_declarados` de su propio JSON commiteado.

Uso (desde la raiz del repositorio):
    python research/ola6/F4_pares_por_mecanismo/scripts/00_anclas.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(RAIZ / "research/ola6/O4_enumerador_quimeras/scripts"))
import pares_por_mecanismo as PM   # noqa: E402

F3 = RAIZ / "research/ola6/F3_recomendador_genes/resultados"
O4_JSON = (RAIZ / "research/ola6/O4_enumerador_quimeras/resultados"
           / "quimeras_enumeradas_o4_cobertura_fenotipica_corregido_vienna.json")

#: El reparto de la entrada 70 y del REPORT de F3 §6. Lo midio `01_eje_fenotipo.py`.
REPARTO = {"letalidad": 16, "reproduccion": 13, "transmision": 4, "movilidad": 1}
ELEGIBLES, EXCLUIDAS, TOTAL = 25, 11, 36

FALLAS: list[str] = []


def check(cond, msg):
    print("  %s %s" % ("ok  " if cond else "FALLA", msg))
    if not cond:
        FALLAS.append(msg)


def leer_tsv(p: Path) -> list[dict]:
    with p.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main() -> int:
    filas = PM.leer_tabla()
    elegibles, excluidos = PM.clasificar(filas)
    PM.verificar(filas, elegibles, excluidos)
    contra = PM.leer_contraevidencia(elegibles, filas)
    sop = PM.soporte(elegibles)

    print("ancla 1 — contra el reparto publicado (entrada 70, REPORT de F3 §6)")
    check(len(filas) == TOTAL, "el catalogo tiene %d filas (son %d)" % (TOTAL, len(filas)))
    check(len(elegibles) == ELEGIBLES,
          "%d filas elegibles (son %d)" % (ELEGIBLES, len(elegibles)))
    check(len(excluidos) == EXCLUIDAS,
          "%d filas excluidas por su etiqueta (son %d)" % (EXCLUIDAS, len(excluidos)))
    for m, n in REPARTO.items():
        check(sop[m]["n"] == n, "%s sostenido por %d candidatos (son %d)"
              % (m, n, sop[m]["n"]))

    print("\nancla 2 — contra las dos salidas de F3, que las produjo otro script")
    orden = {r["id"] for r in leer_tsv(F3 / "orden_genes.tsv")}
    fuera = {r["id"] for r in leer_tsv(F3 / "fuera_del_orden.tsv")}
    check(set(elegibles) == orden,
          "los elegibles son exactamente los de orden_genes.tsv (sobran %s, faltan %s)"
          % (sorted(set(elegibles) - orden), sorted(orden - set(elegibles))))
    check(set(excluidos) == fuera,
          "los excluidos son exactamente los de fuera_del_orden.tsv (sobran %s, faltan %s)"
          % (sorted(set(excluidos) - fuera), sorted(fuera - set(excluidos))))
    check(not (orden & fuera), "ningun candidato esta en los dos archivos de F3")

    print("\nancla 3 — contra D67 y O3: el unico par que ya estaba armado a mano")
    propios = {i: f for i, f in elegibles.items() if f["especie"] == PM.ESPECIE_BLANCO}
    sop_propios = PM.soporte(propios)
    ps = PM.pares(propios, "reproduccion", "movilidad", sop_propios, contra, False)
    check(len(ps) == 1, "un solo par elegible de reproduccion+movilidad en %s (son %d)"
          % (PM.ESPECIE_BLANCO, len(ps)))
    if ps:
        p = ps[0]
        check((p["id_a"], p["rol_a"], p["id_b"], p["rol_b"])
              == ("DM-01", "reproduccion", "DM-02", "movilidad"),
              "el par es DM-01 cubriendo reproduccion con DM-02 cubriendo movilidad "
              "(es %s/%s + %s/%s)" % (p["id_a"], p["rol_a"], p["id_b"], p["rol_b"]))
        check(p["rol_b_descansa_en_un_solo_candidato"] == "si",
              "la salida dice que movilidad descansa en un solo candidato")
        check("DM-03" in p["contraevidencia_del_rol_b"],
              "y lleva al lado la contraevidencia de DM-03 (entrada 70)")

    # La mitad que conecta con O4: el eje resuelto desde la tabla tiene que ser el mismo que
    # la corrida publicada recibio escrito en la linea de comandos.
    import enumerar_quimeras as EQ   # noqa: E402  el enumerador, con el puente de F4
    ejes, decl = EQ.ejes_por_mecanismo(
        "reproduccion,movilidad",
        ["DM-01=BicC_Dm", "DM-02=VATPaseB_Dm"],
        ["BicC_Dm", "VATPaseB_Dm"], False)
    publicados = json.loads(O4_JSON.read_text(encoding="utf-8"))["ejes_declarados"]
    check(ejes == publicados,
          "el eje resuelto desde la tabla es identico al publicado por O4 "
          "(resuelto %s; publicado %s)" % (ejes, publicados))
    check(decl["mecanismos_de_los_dos_se_solapan"] is False
          and decl["ampliacion_de_d67_sin_adr"] is False,
          "y la declaracion dice que no hay solape y que no amplia D67")

    print()
    if FALLAS:
        print("FALLAS: %d. Esta linea para y no lee ningun numero nuevo." % len(FALLAS))
        return 1
    print("las tres anclas pasan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
