"""D48: la coincidencia perfecta de 21 nt es una alerta que obliga a justificar.

Este modulo **no decide**. Produce la fila que hace exigible el argumento y verifica
mecanicamente que la fila este completa; que el argumento sea bueno no lo puede
verificar ningun script, y esa es exactamente la contracara declarada de D48: «un
parrafo puede estar mal escrito de un modo en que un booleano no puede».

Los cuatro campos obligatorios son los que enumera el investigador `[R]`:

  1. `organismo`          que organismo es, con su rol en el panel.
  2. `exposicion`         su posibilidad de exposicion. **No se reinventa**: sale de
                          `ejes_separados.PANEL_EJES`, que es donde M5 dejo el peso y su
                          motivo por referencia. El de *H. vitripennis* es una decision
                          abierta del usuario (pedido 4 del lunes), asi que la fila lleva
                          los dos valores —el de D47 y el de D18— y **no hay que
                          recalcular la tabla** para leerla con cualquiera de los dos.
  3. `gen_involucrado`    que gen esta involucrado. Es el unico campo que no estaba en el
                          dato: `offtarget_21nt.escanear_con_identidad()` conserva la
                          accesion y la cabecera del FASTA de referencia trae el nombre,
                          el LOC y el tipo de molecula. Todo de disco.
  4. `evidencia_biologica` que evidencia biologica hay. Lleva una clave de vocabulario
                          cerrado —que el script si puede verificar— y la prosa, que no.

Granularidad de la fila: **region x organismo x gen**, con los transcriptos de ese gen
en una columna y el conteo de ventanas por umbral. El motivo esta medido y es lo que
cambia respecto de la sonda del prompt: para los aciertos de 21/21 las dos
granularidades coinciden porque todos caen en un solo transcripto, pero para el bloque
de >= 19 nt no, y la diferencia es de isoformas del MISMO gen —ocho transcriptos de
`SLC24A4` para las tres ventanas de `BicC_Dm` 2121-2420, tres variantes de la misma
esterasa de maiz para `BicC_Dm` 264-563—. Una fila por ventana x transcripto pediria
veinticuatro parrafos identicos para un solo gen humano. La tabla por ventana se
conserva igual, en `resultados/alertas_por_ventana.tsv`.

Los dos umbrales de D28 van **siempre los dos** y estan anidados por construccion: toda
ventana con 21/21 perfecto tiene tambien un bloque perfecto de >= 19 nt. Y todo conteo
va en dos cifras por D59: el total y cuanto de ese total es de baja complejidad.
"""

from __future__ import annotations

import csv
from pathlib import Path

CAMPOS_OBLIGATORIOS = ("organismo", "exposicion", "gen_involucrado", "evidencia_biologica")

# Las columnas que materializan cada campo obligatorio. Una fila esta completa cuando
# TODAS las columnas de los cuatro campos tienen contenido; falta una y es error.
COLUMNAS_DE = {
    "organismo": ("organismo_corto", "organismo_especie", "organismo_rol"),
    "exposicion": ("exposicion_w", "exposicion_w_alternativa", "exposicion_motivo",
                   "exposicion_fuente", "exposicion_decision_abierta"),
    "gen_involucrado": ("gen_simbolo", "gen_locus", "gen_tipo_molecula",
                        "gen_transcriptos", "gen_anotacion", "gen_fuente"),
    "evidencia_biologica": ("evidencia_clave", "evidencia_bioensayo", "evidencia_prosa"),
}

# Vocabulario cerrado del cuarto campo. Lo que el script puede verificar es que la clave
# sea una de estas y que la prosa exista; lo que NO puede verificar es si la prosa dice
# algo cierto, algo pertinente o algo suficiente.
CLAVES_EVIDENCIA = (
    "ortologo_del_blanco",       # el gen impactado es el ortologo del gen que se silencia
    "gen_no_relacionado",        # gen anotado, sin relacion funcional con el blanco
    "sin_anotacion_de_gen",      # el acierto cae en ensamblado genomico sin anotacion
)
CLAVES_BIOENSAYO = (
    "sin_bioensayo_consultado",  # no se abrio ninguna fuente experimental para esta fila
    "bioensayo_citado",          # hay fuente abierta, y va en `evidencia_prosa`
)
PROSA_MINIMA = 40  # caracteres; un campo de una palabra no es una justificacion

