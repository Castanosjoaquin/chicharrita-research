"""O4 — las cuatro anclas de `PREREGISTRO.md` §7. Si alguna falla, la linea para.

Las cuatro, con lo que verifica cada una:

1. **Contra `C13` §5.** Las doce quimeras de las coordenadas vigentes, comparadas **celda
   por celda** contra la tabla publicada `quimeras_eficiencia_vigentes_corregido_vienna.tsv`.
   Es la mas fuerte, porque esa tabla tiene diecisiete columnas y no las produjo este
   codigo. No necesita tamizado: mide eficiencia y contabilidad.
2. **Contra `O3` y `D74`.** La quimera `BicC_Dm` 922-1221 + `V-ATPase B` 517-816 en los dos
   ordenes: 41 y 40 ventanas eficientes contra 40 de la suma de las partes, el bloque
   fabricado de 19 nt **solo** en el orden `V-ATPase B` + `BicC_Dm`, ninguna de sus ventanas
   eficiente, y cero fabricados en el orden inverso. Esta si tamiza el panel de seis, asi
   que tarda unos minutos.
3. **Contra la mascara de veto**, en marco 1, que es donde `D74` es reproducible. La corre
   `mascara.py` y aca se la invoca.
4. **Motor en proceso contra motor por linea de comandos.** La misma molecula evaluada por
   las dos vias tiene que dar la misma lista de ventanas eficientes, ventana por ventana.
   Es lo que autoriza a plegar miles de candidatos sin pasar por `run_sifi.py`.

**Sobre la suma que hace el ancla 1 y la feature no hace.** `C13` publica
`ef_quimera_total`, que suma ventanas heredadas y de juntura en una cifra. `D67` decidio que
la feature **no** publique esa suma, y el criterio de terminado del issue #24 lo repite. El
ancla la calcula igual, porque comparar contra una tabla publicada exige reproducir su
columna: la suma vive aca, en la verificacion, y no en la salida del enumerador.

Uso:
    python research/ola6/O4_enumerador_quimeras/scripts/00_anclas.py
    python research/ola6/O4_enumerador_quimeras/scripts/00_anclas.py --sin-tamizado
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import enumerar_quimeras as EQ   # noqa: E402
import mascara as MA             # noqa: E402

C13 = (RAIZ / "research/ola3/C13_quimeras_region_recomendada/resultados"
       / "quimeras_eficiencia_vigentes_corregido_vienna.tsv")
FULL = RAIZ / "work/sifi_check"
TAMIZADO_EPILAB = [FULL / "offtarget_full" / "offtarget_por_sirna.tsv"]

#: Las coordenadas vigentes de los cuatro genes de EPILAB, las mismas de `C13`.
VIGENTES = {"MP_MRFV": (72, 271), "CP_MRFV": (99, 298),
            "BicC_Dm": (922, 1221), "ATPaseD_Dm": (72, 371)}
#: Columnas de la tabla de `C13` y de donde sale cada una en nuestras filas.
EQUIVALENCIAS = {
    "largo_nt": lambda f: f["largo_total_nt"],
    "corte_nt": lambda f: f["l1"],
    "ventanas_quimera": lambda f: f["ventanas_molecula"],
    "ef_region_izq": lambda f: f["ef_fragmento_izq_solo"],
    "ef_region_der": lambda f: f["ef_fragmento_der_solo"],
    "suma_de_partes": lambda f: f["suma_de_las_partes"],
    "ef_quimera_total": lambda f: f["ef_heredadas"] + f["ef_juntura"],
    "ef_heredadas_izq": lambda f: f["ef_heredadas_izq"],
    "ef_heredadas_der": lambda f: f["ef_heredadas_der"],
    "ventanas_empalme": lambda f: f["ventanas_juntura"],
    "ef_empalme": lambda f: f["ef_juntura"],
    "ventanas_heredadas_que_cambiaron": lambda f: f["heredadas_que_cambiaron"],
}


def genes_epilab() -> dict:
    genes = {}
    for nombre in VIGENTES:
        ruta = FULL / ("%s_full.fasta" % nombre)
        if not ruta.exists():
            raise SystemExit("falta %s" % ruta)
        consulta, seq = MA.leer_fasta_simple(ruta)
        genes[nombre] = {"nombre": nombre, "consulta": consulta, "seq": seq,
                         "n": len(seq), "desde": 1, "hasta": len(seq),
                         "ruta": str(ruta.relative_to(RAIZ))}
    return genes


def fila_de(c: dict, genes: dict, cache: dict) -> dict:
    """Una fila de contabilidad para un par ya fijado, sin tamizado de juntura."""
    for gen, ini, largo in ((c["izq"], c["a1"], c["l1"]), (c["der"], c["a2"], c["l2"])):
        cache.setdefault((gen, ini, largo),
                         EQ.perfil(genes[gen]["seq"][ini - 1:ini + largo - 1]))
    qseq = (genes[c["izq"]]["seq"][c["a1"] - 1:c["a1"] + c["l1"] - 1]
            + genes[c["der"]]["seq"][c["a2"] - 1:c["a2"] + c["l2"] - 1])
    f = {"quimera": "Q_%s__%s" % (c["izq"], c["der"]),
         "izquierda": c["izq"], "derecha": c["der"], "l1": c["l1"],
         "largo_total_nt": c["l1"] + c["l2"]}
    f.update(EQ.cuentas_de(c, genes, EQ.perfil(qseq),
                           cache[(c["izq"], c["a1"], c["l1"])],
                           cache[(c["der"], c["a2"], c["l2"])], None))
    return f


def ancla_1() -> list[str]:
    """Las doce quimeras vigentes contra la tabla de `C13`, celda por celda."""
    if not C13.exists():
        return ["no esta la tabla de C13 (%s)" % C13]
    with C13.open(encoding="utf-8") as fh:
        publicada = {r["quimera"]: r for r in csv.DictReader(fh, delimiter="\t")}
    genes = genes_epilab()
    cache, malas, filas = {}, [], []
    for izq in VIGENTES:
        for der in VIGENTES:
            if izq == der:
                continue
            a1, b1 = VIGENTES[izq]
            a2, b2 = VIGENTES[der]
            filas.append(fila_de({"izq": izq, "der": der, "a1": a1, "l1": b1 - a1 + 1,
                                  "a2": a2, "l2": b2 - a2 + 1}, genes, cache))
    for f in filas:
        esperada = publicada.get(f["quimera"])
        if esperada is None:
            malas.append("%s no esta en la tabla de C13" % f["quimera"])
            continue
        for col, saca in EQUIVALENCIAS.items():
            if str(saca(f)) != str(esperada[col]):
                malas.append("%s %s: C13=%s aca=%s"
                             % (f["quimera"], col, esperada[col], saca(f)))
    # Las dos sumas que el preregistro nombra ademas de las celdas.
    juntura = sum(f["ventanas_juntura"] for f in filas)
    ef_juntura = sum(f["ef_juntura"] for f in filas)
    cambiadas = sum(f["heredadas_que_cambiaron"] for f in filas)
    print("  ancla 1: %d filas x %d columnas contra C13; juntura %d ventanas, %d "
          "eficientes; heredadas que cambiaron %d"
          % (len(filas), len(EQUIVALENCIAS), juntura, ef_juntura, cambiadas))
    if (juntura, ef_juntura, cambiadas) != (240, 4, 61):
        malas.append("las tres sumas de C13 §5 son 240/4/61 y aca son %d/%d/%d"
                     % (juntura, ef_juntura, cambiadas))
    return malas


def ancla_2() -> list[str]:
    """`O3` y `D74`: los dos ordenes, los totales y el bloque fabricado. Tamiza el panel."""
    genes = {}
    for nombre, ruta, tramo in (
            ("BicC_Dm", "work/O3/fasta/BicC_Dm_full.fasta", (922, 1221)),
            ("VATPaseB_Dm", "work/O3/fasta/VATPaseB_Dm_full.fasta", (517, 816))):
        genes[nombre] = EQ.leer_gen("%s=%s:%d-%d" % (nombre, ruta, *tramo))
    cands = [{"izq": "BicC_Dm", "der": "VATPaseB_Dm", "a1": 922, "l1": 300,
              "a2": 517, "l2": 300},
             {"izq": "VATPaseB_Dm", "der": "BicC_Dm", "a1": 517, "l1": 300,
              "a2": 922, "l2": 300}]
    junturas = EQ.tamizar_junturas(cands, genes)
    cache, malas = {}, []
    esperado = {"Q_BicC_Dm__VATPaseB_Dm": {"total": 40, "fab21": 0, "fab19": 0},
                "Q_VATPaseB_Dm__BicC_Dm": {"total": 41, "fab21": 0, "fab19": 1}}
    for i, c in enumerate(cands):
        f = fila_de(c, genes, cache)
        f.update(EQ.cuentas_de(c, genes,
                               EQ.perfil(genes[c["izq"]]["seq"][c["a1"] - 1:c["a1"] + 299]
                                         + genes[c["der"]]["seq"][c["a2"] - 1:c["a2"] + 299]),
                               cache[(c["izq"], c["a1"], 300)],
                               cache[(c["der"], c["a2"], 300)], junturas.get(i)))
        total = f["ef_heredadas"] + f["ef_juntura"]
        e = esperado[f["quimera"]]
        print("  ancla 2: %-28s total %d, suma de partes %d, fab21 %d, fab19 %d, "
              "fabricados en ventana eficiente %d"
              % (f["quimera"], total, f["suma_de_las_partes"], f["fabricados_21_refs"],
                 f["fabricados_ge19_refs"], f["fabricados_en_ventana_eficiente"]))
        if total != e["total"]:
            malas.append("%s: D74 dice %d eficientes y aca son %d"
                         % (f["quimera"], e["total"], total))
        if f["suma_de_las_partes"] != 40:
            malas.append("%s: D74 dice 40 de suma de las partes y aca son %d"
                         % (f["quimera"], f["suma_de_las_partes"]))
        if (f["fabricados_21_refs"], f["fabricados_ge19_refs"]) != (e["fab21"], e["fab19"]):
            malas.append("%s: D74 dice fab21=%d fab19=%d y aca son %d y %d"
                         % (f["quimera"], e["fab21"], e["fab19"],
                            f["fabricados_21_refs"], f["fabricados_ge19_refs"]))
        if f["fabricados_en_ventana_eficiente"]:
            malas.append("%s: D74 dice que ninguna ventana con bloque fabricado es "
                         "eficiente y aca son %d"
                         % (f["quimera"], f["fabricados_en_ventana_eficiente"]))
    return malas


def ancla_4() -> list[str]:
    """El motor en proceso contra `run_sifi.py`, ventana por ventana."""
    g = EQ.leer_gen("BicC_Dm=work/O3/fasta/BicC_Dm_full.fasta")
    seq = g["seq"][921:1221] + g["seq"][1521:1821]
    tmp = RAIZ / "work/O4" / "ancla_motor"
    tmp.mkdir(parents=True, exist_ok=True)
    (tmp / "m.fasta").write_text(">m\n%s\n" % seq, encoding="utf-8")
    r = subprocess.run([sys.executable, str(RAIZ / "tools/sifi21_port/run_sifi.py"),
                        str(tmp / "m.fasta"), "--modo", EQ.MODO,
                        "--backend", EQ.BACKEND, "--salida", str(tmp)],
                       cwd=str(RAIZ), text=True, capture_output=True)
    if r.returncode != 0:
        return ["run_sifi.py fallo con codigo %d: %s" % (r.returncode, r.stderr[-400:])]
    ruta = tmp / ("m_%s_%s.tsv" % (EQ.MODO, EQ.BACKEND))
    with ruta.open(encoding="utf-8") as fh:
        cli = {int(f["pos"]): str(f["is_efficient"]).strip().lower() in ("true", "1")
               for f in csv.DictReader(fh, delimiter="\t")}
    proceso = EQ.perfil(seq)
    distintas = [p for p in cli if cli[p] != proceso.get(p)]
    print("  ancla 4: %d ventanas comparadas, %d distintas" % (len(cli), len(distintas)))
    if len(cli) != len(proceso):
        return ["el motor en proceso da %d ventanas y la linea de comandos %d"
                % (len(proceso), len(cli))]
    return (["el motor en proceso difiere de run_sifi.py en %d ventanas: %s"
             % (len(distintas), distintas[:8])] if distintas else [])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sin-tamizado", action="store_true", dest="sin_tamizado",
                    help="saltea el ancla 2, que es la unica que escanea el panel")
    a = ap.parse_args(argv)

    # Las cuatro regiones de EPILAB tienen su tamizado en work/sifi_check/, no en work/O4/.
    MA.TAMIZADOS = TAMIZADO_EPILAB
    print("anclas de O4, PREREGISTRO.md §7")
    malas = {"1 (C13 §5, doce quimeras)": ancla_1()}
    if not a.sin_tamizado:
        malas["2 (O3 y D74)"] = ancla_2()
    else:
        print("  ancla 2: salteada por --sin-tamizado")
    MA.TAMIZADOS = [RAIZ / "work/O4" / "offtarget" / "offtarget_por_sirna.tsv",
                    RAIZ / "work/O4" / "offtarget_humano" / "offtarget_por_sirna.tsv"]
    malas["3 (mascara de veto, marco 1)"] = (
        [] if MA._ancla_vatpase_b() == 0 else ["la mascara no reproduce D74 en marco 1"])
    malas["4 (motor en proceso contra CLI)"] = ancla_4()

    print()
    fallo = False
    for nombre, lista in malas.items():
        print("ancla %s: %s" % (nombre, "PASA" if not lista else "FALLA"))
        for m in lista[:10]:
            print("    %s" % m)
        fallo = fallo or bool(lista)
    if fallo:
        print("\nAlguna ancla no pasa. Por el §7 del preregistro la linea para aca y no "
              "lee ningun numero nuevo.")
    return 1 if fallo else 0


if __name__ == "__main__":
    sys.exit(main())
