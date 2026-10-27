"""Verificaciones de `evidencia_en_prosa.py`, la feature `F2` del issue #26.

Las tres casillas del criterio de terminado del issue, y nada mas que eso:

- **Cada afirmacion del parrafo tiene su fuente al lado.** No alcanza con que el parrafo
  cite: se prueba que `frases` tenga una fuente no vacia por frase, que toda fuente sea
  uno de los campos de procedencia que la ficha declara —no cualquier palabra suelta de
  la ficha— y que el parrafo sea exactamente la union de esas frases. Y se prueba que la
  identidad del alineamiento no se cite con la accesion del ortologo: son dos
  afirmaciones distintas y una es medicion nuestra.
- **Un locus sin anotacion no recibe parrafo.** Se prueba con las tres formas de no tener
  anotacion transferible que distinguen `F1` y `alertas.partir_anotacion`: ficha sin
  bloque de anotacion, cabecera sin parentesis —el ensamblado genomico del vector, que es
  el modo de falla que el issue nombra—, nombre no informativo («uncharacterized») y
  alineamiento sin ortologo reciproco. Todas devuelven el texto fijo y **cuentan** en el
  censo, igual que la ficha que no se puede leer: `F1` pide que los loci sin anotacion
  informativa aparezcan contados, no filtrados.
- **Nada de esto entra al diseno.** Prueba estructural: ningun `.py` del repositorio
  importa este modulo, y la salida no trae ninguna clave de puntaje.

Y la pieza que vuelve segura la feature si el parrafo lo escribe un modelo de lenguaje en
vez de la plantilla: `verificar_procedencia()` es determinista y rechaza toda palabra,
todo numero y toda fuente que no salgan de la ficha. Se prueba contra el parrafo de la
plantilla —que tiene que pasar, y pasar es lo que mantiene el vocabulario de la plantilla
en sincronia— y contra cinco parrafos adulterados a mano.

    python pipeline/test_evidencia_en_prosa.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import evidencia_en_prosa as P    # noqa: E402

FALLAS, SALTEADAS = [], []


def check(cond, msg):
    print(("  ok   " if cond else "  FALLA") + "  " + msg)
    if not cond:
        FALLAS.append(msg)


def falla_con(exc, fn, msg):
    try:
        fn()
    except exc:
        check(True, msg)
    except Exception as e:                                      # noqa: BLE001
        check(False, msg + " (levanto %s: %s)" % (type(e).__name__, e))
    else:
        check(False, msg + " (no levanto nada)")


# --------------------------------------------------------------------- fichas de prueba

# La cabecera es real: es la misma de `work/W5/ref/` que usa `test_alertas.py`, y es de
# donde salen el simbolo y el LOC. La identidad, la cobertura y la banda son los numeros
# que el issue #25 pone como ejemplo de lo que tiene que viajar con cada anotacion.
ANOT = {
    "cabecera": "PREDICTED: Homalodisca vitripennis protein bicaudal C homolog 1-A "
                "(LOC124362408), mRNA",
    "accesion": "XM_046974266.1",
    "organismo": "Homalodisca vitripennis",
    "identidad": 94.0,
    "cobertura_orf": 88.0,
    "cobertura_referencia": 91.0,
    "reciproco": True,
    "empate": False,
    "fuente_alineamiento": "F1 diamond blastp, transferencia_HV.tsv.gz",
    "banda": {"tramo": "mayor o igual a 90", "concordancia": 86.2, "ic": [80.9, 90.2],
              "n": 1152, "concluyente": True, "fuente": "C12 A"},
}

FICHA_ANOTADA = {
    "locus": "DMAI_0001234",
    "anotacion": ANOT,
    "go": [{"id": "GO:0045495", "termino": "pole plasm", "fuente": "UniProt GOA"}],
    "dominios": [{"id": "PF00013", "nombre": "KH_1", "fuente": "Pfam"}],
    "papers": [{"doc_id": "PMID:24550109",
                "cita": "bicaudal C is required for oogenesis"}],
}

FICHA_SIN_BLOQUE = {"locus": "DMAI_0009999", "anotacion": None}

# El modo de falla que nombra el issue: la cabecera del ensamblado genomico del vector no
# tiene parentesis, asi que no hay gen. Inventarle un simbolo al cromosoma seria el peor
# error posible, y es justo lo que un modelo de lenguaje hace con naturalidad.
FICHA_CROMOSOMA = {
    "locus": "DMAI_0007777",
    "anotacion": dict(ANOT, cabecera="Dalbulus maidis genome assembly, chromosome: 6",
                      accesion="OX376242.1", organismo="Dalbulus maidis"),
}

FICHA_NO_INFORMATIVA = {
    "locus": "DMAI_0005555",
    "anotacion": dict(ANOT, cabecera="PREDICTED: Homalodisca vitripennis uncharacterized "
                                     "protein LOC124360001 (LOC124360001), mRNA"),
}

FICHA_NO_RECIPROCA = {"locus": "DMAI_0004444", "anotacion": dict(ANOT, reciproco=False)}

# `F1` no resuelve un empate en el primer puesto y por eso no lo cuenta como reciproco;
# decirle «sin ortologo reciproco» perderia que el alineamiento existe.
FICHA_EMPATE = {"locus": "DMAI_0002222",
                "anotacion": dict(ANOT, reciproco=False, empate=True)}

FICHA_SIN_BANDA = {"locus": "DMAI_0003333",
                   "anotacion": {k: v for k, v in ANOT.items() if k != "banda"}}

# El tramo de identidad bajo que la medicion de origen rotula no concluyente: 16 pares.
FICHA_NO_CONCLUYENTE = {
    "locus": "DMAI_0001111",
    "anotacion": dict(ANOT, identidad=38.0, banda=dict(ANOT["banda"], tramo="menor a 40",
                                                       concordancia=25.0, ic=[10.2, 49.5],
                                                       n=16, concluyente=False)),
}


# ------------------------------------------- 1. el parrafo, y la fuente de cada frase

print("\n1. el locus anotado recibe parrafo, y cada frase trae su fuente")

salida = P.redactar(FICHA_ANOTADA)
legitimas = P.fuentes_de(FICHA_ANOTADA)

check(salida["estado"] == P.ANOTADA, "estado 'anotada' para el locus con ortologo reciproco")
check(len(salida["frases"]) >= 3, "el parrafo tiene al menos tres frases (%d)"
      % len(salida["frases"]))
check(all(f["fuente"].strip() for f in salida["frases"]), "ninguna frase queda sin fuente")
check(salida["texto"] == " ".join(f["texto"] for f in salida["frases"]),
      "el parrafo es exactamente la union de las frases, sin texto suelto sin fuente")

# Toda fuente citada tiene que ser un campo de procedencia declarado, no una palabra
# cualquiera de la ficha. Una fuente que no es una fuente es peor que una frase sin
# fuente: parece verificada.
check(all(f["fuente"] in legitimas for f in salida["frases"]),
      "toda fuente citada es un campo de procedencia de la ficha")
check("oogenesis" not in legitimas and "Homalodisca" not in legitimas,
      "una palabra suelta de la ficha no cuenta como fuente")

# La identidad y la cobertura son medicion nuestra; la accesion dice QUIEN es el ortologo,
# no cuanto alinea. Dos afirmaciones, dos fuentes.
frase_alin = [f for f in salida["frases"] if "cobertura del ORF" in f["texto"]]
check(len(frase_alin) == 1 and frase_alin[0]["fuente"] == ANOT["fuente_alineamiento"],
      "la identidad y la cobertura se citan con la corrida que las midio, no con la accesion")
frase_quien = [f for f in salida["frases"] if f["texto"].startswith("El locus")]
check(len(frase_quien) == 1 and frase_quien[0]["fuente"] == ANOT["accesion"],
      "quien es el ortologo se cita con su accesion")

# El cortafuego de D37 viaja con la salida y **no** adentro del parrafo: es una decision
# nuestra, no evidencia recuperada, asi que no tiene fuente que verificar.
check("D37" in salida["advertencia"], "la salida trae la advertencia del cortafuego D37")
check("D37" not in salida["texto"],
      "la advertencia no se cuela adentro del parrafo como si fuera evidencia")

# Lo que la feature NO hace: generar funcion. El simbolo transferido aparece; ninguna
# atribucion de funcion que no este en la ficha, tampoco.
check("bicaudal" in salida["texto"].lower(), "el simbolo transferido aparece en el parrafo")
check("LOC124362408" in salida["texto"], "el LOC del ortologo aparece en el parrafo")
check("86,2" in salida["texto"], "la concordancia medida de la banda aparece en el parrafo")
check("80,9" in salida["texto"],
      "el intervalo de confianza aparece: sin la banda la feature miente por omision")

# Dos terminos GO de bases distintas dan dos frases, cada una con su procedencia. Si
# fueran una sola frase, la mitad de los terminos quedaria citada con la fuente de la otra
# mitad: una afirmacion sin fuente con aspecto de afirmacion citada.
dos_bases = dict(FICHA_ANOTADA, go=[
    {"id": "GO:0045495", "termino": "pole plasm", "fuente": "UniProt GOA"},
    {"id": "GO:0003723", "termino": "RNA binding", "fuente": "InterPro2GO"}])
frases_go = [f for f in P.redactar(dos_bases)["frases"] if "ontologia" in f["texto"]]
check(len(frases_go) == 2, "dos terminos GO de bases distintas dan dos frases (%d)"
      % len(frases_go))
check({f["fuente"] for f in frases_go} == {"UniProt GOA", "InterPro2GO"},
      "cada frase de GO lleva la procedencia de sus propios terminos")

# Un tramo que la medicion de origen rotula no concluyente se dice. Publicar su
# concordancia sin esa linea es citar un numero que su propio autor no sostiene.
flojo = P.redactar(FICHA_NO_CONCLUYENTE)
check("no concluyente" in flojo["texto"],
      "el parrafo dice que el tramo esta rotulado no concluyente")
check(P.verificar_procedencia(flojo, FICHA_NO_CONCLUYENTE)["ok"],
      "y ese parrafo pasa la verificacion de procedencia")
check("no concluyente" not in salida["texto"],
      "y no lo dice cuando el tramo si es concluyente")

# La unidad la pone la ficha. `F1` habla de contigs y no de loci —varios contigs pueden ser
# isoformas del mismo gen— y el parrafo tiene que decir lo que la corrida midio.
como_contig = P.redactar(dict(FICHA_ANOTADA, unidad="contig"))
check(como_contig["texto"].startswith("El contig DMAI_0001234 alinea"),
      "el parrafo nombra la unidad que declara la ficha (%s)"
      % como_contig["texto"][:30])
check(salida["texto"].startswith("El locus DMAI_0001234 alinea"),
      "y usa «locus» cuando la ficha no declara otra")


# ----------------------------------- 2. sin anotacion no hay parrafo, y queda contado

print("\n2. las tres formas de no tener anotacion transferible no reciben parrafo")

casos = [
    (FICHA_SIN_BLOQUE, P.SIN_ANOTACION_DE_GEN, "la ficha no trae bloque de anotacion"),
    (FICHA_CROMOSOMA, P.SIN_ANOTACION_DE_GEN,
     "la cabecera no tiene parentesis: es el cromosoma"),
    (FICHA_NO_INFORMATIVA, P.ANOTACION_NO_INFORMATIVA,
     "el nombre recuperado es «uncharacterized»"),
    (FICHA_NO_RECIPROCA, P.ORTOLOGIA_NO_RECIPROCA,
     "el alineamiento no es un par reciproco"),
    (FICHA_EMPATE, P.EMPATE_DE_ORTOLOGIA, "el primer puesto empato y F1 no lo resuelve"),
]
for ficha, esperado, motivo in casos:
    r = P.redactar(ficha)
    check(r["estado"] == esperado,
          "estado %r cuando %s (dio %r)" % (esperado, motivo, r["estado"]))
    check(r["frases"] == [], "no se redacta ninguna frase cuando %s" % motivo)
    check(r["texto"] == P.TEXTO_DE[esperado],
          "devuelve el texto fijo y no una conjetura cuando %s" % motivo)

# La casilla literal del issue: la salida del locus sin anotacion es «sin anotacion de
# gen», no un parrafo.
check(P.redactar(FICHA_SIN_BLOQUE)["texto"] == "sin anotacion de gen",
      "el texto del locus sin anotacion es exactamente «sin anotacion de gen»")

# Y todos cuentan, la ficha ilegible incluida. Una sola ficha rota de `F1` no puede tirar
# abajo el recuento de 12.540 loci: eso seria filtrar por accidente justo lo que hay que
# contar.
censo = P.censo([FICHA_ANOTADA, FICHA_SIN_BLOQUE, FICHA_CROMOSOMA, FICHA_NO_INFORMATIVA,
                 FICHA_NO_RECIPROCA, FICHA_EMPATE, FICHA_SIN_BANDA])
check(censo["total"] == 7, "el censo cuenta los siete loci (%d)" % censo["total"])
check(censo[P.ANOTADA] == 1 and censo[P.SIN_ANOTACION_DE_GEN] == 2
      and censo[P.ANOTACION_NO_INFORMATIVA] == 1 and censo[P.ORTOLOGIA_NO_RECIPROCA] == 1
      and censo[P.EMPATE_DE_ORTOLOGIA] == 1 and censo[P.FICHA_INCOMPLETA] == 1,
      "el censo reparte 1/2/1/1/1/1 entre los seis estados")
check(censo["con_parrafo"] + censo["sin_parrafo"] == censo["total"],
      "todo locus esta en una de las dos columnas: ninguno se pierde")


# -------------------------------------------- 3. la evidencia incompleta no se publica

print("\n3. una evidencia sin el campo que la vuelve citable es ficha incompleta")

falla_con(P.FichaIncompleta, lambda: P.redactar(FICHA_SIN_BANDA),
          "redactar() con anotacion sin banda levanta FichaIncompleta")
for campo in ("identidad", "cobertura_orf", "cobertura_referencia",
              "fuente_alineamiento", "accesion", "empate"):
    rota = {"locus": "X", "anotacion": {k: v for k, v in ANOT.items() if k != campo}}
    falla_con(P.FichaIncompleta, lambda f=rota: P.redactar(f),
              "redactar() sin %s levanta FichaIncompleta" % campo)

# `reciproco` ausente no es `reciproco` falso. Publicar «no es un par reciproco» cuando
# nadie lo midio es dar por medido un negativo: es la tercera correccion de `F1`.
sin_rec = {"locus": "X", "anotacion": {k: v for k, v in ANOT.items() if k != "reciproco"}}
falla_con(P.FichaIncompleta, lambda: P.redactar(sin_rec),
          "una ficha sin el campo reciproco es incompleta, no «no reciproca»")
check(P.redactar(FICHA_NO_RECIPROCA)["estado"] == P.ORTOLOGIA_NO_RECIPROCA,
      "y con el campo en False si es «no reciproca»: el dato medido se respeta")

# Un termino GO o un paper sin su procedencia tampoco se publica ni se descarta callado.
for lista, item in (("go", {"id": "GO:1", "termino": "x"}),
                    ("dominios", {"id": "PF1", "nombre": "x"}),
                    ("papers", {"cita": "x"})):
    rota = dict(FICHA_ANOTADA)
    rota[lista] = [item]
    falla_con(P.FichaIncompleta, lambda f=rota: P.redactar(f),
              "una entrada de %s sin su fuente levanta FichaIncompleta" % lista)


# ------------------------------------------------------- 4. la verificacion de origen

print("\n4. verificar_procedencia() rechaza lo que no sale de la ficha")

v_plantilla = P.verificar_procedencia(salida, FICHA_ANOTADA)
check(v_plantilla["ok"], "el parrafo de la plantilla pasa su propia verificacion (%s)"
      % (", ".join(v_plantilla["fuera_de_ficha"]) or "sin sobrantes"))

# Una funcion inventada. Es el modo de falla del issue en una palabra: plausible, no
# recuperada. Ninguna de las dos palabras esta en la ficha ni en la plantilla.
v_inventado = P.verificar_procedencia({
    "estado": P.ANOTADA,
    "texto": salida["texto"] + " El gen regula la apoptosis intestinal.",
    "frases": salida["frases"] + [{"texto": "El gen regula la apoptosis intestinal.",
                                   "fuente": ANOT["accesion"]}]}, FICHA_ANOTADA)
check(not v_inventado["ok"], "un parrafo con una funcion inventada no pasa")
check("apoptosis" in v_inventado["fuera_de_ficha"],
      "la verificacion nombra la palabra inventada")

# Una cifra inventada. La identidad real es 94; 97,3 no esta en ninguna parte de la ficha
# y es exactamente el error que no se ve leyendo.
v_cifra = P.verificar_procedencia({
    "estado": P.ANOTADA, "texto": "El alineamiento tiene 97,3 % de identidad.",
    "frases": [{"texto": "El alineamiento tiene 97,3 % de identidad.",
                "fuente": ANOT["fuente_alineamiento"]}]}, FICHA_ANOTADA)
check(not v_cifra["ok"], "un parrafo con una cifra que no esta en la ficha no pasa")
check(any("97,3" in x for x in v_cifra["fuera_de_ficha"]),
      "la verificacion nombra la cifra inventada")

# Un recorte de una palabra de la ficha. Pasaria cualquier chequeo de subcadena —«oge»
# esta adentro de «oogenesis»— y dice otra cosa. Se compara por palabra entera.
v_recorte = P.verificar_procedencia({
    "estado": P.ANOTADA, "texto": "El gen tiene oge.",
    "frases": [{"texto": "El gen tiene oge.", "fuente": "PMID:24550109"}]}, FICHA_ANOTADA)
check(not v_recorte["ok"] and "oge" in v_recorte["fuera_de_ficha"],
      "un recorte de una palabra de la ficha no pasa: se compara por palabra entera")

# Una fuente que es una palabra de la ficha pero no un campo de procedencia.
v_fuente = P.verificar_procedencia({
    "estado": P.ANOTADA, "texto": "El gen tiene %s de identidad." % "94",
    "frases": [{"texto": "El gen tiene 94 de identidad.", "fuente": "oogenesis"}]},
    FICHA_ANOTADA)
check(not v_fuente["ok"] and v_fuente["fuentes_invalidas"] == ["oogenesis"],
      "citar como fuente una palabra que no es campo de procedencia no pasa")

# Una frase sin fuente.
v_sin_fuente = P.verificar_procedencia({
    "estado": P.ANOTADA, "texto": "El gen tiene 94 de identidad.",
    "frases": [{"texto": "El gen tiene 94 de identidad.", "fuente": ""}]}, FICHA_ANOTADA)
check(not v_sin_fuente["ok"] and v_sin_fuente["frases_sin_fuente"] == [0],
      "una frase sin fuente no pasa y la verificacion dice cual es")

# Un texto que no es la union de sus frases: por ahi se cuela prosa sin fuente.
v_colado = P.verificar_procedencia({
    "estado": P.ANOTADA, "texto": salida["texto"] + " Y ademas es esencial.",
    "frases": salida["frases"]}, FICHA_ANOTADA)
check(not v_colado["ok"], "un texto con prosa fuera de las frases no pasa")

# El estado sin parrafo se verifica igual: el texto fijo, y nada mas.
check(P.verificar_procedencia(P.redactar(FICHA_SIN_BLOQUE), FICHA_SIN_BLOQUE)["ok"],
      "la salida «sin anotacion de gen» pasa la verificacion")
v_falso = P.verificar_procedencia({
    "estado": P.SIN_ANOTACION_DE_GEN,
    "texto": "Probablemente sea una subunidad de la V-ATPasa.", "frases": []},
    FICHA_SIN_BLOQUE)
check(not v_falso["ok"],
      "una conjetura publicada bajo el estado «sin anotacion» no pasa")


# ------------------------------------------------------------- 5. el cortafuego de D37

print("\n5. ninguna salida de esta feature entra al diseno ni al ranking")

# La forma verificable del tercer criterio del issue: que nadie la importe. Se barre el
# repositorio entero y no solo las carpetas de codigo, porque el ranking que podria
# consumirla —`F3`, el recomendador— se esta armando en `research/`, que es justo donde
# un barrido de `pipeline/` y `tools/` no mira. Si manana un modulo la importa, esta
# prueba falla y hay que discutirlo, que es lo que el cortafuego pide.
# Los archivos de la feature misma: el modulo, su adaptador de entrada y los dos tests. El
# adaptador la importa y esta bien que lo haga —es la entrada de F2, no un consumidor de su
# salida—; lo que el cortafuego prohibe es que la lea algo que disena o rankea.
DE_LA_FEATURE = ("evidencia_en_prosa.py", "fichas_desde_f1.py", "test_fichas_desde_f1.py")
propios = {Path(__file__).name} | set(DE_LA_FEATURE)
escaneados, importadores = 0, []
for py in RAIZ.rglob("*.py"):
    partes = py.relative_to(RAIZ).parts
    if ".claude" in partes or "__pycache__" in partes or py.name in propios:
        continue
    escaneados += 1
    if "evidencia_en_prosa" in py.read_text(encoding="utf-8", errors="replace"):
        importadores.append(str(py.relative_to(RAIZ)))
if escaneados < 50:
    SALTEADAS.append("§5 solo se encontraron %d .py en el arbol: el barrido no es "
                     "representativo" % escaneados)
else:
    check(not importadores,
          "ninguno de los %d .py del repositorio menciona evidencia_en_prosa (%s)"
          % (escaneados, ", ".join(importadores) or "ninguno"))

# Y la salida no trae ninguna clave con la que se pueda rankear sin querer.
PUNTAJE = ("puntaje", "score", "ranking", "orden", "prioridad", "esencial", "peso")
check(not [k for k in salida if any(p in k.lower() for p in PUNTAJE)],
      "la salida no tiene ninguna clave de puntaje: no es rankeable por accidente")
check(not [k for k in censo if any(p in k.lower() for p in PUNTAJE)],
      "el censo tampoco: cuenta loci, no los ordena")


print()
if SALTEADAS:
    print("SALTEADAS: %s" % "; ".join(SALTEADAS))
if FALLAS:
    print("FALLAS: %d" % len(FALLAS))
    sys.exit(1)
print("todo bien")
