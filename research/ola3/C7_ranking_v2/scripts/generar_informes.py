"""Genera REPORT.md e index.html de C7 desde `resultados/ranking_v2.json`.

Una sola fuente de prosa (`bloques`) que se vuelca a los dos formatos, para que la
pagina y el informe no puedan diverger, y todas las tablas salen del JSON y no de
numeros tipeados a mano. Los numeros que aparecen dentro de la prosa se calculan
aca (variables `v_*`) cuando se pudo; los pocos que son citas de otros informes
llevan su fuente al lado.

Uso (desde la raiz del repositorio):
    python research/ola3/C7_ranking_v2/scripts/generar_informes.py
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
D = json.loads((RAIZ / "resultados" / "ranking_v2.json").read_text(encoding="utf-8"))
K = {21: D["k"]["21"], 22: D["k"]["22"]}
NOMBRE = {"MP_MRFV": "MP_MRFV", "CP_MRFV": "CP_MRFV", "BicC_Dm": "BicC_Dm",
          "ATPaseD_Dm": "ATPaseD_Dm", "eth_Dm": "eth_Dm", "bursA_Dm": "bursA_Dm"}
ORDEN6 = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm", "eth_Dm", "bursA_Dm"]
GEO = "geometrica/conservadora/absoluta"


# ------------------------------------------------------------------ utilidades

def c(x, nd=4):
    """Numero con coma decimal, que es como escribe el resto del repositorio."""
    return ("%.*f" % (nd, x)).replace(".", ",")


def pc(x):
    return ("%.1f" % x).replace(".", ",") + " %"


def pc0(x):
    return ("%.0f" % x) + " %"


def ficha(k, gen, rec=False):
    lista = K[k]["fichas_recomendadas" if rec else "fichas"]
    return next(f for f in lista if f["gen"] == gen)


def barrido(k, conj, clave=GEO):
    return K[k]["barridos"][conj][clave]


def modal(k, conj, clave=GEO):
    o = barrido(k, conj, clave)["ordenes"][0]
    return o["pct"], o["orden"]


def flecha(orden):
    return " > ".join("`%s`" % g for g in orden)


# ----------------------------------------------------------------------- bloques

def tabla_fichas(k, rec=False):
    filas = []
    for g in ORDEN6:
        f = ficha(k, g, rec)
        e = f["conservadora"]
        quien = ("EPILAB" if g in ("MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm") and not rec
                 else "nuestra (cascada)")
        filas.append([
            "`%s`" % g, f["region"], quien, str(e["n_ventanas"]), str(e["eficientes"]),
            c(e["eficacia"]), c(e["limpieza"]), str(e["buenos_limpios"]),
            str(e["con_21_perfecto"]), "**sí**" if e["vetada"] else "no"])
    return (["Candidato", "Región", "La eligió", "Ventanas", "Eficientes", "Eficacia",
             "Limpieza", "Limpias y eficientes", "Con 21/21", "¿Vetada?"], filas)


def tabla_frecuencias(k, conj, clave=GEO):
    r = barrido(k, conj, clave)
    nombres = list(r["frecuencia"])
    cab = ["Candidato"] + ["Puesto %d" % (i + 1) for i in range(len(nombres))]
    filas = [["`%s`" % n] + [pc0(x) if x else "·" for x in r["frecuencia"][n]]
             for n in nombres]
    return cab, filas


def tabla_ordenes(k, conj):
    """Orden modal bajo cuatro combinaciones: lo que dice que tan sensible es a la regla."""
    filas = []
    for clave, rot in (("geometrica/conservadora/absoluta", "geométrica · conservadora · absoluta"),
                       ("geometrica/conservadora/minmax", "geométrica · conservadora · min-max"),
                       ("suma/conservadora/absoluta", "suma · conservadora · absoluta"),
                       ("cascada/conservadora", "cascada (veto + eficientes limpias)")):
        p, o = modal(k, conj, clave)
        filas.append([rot, pc(p), flecha(o)])
    return ["Combinación", "Frecuencia del orden", "Orden más frecuente"], filas


def tabla_gen_entero(k):
    G = K[k]["gen_entero"]
    refs = ["maiz", "H_axyridis", "A_mellifera", "H_vitripennis", "F_candida", "humano"]
    cab = ["Gen (secuencia pública completa)", "Ventanas", "Eficientes"] + [
        {"maiz": "maíz", "H_axyridis": "*H. axyridis*", "A_mellifera": "*A. mellifera*",
         "H_vitripennis": "*H. vitripennis*", "F_candida": "*F. candida*",
         "humano": "humano"}[r] for r in refs]
    filas = []
    for g in ("eth_Dm", "bursA_Dm", "BicC_Dm", "ATPaseD_Dm", "MP_MRFV", "CP_MRFV"):
        v = G[g]
        fila = ["`%s`" % g, str(v["ventanas"]), str(v["eficientes"])]
        for r in refs:
            x = v["por_referencia"].get(r)
            if not x:
                fila.append("·")
            else:
                fila.append("%d / %d / %d" % (x.get("perfecto_21", 0), x.get("perfecto_ge19", 0),
                                              x.get("mm1_21", 0)))
        filas.append(fila)
    return cab, filas


def tabla_k(gen_lista):
    filas = []
    for g in gen_lista:
        j = D["jaccard_21_22"][g]
        r21, r22 = K[21]["regiones_recomendadas"][g], K[22]["regiones_recomendadas"][g]
        filas.append(["`%s`" % g, str(j["k21"]), str(j["k22"]), str(j["en_ambos"]),
                      c(j["jaccard"], 2), r21, r22,
                      "estable" if abs(int(r21.split("-")[0]) - int(r22.split("-")[0])) <= 3
                      else "**se muda**"])
    return (["Candidato", "Eficientes a 21", "a 22", "En ambos", "Jaccard",
             "Región propuesta a 21", "a 22", "¿Aguanta?"], filas)


def tabla_nulo():
    filas = []
    for g in ("eth_Dm", "bursA_Dm"):
        n = K[21]["nulo_nuevos"][g]
        filas.append(["`%s`" % g, str(n["regiones_posibles"]), "%d–%d" % (n["minimo"], n["maximo"]),
                      c(n["mediana"], 0), str(n["maximo"]), c(n["nulo_etiquetas_media"], 1),
                      c(n["nulo_etiquetas_p"]), c(n["nulo_bloques30_media"], 1),
                      c(n["nulo_bloques30_p"])])
    return (["Gen", "Regiones de 200 nt", "Rango de eficientes", "Mediana", "Máximo observado",
             "Nulo de etiquetas (media)", "p", "Nulo de bloques de 30 (media)", "p"], filas)


def tabla_evidencia():
    cab = ["Gen", "Qué se midió en *D. maidis*", "Cómo se entregó", "Fuente", "Marcador"]
    filas = [
        ["`eth_Dm`", "Knockdown del transcrito ~90 %; supervivencia 10 % al día 4 frente a >95 % del control "
         "(β-lactamasa); defectos de muda. ARNdc de **544 pb**; n = 40 por tratamiento para supervivencia y "
         "3 réplicas biológicas de 3 ninfas para el knockdown",
         "Microinyección en ninfas de quinto estadio recién mudadas, 125 ng por insecto",
         "Andrada *et al.* 2026, *Front Insect Sci* 6:1811933 (vía W1/P3, ola 2)", "`[R]`"],
        ["`bursA_Dm`", "Knockdown ~95 %; supervivencia 10 % al día 4 frente a >95 % del control. "
         "ARNdc de **578 pb**; mismo n",
         "Ídem", "Ídem", "`[R]`"],
        ["`BicC_Dm`", "Oviposición casi nula; transcrito baja >170 veces al día 7. Fenotipo de "
         "**esterilidad**, no de letalidad", "Microinyección e ingesta (dosis: ver fuente)",
         "Dalaisón-Fuentes *et al.* 2022, *Pest Manag Sci* (PMID 35442515), fila `DM-01` de C5", "`[R]`"],
        ["`ATPaseD_Dm`", "Supervivencia 18 % al día 4; efecto en alas no significativo. El catálogo no "
         "registra el control de esta fila", "Ingesta",
         "Jones, Bernal y Medina 2021 (leído en la ola 2), fila `DM-03` de C5", "`[R]`"],
        ["`MP_MRFV`, `CP_MRFV`", "Ninguna medición propia del ARNi sobre estos genes; el mecanismo antiviral "
         "es en planta, no en el insecto", "—", "Checkpoint 1 (investigador) y W1", "`[?]`"],
    ]
    return cab, filas


def tabla_cambios():
    pm, om = modal(21, "los_seis_recomendados")
    eh = D["efecto_humano"]
    bic_ant = eh["regiones_recomendadas_w7"]["BicC_Dm"]["recomendada"]
    bic_nue = eh["fichas"]["con_humano_recomendada"]["BicC_Dm"]
    b0 = eh["barrido"]["sin_humano"]["como_estan"]
    b1 = eh["barrido"]["con_humano"]["como_estan"]
    return (["Conclusión de W7", "En la v2", "¿Cambió?"], [
        ["`MP_MRFV` primero y `CP_MRFV` segundo entre los cuatro",
         "`MP_MRFV` primero %s, `CP_MRFV` segundo %s (antes %s y %s)" % (
             pc0(b1["MP_MRFV"][0]), pc0(b1["CP_MRFV"][1]), pc0(b0["MP_MRFV"][0]),
             pc0(b0["CP_MRFV"][1])), "No"],
        ["`BicC_Dm` y `ATPaseD_Dm` no se ordenan entre sí",
         "Tercero `BicC_Dm` %s / `ATPaseD_Dm` %s (antes %s / %s)" % (
             pc0(b1["BicC_Dm"][2]), pc0(b1["ATPaseD_Dm"][2]), pc0(b0["BicC_Dm"][2]),
             pc0(b0["ATPaseD_Dm"][2])), "No (sigue siendo la elección de pesos)"],
        ["Mover la región en `BicC_Dm` a %s" % bic_ant,
         "A %s (%s ventanas eficientes), por la columna de humano" % (
             bic_nue, ficha(21, "BicC_Dm", True)["conservadora"]["eficientes"]),
         "Dos nucleótidos"],
        ["Mover la región en `ATPaseD_Dm` a 72-371",
         "72-371, igual", "No"],
        ["Con las regiones movidas: `MP_MRFV` > `BicC_Dm` > `CP_MRFV` > `ATPaseD_Dm`",
         "Mismo orden entre los cuatro: `BicC_Dm` segundo %s" % pc0(
             eh["barrido"]["con_humano"]["recomendadas"]["BicC_Dm"][1]), "No"],
        ["Los dos genes del insecto, vetados por *H. vitripennis*",
         "Siguen vetados y últimos a 21 y a 22 nt", "No"],
        ["Seis referencias, cuatro candidatos, 21 nt",
         "Seis referencias más humano, seis candidatos, 21 y 22 nt", "**Sí: es lo que agrega la v2**"],
    ])


# -------------------------------------------------------------------- el documento

def construir():
    f21_eth, f21_bur = ficha(21, "eth_Dm"), ficha(21, "bursA_Dm")
    r_eth, r_bur = f21_eth["conservadora"], f21_bur["conservadora"]
    G21 = K[21]["gen_entero"]
    p_l3, o_l3 = modal(21, "los_seis_recomendados")
    p_l3b, o_l3b = modal(22, "los_seis_recomendados")
    p_l1, o_l1 = modal(21, "los_seis")
    p_l1b, o_l1b = modal(22, "los_seis")
    p_in, o_in = modal(21, "insecto_recomendados")
    p_inb, o_inb = modal(22, "insecto_recomendados")
    p_vi, o_vi = modal(21, "virus")
    p_vib, o_vib = modal(22, "virus")
    nulo = K[21]["nulo_nuevos"]
    eth_dens = K[21]["nulo_nuevos"]["eth_Dm"]
    b = []

    def H(n, t):
        b.append(("h%d" % n, t))

    def P(t):
        b.append(("p", t))

    def T(cab, filas, nota=None):
        b.append(("tabla", cab, filas, nota))

    def BOX(t, ok=False):
        b.append(("box", t, ok))

    H(1, "El ranking v2: los cuatro candidatos de EPILAB y dos genes nuevos, a 21 y a 22 nt")
    P("Fecha: 2026-10-21. Complementa [`research/ola2/W7_ranking/REPORT.md`](../../ola2/W7_ranking/REPORT.md), "
      "que sigue siendo el ranking de partida, y toma lo que midieron "
      "[C5](../C5_estructura_genes_ingenieria_inversa/REPORT.md) (los genes nuevos) y "
      "[C6](../C6_panel_y_largo/REPORT.md) (el largo de ventana). Reproducible con "
      "`tools/sifi21_port/ranking_v2.py`; todos los números salen de `resultados/ranking_v2.json`. "
      "Marcadores de `CLAUDE.md`.")

    H(2, "El resultado, en un párrafo")
    P("**La v2 reproduce a W7 y no le desarma ninguna conclusión; agrega dos candidatos que entran sin "
      "vetos en el medio de la tabla, y muestra qué parte del orden aguanta un cambio de 21 a 22 nt.** "
      "Antes de medir nada nuevo el motor reprodujo exacto los cuatro conteos de eficientes, las cuatro "
      "fichas y el barrido de 2.000 sorteos de W7. Con el panel de W7 más humano —y sin *Macrosteles "
      "quadrilineatus*, decisión D23—, `MP_MRFV` sigue primero y `CP_MRFV` segundo entre los virales; "
      "`BicC_Dm` y `ATPaseD_Dm`, tal como los eligió EPILAB, siguen vetados y sin orden entre sí; y la "
      "recomendación de mover la región dentro de los dos genes del insecto sigue en pie "
      "(`BicC_Dm` pasa de 2123-2422 a %s por dos nucleótidos que cambia humano, `ATPaseD_Dm` sigue en 72-371). "
      "Los dos genes nuevos, `eth` y `burs-alpha`, no desplazan a nadie: cuando los seis se comparan cada uno en "
      "su mejor región, el orden es %s (%s de los sorteos) y a 22 nt es %s (%s). Lo que los distingue no "
      "está en los dos ejes del ranking sino en lo que el ranking no mide: tienen el fenotipo letal publicado "
      "en la propia especie (10 %% de supervivencia al día 4 contra más del 95 %% del control, por "
      "microinyección), y `burs-alpha` es el único candidato sin una sola coincidencia perfecta de 19 nt o "
      "más contra ninguna referencia en el gen entero. **A 22 nt las puntas del orden aguantan y el medio no** (con la escala absoluta, la que W7 recomienda "
      "leer en este nivel): `MP_MRFV` primero, `BicC_Dm` segundo y `ATPaseD_Dm` último a los dos largos, pero `CP_MRFV`, `eth` y "
      "`burs-alpha` se reordenan, y las regiones propuestas de `MP_MRFV`, `CP_MRFV`, `eth` y `burs-alpha` se "
      "mudan, mientras que las de `BicC_Dm` y `ATPaseD_Dm` se mueven uno o dos nucleótidos." % (
          K[21]["regiones_recomendadas"]["BicC_Dm"], flecha(o_l3), pc(p_l3), flecha(o_l3b), pc(p_l3b)))

    BOX("**Lo que se deduce, en cinco líneas.** (1) El ranking de W7 aguanta: se reprodujo exacto y agregar humano no "
        "mueve ninguna conclusión. (2) Tal como los eligió EPILAB, `BicC_Dm` y `ATPaseD_Dm` quedan vetados y últimos; "
        "moviendo la región, `BicC_Dm` sube a segundo y `ATPaseD_Dm` sigue último en el orden por tasas. (3) Los genes nuevos no ganan por "
        "diseño; su valor está en la evidencia publicada y, en `burs-alpha`, en una especificidad limpia. (4) El largo "
        "de ventana mueve el medio de la tabla y las regiones de cuatro candidatos, pero no las de `BicC_Dm` ni "
        "`ATPaseD_Dm`. (5) Quedan abiertas cosas que no podemos cerrar nosotros: una ventana de `eth`, las posiciones "
        "del amplicón publicado, la conservación entre poblaciones y el largo de siRNA en hemípteros.")

    BOX("**Qué es medición y qué es decisión nuestra.** Son medición: los conteos de ventanas eficientes, "
        "las coincidencias por referencia, los nulos y las frecuencias del barrido. Son decisión nuestra y "
        "están declaradas: que *Macrosteles* no entre al panel (D23); el peso 1,00 de humano; elegir la región de "
        "los dos genes nuevos por la misma cascada con la que W7 recomienda regiones; y leer el ranking de "
        "diseño y la evidencia publicada como dos ejes separados, sin sumarlos (D24). Las cinco decisiones de "
        "agregación de W7 (D16 a D20) no se tocan.")

    H(2, "1. Qué cambió respecto de W7")
    P("`[E]` Antes de contar nada se verificó el entorno contra W7. El motor reproduce los cuatro conteos de "
      "eficientes (123, 30, 171 y 29), las cuatro fichas campo por campo —ventanas, eficientes, eficacia, "
      "limpieza, exposición, limpias y eficientes, ventanas con off-target, ventanas con 21/21, veto— y las "
      "frecuencias del barrido de 2.000 sorteos con la misma semilla. Si alguno hubiera fallado, el script "
      "aborta; no abortó. Esa verificación se hizo **sin** la columna de humano, para que fuera la de W7. "
      "El primer intento de ancla falló y vale registrarlo: no se había incluido el genoma de *D. maidis*, que "
      "para los genes virales cuenta como off-target (D20), y el desfase de una ventana lo delató.")
    T(*tabla_cambios())
    P("`[E]` **Humano no cambia ninguna conclusión.** Da cero coincidencias perfectas de 21 nt en los seis genes, "
      "como ya había medido C6. Baja la limpieza de las regiones de EPILAB en menos de un centésimo "
      "(`MP_MRFV` de 0,9802 a 0,9757; `BicC_Dm` de 0,9334 a 0,9304; `ATPaseD_Dm` de 0,9804 a 0,9724) porque "
      "agrega algunos aciertos de un desajuste y de 19 nt, que son del orden de lo que el azar da contra un "
      "transcriptoma de 718,6 Mb: para un 19-mero cualquiera la probabilidad de aparecer en alguna de las "
      "dos hebras es de unos 2·718,6·10⁶/4¹⁹ ≈ 0,5 %, o sea entre 2 y 13 aciertos esperados por gen contra "
      "los 0 a 12 observados (cuenta gruesa, sin corregir composición). La excepción posible es `ATPaseD_Dm` "
      "(7 observados contra 2,4 esperados), compatible con que la subunidad D de la V-ATPasa esté conservada. `[H]`")

    H(2, "2. El panel, y lo que queda afuera")
    P("Seis referencias no objetivo más el genoma del vector. Cinco son transcriptomas de RefSeq que W7 ya "
      "usaba —maíz, *Harmonia axyridis*, *Apis mellifera*, *Homalodisca vitripennis* y *Folsomia candida*— y "
      "se volvieron a bajar para esta corrida (116 MB, accesiones en la sección 9); la sexta es humano "
      "(GRCh38.p14), con peso base 1,00 porque, nuestra lectura `[H]`, un acierto ahí frenaría un registro antes que cualquier otro. "
      "El genoma de *D. maidis* (GCA_975739785.1) es on-target para los genes del insecto y se excluye del "
      "cómputo; para los virales cuenta como off-target, igual que en W7. El barrido mueve los pesos sobre todo el "
      "símplex, de modo que el orden que sobrevive no depende de ese peso base.")
    P("**Lo que no entra.** *Macrosteles quadrilineatus* queda fuera de esta versión por decisión del "
      "equipo (D23), con el argumento de que la especie no está en Argentina, que todavía no verificamos contra un "
      "catálogo de distribución `[?]`. La medición existe y no se borra: C6 midió exposición alta en `BicC_Dm` y "
      "C5 midió 21 ventanas con coincidencia perfecta en el gen entero de `eth`. Esta versión simplemente no la usa, y por eso "
      "toda recomendación de región de este informe dice contra qué panel se evaluó. Tampoco entran los "
      "parasitoides de huevos ni los cicadélidos nativos, que no tienen transcriptoma anotado: un peso sobre "
      "una referencia que no existe es cero por omisión, no por evidencia. `[?]`")

    H(2, "3. Los dos candidatos nuevos")
    P("`eth` (*ecdysis triggering hormone*) y `burs-alpha` (*bursicon* α) son los dos genes del trabajo de "
      "Andrada *et al.* 2026 sobre la muda de *D. maidis* que no estaban en la planilla de EPILAB. C5 los "
      "puso primeros en su lista corta porque son los únicos candidatos nuevos con ARNm público de la propia "
      "especie (GenBank PZ371507.1 y PZ371508.1; 615 y 468 nt), de modo que la ventana se calcula sobre la "
      "secuencia que se sintetizaría y no sobre el ortólogo de otro cicadélido. Los otros candidatos de C5 "
      "**no entran**: se diseñaron sobre ortólogos de *Macrosteles*, *Scaphoideus* o *Euscelidius* y la "
      "propia medición de C5 muestra que entre el 0,7 % y el 11,1 % de sus 21-meros existen en el genoma del vector, "
      "así que no son material para diseñar sobre *D. maidis* hasta recuperar su secuencia.")
    P("**Dos aclaraciones que cambian cómo leer los números.** Primero, los conteos de C5 (44 y 33 eficientes) "
      "son del modo fiel de si-Fi21; los de acá son del modo corregido (%d y %d), y la diferencia es "
      "exactamente la rama de la regla terminal que W5 midió entre el 14 y el 24 %% de lo que el original llama "
      "eficiente: no son comparables y no se mezclan. Segundo, **la molécula que tiene evidencia es del orden "
      "del transcrito entero**: los ARNdc publicados miden 544 y 578 pb frente a los 615 y 468 nt de la secuencia "
      "codificante pública que tenemos (en `burs-alpha` el amplicón es más largo que ella, así que incluye "
      "regiones no codificantes), y nosotros proponemos 200 nt. Esa región es una extrapolación `[H]`: el piso de longitud está sostenido (unos 60 pb, "
      "C4) pero que 200 nt de `eth` o de `burs-alpha` silencien como la molécula completa no está probado." % (
          G21["eth_Dm"]["eficientes"], G21["bursA_Dm"]["eficientes"]))
    T(*tabla_gen_entero(21), nota="Cada celda es 21/21 perfectos / ventanas con un bloque perfecto de ≥19 nt / "
      "ventanas con un desajuste, sobre la secuencia pública completa y a 21 nt; · = ninguna. Es el riesgo "
      "de la molécula que se acerca a la que se probó, no el de la región de 200 nt.")
    P("`[E]` **`burs-alpha` es el candidato más limpio de los seis sobre la secuencia completa:** cero coincidencias "
      "perfectas de 21 nt y cero bloques de 19 nt o más contra las seis referencias; solo cinco ventanas con un "
      "desajuste. Su región propuesta (%s, %d eficientes) tiene cero ventanas con riesgo bajo cualquiera de los tres "
      "criterios. **`eth` tiene una sola ventana con coincidencia perfecta de 21 nt** contra *H. vitripennis*, en la "
      "posición 347 y no eficiente, y cinco ventanas con un bloque de 19 nt o más (una de ellas es la misma de 21/21); la región propuesta (%s, %d eficientes) la evita, pero "
      "evitarla cuesta: la región más densa de `eth` (194-393) tiene 22 eficientes y contiene esa ventana. "
      "Si una sola ventana debe vetar la molécula completa es una decisión de umbral que no podemos tomar "
      "con estos datos y va a la lista de preguntas para el investigador. `[?]`" % (
          K[21]["regiones"]["bursA_Dm"], r_bur["eficientes"], K[21]["regiones"]["eth_Dm"],
          r_eth["eficientes"]))
    P("`[E]` Sobre si elegir región discrimina en estos genes cortos, el resultado repite el de W7: con el nulo "
      "de etiquetas `eth` sí (p = %s) y `burs-alpha` no (p = %s); con el de bloques de 30, ninguno (p = %s y %s). "
      "En un gen de 468 nt, una región de 200 nt cubre casi la mitad, y no hay mucho que elegir." % (
          c(nulo["eth_Dm"]["nulo_etiquetas_p"], 3), c(nulo["bursA_Dm"]["nulo_etiquetas_p"], 3),
          c(nulo["eth_Dm"]["nulo_bloques30_p"], 3), c(nulo["bursA_Dm"]["nulo_bloques30_p"], 3)))
    T(*tabla_nulo())

    H(2, "4. El ranking")
    P("Dos lecturas, y la segunda es la que hay que usar para comparar. **Nivel 1:** los cuatro de EPILAB con la "
      "región que eligió el laboratorio y los dos nuevos con la que proponemos nosotros. Mezcla regiones elegidas "
      "por procedimientos distintos —las de EPILAB sin ver los off-targets, las nuestras con la cascada—, así que "
      "favorece a los nuevos. **Nivel 3:** los seis, cada uno en la mejor región que la cascada encuentra para su "
      "gen. Es la comparación pareja y es la que reportamos como resultado.")
    P("Nivel 1, 21 nt (escala absoluta, media geométrica, regla conservadora; 2.000 sorteos):")
    T(*tabla_fichas(21))
    T(*tabla_frecuencias(21, "los_seis"))
    P("Orden más frecuente %s en el %s. Con otras combinaciones:" % (flecha(o_l1), pc(p_l1)))
    T(*tabla_ordenes(21, "los_seis"))
    P("Nivel 3, 21 nt, todos en su mejor región:")
    T(*tabla_fichas(21, rec=True))
    T(*tabla_frecuencias(21, "los_seis_recomendados"))
    P("Orden más frecuente %s en el %s. Con otras combinaciones:" % (flecha(o_l3), pc(p_l3)))
    T(*tabla_ordenes(21, "los_seis_recomendados"))
    P("`[E]` **Lo que dice el nivel 3.** `MP_MRFV` primero (99 %% de los sorteos con la escala absoluta), "
      "`BicC_Dm` segundo (97 %%) y `ATPaseD_Dm` último (100 %%). Entre medio, `CP_MRFV`, `eth` y `burs-alpha` quedan "
      "separados por dos ventanas limpias y eficientes de 200 entre cada par (%d, %d y %d) y por centésimas de "
      "limpieza. La cascada, que cuenta limpias y eficientes, los ordena `CP_MRFV`, `eth`, `ATPaseD_Dm`, "
      "`burs-alpha`, y le pone `ATPaseD_Dm` por delante de `burs-alpha` por una sola ventana (17 contra 16). "
      "La cascada cuenta ventanas y no tasas, así que favorece a las regiones de 300 nt sobre las de 200: es "
      "la razón de que ponga a `ATPaseD_Dm` por delante de `burs-alpha`. "
      "**Una diferencia de una o dos ventanas sobre 200 está por debajo de la resolución del umbral de si-Fi21**, que ni siquiera reproduce "
      "los conteos que declara el laboratorio. Por eso el medio no se lee como orden." % (
          ficha(21, "CP_MRFV", True)["conservadora"]["buenos_limpios"],
          ficha(21, "eth_Dm", True)["conservadora"]["buenos_limpios"],
          ficha(21, "bursA_Dm", True)["conservadora"]["buenos_limpios"]))
    P("`[E]` **Corrección de lectura (2026-10-21), equivalente a la de W7 §2.1 bis.** ~~Los porcentajes de arriba "
      "(99 %, 97 %, 100 %) se leían como robustez del orden.~~ Con la escala absoluta la limpieza casi no tiene "
      "palanca (factor 1,015–1,064 entre candidatos contra 2,38–2,50 de la eficacia; piso duro de 0,8533 en el "
      "peor caso), de modo que el sorteo de pesos sólo puede dar vuelta un par ya casi empatado en eficacia, y esos "
      "porcentajes **miden la escala**, no que un candidato domine a otro: hay 3 pares en conflicto de 6 y sus "
      "cruces caen en w* ≈ 0,02, al borde del rango. Bajo la escala min-max las frecuencias de las tablas de esta "
      "sección se aflojan. Fuente: auditoría propia registrada en `00_meta/PREGUNTAS_ABIERTAS.md`; no se volvió "
      "a medir aquí. Detalle en [`research/ola2/W7_ranking/REPORT.md`](../../ola2/W7_ranking/REPORT.md) §2.1 bis.")
    P("`[H]` **Los genes nuevos no mejoran el ranking de diseño y eso es un resultado.** C5 ya lo había anticipado "
      "(\"ningún gen nuevo se destaca por densidad de eficientes\") y acá se confirma con el procedimiento "
      "completo: su eficacia (%s y %s) cae en el rango de las regiones de EPILAB, elegidas o movidas (%s a %s), y son genes cortos con "
      "poco margen de región. Lo que aportan es otra cosa: un fenotipo publicado en la especie objetivo y, en el "
      "caso de `burs-alpha`, el perfil de especificidad más limpio. Ninguna de las dos cosas la mide el ranking." % (
          c(r_eth["eficacia"]), c(r_bur["eficacia"]),
          c(min(ficha(21, g)["conservadora"]["eficacia"] for g in ("MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"))),
          c(max(ficha(21, g, True)["conservadora"]["eficacia"] for g in ("MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm")))))
    H(3, "Por estrategia, como en W7 (D20)")
    P("Los off-targets no significan lo mismo para un gen viral que para uno del insecto, y W7 presenta un "
      "ranking por estrategia. Virus, con las regiones de EPILAB: %s (%s a 21 nt y %s a 22). Insecto, con las regiones movidas: %s "
      "(%s a 21 nt y %s a 22). Con las regiones de EPILAB tal como están, el orden de los insectos es `eth` > `burs-alpha` > "
      "`BicC_Dm` / `ATPaseD_Dm`, pero ahí compiten regiones vetadas contra regiones ya elegidas por la cascada, "
      "y el resultado se explica por el veto, no por el gen." % (
          flecha(o_vi), pc(p_vi), pc(p_vib), flecha(o_in), pc(p_in), pc(p_inb)))
    P("`[E]` En la estrategia insecto, que es la que el investigador prefirió, `BicC_Dm` pasa a primero **solo si se "
      "acepta mover su región**: tal como la eligió EPILAB (264-563) está vetada por 22 ventanas con 21/21 contra "
      "*H. vitripennis*. Ese es el mismo mecanismo de W7 y no cambió.")

    H(2, "5. Veintiuno contra veintidós")
    P("Mismo motor, mismo modo corregido, misma versión de ViennaRNA; lo único que cambia es el tamaño de ventana, "
      "con la regla terminal conservada en su posición relativa (la decisión de C6). Para hemípteros no hay perfil "
      "de longitud de siRNA publicado, así que **no hay forma de saber hoy cuál de los dos largos es el correcto** y "
      "reportamos los dos.")
    T(*tabla_k(ORDEN6))
    P("`[E]` **Las puntas aguantan y el medio no**, bajo la escala absoluta. A 22 nt `MP_MRFV` sigue primero (%s), `BicC_Dm` segundo (%s) y "
      "`ATPaseD_Dm` último. `CP_MRFV`, `eth` y `burs-alpha` se permutan: a 22 nt `eth` pasa de cuarto a tercero y "
      "`CP_MRFV` de tercero a cuarto. Las regiones de `BicC_Dm` y `ATPaseD_Dm` se mueven uno o dos nucleótidos, de "
      "modo que **esas dos recomendaciones son robustas al largo**; las de `MP_MRFV`, `CP_MRFV`, `eth` y `burs-alpha` "
      "se mudan decenas de posiciones. El conjunto de ventanas eficientes cambia mucho aunque el conteo "
      "no: Jaccard de %s a %s, con `eth` en el extremo alto (%s) y `CP_MRFV` en el bajo (%s)." % (
          pc0(K[22]["barridos"]["los_seis_recomendados"][GEO]["frecuencia"]["MP_MRFV"][0]),
          pc0(K[22]["barridos"]["los_seis_recomendados"][GEO]["frecuencia"]["BicC_Dm"][1]),
          c(min(v["jaccard"] for v in D["jaccard_21_22"].values()), 2),
          c(max(v["jaccard"] for v in D["jaccard_21_22"].values()), 2),
          c(D["jaccard_21_22"]["eth_Dm"]["jaccard"], 2),
          c(D["jaccard_21_22"]["CP_MRFV"]["jaccard"], 2)))
    P("Nivel 3 a 22 nt:")
    T(*tabla_fichas(22, rec=True))
    T(*tabla_frecuencias(22, "los_seis_recomendados"))
    T(*tabla_ordenes(22, "los_seis_recomendados"))
    P("Bajo la escala min-max y bajo la cascada las puntas se aflojan: la cascada pone a `BicC_Dm` primero a 22 nt "
      "(39 limpias y eficientes contra 30 de `MP_MRFV`) por la misma razón de longitud de región. Es una sensibilidad "
      "a la regla de combinación que ya tenía W7 (D16) y no una propiedad nueva de los candidatos.")
    P("`[H]` Una regla de método sale de acá: **toda región concreta lleva el largo al que se la eligió**, y las que "
      "dependen del largo se reportan con las dos. Cuando dos regiones empatan en limpias y eficientes, la cascada "
      "se queda con la primera por posición, que es un desempate arbitrario: a 22 nt `MP_MRFV` tiene dos regiones "
      "con 30 limpias y eficientes (162-361 y 820-1019) y la cascada elige la primera sin que haya un motivo.")

    H(2, "6. El segundo eje: qué evidencia hay de que el gen sirve")
    P("El ranking mide calidad de diseño dentro de un gen que alguien ya eligió, no el valor del gen (W7 §5). "
      "Para no esconder eso, la evidencia publicada se presenta aparte y **sin puntaje**: sumarla al ranking exigiría "
      "una equivalencia entre un fenotipo de microinyección y uno de ingesta que no tenemos. C5 marcó estas filas "
      "como `[E]`; acá van como `[R]` porque cada gen descansa en un solo estudio, según la definición de `CLAUDE.md`.")
    T(*tabla_evidencia())
    P("Dos cosas que la tabla obliga a decir. Primero, la entrega es distinta: `eth` y `burs-alpha` se probaron por "
      "microinyección, que esquiva la barrera que el laboratorio declara como principal (las dsRNasas del intestino "
      "y las glándulas salivales, Dalaisón-Fuentes *et al.* 2023); la evidencia de silenciamiento por ingesta es la de "
      "`ATPaseD_Dm`. Segundo, el knockdown de los dos genes nuevos descansa en tres réplicas biológicas de tres "
      "ninfas cada una: demuestra que el gen es esencial, no mide una eficacia comparable. "
      "La regla de oro de la ficha del investigador aplica sin retoques: detectar ARN no es que haya entrado a la "
      "célula correcta, ni que se haya generado siRNA funcional, ni que haya efecto biológico.")

    H(2, "7. Lo que proponemos, y lo que no se puede decir")
    P("`[H]` Para el entregable, la lectura que mejor aguanta es de dos ejes. **Diseño:** `MP_MRFV` primero entre todos y "
      "`CP_MRFV` segundo entre los virales; entre los del insecto, `BicC_Dm` en la región %s (%s eficientes, "
      "limpia a 21 y a 22 nt) por delante de los dos nuevos, y `ATPaseD_Dm` último incluso mejorado. **Evidencia y "
      "especificidad:** `burs-alpha` es el candidato de menor riesgo de los seis y `eth` tiene, como `burs-alpha`, un "
      "fenotipo letal documentado por microinyección, con un único punto a decidir (la ventana de 21 nt contra "
      "*H. vitripennis*). Si el laboratorio quiere un candidato nuevo para probar en "
      "paralelo con `BicC_Dm`, la v2 sostiene `burs-alpha`, con la advertencia de que su región de 200 nt es una "
      "extrapolación de la molécula de 578 pb que sí se probó." % (
          K[21]["regiones_recomendadas"]["BicC_Dm"],
          ficha(21, "BicC_Dm", True)["conservadora"]["eficientes"]))
    P("**Lo que este informe no dice.** No dice que `eth` o `burs-alpha` sean mejores que `BicC_Dm`: por diseño no lo "
      "son y por evidencia no se pueden comparar. No dice cuál largo de siRNA es el correcto en hemípteros. No "
      "mide eficacia: \"eficiente\" sigue siendo \"pasa el umbral de si-Fi21\". Y no dice que las regiones propuestas "
      "estén conservadas en las poblaciones de *D. maidis* del noroeste argentino: ese cruce sigue sin hacerse y "
      "heredan el pendiente de W7.")

    H(2, "8. Límites, incluidos los que marcó la ficha del investigador")
    P("La ficha optativa del 19 al 26 de octubre (`Investigathon_EpiLab_Fichas_Optativas_v3_19oct.docx.md`, en la raíz "
      "del repositorio, sin versionar) es una guía y no una consigna; tomamos tres cosas de ella. "
      "**Una coincidencia off-target es una hipótesis de riesgo, no un daño demostrado**: por eso en este informe lo "
      "que W7 llama veto se lee como señal para revisar, aunque el cálculo no cambia. **Contar ventanas de 21 nt no "
      "dice qué hebra termina en AGO2**: si-Fi21 usa la diferencia de estabilidad de los extremos 5′ como filtro, "
      "pero la hebra que carga también depende de otros factores, y el ranking no la modela `[H]`. **Hay que poder "
      "justificar el largo de la región**: la nuestra es de 200 nt para los genes cortos y de 300 para los largos "
      "por herencia de EPILAB, y para los dos genes nuevos hay evidencia a 544 y 578 pb, no a 200.")
    P("Otros límites: el panel es de seis referencias y no incluye cicadélidos nativos ni parasitoides; el genoma "
      "de *D. maidis* usado (GCA_975739785.1) no tiene anotación, de modo que las coincidencias contra él "
      "se miden sobre secuencia genómica y no solo expresada; ViennaRNA 2.7.2 no es el RNAplfold 2.1.5 que usa el "
      "original (los conteos absolutos no son comparables con los de la planilla, las comparaciones internas sí); y "
      "las posiciones exactas del amplicón publicado de `eth` y `burs-alpha` sobre el transcrito no se "
      "leyeron en esta sesión, de modo que no se puede decir qué fracción de la molécula probada cubre nuestra región. `[?]`")

    H(2, "9. Cómo reproducirlo")
    P("Referencias (solo entró tráfico; las secuencias de EPILAB no salieron de la máquina). Las cinco de RefSeq "
      "salen de `https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/…/<accesión>_rna.fna.gz`: maíz "
      "`GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0` (37,8 MB), *H. axyridis* `GCF_914767665.1_icHarAxyr1.1` (14,0 MB), "
      "*A. mellifera* `GCF_003254395.2_Amel_HAv3.1` (19,5 MB), *H. vitripennis* `GCF_021130785.1_UT_GWSS_2.1` "
      "(19,0 MB) y *F. candida* `GCF_002217175.1_ASM221717v1` (25,6 MB); humano `GCF_000001405.40_GRCh38.p14` "
      "(135,5 MB, la copia de C6); y el genoma `GCA_975739785.1_ihDalMaid1.1_genomic.fna.gz` (281,7 MB).")
    b.append(("codigo", """# perfil de eficiencia de los seis genes a 21 y a 22 nt (modo corregido, ViennaRNA 2.7.2)