# Como se reconoce el ortologo del blanco en la anotacion de la referencia. Explicito y
# auditable a proposito: es una regla nuestra `[H]` sobre texto de cabecera, no una
# inferencia de homologia por alineamiento.
ORTOLOGO_DE = {
    "BicC_Dm": ("bicaudal c",),
    "ATPaseD_Dm": ("v-type proton atpase subunit d",),
    "eth_Dm": ("ecdysis triggering hormone", "ecdysis-triggering hormone"),
    "bursA_Dm": ("bursicon",),
    "MP_MRFV": (),   # proteina viral: ningun gen del hospedador es su ortologo
    "CP_MRFV": (),
}


class FilaIncompleta(ValueError):
    """Una fila de alerta sin los cuatro campos. No es una celda vacia: es un error."""


def _vacio(v) -> bool:
    return v is None or (isinstance(v, str) and not v.strip())


def validar_fila(fila: dict) -> None:
    """Levanta `FilaIncompleta` si falta cualquiera de los cuatro campos obligatorios.

    Verifica, en este orden: que esten todas las columnas de los cuatro campos y no
    vacias; que `evidencia_clave` y `evidencia_bioensayo` esten en el vocabulario
    cerrado; y que `evidencia_prosa` tenga al menos `PROSA_MINIMA` caracteres. Lo que
    no verifica —y el informe lo dice— es si la prosa es verdadera o suficiente.
    """
    faltan = []
    for campo in CAMPOS_OBLIGATORIOS:
        for col in COLUMNAS_DE[campo]:
            if col not in fila or _vacio(fila.get(col)):
                faltan.append("%s/%s" % (campo, col))
    if faltan:
        raise FilaIncompleta(
            "fila de alerta incompleta (%s, %s): faltan %s. Los cuatro campos de D48 son "
            "obligatorios: %s" % (fila.get("gen", "?"), fila.get("region", "?"),
                                  ", ".join(faltan), ", ".join(CAMPOS_OBLIGATORIOS)))
    if fila["evidencia_clave"] not in CLAVES_EVIDENCIA:
        raise FilaIncompleta("evidencia_clave %r no esta en el vocabulario cerrado %s"
                             % (fila["evidencia_clave"], CLAVES_EVIDENCIA))
    if fila["evidencia_bioensayo"] not in CLAVES_BIOENSAYO:
        raise FilaIncompleta("evidencia_bioensayo %r no esta en el vocabulario cerrado %s"
                             % (fila["evidencia_bioensayo"], CLAVES_BIOENSAYO))
    if len(str(fila["evidencia_prosa"]).strip()) < PROSA_MINIMA:
        raise FilaIncompleta(
            "evidencia_prosa de (%s, %s) tiene %d caracteres y el minimo es %d: una "
            "palabra no es una justificacion" % (fila.get("gen", "?"), fila.get("region", "?"),
                                                 len(str(fila["evidencia_prosa"]).strip()),
                                                 PROSA_MINIMA))


def validar(filas: list[dict]) -> int:
    """Valida todas las filas. Devuelve cuantas pasaron; la primera incompleta aborta."""
    for f in filas:
        validar_fila(f)
    return len(filas)


# ------------------------------------------------------------------ campos 3 y 4

