"""Verificaciones de `alertas.py` y de la regla de alerta de D48 en `ejes_separados.py`.

Cuatro clases de prueba:

- **Una fila sin los cuatro campos falla la validacion**, que es lo que pide el issue
  #10 textualmente: «una fila sin esos cuatro campos es un error de validacion, no una
  fila con celdas vacias». Se prueba con una fila incompleta a proposito, campo por
  campo, y con las tres formas de estar incompleta sin estar vacia: clave fuera del
  vocabulario, bioensayo fuera del vocabulario y prosa de una palabra.
- **Una fila incompleta no llega al disco**: `escribir()` valida antes de abrir el
  archivo.
- **La anotacion se parte bien**, con cabeceras reales de `work/W5/ref/` —incluida la
  del ensamblado genomico del vector, que no tiene anotacion de gen— y las isoformas del
  mismo gen agrupan en una sola clave.
- **La compuerta esta retirada**: `estado_region()` nunca devuelve un veredicto y
  `barrer_exposicion(regla_veto='alerta')` no veta a nadie; pedirle la forma `cascada`
  —que es la compuerta— levanta `CompuertaRetirada`.

Y un ancla del desarrollo nuevo: `escanear_con_identidad()` devuelve **lo mismo** que
`escanear()`, que es la unica forma de saber que conservar la identidad no cambio
ningun conteo publicado.

    python tools/sifi21_port/test_alertas.py
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import alertas as AL              # noqa: E402
import ejes_separados as E        # noqa: E402
import offtarget_21nt as O        # noqa: E402
import ranking as R               # noqa: E402
import ranking_v2 as V            # noqa: E402

FALLAS, SALTEADAS = [], []
TRABAJO = RAIZ / "work" / "sifi_v2"
REF = RAIZ / "work" / "W5" / "ref"


def check(cond, msg):
    print(("  ok   " if cond else "  FALLA ") + msg)
    if not cond:
        FALLAS.append(msg)


def fila_completa() -> dict:
    return {
        "gen": "BicC_Dm", "region": "264-563",
        "organismo_corto": "H_vitripennis", "organismo_especie": "Homalodisca vitripennis",
        "organismo_rol": "cicadelido no objetivo del panel",
        "exposicion_w": "0.00", "exposicion_w_alternativa": "0.60",
        "exposicion_motivo": "cicadelido no reportado en la Argentina",
        "exposicion_fuente": "PANEL_EJES, tools/sifi21_port/ejes_separados.py",
        "exposicion_decision_abierta": "si",
        "gen_simbolo": "protein bicaudal C homolog 1-A", "gen_locus": "LOC124362408",
        "gen_tipo_molecula": "mRNA", "gen_transcriptos": "XM_046816879.1",
        "gen_anotacion": "PREDICTED: Homalodisca vitripennis protein bicaudal C homolog 1-A",
        "gen_fuente": "work/W5/ref/GCF_021130785.1_UT_GWSS_2.1_rna.fna.gz",
        "evidencia_clave": "ortologo_del_blanco",
        "evidencia_bioensayo": "sin_bioensayo_consultado",
        "evidencia_prosa": "el transcripto impactado es el ortologo del gen que se silencia, "
                           "asi que el escenario es el de silenciar al no objetivo.",
        # las dos columnas de decision son parte del contrato de la tabla: una fila
        # siempre declara su estado, aunque ese estado sea «todavia no lo decidio nadie»
        "decision_usuario": "pendiente",
        "justificacion_usuario": "pendiente: la escribe el usuario, no el motor",
    }


print("1. una fila sin los cuatro campos falla la validacion")
check(AL.validar_fila(fila_completa()) is None, "la fila completa pasa")
for campo in AL.CAMPOS_OBLIGATORIOS:
    for col in AL.COLUMNAS_DE[campo]:
        rota = fila_completa()
        rota[col] = ""                      # vacia a proposito, que es el caso del issue
        try:
            AL.validar_fila(rota)
            check(False, "la fila sin %s/%s deberia fallar y paso" % (campo, col))
        except AL.FilaIncompleta as e:
            check(col in str(e) and campo in str(e),
                  "sin %s/%s falla y el mensaje nombra el campo" % (campo, col))
    faltante = fila_completa()
    for col in AL.COLUMNAS_DE[campo]:
        faltante.pop(col)                   # columna ausente, no vacia
    try:
        AL.validar_fila(faltante)
        check(False, "la fila sin la columna %s deberia fallar" % campo)
    except AL.FilaIncompleta:
        check(True, "la fila con la columna %s ausente tambien falla" % campo)

print("2. las tres formas de estar incompleta sin estar vacia")
for col, valor, que in (("evidencia_clave", "me_parece_que_si", "clave fuera del vocabulario"),
                        ("evidencia_bioensayo", "lo_vi_en_un_paper", "bioensayo fuera del vocabulario"),
                        ("evidencia_prosa", "ortologo", "prosa de una palabra")):
    rota = fila_completa()
    rota[col] = valor
    try:
        AL.validar_fila(rota)
        check(False, "%s deberia fallar y paso" % que)
    except AL.FilaIncompleta:
        check(True, "%s falla" % que)

print("3. una fila incompleta no llega al disco")
with tempfile.TemporaryDirectory() as tmp:
    destino = Path(tmp) / "alertas.tsv"
    rota = fila_completa()
    rota["evidencia_prosa"] = ""
    try:
        AL.escribir([fila_completa(), rota], destino, list(fila_completa()))
        check(False, "escribir() deberia haber abortado")
    except AL.FilaIncompleta:
        check(not destino.exists(), "escribir() aborta y no deja archivo a medio escribir")
    AL.escribir([fila_completa()], destino, list(fila_completa()))
    check(destino.exists() and len(destino.read_text().splitlines()) == 2,
          "con la fila completa escribe cabecera y una fila")

print("4. la anotacion de la cabecera se parte bien")
casos = [
    ("PREDICTED: Homalodisca vitripennis protein bicaudal C homolog 1-A (LOC124362408), mRNA",
     "Homalodisca vitripennis protein bicaudal C homolog 1-A", "LOC124362408", "mRNA"),
    ("PREDICTED: Zea mays serine esterase family protein (LOC100281777), transcript variant X1, misc_RNA",
     "Zea mays serine esterase family protein", "LOC100281777", "misc_RNA"),
    ("Homo sapiens solute carrier family 24 member 4 (SLC24A4), transcript variant 4, mRNA",
     "Homo sapiens solute carrier family 24 member 4", "SLC24A4", "mRNA"),
    # sin parentesis no hay gen anotado: el campo queda vacio y no se inventa
    ("Dalbulus maidis genome assembly, chromosome: 6", "", "",
     "Dalbulus maidis genome assembly, chromosome: 6"),
]
for cab, simbolo, locus, molecula in casos:
    d = AL.partir_anotacion(cab)
    check((d["simbolo"], d["locus"], d["molecula"]) == (simbolo, locus, molecula),
          "cabecera %r -> %r" % (cab[:46], (d["simbolo"], d["locus"], d["molecula"])))

isoformas = ["NM_153646.4", "NM_153647.4", "XM_011536436.3"]
claves = {AL.clave_de_gen("humano",
                          "Homo sapiens solute carrier family 24 member 4 (SLC24A4), "
                          "transcript variant 4, mRNA", t) for t in isoformas}
check(len(claves) == 1, "tres isoformas de SLC24A4 agrupan en una sola clave de gen")
check(AL.clasificar_evidencia(
    "BicC_Dm", "PREDICTED: Homalodisca vitripennis protein bicaudal C homolog 1-A "
               "(LOC124362408), mRNA") == "ortologo_del_blanco",
    "bicaudal C de H. vitripennis se clasifica como ortologo del blanco")
check(AL.clasificar_evidencia(
    "BicC_Dm", "PREDICTED: Zea mays serine esterase family protein (LOC100281777), mRNA")
    == "gen_no_relacionado", "la esterasa de maiz no es ortologo del blanco")
check(AL.clasificar_evidencia("MP_MRFV", "Dalbulus maidis genome assembly, chromosome: 6")
      == "sin_anotacion_de_gen", "el ensamblado genomico queda sin anotacion de gen")

print("5. la compuerta esta retirada (D48)")
if not (TRABAJO / "salida_k21").exists():
    SALTEADAS.append("pruebas con datos: falta work/sifi_v2/")
    print("  SALTEADA  falta work/sifi_v2/ (no se versiona)")
else:
    V.con_panel(sin_humano=False)
    genes = V.cargar(TRABAJO, 21, ["BicC_Dm", "ATPaseD_Dm"])
    cand = {"gen": "BicC_Dm", "region": (264, 563), "estrategia": "insecto"}
    excl = R.excluidas_de(cand, "off")
    est = E.estado_region(genes["BicC_Dm"], 264, 563, None, excl)
    check(est["estado"] == "con alertas, pendiente de justificacion" and est["decide"] == "el usuario",
          "264-563 queda pendiente de justificacion, no descartada")
    check(est["ventanas_perfecto_21"] == 22, "y reporta las 22 ventanas de 21/21 de M7 §5")
    check(est["vetada_regla_anterior"] is True, "la regla anterior la vetaba, y se informa")
    limpia = E.estado_region(genes["BicC_Dm"], 922, 1221, None, excl)
    check(limpia["ventanas_perfecto_21"] == 0 and limpia["ventanas_perfecto_ge19"] == 3,
          "922-1221 da 0 y 3, los dos umbrales de D28 anidados")
    estados = {e["estado"] for e in (est, limpia)}
    check(not (estados & {"descartada", "aceptada"}),
          "estado_region() no produce ningun veredicto")
    import numpy as np
    cands = [cand, {"gen": "ATPaseD_Dm", "region": (137, 436), "estrategia": "insecto"}]
    w = E.vector_exposicion()
    r = E.barrer_exposicion(cands, genes, w, "geometrica", False, 50,
                            np.random.default_rng(7), "absoluta", regla_veto="alerta")
    check(r["vetadas"] == [] and set(r["alertadas"]) == {"BicC_Dm", "ATPaseD_Dm"},
          "con regla_veto='alerta' no veta a nadie y devuelve el inventario")
    try:
        E.barrer_exposicion(cands, genes, w, "cascada", False, 10,
                            np.random.default_rng(7), "absoluta", regla_veto="alerta")
        check(False, "la cascada bajo la regla de alerta deberia levantar CompuertaRetirada")
    except E.CompuertaRetirada:
        check(True, "pedir la cascada bajo la regla de alerta levanta CompuertaRetirada")

print("6. ancla: escanear_con_identidad() devuelve lo mismo que escanear()")
consulta = TRABAJO / "fasta" / "ATPaseD_Dm_full.fasta"
db = REF / "GCF_021130785.1_UT_GWSS_2.1_rna.fna.gz"
if not (consulta.exists() and db.exists()):
    SALTEADAS.append("ancla de identidad: faltan insumos locales")
    print("  SALTEADA  faltan insumos locales")
else:
    aut, sirnas = O.construir([consulta], con_mm1=False)
    a = O.escanear(aut, sirnas, db)
    b, anot = O.escanear_con_identidad(aut, sirnas, db)
    check(a == b, "los dos escaneos dan el mismo dict de referencias por ventana")
    check(anot and all(isinstance(v, str) and v for v in anot.values()),
          "y la version con identidad ademas trae la anotacion de %d accesiones" % len(anot))

print("7. la compuerta: «pendiente» no pasa en silencio")

def fila_alerta(**kw):
    f = fila_completa()
    f.update({"ventanas_perfecto_21": "22", "ventanas_perfecto_ge19": "30"})
    f.update(kw)
    return f

# una region sin alertas pasa, y no es una laguna: no hay nada que justificar
sin = [fila_alerta(gen="CP_MRFV", region="99-298",
                   ventanas_perfecto_21="0", ventanas_perfecto_ge19="0")]
est = AL.exigir_decidida(sin, "CP_MRFV", "99-298")
check(est["estado"] == "sin alertas en este umbral" and est["alertas"] == 0,
      "una region sin alertas pasa la compuerta")

# una region con una alerta pendiente NO pasa
pend = [fila_alerta()]
try:
    AL.exigir_decidida(pend, "BicC_Dm", "264-563")
    check(False, "una alerta pendiente deberia levantar AlertaSinDecidir")
except AL.AlertaSinDecidir as e:
    check("264-563" in str(e) and "H_vitripennis" in str(e),
          "una alerta pendiente levanta AlertaSinDecidir y nombra la region y el organismo")

# decidir reescribiendo una palabra NO alcanza
try:
    AL.exigir_decidida([fila_alerta(decision_usuario="aceptada")], "BicC_Dm", "264-563")
    check(False, "aceptar sin justificar deberia fallar")
except AL.FilaIncompleta as e:
    check("relleno" in str(e), "aceptar dejando el texto de relleno falla")

# una justificacion generica, que no cita la fila, tampoco
generica = fila_alerta(decision_usuario="aceptada",
                       justificacion_usuario="Lo discutimos en la reunion y nos parece "
                                             "que el riesgo es aceptable para esta region.")
try:
    AL.exigir_decidida([generica], "BicC_Dm", "264-563")
    check(False, "una justificacion que no cita la fila deberia fallar")
except AL.FilaIncompleta as e:
    check("no cita la fila" in str(e), "una justificacion generica que no cita la fila falla")

# citando la accesion, pasa
buena = fila_alerta(decision_usuario="aceptada",
                    justificacion_usuario="Se acepta: el acierto es contra XM_046816879.1, el "
                                          "ortologo de bicaudal C de un cicadelido ausente en la "
                                          "Argentina, asi que la exposicion es la que decide.")
est = AL.exigir_decidida([buena], "BicC_Dm", "264-563")
check(est["estado"] == "decidida: aceptada con justificacion" and est["pendientes"] == 0,
      "con la justificacion que cita la accesion, la region pasa")

# bloqueante tambien es decidir: pasa la compuerta y el estado lo dice
bloq = fila_alerta(decision_usuario="bloqueante",
                   justificacion_usuario="Se bloquea: XM_046816879.1 es el ortologo exacto del "
                                         "gen blanco y no aceptamos silenciar al pariente.")
est = AL.exigir_decidida([bloq], "BicC_Dm", "264-563")
check(est["estado"] == "decidida: bloqueante" and est["bloqueantes"] == 1,
      "una fila bloqueante pasa la compuerta y el estado dice que esta bloqueada")

# el vocabulario de decision es cerrado
try:
    AL.validar_decision(fila_alerta(decision_usuario="mas o menos"))
    check(False, "una decision fuera del vocabulario deberia fallar")
except AL.FilaIncompleta:
    check(True, "una decision fuera del vocabulario cerrado falla")

# el umbral es un parametro: una fila con 0 de 21/21 y 3 de >=19 obliga solo en el laxo
laxa = [fila_alerta(gen="BicC_Dm", region="922-1221", organismo_corto="humano",
                    ventanas_perfecto_21="0", ventanas_perfecto_ge19="3")]
check(AL.exigir_decidida(laxa, "BicC_Dm", "922-1221", "perfecto_21")["alertas"] == 0,
      "con umbral perfecto_21 una alerta de solo >=19 nt no obliga")
try:
    AL.exigir_decidida(laxa, "BicC_Dm", "922-1221", "perfecto_ge19")
    check(False, "con umbral perfecto_ge19 esa misma fila deberia obligar")
except AL.AlertaSinDecidir:
    check(True, "con umbral perfecto_ge19 esa misma fila obliga a justificar")

# leer() valida al abrir: una tabla con una decision invalida no se puede leer
import tempfile as _tf
with _tf.TemporaryDirectory() as tmp:
    ruta = Path(tmp) / "alertas.tsv"
    AL.escribir([fila_alerta()], ruta, list(fila_alerta()))
    check(len(AL.leer(ruta)) == 1, "leer() abre una tabla con filas pendientes")
    texto = ruta.read_text(encoding="utf-8").replace("\tpendiente\t", "\taceptada\t")
    ruta.write_text(texto, encoding="utf-8")
    try:
        AL.leer(ruta)
        check(False, "leer() deberia rechazar una tabla aceptada sin justificar")
    except AL.FilaIncompleta:
        check(True, "leer() rechaza una tabla donde se acepto sin justificar")


print()
if SALTEADAS:
    print("SALTEADAS: %s" % "; ".join(SALTEADAS))
if FALLAS:
    print("FALLAS: %d" % len(FALLAS))
    sys.exit(1)
print("todo bien")
