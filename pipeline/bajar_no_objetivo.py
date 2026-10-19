"""Baja los transcriptomas RefSeq de los organismos no objetivo del catalogo.

Usa los `_rna.fna.gz` de RefSeq, no los genomas: son un orden de magnitud mas
chicos y son lo correcto para off-target de RNAi, porque lo que importa es lo que
el organismo transcribe, no lo que tiene guardado en intrones.

Respeta el patron que ya habia (`maiz_rna.fna.gz`, `abeja_rna.fna.gz`): el nombre
del archivo sale de la columna `clave` del catalogo.

Uso:
    python3 bajar_no_objetivo.py <catalogo.csv> [--dir ~/yhat/data]
"""

from __future__ import annotations

import csv
import re
import sys
import urllib.request
from pathlib import Path


FTP = "https://ftp.ncbi.nlm.nih.gov/genomes/all"


def resolver_url(acc: str) -> str | None:
    """Resuelve la URL del `_rna.fna.gz` listando el directorio padre en el FTP.

    No se puede armar la URL a partir del `assembly_name` que devuelve la API:
    el nombre de la carpeta en el FTP es el del ensamblado VIGENTE y no siempre
    coincide. Verificado con el pez cebra, donde la API dice `GRCz12tu` y la
    carpeta real es `GCF_052040795.2_GRCz13ab`. Armar la URL a mano daba un 404
    que se guardaba como si fuera un .gz valido.
    """
    padre = f"{FTP}/{acc[:3]}/{acc[4:7]}/{acc[7:10]}/{acc[10:13]}/"
    try:
        with urllib.request.urlopen(padre, timeout=120) as r:
            html = r.read().decode("utf-8", "replace")
    except Exception:
        return None
    carpetas = re.findall(rf'({re.escape(acc)}_[A-Za-z0-9._-]+)/', html)
    if not carpetas:
        return None
    carpeta = sorted(set(carpetas))[-1]
    return f"{padre}{carpeta}/{carpeta}_rna.fna.gz"


def es_gzip(ruta: Path) -> bool:
    """Un .gz real arranca con 1f 8b. Una pagina de error de NCBI, no."""
    try:
        with ruta.open("rb") as f:
            return f.read(2) == bytes([0x1F, 0x8B])
    except OSError:
        return False


def bajar(url: str, destino: Path, acc: str = "") -> tuple[bool, int, str]:
    if destino.exists() and destino.stat().st_size > 0 and es_gzip(destino):
        return True, destino.stat().st_size, "ya estaba"
    destino.unlink(missing_ok=True)
    tmp = destino.with_suffix(destino.suffix + ".parcial")
    for intento, candidata in enumerate([url, resolver_url(acc) if acc else None]):
        if not candidata:
            continue
        try:
            with urllib.request.urlopen(candidata, timeout=600) as r, tmp.open("wb") as f:
                while True:
                    trozo = r.read(1 << 20)
                    if not trozo:
                        break
                    f.write(trozo)
        except Exception as e:
            tmp.unlink(missing_ok=True)
            if intento == 1:
                return False, 0, str(e)[:90]
            continue
        if not es_gzip(tmp):
            tmp.unlink(missing_ok=True)
            if intento == 1:
                return False, 0, "lo que bajo no es gzip (404 disfrazado?)"
            continue
        tmp.rename(destino)
        return True, destino.stat().st_size, "bajado" if intento == 0 else "bajado (url resuelta)"
    return False, 0, "no se pudo resolver la URL"


def main() -> int:
    catalogo = Path(sys.argv[1])
    base = Path.home() / "yhat" / "data"
    if "--dir" in sys.argv:
        base = Path(sys.argv[sys.argv.index("--dir") + 1]).expanduser()
    base.mkdir(parents=True, exist_ok=True)

    filas = list(csv.DictReader(catalogo.open(encoding="utf-8")))
    total = 0
    listos = []
    for fila in filas:
        if fila["estado"] != "ok":
            print(f"[--] {fila['especie']:<32}sin RefSeq, no hay que bajar")
            continue
        destino = base / f"{fila['clave']}_rna.fna.gz"
        ok, tam, nota = bajar(fila["url_rna"], destino, fila["refseq"])
        if ok:
            total += tam
            listos.append(destino)
            print(f"[ok] {fila['especie']:<32}{tam/1e6:>8.1f} MB  {nota}")
        else:
            print(f"[ER] {fila['especie']:<32}{nota}")

    print(f"\n{len(listos)} archivos, {total/1e6:.0f} MB en total")
    print("\nArgumentos para sirna_offtarget.py:")
    print(" ".join(str(p) for p in listos))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
