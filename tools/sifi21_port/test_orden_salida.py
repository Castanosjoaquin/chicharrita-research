"""El orden de D76 verificado a traves de los escritores reales, no en aislamiento.

`test_ranking.py` prueba `por_referencia_ordenado()` sola, que es la propiedad; esto prueba
la cadena, que es lo que el issue #34 pide: que el JSON que sale de `ranking_v2.ficha()` y
de `ranking_v2.gen_entero()` tenga el orden del panel **cualquiera sea el orden de las
columnas del TSV de off-targets**, que es de donde el orden se heredaba.

No hace falta ViennaRNA ni `work/sifi_v2/`: el fixture son cuatro TSV minusculos escritos
aca, con las mismas columnas que producen `run_sifi.py` y `offtarget_21nt.py`. Lo que el
fixture no puede dar son las cifras publicadas —para eso hay que correr el generador de
verdad, y queda pendiente en `00_meta/PREGUNTAS_ABIERTAS.md`—; lo que si da es el orden.

    python test_orden_salida.py
"""

from __future__ import annotations

import csv
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ranking as R
import ranking_v2 as V

FALLAS = []

GEN = "MP_MRFV"
N = 40                      # ventanas del gen sintetico
REGION = (5, 24)
PANEL = ["maiz", "A_mellifera", "H_vitripennis", "F_candida", "humano", "D_maidis"]

# Las referencias del panel por su nombre largo, que es la clave de las columnas del TSV.
LARGAS = {
    "maiz": "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna",
    "A_mellifera": "GCF_003254395.2_Amel_HAv3.1_rna",
    "H_vitripennis": "GCF_021130785.1_UT_GWSS_2.1_rna",
    "F_candida": "GCF_002217175.1_ASM221717v1_rna",
    "humano": V.HUMANO,
}


def check(cond, msg):
    if cond:
        print("  ok   %s" % msg)
    else:
        print("  FALLA %s" % msg)
        FALLAS.append(msg)


def _escribir_perfil(dirs: Path):
    """El TSV de perfil que lee `ranking.leer_perfil`: una fila por ventana."""
    dirs.mkdir(parents=True, exist_ok=True)
    ruta = dirs / ("%s_full_corregido_vienna.tsv" % GEN)
    with ruta.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["pos", "is_efficient"])
        for p in range(1, N + 1):
            w.writerow([p, "True" if p % 3 == 0 else "False"])


