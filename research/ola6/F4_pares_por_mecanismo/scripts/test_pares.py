#!/usr/bin/env python3
"""Verificaciones del selector de pares de `F4`. No necesita nada de `work/`.

Las diez secciones prueban las propiedades que el criterio de terminado del issue #39 pide
por escrito, mas las que el preregistro agrega. Corren sobre la tabla real de `F3` y, donde
hace falta probar que la regla lee la tabla y no una lista, sobre tablas sinteticas escritas
en un directorio temporal: ninguna seccion lee una secuencia y ninguna escribe en
`resultados/`.

- **§1 Los excluidos no pueden aparecer en ninguna combinacion.** Es el criterio de terminado
  del issue: los dos de signo invertido, los dos de mortalidad no atribuible al blanco y el
  potenciador de entrega. Se prueba **exhaustivamente**, sobre los seis pares de los cuatro
  mecanismos y sobre las dos puntas de cada par.
- **§2 La exclusion es por etiqueta y no por identificador.** Una fila nueva con
  `fenotipo_invertido` queda afuera sin tocar el codigo, y una fila hoy excluida que cambiara
  de etiqueta entraria: las dos cosas prueban que la regla vive en la tabla. Es la propiedad
  que evita que esta linea siga publicando una asignacion vieja cuando el catalogo cambie.
- **§3 La tabla que cambio de semantica aborta.** Etiqueta desconocida, mecanismo
  desconocido, las tres senales en desacuerdo y el esquema cambiado: los cuatro paran la
  corrida en vez de excluir o admitir en silencio.
- **§4 `D67`: los dos mecanismos tienen que ser distintos** y un candidato no se empareja
  consigo mismo aunque tenga los dos.
- **§5 El cuarto mecanismo esta detras de una puerta.** `transmision` aborta sin
  `--ampliar-d67`, corre con el, y entonces **cada** fila lleva la condicion.
- **§6 La salida dice cuantos candidatos sostienen cada mecanismo**, y una combinacion que
  descansa en una sola fila se ve: `movilidad` tiene un solo candidato y su contraevidencia
  viaja al lado, verificada textual contra la tabla.
- **§7 Ninguna recomendacion.** No hay columna de puntaje, de puesto ni de orden de calidad,
  y el orden de las filas es alfabetico por identificador.
- **§8 La enumeracion es determinista**: dos corridas del mismo pedido dan la misma lista, en
  el mismo orden, sin semilla.
- **§9 Ningun identificador de candidato esta escrito en el codigo que decide.** Se recorre
  el AST del selector y se excluyen los docstrings. Es la forma de desactivar la regla del §2
  sin tocarla: volver a escribir al lado la lista que reemplaza.
- **§10 El puente con `O4` no enumera un par que no sea elegible**, y el motivo que imprime
  sale de la tabla.

Uso:
    python research/ola6/F4_pares_por_mecanismo/scripts/test_pares.py
"""

from __future__ import annotations

import ast
import csv
import itertools
import re
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(RAIZ / "research/ola6/O4_enumerador_quimeras/scripts"))
import pares_por_mecanismo as PM   # noqa: E402

FALLAS: list[str] = []


def check(cond, msg):
    print("  %s %s" % ("ok  " if cond else "FALLA", msg))
    if not cond:
        FALLAS.append(msg)


def aborta(fn, *args, **kw) -> str:
    """Corre `fn` esperando que pare. Devuelve el mensaje, o '' si no paro."""
    try:
        fn(*args, **kw)
    except SystemExit as e:
        return str(e)
    return ""


def tabla_con(cambios: dict[str, dict], agregar: list[dict] | None = None,
              columnas=PM.COLUMNAS) -> Path:
    """Una copia de la tabla de `F3` con los cambios pedidos, en un temporal."""
    filas = [dict(f) for f in PM.leer_tabla()]
    for f in filas:
        f.update(cambios.get(f["id"], {}))
    filas.extend(agregar or [])
    p = Path(tempfile.mkdtemp(prefix="f4_test_")) / "eje_fenotipo.tsv"
    with p.open("w", encoding="utf-8", newline="") as fh:
        esc = csv.DictWriter(fh, fieldnames=list(columnas), delimiter="\t",
                             lineterminator="\n", extrasaction="ignore")
        esc.writeheader()
        esc.writerows(filas)
    return p


