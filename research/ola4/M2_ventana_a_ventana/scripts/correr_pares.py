"""Corre los pares de M2 que esta maquina puede correr, y declara el que no.

De los cuatro pares del issue #6, tres se corren aca con ViennaRNA 2.7.2 y uno no:

  1. `fiel` contra `corregido`              -> si
  2. `RNA_NN3` contra `RNA_NN4`             -> si (NN4 transcrita de sifi21INTA)
  3. RNAplfold 2.1.5 contra ViennaRNA 2.7.2 -> si, con el binario compilado (ver abajo)
  4. region recortada contra region en contexto -> si

Como corre el par 3 fuera de Windows. El backend `exe` del port invoca el `RNAplfold.exe`
del instalador de si-Fi2015. Ese binario **es ViennaRNA 2.1.5**, asi que se compila esa
version desde el tag `v2.1.5` del fuente oficial y se apunta el port con la variable de
entorno `SIFI_RNAPLFOLD`. Que la compilacion sea equivalente al binario del instalador no
se asume: se verifica, y se verifica con los cuatro conteos publicados --133, 32, 212 y
42-- y con el control de 19, 7, 50 y 8 del criterio de terminado. Los dos pasan exactos.

Receta de compilacion (macOS/Linux, unos minutos):

    git clone --depth 1 --branch v2.1.5 https://github.com/ViennaRNA/ViennaRNA.git
    cd ViennaRNA
    autoreconf -i                      # el repo no trae `configure`, solo configure.ac
    ./configure --without-perl --without-python --without-kinfold --without-forester \
                --without-rnalocmin --disable-openmp
    FLAGS="-O2 -Wno-implicit-int -Wno-error=implicit-int \
           -Wno-implicit-function-declaration -Wno-error=implicit-function-declaration \
           -Wno-int-conversion -Wno-error=int-conversion -Wno-return-type"
    make -C lib CFLAGS="$FLAGS" && make -C Progs RNAplfold CFLAGS="$FLAGS"

Las flags hacen falta porque el codigo es C89 con `register i;` sin tipo, que los clang
modernos rechazan por defecto. Requiere `autoconf`, `automake`, `libtool` y `gengetopt`.

    SIFI_RNAPLFOLD=/ruta/a/ViennaRNA/Progs/RNAplfold \
        python3 research/ola4/M2_ventana_a_ventana/scripts/correr_pares.py

Sin esa variable el script corre los tres pares que no dependen del binario y declara el
par 3 y el control numerico como no corridos, en vez de darlos por cero.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comparar_ventanas import comparar, escribir, leer  # noqa: E402

RAIZ = Path(__file__).resolve().parents[4]
SALIDA = Path(__file__).resolve().parents[1] / "resultados"
TRABAJO = Path("/tmp/m2_pares")
GENES = ["MP_MRFV", "CP_MRFV", "BicC_Dm", "ATPaseD_Dm"]

# Los genes completos, en ARN. Son los mismos insumos que uso W5.
FASTA_GEN = {g: RAIZ / "work" / "W5" / "plfold" / f"{g}.rna.fa" for g in GENES}

# Regiones vigentes al 2026-10-22, 1-based inclusive: iguales a las de C7 salvo
# `BicC_Dm`, que D25 movio de 2121-2420 a 922-1221 por conservacion (C8). Copiadas de
# `research/ola3/C13_quimeras_region_recomendada/scripts/quimeras_v2.py`, CONJUNTOS.
VIGENTES = {"MP_MRFV": (72, 271), "CP_MRFV": (99, 298),
            "BicC_Dm": (922, 1221), "ATPaseD_Dm": (72, 371)}

# El ancla de C9: los cuatro conteos del gen completo con ViennaRNA 2.7.2, por modo.
ANCLA = {"fiel": {"MP_MRFV": 142, "CP_MRFV": 39, "BicC_Dm": 223, "ATPaseD_Dm": 35},
         "corregido": {"MP_MRFV": 123, "CP_MRFV": 30, "BicC_Dm": 171, "ATPaseD_Dm": 29}}

# Los cuatro conteos publicados con RNAplfold 2.1.5, verificados en la ola 2 contra el
# programa original y de nuevo por M1 contra el gen mismo. Son el ancla que valida que el
# binario compilado equivale al del instalador.
ANCLA_EXE = {"fiel": {"MP_MRFV": 133, "CP_MRFV": 32, "BicC_Dm": 212, "ATPaseD_Dm": 42},
             "corregido": {"MP_MRFV": 114, "CP_MRFV": 25, "BicC_Dm": 162, "ATPaseD_Dm": 34}}

# El control que pide el criterio de terminado del issue, en el motor en que fue medido.
CONTROL_MODOS_EXE = {"MP_MRFV": 19, "CP_MRFV": 7, "BicC_Dm": 50, "ATPaseD_Dm": 8}

HAY_EXE = bool(os.environ.get("SIFI_RNAPLFOLD")) and Path(
    os.environ.get("SIFI_RNAPLFOLD", "")).exists()


def leer_fasta(ruta: Path) -> str:
    return "".join(l.strip() for l in ruta.read_text().splitlines()[1:])


def correr_port(fastas: list[Path], modo: str, destino: Path, tabla: str = "NN3",
                backend: str = "vienna") -> None:
    destino.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(RAIZ / "tools/sifi21_port/run_sifi.py"), *map(str, fastas),
           "--modo", modo, "--backend", backend, "--salida", str(destino)]
    if tabla != "NN3":
        cmd += ["--tabla-nn", tabla]
    r = subprocess.run(cmd, cwd=str(RAIZ), text=True, capture_output=True)
    if r.returncode != 0:
        print(r.stdout[-1500:], r.stderr[-1500:])
        raise SystemExit("run_sifi.py fallo")


def tsv(directorio: Path, gen: str, modo: str, sufijo: str = "",
        backend: str = "vienna") -> Path:
    cands = [p for p in sorted(directorio.glob(f"{gen}*_{modo}_{backend}{sufijo}.tsv"))
             if "_features" not in p.name]
    if not cands:
        raise SystemExit(f"no encontre el TSV de {gen} {modo}{sufijo} en {directorio}")
    return cands[0]


def main() -> int:
    TRABAJO.mkdir(parents=True, exist_ok=True)
    reporte: dict[str, dict] = {}

    # --- insumos -----------------------------------------------------------
    # Genes completos, los dos modos, tabla NN3 y NN4.
    dirs = {}
    for modo in ("fiel", "corregido"):
        d = TRABAJO / f"gen_{modo}_nn3"
        correr_port(list(FASTA_GEN.values()), modo, d)
        dirs[(modo, "NN3")] = d
        d4 = TRABAJO / f"gen_{modo}_nn4"
        correr_port(list(FASTA_GEN.values()), modo, d4, tabla="NN4")
        dirs[(modo, "NN4")] = d4

    # Control: el gen completo tiene que reproducir el ancla de C9 en los dos modos.
    for modo in ("fiel", "corregido"):
        for g in GENES:
            filas = leer(tsv(dirs[(modo, "NN3")], g, modo))
            n = sum(1 for f in filas.values() if f["is_efficient"] == "True")
            if n != ANCLA[modo][g]:
                raise SystemExit(f"ancla de C9: {g} {modo} dio {n}, se esperaban "
                                 f"{ANCLA[modo][g]}")
    print("ancla de C9 reproducida en los 8 casos (4 genes x 2 modos)")

    # Recortes: la region vigente extraida del gen y corrida por separado.
    dir_rec = {}
    for modo in ("fiel", "corregido"):
        rec_fastas = []
        for g in GENES:
            ini, fin = VIGENTES[g]
            seq = leer_fasta(FASTA_GEN[g])[ini - 1:fin]
            p = TRABAJO / f"{g}_rec.fa"
            p.write_text(f">{g}_rec\n{seq}\n")
            rec_fastas.append(p)
        d = TRABAJO / f"rec_{modo}"
        correr_port(rec_fastas, modo, d)
        dir_rec[modo] = d

    # --- pares -------------------------------------------------------------
    print("\npar 1 — fiel contra corregido (perfil del gen completo)")
    for g in GENES:
        res, camb = comparar(leer(tsv(dirs[("fiel", "NN3")], g, "fiel")),
                             leer(tsv(dirs[("corregido", "NN3")], g, "corregido")),
                             1, ("fiel", "corregido"))
        escribir(SALIDA / f"par1_modos_{g}", res, camb)
        reporte[f"par1_modos:{g}"] = res
        print(f"  {g:12s} fiel {res['eficientes_fiel']:4d} | corregido "
              f"{res['eficientes_corregido']:4d} | cambian {res['cambian']:3d}")

    # Los dos modos: el fiel es el que compara contra `sifi21INTA`, que corre la rama del
    # original; el corregido va igual para poder decir la direccion sobre el conjunto
    # completo y no sobre la mitad.
    print("\npar 2 — RNA_NN3 contra RNA_NN4")
    for modo in ("fiel", "corregido"):
        for g in GENES:
            res, camb = comparar(leer(tsv(dirs[(modo, "NN3")], g, modo)),
                                 leer(tsv(dirs[(modo, "NN4")], g, modo, "_nn4")),
                                 1, ("nn3", "nn4"))
            escribir(SALIDA / f"par2_tablas_{modo}_{g}", res, camb)
            reporte[f"par2_tablas:{g}:{modo}"] = res
            print(f"  {g:12s} {modo:10s} NN3 {res['eficientes_nn3']:4d} | NN4 "
                  f"{res['eficientes_nn4']:4d} | cambian {res['cambian']:3d}")

    print("\npar 3 — RNAplfold 2.1.5 contra ViennaRNA 2.7.2")
    if not HAY_EXE:
        print("  NO CORRIDO: falta SIFI_RNAPLFOLD apuntando a un RNAplfold 2.1.5")
        print("  la receta de compilacion esta en el encabezado de este script")
        reporte["par3_motor"] = {
            "estado": "no corrido",
            "motivo": "sin binario de RNAplfold 2.1.5; el backend exe del port apunta por "
                      "defecto al RNAplfold.exe del instalador de si-Fi2015, que es de "
                      "Windows",
            "que_haria_falta": "compilar el tag v2.1.5 y exportar SIFI_RNAPLFOLD",
        }
        reporte["control_modos_exe"] = {"estado": "no corrido", "motivo": "idem"}
    else:
        dirs_exe = {}
        for modo in ("fiel", "corregido"):
            d = TRABAJO / f"gen_{modo}_exe"
            correr_port(list(FASTA_GEN.values()), modo, d, backend="exe")
            dirs_exe[modo] = d

        # Ancla: el binario compilado tiene que dar los cuatro conteos publicados. Si no,
        # no equivale al del instalador y nada de lo que sigue vale.
        for modo in ("fiel", "corregido"):
            for g in GENES:
                filas = leer(tsv(dirs_exe[modo], g, modo, backend="exe"))
                n = sum(1 for f in filas.values() if f["is_efficient"] == "True")
                if n != ANCLA_EXE[modo][g]:
                    raise SystemExit(
                        f"el RNAplfold compilado NO equivale al del instalador: {g} {modo} "
                        f"dio {n}, se esperaban {ANCLA_EXE[modo][g]}")
        print("  ancla del backend exe reproducida: 133/32/212/42 y 114/25/162/34")

        for g in GENES:
            res, camb = comparar(leer(tsv(dirs_exe["fiel"], g, "fiel", backend="exe")),
                                 leer(tsv(dirs[("fiel", "NN3")], g, "fiel")),
                                 1, ("plfold215", "vienna272"))
            escribir(SALIDA / f"par3_motor_{g}", res, camb)
            reporte[f"par3_motor:{g}"] = res
            print(f"  {g:12s} 2.1.5 {res['eficientes_plfold215']:4d} | 2.7.2 "
                  f"{res['eficientes_vienna272']:4d} | cambian {res['cambian']:3d}")

        # El control numerico del criterio de terminado, en el motor en que fue medido.
        print("\ncontrol — par de modos con backend exe (criterio: 19, 7, 50 y 8)")
        for g in GENES:
            res, camb = comparar(leer(tsv(dirs_exe["fiel"], g, "fiel", backend="exe")),
                                 leer(tsv(dirs_exe["corregido"], g, "corregido",
                                          backend="exe")),
                                 1, ("fiel", "corregido"))
            escribir(SALIDA / f"control_modos_exe_{g}", res, camb)
            reporte[f"control_modos_exe:{g}"] = res
            marca = "OK" if res["cambian"] == CONTROL_MODOS_EXE[g] else "DIFIERE"
            print(f"  {g:12s} cambian {res['cambian']:3d} | criterio "
                  f"{CONTROL_MODOS_EXE[g]:3d}  {marca}")
            if marca == "DIFIERE":
                raise SystemExit(f"el control del par de modos fallo en {g}")

    print("\npar 4 — region recortada contra region en contexto (modo corregido)")
    for g in GENES:
        ini, _ = VIGENTES[g]
        res, camb = comparar(leer(tsv(dirs[("corregido", "NN3")], g, "corregido")),
                             leer(tsv(dir_rec["corregido"], g, "corregido")),
                             ini, ("contexto", "recorte"))
        escribir(SALIDA / f"par4_recorte_{g}", res, camb)
        reporte[f"par4_recorte:{g}"] = res
        print(f"  {g:12s} en contexto {res['eficientes_contexto']:4d} | recortada "
              f"{res['eficientes_recorte']:4d} | comparadas "
              f"{res['ventanas_comparadas']:4d} | cambian {res['cambian']:3d}")

    (SALIDA / "pares_resumen.json").write_text(
        json.dumps(reporte, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nescrito en {SALIDA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
