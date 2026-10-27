"""M6: la compuerta que D48 deja abierta, aplicada a la tabla entregada.

D48 retira el veto automático y con eso **invierte el default**: la compuerta descartaba
por omisión y la tabla no descarta nada, así que una alerta **no leída** queda
operativamente igual que una aceptada. El informe de M6 lo dejó declarado como lo que el
software no puede hacer cumplir. Esto es lo mínimo que sí puede: negarse a tratar una
región como usable mientras alguna de sus filas siga sin decidir.

**No decide nada.** No dice qué alertas se aceptan y no verifica si una justificación es
cierta ni suficiente. Este script es el **inventario** de la compuerta: la corre sobre las
dieciocho regiones del inventario para mirar el estado de una sola vez, y no produce
ninguna recomendación.
Quien la aplica de verdad, desde D69, es `ranking.region_recomendada()` en el port: ahí
está el único punto donde una región se vuelve recomendación, y por eso llamarla desde
acá nunca alcanzó para dar la tarea por hecha.

Se corre en los dos umbrales de D28 a propósito. Con `perfecto_21` obligan las alertas de
las que habla D48 textualmente; con `perfecto_ge19` obligan también las del umbral laxo,
sobre las que D48 no se pronuncia. Los dos números cambian mucho la respuesta y por eso
van los dos.

    python research/ola4/M6_alertas/scripts/compuerta.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))

import alertas as AL   # noqa: E402

TABLA = RAIZ / "research/ola4/M6_alertas/resultados/alertas.tsv"
ESTADOS = RAIZ / "research/ola4/M6_alertas/resultados/estado_regiones.tsv"
SALIDA = RAIZ / "research/ola4/M6_alertas/resultados/compuerta.json"
# Las regiones del inventario, en el orden de estado_regiones.tsv: las que no tienen
# ninguna fila de alerta no aparecen en alertas.tsv y hay que traerlas de ahí, porque «sin
# alertas» es un estado que la compuerta tiene que poder informar. Desde D72 ese archivo
# es además **el inventario que la compuerta exige**: por eso este script nunca puede ver
# una `RegionNoTamizada` —itera justo sobre las regiones presentes— y es `ranking.py`,
# que itera sobre lo que el orden propone, el que sí puede.
import csv  # noqa: E402


def main() -> int:
    filas = AL.leer(TABLA)
    with ESTADOS.open(encoding="utf-8") as fh:
        regiones = [(r["gen"], r["region"], r["vigente"], r["que_es"])
                    for r in csv.DictReader(fh, delimiter="\t")]
    inventario = {(g, r) for g, r, _v, _q in regiones}
    print("tabla: %d filas, %d regiones\n" % (len(filas), len(regiones)))

    salida = {"tabla": str(TABLA.relative_to(RAIZ)), "filas": len(filas), "umbrales": {}}
    for umbral in ("perfecto_21", "perfecto_ge19"):
        print("== umbral %s ==" % umbral)
        detalle, pasan, frenadas = [], [], []
        for gen, region, vigente, que_es in regiones:
            try:
                est = AL.exigir_decidida(filas, gen, region, umbral,
                                         inventario=inventario)
                pasan.append((gen, region, vigente, est["estado"]))
                marca = "pasa"
            except AL.AlertaSinDecidir as e:
                est = AL.estado_decision(filas, gen, region, umbral)
                frenadas.append((gen, region, vigente, est))
                marca = "FRENADA"
                est["mensaje"] = str(e)
            est.update({"vigente": vigente, "que_es": que_es, "resultado": marca})
            detalle.append(est)
            print("  %-7s %-11s %-10s vigente=%-3s %s"
                  % (marca, gen, region, vigente, est["estado"]))
        nv = sum(1 for g, r, v, _ in frenadas if v == "sí")
        # «Pasa» y «se puede usar» NO son lo mismo, y desde que hay firmas la diferencia
        # se ve: una región `bloqueante` pasa la compuerta —bloquear es decidir, y la
        # compuerta sólo impide seguir de largo sin que nadie haya mirado— pero el que
        # llama tiene que descartarla. Un resumen de «pasan 12 de 12, frenadas 0» sin
        # esta cifra se lee como «todas sirven», que es exactamente al revés.
        bloq = [(g, r, v) for g, r, v, e in pasan if e == "decidida: bloqueante"]
        bv = sum(1 for _g, _r, v in bloq if v == "sí")
        print("  -> pasan %d de %d; frenadas %d, de las cuales %d son regiones vigentes"
              % (len(pasan), len(regiones), len(frenadas), nv))
        print("     de las que pasan, %d están **bloqueantes** (%d vigentes): pasan la "
              "compuerta porque alguien las decidió, y el que llama tiene que descartarlas%s\n"
              % (len(bloq), bv,
                 (": " + ", ".join("%s %s" % (g, r) for g, r, _v in bloq)) if bloq else ""))
        salida["umbrales"][umbral] = {
            "pasan": len(pasan), "frenadas": len(frenadas),
            "frenadas_vigentes": nv,
            "bloqueantes": len(bloq), "bloqueantes_vigentes": bv,
            "bloqueantes_detalle": ["%s %s" % (g, r) for g, r, _v in bloq],
            "detalle": detalle}

    SALIDA.write_text(json.dumps(salida, indent=1, ensure_ascii=False), encoding="utf-8")
    print("escrito en %s" % SALIDA.relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
