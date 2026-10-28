#!/usr/bin/env python3
"""Paso 3 y 4 de F3 — el orden por cohortes, la salida y el analisis de sensibilidad.

Criterio: `PREREGISTRO.md` y `D87` (pesos confirmados por el usuario el 2026-10-27).
Escalas: `resultados/escala_fenotipo.md` (eje 1) y `resultados/escala_esencialidad.md`
(eje 2), las dos commiteadas antes de este calculo.

Pesos de `D87`: fenotipo 0,40, esencialidad 0,25, off-target 0,25, conservacion 0,10 y
expresion en tejido expuesto 0,00 declarado faltante. Los ejes 3, 4 y 5 **no son calculables**
—el 3 por dos razones, ver `escala_fenotipo.md`— asi que el peso se renormaliza sobre los ejes
presentes de cada cohorte, que es la regla de `D87` §4.2.

Lo que este script NO hace: comparar candidatos de cohortes distintas, desempatar diferencias
menores a 0,05, y puntuar cualquier eje que no este calculado.

Uso:
    python research/ola6/F3_recomendador_genes/scripts/03_orden.py
"""

import csv
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
BLOQUE = Path(__file__).resolve().parents[1]
CATALOGO = RAIZ / "research/ola3/C5_estructura_genes_ingenieria_inversa/catalogo_genes_blanco.json"

PESOS_D87 = {"fenotipo": 0.40, "esencialidad": 0.25, "off_target": 0.25,
             "conservacion": 0.10, "expresion_tejido": 0.00}

EJES_NO_CALCULABLE_FILA = ("no calculado: sin secuencia de D. maidis admisible para el panel de seis "
                           "(PREREGISTRO_EJE3.md §1; entradas 97 y 99)")
EJES_NO_CALCULABLES = {
    "off_target": "calculado para 5 de 36 filas (DM-01, DM-02, DM-03, DM-05, DM-06; PREREGISTRO_EJE3.md). "
                  "Las otras 31 no tienen secuencia de D. maidis admisible (entradas 97 y 99); sus conteos "
                  "del catalogo son contra otro panel y no se ordenan por ellos",
    "expresion_tejido": 0.00}

EJES_NO_CALCULABLE_FILA = ("no calculado: sin secuencia de D. maidis admisible para el panel de seis "
                           "(PREREGISTRO_EJE3.md §1; entradas 97 y 99)")
EJES_NO_CALCULABLES = {
    "off_target": "no calculable: falta work/sifi_v2/ Y los conteos del catalogo son contra "
                  "otro panel (5 referencias, con M. quadrilineatus y sin H. axyridis ni "
                  "F. candida). Ver escala_fenotipo.md",
    "expresion_tejido": "FALTANTE para todos los candidatos: los transcriptomas publicos son "
                        "de cuerpo entero y huevos. El zip del investigador no lo trae "
                        "(verificacion_zip_expresion.md)",
}

# El panel con el que el catalogo de C5 calculo sus conteos. Se nombra en el encabezado de las
# columnas para que nadie lo confunda con el panel de seis.
PANEL_C5 = ["genoma_D_maidis", "M_quadrilineatus", "H_vitripennis", "Zea_mays", "Apis_mellifera"]

UMBRAL_EMPATE = 0.05


def puntaje_fenotipo(especie: str, marcador: str) -> tuple[str, float]:
    """Escala de `escala_fenotipo.md`, declarada antes de este calculo."""
    if especie == "Dalbulus maidis" and marcador == "E":
        return "F3", 1.00
    if marcador == "E":
        return "F2", 0.66
    return "F1", 0.33


def leer_tsv(ruta: Path) -> dict:
    with ruta.open(encoding="utf-8") as fh:
        return {r["id"]: r for r in csv.DictReader(fh, delimiter="\t")}


def primero_de(cohorte: list, w_fen: float, resto: dict) -> list:
    """Quien queda primero con un peso de fenotipo dado; el resto se reparte segun `resto`
    (claves de puntaje -> peso relativo, que suma 1)."""
    puntuados = [(r["id"], w_fen * r["_f"] + (1 - w_fen) * sum(w * r[k] for k, w in resto.items()))
                 for r in cohorte]
    tope = max(p for _, p in puntuados)
    return sorted(i for i, p in puntuados if abs(p - tope) < 1e-12)