def contraevidencia_con(filas: list[dict], columnas=PM.COLUMNAS_CONTRA) -> Path:
    """Un `contraevidencia.tsv` sintetico, para probar sus dos candados."""
    p = Path(tempfile.mkdtemp(prefix="f4_test_")) / "contraevidencia.tsv"
    with p.open("w", encoding="utf-8", newline="") as fh:
        esc = csv.DictWriter(fh, fieldnames=list(columnas), delimiter="\t",
                             lineterminator="\n", extrasaction="ignore")
        esc.writeheader()
        esc.writerows(filas)
    return p


FILAS = PM.leer_tabla()
ELEGIBLES, EXCLUIDOS = PM.clasificar(FILAS)
PM.verificar(FILAS, ELEGIBLES, EXCLUIDOS)
CONTRA = PM.leer_contraevidencia(ELEGIBLES, FILAS)
SOP = PM.soporte(ELEGIBLES)
#: Los seis pares de los cuatro mecanismos. Con la puerta abierta, para que la exhaustividad
#: del §1 cubra tambien las combinaciones que amplian `D67`.
PEDIDOS = list(itertools.permutations(PM.MECANISMOS, 2))


print("§1 los excluidos no pueden aparecer en ninguna combinacion (criterio del issue #39)")
#: Las etiquetas que el issue nombra una por una. Las otras tres de `F3` quedan igual de
#: afuera, y el conteo de abajo lo verifica.
ETIQUETAS_DEL_ISSUE = ("fenotipo_invertido", "sin_fenotipo_atribuible_al_blanco",
                       "potenciador_de_entrega")
prohibidos = {i for i, f in EXCLUIDOS.items()
              if f["etiqueta_de_ausencia"] in ETIQUETAS_DEL_ISSUE}
check(len(prohibidos) == 5,
      "la tabla trae los cinco que el issue nombra: dos de signo invertido, dos de mortalidad "
      "no atribuible y el potenciador (son %d: %s)" % (len(prohibidos), sorted(prohibidos)))
todas = []
for x, y in PEDIDOS:
    todas.extend(PM.pares(ELEGIBLES, x, y, SOP, CONTRA, True))
check(len(todas) > 0, "hay %d asignaciones de rol sobre los seis pares de mecanismos"
      % len(todas))
aparecen = {p[k] for p in todas for k in ("id_a", "id_b")}
check(not (aparecen & prohibidos),
      "ninguno de los cinco aparece en ninguna de las %d asignaciones (aparecen %s)"
      % (len(todas), sorted(aparecen & prohibidos)))
check(not (aparecen & set(EXCLUIDOS)),
      "ni ninguna de las once filas excluidas (aparecen %s)"
      % sorted(aparecen & set(EXCLUIDOS)))
check(aparecen <= set(ELEGIBLES),
      "todo lo que aparece es una fila elegible de la tabla")
check(all(p["id_a"] != p["id_b"] for p in todas),
      "ninguna asignacion empareja un candidato consigo mismo")

print("\n§2 la exclusion es por etiqueta y no por identificador")
nueva = {"id": "ZZ-01", "especie": "Especie sintetica", "gen": "gen sintetico",
         "familia_id": "ZZ", "mecanismos": "", "etiqueta_de_ausencia": "fenotipo_invertido",
         "entra_al_orden_por_fenotipo": "no", "marcador_evidencia": "R",
         "frases_de_apoyo": "silenciarlo AUMENTA la cosa", "evidencia_negativa_medida": "",
         "tiene_ventanas_21nt": "no", "nota": "fila sintetica de la prueba"}
