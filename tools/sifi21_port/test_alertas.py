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
- **El port no recomienda una region con una alerta sin decidir, ni una region que no se
  tamizo** (§9, D69 y D72): `ranking.region_recomendada()` es el unico lugar donde el
  primer puesto de `alternativas()` se vuelve recomendacion, y llama a
  `exigir_decidida()`. Se prueba que falla con la fila en «pendiente», que pasa firmada,
  que el umbral de D28 es un parametro, que una tabla ausente falla cerrada y que un
  inventario ausente tambien. El par 6/7 de la seccion es el nucleo de D72: la **misma**
  region sin ninguna fila de alerta se frena o pasa segun este o no en el inventario, que
  es la distincion que `alertas.tsv` por si solo no puede hacer. La prueba estructural
  sigue ahi: ninguna de las tres rutas del port rearma la region a mano.

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
import ranking as R               # noqa: E402
import ranking_v2 as V            # noqa: E402

# `offtarget_21nt` es la unica pieza de este archivo que necesita `pyahocorasick`, y lo
# necesita solo el ancla de identidad de §6. Importarlo arriba y sin red hacia que una
# maquina sin esa dependencia no pudiera correr **ninguna** de las pruebas, incluidas
# las de la compuerta y las firmas, que no dependen de ningun binario ni de ningun dato.
# Se importa aparte y su ausencia saltea §6 con el mismo mecanismo que los insumos que
# no estan en disco: una prueba salteada se declara, no se esconde.
try:
    import offtarget_21nt as O    # noqa: E402
except ImportError as _e:
    O, _FALTA_O = None, str(_e)

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
if O is None:
    SALTEADAS.append("ancla de identidad: %s (la necesita offtarget_21nt, no estas pruebas)"
                     % _FALTA_O)
    print("  SALTEADA  %s" % _FALTA_O)
elif not (consulta.exists() and db.exists()):
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

# Desde D72 la compuerta pide el inventario de regiones tamizadas, por nombre y sin
# default, asi que toda llamada tiene que declarar contra que inventario exige presencia.
# Este es el de las pruebas sinteticas, y `CP_MRFV` 99-298 esta adentro a proposito: es
# una region que **si** se tamizo y no tiene ningun acierto, que es el caso que
# `alertas.tsv` no puede distinguir de «nunca se tamizo» y por el que hace falta el
# inventario aparte.
INV = {("CP_MRFV", "99-298"), ("BicC_Dm", "264-563"), ("BicC_Dm", "922-1221"),
       ("ATPaseD_Dm", "72-371")}

# una region tamizada y sin alertas pasa, y no es una laguna: no hay nada que justificar
sin = [fila_alerta(gen="CP_MRFV", region="99-298",
                   ventanas_perfecto_21="0", ventanas_perfecto_ge19="0")]
est = AL.exigir_decidida(sin, "CP_MRFV", "99-298", inventario=INV)
check(est["estado"] == "sin alertas en este umbral" and est["alertas"] == 0,
      "una region sin alertas pasa la compuerta")

# una region con una alerta pendiente NO pasa
pend = [fila_alerta()]
try:
    AL.exigir_decidida(pend, "BicC_Dm", "264-563", inventario=INV)
    check(False, "una alerta pendiente deberia levantar AlertaSinDecidir")
except AL.AlertaSinDecidir as e:
    check("264-563" in str(e) and "H_vitripennis" in str(e),
          "una alerta pendiente levanta AlertaSinDecidir y nombra la region y el organismo")

# decidir reescribiendo una palabra NO alcanza
try:
    AL.exigir_decidida([fila_alerta(decision_usuario="aceptada")], "BicC_Dm",
                       "264-563", inventario=INV)
    check(False, "aceptar sin justificar deberia fallar")
except AL.FilaIncompleta as e:
    check("relleno" in str(e), "aceptar dejando el texto de relleno falla")

# una justificacion generica, que no cita la fila, tampoco
generica = fila_alerta(decision_usuario="aceptada",
                       justificacion_usuario="Lo discutimos en la reunion y nos parece "
                                             "que el riesgo es aceptable para esta region.")
try:
    AL.exigir_decidida([generica], "BicC_Dm", "264-563", inventario=INV)
    check(False, "una justificacion que no cita la fila deberia fallar")
except AL.FilaIncompleta as e:
    check("no cita la fila" in str(e), "una justificacion generica que no cita la fila falla")

# citando la accesion, pasa
buena = fila_alerta(decision_usuario="aceptada",
                    justificacion_usuario="Se acepta: el acierto es contra XM_046816879.1, el "
                                          "ortologo de bicaudal C de un cicadelido ausente en la "
                                          "Argentina, asi que la exposicion es la que decide.")
est = AL.exigir_decidida([buena], "BicC_Dm", "264-563", inventario=INV)
check(est["estado"] == "decidida: aceptada con justificacion" and est["pendientes"] == 0,
      "con la justificacion que cita la accesion, la region pasa")

# bloqueante tambien es decidir: pasa la compuerta y el estado lo dice
bloq = fila_alerta(decision_usuario="bloqueante",
                   justificacion_usuario="Se bloquea: XM_046816879.1 es el ortologo exacto del "
                                         "gen blanco y no aceptamos silenciar al pariente.")
est = AL.exigir_decidida([bloq], "BicC_Dm", "264-563", inventario=INV)
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
check(AL.exigir_decidida(laxa, "BicC_Dm", "922-1221", "perfecto_21",
                         inventario=INV)["alertas"] == 0,
      "con umbral perfecto_21 una alerta de solo >=19 nt no obliga")
