"""Corre el off-target de los siRNA finales contra la lista AMPLIADA de no objetivo.

Reusa el escaneo de `sirna_offtarget.py` (mismo criterio: tramo identico mas largo
entre el siRNA y cada transcriptoma, ambas hebras) pero corrige un problema que
impide usarlo tal cual sobre un CSV de varios genes.

EL PROBLEMA
-----------
`sirna_offtarget.py` y `cadena_completa.py` indexan los resultados por la columna
`pos`, que es la posicion de la ventana DENTRO DE SU PROPIO CDS. Con un solo gen
eso es unico. Con varios genes no: en `sirna_finales.csv` hay 375 ventanas de 16
genes y **59 valores de `pos` aparecen en mas de un gen**. Dos siRNA distintos
caen en el mismo casillero y se pisan: el `off_target_max` que termina en la tabla
es el peor de los dos, atribuido a los dos.

Aca la clave es `locus|pos|sitio`, que lleva la secuencia adentro.

Uso:
    python3 no_objetivo_correr.py <sirna_finales.csv> <catalogo.csv> [--csv salida.csv]
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sirna_offtarget import K, K_ALERTA, recorrer, revcomp  # noqa: E402

DATOS = Path.home() / "yhat" / "data"
# Lo que ya se chequeaba antes de esta tanda. Sirve para medir el delta.
PREVIAS = {"maiz", "abeja"}


def clave_ventana(f: dict) -> str:
    """locus|pos|sitio: la clave de una ventana en todo el pipeline.

    `pos` sola colisiona entre genes (fue un bug real, ya arreglado aguas arriba).
    La secuencia va adentro porque si dos corridas enumeran el mismo locus sobre
    un CDS distinto, `locus|pos` podria apuntar a secuencias distintas y el cruce
    entre archivos saldria mal en silencio.
    """
    return f"{f['locus']}|{f['pos']}|{f['sitio']}"


def cargar(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8") as fh:
        return [f for f in csv.DictReader(fh) if not f.get("descarte")]


def indexar(filas: list[dict]) -> tuple[dict[str, set[str]], dict[str, list[str]]]:
    """Semillas de K_ALERTA nt -> claves, y clave -> sus dos hebras."""
    secuencias: dict[str, list[str]] = {}
    semillas: dict[str, set[str]] = defaultdict(set)
    for f in filas:
        clave = clave_ventana(f)
        sitio = f["sitio"].upper()
        secuencias[clave] = [sitio, revcomp(sitio)]
        for variante in secuencias[clave]:
            for i in range(len(variante) - K_ALERTA + 1):
                semillas[variante[i:i + K_ALERTA]].add(clave)
    return semillas, secuencias


def escanear(ruta: Path, semillas: dict[str, set[str]], secuencias: dict[str, list[str]],
             peor: dict[str, int]) -> dict:
    """Una pasada por un transcriptoma. Actualiza `peor` con el tramo identico mas largo."""
    golpes: dict[str, set[str]] = defaultdict(set)
    local: dict[str, int] = {}
    transcriptos = bases = 0

    for nombre, seq in recorrer(ruta):
        transcriptos += 1
        bases += len(seq)
        tope = len(seq) - K_ALERTA + 1
        for i in range(tope):
            semilla = seq[i:i + K_ALERTA]
            claves = semillas.get(semilla)
            if not claves:
                continue
            for clave in claves:
                mejor = K_ALERTA
                for variante in secuencias[clave]:
                    j = variante.find(semilla)
                    if j < 0:
                        continue
                    largo = K_ALERTA
                    while (j + largo < len(variante) and i + largo < len(seq)
                           and variante[j + largo] == seq[i + largo]):
                        largo += 1
                    mejor = max(mejor, largo)
                if mejor > local.get(clave, 0):
                    local[clave] = mejor
                if mejor > peor.get(clave, 0):
                    peor[clave] = mejor
                if mejor >= K:
                    golpes[clave].add(nombre)

    return {"archivo": ruta.name, "transcriptos": transcriptos, "bases": bases,
            "exactos": golpes, "peor_local": local}


def riesgo(valor: int) -> str:
    """Mismo criterio que cadena_completa.py, para que los numeros sean comparables."""
    return "descartar" if valor >= K else "alerta" if valor >= 17 else "ok"


def main() -> int:
    finales = Path(sys.argv[1])
    catalogo = Path(sys.argv[2])

    filas = cargar(finales)
    especies = [f for f in csv.DictReader(catalogo.open(encoding="utf-8"))
                if f["estado"] == "ok"]
    if "--solo" in sys.argv:
        quiero = set(sys.argv[sys.argv.index("--solo") + 1].split(","))
        especies = [e for e in especies if e["clave"] in quiero]

    semillas, secuencias = indexar(filas)
    print(f"{len(filas)} ventanas de {len(set(f['locus'] for f in filas))} genes "
          f"· {len(semillas)} semillas de {K_ALERTA} nt")
    print(f"catalogo: {len(especies)} especies con RefSeq\n")

    peor: dict[str, int] = {}
    peor_previo: dict[str, int] = {}
    por_especie: dict[str, dict] = {}

    # --base permite sumar una tanda nueva de especies a una corrida anterior sin
    # volver a escanear todo: se arranca del peor valor ya encontrado.
    if "--base" in sys.argv:
        previa = Path(sys.argv[sys.argv.index("--base") + 1])
        with previa.open(encoding="utf-8") as fh:
            for f in csv.DictReader(fh):
                clave = clave_ventana(f)
                peor[clave] = max(peor.get(clave, 0), int(f.get("off_target_ampliado") or 0))
                peor_previo[clave] = max(peor_previo.get(clave, 0),
                                         int(f.get("off_target_previo") or 0))
        print(f"arranco desde {previa.name}: {len(peor)} ventanas con valor previo")
        print()

    for esp in especies:
        ruta = DATOS / f"{esp['clave']}_rna.fna.gz"
        if not ruta.exists():
            print(f"  {esp['especie']:<32}FALTA {ruta.name}, lo salteo")
            continue
        r = escanear(ruta, semillas, secuencias, peor)
        por_especie[esp["clave"]] = {**r, "especie": esp["especie"], "grupo": esp["grupo"]}
        if esp["clave"] in PREVIAS:
            for clave, valor in r["peor_local"].items():
                if valor > peor_previo.get(clave, 0):
                    peor_previo[clave] = valor
        n_desc = sum(1 for v in r["peor_local"].values() if v >= K)
        n_alerta = sum(1 for v in r["peor_local"].values() if 17 <= v < K)
        print(f"  {esp['especie']:<32}{esp['grupo']:<22}"
              f"{r['transcriptos']:>8,} tx {r['bases']/1e6:>9.1f} Mnt "
              f"| descartan {n_desc:>3}  alerta {n_alerta:>3}")

    # -------------------------------------------------------------------
    for f in filas:
        clave = clave_ventana(f)
        f["off_target_ampliado"] = peor.get(clave, 0)
        f["riesgo_ampliado"] = riesgo(f["off_target_ampliado"])
        f["off_target_previo"] = peor_previo.get(clave, 0)
        f["riesgo_previo"] = riesgo(f["off_target_previo"])

    print()
    print("=== ventanas por nivel de riesgo ===")
    print(f"{'':<14}{'solo maiz+abeja':>18}{'catalogo ampliado':>20}")
    for nivel in ("ok", "alerta", "descartar"):
        a = sum(1 for f in filas if f["riesgo_previo"] == nivel)
        b = sum(1 for f in filas if f["riesgo_ampliado"] == nivel)
        print(f"  {nivel:<12}{a:>18}{b:>20}")

    # -------------------------------------------------------------------
    def doce(campo_riesgo: str, campo_off: str) -> list[dict]:
        limpias = [f for f in filas if f[campo_riesgo] == "ok"]
        vistos: set[str] = set()
        salida = []
        for f in sorted(limpias, key=lambda f: -float(f["score_geom"])):
            if f["locus"] in vistos:
                continue
            vistos.add(f["locus"])
            salida.append(f)
            if len(salida) >= 12:
                break
        return salida

    antes = doce("riesgo_previo", "off_target_previo")
    despues = doce("riesgo_ampliado", "off_target_ampliado")
    claves_antes = {clave_ventana(f) for f in antes}
    claves_despues = {clave_ventana(f) for f in despues}

    print()
    print("=== los 12 finales, antes y despues ===")
    print(f"{'locus':<9}{'gen':<11}{'pos':>6}{'off previo':>12}{'off ampliado':>14}"
          f"{'veredicto':>26}")
    for f in antes:
        clave = clave_ventana(f)
        if clave in claves_despues:
            v = "sobrevive"
        elif f["riesgo_ampliado"] != "ok":
            v = f"CAE ({f['riesgo_ampliado']})"
        else:
            v = "lo desplaza otra ventana"
        gen = (f["gen_drosophila"] or f["tribolium"] or "")[:10]
        print(f"{f['locus']:<9}{gen:<11}{f['pos']:>6}{f['off_target_previo']:>12}"
              f"{f['off_target_ampliado']:>14}{v:>26}")

    sobreviven = len(claves_antes & claves_despues)
    print()
    print(f"de los 12 de antes, siguen estando: {sobreviven}")
    genes_antes = {f["locus"] for f in antes}
    genes_despues = {f["locus"] for f in despues}
    print(f"genes que pierden TODA ventana limpia: "
          f"{sorted(genes_antes - genes_despues) or 'ninguno'}")

    print()
    print("=== quien aporta el descarte ===")
    print("(para cada especie, cuantas ventanas descarta que NINGUNA otra descartaba)")
    descartan: dict[str, set[str]] = {}
    for clave_esp, r in por_especie.items():
        descartan[clave_esp] = {k for k, v in r["peor_local"].items() if v >= K}
    for clave_esp, conjunto in sorted(descartan.items(), key=lambda x: -len(x[1])):
        otros = set().union(*[v for k, v in descartan.items() if k != clave_esp]) \
            if len(descartan) > 1 else set()
        solos = conjunto - otros
        if conjunto:
            print(f"  {por_especie[clave_esp]['especie']:<32}"
                  f"descarta {len(conjunto):>4}  ·  solo esta especie: {len(solos):>4}")

    print()
    print("=== curva de umbral con el catalogo ampliado ===")
    print(f"{'umbral':>8}{'caen':>10}{'sobreviven':>13}{'%':>8}")
    total = len(filas)
    for umbral in range(K_ALERTA, K + 1):
        caen = sum(1 for f in filas if f["off_target_ampliado"] >= umbral)
        print(f"{umbral:>5} nt{caen:>10}{total - caen:>13}{(total-caen)/total*100:>7.1f}%")

    if "--csv" in sys.argv:
        destino = Path(sys.argv[sys.argv.index("--csv") + 1])
        with destino.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
            w.writeheader()
            w.writerows(sorted(filas, key=lambda f: -float(f["score_geom"])))
        print(f"\ncsv escrito en {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
