"""La salida real de `F1` leida como fichas de `F2` (issues #25 y #26).

`F1` entrega `research/ola6/F1_transferencia_homologia/resultados/transferencia_<REF>.tsv.gz`,
una fila **por ORF** con su ortologo reciproco, su identidad, sus dos coberturas y la banda
de concordancia de `C12`. `F2` lee fichas. Este modulo es el unico lugar donde se traduce
una cosa en la otra, y es tambien donde quedan escritas las cuatro diferencias entre lo que
`F1` produce y lo que `F2` suponia antes de que `F1` corriera:

1. **`F1` habla de contigs, no de loci**, y lo dice en su preregistro: varios contigs pueden
   ser isoformas o fragmentos del mismo gen, asi que el numero de contigs es una cota
   superior del numero de genes. La ficha lleva `unidad: "contig"` y el parrafo dice
   «contig», no «locus». Es la diferencia que mas facil se perdia al traducir.
2. **La tabla es por ORF y la ficha es por contig.** Un contig puede tener varios ORF de
   100 aminoacidos o mas, y `F1` ya fija como se resuelve: gana la **mejor categoria** del
   contig segun su jerarquia, y dentro de la misma categoria, el mayor `bitscore`. Esa
   regla se copia de `F1` y no se inventa aca.
3. **No hay cabecera FASTA**: el nombre de producto viene en su propia columna, asi que la
   regla del parentesis de `alertas.partir_anotacion` no tiene nada que hacer con estas
   filas. La ficha usa el camino `simbolo` + `accesion`, que `F2` acepta justamente para
   esto; la regla del parentesis sigue viva para el otro productor.
4. **La concordancia viene como proporcion** (`0.862`) y el parrafo la dice en porcentaje.
   La conversion se hace **aca**, y el valor convertido es el que queda en la ficha, que es
   la condicion para que `verificar_procedencia` lo pueda respaldar: lo que el parrafo dice
   tiene que estar en la ficha, no en la cabeza del que tradujo.

Y una diferencia mas, que es un hueco y no una traduccion: `F1` no registra en la tabla con
que corrida se midio cada fila. El campo `fuente_alineamiento` que `F2` exige se arma aca
con el nombre del archivo leido `[H]`, que es lo mas preciso que se puede decir sin
inventar: identifica la corrida tanto como el archivo la identifique.

`F1` tampoco produce terminos GO, dominios ni papers. Las fichas salen con esas tres listas
vacias y el parrafo sale mas corto. No se rellenan.

Uso:
    python3 fichas_desde_f1.py <transferencia_REF.tsv.gz> --censo
    python3 fichas_desde_f1.py <transferencia_REF.tsv.gz> --fichas fichas.json [--max 500]
"""

from __future__ import annotations

import argparse
import collections
import csv
import gzip
import json
import sys
from pathlib import Path

# La jerarquia y las categorias son de `F1`: se copian textuales de
# `research/ola6/F1_transferencia_homologia/scripts/transferir_anotacion.py` para que el
# orden de desempate sea el mismo y no una reconstruccion nuestra.
JERARQUIA = ["f_reciproco_con_nombre", "e_reciproco_sin_nombre", "d_empate",
             "c_hit_no_reciproco", "b_sin_hit", "a_sin_orf"]
RANGO = {c: i for i, c in enumerate(JERARQUIA)}

# Las categorias que traen un alineamiento con todos sus numeros. Las otras dos —sin ORF y
# sin hit— no tienen nada que anotar y van a ficha sin bloque de anotacion.
CON_ALINEAMIENTO = ("c_hit_no_reciproco", "d_empate", "e_reciproco_sin_nombre",
                    "f_reciproco_con_nombre")

# Las dos referencias del preregistro de `F1`, por el sufijo de su archivo.
ORGANISMO_DE = {
    "MQ": "Macrosteles quadrilineatus",
    "HV": "Homalodisca vitripennis",
}

# `F1` rotula este tramo como no concluyente: son 16 pares en `C12`. El parrafo lo dice.
TRAMO_NO_CONCLUYENTE = "<40"

COLUMNAS = ("contig", "categoria", "ref_id", "ref_producto", "nombre_normalizado",
            "pident", "cob_orf", "cob_ref", "bitscore", "banda_identidad",
            "banda_concordancia", "banda_ic_lo", "banda_ic_hi", "banda_pares_c12")


def organismo_de(ruta: Path) -> str:
    """La especie de referencia, por el sufijo del archivo de `F1`."""
    tallo = ruta.name.split(".")[0]
    sufijo = tallo.rsplit("_", 1)[-1].upper()
    if sufijo not in ORGANISMO_DE:
        raise ValueError(
            "no se que proteoma de referencia es %r. Los del preregistro de F1 son %s; si "
            "aparece otro, agregarlo aca a mano y no adivinarlo del nombre del archivo"
            % (ruta.name, ", ".join(sorted(ORGANISMO_DE))))
    return ORGANISMO_DE[sufijo]