try:
    AL.exigir_decidida(laxa, "BicC_Dm", "922-1221", "perfecto_ge19", inventario=INV)
    check(False, "con umbral perfecto_ge19 esa misma fila deberia obligar")
except AL.AlertaSinDecidir:
    check(True, "con umbral perfecto_ge19 esa misma fila obliga a justificar")

# ---------------------------------------------------------------- presencia (D72)
# Lo que sigue es el agujero que D69 dejo declarado y D70 decidio cerrar: la compuerta
# no podia distinguir «se tamizo y no hay alertas» de «no se tamizo», porque los dos
# casos se ven igual desde `alertas.tsv` —cero filas—. Las dos primeras pruebas son el
# par que importa: la misma consulta, con cero filas en los dos casos, y dos resultados
# distintos segun el inventario.

# 1. region tamizada sin aciertos: pasa, y el estado dice por que
est = AL.exigir_decidida(sin, "CP_MRFV", "99-298", inventario=INV)
check(est["estado"] == "sin alertas en este umbral",
      "una region del inventario sin aciertos pasa: se la miro y no hay nada que justificar")

# 2. region ausente del inventario: NO pasa, con las mismas cero filas
try:
    AL.exigir_decidida(sin, "eth_Dm", "193-392", inventario=INV)
    check(False, "una region que no esta en el inventario deberia levantar RegionNoTamizada")
except AL.RegionNoTamizada as e:
    check("193-392" in str(e) and "no se tamizo" in str(e),
          "una region ausente del inventario levanta RegionNoTamizada y nombra la region")

# 3. y no es un caso de borde del umbral: falla en los dos de D28, porque no hay medicion
for umbral in ("perfecto_21", "perfecto_ge19"):
    try:
        AL.exigir_decidida(sin, "eth_Dm", "193-392", umbral, inventario=INV)
        check(False, "deberia fallar en %s tambien" % umbral)
    except AL.RegionNoTamizada:
        pass
check(True, "la presencia se exige en los dos umbrales de D28: no hay medicion que umbralar")

# 4. las dos formas de no pasar son distintas y las dos son `CompuertaCerrada`
check(issubclass(AL.RegionNoTamizada, AL.CompuertaCerrada)
      and issubclass(AL.AlertaSinDecidir, AL.CompuertaCerrada)
      and not issubclass(AL.RegionNoTamizada, AL.AlertaSinDecidir),
      "RegionNoTamizada y AlertaSinDecidir son hermanas bajo CompuertaCerrada, no la misma")

# 5. olvidarse el inventario es un TypeError, no un pase. Es la razon de que el parametro
#    sea obligatorio y por nombre: una compuerta con default se desactiva olvidandola.
try:
    AL.exigir_decidida(sin, "CP_MRFV", "99-298")
    check(False, "llamar la compuerta sin inventario deberia ser un TypeError")
except TypeError:
    check(True, "la compuerta no se puede llamar sin declarar el inventario")

# 6. un inventario que no esta en disco falla cerrado, igual que una tabla ausente en D69
try:
    AL.leer_inventario(Path("/no/existe/estado_regiones.tsv"))
    check(False, "un inventario ausente deberia levantar FileNotFoundError")
except FileNotFoundError as e:
    check("no se tamizo" in str(e),
          "un inventario ausente falla cerrado: no es un inventario vacio")

# 7. el inventario real del proyecto, leido de disco
ESTADOS = RAIZ / "research/ola4/M6_alertas/resultados/estado_regiones.tsv"
if ESTADOS.exists():
    real = AL.leer_inventario(ESTADOS)
    check(("eth_Dm", "193-392") in real and ("CP_MRFV", "77-276") in real,
          "las regiones de k=22 estan en el inventario real desde R7 (%d regiones)" % len(real))
else:
    SALTEADAS.append("§7 el inventario real no esta en disco")

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



# ------------------------------------------------------------------------------- §8
# La persistencia de las firmas. Lo que se prueba acá no es que el volcado funcione
# —eso es trivial— sino las tres formas de perder una firma sin que nadie se entere,
# que es el modo de fallar que hacía que el mecanismo de D48 se desarmara solo.

def firma(fila, decision="aceptada", just=None, **kw):
    """La fila de firma que le corresponde a una fila de alerta."""
    h21, h19 = AL.huella_de(fila)
    f = {"gen": fila["gen"], "region": fila["region"],
         "organismo_corto": fila["organismo_corto"], "gen_locus": fila["gen_locus"],
         "huella_21": h21, "huella_ge19": h19, "firmado_por": "prueba",
         "fecha": "2026-10-26", "decision_usuario": decision,
         "justificacion_usuario": just or ("Se acepta: el acierto es contra XM_046816879.1 y "
                                           "el argumento va escrito acá.")}
    f.update(kw)
    return f

base = fila_alerta()

# 1. el caso normal: la firma se vuelca y la fila queda decidida
filas = [fila_alerta()]
inf = AL.aplicar_decisiones(filas, {AL.clave_de(base): firma(base)})
check(inf["firmadas"] == 1 and inf["pendientes"] == 0
      and filas[0]["decision_usuario"] == "aceptada",
      "una firma se vuelca sobre su fila y la deja decidida")

# 2. una fila sin firma vuelve a «pendiente», que es el estado de fábrica y es legítimo
filas = [fila_alerta(decision_usuario="aceptada", justificacion_usuario="texto viejo")]
inf = AL.aplicar_decisiones(filas, {})
check(filas[0]["decision_usuario"] == AL.MARCA_PENDIENTE and inf["pendientes"] == 1,
      "una fila sin firma queda en pendiente aunque la tabla trajera otra cosa")

