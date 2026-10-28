"""Vista F: el enumerador de quimeras de O4, leido de disco.

De los 47,8 millones de combinaciones que la grilla recorre, 3.204 son admisibles, y esas 3.204
estan enumeradas y escritas. **Esta vista las muestra; no enumera nada.** El enumerador cuesta
una corrida larga y la grilla fina de paso 10 esta declarada como decision abierta: un boton que
lo corriera seria una mentira, pero mostrar lo que ya corrio no cuesta nada y es justamente lo
que faltaba para que el resultado se pueda mirar.

**La regla que esta vista tiene que respetar, y es la mas facil de romper: el orden ES el
criterio.** Los tres objetivos —`eficiencia_heredada`, `riesgo_minimo`, `cobertura_fenotipica`—
son **las mismas 3.204 quimeras ordenadas distinto**, asi que el primer puesto de cada uno es la
respuesta de ese objetivo y no una propiedad de la quimera. La vista:

  * muestra el orden **que el archivo trae**, y lo numera como viene;
  * **no** combina los tres objetivos en ningun indice;
  * si quien mira ordena la tabla por una columna, eso es comodidad de lectura y queda
    **marcado como tal**, separado del puesto del archivo.

Y la advertencia del JSON viaja arriba de la tabla y no al pie. Una tabla de 3.204 quimeras
ordenadas por eficiencia invita a leer el primer puesto como una recomendacion; el criterio de
eficiencia de si-Fi21 no esta validado en hemipteros y el archivo lo dice.
"""

from __future__ import annotations

from lectura import MOTORES, NO_DECLARADA, entero, leer_json, leer_tsv, procedencia, rel
from lectura import RAIZ

O4 = RAIZ / "research" / "ola6" / "O4_enumerador_quimeras" / "resultados"
COMANDO = "python research/ola6/O4_enumerador_quimeras/scripts/ (ver el REPORT de O4)"

# Los tres objetivos, con la pregunta que contesta cada uno. El texto es de la vista: el archivo
# trae el nombre del objetivo pero no que significa, y un selector con tres palabras sueltas no
# dice cual conviene mirar.
OBJETIVOS = {
    "eficiencia_heredada": {
        "titulo": "Eficiencia heredada",
        "pregunta": "cual quimera conserva mas ventanas eficientes de las que ya tenian sus dos "
                    "fragmentos por separado",
    },
    "riesgo_minimo": {
        "titulo": "Riesgo minimo",
        "pregunta": "cual quimera trae menos coincidencias con las referencias del panel, "
                    "contando aparte las que el empalme fabrica",
    },
    "cobertura_fenotipica": {
        "titulo": "Cobertura fenotipica",
        "pregunta": "cual quimera cubre los dos ejes de fenotipo declarados —reproduccion y "
                    "movilidad— con los dos genes que los aportan",
    },
}

# La grilla fina existe y no entra: son dos ordenes de magnitud mas filas y su destino es una
# decision abierta. Se nombra el archivo en vez de cargarlo.
GRILLA_FINA = O4 / "quimeras_enumeradas_o4_cobertura_fenotipica_paso10_corregido_vienna.tsv.gz"

COLS = ("quimera", "izquierda", "derecha", "a1", "l1", "a2", "l2", "largo_total_nt",
        "eje_izq", "eje_der", "ventanas_molecula",
        "ef_fragmento_izq_solo", "ef_fragmento_der_solo", "suma_de_las_partes",
        "ef_heredadas", "delta_heredadas_menos_suma", "heredadas_que_cambiaron",
        "max_nt_hasta_la_union_de_un_cambio", "ventanas_juntura", "ef_juntura",
        "juntura_con_blanco_continuo", "fabricados_21_refs", "fabricados_ge19_refs",
        "fabricados_refs", "aporte_del_bloque_mas_repartido",
        "fabricados_en_ventana_eficiente", "existe_en_el_genoma_del_vector",
        "alerta_juntura_nueva")

ENTEROS = ("a1", "l1", "a2", "l2", "largo_total_nt", "ventanas_molecula",
           "ef_fragmento_izq_solo", "ef_fragmento_der_solo", "suma_de_las_partes",
           "ef_heredadas", "delta_heredadas_menos_suma", "heredadas_que_cambiaron",
           "max_nt_hasta_la_union_de_un_cambio", "ventanas_juntura", "ef_juntura",
           "juntura_con_blanco_continuo", "fabricados_21_refs", "fabricados_ge19_refs",
           "aporte_del_bloque_mas_repartido", "fabricados_en_ventana_eficiente")


def _rutas(objetivo: str) -> tuple:
    base = "quimeras_enumeradas_o4_%s_corregido_vienna" % objetivo
    return O4 / (base + ".tsv"), O4 / (base + ".json")


def _procedencia(meta, tsv) -> dict:
    """Modo, motor y panel del tamizado de juntura, leidos del JSON del objetivo."""
    if not isinstance(meta, dict):
        return procedencia(tsv, nota="falta el JSON del objetivo, que es donde se declaran el "
                                     "modo, el motor y el panel de esta corrida")
    backend = (meta.get("backend") or "").strip()
    tam = meta.get("tamizado_de_juntura") or {}
    panel = tam.get("panel") or tam.get("referencias") or NO_DECLARADA
    return procedencia(
        tsv,
        modo=(meta.get("modo") or NO_DECLARADA).strip() or NO_DECLARADA,
        motor=MOTORES.get(backend, NO_DECLARADA if not backend else backend),
        panel=panel,
        nota="tabla %s, %s °C. %s" % (meta.get("tabla_nn", "?"), meta.get("temp_c", "?"),
                                      tam.get("que_se_busca", "")))


