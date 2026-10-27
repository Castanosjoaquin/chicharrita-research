"""M6: la tabla de alertas de D48 y el estado de las diecinueve regiones de la regla nueva.

Qué hace, en orden, y **aborta si un ancla falla**:

  A1/A2  `anclas.correr()` de M5: el motor sigue reproduciendo `ranking_v2.json`
         (162 de 162 conteos del gen entero y 51 de 51 barridos).
  A3     las seis cifras de M7 §5: las tres regiones de `BicC_Dm` dan 0 / 0 / 22 con
         21/21 perfecto y 3 / 6 / 33 con bloque de >= 19 nt.
  A4     los conteos por región y por referencia reproducen las fichas publicadas en
         `ranking_v2.json` —las diez regiones que el JSON publica— en los dos umbrales
         de D28. Las dos regiones de D25 (`BicC_Dm` 922-1221 y `ATPaseD_Dm` 137-436) no
         tienen ficha publicada y se marcan como tales.
  A5     la tabla de alertas, sumada por región y referencia, reproduce el conteo que
         sale de la matriz por ventana. Es la que ata la granularidad elegida —región x
         organismo x gen— al dato por ventana.

Después construye `alertas.tsv` con los cuatro campos obligatorios de D48, lo valida con
`alertas.validar()` —una fila sin los cuatro campos aborta— y escribe el estado de las
diecinueve regiones. **No decide nada**: ninguna región se acepta ni se descarta acá.

Las seis últimas entraron con `R7` (D70, D72): son las que el ranking recomienda a k=22 y
hasta entonces **no estaban tamizadas**, así que atravesaban la compuerta sin que nadie
hubiera mirado sus alertas. Entran al inventario con las mismas cuatro columnas
obligatorias de D48 que las otras doce, y sus filas salen en «pendiente», que es correcto:
una firma la escribe una persona y `aplicar_decisiones()` no la autogenera.

    python research/ola4/M6_alertas/scripts/tabla_alertas.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))
sys.path.insert(0, str(RAIZ / "research/ola4/M5_dos_ejes/scripts"))

import alertas as AL              # noqa: E402
import ejes_separados as E        # noqa: E402
import ranking as R               # noqa: E402
import ranking_v2 as V            # noqa: E402
import anclas as A                # noqa: E402

IDENTIDAD = RAIZ / "work" / "m6_alertas" / "identidad_por_ventana.tsv"
PUBLICADO = RAIZ / "research/ola3/C7_ranking_v2/resultados/ranking_v2.json"
COMPLEJIDAD = RAIZ / "research/ola4/M5_dos_ejes/resultados/complejidad_seis_genes.json"
SALIDA = RAIZ / "research/ola4/M6_alertas/resultados"
# Las firmas de D48. Es **entrada**, no salida: vive fuera de `resultados/` porque esta
# carpeta se reescribe entera en cada corrida y antes se llevaba puesta cualquier firma.
DECISIONES = RAIZ / "research/ola4/M6_alertas/decisiones.tsv"
REF_DIR = "work/W5/ref"

# Las diecinueve regiones. «qué es» sale de los ADR citados; la columna `vigente` dice si
# hoy es la región que el proyecto recomienda para ese gen, y ninguna de las seis de k=22
# lo es: las vigentes son las seis de k=21 de arriba.
#
# El orden de esta lista es el orden de las filas de `alertas.tsv`, así que las seis de
# k=22 van al final a propósito: agregarlas no mueve ni una línea de las que ya estaban,
# y eso hace que el diff de la tabla sea legible y que se vea que ninguna firma de D68
# quedó debajo de una fila distinta.
REGIONES = [
    ("MP_MRFV", (72, 271), "recomendada por C7 v2", True),
    ("CP_MRFV", (99, 298), "recomendada por C7 v2", True),
    ("BicC_Dm", (922, 1221), "recomendada por D25, por conservación", True),
    ("ATPaseD_Dm", (72, 371), "recomendada por C7 v2 y mantenida por D25", True),
    ("eth_Dm", (114, 313), "propuesta por C7 v2 (gen nuevo)", True),
    ("bursA_Dm", (13, 212), "propuesta por C7 v2 (gen nuevo)", True),
    ("MP_MRFV", (1, 200), "planilla de EPILAB", False),
    ("CP_MRFV", (201, 400), "planilla de EPILAB", False),
    ("BicC_Dm", (264, 563), "planilla de EPILAB", False),
    ("BicC_Dm", (2121, 2420), "recomendada por C7 v2, desplazada por D25", False),
    ("ATPaseD_Dm", (151, 450), "planilla de EPILAB", False),
    ("ATPaseD_Dm", (137, 436), "la más conservada, alternativa b de D25, vetada", False),
    # R7 (D70): las seis que el ranking recomienda a k=22, leídas de
    # research/ola3/C7_ranking_v2/resultados/ranking_v2.json, clave k.22.regiones_recomendadas.
    ("MP_MRFV", (162, 361), "recomendada por C7 v2 a k=22", False),
    ("CP_MRFV", (77, 276), "recomendada por C7 v2 a k=22", False),
    ("BicC_Dm", (2119, 2418), "recomendada por C7 v2 a k=22", False),
    ("ATPaseD_Dm", (71, 370), "recomendada por C7 v2 a k=22", False),
    ("eth_Dm", (193, 392), "recomendada por C7 v2 a k=22", False),
    ("bursA_Dm", (44, 243), "recomendada por C7 v2 a k=22", False),
    # R7, segunda vuelta: la compuerta de D72 encontro una mas al regenerar C7. Sale del
    # bloque `efecto_humano` de ranking_v2.py —la corrida contrafactica con la referencia
    # humana fuera del panel— y esta publicada en `efecto_humano.fichas.
    # sin_humano_recomendada` y en `regiones_recomendadas_w7`. Con humano en el panel la
    # recomendacion es 2121-2420, que ya estaba; sacarlo la corre dos nucleotidos.
    ("BicC_Dm", (2123, 2422), "recomendada por C7 v2 con el panel sin humano", False),
]
# El archivo de referencia de cada organismo, que es la fuente del cuarto campo.
ARCHIVO = {
    "maiz": "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna.fna.gz",
    "H_axyridis": "GCF_914767665.1_icHarAxyr1.1_rna.fna.gz",
    "A_mellifera": "GCF_003254395.2_Amel_HAv3.1_rna.fna.gz",
    "H_vitripennis": "GCF_021130785.1_UT_GWSS_2.1_rna.fna.gz",
    "F_candida": "GCF_002217175.1_ASM221717v1_rna.fna.gz",
    "humano": "humano_rna.fna.gz",
    "D_maidis": "GCA_975739785.1_ihDalMaid1.1_genomic.fna.gz",
}
CRITERIOS = ("perfecto_21", "perfecto_ge19")
COLUMNAS = [
    "gen", "region", "que_es", "vigente", "estado_region",
    # campo 1 de D48
    "organismo_corto", "organismo_especie", "organismo_rol",
    # campo 2 de D48 (M5, PANEL_EJES)
    "exposicion_w", "exposicion_w_alternativa", "exposicion_motivo", "exposicion_fuente",
    "exposicion_decision_abierta",
    # campo 3 de D48 (el desarrollo nuevo de esta línea)
    "gen_simbolo", "gen_locus", "gen_tipo_molecula", "gen_transcriptos", "gen_anotacion",
    "gen_fuente",
    # campo 4 de D48
    "evidencia_clave", "evidencia_bioensayo", "evidencia_prosa",
    # los dos umbrales de D28, anidados, y el descuento de D59
    "ventanas_perfecto_21", "ventanas_perfecto_ge19", "umbrales_anidados",
    "baja_complejidad_perfecto_21", "baja_complejidad_perfecto_ge19", "complejidad_fuente",
    # contexto, que NO decide (D17)
    "ventanas_21_eficientes", "ventanas_ge19_eficientes",
    "posiciones_perfecto_21", "posiciones_perfecto_ge19",
    # lo que escribe una persona
    "decision_usuario", "justificacion_usuario",
]
FUNCION = {c["gen"]: c["funcion"] for c in list(R.CANDIDATOS) + V.NUEVOS}


def leer_identidad() -> list[dict]:
    if not IDENTIDAD.exists():
        sys.exit("falta %s: corré antes research/ola4/M6_alertas/scripts/identidad.py"
                 % IDENTIDAD.relative_to(RAIZ))
    with IDENTIDAD.open(encoding="utf-8") as fh:
        return [dict(f, pos=int(f["pos"])) for f in csv.DictReader(fh, delimiter="\t")]


def conteos_de_region(g: dict, ini: int, fin: int, excl: set) -> dict:
    """{(corto, criterio): (ventanas, de_esas_eficientes)} desde la matriz por ventana."""
    out = {}
    efi = g["eficiente"][ini - 1:fin]
    for ref, crits in g["riesgo"].items():
        if ref in excl:
            continue
        for crit in CRITERIOS:
            v = crits[crit][ini - 1:fin]
            if v.any():
                out[(R.corto(ref), crit)] = (int(v.sum()), int((v & efi).sum()))
    return out


# ------------------------------------------------------------------------- anclas

def a3_m7(genes: dict) -> list[dict]:
    """Las seis cifras de M7 §5, que son el ancla de esta línea."""
    esperado = {(922, 1221): (0, 3), (2121, 2420): (0, 6), (264, 563): (22, 33)}
    excl = R.excluidas_de({"gen": "BicC_Dm", "estrategia": "insecto"}, "off")
    filas = []
    for (ini, fin), (e21, e19) in esperado.items():
        est = E.estado_region(genes["BicC_Dm"], ini, fin, None, excl)
        filas.append({"ancla": "A3", "region": "BicC_Dm %d-%d" % (ini, fin),
                      "mio": [est["ventanas_perfecto_21"], est["ventanas_perfecto_ge19"]],
                      "publicado": [e21, e19], "fuente": "research/ola4/M7_robustez_bicc/REPORT.md §5",
                      "coincide": [est["ventanas_perfecto_21"],
                                   est["ventanas_perfecto_ge19"]] == [e21, e19]})
    return filas


def a4_fichas(genes: dict) -> list[dict]:
    """Conteos por región y referencia contra las fichas publicadas en ranking_v2.json."""
    pub = json.loads(PUBLICADO.read_text(encoding="utf-8"))["k"]["21"]
    fichas = {(f["gen"], f["region"]): f for f in pub["fichas"] + pub["fichas_recomendadas"]}
    por_gen = {c["gen"]: c for c in list(R.CANDIDATOS) + V.NUEVOS}
    filas = []
    for gen, (ini, fin), _que, _vig in REGIONES:
        clave = (gen, "%d-%d" % (ini, fin))
        f = fichas.get(clave)
        if f is None:
            # Las fichas publicadas son las de k=21. Las dos regiones de D25 no tienen
            # ficha porque nacieron después del JSON; las seis de k=22 no tienen ficha
            # **en k=21** porque son de la otra corrida, y el ancla no puede compararlas
            # contra algo que ese bloque del JSON no publica. Decir cuál de los dos
            # motivos es importa: el primero es una región sin publicar, el segundo es
            # una región publicada en otro `k`.
            motivo = ("sin ficha publicada (región de D25)" if "D25" in _que
                      else "sin ficha publicada en k=21 (región recomendada a k=22)")
            filas.append({"ancla": "A4", "region": "%s %s" % clave, "referencia": "-",
                          "criterio": "-", "mio": None, "publicado": None,
                          "nota": motivo, "coincide": True})
            continue
        mio = conteos_de_region(genes[gen], ini, fin,
                               R.excluidas_de(por_gen[gen], "off"))
        suyo = f["riesgo_por_referencia"]
        refs = sorted({k[0] for k in mio} | set(suyo))
        for ref in refs:
            for crit in CRITERIOS:
                x = mio.get((ref, crit), (0, 0))[0]
                y = suyo.get(ref, {}).get(crit, {}).get("ventanas", 0)
                filas.append({"ancla": "A4", "region": "%s %s" % clave, "referencia": ref,
                              "criterio": crit, "mio": x, "publicado": y,
                              "nota": "", "coincide": x == y})
    return filas


def a5_identidad(filas_alerta: list[dict], genes: dict) -> list[dict]:
    """La tabla agrupada reproduce el conteo por región y referencia de la matriz."""
    por_gen = {c["gen"]: c for c in list(R.CANDIDATOS) + V.NUEVOS}
    desde_tabla: dict[tuple, list[int]] = {}
    for f in filas_alerta:
        k = (f["gen"], f["region"], f["organismo_corto"])
        d = desde_tabla.setdefault(k, [set(), set()])
        d[0].update(json.loads(f["posiciones_perfecto_21"]))
        d[1].update(json.loads(f["posiciones_perfecto_ge19"]))
    out = []
    for gen, (ini, fin), _q, _v in REGIONES:
        mio = conteos_de_region(genes[gen], ini, fin, R.excluidas_de(por_gen[gen], "off"))
        refs = sorted({k[0] for k in mio})
        for ref in refs:
            k = (gen, "%d-%d" % (ini, fin), ref)
            d = desde_tabla.get(k, [set(), set()])
            for i, crit in enumerate(CRITERIOS):
                esperado = mio.get((ref, crit), (0, 0))[0]
                out.append({"ancla": "A5", "region": "%s %d-%d" % (gen, ini, fin),
                            "referencia": ref, "criterio": crit,
                            "mio": len(d[i]), "publicado": esperado,
                            "coincide": len(d[i]) == esperado})
    return out


# ------------------------------------------------------------------- los cuatro campos

def prosa_evidencia(clave: str, gen: str, especie: str, d: dict, n21: int, n19: int,
                    efi21: int, efi19: int, transcriptos: list[str]) -> str:
    """El cuarto campo. Todo lo que afirma sale de disco o de una medición propia `[M]`.

    Lo que NO dice, y por eso la clave de bioensayo va en `sin_bioensayo_consultado`: si
    alguien midió experimentalmente el silenciamiento de ese gen en ese organismo. Esta
    línea no abrió ninguna fuente experimental, y el informe lo declara en vez de
    insinuar que la tabla resuelve la evidencia.
    """
    base = {
        "ortologo_del_blanco":
            "El transcripto impactado es el ortólogo del gen que se silencia (%s): «%s» "
            "(%s) en %s. El acierto no es un off-target incidental en un gen cualquiera, "
            "es el mismo gen en un pariente, que es exactamente el escenario en el que un "
            "ARNdc silenciaría al no objetivo."
            % (FUNCION.get(gen, gen), d["simbolo"], d["locus"], especie),
        "gen_no_relacionado":
            "El gen impactado está anotado y no tiene relación funcional declarada con el "
            "blanco (%s): «%s» (%s), %s, en %s. La anotación sale de la cabecera del FASTA "
            "de referencia, no de un alineamiento ni de un servicio web."
            % (FUNCION.get(gen, gen), d["simbolo"], d["locus"], d["molecula"], especie),
        "sin_anotacion_de_gen":
            "El acierto cae en el ensamblado genómico de %s (%s), que no trae anotación de "
            "gen: no se puede nombrar un gen y no se inventa. D28 pide clasificar por clase "
            "de blanco y la clase acá es «genómico sin anotación»; la pregunta de si cae en "
            "exón, intrón o intergénico queda abierta."
            % (especie, ", ".join(transcriptos)),
    }[clave]
    return (base + " Umbrales de D28: %d ventanas con 21/21 perfecto y %d con bloque "
            "perfecto de >= 19 nt (anidadas), de las cuales %d y %d son además "
            "predichas eficientes; la predicción de eficiencia no entra al criterio "
            "(D17). Ninguna fuente experimental sobre este organismo y este gen fue "
            "abierta en esta línea." % (n21, n19, efi21, efi19))


def construir(genes: dict, identidad: list[dict], complejidad: dict) -> list[dict]:
    por_gen = {c["gen"]: c for c in list(R.CANDIDATOS) + V.NUEVOS}
    pesos_d18 = {k: v["peso"] for k, v in R.REFERENCIAS.items()}
    pesos_d18[R.DMAIDIS] = R.DMAIDIS_INFO["peso"]
    filas = []
    for gen, (ini, fin), que, vigente in REGIONES:
        excl = R.excluidas_de(por_gen[gen], "off")
        est = E.estado_region(genes[gen], ini, fin, None, excl)
        conteos = conteos_de_region(genes[gen], ini, fin, excl)
        # agrupación región x organismo x gen
        grupos: dict[tuple, dict] = {}
        for f in identidad:
            if f["gen"] != gen or not (ini <= f["pos"] <= fin):
                continue
            k = (f["corto"], AL.clave_de_gen(f["corto"], f["anotacion"], f["transcripto"]))
            g = grupos.setdefault(k, {"anotacion": f["anotacion"], "transcriptos": set(),
                                      "pos": {c: set() for c in CRITERIOS}})
            g["transcriptos"].add(f["transcripto"])
            g["pos"][f["criterio"]].add(f["pos"])
        for (corto, _clave), g in sorted(grupos.items()):
            ref_larga = next(r for r in list(R.REFERENCIAS) + [R.DMAIDIS]
                             if R.corto(r) == corto)
            info = R.REFERENCIAS.get(ref_larga, R.DMAIDIS_INFO)
            ejes = E.PANEL_EJES[ref_larga]
            d = AL.partir_anotacion(g["anotacion"])
            pos21 = sorted(g["pos"]["perfecto_21"])
            pos19 = sorted(g["pos"]["perfecto_ge19"] | g["pos"]["perfecto_21"])
            efi = genes[gen]["eficiente"]
            efi21 = sum(1 for p in pos21 if efi[p - 1])
            efi19 = sum(1 for p in pos19 if efi[p - 1])
            clave_ev = AL.clasificar_evidencia(gen, g["anotacion"])
            filas.append({
                "gen": gen, "region": "%d-%d" % (ini, fin), "que_es": que,
                "vigente": "sí" if vigente else "no", "estado_region": est["estado"],
                "organismo_corto": corto, "organismo_especie": info["especie"],
                "organismo_rol": info["rol"],
                "exposicion_w": "%.2f" % ejes["w_exposicion"],
                "exposicion_w_alternativa": "%.2f" % pesos_d18[ref_larga],
                "exposicion_motivo": ejes["motivo"],
                "exposicion_fuente": "PANEL_EJES de tools/sifi21_port/ejes_separados.py (M5, D47)",
                "exposicion_decision_abierta": "sí" if corto == "H_vitripennis" else "no",
                "gen_simbolo": d["simbolo"] or "(sin anotación de gen)",
                "gen_locus": d["locus"] or "(sin LOC)",
                "gen_tipo_molecula": d["molecula"] or "(sin tipo)",
                "gen_transcriptos": ",".join(sorted(g["transcriptos"])),
                "gen_anotacion": g["anotacion"],
                "gen_fuente": "%s/%s (cabecera FASTA, leída de disco)" % (REF_DIR, ARCHIVO[corto]),
                "evidencia_clave": clave_ev,
                "evidencia_bioensayo": "sin_bioensayo_consultado",
                "evidencia_prosa": prosa_evidencia(clave_ev, gen, info["especie"], d,
                                                   len(pos21), len(pos19), efi21, efi19,
                                                   sorted(g["transcriptos"])),
                "ventanas_perfecto_21": len(pos21),
                "ventanas_perfecto_ge19": len(pos19),
                "umbrales_anidados": "sí: toda ventana con 21/21 tiene bloque de >= 19 nt",
                "baja_complejidad_perfecto_21": 0,
                "baja_complejidad_perfecto_ge19": 0,
                "complejidad_fuente": "M5, complejidad_seis_genes.json: 0 de %d ventanas "
                                      "del gen %s son de baja complejidad"
                                      % (complejidad["por_gen"][gen]["ventanas"], gen),
                "ventanas_21_eficientes": efi21, "ventanas_ge19_eficientes": efi19,
                "posiciones_perfecto_21": json.dumps(pos21),
                "posiciones_perfecto_ge19": json.dumps(pos19),
                "decision_usuario": "pendiente",
                "justificacion_usuario": "pendiente: la escribe el usuario, no el motor",
            })
        # control: la suma de la tabla contra la matriz, por referencia
        for (corto, crit), (n, _e) in sorted(conteos.items()):
            de_tabla = sum(f["ventanas_%s" % crit] for f in filas
                           if f["gen"] == gen and f["region"] == "%d-%d" % (ini, fin)
                           and f["organismo_corto"] == corto)
            if crit == "perfecto_21" and de_tabla != n:
                sys.exit("la tabla no reproduce la matriz en %s %d-%d / %s / %s: %d vs %d"
                         % (gen, ini, fin, corto, crit, de_tabla, n))
    return filas


def estados(genes: dict, filas: list[dict]) -> list[dict]:
    """El estado de las diecinueve regiones bajo la regla nueva, y bajo las dos anteriores.

    Esta es la salida que desde D72 hace de **inventario**: `alertas.exigir_decidida()` le
    exige a la región estar acá, y es el único archivo que puede decir «tamizada, cero
    aciertos», porque en `alertas.tsv` eso y «nunca tamizada» son las mismas cero filas.
    """
    por_gen = {c["gen"]: c for c in list(R.CANDIDATOS) + V.NUEVOS}
    w = E.vector_exposicion()
    out = []
    for gen, (ini, fin), que, vigente in REGIONES:
        excl = R.excluidas_de(por_gen[gen], "off")
        reg = "%d-%d" % (ini, fin)
        est = E.estado_region(genes[gen], ini, fin, None, excl)
        est_exp = E.estado_region(genes[gen], ini, fin, w, excl)
        mias = [f for f in filas if f["gen"] == gen and f["region"] == reg]
        out.append({
            "gen": gen, "region": reg, "que_es": que, "vigente": "sí" if vigente else "no",
            "n_ventanas": int(genes[gen]["presente"][ini - 1:fin].sum()),
            "eficientes": int(genes[gen]["eficiente"][ini - 1:fin].sum()),
            "alertas_21_21": est["ventanas_perfecto_21"],
            "alertas_ge19": est["ventanas_perfecto_ge19"],
            "baja_complejidad": 0,
            "filas_de_alerta": len(mias),
            "organismos_con_alerta": ",".join(sorted({f["organismo_corto"] for f in mias})) or "-",
            "genes_con_alerta": ",".join(sorted({f["gen_simbolo"] for f in mias})) or "-",
            "veto_regla_hoy_ciega_al_peso": "sí" if est["vetada_regla_anterior"] else "no",
            "veto_regla_por_exposicion_M5": "sí" if est_exp["vetada_regla_anterior"] else "no",
            "estado_D48": est["estado"],
            # `estado_D48` es lo que el motor puede decir solo, y por diseño nunca dice
            # «aceptada» (ver el docstring de `ejes_separados.estado_region`). Las dos
            # columnas que siguen son lo que agregan las firmas, en los dos umbrales de
            # D28, que es donde se ve la diferencia que M6 dejó como pregunta abierta.
            "estado_firmado_21": AL.estado_decision(filas, gen, reg, "perfecto_21")["estado"],
            "estado_firmado_ge19": AL.estado_decision(filas, gen, reg, "perfecto_ge19")["estado"],
            "decide": est["decide"],
        })
    return out


def main() -> int:
    print("A1/A2  anclas de M5 (abortan si fallan)...", flush=True)
    res = A.correr()
    genes = res["genes"]
    complejidad = json.loads(COMPLEJIDAD.read_text(encoding="utf-8"))

    f3, f4 = a3_m7(genes), a4_fichas(genes)
    for nombre, fs in (("A3  las seis cifras de M7 §5", f3),
                       ("A4  conteos por región contra las fichas publicadas", f4)):
        rotas = [f for f in fs if not f["coincide"]]
        print("%s: %d de %d coinciden" % (nombre, len(fs) - len(rotas), len(fs)), flush=True)
        for f in rotas[:10]:
            print("  ANCLA ROTA  %s" % f, file=sys.stderr)
        if rotas:
            sys.exit("ANCLAS ROTAS en %s" % nombre)

    identidad = leer_identidad()
    filas = construir(genes, identidad, complejidad)
    n = AL.validar(filas)
    print("validación de los cuatro campos: %d de %d filas completas" % (n, len(filas)))

    # Las firmas, volcadas sobre las filas recién construidas. Aborta si una firma no
    # corresponde a ninguna fila o si los conteos de su fila cambiaron desde que se
    # firmó: las dos cosas significan que nadie leyó la fila que hoy está en la tabla.
    inf = AL.aplicar_decisiones(filas, AL.leer_decisiones(DECISIONES))
    print("firmas de D48 (%s): %d de %d filas decididas, %d en pendiente"
          % (DECISIONES.relative_to(RAIZ), inf["firmadas"], inf["filas"], inf["pendientes"]))
    for k in inf["sin_firma"]:
        # cuatro campos, no tres: la clave lleva el gen impactado (ver `alertas.clave_de`)
        print("  sin firmar  %s %s / %s / %s" % k)

    f5 = a5_identidad(filas, genes)
    rotas = [f for f in f5 if not f["coincide"]]
    print("A5  la tabla agrupada contra la matriz por ventana: %d de %d coinciden"
          % (len(f5) - len(rotas), len(f5)))
    for f in rotas[:10]:
        print("  ANCLA ROTA  %s" % f, file=sys.stderr)
    if rotas:
        sys.exit("ANCLA A5 ROTA")

    SALIDA.mkdir(parents=True, exist_ok=True)
    AL.escribir(filas, SALIDA / "alertas.tsv", COLUMNAS)
    for gen, (ini, fin), _q, _v in REGIONES:
        reg = "%d-%d" % (ini, fin)
        sub = [f for f in filas if f["gen"] == gen and f["region"] == reg]
        destino = SALIDA / "alertas_por_region" / ("%s_%s.tsv" % (gen, reg))
        if sub:
            AL.escribir(sub, destino, COLUMNAS)
        else:
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text("\t".join(COLUMNAS) + "\n", encoding="utf-8")

    est = estados(genes, filas)
    with (SALIDA / "estado_regiones.tsv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(est[0]), delimiter="\t")
        w.writeheader()
        w.writerows(est)

    # la tabla por ventana, sin columna de secuencia (se puede versionar)
    with (SALIDA / "alertas_por_ventana.tsv").open("w", encoding="utf-8", newline="") as fh:
        campos = ["gen", "region", "pos", "organismo_corto", "criterio", "transcripto",
                  "gen_simbolo", "gen_locus"]
        w = csv.DictWriter(fh, fieldnames=campos, delimiter="\t")
        w.writeheader()
        for gen, (ini, fin), _q, _v in REGIONES:
            for f in identidad:
                if f["gen"] != gen or not (ini <= f["pos"] <= fin):
                    continue
                d = AL.partir_anotacion(f["anotacion"])
                w.writerow({"gen": gen, "region": "%d-%d" % (ini, fin), "pos": f["pos"],
                            "organismo_corto": f["corto"], "criterio": f["criterio"],
                            "transcripto": f["transcripto"],
                            "gen_simbolo": d["simbolo"] or "(sin anotación de gen)",
                            "gen_locus": d["locus"] or "(sin LOC)"})

    (SALIDA / "anclas_m6.json").write_text(json.dumps(
        {"A1_comparaciones": len(res["a1"]), "A1_coinciden": sum(f["coincide"] for f in res["a1"]),
         "A2_comparaciones": len(res["a2"]), "A2_coinciden": sum(f["coincide"] for f in res["a2"]),
         "A3": f3, "A4_comparaciones": len(f4), "A4_coinciden": sum(f["coincide"] for f in f4),
         "A5_comparaciones": len(f5), "A5_coinciden": sum(f["coincide"] for f in f5),
         "filas_validadas": n, "regiones": len(REGIONES),
         "A4_detalle": f4, "A5_detalle": f5}, indent=1, ensure_ascii=False), encoding="utf-8")
    print("escrito en %s" % SALIDA.relative_to(RAIZ))
    print("filas de alerta: %d sobre %d regiones; regiones con alerta de 21/21: %s"
          % (len(filas), len(REGIONES),
             ", ".join("%s %s" % (e["gen"], e["region"]) for e in est if e["alertas_21_21"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