def partir_anotacion(anotacion: str) -> dict:
    """Simbolo, LOC y tipo de molecula de una cabecera de RefSeq, leidos de disco.

    `PREDICTED: Homalodisca vitripennis protein bicaudal C homolog 1-A (LOC124362408),
    mRNA` -> simbolo «protein bicaudal C homolog 1-A», locus «LOC124362408», molecula
    «mRNA». Si la cabecera no tiene parentesis —el ensamblado genomico del vector, que
    no esta anotado— el simbolo queda vacio y el tipo es el texto de la cabecera.
    """
    txt = (anotacion or "").strip()
    if not txt:
        return {"simbolo": "", "locus": "", "molecula": ""}
    partes = [p.strip() for p in txt.split(",")]
    cuerpo = partes[0]
    molecula = partes[-1] if len(partes) > 1 else ""
    # la variante de transcripto no es parte del nombre del gen
    if len(partes) > 2 and partes[-2].startswith("transcript variant"):
        molecula = partes[-1]
    # El simbolo del gen es lo que va ANTES del parentesis, y el LOC o el simbolo
    # oficial es lo que va adentro. Una cabecera sin parentesis no es un transcripto
    # anotado —el ensamblado genomico del vector dice «Dalbulus maidis genome assembly,
    # chromosome: 6»— y en ese caso **no hay gen**: el campo queda vacio a proposito y
    # `clasificar_evidencia` lo marca como `sin_anotacion_de_gen`. Inventarle un simbolo
    # al cromosoma seria el peor error posible en el cuarto campo de D48.
    simbolo, locus = "", ""
    if cuerpo.endswith(")") and "(" in cuerpo:
        simbolo, locus = cuerpo.rsplit("(", 1)[0].strip(), cuerpo.rsplit("(", 1)[1][:-1]
        if simbolo.startswith("PREDICTED: "):
            simbolo = simbolo[len("PREDICTED: "):]
    else:
        molecula = txt
    return {"simbolo": simbolo, "locus": locus, "molecula": molecula}


def clave_de_gen(corto: str, anotacion: str, transcripto: str) -> str:
    """Identidad del gen impactado, para agrupar isoformas del mismo gen en una fila."""
    d = partir_anotacion(anotacion)
    if d["locus"]:
        return "%s|%s" % (corto, d["locus"])
    if d["simbolo"]:
        return "%s|%s" % (corto, d["simbolo"])
    return "%s|%s" % (corto, transcripto)


def clasificar_evidencia(gen_blanco: str, anotacion: str) -> str:
    """Clave del cuarto campo a partir de la anotacion de disco. Regla nuestra `[H]`."""
    d = partir_anotacion(anotacion)
    if not d["locus"] and not d["simbolo"]:
        return "sin_anotacion_de_gen"
    texto = (d["simbolo"] or "").lower()
    for pista in ORTOLOGO_DE.get(gen_blanco, ()):
        if pista in texto:
            return "ortologo_del_blanco"
    return "gen_no_relacionado"


# ------------------------------------------------- la compuerta que D48 deja abierta

# D48 retira el veto automatico y con eso **invierte el default**: la compuerta
# descartaba por omision y la tabla no descarta nada, asi que una alerta **no leida**
# queda operativamente igual que una alerta aceptada. M6 lo midio y lo dejo declarado
# como lo que no puede hacer cumplir el software. Esto es lo minimo que si puede: negarse
# a tratar una region como usable mientras alguna de sus filas siga sin decidir.
#
# Lo que esto NO hace, y conviene que quede escrito al lado del codigo que lo hace:
#   * no decide que alertas se aceptan. Eso es del usuario y es el punto entero de D48;
#   * no verifica si la justificacion es cierta, pertinente ni suficiente;
#   * no dice nada sobre el riesgo de una region que **si** esta tamizada y sin aciertos:
#     «sin alertas en este umbral» es una medicion del tamizado, no un certificado.
#
# Lo que hasta D71 tampoco hacia, y D72 cierra: distinguir «se tamizo y no hay alertas» de
# «no se tamizo». Una region sin filas en la tabla pasaba como «sin alertas», que es cierto
# para una region tamizada sin aciertos y falso para una que nunca se tamizo, porque las
# dos se ven igual desde `alertas.tsv`. Desde D72 la compuerta pide **tambien** el
# inventario de regiones tamizadas —`resultados/estado_regiones.tsv`, que es la otra salida
# del mismo generador y la unica que puede decir «tamizada, cero aciertos»— y una region
# ausente de ese inventario levanta `RegionNoTamizada`. El parametro `inventario` es
# **obligatorio y por nombre** a proposito: la unica forma de equivocarse seria llamar a la
# compuerta sin declarar contra que inventario se exige presencia, y eso ahora es un
# `TypeError` ruidoso en vez de un pase silencioso.
#
# Desde D69 **si esta adoptada**: la llama `ranking.region_recomendada()`, que es el unico
# lugar del port donde el primer puesto de `alternativas()` se convierte en una region
# recomendada, con el umbral `perfecto_21` por defecto (D48 literal) y configurable.
#
# Y lo que D77 agrega: la compuerta **sabe contra que panel se le pregunta**. Hasta
# entonces consultaba la tabla entera sin poder saber que referencias tenia la corrida que
# la llamaba, y eso tiene un caso concreto en el repositorio: la rama `sin_humano` de
# `ranking_v2.efecto_humano()` evaluaba sus regiones contra filas de *Homo sapiens* que esa
# misma rama habia sacado del panel. Lo que D77 **no** hace es filtrarlas: una alerta de un
# organismo fuera del panel frena igual, porque la coincidencia perfecta es una propiedad
# del ARN que se sintetizaria y no del panel con el que una corrida lo puntua. Lo que hace
# es que el estado y el mensaje la nombren, para que frenar por una referencia que la
# corrida no mira sea una decision leida y no una sorpresa.

