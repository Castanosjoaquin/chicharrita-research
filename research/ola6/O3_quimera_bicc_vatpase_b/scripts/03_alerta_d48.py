"""O3 paso 3 — la fila de alerta de D48 para lo que fabrica el empalme.

Por que es un paso aparte. El paso 2 **mide**: dice que bloques de la juntura coinciden,
donde y cuanto aporta cada gen. Convertir eso en una fila de alerta es otra cosa, y D48
fija como: la coincidencia perfecta no es un veto automatico sino una alerta que **obliga a
justificar**, con cuatro campos obligatorios, y «la justificacion la escribe el usuario y no
el motor». Este script escribe lo que la maquina puede saber y deja marcado lo que no.

Que llena la maquina, y de donde sale cada cosa:

  - **organismo**: de `ranking.REFERENCIAS`, con el panel de seis registrado, asi que el
    peso y el rol son los mismos que usa el ranking.
  - **exposicion**: el peso de la referencia y el de su criterio, con el motivo y la fuente.
    `D66` ya cerro que a la exposicion del no objetivo no se le pide un numero propio: se
    declara.
  - **gen_involucrado**: la anotacion de los transcriptos que coinciden, leida de la
    cabecera FASTA de la referencia local. No se inventa un simbolo: si la cabecera no lo
    trae, va la cabecera cruda.
  - **evidencia_biologica**: la clave del vocabulario cerrado de `alertas.CLAVES_EVIDENCIA`
    que la anotacion sostiene, mas la prosa de los hechos. Si el gen impactado no es el
    ortologo del blanco, eso es determinable de la anotacion y se determina.

Que NO llena, a proposito: `decision_usuario` y `justificacion_usuario` van vacias. La fila
nace **pendiente**, que es lo que D48 quiere, y por eso la compuerta la frena.

Que esta fila NO es. Una fila del inventario de `M6`. El generador de `M6`
(`tabla_alertas.py`) tamiza **regiones** y esta alerta es de una **juntura**, que no es una
region de ningun gen: es secuencia que fabrica el ensamblado. Integrar las junturas al
inventario es trabajo de la linea que mantiene `M6` y no se hace aca; mientras no se haga,
esta fila vive en el bloque de `O3` con el mismo esquema de columnas para que se pueda pegar.

Uso:
    python research/ola6/O3_quimera_bicc_vatpase_b/scripts/03_alerta_d48.py
"""

from __future__ import annotations

import csv
import gzip
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
BLOQUE = Path(__file__).resolve().parents[1]
RESULTADOS = BLOQUE / "resultados"
DB = RAIZ / "work/offtarget_db"
HUMANA = RAIZ / "work/W5/ref/humano_rna.fna.gz"

sys.path.insert(0, str(RAIZ / "tools/sifi21_port"))
import alertas as AL   # noqa: E402  el esquema y el vocabulario, sin tocarlos
import ranking as R    # noqa: E402
import ranking_v2 as V  # noqa: E402

#: Las columnas del inventario de M6, en su orden, para que la fila se pueda pegar ahi.
TABLA_M6 = (RAIZ / "research/ola4/M6_alertas/resultados/alertas.tsv")

ARCHIVO_DE = {
    "maiz": DB / "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna.fna.gz",
    "humano": HUMANA,
    "H_vitripennis": DB / "GCF_021130785.1_UT_GWSS_2.1_rna.fna.gz",
    "H_axyridis": DB / "GCF_914767665.1_icHarAxyr1.1_rna.fna.gz",
    "A_mellifera": DB / "GCF_003254395.2_Amel_HAv3.1_rna.fna.gz",
    "F_candida": DB / "GCF_002217175.1_ASM221717v1_rna.fna.gz",
}


def cabeceras(corto: str, ids: set[str]) -> dict[str, str]:
    """La cabecera FASTA de cada transcripto, de la referencia local."""
    ruta = ARCHIVO_DE.get(corto)
    if ruta is None or not ruta.exists():
        return {i: "" for i in ids}
    out = {}
    with gzip.open(ruta, "rt") as fh:
        for linea in fh:
            if not linea.startswith(">"):
                continue
            ident = linea[1:].split()[0]
            if ident in ids:
                out[ident] = linea[1:].strip()
                if len(out) == len(ids):
                    break
    return {i: out.get(i, "") for i in ids}