f2 = PM.leer_tabla(tabla_con({}, [nueva]))
e2, x2 = PM.clasificar(f2)
check("ZZ-01" in x2 and "ZZ-01" not in e2,
      "una fila nueva con fenotipo_invertido queda afuera sin tocar el codigo")
sop2 = PM.soporte(e2)
check(not any("ZZ-01" in (p["id_a"], p["id_b"])
              for x, y in PEDIDOS
              for p in PM.pares(e2, x, y, sop2, CONTRA, True)),
      "y no aparece en ninguna combinacion de los seis pares")
# El mismo mecanismo al reves: si F3 cambiara de lectura, esta linea la sigue en vez de
# divergir en silencio. Se prueba sobre una fila hoy excluida por signo invertido.
invertido = sorted(i for i, f in EXCLUIDOS.items()
                   if f["etiqueta_de_ausencia"] == "fenotipo_invertido")[0]
f3 = PM.leer_tabla(tabla_con({invertido: {"etiqueta_de_ausencia": "", "mecanismos": "letalidad",
                                          "entra_al_orden_por_fenotipo": "si"}}))
e3, x3 = PM.clasificar(f3)
check(invertido in e3 and invertido not in x3,
      "y si esa misma fila cambiara de etiqueta en la tabla, entraria: la regla vive en la "
      "tabla y no en una lista de identificadores")

print("\n§3 la tabla que cambio de semantica aborta, no excluye ni admite en silencio")
ident = sorted(ELEGIBLES)[0]
casos = (
    ({ident: {"mecanismos": "", "etiqueta_de_ausencia": "etiqueta_que_nadie_declaro",
              "entra_al_orden_por_fenotipo": "no"}}, "etiqueta desconocida"),
    ({ident: {"mecanismos": "superpoder"}}, "mecanismo desconocido"),
    ({ident: {"entra_al_orden_por_fenotipo": "no"}}, "las tres senales en desacuerdo"),
)
for cambios, caso in casos:
    msg = aborta(PM.clasificar, PM.leer_tabla(tabla_con(cambios)))
    check(msg != "" and ident in msg or "etiqueta_que_nadie_declaro" in msg,
          "%s: aborta y nombra la fila" % caso)
sin_columna = tuple(c for c in PM.COLUMNAS if c != "nota")
msg = aborta(PM.leer_tabla, tabla_con({}, columnas=sin_columna))
check("el esquema cambio" in msg, "el esquema cambiado aborta en la lectura")

print("\n§4 D67: los dos mecanismos tienen que ser distintos")
msg = aborta(PM.pedido, "letalidad,letalidad", True)
check("no se solapan" in msg, "pedir dos veces el mismo mecanismo aborta y cita D67")
msg = aborta(PM.pedido, "letalidad", True)
check("separados por coma" in msg, "un solo mecanismo aborta")
msg = aborta(PM.pedido, "letalidad,inventado", True)
check("desconocido" in msg, "un mecanismo que no es de F3 aborta")
#: `DM-02` es el caso real: tiene `letalidad` y `movilidad` a la vez.
dobles = [i for i, f in ELEGIBLES.items()
          if {"letalidad", "movilidad"} <= set(f["mecanismos_lista"])]
check(len(dobles) == 1, "hay un candidato con letalidad y movilidad a la vez (son %d)"
      % len(dobles))
ps = PM.pares(ELEGIBLES, "letalidad", "movilidad", SOP, CONTRA, False)
check(all(p["id_a"] != p["id_b"] for p in ps) and dobles[0] not in
      [p["id_a"] for p in ps if p["id_b"] == dobles[0]],
      "y no se empareja consigo mismo: una quimera son dos fragmentos de dos genes")

print("\n§5 el cuarto mecanismo esta detras de una puerta")
msg = aborta(PM.pedido, "letalidad,transmision", False)
check("ampliacion de D67" in msg and "ADR" in msg,
      "transmision aborta sin --ampliar-d67 y nombra que falta el ADR")