# 3. la huella vencida: la fila pasó de 22 a 5 coincidencias perfectas desde que se firmó
movida = fila_alerta(ventanas_perfecto_21="5")
try:
    AL.aplicar_decisiones([movida], {AL.clave_de(base): firma(base)})
    check(False, "una firma sobre conteos que cambiaron debería levantar FirmaVencida")
except AL.FirmaVencida as e:
    check("volver a firmarla" in str(e),
          "una fila cuyos conteos cambiaron no hereda la firma: levanta FirmaVencida")

# 4. la firma huérfana: la tabla ya no produce esa fila
try:
    AL.aplicar_decisiones([], {AL.clave_de(base): firma(base)})
    check(False, "una firma sin fila debería levantar FirmaHuerfana")
except AL.FirmaHuerfana as e:
    check("264-563" in str(e), "una firma que no corresponde a ninguna fila levanta FirmaHuerfana")

# 5. la clave incluye el gen impactado. Es el caso real de `ATPaseD_Dm` 72-371, donde hay
#    DOS filas humanas: con una clave de región x organismo, firmar una firmaría las dos.
a = fila_alerta(gen="ATPaseD_Dm", region="72-371", organismo_corto="humano",
                gen_locus="LOC107984331", ventanas_perfecto_21="0",
                ventanas_perfecto_ge19="4")
b = fila_alerta(gen="ATPaseD_Dm", region="72-371", organismo_corto="humano",
                gen_locus="PDE1C", ventanas_perfecto_21="0", ventanas_perfecto_ge19="3")
check(AL.clave_de(a) != AL.clave_de(b),
      "dos genes impactados distintos en la misma región y organismo son dos claves")
filas = [dict(a), dict(b)]
inf = AL.aplicar_decisiones(filas, {AL.clave_de(a): firma(a)})
check(inf["firmadas"] == 1 and filas[1]["decision_usuario"] == AL.MARCA_PENDIENTE,
      "firmar una de las dos filas humanas no firma la otra")

# 6. una firma mal escrita aborta en vez de llegar al disco
try:
    AL.aplicar_decisiones([fila_alerta()],
                          {AL.clave_de(base): firma(base, just=(
                              "Se acepta porque el riesgo nos parece bajo y la region es buena. "
                              "Es prosa suficiente en largo y no nombra ni el LOC ni la "
                              "accesion, que es justo lo que D48 pide."))})
    check(False, "una firma que no cita la fila debería fallar al aplicarse")
except AL.FilaIncompleta as e:
    check("no cita la fila" in str(e), "una firma que no cita la fila aborta al aplicarse")

# 7. dos firmas para la misma fila es un error del archivo, no la última gana
with tempfile.TemporaryDirectory() as tmp:
    ruta = Path(tmp) / "decisiones.tsv"
    import csv as _csv
    with ruta.open("w", encoding="utf-8", newline="") as fh:
        w = _csv.DictWriter(fh, fieldnames=list(AL.COLUMNAS_DECISION), delimiter="\t")
        w.writeheader()
        w.writerow(firma(base))
        w.writerow(firma(base, decision="bloqueante"))
    try:
        AL.leer_decisiones(ruta)
        check(False, "dos firmas para la misma fila deberían fallar")
    except AL.FilaIncompleta as e:
        check("dos firmas" in str(e), "dos firmas para la misma fila es un error del archivo")

# 8. un archivo que no existe es el estado inicial, no un error
check(AL.leer_decisiones(Path("/no/existe/decisiones.tsv")) == {},
      "sin archivo de firmas, las filas salen en pendiente y no hay error")

# 9. el archivo real del proyecto: las 17 firmas de D68 se aplican sobre la tabla real.
#    Desde R7 la tabla tiene seis filas mas —las de las regiones de k=22, que entraron al
#    inventario con D70— y esas seis estan en «pendiente»: las firmas **no** se
#    autogeneran, y que las diecisiete sigan aplicando sobre sus filas y ninguna se haya
#    movido a otra fila es justamente lo que esta seccion verifica. Si agregar regiones
#    hubiera corrido una fila debajo de una firma, `aplicar_decisiones()` levantaria
#    `FirmaVencida` o `FirmaHuerfana` antes de llegar a este `check`.
TABLA = RAIZ / "research/ola4/M6_alertas/resultados/alertas.tsv"
FIRMAS = RAIZ / "research/ola4/M6_alertas/decisiones.tsv"
K22 = (("MP_MRFV", "162-361"), ("CP_MRFV", "77-276"), ("BicC_Dm", "2119-2418"),
       ("ATPaseD_Dm", "71-370"), ("eth_Dm", "193-392"), ("bursA_Dm", "44-243"))
