"""La tabla del informe: que afirmacion ya publicada se sostiene, y en que fraccion.

Lee `resultados/sensibilidad_reparto.json` y cruza cada afirmacion **que ya esta
publicada** —en `entregables/`, en un ADR o en un REPORT de ola 2 o 3— con la fraccion
de sorteos en la que se sostiene, a lo largo del barrido de rho. No inventa
afirmaciones nuevas: cada fila cita donde se publico la que mide.

    python research/ola4/M5_dos_ejes/scripts/tabla_afirmaciones.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
SALIDA = RAIZ / "research/ola4/M5_dos_ejes/resultados"

# (id, conjunto, combinacion, tipo, argumento, texto, donde se publico)
AFIRMACIONES = [
    ("A1", "virus", "geometrica/conservadora/absoluta", "par", ("MP_MRFV", "CP_MRFV"),
     "MP_MRFV va antes que CP_MRFV en escala absoluta",
     "entregables/para-el-investigador.md, fila 3 (>= 78,5 %)"),
    ("A2a", "los_seis", "geometrica/conservadora/absoluta", "dos_primeros",
     ("MP_MRFV", "eth_Dm"),
     "el orden de los dos primeros de los seis aguanta",
     "D18, consecuencia; ranking_v2.json los_seis (98,0 / 96,2 %)"),
    ("A2b", "insecto", "geometrica/conservadora/absoluta", "dos_primeros",
     ("eth_Dm", "bursA_Dm"),
     "el orden de los dos primeros de la lista del insecto aguanta",
     "ranking_v2.json insecto (96,4 / 96,4 %)"),
    ("A3", "insecto_recomendados", "geometrica/conservadora/absoluta", "posicion",
     ("BicC_Dm", 1),
     "BicC_Dm primero en la lista del insecto con las regiones recomendadas",
     "entregables/para-el-investigador.md, fila 3 (76-100 %)"),
    ("A4", "insecto_recomendados", "geometrica/conservadora/absoluta", "posicion",
     ("ATPaseD_Dm", 4),
     "ATPaseD_Dm ultimo en la lista del insecto con las regiones recomendadas",
     "entregables/para-el-investigador.md, fila 3"),
    ("A5", "insecto", "geometrica/conservadora/absoluta", "par", ("eth_Dm", "bursA_Dm"),
     "eth va antes que burs-alpha en escala absoluta",
     "entregables/checkpoint2-una-pagina.md, punto 5 (76-100 %)"),
    ("A6", "insecto", "geometrica/conservadora/absoluta", "par",
     ("BicC_Dm", "ATPaseD_Dm"),
     "BicC_Dm tercero y ATPaseD_Dm cuarto con las regiones de la planilla",
     "ranking_v2.json insecto (78,8 %)"),
    ("A7", "los_seis", "cascada/conservadora", "par", ("CP_MRFV", "ATPaseD_Dm"),
     "CP_MRFV va antes que ATPaseD_Dm (el par del 'tercer puesto' del issue #9)",
     "C9 T1 bis: se da vuelta en el 3,3 % de la grilla de umbrales"),
    ("A7b", "los_seis", "geometrica/conservadora/absoluta", "par",
     ("CP_MRFV", "ATPaseD_Dm"),
     "CP_MRFV va antes que ATPaseD_Dm, en la forma geometrica",
     "C9 T1 bis; D38 advierte que las dos listas no se comparan"),
]
# Las mismas, en todas las combinaciones de forma, regla y escala, para la tabla larga.


def fraccion(d: dict, tipo: str, arg) -> float | None:
    if tipo == "par":
        a, b = arg
        if "%s>%s" % (a, b) in d["pares_pct"]:
            return d["pares_pct"]["%s>%s" % (a, b)]
        if "%s>%s" % (b, a) in d["pares_pct"]:
            return round(100.0 - d["pares_pct"]["%s>%s" % (b, a)], 1)
        return None
    if tipo == "posicion":
        gen, puesto = arg
        return d["frecuencia"][gen][puesto - 1]
    if tipo == "dos_primeros":
        a, b = arg
        n = sum(o["pct"] for o in d["ordenes"] if o["orden"][:2] == [a, b])
        return round(n, 1)
    raise ValueError(tipo)


def main() -> int:
    S = json.loads((SALIDA / "sensibilidad_reparto.json").read_text(encoding="utf-8"))
    rhos = list(S["rho"])
    filas, largas = [], []
    for ident, conj, clave, tipo, arg, texto, donde in AFIRMACIONES:
        fila = {"id": ident, "afirmacion": texto, "publicada_en": donde,
                "conjunto": conj, "combinacion": clave, "muestras": S["muestras"]}
        for rho in rhos:
            fila["rho_" + rho] = fraccion(S["rho"][rho][conj][clave], tipo, arg)
        fila["rho_0_veto_ciego"] = fraccion(S["rho_0_veto_ciego"][conj][clave], tipo, arg)
        filas.append(fila)
        for clave2 in S["rho"][rhos[0]][conj]:
            f2 = {"id": ident, "afirmacion": texto, "conjunto": conj,
                  "combinacion": clave2, "muestras": S["muestras"]}
            for rho in rhos:
                f2["rho_" + rho] = fraccion(S["rho"][rho][conj][clave2], tipo, arg)
            f2["rho_0_veto_ciego"] = fraccion(S["rho_0_veto_ciego"][conj][clave2], tipo, arg)
            largas.append(f2)

    for nombre, datos in (("tabla_afirmaciones.tsv", filas),
                          ("tabla_afirmaciones_todas_las_combinaciones.tsv", largas)):
        with (SALIDA / nombre).open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(datos[0]), delimiter="\t")
            w.writeheader()
            w.writerows(datos)

    enc = ["%6s" % r for r in rhos]
    print("%-4s%-62s%s%s" % ("id", "afirmacion", "".join(enc), "  ciego"))
    for f in filas:
        print("%-4s%-62s%s%8s" % (
            f["id"], f["afirmacion"][:60],
            "".join("%6.1f" % f["rho_" + r] for r in rhos), f["rho_0_veto_ciego"]))
    print("\nescrito en %s" % (SALIDA / "tabla_afirmaciones.tsv").relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
