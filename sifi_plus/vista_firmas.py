"""Vista D: la bandeja de firmas del inventario de alertas. La unica vista que escribe.

Una bandeja de entrada sin interfaz es un TSV que nadie firma. D48 reemplazo la compuerta
booleana del veto por una tabla de alertas: cada coincidencia perfecta de 21 nt genera una fila
con cuatro campos obligatorios, y la region no se descarta por tenerla —se acepta o se descarta
con una justificacion escrita que cita la fila—. El motor completa los cuatro campos y deja
`decision_usuario` y `justificacion_usuario` vacias **a proposito**: firmar es del equipo, no
del motor.

**Donde escribe, y por que no donde se lee.** La firma va a
`research/ola4/M6_alertas/decisiones.tsv`, que es **entrada** del generador y no salida suya
(D68). El inventario `alertas.tsv` se regenera desde ahi corriendo `tabla_alertas.py`. Esta
vista **no edita el inventario en el lugar**: es el resultado de otra linea, y una firma escrita
encima se perderia sin aviso la proxima vez que alguien corra el generador, que es exactamente
el modo de fallar que D68 vino a cerrar.

Es tambien la unica cosa que esta carpeta escribe **dentro** del control de versiones. Todo lo
demas va a `work/sifi_plus/`; la firma se versiona porque es una decision del equipo y no una
salida de computo, y no lleva secuencia.

**La huella.** Cada firma guarda los dos conteos de D28 de la fila que el firmante tenia
delante. Si manana esos conteos cambian, la firma **no es de esta fila** y el generador levanta
`FirmaVencida`. La vista la escribe leyendola de la fila que muestra, que es la unica forma de
que la firma quede atada a lo que se leyo.

**Las constantes de validacion estan duplicadas a proposito**, porque esta vista no puede
importar `tools/sifi21_port/alertas.py` —la linea no toca el motor— y el generador no puede
importar la interfaz. El riesgo de que las dos copias se separen se cubre con una verificacion
de `test_api.py` que compara las constantes de los dos modulos leyendo el archivo del motor como
texto, sin importarlo. Si alguien cambia una de las dos, esa verificacion falla.

**Esta linea no firma ninguna alerta.** Construye la bandeja; firmar es del equipo.
"""

from __future__ import annotations

import csv
import datetime as _dt
import os
import re
import tempfile
from pathlib import Path

from lectura import NO_APLICA, NO_DECLARADA, entero, leer_tsv, procedencia, rel
from lectura import RAIZ

M6 = RAIZ / "research" / "ola4" / "M6_alertas"
INVENTARIO = M6 / "resultados" / "alertas.tsv"
ESTADO_REGIONES = M6 / "resultados" / "estado_regiones.tsv"
FIRMAS = M6 / "decisiones.tsv"
COMANDO = "python research/ola4/M6_alertas/scripts/tabla_alertas.py"

# --- lo que esta duplicado del motor, y que test_api.py verifica contra el ---------------

DECISIONES = ("pendiente", "aceptada", "bloqueante")
MARCA_PENDIENTE = "pendiente"
PROSA_MINIMA = 40  # caracteres; un campo de una palabra no es una justificacion
COLUMNAS_DECISION = ("gen", "region", "organismo_corto", "gen_locus",
                     "huella_21", "huella_ge19", "firmado_por", "fecha",
                     "decision_usuario", "justificacion_usuario")

# Los cuatro campos obligatorios de D48 y las columnas que los materializan. La bandeja los
# muestra completos: una firma se escribe mirando los cuatro, no el nombre de la region.
CAMPOS_OBLIGATORIOS = {
    "organismo": ("organismo_corto", "organismo_especie", "organismo_rol"),
    "exposicion": ("exposicion_w", "exposicion_w_alternativa", "exposicion_motivo",
                   "exposicion_fuente", "exposicion_decision_abierta"),
    "gen_involucrado": ("gen_simbolo", "gen_locus", "gen_tipo_molecula",
                        "gen_transcriptos", "gen_anotacion", "gen_fuente"),
    "evidencia_biologica": ("evidencia_clave", "evidencia_bioensayo", "evidencia_prosa"),
}

CONTEOS = ("ventanas_perfecto_21", "ventanas_perfecto_ge19",
           "baja_complejidad_perfecto_21", "baja_complejidad_perfecto_ge19",
           "ventanas_21_eficientes", "ventanas_ge19_eficientes")

# El umbral con el que la compuerta exige decision es `perfecto_21`, que es D48 literal
# (`ranking.UMBRAL_COMPUERTA`). El otro umbral de D28 se informa al lado.
UMBRAL_COMPUERTA = "perfecto_21"