if TABLA.exists() and FIRMAS.exists():
    import csv as _csv2
    with TABLA.open(encoding="utf-8") as fh:
        reales = list(_csv2.DictReader(fh, delimiter="\t"))
    inf = AL.aplicar_decisiones(reales, AL.leer_decisiones(FIRMAS))
    check(inf["firmadas"] == len(AL.leer_decisiones(FIRMAS)) == 18,
          "las 18 firmas se aplican, cada una sobre su fila (%d filas en la tabla)"
          % len(reales))
    sin_firma = {(g, r) for g, r, _o, _l in inf["sin_firma"]}
    # Cuatro de las seis regiones de k=22, no seis: `CP_MRFV` 77-276 y `bursA_Dm` 44-243
    # **no tienen ninguna fila** en la tabla, porque se tamizaron y no dieron ningun
    # acierto. Que esas dos no aparezcan aca es exactamente el hecho por el que D72 hizo
    # falta: desde `alertas.tsv` son indistinguibles de una region nunca tamizada, y la
    # unica forma de saber que si se miraron es que esten en el inventario.
    # Cinco regiones pendientes: tres de k=22; `BicC_Dm` 2123-2422, que es la que la
    # compuerta de D72 encontro al regenerar C7 —sale del bloque `efecto_humano`, la
    # corrida con la referencia humana fuera del panel (D75)—; y `eth_Dm` 194-393, que
    # entro con la segunda vuelta de la compuerta del issue #37, al correr los ocho
    # generadores de punta a punta con `work/` en disco. Sale de `sensibilidad_reparto.py`
    # y solo en rho = 0,00 (el reparto de D47).
    #
    # **La quinta no es como las otras cuatro, y esa es la mitad que importa aca.** Las
    # cuatro primeras no tienen ninguna alerta de 21/21, asi que no frenan en el umbral
    # vigente: estan pendientes y pasan. `eth_Dm` 194-393 **si** tiene una, contra
    # *H. vitripennis* en la posicion 347 —la misma ventana que ya tenia 193-392, vista
    # desde una region corrida un nucleotido—, asi que es la unica de las cinco que frena
    # en `perfecto_21`. Por eso las dos afirmaciones van separadas: el conjunto de
    # pendientes y «ninguna trae 21/21» dejaron de ser la misma cosa.
    # La sexta es `VATPaseB_Dm` 517-816, que entro con `D78` (issue #37): la region
    # candidata de `O3`, el unico gen del inventario que **no** tiene ficha de ranking.
    # Sus cuatro filas —maiz, *H. axyridis*, *H. vitripennis* y humano— quedan en
    # «pendiente» porque la firma la escribe una persona, y ninguna trae 21/21.
    # La septima es la juntura de `Q_VATPaseB_Dm__BicC_Dm`, que entro con `D78` por la
    # clave `(quimera <nombre>, "juntura")`. Sus tres bloques fabricados son de 19 nt, asi
    # que no trae 21/21 y frena solo en el umbral laxo.
    check(sin_firma == {("MP_MRFV", "162-361"), ("BicC_Dm", "2119-2418"),
                        ("ATPaseD_Dm", "71-370"), ("BicC_Dm", "2123-2422"),
                        ("eth_Dm", "194-393"), ("VATPaseB_Dm", "517-816"),
                        ("quimera Q_VATPaseB_Dm__BicC_Dm", "juntura")},
          "las siete regiones con filas pendientes son las esperadas")

    # `D78`, las tres mitades que la decision pide y que no son la misma. La que importa
    # es la segunda: en `alertas.tsv` una quimera tamizada sin aciertos y una que nadie
    # tamizo tienen las mismas **cero** filas, y lo unico que las separa es el inventario.
    inv_j = AL.leer_inventario(RAIZ / "research/ola4/M6_alertas/resultados/estado_regiones.tsv")
    for q, umbral, pasa in (("Q_BicC_Dm__VATPaseB_Dm", "perfecto_ge19", True),
                            ("Q_VATPaseB_Dm__BicC_Dm", "perfecto_21", True),
                            ("Q_VATPaseB_Dm__BicC_Dm", "perfecto_ge19", False)):
        try:
            AL.exigir_decidida(reales, "quimera %s" % q, "juntura", umbral,
                               inventario=inv_j)
            ok = True
        except AL.CompuertaCerrada:
            ok = False
        check(ok is pasa, "la juntura de %s en %s: %s"
              % (q, umbral, "pasa" if pasa else "frena sin firma"))
    try:
        AL.exigir_decidida(reales, "quimera Q_que_nadie_tamizo__X", "juntura",
                           inventario=inv_j)
        ok = False
    except AL.RegionNoTamizada:
        ok = True
    check(ok, "una quimera cuyo empalme nadie tamizo levanta RegionNoTamizada (D78)")
    con_21 = {(g, r) for g, r in sin_firma
              if any(int(f["ventanas_perfecto_21"] or 0) > 0 for f in reales
                     if (f["gen"], f["region"]) == (g, r))}
    check(con_21 == {("eth_Dm", "194-393")},
          "y la unica pendiente con coincidencia perfecta de 21 nt es eth_Dm 194-393")
    inv_k22 = AL.leer_inventario(RAIZ / "research/ola4/M6_alertas/resultados/estado_regiones.tsv")
    check(all(not AL.filas_de_region(reales, g, r) and (g, r) in inv_k22
              for g, r in (("CP_MRFV", "77-276"), ("bursA_Dm", "44-243"))),
          "las otras dos se tamizaron sin aciertos: cero filas y si en el inventario")
    inv_real = AL.leer_inventario(RAIZ / "research/ola4/M6_alertas/resultados/estado_regiones.tsv")
    for g, r in (("MP_MRFV", "72-271"), ("BicC_Dm", "922-1221"), ("ATPaseD_Dm", "72-371"),
                 ("eth_Dm", "114-313")):
        AL.exigir_decidida(reales, g, r, "perfecto_ge19", inventario=inv_real)
    check(True, "las regiones vigentes con alerta pasan la compuerta en el umbral laxo de D28")
    tres = [AL.estado_decision(reales, g, r)["estado"]
            for g, r in (("BicC_Dm", "264-563"), ("ATPaseD_Dm", "151-450"),
                         ("ATPaseD_Dm", "137-436"))]
    check(tres == ["decidida: bloqueante"] * 3,
          "las tres regiones de D68 con coincidencia perfecta de 21 nt quedan bloqueantes")
    # Y la cuarta, que es el hallazgo de R7: `eth_Dm` 193-392 —una de las seis que el
    # ranking recomienda a k=22— tiene una coincidencia perfecta de 21 nt contra
    # *Homalodisca vitripennis*, y el equipo la firmo **bloqueante con condicion**, por
    # la misma forma que D68 uso para ATPaseD_Dm 137-436 (ver D73). La prueba fija las dos
    # mitades que importan y que no son lo mismo: la region **pasa** la compuerta, porque
    # bloquear es decidir, y su estado dice que esta bloqueada, o sea que el que llama
    # tiene que descartarla. Un `check` de «pasa» a secas se leeria como «se puede usar».
    inv_real = AL.leer_inventario(RAIZ / "research/ola4/M6_alertas/resultados/estado_regiones.tsv")
    est_eth = AL.exigir_decidida(reales, "eth_Dm", "193-392", inventario=inv_real)
    check(est_eth["estado"] == "decidida: bloqueante" and est_eth["bloqueantes"] == 1
          and est_eth["pendientes"] == 0,
          "eth_Dm 193-392 pasa la compuerta y queda bloqueante: pasar no es poder usarse")
    # Las filas con 21/21 son cinco desde el issue #37, y **cuatro de las cinco** estan
    # bloqueantes. La quinta, `eth_Dm` 194-393, esta en «pendiente» a proposito: la firma
    # la escribe una persona y el motor no se la pone. Las dos mitades van separadas
    # porque el ancla vieja las tenia pegadas —«las que tienen 21/21» y «las bloqueantes»
    # eran el mismo conjunto— y eso ya no se sostiene: el dia que alguien firme 194-393
    # vuelven a coincidir, y hasta entonces lo que el ancla fija es que la unica con 21/21
    # sin firmar es esa.
    con_21 = {(f["gen"], f["region"]) for f in reales
              if int(f["ventanas_perfecto_21"] or 0) > 0}
    check(con_21 == {("BicC_Dm", "264-563"), ("ATPaseD_Dm", "151-450"),
                     ("ATPaseD_Dm", "137-436"), ("eth_Dm", "193-392"),
                     ("eth_Dm", "194-393")},
          "las cinco filas con coincidencia perfecta de 21 nt son las esperadas")
    check(all(AL.estado_decision(reales, g, r)["estado"] == "decidida: bloqueante"
              for g, r in con_21 - {("eth_Dm", "194-393")})
          and AL.estado_decision(reales, "eth_Dm", "194-393")["pendientes"] == 1,
          "cuatro de las cinco estan bloqueantes y eth_Dm 194-393 sigue en pendiente")
