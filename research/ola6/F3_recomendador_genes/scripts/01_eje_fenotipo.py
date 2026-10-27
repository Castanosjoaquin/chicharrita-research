#!/usr/bin/env python3
"""Paso 1 de F3 — el eje de fenotipo, asignado desde `resultado` y verificado contra la fuente.

Por qué este script tiene una tabla escrita a mano y no un clasificador
---------------------------------------------------------------------
El preregistro (§6) pide que el mecanismo de cada candidato salga de la columna
`resultado` del catálogo de C5, en una columna explícita y **nunca inferido del nombre
del gen**. Un clasificador por palabras clave sobre prosa libre en español haría
justamente lo contrario de lo pedido: acertaría por correlación con el nombre del gen
y fallaría en silencio en las filas que dicen lo opuesto de lo que el gen sugiere
—y hay cuatro de ésas—.

Entonces la asignación la hace una persona leyendo las 36 filas, y el programa la
**verifica**: cada asignación viaja con la frase exacta de `resultado` que la sostiene,
y el script falla si esa frase no está, textual, en el catálogo. Eso cierra el agujero
que importa: nadie puede asignar un mecanismo que la fuente no diga, y si el catálogo
cambia, el script se rompe en vez de seguir publicando una asignación vieja.

La asignación de este archivo se escribió leyendo el campo `resultado` completo, no su
versión recortada. Dos errores de una lectura anterior, hecha sobre el texto truncado,
quedan documentados en `resultados/correcciones_al_preregistro.md`.

Uso:
    python research/ola6/F3_recomendador_genes/scripts/01_eje_fenotipo.py
"""

import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
CATALOGO = RAIZ / "research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.json"
SALIDA = Path(__file__).resolve().parents[1] / "resultados/eje_fenotipo.tsv"

# Los cuatro mecanismos: los tres de D67 más `transmision`, que el catálogo tiene y D67 no
# (entrada 65 de la ola 6). Un candidato puede tener más de uno.
MECANISMOS = ("reproduccion", "movilidad", "letalidad", "transmision")

# Las etiquetas de ausencia. Son excluyentes entre sí y con los mecanismos: una fila con
# etiqueta no entra al orden por el eje de fenotipo, y la etiqueta dice por qué.
ETIQUETAS = (
    "sin_fenotipo_publicado",            # `resultado` no reporta un desenlace
    "sin_fenotipo_atribuible_al_blanco",  # lo reporta, y la propia fuente dice que no es del blanco
    "fenotipo_invertido",                 # silenciarlo empeora el problema
    "potenciador_de_entrega",             # no tiene fenotipo propio: mejora la respuesta al ARNdc
    "fenotipo_fuera_de_los_cuatro",       # desenlace real que no entra en ninguno de los cuatro
)