check(PM.pedido("letalidad,transmision", True) == ("letalidad", "transmision"),
      "con --ampliar-d67 el pedido se acepta")
ps_t = PM.pares(ELEGIBLES, "letalidad", "transmision", SOP, CONTRA, True)
check(len(ps_t) > 0 and all(p["ampliacion_de_d67_sin_adr"] == "si" for p in ps_t),
      "y las %d filas resultantes llevan la condicion pegada, todas" % len(ps_t))
ps_d67 = PM.pares(ELEGIBLES, "letalidad", "reproduccion", SOP, CONTRA, False)
check(all(p["ampliacion_de_d67_sin_adr"] == "no" for p in ps_d67),
      "y un pedido de los tres de D67 no la lleva")

print("\n§6 la salida dice cuantos candidatos sostienen cada mecanismo")
check(all(p["candidatos_que_sostienen_rol_a"] == SOP[p["rol_a"]]["n"]
          and p["candidatos_que_sostienen_rol_b"] == SOP[p["rol_b"]]["n"]
          for p in todas),
      "cada fila trae el respaldo de sus dos roles")
solos = [m for m in PM.MECANISMOS if SOP[m]["descansa_en_un_solo_candidato"]]
check(solos == ["movilidad"],
      "el unico mecanismo que descansa en una sola fila es movilidad (son %s)" % solos)
con_movilidad = [p for p in todas if "movilidad" in (p["rol_a"], p["rol_b"])]
check(con_movilidad and all(
    (p["rol_a_descansa_en_un_solo_candidato"] == "si" if p["rol_a"] == "movilidad"
     else p["rol_b_descansa_en_un_solo_candidato"] == "si") for p in con_movilidad),
      "las %d combinaciones de movilidad lo dicen en su propia fila" % len(con_movilidad))
check(all(p["contraevidencia_del_rol_a" if p["rol_a"] == "movilidad"
                                       else "contraevidencia_del_rol_b"]
          for p in con_movilidad),
      "y ninguna sale sin la contraevidencia al lado")
msg = aborta(PM.leer_contraevidencia, ELEGIBLES, FILAS,
             contraevidencia_con([{"mecanismo": "movilidad", "fila_que_la_sostiene": "DM-03",
                                   "frase_textual_en_eje_fenotipo": "frase que nadie midio",
                                   "por_que_cuenta_como_contraevidencia": "—",
                                   "fuente_de_la_lectura": "—"}]))
check("no esta textual" in msg,
      "una contraevidencia cuya frase no esta textual en la tabla aborta")
msg = aborta(PM.leer_contraevidencia, ELEGIBLES, FILAS,
             contraevidencia_con([{"mecanismo": "movilidad", "fila_que_la_sostiene": "ZZ-99",
                                   "frase_textual_en_eje_fenotipo": "da igual",
                                   "por_que_cuenta_como_contraevidencia": "—",
                                   "fuente_de_la_lectura": "—"}]))
check("que no esta en la tabla" in msg,
      "y una que cita una fila inexistente tambien")
msg = aborta(PM.leer_contraevidencia, ELEGIBLES, FILAS,
             contraevidencia_con([{"mecanismo": "movilidad"}],
                                 columnas=("mecanismo",)))
check("el esquema de" in msg, "y el esquema cambiado aborta en la lectura")

print("\n§7 ninguna recomendacion: no hay puntaje, puesto ni orden de calidad")
PALABRAS = ("punt", "puesto", "mejor", "recomend", "ranking", "score", "prioridad")
sucias = [c for c in todas[0] for w in PALABRAS if w in c.lower()]
check(not sucias, "ninguna columna de la salida sugiere un orden de calidad (%s)" % sucias)
for x, y in PEDIDOS:
    ps = PM.pares(ELEGIBLES, x, y, SOP, CONTRA, True)
    if ps != sorted(ps, key=lambda p: (p["id_a"], p["id_b"])):
        FALLAS.append("el orden de %s+%s no es alfabetico" % (x, y))
