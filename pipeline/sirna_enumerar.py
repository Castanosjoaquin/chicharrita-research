"""De un locus del genoma a las ventanas de 21 nt rankeadas.

Cierra la cadena completa: gen candidato -> secuencia codificante -> todas las ventanas
posibles -> features de diseno -> ranking explicable.

El espacio de diseno aca es ELEGIR, no generar: para un transcripto dado, el siRNA es una
ventana del mensajero. Un CDS de 1,5 kb tiene ~1.480 ventanas de 21 nt. Enumerarlas todas
es trivial y exacto, y ademas auditable: cada numero del ranking se puede explicar.

Features que calcula, y de donde sale cada regla:
  gc                 contenido GC global de la ventana.
  gc_9_14            GC en las posiciones 9-14 de la hebra guia. [sin-verificar] La corrida
                     previa del equipo dice que en insectos GC alto aca ayuda, al reves que
                     en los datos humanos. Hay que confirmarlo contra dsRIP.
  a_en_10            si la guia tiene A en la posicion 10. [sin-verificar] misma fuente.
  asimetria          dG(extremo 5' de la guia) - dG(extremo 5' del pasajero), con ViennaRNA.
                     Positivo = el extremo 5' de la guia es MENOS estable = se carga mejor.
                     [paper] Es la regla que mejor transfiere entre especies.
  dg_duplex          energia libre del duplex guia:pasajero completo.
  accesibilidad      probabilidad de que el sitio blanco este desapareado, con RNAplfold.
                     [sin-verificar] En insectos dsRIP no la encontro significativa.
  corrida_max        corrida mas larga de nucleotidos identicos. Las herramientas serias
                     filtran a proposito las de mas de 4.

El score es una suma ponderada explicita y los pesos estan arriba, a la vista, para que se
puedan discutir y para que el analisis de sensibilidad tenga sobre que correr. NO es un
modelo entrenado: no hay datos de eficacia para esta especie con que entrenarlo.

Uso:
    python3 sirna_enumerar.py <genoma.fna.gz> <anotacion.gff> <ID_del_mRNA> [--csv salida.csv]
"""

from __future__ import annotations

import csv
import gzip
import sys
from pathlib import Path

import RNA

VENTANA = 21
PESOS = {
    "asimetria": 0.35,
    "gc_9_14": 0.20,
    "accesibilidad": 0.20,
    "gc": 0.15,
    "a_en_10": 0.10,
}
GC_IDEAL = (0.36, 0.52)
COMPLEMENTO = str.maketrans("ACGTNacgtn", "TGCANtgcan")


def revcomp(s: str) -> str:
    return s.translate(COMPLEMENTO)[::-1]


def leer_cromosoma(genoma: Path, nombre: str) -> str:
    """Devuelve la secuencia de un solo cromosoma, sin cargar el genoma entero."""
    partes: list[str] = []
    dentro = False
    abrir = gzip.open if genoma.suffix == ".gz" else open
    with abrir(genoma, "rt") as fh:
        for linea in fh:
            if linea.startswith(">"):
                if dentro:
                    break
                dentro = linea[1:].split()[0] == nombre
            elif dentro:
                partes.append(linea.strip())
    return "".join(partes).upper()


def cds_del_mrna(gff: Path, id_mrna: str) -> tuple[str, str, list[tuple[int, int]]]:
    """Devuelve (cromosoma, hebra, lista de exones CDS ordenados 5'->3')."""
    cromosoma = hebra = ""
    exones: list[tuple[int, int]] = []
    for linea in gff.read_text(encoding="utf-8").splitlines():
        if linea.startswith("#") or "\t" not in linea:
            continue
        c = linea.split("\t")
        if len(c) < 9 or c[2] != "CDS" or f"Parent={id_mrna}" not in c[8]:
            continue
        cromosoma, hebra = c[0], c[6]
        exones.append((int(c[3]), int(c[4])))
    if not exones:
        raise SystemExit(f"no se encontraron CDS para {id_mrna} en {gff}")
    exones.sort(reverse=hebra == "-")
    return cromosoma, hebra, exones


def armar_cds(seq: str, hebra: str, exones: list[tuple[int, int]]) -> str:
    trozos = [seq[ini - 1:fin] for ini, fin in exones]
    if hebra == "-":
        trozos = [revcomp(t) for t in trozos]
    return "".join(trozos)


