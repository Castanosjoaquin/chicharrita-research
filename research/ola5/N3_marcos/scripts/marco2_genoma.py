"""N3 - El marco intermedio sobre el gen tal como lo escribe el genoma, sin blastn.

Por que existe. `N3` §7 declaro esta fuente como no corrida con un motivo que no se sostenia
--«son 984 MB y sin alineador de consultas largas no se ubica el gen»--. El locus ya estaba en
disco: `M1` mapeo los 21-meros del gen contra el genoma con el bowtie del instalador de
si-Fi2015, y `work/M1/hits/dmaid_genoma_BicC_Dm.txt` tiene 2.178 aciertos exactos, todos en
`OZ319706.1` y en la hebra `+`. Con eso no hace falta alinear nada.

El metodo, que es aritmetica sobre los aciertos y no un alineamiento nuevo. Un acierto exacto
del 21-mero que arranca en la posicion `p` del gen contra el offset `o` del genoma dice que
`gen[p..p+20] == genoma[o..o+20]`, o sea que para ese tramo vale la recta `g(x) = x + d` con
`d = o - p`. Agrupando los arranques cubiertos por `d` constante salen los **exones**, y los
saltos de `d` entre dos grupos son los **empalmes**. Dos huecos de cobertura hay que distinguir
y se distinguen solos:

  - un **empalme** entre las posiciones `j` y `j+1` deja sin acierto exactamente los 20
    arranques `j-19 .. j`, porque son los 21-meros que cruzan la juntura, y **cambia** `d`;
  - una **variante** en la posicion `v` deja sin acierto los 21 arranques `v-20 .. v`, porque
    son los que contienen la base distinta, y **no cambia** `d`.

Asi que cada posicion del gen tiene su exon y su coordenada genomica, y el transcrito tal como
lo escribe el genoma es leer la base del genoma en cada posicion mapeada. Los empalmes no
afectan a esa secuencia: afectan a si un 21-mero existe como tramo contiguo del genoma, que es
otra pregunta y la contesto `M7` §4.

Una posicion que no cae en ningun exon queda **sin datos**, y una region con posiciones sin
datos **no se compara**: se declara no corrida, como hizo `M7` con `GCWP01`.

El ancla es lo que `M7` §4 publico con blastn para esta fuente en el marco 3: 26 para 922-1221
y 22 para 2121-2420. Si la aritmetica sobre los aciertos de bowtie reproduce los conteos del
alineamiento de blastn, la reconstruccion no depende de la herramienta.

Configuracion: punto por defecto, modo `corregido`, ViennaRNA 2.7.2, tabla `RNA_NN3`.

Uso (desde la raiz del repositorio):
    python research/ola5/N3_marcos/scripts/marco2_genoma.py
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
SALIDA = AQUI.parents[1] / "resultados"
sys.path.insert(0, str(AQUI.parent))

from tres_marcos import eficientes, leer_fasta  # noqa: E402

K = 21
GEN = "BicC_Dm"
FASTA_GEN = RAIZ / "work" / "sifi_check" / f"{GEN}_full.fasta"
HITS = RAIZ / "work" / "M1" / "hits" / f"dmaid_genoma_{GEN}.txt"
GENOMA = RAIZ / "work" / "M1" / "bases" / "dmaid_genoma.fa"
CROMOSOMA = "OZ319706.1"

REGIONES = {"922-1221": (922, 1221), "2121-2420": (2121, 2420), "264-563": (264, 563)}
EPILAB = {"922-1221": (36, 29, 26), "2121-2420": (35, 27, 22), "264-563": (20, 15, 17)}

#: Ancla de M7 §4, genoma del Reino Unido, marco 3, modo corregido. 264-563 quedo no corrida
#: ahi por cobertura parcial, asi que no entra al ancla.
ANCLA_M7_MARCO3 = {"922-1221": 26, "2121-2420": 22}


def leer_hits() -> dict[int, int]:
    """{posicion del gen (1-based): offset del genoma (0-based)} de los aciertos exactos."""
    out = {}
    with open(HITS, encoding="utf-8", errors="replace") as fh:
        for linea in fh:
            c = linea.rstrip("\n").split("\t")
            if len(c) < 4 or c[2] != CROMOSOMA or c[1] != "+":
                continue
            nombre = c[0]
            if not nombre.startswith("w"):
                continue
            out[int(nombre[1:])] = int(c[3])
    return out


def exones(hits: dict[int, int]) -> list[tuple[int, int, int]]:
    """Los tramos de `d` constante, como (primer arranque, ultimo arranque, d)."""
    por_d = defaultdict(list)
    for p, o in hits.items():
        por_d[o - p].append(p)
    tramos = []
    for d, ps in por_d.items():
        ps.sort()
        ini = ant = ps[0]
        for p in ps[1:]:
            if p - ant > K:          # un hueco mayor que una variante: otro tramo del mismo d
                tramos.append((ini, ant, d))
                ini = p
            ant = p
        tramos.append((ini, ant, d))
    return sorted(tramos)


def mapa_de_posiciones(tramos, largo):
    """Para cada posicion 1..largo, su coordenada genomica, o None si no cae en ningun exon.

    El borde entre dos exones se resuelve con la regla del encabezado: si el exon de la
    izquierda tiene su ultimo arranque cubierto en `u` y el de la derecha el primero en `v`,
    el empalme cae entre `v - 1` y `v`, asi que la izquierda llega hasta `v - 1`.
    """
    mapa: list[int | None] = [None] * (largo + 1)
    # Cada exon cubre, por sus aciertos, desde su primer arranque hasta su ultimo + 20.
    spans = []
    for i, (ini, fin, d) in enumerate(tramos):
        desde = ini if i == 0 else max(ini, tramos[i - 1][1] + 1)
        hasta = fin + (K - 1)
        spans.append([desde, hasta, d])
    # El limite entre exones consecutivos: la derecha empieza en su primer arranque.
    for i in range(len(spans) - 1):
        _, _, _ = spans[i]
        derecha_ini = tramos[i + 1][0]
        spans[i][1] = min(spans[i][1], derecha_ini - 1)
        spans[i + 1][0] = derecha_ini
    for desde, hasta, d in spans:
        for x in range(max(1, desde), min(largo, hasta) + 1):
            if mapa[x] is None:
                mapa[x] = x + d
    return mapa, spans


def leer_cromosoma(desde: int, hasta: int) -> str:
    """Lee `genoma[desde..hasta]` (0-based, inclusive) de `CROMOSOMA`, sin cargar el archivo."""
    buf, pos, dentro = [], 0, False
    with open(GENOMA, encoding="utf-8", errors="replace") as fh:
        for linea in fh:
            if linea.startswith(">"):
                if dentro:
                    break
                dentro = linea[1:].split()[0] == CROMOSOMA
                continue
            if not dentro:
                continue
            s = linea.strip()
            fin = pos + len(s)
            if fin > desde and pos <= hasta:
                a = max(0, desde - pos)
                b = min(len(s), hasta - pos + 1)
                buf.append(s[a:b])
            pos = fin
            if pos > hasta:
                break
    return "".join(buf).upper().replace("U", "T")


def main() -> int:
    for p in (FASTA_GEN, HITS, GENOMA):
        if not p.exists():
            raise SystemExit("falta %s; `work/` no esta en git" % p)

    gen = leer_fasta(FASTA_GEN)
    hits = leer_hits()
    if not hits:
        raise SystemExit("no hay aciertos exactos de %s en %s" % (GEN, CROMOSOMA))
    tramos = exones(hits)
    mapa, spans = mapa_de_posiciones(tramos, len(gen))

    sin_datos = [x for x in range(1, len(gen) + 1) if mapa[x] is None]
    coords = [c for c in mapa[1:] if c is not None]
    seq = leer_cromosoma(min(coords), max(coords))
    base0 = min(coords)

    reconstruido = []
    for x in range(1, len(gen) + 1):
        c = mapa[x]
        reconstruido.append("N" if c is None else seq[c - base0])
    reconstruido = "".join(reconstruido)
    if len(reconstruido) != len(gen):
        raise SystemExit("la reconstruccion mide %d y el gen %d"
                         % (len(reconstruido), len(gen)))
    desajustes = [i + 1 for i, (a, b) in enumerate(zip(gen, reconstruido))
                  if a != b and b != "N"]

    # Los marcos 1 y 2 pliegan el gen COMPLETO, asi que no se pueden calcular si al gen le
    # faltan posiciones: rellenarlas seria inventar bases, y como el plegado es global una
    # base inventada mueve la accesibilidad de ventanas que estan lejos de ella. El marco 3
    # pliega la molecula, asi que se calcula por region si la region esta completa.
    marcos_de_contexto = not sin_datos
    efic_gen = eficientes(reconstruido) if marcos_de_contexto else None
    filas = {}
    for nom, (i, f) in REGIONES.items():
        ult = f - (K - 1)
        sd = [x for x in sin_datos if i <= x <= f]
        fila = {"epilab": list(EPILAB[nom]),
                "desajustes_en_la_region": sum(1 for d in desajustes if i <= d <= f),
                "empalmes_en_la_region": sum(1 for a, b, _ in spans[1:] if i <= a <= f),
                "posiciones_sin_datos_en_la_region": len(sd)}
        if sd:
            fila["marco3"] = None
            fila["marco3_no_corrido"] = ("la region tiene %d posiciones sin datos en el "
                                         "ensamblado" % len(sd))
        else:
            fila["marco3"] = len(eficientes(reconstruido[i - 1:f]))
        if marcos_de_contexto:
            fila["marco1"] = sum(1 for p in efic_gen if i <= p <= f)
            fila["marco2"] = sum(1 for p in efic_gen if i <= p <= ult)
        else:
            fila["marco1"] = fila["marco2"] = None
            fila["marcos_de_contexto_no_corridos"] = (
                "el gen tiene %d posiciones sin datos en el ensamblado, y los marcos de "
                "contexto pliegan el gen completo" % len(sin_datos))
        filas[nom] = fila

    roto = [("%s marco 3: %s, M7 publico %d" % (n, filas[n].get("marco3"), esp))
            for n, esp in ANCLA_M7_MARCO3.items() if filas[n].get("marco3") != esp]
    if desajustes:
        roto.append("hay %d desajustes contra EPILAB, y M7 §4 no reporto variantes para esta "
                    "fuente: solo ventanas que cruzan empalme" % len(desajustes))
    if roto:
        raise SystemExit("el ancla de M7 no se reprodujo:\n  " + "\n  ".join(roto))

    tramos_sin_datos = []
    if sin_datos:
        ini = ant = sin_datos[0]
        for x in sin_datos[1:]:
            if x != ant + 1:
                tramos_sin_datos.append([ini, ant])
                ini = x
            ant = x
        tramos_sin_datos.append([ini, ant])

    out = {"fuente": "genoma GCA_975739785.1, %s" % CROMOSOMA,
           "tramos_sin_datos": tramos_sin_datos,
           "marcos_de_contexto_corridos": marcos_de_contexto,
           "metodo": "aritmetica sobre los aciertos exactos de bowtie de M1; sin blastn",
           "aciertos_exactos": len(hits), "exones_detectados": len(spans),
           "locus": [min(coords) + 1, max(coords) + 1],
           "posiciones_sin_datos": len(sin_datos),
           "desajustes_contra_epilab": len(desajustes),
           "ancla_m7_marco3": ANCLA_M7_MARCO3,
           "configuracion": {"modo": "corregido", "backend": "vienna", "tabla_nn": "NN3"},
           "regiones": filas}
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "marco2_genoma.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print("%s: %d aciertos exactos, %d exones, locus %d-%d (%.1f kb)"
          % (CROMOSOMA, len(hits), len(spans), min(coords) + 1, max(coords) + 1,
             (max(coords) - min(coords)) / 1000))
    print("posiciones del gen sin datos: %d | desajustes contra EPILAB: %d"
          % (len(sin_datos), len(desajustes)))
    print("\n%-10s %-22s %-22s" % ("region", "EPILAB m1/m2/m3", "genoma m1/m2/m3"))
    print("tramos del gen sin datos: %s" % tramos_sin_datos)
    for nom in REGIONES:
        d = filas[nom]
        cel = lambda v: "-" if v is None else str(v)   # noqa: E731
        print("%-10s %-22s %-24s  desajustes %d, empalmes %d, sin datos %d"
              % (nom, "%d / %d / %d" % tuple(d["epilab"]),
                 "%s / %s / %s" % (cel(d["marco1"]), cel(d["marco2"]), cel(d["marco3"])),
                 d["desajustes_en_la_region"], d["empalmes_en_la_region"],
                 d["posiciones_sin_datos_en_la_region"]))
    if not marcos_de_contexto:
        print("\nlos marcos 1 y 2 quedan NO CORRIDOS: el gen tiene %d posiciones sin datos "
              "en el ensamblado y esos marcos pliegan el gen completo" % len(sin_datos))
    print("\nancla de M7 reproducida sin blastn: %s"
          % {n: filas[n].get("marco3") for n in ANCLA_M7_MARCO3})
    print("resultados en %s" % (SALIDA / "marco2_genoma.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
