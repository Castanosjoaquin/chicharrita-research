"""N9 - El manifiesto del paquete que se le puede mostrar al investigador.

Que resuelve. La carta del 2026-10-25 cierra el tema: «esta perfecto que revisen antes los
archivos derivados de nuestros proyectos. Me interesa conocer su implementacion, pero no
necesitan compartir datos internos de EpiLab ni archivos intermedios de nuestros disenos»
`[R]`. Entonces el paquete se acota a codigo y pruebas, y lo que hay que poder mostrar es
**que esta adentro, que no, y con que verificacion**.

El manifiesto se genera de `git ls-files` sobre los dos directorios del paquete, cruzado
con el reporte JSON de `tools/verificacion/sin_secuencias.py`. No copia nada: lista. Armar
el .zip es una decision del equipo y no de un script.

Uso (desde la raiz del repositorio):

    python tools/verificacion/sin_secuencias.py --json /ruta/libre/verif.json
    python research/ola5/N9_paquete_port/scripts/armar_manifiesto.py /ruta/libre/verif.json
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
SALIDA = AQUI.parents[1] / "resultados"

#: Lo que va. Son los dos directorios del port y de su interfaz, completos.
DENTRO = ["tools/sifi21_port", "sifi_plus"]

#: Lo que no va, y por que. Se chequea que ninguna ruta del paquete caiga adentro.
FUERA = {
    "work/": "insumos y salidas con las secuencias del laboratorio; no esta en git",
    "research/": "resultados derivados, incluidos los que tocan regiones de EPILAB",
    "baseline_dsrip/": "el CDS reconstruido de V-ATPase A (D60)",
    "YHat-Biotech/": "el corpus del Investigathon, que es material de ellos",
    "pipeline/salida/": "salidas intermedias del pipeline, en .gitignore",
}


def main(argv=None) -> int:
    ruta_json = Path(argv[0]) if argv else None
    archivos = subprocess.run(["git", "ls-files", *DENTRO], cwd=RAIZ, check=True,
                              capture_output=True, text=True).stdout.split()
    archivos = sorted(archivos)

    malos = [a for a in archivos if any(a.startswith(f) for f in FUERA)]
    if malos:
        raise SystemExit("hay rutas del paquete en la lista de lo que no va: %s" % malos)

    con_nt: dict[str, int] = {}
    no_exceptuados: list[str] = []
    if ruta_json and ruta_json.exists():
        rep = json.loads(ruta_json.read_text(encoding="utf-8"))
        dentro = set(archivos)
        for h in rep.get("hallazgos", []):
            a = h.get("archivo")
            if a in dentro:
                con_nt[a] = con_nt.get(a, 0) + 1
                if not h.get("exceptuado"):
                    no_exceptuados.append(a)
        if no_exceptuados:
            raise SystemExit(
                "el paquete tiene hallazgos de nucleotidos sin exceptuar: %s"
                % sorted(set(no_exceptuados)))

    SALIDA.mkdir(parents=True, exist_ok=True)
    lineas = ["# Manifiesto del paquete del port", "",
              "Generado por `scripts/armar_manifiesto.py`. %d archivos." % len(archivos), ""]
    for a in archivos:
        marca = "  **con nucleotidos (%d hallazgos, todos exceptuados)**" % con_nt[a] \
            if a in con_nt else ""
        lineas.append("- `%s`%s" % (a, marca))
    lineas += ["", "## Lo que no va", ""]
    for f, por_que in FUERA.items():
        lineas.append("- `%s` — %s" % (f, por_que))
    (SALIDA / "manifiesto.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")

    print("%d archivos en el paquete" % len(archivos))
    print("%d con nucleotidos, todos exceptuados con su motivo:" % len(con_nt))
    for a, n in sorted(con_nt.items()):
        print("   %-44s %d hallazgos" % (a, n))
    if not ruta_json:
        print("AVISO: sin el JSON de sin_secuencias.py no se pudo cruzar la verificacion")
    print("manifiesto en %s" % (SALIDA / "manifiesto.md"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