def _escribir_offtarget(ruta: Path, refs: list[str]):
    """La matriz de off-targets, con las columnas `<referencia>|<criterio>` en el orden en
    que vienen `refs`. Ese orden es justamente la variable del experimento."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    cols = ["%s|%s" % (r, c) for r in refs for c in R.CRITERIOS]
    with ruta.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["consulta", "pos"] + cols)
        for p in range(1, N + 1):
            # Un acierto cada dos posiciones, igual para todas las referencias: lo que se
            # mira es el orden de las claves, no la cifra.
            marca = 1 if p % 2 == 0 else 0
            w.writerow(["%s_full" % GEN, p] + [marca] * len(cols))


def _armar(raiz: Path, orden_refs: list[str]):
    """Un `work/sifi_v2/` sintetico con las referencias en el orden pedido."""
    _escribir_perfil(raiz / "salida_k21")
    _escribir_offtarget(raiz / "offtarget_k21" / "offtarget_por_sirna.tsv", orden_refs)
    _escribir_offtarget(raiz / "offtarget_dm_k21" / "offtarget_por_sirna.tsv", [R.DMAIDIS])


def _salida(raiz: Path) -> dict:
    """Lo que los escritores de verdad producen desde ese directorio."""
    genes = V.cargar(raiz, 21, [GEN])
    cand = {"gen": GEN, "region": REGION, "estrategia": "virus"}
    wr, wc = R.pesos_base()
    return {"ficha": V.ficha(genes[GEN], cand, wr, wc),
            "gen_entero": V.gen_entero(genes[GEN], R.excluidas_de(cand, "off"))}


def test_el_orden_del_tsv_no_llega_a_la_salida():
    """Dos corridas con las columnas del TSV en ordenes distintos dan el mismo JSON."""
    print("el orden de las columnas del TSV no se filtra a la salida")
    V.con_panel(sin_humano=False)
    largas = [LARGAS[c] for c in PANEL if c != "D_maidis"]
    # Orden de accesion ascendente, que es el que tenia el archivo publicado en 38ad686,
    # contra el del panel. Si el orden se heredara, estas dos salidas no coincidirian.
    ordenes = {"accesion": sorted(largas), "panel": largas,
               "invertido": list(reversed(largas))}
    salidas = {}
    for nombre, refs in ordenes.items():
        raiz = Path(tempfile.mkdtemp(prefix="d76_"))
        try:
            _armar(raiz, refs)
            salidas[nombre] = _salida(raiz)
        finally:
            shutil.rmtree(raiz, ignore_errors=True)

    for nombre, s in salidas.items():
        for bloque, clave in (("ficha", "riesgo_por_referencia"),
                              ("gen_entero", "por_referencia")):
            check(list(s[bloque][clave]) == PANEL,
                  "%s, %s: %s" % (nombre, bloque, " ".join(s[bloque][clave])))

    volcados = {n: json.dumps(s, indent=1, ensure_ascii=False, default=int)
                for n, s in salidas.items()}
    ref = volcados["panel"]
    for nombre, v in volcados.items():
        check(v == ref, "la salida con las columnas en orden %r es identica a la del panel"
                        % nombre)


def test_dos_corridas_seguidas_dan_lo_mismo():
    """La parte reproducible del criterio del issue que si se puede correr aca: el mismo
    insumo dos veces da el mismo volcado byte a byte. La corrida con los insumos de verdad
    queda pendiente, porque necesita ViennaRNA."""
    print("dos corridas seguidas sobre el mismo insumo dan el mismo volcado")
    V.con_panel(sin_humano=False)
    raiz = Path(tempfile.mkdtemp(prefix="d76_"))
    try:
        _armar(raiz, [LARGAS[c] for c in PANEL if c != "D_maidis"])
        a = json.dumps(_salida(raiz), indent=1, ensure_ascii=False, default=int)
        b = json.dumps(_salida(raiz), indent=1, ensure_ascii=False, default=int)
    finally:
        shutil.rmtree(raiz, ignore_errors=True)
    check(a.encode("utf-8") == b.encode("utf-8"), "identico byte a byte (%d bytes)"
          % len(a.encode("utf-8")))


def test_una_referencia_fuera_del_panel_no_llega_a_la_guarda():
    """El limite de lo que D76 cierra, medido y no supuesto.

    `por_referencia_ordenado()` levanta `KeyError` ante un nombre corto que no sea del
    panel, y eso esta probado en `test_ranking.py`. Lo que esta prueba fija es que **el
    escritor nunca le pasa uno**: `ranking.corto()` dobla toda referencia desconocida a
    `D_maidis`, asi que una columna de una referencia que el panel no tiene entra como el
    vector y **choca con el**, silenciosamente, antes de que la guarda la vea. Gana la
    ultima que escribe, o sea que *cual* gana depende del orden de las columnas del TSV:
    es la misma clase de problema que D76 cierra para el orden de las claves, en un lugar
    donde sigue abierto.

    Queda anotado en `00_meta/PREGUNTAS_ABIERTAS.md`. No lo introdujo D76 y arreglarlo es
    cambiar `corto()`, que es de otra linea.
    """
    print("una referencia fuera del panel se dobla a D_maidis y no llega a la guarda")
    V.con_panel(sin_humano=False)
    raiz = Path(tempfile.mkdtemp(prefix="d76_"))
    try:
        intrusa = "GCF_000000000.0_M_quadrilineatus_rna"
        _armar(raiz, [LARGAS["maiz"], intrusa])
        s = _salida(raiz)
        claves = list(s["ficha"]["riesgo_por_referencia"])
        check(claves == ["maiz", "D_maidis"],
              "la intrusa no aparece con su nombre: %s" % " ".join(claves))
        check("M_quadrilineatus" not in json.dumps(s),
              "y no queda rastro de ella en la salida")
    finally:
        shutil.rmtree(raiz, ignore_errors=True)


def main():
    for t in (test_el_orden_del_tsv_no_llega_a_la_salida,
              test_dos_corridas_seguidas_dan_lo_mismo,
              test_una_referencia_fuera_del_panel_no_llega_a_la_guarda):
        t()
    print()
    if FALLAS:
        print("FALLARON %d verificaciones" % len(FALLAS))
        return 1
    print("todas las verificaciones pasaron")
    return 0


if __name__ == "__main__":
    sys.exit(main())