# Una racha de 21 nt o mas es lo que `tools/verificacion/sin_secuencias.py` no deja commitear,
# y este archivo **se versiona**. Una justificacion es prosa: si trae una racha asi, algo se
# pego mal, y conviene que la vista lo frene antes de que lo frene el hook.
RE_RACHA = re.compile(r"[ACGTUacgtu]{21,}")


class FirmaRechazada(ValueError):
    """La firma no se escribe. El mensaje dice cual de las reglas de D48 no cumple."""


def clave_de(fila: dict) -> tuple:
    """Region x organismo x **gen impactado**, que es la granularidad de D48.

    El cuarto elemento no es decorativo: en `ATPaseD_Dm` 72-371 hay dos filas de *Homo
    sapiens*, y una clave sin el gen las fusionaria. Fusionarlas significa firmar una y que la
    otra herede la firma sin que nadie la haya leido.
    """
    return (fila.get("gen"), fila.get("region"), fila.get("organismo_corto"),
            (fila.get("gen_locus") or "").strip())


def cita_la_fila(fila: dict, texto: str) -> bool:
    """D48 pide que la justificacion «cite la fila». Verificable: que la nombre.

    Alcanza con que mencione el LOC del gen impactado o una de las accesiones de transcripto de
    esa fila. Es un piso mecanico y grosero —se cumple pegando una accesion— pero distingue un
    parrafo escrito sobre esta fila de uno generico copiado a todas.
    """
    t = texto or ""
    loc = (fila.get("gen_locus") or "").strip()
    candidatos = [loc] if loc and not loc.startswith("(") else []
    candidatos += [a.strip() for a in (fila.get("gen_transcriptos") or "").split(",")
                   if a.strip()]
    candidatos += [a.strip() for a in (fila.get("gen_transcriptos") or "").split(";")
                   if a.strip()]
    return any(c in t for c in candidatos)


def validar_firma(fila: dict, decision: str, justificacion: str) -> None:
    """Las cuatro formas de rechazar una firma. `pendiente` no se escribe desde la bandeja.

    `pendiente` es un estado legitimo de la tabla pero **no es una firma**: escribir una firma
    que dice «pendiente» es ocupar la clave sin decidir nada, y despues la fila figura firmada.
    Quien quiera dejar algo sin decidir, lo deja sin fila.
    """
    d = (decision or "").strip()
    j = (justificacion or "").strip()
    donde = "%s %s / %s" % (fila.get("gen", "?"), fila.get("region", "?"),
                            fila.get("organismo_corto", "?"))

    if d not in DECISIONES:
        raise FirmaRechazada(
            "la decision %r no esta en el vocabulario cerrado %s" % (d, DECISIONES))
    if d == MARCA_PENDIENTE:
        raise FirmaRechazada(
            "«pendiente» no es una firma: es el estado de fabrica de la fila. Para dejar (%s) "
            "sin decidir, no la firmes." % donde)
    if j.startswith(MARCA_PENDIENTE):
        raise FirmaRechazada(
            "la justificacion de (%s) sigue siendo el texto de relleno. D48 pide una "
            "justificacion escrita, no cambiar una palabra." % donde)
    if len(j) < PROSA_MINIMA:
        raise FirmaRechazada(
            "la justificacion de (%s) tiene %d caracteres y el minimo es %d: D48 pide un "
            "parrafo, no un clic." % (donde, len(j), PROSA_MINIMA))
    if not cita_la_fila(fila, j):
        raise FirmaRechazada(
            "la justificacion de (%s) no cita la fila: tiene que nombrar el LOC (%s) o una de "
            "las accesiones (%s). D48 pide que la justificacion cite la fila."
            % (donde, fila.get("gen_locus", ""), fila.get("gen_transcriptos", "")))
    if RE_RACHA.search(j):
        raise FirmaRechazada(
            "la justificacion de (%s) tiene una racha de 21 nt o mas. Este archivo se "
            "versiona y las secuencias no salen del repositorio: cita la accesion o el LOC, no "
            "la secuencia." % donde)


# ------------------------------------------------------------------------- lectura