else:
    SALTEADAS.append("§8.9 la tabla real o el archivo de firmas no estan en disco")


# ------------------------------------------------------------------------------- §9
print()
print("9. el port no recomienda una region con una alerta en «pendiente» (D69)")

# El `alternativas()` de verdad necesita `work/`, que no se versiona. Lo que la
# compuerta recibe de el es una sola cosa —el primer puesto de `mejores`— y eso se
# construye a mano, que es lo que hace la prueba independiente del dato.
ALT = {"mejores": [{"region": "264-563", "puntaje": 1.0}]}
COLS_PRUEBA = list(fila_completa().keys()) + ["ventanas_perfecto_21", "ventanas_perfecto_ge19"]


def tabla_con(filas, destino: Path, inventario=(("BicC_Dm", "264-563"),)) -> Path:
    """La tabla de prueba y, al lado, su inventario: desde D72 la compuerta pide los dos.

    El inventario va al lado y no como parametro aparte porque asi esta en el proyecto:
    `estado_regiones.tsv` es la otra salida del mismo generador, y `ranking.py` lo busca
    junto a la tabla. Una tabla de prueba sin su inventario al lado es media entrada, y
    la prueba 5 de abajo verifica que eso falla cerrado.
    """
    AL.escribir(filas, destino, COLS_PRUEBA)
    with (destino.parent / R.NOMBRE_INVENTARIO).open("w", encoding="utf-8", newline="") as fh:
        fh.write("gen\tregion\n")
        for gen, reg in inventario:
            fh.write("%s\t%s\n" % (gen, reg))
    R._ALERTAS_LEIDAS.clear()     # el cache es por ruta, y la ruta se reusa
    return destino


