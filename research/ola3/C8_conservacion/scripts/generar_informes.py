"""Genera REPORT.md e index.html de C8 desde `resultados/conservacion.json`.

Misma mecanica que C7: una sola fuente de prosa que se vuelca a los dos formatos, con las
tablas sacadas del JSON. Uso, desde la raiz del repositorio:
    python research/ola3/C8_conservacion/scripts/generar_informes.py
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
REPO = RAIZ.parents[2]
D = json.loads((RAIZ / "resultados" / "conservacion.json").read_text(encoding="utf-8"))
V2 = json.loads((REPO / "research/ola3/C7_ranking_v2/resultados/ranking_v2.json")
                .read_text(encoding="utf-8"))


def c(x, nd=4):
    return ("%.*f" % (nd, x)).replace(".", ",")


def pc(x, nd=0):
    return ("%.*f" % (nd, x)).replace(".", ",") + " %"


def reg(r):
    return "%d-%d" % tuple(r)


def alt_v2(gen, region):
    """Fila de las alternativas de C7 (k = 21) para una region, si esta entre las listadas."""
    for forma in ("cascada", "geometrica"):
        for m in V2["k"]["21"]["alternativas"][gen][forma]["mejores"]:
            if m["region"] == region:
                return m
    return None


# --------------------------------------------------------------------------- tablas

def t_fuentes():
    cab = ["Fuente", "Qué es", "Origen declarado", "Tecnología", "Papel en este análisis"]
    filas = [
        ["`GCA_975739785.1` (hap1)", "genoma cromosómico", "Reino Unido, muestra de 2024-11-11 (BioProject PRJEB97791)",
         "PacBio y Arima2", "línea de base: separa las ventanas que caen en un empalme"],
        ["`GCA_975739835.1` (hap2)", "haplotipo alternativo, 488 Mb en 8.928 contigs", "el mismo individuo",
         "PacBio y Arima2", "descripción; **está incompleto en estos loci** y no entra al criterio"],
        ["`GCA_054756405.1` (CIAP v1)", "genoma a nivel de contig, 585 Mb, N50 de 50,5 kb",
         "**Argentina: Córdoba**, muestra de 2024-05-27 (INTA)", "Oxford Nanopore MinION, Flye",
         "descripción; con tasa de error del orden de la variación que se busca, no entra al criterio"],
        ["`GCWP01` (TSA)", "transcriptoma", "Illinois Natural History Survey (Johnson *et al.*, sin publicar)",
         "454, Newbler", "criterio; cubre solo fragmentos de `BicC_Dm`"],
        ["`GITV01` (TSA)", "transcriptoma", "Ohio State University (Xu y Stewart; BioProject PRJNA631706)",
         "Illumina HiSeq, CLC", "criterio"],
        ["`GHCC01` (TSA)", "transcriptoma de huevos, cuerpo entero",
         "**Argentina**, colecta de 2015-03-01; depositado desde el CeBio, Pergamino (BioProject PRJNA505619)",
         "Illumina HiSeq, Trinity", "criterio, y la fuente argentina de mejor calidad"],
    ]
    return cab, filas


def t_amplicones():
    A = D["amplicones"]
    filas = []
    for g in ("eth_Dm", "bursA_Dm"):
        a = A[g]
        ds = a["dsRNA_a"] or a["dsRNA_b"]
        filas.append([
            "`%s`" % g, "%d pb" % a["largo_amplicon"],
            "%s %d–%d (%s); el otro cebador no está en la secuencia pública" % (
                "un cebador en", ds["inicio"], ds["fin"], "hebra " + ds["hebra_del_cebador"]),
            "%d a %d" % tuple(a["amplicon_coordenadas"]),
            "%d–%d de %d" % (a["en_secuencia_publica"][0], a["en_secuencia_publica"][1],
                              a["largo_secuencia_publica"]),
            "%d nt" % a["fuera_de_la_secuencia_publica_nt"],
            ("%d–%d" % tuple(a["qPCR_amplicon"])) if a.get("qPCR_amplicon") else "5′ de la secuencia pública"])
    return (["Gen", "ARNdc declarado", "Cebadores", "Amplicón (coordenadas de la secuencia pública)",
             "Parte dentro de la secuencia pública", "Fuera (UTR)", "qPCR"], filas)


def t_region_probada():
    filas = []
    for k in ("21", "22"):
        for g in ("eth_Dm", "bursA_Dm"):
            x = D["region_probada"][k][g]
            p, m = x["propuesta_v2"], x["mejor_dentro_de_lo_probado"]
            filas.append(["%s nt" % k, "`%s`" % g, "%d–%d" % tuple(x["cubierto"]),
                          "%s (ocupa %d–%d)" % (reg(p["region"]), p["ocupa"][0], p["ocupa"][1]),
                          pc(p["fraccion"] * 100), str(p["eficientes"]),
                          reg(m["region"]), str(m["eficientes"]), str(m["limpias_y_eficientes"])])
    return (["Ventana", "Gen", "Tramo probado", "Región propuesta en C7", "Dentro de lo probado",
             "Eficientes", "Mejor región dentro de lo probado", "Eficientes", "Limpias y eficientes"], filas)


def t_transcriptomas():
    filas = []
    for g in ("BicC_Dm", "ATPaseD_Dm"):
        r = D["insecto"][g]
        for f, x in r["transcriptomas"].items():
            tr = r["variantes_en_transcriptomas"][f]
            filas.append(["`%s`" % g, f, str(x["con_datos"]), str(x["conservadas"]), str(x["variantes"]),
                          "; ".join("%d–%d" % tuple(t) for t in tr) or "ninguno"])
    return (["Gen", "Fuente", "Ventanas con datos", "Idénticas", "Con diferencia",
             "Tramos de ventanas con diferencia (cada tramo de 41 es un solo cambio de base)"], filas)


def t_genomas():
    filas = []
    for g in ("BicC_Dm", "ATPaseD_Dm", "eth_Dm", "bursA_Dm"):
        r = D["insecto"][g]["genomas"]
        for f, x in r.items():
            if f == "UK hap1":
                filas.append(["`%s`" % g, "UK hap1 (línea de base)", str(x["exactas"]), str(x["un_desajuste"]),
                              str(x["ausentes"]), "—"])
            else:
                filas.append(["`%s`" % g, f, str(x["de_esas_exactas"]), str(x["de_esas_con_un_desajuste"]),
                              str(x["de_esas_ausentes"]), "%d presentes en hap1" % x["presentes_en_hap1"]])
    return (["Gen", "Genoma", "Ventanas exactas", "Con un desajuste", "Ausentes", "Sobre cuántas"], filas)


def t_regiones_insecto(g):
    R_ = D["regiones_insecto"][g]
    filas = []
    for et, rot in (("epilab", "elegida por EPILAB"), ("v2_recomendada", "recomendada en C7"),
                    ("mejor_por_conservacion", "mejor por conservación")):
        if et not in R_:
            continue
        x = R_[et]
        if g == "ATPaseD_Dm" and et == "mejor_por_conservacion":
            rot += " (vetada)"
        ex = x["eficientes"]
        filas.append([rot, reg(x["region"]), str(ex),
                      "%d (%s)" % (x["eficientes_conservadas_en_todos_los_transcriptomas"],
                                   pc(100 * x["eficientes_conservadas_en_todos_los_transcriptomas"] / ex)),
                      str(x["eficientes_conservadas_en_Argentina"]),
                      "%d / %d / %d" % (x["de_esas_exactas_en_CIAP"], x["de_esas_con_un_desajuste_en_CIAP"],
                                        x["de_esas_ausentes_en_CIAP"]),
                      str(x["con_21_perfecto"]), "sí" if x["vetada"] else "no",
                      str(x["limpias_y_eficientes"])])
    return (["Región", "Posiciones", "Eficientes", "Idénticas en los tres transcriptomas",
             "Idénticas en el argentino", "En Córdoba: exactas / un desajuste / ausentes",
             "Con 21/21 en el panel", "¿Vetada?", "Limpias y eficientes"], filas)


def t_eth_bursa():
    filas = []
    for g in ("eth_Dm", "bursA_Dm"):
        x = D["regiones_insecto"][g]["v2_recomendada"]
        filas.append(["`%s`" % g, reg(x["region"]), str(x["eficientes"]),
                      str(x["eficientes_presentes_en_hap1"]), str(x["de_esas_exactas_en_CIAP"]),
                      str(x["de_esas_con_un_desajuste_en_CIAP"]), str(x["de_esas_ausentes_en_CIAP"])])
    return (["Gen", "Región propuesta", "Eficientes", "Presentes en hap1", "Exactas en Córdoba",
             "Con un desajuste", "Ausentes"], filas)


def t_virus_registros():
    filas = []
    for g in ("MP_MRFV", "CP_MRFV"):
        v = D["virus"][g]
        filas.append(["`%s`" % g, str(v["registros_con_alineamiento"]),
                      ", ".join("%s %d" % (p, n) for p, n in v["por_pais"].items()),
                      str(v["cobertura_mediana"])])
    return (["Gen", "Registros de GenBank que lo cubren (de 71)", "Por país", "Mediana de registros por ventana"], filas)


def t_cp_umbrales():
    v = D["virus"]["CP_MRFV"]["resumen"]
    filas = []
    for et, rot in (("todos", "todos los registros"), ("solo_Brasil", "solo los 42 brasileños")):
        x = v[et]
        filas.append([rot, str(x["ventanas_con_al_menos_10_registros"]), str(x["conservadas_ge_90"]),
                      str(x["conservadas_ge_75"]), str(x["conservadas_ge_50"])])
    return (["Registros considerados", "Ventanas evaluables (≥10 registros)", "Idénticas en ≥90 %",
             "≥75 %", "≥50 %"], filas)


def t_cp_regiones():
    filas = []
    for g in ("CP_MRFV",):
        for et, rot in (("epilab", "elegida por EPILAB"), ("v2_recomendada", "recomendada en C7"),
                        ("mejor_por_conservacion", "mejor por conservación")):
            x = D["regiones_virus"][g]["todos"][et]
            filas.append([rot, reg(x["region"]), str(x["eficientes"]), str(x["eficientes_conservadas"]),
                          pc(100 * x["eficientes_conservadas"] / x["eficientes"])])
    return (["Región de `CP_MRFV`", "Posiciones", "Eficientes", "Idénticas en ≥75 % de los registros",
             "Fracción"], filas)


def t_ranking():
    rk = D["ranking_con_region_conservada"]
    filas = []
    for et, rot in (("v2_recomendadas", "regiones de C7"), ("con_BicC_por_conservacion", "con `BicC_Dm` en 922-1221")):
        x = rk[et]
        o = x["geometrica_conservadora_absoluta"]["orden_modal"]
        fr = x["geometrica_conservadora_absoluta"]["frecuencia"]
        filas.append([rot, " > ".join("`%s`" % n for n in o["orden"]), pc(o["pct"], 1),
                      pc(fr["BicC_Dm"][1]) + " segundo"])
    return (["Escenario", "Orden más frecuente (media geométrica, escala absoluta)", "Frecuencia",
             "`BicC_Dm`"], filas)


# ------------------------------------------------------------------------ documento

def construir():
    b = []

    def H(n, t):
        b.append(("h%d" % n, t))

    def P(t):
        b.append(("p", t))

    def T(cab, filas, nota=None):
        b.append(("tabla", cab, filas, nota))

    def BOX(t):
        b.append(("box", t, False))

    A = D["amplicones"]
    BR = D["regiones_insecto"]["BicC_Dm"]
    AT = D["regiones_insecto"]["ATPaseD_Dm"]
    VCP = D["virus"]["CP_MRFV"]
    rp21 = D["region_probada"]["21"]
    r_a = alt_v2("BicC_Dm", "2121-2420")
    r_b = alt_v2("BicC_Dm", "922-1221")
    rk = D["ranking_con_region_conservada"]

    H(1, "Conservación entre poblaciones y aislados, y qué parte de la molécula probada cubren nuestras regiones")
    P("Fecha: 2026-10-21. Complementa [`research/ola3/C7_ranking_v2/REPORT.md`](../C7_ranking_v2/REPORT.md). "
      "Reproducible con `tools/sifi21_port/conservacion.py`; los números salen de `resultados/conservacion.json`. "
      "Marcadores de `CLAUDE.md`.")

    H(2, "El resultado, en un párrafo")
    P("**Una recomendación de C7 cambia, una aguanta, y para dos candidatos virales el dato no alcanza.** "
      "En `BicC_Dm`, la región que C7 recomienda (%s) tiene %d eficientes y solo %d son idénticas en los tres "
      "transcriptomas públicos de *D. maidis*; la región %s tiene %d eficientes, %d idénticas en los tres, "
      "%d de %d idénticas en el transcriptoma argentino y las %d presentes en el genoma de Córdoba son exactas. "
      "Es la misma región que C6 había encontrado como salida al veto de *Macrosteles*, y ahora aparece por un "
      "motivo que no depende de ese pariente. Cambiarla no mueve el ranking de diseño (`BicC_Dm` sigue segundo, "
      "%s de los sorteos). En `ATPaseD_Dm`, la región de C7 (%s) aguanta: sus %d eficientes son idénticas en los "
      "tres transcriptomas y en Córdoba. En el virus, `CP_MRFV` es frágil —de las %d eficientes de la región de EPILAB solo "
      "%d están en el 75 %% o más de los registros que las cubren— y `MP_MRFV`, el primero del ranking, no se puede "
      "evaluar: solo %d de 71 registros de GenBank la cubren y dos de ellos son la referencia. "
      "Por último, los cebadores publicados ubican el ARNdc de `eth` (544 pb) sobre la secuencia codificante 1–446 y el de "
      "`burs-alpha` (578 pb) sobre 79–468 más 188 nt de 3′UTR `[H]`: la región propuesta para `eth` queda entera dentro "
      "de lo probado, y la de `burs-alpha` solo en un %s." % (
          reg(BR["v2_recomendada"]["region"]), BR["v2_recomendada"]["eficientes"],
          BR["v2_recomendada"]["eficientes_conservadas_en_todos_los_transcriptomas"],
          reg(BR["mejor_por_conservacion"]["region"]), BR["mejor_por_conservacion"]["eficientes"],
          BR["mejor_por_conservacion"]["eficientes_conservadas_en_todos_los_transcriptomas"],
          BR["mejor_por_conservacion"]["eficientes_conservadas_en_Argentina"],
          BR["mejor_por_conservacion"]["eficientes"], BR["mejor_por_conservacion"]["de_esas_exactas_en_CIAP"],
          pc(rk["con_BicC_por_conservacion"]["geometrica_conservadora_absoluta"]["frecuencia"]["BicC_Dm"][1]),
          reg(AT["v2_recomendada"]["region"]), AT["v2_recomendada"]["eficientes"],
          D["regiones_virus"]["CP_MRFV"]["todos"]["epilab"]["eficientes"],
          D["regiones_virus"]["CP_MRFV"]["todos"]["epilab"]["eficientes_conservadas"],
          D["virus"]["MP_MRFV"]["registros_con_alineamiento"],
          pc(100 * rp21["bursA_Dm"]["propuesta_v2"]["fraccion"])))

    BOX("**Lo que se deduce, en cinco líneas.** (1) La recomendación de región para `BicC_Dm` pasa de 2121-2420 a "
        "922-1221: más conservada en todas las fuentes y sin costo en el ranking. (2) La de `ATPaseD_Dm` (72-371) "
        "se mantiene. (3) `CP_MRFV` tiene pocas ventanas eficientes que sobrevivan a la variación entre aislados, y de "
        "`MP_MRFV` no sabemos nada porque no hay registros. (4) Nuestra región de `burs-alpha` cubre solo el 70 % de lo "
        "probado y hay una alternativa dentro de lo probado que cuesta dos ventanas eficientes. (5) Todo esto es "
        "conservación entre fuentes públicas y no entre poblaciones de campo del noroeste argentino, que no tenemos.")

    H(2, "1. Qué parte de la molécula probada cubren nuestras regiones")
    P("La Tabla 1 de Andrada *et al.* 2026 (PMC13279319) da los cebadores del ARNdc y de la qPCR de `eth` y `burs-alpha`, "
      "pero no sus posiciones: el texto remite a la Figura S1, que no se leyó, y no dice si los amplicones incluyen UTR. "
      "Lo que sigue **es una inferencia nuestra** `[H]`: se buscó cada cebador en las dos hebras de la secuencia "
      "pública (GenBank PZ371507.1 y PZ371508.1, que son la secuencia codificante) y se dedujo la orientación de dónde "
      "aparece. Los rótulos \"forward\" y \"reverse\" de la tabla no coinciden con la orientación real: el \"forward\" del ARNdc de `eth` "
      "es antisentido sobre la secuencia. Un cebador con la secuencia del sentido se extiende hacia 3′; uno con la "
      "del antisentido, hacia 5′. Con un cebador ubicado y el largo declarado del amplicón se obtiene el otro extremo, "
      "que cae fuera de la secuencia pública y por lo tanto es UTR.")
    T(*t_amplicones())
    P("Dos lecturas. El ARNdc de `eth` cubre el 72 % de la secuencia codificante (1–446 de 615) más 98 nt río arriba; el de "
      "`burs-alpha` cubre 79–468 más 188 nt de 3′UTR, es decir que le falta el primer sexto de la secuencia codificante. "
      "Y en `burs-alpha` el amplicón de la qPCR (90 pb) cae río arriba del ARNdc, mientras que en `eth` se solapa con "
      "apenas 19 nt: las dos mediciones se hicieron en gran parte fuera de la región silenciada, que es la práctica "
      "correcta para no detectar el ARNdc inyectado `[H]`.")
    T(*t_region_probada())
    P("`[E]` **`eth`: la región propuesta en C7 (%s) está entera dentro de lo probado**, a 21 y a 22 nt. "
      "**`burs-alpha`: no.** La propuesta a 21 nt (13-212) ocupa 13–232, y solo 79–232 (%s) está dentro; a 22 nt, el %s. "
      "La mejor región enteramente dentro de lo probado es %s a 21 nt (%d eficientes y %d limpias y eficientes, contra "
      "%d de la propuesta) y %s a 22 nt (%d contra %d). Cuesta dos ventanas eficientes y deja el argumento "
      "limpio: cada nucleótido de la región propuesta pertenece a una molécula que se probó." % (
          reg(rp21["eth_Dm"]["propuesta_v2"]["region"]), pc(100 * rp21["bursA_Dm"]["propuesta_v2"]["fraccion"]),
          pc(100 * D["region_probada"]["22"]["bursA_Dm"]["propuesta_v2"]["fraccion"]),
          reg(rp21["bursA_Dm"]["mejor_dentro_de_lo_probado"]["region"]),
          rp21["bursA_Dm"]["mejor_dentro_de_lo_probado"]["eficientes"],
          rp21["bursA_Dm"]["mejor_dentro_de_lo_probado"]["limpias_y_eficientes"],
          rp21["bursA_Dm"]["propuesta_v2"]["eficientes"],
          reg(D["region_probada"]["22"]["bursA_Dm"]["mejor_dentro_de_lo_probado"]["region"]),
          D["region_probada"]["22"]["bursA_Dm"]["mejor_dentro_de_lo_probado"]["eficientes"],
          D["region_probada"]["22"]["bursA_Dm"]["propuesta_v2"]["eficientes"]))
    P("Un límite que conviene decir: las ventanas se calculan sobre la secuencia codificante, así que los 98 nt de 5′UTR "
      "de `eth` y los 188 nt de 3′UTR de `burs-alpha` que sí estaban en la molécula probada no se pueden evaluar "
      "con lo que tenemos. Y lo que se probó fue la molécula completa, no una región de 200 nt: que esa región silencie "
      "como la molécula entera sigue sin estar demostrado `[H]`.")

    H(2, "2. De dónde sale la conservación, y qué tan buena es cada fuente")
    P("No tenemos poblaciones de campo. Lo que existe en bases públicas son tres transcriptomas de *D. maidis* y tres "
      "ensamblados genómicos, de orígenes distintos. La procedencia de cada uno se leyó en su registro de GenBank y en el "
      "informe de ensamblado de NCBI.")
    T(*t_fuentes())
    P("Tres precauciones de método. **Primera:** el criterio de \"conservada\" usa solo los transcriptomas, que no tienen "
      "intrones ni la tasa de error del ONT. **Segunda:** el haplotipo 2 del Reino Unido es un ensamblado alternativo "
      "incompleto —no contiene los loci de `ATPaseD_Dm`, `eth` ni `burs-alpha` (0, 1 y 0 ventanas exactas)— y usarlo como fuente "
      "habría contado como variación lo que es un hueco; un primer intento lo hizo y dio números absurdos. "
      "**Tercera:** el genoma de Córdoba es solo ONT a 20x, de modo que una ventana con un desajuste puede ser variación o "
      "error de lectura; por eso se reporta en tres categorías (exacta, un desajuste, ausente) y no se usa para excluir. "
      "Además, un alineamiento local puede esconder una inserción: se marcó como \"con diferencia\" toda ventana que "
      "cruza un salto entre bloques alineados, que es lo que detectó la inserción de 36 nt del transcriptoma argentino "
      "en `BicC_Dm`.")

    H(2, "3. Insecto: lo que dicen los transcriptomas y el genoma de Córdoba")
    P("`[E]` `BicC_Dm` es idéntico al 99,88 % al transcriptoma argentino sobre 2.520 nt (tres cambios de base y una inserción "
      "de 36 nt en ese transcriptoma, en la posición 1409) y al 99,72 % al de Ohio (siete cambios de base). `ATPaseD_Dm` "
      "es idéntica al 100 % al contig de Illinois y al 99,80 % a los de Ohio y Argentina, **con un único cambio de base "
      "en las mismas ventanas (242–282) de los dos y ausente en el de Illinois**. Eso es consistente con lo que W5 ya "
      "había anotado (§2.5): la secuencia de `ATPaseD_Dm` es un fragmento exacto de un contig público y lleva el alelo del de "
      "Illinois `[H]`. Anotamos acá que la frase de D21 \"no son subcadenas de nada publicado\" no vale para `ATPaseD_Dm`; "
      "la decisión no cambia —las dos siguen tratándose como confidenciales y no se subieron— pero la frase hay que corregirla.")
    T(*t_transcriptomas())
    T(*t_genomas(), nota="Para los dos genomas que no son la línea de base, los conteos son sobre las ventanas que sí están en "
      "hap1, para no confundir un empalme con una diferencia. Un genoma no tiene la secuencia continua de un transcrito: "
      "las ventanas que cruzan un intrón faltan en todos, y por eso hap1 no llega al total.")
    H(3, "`BicC_Dm`: la región recomendada cambia")
    T(*t_regiones_insecto("BicC_Dm"))
    P("`[E]` Las ventanas eficientes de la región que recomendó C7 (%s) se pierden en las otras fuentes porque caen sobre "
      "los cambios de base de los transcriptomas (ventanas 2123–2163 y 2288–2349 en el de Ohio, 2240–2280 en el argentino y varios "
      "más en los fragmentos de Illinois), donde la tecnología (454) produce errores de homopolímero que no se pueden "
      "separar de variación real `[H]`. En el transcriptoma argentino las 35 eficientes son idénticas; la pérdida está en "
      "Ohio y en Illinois. Y en el genoma de Córdoba, %d de las %d eficientes presentes en hap1 no aparecen, con la "
      "salvedad del ONT. La región %s no tiene ese problema: %d de %d idénticas en los tres transcriptomas, todas en el "
      "argentino y las %d presentes exactas en Córdoba." % (
          reg(BR["v2_recomendada"]["region"]), BR["v2_recomendada"]["de_esas_ausentes_en_CIAP"],
          BR["v2_recomendada"]["eficientes_presentes_en_hap1"], reg(BR["mejor_por_conservacion"]["region"]),
          BR["mejor_por_conservacion"]["eficientes_conservadas_en_todos_los_transcriptomas"],
          BR["mejor_por_conservacion"]["eficientes"], BR["mejor_por_conservacion"]["de_esas_exactas_en_CIAP"]))
    P("`[E]` **El costo es chico.** La región 922-1221 tiene %d eficientes contra %d, %d limpias y eficientes contra %d y "
      "%d ventanas con alguna señal de off-target contra %d; ninguna de las dos tiene coincidencias perfectas de 21 nt "
      "con el panel. Con la región cambiada, el orden de diseño no se mueve (tabla de abajo). La región de EPILAB (264-563) "
      "es la más conservada de las tres —sus 20 eficientes son idénticas en todo— y sigue vetada por *H. vitripennis*, así que "
      "la conservación no la rescata." % (
          BR["mejor_por_conservacion"]["eficientes"], BR["v2_recomendada"]["eficientes"],
          BR["mejor_por_conservacion"]["limpias_y_eficientes"], BR["v2_recomendada"]["limpias_y_eficientes"],
          r_b["con_off_target"] if r_b else 0, r_a["con_off_target"] if r_a else 0))
    T(*t_ranking())
    H(3, "`ATPaseD_Dm`: la recomendación aguanta")
    T(*t_regiones_insecto("ATPaseD_Dm"))
    P("`[E]` Las %d eficientes de 72-371 son idénticas en los tres transcriptomas y las %d presentes en hap1 están exactas en "
      "Córdoba: el cambio de base de las ventanas 242–282 no toca ninguna eficiente de esa región. La región más densa del gen "
      "(137-436) tiene 24 eficientes pero está vetada por *H. vitripennis*, así que la conservación no la recomienda." % (
          AT["v2_recomendada"]["eficientes"], AT["v2_recomendada"]["eficientes_presentes_en_hap1"]))
    H(3, "`eth` y `burs-alpha`: sin transcriptoma, solo una descripción")
    P("No ubicamos contigs de estos dos genes en los transcriptomas: la búsqueda contra el TSA de NCBI (con las secuencias públicas "
      "PZ371507 y PZ371508, no con las de EPILAB) quedó en cola más de media hora sin resultado y se canceló. Su conservación "
      "solo se puede describir con el genoma de Córdoba, que es la fuente menos confiable. No se afirma conservación ni "
      "variación: se reporta lo que aparece. Es un pendiente concreto: un transcriptoma de *D. maidis* que contenga `eth` y "
      "`burs-alpha` permitiría hacer con ellos lo que acá se hizo con `BicC_Dm` y `ATPaseD_Dm`. `[?]`")
    T(*t_eth_bursa())
    P("`[?]` En `eth` 17 de 19 eficientes están exactas y 2 ausentes; en `burs-alpha`, 12 exactas y 4 con un desajuste. Con un ensamblado "
      "ONT eso es compatible con error y con variación a la vez, y no permite decidir.")

    H(2, "4. Virus: `MP_MRFV` no se puede evaluar y `CP_MRFV` es frágil")
    P("Se alineó cada gen contra los 71 registros de MRFV de GenBank (los mismos de W5, rebajados de NCBI) y se midió, ventana por "
      "ventana, en cuántos de los registros que la cubren es idéntica. Ningún registro es argentino: de los 71, 45 son de Brasil, 4 de "
      "EE. UU., 2 de Ecuador, 1 de Costa Rica y 19 no declaran país `[E]`.")
    T(*t_virus_registros())
    P("`[E]` **`MP_MRFV`: cuatro registros alinean y dos son la referencia** (NC_002786.2 y AF265566.2). Los otros dos son "
      "un registro de EE. UU. completo (KM523134.1, 93,75 % de identidad sobre el gen) y un fragmento brasileño de 40 nt. "
      "No hay ventana con diez registros que la cubran. Es el candidato que el ranking de diseño pone primero, y su robustez "
      "frente a la variación entre aislados **no se puede medir con lo que hay publicado**; contra el único aislado independiente "
      "disponible, W5 midió que solo 54 de las 180 ventanas de la región son idénticas. `[?]`")
    P("`[E]` **`CP_MRFV`: 65 registros cubren cada ventana, y pocas ventanas son idénticas en la gran mayoría: 118 de 505 llegan al 75 % y 11 al 90 %.**")
    T(*t_cp_umbrales())
    T(*t_cp_regiones())
    P("De las %d eficientes de la región de EPILAB, %d están en el 75 %% o más de los registros; en la que recomendó C7, 4 de 21. "
      "La mejor región por conservación (196-395) llega a 7 eficientes conservadas de 21. Es el reverso de lo que mostró el "
      "ranking: `CP_MRFV` es el candidato más limpio, pero casi todas sus ventanas eficientes dejan de ser idénticas en los "
      "aislados brasileños, que son los de mayor peso en la muestra. Una región limpia que funciona en un solo aislado no sirve, "
      "y acá la cifra es 7. Pesa menos de lo que parece porque un ARNdc largo se procesa en un conjunto de siRNA y no todos "
      "necesitan ser idénticos, pero no tenemos con qué cuantificarlo. `[H]`" % (
          D["regiones_virus"]["CP_MRFV"]["todos"]["epilab"]["eficientes"],
          D["regiones_virus"]["CP_MRFV"]["todos"]["epilab"]["eficientes_conservadas"]))

    H(2, "5. Qué cambia en el ranking de C7")
    P("`[H]` Tres cosas. **Primera:** para `BicC_Dm`, la región recomendada pasa a 922-1221 sin costo en el orden de diseño. "
      "**Segunda:** el primer puesto de `MP_MRFV` descansa en un candidato cuya variación entre aislados es desconocida, y el "
      "tercero de `CP_MRFV` en uno con muy pocas ventanas conservadas; las dos cosas deben ir junto al orden de diseño y no "
      "debajo. **Tercera:** el argumento de que los candidatos del insecto tienen más respaldo que los virales gana un "
      "componente que no tenía: sus regiones recomendadas son idénticas en fuentes argentinas y las virales no se pueden "
      "evaluar o no lo aguantan. Esto es una lectura de datos públicos y no una medición sobre poblaciones de campo.")

    H(2, "6. Límites")
    P("La conservación entre fuentes públicas no es conservación entre poblaciones de campo: son tres transcriptomas "
      "de laboratorio o de colonia y un genoma de una muestra de Córdoba, y ninguno fue diseñado para medir variación. Con tres "
      "fuentes una ventana \"idéntica en todas\" no descarta variación en una cuarta. Los fragmentos de Illinois (454) "
      "mezclan variación y error de secuenciación. El criterio de MRFV (idéntica en al menos el 75 % de los registros que "
      "cubren la ventana, con al menos diez) es una decisión nuestra; la tabla da los umbrales de 50, 75 y 90 % para que se "
      "vea cuánto cambia. Los registros brasileños pesan 42 de 65, de modo que la muestra describe a Brasil más que "
      "a cualquier otro lugar. El análisis se hizo a 21 nt y no se repitió a 22. Por último, quedan sin evaluar los 98 nt de "
      "5′UTR de `eth` y los 188 de 3′UTR de `burs-alpha`, y las posiciones exactas de los amplicones dependen de la Figura S1 "
      "del artículo, que no se leyó. `[?]`")

    H(2, "7. Cómo reproducirlo")
    P("Fuentes, todas públicas y bajadas a disco (solo entró tráfico): los dos genomas "
      "`GCA_975739835.1_ihDalMaid1.1_alternate_haplotype` (135,0 MB) y `GCA_054756405.1_CIAP_v1` (179,9 MB) del FTP de NCBI "
      "bajo `genomes/all/GCA/`; los nueve contigs TSA de `tsa/` (`GITV01000968.1`, `GITV01001458.1`, `GHCC01002326.1`, "
      "`GHCC01051703.1`, `GCWP01003534.1`, `GCWP01003535.1`, `GCWP01004692.1`, `GCWP01004693.1`, `GCWP01010867.1`), que son "
      "los que W5 ya había ubicado; y los 71 registros de MRFV, por E-utilities (`Maize rayado fino virus[Organism]`).")
    b.append(("codigo", """# off-targets de los cuatro genes del insecto contra los dos genomas nuevos