def _destraba(estados: list[dict], fila: dict) -> dict:
    """Que region destraba esta firma, leido de `estado_regiones.tsv`.

    «Destrabar» es una afirmacion sobre la compuerta, asi que se responde con lo que el
    inventario de regiones dice y con el umbral con el que la compuerta pregunta. Una fila con
    cero coincidencias de 21/21 **no destraba nada en el umbral vigente**, y la vista lo dice
    en vez de sugerir que cada firma pendiente libera una region.
    """
    gen, region = fila.get("gen"), fila.get("region")
    e = next((x for x in estados if x.get("gen") == gen and x.get("region") == region), None)
    if e is None:
        return {"region": "%s %s" % (gen, region), "en_el_inventario": False,
                "nota": "esta region no esta en el inventario de regiones tamizadas"}
    cuenta_21 = (entero(fila.get("ventanas_perfecto_21"), 0) or 0) > 0
    return {
        "region": "%s %s" % (gen, region),
        "en_el_inventario": True,
        "que_es": e.get("que_es", ""), "vigente": e.get("vigente", ""),
        "estado_D48": e.get("estado_D48", ""),
        "estado_firmado_21": e.get("estado_firmado_21", ""),
        "estado_firmado_ge19": e.get("estado_firmado_ge19", ""),
        "decide": e.get("decide", ""),
        "filas_de_alerta": entero(e.get("filas_de_alerta")),
        "cuenta_en_el_umbral_vigente": cuenta_21,
        "nota": ("esta fila cuenta en el umbral vigente (%s): firmarla mueve el estado de la "
                 "region" % UMBRAL_COMPUERTA) if cuenta_21 else
                ("esta fila tiene cero coincidencias de 21/21, y el umbral con el que la "
                 "compuerta exige decision es %s: firmarla NO destraba la region en el umbral "
                 "vigente. Cuenta en el umbral laxo de D28 (perfecto_ge19)."
                 % UMBRAL_COMPUERTA),
    }


def _fila_para_la_bandeja(f: dict, firmas: dict, estados: list[dict]) -> dict:
    k = clave_de(f)
    firma = firmas.get(k)
    return {
        "clave": "|".join(str(x) for x in k),
        "gen": f.get("gen", ""), "region": f.get("region", ""),
        "que_es": f.get("que_es", ""), "vigente": f.get("vigente", ""),
        "estado_region": f.get("estado_region", ""),
        "decision_usuario": (f.get("decision_usuario") or "").strip(),
        "justificacion_usuario": (f.get("justificacion_usuario") or "").strip(),
        # Los cuatro campos obligatorios de D48, completos.
        "campos": {campo: {c: f.get(c, "") for c in cols}
                   for campo, cols in CAMPOS_OBLIGATORIOS.items()},
        "conteos": {c: entero(f.get(c)) for c in CONTEOS},
        "posiciones_perfecto_21": f.get("posiciones_perfecto_21", ""),
        "posiciones_perfecto_ge19": f.get("posiciones_perfecto_ge19", ""),
        # La huella que una firma de esta fila tendria que llevar, leida de la fila.
        "huella": {"huella_21": str(entero(f.get("ventanas_perfecto_21"), "")),
                   "huella_ge19": str(entero(f.get("ventanas_perfecto_ge19"), ""))},
        "firma": None if firma is None else {
            "firmado_por": firma.get("firmado_por", ""), "fecha": firma.get("fecha", ""),
            "decision_usuario": firma.get("decision_usuario", ""),
            "huella_21": firma.get("huella_21", ""),
            "huella_ge19": firma.get("huella_ge19", ""),
        },
        "destraba": _destraba(estados, f),
    }


def ver() -> dict:
    """La bandeja: las filas por estado, con sus cuatro campos y que destraba cada una."""
    filas, problema = leer_tsv(INVENTARIO, COMANDO)
    if problema:
        return dict(problema, vista="firmas")
    estados, falta_estados = leer_tsv(ESTADO_REGIONES, COMANDO)
    crudas, _ = leer_tsv(FIRMAS, "")
    firmas = {clave_de(f): f for f in crudas}

    bandeja = [_fila_para_la_bandeja(f, firmas, estados) for f in filas]
    por_estado: dict[str, list] = {d: [] for d in DECISIONES}
    for f in bandeja:
        por_estado.setdefault(f["decision_usuario"] or "(sin dato)", []).append(f)

    pendientes = por_estado.get(MARCA_PENDIENTE, [])
    pend_en_umbral = [f for f in pendientes
                      if (f["conteos"]["ventanas_perfecto_21"] or 0) > 0]

    return {
        "estado": "listo", "vista": "firmas",
        "filas": bandeja,
        "por_estado": {k: [f["clave"] for f in v] for k, v in por_estado.items()},
        "cuenta": {k: len(v) for k, v in por_estado.items()},
        "total": len(bandeja),
        "pendientes": len(pendientes),
        "pendientes_en_el_umbral_vigente": len(pend_en_umbral),
        "umbral_de_la_compuerta": UMBRAL_COMPUERTA,
        "nota_del_umbral":
            "hay %d fila(s) en «pendiente», y %d de ellas cuenta(n) en el umbral con el que la "
            "compuerta exige decision (%s). Las demas cuentan solo en el umbral laxo de D28, "
            "asi que firmarlas no cambia el estado de ninguna region en el umbral vigente."
            % (len(pendientes), len(pend_en_umbral), UMBRAL_COMPUERTA),
        "archivo_inventario": rel(INVENTARIO),
        "archivo_estados": rel(ESTADO_REGIONES),
        "archivo_firmas": rel(FIRMAS),
        "firmas_en_disco": len(firmas),
        "falta_estados": falta_estados,
        "regla": "la firma se escribe en %s, que es entrada del generador. El inventario se "
                 "regenera corriendo: %s. Esta vista NO edita %s."
                 % (rel(FIRMAS), COMANDO, rel(INVENTARIO)),
        # Los conteos de la tabla son apareamiento exacto; las dos columnas de eficiencia no.
        "procedencia": procedencia(
            INVENTARIO, modo=NO_APLICA, motor=NO_APLICA, panel=NO_DECLARADA,
            nota="los conteos de coincidencia son apareamiento exacto y no dependen del modo "
                 "ni del motor. Las dos columnas de eficiencia si, y ningun archivo de M6 las "
                 "declara. El panel de referencias tampoco esta declarado en M6"),
    }


