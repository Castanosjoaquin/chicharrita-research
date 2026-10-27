#!/usr/bin/env python3
"""R8 paso 1 — ¿tiene ortólogo en el panel la quitinasa que impacta `eth_Dm` 193-392?

Qué contesta. `eth_Dm` 193-392 tiene una coincidencia perfecta de 21 nt en la posición 347
contra `LOC124369889` de *Homalodisca vitripennis*, anotado «probable chitinase 2» (M6,
firmado en D73). La firma declaró faltante un dato: si ese gen tiene ortólogo en las otras
cinco referencias del panel y con qué conservación, porque el tamizaje por coincidencia
exacta no ve un ortólogo que difiera en unos pocos nucleótidos y un ARNdc sí podría
silenciarlo.

Método, y por qué este y no otro. La búsqueda es de **homología**, no de coincidencia
exacta, así que no la cubre `offtarget_21nt.py` (Aho-Corasick es exacto por construcción).
Se hace **a nivel proteína**, por lo que midió `C5`: 77-84 % de identidad en nucleótido
contra 0,866 de mediana en proteína, porque el ADN codificante diverge en la tercera
posición del codón sin cambiar la proteína. Y se exige **ortología recíproca**, nunca el
gen con el mismo nombre: `C12` midió 78,2 % de concordancia sobre 1.152 pares recíprocos, y
el propio repositorio tiene medido que elegir por nombre mueve el conteo de ventanas
eficientes un 65 %.

  ida      `tblastn` de la proteína de la quitinasa contra cada referencia del panel.
  vuelta   del mejor acierto de cada referencia se extrae su ORF más largo y se lo
           devuelve con `tblastn` contra el transcriptoma de *H. vitripennis*; el par es
           recíproco sólo si vuelve a `LOC124369889`.

Las referencias se leen de disco y nada sale de la máquina. Ninguna salida versionada lleva
nucleótidos: este script emite identidades, coberturas y coordenadas, y las secuencias
quedan en `work/R8/`.

Uso (desde la raíz, con un entorno que tenga BLAST+ en el PATH):
    python3 research/ola6/R8_quitinasa_eth/scripts/01_ortologos.py
"""
from __future__ import annotations

import gzip
import json
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
TRABAJO = RAIZ / "work/R8"
SALIDA = Path(__file__).resolve().parents[1] / "resultados"

#: El panel de seis de `ranking.py`, con *D. maidis* fuera por ser el blanco.
PANEL = {
    "maiz": "GCF_902167145.1_Zm-B73-REFERENCE-NAM-5.0_rna.fna.gz",
    "H_axyridis": "GCF_914767665.1_icHarAxyr1.1_rna.fna.gz",
    "A_mellifera": "GCF_003254395.2_Amel_HAv3.1_rna.fna.gz",
    "H_vitripennis": "GCF_021130785.1_UT_GWSS_2.1_rna.fna.gz",
    "F_candida": "GCF_002217175.1_ASM221717v1_rna.fna.gz",
    "humano": "humano_rna.fna.gz",
}
ORIGEN = "H_vitripennis"          # la referencia de la que sale la consulta
LOCUS = "LOC124369889"
TRANSCRIPTOS = ("XM_046828031.1", "XM_046828033.1")
COLS = "qseqid sseqid pident length qstart qend sstart send evalue bitscore qcovs"

CODONES = {}
_B, _AA = "TCAG", "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
for _i, _b1 in enumerate(_B):
    for _j, _b2 in enumerate(_B):
        for _k, _b3 in enumerate(_B):
            CODONES[_b1 + _b2 + _b3] = _AA[_i * 16 + _j * 4 + _k]


def traducir(s: str) -> str:
    s = s.upper()
    return "".join(CODONES.get(s[i:i + 3], "X") for i in range(0, len(s) - 2, 3))


def orf_mas_largo(s: str) -> str:
    mejor = ""
    for f in range(3):
        for tramo in traducir(s[f:]).split("*"):
            if "M" in tramo:
                orf = tramo[tramo.index("M"):]
                if len(orf) > len(mejor):
                    mejor = orf
    return mejor


def leer_fasta(ruta: Path) -> dict[str, str]:
    abrir = gzip.open if ruta.suffix == ".gz" else open
    out, nombre, buf = {}, None, []
    with abrir(ruta, "rt") as fh:
        for l in fh:
            if l.startswith(">"):
                if nombre:
                    out[nombre] = "".join(buf)
                nombre, buf = l[1:].split()[0], []
            else:
                buf.append(l.strip())
    if nombre:
        out[nombre] = "".join(buf)
    return out


def descomprimir(gz: Path, destino: Path) -> Path:
    if not destino.exists():
        with gzip.open(gz, "rb") as a, open(destino, "wb") as b:
            shutil.copyfileobj(a, b)
    return destino


