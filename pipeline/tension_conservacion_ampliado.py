"""La tension conservacion-riesgo, medida contra tres listas de no objetivo distintas.

`tension_conservacion.py` midio con maiz y abeja y no encontro relacion
(Spearman +0,086). Pero maiz y abeja estan lejisimos de un cicadelido: el maiz no
es ni un animal. Si la hipotesis es "lo que hace a un gen buen blanco lo hace
peligroso", el lugar donde tiene que aparecer es contra **parientes del insecto**,
no contra el cultivo.

Entonces se mide lo mismo tres veces, cambiando solo quien es el no objetivo:

  1. maiz + abeja          (lo que habia: el cultivo y el polinizador centinela)
  2. el catalogo completo  (25 especies)
  3. solo los parientes    (hemipteros y artropodos cercanos)

Si la correlacion aparece en (3) y no en (1), el resultado no es "no hay tension"
sino **"la tension existe pero no esta donde la estabamos buscando"**.

Uso:
    python3 tension_conservacion_ampliado.py
"""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

SALIDA = Path(__file__).parent / "salida"
UMBRAL_RIESGO = 17  # mismo umbral que tension_conservacion.py, para poder comparar

# Las tres listas. La clave es la columna del CSV de donde sale el peor valor.
JUEGOS = [
    ("maiz + abeja", "sirna_no_objetivo_ampliado.csv", "off_target_previo"),
    ("catalogo completo (25 sp)", "sirna_no_objetivo_ampliado.csv", "off_target_ampliado"),
    ("solo parientes del insecto", "sirna_cercanos.csv", "off_target_ampliado"),
]


def numero(v, por_defecto=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return por_defecto


def spearman(xs, ys):
    def rangos(v):
        orden = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(orden):
            j = i
            while j + 1 < len(orden) and v[orden[j + 1]] == v[orden[i]]:
                j += 1
            for k in range(i, j + 1):
                r[orden[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = rangos(xs), rangos(ys)
    n = len(xs)
    if n < 3:
        return float("nan")
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else float("nan")


def cargar_conservacion() -> dict[str, float]:
    """Identidad del mejor alineamiento del locus, igual que tension_conservacion.py."""
    conservacion: dict[str, float] = {}
    with (SALIDA / "tabla_unificada.csv").open(encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            ident = [numero(fila.get(f"{p}_identidad")) for p in ("tcas", "dmel", "nlug")]
            ident = [v for v in ident if v > 0]
            if ident:
                conservacion[fila["locus"]] = max(ident)
    return conservacion


def medir(ruta: Path, columna: str, conservacion: dict[str, float]):
    """Un punto por gen: (conservacion, fraccion de ventanas riesgosas, peor coincidencia)."""
    ventanas: dict[str, list[int]] = defaultdict(list)
    with ruta.open(encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            ventanas[fila["locus"]].append(int(numero(fila.get(columna))))

    datos = []
    for locus, offs in ventanas.items():
        if locus not in conservacion or len(offs) < 5:
            continue
        riesgosas = sum(1 for o in offs if o >= UMBRAL_RIESGO) / len(offs)
        datos.append((conservacion[locus], riesgosas, max(offs), locus))
    return datos


TRAMOS = [(0.0, 0.5), (0.5, 0.7), (0.7, 0.85), (0.85, 1.01)]


def informe(nombre: str, datos: list) -> dict:
    xs = [d[0] for d in datos]
    rho = spearman(xs, [d[1] for d in datos])
    rho_max = spearman(xs, [d[2] for d in datos])

    print(f"\n{'=' * 72}")
    print(f"{nombre}  ({len(datos)} genes)")
    print("=" * 72)
    print(f"  Spearman(conservacion, fraccion de ventanas riesgosas) = {rho:+.3f}")
    print(f"  Spearman(conservacion, peor coincidencia del gen)      = {rho_max:+.3f}")
    print(f"\n  {'identidad':<16}{'genes':>7}{'ventanas riesgosas':>21}{'peor coincid.':>16}")
    por_tramo = {}
    for bajo, alto in TRAMOS:
        grupo = [d for d in datos if bajo <= d[0] < alto]
        if not grupo:
            continue
        media_riesgo = sum(d[1] for d in grupo) / len(grupo)
        media_peor = sum(d[2] for d in grupo) / len(grupo)
        por_tramo[(bajo, alto)] = (len(grupo), media_riesgo, media_peor)
        print(f"  {bajo:.2f} a {alto:.2f}    {len(grupo):>7}{media_riesgo * 100:>20.1f}%"
              f"{media_peor:>16.1f}")

    muy = [d for d in datos if d[0] >= 0.85]
    limpios = sum(1 for d in muy if d[1] < 0.5) if muy else 0
    if muy:
        print(f"\n  genes con identidad >= 0,85: {len(muy)}")
        print(f"    con MENOS de la mitad de sus ventanas riesgosas: {limpios} "
              f"({limpios / len(muy) * 100:.0f} %)")
        sin_salida = [d for d in muy if d[1] >= 0.9]
        print(f"    con 90 % o mas de sus ventanas riesgosas (sin salida): {len(sin_salida)}")
    return {"rho": rho, "rho_max": rho_max, "tramos": por_tramo,
            "muy": len(muy), "limpios": limpios}


def main() -> None:
    conservacion = cargar_conservacion()
    print(f"loci con identidad conocida: {len(conservacion)}")

    resumen = {}
    for nombre, archivo, columna in JUEGOS:
        ruta = SALIDA / archivo
        if not ruta.exists():
            print(f"\n[falta {archivo}, salteo '{nombre}']")
            continue
        datos = medir(ruta, columna, conservacion)
        if len(datos) < 10:
            print(f"\n[pocos genes para '{nombre}' ({len(datos)}), salteo]")
            continue
        resumen[nombre] = informe(nombre, datos)

    if len(resumen) > 1:
        print(f"\n{'=' * 72}")
        print("COMPARACION")
        print("=" * 72)
        print(f"{'lista de no objetivo':<32}{'rho':>8}{'riesgo 0-0,5':>14}{'riesgo >=0,85':>15}")
        for nombre, r in resumen.items():
            bajo = r["tramos"].get((0.0, 0.5))
            alto = r["tramos"].get((0.85, 1.01))
            t_bajo = f"{bajo[1] * 100:.1f}%" if bajo else "-"
            t_alto = f"{alto[1] * 100:.1f}%" if alto else "-"
            print(f"{nombre:<32}{r['rho']:>+8.3f}{t_bajo:>14}{t_alto:>15}")
        print("\nSi rho sube al acercarse la especie, la tension existe pero vive en los")
        print("parientes del insecto, no en el cultivo. Si no sube, no existe y hay que")
        print("dejar de contarla como si existiera.")


if __name__ == "__main__":
    main()
