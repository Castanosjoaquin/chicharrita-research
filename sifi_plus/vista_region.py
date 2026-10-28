"""Vista A: que cambia cuando una region se mueve dentro del mismo gen.

Lee el inventario de alertas de `M6` y muestra dos regiones del mismo gen sobre el mismo eje de
posicion, con una marca por ventana con alerta y el organismo que la produce. El caso que la
motiva es `BicC_Dm` 264-563 contra 922-1221 —veintidos coincidencias perfectas de 21 nt contra
cero—, pero la vista toma **cualquier par** del directorio: el inventario se arma leyendo los
archivos que hay, no una lista escrita a mano.

**Esta vista no tamiza nada.** Si el par que alguien quiere ver no esta entre los archivos del
directorio, dice que falta ese archivo.

Dos cosas que la granularidad obliga a hacer bien:

**La unidad de conteo es la posicion, no la fila.** `alertas_por_ventana.tsv` tiene una fila por
posicion x organismo x **transcripto**, asi que las tres isoformas de la esterasa de maiz de
`BicC_Dm` 264-563 son nueve filas para tres posiciones. Contar filas daria nueve donde la tabla
por region declara tres. Se cuentan posiciones distintas `[M]`.

**El eje es la union de las dos regiones, no el gen entero.** El largo del gen no esta en
ninguno de los dos archivos que esta vista lee —aparece dentro de una frase de la columna
`complejidad_fuente`, y sacarlo de ahi seria parsear prosa—, asi que el eje va del arranque de
la primera region al final de la ultima y lo dice. Pintar un eje de largo inventado seria
afirmar algo sobre el gen que estos archivos no dicen.
"""

from __future__ import annotations

from lectura import (NO_APLICA, NO_DECLARADA, entero, leer_tsv, procedencia, rel,
                     tramos)
from lectura import RAIZ

M6 = RAIZ / "research" / "ola4" / "M6_alertas" / "resultados"
POR_VENTANA = M6 / "alertas_por_ventana.tsv"
POR_REGION = M6 / "alertas_por_region"
COMANDO = "python research/ola4/M6_alertas/scripts/tabla_alertas.py"

# Las columnas de la tabla por region que esta vista usa. Declaradas aca y no repartidas por
# el codigo para que el preregistro y el programa se puedan comparar de un vistazo.
COLS_FILA = ("organismo_corto", "organismo_especie", "organismo_rol", "gen_simbolo",
             "gen_locus", "gen_transcriptos", "evidencia_clave", "estado_region",
             "vigente", "que_es", "decision_usuario")
COLS_CONTEO = ("ventanas_perfecto_21", "ventanas_perfecto_ge19",
               "baja_complejidad_perfecto_21", "baja_complejidad_perfecto_ge19")
# Estas dos dependen del modo y del motor, y ningun archivo de M6 los declara.
COLS_SIN_PROCEDENCIA = ("ventanas_21_eficientes", "ventanas_ge19_eficientes")


def _partir(nombre: str) -> tuple[str, str]:
    """`BicC_Dm_264-563` -> `('BicC_Dm', '264-563')`.

    Se parte por el **ultimo** guion bajo: los nombres de gen los tienen adentro
    (`ATPaseD_Dm`, `MP_MRFV`), asi que partir por el primero daria `('BicC', 'Dm_264-563')`.
    """
    gen, _, region = nombre.rpartition("_")
    return gen, region


def inventario() -> dict:
    """Las regiones que hay en el directorio, para que el desplegable no sea una lista fija."""
    if not POR_REGION.is_dir():
        return {"estado": "no corrido", "archivo": rel(POR_REGION),
                "motivo": "no esta el directorio de regiones", "comando": COMANDO,
                "regiones": []}
    regiones = []
    for p in sorted(POR_REGION.glob("*.tsv")):
        gen, region = _partir(p.stem)
        a, _, b = region.partition("-")
        regiones.append({"clave": p.stem, "gen": gen, "region": region,
                         "inicio": entero(a), "fin": entero(b), "archivo": rel(p)})
    return {"estado": "listo", "regiones": regiones, "directorio": rel(POR_REGION)}