with tempfile.TemporaryDirectory() as tmp:
    ruta = Path(tmp) / "alertas.tsv"

    # 1. una fila pendiente frena la recomendacion, y no devuelve region
    tabla_con([fila_alerta()], ruta)
    try:
        R.region_recomendada(ALT, "BicC_Dm", tabla=ruta)
        check(False, "con una alerta pendiente no deberia salir ninguna region")
    except AL.AlertaSinDecidir as e:
        check("264-563" in str(e),
              "region_recomendada() levanta AlertaSinDecidir con la fila en pendiente")

    # 2. la misma fila firmada devuelve la region, como par de enteros
    tabla_con([fila_alerta(
        decision_usuario="aceptada",
        justificacion_usuario="Se acepta: el acierto es contra XM_046816879.1, el ortologo "
                              "de bicaudal C de un cicadelido ausente en la Argentina.")], ruta)
    check(R.region_recomendada(ALT, "BicC_Dm", tabla=ruta) == (264, 563),
          "con la fila firmada, region_recomendada() devuelve la region")

    # 3. el umbral es un parametro, y los dos de D28 no dan lo mismo: una fila que solo
    #    tiene bloques de >=19 nt no obliga con D48 literal y si obliga con el laxo
    tabla_con([fila_alerta(ventanas_perfecto_21="0", ventanas_perfecto_ge19="4")], ruta)
    check(R.region_recomendada(ALT, "BicC_Dm", "perfecto_21", ruta) == (264, 563),
          "con umbral perfecto_21 una alerta de solo >=19 nt no frena la recomendacion")
    try:
        R.region_recomendada(ALT, "BicC_Dm", "perfecto_ge19", ruta)
        check(False, "con umbral perfecto_ge19 esa misma fila deberia frenar")
    except AL.AlertaSinDecidir:
        check(True, "con umbral perfecto_ge19 esa misma fila frena la recomendacion")

    # 4. sin tabla no hay recomendacion: una tabla ausente no es «cero alertas»
    R._ALERTAS_LEIDAS.clear()
    try:
        R.region_recomendada(ALT, "BicC_Dm", tabla=Path(tmp) / "no_existe.tsv")
        check(False, "sin tabla de alertas no deberia salir ninguna region")
    except FileNotFoundError as e:
        check("compuerta" in str(e) or "alertas" in str(e),
              "sin tabla de alertas la compuerta falla cerrada, no deja pasar todo")

    # 5. y sin inventario al lado tampoco, por el mismo motivo (D72): un inventario
    #    ausente no es un inventario vacio, que haria pasar a toda region como tamizada
    tabla_con([fila_alerta(
        decision_usuario="aceptada",
        justificacion_usuario="Se acepta: el acierto es contra XM_046816879.1, el ortologo "
                              "de bicaudal C de un cicadelido ausente en la Argentina.")], ruta)
    (ruta.parent / R.NOMBRE_INVENTARIO).unlink()
    R._ALERTAS_LEIDAS.clear()
    try:
        R.region_recomendada(ALT, "BicC_Dm", tabla=ruta)
        check(False, "sin inventario al lado no deberia salir ninguna region")
    except FileNotFoundError as e:
        check("inventario" in str(e),
              "sin el inventario de regiones tamizadas la compuerta falla cerrada (D72)")

    # 6. la region que no esta en el inventario no se recomienda, aunque la tabla este
    #    perfecta y la region no tenga ni una fila de alerta. Es R7 entero en una prueba:
    #    la region del ranking a k=22 contra el inventario que no la tiene.
    tabla_con([fila_alerta(
        decision_usuario="aceptada",
        justificacion_usuario="Se acepta: el acierto es contra XM_046816879.1, el ortologo "
                              "de bicaudal C de un cicadelido ausente en la Argentina.")], ruta)
    try:
        R.region_recomendada({"mejores": [{"region": "193-392"}]}, "eth_Dm", tabla=ruta)
        check(False, "una region fuera del inventario no deberia recomendarse")
    except AL.RegionNoTamizada as e:
        check("193-392" in str(e),
              "region_recomendada() levanta RegionNoTamizada con una region no tamizada")

    # 7. y la misma region, con el inventario que si la tiene y sin filas de alerta, pasa.
    #    El par 6/7 es la prueba de que lo que decide es la presencia y no las filas.
    tabla_con([fila_alerta(
        decision_usuario="aceptada",
        justificacion_usuario="Se acepta: el acierto es contra XM_046816879.1, el ortologo "
                              "de bicaudal C de un cicadelido ausente en la Argentina.")], ruta,
              inventario=(("BicC_Dm", "264-563"), ("eth_Dm", "193-392")))
    check(R.region_recomendada({"mejores": [{"region": "193-392"}]}, "eth_Dm",
                               tabla=ruta) == (193, 392),
          "con la region en el inventario y sin alertas, la recomendacion sale")

R._ALERTAS_LEIDAS.clear()

# 5. el default del port es D48 literal (D69), y esta como nombre, no en el cuerpo
check(R.UMBRAL_COMPUERTA == "perfecto_21",
      "el umbral por defecto de la compuerta del port es perfecto_21, D48 literal")

# 6. las tres rutas del port pasan por la compuerta: ninguna rearma la region a mano.
#    Es una prueba estructural y hace falta, porque la forma de desactivar la compuerta
#    sin tocarla es volver a escribir al lado la expresion que ella reemplazo.
A_MANO = '["mejores"][0]["region"].split('
FUENTES = {n: (Path(__file__).resolve().parent / n).read_text(encoding="utf-8")
           for n in ("ranking.py", "ranking_v2.py")}
for nombre, fuente in FUENTES.items():
    # en `ranking.py` la unica aparicion legitima de la expresion es la de adentro de la
    # compuerta misma, asi que se mira lo que viene antes de su definicion
    cuerpo = fuente.split("def region_recomendada(")[0]
    check(A_MANO not in cuerpo,
          "%s no convierte el primer puesto en region sin pasar por la compuerta" % nombre)
for funcion in ("def completar_regiones(", "def recomendadas("):
    cuerpo = FUENTES["ranking_v2.py"].split(funcion)[1].split("\ndef ")[0]
    check("R.region_recomendada(" in cuerpo,
          "ranking_v2.%s pasa por la compuerta" % funcion[4:-1])

# y el JSON que escribe ranking_v2 lleva el estado de cada region recomendada (D75), que
# es donde el estado le sirve a quien lee el resultado y no solo a quien llama la funcion
cuerpo_k = FUENTES["ranking_v2.py"].split("def correr_k(")[1].split("\ndef ")[0]
check('"estado_alertas_recomendadas"' in cuerpo_k
      and '"recomendadas_bloqueantes"' in cuerpo_k,
      "correr_k escribe el estado de alertas al lado de regiones_recomendadas")

