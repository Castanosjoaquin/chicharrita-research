"""Off-target contra los enemigos naturales que NO tienen genoma anotado.

Cuatro especies clave del control biologico de D. maidis tienen ensamblado en
GenBank pero ninguna anotacion, asi que no hay transcriptoma que bajar. La salida
no es rendirse: se busca el 21-mero contra el **genoma crudo**.

Eso sobre-marca, porque el genoma incluye intrones e intergenico y un tramo
identico ahi no silencia nada. Pero en un filtro de seguridad el error que se
puede permitir es marcar de mas, no de menos. Una especie chequeada contra su
genoma esta peor medida que una chequeada contra su transcriptoma, y muchisimo
mejor medida que una que no esta.

Uso:
    python3 no_objetivo_genomas.py <sirna_finales.csv> [--csv salida.csv]
"""

from __future__ import annotations

import csv
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from no_objetivo_correr import cargar, clave_ventana, escanear, indexar, riesgo  # noqa: E402
from sirna_offtarget import K, K_ALERTA  # noqa: E402

DATOS = Path.home() / "yhat" / "data"
FTP = "https://ftp.ncbi.nlm.nih.gov/genomes/all"

# (clave, accession, nombre de ensamblado, especie, por que esta)
GENOMAS = [
    ("anagrus", "GCA_022575985.1", "ASM2257598v1", "Anagrus nilaparvatae",
     "Mymaridae. El genero del parasitoide de huevos mas abundante de D. maidis en "
     "Argentina (A. virlai). No hay genoma de A. virlai; este es el congenere mas cercano "
     "disponible."),
    ("gonatopus", "GCA_018340375.1", "Gfla_zju_1.0", "Gonatopus flavifemur",
     "Dryinidae. El genero de G. bartletti, que es depredador Y parasitoide de ninfas y "
     "adultos de la chicharrita."),
    ("orius", "GCA_014119065.1", "ASM1411906v1", "Orius insidiosus",
     "Anthocoridae. Chinche depredadora del maiz americano, y ademas hemiptero: el riesgo "
     "por parentesco con el blanco es alto."),
]


def url_genoma(acc: str, nombre: str) -> str:
    base = acc[:3] + "/" + acc[4:7] + "/" + acc[7:10] + "/" + acc[10:13]
    carpeta = f"{acc}_{nombre}".replace(" ", "_")
    return f"{FTP}/{base}/{carpeta}/{carpeta}_genomic.fna.gz"


def bajar(url: str, destino: Path) -> bool:
    if destino.exists() and destino.stat().st_size > 0:
        return True
    tmp = destino.with_suffix(destino.suffix + ".parcial")
    try:
        with urllib.request.urlopen(url, timeout=900) as r, tmp.open("wb") as f:
            while True:
                trozo = r.read(1 << 20)
                if not trozo:
                    break
                f.write(trozo)
        tmp.rename(destino)
        return True
    except Exception as e:
        print(f"    error: {str(e)[:100]}", flush=True)
        tmp.unlink(missing_ok=True)
        return False


def main() -> int:
    filas = cargar(Path(sys.argv[1]))
    semillas, secuencias = indexar(filas)
    print(f"{len(filas)} ventanas · {len(semillas)} semillas de {K_ALERTA} nt", flush=True)

    peor: dict[str, int] = {}
    resultados = []
    for clave, acc, nombre, especie, razon in GENOMAS:
        destino = DATOS / f"{clave}_genomic.fna.gz"
        print(f"\n{especie} ({acc})", flush=True)
        if not bajar(url_genoma(acc, nombre), destino):
            continue
        print(f"  {destino.stat().st_size/1e6:.0f} MB, escaneando...", flush=True)
        r = escanear(destino, semillas, secuencias, peor)
        n_desc = sum(1 for v in r["peor_local"].values() if v >= K)
        n_alerta = sum(1 for v in r["peor_local"].values() if 17 <= v < K)
        print(f"  {r['transcriptos']:,} secuencias, {r['bases']/1e6:.0f} Mnt "
              f"| descartan {n_desc}  alerta {n_alerta}", flush=True)
        resultados.append((especie, razon, n_desc, n_alerta))

    for f in filas:
        clave = clave_ventana(f)
        f["off_target_genomas"] = peor.get(clave, 0)
        f["riesgo_genomas"] = riesgo(f["off_target_genomas"])

    print("\n=== ventanas por nivel de riesgo, solo contra estos genomas ===")
    for nivel in ("ok", "alerta", "descartar"):
        n = sum(1 for f in filas if f["riesgo_genomas"] == nivel)
        print(f"  {nivel:<12}{n:>6}")

    print("\n=== curva de umbral ===")
    total = len(filas)
    for umbral in range(K_ALERTA, K + 1):
        caen = sum(1 for f in filas if f["off_target_genomas"] >= umbral)
        print(f"{umbral:>5} nt  caen {caen:>5}  sobreviven {total-caen:>5}  "
              f"{(total-caen)/total*100:>6.1f}%")

    if "--csv" in sys.argv:
        destino = Path(sys.argv[sys.argv.index("--csv") + 1])
        campos = ["locus", "pos", "gen_drosophila", "sitio", "guia", "score_geom",
                  "off_target_genomas", "riesgo_genomas"]
        with destino.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=campos, extrasaction="ignore")
            w.writeheader()
            w.writerows(sorted(filas, key=lambda f: -float(f["score_geom"])))
        print(f"\ncsv escrito en {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