def _marcas(ventanas: list[dict], gen: str, region: str) -> dict:
    """Las posiciones con alerta de una region, agrupadas por organismo y criterio.

    Devuelve posiciones **distintas** y sus tramos. Los tramos son lo que se dibuja: las
    veintidos ventanas de 21/21 de `BicC_Dm` 264-563 son dos tramos contiguos, y dibujar
    veintidos marcas sueltas sugeriria veintidos aciertos independientes.
    """
    por_clave: dict[tuple, dict] = {}
    for f in ventanas:
        if f.get("gen") != gen or f.get("region") != region:
            continue
        k = (f.get("organismo_corto", ""), f.get("criterio", ""), f.get("gen_locus", ""))
        d = por_clave.setdefault(k, {
            "organismo_corto": k[0], "criterio": k[1], "gen_locus": k[2],
            "gen_simbolo": f.get("gen_simbolo", ""), "transcriptos": set(),
            "posiciones": set()})
        d["transcriptos"].add(f.get("transcripto", ""))
        p = entero(f.get("pos"))
        if p is not None:
            d["posiciones"].add(p)
    out = []
    for d in por_clave.values():
        pos = sorted(d["posiciones"])
        out.append({"organismo_corto": d["organismo_corto"], "criterio": d["criterio"],
                    "gen_locus": d["gen_locus"], "gen_simbolo": d["gen_simbolo"],
                    "transcriptos": sorted(t for t in d["transcriptos"] if t),
                    "posiciones": len(pos), "filas_del_archivo": None,
                    "tramos": tramos(pos), "desde": pos[0] if pos else None,
                    "hasta": pos[-1] if pos else None})
    out.sort(key=lambda d: (d["organismo_corto"], d["criterio"]))
    return {"marcas": out,
            "posiciones_distintas": len({p for d in por_clave.values()
                                         for p in d["posiciones"]})}


def _contrastar(filas: list[dict], marcas: list[dict]) -> list[dict]:
    """Compara el conteo por posicion con el que la tabla por region declara.

    Si no coinciden **no se corrige ninguno de los dos**: se devuelven las dos cifras con sus
    dos archivos, que es la convencion del repositorio para una contradiccion. Que coincidan no
    es obvio: son dos granularidades distintas y la de `alertas_por_ventana.tsv` lleva el
    transcripto adentro de la clave.
    """
    declarado = {}
    for f in filas:
        k = ((f.get("organismo_corto") or "").strip(), (f.get("gen_locus") or "").strip())
        declarado[k] = (entero(f.get("ventanas_perfecto_21"), 0),
                        entero(f.get("ventanas_perfecto_ge19"), 0))
    choques = []
    for m in marcas:
        k = (m["organismo_corto"], m["gen_locus"])
        if k not in declarado:
            choques.append({"clave": "%s / %s" % k, "que": "la tabla por region no tiene "
                            "fila para este organismo y gen",
                            "por_ventana": m["posiciones"], "por_region": None})
            continue
        esperado = declarado[k][0 if m["criterio"] == "perfecto_21" else 1]
        m["filas_del_archivo"] = esperado
        if esperado != m["posiciones"]:
            choques.append({
                "clave": "%s / %s / %s" % (k[0], k[1], m["criterio"]),
                "que": "no coinciden las dos cifras del mismo hecho",
                "por_ventana": m["posiciones"], "por_region": esperado,
                "archivo_por_ventana": rel(POR_VENTANA),
                "archivo_por_region": rel(POR_REGION)})
    return choques