DECISIONES = ("pendiente", "aceptada", "bloqueante")
# El texto con el que sale la tabla recien construida. Reescribir una palabra no es decidir.
MARCA_PENDIENTE = "pendiente"


class CompuertaCerrada(RuntimeError):
    """La compuerta no deja pasar la region. Base de las dos formas de no pasar.

    Existe para que quien llame pueda atajar las dos con una clausula, sin que por eso
    se confundan: no son el mismo hecho y no se arreglan igual. La subclase dice cual es.
    """


class AlertaSinDecidir(CompuertaCerrada):
    """Se trato como usable una region con alertas que nadie decidio todavia.

    No es lo mismo que «la region esta bloqueada»: es que **no se sabe**, y bajo D48 no
    saber tiene que costar algo, porque si no una alerta no leida vale lo mismo que una
    aceptada.
    """


class RegionNoTamizada(CompuertaCerrada):
    """Se trato como usable una region que nunca se tamizo (D72).

    Tampoco es «la region esta bloqueada», y sobre todo **no es** «la region no tiene
    alertas»: es que no hay medicion. La diferencia no se puede leer de `alertas.tsv`,
    porque una region tamizada sin aciertos y una region nunca tamizada tienen las mismas
    cero filas; de ahi que la compuerta pida el inventario aparte.
    """


def cita_la_fila(fila: dict, texto: str) -> bool:
    """D48 pide que la justificacion «cite la fila». Verificable: que la nombre.

    Alcanza con que mencione el LOC del gen impactado o una de las accesiones de
    transcripto de esa fila. Es un piso mecanico y deliberadamente grosero —se puede
    cumplir pegando una accesion— pero distingue una justificacion escrita **sobre esta
    fila** de un parrafo generico copiado a todas.
    """
    t = (texto or "")
    candidatos = [c for c in [fila.get("gen_locus", "")] if c and not c.startswith("(")]
    candidatos += [a.strip() for a in (fila.get("gen_transcriptos") or "").split(",") if a.strip()]
    return any(c in t for c in candidatos)


def validar_decision(fila: dict) -> None:
    """Valida el par (decision, justificacion) de una fila ya completa.

    `pendiente` es un estado legitimo y no falla: la tabla se entrega asi a proposito.
    Lo que falla es **decidir sin justificar**, que es la forma de aceptar una alerta
    reescribiendo una palabra.
    """
    d = (fila.get("decision_usuario") or "").strip()
    if d not in DECISIONES:
        raise FilaIncompleta("decision_usuario %r no esta en el vocabulario cerrado %s"
                             % (d, DECISIONES))
    if d == MARCA_PENDIENTE:
        return
    j = (fila.get("justificacion_usuario") or "").strip()
    donde = "%s %s / %s" % (fila.get("gen", "?"), fila.get("region", "?"),
                            fila.get("organismo_corto", "?"))
    if j.startswith(MARCA_PENDIENTE):
        raise FilaIncompleta(
            "la fila (%s) dice '%s' pero su justificacion sigue siendo el texto de "
            "relleno. D48 pide una justificacion escrita, no cambiar una palabra." % (donde, d))
    if len(j) < PROSA_MINIMA:
        raise FilaIncompleta(
            "la justificacion de (%s) tiene %d caracteres y el minimo es %d: una palabra "
            "no es una justificacion" % (donde, len(j), PROSA_MINIMA))
    if not cita_la_fila(fila, j):
        raise FilaIncompleta(
            "la justificacion de (%s) no cita la fila: tiene que nombrar el LOC o una de "
            "las accesiones (%s). D48 pide que la justificacion cite la fila."
            % (donde, fila.get("gen_transcriptos", "")))


