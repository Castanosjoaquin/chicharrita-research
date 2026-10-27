"""Verificaciones de `fichas_desde_f1.py`: la salida real de `F1` leida como fichas de `F2`.

Cuatro cosas, y la cuarta es la que importa:

- **Las seis categorias de `F1` caen en el estado que les corresponde**, y ninguna se
  pierde por el camino. Se prueba con un TSV escrito aca que tiene las mismas columnas que
  produce `transferir_anotacion.py` y una fila de cada categoria.
- **La tabla es por ORF y la ficha es por contig.** Gana la mejor categoria del contig
  segun la jerarquia de `F1`, y dentro de la misma categoria el mayor `bitscore`. Se
  prueba con un contig que tiene tres ORF de categorias distintas y con otro que tiene dos
  de la misma.
- **La conversion de proporcion a porcentaje queda en la ficha**, que es la condicion para
  que `verificar_procedencia` pueda respaldar lo que el parrafo dice.
- **El parrafo que sale de una fila real de `F1` pasa la verificacion de procedencia.** Es
  el unico extremo a extremo que hay: si el adaptador inventara un campo, o si el
  vocabulario de la plantilla se desincronizara, esto falla. Corre contra el archivo de
  verdad si esta en disco, y si no esta se **declara salteado**, no se da por bueno.

    python pipeline/test_fichas_desde_f1.py
"""

from __future__ import annotations

import gzip
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import evidencia_en_prosa as P       # noqa: E402
import fichas_desde_f1 as A          # noqa: E402

FALLAS, SALTEADAS = [], []

TABLA_REAL = (RAIZ / "research" / "ola6" / "F1_transferencia_homologia" / "resultados"
              / "transferencia_MQ.tsv.gz")


def check(cond, msg):
    print(("  ok   " if cond else "  FALLA") + "  " + msg)
    if not cond:
        FALLAS.append(msg)


# ------------------------------------------------------------------ el TSV de prueba

# Las columnas son las de `transferir_anotacion.py`, en su orden, y los valores de las
# filas con alineamiento son los de filas reales del archivo de `F1`.
CABECERA = ["contig", "orf_aa", "orf_hebra", "orf_ini", "orf_fin", "categoria",
            "empate_lado", "empate_homonimo", "ref_id", "ref_producto",
            "nombre_normalizado", "pident", "cob_orf", "cob_ref", "rotulo_cobertura",
            "evalue", "bitscore", "banda_identidad", "banda_concordancia", "banda_ic_lo",
            "banda_ic_hi", "banda_pares_c12"]

VACIOS = [""] * 14


def fila(contig, categoria, bitscore="", ref_id="", producto="", pident="",
         cob_orf="", cob_ref="", banda="", conc="", lo="", hi="", pares=""):
    d = dict.fromkeys(CABECERA, "")
    d.update(contig=contig, orf_aa="200", orf_hebra="+", orf_ini="1", orf_fin="600",
             categoria=categoria, ref_id=ref_id, ref_producto=producto,
             nombre_normalizado=producto.lower(), pident=pident, cob_orf=cob_orf,
             cob_ref=cob_ref, bitscore=bitscore, banda_identidad=banda,
             banda_concordancia=conc, banda_ic_lo=lo, banda_ic_hi=hi,
             banda_pares_c12=pares)
    if categoria == "d_empate":
        d["empate_lado"] = "directo"
    return [d[c] for c in CABECERA]


ALTA = dict(banda=">=90", conc="0.862", lo="0.809", hi="0.902", pares="210")
BAJA = dict(banda="<40", conc="0.250", lo="0.102", hi="0.495", pares="16")

FILAS = [
    fila("C_nombre", "f_reciproco_con_nombre", "765", "XP_046681924.1",
         "RNA-binding protein fusilli isoform X2", "98.8", "99.1", "100", **ALTA),
    fila("C_sinnombre", "e_reciproco_sin_nombre", "400", "XP_054259524.1",
         "uncharacterized protein LOC128984247", "86.5", "99.8", "47.4",
         banda="80-90", conc="0.786", lo="0.739", hi="0.826", pares="336"),
    fila("C_empate", "d_empate", "300", "XP_054279750.1",
         "single-stranded DNA-binding protein 3-like isoform X3", "98.5", "96.9", "100",
         **ALTA),
    fila("C_noreciproco", "c_hit_no_reciproco", "250", "XP_054269953.1",
         "nuclear hormone receptor FTZ-F1 beta isoform X3", "92.9", "96.5", "70.5",
         **ALTA),
    fila("C_sinhit", "b_sin_hit"),
    fila("C_sinorf", "a_sin_orf"),
    fila("C_floja", "f_reciproco_con_nombre", "120", "XP_000000001.1",
         "cuticle protein 7", "38.0", "80.0", "75.0", **BAJA),
    # Un contig con tres ORF: gana la mejor categoria, no el primero ni el de mas bitscore.
    fila("C_varios", "b_sin_hit", "0"),
    fila("C_varios", "f_reciproco_con_nombre", "90", "XP_046681925.1",
         "chitin synthase", "95.0", "88.0", "92.0", **ALTA),
    fila("C_varios", "c_hit_no_reciproco", "9000", "XP_046681926.1", "otra cosa", "99.0",
         "99.0", "99.0", **ALTA),
    # Dos ORF de la MISMA categoria: gana el de mayor bitscore.
    fila("C_dosiguales", "f_reciproco_con_nombre", "100", "XP_111.1", "proteina baja",
         "91.0", "80.0", "80.0", **ALTA),
    fila("C_dosiguales", "f_reciproco_con_nombre", "900", "XP_999.1", "proteina alta",
         "97.0", "90.0", "90.0", **ALTA),
]