def dg_extremo(duplex_5p: str) -> float:
    """Estabilidad de los 4 nt de un extremo del duplex. Menos negativo = mas suelto."""
    return RNA.duplexfold(duplex_5p.replace("T", "U"), revcomp(duplex_5p).replace("T", "U")).energy


def corrida_maxima(s: str) -> int:
    mejor = actual = 1
    for i in range(1, len(s)):
        actual = actual + 1 if s[i] == s[i - 1] else 1
        mejor = max(mejor, actual)
    return mejor


def accesibilidad(cds: str, ulength: int = 8, ventana: int = 80, span: int = 40) -> list[float]:
    """Probabilidad de estar desapareado por posicion, con RNAplfold."""
    up = RNA.pfl_fold_up(cds.replace("T", "U"), ulength, ventana, span)
    # up[i][u] = prob de que el tramo de largo u que termina en i este desapareado (1-indexado)
    return [up[i][ulength] if i < len(up) and ulength < len(up[i]) else 0.0 for i in range(len(up))]


def normalizar(valores: list[float]) -> list[float]:
    lo, hi = min(valores), max(valores)
    return [0.5] * len(valores) if hi == lo else [(v - lo) / (hi - lo) for v in valores]


def deseabilidad_gc(gc: float) -> float:
    """1.0 dentro del rango ideal, cae linealmente afuera. Derringer-Suich simplificado."""
    bajo, alto = GC_IDEAL
    if bajo <= gc <= alto:
        return 1.0
    return max(0.0, 1.0 - (bajo - gc if gc < bajo else gc - alto) / 0.25)


def enumerar(cds: str) -> list[dict]:
    acc = accesibilidad(cds)
    filas = []
    for i in range(len(cds) - VENTANA + 1):
        sitio = cds[i:i + VENTANA]
        if "N" in sitio:
            continue
        guia = revcomp(sitio)
        gc = (sitio.count("G") + sitio.count("C")) / VENTANA
        region = guia[8:14]
        filas.append({
            "pos": i + 1,
            "sitio": sitio,
            "guia": guia,
            "gc": round(gc, 4),
            "gc_9_14": round((region.count("G") + region.count("C")) / len(region), 4),
            "a_en_10": int(guia[9] == "A"),
            "asimetria": round(dg_extremo(guia[:4]) - dg_extremo(sitio[:4]), 3),
            "dg_duplex": round(RNA.duplexfold(guia.replace("T", "U"), sitio.replace("T", "U")).energy, 3),
            "accesibilidad": round(acc[min(i + VENTANA - 1, len(acc) - 1)], 5),
            "corrida_max": corrida_maxima(sitio),
            "desea_gc": round(deseabilidad_gc(gc), 4),
        })
    return filas


def puntuar(filas: list[dict]) -> None:
    """Filtro duro primero, despues score ponderado. El descarte queda explicito."""
    for f in filas:
        f["descarte"] = "corrida>4" if f["corrida_max"] > 4 else ""

    vivos = [f for f in filas if not f["descarte"]]
    if not vivos:
        return
    normas = {k: normalizar([f[k] for f in vivos]) for k in ("asimetria", "gc_9_14", "accesibilidad")}
    for j, f in enumerate(vivos):
        d = {
            "asimetria": normas["asimetria"][j],
            "gc_9_14": normas["gc_9_14"][j],
            "accesibilidad": normas["accesibilidad"][j],
            "gc": f["desea_gc"],
            "a_en_10": float(f["a_en_10"]),
        }
        f["score"] = round(sum(PESOS[k] * d[k] for k in PESOS), 4)
        # Media geometrica ponderada: un criterio malo baja el total sin necesidad de veto
        # manual. Con suma ponderada, un candidato con accesibilidad pesima puede entrar
        # igual al top si compensa con los otros. Con media geometrica, no.
        producto = 1.0
        for k in PESOS:
            producto *= max(d[k], 1e-6) ** PESOS[k]
        f["score_geom"] = round(producto, 4)
    for f in filas:
        f.setdefault("score", 0.0)
        f.setdefault("score_geom", 0.0)