def inventario() -> dict:
    """Que objetivos hay en disco, para que el selector no sea una lista fija."""
    out = []
    for clave, d in OBJETIVOS.items():
        tsv, js = _rutas(clave)
        out.append({"objetivo": clave, "titulo": d["titulo"], "pregunta": d["pregunta"],
                    "en_disco": tsv.is_file(), "archivo": rel(tsv)})
    return {"estado": "listo", "objetivos": out}


def ver(objetivo: str = "eficiencia_heredada", *, desde: int = 0, cuantas: int = 50,
        izquierda: str = "", derecha: str = "", solo_con_alerta: bool = False,
        l1: int | None = None) -> dict:
    """Las quimeras de un objetivo, en el orden del archivo, con filtros de lectura.

    `desde` y `cuantas` paginan. Los filtros **no cambian el orden**: recortan las filas y
    conservan el puesto que cada una traia, que es lo que mantiene legible que el orden es del
    archivo y no de la vista.
    """
    if objetivo not in OBJETIVOS:
        raise ValueError("el objetivo es uno de %s; recibi %r"
                         % (", ".join(OBJETIVOS), objetivo))
    tsv, js = _rutas(objetivo)
    filas, problema = leer_tsv(tsv, COMANDO)
    if problema:
        return dict(problema, vista="quimeras", objetivo=objetivo)
    meta, falta_meta = leer_json(js, COMANDO)

    # El puesto se asigna ANTES de filtrar: es la posicion en el archivo, no en lo que quedo
    # despues del filtro. Renumerar despues de filtrar convertiria el filtro en un criterio.
    todas = []
    for i, f in enumerate(filas, start=1):
        d = {c: f.get(c, "") for c in COLS}
        for c in ENTEROS:
            d[c] = entero(f.get(c))
        d["puesto_en_el_archivo"] = i
        d["fabricados_refs"] = [x.strip() for x in (f.get("fabricados_refs") or "").split(",")
                                if x.strip()]
        todas.append(d)

    sel = todas
    if izquierda:
        sel = [d for d in sel if d["izquierda"] == izquierda]
    if derecha:
        sel = [d for d in sel if d["derecha"] == derecha]
    if solo_con_alerta:
        sel = [d for d in sel if (d["alerta_juntura_nueva"] or "").strip() == "si"]
    if l1 is not None:
        sel = [d for d in sel if d["l1"] == l1]

    desde = max(0, int(desde))
    cuantas = max(1, min(int(cuantas), 500))
    pagina = sel[desde:desde + cuantas]

    grilla = (meta or {}).get("grilla") or {}
    con_alerta = sum(1 for d in todas if (d["alerta_juntura_nueva"] or "").strip() == "si")

    return {
        "estado": "listo", "vista": "quimeras", "objetivo": objetivo,
        "titulo": OBJETIVOS[objetivo]["titulo"],
        "pregunta": OBJETIVOS[objetivo]["pregunta"],
        "filas": pagina,
        "total_en_el_archivo": len(todas), "total_filtrado": len(sel),
        "desde": desde, "cuantas": cuantas,
        "orden": "el que trae el archivo: la fila 1 es el primer puesto de este objetivo. La "
                 "vista no reordena ni combina los tres objetivos, porque el orden ES el "
                 "criterio y cambiarlo seria calcular uno nuevo.",
        # La advertencia del archivo, arriba y no al pie: califica todas las columnas de
        # eficiencia de esta tabla.
        "advertencia": (meta or {}).get("advertencia", ""),
        "grilla": {
            "combinaciones_antes_de_podar": grilla.get("combinaciones_antes_de_podar"),
            "combinaciones_admisibles": grilla.get("combinaciones_admisibles"),
            "paso": grilla.get("paso"), "l1_min": grilla.get("l1_min"),
            "l1_max": grilla.get("l1_max"), "largo_total": grilla.get("largo_total"),
        },
        "plegados": (meta or {}).get("plegados"),
        "ejes_declarados": (meta or {}).get("ejes_declarados") or {},
        "genes": {k: {"n": v.get("n"), "desde": v.get("desde"), "hasta": v.get("hasta")}
                  for k, v in ((meta or {}).get("genes") or {}).items()},
        "con_alerta_de_juntura_nueva": con_alerta,
        "izquierdas": sorted({d["izquierda"] for d in todas if d["izquierda"]}),
        "derechas": sorted({d["derecha"] for d in todas if d["derecha"]}),
        "l1_posibles": sorted({d["l1"] for d in todas if d["l1"] is not None}),
        "procedencia": _procedencia(meta, tsv),
        "configuracion_declarada": falta_meta is None,
        "falta_configuracion": falta_meta,
        "archivo": rel(tsv), "archivo_configuracion": rel(js),
        # La grilla fina no entra, y se dice cual es y por que.
        "grilla_fina": {
            "archivo": rel(GRILLA_FINA), "en_disco": GRILLA_FINA.is_file(),
            "nota": "la grilla de paso 10 —169.648 combinaciones— existe en disco y no entra a "
                    "esta vista: son dos ordenes de magnitud mas filas y si se reparte entre "
                    "maquinas o se archiva es una decision abierta (D89, issue #42).",
        },
    }