check(all(PM.pares(ELEGIBLES, x, y, SOP, CONTRA, True)
          == sorted(PM.pares(ELEGIBLES, x, y, SOP, CONTRA, True),
                    key=lambda p: (p["id_a"], p["id_b"])) for x, y in PEDIDOS),
      "el orden de las filas es alfabetico por identificador y no significa nada")

print("\n§8 la enumeracion es determinista y no muestrea")
a1 = PM.pares(ELEGIBLES, "reproduccion", "letalidad", SOP, CONTRA, False)
a2 = PM.pares(ELEGIBLES, "reproduccion", "letalidad", SOP, CONTRA, False)
check(a1 == a2 and len(a1) > 0,
      "dos corridas del mismo pedido dan la misma lista (%d asignaciones)" % len(a1))
check(all(p["rol_a"] == "reproduccion" and p["rol_b"] == "letalidad" for p in a1),
      "y el rol de cada lado es el pedido")

print("\n§9 ningun identificador de candidato esta escrito en el codigo que decide")
fuente = Path(PM.__file__).read_text(encoding="utf-8")
arbol = ast.parse(fuente)
docs = set()
for nodo in ast.walk(arbol):
    if isinstance(nodo, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        if ast.get_docstring(nodo, clean=False) is not None:
            docs.add(id(nodo.body[0].value))
literales = [n.value for n in ast.walk(arbol)
             if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs]
PATRON = re.compile(r"\b[A-Z]{2}-\d{2}\b")
con_id = sorted({s for s in literales if PATRON.search(s)})
check(not con_id,
      "el AST del selector no tiene ningun identificador como literal fuera de los "
      "docstrings (%s)" % con_id)
check(PATRON.search("DM-01") is not None and PATRON.search("C5/") is None,
      "el patron de la prueba reconoce un identificador y no se dispara con C5/")

print("\n§10 el puente con O4 no enumera un par que no sea elegible")
import enumerar_quimeras as EQ   # noqa: E402
invertidos = sorted(i for i, f in EXCLUIDOS.items()
                    if f["etiqueta_de_ausencia"] == "fenotipo_invertido")
msg = aborta(EQ.ejes_por_mecanismo, "reproduccion,letalidad",
             ["DM-01=G1", "%s=G2" % invertidos[0]], ["G1", "G2"], False)
check("no es elegible" in msg and "fenotipo_invertido" in msg,
      "un par con un candidato de signo invertido aborta y nombra su etiqueta")
check("peor que no hacer nada" in msg, "y dice por que importa")
msg = aborta(EQ.ejes_por_mecanismo, "reproduccion,movilidad",
             ["DM-02=G1", "DM-01=G2"], ["G1", "G2"], False)
check("no es un par elegible" in msg,
      "una asignacion de roles al reves de la elegible aborta")
check("los roles al reves" in msg, "y dice que el mismo par si es elegible al revés")
msg = aborta(EQ.ejes_por_mecanismo, "reproduccion,movilidad",
             ["DM-01=G1"], ["G1", "G2"], False)
check("exactamente dos" in msg, "con un solo --candidato aborta")
ejes, decl = EQ.ejes_por_mecanismo("reproduccion,movilidad",
                                   ["DM-01=G1", "DM-02=G2"], ["G1", "G2"], False)
check(ejes == {"G1": {"eje": "reproduccion", "fuente": "C5/DM-01"},
               "G2": {"eje": "movilidad", "fuente": "C5/DM-02"}},
      "el par elegible resuelve el eje de cada gen desde la tabla")
check(decl["soporte_por_mecanismo_pedido"]["movilidad"]["descansa_en_un_solo_candidato"],
      "y la declaracion que va al JSON dice que movilidad descansa en una sola fila")

print()
if FALLAS:
    print("FALLAS: %d" % len(FALLAS))
    for f in FALLAS:
        print("  %s" % f)
    sys.exit(1)
print("todo bien")