# 7. contra la tabla real: las regiones que el port recomienda hoy pasan en los dos
#    umbrales de D28, que es lo que D68 dejo medido
if TABLA.exists():
    R._ALERTAS_LEIDAS.clear()
    RECOMENDADAS_C7 = (("MP_MRFV", "72-271"), ("CP_MRFV", "99-298"),
                       ("BicC_Dm", "2121-2420"), ("ATPaseD_Dm", "72-371"),
                       ("eth_Dm", "114-313"), ("bursA_Dm", "13-212"))
    for umbral in ("perfecto_21", "perfecto_ge19"):
        for gen, reg in RECOMENDADAS_C7:
            ini, fin = R.region_recomendada({"mejores": [{"region": reg}]}, gen, umbral, TABLA)
            assert "%d-%d" % (ini, fin) == reg
    check(True, "las seis regiones recomendadas por C7 pasan la compuerta en los dos umbrales")
    R._ALERTAS_LEIDAS.clear()

    # 8. y la corrida a k=22, contra la tabla real: es el estado medido que R7 deja, y la
    #    prueba esta para que si alguien firma las seis filas esto falle y haya que venir
    #    a leer por que. `eth_Dm` 193-392 frena por su acierto perfecto de 21 nt; las
    #    otras cinco pasan el umbral literal de D48 y tres de ellas frenan en el laxo.
    frenadas = {}
    for umbral in ("perfecto_21", "perfecto_ge19"):
        frenadas[umbral] = set()
        for gen, reg in K22:
            try:
                R.region_recomendada({"mejores": [{"region": reg}]}, gen, umbral, TABLA)
            except AL.CompuertaCerrada:
                frenadas[umbral].add((gen, reg))
    check(frenadas["perfecto_21"] == set(),
          "a k=22 y con D48 literal ya no frena ninguna: las seis pasan la compuerta (D73)")
    check(frenadas["perfecto_ge19"] == {("MP_MRFV", "162-361"), ("BicC_Dm", "2119-2418"),
                                        ("ATPaseD_Dm", "71-370")},
          "a k=22 y con el umbral laxo de D28 siguen frenando tres de las seis")
    # Que las seis pasen no es que las seis sirvan, y la diferencia esta medida: una de
    # las seis esta firmada bloqueante, asi que una corrida de k=22 que recomiende sin
    # mirar el estado recomendaria una region que el equipo descarto por escrito.
    bloq_k22 = {(g, r) for g, r in K22
                if AL.estado_decision(reales, g, r)["estado"] == "decidida: bloqueante"}
    check(bloq_k22 == {("eth_Dm", "193-392")},
          "de las seis de k=22 que pasan, una esta bloqueante y hay que descartarla")

    # 9. el estado viaja con la region (D75). Lo que se prueba acá no es que el atributo
    #    exista —eso es trivial— sino las dos mitades que lo hacen util: que la region
    #    bloqueante **sale** (no se frena, D69 intacto) y que **no se la puede recibir sin
    #    el estado**, que era el agujero que D73 destapó. Antes de D75 el que llamaba
    #    recibia un par de enteros indistinguible del de una region limpia.
    R._ALERTAS_LEIDAS.clear()
    reg = R.region_recomendada({"mejores": [{"region": "193-392"}]}, "eth_Dm", tabla=TABLA)
    check(reg == (193, 392) and tuple(reg) == (193, 392) and len(reg) == 2,
          "la region sigue siendo una tupla (ini, fin): nada de lo que ya desempaquetaba cambia")
    ini, fin = reg
    check((ini, fin) == (193, 392), "y sigue desempaquetando en dos enteros")
    check(reg.estado == "decidida: bloqueante" and reg.bloqueante is True
          and reg.decision == "bloqueante",
          "pero ahora trae pegado que esta bloqueante, que es lo que D69 pide mirar")

    # y una region limpia trae su estado tambien: el atributo esta siempre, no solo cuando
    # hay mala noticia, porque un atributo que aparece a veces no se puede consultar nunca
    limpia = R.region_recomendada({"mejores": [{"region": "114-313"}]}, "eth_Dm", tabla=TABLA)
    check(limpia.bloqueante is False and limpia.estado == "sin alertas en este umbral",
          "una region limpia trae el estado igual: el atributo esta siempre")
    limpia_ge19 = R.region_recomendada({"mejores": [{"region": "114-313"}]}, "eth_Dm",
                                       "perfecto_ge19", TABLA)
    check(limpia_ge19.estado == "decidida: aceptada con justificacion"
          and limpia_ge19.bloqueante is False,
          "y el estado es el del umbral con el que se pidio, no uno fijo")
    R._ALERTAS_LEIDAS.clear()
    check(frenadas["perfecto_21"] <= frenadas["perfecto_ge19"],
          "lo que frena el umbral literal lo frena tambien el laxo: los dos estan anidados")
    R._ALERTAS_LEIDAS.clear()
else:
    SALTEADAS.append("§9.7 y §9.8 la tabla real de alertas no esta en disco")


# ------------------------------------------------------------------------------ §10
print()
print("10. la compuerta sabe contra que panel se le pregunta, y frena igual (D77)")

# El caso exacto que pide el issue #35: **la misma region, el mismo umbral**, con y sin el
# organismo de la alerta en el panel. Es el de la rama `sin_humano` de
# `ranking_v2.efecto_humano()`, que evaluaba sus regiones contra filas de *Homo sapiens*
# que esa misma rama habia sacado del panel.
HUM = fila_alerta(gen="BicC_Dm", region="922-1221", organismo_corto="humano",
                  organismo_especie="Homo sapiens",
                  organismo_rol="no objetivo de maxima consecuencia")
INV_PANEL = {("BicC_Dm", "922-1221")}
PANEL_CON = {"maiz", "H_vitripennis", "humano", "D_maidis"}
PANEL_SIN = {"maiz", "H_vitripennis", "D_maidis"}