# id -> (mecanismos, etiqueta, frases de apoyo, evidencia negativa explícita, nota)
# `apoyo`: subcadenas EXACTAS de `resultado`. El script verifica que estén.
# `negativa`: subcadenas exactas donde la propia fuente niega un mecanismo. Se publican
#             porque un «no hubo efecto» medido vale tanto como un efecto.
ASIGNACION = {
    "DM-01": (["reproduccion"], None, ["oviposicion casi nula"], [], ""),
    "DM-02": (["letalidad", "movilidad"], None,
              ["supervivencia 16 % a dia 4", "alas deformes"], [],
              "la deformacion de alas es el unico apoyo de movilidad en todo el catalogo"),
    "DM-03": (["letalidad"], None, ["supervivencia 18 % a dia 4"],
              ["efecto en alas no significativo"],
              "mismo gen que DM-02 en otra subunidad: aca el efecto en alas se midio y NO dio"),
    "DM-04": ([], "potenciador_de_entrega", ["mejora la respuesta al ARNdc"], [],
              "no es un blanco por su fenotipo: es un co-blanco que mejora la entrega. "
              "Sin fenotipo propio, no compite en el orden"),
    "DM-05": (["letalidad"], None, ["supervivencia 10 % a dia 4"], [], ""),
    "DM-06": (["letalidad"], None, ["supervivencia 10 % a dia 4"], [], ""),
    "CI-01": (["letalidad", "reproduccion"], None,
              ["supervivencia menor que dsGFP", "ovarios sin huevos"], [], ""),
    "CI-02": (["letalidad", "reproduccion"], None,
              ["supervivencia menor que dsGFP", "progenie 0,03 ninfas"], [],
              "el efecto es de la hembra segun los cruzamientos de la propia fuente"),
    "CI-03": (["reproduccion"], None, ["morfologia de huevos alterada"],
              ["SIN efecto sobre la supervivencia"],
              "mismo gen que CI-04 en otra especie, con el desenlace de supervivencia opuesto: "
              "contradiccion declarada, no promediada"),
    "CI-04": (["letalidad"], None, ["caida significativa de la supervivencia"], [],
              "mismo gen que CI-03 en otra especie, con el desenlace opuesto"),
    "CI-05": (["letalidad"], None, ["caida significativa de la supervivencia"], [],
              "el gen es actina muscular, pero `resultado` mide supervivencia y no movilidad: "
              "no se asigna movilidad por el nombre del gen"),
    "CI-06": (["transmision"], None, ["menos adquisicion de fitoplasma"], [],
              "la fuente mide el efecto sobre el patogeno, no sobre el insecto"),
    "CI-07": (["transmision"], None,
              ["reduce la colonizacion de intestino y glandulas salivales",
               "menos transmision a haba"], [],
              "la unica fila del catalogo con transmision a planta medida"),
    "CI-08": ([], "fenotipo_invertido",
              ["silenciarlo AUMENTO la colonizacion del vector por el fitoplasma"], [],
              "silenciarlo empeora el problema: fuera del orden, sin puntaje negativo"),
    "CI-09": (["transmision"], None, ["reduccion significativa de la multiplicacion del fitoplasma"],
              ["ninguno de los tres genes afecto la supervivencia"],
              "fila que agrupa tres genes; la ausencia de efecto en supervivencia es medida"),
    "CI-10": (["letalidad", "reproduccion"], None,
              ["baja la supervivencia", "la fecundidad"], [],
              "`resultado` tambien reporta caida de la capacidad de alimentacion y del peso, "
              "que no entran en ninguno de los cuatro mecanismos"),
    "CI-11": (["letalidad"], None, ["alta mortalidad"], [],
              "fila que agrupa NcLac2 y NcLac5; el desenlace descrito es del primero"),
    "CI-12": (["letalidad"], None, ["alta mortalidad y despigmentacion"], [],
              "RNAi parental: el desenlace se mide en la progenie, no en el inyectado"),
    "CI-13": ([], "fenotipo_invertido",
              ["silenciarlo AUMENTA la infeccion del sistema nervioso"], [],
              "silenciarlo empeora el problema: fuera del orden, sin puntaje negativo"),
    "DE-01": (["letalidad", "reproduccion"], None, ["mayor mortalidad y menor fecundidad"], [],
              "fila que agrupa V-ATPase B y V-ATPase D"),
    "DE-02": (["reproduccion"], None, ["sin ovocitos maduros a 8 y 12 dias"], [], ""),
    "DE-03": (["reproduccion"], None,
              ["las hembras se transforman en pseudomachos", "los machos quedan esteriles"], [],
              "esterilidad de los dos sexos por vias distintas"),
    "DE-04": (["letalidad", "reproduccion"], None,
              ["alta mortalidad en menos de 5 dias", "desarrollo ovarico impedido"], [],
              "fila que agrupa tres transportadores ABC con desenlaces DISTINTOS: "
              "la letalidad es de ABCE y ABCF, la reproduccion es de ABCB"),
    "DE-05": (["letalidad", "reproduccion", "transmision"], None,
              ["menor supervivencia y reproduccion de las hembras",
               "menor acumulacion del rabdovirus MMV"], [],
              "la unica fila con los tres mecanismos medidos a la vez"),
    "DE-06": ([], "sin_fenotipo_publicado", ["ver fuente para la magnitud por especie"], [],
              "el catalogo dice que el diseno es el mismo que en D. maidis pero no trae la "
              "magnitud: asignarle la letalidad de DM-05 y DM-06 seria inferirla de otra fila"),
    "HE-01": (["reproduccion"], None, ["papel vital en oogenesis"], [],
              "cualitativo: la fuente no trae una medicion"),
    "HE-02": (["letalidad"], None, ["45 % de mortalidad"], [], ""),
    "HE-03": ([], "sin_fenotipo_publicado", ["silenciamiento por varias vias de entrega"], [],
              "reporta que el silenciamiento ocurre, no que produzca un desenlace"),
    "HE-04": ([], "sin_fenotipo_atribuible_al_blanco",
              ["el knockdown NO correlaciona con la dosis"], [],
              "la propia fuente dice que el control de dsGFP a 500 y 1000 ng/uL ya mata mas que "
              "el de sacarosa: hay 64 % de mortalidad y no es atribuible al blanco"),
    "HE-05": (["reproduccion"], None, ["necesario para el epitelio folicular"], [],
              "cualitativo: la fuente no trae una medicion"),
    "HE-06": ([], "sin_fenotipo_publicado", ["efecto sobre el ARNm de actina"], [],
              "el desenlace reportado es molecular, no fenotipico"),
    "HE-07": (["letalidad", "reproduccion"], None, ["longevidad a la mitad", "menos huevos"], [],
              "la FUNCION es una proteina salival de la ingestion de floema, lo que invita a "
              "leerlo como transmision; `resultado` mide longevidad, desarrollo y huevos. "
              "Se asigna por el resultado"),
    "HE-08": ([], "sin_fenotipo_atribuible_al_blanco",
              ["mortalidad alta por la dosis, no por el blanco"], [],
              "control negativo que el propio catalogo trae"),
    "HE-09": ([], "fenotipo_fuera_de_los_cuatro", ["necesaria para la respuesta inmune"], [],
              "silenciarla bajaria la inmunidad del vector frente a Spiroplasma; el signo para "
              "nuestro objetivo no es determinable con lo que la fuente dice"),
    "HE-10": ([], "sin_fenotipo_publicado",
              ["demostracion de RNAi en un cicadelido del algodon"], [],
              "la fila documenta que el RNAi funciona en la especie, sin blanco ni desenlace"),
    "HE-11": ([], "sin_fenotipo_publicado",
              ["RNAi funcional en la interaccion con el virus"], [],
              "no reporta un desenlace medido; la interaccion con el virus no es, por si sola, "
              "una reduccion de transmision medida"),
}


