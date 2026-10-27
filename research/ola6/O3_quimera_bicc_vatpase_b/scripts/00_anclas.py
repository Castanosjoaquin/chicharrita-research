"""O3 paso 0 — las tres anclas de `PREREGISTRO.md` §6, antes de leer cualquier numero nuevo.

«Si una de esas anclas no pasa y no se arregla con la generalizacion, esta linea para y lo
dice, sin leer ningun numero nuevo» (§6). Este script es ese freno, y devuelve 1 si alguna
falla.

Las tres:

A. **Contra C4.** `quimeras_v2.py --conjunto epilab` reproduce la tabla de las doce quimeras
   de C4, fila por fila, en los **dos** modos. La verificacion la hace el propio evaluador,
   que aborta si no la reproduce; aca se corre y se mira el codigo de salida.
B. **Contra C13 §5.** `--conjunto vigentes --modo corregido` reproduce la tabla versionada
   de C13 celda por celda, con las tres sumas que el preregistro nombra
   (`ATPaseD_Dm`+`MP_MRFV` 47 -> 50, `MP_MRFV`+`ATPaseD_Dm` 47 -> 44, `CP_MRFV`+`MP_MRFV`
   50 -> 46), 4 ventanas de juntura eficientes y 61 heredadas cambiadas.
C. **Contra el nivel 3 de C7.** `ranking.ejes()` sigue dando los cuatro conteos (38, 21,
   35, 21) y sus `buenos_limpios` (37, 20, 34, 17) sobre los datos ya versionados de
   `work/sifi_check/`. Es el ancla de que el motor del criterio no cambio de comportamiento,
   y vale doble porque `tools/sifi21_port/ranking.py` lo edito la sesion del issue #30: si
   esta ancla falla, lo primero que se revisa es esa edicion.

Las dos primeras corren el evaluador **despues** de generalizarlo, que es lo que §6 pide.

Uso (desde la raiz del repositorio):
    python research/ola6/O3_quimera_bicc_vatpase_b/scripts/00_anclas.py
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EVALUADOR = RAIZ / "research/ola3/C13_quimeras_region_recomendada/scripts/quimeras_v2.py"
C13 = RAIZ / "research/ola3/C13_quimeras_region_recomendada/resultados"
SIFI_CHECK = RAIZ / "work/sifi_check"

sys.path.insert(0, str(RAIZ / "tools/sifi21_port"))
import ranking as R  # noqa: E402

#: §6, ancla C. Region del nivel 3 de C7 -> (eficientes, buenos_limpios).
ANCLA_C7 = {
    "MP_MRFV": ((72, 271), 38, 37),
    "CP_MRFV": ((99, 298), 21, 20),
    "BicC_Dm": ((2121, 2420), 35, 34),
    "ATPaseD_Dm": ((72, 371), 21, 17),
}
#: §6, ancla B. Las tres sumas que el preregistro nombra, mas los dos totales.
ANCLA_C13 = {
    "Q_ATPaseD_Dm__MP_MRFV": (47, 50),
    "Q_MP_MRFV__ATPaseD_Dm": (47, 44),
    "Q_CP_MRFV__MP_MRFV": (50, 46),
}


def leer_tsv(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def correr(args: list[str]) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(EVALUADOR), *args]
    return subprocess.run(cmd, cwd=str(RAIZ), text=True, capture_output=True)


def ancla_a(fallas: list[str]) -> None:
    print("A. contra C4, los dos modos")
    for modo in ("fiel", "corregido"):
        r = correr(["--conjunto", "epilab", "--modo", modo, "--backend", "vienna"])
        ok = r.returncode == 0 and "VERIFICACION: reproduce la tabla de C4" in r.stdout
        linea = next((l for l in r.stdout.splitlines() if "VERIFICACION" in l), "")
        print("   modo %-10s %s  %s" % (modo, "OK " if ok else "FALLA", linea.strip()))
        if not ok:
            fallas.append("ancla A, modo %s" % modo)
            print(r.stdout[-1500:]); print(r.stderr[-1500:])


def ancla_b(fallas: list[str]) -> None:
    print("\nB. contra C13 seccion 5, conjunto vigentes, modo corregido")
    r = correr(["--conjunto", "vigentes", "--modo", "corregido", "--backend", "vienna"])
    if r.returncode != 0:
        fallas.append("ancla B: el evaluador fallo")
        print("   FALLA: el evaluador fallo\n%s" % r.stderr[-1500:])
        return
    # El evaluador acaba de reescribir el archivo, asi que la tabla recien calculada es la
    # del disco y la de referencia es la que esta versionada en git.
    recien = {f["quimera"]: f
              for f in leer_tsv(C13 / "quimeras_eficiencia_vigentes_corregido_vienna.tsv")}
    g = subprocess.run(["git", "show",
                        "HEAD:research/ola3/C13_quimeras_region_recomendada/resultados/"
                        "quimeras_eficiencia_vigentes_corregido_vienna.tsv"],
                       cwd=str(RAIZ), text=True, capture_output=True)
    if g.returncode != 0:
        fallas.append("ancla B: no pude leer la tabla versionada de git")
        print("   FALLA: %s" % g.stderr.strip())
        return
    publicado = {f["quimera"]: f for f in
                 csv.DictReader(g.stdout.splitlines(), delimiter="\t")}
    distintas = 0
    for q, pub in publicado.items():
        act = recien.get(q)
        if act is None:
            distintas += 1
            print("   FALTA %s" % q)
            continue
        for col, v in pub.items():
            if str(act.get(col)) != str(v):
                distintas += 1
                print("   DISTINTO %-26s %-28s versionado=%s ahora=%s"
                      % (q, col, v, act.get(col)))
    print("   tabla de 12 filas x %d columnas: %s"
          % (len(next(iter(publicado.values()))),
             "identica a la versionada" if not distintas
             else "%d celdas distintas" % distintas))
    if distintas:
        fallas.append("ancla B: la tabla cambio")

    for q, (suma, total) in ANCLA_C13.items():
        f = recien.get(q, {})
        ok = (int(f.get("suma_de_partes", -1)) == suma
              and int(f.get("ef_quimera_total", -1)) == total)
        print("   %-26s %d -> %d  %s" % (q, suma, total, "OK" if ok else "FALLA"))
        if not ok:
            fallas.append("ancla B: %s" % q)
    emp = sum(int(f["ef_empalme"]) for f in recien.values())
    flips = sum(int(f["ventanas_heredadas_que_cambiaron"]) for f in recien.values())
    print("   ventanas de juntura eficientes: %d (espera 4)   heredadas cambiadas: %d "
          "(espera 61)" % (emp, flips))
    if (emp, flips) != (4, 61):
        fallas.append("ancla B: juntura %d / flips %d" % (emp, flips))


def ancla_c(fallas: list[str]) -> None:
    print("\nC. contra el nivel 3 de C7, con ranking.ejes() sobre los datos versionados")
    perfil = SIFI_CHECK / "salida"
    off = SIFI_CHECK / "offtarget_full" / "offtarget_por_sirna.tsv"
    mm1 = str(SIFI_CHECK / "offtarget_mm1_{gen}" / "offtarget_por_sirna.tsv")
    if not off.exists():
        fallas.append("ancla C: falta %s" % off)
        print("   FALLA: falta %s; `work/` no se versiona" % off)
        return
    wr, wc = R.pesos_base()
    print("   %-12s %-12s %6s %6s %8s %8s" % ("gen", "region", "efic", "espera",
                                              "lim+ef", "espera"))
    for c in R.CANDIDATOS:
        gen = c["gen"]
        (ini, fin), n_esp, bl_esp = ANCLA_C7[gen]
        g = R.cargar_gen(gen, perfil, off, mm1)
        e = R.ejes(g, ini, fin, wr, wc, R.excluidas_de(c, "off"), False)
        ok = (e["eficientes"], e["buenos_limpios"]) == (n_esp, bl_esp)
        print("   %-12s %-12s %6d %6d %8d %8d  %s"
              % (gen, "%d-%d" % (ini, fin), e["eficientes"], n_esp,
                 e["buenos_limpios"], bl_esp, "OK" if ok else "FALLA"))
        if not ok:
            fallas.append("ancla C: %s" % gen)


def main() -> int:
    fallas: list[str] = []
    ancla_a(fallas)
    ancla_b(fallas)
    ancla_c(fallas)
    print()
    if fallas:
        print("ANCLAS ROTAS (%d): %s" % (len(fallas), "; ".join(fallas)))
        print("La linea para aca: no se lee ningun numero nuevo (PREREGISTRO §6).")
        return 1
    print("las tres anclas de PREREGISTRO.md seccion 6 pasaron")
    return 0


if __name__ == "__main__":
    sys.exit(main())
