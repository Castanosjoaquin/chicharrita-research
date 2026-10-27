"""`F2` (issue #26): la evidencia recuperada por homologia, leida en lenguaje natural.

El cuello de botella del biologo no es calcular: es leer los 12.540 loci que `C5` recupero
en el ensamblado no anotado de *Dalbulus maidis* `[M]`. Este modulo arma, por locus, un
parrafo que dice que se sabe de ese gen **y de donde sale cada cosa que dice**.

**La regla dura, que es el modulo entero.** Aca se *resume anotacion recuperada*; nunca se
*genera funcion*. La entrada son los nombres de producto, los terminos GO, los dominios
conservados y los papers que encontro `F1`. La salida es prosa armada con esas piezas. El
modo de falla contra el que esta disenado ya estaba documentado en el repositorio, en
`tools/sifi21_port/alertas.py`: una cabecera FASTA **sin parentesis** no es un transcripto
anotado —el ensamblado genomico del vector dice «Dalbulus maidis genome assembly,
chromosome: 6»— y inventarle un simbolo al cromosoma seria el peor error posible. Un
modelo de lenguaje lo inventa con toda naturalidad. Entonces: **sin anotacion, no hay
parrafo**, y la salida es el texto fijo «sin anotacion de gen».

Esa regla no se reescribe aca. `estado_de()` llama a `alertas.partir_anotacion()`, que es
donde vive, porque un filtro que vive en un camino y no en el otro no es un filtro.

**Tres piezas, y ninguna necesita un modelo de lenguaje:**

  1. `estado_de`             DETERMINISTA. Decide si hay anotacion transferible, y si no
                             la hay, cual de las tres formas de no haberla es. Las tres
                             **cuentan** en el censo, igual que las fichas incompletas:
                             `F1` pide que los loci sin anotacion informativa aparezcan
                             contados, no filtrados, porque una plataforma que los
                             descarte en silencio sobredeclara su cobertura.
  2. `redactar`              DETERMINISTA. Arma el parrafo por plantilla, una frase por
                             fuente, cada una con esa fuente al lado. No hay ninguna
                             palabra de contenido que no venga de la ficha.
  3. `verificar_procedencia` DETERMINISTA, y es la pieza que importa. Audita un parrafo
                             **cualquiera** contra su ficha: toda palabra que no este en
                             el vocabulario fijo de la plantilla tiene que aparecer en la
                             ficha, todo numero tambien, y toda fuente citada tiene que
                             ser uno de los campos de procedencia que `F1` declara —no
                             cualquier palabra suelta de la ficha—. Si manana el parrafo
                             lo escribe un modelo de lenguaje en vez de la plantilla, esta
                             funcion es lo unico que hay entre su fluidez y una afirmacion
                             sin fuente.

Es la misma division de trabajo que `agente_evidencia.py`: el que redacta puede ser un
modelo, el que verifica nunca. Y el limite declarado es el mismo: **la verificacion prueba
que las palabras salen de la ficha, no que la frase sea cierta.** Una pieza real puesta en
un orden equivocado pasa el chequeo lexico. Eso no lo arregla ningun script.

**Una frase, una fuente, y la fuente es la que corresponde.** La identidad y la cobertura
del alineamiento son medicion nuestra `[M]`, no un dato de RefSeq, asi que viajan con la
fuente de la corrida que las produjo y no con la accesion del ortologo; la accesion
respalda **quien es** el ortologo, que es otra afirmacion. Los terminos GO y los dominios
se agrupan por fuente, una frase por fuente, para que ningun termino quede citado con la
procedencia de otro.

**El cortafuego de `D37`.** Esto contesta *que gen considerar*. No entra al diseno del
ARNdc, que se hace siempre sobre la secuencia propia del vector: las ventanas de 21 nt de
la especie cercana que existen identicas en *D. maidis* son 0,7 % a 11,1 % `[M]`. La
salida lo dice en `ADVERTENCIA`, que es constante y viaja **afuera** del parrafo —no es
evidencia recuperada y no tiene por que pasar por la verificacion de procedencia—; la
salida no tiene ninguna clave de puntaje; y `test_evidencia_en_prosa.py` §5 prueba que
ningun `.py` del repositorio importa este modulo. La version original de esta idea
—categorizar genes con un modelo de lenguaje para decidir cuales son esenciales— esta en
`00_meta/CAMINOS_PROBADOS.md` como camino reemplazado y no se reabre.

**La entrada todavia no existe en disco.** `F1` (issue #25) es la que produce estas fichas
y no corrio todavia. El contrato de la ficha esta declarado abajo en `FICHA` y las pruebas
corren contra fichas escritas a mano; la primera corrida real es sobre el zip del
investigador cuando llegue. `[H]` Que el contrato sea el correcto es una hipotesis nuestra
hasta que `F1` escriba la primera ficha de verdad, y el campo que mas riesgo tiene de no
existir alla es `fuente_alineamiento`: nadie lo pidio antes de este modulo.

Uso:
    python3 evidencia_en_prosa.py fichas.json [--salida parrafos.json]
    python3 evidencia_en_prosa.py fichas.json --censo
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "tools" / "sifi21_port"))

import alertas as AL              # noqa: E402

# --------------------------------------------------------------------- el contrato

# Lo que `F1` tiene que entregar por locus. Los campos de `anotacion` son obligatorios
# todos juntos: `F1` corrige que cada anotacion transferida viaje con su identidad y su
# banda de concordancia, porque sin la banda la feature miente por omision `[H]`. No es
# «es una subunidad de la V-ATPasa», es «con 94 % de identidad a su ortologo reciproco,
# tramo en el que la concordancia medida es 86 %».
FICHA = {
    "locus": "id del locus en el ensamblado o transcriptoma del vector",
    "anotacion": {
        "cabecera": "la cabecera FASTA del ortologo, tal como esta en disco",
        "accesion": "accesion del ortologo: respalda QUIEN es, no cuanto alinea",
        "organismo": "especie del ortologo",
        "identidad": "porcentaje de identidad del alineamiento de proteina",
        "cobertura": "porcentaje de la proteina consulta cubierto",
        "reciproco": "True o False, medido; si no se midio, la ficha esta incompleta",
        "fuente_alineamiento": "la corrida que midio identidad, cobertura y reciprocidad",
        "banda": {"tramo": "", "concordancia": 0.0, "ic": [0.0, 0.0], "n": 0,
                  "fuente": "la medicion de concordancia que respalda el tramo"},
    },
    "go": [{"id": "", "termino": "", "fuente": ""}],
    "dominios": [{"id": "", "nombre": "", "fuente": ""}],
    "papers": [{"doc_id": "", "cita": "cita literal, ya verificada aguas arriba"}],
}

CAMPOS_ANOTACION = ("cabecera", "accesion", "organismo", "identidad", "cobertura",
                    "reciproco", "fuente_alineamiento", "banda")
CAMPOS_BANDA = ("tramo", "concordancia", "ic", "n", "fuente")

# Las listas de evidencia y que campo las vuelve citables. Una entrada sin su fuente no se
# puede publicar ni se puede esconder: vuelve incompleta a la ficha entera, que es como
# `alertas.validar_fila` trata un campo faltante y lo que manda `CLAUDE.md` —sin fuente,
# no entra al reporte—.
LISTAS = {"go": ("termino", "fuente"), "dominios": ("nombre", "fuente"),
          "papers": ("cita", "doc_id")}

# Los cuatro estados que puede tener un locus, mas el de la ficha que no se puede leer.
# Solo el primero recibe parrafo; los otros tres son las tres formas de no tener anotacion
# transferible, y se distinguen porque dicen cosas distintas sobre la corrida: una es que
# el locus no alineo contra nada con nombre, otra es que alineo contra algo sin nombre, y
# la tercera es que alineo pero el reciproco no vuelve.
ANOTADA = "anotada"
SIN_ANOTACION_DE_GEN = "sin_anotacion_de_gen"      # misma clave que alertas.py
ANOTACION_NO_INFORMATIVA = "anotacion_no_informativa"
ORTOLOGIA_NO_RECIPROCA = "ortologia_no_reciproca"
FICHA_INCOMPLETA = "ficha_incompleta"

ESTADOS = (ANOTADA, SIN_ANOTACION_DE_GEN, ANOTACION_NO_INFORMATIVA,
           ORTOLOGIA_NO_RECIPROCA, FICHA_INCOMPLETA)

# El texto que sale en vez del parrafo. Es el punto entero del issue: devolver esto, y no
# una conjetura plausible. Los tres son distintos a proposito: decirle «sin anotacion de
# gen» a un locus que si alineo contra un ortologo sin nombre informativo seria perder la
# unica informacion que esa corrida produjo sobre el.
TEXTO_DE = {
    SIN_ANOTACION_DE_GEN: "sin anotacion de gen",
    ANOTACION_NO_INFORMATIVA: "sin anotacion de gen informativa",
    ORTOLOGIA_NO_RECIPROCA: "sin ortologo reciproco",
}

# Viaja con cada salida y **no** es una frase del parrafo: es una decision nuestra, no
# evidencia recuperada, asi que no tiene fuente que verificar contra la ficha.
ADVERTENCIA = ("Esta lectura dice que gen considerar; no entra al diseno del ARNdc, que se "
               "hace siempre sobre la secuencia propia del vector (D37).")

# Nombres de producto que son la ausencia de un nombre. `C12` los excluyo de la medicion
# de concordancia; aca no se excluyen, se cuentan aparte.
NO_INFORMATIVOS = ("uncharacterized", "hypothetical", "unnamed protein",
                   "unknown function", "putative protein", "predicted protein")


class FichaIncompleta(ValueError):
    """La ficha trae evidencia sin alguno de los campos que la vuelven publicable."""


# ------------------------------------------------------------------- 1. el estado

def _simbolo_de(anot: dict) -> tuple[str, str]:
    """Simbolo y LOC del ortologo, con el nombre de la especie sacado del simbolo.

    `partir_anotacion` devuelve el cuerpo entero de la cabecera como simbolo —«Homalodisca
    vitripennis protein bicaudal C homolog 1-A»— porque para el cuarto campo de D48 eso
    alcanza. El recorte del organismo se hace **aca y no alla** porque es cosmetica de
    este parrafo —el organismo va en su propia frase y repetirlo se lee mal—, y
    `alertas.partir_anotacion` es codigo verificado del que cuelgan conteos publicados.
    La regla que si es regla, la del parentesis, sigue viviendo de aquel lado.
    """
    d = AL.partir_anotacion(anot.get("cabecera", ""))
    simbolo, organismo = d["simbolo"], (anot.get("organismo") or "").strip()
    if organismo and simbolo.lower().startswith(organismo.lower()):
        simbolo = simbolo[len(organismo):].strip()
    return simbolo, d["locus"]


def _falta(donde: dict, campos) -> list:
    return [c for c in campos if c not in donde or donde[c] is None or donde[c] == ""]


def validar(ficha: dict) -> None:
    """Si hay evidencia, tiene que estar entera. La primera falta aborta.

    `reciproco` es obligatorio aunque sea `False`: su ausencia y su negacion dicen cosas
    distintas, y publicar «no es un par reciproco» cuando nadie lo midio es exactamente el
    error que corrige la tercera correccion de `F1`.
    """
    anot = ficha.get("anotacion")
    if anot:
        faltan = _falta(anot, CAMPOS_ANOTACION)
        if faltan:
            raise FichaIncompleta(
                "la anotacion de %r no trae %s. Una anotacion transferida viaja siempre "
                "con su identidad y su banda de concordancia (F1); sin eso el parrafo "
                "miente por omision" % (ficha.get("locus", "?"), ", ".join(faltan)))
        faltan_b = _falta(anot["banda"], CAMPOS_BANDA)
        if faltan_b:
            raise FichaIncompleta("la banda de concordancia de %r no trae %s"
                                  % (ficha.get("locus", "?"), ", ".join(faltan_b)))
    for lista, campos in LISTAS.items():
        for i, item in enumerate(ficha.get(lista) or []):
            faltan_i = _falta(item, campos)
            if faltan_i:
                raise FichaIncompleta(
                    "la entrada %d de %s en %r no trae %s: sin fuente no entra al parrafo, "
                    "y tampoco se descarta en silencio"
                    % (i, lista, ficha.get("locus", "?"), ", ".join(faltan_i)))


def estado_de(ficha: dict) -> str:
    """Cual de los estados le toca al locus. Determinista y sin red."""
    validar(ficha)
    anot = ficha.get("anotacion")
    if not anot:
        return SIN_ANOTACION_DE_GEN
    simbolo, locus_ref = _simbolo_de(anot)
    # La regla de la cabecera sin parentesis, que vive en alertas.py: sin simbolo y sin
    # LOC no hay gen, hay un cromosoma.
    if not simbolo and not locus_ref:
        return SIN_ANOTACION_DE_GEN
    if not anot["reciproco"]:
        return ORTOLOGIA_NO_RECIPROCA
    bajo = simbolo.lower()
    if not bajo or bajo == locus_ref.lower() or any(p in bajo for p in NO_INFORMATIVOS):
        return ANOTACION_NO_INFORMATIVA
    return ANOTADA


def estado_seguro(ficha: dict) -> str:
    """El estado, o `ficha_incompleta` si la ficha no se puede leer.

    Es lo que usa el censo. Una sola ficha rota de `F1` no puede tirar abajo el recuento
    de 12.540 loci: eso seria filtrar por accidente justo lo que hay que contar.
    """
    try:
        return estado_de(ficha)
    except FichaIncompleta:
        return FICHA_INCOMPLETA


# ----------------------------------------------------------------- 2. la redaccion

def _num(valor) -> str:
    """Numero en la notacion del repositorio: coma decimal, sin separador de miles.

    El separador de miles se omite a proposito: «1.152» es ambiguo con un decimal y la
    verificacion de procedencia tendria que adivinar cual de las dos cosas es.
    """
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return str(valor)
    if isinstance(valor, int) or float(valor).is_integer():
        return str(int(valor))
    return ("%.1f" % float(valor)).replace(".", ",")


def _lista(piezas: list) -> str:
    if len(piezas) == 1:
        return piezas[0]
    return ", ".join(piezas[:-1]) + " y " + piezas[-1]


def _por_fuente(items: list, clave: str) -> list:
    """Agrupa las entradas por su fuente, conservando el orden de aparicion.

    Una frase por fuente. Mezclarlas pondria terminos de una base bajo la procedencia de
    otra, que es una afirmacion sin fuente con aspecto de afirmacion citada.
    """
    grupos: dict = {}
    for it in items:
        grupos.setdefault(it["fuente"], []).append("%s (%s)" % (it[clave], it["id"]))
    return list(grupos.items())


def fuentes_de(ficha: dict) -> set:
    """Los campos de procedencia que la ficha declara. Nada mas puede citarse como fuente.

    Sin esto, la verificacion aceptaba como fuente cualquier palabra que apareciera en la
    ficha —«oogenesis», sacada de la cita de un paper, pasaba— y una fuente que no es una
    fuente es peor que una frase sin fuente: parece verificada.
    """
    anot, fuentes = ficha.get("anotacion") or {}, set()
    for campo in ("accesion", "fuente_alineamiento"):
        if anot.get(campo):
            fuentes.add(anot[campo])
    if anot.get("banda", {}).get("fuente"):
        fuentes.add(anot["banda"]["fuente"])
    for lista, (_, campo) in LISTAS.items():
        for it in (ficha.get(lista) or []):
            if it.get(campo):
                fuentes.add(it[campo])
    return fuentes


def redactar(ficha: dict) -> dict:
    """Parrafo del locus, frase por frase y cada una con su fuente.

    Devuelve `{locus, estado, texto, frases, advertencia}`. `texto` es exactamente la
    union de las frases —no hay prosa suelta sin fuente— y `frases` es la lista de
    `{texto, fuente}`, que es la forma de «la fuente al lado» que pide el issue. Si el
    estado no es `anotada`, `frases` queda vacia y `texto` es el texto fijo.
    """
    estado = estado_de(ficha)
    base = {"locus": ficha.get("locus", ""), "estado": estado, "advertencia": ADVERTENCIA}
    if estado != ANOTADA:
        return dict(base, texto=TEXTO_DE[estado], frases=[])

    anot = ficha["anotacion"]
    simbolo, locus_ref = _simbolo_de(anot)
    banda = anot["banda"]
    frases = [
        {"texto": "El locus %s alinea con %s (%s) de %s."
                  % (ficha["locus"], simbolo, locus_ref, anot["organismo"]),
         "fuente": anot["accesion"]},
        {"texto": "El alineamiento tiene %s %% de identidad y %s %% de cobertura de la "
                  "proteina consulta, y es un par reciproco."
                  % (_num(anot["identidad"]), _num(anot["cobertura"])),
         "fuente": anot["fuente_alineamiento"]},
        {"texto": "En el tramo de identidad %s la concordancia de anotacion medida entre "
                  "dos cicadelidos es %s %%, con intervalo de confianza de %s a %s sobre "
                  "%s pares."
                  % (banda["tramo"], _num(banda["concordancia"]), _num(banda["ic"][0]),
                     _num(banda["ic"][1]), _num(banda["n"])),
         "fuente": banda["fuente"]},
    ]

    for fuente, piezas in _por_fuente(ficha.get("go") or [], "termino"):
        frases.append({
            "texto": "Los terminos de ontologia genica recuperados para ese ortologo son "
                     "%s." % _lista(piezas),
            "fuente": fuente})

    for fuente, piezas in _por_fuente(ficha.get("dominios") or [], "nombre"):
        frases.append({
            "texto": "Los dominios conservados anotados en ese ortologo son %s."
                     % _lista(piezas),
            "fuente": fuente})

    # La cita va literal. Resumirla con otras palabras seria generar, que es lo unico que
    # este modulo no hace; y la literalidad ya la verifica `agente_evidencia.py` aguas
    # arriba, contra el documento.
    for pap in (ficha.get("papers") or []):
        frases.append({
            "texto": "Sobre la funcion de ese gen, la literatura recuperada dice: «%s»."
                     % pap["cita"],
            "fuente": pap["doc_id"]})

    return dict(base, texto=" ".join(f["texto"] for f in frases), frases=frases)


# El vocabulario fijo de las plantillas de arriba: toda palabra que `redactar` pone y que
# no sale de la ficha. Es el complemento exacto de la verificacion —lo que no esta aca
# tiene que estar en la ficha— asi que cambiar una plantilla sin tocar esta lista hace
# fallar `test_evidencia_en_prosa.py` §4, que es el punto. El acoplamiento es a proposito:
# es el precio de que ninguna palabra entre al parrafo sin que alguien la haya declarado.
VOCABULARIO_DE_PLANTILLA = frozenset("""
el la los un una de en con y a es ese par
locus alinea alineamiento tiene identidad cobertura proteina consulta reciproco
tramo concordancia anotacion medida entre dos cicadelidos intervalo confianza sobre pares
terminos ontologia genica recuperados para ortologo son
dominios conservados anotados
funcion gen literatura recuperada dice
""".split())


# ------------------------------------------------------- 3. la verificacion de origen

_TOKEN = re.compile(r"[\w:.,\-]+", re.UNICODE)
_NUMERO = re.compile(r"\d")


def _tokens(texto: str) -> list:
    return [t for t in (b.strip(".,:-").lower() for b in _TOKEN.findall(texto or "")) if t]


def _recorrer(x, visitar) -> None:
    """Un solo recorrido de la ficha, para las palabras y para los numeros."""
    if isinstance(x, bool):
        return
    if isinstance(x, (int, float, str)):
        visitar(x)
    elif isinstance(x, dict):
        for v in x.values():
            _recorrer(v, visitar)
    elif isinstance(x, (list, tuple)):
        for v in x:
            _recorrer(v, visitar)


def _palabras_y_numeros(ficha: dict) -> tuple:
    """Las palabras y los numeros de los VALORES de la ficha, no de sus claves.

    La comparacion es por palabra entera y no por subcadena a proposito: «oge» esta
    adentro de «oogenesis» y un recorte asi pasaria un chequeo de subcadena diciendo otra
    cosa. Y se ignoran las claves del JSON —«anotacion», «cobertura», «papers»— porque son
    el nombre del casillero, no evidencia recuperada; dejarlas adentro le regalaria al
    redactor media docena de palabras tecnicas que nadie midio.
    """
    palabras, numeros = set(), set()

    def visitar(v):
        if isinstance(v, str):
            palabras.update(_tokens(v))
            for m in re.findall(r"\d+(?:[.,]\d+)?", v):
                numeros.add(float(m.replace(",", ".")))
        else:
            palabras.update(_tokens(_num(v)))
            palabras.update(_tokens(str(v)))
            numeros.add(float(v))

    _recorrer(ficha, visitar)
    return palabras, numeros


def verificar_procedencia(salida: dict, ficha: dict) -> dict:
    """Audita un parrafo contra su ficha. Determinista, y no mira quien lo escribio.

    Una palabra pasa si esta en el vocabulario fijo de la plantilla o si aparece en la
    ficha. Un numero pasa si su valor aparece en la ficha, aunque este escrito con coma
    decimal y la ficha lo tenga con punto. Una fuente pasa solo si es uno de los campos de
    procedencia que devuelve `fuentes_de()`. Lo que sobra se devuelve enumerado.

    **Lo que esto no hace**, y conviene que quede escrito al lado del codigo que lo hace:
    prueba que las piezas del parrafo salen de la ficha, no que la frase sea cierta ni que
    la fuente sostenga lo que la frase dice. Es el mismo limite declarado de
    `agente_evidencia.verificar`, y es el techo de lo que un script puede comprobar.
    """
    fuera_de_ficha, sin_fuente, invalidas, suelto = [], [], [], False
    estado = salida.get("estado")

    # Los estados sin parrafo se verifican por igualdad: el texto fijo, y nada mas.
    if estado != ANOTADA:
        suelto = salida.get("texto") != TEXTO_DE.get(estado) or bool(salida.get("frases"))
        return {"ok": not suelto, "fuera_de_ficha": [], "frases_sin_fuente": [],
                "fuentes_invalidas": [], "texto_fuera_de_frases": suelto}

    frases = salida.get("frases") or []
    suelto = salida.get("texto") != " ".join(f.get("texto", "") for f in frases)

    legitimas = fuentes_de(ficha)
    for i, f in enumerate(frases):
        fuente = (f.get("fuente") or "").strip()
        if not fuente:
            sin_fuente.append(i)
        elif fuente not in legitimas:
            invalidas.append(fuente)

    palabras, numeros = _palabras_y_numeros(ficha)
    for t in _tokens(salida.get("texto", "")):
        if t in VOCABULARIO_DE_PLANTILLA or t in palabras:
            continue
        if _NUMERO.search(t):
            try:
                if float(t.replace(",", ".")) in numeros:
                    continue
            except ValueError:
                pass
        fuera_de_ficha.append(t)

    return {"ok": not (fuera_de_ficha or sin_fuente or invalidas or suelto),
            "fuera_de_ficha": fuera_de_ficha, "frases_sin_fuente": sin_fuente,
            "fuentes_invalidas": invalidas, "texto_fuera_de_frases": suelto}


# ------------------------------------------------------------------------ el censo

def censo(fichas: list) -> dict:
    """Cuantos loci cayeron en cada estado. Los que no reciben parrafo se cuentan, no se
    filtran: una plataforma que los descarte en silencio sobredeclara su cobertura."""
    cuenta = {e: 0 for e in ESTADOS}
    for ficha in fichas:
        cuenta[estado_seguro(ficha)] += 1
    cuenta["total"] = sum(cuenta[e] for e in ESTADOS)
    cuenta["con_parrafo"] = cuenta[ANOTADA]
    cuenta["sin_parrafo"] = cuenta["total"] - cuenta[ANOTADA]
    return cuenta


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("fichas", type=Path, help="JSON con la lista de fichas de F1")
    ap.add_argument("--salida", type=Path, help="JSON de parrafos a escribir")
    ap.add_argument("--censo", action="store_true", help="solo el reparto por estado")
    args = ap.parse_args(argv)

    fichas = json.loads(args.fichas.read_text(encoding="utf-8"))
    cuenta = censo(fichas)
    for clave in ESTADOS + ("total", "con_parrafo", "sin_parrafo"):
        print("%-28s %6d" % (clave, cuenta[clave]))
    if args.censo:
        return 0

    parrafos, rotas = [], []
    for ficha in fichas:
        try:
            r = redactar(ficha)
        except FichaIncompleta as e:
            rotas.append(str(e))
            continue
        v = verificar_procedencia(r, ficha)
        if not v["ok"]:
            print("procedencia fallida en %s: %s" % (r["locus"], v), file=sys.stderr)
            return 1
        parrafos.append(r)
    for msg in rotas:
        print("ficha incompleta, sin parrafo: %s" % msg, file=sys.stderr)

    if args.salida:
        args.salida.write_text(json.dumps(parrafos, ensure_ascii=False, indent=2),
                               encoding="utf-8")
        print("escrito %s" % args.salida)
    else:
        for p in parrafos:
            print("\n%s\t%s\n%s" % (p["locus"], p["estado"], p["texto"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
