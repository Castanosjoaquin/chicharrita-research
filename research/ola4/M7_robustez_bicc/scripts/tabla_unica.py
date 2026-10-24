"""M7 - la tabla unica de salida, armada desde los JSON de los dos ejes.

El issue #11 pide **una sola tabla**: en que fraccion de las configuraciones 922-1221 le
gana a 2121-2420 y a 264-563, por cada eje y en conjunto. Este script la escribe en
`resultados/tabla_unica.md` a partir de `fracciones_parametros.json` y
`referencia_resumen.json`, para que las cifras del informe no se transcriban a mano.

Uso (desde la raiz del repositorio):
    python research/ola4/M7_robustez_bicc/scripts/tabla_unica.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SALIDA = Path(__file__).resolve().parents[1] / "resultados"
ORDEN = ["en conjunto", "modo = fiel", "modo = corregido", "tabla = NN3", "tabla = NN4",
         "motor = vienna", "motor = exe", "brecha = 1,0 (defecto)",
         "accesibilidad = 0,1 (defecto)", "punto por defecto"]
NOMBRE = {"en conjunto": "**en conjunto**", "modo = fiel": "modo `fiel`",
          "modo = corregido": "modo `corregido`", "tabla = NN3": "tabla `RNA_NN3`",
          "tabla = NN4": "tabla `RNA_NN4`", "motor = vienna": "ViennaRNA 2.7.2",
          "motor = exe": "RNAplfold 2.1.5", "brecha = 1,0 (defecto)": "brecha 1,0, toda la accesibilidad",
          "accesibilidad = 0,1 (defecto)": "accesibilidad 0,1, toda la brecha",
          "punto por defecto": "punto por defecto (8 celdas)"}


def pct(v):
    return "—" if v is None else ("%.1f %%" % v).replace(".", ",")


def main() -> int:
    p = json.loads((SALIDA / "fracciones_parametros.json").read_text(encoding="utf-8"))
    r = json.loads((SALIDA / "referencia_resumen.json").read_text(encoding="utf-8"))
    # El recalculo por region sale del TSV, que lo tiene para toda region con cobertura
    # completa, aunque la region foco no se pueda comparar en esa fuente (caso GCWP01).
    recalc = {}
    lineas = (SALIDA / "referencia_por_region.tsv").read_text(encoding="utf-8").splitlines()
    cab = lineas[0].split("\t")
    for linea in lineas[1:]:
        c = dict(zip(cab, linea.split("\t")))
        recalc[(c["fuente"], c["region"])] = c["recalc_corregido"]
    L = []

    L.append("## Tabla unica — en que fraccion de las configuraciones gana 922-1221\n")
    L.append("Fuente: `resultados/fracciones_parametros.json`. Cada celda dice sobre "
             "cuantas configuraciones se calculo. «Contexto» cuenta las ventanas que "
             "arrancan en la region dentro del gen de 2.520 nt; «recorte» es la molecula "
             "de 300 nt plegada sola, que es la que se sintetizaria.\n")
    L.append("| Corte de la grilla | Config. | vs 2121-2420 (contexto) | vs 2121-2420 "
             "(recorte) | vs 264-563 (contexto) | vs 264-563 (recorte) | a las dos a la "
             "vez (recorte) |")
    L.append("|---|---|---|---|---|---|---|")
    for clave in ORDEN:
        c = p["fracciones"]["contexto"].get(clave)
        d = p["fracciones"]["recorte"].get(clave)
        if c is None:
            continue
        L.append("| %s | %d | %s | %s | %s | %s | %s |" % (
            NOMBRE[clave], c["configuraciones"],
            pct(c["vs_2121-2420"]["gana_pct"]), pct(d["vs_2121-2420"]["gana_pct"]),
            pct(c["vs_264-563"]["gana_pct"]), pct(d["vs_264-563"]["gana_pct"]),
            pct(d["gana_a_los_dos_pct"])))
    sb = p["fracciones"]["recorte_sin_bordes"]["en conjunto"]
    L.append("| recorte sin sus dos primeras posiciones | %d | — | %s | — | %s | %s |" % (
        sb["configuraciones"], pct(sb["vs_2121-2420"]["gana_pct"]),
        pct(sb["vs_264-563"]["gana_pct"]), pct(sb["gana_a_los_dos_pct"])))
    L.append("")

    L.append("Margen de la diferencia, en conjunto (ventanas eficientes de 922-1221 menos "
             "las de la rival, mediana y extremos sobre las %d configuraciones):\n"
             % p["fracciones"]["contexto"]["en conjunto"]["configuraciones"])
    L.append("| Marco | vs 2121-2420 | vs 264-563 |")
    L.append("|---|---|---|")
    for marco in ("contexto", "recorte"):
        c = p["fracciones"][marco]["en conjunto"]
        fila = []
        for riv in ("vs_2121-2420", "vs_264-563"):
            v = c[riv]
            fila.append(("%+.1f (de %+d a %+d)" % (v["dif_mediana"], v["dif_min"],
                                                   v["dif_max"])).replace(".", ","))
        L.append("| %s | %s | %s |" % (marco, fila[0], fila[1]))
    L.append("")

    L.append("## Eje de referencia — eficiencia recalculada y coincidencias\n")
    L.append("Fuente: `resultados/referencia_resumen.json`. %s. «Recalculada» es el "
             "conteo de la molecula recortada **tal como la escribe esa fuente**; "
             "«idénticas» cuenta, de las ventanas eficientes de la secuencia de EPILAB en "
             "contexto, cuantas existen identicas en esa fuente.\n" % r["motor"])
    L.append("| Fuente | Region | Cobertura de la region | Eficientes recalculadas "
             "(corregido) | Eficientes (EPILAB, contexto) | Identicas | Variantes | Cruzan "
             "empalme | Sin datos |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for fuente, v in r["veredicto"].items():
        for region in r["regiones"]:
            co = v["coincidencias_corregido"][region]
            rec = recalc.get((fuente, region), "")
            cob = "completa" if region in v["regiones_con_cobertura_total_de_ventanas"] \
                else "parcial"
            L.append("| %s | %s | %s | %s | %d | %d | %d | %d | %d |" % (
                fuente, region, cob,
                rec if rec else "no corrida",
                co["eficientes"], co["identicas"], co["variantes"],
                co["cruzan_empalme"], co["sin_datos"]))
    L.append("")
    L.append("Conteos de la molecula recortada de EPILAB, para comparar: " +
             "; ".join("%s = %d (corregido), %d (fiel)" % (k, v["corregido"], v["fiel"])
                       for k, v in r["recorte_epilab"].items()) + ".")
    L.append("")

    # -- eje 3: sensibilidad al criterio de riesgo ---------------------------------------
    ruta3 = SALIDA / "riesgo_sensibilidad.json"
    if ruta3.exists():
        s = json.loads(ruta3.read_text(encoding="utf-8"))
        L.append("## Eje de criterios de riesgo — sensibilidad, no adopcion\n")
        L.append("Fuente: `resultados/riesgo_sensibilidad.json`. **No elige regla**: mide "
                 "cuanto cambia la comparacion segun cual se elija, que es lo que M6 (#10) "
                 "tiene que decidir. Panel de C7 v2 (%s), sin los pesos de D18. "
                 "«Limpias y eficientes» es eficiente y sin coincidencia, y **no depende de "
                 "la regla**: una ventana eficiente con coincidencia es riesgosa para las "
                 "dos. Lo que la regla cambia es el tamano del riesgo declarado.\n"
                 % ", ".join(s["panel"]))
        L.append("| Umbral (D28) | Marco | Config. | 922-1221 gana a 2121-2420 | gana a "
                 "264-563 | Alertas, regla conservadora (922 / 2121 / 264) | Alertas, regla "
                 "mecanicista |")
        L.append("|---|---|---|---|---|---|---|")
        for clave, b in s["por_combinacion"].items():
            marco, umbral = [x.strip() for x in clave.split("/")]
            con = b["riesgo_conservadora_en_vienna_NN3_corregido_defecto"]
            mec = b["riesgo_mecanicista_en_vienna_NN3_corregido_defecto"]
            L.append("| `%s` | %s | %d | %s | %s | %d / %d / %d | %d / %d / %d |" % (
                umbral, marco, b["configuraciones"],
                pct(b["limpias_eficientes_vs_2121-2420"]["gana_pct"]),
                pct(b["limpias_eficientes_vs_264-563"]["gana_pct"]),
                con["922-1221"], con["2121-2420"], con["264-563"],
                mec["922-1221"], mec["2121-2420"], mec["264-563"]))
        L.append("")
        L.append("Las columnas de alertas estan medidas en ViennaRNA 2.7.2, tabla NN3, modo "
                 "`corregido` y punto por defecto. El conteo de la regla conservadora no "
                 "depende de la configuracion —es coincidencia exacta de secuencia—; el de "
                 "la mecanicista si, y sobre las ocho celdas del punto por defecto su rango "
                 "es %s." % "; ".join(
                     "%s %s" % (k, v) for k, v in
                     s["por_combinacion"]["contexto / perfecto_ge19"][
                         "riesgo_mecanicista_rango_en_las_celdas_por_defecto"].items()))
        L.append("")
        c21 = s["ventanas_con_coincidencia_en_el_gen"]["perfecto_21"]
        c19 = s["ventanas_con_coincidencia_en_el_gen"]["perfecto_ge19"]
        L.append("Ventanas del gen con coincidencia en el panel: %d con `perfecto_21` y %d "
                 "con `perfecto_ge19`. **Control de D59** (baja complejidad, que es lo que "
                 "inflaba los conteos del MRFV con la cola de poli-A): de esas, %d y %d son "
                 "de baja complejidad, y en las 2.500 ventanas del gen hay %d. Ninguna "
                 "alerta de esta tabla es un artefacto de poli-A." % (
                     c21["total"], c19["total"], c21["de_baja_complejidad"],
                     c19["de_baja_complejidad"],
                     s["ventanas_de_baja_complejidad_en_el_gen"]))

    (SALIDA / "tabla_unica.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