# --------------------------------------------------------------------- persistencia
#
# El problema que resuelve esta seccion es banal y por eso peligroso: `tabla_alertas.py`
# reconstruye `alertas.tsv` desde cero en cada corrida y escribia `decision_usuario =
# "pendiente"` fijo. Una firma escrita a mano sobre esa tabla se pierde la proxima vez
# que alguien corre el script, sin aviso y sin diff que lo explique, porque el archivo
# vuelve a su estado de fabrica. O sea: el mecanismo que D48 monta para que no saber
# cueste algo se desarmaba solo.
#
# La firma vive entonces en un archivo aparte —la tabla es salida, la firma es entrada—
# y se vuelca sobre las filas generadas. Las dos formas de fallar estan cerradas:
#
#   * una firma que no corresponde a ninguna fila (`FirmaHuerfana`) significa que la
#     tabla cambio debajo de la firma: la region se retiro, el organismo salio del panel
#     o el gen impactado es otro. Pasarla por alto dejaria una firma apuntando a nada;
#   * una firma cuya huella no coincide con la fila (`FirmaVencida`) significa que los
#     conteos de esa fila cambiaron desde que se firmo. Una fila que pasa de 0 a 5
#     coincidencias perfectas **no es la fila que alguien acepto**, y heredar el
#     «aceptada» seria exactamente el default invertido que D48 vino a corregir.
#
# Las dos levantan en vez de avisar. Es fail-closed a proposito: el costo de equivocarse
# es volver a firmar una fila, y el de no hacerlo es publicar una region con una alerta
# que nadie leyo.

COLUMNAS_DECISION = ("gen", "region", "organismo_corto", "gen_locus",
                     "huella_21", "huella_ge19", "firmado_por", "fecha",
                     "decision_usuario", "justificacion_usuario")


class FirmaHuerfana(ValueError):
    """Hay una firma para una fila que la tabla ya no produce."""


class FirmaVencida(ValueError):
    """La fila que se firmo y la que la tabla produce hoy no tienen los mismos conteos."""


def clave_de(fila: dict) -> tuple:
    """La identidad de una fila de alerta: region x organismo x **gen impactado**.

    Los cuatro campos hacen falta, y el cuarto no es decorativo: en `ATPaseD_Dm` 72-371
    hay **dos** filas de *Homo sapiens* —`LOC107984331` y `PDE1C`— y lo mismo en 137-436.
    Una clave de region x organismo las fusiona, y fusionarlas significa firmar una y
    que la otra herede la firma sin que nadie la haya leido, que es justo el modo de
    fallar que D48 quiere cerrar. Es ademas la granularidad que el modulo declara arriba.

    Que una reanotacion de la referencia mueva el acierto a otro LOC deja la firma
    huerfana, y eso **tambien** es lo correcto: el gen impactado es la mitad del
    argumento, asi que si cambia hay que volver a escribirlo.
    """
    return (fila.get("gen"), fila.get("region"), fila.get("organismo_corto"),
            (fila.get("gen_locus") or "").strip())


def huella_de(fila: dict) -> tuple:
    """Lo que tiene que seguir siendo cierto para que una firma siga valiendo.

    Los dos conteos de D28. No la prosa de evidencia, que se puede reescribir sin que
    cambie el hecho, ni las posiciones, que se mueven si la region se corre un nucleotido
    sin que cambie el riesgo. El gen impactado no esta aca porque ya esta en la clave.
    """
    return (str(fila.get("ventanas_perfecto_21", "")).strip(),
            str(fila.get("ventanas_perfecto_ge19", "")).strip())


def huella_firmada(firma: dict) -> tuple:
    """La misma huella, leida de la fila de firma, donde las columnas se llaman distinto.

    Son dos funciones y no una con heuristica a proposito: una fila de alerta y una de
    firma son dos formatos distintos, y adivinar cual es cual por las columnas presentes
    es la clase de atajo que falla en silencio el dia que un formato gana una columna.
    """
    return (str(firma.get("huella_21", "")).strip(),
            str(firma.get("huella_ge19", "")).strip())


