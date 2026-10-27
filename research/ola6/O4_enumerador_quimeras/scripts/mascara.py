"""O4 — la mascara de veto por ventana, que es lo que vuelve finita la grilla.

**El criterio no lo elige este archivo: lo fija `PREREGISTRO.md` §4.** Una ventana queda
vetada si tiene coincidencia perfecta de 21 nt contra el panel de **seis** referencias no
objetivo —la humana incluida con peso 1,00, via `ranking_v2.con_panel(sin_humano=False)`— y
con el genoma de *Dalbulus maidis* **excluido por ser on-target** cuando el gen es del
insecto, que es lo que hace `ranking.excluidas_de()` con `estrategia="insecto"`.

Por que la mascara se calcula una vez por gen y no por candidato: el estado de off-target de
una ventana depende solo de sus 21 nt (`C13` §6), asi que el riesgo de las ventanas heredadas
**se hereda**. Lo que no se hereda es lo que el empalme fabrica, y eso se tamiza aparte, por
candidato, en `enumerar_quimeras.py`.

Un fragmento es admisible si **ninguna** de sus ventanas esta vetada, de modo que los
fragmentos admisibles de largo `l` son las rachas de ventanas no vetadas de largo `l - 20`.
Se leen de la mascara en una pasada, y es la poda que hace enumerable el problema: en
`V-ATPase B` sobrevive **una** region de 300 nt de las 1.184 que caben en su CDS (`D74`).

Entrada: las salidas de `offtarget_21nt.py` sobre el **gen entero**, no sobre una region. El
panel esta repartido en dos corridas porque la humana vive en otro directorio, igual que en
`O3`. Ninguna sale de la maquina y ninguna se versiona.

Uso como ancla 3 del preregistro (verifica `V-ATPase B` contra `D74`):
    python research/ola6/O4_enumerador_quimeras/scripts/mascara.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[4]
TRABAJO = RAIZ / "work/O4"

sys.path.insert(0, str(RAIZ / "tools/sifi21_port"))
import ranking as R      # noqa: E402  el motor de W7, sin tocarlo
import ranking_v2 as V   # noqa: E402  solo para fijar el panel

VENTANA = 21
#: §4 del preregistro: el veto es el criterio mas fuerte de los tres del port.
CRITERIO_VETO = "perfecto_21"
#: Los dos tamizados del panel de seis, en el orden en que los produjo la linea.
TAMIZADOS = [TRABAJO / "offtarget" / "offtarget_por_sirna.tsv",
             TRABAJO / "offtarget_humano" / "offtarget_por_sirna.tsv"]


def leer_fasta_simple(ruta: Path) -> tuple[str, str]:
    """Devuelve (nombre de la cabecera, secuencia). El nombre es la clave del tamizado."""
    lineas = Path(ruta).read_text().splitlines()
    nombre = lineas[0][1:].split()[0]
    return nombre, "".join(l.strip() for l in lineas[1:] if not l.startswith(">"))


def panel_de_seis() -> list[str]:
    """Las seis referencias no objetivo, con la humana adentro. Aborta si no son seis."""
    V.con_panel(sin_humano=False)
    refs = list(R.REFERENCIAS)
    if len(refs) != 6:
        raise SystemExit("el panel tiene %d referencias y el preregistro declara seis: %s"
                         % (len(refs), ", ".join(refs)))
    return refs


def mascara_de(consulta: str, n_ventanas: int, estrategia: str = "insecto",
               tamizados: list[Path] | None = None) -> tuple[np.ndarray, dict]:
    """Vector booleano de ventanas vetadas, y el detalle por referencia.

    `n_ventanas` es `largo_del_gen - 20` y se exige exacto: un tamizado que cubra una
    region y no el gen entero no sirve para enumerar fragmentos en todo el gen, y el modo
    de falla seria silencioso y optimista.
    """
    refs = panel_de_seis()
    excluidas = R.excluidas_de({"estrategia": estrategia}, "off")
    cuenta = {r: 0 for r in refs}
    vetada = np.zeros(n_ventanas, dtype=bool)
    vistas = 0
    for ruta in (tamizados or TAMIZADOS):
        if not Path(ruta).exists():
            raise SystemExit("falta el tamizado %s; corre offtarget_21nt.py sobre el gen "
                             "entero antes de enumerar" % ruta)
        with Path(ruta).open(encoding="utf-8") as fh:
            lector = csv.DictReader(fh, delimiter="\t")
            cols = [c for c in (lector.fieldnames or [])
                    if c.endswith("|" + CRITERIO_VETO)
                    and c.split("|", 1)[0] in refs
                    and c.split("|", 1)[0] not in excluidas]
            propias = 0
            for fila in lector:
                if fila["consulta"] != consulta:
                    continue
                propias += 1
                p = int(fila["pos"])
                if not 1 <= p <= n_ventanas:
                    raise SystemExit("%s: la ventana %d no cabe en %d"
                                     % (consulta, p, n_ventanas))
                for c in cols:
                    if int(fila[c] or 0) > 0:
                        vetada[p - 1] = True
                        cuenta[c.split("|", 1)[0]] += 1
            if propias != n_ventanas:
                raise SystemExit("%s trae %d ventanas en %s y el gen tiene %d: el tamizado "
                                 "no cubre el gen entero" % (consulta, propias, ruta,
                                                             n_ventanas))
        vistas += 1
    detalle = {"referencias_del_panel": refs, "excluidas_on_target": sorted(excluidas),
               "criterio": CRITERIO_VETO, "tamizados": vistas,
               "ventanas": int(n_ventanas), "vetadas": int(vetada.sum()),
               "por_referencia": {R.corto(r): n for r, n in cuenta.items() if n}}
    return vetada, detalle


def rachas_admisibles(vetada: np.ndarray) -> list[tuple[int, int]]:
    """Los tramos maximales de ventanas no vetadas, en coordenadas de ventana 1-based."""
    rachas, inicio = [], None
    for i, v in enumerate(vetada):
        if not v and inicio is None:
            inicio = i + 1
        elif v and inicio is not None:
            rachas.append((inicio, i))
            inicio = None
    if inicio is not None:
        rachas.append((inicio, len(vetada)))
    return rachas


def fragmentos_admisibles(vetada: np.ndarray, largo: int, paso: int = 1,
                          desde: int = 1, hasta: int | None = None) -> list[int]:
    """Arranques 1-based de los fragmentos de `largo` nt sin ninguna ventana vetada.

    Un fragmento `[a, a + largo - 1]` contiene las ventanas `a` a `a + largo - 21`, asi
    que es admisible si esa racha entera esta libre. `desde`/`hasta` restringen la busqueda
    a un tramo del gen, que es lo que usan las anclas para fijar coordenadas exactas.
    """
    if largo < VENTANA:
        raise SystemExit("un fragmento de %d nt no llega a una ventana de %d"
                         % (largo, VENTANA))
    n_gen = len(vetada) + VENTANA - 1
    tope = min(n_gen - largo + 1, (hasta or n_gen) - largo + 1)
    salida = []
    for a in range(max(1, desde), tope + 1, paso):
        if not vetada[a - 1:a + largo - VENTANA].any():
            salida.append(a)
    return salida


def _ancla_vatpase_b() -> int:
    """Ancla 3 del preregistro, contra `D74`: 71 ventanas vetadas, una region de 300 nt.

    `D74` midio sobre el CDS de `V-ATPase B`: **71** ventanas con coincidencia perfecta de
    21 nt, **una** region admisible de 300 nt —517-816, sin un nucleotido de holgura— de
    las 1.184 que caben, y **ninguna** a 301 nt.
    """
    fasta = RAIZ / "work/O3/fasta/VATPaseB_Dm_full.fasta"
    if not fasta.exists():
        raise SystemExit("falta %s; es el CDS que regenera O2" % fasta)
    consulta, seq = leer_fasta_simple(fasta)
    vetada, detalle = mascara_de(consulta, len(seq) - VENTANA + 1)
    de300 = fragmentos_admisibles(vetada, 300)
    de301 = fragmentos_admisibles(vetada, 301)
    caben = len(seq) - 300 + 1
    print("V-ATPase B: %d nt, %d ventanas, %d vetadas"
          % (len(seq), len(vetada), detalle["vetadas"]))
    print("  por referencia: %s" % detalle["por_referencia"])
    print("  regiones de 300 nt: %d admisibles de %d que caben -> %s"
          % (len(de300), caben, ", ".join("%d-%d" % (a, a + 299) for a in de300) or "ninguna"))
    print("  regiones de 301 nt: %d admisibles" % len(de301))
    fallas = []
    if detalle["vetadas"] != 71:
        fallas.append("vetadas: D74 dice 71 y aca son %d" % detalle["vetadas"])
    if de300 != [517]:
        fallas.append("regiones de 300: D74 dice una sola, 517-816, y aca son %s"
                      % ([("%d-%d" % (a, a + 299)) for a in de300] or "ninguna"))
    if de301:
        fallas.append("regiones de 301: D74 dice ninguna y aca son %d" % len(de301))
    if caben != 1184:
        fallas.append("caben: D74 dice 1.184 regiones de 300 nt y aca caben %d" % caben)
    for f in fallas:
        print("  ANCLA FALLA  %s" % f)
    print("  ancla 3: %s" % ("PASA" if not fallas else "FALLA"))
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(_ancla_vatpase_b())
