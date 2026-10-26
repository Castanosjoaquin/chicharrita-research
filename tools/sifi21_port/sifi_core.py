"""Criterio de eficiencia de si-Fi21, portado a Python 3 y corriendo sin interfaz grafica.

Origen: si-Fi21 (Luck et al. 2019, Front Plant Sci 10:1023), modulo sifi_pipeline.py.
Repositorio: github.com/snowformatics/siFi21-

Dos modos, seleccionables:

  modo "fiel"     reproduce el programa original tal como es, incluidas sus rarezas.
                  Sirve para auditar numeros producidos con si-Fi.
  modo "corregido" aplica los arreglos documentados en CAMBIOS.md.
                  Es el que usamos para diseñar.

Sobre Bowtie: en el original el calculo de eficiencia esta dentro de un
`if strand == '+'`, asi que Bowtie decide QUE ventanas se registran, pero el
veredicto de eficiencia de cada ventana no depende de Bowtie en absoluto
(`calculate_efficiency` recibe solo la secuencia y la accesibilidad). En el uso
normal del modo diseño la base contiene el gen consultado, todas las ventanas
tienen un hit perfecto en hebra +, y entonces el conteo de eficientes es funcion
unicamente de la secuencia. Este modulo calcula ese perfil completo. El tamizaje
de off-targets con Bowtie es un paso separado, no incluido aca.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, asdict

from Bio.Seq import Seq

from sifi_energy import TABLAS_NN, free_energy

# Valores por defecto de la interfaz del original (main.py:329-339 y 354-363).
DEFAULTS = {
    "sirna_size": 21,
    "end_stability_threshold": 1.0,
    "accessibility_threshold": 0.1,
    "accessibility_window": 8,
    "strand_check": True,
    "end_check": True,
    "accessibility_check": True,
    "terminal_check": True,
}

# Constantes fijadas en el codigo del original (sifi_pipeline.py:60-65).
WINSIZE = 80        # RNAplfold -W
SPAN = 40           # RNAplfold -L
TEMPERATURE = 22.0  # C; usada tanto para dG como para RNAplfold
OVERHANG = 2
END_NUCLEOTIDES = 3

# Donde esta el RNAplfold 2.1.5, que es el binario con el que corre el original.
#
# `SIFI_RNAPLFOLD` manda siempre que este definida: es la forma de apuntar a un binario
# compilado a mano fuera de Windows (la linea M2 lo compila desde el tag v2.1.5 del fuente
# oficial, con la receta del encabezado de research/ola4/M2_ventana_a_ventana/scripts/
# correr_pares.py).
#
# Sin esa variable se prueban las ubicaciones conocidas en Windows, en orden. Hasta M11 la
# unica era `ToCopy\RNAplfold\`, y eso daba un falso «no disponible» en la maquina donde el
# original efectivamente corrio: `ToCopy\` es la carpeta DESDE la cual el instalador copia,
# no donde deja el binario. El instalador de si-Fi2015 lo deja bajo `%LOCALAPPDATA%\siFi2015\`
# (research/ola4/M1_conteo_y_referencia/REPORT.md §1), asi que esa va primero.
#
# No se busca un `RNAplfold` suelto en el PATH, y es a proposito: el que este en el PATH es
# casi seguro un ViennaRNA moderno, este backend se llama «2.1.5» en la interfaz, y los dos
# motores no dan lo mismo. Elegir un binario de otra version por conveniencia convertiria la
# etiqueta del motor en una mentira. Para eso esta la variable de entorno, que es explicita.


def _rutas_rnaplfold() -> list[str]:
    local = os.environ.get("LOCALAPPDATA", "")
    rutas = []
    if local:
        rutas.append(os.path.join(local, "siFi2015", "RNAplfold", "RNAplfold.exe"))
        rutas.append(os.path.join(local, "siFi2015", "RNAplfold.exe"))
    rutas.append(r"C:\Program Files (x86)\siFi21\ToCopy\RNAplfold\RNAplfold.exe")
    return rutas


RUTAS_RNAPLFOLD = _rutas_rnaplfold()


def resolver_rnaplfold() -> str:
    """La ruta del RNAplfold 2.1.5 a usar: la variable de entorno, o la primera que exista.

    Si no existe ninguna devuelve la ultima candidata, para que el mensaje de error pueda
    nombrar una ruta concreta en vez de quedarse en «no se encontro».
    """
    desde_env = os.environ.get("SIFI_RNAPLFOLD")
    if desde_env:
        return desde_env
    for ruta in RUTAS_RNAPLFOLD:
        if os.path.isfile(ruta):
            return ruta
    return RUTAS_RNAPLFOLD[-1]


RNAPLFOLD_EXE = resolver_rnaplfold()


@dataclass
class Window:
    """Una ventana de siRNA con su veredicto y los terminos que lo producen.

    Sobre los tres campos de la regla terminal (`nt19_at`, `nt2_gc`, `rama_terminal`):
    son **categorias y no los nucleotidos**, y la diferencia es deliberada. La linea M9
    midio que una columna con la letra de una posicion fija de la ventana, concatenada
    sobre ventanas que se solapan de a 1 nt, es una subcadena literal del gen: `nt19` y
    `nt2` juntas reconstruyen el 99,4 % de un gen de 500 nt sin producir ni una racha de
    21 nt que un escaner pueda ver. Las categorias que la regla efectivamente usa son
    `nt19 in (A,T)` y `nt2 in (G,C)`, o sea un bit por posicion en vez de dos, asi que
    conservan **todo** el poder predictivo de la regla y no permiten escribir la
    secuencia. Aun asi la cadena de bits es informacion parcial del gen, de modo que la
    tabla de `--features` no se versiona: se genera local. Ver `research/ola4/
    M9_auditoria_secuencias/REPORT.md` §3.5 y el issue #7.
    """
    pos: int                  # posicion de inicio, 1-based
    seq: str
    dg_sense5: float
    dg_antisense5: float
    ddg: float                # antisense - sense
    accessibility: float
    nt19_at: bool             # el nucleotido 19 es A o T (la preferencia del 5' de la guia)
    nt2_gc: bool              # el nucleotido 2 es G o C
    rama_terminal: int        # 1 a 4, cual de las cuatro ramas de la regla se aplico
    strand_selection: bool
    end_stability: bool
    target_site_accessibility: bool
    thermo_efficient: bool
    is_efficient: bool


# Las cuatro ramas de `_terminal_rule`, numeradas como pide el issue #7. La 2 es el
# atajo que la auditoria encontro y que Diego confirmo: en modo fiel decide mirando
# solo la accesibilidad y se saltea el veredicto termodinamico.
RAMAS_TERMINALES = {
    1: "nt19 A/T y nt2 A/T: decide la termodinamica",
    2: "nt19 A/T y nt2 G/C: ATAJO, decide solo la accesibilidad (modo fiel)",
    3: "nt19 G/C y nt2 G/C: decide la termodinamica",
    4: "nt19 G/C y nt2 A/T: no eficiente, sin mirar nada mas",
}


def rama_terminal(nt19_at: bool, nt2_gc: bool) -> int:
    """Cual de las cuatro ramas de la regla terminal aplica. Ver RAMAS_TERMINALES."""
    if nt19_at:
        return 1 if not nt2_gc else 2
    return 3 if nt2_gc else 4


# --- Accesibilidad ----------------------------------------------------------

def accessibility_vienna(sequence: str, sirna_size: int, temp_c: float = TEMPERATURE):
    """Perfil de probabilidad de estar desapareado, con las ligaduras de ViennaRNA.

    Devuelve `up` tal que up[i][u] = P(el tramo de largo u que termina en la
    posicion i, 1-based, esta desapareado).
    """
    import RNA
    RNA.cvar.temperature = temp_c
    rna = sequence.upper().replace("T", "U")
    return RNA.pfl_fold_up(rna, sirna_size, WINSIZE, SPAN)


def accessibility_exe(sequence: str, sirna_size: int, temp_c: float = TEMPERATURE,
                      exe: str = RNAPLFOLD_EXE, name: str = "query"):
    """Idem, pero invocando el RNAplfold.exe que trae la instalacion de si-Fi.

    Es el binario que el original usa (ViennaRNA 2.1.5). Se incluye para poder
    medir cuanto cambia el resultado por la version de ViennaRNA.
    """
    if not os.path.exists(exe):
        raise FileNotFoundError("no se encontro RNAplfold.exe en %r" % exe)
    work = tempfile.mkdtemp(prefix="plfold_")
    try:
        fasta = ">%s\n%s\n" % (name, sequence.upper())
        subprocess.run(
            [exe, "-W", str(WINSIZE), "-L", str(SPAN),
             "-u", str(sirna_size), "-T", "%.2f" % temp_c],
            input=fasta.encode(), cwd=work,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True,
        )
        lunp = None
        for fn in os.listdir(work):
            if fn.endswith("_lunp"):
                lunp = os.path.join(work, fn)
                break
        if lunp is None:
            raise RuntimeError("RNAplfold no produjo archivo _lunp en %r" % work)

        # Formato: posicion, luego una columna por cada u = 1..sirna_size.
        up = [None]  # indice 0 sin usar, para que up[i] sea 1-based
        with open(lunp) as fh:
            for line in fh:
                s = line.strip()
                # El encabezado de RNAplfold viene como ' #$i  l=1  2  3 ...',
                # con un espacio delante del '#', asi que hay que normalizar antes.
                if not s or s.startswith("#"):
                    continue
                parts = s.split()
                row = [float("nan")]  # idem, up[i][0] sin usar
                for v in parts[1:]:
                    row.append(float("nan") if v == "NA" else float(v))
                up.append(row)
        return up
    finally:
        shutil.rmtree(work, ignore_errors=True)


# --- Motor ------------------------------------------------------------------

class SifiEngine:
    def __init__(self, mode: str = "fiel", temp_c: float = TEMPERATURE, **kw):
        if mode not in ("fiel", "corregido"):
            raise ValueError("mode debe ser 'fiel' o 'corregido'")
        self.mode = mode
        self.temp_c = temp_c
        p = dict(DEFAULTS)
        p.update(kw)
        self.p = p
        self.size = p["sirna_size"]
        self.track: dict = {}
        # Tabla de apilamiento. NN3 es la del original; NN4 es la que usa sifi21INTA y
        # difiere de NN3 en 22 de sus 28 entradas.
        tabla = p.get("tabla_nn", "NN3")
        if tabla not in TABLAS_NN:
            raise ValueError("tabla_nn debe ser una de %s" % sorted(TABLAS_NN))
        self.tabla_nn = tabla
        self.nn_table = None if tabla == "NN3" else TABLAS_NN[tabla]

    # -- energias del original ---------------------------------------------

    def _dg(self, seq, c_seq=None, shift=0):
        # `nn_table` queda en None para NN3, que es el default real de si-Fi y el que
        # free_energy ya aplica; se pasa explicita solo cuando se pide otra tabla, como
        # la NN4 de sifi21INTA.
        return free_energy(seq, c_seq=c_seq, shift=shift, temp_c=self.temp_c,
                           nn_table=self.nn_table, track=self.track)

    def _ends_plain(self, sirna: str):
        """Sin extremos colgantes. El original lo usa para los dos primeros siRNA."""
        sense5 = sirna[0:END_NUCLEOTIDES]
        anti5 = sirna[self.size - OVERHANG - END_NUCLEOTIDES:self.size - OVERHANG]
        return self._dg(sense5), self._dg(anti5)

    def _ends_dangling(self, sirna: str, sirna_n2: str):
        """Con extremos colgantes, usando el siRNA de dos posiciones antes."""
        rc_n2 = str(Seq(sirna_n2).reverse_complement()).strip()
        sense5 = sirna[0:END_NUCLEOTIDES]
        sense_c = rc_n2[self.size - 5:self.size - 1]
        anti5 = rc_n2[0:END_NUCLEOTIDES]
        anti_c = sirna[self.size - 5:self.size - 1]
        return (self._dg(sense5, c_seq=sense_c[::-1], shift=1),
                self._dg(anti5, c_seq=anti_c[::-1], shift=1))

    # -- composicion de reglas ---------------------------------------------

    def _thermo_efficient(self, strand_sel, end_stab, access):
        """Conjuncion de los filtros que esten activados (original: check_efficient)."""
        active = []
        if self.p["strand_check"]:
            active.append(strand_sel)
        if self.p["end_check"]:
            active.append(end_stab)
        if self.p["accessibility_check"]:
            active.append(access)
        return all(active) if active else True

    def _terminal_rule(self, sirna, thermo, access):
        """Regla de los nucleotidos terminales.

        FIEL: reproduce sifi_pipeline.py:525-550. Es una rama, no un filtro: cuando
        el nucleotido 19 es A/T y el 2 no lo es, devuelve eficiente MIRANDO SOLO la
        accesibilidad, salteando el veredicto termodinamico.

        CORREGIDO: la preferencia terminal se aplica como filtro adicional sobre el
        veredicto termodinamico, que nunca se saltea. Justificacion en CAMBIOS.md (C1).
        """
        nt19 = sirna[self.size - 3]
        nt2 = sirna[1]

        if self.mode == "fiel":
            if nt19 in ("A", "T"):
                if nt2 in ("A", "T"):
                    return bool(thermo)
                if self.p["accessibility_check"]:
                    return bool(access)
                return True
            if nt2 in ("G", "C"):
                return bool(thermo)
            return False

        # corregido
        terminal_ok = (nt19 in ("A", "T")) or (nt2 in ("G", "C"))
        return bool(thermo) and terminal_ok

    # -- recorrido ----------------------------------------------------------

    def run(self, sequence: str, backend: str = "vienna"):
        """Calcula el perfil de eficiencia de toda la secuencia.

        Devuelve (ventanas, resumen).
        """
        seq = sequence.upper().replace("U", "T")
        seq = "".join(b for b in seq if b in "ACGT")
        n = len(seq)
        if n < self.size:
            raise ValueError("secuencia mas corta que la ventana")

        sirnas = [seq[i:i + self.size] for i in range(n - self.size + 1)]

        if backend == "vienna":
            up = accessibility_vienna(seq, self.size, self.temp_c)
        elif backend == "exe":
            up = accessibility_exe(seq, self.size, self.temp_c)
        else:
            raise ValueError("backend debe ser 'vienna' o 'exe'")

        u = self.p["accessibility_window"]
        windows = []
        for idx, sirna in enumerate(sirnas):
            pos = idx + 1  # 1-based
            n2 = None if pos <= 2 else sirnas[pos - 3]

            if n2 is None:
                dg_s, dg_as = self._ends_plain(sirna)
            else:
                dg_s, dg_as = self._ends_dangling(sirna, n2)

            # El original lee la probabilidad del tramo de largo u que termina en
            # el ULTIMO nucleotido de la ventana (sifi_pipeline.py:252 y 360).
            access_val = up[pos + self.size - 1][u]

            strand_sel = dg_as >= dg_s
            end_stab = (dg_as - dg_s) >= self.p["end_stability_threshold"]
            access_ok = access_val >= self.p["accessibility_threshold"]
            thermo = self._thermo_efficient(strand_sel, end_stab, access_ok)

            if self.p["terminal_check"]:
                eff = self._terminal_rule(sirna, thermo, access_ok)
            else:
                eff = bool(thermo)

            # Las dos categorias que la regla terminal realmente usa, con los mismos
            # indices que `_terminal_rule`: posicion 19 (1-based) y posicion 2.
            nt19_at = sirna[self.size - 3] in ("A", "T")
            nt2_gc = sirna[1] in ("G", "C")

            windows.append(Window(
                pos=pos, seq=sirna,
                dg_sense5=round(dg_s, 4), dg_antisense5=round(dg_as, 4),
                ddg=round(dg_as - dg_s, 4),
                accessibility=round(access_val, 6),
                nt19_at=nt19_at, nt2_gc=nt2_gc,
                rama_terminal=rama_terminal(nt19_at, nt2_gc),
                strand_selection=strand_sel, end_stability=end_stab,
                target_site_accessibility=access_ok,
                thermo_efficient=thermo, is_efficient=eff,
            ))

        resumen = {
            "largo": n,
            "ventanas": len(windows),
            "eficientes": sum(w.is_efficient for w in windows),
            "solo_termodinamico": sum(w.thermo_efficient for w in windows),
            "seleccion_hebra": sum(w.strand_selection for w in windows),
            "estabilidad_extremos": sum(w.end_stability for w in windows),
            "accesibilidad": sum(w.target_site_accessibility for w in windows),
            "modo": self.mode,
            "temp_c": self.temp_c,
            "backend": backend,
            "tablas_mismatch_usadas": dict(self.track),
        }
        return windows, resumen


def primitives(sequence: str, temp_c: float = TEMPERATURE, backend: str = "vienna",
               sirna_size: int = 21):
    """Calcula una sola vez los terminos que no dependen de los umbrales.

    Separa lo caro (energias libres y plegado) de lo barato (comparar contra un
    umbral), para poder barrer configuraciones sin recalcular. Devuelve, por
    ventana: posicion, secuencia, dG de los dos extremos 5' y la fila completa de
    probabilidades de desapareamiento (indice = u).
    """
    eng = SifiEngine(mode="fiel", temp_c=temp_c, sirna_size=sirna_size)
    seq = sequence.upper().replace("U", "T")
    seq = "".join(b for b in seq if b in "ACGT")
    sirnas = [seq[i:i + sirna_size] for i in range(len(seq) - sirna_size + 1)]

    if backend == "vienna":
        up = accessibility_vienna(seq, sirna_size, temp_c)
    elif backend == "exe":
        up = accessibility_exe(seq, sirna_size, temp_c)
    else:
        raise ValueError("backend debe ser 'vienna' o 'exe'")

    out = []
    for idx, sirna in enumerate(sirnas):
        pos = idx + 1
        n2 = None if pos <= 2 else sirnas[pos - 3]
        if n2 is None:
            dg_s, dg_as = eng._ends_plain(sirna)
        else:
            dg_s, dg_as = eng._ends_dangling(sirna, n2)
        out.append({
            "pos": pos, "sirna": sirna, "dg_s": dg_s, "dg_as": dg_as,
            "lunp": list(up[pos + sirna_size - 1]),
        })
    return out


def apply_rules(prims, *, mode="fiel", u=8, end_thr=1.0, access_thr=0.1,
                strand_check=True, end_check=True, access_check=True,
                terminal_check=True, sirna_size=21) -> int:
    """Aplica las reglas a primitivos ya calculados y devuelve el conteo de eficientes."""
    n_eff = 0
    for p in prims:
        dg_s, dg_as = p["dg_s"], p["dg_as"]
        sirna = p["sirna"]
        strand_sel = dg_as >= dg_s
        end_stab = (dg_as - dg_s) >= end_thr
        access_val = p["lunp"][u]
        access_ok = (access_val == access_val) and access_val >= access_thr  # NaN -> False

        active = []
        if strand_check:
            active.append(strand_sel)
        if end_check:
            active.append(end_stab)
        if access_check:
            active.append(access_ok)
        thermo = all(active) if active else True

        if not terminal_check:
            eff = thermo
        else:
            nt19 = sirna[sirna_size - 3]
            nt2 = sirna[1]
            if mode == "fiel":
                if nt19 in ("A", "T"):
                    if nt2 in ("A", "T"):
                        eff = thermo
                    elif access_check:
                        eff = access_ok
                    else:
                        eff = True
                elif nt2 in ("G", "C"):
                    eff = thermo
                else:
                    eff = False
            else:
                eff = thermo and ((nt19 in ("A", "T")) or (nt2 in ("G", "C")))
        n_eff += bool(eff)
    return n_eff


def best_region(windows, length: int = 200):
    """Ventana deslizante: la region de `length` nt con mas siRNA eficientes.

    Es la decision que el investigador describio en el checkpoint: elegir la
    region con mayor densidad de eficientes.
    """
    eff = [w.pos for w in windows if w.is_efficient]
    if not eff:
        return None
    best, best_n = None, -1
    # Solo regiones completas: una que se pase del final del gen tendria menos
    # ventanas y competiria en desigualdad. Con los cuatro genes del corpus el
    # argmax cae dentro de este dominio, asi que acotarlo no cambia ningun numero
    # ya publicado; lo que evita es un artefacto en genes donde si caiga al final.
    last_start = max(1, max(w.pos for w in windows) - length + 1)
    for start in range(1, last_start + 1):
        end = start + length - 1
        k = sum(1 for p in eff if start <= p <= end)
        if k > best_n:
            best_n, best = k, (start, end)
    return {"inicio": best[0], "fin": best[1], "eficientes": best_n}


# Los seis terminos que el modelo usa, sin ningun booleano de veredicto. Es la tabla
# que pidio Diego: «conservar los valores termodinamicos, las preferencias terminales y
# la accesibilidad como variables independientes del proceso de clasificacion, para
# evaluar posteriormente como contribuyen a la eficiencia». `is_efficient` se agrega
# aparte como etiqueta, porque sin ella la tabla no sirve para ajustar nada.
COLUMNAS_FEATURES = [
    "pos",
    "dg_sense5",
    "dg_antisense5",
    "ddg",
    "accessibility",
    "nt19_at",
    "nt2_gc",
    "rama_terminal",
]


def to_tsv(windows, path, *, con_seq: bool = False, columnas=None):
    """Escribe un TSV por ventana.

    `seq` **no se emite por defecto**: es un 21-mero por ventana y, como las ventanas se
    solapan de a 1 nt, la columna reconstruye el gen entero. Fue el incidente de C9 y es
    lo que el gancho de `tools/verificacion/sin_secuencias.py` ahora rechaza. Quien la
    necesite para un paso local —`research/ola4/M1_conteo_y_referencia` la usa para armar
    las consultas de Bowtie— la pide con `con_seq=True` y **no versiona esa salida**.
    """
    todas = list(asdict(windows[0]).keys())
    if columnas is not None:
        cols = [c for c in columnas if c in todas]
    else:
        cols = [c for c in todas if c != "seq" or con_seq]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\t".join(cols) + "\n")
        for w in windows:
            d = asdict(w)
            fh.write("\t".join(str(d[c]) for c in cols) + "\n")