python tools/sifi21_port/offtarget_21nt.py --size 21 --mm1 --consulta work/sifi_v2/fasta/{BicC_Dm,ATPaseD_Dm,eth_Dm,bursA_Dm}_full.fasta \\
    --db <genomas>/GCA_975739835.1*.fna.gz --salida work/sifi_v2/cons_hap2
python tools/sifi21_port/offtarget_21nt.py --size 21 --mm1 --consulta work/sifi_v2/fasta/{BicC_Dm,ATPaseD_Dm,eth_Dm,bursA_Dm}_full.fasta \\
    --db <genomas>/GCA_054756405.1*.fna.gz --salida work/sifi_v2/cons_ciap

# la conservación, los amplicones y el efecto sobre el ranking
python tools/sifi21_port/conservacion.py --datos <dir con tsa/ mrfv/ gen/> \\
    --json research/ola3/C8_conservacion/resultados/conservacion.json

# este informe y su página
python research/ola3/C8_conservacion/scripts/generar_informes.py"""))
    P("Necesita `ViennaRNA`, `biopython`, `pyahocorasick` y `numpy`, y los resultados de C7 en `work/sifi_v2/`.")
    return b


# --------------------------------------------------------------------------- render

def inline_html(t: str) -> str:
    out = []
    for p in re.split(r"(`[^`]*`)", t):
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append("<code>%s</code>" % html.escape(p[1:-1]))
            continue
        p = html.escape(p, quote=False)
        p = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', p)
        p = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", p)
        p = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", p)
        out.append(p)
    return "".join(out)


def a_md(bloques) -> str:
    out = []
    for bl in bloques:
        t = bl[0]
        if t == "h1":
            out.append("# %s\n" % bl[1])
        elif t == "h2":
            out.append("\n## %s\n" % bl[1])
        elif t == "h3":
            out.append("\n### %s\n" % bl[1])
        elif t == "p":
            out.append(bl[1] + "\n")
        elif t == "box":
            out.append("> " + bl[1] + "\n")
        elif t == "codigo":
            out.append("```bash\n%s\n```\n" % bl[1])
        elif t == "tabla":
            cab, filas, nota = bl[1], bl[2], bl[3]
            out.append("| " + " | ".join(cab) + " |")
            out.append("|" + "|".join("---" for _ in cab) + "|")
            for f in filas:
                out.append("| " + " | ".join(f) + " |")
            out.append("")
            if nota:
                out.append("*%s*\n" % nota)
    return "\n".join(out)


CSS = """:root{--bg:#fff;--fg:#1c1f23;--mut:#5b6470;--line:#dfe3e8;--card:#f5f7f9;--azul:#2a6fdb;
--rojo:#c23b3b;--verde:#1f7a4d}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#14171a;--fg:#e6e8eb;
--mut:#9aa4af;--line:#2b3138;--card:#1b1f24;--azul:#6aa3ff;--rojo:#ff8a8a;--verde:#5fd09a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,sans-serif}
main{max-width:980px;margin:0 auto;padding:28px 16px 60px}
.k{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
h1{font-size:26px;margin:6px 0 4px;line-height:1.2}h2{font-size:19px;margin:34px 0 10px}
h3{font-size:16px;margin:22px 0 6px}.lead{color:var(--mut);margin:0 0 18px}
.box{background:var(--card);border-left:3px solid var(--azul);padding:12px 16px;border-radius:6px;margin:16px 0}
.box p{margin:6px 0}
table{width:100%;border-collapse:collapse;font-size:14px;margin:4px 0}
th,td{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{color:var(--mut);font-weight:600;font-size:13px}.tw{overflow-x:auto;margin:8px 0}
.fine{font-size:13px;color:var(--mut)}code{font-size:.92em}
pre{background:var(--card);padding:12px;border-radius:6px;overflow-x:auto;font-size:13px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin:14px 0}
.kpi{border:1px solid var(--line);border-radius:8px;padding:10px 12px}
.kpi b{display:block;font-size:22px}.kpi span{font-size:13px;color:var(--mut)}
@media (max-width:600px){main{padding:20px 16px 50px}h1{font-size:22px}}"""


def a_html(bloques) -> str:
    cuerpo, primero = [], True
    for bl in bloques:
        t = bl[0]
        if t == "h1":
            continue
        if t == "h2":
            cuerpo.append("<h2>%s</h2>" % inline_html(bl[1]))
        elif t == "h3":
            cuerpo.append("<h3>%s</h3>" % inline_html(bl[1]))
        elif t == "p":
            if primero:
                primero = False
                continue
            cuerpo.append("<p>%s</p>" % inline_html(bl[1]))
        elif t == "box":
            cuerpo.append('<div class="box"><p>%s</p></div>' % inline_html(bl[1]))
        elif t == "codigo":
            cuerpo.append("<pre>%s</pre>" % html.escape(bl[1]))
        elif t == "tabla":
            cab, filas, nota = bl[1], bl[2], bl[3]
            th = "".join("<th>%s</th>" % inline_html(x) for x in cab)
            tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline_html(x) for x in f) for f in filas)
            cuerpo.append('<div class="tw"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                          % (th, tr))
            if nota:
                cuerpo.append('<p class="fine">%s</p>' % inline_html(nota))
    BR = D["regiones_insecto"]["BicC_Dm"]
    kpis = """<div class="kpis">
<div class="kpi"><b>%s → %s</b><span>región recomendada para <code>BicC_Dm</code>: 36 eficientes, %d idénticas en los tres transcriptomas</span></div>
<div class="kpi"><b>72-371 se mantiene</b><span><code>ATPaseD_Dm</code>: 21 de 21 eficientes idénticas en todas las fuentes</span></div>
<div class="kpi"><b>%d de 71</b><span>registros de MRFV cubren <code>MP_MRFV</code>: no se puede evaluar</span></div>
<div class="kpi"><b>%d de %d</b><span>eficientes de <code>CP_MRFV</code> (EPILAB) en ≥75 %% de los registros</span></div>
</div>""" % (reg(BR["v2_recomendada"]["region"]), reg(BR["mejor_por_conservacion"]["region"]),
             BR["mejor_por_conservacion"]["eficientes_conservadas_en_todos_los_transcriptomas"],
             D["virus"]["MP_MRFV"]["registros_con_alineamiento"],
             D["regiones_virus"]["CP_MRFV"]["todos"]["epilab"]["eficientes_conservadas"],
             D["regiones_virus"]["CP_MRFV"]["todos"]["epilab"]["eficientes"])
    cab = ('<!doctype html>\n<html lang="es"><head><meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
           "<title>Conservación entre poblaciones y aislados</title>\n<style>%s</style></head><body><main>\n"
           '<div class="k">Investigathon Y-Hat · track chicharrita / ARNi · ola 3 · C8</div>\n'
           "<h1>Conservación entre poblaciones y aislados, y qué cubre la molécula probada</h1>\n"
           '<p class="lead">2026-10-21. Complementa el <a href="../C7_ranking_v2/index.html">ranking v2</a>. '
           'Detalle y reproducción en <a href="REPORT.md">REPORT.md</a>.</p>\n' % CSS)
    return cab + kpis + "\n".join(cuerpo) + "\n</main></body></html>\n"


def main():
    bl = construir()
    (RAIZ / "REPORT.md").write_text(a_md(bl), encoding="utf-8")
    (RAIZ / "index.html").write_text(a_html(bl), encoding="utf-8")
    print("escrito REPORT.md e index.html en", RAIZ)


if __name__ == "__main__":
    main()