def comparar_agregaciones(filas: list[dict], n: int = 10) -> None:
    """Muestra cuanto cambia el top-N segun como se agreguen los criterios."""
    vivos = [f for f in filas if not f["descarte"]]
    top_suma = {f["pos"] for f in sorted(vivos, key=lambda f: -f["score"])[:n]}
    top_geom = {f["pos"] for f in sorted(vivos, key=lambda f: -f["score_geom"])[:n]}
    comunes = top_suma & top_geom
    print(f"\nSuma ponderada vs media geometrica, top-{n}: {len(comunes)} de {n} coinciden.")
    if top_suma - top_geom:
        print(f"  solo en suma ponderada : {sorted(top_suma - top_geom)}")
        peor = min((f for f in vivos if f["pos"] in top_suma - top_geom),
                   key=lambda f: f["accesibilidad"])
        print(f"  el caso que lo explica : pos {peor['pos']} entra con accesibilidad "
              f"{peor['accesibilidad']:.4f} porque compensa con asimetria {peor['asimetria']:.1f}")
    if top_geom - top_suma:
        print(f"  solo en media geometrica: {sorted(top_geom - top_suma)}")


def sensibilidad(filas: list[dict], n: int = 10, muestras: int = 2000) -> None:
    """Frecuencia de aparicion en el top-N sobre todo el espacio de pesos (Dirichlet).

    Responde la pregunta que importa: cuales candidatos son robustos a como pesemos
    los criterios, y cuales estan arriba solo por los pesos que elegimos nosotros.
    """
    import random

    vivos = [f for f in filas if not f["descarte"]]
    if not vivos:
        return
    claves = list(PESOS)
    normas = {k: normalizar([f[k] for f in vivos]) for k in ("asimetria", "gc_9_14", "accesibilidad")}
    base = []
    for j, f in enumerate(vivos):
        base.append({
            "asimetria": normas["asimetria"][j], "gc_9_14": normas["gc_9_14"][j],
            "accesibilidad": normas["accesibilidad"][j], "gc": f["desea_gc"],
            "a_en_10": float(f["a_en_10"]), "pos": f["pos"],
        })

    conteo: dict[int, int] = {}
    rnd = random.Random(0)
    for _ in range(muestras):
        w = [rnd.gammavariate(1.0, 1.0) for _ in claves]
        total = sum(w)
        w = {k: v / total for k, v in zip(claves, w)}
        mejores = sorted(base, key=lambda d: -sum(w[k] * d[k] for k in claves))[:n]
        for d in mejores:
            conteo[d["pos"]] = conteo.get(d["pos"], 0) + 1

    print(f"\nEstabilidad sobre {muestras} juegos de pesos al azar (Dirichlet uniforme):")
    print(f"{'pos':>6}{'frec en top-10':>16}")
    for pos, c in sorted(conteo.items(), key=lambda x: -x[1])[:8]:
        print(f"{pos:>6}{c / muestras * 100:>15.1f}%")
    robustos = sum(1 for c in conteo.values() if c / muestras > 0.5)
    print(f"candidatos distintos que pasaron por el top-10: {len(conteo)}")
    print(f"candidatos que estan en el top-10 en mas de la mitad de los pesos: {robustos}")


def main() -> None:
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    genoma, gff, id_mrna = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]

    cromosoma, hebra, exones = cds_del_mrna(gff, id_mrna)
    secuencia = leer_cromosoma(genoma, cromosoma)
    cds = armar_cds(secuencia, hebra, exones)
    print(f"{id_mrna}: {cromosoma}({hebra}), {len(exones)} exones, CDS de {len(cds)} nt")

    filas = enumerar(cds)
    puntuar(filas)
    descartados = sum(1 for f in filas if f["descarte"])
    print(f"ventanas de {VENTANA} nt: {len(filas)}  ·  descartadas por filtro duro: {descartados}")

    top = sorted((f for f in filas if not f["descarte"]), key=lambda f: -f["score"])[:10]
    print(f"\n{'pos':>6}  {'guia (5->3)':<23}{'score':>7}{'asim':>7}{'gc':>7}{'gc9_14':>8}{'acces':>8}{'A10':>5}")
    for f in top:
        print(f"{f['pos']:>6}  {f['guia']:<23}{f['score']:>7.3f}{f['asimetria']:>7.2f}"
              f"{f['gc']:>7.2f}{f['gc_9_14']:>8.2f}{f['accesibilidad']:>8.4f}{f['a_en_10']:>5}")

    comparar_agregaciones(filas)
    sensibilidad(filas)

    if "--csv" in sys.argv:
        destino = Path(sys.argv[sys.argv.index("--csv") + 1])
        with destino.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
            w.writeheader()
            w.writerows(filas)
        print(f"\ncsv con las {len(filas)} ventanas en {destino}")


if __name__ == "__main__":
    main()