def leer_decisiones(ruta) -> dict:
    """Lee el archivo de firmas. Devuelve {clave: fila de firma}. No valida contra nada.

    Un archivo que no existe no es un error: es el estado inicial, en el que las
    diecisiete filas salen en «pendiente», que es como la tabla se entrego.
    """
    ruta = Path(ruta)
    if not ruta.exists():
        return {}
    with ruta.open(encoding="utf-8") as fh:
        crudas = [f for f in csv.DictReader(fh, delimiter="\t")
                  if (f.get("gen") or "").strip() and not (f.get("gen") or "").startswith("#")]
    out = {}
    for f in crudas:
        k = clave_de(f)
        if k in out:
            raise FilaIncompleta("hay dos firmas para la misma fila %s en %s" % (k, ruta))
        out[k] = f
    return out


def aplicar_decisiones(filas: list[dict], decisiones: dict) -> dict:
    """Vuelca las firmas sobre las filas generadas y valida el resultado.

    Una fila sin firma queda en «pendiente» con su texto de relleno, que es el estado de
    fabrica y es legitimo. Una fila con firma queda decidida y pasa por
    `validar_decision`, de modo que una firma mal escrita —sin prosa, o sin citar la
    fila— aborta la corrida en vez de llegar al disco.
    """
    usadas, aplicadas = set(), 0
    for fila in filas:
        k = clave_de(fila)
        firma = decisiones.get(k)
        if firma is None:
            fila["decision_usuario"] = MARCA_PENDIENTE
            fila["justificacion_usuario"] = "pendiente: la escribe el usuario, no el motor"
            continue
        usadas.add(k)
        esperada, actual = huella_firmada(firma), huella_de(fila)
        if esperada != actual:
            raise FirmaVencida(
                "la firma de %s %s / %s / %s se escribio sobre una fila con 21/21=%s y "
                ">=19=%s, y hoy la fila tiene 21/21=%s y >=19=%s. No es la misma fila: hay "
                "que volver a leerla y volver a firmarla." % (k + esperada + actual))
        fila["decision_usuario"] = (firma.get("decision_usuario") or "").strip()
        fila["justificacion_usuario"] = (firma.get("justificacion_usuario") or "").strip()
        validar_decision(fila)
        aplicadas += 1
    huerfanas = sorted(set(decisiones) - usadas)
    if huerfanas:
        raise FirmaHuerfana(
            "hay %d firma(s) que no corresponden a ninguna fila de la tabla: %s. La tabla "
            "cambio debajo de la firma; hay que revisarlas antes de seguir."
            % (len(huerfanas), ", ".join("%s %s / %s / %s" % h for h in huerfanas)))
    pendientes = [f for f in filas if (f.get("decision_usuario") or "") == MARCA_PENDIENTE]
    return {"filas": len(filas), "firmadas": aplicadas, "pendientes": len(pendientes),
            "sin_firma": sorted(clave_de(f) for f in pendientes)}


def filas_de_region(filas: list[dict], gen: str, region: str) -> list[dict]:
    return [f for f in filas if f.get("gen") == gen and f.get("region") == region]


def fuera_del_panel(fila: dict, panel: set | None) -> bool:
    """Si la fila es de un organismo que el panel de la corrida no tiene (D77).

    Un solo predicado, llamado desde los dos lados —el conteo y el mensaje—, por el mismo
    motivo que M9 dejo escrito: un filtro que vive en un camino y no en el otro no es un
    filtro. `panel` en `None` es «no se declaro panel» y entonces ninguna fila esta fuera;
    un panel vacio declarado deja a todas afuera, y la diferencia es deliberada.
    """
    if panel is None:
        return False
    return (fila.get("organismo_corto") or "").strip() not in panel


