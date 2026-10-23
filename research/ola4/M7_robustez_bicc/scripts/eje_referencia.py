"""M7 eje 2 - la ventaja de `BicC_Dm` 922-1221 frente a la referencia que se use.

Que contesta. Si la secuencia del gen se toma de otra fuente, cambian dos cosas a la vez:
la eficiencia predicha (porque cambia la secuencia con la que se pliega y se calcula el
dG) y la coincidencia (cuantas de las ventanas eficientes existen identicas en esa
fuente). Este script recalcula las dos para las tres regiones de 300 nt que compiten
—922-1221, 2121-2420 y 264-563— contra cuatro fuentes:

  GHCC01   transcriptoma de huevos y cuerpo entero, Argentina (CeBio Pergamino, 2015)
  GITV01   transcriptoma, Ohio State University
  GCWP01   transcriptoma, Illinois Natural History Survey; **cubre solo fragmentos**
  genoma   GCA_975739785.1 (Reino Unido, cromosomico), como fuente de coordenadas

El ensamblado ONT de Cordoba (GCA_054756405.1) no entra: por D25 se reporta y no decide.
El haplotipo 2 (GCA_975739835.1) no se usa: esta incompleto en estos loci.

Metodo, y en que se diferencia de C8. C8 alineo con `PairwiseAligner` de Biopython contra
los contigs que W5 habia ubicado a mano. Aca el alineamiento es **blastn local** contra las
bases que ya estan armadas en `work/W5/db/`, sin lista de contigs escrita a mano, y de cada
HSP se leen las dos secuencias alineadas para reconstruir posicion por posicion como se ve
el gen en esa fuente. Nada sale de la maquina: las bases son locales y la consulta nunca
se sube a ningun servicio.

De los HSPs se arma, por posicion del gen: si la fuente la cubre, con que base, y si hay
discontinuidad con la posicion siguiente. Una discontinuidad dentro de un transcriptoma es
un indel; en el genoma es un empalme, y por eso se cuenta aparte: la ventana existe en el
transcrito y no existe como tramo contiguo del genoma.

Por ventana de 21 nt quedan cuatro estados: `identica`, `variante` (algun desajuste o
indel), `cruza_empalme` (solo en el genoma) y `sin_datos` (la fuente no cubre las 21
posiciones). **Una region con ventanas `sin_datos` no se compara: se declara no corrida.**
Es la trampa de `GCWP01`, que cubre fragmentos: ahi una region puede "ganar" por falta de
cobertura y no por merito.

La eficiencia se recalcula sobre la molecula recortada de 300 nt **tal como la escribe cada
fuente**, con ViennaRNA 2.7.2, tabla NN3 y el punto por defecto (brecha 1,0, accesibilidad
0,1, u = 8, 22 C), en los dos modos. Los conteos de este script no son comparables con los
de RNAplfold 2.1.5.

Uso (desde la raiz del repositorio, con blastn en el PATH):

    python research/ola4/M7_robustez_bicc/scripts/eje_referencia.py

El TSV crudo de blastn lleva las secuencias alineadas, asi que se escribe fuera del
repositorio (`/tmp/m7_blast/`) y no se versiona.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve()
RAIZ = AQUI.parents[4]
SALIDA = AQUI.parents[1] / "resultados"
TRABAJO = Path("/tmp/m7_blast")
sys.path.insert(0, str(RAIZ / "tools" / "sifi21_port"))
sys.path.insert(0, str(AQUI.parent))
from grilla_parametros import (ACC_GRID, DEF_ACC, DEF_END, K, MODOS,  # noqa: E402
                               REGIONES, RIVALES, FOCO, eficientes, leer_fasta, primitivos)

CONSULTA = RAIZ / "work" / "W5" / "fasta" / "BicC_Dm_full.fasta"
GEN_RNA = RAIZ / "work" / "W5" / "plfold" / "BicC_Dm.rna.fa"
BASES = {
    "GHCC01 (Argentina, Pergamino)": "TSA_GHCC01",
    "GITV01 (Ohio State)": "TSA_GITV01",
    "GCWP01 (Illinois)": "TSA_GCWP01",
    "genoma UK GCA_975739785.1": "GCA_975739785.1_ihDalMaid1.1_genomic",
}
ES_GENOMA = {"genoma UK GCA_975739785.1"}
COLS = ("qseqid sseqid pident length mismatch gapopen qstart qend sstart send "
        "sstrand bitscore evalue qseq sseq")


def correr_blast(db: str) -> list[dict]:
    salida = TRABAJO / ("%s.hsp.tsv" % db)
    TRABAJO.mkdir(parents=True, exist_ok=True)
    if not salida.exists():
        cmd = ["blastn", "-query", str(CONSULTA), "-db", str(RAIZ / "work" / "W5" / "db" / db),
               "-outfmt", "6 " + COLS, "-evalue", "1e-20", "-num_threads", "4",
               "-max_target_seqs", "20"]
        salida.write_text(subprocess.run(cmd, capture_output=True, text=True,
                                         check=True).stdout, encoding="utf-8")
    campos = COLS.split()
    filas = []
    for linea in salida.read_text(encoding="utf-8").splitlines():
        if not linea.strip():
            continue
        d = dict(zip(campos, linea.split("\t")))
        for c in ("length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send"):
            d[c] = int(d[c])
        for c in ("pident", "bitscore"):
            d[c] = float(d[c])
        filas.append(d)
    return filas


def mapear(hsps: list[dict], n: int) -> dict:
    """Por posicion del gen: cobertura, base de la fuente, identidad y discontinuidades.

    Los HSPs se aplican de mejor a peor puntaje y solo sobre posiciones todavia libres,
    de modo que un solapamiento no pisa al mejor alineamiento.
    """
    cubierta = np.zeros(n, dtype=bool)
    identica = np.zeros(n, dtype=bool)
    base = [""] * n              # lo que la fuente escribe en esa posicion ("" = delecion)
    inserto = [""] * n           # lo que la fuente agrega DESPUES de esa posicion
    de_hsp = np.full(n, -1, dtype=int)
    contigs = {}
    for i, h in enumerate(sorted(hsps, key=lambda x: -x["bitscore"])):
        q = h["qstart"] - 1
        ultimo = None   # ultima posicion que ESTE HSP escribio, para colgarle la insercion
        for qc, sc in zip(h["qseq"], h["sseq"]):
            if qc == "-":
                # insercion de la fuente: no consume posicion del gen
                if ultimo is not None:
                    inserto[ultimo] += sc
                continue
            if not cubierta[q]:
                cubierta[q] = True
                de_hsp[q] = i
                base[q] = "" if sc == "-" else sc
                identica[q] = (sc == qc)
                ultimo = q
            q += 1
        contigs[h["sseqid"]] = contigs.get(h["sseqid"], 0) + 1
    # Discontinuidad entre i e i+1: distinto HSP, o el mismo HSP con una insercion.
    salto_hsp = np.zeros(n, dtype=bool)      # cambio de bloque alineado (empalme o indel grande)
    salto_ins = np.zeros(n, dtype=bool)      # insercion de la fuente entre i e i+1
    for i in range(n - 1):
        if cubierta[i] and cubierta[i + 1] and de_hsp[i] != de_hsp[i + 1]:
            salto_hsp[i] = True
        if inserto[i]:
            salto_ins[i] = True
    return {"cubierta": cubierta, "identica": identica, "base": base, "inserto": inserto,
            "salto_hsp": salto_hsp, "salto_ins": salto_ins, "contigs": contigs,
            "de_hsp": de_hsp}


def estado_ventanas(m: dict, n: int, es_genoma: bool) -> np.ndarray:
    """0 sin datos, 1 identica, 2 variante, 3 cruza un empalme (solo genoma)."""
    out = np.zeros(n - K + 1, dtype=np.int8)
    for i in range(n - K + 1):
        tramo = slice(i, i + K)
        if not m["cubierta"][tramo].all():
            out[i] = 0
            continue
        cruza_hsp = m["salto_hsp"][i:i + K - 1].any()
        if cruza_hsp and es_genoma:
            out[i] = 3
            continue
        hay_ins = m["salto_ins"][i:i + K - 1].any()
        delecion = any(m["base"][j] == "" for j in range(i, i + K))
        out[i] = 1 if (m["identica"][tramo].all() and not hay_ins and not delecion
                       and not cruza_hsp) else 2
    return out


def secuencia_segun_fuente(m: dict, ini: int, fin: int) -> str | None:
    """La region [ini, fin] tal como la escribe la fuente, o None si no la cubre entera.

    Las inserciones internas de la fuente se conservan (son variacion); un salto entre
    bloques alineados **no** se rellena: en el genoma es un intron, y lo que queda es el
    transcrito empalmado segun esa referencia.
    """
    if not m["cubierta"][ini - 1:fin].all():
        return None
    partes = []
    for i in range(ini - 1, fin):
        partes.append(m["base"][i])
        if i < fin - 1:
            partes.append(m["inserto"][i])
    return "".join(partes)


def conteos(seq: str) -> dict:
    """Eficientes de una molecula recortada, por modo, en el punto por defecto."""
    P = primitivos(seq, "vienna", "NN3")
    return {modo: int(eficientes(P, modo, DEF_END, DEF_ACC).sum()) for modo in MODOS}


def main() -> int:
    SALIDA.mkdir(parents=True, exist_ok=True)
    gen = leer_fasta(GEN_RNA)
    n = len(gen)
    nv = n - K + 1

    # Las ventanas eficientes de la secuencia de EPILAB, en contexto, con las que se
    # miden las coincidencias. Motor y tabla declarados; los dos modos.
    P_gen = primitivos(gen, "vienna", "NN3")
    eff_ctx = {modo: eficientes(P_gen, modo, DEF_END, DEF_ACC) for modo in MODOS}

    res = {"motor": "ViennaRNA 2.7.2, tabla NN3, punto por defecto (brecha 1,0, "
                    "accesibilidad 0,1, u = 8, 22 C)",
           "consulta": str(CONSULTA.relative_to(RAIZ)).replace("\\", "/"),
           "alineamiento": "blastn local, evalue 1e-20, bases de work/W5/db/",
           "fuentes": {}, "regiones": {k: list(v) for k, v in REGIONES.items()},
           "eficientes_epilab_contexto": {
               modo: {nom: int(eff_ctx[modo][ini - 1:fin].sum())
                      for nom, (ini, fin) in REGIONES.items()} for modo in MODOS}}
    filas = []
    for etiqueta, db in BASES.items():
        hsps = correr_blast(db)
        m = mapear(hsps, n)
        es_gen = etiqueta in ES_GENOMA
        est = estado_ventanas(m, n, es_gen)
        res["fuentes"][etiqueta] = {
            "base": db, "hsps": len(hsps), "contigs": m["contigs"],
            "posiciones_cubiertas": int(m["cubierta"].sum()), "posiciones": n,
            "ventanas_identicas": int((est == 1).sum()),
            "ventanas_variantes": int((est == 2).sum()),
            "ventanas_que_cruzan_empalme": int((est == 3).sum()),
            "ventanas_sin_datos": int((est == 0).sum()), "ventanas": nv,
            "es_genoma": es_gen}
        for nom, (ini, fin) in REGIONES.items():
            sl = slice(ini - 1, fin)
            e_reg = est[sl]
            fila = {"fuente": etiqueta, "region": nom,
                    "ventanas_region": int(len(e_reg)),
                    "sin_datos": int((e_reg == 0).sum()),
                    "identicas": int((e_reg == 1).sum()),
                    "variantes": int((e_reg == 2).sum()),
                    "cruzan_empalme": int((e_reg == 3).sum())}
            for modo in MODOS:
                ef = eff_ctx[modo][sl]
                fila["eficientes_epilab_%s" % modo] = int(ef.sum())
                fila["efic_identicas_%s" % modo] = int((ef & (e_reg == 1)).sum())
                fila["efic_variantes_%s" % modo] = int((ef & (e_reg == 2)).sum())
                fila["efic_cruzan_empalme_%s" % modo] = int((ef & (e_reg == 3)).sum())
                fila["efic_sin_datos_%s" % modo] = int((ef & (e_reg == 0)).sum())
            seq = secuencia_segun_fuente(m, ini, fin)
            if seq is None:
                fila["recalculo"] = "no corrido: la fuente no cubre la region entera"
                for modo in MODOS:
                    fila["recalc_%s" % modo] = ""
                fila["largo_segun_fuente"] = ""
            else:
                c = conteos(seq)
                fila["recalculo"] = "corrido"
                fila["largo_segun_fuente"] = len(seq)
                for modo in MODOS:
                    fila["recalc_%s" % modo] = c[modo]
            filas.append(fila)

    # Conteos de la molecula de EPILAB recortada, para comparar contra el recalculo.
    rec_epilab = {}
    for nom, (ini, fin) in REGIONES.items():
        rec_epilab[nom] = conteos(gen[ini - 1:fin])
    res["recorte_epilab"] = rec_epilab

    # Quien gana por fuente, cuando la fuente permite comparar las tres regiones.
    veredicto = {}
    for etiqueta in BASES:
        sub = {f["region"]: f for f in filas if f["fuente"] == etiqueta}
        comparables = [r for r in REGIONES if sub[r]["recalculo"] == "corrido"]
        v = {"regiones_comparables": comparables}
        if FOCO in comparables:
            for modo in MODOS:
                v["recalculo_%s" % modo] = {
                    "gana_a": [r for r in RIVALES if r in comparables
                               and sub[FOCO]["recalc_%s" % modo] > sub[r]["recalc_%s" % modo]],
                    "pierde_con": [r for r in RIVALES if r in comparables
                                   and sub[FOCO]["recalc_%s" % modo] < sub[r]["recalc_%s" % modo]],
                    "conteos": {r: sub[r]["recalc_%s" % modo] for r in comparables}}
        # La conservacion se puede leer aunque la region no se pueda recalcular entera,
        # pero solo entre regiones con cobertura completa de ventanas.
        con_cobertura = [r for r in REGIONES if sub[r]["sin_datos"] == 0]
        v["regiones_con_cobertura_total_de_ventanas"] = con_cobertura
        for modo in MODOS:
            v["coincidencias_%s" % modo] = {
                r: {"eficientes": sub[r]["eficientes_epilab_%s" % modo],
                    "identicas": sub[r]["efic_identicas_%s" % modo],
                    "variantes": sub[r]["efic_variantes_%s" % modo],
                    "cruzan_empalme": sub[r]["efic_cruzan_empalme_%s" % modo],
                    "sin_datos": sub[r]["efic_sin_datos_%s" % modo]} for r in REGIONES}
        veredicto[etiqueta] = v
    res["veredicto"] = veredicto

    cols = list(filas[0].keys())
    with (SALIDA / "referencia_por_region.tsv").open("w", encoding="utf-8") as fh:
        fh.write("\t".join(cols) + "\n")
        for f in filas:
            fh.write("\t".join(str(f.get(c, "")) for c in cols) + "\n")
    (SALIDA / "referencia_resumen.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

    for etiqueta in BASES:
        f = res["fuentes"][etiqueta]
        print("%-32s cubre %d/%d nt | ventanas id %d, var %d, empalme %d, sin datos %d"
              % (etiqueta, f["posiciones_cubiertas"], f["posiciones"],
                 f["ventanas_identicas"], f["ventanas_variantes"],
                 f["ventanas_que_cruzan_empalme"], f["ventanas_sin_datos"]), flush=True)
    for f in filas:
        print("  %-32s %-10s sin_datos %3d id %3d var %3d emp %3d | recalc corregido %s"
              % (f["fuente"], f["region"], f["sin_datos"], f["identicas"], f["variantes"],
                 f["cruzan_empalme"], f.get("recalc_corregido", "")), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