def main() -> int:
    filas = json.loads(CATALOGO.read_text(encoding="utf-8"))["filas"]
    por_id = {f["id"]: f for f in filas}

    faltan = sorted(set(por_id) - set(ASIGNACION))
    sobran = sorted(set(ASIGNACION) - set(por_id))
    if faltan or sobran:
        print(f"ERROR: el catalogo y la asignacion no coinciden.", file=sys.stderr)
        if faltan:
            print(f"  filas del catalogo sin asignar: {faltan}", file=sys.stderr)
        if sobran:
            print(f"  asignaciones sin fila en el catalogo: {sobran}", file=sys.stderr)
        return 1

    errores = []
    registros = []
    for ident, fila in por_id.items():
        mecanismos, etiqueta, apoyo, negativa, nota = ASIGNACION[ident]
        resultado = fila["resultado"] or ""

        # La verificacion que da sentido al archivo: la frase tiene que estar en la fuente.
        for frase in list(apoyo) + list(negativa):
            if frase not in resultado:
                errores.append(f"{ident}: la frase de apoyo no esta en `resultado`: {frase!r}")

        for m in mecanismos:
            if m not in MECANISMOS:
                errores.append(f"{ident}: mecanismo desconocido {m!r}")
        if etiqueta is not None and etiqueta not in ETIQUETAS:
            errores.append(f"{ident}: etiqueta desconocida {etiqueta!r}")
        if bool(mecanismos) == bool(etiqueta):
            errores.append(f"{ident}: tiene que tener mecanismos O etiqueta, no las dos ni ninguna")
        if not apoyo:
            errores.append(f"{ident}: sin frase de apoyo; toda asignacion tiene que citar la fuente")

        registros.append({
            "id": ident,
            "especie": fila["especie"],
            "gen": fila["gen"],
            "familia_id": ident.split("-")[0],
            "mecanismos": "|".join(mecanismos) if mecanismos else "",
            "etiqueta_de_ausencia": etiqueta or "",
            "entra_al_orden_por_fenotipo": "si" if mecanismos else "no",
            "marcador_evidencia": fila["marcador"],
            "frases_de_apoyo": " // ".join(apoyo),
            "evidencia_negativa_medida": " // ".join(negativa),
            "tiene_ventanas_21nt": "si" if fila.get("ventanas_21nt") else "no",
            "nota": nota,
        })

    if errores:
        print("ERROR: la asignacion no se verifica contra el catalogo.", file=sys.stderr)
        for e in errores:
            print(f"  {e}", file=sys.stderr)
        return 1

    registros.sort(key=lambda r: r["id"])
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA.open("w", encoding="utf-8", newline="") as fh:
        esc = csv.DictWriter(fh, fieldnames=list(registros[0]), delimiter="\t",
                             lineterminator="\n")
        esc.writeheader()
        esc.writerows(registros)

    con_mec = [r for r in registros if r["mecanismos"]]
    print(f"eje de fenotipo: {len(registros)} filas, "
          f"{len(con_mec)} con mecanismo y {len(registros) - len(con_mec)} con etiqueta de ausencia")
    for m in MECANISMOS:
        n = sum(1 for r in con_mec if m in r["mecanismos"].split("|"))
        print(f"  {m:12s}: {n}")
    for e in ETIQUETAS:
        n = sum(1 for r in registros if r["etiqueta_de_ausencia"] == e)
        if n:
            print(f"  {e:34s}: {n}")
    n_neg = sum(1 for r in registros if r["evidencia_negativa_medida"])
    print(f"  filas con un 'no hubo efecto' medido y publicado: {n_neg}")
    print(f"escrito: {SALIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