def estado_decision(filas: list[dict], gen: str, region: str,
                    umbral: str = "perfecto_21", panel: set | None = None) -> dict:
    """Estado de decision de una region. **No** dice si la region sirve ni si es segura.

    `umbral` elige que alertas obligan a justificar. Por defecto `perfecto_21`, que es lo
    que D48 dice literalmente —«cada coincidencia perfecta de 21 nt ... genera una fila»—;
    con `perfecto_ge19` obligan tambien las del umbral laxo de D28, que la tabla informa
    al lado pero sobre las que D48 no se pronuncia. Los dos numeros valen la pena y por
    eso el umbral es un parametro y no una constante.

    `panel` es el conjunto de `organismo_corto` que la corrida que pregunta tiene en su
    panel de referencias. Es **solo informativo** y por decision escrita (D77): las filas
    de un organismo que la corrida excluyo cuentan igual para `pendientes` y para el
    estado, porque la coincidencia es una propiedad del ARN y no del panel con el que se
    la puntua. Lo que el panel agrega es que el estado pueda **nombrar** esas filas en vez
    de que la inconsistencia quede muda: `None` —el default— es «no se declaro panel» y
    deja las dos listas vacias.
    """
    if umbral not in ("perfecto_21", "perfecto_ge19"):
        raise ValueError("umbral %r: los de D28 son perfecto_21 y perfecto_ge19" % umbral)
    col = "ventanas_%s" % umbral
    mias = [f for f in filas_de_region(filas, gen, region) if int(f.get(col) or 0) > 0]
    for f in mias:
        validar_decision(f)
    pendientes = [f for f in mias if (f.get("decision_usuario") or "").strip() == MARCA_PENDIENTE]
    bloqueantes = [f for f in mias if (f.get("decision_usuario") or "").strip() == "bloqueante"]
    filas_fuera = [f for f in mias if fuera_del_panel(f, panel)]
    pend_fuera = [f for f in pendientes if fuera_del_panel(f, panel)]
    if not mias:
        estado = "sin alertas en este umbral"
    elif pendientes:
        estado = "sin decidir"
    elif bloqueantes:
        estado = "decidida: bloqueante"
    else:
        estado = "decidida: aceptada con justificacion"
    return {"gen": gen, "region": region, "umbral": umbral, "alertas": len(mias),
            "pendientes": len(pendientes), "bloqueantes": len(bloqueantes),
            "estado": estado,
            "organismos_pendientes": sorted({f["organismo_corto"] for f in pendientes}),
            "decide": "el usuario" if pendientes else "ya decidido",
            # D77: contra que panel se pregunto, y que filas son de un organismo que ese
            # panel no tiene. `panel` en `None` es «no se declaro», que no es lo mismo que
            # «el panel esta vacio»: con panel vacio toda fila queda fuera.
            "panel": None if panel is None else sorted(panel),
            "organismos_fuera_del_panel": sorted({f["organismo_corto"] for f in filas_fuera}),
            "pendientes_fuera_del_panel": sorted({f["organismo_corto"] for f in pend_fuera})}


def leer_inventario(ruta) -> set:
    """El inventario de regiones tamizadas, leido de `estado_regiones.tsv` (D72).

    Devuelve `{(gen, region)}`. Es la otra salida de `tabla_alertas.py` y la unica que
    distingue «tamizada, cero aciertos» de «nunca tamizada»: `alertas.tsv` no puede,
    porque los dos casos tienen las mismas cero filas.

    Un archivo que no existe **si** es un error, y ahi esta la asimetria con
    `leer_decisiones()`: sin firmas el estado inicial legitimo es «todo pendiente», pero
    sin inventario no hay estado inicial legitimo —un inventario vacio haria pasar a toda
    region como tamizada, que es el modo de fallar en silencio que D72 cierra—.
    """
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(
            "no esta el inventario de regiones tamizadas (%s) y sin el la compuerta no "
            "puede distinguir «se tamizo y no hay alertas» de «no se tamizo» (D72). Corre "
            "research/ola4/M6_alertas/scripts/tabla_alertas.py." % ruta)
    with ruta.open(encoding="utf-8") as fh:
        return {((f.get("gen") or "").strip(), (f.get("region") or "").strip())
                for f in csv.DictReader(fh, delimiter="\t")
                if (f.get("gen") or "").strip()}


