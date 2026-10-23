"""Driver de la matriz de bases de M1: del FASTA al conteo por acierto, en un comando.

Por que existe. La primera mitad de M1 dejo la regla de conteo implementada
(`conteo_por_acierto.py`) pero la matriz sin correr, y los comandos para correrla
quedaron escritos a mano en el REPORT. Eso es justo lo que la seccion 8 del propio
REPORT se quejaba de la ola 3: los drivers de C2 viven en `work/` y no se pueden
releer desde el repositorio, asi que una medicion no se puede repetir sin
reconstruir los comandos. Este archivo es el driver, versionado.

Que hace, en cuatro pasos:

  1. **Port.** Corre `tools/sifi21_port/run_sifi.py --modo fiel --backend exe` sobre
     los cuatro FASTA de EPILAB y produce el TSV por ventana. El backend `exe` es el
     RNAplfold 2.1.5 del instalador de si-Fi2015 y es el unico verificado contra el
     programa original: 133, 32, 212 y 42 eficientes.
  2. **Ventanas.** Escribe el FASTA de ventanas de 21 nt con el nombre `w<pos>`, que
     es la convencion que `conteo_por_acierto.py` espera.
  3. **Bowtie.** Construye el indice de cada base y corre `bowtie -a -v 0`. Con
     `--mm 1` corre tambien `-a -v 1` como sensibilidad.
  4. **Conteo.** Aplica la regla del original y escribe `matriz.json` y `matriz.md`.

Que NO hace: no reimplementa el criterio de eficiencia (lo calcula el port), no
reimplementa Bowtie (lo invoca), y no inventa una base que no este en el disco. Una
base ausente se salta con un aviso y queda listada en el JSON bajo `bases_ausentes`,
porque una celda que no corrio y una celda que dio cero no son lo mismo.

Confidencialidad (CLAUDE.md). Los TSV por ventana y los FASTA de ventanas contienen
secuencias de EPILAB y por eso **todo lo que este script escribe va a `work/`**,
menos los dos archivos de resultados agregados, que son conteos. Bowtie y el port
corren localmente; el script no sube nada a ningun servicio.

Uso:
    python scripts/correr_matriz.py                      # matriz completa, -v 0
    python scripts/correr_matriz.py --mm 1               # agrega la corrida -v 1
    python scripts/correr_matriz.py --solo epilab4,gitv01_blancos
    python scripts/correr_matriz.py --orientacion        # control de orientacion
    python scripts/correr_matriz.py --saltear-port       # reusa los TSV ya escritos
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
M1 = Path(__file__).resolve().parent.parent
TRABAJO = RAIZ / "work" / "M1"

GENES = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]

# Donde busca el bowtie y el bowtie-build que trae el instalador de si-Fi2015. El
# primero que exista gana; `--bowtie DIR` lo sobrescribe. Se busca el del instalador
# y no uno del PATH a proposito: es el mismo binario con el que corrio el original.
CANDIDATOS_BOWTIE = [
    Path(os.environ.get("LOCALAPPDATA", "")) / "siFi2015" / "Bowtie",
    Path(r"C:\Program Files (x86)\siFi21\ToCopy\Bowtie"),
]

# Las bases de la matriz. `fuente` es de donde sale el FASTA: una ruta del corpus,
# un `.gz` de `work/offtarget_db/` que se descomprime, o una descarga publica por
# numero de acceso. Nada de esto manda una secuencia nuestra a ninguna parte: los
# accesos son identificadores publicos.
BASES = {
    "epilab4": {
        "fuente": ("copia", "work/sifi_check/epilab_4genes.fasta"),
        "genes": GENES,
        "que_es": "los cuatro genes de EPILAB: la celda de verificacion",
    },
    "mrfv_nc": {
        "fuente": ("copia", "work/sifi_check/NC_002786.2.fasta"),
        "genes": ["MP_MRFV", "CP_MRFV"],
        "que_es": "genoma de referencia de MRFV, aislamiento Costa Rican",
    },
    "mrfv_all": {
        "fuente": ("ncbi", "research/ola2/W5_secuencias_epilab/analisis/"
                            "mrfv_conservacion_aislados.txt"),
        "genes": ["MP_MRFV", "CP_MRFV"],
        "que_es": "los registros publicos de MRFV de GenBank analizados en W5",
    },
    "gitv01_blancos": {
        "fuente": ("ncbi_fijo", ["GITV01000968.1", "GITV01001458.1"]),
        "genes": ["BicC_Dm", "ATPaseD_Dm"],
        "que_es": "los dos contigs del transcriptoma publico de D. maidis (TSA "
                  "GITV01) que la ola 3 identifico como blanco principal",
    },
    "dmaid_genoma": {
        "fuente": ("gz", "work/offtarget_db/GCA_975739785.1_ihDalMaid1.1_genomic.fna.gz"),
        "genes": GENES,
        "que_es": "genoma de Dalbulus maidis GCA_975739785.1",
    },
    "hvitri": {
        "fuente": ("gz", "work/offtarget_db/GCF_021130785.1_UT_GWSS_2.1_rna.fna.gz"),
        "genes": GENES,
        "que_es": "transcriptoma de Homalodisca vitripennis GCF_021130785.1",
    },
    "zmays": {
        "fuente": ("gz", "work/offtarget_db/"
                         "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna.fna.gz"),
        "genes": GENES,
        "que_es": "transcriptoma de maiz GCF_902167145.1",
    },
    "amel": {
        "fuente": ("gz", "work/offtarget_db/GCF_003254395.2_Amel_HAv3.1_rna.fna.gz"),
        "genes": GENES,
        "que_es": "transcriptoma de Apis mellifera GCF_003254395.2",
    },
    "haxyr": {
        "fuente": ("gz", "work/offtarget_db/GCF_914767665.1_icHarAxyr1.1_rna.fna.gz"),
        "genes": GENES,
        "que_es": "transcriptoma de Harmonia axyridis GCF_914767665.1",
    },
    "fcandida": {
        "fuente": ("gz", "work/offtarget_db/GCF_002217175.1_ASM221717v1_rna.fna.gz"),
        "genes": GENES,
        # Ojo: el plan de la ola 4 y el issue #5 llaman a este acceso «transcriptoma
        # de D. maidis», y no lo es. La cabecera del propio archivo dice Folsomia
        # candida. El transcriptoma de D. maidis no esta en `work/offtarget_db/`.
        "que_es": "transcriptoma de Folsomia candida GCF_002217175.1 (NO es "
                  "D. maidis, contra lo que dice el plan)",
    },
}

EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def paso(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def correr(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run([str(c) for c in cmd], check=True, text=True,
                          capture_output=True, **kw)


def hallar_bowtie(forzado: str | None) -> Path:
    for d in ([Path(forzado)] if forzado else CANDIDATOS_BOWTIE):
        if (d / "bowtie.exe").exists() or (d / "bowtie").exists():
            return d
    raise SystemExit(
        "no se encontro bowtie. Se busco en:\n  " +
        "\n  ".join(str(d) for d in CANDIDATOS_BOWTIE) +
        "\nPasa --bowtie DIR con el directorio que tenga bowtie y bowtie-build.")


def exe(dir_bowtie: Path, nombre: str) -> Path:
    for cand in (dir_bowtie / f"{nombre}.exe", dir_bowtie / nombre):
        if cand.exists():
            return cand
    raise SystemExit(f"falta {nombre} en {dir_bowtie}")


def version_bowtie(dir_bowtie: Path) -> str:
    try:
        salida = subprocess.run([str(exe(dir_bowtie, "bowtie")), "--version"],
                                text=True, capture_output=True).stdout
        return salida.splitlines()[0].strip() if salida else "desconocida"
    except Exception as err:                                  # pragma: no cover
        return f"desconocida ({err})"


# --- Paso 1 y 2: port y ventanas -------------------------------------------

def correr_port(modo: str, backend: str, fastas: list[Path], destino: Path) -> None:
    destino.mkdir(parents=True, exist_ok=True)
    # `--con-seq` es necesario: esta linea arma las consultas de Bowtie con el 21-mero de
    # cada ventana, y desde la linea M3 (issue #7) el port no emite la columna `seq` por
    # defecto, porque sobre ventanas solapadas de a 1 nt reconstruye el gen entero. El TSV
    # que sale de aca es de trabajo y **no se versiona**: vive bajo `work/`.
    cmd = [sys.executable, "-I", RAIZ / "tools" / "sifi21_port" / "run_sifi.py",
           *fastas, "--modo", modo, "--backend", backend, "--salida", destino,
           "--con-seq"]
    paso(f"port: {modo}/{backend} sobre {len(fastas)} FASTA -> {destino}")
    res = correr(cmd, cwd=RAIZ)
    for linea in res.stdout.splitlines():
        if "eficientes:" in linea or linea.startswith("=="):
            print("   " + linea.strip())


def tsv_del_gen(dir_port: Path, gen: str, sufijo: str) -> Path:
    """El TSV que escribe el port: `<nombre del registro>_<modo>_<backend>.tsv`."""
    cands = sorted(dir_port.glob(f"{gen}_*{sufijo}.tsv"))
    if not cands:
        raise SystemExit(f"no hay TSV de {gen} en {dir_port} (sufijo {sufijo})")
    return cands[0]


def escribir_ventanas(tsv: Path, salida: Path) -> None:
    correr([sys.executable, "-I", M1 / "scripts" / "conteo_por_acierto.py", "ventanas",
            "--tsv", tsv, "--salida", salida], cwd=RAIZ)


# --- Paso 3: las bases y Bowtie --------------------------------------------

def materializar(nombre: str, spec: dict, destino: Path) -> Path | None:
    """Deja el FASTA de la base en el disco y devuelve su ruta, o None si no se puede."""
    destino.mkdir(parents=True, exist_ok=True)
    fa = destino / f"{nombre}.fa"
    if fa.exists() and fa.stat().st_size > 0:
        return fa
    clase, arg = spec["fuente"]

    if clase == "copia":
        origen = RAIZ / arg
        if not origen.exists():
            return None
        shutil.copyfile(origen, fa)
        return fa

    if clase == "gz":
        import gzip
        origen = RAIZ / arg
        if not origen.exists():
            return None
        paso(f"descomprimiendo {origen.name}")
        with gzip.open(origen, "rb") as src, open(fa, "wb") as dst:
            shutil.copyfileobj(src, dst, length=1 << 22)
        return fa

    if clase in ("ncbi", "ncbi_fijo"):
        if clase == "ncbi_fijo":
            accesos = list(arg)
        else:
            import re
            texto = (RAIZ / arg)
            if not texto.exists():
                return None
            accesos = sorted(set(re.findall(
                r"\b[A-Z]{1,2}_?[0-9]{5,6}\.[0-9]+\b", texto.read_text(encoding="utf-8",
                                                                       errors="replace"))))
        if not accesos:
            return None
        # Solo salen numeros de acceso publicos. Ninguna secuencia nuestra viaja.
        paso(f"bajando {len(accesos)} registros publicos de NCBI para {nombre}")
        from urllib.parse import urlencode
        from urllib.request import urlopen
        url = EFETCH + "?" + urlencode({"db": "nuccore", "rettype": "fasta",
                                        "retmode": "text", "id": ",".join(accesos)})
        with urlopen(url, timeout=180) as resp:
            datos = resp.read()
        if not datos.startswith(b">"):
            print(f"   aviso: NCBI no devolvio un FASTA para {nombre}", file=sys.stderr)
            return None
        fa.write_bytes(datos)
        return fa

    raise SystemExit(f"fuente desconocida para {nombre}: {clase}")


def indexar(dir_bowtie: Path, fa: Path, indice: Path) -> bool:
    if (indice.with_suffix(".rev.2.ebwt")).exists():
        return True
    indice.parent.mkdir(parents=True, exist_ok=True)
    paso(f"indexando {fa.name} ({fa.stat().st_size // (1 << 20)} MB)")
    try:
        correr([exe(dir_bowtie, "bowtie-build"), "-q", fa, indice])
    except subprocess.CalledProcessError as err:
        print(f"   FALLO bowtie-build en {fa.name}: "
              f"{(err.stderr or '').strip()[:300]}", file=sys.stderr)
        return False
    return True


def alinear(dir_bowtie: Path, indice: Path, ventanas: Path, salida: Path,
            mm: int) -> int | None:
    """Corre `bowtie -a -v <mm>`. Devuelve el numero de aciertos, o None si fallo.

    bowtie 0.11.3 es el binario de 32 bits del instalador de si-Fi2015 y con
    `-v 1` sobre un indice del tamano de un genoma aborta con «Error reading
    _rstarts[] array». Eso se informa como fallo de la celda y no como cero.
    """
    salida.parent.mkdir(parents=True, exist_ok=True)
    try:
        res = subprocess.run(
            [str(exe(dir_bowtie, "bowtie")), "-a", "-v", str(mm), "-f",
             str(indice), str(ventanas)],
            text=True, capture_output=True)
    except OSError as err:                                    # pragma: no cover
        print(f"   FALLO bowtie: {err}", file=sys.stderr)
        return None
    err = (res.stderr or "")
    if res.returncode != 0 or "Error reading" in err:
        print(f"   FALLO bowtie -v {mm} en {indice.name}: "
              f"{err.strip().splitlines()[0][:200] if err.strip() else res.returncode}",
              file=sys.stderr)
        # Una celda que fallo no deja archivo. Si quedara uno vacio de un intento
        # anterior, el paso de conteo lo leeria como «cero aciertos» y una celda
        # fallida pasaria por un nulo medido, que es justo la confusion que esta
        # linea vino a evitar. Un archivo vacio escrito por este script significa,
        # siempre, que Bowtie corrio bien y no encontro nada.
        salida.unlink(missing_ok=True)
        return None
    salida.write_text(res.stdout, encoding="utf-8", newline="\n")
    return sum(1 for linea in res.stdout.splitlines() if linea.strip())


# --- Orquestacion ----------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bowtie", default=None, help="directorio con bowtie y bowtie-build")
    ap.add_argument("--mm", type=int, default=0, choices=(0, 1),
                    help="0 corre solo -v 0; 1 corre -v 0 y ademas -v 1")
    ap.add_argument("--solo", default=None, help="lista de bases separadas por coma")
    ap.add_argument("--orientacion", action="store_true",
                    help="control de orientacion: el complemento reverso de cada gen")
    ap.add_argument("--saltear-port", action="store_true",
                    help="reusa los TSV por ventana que ya esten escritos")
    a = ap.parse_args(argv)

    dir_bowtie = hallar_bowtie(a.bowtie)
    paso(f"bowtie en {dir_bowtie}: {version_bowtie(dir_bowtie)}")

    sufijo = "fiel_exe"
    if a.orientacion:
        return orientacion(dir_bowtie, a, sufijo)

    dir_port = TRABAJO / "port_fiel"
    if not a.saltear_port:
        fastas = [RAIZ / "work" / "sifi_check" / f"{g}_full.fasta" for g in GENES]
        faltan = [f for f in fastas if not f.exists()]
        if faltan:
            raise SystemExit(
                "faltan FASTA del corpus en work/sifi_check/:\n  " +
                "\n  ".join(f.name for f in faltan) +
                "\nEsas secuencias no estan en git (regla de confidencialidad): "
                "las pasa el equipo a mano.")
        correr_port("fiel", "exe", fastas, dir_port)

    tsv = {g: tsv_del_gen(dir_port, g, sufijo) for g in GENES}
    dir_vent = TRABAJO / "ventanas"
    for g in GENES:
        escribir_ventanas(tsv[g], dir_vent / f"{g}.fasta")
    paso(f"ventanas escritas en {dir_vent}")

    pedidas = set(a.solo.split(",")) if a.solo else set(BASES)
    desconocidas = pedidas - set(BASES)
    if desconocidas:
        raise SystemExit(f"bases desconocidas: {sorted(desconocidas)}")

    ausentes, aciertos, fallidas = {}, {}, {}
    for nombre in BASES:
        if nombre not in pedidas:
            continue
        spec = BASES[nombre]
        fa = materializar(nombre, spec, TRABAJO / "bases")
        if fa is None:
            ausentes[nombre] = spec["fuente"][1] if isinstance(spec["fuente"][1], str) \
                else ", ".join(spec["fuente"][1])
            print(f"   AUSENTE {nombre}: no esta el insumo", file=sys.stderr)
            continue
        indice = TRABAJO / "indices" / nombre
        if not indexar(dir_bowtie, fa, indice):
            fallidas[f"{nombre}:indice"] = "bowtie-build fallo"
            continue
        for mm in ([0, 1] if a.mm == 1 else [0]):
            destino = TRABAJO / ("hits" if mm == 0 else "hits_mm1")
            for g in spec["genes"]:
                salida = destino / f"{nombre}_{g}.txt"
                n = alinear(dir_bowtie, indice, dir_vent / f"{g}.fasta", salida, mm)
                if n is None:
                    fallidas[f"{nombre}:{g}:mm{mm}"] = f"bowtie -v {mm} abortó"
                else:
                    aciertos[f"mm{mm}:{nombre}:{g}"] = n
                    paso(f"  {nombre}/{g} -v {mm}: {n} aciertos")

    for mm in ([0, 1] if a.mm == 1 else [0]):
        contar(tsv, TRABAJO / ("hits" if mm == 0 else "hits_mm1"), pedidas, mm)

    prov = {
        "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
        "bowtie": version_bowtie(dir_bowtie),
        "dir_bowtie": str(dir_bowtie),
        "python": sys.version.split()[0],
        "port": "fiel/exe (RNAplfold 2.1.5 del instalador de si-Fi2015)",
        "bases_corridas": sorted(set(n for n in pedidas if n not in ausentes)),
        "bases_ausentes": ausentes,
        "celdas_fallidas": fallidas,
        "aciertos_crudos": aciertos,
        "que_es_cada_base": {n: BASES[n]["que_es"] for n in sorted(pedidas)},
    }
    (M1 / "resultados" / "procedencia.json").write_text(
        json.dumps(prov, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    paso("procedencia -> resultados/procedencia.json")
    if ausentes:
        print("\nBases que no corrieron por falta de insumo:", file=sys.stderr)
        for n, d in ausentes.items():
            print(f"  {n}: {d}", file=sys.stderr)
    return 0


def contar(tsv: dict[str, Path], dir_hits: Path, pedidas: set[str], mm: int) -> None:
    """Llama a `conteo_por_acierto.py contar` con todas las celdas que existan."""
    cmd = [sys.executable, "-I", M1 / "scripts" / "conteo_por_acierto.py", "contar"]
    for g in GENES:
        cmd += ["--gen", f"{g}={tsv[g]}"]
    celdas = 0
    for nombre in BASES:
        if nombre not in pedidas:
            continue
        for g in BASES[nombre]["genes"]:
            ruta = dir_hits / f"{nombre}_{g}.txt"
            if ruta.exists():
                cmd += ["--aciertos", f"{nombre}:{g}={ruta}"]
                celdas += 1
    if not celdas:
        print(f"no hay celdas para mm{mm}", file=sys.stderr)
        return
    sufijo = "" if mm == 0 else "_mm1"
    if "epilab4" in pedidas and (dir_hits / "epilab4_BicC_Dm.txt").exists():
        cmd += ["--exigir-identidad", "epilab4"]
    cmd += ["--json", M1 / "resultados" / f"matriz{sufijo}.json",
            "--md", M1 / "resultados" / f"matriz{sufijo}.md"]
    paso(f"contando {celdas} celdas (mm{mm})")
    res = subprocess.run([str(c) for c in cmd], text=True, capture_output=True, cwd=RAIZ)
    if res.stderr.strip():
        print(res.stderr.strip(), file=sys.stderr)
    print(res.stdout)


def orientacion(dir_bowtie: Path, a, sufijo: str) -> int:
    """El control de orientacion: revcomp del gen, motor de nuevo, y contar.

    El complemento reverso cambia **las ventanas**, no solo los aciertos, asi que no
    alcanza con dar vuelta la referencia: hay que volver a correr el motor de
    eficiencia sobre el gen invertido. Eso es el costo real de este control.
    """
    dir_rc = TRABAJO / "revcomp"
    for g in GENES:
        origen = RAIZ / "work" / "sifi_check" / f"{g}_full.fasta"
        if not origen.exists():
            raise SystemExit(f"falta {origen}")
        correr([sys.executable, "-I", M1 / "scripts" / "conteo_por_acierto.py", "revcomp",
                "--fasta", origen, "--salida", dir_rc / f"{g}_full.fasta"], cwd=RAIZ)
    paso(f"complemento reverso -> {dir_rc}")

    dir_port = TRABAJO / "port_revcomp"
    if not a.saltear_port:
        correr_port("fiel", "exe", sorted(dir_rc.glob("*.fasta")), dir_port)

    tsv = {g: tsv_del_gen(dir_port, g, sufijo) for g in GENES}
    dir_vent = TRABAJO / "ventanas_rc"
    for g in GENES:
        escribir_ventanas(tsv[g], dir_vent / f"{g}.fasta")

    fa = TRABAJO / "bases" / "epilab4_rc.fa"
    fa.parent.mkdir(parents=True, exist_ok=True)
    fa.write_text("".join((dir_rc / f"{g}_full.fasta").read_text(encoding="utf-8")
                          for g in GENES), encoding="utf-8")
    indice = TRABAJO / "indices" / "epilab4_rc"
    if not indexar(dir_bowtie, fa, indice):
        raise SystemExit("no se pudo indexar el revcomp")

    cmd = [sys.executable, "-I", M1 / "scripts" / "conteo_por_acierto.py", "contar"]
    for g in GENES:
        salida = TRABAJO / "hits_rc" / f"epilab4_rc_{g}.txt"
        n = alinear(dir_bowtie, indice, dir_vent / f"{g}.fasta", salida, 0)
        paso(f"  epilab4_rc/{g}: {n} aciertos")
        cmd += ["--gen", f"{g}={tsv[g]}", "--aciertos", f"epilab4_rc:{g}={salida}"]
    cmd += ["--exigir-identidad", "epilab4_rc",
            "--json", M1 / "resultados" / "orientacion.json",
            "--md", M1 / "resultados" / "orientacion.md"]
    res = subprocess.run([str(c) for c in cmd], text=True, capture_output=True, cwd=RAIZ)
    if res.stderr.strip():
        print(res.stderr.strip(), file=sys.stderr)
    print(res.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