tmp = Path(tempfile.mkdtemp(prefix="f1_fichas_"))
RUTA = tmp / "transferencia_MQ.tsv.gz"
with gzip.open(RUTA, "wt", encoding="utf-8", newline="") as fh:
    fh.write("\t".join(CABECERA) + "\n")
    for f in FILAS:
        fh.write("\t".join(f) + "\n")


# --------------------------------------------- 1. cada categoria cae donde corresponde

print("\n1. las seis categorias de F1 caen en el estado de F2 que les corresponde")

por_contig = {f["locus"]: f for f in A.fichas(RUTA)}
check(len(por_contig) == 9, "nueve contigs distintos a partir de doce filas (%d)"
      % len(por_contig))

esperado = {
    "C_nombre": P.ANOTADA,
    "C_sinnombre": P.ANOTACION_NO_INFORMATIVA,
    "C_empate": P.EMPATE_DE_ORTOLOGIA,
    "C_noreciproco": P.ORTOLOGIA_NO_RECIPROCA,
    "C_sinhit": P.SIN_ANOTACION_DE_GEN,
    "C_sinorf": P.SIN_ANOTACION_DE_GEN,
}
for contig, estado in esperado.items():
    dio = P.estado_de(por_contig[contig])
    check(dio == estado, "%s -> %s (dio %s)" % (contig, estado, dio))

check(por_contig["C_sinhit"]["anotacion"] is None,
      "un contig sin hit no se inventa un bloque de anotacion")
check(all(f["unidad"] == "contig" for f in por_contig.values()),
      "todas las fichas declaran que su unidad es el contig, no el locus")
check(all(f["go"] == [] and f["dominios"] == [] and f["papers"] == []
          for f in por_contig.values()),
      "F1 no produce GO, dominios ni papers, y las listas quedan vacias sin rellenarse")


# --------------------------------------------------- 2. de fila por ORF a ficha por contig

print("\n2. la tabla es por ORF y la ficha es por contig")

check(P.estado_de(por_contig["C_varios"]) == P.ANOTADA,
      "con tres ORF gana la mejor categoria, no el bitscore mas alto")
check(por_contig["C_varios"]["anotacion"]["accesion"] == "XP_046681925.1",
      "y la ficha se queda con la fila de esa categoria (%s)"
      % por_contig["C_varios"]["anotacion"]["accesion"])
check(por_contig["C_dosiguales"]["anotacion"]["accesion"] == "XP_999.1",
      "dentro de la misma categoria gana el mayor bitscore")


# ------------------------------------------------------- 3. la conversion queda en la ficha

print("\n3. la concordancia pasa de proporcion a porcentaje, y queda guardada")

banda = por_contig["C_nombre"]["anotacion"]["banda"]
check(banda["concordancia"] == 86.2 and banda["ic"] == [80.9, 90.2] and banda["n"] == 210,
      "0,862 se guarda como 86,2 con su IC y sus pares (%s)" % banda)
check(banda["concluyente"] is True, "el tramo >=90 es concluyente")
check(por_contig["C_floja"]["anotacion"]["banda"]["concluyente"] is False,
      "y el tramo <40, que F1 rotula no concluyente, no lo es")
check("no concluyente" in P.redactar(por_contig["C_floja"])["texto"],
      "el parrafo de un tramo no concluyente lo dice")

# El organismo sale del sufijo del archivo, y un sufijo que no es de los dos proteomas del
# preregistro tiene que fallar en vez de adivinarse.
check(A.organismo_de(RUTA) == "Macrosteles quadrilineatus",
      "el proteoma de referencia sale del nombre del archivo")
try:
    A.organismo_de(Path("transferencia_XX.tsv.gz"))
    check(False, "un proteoma desconocido levanta ValueError (no levanto nada)")
except ValueError:
    check(True, "un proteoma desconocido levanta ValueError en vez de adivinarse")


# ----------------------------------------- 4. extremo a extremo, contra el archivo real

print("\n4. el parrafo de una fila de F1 pasa la verificacion de procedencia")

for contig in ("C_nombre", "C_varios", "C_dosiguales", "C_floja"):
    ficha = por_contig[contig]
    r = P.redactar(ficha)
    v = P.verificar_procedencia(r, ficha)
    check(v["ok"], "%s: el parrafo pasa la verificacion (%s)"
          % (contig, ", ".join(v["fuera_de_ficha"] + v["fuentes_invalidas"])
             or "sin sobrantes"))

if not TABLA_REAL.exists():
    SALTEADAS.append("§4 la tabla real de F1 no esta en disco (%s): el extremo a extremo "
                     "corre solo contra el TSV de prueba"
                     % TABLA_REAL.relative_to(RAIZ))
else:
    reales = A.fichas(TABLA_REAL)
    cuenta = P.censo(reales)
    check(cuenta["total"] == len(reales) and cuenta[P.FICHA_INCOMPLETA] == 0,
          "las %d fichas reales se leen todas y ninguna queda incompleta (%d incompletas)"
          % (len(reales), cuenta[P.FICHA_INCOMPLETA]))
    fallidas = []
    for ficha in reales:
        r = P.redactar(ficha)
        if not P.verificar_procedencia(r, ficha)["ok"]:
            fallidas.append(ficha["locus"])
    check(not fallidas,
          "los %d parrafos reales pasan la verificacion de procedencia (%d fallan: %s)"
          % (cuenta[P.ANOTADA], len(fallidas), ", ".join(fallidas[:5]) or "ninguno"))
    print("     censo real: %s" % {k: cuenta[k] for k in P.ESTADOS})


print()
if SALTEADAS:
    print("SALTEADAS: %s" % "; ".join(SALTEADAS))
if FALLAS:
    print("FALLAS: %d" % len(FALLAS))
    sys.exit(1)
print("todo bien")