def exigir_decidida(filas: list[dict], gen: str, region: str,
                    umbral: str = "perfecto_21", *, inventario,
                    panel: set | None = None) -> dict:
    """Puerta: la region tiene que estar tamizada (D72) y sin alertas sin decidir (D48).

    Levanta `RegionNoTamizada` si la region no esta en `inventario`, y
    `AlertaSinDecidir` si esta tamizada pero le queda una alerta en «pendiente». Las dos
    heredan de `CompuertaCerrada`.

    El orden importa y es el de D70: primero presencia, despues decision. Preguntar por
    las filas de una region que nunca se tamizo no tiene respuesta —no hay cero alertas,
    hay cero mediciones— y contestar «sin alertas en este umbral» seria afirmar lo que no
    se midio.

    `inventario` es el conjunto de `(gen, region)` tamizados, normalmente el que devuelve
    `leer_inventario()`. Es **obligatorio y por nombre**: una compuerta cuyo parametro de
    presencia tiene default se puede desactivar olvidandolo, y olvidarlo tiene que ser un
    `TypeError` y no un pase. Esa es la misma razon por la que D69 hizo que una tabla
    ausente falle cerrada.

    Una region tamizada **sin alertas** pasa, y eso no es una laguna: se la miro y no hay
    nada que justificar. Una region con alertas **todas decididas** pasa tambien, incluso
    si alguna es `bloqueante` —quien llama decide que hacer con eso, y el estado se lo
    dice—. Lo unico que esta funcion impide es seguir de largo sin que nadie haya mirado,
    y desde D72 tambien sin que nadie haya medido.

    `panel` —los `organismo_corto` que la corrida que pregunta tiene en su panel— **no
    cambia que frena** (D77): una alerta de un organismo que esa corrida excluyo frena
    igual, porque la coincidencia perfecta esta en el ARN que se va a sintetizar y no en
    el panel con el que esa corrida lo puntua. Lo que cambia es que el mensaje lo diga con
    todas las letras, que es lo que faltaba: hasta D77 la compuerta no podia saber contra
    que panel se le preguntaba, asi que una corrida frenada por una alerta de un organismo
    que no estaba mirando no tenia forma de enterarse de por que.
    """
    if (gen, region) not in set(inventario):
        raise RegionNoTamizada(
            "%s %s no esta en el inventario de regiones tamizadas (%d regiones) y no se "
            "puede tratar como usable: cero filas de alerta es «no se tamizo», no «se "
            "tamizo y no hay alertas» (D70, D72). Agregala a REGIONES en "
            "research/ola4/M6_alertas/scripts/tabla_alertas.py y corre el script."
            % (gen, region, len(set(inventario))))
    est = estado_decision(filas, gen, region, umbral, panel)
    if est["pendientes"]:
        # D77: si alguna de las pendientes es de un organismo que esta corrida no tiene en
        # el panel, la compuerta frena igual y **lo dice**. Frenar sin decirlo era el modo
        # de fallar que esto cierra: correcto para el umbral, incompresible para el que
        # corre.
        organismos_fuera = est["pendientes_fuera_del_panel"]
        nota = ""
        if organismos_fuera:
            nota = (" De esas, %s %s de un organismo que esta corrida NO tiene en el panel "
                    "(%s): frena igual porque la coincidencia perfecta esta en el ARN y no "
                    "en el panel con el que se lo puntua (D77)."
                    % (", ".join(organismos_fuera),
                       "es" if len(organismos_fuera) == 1 else "son",
                       ", ".join(est["panel"] or ["panel vacio"])))
        raise AlertaSinDecidir(
            "%s %s tiene %d alerta(s) de %s sin decidir (%s) y no se puede tratar como "
            "usable: D48 pide que la region se acepte o se descarte con una justificacion "
            "escrita que cite la fila. Ver research/ola4/M6_alertas/resultados/alertas.tsv%s"
            % (gen, region, est["pendientes"], umbral,
               ", ".join(est["organismos_pendientes"]), nota))
    return est


def regiones_sin_decidir(filas: list[dict], umbral: str = "perfecto_21") -> list[dict]:
    """Inventario de lo que falta decidir, para mirarlo de una sola vez."""
    vistas, out = [], []
    for f in filas:
        clave = (f.get("gen"), f.get("region"))
        if clave in vistas:
            continue
        vistas.append(clave)
        out.append(estado_decision(filas, clave[0], clave[1], umbral))
    return out


def leer(ruta: Path) -> list[dict]:
    """Lee `alertas.tsv` y valida las filas. No decide nada."""
    with Path(ruta).open(encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh, delimiter="\t"))
    validar(filas)
    for f in filas:
        validar_decision(f)
    return filas


def escribir(filas: list[dict], ruta: Path, columnas: list[str]) -> None:
    """Escribe el TSV validando antes. Una fila incompleta no llega al disco."""
    validar(filas)
    for f in filas:
        validar_decision(f)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=columnas, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for f in filas:
            w.writerow(f)