def tblastn(consulta: Path, sujeto: Path, max_hits: int = 20) -> list[dict]:
    r = subprocess.run(
        ["tblastn", "-query", str(consulta), "-subject", str(sujeto),
         "-outfmt", "6 " + COLS, "-evalue", "1e-5",
         "-max_hsps", "1", "-max_target_seqs", str(max_hits)],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("tblastn fallo: " + r.stderr[-2000:])
    campos = COLS.split()
    filas = []
    for linea in r.stdout.strip().splitlines():
        if not linea:
            continue
        d = dict(zip(campos, linea.split("\t")))
        for c in ("pident", "evalue", "bitscore"):
            d[c] = float(d[c])
        for c in ("length", "qstart", "qend", "sstart", "send", "qcovs"):
            d[c] = int(d[c])
        filas.append(d)
    return filas


def main() -> int:
    TRABAJO.mkdir(parents=True, exist_ok=True)
    SALIDA.mkdir(parents=True, exist_ok=True)
    ref = RAIZ / "work/W5/ref"
    db = TRABAJO / "db"
    db.mkdir(exist_ok=True)

    version = subprocess.run(["tblastn", "-version"], capture_output=True,
                             text=True).stdout.splitlines()[0].strip()
    print("herramienta:", version)

    consulta = TRABAJO / "quitinasa_prot.faa"
    if not consulta.exists():
        raise SystemExit("falta %s" % consulta)
    prot_consulta = leer_fasta(consulta)
    print("consulta: %d proteinas, la mas larga %d aa"
          % (len(prot_consulta), max(len(s) for s in prot_consulta.values())))

    # La referencia de origen se descomprime primero: la vuelta la necesita ya desde la
    # primera referencia del panel, y el orden del diccionario la deja para el final.
    plano_origen = descomprimir(ref / PANEL[ORIGEN],
                                db / PANEL[ORIGEN].replace(".gz", ""))

    filas_out, detalle = [], {}
    for corto, nombre in PANEL.items():
        plano = descomprimir(ref / nombre, db / nombre.replace(".gz", ""))
        hits = tblastn(consulta, plano)
        print("%-14s %4d aciertos" % (corto, len(hits)), flush=True)
        detalle[corto] = hits[:10]
        if not hits:
            filas_out.append({"referencia": corto, "archivo": nombre,
                              "tiene_ortologo": "no", "mejor_acierto": "",
                              "identidad_pct": "", "cobertura_consulta_pct": "",
                              "evalue": "", "reciproco": "", "nota":
                              "sin acierto de tblastn a e-value <= 1e-5"})
            continue
        mejor = max(hits, key=lambda h: h["bitscore"])
        fila = {"referencia": corto, "archivo": nombre, "tiene_ortologo": "",
                "mejor_acierto": mejor["sseqid"], "identidad_pct": round(mejor["pident"], 1),
                "cobertura_consulta_pct": mejor["qcovs"],
                "evalue": "%.1e" % mejor["evalue"], "reciproco": "", "nota": ""}

        # --- la vuelta: el mejor acierto se devuelve contra H. vitripennis
        if corto == ORIGEN:
            fila.update({"tiene_ortologo": "si (es la fuente)", "reciproco": "n/a",
                         "nota": "la consulta sale de esta referencia"})
        else:
            sec = leer_fasta(plano).get(mejor["sseqid"], "")
            orf = orf_mas_largo(sec)
            ida_vuelta = TRABAJO / ("vuelta_%s.faa" % corto)
            ida_vuelta.write_text(">%s_orf\n%s\n" % (mejor["sseqid"], orf))
            atras = tblastn(ida_vuelta, plano_origen)
            top = max(atras, key=lambda h: h["bitscore"])["sseqid"] if atras else ""
            recip = top in TRANSCRIPTOS
            fila["reciproco"] = "si" if recip else "no"
            fila["tiene_ortologo"] = "si" if recip else "no (acierto no reciproco)"
            fila["nota"] = ("la vuelta da %s" % top) if top else "la vuelta no dio acierto"
            fila["orf_vuelta_aa"] = len(orf)
        filas_out.append(fila)

    campos = ["referencia", "archivo", "tiene_ortologo", "mejor_acierto", "identidad_pct",
              "cobertura_consulta_pct", "evalue", "reciproco", "orf_vuelta_aa", "nota"]
    import csv
    with open(SALIDA / "ortologos_quitinasa.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(filas_out)
    (SALIDA / "ortologos_meta.json").write_text(json.dumps({
        "herramienta": version, "consulta_locus": LOCUS,
        "consulta_transcriptos": list(TRANSCRIPTOS),
        "criterio": "tblastn e-value <= 1e-5, mejor acierto por bitscore, "
                    "ortologia reciproca contra el transcriptoma de origen",
        "panel": PANEL, "aciertos_top10": detalle,
        "python": sys.version.split()[0],
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n%-14s %-22s %7s %7s %10s %s" % (
        "referencia", "mejor acierto", "ident%", "cob%", "reciproco", "ortologo"))
    for f in filas_out:
        print("%-14s %-22s %7s %7s %10s %s" % (
            f["referencia"], f["mejor_acierto"] or "-", f["identidad_pct"],
            f["cobertura_consulta_pct"], f["reciproco"], f["tiene_ortologo"]))
    print("\nescrito en %s" % SALIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
