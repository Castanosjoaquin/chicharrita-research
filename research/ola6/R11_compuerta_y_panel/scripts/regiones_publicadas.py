"""R11, parte 2: toda coordenada de region que un JSON publicado trae, contra el inventario.

El issue #35 parte 2 dice que no hay garantia de que no queden regiones publicadas sin
tamizar, y que la forma de encontrarlas no es buscarlas a mano. Correr cada generador de
punta a punta es la forma fuerte y necesita `work/`. Esto es la otra mitad, que **no**
necesita `work/` y que ninguna de las dos busquedas anteriores hizo: en vez de mirar la
clave `regiones_recomendadas` -que es lo que `D70` y el issue #30 miraron, y por donde
`BicC_Dm` 2123-2422 se escapo-, recorre **el JSON entero**, recoge toda cadena con forma
de region y la cruza contra `estado_regiones.tsv`.

La diferencia con la compuerta es importante y conviene no confundirlas:

  * la compuerta frena una region **que se va a recomendar**. Es la garantia fuerte y es
    la que vale.
  * esto cuenta coordenadas **publicadas**, sin preguntar para que. Una region aparece en
    un JSON por cuatro motivos muy distintos, y el barrido los encontro a los cuatro:
    porque se la recomienda; porque es un puesto del orden de alternativas de la cascada;
    porque es un descriptivo del gen (`region_maxima` de un nulo, `mejor_region_21`); o
    porque es la region por defecto de un barrido de sensibilidad (`region_en_defecto` de
    `C9`). Los tres ultimos **no** pasan ni tienen por que pasar por la compuerta: no son
    recomendaciones. Lo que el conteo contesta es cuantas coordenadas hay publicadas,
    cuales estan tamizadas y de que bloque sale cada una, que es lo que hacia falta para
    poder decir «esto es todo» en vez de «no sabemos».

El gen de cada coordenada se toma de la clave ancestro mas cercana que sea un nombre de gen
conocido, o del hermano `gen` del mismo objeto. Una coordenada sin gen deducible se reporta
como tal y no se adivina, y una de un gen que no es del panel —el catalogo de `C5` publica la
mejor region de blancos de la literatura— se clasifica y **no** se cruza contra el
inventario: el inventario de `M6` no tiene por que tamizarla.

    python research/ola6/R11_compuerta_y_panel/scripts/regiones_publicadas.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
SALIDA = Path(__file__).resolve().parents[1] / "resultados"
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))

import alertas as AL  # noqa: E402

# Los JSON publicados que pueden traer coordenadas. Son los dos del ranking: `C7` es el
# vigente y `W7` es la primera version reproducida.
#
# Los archivos no se declaran a mano: se **barren**. Una lista escrita a mano es el mismo
# error que la entrada 24 describe —buscar donde uno se acuerda— un piso mas abajo, y la
# primera version de este script lo cometio: miraba tres archivos y decia «los tres
# publicados», cuando `research/` tiene mas JSON con coordenadas adentro.
RAIZ_BARRIDO = "research"
# Se saltean dos cosas, las dos declaradas. La salida de esta misma linea, que contiene las
# coordenadas que el barrido acaba de escribir y se contaria a si misma; y
# `research/R7_microgravedad/`, que es **otro proyecto** —estructura de mollicutes— cuyos
# volcados de RCSB y UniProt traen rangos de residuos con la misma forma `ini-fin` que una
# region, no son de ningun gen de este panel y varios no son JSON validos.
SALTAR_RUTA = ("research/ola6/R11_compuerta_y_panel/resultados",
               "research/R7_microgravedad/")

# Para los archivos de un solo gen, que no lo repiten en cada bloque: `region_vatpase_b.json`
# es todo del mismo gen y lo dice en su `consulta`, no en la clave de cada region. Se declara
# aca en vez de adivinarlo, y un archivo que no este en este mapa simplemente reporta sus
# coordenadas como «(sin gen deducible)», que es informacion y no un error.
# Verificado archivo por archivo antes de declararlo: los tres de abajo son de un solo gen
# y lo dicen en su encabezado (`consulta: work/W5/fasta/BicC_Dm_full.fasta` en `M7`) o en su
# alcance (las tres coordenadas de `N3` son las tres regiones de `BicC_Dm`).
GEN_SI_FALTA = {
    "research/ola6/O3_quimera_bicc_vatpase_b/resultados/region_vatpase_b.json": "VATPaseB_Dm",
    "research/ola4/M7_robustez_bicc/resultados/referencia_resumen.json": "BicC_Dm",
    "research/ola5/N3_marcos/resultados/marco2_por_fuente.json": "BicC_Dm",
}
INVENTARIO = "research/ola4/M6_alertas/resultados/estado_regiones.tsv"

# Una region es `ini-fin` con los dos enteros. El filtro de largo saca accesiones y
# fechas: ninguna region del proyecto tiene menos de 150 nt (el rango del investigador).
RX_REGION = re.compile(r"^(\d{1,5})-(\d{1,5})$")
LARGO_MINIMO = 150
GENES = ("MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm", "eth_Dm", "bursA_Dm",
         "VATPaseB_Dm", "V-ATPase B")


def gen_de(camino: list[str]) -> str:
    """El gen de la coordenada, de la clave ancestro mas cercana que sea un gen conocido.

    Hay dos formas en que un JSON de este repositorio dice de que gen es una region: que
    el gen sea la **clave** (`regiones_recomendadas.BicC_Dm`) o que sea un **hermano**
    (`candidatos[0]` tiene `gen` y `region` al mismo nivel). La segunda es la que hacia
    que cuatro de las coordenadas publicadas quedaran sin gen: se resuelve marcando el
    camino con `gen=<valor>` al bajar a un objeto que trae su propio `gen`.
    """
    for paso in reversed(camino):
        if paso.startswith("gen="):
            return paso[4:]
        if paso in GENES:
            return paso
        for g in GENES:
            if paso.startswith(g + "_") or paso.endswith("_" + g):
                return g
    return "(sin gen deducible)"


def clase_de(gen: str) -> str:
    """Si la coordenada es de un gen del panel, de otro gen, o de ninguno identificable.

    Hace falta porque el barrido encuentra coordenadas que no son regiones candidatas de
    nuestros genes: el catalogo de `C5` trae la mejor region de 200 nt de blancos de la
    literatura (troponina C, ATP sintasa beta), que el inventario de `M6` no tiene por que
    tamizar. Clasificarlas y no cruzarlas es la diferencia entre un agujero y un dato.
    """
    if gen in GENES:
        return "gen del panel"
    return "sin gen deducible" if gen.startswith("(sin gen") else "otro gen"


def bloque_de(camino: list[str]) -> str:
    """El bloque del JSON donde aparece: la primera clave que no sea `k`, un indice ni la
    marca `gen=` que `recoger()` agrega al bajar a un objeto con su propio gen."""
    for paso in camino:
        if (paso == "k" or paso.startswith("[") or paso.isdigit()
                or paso.startswith("gen=")):
            continue
        return paso
    return "(raiz)"


def recoger(nodo, camino: list[str], out: list[dict]) -> None:
    if isinstance(nodo, dict):
        propio = nodo.get("gen")
        aqui = camino + ["gen=%s" % propio] if isinstance(propio, str) else camino
        for k, v in nodo.items():
            recoger(v, aqui + [str(k)], out)
    elif isinstance(nodo, list):
        for i, v in enumerate(nodo):
            recoger(v, camino + ["[%d]" % i], out)
    elif isinstance(nodo, str):
        m = RX_REGION.match(nodo.strip())
        if not m:
            return
        ini, fin = int(m.group(1)), int(m.group(2))
        if fin - ini + 1 < LARGO_MINIMO:
            return
        out.append({"region": "%d-%d" % (ini, fin), "gen": gen_de(camino),
                    "camino": ".".join(p for p in camino if not p.startswith("gen=")),
                    "bloque": bloque_de(camino)})


def leer_inventario() -> set:
    """El inventario, leido con la funcion del port y no con una copia.

    `AL.leer_inventario()` levanta `FileNotFoundError` si el archivo no esta, y eso importa
    aca igual que en la compuerta: un inventario vacio haria que este censo reportara
    **todo** como sin tamizar, que es el mismo modo de fallar en silencio que `D72` cerro,
    del otro lado.
    """
    return AL.leer_inventario(RAIZ / INVENTARIO)


def main() -> int:
    inv = leer_inventario()
    filas = []
    candidatos = sorted((RAIZ / RAIZ_BARRIDO).rglob("*.json"))
    print("barriendo %d JSON bajo %s/" % (len(candidatos), RAIZ_BARRIDO))
    for ruta in candidatos:
        rel = ruta.relative_to(RAIZ).as_posix()
        if any(s in rel for s in SALTAR_RUTA):
            continue
        try:
            datos = json.loads(ruta.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print("NO SE PUDO LEER  %s: %s" % (rel, e))
            continue
        crudas: list[dict] = []
        recoger(datos, [], crudas)
        if not crudas:
            continue
        for c in crudas:
            c["archivo"] = rel
            if c["gen"] == "(sin gen deducible)" and rel in GEN_SI_FALTA:
                c["gen"] = GEN_SI_FALTA[rel]
            c["clase"] = clase_de(c["gen"])
            # El inventario es de las regiones de los genes del panel: cruzar contra el una
            # coordenada de otro gen daria «sin tamizar» para algo que no le corresponde
            # tamizar. Lo que no es del panel se reporta como tal y no como agujero.
            c["tamizada"] = ((c["gen"], c["region"]) in inv
                             if c["clase"] == "gen del panel" else None)
            filas.append(c)
        mias = [c for c in crudas if c["clase"] == "gen del panel"]
        pares = {(c["gen"], c["region"]) for c in mias}
        sin = sorted(p for p in pares if p not in inv)
        print("%s: %d coordenadas (%d de genes del panel), %d pares, %d sin tamizar"
              % (rel, len(crudas), len(mias), len(pares), len(sin)))
        for gen, reg in sin:
            donde = sorted({c["bloque"] for c in mias
                            if (c["gen"], c["region"]) == (gen, reg)})
            print("   SIN TAMIZAR  %s %s  (bloques: %s)" % (gen, reg, ", ".join(donde)))

    SALIDA.mkdir(parents=True, exist_ok=True)
    cols = ["archivo", "bloque", "gen", "clase", "region", "tamizada", "camino"]
    with (SALIDA / "regiones_publicadas.tsv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for f in sorted(filas, key=lambda x: (x["archivo"], x["gen"], x["region"],
                                              x["camino"])):
            w.writerow(f)
    delp = [f for f in filas if f["clase"] == "gen del panel"]
    sin_t = sorted({(f["gen"], f["region"]) for f in delp if not f["tamizada"]})
    resumen = {"json_barridos": len(candidatos),
               "coordenadas": len(filas),
               "coordenadas_de_genes_del_panel": len(delp),
               "pares_del_panel": len({(f["gen"], f["region"]) for f in delp}),
               "pares_del_panel_sin_tamizar": ["%s %s" % p for p in sin_t],
               "bloques_de_los_sin_tamizar": sorted({f["bloque"] for f in delp
                                                     if not f["tamizada"]}),
               "inventario": sorted("%s %s" % p for p in inv),
               "por_archivo": {}}
    for rel in sorted({f["archivo"] for f in filas}):
        mias = [f for f in filas if f["archivo"] == rel]
        dp = [f for f in mias if f["clase"] == "gen del panel"]
        pares = sorted({(f["gen"], f["region"]) for f in dp})
        resumen["por_archivo"][rel] = {
            "coordenadas": len(mias),
            "de_genes_del_panel": len(dp),
            "pares": ["%s %s" % p for p in pares],
            "sin_tamizar": ["%s %s" % p for p in pares if p not in inv]}
    (SALIDA / "regiones_publicadas.json").write_text(
        json.dumps(resumen, indent=1, ensure_ascii=False), encoding="utf-8")
    print()
    print("%d JSON barridos, %d coordenadas, %d de genes del panel, %d pares, %d sin tamizar"
          % (len(candidatos), len(filas), len(delp), resumen["pares_del_panel"], len(sin_t)))
    print("bloques de los que salen los sin tamizar: %s"
          % ", ".join(resumen["bloques_de_los_sin_tamizar"]))
    print("escrito en %s" % SALIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
