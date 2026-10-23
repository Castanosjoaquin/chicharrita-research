"""Corre los pares de M2 que esta maquina puede correr, y declara el que no.

De los cuatro pares del issue #6, tres se corren aca con ViennaRNA 2.7.2 y uno no:

  1. `fiel` contra `corregido`              -> si
  2. `RNA_NN3` contra `RNA_NN4`             -> si (NN4 transcrita de sifi21INTA)
  3. RNAplfold 2.1.5 contra ViennaRNA 2.7.2 -> **NO**, ver abajo
  4. region recortada contra region en contexto -> si

Por que el 3 no corre. El backend `exe` del port invoca el `RNAplfold.exe` que trae el
instalador de si-Fi2015, que es un binario de Windows; en esta maquina no hay ningun
RNAplfold y ninguno de los TSV por ventana versionados es `_exe`. Compilar ViennaRNA
2.1.5 desde fuente no sirve como control, porque lo que el criterio de terminado pide es
reproducir numeros medidos con **ese** binario. Queda declarado como no corrido, no como
cero.

Consecuencia sobre los controles. El criterio de terminado pide que el par de modos
reproduzca 19, 7, 50 y 8 ventanas. Esos numeros son del backend `exe`; con ViennaRNA
2.7.2 el mismo par da 19, 9, 52 y 6. No es una discrepancia: es otro motor. El control
exacto necesita el mismo binario.

    python3 research/ola4/M2_ventana_a_ventana/scripts/correr_pares.py
"""

from __future__ import annotations

import json
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


def leer_fasta(ruta: Path) -> str:
    return "".join(l.strip() for l in ruta.read_text().splitlines()[1:])


def correr_port(fastas: list[Path], modo: str, destino: Path, tabla: str = "NN3") -> None:
    destino.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(RAIZ / "tools/sifi21_port/run_sifi.py"), *map(str, fastas),
           "--modo", modo, "--backend", "vienna", "--salida", str(destino)]
    if tabla != "NN3":
        cmd += ["--tabla-nn", tabla]
    r = subprocess.run(cmd, cwd=str(RAIZ), text=True, capture_output=True)
    if r.returncode != 0:
        print(r.stdout[-1500:], r.stderr[-1500:])
        raise SystemExit("run_sifi.py fallo")


def tsv(directorio: Path, gen: str, modo: str, sufijo: str = "") -> Path:
    cands = [p for p in sorted(directorio.glob(f"{gen}*_{modo}_vienna{sufijo}.tsv"))
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

    print("\npar 3 — RNAplfold 2.1.5 contra ViennaRNA 2.7.2: NO CORRIDO")
    print("  falta el binario del instalador de si-Fi2015; ver el encabezado")
    reporte["par3_motor"] = {
        "estado": "no corrido",
        "motivo": "el backend exe invoca el RNAplfold.exe del instalador de si-Fi2015, "
                  "que es un binario de Windows; no hay RNAplfold en esta maquina y "
                  "ningun TSV versionado es _exe",
        "que_haria_falta": "el binario, o los TSV por ventana con backend exe de los "
                           "cuatro genes",
    }

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