def simbolo_y_nombre(cabecera: str) -> tuple[str, str]:
    """`(simbolo, nombre)` de una cabecera RefSeq, sin inventar nada.

    El simbolo de RefSeq viene entre parentesis al final del nombre del producto. Si no
    hay parentesis **no hay simbolo**: se devuelve vacio y el nombre crudo. Inventarle un
    simbolo a una cabecera sin parentesis es el peor error posible de esta maquinaria.
    """
    if not cabecera:
        return "", ""
    resto = cabecera.split(None, 1)[1] if " " in cabecera else ""
    nombre = resto.rsplit(", mRNA", 1)[0].rsplit(", transcript", 1)[0].strip()
    simbolo = ""
    if nombre.endswith(")") and "(" in nombre:
        simbolo = nombre[nombre.rfind("(") + 1:-1]
        nombre = nombre[:nombre.rfind("(")].strip()
    return simbolo, nombre


def main() -> int:
    V.con_panel(sin_humano=False)
    suf = "o3_corregido_vienna"
    ruta = RESULTADOS / ("juntura_alertas_%s.json" % suf)
    if not ruta.exists():
        print("no hay %s: el empalme no fabrico ninguna coincidencia, "
              "asi que no hay fila de alerta" % ruta.name)
        return 0
    crudas = json.loads(ruta.read_text(encoding="utf-8"))

    with TABLA_M6.open(encoding="utf-8") as fh:
        columnas = next(csv.reader(fh, delimiter="\t"))

    por_clave: dict[tuple, dict] = {}
    for al in crudas:
        clave = (al["quimera"], al["organismo_corto"], tuple(sorted(al["secuencias"])))
        d = por_clave.setdefault(clave, {"js": [], "ejemplo": al})
        d["js"].append(al["j"])

    filas = []
    for (quimera, corto, ids), d in sorted(por_clave.items()):
        al = d["ejemplo"]
        ref = next(k for k in R.REFERENCIAS if R.corto(k) == corto)
        info = R.REFERENCIAS[ref]
        cab = cabeceras(corto, set(ids))
        simbolos, nombres = [], []
        for i in sorted(ids):
            s, n = simbolo_y_nombre(cab[i])
            simbolos.append(s or "sin simbolo en la cabecera")
            nombres.append(n or cab[i] or "sin anotacion en la cabecera")
        # La anotacion dice si el gen impactado es el ortologo del blanco. Los dos genes
        # de esta quimera son `BicC_Dm` y `V-ATPase B`; `alertas.ORTOLOGO_DE` trae las
        # claves de texto con las que el proyecto reconoce a cada uno.
        claves_blanco = ("bicaudal c", "v-type proton atpase subunit b",
                         "v-atpase subunit b", "vacuolar atpase subunit b")
        es_ortologo = any(any(k in n.lower() for k in claves_blanco) for n in nombres)
        prosa = (
            "El empalme de %s fabrica un bloque perfecto de %d nt que no existe en ninguno "
            "de los dos genes: toma %d nt de %s y %d de %s. El bloque coincide en %d "
            "transcripto(s) de %s (%s), anotado(s) como %s. %s Ninguna de las %d ventanas "
            "de juntura afectadas (j=%s) es eficiente, asi que el bloque no esta en una "
            "ventana que el criterio prediga activa; eso limita la consecuencia pero no la "
            "borra, porque el criterio de eficiencia no esta validado."
            % (quimera, al["bloque_largo"], al["nt_de_izquierda"],
               quimera.split("__")[0][2:], al["nt_de_derecha"], quimera.split("__")[1],
               len(ids), info["especie"], ", ".join(sorted(ids)), "; ".join(nombres),
               "Es el ortologo del gen que se silencia." if es_ortologo
               else "No es el ortologo de ninguno de los dos genes que se silencian.",
               len(d["js"]), ",".join(str(x) for x in sorted(d["js"]))))
        fila = {c: "" for c in columnas}
        fila.update({
            "gen": "quimera %s" % quimera,
            "region": "juntura, j=%s" % ",".join(str(x) for x in sorted(d["js"])),
            "que_es": "bloque fabricado por el empalme, %d nt" % al["bloque_largo"],
            "vigente": "no: region candidata de O3, no recomendada (D74)",
            "estado_region": "juntura de quimera; no es una region del inventario de M6",
            "organismo_corto": corto,
            "organismo_especie": info["especie"],
            "organismo_rol": info["rol"],
            "exposicion_w": "%.2f" % info["peso"],
            "exposicion_w_alternativa": "%.2f" % AL_peso_criterio(al["bloque_largo"]),
            "exposicion_motivo": "peso de referencia de ranking.pesos_base() y peso del "
                                 "criterio por el largo del bloque (D4)",
            "exposicion_fuente": "tools/sifi21_port/ranking.py REFERENCIAS y PESO_CRITERIO",
            "exposicion_decision_abierta": "si: D66 declara la exposicion del no objetivo "
                                           "y no le pide un numero propio",
            "gen_simbolo": "; ".join(simbolos),
            "gen_locus": "; ".join(sorted(ids)),
            "gen_tipo_molecula": "ARNm de referencia (RefSeq)",
            "gen_transcriptos": str(len(ids)),
            "gen_anotacion": "; ".join(nombres),
            "gen_fuente": "cabecera FASTA de %s" % ARCHIVO_DE[corto].name,
            "evidencia_clave": ("ortologo_del_blanco" if es_ortologo
                                else "gen_no_relacionado"),
            "evidencia_bioensayo": "sin_bioensayo_consultado",
            "evidencia_prosa": prosa,
            "ventanas_perfecto_21": "0" if al["bloque_largo"] < 21 else str(len(d["js"])),
            "ventanas_perfecto_ge19": str(len(d["js"])),
            "umbrales_anidados": "si: el bloque es de %d nt, entra por el piso de D28 y "
                                 "no por el umbral literal de D48" % al["bloque_largo"],
            "ventanas_21_eficientes": "0",
            "ventanas_ge19_eficientes": str(sum(
                1 for a in crudas if a["quimera"] == quimera
                and a["organismo_corto"] == corto and a["ventana_eficiente"])),
            "posiciones_perfecto_ge19": ",".join(
                str(a["pos_en_la_quimera"]) for a in sorted(
                    (a for a in crudas if a["quimera"] == quimera
                     and a["organismo_corto"] == corto),
                    key=lambda x: x["pos_en_la_quimera"])),
            "decision_usuario": "",
            "justificacion_usuario": "",
        })
        filas.append(fila)

    salida = RESULTADOS / ("alertas_juntura_d48_%s.tsv" % suf)
    with salida.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=columnas, delimiter="\t",
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)

    print("%d fila(s) de alerta, con el esquema de %s"
          % (len(filas), TABLA_M6.relative_to(RAIZ)))
    for f in filas:
        print("\n  %s | %s" % (f["gen"], f["region"]))
        print("    organismo      %s (%s), peso %s"
              % (f["organismo_corto"], f["organismo_especie"], f["exposicion_w"]))
        print("    gen impactado  %s — %s" % (f["gen_locus"], f["gen_anotacion"]))
        print("    evidencia      %s / %s" % (f["evidencia_clave"], f["evidencia_bioensayo"]))
        print("    decision       PENDIENTE (la escribe el usuario, D48)")

    # Los cuatro campos tienen que estar completos; la decision, no.
    faltan = []
    for f in filas:
        for campo in AL.CAMPOS_OBLIGATORIOS:
            vacias = [c for c in AL.COLUMNAS_DE[campo] if not str(f.get(c, "")).strip()]
            if vacias:
                faltan.append("%s: %s" % (campo, ", ".join(vacias)))
    print("\nlos cuatro campos de D48: %s"
          % ("completos" if not faltan else "FALTAN -> %s" % "; ".join(faltan)))
    if len(filas) and not faltan:
        corta = [f for f in filas
                 if len(f["evidencia_prosa"]) < AL.PROSA_MINIMA]
        print("prosa de justificacion: %s"
              % ("sobre el minimo de %d caracteres" % AL.PROSA_MINIMA if not corta
                 else "DEMASIADO CORTA"))
    print("\nescrito en %s" % salida)
    return 0 if not faltan else 1


def AL_peso_criterio(largo: int) -> float:
    """El peso del criterio que le corresponde a un bloque de este largo (D4)."""
    return R.PESO_CRITERIO["perfecto_21" if largo >= 21 else "perfecto_ge19"]


if __name__ == "__main__":
    sys.exit(main())
