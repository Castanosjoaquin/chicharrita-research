"""Toma candidatos de dsRNA YA DISENADOS y los prioriza. El camino que pide el track.

El resto del pipeline va del genoma a los candidatos. Pero la slide 11 plantea el desafio al
reves: el EPILAB trae sus candidatos preliminares y la pregunta es **cuales merecen validacion
y por que**. Esto cubre ese caso: entra un FASTA de secuencias de dsRNA de cualquier largo,
sale un ranking con la razon de cada puesto.

La diferencia con `sirna_enumerar.py` no es menor. Un dsRNA largo no es un siRNA: Dicer lo corta
en un pool heterogeneo, y lo que importa es **cuantos efectores buenos produce ese pool**, no si
contiene al mejor siRNA del mundo. Por eso el score de un candidato se agrega desde sus ventanas.

Y hay una asimetria deliberada entre eficacia y riesgo:
  - la eficacia se agrega por la **fraccion de ventanas buenas**: un pool con muchos efectores
    decentes sirve mas que uno con una joya y basura alrededor;
  - el riesgo se agrega por el **peor caso**: una sola ventana que pegue en un organismo no
    objetivo es un problema, por buenas que sean las otras veinte.

Uso:
    python3 puntuar_candidatos.py <candidatos.fasta> [--no-objetivo a.fna.gz b.fna.gz ...]
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sirna_enumerar import VENTANA, enumerar, puntuar  # noqa: E402
from sirna_offtarget import (K, K_ALERTA, escanear, revcomp,  # noqa: E402
                             semillas_alerta)

SALIDA = Path(__file__).parent / "salida"
DATOS = Path.home() / "yhat" / "data"
POR_DEFECTO = [DATOS / "maiz_rna.fna.gz", DATOS / "abeja_rna.fna.gz"]
UMBRAL_BUENA = 0.33   # fraccion del pool que cuenta como "buena": el tercio superior


def leer_fasta(ruta: Path) -> list[tuple[str, str]]:
    secuencias, nombre, trozos = [], None, []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if linea.startswith(">"):
            if nombre:
                secuencias.append((nombre, "".join(trozos).upper()))
            nombre, trozos = linea[1:].split()[0], []
        elif linea.strip():
            trozos.append(linea.strip())
    if nombre:
        secuencias.append((nombre, "".join(trozos).upper()))
    return secuencias


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    entrada = Path(sys.argv[1])
    if "--no-objetivo" in sys.argv:
        no_objetivo = [Path(a) for a in sys.argv[sys.argv.index("--no-objetivo") + 1:]]
    else:
        no_objetivo = [r for r in POR_DEFECTO if r.exists()]

    candidatos = leer_fasta(entrada)
    print(f"candidatos: {len(candidatos)} secuencias de {entrada.name}")

    # Clave: las ventanas de TODOS los candidatos se puntuan juntas. Si cada secuencia se
    # normaliza por separado, el mejor de una mala empata con el mejor de una buena y el
    # ranking entre candidatos pierde sentido. Comparar candidatos exige una escala comun.
    todas: list[dict] = []
    largos: dict[str, int] = {}
    for nombre, seq in candidatos:
        if len(seq) < VENTANA:
            print(f"  {nombre}: {len(seq)} nt, mas corta que una ventana, la salteo")
            continue
        filas = enumerar(seq)
        for f in filas:
            f["locus"] = nombre
        todas.extend(filas)
        largos[nombre] = len(seq)

    if not todas:
        sys.exit("ninguna secuencia utilizable")

    puntuar(todas)
    vivas_todas = [f for f in todas if not f["descarte"]]
    # "Buena" se define contra el pool completo: el tercio superior de lo que hay sobre la mesa.
    ordenadas = sorted(f["score_geom"] for f in vivas_todas)
    corte = ordenadas[int(len(ordenadas) * (1 - UMBRAL_BUENA))] if ordenadas else 0.0
    print(f"\ncorte de ventana buena (tercio superior del pool): score_geom >= {corte:.4f}")

    resumen: list[dict] = []
    for nombre in largos:
        filas = [f for f in todas if f["locus"] == nombre]
        vivas = [f for f in filas if not f["descarte"]]
        buenas = sum(1 for f in vivas if f["score_geom"] >= corte)
        resumen.append({
            "candidato": nombre,
            "largo": largos[nombre],
            "ventanas": len(filas),
            "descartadas_motivo": len(filas) - len(vivas),
            "buenas": buenas,
            "frac_buenas": round(buenas / len(vivas), 4) if vivas else 0.0,
            "score_medio": round(sum(f["score_geom"] for f in vivas) / len(vivas), 4) if vivas else 0.0,
        })
        print(f"  {nombre}: {largos[nombre]} nt, {len(filas)} ventanas, "
              f"{buenas} buenas ({buenas / max(len(vivas), 1) * 100:.0f} %)")

    # Off-target: una sola pasada por transcriptoma para todos los candidatos juntos
    indice: dict[str, list[str]] = {}
    for f in todas:
        clave = f"{f['locus']}|{f['pos']}|{f['sitio']}"
        indice.setdefault(f["sitio"], []).append(clave)
        indice.setdefault(revcomp(f["sitio"]), []).append(clave)
    semillas = semillas_alerta(indice)
    secuencias = {}
    for kmero, claves in indice.items():
        for c in claves:
            secuencias.setdefault(c, []).append(kmero)

    por_organismo: dict[str, dict[str, int]] = {}
    for ruta in no_objetivo:
        if not ruta.exists():
            print(f"  falta {ruta.name}, lo salteo")
            continue
        peor: dict[str, int] = {}
        escanear(ruta, indice, semillas, secuencias, peor)
        por_organismo[ruta.name.replace("_rna.fna.gz", "")] = peor
        print(f"  chequeado contra {ruta.name}")

    peor_por_candidato: dict[str, int] = {}
    especies_por_candidato: dict[str, set] = {}
    for f in todas:
        clave = f"{f['locus']}|{f['pos']}|{f['sitio']}"
        for org, peor in por_organismo.items():
            v = peor.get(clave, 0)
            if v > peor_por_candidato.get(f["locus"], 0):
                peor_por_candidato[f["locus"]] = v
            if v >= 17:
                especies_por_candidato.setdefault(f["locus"], set()).add(org)

    for r in resumen:
        r["off_target_peor"] = peor_por_candidato.get(r["candidato"], 0)
        r["off_target_especies"] = len(especies_por_candidato.get(r["candidato"], ()))
        r["veredicto"] = ("descartar" if r["off_target_peor"] >= K
                          else "revisar" if r["off_target_peor"] >= 17 or r["frac_buenas"] < 0.2
                          else "priorizar")

    orden = {"priorizar": 0, "revisar": 1, "descartar": 2}
    resumen.sort(key=lambda r: (orden[r["veredicto"]], -r["frac_buenas"]))

    print(f"\n{'candidato':<22}{'nt':>6}{'buenas':>8}{'%':>7}{'peor off':>10}{'sp':>4}  veredicto")
    for r in resumen:
        print(f"{r['candidato'][:21]:<22}{r['largo']:>6}{r['buenas']:>8}"
              f"{r['frac_buenas'] * 100:>6.0f}%{r['off_target_peor']:>10}"
              f"{r['off_target_especies']:>4}  {r['veredicto']}")

    destino = SALIDA / "candidatos_priorizados.csv"
    with destino.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(resumen[0].keys()))
        w.writeheader()
        w.writerows(resumen)
    print(f"\nranking en {destino}")
    print(f"umbral de ventana buena: tercio superior del pool (score_geom >= {corte:.4f}); "
          f"off-target: descartar a {K} nt, revisar a 17 nt")


if __name__ == "__main__":
    main()