python research/ola3/C7_ranking_v2/scripts/perfil_k.py

# off-targets: panel de siete referencias, a 21 y a 22 nt (el genoma de D. maidis va aparte)
python tools/sifi21_port/offtarget_21nt.py --size 21 --mm1 --consulta work/sifi_v2/fasta/*_full.fasta \\
    --db <refs>/*.fna.gz --salida work/sifi_v2/offtarget_k21
python tools/sifi21_port/offtarget_21nt.py --size 21 --mm1 --consulta work/sifi_v2/fasta/*_full.fasta \\
    --db <refs_dm>/*.fna.gz --salida work/sifi_v2/offtarget_dm_k21
# lo mismo con --size 22 y los directorios *_k22

# el ranking v2, con las anclas de W7 adelante
python tools/sifi21_port/ranking_v2.py --trabajo work/sifi_v2 \\
    --json research/ola3/C7_ranking_v2/resultados/ranking_v2.json

# este informe y su página
python research/ola3/C7_ranking_v2/scripts/generar_informes.py"""))
    P("Necesita `ViennaRNA`, `biopython`, `pyahocorasick` y `numpy`, y las secuencias de EPILAB en "
      "`work/sifi_v2/fasta/` (fuera del control de versiones). Las de `eth` y `burs-alpha` salen de "
      "`research/ola3/C5_estructura_genes_ingenieria_inversa/resultados/candidatos_c5.fa`.")
    return b


# ------------------------------------------------------------------------- render

def inline_html(t: str) -> str:
    partes = re.split(r"(`[^`]*`)", t)
    out = []
    for p in partes:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append("<code>%s</code>" % html.escape(p[1:-1]))
            continue
        p = html.escape(p, quote=False)
        p = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', p)
        p = re.sub(r"~~(.+?)~~", r"<del>\1</del>", p)
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
--rojo:#c23b3b;--verde:#1f7a4d;--hot:#c23b3b1a}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#14171a;--fg:#e6e8eb;
--mut:#9aa4af;--line:#2b3138;--card:#1b1f24;--azul:#6aa3ff;--rojo:#ff8a8a;--verde:#5fd09a;--hot:#ff8a8a1f}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,sans-serif}
main{max-width:900px;margin:0 auto;padding:28px 16px 60px}
.k{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
h1{font-size:26px;margin:6px 0 4px;line-height:1.2}h2{font-size:19px;margin:34px 0 10px}
h3{font-size:16px;margin:22px 0 6px}
.lead{color:var(--mut);margin:0 0 18px}
.box{background:var(--card);border-left:3px solid var(--azul);padding:12px 16px;border-radius:6px;margin:16px 0}
.box.ok{border-left-color:var(--verde)}.box p{margin:6px 0}
table{width:100%;border-collapse:collapse;font-size:14px;margin:4px 0}
th,td{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{color:var(--mut);font-weight:600;font-size:13px}
.tw{overflow-x:auto;margin:8px 0}
.muted,.fine{font-size:13px;color:var(--mut)}code{font-size:.92em}
pre{background:var(--card);padding:12px;border-radius:6px;overflow-x:auto;font-size:13px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;margin:14px 0}
.kpi{border:1px solid var(--line);border-radius:8px;padding:10px 12px}
.kpi b{display:block;font-size:22px}.kpi span{font-size:13px;color:var(--mut)}
.bar{display:inline-block;width:64px;height:8px;background:var(--line);border-radius:4px;vertical-align:middle;
overflow:hidden;margin-right:6px}.bar i{display:block;height:100%;background:var(--azul)}
@media (max-width:600px){main{padding:20px 16px 50px}h1{font-size:22px}}"""


def celda_html(txt: str) -> str:
    m = re.fullmatch(r"(\d+) %", txt)
    if m:
        n = int(m.group(1))
        return '<span class="bar"><i style="width:%d%%"></i></span>%s' % (n, txt)
    return inline_html(txt)


def a_html(bloques) -> str:
    cuerpo = []
    primero = True
    for bl in bloques:
        t = bl[0]
        if t == "h1":
            continue
        if t == "h2":
            cuerpo.append("<h2>%s</h2>" % inline_html(bl[1]))
        elif t == "h3":
            cuerpo.append("<h3>%s</h3>" % inline_html(bl[1]))
        elif t == "p":
            if primero:          # el parrafo de fecha y enlaces ya esta en el encabezado
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
            tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % celda_html(x) for x in f)
                         for f in filas)
            cuerpo.append('<div class="tw"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                          % (th, tr))
            if nota:
                cuerpo.append('<p class="fine">%s</p>' % inline_html(nota))
    pm, om = modal(21, "los_seis_recomendados")
    kpis = """<div class="kpis">
<div class="kpi"><b>exacto</b><span>W7 reproducido: 4 conteos, 4 fichas, 2.000 sorteos</span></div>
<div class="kpi"><b>0 de 6</b><span>genes con coincidencia perfecta de 21 nt en humano</span></div>
<div class="kpi"><b>%s</b><span>orden más frecuente, todos en su mejor región, 21 nt (%s)</span></div>
<div class="kpi"><b>puntas sí, medio no</b><span>MP, BicC y ATPaseD aguantan a 22 nt; CP, eth y burs-α se permutan</span></div>
</div>""" % (inline_html(" > ".join(om[:2]) + " …"), pc(pm))
    cab = ('<!doctype html>\n<html lang="es"><head><meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
           "<title>Ranking v2: seis candidatos, 21 y 22 nt</title>\n<style>%s</style></head><body><main>\n"
           '<div class="k">Investigathon Y-Hat · track chicharrita / ARNi · ola 3 · C7</div>\n'
           "<h1>El ranking v2: los cuatro de EPILAB y dos genes nuevos, a 21 y a 22 nt</h1>\n"
           '<p class="lead">2026-10-21. Segunda versión del ranking de <a href="../../ola2/W7_ranking/index.html">W7</a>. '
           'Detalle y reproducción en <a href="REPORT.md">REPORT.md</a>.</p>\n' % CSS)
    return cab + kpis + "\n".join(cuerpo) + "\n</main></body></html>\n"


def main():
    bl = construir()
    (RAIZ / "REPORT.md").write_text(a_md(bl), encoding="utf-8")
    (RAIZ / "index.html").write_text(a_html(bl), encoding="utf-8")
    print("escrito REPORT.md e index.html en", RAIZ)


if __name__ == "__main__":
    main()
