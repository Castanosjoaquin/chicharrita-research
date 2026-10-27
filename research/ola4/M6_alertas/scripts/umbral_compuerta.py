"""M6: cuanto cambia la compuerta segun el umbral de D28 que se le exija, y con que firmas.

`compuerta.py` corre la compuerta sobre la tabla **tal como esta**. Esto contesta la
pregunta de al lado, que es la que D69 tuvo que decidir: **cual de los dos umbrales de
D28 adopta la compuerta**, y cuanto cuesta esa eleccion.

Para eso hacen falta dos estados de la tabla, no uno:

  * `firmada`   la tabla de hoy, con las diecisiete firmas de D68 aplicadas.
  * `pendiente` la misma tabla con las diecisiete filas devueltas a «pendiente». Es el
                contrafactico del 2026-10-25, y es el que muestra de que tamano era la
                eleccion del umbral antes de que existieran las firmas. No se reconstruye
                regenerando la tabla —`tabla_alertas.py` necesita insumos de `work/` que
                no se versionan— sino sobreescribiendo en memoria las dos columnas de
                decision, que es exactamente lo que `tabla_alertas.py` escribia fijo
                antes de D68.

No decide nada y no escribe la tabla: lee, mide e imprime.

    python research/ola4/M6_alertas/scripts/umbral_compuerta.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))

import alertas as AL   # noqa: E402

TABLA = RAIZ / "research/ola4/M6_alertas/resultados/alertas.tsv"
ESTADOS = RAIZ / "research/ola4/M6_alertas/resultados/estado_regiones.tsv"
SALIDA = RAIZ / "research/ola4/M6_alertas/resultados/umbral_compuerta.json"

UMBRALES = ("perfecto_21", "perfecto_ge19")
# `estado_regiones.tsv` esta escrito con tildes; la columna `vigente` dice «si» o «no».
VIGENTE = ("si", "sí")


def en_pendiente(filas: list[dict]) -> list[dict]:
    """Las mismas filas con las dos columnas de decision de fabrica."""
    out = []
    for f in filas:
        g = dict(f)
        g["decision_usuario"] = AL.MARCA_PENDIENTE
        g["justificacion_usuario"] = "pendiente: la escribe el usuario, no el motor"
        out.append(g)
    return out


def medir(filas: list[dict], regiones: list[tuple]) -> dict:
    """Cuantas regiones pasan la compuerta en cada umbral, y cuantas de las frenadas son vigentes."""
    out = {}
    for umbral in UMBRALES:
        pasan, frenadas, bloqueantes = [], [], []
        for gen, region, vigente in regiones:
            try:
                est = AL.exigir_decidida(filas, gen, region, umbral)
                pasan.append((gen, region, vigente))
                if est["estado"] == "decidida: bloqueante":
                    bloqueantes.append((gen, region, vigente))
            except AL.AlertaSinDecidir:
                frenadas.append((gen, region, vigente))
        out[umbral] = {
            "regiones": len(regiones),
            "pasan": len(pasan),
            "frenadas": len(frenadas),
            "frenadas_vigentes": sum(1 for _g, _r, v in frenadas if v in VIGENTE),
            "bloqueantes": len(bloqueantes),
            "bloqueantes_vigentes": sum(1 for _g, _r, v in bloqueantes if v in VIGENTE),
            "frenadas_detalle": ["%s %s (vigente=%s)" % f for f in frenadas],
            "bloqueantes_detalle": ["%s %s" % (g, r) for g, r, _v in bloqueantes],
        }
    return out


def main() -> int:
    filas = AL.leer(TABLA)
    with ESTADOS.open(encoding="utf-8") as fh:
        regiones = [(r["gen"], r["region"], r["vigente"])
                    for r in csv.DictReader(fh, delimiter="\t")]
    vigentes = [r for r in regiones if r[2] in VIGENTE]
    print("tabla: %d filas | regiones: %d, de las cuales %d vigentes"
          % (len(filas), len(regiones), len(vigentes)))

    salida = {"tabla": "research/ola4/M6_alertas/resultados/alertas.tsv",
              "filas": len(filas), "regiones": len(regiones),
              "regiones_vigentes": ["%s %s" % (g, r) for g, r, _v in vigentes],
              "estados": {}}
    for etiqueta, fs in (("firmada", filas), ("pendiente", en_pendiente(filas))):
        salida["estados"][etiqueta] = medir(fs, regiones)
        print("\n== tabla %s ==" % etiqueta)
        for umbral in UMBRALES:
            m = salida["estados"][etiqueta][umbral]
            print("  %-14s pasan %2d de %d | frenadas %d (vigentes %d) | bloqueantes %d (vigentes %d)"
                  % (umbral, m["pasan"], m["regiones"], m["frenadas"], m["frenadas_vigentes"],
                     m["bloqueantes"], m["bloqueantes_vigentes"]))
            if m["frenadas_detalle"]:
                print("      frenadas: %s" % ", ".join(m["frenadas_detalle"]))

    SALIDA.write_text(json.dumps(salida, indent=1, ensure_ascii=False), encoding="utf-8")
    print("\nescrito en %s" % SALIDA.relative_to(RAIZ).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
