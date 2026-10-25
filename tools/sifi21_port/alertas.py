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


def escribir(filas: list[dict], ruta: Path, columnas: list[str]) -> None:
    """Escribe el TSV validando antes. Una fila incompleta no llega al disco."""
    validar(filas)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=columnas, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for f in filas:
            w.writerow(f)