def main() -> int:
    cat = {f["id"]: f for f in json.loads(CATALOGO.read_text(encoding="utf-8"))["filas"]}
    fen = leer_tsv(BLOQUE / "resultados/eje_fenotipo.tsv")
    ese = leer_tsv(BLOQUE / "resultados/eje_esencialidad.tsv")
    # Eje 4: regla de la enmienda 1 (PREREGISTRO_EJE4_ENMIENDA1.md). La regla original
    # queda en eje4_conservacion.tsv y NO entra al puntaje.
    c4 = leer_tsv(BLOQUE / "resultados/eje4_conservacion.tsv")
    # Eje 3 (PREREGISTRO_EJE3.md): fraccion limpia contra el panel de seis, solo cinco filas DM.
    c3 = leer_tsv(BLOQUE / "resultados/eje3_offtarget.tsv")
    n3 = leer_tsv(BLOQUE / "resultados/eje3_nulo.tsv")

    en_orden, fuera = [], []
    for ident, f in sorted(fen.items()):
        c = cat[ident]
        if not f["mecanismos"]:
            fuera.append({
                "id": ident, "gen": c["gen"], "especie": c["especie"],
                "etiqueta_de_ausencia": f["etiqueta_de_ausencia"],
                "por_que_no_entra": f["nota"] or f["etiqueta_de_ausencia"],
                "frases_de_apoyo": f["frases_de_apoyo"],
                "marcador_evidencia": f["marcador_evidencia"],
            })
            continue
        nivel_f, p_f = puntaje_fenotipo(c["especie"], f["marcador_evidencia"])
        e = ese[ident]
        p_e = float(e["puntaje"]) if e["puntaje"] else None
        en_orden.append({
            "id": ident, "gen": c["gen"], "especie": c["especie"],
            "familia_id": f["familia_id"],
            "_f": p_f, "_e": p_e,
            "_o": float(c3[ident]["fraccion_limpia"]) if ident in c3 else None,
            "eje3_puntaje": c3[ident]["fraccion_limpia"] if ident in c3 else "",
            "eje3_vs_nulo": ("" if ident not in n3 else
                             "dentro del rango del nulo" if float(n3[ident]["minimo"]) <= float(c3[ident]["fraccion_limpia"]) <= float(n3[ident]["maximo"])
                             else "fuera del rango del nulo"),
            "eje3_nulo_rango": (f"{n3[ident]['minimo']}-{n3[ident]['maximo']} (mediana {n3[ident]['fraccion_limpia_mediana']})"
                                if ident in n3 else ""),
            "_c": (float(c4[ident]["enm1_fraccion"])
                   if ident in c4 and c4[ident]["enm1_estado"] == "puntuado" else None),
            "eje4_puntaje": (c4[ident]["enm1_fraccion"]
                             if ident in c4 and c4[ident]["enm1_estado"] == "puntuado" else ""),
            "eje4_cobertura": c4[ident]["enm1_cobertura"] if ident in c4 else "",
            "eje4_tsa_con_el_gen": c4[ident]["enm1_tsa_con_el_gen"] if ident in c4 else "",
            "eje1_nivel": nivel_f, "eje1_puntaje": f"{p_f:.2f}",
            "mecanismos": f["mecanismos"],
            "n_mecanismos_publicado_no_puntuado": str(len(f["mecanismos"].split("|"))),
            "eje2_nivel": e["nivel"],
            "eje2_puntaje": e["puntaje"],
            "eje2_via": e["via"],
            "eje2_especie_donde_se_demostro": e["especie_donde_se_demostro"],
            "eje2_fuente_primaria_abierta": e["fuente_primaria_abierta"],
            "marcador_evidencia": f["marcador_evidencia"],
            "evidencia_negativa_medida": f["evidencia_negativa_medida"],
        })

    # --- Cohortes: por que ejes tiene calculados cada candidato (D87 4.2) ---
    # Eje 1 lo tienen todos los que entran al orden. Los ejes 2 y 4 definen la cohorte.
    DEF = {  # (tiene eje 2, tiene eje 3, tiene eje 4) -> (clave, nombre, ejes presentes)
        (True, True, True): ("A34", "A+3+4: ejes 1, 2, 3 y 4",
                             ("fenotipo", "esencialidad", "off_target", "conservacion")),
        (True, False, True): ("A4", "A+4: ejes 1, 2 y 4", ("fenotipo", "esencialidad", "conservacion")),
        (False, False, True): ("B4", "B+4: ejes 1 y 4", ("fenotipo", "conservacion")),
        (True, False, False): ("A", "A: ejes 1 y 2", ("fenotipo", "esencialidad")),
        (False, False, False): ("B", "B: solo eje 1", ("fenotipo",)),
    }
    CLAVE_PUNTAJE = {"fenotipo": "_f", "esencialidad": "_e", "off_target": "_o", "conservacion": "_c"}
    cohortes = {k: [] for k, _, _ in DEF.values()}
    pesos_coh = {}
    for r in en_orden:
        clave, nombre, ejes = DEF[(r["_e"] is not None, r["_o"] is not None, r["_c"] is not None)]
        base = sum(PESOS_D87[e] for e in ejes)
        w = {e: PESOS_D87[e] / base for e in ejes}
        pesos_coh[clave] = w
        r["cohorte"] = nombre
        r["pesos_renormalizados"] = " | ".join(
            f"{e} {w[e]:.3f}" if len(ejes) > 1 else "fenotipo 1,000" for e in ejes)
        r["puntaje"] = sum(w[e] * r[CLAVE_PUNTAJE[e]] for e in ejes)
        cohortes[clave].append(r)
    coh_a, coh_b = cohortes["A"], cohortes["B"]
    coh_a34, coh_a4, coh_b4 = cohortes["A34"], cohortes["A4"], cohortes["B4"]
    w_fen_a = pesos_coh["A"]["fenotipo"] if coh_a else None

    filas = []
    for cohorte in (coh_a34, coh_a4, coh_b4, coh_a, coh_b):
        cohorte.sort(key=lambda r: (-r["puntaje"], r["id"]))
        # Empates declarados: grupos consecutivos a menos de UMBRAL_EMPATE del primero del grupo.
        grupos, actual = [], []
        for r in cohorte:
            if actual and abs(actual[0]["puntaje"] - r["puntaje"]) >= UMBRAL_EMPATE:
                grupos.append(actual); actual = []
            actual.append(r)
        if actual:
            grupos.append(actual)
        puesto = 0
        for g in grupos:
            puesto += 1
            for r in g:
                r["puesto_en_su_cohorte"] = str(puesto)
                r["empate_declarado"] = ("si, con " + ", ".join(x["id"] for x in g if x is not r)
                                         if len(g) > 1 else "no")
            puesto += len(g) - 1
        filas.extend(cohorte)

    # --- Las columnas de off-target del catalogo: publicadas, con su panel, FUERA del puntaje ---
    for r in filas:
        v = cat[r["id"]].get("ventanas_21nt")
        r["eje3_estado"] = (
            f"calculado (PREREGISTRO_EJE3.md): fraccion limpia {r['eje3_puntaje']}, {r['eje3_vs_nulo']}"
            if r["eje3_puntaje"] else EJES_NO_CALCULABLE_FILA)
        r["eje4_estado"] = (
            f"calculado, regla de la enmienda 1: {r['eje4_puntaje']} "
            f"(cobertura {r['eje4_cobertura']}, {r['eje4_tsa_con_el_gen']} de 3 TSA con el gen)"
            if r["eje4_puntaje"] else
            "sin secuencia de D. maidis admisible en esta maquina (PREREGISTRO_EJE4.md §2)"
            if not r["eje4_cobertura"] else "cobertura insuficiente")
        r["eje5_estado_FALTANTE"] = EJES_NO_CALCULABLES["expresion_tejido"]
        for ref in PANEL_C5:
            clave = f"panelC5_NO_es_el_de_seis__21meros_perfectos_en_{ref}"
            r[clave] = (v or {}).get(f"21meros_perfectos_en_{ref}", "") or ""
        r["panelC5_ventanas_eficientes_sifi21"] = str((v or {}).get(
            "eficientes_sifi21_modo_fiel", "") or "")
        r["panelC5_mejor_region_200nt"] = (v or {}).get("mejor_region_200nt", "") or ""

    orden_cols = [
        "id", "gen", "especie", "familia_id", "cohorte", "puesto_en_su_cohorte",
        "empate_declarado", "puntaje", "pesos_renormalizados",
        "eje1_nivel", "eje1_puntaje", "mecanismos", "n_mecanismos_publicado_no_puntuado",
        "eje2_nivel", "eje2_puntaje", "eje2_via", "eje2_especie_donde_se_demostro",
        "eje2_fuente_primaria_abierta", "eje3_puntaje", "eje3_vs_nulo", "eje3_nulo_rango", "eje4_puntaje", "eje4_cobertura", "eje4_tsa_con_el_gen",
        "eje3_estado", "eje4_estado", "eje5_estado_FALTANTE",
        "marcador_evidencia", "evidencia_negativa_medida",
    ] + [f"panelC5_NO_es_el_de_seis__21meros_perfectos_en_{r}" for r in PANEL_C5] + [
        "panelC5_ventanas_eficientes_sifi21", "panelC5_mejor_region_200nt"]

    salida = BLOQUE / "resultados/orden_genes.tsv"
    with salida.open("w", encoding="utf-8", newline="") as fh:
        esc = csv.DictWriter(fh, fieldnames=orden_cols, delimiter="\t", lineterminator="\n",
                             extrasaction="ignore")
        esc.writeheader()
        for r in filas:
            esc.writerow({**r, "puntaje": f"{r['puntaje']:.4f}"})

    salida_fuera = BLOQUE / "resultados/fuera_del_orden.tsv"
    with salida_fuera.open("w", encoding="utf-8", newline="") as fh:
        esc = csv.DictWriter(fh, fieldnames=list(fuera[0]), delimiter="\t", lineterminator="\n")
        esc.writeheader()
        esc.writerows(fuera)

    # --- Sensibilidad: en que rango del peso de fenotipo cambia el primer puesto, por cohorte ---
    def barrido(cohorte, resto):
        pasos, cambios, previo = 2001, [], None
        for i in range(pasos):
            w = i / (pasos - 1)
            lider = primero_de(cohorte, w, resto)
            if previo is not None and lider != previo:
                cambios.append({"peso_fenotipo_aprox": round(w, 4), "de": previo, "a": lider})
            previo = lider
        return cambios
    resto_a = {"_e": 1.0}
    b_ese = PESOS_D87["esencialidad"] + PESOS_D87["conservacion"]
    resto_a4 = {"_e": PESOS_D87["esencialidad"] / b_ese, "_c": PESOS_D87["conservacion"] / b_ese}
    cambios = barrido(coh_a, resto_a) if coh_a else []
    lider_d84 = primero_de(coh_a, w_fen_a, resto_a) if coh_a else []
    cambios_a4 = barrido(coh_a4, resto_a4) if coh_a4 else []
    b3 = PESOS_D87["esencialidad"] + PESOS_D87["off_target"] + PESOS_D87["conservacion"]
    resto_a34 = {"_e": PESOS_D87["esencialidad"] / b3, "_o": PESOS_D87["off_target"] / b3,
                 "_c": PESOS_D87["conservacion"] / b3}
    cambios_a34 = barrido(coh_a34, resto_a34) if coh_a34 else []
    w_fen_a34 = pesos_coh["A34"]["fenotipo"] if coh_a34 else None
    lider_a34 = primero_de(coh_a34, w_fen_a34, resto_a34) if coh_a34 else []
    w_fen_a4 = pesos_coh["A4"]["fenotipo"] if coh_a4 else None
    lider_a4 = primero_de(coh_a4, w_fen_a4, resto_a4) if coh_a4 else []

    meta = {
        "linea": "F3 — recomendador de genes",
        "issue": 27,
        "fecha": "2026-10-27",
        "criterio": {
            "preregistro": "research/ola6/F3_recomendador_genes/PREREGISTRO.md",
            "adr_pesos": "D87, confirmado por el usuario el 2026-10-27",
            "pesos_declarados": PESOS_D87,
            "escala_eje1": "resultados/escala_fenotipo.md",
            "escala_eje2": "resultados/escala_esencialidad.md",
            "umbral_de_empate": UMBRAL_EMPATE,
        },
        "ejes_no_calculables": EJES_NO_CALCULABLES,
        "panel_de_las_columnas_de_off_target": {
            "referencias": PANEL_C5,
            "advertencia": "NO es el panel de seis. Estas columnas se publican fuera del "
                           "puntaje; ningun candidato se ordena por ellas.",
        },
        "conteos": {
            "filas_del_catalogo": len(fen),
            "en_el_orden": len(filas),
            "fuera_del_orden": len(fuera),
            "cohorte_A34_ejes_1_2_3_y_4": len(coh_a34),
            "cohorte_A4_ejes_1_2_y_4": len(coh_a4),
            "cohorte_B4_ejes_1_y_4": len(coh_b4),
            "cohorte_A_ejes_1_y_2": len(coh_a),
            "cohorte_B_solo_eje_1": len(coh_b),
            "con_eje2_desde_fuente_primaria_no_abierta": sum(
                1 for r in en_orden if r["_e"] is not None and r["eje2_fuente_primaria_abierta"] == "no"),
        },
        "sensibilidad_cohorte_A34": {
            "lider_con_los_pesos_de_D87": lider_a34,
            "peso_de_fenotipo_en_D87_renormalizado": round(w_fen_a34, 4) if w_fen_a34 else None,
            "cambios_de_primer_puesto_al_mover_el_peso_de_fenotipo_de_0_a_1": cambios_a34,
        },
        "sensibilidad_cohorte_A4": {
            "lider_con_los_pesos_de_D87": lider_a4,
            "peso_de_fenotipo_en_D87_renormalizado": round(w_fen_a4, 4) if w_fen_a4 else None,
            "cambios_de_primer_puesto_al_mover_el_peso_de_fenotipo_de_0_a_1": cambios_a4,
        },
        "eje4": {"regla": "enmienda 1 (PREREGISTRO_EJE4_ENMIENDA1.md); la original queda en "
                          "eje4_conservacion.tsv y no entra al puntaje",
                 "reporte": "resultados/eje4_REPORT.md"},
        "sensibilidad_cohorte_A": {
            "lider_con_los_pesos_de_D87": lider_d84,
            "peso_de_fenotipo_en_D87_renormalizado": round(w_fen_a, 4),
            "cambios_de_primer_puesto_al_mover_el_peso_de_fenotipo_de_0_a_1": cambios,
        },
        "entorno": {
            "python": sys.version.split()[0],
            "plataforma": sys.platform,
            "nota": "03_orden.py no usa herramientas externas: lee los ejes ya calculados. El eje 4 "
                    "lo calcula 05_eje_conservacion.py (BLAST+, Biopython, ahocorasick; ver "
                    "eje4_meta.json)",
        },
    }
    try:
        meta["commit_al_correr"] = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=RAIZ, capture_output=True,
            text=True, check=True).stdout.strip()
    except Exception as exc:                                     # pragma: no cover
        meta["commit_al_correr"] = f"(no se pudo leer: {exc})"

    (BLOQUE / "resultados/meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    print(f"orden: {len(filas)} candidatos en el orden, {len(fuera)} fuera")
    print(f"  cohortes: A+3+4 {len(coh_a34)} | A+4 {len(coh_a4)} | B+4 {len(coh_b4)} | A {len(coh_a)} | B {len(coh_b)}")
    for cohorte, nombre in ((coh_a34, "A+3+4"), (coh_a4, "A+4"), (coh_b4, "B+4"), (coh_a, "A"), (coh_b, "B")):
        if not cohorte:
            continue
        print(f"  --- cohorte {nombre} ---")
        for r in cohorte:
            emp = "" if r["empate_declarado"] == "no" else "  [EMPATE DECLARADO]"
            print(f"   {r['puesto_en_su_cohorte']:>2}. {r['id']} {r['puntaje']:.4f}  "
                  f"{r['eje1_nivel']}/{r['eje2_nivel']}  {r['gen'][:26]}{emp}")
    print()
    print(f"  lider de A+3+4 con los pesos de D87: {lider_a34}; cambios al mover w_fenotipo: {len(cambios_a34)}")
    for c in cambios_a34:
        print(f"    en w_fenotipo ~ {c['peso_fenotipo_aprox']}: {c['de']} -> {c['a']}")
    print(f"  lider de A+4 con los pesos de D87: {lider_a4}; cambios al mover w_fenotipo: {len(cambios_a4)}")
    for c in cambios_a4:
        print(f"    en w_fenotipo ~ {c['peso_fenotipo_aprox']}: {c['de']} -> {c['a']}")
    print(f"  lider de A con los pesos de D87: {lider_d84}; cambios al mover w_fenotipo: {len(cambios)}")
    for c in cambios:
        print(f"    en w_fenotipo ~ {c['peso_fenotipo_aprox']}: {c['de']} -> {c['a']}")
    print(f"escrito: {salida.relative_to(RAIZ)}, {salida_fuera.relative_to(RAIZ)}, meta.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