# ------------------------------------------------------------------------- escritura

def _escribir_atomico(ruta: Path, filas: list[dict]) -> None:
    """Escribe el TSV completo por reemplazo atomico.

    Un `open(..., "w")` que falla a la mitad deja el archivo de firmas truncado, y el archivo de
    firmas es la unica cosa de esta linea que no se puede regenerar desde un calculo: son
    decisiones escritas por personas. Se escribe al lado y se reemplaza de una.
    """
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(ruta.parent), prefix=".firmas-", suffix=".tsv")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(COLUMNAS_DECISION), delimiter="\t",
                               extrasaction="ignore")
            w.writeheader()
            for f in filas:
                w.writerow(f)
        os.replace(tmp, ruta)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def firmar(clave: str, decision: str, justificacion: str, firmado_por: str = "") -> dict:
    """Escribe una firma en el archivo de firmas. No toca el inventario.

    `clave` es la de la bandeja: `gen|region|organismo_corto|gen_locus`. La fila se busca en el
    inventario y **la huella se lee de ahi**, no de lo que mande el navegador: una firma cuya
    huella la pone quien firma no verifica nada.
    """
    filas, problema = leer_tsv(INVENTARIO, COMANDO)
    if problema:
        raise FirmaRechazada("no esta el inventario de alertas (%s): sin el no hay fila que "
                             "firmar" % rel(INVENTARIO))

    objetivo = next((f for f in filas if "|".join(str(x) for x in clave_de(f)) == clave), None)
    if objetivo is None:
        raise FirmaRechazada(
            "no hay ninguna fila con la clave %r en %s. Una firma que no corresponde a ninguna "
            "fila queda huerfana y el generador la rechaza." % (clave, rel(INVENTARIO)))

    autor = (firmado_por or "").strip()
    if not autor:
        raise FirmaRechazada("la firma necesita un autor: D48 pide que la escriba alguien, y "
                             "el archivo guarda quien y cuando")

    validar_firma(objetivo, decision, justificacion)

    # Una fila bloqueante que vuelve a aceptada es el caso que D48 nombra: la justificacion
    # tiene que citar la fila, y ya lo verifico `validar_firma`. Queda declarado en la
    # respuesta para que la vista pueda decirlo en pantalla y no sea un cambio mudo.
    antes = (objetivo.get("decision_usuario") or "").strip()
    reapertura = antes == "bloqueante" and decision.strip() == "aceptada"

    crudas, _ = leer_tsv(FIRMAS, "")
    nueva = {
        "gen": objetivo.get("gen", ""), "region": objetivo.get("region", ""),
        "organismo_corto": objetivo.get("organismo_corto", ""),
        "gen_locus": (objetivo.get("gen_locus") or "").strip(),
        "huella_21": str(entero(objetivo.get("ventanas_perfecto_21"), "")),
        "huella_ge19": str(entero(objetivo.get("ventanas_perfecto_ge19"), "")),
        "firmado_por": autor,
        "fecha": _dt.date.today().isoformat(),
        "decision_usuario": decision.strip(),
        "justificacion_usuario": justificacion.strip(),
    }

    k = clave_de(nueva)
    salida, reemplazada = [], False
    for f in crudas:
        if clave_de(f) == k:
            salida.append(nueva)
            reemplazada = True
        else:
            salida.append({c: f.get(c, "") for c in COLUMNAS_DECISION})
    if not reemplazada:
        salida.append(nueva)

    _escribir_atomico(FIRMAS, salida)

    return {
        "escrito": True, "clave": clave, "archivo": rel(FIRMAS),
        "reemplazada": reemplazada, "firmas": len(salida),
        "decision_anterior": antes, "reapertura_de_bloqueante": reapertura,
        "siguiente_paso":
            "la firma esta escrita. El inventario %s **no** cambio: se regenera corriendo %s, "
            "que vuelca las firmas sobre las filas y aborta si alguna quedo huerfana o "
            "vencida." % (rel(INVENTARIO), COMANDO),
    }
