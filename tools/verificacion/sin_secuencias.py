"""Busca secuencias de nucleotidos en el arbol versionado, en el indice y en el historial.

Por que existe: en C9 se commitearon TSV con una columna `seq` de 21-meros solapados
de a 1 nt, y como las ventanas se solapan esa columna reconstruye el gen completo.
Dos de los cuatro genes son secuencias de EPILAB, que por la regla de confidencialidad
de CLAUDE.md no se publican. Se detecto revisando el diff antes de pushear y se
reescribieron los tres commits locales. La herramienta que lo evito era local a una
linea de investigacion (`research/ola3/C9_sensibilidad_umbral/scripts/limpiar_ancla.py`,
que solo miraba una carpeta); esto la promueve al repositorio entero. Linea M9 de la
ola 4, issue #13.

Que chequea, en dos pasadas distintas:

  1. **Rachas.** Tramos de 21 nt o mas de alfabeto de nucleotidos. Es el umbral del
     proyecto porque 21 nt es el largo de la ventana de si-Fi21 y el umbral de veto
     de off-target (D28): una racha de 21 es exactamente lo que no debe salir.

  2. **Columnas de k-meros solapados.** El incidente de C9 no se atrapa solo con el
     umbral de 21: una columna de 20-meros, o de 15-meros, tambien reconstruye el gen
     si las filas consecutivas se solapan. Esta pasada busca, en archivos tabulares y
     JSON, grupos de >= 10 valores cortos de nucleotidos (>= 12 nt) donde el sufijo de
     uno es el prefijo del siguiente, y reporta cuantos nt reconstruye la cadena. Es
     la forma exacta del incidente y ninguna racha individual la delata.

Lo que el reporte **no** hace es imprimir la secuencia encontrada. Informa archivo,
linea, largo y un hash corto, porque un reporte de fuga que copia el dato fugado es
el mismo problema con otro nombre. Para ver el contenido hay que abrir el archivo.

Modos:
    python tools/verificacion/sin_secuencias.py                 # arbol versionado (HEAD)
    python tools/verificacion/sin_secuencias.py --staged        # solo el indice (pre-commit)
    python tools/verificacion/sin_secuencias.py --historial     # lineas agregadas en git log -p
    python tools/verificacion/sin_secuencias.py --sin-excepciones   # ignora la lista blanca
    python tools/verificacion/sin_secuencias.py --json salida.json  # reporte legible por maquina

Codigo de salida: 0 si no hay hallazgos no exceptuados, 1 si los hay. Eso es lo que
lo hace util como gancho de pre-commit.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

# --- Parametros del chequeo -------------------------------------------------

LARGO_RACHA = 21          # nt; el largo de la ventana de si-Fi21 y el umbral de veto (D28)
LARGO_KMERO = 12          # nt; largo minimo para considerar un valor como k-mero
MIN_KMEROS = 10           # cuantos k-meros solapados hacen falta para reportar
MAX_FRACCION_N = 0.2      # un tramo con mas de 20 % de N no se cuenta como secuencia

RE_RACHA = re.compile(r"[ACGTUNacgtun]{%d,}" % LARGO_RACHA)
RE_KMERO = re.compile(r"^[ACGTUacgtu]{%d,}$" % LARGO_KMERO)

# Extensiones binarias o de indice que no se leen como texto.
EXT_BINARIAS = {
    ".bwt", ".ebwt", ".rev", ".amb", ".ann", ".pac", ".sa", ".nhr", ".nin", ".nsq",
    ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".xlsx", ".pptx", ".docx", ".zip",
    ".gz", ".bz2", ".tar", ".pyc", ".so", ".dylib", ".h5", ".npy", ".npz",
}

# --- Lista blanca -----------------------------------------------------------
# Cada excepcion lleva su motivo por escrito. Una excepcion sin motivo no es una
# excepcion, es un agujero. El motivo tiene que decir por que el dato es publico,
# no por que molesta el hallazgo.

EXCEPCIONES: list[tuple[str, str]] = [
    (
        "research/ola3/C9_sensibilidad_umbral/datos/cedden2025_28dsrna_con_secuencia.csv",
        "D41: los 28 ARNdc de Cedden et al. 2025 (PMC12039203, CC BY) son de Tribolium "
        "castaneum y no tienen relacion con las secuencias de EPILAB. Publicados a "
        "proposito y declarados en el LEEME de datos/.",
    ),
    (
        "research/ola2/W2_herramientas/ejemplos/*",
        "El README de la carpeta declara cada entrada con su accesion del NCBI "
        "(`PZ371507.1`, `PZ371508.1`, `NC_002786.2`, ARNm RefSeq de Zea mays y Apis "
        "mellifera) y que ninguna consulta se envio a un servicio web. Las salidas de "
        "la carpeta derivan de esas mismas entradas publicas.",
    ),
    (
        "research/ola3/C5_estructura_genes_ingenieria_inversa/resultados/candidatos_c5.fa",
        "Cada cabecera lleva su accesion publica (PZ371507, PZ371508, GJQL01135962, "
        "GFTU01006765, XM_054426723 y demas): son transcriptos de NCBI, no material de "
        "EPILAB.",
    ),
    (
        "baseline_dsrip/ventanas_multigen.csv",
        "Las ventanas se enumeran sobre CDS armados por `baseline_dsrip/gen_multi.py` "
        "desde el genoma y el GFF de referencia de Tribolium castaneum (constantes "
        "GENOMA y GFF_TCAS del pipeline), que son publicos. Los 20 loci llevan nombre de "
        "ortologo de Drosophila. Lo que no tiene licencia abierta son los fenotipos de "
        "iBeetle-Base, que no estan en este archivo.",
    ),
    (
        "tools/sifi21_port/conservacion.py",
        "Los cebadores son la Tabla 1 de Andrada et al. 2026 (Front Insect Sci "
        "6:1811933, leida en PMC13279319), publicada.",
    ),
    (
        "tools/sifi21_port/test_sifi.py",
        "Fixtures de prueba: el ejemplo del docstring de `free_energy3` del si-Fi21 "
        "original y secuencias de control. Verificado que ninguna es de EPILAB.",
    ),
    (
        "sifi_plus/datos_ejemplo/*",
        "El dato de ejemplo de la interfaz es `NM_001111367.2`, el ARNm de la ferredoxina-6 "
        "de Zea mays, con su accesion en el encabezado. Es RefSeq publico y no tiene relacion "
        "con las cuatro regiones de EPILAB: la pasada contra la planilla da cero. Se eligio "
        "el maiz y no el genoma del MRFV a proposito, porque `NC_002786.2` cubre el 90,5 % "
        "de MP_MRFV y el 96,5 % de CP_MRFV (M9 §3.2) y, aunque eso es publico y no una fuga, "
        "no conviene mandarselo al investigador dentro de nuestra herramienta.",
    ),
    (
        "sifi_plus/test_api.py",
        "Fixtures de prueba del criterio de baja complejidad: poli-A, un dinucleotido "
        "alternado y un 21-mero sintetico de composicion normal. Verificado contra la "
        "planilla: ninguna es de EPILAB.",
    ),
    (
        "pipeline/test_features.py",
        "Fixtures de prueba sinteticas (horquilla, secuencia suelta, CDS de juguete). "
        "Verificado que ninguna es de EPILAB.",
    ),
    (
        "research/ola2/W4_genomas/REPORT.md",
        "Tres 21-meros de Coccinella septempunctata citados en el cuerpo del informe "
        "para mostrar que son solapados y forman una sola ventana de 23 nt. Genoma "
        "publico.",
    ),
    (
        "research/ola2/W3_bases_datos/consultas/04_descarga_real_mrfv.md",
        "Dos lineas del FASTA de MRFV `NC_002786.2`, pegadas como evidencia de que la "
        "descarga por E-utilities funciono. Accesion publica.",
    ),
    (
        "research/R7_microgravedad/M4_mollicutes_estructura/datos/*",
        "Secuencias de entradas del PDB (8P6P, 7P6Z, 7OOC) y ARNr 16S de accesiones "
        "publicas, bajadas por la consulta GraphQL que esta en la misma carpeta.",
    ),
]


def esta_exceptuada(ruta: str) -> str | None:
    """Devuelve el motivo si la ruta esta en la lista blanca, o None."""
    for patron, motivo in EXCEPCIONES:
        if ruta == patron or fnmatch.fnmatch(ruta, patron):
            return motivo
    return None


# --- Deteccion --------------------------------------------------------------


def _huella(tramo: str) -> str:
    """Hash corto del tramo, para poder cotejar dos hallazgos sin copiar la secuencia."""
    return hashlib.sha256(tramo.upper().encode()).hexdigest()[:10]


def _es_secuencia(tramo: str) -> bool:
    """Descarta tramos que son mayormente N (una racha de NNNN no es un dato fugado)."""
    enes = sum(1 for c in tramo.upper() if c == "N")
    return (enes / len(tramo)) <= MAX_FRACCION_N


ALFANUM_NO_NT = re.compile(r"[B-FH-MO-SV-Zb-fh-mo-sv-z0-9+/=]")


def _dentro_de_token_mayor(linea: str, ini: int, fin: int) -> bool:
    """True si el tramo es parte de un token mas largo que no es secuencia.

    Atrapa el caso real que aparecio en `research/ola2/W6_agentes_ciencia/index.html`:
    una fuente woff2 embebida en base64 contiene por azar tramos largos de A, C, G y T.
    Si el caracter pegado al tramo es alfanumerico y no es un nucleotido, el tramo no es
    una secuencia: es el interior de otra cosa.
    """
    if ini > 0 and ALFANUM_NO_NT.match(linea[ini - 1]):
        return True
    if fin < len(linea) and ALFANUM_NO_NT.match(linea[fin]):
        return True
    return False


def buscar_rachas(texto: str, ruta: str) -> list[dict]:
    """Pasada 1: tramos de LARGO_RACHA nt o mas, con su linea."""
    hallazgos = []
    for n, linea in enumerate(texto.split("\n"), start=1):
        for m in RE_RACHA.finditer(linea):
            tramo = m.group(0)
            if not _es_secuencia(tramo):
                continue
            if _dentro_de_token_mayor(linea, m.start(), m.end()):
                continue
            hallazgos.append(
                {
                    "tipo": "racha",
                    "archivo": ruta,
                    "linea": n,
                    "columna": m.start() + 1,
                    "largo_nt": len(tramo),
                    "huella": _huella(tramo),
                }
            )
    return hallazgos


def _series_candidatas(texto: str, ruta: str) -> list[list[tuple[int, str]]]:
    """Agrupa los k-meros por **columna**, no por orden de aparicion.

    Esto importa: un TSV con una columna `sitio` y otra `guia` intercala dos series en
    cada linea, y recorrer celda por celda rompe la cadena en cada fila. Agrupar por
    indice de columna es lo que deja ver la serie. Lo descubrio la primera corrida de
    esta herramienta sobre `baseline_dsrip/ventanas_multigen.csv`, que tiene 47.224
    k-meros en dos columnas y no reportaba ni una cadena.
    """
    sufijo = Path(ruta).suffix.lower()
    series: dict[int | str, list[tuple[int, str]]] = {}
    if sufijo in {".tsv", ".csv", ".txt"}:
        sep = "," if sufijo == ".csv" else "\t"
        for n, linea in enumerate(texto.split("\n"), start=1):
            for col, celda in enumerate(linea.split(sep)):
                celda = celda.strip().strip('"').strip("\r")
                if RE_KMERO.match(celda):
                    series.setdefault(col, []).append((n, celda))
    elif sufijo == ".json":
        # Sin parsear: los k-meros aparecen como strings entrecomillados. Se agrupan por
        # la clave que los precede, que es el analogo de la columna.
        for n, linea in enumerate(texto.split("\n"), start=1):
            for clave, s in re.findall(
                r'"(\w+)"\s*:\s*"([ACGTUacgtu]{%d,})"' % LARGO_KMERO, linea
            ):
                series.setdefault(clave, []).append((n, s))
            for s in re.findall(r'(?<![:,]\s)"([ACGTUacgtu]{%d,})"' % LARGO_KMERO, linea):
                series.setdefault("_lista", []).append((n, s))
    return [v for v in series.values() if len(v) >= MIN_KMEROS]


def _desplazamiento(recon: str, v: str) -> int:
    """Cuantos nt nuevos aporta `v` al final de `recon`, por solapamiento maximo.

    Devuelve len(v) si no hay solapamiento. Solo se aceptan solapamientos de al menos
    la mitad del k-mero: coincidencias de 1 o 2 nt son azar, no una cadena.
    """
    minimo_solape = max(1, len(v) // 2)
    for d in range(1, len(v) - minimo_solape + 1):
        if recon[-(len(v) - d):] == v[: len(v) - d]:
            return d
    return len(v)


def buscar_kmeros_solapados(texto: str, ruta: str) -> list[dict]:
    """Pasada 2: cadenas de k-meros donde el sufijo de uno es el prefijo del siguiente.

    Reconstruye la cadena para medir cuantos nt cubre, pero no la devuelve: lo que
    sale del chequeo es el largo y la huella.

    Cada serie se recorre en los dos sentidos y se queda el que reconstruye mas. Una
    columna antisentido —el complemento reverso de la ventana, como `antisense_5_3` de
    dsRIP— encadena al reves: el sufijo del k-mero siguiente es el prefijo del anterior.
    Mirando un solo sentido esa columna no se ve, y reconstruye igual.
    """
    hallazgos: list[dict] = []
    for valores in _series_candidatas(texto, ruta):
        directa = _cadenas_de_serie(valores, ruta)
        inversa = _cadenas_de_serie(list(reversed(valores)), ruta)
        mejor = max(
            (directa, inversa),
            key=lambda hs: max((h["nt_reconstruidos"] for h in hs), default=0),
        )
        for h in mejor:
            if mejor is inversa:
                h["sentido"] = "antisentido"
                h["linea_desde"], h["linea_hasta"] = h["linea_hasta"], h["linea_desde"]
        hallazgos.extend(mejor)
    return hallazgos


def _cadenas_de_serie(valores: list[tuple[int, str]], ruta: str) -> list[dict]:
    hallazgos = []
    cadena: list[tuple[int, str]] = []

    def cerrar(cadena: list[tuple[int, str]]) -> None:
        if len(cadena) < MIN_KMEROS:
            return
        # Reconstruye por solapamiento maximo: d es el desplazamiento, o sea cuantos
        # nt nuevos aporta el k-mero siguiente. El minimo d que encaja es el maximo
        # solapamiento.
        recon = cadena[0][1].upper()
        for _, v in cadena[1:]:
            v = v.upper()
            d = _desplazamiento(recon, v)
            recon += v[len(v) - d:] if d < len(v) else v
        hallazgos.append(
            {
                "tipo": "kmeros_solapados",
                "archivo": ruta,
                "linea_desde": cadena[0][0],
                "linea_hasta": cadena[-1][0],
                "n_kmeros": len(cadena),
                "largo_kmero": len(cadena[0][1]),
                "nt_reconstruidos": len(recon),
                "huella": _huella(recon),
            }
        )

    for n, v in valores:
        if cadena:
            prev = cadena[-1][1].upper()
            cur = v.upper()
            # Solapan si el sufijo de uno es el prefijo del otro en al menos la mitad
            # del k-mero. Mismo criterio que usa la reconstruccion.
            if len(cur) == len(prev) and _desplazamiento(prev, cur) < len(cur):
                cadena.append((n, v))
                continue
            cerrar(cadena)
            cadena = []
        cadena.append((n, v))
    cerrar(cadena)
    return hallazgos


# --- Recorridos -------------------------------------------------------------


def _git(args: list[str], raiz: Path) -> str:
    return subprocess.run(
        ["git", *args], cwd=raiz, capture_output=True, text=True, errors="replace"
    ).stdout


def _leer(raiz: Path, ruta: str, desde_indice: bool) -> str | None:
    if Path(ruta).suffix.lower() in EXT_BINARIAS:
        return None
    if desde_indice:
        texto = _git(["show", f":{ruta}"], raiz)
    else:
        p = raiz / ruta
        if not p.is_file():
            return None
        try:
            texto = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None
    if "\x00" in texto[:4096]:
        return None
    return texto


def escanear_arbol(
    raiz: Path, desde_indice: bool, epilab: tuple[dict, dict] | None, solo_epilab: bool
) -> tuple[list[dict], int]:
    if desde_indice:
        salida = _git(["diff", "--cached", "--name-only", "--diff-filter=ACM"], raiz)
    else:
        salida = _git(["ls-files"], raiz)
    rutas = [r for r in salida.split("\n") if r.strip()]
    hallazgos: list[dict] = []
    leidos = 0
    for ruta in rutas:
        texto = _leer(raiz, ruta, desde_indice)
        if texto is None:
            continue
        leidos += 1
        if not solo_epilab:
            hallazgos.extend(buscar_rachas(texto, ruta))
            hallazgos.extend(buscar_kmeros_solapados(texto, ruta))
        if epilab:
            hallazgos.extend(buscar_epilab(texto, ruta, epilab[0], epilab[1]))
    return hallazgos, leidos


# --- Pasada 3: contra las secuencias confidenciales reales ------------------
# La pasada de rachas responde «hay nucleotidos publicados», que en este repositorio
# son decenas de miles y casi todos publicos (CDS de Tribolium castaneum desde el
# genoma de referencia, el genoma de MRFV por su accesion, los ARNdc de Cedden). La
# pregunta que la regla de CLAUDE.md hace es otra: «hay secuencias **de EPILAB**
# publicadas». Esta pasada la contesta, y por eso es la unica que distingue un
# hallazgo accionable de un dato publico.
#
# El archivo de referencia NO se versiona: vive en `YHat-Biotech/`, que esta en
# .gitignore. Si no esta, la pasada se declara no corrida en vez de dar un cero
# tranquilizador que en realidad significa «no mire».

RUTA_EPILAB = Path("YHat-Biotech/Sequences_EPILAB.xlsx")


def _revcomp(s: str) -> str:
    return s.translate(str.maketrans("ACGT", "TGCA"))[::-1]


def cargar_kmeros_epilab(raiz: Path) -> tuple[dict[str, str], dict[str, str]] | None:
    """Devuelve ({kmero: region}, {region: secuencia}), o None si no hay fuente local."""
    ruta = raiz / RUTA_EPILAB
    if not ruta.is_file():
        return None
    try:
        import openpyxl
    except ImportError:
        print("  aviso: falta openpyxl, la pasada contra EPILAB no se corre", file=sys.stderr)
        return None

    wb = openpyxl.load_workbook(ruta, data_only=True)
    kmeros: dict[str, str] = {}
    regiones: dict[str, str] = {}
    for ws in wb.worksheets:
        for fila in ws.iter_rows(values_only=True):
            celdas = [str(c) for c in fila if c is not None]
            for i, c in enumerate(celdas):
                s = re.sub(r"\s", "", c).upper()
                if len(s) < LARGO_RACHA or not set(s) <= set("ACGTUN"):
                    continue
                etiquetas = [
                    x.strip()
                    for j, x in enumerate(celdas)
                    if j != i and not set(re.sub(r"\s", "", x).upper()) <= set("ACGTUN")
                ]
                # Prefiere la etiqueta con forma de identificador de gen (`MP_MRFV`,
                # `BicC_Dm`, `ATPaseD_Dm`) sobre el nombre del organismo o del virus,
                # que en la planilla aparece en la misma fila y es menos especifico.
                nombre = next(
                    (e for e in etiquetas if re.fullmatch(r"[A-Za-z0-9]+_[A-Za-z0-9_]+", e)),
                    next((e for e in etiquetas if re.search(r"[A-Za-z]{3}", e)), "sin_nombre"),
                )[:40]
                s = s.replace("U", "T")
                regiones[nombre] = s
                for k in range(len(s) - LARGO_RACHA + 1):
                    km = s[k : k + LARGO_RACHA]
                    for var in (km, _revcomp(km)):
                        kmeros[var] = nombre
                        kmeros[var.replace("T", "U")] = nombre
    return (kmeros, regiones) if kmeros else None


def buscar_epilab(
    texto: str, ruta: str, kmeros: dict[str, str], regiones: dict[str, str]
) -> list[dict]:
    """Que regiones de EPILAB aparecen, cuantos nt de cada una y el tramo contiguo mayor.

    La cobertura es la cifra que decide: 25 ventanas sueltas no son lo mismo que una
    region entera, y «hay k-meros» no distingue los dos casos.
    """
    presentes: set[str] = set()
    for m in RE_RACHA.finditer(texto):
        t = m.group(0).upper().replace("U", "T")
        for i in range(len(t) - LARGO_RACHA + 1):
            km = t[i : i + LARGO_RACHA]
            if km in kmeros:
                presentes.add(km)
    if not presentes:
        return []

    hallazgos = []
    for nombre, seq in regiones.items():
        cubierto = [False] * len(seq)
        for i in range(len(seq) - LARGO_RACHA + 1):
            km = seq[i : i + LARGO_RACHA]
            if km in presentes or _revcomp(km) in presentes:
                for j in range(i, i + LARGO_RACHA):
                    cubierto[j] = True
        n = sum(cubierto)
        if not n:
            continue
        mayor = actual = 0
        for b in cubierto:
            actual = actual + 1 if b else 0
            mayor = max(mayor, actual)
        hallazgos.append(
            {
                "tipo": "kmero_de_epilab",
                "archivo": ruta,
                "region": nombre,
                "nt_cubiertos": n,
                "nt_region": len(seq),
                "pct_cubierto": round(100 * n / len(seq), 1),
                "tramo_contiguo_mayor": mayor,
            }
        )
    return hallazgos


def escanear_historial(
    raiz: Path, epilab: tuple[dict, dict] | None = None, solo_epilab: bool = False
) -> tuple[list[dict], int]:
    """Solo lineas agregadas (`+`) de todo el historial: un dato que estuvo sigue estando."""
    salida = _git(
        ["log", "--all", "--format=%x00commit %H", "-p", "--no-color", "--unified=0"], raiz
    )
    hallazgos: list[dict] = []
    commit = "?"
    archivo = "?"
    commits = set()
    for linea in salida.split("\n"):
        if linea.startswith("\x00commit "):
            commit = linea.split()[1][:10]
            commits.add(commit)
            continue
        if linea.startswith("+++ b/"):
            archivo = linea[6:]
            continue
        if not linea.startswith("+") or linea.startswith("+++"):
            continue
        if Path(archivo).suffix.lower() in EXT_BINARIAS:
            continue
        cuerpo = linea[1:]
        if epilab:
            for h in buscar_epilab(cuerpo, archivo, epilab[0], epilab[1]):
                h["tipo"] = "kmero_de_epilab_historial"
                h["commit"] = commit
                hallazgos.append(h)
        if solo_epilab:
            continue
        for m in RE_RACHA.finditer(cuerpo):
            tramo = m.group(0)
            if not _es_secuencia(tramo):
                continue
            hallazgos.append(
                {
                    "tipo": "racha_historial",
                    "commit": commit,
                    "archivo": archivo,
                    "largo_nt": len(tramo),
                    "huella": _huella(tramo),
                }
            )
    return hallazgos, len(commits)


# --- Informe ----------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--staged", action="store_true", help="solo el indice (gancho de pre-commit)")
    ap.add_argument("--historial", action="store_true", help="lineas agregadas en todo git log -p")
    ap.add_argument("--sin-excepciones", action="store_true", help="ignora la lista blanca")
    ap.add_argument(
        "--solo-epilab",
        action="store_true",
        help="solo la pasada contra las secuencias de EPILAB (la que distingue fuga de dato publico)",
    )
    ap.add_argument("--json", metavar="ARCHIVO", help="escribe el reporte completo en JSON")
    args = ap.parse_args()

    raiz = Path(
        _git(["rev-parse", "--show-toplevel"], Path(__file__).resolve().parent).strip()
        or Path(__file__).resolve().parents[2]
    )

    epilab = cargar_kmeros_epilab(raiz)
    if epilab is None:
        print(
            f"  aviso: {RUTA_EPILAB} no esta en disco; la pasada contra EPILAB NO se corrio.\n"
            "  Un cero en este modo no significa que no haya secuencias de EPILAB: significa"
            " que no se miro.",
            file=sys.stderr,
        )
        if args.solo_epilab:
            return 2
    else:
        print(f"  referencia EPILAB: {len(epilab[1])} regiones, {len(epilab[0])} 21-meros")

    if args.historial:
        hallazgos, n_unidades = escanear_historial(raiz, epilab, args.solo_epilab)
        unidad = f"{n_unidades} commits"
    else:
        hallazgos, n_unidades = escanear_arbol(
            raiz, args.staged, epilab, args.solo_epilab
        )
        unidad = f"{n_unidades} archivos de texto"

    for h in hallazgos:
        motivo = None if args.sin_excepciones else esta_exceptuada(h["archivo"])
        h["exceptuado"] = motivo is not None
        if motivo:
            h["motivo_excepcion"] = motivo

    vivos = [h for h in hallazgos if not h["exceptuado"]]
    exceptuados = len(hallazgos) - len(vivos)
    modo = "historial" if args.historial else ("indice" if args.staged else "arbol")
    print(f"sin_secuencias.py — modo {modo}, {unidad} revisados")
    print(f"  hallazgos: {len(vivos)} no exceptuados, {exceptuados} exceptuados")

    por_archivo: dict[str, list[dict]] = {}
    for h in vivos:
        por_archivo.setdefault(h["archivo"], []).append(h)

    # En el modo historial cada linea agregada se evalua por separado, asi que una
    # misma region aparece una vez por linea. Se agrega por commit, archivo y region y
    # se conserva la cobertura mayor, que es la cifra que interesa.
    agregados: dict[tuple, dict] = {}
    for h in vivos:
        if not h["tipo"].startswith("kmero_de_epilab"):
            continue
        clave = (h.get("commit"), h["archivo"], h["region"])
        previo = agregados.get(clave)
        if previo is None or h["nt_cubiertos"] > previo["nt_cubiertos"]:
            agregados[clave] = h
    epilab_vivos = list(agregados.values())
    if epilab_vivos:
        donde = "el historial" if modo == "historial" else "el arbol versionado"
        print(f"\n  SECUENCIAS DE EPILAB en {donde}:")
        for h in sorted(epilab_vivos, key=lambda x: -x["pct_cubierto"]):
            commit = f" [{h['commit']}]" if "commit" in h else ""
            print(
                f"    {h['archivo']}{commit}\n"
                f"      region {h['region']}: {h['nt_cubiertos']}/{h['nt_region']} nt"
                f" ({h['pct_cubierto']} %), tramo contiguo mayor {h['tramo_contiguo_mayor']} nt"
            )
        print()

    for ruta, hs in sorted(por_archivo.items(), key=lambda kv: -len(kv[1])):
        rachas = [h for h in hs if h["tipo"].startswith("racha")]
        kmeros = [h for h in hs if h["tipo"] == "kmeros_solapados"]
        detalle = []
        if rachas:
            largos = [h["largo_nt"] for h in rachas]
            detalle.append(f"{len(rachas)} rachas, {min(largos)}–{max(largos)} nt")
        if kmeros:
            peor = max(h["nt_reconstruidos"] for h in kmeros)
            detalle.append(
                f"{len(kmeros)} cadenas de k-meros solapados, hasta {peor} nt reconstruidos"
            )
        if detalle:
            print(f"  {ruta}: {'; '.join(detalle)}")

    if args.json:
        Path(args.json).write_text(
            json.dumps(
                {
                    "modo": modo,
                    "unidades_revisadas": n_unidades,
                    "largo_racha": LARGO_RACHA,
                    "no_exceptuados": len(vivos),
                    "exceptuados": exceptuados,
                    "hallazgos": hallazgos,
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"  reporte JSON: {args.json}")

    return 1 if vivos else 0


if __name__ == "__main__":
    sys.exit(main())