def _region(clave: str, ventanas: list[dict]) -> dict:
    """Un panel de la vista: una region con sus filas de alerta y sus marcas."""
    gen, region = _partir(clave)
    ruta = POR_REGION / ("%s.tsv" % clave)
    filas, problema = leer_tsv(ruta, COMANDO)
    if problema:
        return dict(problema, clave=clave, gen=gen, region=region)

    m = _marcas(ventanas, gen, region)
    choques = _contrastar(filas, m["marcas"])
    a, _, b = region.partition("-")
    cab = filas[0] if filas else {}

    return {
        "estado": "listo", "clave": clave, "gen": gen, "region": region,
        "inicio": entero(a), "fin": entero(b),
        "que_es": cab.get("que_es", ""), "vigente": cab.get("vigente", ""),
        "estado_region": cab.get("estado_region", ""),
        "filas": [{c: f.get(c, "") for c in COLS_FILA}
                  | {c: entero(f.get(c)) for c in COLS_CONTEO}
                  | {c: {"valor": entero(f.get(c)), "procedencia": NO_DECLARADA}
                     for c in COLS_SIN_PROCEDENCIA}
                  for f in filas],
        "n_filas": len(filas),
        "marcas": m["marcas"], "posiciones_distintas": m["posiciones_distintas"],
        "contradicciones": choques,
        "archivo_region": rel(ruta), "archivo_ventanas": rel(POR_VENTANA),
    }


def ver(a: str, b: str) -> dict:
    """Las dos regiones del par, sobre el mismo eje de posicion.

    `a` y `b` son claves del inventario (`BicC_Dm_264-563`). Pueden ser de genes distintos: la
    vista no lo impide, pero lo **declara**, porque en ese caso el eje compartido no significa
    lo mismo y comparar posiciones entre dos genes no quiere decir nada.
    """
    ventanas, problema = leer_tsv(POR_VENTANA, COMANDO)
    if problema:
        return dict(problema, vista="region")

    paneles = [_region(a, ventanas), _region(b, ventanas)]
    listos = [p for p in paneles if p.get("estado") == "listo"]
    genes = {p["gen"] for p in listos}

    eje = None
    if listos:
        pos = [p["inicio"] for p in listos if p["inicio"] is not None]
        pos += [p["fin"] for p in listos if p["fin"] is not None]
        marcadas = [m for p in listos for d in p["marcas"] for m in (d["desde"], d["hasta"])
                    if m is not None]
        if pos:
            eje = {"desde": min(pos + marcadas), "hasta": max(pos + marcadas),
                   "que_es": "la union de las regiones mostradas, no el largo del gen: "
                             "el largo del gen no esta en estos archivos"}

    return {
        "estado": "listo", "vista": "region", "paneles": paneles, "eje": eje,
        "mismo_gen": len(genes) == 1,
        "aviso": "" if len(genes) == 1 else
                 "las dos regiones son de genes distintos (%s): el eje de posicion no es "
                 "comparable entre genes" % ", ".join(sorted(genes)),
        # Los conteos de coincidencia son apareamiento exacto de cadenas: no dependen de la
        # termodinamica, asi que el modo y el motor **no aplican**.
        #
        # El panel, en cambio, queda en «no declarado», y la diferencia con la lista de abajo
        # es la que mas facil seria pasar por alto: los organismos que aparecen en la tabla son
        # los que **tuvieron** alerta, no el panel contra el que se tamizo. Una referencia con
        # cero aciertos no deja ninguna fila, asi que leer el panel de las filas confundiria
        # «no tiene aciertos» con «no se miro», que es exactamente el estado 1 contra el 4 del
        # preregistro. El panel completo de esta corrida no esta en ningun archivo de M6.
        "procedencia": procedencia(
            POR_VENTANA, modo=NO_APLICA, motor=NO_APLICA, panel=NO_DECLARADA,
            nota="el conteo de coincidencias es apareamiento exacto y no depende del modo ni "
                 "del motor. Las dos columnas de eficiencia de la tabla si dependen, y "
                 "ningun archivo de M6 las declara: van con «procedencia no declarada». El "
                 "panel de referencias tampoco esta declarado en M6"),
        "organismos_con_alerta": sorted({d["organismo_corto"] for p in listos
                                         for d in p["marcas"]}),
        "organismos_nota": "son los organismos con alerta en estas dos regiones, NO el panel "
                           "contra el que se tamizo: una referencia con cero aciertos no deja "
                           "fila y no se puede distinguir aca de una que no se miro",
    }