for umbral in ("perfecto_21", "perfecto_ge19"):
    mensajes = {}
    for nombre, panel in (("con", PANEL_CON), ("sin", PANEL_SIN)):
        try:
            AL.exigir_decidida([HUM], "BicC_Dm", "922-1221", umbral,
                               inventario=INV_PANEL, panel=panel)
            check(False, "la fila humana pendiente deberia frenar con el panel %s humano"
                         % nombre)
        except AL.AlertaSinDecidir as e:
            mensajes[nombre] = str(e)
    check(len(mensajes) == 2,
          "en %s frena las dos veces: sacar al humano del panel no abre la compuerta"
          % umbral)
    check("NO tiene en el panel" not in mensajes.get("con", ""),
          "con humano en el panel el mensaje no habla de organismos fuera (%s)" % umbral)
    check("NO tiene en el panel" in mensajes.get("sin", "")
          and "humano" in mensajes.get("sin", ""),
          "sin humano en el panel el mensaje lo nombra y dice por que frena igual (%s)"
          % umbral)

# Y el estado lo dice en datos, no solo en la prosa del error.
est_con = AL.estado_decision([HUM], "BicC_Dm", "922-1221", panel=PANEL_CON)
est_sin = AL.estado_decision([HUM], "BicC_Dm", "922-1221", panel=PANEL_SIN)
check(est_con["pendientes"] == est_sin["pendientes"] == 1
      and est_con["estado"] == est_sin["estado"] == "sin decidir",
      "el panel no mueve ni el conteo de pendientes ni el estado: D77 no filtra")
check(est_con["organismos_fuera_del_panel"] == []
      and est_sin["organismos_fuera_del_panel"] == ["humano"]
      and est_sin["pendientes_fuera_del_panel"] == ["humano"],
      "y el estado nombra la fila que es de un organismo fuera del panel")
check(est_con["panel"] == sorted(PANEL_CON) and est_sin["panel"] == sorted(PANEL_SIN),
      "el estado deja escrito contra que panel se pregunto")

# `None` es «no se declaro panel», que no es «el panel esta vacio»: con panel vacio toda
# fila queda fuera, y la diferencia tiene que notarse.
est_nada = AL.estado_decision([HUM], "BicC_Dm", "922-1221")
est_vacio = AL.estado_decision([HUM], "BicC_Dm", "922-1221", panel=set())
check(est_nada["panel"] is None and est_nada["organismos_fuera_del_panel"] == [],
      "sin declarar panel la compuerta no afirma nada sobre el panel")
check(est_vacio["panel"] == [] and est_vacio["organismos_fuera_del_panel"] == ["humano"],
      "y un panel vacio declarado no es lo mismo: ahi la fila si esta fuera")

# Una fila decidida pasa igual aunque sea de un organismo fuera del panel —el panel no
# decide nada— y el estado que devuelve la compuerta lo sigue informando.
FIRMADA = fila_alerta(gen="BicC_Dm", region="922-1221", organismo_corto="humano",
                      organismo_especie="Homo sapiens",
                      organismo_rol="no objetivo de maxima consecuencia",
                      decision_usuario="aceptada",
                      justificacion_usuario=(
                          "XM_046816879.1 es la accesion de esta fila; la justificacion "
                          "es de prueba y solo existe para que la fila este decidida."))
est_ok = AL.exigir_decidida([FIRMADA], "BicC_Dm", "922-1221",
                            inventario=INV_PANEL, panel=PANEL_SIN)
check(est_ok["estado"] == "decidida: aceptada con justificacion"
      and est_ok["organismos_fuera_del_panel"] == ["humano"],
      "una fila decidida de un organismo fuera del panel pasa, y el estado lo informa")

# El panel que la compuerta usa por defecto es el **vivo** de la corrida: eso es lo que
# hace que la rama `sin_humano` quede declarada sin que nadie se acuerde de pasarlo.
try:
    V.con_panel(sin_humano=False)
    con_h = R.panel_actual()
    V.con_panel(sin_humano=True)
    sin_h = R.panel_actual()
finally:
    V.con_panel(sin_humano=False)
check("humano" in con_h and "humano" not in sin_h,
      "panel_actual() refleja el panel que la corrida tiene puesto en ese momento")
check("D_maidis" in con_h and "D_maidis" in sin_h,
      "y D_maidis esta siempre: se excluye por ser on-target, no por estar fuera del panel")
check(con_h - sin_h == {"humano"},
      "la unica diferencia entre las dos ramas de efecto_humano es la referencia humana")

# Y contra la tabla real: la fila humana de BicC_Dm 922-1221 esta firmada (D68), asi que
# con el panel de W7 —sin humano— la region pasa y la compuerta igual deja escrito que esa
# fila es de un organismo que esa corrida no mira.
if TABLA.exists():
    R._ALERTAS_LEIDAS.clear()
    reales = R.alertas_de(TABLA)
    inv_panel = R.inventario_de(TABLA)
    e_real = AL.exigir_decidida(reales, "BicC_Dm", "922-1221", "perfecto_ge19",
                                inventario=inv_panel, panel=sin_h)
    check(e_real["estado"] == "decidida: aceptada con justificacion"
          and e_real["organismos_fuera_del_panel"] == ["humano"],
          "en la tabla real, 922-1221 pasa con el panel de W7 y la fila humana queda nombrada")
    R._ALERTAS_LEIDAS.clear()
else:
    SALTEADAS.append("§10 la tabla real de alertas no esta en disco")


print()
if SALTEADAS:
    print("SALTEADAS: %s" % "; ".join(SALTEADAS))
if FALLAS:
    print("FALLAS: %d" % len(FALLAS))
    sys.exit(1)
print("todo bien")
