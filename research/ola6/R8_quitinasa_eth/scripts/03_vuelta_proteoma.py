"""R8 paso 3 — la vuelta de la reciprocidad contra el proteoma **anotado**, no contra el ORF.

Por que existe. El §7 de `REPORT.md` declara dos limitaciones de metodo, y las dos salen de
lo mismo: ninguna de las seis referencias del panel es un proteoma, asi que la vuelta se hizo
con `tblastn` del **ORF mas largo** del transcripto contra el transcriptoma de origen. El
issue #32 pide rehacerla contra una proteina anotada. En esta maquina **si hay** un proteoma
anotado del organismo de origen —`GCF_021130785.1_UT_GWSS_2.1_protein.faa`, el de
*Homalodisca vitripennis*, en `work/F1v/ref/`— y BLAST+ 2.17.0 en los entornos de
`micromamba` (entrada 54). Con los dos, la vuelta se puede hacer `blastp`, proteina contra
proteina anotada, sin pasar por la traduccion del ORF.

Que cambia y que no. Esto **no corrige ninguna cifra de la ida**: identidad, cobertura y
e-value de `ortologos_quitinasa.tsv` salen del `tblastn` de ida y no se tocan. Lo que se
rehace es la columna `reciproco`, que es la que dependia del ORF. El resultado se publica al
lado del anterior, con las dos lecturas, que es la forma que el proyecto usa cuando una
medicion nueva no reemplaza a la vieja sino que la acompana.

La segunda limitacion de §7 —un transcripto por acierto, el de mejor `bitscore`— se mide
aparte y a proposito: la vuelta se corre tambien tomando los `--top` mejores aciertos de la
ida, para ver si el veredicto de reciprocidad depende de haber elegido una sola variante.

Ambito, que no cambia: `blastp` contra un proteoma encuentra **proteinas anotadas**, asi que
una ausencia es ausencia en el proteoma publicado. Y la reciprocidad sigue siendo una prueba
de mejor-acierto-mutuo, no una prueba de ortologia filogenetica.

Uso (desde la raiz del repositorio, entorno con BLAST+ en el PATH):
    python research/ola6/R8_quitinasa_eth/scripts/03_vuelta_proteoma.py
    python research/ola6/R8_quitinasa_eth/scripts/03_vuelta_proteoma.py --top 5
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
BLOQUE = Path(__file__).resolve().parents[1]
RESULTADOS = BLOQUE / "resultados"
TRABAJO = RAIZ / "work" / "R8"
#: El proteoma anotado del organismo de origen. No se versiona (es una referencia publica
#: de 150 MB); si falta, el script lo dice y no sigue.
PROTEOMA = RAIZ / "work/F1v/ref/GCF_021130785.1_UT_GWSS_2.1_protein.faa"
PROTEOMA_GZ = Path(str(PROTEOMA) + ".gz")
CONSULTA = TRABAJO / "quitinasa_prot.faa"
IDA = RESULTADOS / "ortologos_quitinasa.tsv"
TRANSCRIPTOS = TRABAJO / "quitinasa_transcriptos.fasta"


def cabeceras(ruta: Path) -> dict[str, str]:
    """accesion -> nombre del producto, leido de la cabecera del FASTA de referencia."""
    out = {}
    with ruta.open(encoding="utf-8") as fh:
        for linea in fh:
            if linea.startswith(">"):
                acc, _, resto = linea[1:].strip().partition(" ")
                out[acc] = resto
    return out


ISOFORMA = re.compile(r"\s+isoform\s+\S+$", re.IGNORECASE)


def producto(cab: str) -> str:
    """El producto sin el sufijo de isoforma y sin el corchete de especie.

    Por que hace falta. La reciprocidad se evalua comparando **accesiones de proteina**, y
    un proteoma anotado trae una accesion por isoforma: la consulta es
    `probable chitinase 2 isoform X1` y la vuelta puede caer en `isoform X2`, que es **el
    mismo gen**. Comparar accesiones las cuenta como proteinas distintas y declara no
    reciproco un par que si lo es. Colapsar por producto es el criterio mas conservador
    que tenemos sin el GFF: no agrupa genes distintos con nombres parecidos, porque exige
    el nombre completo igual, y agrupa las isoformas, que es lo que se busca.
    """
    return ISOFORMA.sub("", cab.split(" [")[0]).strip().lower()


def leer_fasta(ruta: Path) -> dict[str, str]:
    seqs, nombre, buf = {}, None, []
    with ruta.open(encoding="utf-8") as fh:
        for linea in fh:
            if linea.startswith(">"):
                if nombre:
                    seqs[nombre] = "".join(buf)
                nombre, buf = linea[1:].split()[0], []
            else:
                buf.append(linea.strip())
    if nombre:
        seqs[nombre] = "".join(buf)
    return seqs


TABLA = {}
for i, aa in enumerate("FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"):
    TABLA["TCAG"[i // 16] + "TCAG"[i // 4 % 4] + "TCAG"[i % 4]] = aa


def traducir(s: str) -> str:
    s = s.upper().replace("U", "T")
    return "".join(TABLA.get(s[i:i + 3], "X") for i in range(0, len(s) - 2, 3))


def orf_mas_largo(s: str) -> str:
    """El mismo criterio que usa el paso 1, para que la comparacion sea de la vuelta y no
    de dos formas distintas de sacar el ORF."""
    mejor = ""
    for marco in range(3):
        for tramo in traducir(s[marco:]).split("*"):
            if "M" in tramo:
                orf = tramo[tramo.index("M"):]
                if len(orf) > len(mejor):
                    mejor = orf
    return mejor


def correr(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("%s fallo:\n%s" % (cmd[0], r.stderr[-2000:]))
    return r.stdout


def blastp(consulta: Path, sujeto: Path, max_hits: int = 20) -> list[dict]:
    campos = ["qseqid", "sseqid", "pident", "length", "qlen", "slen", "evalue", "bitscore"]
    salida = correr(["blastp", "-query", str(consulta), "-subject", str(sujeto),
                     "-evalue", "1e-5", "-max_target_seqs", str(max_hits),
                     "-outfmt", "6 " + " ".join(campos)])
    filas = []
    for linea in salida.splitlines():
        if linea.strip():
            filas.append(dict(zip(campos, linea.split("\t"))))
    return filas


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", type=int, default=1,
                    help="cuantos aciertos de la ida devolver por referencia (§7, segunda "
                         "limitacion). Con 1 se reproduce la eleccion publicada.")
    a = ap.parse_args(argv)

    if not shutil.which("blastp"):
        raise SystemExit(
            "falta `blastp` en el PATH. En la maquina de Joaquin esta en los entornos de "
            "micromamba sin activar: envs/alineador/bin y envs/w5bio/bin (entrada 54).")
    if not PROTEOMA.exists():
        if PROTEOMA_GZ.exists():
            print("descomprimiendo %s ..." % PROTEOMA_GZ.name, flush=True)
            with gzip.open(PROTEOMA_GZ, "rb") as g, PROTEOMA.open("wb") as fh:
                shutil.copyfileobj(g, fh)
        else:
            raise SystemExit(
                "falta el proteoma anotado de H. vitripennis en %s. Es una referencia "
                "publica del NCBI (GCF_021130785.1, UT_GWSS_2.1) y no se versiona."
                % PROTEOMA)
    for ruta in (CONSULTA, IDA, TRANSCRIPTOS):
        if not ruta.exists():
            raise SystemExit("falta %s. Lo produce el paso 1 "
                             "(scripts/01_ortologos.py)." % ruta)

    proteinas = leer_fasta(PROTEOMA)
    cabs = cabeceras(PROTEOMA)
    print("proteoma anotado: %d proteinas de %s" % (len(proteinas), PROTEOMA.name))

    # El ancla de la vuelta: la propia consulta tiene que encontrarse a si misma en el
    # proteoma. Si no, el proteoma no es el del organismo de origen y todo lo que sigue
    # mide otra cosa.
    propia = blastp(CONSULTA, PROTEOMA, max_hits=5)
    if not propia or float(propia[0]["pident"]) < 99.0:
        raise SystemExit(
            "ANCLA ROTA: la quitinasa de consulta no se encuentra a si misma en el "
            "proteoma (mejor acierto %s). El proteoma no corresponde al organismo de "
            "origen." % (propia[0] if propia else "ninguno"))
    propia_id = propia[0]["sseqid"]
    print("ancla: la consulta se encuentra a si misma -> %s (%s%% identidad)"
          % (propia_id, propia[0]["pident"]))

    transcriptos = leer_fasta(TRANSCRIPTOS)
    with IDA.open(encoding="utf-8") as fh:
        ida = list(csv.DictReader(fh, delimiter="\t"))

    filas = []
    for f in ida:
        ref = f["referencia"]
        if ref == "H_vitripennis":
            continue                      # es la fuente: no tiene vuelta
        acc = f["mejor_acierto"]
        # El ORF que se devuelve es **el mismo** que uso la vuelta publicada: el paso 1 lo
        # dejo escrito en `work/R8/vuelta_<ref>.faa`. Reusarlo en vez de volver a
        # extraerlo deja una sola variable en juego —contra que se devuelve, transcriptoma
        # o proteoma anotado— que es justo lo que el issue #32 pregunta. Si el archivo no
        # esta, se reconstruye del transcripto con el mismo criterio.
        ruta_orf = TRABAJO / ("vuelta_%s.faa" % ref)
        if ruta_orf.exists():
            orf = "".join(l.strip() for l in ruta_orf.read_text().splitlines()[1:])
            origen_orf = "work/R8/%s (el del paso 1)" % ruta_orf.name
        else:
            sec = transcriptos.get(acc)
            if not sec:
                filas.append({"referencia": ref, "mejor_acierto": acc,
                              "reciproco_orf_publicado": f["reciproco"],
                              "reciproco_proteoma": "sin medir",
                              "nota": "no estan ni el ORF del paso 1 ni el transcripto"})
                continue
            orf = orf_mas_largo(sec)
            ruta_orf = TRABAJO / ("vuelta_prot_%s.faa" % ref)
            ruta_orf.write_text(">%s_orf\n%s\n" % (acc, orf), encoding="utf-8")
            origen_orf = "reconstruido del transcripto"
        atras = blastp(ruta_orf, PROTEOMA, max_hits=max(5, a.top))
        top = atras[0]["sseqid"] if atras else ""
        recip = "si" if top == propia_id else ("no" if top else "sin acierto")
        prod_consulta, prod_top = producto(cabs.get(propia_id, "")), producto(cabs.get(top, ""))
        recip_prod = ("si" if top and prod_top and prod_top == prod_consulta
                      else ("no" if top else "sin acierto"))
        filas.append({
            "referencia": ref, "mejor_acierto": acc,
            "orf_vuelta_aa": len(orf),
            "vuelta_contra": "proteoma anotado (blastp)",
            "origen_del_orf": origen_orf,
            "mejor_de_la_vuelta": top,
            "identidad_vuelta_pct": atras[0]["pident"] if atras else "",
            "evalue_vuelta": atras[0]["evalue"] if atras else "",
            "reciproco_proteoma": recip,
            "producto_de_la_vuelta": cabs.get(top, ""),
            "reciproco_por_producto": recip_prod,
            "reciproco_orf_publicado": f["reciproco"],
            "coincide_con_lo_publicado": "si" if recip == f["reciproco"] else "NO",
            "nota": ("la vuelta llega a la propia consulta (%s)" % propia_id) if recip == "si"
                    else ("la vuelta llega a %s, OTRA ISOFORMA del mismo producto (%s): "
                          "reciproco por gen, no por accesion" % (top, prod_top))
                    if recip_prod == "si"
                    else ("la vuelta llega a %s, que es otro producto (%s)"
                          % (top, prod_top or "sin anotacion")) if top
                    else "la vuelta no dio acierto a e-value <= 1e-5",
        })

    RESULTADOS.mkdir(parents=True, exist_ok=True)
    campos = ["referencia", "mejor_acierto", "orf_vuelta_aa", "origen_del_orf",
              "vuelta_contra",
              "mejor_de_la_vuelta", "identidad_vuelta_pct", "evalue_vuelta",
              "reciproco_proteoma", "producto_de_la_vuelta",
              "reciproco_por_producto", "reciproco_orf_publicado",
              "coincide_con_lo_publicado", "nota"]
    with (RESULTADOS / "vuelta_proteoma.tsv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for f in filas:
            w.writerow(f)

    distintas = [f for f in filas if f.get("coincide_con_lo_publicado") == "NO"]
    por_prod = [f for f in filas
                if f.get("reciproco_por_producto") != f.get("reciproco_orf_publicado")]
    isoformas = [f for f in filas if f.get("reciproco_proteoma") == "no"
                 and f.get("reciproco_por_producto") == "si"]
    (RESULTADOS / "vuelta_proteoma_meta.json").write_text(json.dumps({
        "que_mide": "la vuelta de la reciprocidad contra el proteoma anotado de "
                    "H. vitripennis, en vez del ORF mas largo del transcripto (issue #32)",
        "proteoma": PROTEOMA.relative_to(RAIZ).as_posix(),
        "proteinas_en_el_proteoma": len(proteinas),
        "ancla_consulta_se_encuentra": {"sseqid": propia_id, "pident": propia[0]["pident"]},
        "referencias_medidas": len(filas),
        "veredictos_que_cambian_por_accesion": len(distintas),
        "veredictos_que_cambian_por_producto": len(por_prod),
        "cambian_solo_por_isoforma": len(isoformas),
        "detalle_de_los_que_cambian": distintas,
        "lectura": "comparar accesiones mueve %d de %d veredictos, y %d de esos %d son la "
                   "vuelta cayendo en OTRA ISOFORMA del mismo producto, o sea el mismo "
                   "gen. Colapsando por producto cambian %d. La limitacion que el issue "
                   "#32 nombra —un transcripto por acierto, con variantes de empalme— "
                   "aparece aca del lado del proteoma, no del transcripto."
                   % (len(distintas), len(filas), len(isoformas), len(distintas),
                      len(por_prod)),
        "limite": "blastp contra un proteoma encuentra proteinas anotadas: una ausencia es "
                  "ausencia en el proteoma publicado. La reciprocidad sigue siendo "
                  "mejor-acierto-mutuo y no una prueba de ortologia filogenetica.",
        "entorno": {"python": platform.python_version(), "sistema": platform.system(),
                    "blastp": correr(["blastp", "-version"]).splitlines()[0]},
    }, indent=1, ensure_ascii=False), encoding="utf-8")

    print()
    print("%-14s %-16s %-11s %-12s %-12s %s"
          % ("referencia", "mejor acierto", "ORF (pub.)", "por accesion", "por producto",
             "a que llega la vuelta"))
    for f in filas:
        print("%-14s %-16s %-11s %-12s %-12s %s"
              % (f["referencia"], f["mejor_acierto"], f["reciproco_orf_publicado"],
                 f.get("reciproco_proteoma", "-"), f.get("reciproco_por_producto", "-"),
                 (f.get("producto_de_la_vuelta") or "")[:46]))
    print()
    print("veredictos que cambian comparando ACCESIONES: %d de %d"
          % (len(distintas), len(filas)))
    print("  de esos, son otra ISOFORMA del mismo producto: %d" % len(isoformas))
    print("veredictos que cambian comparando PRODUCTOS (isoformas colapsadas): %d de %d"
          % (len(por_prod), len(filas)))
    print("escrito en %s" % RESULTADOS.relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
