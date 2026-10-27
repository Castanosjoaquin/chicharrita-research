#!/usr/bin/env python3
"""F4 — Los pares de candidatos elegibles para armar una quimera por mecanismo.

**El criterio no lo elige este script: lo fija `PREREGISTRO.md`, escrito y commiteado antes
de enumerar un solo par.** Si alguna pieza de aca no coincide con el preregistro, el
preregistro manda y esto es un error a corregir.

Que hace. Pedile «uno de reproduccion con uno de letalidad» y devuelve los pares de
candidatos elegibles, leyendo la asignacion de mecanismo que dejo `F3` en
`research/ola6/F3_recomendador_genes/resultados/eje_fenotipo.tsv`. No devuelve «el mejor
par»: no hay orden de calidad, no hay puntaje y no hay primer puesto. Las filas salen en
orden alfabetico por identificador y **ese orden no significa nada**.

De donde sale quien entra, y de donde no
----------------------------------------
De las columnas de la tabla, con el triple candado del §2 del preregistro: `etiqueta_de_ausencia`
vacia, `entra_al_orden_por_fenotipo` en `si`, y `mecanismos` no vacio con mecanismos conocidos.
Las tres dicen lo mismo por tres caminos y la corrida **aborta** si una fila no las tiene
coherentes, porque eso no es un caso a resolver con una preferencia: es una tabla que cambio de
semantica.

**Ningun identificador de candidato se escribe en este archivo.** No es una preferencia de
estilo: una lista escrita a mano queda muerta cuando el catalogo cambia, y sigue publicando la
asignacion vieja sin romperse. Dos de las 36 filas tienen el signo invertido —silenciarlas
AUMENTA la colonizacion del vector por el patogeno, entrada 66— asi que una lista que se olvide
de sacarlas no produce un numero flojo: produce una quimera peor que no hacer nada. La prueba
`test_pares.py` §9 recorre el AST de este modulo y falla si aparece un identificador como
literal en el codigo ejecutable.

Lo unico declarado a mano aca es el **vocabulario** de `F3` —los cuatro mecanismos y las cinco
etiquetas de ausencia—, y si la tabla trae uno que no esta en esa lista la corrida aborta y lo
nombra: una etiqueta nueva puede querer decir «excluir» o «admitir» y el programa no tiene con
que decidirlo. La contraevidencia por mecanismo es **entrada** y no codigo: vive en
`contraevidencia.tsv` —la forma que `D68` le dio a las firmas de `M6`— y cada frase se verifica
textual contra la columna `evidencia_negativa_medida` de la propia tabla.

El cuarto mecanismo
-------------------
`F3` publica `transmision` con cuatro candidatos y `D67` define tres. Ampliar `D67` no es de
esta linea (entrada 65), pero medir no es adoptar: un pedido que incluya `transmision` aborta,
y con `--ampliar-d67` corre con la condicion pegada a **cada fila** de la salida. La tabla de
respaldo de los cuatro mecanismos se imprime siempre, porque contar filas de una tabla no
amplia ninguna decision.

Lo que este script no hace: no recomienda ningun par, no afirma eficacia —el criterio de
eficiencia de si-Fi21 no esta validado en hemipteros: rho = +0,142, IC95 [-0,247, +0,492],
n = 29 `[M]`—, no decide si `movilidad` sigue siendo una pata del esquema (entrada 70) y no
mira secuencias: un par elegible no es un par corrible, y eso lo dice el enumerador de `O4`
cuando se le pasan las rutas.

Uso (desde la raiz del repositorio):
    python research/ola6/F4_pares_por_mecanismo/scripts/pares_por_mecanismo.py \\
        --mecanismos reproduccion,letalidad \\
        --mecanismos reproduccion,movilidad \\
        --mecanismos letalidad,movilidad
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
BLOQUE = Path(__file__).resolve().parents[1]
TABLA = RAIZ / "research/ola6/F3_recomendador_genes/resultados/eje_fenotipo.tsv"
CONTRAEVIDENCIA = BLOQUE / "contraevidencia.tsv"

#: Los cuatro mecanismos de `F3`, en el orden en que los declara su paso 1.
MECANISMOS = ("reproduccion", "movilidad", "letalidad", "transmision")
#: Los tres que `D67` define. El cuarto queda detras de `--ampliar-d67` (§5 del preregistro).
MECANISMOS_D67 = ("reproduccion", "movilidad", "letalidad")
#: Las cinco etiquetas de ausencia de `F3`. Una fila con etiqueta no es elegible, y la
#: etiqueta dice por que. Una etiqueta que no este aca aborta la corrida.
ETIQUETAS = (
    "sin_fenotipo_publicado",
    "sin_fenotipo_atribuible_al_blanco",
    "fenotipo_invertido",
    "potenciador_de_entrega",
    "fenotipo_fuera_de_los_cuatro",
)
#: El esquema de `eje_fenotipo.tsv`. Si cambia, esta linea para en vez de leer columnas
#: por posicion o de adivinar un nombre nuevo.
COLUMNAS = ("id", "especie", "gen", "familia_id", "mecanismos", "etiqueta_de_ausencia",
            "entra_al_orden_por_fenotipo", "marcador_evidencia", "frases_de_apoyo",
            "evidencia_negativa_medida", "tiene_ventanas_21nt", "nota")
#: El esquema de `contraevidencia.tsv`, que es entrada declarada de esta linea.
COLUMNAS_CONTRA = ("mecanismo", "fila_que_la_sostiene", "frase_textual_en_eje_fenotipo",
                   "por_que_cuenta_como_contraevidencia", "fuente_de_la_lectura")
#: La especie blanco. Un candidato de otra especie es una quimera sobre el ortologo en la
#: nuestra, que hay que tener y anotar (`F1`), no sobre el gen medido.
ESPECIE_BLANCO = "Dalbulus maidis"
#: La frase con la que el catalogo marca que una fila es mas de un gen. La escribio el paso 1
#: de `F3` y su script la verifico contra la fuente.
MARCA_AGRUPA = "fila que agrupa"
SIN_VALIDAR = ("el criterio de eficiencia de si-Fi21 no esta validado en hemipteros: "
               "rho = +0,142, IC95 [-0,247, +0,492], n = 29")


class Aborta(SystemExit):
    """Para que la tabla que cambio de semantica se lea como lo que es: una parada."""

    def __init__(self, *motivos: str):
        cuerpo = "\n".join("  - %s" % m for m in motivos)
        super().__init__("la tabla de mecanismos no se verifica contra el vocabulario "
                         "declarado en PREREGISTRO.md §2:\n%s" % cuerpo)


def leer_tabla(ruta: Path = TABLA) -> list[dict]:
    """Las 36 filas, con el esquema verificado y nada interpretado todavia."""
    if not ruta.exists():
        raise SystemExit("falta %s. Lo produce "
                         "research/ola6/F3_recomendador_genes/scripts/01_eje_fenotipo.py"
                         % ruta)
    with ruta.open(encoding="utf-8", newline="") as fh:
        filas = list(csv.DictReader(fh, delimiter="\t"))
    if not filas:
        raise SystemExit("%s esta vacia" % ruta)
    if tuple(filas[0]) != COLUMNAS:
        raise Aborta("el esquema cambio. Esperado %s; llego %s"
                     % (list(COLUMNAS), list(filas[0])))
    return filas


def _mecanismos_de(fila: dict) -> list[str]:
    bruto = (fila["mecanismos"] or "").strip()
    return bruto.split("|") if bruto else []


def clasificar(filas: list[dict]) -> tuple[dict[str, dict], dict[str, dict]]:
    """Elegibles y excluidos, con el triple candado. Aborta si la tabla se contradice.

    Devuelve dos diccionarios por identificador. El de excluidos lleva el motivo que da la
    propia tabla, porque saber que se descarto y por que es parte del resultado: el issue
    #39 pide que los de signo invertido, los de mortalidad no atribuible y el potenciador
    **no puedan** aparecer, no que se escondan.
    """
    problemas, elegibles, excluidos = [], {}, {}
    for f in filas:
        ident, etiqueta = f["id"], (f["etiqueta_de_ausencia"] or "").strip()
        mecanismos = _mecanismos_de(f)
        entra = (f["entra_al_orden_por_fenotipo"] or "").strip()

        if etiqueta and etiqueta not in ETIQUETAS:
            problemas.append("%s: etiqueta desconocida %r. Una etiqueta nueva puede querer "
                             "decir «excluir» o «admitir» y este programa no tiene con que "
                             "decidirlo" % (ident, etiqueta))
            continue
        desconocidos = [m for m in mecanismos if m not in MECANISMOS]
        if desconocidos:
            problemas.append("%s: mecanismo desconocido %s. Un quinto mecanismo mueve la "
                             "pregunta de la entrada 65 y pide revisar la puerta del §5"
                             % (ident, desconocidos))
            continue
        if entra not in ("si", "no"):
            problemas.append("%s: entra_al_orden_por_fenotipo vale %r y tiene que ser "
                             "'si' o 'no'" % (ident, entra))
            continue

        # El triple candado: las tres senales tienen que decir lo mismo.
        senales = (not etiqueta, entra == "si", bool(mecanismos))
        if len(set(senales)) != 1:
            problemas.append(
                "%s: las tres senales de elegibilidad no coinciden "
                "(etiqueta=%r, entra=%r, mecanismos=%r)"
                % (ident, etiqueta, entra, f["mecanismos"]))
            continue

        destino = elegibles if all(senales) else excluidos
        destino[ident] = {**f, "mecanismos_lista": mecanismos,
                          "agrupa_varios_genes": agrupa_varios_genes(f)}
    if problemas:
        raise Aborta(*problemas)
    return elegibles, excluidos


def agrupa_varios_genes(fila: dict) -> bool:
    """Si la fila es mas de un gen. Dos detectores sobre la fila, y se cruzan en `verificar`.

    Una quimera se arma con un gen y no con una fila: `DE-01` es `V-ATPase B` **y**
    `V-ATPase D`, y `DE-04` agrupa tres transportadores ABC con desenlaces distintos, donde
    la letalidad es de dos de ellos y la reproduccion del tercero. Una fila agrupada no es
    directamente un insumo del enumerador.
    """
    return MARCA_AGRUPA in (fila["nota"] or "")


def _parece_varios_genes(fila: dict) -> bool:
    """El segundo detector, sobre la forma del campo `gen` y no sobre la nota."""
    gen = fila["gen"] or ""
    return " y " in gen or "," in gen


def soporte(elegibles: dict[str, dict]) -> dict[str, dict]:
    """Cuantos candidatos elegibles sostienen cada mecanismo, y cuantos en la especie blanco.

    Es lo que el issue #39 pide que la salida diga, y el motivo esta medido: `movilidad`
    tiene un solo candidato en las 36 filas y su replica mas cercana es negativa
    (entrada 70). Un enumerador que ofrece combinaciones de tres mecanismos sin decir eso
    deja que una sola fila se lea como una opcion entre varias.
    """
    salida = {}
    for m in MECANISMOS:
        ids = sorted(i for i, f in elegibles.items() if m in f["mecanismos_lista"])
        propios = [i for i in ids if elegibles[i]["especie"] == ESPECIE_BLANCO]
        salida[m] = {"ids": ids, "n": len(ids),
                     "ids_en_la_especie_blanco": propios,
                     "n_en_la_especie_blanco": len(propios),
                     "descansa_en_un_solo_candidato": len(ids) == 1,
                     "en_d67": m in MECANISMOS_D67}
    return salida


def leer_contraevidencia(elegibles: dict[str, dict], filas: list[dict],
                         ruta: Path = CONTRAEVIDENCIA) -> dict[str, list[dict]]:
    """La contraevidencia declarada, verificada textual contra la tabla de `F3`.

    Es el candado que `F3` uso para las frases de apoyo, del otro lado: nadie puede declarar
    una contraevidencia que la fuente no diga, y si la tabla cambia esto se rompe en vez de
    seguir publicando una lectura vieja. El archivo es **entrada** del script y no salida
    suya, que es la forma que `D68` le dio a las firmas de `M6`.
    """
    if not ruta.exists():
        raise SystemExit("falta %s, que es entrada declarada de esta linea" % ruta)
    with ruta.open(encoding="utf-8", newline="") as fh:
        decl = list(csv.DictReader(fh, delimiter="\t"))
    if decl and tuple(decl[0]) != COLUMNAS_CONTRA:
        raise Aborta("el esquema de %s cambio. Esperado %s; llego %s"
                     % (ruta.name, list(COLUMNAS_CONTRA), list(decl[0])))
    por_id = {f["id"]: f for f in filas}
    problemas, salida = [], {}
    for d in decl:
        mec, ident, frase = d["mecanismo"], d["fila_que_la_sostiene"], d["frase_textual_en_eje_fenotipo"]
        if mec not in MECANISMOS:
            problemas.append("contraevidencia de un mecanismo desconocido: %r" % mec)
            continue
        if ident not in por_id:
            problemas.append("la contraevidencia de %s cita la fila %s, que no esta en la "
                             "tabla" % (mec, ident))
            continue
        if frase not in (por_id[ident]["evidencia_negativa_medida"] or ""):
            problemas.append("la contraevidencia de %s cita una frase que no esta textual en "
                             "evidencia_negativa_medida de %s: %r" % (mec, ident, frase))
            continue
        salida.setdefault(mec, []).append(d)
    if problemas:
        raise Aborta(*problemas)
    return salida


def verificar(filas: list[dict], elegibles: dict[str, dict],
              excluidos: dict[str, dict]) -> None:
    """Los cruces que no son sobre una fila sola. Abortan, no advierten."""
    problemas = []
    if len(filas) != len(elegibles) + len(excluidos):
        problemas.append("se perdio una fila en la clasificacion")
    # Los dos detectores de fila agrupada tienen que coincidir sobre las elegibles (§4 del
    # preregistro). Si no coinciden, una de las dos lecturas quedo vieja y hay que mirarla.
    for ident, f in sorted(elegibles.items()):
        if agrupa_varios_genes(f) != _parece_varios_genes(f):
            problemas.append(
                "%s: los dos detectores de fila agrupada no coinciden (nota dice %s, el "
                "campo gen %r dice %s)"
                % (ident, agrupa_varios_genes(f), f["gen"], _parece_varios_genes(f)))
    if problemas:
        raise Aborta(*problemas)


def motivo_de_exclusion(excluidos: dict[str, dict], ident: str) -> str:
    """La frase que explica, con la tabla en la mano, por que un candidato no entra."""
    f = excluidos[ident]
    return ("%s (%s, %s) esta fuera del orden de F3 con la etiqueta %r: %s"
            % (ident, f["gen"], f["especie"], f["etiqueta_de_ausencia"],
               f["nota"] or f["frases_de_apoyo"]))


def pares(elegibles: dict[str, dict], x: str, y: str, sop: dict[str, dict],
          contra: dict[str, list[dict]], ampliar_d67: bool) -> list[dict]:
    """Los pares elegibles para «uno de `x` con uno de `y`», con su respaldo al lado.

    Un par es una **asignacion de rol a dos candidatos distintos**: `a` cubriendo `x` y `b`
    cubriendo `y`, con `x != y` y `a != b` (§3 del preregistro). El par **no esta ordenado**:
    que el fragmento izquierdo sea uno o el otro es un grado de libertad de la grilla de `O4`
    —esta medido que cambia el resultado— y duplicar cada fila aca no agregaria informacion.
    Lo que si se enumera dos veces es la asignacion de roles cuando los dos candidatos tienen
    los dos mecanismos, porque el eje declarado de cada gen es distinto en cada una y es lo
    que `O4` escribe en sus columnas.
    """
    sx, sy = sop[x]["ids"], sop[y]["ids"]
    filas = []
    for a, b in itertools.product(sx, sy):
        if a == b:
            continue                      # una quimera son dos fragmentos de dos genes
        fa, fb = elegibles[a], elegibles[b]
        comunes = sorted(set(fa["mecanismos_lista"]) & set(fb["mecanismos_lista"]))
        propias = sum(1 for f in (fa, fb) if f["especie"] == ESPECIE_BLANCO)
        filas.append({
            "mecanismos_pedidos": "%s+%s" % (x, y),
            "rol_a": x, "id_a": a, "gen_a": fa["gen"], "especie_a": fa["especie"],
            "marcador_a": fa["marcador_evidencia"], "mecanismos_de_a": fa["mecanismos"],
            "fuente_del_eje_a": "C5/%s" % a,
            "rol_b": y, "id_b": b, "gen_b": fb["gen"], "especie_b": fb["especie"],
            "marcador_b": fb["marcador_evidencia"], "mecanismos_de_b": fb["mecanismos"],
            "fuente_del_eje_b": "C5/%s" % b,
            "candidatos_que_sostienen_rol_a": sop[x]["n"],
            "candidatos_que_sostienen_rol_b": sop[y]["n"],
            "rol_a_descansa_en_un_solo_candidato":
                "si" if sop[x]["descansa_en_un_solo_candidato"] else "no",
            "rol_b_descansa_en_un_solo_candidato":
                "si" if sop[y]["descansa_en_un_solo_candidato"] else "no",
            "mecanismos_de_los_dos_se_solapan": "si" if comunes else "no",
            "mecanismos_en_comun": "|".join(comunes),
            "roles_al_reves_tambien_elegible":
                "si" if (y in fa["mecanismos_lista"] and x in fb["mecanismos_lista"])
                else "no",
            "mitades_de_la_especie_blanco": propias,
            "fila_a_agrupa_varios_genes": "si" if fa["agrupa_varios_genes"] else "no",
            "fila_b_agrupa_varios_genes": "si" if fb["agrupa_varios_genes"] else "no",
            "evidencia_negativa_medida_a": fa["evidencia_negativa_medida"],
            "evidencia_negativa_medida_b": fb["evidencia_negativa_medida"],
            "contraevidencia_del_rol_a": " // ".join(
                "%s: %s" % (c["fila_que_la_sostiene"], c["frase_textual_en_eje_fenotipo"])
                for c in contra.get(x, [])),
            "contraevidencia_del_rol_b": " // ".join(
                "%s: %s" % (c["fila_que_la_sostiene"], c["frase_textual_en_eje_fenotipo"])
                for c in contra.get(y, [])),
            "ampliacion_de_d67_sin_adr": "si" if ampliar_d67 else "no",
        })
    # Orden declarado: alfabetico y reproducible. No es un orden de calidad (§3).
    filas.sort(key=lambda f: (f["id_a"], f["id_b"]))
    return filas


def pedido(spec: str, ampliar_d67: bool) -> tuple[str, str]:
    """`X,Y`: dos mecanismos distintos, con la puerta del cuarto cerrada por defecto."""
    partes = [p.strip() for p in spec.split(",")]
    if len(partes) != 2:
        raise SystemExit("--mecanismos pide dos mecanismos separados por coma, llego %r"
                         % spec)
    x, y = partes
    desconocidos = [m for m in partes if m not in MECANISMOS]
    if desconocidos:
        raise SystemExit("mecanismo desconocido %s. Los cuatro de F3 son %s"
                         % (desconocidos, ", ".join(MECANISMOS)))
    if x == y:
        raise SystemExit(
            "D67 arma las quimeras combinando fenotipos que **no se solapan**, asi que los "
            "dos mecanismos tienen que ser distintos y llegaron dos veces %r. Es la misma "
            "condicion que exige el objetivo cobertura_fenotipica de O4." % x)
    fuera = [m for m in partes if m not in MECANISMOS_D67]
    if fuera and not ampliar_d67:
        raise SystemExit(
            "el pedido incluye %s, que F3 publica como categoria declarada con %d candidatos "
            "y que D67 **no** tiene: D67 define tres mecanismos. Si entra al armado es una "
            "ampliacion de D67 y pide su propio ADR (entrada 65), que no es de esta linea. "
            "Para medirlo sin adoptarlo: --ampliar-d67, y entonces cada fila de la salida "
            "lleva la condicion pegada."
            % (", ".join(fuera), len(MECANISMOS) - len(MECANISMOS_D67)))
    return x, y


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mecanismos", action="append", default=[], metavar="X,Y",
                    help="se repite por par pedido; los dos mecanismos tienen que ser "
                         "distintos (D67)")
    ap.add_argument("--especie", default=None,
                    help="restringe los dos lados a una especie, p. ej. 'Dalbulus maidis'")
    ap.add_argument("--ampliar-d67", action="store_true", dest="ampliar",
                    help="habilita `transmision`, que D67 no tiene, y estampa la condicion "
                         "en cada fila")
    ap.add_argument("--nombre", default="d67")
    ap.add_argument("--resultados", default=None, type=Path)
    a = ap.parse_args(argv)

    if not a.mecanismos:
        raise SystemExit("hace falta al menos un --mecanismos X,Y. No tiene default: el par "
                         "de mecanismos es lo que esta linea recibe, no lo que supone.")
    pedidos = [pedido(s, a.ampliar) for s in a.mecanismos]

    filas = leer_tabla()
    elegibles, excluidos = clasificar(filas)
    verificar(filas, elegibles, excluidos)
    contra = leer_contraevidencia(elegibles, filas)

    print("tabla de mecanismos: %s" % TABLA.relative_to(RAIZ))
    print("  %d filas, %d elegibles y %d excluidas por su etiqueta"
          % (len(filas), len(elegibles), len(excluidos)))
    for e in ETIQUETAS:
        ids = sorted(i for i, f in excluidos.items() if f["etiqueta_de_ausencia"] == e)
        if ids:
            print("    %-34s %d: %s" % (e, len(ids), ", ".join(ids)))

    if a.especie:
        especies = {f["especie"] for f in filas}
        if a.especie not in especies:
            raise SystemExit("ninguna fila es de %r. Las especies de la tabla son: %s"
                             % (a.especie, ", ".join(sorted(especies))))
        elegibles = {i: f for i, f in elegibles.items() if f["especie"] == a.especie}
        print("  restringido a %s: quedan %d elegibles de las %d"
              % (a.especie, len(elegibles), len(filas) - len(excluidos)))
    sop = soporte(elegibles)
    print("\nrespaldo por mecanismo (lo que el issue #39 pide que la salida diga)")
    print("  %-13s %-6s %5s %5s  %s" % ("mecanismo", "en D67", "elig", "blanco", "nota"))
    for m in MECANISMOS:
        s = sop[m]
        nota = []
        if s["descansa_en_un_solo_candidato"]:
            nota.append("DESCANSA EN UNA SOLA FILA")
        for c in contra.get(m, []):
            nota.append("contraevidencia %s: «%s»"
                        % (c["fila_que_la_sostiene"], c["frase_textual_en_eje_fenotipo"]))
        print("  %-13s %-6s %5d %5d  %s"
              % (m, "si" if s["en_d67"] else "NO", s["n"], s["n_en_la_especie_blanco"],
                 "; ".join(nota)))
    n_neg = sum(1 for f in elegibles.values() if f["evidencia_negativa_medida"])
    print("  filas elegibles con un «no hubo efecto» medido y publicado: %d" % n_neg)

    todas, resumen = [], []
    for x, y in pedidos:
        ps = pares(elegibles, x, y, sop, contra, a.ampliar)
        todas.extend(ps)
        genes = {frozenset((p["id_a"], p["id_b"])) for p in ps}
        resumen.append({
            "mecanismos_pedidos": "%s+%s" % (x, y),
            "asignaciones_de_rol": len(ps),
            "pares_de_genes_distintos": len(genes),
            "sostenido_por": {x: sop[x]["n"], y: sop[y]["n"]},
            "roles_que_descansan_en_un_solo_candidato": [
                m for m in (x, y) if sop[m]["descansa_en_un_solo_candidato"]],
            "pares_con_mecanismos_solapados": sum(
                1 for p in ps if p["mecanismos_de_los_dos_se_solapan"] == "si"),
            "pares_con_las_dos_mitades_de_la_especie_blanco": sum(
                1 for p in ps if p["mitades_de_la_especie_blanco"] == 2),
            "pares_con_alguna_fila_que_agrupa_varios_genes": sum(
                1 for p in ps if "si" in (p["fila_a_agrupa_varios_genes"],
                                          p["fila_b_agrupa_varios_genes"])),
            "amplia_d67": sorted(set((x, y)) - set(MECANISMOS_D67)),
        })
        print("\n%s+%s: %d asignaciones de rol sobre %d pares de genes distintos"
              % (x, y, len(ps), len(genes)))
        if not ps:
            print("  ninguna. Con este pedido no hay par elegible%s"
                  % (" en %s" % a.especie if a.especie else ""))
        for p in ps[:6]:
            print("    %s (%s) + %s (%s)%s"
                  % (p["id_a"], p["rol_a"], p["id_b"], p["rol_b"],
                     "  [mecanismos en comun: %s]" % p["mecanismos_en_comun"]
                     if p["mecanismos_en_comun"] else ""))
        if len(ps) > 6:
            print("       … y %d mas en el TSV" % (len(ps) - 6))

    res = a.resultados or (BLOQUE / "resultados")
    res.mkdir(parents=True, exist_ok=True)
    f_pares = res / ("pares_elegibles_%s.tsv" % a.nombre)
    if todas:
        with f_pares.open("w", encoding="utf-8", newline="") as fh:
            esc = csv.DictWriter(fh, fieldnames=list(todas[0]), delimiter="\t",
                                 lineterminator="\n")
            esc.writeheader()
            esc.writerows(todas)

    f_sop = res / ("soporte_por_mecanismo_%s.tsv" % a.nombre)
    with f_sop.open("w", encoding="utf-8", newline="") as fh:
        esc = csv.DictWriter(fh, delimiter="\t", lineterminator="\n", fieldnames=[
            "mecanismo", "en_d67", "candidatos_elegibles", "ids",
            "candidatos_en_la_especie_blanco", "ids_en_la_especie_blanco",
            "descansa_en_un_solo_candidato", "contraevidencia_declarada"])
        esc.writeheader()
        for m in MECANISMOS:
            s = sop[m]
            esc.writerow({
                "mecanismo": m, "en_d67": "si" if s["en_d67"] else "no",
                "candidatos_elegibles": s["n"], "ids": "|".join(s["ids"]),
                "candidatos_en_la_especie_blanco": s["n_en_la_especie_blanco"],
                "ids_en_la_especie_blanco": "|".join(s["ids_en_la_especie_blanco"]),
                "descansa_en_un_solo_candidato":
                    "si" if s["descansa_en_un_solo_candidato"] else "no",
                "contraevidencia_declarada": " // ".join(
                    "%s: %s" % (c["fila_que_la_sostiene"],
                                c["frase_textual_en_eje_fenotipo"])
                    for c in contra.get(m, []))})

    f_meta = res / ("meta_%s.json" % a.nombre)
    f_meta.write_text(json.dumps({
        "que_es_esto": "los pares de candidatos elegibles para armar una quimera por "
                       "mecanismo, leidos de la asignacion de F3. No hay orden de calidad, "
                       "no hay puntaje y no hay primer puesto: el orden de las filas es "
                       "alfabetico por identificador y no significa nada",
        "criterio": "research/ola6/F4_pares_por_mecanismo/PREREGISTRO.md, commiteado antes "
                    "de enumerar un solo par",
        "entrada": {
            "tabla": str(TABLA.relative_to(RAIZ)),
            "filas": len(filas),
            "contraevidencia_declarada": str(CONTRAEVIDENCIA.relative_to(RAIZ))},
        "regla_de_elegibilidad": "etiqueta_de_ausencia vacia Y "
                                 "entra_al_orden_por_fenotipo = si Y mecanismos no vacio; "
                                 "las tres tienen que coincidir o la corrida aborta. Ningun "
                                 "identificador de candidato esta escrito en el codigo",
        "especie_blanco": ESPECIE_BLANCO,
        "restringido_a_especie": a.especie,
        "elegibles": sorted(elegibles),
        "excluidos": {i: excluidos[i]["etiqueta_de_ausencia"] for i in sorted(excluidos)},
        "soporte_por_mecanismo": {
            m: {k: v for k, v in sop[m].items()} for m in MECANISMOS},
        "contraevidencia_verificada_textual": contra,
        "pedidos": resumen,
        "ampliacion_de_d67": {
            "estado": "pedida con --ampliar-d67" if a.ampliar else "no pedida",
            "que_significa": "transmision es categoria declarada de F3 con cuatro "
                             "candidatos y D67 define tres. Entrar al armado es ampliar "
                             "D67 y pide su propio ADR (PREGUNTAS_ABIERTAS 65). Medir no "
                             "es adoptar: con la puerta abierta cada fila lleva "
                             "ampliacion_de_d67_sin_adr = si"},
        "lo_que_no_hace": [
            "no recomienda ningun par: enumera y mide",
            "no afirma eficacia: %s [M]" % SIN_VALIDAR,
            "no decide si movilidad sigue siendo una pata del esquema "
            "(PREGUNTAS_ABIERTAS 70)",
            "no mira secuencias: un par elegible no es un par corrible. El enumerador de O4 "
            "necesita el gen entero de cada mitad",
            "un par no pasa todavia por el inventario de alertas de M6: la clave de juntura "
            "que D78 le dio a una quimera no esta implementada (PREGUNTAS_ABIERTAS 41)"],
        "python": sys.version.split()[0],
    }, indent=2, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8")

    donde = res.relative_to(RAIZ) if res.is_relative_to(RAIZ) else res
    print("\nescrito en %s" % donde)
    for p in (f_pares if todas else None, f_sop, f_meta):
        if p:
            print("  %s" % p.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