def _abrir(ruta: Path):
    if ruta.suffix == ".gz":
        return gzip.open(ruta, "rt", encoding="utf-8", newline="")
    return ruta.open("r", encoding="utf-8", newline="")


def mejor_por_contig(ruta: Path) -> dict:
    """Una fila por contig: la mejor categoria, y dentro de ella el mayor bitscore.

    Es la regla de `F1`, no una nuestra. Devuelve `{contig: fila}` conservando el orden de
    aparicion, que es el del transcriptoma.
    """
    mejores: dict = collections.OrderedDict()
    with _abrir(ruta) as fh:
        for fila in csv.DictReader(fh, delimiter="\t"):
            faltan = [c for c in COLUMNAS if c not in fila]
            if faltan:
                raise ValueError("a %s le faltan columnas de F1: %s"
                                 % (ruta.name, ", ".join(faltan)))
            contig = fila["contig"]
            previa = mejores.get(contig)
            if previa is None or _mejor_que(fila, previa):
                mejores[contig] = fila
    return mejores


def _mejor_que(fila: dict, otra: dict) -> bool:
    r_nueva = RANGO.get(fila["categoria"], len(JERARQUIA))
    r_vieja = RANGO.get(otra["categoria"], len(JERARQUIA))
    if r_nueva != r_vieja:
        return r_nueva < r_vieja
    return _float(fila["bitscore"]) > _float(otra["bitscore"])


def _float(txt: str) -> float:
    try:
        return float(txt)
    except (TypeError, ValueError):
        return 0.0


def ficha_de(fila: dict, organismo: str, fuente: str) -> dict:
    """La ficha de `F2` que corresponde a una fila de `F1`."""
    base = {"locus": fila["contig"], "unidad": "contig",
            "go": [], "dominios": [], "papers": []}
    if fila["categoria"] not in CON_ALINEAMIENTO:
        return dict(base, anotacion=None)

    tramo = fila["banda_identidad"]
    return dict(base, anotacion={
        # `ref_producto` es el nombre tal como lo escribe RefSeq, que es lo que se lee;
        # `nombre_normalizado` es la version de `C12` para comparar, y no se publica como
        # si fuera el nombre. Un producto «uncharacterized» llega igual y es `F2` quien lo
        # clasifica como anotacion no informativa: aca no se filtra nada.
        "simbolo": fila["ref_producto"],
        "accesion": fila["ref_id"],
        "organismo": organismo,
        "identidad": _float(fila["pident"]),
        "cobertura_orf": _float(fila["cob_orf"]),
        "cobertura_referencia": _float(fila["cob_ref"]),
        "reciproco": fila["categoria"].startswith(("e_", "f_")),
        "empate": fila["categoria"] == "d_empate",
        "fuente_alineamiento": fuente,
        "banda": {
            "tramo": tramo,
            # De proporcion a porcentaje, aca y no en el parrafo: lo que el parrafo dice
            # tiene que estar en la ficha para que la verificacion lo pueda respaldar.
            "concordancia": round(_float(fila["banda_concordancia"]) * 100, 1),
            "ic": [round(_float(fila["banda_ic_lo"]) * 100, 1),
                   round(_float(fila["banda_ic_hi"]) * 100, 1)],
            "n": int(_float(fila["banda_pares_c12"])),
            "concluyente": tramo != TRAMO_NO_CONCLUYENTE,
            "fuente": "C12 Validacion A",
        },
    })


def fichas(ruta: Path) -> list:
    """Todas las fichas de un archivo de `F1`, una por contig."""
    organismo = organismo_de(ruta)
    fuente = "F1 diamond blastp, %s" % ruta.name
    return [ficha_de(f, organismo, fuente) for f in mejor_por_contig(ruta).values()]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("tabla", type=Path, help="transferencia_<REF>.tsv.gz de F1")
    ap.add_argument("--fichas", type=Path, help="JSON de fichas a escribir")
    ap.add_argument("--max", type=int, help="escribir solo las primeras N fichas")
    ap.add_argument("--censo", action="store_true",
                    help="el reparto por estado de F2, sin escribir nada")
    args = ap.parse_args(argv)

    todas = fichas(args.tabla)
    print("contigs                      %6d" % len(todas))

    if args.censo:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import evidencia_en_prosa as P        # noqa: PLC0415
        cuenta = P.censo(todas)
        for clave in P.ESTADOS + ("total", "con_parrafo", "sin_parrafo"):
            print("%-28s %6d" % (clave, cuenta[clave]))
        return 0

    recorte = todas[:args.max] if args.max else todas
    if args.fichas:
        args.fichas.write_text(json.dumps(recorte, ensure_ascii=False, indent=2),
                               encoding="utf-8")
        print("escritas %d fichas en %s" % (len(recorte), args.fichas))
    else:
        print(json.dumps(recorte[:3], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
